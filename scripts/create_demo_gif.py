#!/usr/bin/env python3
"""Create a small animated demo GIF for release assets."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def create_with_pillow(output: Path) -> None:
    from PIL import Image, ImageDraw, ImageFont  # type: ignore

    frames = []
    steps = [
        ("1", "Product + country"),
        ("2", "Research scaffold"),
        ("3", "HTML + PDF report"),
    ]
    for number, label in steps:
        img = Image.new("RGB", (960, 540), "#0B1220")
        draw = ImageDraw.Draw(img)
        try:
            title_font = ImageFont.truetype("Arial.ttf", 44)
            body_font = ImageFont.truetype("Arial.ttf", 30)
        except OSError:
            title_font = ImageFont.load_default()
            body_font = ImageFont.load_default()
        draw.rectangle((0, 0, 960, 540), fill="#0B1220")
        draw.rectangle((64, 64, 896, 476), outline="#C9A45A", width=3)
        draw.text((96, 116), "Executive Market Research", fill="#FFFFFF", font=title_font)
        draw.text((96, 196), f"Step {number}", fill="#C9A45A", font=body_font)
        draw.text((96, 252), label, fill="#E8EEF7", font=body_font)
        draw.text((96, 382), "Khelifi Consulting", fill="#8EA3BF", font=body_font)
        frames.append(img)
    frames[0].save(
        output,
        save_all=True,
        append_images=frames[1:],
        duration=900,
        loop=0,
        optimize=True,
    )


def create_fallback_gif(output: Path) -> None:
    # 1x1 transparent GIF. Used only when Pillow is unavailable.
    output.write_bytes(
        b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00"
        b"\xff\xff\xff!\xf9\x04\x01\x00\x00\x00\x00,"
        b"\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Create release demo GIF.")
    parser.add_argument("--output", default="dist/demo.gif")
    args = parser.parse_args()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        create_with_pillow(output)
    except Exception:  # noqa: BLE001
        create_fallback_gif(output)
    print(f"✓ Demo GIF written: {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
