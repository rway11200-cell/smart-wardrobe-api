ALTER TABLE identities
ADD COLUMN nickname VARCHAR(50) NULL AFTER display_name;

UPDATE identities
SET nickname = LOWER(CONCAT(LEFT(REPLACE(display_name, ' ', '_'), 32), '_', id))
WHERE nickname IS NULL;

ALTER TABLE identities
MODIFY nickname VARCHAR(50) NOT NULL;

ALTER TABLE identities
ADD CONSTRAINT uq_identities_nickname UNIQUE (nickname);
