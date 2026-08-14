from playwright.sync_api import Page
from .base_page import BasePage

class ClaimPage(BasePage):
    EMPLOYEE_CLAIMS_TAB = '.oxd-topbar-body-nav-tab:has-text("Employee Claims")'
    MY_CLAIMS_TAB = '.oxd-topbar-body-nav-tab:has-text("My Claims")'
    SEARCH_BUTTON = 'button:has-text("Search")'
    TABLE_ROWS = '.oxd-table-body .oxd-table-row'
    SUBMIT_CLAIM_URL = "/web/index.php/claim/submitClaim"

    def navigate_to_employee_claims(self):
        self.navigate("/web/index.php/claim/viewClaimModule")
        self.page.locator(self.EMPLOYEE_CLAIMS_TAB).click()
        self.page.wait_for_selector(self.SEARCH_BUTTON)

    def navigate_to_my_claims(self):
        self.navigate("/web/index.php/claim/viewClaimModule")
        self.page.wait_for_selector(self.SEARCH_BUTTON)

    def navigate_to_submit_claim(self):
        self.navigate(self.SUBMIT_CLAIM_URL)
        self.page.wait_for_load_state("networkidle")

    def select_event(self, event_name: str):
        event_dropdown = self.page.locator('.oxd-select-wrapper').first
        event_dropdown.click()
        self.page.get_by_role("option", name=event_name).click()

    def select_currency(self, currency_name: str):
        currency_dropdown = self.page.locator('.oxd-select-wrapper').nth(1)
        currency_dropdown.click()
        self.page.get_by_role("option", name=currency_name).click()

    def click_create(self):
        self.page.get_by_role("button", name="Create").click()
        self.page.wait_for_url("**/claim/submitClaim/id/**", timeout=10000)

    def add_expense(self, expense_type: str, date: str, amount: str):
        self.page.get_by_role("button", name=" Add").first.click()
        self.page.wait_for_selector('[role="dialog"] .oxd-select-wrapper', timeout=5000)
        self.page.locator('[role="dialog"] .oxd-select-wrapper').click()
        self.page.get_by_role("option", name=expense_type).click()
        # Date field
        self.page.locator('[role="dialog"]').get_by_placeholder("yyyy-dd-mm").fill(date)
        # Amount field — target by placeholder absence (only plain textbox in row)
        amount_input = self.page.locator('[role="dialog"] .oxd-input-group').filter(
            has_text="Amount"
        ).locator('input')
        amount_input.clear()
        amount_input.fill(amount)
        self.page.locator('[role="dialog"]').get_by_role("button", name="Save").click()
        self.page.wait_for_load_state("networkidle")

    def click_submit_claim(self):
        self.page.get_by_role("button", name="Submit").click()
        # Wait until status field changes to Submitted
        self.page.wait_for_function(
            "() => Array.from(document.querySelectorAll('input[disabled]')).some(el => el.value === 'Submitted')",
            timeout=15000
        )

    def click_search(self):
        self.page.click(self.SEARCH_BUTTON)
        self.page.wait_for_load_state("networkidle")

    def get_result_rows(self):
        return self.page.locator(self.TABLE_ROWS)
