from resume.models import Resume


def export_txt(resume: Resume) -> str:
    lines = []
    pi = resume.personal_info
    lines.append(pi.full_name)
    if pi.headline:
        lines.append(pi.headline)
    contact = " | ".join(filter(None, [pi.email, pi.phone, pi.location, pi.linkedin, pi.github, pi.portfolio]))
    if contact:
        lines.append(contact)
    lines.append("")

    if resume.professional_summary:
        lines += ["PROFESSIONAL SUMMARY", resume.professional_summary, ""]

    if resume.work_experience:
        lines.append("WORK EXPERIENCE")
        for exp in resume.work_experience:
            lines.append(f"{exp.job_title} — {exp.company} ({exp.start_date} - {exp.end_date})")
            lines += [f"  • {b}" for b in exp.bullets]
        lines.append("")

    if resume.education:
        lines.append("EDUCATION")
        for edu in resume.education:
            lines.append(f"{edu.degree} — {edu.institution} ({edu.start_date} - {edu.end_date})")
        lines.append("")

    if resume.technical_skills:
        lines += ["TECHNICAL SKILLS", ", ".join(resume.technical_skills), ""]

    if resume.projects:
        lines.append("PROJECTS")
        lines += [f"{p.title}: {p.description}" for p in resume.projects]
        lines.append("")

    if resume.certifications:
        lines.append("CERTIFICATIONS")
        lines += [f"{c.name} — {c.issuer} ({c.date})" for c in resume.certifications]

    return "\n".join(lines)
