# Stage — history

Moved out of `docs/stage-current.md` on 2026-07-30 so the stage doc fits the
SessionStart per-hook byte cap (~9,000 bytes measured on the JSON-escaped hook
output; over that the harness silently injects only a ~2KB preview). Nothing was
deleted — every line below is verbatim from the stage doc. This file is NOT
auto-loaded; read it on demand.

## Recently shipped

- **2026-07-13** — **Winter seasonal keyword research** (research only, nothing on the live site). Built a pipeline in `research/keyword-research/` that pulls 12-month `monthly_searches` arrays from DataForSEO and filters to strict hire intent. Findings (Utah statewide, hire-intent only, measured 2026-07-13): **winter carries the most demand of any season** — Winter 12,230 / Spring 10,080 / Summer 9,440 / Fall 8,860. By service in winter: excavation 4,110, sewer/water line 3,870, demolition 3,150, drainage 570. **Demolition genuinely peaks in winter**; **drainage/french drain is a warm-weather business**; **"winter excavation" has no search demand at all** (1 keyword above 20/mo, and it peaks in March) — do not write "we dig in frozen ground" content expecting traffic. Report: `research/keyword-research/seasonal-demand.html`. Commits `25d6bc8`, `9a633f0`, `25c1cb8`, `b7207b5`, `4a596b6`.
- **2026-07-17** — Migrated the GBP weekly post off the claude.ai cloud routine to a **local macOS launchd job** (`com.rosswalker.accurite-gbp-weekly` → `scripts/run-gbp-weekly.sh` → gbp-post skill headless, REST-only), Tuesday 12:03 local. Root cause of the ongoing failure: the cloud sandbox blocks outbound HTTPS to `csfund.teamwork.com`, so REST was silently proxy-rejected — the token was fine all along. Old cloud routine disabled. Commit `c258b73`. REST reachability verified from a launchd-like env; first full live run is 2026-07-21.
- **2026-07-13** — Attempted to fix the GBP weekly post routine by replacing the expiring Teamwork MCP connector with a static-token REST client (`d83529d`). The MCP OAuth had expired ~2026-06-23 and silently killed three weeks of posts (06-23, 06-30, 07-07). **This fix did not actually work** — see the 2026-07-17 entry: REST ran in a cloud sandbox that can't reach Teamwork.
- **2026-07-03** — Generated the **June 2026** client SEO report on demand (off the monthly launchd cycle). GSC June vs May: clicks 128 (+22%), impressions 18,400 (+25%), queries ranked 910 (+16%); leads 5 (May 6 — shown as the rising quarter 2→4→6→5, down-MoM buried per the only-good-news rule after Ross re-tagged June AccuRite leads in the sheet). PDF at `~/Documents/accurite-reports/accurite-seo-2026-06.pdf`; review task TW #36729916 (due 2026-07-06), created via Teamwork REST API (MCP token expired). Also shipped 3 report-generator improvements in `3sm_code` (pushed `5d1aec5`): bury down-leads MoM + show trend, fix work_shipped filter leaking internal commits, allow curated client-readable work_shipped bullets. GBP still shows the API-pending stub.
- **2026-06-23** — Fixed blog-index 404s: `blog/index.astro` linked to `/blog/${post.id}`, but Astro 5 `post.id` carries the `.md` extension, so every blog-index link 404'd (surfaced via the new Hill AFB safety post). Stripped `.md` on both links (commit `63a48c3`); all 13 posts return 200. Added 13 enumerated per-slug 301s in `netlify.toml` for stale `.md` URLs (`6104954`; wildcard/placeholder forms don't work on Netlify — see global memory). GSC read-only inspection diagnosed indexation state (see In-flight follow-up). Verified live.
- **2026-06-22** — HHI Corporation safety letter (Hill AFB B1286 Steam Plant) added across the site: new human-first blog post `/blog/excavation-safety-on-federal-projects` + proof sections on `/safety`, `/services/government-projects`, the existing Hill AFB post, and an HHI testimonial in `reviews.json` (renders on `/reviews`, `/services/government-projects`, `/locations/layton`). Commit `9bef056`, verified live. Keyword research (`research/keyword-research/`) confirmed the angle is an E-E-A-T/conversion asset, not a traffic play. Cassandra review task TW #36659998 (due 2026-06-23).
- **2026-05-28** — `/services/land-clearing` focused sub-page targeting the "land clearing ogden" Map Pack gap query (option C from session: coexists with combined `/services/grading-land-clearing` hub, no redirect). Live and verified at https://accuriteexcavation.com/services/land-clearing.
- **2026-05-28** — GBP categories overhauled with Shawn from 4 → 7 (Excavating contractor primary; +Drainage service, Trucking company, Earth works company; kept Septic system service, Demolition contractor, Retaining wall supplier). Picker is now maxed for Excavating-contractor primary — see `~/.claude/projects/-Users-rosswalker-projects-accurite-excavation/memory/reference_accurite_gbp_categories.md`.
- Monthly SEO report pipeline end-to-end: leads extractor, GBP stub client, Jinja2/WeasyPrint PDF template (AccuRite gold `#E8C840` / charcoal `#333333`), GSC wiring via existing `GSCClient`, positive-framing visibility table, launchd wrapper. All in `/Users/rosswalker/projects/3sm_code/monthly-reports/accurite/`.
- April client report delivered: 4 qualified leads (+100% vs March), 82 clicks (+61%), 10,913 impressions (+205%), 597 unique queries ranking (+90%). PDF at `~/Documents/accurite-reports/accurite-seo-2026-04.pdf`.
- Project-scoped memory bootstrapped at `~/.claude/projects/-Users-rosswalker-projects-accurite-excavation/memory/` with `MEMORY.md` index and `feedback_monthly_report_positive_framing.md` standing rule.
- Homepage CTR title/meta rewrite merged to main (`16f79a0`).
- Memory system adopted: daily notes in `docs/memory/`, SessionEnd memory-keeper agent, session-start context loader, audit-brief / audit-memory commands.

