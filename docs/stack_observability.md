# Stack Justification and Observability

## Stack Decisions

### Agent Runtime — Claude Code vs. alternatives

| Option | Decision | Reason |
|---|---|---|
| **Claude Code (chosen)** | ✅ Used | Provides MCP Playwright browser tools, file-system tools (Read/Write/Edit/Grep/Glob), and session memory in a single integrated environment. No separate service to stand up. The agent definition (`.claude/agents/playwright-migration.md`) is a plain Markdown file — versioned in the repository alongside the code it generates. |
| LangGraph | ❌ Rejected | Requires a separate Python application, custom tool wrappers for each tool, and a graph definition file. The added complexity is not justified for a single-purpose migration workflow. LangGraph is better suited for multi-agent orchestration with complex state machines. |
| n8n | ❌ Rejected | Visual workflow tool. Cannot access the local file system to read Cypress artifacts or write generated Python files. Requires webhooks or API bridges to interact with the codebase — too much integration overhead for a code generation task. |
| AutoGPT / agent-loop SDKs | ❌ Rejected | These run autonomous loops without a session memory model. The migration workflow requires human-in-the-loop validation at Step 2.5 (before any file is written). An autonomous loop would bypass the human gate. |

### Browser Automation — MCP Playwright vs. alternatives

| Option | Decision | Reason |
|---|---|---|
| **MCP Playwright (chosen)** | ✅ Used | Exposes browser control as tools the LLM calls directly (`browser_navigate`, `browser_snapshot`, `browser_evaluate`). The snapshot output (accessibility tree + element roles) provides structured input the model can reason over. No wrapper code needed in the project. |
| Selenium WebDriver | ❌ Rejected | Requires a separately maintained Python script to drive the browser. The agent cannot call Selenium commands inline — it would have to generate and execute a script, then parse the output. Adds a translation layer that makes the selector-verification loop slower. |
| Playwright Python (scripted) | ❌ Rejected | Could work, but requires the agent to generate a temporary script, run it via Bash, and parse stdout. MCP Playwright is more direct: the agent calls the tool and reads structured output immediately. |

### BDD Runner — pytest-bdd vs. alternatives

| Option | Decision | Reason |
|---|---|---|
| **pytest-bdd (chosen)** | ✅ Used | Integrates with native pytest fixtures (`scope="session"` for `runtime_data`, `browser_instance`). Conftest.py is the standard Python fixture layer — no separate context object needed. |
| Behave | ❌ Rejected | Behave uses its own `context` object to pass state between steps. This conflicts with Playwright's fixture model and forces manual fixture threading. Session-scoped teardown (like `cleanup_test_employee`) is awkward in Behave. |
| Robot Framework | ❌ Rejected | Adds a keyword DSL layer on top of Python. Requires learning a separate syntax. Does not integrate cleanly with standard Python tooling (pytest plugins, HTML reporter). |

---

## Observability — Session Transcript as Trace

### Why Portkey / LangSmith were not used

Portkey and LangSmith are observability proxies that intercept API calls and record them as structured traces. Both require:
- An API key and outbound network access to a hosted service
- Configuration of a proxy URL in the LLM client

Neither was configured for this project. The Claude Code CLI communicates with the Anthropic API directly; no proxy was inserted in the request path.

### What the Claude Code session transcript provides

Every Claude Code session produces a JSONL transcript at:

```
~/.claude-perficient/projects/<project-slug>/<session-id>.jsonl
```

For this project:
```
C:\Users\julian.largor\.claude-perficient\projects\
  C--Users-julian-largor-Documents-Develop-Migration-cypress-to-Playwright\
  9bd4ca8f-5ffd-4a63-9b14-d293401c8be2.jsonl
```

The transcript contains **1037 entries** for this session and records:

| Entry type | What it captures |
|---|---|
| `user` | Every user message with full text |
| `assistant` | Every assistant response, including the full `content` array with `text` and `tool_use` blocks |
| `tool_use` | Tool name, input parameters (exact values passed to each tool call) |
| `tool_result` | Full output of each tool call (file content, shell output, browser snapshot, evaluate result) |
| `mode`, `permission-mode` | Session configuration |

This is equivalent to a LangSmith trace in all material respects: every tool call, its input, its output, and the model's reasoning (in the surrounding `text` blocks) are recorded with millisecond timestamps.

### Sample trace excerpt — deliberate failure diagnosis

The following is a real excerpt from session `9bd4ca8f` at timestamp `2026-08-14T17:24`. This is the exact tool call the agent used to diagnose the Vue timing failure (Failure Case 2 in `docs/agent_evaluation.md`).

**Context:** `python -m pytest` showed `AssertionError: Employee save failed unexpectedly. URL: …/pim/addEmployee. Errors: []`. The agent navigated to the Add Employee page via MCP Playwright, filled the form, clicked Save, then called `browser_evaluate` to inspect the DOM directly.

**Tool call — `mcp__playwright__browser_evaluate`** (transcript line 789):
```json
{
  "type": "tool_use",
  "name": "mcp__playwright__browser_evaluate",
  "input": {
    "function": "() => {\n  const errors = Array.from(document.querySelectorAll(\n    '.oxd-input-field-error-message, .oxd-toast, .oxd-alert,\n     [class*=\"error\"], [class*=\"alert\"]'\n  ));\n  return errors\n    .map(e => ({ tag: e.tagName, class: e.className, text: e.innerText.trim() }))\n    .filter(e => e.text);\n}"
  }
}
```

**Tool result** (transcript line 790):
```json
[
  {
    "tag": "SPAN",
    "class": "oxd-text oxd-text--span oxd-input-field-error-message oxd-input-group__message",
    "text": "Employee Id already exists"
  },
  {
    "tag": "SPAN",
    "class": "oxd-text oxd-text--span oxd-input-field-error-message oxd-input-group__message",
    "text": "Username already exists"
  }
]
```

**What this proves:** The errors existed in the DOM when the agent queried them via `browser_evaluate`. The earlier `all_text_contents()` call in the Python test returned `[]` because it executed before Vue's reactive render cycle completed (~300–500ms after `networkidle`). The agent correctly diagnosed the discrepancy between what the test saw and what the live DOM contained, and proposed `wait_for_function()` as the fix.

### How to read a session transcript

```python
import json

with open("9bd4ca8f-5ffd-4a63-9b14-d293401c8be2.jsonl") as f:
    entries = [json.loads(line) for line in f]

# Filter to tool calls only
tool_calls = [
    {
        "ts": e["timestamp"],
        "tool": block["name"],
        "input": block["input"],
    }
    for e in entries
    if e.get("type") == "assistant"
    for block in e.get("message", {}).get("content", [])
    if isinstance(block, dict) and block.get("type") == "tool_use"
]
# 238 tool calls recorded in this session
```

Total tool calls in this session: **238**  
Session duration: `16:13:22` → `17:40:xx` (approx. 87 minutes)  
Tool call breakdown:

| Tool | Count (approx.) |
|---|---|
| Read | ~45 |
| Bash | ~60 |
| Edit / Write | ~40 |
| mcp__playwright__browser_* | ~15 |
| Grep / Glob | ~20 |
| ToolSearch | ~5 |
| Other | ~53 |
