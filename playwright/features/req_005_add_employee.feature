Feature: REQ-005 Add New Employee
  As an admin user
  I want to add a new employee through the PIM module
  So that I can create employee records

  Background:
    Given I am logged in with valid credentials

  Scenario: Successfully add a new employee
    When I navigate to the Add Employee page
    And I fill in the employee first name and last name
    And I save the new employee
    Then I should be redirected to the employee profile page
