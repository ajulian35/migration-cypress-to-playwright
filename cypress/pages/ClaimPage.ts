import { BasePage } from './BasePage';

export class ClaimPage extends BasePage {
  protected url: string = '/web/index.php/claim/viewClaimModule';

  navigateToEmployeeClaims(): void {
    cy.visit(this.url);
    cy.contains('.oxd-topbar-body-nav-tab', 'Employee Claims').click();
    cy.contains('button', 'Search').should('be.visible');
  }

  navigateToMyClaims(): void {
    cy.visit(this.url);
    cy.contains('button', 'Search').should('be.visible');
  }

  navigateToSubmitClaim(): void {
    cy.visit('/web/index.php/claim/submitClaim');
  }

  selectEvent(eventName: string): void {
    cy.contains('.oxd-input-group', 'Event').find('.oxd-select-wrapper').click();
    cy.get('[role="listbox"] [role="option"]').contains(eventName).click();
  }

  selectCurrency(currencyName: string): void {
    cy.contains('.oxd-input-group', 'Currency').find('.oxd-select-wrapper').click();
    cy.get('[role="listbox"] [role="option"]').contains(currencyName).click();
  }

  clickCreate(): void {
    cy.contains('button', 'Create').click();
    cy.url().should('include', '/claim/submitClaim/id/');
  }

  addExpense(expenseType: string, date: string, amount: string): void {
    cy.contains('button', 'Add').first().click();
    cy.get('[role="dialog"]').last().within(() => {
      cy.get('.oxd-select-wrapper').click();
    });
    cy.get('[role="listbox"] [role="option"]').contains(expenseType).click();
    cy.get('[role="dialog"]').last().within(() => {
      cy.get('input[placeholder="yyyy-dd-mm"]').type(date);
      cy.get('input').last().clear().type(amount);
      cy.contains('button', 'Save').click();
    });
    cy.contains('.oxd-toast', 'Successfully Saved').should('be.visible');
  }

  clickSubmitClaim(): void {
    cy.contains('button', 'Submit').click();
    cy.get('input[disabled]').should(($inputs) => {
      const values = [...$inputs].map((el) => (el as HTMLInputElement).value);
      expect(values).to.include('Submitted');
    });
  }

  clickSearch(): void {
    cy.contains('button', 'Search').click();
  }

  getResultRows(): Cypress.Chainable<JQuery<HTMLElement>> {
    return cy.get('.oxd-table-body .oxd-table-row');
  }
}
