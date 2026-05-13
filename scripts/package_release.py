#!/usr/bin/env python3
"""Build a clean downloadable ZIP for GitHub releases."""

from __future__ import annotations

import argparse
import zipfile
from pathlib import Path


EXCLUDE_PARTS = {
    ".git",
    ".serena",
    ".pytest_cache",
    ".venv",
    ".venv-eval",
    ".venv-rebuild",
    "__pycache__",
    "dist",
    "output",
    "node_modules",
}


def should_include(path: Path) -> bool:
    return not any(part in EXCLUDE_PARTS for part in path.parts)


def build_zip(root: Path, output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(root.rglob("*")):
            rel = path.relative_to(root)
            if path.is_file() and should_include(rel):
                zf.write(path, rel.as_posix())
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="Package release ZIP.")
    parser.add_argument("--version", required=True, help="Release version or tag")
    parser.add_argument("--output-dir", default="dist")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    version = args.version.lstrip("v")
    output = Path(args.output_dir) / f"executive-market-research-v{version}.zip"
    build_zip(root, output)
    print(f"✓ Release ZIP written: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
