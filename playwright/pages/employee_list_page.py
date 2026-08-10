from playwright.sync_api import Page
from .base_page import BasePage

class EmployeeListPage(BasePage):
    URL = "/web/index.php/directory/viewDirectory"

    NAME_INPUT = 'input[placeholder="Type for hints..."]'
    SEARCH_BUTTON = 'button:has-text("Search")'
    RESULT_CARDS = '.orangehrm-directory-card'
    RESULT_COUNT = '.orangehrm-directory-result-content, .orangehrm-container'

    def visit(self):
        self.navigate(self.URL)
        self.page.wait_for_load_state("networkidle")

    def search_by_name(self, name: str):
        self.page.fill(self.NAME_INPUT, name)
        self.page.wait_for_selector('[role="listbox"] [role="option"]', timeout=5000)
        self.page.locator('[role="listbox"] [role="option"]').first.click()

    def click_search(self):
        self.page.click(self.SEARCH_BUTTON)
        # Wait for results to update — either a card appears or "No Records Found"
        self.page.wait_for_selector(
            f'{self.RESULT_CARDS}, .oxd-text:has-text("No Records")',
            timeout=15000
        )

    def get_result_rows(self):
        return self.page.locator(self.RESULT_CARDS)
