# Monthly SEO Report for AccuRite — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate a branded PDF SEO report for AccuRite Excavation on the 1st of each month and attach it to a Teamwork task assigned to Ross for review.

**Architecture:** A scheduled Claude routine (via `/schedule`) fires monthly. It orchestrates data pulls via existing MCPs (GSC, Google Drive for the leads Sheet, Teamwork) plus a small Python helper for the parts MCPs can't do (Google Business Profile Performance API, PDF rendering, git-log work-shipped section). The HTML→PDF template lives alongside the helper so branding can be edited by hand.

**Tech Stack:** Python 3.11+, `google-api-python-client` (Business Profile Performance API), `jinja2` (HTML template), `weasyprint` (HTML→PDF), existing MCPs for GSC / Drive / Teamwork.

**Code home:** `/Users/rosswalker/projects/3sm_code/monthly-reports/accurite/` (matches the `weekly-audit/` pattern — light scaffolding, Claude routine does the orchestration).

---

## Sections in the final PDF, in order

1. **Leads this month** — count for the reporting month, MoM change, 6-month sparkline. Source: Google Sheet, col B = "AccuRite Excavation".
2. **Phone calls & direction requests from Google** — totals + MoM. Source: GBP Performance API.
3. **Search visibility** — total clicks, impressions, avg position, avg CTR; MoM deltas. Source: GSC.
4. **Keyword movement** — top 10 risers (positions 4–20 with biggest position gain), top queries by impressions, new queries the site started ranking for this month. Source: GSC.
5. **Top pages & queries** — top 10 landing pages by clicks with the 2–3 queries driving each. Source: GSC.
6. **What we shipped this month** — 3–6 bullets pulled from `git log` on this repo, filtered to exclude memory-system/chore commits.

---

## Task 1: GBP API access application

**Files:**
- Create: `/Users/rosswalker/projects/3sm_code/monthly-reports/accurite/README.md` (tracks state of this app)

- [ ] **Step 1: Draft the use-case text for Ross to paste into Google's Business Profile APIs access form**

Use-case text to provide Ross:

> AccuRite Excavation is a single-location excavation contractor in Salt Lake City, UT. As their marketing operator I generate a monthly internal performance report that combines Search Console data with Business Profile performance metrics (calls, direction requests, profile views). The report is delivered to the business owner only — no third-party redistribution. We need read-only access to the Business Profile Performance API (`performance.locations.fetchMultiDailyMetricsTimeSeries`) for the single managed location.

- [ ] **Step 2: Ross submits the form**

Form URL: `https://support.google.com/business/contact/api_default` (the current form may have moved — search "Business Profile APIs access form" if dead). Signed in as `ross@rossjwalker.com`. Project = existing GSC GCP project (reuse).

- [ ] **Step 3: Record submission date + status in `README.md`**

Schema:
```markdown
# Monthly SEO Report — AccuRite

## GBP API access
- Form submitted: YYYY-MM-DD
- GCP project: <project-id>
- Status: pending | approved | denied
- Approval date: —
```

Wait for Google. Continue plan with GBP stubbed (Task 4).

---

## Task 2: Repo scaffolding

**Files:**
- Create: `/Users/rosswalker/projects/3sm_code/monthly-reports/accurite/pyproject.toml`
- Create: `/Users/rosswalker/projects/3sm_code/monthly-reports/accurite/.gitignore`
- Create: `/Users/rosswalker/projects/3sm_code/monthly-reports/accurite/src/accurite_report/__init__.py`
- Create: `/Users/rosswalker/projects/3sm_code/monthly-reports/accurite/src/accurite_report/main.py`

- [ ] **Step 1: Write `pyproject.toml`**

```toml
[project]
name = "accurite-monthly-report"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
  "jinja2>=3.1",
  "weasyprint>=62",
  "google-api-python-client>=2.120",
  "google-auth>=2.28",
  "google-auth-oauthlib>=1.2",
  "python-dateutil>=2.9",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
```

- [ ] **Step 2: Write `.gitignore`**

```
__pycache__/
*.pyc
.venv/
output/
secrets/
*.pdf
```

- [ ] **Step 3: Stub `main.py` with the orchestration shell**

