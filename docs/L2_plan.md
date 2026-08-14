# L2 Work Plan — Cypress → Playwright Migration Agent

**Branch:** L2  
**Baseline:** Phase 1 (Cypress + Playwright suites, 8 specs each) delivered on `master`.  
**Goal:** Satisfy all L2 evaluation criteria by demonstrating a working, documented, and evaluated agent.

---

## Scope

L2 extends L1 in three dimensions:

1. **Agent documentation** — make the existing agent's decision model, tool usage, memory tier, and failure handling explicit and traceable.
2. **Evaluation evidence** — produce objective proof that the agent works (test output, failure injection, observability traces, pytest-asyncio suite).
3. **Communication** — REFLECTION.md, updated declared-effort, and a complete slide deck.

L2 does NOT rewrite the existing test suites. The Cypress and Playwright suites are the agent's output; they stay as-is except for known bugs listed below.

---

## Architecture Decisions (recorded before implementation)

| Component | Choice | Rationale |
|---|---|---|
| Agent runtime | Claude Code (MCP + tools) | Already configured; provides browser, file, and memory tools in a single session. Avoided LangGraph (more overhead) and n8n (no code-level access to generated artifacts). |
| Browser tool | MCP Playwright | Live selector verification against the real app. No static codemod can do this. |
| Memory tier | Short-term (session context) | The migration workflow is stateless across sessions — each run re-explores the app from scratch. No long-term memory needed; CLAUDE.md provides the persistent convention layer. |
| Human gate | Explicit confirmation before first `git commit` and before any delete operation on demo data | Irreversible actions: committing generated tests and cleaning test fixtures from the shared demo. |
| Failure handling | validate → retry with specific error → escalate after 2 failures | Tool output (selector snapshot, generated code) is checked against criteria before proceeding; failure reason is embedded in the retry prompt. |
| BDD runner | pytest-bdd (not Behave) | Simpler fixture integration with pytest; native `scope="session"` fixtures for runtime_data. |
| Observability | Claude Code transcript + session task output files | Portkey/LangSmith not configured; transcript captures every tool call, input, and output as the equivalent trace. |

---

## Task Breakdown

### A — Git / Spec-Driven (this plan)
- [x] **A1** — Commit L2 spec (problem_statement.md, agent decision, data provenance) as first L2 commit.
- [x] **A2** — Commit L2 plan (this file) as second L2 commit.
- [ ] **A3** — Update `requirements/functional_requirements_Cypress.md` lines 26–28 with current live demo values (Nationality, Marital Status, Date of Birth).

### B — Code: Known Bugs
- [ ] **B1** — Fix `playwright/tests/step_defs/req_007_steps.py:8`: replace hardcoded `"mandaa user"` string with `.oxd-userdropdown-tab` selector.
- [ ] **B2** — Fix `playwright/tests/step_defs/req_002_steps.py`: remove hardcoded claim reference `"202307180000002"`, use `ref_id` from fixture or env.
- [ ] **B3** — Add post-scenario teardown in `playwright/tests/step_defs/req_005_steps.py` to delete the employee created during the test.
- [ ] **B4 (pre-001 fixes)** — Commit the already-implemented fixes: `cypress.config.ts` runtimeData, `AddEmployeePage.ts` fillEmployeeId + empNumber capture, `add_employee_page.py` graceful "already exists" handling, `pre_001_steps.py` runtime_data capture.

### C — Tests: Execution Evidence
- [ ] **C1** — Re-run Playwright 8 tests after B4 fix and capture clean 8/8 report under `reports/playwright/`.
- [ ] **C2** — Document known instability of shared demo as a measured limitation (not a defect in the tests).

### D — Agent Architecture Documentation
- [ ] **D1** — Write `docs/agent_architecture.md`: tools, memory tier (with justification), human gate behavior, failure handling protocol.
- [ ] **D2** — Confirm `.claude/agents/playwright-migration.md` accurately describes the agent's runtime decision flow.

### E — Agent Evaluation
- [ ] **E1** — Write `docs/agent_evaluation.md`: evaluation criteria, 2+ mechanistic failure cases (input → wrong output → root cause).
- [ ] **E2** — Document the deliberate failure injection performed (Employee ID conflict scenario) and the agent's response.
- [ ] **E3** — Create `tests/agent/test_agent_loop.py` — pytest-asyncio suite covering agent loop, tool mock, and recovery path.

### F — Observability
- [ ] **F1** — Document how to read the Claude Code session transcript as an observability trace (tool calls, inputs, outputs).
- [ ] **F2** — Include a representative excerpt in `docs/agent_evaluation.md` or as a separate `docs/trace_sample.md`.

### G — Communication
- [ ] **G1** — Write `REFLECTION.md` (600–1000 words): what was built, why, what failed, how it was fixed, what would be done differently, business impact.
- [ ] **G2** — Update `docs/declared_effort.md` with L2 hours and what was cut.
- [ ] **G3** — Complete all blank slides in `docs/AI_Capstone_L2_Julian Largo.pptx` (slides 1, 3–9, 11–12).

---

## Commit Strategy

Each task group above maps to one or more atomic commits. The L2 branch git history will show:

1. `spec(L2)` — problem statement (committed)
2. `plan(L2)` — this document (next commit)
3. `fix(pre-001)` — implementation fixes for pre-condition tests
4. `fix(bugs)` — B1–B3 code fixes
5. `docs(agent)` — D1–D2 architecture documentation
6. `docs(eval)` — E1–E2 evaluation and failure analysis
7. `test(agent)` — E3 pytest-asyncio suite
8. `docs(reflect)` — G1–G2 reflection and declared effort
9. `docs(ppt)` — G3 presentation (binary, tracked separately)
