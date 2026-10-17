#!/usr/bin/env python3
"""
georeference_sheets.py — georeference Spezialkarte 1:75,000 scans by their
sheet corners, for use as a tracing layer in Plai.

Every Spezialkarte sheet covers an exact graticule cell of 30' longitude
(Ferro) x 15' latitude, so the geographic coordinates of its four corners
follow from the Zone and Kolonne number alone:

    north latitude      = 51°30'  -  Zone  * 15'
    west longitude      = 27°00'  + (Kol-1)* 30'   (Ferro)
    Greenwich longitude = Ferro longitude - 17°40'

What you supply, once per sheet, is the PIXEL position of the four corners
of the printed map frame (the inner neatline, where the graticule ends --
not the paper edge). Read them off in any image viewer that shows the
cursor position (GIMP, IrfanView, `qgis`, even a browser dev-tool).

Workflow (host or laptop; needs the GDAL command-line tools: apt install gdal-bin):

    1.  python3 tools/georeference_sheets.py init  DIR_WITH_SCANS
            writes DIR_WITH_SCANS/sheets.csv, one row per image
    2.  fill in zone, kol and the eight corner-pixel values per row
            IMPORTANT: compare the computed corner coordinates (printed by
            `warp`, and present in the sheet margin -- the sheets print
            their Ferro longitudes) and use the override columns if the
            printed values differ.
    3.  python3 tools/georeference_sheets.py warp  DIR_WITH_SCANS
            -> DIR_WITH_SCANS/georef/<name>.tif        (EPSG:4326, GCP+TPS)
        options:
            --merc            output in EPSG:3857 (web mercator)
            --tiles 8 15      additionally render XYZ tiles with gdal2tiles
                              into DIR_WITH_SCANS/tiles/<name>/  -- these can
                              be served as static files behind the mapservice

Datum: the sheets stand on the Austro-Hungarian datum (Bessel 1841 ellipsoid,
Hermannskogel origin; EPSG:4312 MGI, with longitudes from Ferro). In the
corridor that datum sits some 170 m west and 15-20 m south of WGS84 for the
same numbers -- PROJ itself offers only a "ballpark" (no shift) outside
Austria, so the corners are given in MGI with the Austrian Helmert
parameters stated explicitly (EPSG:1618, "MGI to WGS 84 (3)"), and gdalwarp
shifts them. Extrapolated 600 km east of Austria it is still far better than
no shift; check the result against today's churches and confluences, and
use --datum none to see the unshifted placement.

Accuracy: corner-pinning carries the 1880s survey's own distortion -- expect
tens of metres of local error in high relief. Good for finding the historic
alignment; where a stretch needs precision, refine that sheet in the QGIS
Georeferencer with local control points (churches, bridges, confluences).

sheets.csv columns
    file        image file name (relative to the csv)
    zone        Spezialkarte Zone, e.g. 13
    kol         Kolonne, roman or arabic: XXXI or 31
    nw_x nw_y   pixel of the north-west neatline corner
    ne_x ne_y   ... north-east
    se_x se_y   ... south-east
    sw_x sw_y   ... south-west
    west east north south
                optional overrides, decimal degrees Greenwich (MGI); leave empty
                to use the Zone/Kolonne-derived values
"""

import argparse
import csv
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

FERRO_OFFSET = 17 + 40 / 60          # Ferro = Greenwich + 17°40' (Austrian convention)
# MGI (Bessel 1841, Hermannskogel) with EPSG:1618's Helmert parameters
# written out, so the shift is applied outside Austria's area of use too.
MGI_SRS = ("+proj=longlat +ellps=bessel "
           "+towgs84=577.326,90.129,463.919,5.137,1.474,5.297,2.4232 +no_defs")
IMG_EXT = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}
FIELDS = ["file", "zone", "kol",
          "nw_x", "nw_y", "ne_x", "ne_y", "se_x", "se_y", "sw_x", "sw_y",
          "west", "east", "north", "south"]

ROMAN = {"i": 1, "v": 5, "x": 10, "l": 50, "c": 100}


