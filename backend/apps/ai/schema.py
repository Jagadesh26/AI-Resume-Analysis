from dataclasses import dataclass, field


@dataclass
class OverallScore:

    score: int

    grade: str

    reason: str


@dataclass
class GrammarAnalysis:

    score: int

    issues: list[str] = field(default_factory=list)


@dataclass
class FormattingAnalysis:

    score: int

    issues: list[str] = field(default_factory=list)