# EMOD Safety & Commercial Content Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a safety/prequalification page and EMOD-focused blog post to capture uncontested commercial/B2B search traffic, then add internal links from existing content to reinforce topical authority.

**Architecture:** Three new content files (1 blog post, 1 blog post, 1 standalone page) plus internal link additions to 5 existing content files. The standalone safety page uses an Astro page file since it's not a service or location. Blog posts use the existing blog collection. All internal links follow the established pattern: `[anchor text](/path)` in markdown, `class="text-gold-dark hover:underline"` in Astro components.

**Tech Stack:** Astro 5, Markdown content collections, Tailwind CSS 4

---

### Task 1: Create the Safety & Prequalification Page

This is the centerpiece — a standalone page at `/safety/` that showcases AccuRite's 0.91 EMOD, safety credentials, and prequalification data. This page targets GCs and project managers searching for prequalified, low-EMR excavation subcontractors.

**Target keywords:** "prequalified excavation contractor Utah", "low EMR excavation contractor", "excavation contractor safety record Utah", "contractor prequalification Utah"

**Files:**
- Create: `src/pages/safety.astro`

- [ ] **Step 1: Create the safety page**

Create `src/pages/safety.astro` following the pattern of `about.astro` — imports BaseLayout, Hero (compact), TrustBar, CTASection. The page should contain these sections:

