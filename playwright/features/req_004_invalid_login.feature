Feature: REQ-004 Invalid Login Shows Error Message
  As a user
  I want to see an error message when I enter wrong credentials
  So that I know the login failed

  Scenario: Invalid credentials show error message
    Given I am on the login page
    When I enter invalid credentials
    And I click the login button
    Then an error message "Invalid credentials" should be displayed
    And I should remain on the login page
