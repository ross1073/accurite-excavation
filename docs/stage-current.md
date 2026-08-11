# Stage — current

## Current focus

Site-side work remains in SEO maintenance mode — GSC 404 fixes, redirect cleanup, title/meta CTR rewrites. No active feature work on the Astro site itself. The monthly SEO report has shipped for April, June and July; **May was never generated** and every report so far was built by hand — the launchd automation was broken from its first run until 2026-08-11.

**New (2026-07-13):** winter content planning. Research is done (see "Recently shipped"); no content has been written or shipped. The open question is which winter lane to build first, and that decision is gated on the two items at the top of "In flight."

## In flight

- **Trenchless or open-cut? (2026-07-13, unanswered)** — Does Shawn do trenchless sewer work, or open-cut only? All trenchless/no-dig keywords (~300–400 winter searches) were excluded from the winter analysis on the assumption AccuRite is open-cut. That assumption is unconfirmed and blocks any sewer-line copy. See `~/.claude/projects/-Users-rosswalker-projects-accurite-excavation/memory/reference_accurite_service_scope.md`.
- **Verify the sewer spike before building on it (2026-07-13)** — `sewer line repair near me` reports 1,900 searches in Feb against a 480/mo average. That single reading is ~80% of the sewer bucket's winter total and is uncorroborated. Cross-check in Google Keyword Planner. If it's a DataForSEO artifact, sewer deflates to ~1,900 and **excavation becomes the largest winter lane instead of sewer**, changing which page gets built first.
- **Winter content needs to be live by ~early October** to index and rank before the Jan–Feb peak. That timing estimate is Claude's rule of thumb (8–12 weeks to settle), not a measured figure for this site.
- **Verify the monthly report fires 2026-09-01 at 8am** — the launchd job had never once succeeded (three runs, all killed by a nonexistent `--channels` flag, removed 2026-08-11 in `6d71521`). This is the first run that can actually work. Success = a task in project 210055 / tasklist Inbox. The fix could not be tested from a session because Claude Code refuses to nest inside itself. (History: `docs/stage-history.md`)
- **Push `~/.claude` commit `878d750`** — committed locally, not pushed (Auto Mode blocked it). Contains `bin/tw` and the global Teamwork skill/memory updates.

- Re-check the homepage CTR title/meta rewrite (`16f79a0`) after the May 2026 core update. 2026-05-22 decision: **keep, don't revert** (CTR unmeasurable at ~0-1 clicks/window). Re-pull post-rollout. Full evaluation notes in `docs/stage-history.md`.
- **Lead tagging keeps silently breaking.** AccuRite rows stop carrying the "Accurite Excavation" domain tag in the leads sheet, so the monthly count reads low until Ross re-tags by hand. Broke after 2026-05-08, fixed 07-03; broke again after 07-02, fixed 08-11 (July went 2 → 4). The capture side has never been touched. Expect it again in September. Side effect: the 08-11 re-tag also moved June from 5 to 6, so the already-shipped June report (5) disagrees with current data.
- **Decide whether to backfill the May 2026 report** — never generated, because the launchd job was broken from its first run.
- Re-check `/services/land-clearing` (shipped 2026-05-28) indexation + "land clearing ogden" impressions in GSC in ~10-14 days. If page picks up impressions, validate split-out strategy and consider parallel `/services/grading` split.
- **Blog indexation follow-up:** TW #36664201 is DONE (2026-07-13). Still open: 3 posts "crawled, currently not indexed" — a quality decision, not a discovery gap; needs content depth, not resubmission. Not yet scoped. Full text in `docs/stage-history.md`.
- **Map Pack monitoring (2026-06-18 re-pull):** Ogden slipped #1→#2 for "excavation companies near me" (Skinner now #1), Pleasant View dropped out, Layton still out; organic "excavation company" holds ~#1. Competitor review benchmark (`research/local-pack/review-velocity-2026-06-18.json`) shows reviews are NOT the cause — AccuRite leads the cluster (60 reviews vs Skinner's 9, last review Oct 2023). Diagnosis = proximity near-tie within a tightly-clustered, same-category competitor set; Ogden slip likely post-core-update volatility, real loss is at the edges (Pleasant View/Layton). **Next:** geo-grid Share-of-Local-Voice scan (offered, deferred by Ross 06-18) to confirm real vs noise; edge-city location-page deepening (Pleasant View/Layton/West Haven) is the durable in-house lever. See `docs/memory/2026-06-18.md`.
  **2026-08-11 re-pull** (`research/local-pack/review-velocity-2026-08-11.json`): AccuRite 61 reviews / 4.9 / rank 2, one new review on 07-31; Skinner still rank 1 on 9 reviews with nothing since 2023-10-26; Triple H rank 4 on 11. Two months on, the review gap remains enormous and is still not the lever — the diagnosis above holds.

## Recently shipped

Full history moved to `docs/stage-history.md` on 2026-07-30 (verbatim, nothing
deleted) so this doc fits the SessionStart per-hook byte cap. Two most recent,
abbreviated:

- **2026-07-17** — GBP weekly post migrated off the claude.ai cloud routine to a local launchd job (`com.rosswalker.accurite-gbp-weekly`), Tuesday 12:03 local. Root cause of the outage: the cloud sandbox blocks outbound HTTPS to `csfund.teamwork.com`. Commit `c258b73`. Details in `docs/stage-history.md`.
- **2026-07-13** — Winter seasonal keyword research (research only, nothing live). Winter carries the most hire-intent demand of any season; demolition peaks in winter; drainage is warm-weather; "winter excavation" has no demand. Report `research/keyword-research/seasonal-demand.html`. Details in `docs/stage-history.md`.

## Blocked / waiting on

- PDF → Drive upload helper: deferred. PDFs are currently delivered as absolute local paths in the Teamwork task body because the Teamwork MCP in that session had no file-upload tool. Pick up only if Ross wants attachments instead of references.

## Notes

- `gbp-post` skill at `.claude/skills/gbp-post/` is the project-scoped tool for generating Google Business Profile posts — separate from the monthly report pipeline.
- Standing rule on the monthly client report: only good news. Suppress avg-position and CTR drops from the visible table; show queries-ranking-count instead; suppress sparkline until 4+ months of non-zero data.
- Site is a real client property — don't ship experimental SEO or copy changes without explicit approval from Ross.
- "Done" on a deploy task means verified live on the production URL, not just pushed to main.
