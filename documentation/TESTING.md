# Testing
----------

Here you will find all tests performed on the Regulate site.

Return to [README.md](../README.md)

----------
## Contents
----------

1. [Test User Accounts](#test-user-accounts)
2. [Manual Testing](#manual-testing)
    - [CSS Validation](#css-validation)
    - [HTML Validation](#html-validation)
        - [HTML Summary](#html-summary)
        - [HTML Full Details](#html-full-details-collapsible)
    - [JavaScript Validation](#javascript-validation)
        - [JS Summary](#js-summary)
        - [JS Full Details](#js-full-details-collapsible)
    - [Lighthouse Testing](#lighthouse-testing)
        - [Desktop Results](#desktop-results)
        - [Mobile Results](#mobile-results)
    - [Responsive Testing](#responsive-testing)
    - [Browser Compatibility Testing](#browser-compatibility-testing)
    - [User Story Testing](#user-story-testing)
    - [Feature Interaction Testing](#feature-interaction-testing)
        - [Feature Interaction Summary](#feature-interaction-summary) 
        - [Feature Interaction Full Details](#feature-interaction-full-details-collapsible)
    - [Admin Area Security Testing](#admin-area-security-testing)
    - [Error Handling](#error-handling)
    - [Security Testing](#security-testing)
3. [Automated Testing](#automated-testing)
    - [Running Tests](#running-tests)
    - [Test Structure](#test-structure)
    - [Plan & Subscription Behaviour](#plan--subscription-behaviour)
    - [Free Plan Limits (Business Logic)](#free-plan-limits-business-logic)
    - [Permissions & Security](#permissions--security)
    - [Test-Driven Development Evidence](#test-driven-development-evidence)
    - [Summary](#summary)
    - [Technical Note](#technical-note)
    - [Test Output Log](#test-output-log)
4. [Initial Heroku Deployment Test](#initial-heroku-deployment-test)    
5. [Final Deployment Checks](#final-deployment-checks)

Return to [README.md](../README.md)

---
## Test User Accounts
---

To allow the assessors to fully explore the site, the following **dummy accounts** have been created for testing purposes only.  
These accounts contain no personal data and can be safely shared.

### <u>Admin Dashboard Access:</u>

#### Superuser Account (Full Django Admin Access)
```text
For security reasons, the superuser login details are not included in the repository.  
They have been submitted separately through the Peterborough University Dashboard
under the “submission comment” section.
```

#### Admin Staff Account (Restricted Admin Permissions - view only)
```text
Username: TestAdminviewonly  
Email: testadminviewonly@testuser.com  
Password: Password54321
```

### <u>Regulate main site access</u>

#### Standard Site User 1 (Regular User Account - Free plan)
```text
Username: TestSiteUser1  
Email: testsiteuser1@testuser.com
Password: Password98765
```

#### Standard Site User 2 (Regular User Account - Free Trial)
```text
Username: TestSiteUser2  
Email: testsiteuser2@testuser.com
Password: Password99999
```

#### Standard Site User 3 (Regular User Account - Full subscription)
```text
Username: TestSiteUser3  
Email: testsiteuser3@testuser.com
Password: Password88888
```

[Back to contents](#contents)

Return to [README.md](../README.md)

---
## Manual Testing
---

*(To be completed – manual test cases, screenshots, and validation results will be added here.)*

[Back to contents](#contents)

Return to [README.md](../README.md)

---
---

## Automated Testing

To improve reliability, maintainability, and overall code quality, automated tests were implemented using Django’s built-in testing framework (`django.test.TestCase`).

These tests validate:

- Subscription plan detection and banner rendering
- Free plan entry limits and gating logic
- Authentication requirements
- User ownership and permission controls
- Core business rules independent of the UI

Where appropriate, tests simulate real user behaviour by sending HTTP requests to views rather than testing isolated functions. This ensures templates, context processors, and permissions all work together correctly.

[Back to contents](#contents)

Return to [README.md](../README.md)

---

### Running Tests

From the project root:

```bash
python manage.py test -v 3
```

Example successful output:

```text
Ran 16 tests in 9.945s
OK
```

[Back to contents](#contents)

Return to [README.md](../README.md)

---

### Test Structure

Tests are organised per app following Django best practices:

```text
core/tests/
    test_plan_status.py
    test_limits.py
    test_permissions.py
    test_revision_creation.py
    test_delete_unlocks.py
```

This keeps related logic grouped and improves readability and maintainability.

[Back to contents](#contents)

Return to [README.md](../README.md)

---

### Plan & Subscription Behaviour

These tests ensure the correct account banner is displayed depending on the user’s subscription status.

| Test Case | Purpose | Result |
|-----------|---------------------------------------------|-----------|
| Free user shows Free plan banner | Default experience without subscription | Passed |
| Trialing status shows trial banner | Stripe `trialing` state recognised | Passed |
| Future `trial_end` shows trial banner | Date-based trial detection | Passed |
| Active subscription shows plus banner | Paid plan recognised correctly | Passed |
| Cancelled but period active shows ending soon | Grace-period messaging works | Passed |

[Back to contents](#contents)

Return to [README.md](../README.md)

---

### Free Plan Limits (Business Logic)

These tests validate the entry limit rules enforced in `core/limits.py`.

| Test Case | Purpose | Result |
|-----------|----------------------------------|-----------|
| Below limit not locked | User can continue posting | Passed |
| At limit locked | Posting correctly restricted | Passed |
| Active subscription never locked | Paid users unrestricted | Passed |
| Trialing user never locked | Trial users unrestricted | Passed |
| Future `trial_end` never locked | Treat future trial as paid access | Passed |

[Back to contents](#contents)

Return to [README.md](../README.md)

---

### Permissions & Security

These tests ensure correct access control and data isolation.

| Test Case | Purpose | Result |
|-----------|--------------------------------------|-----------|
| Dashboard requires login | Anonymous users redirected | Passed |
| Cannot view another user’s entry | Data privacy enforced | Passed |
| Cannot edit another user’s entry | Ownership enforced | Passed |
| Cannot delete another user’s entry | Ownership enforced | Passed |

[Back to contents](#contents)

Return to [README.md](../README.md)

---

### Test-Driven Development Evidence

For selected business rules, a test-first workflow was used. This is evidenced in Git commit history using paired commits (test added first, then fix applied).

#### 1) Prevent revisions being created for no-op edits

- **Test (fails first):**  
  `test: prevent revision creation when entry unchanged` (`0318cc2`)

- **Fix (makes test pass):**  
  `fix: avoid creating EntryRevision on no-op edits` (`c26ab28`)

**Outcome:**  
Editing an entry without changing any values does **not** create an `EntryRevision`.

---

#### 2) Treat future `trial_end` as paid access in free-lock logic

- **Test (fails first):**  
  `test: add failing lock test for trial_end future subscriptions` (`65cbd5c`)

- **Fix (makes test pass):**  
  `fix: treat future trial_end as paid access in free-lock logic` (`219321a`)

**Outcome:**  
A user with a subscription containing a future `trial_end` date is **not** treated as locked on the free plan.

---

#### 3) Allow free-locked users to delete entries to regain access

- **Test (fails first):**  
  `test: allow free locked users to delete entries to regain access` (`8e63458`)

- **Fix (makes test pass):**  
  `fix: allow free locked users to delete entries to regain access` (`e5e892f`)

**Outcome:**  
Users who have reached the free entry limit can delete an entry to drop below the threshold and immediately regain create/edit access.

This demonstrates traceable red → green cycles in the repository history.

[Back to contents](#contents)

Return to [README.md](../README.md)

---

### Summary

| Metric | Value |
|--------|--------|
| Total tests | 16 |
| Passed | 16 |
| Failed | 0 |
| Errors | 0 |

All automated tests pass successfully.

[Back to contents](#contents)

Return to [README.md](../README.md)

---

### Technical Note

The production environment uses WhiteNoise’s manifest-based static file storage. During testing, the storage backend automatically switches to Django’s standard `StaticFilesStorage` to prevent manifest lookup errors and allow templates to render correctly without requiring `collectstatic`.

[Back to contents](#contents)

Return to [README.md](../README.md)

---

### Test Output Log

The full raw console output from the automated test run can be viewed:  
[here](./automated-tests.txt)

This file contains the complete Django test runner output showing all migrations, test execution, and the final successful result.

[Back to contents](#contents)

Return to [README.md](../README.md)

---

**End of TESTING**
