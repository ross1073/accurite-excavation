"""
Render the seasonal-demand audit to standalone HTML.

Reads the buckets built by build_intent_buckets.py (which reads the 2026-07-13
DataForSEO pull) and writes an auditable page: every keyword in every bucket, every
keyword rejected and why, so the grouping can be checked by eye rather than trusted.

Run: python render_report.py [out.html]
"""
from __future__ import annotations

import html
import sys
from pathlib import Path

from build_intent_buckets import build, SEASONS

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "seasonal-demand.html"

SERVICE_ORDER = ["sewer/water line", "excavation", "demolition", "drainage",
                 "retaining wall", "land clearing"]


def money(cpc) -> str:
    return f"${cpc:,.2f}" if isinstance(cpc, (int, float)) else "—"


def num(n) -> str:
    return f"{n:,}"


def main() -> int:
    buckets, research, rejected = build()

    season_totals = {
        s: sum(r["seasons"][s] for rows in buckets.values() for r in rows) for s in SEASONS
    }
    peak_season = max(season_totals, key=season_totals.get)

    service_rows = []
    for service in SERVICE_ORDER:
        rows = buckets.get(service, [])
        if not rows:
            continue
        totals = {s: sum(r["seasons"][s] for r in rows) for s in SEASONS}
        service_rows.append((service, totals, rows))
    service_rows.sort(key=lambda x: x[1]["Winter"], reverse=True)

    parts: list[str] = []
    A = parts.append

    A('<title>AccuRite — Seasonal Search Demand</title>')
    A(STYLE)

    # ---- header --------------------------------------------------------------
    A('<header class="masthead">')
    A('<p class="eyebrow">AccuRite Excavation &middot; Northern Utah</p>')
    A('<h1>Seasonal Search Demand</h1>')
    A('<p class="standfirst">What people search for, season by season, filtered down to '
      'the people who want to <em>hire someone</em>. Every keyword in every group is listed '
      'below, along with every keyword thrown out and the reason why.</p>')
    A('<p class="provenance">Source: DataForSEO Google&nbsp;Ads <code>keywords_for_keywords</code>, '
      'location Utah, English &middot; pulled <strong>2026-07-13</strong> &middot; '
      'search volume and CPC are Google&rsquo;s figures; the season groupings and the '
      'intent filter are ours.</p>')
    A('</header>')

    # ---- season summary ------------------------------------------------------
    A('<section>')
    A('<h2>The headline</h2>')
    A('<p class="lede">Winter is not the quiet season. With do-it-yourself and '
      'research traffic stripped out, <strong>winter carries the most hire-intent search '
      'demand of any season</strong> — the work simply changes shape.</p>')
    A('<div class="tiles">')
    for s in SEASONS:
        cls = "tile peak" if s == peak_season else "tile"
        A(f'<div class="{cls}">')
        A(f'<p class="tile-label">{s}</p>')
        A(f'<p class="tile-value">{num(season_totals[s])}</p>')
        A('<p class="tile-unit">hire-intent searches</p>')
        A('</div>')
    A('</div>')
    A('<p class="footnote">Three-month buckets: Winter = Dec&ndash;Feb, Spring = Mar&ndash;May, '
      'Summer = Jun&ndash;Aug, Fall = Sep&ndash;Nov. Each figure is the sum of Google&rsquo;s '
      'monthly search volumes for every keyword in the groups below.</p>')
    A('</section>')

    # ---- by service ----------------------------------------------------------
    A('<section>')
    A('<h2>By service</h2>')
    A('<p>Sorted by winter demand. The mix is the story: sewer and water&nbsp;line work is a '
      'winter business, drainage is a warm-weather business.</p>')
    A('<div class="scroll">')
    A('<table class="summary">')
    A('<thead><tr><th>Service</th>' + "".join(f'<th class="n">{s}</th>' for s in SEASONS)
      + '<th class="n">Peak</th></tr></thead><tbody>')
    for service, totals, _ in service_rows:
        peak = max(totals, key=totals.get)
        A('<tr>')
        A(f'<td class="svc">{html.escape(service)}</td>')
        for s in SEASONS:
            hi = ' class="n hi"' if s == peak else ' class="n"'
            A(f'<td{hi}>{num(totals[s])}</td>')
        A(f'<td class="n"><span class="pill">{peak}</span></td>')
        A('</tr>')
    A('<tr class="total"><td>All services</td>'
      + "".join(f'<td class="n">{num(season_totals[s])}</td>' for s in SEASONS)
      + f'<td class="n"><span class="pill">{peak_season}</span></td></tr>')
    A('</tbody></table>')
    A('</div>')
    A('</section>')

    # ---- the buckets, fully exposed -----------------------------------------
    A('<section>')
    A('<h2>Exactly what is in each group</h2>')
    A('<p>This is the audit. Every keyword counted toward the numbers above appears here, '
      'with what advertisers pay per click — a useful lie-detector for intent. A high CPC means '
      'the click is worth real money to someone; a CPC under a dollar or two usually means '
      'the searcher is reading, not buying.</p>')

    for service, totals, rows in service_rows:
        A('<div class="bucket">')
        A(f'<h3>{html.escape(service)}</h3>')
        A('<p class="bucket-totals">'
          + " &middot; ".join(f'{s} <strong>{num(totals[s])}</strong>' for s in SEASONS)
          + '</p>')
        A('<div class="scroll">')
        A('<table class="kw">')
        A('<thead><tr><th>Keyword</th><th class="n">CPC</th>'
          + "".join(f'<th class="n">{s[:2]}</th>' for s in SEASONS)
          + '</tr></thead><tbody>')
        for r in rows:
            A('<tr>')
            A(f'<td>{html.escape(r["keyword"])}</td>')
            A(f'<td class="n cpc">{money(r["cpc"])}</td>')
            for s in SEASONS:
                A(f'<td class="n">{num(r["seasons"][s])}</td>')
            A('</tr>')
        A('</tbody></table>')
        A('</div>')
        A('</div>')
    A('</section>')

    # ---- research ------------------------------------------------------------
    A('<section>')
    A('<h2>Counted separately: price shoppers</h2>')
    A('<p>Cost and price queries are real buyers, but earlier in the process — they are '
      'reading, not calling. They are <strong>not</strong> in any total above. Worth content '
      'eventually; not worth counting as demand today.</p>')
    A('<div class="scroll">')
    A('<table class="kw"><thead><tr><th>Keyword</th><th>Service</th><th class="n">CPC</th>'
      '</tr></thead><tbody>')
    for service in SERVICE_ORDER:
        for r in research.get(service, []):
            A(f'<tr><td>{html.escape(r["keyword"])}</td>'
              f'<td class="svc">{html.escape(service)}</td>'
              f'<td class="n cpc">{money(r["cpc"])}</td></tr>')
    A('</tbody></table></div>')
    A('</section>')

    # ---- rejected ------------------------------------------------------------
    A('<section>')
    A('<h2>Thrown out, and why</h2>')
    A('<p>The part worth arguing with. If any of these belong back in, say so and the '
      'numbers change. Note <code>french drain</code> in particular — 880 searches a month '
      'at a <strong>$2.33</strong> CPC. That price is the market saying there is no job behind '
      'the click. It was inflating the drainage group until it was cut.</p>')
    A('<div class="scroll">')
    A('<table class="kw rejected"><thead><tr><th>Keyword</th><th class="n">Avg/mo</th>'
      '<th class="n">CPC</th><th>Reason cut</th></tr></thead><tbody>')
    for r in rejected:
        A('<tr>')
        A(f'<td>{html.escape(r["keyword"])}</td>')
        A(f'<td class="n">{num(r["avg_month"])}</td>')
        A(f'<td class="n cpc">{money(r["cpc"])}</td>')
        A(f'<td><span class="reason">{html.escape(r["reason"])}</span></td>')
        A('</tr>')
    A('</tbody></table></div>')
    A('</section>')

    # ---- method --------------------------------------------------------------
    A('<section class="method">')
    A('<h2>How a keyword gets in</h2>')
    A('<dl>')
    A('<dt>Kept &mdash; hire intent</dt><dd>The phrase contains a hiring signal: '
      '<em>contractor, company, companies, service, services, near me, installer, '
      'installation, repair, replacement, replace, install</em>. Someone using these words '
      'is looking for a person to do the work.</dd>')
    A('<dt>Set aside &mdash; research</dt><dd>The phrase contains <em>cost, price, how much, '
      'estimate, quote</em>. A future customer, but not one who is calling today. Counted in '
      'its own table, never in the season totals.</dd>')
    A('<dt>Cut &mdash; do-it-yourself</dt><dd><em>how to, diy, yourself, youtube, video, '
      'tutorial, guide.</em></dd>')
    A('<dt>Cut &mdash; not the business</dt><dd>Snow removal, septic (including Google&rsquo;s '
      '&ldquo;sewer tank&rdquo; alias for it), septic pumping, trenchless and no-dig methods, '
      'and any plumbing inside a house or business. All confirmed out of scope on 2026-07-13.</dd>')
    A('<dt>Cut &mdash; equipment, jobs, rivals</dt><dd>Excavator rentals and retail, employment '
      'searches, and competitors&rsquo; own business names, which are people looking for a '
      'specific rival rather than for a contractor.</dd>')
    A('<dt>Cut &mdash; bare head terms</dt><dd>No hiring signal at all &mdash; '
      '<em>french drain</em>, <em>water main</em>, <em>concrete removal</em>. Mostly reading.</dd>')
    A('</dl>')
    A('<h3>What to distrust</h3>')
    A('<ul class="caveats">')
    A('<li><strong>These are Utah statewide figures.</strong> AccuRite&rsquo;s slice of the '
      'Ogden corridor is a fraction of them. Trust the <em>comparisons</em> between seasons '
      'and services; do not read the absolute numbers as traffic AccuRite can win.</li>')
    A('<li><strong>One suspicious month.</strong> <code>sewer line repair near me</code> reports '
      '1,900 searches in February against a 480/month average. That single reading drives a lot '
      'of the winter total and has not been corroborated against a second source. Check it in '
      'Keyword Planner before betting a crew schedule on it.</li>')
    A('<li><strong>Google repeats itself.</strong> The same query comes back under several '
      'phrasings (<em>demolition contractor</em> / <em>demolish contractor</em> / '
      '<em>contractor demolition</em>, all identical figures). They are shown as-is rather '
      'than silently merged, so the duplication is visible rather than hidden.</li>')
    A('</ul>')
    A('</section>')

    A('<footer><p>Prepared for Shawn Durrant &middot; data pulled 2026-07-13 &middot; '
      'AccuRite Excavation &amp; Hauling</p></footer>')

    OUT.write_text("\n".join(parts))
    print(f"Wrote {OUT}  ({OUT.stat().st_size:,} bytes)")
    print(f"Season totals (hire intent): "
          + ", ".join(f"{s} {season_totals[s]:,}" for s in SEASONS))
    return 0


