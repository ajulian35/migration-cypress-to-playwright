from pytest_bdd import scenarios, when, then, parsers
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

scenarios("../../features/req_003_user_login.feature")

@when("I enter valid credentials")
def enter_valid_credentials(page: Page, base_url: str, new_user_credentials: dict):
    login = LoginPage(page, base_url)
    login.fill_username(new_user_credentials["username"])
    login.fill_password(new_user_credentials["password"])

@then("I should be redirected to the dashboard")
def check_dashboard_url(page: Page):
    page.wait_for_url("**/dashboard/index")
    assert "dashboard/index" in page.url

@then(parsers.cfparse('the dashboard heading should display "{expected}"'))
def check_dashboard_heading(page: Page, base_url: str, expected: str):
    dashboard = DashboardPage(page, base_url)
    assert dashboard.page.text_content(dashboard.HEADING) == expected
