import { BasePage } from './BasePage';

export class AddEmployeePage extends BasePage {
  protected url: string = '/web/index.php/pim/addEmployee';

  fillFirstName(name: string): void {
    cy.get('input[name="firstName"]').clear().type(name);
  }

  fillMiddleName(name: string): void {
    cy.get('input[name="middleName"]').clear().type(name);
  }

  fillLastName(name: string): void {
    cy.get('input[name="lastName"]').clear().type(name);
  }

  enableLoginDetails(): void {
    cy.get('.oxd-switch-input').click();
    cy.get('.oxd-input-group:contains("Username") input').should('be.visible');
  }

  fillUsername(username: string): void {
    cy.contains('.oxd-input-group', 'Username').find('input').type(username);
  }

  fillPassword(password: string): void {
    cy.get('input[type="password"]').first().type(password);
    cy.get('input[type="password"]').last().type(password);
  }

  clickSave(): void {
    cy.contains('button', 'Save').click();
    // Accept redirect on success OR staying on addEmployee when username already exists
    cy.url().should((url) => {
      expect(
        url.includes('/pim/viewPersonalDetails/empNumber/') ||
        url.includes('/pim/addEmployee')
      ).to.be.true;
    });
  }
}
