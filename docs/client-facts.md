# AccuRite Excavation — client facts

The source of truth for every factual claim on this site. The `review-gate` agent reads
this file before any push and blocks content that contradicts it or invents claims it
can't find here.

**How to read a status:**

- **CONFIRMED** — Shawn or Ross said it, directly. Trustworthy. Beats the diff, beats the
  repo, beats the live site.
- **UNCONFIRMED** — extracted from the live site or a research note. **This is not
  evidence.** The live site is where a fabrication would already be living, so it can
  never confirm itself. Everything seeded from the site starts here until a human says
  otherwise.
- **SUPERSEDED &lt;date&gt;** — was true, now replaced. Kept, never deleted, so the history is
  auditable.

**How this file grows:** lazily. Nobody sits down to fill it in. When the review gate
blocks a push, it asks Ross a question; his answer gets appended here, dated and sourced,
and the gate is smarter on the next run. Append only — never edit or delete an entry.

Entry format:

```
- **[CONFIRMED|UNCONFIRMED]** <the fact, stated plainly and checkably>
  - Source: <who said it and how> — <YYYY-MM-DD>
```

---

## Confirmed

These three are settled. They are the reason this file exists — each one is a claim the
site got wrong or could get wrong.

- **CONFIRMED** The vacuum truck is **water-based, NOT heated**. Do not describe it as a
  heated vacuum truck, hydrovac-with-heat, or any wording implying it heats water. It does
  not.
  - Source: Shawn, relayed by Ross — 2026-07-14

- **CONFIRMED** **Cal Ranch is NOT a client.** Do not name Cal Ranch as a customer,
  reference, partner, or past project anywhere on the site.
  - Source: Shawn, relayed by Ross — 2026-07-14

- **CONFIRMED** Google Business Profile **strips EXIF data from images on upload**. Do not
  claim or rely on geotagged photos carrying location data through to GBP; any strategy or
  copy premised on EXIF surviving a GBP upload is wrong.
  - Source: Confirmed by Ross — 2026-07-14

---

## Unconfirmed — seeded from the live site 2026-07-14

Pulled from accuriteexcavation.com on 2026-07-14. **Every item below is unverified.** The
site is the thing being audited, so it cannot vouch for itself. Ross confirms or kills
these in one sitting; until then the gate treats a *contradiction* of any of them as a
flag, but will not accept one as proof.

### Business identity

- **UNCONFIRMED** Owner is Shawn Durrant, who founded AccuRite Excavation in 1995.
  - Source: /about/ live page — 2026-07-14
- **UNCONFIRMED** In business 31+ years / "Serving the Wasatch Front since 1995."
  - Source: /about/ and /services/ live pages — 2026-07-14
- **UNCONFIRMED** Phone (801) 814-6975; address 2940 Midland Dr, Ogden, UT 84401.
  - Source: /services/ and /about/ live pages — 2026-07-14
- **UNCONFIRMED** Hours are 6:30 AM–6:00 PM weekdays, closed weekends.
  - Source: /about/ live page — 2026-07-14

### Legal / licensing — highest risk, a regulator can check these

- **UNCONFIRMED** Holds a Utah Contractor License, designation **E100**; "E100 Licensed &
  Fully Insured."
  - Source: /services/ and /about/ live pages — 2026-07-14
- **UNCONFIRMED** "Utah DOPL verified."
  - Source: /about/ live page — 2026-07-14
- **UNCONFIRMED** "BBB Accredited."
  - Source: /about/ live page — 2026-07-14
- **UNCONFIRMED** Safety rating **0.91 EMOD**.
  - Source: /about/ live page — 2026-07-14

### Statistics

- **SUPERSEDED 2026-07-14: UNCONFIRMED** 4.9 Google star rating with 49 reviews (site says
  both "49 Google reviews" and "49 Five-Star Reviews" — these are not the same claim and at
  least one is imprecise).
  - Source: /services/ and /about/ live pages — 2026-07-14
  - Superseded by the CONFIRMED 60-five-star entry below — Shawn via Ross, 2026-07-14.

- **CONFIRMED** AccuRite currently has **60 five-star reviews**. The number 49 is stale
  wherever it appears.
  - Source: Shawn via Ross — 2026-07-14
  - **The live site is stale and still says 49.** Updating site copy is a separate task and
    was deliberately not done when this fact was recorded. The stale 49 lives in four
    places in the repo:
    - `src/data/business.json` → `reviews.count: 49` (with `rating: 4.9`,
      `lastUpdated: 2026-03-12`). This is the data source, imported across the site, and it
      feeds the schema.org `aggregateRating` in `src/components/SchemaMarkup.astro` — so
      Google is being served this number as structured data, not just page text.
    - `src/pages/index.astro` → "backed by 49 five-star reviews" (hardcoded).
    - `src/content/locations/ogden.md` → meta description, "4.9 stars from 49 reviews"
      (hardcoded).
    - `src/content/services/residential-excavation.md` → "With 49 reviews on Google"
      (hardcoded).
  - **Careful when the site is updated:** "60 five-star reviews" is not the same claim as a
    total review count of 60, and `business.json`'s `reviews.count` feeds a schema.org
    `aggregateRating.reviewCount`, which is supposed to be the **total** number of reviews.
    Shawn confirmed the five-star figure; the total is still unconfirmed. Do not assume
    `count: 60` is the correct edit without asking.

### Services offered

- **UNCONFIRMED** Residential excavation (foundation digs, basement excavation, grading,
  site preparation).
  - Source: /services/ live page — 2026-07-14
- **UNCONFIRMED** Commercial projects (building pads, parking lots, subdivisions,
  multi-family developments).
  - Source: /services/ live page — 2026-07-14
- **UNCONFIRMED** Government projects.
  - Source: /services/ live page — 2026-07-14
