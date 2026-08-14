# Submission Checklist — L2_Case05_Open_Choice_Agent

You chose this case, so you own the scope. Everything below is required
regardless of what you built.

## Repository

| Field | Value |
|-------|-------|
| **Platform** | GitHub |
| **URL** | https://github.com/ajulian35/migration-cypress-to-playwright |
| **Branch** | `L2` |
| **Visibility** | Public |
| **Key commits** | `c168a01` spec · `ed438f4` plan · `6a379e1` fix · `fe083bc` timing fix · `82865d2` pytest-asyncio + REFLECTION · `92fb95c` PPT |

## Define

- [x] Problem statement: the domain, the user, and the decision the agent takes on their behalf.
  > `docs/problem_statement.md` — Domain: QA Engineering / test-suite migration. User: developer/QA engineer. Decision: which selector strategy to use after live DOM inspection, before writing any code.

- [x] Justification that an agent is warranted — what makes this require runtime decision-making rather than a deterministic script.
  > `docs/problem_statement.md` § "Why an Agent, Not a Deterministic Script" — a codemod/transpiler cannot verify that copied selectors resolve in the live app; OrangeHRM changes continuously (shared users, daily resets, ID conflicts). The agent inspects the DOM and decides selector strategy at runtime; a script cannot.

- [x] Data provenance note: source or generation method, what it represents, whether it includes the awkward cases that expose agent failure, and how you handled anything sensitive.
  > `docs/problem_statement.md` § "Data Provenance" — OrangeHRM public demo (`opensource-demo.orangehrmlive.com`). Represents a shared, mutable HR system. Awkward cases included: Employee ID auto-increments conflict with existing users; demo resets daily at uncertain time. Sensitive data: `.env` tracks only public demo credentials (no real secrets). Handled via explicit `NEW_EMP_ID` injection and idempotent "already exists" check.

## Build

- [x] Working agent, demonstrable end to end, where the model decides what to do at runtime rather than following a hardcoded sequence.
  > Cypress 8/8 passing (`reports/cypress/mochawesome_086-093.html`) + Playwright 8/8 passing (`reports/playwright/report.html`). Agent defined in `.claude/agents/playwright-migration.md`.

- [x] At least two tools the agent invokes.
  > `docs/agent_architecture.md` — 3 tools: (1) MCP Playwright (`browser_navigate`, `browser_snapshot`, `browser_evaluate`), (2) file-system tools (Read, Write, Edit, Glob, Grep), (3) Bash/pytest for execution and output parsing.

- [x] A memory component, with a stated reason for the tier you chose.
  > `docs/agent_architecture.md` § "Memory" — short-term in-context (selector decisions, validation results within session) + CLAUDE.md as session-persistent procedural memory (import rules, file naming, POM structure). Long-term persistence not needed: each migration session is self-contained.

- [x] An explicit human validation gate before anything irreversible.
  > `.claude/agents/playwright-migration.md` Step 2.5 — agent presents a validation summary (confirmed selectors, adjustments made, unresolved mismatches) and waits for explicit user confirmation before writing any file.

- [x] Failure handling: output validated rather than trusted, the specific failure reason fed back on retry, and escalation with full context after repeated failure.
  > `docs/agent_evaluation.md` § "P7 Failure Handling Protocol" — snapshot count validated (must == 1); pytest output parsed for traceback; URL checked for redirect. On retry: original input + exact error + DOM excerpt included. After 2 consecutive failures: stop, surface full context, await human guidance.

## Prove

- [x] Evaluation against criteria you defined and defend, not by inspection.
  > `docs/agent_evaluation.md` — 5 criteria (C1–C5): selector resolves to exactly 1 element; generated code runs without manual edit; first-pass pass rate ≥ 70%; failure reason appears in retry prompt; escalation triggers after 2 failures. Each has a measurement method and recorded result.

- [x] The cases it gets wrong, with at least two explained mechanistically.
  > `docs/agent_evaluation.md` — 3 cases: (1) Employee ID collision: OR condition in `clickSave()` accepted `/pim/addEmployee` as success → silent failure → 7 downstream tests failed on "Invalid credentials". (2) Vue timing race: `wait_for_load_state("networkidle")` resolved before Vue rendered validation messages → `all_text_contents()` returned `[]` when 2 errors existed in DOM. (3) Import path shadowing: `from playwright.pages.X` resolved to installed package, not project directory.

- [x] A deliberate failure injection and the recovery or escalation it triggered.
  > `docs/agent_evaluation.md` § "Deliberate Failure Injection" + commit `fe083bc` — Vue timing race reproduced: `networkidle` fired, `all_text_contents()` returned `[]`, test raised `AssertionError: Employee save failed unexpectedly. Errors: []`. Recovery: `wait_for_function()` polling until `'.oxd-input-field-error-message' !== null`, confirmed via `browser_evaluate`. Also reproduced in `tests/agent/test_agent_loop.py::test_vue_timing_race_old_approach_misses_errors`.

