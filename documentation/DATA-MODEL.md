# Data Model & Relationships
---

The data model for Regulate is designed to support **flexible emotional expression**, **user privacy**, and **future expansion**, while remaining clear, maintainable, and aligned with relational database best practices.

```
┌─────────────────────────┐
│ User                    │
└─────────────┬───────────┘
              │ 1-to-many
┌─────────────▼───────────┐
│ Entry                   │
├─────────────────────────┤
│ id (PK)                 │
│ user (FK → User)        │
│ hue (integer)           │
│ mood_label (derived)    │
│ emotion_words (text)    │
│ notes (text, optional)  │
│ created_at (datetime)   │
│ updated_at (datetime)   │
└─────────────┬───────────┘
              │ 1-to-many
┌─────────────▼───────────┐
│ EntryRevision           │
├─────────────────────────┤
│ id (PK)                 │
│ entry (FK → Entry)      │
│ previous_hue            │
│ previous_emotions       │
│ previous_notes          │
│ edited_at (datetime)    │
└─────────────────────────┘

┌─────────────────────────┐
│ EmotionWord             │
└─────────────┬───────────┘
              │ many-to-many
┌─────────────▼───────────┐
│ Entry                   │
└─────────────────────────┘

┌─────────────────────────┐
│ Subscription            │
├─────────────────────────┤
│ user (OneToOne → User)  │
│ status                  │
│ stripe_customer_id      │
│ stripe_subscription_id  │
│ trial_start             │
│ trial_end               │
│ has_had_trial (bool)    │
│ cancel_at_period_end    │
└─────────────────────────┘

┌─────────────────────────┐
│ SupportTicket           │
├─────────────────────────┤
│ id (PK)                 │
│ user (FK, optional)     │
│ email (optional)        │
│ subject                 │
│ message                 │
│ created_at              │
│ is_resolved (bool)      │
└─────────────────────────┘

┌─────────────────────────┐
│ SiteAnnouncement        │
├─────────────────────────┤
│ id (PK)                 │
│ title                   │
│ message                 │
│ start_date              │
│ end_date                │
│ is_active (derived)     │
└─────────────────────────┘
```

# Why this structure works

- The schema follows **Django and relational database best practices**  
- Core emotional data is clearly owned by the user and never shared  
- Entries support minimal or detailed input without enforcing structure  
- Revision history preserves emotional context without overwriting past states  
- Emotion words are stored relationally to support future pattern analysis  
- Subscription data is isolated from emotional content  
- Support tickets allow user-initiated contact without exposing private entries  
- Administrative announcements are separated from user data  

The model is intentionally designed to be **expandable**, allowing future features such as mood visualisation, data export, and international support resources to be added without restructuring existing data.

# Data Integrity & Schema Alignment

All database models are fully implemented and match the schema documented above. 

The deployed application reflects this schema exactly, with no divergence between documented structure and implemented models.

All relational links (ForeignKey, ManyToMany, OneToOne) are enforced at model level and validated at form level, ensuring structural integrity and preventing invalid data states.

---

Return to [README.md](../README.md)