"""SQLite persistence helpers for meeting history."""

import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / "database"
DB_PATH = DB_DIR / "app.db"


def init_db() -> None:
    """Create the application database and tables if they do not exist."""
    DB_DIR.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS meeting_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT,
                ai_result TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def save_meeting(content: str, ai_result: str) -> None:
    """Save one meeting summary result."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO meeting_history (
                content,
                ai_result
            )
            VALUES (?, ?)
            """,
            (content, ai_result),
        )


def get_history() -> list[tuple[int, str, str, str]]:
    """Return saved meeting summaries with newest records first."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            """
            SELECT id, content, ai_result, created_at
            FROM meeting_history
            ORDER BY created_at DESC, id DESC
            """
        )
        return cursor.fetchall()
