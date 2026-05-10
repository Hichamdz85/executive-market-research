#!/usr/bin/env python3
"""
Asset fetcher — pulls country flag + section divider stock images.

Uses:
- flagcdn.com  for country flags (free, no API key)
- Unsplash Source URLs (free, ~1080p, no auth required)

Usage:
    python fetch_assets.py --country dz --output ./examples/assets/

The output directory is then referenced in the engagement JSON's
divider_images dict.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
from pathlib import Path

DIVIDER_QUERIES = {
    "methodology": "containers,cargo,port",
    "country":     "{country},landmark,city",
    "exec":        "boardroom,meeting,office",
    "market":      "marketplace,industry,commerce",
    "imports":     "shipping,port,cargo",
    "regulatory":  "documents,signing,law",
    "competitive": "skyline,buildings,corporate",
    "conclusion":  "handshake,partnership,deal",
    "appendix":    "books,library,archive",
}


def download(url: str, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "executive-market-research/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp, open(target, "wb") as fh:
        fh.write(resp.read())


def fetch_flag(country_iso2: str, out: Path) -> Path:
    iso = country_iso2.lower()
    target = out / f"flag_{iso}.svg"
    download(f"https://flagcdn.com/{iso}.svg", target)
    return target


def fetch_dividers(country_name: str, out: Path) -> dict[str, str]:
    """Fetch one stock photo per section.

    Note: Unsplash Source has been deprecated for some endpoints. As a fallback
    we use picsum.photos with a deterministic seed per section so callers
    always get *some* image even when offline.
    """
    out.mkdir(parents=True, exist_ok=True)
    paths: dict[str, str] = {}
    for section, query in DIVIDER_QUERIES.items():
        q = query.replace("{country}", country_name)
        target = out / f"divider_{section}.jpg"
        # Try a few sources in order
        candidates = [
            f"https://source.unsplash.com/1600x900/?{q.replace(',', '%2C')}",
            f"https://picsum.photos/seed/{section}-{country_name.lower()}/1600/900",
        ]
        for url in candidates:
            try:
                download(url, target)
                paths[section] = str(target.relative_to(out.parent))
                break
            except Exception as e:  # noqa: BLE001
                print(f"  ! {section}: {url} failed ({e})")
        if section not in paths:
            print(f"  ✗ {section}: all sources failed; leave blank")
    return paths


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--country-iso2", required=True, help="ISO 3166-1 alpha-2 code (e.g. dz, sa, fr)")
    parser.add_argument("--country-name", required=True, help="Display name (e.g. Algeria)")
    parser.add_argument("--output", default="./examples/assets", help="Output directory")
    args = parser.parse_args()

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    print(f"→ Fetching flag ({args.country_iso2})...")
    flag = fetch_flag(args.country_iso2, out)
    print(f"  ✓ {flag}")

    print(f"→ Fetching divider images for {args.country_name}...")
    dividers = fetch_dividers(args.country_name, out)
    for k, v in dividers.items():
        print(f"  ✓ {k}: {v}")

    summary = {
        "flag": str(flag.relative_to(out.parent)),
        "dividers": dividers,
    }
    summary_path = out / "_assets_manifest.json"
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    print(f"→ Manifest: {summary_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
