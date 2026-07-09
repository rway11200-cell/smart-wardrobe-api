CREATE TABLE IF NOT EXISTS clothing_colors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(80) NOT NULL UNIQUE,
    hex_code CHAR(7) NULL,
    display_order INT NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT IGNORE INTO clothing_colors (name, hex_code, display_order)
VALUES
    ('black', '#000000', 1),
    ('white', '#FFFFFF', 2),
    ('gray', '#808080', 3),
    ('navy', '#000080', 4),
    ('blue', '#0000FF', 5),
    ('green', '#008000', 6),
    ('red', '#FF0000', 7),
    ('pink', '#FFC0CB', 8),
    ('purple', '#800080', 9),
    ('brown', '#8B4513', 10),
    ('beige', '#F5F5DC', 11),
    ('yellow', '#FFFF00', 12),
    ('orange', '#FFA500', 13),
    ('multicolor', NULL, 14);
