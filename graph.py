# graph.py
import json, os
from langgraph.graph import StateGraph, START, END
from state import GraphState
from nodes.parser import parser_node
from nodes.credibility import credibility_node
from nodes.tactical_fit import fit_node
from nodes.verdict import verdict_node

# --- load the cached player inputs once at import ---
with open(os.path.join("data", "cache", "players.json"), encoding="utf-8") as f:
    PLAYER_CACHE = json.load(f)

def _match_player(name: str):
    key = (name or "").lower().strip()
    if key in PLAYER_CACHE:
        return PLAYER_CACHE[key]
    # fallback: match on last name or substring
    for k, v in PLAYER_CACHE.items():
        if key and (key in k or k in key or key.split()[-1] == k.split()[-1]):
            return v
    return None

def data_ingestion_node(state: GraphState) -> dict:
    """Reads REAL cached stats for the parsed player and computes the fee premium."""
    player_name = state["rumor"].get("player_name", "")
    fee = state["rumor"].get("reported_fee_eur") or 0
    rec = _match_player(player_name)

    if not rec:
        # graceful degradation — no crash, just flag missing data
        return {
            "performance": {"found": False, "role": "Unknown", "percentiles": {},
                            "note": f"No cached data for '{player_name}'"},
            "value": {"found": False, "market_value_eur": None,
                      "reported_fee_eur": fee, "premium_pct": None},
            "errors": [f"No cached data for {player_name}"],
        }

    mv = rec["market_value_eur"]
    prem = round((fee - mv) / mv * 100, 1) if (mv and fee) else None
    return {
        "performance": {"found": True, "role": rec["role"],
                        "percentiles": rec["percentiles"], "note": ""},
        "value": {"found": True, "market_value_eur": mv,
                  "reported_fee_eur": fee, "premium_pct": prem},
        "errors": [],
    }

def credibility_router(state: GraphState):
    """Short-circuit only a junk rumor: lowest tier AND zero corroboration."""
    cred = state.get("credibility") or {}
    if cred.get("tier", 5) == 5 and cred.get("corroboration_count", 0) == 0:
        return "early_exit"
    return "continue"

# --- build the graph ---
workflow = StateGraph(GraphState)
workflow.add_node("parse_rumor", parser_node)
workflow.add_node("evaluate_credibility", credibility_node)
workflow.add_node("fetch_market_data", data_ingestion_node)
workflow.add_node("calculate_tactical_fit", fit_node)
workflow.add_node("generate_verdict", verdict_node)

workflow.add_edge(START, "parse_rumor")
workflow.add_edge("parse_rumor", "evaluate_credibility")
workflow.add_conditional_edges(
    "evaluate_credibility",
    credibility_router,
    {"early_exit": "generate_verdict", "continue": "fetch_market_data"},
)
workflow.add_edge("fetch_market_data", "calculate_tactical_fit")
workflow.add_edge("calculate_tactical_fit", "generate_verdict")
workflow.add_edge("generate_verdict", END)

app = workflow.compile()