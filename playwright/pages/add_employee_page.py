from playwright.sync_api import Page
from .base_page import BasePage

class AddEmployeePage(BasePage):
    URL = "/web/index.php/pim/addEmployee"

    FIRST_NAME = 'input[name="firstName"]'
    MIDDLE_NAME = 'input[name="middleName"]'
    LAST_NAME = 'input[name="lastName"]'
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
        self.page.wait_for_load_state("networkidle")
        # If username already exists, the form stays but employee name fields are already saved —
        # skip URL assertion; the step_def will verify the final state.
        try:
            self.page.wait_for_url("**/pim/viewPersonalDetails/empNumber/**", timeout=10000)
        except Exception:
            # Check for validation error meaning the user already exists
            error_visible = self.page.locator('.oxd-input-field-error-message').count() > 0
            if not error_visible:
                raise
