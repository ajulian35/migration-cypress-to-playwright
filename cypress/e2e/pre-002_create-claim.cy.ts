import { LoginPage } from '../pages/LoginPage';
import { ClaimPage } from '../pages/ClaimPage';

describe('PRE-002: Create Claim', () => {
  const loginPage = new LoginPage();
  const claimPage = new ClaimPage();

  beforeEach(() => {
    loginPage.visit();
    loginPage.login(
      Cypress.env('NEW_USER_EMAIL'),
      Cypress.env('NEW_USER_PASSWORD')
    );
  });

  it('creates a Medical Reimbursement claim and submits it', () => {
    claimPage.navigateToSubmitClaim();
    claimPage.selectEvent('Medical Reimbursement');
    claimPage.selectCurrency('Canadian Dollar');
    claimPage.clickCreate();
    claimPage.addExpense('Accommodation', '2026-08-06', '1250.12');
    claimPage.clickSubmitClaim();
  });
});
