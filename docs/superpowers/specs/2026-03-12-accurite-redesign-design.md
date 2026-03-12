# AccuRite Excavation Website Redesign — Design Specification

**Date:** 2026-03-12
**Client:** AccuRite Excavation & Hauling, Inc. (Shawn Durrant)
**Domain:** accuriteexcavation.com
**Project:** Full website redesign — WordPress/Divi to Astro static site

---

## 1. Project Overview

AccuRite Excavation is a 25+ year excavation contractor based in Ogden, UT serving the Wasatch Front and Northern Utah. The current WordPress/Divi site has SEO issues (duplicate titles/descriptions, broken links, orphaned pages, no navigation), a dated design, and is not generating enough leads.

**Goals:**
- Dominate local search for excavation services across 18 Wasatch Front cities
- Modern, professional design that reflects 25+ years of credibility
- Maximize lead generation (phone calls primary, form submissions secondary)
- Preserve and build on existing domain authority (domain active since 1999)
- Outperform 5 identified competitors

**Approach:** Monolithic Astro static site with Content Collections, Tailwind CSS, deployed to Netlify. Single repo, single deploy, all authority consolidated on one domain.

---

## 2. Site Architecture & Page Structure

### ~60+ pages total

**Core Pages (5):**
- Homepage
- About / The AccuRite Promise
- Gallery / Our Work
- Reviews / Testimonials
- Contact / Request a Quote

**Service Pages (10):**
1. Residential Excavation
2. Retaining & Rock Walls
3. Demolition & Hauling
4. Underground Utilities
5. Septic Systems
6. Grading & Site Prep
7. Footings & Foundations
8. Road Building
9. Commercial Projects
10. Government Projects

**Location Pages (18):**
Ogden, Layton, Bountiful, Farmington, Kaysville, Clearfield, Roy, Riverdale, South Ogden, North Ogden, Pleasant View, Harrisville, West Haven, Syracuse, Clinton, Sunset, Washington Terrace, Morgan

Each location page covers all services available in that area with unique local content (not city-name swaps).

**Service x Location Pages (Phase 2):**
Cross-product pages like "Retaining Walls in Ogden." Only built once genuinely unique content exists for each. Start with highest-volume keyword combinations. Do NOT generate all 180 at once.

**Blog (migrated):**
Cherry-picked posts from existing WordPress site based on Search Console traffic/ranking data. Unmigrated posts get 301 redirected to relevant service pages.

### URL Structure

```
/                                    -> Homepage
/about                               -> About
/gallery                             -> Gallery
/reviews                             -> Reviews
/contact                             -> Contact / Quote
/services/residential-excavation     -> Service page
/services/retaining-walls            -> Service page
/services/demolition-hauling         -> Service page
/services/underground-utilities      -> Service page
/services/septic-systems             -> Service page
/services/grading-site-prep          -> Service page
/services/footings-foundations        -> Service page
/services/road-building              -> Service page
/services/commercial-projects        -> Service page
/services/government-projects        -> Service page
/locations/ogden                     -> Location page
/locations/layton                    -> Location page
/locations/[city-slug]               -> Location page
/services/[service]/[city]           -> Service x Location (phase 2)
/blog/[slug]                         -> Blog posts
```

### 301 Redirect Strategy

Every existing WordPress URL gets mapped to its new equivalent. Implemented via Netlify `_redirects` file. Key mappings include:

- `/the-accurite-excavation-promise` -> `/about`
- `/our-services` -> `/services/residential-excavation` (or a services index)
- `/our-services/services` -> relevant service page
- `/our-services/services-2` -> relevant service page
- `/our-services/services-3` -> relevant service page
- `/request-a-quote` -> `/contact`
- `/accurite-gallery` -> `/gallery`
- `/the-accurite-excavation-reviews` -> `/reviews`
- `/the-accurite-excavation-promise/about-us-2` -> `/about`
- `/the-accurite-excavation-promise/about-us-2-2` -> `/about`
- All existing blog post URLs -> new `/blog/[slug]` or relevant service page

