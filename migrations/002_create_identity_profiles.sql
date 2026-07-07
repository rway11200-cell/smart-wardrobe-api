CREATE TABLE IF NOT EXISTS identity_profiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    identity_id INT NOT NULL UNIQUE,
    cold_sensitivity DECIMAL(3,2) NOT NULL DEFAULT 0.50,
    heat_sensitivity DECIMAL(3,2) NOT NULL DEFAULT 0.50,
    comfort_priority DECIMAL(3,2) NOT NULL DEFAULT 0.50,
    style_priority DECIMAL(3,2) NOT NULL DEFAULT 0.50,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NULL,
    CONSTRAINT fk_identity_profiles_identity_id
        FOREIGN KEY (identity_id) REFERENCES identities(id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
