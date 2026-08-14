# Agent Architecture — Cypress → Playwright Migration Agent

## Agent Identity

**Name:** `playwright-migration`  
**Definition:** `.claude/agents/playwright-migration.md`  
**Runtime:** Claude Code (Anthropic) with MCP Playwright and file-system tools  
**Invocation:** One agent call per requirement ID (e.g. `REQ-001`)

---

## P5 Confirmation — Does the Agent Decide at Runtime?

The `playwright-migration` agent meets the L2 definition of an agent ("the model decides what to do at runtime rather than following a hardcoded sequence") on three counts:

### 1. Selector strategy is not predetermined

The agent reads the Cypress selector (e.g. `cy.contains('.oxd-input-group', 'Employee Id').find('input')`), then navigates the live DOM and decides which Playwright equivalent to use. The choice between `getByRole(…)`, `locator('.css-class')`, `locator(':has-text(…) input')`, or `locator('input[name="…"]')` depends on:

- Whether the element has a stable ARIA role at the time of inspection
- Whether the CSS class is specific enough (not shared by multiple elements)
- Whether the text-based selector resolves to exactly one element

A deterministic transpiler would copy the Cypress selector. The agent snapshots the page and chooses based on what it observes.

### 2. The agent stops and escalates when validation fails

The agent's definition states: **"Do not generate code if Step 2 validation failed."** This is a conditional branch — not a linear sequence. If a selector resolves to zero elements, the agent:
- Reports the failure with the actual DOM state
- Asks for human guidance before proceeding
- Retries with a different selector strategy if one is available from the snapshot

A script has no equivalent mechanism. It would write broken locators silently.

### 3. BDD structure is inferred, not templated

The number of Gherkin steps, the granularity of each step, and whether state is shared via `Background` or per-scenario fixtures are all decisions the agent makes by reading the test intent and the page flow. Two tests with the same structure may produce different Gherkin depending on whether the agent determines that steps can be reused across scenarios.

---

## Tools Invoked

### Tool 1 — MCP Playwright Browser (`mcp__playwright__browser_*`)

**Used in:** Step 2 (live validation)

| Tool call | Purpose |
|---|---|
| `browser_navigate` | Open the target page for the requirement |
| `browser_snapshot` | Capture accessibility tree to identify element roles and selectors |
| `browser_click`, `browser_fill_form` | Reproduce the Cypress test steps against the live app |
| `browser_evaluate` | Query the DOM directly when snapshot is ambiguous (e.g. Vue-rendered inputs) |

**Why this requires an agent:** The snapshot output is different on every run depending on the live app state. The agent must interpret the snapshot and make a selection — there is no fixed mapping.

### Tool 2 — File System (Read, Write, Edit, Grep, Glob)

**Used in:** Step 1 (read Cypress artifacts) and Step 3 (write Playwright artifacts)

| Tool call | Purpose |
|---|---|
| `Read` | Load Cypress spec and Page Object source |
| `Glob` | Discover which Page Objects exist for the target requirement |
| `Grep` | Find selector patterns and existing step definitions to avoid duplication |
| `Write` / `Edit` | Create or update the Gherkin feature file, Python POM, and step definitions |

### Tool 3 — Bash (`python -m pytest`)

**Used in:** Post-generation validation (Step 3.4)

After writing the generated files, the agent runs `python -m pytest tests/step_defs/<req>_steps.py -v` and reads the output. If the test fails, the agent diagnoses the error and corrects the generated code before reporting success to the user.

---

## Memory Architecture

### Tier chosen: Short-term (in-context conversation window) + Session-persistent convention layer (CLAUDE.md)

| Tier | What is stored | Why |
|---|---|---|
| **In-context (short-term)** | Extracted selectors, DOM snapshot content, validation results, intermediate generated code | The migration is a single-session task. State does not need to survive beyond the conversation. |
| **CLAUDE.md (session-persistent)** | Project conventions: POM structure, import path rules (`from pages.X import Y`), file naming (`snake_case`), `.env` usage, constraint list | Loaded fresh every session — serves as the agent's procedural memory so it doesn't re-derive conventions from the codebase each time. |
| **Long-term memory (not used)** | — | Each migration re-derives everything from Cypress artifacts. There is no accumulated state that would improve future migrations. The Cypress artifacts are the authoritative source. |

