# AccuRite Excavation Website Redesign — Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild accuriteexcavation.com as an Astro static site optimized for local SEO, lead generation, and modern design — replacing the existing WordPress/Divi site without losing domain authority.

**Architecture:** Monolithic Astro project with Content Collections (Markdown/MDX) for services, locations, and blog posts. JSON data files as single source of truth for business info, services, and locations. Tailwind CSS for styling. Vanilla JS for interactivity (gallery filter, mobile menu). Deployed to Netlify with CDN.

**Tech Stack:** Astro, Tailwind CSS, Vanilla JS, Netlify, GitHub

**Spec:** `docs/superpowers/specs/2026-03-12-accurite-redesign-design.md`

---

## Chunk 1: Research & Competitive Analysis

This phase must complete before content writing or design finalization. It produces the competitive intelligence that shapes everything downstream.

### Task 1: Competitive Analysis — Website Audit

**Files:**
- Create: `research/competitors/competitive-analysis.md`

- [ ] **Step 1: Fetch and analyze each competitor's website**

Use SEO Machine tools and web research to audit all 5 competitors:
1. Next Construction
2. D&J Grading
3. Parker Rock and Dirt
4. Wasatch Valley Excavation
5. Ormond Construction

For each, document:
- URL and tech stack
- Page count and structure (service pages, location pages, blog)
- Content depth (word count on key pages)
- Design quality (modern vs dated, mobile experience)
- Page speed (run through PageSpeed Insights)
- Schema markup present
- Meta tags (unique or duplicate?)

- [ ] **Step 2: SERP position analysis**

Using DataForSEO (via `python3 data_sources/modules/dataforseo.py` or direct API), check rankings for these keyword clusters:
- "excavation contractor ogden"
- "excavation utah"
- "residential excavation ogden"
- "commercial excavation utah"
- "retaining walls ogden"
- "septic system installation ogden"
- "demolition contractor ogden"
- "grading contractor utah"
- "underground utilities ogden"
- "[competitor name]" (branded searches)

Document: who ranks where, what pages rank, estimated traffic.

- [ ] **Step 3: Backlink and domain authority comparison**

For each competitor, document:
- Domain authority / domain rating
- Total backlinks and referring domains
- Top linking domains (potential link building targets for AccuRite)
- Any notable local links (chambers, associations, news)

- [ ] **Step 4: Google Business Profile audit**

For each competitor, check:
- Review count and average rating
- Response rate to reviews
- Post frequency
- Photo count and recency
- Categories used
- Service area coverage

- [ ] **Step 5: Write competitive intelligence report**

Create `research/competitors/competitive-analysis.md` with:
- Executive summary (who's strongest, who's weakest, where AccuRite can win)
- Keyword priority list (ranked by opportunity)
- Content depth benchmarks (target word counts per page type)
- Design benchmarks (what "good" looks like in this market)
- Link building targets (domains linking to competitors but not AccuRite)
- Gaps competitors are leaving open

- [ ] **Step 6: Commit**

```bash
git add research/competitors/
git commit -m "feat: add competitive analysis for 5 excavation competitors"
```

### Task 2: Existing Site SEO Audit & Content Migration Planning

**Files:**
- Create: `research/migration/existing-site-audit.md`
- Create: `research/migration/redirect-map-draft.md`
- Create: `research/migration/content-to-migrate.md`

- [ ] **Step 1: Crawl existing WordPress sitemaps**

Fetch and catalog all URLs from:
- `https://accuriteexcavation.com/sitemap_index.xml`
- Each sub-sitemap (pages, posts, categories, tags, attachments)

Document every URL, its type, and last modified date.

- [ ] **Step 2: Check Search Console for traffic data**

If Search Console access is available, identify:
- Which pages get organic traffic (keep these)
- Which blog posts rank for anything (migrate these)
- Which pages have backlinks (redirect these carefully)
- Current keyword positions to monitor post-launch

If no Search Console access, use DataForSEO to estimate which pages have visibility.

- [ ] **Step 3: Draft redirect map**

Create `research/migration/redirect-map-draft.md` mapping every old URL to its new destination:
- Page URLs -> new page paths
- Post URLs -> `/blog/[slug]` or relevant service page
- Category/tag archives -> homepage or relevant service page
- Media/attachment pages -> `/gallery` or relevant service page
- Feed URLs -> homepage
- `?p=` and `?page_id=` params -> resolved URLs
- `wp-content/uploads/` image paths -> plan for serving or redirecting

- [ ] **Step 4: Identify content to migrate**

Create `research/migration/content-to-migrate.md` listing:
- Blog posts to migrate (with current URL, traffic data, target keyword)
- Blog posts to redirect only (with redirect target)
- Existing content files to use as drafts (8 files in `~/Desktop/Accurite/web content/`)

- [ ] **Step 5: Commit**

```bash
git add research/migration/
git commit -m "feat: add existing site audit and migration plan"
```

### Task 3: Keyword Research & Content Briefs

**Files:**
- Create: `research/keywords/keyword-map.md`
- Create: `research/keywords/content-briefs/` (one brief per service page)

- [ ] **Step 1: Build keyword map**

Using SEO Machine `/research-topics` and `/research-serp` commands plus DataForSEO, build a keyword map:

For each of the 10 service pages, identify:
- Primary keyword (highest volume + intent match)
- Secondary keywords (3-5 supporting terms)
- Long-tail keywords (FAQ-style queries)
- Search volume and competition data

For location pages, identify:
- "[service] in [city]" volume for top cities
- "excavation contractor [city]" variations
- "near me" query patterns

- [ ] **Step 2: Create content briefs for service pages**