```python
"""Monthly SEO report generator for AccuRite Excavation.

Invoked by the scheduled Claude routine. The routine itself handles the
data pulls that go through MCPs (Sheets, GSC, Teamwork). This script
handles the parts MCPs can't: GBP API, git log, PDF rendering.

Entry point: `python -m accurite_report.main --month YYYY-MM --data data.json`
where data.json is written by the Claude routine before invocation.
"""
import argparse, json, sys
from pathlib import Path

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--month", required=True, help="Reporting month, YYYY-MM")
    p.add_argument("--data", required=True, type=Path, help="JSON file with leads + GSC data from MCPs")
    p.add_argument("--output", required=True, type=Path, help="Output PDF path")
    args = p.parse_args()
    data = json.loads(args.data.read_text())
    # TODO Task 3-6: enrich `data` with GBP + git-log, render PDF
    print(f"stub: would render report for {args.month} to {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Commit**

```bash
git -C /Users/rosswalker/projects/3sm_code add monthly-reports/accurite
git -C /Users/rosswalker/projects/3sm_code commit -m "feat(accurite-report): scaffold monthly SEO report pipeline"
```

---

## Task 3: Git-log "work shipped" extractor

**Files:**
- Create: `/Users/rosswalker/projects/3sm_code/monthly-reports/accurite/src/accurite_report/work_shipped.py`
- Create: `/Users/rosswalker/projects/3sm_code/monthly-reports/accurite/tests/test_work_shipped.py`

- [ ] **Step 1: Write failing test**

```python
# tests/test_work_shipped.py
from accurite_report.work_shipped import is_meaningful_commit

def test_excludes_memory_commits():
    assert not is_meaningful_commit("chore(memory): rotate daily note")
    assert not is_meaningful_commit("fix(memory): adopt SessionEnd-failure mitigations")

def test_includes_seo_work():
    assert is_meaningful_commit("Homepage CTR: rewrite title + meta to better match service-query intent")
    assert is_meaningful_commit("Fix 2 GSC 404s: /services/grading-and-site-prep")

def test_excludes_pure_chores():
    assert not is_meaningful_commit("chore: bump dependencies")
    assert not is_meaningful_commit("docs: update README")
```

- [ ] **Step 2: Run, confirm failure**

```bash
cd /Users/rosswalker/projects/3sm_code/monthly-reports/accurite && pytest tests/test_work_shipped.py -v
```

Expected: ImportError.

- [ ] **Step 3: Implement**

```python
# src/accurite_report/work_shipped.py
import subprocess
from datetime import date
from pathlib import Path

EXCLUDE_PREFIXES = ("chore(memory)", "fix(memory)", "chore:", "docs:")

def is_meaningful_commit(subject: str) -> bool:
    return not any(subject.lower().startswith(p) for p in EXCLUDE_PREFIXES)

def list_shipped(repo: Path, since: date, until: date) -> list[str]:
    out = subprocess.check_output(
        ["git", "-C", str(repo), "log",
         f"--since={since.isoformat()}", f"--until={until.isoformat()}",
         "--pretty=format:%s", "--no-merges"],
        text=True,
    )
    return [line for line in out.splitlines() if is_meaningful_commit(line)]
```

- [ ] **Step 4: Run, confirm pass**

```bash
pytest tests/test_work_shipped.py -v
```

Expected: 3 passed.

- [ ] **Step 5: Commit**

```bash
git -C /Users/rosswalker/projects/3sm_code add monthly-reports/accurite/src monthly-reports/accurite/tests
git -C /Users/rosswalker/projects/3sm_code commit -m "feat(accurite-report): extract meaningful commits for work-shipped section"
```

---

## Task 4: GBP Performance API client (with stub fallback)

**Files:**
- Create: `/Users/rosswalker/projects/3sm_code/monthly-reports/accurite/src/accurite_report/gbp.py`
- Create: `/Users/rosswalker/projects/3sm_code/monthly-reports/accurite/tests/test_gbp.py`
- Reuse: OAuth credentials path from the existing GSC MCP — confirm by reading `/Users/rosswalker/projects/3sm_code/mcp-servers/gsc/gsc_client.py` and matching the same client-secret/token pattern.

- [ ] **Step 1: Confirm OAuth client pattern from GSC MCP**

Read `gsc_client.py` and note: (a) where the client secret lives, (b) where the refresh token is cached, (c) the scope-expansion pattern. The new GBP client must reuse the same GCP project but will need an additional scope (`https://www.googleapis.com/auth/business.manage`) and a separate token cache (different scopes = different token).

- [ ] **Step 2: Implement `gbp.py` with `fetch_monthly_metrics()` and a stub mode**

