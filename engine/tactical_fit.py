# engine/tactical_fit.py
from engine.profiles import CLUB_STYLE

CLUB_ALIASES = {
    "fc barcelona": "barcelona", "barca": "barcelona",
    "real madrid cf": "real madrid", "madrid": "real madrid",
    "man city": "manchester city", "manchester city fc": "manchester city",
    "arsenal fc": "arsenal", "the gunners": "arsenal",
    "liverpool fc": "liverpool", "lfc": "liverpool",
}

def _normalize_club(name: str) -> str:
    key = (name or "").lower().strip()
    return CLUB_ALIASES.get(key, key)

def compute_tactical_fit(buying_club: str, player_perf: dict) -> dict:
    club = _normalize_club(buying_club)
    if club not in CLUB_STYLE or not player_perf.get("found"):
        return {"computed": False, "fit_score": 50.0, "role": "Unknown",
                "strengths": [], "gaps": []}

    style = CLUB_STYLE[club]
    pcts = player_perf.get("percentiles", {})

    score_sum, strengths, gaps = 0, [], []
    for m in style["key_metrics"]:
        val = pcts.get(m)
        if val is None:
            val = 50  # missing metric -> neutral, and call it out as a gap
            gaps.append(f"{m} (no data)")
        elif val >= style["min_percentile"]:
            strengths.append(m)
        else:
            gaps.append(m)
        score_sum += val

    fit_score = round(score_sum / len(style["key_metrics"]), 1)
    return {"computed": True, "fit_score": fit_score,
            "role": style["required_role"], "strengths": strengths, "gaps": gaps}