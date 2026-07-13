"""
Targeted winter-lane keyword pull for AccuRite (Northern Utah).

Scoped by the client's actual winter capability, confirmed by Ross 2026-07-13:
  - NO snow removal / plowing.
  - NO indoor plumbing (frozen pipes inside a house or business).
  - YES buried/exterior line work — water main, sewer, utility trench "out of the road".
  - YES emergency winter call-outs, exterior/underground only.
  - Goal is WINTER WORK to keep crews paid, not just spring bookings.

Three lanes:
  1. demolition        — the one core service that already peaks in January.
  2. water_main_break  — exterior emergency dig; excludes indoor plumbing intent.
  3. winter_excavation — frozen-ground capability + off-season scheduling intent.

Same seasonality method as pull_winter_seasonality.py:
  winter_index = mean(Nov..Feb volume) / mean(12-month volume)

Run: DATAFORSEO_AUTH=... python pull_winter_lanes.py
Output: prints per-lane tables + writes winter-lanes-YYYY-MM-DD.json next to this file.
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
MONTH_NAMES = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
               7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}

LANES = {
    "demolition": [
        "demolition contractor",
        "demolition services",
        "house demolition",
        "concrete removal",
        "concrete driveway removal",
        "shed removal",
        "garage demolition",
        "barn demolition",
        "interior demolition",
        "pool removal",
        "demolition cost",
    ],
    "water_main_break": [
        "water main break",
        "water main repair",
        "water main replacement",
        "broken water line in yard",
        "water line replacement cost",
        "sewer line repair",
        "sewer line replacement",
        "buried water line leak",
        "water service line repair",
        "emergency excavation",
        "utility line repair",
        "water leak in yard",
    ],
    "winter_excavation": [
        "winter excavation",
        "excavating in winter",
        "can you excavate in winter",
        "digging in frozen ground",
        "frost line depth utah",
        "winter construction",
        "off season construction discount",
        "excavation contractor availability",
        "when to schedule excavation",
    ],
}

# Intent we cannot serve: indoor plumbing, DIY, equipment, jobs.
NOISE = [
    "plumber", "plumbing", "under sink", "kitchen", "bathroom", "toilet", "faucet",
    "water heater", "pipe in house", "inside", "indoor", "basement pipe",
    "diy", "how to fix", "yourself", "rental", "rent ", "for sale", "buy",
    "job", "jobs", "hiring", "salary", "school", "training", "license",
    "insurance cover", "home warranty",
]


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


def winter_index(monthly: list[dict] | None):
    if not monthly:
        return None, None
    vols = [m.get("search_volume") or 0 for m in monthly]
    if not vols or sum(vols) == 0:
        return None, None
    mean_all = statistics.mean(vols)
    winter = [(m.get("search_volume") or 0) for m in monthly if m.get("month") in WINTER_MONTHS]
    if not winter or mean_all == 0:
        return None, None
    peak = max(monthly, key=lambda m: m.get("search_volume") or 0)
    return statistics.mean(winter) / mean_all, MONTH_NAMES[peak["month"]]


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
        print(f"... expanding {len(seeds)} seeds for lane '{lane}' @ Utah", file=sys.stderr)
        rows = []
        for item in pull(auth, seeds):
            kw = item.get("keyword")
            if not kw or is_noise(kw):
                continue
            monthly = item.get("monthly_searches")
            idx, peak = winter_index(monthly)
            rows.append({
                "keyword": kw,
                "lane": lane,
                "ut_volume": item.get("search_volume"),
                "cpc": item.get("cpc"),
                "competition": item.get("competition"),
                "winter_index": round(idx, 2) if idx is not None else None,
                "peak_month": peak,
                "monthly_searches": monthly,
            })
        all_rows[lane] = rows

    for lane, rows in all_rows.items():
        keep = [
            r for r in rows
            if isinstance(r["ut_volume"], (int, float)) and r["ut_volume"] >= 20
            and r["winter_index"] is not None
        ]
        keep.sort(key=lambda r: (r["winter_index"], r["ut_volume"]), reverse=True)

        print(f"\n\n=== LANE: {lane.upper()} (UT vol >= 20, ranked by winter index) ===")
        hdr = f"{'keyword':<42} {'UT/mo':>6} {'wIdx':>5} {'peak':>5} {'CPC$':>7}  {'Jan......Dec':<12}"
        print(hdr)
        print("-" * len(hdr))
        for r in keep[:18]:
            cpc = f"{r['cpc']:.2f}" if isinstance(r["cpc"], (int, float)) else "-"
            spark = sparkline(r["monthly_searches"]) if r.get("monthly_searches") else ""
            print(f"{r['keyword'][:42]:<42} {r['ut_volume']:>6} {r['winter_index']:>5.2f} "
                  f"{str(r['peak_month']):>5} {cpc:>7}  {spark:<12}")
        if not keep:
            print("(nothing above volume floor)")

    out = Path(__file__).parent / f"winter-lanes-{today}.json"
    out.write_text(json.dumps({
        "date": today,
        "location": LOCATION,
        "capability_scope": "no snow removal; no indoor plumbing; exterior/buried line work only",
        "method": "winter_index = mean(Nov..Feb volume) / mean(12-month volume)",
        "lanes": all_rows,
    }, indent=2))
    print(f"\nWrote {out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
