import csv
import json
from typing import List
from .model import Competition, StudentProfile

def load_competitions_from_csv(path: str) -> List[Competition]:
    comps: List[Competition] = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for line_no, row in enumerate(reader, start=2):
            try:
                comp = Competition(
                    name=row["name"].strip(),
                    subject=row["subject"].strip(),
                    min_grade=int(row["min_grade"]),
                    max_grade=int(row["max_grade"]),
                    difficulty=int(row["difficulty"]),
                    prestige=int(row["prestige"]),
                    roi=int(row["roi"]),
                    format=row.get("format", "").strip(),
                    season=row.get("season", "").strip(),
                    scope=row.get("scope", "").strip(),
                    prep_time_weeks=int(row.get("prep_time_weeks", "0") or 0),
                    link=row.get("link", "").strip(),
                )
                comps.append(comp)
            except Exception as e:
                raise ValueError(f"CSV 第{line_no}行解析失败：{e}\nrow={row}") from e
    return comps

def load_profile_from_json(path: str) -> StudentProfile:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return StudentProfile(
        grade=int(data["grade"]),
        academic_strength=int(data.get("academic_strength", 3)),
        interests=list(data.get("interests", [])),
        weekly_hours=float(data.get("weekly_hours", 4)),
        target_tier=str(data.get("target_tier", "any")),
        prefer_online=data.get("prefer_online", None),
        prefer_team=data.get("prefer_team", None),
    )
