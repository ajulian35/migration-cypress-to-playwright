from pytest_bdd import scenarios, when, then, parsers
from playwright.sync_api import Page
from pages.employee_list_page import EmployeeListPage

scenarios("../../features/req_006_search_employee.feature")

@when("I navigate to the Employee List page")
def navigate_employee_list(page: Page, base_url: str):
    emp_list = EmployeeListPage(page, base_url)
    emp_list.visit()

@when(parsers.cfparse('I search for employee with name "{name}"'))
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

@then(parsers.cfparse('the results should contain an employee with name matching "{name}"'))
def check_result_contains_name(page: Page, base_url: str, name: str):
    matching = page.locator('.orangehrm-directory-card').filter(has_text=name)
    assert matching.count() > 0, f"No directory card found containing '{name}'"
