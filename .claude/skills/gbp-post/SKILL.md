---
name: gbp-post
description: Use when generating a Google Business Profile post for AccuRite Excavation. Invoke with /gbp-post or when asked to create a GBP post, social media post, or Google Business update. Generates the post, picks a real photo from the website, and creates a Teamwork task for Cassandra to proof and approve.
---

# GBP Post Generator — AccuRite Excavation

Generate a ready-to-paste Google Business Profile post for AccuRite Excavation & Hauling, name a real photo from the website for it, and route it to Cassandra in Teamwork for proofreading + approval. Posts are informational only — no advertising, no calls to action, and never any invented facts.

## Usage

`/gbp-post` — generates the next post in the rotation
`/gbp-post educational` — educational / know-before-you-dig post
`/gbp-post seasonal` — seasonal tip post
`/gbp-post service "demolition"` — service highlight post
`/gbp-post review` — review/trust post
`/gbp-post project "<real, verified job details>"` — MANUAL real-project spotlight. Only use when you have actual job facts (real city, real work). Never invent a project — see the No fabrication hard rule.

## How it works

1. Read the post log at `.claude/skills/gbp-post/post-log.md` (or create it if it doesn't exist)
2. Determine post type from the 4-week rotation (or honor the explicit arg)
3. Generate post text following the rules + template below
4. Pick a real photo from the website matching the post type (see Photo Selection)
5. Create a Teamwork task assigned to Cassandra with the post text and the photo's filename + repo path (the connector can't attach files — Cassandra pulls the photo from the repo/website)
6. Show the user a preview of what was sent
7. Log the post to the log file (date, type, post text, photo used, TW task ID)

## Rotation schedule

| Week of month | Post type |
|---------------|-----------|
| 1st | Educational / know-before-you-dig |
| 2nd | Seasonal tip |
| 3rd | Service highlight |
| 4th | Review / trust |

## Business info (use exactly)

- **Name:** AccuRite Excavation & Hauling, Inc.
- **Phone:** (801) 814-6975 — reference only. NEVER write this (or any phone number) into the post text. Google prohibits it. Do not surface it via a "Call now" button either — these posts carry no CTA or button (see hard rule below).
- **Website:** accuriteexcavation.com
- **Location:** Ogden, UT
- **Service area:** Weber, Davis, Box Elder, and Morgan counties (Northern Utah / Wasatch Front)
- **Established:** 1995
- **Owner:** Shawn Durrant
- **Review count:** Hardcoded baseline of 49 five-star reviews — this is likely stale. Before using a specific review number in the post, fetch the current count from GBP or omit the specific number in favor of "5-star rated" / "decades of satisfied customers."
- **License:** Utah E100

**Do NOT mention Salt Lake County or Salt Lake City as a service area.** AccuRite stopped taking SLC jobs in 2026. Cottonwood Heights, Holladay, Herriman, Taylorsville, Sandy, West Jordan, Salt Lake City, Draper, Midvale, Murray, West Valley, and South Jordan are NOT current service areas for GBP-post purposes, even though those location pages still exist on the website.

## Services (rotate through for service highlights)

Residential Excavation, Commercial Projects, Government Projects, Rock Walls & Retaining Walls, Underground Utilities, Grading & Land Clearing, Demolition, Septic Systems, Hauling & Delivery, Water Features & Ponds

## Cities to mention (in-service-area only)

Ogden, North Ogden, South Ogden, Roy, Riverdale, Clearfield, Layton, Kaysville, Farmington, Centerville, Bountiful, Woods Cross, Brigham City, Perry, Willard, Pleasant View, Farr West, West Haven, Harrisville, Washington Terrace, Eden, Huntsville, Liberty, Morgan, Syracuse, Clinton, West Point, Fruit Heights

## Google policy — HARD RULES (never violate)

Google Business Profile post content has rules. Breaking them gets posts rejected or the profile flagged. Reference: https://support.google.com/business/answer/7213077

