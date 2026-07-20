# DSCI Lead Intelligence

Static lead-intelligence website for Drone Services Canada Inc. The application contains the lead dataset, filters, scoring, outreach tools, browser-local pipeline stages and notes, and CSV/JSON export functions.

## Repository contents

- `index.html` — complete browser application with an embedded offline dataset
- `leads.json` — hosted dataset loaded by the website when available
- `leads.csv` — spreadsheet-ready export
- `404.html` — GitHub Pages fallback copy of the application
- `QA_DEDUPE_SATURATION.md` — dataset QA and sourcing notes
- `.github/workflows/deploy-pages.yml` — automatic GitHub Pages deployment
- `scripts/validate_dataset.py` — deployment-time schema and duplicate validation
- `scripts/sync_embedded_data.py` — updates the offline dataset inside the HTML files
- `scripts/add_wave1_surveyors.py` — reproducible Wave 1 surveyor/geomatics lead expansion
- `scripts/add_wave2_construction_inspection.py` — reproducible Wave 2 construction/inspection lead expansion

## Publish with GitHub Pages

1. Create a new GitHub repository.
2. Extract this ZIP and upload all contents, including the hidden `.github` folder and `.nojekyll` file.
3. Commit the files to the `main` branch.
4. In **Settings → Pages**, set **Source** to **GitHub Actions** if GitHub does not select it automatically.
5. Open the **Actions** tab and allow the `Deploy DSCI Lead Intelligence to GitHub Pages` workflow to finish.
6. The workflow summary will show the live `github.io` address.

The site uses relative paths, so it works both as a user/organization site and as a project site such as:

`https://USERNAME.github.io/REPOSITORY/`

## Open locally

Double-click `index.html`. The complete dataset is embedded, so no local server and no JSON paste are required.

## Update the dataset

1. Replace or edit `leads.json`.
2. Update `leads.csv` if a matching CSV is required.
3. Run:

```bash
python scripts/validate_dataset.py
python scripts/sync_embedded_data.py
```

4. Commit and push. GitHub Actions will validate and deploy the update.

## Browser-local sales data

Pipeline stages, notes, saved views and sender settings are stored in the browser's `localStorage`. They are not committed to GitHub. Use the application's JSON patch export/import functions to move those updates between browsers.

## Privacy and indexing

The pages contain a `noindex` meta tag and `robots.txt` disallows crawling. GitHub Pages cannot enforce Netlify-style security response headers. Do not place confidential data in this public repository. Use a private repository only for source control; verify separately whether your GitHub plan supports the desired Pages visibility.

## Custom domain

Configure a custom domain in **Settings → Pages**. GitHub creates or updates a `CNAME` file when the domain is saved through the interface.
