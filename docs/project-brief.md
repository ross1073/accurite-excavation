# accurite-excavation — Project Brief

## What this project is

Client website and project hub for **AccuRite Excavation** (accuriteexcavation.com) — a Utah excavation contractor serving the Wasatch Front (Ogden corridor south to Riverton/Sandy). This is Ross's only real client site; every other repo under `~/projects/` is rank-and-rent that Ross owns. Changes here go live on someone else's business, so the rule is: move slowly, no experimental SEO or copy without explicit approval.

Active work is dominated by SEO maintenance (GSC 404 fixes, redirect cleanup, title/meta CTR rewrites, schema additions, lead-gen markup) plus a recurring monthly client SEO report. A project-scoped `gbp-post` skill (`.claude/skills/gbp-post/`) generates Google Business Profile posts for the business.

## How it's structured

**Stack**

- **Framework:** Astro 5 (static, `trailingSlash: 'never'`) — see `astro.config.mjs`
- **Styling:** Tailwind v4 via `@tailwindcss/vite`
- **Sitemap:** `@astrojs/sitemap`
- **Build:** `npm run build` → `dist/`
- **Hosting:** Netlify, auto-deploys on push to `main`. Redirects/headers in `netlify.toml`.
- **Repo:** `github.com/ross1073/accurite-excavation`. Direct push to `main` is the standard workflow (single-developer client site, accepted risk — see `.claude/settings.json`).

**Content layout**

- `src/pages/` — top-level routes: `index.astro`, `about`, `contact`, `free-estimate`, `gallery`, `reviews`, `safety`, `privacy-policy`, `terms`, `404`, `blog/`, plus dynamic catch-alls `services/[...slug].astro` and `locations/[...slug].astro`.
- `src/content/services/` — 11 service pages on disk (residential excavation, demolition, grading & land clearing, land clearing, hauling/delivery, rock & retaining walls, commercial projects, government projects, septic systems, underground utilities, water features & ponds). The standalone `land-clearing` page was added 2026-05-28 as a focused sub-page to target the "land clearing ogden" Map Pack gap query; the combined grading-land-clearing page remains as the topical hub.
- `src/content/locations/` — 40 Wasatch Front city pages (Ogden corridor + SLC south to Riverton/Sandy).
- `src/content/blog/` — 13 blog posts (cost guides, contractor evaluation, retaining walls, soil, EMOD, project case studies, excavation safety).
- `src/content/config.ts` — content collection schemas.
- `src/components/`, `src/layouts/`, `src/data/`, `src/styles/`, `src/assets/` — supporting code and assets.
- `plugins/` — local Astro/build plugins.
- `public/` — static assets, redirects file, IndexNow verification key, EMOD letter PDF, fonts/images/js.
- `dist/` — build output; never edit by hand.
- `research/` — competitor, keyword, migration research; planning material, not site content.
- `docs/` — project brief, stage doc, audit reports, memory daily notes, superpowers plans.

**Tooling around the site**

- Monthly branded PDF SEO report runs on the 1st of each month at 8am local via `launchd`, delivered as a Teamwork task assigned to Ross for review before forwarding to the client. Pipeline lives at `/Users/rosswalker/projects/3sm_code/monthly-reports/accurite/`. Standing rule: positive framing only — see project-scoped memory `feedback_monthly_report_positive_framing.md`.
- `.claude/skills/gbp-post/` — project-scoped skill for generating Google Business Profile posts. Runs automatically every Tuesday 12:03 PM local via `launchd` (`com.rosswalker.accurite-gbp-weekly` → `scripts/run-gbp-weekly.sh`), creating a Teamwork task for Cassandra to proof. Migrated 2026-07-17 off a claude.ai cloud routine, whose sandbox blocks outbound egress to Teamwork — see project-scoped memory `reference_cloud_routine_egress_limit.md`.
- `.claude/agents/memory-keeper.md` — SessionEnd agent that writes daily notes to `docs/memory/`.
- `.claude/hooks/` — `session-end-memory-keeper.sh`, `session-beacon.sh`. (`session-start-load-context.sh` is still on disk but was retired 2026-07-30 — context loading is global now.)
- `.claude/commands/` — `audit-brief`, `audit-memory`.

## Conventions

- **Deploy means live.** "Done" on any deploy task means the change is verified live on the production URL — not just pushed to git.
- **Netlify trailing-slash redirect uses `force = false`.** Setting it to `true` causes an infinite-loop on top-level pages (verified breakage in `d3a266d`, reverted 2026-04-17). The comment in `netlify.toml` explains; do not re-flip it.
- **www → non-www** consolidated in a single hop via explicit `netlify.toml` rules to shorten the http-www chain.
- **WP search URLs** (`/?s=`) are blocked at the redirect layer.
- **IndexNow key file** (`public/e03de1ac69fc4666a18fe5ec07b68436.txt`) must be served as-is with `force = true` 200 redirect.
- **`.html → clean URL` redirects** use 301 to prevent GSC duplicate indexing (see global `feedback_netlify_gsc_duplicates.md`).
- **Build output and planning dirs are off-limits for hand edits:** `dist/` is generated; `research/` and `docs/` are planning material, not site content.
- **Monthly client report: positive framing only.** Suppress avg-position drops and CTR drops from the visible table; show queries-ranking-count (growth metric) instead. Suppress sparkline until 4+ months of non-zero data.

## Memory system

Context auto-loads at SessionStart via four **global** hooks, `~/.claude/hooks/project-context-load-1..4.sh` (1 = time anchor + `docs/stage-current.md`, 2 = `docs/project-brief.md`, 3 = the per-project `MEMORY.md` index, 4 = recent `docs/memory/` daily notes — two if both fit, else the newest); the user profile (`~/.claude/user.md`) comes from a separate global hook, `memory-load.sh`. The ~10,000-byte SessionStart cap is **per hook, not per session**, so each part holds itself under 9,000 bytes and truncates an oversized file with a marker naming it and its full size — the rest is still on disk, never dropped to a pointer. More context means adding a part, never growing one. The repo-local `.claude/hooks/session-start-load-context.sh` was retired 2026-07-30 (unregistered, kept on disk with a dated header); it had no budget logic at all. Daily notes are written by the SessionEnd memory-keeper agent (`.claude/agents/memory-keeper.md`) — it appends a timestamped session block to `docs/memory/<YYYY-MM-DD>.md`, never overwriting prior days. The retired `docs/status.md` rolling file was migrated into the first dated note. `/audit-brief` is the manual drift check that compares the brief against the codebase and writes a severity-tagged findings file under `docs/audits/`.
