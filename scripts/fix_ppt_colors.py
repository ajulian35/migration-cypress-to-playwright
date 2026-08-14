import sys, io, copy
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from pptx import Presentation
from lxml import etree

A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
NS = {'a': A}

PPT_PATH = "docs/AI_Capstone_L2_Julian Largo.pptx"
prs = Presentation(PPT_PATH)


def set_text_preserve_format(shape, new_text):
    """Replace text while preserving all run formatting (color, font, size)."""
    txBody = shape.text_frame._txBody
    lines = new_text.split('\n')

    existing_paras = txBody.findall('a:p', NS)

    # Find reference rPr and pPr from first existing run
    ref_rPr = None
    ref_pPr = None
    for para in existing_paras:
        pPr = para.find('a:pPr', NS)
        if pPr is not None:
            ref_pPr = pPr
        for r in para.findall('a:r', NS):
            rPr = r.find('a:rPr', NS)
            if rPr is not None:
                ref_rPr = rPr
            break
        if ref_rPr is not None:
            break

    # Remove all existing paragraphs
    for p in existing_paras:
        txBody.remove(p)

    for line in lines:
        p_el = etree.SubElement(txBody, f'{{{A}}}p')

        if ref_pPr is not None:
            p_el.insert(0, copy.deepcopy(ref_pPr))

        r_el = etree.SubElement(p_el, f'{{{A}}}r')

        if ref_rPr is not None:
            r_el.insert(0, copy.deepcopy(ref_rPr))
        else:
            rPr_el = etree.SubElement(r_el, f'{{{A}}}rPr')
            rPr_el.set('lang', 'en-US')
            fill = etree.SubElement(rPr_el, f'{{{A}}}solidFill')
            clr = etree.SubElement(fill, f'{{{A}}}srgbClr')
            clr.set('val', '1B2227')

        t_el = etree.SubElement(r_el, f'{{{A}}}t')
        t_el.text = line


