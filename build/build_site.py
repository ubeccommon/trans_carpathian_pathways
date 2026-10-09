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
to its circle from docs/proposal/assets/plai_emblem_mark.svg. site/dist/
is not tracked; the host and the path are arguments, never in the tree.

The check refuses a build in which any page or stylesheet loads anything
from another server, links to a file that is not there, or leaves an
element unclosed; links out are allowed only to the hosts in LINKS_OUT.

Needs pandoc on the PATH, and Python 3 alone; deploy needs rsync and ssh.

SPDX-License-Identifier: AGPL-3.0-or-later

Changelog:
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
LINKS_OUT = {"mapservice.ubec.network", "pilgrims.ubec.network"}
MAILTO = {"stewardship@ubec.network"}

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
    <a class="brand" href="{up}{home}"><img src="{up}{v_mark}" alt="UBEC" width="42" height="42"><span>UBEC · {hub}</span></a>
    <a class="switch" href="{up}{other_href}" hreflang="{other_lang}" lang="{other_lang}">{switch}</a>
  </div>
  <figure class="art">
    <img src="{up}{v_art}" alt="{image_alt}" width="1600" height="900">
    <figcaption class="hero">
      <h1>{title}</h1>
      <p class="other" lang="{other_lang}">{other_title}</p>
      <p class="tagline">{tagline}</p>
    </figcaption>
  </figure>
</header>
<main id="main">
{body}
</main>
<footer>
  <div class="foot">
    <p class="who">{initiative}</p>
    <p>{licence} {privacy}</p>
    <p>{sources} {version_label} {version}.</p>
  </div>
