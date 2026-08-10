# Submission Checklist — L1_Case05_Open_Choice_Prototype

You chose this case, so you own the scope. Everything below is required
regardless of what you built.

## Define

- [x] Problem statement: the domain, the user, the problem, and your definition of success.
  → `docs/problem_statement.md`
- [x] Why this problem is worth solving, in terms a client stakeholder would recognise.
  → `docs/problem_statement.md` — "Why This Is Worth Solving" section
- [x] Data provenance note: where the data came from or how you generated it, what it does and does not represent, its known limitations, and how you handled anything sensitive.
  → `docs/data_provenance.md`

## Build

- [x] Working prototype, demonstrable end to end. Polish is explicitly not scored.
  → Cypress 8/8 passing (`reports/cypress/`), Playwright 8/8 passing (`reports/playwright/`)
- [x] Spec, plan, and task artifacts, with commit history showing they preceded the implementation.
  → `requirements/functional_requirements_Cypress.md`, `CLAUDE.md`, `.claude/skills/cypress-test-gen.md`, `.claude/agents/playwright-migration.md`, and `criteria_checklist.md` are all present in commit `59af56b` (the initial commit). **Known limitation:** the requirements and implementation land in the same commit because the project was initialized from a working session rather than a blank repo. The requirements document and agent skill files were authored before code generation — the workflow is documented in `migration_workflow.md` sections 2 and 3 — but the git history does not record that sequence separately.
- [x] A context artifact (`CLAUDE.md`) plus before-and-after evidence of its effect on output quality.
  → `CLAUDE.md` at project root; `docs/claude_md_evidence.md` documents 7 specific CLAUDE.md instructions with before/after code comparison showing the effect on naming, POM structure, credential handling, and requirement traceability.
- [ ] Either a retrieval pipeline over your own documents or a working AI-in-the-loop n8n automation, with a stated reason for choosing that over the other.
  → **Not implemented.** Decision documented in `docs/declared_effort.md`: n8n was out of scope given the time available and the nature of the project (test migration, not document retrieval). A retrieval pipeline over project documents was also not implemented — the agent workflow operates directly on live application state via MCP Playwright, not over a document corpus. This item is a known gap in the submission.

## Prove

- [x] Your review of what the AI generated for you, across intent, tests, security, performance, and maintainability — including at least one error you caught and corrected.
  → `docs/ai_review.md` — covers all 5 dimensions; 3 errors documented with before/after code
- [x] Failure analysis naming specific inputs that break the prototype and why.
  → `docs/failure_analysis.md` — 5 failure scenarios, each with specific triggering input, exact wrong output, root cause, and resolution status
- [x] One measured improvement: the before state, the change, the after state, and anything that got worse.
  → `docs/measured_improvement.md` — REQ-006 autocomplete: `wait_for_timeout(800)` replaced with `wait_for_selector` + name filter; FAILED → PASSED verified with test output

## Communicate

- [x] One slide pitching the solution to client stakeholders.
  → `docs/AI_Capstone_Filled_L1.pptx` and `docs/stakeholder_slide.md`
- [ ] A short demo (recording or transcript), including at least one case it handles badly.
  → **Descoped** per user decision. The failure cases are documented in `docs/failure_analysis.md` with specific inputs and outputs.
- [x] Declared-effort statement: approximate hours and what you cut.
  → `docs/declared_effort.md` — ~7h total, itemized by activity, with explicit list of what was cut

## Before you submit — challenge your own work

- [x] Is the problem I chose narrow enough that I have actually solved it, rather than gestured at it?
  → Yes. The problem is specifically "migrate a 7-requirement Cypress TypeScript suite to Playwright Python BDD using an agent-driven workflow." Both suites run and pass against the live app.
- [x] Can I explain every significant decision and the alternatives I rejected?
  → Yes. pytest-bdd vs Behave, POM preservation, n8n descope, and credential handling are all explained in `migration_workflow.md` section 7 and `docs/declared_effort.md`.
- [x] Would my solution survive being pointed at data I did not choose?
  → Partially. The workflow is reusable — the agent prompts and project structure are portable. But the generated assertions are calibrated to the specific OrangeHRM demo instance. Limitations documented in `docs/failure_analysis.md` (last section).
- [x] Have I named specific inputs where it fails, or only described failure in general terms?
  → Yes. `docs/failure_analysis.md` names specific files, line numbers, exact assertion values, and exact error messages for each failure.
- [x] Does my write-up let the work speak for itself, without guessing at how it will be scored?
  → Yes. Every claim in the documentation cites a specific file, line, test output, or measured number.

## Evidence standard

Every claim cites a specific input, output, file, or measured number. "Retrieval
works well" scores nothing. "On these three queries the assistant cited the wrong
source document, because my chunking split the table away from its heading"
scores.

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
