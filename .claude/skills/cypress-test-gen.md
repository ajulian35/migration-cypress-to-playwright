---
name: cypress-test-gen
description: Generate a Cypress TypeScript test for a single functional requirement. Explores the live app with MCP Playwright to map selectors, then creates the Page Object and spec file.
triggers:
  - "generate cypress test"
  - "cypress test gen"
  - "/cypress-test-gen"
---

# Skill — Cypress Test Generation

## Objective
Execute the test case defined in the functional requirements using MCP Playwright in Chrome,
and once the execution is validated as successful, generate the test automation code in Cypress
with TypeScript.

## How to invoke
Run `/cypress-test-gen` and specify the requirement ID, for example:
```
/cypress-test-gen REQ-002
```

---

## Instructions

### Step 1 — Exploratory execution with MCP Playwright

1. Open Chrome via MCP Playwright.
2. Navigate to the `BASE_URL` defined in `.env`.
3. Manually execute each step of requirement **{req-xxx}** as described in
   `requirements/functional_requirements_Cypress.md`.
4. Record:
   - CSS / XPath selectors for each element interacted with.
   - URLs of each page visited.
   - Texts and values that must be verified.
5. Confirm that the result matches the **Expected Result** of the requirement.

### Step 2 — Cypress TypeScript code generation

Only if Step 1 execution was successful:

1. Create (or update) the Page Object in `cypress/pages/<PageName>Page.ts` extending `BasePage`.
   - One method per meaningful action (e.g. `fillUsername`, `clickLogin`, `getErrorMessage`).
   - All selectors as private class constants.
2. Create the spec file in `cypress/e2e/<req-xxx>_<short-name>.cy.ts`.
   - `describe` block labelled with the requirement ID and name.
   - One `it` block per scenario / assertion group.
   - Credentials and base URL read exclusively via `Cypress.env()` (mapped from `.env`).
3. Verify the files compile without TypeScript errors.

---

## Requirement to execute

> Replace `{req-xxx}` with the ID of the requirement to work on, for example: `REQ-001`.

**Active requirement:** {req-xxx}

**Reference:** `requirements/functional_requirements_Cypress.md`

---

## Constraints

- Never hardcode credentials or URLs in the code; always use `Cypress.env()`.
- Follow the Page Object Model (POM) pattern: element selection logic goes in `cypress/pages/`,
  assertions go in `cypress/e2e/`.
- Name files in `kebab-case` format.
- Do not generate code for a requirement if the MCP Playwright exploratory execution failed.

---

## Expected output

| Artifact    | Path                                       |
|-------------|--------------------------------------------|
| Page Object | `cypress/pages/<PageName>Page.ts`          |
| Spec file   | `cypress/e2e/<req-xxx>_<short-name>.cy.ts` |

## Reference files
- Requirements: `requirements/functional_requirements_Cypress.md`
- Base class: `cypress/pages/BasePage.ts`
- Existing examples: `cypress/pages/LoginPage.ts`, `cypress/e2e/req-003_user-login.cy.ts`
- Config: `cypress.config.ts`, `.env`
