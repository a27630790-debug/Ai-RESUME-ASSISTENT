import hashlib
import secrets


def hash_password(password: str, salt: str = None) -> tuple:
    """
    Returns (password_hash, salt). Uses PBKDF2-HMAC-SHA256, which is in
    Python's standard library — no extra dependency needed, and secure
    enough for this project's threat model.
    """
    if salt is None:
        salt = secrets.token_hex(16)
    pwd_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), 100_000
    ).hex()
    return pwd_hash, salt


def verify_password(password: str, stored_hash: str, salt: str) -> bool:
    computed_hash, _ = hash_password(password, salt)
    return secrets.compare_digest(computed_hash, stored_hash)
