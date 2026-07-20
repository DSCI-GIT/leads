#!/usr/bin/env python3
"""Append Wave 2 construction, heavy-civil and inspection leads."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "leads.json"
CSV_PATH = ROOT / "leads.csv"
VERIFIED = "2026-07-20"

FIELDS = [
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
]


def slug(name: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return f"on-wave2-{value}"[:80]


def lead(
    name: str,
    company_type: str,
    city: str,
    website: str,
    services: list[str],
    clients: list[str],
    regions: list[str] | None = None,
    email: str = "NOT CONFIRMED",
    phone: str = "NOT CONFIRMED",
    form: str = "NOT CONFIRMED",
    source: str | None = None,
    confidence: int | None = None,
) -> dict[str, object]:
    regions = regions or ["Ontario"]
    evidence = [website]
    if source and source != website:
        evidence.append(source)
    signals = [
        service
        for service in services
        if any(
            key in service.lower()
            for key in (
                "inspection",
                "as-built",
                "site",
                "earthworks",
                "grading",
                "road",
                "bridge",
                "roof",
                "envelope",
                "utility",
                "sewer",
                "watermain",
                "condition",
                "thermal",
            )
        )
    ] or services[:3]
    if confidence is None:
        confidence = 65
        if len(evidence) > 1:
            confidence += 10
        if email != "NOT CONFIRMED":
            confidence += 10
        if phone != "NOT CONFIRMED":
            confidence += 10
        confidence = min(confidence, 95)
    service_text = ", ".join(services[:4]).lower()
    client_text = ", ".join(clients[:3]).lower()
    return {
        "id": slug(name),
        "company_name": name,
        "company_type": company_type,
        "hq_city": city,
        "hq_province": "Ontario",
        "regions_served": regions,
        "primary_services": services,
        "client_types": clients,
        "evidence_links": evidence,
        "summary": f"{company_type} firm with public signals for {', '.join(services[:3]).lower()} work.",
        "fit_rationale": f"Provides {service_text} services for {client_text}, creating a fit for RPAS site documentation, aerial progress capture, LiDAR/topographic support and inspection imagery.",
        "drone_lidar_fit_signals": signals,
        "contacts": [
            {
                "name": "NOT CONFIRMED",
                "title": "NOT CONFIRMED",
                "source_url": website,
                "contact_method": "; ".join(
                    part
                    for part in (
                        f"Email: {email}" if email != "NOT CONFIRMED" else "",
                        f"Phone: {phone}" if phone != "NOT CONFIRMED" else "",
                        "Website/contact form",
                    )
                    if part
                ),
            }
        ],
        "public_email": email,
        "public_phone": phone,
        "contact_form_url": form,
        "outreach_angle": f"Offer construction-progress mapping, as-built documentation, aerial LiDAR/topographic capture and inspection imagery around {', '.join(services[:3]).lower()} workloads.",
        "fit_score": 90
        if any(k in " ".join(services).lower() for k in ("inspection", "roof", "envelope", "lidar", "as-built"))
        else 82,
        "confidence_score": confidence,
        "pipeline_stage": "New",
        "notes": "Wave 2 construction/heavy-civil/inspection expansion.",
        "last_verified_date": VERIFIED,
    }


ORCGA = "https://orcga.com/members/"
OCA = "https://oca.ca/member-directory/"
ORBA = "https://orba.org/"
OIRCA = "https://secure.ontarioroofing.com/"

WAVE2 = [
    lead("24/7 Vacuum Excavation", "Construction", "Pickering", "https://www.247vac.com/", ["Vacuum excavation", "Utility daylighting", "Hydrovac services", "Site support"], ["Excavators", "Utilities", "Contractors"], ["Greater Toronto Area"], source=ORCGA),
    lead("A & J Vacworx Inc.", "Construction", "Mount Albert", "https://www.ajvac.ca/", ["Vacuum excavation", "Hydrovac services", "Utility exposure", "Site support"], ["Utilities", "Excavators", "Contractors"], ["York Region", "Ontario"], source=ORCGA),
    lead("Accuworx Inc.", "Heavy Civil", "Mississauga", "https://www.accuworx.ca/", ["Environmental contracting", "Infrastructure services", "Road-builder support", "Site remediation"], ["Municipalities", "Utilities", "Contractors"], ["Ontario"], source=ORCGA),
    lead("Aecon Civil and Utilities", "Heavy Civil", "Toronto", "https://www.aecon.com/", ["Civil construction", "Utilities", "Road building", "Infrastructure construction"], ["Transportation agencies", "Utilities", "Municipalities"], ["Ontario", "Canada"], source=ORCGA),
    lead("Aecon Construction Ontario East", "Heavy Civil", "Carp", "https://www.karson.ca/", ["Road building", "Civil construction", "Aggregates", "Infrastructure construction"], ["Municipalities", "Transportation agencies", "Developers"], ["Eastern Ontario"], source=ORCGA),
    lead("All Clear Locates Inc.", "Inspection", "Stouffville", "https://www.allclearlocates.com/", ["Utility locating", "Site investigation", "Damage prevention", "Subsurface utility support"], ["Excavators", "Contractors", "Utilities"], ["Ontario"], source=ORCGA),
    lead("Altech Utility Services", "Inspection", "Cambridge", "http://www.altechworld.com/", ["Utility locating", "Subsurface utility support", "Field investigation", "Damage prevention"], ["Utilities", "Excavators", "Municipal clients"], ["Ontario"], source=ORCGA),
    lead("Antrim Contracting", "Construction", "Arnprior", "http://www.antrimcontracting.com/", ["Excavation", "Site servicing", "Grading", "Heavy equipment"], ["Municipalities", "Builders", "Developers"], ["Eastern Ontario"], source=ORCGA),
    lead("Ardel Construction & Aggregates Ltd.", "Construction", "North Bay", "https://ardelconstruction.ca/", ["Excavation", "Aggregates", "Site works", "Road-builder support"], ["Municipalities", "Contractors", "Developers"], ["Northern Ontario"], source=ORCGA, confidence=70),
    lead("Arnott Construction", "Construction", "Midhurst", "https://arnottconstruction.com/", ["Excavation", "Site servicing", "Sewer and watermain", "Heavy civil construction"], ["Municipalities", "Developers", "Contractors"], ["Simcoe County", "Ontario"], source=ORCGA),
    lead("Avertex Utility Solutions Inc.", "Construction", "Amaranth", "https://www.avertex.ca/", ["Utility construction", "Excavation", "Directional drilling", "Site support"], ["Utilities", "Municipalities", "Contractors"], ["Ontario"], source=ORCGA),
    lead("WRC Contracting", "Construction", "Pakenham", "https://wrccontracting.com/", ["Excavating contractors", "Site services", "Grading", "Sewers and watermains"], ["Builders", "Municipalities", "Contractors"], ["Ottawa", "Eastern Ontario"], source=OCA),
    lead("Malwood", "Construction", "Dunrobin", "https://malwood.ca/", ["Concrete contractors", "Excavating contractors", "Crane service", "Site support"], ["Contractors", "Builders", "Commercial clients"], ["Ottawa", "Eastern Ontario"], source=OCA, confidence=70),
    lead("Coco Paving Inc.", "Heavy Civil", "Toronto", "https://www.cocopaving.com/", ["Road building", "Asphalt paving", "Heavy civil construction", "Infrastructure construction"], ["Municipalities", "Transportation agencies", "Developers"], ["Ontario"], source=ORBA),
    lead("Dufferin Construction", "Heavy Civil", "Oakville", "https://www.dufferinconstruction.com/", ["Road construction", "Bridge construction", "Heavy civil", "Infrastructure construction"], ["Municipalities", "MTO", "Infrastructure owners"], ["Ontario"], source=ORBA),
    lead("Green Infrastructure Partners", "Heavy Civil", "Toronto", "https://www.gipi.com/", ["Infrastructure construction", "Road building", "Paving", "Civil works"], ["Municipalities", "Transportation agencies", "Developers"], ["Ontario"], source=ORBA),
    lead("Fowler Construction", "Heavy Civil", "Bracebridge", "https://www.fowler.ca/", ["Road construction", "Aggregates", "Site development", "Civil construction"], ["Municipalities", "Transportation agencies", "Developers"], ["Muskoka", "Northern Ontario"], source=ORBA),
    lead("Bot Construction Group", "Heavy Civil", "Oakville", "https://botconstruction.ca/", ["Heavy civil construction", "Roads", "Bridges", "Transportation infrastructure"], ["Transportation agencies", "Municipalities", "Infrastructure owners"], ["Ontario"], source=ORBA),
    lead("EBC Inc.", "Heavy Civil", "Mississauga", "https://www.ebcinc.com/", ["Civil engineering construction", "Transportation infrastructure", "Major projects", "Bridges"], ["Public sector", "Transportation agencies", "Infrastructure owners"], ["Ontario", "Canada"], source=ORBA),
    lead("Fermar Paving Limited", "Heavy Civil", "Toronto", "https://www.fermarpaving.com/", ["Paving", "Road construction", "Municipal infrastructure", "Civil construction"], ["Municipalities", "Transportation agencies", "Developers"], ["Greater Toronto Area", "Ontario"], source=ORBA),
    lead("Grascan Construction Ltd.", "Heavy Civil", "Toronto", "https://www.grascan.com/", ["Road building", "Bridge construction", "Civil construction", "Infrastructure rehabilitation"], ["Municipalities", "Transportation agencies", "Infrastructure owners"], ["Ontario"], source=ORCGA),
    lead("Four Seasons Site Development Ltd.", "Construction", "Brampton", "https://www.sitedevelopment.ca/", ["Site development", "Road-builder support", "Earthworks", "Civil construction"], ["Developers", "Builders", "Municipalities"], ["Greater Toronto Area"], source=ORCGA),
    lead("K.G. Reid Trenching & Construction Ltd.", "Construction", "Belleville", "https://www.kgreid.ca/", ["Trenching", "Excavation", "Utility construction", "Site servicing"], ["Utilities", "Municipalities", "Contractors"], ["Eastern Ontario"], source=ORCGA),
    lead("Steed and Evans Limited", "Heavy Civil", "St. Jacobs", "https://www.steedandevans.ca/", ["Road construction", "Site servicing", "Aggregates", "Asphalt paving"], ["Municipalities", "Developers", "Transportation clients"], ["Waterloo Region", "Ontario"], source=ORBA),
    lead("KAPP Infrastructure Inc.", "Heavy Civil", "Vaughan", "https://www.kappinfrastructure.com/", ["Heavy civil construction", "Roads", "Sewer and watermain", "Site development"], ["Municipalities", "Developers", "Infrastructure owners"], ["Greater Toronto Area", "Ontario"], source=ORBA),
    lead("Bronte Construction", "Heavy Civil", "Oakville", "https://bronteconstruction.ca/", ["Heavy civil construction", "Bridge construction", "Roadwork", "Marine construction"], ["Municipalities", "Transportation agencies", "Infrastructure owners"], ["Ontario"], source=ORBA),
    lead("Alliance Verdi Civil", "Heavy Civil", "Bolton", "https://allianceverdi.com/", ["Civil construction", "Earthworks", "Site servicing", "Infrastructure construction"], ["Developers", "Municipalities", "Builders"], ["Greater Toronto Area"], source=ORBA),
    lead("Gateman-Milloy Inc.", "Construction", "Kitchener", "https://www.gatemanmilloy.com/", ["Site development", "Civil construction", "Landscape construction", "Earthworks"], ["Developers", "Institutions", "Municipalities"], ["Waterloo Region", "Ontario"], source=ORBA),
    lead("Earth Boring Co. Limited", "Construction", "Mississauga", "https://www.earthboring.ca/", ["Trenchless construction", "Tunnelling", "Utility crossings", "Subsurface infrastructure"], ["Utilities", "Municipalities", "Infrastructure owners"], ["Ontario"], source=ORBA),
    lead("Technicore Underground Inc.", "Construction", "Newmarket", "https://technicore.ca/", ["Microtunnelling", "Trenchless construction", "Shaft construction", "Underground infrastructure"], ["Municipalities", "Utilities", "Infrastructure owners"], ["Ontario"], source=ORBA),
    lead("Memme Infrastructure Contractors", "Heavy Civil", "Hamilton", "https://www.memme.ca/", ["Heavy civil construction", "Sewer and watermain", "Road reconstruction", "Site servicing"], ["Municipalities", "Developers", "Contractors"], ["Hamilton", "Niagara", "Ontario"], source=ORBA),
    lead("Clearway Construction Inc.", "Heavy Civil", "Vaughan", "https://www.clearwaygroup.com/", ["Heavy civil construction", "Earthworks", "Roads", "Infrastructure projects"], ["Municipalities", "Transportation agencies", "Developers"], ["Ontario"], source=ORBA),
    lead("Powell Contracting", "Heavy Civil", "Stouffville", "https://powellcontracting.com/", ["Road construction", "Bridge rehabilitation", "Civil infrastructure", "Traffic control"], ["MTO", "Municipalities", "Transportation agencies"], ["Ontario"], source=ORBA),
    lead("Sierra Infrastructure Inc.", "Heavy Civil", "Woodbridge", "https://www.sierrainfrastructure.ca/", ["Heavy civil construction", "Sewer and watermain", "Road reconstruction", "Site servicing"], ["Municipalities", "Developers", "Infrastructure owners"], ["Greater Toronto Area", "Ontario"], source=ORBA),
    lead("Metric Contracting Services Corporation", "Heavy Civil", "Toronto", "https://www.metriccontracting.com/", ["Heavy civil construction", "Earthworks", "Roads", "Municipal infrastructure"], ["Municipalities", "Developers", "Transportation agencies"], ["Ontario"], source=ORBA),
    lead("O'Hara Trucking & Excavating Inc.", "Construction", "Ayr", "https://oharatrucking.com/", ["Excavation", "Trucking", "Site servicing", "Earthworks"], ["Developers", "Contractors", "Municipal clients"], ["Waterloo Region", "Ontario"], source=ORBA, confidence=70),
    lead("North Rock Group Ltd.", "Construction", "Barrie", "https://northrockgroup.ca/", ["Infrastructure construction", "Site development", "Roadwork", "Civil construction"], ["Municipalities", "Developers", "Commercial clients"], ["Central Ontario"], source=ORBA),
    lead("CSL Group Ltd.", "Construction", "Ancaster", "https://www.cslgroup.ca/", ["Commercial site services", "Landscape construction", "Snow and ice management", "Property services"], ["Commercial clients", "Institutions", "Property managers"], ["Ontario"], source=ORBA),
    lead("IRC Building Sciences Group", "Inspection", "Mississauga", "https://www.ircgroup.com/", ["Building envelope consulting", "Roofing assessment", "Condition assessment", "Inspection"], ["Property managers", "Institutions", "Commercial owners"], ["Ontario", "Canada"], source=OIRCA),
    lead("Pretium Engineering Inc.", "Inspection", "Burlington", "https://pretiumengineering.com/", ["Building science", "Roofing consulting", "Envelope assessment", "Structural restoration"], ["Building owners", "Property managers", "Institutions"], ["Ontario"], source=OIRCA),
    lead("Brown & Beattie Ltd.", "Inspection", "Guelph", "https://brownbeattie.com/", ["Building science", "Roofing consulting", "Reserve fund studies", "Condition assessments"], ["Condominiums", "Property managers", "Building owners"], ["Ontario"], source=OIRCA),
    lead("Sense Engineering", "Inspection", "Toronto", "https://senseengineering.com/", ["Building restoration", "Building envelope", "Roofing consulting", "Condition assessments"], ["Condominiums", "Institutions", "Commercial owners"], ["Ontario"], source=OIRCA),
    lead("Edison Engineers Inc.", "Inspection", "Markham", "https://edisonengineers.ca/", ["Building restoration", "Envelope assessment", "Roof consulting", "Parking garage restoration"], ["Condominiums", "Property managers", "Building owners"], ["Ontario"], source=OIRCA),
    lead("Keller Engineering", "Inspection", "Ottawa", "https://kellerengineering.com/", ["Building envelope", "Roof consulting", "Structural restoration", "Condition assessments"], ["Condominiums", "Commercial owners", "Institutions"], ["Ontario"], source=OIRCA),
    lead("Pinchin Ltd.", "Inspection", "Mississauga", "https://www.pinchin.com/", ["Environmental consulting", "Building science", "Property condition assessments", "Hazardous materials"], ["Property owners", "Institutions", "Commercial clients"], ["Ontario", "Canada"], source=OIRCA),
    lead("Acuren", "Inspection", "Oakville", "https://www.acuren.com/", ["NDT inspection", "Materials engineering", "Asset integrity", "Industrial inspection"], ["Industrial clients", "Infrastructure owners", "Utilities"], ["Ontario", "Canada"], source=ORCGA),
    lead("MISTRAS Group Canada", "Inspection", "Burlington", "https://www.mistrasgroup.com/", ["NDT inspection", "Asset protection", "Condition monitoring", "Industrial inspection"], ["Industrial clients", "Utilities", "Infrastructure owners"], ["Ontario", "Canada"], source=ORCGA),
    lead("IRISNDT", "Inspection", "Burlington", "https://www.irisndt.com/", ["NDT inspection", "Engineering inspection", "Asset integrity", "Industrial services"], ["Industrial clients", "Energy clients", "Infrastructure owners"], ["Ontario", "Canada"], source=ORCGA),
    lead("Flynn Group of Companies", "Roofing/Envelope", "Mississauga", "https://flynncompanies.com/", ["Commercial roofing", "Building envelope", "Glazing", "Architectural metals"], ["Commercial owners", "Institutions", "General contractors"], ["Ontario", "Canada"], source=OIRCA),
    lead("Semple Gooder Roofing Corporation", "Roofing/Envelope", "Toronto", "https://semplegooder.com/", ["Commercial roofing", "Roof replacement", "Roof maintenance", "Roofing service"], ["Commercial owners", "Institutions", "Property managers"], ["Greater Toronto Area", "Ontario"], source=OIRCA),
    lead("Bothwell-Accurate", "Roofing/Envelope", "Mississauga", "https://bothwell-accurate.com/", ["Commercial roofing", "Waterproofing", "Building envelope", "Metal cladding"], ["General contractors", "Commercial owners", "Institutions"], ["Ontario"], source=OIRCA),
    lead("Atlas-Apex Roofing Inc.", "Roofing/Envelope", "Etobicoke", "https://atlas-apex.com/", ["Commercial roofing", "Roof maintenance", "Waterproofing", "Building envelope"], ["Commercial owners", "Institutions", "Property managers"], ["Ontario", "Canada"], source=OIRCA),
    lead("Canadian Roof Management Services Ltd.", "Inspection", "Mississauga", "https://canadianroofmanagement.ca/", ["Roof consulting", "Roof inspections", "Asset management", "Condition assessments"], ["Commercial owners", "Property managers", "Institutions"], ["Ontario"], source=OIRCA),
    lead("Tremco Roofing Canada", "Roofing/Envelope", "Toronto", "https://www.tremcoroofing.com/", ["Roof restoration", "Roof assessment", "Building envelope", "Weatherproofing"], ["Commercial owners", "Institutions", "Property managers"], ["Ontario", "Canada"], source=OIRCA),
    lead("Garland Canada Inc.", "Roofing/Envelope", "Toronto", "https://www.garlandcanada.com/", ["Roofing systems", "Building envelope", "Roof assessment", "Asset management"], ["Commercial owners", "Institutions", "Property managers"], ["Ontario", "Canada"], source=OIRCA),
]


def csv_cell(value: object) -> str:
    if isinstance(value, list):
        items = []
        for item in value:
            if isinstance(item, dict):
                items.append(" | ".join(str(item.get(key, "")) for key in ("name", "title", "contact_method", "source_url")))
            else:
                items.append(str(item))
        return "; ".join(items)
    return "" if value is None else str(value)


def main() -> None:
    leads = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    existing_names = {str(item["company_name"]).casefold() for item in leads}
    existing_ids = {str(item["id"]) for item in leads}
    added = []
    for item in WAVE2:
        if item["company_name"].casefold() in existing_names:
            continue
        base_id = str(item["id"])
        while item["id"] in existing_ids:
            item["id"] = f"{base_id}-{len(added) + 1}"
        leads.append(item)
        existing_names.add(item["company_name"].casefold())
        existing_ids.add(str(item["id"]))
        added.append(item)

    JSON_PATH.write_text(json.dumps(leads, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    with CSV_PATH.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        for item in leads:
            writer.writerow({field: csv_cell(item[field]) for field in FIELDS})
    print(f"Added {len(added)} Wave 2 construction/inspection leads. Total leads: {len(leads)}")


if __name__ == "__main__":
    main()
