"""SQLite persistence for packages and their tracking history."""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "tracking_system.db"


def _connect() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def create_tables() -> None:
    with _connect() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS packages (
                tracking_number TEXT PRIMARY KEY,
                sender TEXT,
                recipient TEXT NOT NULL
            )
        """)
        connection.execute("""
            CREATE TABLE IF NOT EXISTS tracking_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tracking_number TEXT NOT NULL,
                status TEXT NOT NULL,
                location TEXT NOT NULL,
                note TEXT NOT NULL DEFAULT '',
                timestamp TEXT NOT NULL,
                FOREIGN KEY (tracking_number)
                    REFERENCES packages (tracking_number)
            )
        """)


def save_package(tracking_number: str, recipient: str) -> None:
    with _connect() as connection:
        connection.execute(
            "INSERT INTO packages (tracking_number, recipient) VALUES (?, ?)",
            (tracking_number, recipient),
        )


def save_tracking_event(tracking_number: str, status: str, location: str,
                        note: str, timestamp: str) -> None:
    with _connect() as connection:
        connection.execute(
            """INSERT INTO tracking_events
               (tracking_number, status, location, note, timestamp)
               VALUES (?, ?, ?, ?, ?)""",
            (tracking_number, status, location, note, timestamp),
        )


def load_packages() -> list[sqlite3.Row]:
    with _connect() as connection:
        return connection.execute(
            "SELECT tracking_number, recipient FROM packages ORDER BY tracking_number"
        ).fetchall()


def load_tracking_events(tracking_number: str) -> list[sqlite3.Row]:
    with _connect() as connection:
        return connection.execute(
            """SELECT status, location, note, timestamp
               FROM tracking_events
               WHERE tracking_number = ?
               ORDER BY id""",
            (tracking_number,),
        ).fetchall()

'AI generated method to get the next tracking number based on the existing ones in the database'
def get_next_tracking_number() -> int:
    """Return one higher than the largest numeric PKG tracking number."""
    with _connect() as connection:
        rows = connection.execute(
            "SELECT tracking_number FROM packages WHERE tracking_number LIKE 'PKG-%'"
        ).fetchall()
    numbers = []
    for row in rows:
        suffix = row["tracking_number"][4:]
        if suffix.isdigit():
            numbers.append(int(suffix))
    return max(numbers, default=0) + 1
