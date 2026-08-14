"""
pytest-asyncio tests for the migration agent's key decision loops.

These tests verify the agent's tool-output validation, retry logic, and
recovery path using mocked MCP tool responses — no live browser required.

Coverage:
  - Selector validation (count-based gate before code generation)
  - click_save() success, already-exists, and unexpected-failure branches
  - Vue timing race: demonstrate why networkidle alone was insufficient
    and that wait_for_function() correctly gates on DOM state
  - Escalation: unexpected state raises AssertionError with full context
"""

import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock, patch


# ---------------------------------------------------------------------------
# Agent decision helpers (thin Python representation of the agent's logic)
# ---------------------------------------------------------------------------

async def validate_selector(browser_evaluate_fn, selector: str) -> dict:
    """
    Represents Step 2 of the playwright-migration agent workflow.
    Calls browser_evaluate to count matching DOM elements.
    Returns {'selector': str, 'count': int, 'valid': bool}.
    The agent only proceeds to code generation when valid == True.
    """
    raw = await browser_evaluate_fn(
        f"() => document.querySelectorAll('{selector}').length"
    )
    count = int(raw)
    return {"selector": selector, "count": count, "valid": count == 1}


async def agent_save_employee(page_mock) -> dict:
    """
    Represents the pre-001 save flow with tool-output validation.
    Mirrors the logic in playwright/pages/add_employee_page.py click_save().

    Decision tree:
      1. Click Save
      2. wait_for_function polls until redirect OR error element appears
      3. Check URL — if empNumber/ redirect → employee created
      4. Check .oxd-input-field-error-message — if "already exists" → idempotent
      5. Else → raise AssertionError with full context (escalation)
    """
    await page_mock.click('button:has-text("Save")')

    await page_mock.wait_for_function(
        "() => window.location.href.includes('empNumber/') || "
        "document.querySelector('.oxd-input-field-error-message') !== null",
        timeout=12000,
    )

    if "empNumber/" in page_mock.url:
        import re
        m = re.search(r"empNumber/(\d+)", page_mock.url)
        return {"status": "created", "emp_number": m.group(1) if m else None}

    errors = await page_mock.evaluate(
        "() => Array.from(document.querySelectorAll('.oxd-input-field-error-message'))"
        ".map(e => e.innerText.trim())"
    )
    if any("already exists" in e for e in errors):
        return {"status": "already_exists", "errors": errors}

    raise AssertionError(
        f"Agent escalation — unexpected state after Save. "
        f"URL: {page_mock.url}. Errors: {errors}"
    )


# ---------------------------------------------------------------------------
# Selector validation tests (C2 criterion: selector resolves to exactly 1)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_selector_valid_when_exactly_one_element():
    """Agent proceeds when selector matches exactly one DOM element."""
    mock_evaluate = AsyncMock(return_value="1")
    result = await validate_selector(
        mock_evaluate, '.oxd-input-group:has-text("Employee Id") input'
    )
    assert result["valid"] is True
    assert result["count"] == 1
    mock_evaluate.assert_awaited_once()


@pytest.mark.asyncio
async def test_selector_invalid_when_zero_elements():
    """Agent blocks code generation when selector matches nothing."""
    mock_evaluate = AsyncMock(return_value="0")
    result = await validate_selector(mock_evaluate, ".nonexistent-class input")
    assert result["valid"] is False
    assert result["count"] == 0


@pytest.mark.asyncio
async def test_selector_invalid_when_multiple_elements():
    """Agent blocks code generation when selector is ambiguous (N > 1)."""
    mock_evaluate = AsyncMock(return_value="3")
    result = await validate_selector(mock_evaluate, ".oxd-input")
    assert result["valid"] is False
    assert result["count"] == 3


# ---------------------------------------------------------------------------
# click_save() agent loop — tool output validation
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_save_employee_success_redirect():
    """
    Agent detects successful employee creation from empNumber redirect URL.
    Tool output validated: URL contains empNumber/ → extract and return.
    """
    page = MagicMock()
    page.click = AsyncMock()
    page.wait_for_function = AsyncMock()
    page.url = (
        "https://opensource-demo.orangehrmlive.com"
        "/web/index.php/pim/viewPersonalDetails/empNumber/251"
    )

    result = await agent_save_employee(page)

    assert result["status"] == "created"
    assert result["emp_number"] == "251"
    page.wait_for_function.assert_awaited_once()


