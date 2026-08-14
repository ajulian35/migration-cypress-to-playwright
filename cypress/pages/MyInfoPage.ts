import { BasePage } from './BasePage';

export class MyInfoPage extends BasePage {
  protected url: string = '/web/index.php/pim/viewMyDetails';

  getFirstName(): Cypress.Chainable<JQuery<HTMLElement>> {
    return cy.get('input[name="firstName"]');
  }

  getMiddleName(): Cypress.Chainable<JQuery<HTMLElement>> {
    return cy.get('input[name="middleName"]');
  }

  getLastName(): Cypress.Chainable<JQuery<HTMLElement>> {
    return cy.get('input[name="lastName"]');
  }

  getEmployeeId(): Cypress.Chainable<JQuery<HTMLElement>> {
    return cy.contains('.oxd-input-group', 'Employee Id').find('input');
  }

  getOtherId(): Cypress.Chainable<JQuery<HTMLElement>> {
    return cy.contains('.oxd-input-group', 'Other Id').find('input');
  }

  getNationality(): Cypress.Chainable<JQuery<HTMLElement>> {
    return cy.contains('.oxd-input-group', 'Nationality').find('.oxd-select-text-input');
  }

  getMaritalStatus(): Cypress.Chainable<JQuery<HTMLElement>> {
    return cy.contains('.oxd-input-group', 'Marital Status').find('.oxd-select-text-input');
  }

  getDateOfBirth(): Cypress.Chainable<JQuery<HTMLElement>> {
    return cy.contains('.oxd-input-group', 'Date of Birth').find('input');
  }

  getGenderValue(): Cypress.Chainable<JQuery<HTMLElement>> {
    return cy.get('.oxd-radio-input:checked').closest('.oxd-radio-wrapper').find('span');
  }
}
