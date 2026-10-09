"""Place the site's fonts in site/static/fonts/ from their upstream releases.

Run once, by hand, when a font is updated — not by build_site.py, which
only copies what this tool left in the tree. The site serves every font
itself (no Google Fonts, no other server), so the files are committed.

    python3 build/site_fonts.py INTER_ZIP LORA_CHECKOUT

INTER_ZIP      Inter's release archive, e.g. Inter-4.1.zip from
               https://github.com/rsms/inter/releases
LORA_CHECKOUT  a clone of https://github.com/cyrealtype/Lora-Cyrillic

What it does, and nothing more:
- Inter: copies web/Inter-{Regular,Italic,SemiBold}.woff2 unchanged, and
  LICENSE.txt as OFL-Inter.txt.
- Lora: re-encodes fonts/variable/Lora[wght].ttf and Lora-Italic[wght].ttf
  as WOFF2 — the same font data, no glyph removed or changed — and copies
  OFL.txt as OFL-Lora.txt. Lora has the Reserved Font Name "Lora", so it
  is deliberately not subset; a subset would be a Modified Version under
  the OFL and could not keep the name.
- Writes SOURCES.txt beside them: each file, where it came from, and its
  SHA-256.

Needs fontTools and brotli (pip install fonttools brotli); neither is in
requirements.txt, since the site build does not need them.

SPDX-License-Identifier: AGPL-3.0-or-later

Changelog:
  v0.1 — 2026-10-09 — initial (the landing page at tcp.ubec.network).
"""
import hashlib
import io
import subprocess
import sys
import zipfile
from pathlib import Path

from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "site" / "static" / "fonts"

INTER = ["Inter-Regular.woff2", "Inter-Italic.woff2", "Inter-SemiBold.woff2"]
LORA = {"Lora[wght].ttf": "Lora-Variable.woff2",
        "Lora-Italic[wght].ttf": "Lora-Italic-Variable.woff2"}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main(inter_zip: str, lora_dir: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    lines = []
    zip_name = Path(inter_zip).name
    with zipfile.ZipFile(inter_zip) as z:
        for name in INTER:
            (OUT / name).write_bytes(z.read(f"web/{name}"))
            lines.append(f"{name}\t{zip_name}:web/{name}, unchanged")
        (OUT / "OFL-Inter.txt").write_bytes(z.read("LICENSE.txt"))
        lines.append(f"OFL-Inter.txt\t{zip_name}:LICENSE.txt")

    lora = Path(lora_dir)
    commit = subprocess.run(["git", "-C", str(lora), "rev-parse", "--short", "HEAD"],
                            capture_output=True, text=True).stdout.strip() or "unknown"
    for src, dst in LORA.items():
        font = TTFont(str(lora / "fonts" / "variable" / src))
        font.flavor = "woff2"
        font.save(str(OUT / dst))
        lines.append(f"{dst}\tLora-Cyrillic@{commit}:fonts/variable/{src}, re-encoded as WOFF2, not subset")
    (OUT / "OFL-Lora.txt").write_bytes((lora / "OFL.txt").read_bytes())
    lines.append(f"OFL-Lora.txt\tLora-Cyrillic@{commit}:OFL.txt")

    rows = []
    for line in lines:
        name, origin = line.split("\t")
        rows.append(f"{name}\n  from: {origin}\n  sha256: {sha(OUT / name)}")
    (OUT / "SOURCES.txt").write_text(
        "Fonts served by tcp.ubec.network, written by build/site_fonts.py.\n"
        "Inter and Lora are under the SIL Open Font License 1.1 (the OFL-*.txt files).\n\n"
        + "\n\n".join(rows) + "\n", encoding="utf-8")
    for p in sorted(OUT.iterdir()):
        print(f"{p.stat().st_size:>8}  {p.relative_to(ROOT)}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__.split("\n\n")[1])
    main(sys.argv[1], sys.argv[2])
