"""Build, check and deploy the site at tcp.ubec.network.

One command rebuilds the whole site from the tree:

    python3 build/build_site.py            # build and check site/dist/
    python3 build/build_site.py check      # check site/dist/ as it is
    python3 build/build_site.py deploy HOST PATH
                                           # build, check, then rsync
                                           # site/dist/ to HOST:PATH
    python3 build/build_site.py verify ORIGIN
                                           # fetch the live site and
                                           # list every host it uses

It reads site/content/*.md (one file per page and language, a short
front matter of `key: value` lines, the body in pandoc Markdown), wraps
each in the page below, and writes site/dist/: the pages, style.css,
the fonts and the marks from site/static/, and the Plai emblem cropped
to its circle from docs/proposal/assets/plai_emblem_mark.svg.

It also builds one page per document and language from the documents
themselves (DOCS below): the latest version of each file in docs/, its
diagrams, and its committed PDF, copied as they are. The site never holds
a second copy of a document's words; a document changes in docs/ and the
site follows on the next build. Every page carries the same menu, above
the picture, with the chapters of the longer documents in a drop-down.
site/dist/ is not tracked; the host and the path are arguments, never in
the tree.

The check refuses a build in which any page or stylesheet loads anything
from another server, links to a file that is not there, or leaves an
element unclosed. The site's own pages link out only to the hosts in
LINKS_OUT and the paths in LINKS_OUT_PATHS; a page built from a document
may also link to the sources the document cites, over https. Nothing
links to a host's point on Plai. It also checks what WCAG 2.2 AA asks
that a build can check: a valid language tag on every page and part, one
h1 and no skipped heading level, alt on every picture, a name on every
link, a title, and the contrast of every colour pair in CONTRAST. What
only a person can check is listed in site/README.md.

Needs pandoc on the PATH, and Python 3 alone; deploy needs rsync and ssh.

SPDX-License-Identifier: AGPL-3.0-or-later

Changelog:
  v0.13 — 2026-10-11 — the field writing at soilandpeace.ubec.network
         (Michel's word), in the menu, the landing pages and the list of
         hosts a page may link to; pilgrims.ubec.network, another blog,
         no longer allowed.
  v0.12 — 2026-10-11 — the overview, the proposal and the white paper in
         German and Polish (Michel's word): their pages under /de/ and /pl/,
         each with its own PDF; a document's PDF chosen by its language; the
         EN tag left only where a document has no text in the page's
         language; Anhang and Załącznik take the appendix's id.
  v0.11 — 2026-10-11 — German and Polish (Michel's word): a landing page in
         each, the menu in each, the documents shown in English to both;
         the two-way switch replaced by a list of the four languages, each
         by its own name; hreflang for all four and x-default; a note on
         each German and Polish page that it is a translation not yet read
         by a speaker of the language. A document not in the page's
         language carries a small EN in the menu, and the words for a
         screen reader.
  v0.10 — 2026-10-11 — the field writing opens in a new tab too (Michel's
         word), as the map does.
  v0.9 — 2026-10-11 — the map opens in a new tab (Michel's word), with
         rel="noopener", an arrow, and "opens in a new tab" for a screen
         reader; the check refuses a new tab with an opener.
  v0.8 — 2026-10-11 — the overview second in the menu, in both languages,
         as the logical order (Michel's word): About, Overview, Proposal,
         White paper, Co-creator agreement, Plai, Field writing.
  v0.7 — 2026-10-11 — the map link opens the Pathways application on
         Plai, ubec_plai_hub_tcp, on the corridor around Verkhovyna
         (Michel's word); the check allows that application's path and
         the front page, nothing else on the map service.
  v0.6 — 2026-10-11 — the proposal before the white paper in the menu
         (Michel's word): About, Proposal, White paper, Co-creator
         agreement, Overview, Plai, Field writing.
  v0.5 — 2026-10-11 — a menu above the picture on every page (Michel's
         word): About, the white paper with its chapters, the proposal,
         the co-creator agreement with its parts and roles, the overview,
         Plai and the field writing. A page per document and language,
         built from the latest file in docs/, with its diagrams and PDF;
         the record on GitHub allowed as a link out, the repository being
         public (October 11); a document's own sources allowed as links.
  v0.4 — 2026-10-09 — WCAG 2.2 AA in the check (Michel's word): BCP 47
         language tags, one h1 and no skipped heading level, alt on every
         picture, a name on every link, a title, and the contrast of the
         stylesheet's colour pairs; the UBEC mark beside its name is alt="".
  v0.3 — 2026-10-09 — the name inside the picture's frame (Michel's word);
         ?v= on the stylesheet and the pictures, after a cached v0.1
         stylesheet left the picture unstyled.
  v0.2 — 2026-10-09 — Michel's picture "Warm wind on the path" in the
         head, in place of the drawn ridges.
  v0.1 — 2026-10-09 — initial: the landing page, English and Ukrainian.
"""
import hashlib
import html
import re
import shutil
import subprocess
import sys
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
CONTENT = SITE / "content"
STATIC = SITE / "static"
DIST = SITE / "dist"
EMBLEM = ROOT / "docs" / "proposal" / "assets" / "plai_emblem_mark.svg"

