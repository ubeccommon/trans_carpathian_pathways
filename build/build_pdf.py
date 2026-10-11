"""Build the bilingual A4 PDF (English, then Ukrainian) from the two markdown files.

One command, from anywhere:

    python3 build/build_pdf.py

It renders the logo (logo.py) and redraws the diagrams (diagrams.py)
first, then reads
docs/proposal/Trans-Carpathian_Pathways_Proposal_{EN,UK}.md and writes
docs/proposal/Trans-Carpathian_Pathways_Proposal_EN-UK.pdf. The HTML it
renders from is left in build/proposal.html for inspection and is not
tracked.

Needs pandoc on the PATH, the Inter and Lora fonts installed, and
requirements.txt.

SPDX-License-Identifier: AGPL-3.0-or-later

Changelog:
  v0.5 — 2026-10-11 — German and Polish (Michel's word): one PDF per
         translation, Trans-Carpathian_Pathways_Proposal_{DE,PL}.pdf, its
         cover in its own language, and under its title the line that it
         is a translation not yet read by a speaker of the language. The
         EN-UK PDF is unchanged. The diagrams are drawn in all four
         languages.
  v0.4 — 2026-10-09 — the document says its language: lang="en" on the root,
         lang="uk" on the Ukrainian cover lines (BCP 47; Michel's word).
  v0.3 — 2026-10-07 — skips each text's YAML front matter (version and
         changelog), which the PDF does not print.
  v0.2 — 2026-10-07 — moved into the repository: reads and writes
         docs/proposal/, renders the logo and draws the diagrams
         first.
  v0.1 — 2026-10-07 — initial, in the Claude Project.
"""
import re
import subprocess
from pathlib import Path

from weasyprint import HTML

import diagrams
import logo

ROOT = Path(__file__).resolve().parent.parent
PROP = ROOT / "docs" / "proposal"
OUT = PROP / "Trans-Carpathian_Pathways_Proposal_EN-UK.pdf"
HTML_OUT = ROOT / "build" / "proposal.html"

LANGS = [
    {"code": "en", "md": "Trans-Carpathian_Pathways_Proposal_EN.md",
     "label": "English", "footer": "Trans-Carpathian Pathways — Project summary and proposal"},
    {"code": "uk", "md": "Trans-Carpathian_Pathways_Proposal_UK.md",
     "label": "Українська", "footer": "Транскарпатські стежки — опис проєкту та пропозиція"},
]

# The translations: one PDF each, in one language (Michel's word, October 11,
# 2026). Each says, under its title, that it is a translation nobody whose
# language it is has read yet.
TRANSLATIONS = [
    {"code": "de", "md": "Trans-Carpathian_Pathways_Proposal_DE.md", "label": "Deutsch",
     "footer": "Trans-Carpathian Pathways — Projektvorschlag",
     "tag": "Ein lebendiges Netz aus Ort, Menschen und Pfad",
     "kind": "Projektvorschlag",
     "meta": "Oktober 2026 · UBEC / Karpaten-Hub-Initiative",
     "note": "Übersetzung der englischen Fassung durch Claude; noch von niemandem "
             "mit Deutsch als Muttersprache gelesen."},
    {"code": "pl", "md": "Trans-Carpathian_Pathways_Proposal_PL.md", "label": "Polski",
     "footer": "Trans-Carpathian Pathways — propozycja projektu",
     "tag": "Żywa sieć miejsc, ludzi i ścieżek",
     "kind": "Propozycja projektu",
     "meta": "Październik 2026 · UBEC / Inicjatywa Karpackiego Hubu",
     "note": "Tłumaczenie angielskiej wersji wykonane przez Claude; nie czytał go jeszcze "
             "nikt, dla kogo polski jest językiem ojczystym."},
]
SUMMARY = ("Summary", "Коротко", "Zusammenfassung", "Streszczenie")