For each of the 10 services, create a brief in `research/keywords/content-briefs/[service-slug].md`:
- Target primary keyword
- Secondary keywords to include
- Target word count (based on competitor benchmarks from Task 1)
- Required sections (based on spec's page structure)
- FAQ questions to answer (from keyword research)
- Internal links to include
- Competitor pages to beat (URL + word count)

- [ ] **Step 3: Commit**

```bash
git add research/keywords/
git commit -m "feat: add keyword map and content briefs for all services"
```

---

## Chunk 2: Project Scaffolding & Data Foundation

### Task 4: Initialize Astro Project

**Files:**
- Create: `package.json`
- Create: `astro.config.mjs`
- Create: `tailwind.config.mjs`
- Create: `tsconfig.json`
- Create: `src/env.d.ts`
- Create: `.gitignore`
- Create: `netlify.toml`

- [ ] **Step 1: Create Astro project**

```bash
cd /Users/rosswalker/sites/accurite-excavation-ogden-ut
npm create astro@latest . -- --template minimal --no-install
```

- [ ] **Step 2: Install dependencies**

```bash
npm install
npm install @astrojs/tailwind @astrojs/sitemap tailwindcss
```

- [ ] **Step 3: Configure Astro**

Create `astro.config.mjs`:
```javascript
import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://accuriteexcavation.com',
  integrations: [tailwind(), sitemap()],
  trailingSlash: 'never',
});
```

- [ ] **Step 4: Configure Tailwind**

Create `tailwind.config.mjs` with AccuRite brand colors:
```javascript
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        gold: {
          DEFAULT: '#E8C840',
          dark: '#9A7B00', // WCAG AA compliant on white
        },
        charcoal: {
          DEFAULT: '#333333',
        },
      },
      fontFamily: {
        heading: ['var(--font-heading)', 'sans-serif'],
        body: ['var(--font-body)', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
```

Note: Specific Google Font pairing to be selected and documented in this step. Research industrial sans-serif fonts that complement the AccuRite brand. Candidates: Barlow, Oswald, or Teko for headings; Inter or Source Sans 3 for body.

- [ ] **Step 5: Create Netlify config**

Create `netlify.toml`:
```toml
[build]
  command = "npm run build"
  publish = "dist"

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "SAMEORIGIN"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"
```

- [ ] **Step 6: Verify build works**

```bash
npm run build
npm run preview
```

Expected: Clean build with no errors. Preview server starts.

- [ ] **Step 7: Commit**

```bash
git add -A
git commit -m "feat: initialize Astro project with Tailwind and Netlify config"
```

### Task 5: Create Data Files (Single Source of Truth)

**Files:**
- Create: `src/data/business.json`
- Create: `src/data/services.json`
- Create: `src/data/locations.json`
- Create: `src/data/reviews.json`
- Create: `src/data/clients.json`

- [ ] **Step 1: Create business.json**

```json
{
  "name": "AccuRite Excavation & Hauling, Inc.",
  "shortName": "AccuRite Excavation",
  "owner": "Shawn Durrant",
  "founded": 1995,
  "incorporated": 1999,
  "address": {
    "street": "2940 Midland Dr",
    "city": "Ogden",
    "state": "UT",
    "zip": "84401"
  },
  "phone": "(801) 814-6975",
  "phoneTel": "+18018146975",
  "email": "",
  "license": "E100",
  "insured": true,
  "hours": {
    "monday": "6:30 AM - 6:00 PM",
    "tuesday": "6:30 AM - 6:00 PM",
    "wednesday": "6:30 AM - 6:00 PM",
    "thursday": "6:30 AM - 6:00 PM",
    "friday": "6:30 AM - 6:00 PM",
    "saturday": "Closed",
    "sunday": "Closed"
  },
  "geo": {
    "latitude": 41.223,
    "longitude": -111.9738
  },
  "social": {
    "facebook": "",
    "google": ""
  },
  "reviews": {
    "rating": 4.9,
    "count": 49,
    "lastUpdated": "2026-03-12"
  }
}
```

- [ ] **Step 2: Create services.json**

```json
[
  {
    "slug": "residential-excavation",
    "name": "Residential Excavation",
    "shortName": "Residential",
    "description": "Foundation digs, basement excavation, grading, and site preparation for homes.",
    "icon": "home",
    "keywords": {
      "primary": "residential excavation utah",
      "secondary": ["home excavation", "basement dig", "foundation excavation"]
    }
  },
  {
    "slug": "retaining-walls",
    "name": "Retaining & Rock Walls",
    "shortName": "Rock Walls",
    "description": "Engineered retaining walls and decorative rock walls for residential and commercial properties.",
    "icon": "wall",
    "keywords": {
      "primary": "retaining walls ogden utah",
      "secondary": ["rock walls", "boulder walls", "retaining wall contractor"]
    }
  },
  {
    "slug": "demolition-hauling",
    "name": "Demolition & Hauling",
    "shortName": "Demolition",
    "description": "Structure demolition, debris removal, and material hauling for any project size.",
    "icon": "demolition",
    "keywords": {
      "primary": "demolition contractor utah",
      "secondary": ["hauling services", "debris removal", "structure demolition"]
    }
  },
  {
    "slug": "underground-utilities",
    "name": "Underground Utilities",
    "shortName": "Utilities",
    "description": "Water lines, sewer lines, storm drain, and utility trenching.",
    "icon": "utilities",
    "keywords": {
      "primary": "underground utilities ogden utah",
      "secondary": ["utility trenching", "water line installation", "sewer line"]
    }
  },
  {
    "slug": "septic-systems",
    "name": "Septic Systems",
    "shortName": "Septic",
    "description": "Septic tank installation, repair, and replacement.",
    "icon": "septic",
    "keywords": {
      "primary": "septic system installation utah",
      "secondary": ["septic tank repair", "septic replacement", "drain field"]
    }
  },
  {
    "slug": "grading-site-prep",
    "name": "Grading & Site Prep",
    "shortName": "Grading",
    "description": "Land grading, lot clearing, and site preparation for construction projects.",
    "icon": "grading",
    "keywords": {
      "primary": "land grading utah",
      "secondary": ["site preparation", "lot clearing", "rough grading"]
    }
  },
  {
    "slug": "footings-foundations",
    "name": "Footings & Foundations",
    "shortName": "Foundations",
    "description": "Precision footing excavation and foundation preparation.",
    "icon": "foundation",
    "keywords": {
      "primary": "foundation excavation utah",
      "secondary": ["footing dig", "foundation contractor", "building pad"]
    }
  },
  {
    "slug": "road-building",
    "name": "Road Building",
    "shortName": "Roads",
    "description": "Road construction, repair, and grading for private and commercial access.",
    "icon": "road",
    "keywords": {
      "primary": "road building utah",
      "secondary": ["road grading", "road construction", "access road"]
    }
  },
  {
    "slug": "commercial-projects",
    "name": "Commercial Projects",
    "shortName": "Commercial",
    "description": "Large-scale commercial excavation including building pads, parking lots, and subdivisions.",
    "icon": "commercial",
    "keywords": {
      "primary": "commercial excavation utah",
      "secondary": ["commercial contractor", "building pad", "parking lot excavation"]
    }
  },
  {
    "slug": "government-projects",
    "name": "Government Projects",
    "shortName": "Government",
    "description": "Government and military excavation contracts with security clearance and compliance.",
    "icon": "government",
    "keywords": {
      "primary": "government excavation contractor utah",
      "secondary": ["military contractor", "government contract", "public works"]
    }
  }
]
```

- [ ] **Step 3: Create locations.json**

```json
[
  { "slug": "ogden", "name": "Ogden", "county": "Weber", "region": "Ogden Metro", "geo": { "lat": 41.223, "lng": -111.9738 }, "nearby": ["north-ogden", "south-ogden", "riverdale", "roy"], "priority": 1 },
  { "slug": "layton", "name": "Layton", "county": "Davis", "region": "Davis County", "geo": { "lat": 41.0602, "lng": -111.9711 }, "nearby": ["kaysville", "clearfield", "syracuse"], "priority": 2 },
  { "slug": "bountiful", "name": "Bountiful", "county": "Davis", "region": "Davis County", "geo": { "lat": 40.8894, "lng": -111.8808 }, "nearby": ["farmington", "kaysville"], "priority": 3 },
  { "slug": "farmington", "name": "Farmington", "county": "Davis", "region": "Davis County", "geo": { "lat": 40.9805, "lng": -111.8874 }, "nearby": ["bountiful", "kaysville", "layton"], "priority": 4 },
  { "slug": "kaysville", "name": "Kaysville", "county": "Davis", "region": "Davis County", "geo": { "lat": 41.0352, "lng": -111.9385 }, "nearby": ["layton", "farmington", "clearfield"], "priority": 5 },
  { "slug": "clearfield", "name": "Clearfield", "county": "Davis", "region": "Davis County", "geo": { "lat": 41.1108, "lng": -112.0261 }, "nearby": ["layton", "syracuse", "roy", "sunset"], "priority": 6 },
  { "slug": "roy", "name": "Roy", "county": "Weber", "region": "Ogden Metro", "geo": { "lat": 41.1616, "lng": -112.0264 }, "nearby": ["ogden", "riverdale", "clearfield"], "priority": 7 },
  { "slug": "riverdale", "name": "Riverdale", "county": "Weber", "region": "Ogden Metro", "geo": { "lat": 41.1722, "lng": -111.9939 }, "nearby": ["ogden", "south-ogden", "roy"], "priority": 8 },
  { "slug": "south-ogden", "name": "South Ogden", "county": "Weber", "region": "Ogden Metro", "geo": { "lat": 41.1919, "lng": -111.9713 }, "nearby": ["ogden", "riverdale", "washington-terrace"], "priority": 9 },
  { "slug": "north-ogden", "name": "North Ogden", "county": "Weber", "region": "Ogden Metro", "geo": { "lat": 41.3072, "lng": -111.9602 }, "nearby": ["ogden", "pleasant-view", "harrisville"], "priority": 10 },
  { "slug": "pleasant-view", "name": "Pleasant View", "county": "Weber", "region": "Ogden Metro", "geo": { "lat": 41.3186, "lng": -111.9919 }, "nearby": ["north-ogden", "harrisville"], "priority": 11 },
  { "slug": "harrisville", "name": "Harrisville", "county": "Weber", "region": "Ogden Metro", "geo": { "lat": 41.2814, "lng": -111.9883 }, "nearby": ["north-ogden", "pleasant-view", "ogden"], "priority": 12 },
  { "slug": "west-haven", "name": "West Haven", "county": "Weber", "region": "Weber County", "geo": { "lat": 41.2033, "lng": -112.0511 }, "nearby": ["ogden", "roy"], "priority": 13 },
  { "slug": "syracuse", "name": "Syracuse", "county": "Davis", "region": "Davis County", "geo": { "lat": 41.0894, "lng": -112.0647 }, "nearby": ["layton", "clearfield", "clinton"], "priority": 14 },
  { "slug": "clinton", "name": "Clinton", "county": "Davis", "region": "Davis County", "geo": { "lat": 41.1397, "lng": -112.0505 }, "nearby": ["syracuse", "clearfield", "sunset"], "priority": 15 },
  { "slug": "sunset", "name": "Sunset", "county": "Davis", "region": "Davis County", "geo": { "lat": 41.1364, "lng": -112.0311 }, "nearby": ["clearfield", "clinton", "roy"], "priority": 16 },
  { "slug": "washington-terrace", "name": "Washington Terrace", "county": "Weber", "region": "Ogden Metro", "geo": { "lat": 41.1739, "lng": -111.9602 }, "nearby": ["south-ogden", "ogden", "riverdale"], "priority": 17 },
  { "slug": "morgan", "name": "Morgan", "county": "Morgan", "region": "Morgan County", "geo": { "lat": 41.0361, "lng": -111.6769 }, "nearby": [], "priority": 18 }
]
```

- [ ] **Step 4: Create reviews.json**

Pull the existing reviews from the WordPress site and structure them:
```json
[
  {
    "name": "Mike M.",
    "rating": 5,
    "text": "[actual review text]",
    "service": "residential-excavation",
    "location": "ogden",
    "source": "google"
  }
]
```

Populate with all available Google reviews (not just 3).

- [ ] **Step 5: Create clients.json**

```json
[
  { "name": "Army Corps of Engineers", "type": "government", "logo": "army-corps.png" },
  { "name": "National Park Service", "type": "government", "logo": "nps.png" },
  { "name": "U.S. Postal Service", "type": "government", "logo": "usps.png" },
  { "name": "Ogden City Airport", "type": "government", "logo": null },
  { "name": "Weber County Engineering", "type": "government", "logo": null },
  { "name": "Big D Construction", "type": "commercial", "logo": null },
  { "name": "Alpine Community Church", "type": "commercial", "logo": null },
  { "name": "O'Reilly's", "type": "commercial", "logo": null },
  { "name": "HHI", "type": "commercial", "logo": null }
]
```

- [ ] **Step 6: Verify data files load correctly**

```bash
# Quick sanity check — Astro should build without errors
npm run build
```

- [ ] **Step 7: Commit**

```bash
git add src/data/
git commit -m "feat: add data files — business info, services, locations, reviews, clients"
```

### Task 6: Content Collection Schemas

**Files:**
- Create: `src/content/config.ts`
- Create: `src/content/services/residential-excavation.md` (template)
- Create: `src/content/locations/ogden.md` (template)
- Create: `src/content/blog/.gitkeep`

- [ ] **Step 1: Define content collection schemas**

Create `src/content/config.ts`:
```typescript
import { defineCollection, z } from 'astro:content';

const services = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    slug: z.string(),
    keywords: z.object({
      primary: z.string(),
      secondary: z.array(z.string()),
    }),
    faqs: z.array(z.object({
      question: z.string(),
      answer: z.string(),
    })).optional(),
    relatedServices: z.array(z.string()).optional(),
    heroImage: z.string().optional(),
    galleryImages: z.array(z.string()).optional(),
  }),
});

const locations = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    city: z.string(),
    county: z.string(),
    metaTitle: z.string(),
    metaDescription: z.string(),
    localIntro: z.string(),
    permitInfo: z.string().optional(),
    soilInfo: z.string().optional(),
    faqs: z.array(z.object({
      question: z.string(),
      answer: z.string(),
    })).optional(),
    projects: z.array(z.object({
      name: z.string(),
      description: z.string(),
      images: z.array(z.string()).optional(),
    })).optional(),
    testimonials: z.array(z.string()).optional(),
  }),
});

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.date(),
    updatedDate: z.date().optional(),
    author: z.string().default('AccuRite Excavation'),
    heroImage: z.string().optional(),
    tags: z.array(z.string()).optional(),
    relatedServices: z.array(z.string()).optional(),
    relatedLocations: z.array(z.string()).optional(),
  }),
});

export const collections = { services, locations, blog };
```

- [ ] **Step 2: Create one service template file**

Create `src/content/services/residential-excavation.md` as a template:
```markdown
---
title: "Residential Excavation Services in Utah"
description: "Professional residential excavation for foundations, basements, grading, and site prep across the Wasatch Front."
slug: "residential-excavation"
keywords:
  primary: "residential excavation utah"
  secondary:
    - "home excavation ogden"
    - "basement dig utah"
    - "foundation excavation wasatch front"
faqs:
  - question: "How much does residential excavation cost in Utah?"
    answer: "Placeholder — to be written with research data."
  - question: "Do I need a permit for excavation in Ogden?"
    answer: "Placeholder — to be written with research data."
relatedServices:
  - "grading-site-prep"
  - "footings-foundations"
  - "septic-systems"
---

<!-- Content to be written using SEO Machine /research and /write commands -->
<!-- Target word count: TBD from competitive analysis -->
<!-- Must beat competitor benchmarks identified in Task 1 -->

Placeholder content — will be replaced with full SEO-optimized content.
```

- [ ] **Step 3: Create one location template file**

Create `src/content/locations/ogden.md` as a template:
```markdown
---
title: "Excavation Services in Ogden, UT"
description: "AccuRite Excavation provides residential and commercial excavation in Ogden, Utah. 25+ years of local experience. Call (801) 814-6975."
city: "Ogden"
county: "Weber"
metaTitle: "Excavation Contractor in Ogden, UT | AccuRite Excavation"
metaDescription: "Trusted Ogden excavation contractor with 25+ years experience. Residential, commercial, retaining walls, utilities. Call (801) 814-6975 for a free estimate."
localIntro: "Placeholder — unique Ogden-specific intro to be written."
permitInfo: "Placeholder — Ogden-specific permit requirements."
soilInfo: "Placeholder — Ogden-area soil conditions."
faqs:
  - question: "Do I need a permit for excavation in Ogden?"
    answer: "Placeholder"
  - question: "What type of soil is common in Ogden?"
    answer: "Placeholder"
projects: []
testimonials: []
---

<!-- Content to be written with unique local information -->
<!-- Must have 40-60% unique content vs other location pages -->

Placeholder content — will be replaced with unique Ogden-specific content.
```

- [ ] **Step 4: Verify collections build**

```bash
npm run build
```

Expected: Clean build, content collections recognized.

- [ ] **Step 5: Commit**

```bash
git add src/content/
git commit -m "feat: add content collection schemas and template files"
```

---

## Chunk 3: Core Components & Base Layout

### Task 7: Base Layout with SEO Infrastructure

**Files:**
- Create: `src/layouts/BaseLayout.astro`
- Create: `src/components/SchemaMarkup.astro`
- Create: `src/components/SEOHead.astro`

- [ ] **Step 1: Create SEOHead component**

Create `src/components/SEOHead.astro` — handles all meta tags, Open Graph, Twitter Cards, and canonical URLs:

```astro
---
interface Props {
  title: string;
  description: string;
  canonical?: string;
  ogImage?: string;
  ogType?: string;
  noindex?: boolean;
}

const {
  title,
  description,
  canonical = Astro.url.href,
  ogImage = '/images/og-default.jpg',
  ogType = 'website',
  noindex = false,
} = Astro.props;

import business from '../data/business.json';
const siteName = business.shortName;
---

<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{title}</title>
<meta name="description" content={description} />
<link rel="canonical" href={canonical} />
{noindex && <meta name="robots" content="noindex, nofollow" />}

<!-- Open Graph -->
<meta property="og:title" content={title} />
<meta property="og:description" content={description} />
<meta property="og:type" content={ogType} />
<meta property="og:url" content={canonical} />
<meta property="og:image" content={ogImage} />
<meta property="og:site_name" content={siteName} />

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content={title} />
<meta name="twitter:description" content={description} />
<meta name="twitter:image" content={ogImage} />

<!-- Favicons -->
<link rel="icon" type="image/svg+xml" href="/favicon.svg" />
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
<link rel="manifest" href="/site.webmanifest" />
```

- [ ] **Step 2: Create SchemaMarkup component**

Create `src/components/SchemaMarkup.astro` — generates JSON-LD structured data:

```astro
---
interface Props {
  type: 'home' | 'service' | 'location' | 'blog' | 'reviews' | 'page';
  data?: Record<string, any>;
}

const { type, data = {} } = Astro.props;

import business from '../data/business.json';
import services from '../data/services.json';
import locations from '../data/locations.json';

const siteUrl = 'https://accuriteexcavation.com';

// Organization schema (all pages)
const organization = {
  '@type': 'Organization',
  '@id': `${siteUrl}/#organization`,
  name: business.name,
  url: siteUrl,
  telephone: business.phone,
  address: {
    '@type': 'PostalAddress',
    streetAddress: business.address.street,
    addressLocality: business.address.city,
    addressRegion: business.address.state,
    postalCode: business.address.zip,
    addressCountry: 'US',
  },
};

