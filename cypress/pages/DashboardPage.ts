import { BasePage } from './BasePage';

export class DashboardPage extends BasePage {
  protected url: string = '/web/index.php/dashboard/index';

  private readonly dashboardHeading = 'h6.oxd-topbar-header-breadcrumb-module';

  getDashboardHeading(): Cypress.Chainable<JQuery<HTMLElement>> {
    return cy.get(this.dashboardHeading);
  }

  isLoaded(): void {
    cy.url().should('include', '/dashboard/index');
    this.getDashboardHeading().should('contain.text', 'Dashboard');
  }
}
