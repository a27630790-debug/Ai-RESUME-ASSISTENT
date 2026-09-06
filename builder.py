from resume.models import Resume, PersonalInfo, WorkExperience, Education, Project, Certification


def build_resume_from_answers(answers: dict) -> Resume:
    resume = Resume()
    resume.personal_info = PersonalInfo(
        full_name=answers.get("full_name", ""),
        headline=answers.get("headline", ""),
        email=answers.get("email", ""),
        phone=answers.get("phone", ""),
        location=answers.get("location", ""),
        linkedin=answers.get("linkedin", ""),
        github=answers.get("github", ""),
        portfolio=answers.get("portfolio", ""),
    )
    resume.professional_summary = answers.get("professional_summary", "")
    resume.career_objective = answers.get("career_objective", "")
    resume.technical_skills = answers.get("technical_skills", [])
    resume.soft_skills = answers.get("soft_skills", [])

    for exp in answers.get("work_experience", []):
        resume.work_experience.append(WorkExperience(**exp))
    for edu in answers.get("education", []):
        resume.education.append(Education(**edu))
    for proj in answers.get("projects", []):
        resume.projects.append(Project(**proj))
    for cert in answers.get("certifications", []):
        resume.certifications.append(Certification(**cert))

    return resume


def add_work_experience(resume: Resume, **kwargs) -> Resume:
    resume.work_experience.append(WorkExperience(**kwargs))
    return resume


def add_project(resume: Resume, **kwargs) -> Resume:
    resume.projects.append(Project(**kwargs))
    return resume
