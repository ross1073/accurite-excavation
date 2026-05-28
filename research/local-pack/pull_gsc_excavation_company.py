"""
GSC re-check for "excavation company" — track recovery from the May 11 slide.

Pulls daily GSC position for the query 'excavation company' (exact match)
for the last ~21 days. Baseline 2026-05-22: query had slid from organic
~1.5 down to #13 starting ~2026-05-11.

Run: GOOGLE_OAUTH_CREDS=/abs/path python pull_gsc_excavation_company.py
"""
from __future__ import annotations
import os
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path.home() / "projects/3sm_code/command-center"))

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SITE = "sc-domain:accuriteexcavation.com"
TARGET = "excavation company"
DAYS = 28


def main() -> int:
    creds_path = os.environ.get("GOOGLE_OAUTH_CREDS", "")
    if not creds_path:
        print("ERROR: GOOGLE_OAUTH_CREDS not set", file=sys.stderr)
        return 1
    creds = Credentials.from_authorized_user_file(creds_path)
    svc = build("searchconsole", "v1", credentials=creds)

    end = date.today()
    start = end - timedelta(days=DAYS)

    # Daily breakdown for the exact query
    resp = svc.searchanalytics().query(
        siteUrl=SITE,
        body={
            "startDate": start.isoformat(),
            "endDate": end.isoformat(),
            "dimensions": ["date", "query"],
            "dimensionFilterGroups": [{
                "filters": [{
                    "dimension": "query",
                    "operator": "equals",
                    "expression": TARGET,
                }],
            }],
            "rowLimit": 500,
        },
    ).execute()

    rows = resp.get("rows", [])
    if not rows:
        print(f"No GSC rows for {TARGET!r} in last {DAYS} days.")
        # Try also as contains, in case the exact phrase yields nothing
        resp2 = svc.searchanalytics().query(
            siteUrl=SITE,
            body={
                "startDate": start.isoformat(),
                "endDate": end.isoformat(),
                "dimensions": ["query"],
                "dimensionFilterGroups": [{
                    "filters": [{
                        "dimension": "query",
                        "operator": "contains",
                        "expression": "excavation company",
                    }],
                }],
                "rowLimit": 500,
            },
        ).execute()
        print(f"\nQueries containing 'excavation company' last {DAYS}d:")
        for r in resp2.get("rows", []):
            q = r["keys"][0]
            print(f"  {q:<50} imp={r['impressions']:>5}  clicks={r['clicks']:>3}  pos={r['position']:.1f}")
        return 0

    print(f"Daily GSC for {TARGET!r} — last {DAYS} days")
    print(f"{'date':<12} {'impressions':>11} {'clicks':>6} {'ctr':>6} {'position':>8}")
    print("-" * 50)
    rows.sort(key=lambda r: r["keys"][0])
    for r in rows:
        d = r["keys"][0]
        print(f"{d:<12} {r['impressions']:>11.0f} {r['clicks']:>6.0f} {r['ctr']*100:>5.1f}% {r['position']:>8.1f}")

    # Summary windows
    print("\nWindow averages:")
    by_date = {r["keys"][0]: r for r in rows}
    today_iso = date.today().isoformat()

    def window(start_d: date, end_d: date) -> tuple[float, int, int]:
        ps, imp, clk = [], 0, 0
        d = start_d
        while d <= end_d:
            iso = d.isoformat()
            if iso in by_date:
                r = by_date[iso]
                ps.append(r["position"] * r["impressions"])
                imp += r["impressions"]
                clk += r["clicks"]
            d += timedelta(days=1)
        return (sum(ps) / imp if imp else 0.0), imp, clk

    # Pre-slide window (before 2026-05-11)
    pre_pos, pre_imp, pre_clk = window(end - timedelta(days=DAYS), date(2026, 5, 10))
    # Slide window 2026-05-11 → 2026-05-22 (baseline session)
    mid_pos, mid_imp, mid_clk = window(date(2026, 5, 11), date(2026, 5, 22))
    # Post-baseline window 2026-05-23 → today
    post_pos, post_imp, post_clk = window(date(2026, 5, 23), end)

    print(f"  pre-slide   (≤2026-05-10): pos={pre_pos:.1f}  imp={pre_imp}  clicks={pre_clk}")
    print(f"  slide       (05-11→05-22): pos={mid_pos:.1f}  imp={mid_imp}  clicks={mid_clk}")
    print(f"  post-base   (05-23→today): pos={post_pos:.1f}  imp={post_imp}  clicks={post_clk}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