```astro
---
import BaseLayout from '../layouts/BaseLayout.astro';
import Hero from '../components/Hero.astro';
import TrustBar from '../components/TrustBar.astro';
import CTASection from '../components/CTASection.astro';

import business from '../data/business.json';
---

<BaseLayout
  title="Safety Record & Prequalification | AccuRite Excavation"
  description="AccuRite Excavation's 0.91 EMOD rating, safety credentials, and prequalification documentation. E100 licensed, bonded, and trusted by Utah general contractors."
  schemaType="page"
>
  <Hero
    headline="Safety Record & Contractor Prequalification"
    subheadline="0.91 Experience Modification Rate — 9% better than industry average. E100 licensed, bonded, and ready for your prequalification review."
    compact={true}
  />

  <TrustBar />

  <!-- EMOD Highlight Section -->
  <section class="py-12 lg:py-16">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="max-w-4xl mx-auto">
        <div class="bg-gray-50 border border-gray-200 rounded-lg p-8 lg:p-10 text-center mb-10">
          <div class="text-5xl lg:text-6xl font-bold text-gold-dark">0.91</div>
          <div class="mt-2 text-lg font-heading font-bold text-charcoal">Experience Modification Rate (EMOD)</div>
          <p class="mt-3 text-gray-600 max-w-xl mx-auto">
            An EMOD below 1.0 means fewer claims and a stronger safety record than the industry average. AccuRite's 0.91 rating reflects over 30 years of prioritizing crew safety and jobsite discipline.
          </p>
          <div class="mt-4 text-sm text-gray-500">Effective 11/17/2025 — verified by Beehive Insurance</div>
        </div>

        <h2 class="font-heading text-2xl lg:text-3xl font-bold text-charcoal">
          What EMOD Means for Your Project
        </h2>
        <div class="mt-6 space-y-4 text-gray-600 leading-relaxed">
          <p>
            The Experience Modification Rate is a workers' compensation metric that compares a contractor's actual claims history against the expected claims for their industry and payroll size. A score of 1.0 is the industry baseline. Below 1.0 means the contractor has fewer and less severe claims than average.
          </p>
          <p>
            For general contractors evaluating excavation subcontractors, EMOD is one of the most important prequalification criteria. A low EMOD means lower insurance risk on your project, fewer safety incidents that disrupt your schedule, and a subcontractor whose crew knows how to work safely in high-hazard conditions like deep trenches, unstable soils, and active job sites.
          </p>
          <p>
            Many commercial and government contracts in Utah require an EMOD below 1.0 as a minimum threshold for bid eligibility. AccuRite's 0.91 clears that bar and demonstrates a consistent pattern of safe operations — not a single lucky year.
          </p>
        </div>

        <h2 class="font-heading text-2xl lg:text-3xl font-bold text-charcoal mt-10">
          Prequalification Credentials
        </h2>
        <div class="mt-6 grid grid-cols-1 sm:grid-cols-2 gap-6">
          <div class="p-6 border border-gray-200 rounded-lg">
            <h3 class="font-heading text-lg font-bold text-charcoal">E100 Contractor License</h3>
            <p class="mt-2 text-gray-600 text-sm">Utah's highest-level excavation contractor designation, covering earthwork, grading, and underground utility installation. Verified through <a href="https://dopl.utah.gov/" target="_blank" rel="noopener" class="text-gold-dark hover:underline">Utah DOPL</a>.</p>
          </div>
          <div class="p-6 border border-gray-200 rounded-lg">
            <h3 class="font-heading text-lg font-bold text-charcoal">Commercial Bonding</h3>
            <p class="mt-2 text-gray-600 text-sm">Performance and payment bonds for commercial and <a href="/services/government-projects" class="text-gold-dark hover:underline">government contracts</a>. Bonding documentation available with bid submissions.</p>
          </div>
          <div class="p-6 border border-gray-200 rounded-lg">
            <h3 class="font-heading text-lg font-bold text-charcoal">Insurance Coverage</h3>
            <p class="mt-2 text-gray-600 text-sm">Full general liability, workers' compensation, and equipment coverage. Certificates of insurance provided before work begins on every project.</p>
          </div>
          <div class="p-6 border border-gray-200 rounded-lg">
            <h3 class="font-heading text-lg font-bold text-charcoal">Davis-Bacon Compliance</h3>
            <p class="mt-2 text-gray-600 text-sm">Certified payroll records and prevailing wage compliance on all federally funded projects. Experience with Army Corps of Engineers, National Park Service, and military installations.</p>
          </div>
        </div>

        <h2 class="font-heading text-2xl lg:text-3xl font-bold text-charcoal mt-10">
          Safety on the Job Site
        </h2>
        <div class="mt-6 space-y-4 text-gray-600 leading-relaxed">
          <p>
            Excavation is one of the most hazardous activities in construction. Trench collapses, cave-ins, struck-by incidents, and utility strikes are real risks on every project. Our safety record reflects the systems and habits we have built over three decades of managing those risks daily.
          </p>
          <ul class="list-disc pl-6 space-y-2">
            <li><strong>Trench safety:</strong> OSHA-compliant sloping, shoring, and trench box use on all excavations exceeding 5 feet in depth</li>
            <li><strong>Utility locating:</strong> Blue Stakes coordination and manual potholing before any dig</li>
            <li><strong>Equipment inspection:</strong> Daily pre-operation equipment checks before machines start</li>
            <li><strong>Site access control:</strong> Barricading, flagging, and traffic management on active job sites</li>
            <li><strong>Crew training:</strong> Experienced operators who understand soil behavior, load limits, and safe excavation practices in Northern Utah's clay-heavy and variable soil conditions</li>
          </ul>
        </div>

        <h2 class="font-heading text-2xl lg:text-3xl font-bold text-charcoal mt-10">
          For General Contractors
        </h2>
        <div class="mt-6 space-y-4 text-gray-600 leading-relaxed">
          <p>
            If you are assembling a bid team or prequalifying subcontractors for a <a href="/services/commercial-projects" class="text-gold-dark hover:underline">commercial</a> or <a href="/services/government-projects" class="text-gold-dark hover:underline">government project</a> in Utah, we can provide:
          </p>
          <ul class="list-disc pl-6 space-y-2">
            <li>Current EMOD letter (0.91 as of 11/17/2025)</li>
            <li>Certificate of insurance with your company listed as additional insured</li>
            <li>Bonding letter and capacity documentation</li>
            <li>E100 license verification</li>
            <li>Project references from government agencies and general contractors</li>
            <li>Detailed bid response with unit pricing from your civil plans</li>
          </ul>
          <p>
            We have worked with general contractors across Weber, Davis, Salt Lake, Box Elder, and Morgan counties on projects ranging from $50,000 site prep to multi-million dollar subdivisions. Our <a href="/about" class="text-gold-dark hover:underline">client list</a> includes the Army Corps of Engineers, National Park Service, Hill Air Force Base, Camp Williams, and municipal agencies throughout Northern Utah.
          </p>
        </div>
      </div>
    </div>
  </section>

  <CTASection
    headline="Request Prequalification Documents"
    subheadline="Call Shawn directly or request our EMOD letter, insurance certificates, and bid documents."
    showForm={true}
  />
</BaseLayout>
```

