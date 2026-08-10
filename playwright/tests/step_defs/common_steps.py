from pytest_bdd import given, when
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

@given("I am logged in with valid credentials")
def logged_in(page: Page, base_url: str, new_user_credentials: dict):
    login = LoginPage(page, base_url)
    login.visit()
    login.login(new_user_credentials["username"], new_user_credentials["password"])
    dashboard = DashboardPage(page, base_url)
    dashboard.is_loaded()

@given("I am logged in as Admin")
def logged_in_as_admin(page: Page, base_url: str, credentials: dict):
    login = LoginPage(page, base_url)
    login.visit()
    login.login(credentials["username"], credentials["password"])
    dashboard = DashboardPage(page, base_url)
    dashboard.is_loaded()

@given("I am on the login page")
def on_login_page(page: Page, base_url: str):
    login = LoginPage(page, base_url)
    login.visit()

@when("I click the login button")
def click_login_button(page: Page, base_url: str):
    login = LoginPage(page, base_url)
    login.click_login()
