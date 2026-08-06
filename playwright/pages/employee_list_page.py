from playwright.sync_api import Page
from .base_page import BasePage

class EmployeeListPage(BasePage):
    URL = "/web/index.php/pim/viewEmployeeList"

    NAME_INPUT = '.oxd-input-group:has-text("Employee Name") .oxd-autocomplete-text-input input'
    SEARCH_BUTTON = 'button:has-text("Search")'
    TABLE_ROWS = '.oxd-table-body .oxd-table-row'

    def visit(self):
        self.navigate(self.URL)

    def search_by_name(self, name: str):
        self.page.fill(self.NAME_INPUT, name)
        self.page.wait_for_timeout(800)
        suggestion = self.page.locator('.oxd-autocomplete-dropdown .oxd-autocomplete-option').first
        if suggestion.is_visible():
            suggestion.click()

    def click_search(self):
        self.page.click(self.SEARCH_BUTTON)
        self.page.wait_for_load_state("networkidle")

    def get_result_rows(self):
        return self.page.locator(self.TABLE_ROWS)
