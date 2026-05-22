# Four Systems Pilot — AccuRite Excavation

**Status:** Planning (not started)
**Created:** 2026-05-08
**Owner:** Ross Walker
**Pilot site:** accuriteexcavation.com
**Source repo:** https://github.com/NicoSKOOL/the-four-systems

## Goal

Stand up an AI-assisted, human-in-the-loop content + refresh system on AccuRite. Run it for 60 days. Measure GSC clicks/impressions delta. Decide afterward whether to roll the pattern out to the strongest R&R sites.

Success = (a) the loop runs reliably each week without Ross babysitting it, (b) GSC clicks for new + refreshed pages show measurable lift over the 60-day window, (c) the client deliverable is something Ross can show.

Out of scope for the pilot: rolling this out to any R&R site, automating GBP/ads, multi-site orchestration. Those are Phase 2 decisions made *after* the 60-day measurement.

## Why AccuRite first (not an R&R site)

- Real operator experience to inject (Three Kings / E-E-A-T patterns actually apply).
- Already on Astro → `publish-to-astro.py` works without porting.
- GSC, GBP, ad tracking, real CMS-style site — supporting infra exists.
- Client work amortizes setup cost; ongoing content is a defensible deliverable.
- Excavation has real informational search volume (French drains, grading, frost line, septic install, retaining walls).

## Architecture decisions (locked before kickoff)

1. **Install location:** `~/projects/accurite-excavation/four-systems/` (subfolder inside the existing Astro repo). Keeps state, prompts, and skills colocated with the site they operate on. Skills get scoped to the project via `.claude/` at the AccuRite root.
2. **Mode:** Interactive only. **No cron, no launchd, no `--dangerously-skip-permissions`.** Every post is human-approved before publish. Non-negotiable for client work.
3. **Cadence:**
   - System 1 (keyword research): on demand, when topical coverage gap appears
   - System 2 (content writer): 1 post/week, interactive
   - System 3 (onsite audit): monthly
   - System 4 (refresh recommender): monthly
4. **Publishing:** Draft to markdown → Ross reviews → Ross approves → publish via Astro script → Netlify deploys → verify live.
5. **Keyword research source of truth:** Use the four-systems keyword-researcher for *this site*. Do NOT cross-pollinate with `~/seomachine/` outputs. AccuRite already has its own research; we extend it inside the four-systems bank.
6. **Cost ceiling:** Expect $5–10/month combined (DataForSEO + Anthropic API). Hard cap: if monthly spend exceeds $25, pause and review.

## Required skills, accounts, credentials

Ross must have these working before kickoff. Most already exist; flagged ones need verification.

| Item | Status | Notes |
|---|---|---|
| Claude Code installed, working in AccuRite repo | ✅ have | |
| DataForSEO account + API credentials | ⚠️ verify | Used by 4 of the 5 skills. ~$2–5/mo |
| Google Search Console access for accuriteexcavation.com | ✅ have | |
| GSC MCP server configured in Claude Code | ⚠️ verify | Required for refresh-recommender |
| Anthropic API key (for any background/scripted runs) | ✅ have | Interactive runs use Ross's CC session |
| Astro dev environment functional (`npm run dev`) | ✅ have | |
| Netlify deploy verified working | ✅ have | |
| Git clean on AccuRite main branch | check at kickoff | |

## Plan — sequenced

Each phase has clear "Ross does X" / "Claude does Y" splits. Don't execute any of this yet.

---

### Phase 0 — Prerequisites (Ross, ~30 min)

**Ross:**
1. Verify DataForSEO credentials are active and you remember where they're stored.
2. Verify GSC MCP is configured in `~/.claude/settings.json` (or wherever your MCP config lives) and authenticated for `accuriteexcavation.com`.
3. Confirm AccuRite git working tree is clean; create a branch `four-systems-pilot` for the install.
4. Decide: keep four-systems as a subfolder of the AccuRite repo (recommended) or as a sibling folder. Plan assumes subfolder.

**Claude:** nothing. This is gate-check work that needs Ross's hands on credentials.

---

### Phase 1 — Install + scope (Claude, ~30 min wall-clock)

