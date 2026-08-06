import { BasePage } from './BasePage';

export class LoginPage extends BasePage {
  protected url: string = '/web/index.php/auth/login';

  private readonly usernameInput = 'input[name="username"]';
  private readonly passwordInput = 'input[name="password"]';
  private readonly loginButton = 'button[type="submit"]';
  private readonly errorAlert = '.oxd-alert-content-text';

  fillUsername(username: string): void {
    cy.get(this.usernameInput).clear().type(username);
  }

  fillPassword(password: string): void {
    cy.get(this.passwordInput).clear().type(password);
  }

  clickLogin(): void {
    cy.get(this.loginButton).click();
  }

  login(username: string, password: string): void {
    this.fillUsername(username);
    this.fillPassword(password);
    this.clickLogin();
  }

  getErrorMessage(): Cypress.Chainable<JQuery<HTMLElement>> {
    return cy.get(this.errorAlert);
  }
}
