from dataclasses import dataclass, field, asdict
from typing import List
import json


@dataclass
class PersonalInfo:
    full_name: str = ""
    headline: str = ""
    email: str = ""
    phone: str = ""
    location: str = ""
    linkedin: str = ""
    github: str = ""
    portfolio: str = ""


@dataclass
class WorkExperience:
    job_title: str = ""
    company: str = ""
    location: str = ""
    start_date: str = ""
    end_date: str = ""
    bullets: List[str] = field(default_factory=list)


@dataclass
class Education:
    degree: str = ""
    institution: str = ""
    location: str = ""
    start_date: str = ""
    end_date: str = ""
    details: str = ""


@dataclass
class Project:
    title: str = ""
    description: str = ""
    tech_stack: List[str] = field(default_factory=list)
    link: str = ""


@dataclass
class Certification:
    name: str = ""
    issuer: str = ""
    date: str = ""


@dataclass
class ResumeSection:
    """Generic container for custom/extra sections (Achievements, Languages, etc.)"""
    name: str
    items: List[str] = field(default_factory=list)


@dataclass
class Resume:
    personal_info: PersonalInfo = field(default_factory=PersonalInfo)
    professional_summary: str = ""
    career_objective: str = ""
    work_experience: List[WorkExperience] = field(default_factory=list)
    education: List[Education] = field(default_factory=list)
    technical_skills: List[str] = field(default_factory=list)
    soft_skills: List[str] = field(default_factory=list)
    projects: List[Project] = field(default_factory=list)
    certifications: List[Certification] = field(default_factory=list)
    custom_sections: List[ResumeSection] = field(default_factory=list)
    section_order: List[str] = field(default_factory=lambda: [
        "personal_info", "professional_summary", "work_experience",
        "education", "technical_skills", "soft_skills", "projects",
        "certifications",
    ])

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)

    @staticmethod
    def from_dict(data: dict) -> "Resume":
        r = Resume()
        r.personal_info = PersonalInfo(**data.get("personal_info", {}))
        r.professional_summary = data.get("professional_summary", "")
        r.career_objective = data.get("career_objective", "")
        r.work_experience = [WorkExperience(**w) for w in data.get("work_experience", [])]
        r.education = [Education(**e) for e in data.get("education", [])]
        r.technical_skills = data.get("technical_skills", [])
        r.soft_skills = data.get("soft_skills", [])
        r.projects = [Project(**p) for p in data.get("projects", [])]
        r.certifications = [Certification(**c) for c in data.get("certifications", [])]
        r.custom_sections = [ResumeSection(**s) for s in data.get("custom_sections", [])]
        r.section_order = data.get("section_order", r.section_order)
        return r

    def add_section(self, name: str):
        if name not in self.section_order:
            self.section_order.append(name)

    def remove_section(self, name: str):
        if name in self.section_order:
            self.section_order.remove(name)

    def reorder_sections(self, new_order: List[str]):
        self.section_order = new_order