```python
# src/accurite_report/gbp.py
import os
from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class GbpMetrics:
    calls: int
    direction_requests: int
    website_clicks: int
    profile_views: int
    is_stub: bool

STUB = GbpMetrics(calls=0, direction_requests=0, website_clicks=0, profile_views=0, is_stub=True)

def fetch_monthly_metrics(location_id: str, month_start: date, month_end: date) -> GbpMetrics:
    """Real call when ACCURITE_GBP_ENABLED=1, otherwise returns stub.
    Real implementation pulls the daily metric time series and sums:
      CALL_CLICKS, BUSINESS_DIRECTION_REQUESTS, WEBSITE_CLICKS, BUSINESS_IMPRESSIONS_*
    """
    if os.environ.get("ACCURITE_GBP_ENABLED") != "1":
        return STUB

    # Real path — enabled after Google approves API access (Task 1).
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    creds = Credentials.from_authorized_user_file(
        os.path.expanduser("~/.config/accurite-report/gbp_token.json"),
        scopes=["https://www.googleapis.com/auth/business.manage"],
    )
    svc = build("businessprofileperformance", "v1", credentials=creds)
    metric_names = [
        "CALL_CLICKS", "BUSINESS_DIRECTION_REQUESTS", "WEBSITE_CLICKS",
        "BUSINESS_IMPRESSIONS_DESKTOP_MAPS", "BUSINESS_IMPRESSIONS_DESKTOP_SEARCH",
        "BUSINESS_IMPRESSIONS_MOBILE_MAPS",  "BUSINESS_IMPRESSIONS_MOBILE_SEARCH",
    ]
    req = svc.locations().fetchMultiDailyMetricsTimeSeries(
        location=f"locations/{location_id}",
        dailyMetrics=metric_names,
        dailyRange_startDate_year=month_start.year,
        dailyRange_startDate_month=month_start.month,
        dailyRange_startDate_day=month_start.day,
        dailyRange_endDate_year=month_end.year,
        dailyRange_endDate_month=month_end.month,
        dailyRange_endDate_day=month_end.day,
    )
    resp = req.execute()
    totals = _sum_daily(resp)
    return GbpMetrics(
        calls=totals.get("CALL_CLICKS", 0),
        direction_requests=totals.get("BUSINESS_DIRECTION_REQUESTS", 0),
        website_clicks=totals.get("WEBSITE_CLICKS", 0),
        profile_views=sum(totals.get(k, 0) for k in metric_names if k.startswith("BUSINESS_IMPRESSIONS_")),
        is_stub=False,
    )

def _sum_daily(resp: dict) -> dict[str, int]:
    out: dict[str, int] = {}
    for series in resp.get("multiDailyMetricTimeSeries", []):
        for tv in series.get("dailyMetricTimeSeries", []):
            name = tv.get("dailyMetric", "")
            total = sum(int(v.get("value", 0)) for v in tv.get("timeSeries", {}).get("datedValues", []))
            out[name] = out.get(name, 0) + total
    return out
```

- [ ] **Step 3: Write tests covering stub-mode + parse logic**

```python
# tests/test_gbp.py
from accurite_report.gbp import fetch_monthly_metrics, _sum_daily, STUB
from datetime import date

def test_stub_when_disabled(monkeypatch):
    monkeypatch.delenv("ACCURITE_GBP_ENABLED", raising=False)
    m = fetch_monthly_metrics("123", date(2026,4,1), date(2026,4,30))
    assert m.is_stub
    assert m == STUB

def test_sum_daily_aggregates_per_metric():
    resp = {"multiDailyMetricTimeSeries": [{
        "dailyMetricTimeSeries": [{
            "dailyMetric": "CALL_CLICKS",
            "timeSeries": {"datedValues": [{"value": "3"}, {"value": "5"}]},
        }],
    }]}
    assert _sum_daily(resp) == {"CALL_CLICKS": 8}
```

- [ ] **Step 4: Run tests, confirm pass**

```bash
pytest tests/test_gbp.py -v
```

- [ ] **Step 5: Commit**

```bash
git -C /Users/rosswalker/projects/3sm_code add monthly-reports/accurite
git -C /Users/rosswalker/projects/3sm_code commit -m "feat(accurite-report): GBP performance client with stub fallback"
```

---

## Task 5: HTML template + PDF rendering

