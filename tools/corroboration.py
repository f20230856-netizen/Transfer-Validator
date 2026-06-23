# tools/corroboration.py
import os
from urllib.parse import urlparse
from tavily import TavilyClient

def search_corroboration(claim: dict) -> list[dict]:
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    q = f"{claim['player_name']} {claim['buying_club']} transfer"
    try:
        res = client.search(query=q, max_results=10, topic="news")
    except Exception:
        return []   # Degrade gracefully: return empty list if search fails
    seen, out = set(), []
    for r in res.get("results", []):
        d = urlparse(r["url"]).netloc.replace("www.", "")
        if d in seen:
            continue
        seen.add(d)
        out.append({"domain": d, "url": r["url"], "title": r.get("title", "")})
    return out