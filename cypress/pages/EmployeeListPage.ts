import { BasePage } from './BasePage';

export class EmployeeListPage extends BasePage {
  protected url: string = '/web/index.php/pim/viewEmployeeList';

  searchByName(name: string): void {
    cy.contains('.oxd-input-group', 'Employee Name')
      .find('.oxd-autocomplete-text-input input')
      .clear()
      .type(name);
  }

  clickSearch(): void {
    cy.contains('button', 'Search').click();
  }

  getResultRows(): Cypress.Chainable<JQuery<HTMLElement>> {
    return cy.get('.oxd-table-body .oxd-table-row');
  }
}
