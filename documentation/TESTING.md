# Testing
----------

Here you will find all tests performed on the Regulate site.

Return to [README.md](../README.md)

----------
## Contents
----------

1. [Test User Accounts](#test-user-accounts)
2. [Manual Testing](#manual-testing)
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

Return to [README.md](../README.md)

---

## Test User Accounts
---

To allow the assessors to fully explore the site, the following **dummy accounts** have been created for testing purposes only.  
These accounts contain no personal data and can be safely shared.

### Admin Dashboard Access

#### Superuser Account (Full Django Admin Access)
For security reasons, the superuser login details are not included in the repository.  
They have been submitted separately through the Peterborough University Dashboard under the submission comment section.

#### Admin Staff Account (Restricted Admin Permissions - view only)

Username: TestAdminviewonly  
Email: testadminviewonly@testuser.com  
Password: Password54321  

[Back to contents](#contents)

Return to [README.md](../README.md)

---

### Regulate Main Site Access

#### Standard Site User 1 (Free plan)

Username: TestSiteUser1  
Email: testsiteuser1@testuser.com  
Password: Password98765  

#### Standard Site User 2 (Free Trial)

Username: TestSiteUser2  
Email: testsiteuser2@testuser.com  
Password: Password99999  

#### Standard Site User 3 (Full Subscription)

Username: TestSiteUser3  
Email: testsiteuser3@testuser.com  
Password: Password88888  

Return to [README.md](../README.md)

[Back to contents](#contents)

Return to [README.md](../README.md)

---
## Manual Testing
---

(To be completed – validation screenshots, feature interaction walkthroughs, and browser/device checks will be added here.)

[Back to contents](#contents)

Return to [README.md](../README.md)

---
## Automated Testing
---

Automated tests were implemented using Django’s built-in `TestCase` framework.

These tests validate:

- Subscription plan detection and banner rendering
- Free plan entry limits and gating logic
- Authentication requirements
- User ownership and permission controls
- Revision logic
- Deletion behaviour under free plan limits
- Keyword search functionality

Tests simulate real user behaviour by sending HTTP requests to views where appropriate.

[Back to contents](#contents)

Return to [README.md](../README.md)

---

### Running Tests

From the project root:

    python manage.py test -v 3

Latest successful output:

    Ran 17 tests in 9.556s
    OK

[Back to contents](#contents)

Return to [README.md](../README.md)

---

### Test Structure

Tests are organised per app following Django best practice:

    core/tests/
        test_plan_status.py
        test_limits.py
        test_permissions.py
        test_revision_creation.py
        test_delete_unlocks.py
        test_keyword_search.py

[Back to contents](#contents)

Return to [README.md](../README.md)

---

### Plan & Subscription Behaviour

| Test Case | Purpose | Result |
|------------|---------------------------------------------|---------|
| Free user shows Free plan banner | Default experience without subscription | Passed |
| Trialing status shows trial banner | Stripe `trialing` state recognised | Passed |
| Future `trial_end` shows trial banner | Date-based trial detection | Passed |
| Active subscription shows plus banner | Paid plan recognised correctly | Passed |
| Cancelled but period active shows ending soon | Grace-period messaging works | Passed |

[Back to contents](#contents)

Return to [README.md](../README.md)

---

### Free Plan Limits (Business Logic)

| Test Case | Purpose | Result |
|------------|----------------------------------|---------|
| Below limit not locked | User can continue posting | Passed |
| At limit locked | Posting correctly restricted | Passed |
| Active subscription never locked | Paid users unrestricted | Passed |
| Trialing user never locked | Trial users unrestricted | Passed |
| Future `trial_end` never locked | Treat future trial as paid access | Passed |

[Back to contents](#contents)

Return to [README.md](../README.md)

---

### Permissions & Security

| Test Case | Purpose | Result |
|------------|--------------------------------------|---------|
| Dashboard requires login | Anonymous users redirected | Passed |
| Cannot view another user’s entry | Data privacy enforced | Passed |
| Cannot edit another user’s entry | Ownership enforced | Passed |
| Cannot delete another user’s entry | Ownership enforced | Passed |

[Back to contents](#contents)

Return to [README.md](../README.md)

---

### Test-Driven Development Evidence

Several features were implemented using a test-first (Red → Green) workflow. This is traceable in the commit history.

[Back to contents](#contents)

Return to [README.md](../README.md)

---

#### 1) Prevent revision creation on unchanged edits

Test (fails first):  
test: prevent revision creation when entry unchanged (0318cc2)

Fix:  
fix: avoid creating EntryRevision on no-op edits (c26ab28)

Outcome:  
No EntryRevision is created when a user submits an edit without changing values.

[Back to contents](#contents)

Return to [README.md](../README.md)

---

#### 2) Treat future trial_end as paid access

Test (fails first):  
test: add failing lock test for trial_end future subscriptions (65cbd5c)

Fix:  
fix: treat future trial_end as paid access in free-lock logic (219321a)

Outcome:  
Users with a future trial_end date are not treated as locked.

[Back to contents](#contents)

Return to [README.md](../README.md)

---

#### 3) Allow free-locked users to delete entries to regain access

Test (fails first):  
test: allow free locked users to delete entries to regain access (8e63458)

Fix:  
fix: allow free locked users to delete entries to regain access (e5e892f)

Outcome:  
Deleting an entry reduces the count and restores create/edit access.

[Back to contents](#contents)

Return to [README.md](../README.md)

---

#### 4) Keyword search for entries (User Story 13)

Test (fails first):  
test: add failing keyword search test for entries (89933aa)

Feature implementation:  
feat: add keyword search to my entries (e0209d9)

Outcome:  
Users can search their entries by keyword.

Search matches:
- Notes field
- Comma-separated emotion words
- Only entries belonging to the logged-in user

This completes the SHOULD-HAVE user story for keyword search.

[Back to contents](#contents)

Return to [README.md](../README.md)

---

### Summary

| Metric | Value |
|---------|-------|
| Total tests | 17 |
| Passed | 17 |
| Failed | 0 |
| Errors | 0 |

All automated tests pass successfully.

[Back to contents](#contents)

Return to [README.md](../README.md)

---

### Technical Note

The production environment uses WhiteNoise manifest storage.  
During testing, Django falls back to standard static storage to avoid manifest lookup errors and allow template rendering without requiring collectstatic.

[Back to contents](#contents)

Return to [README.md](../README.md)

---

### Test Output Log

The full raw console output from the automated test run can be viewed here:

    ./automated-tests.txt

[Back to contents](#contents)

Return to [README.md](../README.md)

---

End of TESTING
