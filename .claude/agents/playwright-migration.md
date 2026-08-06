---
name: playwright-migration
description: Migrates a single Cypress TypeScript test to a Playwright Python BDD suite. Reads the existing Cypress artifacts, validates the flow with MCP Playwright, then generates the Gherkin feature file, Python Page Object, and pytest-bdd step definitions.
---

# Agent — Playwright Python Migration

## Purpose
Given a requirement ID, this agent reads the existing Cypress spec and Page Object,
re-validates the flow with MCP Playwright, and produces the three Playwright/Python
artifacts for the Playwright BDD framework under `playwright/`.

## Inputs expected
- Requirement ID (e.g. `REQ-001`)
- The Cypress spec: `cypress/e2e/<req-xxx>_<short-name>.cy.ts`
- The Cypress Page Object(s): `cypress/pages/<PageName>Page.ts`

## Workflow

### Step 1 — Read the Cypress artifacts
1. Read the Cypress spec file for the target requirement.
2. Read all Page Objects imported by that spec.
3. Extract:
   - Selectors (CSS / XPath).
   - Actions (clicks, fills, navigations).
   - Assertions (text, value, URL checks).
   - Environment variable references.

### Step 2 — Validate the flow with MCP Playwright
1. Open Chrome via MCP Playwright.
2. Navigate to `BASE_URL` from `.env`.
3. Execute each step extracted in Step 1 for the target requirement.
4. Record any selector adjustments needed.
5. Confirm the result matches the **Expected Result** in
   `requirements/functional_requirements_Cypress.md`.

### Step 3 — Generate Playwright Python artifacts
Only if Step 2 succeeded:

1. **Feature file** → `playwright/features/<req_xxx_name>.feature`
   - One `Scenario` per test case / assertion group.
   - `Background` block for shared login precondition.
   - Business-readable `Given / When / Then` language.

2. **Page Object** → `playwright/pages/<name>_page.py`
   - Extend `BasePage` from `playwright/pages/base_page.py`.
   - One method per meaningful action.
   - All locators as class-level constants.
   - No assertions inside Page Objects.

3. **Step definitions** → `playwright/tests/step_defs/<req_xxx>_steps.py`
   - Call `scenarios("../../features/<req_xxx_name>.feature")` at the top.
   - Import the Page Object created above.
   - Map each Gherkin step with `@given`, `@when`, `@then`.
   - Use `from pages.<module> import <Class>` (not `from playwright.pages…`).
   - Read credentials via `os.environ.get()` backed by `python-dotenv`.
   - Shared steps (`logged_in`, `on_login_page`) stay in `common_steps.py` — do not duplicate.

4. Verify Python syntax is valid (correct indentation, no import errors).

## Requirement to migrate

> Replace `{req-xxx}` with the ID of the requirement to work on, for example: `REQ-001`.

**Active requirement:** {req-xxx}

**Reference:** `requirements/functional_requirements_Cypress.md`

---

## Constraints
- Never hardcode credentials or URLs — use `os.environ.get()` / `.env`.
- POM pattern: interaction logic in `playwright/pages/`, steps in `playwright/tests/step_defs/`.
- All file names in `snake_case`.
- Imports must use `from pages.X import Y` (not `from playwright.pages.X import Y`)
  because `pythonpath = playwright` is set in `playwright/pytest.ini`.
- Do not generate code if Step 2 validation failed.
- Each Gherkin scenario must be self-contained and independent.

## Expected output

| Artifact         | Path                                                        |
|------------------|-------------------------------------------------------------|
| Feature file     | `playwright/features/<req_xxx_name>.feature`                |
| Page Object      | `playwright/pages/<name>_page.py`                           |
| Step definitions | `playwright/tests/step_defs/<req_xxx>_steps.py`             |

## Reference files
- Requirements: `requirements/functional_requirements_Cypress.md`
- Base class: `playwright/pages/base_page.py`
- Shared steps: `playwright/tests/step_defs/common_steps.py`
- Existing example: `playwright/pages/login_page.py`, `playwright/tests/step_defs/req_003_steps.py`
- Config: `playwright/pytest.ini`, `playwright/conftest.py`, `.env`
