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
