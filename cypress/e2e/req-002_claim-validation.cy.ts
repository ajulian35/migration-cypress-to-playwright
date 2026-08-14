import { LoginPage } from '../pages/LoginPage';
import { ClaimPage } from '../pages/ClaimPage';

describe('REQ-002: Claim Validation', () => {
  const loginPage = new LoginPage();
  const claimPage = new ClaimPage();

  beforeEach(() => {
    loginPage.visit();
    loginPage.login(
      Cypress.env('NEW_USER_EMAIL'),
      Cypress.env('NEW_USER_PASSWORD')
    );
  });

  it('finds a submitted Medical Reimbursement claim in My Claims', () => {
    claimPage.navigateToMyClaims();
    claimPage.clickSearch();

    claimPage.getResultRows()
      .filter(':contains("Medical Reimbursement")')
      .filter(':contains("Submitted")')
      .should('have.length.greaterThan', 0)
      .first()
      .within(() => {
        cy.contains('Medical Reimbursement').should('be.visible');
        cy.contains('Canadian Dollar').should('be.visible');
        cy.contains('Submitted').should('be.visible');
        cy.contains('1,250.12').should('be.visible');
      });
  });
});
