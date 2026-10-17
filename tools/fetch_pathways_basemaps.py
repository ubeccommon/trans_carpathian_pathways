#!/usr/bin/env python3
"""
fetch_pathways_basemaps.py — download public-domain historic map sheets and
OpenAerialMap imagery for the Hutsul corridor (Trans-Carpathian Pathways).

Runs on the host, from the mapservice checkout, like the planner:

    scp tools/fetch_pathways_basemaps.py ubec-common:/tmp/        # from schiff
    cd /home/ubec/ubec_commons/ubec_mapservice && source tools/hostenv.sh
    python3 /tmp/fetch_pathways_basemaps.py

Downloads into $UBEC_EXCHANGE/basemaps (the mapservice's work area,
/data/ubec_mapservice/exchange, writable by ubec), or --out DATA_DIR;
./pathways_basemaps when UBEC_EXCHANGE is not set:
    historic/sdoum_75k/   Austro-Hungarian Spezialkarte 1:75,000 sheets
                          (Third Military Survey — public domain), from a
                          list of URLs you give with --sheet-urls; without
                          it, the script prints the six corridor sheets to
                          fetch by hand. No crawling: v0.1 crawled the
                          igrek.amzp.pl index blind, and the site began
                          resetting the host's connections.
    historic/gkm_200k/    Generalkarte 1:200,000 overview sheets 42-47, 42-48
                          (from Wikimedia Commons — public domain)
    oam/                  Any CC-BY imagery OpenAerialMap holds for the
                          corridor (currently none — kept so re-runs pick up
                          new uploads, including your own)

Stdlib only. Be gentle: one request at a time, with a pause.
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

UA = {"User-Agent": "TransCarpathianPathways/0.2 (michel@ubec.network; corridor basemap fetch)"}
PAUSE = 2.0  # seconds between requests

# Hutsul corridor, generous: Vorokhta .. Kosiv/Kuty, down past Hryniawa
CORRIDOR_BBOX = (24.3, 47.8, 25.4, 48.5)   # W, S, E, N (Greenwich)

# The corridor's Spezialkarte sheets, by Zone and Kolonne. Each covers
# 15' of latitude by 30' of longitude (Ferro); the bounds below are the
# same arithmetic georeference_sheets.py uses, checked against Wien
# (Zone 13 Kol. XV) and Wels (Zone 13 Kol. X).
# Sheet titles and the alternative numbers (4673 …) as Mapster
# (igrek.amzp.pl) indexes them, read off its index on October 17, 2026.
CORRIDOR_SHEETS = [
    (12, "XXXI",  "Mikuliczyn, Körösmező (4673) — Vorokhta, Yaremche, Mikulychyn"),
    (12, "XXXII", "Kuty (4674) — Kosiv, Kuty, Pistyn"),
    (13, "XXXI",  "Bogdan (4773) — Verkhovyna (east edge), Hoverla, Chornohora"),
    (13, "XXXII", "Wiznitz, Malenicze (4774) — Kryvorivnia, the Cheremosh"),
    (14, "XXXI",  "Ruszpolyana (4873) — southern Chornohora, mostly Romania; optional"),
    (14, "XXXII", "Szipot-kamerale (4874) — Hryniava, Burkut"),
]
FERRO_OFFSET = 17 + 40 / 60
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


def roman(n: str) -> int:
    vals = {"I": 1, "V": 5, "X": 10, "L": 50}
    total, prev = 0, 0
    for ch in reversed(n.upper()):
        v = vals[ch]
        total += v if v >= prev else -v
        prev = max(prev, v)
    return total


def sheet_bounds(zone: int, kol: str):
    north = 51.5 - zone * 0.25
    west = 27.0 + (roman(kol) - 1) * 0.5 - FERRO_OFFSET
    return west, west + 0.5, north - 0.25, north   # W, E, S, N


# ---------------------------------------------------------------- Spezialkarte

def fetch_spezialkarte(out: Path, url_file: Path | None):
    print("\n== Spezialkarte 1:75,000 (Third Military Survey) ==")
    out.mkdir(parents=True, exist_ok=True)
    print("  corridor sheets (Greenwich bounds):")
    for zone, kol, places in CORRIDOR_SHEETS:
        w, e, s, n = sheet_bounds(zone, kol)
        print(f"    Zone {zone:>2} Kol. {kol:<5}  {s:.2f}-{n:.2f} N  {w:.2f}-{e:.2f} E  {places}")
    if url_file is None:
        print(f"""
  No --sheet-urls given, so nothing is fetched. Download the sheets above in
  a browser (on schiff), name each Z<zone>_K<kol>_<name>.jpg, and copy them to
    {out}/
  or put one URL per line in a file and run again with --sheet-urls FILE.""")
        return
    urls = [ln.strip() for ln in url_file.read_text().splitlines()
            if ln.strip() and not ln.lstrip().startswith("#")]
    print(f"  {len(urls)} URL(s) from {url_file}")
    for i, url in enumerate(urls, 1):
        name = urllib.parse.unquote(Path(urllib.parse.urlparse(url).path).name) or f"sheet_{i}.jpg"
        print(f"  [{i}/{len(urls)}]")
        download(url, out / name)


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
    ex = os.environ.get("UBEC_EXCHANGE")
    default_out = Path(ex) / "basemaps" if ex else Path("pathways_basemaps")
    ap.add_argument("--out", default=default_out, type=Path,
                    help=f"download directory (default: {default_out})")
    ap.add_argument("--sheet-urls", type=Path, metavar="FILE",
                    help="file with one Spezialkarte sheet URL per line")
    a = ap.parse_args()
    fetch_spezialkarte(a.out / "historic" / "sdoum_75k", a.sheet_urls)
    fetch_generalkarte(a.out / "historic" / "gkm_200k")
    fetch_oam(a.out / "oam")
    print("\nDone. Next step for tracing: georeference each 75k sheet in QGIS")
    print("(Raster > Georeferencer, target EPSG:4326, thin-plate-spline against")
    print("church/bridge/confluence points), then load as a raster layer and trace.")


if __name__ == "__main__":
    main()