def roman_to_int(s: str) -> int:
    s = s.strip().lower()
    if s.isdigit():
        return int(s)
    total, prev = 0, 0
    for ch in reversed(s):
        v = ROMAN[ch]
        total += v if v >= prev else -v
        prev = max(prev, v)
    return total


def corners_from_grid(zone: int, kol: int):
    """(west, east, north, south) in decimal degrees Greenwich, MGI datum."""
    north = 51.5 - zone * 0.25
    south = north - 0.25
    west_ferro = 27.0 + (kol - 1) * 0.5
    west = west_ferro - FERRO_OFFSET
    east = west + 0.5
    return west, east, north, south


def frame_ring(src_srs: str, west: float, east: float, north: float, south: float):
    """The frame's corners in WGS84 lon/lat, as a closed ring (gdaltransform)."""
    pts = [(west, north), (east, north), (east, south), (west, south)]
    if src_srs == "EPSG:4326":
        out = pts
    else:
        res = subprocess.run(["gdaltransform", "-s_srs", src_srs, "-t_srs", "EPSG:4326",
                              "-output_xy"],
                             input="".join(f"{x} {y}\n" for x, y in pts),
                             capture_output=True, text=True, check=True).stdout
        out = [tuple(map(float, ln.split()[:2])) for ln in res.splitlines() if ln.strip()]
    return [list(p) for p in out] + [list(out[0])]


def need(cmd: str):
    if shutil.which(cmd) is None:
        sys.exit(f"'{cmd}' not found — install the GDAL tools:  sudo apt install gdal-bin")


def run(args: list[str]):
    print("   $", " ".join(str(a) for a in args))
    subprocess.run([str(a) for a in args], check=True)


# ------------------------------------------------------------------------ init

def cmd_init(d: Path):
    csv_path = d / "sheets.csv"
    if csv_path.exists():
        sys.exit(f"{csv_path} already exists — fill it in, or remove it to start over.")
    images = sorted(p.name for p in d.iterdir() if p.suffix.lower() in IMG_EXT)
    with csv_path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for name in images:
            row = {"file": name}
            # Z13_K31_Bogdan.jpg -> zone 13, kol 31; 14_XXXI_… -> 14, XXXI
            m = (re.match(r"[Zz](\d{1,2})_[Kk]([0-9IVXLivxl]+)_", name)
                 or re.match(r"(\d{1,2})_([IVXLivxl]+)_", name))
            if m:
                row["zone"], row["kol"] = m.group(1), m.group(2).upper()
            w.writerow(row)
    print(f"wrote {csv_path} with {len(images)} row(s).")
    print("Zone and Kolonne are filled in from the file names where they follow")
    print("Z<zone>_K<kol>_<name>; fill in the four corner-pixel pairs, then run: warp")


# ------------------------------------------------------------------------ warp

