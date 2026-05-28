# AccuRite Excavation — Lead Generation Plan

*Revision 2 — prepared for Claude Code execution*
*Updated: April 17, 2026*

---

## How to Read This Document

Every action is tagged with its executor:

- **[CC]** — Claude Code can execute directly against the codebase
- **[Ross]** — Ross does manually (strategy review, copy approval, scheduling)
- **[Shawn]** — Requires the client's input or access
- **[HighLevel UI]** — Done inside HighLevel's interface
- **[GSC UI]** — Done inside Google Search Console
- **[Google Ads UI]** — Done inside Google Ads (account + Editor)
- **[GBP UI]** — Done inside Google Business Profile

Tasks are ordered by "do now" vs. "waits on something." Anything CC can execute today is marked **⚡ Ship today**.

---

## What Claude Code Can and Cannot Do on This Project

### ✅ CC can execute

- Run diagnostic `curl` commands against old WordPress URLs and report redirect status codes
- Edit Astro components, layouts, and MDX/markdown content files
- Implement `data-ghl-phone` attribute convention across the site
- Generate Google Ads Editor CSV files for bulk import
- Rewrite title tags and meta descriptions in BaseLayout and frontmatter
- Add the basement excavation content section to `/services/residential-excavation`
- Grep/audit the codebase for existing phone number usage patterns
- Run builds and report errors
- Commit changes to git (with Ross's review/approval)
- Create tasks in Teamwork (Ross's project management system) for any action items that Ross or Shawn are responsible for — see the Teamwork Task Creation section below

### ❌ CC cannot execute (Ross or Shawn does these)

- Log into Google Business Profile and convert to SAB **[Shawn + Ross]**
- Log into Google Search Console to submit indexing requests or removals **[Ross, GSC UI]**
- Provision HighLevel Number Pool or install tracking script in HighLevel **[Ross, HighLevel UI]**
- Launch or configure Google Ads campaigns — upload the CSV manually **[Ross, Google Ads UI]**
- Place real test calls to verify DNI routing
- Deploy to Netlify (unless Netlify CLI is set up — confirm with Ross first)

---

## Do-Not-Touch List

CC should not modify these without explicit approval from Ross:

- `src/data/business.json` — single source of truth for NAP data
- `public/_redirects` — carefully structured 301 map; additions only after diagnostic pass
- Anything under `/privacy`, `/terms`, or `/404`
- Any file in the `/locations/` tree unless specifically tasked (40 pages, tight templates)
- Schema markup logic in `BaseLayout` (read-only without approval — it's NAP-critical)
- Any blog post content

---

## Situation Summary

AccuRite has real organic signal and weak paid competition in its market. Position 1.7 for "excavation company," 1.9 for "excavation near me," impression growth of +152% month-over-month. The lead leak is elsewhere: brand-SERP fragmentation (14 URLs competing for "accurite"), a Huntsville-registered GBP instead of Ogden, and legacy WordPress URLs still pulling clicks from the new Astro site.

The plan runs three parallel tracks:

1. Free foundation work in week 1
2. Google Ads launch in week 2
3. Organic and content polish shipping as soon as today

Total monthly spend stays under $1,000.

---

## Tooling: HighLevel Handles Call Tracking, CRM, and Review Automation

Already owned, so marginal cost is $0. Replaces CallRail (~$45/mo) and standalone review generation (~$150/mo).

**Configuration [Ross, HighLevel UI]:**

- **Number Pool** of 4 local 801-area-code numbers, all forwarding to Shawn's line, call recording on
- **Dedicated tracking number** for Google Ads call assets (outside the pool — used directly in ad copy, not injected via DNI)
- **Missed-call SMS automation** — fires "Hi, this is Shawn at AccuRite, sorry I missed you — calling right back" when Shawn doesn't answer
- **Review request automation** — post-job workflow texts customer a direct Google review link shortly after job completion
- **GBP keeps the real number** — do NOT put a HighLevel tracking number on the Google Business Profile

---

## DNI Markup Specification

The DNI script swap target is the attribute `data-ghl-phone`. All phone number renders on the site get this attribute so that when the HighLevel tracking script is installed, DNI works sitewide without further component refactoring.

### Markup convention [CC — ⚡ Ship today]

**For clickable phone links:**

```astro
<a
  href={`tel:+1${business.phoneDigits}`}
  data-ghl-phone
  class="phone-link"
>
  {business.phoneFormatted}
</a>
```

**For display-only phone numbers (e.g., inside prose):**

```astro
<span data-ghl-phone>{business.phoneFormatted}</span>
```

### Implementation tasks [CC]

1. **Audit existing phone markup:** `grep -rn "tel:" src/` and `grep -rn "814-6975" src/` — report all locations to Ross before editing
2. **Add `data-ghl-phone` to every phone render** — header, footer, contact page, free-estimate page, service page CTAs, location page CTAs, any inline prose mentions
3. **Do NOT swap the number values themselves** — the real number `(801) 814-6975` stays hardcoded everywhere. The attribute just marks the elements for DNI to find later.
4. **Verify schema markup is unaffected** — the JSON-LD `telephone` field in `BaseLayout` must continue to output the real number
5. **Build check:** confirm Astro build passes and no hydration warnings fire

### Later, when HighLevel script is ready [Ross, Astro]

Drop the HighLevel tracking script into `BaseLayout.astro` `<head>`. DNI fires on any element with `data-ghl-phone` attribute when the visitor arrives with `gclid` or `utm_source=google` + `utm_medium=cpc` parameters. Bots don't execute JS, so crawlers see the real number in HTML — NAP integrity preserved.

---

## Track 1: Foundation Work

### 1A. Redirect Audit [CC — ⚡ Ship today]

Confirm the `_redirects` file is returning real 301 status codes before any GSC work. Run these checks and report results to Ross:

```bash
curl -I https://accuriteexcavation.com/utah-ogden-excavation
curl -I https://accuriteexcavation.com/contact-us-2
curl -I https://accuriteexcavation.com/about-us-2
curl -I https://accuriteexcavation.com/the-accurite-excavation-promise
curl -I https://accuriteexcavation.com/what-makes-the-best-construction-company-in-utah
curl -I https://accuriteexcavation.com/our-services
curl -I https://accuriteexcavation.com/category/commercial
curl -I https://accuriteexcavation.com/our-work-past-projects
curl -I https://accuriteexcavation.com/we-build-roads
curl -I https://accuriteexcavation.com/steam-plant-hill
curl -I https://accuriteexcavation.com/about/
curl -I http://www.accuriteexcavation.com/
```

**Pass criteria:** each returns HTTP/2 301 with a `location:` header pointing to a current canonical URL.

**Fail actions:** if any return 200, 302, or 404, flag to Ross before proceeding to GSC work.

### 1B. GBP — Convert to Service Area Business [Shawn + Ross, GBP UI]

The Huntsville registration is actively suppressing Ogden map-pack rankings.

- Remove public Huntsville address
- Set service area: Weber, Davis, Morgan counties
- Primary city: Ogden
- Verify business categories: Excavating Contractor (primary), plus Demolition Contractor, Septic System Service
- Upload 10+ real job-site photos
- Add 3 GBP Posts about recent completed jobs (no links or phone numbers per platform rules)

**Blocked on:** Shawn's confirmation of GBP admin access and confirmation that removing the Huntsville listing doesn't conflict with business license/insurance records.

### 1C. Brand-SERP Cleanup [Ross, GSC UI]

612 people searched "accurite" in 90 days with effectively 0% CTR across 14 URLs. Most are legacy WordPress URLs still in Google's index.

- Use GSC Removals tool to request removal of the worst legacy offenders:
  - `/utah-ogden-excavation`
  - `/contact-us-2`
  - `/about-us-2`
  - `/the-accurite-excavation-promise`
  - `/our-services`
  - `/what-makes-the-best-construction-company-in-utah`
- URL Inspection → Request Indexing on canonical pages: `/`, `/about`, `/contact`, `/services/residential-excavation`, `/reviews`
- Confirm no old WordPress sitemap is submitted anywhere

### 1D. Call Tracking Setup [Ross, HighLevel UI]

- Provision 4-number pool in HighLevel
- Configure missed-call SMS automation
- Configure post-job review request workflow
- Note: the DOM markup work is already done by CC in the DNI Markup Specification section — once the HighLevel script is placed in `BaseLayout`, DNI fires automatically

---

## Track 2: Organic Quick Wins [CC — ⚡ Ship today]

These do not need DNI, do not need GBP fixes, and do not need ads to be live. Ship them today to get 2 extra weeks of ranking/CTR data before May peak.

### 2A. Title Tag + Meta Description Rewrites

CC: update the `metaTitle` and `metaDescription` frontmatter (or equivalent Astro props) on the following pages. The existing `| AccuRite Excavation` suffix pattern is preserved.

---

**`/services/grading-land-clearing`** *(373 impressions, position 19.3)*

- **Current:** Grading & Land Clearing — Northern Utah | AccuRite Excavation
- **New title:** Grading & Land Clearing Contractor — Ogden, UT | AccuRite Excavation
- **New meta:** Site grading, lot clearing, and drainage correction across Weber and Davis counties. E100 licensed, 31+ years in Northern Utah. Free estimates — call (801) 814-6975.

---

**`/locations/riverton`** *(324 impressions, position 10.4 — close to page 1)*

- **New title:** Excavation Contractor in Riverton, UT | AccuRite Excavation
- **New meta:** Riverton excavation, foundation digs, grading, and retaining walls. Local experience with south Salt Lake Valley soils. Free estimates — call (801) 814-6975.

---

**`/services/underground-utilities`** *(214 impressions, position 7.1 — page 1)*

- **New title:** Underground Utility Contractor — Ogden, UT | AccuRite Excavation
- **New meta:** Water lines, sewer, storm drain, and utility trenching for residential and commercial projects across Weber and Davis counties. Free estimates — call (801) 814-6975.

---

**`/reviews`** *(214 impressions, position 4.5 — major CTR rescue)*

- **New title:** Customer Reviews — AccuRite Excavation | Ogden, UT
- **New meta:** Read real Google reviews from Weber and Davis County customers. 4.9 stars across 49 reviews. 31 years of excavation work across Northern Utah.

---

**`/services/residential-excavation`** *(170 impressions, position 22.7)*

- **New title:** Residential Excavation Contractor — Basements & Foundations | Ogden, UT
- **New meta:** Basement excavation, foundation digs, site prep, and grading for homes across Weber and Davis counties. E100 licensed since 1995. Call (801) 814-6975.

---

**`/locations/south-ogden`** *(241 impressions, position 19.0)*

- **New title:** Excavation Contractor in South Ogden, UT | AccuRite Excavation
- **New meta:** South Ogden excavation, foundation work, retaining walls, and drainage. Weber County licensed and insured since 1995. Free estimates — call (801) 814-6975.

---

### 2B. Basement Excavation Content Block

Add as a new H2 section on `/services/residential-excavation`. Place it after the page's existing intro/overview section and before the soil-conditions block. Match the existing page voice: direct, specific, no marketing fluff.

**Section markdown to implement:**

```markdown
## Basement Excavation in Utah

New basement construction is one of the most common residential excavation jobs we do in Northern Utah. Most Wasatch Front homes are built with full or daylight basements, and getting the dig right sets up everything that follows — foundation pour, waterproofing, backfill, and final grade.

A standard residential basement excavation runs 8 to 10 feet deep depending on the foundation design and whether the basement is below grade or walk-out. We work from your builder's foundation plan, stake the excavation to the dimensions and depth called for, and cut the hole with enough overdig to allow for wall forms and drainage work. On a typical Ogden-area lot, a basement dig takes one to two days once we're on site.

Soil conditions shape how the work goes. Valley-floor basements in Roy, West Haven, or Riverdale usually dig cleanly in sand and silt. Bench lots above Harrison Boulevard or in North Ogden often hit hardpan caliche or fractured rock that requires hydraulic hammering. We'll know what to expect once we walk the site and review the geotech report if one has been done. If water comes up during excavation — common in lower West Haven and parts of Bountiful in spring — we have dewatering equipment to manage it without stalling the foundation schedule.

Basement excavation costs depend on depth, soil, equipment access, and haul-off. Rocky bench lots cost more than valley dirt. Tight infill lots in older Ogden neighborhoods take longer than open new-construction subdivisions. We quote basement excavation after a site visit, not from photos or square footage. Call (801) 814-6975 for a free estimate.
```

**Implementation notes for CC:**
- Inspect `/services/residential-excavation`'s source file (likely `.astro` or `.mdx` under `src/pages/services/`) for its content structure
- Match the existing H2/H3 heading pattern on the page
- Add the phone number with the `data-ghl-phone` convention
- Confirm no conflicts with existing basement-related copy on the page (do not duplicate)

### 2C. Image Replacement [Ross + Shawn]

AI-generated placeholders on top 5 service pages get swapped for real job-site photos as Shawn captures them. Budget ~$75/mo accrued from the flex bucket toward a half-day shoot in peak season.

---

## Track 3: Google Ads Launch

Total ad budget: **$925/mo**, starting conservatively. Scale based on CPL.

### 3A. Brand Protection — Monday, April 20 [Ross, Google Ads UI]

Ship this Monday. Doesn't need DNI (the ad itself is the source attribution since it's a dedicated brand campaign). Brand CTR recovery starts immediately.

- **Campaign:** AccuRite — Brand Protection
- **Budget:** $50/mo ($1.64/day)
- **Bidding:** Manual CPC, $2.50 max
- **Keywords (exact match):**
  - `[accurite]`
  - `[accurite excavation]`
  - `[accurate excavation]` *(misspelling — 43 impressions at position 21)*
- **Ad copy:** Emphasize "the real AccuRite" / "since 1995" / direct phone number in call assets

### 3B. Main Campaigns — Launch Week 2 [Ross, Google Ads UI]

Blocked on: HighLevel DNI live and tested. Running $925/mo of traffic with no attribution is the mistake we're avoiding.

CC generates the bulk-import CSV; Ross uploads via Google Ads Editor.

#### Campaign 1 — Residential Basement/Foundation ($500/mo)

Keywords (phrase + exact only):

```
basement excavation ogden
basement excavation utah
foundation excavation utah
excavation contractor ogden
excavation company ogden
dig basement utah
new construction excavation ogden
residential excavation ogden
residential excavation contractor utah
```

#### Campaign 2 — Septic + Underground Utilities ($275/mo)

```
septic system installation ogden
septic tank install utah
septic system installer weber county
sewer line install ogden
trenching contractor weber county
underground utility contractor utah
utility excavation ogden
```

#### Campaign 3 — Retaining Walls Test ($100/mo)

Exact only. Tight geo: Draper, Huntsville, Mountain Green, Morgan.

```
boulder retaining wall contractor utah
rock retaining wall contractor ogden
retaining wall installer weber county
boulder retaining wall draper
```

### 3C. Account-Level Settings

**Geo targeting (main campaigns):** Ogden, Roy, Layton, Clearfield, Bountiful, North Ogden, South Ogden, Riverdale, Washington Terrace, West Haven, Clinton, Syracuse, Farmington, Kaysville.

**Bidding strategy:** Manual CPC for first 2–3 weeks. Switch to Maximize Conversions once 15+ tracked calls logged (month 2 earliest).

**Ad formats:** Call-only ads during business hours (6:30 AM – 6 PM Mon–Fri). Standard search ads with call assets outside those hours (routes to HighLevel missed-call workflow if unanswered).

**Mandatory negative keywords (account-level):**

```
foundation repair, crack repair, waterproofing, leveling, basement waterproofing, mudjacking
rental, rent, for sale, used, parts, buy
jobs, hiring, salary, training, school, license, operator, career
DIY, how to, free, toys, rc, simulator, game, video
bobcat, kubota, cat, caterpillar, mini excavator
craigslist, homedepot, lowes
```

The foundation-repair family is critical — this was the LSA problem. Hard-block it day one.

### 3D. Google Ads CSV Generation [CC — when Ross is ready to upload]

When Ross is ready to launch Campaigns 1–3, CC generates a Google Ads Editor-compatible CSV from the structure above. Output to a separate file; do not embed in the main codebase.

**Required CSV columns (Google Ads Editor import format):**

```
Campaign, Campaign Type, Budget, Budget Type, Bid Strategy Type, Ad Group, Max CPC, Keyword, Match Type, Status, Final URL
```

Additional sheets/files for ads and negative keywords:

- **Ads sheet:** Campaign, Ad Group, Ad Type, Headline 1-15, Description 1-4, Final URL, Path 1, Path 2
- **Negative keywords sheet:** Campaign (blank for account-level), Keyword, Match Type

**Landing page mapping:**

- Residential Basement/Foundation → `/services/residential-excavation`
- Septic + Underground Utilities → `/services/septic-systems` and `/services/underground-utilities` (split ad groups)
- Retaining Walls → `/services/rock-walls-retaining-walls`
- Brand Protection → `/` (homepage)

CC should prompt Ross for ad copy (headlines/descriptions) before generating — those are voice-sensitive and Ross should draft or approve.

---

## Month 2+ Optimization

- Review CPL per campaign in HighLevel; kill or scale based on actual conversion data
- Switch ad bidding to Maximize Conversions once 15+ tracked calls logged
- Expand keyword set only into verticals that prove profitable
- Add content to whichever location pages are converting; cull low performers
- GBP Posts cadence: 1/week minimum, ideally 2/week

---

## Budget Summary

| Item | Monthly |
|---|---|
| Google Ads — Residential Foundation | $500 |
| Google Ads — Septic + Utilities | $275 |
| Google Ads — Retaining Walls (test) | $100 |
| Google Ads — Brand Protection | $50 |
| HighLevel (tracking, CRM, automation) | $0 *(already owned)* |
| Photography / flex | $75 |
| **Total** | **$1,000** |

---

## What's Not in This Plan (and Why)

- **LSA ads** — per Ross's direction; burned by foundation-repair leads previously
- **Facebook/Instagram ads** — wrong platform for commercial-intent excavation
- **SEO blog content sprint** — 12 posts already exist; paid and GBP move the needle faster for "need leads now"
- **Retargeting display** — not enough traffic volume to justify setup cost
- **Commercial/government bidding keywords** — those come from relationships and bid lists, not clicks
- **Broad-match keywords** — will waste budget at $1K/mo
- **Google Ads API automation via CC** — CC's Google Ads API integration is unreliable; CSV upload via Google Ads Editor is the path

---

## Open Questions for Shawn

1. Google Ads account ownership — who's admin? Needs to be clear before launch.
2. GBP admin access — who currently has it?
3. Confirm Shawn's phone answer rate during business hours — if it's low, missed-call SMS automation becomes even more critical.
4. OK to schedule half-day photo shoot in May/June for real job-site images?
5. Business license / insurance — does removing the Huntsville address from GBP create any registration conflicts?

---

## Realistic 90-Day Outcome

- **Month 1:** 2–5 qualified calls from ads (learning phase). GBP map-pack lift visible by week 4. Brand-CTR recovery visible within 2 weeks as old URLs drop from index.
- **Month 2:** 6–12 qualified calls from ads with tightened keyword set. Review count growing by 4–8/month.
- **Month 3:** 10–15 qualified calls from ads consistently. Map-pack presence for "excavation contractor Ogden" established. ~40 Google reviews, top-of-category in Weber County.

---

## Teamwork Task Creation [CC]

Ross uses Teamwork as his project management system. Every action item in this plan tagged [Ross], [Shawn], [HighLevel UI], [GSC UI], [GBP UI], or [Google Ads UI] should be created as a Teamwork task so nothing gets lost between sessions.

### Setup

- **Find the AccuRite project** in Teamwork. If an "AccuRite Excavation" project already exists, add tasks there. If not, ask Ross which project to use.
- **Create a task list** within that project called something like "Lead Gen Plan — April 2026" to keep these grouped and separate from site-build work.
- **Assign all tasks to Ross**, even the Shawn-owned ones. Ross coordinates with Shawn; he shouldn't need a separate Teamwork seat for the client.
- **Due dates:** set where specified below. For unspecified items, leave blank — don't invent dates.

### Task structure

- Use parent tasks for grouped work (e.g., "GBP Conversion to Service Area Business" with sub-tasks for each action)
- Put the executor tag at the start of the description so Ross can see at a glance who owns what (e.g., "[Shawn + Ross, GBP UI] — Remove Huntsville address...")
- Keep descriptions short but include the "why" so Ross doesn't have to re-read the full plan to remember context
- Link back to the relevant section of this plan where useful

### Tasks to create

**Ship this week:**

1. **Brand Protection Google Ads campaign launch** — Due Monday, April 20. [Ross, Google Ads UI]. $50/mo, exact match on accurite / accurite excavation / accurate excavation. Protects against brand-SERP leak.
2. **GSC: Submit removal requests for legacy WP URLs** — [Ross, GSC UI]. Six URLs listed in section 1C. Do this after CC's redirect diagnostic passes.
3. **GSC: Request Indexing on 5 canonical pages** — [Ross, GSC UI]. Homepage, about, contact, residential-excavation, reviews.

**Parent: GBP Conversion to Service Area Business** — [Shawn + Ross, GBP UI]
- Confirm GBP admin access — who has it?
- Confirm business license / insurance implications of removing Huntsville address
- Remove Huntsville address
- Set service area to Weber, Davis, Morgan counties with primary city Ogden
- Verify business categories (Excavating Contractor primary, plus Demolition + Septic)
- Upload 10+ real job-site photos
- Add 3 GBP Posts about recent completed jobs (no links, no phone numbers)

**Parent: HighLevel Setup** — [Ross, HighLevel UI]
- Provision 4-number pool (801 area code, all forwarding to Shawn)
- Enable call recording on the pool
- Set up dedicated tracking number for Google Ads call assets (outside the pool)
- Configure missed-call SMS automation
- Configure post-job review request workflow
- Grab tracking script snippet and hand to CC for `BaseLayout` install

**Parent: Main Google Ads Launch** — [Ross, Google Ads UI] — blocked on DNI live
- Confirm Google Ads account ownership with Shawn
- Draft ad copy (headlines + descriptions) — coordinate with Claude web for voice-matched copy
- Review CC-generated CSV
- Upload via Google Ads Editor
- Confirm negative keyword list applied at account level before enabling campaigns

**Standalone tasks:**

4. **Shawn: confirm phone answer rate during business hours** — context for how much weight the missed-call SMS automation carries.
5. **Schedule half-day photo shoot with Shawn** — May or June. Real job-site photos to replace AI placeholders on top 5 service pages.
6. **Week 1: Shawn triggers HighLevel review workflow manually** — after every completed job. Evaluate automation path in month 2.
7. **Month 2: review CPL per ad campaign, kill or scale** — after 15+ tracked calls.

### What not to put in Teamwork

- CC's own execution tasks (code edits, builds, diffs) — those live in the CC session, not the PM system
- Anything not tagged for a human executor



1. **Diagnostic pass:** run the 12 `curl -I` commands, report redirect status
2. **Phone markup audit:** grep for `tel:` and `814-6975`, report inventory
3. **Phone markup implementation:** add `data-ghl-phone` to every phone render
4. **Title/meta rewrites:** update the 6 priority pages
5. **Basement content block:** add the new H2 section to residential excavation page
6. **Build + smoke test:** Astro build passes, no hydration warnings, phone numbers still render as real number
7. **Create Teamwork tasks** for all items in the Teamwork Task Creation section — this ensures Ross and Shawn's responsibilities don't get lost between sessions
8. **Report back to Ross** with a diff summary and Teamwork task links before any deploy

The Google Ads CSV and HighLevel DNI script integration wait for later sessions.