**Why short-term is sufficient:** The agent is stateless across requirements. REQ-002 migration does not benefit from knowing how REQ-001 was migrated. If a selector strategy worked for one page, it is not necessarily correct for another page with different DOM structure.

**Why CLAUDE.md is the right persistent layer:** Import conventions, file paths, and POM patterns are project-wide invariants, not per-run discoveries. Storing them in CLAUDE.md means they are available to any future agent call without requiring re-exploration of the codebase.

---

## Human Validation Gate

The agent has an explicit gate before any file write.

### Gate location: End of Step 2 (before Step 3)

After completing the live validation, the agent presents a summary to the user:
- Which selectors were confirmed
- Which selectors were adjusted (and why)
- Whether all assertions matched the expected values from the requirements doc
- Whether any prerequisite state (e.g. test user must exist) was not satisfied

**The agent does not write any file until the user confirms the summary is acceptable.**

This gate exists because:
- Writing files is partially irreversible (overwriting an existing step file loses its history in the working tree)
- The user may want to adjust a validation result before it becomes code
- If the live app behavior differs from the spec (data drift), the user must decide whether to update the spec or accept the observed value

### Gate in the agent definition

`.claude/agents/playwright-migration.md` — Step 2 ends with:
> "Do not generate code if Step 2 validation failed."

And the CLAUDE.md system instruction states:
> "For actions that are hard to reverse... check with the user before proceeding."

Claude Code enforces tool permission prompts for file writes — the user sees every `Write` or `Edit` call and can deny it before the file is modified.

### Additional gate: before demo data operations

The `cleanup_test_employee` fixture in `conftest.py` is session-scoped and runs as a teardown — only after all tests have completed. Data deletion on the shared demo happens at the end of the session, not mid-run, to avoid affecting dependent tests.

---

## Failure Handling

| Failure type | Detection | Response |
|---|---|---|
| Selector resolves to 0 elements | `browser_snapshot` shows no match | Report specific selector + actual DOM excerpt; ask user how to proceed |
| Selector resolves to N > 1 elements | Snapshot shows multiple matches | Try a more specific selector strategy; if still ambiguous, report all candidates and ask |
| Generated test fails on first run | `pytest` output shows error | Read the traceback, correct the specific line, re-run; after 2 failures escalate with full context |
| Prerequisite state missing (e.g. employee not created) | URL does not redirect as expected | Stop, report exact URL and expected URL, ask user to confirm precondition before retrying |

**Retry protocol:** On first failure, the retry prompt includes:
1. The original selector/code
2. The exact error message
3. The DOM state at the time of failure (snapshot excerpt)

This ensures the retry is targeted, not blind.

---

## Stack Justification

| Component | Chosen | Rejected alternatives | Reason |
|---|---|---|---|
| Agent runtime | Claude Code (this session) | LangGraph, n8n, AutoGPT | Claude Code provides MCP Playwright integration, file tools, and session memory in a single environment. LangGraph requires a separate Python service and custom tool wrappers. n8n cannot access the local file system for code generation. |
| Browser automation | MCP Playwright | Selenium, direct Playwright Python | MCP Playwright exposes browser control as tools the LLM can call directly — no wrapper code needed. Selenium requires a separate scripted driver. |
| BDD runner | pytest-bdd | Behave, Robot Framework | pytest-bdd integrates naturally with pytest fixtures (session scope, conftest.py). Behave has a separate context object that conflicts with Playwright's fixture model. Robot Framework adds keyword DSL overhead. |
| Observability | Claude Code session transcript | Portkey, LangSmith | The transcript captures every tool call, input, output, and decision in a structured JSONL format. Portkey/LangSmith provide richer dashboards but require API key setup and outbound network access not configured in this environment. |