**Files:**
- Create: `/Users/rosswalker/projects/3sm_code/monthly-reports/accurite/src/accurite_report/templates/report.html.j2`
- Create: `/Users/rosswalker/projects/3sm_code/monthly-reports/accurite/src/accurite_report/templates/report.css`
- Create: `/Users/rosswalker/projects/3sm_code/monthly-reports/accurite/src/accurite_report/render.py`
- Create: `/Users/rosswalker/projects/3sm_code/monthly-reports/accurite/src/accurite_report/templates/assets/logo.svg` (copied from accurite repo `src/components/` or `public/`)
- Create: `/Users/rosswalker/projects/3sm_code/monthly-reports/accurite/tests/test_render.py`

- [ ] **Step 1: Source brand assets**

Read `/Users/rosswalker/projects/accurite-excavation/src/styles/` and `astro.config.mjs` / Tailwind config to extract the primary color palette. Copy the AccuRite logo from the accurite repo (likely `src/assets/` or `public/`). Bake colors as CSS variables in `report.css`.

- [ ] **Step 2: Write the Jinja template skeleton**

```html
<!-- templates/report.html.j2 -->
<!doctype html>
<html><head><meta charset="utf-8">
<link rel="stylesheet" href="report.css">
<title>AccuRite SEO Report — {{ month_label }}</title>
</head><body>

<header class="cover">
  <img src="assets/logo.svg" class="logo">
  <h1>SEO Performance Report</h1>
  <h2>{{ month_label }}</h2>
</header>

<section class="leads">
  <h2>Leads this month</h2>
  <div class="big-number">{{ leads.count }}</div>
  <div class="delta {{ leads.mom_class }}">{{ leads.mom_pct }} vs prior month</div>
  <!-- 6-month sparkline as inline SVG, rendered server-side -->
  {{ leads.sparkline_svg | safe }}
</section>

<section class="gbp">
  <h2>Calls & directions from Google</h2>
  {% if gbp.is_stub %}<p class="stub-notice">GBP data unavailable this month (API access pending).</p>
  {% else %}
  <table>
    <tr><th>Phone calls</th><td>{{ gbp.calls }}</td><td class="delta {{ gbp.calls_mom_class }}">{{ gbp.calls_mom_pct }}</td></tr>
    <tr><th>Direction requests</th><td>{{ gbp.direction_requests }}</td><td class="delta {{ gbp.dir_mom_class }}">{{ gbp.dir_mom_pct }}</td></tr>
    <tr><th>Profile views</th><td>{{ gbp.profile_views }}</td><td class="delta {{ gbp.views_mom_class }}">{{ gbp.views_mom_pct }}</td></tr>
  </table>
  {% endif %}
</section>

<section class="visibility">
  <h2>Search visibility</h2>
  <table>
    <tr><th>Clicks</th><td>{{ gsc.clicks }}</td><td class="delta {{ gsc.clicks_mom_class }}">{{ gsc.clicks_mom_pct }}</td></tr>
    <tr><th>Impressions</th><td>{{ gsc.impressions }}</td><td class="delta {{ gsc.imps_mom_class }}">{{ gsc.imps_mom_pct }}</td></tr>
    <tr><th>Avg position</th><td>{{ gsc.avg_position }}</td><td class="delta {{ gsc.pos_mom_class }}">{{ gsc.pos_mom_delta }}</td></tr>
    <tr><th>Avg CTR</th><td>{{ gsc.avg_ctr }}%</td><td class="delta {{ gsc.ctr_mom_class }}">{{ gsc.ctr_mom_pct }}</td></tr>
  </table>
</section>

<section class="movers">
  <h2>Keywords moving up</h2>
  <table>
    <thead><tr><th>Query</th><th>Was</th><th>Now</th><th>Gain</th><th>Impressions</th></tr></thead>
    <tbody>
    {% for k in gsc.top_movers %}
      <tr><td>{{ k.query }}</td><td>{{ k.prev_pos }}</td><td>{{ k.curr_pos }}</td><td class="gain">+{{ k.gain }}</td><td>{{ k.impressions }}</td></tr>
    {% endfor %}
    </tbody>
  </table>
</section>

<section class="pages">
  <h2>Top landing pages</h2>
  {% for page in gsc.top_pages %}
    <div class="page-card">
      <a href="{{ page.url }}">{{ page.url }}</a>
      <span class="clicks">{{ page.clicks }} clicks</span>
      <ul>{% for q in page.top_queries %}<li>{{ q }}</li>{% endfor %}</ul>
    </div>
  {% endfor %}
</section>

<section class="shipped">
  <h2>What we shipped this month</h2>
  <ul>{% for line in work_shipped %}<li>{{ line }}</li>{% endfor %}</ul>
</section>

<footer>Generated {{ generated_at }} · AccuRite Excavation · Prepared by Ross Walker</footer>
</body></html>
```

