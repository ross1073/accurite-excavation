"""
Second-pass analysis over winter-keywords-<date>.json.

The raw discovery pull is dominated by snow-plow EQUIPMENT shoppers (ATV plows, Toro
snowblowers, brand names). Those have a winter spike but zero commercial value to an
excavation contractor — nobody buying a Meyer plow blade is hiring AccuRite.

This pass:
  1. Strips product/equipment/DIY/jobs intent so only hire-a-contractor queries survive.
  2. Ranks the survivors by winter index (demand that PEAKS in winter).
  3. Separately profiles AccuRite's core service terms month-by-month, so we can see
     which services actually survive a Utah winter and which go to zero — that decides
     whether winter content should sell winter WORK or sell spring PLANNING.

Run: python analyze_winter.py [path-to-winter-keywords-*.json]
"""
from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).parent
WINTER_MONTHS = {11, 12, 1, 2}

# Equipment / retail / DIY / jobs intent — a winter spike here is not a lead.
NOISE = [
    "plow", "plough", "blower", "blade", "spreader", "salt spreader", "shovel",
    "toro", "meyer", "western", "boss ", "fisher", "atv", "utv", "quad", "fourwheeler",
    "4wheeler", "tractor", "skid steer", "bobcat", "kubota", "john deere", "caterpillar",
    "for sale", "rental", "rent ", "rents", "buy", "price of", "used ", "parts",
    "job", "jobs", "hiring", "salary", "career", "school", "training", "license",
    "diy", "how to", "yourself", "amazon", "home depot", "lowes", "walmart",
    "game", "simulator", "toy", "movie", "meaning", "definition",
]

# Core AccuRite services — profile these month-by-month regardless of winter index.
CORE_TERMS = [
    "excavation contractor",
    "excavation companies near me",
    "basement excavation",
    "foundation excavation",
    "septic system installation",
    "septic tank repair",
    "french drain installation",
    "retaining wall contractor",
    "demolition contractor",
    "land clearing",
    "grading contractor",
    "excavation cost",
    "basement excavation cost",
]

MONTH_NAMES = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
               7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}


def is_noise(kw: str) -> bool:
    k = kw.lower()
    return any(n in k for n in NOISE)


def sparkline(monthly: list[dict]) -> str:
    """Chronological Jan..Dec bar sparkline, scaled to the keyword's own peak."""
    blocks = " ▁▂▃▄▅▆▇█"
    by_month = {m.get("month"): (m.get("search_volume") or 0) for m in monthly}
    vols = [by_month.get(m, 0) for m in range(1, 13)]
    peak = max(vols) or 1
    return "".join(blocks[min(8, round(v / peak * 8))] for v in vols)


def main() -> int:
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
    else:
        candidates = sorted(HERE.glob("winter-keywords-*.json"))
        if not candidates:
            print("No winter-keywords-*.json found", file=sys.stderr)
            return 1
        path = candidates[-1]

    data = json.loads(path.read_text())
    rows = data["rows"]
    print(f"Source: {path.name}  ({len(rows)} keywords, {data['location']})\n")

    # ---- 1. Winter-peaking SERVICE demand (noise stripped) --------------------
    service_rows = [
        r for r in rows
        if not is_noise(r["keyword"])
        and isinstance(r["ut_volume"], (int, float)) and r["ut_volume"] >= 20
        and r["winter_index"] is not None and r["winter_index"] >= 1.10
    ]
    service_rows.sort(key=lambda r: (r["winter_index"], r["ut_volume"]), reverse=True)

    print("=== WINTER-PEAKING DEMAND, SERVICE INTENT ONLY (UT vol >= 20, index >= 1.10) ===")
    hdr = f"{'keyword':<40} {'UT/mo':>6} {'wIdx':>5} {'CPC$':>7}  {'Jan........Dec':<14}"
    print(hdr)
    print("-" * len(hdr))
    for r in service_rows[:30]:
        cpc = f"{r['cpc']:.2f}" if isinstance(r["cpc"], (int, float)) else "-"
        spark = sparkline(r["monthly_searches"]) if r.get("monthly_searches") else ""
        print(f"{r['keyword'][:40]:<40} {r['ut_volume']:>6} {r['winter_index']:>5.2f} "
              f"{cpc:>7}  {spark:<14}")
    if not service_rows:
        print("(none)")

    # ---- 2. Core service seasonality profile ---------------------------------
    print(f"\n\n=== CORE ACCURITE SERVICES — SEASONAL SHAPE ===")
    print("wIdx < 1.0 = winter trough (sell spring PLANNING, not winter work)\n")
    by_kw = {r["keyword"]: r for r in rows}
    hdr2 = f"{'keyword':<40} {'UT/mo':>6} {'wIdx':>5} {'peak':>6} {'trough':>7}  {'Jan........Dec':<14}"
    print(hdr2)
    print("-" * len(hdr2))
    for term in CORE_TERMS:
        r = by_kw.get(term)
        if not r or not r.get("monthly_searches"):
            print(f"{term:<40} {'(no data)':>6}")
            continue
        monthly = r["monthly_searches"]
        peak = max(monthly, key=lambda m: m.get("search_volume") or 0)
        trough = min(monthly, key=lambda m: m.get("search_volume") or 0)
        idx = r["winter_index"] if r["winter_index"] is not None else float("nan")
        print(f"{term:<40} {r['ut_volume'] or 0:>6} {idx:>5.2f} "
              f"{MONTH_NAMES[peak['month']]:>6} {MONTH_NAMES[trough['month']]:>7}  {sparkline(monthly):<14}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
