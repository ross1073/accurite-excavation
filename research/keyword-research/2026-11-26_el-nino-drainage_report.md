# El Niño / drainage keyword pull — 2026-11-26

Script: `pull_el_nino_drainage.py` · raw: `2026-11-26_el-nino-drainage_raw.json`
Source: DataForSEO Google Ads `search_volume/live` (State of Utah 21175, and the Google Ads
DMA 200770 that contains Ogden) + `keywords_for_keywords/live` (Utah). Monthly data
covers Nov 2025 – Oct 2026. **Cost: $0.27** (3 tasks × $0.09, as reported by DataForSEO).
Account balance before the pull: $13.04 (DataForSEO `user_data`, 2026-11-26). The project
keeps no monthly spend log, so month-to-date spend against the $25 cap could not be read.

## Pick: target phrase **"El Niño winter"**

| | Utah avg/mo | DMA avg/mo | Sep 2026 | Oct 2026 |
|---|---|---|---|---|
| el nino winter | 320 | 210 | 1,900 (Utah) | 880 (Utah) |

Why: it is the only El Niño phrase that both data sets agree on, it is rising into this
winter, and it is the phrase the post's title already uses. Secondary: `el nino 2026`
(Utah 2,900 avg, national-news competition), `el nino utah` (see conflict below),
`erosion control` (320), `driveway culvert` (110), `yard drainage` (90),
`retaining wall drainage` (70).

## What the numbers rule out

- **"spring runoff" / "utah spring runoff" / "spring runoff utah": 0** in Utah. Not a target.
- **"culvert repair": 10**, "culvert installation" 20, "washout repair" no data. Culverts
  stay in the post as checklist content, not as a target phrase.
- **"drainage contractor": 20.** "drainage contractor near me" shows 110 in Utah but only
  10 in the DMA, and its Utah figure is one 720 spike in Oct 2026 on a 20–90 baseline —
  treat as noise.

## Conflict to flag

`el nino utah` reads **10/mo for the State of Utah but 480/mo for the DMA** (peaking 1,300
in Sep 2026). The DMA is mostly Utah plus slivers of neighboring states, so it cannot
plausibly have 48× the state's searches; one of the two readings is wrong. Unresolved;
the post does not depend on it.

## Full table (Utah avg, DMA avg, CPC)

el nino 4400/2900/$1.26 · el nino 2026 2900/1900/$1.40 · french drain installation
1000/390/$29.45 · el nino winter 320/210/$3.52 · erosion control 320/70/$3.32 · drainage
contractor near me 110/10/$22.88 · drainage solutions 110/10 · grading contractor
110/10/$13.88 · driveway culvert 110/10/$3.50 · yard drainage 90/20 · drainage repair 70/90
· driveway grading 70/10 · gravel driveway repair 70/10/$17.02 · retaining wall drainage
70/30 · yard grading 50/20 · land grading 50/20 · drainage ditch 50/20 · retaining wall
repair 40/40/$28.86 · el nino utah 10/480 · el nino 2026 utah 10/320 · utah winter forecast
10/260 · culvert repair 10/10 · spring runoff 0/10. Full monthly series in the script output
and raw JSON.
