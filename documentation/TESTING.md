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
    - [Free Plan Limits (Business Logic)](#free-plan-limits)
    - [Permissions & Security](#permissions--security)
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

    python manage.py test -v 3

Example successful output:

    Ran 12 tests in 6.4s
    OK

[Back to contents](#contents)

Return to [README.md](../README.md)

---

### Test Structure

Tests are organised per app following Django best practices:

    core/tests/
        test_plan_status.py
        test_limits.py
        test_permissions.py

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

[Back to contents](#contents)

Return to [README.md](../README.md)

---

### Summary

| Metric | Value |
|--------|--------|
| Total tests | 12 |
| Passed | 12 |
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

The full raw console output from the automated test run can be viewed: [here](./automated-tests.txt)

This file contains the complete Django test runner output showing all migrations, test execution, and the final successful result.

[Back to contents](#contents)

Return to [README.md](../README.md)

---

### Test-First Workflow Evidence

For selected business rules, tests were written before implementing fixes/features. This is reflected in commit history using paired commits such as:

- `test: add failing test for ...`
- `fix/feat: ...`

This provides clear traceability between requirements, automated tests, and implementation.

[Back to contents](#contents)

Return to [README.md](../README.md)

---



















**End of TESTING**  