# Phase 2 Prompt — Playwright Python BDD Migration

**Phase:** 2 — Migrate Cypress TypeScript tests to Playwright Python BDD  
**Input:** `cypress/e2e/*.cy.ts`, `cypress/pages/*.ts`, live OrangeHRM DOM  
**Output:** `playwright/features/*.feature`, `playwright/pages/*_page.py`, `playwright/tests/step_defs/*_steps.py`

---

## Agent Prompt (per-requirement invocation)

> The `playwright-migration` agent handles one requirement per invocation.
> Full definition: `.claude/agents/playwright-migration.md`
>
> **Invocation pattern:**
> ```
> Migrate REQ-001 from Cypress to Playwright Python BDD.
> ```
>
> The agent reads the Cypress spec and Page Objects, validates selectors via MCP Playwright, presents a validation summary for human approval, and only then generates the three Playwright artifacts.

---

## Batch invocation prompt (used during Phase 2 generation)

> Migrate all 8 requirements to Playwright Python BDD in order:
> pre-001, pre-002, REQ-001, REQ-002, REQ-003, REQ-004, REQ-006, REQ-007.
>
> For each requirement:
> 1. Read the Cypress spec and Page Object.
> 2. Open MCP Playwright and validate the flow against the live app.
> 3. Confirm selectors before writing code.
> 4. Generate: Gherkin `.feature` file, Python Page Object (POM), pytest-bdd step definitions.
> 5. Run `python -m pytest tests/step_defs/<req>_steps.py -v` and fix any failures before moving on.
>
> Framework structure:
> - Features: `playwright/features/`
> - Pages: `playwright/pages/` (extend `BasePage`)
> - Steps: `playwright/tests/step_defs/`
> - Shared login steps: `playwright/tests/step_defs/common_steps.py` — do not duplicate
> - Config: `playwright/pytest.ini`, `playwright/conftest.py`, `.env`
>
> Import path rule: `from pages.X import Y` (not `from playwright.pages.X`) because
> `pythonpath = playwright` is set in `pytest.ini`.
>
> Credentials via `os.environ.get('KEY')` backed by `python-dotenv`.

---

## Invocation record

This prompt was used during the Phase 2 migration session. All 8 requirements were migrated in one session. The agent performed live DOM validation for each requirement before generating code.

**Known adjustments made during migration:**
- `fill_password()` in `AddEmployeePage` required a JavaScript `evaluate()` injection because Vue's reactivity layer ignored standard Playwright `fill()` on password inputs.
- `click_save()` required a `wait_for_function()` guard instead of `wait_for_load_state("networkidle")` because Vue renders inline error messages 300–500ms after network becomes idle.
- `pre_001_steps.py` captures `emp_number` from the redirect URL into `runtime_data` for use by downstream tests.
- Sequential Cypress + Playwright runs on the shared demo required graceful "already exists" handling in `click_save()`.