ORIGIN = "https://tcp.ubec.network"
RECORD = "https://github.com/ubeccommon/trans_carpathian_pathways"
LINKS_OUT = {"mapservice.ubec.network", "soilandpeace.ubec.network"}
# Hosts the site's own pages may link to only under one path: the record.
LINKS_OUT_PATHS = {"github.com": "/ubeccommon/trans_carpathian_pathways"}
MAILTO = {"stewardship@ubec.network"}
# The map: the Pathways application on Plai, opened on the first corridor
# around Verkhovyna (Michel's word, October 11, 2026).
MAP = "https://mapservice.ubec.network/application/ubec_plai_hub_tcp?#34377@24.81486/48.15413r0@EPSG:3857"
# The only paths on the map service a page may link to: its front page and
# the Pathways application. Never a point on it.
MAP_PATHS = {"", "/", "/application/ubec_plai_hub_tcp"}
# The field writing, Soil and Peace (Michel's word, October 11, 2026: its own
# address; pilgrims.ubec.network is another of his blogs).
WRITING = "https://soilandpeace.ubec.network/"

# The documents on the site, in the menu's order. `src` is a glob in docs/
# per language; the latest version wins. `toc` says which headings the
# menu lists: "h2" the chapters; "h2+roles" the parts and, under Part II,
# each role. A document with no file in a language is shown in English.
DOCS = [
    {"slug": "overview",
     "src": {"en": "overview/PROJECT_OVERVIEW_v*.md",
             "de": "overview/PROJECT_OVERVIEW_DE_v*.md",
             "pl": "overview/PROJECT_OVERVIEW_PL_v*.md"},
     "pdf": {},
     "label": {"en": "Overview", "uk": "Огляд", "de": "Überblick", "pl": "Przegląd"},
     "kind": {"en": "Project overview", "uk": "Огляд проєкту", "de": "Überblick über das Projekt",
              "pl": "Przegląd projektu"},
     "toc": None},
    {"slug": "proposal",
     "src": {"en": "proposal/Trans-Carpathian_Pathways_Proposal_EN.md",
             "uk": "proposal/Trans-Carpathian_Pathways_Proposal_UK.md",
             "de": "proposal/Trans-Carpathian_Pathways_Proposal_DE.md",
             "pl": "proposal/Trans-Carpathian_Pathways_Proposal_PL.md"},
     "pdf": {"en": ("proposal/Trans-Carpathian_Pathways_Proposal_EN-UK.pdf", "en-uk"), "uk": ("proposal/Trans-Carpathian_Pathways_Proposal_EN-UK.pdf", "en-uk"),
             "de": ("proposal/Trans-Carpathian_Pathways_Proposal_DE.pdf", "own"),
             "pl": ("proposal/Trans-Carpathian_Pathways_Proposal_PL.pdf", "own")},
     "label": {"en": "Proposal", "uk": "Пропозиція", "de": "Projektvorschlag", "pl": "Propozycja"},
     "kind": {"en": "Project summary and proposal", "uk": "Опис проєкту та пропозиція",
              "de": "Projektbeschreibung und Vorschlag", "pl": "Opis i propozycja projektu"},
     "toc": None},
    {"slug": "whitepaper",
     "src": {"en": "whitepaper/Trans-Carpathian_Pathways_White_Paper_EN.md",
             "uk": "whitepaper/Trans-Carpathian_Pathways_White_Paper_UK.md",
             "de": "whitepaper/Trans-Carpathian_Pathways_White_Paper_DE.md",
             "pl": "whitepaper/Trans-Carpathian_Pathways_White_Paper_PL.md"},
     "pdf": {"en": ("whitepaper/Trans-Carpathian_Pathways_White_Paper.pdf", "en-uk"), "uk": ("whitepaper/Trans-Carpathian_Pathways_White_Paper.pdf", "en-uk"),
             "de": ("whitepaper/Trans-Carpathian_Pathways_White_Paper_DE.pdf", "own"),
             "pl": ("whitepaper/Trans-Carpathian_Pathways_White_Paper_PL.pdf", "own")},
     "label": {"en": "White paper", "uk": "Біла книга", "de": "Weißbuch", "pl": "Biała księga"},
     "kind": {"en": "White paper", "uk": "Біла книга", "de": "Weißbuch", "pl": "Biała księga"},
     "toc": "h2"},
    {"slug": "agreement",
     "src": {"en": "agreement/Trans-Carpathian_Pathways_Co-Creator_Agreement_EN.md",
             "uk": "agreement/Trans-Carpathian_Pathways_Co-Creator_Agreement_UK.md"},
     "pdf": {"en": ("agreement/Trans-Carpathian_Pathways_Co-Creator_Agreement_EN-UK.pdf", "en-uk"), "uk": ("agreement/Trans-Carpathian_Pathways_Co-Creator_Agreement_EN-UK.pdf", "en-uk")},
     "label": {"en": "Co-creator agreement", "uk": "Угода співтворців",
               "de": "Mitgestaltungsvereinbarung", "pl": "Porozumienie współtwórców"},
     "kind": {"en": "Co-creator agreement", "uk": "Угода співтворців"},
     "toc": "h2+roles"},
]

