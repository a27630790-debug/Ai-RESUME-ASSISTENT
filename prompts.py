RESUME_ANALYSIS_PROMPT = """You are a professional resume reviewer.
Analyze the resume text below and identify:
1. Grammar/spelling issues
2. Weak or vague wording
3. Repetition
4. Missing common resume sections
5. Weak bullet points (not results-oriented)
6. ATS formatting issues
7. Keyword issues

IMPORTANT: Do NOT invent any experience, skill, employer, or achievement not
present in the text. Only critique presentation, never fabricate content.

Resume text:
---
{resume_text}
---

Respond with these headings: Grammar & Spelling, Weak Wording, Missing Sections,
Weak Bullet Points, ATS Issues, Overall Recommendations.
"""

RESUME_REWRITE_BULLET_PROMPT = """Rewrite this resume bullet to be more
professional and results-oriented, starting with a strong action verb.
Do NOT invent numbers/metrics/achievements not implied by the original.

Original bullet: "{bullet_text}"

Return ONLY the rewritten bullet, nothing else.
"""

ATS_ANALYSIS_PROMPT = """You are an ATS compatibility checker. This is an
ESTIMATE only, not a real company's ATS score.

Resume text:
---
{resume_text}
---

Provide: 1) Estimated ATS Compatibility Score (0-100, label it "Estimated ATS
Guidance") 2) Keyword Optimization notes 3) Formatting issues 4) Missing
sections 5) 3-5 concrete recommendations. Never claim this matches a real
company's actual ATS score.
"""

JOB_MATCH_PROMPT = """Compare this resume against the job description.
Do NOT invent skills or experience the candidate does not have.

RESUME:
---
{resume_text}
---

JOB DESCRIPTION:
---
{job_description}
---

Provide: Overall Match % (estimate), Matching Skills, Missing Skills,
Matching Keywords, Missing Keywords, Strengths, Weaknesses, and
presentation-only recommendations to improve the match.
"""

# ============================================================
# Phase 3 — structured (JSON) prompts, used for UI-renderable
# scores/tables instead of free-text paragraphs.
# ============================================================

ATS_ANALYSIS_JSON_PROMPT = """You are an ATS compatibility checker. The score
you give is an ESTIMATE only, never a real company's actual ATS score.

Resume text:
---
{resume_text}
---

Return ONLY valid JSON (no markdown, no extra commentary) with EXACTLY this
schema:
{{
  "ats_score": <integer 0-100>,
  "score_label": "Estimated ATS Guidance",
  "keyword_optimization": "<short paragraph>",
  "formatting_issues": ["...", "..."],
  "missing_sections": ["...", "..."],
  "recommendations": ["...", "...", "..."]
}}
"""

JD_ANALYSIS_JSON_PROMPT = """Extract structured information from this job
description. Only extract what is explicitly stated or clearly implied.

Job description:
---
{jd_text}
---

Return ONLY valid JSON (no markdown, no extra commentary) with EXACTLY this
schema:
{{
  "job_title": "...",
  "required_skills": ["..."],
  "preferred_skills": ["..."],
  "experience_required": "...",
  "education_required": "...",
  "responsibilities": ["..."],
  "keywords": ["..."],
  "soft_skills": ["..."]
}}
"""

JOB_MATCH_JSON_PROMPT = """Compare the resume against the job description.
Do NOT invent or credit the candidate with any skill or experience that is
not present in the resume text.

RESUME:
---
{resume_text}
---

JOB DESCRIPTION:
---
{jd_text}
---

Return ONLY valid JSON (no markdown, no extra commentary) with EXACTLY this
schema:
{{
  "match_percentage": <integer 0-100>,
  "matching_skills": ["..."],
  "missing_skills": ["..."],
  "matching_keywords": ["..."],
  "missing_keywords": ["..."],
  "experience_gap": "...",
  "education_match": "...",
  "strengths": ["..."],
  "weaknesses": ["..."],
  "recommendations": ["..."]
}}
"""

# ============================================================
# Phase 4 — Resume Tailoring + Cover Letter Generator
# ============================================================

RESUME_TAILORING_JSON_PROMPT = """You are tailoring a resume for a specific
job. You must ONLY reorganize, rephrase, and prioritize information that is
ALREADY present in the resume text below. NEVER invent new skills, employers,
projects, numbers, or achievements that are not implied by the original text.

RESUME:
---
{resume_text}
---

JOB DESCRIPTION:
---
{jd_text}
---

Return ONLY valid JSON (no markdown, no extra commentary) with EXACTLY this
schema:
{{
  "tailored_summary": "<rewritten professional summary aligned to this job, based only on real resume content>",
  "prioritized_skills": ["<candidate's own skills, reordered so most job-relevant come first>"],
  "rewritten_bullets": [
    {{"original": "<original bullet text>", "tailored": "<same bullet, rewritten to highlight job-relevant angle>"}}
  ],
  "keywords_to_naturally_add": ["<keywords from the JD the candidate could genuinely use if truthful>"],
  "sections_to_deprioritize": ["<resume sections/items less relevant to this job, if any>"]
}}
"""

