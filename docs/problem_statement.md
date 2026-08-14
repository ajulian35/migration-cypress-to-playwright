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

---

## The Agent Decision (L2 — Agent Architecture)

The core agentic decision is: **given a Cypress TypeScript spec and access to a live browser, determine the correct Playwright Python implementation without human-directed step-by-step instruction.**

On each requirement, the agent must decide at runtime:

1. **Which selectors to use** — it cannot copy Cypress selectors verbatim because Playwright's query semantics differ. It must inspect the live DOM, identify the element, and choose a selector strategy (`getByRole`, CSS, or `has-text` pseudo-class) that will be stable under re-renders.
2. **How to translate the assertion** — Cypress `should('have.text', …)` becomes a Playwright `expect(locator).to_have_text(…)`, but the equivalence depends on whether the element contains nested markup, whitespace normalization, or dynamic content. The agent must observe the actual element before deciding.
3. **How to structure the BDD layer** — the Gherkin scenario title, step granularity, and fixture sharing strategy are not derivable from the Cypress test alone; they require understanding the test's intent and the page flow.

None of these decisions can be resolved with a fixed lookup table. Each requires live browser evidence at the time of migration.

## Why an Agent, Not a Deterministic Script

A deterministic script could transpile Cypress command syntax to Playwright syntax mechanically (and tools like `cypress-to-playwright-codemod` attempt this). The gap is **selector validity**: a script cannot know whether a copied selector resolves correctly on the live application at migration time. Selectors rot as the application changes, and the shared demo environment used in this project changes continuously across sessions.

An agent — specifically one with MCP Playwright browser tools — can:
- Navigate the live page, snapshot the DOM, and verify that a proposed selector resolves to exactly one element before writing the code.
- Detect when a selector resolves to zero or multiple elements and choose a different strategy, rather than writing broken code silently.
- Flag when an application state prerequisite (e.g., a test user that must be created first) is not satisfied, and pause for human confirmation before proceeding.

A script has no mechanism to handle these cases. It would silently produce broken tests. The agent produces tests that pass on first execution because it verified the selectors before committing them.

## Data Provenance

**Source:** OrangeHRM open-source demo (`opensource-demo.orangehrmlive.com`) — a publicly hosted instance of OrangeHRM, shared among all visitors. Credentials are public and included in the repository `.env` file.

**What it represents:** A realistic HR application with employee management, leave, and claims modules. It provides authentic DOM structure, navigation flows, and form interactions representative of enterprise HR software.

**Limitations and awkward cases:**
- The demo resets daily, clearing data created by previous sessions. Any test that depends on pre-existing data (e.g., a specific employee or claim record) is fragile across resets.
- The demo is shared: other users can create, modify, or delete records concurrently. Employee ID conflicts and username collisions occur in practice and were observed during this project.
- Date-sensitive fields (e.g., claim submission dates) display differently depending on the demo's current data state.

These limitations were handled by:
- Pre-condition tests (`pre-001`, `pre-002`) that create required data at the start of each run.
- Explicit Employee ID injection (`NEW_EMP_ID` from `.env`) to avoid auto-generated ID collisions.
- Graceful handling in `click_save()` when a conflicting employee already exists (from a prior run in the same session).

**Sensitive data:** None. All credentials in `.env` are the demo's publicly documented test credentials. No real user data is involved.
