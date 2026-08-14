import { LoginPage } from '../pages/LoginPage';
import { DashboardPage } from '../pages/DashboardPage';

describe('REQ-003: User Login (Valid Credentials)', () => {
  const loginPage = new LoginPage();
  const dashboardPage = new DashboardPage();

  beforeEach(() => {
    loginPage.visit();
  });

  it('should redirect to Dashboard after login with valid credentials', () => {
    loginPage.login(
      Cypress.env('NEW_USER_EMAIL'),
      Cypress.env('NEW_USER_PASSWORD')
    );

    cy.url().should('include', '/dashboard/index');
    dashboardPage.isLoaded();
  });
});
