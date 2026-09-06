import streamlit as st

from database.database import init_db
from auth.authentication import register_user, login_user, create_guest_session, AuthError
from ai.provider_manager import AIProviderManager

from ui.resume_ui import render_create_resume, render_upload_resume, render_resume_analyzer, render_ats_analyzer
from ui.jobs_ui import render_jd_analyzer, render_job_match, render_tailor_resume, render_cover_letter
from ui.career_ui import render_career_chat, render_career_roadmap, render_interview_prep
from ui.tracker_ui import render_application_tracker, render_analytics

st.set_page_config(page_title="CareerPilot AI", page_icon="🧭", layout="wide")

init_db()


@st.cache_resource
def get_ai_manager():
    return AIProviderManager()


manager = get_ai_manager()


# ============================================================
# Auth — Guest Mode is always available, login/register optional
# ============================================================
def render_auth_sidebar():
    st.sidebar.markdown("### Account")

    if st.session_state.get("user"):
        user = st.session_state["user"]
        label = user.get("full_name") or user.get("email") or "Guest"
        st.sidebar.success(f"Signed in as {label}")
        if st.sidebar.button("Log out"):
            st.session_state["user"] = None
            st.rerun()
        return

    tab1, tab2, tab3 = st.sidebar.tabs(["Guest", "Login", "Register"])

    with tab1:
        st.write("No account needed — your work stays in this session only.")
        if st.button("Continue as Guest"):
            st.session_state["user"] = create_guest_session()
            st.rerun()

    with tab2:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Log In"):
            try:
                user = login_user(email, password)
                st.session_state["user"] = user
                st.rerun()
            except AuthError as e:
                st.error(str(e))

    with tab3:
        reg_name = st.text_input("Full Name", key="reg_name")
        reg_email = st.text_input("Email", key="reg_email")
        reg_password = st.text_input("Password (min 8 chars)", type="password", key="reg_password")
        if st.button("Create Account"):
            try:
                user = register_user(reg_email, reg_password, reg_name)
                st.session_state["user"] = user
                st.success("Account created!")
                st.rerun()
            except AuthError as e:
                st.error(str(e))


render_auth_sidebar()

if not st.session_state.get("user"):
    st.title("🧭 CareerPilot AI")
    st.write("Your AI-Powered Career Companion")
    st.info("👈 Continue as Guest, or Log In / Register from the sidebar to get started.")
    st.stop()


# ============================================================
# Main navigation
# ============================================================
PAGES = {
    "Create Resume": lambda: render_create_resume(),
    "Upload Resume": lambda: render_upload_resume(),
    "Resume Analyzer": lambda: render_resume_analyzer(manager),
    "ATS Analyzer": lambda: render_ats_analyzer(manager),
    "Job Description Analyzer": lambda: render_jd_analyzer(manager),
    "Job Match": lambda: render_job_match(manager),
    "Tailor Resume": lambda: render_tailor_resume(manager),
    "Cover Letter": lambda: render_cover_letter(manager),
    "Career Chat": lambda: render_career_chat(manager),
    "Career Roadmap": lambda: render_career_roadmap(manager),
    "Interview Preparation": lambda: render_interview_prep(manager),
    "Application Tracker": lambda: render_application_tracker(),
    "Analytics": lambda: render_analytics(manager),
}

st.sidebar.markdown("### CareerPilot AI 🧭")
choice = st.sidebar.radio("Navigate", list(PAGES.keys()), label_visibility="collapsed")

PAGES[choice]()
