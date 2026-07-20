#!/usr/bin/env python3
"""Append Wave 3 leads across the remaining high-fit DSCI categories."""

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

SOURCES = {
    "municipal": "https://www.ontario.ca/page/list-ontario-municipalities",
    "utilities": "https://www.oeb.ca/ontarios-energy-sector/list-licensed-companies",
    "aggregates": "https://www.ossga.com/membership/active-members/",
    "bild": "https://www.bildgta.ca/about/find-a-member/",
    "hcra": "https://obd.hcraontario.ca/buildersearchresults",
}

CATEGORY_PROFILE = {
    "Municipal/Public Works": {
        "services": ["Roads and bridges", "Public works", "Water and wastewater", "Stormwater assets", "Capital projects"],
        "clients": ["Municipal public works", "Engineering departments", "Operations teams"],
        "signals": ["Roads and bridges", "Water and wastewater", "Stormwater assets", "Capital projects"],
        "angle": "Offer aerial asset documentation, corridor mapping, construction-progress capture and inspection imagery for public works and capital projects.",
        "fit": 86,
    },
    "Utilities/Energy": {
        "services": ["Electricity distribution", "Utility infrastructure", "Pole line and corridor assets", "Substation and facility assets"],
        "clients": ["Utilities", "Municipal shareholders", "Infrastructure owners"],
        "signals": ["Utility infrastructure", "Pole line and corridor assets", "Substation and facility assets"],
        "angle": "Offer RPAS corridor patrol imagery, LiDAR-ready field capture, utility asset documentation and difficult-access inspection support.",
        "fit": 84,
    },
    "Aggregates/Materials": {
        "services": ["Aggregate production", "Pits and quarries", "Stockpile management", "Haul roads and site works"],
        "clients": ["Aggregate producers", "Construction materials firms", "Site operations teams"],
        "signals": ["Pits and quarries", "Stockpile management", "Haul roads and site works"],
        "angle": "Offer stockpile volume surveys, quarry/pit mapping, haul-road documentation, rehabilitation progress imagery and site-change monitoring.",
        "fit": 88,
    },
    "Developer/Property": {
        "services": ["Land development", "Construction projects", "Property assets", "Building envelope and site documentation"],
        "clients": ["Developers", "Property owners", "Asset managers"],
        "signals": ["Land development", "Construction projects", "Property assets", "Building envelope and site documentation"],
        "angle": "Offer construction progress capture, marketing-safe aerial documentation, roof/envelope inspection imagery and site condition records.",
        "fit": 82,
    },
}