def section(lang):
    text = (PROP / lang["md"]).read_text(encoding="utf-8")
    # Front matter (version, changelog) is for the record, not the page.
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)
    lines = text.splitlines()
    # Front matter of each file: logo, title, subtitle, byline — the PDF sets these itself.
    title = next(l[2:] for l in lines if l.startswith("# "))
    subtitle = next(l.strip("*") for l in lines if l.startswith("*") and not l.startswith("**"))
    byline = next(l for l in lines if "UBEC /" in l)
    body = "\n".join(lines[next(i for i, l in enumerate(lines) if l.startswith("## ")):])
    html = subprocess.run(
        ["pandoc", "-f", "markdown-implicit_figures", "-t", "html5"],
        input=body, capture_output=True, text=True, check=True).stdout
    # Column widths come from the stylesheet, not from pandoc.
    html = re.sub(r"<colgroup>.*?</colgroup>", "", html, flags=re.S)
    # A table whose header cells are all empty has no header.
    html = re.sub(r"<thead>\s*<tr[^>]*>\s*(<th[^>]*>\s*</th>\s*)+</tr>\s*</thead>", "", html)
    html = html.replace("<table>", '<table class="kv">', 1) if any(w in body[:24] for w in SUMMARY) else html
    note = f'<p class="byline note">{lang["note"]}</p>' if lang.get("note") else ""
    return f"""
<section class="lang" id="{lang['code']}" lang="{lang['code']}">
  <div class="footer-text">{lang['footer']}</div>
  <header class="opener">
    <img class="mark" src="assets/logo.png" alt="">
    <div>
      <p class="lang-label">{lang['label']}</p>
      <h1>{title}</h1>
      <p class="subtitle">{subtitle}</p>
      <p class="byline">{byline}</p>
      {note}
    </div>
  </header>
  {html}
</section>"""


CSS = """
@page {
  size: A4;
  margin: 20mm 19mm 22mm 19mm;
  @bottom-left { content: string(footer); font: 400 7.5pt Inter; color: #8a8474; }
  @bottom-right { content: counter(page); font: 600 7.5pt Inter; color: #8a8474; }
}
@page cover { margin: 0; @bottom-left { content: none } @bottom-right { content: none } }

html { font-family: Inter; font-size: 9.6pt; line-height: 1.5; color: #23252b; }
body { margin: 0; }

/* cover */
.cover { page: cover; height: 297mm; background: #fff; color: #23252b;
         display: flex; flex-direction: column; align-items: center; text-align: center; }
.cover .logo { width: 104mm; margin-top: 30mm; }
.cover h1 { font-family: Lora; font-weight: 600; font-size: 30pt; line-height: 1.15;
            margin: 14mm 0 0; color: #161a33; }
.cover h1.uk { font-size: 24pt; margin-top: 3mm; color: #9a362b; }
.cover .tag { font-family: Lora; font-style: italic; font-size: 11.5pt; margin: 6mm 22mm 0; color: #3a3a35; }
.cover .tag + .tag { margin-top: 1.5mm; color: #5d5a52; }
.cover .rule { width: 24mm; height: 1.2pt; background: #c98a2e; margin: 10mm auto 6mm; }
.cover .meta { font-size: 9pt; letter-spacing: .04em; color: #3a3a35; }
.cover .toc { margin-top: 5mm; font-size: 9pt; color: #5d5a52; }
.cover .toc a { color: #161a33; font-weight: 600; text-decoration: none; }
.cover .toc a::after { content: " — " target-counter(attr(href), page); color: #5d5a52; font-weight: 400; }
.cover .toc span { margin: 0 4mm; }

/* language sections */
.lang { page-break-before: always; }
.footer-text { string-set: footer content(); height: 0; overflow: hidden; font-size: 0; line-height: 0; }
.opener { display: flex; align-items: center; gap: 7mm; padding-bottom: 6mm;
          border-bottom: 1.2pt solid #c98a2e; margin-bottom: 7mm; }
.opener .mark { width: 30mm; height: 30mm; flex: none; }
.lang-label { font-size: 7.5pt; letter-spacing: .14em; text-transform: uppercase;
              color: #9a362b; font-weight: 600; margin: 0 0 1.5mm; }
.opener h1 { font-family: Lora; font-weight: 600; font-size: 22pt; line-height: 1.15;
             color: #161a33; margin: 0; }
.subtitle { font-family: Lora; font-style: italic; font-size: 10.5pt; color: #4a4a44; margin: 2mm 0 0; }
.byline { font-size: 8pt; color: #8a8474; margin: 1.5mm 0 0; }

h2 { font-family: Lora; font-weight: 600; font-size: 14.5pt; color: #161a33;
     margin: 8mm 0 2.5mm; page-break-after: avoid; }
h2::before { content: ""; display: block; width: 10mm; height: 1.2pt; background: #c98a2e;
             margin-bottom: 2.5mm; }
p { margin: 0 0 2.6mm; orphans: 3; widows: 3; }
strong { font-weight: 600; color: #161a33; }
ul, ol { margin: 0 0 3mm; padding-left: 5.5mm; }
li { margin-bottom: 1.2mm; }
ul li::marker { color: #c98a2e; }
ol li::marker { color: #9a362b; font-weight: 600; }

table { width: 100%; border-collapse: collapse; margin: 1.5mm 0 4.5mm; font-size: 8.9pt;
        page-break-inside: avoid; }
th { text-align: left; font-weight: 600; color: #161a33;
     padding: 1.8mm 2.5mm; border-bottom: 1pt solid #c98a2e; }
td { padding: 1.7mm 2.5mm; border-bottom: .5pt solid #e3ddd0; vertical-align: top; }
td:first-child { font-weight: 600; color: #161a33; width: 32%; }
table.kv { border-top: 1pt solid #c98a2e; }
table.kv td:first-child { width: 22%; }

p > img:only-child { display: block; width: 86%; margin: 3mm auto 2mm; }
p:has(> img) { page-break-inside: avoid; }
em { color: #4a4a44; }
"""


