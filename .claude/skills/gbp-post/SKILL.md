---
name: gbp-post
description: Use when generating a Google Business Profile post for AccuRite Excavation. Invoke with /gbp-post or when asked to create a GBP post, social media post, or Google Business update. Generates the post, picks a real photo from the website, and creates a Teamwork task for Cassandra to proof and approve.
---

# GBP Post Generator — AccuRite Excavation

Generate a ready-to-paste Google Business Profile post for AccuRite Excavation & Hauling, attach a real photo from the website, and route it to Cassandra in Teamwork for proofreading + approval.

## Usage

`/gbp-post` — generates the next post in the rotation
`/gbp-post project "retaining wall in Layton"` — project spotlight post
`/gbp-post seasonal` — seasonal tip post
`/gbp-post service "demolition"` — service highlight post
`/gbp-post review` — review/trust post

## How it works

1. Read the post log at `.claude/skills/gbp-post/post-log.md` (or create it if it doesn't exist)
2. Determine post type from the 4-week rotation (or honor the explicit arg)
3. Generate post text following the rules + template below
4. Pick a real photo from the website matching the post type (see Photo Selection)
5. Create a Teamwork task assigned to Cassandra with the post text + photo attached
6. Show the user a preview of what was sent
7. Log the post to the log file (date, type, post text, photo used, TW task ID)

## Rotation schedule

| Week of month | Post type |
|---------------|-----------|
| 1st | Project photo spotlight |
| 2nd | Seasonal tip |
| 3rd | Service highlight |
| 4th | Review / trust |

## Business info (use exactly)

- **Name:** AccuRite Excavation & Hauling, Inc.
- **Phone:** (801) 814-6975 — reference only. NEVER write this (or any phone number) into the post text. Google prohibits it. Use the "Call now" button instead.
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
- **To let customers call, use the post's "Call now" button instead.** The button pulls the verified Business Profile phone number automatically — that's the compliant way to surface the phone. The button is set when publishing, not typed into the post text (see "How to publish" below).
- Post content must comply with all applicable laws and regulations.
- No deals/promotions/discounts framing that reads like a hotel offer (AccuRite isn't a hotel, but keep posts informational, not coupon-style).

When in doubt, drive the CTA to the website (accuriteexcavation.com) and the "Call now" button — never a typed number.

## Post rules

- 150-300 words max
- Include a call to action — direct to the website and/or the post's "Call now" button, NEVER a typed phone number
- Mention a specific in-service-area city when possible
- Sound like a real contractor, not marketing copy — direct, confident, no fluff
- No hashtags (GBP isn't Instagram)
- No emojis unless specifically requested
- End with a clear CTA (website + "tap Call" — no number in the text)

## Templates

### Project spotlight
```
[1-2 sentences about the specific project — what was done, where, any challenges]

[1 sentence about why this type of work matters or what makes it tricky]

[1 sentence credibility: years in business, license, or general 5-star rating]

Planning a similar project? Request a free estimate at accuriteexcavation.com, or tap the Call button on this post.
```

### Seasonal tip
```
[1-2 sentences about what's timely right now — spring ground thaw, fall prep, winter considerations]

[1-2 sentences of practical advice a homeowner or contractor would find useful]

[Tie it back to AccuRite's experience in the area]

Ready to get started? Request a free estimate at accuriteexcavation.com, or tap the Call button to reach our team.
```

### Service highlight
```
[1 sentence naming the service and what it covers]

[2-3 sentences about common projects, what's involved, or what makes AccuRite's approach different]

[1 sentence about service area or experience]

Need [service]? Tap the Call button for a free on-site estimate, or visit accuriteexcavation.com.
```

### Review / Trust
```
[Thank customers — reference 5-star rating without a specific count unless verified current]

[1-2 sentences about what drives the reviews — showing up on time, clean sites, honest pricing, etc.]

[1 sentence about commitment to Weber/Davis County community]

See what our customers say on Google. Visit accuriteexcavation.com or tap the Call button to start your project.
```

## Photo selection

The skill must select a real photo from one of these directories and attach it to the Teamwork task. Pick by post type:

**Project spotlight** — pick from `/Users/rosswalker/projects/accurite-excavation/src/assets/images/gallery/`:
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

Match the photo to the project being described. If the post is about a basement dig, use a basement photo. If it's about utility trenching, use a trenching photo. Don't pick a hauling photo for a grading post.

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

After the post and photo are ready, create a task in Teamwork:

- **Project ID:** 628283
- **Tasklist ID:** 2504854 (General tasks — there is no AccuRite-specific tasklist yet)
- **Assignee:** Cassandra (user ID 463236)
- **Priority:** none (NEVER high priority)
- **Due date:** 3 days from now
- **Task name:** `GBP Post for AccuRite — Proof & Approve — [post type] — [date]`
- **Description:** Use this exact structure:

```markdown
## Post to approve

**Type:** [Project Spotlight / Seasonal Tip / Service Highlight / Review-Trust]
**Suggested photo:** [filename] (attached)

---

[POST TEXT HERE — ready to paste into GBP]

---

## What to check

- [ ] Reads naturally, not like marketing copy
- [ ] NO phone number anywhere in the post text (Google policy — set the "Call now" button instead)
- [ ] CTA at the end is clear
- [ ] City named is in service area (Weber, Davis, Box Elder, or Morgan County — NOT Salt Lake County)
- [ ] No typos
- [ ] Photo matches the post topic

## How to publish

1. Open Google Business Profile: search "AccuRite Excavation" on Google while signed in to the business account
2. Click "Add update" or "Post"
3. Paste the post text above
4. Attach the photo (download from this task if needed)
5. Set the button to "Call now" so customers can call without a number in the text (Google prohibits phone numbers in post content)
6. Click "Post"

If you have any questions, review with Ross.
```

- **Attach the photo file** to the task. Use the photo path identified above and pass it as a file attachment in the create-task call.

## Output format

After creating the TW task, show the user this summary:

```
GBP Post — [Type] — [Date]
Photo: [filename]
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

## Scheduling

This skill is scheduled to run automatically every Tuesday at 12:03 PM Denver time via a persistent routine. When called from that routine, behave the same as when invoked manually — generate the post, attach photo, create TW task, log it. No user confirmation step required for the scheduled run; ship straight to Cassandra.
