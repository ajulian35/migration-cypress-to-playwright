import { BasePage } from './BasePage';

export class EmployeeListPage extends BasePage {
  protected url: string = '/web/index.php/directory/viewDirectory';

  searchByName(name: string): void {
    cy.get('input[placeholder="Type for hints..."]').clear().type(name);
    // Wait for autocomplete dropdown then select the first matching option
    cy.get('[role="listbox"] [role="option"]').first().click();
  }

  clickSearch(): void {
    cy.contains('button', 'Search').click();
    cy.get('.orangehrm-directory-card', { timeout: 10000 }).should('exist');
  }

  getResultRows(): Cypress.Chainable<JQuery<HTMLElement>> {
    return cy.get('.orangehrm-directory-card');
  }
}