// WebSite schema with SearchAction (all pages)
const website = {
  '@type': 'WebSite',
  '@id': `${siteUrl}/#website`,
  url: siteUrl,
  name: business.shortName,
  publisher: { '@id': `${siteUrl}/#organization` },
};

// HomeAndConstructionBusiness (homepage)
const localBusiness = {
  '@type': 'HomeAndConstructionBusiness',
  '@id': `${siteUrl}/#localbusiness`,
  name: business.name,
  url: siteUrl,
  telephone: business.phone,
  address: organization.address,
  geo: {
    '@type': 'GeoCoordinates',
    latitude: business.geo.latitude,
    longitude: business.geo.longitude,
  },
  openingHoursSpecification: Object.entries(business.hours)
    .filter(([, v]) => v !== 'Closed')
    .map(([day, hours]) => ({
      '@type': 'OpeningHoursSpecification',
      dayOfWeek: day.charAt(0).toUpperCase() + day.slice(1),
      opens: hours.split(' - ')[0],
      closes: hours.split(' - ')[1],
    })),
  aggregateRating: {
    '@type': 'AggregateRating',
    ratingValue: business.reviews.rating,
    reviewCount: business.reviews.count,
  },
  areaServed: locations.map(loc => ({
    '@type': 'City',
    name: loc.name,
    '@id': `https://en.wikipedia.org/wiki/${loc.name},_Utah`,
  })),
};

