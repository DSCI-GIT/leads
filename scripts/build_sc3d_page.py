#!/usr/bin/env python3
"""Build sc3d.html from the lead workspace shell and SC3D data."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
SC3D_HTML = ROOT / "sc3d.html"
SC3D_DATA = ROOT / "sc3d_leads.json"

SC3D_TEMPLATES = {
    "space-sales": {
        "name": "Space sales / walkthrough buyer",
        "subjects": [
            "Photorealistic 3D walkthroughs for {{company_name}}",
            "A hosted digital twin for your spaces",
            "Help prospects walk the space before they visit",
        ],
        "body": "Hello {{contact_name}},\n\nI am reaching out from SplatCap3D. We create photorealistic, walkable 3D digital twins of real spaces using Gaussian splat capture and hosted browser viewers.\n\n{{personalization_line}}\n\nFor teams selling or presenting spaces, the practical value is simple: prospects can explore the environment remotely, understand scale and flow, and share the experience with decision makers without booking another site visit. The same capture can also support web embeds, short teaser clips, annotations and internal review.\n\nWould it be useful to look at one location where an interactive 3D walkthrough could help your sales, leasing or stakeholder process?\n\nRegards,\n{{sender_name}}\nSplatCap3D\n{{sender_contact}}",
    },
    "aec-progress": {
        "name": "AEC / construction progress",
        "subjects": [
            "3D progress capture for active sites",
            "A browser-based site twin for stakeholder review",
            "Photorealistic construction documentation",
        ],
        "body": "Hello {{contact_name}},\n\nSplatCap3D builds photorealistic 3D twins of sites and facilities so teams can review spaces remotely in a browser.\n\n{{personalization_line}}\n\nThis is different from traditional drone mapping: the goal is an explorable visual record that stakeholders can walk through, annotate, measure and compare over time. It is useful for interiors, exteriors, model suites, fit-outs, facilities and repeat progress captures where photos or 360 tours do not carry enough spatial context.\n\nCould we compare one upcoming project or property where a lightweight digital twin would reduce site visits or improve review quality?\n\nRegards,\n{{sender_name}}\nSplatCap3D\n{{sender_contact}}",
    },
    "training": {
        "name": "Operations / training twin",
        "subjects": [
            "3D facility walkthroughs for training and orientation",
            "A digital twin for operational context",
            "Reduce repeat site visits with a hosted 3D space",
        ],
        "body": "Hello {{contact_name}},\n\nI am contacting you from SplatCap3D. We capture real spaces as photorealistic 3D digital twins that can be opened in a browser and shared with teams.\n\n{{personalization_line}}\n\nFor complex facilities, venues or operational spaces, a digital twin can support orientation, training, remote review and documentation without sending every stakeholder back to site. The result is more spatially useful than a photo set and easier to distribute than a specialist 3D model.\n\nWould you be open to a short call to identify one space where a browser-based walkthrough could help training, planning or stakeholder alignment?\n\nRegards,\n{{sender_name}}\nSplatCap3D\n{{sender_contact}}",
    },
}


def replace_block(html: str, script_id: str, payload: object) -> str:
    data = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    pattern = re.compile(
        rf'(<script id="{re.escape(script_id)}" type="application/json">)(.*?)(</script>)',
        flags=re.DOTALL,
    )
    updated, count = pattern.subn(lambda match: match.group(1) + data + match.group(3), html, count=1)
    if count != 1:
        raise RuntimeError(f"Could not replace {script_id}")
    return updated


def main() -> None:
    html = INDEX.read_text(encoding="utf-8")
    leads = json.loads(SC3D_DATA.read_text(encoding="utf-8"))

    html = replace_block(html, "embeddedData", leads)
    html = replace_block(html, "templateData", SC3D_TEMPLATES)

    replacements = {
        "Drone Services Canada Inc. Ontario engineering lead intelligence workspace.": "SplatCap3D 3D digital twin lead intelligence workspace.",
        "<title>DSCI Lead Intelligence</title>": "<title>SplatCap3D Lead Intelligence</title>",
        '<div class="brand"><div class="brand-mark">DS</div><div><h1>Lead Intelligence</h1><small>Drone Services Canada Inc. Â· Ontario engineering market</small></div></div>': '<div class="brand"><div class="brand-mark">SC3D</div><div><h1>Lead Intelligence</h1><small>SplatCap3D Â· 3D digital twin market</small></div></div>',
        '<a class="btn dark" href="sc3d.html">SC3D</a>': '<a class="btn dark" href="index.html">DS</a>',
        "Research snapshot: July 19, 2026. Pipeline stages, notes, sender settings and saved views stay in this browserâ€™s local storage.": "SC3D snapshot: July 21, 2026. Pipeline stages, notes, sender settings and saved views stay separate from the DS workspace.",
        "const embedded=JSON.parse($('#embeddedData').textContent); const templates=JSON.parse($('#templateData').textContent);": "const embedded=JSON.parse($('#embeddedData').textContent); const templates=JSON.parse($('#templateData').textContent);",
        "dsci_viewMode": "sc3d_viewMode",
        "dsci_updates": "sc3d_updates",
        "dsci_savedViews": "sc3d_savedViews",
        "dsci_sender": "sc3d_sender",
        "Drone Services Canada Inc.": "SplatCap3D",
        "leads.json": "sc3d_leads.json",
        "dsci-leads-filtered.csv": "sc3d-leads-filtered.csv",
        "dsci-leads-full.csv": "sc3d-leads-full.csv",
        "dsci-lead-local-updates.json": "sc3d-lead-local-updates.json",
        "dsci-lead-updates-v1": "sc3d-lead-updates-v1",
        "Primary services are NOT CONFIRMED; no service claim was inserted.": "SC3D fit signals are NOT CONFIRMED; no service claim was inserted.",
        "Your public service profile identifies": "Your public profile suggests a space-driven use case around",
    }
    for old, new in replacements.items():
        html = html.replace(old, new)

    html = re.sub(
        r":root\{[^}]+\}",
        ":root{--navy:#111827;--navy2:#312e81;--ink:#14151f;--muted:#687083;--line:#dddaf0;--bg:#f6f4ff;--card:#fff;--cyan:#7c3aed;--cyan2:#5b21b6;--orange:#14b8a6;--danger:#bd3d42;--warn:#8a5a10;--success:#23734d;--shadow:0 10px 30px rgba(49,46,129,.14);--radius:14px}",
        html,
        count=1,
    )
    html = html.replace(
        "background:linear-gradient(110deg,var(--navy),var(--navy2));color:#fff;border-bottom:4px solid var(--cyan);box-shadow:0 5px 24px rgba(0,0,0,.22)",
        "background:linear-gradient(110deg,#111827 0%,#312e81 58%,#5b21b6 100%);color:#fff;border-bottom:4px solid var(--cyan);box-shadow:0 5px 24px rgba(49,46,129,.24)",
    )
    html = html.replace(
        "background:rgba(255,255,255,.08)}.brand h1",
        "background:rgba(124,58,237,.22)}.brand h1",
    )
    html = re.sub(
        r'<div class="brand"><div class="brand-mark">.*?</div><div><h1>Lead Intelligence</h1><small>.*?</small></div></div>',
        '<div class="brand"><div class="brand-mark">SC3D</div><div><h1>Lead Intelligence</h1><small>SplatCap3D · 3D digital twin market</small></div></div>',
        html,
        count=1,
        flags=re.DOTALL,
    )
    html = html.replace(".brand-mark{width:42px;", ".brand-mark{width:58px;")
    html = html.replace("placeholder=\"Eric Papky\"", "placeholder=\"Your name\"")
    html = html.replace(
        "Position corridor mapping, site modelling and inspection support around the firmâ€™s",
        "Position photorealistic 3D walkthroughs and hosted digital twins around the account's",
    )

    SC3D_HTML.write_text(html, encoding="utf-8", newline="\n")
    print(f"Built {SC3D_HTML.name} with {len(leads)} embedded SC3D leads")


if __name__ == "__main__":
    main()
