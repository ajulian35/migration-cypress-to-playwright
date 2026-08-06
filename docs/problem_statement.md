# Problem Statement

## Domain

Enterprise HR software projects routinely include end-to-end test suites built in Cypress (TypeScript). As teams mature their QA practices — or as client engagements hand off to new vendors — those suites must be migrated to Playwright (Python) to align with updated tooling standards, cross-language team composition, or BDD/Gherkin reporting requirements.

## The User

A QA engineer or consultant assigned to migrate an existing Cypress TypeScript test suite to Playwright Python on a client project. They understand both frameworks but face a time-boxed engagement with limited capacity for repetitive, low-value work.

## The Problem

Cypress-to-Playwright migrations are manual, repetitive, and error-prone by default. Every test file requires:

- **Selector re-verification** — Cypress and Playwright query the DOM differently; selectors must be re-confirmed against the live application rather than copied verbatim.
- **Page Object rewrite** — TypeScript classes become Python classes. Method signatures, typing conventions, and import paths all change.
- **BDD layer added from scratch** — Gherkin `.feature` files, step definition bindings, and fixture setup do not exist in the Cypress suite and must be authored from zero.
- **Test logic translation** — Cypress's chainable command API does not map one-to-one to Playwright's async/await model.

Doing this manually for a suite of 7+ requirements across multiple modules takes multiple days of skilled engineering time. On a client engagement, that is budget spent on mechanical translation rather than on new test coverage or exploratory validation.

## Definition of Success

A reproducible, agent-driven workflow that:

1. Explores the live application using MCP Playwright to capture real, verified selectors — no guessing, no stale locators.
2. Generates working Cypress TypeScript test code directly from a structured requirements document.
3. Migrates that code to Playwright Python BDD with zero manual selector re-mapping — the same selectors, confirmed once, flow into both frameworks.
4. Produces runnable, passing test suites for both frameworks from a single source of requirements.

## Why This Is Worth Solving

For a client stakeholder, the value is threefold:

- **Faster time-to-quality.** A migration that takes days manually is compressed into a guided agent session. Test coverage is active sooner.
- **Reduced migration cost.** Engineering hours shift from mechanical rewriting to reviewing and validating generated output — a higher-value use of skilled time.
- **Reusable workflow.** The agent prompts, project structure, and conventions documented here are portable. The next migration starts from a known, working baseline rather than a blank page.

Any team member who can follow the documented prompts and project structure can execute this workflow — it does not depend on a single expert's institutional knowledge.