// Build breadcrumbs from current URL
const pathSegments = Astro.url.pathname.split('/').filter(Boolean);
const breadcrumbs = {
  '@type': 'BreadcrumbList',
  itemListElement: [
    { '@type': 'ListItem', position: 1, name: 'Home', item: siteUrl },
    ...pathSegments.map((seg, i) => ({
      '@type': 'ListItem',
      position: i + 2,
      name: data.breadcrumbName || seg.replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase()),
      item: `${siteUrl}/${pathSegments.slice(0, i + 1).join('/')}`,
    })),
  ],
};

// Assemble schema based on page type
let schemas = [organization, website, breadcrumbs];

if (type === 'home') {
  schemas.push(localBusiness);
}
if (type === 'service' && data.service) {
  schemas.push({
    '@type': 'Service',
    name: data.service.name,
    description: data.service.description,
    provider: { '@id': `${siteUrl}/#localbusiness` },
    areaServed: localBusiness.areaServed,
  });
}
// Additional types handled similarly

const jsonLd = {
  '@context': 'https://schema.org',
  '@graph': schemas,
};
---

<script type="application/ld+json" set:html={JSON.stringify(jsonLd)} />
```

- [ ] **Step 3: Create BaseLayout**

Create `src/layouts/BaseLayout.astro`:

```astro
---
interface Props {
  title: string;
  description: string;
  schemaType?: 'home' | 'service' | 'location' | 'blog' | 'reviews' | 'page';
  schemaData?: Record<string, any>;
  canonical?: string;
  ogImage?: string;
  ogType?: string;
  noindex?: boolean;
}

