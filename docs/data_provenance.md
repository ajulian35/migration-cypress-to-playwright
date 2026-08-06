# Data Provenance

## Source

All test data originates from the OrangeHRM open-source demo instance at:
**https://opensource-demo.orangehrmlive.com**

This is a publicly hosted demo environment maintained by OrangeHRM Inc. for evaluation and demonstration purposes. Access credentials (`Admin` / `admin123`) are displayed directly on the login page and are publicly known by design. No private credentials were used or stored.

## What the Data Represents

The demo instance contains pre-seeded HR records including employee profiles, personal details, PIM module entries, and claims records. This data is synthetic — it exists to demonstrate application functionality and does not correspond to any real individuals or organizations.

## What It Does NOT Represent

- Real employee personally identifiable information (PII)
- Production HR system data from any organization
- A representative sample of enterprise HR data complexity, volume, or schema variation

The data should not be treated as a benchmark for real-world HR data quality or completeness.

## Known Limitations

The demo instance is a shared public environment. Any authenticated user can modify records at any time. This introduces state drift between when requirements were originally written and when the agent explored the application.

Concretely: the personal details record for the `Admin` user (REQ-001) had been modified by a prior user before exploration. Field values for first name, nationality, marital status, and date of birth differed from those specified in the original requirements document. The generated tests assert the values observed during the agent's live exploration session, not the originally specified values. If another user modifies these records again, assertions in those tests will fail until updated.

All other module tests (claims, PIM, logout) are written around actions and navigation flows, which are less susceptible to data drift than field-value assertions.

## Sensitive Data Handling

- No real credentials or PII appear anywhere in the codebase.
- The `.env` file containing environment variables is excluded from version control via `.gitignore`.
- The only credentials referenced are the public demo credentials, which are intentionally published by OrangeHRM on the login page.
- All tests target the public demo instance only; no internal or client systems were accessed.
