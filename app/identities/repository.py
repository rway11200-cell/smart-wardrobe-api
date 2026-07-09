PROFILE_FIELDS = {
    "cold_sensitivity",
    "heat_sensitivity",
    "comfort_priority",
    "style_priority",
}


def _to_identity_response(row):
    if not row:
        return None

    return {
        "public_id": row["public_id"],
        "display_name": row["display_name"],
        "nickname": row["nickname"],
        "profile": {
            "cold_sensitivity": float(row["cold_sensitivity"]),
            "heat_sensitivity": float(row["heat_sensitivity"]),
            "comfort_priority": float(row["comfort_priority"]),
            "style_priority": float(row["style_priority"]),
        },
    }


def create_identity(connection, public_id: str, display_name: str, nickname: str) -> int:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO identities (public_id, display_name, nickname)
            VALUES (%s, %s, %s)
            """,
            (public_id, display_name, nickname),
        )
        return cursor.lastrowid


def create_profile(connection, identity_id: int):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO identity_profiles (identity_id)
            VALUES (%s)
            """,
            (identity_id,),
        )


def get_identity_by_public_id(connection, public_id: str):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                i.public_id,
                i.display_name,
                i.nickname,
                p.cold_sensitivity,
                p.heat_sensitivity,
                p.comfort_priority,
                p.style_priority
            FROM identities i
            INNER JOIN identity_profiles p ON p.identity_id = i.id
            WHERE i.public_id = %s
            """,
            (public_id,),
        )
        return _to_identity_response(cursor.fetchone())


def get_identity_by_nickname(connection, nickname: str):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                i.public_id,
                i.display_name,
                i.nickname,
                p.cold_sensitivity,
                p.heat_sensitivity,
                p.comfort_priority,
                p.style_priority
            FROM identities i
            INNER JOIN identity_profiles p ON p.identity_id = i.id
            WHERE i.nickname = %s
            """,
            (nickname,),
        )
        return _to_identity_response(cursor.fetchone())


def list_identities(connection, name: str | None = None):
    values = []
    where_clause = ""

    if name:
        where_clause = "WHERE i.display_name LIKE %s"
        values.append(f"%{name}%")

    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            SELECT
                i.public_id,
                i.display_name,
                i.nickname,
                p.cold_sensitivity,
                p.heat_sensitivity,
                p.comfort_priority,
                p.style_priority
            FROM identities i
            INNER JOIN identity_profiles p ON p.identity_id = i.id
            {where_clause}
            ORDER BY i.id ASC
            """,
            values,
        )
        return [_to_identity_response(row) for row in cursor.fetchall()]


def get_internal_identity_id(connection, public_id: str):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM identities WHERE public_id = %s", (public_id,))
        row = cursor.fetchone()

    if not row:
        return None

    return row["id"]


def update_profile(connection, identity_id: int, changes: dict):
    fields = []
    values = []

    for field_name, value in changes.items():
        if field_name not in PROFILE_FIELDS:
            continue

        if value is None:
            fields.append(f"{field_name} = NULL")
        else:
            fields.append(f"{field_name} = %s")
            values.append(value)

    fields.append("updated_at = CURRENT_TIMESTAMP")
    values.append(identity_id)

    with connection.cursor() as cursor:
        cursor.execute(
            f"UPDATE identity_profiles SET {', '.join(fields)} WHERE identity_id = %s",
            values,
        )
