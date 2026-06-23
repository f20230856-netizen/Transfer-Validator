# engine/credibility_algo.py

def score_credibility(claim: dict, web_sources: list) -> dict:
    """Deterministic algorithm to evaluate rumor reliability."""
    # `or ""` guards against the field being present but None (parser returns
    # None when no source is named in the rumor).
    source = (claim.get("reported_source") or "").lower()
    web_sources = web_sources or []

    # Establish baseline tier from the named source
    if any(k in source for k in ["ornstein", "romano", "athletic"]):
        base_tier, confidence = 1, 90.0
    elif any(k in source for k in ["sky", "bbc", "telegraph"]):
        base_tier, confidence = 2, 75.0
    elif any(k in source for k in ["bild", "marca", "sport"]):
        base_tier, confidence = 3, 55.0
    else:
        base_tier, confidence = 5, 25.0

    # Boost confidence based on how many independent web reports corroborate it
    corroboration_count = len(web_sources)
    boost = min(corroboration_count * 5, 15)  # cap boost at 15%
    confidence = min(confidence + boost, 99.0)

    # If no source was named but multiple outlets corroborate, don't leave it
    # stranded at the junk tier — lift it so it isn't auto-short-circuited.
    if base_tier == 5 and corroboration_count >= 2:
        base_tier = 4

    # World Cup window hype flag (general Summer 2026 window heuristic)
    hype_risk = True

    return {
        "tier": base_tier,
        "confidence": confidence,
        "best_source_tier": base_tier,
        "corroboration_count": corroboration_count,
        "sources": web_sources,
        "hype_risk": hype_risk,
        "rationale": (f"Base Tier {base_tier} source with {corroboration_count} "
                      f"cross-verified web reports."),
    }