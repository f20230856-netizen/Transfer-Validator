# tools/scrapers.py
import os
import json
import hashlib

def _get_cache_path(func_name: str, player_name: str) -> str:
    # Force lowercase and stripped name so "Nico Williams" matches "nico williams"
    clean_name = player_name.lower().strip()
    key = f"{func_name}:{clean_name}"
    hashed = hashlib.md5(key.encode("utf-8")).hexdigest()
    return os.path.join("data", "cache", f"{hashed}.json")

def scrape_fbref(player_name: str) -> dict:
    path = _get_cache_path("scrape_fbref", player_name)
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {"found": False, "note": f"No cached FBref data for {player_name}"}

def scrape_transfermarkt(player_name: str) -> dict:
    path = _get_cache_path("scrape_transfermarkt", player_name)
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {"found": False, "note": f"No cached Transfermarkt data for {player_name}"}