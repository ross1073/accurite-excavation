"""
Winter-seasonal keyword discovery for AccuRite Excavation (Northern Utah).

Goal: find search terms that (a) have real volume in Utah, and (b) peak in the
winter months, so content can be written and indexed BEFORE the demand arrives.

Method:
  1. Discovery — keywords_data/google_ads/keywords_for_keywords/live expands a set
     of AccuRite-service seeds into related real queries, at Utah state level.
  2. Seasonality — the same response carries `monthly_searches`, a 12-month array of
     per-month volume. Winter index = mean(Nov..Feb) / mean(all 12 months). An index
     of 1.0 means flat year-round; 2.0 means winter months run double the annual mean.

A keyword is only a winter play if BOTH hold: non-trivial Utah volume AND index > 1.
High index on 10 searches/mo is noise, so volume is reported alongside, never hidden.

Run: DATAFORSEO_AUTH=... python pull_winter_seasonality.py
Output: prints ranked tables + writes winter-keywords-YYYY-MM-DD.json next to this file.
"""
from __future__ import annotations

import json
import os
import statistics
import sys
from datetime import date
from pathlib import Path

import requests

BASE = "https://api.dataforseo.com/v3"
KEYWORDS_FOR_KEYWORDS = f"{BASE}/keywords_data/google_ads/keywords_for_keywords/live"

LOCATION = "Utah,United States"
WINTER_MONTHS = {11, 12, 1, 2}

# Seeds grouped by the AccuRite service they map to. Each seed is expanded by Google Ads
# into related real queries; the seeds themselves are also scored.
SEED_GROUPS = {
    "excavation_core": [
        "excavation contractor",
        "excavation company",
        "basement excavation",
        "foundation excavation",
        "winter excavation",
    ],
    "frozen_ground": [
        "frozen ground excavation",
        "digging in frozen ground",
        "frost line depth",
        "ground frozen how deep",
    ],
    "drainage_water": [
        "french drain installation",
        "yard drainage",
        "drainage contractor",
        "standing water in yard",
        "basement flooding",
        "water line repair",
        "frozen water line",
        "burst pipe repair",
    ],
    "septic": [
        "septic system installation",
        "septic tank repair",
        "septic tank pumping",
        "frozen septic line",
    ],
    "snow_winter_services": [
        "snow removal",
        "snow plowing",
        "commercial snow removal",
        "snow hauling",
    ],
    "sitework_grading": [
        "grading contractor",
        "land clearing",
        "retaining wall contractor",
        "demolition contractor",
        "site preparation",
    ],
    "planning_intent": [
        "excavation cost",
        "basement excavation cost",
        "when to start excavation",
        "spring construction schedule",
    ],
}


def auth_headers(auth: str) -> dict:
    return {"Authorization": f"Basic {auth}", "Content-Type": "application/json"}


def pull(auth: str, seeds: list[str]) -> list[dict]:
    """Expand seeds into related keywords with 12-month volume history."""
    payload = [{
        "keywords": seeds,
        "location_name": LOCATION,
        "language_name": "English",
        "search_partners": False,
        "sort_by": "search_volume",
    }]
    r = requests.post(KEYWORDS_FOR_KEYWORDS, json=payload, headers=auth_headers(auth), timeout=180)
    r.raise_for_status()
    body = r.json()
    tasks = body.get("tasks") or []
    if not tasks:
        return []
    task = tasks[0]
    if task.get("status_code") != 20000:
        print(f"  ! task error: {task.get('status_message')}", file=sys.stderr)
        return []
    return task.get("result") or []


def winter_index(monthly: list[dict] | None) -> tuple[float | None, int | None, str | None]:
    """Return (winter index, peak month volume, peak month label) from a monthly_searches array."""
    if not monthly:
        return None, None, None
    vols = [m.get("search_volume") or 0 for m in monthly]
    if not vols or sum(vols) == 0:
        return None, None, None
    annual_mean = statistics.mean(vols)
    if annual_mean == 0:
        return None, None, None

    winter_vols = [
        (m.get("search_volume") or 0) for m in monthly if m.get("month") in WINTER_MONTHS
    ]
    if not winter_vols:
        return None, None, None

    idx = statistics.mean(winter_vols) / annual_mean

    peak = max(monthly, key=lambda m: m.get("search_volume") or 0)
    peak_label = f"{peak.get('year')}-{peak.get('month'):02d}"
    return idx, peak.get("search_volume"), peak_label


def main() -> int:
    auth = os.environ.get("DATAFORSEO_AUTH", "")
    if not auth:
        print("ERROR: DATAFORSEO_AUTH not set", file=sys.stderr)
        return 1

    today = date.today().isoformat()
    seen: dict[str, dict] = {}

    for group, seeds in SEED_GROUPS.items():
        print(f"... expanding {len(seeds)} seeds for '{group}' @ Utah", file=sys.stderr)
        for item in pull(auth, seeds):
            kw = item.get("keyword")
            if not kw or kw in seen:
                continue
            monthly = item.get("monthly_searches")
            idx, peak_vol, peak_label = winter_index(monthly)
            seen[kw] = {
                "keyword": kw,
                "seed_group": group,
                "ut_volume": item.get("search_volume"),
                "cpc": item.get("cpc"),
                "competition": item.get("competition"),
                "winter_index": round(idx, 2) if idx is not None else None,
                "peak_month": peak_label,
                "peak_volume": peak_vol,
                "monthly_searches": monthly,
            }

    rows = list(seen.values())
    print(f"\nPulled {len(rows)} unique keywords @ Utah — {today}", file=sys.stderr)

    def is_winter_play(r: dict) -> bool:
        return (
            isinstance(r["ut_volume"], (int, float))
            and r["ut_volume"] >= 30
            and r["winter_index"] is not None
            and r["winter_index"] >= 1.15
        )

    winners = sorted(
        (r for r in rows if is_winter_play(r)),
        key=lambda r: (r["winter_index"], r["ut_volume"]),
        reverse=True,
    )

    hdr = f"{'keyword':<44} {'group':<20} {'UT/mo':>6} {'wIdx':>5} {'peak':>8} {'CPC$':>6}"
    print(f"\n=== WINTER-SEASONAL KEYWORDS (UT vol >= 30, winter index >= 1.15) ===")
    print(hdr)
    print("-" * len(hdr))
    for r in winners:
        cpc = f"{r['cpc']:.2f}" if isinstance(r["cpc"], (int, float)) else "-"
        print(f"{r['keyword'][:44]:<44} {r['seed_group']:<20} "
              f"{r['ut_volume']:>6} {r['winter_index']:>5.2f} {str(r['peak_month']):>8} {cpc:>6}")

    out = Path(__file__).parent / f"winter-keywords-{today}.json"
    out.write_text(json.dumps({
        "date": today,
        "location": LOCATION,
        "winter_months": sorted(WINTER_MONTHS),
        "method": "winter_index = mean(Nov..Feb volume) / mean(12-month volume)",
        "rows": sorted(rows, key=lambda r: r["ut_volume"] or 0, reverse=True),
    }, indent=2))
    print(f"\nWrote {out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
