"""
AccuRite vs competitors — review count / rating / velocity / recency puller.

Created 2026-06-18 to diagnose the Ogden Map-Pack slip (AccuRite #1 -> #2,
Skinner Excavating took #1). Current local-pack research says review *velocity*
(reviews this month) and *recency* (days since last review) outweigh lifetime
total for Map-Pack position — so we benchmark AccuRite against the Ogden top-3.

Steps:
  1. serp/google/maps live — enumerate excavation businesses ranking from the
     Ogden geo point, capturing title / rating / review-count / cid / place_id.
  2. business_data/google/reviews task — for AccuRite + each top competitor,
     pull recent reviews sorted newest, then compute:
       - total review count + avg rating
       - days since most recent review (recency)
       - reviews in trailing 30 / 60 / 90 days (velocity)

Run: DATAFORSEO_AUTH=... python pull_review_velocity.py
Output: prints a table and writes review-velocity-YYYY-MM-DD.json next to this file.
"""
from __future__ import annotations
import json
import os
import sys
import time
from datetime import date, datetime, timezone
from pathlib import Path

import requests

BASE = "https://api.dataforseo.com/v3"
MAPS = f"{BASE}/serp/google/maps/live/advanced"
REVIEWS_POST = f"{BASE}/business_data/google/reviews/task_post"
# Business Data review endpoints use plain task_get/{id} (no /advanced suffix,
# unlike the SERP endpoints).
REVIEWS_GET = f"{BASE}/business_data/google/reviews/task_get"

OGDEN = "41.2230,-111.9738,10"
SEED_QUERY = "excavation companies near me"

# Businesses we care about (match on lowercased title substring).
TARGETS = ["accurite", "skinner", "triple h"]
REVIEW_DEPTH = 100  # how many recent reviews to pull per business


def auth_headers(auth: str) -> dict:
    return {"Authorization": f"Basic {auth}", "Content-Type": "application/json"}


def maps_search(auth: str) -> list[dict]:
    payload = [{
        "keyword": SEED_QUERY,
        "location_coordinate": OGDEN,
        "language_name": "English",
        "depth": 20,
    }]
    r = requests.post(MAPS, json=payload, headers=auth_headers(auth), timeout=60)
    r.raise_for_status()
    data = r.json()
    tasks = data.get("tasks") or []
    if not tasks:
        return []
    result = tasks[0].get("result") or []
    if not result:
        return []
    return result[0].get("items") or []


def extract_business(item: dict) -> dict:
    rating = item.get("rating") or {}
    return {
        "title": item.get("title") or "",
        "rating_value": rating.get("value"),
        "rating_count": rating.get("votes_count"),
        "cid": item.get("cid"),
        "place_id": item.get("place_id"),
        "rank_absolute": item.get("rank_absolute"),
    }


def post_reviews_task(auth: str, biz: dict) -> str | None:
    # NOTE: the reviews endpoint wants location_name, not location_coordinate
    # (a coordinate yields a rejected task with a null id -> 404 on task_get).
    task = {
        "language_name": "English",
        "location_name": "United States",
        "sort_by": "newest",
        "depth": REVIEW_DEPTH,
    }
    if biz.get("place_id"):
        task["place_id"] = biz["place_id"]
    elif biz.get("cid"):
        task["cid"] = biz["cid"]
    else:
        return None
    r = requests.post(REVIEWS_POST, json=[task], headers=auth_headers(auth), timeout=60)
    r.raise_for_status()
    tasks = r.json().get("tasks") or []
    if not tasks:
        return None
    return tasks[0].get("id")


def get_reviews(auth: str, task_id: str, max_wait: int = 180) -> list[dict] | None:
    """Poll task_get until ready. Returns review items or None."""
    waited = 0
    while waited <= max_wait:
        r = requests.get(f"{REVIEWS_GET}/{task_id}", headers=auth_headers(auth), timeout=60)
        r.raise_for_status()
        tasks = r.json().get("tasks") or []
        if tasks:
            t = tasks[0]
            sc = t.get("status_code")
            if sc == 20000:
                result = t.get("result") or []
                if result:
                    return result[0].get("items") or []
                return []
            # 40602 = task in queue / not ready yet
        time.sleep(12)
        waited += 12
    return None


