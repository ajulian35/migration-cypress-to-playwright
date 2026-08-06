# Failure Analysis

**Project:** OrangeHRM QA Automation — Cypress to Playwright Migration  
**Framework under analysis:** Playwright Python (Phase 2)  
**Date:** 2026-08-05

This document records every known failure scenario for the prototype test suite. Each entry states the triggering condition, the exact wrong output or error, the root cause, and its resolution status.

---

## 1. REQ-001 — Shared mutable state breaks field assertions

**Specific input or condition:**  
A second user modifies the `mandaa user` employee record on the shared OrangeHRM demo instance (e.g., changes nationality, marital status, or date of birth) at any point after the test suite was last calibrated.

**Exact wrong output or error:**  
The `@then` steps in `playwright/tests/step_defs/req_001_steps.py` call `assert my_info.get_nationality() == "American"` (and equivalent for marital status and date of birth). If the field value has changed, pytest reports:

```
AssertionError: assert "Indian" in "Indian"
# or, depending on the new value:
AssertionError
```

The scenario fails with no indication that the cause is external data mutation rather than a code defect.

**Root cause:**  
The test suite asserts against specific field values on a shared, publicly editable demo instance. The demo has no data isolation between concurrent users. The test owns no fixture setup or teardown that resets the employee record to a known state before running assertions.

**Status:** Known limitation — not fixed. The prototype does not implement pre-test data seeding or cleanup against the shared demo. Fixing this would require either using a private OrangeHRM instance with controlled seed data, or adding an API-level setup step that resets the record before each scenario run.

---

## 2. REQ-005 — Add Employee accumulates test data on repeated runs

**Specific input or condition:**  
`playwright/tests/step_defs/req_005_steps.py` is executed more than once (e.g., in a CI loop, during local development re-runs, or in a parallel test run).

**Exact wrong output or error:**  
Each run creates a real employee record on the shared demo with a timestamped name (`Test<epoch>` / `Playwright<epoch>`). The records are never cleaned up. Over time:

- The Employee List grows with orphaned test records.
- If the demo instance imposes a maximum employee count, a future run may fail with an application-level error rather than a test assertion failure, producing an ambiguous result.
- REQ-006 (search by name) may incidentally match orphaned records, making its "at least one row" assertion pass for the wrong employee.

**Root cause:**  
The test has no teardown step. The add-employee flow is a write operation with a visible side effect on shared state. Timestamped names prevent name collisions between runs but do not prevent accumulation.

**Status:** Known limitation — not fixed. A proper fixture with `yield` + cleanup (deleting the created employee via the UI or API after the scenario) would address this. Left out of scope for the prototype.

---

## 3. REQ-002 — Custom OXD dropdown breaks if rendering changes

**Specific input or condition:**  
The Event Name filter on the Employee Claims page uses a custom OrangeHRM OXD dropdown component, not a native HTML `<select>`. The step `filter_event_name` in `playwright/tests/step_defs/req_002_steps.py` exercises `ClaimPage.select_event_name`, which does:

```python
def select_event_name(self, name: str):
    self.page.click(self.EVENT_NAME_DROPDOWN)
    self.page.locator(f'role=option[name="{name}"]').click()
```

If the OrangeHRM front-end is updated and the dropdown options are no longer rendered with `role="option"`, or if the dropdown trigger selector (`.oxd-select-text`) changes, the click sequence fails.

**Exact wrong output or error:**  
```
playwright._impl._errors.TimeoutError: Locator.click: Timeout 30000ms exceeded.
```
or
```
playwright._impl._errors.Error: strict mode violation: locator('role=option[name="Medical Reimbursement"]') resolved to N elements
```

**Root cause:**  
The OXD component is a custom Vue widget. Its DOM structure is not governed by the HTML spec and can change with any front-end dependency update. The `role=option` ARIA role is applied by the component, not the browser, and is therefore less stable than a native `<select>` locator.

**Status:** Known limitation — not fixed. The locator strategy was chosen because it is the most readable option available for this component. A fallback strategy using `.oxd-select-option:has-text("Medical Reimbursement")` would be slightly more resilient to ARIA attribute changes but equally brittle to class name changes. True stability requires either a data-testid attribute on the component (a change to the OrangeHRM source) or an API-level filter bypass.

---