- [x] `pytest-asyncio` suite covering the agent loop, tool mocking, and the recovery path, with passing output.
  > `tests/agent/test_agent_loop.py` — 8 tests, 8/8 passed in 0.06s. Covers: selector valid/zero/multiple, save success/already-exists/escalation, Vue timing race reproduction, `wait_for_function` call ordering verification.

- [x] Observability evidence: Portkey traces, LangSmith step traces, or equivalent.
  > `docs/stack_observability.md` — session transcript JSONL (`9bd4ca8f-5ffd-4a63-9b14-d293401c8be2.jsonl`) used as trace equivalent: 238 tool calls, timestamped, full input/output per call. Real trace excerpt included (the `browser_evaluate` call that diagnosed the Vue timing race). Python parsing snippet for extracting tool call sequences.

## Communicate

- [x] `REFLECTION.md`, 600-1000 words: what was built · why · what failed · how you fixed it · what you'd do differently · business impact. The failure sections carry the most weight.
  > `REFLECTION.md` — ~800 words. All sections present. Failure sections: Employee ID collision (most damaging — silent masking), Vue timing race (root cause via `browser_evaluate`), import shadowing. Business impact: 2–3 days manual → 3.5h agent session.

- [x] One slide pitching the solution to client stakeholders.
  > `docs/AI_Capstone_L2_Julian Largo.pptx` — slides 3–9 cover domain/problem/outcomes, AI approach, before/after, impact scorecard, reusability, what AI got right/wrong, and evidence artifacts.

- [ ] A demo showing both a normal run and a failure being handled.
  > **Descoped** — documented in `docs/declared_effort.md`. The session transcript JSONL (238 tool calls) and git commit history (`fe083bc` = Vue timing race fix) serve as equivalent evidence. A live screen-capture was not recorded due to time constraints.

- [x] Declared-effort statement: approximate hours and what you cut.
  > `docs/declared_effort.md` — L1: ~7.0h, L2: ~6.0h, combined: ~13.0h. Descoped: demo recording, CI pipeline, containerized OrangeHRM.

## Evidence standard

Every claim cites a specific input, tool call, trace, or measured number. "The
agent recovers from failures" scores nothing. "When the pricing tool returned a
string instead of a float, validation rejected it, the retry included the schema
mismatch, and the second attempt succeeded — trace attached" scores.

If you concluded during the build that your problem did not actually need an
agent, say so in your reflection. That finding, honestly reported and evidenced,
scores better than an agent nobody needed.

## Before you submit — challenge your own work

- [x] Is the problem I chose narrow enough that I have actually solved it, rather than gestured at it?
  > Yes — 7 specific functional requirements for one target application, with passing test suites as the acceptance bar.

- [x] Can I explain every significant decision and the alternatives I rejected?
  > Yes — `docs/stack_observability.md` covers rejected alternatives: LangGraph, n8n, AutoGPT, Selenium, Behave, Robot Framework. Each rejection has a stated reason.

- [x] Would my solution survive being pointed at data I did not choose?
  > Partially — the agent validates selectors against the live DOM before generating code, so it would adapt to a different app. However, the Page Object class names and step definitions are OrangeHRM-specific. A new app would require a new migration session, not just re-running the existing suite.

- [x] Have I named specific inputs where it fails, or only described failure in general terms?
  > Yes — `docs/agent_evaluation.md`: Employee ID `0428` conflicting with existing demo user; `all_text_contents('.oxd-input-field-error-message')` returning `[]` when DOM contained 2 error elements; `from playwright.pages.login_page import LoginPage` resolving to installed package.

- [x] Does my write-up let the work speak for itself, without guessing at how it will be scored?
  > Yes — `REFLECTION.md` describes what was built and what failed with specific commit SHAs, tool call outputs, and measured times. No claims without cited evidence.

## How this will be assessed

There is no answer key for this case, because you defined the problem. You are
scored against the criteria for your level and against your own stated definition
of success — so a vague definition of success is not a safe choice, it is an
unscoreable one.

Two things carry disproportionate weight:

1. **Your data.** Where it came from, what it does and does not represent, and
   whether it contains cases that genuinely stress your solution. Data selected
   to flatter the prototype is a finding against you, not a neutral choice.
2. **Your failure analysis.** Specific inputs, specific wrong outputs, specific
   causes. "It sometimes struggles with ambiguous cases" is not a failure
   analysis.

You will answer several questions about your own submission at submission time.
They are generated from what you submitted — your stated problem, your data
decisions, your architecture — so they cannot be prepared in advance.
