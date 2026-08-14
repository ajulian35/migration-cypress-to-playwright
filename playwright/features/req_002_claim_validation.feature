Feature: REQ-002 Claim Validation
  As a new employee user
  I want to view my submitted claims in My Claims
  So that I can verify specific claim records

  Background:
    Given I am logged in with valid credentials

  Scenario: Verify a submitted Medical Reimbursement claim exists in My Claims
    When I navigate to My Claims
    And I click the search button
    Then a submitted claim with event "Medical Reimbursement" should be visible
    And the claim currency should show "Canadian Dollar"
    And the claim amount should show "1,250.12"
