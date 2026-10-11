"""Build the bilingual A4 white paper (English, then Ukrainian).

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
  v0.4 — 2026-10-11 — German and Polish (Michel's word): one PDF per
         translation, Trans-Carpathian_Pathways_White_Paper_{DE,PL}.pdf, its
         cover and footers in its own language, and under its title the
         line that it is a translation not yet read by a speaker of the
         language. The EN-UK PDF is unchanged. The diagrams are drawn in
         all four languages.
  v0.3 — 2026-10-09 — the document says its language: lang="en" on the root,
         lang="uk" on the Ukrainian cover lines (BCP 47; Michel's word).
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

# The translations: one PDF each (Michel's word, October 11, 2026).
TRANSLATIONS = [
    {"code": "de", "md": f"{STEM}_DE.md", "label": "Deutsch",
     "footer": "Trans-Carpathian Pathways — Weißbuch", "draft": "Entwurf {v}",
     "cover": "Weißbuch",
     "tag": "Ein lebendiges Netz aus Gastgebenden, Pfaden und Kuratorinnen und Kuratoren "
            "entlang des Karpatenbogens – Begründung, Belege und Entwurf",
     "meta": "Oktober 2026 · UBEC / Karpaten-Hub-Initiative",
     "for": "Entwurf {v} – zur Diskussion",
     "note": "Übersetzung der englischen Fassung durch Claude; noch von niemandem "
             "mit Deutsch als Muttersprache gelesen."},
    {"code": "pl", "md": f"{STEM}_PL.md", "label": "Polski",
     "footer": "Trans-Carpathian Pathways — biała księga", "draft": "wersja robocza {v}",
     "cover": "Biała księga",
     "tag": "Żywa sieć gospodarzy, ścieżek i kuratorów wzdłuż łuku Karpat – argumenty, dowody i koncepcja",
     "meta": "Październik 2026 · UBEC / Inicjatywa Karpackiego Hubu",
     "for": "Wersja robocza {v} – do dyskusji",
     "note": "Tłumaczenie angielskiej wersji wykonane przez Claude; nie czytał go jeszcze "
             "nikt, dla kogo polski jest językiem ojczystym."},
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
    note = f'<p class="byline note">{lang["note"]}</p>' if lang.get("note") else ""
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
      {note}
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
  <h1 class="uk" lang="uk">Біла книга</h1>
  <p class="tag">A living network of hosts, paths and Curators across the Carpathian arc — the case, the evidence and the design</p>
  <p class="tag" lang="uk">Жива мережа господарів, стежок і кураторів через усю Карпатську дугу — підстави, свідчення та задум</p>
  <div class="rule"></div>
  <p class="meta">Trans-Carpathian Pathways · Транскарпатські стежки</p>
  <p class="meta">October 2026 · Жовтень 2026 · UBEC / Carpathian Hub Initiative</p>
  <p class="draft">Draft {v} — for discussion<br><span lang="uk">Проєкт {v} — для обговорення</span></p>
  <p class="toc">{toc}</p>
</section>"""
    doc = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
           '<meta name="author" content="Michel Garand">'
           '<title>Trans-Carpathian Pathways — White Paper</title>'
           f'<style>{CSS}{EXTRA_CSS}{WP_CSS}</style></head><body>{cover}'
           + "".join(section(l, v) for l in langs) + "</body></html>")
    HTML_OUT.write_text(doc, encoding="utf-8")
    HTML(string=doc, base_url=str(WP)).write_pdf(OUT)
    print("wrote", OUT.relative_to(ROOT))
    for t in TRANSLATIONS:
        if (WP / t["md"]).exists():
            translation(t, v)


def translation(t, v):
    """One translation, one PDF, its cover and footers in its own language."""
    cover = f"""
<section class="cover">
  <img class="logo" src="{LOGO}" alt="Trans-Carpathian Pathways">
  <h1>{t["cover"]}</h1>
  <p class="tag">{t["tag"]}</p>
  <div class="rule"></div>
  <p class="meta">Trans-Carpathian Pathways</p>
  <p class="meta">{t["meta"]}</p>
  <p class="draft">{t["for"].format(v=v)}</p>
  <p class="meta note">{t["note"]}</p>
</section>"""
    doc = (f'<!doctype html><html lang="{t["code"]}"><head><meta charset="utf-8">'
           '<meta name="author" content="Michel Garand">'
           f'<title>Trans-Carpathian Pathways — {t["cover"]}</title>'
           f'<style>{CSS}{EXTRA_CSS}{WP_CSS} .cover .note {{ margin: 8mm 32mm 0; line-height: 1.5; color: #5d5a52; }}</style></head><body>{cover}{section(t, v)}</body></html>')
    out = WP / t["md"].replace(".md", ".pdf")
    HTML(string=doc, base_url=str(WP)).write_pdf(out)
    print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
