from dataclasses import dataclass, field


@dataclass(slots=True)
class JobSchema:

    job_title: str

    company: str

    location: str

    experience: str

    employment_type: str

    work_mode: str

    salary: str

    description: str

    skills: list[str] = field(default_factory=list)

    posted_date: str = ""

    apply_url: str = ""

    source: str = ""

    match_score: float = 0.0

    match_reason: str = ""