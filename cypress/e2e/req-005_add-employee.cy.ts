import { LoginPage } from '../pages/LoginPage';
import { AddEmployeePage } from '../pages/AddEmployeePage';

describe('REQ-005: Add Employee', () => {
  const loginPage = new LoginPage();
  const addEmployeePage = new AddEmployeePage();

  beforeEach(() => {
    loginPage.visit();
    loginPage.login(
      Cypress.env('TEST_USER_EMAIL'),
      Cypress.env('TEST_USER_PASSWORD')
    );
    addEmployeePage.visit();
  });

  it('adds a new employee and redirects to the personal details page', () => {
    const suffix = Date.now();
    addEmployeePage.fillFirstName(`Test${suffix}`);
    addEmployeePage.fillLastName(`Cypress${suffix}`);
    addEmployeePage.clickSave();

    cy.url().should('include', '/pim/viewPersonalDetails/empNumber/');
  });
});
