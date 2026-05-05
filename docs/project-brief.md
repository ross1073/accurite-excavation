# accurite-excavation — Project Brief

Client website for **AccuRite Excavation** (accuriteexcavation.com). This is Ross's only real client site — every other repo under `~/projects/` is rank-and-rent that he owns. Changes go live on someone else's business; move slowly, no experimental SEO/copy without approval.

## Stack

- **Framework:** Astro 5 (static, `trailingSlash: 'never'`)
- **Styling:** Tailwind v4 (via `@tailwindcss/vite`)
- **Sitemap:** `@astrojs/sitemap`
- **Build:** `npm run build` → `dist/`
- **Hosting:** Netlify, auto-deploys on push to `main`. Redirects/headers in `netlify.toml`.
- **Repo:** `github.com/ross1073/accurite-excavation`. Direct push to `main` is the standard workflow (single-developer client site, accepted risk — see `.claude/settings.json` autoMode allow rule).

## Content layout

- `src/pages/` — top-level routes: `index.astro`, `about`, `contact`, `free-estimate`, `gallery`, `reviews`, `safety`, `privacy-policy`, `terms`, `404`, `blog/`, plus dynamic catch-alls `services/[...slug].astro` and `locations/[...slug].astro`.
- `src/content/services/` — 10 service pages (residential excavation, demolition, grading & land clearing, septic, retaining walls, water features/ponds, underground utilities, hauling, commercial projects, government projects).
- `src/content/locations/` — Wasatch Front city pages (Ogden corridor + SLC south to Riverton/Sandy).
- `src/content/blog/` — blog content collection.
- `src/content/config.ts` — content collection schemas.
- `src/components/`, `src/layouts/`, `src/data/`, `src/styles/` — supporting code.
- `dist/` — build output, never edit by hand.
- `research/`, `docs/` — planning material, not site content.
- `plugins/` — local Astro/build plugins.

## Recurring work

SEO maintenance dominates: GSC 404 fixes, redirect cleanup, title/meta CTR rewrites, lead-gen markup (DNI, basement content). Recent commits hit homepage CTR rewrite (16f79a0), 404 fixes for grading-and-site-prep / commercial-excavation (3aefbdf), redirect-loop fix + www consolidation (c33f8b9), and meta robots additions.

## Conventions / gotchas

- Netlify trailing-slash redirect uses `force = false`. Setting it to `true` causes infinite-loop on top-level pages (verified breakage in d3a266d, reverted 2026-04-17). Comment in `netlify.toml` explains.
- Single-hop www → non-www handled in `netlify.toml` to shorten the http-www chain.
- WP search URLs (`/?s=`) are blocked at the redirect layer.
- IndexNow key file (`public/e03de1ac69fc4666a18fe5ec07b68436.txt`) must be served as-is with `force = true` 200 redirect.
- When adding `.html → clean URL` redirects, use 301 to prevent GSC duplicate indexing (see global feedback file).
- "Done" on any deploy task means the change is live on the production URL — not just pushed.

## Project memory

User-scoped memory lives at `~/.claude/projects/-Users-rosswalker/memory/`:
- `project_accurite_client.md` — client context, rules of engagement.
- `project_accurite_seo_state.md` — current SEO state, fixes shipped, known constraints. Read before any new pages or copy rewrites.
