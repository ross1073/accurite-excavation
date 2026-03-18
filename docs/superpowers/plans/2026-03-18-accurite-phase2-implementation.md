# AccuRite Excavation Phase 2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add trust badges, images, contact form with HighLevel webhook, and full SEO overhaul to the AccuRite Excavation Astro 5 site — targeting page 1, position 1 across Weber, Davis, Salt Lake, Morgan, and Box Elder counties.

**Architecture:** Astro 5 static site with Tailwind v4, content collections for services/locations/blog, JSON data files for structured data. New ContactForm component posts to HighLevel webhook via fetch. Trust badges are AI-generated images. Real client photos + free-licensed landmark images for location pages. All images processed through Astro `<Image>` component from `astro:assets`.

**Tech Stack:** Astro 5, Tailwind v4, TypeScript, Netlify hosting, HighLevel webhook, Gemini image generator

**Spec:** `docs/superpowers/specs/2026-03-18-accurite-phase2-design.md`

---

## Task 1: Fix business.json and Hardcoded Date References

The `business.json` `founded` field was changed from 1995 to 2010 (16 years experience). Multiple pages have hardcoded "1995" and "three decades" references that are now wrong.

**Files:**
- Modify: `src/data/business.json`
- Modify: `src/pages/about.astro`
- Modify: `src/pages/index.astro`

- [ ] **Step 1: Verify business.json is correct**

`src/data/business.json` should already have `"founded": 2010` and `"yearsExperience": 16`. Verify this.

- [ ] **Step 2: Fix about.astro hardcoded references**

In `src/pages/about.astro`:
- Line 12: Change title from `"About AccuRite Excavation | Ogden, UT Since 1995"` to `"About AccuRite Excavation | Ogden, UT Since 2010"`
- Line 13: Change description `"since 1995"` to `"since 2010"`
- Line 17: Change hero headline from `"Family-Owned. Locally Trusted. Since 1995."` to `"Family-Owned. Locally Trusted. Since 2010."`
- Line 18: Change `"Over three decades"` to `"Over 16 years"`
- Line 53: Change `"over three decades"` to `"over 16 years"`

- [ ] **Step 3: Fix index.astro hardcoded references**

In `src/pages/index.astro`:
- Line 24: Change hero headline from `"Ogden's Trusted Excavation Contractor Since 1995"` to `"Ogden's Trusted Excavation Contractor Since 2010"`

- [ ] **Step 4: Add social URLs to business.json**

Add to `business.json`:
```json
"social": {
  "facebook": "",
  "google": "https://google.com/maps/place/AccuRite+Excavation+%26+Hauling,+Inc./data=!4m2!3m1!1s0x0:0x10e0b92e4cac2d87",
  "bbb": "https://www.bbb.org/us/ut/huntsville/profile/excavating-contractors/accurite-excavation-hauling-inc-1166-22284228"
}
```

- [ ] **Step 5: Build and verify**

Run: `cd ~/sites/accurite-excavation-ogden-ut && npm run build`
Expected: Build succeeds with no errors.

- [ ] **Step 6: Commit**

```bash
git add src/data/business.json src/pages/about.astro src/pages/index.astro
git commit -m "fix: update founded year to 2010, add BBB and Google profile URLs"
```

---

## Task 2: Contact Form Component + Tracking Script

Build the ContactForm component and form tracking script. This is the highest-priority item — it unblocks lead capture.

**Files:**
- Create: `src/components/ContactForm.astro`
- Create: `public/js/form-tracking.js`

- [ ] **Step 1: Create form tracking script**

Create `public/js/form-tracking.js`. This script:
1. On DOMContentLoaded, reads URL params and populates hidden form fields
2. Stores `landing_page` in sessionStorage on first visit
3. Sets `page_url` and `page_referrer` automatically
4. Handles form submission via `fetch()` POST to webhook URL
5. Shows inline success/error messages
6. Checks honeypot field before submitting

```javascript
(function() {
  // Store landing page on first visit
  if (!sessionStorage.getItem('landing_page')) {
    sessionStorage.setItem('landing_page', window.location.href);
  }

  document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('[data-contact-form]');
    forms.forEach(initForm);
  });

  function initForm(form) {
    const params = new URLSearchParams(window.location.search);

    // UTM params
    ['utm_source','utm_medium','utm_campaign','utm_content','utm_term'].forEach(key => {
      const field = form.querySelector(`[name="${key}"]`);
      if (field && params.get(key)) field.value = params.get(key);
    });

    // Google Ads params
    ['gclid','gbraid','wbraid','gad_source'].forEach(key => {
      const field = form.querySelector(`[name="${key}"]`);
      if (field && params.get(key)) field.value = params.get(key);
    });

    // Auto-set fields
    const pageUrl = form.querySelector('[name="page_url"]');
    if (pageUrl) pageUrl.value = window.location.href;

    const pageReferrer = form.querySelector('[name="page_referrer"]');
    if (pageReferrer) pageReferrer.value = document.referrer;

    const landingPage = form.querySelector('[name="landing_page"]');
    if (landingPage) landingPage.value = sessionStorage.getItem('landing_page') || '';

    // Submit handler
    form.addEventListener('submit', function(e) {
      e.preventDefault();

      // Honeypot check
      const honeypot = form.querySelector('[name="website"]');
      if (honeypot && honeypot.value) return;

      const submitBtn = form.querySelector('[type="submit"]');
      const originalText = submitBtn.textContent;
      submitBtn.disabled = true;
      submitBtn.textContent = 'Sending...';

      const formData = new FormData(form);
      const data = {};
      formData.forEach((value, key) => {
        if (key !== 'website') data[key] = value; // exclude honeypot
      });

      const webhookUrl = form.dataset.webhookUrl;

      fetch(webhookUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      })
      .then(response => {
        if (!response.ok) throw new Error('Network response was not ok');
        // Show success
        const formContainer = form.closest('[data-form-container]');
        formContainer.innerHTML = '<div class="text-center py-8"><div class="text-2xl font-bold text-green-700 mb-2">Thank You!</div><p class="text-gray-600">We\'ll be in touch within one business day. For immediate assistance, call <a href="tel:+18018146975" class="text-gold-dark font-semibold hover:underline">(801) 814-6975</a>.</p></div>';
      })
      .catch(error => {
        submitBtn.disabled = false;
        submitBtn.textContent = originalText;
        const errorDiv = form.querySelector('[data-form-error]');
        if (errorDiv) {
          errorDiv.textContent = 'Something went wrong. Please try again or call us directly.';
          errorDiv.classList.remove('hidden');
        }
      });
    });
  }
})();
```