**Claude:**
1. Clone `NicoSKOOL/the-four-systems` into `~/projects/accurite-excavation/four-systems/`.
2. Wire `.mcp.json` with DataForSEO + GSC creds (Ross provides values).
3. Wire `.claude/settings.local.json` with the tool allowlist.
4. Verify the 5 skills register in this Claude Code session (they live under `four-systems/.claude/skills/`).
5. Read every prompt file (`prompts/*.md`) and every skill file end-to-end. Report back what each one expects and any rules that conflict with AccuRite's existing voice/conventions.
6. Inspect `publish-to-astro.py` and confirm it matches AccuRite's `src/content/` collection structure. If mismatch, document required changes (don't apply yet).

**Ross:**
- Hand Claude the DataForSEO credentials when asked.
- Review Claude's report on prompt rules vs. AccuRite voice; flag anything to override.

**Exit criteria:** Skills load, MCPs respond, Claude has read everything and produced a one-page "what's installed and how it'll behave" summary.

---

### Phase 2 — Context bootstrap (Ross + Claude, ~30 min interactive)

**Claude:**
1. Run the `context-bootstrapper` skill. It interviews Ross for 15–20 minutes and writes 8 business-context files into `four-systems/context/`.
2. After interview: cross-reference the generated context against AccuRite's existing `docs/project-brief.md` and `research/` folder. Flag contradictions for Ross.

**Ross:**
- Sit through the interview. Answer honestly about: services, geography, ICP, differentiators, voice, what AccuRite has actually done (job stories), what *not* to claim.
- Resolve any contradictions Claude flags.

**Exit criteria:** 8 context files exist, Ross has reviewed them, no fabricated claims.

---

### Phase 3 — Voice + brand calibration (Ross + Claude, ~45 min)

This phase doesn't exist in the upstream repo. Adding it because client work demands it.

**Claude:**
1. Read 3–5 existing AccuRite blog/service pages and extract: tone, sentence length, technical depth, how Ross-the-operator's voice reads.
2. Append a `context/voice.md` file with concrete rules: vocabulary to use, vocabulary to avoid, when to be technical vs. plain, how to reference experience.
3. Add an explicit "do not fabricate" addendum to the content-writer prompt, calling out specific AccuRite-relevant traps (don't claim certifications we don't have, don't invent customer stories, don't promise outcomes).

**Ross:**
- Review the extracted voice rules. Edit them. This is the single highest-leverage human input in the whole pilot.

**Exit criteria:** `voice.md` exists and Ross has signed off on it.

---

### Phase 4 — System 1 dry run: keyword research (Claude, ~15 min)

**Claude:**
1. Run the `keyword-researcher` skill on a seed Ross picks (suggested: "french drain installation [region]" or "site grading cost").
2. Generate the keyword bank, content queue, dashboard.
3. Show Ross the dashboard.

**Ross:**
- Pick the seed.
- Review queued items. Reject anything that's not actually a fit. Make sure the priority-1 queue is content you'd be proud to publish.

**Exit criteria:** Keyword bank populated, content queue has 5–10 priority-1 items Ross approves of, dashboard renders.

---

### Phase 5 — System 2 dry run: write one post (Ross + Claude, ~45 min interactive)

**Claude:**
1. Run the `content-writer` skill. Pull top queue item.
2. Walk Ross through the 5-step interactive workflow: brief → research → outline → draft → review.
3. Save to `four-systems/output/posts/<slug>.md`. Do **not** publish yet.

**Ross:**
- Approve sources, outline, and draft at each checkpoint.
- Inject experience callouts at the brief stage — this is what makes the post different from generic AI slop.
- Read the final draft end-to-end before approving publish.

**Exit criteria:** One markdown post drafted to AccuRite voice, reviewed, and ready to publish — but not yet published.

---

### Phase 6 — Publish path validation (Claude, ~15 min)

**Claude:**
1. Run `publish-to-astro.py` against the Phase 5 draft.
2. Verify it lands in the correct `src/content/` collection with correct frontmatter.
3. Run `npm run build` locally; fix any build errors.
4. Push to a preview branch; let Netlify generate a deploy preview.

**Ross:**
- Review the deploy preview URL. Approve or reject.
- If approved: merge to main, verify live on production URL, confirm "done" per AccuRite's standard.

**Exit criteria:** First post is **live on accuriteexcavation.com** and verified by Ross.

---

### Phase 7 — System 3 dry run: onsite audit (Claude, ~10 min)

**Claude:**
1. Run the `onsite-audit` skill against accuriteexcavation.com.
2. Generate the report and dashboard view.
3. Sort findings by impact and propose a fix order.

**Ross:**
- Review findings. Decide which to fix now vs. backlog.

