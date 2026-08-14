import { LoginPage } from '../pages/LoginPage';
import { DashboardPage } from '../pages/DashboardPage';

describe('REQ-007: User Logout', () => {
  const loginPage = new LoginPage();
  const dashboardPage = new DashboardPage();

  beforeEach(() => {
    loginPage.visit();
    loginPage.login(
      Cypress.env('NEW_USER_EMAIL'),
      Cypress.env('NEW_USER_PASSWORD')
    );
    dashboardPage.isLoaded();
  });

  it('logs the user out and redirects to the login page', () => {
    cy.get('.oxd-userdropdown-tab').click();
    cy.get('[role="menuitem"]').contains('Logout').click();

    cy.url().should('include', '/auth/login');
  });
});