- [ ] **Step 2: Verify the page builds**

Run: `cd /Users/rosswalker/accurite-excavation && npm run build 2>&1 | tail -20`
Expected: Build completes successfully, `/safety/` route appears in output.

- [ ] **Step 3: Commit**

```bash
git add src/pages/safety.astro
git commit -m "feat: add safety & prequalification page with EMOD data"
```

---

### Task 2: Create Blog Post — "What is EMOD and Why It Matters When Choosing an Excavation Contractor"

Educational blog post targeting national informational keywords (2,000-4,000/mo volume for "experience modification rate") while funneling readers to AccuRite's safety page and commercial services.

**Target keywords:** "experience modification rate", "what is EMOD", "EMR rating construction", "what is a good EMR rate for a contractor"

**Files:**
- Create: `src/content/blog/what-is-emod-experience-modification-rate.md`

- [ ] **Step 1: Create the EMOD blog post**

Create `src/content/blog/what-is-emod-experience-modification-rate.md`:

```markdown
---
title: "What Is EMOD? Why Experience Modification Rate Matters When Hiring an Excavation Contractor"
metaTitle: "What Is EMOD (Experience Modification Rate)? Guide for Hiring Contractors"
description: "The Experience Modification Rate (EMOD/EMR) is one of the most important numbers to check before hiring an excavation contractor. Learn what it is, what a good score looks like, and why it matters for your project."
pubDate: 2026-03-26
author: "AccuRite Excavation"
tags: ["safety", "education", "commercial", "hiring guide"]
relatedServices: ["commercial-projects", "government-projects"]
relatedLocations: ["ogden", "salt-lake-city", "layton"]
---

If you are a general contractor evaluating excavation subcontractors or a property owner hiring for a significant project, there is one number that tells you more about a contractor's safety and reliability than almost anything else: their Experience Modification Rate.

It is called EMOD, EMR, or sometimes just "the mod." Whatever you call it, understanding what it means and what constitutes a good score can save you from hiring a contractor whose safety record could put your project at risk.

## What Is the Experience Modification Rate?

The Experience Modification Rate is a workers' compensation insurance metric calculated by the National Council on Compensation Insurance (NCCI) or a state rating bureau. It compares a contractor's actual workers' comp claims history to the expected claims for companies of similar size in the same industry.

The baseline is **1.0**. That represents the average claims experience for the industry.

- **Below 1.0:** The contractor has fewer and less severe claims than average. A score of 0.85 means their claims are 15% below the industry norm.
- **Above 1.0:** The contractor has more claims or more severe claims than average. A score of 1.15 means 15% worse than the norm.
- **Exactly 1.0:** Average for the industry.

The EMOD is recalculated annually based on the prior three years of claims data (excluding the most recent year). This means a contractor cannot fake a good score with one clean year — it reflects a sustained pattern.

## What Is a Good EMOD for an Excavation Contractor?

Excavation and earthwork are among the most hazardous construction trades. Trenching, grading near utilities, operating heavy equipment in close quarters, and working in unstable soils all carry real injury risk. Because of that baseline hazard, the industry average claims experience is already high.

An excavation contractor with an EMOD below 1.0 is performing meaningfully better than their peers on safety. Specific benchmarks:

- **0.75 or below:** Exceptional safety record. Uncommon in excavation due to the inherent hazards.
- **0.75 – 0.90:** Strong safety program. The contractor is managing risks well and has low claim frequency and severity.
- **0.90 – 1.0:** Better than average. Solid but not outstanding.
- **1.0 – 1.15:** Average to slightly below average. Not a disqualifier, but warrants deeper investigation into recent claims.
- **Above 1.15:** Elevated risk. Ask hard questions about what happened and what has changed.

AccuRite Excavation's current EMOD is **0.91** (effective 11/17/2025). For an excavation contractor with over 30 years of operations in Northern Utah, maintaining a sub-1.0 mod reflects a genuine culture of safety — not just a small payroll that happens to have avoided claims. You can see more detail on our [safety and prequalification page](/safety).

## Why EMOD Matters for Your Project

### It Predicts Future Performance

EMOD is based on three years of actual data. A contractor with a consistently low mod has internalized safe work practices. Their crews know how to [trench safely](/services/underground-utilities), manage equipment around other trades, and handle the soil conditions that cause problems on Wasatch Front job sites.

### It Affects Your Insurance Costs

On commercial projects, the general contractor's insurance and bonding costs can be affected by the subcontractors they use. A high-EMOD sub increases the risk profile of the project. Some commercial insurance policies specifically require that all subcontractors carry an EMOD below a certain threshold.

### It Is a Prequalification Gatekeeper

Many [government contracts](/services/government-projects) and large commercial projects require an EMOD below 1.0 as a minimum prequalification standard. Utah's Division of Facilities Construction and Management (DFCM), UDOT, and federal agencies like the Army Corps of Engineers all evaluate contractor safety metrics during prequalification.

If your excavation subcontractor cannot produce a current EMOD letter, they may not be eligible to work on your project — and you may not discover that until the bid is already submitted.

### It Reveals Management Quality

A low EMOD does not happen by accident. It requires consistent training, proper equipment maintenance, jobsite discipline, and a management team that takes safety seriously even when nobody is watching. These are the same traits that predict whether a contractor will show up on time, communicate problems early, and finish the work they committed to.

## How to Request and Verify an EMOD

Ask the contractor for their **current EMOD letter** from their insurance carrier. This is a standard document — any legitimate contractor can produce it within a day. The letter will show:

- The EMOD factor (the number itself)
- The effective date
- The insurance carrier's name and contact

If a contractor cannot or will not provide their EMOD letter, treat that the same way you would treat a contractor who cannot produce proof of insurance. It is a serious red flag.

You can also verify a contractor's workers' comp coverage status through Utah's [Workers' Compensation Fund](https://www.wccf.com/) or by contacting the carrier listed on their certificate of insurance.

## EMOD Is One Piece — Not the Whole Picture

EMOD is valuable because it is objective, standardized, and based on real data. But it should be evaluated alongside other factors:

- **[Licensing](/about):** Does the contractor hold the appropriate Utah license for the scope of work? For significant excavation, that means an E100 General Engineering Contractor license.
- **Bonding:** Can they provide performance and payment bonds at the required contract level?
- **Experience:** Have they completed projects similar to yours? In similar soil conditions? At similar scale?
- **References:** What do other general contractors say about working with them?

Our [guide to choosing an excavation contractor](/blog/how-to-choose-excavation-contractor-utah) covers these criteria in more detail.

## The Bottom Line

The EMOD is not a vanity metric. It is a data-backed indicator of how a contractor manages risk on real job sites over multiple years. When you are choosing an excavation subcontractor for a [commercial project](/services/commercial-projects) or [government contract](/services/government-projects) in Utah, ask for the number.

AccuRite Excavation's EMOD is 0.91. We have been doing excavation work in Northern Utah since 1995, and our safety record is a direct reflection of how we run our crews and our job sites. If you are putting together a bid and need a prequalified excavation sub, [contact us](/contact) or visit our [safety and prequalification page](/safety) for documentation.
```