## 4. REQ-006 — Autocomplete timeout causes silent wrong-scope search

**Specific input or condition:**  
The employee name search field uses a typeahead autocomplete. `EmployeeListPage.search_by_name` in `playwright/pages/employee_list_page.py` (line 16) waits exactly 800 ms for the suggestion to appear:

```python
self.page.fill(self.NAME_INPUT, name)
self.page.wait_for_timeout(800)
suggestion = self.page.locator('.oxd-autocomplete-dropdown .oxd-autocomplete-option').first
if suggestion.is_visible():
    suggestion.click()
```

On a slow network or a loaded demo server, the autocomplete response takes longer than 800 ms.

**Exact wrong output or error:**  
`suggestion.is_visible()` returns `False`. The `if` branch is skipped. No name filter is applied to the search form. The subsequent `click_search()` call returns all employees in the system. The assertion in `req_006_steps.py` (line 22–25) is:

```python
assert emp_list.get_result_rows().count() > 0
```

This assertion passes because the unfiltered list is non-empty — but the test has silently validated the wrong thing. The name-match assertion at lines 27–36 checks `row.text_content()` for the searched name; if the target employee is in the full list, that assertion also passes falsely.

**Root cause:**  
`page.wait_for_timeout` is a fixed sleep, not a condition wait. The 800 ms value was calibrated against the network conditions present during agent exploration. It does not adapt to variable latency.

**Status:** Known limitation — not fixed in the prototype. The correct fix is to replace the fixed sleep with a condition-based wait:

```python
self.page.wait_for_selector(
    '.oxd-autocomplete-dropdown .oxd-autocomplete-option',
    state='visible',
    timeout=5000
)
```

This would raise a clear `TimeoutError` on slow networks instead of silently degrading test scope.

---

## 5. REQ-007 — Logout step breaks if logged-in username changes

**Specific input or condition:**  
The test runs against an OrangeHRM instance where the logged-in user's display name is not `"mandaa user"`. This includes: a different demo account, a private OrangeHRM instance, or the demo being reset by the administrator.

**Exact wrong output or error:**  
`playwright/tests/step_defs/req_007_steps.py`, line 8:

```python
page.locator("span").filter(has_text="mandaa user").click()
```

When the display name does not match, Playwright finds zero elements matching the locator and raises:

```
playwright._impl._errors.TimeoutError: Locator.click: Timeout 30000ms exceeded.
waiting for locator("span").filter(has_text="mandaa user")
```

The scenario fails at the first `@when` step, before any logout action is attempted.

**Root cause:**  
The username is hardcoded as a string literal. It was taken from the MCP Playwright exploration session and embedded directly into the step definition without parameterization. There is no mechanism to supply the expected username through configuration or a fixture.

**Status:** Known limitation — not fixed in the prototype. The recommended fix is to either read the expected username from the `.env` file via a fixture, or use a selector that does not depend on the username text at all (for example, `.oxd-userdropdown-tab`).

---

## Limitations outside the prototype's scope

This prototype was designed, generated, and validated exclusively against the public OrangeHRM demo at `https://opensource-demo.orangehrmlive.com`. The following limitations apply to any attempt to run the suite against a different environment:

- **Private OrangeHRM instances:** Employee records, claim records, and user account names differ. Every data-dependent assertion (REQ-001, REQ-002, REQ-006) will fail without recalibration.
- **Different OrangeHRM versions:** The OXD component library and URL routing patterns differ between OrangeHRM Community Edition versions. Selectors referencing `.oxd-*` class names or specific URL paths (e.g., `/web/index.php/pim/viewEmployeeList`) may not be stable across versions.
- **Non-admin accounts:** REQ-005 (Add Employee) requires admin privileges. The prototype assumes the credentials in `.env` belong to an admin account, as is the case on the public demo. A standard user account will be denied access and the test will fail at navigation.
- **Shared demo instability:** The public demo is reset periodically by OrangeHRM. After a reset, all reference ids (REQ-002: `202307180000002`), employee records (REQ-001, REQ-006), and accumulated test data (REQ-005) are wiped. The suite must be re-explored and recalibrated after each reset.

The prototype is not intended as a production-grade regression suite. It demonstrates the migration workflow and agent-driven generation process. Hardening the suite for production use would require data isolation, parameterized credentials, and a controlled test environment.
