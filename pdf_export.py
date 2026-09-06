from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from resume.models import Resume


def export_pdf(resume: Resume, output_path: str = "resume.pdf") -> str:
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    pi = resume.personal_info

    story.append(Paragraph(pi.full_name or "Your Name", styles["Title"]))
    if pi.headline:
        story.append(Paragraph(pi.headline, styles["Normal"]))
    contact = " | ".join(filter(None, [pi.email, pi.phone, pi.location, pi.linkedin, pi.github, pi.portfolio]))
    if contact:
        story.append(Paragraph(contact, styles["Normal"]))
    story.append(Spacer(1, 12))

    if resume.professional_summary:
        story.append(Paragraph("Professional Summary", styles["Heading2"]))
        story.append(Paragraph(resume.professional_summary, styles["Normal"]))
        story.append(Spacer(1, 8))

    if resume.work_experience:
        story.append(Paragraph("Work Experience", styles["Heading2"]))
        for exp in resume.work_experience:
            story.append(Paragraph(f"<b>{exp.job_title}</b> — {exp.company} ({exp.start_date} - {exp.end_date})", styles["Normal"]))
            for b in exp.bullets:
                story.append(Paragraph(f"• {b}", styles["Normal"]))
        story.append(Spacer(1, 8))

    if resume.education:
        story.append(Paragraph("Education", styles["Heading2"]))
        for edu in resume.education:
            story.append(Paragraph(f"{edu.degree} — {edu.institution} ({edu.start_date} - {edu.end_date})", styles["Normal"]))
        story.append(Spacer(1, 8))

    if resume.technical_skills:
        story.append(Paragraph("Technical Skills", styles["Heading2"]))
        story.append(Paragraph(", ".join(resume.technical_skills), styles["Normal"]))
        story.append(Spacer(1, 8))

    if resume.projects:
        story.append(Paragraph("Projects", styles["Heading2"]))
        for p in resume.projects:
            story.append(Paragraph(f"<b>{p.title}</b>: {p.description}", styles["Normal"]))
        story.append(Spacer(1, 8))

    if resume.certifications:
        story.append(Paragraph("Certifications", styles["Heading2"]))
        for c in resume.certifications:
            story.append(Paragraph(f"{c.name} — {c.issuer} ({c.date})", styles["Normal"]))

    doc.build(story)
    return output_path