- [ ] **Step 2: Verify the blog post builds**

Run: `cd /Users/rosswalker/accurite-excavation && npm run build 2>&1 | tail -20`
Expected: Build completes successfully, `/blog/what-is-emod-experience-modification-rate/` route appears.

- [ ] **Step 3: Commit**

```bash
git add src/content/blog/what-is-emod-experience-modification-rate.md
git commit -m "feat: add EMOD educational blog post targeting safety/prequalification keywords"
```

---

### Task 3: Create Blog Post — "How General Contractors Should Evaluate Excavation Subcontractors in Utah"

B2B-focused blog post targeting GCs and project managers searching for qualified excavation subs. Positions AccuRite as the authority on what to look for.

**Target keywords:** "excavation subcontractor Utah", "how to evaluate subcontractors", "subcontractor prequalification", "excavation subcontractor prequalification"

**Files:**
- Create: `src/content/blog/evaluate-excavation-subcontractors-utah.md`

- [ ] **Step 1: Create the GC-focused blog post**

Create `src/content/blog/evaluate-excavation-subcontractors-utah.md`:

```markdown
---
title: "How General Contractors Should Evaluate Excavation Subcontractors in Utah"
metaTitle: "Evaluating Excavation Subcontractors in Utah — GC Guide"
description: "A practical guide for general contractors evaluating excavation subcontractors in Utah. What to check, what to ask, and the prequalification criteria that separate reliable subs from risky ones."
pubDate: 2026-03-26
author: "AccuRite Excavation"
tags: ["commercial", "hiring guide", "safety", "general contractors"]
relatedServices: ["commercial-projects", "government-projects", "grading-land-clearing"]
relatedLocations: ["ogden", "salt-lake-city", "layton", "clearfield"]
---

As a general contractor in Utah, the excavation subcontractor you select sets the pace for every trade that follows. A sub who shows up late, underestimates the soil, or cuts corners on compaction creates problems that ripple through the entire project timeline. The time to avoid those problems is during prequalification — before the contract is signed.

This guide covers the criteria that matter most when evaluating excavation subcontractors along the Wasatch Front, from Weber County down through Salt Lake.

## Start With the EMOD

The [Experience Modification Rate](/blog/what-is-emod-experience-modification-rate) is the single most efficient screening tool for excavation subcontractors. It is an objective, data-driven measure of a contractor's safety performance over the prior three years.

Ask for the current EMOD letter from their insurance carrier. For excavation work — which involves trenching, heavy equipment, unstable soils, and confined spaces — you want an EMOD **below 1.0**. That is the industry average baseline, and a sub below it has demonstrated that their safety practices actually work.

AccuRite Excavation carries a [0.91 EMOD](/safety), verified by our insurance carrier. For an excavation contractor with 30+ years of operations, that reflects a sustained commitment to safety — not a statistical anomaly.

Why does this matter to you as a GC? Because a sub's safety record affects your project insurance costs, your OSHA exposure, and your schedule. A lost-time injury on the excavation phase does not just hurt the sub — it can shut down your entire site.

## Verify the License

In Utah, excavation contractors performing significant earthwork, utility installation, or public works projects must hold an **E100 General Engineering Contractor** license through the [Utah Division of Occupational and Professional Licensing (DOPL)](https://dopl.utah.gov/).

The E100 covers the full scope of commercial site work: mass grading, trenching, underground utility installation, and road subgrade preparation. Contractors operating under a lesser license classification may be qualified for limited residential work, but for [commercial](/services/commercial-projects) or [government projects](/services/government-projects), the E100 is the standard.

Verify the license online through DOPL before including any sub in your bid.

## Check Bonding Capacity

Excavation is often one of the largest line items in a site development budget. If your excavation sub defaults, you need bonding to cover the cost of completion and any unpaid suppliers or sub-tiers.

Ask for:
- **Payment bond** — protects material suppliers and lower-tier subs
- **Performance bond** — guarantees completion of the contracted scope
- **Bonding capacity** — can they bond at the level your project requires?

A sub who "does not carry bonds" or "can get one if needed" is not at the same level as one who bonds routinely. AccuRite maintains active bonding relationships and can provide bond documentation as part of our standard bid package.

## Evaluate Their Equipment

An excavation sub running one mid-size excavator and a rented dump truck is a different operation than one with a full fleet of owned equipment. For [commercial site work](/services/commercial-projects), you need confidence that the sub can handle the scope without equipment bottlenecks.

Ask what equipment they plan to mobilize for your project, whether they own or rent it, and what happens if a machine goes down. A sub who owns their fleet can swap equipment without waiting on a rental yard.

AccuRite runs a full fleet — multiple excavator sizes, dozers, scrapers, motor graders, compactors, dump trucks, and trenchers. We own our equipment, which means no rental delays and the ability to scale up when a project demands it.

## Ask About Wasatch Front Soil Experience

Northern Utah soil conditions are not forgiving of contractors who have not worked in them before. The Lake Bonneville sediments that underlie the valley floor from [Ogden](/locations/ogden) through [Salt Lake City](/locations/salt-lake-city) include expansive clays, variable sand layers, high water tables in low-lying areas, and occasional buried organics.

A sub who has been working these soils for years will give you specific answers about compaction methods, moisture management, and what to expect at different elevations and neighborhoods. A sub who gives generic answers may be working outside their experience.

We have been excavating in Weber, Davis, Salt Lake, Morgan, and Box Elder counties since 1995. We know what the soils do in [Roy](/locations/roy), [Layton](/locations/layton), the Ogden bench, and everywhere in between.

## Review Their Documentation Process

[Commercial excavation](/services/commercial-projects) and [government work](/services/government-projects) generate paperwork. Compaction test coordination, daily logs, certified payrolls on Davis-Bacon projects, change order documentation, lien waivers, and progress billing all need to be handled correctly and on time.

Ask the sub how they handle documentation. A sub who is organized administratively is usually organized in the field. A sub who is consistently late on paperwork is often consistently late on everything else.

## Check References From Other GCs

The most valuable references come from general contractors who have used the sub on projects similar to yours — similar scope, similar contract value, similar schedule pressure.

Ask specifically:
- Did they show up when they said they would?
- How did they handle unexpected conditions (rock, water, changed grades)?
- Was their billing accurate and timely?
- Would you use them again?

AccuRite has worked with general contractors across the Wasatch Front on everything from single-pad commercial site prep to multi-phase subdivision development. We are happy to provide references from GCs who know our work.

## The Prequalification Checklist

When you are evaluating excavation subs for a project, here is the short list of what to collect:

- **EMOD letter** (current year, from their insurance carrier) — [what to look for](/blog/what-is-emod-experience-modification-rate)
- **Certificate of insurance** (GL, workers' comp, auto, umbrella)
- **E100 license verification** (or appropriate license for scope)
- **Bonding letter** with available capacity
- **Equipment list** (owned vs. rented)
- **References** from 2-3 GCs on similar projects
- **Safety program documentation** (if your project requires it)

AccuRite can provide all of these documents as part of our standard prequalification package. Visit our [safety and prequalification page](/safety) to learn more, or [contact us](/contact) to request documentation for your project.

## Finding Qualified Excavation Subs in Utah

Beyond your existing network, qualified excavation subcontractors in Utah can be found through:

- **[AGC Utah](https://www.agc-utah.org/)** member directory
- **BuildingConnected** and **PlanHub** platforms
- **DFCM prequalified contractor list** (for state-funded projects)
- **Local bid solicitation services**

Or you can call us directly. AccuRite Excavation is based in [Ogden](/locations/ogden) and serves the entire Wasatch Front. We respond to formal bid invitations, informal quotes, and direct procurement requests. Call Shawn at (801) 814-6975 or [request an estimate](/free-estimate).
```

