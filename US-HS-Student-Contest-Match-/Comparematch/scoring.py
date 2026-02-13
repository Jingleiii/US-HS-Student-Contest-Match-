from typing import List, Optional, Tuple
from .model import Competition, StudentProfile, Recommendation

def _norm(s: str) -> str:
    return s.strip().lower().replace("&", "and")

def _fmt_tokens(fmt: str) -> set[str]:
    return {_norm(x) for x in fmt.split("|") if x.strip()}

def score_one(profile: StudentProfile, comp: Competition) -> Optional[Tuple[float, List[str], List[str]]]:
    # 过滤年级不符合直接不推荐
    if not (comp.min_grade <= profile.grade <= comp.max_grade):
        return None

    score = 0.0
    reasons: List[str] = []
    warnings: List[str] = []

    # 1) 兴趣匹配
    interests = {_norm(x) for x in profile.interests}
    subject = _norm(comp.subject)
    if subject in interests:
        score += 30
        reasons.append(f"兴趣匹配：{comp.subject} (+30)")
    elif "stem" in interests and subject in {"math", "cs", "physics", "chemistry", "biology", "stem"}:
        score += 20
        reasons.append(f"兴趣大类匹配：STEM → {comp.subject} (+20)")
    else:
        score += 5
        reasons.append("兴趣不完全匹配：可作为补充尝试 (+5)")

    # 2) 难度匹配
    gap = abs(profile.academic_strength - comp.difficulty)
    diff_score = max(0, 25 - gap * 7)
    score += diff_score
    if gap <= 1:
        reasons.append(f"难度较匹配：强度{profile.academic_strength}/5 vs 难度{comp.difficulty}/5 (+{diff_score:.0f})")
    else:
        warnings.append(f"难度可能不匹配：强度{profile.academic_strength}/5 vs 难度{comp.difficulty}/5 (+{diff_score:.0f})")

    # 3) ROI
    roi_score = comp.roi * 6
    score += roi_score
    reasons.append(f"ROI：{comp.roi}/5 (+{roi_score})")

    # 4) Prestige
    tier = _norm(profile.target_tier)
    prestige_w = 8 if tier == "top" else 5 if tier == "mid" else 4
    pres_score = comp.prestige * prestige_w
    score += pres_score
    reasons.append(f"Prestige：{comp.prestige}/5 (权重{prestige_w}) (+{pres_score})")

    # 5) 时间投入
    if profile.weekly_hours < 3 and comp.prep_time_weeks >= 10:
        score -= 12
        warnings.append(f"时间压力：每周{profile.weekly_hours}h，但建议准备{comp.prep_time_weeks}周 (-12)")
    elif profile.weekly_hours >= 6 and comp.prep_time_weeks >= 10:
        score += 6
        reasons.append(f"投入充足：每周{profile.weekly_hours}h 支撑长期准备 (+6)")

    # 6) 形式偏好
    fmt = _fmt_tokens(comp.format)
    if profile.prefer_online is True:
        if "online" in fmt:
            score += 6
            reasons.append("形式偏好：在线 (+6)")
        else:
            score -= 4
            warnings.append("形式偏好：你偏在线，但该比赛偏线下 (-4)")
    if profile.prefer_team is True:
        if "team" in fmt:
            score += 4
            reasons.append("形式偏好：团队 (+4)")
        else:
            score -= 2
            warnings.append("形式偏好：你偏团队，但该比赛偏个人 (-2)")

    return score, reasons, warnings

def recommend(profile: StudentProfile, competitions: List[Competition], topk: int = 10) -> List[Recommendation]:
    recs: List[Recommendation] = []
    for comp in competitions:
        scored = score_one(profile, comp)
        if scored is None:
            continue
        s, reasons, warnings = scored
        recs.append(Recommendation(comp, s, reasons, warnings))

    recs.sort(key=lambda r: r.score, reverse=True)
    return recs[:topk]
