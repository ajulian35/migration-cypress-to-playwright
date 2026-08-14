# REFLECTION.md

**Repository:** https://github.com/ajulian35/migration-cypress-to-playwright (branch `L2`)

## What Was Built

This project demonstrates a two-phase, agent-driven workflow for migrating end-to-end test suites from Cypress (TypeScript) to Playwright (Python BDD).

**Phase 1** used Claude Code as a code-generation agent: given seven functional requirements for OrangeHRM, the agent navigated the live application via MCP Playwright, confirmed selectors against the real DOM, and generated a complete Cypress TypeScript suite with Page Object Model structure. The workflow was seeded by the README steps (Step 4), which defined the methodology: requirements → MCP exploration → TypeScript code → execution → results.

**Phase 2** used the same agent in a migration mode (the `playwright-migration` agent defined in `.claude/agents/playwright-migration.md`): for each requirement, the agent read the existing Cypress artifacts, re-validated the flow in the live browser, and produced three Playwright artifacts — a Gherkin `.feature` file, a Python Page Object, and pytest-bdd step definitions. This mapped to README Step 6: Gherkin → Python → POM → execution → results.

Both phases produced runnable, passing test suites: **Cypress 8/8** (mochawesome reports in `reports/cypress/`) and **Playwright 8/8** (pytest-html report in `reports/playwright/`).

## Why This Approach

The alternative — a deterministic transpiler like `cypress-to-playwright-codemod` — cannot verify that copied selectors resolve correctly in the live application. The shared OrangeHRM demo changes continuously: Employee IDs conflict, claim records are modified, and page structure evolves. An agent with live browser access can detect these discrepancies and choose a different selector strategy before writing broken code. A script cannot.

The CLAUDE.md file served as the persistent convention layer (the agent's "procedural memory"), carrying import path rules, file naming conventions, and POM structure across sessions without requiring re-exploration of the codebase each time.

## What Failed

**Three concrete failures occurred, all documented mechanistically in `docs/agent_evaluation.md`:**

**1. Employee ID collision — silent failure masking (most damaging)**

The original `clickSave()` in the Cypress Page Object used an OR condition: it accepted `/pim/addEmployee` as a valid outcome alongside the success redirect. When OrangeHRM's auto-generated Employee ID `0428` conflicted with an existing demo user, the page stayed on `addEmployee` — and the OR condition silently accepted this as success. The employee was never created. All 7 downstream tests failed with "Invalid credentials" errors, not the real "Employee ID conflict" error. The failure was invisible at the point it occurred and only surfaced two test files later.

**2. Vue timing race — tool output trusted incorrectly**

After fixing the ID conflict by injecting an explicit `NEW_EMP_ID` from `.env`, the Playwright equivalent of `click_save()` still failed. The sequence: click Save → `wait_for_load_state("networkidle")` → `all_text_contents('.oxd-input-field-error-message')` → `[]`. The test concluded there were no errors and raised `AssertionError: Employee save failed unexpectedly. Errors: []`. But `MCP Playwright browser_evaluate` querying the same DOM moments later returned two error elements. Root cause: `networkidle` fires when no network requests are in-flight; Vue's reactive render cycle (which inserts the error messages into the DOM) runs synchronously after the XHR response and completes ~300–500ms after networkidle. The Playwright call read the DOM in that gap.

**3. Import path shadowing (early generation)**

Generated step files used `from playwright.pages.login_page import LoginPage`. Python resolved `playwright` as the installed Playwright package (not the project directory), because `pytest.ini` sets `pythonpath = playwright` but does not rename the directory. The agent fixed this once and added the constraint to `.claude/agents/playwright-migration.md` so it would not recur.

## How Each Was Fixed

1. **ID collision:** Removed the OR condition from `clickSave()`. Added `fillEmployeeId(NEW_EMP_ID)` to inject a controlled ID before saving. Added strict URL assertion on `/empNumber/` redirect. Added `cy.task('setRuntimeValue')` to capture the dynamic `empNumber` for downstream tests.

2. **Vue timing race:** Replaced `wait_for_load_state("networkidle")` with `wait_for_function()` that polls until either the success redirect URL appears or the first `.oxd-input-field-error-message` element is present — whichever comes first. The diagnosis relied on MCP Playwright `browser_evaluate` querying the DOM directly after clicking Save, which confirmed the errors existed but had not yet been read by the test code.

3. **Import shadowing:** Added explicit constraint to the agent definition: `from pages.X import Y` (not `from playwright.pages.X`). Added to prompts and agent markdown file.

## What I Would Do Differently

**Use a containerized OrangeHRM instance.** The shared public demo is the project's largest technical debt. Concurrent users modify records, Employee IDs conflict unpredictably, and the demo resets daily at an uncertain time. Approximately 40% of debugging time in this project was spent on failures caused by the shared demo rather than by actual agent or code errors. A Docker-compose OrangeHRM instance would eliminate this entirely and make the test suite reproducible.

**Commit earlier and more granularly.** The L1 submission had no git history separating spec from implementation. The L2 branch addressed this retroactively — the first four commits follow spec → plan → implementation → docs — but a clean history from day one would be better evidence of the methodology.

**Version the selector decisions.** Each time the agent chose a selector strategy, that decision was embedded in the generated code but not recorded elsewhere. A short SELECTORS.md documenting which selectors were tried, rejected, and why would make the agent's work auditable without reading every generated file.

## Business Impact

A Cypress-to-Playwright migration for a 7-requirement suite took approximately **3.5 hours of total agent-session time** across both phases, including live DOM validation for each requirement, full code generation, and bug resolution. A skilled QA engineer doing this manually — re-verifying selectors, rewriting Page Objects from TypeScript to Python, authoring Gherkin from scratch, and debugging import errors — would conservatively spend **2–3 days** on the same scope.

The workflow is portable. The agent definition (`.claude/agents/playwright-migration.md`), the CLAUDE.md convention layer, the prompts, and the project structure are all version-controlled and reusable. A new engagement starts from a working baseline rather than a blank project — the next migration compresses further because the framework is already in place.

The failure analysis in this document is the most transferable artifact: knowing that Vue reactive timing, OR-condition masking, and import namespace collisions are the three failure modes to anticipate makes the next agent-assisted migration measurably more reliable from the first run.
