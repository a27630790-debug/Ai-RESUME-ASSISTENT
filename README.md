# CareerPilot AI 🧭

Your AI-Powered Career Companion — an AI career platform for resume building,
ATS analysis, job matching, resume tailoring, cover letters, career chat,
roadmaps, interview prep, and application tracking.

## Tech Stack
- Python + Streamlit
- Gemini API + Groq API (with automatic fallback)
- SQLite (local/dev)
- python-docx, ReportLab, pypdf

## Local Setup

```bash
pip install -r requirements.txt
```

Create `.streamlit/secrets.toml` (never commit this file):
```toml
GEMINI_API_KEY = "your-gemini-key"
GROQ_API_KEY = "your-groq-key"
```

Run:
```bash
streamlit run app.py
```

## Deploying to Streamlit Community Cloud

1. Push this repo to GitHub.
2. Go to https://share.streamlit.io and connect your GitHub account.
3. Create a new app, pick this repo, branch `main`, and set the main file to `app.py`.
4. In the app's **Settings → Secrets**, paste:
   ```toml
   GEMINI_API_KEY = "your-gemini-key"
   GROQ_API_KEY = "your-groq-key"
   ```
5. Deploy.

## Project Structure

- `ai/` — AI provider manager (Gemini + Groq with fallback), prompts
- `resume/` — resume model, builder, parser, analyzer, ATS, tailoring
- `jobs/` — job description analyzer, resume-job matcher, application tracker
- `coverletter/` — cover letter generator
- `career/` — chat assistant, roadmap generator, interview prep, analytics
- `auth/` — email/password authentication + guest mode
- `database/` — SQLite schema and connection handling
- `exports/` — TXT, JSON, DOCX, PDF export
- `utils/` — JSON parsing helpers, self-repairing structured AI output
- `ui/` — Streamlit page renderers for each feature
- `app.py` — main Streamlit entry point

## Notes

- ATS scores are **estimates only**, never a real company's actual ATS score.
- The AI never invents experience, skills, or achievements — it only works
  with what the user provides.
- Google Login (OAuth) is not yet implemented — email/password and guest
  mode are available now.
