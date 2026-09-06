import streamlit as st
import tempfile
import os

from resume.builder import build_resume_from_answers
from resume.parser import extract_text
from resume.analyzer import analyze_resume, rewrite_bullet
from resume.ats import analyze_ats_score
from exports.txt import export_txt
from exports.json_export import export_json
from exports.docx_export import export_docx
from exports.pdf_export import export_pdf


def _get_resume_text() -> str:
    """Returns text for whichever resume is currently active in session."""
    if st.session_state.get("resume_text"):
        return st.session_state["resume_text"]
    if st.session_state.get("resume_obj"):
        return export_txt(st.session_state["resume_obj"])
    return ""


def render_create_resume():
    st.header("📝 Create Resume")
    st.caption("Fill in what applies to you — leave anything blank that doesn't apply.")

    with st.form("resume_form"):
        col1, col2 = st.columns(2)
        with col1:
            full_name = st.text_input("Full Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
        with col2:
            headline = st.text_input("Professional Headline")
            location = st.text_input("Location")
            linkedin = st.text_input("LinkedIn URL")

        github = st.text_input("GitHub URL")
        summary = st.text_area("Professional Summary")
        skills = st.text_input("Technical Skills (comma-separated)")

        st.markdown("**Work Experience** (one entry — add more via 'My Documents' later)")
        job_title = st.text_input("Job Title")
        company = st.text_input("Company")
        exp_dates = st.text_input("Dates (e.g. 2024 - 2025)")
        bullets_raw = st.text_area("Bullet points (one per line)")

        st.markdown("**Education**")
        degree = st.text_input("Degree")
        institution = st.text_input("Institution")
        edu_dates = st.text_input("Education Dates")

        submitted = st.form_submit_button("Build Resume")

    if submitted:
        answers = {
            "full_name": full_name, "headline": headline, "email": email,
            "phone": phone, "location": location, "linkedin": linkedin,
            "github": github, "professional_summary": summary,
            "technical_skills": [s.strip() for s in skills.split(",") if s.strip()],
            "work_experience": [{
                "job_title": job_title, "company": company,
                "start_date": exp_dates, "end_date": "",
                "bullets": [b.strip() for b in bullets_raw.split("\n") if b.strip()],
            }] if job_title else [],
            "education": [{
                "degree": degree, "institution": institution,
                "start_date": edu_dates, "end_date": "",
            }] if degree else [],
        }
        resume = build_resume_from_answers(answers)
        st.session_state["resume_obj"] = resume
        st.session_state["resume_text"] = export_txt(resume)
        st.success("Resume built! Check the preview below, or go to other tools in the sidebar.")

    if st.session_state.get("resume_obj"):
        st.divider()
        st.subheader("Preview")
        st.text(export_txt(st.session_state["resume_obj"]))
        _render_export_buttons(st.session_state["resume_obj"])


def _render_export_buttons(resume):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.download_button("Download TXT", export_txt(resume), file_name="resume.txt")
    with col2:
        st.download_button("Download JSON", export_json(resume), file_name="resume.json")
    with col3:
        with tempfile.TemporaryDirectory() as tmpdir:
            docx_path = os.path.join(tmpdir, "resume.docx")
            export_docx(resume, docx_path)
            with open(docx_path, "rb") as f:
                st.download_button("Download DOCX", f.read(), file_name="resume.docx")


def render_upload_resume():
    st.header("📤 Upload Resume")
    uploaded = st.file_uploader("Upload PDF, DOCX, or TXT", type=["pdf", "docx", "txt"])

    if uploaded:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, uploaded.name)
            with open(path, "wb") as f:
                f.write(uploaded.getbuffer())
            try:
                text = extract_text(path)
                st.session_state["resume_text"] = text
                st.session_state["resume_obj"] = None  # uploaded text takes priority now
                st.success("Resume uploaded and text extracted.")
                st.text_area("Extracted text (you can edit before analyzing)", value=text, height=300, key="resume_text_edit")
                if st.button("Use this text for analysis"):
                    st.session_state["resume_text"] = st.session_state["resume_text_edit"]
                    st.success("Updated. Go to Resume Analyzer or ATS Analyzer in the sidebar.")
            except Exception as e:
                st.error(f"Could not read file: {e}")


def render_resume_analyzer(manager):
    st.header("🔍 Resume Analyzer")
    resume_text = _get_resume_text()
    if not resume_text:
        st.info("Create or upload a resume first.")
        return

    if st.button("Analyze My Resume"):
        with st.spinner("Analyzing..."):
            try:
                result = analyze_resume(manager, resume_text)
                st.markdown(result)
            except Exception as e:
                st.error(f"AI service is temporarily busy: {e}")

    st.divider()
    st.subheader("Rewrite a bullet point")
    bullet = st.text_input("Paste a bullet point to improve")
    if st.button("Rewrite Bullet") and bullet:
        with st.spinner("Rewriting..."):
            try:
                st.write(rewrite_bullet(manager, bullet))
            except Exception as e:
                st.error(f"AI service is temporarily busy: {e}")


def render_ats_analyzer(manager):
    st.header("📊 ATS Analyzer")
    st.caption("Estimated ATS Guidance — not a real company's actual ATS score.")
    resume_text = _get_resume_text()
    if not resume_text:
        st.info("Create or upload a resume first.")
        return

    if st.button("Run ATS Analysis"):
        with st.spinner("Analyzing..."):
            try:
                result = analyze_ats_score(manager, resume_text)
                st.metric("Estimated ATS Score", f"{result.get('ats_score', '?')}/100")
                st.caption(result.get("score_label", ""))
                st.markdown("**Keyword Optimization**")
                st.write(result.get("keyword_optimization", ""))
                st.markdown("**Formatting Issues**")
                for i in result.get("formatting_issues", []):
                    st.write(f"- {i}")
                st.markdown("**Missing Sections**")
                for s in result.get("missing_sections", []):
                    st.write(f"- {s}")
                st.markdown("**Recommendations**")
                for r in result.get("recommendations", []):
                    st.write(f"- {r}")
            except Exception as e:
                st.error(f"AI service is temporarily busy: {e}")
