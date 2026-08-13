# accurite-excavation

Client website + project hub for **AccuRite Excavation**.

## Important — this is Ross's only client site

Every other folder under `~/projects/` is rank-and-rent (R&R) that Ross owns. AccuRite is a real client. That changes the rules: changes here go live on someone else's business. Move slowly. Don't ship experimental SEO tactics or copy changes without explicit approval. Memory: see `project_accurite_client.md` for client context, and `docs/memory/2026-05-22.md` (GSC + local-pack baseline), `docs/seo/accurite-directory-listings.md`, and `docs/seo/accurite-seo-action-plans.md` for current SEO state, fixes already shipped, and known constraints.

## Stack and deploy

- **Framework:** Astro (`astro.config.mjs`, `src/`, `public/`)
- **Repo:** `github.com/ross1073/accurite-excavation`
- **Deploy:** Netlify, auto-builds on push to `main`. `netlify.toml` holds redirects and headers.
- **Production URL:** verify the deploy succeeded on the live site before reporting any change as done — pushing to GitHub is not "done."

## Recurring work

Most recent work has been SEO maintenance: fixing GSC 404s, redirect cleanup, title/meta rewrites for CTR. Before adding new pages or rewriting copy, check `docs/memory/2026-05-22.md` (baseline numbers), `docs/seo/accurite-directory-listings.md`, and `docs/seo/accurite-seo-action-plans.md` so we don't undo a deliberate decision.

## Conventions

- `dist/` is build output, don't edit by hand.
- `research/` and `docs/` hold planning material, not site content.
- Netlify redirects: when adding `.html → clean URL` redirects, follow `feedback_netlify_gsc_duplicates.md` (always 301, prevent GSC duplicate indexing).

## Memory system

Context auto-loads at SessionStart via four **global** hooks, `~/.claude/hooks/project-context-load-1..4.sh` (1 = time anchor + `docs/stage-current.md`, 2 = `docs/project-brief.md`, 3 = the per-project `MEMORY.md` index, 4 = recent `docs/memory/` daily notes — two if both fit, else the newest); the user profile (`~/.claude/user.md`) comes from a separate global hook, `memory-load.sh`. The ~10,000-byte SessionStart cap is **per hook, not per session**, so each part holds itself under 9,000 bytes and truncates an oversized file with a marker naming it and its full size — the rest is still on disk, never dropped to a pointer. More context means adding a part, never growing one. The repo-local `.claude/hooks/session-start-load-context.sh` was retired 2026-07-30 (unregistered, kept on disk with a dated header); it had no budget logic at all. Daily notes are written by the SessionEnd memory-keeper agent (`.claude/agents/memory-keeper.md`) — it appends a timestamped session block to `docs/memory/<YYYY-MM-DD>.md`, never overwriting prior days. The retired `docs/status.md` rolling file was migrated into the first dated note. `/audit-brief` is the manual drift check that compares the brief against the codebase and writes a severity-tagged findings file under `docs/audits/`.


<!-- BRAIN-MANIFEST-START -->
## Brain library manifest

Generated 2026-08-13 by ~/projects/brain/scripts/manifest.py. Do not hand-edit — this block is regenerated in place. Read these with `/load`.

- `library/2026-08-13-glossary-three-step-marketing.html` — reference summary — entities: AccuRite Excavation

Library root: ~/projects/brain/
<!-- BRAIN-MANIFEST-END -->
