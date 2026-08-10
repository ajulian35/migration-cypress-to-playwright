from pytest_bdd import scenarios, when, then, parsers
from playwright.sync_api import Page
from pages.claim_page import ClaimPage

scenarios("../../features/req_002_claim_validation.feature")

@when("I navigate to My Claims")
def navigate_my_claims(page: Page, base_url: str):
    claim = ClaimPage(page, base_url)
    claim.navigate_to_my_claims()

@when("I click the search button")
def click_search(page: Page, base_url: str):
    claim = ClaimPage(page, base_url)
    claim.click_search()

@then(parsers.cfparse('a submitted claim with event "{event_name}" should be visible'))
def check_submitted_claim_visible(page: Page, event_name: str):
    rows = page.locator('.oxd-table-body .oxd-table-row')
    count = rows.count()
    found = any(
        event_name in (rows.nth(i).text_content() or "") and
        "Submitted" in (rows.nth(i).text_content() or "")
        for i in range(count)
    )
    assert found, f"No submitted row found with event '{event_name}'"

@then(parsers.cfparse('the claim currency should show "{expected}"'))
def check_claim_currency(page: Page, expected: str):
    rows = page.locator('.oxd-table-body .oxd-table-row')
    count = rows.count()
    found = any(
        "Medical Reimbursement" in (rows.nth(i).text_content() or "") and
        expected in (rows.nth(i).text_content() or "")
        for i in range(count)
    )
    assert found, f"No row found with currency '{expected}'"

@then(parsers.cfparse('the claim amount should show "{expected}"'))
def check_claim_amount(page: Page, expected: str):
    rows = page.locator('.oxd-table-body .oxd-table-row')
    count = rows.count()
    found = any(
        "Medical Reimbursement" in (rows.nth(i).text_content() or "") and
        expected in (rows.nth(i).text_content() or "")
        for i in range(count)
    )
    assert found, f"No row found with amount '{expected}'"
