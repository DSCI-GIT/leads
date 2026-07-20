# DSCI Lead Intelligence — QA, Dedupe and Saturation Report

**Research date:** July 20, 2026<br>
**Final lead count:** 207

## Scope

The lead universe was rebuilt from the current ACEC-Ontario member directory, ORCGA listings, OCA member-directory examples, Ontario surveyor/geomatics company websites, road-building/roofing market sources and current first-party company websites. The target profile is Ontario engineering, surveying, geomatics, construction-support, heavy-civil, inspection and infrastructure firms whose services overlap with Drone Services Canada Inc.'s RPAS LiDAR, mapping, inspection and documentation work.

## Verification checklist

- Every record contains at least two evidence URLs: the company website and the ACEC-Ontario directory page used for the record.
- Names, public emails, phones, headquarters, service categories, market sectors and regions were not generated from email patterns or guessed from company names.
- Missing public information is marked `NOT CONFIRMED`.
- Named contacts are included only where the source explicitly states the name and title.
- Summaries and outreach angles are generated only from listed service categories, sectors and regions.
- Original engineering records use `last_verified_date` = `2026-07-19`; Wave 1 and Wave 2 expansion records use `last_verified_date` = `2026-07-20`.

## Dedupe log

- Gannett Fleming Canada / Gannett Fleming TranSystems / GFT: consolidated under the current **GFT** brand.
- McIntosh Perry / Egis Canada: consolidated under **Egis Canada Ltd. (formerly McIntosh Perry)**.
- SNC-Lavalin / AtkinsRéalis: consolidated under **AtkinsRéalis Canada Inc.**
- Morrison Hershfield was not added separately because it is now part of Stantec.
- Cole Engineering was not added separately because current Arcadis ownership creates corporate overlap.
- A.J. Clarke was not added separately because it operates as a division of TULLOCH.
- Duplicate office listings and repeated pagination results for AECOM, WSP, TULLOCH, Tatham and other multi-office firms were merged into one company record.
- Eramosa was retained as a distinct operating lead because the current directory publishes a separate brand, website and public contact, despite CIMA+ ownership.

## Saturation report

The current ACEC-Ontario directory displayed 131 results during final verification. The first build included 100 firms selected for direct relevance to Ontario civil infrastructure, water/wastewater, environmental and geotechnical work, geomatics/surveying, construction management, transportation, asset assessment or infrastructure inspection. Wave 1 added 52 surveyor/geomatics-skewed leads from ORCGA listings, public search results and first-party websites. Wave 2 added 55 construction, heavy-civil, roofing/envelope and inspection leads from ORCGA, OCA, ORBA/OIRCA market sources and first-party websites.

Repeated pagination produced the same firms, offices and parent brands. After corporate consolidation and relevance filtering, additional ACEC results were primarily outside the target service profile. The expanded 207-record set adds deliberate surveyor/geomatics, construction, heavy-civil, roofing/envelope and inspection skew without padding the dataset with unrelated firms.

## Reproducible fit score

The score uses only verified service, client and region fields and is capped at 100:

- +30: surveying, geomatics or explicitly listed LiDAR
- +25: civil, municipal, land-development or transportation infrastructure
- +20: water, wastewater, stormwater, sewer, watermain or water resources
- +20: environmental, geotechnical, geological, ecology, hydrogeology or mining infrastructure
- +15: construction inspection, condition assessment, contract/construction management, asset management, bridges or building science
- +10: explicit municipal, transportation, utility, infrastructure-owner, mining or industrial client market
- +5: verified Ontario or wider service region

## Reproducible confidence score

- 45: ACEC-Ontario member-directory evidence
- +15: first-party company website provided
- +10: public email provided
- +10: public phone provided
- +10: explicit service list available
- +5: explicit client/sector list available
- +5: explicit service region available

A lead receives a **Needs verification** flag when confidence is below 60 or a key public contact/service field is missing.

## App QA

- The HTML contains an embedded copy of all lead data and therefore works when double-clicked with no server.
- On Netlify/HTTP it attempts to load `leads.json`, falling back to the embedded dataset if unavailable.
- Pipeline stage, notes, sender settings and saved views persist in `localStorage`.
- Full and filtered CSV exports include local stage and note updates.
- Local updates can be exported and re-imported as a JSON patch.
- The site uses no external JavaScript or CSS dependencies.
