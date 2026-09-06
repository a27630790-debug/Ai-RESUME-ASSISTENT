from resume.models import Resume


def export_json(resume: Resume) -> str:
    return resume.to_json()
