import { LoginPage } from '../pages/LoginPage';
import { MyInfoPage } from '../pages/MyInfoPage';

describe('REQ-001: Personal Details', () => {
  const loginPage = new LoginPage();
  const myInfoPage = new MyInfoPage();

  beforeEach(() => {
    loginPage.visit();
    loginPage.login(
      Cypress.env('TEST_USER_EMAIL'),
      Cypress.env('TEST_USER_PASSWORD')
    );
    myInfoPage.visit();
  });

  it('displays correct personal details for the employee', () => {
    cy.contains('h6', 'PIM').should('be.visible');
    cy.contains('.oxd-text', 'Personal Details').should('be.visible');

    myInfoPage.getFirstName().should('have.value', 'mandaa');
    myInfoPage.getMiddleName().should('have.value', 'akhill');
    myInfoPage.getLastName().should('have.value', 'user');
    myInfoPage.getEmployeeId().should('have.value', 'muser');
    myInfoPage.getOtherId().should('have.value', '4957589');
    myInfoPage.getNationality().should('contain.text', 'American');
    myInfoPage.getMaritalStatus().should('contain.text', 'Single');
    myInfoPage.getDateOfBirth().should('have.value', '2023-21-10');
    myInfoPage.getGenderValue().should('contain.text', 'Male');
  });
});
