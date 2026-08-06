Feature: REQ-003 User Login with Valid Credentials
  As a registered user
  I want to log in with valid credentials
  So that I can access the dashboard

  Scenario: Successful login redirects to Dashboard
    Given I am on the login page
    When I enter valid credentials
    And I click the login button
    Then I should be redirected to the dashboard
    And the dashboard heading should display "Dashboard"