WORDS = {
    "en": {"hub": "Carpathian Hub Initiative", "skip": "Skip to the text", "version": "Page",
           "nav": "Site", "about": "About", "map": "Map — Plai", "writing": "Field writing",
           "whole": "The whole text", "pdf": "PDF, English and Ukrainian", "table": "Table",
           "in_en": "", "doc_pdf": "Download the PDF (English and Ukrainian)",
           "built": "This page is the text of {file}, {version}, in the project's record",
           "record": "on GitHub", "licence": "Text CC BY-SA 4.0.", "contents": "Contents",
           "new_tab": " (opens in a new tab)", "language": "Language", "pdf_own": "PDF", "doc_pdf_own": "Download the PDF"},
    "uk": {"hub": "Ініціатива Карпатського хабу", "skip": "До тексту", "version": "Сторінка",
           "nav": "Сайт", "about": "Про проєкт", "map": "Мапа — Плай", "writing": "Польові записи",
           "whole": "Увесь текст", "pdf": "PDF, англійською та українською", "table": "Таблиця",
           "in_en": " (англійською)", "doc_pdf": "Завантажити PDF (англійською та українською)",
           "built": "Ця сторінка — текст файлу {file}, {version}, у записі проєкту",
           "record": "на GitHub", "licence": "Тексти — CC BY-SA 4.0.", "contents": "Зміст",
           "new_tab": " (відкривається в новій вкладці)", "language": "Мова", "pdf_own": "PDF", "doc_pdf_own": "Завантажити PDF"},
    "de": {"hub": "Karpaten-Hub-Initiative", "skip": "Zum Text", "version": "Seite",
           "nav": "Website", "about": "Über das Projekt", "map": "Karte – Plai", "writing": "Feldnotizen",
           "whole": "Der ganze Text", "pdf": "PDF, Englisch und Ukrainisch", "table": "Tabelle",
           "in_en": " (auf Englisch)", "doc_pdf": "PDF herunterladen (Englisch und Ukrainisch)",
           "built": "Diese Seite ist der Text von {file}, {version}, im Projektarchiv",
           "record": "auf GitHub", "licence": "Texte: CC BY-SA 4.0.", "contents": "Inhalt",
           "new_tab": " (öffnet in einem neuen Tab)", "language": "Sprache", "pdf_own": "PDF (Deutsch)", "doc_pdf_own": "PDF herunterladen"},
    "pl": {"hub": "Inicjatywa Karpackiego Hubu", "skip": "Przejdź do treści", "version": "Strona",
           "nav": "Witryna", "about": "O projekcie", "map": "Mapa – Plai", "writing": "Zapiski z terenu",
           "whole": "Cały tekst", "pdf": "PDF, po angielsku i ukraińsku", "table": "Tabela",
           "in_en": " (po angielsku)", "doc_pdf": "Pobierz PDF (po angielsku i ukraińsku)",
           "built": "Ta strona to tekst pliku {file}, {version}, w zapisie projektu",
           "record": "na GitHubie", "licence": "Teksty: CC BY-SA 4.0.", "contents": "Spis treści",
           "new_tab": " (otwiera się w nowej karcie)", "language": "Język", "pdf_own": "PDF (po polsku)", "doc_pdf_own": "Pobierz PDF"},
}

# The site's languages, in the order the language list shows them, each by its
# own name. English is the root; every other language lives under /<tag>/.
LANGS = ["en", "uk", "de", "pl"]
LANG_NAMES = {"en": "English", "uk": "Українська", "de": "Deutsch", "pl": "Polski"}
# Under the name in the picture, each page shows the name in one other language:
# English and Ukrainian show each other's; German and Polish show the Ukrainian,
# the corridor's own.
OTHER = {"en": "uk", "uk": "en", "de": "uk", "pl": "uk"}
# Until the Ukrainian has been read in the corridor (D-2, open), every
# Ukrainian page says so, in one line.
UK_NOTE = "Українських текстів ще не читали люди з коридору."
# The German and Polish pages are Claude's translations of the English (Michel's
# word, October 11, 2026, for German and Polish); until a speaker of each has
# read them, they say so, and say that the documents are in English and Ukrainian.
NOTES = {
    "uk": UK_NOTE,
    "de": "Diese Seiten sind aus dem Englischen übersetzt und noch nicht von Muttersprachlerinnen "
          "und Muttersprachlern geprüft. Die Mitgestaltungsvereinbarung gibt es bisher nur auf "
          "Englisch und Ukrainisch.",
    "pl": "Te strony są przetłumaczone z angielskiego i nie zostały jeszcze sprawdzone przez "
          "rodzimych użytkowników języka. Porozumienie współtwórców jest na razie dostępne tylko "
          "po angielsku i ukraińsku.",
}

# The landing page's picture is Michel's "Warm wind on the path" (day 70),
# static/assets/warm_wind_on_the_path.svg, 1600 x 900, with the name set
# in its sky, inside its frame. Its alt text is each page's `image_alt`.
# Files that may change keep their name, so every reference to them
# carries ?v= and the first eight hex digits of their SHA-256: a browser
# that cached the old one fetches the new one at once.

PAGE = """<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title_full}</title>
<meta name="description" content="{description}">
<meta name="author" content="Michel Garand">
<meta name="referrer" content="no-referrer">
<link rel="canonical" href="{canonical}">
{alternates}
<link rel="icon" href="{up}{v_mark}" type="image/svg+xml">
<link rel="stylesheet" href="{up}{v_css}">
</head>
<body>
<a class="skip" href="#main">{skip}</a>
<header class="head">
  <div class="bar">
    <a class="brand" href="{up}{home}"><img src="{up}{v_mark}" alt="" width="42" height="42"><span>UBEC · {hub}</span></a>
{langs}
  </div>
{nav}
{top}
</header>
<main id="main">
{note}{body}
</main>
<footer>
  <div class="foot">
    <p class="who">{initiative}</p>
    <p>{licence} {privacy}</p>
    <p>{sources}</p>
  </div>
</footer>
</body>
</html>
"""

HERO = """  <figure class="art">
    <img src="{up}{v_art}" alt="{image_alt}" width="1600" height="900">
    <figcaption class="hero">
      <h1>{title}</h1>
      <p class="other" lang="{other_lang}">{other_title}</p>
      <p class="tagline">{tagline}</p>
    </figcaption>
  </figure>"""

