import sqlite3
import os

# Development uses SQLite. In production, migrating to Supabase means
# changing only this file — jobs/tracker.py and career/analytics.py talk to
# a plain connection/row interface and won't need to change.
DB_PATH = os.environ.get("CAREERPILOT_DB_PATH", "careerpilot.db")

VALID_STATUSES = ["Saved", "Applied", "Assessment", "Interview", "Offer", "Rejected"]

SCHEMA = """
CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT NOT NULL,
    job_title TEXT NOT NULL,
    job_url TEXT,
    date_applied TEXT,
    resume_used TEXT,
    cover_letter_used TEXT,
    job_description TEXT,
    interview_date TEXT,
    notes TEXT,
    status TEXT NOT NULL DEFAULT 'Saved',
    follow_up_reminder TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT,
    password_salt TEXT,
    full_name TEXT,
    auth_provider TEXT NOT NULL DEFAULT 'email',
    is_admin INTEGER NOT NULL DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
"""


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()