## Long-running in-flight items — full text

Abbreviated in `docs/stage-current.md` on 2026-07-30 to fit the byte cap.
These are still IN FLIGHT, not shipped. Verbatim originals:

- Re-check the homepage CTR title/meta rewrite (commit `16f79a0`) after the May 2026 Google core update finishes (~early June; started 2026-05-21). 2026-05-22 evaluation: title/meta confirmed live; CTR test is unmeasurable (~0-1 clicks/window); decision = **keep, don't revert**. 2026-05-28 mid-update checkpoint: "excavation company" organic recovering toward #1 (3 of 4 post-baseline days at #1) but impressions too thin to call; Map Pack steady (Ogden #1, Pleasant View #3, Layton improved #4→#3). Re-pull post-rollout. (Tracked in Shawn Durrant Teamwork tasks 36495489 / 36495490, both now closed.)
- **Blog indexation follow-up:** TW #36664201 (Cassandra, Request Indexing for `/blog/excavation-safety-on-federal-projects` and `/blog/national-park-service-project`) is **DONE** — confirmed complete in Teamwork 2026-07-13. Still open: 3 posts are "crawled, currently not indexed" (`avoid-flooding-new-home`, `retaining-wall-permit-utah`, `retaining-wall-types-utah-soil`) — Google's quality decision, not a discovery gap; fixing needs content depth, not resubmission. Not yet scoped.

---

## Moved 2026-08-11

Moved out of `docs/stage-current.md` — completed or superseded by the 2026-08-11
session. Verbatim originals.

### Completed — GBP weekly post verification (was "In flight")

- **Verify the GBP post routine fires Tuesday 2026-07-21** — first run after the 2026-07-17 migration to a **local launchd job** (`com.rosswalker.accurite-gbp-weekly`). The 07-13 MCP→REST fix did NOT work: 07-14 also produced no task, because the claude.ai cloud sandbox blocks outbound egress to `csfund.teamwork.com` (not a token problem). Confirm a task lands in project 628283 after 12:03 PM Tue; the runner pings via `~/.local/bin/notify` on failure. See memory `reference_gbp_weekly_routine.md`.

