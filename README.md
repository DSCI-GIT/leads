# DSCI Lead Intelligence

Static lead-intelligence website for Drone Services Canada Inc. and SplatCap3D. The application contains separate lead datasets, filters, scoring, outreach tools, browser-local pipeline stages and notes, and CSV/JSON export functions.

## Repository contents

- `index.html` - DS lead workspace with embedded offline dataset
- `sc3d.html` - SplatCap3D lead workspace with embedded offline dataset
- `leads.json` - hosted DS dataset loaded by the website when available
- `leads.csv` - DS spreadsheet-ready export
- `sc3d_leads.json` - separate SplatCap3D lead dataset
- `sc3d_leads.csv` - SplatCap3D spreadsheet-ready export
- `404.html` - GitHub Pages fallback copy of the DS application
- `QA_DEDUPE_SATURATION.md` - DS dataset QA and sourcing notes
- `SC3D_SOURCING.md` - SplatCap3D qualification and sourcing notes
- `.github/workflows/deploy-pages.yml` - automatic GitHub Pages deployment
- `scripts/validate_dataset.py` - deployment-time schema and duplicate validation for both datasets
- `scripts/sync_embedded_data.py` - updates offline datasets inside the HTML files
- `scripts/add_wave1_surveyors.py` - reproducible Wave 1 surveyor/geomatics lead expansion
- `scripts/add_wave2_construction_inspection.py` - reproducible Wave 2 construction/inspection lead expansion
- `scripts/add_wave3_remaining_categories.py` - reproducible Wave 3 expansion for municipal, utility, aggregate and developer/property leads
- `scripts/add_sc3d_initial_leads.py` - builds the initial SplatCap3D lead database
- `scripts/build_sc3d_page.py` - builds the SC3D lead page from the shared app shell

## Publish with GitHub Pages

1. Commit the files to the `main` branch.
2. In Settings -> Pages, set Source to GitHub Actions if GitHub does not select it automatically.
3. Open the Actions tab and allow the deploy workflow to finish.
4. The workflow summary will show the live `github.io` address.

The site uses relative paths, so it works both as a user/organization site and as a project site such as:

`https://USERNAME.github.io/REPOSITORY/`

## Open locally

Double-click `index.html` for DS or `sc3d.html` for SplatCap3D. The complete datasets are embedded, so no local server and no JSON paste are required.

## Update the datasets

1. Edit `leads.json` or `sc3d_leads.json`.
2. Update the matching CSV if required.
3. Run:

```bash
python scripts/validate_dataset.py
python scripts/sync_embedded_data.py
```

4. Commit and push. GitHub Actions will validate and deploy the update.

## Browser-local sales data

Pipeline stages, notes, saved views and sender settings are stored in the browser's `localStorage`. DS and SC3D use separate local-storage keys. Use the application's JSON patch export/import functions to move those updates between browsers.

## Privacy and indexing

The pages contain a `noindex` meta tag and `robots.txt` disallows crawling. GitHub Pages cannot enforce Netlify-style security response headers. Do not place confidential data in this public repository.
