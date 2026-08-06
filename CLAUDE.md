# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a two-phase QA automation migration project:

1. **Phase 1 — Cypress Framework (TypeScript):** Build a Cypress test suite from defined functional requirements using an AI agent that navigates the target app via MCP Playwright, generates TypeScript test code, executes it, and reports results.
2. **Phase 2 — Playwright Framework (Python):** Migrate the Cypress tests to a Playwright Python suite using Gherkin/Cucumber BDD syntax, Page Object Model (POM) structure, and the same agent-driven workflow.

The goal is to produce a documented, reproducible migration workflow from Cypress to Playwright.

## Project Phases

### Phase 1: Cypress (TypeScript)
- Set up framework structure under `cypress/`
- Define at least 3 functional requirements in a requirements document
- Agent workflow: requirements → test cases → MCP Playwright navigation → TypeScript Cypress scripts → execution → results report

### Phase 2: Playwright (Python)
- Set up framework structure under `playwright/` (Python)
- Agent workflow: requirements → Gherkin scenarios → Python Playwright scripts (POM) → execution → results report

### Prompt Discipline
Each phase has its own prompt(s). Create and version prompts per stage — store them in a `prompts/` directory.

## Cypress Commands

```bash
npm run cy:open              # open Cypress Test Runner (interactive)
npm run cy:run               # run all tests headless
npm run cy:run:headed        # run all tests headed
npm run cy:run:spec -- --spec "cypress/e2e/login.cy.ts"  # run a single spec
```

## Conventions

- **Sensitive data:** Use `.env` files; never commit secrets. Reference variables via `process.env` (TypeScript) or `os.environ` / `python-dotenv` (Python).
- **Cypress:** TypeScript, structured under `cypress/e2e/`, `cypress/pages/` (POM), `cypress/support/`
- **Playwright (Python):** POM pattern under `playwright/pages/`, tests under `playwright/tests/`, features under `playwright/features/` (Gherkin `.feature` files)
- **Reports:** Collect execution results and store under `reports/` per framework

## Expected Deliverables

- `requirements/` — functional requirements specification
- `cypress/` — Cypress TypeScript framework and generated test scripts
- `playwright/` — Playwright Python framework and migrated test scripts
- `reports/` — test execution results for both frameworks
- `prompts/` — agent prompts used at each stage
- Migration workflow document describing the Cypress → Playwright conversion approach
