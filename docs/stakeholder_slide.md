# AI-Driven QA Migration: Cypress → Playwright

---

## The Problem

- Manual test migration requires re-mapping every selector by hand — fragile and time-consuming
- Translating Cypress TypeScript to Playwright Python means rewriting POM classes, step definitions, and Gherkin scenarios from scratch
- Every migrated test must be re-validated against the live app to confirm selectors still resolve

---

## The Solution

- An AI agent (Claude Code + MCP Playwright) explores the live OrangeHRM demo app and captures real, working selectors
- From a single requirements document the agent generates both a Cypress TypeScript suite and a Playwright Python BDD suite
- Page Object Models in both frameworks are produced automatically from live app observation
- The entire workflow is prompt-driven and repeatable for any future migration target

---

## What Was Delivered

- 7 Cypress TypeScript spec files (E2E tests)
- 7 Playwright Python BDD test files with pytest-bdd
- 7 Gherkin `.feature` scenario files
- Page Object Model layer in both frameworks (6 Cypress POMs, 7 Playwright POMs)
- HTML test execution reports for both frameworks
- Migration workflow document and versioned agent prompts

---

## The Gain

- An estimated 2–3 days of manual migration work was completed in a single agent session
- The workflow is fully reusable: point it at a new requirements doc and target app, and it repeats

---

## One Thing It Does Not Handle

- Assertions tied to shared demo data: values drift when other users modify records in the live OrangeHRM environment, so hard-coded expected values in tests can silently become stale
