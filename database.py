"""
Database helper module for the Cybersecurity Portfolio website.
"""

import os

import psycopg2


DATABASE_URL = os.environ.get("DATABASE_URL")


def get_db_connection():
    """Open a PostgreSQL database connection."""

    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not set.")

    return psycopg2.connect(DATABASE_URL)


def init_db():
    """Create the messages table if it does not exist."""

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL
        )
    """)

    connection.commit()

    cursor.close()
    connection.close()


def insert_message(name, email, message):
    """Save a contact form submission."""

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO messages (
            name,
            email,
            message,
            created_at
        )
        VALUES (%s, %s, %s, NOW())
    """, (
        name,
        email,
        message,
    ))

    connection.commit()

    cursor.close()
    connection.close()