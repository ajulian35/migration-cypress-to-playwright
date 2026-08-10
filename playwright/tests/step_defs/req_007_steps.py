from pytest_bdd import scenarios, when, then
from playwright.sync_api import Page

scenarios("../../features/req_007_user_logout.feature")

@when("I click on the user profile menu")
def click_profile_menu(page: Page):
    page.locator(".oxd-userdropdown-tab").click()

@when("I click the logout option")
def click_logout(page: Page):
    page.get_by_role("menuitem", name="Logout").click()

@then("I should be redirected to the login page")
def check_login_page(page: Page):
    page.wait_for_url("**/auth/login")
    assert "/auth/login" in page.url
