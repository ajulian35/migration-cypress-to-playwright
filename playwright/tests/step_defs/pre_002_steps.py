from pytest_bdd import scenarios, when, then, parsers
from playwright.sync_api import Page
from pages.claim_page import ClaimPage

scenarios("../../features/pre_002_create_claim.feature")

@when("I navigate to the Submit Claim page")
def navigate_submit_claim(page: Page, base_url: str):
    claim = ClaimPage(page, base_url)
    claim.navigate_to_submit_claim()

@when(parsers.cfparse('I select the event "{event_name}"'))
def select_event(page: Page, base_url: str, event_name: str):
    claim = ClaimPage(page, base_url)
    claim.select_event(event_name)

@when(parsers.cfparse('I select the currency "{currency_name}"'))
def select_currency(page: Page, base_url: str, currency_name: str):
    claim = ClaimPage(page, base_url)
    claim.select_currency(currency_name)

@when("I create the claim")
def create_claim(page: Page, base_url: str):
    claim = ClaimPage(page, base_url)
    claim.click_create()

@when(parsers.cfparse('I add an expense of "{amount}"'))
def add_expense(page: Page, base_url: str, amount: str):
    claim = ClaimPage(page, base_url)
    claim.add_expense("Accommodation", "2026-08-06", amount)

@when("I submit the claim")
def submit_claim(page: Page, base_url: str):
    claim = ClaimPage(page, base_url)
    claim.click_submit_claim()

@then(parsers.cfparse('the claim status should show "{expected_status}"'))
def check_claim_submitted_status(page: Page, expected_status: str):
    # Wait for the status field to update after Submit
    page.wait_for_function(
        f"() => Array.from(document.querySelectorAll('input[disabled]')).some(el => el.value === '{expected_status}')",
        timeout=10000
    )
    status_inputs = page.locator('input[disabled]')
    values = [status_inputs.nth(i).input_value() for i in range(status_inputs.count())]
    assert expected_status in values, f"Expected '{expected_status}' in disabled inputs: {values}"
