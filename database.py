import os
import psycopg
from datetime import datetime, timezone


DATABASE_URL = os.environ.get("DATABASE_URL")


def get_db_connection():
    """Open a PostgreSQL database connection."""

    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not set.")

    return psycopg.connect(DATABASE_URL)


def init_db():
    """Create the messages table if it does not exist."""

    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    message TEXT NOT NULL,
                    created_at TIMESTAMPTZ NOT NULL
                )
                """
            )

        connection.commit()

    finally:
        connection.close()


def insert_message(name, email, message):
    """Insert a contact form submission."""

    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO messages
                (name, email, message, created_at)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    name,
                    email,
                    message,
                    datetime.now(timezone.utc),
                ),
            )

        connection.commit()

    finally:
        connection.close()