- [ ] **Step 3: Write `report.css` with brand colors**

Use AccuRite's actual brand palette (extracted in Step 1). Big-number style for leads count, color-coded `.delta.up` (green) / `.delta.down` (red), page-card hairline borders, print-friendly margins.

- [ ] **Step 4: Implement `render.py`**

```python
# src/accurite_report/render.py
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import HTML

TEMPLATE_DIR = Path(__file__).parent / "templates"

def render_pdf(context: dict, output: Path) -> Path:
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), autoescape=select_autoescape(["html"]))
    html = env.get_template("report.html.j2").render(**context)
    HTML(string=html, base_url=str(TEMPLATE_DIR)).write_pdf(output)
    return output
```

- [ ] **Step 5: Write smoke test with fixture data**

```python
# tests/test_render.py
from pathlib import Path
from accurite_report.render import render_pdf

def test_renders_pdf(tmp_path):
    ctx = {
        "month_label": "April 2026",
        "leads": {"count": 18, "mom_pct": "+38%", "mom_class": "up", "sparkline_svg": "<svg/>"},
        "gbp": {"is_stub": True},
        "gsc": {"clicks": 412, "impressions": 18230, "avg_position": 11.4, "avg_ctr": 2.3,
                "clicks_mom_pct": "+12%", "clicks_mom_class": "up",
                "imps_mom_pct": "+5%", "imps_mom_class": "up",
                "pos_mom_delta": "-0.4", "pos_mom_class": "up",
                "ctr_mom_pct": "+0.1pp", "ctr_mom_class": "up",
                "top_movers": [], "top_pages": []},
        "work_shipped": ["Homepage CTR rewrite", "Fixed 2 GSC 404s"],
        "generated_at": "2026-05-01",
    }
    pdf = render_pdf(ctx, tmp_path / "report.pdf")
    assert pdf.exists() and pdf.stat().st_size > 5000  # >5KB = real PDF
```

- [ ] **Step 6: Run tests**

```bash
pytest tests/test_render.py -v
```

- [ ] **Step 7: Eyeball the rendered PDF once**

```bash
python -c "from tests.test_render import test_renders_pdf; from pathlib import Path; import tempfile; td = Path(tempfile.mkdtemp()); test_renders_pdf.__wrapped__(td) if hasattr(test_renders_pdf,'__wrapped__') else None"
# or simpler:
pytest tests/test_render.py -v -s --keep-output
open /tmp/.../report.pdf
```

Visually check: logo loads, colors look right, no broken sections, page breaks make sense.

- [ ] **Step 8: Commit**

```bash
git -C /Users/rosswalker/projects/3sm_code add monthly-reports/accurite
git -C /Users/rosswalker/projects/3sm_code commit -m "feat(accurite-report): HTML template + PDF renderer with AccuRite branding"
```

---

## Task 6: Wire-up — main entry point that produces a PDF

**Files:**
- Modify: `/Users/rosswalker/projects/3sm_code/monthly-reports/accurite/src/accurite_report/main.py`
- Create: `/Users/rosswalker/projects/3sm_code/monthly-reports/accurite/src/accurite_report/transform.py` (computes MoM deltas, classes, sparkline)
- Create: `/Users/rosswalker/projects/3sm_code/monthly-reports/accurite/tests/test_transform.py`

- [ ] **Step 1: Define the `data.json` contract**

The Claude routine writes this file before invoking the script. Exact schema:

```json
{
  "month": "2026-04",
  "leads": {
    "current_month_count": 18,
    "prior_month_count": 13,
    "trailing_6_months": [{"month": "2025-11", "count": 6}, ...]
  },
  "gsc": {
    "current":  {"clicks": 412, "impressions": 18230, "position": 11.4, "ctr": 0.023},
    "previous": {"clicks": 368, "impressions": 17350, "position": 11.8, "ctr": 0.022},
    "top_movers": [{"query":"...","prev_pos":12.3,"curr_pos":6.1,"impressions":420}, ...],
    "top_pages":  [{"url":"...","clicks":54,"top_queries":["...","..."]}, ...]
  },
  "gbp_location_id": "12345..."
}
```

- [ ] **Step 2: Write `transform.py` with pure functions for delta + sparkline**