**Outcome:** confirmed working. `.claude/skills/gbp-post/post-log.md` records four
consecutive Tuesday posts — 2026-07-21 (TW 36817398), 07-28 (TW 36853273), 08-04
(TW 36893596), 08-11 (TW 36926145). The launchd migration held.

### Completed — first automated monthly report run (was "In flight")

- Monitor the first fully-automated monthly report run on **2026-06-01 at 8am local** — confirm `launchd` fires cleanly and the May report lands as a Teamwork task.

**Outcome (2026-08-11): it never worked, and had never worked.** `run-monthly.sh`
passed `--channels plugin:telegram@claude-plugins-official`, a flag the Claude Code CLI
does not have, so the binary exited during argument parsing before reading `ROUTINE.md`.
`~/Library/Logs/accurite-monthly-report.log` contains exactly three entries — 2026-06-01,
07-01, 08-01 — each a "run start" followed by `error: unknown option '--channels'`. The
May 2026 report was therefore never generated at all; June was built by hand on
2026-07-03 and July by hand on 2026-08-11. Flag removed in commit `6d71521`. The fix is
unverified end-to-end because Claude Code refuses to nest inside another Claude Code
session; the real test is the 2026-09-01 08:00 run.

### Superseded — GBP API approval as a blocker (was "Blocked / waiting on")

- **Google Business Profile API approval.** Ross submitted the access form 2026-05-12 at https://support.google.com/business/contact/api_default using ross@rossjwalker.com. Status: pending. GBP stub client returns zeros until approved. Follow-up Teamwork task #36440438 holds the exact prompt to paste once access lands (due 2026-05-17).

**Superseded 2026-08-11.** Ross's call: approval is probably never coming, and he has
manual dashboard access anyway. The report's GBP section no longer depends on it —
commit `4e4709f` feeds it from an optional `gbp` block in `data.json` (hand-entered
calls / direction requests / profile views) plus an automatic public review pull via
`pull_gbp_reviews.py`. The dormant API path remains and would take over on its own if
approval ever landed. Teamwork task 36440438 is now obsolete and still sitting open in
the old R&R tasklist 2518534.

---

## Moved 2026-08-11 (second wrap of the day)

### `/services/land-clearing` indexation re-check — RESOLVED 2026-08-11
Item as it stood: *"Re-check `/services/land-clearing` (shipped 2026-05-28) indexation +
'land clearing ogden' impressions in GSC in ~10-14 days. If page picks up impressions,
validate split-out strategy and consider parallel `/services/grading` split."*

**Answered by the 90-day GSC pull on 2026-08-11** (`research/keywords/gsc-gap-clearing-grading-2026-08-11.txt`):
`land clearing ogden` 97 impressions @ position 11.6, `land clearing services ogden` 64 @ 14.9,
`land clearing kaysville` 47 @ 9.7, `land clearing bountiful` 45 @ 4.4, `land clearing layton`
42 @ 3.8, `land clearing salt lake city` 40 @ 8.8, bare `land clearing` 34 @ 1.0. The page is
indexed and pulling impressions across the whole city set, so **the split-out strategy is
validated**. Clicks are still 0 across all of them — a position problem, not a discovery one.
The parallel `/services/grading` split remains an open option, never actioned.

### Map Pack monitoring — 2026-06-18 diagnosis detail
Superseded in the live doc by a one-line summary; the 2026-08-11 re-pull confirmed the same
diagnosis, so the original narrative is history rather than current state.

