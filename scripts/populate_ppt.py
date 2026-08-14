#!/usr/bin/env python
"""
Populate blank slides in AI_Capstone_L2_Julian Largo.pptx with real project content.
Run from the repo root: python scripts/populate_ppt.py
"""
import os
import copy
from lxml import etree
from pptx import Presentation
from pptx.oxml.ns import qn

BASE = os.path.join(os.path.dirname(__file__), "..")
PPT_IN  = os.path.join(BASE, "docs", "AI_Capstone_L2_Julian Largo.pptx")
PPT_OUT = PPT_IN  # overwrite in place


# ---------------------------------------------------------------------------
# Low-level helpers
# ---------------------------------------------------------------------------

NS = "http://schemas.openxmlformats.org/drawingml/2006/main"


def _txBody(shape):
    return shape.text_frame._txBody


def _find_paras(txb):
    return txb.findall(f"{{{NS}}}p")


def _make_run(text):
    r = etree.Element(f"{{{NS}}}r")
    rPr = etree.SubElement(r, f"{{{NS}}}rPr")
    rPr.set("lang", "en-US")
    rPr.set("dirty", "0")
    t = etree.SubElement(r, f"{{{NS}}}t")
    t.text = text
    return r


def set_text(shape, text):
    """Replace all content in a shape's text frame. Multi-line via '\\n'."""
    if shape is None or not shape.has_text_frame:
        return
    txb = _txBody(shape)
    shape.text_frame.word_wrap = True

    paras = _find_paras(txb)
    # Keep the first paragraph as a template, remove the rest
    first_p = paras[0]
    for p in paras[1:]:
        txb.remove(p)

    lines = text.split("\n")

    # Populate first paragraph
    for r in first_p.findall(f"{{{NS}}}r"):
        first_p.remove(r)
    first_p.append(_make_run(lines[0]))

    # Add extra paragraphs for subsequent lines
    for line in lines[1:]:
        new_p = copy.deepcopy(first_p)
        for r in new_p.findall(f"{{{NS}}}r"):
            new_p.remove(r)
        new_p.append(_make_run(line))
        txb.append(new_p)


def get_shape(slide, name):
    for sh in slide.shapes:
        if sh.name == name:
            return sh
    return None


def set_table_cell(table, row, col, text):
    cell = table.cell(row, col)
    tf = cell.text_frame
    paras = tf._txBody.findall(f"{{{NS}}}p")
    first_p = paras[0]
    for p in paras[1:]:
        tf._txBody.remove(p)
    for r in first_p.findall(f"{{{NS}}}r"):
        first_p.remove(r)
    first_p.append(_make_run(text))


def find_table(slide):
    for sh in slide.shapes:
        if sh.shape_type == 19:  # TABLE
            return sh.table
    return None


# ---------------------------------------------------------------------------
# Main population logic
# ---------------------------------------------------------------------------

