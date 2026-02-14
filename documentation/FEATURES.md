# Features
----------

This document provides a complete, structured breakdown of all functionality within **Regulate**.

It outlines:

- Core user-facing features  
- Subscription behaviour and plan logic  
- Billing and Stripe integration  
- Administrative controls  
- Privacy safeguards  
- Error handling and system messaging  
- UX design decisions and architectural considerations  

Each section explains not only *what* the feature does, but also *why* it was designed that way — with particular focus on emotional safety, low cognitive load, and mobile-first accessibility.

This file serves as the authoritative reference for how Regulate functions at both user and system level.


Return to [README.md](../README.md)

----------
## Contents
----------

1. [Navigation & Account Access](#navigation--account-access)
    - [Primary navigation](#primary-navigation)
    - [Persistent account status](#persistent-account-status)

2. [Home / Landing Page](#home--landing-page)
    - [Introductory video](#introductory-video)
    - [Adaptive content based on authentication](#adaptive-content-based-on-authentication)

3. [Sign In Page](#sign-in-page)
    - [Layout & presentation](#layout--presentation)
    - [Authentication inputs](#authentication-inputs)
    - [Password visibility (SVG eye feature)](#password-visibility-svg-eye-feature)
    - [Behaviour & security](#behaviour--security)

4. [Password Reset (Forgot Password)](#password-reset-forgot-password)
    - [Requesting a reset](#requesting-a-reset)
    - [Email delivery (project configuration)](#email-delivery-project-configuration)
    - [Secure reset flow](#secure-reset-flow)
    - [Setting a new password](#setting-a-new-password)

5. [Sign Up Page](#sign-up-page)
    - [Account creation inputs](#account-creation-inputs)
    - [Validation & feedback](#validation--feedback)
    - [Plan onboarding](#plan-onboarding)

6. [Mood Entry System](#mood-entry-system)
    - [Mood Hue Slider](#mood-hue-slider)
    - [Emotion Words](#emotion-words)

7. [Dashboard](#dashboard)
    - [Entry Overview & Plan Status](#entry-overview--plan-status)
    - [Creating Entries](#creating-entries)
    - [Browsing & Managing Entries](#browsing--managing-entries)
        - [Search & Filtering](#search--filtering)
        - [Grouped Date Accordion Layout](#grouped-date-accordion-layout)
        - [Entry Summary Display](#entry-summary-display)
        - [Viewing Entry Details](#viewing-entry-details)
        - [Editing Entries](#editing-entries)
        - [Deleting Entries](#deleting-entries)
    - [Supportive Phrases (External API Integration)](#supportive-phrases-external-api-integration)
    - [Site Announcements](#site-announcements)

8. [Regulate+ Page](#regulate-page)
    - [Dynamic Plan State Behaviour](#dynamic-plan-state-behaviour)
        - [When on the Free Plan](#when-on-the-free-plan)
        - [When on Free Trial or Active Subscription](#when-on-free-trial-or-active-subscription)
    - [Access Control & Feature Impact](#access-control--feature-impact)

9. [Payment Processing & Stripe Integration](#payment-processing--stripe-integration)
    - [Checkout Flow](#checkout-flow)
    - [Cancelled Checkout Handling](#cancelled-checkout-handling)
    - [Subscription State Management](#subscription-state-management)
    - [Free Trial Logic](#free-trial-logic)
    - [Stripe Test Mode (Academic Project Notice)](#stripe-test-mode-academic-project-notice)
    - [Stripe Checkout Customisation](#stripe-checkout-customisation)
    - [Trial & Billing Transparency](#trial--billing-transparency)
    - [Security & Data Handling](#security--data-handling)
    - [Technical Architecture](#technical-architecture)
    - [Academic Integrity & Development Approach](#academic-integrity--development-approach)

10. [Profile Page (Account Management)](#profile-page-account-management)
    - [Account Overview](#account-overview)
    - [Change Username](#change-username)
    - [Change Email Address](#change-email-address)
    - [Change Password](#change-password)
    - [Logout](#logout)

11. [Footer Navigation](#footer-navigation)
    - [FAQ](#faq)
    - [Crisis & Support Resources](#crisis--support-resources)
    - [Contact & Feedback](#contact--feedback)
    - [Back to top](#back-to-top)

12. [User Feedback & System Messaging](#user-feedback--system-messaging)
    - [Success Messages](#success-messages)
    - [Error Messages](#error-messages)
    - [Informational Messages](#informational-messages)
    - [Defensive UX & Edge Case Handling](#defensive-ux--edge-case-handling)
    - [Design & Accessibility Considerations](#design--accessibility-considerations)
    - [Architectural Approach](#architectural-approach)

13. [Custom Error Pages](#custom-error-pages)
    - [404 Page Not Found](#404-page-not-found)
    - [500 Server Error](#500-server-error)
    - [Security & Production Behaviour](#security--production-behaviour)

14. [Admin Dashboard & Operational Controls](#admin-dashboard--operational-controls)
    - [Django Administration Interface](#django-administration-interface)
    - [Groups](#groups)
    - [Users](#users)
    - [Billing Management](#billing-management)
    - [Admin Emotion Words](#admin-emotion-words)
    - [Admin Site Announcements](#admin-site-announcements)
    - [Support Tickets](#support-tickets)
    - [Models Intentionally Excluded from Admin](#models-intentionally-excluded-from-admin)
    - [Privacy & Security Safeguards](#privacy--security-safeguards)


[Back to contents](#contents)

Return to [README.md](../README.md)

---

## Navigation & Account Access

Regulate uses a clean, responsive navigation system that adapts to both authentication state and screen size, ensuring the interface remains simple, predictable, and low-effort across devices.

---

### Primary navigation

When not signed in, users can:

- Access the home page  
- Log in  
- Create an account  

When signed in, users can:

- Access the dashboard  
- View their entries  
- Create a new entry  
- Manage account and billing details  
- Log out securely  

These links focus only on **core actions**, keeping the interface minimal and reducing cognitive load during emotionally difficult moments.

---

### Persistent account status

When authenticated, a **persistent account status banner** is displayed directly beneath the navigation bar across all pages.

This banner clearly tells the user their current plan:
- Free
- Regulate+ Free Trial
- Regulate+ Subscription  

Keeping this information consistently visible prevents surprises and removes the need for users to search for account details.

---

**UX considerations:**

- Mobile-first layout with touch-friendly targets  
- Minimal, task-focused navigation to reduce cognitive load  
- Clear distinction between authenticated and non-authenticated states  
- Consistent placement and behaviour across all pages  
- Persistent, low-pressure visibility of account status  

[Back to contents](#contents)

Return to [README.md](../README.md)

---

## Home / Landing Page

The home page is designed to be a **calm, welcoming first touchpoint** that introduces the purpose and tone of Regulate before any interaction is required.

Rather than presenting dashboards or data immediately, the page focuses on reassurance, safety, and approachability.

---

### Introductory video

A short, lightweight background video plays automatically on first visit.

The video shows a person resting in bed and casually using their phone, subtly communicating that Regulate can be used:

- anywhere  
- at any time  
- without preparation or pressure  

The sequence ends on a still frame of the user appearing calm and settled, reinforcing the idea of emotional safety and self-reflection.

To avoid distraction or sensory fatigue:

- The video plays only once, upon landing on the page
- It does not loop continuously  
- The final frame remains static  

A Regulate logo and the tagline **“Feel. Reflect. Regulate.”** are overlaid to establish brand identity without overwhelming the screen.

---

### Adaptive content based on authentication

The page content adapts depending on whether the user is signed in.

This ensures returning users can act quickly, while new visitors receive context and reassurance.

**When signed in:**

- Welcome message using their username, for a personalised touch
- Gentle prompt to check in emotionally  
- Quick access **“Start a new entry”** button  

This reduces friction and allows users to begin logging immediately.

**When not signed in:**

- Clear explanation of Regulate’s purpose  
- Emphasis on low pressure and optional input  
- Reassurance that there are no streaks, scores, or expectations  
- Quick access buttons to **Sign in** or **Sign Up**  

Language intentionally avoids productivity or performance framing, instead focusing on self-compassion and autonomy.

---

**UX considerations:**

- Calm, minimal layout  
- Soft visual tone and low cognitive load  
- No forced interaction before understanding the product  
- Personalised experience for returning users  
- Quick access to primary actions  
- Avoids aggressive marketing or urgency tactics  

The landing page sets the emotional tone for the entire application, helping users feel safe, supported, and unhurried before they begin reflecting on their wellbeing.

[Back to contents](#contents)

Return to [README.md](../README.md)

---

## Sign In Page

The sign-in page is designed to be **simple, calm, and low effort**, allowing users to access their private space quickly without unnecessary friction or visual noise.

Rather than presenting dense forms or complex options, the interface focuses only on the essentials required for secure authentication.

---

### Layout & presentation

The page uses a centred card layout with soft colours, rounded edges, and generous spacing to maintain visual clarity and emotional comfort.

This approach:

- Reduces cognitive load  
- Keeps attention focused on a single task  
- Avoids overwhelming users during potentially vulnerable moments  

Brand elements remain present but subtle, with the Regulate logo and consistent colour palette reinforcing familiarity and trust.

---

### Authentication inputs

Users can sign in using:

- Username or email  
- Password  

Additional helpers include:

- **SVG password visibility toggle (eye icon)** to reveal or hide the password  
- “Keep me signed in on this device” option  
- Forgotten password recovery link  
- Quick link to create a new account  

Only essential information is requested, minimising effort and reducing barriers to entry.

---

### Password visibility (SVG eye feature)

To improve usability and accessibility, the password field includes a **custom SVG eye icon** that allows users to toggle password visibility.

This small interaction helps:

- Prevent typing mistakes  
- Reduce repeated login attempts  
- Support mobile users on small screens  
- Lower frustration for users with attention or memory difficulties  
- Improve accessibility for neurodivergent users  

The icon switches visually between hidden and visible states, providing clear feedback without leaving the page or interrupting the login flow.

For consistency and accessibility, this behaviour is implemented across all authentication forms wherever a password is required by a site user.

---

### Behaviour & security

- Authentication handled securely via Django Allauth  
- Session management uses secure cookies in production  
- Users without valid credentials cannot access protected pages  
- Failed attempts are rate limited to protect accounts  

Sensitive emotional data remains inaccessible until authentication is complete.

---

**UX considerations:**

- Minimal, distraction-free design  
- Large, touch-friendly inputs  
- Fast completion (two fields only)  
- Accessible password visibility control  
- Clear recovery and account creation pathways  
- Calm tone without urgency or pressure  

The sign-in experience prioritises **privacy, trust, and ease of access**, ensuring users can quickly return to their emotional entries without feeling overwhelmed or confronted by complex security steps.

[Back to contents](#contents)

Return to [README.md](../README.md)

---

## Password Reset (Forgot Password)

Regulate provides a straightforward and reassuring password recovery process, ensuring users can safely regain access to their account without stress or complicated steps.

The design mirrors the sign-in and sign-up pages, using the same calm, centred layout and minimal inputs to keep the experience focused and low effort.

---

### Requesting a reset

If a user forgets their password, they can select **“Forgot your password?”** from the sign-in page.

They are asked only for:

- Their registered email address  

Submitting this form generates a secure password reset link.

Only essential information is required, preventing unnecessary friction during an already frustrating moment.

---

### Email delivery (project configuration)

For this project, reset emails are handled using Django’s **console email backend**, meaning links are printed directly to the terminal rather than sent externally.

This keeps the application self-contained for testing and assessment while still validating the complete password reset workflow.

---

### Secure reset flow

Password resets are handled by **Django Allauth** and follow industry-standard security practices:

- Each reset link contains a unique, single-use token  
- Links automatically expire after a short period  
- Invalid or expired links are rejected safely  
- Users cannot access the reset form without a valid token  

This prevents reuse or unauthorised access while protecting user accounts.

---

### Setting a new password

After opening a valid reset link, users are guided to a simple form to:

- Enter a new password  
- Confirm the password  

The same validation rules apply as during registration (matching fields, strength requirements, etc.).

Once completed successfully, the user is redirected back to the **Sign In** page where they can immediately log in with their new credentials.

---

**UX considerations:**

- Minimal, single-field request form  
- Clear and calm language  
- No blame or urgency  
- Secure token-based flow  
- Smooth return to login after completion  
- Consistent visual design with other authentication pages  

The password reset process prioritises **reliability, privacy, and reassurance**, ensuring users always have a safe path back to their personal space without unnecessary complexity.

[Back to contents](#contents)

Return to [README.md](../README.md)

---

## Sign Up Page

The sign-up page provides a **simple, reassuring onboarding experience**, allowing new users to create an account quickly without unnecessary complexity or pressure.

Like the sign-in page, the layout uses a centred card design with soft colours and generous spacing to maintain a calm, distraction-free environment.

The goal is to make registration feel approachable rather than clinical or overwhelming.

---

### Account creation inputs

New users are asked only for essential information:

- Username  
- Email address  
- Password  
- Password confirmation  

Keeping the form short reduces friction and lowers the barrier to getting started.

A password visibility toggle is also provided for convenience and accessibility, consistent with the behaviour used across all authentication forms for site users.

---

### Validation & feedback

Authentication and account management are handled securely using **Django Allauth**, which provides robust, industry-standard validation.

Users receive clear, human-readable feedback if:

- The email address is already registered  
- The username is unavailable  
- Passwords do not match  
- Password strength requirements are not met  
- Required fields are missing  

Errors are displayed inline and explained plainly, helping users correct issues without confusion or repeated attempts.

---

### Plan onboarding

To set clear expectations, the page explains that:

- New accounts begin on the Free plan  
- A limited number of entries are available  
- A Regulate+ free trial can be activated later from the account area  

This transparency prevents surprises and reinforces trust from the outset.

---

**UX considerations:**

- Minimal, low-effort form  
- Clear field labels and spacing  
- Touch-friendly inputs for mobile  
- Immediate validation feedback  
- Calm, non-technical language  
- No unnecessary personal information requested  

The sign-up experience prioritises **ease, clarity, and psychological safety**, ensuring that users can begin tracking their emotions quickly without encountering complicated registration steps.

[Back to contents](#contents)

Return to [README.md](../README.md)

---

## Mood Entry System

The Mood Entry System is the core functional feature of Regulate. It is deliberately structured to be **quick to complete, emotionally neutral, and cognitively low-demand**.

Each entry consists of:

- **Mood Hue (required)** – selected via a colour-based slider  
- **Emotion Words (optional)** – selectable tags  
- **Hue Meaning (optional)** – short reflective context  
- **Notes (optional)** – free-text expansion  

Only the hue selection is mandatory. This ensures an entry can always be created, even during periods of emotional shutdown, overwhelm, or low executive functioning.

Because mood tracking is the backbone of the platform, access to creating a new entry is intentionally prioritised and consistently visible once authenticated:

- Accessible from the **navbar dropdown** (available on every page)  
- Accessible from the **Dashboard** 
 - Accessible from the **My Entries** page
- Accessible from the **Home page (signed-in state)** via a clear call-to-action  

Providing multiple predictable access points reduces friction and ensures users never need to search for the platform’s primary function. This is particularly important during moments of distress, when cognitive load and decision-making capacity may be reduced.

---

### Mood Hue Slider

The hue slider is designed as a **non-judgmental emotional indicator**. Originally, the intention was to avoid assigning meaning to colour intensity. The goal was to prevent users from subconsciously associating darker tones with “bad” emotions or lighter tones with “good” emotions. Instead, users were encouraged to interpret the hue personally, supported by the optional *Hue Meaning* field where they could describe what that colour represented for them at that moment.

However, during early user testing, feedback indicated that the absence of guidance created confusion. Users were unsure how to select a hue that reflected a low mood, and questioned whether lighter meant “empty” or “positive,” and whether darker meant “low” or “strong.”

In response to this feedback, a **subtle contextual label** was introduced.

- The slider operates on a 0–100 scale  
- It is divided into five approximate bands (20-point ranges)  
- A dynamic label updates in real time while dragging  

The ranges are:

- 0–19 → Very low  
- 20–39 → Low  
- 40–59 → Neutral  
- 60–79 → Good  
- 80–100 → Very good  

Each new entry defaults to **50 (Neutral)** to avoid biasing the user toward either extreme.

Importantly, these labels act as **guidance rather than judgment**. They provide orientation without introducing scoring, streaks, or value-based language. Users can still override or reinterpret their chosen hue through the optional *Hue Meaning* field.

**Design considerations:**

- Single required input to minimise entry barrier  
- Neutral language (no “success/failure” framing)  
- Default midpoint to reduce emotional priming  
- Optional reflection fields clearly labelled  
- Multiple access points to reinforce feature priority  
- Fully usable on mobile with one-handed interaction  

[Back to contents](#contents)

Return to [README.md](../README.md)

---

### Emotion Words

Emotion Words act as a structured alternative to free-text reflection. They support users who may struggle to articulate feelings verbally but can recognise emotional labels.

Users can:

- Select one or multiple predefined emotion words  
- Filter/search within the emotion list  
- Use emotion words independently or alongside written notes  

The initial emotion vocabulary is seeded from a **JSON configuration file**, ensuring consistent default data. However, ongoing management does not require modification of this file. Additional emotion words can be created and managed directly through the **Django admin interface**, allowing the system to evolve without code-level changes.

This separation supports both technical maintainability and long-term scalability.

---

**UX considerations:**

- Supports emotional recognition before explanation  
- Reduces cognitive effort compared to writing  
- Avoids overwhelming the user with excessive choice  
- Maintains flexibility for future expansion  

[Back to contents](#contents)

Return to [README.md](../README.md)

---
## Dashboard
---

The Dashboard acts as the user’s calm “home base” within Regulate. It provides a structured overview of activity, account status, and supportive features without introducing urgency, metrics, or performance pressure.

The layout prioritises clarity and emotional neutrality while keeping core actions immediately accessible.

[Back to contents](#contents)

Return to [README.md](../README.md)

---

### Entry Overview & Plan Status

The dashboard clearly displays the user’s current subscription tier and remaining entry allowance (for Free plan users).

Free-plan users see a dynamically updated counter (e.g. “Free plan: 9 entries left”), with correct singular/plural handling.  

When the free entry limit is reached:

- Users can still **view** existing entries  
- Editing and deleting are disabled  
- Clear signposting directs users to the **Regulate+ page**  
- Users can start a free trial or subscribe to regain full functionality  

This ensures transparency without sudden lock-outs or hidden restrictions.

[Back to contents](#contents)

Return to [README.md](../README.md)

---

### Creating Entries

If a user has not yet created any entries, the dashboard presents a clear, supportive call-to-action:

- “Create Your First Entry”

If entries already exist, users can:

- Add a new entry  
- Navigate directly to their entries list via **“Go to Your Entries”**

This ensures the primary feature of the platform is always accessible without searching through menus.

[Back to contents](#contents)

Return to [README.md](../README.md)

---

### Browsing & Managing Entries

Selecting **“Go to Your Entries”** takes users to the dedicated entries page, where they can browse, search, view, edit, and delete previous entries in a structured and calm format.

#### Search & Filtering

Users can filter their entries using:

- A **date filter** (HTML date input)
- A **keyword search field** (searches both notes and emotion words)

Search behaviour:

- Only the logged-in user’s entries are queried
- Filters use `GET` parameters
- Date and keyword filters can be combined
- Empty search returns the full grouped list

This supports reflection and pattern recognition without requiring chronological scrolling.

[Back to contents](#contents)

Return to [README.md](../README.md)

---

#### Grouped Date Accordion Layout

Entries are grouped by date and displayed within collapsible accordion dropdown sections.

This:

- Reduces visual overwhelm  
- Keeps the interface clean and structured  
- Organises entries chronologically  

Each accordion header displays a specific date. Expanding it reveals all entries created on that day.

[Back to contents](#contents)

Return to [README.md](../README.md)

---

#### Entry Summary Display

Within each expanded section, entries display:

- Mood (human-readable label)  
- Hue value  
- Selected emotion words (if any)  
- Notes (if provided)  

If an entry has revision history, the following indicator appears:

> *Edited — revision history available*

This provides transparency while maintaining a neutral tone.

[Back to contents](#contents)

Return to [README.md](../README.md)

---

#### Viewing Entry Details

Selecting **“View”** opens a dedicated Entry Details page.

This page displays:

- Original creation timestamp  
- Last updated timestamp  
- Full entry content  
- Complete revision history  

Revision history entries show:

- Timestamp of revision  
- Previous mood, hue, emotion words, and notes  

Older versions remain accessible for reflective purposes.

[Back to contents](#contents)

Return to [README.md](../README.md)

---

#### Editing Entries

Users can edit entries unless:

- They are on the Free plan **and**
- They have reached the entry limit

If locked:

- Edit controls are disabled  
- Clear messaging explains the restriction  
- Users are directed toward Regulate+  

If unlocked:

- Users can update mood, hue, emotion words, and notes  
- A revision record is created **only if changes were made**  
- No revision is created for unchanged submissions (validated via automated testing)

[Back to contents](#contents)

Return to [README.md](../README.md)

---

#### Deleting Entries

Users can delete entries directly from the accordion list.

Deletion includes:

- JavaScript confirmation prompt  
- Clear irreversible warning message  
- Secure POST request with CSRF protection  

If a free-plan user deletes an entry while locked:

- Their entry count decreases  
- Create/edit access is automatically restored  
- A confirmation message is displayed  

This prevents permanent lockout and maintains fairness in the free plan logic.

[Back to contents](#contents)

Return to [README.md](../README.md)

---

### Supportive Phrases (External API Integration)

The dashboard allows users to generate a gentle, validating phrase.

Supportive phrases are fetched from the external API:

- `https://www.affirmations.dev`

If the external API is unavailable or fails, the system automatically falls back to a small set of hardcoded supportive phrases to ensure the feature always works.

This prevents broken UI states and avoids user-facing error messages.

[Back to contents](#contents)

Return to [README.md](../README.md)

---

### Site Announcements

Administrative announcements can be displayed on the dashboard.

Users can:

- Dismiss announcements during their session  

Announcements reappear on the next login if still active.

This design ensures:

- Important updates remain visible  
- Users are not permanently hiding relevant information  
- Interruptions remain minimal and non-intrusive  

---

**UX considerations:**

The dashboard and entries flow are intentionally:

- Calm and visually uncluttered  
- Free from performance metrics or streak tracking  
- Transparent about subscription limitations  
- Supportive rather than motivational  
- Focused on gentle guidance rather than urgency  

The dashboard supports both new and returning users while maintaining the core ethos of Regulate: reflection without pressure.

[Back to contents](#contents)

Return to [README.md](../README.md)

---
## Regulate+ Page
---

The **Regulate+ page** functions as the subscription control centre of the application. It provides users with clear visibility of their current plan and dynamically updates based on subscription status.

Access to this page is permanently available via the **“Regulate+” link in the navbar** once authenticated, ensuring users can review or manage their plan at any time without interruption.

---

### Dynamic Plan State Behaviour

The Regulate+ page renders different content depending on the user’s current subscription tier.

#### <u>When on the Free Plan</u>

If the user is on the **Free plan**, the page displays:

- Current plan indicator (“Free plan”)  
- **Start Free Trial** button  
- **Upgrade to Regulate+** button  

These actions:

- Create a Stripe Checkout session via the Django backend  
- Redirect the user to Stripe’s hosted checkout page  
- Allow activation of either the free trial or paid subscription  

The upgrade pathway is always user-initiated and never forced.

If a user reaches their free entry limit elsewhere in the application, they are signposted to this page — but remain fully in control of whether to upgrade.

#### <u>When on Free Trial or Active Subscription</u>

Once a user activates either:

- A **Regulate+ free trial**, or  
- A **Regulate+ subscription**

The Regulate+ page automatically updates to reflect the new plan state.

Instead of upgrade buttons, the page displays:

- **Manage Billing**

This button redirects the user to the **Stripe Customer Portal**.

All billing management is handled securely by Stripe. Through the Stripe portal, users can:

- View subscription details  
- Update payment methods  
- Cancel their subscription  
- Review invoices  
- Monitor trial status and renewal dates  

The application itself does not manage or store payment data.

---

### Access Control & Feature Impact

Plan tier directly affects platform capabilities:

- Free users have capped entry creation  
- Editing and deleting are disabled once the free limit is reached  
- Existing entries always remain visible  
- Trial and subscribed users have unlimited entry creation and full editing access  

Plan status is clearly displayed via a banner beneath the navbar to maintain transparency and prevent confusion.

No emotional data is ever removed or hidden based on subscription changes.

---

**UX considerations:**

The Regulate+ page was intentionally designed to:

- Avoid aggressive paywalls  
- Avoid urgency-based marketing tactics  
- Keep plan information transparent  
- Maintain user autonomy over upgrades  
- Separate financial transactions from emotional wellbeing tools  

The page presents upgrade options clearly when relevant and shifts to management controls once subscribed.

It acts as a calm, centralised subscription hub while Stripe remains responsible for all financial processing and billing logic.

---

[Back to contents](#contents)

Return to [README.md](../README.md)

---

## Payment Processing & Stripe Integration

Regulate uses **Stripe Checkout** to securely handle subscription payments and free trial activation.

Stripe was selected to ensure:

- Secure payment handling  
- PCI compliance  
- Reliable subscription lifecycle management  
- Minimal exposure of sensitive payment data to the application  

---

### Checkout Flow

When a user selects either:

- Activate Regulate+ free trial  
- Upgrade to Regulate+ subscription  

They are redirected to a **Stripe-hosted Checkout session**.

This ensures:

- Payment details are never processed or stored directly by the Regulate application  
- Card handling and authentication are managed entirely by Stripe  
- Strong Customer Authentication (SCA) is supported automatically  

After successful checkout, the user is redirected back to Regulate.

---

### Cancelled Checkout Handling

If a user leaves the Stripe Checkout page before completing the trial or subscription process, Stripe redirects them back to a dedicated cancellation endpoint within the application.

In this case:

- No subscription is created  
- No trial is activated  
- No billing changes occur  

The user is redirected to a clear status page displaying:

- “Trial not started”  
- A reassurance message explaining that no changes were made  
- A reminder that they can activate the trial later  
- A link back to the Regulate+ page  

A temporary banner message (“Checkout cancelled — no changes were made.”) is also displayed for clarity.

This behaviour ensures:

- No accidental activation  
- No confusing partial subscription states  
- Clear communication of system state  
- A calm, non-punitive user experience  

The cancellation flow is handled via Stripe’s `cancel_url` configuration within the Checkout session.

---

### Subscription State Management

Stripe manages:

- Billing information  
- Subscription status  
- Trial start and end dates  
- Renewal cycles  
- Payment failures  

Regulate stores a local subscription record that mirrors Stripe’s state.

Webhook events are used to:

- Confirm successful subscription creation  
- Update subscription status  
- Handle cancellations  
- Sync trial expiration  

This ensures the application’s access rules remain aligned with Stripe’s billing state.

---

### Free Trial Logic

The Regulate+ free trial is:

- One-time activation per user  
- Managed via Stripe’s trial functionality  
- Automatically converted to a paid subscription (if applicable) based on Stripe configuration  

Trial status is reflected immediately within the application via subscription checks.

---

### Stripe Test Mode (Academic Project Notice)

For the purposes of this Milestone Project Four submission, Stripe is configured in **Test Mode (Sandbox environment)**.

No real payments are processed.

Users and assessors should **not enter real card or payment details**.

Instead, Stripe provides official test card numbers which simulate successful and failed transactions without charging any funds.

A full list of test cards is available via Stripe’s documentation:

https://docs.stripe.com/testing#cards

Common test cards include:

| Card Type | Number | CVC | Expiry |
|------------|--------|------|--------|
| Visa | 4242 4242 4242 4242 | Any 3 digits | Any future date |
| Visa (Debit) | 4000 0566 5566 5556 | Any 3 digits | Any future date |
| Mastercard | 5555 5555 5555 4444 | Any 3 digits | Any future date |

These cards trigger successful subscription flows within Stripe’s test environment.

---

### Stripe Checkout Customisation

The Stripe Checkout page has been configured to reflect the Regulate brand and subscription model:

- Regulate logo uploaded to Stripe dashboard  
- Custom product name (“Regulate+ Monthly”)  
- Clear pricing displayed (£2.50 per month)  
- Free trial duration clearly shown  
- Explicit messaging stating users will not be charged until the trial ends  
- Multiple supported payment methods (Card, Klarna, Revolut Pay, Amazon Pay where available)  

Stripe handles:

- Trial period tracking  
- Recurring billing  
- Subscription renewal logic  
- Secure payment processing  

All payment methods are managed directly by Stripe’s hosted checkout page.

---

### Trial & Billing Transparency

The Checkout page clearly communicates:

- Trial length (e.g., 5 days free)  
- Billing start date  
- Monthly cost after trial (£2.50)  
- That charges continue until cancellation  

This ensures users understand:

- When billing begins  
- What they will be charged  
- That cancellation can occur before trial end  

No hidden fees or automatic charges occur outside Stripe’s clearly displayed subscription terms.

---

### Security & Data Handling

- No card data is stored within the Django application  
- All billing data remains within Stripe  
- Only subscription metadata (plan type, status, expiration) is stored locally  

This architecture reduces risk and ensures compliance with payment security standards.

---

### Technical Architecture

- Django backend creates Stripe Checkout sessions  
- Stripe webhooks update subscription records  
- Access control checks reference subscription status  
- Frontend conditionally renders UI based on plan tier  

This separation of concerns ensures billing logic remains robust while the application maintains clear access boundaries.

---

### Academic Integrity & Development Approach

Development of the Stripe integration involved consultation of:

- Official Stripe documentation  
- Stripe dashboard configuration tools  
- Test-mode debugging and webhook inspection tools  

All architectural decisions, implementation logic, subscription handling, and integration within Django were designed and implemented independently.

External documentation and debugging tools were used strictly as technical references.

---

[Back to contents](#contents)

Return to [README.md](../README.md)

---

## Profile Page (Account Management)

The **Profile page** provides a central location for users to manage their Regulate account details securely and independently.

It is accessible at all times via the **“My Account”** dropdown in the navbar once a user is authenticated. This ensures account management is always available without disrupting the core mood tracking experience.

---

### Account Overview

When viewing the Profile page, users can see:

- Their current **username**
- Their registered **email address**
- Clear options to update account details
- A secure logout option

For security reasons, passwords are never displayed.

This page acts as a calm, structured overview of personal account information.

---

### Change Username

Users can update their username via a dedicated form page.

- The current username is pre-filled for clarity  
- Changes are validated server-side  
- Clear success or error messages are displayed  

This allows users to maintain control over how their identity appears within the application.

---

### Change Email Address

Users may update the email address linked to their account.

- The current email is pre-filled  
- Changes are validated before saving  
- The updated email becomes the new login identifier  

This ensures contact and login information remains accurate.

---

### Change Password

Users can update their password securely by providing:

- Current password  
- New password  
- Confirmation of new password  

The password fields include a **visibility toggle (SVG eye icon)** to reduce typing errors and improve accessibility.

Passwords are never stored or displayed in plain text. All authentication handling is managed securely via Django’s built-in authentication system.

---

### Logout

A clearly marked **Log Out** button allows users to safely end their session.

- Logout is handled securely  
- Users are redirected appropriately after signing out  
- Session data is cleared  

The logout button is styled distinctly to prevent accidental activation while remaining easy to locate.

---

**UX considerations:**

The Profile system was designed to be:

- Simple and non-technical  
- Accessible from every authenticated page  
- Clearly separated from emotional tracking features  
- Secure without being intimidating  

Account management is intentionally calm and structured, reinforcing user autonomy without adding cognitive load.

---

[Back to contents](#contents)

Return to [README.md](../README.md)

---

## Footer Navigation

Secondary and informational pages are placed in the footer rather than the primary navigation to avoid clutter and reduce cognitive load.

These links are accessible to **all users**, whether signed in or not, ensuring that help, guidance, and support information are always available without requiring an account.

The footer provides access to supportive, reference, and utility content that users may need occasionally, but which should not compete with core daily actions such as logging entries.

Footer links include:

- Contact & feedback  
- FAQ  
- Crisis & Support resources  
- Back to top shortcut  

Separating these links from the main navigation helps maintain a calm, task-focused interface while still ensuring assistance remains easy to find when needed.

---

### FAQ

The **FAQ page** provides clear answers to common questions about how Regulate works.

It is intended to reduce uncertainty and minimise the need for direct support by explaining:

- How entries work  
- How plans and limits behave  
- Subscription and billing basics  
- General usage guidance  

Information is written in plain, non-technical language to ensure accessibility for all users.

**Design considerations:**

- Simple question-and-answer format  
- Clear, concise explanations  
- Avoids technical jargon  
- Supports independent problem solving  

---

### Crisis & Support Resources

Regulate includes a dedicated **Crisis & Support** page providing carefully selected, UK-specific mental health resources, including Hub of Hope.

This page is designed purely for **signposting external professional help**, not as a replacement for crisis services.

Users can:

- Access trusted mental health organisations and helplines  
- Find appropriate support quickly and safely  
- Navigate resources without overwhelming or alarmist language  

Regulate does not attempt to provide clinical advice or emergency intervention.  
Instead, it focuses on directing users to established services better equipped to offer immediate help.

**Design considerations:**

- Calm, non-clinical wording  
- Clear external links  
- No fear-based messaging  
- No claims of replacing professional care  

---

### Contact & Feedback

Separate from crisis resources, Regulate also provides a **Contact Us** page for general communication with the site administrator(s).

This form is intended for:

- Account or login support  
- Billing or subscription queries  
- Technical issues  
- Feature suggestions or feedback  

Submitting the form creates a **private support ticket** visible only to the site owner.

The contact form:

- Is available to both logged-in and logged-out users  
- Requires minimal information  
- Does not collect sensitive emotional data  
- Is designed for practical support only  

**Design considerations:**

- Clear separation from crisis messaging  
- Simple, low-effort form  
- Privacy-respecting handling of enquiries  
- Transparent expectations about response purpose  

---

### Back to top

A lightweight **“Back to top”** link is included in the footer to improve navigation on longer pages, particularly on mobile devices.

This allows users to quickly return to the beginning of the page without excessive scrolling.

**Design considerations:**

- Reduces physical effort on touch devices  
- Improves accessibility and ease of navigation  
- Non-intrusive utility element  

---

This structure ensures users can clearly distinguish between:

- informational help (FAQ)  
- emotional support resources (Crisis & Support)  
- practical site assistance (Contact)  

while keeping the primary interface uncluttered and focused on wellbeing tasks.

[Back to contents](#contents)

Return to [README.md](../README.md)

---

## User Feedback & System Messaging

Clear, consistent feedback is essential in an application handling emotional wellbeing data.  
Regulate uses structured success, error, and informational messaging to ensure users always understand what has happened, what is happening, and what will happen next.

All messaging is implemented using Django’s built-in **messages framework**, ensuring consistent rendering across templates and reliable server-side validation.

Messages are displayed in a consistent banner format and are:

- Clearly colour-differentiated (success, info, error)
- Written in plain, non-technical language
- Calm and non-judgemental in tone
- Dismissible where appropriate
- Never emotionally alarmist

---

### Success Messages

Success messages confirm that an action has completed correctly and that the system state has updated as expected.

Examples include:

- Account created successfully  
- Login successful  
- Profile details updated  
- Password changed successfully  
- Support ticket submitted  
- Subscription activated  
- Free trial started  

Stripe checkout success redirects also trigger a confirmation message once the subscription state is synchronised.

These messages:

- Provide immediate reassurance  
- Prevent uncertainty about system behaviour  
- Reduce repeated submissions  
- Confirm secure handling of user actions  

Success messages use a visually distinct success style to differentiate them from informational notices.

<!-- Add success message screenshots here -->

---

### Error Messages

Error messages are triggered when validation fails or when an action cannot be completed.

Examples include:

- Invalid login credentials  
- Username already taken  
- Email already registered  
- Password mismatch  
- Password strength requirements not met  
- Free trial already used  
- Attempting to subscribe while already active  
- Stripe checkout failure  
- Missing billing details  
- Invalid or expired password reset token  

All error messages:

- Are generated server-side  
- Prevent silent failures  
- Clearly explain what went wrong  
- Provide guidance where relevant  

Sensitive system information (such as Stripe exceptions or backend errors) is never exposed to the user. Instead, errors are logged internally while the user receives a safe, human-readable message.

This protects security while maintaining clarity.

<!-- Add error message screenshots here -->

---

### Informational Messages

Informational messages clarify system state without implying success or failure.

Examples include:

- “Checkout cancelled — no changes were made.”  
- “Checkout completed. Your plan usually updates within a few seconds.”  
- “You already have an active plan.”  
- “You can only use the free trial once per user.”  
- “Free plan: X entries left.”  

These messages are particularly important in subscription and billing flows, where confusion can easily occur.

They ensure:

- Transparency in billing state  
- No accidental activations  
- No ambiguous subscription conditions  
- Clear communication after Stripe redirects  

Informational messages help prevent anxiety around financial transactions.

<!-- Add informational message screenshots here -->

---

### Defensive UX & Edge Case Handling

Beyond standard form validation, Regulate includes deliberate defensive messaging patterns to handle edge cases safely and clearly.

These include:

- Stripe webhook delay handling message  
- Stripe checkout cancellation page  
- Free-entry limit soft lock messaging  
- Trial reuse prevention message  
- Billing portal fallback message if Stripe customer ID is missing  
- External API fallback for supportive phrases (no visible error shown to user)  
- Announcement dismissal confirmation  

Where possible:

- The system avoids blocking access abruptly  
- Users retain visibility of existing content  
- Messaging explains restrictions without pressure  
- Financial actions remain entirely user-initiated  

No destructive or irreversible actions occur without confirmation or clear communication.

---

### Design & Accessibility Considerations

All system messages are designed with:

- High colour contrast  
- Clear spacing and padding  
- Readable typography  
- Mobile responsiveness  
- Dismissible controls where appropriate  

Messages are positioned consistently to prevent unexpected layout shifts and ensure predictable behaviour across pages.

---

### Architectural Approach

- Implemented using Django’s `messages` framework  
- Triggered server-side within views  
- Rendered globally in base templates  
- Styled consistently using shared CSS classes  
- Logged internally where required for debugging  

This approach ensures messaging remains:

- Maintainable  
- Scalable  
- Secure  
- Consistent across future feature additions  

Effective system messaging reinforces Regulate’s core principle:

> Users should never feel confused, punished, or uncertain about what the system is doing.

Clear communication supports emotional safety as much as the tracking features themselves.


[Back to contents](#contents)

Return to [README.md](../README.md)

---

## Custom Error Pages

Regulate includes custom-designed error pages for common HTTP failure states to ensure users are never exposed to raw Django error screens in production.

Rather than displaying technical debug information, the application provides calm, user-friendly fallback pages.

---

### 404 Page Not Found

The custom 404 page is shown when a user attempts to access a non-existent URL.

It includes:

- Clear, human-readable explanation (“Page not found”)  
- Context-sensitive navigation button  
  - Authenticated users → redirected to **Dashboard**  
  - Non-authenticated users → redirected to **Home**  
- Visible error code (404) for transparency  

This ensures users can recover quickly without confusion or technical messaging.

No stack traces or internal routing details are exposed.

---

### 500 Server Error

The custom 500 page handles unexpected server-side failures.

It includes:

- Calm, non-alarmist messaging (“Something went wrong”)  
- Context-sensitive navigation back to a safe page  
- Visible error code (500)  
- No exposure of technical exception details  

This protects sensitive backend information while maintaining clarity for the user.

---

### Security & Production Behaviour

In production:

- `DEBUG = False`  
- Django’s default debug tracebacks are disabled  
- Sensitive system information is never shown to end users  

Errors are logged server-side for debugging and maintenance purposes, but the user interface remains stable and reassuring.

---

These custom error pages reinforce Regulate’s commitment to:

- Privacy  
- Emotional safety  
- Clear communication  
- Production-ready deployment standards  

---

[Back to contents](#contents)

Return to [README.md](../README.md)

---

## Admin Dashboard & Operational Controls

The Regulate admin interface is intentionally structured to support **platform maintenance without exposing sensitive emotional data**.

Access to `/admin/` is restricted to:

- Staff users  
- Superusers  

Standard authenticated users cannot access the admin interface.

Permissions follow the principle of **least privilege**, meaning administrative users only see the models required for operational management.

---

### Django Administration Interface

The default Django admin navbar includes:

- Welcome message displaying the logged-in admin user  
- **View site** link (returns to the public-facing application)  
- **Change password** link (admin credential update)  
- **Log out** link  
- Breadcrumb navigation showing current admin location  

The right-hand panel includes:

- Recent actions  
- My actions  
- Filtering tools (where applicable per model)

---

### Groups

Admins can:

- Add new groups  
- Assign permissions to groups  
- View number of group members  
- Edit existing group permissions  

This allows structured role management (e.g. site user vs admin view-only roles).

### Users

Admins can:

- Add new users  
- Edit usernames and email addresses  
- Reset passwords  
- Activate or deactivate accounts  
- Assign staff or superuser status  
- Allocate users to groups  
- View last login timestamp  
- View account creation date  

From the user list view, admins can:

- Search users  
- Filter by active status, staff status, or group  
- Bulk delete selected users  

Importantly:

- Admins cannot view a user’s mood entries or emotional notes from this screen  
- The “Entries” count shown is numeric only and does not expose content  

---

### Billing Management

The admin panel provides access to the `Subscription` model for operational oversight.

Admins can view:

- Associated user  
- Subscription status (trialing, active, cancelled, etc.)  
- Trial end date  
- Current billing period end  
- Stripe customer ID  
- Stripe subscription ID  
- Whether the user has previously used a trial  

Admins may:

- Search subscriptions  
- Filter by status  
- Bulk delete records if required  

Stripe remains the source of truth for billing state.  
The admin reflects subscription metadata only.

---

### Admin Emotion Words

Emotion words are managed through the admin interface rather than requiring manual edits to a JSON file.

Admins can:

- Add new emotion words  
- Edit existing emotion words  
- Delete emotion words (individually or in bulk)  
- Search through the emotion word list  

This allows the emotional vocabulary to evolve without codebase modification.

Emotion word selections tied to individual mood entries are **not visible in admin**.

---

### Admin Site Announcements

Admins can:

- Create new announcements  
- Set active/inactive state  
- Define start and end visibility dates  
- Edit existing announcements  
- Filter by active status  

This allows controlled messaging (e.g., maintenance notices or updates).

---

### Support Tickets

The admin interface allows administrators to manage user contact submissions.

Admins can:

- View submitted support tickets  
- See subject, user, and email reference  
- Mark tickets as replied  
- Delete tickets (individually or in bulk)  
- Filter by ticket status  
- Search tickets  

This provides structured support handling without exposing emotional journal data.

---

### Models Intentionally Excluded from Admin

The following models are deliberately **not registered in the admin panel**:

- Mood entries  
- Emotional notes  
- Entry revisions  
- Hue meanings  
- Emotion word selections per entry  

These models contain deeply personal reflections and are structurally protected from administrative browsing.

This is an architectural decision, not just a policy choice.

---

### Privacy & Security Safeguards

Additional protections include:

- Staff-only authentication  
- Environment variable management for secrets  
- HTTPS enforcement in production  
- Secure cookie configuration  
- Stripe-managed payment data (no card storage in Django)  

The admin interface is therefore restricted to **operational management only**, never emotional surveillance.

---

This design reinforces Regulate’s core principle:

> Users should feel safe expressing emotions without fear of observation.

[Back to contents](#contents)

Return to [README.md](../README.md)

---

---

**End of TESTING**  