</footer>
</body>
</html>
"""

HUB = {"en": "Carpathian Hub Initiative", "uk": "Ініціатива Карпатського хабу"}
SKIP = {"en": "Skip to the text", "uk": "До тексту"}
VERSION = {"en": "Page", "uk": "Сторінка"}


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


def markdown(body: str) -> str:
    out = subprocess.run(["pandoc", "-f", "markdown", "-t", "html5", "--wrap=none"],
                         input=body, capture_output=True, text=True, check=True).stdout
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


def build():
    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(STATIC, DIST)
    (DIST / "assets" / "plai_emblem.svg").write_text(emblem(), encoding="utf-8")

    pages = {}
    for path in sorted(CONTENT.glob("*.md")):
        meta, body = front_matter(path)
        pages[meta["lang"]] = (meta, body)
    if set(pages) != {"en", "uk"}:
        raise SystemExit(f"site/content: expected en and uk, found {sorted(pages)}")

    for lang, (meta, body) in pages.items():
        other_lang = "uk" if lang == "en" else "en"
        other = pages[other_lang][0]
        depth = meta["path"].strip("/").count("/") + (1 if meta["path"].strip("/") else 0)
        up = "../" * depth
        alternates = "\n".join(
            f'<link rel="alternate" hreflang="{l}" href="{ORIGIN}{pages[l][0]["path"]}">' for l in ("en", "uk"))
        e = html.escape
        doc = PAGE.format(
            lang=lang, up=up, home=meta["path"].lstrip("/"),
            title=e(meta["title"]), other_title=e(other["title"]),
            title_full=e(f'{meta["title"]} — {other["title"]}'),
            description=e(meta["description"]), canonical=ORIGIN + meta["path"],
            alternates=alternates, skip=SKIP[lang], hub=HUB[lang],
            other_href=other["path"].lstrip("/"), other_lang=other_lang, switch=e(meta["switch"]),
            tagline=e(meta["tagline"]), image_alt=e(meta["image_alt"]),
            v_css=v("style.css"), v_mark=v("assets/ubec_mark.svg"), v_art=v("assets/warm_wind_on_the_path.svg"),
            body=markdown(body).replace("{up}", up).replace("assets/plai_emblem.svg", v("assets/plai_emblem.svg")),
            initiative=e(meta["initiative"]), licence=e(meta["licence"]), privacy=e(meta["privacy"]),
            sources=e(meta["sources"]), version_label=VERSION[lang], version=e(meta["version"]))
        out = DIST / meta["path"].lstrip("/") / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(doc, encoding="utf-8")
        print("wrote", out.relative_to(ROOT))


VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr",
        "path", "circle", "rect"}
OPTIONAL_END = {"p", "li"}


class Refs(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.loads, self.links, self.stack, self.errors = [], [], [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("img", "script", "iframe", "source", "embed", "audio", "video"):
            if a.get("src"):
                self.loads.append(a["src"])
        if tag == "link" and a.get("href"):
            (self.links if a.get("rel") in ("canonical", "alternate") else self.loads).append(a["href"])
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
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

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        while self.stack and self.stack[-1] != tag and self.stack[-1] in OPTIONAL_END:
            self.stack.pop()
        if not self.stack or self.stack[-1] != tag:
            self.errors.append(f"</{tag}> closes nothing open (open: {self.stack[-3:]})")
            return
        self.stack.pop()


def check(dist: Path = DIST) -> None:
    problems = []
    for page in sorted(dist.rglob("*.html")):
        rel = page.relative_to(dist)
        p = Refs()
        p.feed(page.read_text(encoding="utf-8"))
        p.close()
        open_ = [t for t in p.stack if t not in OPTIONAL_END]
        if open_:
            problems.append(f"{rel}: left open: {open_}")
        problems += [f"{rel}: {e}" for e in p.errors]
        for ref in p.loads:
            u = urlparse(ref)
            if u.scheme or u.netloc:
                problems.append(f"{rel}: loads from another server: {ref}")
            elif not (page.parent / u.path).resolve().exists():
                problems.append(f"{rel}: loads a missing file: {ref}")
        for ref in p.links:
            u = urlparse(ref)
            if u.scheme == "mailto":
                if u.path not in MAILTO:
                    problems.append(f"{rel}: mails an address not listed: {ref}")
            elif u.scheme in ("http", "https"):
                if u.netloc == urlparse(ORIGIN).netloc:
                    continue
                if u.scheme != "https" or u.netloc not in LINKS_OUT:
                    problems.append(f"{rel}: links out to a host not listed: {ref}")
            elif not u.scheme and u.path:
                target = (page.parent / u.path).resolve()
                if target.is_dir():
                    target = target / "index.html"
                if not target.exists():
                    problems.append(f"{rel}: links to a missing page: {ref}")
    for css in sorted(dist.rglob("*.css")):
        for ref in re.findall(r"url\(\s*['\"]?([^'\")]+)", css.read_text(encoding="utf-8")):
            u = urlparse(ref)
            if u.scheme or u.netloc:
                problems.append(f"{css.relative_to(dist)}: loads from another server: {ref}")
            elif not (css.parent / u.path).resolve().exists():
                problems.append(f"{css.relative_to(dist)}: loads a missing file: {ref}")
        if "@import" in css.read_text(encoding="utf-8"):
            problems.append(f"{css.relative_to(dist)}: @import")
    for svg in sorted(dist.rglob("*.svg")):
        if re.search(r"(href|src)=\"https?:", svg.read_text(encoding="utf-8")):
            problems.append(f"{svg.relative_to(dist)}: refers to another server")
    if problems:
        raise SystemExit("check failed:\n  " + "\n  ".join(problems))
    n = len(list(dist.rglob("*.html")))
    print(f"check: {n} pages, every reference resolves, nothing loads from another server")


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
    hosts, problems = set(), []
    seen, queue = set(), [origin + "/", origin + "/uk/"]

    def get(url):
        req = urllib.request.Request(url, headers={"User-Agent": "tcp-site-verify/0.1"})
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, dict(r.headers), r.read()

    while queue:
        url = queue.pop(0)
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
        elif "text/css" in ctype:
            queue += [urljoin(url, ref) for ref in re.findall(r"url\(\s*['\"]?([^'\")]+)", body.decode("utf-8"))]
    print("hosts contacted:", ", ".join(sorted(hosts)))
    print(f"files fetched: {len(seen)}")
    own = urlparse(origin).netloc
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
