# Migration Workflow: Cypress to Playwright

## 1. Overview

This project follows a two-phase approach to QA automation migration.

**Phase 1** establishes a Cypress test suite written in TypeScript, driven by an AI agent that
navigates the target application through MCP Playwright, generates test code, and records results.

**Phase 2** migrates that suite to a Playwright Python framework using:
- **pytest-bdd** for BDD orchestration
- **Gherkin** `.feature` files for human-readable scenario definition
- **Page Object Model (POM)** mirroring the structure built in Phase 1
- **python-dotenv** for credential and environment variable management

The same agent-driven workflow is used in both phases: explore first via MCP Playwright,
then generate code only after the flow is validated to work.

---

## 2. Phase 1: Cypress Framework

### What was built

A Cypress TypeScript framework with at least three functional test scenarios, each corresponding
to a requirement defined in `requirements/functional_requirements.md`.

### Agent workflow

1. Agent reads the target requirement.
2. Agent opens Chrome via MCP Playwright and executes the test flow manually.
3. Agent records selectors, URLs, and expected values.
4. If execution succeeds, agent generates:
   - A Page Object in `cypress/pages/` extending `BasePage`.
   - A spec file in `cypress/e2e/`.
5. Results are written to `reports/cypress/`.

### Directory structure

```
cypress/
  e2e/              # Spec files (<req-xxx>_<short_name>.cy.ts)
  pages/            # Page Object classes (<PageName>Page.ts)
  support/          # commands.ts, e2e.ts, index.d.ts
  fixtures/         # Static test data (JSON)
cypress.config.ts
```

---

## 3. Phase 2: Playwright Migration

### What was migrated

Each Cypress spec and its associated Page Object was converted to an equivalent Playwright
Python suite following BDD conventions. The functional coverage and assertion logic are
preserved; only the language, syntax, and toolchain change.

### Agent workflow

1. Agent reads the existing Cypress spec and Page Object.
2. Agent re-executes the flow via MCP Playwright to confirm it still works.
3. If execution succeeds, agent generates:
   - A Gherkin `.feature` file.
   - A Python Page Object extending `BasePage`.
   - pytest-bdd step definitions.
4. Results are written to `reports/playwright/`.

---

## 4. Conversion Patterns

| Cypress (TypeScript) | Playwright Python |
|---|---|
| `cy.visit(url)` | `page.goto(url)` |
| `cy.get(selector)` | `page.locator(selector)` |
| `cy.contains(text)` | `page.locator(f'text={text}')` |
| `.should('have.value', x)` | `assert locator.input_value() == x` |
| `.should('contain.text', x)` | `assert x in locator.text_content()` |
| `.should('be.visible')` | `locator.is_visible()` |
| `beforeEach` hook | pytest fixture or Gherkin `Background` step |
| `Cypress.env('KEY')` | `os.environ.get('KEY')` / `python-dotenv` |
| `cy.url().should('include', x)` | `assert x in page.url` |
| Page Object extending `BasePage` | Python class extending `BasePage` |
| `describe` / `it` blocks | `Feature` / `Scenario` in Gherkin + pytest-bdd decorators |

---

## 5. Project Structure

```
Migration_cypress_to_Playwright/
|
|-- requirements/
|   └── functional_requirements.md
|
|-- cypress/                          # Phase 1
|   |-- e2e/
|   |-- pages/
|   |-- support/
|   └── fixtures/
|
|-- playwright/                       # Phase 2
|   |-- features/                     # Gherkin .feature files
|   |-- pages/                        # Python Page Objects
|   |   └── base_page.py
|   |-- tests/
|   |   └── step_defs/                # pytest-bdd step definitions
|   └── conftest.py                   # pytest fixtures (browser setup)
|
|-- reports/
|   |-- cypress/
|   └── playwright/
|
|-- .claude/
|   |-- skills/
|   |   └── cypress-test-gen.md       # Phase 1 skill (invoked with /cypress-test-gen)
|   └── agents/
|       └── playwright-migration.md   # Phase 2 agent
|
|-- docs/
|   |-- problem_statement.md
|   |-- data_provenance.md
|   |-- ai_review.md
|   |-- failure_analysis.md
|   |-- stakeholder_slide.md
|   └── declared_effort.md
|
|-- .env                              # Not committed; credentials and BASE_URL
|-- cypress.config.ts
|-- migration_workflow.md
└── CLAUDE.md
```

---

## 6. Running the Tests

### Cypress (Phase 1)

```bash
npm run cy:open                                               # Interactive Test Runner
npm run cy:run                                                # Headless, all specs
npm run cy:run:headed                                         # Headed, all specs
npm run cy:run:spec -- --spec "cypress/e2e/login.cy.ts"       # Single spec
```

### Playwright Python (Phase 2)

```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
pytest playwright/tests/

# Run a specific step definition module
pytest playwright/tests/step_defs/req_001_steps.py

# Run with verbose output and HTML report
pytest playwright/tests/ -v --html=reports/playwright/report.html
```

---

## 7. Key Decisions

### Why pytest-bdd

pytest-bdd integrates BDD Gherkin scenarios directly into the standard pytest runner. This
avoids introducing a separate Behave runtime, keeps CI configuration simple, and allows
existing pytest plugins (coverage, HTML reports, parallel execution) to work without
modification.

### Why POM was preserved

The Page Object Model was established in Phase 1 to isolate selector logic from test logic.
Carrying the same pattern into Phase 2 minimises cognitive overhead during migration: each
Cypress Page Object maps 1-to-1 to a Python Page Object, and reviewers familiar with the
Cypress suite can follow the Playwright code immediately.

### How credentials are handled

Both frameworks read credentials and the base URL from a `.env` file that is never committed
to version control. In Cypress, values are exposed through `Cypress.env()` via
`cypress.config.ts`. In Playwright Python, `python-dotenv` loads the same `.env` file at
test startup, and values are accessed with `os.environ.get()`. This ensures a single source
of truth for environment configuration across both frameworks.
