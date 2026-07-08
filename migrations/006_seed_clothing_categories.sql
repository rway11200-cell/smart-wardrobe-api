INSERT IGNORE INTO clothing_categories (name, layer_type, required_for_outfit, display_order)
VALUES
    ('top', 'base_layer', TRUE, 1),
    ('bottom', 'lower_body', TRUE, 2),
    ('shoes', 'footwear', TRUE, 3),
    ('outerwear', 'outer_layer', FALSE, 4),
    ('accessory', 'accessory', FALSE, 5);
