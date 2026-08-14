from playwright.sync_api import Page
from .base_page import BasePage

class AddEmployeePage(BasePage):
    URL = "/web/index.php/pim/addEmployee"

    FIRST_NAME = 'input[name="firstName"]'
    MIDDLE_NAME = 'input[name="middleName"]'
    LAST_NAME = 'input[name="lastName"]'
    EMPLOYEE_ID = '.oxd-input-group:has-text("Employee Id") input'
    LOGIN_TOGGLE = '.oxd-switch-input'
    USERNAME_INPUT = '.oxd-input-group:has-text("Username") input'
    SAVE_BUTTON = 'button:has-text("Save")'

    def visit(self):
        self.navigate(self.URL)
        self.page.wait_for_load_state("networkidle")

    def fill_first_name(self, name: str):
        self.page.fill(self.FIRST_NAME, name)

    def fill_middle_name(self, name: str):
        self.page.fill(self.MIDDLE_NAME, name)

    def fill_last_name(self, name: str):
        self.page.fill(self.LAST_NAME, name)

    def fill_employee_id(self, emp_id: str):
        self.page.fill(self.EMPLOYEE_ID, emp_id)

    def enable_login_details(self):
        self.page.locator(self.LOGIN_TOGGLE).click()
        self.page.wait_for_timeout(400)

    def fill_username(self, username: str):
        self.page.fill(self.USERNAME_INPUT, username)

    def fill_password(self, password: str):
        self.page.evaluate(f"""() => {{
            const groups = document.querySelectorAll('.oxd-input-group');
            const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
            const pwdInputs = Array.from(groups)
                .filter(g => g.querySelector('input[type=password]'))
                .map(g => g.querySelector('input[type=password]'));
            pwdInputs.forEach(inp => {{
                setter.call(inp, '{password}');
                inp.dispatchEvent(new Event('input', {{ bubbles: true }}));
                inp.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }});
        }}""")

    def click_save(self):
        self.page.locator(self.SAVE_BUTTON).click()

        # Wait for either the success redirect or a validation error to appear.
        # networkidle alone resolves before Vue renders inline error messages.
        self.page.wait_for_function(
            """() =>
                window.location.href.includes('pim/viewPersonalDetails/empNumber/') ||
                document.querySelector('.oxd-input-field-error-message') !== null
            """,
            timeout=12000,
        )

        if "pim/viewPersonalDetails/empNumber/" in self.page.url:
            return  # employee created successfully

        # Check for "already exists" validation errors (e.g. sequential run after Cypress)
        error_texts = self.page.locator('.oxd-input-field-error-message').all_text_contents()
        if any("already exists" in e for e in error_texts):
            return  # employee/username already present — acceptable

        raise AssertionError(
            f"Employee save failed unexpectedly. URL: {self.page.url}. Errors: {error_texts}"
        )