BAND = """  <div class="band">
    <p class="kind">{kind}</p>
    <h1>{title}</h1>
    <p class="sub">{subtitle}</p>
    <p class="meta">{dateline}{pdf}</p>
  </div>"""


def front_matter(path: Path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"\A---\n(.*?)\n---\n", text, flags=re.S)
    if not m:
        raise SystemExit(f"{path.name}: no front matter")
    meta = {}
    for line in m.group(1).splitlines():
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip()
    return meta, text[m.end():]


def pandoc(body: str, extra=()) -> str:
    return subprocess.run(["pandoc", "-f", "markdown" + "".join(extra), "-t", "html5", "--wrap=none"],
                          input=body, capture_output=True, text=True, check=True).stdout


def markdown(body: str) -> str:
    out = pandoc(body)
    # The map link carries the Plai emblem, the one place the emblem appears:
    # it points at a Plai application.
    out = re.sub(r'<li><a href="([^"]+)" class="plai">',
                 r'<li class="has-mark"><img class="mark" src="{up}assets/plai_emblem.svg" alt="" width="38" height="38"><a href="\1">',
                 out)
    # A line break inside a list item is the description that follows the link.
    out = re.sub(r"</a>\n", "</a> ", out)
    return out


def emblem() -> str:
    """The Plai emblem cropped to its outer ring, as build/logo.py does for the PDFs."""
    svg = EMBLEM.read_text(encoding="utf-8")
    cx, cy, r = 400, 400, 300
    if f'<circle cx="{cx}" cy="{cy}" r="{r}"' not in svg:
        raise SystemExit(f"{EMBLEM.name}: outer ring not found; crop by hand")
    box = f'viewBox="{cx - r} {cy - r} {2 * r} {2 * r}" width="{2 * r}" height="{2 * r}"'
    svg, n = re.subn(r'viewBox="[^"]*" width="[^"]*" height="[^"]*"', box, svg, count=1)
    if n != 1:
        raise SystemExit(f"{EMBLEM.name}: no viewBox to replace")
    return ("<!-- The Plai emblem, Michel Garand's, CC BY-SA 4.0; cropped to its circle "
            "from docs/proposal/assets/plai_emblem_mark.svg by build/build_site.py. -->\n" + svg)


def v(rel: str) -> str:
    """A file in site/dist/ named with its content's version, for the browser's cache."""
    return f"{rel}?v={hashlib.sha256((DIST / rel).read_bytes()).hexdigest()[:8]}"


# ---- the documents ----

def latest(pattern: str) -> Path:
    """The file in docs/ that matches, at its highest version if the name carries one."""
    def version(p):
        found = re.findall(r"v(\d+)_(\d+)", p.name)
        return tuple(int(n) for n in found[-1]) if found else (0, 0)
    found = sorted(ROOT.joinpath("docs").glob(pattern), key=version)
    if not found:
        raise SystemExit(f"docs/{pattern}: not found")
    return found[-1]


def heading_ids(md: str) -> str:
    """Stable ids for numbered headings, parts and appendices, in either language."""
    def one(m):
        hashes, text = m.group(1), m.group(2)
        if "{#" in text:
            return m.group(0)
        n = re.match(r"(\d+(?:\.\d+)*)\.?\s", text)
        if n:
            return f"{hashes} {text} {{#s{n.group(1).replace('.', '-')}}}"
        p = re.match(r"(?:Part|Частина) (III|II|I)\b", text)
        if p:
            return f"{hashes} {text} {{#part-{len(p.group(1))}}}"
        a = re.match(r"(?:Appendix|Додаток|Anhang|Załącznik) ([AАBВ])\b", text)
        if a:
            return f"{hashes} {text} {{#appendix-{'a' if a.group(1) in 'AА' else 'b'}}}"
        return m.group(0)
    return re.sub(r"^(#{2,4}) (.+?)\s*$", one, md, flags=re.M)


def read_doc(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"\A---\n(.*?)\n---\n", text, flags=re.S)
    if not m:
        raise SystemExit(f"{path.name}: no front matter")
    fm, body = m.group(1), text[m.end():]
    version = re.search(r'^version:\s*"?([^"\n]+?)"?\s*$', fm, flags=re.M).group(1)
    first = body.find("\n## ")
    if first < 0:
        raise SystemExit(f"{path.name}: no chapter heading")
    head, body = body[:first], body[first + 1:]
    # A changelog kept at the end of the text is the record's, not the reader's.
    body = re.split(r"\n\* \* \*\s*\n+\*Changelog\*", body)[0]
    sub = re.search(r"^\*(.+)\*\s*$", head, flags=re.M)
    lines = [l.strip() for l in head.splitlines()
             if l.strip() and not l.startswith(("#", "![", "*"))]
    return {"path": path, "version": version, "subtitle": sub.group(1) if sub else "",
            "dateline": lines[0] if lines else "", "body": heading_ids(body)}