def cmd_warp(d: Path, merc: bool, tiles: tuple[int, int] | None, datum: str = "mgi"):
    need("gdal_translate")
    need("gdalwarp")
    need("gdaladdo")
    need("gdaltransform")
    if tiles:
        need("gdal2tiles.py") if shutil.which("gdal2tiles.py") else need("gdal2tiles")
    csv_path = d / "sheets.csv"
    if not csv_path.exists():
        sys.exit(f"{csv_path} not found — run 'init' first.")
    out_dir = d / "georef"
    out_dir.mkdir(exist_ok=True)
    srs = "EPSG:3857" if merc else "EPSG:4326"

    with csv_path.open() as f:
        rows = list(csv.DictReader(f))
    done = 0
    for row in rows:
        name = (row.get("file") or "").strip()
        if not name:
            continue
        src = d / name
        missing = [k for k in FIELDS[1:11] if not (row.get(k) or "").strip()]
        if missing:
            print(f"-- {name}: skipped (empty: {', '.join(missing)})")
            continue
        if not src.exists():
            print(f"-- {name}: skipped (file not found)", file=sys.stderr)
            continue

        zone = int(row["zone"])
        kol = roman_to_int(row["kol"])
        c = dict(zip(("west", "east", "north", "south"), corners_from_grid(zone, kol)))
        for key in ("west", "east", "north", "south"):   # per-sheet overrides win
            if (row.get(key) or "").strip():
                c[key] = float(row[key])
        west, east, north, south = c["west"], c["east"], c["north"], c["south"]
        print(f"== {name}  Zone {zone} Kol {kol}")
        print(f"   corners  N {north:.6f}  S {south:.6f}  W {west:.6f}  E {east:.6f}")
        print(f"   check these against the values printed in the sheet margin"
              f" (margin shows Ferro: W {west + FERRO_OFFSET:.4f}  E {east + FERRO_OFFSET:.4f})")

        gcps = []
        for px, py, lon, lat in (
            (row["nw_x"], row["nw_y"], west, north),
            (row["ne_x"], row["ne_y"], east, north),
            (row["se_x"], row["se_y"], east, south),
            (row["sw_x"], row["sw_y"], west, south),
        ):
            gcps += ["-gcp", float(px), float(py), lon, lat]

        stem = re.sub(r"[^\w.-]+", "_", Path(name).stem)
        tmp = out_dir / f"{stem}.gcp.tif"
        cut = out_dir / f"{stem}.frame.geojson"
        out = out_dir / f"{stem}.tif"
        try:
            src_srs = MGI_SRS if datum == "mgi" else "EPSG:4326"
            run(["gdal_translate", "-of", "GTiff", "-a_srs", src_srs, *gcps, src, tmp])
            # Clip to the map frame, so a sheet's paper margin never covers
            # its neighbour: the four corners, shifted as the warp shifts them.
            ring = frame_ring(src_srs, west, east, north, south)
            cut.write_text(json.dumps({"type": "FeatureCollection", "features": [{
                "type": "Feature", "properties": {},
                "geometry": {"type": "Polygon", "coordinates": [ring]}}]}))
            run(["gdalwarp", "-tps", "-r", "bilinear", "-t_srs", srs, "-dstalpha",
                 "-cutline", cut, "-crop_to_cutline",
                 "-overwrite", "-co", "TILED=YES", "-co", "COMPRESS=DEFLATE", tmp, out])
            run(["gdaladdo", "-r", "average", out, "2", "4", "8", "16"])
            if tiles:
                g2t = shutil.which("gdal2tiles.py") or shutil.which("gdal2tiles")
                tile_dir = d / "tiles" / stem
                tile_dir.mkdir(parents=True, exist_ok=True)
                run([g2t, "--xyz", "-z", f"{tiles[0]}-{tiles[1]}",
                     "-r", "bilinear", "-w", "none", out, tile_dir])
        except subprocess.CalledProcessError as e:
            print(f"-- {name}: FAILED ({e}); continuing with the next sheet",
                  file=sys.stderr)
            continue
        finally:
            tmp.unlink(missing_ok=True)
            cut.unlink(missing_ok=True)
        done += 1
    print(f"\n{done} sheet(s) georeferenced into {out_dir}/"
          + (f", tiles in {d / 'tiles'}/" if tiles and done else ""))


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p_init = sub.add_parser("init", help="write a sheets.csv template for a scan directory")
    p_init.add_argument("dir", type=Path)
    p_warp = sub.add_parser("warp", help="georeference every completed row of sheets.csv")
    p_warp.add_argument("dir", type=Path)
    p_warp.add_argument("--merc", action="store_true", help="output EPSG:3857 instead of 4326")
    p_warp.add_argument("--datum", choices=("mgi", "none"), default="mgi",
                        help="mgi (default): shift from the Austro-Hungarian datum to WGS84;"
                             " none: take the sheet's numbers as WGS84")
    p_warp.add_argument("--tiles", nargs=2, type=int, metavar=("ZMIN", "ZMAX"),
                        help="also render XYZ tiles for this zoom range")
    a = ap.parse_args()
    if not a.dir.is_dir():
        sys.exit(f"{a.dir} is not a directory")
    if a.cmd == "init":
        cmd_init(a.dir)
    else:
        cmd_warp(a.dir, a.merc, tuple(a.tiles) if a.tiles else None, a.datum)


if __name__ == "__main__":
    main()