- [ ] **Step 2: Verify the blog post builds**

Run: `cd /Users/rosswalker/accurite-excavation && npm run build 2>&1 | tail -20`
Expected: Build completes successfully.

- [ ] **Step 3: Commit**

```bash
git add src/content/blog/evaluate-excavation-subcontractors-utah.md
git commit -m "feat: add GC-focused blog post on evaluating excavation subcontractors"
```

---

### Task 4: Add Internal Links From Existing Content to New Pages

Add contextual internal links from the 5 most relevant existing content files to the new safety page and blog posts. This reinforces topical authority and passes link equity to the new pages.

**Files:**
- Modify: `src/content/services/commercial-projects.md`
- Modify: `src/content/services/government-projects.md`
- Modify: `src/content/blog/how-to-choose-excavation-contractor-utah.md`
- Modify: `src/content/blog/hill-afb-steam-plant-project.md`
- Modify: `src/content/blog/how-much-does-excavation-cost-utah.md`

- [ ] **Step 1: Add EMOD/safety link to commercial-projects.md**

In `src/content/services/commercial-projects.md`, in the "Capabilities and Equipment" section (around line 68), find the paragraph about bonding and insurance and add a link to the safety page. Replace:

```markdown
**Commercial bonding and insurance:** We carry the bonding required for commercial contracts along with general liability and workers' compensation coverage. Your general contractor and project owner will receive certificates of insurance before work begins.
```

