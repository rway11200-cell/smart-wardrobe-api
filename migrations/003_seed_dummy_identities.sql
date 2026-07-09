INSERT IGNORE INTO identities (public_id, display_name)
VALUES
    ('11111111-1111-4111-8111-111111111111', 'Demo User One'),
    ('22222222-2222-4222-8222-222222222222', 'Demo User Two');

INSERT IGNORE INTO identity_profiles (
    identity_id,
    cold_sensitivity,
    heat_sensitivity,
    comfort_priority,
    style_priority
)
SELECT
    id,
    0.80,
    0.40,
    0.90,
    0.60
FROM identities
WHERE public_id = '11111111-1111-4111-8111-111111111111';

INSERT IGNORE INTO identity_profiles (
    identity_id,
    cold_sensitivity,
    heat_sensitivity,
    comfort_priority,
    style_priority
)
SELECT
    id,
    0.30,
    0.70,
    0.50,
    0.80
FROM identities
WHERE public_id = '22222222-2222-4222-8222-222222222222';
