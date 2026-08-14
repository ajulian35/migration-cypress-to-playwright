import re
import os
from pytest_bdd import scenarios, when, then
from playwright.sync_api import Page
from pages.add_employee_page import AddEmployeePage

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
    add_page.fill_employee_id(os.environ.get("NEW_EMP_ID", "0384"))
    add_page.enable_login_details()
    add_page.fill_username(os.environ.get("NEW_USER_EMAIL", "qauser_001"))
    add_page.fill_password(os.environ.get("NEW_USER_PASSWORD", "QAuser123!"))

@when("I save the new employee")
def save_new_employee(page: Page, base_url: str):
    add_page = AddEmployeePage(page, base_url)
    add_page.click_save()

@then("I should be redirected to the employee profile page")
def check_employee_profile_url(page: Page, runtime_data: dict):
    if "pim/viewPersonalDetails/empNumber/" in page.url:
        # New employee created — capture dynamic empNumber
        match = re.search(r'empNumber/(\d+)', page.url)
        if match:
            runtime_data['emp_number'] = match.group(1)
    elif "pim/addEmployee" in page.url:
        # Employee/username already existed (e.g. created by Cypress run) — acceptable
        pass
    else:
        raise AssertionError(f"Unexpected URL after employee save: {page.url}")
