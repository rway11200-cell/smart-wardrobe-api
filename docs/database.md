# Database

`identities` stores the minimal system identity.
`identity_profiles` stores app-specific preferences for that identity.
`public_id` is temporarily used as an external identifier until real authentication is implemented.
The internal numeric `id` is used only for database relationships.

`migrations/003_seed_dummy_identities.sql` creates two dummy identities for local testing: `Alex Morgan` and `Jordan Lee`.

```mermaid
erDiagram
    IDENTITIES ||--|| IDENTITY_PROFILES : has

    IDENTITIES {
        int id PK
        char public_id UK
        varchar display_name
        boolean is_active
        datetime created_at
        datetime updated_at
    }

    IDENTITY_PROFILES {
        int id PK
        int identity_id FK
        decimal cold_sensitivity
        decimal heat_sensitivity
        decimal comfort_priority
        decimal style_priority
        datetime created_at
        datetime updated_at
    }
```
