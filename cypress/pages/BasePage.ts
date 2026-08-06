export abstract class BasePage {
  protected url: string = '';

  visit(): void {
    cy.visit(this.url);
  }

  getTitle(): Cypress.Chainable<string> {
    return cy.title();
  }
}
