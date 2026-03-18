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
5. **Established 1995 / 30+ Years** — black heritage seal with gold AccuRite brand accents (business.json `founded: 1995`, incorporated 1999)

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
| Homepage hero | Excavator on job site, Wasatch mountains backdrop | Real photo or generated |
| About page | Shawn / team photo, equipment fleet, HQ exterior | Real photos preferred |
| Service pages (10) | One hero image per service | Mix real + generated |
| Location pages (18+) | City-relevant imagery or reuse service photos | Generated or stock |
| Gallery | 12-20 project photos | Real photos from Drive |
| OG default | Branded social card (logo + tagline) | Generated |

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
- Every service page links to 2-3 related services
- Every service page links to 3-5 top location pages
- Every location page links to all services offered in that area
- Blog posts link to relevant service + location pages
- Footer includes top city links organized by county
- Add "Related Services" section to each service page
- Add "Nearby Areas We Serve" section to each location page

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

#### Location Pages (18 existing + 21 new = 39 total)
- Each page: unique H1 targeting `[service] in [city], Utah`
- Content: local knowledge (neighborhoods, soil conditions, permit requirements)
- Embedded Google Map
- Links to all services
- Unique meta title/description per page
- Check for keyword cannibalization — each page should target distinct city
- 800-1,200 words minimum per location page

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

### Pre-launch Blockers (user to provide)
- HighLevel webhook URL for contact form
- BBB profile URL
- Google Business Profile URL
- Real photos downloaded from Google Drive to local folder