const {
  title,
  description,
  schemaType = 'page',
  schemaData = {},
  canonical,
  ogImage,
  ogType,
  noindex,
} = Astro.props;
---

<!DOCTYPE html>
<html lang="en">
  <head>
    <SEOHead
      title={title}
      description={description}
      canonical={canonical}
      ogImage={ogImage}
      ogType={ogType}
      noindex={noindex}
    />
    <SchemaMarkup type={schemaType} data={schemaData} />
    <!-- Google Fonts loaded here once font pairing is selected -->
    <!-- GA4 tracking script -->
    <!-- Cookie consent script -->
  </head>
  <body class="font-body text-charcoal bg-white">
    <Header />
    <Breadcrumbs />
    <main>
      <slot />
    </main>
    <Footer />
  </body>
</html>
```

Note: Import statements for Header, Footer, Breadcrumbs, SEOHead, SchemaMarkup to be added.

- [ ] **Step 4: Verify layout builds**

```bash
npm run build
```

- [ ] **Step 5: Commit**

```bash
git add src/layouts/ src/components/SEOHead.astro src/components/SchemaMarkup.astro
git commit -m "feat: add BaseLayout with SEO head and schema markup"
```

### Task 8: Header Component

**Files:**
- Create: `src/components/Header.astro`
- Create: `public/js/mobile-menu.js`

- [ ] **Step 1: Create Header component**

Create `src/components/Header.astro`:
- Logo (left)
- Main navigation (center): Services dropdown, Locations dropdown, About, Gallery, Reviews, Contact
- Phone number + "Request Quote" button (right)
- Sticky positioning
- Mobile: hamburger menu with slide-out nav
- Click-to-call on phone number (all screen sizes, especially mobile)
- ARIA labels on hamburger button and phone icon
- Keyboard-navigable dropdowns

Services dropdown links to all 10 service pages.
Locations dropdown links to all 18 location pages (or a subset + "View All").

- [ ] **Step 2: Create mobile menu JS**

Create `public/js/mobile-menu.js`:
- Vanilla JS, no framework
- Toggle hamburger menu open/close
- Trap focus within open menu (accessibility)
- Close on Escape key
- Prevent body scroll when menu open
- Manage aria-expanded attribute

- [ ] **Step 3: Test header**

Create a temporary `src/pages/index.astro` that uses BaseLayout to verify:
- Header renders correctly
- Navigation links work
- Mobile menu toggles
- Phone number is clickable
- Sticky behavior works on scroll

```bash
npm run dev
```

Manually verify in browser at `http://localhost:4321`.

- [ ] **Step 4: Commit**

```bash
git add src/components/Header.astro public/js/mobile-menu.js
git commit -m "feat: add sticky header with responsive nav and click-to-call"
```

### Task 9: Footer Component

**Files:**
- Create: `src/components/Footer.astro`

- [ ] **Step 1: Create Footer component**

Create `src/components/Footer.astro`:
- Full NAP from `business.json`
- Service links (all 10, from `services.json`)
- Location links (all 18, from `locations.json`)
- Social links (from `business.json`)
- License and insurance info
- Copyright with dynamic year
- Privacy Policy and Terms of Service links

All data pulled from JSON files — single source of truth.

- [ ] **Step 2: Verify footer renders with data**

```bash
npm run dev
```

Check that all links render, NAP is correct, license info displays.

- [ ] **Step 3: Commit**

```bash
git add src/components/Footer.astro
git commit -m "feat: add footer with NAP, service links, location links"
```

### Task 10: Reusable Components

**Files:**
- Create: `src/components/Hero.astro`
- Create: `src/components/Breadcrumbs.astro`
- Create: `src/components/ServiceCard.astro`
- Create: `src/components/TestimonialCard.astro`
- Create: `src/components/CTASection.astro`
- Create: `src/components/TrustBar.astro`
- Create: `src/components/FAQSection.astro`

- [ ] **Step 1: Create Hero component**

Props: headline, subheadline, ctaText, ctaLink, phoneNumber, backgroundImage
Renders: full-width hero with gradient overlay, H1, CTA buttons (phone + quote), responsive image.

- [ ] **Step 2: Create Breadcrumbs component**

Auto-generates breadcrumb trail from URL path. Uses `locations.json` and `services.json` to resolve slugs to display names. Renders semantic `<nav aria-label="Breadcrumb">` with schema-compatible markup.

- [ ] **Step 3: Create ServiceCard component**

Props: service (from services.json)
Renders: card with icon, service name, short description, link to service page.
Used on homepage and location pages.

- [ ] **Step 4: Create TestimonialCard component**

Props: review (from reviews.json)
Renders: star rating, review text, reviewer name. Clean card layout.

- [ ] **Step 5: Create CTASection component**

Props: headline, showForm (boolean), phoneNumber
Renders: CTA block with phone number (always), LeadConnector form embed (when showForm=true, lazy-loaded), noscript fallback showing phone number.

- [ ] **Step 6: Create TrustBar component**

Renders: horizontal bar with trust signals — "25+ Years", "E100 Licensed", "Fully Insured", Google rating badge. Used on homepage and can be added to any page.

- [ ] **Step 7: Create FAQSection component**

Props: faqs (array of {question, answer})
Renders: accordion-style FAQ with proper heading hierarchy. Each Q/A pair uses `<details>/<summary>` for native accessibility. No JS needed.

- [ ] **Step 8: Verify all components render**

Update temp `index.astro` to include all components. Check rendering.

```bash
npm run dev
```

- [ ] **Step 9: Commit**

```bash
git add src/components/
git commit -m "feat: add reusable components — Hero, Breadcrumbs, ServiceCard, TestimonialCard, CTA, TrustBar, FAQ"
```

---

## Chunk 4: Core Pages

### Task 11: Homepage

**Files:**
- Create/Modify: `src/pages/index.astro`

- [ ] **Step 1: Build homepage**

Using BaseLayout with `schemaType="home"`. Sections in order:
1. Hero (strong headline, phone CTA, quote button, background photo)
2. Trust bar
3. Service cards grid (all 10 services)
4. About teaser (brief company story + link)
5. Notable client logos
6. Testimonials grid (3 top reviews)
7. Service area map (static SVG placeholder — finalize in Task 17)
8. Final CTA with phone + form

All data from JSON files. No hardcoded business info.

- [ ] **Step 2: Verify homepage**

```bash
npm run dev
```

Check: all sections render, links work, responsive on mobile, phone number clickable, schema markup in source.

- [ ] **Step 3: Commit**

```bash
git add src/pages/index.astro
git commit -m "feat: build homepage with all sections"
```

### Task 12: About Page

**Files:**
- Create: `src/pages/about.astro`

- [ ] **Step 1: Build about page**

Sections:
1. Hero
2. Company history (1995 -> present) — pull from existing content files
3. Shawn's bio with photo
4. Team/crew photo
5. Equipment showcase
6. Licensing, insurance, certifications (E100, insured)
7. Notable clients and projects
8. Values/promise
9. CTA

