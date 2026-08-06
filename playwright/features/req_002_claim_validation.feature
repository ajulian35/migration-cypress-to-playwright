Feature: REQ-002 Claim Validation
  As an authenticated user
  I want to filter Employee Claims by event name
  So that I can verify specific claim records

  Background:
    Given I am logged in with valid credentials

  Scenario: Filter claims by Medical Reimbursement and verify record
    When I navigate to Employee Claims
    And I filter by event name "Medical Reimbursement"
    And I click the search button
    Then a claim record with reference id "202307180000002" should be visible
    And the claim employee name should be "mandaa user"
    And the claim event name should be "Medical Reimbursement"
    And the claim currency should be "Canadian Dollar"
    And the claim submitted date should be "2023-18-07"
    And the claim status should be "Submitted"
    And the claim amount should be "1,250.12"