**Exit criteria:** Audit report exists, fix list prioritized, dashboard updated.

---

### Phase 8 — System 4 dry run: refresh recommender (Claude, ~10 min)

**Claude:**
1. Run the `refresh-recommender` skill. Pull GSC data; identify pages older than 12 months and pages with status "crawled, currently not indexed".
2. Score and recommend actions: rewrite, expand, consolidate, leave-alone.

**Ross:**
- Review the recommendation list. Approve which (if any) to rewrite this cycle.

**Exit criteria:** Refresh list exists; at minimum, the highest-priority "crawled, not indexed" page has a rewrite plan.

---

### Phase 9 — Cadence + measurement (Ross, ongoing 60 days)

**Ross:**
- Week 1: Phases 0–8 complete. First post live.
- Weeks 2–8: One post/week using System 2 in interactive mode. Each post: Ross sets aside ~45 min on a fixed day (suggested: Monday morning, aligns with existing Monday brief habit).
- Week 4 and Week 8: Re-run Systems 3 and 4. Apply at least one refresh per cycle.
- Daily: glance at the dashboard.

**Claude:**
- Each weekly run: execute System 2 interactively when Ross invokes it.
- Each monthly run: execute Systems 3 and 4 when Ross invokes it.
- Append session notes to `docs/memory/<date>.md` per existing memory-keeper convention.

**Measurement:**
- Baseline GSC snapshot taken at end of Phase 1 (before any new content lands).
- Day 30 and Day 60 GSC snapshots: total clicks, impressions, indexed page count, average position for target keywords.
- Compare deltas. Document in `docs/four-systems-pilot-results.md`.

**Exit criteria for the pilot:** 8 weeks elapsed, 6–8 new posts published, 1–3 refreshes shipped, GSC delta documented, go/no-go decision made on Phase 2 rollout.

---

## Timeline summary

| Phase | Owner | Wall-clock | Calendar |
|---|---|---|---|
| 0. Prereqs | Ross | 30 min | Day 1 |
| 1. Install + scope | Claude | 30 min | Day 1 |
| 2. Context bootstrap | Both | 30 min | Day 1 |
| 3. Voice calibration | Both | 45 min | Day 1–2 |
| 4. System 1 dry run | Both | 15 min | Day 2 |
| 5. System 2 dry run | Both | 45 min | Day 2 |
| 6. Publish validation | Both | 15 min | Day 2 |
| 7. System 3 dry run | Both | 10 min | Day 2 |
| 8. System 4 dry run | Both | 10 min | Day 2 |
| 9. Cadence | Ross | ~45 min/week | Weeks 2–8 |

**Total kickoff time:** ~3.5 hours over 1–2 days, then ~45 min/week for 8 weeks.

## Risks + mitigations

| Risk | Likelihood | Mitigation |
|---|---|---|
| Generated content damages AccuRite's reputation | Med | Interactive-only mode; Ross approves every post; voice.md guardrails; never auto-publish |
| Astro publisher script breaks against AccuRite's content collection schema | Med | Phase 1 inspects it before use; Phase 6 validates end-to-end before going live |
| DataForSEO costs balloon | Low | $25/mo cap; pause and review if exceeded |
| Pilot drags past 60 days without measurement | Med | Day 30 + Day 60 GSC snapshots are calendar-blocked, not optional |
| Conflict with existing AccuRite SEO work or `~/seomachine` outputs | Low | Four-systems is scoped to its own subfolder; no cross-pollination |
| Cron/automation creep (someone wires it to launchd "just to try") | Low | Documented as non-negotiable: interactive only for this client |

## Decision points

- **End of Phase 6:** First post is live. If it embarrassed Ross or required heavy rewrites at the draft stage, stop and recalibrate voice.md before continuing.
- **Day 30:** Mid-pilot check. If GSC is dead-flat *and* the workflow feels like a slog, consider stopping early.
- **Day 60:** Go/no-go on Phase 2 (rollout to R&R sites). Criteria for "go": measurable GSC lift, workflow felt sustainable, no client complaints.

## What's explicitly NOT in this plan

- Rolling out to any R&R site. That's a separate plan written after the 60-day measurement.
- Automated/scheduled runs. Cron is off the table for client work.
- Cross-pollinating with `~/seomachine/`. Keep them separate.
- Replacing existing AccuRite SEO work. This augments; it doesn't replace.
- Multi-tenant or multi-site orchestration. Single site, single keyword bank, single queue.
