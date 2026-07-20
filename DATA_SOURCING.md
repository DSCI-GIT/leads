# Data Sourcing Notes

## Wave 1 Surveyor/Geomatics Expansion

**Date:** July 20, 2026  
**Added leads:** 52  
**New total:** 152

Wave 1 expands the dataset beyond engineering consultants into surveyors, geomatics firms, UAV survey providers, construction layout firms and inspection-adjacent mapping providers.

Primary source types:

- ORCGA land-surveying member listings.
- First-party company websites for Ontario land surveyors and geomatics firms.
- Public search results for Ontario surveyor pages that listed services such as topographic surveys, construction layout, LiDAR, UAV/drone surveying, 3D scanning, volume calculations, control surveys, as-built surveys, bridge/culvert surveys, hydrographic surveys, machine-control models, GIS and mapping.

Inclusion rules:

- Ontario presence or Ontario service area.
- Clear survey, geomatics, UAV survey, topographic, construction layout, LiDAR, 3D scanning, inspection, mapping or site-data service signal.
- Useful fit for DSCI as an overflow field-capture, aerial LiDAR, photogrammetry, thermal/inspection, construction documentation or data-processing subcontract partner.

Lower-confidence records:

- Some Wave 1 records use `NOT CONFIRMED` for public email or phone where the website/source found during the pass did not expose a reliable public contact in the snippet. These remain useful as research targets but should be verified before outreach.

Refresh process:

1. Add or update records in `leads.json`.
2. Rebuild `leads.csv`.
3. Run `python scripts/validate_dataset.py`.
4. Run `python scripts/sync_embedded_data.py`.
5. Spot-check the app filters for company type, region, score and outreach behavior.

## Wave 2 Construction/Inspection Expansion

**Date:** July 20, 2026<br>
**Added leads:** 55<br>
**New total:** 207

Wave 2 expands the dataset toward contractors, heavy-civil firms, excavation/site-servicing firms, utility/site investigation, roofing/envelope firms and inspection/NDT providers.

Primary source types:

- ORCGA member listings for road builders, excavators, locators and related utility stakeholders.
- Ottawa Construction Association member directory examples with civil/site-service classifications.
- Ontario Road Builders' Association market/source context for transportation infrastructure contractors.
- Ontario Industrial Roofing Contractors Association search/member-directory context for roofing and building-envelope firms.
- First-party company websites for public service descriptions and contact pages.

Inclusion rules:

- Ontario headquarters, office, member listing or active Ontario service area.
- Clear construction, heavy civil, excavation, road/bridge, sewer/watermain, utility, roofing/envelope, condition assessment, inspection or NDT service signal.
- Useful fit for DSCI as a construction documentation, progress mapping, aerial LiDAR/topographic, inspection imagery, roof/envelope inspection or site-data subcontract partner.

Lower-confidence records:

- Many Wave 2 records keep `NOT CONFIRMED` for public email/phone because this pass prioritized market breadth and sourceable company/service fit. Verify public contacts before outreach.

## Wave 3 Remaining Lead Categories

**Date:** July 20, 2026<br>
**Added leads:** 208<br>
**New total:** 415

Wave 3 fills the remaining high-fit lead buckets at a minimum of 50 researched records each:

- Municipal/Public Works: 52
- Utilities/Energy: 52
- Aggregates/Materials: 52
- Developer/Property: 52

Primary source types:

- Ontario's official municipality list, used to target public works, engineering, roads, bridges, water/wastewater, stormwater and capital-project departments.
- Ontario Energy Board licensed-company list, used to target electricity distributors and utility infrastructure owners.
- Ontario Stone, Sand & Gravel Association active-member directory, used to target pits, quarries, aggregate producers and construction-materials firms.
- BILD, HCRA and CHBA builder/developer directories, used to target builders, developers, real-estate owners and property asset managers.
- First-party websites where a reliable company or municipality URL was available during the pass.

Inclusion rules:

- Ontario presence, Ontario operating area or Ontario-regulated/licensed market participation.
- Clear asset owner, site owner, infrastructure owner, utility, public works, aggregates, builder/developer or property-management fit.
- Useful fit for DSCI as an aerial mapping, construction documentation, asset inspection, stockpile survey, roof/envelope inspection or corridor/site-capture provider.

Lower-confidence records:

- Wave 3 is deliberately broad. Most records should be treated as account targets first; public contact names, direct emails and phone numbers should be verified before outreach.
