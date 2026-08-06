from playwright.sync_api import Page
from .base_page import BasePage

class ClaimPage(BasePage):
    EMPLOYEE_CLAIMS_LINK = 'text=Employee Claims'
    EVENT_NAME_DROPDOWN = '.oxd-input-group:has-text("Event Name") .oxd-select-text'
    SEARCH_BUTTON = 'button:has-text("Search")'
    TABLE_ROWS = '.oxd-table-body .oxd-table-row'

    def navigate_to_employee_claims(self):
        self.navigate("/web/index.php/claim/viewClaimModule")
        self.page.click(self.EMPLOYEE_CLAIMS_LINK)
        self.page.wait_for_selector(self.SEARCH_BUTTON)

    def select_event_name(self, name: str):
        self.page.click(self.EVENT_NAME_DROPDOWN)
        self.page.locator(f'role=option[name="{name}"]').click()

    def click_search(self):
        self.page.click(self.SEARCH_BUTTON)
        self.page.wait_for_load_state("networkidle")

    def get_result_rows(self):
        return self.page.locator(self.TABLE_ROWS)