With:

```markdown
**Commercial bonding and insurance:** We carry the bonding required for commercial contracts along with general liability and workers' compensation coverage. Our [0.91 EMOD safety rating](/safety) reflects over 30 years of responsible operations. Your general contractor and project owner will receive certificates of insurance before work begins.
```

Also in the "Working With General Contractors" section (around line 101), find:

```markdown
AccuRite has worked with general contractors across Weber, Davis, and Box Elder counties on projects ranging from $50,000 site prep jobs to multi-million dollar subdivision developments. We're familiar with the documentation requirements, lien waiver processes, and scheduling demands of commercial construction.
```

Replace with:

```markdown
AccuRite has worked with general contractors across Weber, Davis, and Box Elder counties on projects ranging from $50,000 site prep jobs to multi-million dollar subdivision developments. We're familiar with the documentation requirements, lien waiver processes, and scheduling demands of commercial construction. For prequalification documentation including our EMOD letter, insurance certificates, and bonding capacity, visit our [safety and prequalification page](/safety).
```

- [ ] **Step 2: Add safety/EMOD link to government-projects.md**

In `src/content/services/government-projects.md`, in the "Credentials and Compliance" section (around line 36), after the Insurance line, add a new credential entry:

Find:

```markdown
**Insurance:** Full general liability, workers' compensation, and equipment coverage. Certificates of insurance are provided as required by contract specifications.
```

