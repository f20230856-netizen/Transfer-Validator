# build_cache.py
from dotenv import load_dotenv
load_dotenv()
from tools.scrapers import scrape_fbref, scrape_transfermarkt

DEMO_PLAYERS = [
    "Nico Williams", "Anthony Gordon", "Lamine Yamal", "Bukayo Saka",
    "Florian Wirtz", "Rodri", "Vinicius Junior", "Pedri",
    "Alexander Isak", "Martin Odegaard",
]

print("Starting pre-cache loop for portfolio demo players...")
for p in DEMO_PLAYERS:
    print(f"Caching data for: {p} ...")
    try:
        fb_res = scrape_fbref(p)
        print(f"  FBref stats found: {fb_res.get('found')}")
    except Exception as e:
        print(f"  FBref error on {p}: {e}")
        
    try:
        tm_res = scrape_transfermarkt(p)
        print(f"  Transfermarkt value found: {tm_res.get('found')}")
    except Exception as e:
        print(f"  Transfermarkt error on {p}: {e}")
print("Pre-caching loop complete!")