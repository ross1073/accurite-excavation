"""
El Nino / drainage blog-post keyword pull — AccuRite, 2026-11-26.

Purpose: pick the target phrase for the draft post
"El Nino winter 2026-27: what it means for your Northern Utah property".

Three live tasks (Google Ads data via DataForSEO):
  1. search_volume, State of Utah (21175)           — candidate list below
  2. search_volume, Salt Lake City-Ogden UT DMA (200770) — same list
     (DMA is the only metro-level Google Ads location covering Ogden; its NAME
      is just the DMA label — it is not a service-area claim.)
  3. keywords_for_keywords, State of Utah — a few seeds, to catch variants

Auth: DATAFORSEO_AUTH env var or ~/.config/secrets/secrets.env (same loader as
pull_winter_2026_expansion.py). Never prints the credential.

Writes research/keyword-research/2026-11-26_el-nino-drainage_raw.json and prints
a sorted table plus the total API cost DataForSEO reported.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pull_winter_2026_expansion import read_auth, auth_headers  # noqa: E402

BASE = "https://api.dataforseo.com/v3/keywords_data/google_ads"
OUT = Path(__file__).resolve().parent / "2026-11-26_el-nino-drainage_raw.json"

CANDIDATES = [
    # El Nino / outlook
    "el nino utah", "utah el nino", "el nino winter utah", "el nino 2026 utah",
    "el nino 2026", "el nino winter", "el nino", "el nino snow utah",
    "utah winter forecast", "utah winter outlook", "utah winter 2026",
    # drainage
    "drainage contractor", "drainage contractors", "drainage contractor near me",
    "drainage contractors near me", "yard drainage", "yard drainage contractor",
    "yard drainage solutions", "drainage solutions", "french drain installation",
    "french drain contractor", "drainage company", "drainage repair",
    "standing water in yard", "yard flooding", "flood prevention",
    # grading
    "yard grading", "land grading", "grading contractor", "regrading yard",
    "driveway grading",
    # culverts / ditches
    "culvert repair", "culvert installation", "culvert replacement",
    "driveway culvert", "driveway culvert installation", "culvert pipe installation",
    "ditch cleaning", "ditch digging", "drainage ditch",
    # runoff / erosion / washout
    "spring runoff", "spring runoff utah", "utah spring runoff", "runoff 2027 utah",
    "erosion control", "washout repair", "gravel driveway repair",
    "storm drain installation",
    # retaining walls
    "retaining wall drainage", "retaining wall repair",
]

SEEDS = ["el nino utah", "drainage contractor", "culvert repair", "spring runoff", "yard drainage"]


def post(endpoint: str, payload: list[dict], headers: dict) -> dict:
    r = requests.post(f"{BASE}/{endpoint}/live", headers=headers, json=payload, timeout=180)
    r.raise_for_status()
    return r.json()


def main() -> None:
    auth = read_auth()
    if not auth:
        sys.exit("DATAFORSEO_AUTH not found")
    h = auth_headers(auth)

    runs = {
        "sv_utah": post("search_volume", [{"keywords": CANDIDATES, "location_code": 21175, "language_code": "en"}], h),
        "sv_dma": post("search_volume", [{"keywords": CANDIDATES, "location_code": 200770, "language_code": "en"}], h),
        "kfk_utah": post("keywords_for_keywords", [{"keywords": SEEDS, "location_code": 21175, "language_code": "en"}], h),
    }
    total_cost = 0.0
    for name, resp in runs.items():
        t = resp["tasks"][0]
        total_cost += float(t.get("cost") or 0)
        print(f"{name}: {t['status_code']} {t['status_message']} cost=${t.get('cost')}", file=sys.stderr)

    OUT.write_text(json.dumps({"pulled": "2026-11-26", "total_cost_usd": round(total_cost, 4), "runs": runs}, indent=1))

    def rows(name):
        return {r["keyword"]: r for r in (runs[name]["tasks"][0]["result"] or [])}

    ut, dma = rows("sv_utah"), rows("sv_dma")
    print("| keyword | Utah vol | DMA vol | CPC | competition | Utah monthly (oldest→newest) |")
    print("|---|---|---|---|---|---|")
    for kw in sorted(CANDIDATES, key=lambda k: -((ut.get(k) or {}).get("search_volume") or 0)):
        u = ut.get(kw) or {}
        d = dma.get(kw) or {}
        months = sorted(u.get("monthly_searches") or [], key=lambda m: (m["year"], m["month"]))
        spark = " ".join(f"{m['month']}/{str(m['year'])[2:]}:{m['search_volume']}" for m in months)
        print(f"| {kw} | {u.get('search_volume')} | {d.get('search_volume')} | {u.get('cpc')} | {u.get('competition')} | {spark} |")

    print("\n### keywords_for_keywords (Utah), volume >= 20, sorted")
    kfk = runs["kfk_utah"]["tasks"][0]["result"] or []
    for r in sorted(kfk, key=lambda r: -(r.get("search_volume") or 0)):
        if (r.get("search_volume") or 0) >= 20:
            print(f"- {r['keyword']}: {r['search_volume']} (cpc {r.get('cpc')})")
    print(f"\nTOTAL DataForSEO cost: ${total_cost:.4f}")


if __name__ == "__main__":
    main()
