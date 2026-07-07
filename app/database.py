import pymysql

from app.config import get_database_config


def get_connection():
    config = get_database_config()

    missing = [key for key, value in config.items() if value in (None, "")]
    if missing:
        raise RuntimeError(f"Missing database config: {', '.join(missing)}")

    return pymysql.connect(
        **config,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False,
    )
