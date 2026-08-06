from pytest_bdd import scenarios, when, then
from playwright.sync_api import Page
from pages.login_page import LoginPage

scenarios("../../features/req_004_invalid_login.feature")

@when("I enter invalid credentials")
def enter_invalid_credentials(page: Page, base_url: str):
    login = LoginPage(page, base_url)
    login.fill_username("wronguser")
    login.fill_password("wrongpass")

@then('an error message "{expected}" should be displayed')
def check_error_message(page: Page, base_url: str, expected: str):
    login = LoginPage(page, base_url)
    assert expected in login.get_error_message()

@then("I should remain on the login page")
def check_still_on_login(page: Page):
    assert "/auth/login" in page.url
