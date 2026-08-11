"""
Keyword-gap pull for the "clearing & grubbing / new road subgrade" blog topic.

Context (2026-08-11): Ross has drone footage of AccuRite's GPS-guided dozer
grubbing organic material off a new road alignment. Site audit that day showed
the words "GPS", "machine control", "proof roll" and "deleterious" appear ZERO
times anywhere in src/content/ — so the machine-control angle is uncovered.

Lanes are the candidate topical buckets for that post. Volumes are Utah-level
Google Ads data via DataForSEO keywords_for_keywords (same method and endpoint
as pull_winter_lanes.py).

Run: DATAFORSEO_AUTH=... python pull_roadbuild_lanes.py
Output: prints per-lane tables + writes roadbuild-lanes-YYYY-MM-DD.json here.
"""
from __future__ import annotations

import json
import os
import sys
from datetime import date
from pathlib import Path

import requests

BASE = "https://api.dataforseo.com/v3"
KEYWORDS_FOR_KEYWORDS = f"{BASE}/keywords_data/google_ads/keywords_for_keywords/live"

LOCATION = "Utah,United States"
MONTH_NAMES = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
               7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}

# terms that pull in DIY/rental/equipment-sales intent rather than hire intent
NOISE = [
    "for sale", "rental", "rent ", " rent", "jobs", "salary", "job description",
    "game", "simulator", "minecraft", "toy", "rc ", "used ", "auction",
    "how to build a", "definition", "meaning", "wiki",
]

LANES = {
    "clearing_grubbing": [
        "clearing and grubbing",
        "grubbing",
        "land clearing",
        "lot clearing",
        "brush clearing",
        "site clearing",
        "tree and stump removal",
        "land clearing cost per acre",
    ],
    "road_building": [
        "road construction",
        "private road construction",
        "gravel road construction",
        "new road cost per mile",
        "subdivision road construction",
        "road grading",
        "driveway grading",
        "access road construction",
    ],
    "site_prep_subgrade": [
        "site preparation",
        "site work contractor",
        "building pad preparation",
        "topsoil removal",
        "topsoil stripping",
        "subgrade preparation",
        "soil compaction",
        "compaction testing",
        "proof roll",
        "structural fill",
    ],
    "machine_control": [
        "gps grading",
        "gps dozer",
        "machine control grading",
        "3d machine control",
        "gps guided excavation",
        "grade control system",
    ],
}


def auth_headers(auth: str) -> dict:
    return {"Authorization": f"Basic {auth}", "Content-Type": "application/json"}


def is_noise(kw: str) -> bool:
    k = kw.lower()
    return any(n in k for n in NOISE)


def pull(auth: str, seeds: list[str]) -> list[dict]:
    payload = [{
        "keywords": seeds,
        "location_name": LOCATION,
        "language_name": "English",
        "search_partners": False,
        "sort_by": "search_volume",
    }]
    r = requests.post(KEYWORDS_FOR_KEYWORDS, json=payload, headers=auth_headers(auth), timeout=180)
    r.raise_for_status()
    tasks = r.json().get("tasks") or []
    if not tasks or tasks[0].get("status_code") != 20000:
        msg = tasks[0].get("status_message") if tasks else "no tasks"
        print(f"  ! task error: {msg}", file=sys.stderr)
        return []
    return tasks[0].get("result") or []


def peak_month(monthly: list[dict] | None):
    if not monthly:
        return None
    vols = [m.get("search_volume") or 0 for m in monthly]
    if sum(vols) == 0:
        return None
    return MONTH_NAMES[max(monthly, key=lambda m: m.get("search_volume") or 0)["month"]]


def sparkline(monthly: list[dict]) -> str:
    blocks = " ▁▂▃▄▅▆▇█"
    by_month = {m.get("month"): (m.get("search_volume") or 0) for m in monthly}
    vols = [by_month.get(m, 0) for m in range(1, 13)]
    peak = max(vols) or 1
    return "".join(blocks[min(8, round(v / peak * 8))] for v in vols)


def main() -> int:
    auth = os.environ.get("DATAFORSEO_AUTH", "")
    if not auth:
        print("ERROR: DATAFORSEO_AUTH not set", file=sys.stderr)
        return 1

    today = date.today().isoformat()
    all_rows: dict[str, list[dict]] = {}

    for lane, seeds in LANES.items():
        print(f"... expanding {len(seeds)} seeds for lane '{lane}' @ {LOCATION}", file=sys.stderr)
        rows = []
        for item in pull(auth, seeds):
            kw = item.get("keyword")
            if not kw or is_noise(kw):
                continue
            monthly = item.get("monthly_searches")
            rows.append({
                "keyword": kw,
                "lane": lane,
                "ut_volume": item.get("search_volume"),
                "cpc": item.get("cpc"),
                "competition": item.get("competition"),
                "peak_month": peak_month(monthly),
                "monthly_searches": monthly,
            })
        all_rows[lane] = rows

    for lane, rows in all_rows.items():
        keep = [r for r in rows if isinstance(r["ut_volume"], (int, float)) and r["ut_volume"] >= 10]
        keep.sort(key=lambda r: r["ut_volume"], reverse=True)

        print(f"\n\n=== LANE: {lane.upper()} (Utah vol >= 10) ===")
        hdr = f"{'keyword':<44} {'UT/mo':>6} {'CPC$':>7} {'comp':>6} {'peak':>5}  {'Jan......Dec':<12}"
        print(hdr)
        print("-" * len(hdr))
        for r in keep[:20]:
            cpc = f"{r['cpc']:.2f}" if isinstance(r["cpc"], (int, float)) else "-"
            spark = sparkline(r["monthly_searches"]) if r.get("monthly_searches") else ""
            print(f"{r['keyword'][:44]:<44} {r['ut_volume']:>6} {cpc:>7} "
                  f"{str(r['competition'])[:6]:>6} {str(r['peak_month']):>5}  {spark:<12}")
        if not keep:
            print("(nothing above volume floor)")

    out = Path(__file__).parent / f"roadbuild-lanes-{today}.json"
    out.write_text(json.dumps({
        "date": today,
        "location": LOCATION,
        "endpoint": "keywords_data/google_ads/keywords_for_keywords/live",
        "purpose": "keyword gap check for clearing-and-grubbing / new road subgrade blog post",
        "lanes": all_rows,
    }, indent=2))
    print(f"\nWrote {out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
