Feature: PRE-001 Add New Employee
  As an Admin user
  I want to add a new employee through the PIM module
  So that I can create employee records with login access

  Background:
    Given I am logged in as Admin

  Scenario: Successfully add a new employee
    When I navigate to the Add Employee page
    And I fill in the employee details
    And I save the new employee
    Then I should be redirected to the employee profile page