Replace with:

```markdown
**Insurance:** Full general liability, workers' compensation, and equipment coverage. Certificates of insurance are provided as required by contract specifications.

**Experience Modification Rate (EMOD):** Our current EMOD is [0.91](/safety) — 9% below the industry average. This safety metric is a standard prequalification requirement on government and military contracts.
```

- [ ] **Step 3: Add EMOD/safety links to how-to-choose-excavation-contractor-utah.md**

In `src/content/blog/how-to-choose-excavation-contractor-utah.md`, in the "Check for Insurance" section (around line 26), after the workers' compensation bullet, add a paragraph:

Find:

```markdown
A legitimate contractor will provide a current certificate without hesitation. If a contractor is reluctant to provide proof of insurance, that is a serious red flag.
```

Replace with:

```markdown
A legitimate contractor will provide a current certificate without hesitation. If a contractor is reluctant to provide proof of insurance, that is a serious red flag.

For commercial projects, also ask for the contractor's **Experience Modification Rate (EMOD)**. This workers' comp metric reveals their actual safety record over the past three years. An EMOD below 1.0 means the contractor is safer than the industry average. Learn more about [what EMOD means and what a good score looks like](/blog/what-is-emod-experience-modification-rate).
```

Also in the "What Good Looks Like" section (around line 93), update the AccuRite paragraph:

Find:

```markdown
AccuRite has been doing this work in northern Utah since 1995. Our work spans [residential excavation](/services/residential-excavation), grading and drainage, retaining walls, and government contracts. We are based in Ogden, and we know the soil, the terrain, and the local jurisdictions across Weber, Davis, and Salt Lake counties.
```

Replace with:

```markdown
AccuRite has been doing this work in northern Utah since 1995. Our work spans [residential excavation](/services/residential-excavation), grading and drainage, retaining walls, and government contracts. We carry a [0.91 EMOD safety rating](/safety) and are based in Ogden. We know the soil, the terrain, and the local jurisdictions across Weber, Davis, and Salt Lake counties.
```

- [ ] **Step 4: Add safety link to hill-afb-steam-plant-project.md**

In `src/content/blog/hill-afb-steam-plant-project.md`, in the final section "What Makes Government Utility Work Different" (around line 44), find:

```markdown
AccuRite holds the [E100 General Engineering Contractor license](/services/government-projects) that government utility work in Utah requires. We have built the administrative processes to handle government project documentation without it slowing down our field work.
```

Replace with:

```markdown
AccuRite holds the [E100 General Engineering Contractor license](/services/government-projects) that government utility work in Utah requires. Our [0.91 EMOD safety rating](/safety) meets the prequalification thresholds that federal and military contracts demand. We have built the administrative processes to handle government project documentation without it slowing down our field work.
```

- [ ] **Step 5: Add safety link to how-much-does-excavation-cost-utah.md**

Read the full file first. Find a natural place where insurance/contractor quality is discussed and add a brief mention linking to the safety page. This is a high-traffic page — even a brief contextual link passes value.

The cost blog post discusses OSHA and safety. Find the section that mentions OSHA or safety compliance and add a link. If the post mentions hiring a qualified contractor or checking credentials, link to the EMOD blog post there.

- [ ] **Step 6: Verify all modified files build correctly**

Run: `cd /Users/rosswalker/accurite-excavation && npm run build 2>&1 | tail -20`
Expected: Build completes successfully with no errors.

- [ ] **Step 7: Commit**

