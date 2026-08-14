import { LoginPage } from '../pages/LoginPage';
import { MyInfoPage } from '../pages/MyInfoPage';

describe('REQ-001: Personal Details', () => {
  const loginPage = new LoginPage();
  const myInfoPage = new MyInfoPage();

  beforeEach(() => {
    loginPage.visit();
    loginPage.login(
      Cypress.env('NEW_USER_EMAIL'),
      Cypress.env('NEW_USER_PASSWORD')
    );
    myInfoPage.visit();
  });

  it('displays correct personal details for the employee', () => {
    cy.contains('.oxd-text', 'Personal Details').should('be.visible');

    myInfoPage.getFirstName().should('have.value', Cypress.env('NEW_USER_FIRST'));
    myInfoPage.getMiddleName().should('have.value', Cypress.env('NEW_USER_MIDDLE'));
    myInfoPage.getLastName().should('have.value', Cypress.env('NEW_USER_LAST'));
    myInfoPage.getEmployeeId().should('not.have.value', '');
  });
});
