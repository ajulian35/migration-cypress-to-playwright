import { BasePage } from './BasePage';

export class AddEmployeePage extends BasePage {
  protected url: string = '/web/index.php/pim/addEmployee';

  fillFirstName(name: string): void {
    cy.get('input[name="firstName"]').clear().type(name);
  }

  fillLastName(name: string): void {
    cy.get('input[name="lastName"]').clear().type(name);
  }

  clickSave(): void {
    cy.get('button[type="submit"]').click();
  }
}
