"""Build the bilingual A4 user manual (English, then Ukrainian) for Plai.

One command, from anywhere:

    python3 build/build_manual.py

It renders the Plai emblem (logo.py) for the cover, then reads
docs/manual/Plai_User_Manual_{EN,UK}.md and writes
docs/manual/Plai_User_Manual_EN-UK.pdf. The page styles are the
proposal's (build_pdf.CSS), so the two documents read as one set.
The HTML it renders from is left in build/manual.html for inspection
and is not tracked.

Needs what build_pdf.py needs: pandoc on the PATH, the Inter and
Lora fonts installed, and requirements.txt.

SPDX-License-Identifier: AGPL-3.0-or-later

Changelog:
  v0.2 — 2026-10-08 — screenshots: figure styles; images from
         docs/manual/img/, referenced by the texts.
  v0.1 — 2026-10-08 — initial (Michel's word: a user manual for
         entrants and curators, bilingual, Plai's emblem on the
         cover).
"""
import re
import subprocess
from pathlib import Path

from weasyprint import HTML

import logo
from build_pdf import CSS

ROOT = Path(__file__).resolve().parent.parent
MAN = ROOT / "docs" / "manual"
OUT = MAN / "Plai_User_Manual_EN-UK.pdf"
HTML_OUT = ROOT / "build" / "manual.html"
LOGO = "../proposal/assets/logo.png"     # the Plai emblem, cropped to its circle

LANGS = [
    {"code": "en", "md": "Plai_User_Manual_EN.md", "label": "English",
     "footer": "Plai — User Manual"},
    {"code": "uk", "md": "Plai_User_Manual_UK.md", "label": "Українська",
     "footer": "Плай — посібник користувача"},
]

# What the manual adds to the proposal's styles: sub-headings, and
# quoted screen labels kept on one line where they can be.
EXTRA_CSS = """
h3 { font-family: Lora; font-weight: 600; font-size: 11.5pt; color: #161a33;
     margin: 5mm 0 1.5mm; page-break-after: avoid; }
td:first-child { width: 36%; }
/* Long tables may break between rows, so a heading is not left
   alone at the foot of a page with its table on the next. */
table { page-break-inside: auto; }
tr { page-break-inside: avoid; }
h2, h3, h2 + p, h3 + p { page-break-after: avoid; }
.cover .logo { width: 92mm; margin-top: 34mm; }
/* Screenshots: full width for whole pages, narrower for a panel or
   a form, never split across a page. */
figure.shot { margin: 3mm 0 4mm; page-break-inside: avoid; text-align: center; }
figure.shot img { width: 100%; border: 0.3mm solid #d8d2c0; border-radius: 1.2mm; }
figure.half img { width: 74%; }
figure.narrow img { width: 48%; }
figure.shot figcaption { font-size: 8.5pt; color: #5d5a52; margin-top: 1.5mm;
                         text-align: left; }
"""


def section(lang):
    text = (MAN / lang["md"]).read_text(encoding="utf-8")
    # Front matter (version, changelog) is for the record, not the page.
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)
    lines = text.splitlines()
    title = next(l[2:] for l in lines if l.startswith("# "))
    subtitle = next(l.strip("*") for l in lines if l.startswith("*") and not l.startswith("**"))
    byline = next(l for l in lines if "UBEC /" in l)
    body = "\n".join(lines[next(i for i, l in enumerate(lines) if l.startswith("## ")):])
    html = subprocess.run(
        ["pandoc", "-f", "markdown-implicit_figures", "-t", "html5"],
        input=body, capture_output=True, text=True, check=True).stdout
    html = re.sub(r"<colgroup>.*?</colgroup>", "", html, flags=re.S)
    return f"""
<section class="lang" id="{lang['code']}" lang="{lang['code']}">
  <div class="footer-text">{lang['footer']}</div>
  <header class="opener">
    <img class="mark" src="{LOGO}" alt="">
    <div>
      <p class="lang-label">{lang['label']}</p>
      <h1>{title}</h1>
      <p class="subtitle">{subtitle}</p>
      <p class="byline">{byline}</p>
    </div>
  </header>
  {html}
</section>"""


def main():
    logo.main()
    cover = f"""
<section class="cover">
  <img class="logo" src="{LOGO}" alt="Plai">
  <h1>Plai — User Manual</h1>
  <h1 class="uk">Плай — посібник користувача</h1>
  <p class="tag">Entering places on the Carpathian map, and publishing them</p>
  <p class="tag">Як позначати місця на карпатській мапі та оприлюднювати їх</p>
  <div class="rule"></div>
  <p class="meta">For entrants and curators · Для авторів записів і кураторів</p>
  <p class="meta">October 2026 · Жовтень 2026 · UBEC / Carpathian Hub Initiative</p>
  <p class="toc"><a href="#en">English</a><span>·</span><a href="#uk">Українська</a></p>
</section>"""
    doc = ('<!doctype html><html><head><meta charset="utf-8">'
           '<meta name="author" content="Michel Garand">'
           '<title>Plai — User Manual — Плай — посібник користувача</title>'
           f'<style>{CSS}{EXTRA_CSS}</style></head><body>{cover}'
           + "".join(section(l) for l in LANGS) + "</body></html>")
    HTML_OUT.write_text(doc, encoding="utf-8")
    HTML(string=doc, base_url=str(MAN)).write_pdf(OUT)
    print("wrote", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
