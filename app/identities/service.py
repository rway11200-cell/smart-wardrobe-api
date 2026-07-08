from uuid import uuid4

from app.database import get_connection
from app.identities import repository


class IdentityNotFoundError(Exception):
    pass


def create_identity(data):
    public_id = str(uuid4())
    connection = get_connection()

    try:
        identity_id = repository.create_identity(connection, public_id, data.display_name)
        repository.create_profile(connection, identity_id)
        connection.commit()
        return repository.get_identity_by_public_id(connection, public_id)
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def get_identity(public_id: str):
    connection = get_connection()

    try:
        identity = repository.get_identity_by_public_id(connection, public_id)
    finally:
        connection.close()

    if not identity:
        raise IdentityNotFoundError

    return identity


def list_identities():
    connection = get_connection()

    try:
        return repository.list_identities(connection)
    finally:
        connection.close()


def update_identity_profile(public_id: str, changes: dict):
    connection = get_connection()

    try:
        identity_id = repository.get_internal_identity_id(connection, public_id)
        if not identity_id:
            raise IdentityNotFoundError

        repository.update_profile(connection, identity_id, changes)
        connection.commit()
        return repository.get_identity_by_public_id(connection, public_id)
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
