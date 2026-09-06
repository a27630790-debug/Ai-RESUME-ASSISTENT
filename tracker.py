from datetime import datetime, date
from database.database import get_connection, VALID_STATUSES


def add_application(
    company: str,
    job_title: str,
    job_url: str = "",
    date_applied: str = "",
    resume_used: str = "",
    cover_letter_used: str = "",
    job_description: str = "",
    interview_date: str = "",
    notes: str = "",
    status: str = "Saved",
    follow_up_reminder: str = "",
) -> int:
    if status not in VALID_STATUSES:
        raise ValueError(f"Invalid status '{status}'. Must be one of {VALID_STATUSES}")

    now = datetime.utcnow().isoformat()
    conn = get_connection()
    cur = conn.execute(
        """
        INSERT INTO applications
        (company, job_title, job_url, date_applied, resume_used, cover_letter_used,
         job_description, interview_date, notes, status, follow_up_reminder,
         created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (company, job_title, job_url, date_applied, resume_used, cover_letter_used,
         job_description, interview_date, notes, status, follow_up_reminder, now, now),
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


def update_application_status(application_id: int, new_status: str):
    if new_status not in VALID_STATUSES:
        raise ValueError(f"Invalid status '{new_status}'. Must be one of {VALID_STATUSES}")
    conn = get_connection()
    conn.execute(
        "UPDATE applications SET status = ?, updated_at = ? WHERE id = ?",
        (new_status, datetime.utcnow().isoformat(), application_id),
    )
    conn.commit()
    conn.close()


def update_application(application_id: int, **fields):
    """Update any subset of columns, e.g. update_application(3, notes='Called HR', interview_date='2026-09-10')"""
    if not fields:
        return
    allowed = {
        "company", "job_title", "job_url", "date_applied", "resume_used",
        "cover_letter_used", "job_description", "interview_date", "notes",
        "status", "follow_up_reminder",
    }
    updates = {k: v for k, v in fields.items() if k in allowed}
    if "status" in updates and updates["status"] not in VALID_STATUSES:
        raise ValueError(f"Invalid status '{updates['status']}'. Must be one of {VALID_STATUSES}")
    if not updates:
        return

    set_clause = ", ".join(f"{k} = ?" for k in updates)
    values = list(updates.values()) + [datetime.utcnow().isoformat(), application_id]

    conn = get_connection()
    conn.execute(
        f"UPDATE applications SET {set_clause}, updated_at = ? WHERE id = ?",
        values,
    )
    conn.commit()
    conn.close()


def delete_application(application_id: int):
    conn = get_connection()
    conn.execute("DELETE FROM applications WHERE id = ?", (application_id,))
    conn.commit()
    conn.close()


def get_application(application_id: int) -> dict:
    conn = get_connection()
    row = conn.execute("SELECT * FROM applications WHERE id = ?", (application_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def list_applications(status: str = None) -> list:
    conn = get_connection()
    if status:
        rows = conn.execute(
            "SELECT * FROM applications WHERE status = ? ORDER BY created_at DESC", (status,)
        ).fetchall()
    else:
        rows = conn.execute("SELECT * FROM applications ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def applications_needing_followup(days_threshold: int = 7) -> list:
    """
    Returns applications still in 'Applied' status where date_applied is
    older than days_threshold. Pure date arithmetic — no AI involved, so
    this is always factually accurate, never a guess.
    """
    apps = list_applications(status="Applied")
    needing_followup = []
    today = date.today()

    for app in apps:
        if not app.get("date_applied"):
            continue
        try:
            applied_date = datetime.fromisoformat(app["date_applied"]).date()
        except ValueError:
            continue
        days_since = (today - applied_date).days
        if days_since >= days_threshold:
            needing_followup.append({**app, "days_since_applied": days_since})

    return needing_followup