Full redirect map to be built from sitemap data during implementation.

---

## 3. SEO Strategy

### A. On-Page SEO

- Unique title tags per page: `[Primary Keyword] in [City] | AccuRite Excavation` (50-60 chars)
- Unique meta descriptions per page with call-to-action and phone number (150-160 chars)
- Single H1 per page containing primary keyword
- Logical heading hierarchy (H1 -> H2 -> H3, no skipping)
- Primary keyword in first 100 words of body content
- Open Graph and Twitter Card tags on every page
- Canonical URLs on every page (self-referencing)
- HTTPS everywhere, consistent trailing slash handling

### B. Schema Markup

- **Sitewide:** Organization, WebSite with SearchAction, BreadcrumbList
- **Homepage:** LocalBusiness with full NAP, geo coordinates, opening hours, AggregateRating, license info, areaServed for all 18 cities
- **Service pages:** Service schema linked to parent LocalBusiness, with description and areaServed
- **Location pages:** LocalBusiness with specific areaServed, plus Service schemas for services offered in that city
- **Blog posts:** Article schema with author, datePublished, dateModified
- **Reviews page:** AggregateRating + individual Review schemas
- **All pages:** BreadcrumbList for navigation context

### C. Technical SEO

- Static HTML from Astro — zero WordPress/Divi bloat
- Auto-generated XML sitemap
- robots.txt allowing all crawlers, referencing sitemap
- Core Web Vitals targets: LCP < 2.5s, INP < 200ms, CLS < 0.1
- Image optimization: WebP with fallbacks, lazy loading, responsive srcset, descriptive alt text, descriptive filenames
- Mobile-first responsive design (60%+ of contractor searches are mobile)
- All important pages within 3 clicks of homepage
- Clean URL structure with keywords where natural
- Deploy to Netlify with CDN for fast TTFB

### D. Location Pages — Done Right (not doorway pages)

Each page needs 40-60% unique content minimum to avoid doorway page penalties:

- City-specific intro referencing local landmarks, neighborhoods, terrain
- Local soil conditions and excavation challenges specific to that area
- Municipal permit requirements (differ city to city in Utah)
- Completed AccuRite projects in that city with photos (where available)
- Local testimonials from customers in that area
- Embedded map showing service coverage for that specific city
- City-specific FAQs (e.g., "Do I need a permit for excavation in Ogden?")
- Cross-links to nearby city pages (Ogden <-> North Ogden <-> South Ogden)

Prioritize the top 5-6 cities first (where AccuRite has the most projects and photos), build rich pages, then expand.

### E. E-E-A-T Signals

- **Experience:** Real project photos (no stock), before/after galleries with context, case studies, video content of work in progress
- **Expertise:** Shawn's bio with credentials and 25+ years experience, E100 license prominently displayed, content demonstrating deep knowledge (soil types, equipment selection, grading techniques)
- **Authoritativeness:** Government/military client logos, industry association memberships, BBB accreditation, certifications displayed
- **Trustworthiness:** Clear contact info on every page, insurance and licensing visible, privacy policy, terms of service

### F. Internal Linking (Hub-and-Spoke Model)

- **Homepage** -> links to all service pages + "Service Areas" hub
- **Service pages** (hubs) -> link to relevant location pages and related services
- **Location pages** (spokes) -> link back to parent service pages + cross-link to nearby cities
- **Blog posts** -> link to at least one service page and one location page
- Descriptive, varied anchor text (not the same exact-match keyword every time)
- 2-5 contextual internal links per 1,000 words
- Breadcrumbs on every page

### G. Google Business Profile Strategy