```python
# src/accurite_report/transform.py
def pct_delta(curr: float, prev: float) -> tuple[str, str]:
    if prev == 0: return ("n/a", "flat")
    pct = (curr - prev) / prev * 100
    cls = "up" if pct > 0 else "down" if pct < 0 else "flat"
    return (f"{pct:+.0f}%", cls)

def position_delta(curr: float, prev: float) -> tuple[str, str]:
    delta = curr - prev  # lower is better
    cls = "up" if delta < 0 else "down" if delta > 0 else "flat"
    return (f"{delta:+.1f}", cls)

def sparkline_svg(values: list[int], width: int = 200, height: int = 40) -> str:
    if not values: return "<svg/>"
    lo, hi = min(values), max(values)
    rng = max(hi - lo, 1)
    pts = " ".join(
        f"{int(i*width/max(len(values)-1,1))},{int(height - (v-lo)*height/rng)}"
        for i, v in enumerate(values)
    )
    return f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">\
<polyline fill="none" stroke="currentColor" stroke-width="2" points="{pts}"/></svg>'
```

- [ ] **Step 3: Tests for transform**

```python
# tests/test_transform.py
from accurite_report.transform import pct_delta, position_delta, sparkline_svg

def test_pct_delta_up():
    assert pct_delta(120, 100) == ("+20%", "up")

def test_pct_delta_zero_prev_is_na():
    assert pct_delta(5, 0) == ("n/a", "flat")

def test_position_delta_lower_is_up():
    assert position_delta(8.0, 10.0) == ("-2.0", "up")

def test_sparkline_emits_polyline():
    s = sparkline_svg([1,2,3,4,5])
    assert "<polyline" in s and "points=" in s
```

- [ ] **Step 4: Replace stubbed `main.py` with full wiring**

```python
# src/accurite_report/main.py
import argparse, json, sys
from datetime import date, datetime
from pathlib import Path
from dateutil.relativedelta import relativedelta
from .gbp import fetch_monthly_metrics
from .work_shipped import list_shipped
from .transform import pct_delta, position_delta, sparkline_svg
from .render import render_pdf

ACCURITE_REPO = Path("/Users/rosswalker/projects/accurite-excavation")

def build_context(month: str, data: dict) -> dict:
    year, mon = map(int, month.split("-"))
    m_start = date(year, mon, 1)
    m_end = (m_start + relativedelta(months=1)) - relativedelta(days=1)
    month_label = m_start.strftime("%B %Y")

    leads_mom_pct, leads_mom_class = pct_delta(
        data["leads"]["current_month_count"], data["leads"]["prior_month_count"])
    trailing = [d["count"] for d in data["leads"]["trailing_6_months"]]

    gsc_c, gsc_p = data["gsc"]["current"], data["gsc"]["previous"]
    clicks_pct, clicks_cls = pct_delta(gsc_c["clicks"], gsc_p["clicks"])
    imps_pct, imps_cls = pct_delta(gsc_c["impressions"], gsc_p["impressions"])
    pos_d, pos_cls = position_delta(gsc_c["position"], gsc_p["position"])
    ctr_pct, ctr_cls = pct_delta(gsc_c["ctr"], gsc_p["ctr"])

    gbp = fetch_monthly_metrics(data["gbp_location_id"], m_start, m_end)
    # MoM for GBP requires prior-month pull too — fetched same way in real mode
    # For stub, all deltas are blanked
    gbp_prev = fetch_monthly_metrics(data["gbp_location_id"],
                                     m_start - relativedelta(months=1),
                                     m_start - relativedelta(days=1))
    calls_pct, calls_cls = (("", "flat") if gbp.is_stub else pct_delta(gbp.calls, gbp_prev.calls))
    dir_pct,   dir_cls   = (("", "flat") if gbp.is_stub else pct_delta(gbp.direction_requests, gbp_prev.direction_requests))
    views_pct, views_cls = (("", "flat") if gbp.is_stub else pct_delta(gbp.profile_views, gbp_prev.profile_views))

    return {
        "month_label": month_label,
        "leads": {
            "count": data["leads"]["current_month_count"],
            "mom_pct": leads_mom_pct, "mom_class": leads_mom_class,
            "sparkline_svg": sparkline_svg(trailing),
        },
        "gbp": {
            "is_stub": gbp.is_stub,
            "calls": gbp.calls, "calls_mom_pct": calls_pct, "calls_mom_class": calls_cls,
            "direction_requests": gbp.direction_requests, "dir_mom_pct": dir_pct, "dir_mom_class": dir_cls,
            "profile_views": gbp.profile_views, "views_mom_pct": views_pct, "views_mom_class": views_cls,
        },
        "gsc": {
            "clicks": gsc_c["clicks"], "clicks_mom_pct": clicks_pct, "clicks_mom_class": clicks_cls,
            "impressions": gsc_c["impressions"], "imps_mom_pct": imps_pct, "imps_mom_class": imps_cls,
            "avg_position": round(gsc_c["position"], 1), "pos_mom_delta": pos_d, "pos_mom_class": pos_cls,
            "avg_ctr": round(gsc_c["ctr"] * 100, 1), "ctr_mom_pct": ctr_pct, "ctr_mom_class": ctr_cls,
            "top_movers": [{**k, "gain": round(k["prev_pos"] - k["curr_pos"], 1)} for k in data["gsc"]["top_movers"]],
            "top_pages": data["gsc"]["top_pages"],
        },
        "work_shipped": list_shipped(ACCURITE_REPO, m_start, m_end + relativedelta(days=1)),
        "generated_at": datetime.now().strftime("%Y-%m-%d"),
    }

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--month", required=True)
    p.add_argument("--data", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    args = p.parse_args()
    data = json.loads(args.data.read_text())
    ctx = build_context(args.month, data)
    render_pdf(ctx, args.output)
    print(f"wrote {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 5: End-to-end smoke test with a hand-written `data.json`**

```bash
cd /Users/rosswalker/projects/3sm_code/monthly-reports/accurite
cat > /tmp/test-data.json <<'EOF'
{"month":"2026-04",
 "leads":{"current_month_count":18,"prior_month_count":13,"trailing_6_months":[
   {"month":"2025-11","count":6},{"month":"2025-12","count":8},
   {"month":"2026-01","count":11},{"month":"2026-02","count":14},
   {"month":"2026-03","count":13},{"month":"2026-04","count":18}]},
 "gsc":{"current":{"clicks":412,"impressions":18230,"position":11.4,"ctr":0.023},
        "previous":{"clicks":368,"impressions":17350,"position":11.8,"ctr":0.022},
        "top_movers":[{"query":"excavation contractor utah","prev_pos":12.3,"curr_pos":6.1,"impressions":420}],
        "top_pages":[{"url":"https://accuriteexcavation.com/services/grading","clicks":54,"top_queries":["grading utah","site prep"]}]},
 "gbp_location_id":"placeholder"}
