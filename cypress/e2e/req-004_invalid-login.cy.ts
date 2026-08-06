import { LoginPage } from '../pages/LoginPage';

describe('REQ-004: Invalid Login', () => {
  const loginPage = new LoginPage();

  beforeEach(() => {
    loginPage.visit();
  });

  it('shows an error message for invalid credentials and stays on login page', () => {
    loginPage.login('wronguser', 'wrongpass');

    cy.get('[role="alert"]').should('be.visible').and('contain.text', 'Invalid credentials');
    cy.url().should('include', '/auth/login');
  });
});
