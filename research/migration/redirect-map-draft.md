# AccuRite Excavation - 301 Redirect Map (Draft)

**Date:** 2026-03-12
**Total redirects needed:** 113 URLs + pattern rules

---

## New Site URL Structure

| Section | Pattern |
|---------|---------|
| Homepage | `/` |
| Services | `/services/[service-slug]` |
| Service Areas | `/service-area/[city-slug]` |
| About | `/about` |
| Contact | `/contact` |
| Gallery | `/gallery` |
| Blog | `/blog/[post-slug]` |
| Reviews | `/reviews` |
| Quote | `/free-estimate` |

---

## Page Redirects (11)

| Old URL | New URL | Notes |
|---------|---------|-------|
| `/` | `/` | Homepage to homepage |
| `/the-accurite-excavation-promise` | `/about` | About/promise content |
| `/request-a-quote` | `/free-estimate` | Quote form |
| `/our-services` | `/services` | Services parent |
| `/our-services/services` | `/services` | Services page 1 |
| `/our-services/services-2` | `/services` | Duplicate services |
| `/our-services/services-3` | `/services` | Duplicate services |
| `/the-accurite-excavation-promise/about-us-2` | `/about` | Duplicate about |
| `/the-accurite-excavation-promise/about-us-2-2` | `/about` | Duplicate about |
| `/accurite-gallery` | `/gallery` | Gallery |
| `/the-accurite-excavation-reviews` | `/reviews` | Reviews page |

## Post Redirects (27)

| Old URL | New URL | Notes |
|---------|---------|-------|
| `/our-work-past-projects` | `/gallery` | Project portfolio -> gallery |
| `/accurite-excavating-hauling-receives-praise-from-national-park-service` | `/blog/national-park-service-project` | High-value credibility post |
| `/commercial-construction-begins-here-precision-excavation-services` | `/services/commercial-projects` | -> service page |
| `/davis-county-waterline-construction` | `/blog/davis-county-waterline-project` | Project case study |
| `/excavation-companies-near-me` | `/` | Thin SEO post -> homepage |
| `/excavation-in-utah` | `/` | Thin SEO post -> homepage |
| `/exploring-our-legacy-accurite-excavations-commitment-as-utahs-excavation-experts` | `/about` | Legacy/history -> about |
| `/get-a-quote` | `/free-estimate` | Duplicate quote form |
| `/avoid-flooding-in-your-new-home` | `/blog/avoid-flooding-new-home` | Educational content |
| `/ogden-city-engineered-fill` | `/blog/ogden-engineered-fill-project` | Project case study |
| `/building-dreams-from-the-ground-up-residential-excavation-by-accurite-excavation-in-utah` | `/services/residential-excavation` | -> service page |
| `/safe-excavation-for-your-new-home-business-or-commercial-property` | `/services/residential-excavation` | -> service page |
| `/sand-rock-topsoil-and-fill` | `/services/hauling-delivery` | -> service page |
| `/sniper-tower-military-special-project` | `/blog/sniper-tower-military-project` | Military case study |
| `/shooting-range-at-camp-williams` | `/blog/camp-williams-shooting-range` | Military case study |
| `/the-importance-of-soil-stabilization` | `/blog/soil-stabilization-importance` | Educational content |
| `/steam-plant-hill-air-force-base-utah` | `/blog/hill-afb-steam-plant-project` | Military case study |
| `/utah-mortuary-excavation-project` | `/blog/utah-mortuary-excavation` | Commercial case study |
| `/utah-residential-excavation-contractor` | `/services/residential-excavation` | -> service page |
| `/what-makes-the-best-excavation-company-in-utah-heres-why-homeowners-trust-accurite-excavation` | `/about` | Trust content -> about |
| `/we-are-qualified-general-engineers-in-utah` | `/about` | Credentials -> about |
| `/we-have-an-e100-license` | `/about` | Licensing -> about |
| `/we-build-roads` | `/services/grading-land-clearing` | -> service page |
| `/we-have-military-project-experience` | `/services/government-projects` | -> service page |
| `/we-have-the-machine-power` | `/about` | Equipment -> about |
| `/we-install-replace-and-repair-residential-septic-tanks` | `/services/septic-systems` | -> service page |
| `/underground-utilities` | `/services/underground-utilities` | -> service page |

