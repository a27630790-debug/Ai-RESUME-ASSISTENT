import uuid
import re
from database.database import get_connection
from auth.security import hash_password, verify_password

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class AuthError(Exception):
    pass


def register_user(email: str, password: str, full_name: str = "") -> dict:
    """
    Email + password registration. Login is always optional in CareerPilot AI
    (see create_guest_session) — this is only used when the user actively
    chooses to create an account.
    """
    email = email.strip().lower()
    if not EMAIL_REGEX.match(email):
        raise AuthError("Invalid email format")
    if len(password) < 8:
        raise AuthError("Password must be at least 8 characters")

    conn = get_connection()
    existing = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
    if existing:
        conn.close()
        raise AuthError("An account with this email already exists")

    pwd_hash, salt = hash_password(password)
    cur = conn.execute(
        """INSERT INTO users (email, password_hash, password_salt, full_name, auth_provider)
           VALUES (?, ?, ?, ?, 'email')""",
        (email, pwd_hash, salt, full_name),
    )
    conn.commit()
    user_id = cur.lastrowid
    conn.close()
    return {"id": user_id, "email": email, "full_name": full_name, "auth_provider": "email"}


def login_user(email: str, password: str) -> dict:
    """Returns user dict on success. Raises AuthError on failure (never
    reveals whether the email or the password was wrong, to avoid leaking
    which emails are registered)."""
    email = email.strip().lower()
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()

    if not row or row["auth_provider"] != "email":
        raise AuthError("Invalid email or password")
    if not verify_password(password, row["password_hash"], row["password_salt"]):
        raise AuthError("Invalid email or password")

    return {
        "id": row["id"], "email": row["email"], "full_name": row["full_name"],
        "auth_provider": row["auth_provider"], "is_admin": bool(row["is_admin"]),
    }


def get_user_by_id(user_id: int) -> dict:
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def create_guest_session() -> dict:
    """
    Guest mode needs no database row — CareerPilot AI never forces
    registration. Just a temporary in-memory identifier for this session's
    data (e.g. to namespace uploaded files), cleaned up when the session ends.
    """
    return {"guest_id": str(uuid.uuid4()), "is_guest": True}
