import { defineConfig } from 'cypress';
import * as dotenv from 'dotenv';

dotenv.config();

export default defineConfig({
  e2e: {
    baseUrl: process.env.BASE_URL || 'https://opensource-demo.orangehrmlive.com',
    env: {
      TEST_USER_EMAIL: process.env.TEST_USER_EMAIL,
      TEST_USER_PASSWORD: process.env.TEST_USER_PASSWORD,
      NEW_USER_EMAIL: process.env.NEW_USER_EMAIL,
      NEW_USER_PASSWORD: process.env.NEW_USER_PASSWORD,
      NEW_USER_FIRST: process.env.NEW_USER_FIRST,
      NEW_USER_MIDDLE: process.env.NEW_USER_MIDDLE,
      NEW_USER_LAST: process.env.NEW_USER_LAST,
      NEW_EMP_NUMBER: process.env.NEW_EMP_NUMBER,
      NEW_EMP_ID: process.env.NEW_EMP_ID,
      CLAIM_REF_ID: process.env.CLAIM_REF_ID,
    },
    specPattern: [
      'cypress/e2e/pre-001_add-employee.cy.ts',
      'cypress/e2e/pre-002_create-claim.cy.ts',
      'cypress/e2e/req-003_user-login.cy.ts',
      'cypress/e2e/req-004_invalid-login.cy.ts',
      'cypress/e2e/req-001_personal-details.cy.ts',
      'cypress/e2e/req-002_claim-validation.cy.ts',
      'cypress/e2e/req-006_search-employee.cy.ts',
      'cypress/e2e/req-007_user-logout.cy.ts',
    ],
    supportFile: 'cypress/support/e2e.ts',
    fixturesFolder: 'cypress/fixtures',
    screenshotsFolder: 'reports/cypress/screenshots',
    videosFolder: 'reports/cypress/videos',
    reporter: 'mochawesome',
    reporterOptions: {
      reportDir: 'reports/cypress',
      overwrite: false,
      html: true,
      json: true,
    },
    viewportWidth: 1280,
    viewportHeight: 720,
    defaultCommandTimeout: 8000,
    requestTimeout: 10000,
  },
});
