
# Migration_cypress_to_Playwright


## Project Steps

Steps
1. Initialize the Project
	* Create a new project and generate the claude.md file using the /init command.
2. Set Up the Cypress Framework
	* Create the project structure for a Cypress automation framework using TypeScript.
3. Define Project Requirements
	* Gather and document the project requirements.
	* Define a minimum of three functional requirements.
4. Create an Agent for Cypress Test Automation
	* Generate test cases based on the defined requirements.
	* Generate the steps for navigate in the APP
	* Execute the test scenarios using MCP Playwright.
	* Generate the corresponding TypeScript test automation code.
	* Execute the generated scripts within the Cypress framework.
	* Collect, analyze, and present the test execution results.
5. Set Up the Playwright Framework
	* Create the project structure for a Playwright automation framework using Python.
6. Create an Agent for Test Migration from Cypress to Playwright
	* Generate test cases from the requirements using Gherkin syntax / Cucumber BDD.
	* Convert or generate the corresponding Python automation code for Playwright.
	* Use structure POM (Page Object Model)
	* Execute the generated scripts within the Playwright framework.
	* Collect, analyze, and present the test execution results.


## Expected Deliverables
Expected Deliverables
	* Cypress framework structure (TypeScript)
	* Playwright framework structure (Python)
	* Requirements specification document
	* Generated test cases
	* Gherkin scenarios
	* Cypress automation scripts
	* Playwright automation scripts
	* Test execution reports and results
	* Migration workflow from Cypress to Playwright


## Notes
Notes:
	* Use .env for sensible data
	* create and use prompt each stage.
    
## User Requirements
 [001] - Personal Details Validation
 Verify the information displayed in the "Personal Details" section. The following fields must be validated:
	* Employee Full Name
	* Employee ID
	* Other ID
	* Nationality
	* Marital Status
	* Date of Birth
	* Gender
[002] - Claim Validation
 Verify the information available in the "Claim" section. Validate the "Event Name" filter using the value "Medical Reimbursement".

##   Steps:
[001] - Validate Personal Details Information
	* Launch the application.
	* Log in with valid credentials.
	* Navigate to My Info.
	* Open Personal Details.
	* Verify that the following information is displayed correctly:
        ** "Employee Full name": Testing, Name, Employee
        ** "Employee Id": muser
        ** "Other Id": 4957589
        ** "Nationality": Indian
        ** "Marital Status": Married
        ** "Date of Birth": 1995-01-08
        ** "Gender": Male
	
[002] - Validate Employee Claim Information
	* Launch the application.
	* Log in with valid credentials.
	* Navigate to Claim.
	* Open Employee Claims.
	* In the Event Name filter, select Medical Reimbursement.
	* Click Search.
	* Verify that the following claim details are displayed:
        ** "Reference Id": 202307180000002
        ** "Employee Name": manda user
        ** "Event Name": Medical Reimbursement
        ** "Currency": Canadian Dollar
        ** "Submitted Date": 2023-18-07
        ** "Status": Submitted
        ** "Amount": 1,250.12