Ogden slipped #1→#2 for "excavation companies near me" (Skinner now #1), Pleasant View dropped
out, Layton still out; organic "excavation company" holds ~#1. Competitor review benchmark
(`research/local-pack/review-velocity-2026-06-18.json`) showed reviews are NOT the cause —
AccuRite led the cluster (60 reviews vs Skinner's 9, whose last review was Oct 2023).
Diagnosis: proximity near-tie within a tightly-clustered, same-category competitor set; the
Ogden slip likely post-core-update volatility, with the real loss at the edges (Pleasant
View/Layton). Next step offered and deferred by Ross on 06-18: a geo-grid Share-of-Local-Voice
scan to confirm real vs noise. Edge-city location-page deepening (Pleasant View/Layton/West
Haven) was identified as the durable in-house lever. See `docs/memory/2026-06-18.md`.

### Blog indexation follow-up — TW #36664201
TW #36664201 marked DONE 2026-07-13. The remaining open piece (3 posts "crawled, currently not
indexed") stays in the live stage doc.

## Moved 2026-08-13

Moved out of `docs/stage-current.md` during the 2026-08-13 wrap. Both "Recently shipped"
entries below were already detailed elsewhere in this file — these are the abbreviated
summaries that sat in the live doc. The closed in-flight item is recorded verbatim.

### Recently shipped — 2026-07-17 (abbreviated entry from the live doc)
- **2026-07-17** — GBP weekly post migrated off the claude.ai cloud routine to a local launchd job (`com.rosswalker.accurite-gbp-weekly`), Tuesday 12:03 local. Root cause of the outage: the cloud sandbox blocks outbound HTTPS to `csfund.teamwork.com`. Commit `c258b73`.

### Recently shipped — 2026-07-13 (abbreviated entry from the live doc)
- **2026-07-13** — Winter seasonal keyword research (research only, nothing live). Winter carries the most hire-intent demand of any season; demolition peaks in winter; drainage is warm-weather; "winter excavation" has no demand. Report `research/keyword-research/seasonal-demand.html`.

### In flight — closed item, `~/.claude` commit `878d750`
- ~~**Push `~/.claude` commit `878d750`**~~ — **CLOSED 2026-08-11.** The hash no longer exists in the repo (rewritten or amended); `~/.claude` HEAD equals `origin/main` with a clean tree, so the content shipped under a different hash. Nothing outstanding. Closure also recorded in `docs/memory/2026-08-12.md`.

### Recently shipped — 2026-08-11 (full entry from the live doc, moved 2026-08-13)
- **2026-08-11** — **First new blog post since July: `/blog/lot-clearing-and-grading-before-road-construction`** (1,461 words, drone video of the GPS dozer embedded). Targets `residential lot clearing and grading` (218 impr @ pos 13.4 in GSC 90d) and the site-clearing/site-preparation cluster — chosen because the *technical* vocabulary (grubbing, subgrade, GPS grading) has **no measurable Utah search demand**. Same session repaired three pre-existing site-wide faults: a dead OG image on 77 of 79 pages, two nonexistent service slugs linked from 4 location pages, and a missing apple-touch-icon. Also: `VideoObject` schema (frontmatter-driven, reusable), per-post OG images, and all 15 blog titles pulled under the ~60-char SERP limit by aligning the title suffix to the rest of the site. Commits `616430d`, `38fa172`, `34d8ec5`, `9348db5`, `fa86582`.

### Recently shipped — 2026-08-13 (full entry from the live doc, moved 2026-08-13)
- **2026-08-13** — Tone pass on `/blog/lot-clearing-and-grading-before-road-construction` (`d711f04`, verified live). Ross found the post read unfriendly and supplied a full rewrite; the rewrite was **not** shipped — measured against the live file it cut 1,453 words to 413, dropped the `residential lot clearing and grading` target phrase, removed all 13 internal links, stopped referencing the embedded video (orphaning its `VideoObject` schema), and claimed "3D … dozers" against the 2026-08-11 CONFIRMED entry in `docs/client-facts.md`. Actual cause was four sentences taking swings at other contractors; those were rewritten in place, Ross's seven descriptive H2s and his four-question list were adopted, and length held at 1,482 words. Heading anchor IDs changed — nothing in `src/`, `public/`, or `netlify.toml` linked to the old ones.
