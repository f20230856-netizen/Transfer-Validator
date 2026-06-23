# nodes/credibility.py
from engine.credibility_algo import score_credibility
from tools.corroboration import search_corroboration

def credibility_node(state: dict) -> dict:
    claim = state["rumor"]
    # Pull live web corroboration domains using our Tavily tool
    sources = search_corroboration(claim)
    report = score_credibility(claim, sources)
    return {"credibility": report}