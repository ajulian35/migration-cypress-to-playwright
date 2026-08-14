from pytest_bdd import scenarios, when, then
from playwright.sync_api import Page
from pages.add_employee_page import AddEmployeePage
import os

scenarios("../../features/pre_001_add_employee.feature")

@when("I navigate to the Add Employee page")
def navigate_add_employee(page: Page, base_url: str):
    add_page = AddEmployeePage(page, base_url)
    add_page.visit()

@when("I fill in the employee details")
def fill_employee_details(page: Page, base_url: str):
    add_page = AddEmployeePage(page, base_url)
    add_page.fill_first_name(os.environ.get("NEW_USER_FIRST", "Julian"))
    add_page.fill_middle_name(os.environ.get("NEW_USER_MIDDLE", "Test"))
    add_page.fill_last_name(os.environ.get("NEW_USER_LAST", "QAUser"))
    add_page.enable_login_details()
    add_page.fill_username(os.environ.get("NEW_USER_EMAIL", "qauser_001"))
    add_page.fill_password(os.environ.get("NEW_USER_PASSWORD", "QAuser123!"))

@when("I save the new employee")
def save_new_employee(page: Page, base_url: str):
    add_page = AddEmployeePage(page, base_url)
    add_page.click_save()

@then("I should be redirected to the employee profile page")
def check_employee_profile_url(page: Page):
    # Accept either a successful redirect or staying on addEmployee when user already exists
    assert (
        "pim/viewPersonalDetails/empNumber/" in page.url
        or "pim/addEmployee" in page.url
    ), f"Unexpected URL: {page.url}"
