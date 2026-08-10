Feature: REQ-001 Personal Details Validation
  As an authenticated user
  I want to view the Personal Details section of My Info
  So that I can verify my employee information is correctly stored

  Background:
    Given I am logged in with valid credentials

  Scenario: Verify personal details fields display correct values
    When I navigate to the Personal Details page
    Then the first name should be "Julian"
    And the middle name should be "Test"
    And the last name should be "QAUser"
    And the employee id field should not be empty