- **UNCONFIRMED** Rock walls & retaining walls.
  - Source: /services/ live page — 2026-07-14
- **UNCONFIRMED** Underground utilities (water lines, sewer lines, storm drain, gas,
  utility trenching).
  - Source: /services/ live page — 2026-07-14
- **UNCONFIRMED** Septic systems — tank installation, repair, replacement, and perc
  testing.
  - Source: /services/ live page — 2026-07-14
- **UNCONFIRMED** Grading, land clearing, and demolition.
  - Source: /services/ live page — 2026-07-14
- **UNCONFIRMED** Hauling & delivery — gravel, topsoil, fill dirt, sand; debris removal.
  - Source: /services/ live page — 2026-07-14
- **UNCONFIRMED** Water features & ponds.
  - Source: /services/ live page — 2026-07-14

### Equipment

- **UNCONFIRMED** Excavators (multiple sizes), skid steers and loaders, dump trucks and
  trailers, compactors and graders, trenchers, rock hammers and breakers.
  - Source: /about/ live page — 2026-07-14
  - Note: the vacuum truck is **not** in the site's equipment list, yet it exists (see the
    CONFIRMED water-based entry above). The equipment list is therefore known to be
    incomplete — absence from this list is not evidence a machine doesn't exist.

### Service area

- **UNCONFIRMED** Serves Weber, Davis, Salt Lake, Morgan, and Box Elder counties. The
  services page lists 39 Utah municipalities; the about page says "45+ named cities." These
  two numbers disagree and at least one is wrong.
  - Source: /services/ and /about/ live pages — 2026-07-14

### Named third parties presented as clients — treat as radioactive

The about page names these organizations as clients or past projects. **Naming an
organization as a customer when it isn't is the single fastest way to get a client sued**,
and Cal Ranch already proved this site does it (see CONFIRMED above). Every name below is
UNCONFIRMED and the gate flags any of them until Shawn confirms each one individually.

- **SUPERSEDED 2026-07-14: UNCONFIRMED** Army Corps of Engineers
- **SUPERSEDED 2026-07-14: UNCONFIRMED** National Park Service
- **SUPERSEDED 2026-07-14: UNCONFIRMED** U.S. Postal Service
- **SUPERSEDED 2026-07-14: UNCONFIRMED** Ogden City Airport
- **SUPERSEDED 2026-07-14: UNCONFIRMED** Weber County Engineering
- **SUPERSEDED 2026-07-14: UNCONFIRMED** Big D Construction
- **SUPERSEDED 2026-07-14: UNCONFIRMED** Alpine Community Church
- **SUPERSEDED 2026-07-14: UNCONFIRMED** O'Reilly's
- **SUPERSEDED 2026-07-14: UNCONFIRMED** HHI
- **SUPERSEDED 2026-07-14: UNCONFIRMED** Hill Air Force Base
- **SUPERSEDED 2026-07-14: UNCONFIRMED** Camp Williams
  - Source (all of the above): /about/ live page — 2026-07-14
  - Superseded by the CONFIRMED client-list entries below — Shawn via Ross, 2026-07-14.

---

## Confirmed — client list, 2026-07-14

Shawn confirmed the named-client list from /about/ individually. These eleven supersede the
UNCONFIRMED block above. **This confirmation covers the client list only** — it says nothing
about the service-area counts, the review counts, or the equipment list, all of which remain
UNCONFIRMED.

- **CONFIRMED** Army Corps of Engineers is a genuine past client.
  - Source: Shawn via Ross — 2026-07-14
- **CONFIRMED** National Park Service is a genuine past client.
  - Source: Shawn via Ross — 2026-07-14
- **CONFIRMED** U.S. Postal Service is a genuine past client.
  - Source: Shawn via Ross — 2026-07-14
- **CONFIRMED** Ogden City Airport is a genuine past client.
  - Source: Shawn via Ross — 2026-07-14
- **CONFIRMED** Weber County Engineering is a genuine past client.
  - Source: Shawn via Ross — 2026-07-14
- **CONFIRMED** Big D Construction is a genuine past client.
  - Source: Shawn via Ross — 2026-07-14
- **CONFIRMED** Alpine Community Church is a genuine past client.
  - Source: Shawn via Ross — 2026-07-14
- **CONFIRMED** O'Reilly's is a genuine past client.
  - Source: Shawn via Ross — 2026-07-14
- **CONFIRMED** HHI is a genuine past client.
  - Source: Shawn via Ross — 2026-07-14
- **CONFIRMED** Hill Air Force Base is a genuine past client (military construction).
  - Source: Shawn via Ross — 2026-07-14
- **CONFIRMED** Camp Williams is a genuine past client (military construction).
  - Source: Shawn via Ross — 2026-07-14

Cal Ranch remains **NOT a client** (see Confirmed, above). This confirmation does not
reinstate it.

---

## Open questions for Shawn

Answer these in one sitting and most of the file above flips to CONFIRMED.

1. ~~Which of the named organizations above are genuinely past clients, and which are
   aspirational, secondhand, or invented?~~ **ANSWERED 2026-07-14** — all eleven confirmed
   by Shawn via Ross. See "Confirmed — client list" above. Cal Ranch stays out.
2. Is the E100 license current, and is the 0.91 EMOD rating current-year?
3. Is the service area 39 cities or 45+? The two pages disagree.
4. ~~Is the review count 49 total reviews, or 49 five-star reviews specifically?~~
   **PARTLY ANSWERED 2026-07-14** — Shawn confirms **60 five-star reviews** (49 is stale).
   Still open: what is the **total** review count? The site's schema markup publishes
   `reviews.count` to Google as a total, so this number is still needed.
5. What else is in the equipment fleet? The site's list is known to be incomplete.
