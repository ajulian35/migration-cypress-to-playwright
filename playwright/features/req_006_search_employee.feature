Feature: REQ-006 Search Employee by Name
  As an admin user
  I want to search for employees by name in the employee list
  So that I can quickly find specific employee records

  Background:
    Given I am logged in with valid credentials

  Scenario: Search employee by name returns matching results
    When I navigate to the Employee List page
    And I search for employee with name "mandaa"
    And I click the search button
    Then the results table should display at least one row
    And the results should contain an employee with name matching "mandaa"
