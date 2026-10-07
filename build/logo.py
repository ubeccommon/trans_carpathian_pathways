"""Render docs/proposal/assets/logo.png from the emblem SVG, cropped to its circle.

The emblem (plai_emblem_mark.svg) is drawn on an 800 x 800 canvas with
its outer ring a circle of radius 300 about (400, 400); everything outside
that circle is empty. Cropping is a change of viewBox to the circle's
bounding square, so nothing in the drawing is touched. The PNG is
transparent outside the circle.

Run on its own, or through build_pdf.py, which runs it first.

SPDX-License-Identifier: AGPL-3.0-or-later

Changelog:
  v0.1 — 2026-10-07 — initial.
"""
import re
from pathlib import Path

import cairosvg

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "docs" / "proposal" / "assets"
SOURCE = ASSETS / "plai_emblem_mark.svg"
OUT = ASSETS / "logo.png"

CX, CY, R = 400, 400, 300          # the outer ring, from the SVG itself
SIZE = 1200                        # pixels a side: 104 mm on the cover at about 290 dpi


def main():
    svg = SOURCE.read_text(encoding="utf-8")
    ring = f'<circle cx="{CX}" cy="{CY}" r="{R}"'
    if ring not in svg:
        raise SystemExit(f"{SOURCE.name}: outer ring {ring}/> not found; crop by hand")
    box = f'viewBox="{CX - R} {CY - R} {2 * R} {2 * R}" width="{2 * R}" height="{2 * R}"'
    svg, n = re.subn(r'viewBox="[^"]*" width="[^"]*" height="[^"]*"', box, svg, count=1)
    if n != 1:
        raise SystemExit(f"{SOURCE.name}: no viewBox, width and height to replace")
    cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=str(OUT),
                     output_width=SIZE, output_height=SIZE)
    print("wrote", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