- [ ] **Step 2: Verify and commit**

```bash
npm run dev
# Verify page renders correctly
git add src/pages/about.astro
git commit -m "feat: build about page with company history and credentials"
```

### Task 13: Contact Page

**Files:**
- Create: `src/pages/contact.astro`

- [ ] **Step 1: Build contact page**

Sections:
1. Hero
2. Phone number (prominent, click-to-call)
3. LeadConnector form embed (lazy-loaded)
4. Business hours (from business.json)
5. Address (from business.json)
6. Service area map

- [ ] **Step 2: Verify and commit**

```bash
git add src/pages/contact.astro
git commit -m "feat: build contact page with form and business info"
```

### Task 14: Reviews Page

**Files:**
- Create: `src/pages/reviews.astro`

- [ ] **Step 1: Build reviews page**

Schema type: `reviews` (includes AggregateRating + Review schemas)
Sections:
1. Hero with Google rating badge
2. All reviews from `reviews.json` (organized by service type if data allows)
3. CTA to leave a review (link to Google review page)
4. Final CTA with phone

- [ ] **Step 2: Verify and commit**

```bash
git add src/pages/reviews.astro
git commit -m "feat: build reviews page with all testimonials and schema"
```

### Task 15: Gallery Page

**Files:**
- Create: `src/pages/gallery.astro`
- Create: `public/js/gallery-filter.js`

- [ ] **Step 1: Build gallery page**

Sections:
1. Hero
2. Filter buttons (by service type, by city — from JSON data)
3. Photo grid with project descriptions
4. Before/after comparisons where available

- [ ] **Step 2: Create gallery filter JS**

Vanilla JS that shows/hides gallery items based on selected filter. Uses `data-service` and `data-location` attributes on gallery items. No framework needed.

- [ ] **Step 3: Verify filtering works and commit**

```bash
git add src/pages/gallery.astro public/js/gallery-filter.js
git commit -m "feat: build filterable gallery page"
```

### Task 16: Utility Pages

**Files:**
- Create: `src/pages/404.astro`
- Create: `src/pages/privacy-policy.astro`
- Create: `src/pages/terms.astro`
- Create: `public/robots.txt`
- Create: `public/site.webmanifest`
- Create: `public/favicon.svg`

- [ ] **Step 1: Build 404 page**

Branded 404 with navigation, phone number CTA, links to top service pages. Friendly message. Uses BaseLayout with `noindex={true}`.

- [ ] **Step 2: Build privacy policy page**

Include UCPA compliance: clear privacy notice, opt-out mechanism for targeted advertising, disclosure of GA4 and LeadConnector cookies.

- [ ] **Step 3: Build terms of service page**

Standard terms appropriate for a contractor service business.

- [ ] **Step 4: Create robots.txt**

```
User-agent: *
Allow: /

Sitemap: https://accuriteexcavation.com/sitemap-index.xml
```

- [ ] **Step 5: Create web manifest and favicons**

Generate favicon set from AccuRite logo. Create `site.webmanifest` with brand colors and site name.

- [ ] **Step 6: Commit**

```bash
git add src/pages/404.astro src/pages/privacy-policy.astro src/pages/terms.astro public/robots.txt public/site.webmanifest public/favicon.svg
git commit -m "feat: add 404 page, privacy policy, terms, robots.txt, favicons"
```

---

## Chunk 5: Service & Location Page Templates

### Task 17: Service Page Template

**Files:**
- Create: `src/layouts/ServiceLayout.astro`
- Create: `src/pages/services/[...slug].astro`

- [ ] **Step 1: Create ServiceLayout**

Extends BaseLayout with `schemaType="service"`. Sections from spec:
1. Hero with service-specific headline + CTA
2. Problem/need section
3. How AccuRite does it (process, equipment, expertise)
4. Project gallery (filtered to this service from photos)
5. Testimonials (filtered by service from reviews.json)
6. FAQ section (from frontmatter)
7. Related services (internal links from frontmatter)
8. CTA with LeadConnector form

- [ ] **Step 2: Create dynamic route page**

Create `src/pages/services/[...slug].astro` that:
- Gets all service content collection entries
- Generates static paths for all 10 services
- Renders each using ServiceLayout
- Passes service data from both content collection and services.json

- [ ] **Step 3: Verify service pages generate**

```bash
npm run build
```

Expected: 10 service pages generated at `/services/[slug]`.

- [ ] **Step 4: Commit**

```bash
git add src/layouts/ServiceLayout.astro src/pages/services/
git commit -m "feat: add service page template with dynamic routing"
```

### Task 18: Location Page Template

**Files:**
- Create: `src/layouts/LocationLayout.astro`
- Create: `src/pages/locations/[...slug].astro`
- Create: `src/components/ServiceAreaMap.astro`

- [ ] **Step 1: Create ServiceAreaMap component**

Static SVG map of Northern Utah/Wasatch Front showing all 18 cities. Can highlight the current city when a `currentCity` prop is passed. Lightweight, no external API. Hand-crafted or generated SVG with city markers.

- [ ] **Step 2: Create LocationLayout**

Extends BaseLayout with `schemaType="location"`. Sections from spec:
1. Hero with city name + CTA
2. Local intro (unique city-specific content from frontmatter)
3. Services available in this area (ServiceCards from services.json)
4. Local projects completed with photos (from frontmatter)
5. Local testimonials (filtered by location from reviews.json)
6. Permit/regulation info (from frontmatter)
7. Nearby cities served (cross-links from locations.json `nearby` field)
8. CTA with form

- [ ] **Step 3: Create dynamic route page**

Create `src/pages/locations/[...slug].astro` that:
- Gets all location content collection entries
- Generates static paths
- Renders each using LocationLayout
- Passes location data from both content collection and locations.json

- [ ] **Step 4: Verify location pages generate**

```bash
npm run build
```

Expected: Location pages generated for each city with content.

- [ ] **Step 5: Commit**

```bash
git add src/layouts/LocationLayout.astro src/pages/locations/ src/components/ServiceAreaMap.astro
git commit -m "feat: add location page template with map and dynamic routing"
```

### Task 19: Blog Template

**Files:**
- Create: `src/layouts/BlogLayout.astro`
- Create: `src/pages/blog/[...slug].astro`
- Create: `src/pages/blog/index.astro`

- [ ] **Step 1: Create BlogLayout**

Extends BaseLayout with `schemaType="blog"`. Includes:
- Article header (title, date, author)
- Content area
- Related services links (from frontmatter)
- Related location links (from frontmatter)
- CTA (phone, link to service pages — NO form on blog posts per spec)

- [ ] **Step 2: Create blog index page**

Lists all blog posts with title, date, excerpt. Paginated if needed.

- [ ] **Step 3: Create dynamic route page**

Generates pages for each blog post in content collection.

- [ ] **Step 4: Verify and commit**

```bash
npm run build
git add src/layouts/BlogLayout.astro src/pages/blog/
git commit -m "feat: add blog template with index and dynamic routing"
```

---