STYLE = """
<style>
  :root {
    --ground: #FBF9F4;
    --surface: #FFFFFF;
    --ink: #26241F;
    --ink-soft: #5E594E;
    --ink-faint: #8C8574;
    --rule: #E3DDCE;
    --gold: #B58900;
    --gold-bright: #E8C840;
    --clay: #A0522D;
    --slate: #4A5D6B;
    --shadow: 0 1px 2px rgba(38, 36, 31, .06), 0 8px 24px -16px rgba(38, 36, 31, .25);
    --display: Georgia, "Iowan Old Style", "Times New Roman", serif;
    --body: system-ui, -apple-system, "Segoe UI", Helvetica, Arial, sans-serif;
    --data: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
  }
  @media (prefers-color-scheme: dark) {
    :root {
      --ground: #1A1917;
      --surface: #232220;
      --ink: #EDE8DC;
      --ink-soft: #B0A996;
      --ink-faint: #837C6C;
      --rule: #3A382F;
      --gold: #E8C840;
      --gold-bright: #F2D96A;
      --clay: #C97F52;
      --slate: #8FA6B5;
      --shadow: 0 1px 2px rgba(0, 0, 0, .4), 0 8px 24px -16px rgba(0, 0, 0, .8);
    }
  }
  :root[data-theme="dark"] {
    --ground: #1A1917; --surface: #232220; --ink: #EDE8DC; --ink-soft: #B0A996;
    --ink-faint: #837C6C; --rule: #3A382F; --gold: #E8C840; --gold-bright: #F2D96A;
    --clay: #C97F52; --slate: #8FA6B5;
    --shadow: 0 1px 2px rgba(0,0,0,.4), 0 8px 24px -16px rgba(0,0,0,.8);
  }
  :root[data-theme="light"] {
    --ground: #FBF9F4; --surface: #FFFFFF; --ink: #26241F; --ink-soft: #5E594E;
    --ink-faint: #8C8574; --rule: #E3DDCE; --gold: #B58900; --gold-bright: #E8C840;
    --clay: #A0522D; --slate: #4A5D6B;
    --shadow: 0 1px 2px rgba(38,36,31,.06), 0 8px 24px -16px rgba(38,36,31,.25);
  }

  body {
    margin: 0 auto;
    padding: clamp(1.5rem, 4vw, 4rem) clamp(1.1rem, 4vw, 2.5rem) 4rem;
    max-width: 68rem;
    background: var(--ground);
    color: var(--ink);
    font-family: var(--body);
    font-size: 1rem;
    line-height: 1.65;
    -webkit-font-smoothing: antialiased;
  }

  section { margin-top: 4rem; }
  p { max-width: 62ch; }

  .masthead { border-bottom: 3px solid var(--gold); padding-bottom: 2rem; }
  .eyebrow {
    font-size: .74rem; letter-spacing: .16em; text-transform: uppercase;
    color: var(--gold); font-weight: 700; margin: 0 0 .9rem;
  }
  h1 {
    font-family: var(--display); font-weight: 400; text-wrap: balance;
    font-size: clamp(2.3rem, 6vw, 3.9rem); line-height: 1.04;
    letter-spacing: -.015em; margin: 0 0 1.2rem;
  }
  .standfirst { font-size: 1.16rem; color: var(--ink-soft); margin: 0 0 1.4rem; }
  .standfirst em { color: var(--ink); font-style: italic; }
  .provenance {
    font-size: .82rem; color: var(--ink-faint); line-height: 1.55;
    max-width: 68ch; margin: 0; padding-top: 1rem; border-top: 1px solid var(--rule);
  }

  h2 {
    font-family: var(--display); font-weight: 400; text-wrap: balance;
    font-size: clamp(1.6rem, 3.4vw, 2.15rem); line-height: 1.15;
    margin: 0 0 .9rem; padding-bottom: .5rem; border-bottom: 1px solid var(--rule);
  }
  h3 {
    font-family: var(--body); font-size: .82rem; font-weight: 700;
    letter-spacing: .12em; text-transform: uppercase; color: var(--ink);
    margin: 0 0 .35rem;
  }
  .lede { font-size: 1.08rem; }
  .lede strong, p strong { color: var(--ink); font-weight: 650; }

  .tiles {
    display: grid; gap: 1rem; margin: 1.8rem 0 1rem;
    grid-template-columns: repeat(auto-fit, minmax(9.5rem, 1fr));
  }
  .tile {
    background: var(--surface); border: 1px solid var(--rule);
    border-radius: 2px; padding: 1.15rem 1.2rem; box-shadow: var(--shadow);
  }
  .tile.peak {
    border-color: var(--gold);
    box-shadow: inset 0 3px 0 var(--gold-bright), var(--shadow);
  }
  .tile-label {
    margin: 0; font-size: .74rem; letter-spacing: .13em;
    text-transform: uppercase; color: var(--ink-faint); font-weight: 700;
  }
  .tile.peak .tile-label { color: var(--gold); }
  .tile-value {
    margin: .3rem 0 .1rem; font-family: var(--data); font-size: 2.1rem;
    font-weight: 600; font-variant-numeric: tabular-nums; letter-spacing: -.02em;
  }
  .tile-unit { margin: 0; font-size: .76rem; color: var(--ink-faint); }
  .footnote { font-size: .84rem; color: var(--ink-faint); }

  .scroll { overflow-x: auto; margin: 1.4rem 0; }
  table { border-collapse: collapse; width: 100%; font-size: .92rem; }
  th, td {
    text-align: left; padding: .6rem .85rem;
    border-bottom: 1px solid var(--rule); white-space: nowrap;
  }
  thead th {
    font-size: .72rem; letter-spacing: .1em; text-transform: uppercase;
    color: var(--ink-faint); font-weight: 700; border-bottom: 2px solid var(--rule);
  }
  td.n, th.n { text-align: right; font-family: var(--data); font-variant-numeric: tabular-nums; }
  th.n { font-family: var(--body); }
  td.hi { color: var(--gold); font-weight: 700; }
  td.cpc { color: var(--ink-soft); }
  td.svc { color: var(--ink-soft); }
  tbody tr:hover { background: color-mix(in srgb, var(--gold-bright) 8%, transparent); }

  table.summary td:first-child { font-weight: 600; }
  tr.total td {
    border-top: 2px solid var(--rule); border-bottom: none;
    font-weight: 700; padding-top: .8rem;
  }
  .pill {
    display: inline-block; padding: .12rem .55rem; border-radius: 999px;
    background: color-mix(in srgb, var(--gold-bright) 22%, transparent);
    color: var(--gold); font-family: var(--body); font-size: .72rem;
    font-weight: 700; letter-spacing: .05em;
  }

  .bucket {
    margin-top: 2.4rem; padding-top: 1.4rem; border-top: 1px solid var(--rule);
  }
  .bucket-totals {
    margin: 0; font-size: .86rem; color: var(--ink-faint);
    font-variant-numeric: tabular-nums;
  }
  .bucket-totals strong { color: var(--ink); font-family: var(--data); }

  table.rejected td:first-child { color: var(--ink-soft); }
  .reason {
    font-size: .78rem; color: var(--clay);
    border-left: 2px solid var(--clay); padding-left: .5rem;
  }

  .method dl { margin: 1.5rem 0; }
  .method dt {
    font-weight: 700; font-size: .82rem; letter-spacing: .06em;
    text-transform: uppercase; color: var(--gold); margin-top: 1.2rem;
  }
  .method dd { margin: .3rem 0 0; padding-left: 0; max-width: 62ch; color: var(--ink-soft); }
  .method dd em { color: var(--ink); font-style: normal; font-family: var(--data); font-size: .88em; }
  .caveats { max-width: 62ch; padding-left: 1.1rem; color: var(--ink-soft); }
  .caveats li { margin-bottom: .7rem; }
  .caveats strong { color: var(--ink); }

  code {
    font-family: var(--data); font-size: .88em;
    background: color-mix(in srgb, var(--slate) 12%, transparent);
    padding: .08rem .32rem; border-radius: 2px;
  }

  footer {
    margin-top: 4.5rem; padding-top: 1.2rem; border-top: 1px solid var(--rule);
    font-size: .8rem; color: var(--ink-faint);
  }
  @media (prefers-reduced-motion: reduce) {
    * { animation: none !important; transition: none !important; }
  }
</style>
"""

if __name__ == "__main__":
    raise SystemExit(main())
