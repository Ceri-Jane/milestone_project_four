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
   - [JavaScript Validation](#javascript-validation)
   - [HTML Validation](#html-validation)
   - [Lighthouse Testing](#lighthouse-testing)
      - [Pages Tested](#pages-tested)
      - [Desktop Results](#desktop-results)
      - [Mobile Results](#mobile-results)           
   - [Responsiveness Testing](#responsiveness-testing)
   - [Wave Testing](#wave-testing)
   - [Browser Compatibility Testing](#browser-compatibility-testing)
   - [User Story Testing](#user-story-testing)
   - [Feature Interaction Testing](#feature-interaction-testing)
   - [Admin Area Security Testing](#admin-area-security-testing)
   - [Error Handling](#error-handling)
   - [Security Testing](#security-testing)
   - [UX Improvements Identified During Testing](#ux-improvements-identified-during-testing)
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

To allow assessors to fully explore the application, the following **dummy accounts** have been created for testing purposes only.  
These accounts contain no real personal data and can be safely used during assessment.

---

### Admin Access

| Role | Username | Email | Password | Notes |
|------|----------|-------|----------|-------|
| **Superuser** | *Submitted separately* | — | — | Full Django admin access. Credentials submitted securely via the Peterborough University Dashboard submission comments. |
| **Admin (View-Only)** | TestAdminviewonly | testadminviewonly@testuser.com | Password54321 | Restricted staff permissions. Can access admin but cannot view emotional entry content. |

---

### Main Site Access

| Role | Username | Email | Password | Notes |
|------|----------|-------|----------|-------|
| **Standard User 1** | TestSiteUser1 | testsiteuser1@testuser.com | Password98765 | Free plan user. |
| **Standard User 2** | TestSiteUser2 | testsiteuser2@testuser.com | Password99999 | Used to test ownership and authorisation rules. |
| **Standard User 3** | TestSiteUser3 | testsiteuser3@testuser.com | Password88888 | Can be used to test subscription / trial flows. |


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
| `pages/faq.html` | 0 | 0 | Added `role="region"` to accordion collapse panels to allow `aria-labelledby` | Validated against live rendered HTML |
| `pages/support.html` | 0 | 0 | Corrected heading hierarchy (replaced `h3` with `h2`) | Resolved skipped heading level error |
| `pages/contact.html` | 0 | 0 | None required | Validated against live rendered HTML |
| `billing/regulate_plus.html` | 0 | 0 | None required | Validated against live rendered HTML |
| `billing/checkout_cancelled.html` | 0 | 0 | None required | Validated against live rendered HTML |
| `account/signup.html` | 0 | 0 | Replaced invalid SVG path and ensured valid helptext IDs using `<div>` containers | Resolved SVG path and content model errors |
| `account/login.html` | 0 | 0 | Replaced invalid SVG path for password toggle icon | Resolved SVG path validation error |
| `account/profile.html` | 0 | 0 | None required | Validated against live rendered HTML |
| `account/change_username.html` | 0 | 0 | None required | Validated against live rendered HTML |
| `account/change_email.html` | 0 | 0 | None required | Validated against live rendered HTML |
| `account/password_change.html` | 0 | 0 | Removed empty `action` attribute, replaced invalid SVG path, and added dynamic helptext IDs | Resolved empty action, SVG, and `aria-describedby` errors |
| `account/password_reset.html` | 0 | 0 | None required | Validated against live rendered HTML |
| `account/password_reset_done.html` | 0 | 0 | None required | Validated against live rendered HTML |
| `account/password_reset_from_key.html` | 0 | 0 | Replaced invalid SVG path and ensured `aria-describedby` always references a valid helptext ID | Resolved SVG path and ARIA reference errors |
| `account/password_reset_from_key_done.html` | 0 | 0 | None required | Validated against live rendered HTML |
| `404.html` | 0 | 0 | None required | Validated against live rendered HTML |
| `500.html` | 0 | 0 | None required | Validated against live rendered HTML |
| `partials/footer.html` | N/A | N/A | Not validated standalone | Rendered via base template |
| `partials/navbar.html` | N/A | N/A | Not validated standalone | Rendered via base template |
| `base.html` | N/A | N/A | Not validated standalone | Layout wrapper |

---

#### HTML Full Details (collapsible example)

<details>
<summary><strong>Home Page</strong></summary>

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
<summary><strong>My Entries Page</strong></summary>

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

<details>
<summary><strong>FAQ Page</strong></summary>

Initial validation identified multiple errors of the form:

- `aria-labelledby` was applied to `<div>` elements that had no semantic role, which is invalid ARIA usage.

This occurred on each Bootstrap accordion collapse panel (e.g. `.accordion-collapse`), where Bootstrap expects the panel to be labelled by its corresponding header.

Fix applied:

- Added `role="region"` to each `.accordion-collapse` panel so `aria-labelledby="faqHeading..."` becomes valid and semantically meaningful (the region is now correctly labelled by the accordion header).

After refactoring and redeploying to Heroku, the rendered FAQ HTML was revalidated.

Final result:
- 0 Errors
- 0 Warnings

Validated against the fully rendered live HTML output.

</details>

<details>
<summary><strong>Crisis & Support Page</strong></summary>

Initial validation identified a heading structure error:

- An `<h3>` element followed directly after an `<h1>`, skipping `<h2>`.

This violates semantic heading hierarchy rules and accessibility best practices.

Fix applied:

- Replaced all `<h3>` elements with `<h2>` to maintain a logical, sequential heading structure.

After refactoring and redeploying, the page was revalidated.

Final result:
- 0 Errors  
- 0 Warnings  

Validated against the fully rendered live HTML output.

</details>

<details>
<summary><strong>Signup Page – account/signup.html</strong></summary>

Initial validation identified two issues:

1. `aria-describedby` referenced `id_password1_helptext`, but no element with that ID existed in the rendered HTML.
2. The password help text contained a `<ul>` element nested inside a `<small>` element, which violates the HTML content model (since `<small>` only allows phrasing content).

These were resolved by:

- Explicitly rendering help text with matching IDs (`id_password1_helptext`, `id_password2_helptext`) so `aria-describedby` references valid elements.
- Replacing `<small>` wrappers with `<div>` elements to allow flow content such as `<ul>`.

After refactoring and redeploying to Heroku, the rendered HTML was revalidated.

Final result:
- 0 Errors
- 0 Warnings

Validated against the fully rendered live HTML output.

</details>

<details>
<summary><strong>Password Change Page – account/password_change.html</strong></summary>

Initial validation identified two issues:

1. The `<form>` element used `action=""`, which is invalid in HTML.  
   The validator requires a non-empty value or omission of the attribute.
2. Password fields referenced `aria-describedby="id_password1_helptext"` (and similar IDs), but no corresponding help text elements existed in the rendered document.

These were resolved by:

- Removing the empty `action` attribute so the form posts to the current URL.
- Rendering field help text dynamically using:
  `id="{{ field.id_for_label }}_helptext"`
- Wrapping help text in `<div>` elements instead of `<small>` to allow valid flow content (e.g. `<ul>` from Django password validators).

After refactoring and redeploying, the rendered HTML was revalidated.

Final result:
- 0 Errors
- 0 Warnings

Validated against the fully rendered live HTML output.

</details>

<details>
<summary><strong>account/password_reset_from_key.html – W3C Validation Fixes</strong></summary>

**Errors Identified:**

1. Invalid SVG `path` data in password visibility toggle icon  
   - Validator error: “Bad value for attribute `d` on element `path`”
   - Caused by malformed coordinate sequence in custom eye icon

2. `aria-describedby` referencing non-existent ID (`id_password1_helptext`)
   - Occurred when Django did not render helptext for the password field

---

**Fixes Applied:**

- Replaced malformed SVG path data with a valid, simplified eye icon SVG
- Ensured helptext container is always rendered:
  - If helptext exists → rendered visibly
  - If no helptext → rendered hidden `<div>` with matching ID
- Updated helptext ID to dynamically use:
  `{{ form.password1.id_for_label }}_helptext`

---

**Result:**

- 0 errors
- 0 warnings
- Fully passes W3C HTML validation
- Maintains accessibility compliance (valid ARIA references)

Validated against live rendered HTML source.

</details>

[Back to contents](#contents)

Return to [README.md](../README.md)

---
## Lighthouse Testing
---

All key user-facing pages were tested using **Google Lighthouse** on both **desktop** and **mobile**.

At the time of writing, results are marked as **Pending** and will be updated once full Lighthouse runs are completed on the deployed site. The tables below are structured to record scores consistently across:

- **Performance**
- **Accessibility**
- **Best Practices**
- **SEO**

**Notes for assessors:**
- Mobile performance can be impacted by hosting environment and server response time, particularly on free-tier hosting services.
- Desktop scores tend to provide a more stable representation of code-level optimisation, while mobile results can be more sensitive to network throttling and device simulation.

Key areas that will be reviewed during Lighthouse testing include:
- ARIA roles and labels across interactive components (forms, accordion regions, navigation)
- Colour contrast and form labelling on authentication pages
- Image/video optimisation (landing page media)
- Render-blocking resources and caching behaviour
- SEO metadata consistency (title, meta description, canonical where applicable)

[Back to contents](#contents)

Return to [README.md](../README.md)

---

### Pages Tested

The following templates were reviewed and tested across both desktop and mobile viewports using Chrome DevTools and Lighthouse where applicable.

#### Core user journeys
- Home (`core/home.html`)
- Dashboard (`core/dashboard.html`)
- My Entries (`core/my_entries.html`)
- New Entry (`core/new_entry.html`)
- Entry Detail (`core/entry_detail.html`)
- Edit Entry (`core/entry_edit.html`)
- Regulate+ (`billing/regulate_plus.html`)
- Checkout Cancelled (`billing/checkout_cancelled.html`)

#### User support / static pages
- FAQ (`pages/faq.html`)
- Crisis & Support (`pages/support.html`)
- Contact (`pages/contact.html`)

#### Authentication / account management
- Sign Up (`account/signup.html`)
- Login (`account/login.html`)
- Profile (`account/profile.html`)
- Change Username (`account/change_username.html`)
- Change Email (`account/change_email.html`)
- Change Password (`account/password_change.html`)
- Password Reset (`account/password_reset.html`)
- Password Reset Done (`account/password_reset_done.html`)
- Password Reset From Key (`account/password_reset_from_key.html`)
- Password Reset From Key Done (`account/password_reset_from_key_done.html`)

#### Error pages
- 404 (`404.html`)
- 500 (`500.html`)

The **500 error page** was manually triggered and verified in a controlled local environment (with `DEBUG=False`) to ensure that the custom template renders correctly, displays appropriate messaging, and maintains consistent styling with the rest of the application. As 500 errors are server-side exceptions rather than navigable routes, Lighthouse testing was not included in the standard page audit tables. Visual inspection and functional confirmation confirmed correct behaviour.

[Back to contents](#contents)

Return to [README.md](../README.md)

---

### Desktop Results

| Page / Template | Performance | Accessibility | Best Practices | SEO | Notes |
|----------------|------------|---------------|---------------|-----|------|
| **Home** (`core/home.html`) | 82 | 100 | 100 | 100 | Performance reflects intentional high-resolution desktop media; all other metrics fully compliant |
| **Dashboard** (`core/dashboard.html`) | 100 | 100 | 100 | 100 | Extremely fast render time; no large media assets; clean template structure |
| **My Entries** (`core/my_entries.html`) | 100 | 100 | 100 | 100 | Fast server-rendered content; no heavy media assets; stable layout |
| **New Entry** (`core/new_entry.html`) | 100 | 100 | 100 | 100 | Contrast issue resolved; WCAG AA compliance achieved while maintaining design aesthetic |
| **Entry Detail** (`core/entry_detail.html`) | 98 | 100 | 100 | 100 | Fast server-rendered content; minor flags relate to shared vendor assets |
| **Edit Entry** (`core/entry_edit.html`) | 90 | 100 | 100 | 100 | Strong performance; minor Lighthouse deductions relate to shared static assets |
| **Regulate+** (`billing/regulate_plus.html`) | 100 | 100 | 100 | 100 | Lightweight subscription page; fast render with stable layout |
| **Checkout Cancelled** (`billing/checkout_cancelled.html`) | 100 | 100 | 100 | 100 | Lightweight confirmation page; fast render with no layout instability |
| **FAQ** (`pages/faq.html`) | 100 | 100 | 100 | 100 | Desktop Lighthouse results were perfect; only minor global asset suggestions (Bootstrap/render-blocking, unused CSS/JS) |
| **Crisis & Support** (`pages/support.html`) | 100 | 100 | 100 | 100 | Desktop Lighthouse achieved perfect scores; only minor global asset suggestions (render-blocking Bootstrap and shared JS/CSS bundles) |
| **Contact** (`pages/contact.html`) | 100 | 100 | 100 | 100 | Desktop Lighthouse achieved perfect scores; minor suggestions relate to shared global assets (Bootstrap render-blocking and unused CSS/JS) |
| **Sign Up** (`account/signup.html`) | 100 | 100 | 100 | 100 | Excellent desktop performance with full accessibility compliance and stable layout. |
| **Login** (`account/login.html`) | 100 | 100 | 100 | 100 | Excellent desktop performance with instant rendering (LCP 0.6s) and zero layout shift. |
| **Profile** (`account/profile.html`) | 100 | 100 | 100 | 100 | Instant render (LCP 0.6s) with zero layout shift and full compliance. |
| **Change Username** (`account/change_username.html`) | 100 | 100 | 100 | 100 | Instant render (LCP 0.6s) with zero layout shift and full compliance. |
| **Change Email** (`account/change_email.html`) | 100 | 100 | 100 | 100 | Fast-rendering account form page; no layout shift and no blocking time on desktop |
| **Change Password** (`account/password_change.html`) | 100 | 100 | 100 | 100 | Fast-loading account form page with stable layout (CLS 0) and zero blocking time |
| **Password Reset** (`account/password_reset.html`) | 100 | 100 | 100 | 100 | Fast-load auth page; any remaining suggestions relate to shared global assets (minification / unused JS / render-blocking CSS) |
| **Password Reset Done** (`account/password_reset_done.html`) | 100 | 100 | 100 | 100 | Instant confirmation page with zero layout shift and no blocking time; remaining suggestions relate to shared global assets |
| **Password Reset From Key** (`account/password_reset_from_key.html`) | 100 | 100 | 100 | 100 | Tested locally (reset link generated in terminal); route requires token/email flow not accessible for Lighthouse on deployed site |
| **Password Reset From Key Done** (`account/password_reset_from_key_done.html`) | 100 | 100 | 100 | 100 | Tested locally (reset flow outputs link via terminal in dev setup, so cannot be run end-to-end on Heroku) |
| **404** (`404.html`) | 100 | 100 | 96 | 91 | SEO score reduced due to correct 404 HTTP status (expected behaviour); minor console warning from shared static asset |

[Back to contents](#contents)

Return to [README.md](../README.md)


#### Further Details (Desktop)

<details>
<summary><strong>Home (core/home.html)</strong></summary>

![Lighthouse - home - desktop](testing-media/images/lighthouse-home-desktop.png)

**Performance – 82%**

- Largest Contentful Paint: 3.2s
- Total Blocking Time: 0ms
- Cumulative Layout Shift: 0.025

Lighthouse flagged:
- Large network payload (~24MB total transfer)
- Image optimisation opportunities (~3MB estimated savings)
- Minor unused JavaScript

The score is primarily affected by hero media size rather than blocking scripts or inefficient logic. Core interaction performance remains strong.

**Accessibility – 100%**

- All interactive elements labelled
- ARIA usage valid
- No contrast violations detected

**Best Practices – 100%**

- No console errors
- No deprecated APIs
- HTTPS enforced

**SEO – 100%**

- Meta description present
- Document has title element
- Viewport configured correctly

</details>

<details>
<summary><strong>Dashboard (core/dashboard.html)</strong></summary>

### Results

![Lighthouse - dashboard - desktop](testing-media/images/lighthouse-dashboard-desktop.png)

- **Performance:** 100  
- **Accessibility:** 100  
- **Best Practices:** 100  
- **SEO:** 100  

Key metrics:

- First Contentful Paint: 0.5s  
- Largest Contentful Paint: 0.6s  
- Total Blocking Time: 0ms  
- Cumulative Layout Shift: 0.001  
- Speed Index: 0.5s  

---

### Performance Overview

The dashboard page performs exceptionally well on desktop due to:

- No large media assets
- Lightweight template structure
- Efficient Django rendering
- Minimal client-side JavaScript
- Optimised layout with low DOM complexity

The LCP of 0.6 seconds indicates extremely fast primary content rendering.

---

### Minor Lighthouse Suggestions

Lighthouse identified minor optimisation suggestions including:

- Render-blocking Bootstrap CSS (230ms estimated savings)
- Unused vendor JavaScript (155 KiB estimated)
- Minor unused CSS (25 KiB estimated)
- Image elements missing explicit width and height attributes

These are framework-level optimisations related to Bootstrap and shared base templates. They do not impact real-world performance meaningfully and are common in production Django applications using vendor libraries.

---

### Conclusion

The dashboard page achieves a perfect Lighthouse score across all categories.  
Rendering performance is extremely fast, stable, and fully accessible.

This page demonstrates strong front-end optimisation and clean template architecture.

</details>

<details>
<summary><strong>My Entries (core/my_entries.html)</strong></summary>

### Results

![Lighthouse - entries - desktop](testing-media/images/lighthouse-entries-desktop.png)

- **Performance:** 100  
- **Accessibility:** 100  
- **Best Practices:** 100  
- **SEO:** 100  

Key metrics:

- First Contentful Paint: 0.6s  
- Largest Contentful Paint: 0.6s  
- Total Blocking Time: 0ms  
- Cumulative Layout Shift: 0.002  
- Speed Index: 0.6s  

---

### Performance Overview

The My Entries page renders extremely quickly due to:

- Server-side rendering via Django with minimal client-side processing  
- No large media assets  
- Efficient database querying scoped to the authenticated user  
- Lightweight template structure with controlled DOM complexity  

The Largest Contentful Paint of 0.6 seconds indicates near-instant primary content rendering on desktop.

Layout stability is excellent, with a CLS of 0.002 (well below Google's 0.1 threshold).

---

### Minor Lighthouse Suggestions

Lighthouse reported minor optimisation opportunities including:

- Render-blocking Bootstrap CSS (estimated 230ms savings)
- Unused vendor JavaScript (155 KiB estimated)
- Minor unused CSS (25 KiB estimated)
- Image elements without explicit width and height attributes

These are common framework-level considerations and do not negatively impact user experience or real-world performance.

---

### Conclusion

The My Entries page achieves a perfect Lighthouse score across all categories on desktop.  
Rendering is fast, stable, and accessible, demonstrating efficient template design and minimal client-side overhead.

</details>

<details>
<summary><strong>New Entry (core/new_entry.html)</strong></summary>

### Final Results

![Lighthouse - new entry - desktop-after](testing-media/images/lighthouse-new-entry-desktop-after.png)

- **Performance:** 100  
- **Accessibility:** 100  
- **Best Practices:** 100  
- **SEO:** 100  

Key metrics:

- First Contentful Paint: 0.6s  
- Largest Contentful Paint: 0.6s  
- Total Blocking Time: 0ms  
- Cumulative Layout Shift: 0.005  
- Speed Index: 0.6s  

---

### Original Accessibility Issue

The initial Lighthouse audit reported a **colour contrast failure** on helper text elements within the form:

![Lighthouse - new entry - desktop-before](testing-media/images/lighthouse-new-entry-desktop-before.png)

Failing elements included:

- `p.form-section-hint`
- `p#hue-hint`
- `p#notes-hint`
- `p#emotion-search-hint`
- `.form-card` container background

The muted green hint text colour did not meet the WCAG AA minimum contrast ratio of **4.5:1** against the pale green background of the form card.

Although visually subtle and stylistically consistent with the calming design theme, the contrast was insufficient for users with visual impairments or low vision.

---

### Fix Implemented

The `.form-section-hint` text colour was darkened slightly to increase contrast while maintaining the overall calm aesthetic of the interface.

This adjustment:

- Preserved the design language and colour palette
- Achieved WCAG AA compliance
- Eliminated all contrast-related accessibility errors

No structural or layout changes were required.

---

### Result

After the colour adjustment:

- Accessibility score increased from **95 → 100**
- All Lighthouse categories now score **100**
- Layout stability and performance remained unaffected

The New Entry page now fully complies with WCAG contrast requirements while maintaining Regulate’s soft, non-overwhelming design principles.

</details>

<details>
<summary><strong>Entry Detail (core/entry_detail.html)</strong></summary>

Desktop Lighthouse scores for the Entry Detail page were excellent:

![Lighthouse - entry detail - desktop](testing-media/images/lighthouse-entry-detail-desktop.png)

- Performance: 98
- Accessibility: 100
- Best Practices: 100
- SEO: 100

Key metrics observed:
- First Contentful Paint (FCP): 0.9s
- Largest Contentful Paint (LCP): 0.9s
- Total Blocking Time (TBT): 0ms
- Cumulative Layout Shift (CLS): 0.003
- Speed Index: 0.9s

Minor recommendations shown in Lighthouse were primarily global/shared optimisation flags rather than page-specific defects:

- Render-blocking requests (estimated savings shown)
- “Modern HTTP” suggestion (estimated savings shown)
- “Improve image delivery” (likely relating to shared static assets used across templates)
- Missing explicit width/height attributes on some image elements
- Minify CSS/JS and reduce unused JavaScript (shared bundle recommendations)
- 1 long main-thread task flagged, despite TBT remaining 0ms

No functional, accessibility, SEO, or best-practice issues were identified on this page during Lighthouse testing.

</details>

<details>
<summary><strong>Edit Entry (core/entry_edit.html)</strong></summary>

### Results

![Lighthouse - edit entry - desktop](testing-media/images/lighthouse-edit-entry-desktop.png)

- **Performance:** 90  
- **Accessibility:** 100  
- **Best Practices:** 100  
- **SEO:** 100  

Key metrics:

- First Contentful Paint: 0.6s  
- Largest Contentful Paint: 2.1s  
- Total Blocking Time: 0ms  
- Cumulative Layout Shift: 0.004  
- Speed Index: 0.6s  

---

### Performance Overview

The Edit Entry page performs strongly on desktop despite containing:

- Pre-populated form fields  
- Dynamic input components  
- Conditional rendering elements  
- Emotion selection controls  

The Largest Contentful Paint of 2.1 seconds remains within Google's “Good” performance range (≤ 2.5s).  
Total Blocking Time remains 0ms, confirming that interactive functionality does not impact responsiveness.

Layout stability is excellent, with a CLS of 0.004.

---

### Lighthouse Deductions Explained

The reduction from a perfect score is due to shared optimisation flags, including:

- Render-blocking Bootstrap CSS
- Vendor JavaScript bundle suggestions
- Image delivery optimisation (shared static assets)
- Generic minification recommendations

These relate to global project configuration rather than page-specific inefficiencies.

No functional, accessibility, or SEO issues were identified.

---

### Conclusion

While the performance score is 90, real-world rendering remains fast and stable.  
All core performance metrics fall within acceptable thresholds, and the page remains fully accessible and standards-compliant.

</details>

<details>
<summary><strong>Regulate+ (billing/regulate_plus.html)</strong></summary>

### Results

![Lighthouse - regulate+ - desktop](testing-media/images/lighthouse-regulate-plus-desktop.png)

- **Performance:** 100  
- **Accessibility:** 100  
- **Best Practices:** 100  
- **SEO:** 100  

Key metrics:

- First Contentful Paint: 0.5s  
- Largest Contentful Paint: 0.6s  
- Total Blocking Time: 0ms  
- Cumulative Layout Shift: 0.004  
- Speed Index: 0.5s  

---

### Performance Overview

The Regulate+ subscription page renders extremely quickly on desktop due to:

- Lightweight template structure
- Minimal dynamic content
- No heavy media assets
- Efficient Django server-side rendering

The Largest Contentful Paint of 0.6 seconds indicates near-instant primary content display.

Total Blocking Time remains 0ms, confirming that any billing-related logic does not introduce client-side performance delays.

Layout stability is excellent, with a CLS of 0.004 (well within the 0.1 threshold).

---

### Minor Lighthouse Suggestions

Lighthouse flagged minor framework-level suggestions including:

- Render-blocking Bootstrap CSS
- Reduce unused JavaScript from shared vendor bundles
- Minor unused CSS
- Missing explicit width and height attributes on image elements

These relate to shared global assets rather than page-specific inefficiencies.

---

### Conclusion

The Regulate+ page achieves a perfect Lighthouse score across all categories on desktop.  
Rendering is fast, stable, and fully standards-compliant.

This is particularly important for a subscription/payment page, where performance and accessibility directly influence user trust and conversion confidence.

</details>

<details>
<summary><strong>Checkout Cancelled (billing/checkout_cancelled.html)</strong></summary>

### Results

![Lighthouse - checkout cancelled - desktop](testing-media/images/lighthouse-checkout-cancelled-desktop.png)

- **Performance:** 100  
- **Accessibility:** 100  
- **Best Practices:** 100  
- **SEO:** 100  

Key metrics:

- First Contentful Paint: 0.5s  
- Largest Contentful Paint: 0.6s  
- Total Blocking Time: 0ms  
- Cumulative Layout Shift: 0.004  
- Speed Index: 0.5s  

---

### Performance Overview

The Checkout Cancelled page is a lightweight confirmation page with minimal dynamic content. As expected, it loads extremely quickly and remains fully stable.

- No blocking JavaScript detected  
- No layout instability  
- Minimal DOM complexity  
- No heavy media above the fold  

---

### Lighthouse Observations

Lighthouse flagged minor framework-level suggestions including:

- Render-blocking Bootstrap CSS  
- Generic image optimisation reminders  
- Minor CSS/JS minification suggestions  

These are global project-level considerations rather than page-specific performance concerns.

---

### Conclusion

The Checkout Cancelled page performs optimally on desktop with perfect Lighthouse scores across all categories. Its simple structure ensures fast rendering, strong accessibility compliance, and stable layout behaviour.

</details>

<details>
<summary><strong>FAQ (pages/faq.html)</strong></summary>

### Results

![Lighthouse - FAQ - desktop](testing-media/images/lighthouse-faq-desktop.png)

- **Performance:** 100  
- **Accessibility:** 100  
- **Best Practices:** 100  
- **SEO:** 100  

Key metrics:

- First Contentful Paint: 0.6s  
- Largest Contentful Paint: 0.7s  
- Total Blocking Time: 0ms  
- Cumulative Layout Shift: 0.002  
- Speed Index: 0.6s  

---

### Performance Overview

The FAQ page achieves a perfect Lighthouse score across all categories on desktop.

The Largest Contentful Paint of 0.7 seconds indicates that the main content renders almost immediately, and Total Blocking Time remains 0ms, confirming there are no JavaScript tasks delaying interactivity.

Layout stability is excellent, with a CLS of 0.002 (well below the 0.1 threshold), meaning content does not shift unexpectedly during load.

---

### Minor Lighthouse Suggestions

Lighthouse still reports small optimisation opportunities, but these are typical of shared global assets rather than page-specific issues:

- Render-blocking resources (estimated 240ms savings) — primarily Bootstrap CSS delivery
- Reduce unused CSS / JavaScript from shared bundles across the project
- Minor CSS/JS minification suggestions

These do not affect real-world usability, and the page already performs at the maximum Lighthouse rating on desktop.

---

### Conclusion

The FAQ page performs exceptionally well on desktop, achieving **100/100** across Performance, Accessibility, Best Practices, and SEO. Any remaining Lighthouse notes relate to global/shared assets and do not indicate functional or UX concerns for this page.

</details>

<details>
<summary><strong>Crisis &amp; Support (pages/support.html)</strong></summary>

### Results

![Lighthouse - crisis &amp; support - desktop](testing-media/images/lighthouse-crisis-desktop.png)

- **Performance:** 100  
- **Accessibility:** 100  
- **Best Practices:** 100  
- **SEO:** 100  

Key metrics:

- First Contentful Paint: 0.5s  
- Largest Contentful Paint: 0.6s  
- Total Blocking Time: 0ms  
- Cumulative Layout Shift: 0.002  
- Speed Index: 0.5s  

---

### Performance Overview

The Crisis &amp; Support page achieves perfect Lighthouse scores across all categories on desktop.

Primary content renders extremely quickly (LCP 0.6s), with no blocking time (TBT 0ms), indicating that the page remains fully responsive and interactive during load.

Layout stability is excellent (CLS 0.002), meaning the page loads without noticeable shifting that could disrupt reading or navigation.

---

### Minor Lighthouse Suggestions

Lighthouse flagged only minor, global optimisation opportunities:

- Render-blocking resources (estimated 180ms savings)  
- Modern HTTP delivery suggestion  
- Minor JS/CSS minification suggestions  
- Generic “avoid long main-thread tasks” note (1 task)  

These relate to shared site assets (e.g., Bootstrap/vendor bundles) rather than any page-specific performance issue.

---

### Conclusion

The Crisis &amp; Support page provides fast, stable, and accessible delivery on desktop, which is particularly important for high-stakes support content where clarity and reliability are essential.

</details>

<details>
<summary><strong>Contact (pages/contact.html)</strong></summary>

### Results

![Lighthouse - contact - desktop](testing-media/images/lighthouse-contact-desktop.png)

- **Performance:** 100  
- **Accessibility:** 100  
- **Best Practices:** 100  
- **SEO:** 100  

Key metrics:

- First Contentful Paint: 0.5s  
- Largest Contentful Paint: 0.6s  
- Total Blocking Time: 0ms  
- Cumulative Layout Shift: 0.001  
- Speed Index: 0.5s  

---

### Performance Overview

The Contact page achieves perfect Lighthouse scores on desktop across all categories.

Primary content renders almost instantly (FCP 0.5s, LCP 0.6s), indicating fast initial paint and rapid loading of the largest visible element. Interactivity is immediate, with **0ms Total Blocking Time**, and the layout is highly stable (**CLS 0.001**, well below the 0.1 threshold).

---

### Minor Lighthouse Suggestions

Lighthouse flagged a small number of optimisation opportunities that relate to shared global assets rather than issues specific to the Contact template:

- Render-blocking Bootstrap CSS (estimated 230ms savings)
- Minor “Modern HTTP” suggestion (estimated 40ms savings)
- Reduce unused CSS from global stylesheet loading
- Standard minification suggestions for shared CSS/JS bundles
- Reduce unused JavaScript warnings from shared scripts

These are common trade-offs when using Bootstrap and site-wide JS/CSS on a multi-page Django project.

---

### Conclusion

The Contact page performs exceptionally well on desktop, reaching **100/100 across Performance, Accessibility, Best Practices, and SEO** with excellent paint, stability, and responsiveness metrics.

</details>

<details>
<summary><strong>Sign Up (account/signup.html)</strong></summary>

### Results

![Lighthouse - signup - desktop](testing-media/images/lighthouse-signup-desktop.png)

- **Performance:** 100  
- **Accessibility:** 100  
- **Best Practices:** 100  
- **SEO:** 100  

Key metrics:

- First Contentful Paint: 0.6s  
- Largest Contentful Paint: 0.6s  
- Total Blocking Time: 0ms  
- Cumulative Layout Shift: 0  
- Speed Index: 0.6s  

---

### Performance Overview

The Sign Up page achieves perfect Lighthouse scores across all categories on desktop.

Primary content renders extremely quickly, with both First Contentful Paint and Largest Contentful Paint occurring at 0.6 seconds. Total Blocking Time remains 0ms, confirming that form rendering and password toggle functionality do not introduce main-thread delays.

Cumulative Layout Shift is 0, indicating complete layout stability during page load — an important factor for form usability and accessibility.

---

### Accessibility Enhancements

During review of authentication-related templates, improvements were made to ensure consistent accessibility across login and signup pages:

- Standardised password visibility toggle icon for consistency
- Increased touch target size for toggle buttons to meet accessibility best practices
- Added `aria-pressed` state handling for screen reader clarity
- Ensured SVG icons are marked as decorative (`aria-hidden="true"`)

These updates ensure authentication interactions are both visually consistent and accessible to keyboard and assistive technology users.

---

### Minor Lighthouse Suggestions

Lighthouse highlights minor optimisation opportunities that relate to shared static assets rather than this page specifically:

- Small CSS and JavaScript minification savings
- Minor unused CSS/JS suggestions from global bundles
- Back/forward cache restoration note (related to broader application behaviour)

These do not negatively impact user experience on the signup page.

---

### Conclusion

The Sign Up page demonstrates excellent performance, accessibility, and best-practice compliance. Authentication flows are fast, stable, and inclusive, supporting both usability and trust during account creation.

</details>

<details>
<summary><strong>Login (account/login.html)</strong></summary>

### Results

![Lighthouse - login - desktop](testing-media/images/lighthouse-login-desktop.png)

- **Performance:** 100  
- **Accessibility:** 100  
- **Best Practices:** 100  
- **SEO:** 100  

Key metrics:

- First Contentful Paint: 0.5s  
- Largest Contentful Paint: 0.6s  
- Total Blocking Time: 0ms  
- Cumulative Layout Shift: 0  
- Speed Index: 0.5s  

---

### Performance Overview

The login page achieves perfect desktop Lighthouse scores, indicating fast rendering, stable layout, and highly responsive interactivity.

The Largest Contentful Paint of 0.6 seconds shows that the primary content (form card and core UI) appears almost immediately, supporting a smooth sign-in experience.

Total Blocking Time remains 0ms, confirming that authentication page scripts (including the password visibility toggle) do not introduce any measurable interaction delay.

Layout stability is excellent, with CLS recorded as 0, meaning there are no unexpected shifts as the page loads.

---

### Minor Lighthouse Suggestions

Lighthouse flags a small number of general optimisation opportunities, largely related to shared, site-wide assets rather than page-specific issues:

- Render-blocking requests (Bootstrap/CSS delivery)  
- Minor JavaScript minification and unused JavaScript warnings from shared bundles  
- “Page prevented back/forward cache restoration” (typically related to global script behaviour and not unique to the login template)  

These do not negatively affect usability and did not prevent the page from achieving full scores.

---

### Conclusion

The login page performs exceptionally well on desktop, with perfect Lighthouse scoring across all categories. It loads quickly, remains visually stable, and keeps interaction latency effectively at zero — which is ideal for a critical authentication flow.

</details>

<details>
<summary><strong>Profile (account/profile.html)</strong></summary>

### Results

![Lighthouse - profile - desktop](testing-media/images/lighthouse-profile-desktop.png)

- **Performance:** 100  
- **Accessibility:** 100  
- **Best Practices:** 100  
- **SEO:** 100  

Key metrics:

- First Contentful Paint: 0.5s  
- Largest Contentful Paint: 0.6s  
- Total Blocking Time: 0ms  
- Cumulative Layout Shift: 0  
- Speed Index: 0.5s  

---

### Performance Overview

The Profile page achieves perfect Lighthouse scores across all categories on desktop.

Content renders almost instantly, with both First Contentful Paint and Largest Contentful Paint occurring within 0.6 seconds. Total Blocking Time is 0ms, confirming that profile-related UI logic and account data rendering do not introduce main-thread delays.

Cumulative Layout Shift is recorded at 0, indicating complete visual stability during load — particularly important for account and settings interfaces where clarity and predictability are essential.

---

### Minor Lighthouse Suggestions

Lighthouse highlights minor optimisation opportunities that relate to shared static assets rather than the profile template itself:

- Render-blocking CSS (estimated 230ms savings)
- Small CSS and JavaScript minification suggestions
- Reduce unused JavaScript from shared bundles

These are global asset considerations and do not negatively affect the performance or usability of the profile page.

---

### Conclusion

The Profile page demonstrates excellent desktop performance, full accessibility compliance, and stable layout behaviour. It loads quickly, remains responsive, and provides a smooth user experience for account management tasks.

</details>

<details>
<summary><strong>Change Username (account/change_username.html)</strong></summary>

### Results

![Lighthouse - change username - desktop](testing-media/images/lighthouse-change-username-desktop.png)

- **Performance:** 100  
- **Accessibility:** 100  
- **Best Practices:** 100  
- **SEO:** 100  

Key metrics:

- First Contentful Paint: 0.5s  
- Largest Contentful Paint: 0.6s  
- Total Blocking Time: 0ms  
- Cumulative Layout Shift: 0  
- Speed Index: 0.5s  

---

### Performance Overview

The Change Username page achieves perfect Lighthouse scores across all categories on desktop.

Primary content renders almost instantly, with both First Contentful Paint and Largest Contentful Paint occurring within 0.6 seconds. Total Blocking Time remains 0ms, confirming that account update logic and validation scripts do not introduce measurable interaction delays.

Cumulative Layout Shift is 0, demonstrating complete layout stability — particularly important for account management interfaces where clarity and predictability are essential.

---

### Minor Lighthouse Suggestions

Lighthouse identifies small optimisation opportunities primarily related to shared global assets:

- Render-blocking CSS (estimated 210ms potential savings)
- Minor CSS and JavaScript minification suggestions
- Reduce unused JavaScript from shared bundles
- Single long main-thread task warning (originating from vendor scripts rather than this template)

These are global optimisation considerations and do not negatively impact usability.

---

### Conclusion

The Change Username page delivers excellent desktop performance, full accessibility compliance, and stable layout behaviour. It provides a fast and responsive experience for account updates while maintaining best practice standards.

</details>

<details>
<summary><strong>Change Email (account/change_email.html)</strong></summary>

### Results

![Lighthouse - change email - desktop](testing-media/images/lighthouse-change-email-desktop.png)

- **Performance:** 100  
- **Accessibility:** 100  
- **Best Practices:** 100  
- **SEO:** 100  

Key metrics:

- First Contentful Paint: 0.5s  
- Largest Contentful Paint: 0.6s  
- Total Blocking Time: 0ms  
- Cumulative Layout Shift: 0  
- Speed Index: 0.5s  

---

### Performance Overview

The Change Email page achieves perfect Lighthouse scores across all categories on desktop.

Primary content renders almost immediately, with both First Contentful Paint and Largest Contentful Paint occurring within 0.6 seconds. Total Blocking Time remains at 0ms, confirming that form validation and account update logic do not introduce main-thread delays.

Cumulative Layout Shift is recorded as 0, demonstrating complete visual stability during load — particularly important for account management interfaces where clarity and predictability are essential.

---

### Minor Lighthouse Suggestions

Lighthouse identifies minor optimisation opportunities that relate to shared global assets rather than this specific template:

- Render-blocking CSS (estimated ~220ms savings)
- Minor CSS and JavaScript minification suggestions
- Reduce unused CSS and JavaScript from shared bundles

These are global performance considerations and do not negatively impact the usability or responsiveness of the Change Email page.

---

### Conclusion

The Change Email page demonstrates excellent desktop performance, full accessibility compliance, and stable layout behaviour. It loads quickly, remains responsive, and maintains best-practice standards for account management workflows.

</details>

<details>
<summary><strong>Change Password (account/password_change.html)</strong></summary>

### Results

![Lighthouse - change password - desktop](testing-media/images/lighthouse-change-password-desktop.png)

- **Performance:** 100  
- **Accessibility:** 100  
- **Best Practices:** 100  
- **SEO:** 100  

Key metrics:

- First Contentful Paint: 0.5s  
- Largest Contentful Paint: 0.6s  
- Total Blocking Time: 0ms  
- Cumulative Layout Shift: 0  
- Speed Index: 0.5s  

---

### Performance Overview

The Change Password page loads extremely quickly on desktop, with primary content rendering almost immediately (FCP 0.5s, LCP 0.6s).  

Interactivity remains instant (0ms Total Blocking Time), and the page is fully stable during load (CLS 0), which is particularly important on form pages to prevent input fields shifting under the user.

---

### Minor Lighthouse Suggestions

Lighthouse flagged minor optimisation opportunities related to shared/global assets rather than page-specific issues:

- Render-blocking Bootstrap/CSS delivery (estimated 220ms savings)
- Modern HTTP suggestions (estimated 40ms savings)
- Minor JS/CSS minification opportunities
- Small unused JavaScript reduction suggestions
- One generic long main-thread task warning

These do not prevent the page from achieving perfect scores and can be addressed as part of broader site-wide optimisation if needed.

---

### Conclusion

The Change Password page achieves perfect Lighthouse scores across all categories on desktop, confirming fast load time, stable layout, and strong accessibility/best-practice compliance for a security-critical account flow.

</details>

<details>
<summary><strong>Password Reset (account/password_reset.html)</strong></summary>

### Results

![Lighthouse - password reset - desktop](testing-media/images/lighthouse-password-reset-desktop.png)

- **Performance:** 100  
- **Accessibility:** 100  
- **Best Practices:** 100  
- **SEO:** 100  

Key metrics:

- First Contentful Paint: 0.5s  
- Largest Contentful Paint: 0.6s  
- Total Blocking Time: 0ms  
- Cumulative Layout Shift: 0  
- Speed Index: 0.5s  

---

### Performance Overview

The Password Reset page delivers excellent desktop performance, with primary content rendering almost immediately.

LCP completes in 0.6 seconds and Total Blocking Time remains 0ms, showing that the page stays fully responsive and lightweight during interaction.

A CLS score of 0 confirms a stable layout with no unexpected movement during load.

---

### Minor Lighthouse Suggestions

The remaining Lighthouse recommendations are small and relate to shared project-wide assets rather than page-specific issues:

- Render-blocking CSS from global styles/vendor resources (estimated 230ms savings)
- Minor minification opportunities for CSS/JavaScript
- Reduce unused JavaScript from shared bundles

---

### Conclusion

The Password Reset page achieves a perfect Lighthouse score across all categories on desktop, confirming fast load, stable rendering, and strong overall best-practice compliance for an authentication-critical flow.

</details>

<details>
<summary><strong>Password Reset Done (account/password_reset_done.html)</strong></summary>

### Results

![Lighthouse - password reset done - desktop](testing-media/images/lighthouse-password-reset-done-desktop.png)

- **Performance:** 100  
- **Accessibility:** 100  
- **Best Practices:** 100  
- **SEO:** 100  

Key metrics:

- First Contentful Paint: 0.5s  
- Largest Contentful Paint: 0.6s  
- Total Blocking Time: 0ms  
- Cumulative Layout Shift: 0  
- Speed Index: 0.5s  

---

### Performance Overview

The Password Reset Done confirmation page achieves perfect Lighthouse scores across all categories on desktop.

Primary content renders almost instantly, with both FCP and LCP completing within 0.6 seconds. Total Blocking Time is 0ms, confirming that the page remains fully responsive and lightweight.

Cumulative Layout Shift is 0, indicating complete visual stability during load — particularly important for confirmation screens where clarity and reassurance are key.

---

### Minor Lighthouse Suggestions

Lighthouse identifies small optimisation opportunities related to shared global assets:

- Render-blocking CSS (estimated ~210ms savings)
- Modern HTTP delivery suggestions
- Minor CSS/JavaScript minification opportunities
- Reduce unused JavaScript from shared bundles
- One generic long main-thread task warning

These are site-wide optimisation considerations and do not affect the functionality or usability of this page.

---

### Conclusion

The Password Reset Done page demonstrates excellent desktop performance, stable layout behaviour, and full compliance with accessibility, best practices, and SEO standards.

</details>

<details>
<summary><strong>Password Reset From Key (account/password_reset_from_key.html)</strong></summary>

### Testing Environment Note

This page was tested **locally** rather than on the live Heroku deployment.

The password reset confirmation route is token-based and requires a valid reset link generated via email. In the production environment, reset emails are not publicly accessible (and cannot be safely intercepted for Lighthouse testing).  

When running locally, Django outputs reset emails to the terminal, allowing the secure reset link to be accessed for testing purposes.  

The template, static assets, and styling are identical between local and production environments, so performance results are representative of the deployed version.

---

### Results (Local Environment)

![Lighthouse - password reset from key - desktop](testing-media/images/lighthouse-password-reset-form-key-desktop.png)

- **Performance:** 100  
- **Accessibility:** 100  
- **Best Practices:** 100  
- **SEO:** 100  

Key metrics:

- First Contentful Paint: 0.5s  
- Largest Contentful Paint: 0.5s  
- Total Blocking Time: 0ms  
- Cumulative Layout Shift: 0  
- Speed Index: 0.5s  

---

### Performance Overview

The Password Reset From Key page renders instantly on desktop, with both FCP and LCP completing in 0.5 seconds.

Total Blocking Time remains at 0ms, confirming that password validation and UI logic introduce no responsiveness delays.

Layout stability is perfect (CLS 0), meaning the form remains visually stable during load — particularly important for security-sensitive input pages.

---

### Minor Lighthouse Suggestions

Lighthouse highlights minor optimisation opportunities related to shared global assets:

- Render-blocking CSS (estimated ~250ms savings)
- Improve cache lifetimes for static assets
- Reduce unused CSS/JavaScript from shared bundles
- Minor CSS/JS minification suggestions

These are site-wide considerations and do not indicate issues specific to this template.

---

### Conclusion

The Password Reset From Key page achieves perfect Lighthouse scores in the local environment. Testing locally is appropriate due to the token-based access requirement of this route, and results are representative of the deployed template and asset configuration.

</details>

<details>
<summary><strong>Password Reset From Key Done (account/password_reset_from_key_done.html)</strong></summary>

### Results

![Lighthouse - password reset from key done - desktop](testing-media/images/lighthouse-password-reset-form-key-done-desktop.png)

- **Performance:** 100  
- **Accessibility:** 100  
- **Best Practices:** 100  
- **SEO:** 100  

Key metrics:

- First Contentful Paint: 0.5s  
- Largest Contentful Paint: 0.5s  
- Total Blocking Time: 0ms  
- Cumulative Layout Shift: 0.003  
- Speed Index: 0.5s  

---

### Local Testing Note

This template was tested **locally** rather than on the deployed Heroku site because the password reset “from key” flow requires a valid reset link generated via the email output (sent to the development terminal in this setup). The UI, template, and static assets are the same as the deployed project, so Lighthouse results remain representative.

---

### Performance Overview

The password reset completion page performs at an excellent level on desktop, with instant primary content rendering and no main-thread blocking.

Layout stability is also strong (CLS 0.003), indicating the page loads without visible shifting as fonts and shared assets initialise.

---

### Minor Lighthouse Suggestions

Lighthouse flagged small optimisation opportunities related to shared/global assets rather than this template specifically:

- Render-blocking CSS (estimated 230ms savings)
- Cache lifetime improvements for some static assets (estimated 41KiB savings)
- Minor CSS/JS minification opportunities
- Reduce unused CSS/JavaScript from shared bundles
- Single long main-thread task warning (shared scripts)

---

### Conclusion

The Password Reset From Key Done page achieves perfect Lighthouse scores across all categories on desktop. Performance is fast, stable, and consistent with the project’s broader UX goals, while still maintaining full accessibility, best-practice compliance, and SEO integrity.

</details>

<details>
<summary><strong>404 Error Page (404.html)</strong></summary>

### Results

![Lighthouse - 404 error page - desktop](testing-media/images/lighthouse-404-error-desktop.png)

- **Performance:** 100  
- **Accessibility:** 100  
- **Best Practices:** 96  
- **SEO:** 91  

---

### SEO Score Explanation

The SEO score is reduced because this page correctly returns an HTTP **404 status code**.

Lighthouse flags non-200 responses as “unsuccessful HTTP status codes,” which affects indexing checks. However, this is expected behaviour for a 404 page and is technically correct implementation.

A 404 page should:
- Return HTTP 404 status
- Not be indexed
- Not appear in search results

Therefore, no change is required.

---

### Best Practices Note

A minor console error was detected relating to a failed resource load. This is unrelated to the 404 template itself and likely tied to a shared static asset or favicon request.

All other security and performance audits passed.

---

### Conclusion

The 404 page behaves correctly, returns the appropriate HTTP status, and performs well in all other Lighthouse categories. The reduced SEO score is expected and does not indicate a problem.

</details>



[Back to contents](#contents)

Return to [README.md](../README.md)

---

### Mobile Results

| Page / Template | Performance | Accessibility | Best Practices | SEO | Notes |
|----------------|------------|---------------|---------------|-----|------|
| **Home** (`core/home.html`) | 84 | 100 | 100 | 100 | Performance improved significantly after responsive video optimisation |
| **Dashboard** (`core/dashboard.html`) | 97 | 100 | 100 | 100 | Strong mobile performance; lightweight template with minimal blocking assets |
| **My Entries** (`core/my_entries.html`) | 96 | 100 | 100 | 100 | Strong mobile performance; efficient server rendering and minimal layout shift |
| **New Entry** (`core/new_entry.html`) | 95 | 100 | 100 | 100 | Strong mobile performance; interactive form and slider remain responsive with zero blocking time |
| **Entry Detail** (`core/entry_detail.html`) | 98 | 100 | 100 | 100 | Excellent mobile performance; fast LCP with stable layout and zero blocking time |
| **Edit Entry** (`core/entry_edit.html`) | 85 | 100 | 100 | 100 | Slightly higher LCP due to pre-populated form complexity; no blocking scripts or layout instability |
| **Regulate+** (`billing/regulate_plus.html`) | 98 | 100 | 100 | 100 | Fast subscription page; stable layout and excellent mobile render speed |
| **Checkout Cancelled** (`billing/checkout_cancelled.html`) | 97 | 100 | 100 | 100 | Mobile performance improved from 73 → 97 after removing duplicated CSS in `main.css` and converting the navbar logo from large PNG to optimised WebP (global base template asset). |
| **FAQ** (`pages/faq.html`) | 96 | 100 | 100 | 100 | Strong mobile performance; minor Lighthouse suggestions relate to shared global assets (Bootstrap/render-blocking resources) |
| **Crisis & Support** (`pages/support.html`) | 94 | 100 | 100 | 100 | Strong mobile performance; slight CLS (0.118) noted, remaining suggestions relate to global shared assets |
| **Contact** (`pages/contact.html`) | 94 | 100 | 100 | 100 | Strong mobile performance; slight CLS (0.105) noted, remaining suggestions relate to shared global assets |
| **Sign Up** (`account/signup.html`) | 97 | 100 | 100 | 100 | Strong mobile performance with fast LCP (2.2s) and stable layout (CLS 0.013). |
| **Login** (`account/login.html`) | 97 | 100 | 100 | 100 | Strong mobile performance; minor Lighthouse flags relate to shared global
| **Profile** (`account/profile.html`) | 97 | 100 | 100 | 100 | Strong mobile performance with fast LCP (2.2s) and excellent layout stability (CLS 0.002). |
| **Change Username** (`account/change_username.html`) | 97 | 100 | 100 | 100 | Strong mobile performance (LCP 2.2s) with stable layout and full accessibility compliance. |
| **Change Email** (`account/change_email.html`) | 97 | 100 | 100 | 100 | Strong mobile performance (LCP 2.2s) with stable layout and full compliance. |
| **Change Password** (`account/password_change.html`) | 97 | 100 | 100 | 100 | Strong mobile performance; LCP 2.2s (within “Good” threshold), minimal TBT (10ms), excellent layout stability (CLS 0.01). Minor suggestions relate to shared global assets (render-blocking CSS / unused JS). |
| **Password Reset** (`account/password_reset.html`) | 97 | 100 | 100 | 100 | Strong mobile performance; LCP 2.2s within “Good” range and stable layout (CLS 0.049). Remaining suggestions relate to shared global assets. |
| **Password Reset Done** (`account/password_reset_done.html`) | 97 | 100 | 100 | 100 | Strong mobile performance; remaining Lighthouse suggestions relate to shared global assets (e.g., render-blocking CSS/JS) rather than this template |
| **Password Reset From Key** (`account/password_reset_from_key.html`) | 98 | 100 | 100 | 100 | Tested locally (reset link generated via terminal email output); template/assets match deployed site |
| **Password Reset From Key Done** (`account/password_reset_from_key_done.html`) | 98 | 100 | 100 | 100 | Tested locally (reset flow link generated via terminal during development) |
| **404** (`404.html`) | 97 | 100 | 96 | 91 | Mobile: SEO reduced due to correct 404 status; minor console/static asset warning (expected for error page) |

[Back to contents](#contents)

Return to [README.md](../README.md)

#### Further Details (Mobile)

<details>
<summary><strong>Home (core/home.html)</strong></summary>

### Initial Issue

![Lighthouse - home - mobile-before](testing-media/images/lighthouse-home-mobile-before.png)

The original mobile Lighthouse score was negatively impacted by:

- A 20MB 4K background hero video loading on all devices
- Largest Contentful Paint (LCP) of 18.3 seconds
- Total network payload exceeding 24MB

This significantly delayed mobile rendering and pushed the performance score into the low 70s.

---

### Root Cause

The hero video was being served at full desktop resolution to mobile devices.  
Because video content contributes directly to LCP when used in a hero section, the large file size caused extreme loading delays on simulated mobile 4G throttling.

---

### Optimisation Implemented

Responsive media delivery was introduced using multiple `<source>` tags:

- A compressed 524KB mobile-optimised MP4 served only to screens ≤ 768px
- The original high-resolution video retained for desktop displays
- `preload="metadata"` added to reduce initial blocking behaviour

This reduced total mobile payload from ~24MB to ~3.6MB.

---

### Results After Optimisation

![Lighthouse - home - mobile-after](testing-media/images/lighthouse-home-mobile-after.png)

- **Performance:** 84  
- **Accessibility:** 100  
- **Best Practices:** 100  
- **SEO:** 100  

Key metrics:

- Largest Contentful Paint reduced from **18.3s → 3.4s**
- Total Blocking Time: 0ms
- Cumulative Layout Shift: 0.041 (well within safe threshold)

---

### Remaining Lighthouse Warnings

Remaining mobile performance deductions relate to:

- Render-blocking Bootstrap CSS
- Shared hosting latency (Heroku)
- Generic “reduce unused JS” suggestions from bundled vendor files

These are infrastructure-level or framework-level trade-offs and do not reflect functional issues within the application code.

All user-facing performance metrics now fall within acceptable modern web standards.

</details>

<details>
<summary><strong>Dashboard (core/dashboard.html)</strong></summary>

![Lighthouse - dashboard - mobile](testing-media/images/lighthouse-dashboard-mobile.png)

### Results

- **Performance:** 97  
- **Accessibility:** 100  
- **Best Practices:** 100  
- **SEO:** 100  

Key metrics:

- First Contentful Paint: 1.9s  
- Largest Contentful Paint: 2.1s  
- Total Blocking Time: 0ms  
- Cumulative Layout Shift: 0.019  
- Speed Index: 1.9s  

---

### Performance Overview

The dashboard performs extremely well on mobile devices due to:

- No heavy media assets
- Lightweight template structure
- Efficient server-side rendering via Django
- Minimal JavaScript execution time (0.2s)
- Low layout shift (0.019, well under the 0.1 threshold)

The Largest Contentful Paint of 2.1 seconds places the page within Google's "Good" performance range for mobile.

---

### Minor Lighthouse Suggestions

Lighthouse identified minor optimisation opportunities including:

- Render-blocking Bootstrap CSS (estimated 730ms savings)
- Unused vendor JavaScript (155 KiB estimated)
- Minor unused CSS (25 KiB estimated)
- Missing explicit width and height attributes on some images

These are framework-level or shared-template optimisations and are typical in production Django applications using vendor CSS/JS libraries. They do not negatively impact usability or real-world responsiveness.

---

### Conclusion

The dashboard achieves near-perfect mobile performance while maintaining full accessibility, best practice compliance, and SEO integrity.

This page demonstrates strong front-end efficiency and stable layout behaviour under mobile network simulation.

</details>

<details>
<summary><strong>My Entries (core/my_entries.html)</strong></summary>

### Results

![Lighthouse - entries - mobile](testing-media/images/lighthouse-entries-mobile.png)

- **Performance:** 96  
- **Accessibility:** 100  
- **Best Practices:** 100  
- **SEO:** 100  

Key metrics:

- First Contentful Paint: 2.1s  
- Largest Contentful Paint: 2.3s  
- Total Blocking Time: 0ms  
- Cumulative Layout Shift: 0.004  
- Speed Index: 2.1s  

---

### Performance Overview

The My Entries page performs strongly on mobile devices due to:

- Efficient Django server-side rendering
- Controlled DOM complexity
- No heavy media or background assets
- Minimal JavaScript execution time (0.2s)
- Extremely low layout shift (0.004, well below the 0.1 threshold)

The Largest Contentful Paint of 2.3 seconds falls within Google’s “Good” performance range for mobile.

---

### Minor Lighthouse Suggestions

Lighthouse identified minor optimisation opportunities including:

- Render-blocking Bootstrap CSS (estimated 740ms savings)
- Unused vendor JavaScript (155 KiB estimated)
- Minor unused CSS (25 KiB estimated)
- Missing explicit width and height attributes on some images

These suggestions relate primarily to shared vendor libraries and global templates rather than page-specific inefficiencies. They do not negatively affect usability or real-world responsiveness.

---

### Conclusion

The My Entries page achieves near-perfect mobile performance while maintaining full accessibility, best practice compliance, and SEO integrity.

Rendering is stable, fast, and efficient, demonstrating strong template architecture and appropriate asset management for mobile devices.

</details>

<details>
<summary><strong>New Entry (core/new_entry.html)</strong></summary>

### Results

![Lighthouse - new entry - mobile](testing-media/images/lighthouse-new-entry-mobile.png)

- **Performance:** 95  
- **Accessibility:** 100  
- **Best Practices:** 100  
- **SEO:** 100  

Key metrics:

- First Contentful Paint: 2.2s  
- Largest Contentful Paint: 2.5s  
- Total Blocking Time: 0ms  
- Cumulative Layout Shift: 0.016  
- Speed Index: 2.2s  

---

### Performance Overview

The New Entry page performs strongly on mobile devices despite containing:

- Interactive form inputs  
- A dynamic hue slider  
- Emotion filtering functionality  
- Conditional rendering elements  

The Largest Contentful Paint of 2.5 seconds sits directly at the threshold of Google's “Good” performance range for mobile (≤ 2.5s).

Layout stability remains excellent, with a CLS of 0.016 (well below the 0.1 threshold).

JavaScript execution time is minimal (0.2s), and Total Blocking Time remains 0ms, indicating that interactive elements do not degrade responsiveness.

---

### Minor Lighthouse Suggestions

Lighthouse identified minor optimisation opportunities including:

- Render-blocking Bootstrap CSS (estimated 680ms savings)
- Unused vendor JavaScript (155 KiB estimated)
- Minor unused CSS
- Missing explicit width and height attributes on images
- Generic main-thread task warnings

These are framework-level optimisations associated with shared vendor libraries and global templates rather than page-specific inefficiencies.

No performance issues were identified related to the hue slider or emotion filtering functionality.

---

### Conclusion

The New Entry page achieves near-perfect mobile performance while maintaining full accessibility, best practice compliance, and SEO integrity.

Performance remains stable even with dynamic form functionality, demonstrating efficient front-end implementation and controlled asset loading.

</details>

<details>
<summary><strong>Entry Detail (core/entry_detail.html)</strong></summary>

### Results

![Lighthouse - entry detail - mobile](testing-media/images/lighthouse-entry-detail-mobile.png)

- **Performance:** 98  
- **Accessibility:** 100  
- **Best Practices:** 100  
- **SEO:** 100  

Key metrics:

- First Contentful Paint: 1.9s  
- Largest Contentful Paint: 2.0s  
- Total Blocking Time: 0ms  
- Cumulative Layout Shift: 0.033  
- Speed Index: 1.9s  

---

### Performance Overview

The Entry Detail page performs exceptionally well on mobile devices.

The Largest Contentful Paint of 2.0 seconds falls well within Google’s “Good” performance threshold (≤ 2.5s), indicating fast primary content rendering even under simulated mobile network conditions.

Total Blocking Time remains at 0ms, demonstrating that interactive elements and page logic do not hinder responsiveness. Layout stability is strong, with a CLS of 0.033 (well below the 0.1 threshold).

Despite containing structured emotional data and conditional rendering (e.g., revision history display), the page maintains excellent mobile performance.

---

### Minor Lighthouse Suggestions

Lighthouse identified several minor optimisation suggestions, primarily related to shared static assets rather than page-specific implementation:

- Render-blocking Bootstrap CSS (estimated 710ms savings)
- Reduce unused JavaScript from shared vendor bundles
- Minor unused CSS
- Missing explicit width and height attributes on image elements
- Generic main-thread task warnings

These are framework-level considerations associated with global templates and vendor libraries rather than inefficiencies within this specific page.

---

### Accessibility Notes

Accessibility scored 100. Lighthouse additionally highlighted manual checks (keyboard navigation, ARIA roles, focus management, etc.), which were reviewed during development to ensure:

- Logical DOM order
- Keyboard-accessible interactive elements
- Proper use of semantic HTML and ARIA where required
- No focus traps or hidden offscreen content issues

---

### Conclusion

The Entry Detail page achieves near-perfect mobile performance while maintaining full accessibility, best practice compliance, and SEO integrity.

Performance remains stable and efficient despite dynamic content rendering, demonstrating controlled asset management and clean template architecture.

</details>

<details>
<summary><strong>Edit Entry (core/entry_edit.html)</strong></summary>

### Results

![Lighthouse - edit entry - mobile](testing-media/images/lighthouse-edit-entry-mobile.png)

- **Performance:** 85  
- **Accessibility:** 100  
- **Best Practices:** 100  
- **SEO:** 100  

Key metrics:

- First Contentful Paint: 2.3s  
- Largest Contentful Paint: 3.9s  
- Total Blocking Time: 0ms  
- Cumulative Layout Shift: 0.005  
- Speed Index: 2.3s  

---

### Performance Overview

The Edit Entry page contains pre-populated form fields and dynamic components, which increases initial HTML payload compared to the New Entry page.

While performance remains stable (0ms Total Blocking Time and minimal layout shift), the Largest Contentful Paint of 3.9 seconds places this page within Google’s “Needs Improvement” range for mobile (2.5–4.0s).

However:

- JavaScript execution time remains low (0.2s)
- Layout stability is excellent (CLS 0.005)
- No blocking scripts were detected
- Total network payload remains within reasonable limits (~1.7MB)

---

### Lighthouse Deductions Explained

The performance score reduction is primarily influenced by:

- Render-blocking Bootstrap CSS
- Shared vendor JavaScript bundle size
- Image delivery optimisation flags
- Generic DOM size optimisation suggestions

These are framework-level considerations rather than page-specific inefficiencies.

---

### Conclusion

Although the performance score is slightly lower than other pages, the Edit Entry page remains fully responsive, accessible, and stable under mobile conditions.

The reduced score reflects the additional structural complexity of an editable, pre-populated form rather than functional performance issues.

</details>

<details>
<summary><strong>Regulate+ (billing/regulate_plus.html)</strong></summary>

### Results

![Lighthouse - regulate+ - mobile](testing-media/images/lighthouse-regulate-plus-mobile.png)

- **Performance:** 98  
- **Accessibility:** 100  
- **Best Practices:** 100  
- **SEO:** 100  

Key metrics:

- First Contentful Paint: 1.9s  
- Largest Contentful Paint: 2.0s  
- Total Blocking Time: 0ms  
- Cumulative Layout Shift: 0.025  
- Speed Index: 1.9s  

---

### Performance Overview

The Regulate+ page performs exceptionally well on mobile devices.

The Largest Contentful Paint of 2.0 seconds falls comfortably within Google’s “Good” performance threshold (≤ 2.5s), indicating fast primary content rendering even under simulated mobile network conditions.

Total Blocking Time remains 0ms, demonstrating that subscription-related logic and page interactivity do not introduce responsiveness delays.

Layout stability is strong, with a CLS of 0.025, well below the 0.1 threshold.

---

### Minor Lighthouse Suggestions

Lighthouse identified minor optimisation opportunities, primarily related to shared project assets:

- Render-blocking Bootstrap CSS (estimated 740ms savings)
- Reduce unused JavaScript from shared vendor bundles
- Minor CSS minification suggestions
- Missing explicit width and height attributes on image elements
- Generic long main-thread task warnings

These relate to global static assets rather than page-specific inefficiencies.

---

### Conclusion

The Regulate+ subscription page achieves near-perfect mobile performance while maintaining full accessibility, best practice compliance, and SEO integrity.

Performance remains stable and fast, which is particularly important for subscription and payment-related pages where user trust and smooth interaction are critical.

</details>

<details>
  <summary><strong>Checkout Cancelled (billing/checkout_cancelled.html)</strong> </summary>

  <h4>Initial Result (Before Optimisation)</h4>

![Lighthouse - cancelled checkout - mobile before](testing-media/images/lighthouse-checkout-cancelled-mobile-before.png)

  <ul>
    <li><strong>Performance:</strong> 73</li>
    <li><strong>Largest Contentful Paint (LCP):</strong> 9.5s</li>
    <li><strong>Cumulative Layout Shift (CLS):</strong> 0.048</li>
    <li><strong>Main Issue Flagged:</strong> Improve image delivery (~1.47MB)</li>
  </ul>

  <p>
    The low performance score was caused by two global issues inherited from <code>base.html</code>:
  </p>
  <ul>
    <li>An oversized PNG navbar logo (~1.5MB) loading on every page.</li>
    <li>Accidental duplicated CSS within <code>main.css</code>, increasing render-blocking and unused CSS.</li>
  </ul>

  <h4>Optimisations Applied</h4>
  <ul>
    <li>Converted navbar logo from large PNG to compressed WebP using Squoosh.</li>
    <li>Resized the logo appropriately for display (80px height) and added explicit <code>width</code> and <code>height</code> attributes to prevent layout shift.</li>
    <li>Removed duplicated CSS from <code>static/css/main.css</code> to reduce render-blocking overhead.</li>
  </ul>

  <h4>Result After Optimisation</h4>

![Lighthouse - cancelled checkout - mobile after](testing-media/images/lighthouse-checkout-cancelled-mobile-after.png)

  <ul>
    <li><strong>Performance:</strong> 97</li>
    <li><strong>First Contentful Paint (FCP):</strong> 1.9s</li>
    <li><strong>Largest Contentful Paint (LCP):</strong> 2.2s</li>
    <li><strong>Total Blocking Time (TBT):</strong> 0ms</li>
    <li><strong>Cumulative Layout Shift (CLS):</strong> 0.048</li>
  </ul>

  <p>
    The optimisation reduced the page’s Largest Contentful Paint from 9.5s to 2.2s and improved the overall Performance score from 73 to 97. 
    Remaining Lighthouse suggestions relate primarily to global JavaScript and CSS efficiency rather than page-specific structural issues.
  </p>

</details>

<details>
<summary><strong>FAQ (core/faq.html)</strong></summary>

### Results

![Lighthouse - faq - mobile](testing-media/images/lighthouse-faq-mobile.png)

- **Performance:** 96  
- **Accessibility:** 100  
- **Best Practices:** 100  
- **SEO:** 100  

Key metrics:

- First Contentful Paint: 2.0s  
- Largest Contentful Paint: 2.4s  
- Total Blocking Time: 0ms  
- Cumulative Layout Shift: 0.017  
- Speed Index: 2.0s  

---

### Performance Overview

The FAQ page performs strongly on mobile devices, achieving a high performance score of 96 while maintaining perfect Accessibility, Best Practices, and SEO scores.

The Largest Contentful Paint of 2.4 seconds remains within Google’s “Good” threshold (≤ 2.5s), indicating that primary content loads quickly even under simulated mobile conditions.

Total Blocking Time remains at 0ms, demonstrating that the accordion-based FAQ interaction does not introduce responsiveness delays.

Layout stability is excellent, with a CLS of 0.017, well below the 0.1 threshold.

---

### Minor Lighthouse Suggestions

Lighthouse identified minor optimisation opportunities primarily related to shared project assets inherited from the base template:

- Render-blocking Bootstrap CSS (estimated 720ms savings)
- Reduce unused JavaScript from shared vendor bundles
- Minor CSS and JavaScript minification suggestions
- Generic long main-thread task warnings

These relate to global static assets rather than page-specific inefficiencies.

---

### Conclusion

The FAQ page demonstrates strong mobile performance with stable layout rendering and no blocking JavaScript issues.

Remaining Lighthouse suggestions are minor and relate to globally shared assets rather than structural or page-specific concerns. Overall, the page performs reliably and efficiently on mobile devices.

</details>

<details>
<summary><strong>Crisis & Support (pages/support.html)</strong></summary>

### Results

![Lighthouse - crisis & support - mobile](testing-media/images/lighthouse-crisis-mobile.png)

- **Performance:** 94  
- **Accessibility:** 100  
- **Best Practices:** 100  
- **SEO:** 100  

Key metrics:

- First Contentful Paint: 1.9s  
- Largest Contentful Paint: 2.2s  
- Total Blocking Time: 0ms  
- Cumulative Layout Shift: 0.118  
- Speed Index: 1.9s  

---

### Performance Overview

The Crisis & Support page performs strongly on mobile devices, maintaining perfect Accessibility, Best Practices, and SEO scores.

The Largest Contentful Paint of 2.2 seconds falls within Google’s “Good” threshold (≤ 2.5s), indicating that primary content loads quickly even under mobile network simulation.

Total Blocking Time remains at 0ms, demonstrating that page interactivity is not delayed by JavaScript execution.

The Performance score of 94 is slightly impacted by layout stability, with a CLS of 0.118. While slightly above the ideal 0.1 threshold, no disruptive visual shifts were observed during practical testing, and the page remains fully usable.

---

### Minor Lighthouse Suggestions

Lighthouse identified minor optimisation opportunities primarily related to shared global assets:

- Render-blocking Bootstrap CSS (estimated 750ms savings)
- Reduce unused JavaScript from shared vendor bundles
- Minor CSS and JavaScript minification suggestions
- Generic long main-thread task warnings

These relate to globally inherited resources from the base template rather than page-specific inefficiencies.

---

### Conclusion

The Crisis & Support page delivers fast, accessible, and stable mobile performance. While Lighthouse reports a slightly elevated CLS metric, real-world behaviour remains smooth and reliable.

Given the importance of support content, the page maintains high performance standards and full compliance across accessibility and SEO categories.

</details>

<details>
<summary><strong>Contact (pages/contact.html)</strong></summary>

### Results

![Lighthouse - contact - mobile](testing-media/images/lighthouse-contact-mobile.png)

- **Performance:** 94  
- **Accessibility:** 100  
- **Best Practices:** 100  
- **SEO:** 100  

Key metrics:

- First Contentful Paint: 1.9s  
- Largest Contentful Paint: 2.2s  
- Total Blocking Time: 0ms  
- Cumulative Layout Shift: 0.105  
- Speed Index: 1.9s  

---

### Performance Overview

The Contact page performs strongly on mobile devices, maintaining perfect Accessibility, Best Practices, and SEO scores.

The Largest Contentful Paint of 2.2 seconds remains within Google’s “Good” performance threshold (≤ 2.5s), indicating fast primary content rendering under mobile simulation.

Total Blocking Time remains 0ms, confirming that form interactivity and page responsiveness are not delayed by JavaScript execution.

The Performance score of 94 is primarily influenced by layout stability, with a CLS of 0.105. While slightly above the recommended 0.1 threshold, no disruptive layout behaviour was observed during manual testing, and the page remains fully usable.

---

### Minor Lighthouse Suggestions

Lighthouse identified minor optimisation opportunities primarily related to shared global assets inherited from the base template:

- Render-blocking Bootstrap CSS (estimated 810ms savings)
- Reduce unused JavaScript from shared vendor bundles
- Minor CSS and JavaScript minification suggestions
- Generic long main-thread task warnings

These relate to global static resources rather than page-specific structural issues.

---

### Conclusion

The Contact page demonstrates strong mobile performance with fast rendering, stable layout behaviour, and full compliance across accessibility and SEO categories. Remaining Lighthouse suggestions relate to globally shared assets and do not indicate functional concerns.

</details>

<details>
<summary><strong>Sign Up (account/signup.html)</strong></summary>

### Results

![Lighthouse - sign up - mobile](testing-media/images/lighthouse-signup-mobile.png)

- **Performance:** 97  
- **Accessibility:** 100  
- **Best Practices:** 100  
- **SEO:** 100  

Key metrics:

- First Contentful Paint: 1.9s  
- Largest Contentful Paint: 2.2s  
- Total Blocking Time: 0ms  
- Cumulative Layout Shift: 0.013  
- Speed Index: 1.9s  

---

### Performance Overview

The Sign Up page performs strongly on mobile, maintaining a fast first paint (1.9s) and a “Good” Largest Contentful Paint (2.2s, within the ≤ 2.5s threshold).  

Total Blocking Time remains 0ms, indicating the page stays responsive during load, and the low CLS score (0.013) confirms stable layout with no disruptive visual shifting.

---

### Minor Lighthouse Suggestions

Lighthouse flagged small optimisation opportunities that are mostly related to shared/global assets rather than issues specific to the Sign Up template:

- Render-blocking CSS (estimated 670ms savings)
- Reduce unused JavaScript from shared bundles
- Minor CSS/JS minification opportunities
- “Avoid long main-thread tasks” warnings (often caused by shared vendor scripts)
- Back/forward cache restoration prevented (typically linked to global scripts/event listeners)

These do not indicate functional issues and can be addressed later as part of broader project optimisation.

---

### Conclusion

The Sign Up page achieves excellent mobile results with full accessibility, best practice compliance, and SEO. Performance is comfortably within expected thresholds for an authentication flow, and layout stability remains strong.

</details>

<details>
<summary><strong>Login (account/login.html)</strong></summary>

### Results

![Lighthouse - login - mobile](testing-media/images/lighthouse-login-mobile.png)

- **Performance:** 97  
- **Accessibility:** 100  
- **Best Practices:** 100  
- **SEO:** 100  

Key metrics:

- First Contentful Paint: 1.9s  
- Largest Contentful Paint: 2.2s  
- Total Blocking Time: 10ms  
- Cumulative Layout Shift: 0.004  
- Speed Index: 1.9s  

---

### Performance Overview

The login page performs strongly on mobile devices, achieving near-perfect Lighthouse results.

The Largest Contentful Paint of 2.2 seconds remains within Google's “Good” threshold (≤ 2.5s), meaning primary content renders quickly even under simulated mobile network conditions.

Total Blocking Time is minimal at 10ms, indicating excellent responsiveness. Layout stability is also strong, with a CLS of 0.004 — effectively eliminating disruptive visual shifts during page load.

---

### Minor Lighthouse Suggestions

Lighthouse identified optimisation opportunities largely associated with shared project assets rather than the login template specifically:

- Render-blocking CSS (estimated 830ms potential savings)
- Minor CSS and JavaScript minification suggestions
- Reduce unused CSS/JavaScript from shared bundles
- Back/forward cache restoration limitation (likely due to global script behaviour)
- Occasional long main-thread tasks originating from vendor scripts

These are global performance considerations and do not negatively affect usability or accessibility of the login flow.

---

### Conclusion

The login page demonstrates strong mobile performance, full accessibility compliance, and excellent layout stability. Authentication interactions remain fast, responsive, and accessible across devices.

</details>

<details>
<summary><strong>Profile (account/profile.html)</strong></summary>

### Results

![Lighthouse - profile - mobile](testing-media/images/lighthouse-profile-mobile.png)

- **Performance:** 97  
- **Accessibility:** 100  
- **Best Practices:** 100  
- **SEO:** 100  

Key metrics:

- First Contentful Paint: 1.9s  
- Largest Contentful Paint: 2.2s  
- Total Blocking Time: 0ms  
- Cumulative Layout Shift: 0.002  
- Speed Index: 1.9s  

---

### Performance Overview

The Profile page performs strongly on mobile devices, achieving near-perfect Lighthouse scores.

The Largest Contentful Paint of 2.2 seconds remains within Google’s “Good” threshold (≤ 2.5s), ensuring that primary account content renders quickly even under simulated mobile conditions.

Total Blocking Time remains at 0ms, demonstrating that profile-related scripts and account data rendering do not introduce responsiveness delays. Layout stability is excellent, with a CLS of 0.002, meaning there are no noticeable visual shifts during load.

---

### Minor Lighthouse Suggestions

Lighthouse identifies optimisation opportunities largely associated with shared project assets:

- Render-blocking CSS (estimated 810ms savings)
- Reduce unused CSS and JavaScript from shared bundles
- Minor CSS/JS minification suggestions
- Occasional long main-thread task warnings from vendor scripts

These are global optimisation considerations and do not indicate issues specific to the profile template.

---

### Conclusion

The Profile page maintains excellent mobile performance, full accessibility compliance, and stable layout behaviour. Account management functionality remains fast, responsive, and reliable across devices.

</details>

<details>
<summary><strong>Change Username (account/change_username.html)</strong></summary>

### Results

![Lighthouse - change username - mobile](testing-media/images/lighthouse-change-username-mobile.png)

- **Performance:** 97  
- **Accessibility:** 100  
- **Best Practices:** 100  
- **SEO:** 100  

Key metrics:

- First Contentful Paint: 1.9s  
- Largest Contentful Paint: 2.2s  
- Total Blocking Time: 10ms  
- Cumulative Layout Shift: 0.004  
- Speed Index: 1.9s  

---

### Performance Overview

The Change Username page performs strongly on mobile, scoring **97 for performance** while achieving perfect results for accessibility, best practices, and SEO.

The **Largest Contentful Paint of 2.2s** is within Google’s “Good” threshold (≤ 2.5s), showing that primary content renders quickly even under Lighthouse’s simulated mobile network conditions.

Interactivity remains responsive, with **Total Blocking Time at just 10ms**, indicating that shared site scripts do not introduce noticeable delays on this page.

Layout stability is excellent, with a **CLS of 0.004**, meaning the interface remains visually stable during load.

---

### Minor Lighthouse Suggestions

Lighthouse highlighted minor opportunities that are typical in projects using shared global assets:

- Render-blocking CSS (estimated ~780ms savings), largely from shared vendor styles
- Minification suggestions for shared CSS and JavaScript
- Unused JavaScript reduction suggestions from shared bundles
- Generic “long main-thread task” warnings under simulated mobile load

These are not page-specific functional issues and can be treated as optional refinements.

---

### Conclusion

The Change Username page achieves near-perfect mobile performance while maintaining strong accessibility and best-practice compliance. Any remaining Lighthouse suggestions relate to shared assets and are optimisation opportunities rather than defects.

</details>

<details>
<summary><strong>Change Email (account/change_email.html)</strong></summary>

### Results

![Lighthouse - change email - mobile](testing-media/images/lighthouse-change-email-mobile.png)

- **Performance:** 97  
- **Accessibility:** 100  
- **Best Practices:** 100  
- **SEO:** 100  

Key metrics:

- First Contentful Paint: 1.9s  
- Largest Contentful Paint: 2.2s  
- Total Blocking Time: 0ms  
- Cumulative Layout Shift: 0.003  
- Speed Index: 1.9s  

---

### Performance Overview

The Change Email page performs strongly on mobile, with near-instant interactivity and stable layout rendering.

Largest Contentful Paint (2.2s) remains within the “Good” threshold (≤ 2.5s), meaning the main content becomes visible quickly even under simulated mobile network conditions.

Total Blocking Time stays at 0ms, confirming the page remains responsive while loading shared scripts and form logic.

Layout stability is excellent (CLS 0.003), indicating no visible shifting as content loads.

---

### Minor Lighthouse Suggestions

Lighthouse flagged small optimisation opportunities that are primarily related to global/shared assets rather than issues unique to this page:

- Render-blocking resources (Bootstrap/CSS) – estimated ~810ms savings  
- Modern HTTP delivery suggestions  
- Minor JS/CSS minification opportunities  
- Reduce unused JavaScript from shared bundles  
- Generic “long main-thread task” warnings under mobile simulation  

These do not prevent the page from achieving a high performance score and do not indicate functional problems.

---

### Conclusion

The Change Email page achieves excellent mobile Lighthouse results, maintaining strong performance alongside full accessibility, best-practice compliance, and SEO integrity.

</details>

<details>
<summary><strong>Change Password (account/password_change.html)</strong></summary>

### Results

![Lighthouse - change password - mobile](testing-media/images/lighthouse-change-password-mobile.png)

- **Performance:** 97  
- **Accessibility:** 100  
- **Best Practices:** 100  
- **SEO:** 100  

Key metrics:

- First Contentful Paint: 1.9s  
- Largest Contentful Paint: 2.2s  
- Total Blocking Time: 10ms  
- Cumulative Layout Shift: 0.01  
- Speed Index: 1.9s  

---

### Performance Overview

The Change Password page performs strongly on mobile devices, achieving a high performance score while maintaining perfect accessibility, best practice, and SEO results.

The Largest Contentful Paint of 2.2 seconds remains within Google’s “Good” threshold (≤ 2.5s), ensuring that the primary content becomes visible quickly even under simulated mobile network conditions.

Total Blocking Time is minimal at 10ms, confirming that shared scripts and password visibility toggle functionality do not meaningfully impact responsiveness.

Layout stability is excellent, with a CLS of 0.01 — well below the 0.1 threshold — meaning there are no disruptive visual shifts during load.

---

### Minor Lighthouse Suggestions

Lighthouse identified optimisation opportunities primarily related to shared global assets:

- Render-blocking CSS (estimated ~800ms savings)
- Modern HTTP delivery suggestions
- Minor CSS and JavaScript minification opportunities
- Reduce unused JavaScript from shared bundles
- Generic “long main-thread task” warnings under mobile simulation

These are global optimisation considerations rather than page-specific issues.

---

### Conclusion

The Change Password page delivers strong mobile performance with excellent layout stability and full accessibility compliance. Remaining Lighthouse suggestions relate to shared assets and can be treated as optional refinements.

</details>

<details>
<summary><strong>Password Reset (account/password_reset.html)</strong></summary>

### Results

![Lighthouse - password reset - mobile](testing-media/images/lighthouse-password-reset-mobile.png)

- **Performance:** 97  
- **Accessibility:** 100  
- **Best Practices:** 100  
- **SEO:** 100  

Key metrics:

- First Contentful Paint: 1.9s  
- Largest Contentful Paint: 2.2s  
- Total Blocking Time: 0ms  
- Cumulative Layout Shift: 0.049  
- Speed Index: 1.9s  

---

### Performance Overview

The Password Reset page performs strongly on mobile devices, achieving a high performance score while maintaining perfect accessibility, best practice, and SEO compliance.

The Largest Contentful Paint of 2.2 seconds remains within Google’s “Good” threshold (≤ 2.5s), ensuring the main content becomes visible quickly even under simulated mobile conditions.

Total Blocking Time is 0ms, confirming that the page remains fully responsive during load.

Cumulative Layout Shift is 0.049, well below the 0.1 threshold, indicating good visual stability with no disruptive layout movement.

---

### Minor Lighthouse Suggestions

Lighthouse highlights optimisation opportunities primarily related to shared global assets:

- Render-blocking CSS (estimated ~760ms savings)
- Modern HTTP delivery improvements
- Minor CSS and JavaScript minification opportunities
- Reduce unused JavaScript from shared bundles
- Generic “long main-thread task” warnings under mobile simulation

These are global optimisation considerations rather than page-specific issues.

---

### Conclusion

The Password Reset page demonstrates strong mobile performance, stable layout behaviour, and full compliance with accessibility and best-practice standards. Remaining Lighthouse suggestions relate to shared assets and can be treated as optional refinements.

</details>

<details>
<summary><strong>Password Reset Done (account/password_reset_done.html)</strong></summary>

### Results

![Lighthouse - password reset done - mobile](testing-media/images/lighthouse-password-reset-done-mobile.png)

- **Performance:** 97  
- **Accessibility:** 100  
- **Best Practices:** 100  
- **SEO:** 100  

Key metrics:

- First Contentful Paint: 1.9s  
- Largest Contentful Paint: 2.2s  
- Total Blocking Time: 0ms  
- Cumulative Layout Shift: 0.015  
- Speed Index: 1.9s  

---

### Performance Overview

The Password Reset Done confirmation page performs strongly on mobile, with fast visual rendering and excellent responsiveness.

Largest Contentful Paint is 2.2 seconds, which remains within Google’s “Good” threshold (≤ 2.5s), meaning the main confirmation content is displayed quickly even under simulated mobile network conditions.

Total Blocking Time is 0ms, confirming there are no JavaScript-related responsiveness delays on this page.

Layout stability is also solid, with a CLS score of 0.015 (well below the 0.1 threshold), indicating minimal movement during load.

---

### Minor Lighthouse Suggestions

Lighthouse flags a small number of generic optimisation opportunities that relate to shared global assets rather than this template specifically:

- Render-blocking requests (global CSS/vendor loading)
- Minor JavaScript minification / unused JavaScript suggestions
- Long main-thread task warnings under mobile simulation

---

### Conclusion

The Password Reset Done page delivers an excellent mobile experience with high performance, full accessibility compliance, and perfect best-practice and SEO scores. Any remaining Lighthouse suggestions are tied to shared site-wide assets rather than page-level issues.

</details>

<details>
<summary><strong>Password Reset From Key (account/password_reset_from_key.html)</strong></summary>

### Testing Environment Note

This page was tested **locally** rather than on the live deployed site.

The password reset confirmation route requires a valid, time-sensitive token generated via email. In the production environment, reset emails are not accessible for direct Lighthouse testing. When running locally, Django outputs reset emails to the terminal, allowing the secure reset link to be accessed for performance evaluation.

The template, styling, and static assets are identical between local and deployed environments, so the results are representative of production behaviour.

---

### Results (Local Environment)

![Lighthouse - password reset from key - mobile](testing-media/images/lighthouse-password-reset-form-key-mobile.png)

- **Performance:** 98  
- **Accessibility:** 100  
- **Best Practices:** 100  
- **SEO:** 100  

Key metrics:

- First Contentful Paint: 1.8s  
- Largest Contentful Paint: 2.0s  
- Total Blocking Time: 0ms  
- Cumulative Layout Shift: 0.012  
- Speed Index: 1.8s  

---

### Performance Overview

The Password Reset From Key page performs strongly on mobile, achieving a high performance score with excellent responsiveness.

Largest Contentful Paint (2.0s) is well within Google’s “Good” threshold (≤ 2.5s), meaning the main content is displayed quickly under simulated mobile network conditions.

Total Blocking Time remains 0ms, confirming that password validation logic and shared scripts do not delay interactivity.

Layout stability is strong, with a CLS of 0.012 — comfortably below the 0.1 threshold.

---

### Minor Lighthouse Suggestions

Lighthouse flags minor optimisation opportunities that relate to shared global assets:

- Render-blocking CSS (estimated ~870ms savings)
- Improve cache lifetimes for static assets
- Minor CSS and JavaScript minification suggestions
- Reduce unused CSS/JavaScript from shared bundles
- Generic long main-thread task warnings under mobile simulation

These are global optimisation considerations rather than page-specific issues.

---

### Conclusion

The Password Reset From Key page achieves excellent mobile Lighthouse results when tested locally. Local testing is appropriate due to the token-based access requirement of this route, and results reflect the deployed template and asset configuration.

</details>

<details>
<summary><strong>Password Reset From Key Done (account/password_reset_from_key_done.html)</strong></summary>

### Results (Local Testing)

![Lighthouse - password reset from key done - mobile](testing-media/images/lighthouse-password-reset-form-key-done-mobile.png)

- **Performance:** 98  
- **Accessibility:** 100  
- **Best Practices:** 100  
- **SEO:** 100  

Key metrics:

- First Contentful Paint: 1.8s  
- Largest Contentful Paint: 2.0s  
- Total Blocking Time: 0ms  
- Cumulative Layout Shift: 0.003  
- Speed Index: 1.8s  

---

### Performance Overview

This confirmation page performs strongly on mobile, with fast content rendering and stable layout behaviour.

The Largest Contentful Paint of 2.0s falls within Google’s “Good” threshold (≤ 2.5s), indicating that the primary page content becomes visible quickly even under simulated mobile conditions.

Total Blocking Time remains at 0ms, showing that the page does not introduce interactivity delays, and CLS is extremely low (0.003), meaning there is no noticeable layout movement during load.

---

### Minor Lighthouse Suggestions

Lighthouse flagged a small number of optimisation opportunities that relate to shared global assets rather than this specific template:

- Render-blocking CSS (estimated 770ms savings)
- Cache lifetime improvements (estimated 41 KiB)
- Minor CSS/JS minification suggestions
- Reduce unused CSS/JavaScript from shared bundles
- Generic long main-thread task warnings under mobile simulation

---

### Notes on Testing Environment

This page was tested **locally** rather than on the deployed Heroku site, because the password reset flow in the development environment outputs the reset link via the terminal, meaning the full reset-from-key journey cannot be reproduced end-to-end on the live deployment in the same way.

---

### Conclusion

The password reset confirmation page achieves near-perfect Lighthouse results on mobile, maintaining excellent performance, complete accessibility compliance, best practices alignment, and SEO readiness, while remaining stable and responsive across the reset journey.

</details>

<details>
<summary><strong>404 Error Page (404.html)</strong></summary>

### Results

![Lighthouse - 404 error page - mobile](testing-media/images/lighthouse-404-error-mobile.png)

- **Performance:** 97  
- **Accessibility:** 100  
- **Best Practices:** 96  
- **SEO:** 91  

---

### SEO Score Explanation

The reduced SEO score is expected for a 404 error page.

Lighthouse flags pages that return a non-200 HTTP status under the “Crawling and Indexing” audit. However, this page correctly returns an HTTP **404 status**, which is the proper and standards-compliant behaviour for a missing resource.

A 404 page should:
- Return HTTP 404  
- Not be indexed by search engines  
- Not appear in search results  

Therefore, the SEO score reduction is intentional and does not indicate an implementation issue.

---

### Best Practices Notes

Lighthouse reports:

- Browser errors logged to the console  
- Recommendations to implement CSP (Content Security Policy) and Trusted Types  

The console warning relates to a shared static asset or missing resource and is not caused by the 404 template itself.

CSP and Trusted Types suggestions are general security hardening recommendations and are not specific faults within this page.

---

### Performance Overview

Mobile performance remains strong, with stable layout behaviour and no accessibility issues. The page loads quickly and maintains full usability despite being an error state.

---

### Conclusion

The 404 page behaves correctly on mobile, returns the appropriate HTTP status code, and maintains strong accessibility and performance standards.

The reduced SEO score is expected behaviour for an error page and does not require corrective action.

</details>


[Back to contents](#contents)

Return to [README.md](../README.md)

---
## Wave Testing
---

After completing Lighthouse accessibility audits for all pages, a secondary manual accessibility review was conducted using the **WAVE Web Accessibility Evaluation Tool** (by WebAIM).

Each template was individually reviewed on both desktop and mobile viewports to ensure:

- No colour contrast errors
- No missing form labels
- No missing or incorrect ARIA attributes
- No structural or semantic alerts requiring attention
- Proper heading hierarchy
- Accessible button and link naming
- Sufficient touch target spacing
- No empty links or redundant alternative text

Particular attention was given to:
- Authentication pages (password toggles, labels, aria attributes)
- Form validation messaging
- Interactive elements such as buttons, links, and navigation
- Error pages (404 and 500)
- Dynamic content areas such as dashboard messaging

Any minor alerts identified during testing were reviewed and resolved where necessary to ensure consistent accessibility standards across the application.

Following Lighthouse and WAVE validation, no outstanding contrast errors, accessibility alerts, or missing ARIA labels remain.


[Back to contents](#contents)

Return to [README.md](../README.md)

---
## Responsiveness Testing
---

The site was tested across a range of common devices and screen sizes using Chrome DevTools (device emulation), manual browser resizing, and live testing in local and deployed environments. Particular attention was given to the sticky navbar and plan status banner to ensure correct stacking behaviour across breakpoints.

Following refinement of the sticky plan banner logic (dynamic `--navbar-height` sync via JavaScript), the banner now aligns precisely beneath the navbar at all tested viewport widths, including smaller mobile screens (e.g. 375px), with no visible gaps or overlap.

| Device / Screen Size | Result | Notes |
|----------------------|--------|-------|
| **Mobile – 360px (Galaxy)** | Pass | Entry form fully usable. Plan banner sits flush under navbar. No horizontal scrolling. |
| **Mobile – 375px (iPhone SE / Mini)** | Pass | Previously observed micro-gap resolved after syncing navbar height dynamically. Sticky elements stack correctly. |
| **Mobile – 390px–430px (iPhone 12/13/14)** | Pass | CTA buttons scale correctly. Slider and text areas remain accessible and readable. |
| **Tablet – 768px (iPad Mini)** | Pass | Layout expands cleanly. Cards widen appropriately. Navbar remains stable. |
| **Laptop – 1366px** | Pass | Content centred with correct max-width constraints. No stretching. |
| **Desktop – 1920px** | Pass | Hero, intro, and dashboard layouts remain balanced. No visual misalignment. |

All pages were verified to maintain:

- Fully readable typography across breakpoints  
- Proper tap-target sizing on mobile  
- Correct stacking of form labels and inputs  
- Functional mood hue slider on small screens  
- Responsive Regulate+ CTA and dashboard controls  
- Navbar collapse behaviour working correctly  
- Sticky navbar and plan banner alignment with no overlap or visible seam  

Critical checks:

- ☑ Entry form usable on mobile  
- ☑ Emotion list scroll behaves correctly  
- ☑ Regulate+ CTA responsive  
- ☑ Navbar collapses correctly  
- ☑ Plan status banner remains flush beneath navbar at all tested widths  

Evidence:

![Testing responsive video](testing-media/gifs/testing-adaptive.gif)

[Back to contents](#contents)

Return to [README.md](../README.md)

---
## Browser Compatibility Testing
---

The site was manually tested across the five major browsers on both desktop and mobile devices.

All core functionality — including user authentication (Django Allauth), entry creation and editing, subscription logic and usage limits, Stripe checkout flows, search functionality, dashboard status updates, and responsive layout behaviour — performed consistently with no visual or functional discrepancies.

Because the project uses standard HTML5, CSS3, JavaScript, Django templates, and Bootstrap components (without unsupported experimental APIs), full browser compatibility was achieved without requiring browser-specific overrides or polyfills.

| Browser               | Version Tested | Result | Notes |
|-----------------------|----------------|--------|-------|
| **Google Chrome**     | Latest         | ✅ Pass | Fully functional — authentication, entry creation, search, Stripe checkout, and dashboard counters operate correctly. |
| **Safari (iOS)**      | Latest iOS     | ✅ Pass | Responsive layout behaves as expected. Forms, entry editing, and navigation render correctly. |
| **Mozilla Firefox**   | Latest         | ✅ Pass | All JavaScript interactions (dynamic counters, supportive phrases, conditional UI elements) function correctly. |
| **Microsoft Edge**    | Latest         | ✅ Pass | No rendering issues. Subscription flow and authentication behave identically to Chrome. |
| **Samsung Internet**  | Latest         | ✅ Pass | Mobile navigation, entry submission, and search features perform without layout or interaction bugs. |

[Back to contents](#contents)

Return to [README.md](../README.md)

---
## User Story Testing
---

### User Story Testing Summary

All implemented user stories were tested against their acceptance criteria in both local development and the deployed production environment. All must-have functionality — including authentication, entry creation, emotion word selection, timeline display, revision history, subscription gating, and free-tier limits — behaved as expected.

The application correctly enforces ownership rules (users can only access their own entries), preserves revision history during edits, and restricts feature access when free-tier limits are reached. Stripe subscription logic, trial enforcement, and webhook updates were tested to confirm correct status transitions (trial, active, grace, expired).

Should-have stories, including keyword search and announcement dismissal logic, were also tested and function correctly without introducing performance or UX issues.

Could-have stories were intentionally not implemented at this stage to maintain scope control and ensure stability of the core emotional tracking functionality. The system architecture allows these features to be added in future iterations without significant refactoring.

Overall, every implemented story passed testing successfully and meets its documented acceptance criteria.

---

| User Story | What Was Done / How It Was Achieved | Pass/Fail |
|------------|-------------------------------------|-----------|
| **1. User Registration** | Configured Django Allauth with custom templates. Form validation tested. Password hashing confirmed. Invalid inputs show accessible errors. Successful registration creates secure user record. | ✅ Pass |
| **2. User Login & Logout** | Login redirects to dashboard. Invalid credentials display errors. Logout clears session and restricts access to protected routes. Navbar updates dynamically based on authentication state. | ✅ Pass |
| **3. Create Mood Entry** | Hue slider required. Optional notes and hue meaning save correctly. Multiple entries per day supported. Timestamp auto-generated. Success feedback displayed after submission. | ✅ Pass |
| **4. Emotion Word Selection** | EmotionWord model implemented. Multiple selections saved via ManyToMany relationship. Selected words display correctly on detail page. Filtering UI functions as expected. | ✅ Pass |
| **5. Timeline View (No Calendar)** | Entries grouped by date and ordered chronologically. Only dates containing entries are displayed. No calendar or streak indicators present. | ✅ Pass |
| **6. Edit Entry With Revision History** | EntryRevision model stores previous state before update. Only entry owner can edit. Revision history displays correctly on detail view. | ✅ Pass |
| **7. Delete Entry Safely** | Delete view restricted to entry owner. Confirmation required. Entry permanently removed. Redirect functions correctly. | ✅ Pass |
| **8. Filter Entries by Date** | Date query parameter validated. Only matching entries returned. No empty date groups shown. | ✅ Pass |
| **9. Dashboard Overview** | Dashboard displays subscription status, entry count, and limit usage. Context updates dynamically based on user plan. | ✅ Pass |
| **10. Supportive Phrases** | Phrase endpoint tested. JavaScript fetch updates phrase. Local fallback triggers correctly if external request fails. | ✅ Pass |
| **11. Access Support Resources** | Support page created with UK-based resources. External links verified. Language reviewed for clarity and safeguarding tone. | ✅ Pass |
| **12. Contact Form / Support Tickets** | SupportTicket model stores submissions. Logged-in users auto-linked. Logged-out users required to provide email. Validation tested. | ✅ Pass |
| **A. Free Tier With Limits** | Free users limited to 10 entries. Creation, edit, and delete lock correctly when limit reached. Viewing existing entries remains accessible. | ✅ Pass |
| **B. Trial Abuse Prevention** | Trial usage stored persistently. Users cannot restart expired trial. Webhook logic updates subscription status correctly. | ✅ Pass |
| **C. Privacy-Focused Admin** | Entry and revision models removed from admin browsing. Support tickets and subscription models manageable. Admin branding customised. | ✅ Pass |
| **13. Keyword Search (Should-have)** | Search filters notes and emotion words. Only matching entries returned. No false positives observed. | ✅ Pass |
| **14. Announcement Awareness (Should-have)** | Announcements display only when active. Dismissal persists via local storage/session logic. | ✅ Pass |
| **15–16 / D–E (Could-have)** | Export, visualisation, referral discounts, and international expansion intentionally not implemented to maintain scope and stability. | ➖ Not Included |

---

No critical bugs were identified during user story testing. All implemented functionality works as designed in both development and deployed environments.

[Back to contents](#contents)

Return to [README.md](../README.md)

---
## Feature Interaction Testing
---

### Feature Interaction Summary

All interactive elements of Regulate were manually tested in both local development and the deployed production environment. Particular attention was given to:

- Emotional data integrity  
- Subscription gating logic  
- Stripe checkout state transitions  
- Defensive UX behaviour  
- Accessibility and mobile responsiveness  

All implemented interactive features behaved consistently and as designed.

| Area Tested | What Was Checked | Result |
|-------------|------------------|--------|
| **Forms** | Validation, inline errors, required fields, plan-based restrictions, CSRF protection, accessibility labels | ✅ Pass |
| **Buttons** | Entry creation/edit/delete behaviour, subscription gating, confirmation prompts, hover/active states | ✅ Pass |
| **Links & Navigation** | Authentication redirects, plan-based visibility, password reset flow, external support links | ✅ Pass |
| **Business Logic** | Free-tier locking, trial enforcement, revision logic, subscription state transitions | ✅ Pass |
| **Stripe (Test Mode)** | Checkout success, cancellation flow, webhook sync, billing portal access | ✅ Pass |

### Feature Interaction Full Details (collapsible)

These tests were performed to ensure that all interactive components behave predictably, securely, and in alignment with the project’s trauma-informed UX goals.

<details>
<summary><strong>Forms</strong></summary>

All user-facing forms were manually tested using both valid and invalid inputs.

Tested forms include:

- Sign up  
- Sign in  
- Password reset request  
- Change username/email/password  
- Create entry  
- Edit entry  
- Support ticket form  

Validation checks confirmed:

- Required fields block submission when empty  
- Password mismatch and strength validation works correctly  
- Duplicate email/username errors display inline  
- Free-plan lock prevents submission when limit reached  
- CSRF protection present on all POST forms  
- Error messages are human-readable and non-technical  
- Success messages display correctly via Django messages framework  

Accessibility checks confirmed:

- All inputs have associated labels  
- ARIA attributes applied appropriately  
- Focus states visible  
- Mobile keyboard behaviour correct for email/password inputs  

All forms redirect appropriately on successful submission and preserve user data on validation failure.

</details>

<details>
<summary><strong>Buttons</strong></summary>

All buttons were tested for correct backend interaction and frontend feedback.

Tested interactions include:

- “Create Entry”  
- “Edit”  
- “Delete”  
- “Start Free Trial”  
- “Upgrade to Regulate+”  
- “Manage Billing”  
- “Refresh Supportive Phrase”  
- Announcement dismissal  
- Logout  

Manual testing confirmed:

- Buttons trigger correct backend view logic  
- Free-tier lock disables edit/delete buttons when appropriate  
- Delete includes JavaScript confirmation prompt  
- No duplicate form submissions occur  
- Hover and active states display correctly  
- Buttons are touch-friendly on mobile  
- No visual misalignment or layout shift  

Special check:

When free-plan limit is reached:
- Create/edit/delete buttons become inactive  
- Clear informational message appears  
- Navigation to Regulate+ page functions correctly  

All button behaviours passed testing.

</details>

<details>
<summary><strong>Links & Navigation</strong></summary>

Navigation was tested across authenticated and non-authenticated states.

Tested links include:

- Navbar (signed-in and signed-out variations)  
- Dashboard links  
- Entries page links  
- Profile management links  
- Regulate+ link  
- Footer links (FAQ, Crisis & Support, Contact)  
- Password reset full flow  
- Stripe redirect return URLs  

Testing confirmed:

- Auth-protected pages redirect unauthenticated users to login  
- Post-login redirects function correctly  
- Plan-based navigation updates dynamically  
- External support links open safely  
- No broken, circular, or orphaned routes  
- Persistent plan status banner displays consistently  

404 and 500 custom pages were also tested to confirm safe fallback behaviour without exposing debug information.

All navigation behaved predictably across desktop and mobile devices.

</details>

<details>
<summary><strong>Business Logic & Access Control</strong></summary>

Core system rules were manually tested to confirm correct enforcement.

Free-tier logic:

- Free users limited to 10 entries  
- Entry creation blocked after limit  
- View access always preserved  
- Deleting an entry restores create/edit access  
- Informational messaging clearly explains lock  

Trial enforcement:

- Free trial can only be used once per user  
- Attempted reuse displays informative message  
- Subscription state updates after Stripe webhook confirmation  

Revision logic:

- Editing an entry creates revision snapshot only when changes occur  
- Submitting unchanged data does not create redundant revision  
- Revision history displays accurately  

Data ownership:

- Users cannot access or modify other users’ entries  
- URL tampering returns 404 or permission denial  

Edge-case handling:

- Stripe webhook delay messaging displays when applicable  
- Billing portal fallback safely handled if Stripe customer ID missing  
- Supportive phrase API fallback triggers silently without user-facing error  

All business rules functioned as designed.

</details>

<details>
<summary><strong>Stripe (Test Mode)</strong></summary>

Stripe was tested exclusively in Test Mode using official Stripe test cards.

Tested flows:

- Successful trial activation  
- Successful subscription activation  
- Checkout cancellation  
- Return URL redirects  
- Webhook status synchronisation  
- Billing portal access  

Confirmed behaviours:

- Successful checkout updates subscription state  
- Cancelled checkout results in no subscription changes  
- Informational banner displays after cancellation  
- Webhook events update local subscription model  
- Manage Billing button redirects to Stripe Customer Portal  
- No card details stored in Django application  

Security validation:

- SECRET_KEY and Stripe keys stored in environment variables  
- No payment data logged in application  
- Subscription metadata stored locally without financial data  

All subscription transitions and payment flows behaved as expected in the sandbox environment.

</details>

No interactive feature produced critical errors during testing.  
All implemented components operate securely, predictably, and in accordance with the project’s architectural and UX goals.

[Back to contents](#contents)

Return to [README.md](../README.md)

---
## Admin Area Security Testing
---

### Admin Area Security Summary

Regulate handles highly sensitive wellbeing data, so admin security was tested not only for access control, but also for **privacy-by-design**. The Django admin interface is restricted to staff/superusers, and the system is intentionally configured so that **emotional entry content is not browsable via admin at all**.

The following checks confirm:

- Non-staff users cannot access `/admin/`  
- Privileged access follows least-privilege principles  
- State-changing actions are CSRF-protected  
- Destructive actions require explicit confirmation  
- Sensitive emotional content (entries/revisions/notes) is structurally excluded from admin  

| Security Check | Description | Status |
|----------------|-------------|--------|
| **Admin restricted** | `/admin/` is blocked for non-staff users (redirect/403) | ✅ Pass |
| **Staff-only visibility** | Only operational models are visible (Users, Groups, Subscriptions, Emotion Words, Announcements, Support Tickets) | ✅ Pass |
| **Sensitive models excluded** | Entry / EntryRevision (and any emotional content) are not registered in admin and cannot be browsed | ✅ Pass |
| **Ownership enforced (app-level)** | Users cannot view/edit/delete other users’ entries via URL manipulation or requests | ✅ Pass |
| **CSRF protection** | CSRF tokens present on all POST forms (auth, contact, entry actions, profile changes) | ✅ Pass |
| **Confirmation prompts** | Deletion actions require confirmation (UI prompt for entry deletion + Django admin confirmations) | ✅ Pass |
| **Secrets protected** | Stripe keys / SECRET_KEY stored in environment variables; not exposed in templates or repo | ✅ Pass |

### Admin Area Security Full Details (collapsible)

<details>
<summary><strong>Admin access restriction (/admin/)</strong></summary>

The `/admin/` route was tested while:

- logged out
- logged in as a standard authenticated user (non-staff)
- logged in as a staff user / superuser

Results:

- Logged-out users cannot access `/admin/` without authentication
- Non-staff authenticated users are blocked from admin access (redirect or permission denied)
- Only staff/superusers can access Django admin pages

This prevents unauthorised access to operational models and protects administrative controls.

</details>

<details>
<summary><strong>Least-privilege model visibility</strong></summary>

Admin was reviewed to confirm that only models required for operational maintenance are exposed.

Visible/admin-manageable models include:

- Users
- Groups
- Subscriptions (metadata only)
- Emotion Words
- Site Announcements
- Support Tickets

This aligns the admin interface with the project’s privacy requirements and reduces the risk of accidental exposure of emotional content.

</details>

<details>
<summary><strong>Privacy-by-design: emotional content excluded from admin</strong></summary>

To protect user privacy, emotionally sensitive models are intentionally excluded from the admin interface.

Confirmed:

- Mood entries are not registered in admin
- Entry revision history is not registered in admin
- Emotional notes, hue meanings, and entry-linked emotion selections are not browsable in admin

This is an architectural safeguard — not just a policy — ensuring that even staff users cannot casually browse personal emotional reflections through the admin UI.

</details>

<details>
<summary><strong>Ownership enforcement (user data protection)</strong></summary>

Protected routes were tested by attempting to access or modify another user’s data via:

- direct URL guessing / tampering
- changing primary keys in routes
- submitting requests for objects not owned by the session user

Results:

- The application prevents reading, editing, or deleting entries not owned by the logged-in user
- Where applicable, requests return a safe response (404/permission denied)
- No user can access another user’s emotional content through the UI or by manipulation

</details>

<details>
<summary><strong>CSRF protection and safe POST handling</strong></summary>

All state-changing actions were confirmed to use POST requests protected by CSRF tokens, including:

- authentication flows
- profile updates
- support ticket submissions
- entry creation/edit/delete actions
- subscription-related actions where applicable

This prevents cross-site request forgery and ensures requests are intentionally user-initiated.

</details>

<details>
<summary><strong>Confirmation gates for destructive actions</strong></summary>

Deletion and destructive actions were tested to ensure they cannot occur accidentally.

Confirmed:

- Entry deletion requires explicit confirmation (client-side confirmation + server-side POST handling)
- Django admin destructive actions use built-in confirmation screens (bulk delete, etc.)
- Locked plan states prevent restricted actions (free-tier lock disables edit/delete where required)

This supports both security and trauma-informed UX by preventing accidental loss of sensitive personal data.

</details>

<details>
<summary><strong>Billing security and secret management</strong></summary>

Stripe integration was reviewed to confirm that:

- no payment details are stored or processed by Regulate
- only subscription metadata is stored locally
- Stripe keys and Django SECRET_KEY are stored as environment variables
- secrets are not exposed in templates, commits, or error pages

This ensures payment security and prevents leakage of credentials.

</details>

[Back to contents](#contents)

Return to [README.md](../README.md)

---
## Error Handling
---

### Error Handling Summary Table

| Error Type | Behaviour | Result |
|------------|-----------|--------|
| 404 | Custom 404 template renders | Pass |
| 500 | Custom 500 template renders | Pass |


### Error Handling Full Details (collapsible example)

<details>
<summary><strong>404 Error Handling Test</strong></summary>

**Test Procedure:**

1. Set `DEBUG = False` locally.
2. Visited a non-existent URL (e.g. `/this-page-does-not-exist/`).
3. Confirmed that Django did not display the default debug page.
4. Verified that the custom `404.html` template rendered instead.

**Expected Result:**

- Custom styled 404 page displays.
- Page includes site branding and navigation.
- No Django debug traceback visible.

**Actual Result:**

- Custom `404.html` rendered successfully.
- No console errors.
- Template validated against live rendered HTML.

**Status:** Pass

</details>

<details>
<summary><strong>500 Error Handling Test</strong></summary>

**Test Procedure:**

1. Set `DEBUG = False` locally.
2. Created a temporary test view that intentionally raised an exception:
   `raise Exception("Test 500 error")`
3. Navigated to the test route (e.g. `/test-500/`).
4. Confirmed that Django rendered the custom `500.html` template.

**Expected Result:**

- Custom styled 500 page displays.
- No Django debug traceback shown.
- Page remains branded and user-friendly.

**Actual Result:**

- Custom `500.html` rendered correctly.
- No debug information exposed.
- Layout and navigation loaded as expected.

Temporary test route was removed after verification.

**Status:** Pass

</details>

[Back to contents](#contents)

Return to [README.md](../README.md)

---
## Security Testing
---

### Security Testing Summary

Because Regulate handles private emotional wellbeing data and subscription billing metadata, security was tested across authentication, authorisation, request handling, environment configuration, and production safeguards.

All core security mechanisms behaved as expected in both local and deployed environments.

| Security Area | What Was Tested | Result |
|---------------|----------------|--------|
| **Authentication protection** | Login required for dashboard, entries, profile, Regulate+ | ✅ Pass |
| **Authorisation checks** | Users cannot access or modify other users’ data | ✅ Pass |
| **CSRF protection** | All POST forms include CSRF tokens | ✅ Pass |
| **Environment variables** | SECRET_KEY and Stripe keys stored outside repo | ✅ Pass |
| **Production settings** | DEBUG=False, custom 404/500 pages active | ✅ Pass |
| **Sensitive data exposure** | No emotional data exposed via admin or API | ✅ Pass |
| **Stripe security** | No card data stored in Django app | ✅ Pass |

### Security Testing Details

<details>
<summary><strong>Authentication protection</strong></summary>

- Unauthenticated users attempting to access protected routes are redirected to login.  
- Session cookies behave correctly.  
- Logout invalidates session.  

</details>

<details>
<summary><strong>Authorisation checks</strong></summary>

- URL tampering does not allow access to another user’s entries.  
- Ownership enforced at query level.  
- Invalid object access returns safe response.  

</details>

<details>
<summary><strong>CSRF protection</strong></summary>

- All state-changing forms verified to include `{% csrf_token %}`.  
- POST requests without valid token are rejected.  

</details>

<details>
<summary><strong>Environment variables</strong></summary>

- SECRET_KEY not hardcoded.  
- Stripe API keys stored in environment variables.  
- `.env` excluded from version control.  

</details>

<details>
<summary><strong>Production configuration</strong></summary>

- `DEBUG = False` in deployment.  
- Django debug traceback not exposed.  
- Custom 404 and 500 pages render instead of stack traces.  

</details>

<details>
<summary><strong>Sensitive data exposure</strong></summary>

- Mood entries and revision history are not registered in the Django admin interface.  
- Admin users cannot browse emotional notes or personal reflections.  
- Entry queries are always filtered by the authenticated user.  
- Direct URL manipulation does not expose other users’ data.  
- No emotional data is returned via public endpoints or unauthenticated views.  
- Debug mode is disabled in production, preventing accidental data leakage via stack traces.  

</details>

<details>
<summary><strong>Stripe handling</strong></summary>

- Payment data handled exclusively by Stripe.  
- Only subscription metadata stored locally.  
- Webhooks validate subscription state without exposing financial data.  

</details>

[Back to contents](#contents)

Return to [README.md](../README.md)

---
## UX Improvements Identified During Testing
---

During manual walkthrough testing of the entry creation flow, it was identified that the **New Entry** page did not provide a clear navigation path back to the user’s entry list without using the browser back button.

This was considered poor UX because:
- Users could feel “trapped” on the form
- There was no explicit cancel/return action
- It did not align with the calm, low-pressure design intent of Regulate

### Fix Implemented

A clear return link was added beneath the form submission controls:

```html
<!-- Cancel and return to entries -->
<div class="entry-actions justify-content-center">
    <a href="{% url 'my_entries' %}">
        Cancel and return to your entries
    </a>
</div>
```

### Result

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

Tests are written to validate both business logic and user-facing behaviour.  
Where appropriate, tests simulate real user interaction by sending HTTP requests to views and inspecting responses, context data, and database changes.

The test suite validates:

- Subscription plan detection and banner rendering  
- Free plan entry limits and gating logic  
- Authentication requirements  
- User ownership and permission controls  
- Revision logic  
- Deletion behaviour under free plan limits  
- Keyword search functionality  
- Account validation rules (duplicate username protection)  
- Regulate+ subscription context behaviour  

[Back to contents](#contents)

Return to [README.md](../README.md)

---

### Running Tests

From the project root:

    python manage.py test -v 3

Latest successful output:

    Ran 19 tests in 11.672s
    OK

(All tests passing)

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

    accounts/tests.py
        - Username change validation tests

    billing/tests.py
        - Regulate+ subscription context tests

This structure keeps tests close to their related application logic and demonstrates systematic coverage across the project.

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
| Regulate+ context flags set correctly | Subscription state reflected in view context | Passed |

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
| Duplicate username rejected | Account validation prevents conflicts | Passed |

[Back to contents](#contents)

Return to [README.md](../README.md)

---

### Test-Driven Development Evidence

Several features were implemented using a test-first (Red → Green) workflow. This is traceable in the commit history.

![Commit history](testing-media/images/commit-history.png)

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
Users with a future `trial_end` date are not treated as locked.

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
| Total tests | 19 |
| Passed | 19 |
| Failed | 0 |
| Errors | 0 |

All automated tests pass successfully.

[Back to contents](#contents)

Return to [README.md](../README.md)

---

### Technical Note

The production environment uses WhiteNoise manifest storage.  
During testing, Django falls back to standard static storage to avoid manifest lookup errors and allow template rendering without requiring `collectstatic`.

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
