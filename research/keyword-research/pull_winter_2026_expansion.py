"""
Winter 2026 expansion pull — AccuRite (local) + Utah regional / border.

Two batches:
  LOCAL   (Salt Lake City-Ogden metro):
    - demolition, land_clearing_tree, snow_removal_commercial, midland_fab_trailer
  REGIONAL (Utah statewide, location_code=21175):
    - bulk_salt_sand_haul, rv_park_campground, infra_pad_excavation

Endpoint: /keywords_data/google_ads/keywords_for_keywords/live
Auth:     DATAFORSEO_AUTH env var, or read from ~/.config/secrets/secrets.env.

Reads volume, CPC, competition, and 12-month monthly_searches per keyword.
Writes raw JSON to research/keyword-research/2026-09-15_winter_expansion_raw.json
and prints a comprehensive markdown table tagging AD candidates vs ORGANIC targets.

Ad-candidate rule (memory: reference_keyword_intent_filtering.md):
  - avg volume >= 100/mo AND
  - CPC >= $5 (commercial pricing signal) AND
  - keyword names a person/service to hire (contractor / company / near me /
    service / services / delivery / supplier / shop) OR is a commercial
    problem noun (repair / installation / plowing / removal) with a $5+ CPC.

Organic targets = everything else with volume >= 30/mo (research floor).

NOTE: `stump removal` seed is included by explicit request. Memory
feedback_accurite_no_stump_targeting.md — stump keywords have been rejected for
AccuRite targeting twice. Data is for reference, NOT for landing pages/meta.
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

# Salt Lake City-Ogden UT DMA (Google Ads criterion, DataForSEO location_code)
LOCAL_LOCATION_CODE = 200770         # Salt Lake City-Ogden UT DMA
LOCAL_LOCATION_NAME = "Salt Lake City-Ogden UT, United States"
# Fallback if the DMA code is not resolvable in DataForSEO for a given endpoint
LOCAL_FALLBACK_NAME = "Salt Lake City,Utah,United States"

REGIONAL_LOCATION_CODE = 21175       # State of Utah
REGIONAL_LOCATION_NAME = "Utah, United States"

MONTH_NAMES = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
               7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}
WINTER_MONTHS = {11, 12, 1, 2}

# --- Batch 1: LOCAL (SLC / Ogden metro) ---------------------------------------
LOCAL_LANES: dict[str, list[str]] = {
    "demolition": [
        "commercial demolition",
        "residential demolition",
        "building demolition",
        "house demolition",
        "concrete demolition",
    ],
    "land_clearing_tree": [
        "land clearing",
        "tree removal",
        "deforesting",
        "lot clearing",
        "brush clearing",
        "stump removal",   # per request; do NOT target — see file docstring
    ],
    "snow_removal_commercial": [
        "commercial snow removal",
        "parking lot snow plowing",
        "commercial snow plowing",
        "snow removal contracts",
    ],
    "midland_fab_trailer": [
        "dump trailer repair",
        "trailer repair near me",
        "trailer brake repair",
        "trailer jack replacement",
        "atv trailer repair",
        "utility trailer repair",
        "flatbed trailer repair",
        "tailgate repair",
        "welding repair shop",
    ],
}

# --- Batch 2: REGIONAL (Utah statewide) ---------------------------------------
REGIONAL_LANES: dict[str, list[str]] = {
    "bulk_salt_sand_haul": [
        "road salt supplier",
        "bulk road salt",
        "road salt delivery",
        "bulk sand delivery",
        "gravel hauling",
        "commercial road salt",
    ],
    "rv_park_campground": [
        "campground excavation",
        "rv park construction",
        "campground sewer line installation",
        "rv park utilities",
    ],
    "infra_pad_excavation": [
        "substation pad excavation",
        "pipeline pad contractor",
        "power line pad construction",
        "commercial equipment pad",
    ],
}

# Terms that pull DIY / rental / equipment-sales / hobbyist junk into an
# expansion. See reference_keyword_intent_filtering.md for the doctrine.
NOISE = [
    "for sale", "rental", "rent ", " rent", "jobs", "salary", "job description",
    "game", "simulator", "minecraft", "toy", "rc ", "used ", "auction",
    "how to build", "definition", "meaning", "wiki",
    "diy", "how to", "yourself",
]

# Hire-intent hints (person-noun / proximity / trade signal).
HIRE_HINTS = {
    "contractor", "contractors", "company", "companies", "near me",
    "service", "services", "supplier", "suppliers", "shop", "shops",
    "delivery",
}

# Commercial-problem hints (buyer intent even without a person-noun).
COMMERCIAL_HINTS = {
    "repair", "installation", "install", "replacement", "replace",
    "plowing", "plow", "removal", "hauling", "haul",
    "construction", "excavation",
}


def read_auth() -> str:
    v = os.environ.get("DATAFORSEO_AUTH")
    if v:
        return v.strip()
    secrets = Path.home() / ".config/secrets/secrets.env"
    if not secrets.exists():
        return ""
    for line in secrets.read_text().splitlines():
        if line.startswith("DATAFORSEO_AUTH="):
            return line.split("=", 1)[1].strip()
    return ""


def auth_headers(auth: str) -> dict:
    return {"Authorization": f"Basic {auth}", "Content-Type": "application/json"}


def is_noise(kw: str) -> bool:
    k = kw.lower()
    return any(n in k for n in NOISE)


def has_hire_signal(kw: str) -> bool:
    k = kw.lower()
    tokens = set(k.split())
    if any(h in tokens for h in HIRE_HINTS if " " not in h):
        return True
    return any(h in k for h in HIRE_HINTS if " " in h)


def has_commercial_signal(kw: str) -> bool:
    k = kw.lower()
    return any(h in k for h in COMMERCIAL_HINTS)


def peak_month(monthly: list[dict] | None):
    if not monthly:
        return None
    vols = [m.get("search_volume") or 0 for m in monthly]
    if sum(vols) == 0:
        return None
    return MONTH_NAMES[max(monthly, key=lambda m: m.get("search_volume") or 0)["month"]]


def winter_share(monthly: list[dict] | None) -> float | None:
    if not monthly:
        return None
    total = sum((m.get("search_volume") or 0) for m in monthly)
    if not total:
        return None
    winter = sum((m.get("search_volume") or 0) for m in monthly if m.get("month") in WINTER_MONTHS)
    return round(winter / total, 2)


def sparkline(monthly: list[dict] | None) -> str:
    if not monthly:
        return ""
    blocks = " ▁▂▃▄▅▆▇█"
    by_month = {m.get("month"): (m.get("search_volume") or 0) for m in monthly}
    vols = [by_month.get(m, 0) for m in range(1, 13)]
    peak = max(vols) or 1
    return "".join(blocks[min(8, round(v / peak * 8))] for v in vols)


def pull(auth: str, seeds: list[str], *, location_code: int | None,
         location_name: str | None) -> tuple[list[dict], dict]:
    # DataForSEO rejects the payload with "Invalid Field: 'location_name'" when
    # BOTH location_code and location_name are set. Send exactly one; code wins.
    payload_row: dict = {
        "keywords": seeds,
        "language_name": "English",
        "search_partners": False,
        "sort_by": "search_volume",
    }
    if location_code is not None:
        payload_row["location_code"] = location_code
    elif location_name is not None:
        payload_row["location_name"] = location_name

    r = requests.post(
        KEYWORDS_FOR_KEYWORDS,
        json=[payload_row],
        headers=auth_headers(auth),
        timeout=180,
    )
    r.raise_for_status()
    body = r.json()
    tasks = body.get("tasks") or []
    if not tasks or tasks[0].get("status_code") != 20000:
        msg = tasks[0].get("status_message") if tasks else "no tasks"
        print(f"  ! task error: {msg}", file=sys.stderr)
        return [], body
    return tasks[0].get("result") or [], body


def pull_lane(auth: str, lane: str, seeds: list[str], *, location_code: int | None,
              location_name: str | None, fallback_name: str | None = None):
    """
    Try location_code first; if the task returns empty result or an error and a
    fallback name is provided, retry with location_name only.
    """
    print(f"... expanding {len(seeds)} seeds for lane '{lane}' @ "
          f"code={location_code} name={location_name!r}", file=sys.stderr)

    result, raw = pull(auth, seeds, location_code=location_code, location_name=location_name)

    if not result and fallback_name:
        print(f"  ! empty result; retrying with fallback name {fallback_name!r}",
              file=sys.stderr)
        result, raw = pull(auth, seeds, location_code=None, location_name=fallback_name)

    rows: list[dict] = []
    for item in result:
        kw = item.get("keyword")
        if not kw or is_noise(kw):
            continue
        monthly = item.get("monthly_searches")
        rows.append({
            "keyword": kw,
            "lane": lane,
            "volume": item.get("search_volume"),
            "cpc": item.get("cpc"),
            "competition": item.get("competition"),
            "competition_index": item.get("competition_index"),
            "low_top_bid": item.get("low_top_of_page_bid"),
            "high_top_bid": item.get("high_top_of_page_bid"),
            "peak_month": peak_month(monthly),
            "winter_share": winter_share(monthly),
            "monthly_searches": monthly,
        })
    return rows, raw


def classify(row: dict) -> str:
    """AD | ORGANIC | SKIP"""
    vol = row.get("volume") or 0
    cpc = row.get("cpc") or 0
    kw = (row.get("keyword") or "").lower()

    # AD candidate: commercial pricing + real volume + intent signal
    if vol >= 100 and cpc >= 5.0 and (has_hire_signal(kw) or has_commercial_signal(kw)):
        return "AD"
    # Also flag: super-high CPC (>= $10) with any volume — buyer intent priced
    if vol >= 50 and cpc >= 10.0:
        return "AD"
    if vol >= 30:
        return "ORGANIC"
    return "SKIP"


def fmt_cpc(v) -> str:
    return f"${v:.2f}" if isinstance(v, (int, float)) else "-"


def fmt_int(v) -> str:
    return f"{int(v)}" if isinstance(v, (int, float)) else "-"


def emit_markdown(batches: list[dict]) -> str:
    lines: list[str] = []
    lines.append("# Winter 2026 expansion — keyword pull")
    lines.append("")
    lines.append(f"Date: {date.today().isoformat()}")
    lines.append(f"Endpoint: `{KEYWORDS_FOR_KEYWORDS}`")
    lines.append("")
    lines.append("Tag legend:")
    lines.append("- **AD** = ad candidate (vol >= 100 & CPC >= $5 with hire/commercial signal, "
                 "or vol >= 50 & CPC >= $10).")
    lines.append("- **ORG** = organic SEO target (vol >= 30, not an ad candidate).")
    lines.append("- SKIP rows are omitted from the tables (kept in the raw JSON).")
    lines.append("")
    lines.append("Note: `stump removal` seed included for research only. Memory says "
                 "AccuRite does NOT target stump keywords.")
    lines.append("")

    for batch in batches:
        lines.append(f"## Batch: {batch['label']}")
        lines.append("")
        lines.append(f"Location: `{batch['location']}`")
        lines.append("")

        for lane, rows in batch["lanes"].items():
            kept = [r for r in rows if classify(r) != "SKIP"]
            kept.sort(key=lambda r: (r["volume"] or 0), reverse=True)

            lines.append(f"### Lane: `{lane}` — {len(kept)} kept "
                         f"(of {len(rows)} returned)")
            lines.append("")
            if not kept:
                lines.append("_(nothing above research floor)_")
                lines.append("")
                continue

            lines.append("| Tag | Keyword | Vol/mo | CPC | Comp | Peak | Winter% | Trend Jan→Dec |")
            lines.append("|-----|---------|-------:|----:|-----:|:----:|--------:|:--------------|")
            for r in kept[:40]:
                tag = classify(r)
                comp = str(r.get("competition") or "-")
                winter = f"{int((r['winter_share'] or 0) * 100)}%" if r.get("winter_share") else "-"
                spark = sparkline(r.get("monthly_searches"))
                lines.append(
                    f"| {tag} | {r['keyword']} | {fmt_int(r['volume'])} | "
                    f"{fmt_cpc(r['cpc'])} | {comp} | {r.get('peak_month') or '-'} | "
                    f"{winter} | `{spark}` |"
                )
            lines.append("")

    return "\n".join(lines)


def main() -> int:
    auth = read_auth()
    if not auth:
        print("ERROR: DATAFORSEO_AUTH not set and not found in ~/.config/secrets/secrets.env",
              file=sys.stderr)
        return 1

    here = Path(__file__).parent
    today = date.today().isoformat()

    batches = [
        {
            "label": "LOCAL — Salt Lake City / Ogden-Clearfield metro",
            "location_code": LOCAL_LOCATION_CODE,
            "location_name": LOCAL_LOCATION_NAME,
            "fallback_name": LOCAL_FALLBACK_NAME,
            "lanes_config": LOCAL_LANES,
            "location": f"code={LOCAL_LOCATION_CODE} ({LOCAL_LOCATION_NAME})",
            "lanes": {},
            "raw": {},
        },
        {
            "label": "REGIONAL — State of Utah",
            "location_code": REGIONAL_LOCATION_CODE,
            "location_name": REGIONAL_LOCATION_NAME,
            "fallback_name": None,
            "lanes_config": REGIONAL_LANES,
            "location": f"code={REGIONAL_LOCATION_CODE} ({REGIONAL_LOCATION_NAME})",
            "lanes": {},
            "raw": {},
        },
    ]

    for batch in batches:
        print(f"\n== BATCH: {batch['label']} ==", file=sys.stderr)
        for lane, seeds in batch["lanes_config"].items():
            rows, raw = pull_lane(
                auth, lane, seeds,
                location_code=batch["location_code"],
                location_name=batch["location_name"],
                fallback_name=batch["fallback_name"],
            )
            batch["lanes"][lane] = rows
            batch["raw"][lane] = raw

    # Write raw JSON dump
    raw_out = here / f"{today}_winter_expansion_raw.json"
    raw_payload = {
        "date": today,
        "endpoint": KEYWORDS_FOR_KEYWORDS,
        "batches": [
            {
                "label": b["label"],
                "location_code": b["location_code"],
                "location_name": b["location_name"],
                "fallback_name": b["fallback_name"],
                "seeds_by_lane": b["lanes_config"],
                "rows_by_lane": b["lanes"],
                "raw_response_by_lane": b["raw"],
            }
            for b in batches
        ],
    }
    raw_out.write_text(json.dumps(raw_payload, indent=2))
    print(f"\nWrote raw: {raw_out}", file=sys.stderr)

    # Emit markdown to a sibling file and to stdout
    md = emit_markdown([
        {"label": b["label"], "location": b["location"], "lanes": b["lanes"]}
        for b in batches
    ])
    md_out = here / f"{today}_winter_expansion_report.md"
    md_out.write_text(md)
    print(f"Wrote report: {md_out}", file=sys.stderr)

    print("\n" + md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