- [ ] **Step 2: Create ContactForm.astro component**

Create `src/components/ContactForm.astro`. Props:
- `variant`: `"hero"` or `"section"` (default `"section"`)
- `heading`: optional string (default "Get Your Free Estimate")

The webhook URL is hardcoded in the component (not a prop) since it's a single endpoint:
`https://services.leadconnectorhq.com/hooks/uRXK3vFHqEQHApRA2dXE/webhook-trigger/f7eb4f71-39c0-4d90-8cd1-ef9760d49aa1`

The component renders:
- Heading (h2)
- Form with visible fields: Full Name, Phone, Email, Service Needed (dropdown from services.json), Project Description (textarea), Preferred Contact Method (radio)
- Hidden fields: utm_source, utm_medium, utm_campaign, utm_content, utm_term, gclid, gbraid, wbraid, gad_source, page_url, page_referrer, landing_page
- Honeypot field (hidden via CSS, not `type="hidden"`)
- Submit button: "Get Your Free Estimate"
- Error message div (hidden by default)
- `min-height: 400px` on form container for CLS prevention
- Phone number fallback below submit button

For `variant="hero"`: compact layout, tighter spacing, smaller heading
For `variant="section"`: full-width, centered, max-w-xl, more padding, dark charcoal background section

Import `services.json` for the dropdown options.

- [ ] **Step 3: Add form-tracking.js to BaseLayout**

In `src/layouts/BaseLayout.astro`, add before the closing `</body>` tag, after mobile-menu.js:
```html
<script src="/js/form-tracking.js" defer></script>
```

- [ ] **Step 4: Build and verify**

Run: `npm run build`
Expected: Build succeeds. The component exists but isn't used on any page yet.

- [ ] **Step 5: Commit**

```bash
git add src/components/ContactForm.astro public/js/form-tracking.js src/layouts/BaseLayout.astro
git commit -m "feat: add ContactForm component with HighLevel webhook + UTM tracking"
```

---

## Task 3: Integrate Contact Form on Pages

Replace all LeadConnector placeholders and add the form to pages per the placement strategy.

**Files:**
- Modify: `src/pages/contact.astro`
- Modify: `src/pages/free-estimate.astro`
- Modify: `src/components/CTASection.astro`
- Modify: `src/pages/services/[...slug].astro`
- Modify: `src/pages/locations/[...slug].astro`
- Modify: `src/pages/about.astro`
- Modify: `src/pages/blog/[...slug].astro`

- [ ] **Step 1: Replace contact.astro form placeholder**

In `src/pages/contact.astro`, replace the "Form Placeholder" div (lines 79-95) with:
```astro
<div>
  <ContactForm variant="hero" heading="Request a Free Estimate" />
</div>
```
Add import at top: `import ContactForm from '../components/ContactForm.astro';`

- [ ] **Step 2: Restructure free-estimate.astro with form**

Replace the entire form placeholder section in `src/pages/free-estimate.astro` (lines 40-57). Change to a two-column layout:
- Left: value prop text (phone number, why choose us bullets)
- Right: `<ContactForm variant="hero" />`

Add import: `import ContactForm from '../components/ContactForm.astro';`

- [ ] **Step 3: Update CTASection.astro to embed ContactForm**

In `src/components/CTASection.astro`, replace the empty LeadConnector placeholder (lines 41-48) with:
```astro
<ContactForm variant="section" heading="" />
```
Add import: `import ContactForm from './ContactForm.astro';`
This makes all pages that already use `<CTASection showForm={true} />` automatically get the real form. Affects: service pages, location pages.

- [ ] **Step 4: Add form to service pages hero area**

In `src/pages/services/[...slug].astro`, restructure the hero area to two-column:
- After the `<Hero>` and `<TrustBar>`, change the service content section (lines 56-62) to a two-column grid:
  - Left column: existing prose content (the `<Content />` markdown)
  - Right column: `<ContactForm variant="hero" />` (sticky sidebar)
- The testimonials, FAQs, related services sections continue below as full-width

Add import: `import ContactForm from '../../components/ContactForm.astro';`

- [ ] **Step 5: Add form section to about.astro**

