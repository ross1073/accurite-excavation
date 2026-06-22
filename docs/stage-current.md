# Stage — current

## Current focus

Monthly SEO report pipeline is live and shipped its first run (April report delivered as Teamwork task #36440380). Site-side work remains in SEO maintenance mode — GSC 404 fixes, redirect cleanup, title/meta CTR rewrites. No active feature work on the Astro site itself.

## In flight

- Re-check the homepage CTR title/meta rewrite (commit `16f79a0`) after the May 2026 Google core update finishes (~early June; started 2026-05-21). 2026-05-22 evaluation: title/meta confirmed live; CTR test is unmeasurable (~0-1 clicks/window); decision = **keep, don't revert**. 2026-05-28 mid-update checkpoint: "excavation company" organic recovering toward #1 (3 of 4 post-baseline days at #1) but impressions too thin to call; Map Pack steady (Ogden #1, Pleasant View #3, Layton improved #4→#3). Re-pull post-rollout. (Tracked in Shawn Durrant Teamwork tasks 36495489 / 36495490, both now closed.)
- Monitor the first fully-automated monthly report run on **2026-06-01 at 8am local** — confirm `launchd` fires cleanly and the May report lands as a Teamwork task.
- Re-check `/services/land-clearing` (shipped 2026-05-28) indexation + "land clearing ogden" impressions in GSC in ~10-14 days. If page picks up impressions, validate split-out strategy and consider parallel `/services/grading` split.
- **Map Pack monitoring (2026-06-18 re-pull):** Ogden slipped #1→#2 for "excavation companies near me" (Skinner now #1), Pleasant View dropped out, Layton still out; organic "excavation company" holds ~#1. Competitor review benchmark (`research/local-pack/review-velocity-2026-06-18.json`) shows reviews are NOT the cause — AccuRite leads the cluster (60 reviews vs Skinner's 9, last review Oct 2023). Diagnosis = proximity near-tie within a tightly-clustered, same-category competitor set; Ogden slip likely post-core-update volatility, real loss is at the edges (Pleasant View/Layton). **Next:** geo-grid Share-of-Local-Voice scan (offered, deferred by Ross 06-18) to confirm real vs noise; edge-city location-page deepening (Pleasant View/Layton/West Haven) is the durable in-house lever. See `docs/memory/2026-06-18.md`.

## Recently shipped

- **2026-06-22** — HHI Corporation safety letter (Hill AFB B1286 Steam Plant) added across the site: new human-first blog post `/blog/excavation-safety-on-federal-projects` + proof sections on `/safety`, `/services/government-projects`, the existing Hill AFB post, and an HHI testimonial in `reviews.json` (renders on `/reviews`, `/services/government-projects`, `/locations/layton`). Commit `9bef056`, verified live. Keyword research (`research/keyword-research/`) confirmed the angle is an E-E-A-T/conversion asset, not a traffic play. Cassandra review task TW #36659998 (due 2026-06-23).
- **2026-05-28** — `/services/land-clearing` focused sub-page targeting the "land clearing ogden" Map Pack gap query (option C from session: coexists with combined `/services/grading-land-clearing` hub, no redirect). Live and verified at https://accuriteexcavation.com/services/land-clearing.
- **2026-05-28** — GBP categories overhauled with Shawn from 4 → 7 (Excavating contractor primary; +Drainage service, Trucking company, Earth works company; kept Septic system service, Demolition contractor, Retaining wall supplier). Picker is now maxed for Excavating-contractor primary — see `~/.claude/projects/-Users-rosswalker-projects-accurite-excavation/memory/reference_accurite_gbp_categories.md`.
- Monthly SEO report pipeline end-to-end: leads extractor, GBP stub client, Jinja2/WeasyPrint PDF template (AccuRite gold `#E8C840` / charcoal `#333333`), GSC wiring via existing `GSCClient`, positive-framing visibility table, launchd wrapper. All in `/Users/rosswalker/projects/3sm_code/monthly-reports/accurite/`.
- April client report delivered: 4 qualified leads (+100% vs March), 82 clicks (+61%), 10,913 impressions (+205%), 597 unique queries ranking (+90%). PDF at `~/Documents/accurite-reports/accurite-seo-2026-04.pdf`.
- Project-scoped memory bootstrapped at `~/.claude/projects/-Users-rosswalker-projects-accurite-excavation/memory/` with `MEMORY.md` index and `feedback_monthly_report_positive_framing.md` standing rule.
- Homepage CTR title/meta rewrite merged to main (`16f79a0`).
- Memory system adopted: daily notes in `docs/memory/`, SessionEnd memory-keeper agent, session-start context loader, audit-brief / audit-memory commands.

## Blocked / waiting on

- **Google Business Profile API approval.** Ross submitted the access form 2026-05-12 at https://support.google.com/business/contact/api_default using ross@rossjwalker.com. Status: pending. GBP stub client returns zeros until approved. Follow-up Teamwork task #36440438 holds the exact prompt to paste once access lands (due 2026-05-17).
- PDF → Drive upload helper: deferred. PDFs are currently delivered as absolute local paths in the Teamwork task body because the Teamwork MCP in that session had no file-upload tool. Pick up only if Ross wants attachments instead of references.

## Notes

- `gbp-post` skill at `.claude/skills/gbp-post/` is the project-scoped tool for generating Google Business Profile posts — separate from the monthly report pipeline.
- Standing rule on the monthly client report: only good news. Suppress avg-position and CTR drops from the visible table; show queries-ranking-count instead; suppress sparkline until 4+ months of non-zero data.
- Site is a real client property — don't ship experimental SEO or copy changes without explicit approval from Ross.
- "Done" on a deploy task means verified live on the production URL, not just pushed to main.
