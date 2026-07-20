#!/usr/bin/env python3
"""Validate the DSCI lead dataset before GitHub Pages deployment."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "leads.json"

REQUIRED_FIELDS = {
    "id",
    "company_name",
    "company_type",
    "hq_city",
    "hq_province",
    "regions_served",
    "primary_services",
    "client_types",
    "evidence_links",
    "summary",
    "fit_rationale",
    "drone_lidar_fit_signals",
    "contacts",
    "public_email",
    "public_phone",
    "contact_form_url",
    "outreach_angle",
    "fit_score",
    "confidence_score",
    "pipeline_stage",
    "notes",
    "last_verified_date",
}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def valid_http_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def main() -> None:
    try:
        leads = json.loads(DATA.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"Cannot read valid JSON from {DATA}: {exc}")

    if not isinstance(leads, list) or not leads:
        fail("leads.json must contain a non-empty JSON array")

    ids: set[str] = set()
    names: set[str] = set()

    for index, lead in enumerate(leads, start=1):
        if not isinstance(lead, dict):
            fail(f"Lead {index} is not an object")

        missing = REQUIRED_FIELDS - set(lead)
        extra = set(lead) - REQUIRED_FIELDS
        if missing:
            fail(f"Lead {index} is missing fields: {sorted(missing)}")
        if extra:
            fail(f"Lead {index} contains unexpected fields: {sorted(extra)}")

        lead_id = str(lead["id"]).strip()
        company_name = str(lead["company_name"]).strip()
        if not lead_id or lead_id in ids:
            fail(f"Duplicate or blank id at lead {index}: {lead_id!r}")
        if not company_name or company_name.casefold() in names:
            fail(f"Duplicate or blank company name at lead {index}: {company_name!r}")
        ids.add(lead_id)
        names.add(company_name.casefold())

        for score_field in ("fit_score", "confidence_score"):
            score = lead[score_field]
            if not isinstance(score, int) or not 0 <= score <= 100:
                fail(f"{company_name}: {score_field} must be an integer from 0 to 100")

        for array_field in (
            "regions_served",
            "primary_services",
            "client_types",
            "evidence_links",
            "contacts",
        ):
            if not isinstance(lead[array_field], list):
                fail(f"{company_name}: {array_field} must be an array")

        for url in lead["evidence_links"]:
            if not isinstance(url, str) or not valid_http_url(url):
                fail(f"{company_name}: invalid evidence URL {url!r}")

        form_url = lead["contact_form_url"]
        if form_url != "NOT CONFIRMED" and not valid_http_url(str(form_url)):
            fail(f"{company_name}: invalid contact_form_url {form_url!r}")

        for contact in lead["contacts"]:
            if not isinstance(contact, dict):
                fail(f"{company_name}: each contact must be an object")
            expected_contact_fields = {"name", "title", "source_url", "contact_method"}
            if set(contact) != expected_contact_fields:
                fail(f"{company_name}: contact fields must be {sorted(expected_contact_fields)}")
            if not valid_http_url(str(contact["source_url"])):
                fail(f"{company_name}: invalid contact source URL {contact['source_url']!r}")

    print(f"Validated {len(leads)} leads with unique IDs, unique names, valid scores and URL evidence.")


if __name__ == "__main__":
    main()