```bash
git add src/content/services/commercial-projects.md src/content/services/government-projects.md src/content/blog/how-to-choose-excavation-contractor-utah.md src/content/blog/hill-afb-steam-plant-project.md src/content/blog/how-much-does-excavation-cost-utah.md
git commit -m "seo: add internal links from existing content to new safety page and EMOD blog posts"
```

---

### Task 5: Add Safety Page to Site Navigation

Add the safety page to the header navigation so it is discoverable and passes link equity from every page on the site.

**Files:**
- Modify: `src/components/Header.astro`

- [ ] **Step 1: Add Safety link to desktop nav**

In `src/components/Header.astro`, find the desktop navigation links (around line 84-87):

```html
<a href="/about" class="text-sm font-medium text-charcoal hover:text-gold-dark transition-colors">About</a>
<a href="/gallery" class="text-sm font-medium text-charcoal hover:text-gold-dark transition-colors">Gallery</a>
```

Replace with:

```html
<a href="/about" class="text-sm font-medium text-charcoal hover:text-gold-dark transition-colors">About</a>
<a href="/safety" class="text-sm font-medium text-charcoal hover:text-gold-dark transition-colors">Safety</a>
<a href="/gallery" class="text-sm font-medium text-charcoal hover:text-gold-dark transition-colors">Gallery</a>
```

- [ ] **Step 2: Add Safety link to mobile nav**

In the mobile menu section (around line 165-168), find:

```html
<a href="/about" class="block py-2 text-charcoal hover:text-gold-dark font-medium">About</a>
<a href="/gallery" class="block py-2 text-charcoal hover:text-gold-dark font-medium">Gallery</a>
```

Replace with:

```html
<a href="/about" class="block py-2 text-charcoal hover:text-gold-dark font-medium">About</a>
<a href="/safety" class="block py-2 text-charcoal hover:text-gold-dark font-medium">Safety</a>
<a href="/gallery" class="block py-2 text-charcoal hover:text-gold-dark font-medium">Gallery</a>
```

- [ ] **Step 3: Verify navigation builds and renders correctly**

Run: `cd /Users/rosswalker/accurite-excavation && npm run build 2>&1 | tail -20`
Expected: Build completes successfully.

- [ ] **Step 4: Commit**

```bash
git add src/components/Header.astro
git commit -m "nav: add safety page to header navigation"
```

---

### Task 6: Add Safety Link to About Page Credentials Section

The about page has a "Licensed, Insured, and Proven" credentials grid. Add the EMOD as a fifth credential card.

**Files:**
- Modify: `src/pages/about.astro`

- [ ] **Step 1: Add EMOD credential card**

In `src/pages/about.astro`, find the credentials grid (around line 101). Change the grid from `lg:grid-cols-4` to `lg:grid-cols-5` and add a new card after the reviews count card.

Find:

```html
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 max-w-4xl mx-auto">
```

Replace with:

```html
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-6 max-w-5xl mx-auto">
```

Then find the last credential card (around line 123-126):

```html
        <div class="text-center p-6 border border-gray-200 rounded-lg">
          <div class="text-3xl font-bold text-gold-dark">{business.reviews.count}</div>
          <div class="mt-2 text-sm text-gray-600">Five-Star Reviews</div>
        </div>
```

Replace with:

```html
        <div class="text-center p-6 border border-gray-200 rounded-lg">
          <div class="text-3xl font-bold text-gold-dark">{business.reviews.count}</div>
          <div class="mt-2 text-sm text-gray-600">Five-Star Reviews</div>
        </div>
        <div class="text-center p-6 border border-gray-200 rounded-lg">
          <div class="text-3xl font-bold text-gold-dark">0.91</div>
          <div class="mt-2 text-sm text-gray-600">EMOD Safety Rating</div>
          <div class="mt-2">
            <a href="/safety" class="text-sm text-gold-dark hover:underline">Below industry avg</a>
          </div>
        </div>
```

- [ ] **Step 2: Verify the about page builds**

Run: `cd /Users/rosswalker/accurite-excavation && npm run build 2>&1 | tail -20`
Expected: Build completes successfully.

- [ ] **Step 3: Commit**

```bash
git add src/pages/about.astro
git commit -m "trust: add EMOD safety rating to about page credentials grid"
```
