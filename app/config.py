import os
from urllib.parse import urlparse

from dotenv import load_dotenv

load_dotenv()


def get_database_config():
    database_url = os.getenv("DATABASE_URL")

    if database_url:
        parsed = urlparse(database_url)
        return {
            "host": parsed.hostname,
            "port": parsed.port or 3306,
            "user": parsed.username,
            "password": parsed.password,
            "database": parsed.path.lstrip("/"),
        }

    return {
        "host": os.getenv("MYSQL_HOST") or os.getenv("MYSQLHOST"),
        "port": int(os.getenv("MYSQL_PORT") or os.getenv("MYSQLPORT") or "3306"),
        "user": os.getenv("MYSQL_USER") or os.getenv("MYSQLUSER"),
        "password": os.getenv("MYSQL_PASSWORD") or os.getenv("MYSQLPASSWORD"),
        "database": os.getenv("MYSQL_DATABASE") or os.getenv("MYSQLDATABASE"),
    }
