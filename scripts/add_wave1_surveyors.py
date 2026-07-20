#!/usr/bin/env python3
"""Append Wave 1 surveyor/geomatics leads and rebuild the CSV export."""

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
    return f"on-wave1-{value}"[:80]


def lead(
    name: str,
    city: str,
    website: str,
    services: list[str],
    clients: list[str],
    email: str = "NOT CONFIRMED",
    phone: str = "NOT CONFIRMED",
    regions: list[str] | None = None,
    form: str = "NOT CONFIRMED",
    summary: str | None = None,
    confidence: int | None = None,
) -> dict[str, object]:
    regions = regions or ["Ontario"]
    signals = [
        service
        for service in services
        if any(k in service.lower() for k in ("lidar", "drone", "uav", "topographic", "construction", "3d", "volume", "control", "as-built", "mapping"))
    ]
    if not signals:
        signals = services[:3]
    if confidence is None:
        confidence = 80
        if email != "NOT CONFIRMED":
            confidence += 10
        if phone != "NOT CONFIRMED":
            confidence += 10
        confidence = min(confidence, 100)
    return {
        "id": slug(name),
        "company_name": name,
        "company_type": "Geomatics",
        "hq_city": city,
        "hq_province": "Ontario",
        "regions_served": regions,
        "primary_services": services,
        "client_types": clients,
        "evidence_links": [website],
        "summary": summary or f"Surveying and geomatics firm offering {', '.join(services[:3]).lower()} services.",
        "fit_rationale": f"Provides {', '.join(services[:4]).lower()} services for {', '.join(clients[:3]).lower()}, creating a direct fit for overflow RPAS LiDAR, photogrammetry, topo capture, construction documentation and inspection support.",
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
        "outreach_angle": f"Offer subcontract aerial LiDAR, photogrammetry, site modelling and field capture support for {', '.join(services[:3]).lower()} workloads.",
        "fit_score": 90 if any(k in " ".join(services).lower() for k in ("lidar", "drone", "uav", "3d", "volume")) else 80,
        "confidence_score": confidence,
        "pipeline_stage": "New",
        "notes": "Wave 1 surveyor/geomatics expansion.",
        "last_verified_date": VERIFIED,
    }


