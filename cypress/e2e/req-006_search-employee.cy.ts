import { LoginPage } from '../pages/LoginPage';
import { EmployeeListPage } from '../pages/EmployeeListPage';

describe('REQ-006: Search Employee', () => {
  const loginPage = new LoginPage();
  const employeeListPage = new EmployeeListPage();

  beforeEach(() => {
    loginPage.visit();
    loginPage.login(
      Cypress.env('TEST_USER_EMAIL'),
      Cypress.env('TEST_USER_PASSWORD')
    );
    employeeListPage.visit();
  });

  it('returns results containing the searched employee name', () => {
    employeeListPage.searchByName('mandaa');
    cy.get('.oxd-autocomplete-dropdown').should('be.visible');
    cy.get('.oxd-autocomplete-option').first().click();
    employeeListPage.clickSearch();

    employeeListPage.getResultRows().should('have.length.greaterThan', 0);
    employeeListPage.getResultRows().first().should('contain.text', 'mandaa');
  });
});
