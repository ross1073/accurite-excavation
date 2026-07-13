"""
Rebuild AccuRite's seasonal demand buckets from the FULL 2026-07-13 pull, with an
explicit, auditable intent rule — and show every keyword that lands in each bucket.

Why this exists: the earlier season tables summed 12 hand-picked "representative"
keywords. That hid two problems Ross caught:
  1. The bucket labels ("excavation", "drainage") implied full coverage. They didn't have it.
  2. `french drain` (880/mo, CPC $2.33) is a bare informational head term — homeowners
     reading, not hiring. A low CPC is the market telling you there's no job behind
     the click. It was inflating the drainage bucket.

INTENT RULE (the whole thing, no hidden logic):

  HIRE   — the searcher wants to pay someone. Must contain a hire-signal token
           (contractor, company, companies, service, services, near me, installer,
           installation, repair, replacement, replace, install) AND survive the
           DIY/equipment/jobs/brand filters below.

  RESEARCH — cost/price/how-much queries. A real buyer often starts here, but they are
           not ready to call. Counted SEPARATELY, never mixed into the hire totals.

  REJECT — DIY ("how to", "yourself", "diy"), equipment/retail, jobs, competitor brand
           names, indoor plumbing, snow, septic pumping, trenchless. Reason recorded.

Everything is printed with its intent tag and CPC so the grouping can be audited by eye.
Source: DataForSEO monthly_searches, Utah, pulled 2026-07-13. No new API calls.
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

# --- the intent rule -------------------------------------------------------------
# STRICT (Ross, 2026-07-13). The keyword must name a PERSON TO HIRE or ask for one
# nearby. Verbs describing the work -- repair, replace, install, fix -- are NOT hire
# signals: a do-it-yourselfer types "sewer line repair" too. Including them padded the
# sewer bucket with ambiguous traffic and flattered a conclusion I'd already drawn.
HIRE_SIGNALS = [
    "contractor", "contractors", "company", "companies", "near me",
    "service", "services",
]

RESEARCH_SIGNALS = ["cost", "price", "how much", "estimate", "quote"]

REJECT = {
    "diy": ["diy", "how to", "how do", "yourself", "youtube", "video", "tutorial", "guide"],
    "equipment/retail": [
        "plow", "blower", "blade", "spreader", "shovel", "excavator for", "mini excavator",
        "rental", "rent ", "for sale", "buy", "used ", "parts", "amazon", "home depot",
        "lowes", "toro", "meyer", "kubota", "bobcat", "caterpillar", "john deere",
    ],
    "jobs": ["job", "jobs", "hiring", "salary", "career", "school", "training", "license"],
    "out of scope": [
        "snow", "plowing", "pump", "pumping", "trenchless", "no dig", "reline", "relining",
        "liner", "plumber", "plumbing", "toilet", "faucet", "sink", "water heater",
        "refrigerator", "kitchen", "bathroom", "indoor", "inside",
        # "sewer tank ..." is Google's alias for SEPTIC tank (same $60.70 CPC as the
        # septic term). Septic dropped per Ross 2026-07-13, so these go too.
        "septic", "sewer tank",
    ],
    "cleaning/other": ["oil", "stain", "clean", "kitty", "efflorescence", "dissolv", "mineral"],
    "competitor brand": [
        "bryce", "christensen", "mitchell", "prime excavation", "quality excavating",
        "r and d", "whitehouse", "skinner", "triple h",
    ],
}

SERVICE_MAP = [
    ("sewer/water line", ["sewer", "water line", "waterline", "water main", "utility line"]),
    ("drainage",         ["french drain", "drainage", "standing water", "yard drain"]),
    ("demolition",       ["demolition", "demolish", "demo contractor", "demo companies",
                          "demo contractors", "tear down", "concrete removal"]),
    ("excavation",       ["excavat", "basement dig", "foundation dig", "site prep", "grading"]),
    ("retaining wall",   ["retaining wall"]),
    ("land clearing",    ["land clearing"]),
]


def classify(kw: str) -> tuple[str, str]:
    """Return (intent, reason). intent in {HIRE, RESEARCH, REJECT}."""
    k = kw.lower()
    for reason, needles in REJECT.items():
        if any(n in k for n in needles):
            return "REJECT", reason
    if any(s in k for s in RESEARCH_SIGNALS):
        return "RESEARCH", "cost/price query — buyer not ready to call"
    if any(s in k for s in HIRE_SIGNALS):
        return "HIRE", "has hire-signal token"
    return "REJECT", "no hire signal — informational head term"


def service_of(kw: str) -> str | None:
    k = kw.lower()
    for service, needles in SERVICE_MAP:
        if any(n in k for n in needles):
            return service
    return None


def season_total(monthly, months) -> int:
    return sum((m.get("search_volume") or 0) for m in (monthly or []) if m.get("month") in months)


def load() -> dict[str, dict]:
    out: dict[str, dict] = {}
    for name in SOURCES:
        p = HERE / name
        if not p.exists():
            continue
        d = json.loads(p.read_text())
        rows = ([r for lane in d["lanes"].values() for r in lane]
                if "lanes" in d else d.get("rows", []))
        for r in rows:
            kw = r.get("keyword")
            if kw and r.get("monthly_searches") and kw not in out:
                out[kw] = r
    return out


def build():
    data = load()
    buckets: dict[str, list[dict]] = {}
    research: dict[str, list[dict]] = {}
    rejected: list[dict] = []

    for kw, r in data.items():
        service = service_of(kw)
        if not service:
            continue
        intent, reason = classify(kw)
        vol = r.get("ut_volume") or 0
        if vol < 20:
            continue
        rec = {
            "keyword": kw,
            "service": service,
            "intent": intent,
            "reason": reason,
            "avg_month": vol,
            "cpc": r.get("cpc"),
            "seasons": {s: season_total(r["monthly_searches"], m) for s, m in SEASONS.items()},
        }
        if intent == "HIRE":
            buckets.setdefault(service, []).append(rec)
        elif intent == "RESEARCH":
            research.setdefault(service, []).append(rec)
        else:
            rejected.append(rec)

    for v in buckets.values():
        v.sort(key=lambda r: r["seasons"]["Winter"], reverse=True)
    for v in research.values():
        v.sort(key=lambda r: r["seasons"]["Winter"], reverse=True)
    rejected.sort(key=lambda r: r["avg_month"], reverse=True)
    return buckets, research, rejected


if __name__ == "__main__":
    buckets, research, rejected = build()

    print("=== HIRE-INTENT BUCKETS (every keyword shown) ===")
    for service, rows in sorted(buckets.items()):
        tot = {s: sum(r["seasons"][s] for r in rows) for s in SEASONS}
        print(f"\n## {service}   Winter {tot['Winter']} | Spring {tot['Spring']} "
              f"| Summer {tot['Summer']} | Fall {tot['Fall']}")
        for r in rows:
            cpc = f"${r['cpc']:.2f}" if isinstance(r["cpc"], (int, float)) else "-"
            s = r["seasons"]
            print(f"   {r['keyword'][:40]:<40} {cpc:>8}  "
                  f"W{s['Winter']:>5} Sp{s['Spring']:>5} Su{s['Summer']:>5} F{s['Fall']:>5}")

    print("\n\n=== RESEARCH (cost/price — counted separately) ===")
    for service, rows in sorted(research.items()):
        for r in rows:
            cpc = f"${r['cpc']:.2f}" if isinstance(r["cpc"], (int, float)) else "-"
            print(f"   {r['keyword'][:40]:<40} {service:<17} {cpc:>8}")

    print("\n\n=== REJECTED (and why) ===")
    for r in rejected[:40]:
        cpc = f"${r['cpc']:.2f}" if isinstance(r["cpc"], (int, float)) else "-"
        print(f"   {r['keyword'][:40]:<40} {r['avg_month']:>5}/mo {cpc:>8}  <- {r['reason']}")

    print("\n\n=== SEASON TOTALS, HIRE INTENT ONLY ===")
    for s in SEASONS:
        print(f"{s:<8} {sum(r['seasons'][s] for rows in buckets.values() for r in rows):>7}")
