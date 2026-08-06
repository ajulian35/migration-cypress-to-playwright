import { LoginPage } from '../pages/LoginPage';
import { ClaimPage } from '../pages/ClaimPage';

describe('REQ-002: Claim Validation', () => {
  const loginPage = new LoginPage();
  const claimPage = new ClaimPage();

  beforeEach(() => {
    loginPage.visit();
    loginPage.login(
      Cypress.env('TEST_USER_EMAIL'),
      Cypress.env('TEST_USER_PASSWORD')
    );
  });

  it('finds the Medical Reimbursement claim with correct details', () => {
    claimPage.navigateToEmployeeClaims();
    claimPage.selectEventName('Medical Reimbursement');
    claimPage.clickSearch();

    cy.contains('.oxd-table-body .oxd-table-row', '202307180000002').within(() => {
      cy.contains('mandaa user').should('be.visible');
      cy.contains('Medical Reimbursement').should('be.visible');
      cy.contains('Canadian Dollar').should('be.visible');
      cy.contains('2023-18-07').should('be.visible');
      cy.contains('Submitted').should('be.visible');
      cy.contains('1,250.12').should('be.visible');
    });
  });
});
