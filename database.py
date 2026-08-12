"""
Database helper module for the Cybersecurity Portfolio website.
"""

<<<<<<< HEAD
import os

import psycopg2


DATABASE_URL = os.environ.get("DATABASE_URL")


def get_db_connection():
    """Open a PostgreSQL database connection."""

    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not set.")

    return psycopg2.connect(DATABASE_URL)
=======
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


DATABASE_PATH = Path(__file__).parent / "database" / "portfolio.db"


def get_db_connection():
    """Open a new SQLite connection."""
    DATABASE_PATH.parent.mkdir(exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    return connection
>>>>>>> f27048b0c3790e7bb978eddf0649a6b84d153492


def init_db():
    """Create the messages table if it does not exist."""

    connection = get_db_connection()
<<<<<<< HEAD
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
=======

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )

    connection.commit()
>>>>>>> f27048b0c3790e7bb978eddf0649a6b84d153492
    connection.close()


def insert_message(name, email, message):
<<<<<<< HEAD
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
=======
    """Insert a contact form submission."""

    connection = get_db_connection()

    connection.execute(
        """
        INSERT INTO messages
        (name, email, message, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (
            name,
            email,
            message,
            datetime.now(timezone.utc).isoformat(),
        ),
    )

    connection.commit()
>>>>>>> f27048b0c3790e7bb978eddf0649a6b84d153492
    connection.close()