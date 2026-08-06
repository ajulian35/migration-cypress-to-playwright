Feature: REQ-007 User Logout
  As an authenticated user
  I want to log out of the application
  So that my session is securely terminated

  Background:
    Given I am logged in with valid credentials

  Scenario: User can successfully log out
    When I click on the user profile menu
    And I click the logout option
    Then I should be redirected to the login page
