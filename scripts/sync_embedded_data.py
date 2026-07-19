#!/usr/bin/env python3
"""Synchronize leads.json into the offline fallback embedded in index.html and 404.html."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "leads.json"
TARGETS = [ROOT / "index.html", ROOT / "404.html"]
PATTERN = re.compile(
    r'(<script id="embeddedData" type="application/json">)(.*?)(</script>)',
    flags=re.DOTALL,
)


def main() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    embedded = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    # Prevent a company string from accidentally closing the script element.
    embedded = embedded.replace("</", "<\\/")

    for target in TARGETS:
        html = target.read_text(encoding="utf-8")
        updated, count = PATTERN.subn(r"\1" + embedded + r"\3", html, count=1)
        if count != 1:
            raise RuntimeError(f"Could not locate embeddedData block in {target}")
        target.write_text(updated, encoding="utf-8", newline="\n")
        print(f"Updated {target.name}")


if __name__ == "__main__":
    main()
