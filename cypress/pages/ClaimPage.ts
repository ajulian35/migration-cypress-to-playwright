import { BasePage } from './BasePage';

export class ClaimPage extends BasePage {
  protected url: string = '/web/index.php/claim/viewEmployeeClaims';

  navigateToEmployeeClaims(): void {
    cy.contains('.oxd-topbar-body-nav-tab', 'Claim').trigger('mouseover');
    cy.contains('.oxd-topbar-body-nav-tab', 'Employee Claims').click();
  }

  selectEventName(name: string): void {
    cy.contains('.oxd-input-group', 'Event Name').find('.oxd-select-text').click();
    cy.get('.oxd-select-dropdown').should('be.visible').contains(name).click();
  }

  clickSearch(): void {
    cy.contains('button', 'Search').click();
  }

  getResultRows(): Cypress.Chainable<JQuery<HTMLElement>> {
    return cy.get('.oxd-table-body .oxd-table-row');
  }
}
