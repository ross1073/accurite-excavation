# AccuRite Excavation - Content Migration Plan

**Date:** 2026-03-12

---

## Migration Strategy

All existing content will be **rewritten from scratch** for the new site. No content is copied verbatim -- everything gets improved with proper keyword targeting, depth, and structure. This document identifies what existing content provides source material worth building on.

---

## Tier 1: High-Value Content (Rewrite & Expand)

These posts contain unique information, real project details, or credibility signals that can't be recreated from research alone.

### Military/Government Case Studies
| Old URL | New Location | Source Value |
|---------|-------------|-------------|
| `/sniper-tower-military-special-project` | `/blog/sniper-tower-military-project` | Real project photos and details |
| `/shooting-range-at-camp-williams` | `/blog/camp-williams-shooting-range` | Real project photos and details |
| `/steam-plant-hill-air-force-base-utah` | `/blog/hill-afb-steam-plant-project` | Real project photos and details (6 images) |
| `/we-have-military-project-experience` | `/services/government-projects` | Credentials and project list |

**Action:** Extract project details, photos, and any specific achievements. Rewrite as detailed case studies with proper structure, schema markup, and E-E-A-T signals.

### Credibility/Credentials Content
| Old URL | New Location | Source Value |
|---------|-------------|-------------|
| `/accurite-excavating-hauling-receives-praise-from-national-park-service` | `/blog/national-park-service-project` | Unique third-party praise |
| `/we-are-qualified-general-engineers-in-utah` | `/about` | License details |
| `/we-have-an-e100-license` | `/about` | E100 license specifics |
| `/exploring-our-legacy-accurite-excavations-commitment-as-utahs-excavation-experts` | `/about` | Company history, license image |

**Action:** Consolidate credentials into the About page. National Park Service content becomes a standalone case study blog post.

### Educational Content
| Old URL | New Location | Source Value |
|---------|-------------|-------------|
| `/the-importance-of-soil-stabilization` | `/blog/soil-stabilization-importance` | Technical content with images |
| `/avoid-flooding-in-your-new-home` | `/blog/avoid-flooding-new-home` | Educational with 6 diagrams/figures |

**Action:** Rewrite with better structure, expanded depth, and proper keyword targeting. These demonstrate expertise (E-E-A-T).

---

## Tier 2: Medium-Value Content (Absorb Into Service Pages)

These posts contain service descriptions that should be incorporated into the new dedicated service pages rather than existing as standalone posts.

| Old URL | Absorb Into | Content to Extract |
|---------|-------------|-------------------|
| `/commercial-construction-begins-here-precision-excavation-services` | `/services/commercial-projects` | Commercial service descriptions |
| `/building-dreams-from-the-ground-up-residential-excavation-by-accurite-excavation-in-utah` | `/services/residential-excavation` | Residential service descriptions |
| `/safe-excavation-for-your-new-home-business-or-commercial-property` | `/services/residential-excavation` | Safety messaging |
| `/utah-residential-excavation-contractor` | `/services/residential-excavation` | Residential positioning |
| `/underground-utilities` | `/services/underground-utilities` | Utility service details |
| `/we-install-replace-and-repair-residential-septic-tanks` | `/services/septic-systems` | Septic service details |
| `/we-build-roads` | `/services/grading-land-clearing` | Road building capabilities |
| `/sand-rock-topsoil-and-fill` | `/services/hauling-delivery` | Materials and hauling |
| `/we-have-the-machine-power` | `/about` | Equipment inventory |
| `/davis-county-waterline-construction` | `/blog/davis-county-waterline-project` | Project details |
| `/ogden-city-engineered-fill` | `/blog/ogden-engineered-fill-project` | Project details |
| `/utah-mortuary-excavation-project` | `/blog/utah-mortuary-excavation` | Project details |

---

## Tier 3: Low-Value Content (Redirect Only, Do Not Migrate)

These URLs exist but contain no unique content worth preserving. They get 301 redirected to the most relevant new page.

| Old URL | Redirect To | Reason |
|---------|-------------|--------|
| `/excavation-companies-near-me` | `/` | Thin SEO-only content |
| `/excavation-in-utah` | `/` | Thin SEO-only content |
| `/what-makes-the-best-excavation-company-in-utah-heres-why-homeowners-trust-accurite-excavation` | `/about` | Generic trust content |
| `/get-a-quote` | `/free-estimate` | Duplicate of page |
| `/our-work-past-projects` | `/gallery` | Portfolio -> gallery |
| All `/our-services/*` duplicates | `/services` | Duplicate pages |
| All `/about-us-2*` duplicates | `/about` | Duplicate pages |
| All 65 attachment pages | Parent's new URL | WordPress artifacts |
| All category pages | Relevant section | Archive pages |
| All tag pages | Relevant section | Archive pages |

---

## Images to Migrate

### Gallery Images (~33 images from attachment URLs)
Located under `/accurite-gallery/` attachment URLs. Need to download original files from WordPress media library:
- Project photos (excavation sites, completed work)
- Equipment photos
- Rock wall installations
- Storm drain work
- Industrial/commercial projects
- Road construction
- Septic installations
- Grading work

### Project-Specific Images
- Steam plant / Hill AFB photos (6 images)
- Flooding prevention diagrams (6 figures)
- Soil stabilization photos (2 images)
- Camp Williams photos
- Sniper tower project photos
- National Park Service project photos
- License/certification images
- Commercial construction photos (2 images, added Nov 2025)

### Action Items
1. Download all original-resolution images from WordPress media library before decommissioning
2. Optimize for web (WebP format, responsive sizes)
3. Add descriptive alt text (current alt text is likely filename-based)
4. Organize by service type and project for the new gallery

---

## Content Gaps (New Content Needed)

The existing site has NO content for these planned sections:

- [ ] 18 location/service area pages (completely new)
- [ ] Individual service pages with depth (rock walls, grading, demolition, water features, ponds)
- [ ] FAQ content
- [ ] Process/how-it-works content
- [ ] Team/crew content
- [ ] Safety program details
- [ ] Environmental responsibility content
- [ ] Seasonal excavation tips
- [ ] Cost guide / what to expect content
- [ ] Permit and regulation guides by city
