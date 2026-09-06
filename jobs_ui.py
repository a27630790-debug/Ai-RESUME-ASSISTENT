import streamlit as st
import tempfile

from jobs.analyzer import analyze_job_description
from jobs.matcher import match_resume_to_job
from resume.tailoring import tailor_resume_to_job
from coverletter.generator import generate_cover_letter
from ui.resume_ui import _get_resume_text


def render_jd_analyzer(manager):
    st.header("📋 Job Description Analyzer")
    jd_text = st.text_area("Paste the job description", height=250, key="jd_text_input")
    if st.button("Analyze Job Description") and jd_text:
        with st.spinner("Analyzing..."):
            try:
                result = analyze_job_description(manager, jd_text)
                st.session_state["last_jd_text"] = jd_text
                st.subheader(result.get("job_title", "Job"))
                st.markdown("**Required Skills**")
                st.write(", ".join(result.get("required_skills", [])) or "—")
                st.markdown("**Preferred Skills**")
                st.write(", ".join(result.get("preferred_skills", [])) or "—")
                st.markdown(f"**Experience Required:** {result.get('experience_required', '—')}")
                st.markdown(f"**Education Required:** {result.get('education_required', '—')}")
                st.markdown("**Responsibilities**")
                for r in result.get("responsibilities", []):
                    st.write(f"- {r}")
                st.markdown("**Keywords**")
                st.write(", ".join(result.get("keywords", [])) or "—")
            except Exception as e:
                st.error(f"AI service is temporarily busy: {e}")


def render_job_match(manager):
    st.header("🎯 Resume vs Job Match")
    resume_text = _get_resume_text()
    jd_text = st.text_area(
        "Paste the job description",
        value=st.session_state.get("last_jd_text", ""),
        height=200, key="match_jd_input",
    )

    if not resume_text:
        st.info("Create or upload a resume first (see Create Resume / Upload Resume).")
        return

    if st.button("Check Match") and jd_text:
        with st.spinner("Comparing..."):
            try:
                result = match_resume_to_job(manager, resume_text, jd_text)
                st.metric("Match", f"{result.get('match_percentage', '?')}%")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**✅ Matching Skills**")
                    for s in result.get("matching_skills", []):
                        st.write(f"- {s}")
                with col2:
                    st.markdown("**❌ Missing Skills**")
                    for s in result.get("missing_skills", []):
                        st.write(f"- {s}")
                st.markdown("**Strengths**")
                for s in result.get("strengths", []):
                    st.write(f"- {s}")
                st.markdown("**Weaknesses**")
                for w in result.get("weaknesses", []):
                    st.write(f"- {w}")
                st.markdown("**Recommendations**")
                for r in result.get("recommendations", []):
                    st.write(f"- {r}")
            except Exception as e:
                st.error(f"AI service is temporarily busy: {e}")


def render_tailor_resume(manager):
    st.header("✂️ Tailor Resume to a Job")
    resume_text = _get_resume_text()
    jd_text = st.text_area(
        "Paste the job description",
        value=st.session_state.get("last_jd_text", ""),
        height=200, key="tailor_jd_input",
    )

    if not resume_text:
        st.info("Create or upload a resume first.")
        return

    if st.button("Tailor My Resume") and jd_text:
        with st.spinner("Tailoring..."):
            try:
                result = tailor_resume_to_job(manager, resume_text, jd_text)
                st.markdown("**Tailored Summary**")
                st.write(result.get("tailored_summary", ""))
                st.markdown("**Prioritized Skills**")
                st.write(", ".join(result.get("prioritized_skills", [])))
                st.markdown("**Rewritten Bullets**")
                for b in result.get("rewritten_bullets", []):
                    st.write(f"- Original: {b.get('original')}")
                    st.write(f"  → Tailored: {b.get('tailored')}")
                st.markdown("**Keywords You Could Naturally Add**")
                st.write(", ".join(result.get("keywords_to_naturally_add", [])))
            except Exception as e:
                st.error(f"AI service is temporarily busy: {e}")


def render_cover_letter(manager):
    st.header("✉️ Cover Letter Generator")
    resume_text = _get_resume_text()
    jd_text = st.text_area(
        "Paste the job description",
        value=st.session_state.get("last_jd_text", ""),
        height=200, key="cl_jd_input",
    )
    col1, col2 = st.columns(2)
    with col1:
        company = st.text_input("Company Name")
        role = st.text_input("Role Title")
    with col2:
        tone = st.selectbox("Tone", ["professional", "professional but warm", "formal", "enthusiastic"])
        length = st.selectbox("Length", ["short (3 paragraphs)", "medium (3-4 paragraphs)", "long (4-5 paragraphs)"])

    if not resume_text:
        st.info("Create or upload a resume first.")
        return

    if st.button("Generate Cover Letter") and jd_text:
        with st.spinner("Writing..."):
            try:
                letter = generate_cover_letter(manager, resume_text, jd_text, company, role, tone, length)
                st.text_area("Your Cover Letter", value=letter, height=400)
                st.download_button("Download as TXT", letter, file_name="cover_letter.txt")
            except Exception as e:
                st.error(f"AI service is temporarily busy: {e}")
