CREATE TABLE IF NOT EXISTS clothing_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    identity_id INT NOT NULL,
    category_id INT NOT NULL,
    name VARCHAR(120) NOT NULL,
    color VARCHAR(80) NULL,
    material VARCHAR(100) NULL,
    image_url VARCHAR(500) NULL,
    warmth_rating DECIMAL(3,2) NOT NULL DEFAULT 0.50,
    comfort_rating DECIMAL(3,2) NOT NULL DEFAULT 0.50,
    formality_rating DECIMAL(3,2) NOT NULL DEFAULT 0.50,
    rain_rating DECIMAL(3,2) NOT NULL DEFAULT 0.00,
    wind_rating DECIMAL(3,2) NOT NULL DEFAULT 0.00,
    current_status VARCHAR(30) NOT NULL DEFAULT 'clean',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    last_worn_at DATETIME NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NULL,
    CONSTRAINT fk_clothing_items_identity_id
        FOREIGN KEY (identity_id) REFERENCES identities(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_clothing_items_category_id
        FOREIGN KEY (category_id) REFERENCES clothing_categories(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
