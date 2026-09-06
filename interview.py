from ai.prompts import INTERVIEW_QUESTIONS_JSON_PROMPT, INTERVIEW_ANSWER_ANALYSIS_JSON_PROMPT
from utils.ai_json import generate_structured_json

SYSTEM_PROMPT = (
    "You are CareerPilot AI's interview preparation engine. Resume-based "
    "questions must only reference what is actually in the candidate's "
    "resume — never invent experience. Feedback on answers must be honest, "
    "specific, and constructive, never just generic praise."
)


def generate_interview_questions(
    manager,
    resume_text: str,
    jd_text: str = "",
    difficulty: str = "intermediate",
    question_types: list = None,
    count: int = 8,
) -> dict:
    """
    difficulty: "beginner" | "intermediate" | "advanced"
    question_types: subset of ["technical", "behavioral", "hr", "resume-based", "job-specific"]
    Returns: {"questions": [{"category", "difficulty", "question", "sample_answer_approach"}]}
    """
    question_types = question_types or ["technical", "behavioral", "hr"]
    prompt = INTERVIEW_QUESTIONS_JSON_PROMPT.format(
        resume_text=resume_text,
        jd_text=jd_text or "(none provided — general preparation)",
        difficulty=difficulty,
        question_types=", ".join(question_types),
        count=count,
    )
    return generate_structured_json(manager, prompt, system_prompt=SYSTEM_PROMPT, max_tokens=1800)


def analyze_interview_answer(
    manager,
    question: str,
    user_answer: str,
    resume_text: str = "",
) -> dict:
    """
    Returns: {"score": int, "strengths": [...], "improvements": [...],
              "improved_answer_example": str}
    """
    prompt = INTERVIEW_ANSWER_ANALYSIS_JSON_PROMPT.format(
        question=question,
        user_answer=user_answer,
        resume_text=resume_text or "(none provided)",
    )
    return generate_structured_json(manager, prompt, system_prompt=SYSTEM_PROMPT, max_tokens=900)


def run_mock_interview_session(manager, resume_text: str, jd_text: str = "", num_questions: int = 3):
    """
    Simple CLI-style mock interview loop for quick testing (e.g. in Colab).
    Generates questions, asks them one by one via input(), scores each answer,
    then prints a final summary. The future Streamlit UI will replace input()
    with proper form widgets but reuse the same generate/analyze functions.
    """
    questions_data = generate_interview_questions(
        manager, resume_text, jd_text, count=num_questions
    )
    results = []
    for q in questions_data.get("questions", [])[:num_questions]:
        print(f"\n[{q['category']} | {q['difficulty']}] {q['question']}")
        answer = input("Your answer: ")
        analysis = analyze_interview_answer(manager, q["question"], answer, resume_text)
        print(f"Score: {analysis.get('score')}/100")
        for imp in analysis.get("improvements", []):
            print(f"  - Improve: {imp}")
        results.append({"question": q["question"], "answer": answer, "analysis": analysis})

    if results:
        avg_score = sum(r["analysis"].get("score", 0) for r in results) / len(results)
        print(f"\n=== Mock Interview Complete — Average Score: {avg_score:.0f}/100 ===")
    return results