EOF
python -m accurite_report.main --month 2026-04 --data /tmp/test-data.json --output /tmp/accurite-test.pdf
open /tmp/accurite-test.pdf
```

Confirm visually: every section renders, leads count looks prominent, work-shipped lists real April commits, no broken layout.

- [ ] **Step 6: Commit**

```bash
git -C /Users/rosswalker/projects/3sm_code add monthly-reports/accurite
git -C /Users/rosswalker/projects/3sm_code commit -m "feat(accurite-report): wire transforms + end-to-end PDF generation"
```

---

## Task 7: Monthly Claude routine — orchestration

**Files:**
- Create: `/Users/rosswalker/projects/3sm_code/monthly-reports/accurite/ROUTINE.md` (the prompt that runs monthly)

- [ ] **Step 1: Write the routine prompt**

This is the literal prompt the `/schedule` agent will execute on the 1st of each month:

```markdown
# AccuRite Monthly SEO Report — routine

Run on the 1st of the month. Generates last month's report and attaches it to a Teamwork task for Ross.

## Steps

1. Compute reporting month = (today - 1 month) as YYYY-MM. Compute month_start and month_end.

2. **Pull leads** from the Google Sheet `1MswVgpMa8UJHk5MhKfgnAMmYmNaOTtt3HAjcHFTdS8k`:
   - Read sheet via Google Drive MCP
   - Filter rows where column B == "AccuRite Excavation"
   - Count rows whose date column falls in the reporting month → `current_month_count`
   - Count rows in prior month → `prior_month_count`
   - Build `trailing_6_months` (6 months ending in reporting month)

3. **Pull GSC data** for property `sc-domain:accuriteexcavation.com` (or whichever is registered — check `/Users/rosswalker/projects/3sm_code/mcp-servers/gsc/properties.json`):
   - `gsc_performance` for reporting month: clicks, impressions, avg position, avg CTR → `current`
   - `gsc_performance` for prior month → `previous`
   - `gsc_performance` by query for reporting month + prior month; compute top 10 risers (positions between 4 and 20, biggest gain in position, min 50 impressions) → `top_movers`
   - `gsc_performance` by page for reporting month, top 10 by clicks; for each, fetch top 2-3 queries → `top_pages`

