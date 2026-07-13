"""
AccuRite demand by season — same keyword clusters, four equal 3-month buckets.

Winter Dec-Jan-Feb | Spring Mar-Apr-May | Summer Jun-Jul-Aug | Fall Sep-Oct-Nov

NOTE: the winter numbers here will NOT match winter_totals.py. That script used a
4-month winter (Nov-Feb) because Nov is when the crews go quiet. This one uses equal
3-month buckets so the four seasons are actually comparable to each other. Same source
data either way: DataForSEO `monthly_searches`, Utah, pulled 2026-07-13.

Scope, per Ross 2026-07-13: septic dropped; no snow, no pumping, no trenchless,
no indoor plumbing, no competitor brand names.

Run: python season_totals.py
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).parent
SOURCES = ["winter-lanes-2026-07-13.json", "winter-keywords-2026-07-13.json"]

SEASONS = {
    "Winter": (12, 1, 2),
    "Spring": (3, 4, 5),
    "Summer": (6, 7, 8),
    "Fall":   (9, 10, 11),
}

# The clusters Ross signed off on — one representative keyword each, septic removed.
CLUSTERS = [
    ("sewer line repair near me",        "sewer/water line"),
    ("excavation companies near me",     "excavation"),
    ("french drain",                     "drainage"),
    ("french drain installation",        "drainage"),
    ("excavation company",               "excavation"),
    ("sewer repair near me",             "sewer/water line"),
    ("excavation contractor",            "excavation"),
    ("french drain installation near me","drainage"),
    ("demolition contractor",            "demolition"),
    ("demolition contractors near me",   "demolition"),
    ("sewer repair",                     "sewer/water line"),
    ("retaining wall contractor",        "retaining wall"),
]


def load() -> dict[str, dict]:
    out: dict[str, dict] = {}
    for name in SOURCES:
        path = HERE / name
        if not path.exists():
            continue
        data = json.loads(path.read_text())
        rows = (
            [r for lane in data["lanes"].values() for r in lane]
            if "lanes" in data else data.get("rows", [])
        )
        for r in rows:
            kw = r.get("keyword")
            if kw and kw not in out and r.get("monthly_searches"):
                out[kw] = r
    return out


def season_total(monthly: list[dict], months: tuple[int, ...]) -> int:
    return sum((m.get("search_volume") or 0) for m in monthly if m.get("month") in months)


def main() -> int:
    data = load()

    for season, months in SEASONS.items():
        rows = []
        for kw, service in CLUSTERS:
            r = data.get(kw)
            if not r:
                continue
            rows.append({
                "keyword": kw,
                "service": service,
                "total": season_total(r["monthly_searches"], months),
                "avg": r.get("ut_volume") or 0,
                "cpc": r.get("cpc"),
            })
        rows.sort(key=lambda x: x["total"], reverse=True)

        print(f"\n### {season.upper()}  (months {', '.join(str(m) for m in months)})")
        hdr = f"{'query cluster':<38} {'service':<17} {'TOTAL':>6} {'avg/mo':>7} {'CPC':>8}"
        print(hdr)
        print("-" * len(hdr))
        for r in rows:
            cpc = f"${r['cpc']:.2f}" if isinstance(r["cpc"], (int, float)) else "-"
            print(f"{r['keyword'][:38]:<38} {r['service']:<17} {r['total']:>6} {r['avg']:>7} {cpc:>8}")
        print(f"{'SEASON TOTAL':<38} {'':<17} {sum(r['total'] for r in rows):>6}")

    print("\n\n### BY SERVICE, ACROSS SEASONS")
    services = sorted({s for _, s in CLUSTERS})
    hdr = f"{'service':<18} " + " ".join(f"{s:>8}" for s in SEASONS)
    print(hdr)
    print("-" * len(hdr))
    for service in services:
        cells = []
        for season, months in SEASONS.items():
            tot = sum(
                season_total(data[kw]["monthly_searches"], months)
                for kw, svc in CLUSTERS if svc == service and kw in data
            )
            cells.append(f"{tot:>8}")
        print(f"{service:<18} " + " ".join(cells))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
