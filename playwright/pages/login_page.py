from playwright.sync_api import Page
from .base_page import BasePage

class LoginPage(BasePage):
    URL = "/web/index.php/auth/login"

    USERNAME_INPUT = 'input[name="username"]'
    PASSWORD_INPUT = 'input[name="password"]'
    LOGIN_BUTTON = 'button[type="submit"]'
    ERROR_ALERT = '.oxd-alert-content-text'

    def visit(self):
        self.navigate(self.URL)

    def fill_username(self, username: str):
        self.page.fill(self.USERNAME_INPUT, username)

    def fill_password(self, password: str):
        self.page.fill(self.PASSWORD_INPUT, password)

    def click_login(self):
        self.page.click(self.LOGIN_BUTTON)

    def login(self, username: str, password: str):
        self.fill_username(username)
        self.fill_password(password)
        self.click_login()

    def get_error_message(self) -> str:
        return self.page.text_content(self.ERROR_ALERT)
