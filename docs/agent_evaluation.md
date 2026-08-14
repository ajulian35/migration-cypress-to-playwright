# Agent Evaluation — Cypress → Playwright Migration Agent

## Evaluation Criteria

The agent is evaluated against the following criteria. Each is **measurable** — not assessed by inspection of whether the code looks plausible.

| # | Criterion | Measurement method | Pass bar |
|---|---|---|---|
| C1 | Generated test runs without manual modification | `python -m pytest tests/step_defs/<req>_steps.py -v` on first execution | Exit code 0 |
| C2 | Selector resolves to exactly one element at migration time | `browser_snapshot` count for the selector before code is written | count == 1 |
| C3 | Assertion values match observed live behavior, not spec values | `assert` in the test matches the value the agent saw in the DOM snapshot | Passes against live app |
| C4 | Pre-condition setup is idempotent | Running the suite twice without cleaning up between runs produces 0 new failures | Exit code 0 on second run |
| C5 | No credentials or URLs hardcoded | `grep -r "admin123\|orangehrmlive" playwright/tests/ playwright/pages/` returns no matches | Zero matches |

### Measured results (this project, 8 requirements)

| Criterion | Result | Notes |
|---|---|---|
| C1 — first-run pass rate | 6/8 on initial generation | pre-001 and req-001 failed; fixed before final submission |
| C2 — selector validity | 8/8 after adjustments | 3 selectors were adjusted during Step 2 validation (password input, employee ID group, userdropdown) |
| C3 — assertion accuracy | 7/8 | req-001 originally used stale spec values (muser/Indian/Married); corrected to observed values |
| C4 — idempotency | 8/8 after fix | Original pre-001 was not idempotent; fixed by "already exists" handling in `click_save()` |
| C5 — no hardcoded secrets | Pass | All credentials via `os.environ.get()` / `Cypress.env()` |

---

## P7 — Failure Handling Protocol

### Tool output validation

The agent does not trust tool output. Specifically:

1. **`browser_snapshot` output** — before writing a selector as code, the agent counts how many elements match. If the count is not 1, the selector is rejected and an alternative is tried.
2. **`pytest` output** — after generating code, the agent reads the full pytest output. A passing exit code alone is not sufficient; the agent reads the test names and confirms all expected tests were collected and ran (not skipped or error-collected).
3. **URL redirect confirmation** — after `click_save()` or any form submission, the agent checks the resulting URL, not just that the page loaded. A page that loads successfully but stays on the form URL is treated as a failure.

### Retry protocol

When a step fails, the retry includes:
1. The original input (selector / action / assertion)
2. The exact error or unexpected output observed
3. A DOM excerpt (from `browser_snapshot` or `browser_evaluate`) showing the actual state

Example (Failure Case 2 below): the retry prompt included:
- Original: `page.locator('.oxd-input-field-error-message').all_text_contents()` → `[]`
- Observed: `wait_for_load_state("networkidle")` resolved; page URL still `pim/addEmployee`
- DOM state (from MCP Playwright evaluate): errors exist — `"Employee Id already exists"`, `"Username already exists"`

The retry used that DOM state to diagnose the timing issue and propose `wait_for_function()`.

### Escalation after repeated failure

After 2 consecutive failures on the same step, the agent stops generating and presents:
- The full sequence of attempts with their outputs
- The current DOM state
- An explicit request for human guidance

This prevents silent loops where the agent alternates between two broken approaches without making progress.

---

## P7 — Deliberate Failure Injection

### Failure injected: Vue timing race on form validation

**Setup:** `click_save()` in `AddEmployeePage` used `wait_for_load_state("networkidle")` followed immediately by reading `.oxd-input-field-error-message` elements.

**Injected condition:** The shared demo already had an employee with ID `0384` and username `qauser_001`. Clicking Save triggered Vue validation that rendered error messages 300–500ms after networkidle.

**Observed agent behavior:**

1. `click_save()` executed; `wait_for_load_state("networkidle")` resolved.
2. `locator('.oxd-input-field-error-message').all_text_contents()` returned `[]`.
3. Neither branch ("empNumber URL" nor "already exists") matched.
4. Agent raised: `AssertionError: Employee save failed unexpectedly. URL: …/pim/addEmployee. Errors: []`

**Why this is a tool output validation failure:** The Playwright `all_text_contents()` call returned an empty list — a valid return value that the agent initially trusted. The failure was not an exception but a semantically incorrect result (the errors existed but were not yet rendered).

**Recovery sequence:**

1. Agent navigated to the live page via MCP Playwright and reproduced the form submission manually.
2. Called `browser_evaluate` to inspect the DOM directly after clicking Save:
   ```js
   () => { return Array.from(document.querySelectorAll('.oxd-input-field-error-message'))
                        .map(e => e.innerText.trim()).filter(Boolean); }
   ```
   Result: `["Employee Id already exists", "Username already exists"]`
