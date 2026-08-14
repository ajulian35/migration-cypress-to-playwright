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

  fillEmployeeId(id: string): void {
    cy.contains('.oxd-input-group', 'Employee Id').find('input').clear().type(id);
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
    cy.url().should('include', '/pim/viewPersonalDetails/empNumber/');
    cy.url().then((url) => {
      const match = url.match(/empNumber\/(\d+)/);
      if (match) {
        cy.task('setRuntimeValue', { key: 'empNumber', value: match[1] });
      }
    });
  }
}
