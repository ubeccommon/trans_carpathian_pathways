#!/usr/bin/env python3
"""
fetch_pathways_basemaps.py — download public-domain historic map sheets and
OpenAerialMap imagery for the Hutsul corridor (Trans-Carpathian Pathways).

Run on your own machine (schiff), not in a sandbox:

    python3 fetch_pathways_basemaps.py [--out DATA_DIR]

Downloads into DATA_DIR (default ./pathways_basemaps):
    historic/sdoum_75k/   Austro-Hungarian Spezialkarte 1:75,000 sheets
                          (Third Military Survey; scans from the mapywig
                          archive, indexed at igrek.amzp.pl — public domain)
    historic/gkm_200k/    Generalkarte 1:200,000 overview sheets 42-47, 42-48
                          (from Wikimedia Commons — public domain)
    oam/                  Any CC-BY imagery OpenAerialMap holds for the
                          corridor (currently none — kept so re-runs pick up
                          new uploads, including your own)

Stdlib only. Be gentle: one request at a time, with a pause.
"""

import argparse
import html
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

UA = {"User-Agent": "TransCarpathianPathways/0.1 (michel@ubec.network; corridor basemap fetch)"}
PAUSE = 2.0  # seconds between requests

# Hutsul corridor, generous: Vorokhta .. Kosiv/Kuty, down past Hryniawa
CORRIDOR_BBOX = (24.3, 47.8, 25.4, 48.5)   # W, S, E, N (Greenwich)

# Place names that appear in Spezialkarte sheet titles for this area.
# Sheets of interest (15' lat x 30' lon, Ferro longitudes):
#   Zone 12 Kol. XXXI/XXXII  (48°15'-48°30'N)  — Mikuliczyn, Kosów, Kuty, Kołomyja edge
#   Zone 13 Kol. XXXI/XXXII  (48°00'-48°15'N)  — Żabie (Verkhovyna), Worochta
#   Zone 14 Kol. XXXI/XXXII  (47°45'-48°00'N)  — Hryniawa, Burkut, Czywczyn
SHEET_NAMES = [
    "zabie", "żabie", "kuty", "kosów", "kosow", "worochta", "mikuliczyn",
    "hryniawa", "hryniava", "burkut", "delatyn", "nadwórna", "nadworna",
    "pistyń", "pistyn", "kołomyja", "kolomyja", "jablonów", "jablonow",
    "körösmező", "korosmezo", "jasina", "czywczyn", "kirlibaba",
]
ZONE_KOL = re.compile(r"(?:z(?:one)?[ ._-]*1[234])[ ._-]*(?:k(?:ol)?\.?[ ._-]*)(?:xxxi{1,2}|3[12])",
                      re.IGNORECASE)

IGREK = "http://igrek.amzp.pl"
FILE_HOSTS = ("mapywig.org", "amzp.pl")
FILE_EXT = (".jpg", ".jpeg", ".png", ".tif", ".tiff", ".pdf", ".zip")


def get(url: str, binary: bool = False, timeout: int = 120):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = r.read()
    time.sleep(PAUSE)
    return data if binary else data.decode("utf-8", errors="replace")


def download(url: str, dest: Path) -> bool:
    if dest.exists() and dest.stat().st_size > 0:
        print(f"    have      {dest.name}")
        return True
    try:
        print(f"    fetching  {url}")
        data = get(url, binary=True)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        print(f"    saved     {dest.name}  ({len(data)/1e6:.1f} MB)")
        return True
    except Exception as e:
        print(f"    FAILED    {url}  ({e})", file=sys.stderr)
        return False


def links_in(page: str, base: str):
    for m in re.finditer(r'href=["\']([^"\']+)["\']', page, re.IGNORECASE):
        yield urllib.parse.urljoin(base, html.unescape(m.group(1)))


# ---------------------------------------------------------------- Spezialkarte