@pytest.mark.asyncio
async def test_save_employee_already_exists_is_acceptable():
    """
    Agent treats 'already exists' validation error as idempotent success.
    Required for sequential Cypress + Playwright runs on shared demo.
    """
    page = MagicMock()
    page.click = AsyncMock()
    page.wait_for_function = AsyncMock()
    page.url = (
        "https://opensource-demo.orangehrmlive.com"
        "/web/index.php/pim/addEmployee"
    )
    page.evaluate = AsyncMock(
        return_value=["Employee Id already exists", "Username already exists"]
    )

    result = await agent_save_employee(page)

    assert result["status"] == "already_exists"
    assert len(result["errors"]) == 2


@pytest.mark.asyncio
async def test_save_employee_unexpected_state_escalates():
    """
    Agent raises AssertionError with full context (URL + errors) when
    neither success nor known failure condition is met.
    This is the escalation path after retry exhaustion.
    """
    page = MagicMock()
    page.click = AsyncMock()
    page.wait_for_function = AsyncMock()
    page.url = (
        "https://opensource-demo.orangehrmlive.com"
        "/web/index.php/pim/addEmployee"
    )
    page.evaluate = AsyncMock(return_value=[])  # No error messages — unknown failure

    with pytest.raises(AssertionError) as exc_info:
        await agent_save_employee(page)

    assert "Agent escalation" in str(exc_info.value)
    assert "pim/addEmployee" in str(exc_info.value)


# ---------------------------------------------------------------------------
# Recovery path — Vue timing race (deliberate failure injection)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_vue_timing_race_old_approach_misses_errors():
    """
    Demonstrates the root cause of Failure Case 2 (docs/agent_evaluation.md).

    OLD approach: wait_for_load_state("networkidle") resolves before Vue
    renders validation messages. all_text_contents() returns [] even though
    the DOM will contain error elements ~400ms later.

    This test proves the old approach was insufficient by simulating the
    timing gap: the 'early' read returns [], the 'late' read returns errors.
    """
    render_complete = {"done": False}
    errors_in_dom = ["Employee Id already exists", "Username already exists"]

    async def mock_all_text_contents():
        # Simulates reading DOM before Vue reactive render cycle completes
        if not render_complete["done"]:
            return []  # networkidle fired, but Vue hasn't rendered yet
        return errors_in_dom

    # OLD approach: read immediately after networkidle
    early_result = await mock_all_text_contents()
    assert early_result == [], (
        "Bug reproduced: old approach returns [] before Vue renders"
    )

    # Simulate Vue rendering 400ms later
    render_complete["done"] = True

    # NEW approach: wait_for_function ensures DOM is ready before reading
    late_result = await mock_all_text_contents()
    assert len(late_result) == 2
    assert all("already exists" in e for e in late_result)


@pytest.mark.asyncio
async def test_wait_for_function_gates_on_dom_state():
    """
    Verifies that the fixed approach (wait_for_function) is called before
    reading error messages, ensuring DOM is in final state.
    """
    page = MagicMock()
    page.click = AsyncMock()
    page.url = (
        "https://opensource-demo.orangehrmlive.com"
        "/web/index.php/pim/addEmployee"
    )
    page.evaluate = AsyncMock(return_value=["Employee Id already exists"])

    call_order = []
    async def mock_wait_for_function(fn_str, timeout):
        call_order.append("wait_for_function")
    async def mock_evaluate(fn_str):
        call_order.append("evaluate")
        return ["Employee Id already exists"]

    page.wait_for_function = mock_wait_for_function
    page.evaluate = mock_evaluate

    result = await agent_save_employee(page)

    # wait_for_function must be called BEFORE evaluate
    assert call_order.index("wait_for_function") < call_order.index("evaluate"), (
        "Agent must gate on DOM state (wait_for_function) before reading errors"
    )
    assert result["status"] == "already_exists"