- Optimize primary category: "Excavation Contractor" with relevant secondary categories
- Complete every field: description, all services with descriptions, attributes, hours, 18 service areas
- Weekly GBP posts: project photos, tips, seasonal content
- New geotagged photos added weekly
- Q&A section populated with common questions
- Respond to every review within 24-48 hours
- Review generation system: request reviews after every job via SMS/email with direct Google review link
- Coach customers to mention specific services and locations in reviews

### H. NAP Consistency & Citations

Master NAP format used everywhere:
- **Name:** AccuRite Excavation & Hauling, Inc.
- **Address:** 2940 Midland Dr, Ogden, UT 84401
- **Phone:** (801) 814-6975

Platforms for consistency: GBP, Apple Maps, Bing Places, Yelp, Facebook, BBB, HomeAdvisor, Angi, Houzz, Chamber of Commerce, data aggregators (Neustar Localeze, Data Axle, Foursquare). Quarterly audit for drift.

### I. Local Link Building

- Partnerships with complementary businesses (concrete contractors, builders, landscapers, plumbers) — mutual referral pages
- Chamber of Commerce memberships with directory listings
- Industry directories: Houzz, HomeAdvisor, Angi, BBB
- Supplier/equipment dealer directories
- Community involvement: sponsor local teams, donate services, participate in events
- Local content that earns links: "Guide to Excavation Permits in Weber County", "Understanding Utah Soil Types"
- Pitch project stories to local news/publications

### J. AI Search / Generative Engine Optimization

- Structured data on every page so AI systems can parse business info
- Clear, factual content that AI can cite (not fluffy marketing speak)
- Complete GBP profile (AI systems skip incomplete profiles)
- FAQ content in Q&A format that AI assistants can surface
- Consistent entity information across all platforms

---

## 4. Competitive Analysis Phase

Structured analysis of all 5 competitors before finalizing content and design:

**Competitors:**
1. Next Construction
2. D&J Grading
3. Parker Rock and Dirt
4. Wasatch Valley Excavation
5. Ormond Construction

**Analysis per competitor:**
- Website quality (design, speed, mobile experience)
- SERP positions for target keywords (via DataForSEO)
- Content depth and structure (service/location pages)
- Schema markup and technical SEO
- Backlink profile and domain authority
- Google Business Profile (reviews, posts, completeness)
- Strengths to match or beat
- Gaps AccuRite can exploit

**Output:** Competitive intelligence report that informs keyword priorities, content depth benchmarks, design benchmarks, and link building targets.

**Timing:** Early phase — before writing content or finalizing page designs.

---

## 5. Lead Generation Strategy

**Primary conversion: Phone call. Secondary: LeadConnector form.**

### Phone Number Placement
- Sticky header on all pages — phone number always visible, click-to-call on mobile
- Hero section CTA on every page
- Footer with full contact block
- Floating click-to-call button on mobile (bottom of screen)

### LeadConnector Forms On
- All 10 service pages
- All 18 location pages
- Dedicated Contact/Quote page
- NOT on blog posts (keep informational, link to service pages)

### Trust Signals Near Every CTA
- "25+ Years in Business"
- "E100 Licensed & Fully Insured"
- Google rating badge (4.9 stars, 49 reviews)
- Government/military client logos

### Conversion-Focused Page Structure
Every service and location page follows:
Hero with CTA -> Problem/Need -> Solution (what AccuRite does) -> Social proof (testimonials, project photos) -> FAQ -> Final CTA with form

No page ends without a clear next step.

### Tracking
- Call tracking (if used through LeadConnector)
- Form submission tracking via LeadConnector
- Google Analytics 4 event tracking on CTAs
- UTM parameters for paid/social campaigns

---

## 6. Design & UX