4. **Write `data.json`** to `/tmp/accurite-report-<YYYY-MM>.json` with the schema in `main.py`.

5. **Run the report**:
   ```bash
   cd /Users/rosswalker/projects/3sm_code/monthly-reports/accurite
   python -m accurite_report.main \
     --month <YYYY-MM> \
     --data /tmp/accurite-report-<YYYY-MM>.json \
     --output /tmp/accurite-seo-<YYYY-MM>.pdf
   ```

6. **Create Teamwork task** in project 628283:
   - Tasklist: find or create "AccuRite Monthly SEO Report"
   - Title: `Review SEO report — <Month Year>` (e.g. "Review SEO report — April 2026")
   - Assigned to: Ross Walker (157735)
   - Due: 3 days from today
   - No priority
   - Description: 2-sentence summary of MoM changes (leads, clicks)
   - Attach the PDF via `twprojects-create_file` then link to the task

7. **Send Telegram summary** to chat_id 1694510615: one line per metric (leads, clicks, calls if not stub), MoM %, task URL.

## Error handling

- If leads sheet unreachable: skip leads section in PDF (template handles missing data), continue.
- If GSC fails: notify via `~/.local/bin/notify`, abort — no point shipping a report without search data.
- If GBP API not yet approved: `ACCURITE_GBP_ENABLED` env var stays unset → stub mode, template shows pending notice.
- If Teamwork file upload fails: drop PDF into `~/Desktop/accurite-reports/` and create the task without attachment, mention in Telegram.
```

- [ ] **Step 2: Schedule the routine via /schedule**

```bash
# In Claude Code, invoke the schedule skill with:
# - Cron: 0 8 1 * *  (8am Denver, 1st of each month)
# - Routine: the ROUTINE.md content above
# - Name: accurite-monthly-seo-report
```

Confirm the routine is registered (`/schedule list` or equivalent).

- [ ] **Step 3: Manual first-run test (don't wait until June 1)**

Run the routine prompt manually in a Claude Code session with current data. Verify:
- PDF lands at `/tmp/accurite-seo-2026-04.pdf`
- Teamwork task created in project 628283 with PDF attached
- Telegram ping fires

Fix anything broken in the routine prompt and re-test until clean.

- [ ] **Step 4: Commit the routine file**

```bash
git -C /Users/rosswalker/projects/3sm_code add monthly-reports/accurite/ROUTINE.md
git -C /Users/rosswalker/projects/3sm_code commit -m "feat(accurite-report): monthly routine prompt"
```

---

## Task 8: Documentation + handoff

**Files:**
- Modify: `/Users/rosswalker/projects/3sm_code/monthly-reports/accurite/README.md`
- Modify: `/Users/rosswalker/projects/accurite-excavation/docs/project-brief.md` (add reference)

- [ ] **Step 1: Complete `README.md`**

Sections: what it does, where outputs go, how to regenerate manually, how to enable GBP once approved (`export ACCURITE_GBP_ENABLED=1` + token cache path), how to edit the template, how to bypass and run for an arbitrary month.

- [ ] **Step 2: Add a one-liner to accurite project-brief.md**

Under "Recurring work" or a new "Reporting" section: pointer to `/Users/rosswalker/projects/3sm_code/monthly-reports/accurite/` so future Claude sessions know it exists.

- [ ] **Step 3: Commit**

```bash
git -C /Users/rosswalker/projects/3sm_code add monthly-reports/accurite/README.md
git -C /Users/rosswalker/projects/3sm_code commit -m "docs(accurite-report): usage + manual override notes"
git -C /Users/rosswalker/projects/accurite-excavation add docs/project-brief.md
git -C /Users/rosswalker/projects/accurite-excavation commit -m "docs: pointer to monthly SEO report pipeline"
```

---

## Done criteria

- A signed PDF generated for April 2026 with real data, eyeballed by Ross.
- One Teamwork task in 628283 assigned to Ross with the PDF attached.
- Routine scheduled in `/schedule`, will fire June 1 for May data.
- GBP form submitted (Task 1) — pending Google's approval, plan continues with stub. When approval lands: set `ACCURITE_GBP_ENABLED=1`, drop in the token cache, verify next month's report includes real GBP numbers.
