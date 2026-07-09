EDITABLE_ITEM_FIELDS = {
    "category_id",
    "name",
    "color",
    "material",
    "image_url",
    "warmth_rating",
    "comfort_rating",
    "formality_rating",
    "rain_rating",
    "wind_rating",
}

NULLABLE_ITEM_FIELDS = {"color", "material", "image_url"}


def _to_category_response(row):
    return {
        "name": row["name"],
        "layer_type": row["layer_type"],
        "required_for_outfit": bool(row["required_for_outfit"]),
        "display_order": row["display_order"],
    }


def _to_color_response(row):
    return {
        "name": row["name"],
        "hex_code": row["hex_code"],
        "display_order": row["display_order"],
    }


def _to_item_response(row):
    if not row:
        return None

    return {
        "id": row["id"],
        "category_name": row["category_name"],
        "name": row["name"],
        "color": row["color"],
        "material": row["material"],
        "image_url": row["image_url"],
        "warmth_rating": float(row["warmth_rating"]),
        "comfort_rating": float(row["comfort_rating"]),
        "formality_rating": float(row["formality_rating"]),
        "rain_rating": float(row["rain_rating"]),
        "wind_rating": float(row["wind_rating"]),
        "current_status": row["current_status"],
        "is_active": bool(row["is_active"]),
        "last_worn_at": row["last_worn_at"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }


def list_categories(connection):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT name, layer_type, required_for_outfit, display_order
            FROM clothing_categories
            ORDER BY display_order ASC, name ASC
            """
        )
        return [_to_category_response(row) for row in cursor.fetchall()]


def list_colors(connection):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT name, hex_code, display_order
            FROM clothing_colors
            ORDER BY display_order ASC, name ASC
            """
        )
        return [_to_color_response(row) for row in cursor.fetchall()]


def get_identity_id_by_public_id(connection, public_id: str):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM identities WHERE public_id = %s", (public_id,))
        row = cursor.fetchone()

    if not row:
        return None

    return row["id"]


def get_category_id_by_name(connection, category_name: str):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM clothing_categories WHERE name = %s", (category_name,))
        row = cursor.fetchone()

    if not row:
        return None

    return row["id"]


def create_item(connection, identity_id: int, category_id: int, data) -> int:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO clothing_items (
                identity_id,
                category_id,
                name,
                color,
                material,
                image_url,
                warmth_rating,
                comfort_rating,
                formality_rating,
                rain_rating,
                wind_rating,
                current_status
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                identity_id,
                category_id,
                data.name,
                data.color,
                data.material,
                data.image_url,
                data.warmth_rating,
                data.comfort_rating,
                data.formality_rating,
                data.rain_rating,
                data.wind_rating,
                data.current_status,
            ),
        )
        return cursor.lastrowid


def list_items_for_identity(connection, identity_id: int):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                ci.id,
                cc.name AS category_name,
                ci.name,
                ci.color,
                ci.material,
                ci.image_url,
                ci.warmth_rating,
                ci.comfort_rating,
                ci.formality_rating,
                ci.rain_rating,
                ci.wind_rating,
                ci.current_status,
                ci.is_active,
                ci.last_worn_at,
                ci.created_at,
                ci.updated_at
            FROM clothing_items ci
            INNER JOIN clothing_categories cc ON cc.id = ci.category_id
            WHERE ci.identity_id = %s AND ci.is_active = TRUE
            ORDER BY ci.id DESC
            """,
            (identity_id,),
        )
        return [_to_item_response(row) for row in cursor.fetchall()]


def get_item_for_identity(connection, identity_id: int, item_id: int):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                ci.id,
                cc.name AS category_name,
                ci.name,
                ci.color,
                ci.material,
                ci.image_url,
                ci.warmth_rating,
                ci.comfort_rating,
                ci.formality_rating,
                ci.rain_rating,
                ci.wind_rating,
                ci.current_status,
                ci.is_active,
                ci.last_worn_at,
                ci.created_at,
                ci.updated_at
            FROM clothing_items ci
            INNER JOIN clothing_categories cc ON cc.id = ci.category_id
            WHERE ci.id = %s AND ci.identity_id = %s AND ci.is_active = TRUE
            """,
            (item_id, identity_id),
        )
        return _to_item_response(cursor.fetchone())


def update_item(connection, identity_id: int, item_id: int, changes: dict):
    fields = []
    values = []

    for field_name, value in changes.items():
        if field_name not in EDITABLE_ITEM_FIELDS:
            continue

        if value is None and field_name in NULLABLE_ITEM_FIELDS:
            fields.append(f"{field_name} = NULL")
        else:
            fields.append(f"{field_name} = %s")
            values.append(value)

    fields.append("updated_at = CURRENT_TIMESTAMP")
    values.extend([item_id, identity_id])

    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            UPDATE clothing_items
            SET {', '.join(fields)}
            WHERE id = %s AND identity_id = %s AND is_active = TRUE
            """,
            values,
        )


def update_item_status(connection, identity_id: int, item_id: int, current_status: str):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            UPDATE clothing_items
            SET
                current_status = %s,
                last_worn_at = CASE WHEN %s = 'worn' THEN CURRENT_TIMESTAMP ELSE last_worn_at END,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s AND identity_id = %s AND is_active = TRUE
            """,
            (current_status, current_status, item_id, identity_id),
        )


def soft_delete_item(connection, identity_id: int, item_id: int):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            UPDATE clothing_items
            SET is_active = FALSE, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s AND identity_id = %s AND is_active = TRUE
            """,
            (item_id, identity_id),
        )