### Brand
- **Primary color:** Gold (#E8C840)
- **Secondary color:** Charcoal (#333333)
- **Typography:** Bold industrial sans-serif (specific Google Font pairing selected during implementation)
- **Logo:** Existing AccuRite logo with diagonal spade/A lettermark
- **Aesthetic:** Clean & professional. Whitespace-heavy, project photos do the talking. Established contractor, 25+ years of credibility.

### Global Layout
- **Sticky header:** Logo left, main nav center, phone number + "Request Quote" button right. Click-to-call on mobile. Hamburger menu on mobile.
- **Footer:** Full contact block (NAP), service links, location links, social links, license/insurance info, copyright
- **Breadcrumbs:** On every page below header

### Homepage
- Hero: Strong headline + subheadline, phone CTA + quote button, background project photo
- Service cards: All 10 services as visual grid linking to service pages
- Trust bar: Years in business, license, insurance, Google rating
- About teaser: Brief company story with link to About page
- Notable clients: Government/military logos (Army Corps, National Park Service, USPS, etc.)
- Testimonial carousel: 3-5 top reviews
- Service area map: Interactive or static map showing all 18 cities
- Final CTA: Phone + form

### Service Pages
- Hero with service-specific headline + CTA
- Problem/need section (why you need this service)
- How AccuRite does it (process, equipment, expertise)
- Project gallery (real photos of this service type)
- Testimonials relevant to this service
- FAQ section (targets long-tail keywords)
- Related services (internal linking)
- CTA with LeadConnector form

### Location Pages
- Hero with city name + CTA
- Local intro (unique city-specific content)
- Services available in this area
- Local projects completed (with photos)
- Local testimonials
- Permit/regulation info for that municipality
- Nearby cities served (cross-links)
- CTA with form

### Gallery Page
- Filterable by service type and/or city
- Before/after comparisons where available
- Project descriptions with each photo set

### Reviews Page
- All Google reviews (not just 3)
- Google rating badge prominently displayed
- Organized by service type if possible
- CTA to leave a review

### About Page
- Company history (1995 -> present)
- Shawn's bio with photo
- Team/crew photo
- Equipment showcase
- Licensing, insurance, certifications
- Notable clients and projects
- Values/promise

### Contact Page
- LeadConnector form
- Phone number (prominent)
- Business hours
- Service area map
- Address (for NAP consistency)

---

## 7. Content Strategy & Migration

### New Content (written from scratch)
- 10 service pages — deep, authoritative, keyword-targeted
- 18 location pages — unique local content per city (prioritize top 5-6 first)
- Homepage, About, Reviews, Contact, Gallery page descriptions

### Migrated Content
- Cherry-picked blog posts with existing traffic/rankings (determined by Search Console audit)
- 8 existing markdown content files in `~/Desktop/Accurite/web content/` as starting drafts for service pages

### Content Quality Bar
- Every service page should be the most comprehensive in the Wasatch Front market
- No AI-sounding filler — real voice, real expertise, Shawn's knowledge
- Each page targets a primary keyword cluster with supporting long-tail terms
- Content answers actual questions homeowners and project managers are asking

### Content Workflow
1. Competitive analysis determines keyword targets and content depth benchmarks
2. SEO Machine `/research` and `/write` commands draft each page
3. Each draft reviewed against competitors for depth and uniqueness
4. Shawn reviews for accuracy
5. Final SEO optimization pass before publishing

### Blog Strategy (post-launch)
- Ongoing content targeting informational queries feeding into service pages
- Project case studies (E-E-A-T)
- Local guides ("Guide to Excavation Permits in Weber County")
- Seasonal content (spring grading season, winter prep)
- Each post links to relevant service + location pages

---

## 8. Technical Architecture & Deployment

### Tech Stack
- **Framework:** Astro (static site generation)
- **Styling:** Tailwind CSS
- **Content:** Astro Content Collections (Markdown/MDX)
- **Data:** JSON files for services, locations, business info (single source of truth)
- **Hosting:** Netlify (CDN, auto-deploys from GitHub, `_redirects` for 301s)
- **Repository:** GitHub

### Project Structure

```
src/
  layouts/
    BaseLayout.astro          -> Global layout (header, footer, schema, meta)
    ServiceLayout.astro       -> Service page template
    LocationLayout.astro      -> Location page template
    BlogLayout.astro          -> Blog post template
  pages/
    index.astro               -> Homepage
    about.astro               -> About
    gallery.astro             -> Gallery
    reviews.astro             -> Reviews
    contact.astro             -> Contact
    services/
      [slug].astro            -> Dynamic service pages from content collection
    locations/
      [slug].astro            -> Dynamic location pages from content collection
    blog/
      [slug].astro            -> Dynamic blog posts from content collection
  components/
    Header.astro              -> Sticky header with nav + phone
    Footer.astro              -> Full footer with NAP + links
    Hero.astro                -> Reusable hero section
    ServiceCard.astro         -> Service grid card
    TestimonialCard.astro     -> Review/testimonial display
    CTASection.astro          -> Reusable CTA block with form embed
    Breadcrumbs.astro         -> Breadcrumb navigation
    SchemaMarkup.astro        -> JSON-LD schema generator
    ServiceAreaMap.astro      -> Map component
    GalleryGrid.astro         -> Filterable photo gallery
  content/
    services/                 -> Markdown files for each service
    locations/                -> Markdown files for each city
    blog/                     -> Migrated blog posts
  data/
    business.json             -> NAP, hours, license, social links
    services.json             -> Service list with metadata
    locations.json            -> City list with coordinates, details
public/
  images/                     -> Optimized project photos, logos
  _redirects                  -> Netlify 301 redirect map
  robots.txt
```

### Data-Driven Approach
- `business.json` is single source of truth for NAP, phone, hours — referenced everywhere. Change once, updates everywhere.
- `services.json` defines all 10 services with slugs, descriptions, keywords — drives page generation and service cards
- `locations.json` defines all 18 cities with coordinates, region, details — drives location page generation and maps

### Performance Targets
- Lighthouse score: 95+ across all categories
- LCP < 2.0s (beating the 2.5s "good" threshold)
- CLS < 0.05
- Total page weight < 500KB on initial load

### Launch Checklist
- All 301 redirects verified with crawl tool
- Schema markup validated on every page type
- XML sitemap submitted to Google Search Console
- Google Business Profile links updated to point to new page URLs
- All pages pass mobile-friendly test
- Core Web Vitals passing in PageSpeed Insights
- GA4 tracking verified on all pages
- Old WordPress site kept as backup for 30 days

---

## 9. Ogden Rock Walls Cross-Linking Strategy

The separate Ogden Rock Walls niche site (planned as its own Astro build) will coexist with the main AccuRite site:

- **Main site** has its own retaining walls service page with unique content
- **Niche site** goes deeper on rock/retaining walls specifically across 18 cities
- Content is NOT duplicated — different angles, different depth
- Niche site links to AccuRite as parent brand
- AccuRite site can reference "our specialized rock wall division" with a link out
- Both sites benefit from cross-trust signals

---

## 10. Business Information (Reference)

- **Company:** AccuRite Excavation & Hauling, Inc.
- **Owner:** Shawn Durrant
- **Founded:** 1995 (as Durrant Hauling), incorporated 1999
- **Address:** 2940 Midland Dr, Ogden, UT 84401
- **Phone:** (801) 814-6975
- **License:** E100 (fully insured)
- **Hours:** Mon-Fri 6:30am-6:00pm
- **Google Reviews:** 4.9 stars, 49 reviews
- **Notable Clients:** Army Corps of Engineers, Ogden City Airport, Weber County Engineering, USPS, National Park Service, Big D Construction, Alpine Community Church, O'Reilly's, HHI

### Brand Assets Available
- Logo files and brand photography (13 images in `brand/images/`)
- Brand config with colors and typography defined (`brand/brand-config.json`)
- 24 project/team photos (`~/Desktop/Accurite/pics/`)
- 8 markdown content files (`~/Desktop/Accurite/web content/`)
