from playwright.sync_api import Page
from .base_page import BasePage

class MyInfoPage(BasePage):
    URL = "/web/index.php/pim/viewMyDetails"

    def visit(self):
        self.navigate(self.URL)

    def _field_input(self, label: str):
        return self.page.locator('.oxd-input-group').filter(has_text=label).locator('input')

    def _field_select_text(self, label: str):
        return self.page.locator('.oxd-input-group').filter(has_text=label).locator('.oxd-select-text-input')

    def get_first_name(self) -> str:
        return self.page.input_value('input[name="firstName"]')

    def get_middle_name(self) -> str:
        return self.page.input_value('input[name="middleName"]')

    def get_last_name(self) -> str:
        return self.page.input_value('input[name="lastName"]')

    def get_employee_id(self) -> str:
        return self._field_input("Employee Id").input_value()

    def get_other_id(self) -> str:
        return self._field_input("Other Id").input_value()

    def get_nationality(self) -> str:
        return self._field_select_text("Nationality").text_content()

    def get_marital_status(self) -> str:
        return self._field_select_text("Marital Status").text_content()

    def get_date_of_birth(self) -> str:
        return self._field_input("Date of Birth").input_value()

    def get_gender(self) -> str:
        checked = self.page.locator('.oxd-radio-input:checked')
        wrapper = checked.locator('xpath=ancestor::*[contains(@class,"oxd-radio-wrapper")]')
        return wrapper.locator('span').last.text_content()