## Category Redirects (5)

| Old URL | New URL |
|---------|---------|
| `/category/commercial` | `/services/commercial-projects` |
| `/category/excavation` | `/services` |
| `/category/homepage` | `/` |
| `/category/residential` | `/services/residential-excavation` |
| `/category/uncategorized` | `/blog` |

## Tag Redirects (5)

| Old URL | New URL |
|---------|---------|
| `/tag/excavation` | `/services` |
| `/tag/excavator` | `/services` |
| `/tag/homepage` | `/` |
| `/tag/residential` | `/services/residential-excavation` |
| `/tag/utah` | `/` |

## Attachment Page Redirects (65)

All 65 attachment pages redirect to their parent post/page's new URL. Pattern-based rules:

| Pattern | Redirect To |
|---------|-------------|
| `/accurite-gallery/*` | `/gallery` |
| `/steam-plant-hill-air-force-base-utah/*` | `/blog/hill-afb-steam-plant-project` |
| `/the-importance-of-soil-stabilization/*` | `/blog/soil-stabilization-importance` |
| `/avoid-flooding-in-your-new-home/*` | `/blog/avoid-flooding-new-home` |
| `/utah-residential-excavation-contractor/*` | `/services/residential-excavation` |
| `/we-are-qualified-general-engineers-in-utah/*` | `/about` |
| `/we-have-the-machine-power/*` | `/about` |
| `/we-build-roads/*` | `/services/grading-land-clearing` |
| `/ogden-city-engineered-fill/*` | `/blog/ogden-engineered-fill-project` |
| `/we-have-an-e100-license/*` | `/about` |
| `/we-install-replace-and-repair-residential-septic-tanks/*` | `/services/septic-systems` |
| `/we-have-military-project-experience/*` | `/services/government-projects` |
| `/sniper-tower-military-special-project/*` | `/blog/sniper-tower-military-project` |
| `/shooting-range-at-camp-williams/*` | `/blog/camp-williams-shooting-range` |
| `/our-services/*` | `/services` |
| `/get-a-quote/*` | `/free-estimate` |
| `/commercial-construction-begins-here-precision-excavation-services/*` | `/services/commercial-projects` |
| `/accurite-excavating-hauling-receives-praise-from-national-park-service/*` | `/blog/national-park-service-project` |
| `/exploring-our-legacy-accurite-excavations-commitment-as-utahs-excavation-experts/*` | `/about` |

## WordPress Pattern Redirects

| Pattern | Redirect To | Notes |
|---------|-------------|-------|
| `/wp-admin/*` | `/` | Block admin URLs |
| `/wp-login.php` | `/` | Block login |
| `/wp-content/*` | Drop (410) | Media files served differently |
| `/feed` | Drop (410) | RSS feed |
| `/feed/*` | Drop (410) | RSS variants |
| `/*/feed` | Drop (410) | Per-page feeds |
| `/?p=*` | `/` | Query param permalinks |
| `/?page_id=*` | `/` | Query param permalinks |
| `/xmlrpc.php` | Drop (410) | WordPress API |
| `/wp-json/*` | Drop (410) | REST API |
| `/author/*` | `/about` | Author archives |
| `/page/*` | `/blog` | Pagination |
| `/*?replytocom=*` | Strip param | Comment reply URLs |

---

## Implementation Notes

1. Implement in Netlify `_redirects` file or `netlify.toml`
2. Use 301 (permanent) for all content redirects
3. Use 410 (Gone) for WordPress infrastructure URLs
4. Test every redirect before DNS cutover
5. Monitor 404s in Netlify analytics for 30 days post-launch
6. Check Google Search Console for crawl errors weekly
