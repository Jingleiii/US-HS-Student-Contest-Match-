from dataclasses import dataclass, field
from typing import List, Optional

@dataclass(frozen=True)
class Competition:
    name: str
    subject: str
    min_grade: int
    max_grade: int
    difficulty: int
    prestige: int
    roi: int
    format: str      # e.g. "online|individual/offline|team"
    season: str      # e.g. "Fall", "Winter", "Year-round"
    scope: str       # e.g. "regional|national|international"
    prep_time_weeks: int
    link: str = ""

@dataclass
class StudentProfile:
    grade: int
    academic_strength: int
    interests: List[str] = field(default_factory=list)
    weekly_hours: float = 4.0
    target_tier: str = "any"
    prefer_online: Optional[bool] = None
    prefer_team: Optional[bool] = None

@dataclass(frozen=True)
class Recommendation:
    competition: Competition
    score: float
    reasons: List[str]
    warnings: List[str]
