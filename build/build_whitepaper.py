"""Build the A4 white paper (English; Ukrainian joins when its text exists).

One command, from anywhere:

    python3 build/build_whitepaper.py

It renders the emblem (logo.py) for the cover and draws the three
diagrams (diagrams_whitepaper.py) into docs/whitepaper/assets/, then reads
docs/whitepaper/Trans-Carpathian_Pathways_White_Paper_{EN[,UK]}.md
and writes docs/whitepaper/Trans-Carpathian_Pathways_White_Paper.pdf.
The page styles are the proposal's (build_pdf.CSS) with the
agreement's additions for sub-headings and long tables, so the
proposal, the manual, the agreement and the white paper read as one
set. While the paper is a draft, the cover and every page footer say
so; the version comes from the English text's front matter. The HTML
it renders from is left in build/whitepaper.html for inspection and
is not tracked.

Needs what build_pdf.py needs: pandoc on the PATH, the Inter and
Lora fonts installed, and requirements.txt.

SPDX-License-Identifier: AGPL-3.0-or-later

Changelog:
  v0.2 — 2026-10-09 — draws the diagrams first.
  v0.1 — 2026-10-09 — initial (Michel's word: a white paper from a
         review of the documents and background research).
"""
import re
import subprocess
from pathlib import Path

from weasyprint import HTML

import diagrams_whitepaper
import logo
from build_agreement import EXTRA_CSS
from build_pdf import CSS

ROOT = Path(__file__).resolve().parent.parent
WP = ROOT / "docs" / "whitepaper"
STEM = "Trans-Carpathian_Pathways_White_Paper"
OUT = WP / f"{STEM}.pdf"
HTML_OUT = ROOT / "build" / "whitepaper.html"
LOGO = "../proposal/assets/logo.png"

LANGS = [
    {"code": "en", "md": f"{STEM}_EN.md", "label": "English",
     "footer": "Trans-Carpathian Pathways — White Paper",
     "draft": "Draft {v}"},
    {"code": "uk", "md": f"{STEM}_UK.md", "label": "Українська",
     "footer": "Транскарпатські стежки — біла книга",
     "draft": "Проєкт {v}"},
]

# What the white paper adds: numbered sources that may break across
# pages, and bracketed citations that should not break from their word.
WP_CSS = """
ol { padding-left: 6mm; }
ol li { margin-bottom: 1.2mm; }
h2#sources ~ ol li, h2#sources ~ p { font-size: 8.4pt; line-height: 1.4; word-break: break-all; }
h2#sources ~ ol li a { word-break: break-all; }
section.lang > p:first-of-type { margin-top: 0; }
"""


def version():
    text = (WP / LANGS[0]["md"]).read_text(encoding="utf-8")
    return re.search(r'^version:\s*"([^"]+)"', text, flags=re.M).group(1)


def section(lang, v):
    text = (WP / lang["md"]).read_text(encoding="utf-8")
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
    # WeasyPrint does not honour <ol start>; reset the counter by hand so
    # the sources keep counting across their sub-headings.
    html = re.sub(r'<ol start="(\d+)"',
                  lambda m: f'<ol start="{m[1]}" style="counter-reset: list-item {int(m[1]) - 1}"', html)
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
    diagrams_whitepaper.main()
    v = version()
    langs = [l for l in LANGS if (WP / l["md"]).exists()]
    toc = '<span>·</span>'.join(f'<a href="#{l["code"]}">{l["label"]}</a>' for l in langs)
    cover = f"""
<section class="cover">
  <img class="logo" src="{LOGO}" alt="Trans-Carpathian Pathways">
  <h1>White Paper</h1>
  <h1 class="uk">Біла книга</h1>
  <p class="tag">A living network of hosts, paths and Curators across the Carpathian arc — the case, the evidence and the design</p>
  <p class="tag">Жива мережа господарів, стежок і кураторів через усю Карпатську дугу — підстави, свідчення та задум</p>
  <div class="rule"></div>
  <p class="meta">Trans-Carpathian Pathways · Транскарпатські стежки</p>
  <p class="meta">October 2026 · Жовтень 2026 · UBEC / Carpathian Hub Initiative</p>
  <p class="draft">Draft {v} — for discussion<br>Проєкт {v} — для обговорення</p>
  <p class="toc">{toc}</p>
</section>"""
    doc = ('<!doctype html><html><head><meta charset="utf-8">'
           '<meta name="author" content="Michel Garand">'
           '<title>Trans-Carpathian Pathways — White Paper</title>'
           f'<style>{CSS}{EXTRA_CSS}{WP_CSS}</style></head><body>{cover}'
           + "".join(section(l, v) for l in langs) + "</body></html>")
    HTML_OUT.write_text(doc, encoding="utf-8")
    HTML(string=doc, base_url=str(WP)).write_pdf(OUT)
    print("wrote", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
