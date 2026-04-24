"""
database/db.py
--------------
SQLite connection & table initialisation for Talent Map.

For local development: creates talent_map.db in the project root.
For Streamlit Cloud:   same file (ephemeral but functional for demo);
                       swap to PostgreSQL by setting DATABASE_URL secret.
"""

import sqlite3
from pathlib import Path

# ── DB file location ──────────────────────────────────────────────────────────
_DB_PATH = Path(__file__).parent.parent / "talent_map.db"


def get_connection() -> sqlite3.Connection:
    """Return a new SQLite connection with row_factory set to dict-like rows."""
    conn = sqlite3.connect(str(_DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row          # rows behave like dicts
    conn.execute("PRAGMA journal_mode=WAL")  # safe concurrent access
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db() -> None:
    """Create all tables if they do not already exist."""
    ddl = """
    -- Users table
    CREATE TABLE IF NOT EXISTS users (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        name          TEXT    NOT NULL,
        email         TEXT    NOT NULL UNIQUE,
        password_hash TEXT    NOT NULL,
        created_at    TEXT    NOT NULL DEFAULT (datetime('now'))
    );

    -- Recommendations saved per user
    CREATE TABLE IF NOT EXISTS recommendations (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        top_career  TEXT    NOT NULL,
        top_score   REAL    NOT NULL,
        best_domain TEXT,
        created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
    );

    -- Feedback submissions
    CREATE TABLE IF NOT EXISTS feedback (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id    INTEGER REFERENCES users(id) ON DELETE SET NULL,
        user_name  TEXT    NOT NULL DEFAULT 'Anonymous',
        rating     INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
        category   TEXT    NOT NULL,
        comments   TEXT    NOT NULL,
        created_at TEXT    NOT NULL DEFAULT (datetime('now'))
    );

    -- Contact-form messages
    CREATE TABLE IF NOT EXISTS contact_messages (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        name       TEXT NOT NULL,
        email      TEXT NOT NULL,
        subject    TEXT NOT NULL,
        message    TEXT NOT NULL,
        created_at TEXT NOT NULL DEFAULT (datetime('now'))
    );
    """
    with get_connection() as conn:
        conn.executescript(ddl)
