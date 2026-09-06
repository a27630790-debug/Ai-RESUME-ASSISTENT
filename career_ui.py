import streamlit as st

from career.assistant import chat_with_assistant
from career.roadmap import generate_roadmap
from career.interview import generate_interview_questions, analyze_interview_answer
from ui.resume_ui import _get_resume_text


def render_career_chat(manager):
    st.header("💬 Career Chat Assistant")

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    with st.expander("Optional: tell the assistant about your target role/skills"):
        target_role = st.text_input("Target role", key="chat_target_role")
        skills = st.text_input("Your key skills", key="chat_skills")

    for turn in st.session_state["chat_history"]:
        with st.chat_message(turn["role"]):
            st.write(turn["content"])

    user_message = st.chat_input("Ask about your resume, career path, interviews...")
    if user_message:
        st.session_state["chat_history"].append({"role": "user", "content": user_message})
        with st.chat_message("user"):
            st.write(user_message)

        user_context = {"target_role": target_role, "skills": skills}
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    reply = chat_with_assistant(
                        manager, st.session_state["chat_history"][:-1], user_message, user_context
                    )
                    st.write(reply)
                    st.session_state["chat_history"].append({"role": "assistant", "content": reply})
                except Exception as e:
                    st.error(f"AI service is temporarily busy: {e}")


def render_career_roadmap(manager):
    st.header("🗺️ Career Roadmap")

    col1, col2 = st.columns(2)
    with col1:
        education = st.text_input("Education")
        skills = st.text_input("Current skills")
        experience = st.text_input("Experience level")
    with col2:
        interests = st.text_input("Interests")
        target_role = st.text_input("Target role")
        duration = st.selectbox("Duration", [30, 60, 90], index=2)

    if st.button("Generate Roadmap"):
        profile = {
            "education": education, "skills": skills, "experience": experience,
            "interests": interests, "target_role": target_role,
        }
        with st.spinner("Building your roadmap..."):
            try:
                roadmap = generate_roadmap(manager, profile, duration_days=duration)
                for phase in roadmap.get("phases", []):
                    with st.expander(f"{phase.get('phase_label')} — {phase.get('focus')}"):
                        st.markdown("**Skills to Learn**")
                        for s in phase.get("skills_to_learn", []):
                            st.write(f"- {s}")
                        st.markdown("**Projects to Build**")
                        for p in phase.get("projects_to_build", []):
                            st.write(f"- {p}")
                        st.markdown("**Resume Improvements**")
                        for r in phase.get("resume_improvements", []):
                            st.write(f"- {r}")
                        st.markdown("**Weekly Actions**")
                        for w in phase.get("weekly_actions", []):
                            st.write(f"- {w}")
            except Exception as e:
                st.error(f"AI service is temporarily busy: {e}")


def render_interview_prep(manager):
    st.header("🎤 Interview Preparation")
    resume_text = _get_resume_text()
    jd_text = st.text_area("Job description (optional)", height=150, key="interview_jd")

    col1, col2 = st.columns(2)
    with col1:
        difficulty = st.selectbox("Difficulty", ["beginner", "intermediate", "advanced"])
    with col2:
        count = st.slider("Number of questions", 3, 10, 5)

    if st.button("Generate Questions"):
        with st.spinner("Preparing questions..."):
            try:
                data = generate_interview_questions(
                    manager, resume_text, jd_text, difficulty=difficulty, count=count
                )
                st.session_state["interview_questions"] = data.get("questions", [])
            except Exception as e:
                st.error(f"AI service is temporarily busy: {e}")

    for i, q in enumerate(st.session_state.get("interview_questions", [])):
        st.markdown(f"**[{q['category']} | {q['difficulty']}]** {q['question']}")
        answer_key = f"interview_answer_{i}"
        answer = st.text_area("Your answer", key=answer_key, height=100)
        if st.button("Get Feedback", key=f"feedback_btn_{i}") and answer:
            with st.spinner("Scoring..."):
                try:
                    analysis = analyze_interview_answer(manager, q["question"], answer, resume_text)
                    st.metric("Score", f"{analysis.get('score')}/100")
                    st.markdown("**Strengths**")
                    for s in analysis.get("strengths", []):
                        st.write(f"- {s}")
                    st.markdown("**Improvements**")
                    for imp in analysis.get("improvements", []):
                        st.write(f"- {imp}")
                    with st.expander("See a stronger example answer"):
                        st.write(analysis.get("improved_answer_example", ""))
                except Exception as e:
                    st.error(f"AI service is temporarily busy: {e}")
        st.divider()
