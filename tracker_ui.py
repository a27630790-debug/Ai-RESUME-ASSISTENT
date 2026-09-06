import streamlit as st

from jobs.tracker import (
    add_application, update_application_status, update_application,
    delete_application, list_applications, applications_needing_followup,
)
from database.database import VALID_STATUSES
from career.analytics import compute_stats, generate_ai_insights


def render_application_tracker():
    st.header("📌 Job Application Tracker")

    with st.expander("➕ Add New Application"):
        with st.form("add_app_form"):
            col1, col2 = st.columns(2)
            with col1:
                company = st.text_input("Company")
                job_title = st.text_input("Job Title")
                job_url = st.text_input("Job URL")
            with col2:
                status = st.selectbox("Status", VALID_STATUSES)
                date_applied = st.date_input("Date Applied", value=None)
            notes = st.text_area("Notes")
            submitted = st.form_submit_button("Add Application")

        if submitted and company and job_title:
            add_application(
                company=company, job_title=job_title, job_url=job_url,
                date_applied=date_applied.isoformat() if date_applied else "",
                status=status, notes=notes,
            )
            st.success(f"Added {job_title} at {company}")
            st.rerun()

    followups = applications_needing_followup()
    if followups:
        st.warning(f"⏰ {len(followups)} application(s) need a follow-up (7+ days, no response)")
        for f in followups:
            st.write(f"- **{f['company']}** ({f['job_title']}) — {f['days_since_applied']} days ago")

    st.divider()
    filter_status = st.selectbox("Filter by status", ["All"] + VALID_STATUSES)
    apps = list_applications(status=None if filter_status == "All" else filter_status)

    for app in apps:
        with st.expander(f"[{app['status']}] {app['job_title']} at {app['company']}"):
            col1, col2 = st.columns(2)
            with col1:
                new_status = st.selectbox(
                    "Status", VALID_STATUSES, index=VALID_STATUSES.index(app["status"]),
                    key=f"status_{app['id']}",
                )
                if new_status != app["status"]:
                    update_application_status(app["id"], new_status)
                    st.rerun()
            with col2:
                if st.button("Delete", key=f"delete_{app['id']}"):
                    delete_application(app["id"])
                    st.rerun()
            st.write(f"URL: {app['job_url'] or '—'}")
            st.write(f"Applied: {app['date_applied'] or '—'}")
            new_notes = st.text_area("Notes", value=app["notes"] or "", key=f"notes_{app['id']}")
            if new_notes != app["notes"]:
                update_application(app["id"], notes=new_notes)


def render_analytics(manager):
    st.header("📈 Analytics")
    stats = compute_stats()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Applications", stats["total_applications"])
    col2.metric("Interviews", stats["interviews"])
    col3.metric("Offers", stats["offers"])
    col4.metric("Response Rate", f"{stats['response_rate_percent']}%")

    st.subheader("By Status")
    st.bar_chart(stats["by_status"])

    if st.button("Get AI Insights"):
        with st.spinner("Analyzing your progress..."):
            try:
                st.info(generate_ai_insights(manager, stats))
            except Exception as e:
                st.error(f"AI service is temporarily busy: {e}")