def main():
    logo.main()
    diagrams.main()
    en_title = "Trans-Carpathian Pathways"
    uk_title = "Транскарпатські стежки"
    cover = f"""
<section class="cover">
  <img class="logo" src="assets/logo.png" alt="Trans-Carpathian Pathways">
  <h1>{en_title}</h1>
  <h1 class="uk" lang="uk">{uk_title}</h1>
  <p class="tag">A living network of place, people and path</p>
  <p class="tag" lang="uk">Жива мережа місць, людей і стежок</p>
  <div class="rule"></div>
  <p class="meta">Project summary and proposal · Опис проєкту та пропозиція</p>
  <p class="meta">October 2026 · Жовтень 2026 · UBEC / Carpathian Hub Initiative</p>
  <p class="toc"><a href="#en">English</a><span>·</span><a href="#uk">Українська</a></p>
</section>"""
    doc = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="author" content="Michel Garand"><title>{en_title} — {uk_title}</title>'
           f'<style>{CSS}</style></head><body>{cover}'
           + "".join(section(l) for l in LANGS) + "</body></html>")
    HTML_OUT.write_text(doc, encoding="utf-8")
    HTML(string=doc, base_url=str(PROP)).write_pdf(OUT)
    print("wrote", OUT.relative_to(ROOT))
    for t in TRANSLATIONS:
        if (PROP / t["md"]).exists():
            translation(t)


def translation(t):
    """One translation, one PDF, its cover in its own language."""
    cover = f"""
<section class="cover">
  <img class="logo" src="assets/logo.png" alt="Trans-Carpathian Pathways">
  <h1>Trans-Carpathian Pathways</h1>
  <p class="tag">{t["tag"]}</p>
  <div class="rule"></div>
  <p class="meta">{t["kind"]}</p>
  <p class="meta">{t["meta"]}</p>
  <p class="meta note">{t["note"]}</p>
</section>"""
    doc = (f'<!doctype html><html lang="{t["code"]}"><head><meta charset="utf-8">'
           f'<meta name="author" content="Michel Garand"><title>Trans-Carpathian Pathways — {t["kind"]}</title>'
           f'<style>{CSS} .cover .note {{ margin: 8mm 32mm 0; line-height: 1.5; color: #5d5a52; }}</style></head><body>{cover}{section(t)}</body></html>')
    out = PROP / t["md"].replace(".md", ".pdf")
    HTML(string=doc, base_url=str(PROP)).write_pdf(out)
    print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
