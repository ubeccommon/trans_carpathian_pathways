"""Build the bilingual A4 co-creator agreement (English, then Ukrainian).

One command, from anywhere:

    python3 build/build_agreement.py

It renders the emblem (logo.py) for the cover, then reads
docs/agreement/Trans-Carpathian_Pathways_Co-Creator_Agreement_{EN,UK}.md
and writes
docs/agreement/Trans-Carpathian_Pathways_Co-Creator_Agreement_EN-UK.pdf.
The page styles are the proposal's (build_pdf.CSS), so the proposal,
the manual and the agreement read as one set. While the agreement is
a draft, the cover and every page footer say so; the version comes
from the English text's front matter. The HTML it renders from is
left in build/agreement.html for inspection and is not tracked.

Needs what build_pdf.py needs: pandoc on the PATH, the Inter and
Lora fonts installed, and requirements.txt.

SPDX-License-Identifier: AGPL-3.0-or-later

Changelog:
  v0.1 — 2026-10-08 — initial (Michel's word: the agreement in
         Ukrainian as well, one PDF in both languages).
"""
import re
import subprocess
from pathlib import Path

from weasyprint import HTML

import logo
from build_pdf import CSS

ROOT = Path(__file__).resolve().parent.parent
AGR = ROOT / "docs" / "agreement"
STEM = "Trans-Carpathian_Pathways_Co-Creator_Agreement"
OUT = AGR / f"{STEM}_EN-UK.pdf"
HTML_OUT = ROOT / "build" / "agreement.html"
LOGO = "../proposal/assets/logo.png"     # the project's emblem, cropped to its circle

LANGS = [
    {"code": "en", "md": f"{STEM}_EN.md", "label": "English",
     "footer": "Trans-Carpathian Pathways — Co-Creator Agreement",
     "draft": "Draft {v}"},
    {"code": "uk", "md": f"{STEM}_UK.md", "label": "Українська",
     "footer": "Транскарпатські стежки — угода співтворців",
     "draft": "Проєкт {v}"},
]

# What the agreement adds to the proposal's styles: sub-headings,
# long tables that may break between rows, room to write on the
# sign-on sheet, and the draft notice.
EXTRA_CSS = """
h3 { font-family: Lora; font-weight: 600; font-size: 11.5pt; color: #161a33;
     margin: 5mm 0 1.5mm; page-break-after: avoid; }
table { page-break-inside: auto; }
tr { page-break-inside: avoid; }
h2, h3, h2 + p, h3 + p { page-break-after: avoid; }
td.blank { height: 9mm; }
h3.sheet { page-break-before: always; margin-top: 0; }
ul.task-list { list-style: none; padding-left: 7mm; }
ul.task-list li { margin-bottom: 2.4mm; }
ul.task-list + p { margin-top: 10mm; }
span.box { display: inline-block; width: 3.4mm; height: 3.4mm; margin: 0 2.4mm 0 -6.4mm;
           border: .8pt solid #23252b; vertical-align: -.5mm; }
.cover .logo { width: 92mm; margin-top: 30mm; }
.cover .draft { margin-top: 6mm; font-size: 9pt; font-weight: 600;
                letter-spacing: .04em; color: #9a362b; }
"""


def version():
    text = (AGR / LANGS[0]["md"]).read_text(encoding="utf-8")
    return re.search(r'^version:\s*"([^"]+)"', text, flags=re.M).group(1)


def section(lang, v):
    text = (AGR / lang["md"]).read_text(encoding="utf-8")
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
    # A table whose header cells are all empty has no header.
    html = re.sub(r"<thead>\s*<tr[^>]*>\s*(<th[^>]*>\s*</th>\s*)+</tr>\s*</thead>", "", html)
    # An empty cell is a place to write by hand.
    html = re.sub(r"<td>\s*</td>", '<td class="blank"></td>', html)
    # A tick box is drawn to be ticked by hand, not as a form control,
    # and the sign-on sheet starts a page of its own.
    html = html.replace('<input type="checkbox" />', '<span class="box"></span>')
    html = re.sub(r'<h3 id="[^"]*">(Sign-on sheet|Аркуш приєднання)</h3>',
                  r'<h3 class="sheet">\1</h3>', html)
    footer = f"{lang['footer']} · {lang['draft'].format(v=v)}"
    return f"""
<section class="lang" id="{lang['code']}" lang="{lang['code']}">
  <div class="footer-text">{footer}</div>
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
    v = version()
    cover = f"""
<section class="cover">
  <img class="logo" src="{LOGO}" alt="Trans-Carpathian Pathways">
  <h1>Co-Creator Agreement</h1>
  <h1 class="uk">Угода співтворців</h1>
  <p class="tag">What we promise each other while we build the pathway together</p>
  <p class="tag">Що ми обіцяємо одне одному, будуючи стежку разом</p>
  <div class="rule"></div>
  <p class="meta">Trans-Carpathian Pathways · Транскарпатські стежки</p>
  <p class="meta">October 2026 · Жовтень 2026 · UBEC / Carpathian Hub Initiative</p>
  <p class="draft">Draft {v} — for discussion, not yet for signing<br>Проєкт {v} — для обговорення, ще не для підписання</p>
  <p class="toc"><a href="#en">English</a><span>·</span><a href="#uk">Українська</a></p>
</section>"""
    doc = ('<!doctype html><html><head><meta charset="utf-8">'
           '<meta name="author" content="Michel Garand">'
           '<title>Co-Creator Agreement — Угода співтворців</title>'
           f'<style>{CSS}{EXTRA_CSS}</style></head><body>{cover}'
           + "".join(section(l, v) for l in LANGS) + "</body></html>")
    HTML_OUT.write_text(doc, encoding="utf-8")
    HTML(string=doc, base_url=str(AGR)).write_pdf(OUT)
    print("wrote", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
