import { LoginPage } from '../pages/LoginPage';
import { EmployeeListPage } from '../pages/EmployeeListPage';

describe('REQ-006: Search Employee', () => {
  const loginPage = new LoginPage();
  const employeeListPage = new EmployeeListPage();

  beforeEach(() => {
    loginPage.visit();
    loginPage.login(
      Cypress.env('NEW_USER_EMAIL'),
      Cypress.env('NEW_USER_PASSWORD')
    );
    employeeListPage.visit();
  });

  it('returns results containing the searched employee name', () => {
    employeeListPage.searchByName(Cypress.env('NEW_USER_FIRST'));
    employeeListPage.clickSearch();

    employeeListPage.getResultRows().should('have.length.greaterThan', 0);
    employeeListPage.getResultRows().should('contain.text', Cypress.env('NEW_USER_FIRST'));
  });
});
