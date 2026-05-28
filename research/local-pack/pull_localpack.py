"""
AccuRite Excavation — DataForSEO local-pack puller.

Reconstructed 2026-05-28 from the 2026-05-22 baseline session (original
/tmp scripts were cleared). Pulls Google Maps 3-pack rankings for the
AccuRite-target queries from three Wasatch Front geo points.

Run: DATAFORSEO_AUTH=... python pull_localpack.py
Output: prints a table and writes JSON to results-YYYY-MM-DD.json next to this file.
"""
from __future__ import annotations
import json
import os
import sys
import time
from datetime import date
from pathlib import Path

import requests

API = "https://api.dataforseo.com/v3/serp/google/organic/live/advanced"

# Geo points from the 2026-05-22 baseline. radius in km.
GEO_POINTS = [
    {"label": "Ogden",         "coord": "41.2230,-111.9738,10"},
    {"label": "Pleasant View", "coord": "41.3208,-111.9930,10"},
    {"label": "Layton",        "coord": "41.0602,-111.9711,10"},
]

QUERIES = [
    "excavation companies near me",
    "land clearing ogden",
    "grading contractor near me",
]

TARGET_DOMAIN = "accuriteexcavation.com"


def pull_one(auth: str, query: str, coord: str) -> dict:
    payload = [{
        "keyword": query,
        "location_coordinate": coord,
        "language_name": "English",
        "depth": 20,
    }]
    headers = {"Authorization": f"Basic {auth}", "Content-Type": "application/json"}
    resp = requests.post(API, json=payload, headers=headers, timeout=60)
    resp.raise_for_status()
    return resp.json()


def find_local_pack(data: dict) -> list[dict]:
    """Return the local_pack items array, or []."""
    tasks = data.get("tasks") or []
    if not tasks:
        return []
    result = (tasks[0].get("result") or [])
    if not result:
        return []
    items = result[0].get("items") or []
    # DataForSEO returns each local-pack member as its own top-level item
    # with type == "local_pack". Collect them all.
    return [it for it in items if it.get("type") == "local_pack"]


def find_accurite_rank(local_pack: list[dict]) -> tuple[int | None, str | None]:
    """Return (1-based rank within local pack, title) or (None, None)."""
    for idx, it in enumerate(local_pack, start=1):
        url = (it.get("url") or "") + " " + (it.get("domain") or "")
        title = it.get("title") or ""
        if "accurite" in url.lower() or "accurite" in title.lower():
            return idx, title
    return None, None


def main() -> int:
    auth = os.environ.get("DATAFORSEO_AUTH", "")
    if not auth:
        print("ERROR: DATAFORSEO_AUTH not set", file=sys.stderr)
        return 1

    today = date.today().isoformat()
    results = {"date": today, "queries": []}
    rows = []

    for q in QUERIES:
        for geo in GEO_POINTS:
            print(f"... {q!r} @ {geo['label']}", file=sys.stderr)
            try:
                raw = pull_one(auth, q, geo["coord"])
                pack = find_local_pack(raw)
                rank, title = find_accurite_rank(pack)
                pack_size = len(pack)
                rows.append({
                    "query": q,
                    "geo": geo["label"],
                    "accurite_rank": rank,
                    "pack_size": pack_size,
                    "top3": [(it.get("title") or "")[:40] for it in pack[:3]],
                })
            except Exception as e:
                rows.append({"query": q, "geo": geo["label"], "error": str(e)})
            time.sleep(0.5)

    results["rows"] = rows

    # Print table
    print(f"\nAccuRite local-pack snapshot — {today}")
    print(f"{'query':<32} {'geo':<14} {'rank':>5} {'pack':>5}  top3")
    print("-" * 100)
    for r in rows:
        if "error" in r:
            print(f"{r['query']:<32} {r['geo']:<14}  ERR  {r['error'][:50]}")
            continue
        rank = r["accurite_rank"]
        rank_s = str(rank) if rank else "—"
        top3 = " | ".join(r["top3"])
        print(f"{r['query']:<32} {r['geo']:<14} {rank_s:>5} {r['pack_size']:>5}  {top3}")

    out = Path(__file__).parent / f"results-{today}.json"
    out.write_text(json.dumps(results, indent=2))
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
