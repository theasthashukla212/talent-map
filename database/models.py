"""
database/models.py
------------------
All CRUD operations for Talent Map.

Passwords are hashed with bcrypt (never stored in plain text).
"""

import bcrypt
from database.db import get_connection


# ═══════════════════════════════════════════════════════════════
# ── USERS ──────────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════

def create_user(name: str, email: str, plain_password: str) -> dict | None:
    """
    Create a new user. Returns the user dict on success,
    or None if the email is already registered.
    """
    email = email.strip().lower()
    pw_hash = bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt()).decode()
    try:
        with get_connection() as conn:
            cur = conn.execute(
                "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                (name.strip(), email, pw_hash),
            )
            user_id = cur.lastrowid
        return {"id": user_id, "name": name.strip(), "email": email}
    except Exception:
        return None  # email already exists (UNIQUE constraint)


def get_user_by_email(email: str) -> dict | None:
    """Return user row as dict, or None if not found."""
    email = email.strip().lower()
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id, name, email, password_hash FROM users WHERE email = ?",
            (email,),
        ).fetchone()
    if row is None:
        return None
    return dict(row)


def verify_password(plain_password: str, stored_hash: str) -> bool:
    """Check a plain-text password against a stored bcrypt hash."""
    return bcrypt.checkpw(plain_password.encode(), stored_hash.encode())


# ═══════════════════════════════════════════════════════════════
# ── RECOMMENDATIONS ────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════

def save_recommendation(
    user_id: int,
    top_career: str,
    top_score: float,
    best_domain: str = "",
) -> int:
    """
    Persist a recommendation result for a user.
    Returns the new row id.
    """
    with get_connection() as conn:
        cur = conn.execute(
            """INSERT INTO recommendations (user_id, top_career, top_score, best_domain)
               VALUES (?, ?, ?, ?)""",
            (user_id, top_career, round(top_score, 4), best_domain),
        )
        return cur.lastrowid


def get_user_recommendations(user_id: int, limit: int = 10) -> list[dict]:
    """Return the most recent recommendations for a user."""
    with get_connection() as conn:
        rows = conn.execute(
            """SELECT top_career, top_score, best_domain, created_at
               FROM recommendations
               WHERE user_id = ?
               ORDER BY created_at DESC
               LIMIT ?""",
            (user_id, limit),
        ).fetchall()
    return [dict(r) for r in rows]


# ═══════════════════════════════════════════════════════════════
# ── FEEDBACK ───────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════

def save_feedback(
    rating: int,
    category: str,
    comments: str,
    user_id: int | None = None,
    user_name: str = "Anonymous",
) -> int:
    """Persist a feedback entry. Returns the new row id."""
    with get_connection() as conn:
        cur = conn.execute(
            """INSERT INTO feedback (user_id, user_name, rating, category, comments)
               VALUES (?, ?, ?, ?, ?)""",
            (user_id, user_name, rating, category, comments.strip()),
        )
        return cur.lastrowid


def get_all_feedback(limit: int = 20) -> list[dict]:
    """Return most recent feedback entries (newest first)."""
    with get_connection() as conn:
        rows = conn.execute(
            """SELECT user_name, rating, category, comments, created_at
               FROM feedback
               ORDER BY created_at DESC
               LIMIT ?""",
            (limit,),
        ).fetchall()
    return [dict(r) for r in rows]


# ═══════════════════════════════════════════════════════════════
# ── CONTACT MESSAGES ───────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════

def save_contact_message(
    name: str,
    email: str,
    subject: str,
    message: str,
) -> int:
    """Persist a contact-form submission. Returns the new row id."""
    with get_connection() as conn:
        cur = conn.execute(
            """INSERT INTO contact_messages (name, email, subject, message)
               VALUES (?, ?, ?, ?)""",
            (name.strip(), email.strip().lower(), subject, message.strip()),
        )
        return cur.lastrowid
