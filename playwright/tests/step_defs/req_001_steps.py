from pytest_bdd import scenarios, when, then
from playwright.sync_api import Page
from pages.my_info_page import MyInfoPage

scenarios("../../features/req_001_personal_details.feature")

@when("I navigate to the Personal Details page")
def navigate_personal_details(page: Page, base_url: str):
    my_info = MyInfoPage(page, base_url)
    my_info.visit()

@then('the first name should be "{expected}"')
def check_first_name(page: Page, base_url: str, expected: str):
    my_info = MyInfoPage(page, base_url)
    assert my_info.get_first_name() == expected

@then('the middle name should be "{expected}"')
def check_middle_name(page: Page, base_url: str, expected: str):
    my_info = MyInfoPage(page, base_url)
    assert my_info.get_middle_name() == expected

@then('the last name should be "{expected}"')
def check_last_name(page: Page, base_url: str, expected: str):
    my_info = MyInfoPage(page, base_url)
    assert my_info.get_last_name() == expected

@then('the employee id should be "{expected}"')
def check_employee_id(page: Page, base_url: str, expected: str):
    my_info = MyInfoPage(page, base_url)
    assert my_info.get_employee_id() == expected

@then('the other id should be "{expected}"')
def check_other_id(page: Page, base_url: str, expected: str):
    my_info = MyInfoPage(page, base_url)
    assert my_info.get_other_id() == expected

@then('the nationality should contain "{expected}"')
def check_nationality(page: Page, base_url: str, expected: str):
    my_info = MyInfoPage(page, base_url)
    assert expected in my_info.get_nationality()

@then('the marital status should contain "{expected}"')
def check_marital_status(page: Page, base_url: str, expected: str):
    my_info = MyInfoPage(page, base_url)
    assert expected in my_info.get_marital_status()

@then('the date of birth should be "{expected}"')
def check_dob(page: Page, base_url: str, expected: str):
    my_info = MyInfoPage(page, base_url)
    assert my_info.get_date_of_birth() == expected

@then('the gender should be "{expected}"')
def check_gender(page: Page, base_url: str, expected: str):
    my_info = MyInfoPage(page, base_url)
    assert expected in my_info.get_gender()