def fetch_spezialkarte(out: Path):
    print("\n== Spezialkarte 1:75,000 (Third Military Survey) via igrek.amzp.pl ==")
    out.mkdir(parents=True, exist_ok=True)
    try:
        front = get(IGREK + "/")
    except Exception as e:
        print(f"  could not reach {IGREK}: {e}", file=sys.stderr)
        print("  -> open it in a browser instead; series: K.u.K. Spezialkarte 1:75 000.")
        return

    # Find index pages for the K.u.K. 1:75k series on the front page.
    series_pages = sorted({
        u for u in links_in(front, IGREK + "/")
        if re.search(r"(075|75\s*0{3}|kuk)", u, re.IGNORECASE) and "amzp.pl" in u
    })
    if not series_pages:
        series_pages = [IGREK + "/mapindex.php?cat=KUK075"]
    print(f"  index pages to scan: {len(series_pages)}")

    candidates: dict[str, str] = {}   # url -> matched label
    for page_url in series_pages:
        try:
            page = get(page_url)
        except Exception as e:
            print(f"  skip {page_url} ({e})", file=sys.stderr)
            continue
        # Walk one level deeper: sheet-list pages linked from the series index.
        subpages = [u for u in links_in(page, page_url)
                    if "amzp.pl" in u and not u.lower().endswith(FILE_EXT)]
        for sub in [page_url] + subpages[:60]:
            try:
                sheet_html = page if sub == page_url else get(sub)
            except Exception:
                continue
            text = sheet_html.lower()
            if not (any(n in text for n in SHEET_NAMES) or ZONE_KOL.search(sheet_html)):
                continue
            for u in links_in(sheet_html, sub):
                low = u.lower()
                if any(h in low for h in FILE_HOSTS) and low.endswith(FILE_EXT):
                    fname = urllib.parse.unquote(low.rsplit("/", 1)[-1])
                    if any(n in fname for n in SHEET_NAMES) or ZONE_KOL.search(fname):
                        candidates[u] = fname
    if not candidates:
        print("  No sheet scans matched automatically — the index layout may differ.")
        print("  Open http://igrek.amzp.pl in a browser, series 'Spezialkarte 1:75 000',")
        print("  and search for: Żabie, Kuty, Kosów, Worochta, Mikuliczyn, Hryniawa, Burkut.")
        return
    print(f"  matched {len(candidates)} sheet file(s):")
    for url, name in sorted(candidates.items(), key=lambda kv: kv[1]):
        download(url, out / Path(urllib.parse.urlparse(url).path).name)


# ------------------------------------------------------- Generalkarte (Commons)

def fetch_generalkarte(out: Path):
    print("\n== Generalkarte 1:200,000 overview sheets (Wikimedia Commons) ==")
    out.mkdir(parents=True, exist_ok=True)
    api = "https://commons.wikimedia.org/w/api.php"
    for sheet in ("42-48", "42-47", "41-48"):
        q = urllib.parse.urlencode({
            "action": "query", "format": "json", "list": "search",
            "srnamespace": "6", "srlimit": "5",
            "srsearch": f'insource:"{sheet}" Generalkarte OR "Mitteleuropa" {sheet}',
        })
        try:
            res = json.loads(get(f"{api}?{q}"))
            hits = [h["title"] for h in res["query"]["search"] if sheet in h["title"]]
        except Exception as e:
            print(f"  search failed for {sheet}: {e}", file=sys.stderr)
            continue
        if not hits:
            print(f"  {sheet}: no Commons file found")
            continue
        title = hits[0]
        q2 = urllib.parse.urlencode({
            "action": "query", "format": "json", "prop": "imageinfo",
            "iiprop": "url", "titles": title,
        })
        try:
            info = json.loads(get(f"{api}?{q2}"))
            page = next(iter(info["query"]["pages"].values()))
            url = page["imageinfo"][0]["url"]
        except Exception as e:
            print(f"  imageinfo failed for {title}: {e}", file=sys.stderr)
            continue
        safe = re.sub(r"[^\w.-]+", "_", title.removeprefix("File:"))
        download(url, out / safe)


# ------------------------------------------------------------------------- OAM

def fetch_oam(out: Path):
    print("\n== OpenAerialMap (CC-BY 4.0) ==")
    out.mkdir(parents=True, exist_ok=True)
    w, s, e, n = CORRIDOR_BBOX
    url = f"https://api.openaerialmap.org/meta?bbox={w},{s},{e},{n}&limit=100"
    try:
        meta = json.loads(get(url))
    except Exception as ex:
        print(f"  API failed: {ex}", file=sys.stderr)
        return
    (out / "meta.json").write_text(json.dumps(meta, indent=2))
    results = meta.get("results", [])
    print(f"  imagery in corridor bbox: {len(results)}"
          + ("  (none yet — your drone flights would be the first)" if not results else ""))
    for r in results:
        uuid_url = r.get("uuid") or r.get("properties", {}).get("url", "")
        if not uuid_url:
            continue
        name = re.sub(r"[^\w.-]+", "_", (r.get("title") or "untitled")) + ".tif"
        download(uuid_url, out / name)
        print(f"      license: {r.get('properties', {}).get('license', 'CC-BY 4.0')}"
              f"  provider: {r.get('provider', '?')}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default="pathways_basemaps", type=Path)
    a = ap.parse_args()
    fetch_spezialkarte(a.out / "historic" / "sdoum_75k")
    fetch_generalkarte(a.out / "historic" / "gkm_200k")
    fetch_oam(a.out / "oam")
    print("\nDone. Next step for tracing: georeference each 75k sheet in QGIS")
    print("(Raster > Georeferencer, target EPSG:4326, thin-plate-spline against")
    print("church/bridge/confluence points), then load as a raster layer and trace.")


if __name__ == "__main__":
    main()
