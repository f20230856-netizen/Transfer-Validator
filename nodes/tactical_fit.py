# nodes/tactical_fit.py
from engine.tactical_fit import compute_tactical_fit

def fit_node(state: dict) -> dict:
    perf = state.get("performance") or {}
    if not perf.get("found"):
        return {"fit": {"computed": False, "fit_score": 50.0, "role": "Unknown", "strengths": [], "gaps": []}}
    
    club = state["rumor"]["buying_club"]
    report = compute_tactical_fit(club, perf)
    return {"fit": report}