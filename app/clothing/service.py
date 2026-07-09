from app.clothing import repository
from app.database import get_connection

NON_NULL_UPDATE_FIELDS = {
    "category_name",
    "name",
    "warmth_rating",
    "comfort_rating",
    "formality_rating",
    "rain_rating",
    "wind_rating",
}


class IdentityNotFoundError(Exception):
    pass


class ClothingCategoryNotFoundError(Exception):
    pass


class ClothingItemNotFoundError(Exception):
    pass


class InvalidClothingUpdateError(Exception):
    pass


def list_categories():
    connection = get_connection()

    try:
        return repository.list_categories(connection)
    finally:
        connection.close()


def list_colors():
    connection = get_connection()

    try:
        return repository.list_colors(connection)
    finally:
        connection.close()


def _get_identity_id_or_raise(connection, public_id: str):
    identity_id = repository.get_identity_id_by_public_id(connection, public_id)
    if not identity_id:
        raise IdentityNotFoundError
    return identity_id


def _get_category_id_or_raise(connection, category_name: str):
    category_id = repository.get_category_id_by_name(connection, category_name)
    if not category_id:
        raise ClothingCategoryNotFoundError
    return category_id


def create_item(public_id: str, data):
    connection = get_connection()

    try:
        identity_id = _get_identity_id_or_raise(connection, public_id)
        category_id = _get_category_id_or_raise(connection, data.category_name)
        item_id = repository.create_item(connection, identity_id, category_id, data)
        connection.commit()
        return repository.get_item_for_identity(connection, identity_id, item_id)
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def list_items(public_id: str):
    connection = get_connection()

    try:
        identity_id = _get_identity_id_or_raise(connection, public_id)
        return repository.list_items_for_identity(connection, identity_id)
    finally:
        connection.close()


def get_item(public_id: str, item_id: int):
    connection = get_connection()

    try:
        identity_id = _get_identity_id_or_raise(connection, public_id)
        item = repository.get_item_for_identity(connection, identity_id, item_id)
    finally:
        connection.close()

    if not item:
        raise ClothingItemNotFoundError

    return item


def update_item(public_id: str, item_id: int, changes: dict):
    for field_name in NON_NULL_UPDATE_FIELDS:
        if field_name in changes and changes[field_name] is None:
            raise InvalidClothingUpdateError(f"{field_name} cannot be null")

    connection = get_connection()

    try:
        identity_id = _get_identity_id_or_raise(connection, public_id)
        item = repository.get_item_for_identity(connection, identity_id, item_id)
        if not item:
            raise ClothingItemNotFoundError

        if "category_name" in changes:
            changes["category_id"] = _get_category_id_or_raise(connection, changes.pop("category_name"))

        repository.update_item(connection, identity_id, item_id, changes)
        connection.commit()
        return repository.get_item_for_identity(connection, identity_id, item_id)
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def update_item_status(public_id: str, item_id: int, current_status: str):
    connection = get_connection()

    try:
        identity_id = _get_identity_id_or_raise(connection, public_id)
        item = repository.get_item_for_identity(connection, identity_id, item_id)
        if not item:
            raise ClothingItemNotFoundError

        repository.update_item_status(connection, identity_id, item_id, current_status)
        connection.commit()
        return repository.get_item_for_identity(connection, identity_id, item_id)
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def delete_item(public_id: str, item_id: int):
    connection = get_connection()

    try:
        identity_id = _get_identity_id_or_raise(connection, public_id)
        item = repository.get_item_for_identity(connection, identity_id, item_id)
        if not item:
            raise ClothingItemNotFoundError

        repository.soft_delete_item(connection, identity_id, item_id)
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

    return {"message": "Clothing item deleted"}
