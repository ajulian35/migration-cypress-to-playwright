Feature: REQ-001 Personal Details Validation
  As an authenticated user
  I want to view the Personal Details section of My Info
  So that I can verify employee information is correctly stored

  Background:
    Given I am logged in with valid credentials

  Scenario: Verify personal details fields display correct values
    When I navigate to the Personal Details page
    Then the first name should be "mandaa"
    And the middle name should be "akhill"
    And the last name should be "user"
    And the employee id should be "muser"
    And the other id should be "4957589"
    And the nationality should contain "American"
    And the marital status should contain "Single"
    And the date of birth should be "2023-21-10"
    And the gender should be "Male"
