# tools/cache.py
import json
import os
import hashlib

CACHE_DIR = "data/cache"

def cached(fn):
    def wrapper(name, *a, **k):
        os.makedirs(CACHE_DIR, exist_ok=True)
        key = hashlib.md5(f"{fn.__name__}:{name.lower()}".encode()).hexdigest()
        path = os.path.join(CACHE_DIR, f"{key}.json")
        if os.path.exists(path):
            with open(path) as f:
                return json.load(f)
        out = fn(name, *a, **k)
        with open(path, "w") as f:
            json.dump(out, f)
        return out
    return wrapper