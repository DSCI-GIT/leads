#!/usr/bin/env python3
"""Synchronize datasets into the offline fallbacks embedded in HTML pages."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    (ROOT / "leads.json", ROOT / "index.html"),
    (ROOT / "leads.json", ROOT / "404.html"),
    (ROOT / "sc3d_leads.json", ROOT / "sc3d.html"),
]
PATTERN = re.compile(
    r'(<script id="embeddedData" type="application/json">)(.*?)(</script>)',
    flags=re.DOTALL,
)


def main() -> None:
    for data_path, target in TARGETS:
        if not target.exists() or not data_path.exists():
            continue
        data = json.loads(data_path.read_text(encoding="utf-8"))
        embedded = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
        # Prevent a company string from accidentally closing the script element.
        embedded = embedded.replace("</", "<\\/")
        html = target.read_text(encoding="utf-8")
        updated, count = PATTERN.subn(r"\1" + embedded + r"\3", html, count=1)
        if count != 1:
            raise RuntimeError(f"Could not locate embeddedData block in {target}")
        target.write_text(updated, encoding="utf-8", newline="\n")
        print(f"Updated {target.name} from {data_path.name}")


if __name__ == "__main__":
    main()
