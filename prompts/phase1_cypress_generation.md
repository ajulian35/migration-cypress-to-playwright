# Phase 1 Prompt — Cypress TypeScript Test Generation

**Phase:** 1 — Generate Cypress TypeScript test suite  
**Input:** `requirements/functional_requirements_Cypress.md`  
**Output:** `cypress/e2e/*.cy.ts`, `cypress/pages/*.ts`

---

## Agent Prompt

> You are generating a Cypress TypeScript end-to-end test suite for OrangeHRM.
>
> **Source of truth:** `requirements/functional_requirements_Cypress.md` — read it first and treat every requirement as one spec file.
>
> **For each requirement, in order:**
>
> 1. Open Chrome via MCP Playwright and navigate to `BASE_URL` from `.env`.
> 2. Reproduce the steps in the requirement manually to verify the flow and confirm selectors against the live DOM.
> 3. Write a Cypress Page Object under `cypress/pages/` following the existing `LoginPage.ts` pattern:
>    - All selectors as class-level constants.
>    - One method per meaningful action.
>    - No assertions inside Page Objects.
> 4. Write the Cypress spec under `cypress/e2e/` using the naming convention `<req-id>_<short-name>.cy.ts`:
>    - Import the Page Object.
>    - Use `Cypress.env()` for all credentials and test data — never hardcode.
>    - One `describe` block per requirement, one `it` per test case.
> 5. Confirm the test passes with `npm run cy:run:spec -- --spec "cypress/e2e/<spec-file>"`.
>
> **Constraints:**
> - Use TypeScript throughout.
> - POM pattern: interaction logic in `cypress/pages/`, assertions in `cypress/e2e/`.
> - All selectors must be verified against the live DOM before being written into code.
> - Do not generate code for a requirement if live validation failed.
> - Use `.env` for all credentials. Reference via `Cypress.env('KEY')`.

---

## Invocation record

This prompt was used during the Phase 1 generation session. The agent executed MCP Playwright navigation for each of the 8 requirements (pre-001, pre-002, REQ-001 through REQ-007), confirmed selectors against the live OrangeHRM demo, and generated all Cypress artifacts in a single session.

**Known adjustments made during generation:**
- REQ-001 assertion values were updated from the spec to observed live values (data drift on shared demo).
- Employee ID conflict during pre-001 required explicit `NEW_EMP_ID` injection to avoid auto-generated ID collisions.
- A dynamic `empNumber` capture was added to `clickSave()` to support downstream tests that needed the employee's system-assigned ID.