- **NEVER put a phone number in the post text.** Google's exact rule: "We do not allow your post content to include a phone number." This is the rule that got a prior post flagged. No phone number — not (801) 814-6975, not any other format, not spelled out, not anywhere in the body.
- **Do not add a "Call now" button (or any button) either.** Per AccuRite's no-CTA rule below, these posts are informational only — no button, no phone, no ask. (A button is technically permitted by Google; leaving it off is an editorial choice.)
- Post content must comply with all applicable laws and regulations.
- No deals/promotions/discounts framing that reads like a hotel offer (AccuRite isn't a hotel, but keep posts informational, not coupon-style).

When in doubt, leave it out and keep the post purely informational. See the two hard-rule sections below.

## No advertising or calls to action — HARD RULE (never violate)

These posts are informational only. They must NOT read like an ad and must NOT ask the reader to do anything. Banned in the post text:

- Calls to action of any kind: "request a free estimate", "call us", "tap the Call button", "visit our website", "get started", "contact us today", "book now", etc.
- The website URL used as a pitch, and any promotional / coupon / "act now" framing.

Just deliver useful, true information and stop. End on the information, not an invitation.

(For accuracy: Google does technically permit CTAs and CTA buttons in posts. Removing them is AccuRite's editorial choice to keep the profile non-promotional — enforced here as a hard rule.)

## No fabrication — HARD RULE (never violate)

This is a real client's live Google Business Profile. Every factual claim in a post must be verifiably true. NEVER invent or imply:

- A specific project or job ("last month we completed a basement in Roy") unless real job details were explicitly provided to you. **The auto-rotation must never claim a specific job** — that is exactly the failure that put a fabricated Roy basement on the profile.
- A specific customer, testimonial, quote, or named person.
- A specific number (review count, years on a job, crew size, jobs completed) unless it appears in the verified Business info above.
- Having done work in a named city as a stated fact — even as an "example" ("whether it's a retaining wall in Farmington…") — unless it really happened and you were told so.

You MAY state these, because they are verified (see Business info): in business since 1995, Utah E100 licensed, serves Weber/Davis/Box Elder/Morgan counties, the listed services, 5-star rated (no specific count), based in Ogden. You MAY give general, true educational or seasonal information about excavation work and Northern Utah conditions. When unsure whether something is true, leave it out.

## Post rules

- 150-300 words max
- Informational only — NO call to action and NO advertising language (see hard rule above)
- Only verifiable facts — NO invented projects, jobs, places, people, or numbers (see hard rule above)
- A city may be named only for general/regional context (e.g. service area), never as a claim that we did a specific job there
- Sound like a real contractor, not marketing copy — direct, confident, no fluff
- No hashtags (GBP isn't Instagram)
- No emojis unless specifically requested
- End on the information — no sign-off CTA

## Templates

Every template ends ON the information — no closing CTA. None of them may state or imply a specific job unless real details were provided (see No fabrication hard rule).

### Educational / know-before-you-dig
```
[1-2 sentences of genuinely useful, generally-true information about a type of excavation or site work — what's involved, what affects cost or timing, a common consideration for Northern Utah ground. No specific job, no customer, no "we did".]

[1-2 sentences expanding the practical knowledge a property owner or general contractor would find useful.]

[1 sentence of verifiable context about AccuRite — e.g. Utah E100 licensed, in business since 1995, serving Weber/Davis/Box Elder/Morgan counties. Stated as fact, not a pitch.]

[End on the information. No CTA.]
```

### Seasonal tip
```
[1-2 sentences about what's timely right now in Northern Utah — spring ground thaw, fall prep, winter considerations. Generally true, not a specific event.]

[1-2 sentences of practical advice a homeowner or contractor would find useful.]

[Optional: 1 sentence of verifiable context about AccuRite's experience in the region — factual, not a pitch.]

[End on the information. No CTA.]
```

### Service highlight
```
[1 sentence naming a real AccuRite service (from the Services list) and what it covers.]

[2-3 sentences about what that kind of work generally involves or what to consider — general knowledge, NOT a specific job we did.]

[1 sentence of verifiable context — service area or years in business.]

[End on the information. No CTA.]
```

### Review / Trust
```
[Thank customers generally and reference the 5-star rating WITHOUT a specific count (unless a current count was verified). No invented testimonials, quotes, or specific jobs.]

[1-2 sentences about the company's standards — showing up on time, clean sites, honest pricing — stated as how AccuRite works, not as a claim about a specific job.]

[1 sentence about commitment to the Weber/Davis/Box Elder/Morgan community — the real service area.]

[End on the information. No CTA.]
```

### Manual project spotlight (NOT in the auto-rotation)
```
Only generate this when REAL, verified job details have been provided (via `/gbp-post project "<details>"` or by Ross). If you have no real job, do NOT write this type — pick an auto-rotation type instead. Never invent the project.

[1-2 sentences about the ACTUAL provided project — what was really done, the real in-service-area city, any real detail you were given.]

[1 sentence on why that type of work matters or what makes it tricky — general truth.]

[1 sentence of verifiable credibility — Utah E100 license, years in business, or service area.]

[End on the information. No CTA.]
```

## Photo selection

The skill must select a real photo from one of these directories and name it (filename + repo path) in the Teamwork task — the connector cannot attach files, so Cassandra pulls the photo from the repo/website. Pick by post type:

**Educational / know-before-you-dig (and manual project spotlight)** — pick from `/Users/rosswalker/projects/accurite-excavation/src/assets/images/gallery/`:
- `residential-basement-excavation-01.jpg` / `-02.jpg`
- `residential-excavation-foundation-03.jpg` / `-04.jpg`
- `commercial-site-work-oreillys.jpg`
- `commercial-dance-studio-excavation.jpg`
- `hill-afb-military-project.jpg` / `-02.jpg`
- `septic-installation-utah.jpg`
- `underground-utilities-trenching-01.jpg` / `-02.jpg`
- `grading-land-clearing-01.jpg`
- `grading-excavation-02.jpg`
- `soil-stabilization-utah.jpg`
- `dirt-work-excavation-utah.jpg`
- `heavy-equipment-ogden-utah.jpg`

Match the photo to the topic being described. If the post is about basement/foundation work, use a basement photo. If it's about utility trenching, use a trenching photo. Don't pick a hauling photo for a grading post.

**Seasonal tip** — pick from `/Users/rosswalker/projects/accurite-excavation/src/assets/images/gallery/` (any equipment or jobsite shot):
- `excavator-equipment-utah-01.jpg` / `-02.jpg` / `-03.jpg`
- `heavy-equipment-ogden-utah.jpg`
- `dirt-work-excavation-utah.jpg`

**Service highlight** — pick from `/Users/rosswalker/projects/accurite-excavation/src/assets/images/services/hero/`, matching the service:
- residential → `residential-hero.jpg`
- commercial → `commercial-hero.jpg`
- government → `government-hero.jpeg`
- grading → `grading-hero.jpg`
- hauling → `hauling-hero.jpg`
- demolition → `demolition-hero.jpg`
- septic → `septic-hero.jpg`
- rock walls / retaining walls → `rockwalls-hero.jpg`
- underground utilities → `utilities-hero.jpg`
- water features / ponds → `water-features-hero.jpg`

**Review / Trust** — pick from `/Users/rosswalker/projects/accurite-excavation/src/assets/images/about/`:
- `accurite-team-jobsite.png` (preferred — shows the team working)
- `accurite-equipment-fleet-real.jpg` (real fleet shot)
- `shawn-durrant-owner.jpeg` (owner photo)
- `accurite-owner-equipment.png` (owner with equipment)

**Don't reuse the same photo in consecutive posts.** Check the log file's last 3 entries before picking.

## Teamwork submission

**Use the REST API. Never the Teamwork MCP connector.**

The MCP connector authenticates with interactive OAuth: its token expires and only a human
clicking through claude.ai connector settings can renew it. The scheduled run has no human,
so when the token lapses the run fails *silently*. That is precisely how this post vanished
for three consecutive weeks (2026-06-23, 06-30, 07-07) with no error and no warning.

The REST client is vendored in this repo and uses a static token that does not expire:

```bash
# reads $TEAMWORK_API_TOKEN, else ~/.config/secrets/secrets.env
python3 scripts/teamwork.py tasks 628283 --search 'GBP Post for AccuRite'   # post history
python3 scripts/teamwork.py create --tasklist 2504854 \
    --name "GBP Post for AccuRite — Proof & Approve — [type] — [YYYY-MM-DD]" \
    --desc-file /tmp/desc.md --assignee cassandra --due YYYY-MM-DD
```

(Locally, the same client is on PATH as `tw` — `tw create ...` is equivalent.)

If Teamwork auth fails, fix the token. Do NOT fall back to MCP, and do NOT continue silently.

**Teamwork is the source of truth for post history**, not `post-log.md` — the scheduled run
executes in an ephemeral sandbox whose `git push` can be refused, so the log may be stale or
missing entries. Derive the rotation slot from the task list; treat the log as a convenience.

Task parameters:

- **Project ID:** 628283
- **Tasklist ID:** 2504854 (General tasks — there is no AccuRite-specific tasklist yet)
- **Assignee:** Cassandra (user ID 463236)
- **Priority:** none (NEVER high priority)
- **Due date:** 3 days from now
- **Task name:** `GBP Post for AccuRite — Proof & Approve — [post type] — [date]`
- **Description:** Use this exact structure:

```markdown
## Post to approve

**Type:** [Educational / Seasonal Tip / Service Highlight / Review-Trust / Project Spotlight (manual only)]
**Photo to use:** [filename] — repo path: `src/assets/images/.../[filename]`
(NOT attached — the Teamwork connector can't attach files. Cassandra: download this image from the repo or the website before posting.)

---

[POST TEXT HERE — ready to paste into GBP]

---

## What to check

- [ ] Reads naturally, like real information — not like an ad
- [ ] NO call to action or advertising language anywhere (no "free estimate", "call us", "visit our site", etc.)
- [ ] NO invented or unverifiable specifics — no projects, jobs, places we worked, people, or numbers we can't stand behind
- [ ] NO phone number anywhere in the post text (Google policy)
- [ ] Any city named is in service area (Weber, Davis, Box Elder, or Morgan County — NOT Salt Lake County)
- [ ] No typos
- [ ] Photo matches the post topic

## How to publish

1. Open Google Business Profile: search "AccuRite Excavation" on Google while signed in to the business account
2. Click "Add update" or "Post"
3. Paste the post text above
4. Add the photo named above (download it from the repo/website first)
5. Leave the post informational — do not add a promotional button or any phone number
6. Click "Post"

If you have any questions, review with Ross.
```

The photo is referenced by filename + repo path in the description above — the Teamwork connector has no file-attachment capability, so do NOT claim the photo is "attached." Cassandra retrieves it from the repo/website.

## Output format

After creating the TW task, show the user this summary:

```
GBP Post — [Type] — [Date]
Photo (named for Cassandra to pull, not attached): [filename]
Teamwork task: [link to TW task]
Cassandra has been assigned. Due in 3 days.

---
[post text]
---
```

Then ask: "Anything to tweak before this sits with Cassandra?" The user can say "looks good" or send a correction; if a correction comes in, update the TW task description with `update_task`.

## Logging

Append to `.claude/skills/gbp-post/post-log.md` (create if missing):

```
## [Date] — [Post Type] — TW [task ID]
**Photo:** [filename]
**Post:**
[post text]
```

Create the log file if it doesn't exist. Read the log file first to:
1. Avoid repeating the same service, city, or photo as the last 3 posts
2. Determine which rotation slot is next if `/gbp-post` is called without args

### Persisting the log — best effort, NOT load-bearing

After appending the entry, try to commit and push the log. Scope the `git add` to that one
file so a run can never push site code:

```bash
git add .claude/skills/gbp-post/post-log.md
git commit -m "chore(gbp-post): log <date> <post type> post (TW <task id>)"
git push origin main
```

**If the push fails, report it and move on — do not fail the run and do not retry in a loop.**
The scheduled cloud run is only permitted to push to `claude/*` branches unless "Allow
unrestricted branch pushes" is enabled for the repo on the routine, so a push to `main` from
the sandbox can be refused. That refusal is why the log has no entries after 2026-06-02 even
though the 06-09 and 06-16 posts really were created.

This is why **Teamwork — not this file — is the source of truth for post history.** The
Teamwork task is the deliverable; the log is a human-readable convenience. Never let a failed
log push block or abort the actual post.

## Scheduling

This skill is scheduled to run automatically every Tuesday at 12:03 PM Denver time via a persistent routine. When called from that routine, behave the same as when invoked manually — generate the post, name the photo, create TW task, log it (and commit+push the log). No user confirmation step required for the scheduled run; ship straight to Cassandra.
