# accurite-excavation

Client website + project hub for **AccuRite Excavation**.

## Important — this is Ross's only client site

Every other folder under `~/projects/` is rank-and-rent (R&R) that Ross owns. AccuRite is a real client. That changes the rules: changes here go live on someone else's business. Move slowly. Don't ship experimental SEO tactics or copy changes without explicit approval. Memory: see `project_accurite_client.md` and `project_accurite_seo_state.md` for current SEO state, fixes already shipped, and known constraints.

## Stack and deploy

- **Framework:** Astro (`astro.config.mjs`, `src/`, `public/`)
- **Repo:** `github.com/ross1073/accurite-excavation`
- **Deploy:** Netlify, auto-builds on push to `main`. `netlify.toml` holds redirects and headers.
- **Production URL:** verify the deploy succeeded on the live site before reporting any change as done — pushing to GitHub is not "done."

## Recurring work

Most recent work has been SEO maintenance: fixing GSC 404s, redirect cleanup, title/meta rewrites for CTR. Before adding new pages or rewriting copy, check `project_accurite_seo_state.md` so we don't undo a deliberate decision.

## Conventions

- `dist/` is build output, don't edit by hand.
- `research/` and `docs/` hold planning material, not site content.
- Netlify redirects: when adding `.html → clean URL` redirects, follow `feedback_netlify_gsc_duplicates.md` (always 301, prevent GSC duplicate indexing).

## Memory system

The project brief and `docs/status.md` auto-load into context via a SessionStart hook (`.claude/hooks/session-start-load-context.sh`). Status updates are written by the SessionEnd memory-keeper agent (`.claude/agents/memory-keeper.md`) — it folds each session's decisions, closures, and new open items into `docs/status.md` directly. `/audit-brief` is the manual drift check that compares the brief against the codebase and writes a severity-tagged findings file under `docs/audits/`.
