from uuid import uuid4

import pymysql

from app.database import get_connection
from app.identities import repository


class IdentityNotFoundError(Exception):
    pass


class NicknameAlreadyInUseError(Exception):
    pass


def _normalize_nickname(nickname: str) -> str:
    return nickname.strip().lower()


def create_identity(data):
    public_id = str(uuid4())
    nickname = _normalize_nickname(data.nickname)
    connection = get_connection()

    try:
        identity_id = repository.create_identity(connection, public_id, data.display_name, nickname)
        repository.create_profile(connection, identity_id)
        connection.commit()
        return repository.get_identity_by_public_id(connection, public_id)
    except pymysql.err.IntegrityError as error:
        connection.rollback()
        if error.args and error.args[0] == 1062:
            raise NicknameAlreadyInUseError
        raise
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


def get_identity_by_nickname(nickname: str):
    connection = get_connection()

    try:
        identity = repository.get_identity_by_nickname(connection, _normalize_nickname(nickname))
    finally:
        connection.close()

    if not identity:
        raise IdentityNotFoundError

    return identity


def list_identities(name: str | None = None):
    connection = get_connection()

    try:
        return repository.list_identities(connection, name)
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
