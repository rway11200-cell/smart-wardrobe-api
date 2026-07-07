from pathlib import Path

from app.database import get_connection

MIGRATIONS_DIR = Path(__file__).parent / "migrations"


def ensure_migrations_table(connection):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS schema_migrations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                filename VARCHAR(255) NOT NULL UNIQUE,
                executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
    connection.commit()


def get_executed_migrations(connection):
    with connection.cursor() as cursor:
        cursor.execute("SELECT filename FROM schema_migrations")
        rows = cursor.fetchall()
    return {row["filename"] for row in rows}


def run_migration(connection, path):
    sql = path.read_text(encoding="utf-8")

    with connection.cursor() as cursor:
        for statement in sql.split(";"):
            statement = statement.strip()
            if statement:
                cursor.execute(statement)

        cursor.execute(
            "INSERT INTO schema_migrations (filename) VALUES (%s)",
            (path.name,),
        )

    connection.commit()
    print(f"Applied migration: {path.name}")


def run_migrations():
    connection = get_connection()
    try:
        ensure_migrations_table(connection)
        executed = get_executed_migrations(connection)

        for path in sorted(MIGRATIONS_DIR.glob("*.sql")):
            if path.name not in executed:
                run_migration(connection, path)
    finally:
        connection.close()


if __name__ == "__main__":
    run_migrations()
