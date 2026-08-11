"""
Database helper module for the Cybersecurity Portfolio website.
"""

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


def init_db():
    """Create the messages table if it does not exist."""

    connection = get_db_connection()

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
    connection.close()


def insert_message(name, email, message):
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
    connection.close()