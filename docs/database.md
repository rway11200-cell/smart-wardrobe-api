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

## Clothing Inventory

`clothing_categories` stores the available clothing categories.
`clothing_items` stores clothing owned by an identity. Public API endpoints receive `public_id`, but clothing items are stored internally with `identities.id`.

```mermaid
erDiagram
    IDENTITIES ||--o{ CLOTHING_ITEMS : owns
    CLOTHING_CATEGORIES ||--o{ CLOTHING_ITEMS : classifies

    IDENTITIES {
        int id PK
        char public_id UK
        varchar display_name
        boolean is_active
        datetime created_at
        datetime updated_at
    }

    CLOTHING_CATEGORIES {
        int id PK
        varchar name UK
        varchar layer_type
        boolean required_for_outfit
        int display_order
        datetime created_at
    }

    CLOTHING_ITEMS {
        int id PK
        int identity_id FK
        int category_id FK
        varchar name
        varchar color
        varchar material
        varchar image_url
        decimal warmth_rating
        decimal comfort_rating
        decimal formality_rating
        decimal rain_rating
        decimal wind_rating
        varchar current_status
        boolean is_active
        datetime last_worn_at
        datetime created_at
        datetime updated_at
    }
```