def strip_tags(s: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def doc_html(doc: dict, d: dict, lang: str):
    """The document's body as HTML, its pictures copied in, and its table of contents."""
    out = pandoc(doc["body"], extra=("+autolink_bare_uris",))
    src_dir = doc["path"].parent

    def picture(m):
        ref = m.group(1)
        if re.match(r"[a-z]+:", ref):
            raise SystemExit(f"{doc['path'].name}: a picture from elsewhere: {ref}")
        source = (src_dir / ref).resolve()
        rel = f"files/{d['slug']}/{source.name}"
        (DIST / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, DIST / rel)
        return f'src="{{up}}{v(rel)}"'
    out = re.sub(r'src="([^"]+)"', picture, out)
    # Pandoc gives wide tables column widths as inline styles, which the policy
    # refuses; the stylesheet lays tables out instead.
    out = re.sub(r"<colgroup>.*?</colgroup>\s*", "", out, flags=re.S)
    # A wide table scrolls inside its own region, which the keyboard can reach.
    out = out.replace("<table>", f'<div class="table" role="region" tabindex="0" '
                                 f'aria-label="{WORDS[lang]["table"]}"><table>').replace("</table>", "</table></div>")
    # Headings: h2 chapters; under Part II of the agreement, its roles.
    toc, part = [], None
    for level, hid, text in re.findall(r'<h([23]) id="([^"]+)"[^>]*>(.*?)</h\1>', out, flags=re.S):
        if level == "2":
            part = hid
        if d["toc"] and (level == "2" or (d["toc"] == "h2+roles" and part == "part-2")):
            toc.append((int(level), hid, strip_tags(text)))
    return out, toc


# ---- the menu ----

def doc_lang(d: dict, lang: str) -> str:
    return lang if lang in d["src"] else "en"


def doc_path(d: dict, lang: str) -> str:
    """The document's page, from the site's root, without a leading slash."""
    l = doc_lang(d, lang)
    return f"{'' if l == 'en' else l + '/'}{d['slug']}/"


def home_path(lang: str) -> str:
    return "" if lang == "en" else f"{lang}/"


def lang_list(lang: str, up: str, targets: dict) -> str:
    """The language list: the page's own language named, the others a click away.
    `targets` gives, for each language, the page to go to from the site's root."""
    items = []
    for l in LANGS:
        if l not in targets:
            continue
        cur = ' aria-current="true"' if l == lang else ""
        items.append(f'<li><a href="{up}{targets[l]}" hreflang="{l}" lang="{l}"{cur}>{LANG_NAMES[l]}</a></li>')
    return (f'    <details class="langs" name="menu"><summary>'
            f'<span class="vh">{WORDS[lang]["language"]}: </span>{LANG_NAMES[lang]}</summary>'
            f'<ul class="panel">{"".join(items)}</ul></details>')


def nav(lang: str, up: str, current: str, tocs: dict) -> str:
    w = WORDS[lang]
    home = home_path(lang)

    def item(label, href, here, attrs="", raw=False):
        cur = ' aria-current="page"' if here else ""
        cls = ' class="here"' if here else ""
        return f'<li{cls}><a href="{href}"{cur}{attrs}>{label if raw else html.escape(label)}</a></li>'

    items = [item(w["about"], f"{up}{home}", current == "home")]
    for d in DOCS:
        l = doc_lang(d, lang)
        # A document not in the page's language: a small EN for the eye, the
        # words in full for a screen reader.
        label = html.escape(d["label"][lang]) + (
            f'<span class="tag" aria-hidden="true">EN</span><span class="vh">{w["in_en"]}</span>'
            if l != lang else "")
        attrs = f' hreflang="{l}"' if l != lang else ""
        href = f"{up}{doc_path(d, lang)}"
        toc = tocs.get((d["slug"], l))
        if not toc:
            items.append(item(label, href, current == d["slug"], attrs, raw=True))
            continue
        here = current == d["slug"]
        cur = ' aria-current="page"' if here else ""
        entries = [f'<li><a href="{href}"{cur}>{w["whole"]}</a></li>']
        for level, hid, text in toc:
            entries.append(f'<li class="l{level}"><a href="{href}#{hid}">{html.escape(text)}</a></li>')
        if l in d["pdf"]:
            path, kind = d["pdf"][l]
            entries.append(f'<li class="pdf"><a href="{up}{v("files/" + Path(path).name)}" '
                           f'type="application/pdf">{w["pdf"] if kind == "en-uk" else w["pdf_own"]}</a></li>')
        # A panel of chapters in another language says which.
        panel_lang = f' lang="{l}"' if l != lang else ""
        items.append(f'<li class="drop{" here" if here else ""}"><details name="menu">'
                     f'<summary>{label}</summary>'
                     f'<ul class="panel"{panel_lang}>{"".join(entries)}</ul></details></li>')
    items.append(item(w["map"], MAP, False))
    items.append(item(w["writing"], WRITING, False))
    return (f'  <nav class="menu" aria-label="{w["nav"]}">\n    <ul>\n      '
            + "\n      ".join(items) + "\n    </ul>\n  </nav>")


def new_tab(page: str) -> str:
    """The map and the field writing open in a new tab (Michel's word, October 11,
    2026), and say so: an arrow for the eye, the words for a screen reader, and no
    opener for the page they open."""
    lang = re.search(r'<html lang="([a-z]+)"', page).group(1)
    said = WORDS[lang]["new_tab"]

    def one(m):
        return (f'<a href="{m.group(1)}"{m.group(2)} target="_blank" rel="noopener">'
                f'{m.group(3)}<span class="vh">{said}</span></a>')
    return re.sub(r'<a href="(https://(?:mapservice|soilandpeace)\.ubec\.network/[^"]*)"([^>]*)>(.*?)</a>',
                  one, page, flags=re.S)


# ---- the build ----

def build():
    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(STATIC, DIST)
    (DIST / "assets" / "plai_emblem.svg").write_text(emblem(), encoding="utf-8")
    (DIST / "files").mkdir()

    pages = {}
    for path in sorted(CONTENT.glob("*.md")):
        meta, body = front_matter(path)
        pages[meta["lang"]] = (meta, body)
    if "en" not in pages or not set(pages) <= set(LANGS):
        raise SystemExit(f"site/content: expected en and any of {LANGS}, found {sorted(pages)}")
    pages = {l: pages[l] for l in LANGS if l in pages}

    # The documents first: their tables of contents go into every page's menu.
    docs, tocs = {}, {}
    for d in DOCS:
        for path, _ in set(d["pdf"].values()):
            shutil.copyfile(ROOT / "docs" / path, DIST / "files" / Path(path).name)
        for l, pattern in d["src"].items():
            doc = read_doc(latest(pattern))
            doc["html"], tocs[(d["slug"], l)] = doc_html(doc, d, l)
            docs[(d["slug"], l)] = doc

    e = html.escape
    common = dict(v_css=v("style.css"), v_mark=v("assets/ubec_mark.svg"))

    def write(rel_path: str, doc_text: str):
        doc_text = new_tab(doc_text)
        out = DIST / rel_path.lstrip("/") / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(doc_text, encoding="utf-8")
        print("wrote", out.relative_to(ROOT))

    # The landing page, in each language.
    for lang, (meta, body) in pages.items():
        other_lang = OTHER[lang]
        other = pages[other_lang][0]
        up = "../" * meta["path"].strip("/").count("/") + ("../" if meta["path"].strip("/") else "")
        alternates = "\n".join(
            [f'<link rel="alternate" hreflang="{l}" href="{ORIGIN}{pages[l][0]["path"]}">' for l in pages]
            + [f'<link rel="alternate" hreflang="x-default" href="{ORIGIN}/">'])
        top = HERO.format(up=up, v_art=v("assets/warm_wind_on_the_path.svg"), image_alt=e(meta["image_alt"]),
                          title=e(meta["title"]), other_lang=other_lang, other_title=e(other["title"]),
                          tagline=e(meta["tagline"]))
        write(meta["path"], PAGE.format(
            lang=lang, up=up, home=meta["path"].lstrip("/"),
            title_full=e(f'{meta["title"]} — {other["title"]}'),
            description=e(meta["description"]), canonical=ORIGIN + meta["path"],
            alternates=alternates, skip=WORDS[lang]["skip"], hub=WORDS[lang]["hub"],
            langs=lang_list(lang, up, {l: home_path(l) for l in pages}),
            nav=nav(lang, up, "home", tocs).replace("{up}", up), top=top,
            note=f'<p class="note">{NOTES[lang]}</p>\n' if lang in NOTES else "",
            body=markdown(body).replace("{up}", up).replace("assets/plai_emblem.svg", v("assets/plai_emblem.svg")),
            initiative=e(meta["initiative"]), licence=e(meta["licence"]), privacy=e(meta["privacy"]),
            sources=e(f'{meta["sources"]} {WORDS[lang]["version"]} {meta["version"]}.'), **common))

    # A page per document and language.
    for (slug, lang), doc in docs.items():
        d = next(x for x in DOCS if x["slug"] == slug)
        meta = pages[lang][0]
        langs = [l for l in LANGS if l in d["src"]]
        rel = doc_path(d, lang)
        up = "../" * rel.strip("/").count("/") + "../"
        # From a document, each language leads to the same document in it, or to
        # that language's landing page when the document has no text in it.
        targets = {l: doc_path(d, l) if l in d["src"] else home_path(l) for l in pages}
        alternates = "\n".join(
            f'<link rel="alternate" hreflang="{l}" href="{ORIGIN}/{doc_path(d, l)}">' for l in langs)
        file = doc["path"].relative_to(ROOT).as_posix()
        pdf = ""
        if lang in d["pdf"]:
            path, kind = d["pdf"][lang]
            pdf = (f' · <a href="{up}{v("files/" + Path(path).name)}" type="application/pdf">'
                   f'{WORDS[lang]["doc_pdf"] if kind == "en-uk" else WORDS[lang]["doc_pdf_own"]}</a>')
        top = BAND.format(kind=e(d["kind"][lang]), title=e(meta["title"]), subtitle=e(doc["subtitle"].strip("*")),
                          dateline=e(doc["dateline"] if doc["version"] in doc["dateline"]
                                     else f'{doc["dateline"]} · {doc["version"]}'), pdf=pdf)
        built = WORDS[lang]["built"].format(file=file, version=doc["version"])
        write(rel, PAGE.format(
            lang=lang, up=up, home=home_path(lang),
            title_full=e(f'{d["label"][lang]} — {meta["title"]}'),
            description=e(doc["subtitle"] or meta["description"]), canonical=f"{ORIGIN}/{rel}",
            alternates=alternates, skip=WORDS[lang]["skip"], hub=WORDS[lang]["hub"],
            langs=lang_list(lang, up, targets),
            nav=nav(lang, up, slug, tocs).replace("{up}", up), top=top,
            note=f'<p class="note">{NOTES[lang]}</p>\n' if lang in NOTES else "",
            body=f'<article class="doc">\n{doc["html"].replace("{up}", up)}\n</article>',
            initiative=e(meta["initiative"]), licence=WORDS[lang]["licence"], privacy=e(meta["privacy"]),
            sources=f'{e(built)} <a href="{RECORD}/blob/main/{file}">{WORDS[lang]["record"]}</a>.',
            **common))


# WCAG 2.2 AA: every pair of colours the stylesheet sets text or a focus
# outline in, by the names of its :root variables, with the least ratio
# allowed (4.5 for text, 3 for an outline). A new colour pair in
# style.css gets a line here.
CONTRAST = [
    ("ink", "paper", 4.5, "body text"),
    ("quiet", "paper", 4.5, "quiet text, the foot"),
    ("terra", "paper", 4.5, "links"),
    ("night", "paper", 4.5, "headings, links in the list, the menu's panel"),
    ("quiet", "cream-2", 4.5, "the stage block"),
    ("terra", "cream-2", 4.5, "links in the stage block"),
    ("ink", "cream-2", 4.5, "text in the stage block, table heads"),
    ("cream", "night", 4.5, "the head, the menu"),
    ("cream-2", "night", 4.5, "the head, the document's band"),
    ("ochre", "night", 4.5, "the other language's name, narrow; the menu's current page; links in the band"),
    ("night", "cream", 4.5, "the language list, hovered or open; a menu item, hovered"),
    ("night", "cream-2", 4.5, "a link in the menu's panel, hovered"),
    ("night", "paper", 3.0, "focus outline, also in the menu's panel"),
    ("night", "cream-2", 3.0, "focus outline in the stage block"),
    ("ochre", "night", 3.0, "focus outline in the head and the menu"),
]
BCP47 = re.compile(r"^[a-z]{2,3}(-[A-Z][a-z]{3})?(-([A-Z]{2}|[0-9]{3}))?$")


def luminance(hexcolour: str) -> float:
    h = hexcolour.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    def lin(c):
        c = int(c, 16) / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = lin(h[0:2]), lin(h[2:4]), lin(h[4:6])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_problems(css_text: str) -> list:
    colours = dict(re.findall(r"--([a-z0-9-]+):\s*(#[0-9a-fA-F]{3,6})\s*;", css_text))
    problems = []
    for fg, bg, least, where in CONTRAST:
        if fg not in colours or bg not in colours:
            problems.append(f"style.css: --{fg} or --{bg} not defined ({where})")
            continue
        a, b = sorted((luminance(colours[fg]), luminance(colours[bg])), reverse=True)
        ratio = (a + 0.05) / (b + 0.05)
        if ratio < least:
            problems.append(f"style.css: {fg} on {bg} is {ratio:.2f}:1, below {least}:1 ({where})")
    return problems


VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr",
        "path", "circle", "rect"}
