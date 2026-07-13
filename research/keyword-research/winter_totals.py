"""
Winter demand for AccuRite, ranked by WINTER TOTAL.

Metric (Ross's call, 2026-07-13): winter_total = Nov + Dec + Jan + Feb search volume,
summed straight from the DataForSEO `monthly_searches` array. No index, no ratio.
The question is "how many people search this during the months the crews are idle",
and the total answers it directly. A flat keyword with big volume still delivers a
big winter, and the earlier ratio approach wrongly penalized exactly that.

Capability scope, confirmed by Ross 2026-07-13:
  - NO snow removal / plowing.
  - NO septic PUMPING. Septic INSTALLATION only.
  - NO indoor plumbing (frozen pipes inside a house or business).
  - YES buried/exterior line work — water main, sewer, utility trench.
  - YES demolition, excavation, drainage, grading, land clearing, retaining walls.

Reads the JSON already pulled on 2026-07-13; makes no new API calls.
Run: python winter_totals.py
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).parent
WINTER_MONTHS = {11, 12, 1, 2}
SOURCES = ["winter-lanes-2026-07-13.json", "winter-keywords-2026-07-13.json"]

# Work AccuRite does not do, or intent that never becomes a job.
EXCLUDE = [
    # not his services
    "snow", "plow", "plough", "blower", "pump", "pumping", "septic tank service",
    "trenchless", "no dig", "reline", "liner", "relining",
    # indoor plumbing
    "plumber", "plumbing", "toilet", "faucet", "sink", "water heater", "refrigerator",
    "kitchen", "bathroom", "indoor", "inside",
    # cleaning / stains / DIY / retail / jobs
    "oil", "stain", "clean", "kitty", "efflorescence", "dissolv", "whitehouse",
    "diy", "how to", "yourself", "rental", "rent ", "for sale", "buy", "used ",
    "job", "jobs", "hiring", "salary", "school", "training", "license",
    "game", "simulator", "toy", "movie", "meaning", "definition", "mineral",
]

# Map surviving keywords to the AccuRite service that would own the content.
SERVICE_MAP = [
    ("septic",        ["septic", "leach", "drain field", "perc test"]),
    ("sewer/water line", ["sewer", "water line", "waterline", "water main", "utility line", "pipe repair"]),
    ("demolition",    ["demolition", "demolish", "demo ", "tear down", "concrete removal"]),
    ("drainage",      ["french drain", "drainage", "standing water", "yard drain"]),
    ("excavation",    ["excavat", "basement", "foundation", "frost line", "dig"]),
    ("grading/clearing", ["grading", "land clearing", "site prep", "site work"]),
    ("retaining wall", ["retaining wall"]),
    ("hauling",       ["hauling", "haul", "dirt delivery", "gravel"]),
]


def service_of(kw: str) -> str | None:
    k = kw.lower()
    for service, needles in SERVICE_MAP:
        if any(n in k for n in needles):
            return service
    return None


def excluded(kw: str) -> bool:
    k = kw.lower()
    return any(x in k for x in EXCLUDE)


def winter_total(monthly: list[dict] | None) -> int:
    if not monthly:
        return 0
    return sum(
        (m.get("search_volume") or 0) for m in monthly if m.get("month") in WINTER_MONTHS
    )


def load_rows() -> list[dict]:
    rows: list[dict] = []
    for name in SOURCES:
        path = HERE / name
        if not path.exists():
            continue
        data = json.loads(path.read_text())
        if "lanes" in data:
            for lane_rows in data["lanes"].values():
                rows.extend(lane_rows)
        else:
            rows.extend(data.get("rows", []))
    return rows


def main() -> int:
    best: dict[str, dict] = {}
    for r in load_rows():
        kw = r.get("keyword")
        if not kw or excluded(kw):
            continue
        service = service_of(kw)
        if not service:
            continue
        wt = winter_total(r.get("monthly_searches"))
        if wt < 200:  # floor: below this the winter traffic can't justify a page
            continue
        if kw not in best or wt > best[kw]["winter_total"]:
            best[kw] = {
                "keyword": kw,
                "service": service,
                "winter_total": wt,
                "avg_month": r.get("ut_volume") or 0,
                "cpc": r.get("cpc"),
            }

    rows = sorted(best.values(), key=lambda r: r["winter_total"], reverse=True)

    print("AccuRite winter demand — Utah, DataForSEO monthly_searches pulled 2026-07-13")
    print("Ranked by WINTER TOTAL = Nov + Dec + Jan + Feb searches\n")
    hdr = f"{'keyword':<42} {'service':<17} {'WINTER':>7} {'avg/mo':>7} {'CPC':>8}"
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        cpc = f"${r['cpc']:.2f}" if isinstance(r["cpc"], (int, float)) else "-"
        print(f"{r['keyword'][:42]:<42} {r['service']:<17} "
              f"{r['winter_total']:>7} {r['avg_month']:>7} {cpc:>8}")

    print("\n\n=== WINTER TOTAL BY SERVICE ===")
    by_service: dict[str, int] = {}
    for r in rows:
        by_service[r["service"]] = by_service.get(r["service"], 0) + r["winter_total"]
    for service, total in sorted(by_service.items(), key=lambda kv: kv[1], reverse=True):
        print(f"{service:<20} {total:>7}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