## Chunk 6: Content Creation

### Task 20: Write Service Page Content (10 pages)

**Files:**
- Modify: `src/content/services/residential-excavation.md`
- Create: `src/content/services/retaining-walls.md`
- Create: `src/content/services/demolition-hauling.md`
- Create: `src/content/services/underground-utilities.md`
- Create: `src/content/services/septic-systems.md`
- Create: `src/content/services/grading-site-prep.md`
- Create: `src/content/services/footings-foundations.md`
- Create: `src/content/services/road-building.md`
- Create: `src/content/services/commercial-projects.md`
- Create: `src/content/services/government-projects.md`

- [ ] **Step 1: Write each service page using SEO Machine**

For each of the 10 services, use the SEO Machine workflow:
1. Run `/research [service topic]` to generate research brief
2. Run `/write [service topic]` using the content brief from Task 3
3. Run `/optimize [draft file]` for final SEO polish

Use existing content files from `~/Desktop/Accurite/web content/` as starting material where available:
- `residential-excavation.md` -> residential excavation
- `retaining-walls.md` -> retaining walls
- `demolition-hauling.md` -> demolition & hauling
- `underground-utilities.md` -> underground utilities
- `septic-systems.md` -> septic systems
- `commercial-government.md` -> commercial projects AND government projects

Each page must:
- Hit the target word count from competitive benchmarks
- Include all required sections (problem, solution, gallery, testimonials, FAQ, related services)
- Target the primary and secondary keywords from the keyword map
- Include 2-5 internal links per 1,000 words
- Have unique meta title and description

- [ ] **Step 2: Verify all service pages build and render**

```bash
npm run build
npm run preview
```

Check each service page: content renders, schema validates, internal links work.

- [ ] **Step 3: Commit**

```bash
git add src/content/services/
git commit -m "feat: add content for all 10 service pages"
```

### Task 21: Write Location Page Content (18 pages, prioritized)

**Files:**
- Modify: `src/content/locations/ogden.md`
- Create: `src/content/locations/[city-slug].md` (17 more)

- [ ] **Step 1: Write priority cities first (top 5-6)**

Start with Ogden, Layton, Bountiful, Farmington, Kaysville, Clearfield — these are the highest-priority cities.

For each, research and write:
- City-specific intro (local landmarks, neighborhoods, geography)
- Soil conditions and excavation challenges
- Municipal permit requirements (research city government websites)
- Projects completed in the area (from existing content/photos)
- City-specific FAQs
- All must have 40-60% unique content

- [ ] **Step 2: Write remaining cities**

For cities 7-18, follow the same process. Apply fallback strategy for low-project cities:
- Use broader regional project references
- Focus on unique municipal/zoning info
- Reference specific neighborhoods and developments
- If unique content can't hit 40-60%, defer that city page

- [ ] **Step 3: Verify all location pages build**

```bash
npm run build
```

Check: each location page has unique content, cross-links to nearby cities work, schema validates.

- [ ] **Step 4: Commit**

```bash
git add src/content/locations/
git commit -m "feat: add content for location pages across 18 cities"
```

### Task 22: Migrate Blog Posts

**Files:**
- Create: `src/content/blog/[slug].md` (one per migrated post)

- [ ] **Step 1: Migrate selected posts**

From the migration plan (Task 2), convert selected WordPress posts to Markdown with proper frontmatter. Add internal links to relevant service and location pages.

- [ ] **Step 2: Verify and commit**

```bash
npm run build
git add src/content/blog/
git commit -m "feat: migrate selected blog posts from WordPress"
```

---

## Chunk 7: Images, Redirects & Launch Prep

### Task 23: Image Optimization & Asset Pipeline

**Files:**
- Populate: `public/images/` with optimized photos
- Create: `public/images/logos/` for client logos

- [ ] **Step 1: Collect and organize images**

From available sources:
- `~/sites/accurite-excavation-ogden-ut/brand/images/` (13 brand photos)
- `~/Desktop/Accurite/pics/` (24 project/team photos)
- Brand logo files

Organize into:
- `public/images/hero/` — hero background photos
- `public/images/services/` — photos organized by service type
- `public/images/projects/` — before/after and project shots
- `public/images/team/` — crew, equipment, HQ photos
- `public/images/logos/` — AccuRite logo + client logos

- [ ] **Step 2: Optimize all images**

For each image:
- Convert to WebP format (keep JPG fallbacks)
- Generate responsive sizes (400w, 800w, 1200w)
- Compress to target < 100KB per image at 800w
- Add descriptive filenames (not `IMG_1234.jpg`)

Use a build-time image optimization tool or pre-process manually.

- [ ] **Step 3: Verify images load on pages**

```bash
npm run dev
```

Check: images appear on homepage, service pages, gallery. Lazy loading works. No layout shift.

- [ ] **Step 4: Commit**

```bash
git add public/images/
git commit -m "feat: add optimized project photos and brand assets"
```

### Task 24: 301 Redirect Map

**Files:**
- Create: `public/_redirects`

- [ ] **Step 1: Build complete redirect map**

Using the draft from Task 2, create the final Netlify `_redirects` file. Must include ALL URL types identified in the spec:

```
# Page redirects
/the-accurite-excavation-promise  /about  301
/our-services  /services/residential-excavation  301
/our-services/services  /services/residential-excavation  301
/our-services/services-2  /services/commercial-projects  301
/our-services/services-3  /services/government-projects  301
/request-a-quote  /contact  301
/accurite-gallery  /gallery  301
/the-accurite-excavation-reviews  /reviews  301
/the-accurite-excavation-promise/about-us-2  /about  301
/the-accurite-excavation-promise/about-us-2-2  /about  301

# Blog post redirects (migrate or redirect to service pages)
# [One line per existing post URL]

# Category/tag archive redirects
/category/*  /  301
/tag/*  /  301

# Pagination redirects
/page/*  /  301

# Feed redirects
/feed  /  301
/feed/  /  301
/rss  /  301
/comments/feed  /  301
/comments/feed/  /  301

# Media/attachment redirects
/attachment/*  /gallery  301

# Old sitemap redirects
/sitemap.xml  /sitemap-index.xml  301
/sitemap_index.xml  /sitemap-index.xml  301
/wp-sitemap.xml  /sitemap-index.xml  301

# WordPress shorthand parameter URLs
# Note: Netlify _redirects supports query params with specific syntax
# These need Netlify Edge Functions or splat rules

# Custom 404
/*  /404  404
```

- [ ] **Step 2: Verify redirects work locally**

```bash
npm run build
npx netlify-cli dev
```

Test key redirects by visiting old URLs. Verify 301 status codes.

- [ ] **Step 3: Commit**

```bash
git add public/_redirects
git commit -m "feat: add complete 301 redirect map for WordPress migration"
```

### Task 25: Analytics & Tracking Setup

**Files:**
- Modify: `src/layouts/BaseLayout.astro` (add tracking scripts)
- Create: `src/components/CookieConsent.astro`

- [ ] **Step 1: Add GA4 tracking**

Add Google Analytics 4 tag to BaseLayout head (load after cookie consent).

