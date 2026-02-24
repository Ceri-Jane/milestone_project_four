# User Stories
----------

## Must-Have User Stories
---

### User Story 1 – User Registration

**As a new user**, I want to create an account so that my emotional entries are private and securely stored.

**Acceptance Criteria**
- A registration form exists  
- Users can register with a username, email, and password  
- Invalid input displays accessible error messages  
- Passwords are securely hashed  

**Tasks**
- Configure Django Allauth  
- Create and style custom signup template  
- Validate form input and error handling  

Return to [README.md](../README.md)

---
---

### User Story 2 – User Login & Logout

**As a returning user**, I want to log in and out securely so that only I can access my entries.

**Acceptance Criteria**
- Login page exists  
- Invalid credentials show an error  
- Successful login redirects to the dashboard  
- Logout clears the session and redirects safely  

**Tasks**
- Implement authentication views  
- Style login and logout templates  
- Add navigation logic based on authentication state  

Return to [README.md](../README.md)

---
---

### User Story 3 – Create a Mood Entry

**As a user**, I want to log my mood using a simple, low-pressure form so I can record how I’m feeling without being overwhelmed.

**Acceptance Criteria**
- Mood hue input is required  
- Emotion words are optional  
- Notes and hue meaning are optional  
- Entry saves successfully with a timestamp  
- Multiple entries per day are supported  

**Tasks**
- Build entry creation view  
- Add mood hue slider  
- Save entry data to the database  
- Redirect with success feedback  

Return to [README.md](../README.md)

---
---

### User Story 4 – Emotion Words as Low-Effort Input

**As a user**, I want to select from predefined emotion words so I can label how I feel even when I can’t write.

**Acceptance Criteria**
- Emotion words are displayed as selectable options  
- Multiple emotion words can be chosen  
- Selected words save correctly with the entry  
- Emotion words display on the entry detail view  

**Tasks**
- Create EmotionWord model  
- Seed database with curated emotion words  
- Build checkbox UI with search filtering  
- Save selected words to the entry  

Return to [README.md](../README.md)

---
---

### User Story 5 – View Entries Without a Calendar

**As a user**, I want to view my past entries in a timeline so I don’t feel judged for missing days.

**Acceptance Criteria**
- Entries display in chronological order  
- Only dates with entries are shown  
- Entries are grouped by date  
- No calendar or streak indicators exist  

**Tasks**
- Create entries list view  
- Group entries by date  
- Design timeline-style layout  

Return to [README.md](../README.md)

---
---

### User Story 6 – Edit an Entry With History

**As a user**, I want to edit an entry so I can correct or expand on it without losing the original context.

**Acceptance Criteria**
- Only the entry owner can edit  
- Previous entry state is preserved automatically  
- Revision history is visible on the entry detail page  

**Tasks**
- Create EntryRevision model  
- Save revision snapshot before editing  
- Build edit entry form  
- Display revision history  

Return to [README.md](../README.md)

---
---

### User Story 7 – Delete an Entry Safely

**As a user**, I want to delete an entry so I can remove something I no longer want stored.

**Acceptance Criteria**
- Only the entry owner can delete  
- Deletion requires confirmation  
- Entry is permanently removed  
- User is redirected safely  

**Tasks**
- Create delete view (POST-only)  
- Add confirmation prompt  
- Remove entry from database  

Return to [README.md](../README.md)

---
---

### User Story 8 – Filter Entries by Date

**As a user**, I want to filter my entries by date so I can find specific moments easily.

**Acceptance Criteria**
- Date filter input exists  
- Only matching entries are returned  
- No empty dates are displayed  

**Tasks**
- Add date filter logic to entries view  
- Parse and validate query parameters  

Return to [README.md](../README.md)

---
---

### User Story 9 – Dashboard Overview

**As a user**, I want a calm dashboard so I can see my status without being overwhelmed.

**Acceptance Criteria**
- Dashboard loads after login  
- Subscription status is visible  
- Entry count and free limit are displayed  
- Active announcements are shown  

**Tasks**
- Build dashboard view  
- Add subscription context  
- Display announcements  

Return to [README.md](../README.md)

---
---

### User Story 10 – Supportive Phrases

**As a user**, I want to see a gentle supportive phrase so I feel encouraged without pressure.

**Acceptance Criteria**
- A supportive phrase is displayed on the dashboard  
- User can refresh the phrase  
- System falls back safely if the external service fails  

**Tasks**
- Create phrase endpoint  
- Add JavaScript fetch logic  
- Implement local fallback phrases  