WAVE1 = [
    lead("KPK Surveying Inc.", "Huntsville", "https://kpksurvey.ca/", ["Topographic surveys", "Construction layout", "Boundary surveys", "Plans of subdivision"], ["Developers", "Builders", "Property owners"], "info@KPKsurvey.ca", "705-788-2701", ["Muskoka", "Parry Sound", "Haliburton"]),
    lead("Altimap Land Surveyors", "Toronto", "https://altimap.ca/", ["Topographic surveys", "Construction survey", "Site and grading plans", "Reference plans"], ["Developers", "Builders", "Civil engineers"], "info@altimap.ca", "416-990-3001", ["Greater Toronto Area"]),
    lead("Watson Land Surveyors Ltd.", "Belleville", "https://www.watsonsurveyors.ca/", ["Topographic plans", "Construction layout", "Condominium plans", "Legal boundary surveys"], ["Builders", "Municipalities", "Developers"], "info@watsonsurveyors.ca", "613-962-9521", ["South Hastings", "Prince Edward County"]),
    lead("Avant Garde Geomatics", "Kingston", "https://aggeo.ca/", ["Topographic surveying and mapping", "3D scanning", "LiDAR", "Drones", "Construction and land development"], ["Developers", "Commercial clients", "Municipalities"], "info@aggeo.ca", "613-699-7630", ["Eastern Ontario", "Northern Ontario"]),
    lead("JAYMAC Land Surveys Inc.", "Perth", "https://www.jaymaclandsurveys.com/services", ["Topographic plans", "Construction stakeouts", "DTM/TIN models for machine control", "3D LiDAR scanning and mapping", "GIS data collection"], ["Builders", "Construction companies", "Infrastructure companies", "Municipalities"], "info@jaymaclandsurveys.com", "613-701-3220", ["Eastern Ontario"]),
    lead("Vaughan Land Surveyors", "Colborne", "https://www.vaughansurveys.com/", ["Topographic surveys", "Construction layout", "Subdivision planning", "GNSS field execution"], ["Developers", "Municipalities", "Property owners"], "info@vaughansurveys.com", "416-839-1530", ["Ontario"]),
    lead("R-PE Surveying Ltd.", "Woodbridge", "https://www.r-pe.ca/", ["Construction layout", "Topographic surveys", "Volume determination", "Bathymetric surveys", "Geodetic surveys"], ["Land developers", "Home builders", "Construction companies"], "info@r-pe.ca", "416-635-5000", ["South-Central Ontario"]),
    lead("GEOPLAN Surveying Ltd.", "Toronto", "https://geoplansurveying.com/", ["Topographic surveys", "Construction surveys", "Subdivision plans", "Cadastral surveys"], ["Engineering firms", "Architects", "Builders", "Development companies"], "info@geoplansurveying.com", "647-479-4649", ["Greater Toronto Area"]),
    lead("Bishop Geyer Surveying Inc.", "Haliburton", "https://www.bgsurveys.ca/services", ["Topographic surveys", "Construction and grading", "3-D laser scanning", "GPS surveys", "As-built surveys"], ["Residential clients", "Commercial clients", "Industrial clients"], "info@bgsurveys.ca", "705-457-2811", ["Haliburton", "North Hastings", "Northern Kawartha Lakes"]),
    lead("Schultz Barrette Surveying", "Hawkesbury", "https://sbsurveying1.althosted.com/services/topographic-surveys", ["Topographic surveys", "GNSS surveys", "Terrestrial LiDAR", "Drone technology", "Construction planning"], ["Residential developers", "Commercial developers", "Industrial developers"], "info@sbsurveying.ca", "613-632-7611", ["Eastern Ontario"]),
    lead("HJV", "Vaughan", "https://www.hjv-ols.ca/", ["Topographic surveys", "Construction layout", "Control surveys", "Roof surveys", "Government agency surveying"], ["Construction companies", "Government agencies", "Engineers", "Architects"], "hjv@hjv-ols.ca", "905-660-4000", ["Southern Ontario"]),
    lead("Better Measures", "Flesherton", "https://bettermeasures.ca/", ["Topographic and site plans", "Construction layout", "Bathymetric survey", "Volume calculations", "Data preparation"], ["Contractors", "Engineering teams", "Construction clients"], "bmbetts@everus.ca", "519-372-5855", ["Ontario"], confidence=85),
    lead("SBM Geomatics", "London", "https://www.sbmgeomatics.ca/", ["Field engineering", "Topographical plans", "Volume calculations", "LiDAR feature extraction", "Control networks"], ["Public sector", "Private sector", "Design teams"], "info@sbmgeomatics.ca", "519-914-1134", ["Southwestern Ontario"]),
    lead("F.S. Surveying Inc.", "Mississauga", "https://www.fssurveying.com/about", ["Engineering surveys", "As-built surveys", "Topographic surveys", "Construction layout", "Monitoring surveys"], ["Public sector", "Private sector", "Industrial clients"], "NOT CONFIRMED", "NOT CONFIRMED", ["Greater Toronto Area"], confidence=75),
    lead("Speight, van Nostrand & Gibson Limited", "Toronto", "https://svng.on.ca/services.html", ["Topographic and engineering surveys", "Construction layout", "GIS", "3D scanning and modelling", "Monitoring and control surveys"], ["Developers", "Engineers", "Construction clients"], "toronto@svng.on.ca", "416-749-7864", ["Toronto", "Greater Toronto Area"]),
    lead("MTE Consultants - Surveying", "Kitchener", "https://mte85.com/services/surveys/", ["Topographical surveys", "Construction surveys", "Bridge and culvert layout", "3D surface modelling", "Volume calculations"], ["Construction contractors", "Public sector", "Private developers"], "NOT CONFIRMED", "519-743-6500", ["Kitchener", "London", "Burlington", "Toronto"]),
    lead("Farley, Smith & Denis Surveying Ltd.", "Ottawa", "https://fsdsurveys.ca/our-services", ["Topographic surveys", "Construction layout and as-built surveys", "Reference plans", "Real property reports"], ["Residential clients", "Commercial clients", "Institutional clients", "Government clients"], "info@fsdsurveys.ca", "613-727-8226", ["Ottawa", "Eastern Ontario"]),
    lead("Protect Your Boundaries Inc.", "Mississauga", "https://www.protectyourboundaries.ca/commercial-property-survey.html", ["Topographic surveys", "Existing conditions surveys", "Construction layout", "As-constructed surveys", "Commercial property surveys"], ["Commercial property owners", "Developers", "Legal and real estate professionals"], "info@ProtectYourBoundaries.ca", "877-392-2662", ["Greater Toronto Area"]),
    lead("ProMap Surveying", "Richmond Hill", "https://promapsurveying.com/", ["Topographic surveys", "Construction layout", "Site and grading plans", "3D laser scanning", "Monitoring"], ["Property owners", "Builders", "Developers"], "NOT CONFIRMED", "289-637-7775", ["Greater Toronto Area"], confidence=85),
    lead("GeoSolutions Surveying & Engineering", "Whitby", "https://www.geosolutionsurveying.com/", ["Topographic surveys", "Construction layout", "Drone mapping", "LiDAR", "As-built surveys"], ["Engineers", "Architects", "Contractors", "Developers"], "info@geosolutionsurveying.com", "905-429-0310", ["Greater Toronto Area", "Durham Region"]),
    lead("Grad Surveying", "Toronto", "https://www.gradsurveying.ca/", ["Topographical surveys", "Construction layout surveys", "As-built surveys", "Geodetic control surveys", "Volume calculations"], ["Developers", "Builders", "Property owners"], "info@gradsurveying.ca", "647-518-1362", ["Greater Toronto Area"]),
    lead("Paya Surveying", "Markham", "https://payasurveying.ca/", ["Construction layout", "Topographic mapping", "Drone/UAV surveying", "LiDAR mapping", "3D scanning"], ["Engineers", "Builders", "Architects", "Developers"], "info@payasurveying.ca", "289-906-4449", ["Greater Toronto Area"]),
    lead("Topotec Inc.", "Toronto", "https://www.topotec.ca/", ["Topographic and engineering surveys", "Construction surveying", "As-built surveys", "LiDAR surveys", "Drone photogrammetry"], ["Property owners", "Developers", "Contractors"], "NOT CONFIRMED", "NOT CONFIRMED", ["Greater Toronto Area"], confidence=75),
    lead("Pelto Consulting", "Lively", "https://pelto.ca/", ["Industrial survey services", "LiDAR scanning", "3D mapping", "UAV drone surveys", "Volumetric calculations"], ["Industrial clients", "Mining companies", "Construction clients", "Engineering firms"], "keith@pelto.ca", "705-929-2295", ["Northern Ontario", "Canada"]),
    lead("Stratus Aerial Geomatics", "Vaughan", "https://stratusgeomatics.ca/", ["Drone mapping", "LiDAR survey", "Topographic surveys", "Machine control files", "GPS data preparation"], ["Construction teams", "Engineering teams", "Earthworks contractors"], "NOT CONFIRMED", "NOT CONFIRMED", ["Greater Toronto Area", "Ontario"], confidence=75),
    lead("Ontario Drone Survey", "Etobicoke", "https://ontariodronesurvey.ca/", ["Drone surveying", "Topographic mapping", "Volumetric calculations", "Thermal roof inspections", "3D renders"], ["Construction clients", "Agriculture clients", "Industrial roofing clients"], "ontariodronesurvey@gmail.com", "705-816-5352", ["Ontario"]),
    lead("Elev8 Visions", "Ontario", "https://www.elev8visions.com/drone-survey-services", ["Drone survey services", "Topographic surveys", "Aerial LiDAR surveys", "Volumetric calculations", "Orthomosaics"], ["Construction clients", "Aggregates", "Earthworks clients"], "NOT CONFIRMED", "NOT CONFIRMED", ["Ontario"], confidence=75),
    lead("Fairhall, Moffatt & Woodland Limited", "Ottawa", "https://www.fmw.on.ca", ["Land surveying", "Topographic surveys", "Construction layout", "Reference plans"], ["Developers", "Engineers", "Municipal clients"], "NOT CONFIRMED", "NOT CONFIRMED", ["Ottawa", "Eastern Ontario"], confidence=70),
    lead("Ivan B Wallace OLS Ltd.", "Bowmanville", "https://www.ibwsurveyors.com", ["Land surveying", "Topographic surveys", "Construction layout", "Reference plans"], ["Developers", "Builders", "Municipal clients"], "NOT CONFIRMED", "NOT CONFIRMED", ["Durham Region", "Ontario"], confidence=70),
    lead("MacKay MacKay & Peters Limited", "Burlington", "https://www.mmplimited.com", ["Land surveying", "Topographic surveys", "Construction layout", "Reference plans"], ["Developers", "Builders", "Engineers"], "NOT CONFIRMED", "NOT CONFIRMED", ["Halton", "Greater Toronto Area"], confidence=70),
    lead("RivaCore", "Brampton", "https://www.rivacore.com", ["Land surveying", "Geomatics", "Mapping", "Site data services"], ["Construction clients", "Engineering teams", "Infrastructure owners"], "NOT CONFIRMED", "NOT CONFIRMED", ["Greater Toronto Area"], confidence=70),
    lead("Surveyors On Site Inc.", "Windsor", "http://www.surveyorsonsite.com", ["Land surveying", "Construction layout", "Topographic surveys", "Site survey support"], ["Builders", "Developers", "Construction clients"], "NOT CONFIRMED", "NOT CONFIRMED", ["Windsor", "Southwestern Ontario"], confidence=70),
    lead("Van Harten Surveying Inc.", "Guelph", "https://www.vanharten.com", ["Land surveying", "Topographic surveys", "Construction layout", "Survey records"], ["Developers", "Builders", "Municipal clients"], "NOT CONFIRMED", "NOT CONFIRMED", ["Guelph", "Waterloo Region", "Wellington County"], confidence=70),
    lead("J.D. Barnes Limited", "Markham", "https://www.jdbarnes.com", ["Land surveying", "Aerial mapping", "GIS", "Construction layout", "Topographic surveys"], ["Developers", "Municipal clients", "Infrastructure owners"], "NOT CONFIRMED", "NOT CONFIRMED", ["Ontario", "Canada"], confidence=70),
    lead("A.T. McLaren Limited", "Toronto", "https://www.atmclaren.com", ["Ontario land surveying", "Topographic surveys", "Construction layout", "Reference plans"], ["Developers", "Builders", "Engineers"], "NOT CONFIRMED", "NOT CONFIRMED", ["Greater Toronto Area"], confidence=70),
    lead("Callon Dietz Inc.", "London", "https://callondietz.com", ["Land surveying", "Geomatics", "Topographic surveys", "Construction layout"], ["Developers", "Public sector", "Private sector"], "NOT CONFIRMED", "NOT CONFIRMED", ["Ontario"], confidence=70),
    lead("Coote Hiley Jemmett Limited", "Toronto", "https://www.chjsurveyors.com", ["Land surveying", "Topographic surveys", "Construction layout", "Reference plans"], ["Developers", "Engineers", "Legal professionals"], "NOT CONFIRMED", "NOT CONFIRMED", ["Greater Toronto Area"], confidence=70),
    lead("Krcmar Surveyors Ltd.", "Thornhill", "https://www.krcmar.ca", ["Construction surveying", "Land surveying", "Topographic surveys", "3D laser scanning", "Control surveys"], ["Construction clients", "Developers", "Engineers"], "info@krcmar.ca", "905-738-0053", ["Greater Toronto Area"]),
    lead("Alex Marton Ltd.", "Concord", "http://www.amsurveying.ca", ["Topographic surveys", "Construction layout surveys", "Volume calculations", "GPS surveys", "3D LiDAR scanning"], ["Government agencies", "Builders", "Engineers", "Architects"], "alex@amsurveying.ca", "905-879-9889", ["Greater Toronto Area"]),
    lead("Tarasick McMillan Kubicki Limited", "Mississauga", "http://www.tmksurveyors.com", ["Topographical plans", "Site grading plans", "Control surveying", "Construction layout", "Volume calculations"], ["Developers", "Builders", "Engineers"], "NOT CONFIRMED", "NOT CONFIRMED", ["Mississauga", "Greater Toronto and Hamilton Area"], confidence=70),
    lead("Lejan Land Surveying Inc.", "Hamilton", "https://www.lejansurveying.ca/", ["Engineering surveys", "Topographic surveys", "Construction layout", "DTM", "Volume calculations"], ["Developers", "Builders", "Engineering clients"], "NOT CONFIRMED", "905-643-6131", ["Hamilton", "Burlington", "Oakville", "Greater Toronto Area"]),
    lead("Hopkins Chitty Land Surveyors Inc.", "Kingston", "https://www.hopkinschitty.com/", ["Topographic surveys", "Construction layout", "Robotic total station surveys", "GPS surveys", "Digital land survey information"], ["Builders", "Architects", "Engineers", "Municipalities"], "info@hopkinschitty.com", "613-384-9266", ["Kingston", "Brockville", "Eastern Ontario"]),
    lead("Kerr & Potvin Inc.", "Carleton Place", "https://www.kpsurveyors.com/municipalities", ["Topographic and site detail surveys", "Culvert and bridge surveys", "Hydrographic surveys", "Public works surveys"], ["Municipalities", "Public works departments", "Property owners"], "info@kpsurveyors.com", "613-412-4222", ["Eastern Ontario"]),
    lead("Becker & Starcevic Ltd.", "Ontario", "https://becker-starcevic.ca/resources-and-faq", ["Boundary surveys", "Topographic surveys", "Construction staking", "Grading plans", "Reference plans"], ["Property owners", "Construction professionals", "Developers"], "info@becker-starcevic.ca", "NOT CONFIRMED", ["Ontario"], confidence=85),
    lead("Rouse Surveyors Inc.", "Toronto", "http://www.rousesurveyors.com", ["Construction layout", "Rail and transit surveys", "3D laser scanning", "Monitoring surveys", "Drone surveying"], ["Contractors", "Engineers", "Developers", "Municipalities"], "info@rousesurveyors.com", "NOT CONFIRMED", ["Greater Toronto Area", "Ontario"], confidence=85),
    lead("Young & Young Surveying", "Toronto", "https://www.youngandyoungsurveying.com", ["Land surveying", "Topographic surveys", "Construction layout", "Reference plans"], ["Developers", "Builders", "Engineers"], "NOT CONFIRMED", "NOT CONFIRMED", ["Greater Toronto Area"], confidence=65),
    lead("Avanti Surveying Inc.", "Toronto", "https://www.avantisurveying.com", ["Land surveying", "Construction surveying", "Topographic surveys", "Site plans"], ["Developers", "Builders", "Construction clients"], "NOT CONFIRMED", "NOT CONFIRMED", ["Greater Toronto Area"], confidence=65),
    lead("Y. Zhang Surveying Limited", "Mississauga", "https://www.yzhangsurveying.com", ["Land surveying", "Topographic surveys", "Construction layout", "Reference plans"], ["Developers", "Builders", "Property owners"], "NOT CONFIRMED", "NOT CONFIRMED", ["Greater Toronto Area"], confidence=65),
    lead("Monument-Urso Surveying Ltd.", "Ottawa", "https://www.monument-urso.ca/faqs", ["Topographic surveys", "Construction surveys", "Legal boundary surveys", "Property surveys"], ["Property owners", "Construction clients", "Developers"], "info@monument-urso.ca", "613-800-1583", ["Ottawa", "Sault Ste. Marie"]),
    lead("GroundPulse", "Ontario", "https://groundpulse.ca/capabilities", ["Topographic site surveys", "Construction layout and staking", "Legal survey coordination", "Utility locating integration"], ["Contractors", "Excavators", "Developers", "Infrastructure owners"], "NOT CONFIRMED", "519-902-5428", ["Ontario"], confidence=75),
    lead("GeoVerra", "Ontario", "https://www.geoverra.com", ["Geomatics", "Surveying", "LiDAR", "Mapping", "Construction survey support"], ["Infrastructure owners", "Energy clients", "Construction clients"], "NOT CONFIRMED", "NOT CONFIRMED", ["Ontario", "Canada"], confidence=65),
    lead("Tham Surveying Limited", "Toronto", "https://thamsurveying.com", ["Land surveying", "Topographic surveys", "Construction layout", "Reference plans"], ["Developers", "Builders", "Property owners"], "NOT CONFIRMED", "NOT CONFIRMED", ["Greater Toronto Area"], confidence=65),
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
    for item in WAVE1:
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
    print(f"Added {len(added)} Wave 1 surveyor/geomatics leads. Total leads: {len(leads)}")


if __name__ == "__main__":
    main()
