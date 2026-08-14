import { LoginPage } from '../pages/LoginPage';
import { AddEmployeePage } from '../pages/AddEmployeePage';

describe('PRE-001: Add Employee', () => {
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

  it('adds a new employee with login details and redirects to the personal details page', () => {
    addEmployeePage.fillFirstName(Cypress.env('NEW_USER_FIRST'));
    addEmployeePage.fillMiddleName(Cypress.env('NEW_USER_MIDDLE'));
    addEmployeePage.fillLastName(Cypress.env('NEW_USER_LAST'));
    addEmployeePage.fillEmployeeId(Cypress.env('NEW_EMP_ID'));
    addEmployeePage.enableLoginDetails();
    addEmployeePage.fillUsername(Cypress.env('NEW_USER_EMAIL'));
    addEmployeePage.fillPassword(Cypress.env('NEW_USER_PASSWORD'));
    addEmployeePage.clickSave();
  });
});