OPTIONAL_END = {"p", "li"}


class Refs(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.loads, self.links, self.stack, self.errors = [], [], [], []
        self.headings, self.langs, self.title, self.in_title = [], [], "", False
        self.link = None
        self.doc_links = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        for key in ("lang", "hreflang"):
            if key in a:
                self.langs.append(a[key] or "")
        if re.fullmatch(r"h[1-6]", tag):
            self.headings.append(int(tag[1]))
        if tag == "title":
            self.in_title = True
        if tag == "img" and "alt" not in a:
            self.errors.append(f"a picture without alt: {a.get('src')}")
        if tag == "a":
            self.link = {"href": a.get("href"), "name": (a.get("aria-label") or "").strip()}
        if tag == "img" and self.link is not None and (a.get("alt") or "").strip():
            self.link["name"] += a["alt"]
        if tag in ("img", "script", "iframe", "source", "embed", "audio", "video"):
            if a.get("src"):
                self.loads.append(a["src"])
        if tag == "link" and a.get("href"):
            (self.links if a.get("rel") in ("canonical", "alternate") else self.loads).append(a["href"])
        if tag == "a" and a.get("target") == "_blank" and "noopener" not in (a.get("rel") or ""):
            self.errors.append(f"a new tab with an opener: {a.get('href')}")
        if tag == "a" and a.get("href"):
            # A link inside a document's own text may go to the sources it cites.
            (self.doc_links if "article" in self.stack else self.links).append(a["href"])
        if tag == "script":
            self.errors.append("a script: the site carries no JavaScript")
        if "style" in a:
            self.errors.append(f"an inline style on <{tag}>: the policy allows the stylesheet only")
        if tag not in VOID:
            self.stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID and self.stack and self.stack[-1] == tag:
            self.stack.pop()

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self.link is not None:
            self.link["name"] += data.strip()

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if tag == "a" and self.link is not None:
            if not self.link["name"]:
                self.errors.append(f"a link with no name: {self.link['href']}")
            self.link = None
        if tag in VOID:
            return
        while self.stack and self.stack[-1] != tag and self.stack[-1] in OPTIONAL_END:
            self.stack.pop()
        if not self.stack or self.stack[-1] != tag:
            self.errors.append(f"</{tag}> closes nothing open (open: {self.stack[-3:]})")
            return
        self.stack.pop()


def link_problem(page: Path, ref: str, in_doc: bool):
    u = urlparse(ref)
    if u.scheme == "mailto":
        return None if u.path in MAILTO else f"mails an address not listed: {ref}"
    if u.scheme in ("http", "https"):
        if u.netloc == urlparse(ORIGIN).netloc:
            return None
        if u.netloc == "mapservice.ubec.network" and u.path not in MAP_PATHS:
            return f"links into the map beyond its front page and the Pathways application: {ref}"
        if u.scheme == "https" and u.netloc in LINKS_OUT:
            return None
        if u.scheme == "https" and u.netloc in LINKS_OUT_PATHS and \
                (u.path + "/").startswith(LINKS_OUT_PATHS[u.netloc] + "/"):
            return None
        if in_doc and u.scheme == "https":
            return None
        return f"links out to a host not listed: {ref}"
    if u.scheme:
        return f"a link of an unknown kind: {ref}"
    if u.path:
        target = (page.parent / u.path).resolve()
        if target.is_dir():
            target = target / "index.html"
        if not target.exists():
            return f"links to a missing page: {ref}"
    return None


def check(dist: Path = DIST) -> None:
    problems = []
    ids = {}
    for page in sorted(dist.rglob("*.html")):
        ids[page.resolve()] = set(re.findall(r'\sid="([^"]+)"', page.read_text(encoding="utf-8")))
    for page in sorted(dist.rglob("*.html")):
        rel = page.relative_to(dist)
        p = Refs()
        p.feed(page.read_text(encoding="utf-8"))
        p.close()
        open_ = [t for t in p.stack if t not in OPTIONAL_END]
        if open_:
            problems.append(f"{rel}: left open: {open_}")
        problems += [f"{rel}: {e}" for e in p.errors]
        if not p.langs or p.langs[0] not in LANGS:
            problems.append(f"{rel}: the page's language is not one of {LANGS}")
        # hreflang="x-default" names the page for any other language; it is not a tag.
        problems += [f"{rel}: not a BCP 47 tag: '{t}'" for t in p.langs if t != "x-default" and not BCP47.match(t)]
        if p.headings.count(1) != 1:
            problems.append(f"{rel}: {p.headings.count(1)} h1, not one")
        for before, after in zip(p.headings, p.headings[1:]):
            if after > before + 1:
                problems.append(f"{rel}: heading h{before} followed by h{after}")
        if not p.title.strip():
            problems.append(f"{rel}: no title")
        for ref in p.loads:
            u = urlparse(ref)
            if u.scheme or u.netloc:
                problems.append(f"{rel}: loads from another server: {ref}")
            elif not (page.parent / u.path).resolve().exists():
                problems.append(f"{rel}: loads a missing file: {ref}")
        for ref, in_doc in [(r, False) for r in p.links] + [(r, True) for r in p.doc_links]:
            problem = link_problem(page, ref, in_doc)
            if problem:
                problems.append(f"{rel}: {problem}")
                continue
            u = urlparse(ref)
            if not u.scheme and u.fragment:
                target = (page.parent / u.path).resolve() if u.path else page.resolve()
                if target.is_dir():
                    target = target / "index.html"
                if u.fragment not in ids.get(target, set()):
                    problems.append(f"{rel}: links to a missing part: {ref}")
    for css in sorted(dist.rglob("*.css")):
        for ref in re.findall(r"url\(\s*['\"]?([^'\")]+)", css.read_text(encoding="utf-8")):
            u = urlparse(ref)
            if u.scheme or u.netloc:
                problems.append(f"{css.relative_to(dist)}: loads from another server: {ref}")
            elif not (css.parent / u.path).resolve().exists():
                problems.append(f"{css.relative_to(dist)}: loads a missing file: {ref}")
        if "@import" in css.read_text(encoding="utf-8"):
            problems.append(f"{css.relative_to(dist)}: @import")
    problems += contrast_problems((dist / "style.css").read_text(encoding="utf-8"))
    for svg in sorted(dist.rglob("*.svg")):
        if re.search(r"(href|src)=\"https?:", svg.read_text(encoding="utf-8")):
            problems.append(f"{svg.relative_to(dist)}: refers to another server")
    if problems:
        raise SystemExit("check failed:\n  " + "\n  ".join(problems))
    n = len(list(dist.rglob("*.html")))
    print(f"check: {n} pages, every reference resolves, nothing loads from another server;"
          f" WCAG checks passed, {len(CONTRAST)} colour pairs")


def deploy(host: str, path: str) -> None:
    build()
    check()
    cmd = ["rsync", "-rlt", "--delete", "--chmod=D755,F644", "--itemize-changes",
           f"{DIST}/", f"{host}:{path.rstrip('/')}/"]
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)


