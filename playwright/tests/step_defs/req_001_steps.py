from pytest_bdd import scenarios, when, then, parsers
from playwright.sync_api import Page
from pages.my_info_page import MyInfoPage

scenarios("../../features/req_001_personal_details.feature")

@when("I navigate to the Personal Details page")
def navigate_personal_details(page: Page, base_url: str):
    my_info = MyInfoPage(page, base_url)
    my_info.visit()
    page.wait_for_load_state("networkidle")

@then(parsers.cfparse('the first name should be "{expected}"'))
def check_first_name(page: Page, base_url: str, expected: str):
    my_info = MyInfoPage(page, base_url)
    assert my_info.get_first_name() == expected

@then(parsers.cfparse('the middle name should be "{expected}"'))
def check_middle_name(page: Page, base_url: str, expected: str):
    my_info = MyInfoPage(page, base_url)
    assert my_info.get_middle_name() == expected

@then(parsers.cfparse('the last name should be "{expected}"'))
def check_last_name(page: Page, base_url: str, expected: str):
    my_info = MyInfoPage(page, base_url)
    assert my_info.get_last_name() == expected

@then(parsers.cfparse('the employee id should be "{expected}"'))
def check_employee_id(page: Page, base_url: str, expected: str):
    my_info = MyInfoPage(page, base_url)
    assert my_info.get_employee_id() == expected

@then("the employee id field should not be empty")
def check_employee_id_not_empty(page: Page, base_url: str):
    my_info = MyInfoPage(page, base_url)
    emp_id = my_info.get_employee_id()
    assert emp_id and emp_id.strip() != "", f"Employee ID field is empty: '{emp_id}'"

@then(parsers.cfparse('the nationality should contain "{expected}"'))
def check_nationality(page: Page, base_url: str, expected: str):
    my_info = MyInfoPage(page, base_url)
    assert expected in my_info.get_nationality()

@then(parsers.cfparse('the marital status should contain "{expected}"'))
def check_marital_status(page: Page, base_url: str, expected: str):
    my_info = MyInfoPage(page, base_url)
    assert expected in my_info.get_marital_status()

@then(parsers.cfparse('the date of birth should be "{expected}"'))
def check_dob(page: Page, base_url: str, expected: str):
    my_info = MyInfoPage(page, base_url)
    assert my_info.get_date_of_birth() == expected
