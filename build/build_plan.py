"""Build the bilingual A4 implementation plan (English, then Ukrainian).

One command, from anywhere:

    python3 build/build_plan.py

It renders the emblem (logo.py) for the cover, reads the latest
docs/IMPLEMENTATION_PLAN_v0_N.md and docs/IMPLEMENTATION_PLAN_UK_v0_N.md
and writes docs/IMPLEMENTATION_PLAN_EN-UK.pdf. The page styles are the
proposal's (build_pdf.CSS) with the agreement's additions, so the plan
reads as one set with the proposal, the manual, the agreement and the
white paper. The three states of a to-do — ☑ done, ◐ in progress,
☐ to do — are set in DejaVu Sans, which has the glyphs, and coloured
moss, ochre and ink. The version comes from the English text's front
matter; the HTML it renders from is left in build/plan.html for
inspection and is not tracked.

Needs what build_pdf.py needs: pandoc on the PATH, the Inter and
Lora fonts installed, DejaVu Sans, and requirements.txt.

SPDX-License-Identifier: AGPL-3.0-or-later

Changelog:
  v0.1 — 2026-10-10 — initial (Michel's word: a Ukrainian version of
         the implementation plan and a PDF in both languages).
"""
import re
import subprocess
from pathlib import Path

from weasyprint import HTML

import logo
from build_agreement import EXTRA_CSS
from build_pdf import CSS

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
OUT = DOCS / "IMPLEMENTATION_PLAN_EN-UK.pdf"
HTML_OUT = ROOT / "build" / "plan.html"
LOGO = "proposal/assets/logo.png"

LANGS = [
    {"code": "en", "glob": "IMPLEMENTATION_PLAN_v0_*.md", "label": "English",
     "title": "Implementation Plan",
     "byline": "October 2026 · UBEC / Carpathian Hub Initiative",
     "footer": "Trans-Carpathian Pathways — Implementation Plan",
     "draft": "Working plan {v}"},
    {"code": "uk", "glob": "IMPLEMENTATION_PLAN_UK_v0_*.md", "label": "Українська",
     "title": "План впровадження",
     "byline": "Жовтень 2026 · UBEC / Ініціатива Карпатського хабу",
     "footer": "Транскарпатські стежки — план впровадження",
     "draft": "Робочий план {v}"},
]

STATES = {"☑": ("done", "#5b7a4a"), "◐": ("doing", "#c98a2e"), "☐": ("todo", "#23252b")}

PLAN_CSS = """
td:first-child { width: 11%; }
table.dates td:first-child { width: 24%; }
span.st { font-family: "DejaVu Sans"; font-size: 9pt; margin-right: 1mm; }
""" + "".join(f"span.st.{n} {{ color: {c}; }}\n" for n, c in STATES.values())


def latest(pattern):
    return sorted(DOCS.glob(pattern),
                  key=lambda p: [int(x) for x in re.findall(r"\d+", p.stem)])[-1]


def version(path):
    text = path.read_text(encoding="utf-8")
    return re.search(r'^version:\s*"([^"]+)"', text, flags=re.M).group(1)


def section(lang, v):
    path = latest(lang["glob"])
    text = path.read_text(encoding="utf-8")
    fm = re.match(r"\A---\n(.*?)\n---\n", text, flags=re.S).group(1)
    subtitle = re.search(r'^subtitle:\s*"([^"]+)"', fm, flags=re.M).group(1)
    body = text[len(fm) + 8:]
    # The changelog is for the record, not the page.
    body = re.sub(r"\n\* \* \*\n\n\*(Changelog|Журнал змін)\*\n.*\Z", "\n", body, flags=re.S)
    # pandoc 3.1 turns a leading ☐ into a form checkbox whatever the
    # extensions say, so the three glyphs cross it as placeholders.
    for glyph, (name, _) in STATES.items():
        body = body.replace(glyph, f"STATEGLYPH{name.upper()}")
    html = subprocess.run(
        ["pandoc", "-f", "markdown-implicit_figures", "-t", "html5"],
        input=body, capture_output=True, text=True, check=True).stdout
    html = re.sub(r"<colgroup>.*?</colgroup>", "", html, flags=re.S)
    # The dates table is the one whose first header is a date.
    html = re.sub(r"<table>(?=\s*<thead>\s*<tr[^>]*>\s*<th[^>]*>(Date|Дата)<)",
                  '<table class="dates">', html)
    for glyph, (name, _) in STATES.items():
        html = html.replace(f"STATEGLYPH{name.upper()}", f'<span class="st {name}">{glyph}</span>')
    footer = f"{lang['footer']} · {lang['draft'].format(v=v)}"
    return f"""
<section class="lang" id="{lang['code']}" lang="{lang['code']}">
  <div class="footer-text">{footer}</div>
  <header class="opener">
    <img class="mark" src="{LOGO}" alt="">
    <div>
      <p class="lang-label">{lang['label']}</p>
      <h1>{lang['title']}</h1>
      <p class="subtitle">{subtitle}</p>
      <p class="byline">{lang['byline']}</p>
    </div>
  </header>
  {html}
</section>"""


def main():
    logo.main()
    v = version(latest(LANGS[0]["glob"]))
    toc = '<span>·</span>'.join(f'<a href="#{l["code"]}">{l["label"]}</a>' for l in LANGS)
    cover = f"""
<section class="cover">
  <img class="logo" src="{LOGO}" alt="Trans-Carpathian Pathways">
  <h1>Implementation Plan</h1>
  <h1 class="uk" lang="uk">План впровадження</h1>
  <p class="tag">The project in one page, and the step-by-step plan to the first corridor walked — with its to-do lists</p>
  <p class="tag" lang="uk">Проєкт на одній сторінці та покроковий план до першого пройденого коридору — зі списками справ</p>
  <div class="rule"></div>
  <p class="meta">Trans-Carpathian Pathways · Транскарпатські стежки</p>
  <p class="meta">October 2026 · Жовтень 2026 · UBEC / Carpathian Hub Initiative</p>
  <p class="draft">Working plan {v} — states as of October 10, 2026<br><span lang="uk">Робочий план {v} — стан на 10 жовтня 2026 року</span></p>
  <p class="toc">{toc}</p>
</section>"""
    doc = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
           '<meta name="author" content="Michel Garand">'
           '<title>Trans-Carpathian Pathways — Implementation Plan</title>'
           f'<style>{CSS}{EXTRA_CSS}{PLAN_CSS}</style></head><body>{cover}'
           + "".join(section(l, v) for l in LANGS) + "</body></html>")
    HTML_OUT.write_text(doc, encoding="utf-8")
    HTML(string=doc, base_url=str(DOCS)).write_pdf(OUT)
    print("wrote", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
