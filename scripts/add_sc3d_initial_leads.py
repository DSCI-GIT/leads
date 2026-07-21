#!/usr/bin/env python3
"""Create the initial SplatCap3D lead database and CSV export."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "sc3d_leads.json"
CSV_PATH = ROOT / "sc3d_leads.csv"
VERIFIED = "2026-07-21"

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

CATEGORY_PROFILE = {
    "Real Estate Brokerage": {
        "services": ["Luxury listing marketing", "Property walkthroughs", "Remote buyer previews", "Website and MLS media"],
        "clients": ["Brokerages", "Listing agents", "Property sellers"],
        "signals": ["High-value spaces", "Remote buyer previews", "Embeddable walkthroughs"],
        "angle": "Offer photorealistic 3D walkthroughs that let buyers experience premium listings online before booking showings.",
        "fit": 88,
    },
    "Builder/Developer": {
        "services": ["Model home tours", "Construction progress capture", "Pre-sale marketing", "Site documentation"],
        "clients": ["Home builders", "Developers", "Sales centres"],
        "signals": ["Model homes", "Progress updates", "Pre-sale visualization"],
        "angle": "Offer digital twins for model homes, sales centres and staged progress updates that help buyers and stakeholders understand the space.",
        "fit": 86,
    },
    "Commercial Property": {
        "services": ["Leasing walkthroughs", "Tenant improvement documentation", "Building marketing", "Remote stakeholder review"],
        "clients": ["Landlords", "Property managers", "Leasing teams"],
        "signals": ["Leasing", "Remote stakeholder review", "Embeddable tours"],
        "angle": "Offer hosted digital twins for leasing, capital planning and remote stakeholder walkthroughs without repeated site visits.",
        "fit": 87,
    },
    "Hospitality/Event Venue": {
        "services": ["Venue tours", "Event sales", "Room and layout previews", "Guest experience marketing"],
        "clients": ["Hotels", "Venues", "Event sales teams"],
        "signals": ["Venue tours", "Layout previews", "Sales embeds"],
        "angle": "Offer immersive venue twins that planners can walk through remotely when comparing rooms, layouts and guest flow.",
        "fit": 90,
    },
    "Tourism/Heritage": {
        "services": ["Visitor experience", "Collections and site documentation", "Virtual access", "Educational walkthroughs"],
        "clients": ["Museums", "Heritage sites", "Tourism operators"],
        "signals": ["Virtual access", "Public experience", "Educational walkthroughs"],
        "angle": "Offer photorealistic 3D access for exhibits, historic interiors and visitor experiences that can be shared online.",
        "fit": 89,
    },
    "Film/Virtual Production": {
        "services": ["Location scouting", "Virtual production assets", "Set documentation", "Creative previsualization"],
        "clients": ["Studios", "Production companies", "Location managers"],
        "signals": ["Location scouting", "Virtual production", "Reusable 3D environments"],
        "angle": "Offer spatial scans for remote location scouting, virtual production reference and reusable digital environments.",
        "fit": 87,
    },
    "Retail/Showroom": {
        "services": ["Showroom tours", "Product environment capture", "Customer experience marketing", "Web embeds"],
        "clients": ["Retailers", "Showrooms", "Brand teams"],
        "signals": ["Showrooms", "Customer experience", "Interactive web embeds"],
        "angle": "Offer interactive showroom twins that help customers explore the space and product environment before visiting.",
        "fit": 84,
    },
    "Industrial/Training": {
        "services": ["Facility walkthroughs", "Training environments", "Safety orientation", "Operations documentation"],
        "clients": ["Facility owners", "Operations teams", "Training managers"],
        "signals": ["Training", "Operations documentation", "Restricted or complex spaces"],
        "angle": "Offer digital twins for training, orientation and operational context where repeat site visits are costly or disruptive.",
        "fit": 86,
    },
}

LEADS = [
    ("Real Estate Brokerage", "Sotheby's International Realty Canada", "Toronto", "https://sothebysrealty.ca/"),
    ("Real Estate Brokerage", "Chestnut Park Real Estate", "Toronto", "https://www.chestnutpark.com/"),
    ("Real Estate Brokerage", "Harvey Kalles Real Estate", "Toronto", "https://harveykalles.com/"),
    ("Real Estate Brokerage", "Forest Hill Real Estate", "Toronto", "https://foresthill.com/"),
    ("Real Estate Brokerage", "The Agency Toronto", "Toronto", "https://www.theagencyre.com/"),
    ("Real Estate Brokerage", "RE/MAX Hallmark", "Toronto", "https://www.remaxhallmark.com/"),
    ("Real Estate Brokerage", "Royal LePage Signature Realty", "Toronto", "https://royallepagesignature.com/"),
    ("Real Estate Brokerage", "Right At Home Realty", "Toronto", "https://www.rightathomerealty.com/"),
    ("Real Estate Brokerage", "Engel & Volkers Toronto", "Toronto", "https://toronto.evrealestate.com/"),
    ("Real Estate Brokerage", "Berkshire Hathaway HomeServices Toronto Realty", "Toronto", "https://bhhst.ca/"),
    ("Builder/Developer", "Mattamy Homes", "Toronto", "https://mattamyhomes.com/"),
    ("Builder/Developer", "Tridel", "Toronto", "https://www.tridel.com/"),
    ("Builder/Developer", "The Daniels Corporation", "Toronto", "https://danielshomes.ca/"),
    ("Builder/Developer", "Minto Communities", "Ottawa", "https://www.minto.com/"),
    ("Builder/Developer", "Great Gulf", "Toronto", "https://greatgulf.com/"),
    ("Builder/Developer", "Empire Communities", "Vaughan", "https://www.empirecommunities.com/"),
    ("Builder/Developer", "Tribute Communities", "Pickering", "https://www.tributecommunities.com/"),
    ("Builder/Developer", "Fusion Homes", "Guelph", "https://www.fusionhomes.com/"),
    ("Builder/Developer", "Reid's Heritage Homes", "Cambridge", "https://www.reidsheritagehomes.com/"),
    ("Builder/Developer", "Losani Homes", "Hamilton", "https://www.losanihomes.com/"),
    ("Commercial Property", "Oxford Properties", "Toronto", "https://www.oxfordproperties.com/"),
    ("Commercial Property", "Cadillac Fairview", "Toronto", "https://www.cadillacfairview.com/"),
    ("Commercial Property", "RioCan REIT", "Toronto", "https://www.riocan.com/"),
    ("Commercial Property", "Choice Properties REIT", "Toronto", "https://www.choicereit.ca/"),
    ("Commercial Property", "SmartCentres REIT", "Vaughan", "https://www.smartcentres.com/"),
    ("Commercial Property", "First Capital REIT", "Toronto", "https://fcr.ca/"),
    ("Commercial Property", "Allied Properties REIT", "Toronto", "https://www.alliedreit.com/"),
    ("Commercial Property", "GWL Realty Advisors", "Toronto", "https://www.gwlrealtyadvisors.com/"),
    ("Commercial Property", "Morguard", "Mississauga", "https://www.morguard.com/"),
    ("Commercial Property", "Cushman & Wakefield Canada", "Toronto", "https://www.cushmanwakefield.com/en/canada"),
    ("Hospitality/Event Venue", "Fairmont Royal York", "Toronto", "https://www.fairmont-royal-york.com/"),
    ("Hospitality/Event Venue", "Hotel X Toronto", "Toronto", "https://hotelxtoronto.com/"),
    ("Hospitality/Event Venue", "The Drake Hotel", "Toronto", "https://www.thedrake.ca/"),
    ("Hospitality/Event Venue", "Liberty Grand Entertainment Complex", "Toronto", "https://libertygrand.com/"),
    ("Hospitality/Event Venue", "Evergreen Brick Works", "Toronto", "https://www.evergreen.ca/"),
    ("Hospitality/Event Venue", "The Arlington Estate", "Vaughan", "https://thearlingtonestate.com/"),
    ("Hospitality/Event Venue", "Elora Mill Hotel & Spa", "Elora", "https://eloramill.ca/"),
    ("Hospitality/Event Venue", "Pillar and Post", "Niagara-on-the-Lake", "https://www.vintage-hotels.com/pillar-and-post/"),
    ("Hospitality/Event Venue", "Shaw Centre", "Ottawa", "https://shaw-centre.com/"),
    ("Hospitality/Event Venue", "Niagara Falls Convention Centre", "Niagara Falls", "https://www.fallsconventions.com/"),
    ("Tourism/Heritage", "Royal Ontario Museum", "Toronto", "https://www.rom.on.ca/"),
    ("Tourism/Heritage", "Art Gallery of Ontario", "Toronto", "https://ago.ca/"),
    ("Tourism/Heritage", "Aga Khan Museum", "Toronto", "https://agakhanmuseum.org/"),
    ("Tourism/Heritage", "McMichael Canadian Art Collection", "Kleinburg", "https://mcmichael.com/"),
    ("Tourism/Heritage", "Fort Henry National Historic Site", "Kingston", "https://www.forthenry.com/"),
    ("Tourism/Heritage", "Stratford Festival", "Stratford", "https://www.stratfordfestival.ca/"),
    ("Tourism/Heritage", "Canadian Warplane Heritage Museum", "Hamilton", "https://www.warplane.com/"),
    ("Tourism/Heritage", "Science North", "Sudbury", "https://www.sciencenorth.ca/"),
    ("Tourism/Heritage", "Ontario Science Centre", "Toronto", "https://www.ontariosciencecentre.ca/"),
    ("Tourism/Heritage", "Casa Loma", "Toronto", "https://casaloma.ca/"),
    ("Film/Virtual Production", "Pinewood Toronto Studios", "Toronto", "https://pinewoodgroup.com/studios/pinewood-toronto-studios"),
    ("Film/Virtual Production", "William F. White International", "Toronto", "https://www.whites.com/"),
    ("Film/Virtual Production", "Cinespace Studios Toronto", "Toronto", "https://www.cinespace.com/"),
    ("Film/Virtual Production", "Studio City Toronto", "Toronto", "https://studiocitytoronto.com/"),
    ("Film/Virtual Production", "TriBro Studios", "Toronto", "https://www.tribrostudios.com/"),
    ("Film/Virtual Production", "Stratagem Studios", "Toronto", "https://www.stratagemstudios.com/"),
    ("Film/Virtual Production", "Soho VFX", "Toronto", "https://www.sohovfx.com/"),
    ("Film/Virtual Production", "Rocket Science VFX", "Toronto", "https://www.rsvfx.com/"),
    ("Film/Virtual Production", "Mr. X", "Toronto", "https://www.mrxfx.com/"),
    ("Film/Virtual Production", "Pixomondo Toronto", "Toronto", "https://www.pixomondo.com/"),
    ("Retail/Showroom", "IKEA Canada", "Burlington", "https://www.ikea.com/ca/en/"),
    ("Retail/Showroom", "EQ3 Toronto", "Toronto", "https://www.eq3.com/ca/en"),
    ("Retail/Showroom", "Elte", "Toronto", "https://www.elte.com/"),
    ("Retail/Showroom", "Tepperman's", "Windsor", "https://www.tepermans.com/"),
    ("Retail/Showroom", "Mobilia", "Toronto", "https://mobilia.ca/"),
    ("Retail/Showroom", "Tasco Appliances", "Toronto", "https://www.tascoappliance.ca/"),
    ("Retail/Showroom", "Porsche Centre Oakville", "Oakville", "https://www.porschecentreoakville.com/"),
    ("Retail/Showroom", "Pfaff Automotive Partners", "Vaughan", "https://www.pfaffauto.com/"),
    ("Retail/Showroom", "Roche Bobois Toronto", "Toronto", "https://www.roche-bobois.com/en-CA/showrooms/toronto"),
    ("Retail/Showroom", "The Art Shoppe", "Toronto", "https://www.theartshoppe.com/"),
    ("Industrial/Training", "Bruce Power", "Tiverton", "https://www.brucepower.com/"),
    ("Industrial/Training", "Ontario Power Generation", "Toronto", "https://www.opg.com/"),
    ("Industrial/Training", "Stelco", "Hamilton", "https://www.stelco.com/"),
    ("Industrial/Training", "ArcelorMittal Dofasco", "Hamilton", "https://dofasco.arcelormittal.com/"),
    ("Industrial/Training", "Toyota Motor Manufacturing Canada", "Cambridge", "https://tmmc.ca/"),
    ("Industrial/Training", "Honda of Canada Mfg.", "Alliston", "https://www.hondacanadamfg.ca/"),
    ("Industrial/Training", "Magna International", "Aurora", "https://www.magna.com/"),
    ("Industrial/Training", "Linamar", "Guelph", "https://www.linamar.com/"),
    ("Industrial/Training", "Maple Leaf Foods", "Mississauga", "https://www.mapleleaffoods.com/"),
    ("Industrial/Training", "Sleeman Breweries", "Guelph", "https://sleemanbreweries.ca/"),
]


def slug(name: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return f"sc3d-{value}"[:80]


def lead(category: str, name: str, city: str, website: str) -> dict[str, object]:
    profile = CATEGORY_PROFILE[category]
    return {
        "id": slug(name),
        "company_name": name,
        "company_type": category,
        "hq_city": city,
        "hq_province": "Ontario",
        "regions_served": ["Ontario"],
        "primary_services": profile["services"],
        "client_types": profile["clients"],
        "evidence_links": [website],
        "summary": f"{category} account target where photorealistic 3D spaces could support {', '.join(profile['services'][:3]).lower()}.",
        "fit_rationale": f"SC3D fit is based on a visible, valuable or complex space that can benefit from hosted Gaussian-splat digital twins, remote walkthroughs, web embeds, annotations, measurement and repeat capture. Public category signals include {', '.join(profile['signals']).lower()}.",
        "drone_lidar_fit_signals": profile["signals"],
        "contacts": [
            {
                "name": "NOT CONFIRMED",
                "title": "NOT CONFIRMED",
                "source_url": website,
                "contact_method": "Website/contact form",
            }
        ],
        "public_email": "NOT CONFIRMED",
        "public_phone": "NOT CONFIRMED",
        "contact_form_url": "NOT CONFIRMED",
        "outreach_angle": profile["angle"],
        "fit_score": profile["fit"],
        "confidence_score": 70,
        "pipeline_stage": "New",
        "notes": "Initial SplatCap3D lead database. Qualification is based on spatial/digital-twin fit, not drone survey fit. Verify contacts before outreach.",
        "last_verified_date": VERIFIED,
    }


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
    leads = [lead(*item) for item in LEADS]
    names = [item["company_name"].casefold() for item in leads]
    if len(names) != len(set(names)):
        raise SystemExit("Duplicate SC3D company names found")
    JSON_PATH.write_text(json.dumps(leads, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    with CSV_PATH.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        for item in leads:
            writer.writerow({field: csv_cell(item[field]) for field in FIELDS})
    print(f"Wrote {len(leads)} SplatCap3D leads to {JSON_PATH.name} and {CSV_PATH.name}")


if __name__ == "__main__":
    main()
