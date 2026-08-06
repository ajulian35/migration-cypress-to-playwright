from playwright.sync_api import Page
from .base_page import BasePage

class AddEmployeePage(BasePage):
    URL = "/web/index.php/pim/addEmployee"

    FIRST_NAME = 'input[name="firstName"]'
    LAST_NAME = 'input[name="lastName"]'
    SAVE_BUTTON = 'button[type="submit"]'

    def visit(self):
        self.navigate(self.URL)

    def fill_first_name(self, name: str):
        self.page.fill(self.FIRST_NAME, name)

    def fill_last_name(self, name: str):
        self.page.fill(self.LAST_NAME, name)

    def click_save(self):
        self.page.click(self.SAVE_BUTTON)
        self.page.wait_for_url("**/pim/viewPersonalDetails/empNumber/**")
