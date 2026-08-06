from pytest_bdd import scenarios, when, then
from playwright.sync_api import Page
from pages.employee_list_page import EmployeeListPage

scenarios("../../features/req_006_search_employee.feature")

@when("I navigate to the Employee List page")
def navigate_employee_list(page: Page, base_url: str):
    emp_list = EmployeeListPage(page, base_url)
    emp_list.visit()

@when('I search for employee with name "{name}"')
def search_employee(page: Page, base_url: str, name: str):
    emp_list = EmployeeListPage(page, base_url)
    emp_list.search_by_name(name)

@when("I click the search button")  # noqa: F811
def click_search_emp(page: Page, base_url: str):
    emp_list = EmployeeListPage(page, base_url)
    emp_list.click_search()

@then("the results table should display at least one row")
def check_results_not_empty(page: Page, base_url: str):
    emp_list = EmployeeListPage(page, base_url)
    assert emp_list.get_result_rows().count() > 0

@then('the results should contain an employee with name matching "{name}"')
def check_result_contains_name(page: Page, base_url: str, name: str):
    emp_list = EmployeeListPage(page, base_url)
    rows = emp_list.get_result_rows()
    found = False
    for i in range(rows.count()):
        if name.lower() in (rows.nth(i).text_content() or "").lower():
            found = True
            break
    assert found, f"No row found containing '{name}'"