Return to [README.md](../README.md)

---
---

### User Story 11 – Access Support Resources

**As a user**, I want access to trusted support resources so I know where to get help if I’m struggling.

**Acceptance Criteria**
- Support page exists  
- UK-based resources are clearly signposted  
- Language is clear, calm, and non-alarming  

**Tasks**
- Create support template  
- Link to Hub of Hope  
- Write safe support copy  

Return to [README.md](../README.md)

---
---

### User Story 12 – Contact the Site Owner

**As a user**, I want to contact the site owner so I can ask for help or report an issue.

**Acceptance Criteria**
- Contact form exists  
- Logged-out users can submit with an email address  
- Logged-in users are linked automatically  
- Support tickets are saved securely  

**Tasks**
- Create SupportTicket model  
- Build contact form view  
- Save submissions to database  

Return to [README.md](../README.md)

---
---

## Must-Have Site Owner Stories
---

### Site Owner Story A – Free Tier With Limits

**As a site owner**, I want to limit free usage so the app remains sustainable without blocking access to past data.

**Acceptance Criteria**
- Free users can create up to 10 entries  
- Users can still view existing entries after reaching the limit  
- Create, edit, and delete actions are locked  

**Tasks**
- Implement free-tier limit logic  
- Add lock checks to entry views  
- Display clear user messaging  

Return to [README.md](../README.md)

---
---

### Site Owner Story B – Trial Abuse Prevention

**As a site owner**, I want to prevent repeated free trials so the system is fair and sustainable.

**Acceptance Criteria**
- Free trial can only be used once per user  
- Trial status is tracked persistently  
- Users cannot restart a trial after expiry  

**Tasks**
- Add trial tracking field  
- Enforce rules in billing logic  
- Sync subscription status via webhooks  

Return to [README.md](../README.md)

---
---

### Site Owner Story C – Privacy-Focused Administration

**As a site owner**, I want to protect user privacy by restricting admin access to emotional content.

**Acceptance Criteria**
- Entries and revisions are not browsable in admin  
- Support tickets and subscriptions remain manageable  
- Admin interface is clearly branded and structured  

**Tasks**
- Unregister Entry models from admin  
- Configure admin permissions  
- Customise admin branding  

Return to [README.md](../README.md)

---
---

## Should-Have User Stories
---

### User Story 13 – Keyword Search

**As a user**, I want to search my entries by keyword so I can reflect on patterns over time.

**Acceptance Criteria**
- Search includes notes and emotion words  
- Only matching entries are returned  

**Tasks**
- Add keyword search filter  
- Query relevant entry fields  

Return to [README.md](../README.md)

---
---

### User Story 14 – Announcement Awareness

**As a user**, I want to see important site announcements without being repeatedly interrupted.

**Acceptance Criteria**
- Announcements display only while active  
- Dismissal persists per session or login  

**Tasks**
- Add announcement model  
- Implement dismissal logic with local storage  

Return to [README.md](../README.md)

---
---

## Could-Have User Stories (Future Development)
---

### User Story 15 – Export Entries

**As a user**, I want to export my entries so I can share them with a therapist or trusted person.

**Acceptance Criteria**
- Users can select entries  
- Export is available as PDF or text  
- Output is readable and sensitive  

**Tasks**
- Build export service  
- Create export templates  
- Add selection UI  

Return to [README.md](../README.md)

---
---

### User Story 16 – Mood Pattern Visualisation

**As a user**, I want to see my mood trends visually so I can recognise patterns over time.

**Acceptance Criteria**
- Visual graph displays mood trends  
- Uses only the user’s own data  
- Presentation remains non-judgmental  

**Tasks**
- Aggregate mood data  
- Integrate charting library  
- Design calm visual styling  

Return to [README.md](../README.md)

---
---

### Site Owner Story D – Referral Discounts

**As a site owner**, I want to offer referral discounts so users can share the app ethically.

**Acceptance Criteria**
- Referral codes can be generated  
- Discounts apply at checkout  
- Abuse is prevented  

**Tasks**
- Create referral model  
- Integrate with billing system  
- Validate referral usage  

Return to [README.md](../README.md)

---
---

### Site Owner Story E – International Expansion

**As a site owner**, I want to expand support resources internationally once proper research is completed.

**Acceptance Criteria**
- Resources are region-specific  
- Safeguarding considerations are reviewed per region  

**Tasks**
- Research international services  
- Add localisation support  
- Update support pages dynamically  

Return to [README.md](../README.md)

---
---

End of USER-STORIES