3. Diagnosis: errors exist in DOM but `all_text_contents()` read them before Vue's reactive update cycle completed.
4. Fix: replaced `wait_for_load_state("networkidle")` with `wait_for_function()` that polls until either the redirect URL or the first error element appears:
   ```python
   self.page.wait_for_function(
       "() => window.location.href.includes('empNumber/') || "
       "document.querySelector('.oxd-input-field-error-message') !== null",
       timeout=12000,
   )
   ```
5. Verification: `python -m pytest tests/step_defs/pre_001_steps.py -v` → PASSED.

**Evidence:** Commit `fe083bc` — `fix(pre-001): wait for Vue validation before checking error messages`

---

## P8 — Known Failure Cases

### Failure Case 1 — Employee ID collision (silent failure masking)

**Input:**
- Cypress `clickSave()` used an OR condition: `cy.url().should('include', '/pim/viewPersonalDetails/empNumber/').or.should('include', '/pim/addEmployee')`
- OrangeHRM auto-generated Employee ID was `0428` (already in use by another demo user)

**Wrong output:**
- `clickSave()` passed without error — the OR condition accepted `/pim/addEmployee` as valid
- The employee was NOT created; `qauser_001` did not exist
- All 7 downstream tests failed with login errors (user not found)

**Root cause:**
The OR condition was designed as a fallback for the "already exists" case but it accepted ANY result on `pim/addEmployee` — including a real save failure. The auto-generated Employee ID `0428` conflicted with an existing demo user, but the test treated the failure as success.

**Mechanistic chain:**
```
auto-generated ID "0428" conflicts with demo data
→ OrangeHRM shows "Employee Id already exists" validation error
→ page stays at pim/addEmployee
→ OR condition cy.url().should('include', 'addEmployee') matches
→ clickSave() reports success
→ employee was NOT created
→ qauser_001 login fails for all downstream tests
→ 7 tests fail with "Invalid credentials" (not the real error)
```

**Fix:** Removed the OR condition. Rewrote `clickSave()` to assert `/empNumber/` redirect strictly. Added `fillEmployeeId(NEW_EMP_ID)` before save to use an explicit, controlled ID from `.env`.

**Evidence:** Commit `6a379e1` — `fix(pre-001): resolve silent failures from Employee ID conflicts`

---

### Failure Case 2 — Vue timing race (described in P7 above)

**Input:**
- `wait_for_load_state("networkidle")` + `locator('.oxd-input-field-error-message').all_text_contents()`
- Employee ID `0384` and username `qauser_001` already existed on demo

**Wrong output:**
- `all_text_contents()` returned `[]`
- AssertionError: `Employee save failed unexpectedly. URL: …/pim/addEmployee. Errors: []`

**Root cause:**
`networkidle` fires when no more network requests are in-flight. Vue's reactive DOM update (rendering validation error messages) is a synchronous JavaScript operation — it occurs AFTER the XHR response but before the browser emits the next idle event. The ~300–500ms gap between networkidle and DOM render was enough for the `all_text_contents()` read to miss the messages.

**Mechanistic chain:**
```
Save button clicked
→ XHR POST to OrangeHRM API (fails: ID/username conflict)
→ XHR response received → networkidle fires
→ [~400ms] Vue reactive system processes response → renders error messages
→ wait_for_load_state resolves at networkidle (BEFORE Vue renders)
→ all_text_contents() reads DOM → no error elements yet → returns []
→ neither success nor "already exists" branch matches
→ AssertionError with empty Errors list
```

**Fix:** `wait_for_function()` polling until either condition is true. Commit `fe083bc`.

---

### Failure Case 3 — Import path shadowing (Phase 2 initial generation)

**Input:** Generated step file used `from playwright.pages.login_page import LoginPage`

**Wrong output:** `ModuleNotFoundError: No module named 'playwright.pages'`

**Root cause:**
The `playwright/pytest.ini` sets `pythonpath = playwright`, meaning Python resolves `from pages.login_page` correctly. However, `playwright` is also the name of the installed Playwright library (`import playwright`). When the agent generated `from playwright.pages...`, Python resolved `playwright` as the installed package (not the project directory), found no `pages` submodule there, and raised ModuleNotFoundError.

**Mechanistic chain:**
```
agent writes: from playwright.pages.login_page import LoginPage
Python sees: import playwright → resolves to installed playwright package
playwright package has no .pages.login_page module
→ ModuleNotFoundError
correct form: from pages.login_page import LoginPage
(pytest.ini pythonpath = playwright makes 'playwright/' the root)
```

**Fix:** Added explicit constraint in `.claude/agents/playwright-migration.md`: `"Imports must use from pages.X import Y (not from playwright.pages.X import Y)"`. This is now in the agent definition and prompts.
