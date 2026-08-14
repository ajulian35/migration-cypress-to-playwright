# Functional Requirements — OrangeHRM

**Application:** OrangeHRM Demo  
**URL:** .env.BASE_URL
**Credentials:** .env.TEST_USER_EMAIL / .env.TEST_USER_PASSWORD

---

## REQ-001: Personal Details Validation

**Description:** Verify the information displayed in the "Personal Details" section of My Info.

**Preconditions:** User is logged in with valid credentials.

**Steps:**
1. Launch the application.
2. Log in as the test employee created in PRE-001 (`qauser_001`).
3. Navigate to My Info > Personal Details.
4. Verify the following fields are displayed correctly:

| Field | Expected Value |
|---|---|
| First Name | Julian |
| Middle Name | Test |
| Last Name | QAUser |
| Employee ID | non-empty (value assigned by OrangeHRM at creation time) |

> **Note:** Nationality, Marital Status, and Date of Birth are not verified by the automated test. The test user (`qauser_001`) is created fresh by PRE-001 each session and those optional fields are not populated during employee creation. The original spec referenced a pre-existing demo user (`muser`) whose data drifted; values have been updated to reflect the current test user.

**Expected Result:** Name fields and Employee ID match the values set during PRE-001 employee creation.

---

## REQ-002: Claim Validation

**Description:** Verify the information available in the "Claim" section. Validate the "Event Name" filter using the value "Medical Reimbursement".

**Preconditions:** User is logged in with valid credentials.

**Steps:**
1. Launch the application.
2. Log in with valid credentials.
3. Navigate to Claim > Employee Claims.
4. In the Event Name filter, select "Medical Reimbursement".
5. Click Search.
6. Verify the following claim details are displayed:

| Field | Expected Value |
|---|---|
| Reference ID | 202307180000002 |
| Employee Name | manda user |
| Event Name | Medical Reimbursement |
| Currency | Canadian Dollar |
| Submitted Date | 2023-18-07 |
| Status | Submitted |
| Amount | 1,250.12 |

**Expected Result:** The claim record matches all expected field values.

---

## REQ-003: User Login (Valid Credentials)

**Description:** The system must allow a user with valid credentials to log in and access the dashboard.

**Preconditions:** User is on the login page.

**Steps:**
1. Enter a valid username.
2. Enter a valid password.
3. Click the Login button.

**Expected Result:** User is redirected to the dashboard and the page title contains "Dashboard".

---

## REQ-004: Invalid Login Shows Error Message

**Description:** The system must display an error message when invalid credentials are entered.

**Preconditions:** User is on the login page.

**Steps:**
1. Enter an invalid username or password.
2. Click the Login button.

**Expected Result:** An error message is displayed ("Invalid credentials") and the user remains on the login page.

---

## REQ-005: Add New Employee

**Description:** An authenticated admin user must be able to add a new employee via the PIM module.

**Preconditions:** User is logged in as Admin.

**Steps:**
1. Navigate to PIM > Add Employee.
2. Enter First Name and Last Name.
3. Click Save.

**Expected Result:** The new employee record is created and the employee profile page is displayed.

---

## REQ-006: Search Employee by Name

**Description:** An authenticated admin user must be able to search for an employee by name in the employee list.

**Preconditions:** User is logged in and at least one employee exists.

**Steps:**
1. Navigate to PIM > Employee List.
2. Enter the employee's first or last name in the search field.
3. Click Search.

**Expected Result:** The results table displays only employees matching the search term.

---

## REQ-007: User Logout

**Description:** An authenticated user must be able to log out of the application.

**Preconditions:** User is logged in.

**Steps:**
1. Click on the user menu (top right).
2. Click Logout.

**Expected Result:** User is redirected to the login page.
