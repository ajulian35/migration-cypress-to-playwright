Feature: PRE-002 Create Claim
  As a new employee user
  I want to create and submit a Medical Reimbursement claim
  So that the claim is available for validation in REQ-002

  Background:
    Given I am logged in with valid credentials

  Scenario: Create and submit a Medical Reimbursement claim
    When I navigate to the Submit Claim page
    And I select the event "Medical Reimbursement"
    And I select the currency "Canadian Dollar"
    And I create the claim
    And I add an expense of "1250.12"
    And I submit the claim
    Then the claim status should show "Submitted"