def parse_ts(ts: str | None) -> datetime | None:
    if not ts:
        return None
    # DataForSEO format e.g. "2026-05-12 14:03:21 +00:00"
    for fmt in ("%Y-%m-%d %H:%M:%S %z", "%Y-%m-%d %H:%M:%S"):
        try:
            dt = datetime.strptime(ts, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except ValueError:
            continue
    return None


def review_metrics(items: list[dict]) -> dict:
    now = datetime.now(timezone.utc)
    dates = []
    for it in items:
        dt = parse_ts(it.get("timestamp"))
        if dt:
            dates.append(dt)
    dates.sort(reverse=True)
    if not dates:
        return {"pulled": len(items), "with_dates": 0}
    most_recent = dates[0]
    days_since = (now - most_recent).days
    def within(days: int) -> int:
        return sum(1 for d in dates if (now - d).days <= days)
    return {
        "pulled": len(items),
        "with_dates": len(dates),
        "most_recent": most_recent.date().isoformat(),
        "days_since_last": days_since,
        "last_30d": within(30),
        "last_60d": within(60),
        "last_90d": within(90),
    }


def main() -> int:
    auth = os.environ.get("DATAFORSEO_AUTH", "")
    if not auth:
        print("ERROR: DATAFORSEO_AUTH not set", file=sys.stderr)
        return 1

    today = date.today().isoformat()
    print(f"... maps search {SEED_QUERY!r} @ Ogden", file=sys.stderr)
    items = maps_search(auth)
    businesses = [extract_business(it) for it in items if it.get("type") == "maps_search"]

    # Pick our targets (first match per keyword), keep maps order.
    chosen = []
    for kw in TARGETS:
        for b in businesses:
            if kw in b["title"].lower() and b not in chosen:
                chosen.append(b)
                break

    if not chosen:
        print("No target businesses found in maps results.", file=sys.stderr)
        print("Titles seen:", [b["title"] for b in businesses], file=sys.stderr)
        return 1

    results = {"date": today, "seed_query": SEED_QUERY, "geo": "Ogden", "businesses": []}

    for b in chosen:
        print(f"... reviews task for {b['title']!r}", file=sys.stderr)
        rec = dict(b)
        try:
            tid = post_reviews_task(auth, b)
            if not tid:
                rec["error"] = "no task id (missing place_id/cid)"
            else:
                items = get_reviews(auth, tid)
                if items is None:
                    rec["error"] = "reviews task timed out"
                else:
                    rec["metrics"] = review_metrics(items)
        except Exception as e:
            rec["error"] = str(e)
        results["businesses"].append(rec)

    # Table
    print(f"\nAccuRite vs competitors — review benchmark {today} (Ogden, {SEED_QUERY!r})")
    hdr = f"{'business':<38} {'rank':>4} {'rating':>6} {'count':>6} {'last_review':>12} {'d_ago':>6} {'30d':>4} {'60d':>4} {'90d':>4}"
    print(hdr)
    print("-" * len(hdr))
    for rec in results["businesses"]:
        m = rec.get("metrics") or {}
        if "error" in rec:
            print(f"{rec['title'][:38]:<38} {str(rec.get('rank_absolute') or '-'):>4} ERR {rec['error'][:40]}")
            continue
        print(f"{rec['title'][:38]:<38} "
              f"{str(rec.get('rank_absolute') or '-'):>4} "
              f"{str(rec.get('rating_value') or '-'):>6} "
              f"{str(rec.get('rating_count') or '-'):>6} "
              f"{str(m.get('most_recent') or '-'):>12} "
              f"{str(m.get('days_since_last') if m.get('days_since_last') is not None else '-'):>6} "
              f"{str(m.get('last_30d') if m.get('last_30d') is not None else '-'):>4} "
              f"{str(m.get('last_60d') if m.get('last_60d') is not None else '-'):>4} "
              f"{str(m.get('last_90d') if m.get('last_90d') is not None else '-'):>4}")

    out = Path(__file__).parent / f"review-velocity-{today}.json"
    out.write_text(json.dumps(results, indent=2))
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
