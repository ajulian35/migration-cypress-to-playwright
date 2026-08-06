from pytest_bdd import scenarios, when, then
from playwright.sync_api import Page
from pages.claim_page import ClaimPage

scenarios("../../features/req_002_claim_validation.feature")

@when("I navigate to Employee Claims")
def navigate_employee_claims(page: Page, base_url: str):
    claim = ClaimPage(page, base_url)
    claim.navigate_to_employee_claims()

@when('I filter by event name "{name}"')
def filter_event_name(page: Page, base_url: str, name: str):
    claim = ClaimPage(page, base_url)
    claim.select_event_name(name)

@when("I click the search button")
def click_search(page: Page, base_url: str):
    claim = ClaimPage(page, base_url)
    claim.click_search()

@then('a claim record with reference id "{ref_id}" should be visible')
def check_ref_id(page: Page, ref_id: str):
    row = page.locator(f'.oxd-table-body .oxd-table-row:has-text("{ref_id}")')
    assert row.count() > 0

@then('the claim employee name should be "{expected}"')
def check_claim_employee(page: Page, expected: str):
    row = page.locator('.oxd-table-body .oxd-table-row:has-text("202307180000002")')
    assert expected in row.text_content()

@then('the claim event name should be "{expected}"')
def check_claim_event(page: Page, expected: str):
    row = page.locator('.oxd-table-body .oxd-table-row:has-text("202307180000002")')
    assert expected in row.text_content()

@then('the claim currency should be "{expected}"')
def check_claim_currency(page: Page, expected: str):
    row = page.locator('.oxd-table-body .oxd-table-row:has-text("202307180000002")')
    assert expected in row.text_content()

@then('the claim submitted date should be "{expected}"')
def check_claim_date(page: Page, expected: str):
    row = page.locator('.oxd-table-body .oxd-table-row:has-text("202307180000002")')
    assert expected in row.text_content()

@then('the claim status should be "{expected}"')
def check_claim_status(page: Page, expected: str):
    row = page.locator('.oxd-table-body .oxd-table-row:has-text("202307180000002")')
    assert expected in row.text_content()

@then('the claim amount should be "{expected}"')
def check_claim_amount(page: Page, expected: str):
    row = page.locator('.oxd-table-body .oxd-table-row:has-text("202307180000002")')
    assert expected in row.text_content()
