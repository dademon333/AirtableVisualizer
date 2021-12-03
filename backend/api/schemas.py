from pydantic import BaseModel, Field


class Course(BaseModel):
    id: str
    name: str


class Theme(BaseModel):
    id: str
    name: str
    top_level_themes: list[str] = Field(alias='topLevelThemes')
    courses: list[str]


class Quantum(BaseModel):
    id: str
    name: str
    description: str


class Knowledge(BaseModel):
    id: str
    name: str
    quantums: list[str]
    themes: list[str]


class Target(BaseModel):
    id: str
    name: str
    knowledges: list[str]
    metrics: list[str]


class Metric(BaseModel):
    id: str
    name: str
    description: str


class Task(BaseModel):
    id: str
    name: str
    description: str
    targets: list[str]


class Activity(BaseModel):
    id: str
    name: str
    top_level_activities: list[str] = Field(alias='topLevelActivities')
    targets: list[str]


class Skill(BaseModel):
    id: str
    name: str
    activities: list[str]


class Competence(BaseModel):
    id: str
    name: str
    top_level_competences: list[str] = Field(alias='topLevelCompetences')
    skills: list[str]
    knowledges: list[str]


class Profession(BaseModel):
    id: str
    name: str
    competences: list[str]


class SuosCompetence(BaseModel):
    id: str
    name: str
    competences: list[str]


class AllCourses(BaseModel):
    courses: list[Course]
    themes: list[Theme]
    knowledges: list[Knowledge]
    quantums: list[Quantum]
    competences: list[Competence]


class EntireCourse(BaseModel):
    id: str
    name: str
    themes: list[Theme]
    knowledges: list[Knowledge]
    quantums: list[Quantum]
    targets: list[Target]
    metrics: list[Metric]
    tasks: list[Task]
    activities: list[Activity]
    skills: list[Skill]
    competences: list[Competence]
    professions: list[Profession]
    suos_competences: list[SuosCompetence] = Field(alias='suosCompetences')