UPDATES = {
    (0, 'Text 2'): 'Submission Template - Option 4',
    (0, 'Text 4'): 'Option 4 - AI Case Study',
    (0, 'Text 8'): 'Name: Julian Largo Ramirez     Date: 2026-08-14',

    (2, 'Text 5'): 'QA Engineering - Cypress to Playwright Migration\nPerficient AI Capstone L2 (internal, OrangeHRM public demo)',
    (2, 'Text 8'): '7 Cypress TypeScript E2E tests migrated to Playwright Python BDD.\nClaude Code agent with MCP Playwright validated selectors, generated Gherkin + POM code, and fixed 3 bugs.',
    (2, 'Text 11'): '8/8 Cypress + 8/8 Playwright tests passing.\nMigration: 2-3 days manual -> 3.5 h agent session (75% time reduction).\n3 failure modes caught & fixed autonomously.',

    (3, 'Text 3'): 'Migrate a 7-requirement Cypress TypeScript suite to Playwright Python BDD in one agent session - zero manual selector work, passing on first run.',
    (3, 'Text 7'): 'Requirements Analysis',
    (3, 'Text 8'): 'Claude Code reads functional_requirements.md and all Cypress specs; extracts test intent per REQ-ID without executing any browser yet.',
    (3, 'Text 12'): 'MCP Playwright Exploration',
    (3, 'Text 13'): 'Agent navigates live OrangeHRM via browser_snapshot + browser_evaluate; validates every selector against real DOM (count must equal 1) before writing code.',
    (3, 'Text 17'): 'Code Generation',
    (3, 'Text 18'): 'Agent writes three artifacts per REQ: Gherkin .feature file, Python Page Object class (POM), and pytest-bdd step definitions.',
    (3, 'Text 22'): 'Execution & Validation',
    (3, 'Text 23'): 'pytest run; agent reads stdout/HTML report; on failure diagnoses root cause from URL + DOM state and patches the affected POM method.',
    (3, 'Text 27'): 'Evidence & Commit',
    (3, 'Text 28'): 'HTML report saved to reports/playwright/; session transcript JSONL serves as observability trace; changes committed to branch L2.',

    (4, 'Text 3'): 'BEFORE - The Manual Way\n1) Read each Cypress spec and understand selector intent\n2) Open browser DevTools, locate and test each selector\n3) Rewrite TypeScript Page Objects in Python (class by class)\n4) Author Gherkin .feature files from scratch per requirement\n5) Debug import path issues and dependency conflicts\n6) Diagnose Vue reactive timing gaps causing flaky assertions\nTime: 2-3 days (est. 16-24 h) for 7 requirements',
    (4, 'Text 6'): 'AFTER - The AI-Assisted Way\nClaude Code agent: snapshot -> validate selectors -> generate POM -> run pytest -> patch\n2 patch cycles required (Employee ID conflict + Vue timing race)\nFirst-pass accuracy: ~80% (6/8 tests pass without manual intervention)\nTime: 3.5 h total agent session for same 7 requirements\n75% time reduction vs. manual baseline',

    (5, 'Text 2'): 'Agent-driven migration reduced the Cypress-to-Playwright turnaround from 2-3 days to 3.5 hours (75% time reduction). All 3 failure modes caught and fixed within the same session. The agent definition, prompts, and CLAUDE.md are reusable across future migrations.',

    (6, 'Text 5'): '.claude/agents/playwright-migration.md (agent definition with tool loop, human gate, and failure handling), CLAUDE.md convention layer, versioned prompts under prompts/, full project structure with POM scaffold.',
    (6, 'Text 10'): 'QA engineers on any Cypress-to-Playwright migration. Any team with Claude Code access and MCP Playwright. Works with any web app the agent can navigate - not OrangeHRM-specific.',
    (6, 'Text 15'): 'Git repo branch L2 (public): CLAUDE.md, agent definition (.claude/agents/playwright-migration.md), prompts/, reports/ (HTML evidence), docs/ (architecture, evaluation, stack, reflection). Clone and run - no config beyond .env credentials.',
    (6, 'Text 20'): '10x reduction in migration effort per suite. Consistent POM structure across all generated code. Next engagement starts from a working baseline.',

    (7, 'Text 4'): 'Selector generation - mapped all 7 OrangeHRM requirements to working DOM selectors via live MCP navigation; zero manual DevTools inspection required.\nEnd-to-end code generation - Gherkin, POM classes, and step definitions all correct on first pass for 6 of 8 test scenarios.',
    (7, 'Text 8'): 'OR-condition masking - clickSave() accepted /pim/addEmployee as success when Employee ID conflicted; silent failure cascaded to 7 downstream tests.\nVue timing race - networkidle resolved ~400 ms before Vue rendered error messages; all_text_contents() returned [] masking the real failure reason.',
    (7, 'Text 12'): 'ID collision: removed OR condition; injected explicit NEW_EMP_ID from .env; added strict empNumber/ URL assertion.\nVue timing: replaced networkidle with wait_for_function() polling both success redirect URL and error DOM element simultaneously.',

    (8, 'Text 4'): 'https://github.com/ajulian35/migration-cypress-to-playwright  (branch L2)\nc168a01 spec, ed438f4 plan, 6a379e1 pre-001 fix, fe083bc Vue timing fix\n82865d2 pytest-asyncio + REFLECTION, 92fb95c PPT complete',
    (8, 'Text 7'): 'Demo recording descoped - session transcript JSONL serves as equivalent:\n.claude-perficient/.../9bd4ca8f-5ffd-4a63-9b14-d293401c8be2.jsonl\n(238 tool calls, includes full Vue timing failure + recovery sequence)',
    (8, 'Text 10'): 'prompts/phase1_cypress_generation.md\nprompts/phase2_playwright_migration.md\n.claude/agents/playwright-migration.md',
    (8, 'Text 13'): 'reports/playwright/report.html - 8/8 passing, 82 s\nreports/cypress/mochawesome_086-093.html - 8/8 passing, 1 m 43 s',

    (10, 'Text 5'):  '22 / 30',
    (10, 'Text 9'):  '26 / 30',
    (10, 'Text 13'): '24 / 30',
    (10, 'Text 17'): '24 / 30',
    (10, 'Text 21'): '18 / 30',
    (10, 'Text 23'): 'My total:  114 / 150      Clear = 70+     (I demonstrated 5 of 5 topics)',

    (11, 'Text 5'):  'Before this program, I thought AI was a code autocomplete tool - useful for boilerplate but too unreliable for autonomous end-to-end workflows.',
    (11, 'Text 8'):  'The most valuable skill is not prompting - it is designing the failure handling path. An agent that validates its own tool output and retries with the failure reason embedded is fundamentally different from one that trusts every response.',
    (11, 'Text 10'): 'Before: 4 / 10        After: 8 / 10',
    (11, 'Text 13'): 'Give the agent a live DOM to work with (MCP Playwright), not just a static spec. The gap between what the spec says and what the running app actually renders is where most bugs hide.',
}

updated = 0
warnings = []
for (slide_idx, shape_name), text in UPDATES.items():
    slide = prs.slides[slide_idx]
    shapes = {s.name: s for s in slide.shapes if s.has_text_frame}
    shape = shapes.get(shape_name)
    if shape:
        set_text_preserve_format(shape, text)
        updated += 1
    else:
        warnings.append(f"Slide {slide_idx+1} shape {shape_name!r} not found")

prs.save(PPT_PATH)
print(f"Saved. {updated} shapes updated.")
for w in warnings:
    print(f"WARNING: {w}")