In `src/pages/about.astro`, add before the final `<CTASection>`:
```astro
<ContactForm variant="section" heading="Ready to Start Your Project?" />
```
Change the existing `<CTASection>` to not show form (it doesn't currently).
Add import: `import ContactForm from '../components/ContactForm.astro';`

- [ ] **Step 6: Add form to blog posts**

In `src/pages/blog/[...slug].astro`, change `<CTASection />` to `<CTASection showForm={true} />` so the form appears via the updated CTASection component.

- [ ] **Step 7: Build and test form submission**

Run: `npm run build && npm run preview`
Test: Open each page type in browser, verify form renders, submit a test entry.
Expected: Form posts to webhook, success message appears.

- [ ] **Step 8: Commit**

```bash
git add src/pages/contact.astro src/pages/free-estimate.astro src/components/CTASection.astro src/pages/services/[...slug].astro src/pages/about.astro src/pages/blog/[...slug].astro
git commit -m "feat: integrate contact form across all pages — service hero sidebar, CTA sections, contact/estimate pages"
```

---

## Task 4: Image Pipeline — Copy and Optimize Real Photos

Set up the image directory structure, copy and deduplicate real photos from `~/Desktop/Accurite/`, and configure Astro Image.

**Files:**
- Create: `src/assets/images/` directory tree
- Create: `public/images/badges/` directory
- Create: `public/images/og/` directory
- Modify: `src/components/SEOHead.astro` (fix ogImage path)

- [ ] **Step 1: Create image directory structure**

```bash
mkdir -p src/assets/images/{hero,services,gallery,about,locations}
mkdir -p public/images/{badges,og}
```

- [ ] **Step 2: Copy and rename real photos**

Copy the highest-resolution version of each photo from `~/Desktop/Accurite/pics/` into the appropriate `src/assets/images/` subdirectory. Skip the "Do not use" folder. Rename files with SEO-friendly slugs:

**Hero images:**
- Pick best equipment/job site photo → `src/assets/images/hero/excavation-ogden-utah-hero.jpg`
- Pick a wide landscape shot → `src/assets/images/hero/wasatch-front-excavation.jpg`

**Service images (one per service page):**
- `Residential Ex/R1.jpg` (or best) → `src/assets/images/services/residential-excavation-utah.jpg`
- `Commercial Jobs/Orielly_s Complete Site Work.jpg` → `src/assets/images/services/commercial-excavation-utah.jpg`
- `Commercial Jobs/Military.jpg` → `src/assets/images/services/government-military-excavation.jpg`
- `Trenching & Utility/TU1.jpg` (or best) → `src/assets/images/services/underground-utilities-utah.jpg`
- `Dirt/D1.webp` (or best) → `src/assets/images/services/grading-land-clearing-utah.jpg`
- `Custom-Hauling.jpg` → `src/assets/images/services/hauling-delivery-utah.jpg`
- `Utilities-Septic-Install-scaled.jpg` → `src/assets/images/services/septic-systems-utah.jpg`
- (Demolition, Retaining Walls, Water Features will be generated in Task 5)

**Gallery images (best 15-20 across all categories):**
Select the highest-res, most visually compelling photos across all folders. Copy to `src/assets/images/gallery/` with descriptive names like `residential-basement-excavation-01.jpg`, `hill-afb-military-project.jpg`, etc.

**About images:**
- Best equipment fleet shot → `src/assets/images/about/accurite-equipment-fleet.jpg`
- (Team photos will be generated in Task 5)

**Logos:**
- `~/Desktop/Accurite/AccuRite Logo.png` → `src/assets/images/accurite-logo.png`
- `~/Desktop/Accurite/ACCURITE-LOGO.webp` → `src/assets/images/accurite-logo-square.webp`
- `~/Desktop/Accurite/white accurite logo.jpg` → `src/assets/images/accurite-logo-white.jpg`

- [ ] **Step 3: Fix ogImage path in SEOHead**

In `src/components/SEOHead.astro`, change line 15:
```
ogImage = '/images/og-default.jpg',
```
to:
```
ogImage = '/images/og/og-default.jpg',
```

- [ ] **Step 4: Build and verify images load**

Run: `npm run build`
Expected: Build succeeds. Astro processes images in `src/assets/images/`.

- [ ] **Step 5: Commit**

```bash
git add src/assets/images/ public/images/ src/components/SEOHead.astro
git commit -m "feat: add optimized real photos — hero, services, gallery, about, logos"
```

---

## Task 5: Generate Missing Images

Use the image generator to create the 12 images that don't exist as real photos.

**Files:**
- Create: 3 badge images in `public/images/badges/`
- Create: 1 demolition image in `src/assets/images/services/`
- Create: 3 retaining wall images in `src/assets/images/services/`
- Create: 2 water feature images in `src/assets/images/services/`
- Create: 2 team/crew images in `src/assets/images/about/`
- Create: 1 OG social card in `public/images/og/`

- [ ] **Step 1: Generate trust badge images (3)**

Use the MCP image generator tool or `~/seomachine/image_generator.py` to create:

1. `public/images/badges/utah-e100-licensed.webp` — Official Utah state seal style, circular with double gold border, text "STATE OF UTAH / LICENSED / E100 / CONTRACTOR", gold/cream color scheme. No phone numbers or URLs.
2. `public/images/badges/licensed-insured.webp` — Dark blue shield with checkmark, "LICENSED & INSURED" text, professional certification badge style. No phone numbers or URLs.
3. `public/images/badges/established-2010.webp` — Black circular heritage seal with gold AccuRite brand accents, "EST. 2010 / 16 YEARS EXPERIENCE" text. No phone numbers or URLs.

Each badge: square aspect ratio, ~400x400px source, will be displayed at ~100-120px.

- [ ] **Step 2: Generate service images (6)**

Generate with realistic excavation/construction style, Utah landscape:

1. `src/assets/images/services/demolition-contractor-utah.jpg` — Excavator demolishing a building, debris, Utah landscape in background
2. `src/assets/images/services/retaining-wall-boulder-utah.jpg` — Completed boulder/rock retaining wall in residential yard, Utah mountains visible
3. `src/assets/images/services/retaining-wall-block-utah.jpg` — Concrete block retaining wall, neatly finished, residential setting
4. `src/assets/images/services/retaining-wall-landscaping-utah.jpg` — Retaining wall with landscaping above and below, side view
5. `src/assets/images/services/waterfall-backyard-utah.jpg` — Backyard waterfall with natural rock work, pond below
6. `src/assets/images/services/pond-excavation-utah.jpg` — Excavated pond with rock edging, residential backyard

No phone numbers, URLs, or website text on any generated images.

- [ ] **Step 3: Generate team/about images (2)**

1. `src/assets/images/about/accurite-team-jobsite.jpg` — Construction crew (3-4 workers) standing next to excavation equipment on a job site, hard hats, Utah landscape. No phone numbers or URLs.
2. `src/assets/images/about/accurite-owner-equipment.jpg` — Single contractor/owner standing next to large excavator, professional pose, construction site. No phone numbers or URLs.

- [ ] **Step 4: Generate OG social card (1)**

1. `public/images/og/og-default.jpg` — 1200x630px, AccuRite Excavation branding, gold/charcoal color scheme, tagline "Ogden's Trusted Excavation Contractor", phone number (801) 814-6975. This is the one image where branding text IS appropriate.

- [ ] **Step 5: Verify all generated images exist and look good**

Check each file exists, opens correctly, and has no text/artifacts that shouldn't be there (per the "no phone on images" rule — except OG card).

- [ ] **Step 6: Commit**

```bash
git add public/images/badges/ public/images/og/ src/assets/images/services/ src/assets/images/about/
git commit -m "feat: add AI-generated images — trust badges, service photos, team shots, OG card"
```

---

## Task 6: Trust Badges Component

Create the TrustBadges component using the generated badge images + real platform badges (BBB, Google).

**Files:**
- Create: `src/components/TrustBadges.astro`
- Modify: `src/pages/index.astro`
- Modify: `src/pages/about.astro`
- Modify: `src/pages/contact.astro`

- [ ] **Step 1: Create TrustBadges.astro**

Create `src/components/TrustBadges.astro`:

```astro
---
import business from '../data/business.json';
---

<section class="bg-white py-10 lg:py-12">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex flex-wrap items-center justify-center gap-8 lg:gap-12">
      <!-- BBB A+ Rating - real branding -->
      <a href={business.social.bbb} target="_blank" rel="noopener" class="block" aria-label="BBB A+ Accredited Business">
        <!-- BBB badge as inline SVG or styled HTML for crisp rendering -->
        <!-- Blue #00529b / Gold #f0b323 -->
        <div class="w-[100px] h-[110px] bg-[#00529b] rounded-md p-2 flex flex-col items-center justify-center text-white text-center">
          <span class="font-serif text-lg font-bold tracking-wide">BBB</span>
          <div class="w-10 h-0.5 bg-[#f0b323] my-1"></div>
          <span class="font-serif text-[7px] uppercase tracking-widest leading-tight">Accredited<br/>Business</span>
          <div class="mt-1.5 bg-[#f0b323] text-[#00529b] font-bold text-xl w-8 h-8 rounded-full flex items-center justify-center font-serif">A+</div>
        </div>
      </a>

      <!-- Google Reviews - real branding -->
      <a href={business.social.google} target="_blank" rel="noopener" class="block" aria-label="Google Reviews - 4.9 stars">
        <div class="w-[100px] h-[110px] bg-white border-2 border-gray-200 rounded-lg p-2 flex flex-col items-center justify-center text-center">
          <!-- Google "G" logo SVG -->
          <svg class="w-7 h-7 mb-1" viewBox="0 0 24 24">
            <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 01-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z" fill="#4285F4"/>
            <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
            <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
            <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
          </svg>
          <div class="text-[#f4b400] text-sm tracking-wider">★★★★★</div>
          <div class="text-2xl font-bold text-charcoal">{business.reviews.rating}</div>
          <div class="text-[8px] text-gray-500">{business.reviews.count} Reviews</div>
        </div>
      </a>

      <!-- Utah Licensed E100 - generated badge image -->
      <div class="w-[100px] h-[110px] flex items-center justify-center">
        <img src="/images/badges/utah-e100-licensed.webp" alt="Utah State Licensed E100 Excavation Contractor" width="100" height="100" loading="lazy" class="max-w-full h-auto" />
      </div>

      <!-- Licensed & Insured - generated badge image -->
      <div class="w-[100px] h-[110px] flex items-center justify-center">
        <img src="/images/badges/licensed-insured.webp" alt="Licensed and Insured Excavation Contractor" width="100" height="100" loading="lazy" class="max-w-full h-auto" />
      </div>

      <!-- Established 2010 - generated badge image -->
      <div class="w-[100px] h-[110px] flex items-center justify-center">
        <img src="/images/badges/established-2010.webp" alt="Established 2010 - 16 Years Experience" width="100" height="100" loading="lazy" class="max-w-full h-auto" />
      </div>
    </div>
  </div>
</section>
```

- [ ] **Step 2: Add TrustBadges to homepage**

In `src/pages/index.astro`, add `import TrustBadges from '../components/TrustBadges.astro';` and place `<TrustBadges />` after `<TrustBar />` and before the services grid section.

- [ ] **Step 3: Add TrustBadges to about page**

In `src/pages/about.astro`, replace the bottom `<TrustBar />` (line 190) with `<TrustBadges />`.
Add import: `import TrustBadges from '../components/TrustBadges.astro';`

- [ ] **Step 4: Add TrustBadges to contact page**

In `src/pages/contact.astro`, add `<TrustBadges />` after the contact section, before the closing `</BaseLayout>`.
Add import: `import TrustBadges from '../components/TrustBadges.astro';`

- [ ] **Step 5: Build and verify**

Run: `npm run build`
Expected: Build succeeds, badges render on homepage, about, and contact pages.

- [ ] **Step 6: Commit**

```bash
git add src/components/TrustBadges.astro src/pages/index.astro src/pages/about.astro src/pages/contact.astro
git commit -m "feat: add TrustBadges component — BBB, Google, E100, Licensed & Insured, Est. 2010"
```

---

## Task 7: SEO Technical — Schema Markup Enhancements

Expand schema markup for better search visibility.

**Files:**
- Modify: `src/components/SchemaMarkup.astro`

- [ ] **Step 1: Read current SchemaMarkup.astro**

Read `src/components/SchemaMarkup.astro` fully to understand current schema types.

- [ ] **Step 2: Add county-level areaServed to LocalBusiness schema**

In the LocalBusiness schema section, add `areaServed` entries for all 5 counties alongside existing city entries:
```json
"areaServed": [
  { "@type": "AdministrativeArea", "name": "Weber County, Utah" },
  { "@type": "AdministrativeArea", "name": "Davis County, Utah" },
  { "@type": "AdministrativeArea", "name": "Salt Lake County, Utah" },
  { "@type": "AdministrativeArea", "name": "Morgan County, Utah" },
  { "@type": "AdministrativeArea", "name": "Box Elder County, Utah" }
]
```

- [ ] **Step 3: Add sameAs to Organization schema**

Add `sameAs` array to the organization/LocalBusiness schema:
```json
"sameAs": [
  "https://www.bbb.org/us/ut/huntsville/profile/excavating-contractors/accurite-excavation-hauling-inc-1166-22284228",
  "https://google.com/maps/place/AccuRite+Excavation+%26+Hauling,+Inc./data=!4m2!3m1!1s0x0:0x10e0b92e4cac2d87"
]
```

- [ ] **Step 4: Add GeoCircle/ServiceArea to location pages schema**

When `type === 'location'`, add a `ServiceArea` with `GeoCircle`:
```json
"areaServed": {
  "@type": "GeoCircle",
  "geoMidpoint": {
    "@type": "GeoCoordinates",
    "latitude": locationData.geo.lat,
    "longitude": locationData.geo.lng
  },
  "geoRadius": "24140"  // 15 miles in meters; use 40234 (25 miles) for rural
}
```
Check if the location is rural (Morgan, Eden, Huntsville) and use 25-mile radius, otherwise 15 miles.

- [ ] **Step 5: Add FAQPage schema to service pages**

When `type === 'service'` and faqs are provided, include `FAQPage` schema:
```json
{
  "@type": "FAQPage",
  "mainEntity": faqs.map(faq => ({
    "@type": "Question",
    "name": faq.question,
    "acceptedAnswer": {
      "@type": "Answer",
      "text": faq.answer
    }
  }))
}
```

- [ ] **Step 6: Build and validate schema**

Run: `npm run build`
Test: Open build output HTML, verify JSON-LD schema is correct.

- [ ] **Step 7: Commit**

```bash
git add src/components/SchemaMarkup.astro
git commit -m "feat: enhance schema — county areaServed, sameAs links, GeoCircle for locations, FAQPage"
```

---

## Task 8: SEO Technical — Footer, Internal Links, Outbound Links

Reorganize footer by county and add outbound authority links.

**Files:**
- Modify: `src/components/Footer.astro`

- [ ] **Step 1: Reorganize footer service areas by county**

In `src/components/Footer.astro`, replace the flat locations grid (lines 59-73) with county-organized groups:

```astro
<div>
  <p class="font-heading text-lg font-bold mb-4">Service Areas</p>
  {['Weber', 'Davis', 'Salt Lake', 'Morgan', 'Box Elder'].map(county => {
    const countyLocations = locations.filter(l => l.county === county);
    return countyLocations.length > 0 && (
      <div class="mb-4">
        <p class="text-xs font-semibold text-gold uppercase tracking-wider mb-1">{county} County</p>
        <ul class="grid grid-cols-2 gap-x-4 gap-y-1">
          {countyLocations.map(loc => (
            <li>
              <a href={`/locations/${loc.slug}`} class="text-sm text-gray-300 hover:text-gold transition-colors">
                {loc.name}
              </a>
            </li>
          ))}
        </ul>
      </div>
    );
  })}
</div>
```

- [ ] **Step 2: Add outbound authority links to footer**

Add a new section in the footer bottom bar or after the service areas:
```astro
<div class="flex items-center gap-4 text-sm text-gray-400">
  <a href={business.social.bbb} target="_blank" rel="noopener" class="hover:text-gold transition-colors">BBB Accredited</a>
  <span>&middot;</span>
  <a href={business.social.google} target="_blank" rel="noopener" class="hover:text-gold transition-colors">Google Reviews</a>
</div>
```

- [ ] **Step 3: Build and verify**

Run: `npm run build`
Expected: Footer shows locations grouped by county with outbound links.

- [ ] **Step 4: Commit**

```bash
git add src/components/Footer.astro
git commit -m "feat: reorganize footer by county, add BBB and Google outbound links"
```

---

## Task 9: Add Location Data for 22 New Cities

Add entries to `locations.json` for all new cities before creating content pages.

**Files:**
- Modify: `src/data/locations.json`
- Modify: `src/content/config.ts`

- [ ] **Step 1: Add heroImage field to locations collection schema**

In `src/content/config.ts`, add to the locations schema:
```typescript
heroImage: z.string().optional(),
landmarkImage: z.string().optional(),
```

- [ ] **Step 2: Add 22 new city entries to locations.json**

Add entries for each new city with accurate geo coordinates, population, county, nearby cities (referencing other slugs in the array), and tier (1=large city, 2=medium, 3=small).

New entries needed:
- Morgan County: morgan
- Davis County: bountiful, centerville, clinton, syracuse, west-point, fruit-heights, woods-cross, farmington
- Salt Lake County: salt-lake-city, sandy, west-jordan, south-jordan, draper, murray, midvale, west-valley-city, taylorsville, cottonwood-heights, holladay, riverton, herriman

Each entry follows existing format:
```json
{ "slug": "salt-lake-city", "name": "Salt Lake City", "county": "Salt Lake", "region": "Salt Lake Metro", "population": 200133, "geo": { "lat": 40.7608, "lng": -111.8910 }, "nearby": ["murray", "west-valley-city", "south-jordan"], "tier": 1 }
```

Look up accurate geo coordinates and population for each city. Set nearby cities to 3-4 adjacent cities that are also in our locations list.

- [ ] **Step 3: Build and verify**

Run: `npm run build`
Expected: Build succeeds. locations.json now has 40 entries.

- [ ] **Step 4: Commit**

```bash
git add src/data/locations.json src/content/config.ts
git commit -m "feat: add 22 new city entries to locations.json — Salt Lake, Davis, Morgan counties"
```

---

## Task 10: Source Location Landmark Images

Find and download one free-licensed landmark/landscape photo per location page from Unsplash, Pexels, or Wikimedia Commons.

**Files:**
- Create: `src/assets/images/locations/` — ~40 images

- [ ] **Step 1: Source landmark images for Weber County cities (12)**

For each city, search Unsplash/Pexels/Wikimedia for a relevant landmark photo. Download and save as `src/assets/images/locations/{slug}-landmark.jpg`.

Priority landmarks:
- ogden → Union Station or Historic 25th Street
- north-ogden → Ben Lomond Peak view
- south-ogden → Residential foothills
- roy → City park or Roy Complex
- riverdale → Riverdale Parkway area
- washington-terrace → Mountain view
- pleasant-view → North Ogden Divide
- farr-west → Agricultural/rural landscape
- west-haven → Wetlands/marshland area
- harrisville → Mountain backdrop
- eden → Powder Mountain or Nordic Valley
- huntsville → Pineview Reservoir

- [ ] **Step 2: Source landmark images for Box Elder County (3)**

- brigham-city → Box Elder Tabernacle or Peach Days sign
- perry → Perry Peak view
- willard → Willard Bay or Willard Peak

- [ ] **Step 3: Source landmark images for Davis County (11)**

- layton → Wasatch foothills from Layton
- kaysville → Kaysville city view
- clearfield → Hill Air Force Base area
- bountiful → Bountiful Temple or B mountain
- centerville → Centerville Park
- clinton → Clinton city/West Davis corridor
- syracuse → Antelope Island view
- west-point → Great Salt Lake view
- fruit-heights → Fruit Heights overlook
- woods-cross → Woods Cross refinery skyline
- farmington → Lagoon area or Farmington Creek trail

- [ ] **Step 4: Source landmark images for Salt Lake County (13)**

- salt-lake-city → City skyline or Capitol building
- sandy → Sandy city with mountains
- west-jordan → Jordan River Parkway
- south-jordan → Daybreak community
- draper → Point of the Mountain
- murray → Murray Park or city center
- midvale → Midvale area
- west-valley-city → West Valley skyline
- taylorsville → Taylorsville area
- cottonwood-heights → Cottonwood Canyon mouth
- holladay → Mt Olympus view from Holladay
- riverton → Riverton area, Oquirrh Mountains
- herriman → Herriman development with mountain backdrop

- [ ] **Step 5: Source landmark image for Morgan County (1)**

- morgan → Morgan Valley panorama with mountains

- [ ] **Step 6: Verify all 40 images exist and have appropriate licenses**

Check that every location slug has a corresponding `{slug}-landmark.jpg` in `src/assets/images/locations/`.

- [ ] **Step 7: Commit**

```bash
git add src/assets/images/locations/
git commit -m "feat: add 40 location landmark images — free commercial-use licensed"
```

---

## Task 11: Write 22 New Location Page Content

Create unique, locally-informed content for each new location page. This is the largest task and can be parallelized — each page is independent.

**CRITICAL: Content Quality Standard**
Each page must pass the test: "If you removed the city name from the H1, could you still tell which city the page is about?" If not, rewrite.

**Files:**
- Create: 22 markdown files in `src/content/locations/`

- [ ] **Step 1: Write Morgan County location page**

Create `src/content/locations/morgan.md` with unique content about Morgan Valley — rural setting, larger lots, septic systems common, rocky mountain soil, Morgan city permit office, specific neighborhoods/developments.

Frontmatter must match schema: title, description, city, county, metaTitle, metaDescription, localIntro, permitInfo, soilInfo, faqs (3-5 unique), heroImage, landmarkImage.

800-1,200 words of genuinely unique content in the markdown body.

- [ ] **Step 2: Write Davis County location pages (8)**

Create each of these with unique local content:
1. `bountiful.md` — older established neighborhoods, bench communities, proximity to SLC
2. `centerville.md` — small-town feel, Parrish Lane corridor, foothills
3. `clinton.md` — West Davis corridor, newer development, clay soil challenges
4. `syracuse.md` — Antelope Island proximity, Great Salt Lake area, newer subdivisions
5. `west-point.md` — rural-to-suburban transition, larger lots
6. `fruit-heights.md` — bench community, hillside challenges, premium lots
7. `woods-cross.md` — industrial/residential mix, refinery area, I-15 corridor
8. `farmington.md` — Station Park area, Lagoon, Farmington Creek, historic district

Each page: unique frontmatter, unique content, unique FAQs, unique permit/soil info.

- [ ] **Step 3: Write Salt Lake County location pages (13)**

Create each with unique local content:
1. `salt-lake-city.md` — state capital, diverse neighborhoods (Avenues, Sugar House, Rose Park), downtown development, historic foundations, city permitting
2. `sandy.md` — south valley, foothills, Sandy Civic Center area, proximity to canyons
3. `west-jordan.md` — Jordan River area, newer development west side, established east side
4. `south-jordan.md` — Daybreak master-planned community, rapid growth, Oquirrh Mountains
5. `draper.md` — Point of the Mountain, tech corridor, hillside lots, premium homes
6. `murray.md` — central valley, older homes needing foundation work, Murray Park area
7. `midvale.md` — revitalization, Union Park, I-15/I-215 interchange area
8. `west-valley-city.md` — largest west-side city, USANA area, diverse development
9. `taylorsville.md` — central location, established neighborhoods, Jordan River
10. `cottonwood-heights.md` — mouth of Cottonwood Canyons, premium hillside lots
11. `holladay.md` — affluent area, Mt Olympus views, established homes
12. `riverton.md` — southwest growth corridor, Oquirrh Mountain views
13. `herriman.md` — one of Utah's fastest-growing cities, new construction everywhere

Each page: unique frontmatter, unique content, unique FAQs, unique permit/soil info.

- [ ] **Step 4: Build and verify all 22 pages generate**

Run: `npm run build`
Expected: Build succeeds, 22 new location pages generated at `/locations/{slug}`.

- [ ] **Step 5: Commit**

```bash
git add src/content/locations/
git commit -m "feat: add 22 new location pages — unique local content for Salt Lake, Davis, Morgan counties"
```

---

## Task 12: Enhance Existing Location Pages

Update the 18 existing location pages to meet the new content quality standard and add landmark images.

**Files:**
- Modify: 18 files in `src/content/locations/`
- Modify: `src/pages/locations/[...slug].astro`

- [ ] **Step 1: Audit existing location page content**

Read each of the 18 existing `.md` files. Check:
- Do they have `soilInfo` and `permitInfo` filled in?
- Is the markdown body content unique and locally specific?
- Do they have FAQs?
- Do they meet the 800-word minimum?

- [ ] **Step 2: Enhance thin location pages**

For any pages that don't meet the content quality standard, rewrite/expand with genuinely local content. Focus on the most important cities first (tier 1: Ogden, Roy, Layton, Clearfield, Kaysville, Brigham City).

- [ ] **Step 3: Add landmark images to location page template**

In `src/pages/locations/[...slug].astro`, after the Hero and TrustBar, add a landmark image section:

```astro
<!-- Landmark Image -->
{entry.data.landmarkImage && (
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-8">
    <Image
      src={/* dynamic import for landmark image */}
      alt={`${entry.data.city}, Utah — excavation services by AccuRite`}
      class="w-full h-64 object-cover rounded-lg"
      loading="eager"
    />
  </div>
)}
```

Add import: `import { Image } from 'astro:assets';`

Note: Astro dynamic image imports require a mapping approach. Create a utility that maps slug to imported image, or use `import.meta.glob` to load all landmark images.

- [ ] **Step 4: Add Google Map embed to location template**

In `src/pages/locations/[...slug].astro`, add after the services section:

```astro
<!-- Google Map -->
<section class="py-8">
  <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="rounded-lg overflow-hidden" style="min-height: 300px;">
      <iframe
        src={`https://www.google.com/maps/embed/v1/place?key=YOUR_KEY&q=excavation+${encodeURIComponent(entry.data.city)}+Utah`}
        width="100%"
        height="300"
        style="border:0; min-height: 300px;"
        allowfullscreen=""
        loading="lazy"
        referrerpolicy="no-referrer-when-downgrade"
        title={`Map of ${entry.data.city}, Utah service area`}
      ></iframe>
    </div>
  </div>
</section>
```

Note: Google Maps Embed API requires an API key. Ask user for their Google Maps API key, or use a static map image as fallback.

- [ ] **Step 5: Build and verify**

Run: `npm run build`
Expected: All 40 location pages build with landmark images and maps.

- [ ] **Step 6: Commit**

```bash
git add src/content/locations/ src/pages/locations/[...slug].astro
git commit -m "feat: enhance existing location pages + add landmark images and maps to template"
```

---

## Task 13: Service Page Enhancements — Images, "Areas We Serve", Internal Links

Add hero images to service pages and the "Areas We Serve" section for internal linking.

**Files:**
- Modify: `src/pages/services/[...slug].astro`
- Modify: 10 service content `.md` files (add/verify FAQs, verify content depth)

- [ ] **Step 1: Add hero image to service page template**

In `src/pages/services/[...slug].astro`, replace the compact Hero with an image-backed hero. Use `entry.data.heroImage` to load the appropriate image:

```astro
{entry.data.heroImage && (
  <div class="relative">
    <Image
      src={/* mapped service hero image */}
      alt={entry.data.title + ' in Utah'}
      class="w-full h-72 lg:h-96 object-cover"
      loading="eager"
    />
    <div class="absolute inset-0 bg-charcoal/60 flex items-center">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-white">
        <h1 class="font-heading text-3xl lg:text-4xl font-bold">{entry.data.title}</h1>
        <p class="mt-2 text-lg text-gray-200 max-w-2xl">{entry.data.description}</p>
      </div>
    </div>
  </div>
)}
```

- [ ] **Step 2: Add "Areas We Serve" section to service page template**

After the Related Services section and before the CTA, add:

```astro
<!-- Areas We Serve -->
<section class="py-12 lg:py-16">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <h2 class="font-heading text-2xl font-bold text-charcoal text-center mb-8">
      Areas We Serve for {serviceJson?.shortName || entry.data.title}
    </h2>
    <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3 max-w-4xl mx-auto">
      {locationsData.filter(l => l.tier <= 2).map(loc => (
        <a
          href={`/locations/${loc.slug}`}
          class="px-4 py-2 border border-gray-200 rounded-lg text-sm text-gray-600 hover:border-gold-dark hover:text-gold-dark transition-colors text-center"
        >
          {loc.name}, UT
        </a>
      ))}
    </div>
    <p class="mt-4 text-sm text-gray-500 text-center">
      <a href="/locations" class="text-gold-dark hover:underline">View all service areas →</a>
    </p>
  </div>
</section>
```

Import `locationsData` if not already imported (it isn't currently in services template — add it).

- [ ] **Step 3: Verify service page content depth**

Read each of the 10 service `.md` files. Verify:
- FAQs exist (3-5 per page) — add if missing
- Content is 1,500+ words — expand if thin
- `heroImage` frontmatter field is set
- `relatedServices` frontmatter is populated

- [ ] **Step 4: Build and verify**

Run: `npm run build`
Expected: Service pages have hero images, "Areas We Serve" section, and all link to location pages.

- [ ] **Step 5: Commit**

```bash
git add src/pages/services/[...slug].astro src/content/services/
git commit -m "feat: add hero images and Areas We Serve section to service pages"
```

---

## Task 14: Blog Internal Links + Outbound Links on About Page

Add internal links from blog posts to service/location pages, and outbound authority links to about page.

**Files:**
- Modify: 5 blog content `.md` files in `src/content/blog/`
- Modify: `src/pages/about.astro`

- [ ] **Step 1: Add contextual internal links to existing blog posts**

Read each of the 5 blog posts. Add in-content markdown links to:
- 2+ relevant service pages (e.g., `[residential excavation](/services/residential-excavation)`)
- 2+ relevant location pages (e.g., `[excavation services in Ogden](/locations/ogden)`)

Links should be contextual and natural — woven into existing sentences, not bolted on.

- [ ] **Step 2: Add outbound links to about page**

In `src/pages/about.astro`, add to the credentials section:
- Link to BBB profile: `<a href="${business.social.bbb}" target="_blank" rel="noopener">BBB Accredited Business</a>`
- Link to Utah DOPL license verification (use https://dopl.utah.gov/): mention E100 license links to state verification
- Link to Google Business Profile

Import `business` data (already imported).

- [ ] **Step 3: Build and verify**

Run: `npm run build`
Expected: Blog posts have internal links, about page has outbound authority links.

- [ ] **Step 4: Commit**

```bash
git add src/content/blog/ src/pages/about.astro
git commit -m "feat: add internal links to blog posts, outbound authority links on about page"
```

---

## Task 15: Add Images to Existing Pages

Wire up the Astro `<Image>` component on pages that need images — homepage hero, about page, gallery.

**Files:**
- Modify: `src/pages/index.astro`
- Modify: `src/pages/about.astro`
- Modify: `src/pages/gallery.astro`
- Modify: `src/components/Hero.astro`

- [ ] **Step 1: Add hero background image to Hero component**

In `src/components/Hero.astro`, add an optional `backgroundImage` prop. When provided, render the hero with an image background + dark overlay instead of a solid color background.

- [ ] **Step 2: Pass hero image on homepage**

In `src/pages/index.astro`, import the hero image and pass it to the Hero component:
```astro
import heroImage from '../assets/images/hero/excavation-ogden-utah-hero.jpg';
```

- [ ] **Step 3: Add images to about page**

In `src/pages/about.astro`:
- Add team/crew image next to the "Meet Shawn" section
- Add equipment fleet image next to the equipment section
- Use Astro `<Image>` component with appropriate alt tags

- [ ] **Step 4: Populate gallery page with real photos**

In `src/pages/gallery.astro`, import all gallery images and render in a responsive grid with lightbox-style alt tags.

- [ ] **Step 5: Build and verify**

Run: `npm run build`
Expected: Images render on all pages, build output shows WebP conversion.

- [ ] **Step 6: Commit**

```bash
git add src/pages/index.astro src/pages/about.astro src/pages/gallery.astro src/components/Hero.astro
git commit -m "feat: add images to homepage hero, about page, and gallery"
```

---

## Task 16: Final SEO Audit

Run through all pages and verify meta tags, headings, schema, and performance.

**Files:**
- Various (fixes as needed)

- [ ] **Step 1: Audit meta titles and descriptions**

Check every page for:
- Unique title (50-60 chars, keyword-targeted)
- Unique meta description (150-160 chars, includes phone number)
- No duplicate titles across pages
- Title format: `[Keyword] | AccuRite Excavation [City]`

- [ ] **Step 2: Verify heading hierarchy**

Check every page template for:
- Single H1 per page
- Logical H2 > H3 nesting
- No heading level skipping
- H2s contain target keyword variations

- [ ] **Step 3: Verify canonical URLs**

Build the site and check that every page has a correct `<link rel="canonical">` pointing to itself.

- [ ] **Step 4: Verify XML sitemap**

After build, check `dist/sitemap-index.xml` includes all 40 location pages, 10 service pages, 5 blog posts, and all core pages.

- [ ] **Step 5: Run Lighthouse audit**

Run: `npm run build && npx serve dist`
Open Chrome DevTools Lighthouse on homepage, a service page, a location page.
Target: Performance > 90, SEO > 95, Accessibility > 90.

Fix any issues found.

- [ ] **Step 6: Verify redirects**

Check `public/_redirects` still works with Netlify. Test a few old WordPress URLs redirect correctly.

- [ ] **Step 7: Commit any fixes**

```bash
git add -A
git commit -m "fix: SEO audit fixes — meta tags, headings, schema, performance"
```

---

## Task 17: Final Build and Staging Deploy

Deploy to Netlify staging for final review before DNS cutover.

**Files:**
- No new files

- [ ] **Step 1: Final build**

Run: `npm run build`
Expected: Clean build, no warnings, all pages generated.

- [ ] **Step 2: Verify page count**

```bash
find dist -name "*.html" | wc -l
```
Expected: ~60+ HTML files (40 locations + 10 services + 5 blog + index + about + contact + free-estimate + gallery + reviews + 404 + privacy + terms).

- [ ] **Step 3: Deploy to Netlify staging**

Push the branch and deploy preview:
```bash
git push origin feature/redesign-implementation
```
Netlify should auto-deploy a preview URL from the branch.

- [ ] **Step 4: Manual review on staging**

Walk through key pages on the staging URL:
- Homepage: hero image, trust badges, services, testimonials
- A service page: form in sidebar, hero image, FAQs, "Areas We Serve"
- A location page: landmark image, unique content, map, nearby cities, form
- Contact page: form works, submit test entry
- About page: images, outbound links, trust badges
- Gallery: all photos load
- Mobile: responsive on phone-width

- [ ] **Step 5: Submit test form on staging**

Fill out and submit the contact form on the staging site. Verify it hits the HighLevel webhook with all fields including UTM params.

---

## Summary

| Task | Description | Dependencies |
|---|---|---|
| 1 | Fix business.json dates | None |
| 2 | ContactForm component + tracking | None |
| 3 | Integrate form on pages | Tasks 1, 2 |
| 4 | Copy/optimize real photos | None |
| 5 | Generate missing images | None |
| 6 | TrustBadges component | Task 5 (badges) |
| 7 | Schema markup enhancements | Task 1 (social URLs) |
| 8 | Footer + outbound links | Task 9 (new locations data) |
| 9 | Add 22 new city entries to locations.json | None |
| 10 | Source landmark images | None |
| 11 | Write 22 new location pages | Tasks 9, 10 |
| 12 | Enhance existing location pages | Task 10 |
| 13 | Service page enhancements | Tasks 4, 5 (images) |
| 14 | Blog internal links + about outbound links | Task 1 |
| 15 | Wire images to pages | Tasks 4, 5 |
| 16 | Final SEO audit | All previous tasks |
| 17 | Staging deploy | Task 16 |

**Parallelizable groups:**
- Tasks 1, 2, 4, 5, 9, 10 can all run in parallel (no dependencies)
- Tasks 3, 6, 7, 8, 11, 12, 13, 14, 15 depend on earlier tasks
- Tasks 16, 17 must run last