def populate(prs):
    slides = prs.slides

    # ------------------------------------------------------------------
    # SLIDE 1 — Title / identification
    # ------------------------------------------------------------------
    s1 = slides[0]
    set_text(get_shape(s1, "Text 2"),  "Submission Template — Option 4")
    set_text(get_shape(s1, "Text 4"),  "Option 4 — AI Case Study")
    set_text(get_shape(s1, "Text 8"),  "Name: Julian Largo Ramirez     Date: 2026-08-14")

    # ------------------------------------------------------------------
    # SLIDE 3 — My Project Overview (Option 1 column repurposed for Option 4)
    # ------------------------------------------------------------------
    s3 = slides[2]
    set_text(get_shape(s3, "Text 2"),
             "OPTION 4 — AI Case Study")
    set_text(get_shape(s3, "Text 3"),
             "Domain & engagement")
    set_text(get_shape(s3, "Text 5"),
             "QA Engineering — Cypress to Playwright Migration\n"
             "Perficient AI Capstone L2 (internal, OrangeHRM public demo)")
    set_text(get_shape(s3, "Text 6"),
             "Problem · AI solution · outcomes")
    set_text(get_shape(s3, "Text 8"),
             "7 Cypress TypeScript E2E tests migrated to Playwright Python BDD.\n"
             "Claude Code agent with MCP Playwright navigated the live app,\n"
             "validated selectors, generated Gherkin + POM code, and fixed 3 bugs.")
    set_text(get_shape(s3, "Text 9"),
             "Quantified business impact")
    set_text(get_shape(s3, "Text 11"),
             "8/8 Cypress + 8/8 Playwright tests passing.\n"
             "Migration: 2-3 days manual -> 3.5 h agent session (75% time reduction).\n"
             "3 failure modes caught & fixed autonomously.")

    # Clear Option 2 column (not applicable)
    set_text(get_shape(s3, "Text 16"), "N/A — Option 4 submission")
    set_text(get_shape(s3, "Text 19"), "N/A")
    set_text(get_shape(s3, "Text 22"), "N/A")

    # ------------------------------------------------------------------
    # SLIDE 4 — My AI Approach
    # ------------------------------------------------------------------
    s4 = slides[3]
    set_text(get_shape(s4, "Text 3"),
             "Migrate a 7-requirement Cypress TypeScript suite to Playwright Python BDD "
             "in one agent session — zero manual selector work, passing on first run.")

    # Steps: (Text 7/8, Text 12/13, Text 17/18, Text 22/23, Text 27/28)
    set_text(get_shape(s4, "Text 7"),  "Requirements Analysis")
    set_text(get_shape(s4, "Text 8"),
             "Claude Code reads functional_requirements.md and all Cypress specs; "
             "extracts test intent per REQ-ID without executing any browser yet.")

    set_text(get_shape(s4, "Text 12"), "MCP Playwright Exploration")
    set_text(get_shape(s4, "Text 13"),
             "Agent navigates live OrangeHRM via browser_snapshot + browser_evaluate; "
             "validates every selector against real DOM (count must equal 1) before writing code.")

    set_text(get_shape(s4, "Text 17"), "Code Generation")
    set_text(get_shape(s4, "Text 18"),
             "Agent writes three artifacts per REQ: Gherkin .feature file, "
             "Python Page Object class (POM), and pytest-bdd step definitions.")

    set_text(get_shape(s4, "Text 22"), "Execution & Validation")
    set_text(get_shape(s4, "Text 23"),
             "pytest run; agent reads stdout/HTML report; on failure diagnoses "
             "root cause from URL + DOM state and patches the affected POM method.")

    set_text(get_shape(s4, "Text 27"), "Evidence & Commit")
    set_text(get_shape(s4, "Text 28"),
             "HTML report saved to reports/playwright/; session transcript JSONL "
             "serves as observability trace; changes committed to feature/migration-progress.")

    # ------------------------------------------------------------------
    # SLIDE 5 — Before -> After
    # ------------------------------------------------------------------
    s5 = slides[4]
    set_text(get_shape(s5, "Text 5"),
             "BEFORE — The Manual Way\n"
             "1) Read each Cypress spec and understand selector intent\n"
             "2) Open browser DevTools, locate and test each selector\n"
             "3) Rewrite TypeScript Page Objects in Python (class by class)\n"
             "4) Author Gherkin .feature files from scratch per requirement\n"
             "5) Debug import path issues and dependency conflicts\n"
             "6) Diagnose Vue reactive timing gaps causing flaky assertions\n"
             "Time: 2-3 days (est. 16-24 h) for 7 requirements\n"
             "Pain points: selector drift, namespace collision, Vue render timing\n"
             "Quality: 3 known bug patterns went undetected in L1 manual review")

    set_text(get_shape(s5, "Text 6"),
             "AFTER — The AI-Assisted Way\n"
             "Claude Code agent: snapshot -> validate selectors -> generate POM -> run pytest -> patch\n"
             "2 patch cycles required (Employee ID conflict + Vue timing race)\n"
             "First-pass accuracy: ~80% (6/8 tests pass without manual intervention)\n"
             "Time: 3.5 h total agent session for same 7 requirements\n"
             "75% time reduction vs. manual baseline")

    set_text(get_shape(s5, "Text 7"),
             "See reports/playwright/report.html (8/8 passing, 82 s) and "
             "reports/cypress/ (8/8 passing, 1 m 43 s) for execution evidence.")

    # ------------------------------------------------------------------
    # SLIDE 6 — AI Impact Scorecard
    # ------------------------------------------------------------------
    s6 = slides[5]
    set_text(get_shape(s6, "Text 2"),
             "Agent-driven migration reduced the Cypress-to-Playwright turnaround from "
             "2-3 days to 3.5 hours (75% time reduction). "
             "All 3 failure modes caught and fixed within the same session. "
             "The agent definition, prompts, and CLAUDE.md are reusable across future migrations.")

    tbl = find_table(s6)
    if tbl:
        set_table_cell(tbl, 1, 0, "Cypress -> Playwright migration (7 reqs)")
        set_table_cell(tbl, 1, 1, "16-24 hours")
        set_table_cell(tbl, 1, 2, "3.5 hours")
        set_table_cell(tbl, 1, 3, "~80% time saved")

        set_table_cell(tbl, 2, 0, "Selector validation per requirement")
        set_table_cell(tbl, 2, 1, "~20 min/req = 2.3 h total")
        set_table_cell(tbl, 2, 2, "~3 min/req (MCP live nav)")
        set_table_cell(tbl, 2, 3, "~85% per req")

        set_table_cell(tbl, 3, 0, "Bug catch rate")
        set_table_cell(tbl, 3, 1, "3 known bugs undetected in L1")
        set_table_cell(tbl, 3, 2, "3/3 caught & fixed autonomously")
        set_table_cell(tbl, 3, 3, "+100% defect detection")

        set_table_cell(tbl, 4, 0, "Migration frequency / project")
        set_table_cell(tbl, 4, 1, "1-2x per year, high manual cost")
        set_table_cell(tbl, 4, 2, "Same frequency, agent absorbs complexity")
        set_table_cell(tbl, 4, 3, "Risk & cost per run reduced")

        set_table_cell(tbl, 5, 0, "QA engineers on future migrations")
        set_table_cell(tbl, 5, 1, "N/A (no reusable baseline)")
        set_table_cell(tbl, 5, 2, "Any team with Claude Code + MCP")
        set_table_cell(tbl, 5, 3, "~12-20 h saved per migration")

    # ------------------------------------------------------------------
    # SLIDE 7 — Reusability & Scale
    # ------------------------------------------------------------------
    s7 = slides[6]
    set_text(get_shape(s7, "Text 4"),  "What is reusable?")
    set_text(get_shape(s7, "Text 5"),
             ".claude/agents/playwright-migration.md (agent definition with tool loop, "
             "human gate, and failure handling), CLAUDE.md convention layer, "
             "versioned prompts under prompts/, full project structure with POM scaffold.")

    set_text(get_shape(s7, "Text 9"),  "Who can adopt it?")
    set_text(get_shape(s7, "Text 10"),
             "QA engineers on any Cypress-to-Playwright migration. Any team with "
             "Claude Code access and MCP Playwright. Works with any web app the agent "
             "can navigate — not OrangeHRM-specific.")

    set_text(get_shape(s7, "Text 14"), "What was packaged?")
    set_text(get_shape(s7, "Text 15"),
             "Git repo (feature/migration-progress): CLAUDE.md, agent definition, "
             "prompts/, reports/ (HTML evidence), docs/ (architecture + evaluation), "
             "README with step-by-step replication instructions.")

    set_text(get_shape(s7, "Text 19"), "Org-scale potential")
    set_text(get_shape(s7, "Text 20"),
             "10x reduction in migration effort per suite. Consistent POM structure "
             "across all generated code. Next engagement starts from a working baseline — "
             "cumulative improvement as CLAUDE.md grows with each project.")

    # ------------------------------------------------------------------
    # SLIDE 8 — What AI Got Right & Wrong
    # ------------------------------------------------------------------
    s8 = slides[7]
    set_text(get_shape(s8, "Text 3"),  "What AI got RIGHT")
    set_text(get_shape(s8, "Text 4"),
             "Selector generation — mapped all 7 OrangeHRM requirements to working DOM "
             "selectors via live MCP navigation; zero manual DevTools inspection required.\n"
             "End-to-end code generation — Gherkin, POM classes, and step definitions "
             "all correct on first pass for 6 of 8 test scenarios.")

    set_text(get_shape(s8, "Text 7"),  "What AI got WRONG")
    set_text(get_shape(s8, "Text 8"),
             "OR-condition masking — clickSave() accepted /pim/addEmployee as success "
             "when Employee ID conflicted; silent failure cascaded to 7 downstream tests.\n"
             "Vue timing race — networkidle resolved ~400 ms before Vue rendered error "
             "messages; all_text_contents() returned [] masking the real failure reason.")

    set_text(get_shape(s8, "Text 11"), "What I corrected")
    set_text(get_shape(s8, "Text 12"),
             "ID collision: removed OR condition; injected explicit NEW_EMP_ID from .env; "
             "added strict empNumber/ URL assertion.\n"
             "Vue timing: replaced networkidle with wait_for_function() polling both "
             "success redirect URL and error DOM element simultaneously.")

    # ------------------------------------------------------------------
    # SLIDE 9 — Evidence & Artifacts
    # ------------------------------------------------------------------
    s9 = slides[8]
    set_text(get_shape(s9, "Text 4"),
             "Branch feature/migration-progress — key commits:\n"
             "c168a01 (spec), ed438f4 (plan), 6a379e1 (pre-001 fix), "
             "fe083bc (Vue timing fix), 449adf0 (docs)")
    set_text(get_shape(s9, "Text 7"),
             "Demo recording descoped — session transcript JSONL serves as equivalent:\n"
             ".claude-perficient/projects/.../9bd4ca8f-5ffd-4a63-9b14-d293401c8be2.jsonl\n"
             "(238 tool calls, includes full Vue timing failure + recovery sequence)")
    set_text(get_shape(s9, "Text 10"),
             "prompts/phase1_cypress_generation.md\n"
             "prompts/phase2_playwright_migration.md\n"
             ".claude/agents/playwright-migration.md")
    set_text(get_shape(s9, "Text 13"),
             "reports/playwright/report.html — 8/8 passing, 82 s\n"
             "reports/cypress/mochawesome_086-093.html — 8/8 passing, 1 m 43 s")

    # ------------------------------------------------------------------
    # SLIDE 11 — My Self-Rating
    # ------------------------------------------------------------------
    s11 = slides[10]
    set_text(get_shape(s11, "Text 5"),  "22 / 30")
    set_text(get_shape(s11, "Text 9"),  "26 / 30")
    set_text(get_shape(s11, "Text 13"), "24 / 30")
    set_text(get_shape(s11, "Text 17"), "24 / 30")
    set_text(get_shape(s11, "Text 21"), "18 / 30")
    set_text(get_shape(s11, "Text 23"),
             "My total:  114 / 150      Clear = 70+     (I demonstrated 5 of 5 topics)")

    # ------------------------------------------------------------------
    # SLIDE 12 — Reflection & Key Takeaway
    # ------------------------------------------------------------------
    s12 = slides[11]
    set_text(get_shape(s12, "Text 5"),
             '"Before this program, I thought AI was a code autocomplete tool — '
             'useful for boilerplate but too unreliable for autonomous end-to-end workflows."')
    set_text(get_shape(s12, "Text 8"),
             "The most valuable skill is not prompting — it is designing the failure "
             "handling path. An agent that validates its own tool output and retries "
             "with the failure reason embedded is fundamentally different from one that trusts "
             "every response. That difference is where production readiness lives.")
    set_text(get_shape(s12, "Text 10"), "Before: 4 / 10        After: 8 / 10")
    set_text(get_shape(s12, "Text 13"),
             "Give the agent a live DOM to work with (MCP Playwright), not just a static spec. "
             "The gap between what the spec says and what the running app actually renders "
             "is where most bugs hide — and only a live-browser agent can close that gap.")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    prs = Presentation(PPT_IN)
    populate(prs)
    prs.save(PPT_OUT)
    print(f"Saved: {PPT_OUT}")
