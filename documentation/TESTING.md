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

#### Standard Site User 1

Username: TestSiteUser1  
Email: testsiteuser1@testuser.com  
Password: Password98765  

#### Standard Site User 2

Username: TestSiteUser2  
Email: testsiteuser2@testuser.com  
Password: Password99999  

#### Standard Site User 3

Username: TestSiteUser3  
Email: testsiteuser3@testuser.com  
Password: Password88888  

Return to [README.md](../README.md)

[Back to contents](#contents)

Return to [README.md](../README.md)

---
## Manual Testing
---

### CSS Validation

All CSS files were tested using the **W3C CSS Validator**.

| File Tested | Result | Notes / Fixes Applied |
|------------|--------|------------------------|
| `static/css/main.css` | ✔ No errors | Informational warnings only (see explanation below) |
| `static/css/auth.css` | ✔ No errors | Informational warnings only |
| `static/css/entry.css` | ✔ No errors | Informational warnings only |

#### Validator Warnings Explained

The validator returned several **non-critical warnings**, all of which are expected due to modern CSS usage:

- **CSS Variables (`var(--variable-name)`)**  
  The validator states that CSS variables cannot be statically checked.  
  This is expected behaviour and does not indicate an error.

- **Vendor-prefixed properties**  
  Properties such as `-webkit-appearance`, `::-webkit-slider-thumb`, and `::-moz-range-thumb` are intentionally used to ensure consistent cross-browser styling (particularly for the custom hue range slider).  
  Vendor extensions are normal and valid in production code.

- **External `@import` (Google Fonts)**  
  The validator does not check externally imported stylesheets in direct input mode.  
  This does not affect site functionality.

- **Matching `background-color` and `border-color` on hover**  
  A minor stylistic warning was raised where hover states intentionally use the same colour for visual consistency.  
  This is intentional and does not impact accessibility or rendering.

No CSS errors were found, and no functional or accessibility issues were identified during validation.


[Back to contents](#contents)

Return to [README.md](../README.md)

---

### JavaScript Validation

All custom JavaScript files were validated using **JSHint**.

JSHint was configured to support modern syntax by adding the following directive at the top of each file:

`/* jshint esversion: 8 */`

The “New JavaScript features (ES6)” option was disabled in the JSHint configuration panel to avoid conflicts with the `esversion` setting.

| File Tested | Result | Notes / Fixes Applied |
|------------|--------|------------------------|
| `static/js/main.js` | ✅ No warnings | Async/await validated; DOM guards in place |
| `static/js/auth.js` | ✅ No warnings | Password visibility toggle validated |
| `static/js/entry.js` | ✅ No warnings | Emotion filter and hue label logic validated |

#### Checks Performed

- ✅ No syntax errors  
- ✅ No undefined variables  
- ✅ No console errors on pages without certain DOM elements  
- ✅ Event listeners conditionally guarded where required  
- ✅ Async/await correctly linted under ES8  
- ✅ No unused or unreachable code flagged  

JSHint metrics indicated appropriate function size and complexity for interactive UI behaviour. The highest reported cyclomatic complexity reflects structured conditional logic within dashboard features and does not indicate a validation issue.

[Back to contents](#contents)

Return to [README.md](../README.md)

---

### HTML Validation

All user-facing pages were validated using the **W3C HTML Validator** against the fully rendered HTML output of the live Heroku deployment.

Validation was performed using:
https://validator.w3.org/

Partials were not validated standalone, as they are rendered within `base.html`.

---

#### HTML Summary

| Page / Template | Errors Found | Warnings Found | Fixes Applied | Notes |
|----------------|--------------|----------------|--------------|------|
| `core/home.html` | 0 | 0 | ARIA cleanup & semantic improvements | Validated against live rendered HTML |
| `core/dashboard.html` | 0 | 0 | None required | Validated against live rendered HTML |
| `core/my_entries.html` | 0 | 0 | Prevented `value="None"` in date input using `default_if_none` filter | Validated against live rendered HTML |
| `core/new_entry.html` | 0 | 0 | None required | Validated against live rendered HTML |
| `core/entry_detail.html` | 0 | 0 | None required | Validated against live rendered HTML |
| `core/entry_edit.html` | 0 | 0 | None required | Validated against live rendered HTML |
| `pages/faq.html` | ☐ Pending | ☐ Pending | ☐ Pending | |
| `pages/support.html` | ☐ Pending | ☐ Pending | ☐ Pending | |
| `pages/contact.html` | ☐ Pending | ☐ Pending | ☐ Pending | |
| `billing/regulate_plus.html` | ☐ Pending | ☐ Pending | ☐ Pending | |
| `billing/checkout_cancelled.html` | ☐ Pending | ☐ Pending | ☐ Pending | |
| `account/signup.html` | ☐ Pending | ☐ Pending | ☐ Pending | |
| `account/login.html` | ☐ Pending | ☐ Pending | ☐ Pending | |
| `account/profile.html` | ☐ Pending | ☐ Pending | ☐ Pending | |
| `account/change_username.html` | ☐ Pending | ☐ Pending | ☐ Pending | |
| `account/change_email.html` | ☐ Pending | ☐ Pending | ☐ Pending | |
| `account/password_change.html` | ☐ Pending | ☐ Pending | ☐ Pending | |
| `account/password_reset.html` | ☐ Pending | ☐ Pending | ☐ Pending | |
| `account/password_reset_done.html` | ☐ Pending | ☐ Pending | ☐ Pending | |
| `account/password_reset_from_key.html` | ☐ Pending | ☐ Pending | ☐ Pending | |
| `account/password_reset_from_key_done.html` | ☐ Pending | ☐ Pending | ☐ Pending | |
| `404.html` | 0 | 0 | None required | Validated against live rendered HTML |
| `500.html` | 0 | 0 | None required | Validated against live rendered HTML |
| `partials/footer.html` | N/A | N/A | Not validated standalone | Rendered via base template |
| `partials/navbar.html` | N/A | N/A | Not validated standalone | Rendered via base template |
| `base.html` | N/A | N/A | Not validated standalone | Layout wrapper |

---

#### Common Checks Confirmed on `home.html`

- No invalid ARIA attributes  
- No unnecessary landmark roles  
- No invalid `aria-describedby` usage  
- No nested interactive elements  
- Labels correctly associated with inputs  
- Valid semantic landmark structure  

---

#### HTML Full Details (collapsible example)

<details>
<summary><strong>Home Page – core/home.html</strong></summary>

Initial validation identified:

- Unnecessary `role="navigation"` on the `<nav>` element  
- Invalid `aria-label` usage on a `<div>` element  

These were resolved by:

- Removing redundant landmark roles (HTML5 `<nav>` already provides semantic meaning)  
- Removing inappropriate ARIA attributes from non-landmark elements  

After refactoring and redeploying to Heroku, the rendered HTML was revalidated.

Final result:
- 0 Errors  
- 0 Warnings  

Validated against the fully rendered live HTML output.

</details>

<details>
<summary><strong>My Entries Page – core/my_entries.html</strong></summary>

Initial validation identified:

- **Error:** `Bad value None for attribute value on element input`
- Cause: The `type="date"` input was rendering `value="None"` when no date filter was applied.
- This violates the required `YYYY-MM-DD` format for HTML date inputs.

Resolution:

- Updated the template to use:
  ```
  {{ search_date|default_if_none:'' }}
  ```
- This ensures an empty string is rendered instead of `"None"` when no date is selected.
- Prevents invalid HTML output while maintaining filter functionality.

Final result after redeploy and revalidation:

- 0 Errors  
- 0 Warnings  

Validated against the fully rendered live HTML output via the W3C HTML Validator.

</details>



[Back to contents](#contents)

Return to [README.md](../README.md)

---

## Lighthouse Testing

Key pages tested:
- Home
- Dashboard
- My Entries
- New Entry
- Regulate+

### Desktop Results

| Page | Performance | Accessibility | Best Practices | SEO | Notes |
|------|------------|---------------|---------------|-----|------|
| Home | ☐ Pending | ☐ Pending | ☐ Pending | ☐ Pending | |
| Dashboard | ☐ Pending | ☐ Pending | ☐ Pending | ☐ Pending | |
| My Entries | ☐ Pending | ☐ Pending | ☐ Pending | ☐ Pending | |
| New Entry | ☐ Pending | ☐ Pending | ☐ Pending | ☐ Pending | |
| Regulate+ | ☐ Pending | ☐ Pending | ☐ Pending | ☐ Pending | |

### Mobile Results

| Page | Performance | Accessibility | Best Practices | SEO | Notes |
|------|------------|---------------|---------------|-----|------|
| Home | ☐ Pending | ☐ Pending | ☐ Pending | ☐ Pending | |
| Dashboard | ☐ Pending | ☐ Pending | ☐ Pending | ☐ Pending | |
| My Entries | ☐ Pending | ☐ Pending | ☐ Pending | ☐ Pending | |
| New Entry | ☐ Pending | ☐ Pending | ☐ Pending | ☐ Pending | |
| Regulate+ | ☐ Pending | ☐ Pending | ☐ Pending | ☐ Pending | |

Evidence:
- ☐ `documentation/testing-media/images/lighthouse-*.png`

[Back to contents](#contents)

Return to [README.md](../README.md)

---

## Responsiveness Testing

| Device / Screen Size | Result | Notes |
|----------------------|--------|------|
| Mobile – 360px | ☐ Pending | |
| Mobile – 390px | ☐ Pending | |
| Mobile – 375px | ☐ Pending | |
| Tablet – 768px | ☐ Pending | |
| Laptop – 1366px | ☐ Pending | |
| Desktop – 1920px | ☐ Pending | |

Critical checks:
- ☐ Entry form usable on mobile
- ☐ Emotion list scroll behaves correctly
- ☐ Regulate+ CTA responsive
- ☐ Navbar collapses correctly

Evidence:
- ☐ `documentation/testing-media/gifs/responsive-*.gif`

[Back to contents](#contents)

Return to [README.md](../README.md)

---

## Browser Compatibility Testing

| Browser | Version Tested | Result | Notes |
|--------|----------------|--------|------|
| Chrome | Latest | ☐ Pending | |
| Firefox | Latest | ☐ Pending | |
| Edge | Latest | ☐ Pending | |
| Safari | Latest | ☐ Pending | |
| Samsung Internet | Latest | ☐ Pending | |

[Back to contents](#contents)

Return to [README.md](../README.md)

---

## User Story Testing

| Feature | What Was Checked | Pass/Fail |
|---------|------------------|----------|
| Authentication | Signup, login, logout | ☐ Pending |
| Create entry | Hue, emotions, notes save | ☐ Pending |
| View entries | Date grouping, detail page | ☐ Pending |
| Edit entry | Updates persist, revision logic | ☐ Pending |
| Delete entry | Removes correctly | ☐ Pending |
| Keyword search | Notes + emotions matched | ☐ Pending |
| Free plan limit | Lock at limit, unlock on delete | ☐ Pending |
| Subscription gating | Trial/active/grace logic | ☐ Pending |
| Support ticket | Logged-in vs logged-out validation | ☐ Pending |

[Back to contents](#contents)

Return to [README.md](../README.md)

---

## Feature Interaction Testing

| Area Tested | What Was Checked | Result |
|------------|------------------|--------|
| Forms | Validation, accessibility labels | ☐ Pending |
| Buttons | Create/edit/delete behaviour | ☐ Pending |
| Links | Navigation and redirects | ☐ Pending |
| Business Logic | Locking logic + plan messaging | ☐ Pending |
| Stripe (Test Mode) | Checkout success/cancel flows | ☐ Pending |

[Back to contents](#contents)

Return to [README.md](../README.md)

---

## Admin Area Security Testing

| Security Check | Description | Status |
|----------------|-------------|--------|
| Admin restricted | `/admin/` blocked for non-staff | ☐ Pending |
| Ownership enforced | Cannot edit others’ entries | ☐ Pending |
| CSRF protection | Tokens present | ☐ Pending |
| Confirmation prompts | Dangerous actions gated | ☐ Pending |

[Back to contents](#contents)

Return to [README.md](../README.md)

---

## Error Handling

| Error Type | Behaviour | Result |
|------------|-----------|--------|
| 404 | Custom 404 template renders | ☐ Pending |
| 500 | Custom 500 template renders | ☐ Pending |

[Back to contents](#contents)

Return to [README.md](../README.md)

---

## Security Testing

| Security Area | What Was Tested | Result |
|---------------|----------------|--------|
| Authentication protection | Login required for protected pages | ☐ Pending |
| Authorisation checks | Ownership enforced | ☐ Pending |
| CSRF | Forms protected | ☐ Pending |
| Environment variables | Keys not exposed | ☐ Pending |
| Production settings | DEBUG off | ☐ Pending |

[Back to contents](#contents)

Return to [README.md](../README.md)

---
### UX Improvements Identified During Testing
---

During manual walkthrough testing of the entry creation flow, it was identified that the **New Entry** page did not provide a clear navigation path back to the user’s entry list without using the browser back button.

This was considered poor UX because:
- Users could feel “trapped” on the form
- There was no explicit cancel/return action
- It did not align with the calm, low-pressure design intent of Regulate

#### Fix Implemented

A clear return link was added beneath the form submission controls:

```html
<!-- Cancel and return to entries -->
<div class="entry-actions justify-content-center">
    <a href="{% url 'my_entries' %}">
        Cancel and return to your entries
    </a>
</div>
```

#### Result

- Users can now exit the form without submitting data.
- Navigation flow is clearer and more intuitive.
- Behaviour tested on both desktop and mobile.
- No validation or layout issues introduced.

This improves overall usability and aligns with Regulate’s trauma-informed design approach.

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