- [ ] **Step 2: Add Microsoft Clarity**

Add Clarity script to BaseLayout (free heatmaps/session recording).

- [ ] **Step 3: Create cookie consent component**

Lightweight cookie consent banner for UCPA compliance. Must:
- Appear on first visit
- Allow opt-out of analytics/advertising cookies
- Store preference in localStorage
- Only load GA4/Clarity after consent

- [ ] **Step 4: Add event tracking on CTAs**

Add `onclick` tracking events for:
- Phone number clicks (all instances)
- "Request Quote" button clicks
- Form submission events (if LeadConnector exposes them)

- [ ] **Step 5: Verify tracking fires**

```bash
npm run dev
```

Open browser DevTools Network tab, verify GA4 and Clarity requests fire after consent.

- [ ] **Step 6: Commit**

```bash
git add src/layouts/BaseLayout.astro src/components/CookieConsent.astro
git commit -m "feat: add GA4, Clarity, cookie consent, and CTA event tracking"
```

### Task 26: Full Build Verification

**Files:** None created — this is verification only.

- [ ] **Step 1: Full production build**

```bash
npm run build
```

Expected: Clean build, all pages generated (~60+ pages), no errors.

- [ ] **Step 2: Lighthouse audit**

Run Lighthouse on:
- Homepage
- One service page
- One location page
- Contact page

Targets: 95+ Performance, 95+ Accessibility, 95+ Best Practices, 95+ SEO.

- [ ] **Step 3: Schema validation**

Run Google Rich Results Test on:
- Homepage (HomeAndConstructionBusiness)
- One service page (Service)
- One location page (LocalBusiness + Service)
- One blog post (Article)
- Reviews page (AggregateRating)

All should pass with no errors.

- [ ] **Step 4: Accessibility check**

Run axe DevTools or similar on key pages. Verify:
- All images have alt text
- Color contrast passes (especially gold usage)
- Keyboard navigation works (header, menu, forms, FAQs)
- ARIA labels on icon-only buttons
- Focus management on mobile menu

- [ ] **Step 5: Internal link audit**

Verify no broken internal links. Run a local crawl or manually check:
- Service pages link to related services and locations
- Location pages cross-link to nearby cities
- Blog posts link to service and location pages
- Breadcrumbs are accurate on all page types

- [ ] **Step 6: Mobile testing**

Test responsive behavior on:
- iPhone (Safari)
- Android (Chrome)
- Tablet

Check: hamburger menu, click-to-call, form embed, gallery filter, all text readable.

- [ ] **Step 7: Commit any fixes**

```bash
git add -A
git commit -m "fix: address issues found in build verification"
```

---

## Chunk 8: Staging Deploy & Launch

### Task 27: Pre-Launch DNS & Email Verification

- [ ] **Step 1: Verify email/MX records**

```bash
dig MX accuriteexcavation.com
dig A accuriteexcavation.com
```

Document current MX records. Confirm email routing will not be affected by DNS changes. If MX records are on the same host as the website, plan to preserve them.

- [ ] **Step 2: Lower DNS TTL**

Log into DNS provider and lower TTL to 300 seconds (5 minutes). Wait 48 hours for propagation before proceeding with launch.

- [ ] **Step 3: Document current DNS state**

Record all current DNS records (A, CNAME, MX, TXT) for rollback reference.

### Task 28: Deploy to Staging

- [ ] **Step 1: Create GitHub repository**

```bash
cd /Users/rosswalker/sites/accurite-excavation-ogden-ut
gh repo create accurite-excavation --private --source=. --push
```

- [ ] **Step 2: Connect Netlify to GitHub**

Set up Netlify site connected to the GitHub repo. Configure:
- Build command: `npm run build`
- Publish directory: `dist`
- Deploy to staging URL first (auto-assigned Netlify URL or staging.accuriteexcavation.com)

- [ ] **Step 3: Verify staging deploy**

Visit staging URL. Run through:
- All pages load
- Navigation works
- Forms load (LeadConnector)
- Phone numbers clickable
- 301 redirects working (test old URLs)
- Schema markup validates
- Images load
- Mobile responsive

- [ ] **Step 4: Run full launch checklist**

From spec Section 8 Launch Checklist — verify every item:
- [ ] All 301 redirects verified
- [ ] Query parameter redirects tested
- [ ] Media/attachment URL redirects verified
- [ ] Schema markup validated (Rich Results Test)
- [ ] XML sitemap accessible
- [ ] All pages pass mobile-friendly test
- [ ] Core Web Vitals passing (PageSpeed Insights)
- [ ] WCAG 2.1 AA compliance verified
- [ ] GA4 tracking verified
- [ ] Microsoft Clarity installed
- [ ] Cookie consent functional
- [ ] Custom 404 page working

### Task 29: Production Launch

- [ ] **Step 1: Keep WordPress site running**

Move WordPress to subdomain (old.accuriteexcavation.com) as rollback option for 30 days.

- [ ] **Step 2: Point DNS to Netlify**

Update DNS A/CNAME records to point to Netlify. Preserve MX records exactly as documented in Task 27.

- [ ] **Step 3: Verify production site**

Once DNS propagates:
- Confirm site loads at accuriteexcavation.com
- Confirm HTTPS working
- Confirm redirects working on production domain
- Confirm email still works (send test email to Shawn)

- [ ] **Step 4: Submit to search engines**

- Submit new sitemap to Google Search Console
- Submit to Bing Webmaster Tools
- Request re-indexing of top 10 priority pages via URL Inspection tool

- [ ] **Step 5: Warm CDN cache**

Crawl all pages to populate Netlify CDN cache:
```bash
# Use wget or similar to hit every page
wget --spider --recursive --no-parent https://accuriteexcavation.com 2>&1 | grep "URL:"
```

- [ ] **Step 6: Update Google Business Profile**

Update any GBP links that pointed to old WordPress URLs. Verify all service and location links point to new URL structure.

- [ ] **Step 7: Commit launch notes**

```bash
echo "Launched $(date)" >> CHANGELOG.md
git add CHANGELOG.md
git commit -m "docs: record production launch date"
git push
```

### Task 30: Post-Launch Monitoring (First 30 Days)

- [ ] **Step 1: Set up monitoring**

- Configure GA4 alert for >20% traffic drop
- Set up daily ranking check for top 20 keywords
- Bookmark Search Console Index Coverage report

- [ ] **Step 2: Day 1 checks**

- Full-site crawl to validate all redirects on production
- Request re-indexing of priority pages
- Verify no email disruption
- Check Search Console for any immediate errors

- [ ] **Step 3: Week 1 checks**

- Daily ranking checks
- Daily Search Console crawl error review
- Monitor organic traffic in GA4
- Check Google Image Search traffic

- [ ] **Step 4: Weeks 2-4 checks**

- Weekly ranking checks
- Weekly crawl for redirect issues
- Compare traffic week-over-week
- If >30% drop sustained for 1 week, investigate and escalate

- [ ] **Step 5: Day 30 review**

- Full performance review vs. pre-launch baseline
- Decision: decommission WordPress backup or extend rollback window
- Document any issues and resolutions