def slug(category: str, name: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    prefix = re.sub(r"[^a-z0-9]+", "-", category.lower()).strip("-")
    return f"on-wave3-{prefix}-{value}"[:90]


def lead(
    category: str,
    name: str,
    city: str,
    website: str,
    source: str,
    regions: list[str] | None = None,
    email: str = "NOT CONFIRMED",
    phone: str = "NOT CONFIRMED",
    confidence: int | None = None,
) -> dict[str, object]:
    profile = CATEGORY_PROFILE[category]
    evidence = [website, source] if website != source else [source]
    if confidence is None:
        confidence = 75 if website != source else 65
        if email != "NOT CONFIRMED":
            confidence += 10
        if phone != "NOT CONFIRMED":
            confidence += 10
        confidence = min(confidence, 95)
    return {
        "id": slug(category, name),
        "company_name": name,
        "company_type": category,
        "hq_city": city,
        "hq_province": "Ontario",
        "regions_served": regions or ["Ontario"],
        "primary_services": profile["services"],
        "client_types": profile["clients"],
        "evidence_links": evidence,
        "summary": f"{category} lead with public-source relevance to {', '.join(profile['services'][:3]).lower()} work.",
        "fit_rationale": f"Public-source category fit indicates {', '.join(profile['services'][:4]).lower()} responsibilities or market activity, creating a fit for DSCI aerial mapping, site documentation, LiDAR-ready capture and inspection support.",
        "drone_lidar_fit_signals": profile["signals"],
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
        "contact_form_url": "NOT CONFIRMED",
        "outreach_angle": profile["angle"],
        "fit_score": profile["fit"],
        "confidence_score": confidence,
        "pipeline_stage": "New",
        "notes": "Wave 3 remaining-category expansion; verify contact details before outreach.",
        "last_verified_date": VERIFIED,
    }


MUNICIPAL_PUBLIC_WORKS = [
    ("City of Toronto Public Works", "Toronto", "https://www.toronto.ca/", ["Toronto"]),
    ("City of Ottawa Public Works", "Ottawa", "https://ottawa.ca/", ["Ottawa", "Eastern Ontario"]),
    ("City of Mississauga Works Operations", "Mississauga", "https://www.mississauga.ca/", ["Peel", "Greater Toronto Area"]),
    ("City of Brampton Public Works", "Brampton", "https://www.brampton.ca/", ["Peel", "Greater Toronto Area"]),
    ("City of Hamilton Public Works", "Hamilton", "https://www.hamilton.ca/", ["Hamilton"]),
    ("City of London Public Works", "London", "https://london.ca/", ["London", "Southwestern Ontario"]),
    ("City of Markham Engineering and Public Works", "Markham", "https://www.markham.ca/", ["York Region"]),
    ("City of Vaughan Public Works", "Vaughan", "https://www.vaughan.ca/", ["York Region"]),
    ("City of Kitchener Infrastructure Services", "Kitchener", "https://www.kitchener.ca/", ["Waterloo Region"]),
    ("City of Windsor Public Works", "Windsor", "https://www.citywindsor.ca/", ["Windsor", "Essex County"]),
    ("City of Richmond Hill Public Works", "Richmond Hill", "https://www.richmondhill.ca/", ["York Region"]),
    ("Town of Oakville Public Works", "Oakville", "https://www.oakville.ca/", ["Halton Region"]),
    ("City of Burlington Engineering Services", "Burlington", "https://www.burlington.ca/", ["Halton Region"]),
    ("City of Greater Sudbury Infrastructure Services", "Sudbury", "https://www.greatersudbury.ca/", ["Northern Ontario"]),
    ("City of Oshawa Works Services", "Oshawa", "https://www.oshawa.ca/", ["Durham Region"]),
    ("City of Barrie Infrastructure Department", "Barrie", "https://www.barrie.ca/", ["Simcoe County"]),
    ("City of St. Catharines Engineering and Public Works", "St. Catharines", "https://www.stcatharines.ca/", ["Niagara Region"]),
    ("City of Cambridge Public Works", "Cambridge", "https://www.cambridge.ca/", ["Waterloo Region"]),
    ("City of Guelph Public Works", "Guelph", "https://guelph.ca/", ["Wellington County"]),
    ("Town of Whitby Public Works", "Whitby", "https://www.whitby.ca/", ["Durham Region"]),
    ("Town of Ajax Operations and Environmental Services", "Ajax", "https://www.ajax.ca/", ["Durham Region"]),
    ("Town of Milton Engineering Services", "Milton", "https://www.milton.ca/", ["Halton Region"]),
    ("City of Waterloo Transportation and Environmental Services", "Waterloo", "https://www.waterloo.ca/", ["Waterloo Region"]),
    ("City of Thunder Bay Infrastructure and Operations", "Thunder Bay", "https://www.thunderbay.ca/", ["Northwestern Ontario"]),
    ("Municipality of Chatham-Kent Public Works", "Chatham", "https://www.chatham-kent.ca/", ["Chatham-Kent"]),
    ("City of Brantford Engineering Services", "Brantford", "https://www.brantford.ca/", ["Brantford"]),
    ("City of Pickering Engineering Services", "Pickering", "https://www.pickering.ca/", ["Durham Region"]),
    ("City of Niagara Falls Municipal Works", "Niagara Falls", "https://niagarafalls.ca/", ["Niagara Region"]),
    ("City of Peterborough Public Works", "Peterborough", "https://www.peterborough.ca/", ["Peterborough County"]),
    ("City of Sault Ste. Marie Public Works", "Sault Ste. Marie", "https://saultstemarie.ca/", ["Northern Ontario"]),
    ("City of Sarnia Engineering and Operations", "Sarnia", "https://www.sarnia.ca/", ["Lambton County"]),
    ("Norfolk County Public Works", "Simcoe", "https://www.norfolkcounty.ca/", ["Norfolk County"]),
    ("Town of Caledon Public Works", "Caledon", "https://www.caledon.ca/", ["Peel", "Dufferin-Caledon"]),
    ("City of Welland Public Works", "Welland", "https://www.welland.ca/", ["Niagara Region"]),
    ("City of North Bay Engineering and Public Works", "North Bay", "https://www.northbay.ca/", ["Nipissing District"]),
    ("City of Belleville Transportation and Operations", "Belleville", "https://www.belleville.ca/", ["Hastings County"]),
    ("City of Cornwall Municipal Works", "Cornwall", "https://www.cornwall.ca/", ["Eastern Ontario"]),
    ("City of Timmins Public Works", "Timmins", "https://www.timmins.ca/", ["Northern Ontario"]),
    ("City of Quinte West Public Works", "Quinte West", "https://www.quintewest.ca/", ["Eastern Ontario"]),
    ("Town of Newmarket Public Works", "Newmarket", "https://www.newmarket.ca/", ["York Region"]),
    ("Town of Aurora Operational Services", "Aurora", "https://www.aurora.ca/", ["York Region"]),
    ("Town of Halton Hills Public Works", "Halton Hills", "https://www.haltonhills.ca/", ["Halton Region"]),
    ("Town of Orangeville Infrastructure Services", "Orangeville", "https://www.orangeville.ca/", ["Dufferin County"]),
    ("City of Orillia Environment and Infrastructure Services", "Orillia", "https://www.orillia.ca/", ["Simcoe County"]),
    ("City of Stratford Infrastructure Services", "Stratford", "https://www.stratford.ca/", ["Perth County"]),
    ("City of Brockville Public Works", "Brockville", "https://www.brockville.com/", ["Eastern Ontario"]),
    ("City of Owen Sound Public Works", "Owen Sound", "https://www.owensound.ca/", ["Grey County"]),
    ("City of Kenora Operations and Infrastructure", "Kenora", "https://www.kenora.ca/", ["Northwestern Ontario"]),
    ("City of Dryden Public Works", "Dryden", "https://www.dryden.ca/", ["Northwestern Ontario"]),
    ("City of Pembroke Operations Department", "Pembroke", "https://www.pembroke.ca/", ["Renfrew County"]),
    ("County of Prince Edward Public Works", "Picton", "https://www.thecounty.ca/", ["Prince Edward County"]),
    ("City of Kawartha Lakes Public Works", "Kawartha Lakes", "https://www.kawarthalakes.ca/", ["Kawartha Lakes"]),
]

UTILITIES_ENERGY = [
    ("Alectra Utilities Corporation", "Mississauga", "https://alectrautilities.com/"),
    ("Algoma Power Inc.", "Fort Erie", "https://algomapower.com/"),
    ("Atikokan Hydro Inc.", "Atikokan", "https://www.athydro.com/"),
    ("Bluewater Power Distribution Corporation", "Sarnia", "https://bluewaterpower.com/"),
    ("Burlington Hydro Inc.", "Burlington", "https://www.burlingtonhydro.com/"),
    ("Canadian Niagara Power Inc.", "Fort Erie", "https://www.cnpower.com/"),
    ("Centre Wellington Hydro Ltd.", "Fergus", "https://www.cwhydro.ca/"),
    ("Cooperative Hydro Embrun Inc.", "Embrun", "https://www.hydroembrun.ca/"),
    ("Cornwall Electric", "Cornwall", "https://www.cornwallelectric.com/"),
    ("E.L.K. Energy Inc.", "Essex", "https://www.elkenergy.com/"),
    ("Elexicon Energy Inc.", "Ajax", "https://elexiconenergy.com/"),
    ("Enova Power Corp.", "Kitchener", "https://enovapower.com/"),
    ("Entegrus Powerlines Inc.", "Chatham", "https://www.entegrus.com/"),
    ("ENWIN Utilities Ltd.", "Windsor", "https://www.enwin.com/"),
    ("EPCOR Electricity Distribution Ontario Inc.", "Collingwood", "https://www.epcor.com/"),
    ("ERTH Power Corporation", "Ingersoll", "https://www.erthpower.com/"),
    ("Essex Powerlines Corporation", "Oldcastle", "https://essexpowerlines.ca/"),
    ("Festival Hydro Inc.", "Stratford", "https://festivalhydro.com/"),
    ("Fort Frances Power Corporation", "Fort Frances", "https://ffpc.ca/"),
    ("GrandBridge Energy Inc.", "Cambridge", "https://grandbridgeenergy.com/"),
    ("Greater Sudbury Hydro Inc.", "Sudbury", "https://gsuinc.ca/"),
    ("Grimsby Power Incorporated", "Grimsby", "https://www.grimsbypower.com/"),
    ("Halton Hills Hydro Inc.", "Acton", "https://www.haltonhillshydro.com/"),
    ("Hearst Power Distribution Company Limited", "Hearst", "https://hearstpower.com/"),
    ("Hydro 2000 Inc.", "Alfred", "https://hydro2000.ca/"),
    ("Hydro Hawkesbury Inc.", "Hawkesbury", "https://hydrohawkesbury.ca/"),
    ("Hydro One Networks Inc.", "Toronto", "https://www.hydroone.com/"),
    ("Hydro Ottawa Limited", "Ottawa", "https://hydroottawa.com/"),
    ("InnPower Corporation", "Innisfil", "https://innpower.ca/"),
    ("Kingston Hydro Corporation", "Kingston", "https://utilitieskingston.com/"),
    ("Lakefront Utilities Inc.", "Cobourg", "https://www.lakefrontutilities.com/"),
    ("Lakeland Power Distribution Ltd.", "Huntsville", "https://www.lakelandpower.on.ca/"),
    ("London Hydro Inc.", "London", "https://www.londonhydro.com/"),
    ("Milton Hydro Distribution Inc.", "Milton", "https://www.miltonhydro.com/"),
    ("Newmarket-Tay Power Distribution Ltd.", "Newmarket", "https://ntpower.ca/"),
    ("Niagara Peninsula Energy Inc.", "Niagara Falls", "https://www.npei.ca/"),
    ("North Bay Hydro Distribution Limited", "North Bay", "https://www.northbayhydro.com/"),
    ("Northern Ontario Wires Inc.", "Cochrane", "https://nowinc.ca/"),
    ("Oakville Hydro Electricity Distribution Inc.", "Oakville", "https://www.oakvillehydro.com/"),
    ("Orangeville Hydro Limited", "Orangeville", "https://orangevillehydro.on.ca/"),
    ("Oshawa Power", "Oshawa", "https://www.oshawapower.ca/"),
    ("Ottawa River Power Corporation", "Pembroke", "https://orpowercorp.com/"),
    ("PUC Distribution Inc.", "Sault Ste. Marie", "https://ssmpuc.com/"),
    ("Renfrew Hydro Inc.", "Renfrew", "https://renfrewhydro.com/"),
    ("Rideau St. Lawrence Distribution Inc.", "Prescott", "https://rslu.ca/"),
    ("Sioux Lookout Hydro Inc.", "Sioux Lookout", "https://www.siouxlookouthydro.com/"),
    ("Synergy North Corporation", "Thunder Bay", "https://synergynorth.ca/"),
    ("Tillsonburg Hydro Inc.", "Tillsonburg", "https://www.tillsonburg.ca/"),
    ("Toronto Hydro-Electric System Limited", "Toronto", "https://www.torontohydro.com/"),
    ("Wasaga Distribution Inc.", "Wasaga Beach", "https://wasagadist.ca/"),
    ("Wellington North Power Inc.", "Mount Forest", "https://www.wellingtonnorthpower.com/"),
    ("Westario Power Inc.", "Walkerton", "https://www.westario.com/"),
]

AGGREGATES_MATERIALS = [
    ("A.L. Blair Construction Co. Ltd.", "Moose Creek", "https://www.alblairconstruction.com"),
    ("Alder Creek Aggregates", "Kitchener", "https://www.aldercreekaggregates.com"),
    ("Amrize Canada Inc.", "Concord", "https://www.amrize.com"),
    ("Arriscraft International Inc.", "Cambridge", "https://www.arriscraft.com"),
    ("B.R. Fulton Construction Ltd.", "Renfrew", "https://www.brfulton.com"),
    ("Beamish Construction Inc.", "Sudbury", "https://www.beamishconstruction.com"),
    ("Blythe Dale Sand & Gravel", "Blyth", "https://www.blythedale.ca"),
    ("Bot Aggregates Limited", "Oakville", "https://botconstruction.ca"),
    ("Brampton Brick Limited", "Brampton", "https://www.bramptonbrick.com"),
    ("Brent Quarries", "Port Carling", "https://www.brentquarry.com"),
    ("Brock Aggregates Inc.", "Concord", "https://www.brockaggregates.com"),
    ("Buckhorn Sand and Gravel", "Buckhorn", "https://www.buckhornsandgravel.com"),
    ("Cambridge Aggregates Inc.", "Cambridge", "https://www.heidelbergmaterials.com"),
    ("Capital Paving Inc.", "Guelph", "https://www.capitalpaving.net"),
    ("CBM Aggregates", "Toronto", "https://www.stmaryscement.com"),
    ("Cliftondale Construction Co.", "Hawkesbury", "https://www.cliftondale.ca"),
    ("Coloured Aggregates Inc.", "Toronto", "https://www.colouredaggregates.com"),
    ("Cornwall Gravel Company Limited", "Cornwall", "https://www.cornwallgravel.ca"),
    ("Cox Construction Limited", "Guelph", "https://www.coxconstruction.ca"),
    ("D & J Lockhart Excavators Ltd.", "Guelph", "https://www.djlockhart.com"),
    ("Dufferin Aggregates", "Oakville", "https://www.dufferinaggregates.com"),
    ("Draglam Salt", "Concord", "https://www.draglamsalt.com"),
    ("Ed Seguin & Sons Trucking and Paving Ltd.", "St. Isidore", "https://www.edseguinandsons.com"),
    ("Eisses Brothers Excavating", "Barrie", "https://www.eissesexcavating.com"),
    ("Ethier Sand and Gravel Ltd.", "Sudbury", "https://www.ethiersandandgravel.ca"),
    ("Fisher Wavy Inc.", "Sudbury", "https://www.fisherwavy.com"),
    ("G. Tackaberry & Sons Construction Company Limited", "Athens", "https://www.tackaberryconstruction.com"),
    ("Georgian Aggregates and Construction Inc.", "Collingwood", "https://www.georgianaggregates.ca"),
    ("Grant Aggregate", "Sudbury", "https://www.grantaggregate.com"),
    ("Harold Sutherland Construction Ltd.", "Kemble", "https://haroldsutherlandconstruction.com"),
    ("Heidelberg Materials Canada Limited", "Burlington", "https://www.heidelbergmaterials.com"),
    ("James Dick Construction Limited", "Bolton", "https://www.jamesdick.com"),
    ("Jennison Construction Ltd.", "Leamington", "https://www.jennisonconstruction.com"),
    ("K.J. Beamish Construction Co. Limited", "Sudbury", "https://www.kjbeamish.com"),
    ("Lafarge Canada Inc.", "Mississauga", "https://www.lafarge.ca"),
    ("Miller Aggregates", "Markham", "https://www.millergroup.ca"),
    ("Nelson Aggregate Co.", "Burlington", "https://www.nelsonaggregate.com"),
    ("Pakenham Sand & Gravel", "Pakenham", "https://www.pakenhamsandandgravel.ca"),
    ("R.W. Tomlinson Limited", "Ottawa", "https://tomlinsongroup.com"),
    ("Sarjeant Co. Ltd.", "Barrie", "https://sarjeants.com"),
    ("Seeley and Arnill Construction", "Collingwood", "https://seeleyandarnill.com"),
    ("Strada Aggregates", "Woodbridge", "https://www.stradaaggregates.com"),
    ("Walker Aggregates Inc.", "Niagara Falls", "https://www.walkerind.com"),
    ("Wendell Farquhar Trucking", "Huntsville", "https://farquhartrucking.ca"),
    ("Dufferin Concrete", "Oakville", "https://www.dufferinconcrete.ca"),
    ("Thomas Cavanagh Construction Limited", "Ashton", "https://www.thomascavanagh.ca"),
    ("Greenwood Aggregates Limited", "Orangeville", "https://greenwoodaggregates.com"),
    ("L. Walter & Sons Excavating Ltd.", "Waterloo", "https://www.lwalterandsons.ca"),
    ("Priestly Demolition Inc.", "King", "https://www.priestly.ca"),
    ("Toffanello & Sons Aggregates Ltd.", "Sudbury", "https://toffanello.com"),
    ("Villeneuve Construction Co. Ltd.", "Hearst", "https://villeneuve.on.ca"),
    ("W.D. Laflamme Limited", "Sudbury", "https://www.wdlaflamme.ca"),
]

DEVELOPER_PROPERTY = [
    ("Minto Communities", "Ottawa", "https://www.minto.com"),
    ("Mattamy Homes", "Toronto", "https://mattamyhomes.com"),
    ("Tridel", "Toronto", "https://www.tridel.com"),
    ("The Daniels Corporation", "Toronto", "https://danielshomes.ca"),
    ("Menkes Developments", "Toronto", "https://www.menkes.com"),
    ("Great Gulf", "Toronto", "https://greatgulf.com"),
    ("Broccolini", "Toronto", "https://broccolini.com"),
    ("Dream Unlimited", "Toronto", "https://dream.ca"),
    ("RioCan REIT", "Toronto", "https://www.riocan.com"),
    ("Choice Properties REIT", "Toronto", "https://www.choicereit.ca"),
    ("SmartCentres REIT", "Vaughan", "https://www.smartcentres.com"),
    ("First Capital REIT", "Toronto", "https://fcr.ca"),
    ("Allied Properties REIT", "Toronto", "https://www.alliedreit.com"),
    ("Cadillac Fairview", "Toronto", "https://www.cadillacfairview.com"),
    ("Oxford Properties", "Toronto", "https://www.oxfordproperties.com"),
    ("BGO", "Toronto", "https://www.bgo.com"),
    ("QuadReal Property Group", "Toronto", "https://www.quadreal.com"),
    ("GWL Realty Advisors", "Toronto", "https://www.gwlrealtyadvisors.com"),
    ("KingSett Capital", "Toronto", "https://www.kingsettcapital.com"),
    ("Canderel", "Toronto", "https://www.canderel.com"),
    ("Morguard", "Mississauga", "https://www.morguard.com"),
    ("Hazelview Properties", "Toronto", "https://www.hazelviewproperties.com"),
    ("CAPREIT", "Toronto", "https://www.capreit.ca"),
    ("Starlight Investments", "Toronto", "https://www.starlightinvest.com"),
    ("Greenwin", "Toronto", "https://www.greenwin.ca"),
    ("Pemberton Group", "Toronto", "https://www.pembertongroup.com"),
    ("Times Group Corporation", "Markham", "https://timesgroupcorp.com"),
    ("The Remington Group", "Vaughan", "https://www.remingtongroupinc.com"),
    ("Tribute Communities", "Pickering", "https://www.tributecommunities.com"),
    ("Empire Communities", "Vaughan", "https://www.empirecommunities.com"),
    ("Fieldgate Homes", "Markham", "https://www.fieldgatehomes.com"),
    ("Cachet Homes", "Mississauga", "https://www.cachethomes.com"),
    ("Brookfield Residential Ontario", "Toronto", "https://www.brookfieldresidential.com"),
    ("Aspen Ridge Homes", "Vaughan", "https://www.aspenridgehomes.com"),
    ("Geranium", "Markham", "https://www.geranium.com"),
    ("Fusion Homes", "Guelph", "https://www.fusionhomes.com"),
    ("Reid's Heritage Homes", "Cambridge", "https://www.reidsheritagehomes.com"),
    ("Granite Homes", "Guelph", "https://granitehomes.ca"),
    ("Losani Homes", "Hamilton", "https://www.losanihomes.com"),
    ("Marlin Spring", "Toronto", "https://marlinspring.com"),
    ("Plaza", "Toronto", "https://www.pureplaza.com"),
    ("CentreCourt", "Toronto", "https://centrecourt.com"),
    ("Alterra", "Toronto", "https://alterra.com"),
    ("TAS", "Toronto", "https://tasimpact.ca"),
    ("Devron", "Toronto", "https://devron.com"),
    ("Collecdev", "Toronto", "https://collecdev.com"),
    ("Altree Developments", "Toronto", "https://www.altreedevelopments.com"),
    ("Fitzrovia", "Toronto", "https://fitzrovia.ca"),
    ("Hullmark", "Toronto", "https://www.hullmark.ca"),
    ("Freed Developments", "Toronto", "https://freeddevelopments.com"),
    ("Urban Capital", "Toronto", "https://www.urbancapital.ca"),
    ("Starlane Home Corporation", "Vaughan", "https://www.starlanehomes.com"),
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
    candidates: list[dict[str, object]] = []
    candidates.extend(lead("Municipal/Public Works", name, city, website, SOURCES["municipal"], regions) for name, city, website, regions in MUNICIPAL_PUBLIC_WORKS)
    candidates.extend(lead("Utilities/Energy", name, city, website, SOURCES["utilities"]) for name, city, website in UTILITIES_ENERGY)
    candidates.extend(lead("Aggregates/Materials", name, city, website, SOURCES["aggregates"]) for name, city, website in AGGREGATES_MATERIALS)
    candidates.extend(lead("Developer/Property", name, city, website, SOURCES["bild"]) for name, city, website in DEVELOPER_PROPERTY)

    added = []
    skipped = []
    for item in candidates:
        if item["company_name"].casefold() in existing_names:
            skipped.append(item["company_name"])
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

    by_type: dict[str, int] = {}
    for item in added:
        by_type[str(item["company_type"])] = by_type.get(str(item["company_type"]), 0) + 1
    print(f"Added {len(added)} Wave 3 leads. Total leads: {len(leads)}")
    for category, count in sorted(by_type.items()):
        print(f"{category}: +{count}")
    if skipped:
        print(f"Skipped duplicates: {', '.join(skipped)}")


if __name__ == "__main__":
    main()
