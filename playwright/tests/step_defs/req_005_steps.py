import time
from pytest_bdd import scenarios, when, then
from playwright.sync_api import Page
from pages.add_employee_page import AddEmployeePage

scenarios("../../features/req_005_add_employee.feature")

@when("I navigate to the Add Employee page")
def navigate_add_employee(page: Page, base_url: str):
    add_page = AddEmployeePage(page, base_url)
    add_page.visit()

@when("I fill in the employee first name and last name")
def fill_employee_name(page: Page, base_url: str):
    ts = str(int(time.time()))
    add_page = AddEmployeePage(page, base_url)
    add_page.fill_first_name(f"Test{ts}")
    add_page.fill_last_name(f"Playwright{ts}")

@when("I save the new employee")
def save_new_employee(page: Page, base_url: str):
    add_page = AddEmployeePage(page, base_url)
    add_page.click_save()

@then("I should be redirected to the employee profile page")
def check_employee_profile_url(page: Page):
    assert "pim/viewPersonalDetails/empNumber/" in page.url