COVER_LETTER_PROMPT = """Write a professional cover letter based ONLY on the
real information in the resume below. Do NOT invent experience, skills, or
achievements not present in the resume.

RESUME:
---
{resume_text}
---

JOB DESCRIPTION:
---
{jd_text}
---

Company: {company}
Role: {role}
Tone: {tone}
Length: {length}

Write the complete cover letter now (no JSON, plain text, ready to send —
include a greeting and sign-off using the candidate's name from the resume).
"""

# ============================================================
# Phase 5 — AI Career Chat Assistant + Career Roadmap
# ============================================================

CAREER_CHAT_SYSTEM_PROMPT = """You are CareerPilot AI, a friendly and honest
career assistant. You help with resume guidance, career direction, skill-gap
analysis, learning advice, interview preparation, and job application advice.

Rules:
- NEVER invent or assume facts about the user's experience, skills, or
  background beyond what they tell you in this conversation.
- If you don't have enough information to answer well, ask a clarifying
  question instead of guessing.
- Keep answers practical and actionable, not generic filler.
- If the user writes in Roman Urdu or a mix of Urdu/English, you may reply
  in the same natural mixed style if that suits them better.
"""

CAREER_ROADMAP_JSON_PROMPT = """Create a personalized career roadmap for this
person based ONLY on the profile information given. Do not invent skills,
experience, or education they haven't mentioned.

PROFILE:
- Education: {education}
- Current skills: {skills}
- Experience level: {experience}
- Interests: {interests}
- Target role: {target_role}
- Roadmap duration: {duration_days} days

Return ONLY valid JSON (no markdown, no extra commentary) with EXACTLY this
schema:
{{
  "duration_days": {duration_days},
  "target_role": "...",
  "phases": [
    {{
      "phase_label": "e.g. Days 1-30",
      "focus": "short theme for this phase",
      "skills_to_learn": ["..."],
      "projects_to_build": ["..."],
      "certifications_or_courses": ["..."],
      "resume_improvements": ["..."],
      "job_application_goals": ["..."],
      "interview_prep": ["..."],
      "weekly_actions": ["..."]
    }}
  ]
}}
"""

# ============================================================
# Phase 6 — Interview Preparation
# ============================================================

INTERVIEW_QUESTIONS_JSON_PROMPT = """Generate interview preparation questions
for this candidate. Base resume-related questions ONLY on real resume
content — never assume experience not present in it.

RESUME:
---
{resume_text}
---

JOB DESCRIPTION (may be empty if general prep):
---
{jd_text}
---

Difficulty level: {difficulty}
Question categories to include: {question_types}
Number of questions: {count}

Return ONLY valid JSON (no markdown, no extra commentary) with EXACTLY this
schema:
{{
  "questions": [
    {{
      "category": "technical | behavioral | hr | resume-based | job-specific",
      "difficulty": "beginner | intermediate | advanced",
      "question": "...",
      "sample_answer_approach": "<brief guidance on how to structure a strong answer, not a full scripted answer>"
    }}
  ]
}}
"""

INTERVIEW_ANSWER_ANALYSIS_JSON_PROMPT = """Analyze this candidate's interview
answer honestly and constructively.

QUESTION: {question}

CANDIDATE'S ANSWER: {user_answer}

RESUME CONTEXT (may be empty):
---
{resume_text}
---

Return ONLY valid JSON (no markdown, no extra commentary) with EXACTLY this
schema:
{{
  "score": <integer 0-100>,
  "strengths": ["..."],
  "improvements": ["..."],
  "improved_answer_example": "<a stronger version of the answer, based only on what the candidate actually said/has, not invented facts>"
}}
"""

# ============================================================
# Phase 7 — Job Application Tracker Analytics
# ============================================================

ANALYTICS_INSIGHT_PROMPT = """Based ONLY on the following real application
statistics, write 2-4 short, honest, encouraging insights for the user.
Do NOT invent any numbers or facts beyond what's given below. If a stat is
zero or missing, do not pretend otherwise.

STATS:
{stats_json}

Return plain text only (no JSON), 2-4 short sentences.
"""
