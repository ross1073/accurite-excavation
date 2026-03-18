# AccuRite Excavation Phase 2 — Trust Badges, Images, Contact Form, SEO Overhaul

**Date:** 2026-03-18
**Repo:** `~/sites/accurite-excavation-ogden-ut/`
**Branch:** `feature/redesign-implementation`
**Status:** Spec

---

## Overview

Four additions to the existing Astro 5 site before launch:

1. **Trust badges** — 5 earned-look third-party-style badges
2. **Images** — real photos from client + AI-generated fills, fully optimized
3. **Contact form** — native HTML form with HighLevel webhook + UTM/Google tracking
4. **Full SEO overhaul** — technical + content audit targeting page 1 position 1 across Weber, Davis, Salt Lake, and Morgan counties

---

## 1. Trust Badges

### Badge Lineup (5 badges)

1. **BBB A+ Rating** — real BBB blue (#00529b) / gold (#f0b323) branding, torch-style seal
2. **Google Reviews 4.9** — real Google logo colors, star rating, review count
3. **Utah Licensed E100** — official state seal look, gold/cream, circular with double border
4. **Licensed & Insured** — shield-style badge, distinct from E100 seal (different color — dark blue or green)
5. **Established 2010 / 16 Years Experience** — black heritage seal with gold AccuRite brand accents

### Design Requirements

- Each badge must look visually **distinct** — different shapes, colors, typography — as if collected from different organizations over time
- BBB and Google use their real platform branding
- Non-platform badges (E100, Licensed & Insured, Est. 1999) generated as **high-quality AI badge images** via the image generator, saved as optimized WebP
- All badges rendered as images (not CSS-only wireframes) for production quality

### Component: `TrustBadges.astro`

- White background section
- Responsive flex row, centered, wraps on mobile
- Each badge ~100-120px wide, consistent height
- Placement:
  - **Homepage** — below TrustBar, above services grid
  - **About page** — below hero
  - **Contact page** — near form for conversion trust

---

## 2. Images

### Sources

- **Primary:** Real photos from client (Google Drive → download to local, optimize)
- **Fill:** AI-generated images via image generator for gaps

### Directory Structure

```
public/images/
├── hero/          # Hero background images (homepage, service pages)
├── services/      # Service-specific images (one per service page minimum)
├── gallery/       # Project gallery photos
├── badges/        # Trust badge images (5 files)
├── about/         # Team, equipment, HQ photos
└── og/            # Open Graph social sharing images
```

### Optimization Pipeline

- Use **Astro `<Image>` component** from `astro:assets` for automatic build-time optimization (WebP conversion, srcset generation, dimension attributes)
- Place source images in `src/assets/images/` (Astro-managed) for build-time processing; only pre-optimized badges go in `public/images/badges/`
- **Lazy loading** (`loading="lazy"`) on all below-fold images
- Hero images **eager loaded** (`loading="eager"`, `fetchpriority="high"`)
- Descriptive, keyword-rich `alt` tags on every image
- Max file size targets: hero ~150KB, gallery ~80KB, badges ~30KB

### Image Assignments

| Page | Image Needed | Source |
|---|---|---|
| Homepage hero | Excavator on job site, Wasatch mountains backdrop | Real (Equipment folder) |
| About page | Team/crew with equipment | **Generate** (1-2 images) |
| Residential Excavation | Basement dig, foundation work | Real (16 photos in Residential Ex) |
| Commercial Projects | Commercial site work | Real (8 photos in Commercial Jobs) |
| Government Projects | Hill AFB / military project | Real (Hill AFB photos) |
| Demolition | Excavator demolishing structure | **Generate** (1 image) |
| Rock Walls / Retaining Walls | Boulder wall, block wall, completed project | **Generate** (2-3 images) |
| Septic Systems | Septic tank installation | Real (Utilities-Septic-Install) + maybe **generate 1** |
| Underground Utilities | Trenching, utility lines | Real (9 photos in Trenching & Utility) |
| Grading / Land Clearing | Graded lot, clearing work | Real (13 photos in Dirt) |
| Hauling / Delivery | Trucks hauling dirt/gravel | Real (Custom-Hauling, Sand-and-Gravel) |
| Water Features / Ponds | Backyard waterfall, pond excavation | **Generate** (2 images) |
| Gallery | 12-20 project photos | Real (best-of across all categories) |
| Location pages (39) | Reuse service photos per page | Real (no generation needed) |
| OG default | Branded social card (logo + tagline) | **Generate** (1 image) |

### Images to Generate (12 total)

1. Trust badge: Utah E100 state seal
2. Trust badge: Licensed & Insured shield
3. Trust badge: Established 2010 heritage seal
4. Demolition: excavator demolishing structure, Utah landscape
5. Retaining wall: boulder/rock retaining wall, residential yard
6. Retaining wall: concrete block retaining wall, completed project
7. Retaining wall: retaining wall with landscaping, side view
8. Water feature: backyard waterfall with rock work
9. Water feature: pond excavation/installation
10. Team/crew: workers with excavation equipment on job site
11. Team/crew: owner portrait or team group shot with equipment
12. OG social card: AccuRite branding with tagline

### Location Landmark Images (~40 images)

One city-relevant landmark/landscape photo per location page. Source from Unsplash, Pexels, or Wikimedia Commons (free commercial-use licensed). Only generate via AI if no good free photo exists.

**Directory:** `src/assets/images/locations/`
**Naming:** `{city-slug}-landmark.jpg` (e.g., `ogden-landmark.jpg`)

Examples of what to source per city:
- Ogden: Union Station, Historic 25th Street, or Ogden River
- Layton: Wasatch Range foothills view
- Salt Lake City: skyline, Capitol building, or city creek
- Draper: Point of the Mountain
- Clearfield: Hill Air Force Base area
- Syracuse: Antelope Island view
- Morgan: Morgan Valley with mountains
- Brigham City: Box Elder Tabernacle or Peach City sign
- Sandy: Snowbird/Little Cottonwood Canyon mouth
- West Jordan: Jordan River trail area
- Herriman: new development with mountain backdrop

Each image gets a descriptive, keyword-rich alt tag (e.g., "View of Ogden Utah with Wasatch Mountains — excavation services in Ogden")

---

## 3. Contact Form

### Form Design

Native HTML `<form>` posting to a HighLevel webhook URL (to be provided by user).

### Fields

| Field | Type | Required | Notes |
|---|---|---|---|
| Full Name | text | yes | |
| Phone | tel | yes | |
| Email | email | yes | |
| Service Needed | select dropdown | yes | Populated from services.json |
| Project Description | textarea | no | 4 rows |
| Preferred Contact Method | radio | no | Call / Text / Email, default: Call |

### Hidden Tracking Fields

Auto-populated from URL parameters via client-side JS on page load:

**UTM Parameters:**
- `utm_source`
- `utm_medium`
- `utm_campaign`
- `utm_content`
- `utm_term`

**Google Ads Tracking:**
- `gclid` (Google Click ID)
- `gbraid` (Google app campaign)
- `wbraid` (Web-to-app measurement)
- `gad_source` (Google Ads source identifier)

**Additional Google-recommended:**
- `page_url` (current page URL, auto-set)
- `page_referrer` (document.referrer, auto-set)
- `landing_page` (stored in sessionStorage on first visit)

### Spam Protection

- Honeypot field (hidden `website` field — if filled, don't submit)
- No CAPTCHA needed for webhook submission

### Form Behavior

- Client-side validation (HTML5 required + pattern attributes)
- Submit via `fetch()` POST to webhook URL (JSON body)
- Success: inline thank-you message replacing form (no page redirect)
- Error: inline error message with retry option
- Submit button: "Get Your Free Estimate" with phone number fallback text
- `min-height` on form container to prevent CLS

### Form Placement Strategy

| Page Type | Placement | Layout |
|---|---|---|
| **Service pages** (10) | Hero area, top of page | Two-column: content left, form right (sidebar). **Note:** requires restructuring from current single-column `max-w-3xl` centered layout. Prose content continues single-column below the hero two-column section. |
| **Contact page** | Main content area | Two-column: info left, form right (existing layout) |
| **Free estimate page** | Hero area, top of page | Two-column: value prop left, form right. **Note:** currently single-column centered — requires layout restructure. |
| **Location pages** (18+) | Above footer, after content | Full-width section with form centered |
| **About page** | Above footer | Full-width CTA section with form |
| **Blog posts** | Above footer | Full-width CTA section with form |
| **Homepage** | Not on homepage (CTA button links to contact) | — |

### Component: `ContactForm.astro`

Props:
- `variant`: `"hero"` (sidebar, compact) or `"section"` (full-width, below content)
- `heading`: optional override (default: "Get Your Free Estimate")
- `webhookUrl`: HighLevel webhook URL (pre-launch blocker — user to provide; fallback: display phone CTA only if URL not configured)

### Tracking Script: `public/js/form-tracking.js`

- Reads URL params on page load
- Populates hidden fields
- Stores `landing_page` in sessionStorage (first-visit only)
- Attaches to form submit event for fetch POST

---

## 4. Full SEO Overhaul

### Target Geography

Five counties, all cities within:

**Weber County:** Ogden (HQ), North Ogden, South Ogden, Roy, Riverdale, Washington Terrace, Pleasant View, Farr West, West Haven, Harrisville, Eden, Huntsville *(12 existing pages)*

**Box Elder County:** Brigham City, Perry, Willard *(3 existing pages)*

**Davis County:** Layton, Kaysville, Clearfield *(3 existing pages)* + Bountiful, Centerville, Clinton, Syracuse, West Point, Fruit Heights, Woods Cross, Farmington *(8 new pages needed)*

**Salt Lake County (NEW):** Salt Lake City, Sandy, West Jordan, South Jordan, Draper, Murray, Midvale, West Valley City, Taylorsville, Cottonwood Heights, Holladay, Riverton, Herriman *(13 new pages needed)*

**Morgan County (NEW):** Morgan *(1 new page needed — no existing page despite earlier assumption)*

**Existing location pages: 18** (12 Weber + 3 Box Elder + 3 Davis)

### New Location Pages Needed

**Morgan County (1):**
- Morgan

**Davis County additions (8):**
- Bountiful, Centerville, Clinton, Syracuse, West Point, Fruit Heights, Woods Cross, Farmington

**Salt Lake County (13):**
- Salt Lake City, Sandy, West Jordan, South Jordan, Draper, Murray, Midvale, West Valley City, Taylorsville, Cottonwood Heights, Holladay, Riverton, Herriman

**Total new location pages: 22**

**Note:** Each new location page also needs an entry in `locations.json` with slug, name, county, region, population, geo coords, nearby cities, and tier.

### Keyword Strategy

Based on DataForSEO research (March 2026):

**Primary targets (highest volume):**
- "excavation company near me" — 110/mo SLC, 50/mo Ogden
- "excavation companies utah" — 210/mo national
- "retaining wall utah" — 140/mo national (seasonal peak 480 Sept)
- "retaining wall blocks utah" — 70/mo national
- "excavation salt lake city" — 50/mo SLC

**Service-specific targets:**
- "demolition contractor near me" — 20/mo SLC
- "septic tank installation near me" — 10/mo SLC, $16.94 CPC
- "retaining wall contractor near me" — 10/mo each metro
- "basement dig out near me" — 10/mo SLC

**Long-tail strategy:** Each location page targets `[service] [city] utah` combinations. Low individual volume (10-20/mo) but 10 services × 39 cities = significant aggregate traffic + Maps pack dominance.

### Technical SEO Audit & Fixes

#### Meta Tags
- Audit all page titles: unique, keyword-targeted, 50-60 chars
- Title format: `[Primary Keyword] | AccuRite Excavation [City]`
- Meta descriptions: unique, action-oriented, 150-160 chars, include phone number
- Every page must have unique title + description (no duplicates)

#### Schema Markup
- **LocalBusiness** — verify on homepage, add `areaServed` with all 5 counties (existing schema maps city names from locations.json — add county-level entries alongside)
- **Service** — one per service page with `areaServed`, `provider`, `serviceType`
- **BreadcrumbList** — verify on all pages
- **FAQPage** — add to service pages (see Content section)
- **Review/AggregateRating** — verify on reviews page + homepage
- **GeoCircle/ServiceArea** — add to each location page for Maps relevance. Use `ServiceArea` with `GeoCircle` centered on city geo coords (from locations.json), radius 15 miles for metro cities, 25 miles for rural (Morgan, Eden, Huntsville)
- **Organization** — add `sameAs` for BBB, Google Business Profile URLs

#### Sitemap & Crawlability
- XML sitemap via `@astrojs/sitemap` (already installed — verify configuration includes all new pages)
- `robots.txt` — verify, ensure all important pages crawlable
- Canonical URLs on every page (already in SEOHead — verify correctness)
- No orphan pages — every page reachable within 3 clicks from homepage

#### Page Speed & Core Web Vitals
- **LCP:** Hero images eager-loaded, preload critical hero image via `<link rel="preload">`
- **CLS:** `min-height` on form containers, image dimensions specified, font `display: swap` (already using)
- **INP:** Minimal JS — only mobile menu + form tracking script
- Font subsetting if possible (Barlow Condensed + Inter — evaluate subset needs)
- Inline critical CSS (Astro handles this well by default)
- Verify Lighthouse scores > 90 on all Core Web Vitals

#### Internal Linking
- Every service page links to 2-3 related services ("Related Services" section)
- Every service page links to 3-5 top location pages ("Areas We Serve" section)
- Every location page links to all services offered in that area
- Every location page links to 3-5 nearby location pages ("Nearby Areas We Serve" section)
- Blog posts link to relevant service + location pages (contextual in-content links)
- Footer includes top city links organized by county (Weber, Davis, Salt Lake, Morgan, Box Elder)
- Homepage links to all service pages and top location pages
- Breadcrumbs on every page (already implemented — verify correctness)

#### Outbound Links (Authority & Trust Signals)
- **BBB profile** link on about page + footer: `https://www.bbb.org/us/ut/huntsville/profile/excavating-contractors/accurite-excavation-hauling-inc-1166-22284228`
- **Google Business Profile** link on contact page + footer: Google Maps listing
- **Utah DOPL** (Division of Professional Licensing) — link to license verification page from about page and E100 badge
- **Local government links** on location pages where relevant (city permit offices, building departments)
- **Industry associations** — if AccuRite is a member of any (e.g., Utah Excavation Contractors Association, AGC of Utah), link to those
- All outbound links open in new tab (`target="_blank" rel="noopener"`)
- Schema `sameAs` array includes BBB URL and Google Business Profile URL

#### Image SEO
- All images have descriptive `alt` tags with target keywords
- File names use keyword slugs (e.g., `excavation-ogden-utah.webp`)
- Image sitemaps included in XML sitemap

### Content SEO Improvements

#### Service Pages (10 existing)
- Add FAQ section (3-5 questions each) with `FAQPage` schema
- Check heading hierarchy: one H1, logical H2/H3 nesting
- Target 1,500-2,500 words per service page
- Add "Areas We Serve" section linking to location pages
- Add cost/pricing section where appropriate (informational intent capture)
- Review keyword density — primary keyword in H1, first paragraph, 2-3 subheadings

#### Location Pages (18 existing + 22 new = 40 total)

**Content Quality Standard — NO Doorway Pages**

Every location page must pass Google's helpful content standard. This means each page reads like it was written by someone who actually works in that city — not a template with the city name swapped. Google specifically penalizes scaled location pages that don't add unique value per page.

Each location page MUST include:

- **Local soil & terrain** — specific ground conditions (clay-heavy in Layton, rocky in Draper, high water table areas, frost line differences between valley floor and bench communities)
- **City-specific permits & regulations** — which cities require excavation permits, building department contacts, HOA considerations in specific neighborhoods, setback requirements
- **Neighborhood-level detail** — specific subdivisions, developments, or areas where excavation work is common (e.g., older Ogden neighborhoods for basement digs, Herriman growth areas for new construction pad prep)
- **Local geography & landmarks** — proximity to mountains, rivers, canyons, highways that affect the work and give the page local flavor
- **Real project context** — types of projects common in that area (military work near Hill AFB in Clearfield, slope work in foothill communities, tight-access jobs in older downtown areas, large lot grading in rural Morgan)
- **Unique challenges** — what makes excavation different in this city vs neighboring cities
- **Local landmark image** — one city-relevant photo per page sourced from Unsplash, Pexels, or Wikimedia Commons (Creative Commons licensed, free for commercial use). Examples: Ogden's Union Station, Wasatch peaks from Layton, Point of the Mountain from Draper, Salt Lake Temple/skyline, Antelope Island from Syracuse. If no good free photo exists for a city, generate one via AI.

**Quality test:** If you removed the city name from the H1, could you still tell which city the page is about from the content alone? If not, the content isn't local enough.

Page structure:
- Unique H1 targeting `[primary service keyword] in [city], Utah`
- Landmark/city image near top of page with descriptive alt tag
- 800-1,200 words minimum of genuinely unique content
- Embedded Google Map
- Links to all services
- "Nearby Areas We Serve" section with links to adjacent cities
- Unique meta title/description per page
- No keyword cannibalization — each page targets its distinct city

#### Blog Content Expansion
- 5 existing posts — review for internal link opportunities
- Identify 5-10 new blog post topics targeting informational queries:
  - "How much does excavation cost in Utah?"
  - "Do I need a permit for a retaining wall in [county]?"
  - "How to choose an excavation contractor in Utah"
  - "Basement excavation vs. basement dig out: what's the difference?"
  - "Retaining wall types: which is best for Utah soil?"
- Each blog post must link to 2+ service pages and 2+ location pages

#### Heading Structure Review
- Verify single H1 per page on all pages
- Ensure H2s reflect target keyword variations
- No heading level skipping (H1 → H3)

---

## Implementation Priority

1. **Contact form** — highest conversion impact, unblocks lead capture
2. **Images** — download real photos, optimize, assign to pages
3. **Trust badges** — generate badge images, create component, place on pages
4. **SEO technical fixes** — schema, meta tags, sitemap, internal linking, page speed
5. **New location pages** (22) — Salt Lake County + Davis County + Morgan additions
6. **Content depth** — FAQ sections, expanded service page content, blog posts
7. **Final audit** — Lighthouse, mobile check, redirect testing

---

## Files Changed/Added

### New Components
- `src/components/TrustBadges.astro`
- `src/components/ContactForm.astro`

### New Scripts
- `public/js/form-tracking.js`

### Modified Pages
- `src/pages/contact.astro` — replace placeholder with ContactForm
- `src/pages/free-estimate.astro` — add ContactForm hero variant
- `src/pages/index.astro` — add TrustBadges section
- `src/pages/about.astro` — add TrustBadges + ContactForm section variant
- `src/pages/services/[...slug].astro` — add ContactForm hero variant + FAQ section
- `src/pages/locations/[...slug].astro` — add ContactForm section variant + internal links
- `src/pages/blog/[...slug].astro` — add ContactForm section variant
- `src/layouts/BaseLayout.astro` — add sitemap link if needed
- `src/components/SEOHead.astro` — any meta tag fixes
- `src/components/SchemaMarkup.astro` — expanded schema types
- `src/components/Footer.astro` — county-organized city links

### New Content (22 location pages)
- `src/content/locations/morgan.md`
- `src/content/locations/bountiful.md`
- `src/content/locations/centerville.md`
- `src/content/locations/clinton.md`
- `src/content/locations/syracuse.md`
- `src/content/locations/west-point.md`
- `src/content/locations/fruit-heights.md`
- `src/content/locations/woods-cross.md`
- `src/content/locations/farmington.md`
- `src/content/locations/salt-lake-city.md`
- `src/content/locations/sandy.md`
- `src/content/locations/west-jordan.md`
- `src/content/locations/south-jordan.md`
- `src/content/locations/draper.md`
- `src/content/locations/murray.md`
- `src/content/locations/midvale.md`
- `src/content/locations/west-valley-city.md`
- `src/content/locations/taylorsville.md`
- `src/content/locations/cottonwood-heights.md`
- `src/content/locations/holladay.md`
- `src/content/locations/riverton.md`
- `src/content/locations/herriman.md`

### New Images
- `src/assets/images/hero/` — homepage + service hero images (Astro-managed)
- `src/assets/images/services/` — per-service images (Astro-managed)
- `src/assets/images/gallery/` — project photos (Astro-managed)
- `src/assets/images/about/` — team/equipment photos (Astro-managed)
- `public/images/badges/` — 5 trust badge images (pre-optimized, public)
- `public/images/og/og-default.jpg` — social sharing card

### Modified Components
- `src/components/SEOHead.astro` — fix ogImage default path from `/images/og-default.jpg` to `/images/og/og-default.jpg`
- `src/components/CTASection.astro` — update to embed ContactForm when `showForm` is true (currently renders empty placeholder)

### New/Modified Data
- `src/data/locations.json` — add 22 new cities with slug, name, county, region, population, geo coords, nearby cities, tier
- `src/data/business.json` — add BBB URL, Google Business Profile URL (user to provide)

### Schema/Config
- `src/content/config.ts` — add `heroImage` field to locations collection schema
- `astro.config.mjs` — verify sitemap config includes all new pages (already installed)
- `public/robots.txt` — verify sitemap reference (already present)

### Pre-launch Blockers (resolved)
- HighLevel webhook URL: `https://services.leadconnectorhq.com/hooks/uRXK3vFHqEQHApRA2dXE/webhook-trigger/f7eb4f71-39c0-4d90-8cd1-ef9760d49aa1`
- BBB profile: `https://www.bbb.org/us/ut/huntsville/profile/excavating-contractors/accurite-excavation-hauling-inc-1166-22284228`
- Google Business Profile: `https://google.com/maps/place/AccuRite+Excavation+%26+Hauling,+Inc./data=!4m2!3m1!1s0x0:0x10e0b92e4cac2d87`
- Photos: `~/Desktop/Accurite/` (select highest-res, deduplicate)