class Fetched(Refs):
    pass


def verify(origin: str) -> None:
    """Fetch every page and every file it loads; list every host contacted."""
    origin = origin.rstrip("/")
    own = urlparse(origin).netloc
    hosts, problems = set(), []
    seen, queue = set(), [origin + "/"] + [f"{origin}/{l}/" for l in LANGS if l != "en"]

    def get(url):
        req = urllib.request.Request(url, headers={"User-Agent": "tcp-site-verify/0.2"})
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, dict(r.headers), r.read()

    while queue:
        url = queue.pop(0).split("#")[0]
        if url in seen:
            continue
        seen.add(url)
        hosts.add(urlparse(url).netloc)
        status, headers, body = get(url)
        if status != 200:
            problems.append(f"{url}: {status}")
        ctype = headers.get("Content-Type", "")
        if "text/html" in ctype:
            for h in ("Content-Security-Policy", "Strict-Transport-Security", "X-Content-Type-Options"):
                if h not in headers:
                    problems.append(f"{url}: no {h}")
            if "Set-Cookie" in headers:
                problems.append(f"{url}: sets a cookie")
            p = Fetched()
            p.feed(body.decode("utf-8"))
            queue += [urljoin(url, ref) for ref in p.loads]
            # Follow the site's own pages and files through the menu, never out.
            queue += [urljoin(url, ref) for ref in p.links if urlparse(urljoin(url, ref)).netloc == own]
        elif "text/css" in ctype:
            queue += [urljoin(url, ref) for ref in re.findall(r"url\(\s*['\"]?([^'\")]+)", body.decode("utf-8"))]
    print("hosts contacted:", ", ".join(sorted(hosts)))
    print(f"files fetched: {len(seen)}")
    if hosts != {own}:
        problems.append(f"contacted more than {own}: {sorted(hosts)}")
    if problems:
        raise SystemExit("verify failed:\n  " + "\n  ".join(problems))
    print("verify: the site's own name only")


def main(argv):
    if not argv:
        build()
        check()
    elif argv[0] == "check":
        check()
    elif argv[0] == "deploy" and len(argv) == 3:
        deploy(argv[1], argv[2])
    elif argv[0] == "verify" and len(argv) == 2:
        verify(argv[1])
    else:
        raise SystemExit(__doc__.split("\n\n")[1])


if __name__ == "__main__":
    main(sys.argv[1:])
