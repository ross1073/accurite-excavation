"""
Keyword search-volume pull for the HHI / Hill AFB safety-letter blog post idea.

Goal: ground the "what trending keywords can this letter win traffic for?" question
in real Google Ads search-volume data instead of guesses. We pull each candidate
keyword at BOTH Utah-state level (local intent that actually converts for a Wasatch
Front excavation contractor) and US level (national informational demand — traffic
but low local conversion), so the local-vs-national split is visible.

Endpoint: keywords_data/google_ads/search_volume/live
  -> avg monthly search_volume, cpc, competition, plus 12-mo monthly_searches trend.

Run: DATAFORSEO_AUTH=... python pull_letter_keywords.py
Output: prints a sorted table + writes letter-keywords-YYYY-MM-DD.json next to this file.
"""
from __future__ import annotations
import json
import os
import sys
from datetime import date
from pathlib import Path

import requests

BASE = "https://api.dataforseo.com/v3"
SEARCH_VOLUME = f"{BASE}/keywords_data/google_ads/search_volume/live"

# Candidate keywords grouped by angle. Flat list sent to the API; cluster kept for labels.
CLUSTERS = {
    "A_federal_military": [
        "hill afb contractors",
        "hill air force base construction",
        "federal excavation contractor",
        "government excavation contractor",
        "military base construction contractor",
        "em385 compliance",
        "em 385-1-1",
        "davis bacon contractor utah",
        "prevailing wage contractor utah",
        "government construction contractor utah",
    ],
    "B_safety_educational": [
        "excavation safety",
        "trench safety",
        "osha trench safety",
        "excavation safety plan",
        "trenching and excavation safety",
        "osha excavation standards",
        "trench safety requirements",
        "excavation safety toolbox talk",
        "competent person excavation",
        "trench box requirements",
    ],
    "C_utah_commercial": [
        "commercial excavation utah",
        "excavation contractor utah",
        "excavation companies ogden",
        "site work contractor utah",
        "grading contractor utah",
        "excavation contractor near me",
    ],
    "D_b2b_credential": [
        "how to choose an excavation contractor",
        "excavation subcontractor",
        "bonded excavation contractor",
        "questions to ask excavation contractor",
    ],
}

LOCATIONS = [
    ("Utah", "Utah,United States"),
    ("US", "United States"),
]


def auth_headers(auth: str) -> dict:
    return {"Authorization": f"Basic {auth}", "Content-Type": "application/json"}


def kw_cluster(kw: str) -> str:
    for cluster, kws in CLUSTERS.items():
        if kw in kws:
            return cluster
    return "?"


def pull(auth: str, keywords: list[str], location_name: str) -> dict[str, dict]:
    payload = [{
        "keywords": keywords,
        "location_name": location_name,
        "language_name": "English",
    }]
    r = requests.post(SEARCH_VOLUME, json=payload, headers=auth_headers(auth), timeout=120)
    r.raise_for_status()
    tasks = r.json().get("tasks") or []
    out: dict[str, dict] = {}
    if not tasks:
        return out
    result = tasks[0].get("result") or []
    for item in result:
        kw = item.get("keyword")
        if not kw:
            continue
        out[kw] = {
            "search_volume": item.get("search_volume"),
            "cpc": item.get("cpc"),
            "competition": item.get("competition"),
            "competition_index": item.get("competition_index"),
        }
    return out


def main() -> int:
    auth = os.environ.get("DATAFORSEO_AUTH", "")
    if not auth:
        print("ERROR: DATAFORSEO_AUTH not set", file=sys.stderr)
        return 1

    all_keywords = [kw for kws in CLUSTERS.values() for kw in kws]
    today = date.today().isoformat()

    by_location: dict[str, dict[str, dict]] = {}
    for label, loc_name in LOCATIONS:
        print(f"... pulling {len(all_keywords)} keywords @ {label}", file=sys.stderr)
        by_location[label] = pull(auth, all_keywords, loc_name)

    # Merge into rows
    rows = []
    for kw in all_keywords:
        ut = by_location.get("Utah", {}).get(kw, {})
        us = by_location.get("US", {}).get(kw, {})
        rows.append({
            "keyword": kw,
            "cluster": kw_cluster(kw),
            "ut_volume": ut.get("search_volume"),
            "us_volume": us.get("search_volume"),
            "cpc": us.get("cpc") or ut.get("cpc"),
            "competition": us.get("competition") or ut.get("competition"),
        })

    # Sort by Utah volume desc (None -> -1), then US volume
    def sv(v):
        return v if isinstance(v, (int, float)) else -1
    rows.sort(key=lambda r: (sv(r["ut_volume"]), sv(r["us_volume"])), reverse=True)

    hdr = f"{'keyword':<40} {'cluster':<18} {'UT/mo':>7} {'US/mo':>8} {'CPC$':>7} {'comp':>10}"
    print(f"\nLetter/Hill-AFB keyword volume — {today}")
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        cpc_str = f"{r['cpc']:.2f}" if isinstance(r["cpc"], (int, float)) else "-"
        ut_str = str(r["ut_volume"]) if r["ut_volume"] is not None else "-"
        us_str = str(r["us_volume"]) if r["us_volume"] is not None else "-"
        comp_str = str(r["competition"] or "-")
        print(f"{r['keyword'][:40]:<40} {r['cluster']:<18} "
              f"{ut_str:>7} {us_str:>8} {cpc_str:>7} {comp_str:>10}")

    out = Path(__file__).parent / f"letter-keywords-{today}.json"
    out.write_text(json.dumps({"date": today, "rows": rows}, indent=2))
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
