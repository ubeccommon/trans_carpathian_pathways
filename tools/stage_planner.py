#!/usr/bin/env python3
# Trans-Carpathian Pathways — stage planner, `route`, `corridor`, `find` and `inspect`, v0.9
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Stage planner — one route from a start to an end, a fuzzy band
along it, and the places a pilgrim can reach from it; and a
corridor made of such routes.

The first piece of the stage planner specified in the starting
prompt §6 (the proposal's "spatial algorithm"): the routing core.
Splitting a route into days that end at a host is the next piece
(`stages`), built when the corridor has hosts enough to need it.

What it does, for a start and an end:

1. builds the walkable network in memory (networkx) from
   OpenStreetMap's paths, tracks and roads around the two points;
2. prices every segment by DIN 33466 walking time from the ground
   model GEDTM30 (ascent and descent per direction), and steers by
   the criteria below without changing the time it reports;
3. finds the way — the least road, then the richest way on paths
   within an allowance — and up to two alternatives;
4. draws a band on both sides of it: the land a pilgrim reaches in
   2.5, 5, 7.5 and 10 minutes off the route, walked on the network
   and a little off it — nested rings, densest at the route and
   fading outwards, with the outer edge as the boundary;
5. lists the places inside that reach, in the order the route
   meets them, each with its one-way detour in minutes.

The criteria (starting prompt §6, §7; decisions S-8, S-15):

- The pathway is the way (Michel's word, October 11, 2026): not the
  quickest or the shortest. Roads for vehicles only where no path
  joins the two ends, or links two paths (`MINOR_ROAD_WEIGHT`,
  `MAIN_ROAD_WEIGHT`); then, on paths, the
  richest way — marked trails, the plai over open high ground,
  forest away from settlements, meadows, and the places passed —
  within `WAY_ALLOWANCE` more walking than the most direct way on
  paths (`Q_*`, "The way" below).
- Time is reported, as DIN 33466: 4 km/h on the flat, 300 m/h up,
  500 m/h down; a segment takes the larger of its horizontal and
  vertical times plus half the smaller. The party scales it
  (`PARTY`). It is a limit, never the measure.
- Difficulty: a path harder than the party's SAC grade or less
  visible than its limit is not walked (`PARTY`).
- The border strip (S-8): no segment inside five kilometres of the
  state border, and no place in it listed, until the Curator holds
  the permit route in writing and has done it once
  (`--allow-border-strip`, the Curator's flag).
- Air-raid shelters are never listed (open data spec, class B);
  a shelter is listed only when it is a hikers' kind.

Who uses it — Michel's word, October 11, 2026: it is public.
A pilgrim, a steward, a Curator, anyone, plans directly. The
Curator may save a route as a stretch and manage it, a steward may
save a draft that only the Curator publishes (SP-1), and stretches
are combined into a corridor (`corridor`). Saving is Plai's change,
not this tool's: the tool writes files and nothing else (spec
`docs/specs/PATHWAYS_STAGE_PLANNER_SPEC_v0_3.md`).

`--audience public` (the default) names a published host with its
detour time only — Michel's word, October 11, 2026 (SP-3): no
place, no offer, no kind, no point along the route in kilometres,
and no geometry, so nothing it writes puts a host's place in a file
anyone may pass on (open data spec §2: a host is never a waypoint
in a public file); the host's place stays on Plai's map, public and
clickable (S-1). `--audience curator` lists hosts in full, for the
Curator's own planning.

Licence (OI-P10, closed by the same word): a route is a work
derived from OpenStreetMap. Unsaved, it is an answer, computed and
gone; saved as a stretch, it lives in Plai's `instance_sa` under
ODbL 1.0. Every file it writes carries the ODbL notice and the
GEDTM30 credit. Nothing is written to any database.

Sources:

- `--source postgis` (on the host, after `source
  tools/hostenv.sh` in ubec_mapservice): paths and open places from
  `reference_sa.osm_line` and `osm_point` and the border from
  `reference.admin_unit` in the framework database; published Plai
  places from `instance.entry_public` in `ubec_i_plai`; the ground
  from `$DATA_ROOT/terrain/ground.tif` (tools/terrain.py).
- `--source files`: GeoJSON in EPSG:4326 for the paths
  (`--paths`), the places (`--places`) and the border strip
  (`--border-strip`), and a GeoTIFF for the ground (`--dem`) — for
  testing off the host.

Usage:

    python3 tools/stage_planner.py route \\
        --from "48.1520,24.7910" --to "Tepla Gora" \\
        --party couple --month oct \\
        --out route.geojson --html route.html

A point is "lat,lon" as a map app copies it, or a name: a
published Plai place's title, or a village, peak or other named
place in OSM, in Latin or Cyrillic. To see what a name matches:

    python3 tools/stage_planner.py find "Tepla Gora"

A corridor from stretches, each a file `route` wrote:

    python3 tools/stage_planner.py corridor --name "Hutsul corridor" \\
        stretch_1.geojson stretch_2.geojson --out corridor.geojson

Changelog:
  v0.9 — 2026-10-11 — a road is weighed, not forbidden: six times its
         walking time (a main road fifteen), so a short road linking
         two paths is walked. The absolute rule of v0.6 sent the
         second corridor over a ridge rather than along 150 m of
         village road between two paths at Verkhovyna.
  v0.8 — 2026-10-11 — obvious connections, Michel's word: a path end
         is joined across up to 80 m where the path, carried on the
         way it was heading, meets another way and crosses no river
         or stream; every gap a route walks is listed and marked.
  v0.7, amended 2026-10-11 — a click on the preview's map gives that
         point as lat,lon with its `inspect` command, ready to copy.
  v0.7 — 2026-10-11 — footpaths first, Michel's word: a path or
         footway (the dotted brown line on Plai's map) counts most
         among the qualities, a marked route (the red line) a little;
         a path end within 10 m of another way is joined to it;
         `inspect "lat,lon"` says what way lies there, whether the
         party walks it, and whether it joins the network.
  v0.6 — 2026-10-11 — the pathway is the way, Michel's word: no
         longer the quickest route with paths made cheaper. Roads
         for vehicles only where no path joins (a rule); then the
         richest way on paths — marked trails, plai, forest away
         from settlements, meadows, the places passed, farmsteads —
         within an allowance over the most direct way on paths
         (--allowance, 0.5). Forest and open land from canopy.tif
         when present, else OSM land cover. The quickest way is no
         longer shown; the run says what the way holds.
  v0.5 — 2026-10-11 — after Michel's look at the first corridor:
         hiking paths first, roads for vehicles only when there is
         no other way (roads 4 to 15 times their walking time; a
         marked trail is a path, unless it runs on a main road);
         a start or end joins the nearest point on the nearest
         path, not the nearest junction, and the route is drawn on
         to the point itself; the start and the end are marked; how
         much of the route is on roads is said.
  v0.4, amended 2026-10-11 — after the first run on ubec-common:
         the boundary is written as a LineString, not a LinearRing,
         which is no GeoJSON type and stopped the map page; a
         corridor reads a public stretch whose host has no geometry;
         a place without a name is not named twice by its kind;
         the preview's base map is Plai's own WMS, since OpenStreetMap's
         tile servers refuse a page opened from a file.
  v0.4 — 2026-10-11 — after the first run on ubec-common: a Latin
         name finds a Cyrillic one (Zhyva Khata, Жива Хата), on
         Plai or in OSM, peaks and hills too; several equal matches
         are listed instead of guessed; `find` shows what a name
         matches; `corridor` says plainly when a stretch file is
         missing.
  v0.3, amended 2026-10-11 — SP-4: the numbers adopted as proposed;
         the spec's path, v0.3; a name finds a Plai title that
         contains it, the exact title first.
  v0.3 — 2026-10-11 — SP-3, Michel's word: the public answer names
         published hosts with their detour time only; every place
         carries its order along the route.
  v0.2 — 2026-10-11 — public by default, Michel's word: the
         audiences are public and curator; `route` writes a stretch
         (its ends, party and criteria with it); `corridor` joins
         stretches into one band, one boundary and one list.
  v0.1 — 2026-10-11 — initial: route, alternatives, band, places.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

import networkx as nx
import numpy as np
import shapely
from pyproj import Transformer
from shapely import wkb
from shapely.geometry import (LineString, MultiLineString, Point,
                              mapping, shape)
from shapely.ops import substring, unary_union
from shapely.strtree import STRtree

VERSION = "0.9"

# ── Criteria ───────────────────────────────────────────────────
# The party's paces and limits, the band and the reach are as
# proposed and adopted on Michel's word, October 11, 2026 (SP-4).
# The measure of the way below is his word the same day; its weights
# (Q_*, WAY_ALLOWANCE) are Claude's proposal until he has looked at
# a corridor drawn with them. A change is his or the Curator's word.
# Each number is named so it can be changed in one place.

DIN_FLAT_KMH = 4.0          # DIN 33466
DIN_UP_MH = 300.0
DIN_DOWN_MH = 500.0

# ── The way ─────────────────────────────────────────────────────
# Michel's word, October 11, 2026, after the first corridor: "It's
# not a question of saving time or taking the shortest path ... the
# pathway is the way." So the planner does not look for the quickest
# route with paths made cheaper. It looks, in this order, for:
#
#   1. as little road for vehicles as the paths allow — a road
#      weighs MINOR_ROAD_WEIGHT (a main road MAIN_ROAD_WEIGHT) times
#      its walking time, so a short road linking two paths is walked
#      and a long road is not where paths go round it. (An absolute
#      rule, tried first, sent the second corridor over a ridge for
#      kilometres rather than walk 150 m of village road between two
#      paths at Verkhovyna.)
#   2. among the ways on paths, the richest — marked trails, the old
#      plai over open high ground, forest away from settlements,
#      meadows, and the places passed: springs, chapels and crosses,
#      viewpoints, waterfalls, hosts and the places stewards enter,
#      farmsteads — within WAY_ALLOWANCE more walking than the most
#      direct way on paths. Time is a limit, never the measure.
#
# What stewards find when they walk a path they enter on Plai as a
# place; every Plai place counts as an encounter (Q_PLAI_PLACE).

# What each highway is to a walker: a path, a road for vehicles, or
# never walked.
PATH_HIGHWAYS = {"path", "footway", "bridleway", "steps", "pedestrian",
                 "track", "cycleway"}
MINOR_ROADS = {"living_street", "service", "unclassified", "residential",
               "road"}
MAIN_ROADS = {"tertiary", "tertiary_link", "secondary", "secondary_link",
              "primary", "primary_link"}
NEVER_WALKED = {"trunk", "trunk_link", "motorway", "motorway_link",
                "construction", "proposed", "abandoned", "raceway",
                "bus_guideway", "platform"}
# A highway value not listed is a road; a track of grade1 is paved, a
# road. A marked hiking or foot route is a path wherever it follows a
# minor road or a track; on a main road it is still a road.
MINOR_ROAD_WEIGHT = 6.0      # a village, service or unclassified road
MAIN_ROAD_WEIGHT = 15.0      # tertiary, secondary, primary
WAY_ALLOWANCE = 0.5          # up to half again the most direct way

# How rich a path is, 0 to Q_MAX: each quality over the share of the
# path it covers; each place within ENCOUNTER_M over ENCOUNTER_SPAN_M
# of path, so a place enriches the path that passes it, not a whole
# long path.
# Footpaths come first: Michel's word, October 11, 2026, on the
# second corridor — the dotted brown line on Plai's map (path,
# footway) has priority over the red line (a marked hiking route),
# which here often runs on tracks and roads.
Q_FOOTPATH = 0.45            # highway=path, footway, bridleway, steps
FOOTPATHS = {"path", "footway", "bridleway", "steps"}
Q_MARKED = 0.10              # a marked hiking or foot route
Q_PLAI = 0.30                # open land at or above PLAI_MIN_ELE
PLAI_MIN_ELE = 1000.0        # metres, ground model
Q_FOREST = 0.15              # forest at least SETTLEMENT_GAP_M away
SETTLEMENT_GAP_M = 300.0     #   from a village, hamlet or town
Q_MEADOW = 0.10              # open land below PLAI_MIN_ELE
OPEN_MAX_M = 3.0             # canopy.tif: lower is open land
FOREST_MIN_M = 8.0           # canopy.tif: higher is forest
Q_PLACE = {"spring or water": 0.6, "church, chapel or cross": 0.6,
           "viewpoint": 0.6, "waterfall": 0.6, "peak": 0.4,
           "mountain hut": 0.4, "hikers' shelter": 0.3,
           "heritage": 0.4, "museum": 0.3}
Q_PLAI_PLACE = 0.8           # a place on Plai: a host, a steward's find
Q_FARMSTEAD = 0.3            # an isolated dwelling or farm in OSM
Q_MAX = 0.9
ENCOUNTER_M = 100.0
ENCOUNTER_SPAN_M = 200.0
# OSM paths often stop a few metres short of the way they meet; an
# end within JOIN_GAP_M of another way is joined to it, so a path is
# not a dead end only because it was drawn short.
JOIN_GAP_M = 10.0
# Michel's word, October 11, 2026, looking at a dotted path that
# stopped short of Zhiva Khata's: join an obvious connection within a
# search radius. A path end is joined across up to JOIN_OBVIOUS_M when
# the path, carried on the way it was heading, meets the other way
# (within JOIN_ANGLE_DEG) and the gap crosses no river or stream.
# Every gap a route uses is listed and marked, for a steward to check
# on the ground and for OSM to be mended.
JOIN_OBVIOUS_M = 80.0
JOIN_ANGLE_DEG = 60.0
SETTLEMENT_RADIUS_M = {"city": 2500.0, "town": 1200.0,
                       "village": 500.0, "hamlet": 250.0,
                       "suburb": 500.0}

SAC = ["hiking", "mountain_hiking", "demanding_mountain_hiking",
       "alpine_hiking", "demanding_alpine_hiking",
       "difficult_alpine_hiking"]
VISIBILITY = ["excellent", "good", "intermediate", "bad",
              "horrible", "no"]


@dataclass(frozen=True)
class Party:
    pace: float          # multiplies DIN time
    max_sac: str
    max_visibility: str


PARTY = {
    "solo":   Party(1.00, "demanding_mountain_hiking", "bad"),
    "couple": Party(1.00, "demanding_mountain_hiking", "bad"),
    "group":  Party(1.15, "mountain_hiking", "intermediate"),
    "family": Party(1.35, "mountain_hiking", "intermediate"),
}

BAND_MINUTES = (2.5, 5.0, 7.5, 10.0)   # rings, inner to outer
BAND_OPACITY = (0.30, 0.20, 0.12, 0.07)
PATH_HALF_WIDTH_M = 35.0    # the band around a walked line
OFF_PATH_M_PER_MIN = 30.0   # ~1.8 km/h across meadow or forest
OFF_PATH_CAP_M = 200.0      # never further than this off a path
BAND_STEP_M = 40.0          # how finely reached paths are sampled
SNAP_WARN_M = 500.0
BORDER_STRIP_M = 5000.0     # S-8
SAMPLE_M = 30.0             # the DEM's own resolution

OSM_NOTICE = "© OpenStreetMap contributors, ODbL 1.0"

# The base map under a preview: Plai's WMS, bottom layer first.
PLAI_WMS = "https://mapservice.ubec.network/wms/?map=plai"
PLAI_WMS_LAYERS = ("osm_area", "terrain_hillshade", "osm_line",
                   "osm_route", "osm_names")
GEDTM_CREDIT = ("Ground heights: GEDTM30 v1.2, Ho et al. 2025, "
                "PeerJ 13:e19673, CC BY 4.0")

# Open places worth a detour (class B of the open data spec).
# A shelter only when it is a hikers' kind: never an air-raid one.
HIKERS_SHELTERS = {"basic_hut", "lean_to", "weather_shelter",
                   "rock_shelter", "picnic_shelter"}


def open_place_kind(tags: dict) -> str | None:
    """The kind of an OSM point worth listing, or None."""
    if (tags.get("military") or tags.get("bunker_type")
            or tags.get("building") == "bunker"
            or tags.get("emergency") or "air_raid" in json.dumps(tags)):
        return None
    t, n, a, h = (tags.get("tourism"), tags.get("natural"),
                  tags.get("amenity"), tags.get("historic"))
    if t == "viewpoint":
        return "viewpoint"
    if n == "spring" or a == "drinking_water" or a == "water_point":
        return "spring or water"
    if n == "peak":
        return "peak"
    if n in ("waterfall",) or tags.get("waterway") == "waterfall":
        return "waterfall"
    if t in ("alpine_hut", "wilderness_hut"):
        return "mountain hut"
    if a == "shelter":
        return ("hikers' shelter"
                if tags.get("shelter_type") in HIKERS_SHELTERS else None)
    if a == "place_of_worship" or h in ("wayside_cross",
                                        "wayside_shrine"):
        return "church, chapel or cross"
    if h in ("monument", "memorial", "archaeological_site", "ruins",
             "castle", "building", "manor", "mill"):
        return "heritage"
    if t == "museum":
        return "museum"
    return None


# ── Geometry helpers ───────────────────────────────────────────

TO_3035 = Transformer.from_crs(4326, 3035, always_xy=True)
TO_4326 = Transformer.from_crs(3035, 4326, always_xy=True)


def _apply(tf: Transformer, geom):
    return shapely.transform(
        geom, lambda c: np.column_stack(tf.transform(c[:, 0], c[:, 1])))


def to_3035(geom):
    return _apply(TO_3035, geom)


def to_4326(geom):
    return _apply(TO_4326, geom)


def parse_latlon(text: str) -> Point | None:
    parts = text.replace(";", ",").split(",")
    if len(parts) != 2:
        return None
    try:
        lat, lon = float(parts[0]), float(parts[1])
    except ValueError:
        return None
    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
        return None
    return Point(*TO_3035.transform(lon, lat))


def din_minutes(length_m: float, up_m: float, down_m: float) -> float:
    th = length_m / 1000.0 / DIN_FLAT_KMH
    tv = up_m / DIN_UP_MH + down_m / DIN_DOWN_MH
    return 60.0 * (max(th, tv) + min(th, tv) / 2.0)


# ── Names ──────────────────────────────────────────────────────
# A Latin spelling finds a Cyrillic name: both are brought to one
# loose key. Cyrillic is transliterated (the Ukrainian national
# system of 2010, with the Russian letters a map may carry), then
# the spellings that differ between systems are folded together —
# h and g ("Hora", "Gora"), kh and h, zh and z, y and i — so
# "Tepla Gora" meets Тепла Гора and "Zhyva Khata" meets Жива Хата.

TRANSLIT = {
    "а": "a", "б": "b", "в": "v", "г": "h", "ґ": "g", "д": "d",
    "е": "e", "є": "ie", "ж": "zh", "з": "z", "и": "y", "і": "i",
    "ї": "i", "й": "i", "к": "k", "л": "l", "м": "m", "н": "n",
    "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u",
    "ф": "f", "х": "kh", "ц": "ts", "ч": "ch", "ш": "sh",
    "щ": "shch", "ь": "", "ю": "iu", "я": "ia", "'": "", "’": "",
    "ʼ": "", "ы": "y", "э": "e", "ё": "e", "ъ": "",
}
FOLD = (("shch", "s"), ("kh", "h"), ("zh", "z"), ("ts", "c"),
        ("ch", "c"), ("sh", "s"), ("g", "h"), ("w", "v"),
        ("y", "i"), ("j", "i"), ("ie", "e"), ("iu", "u"),
        ("ia", "a"))


def loose(text: str) -> str:
    import unicodedata
    t = "".join(TRANSLIT.get(c, c) for c in text.lower())
    t = unicodedata.normalize("NFKD", t)
    t = "".join(c for c in t if c.isascii() and c.isalnum())
    for a, b in FOLD:
        t = t.replace(a, b)
    return t


@dataclass
class Candidate:
    names: list                  # every name it carries
    kind: str
    source: str
    geom: Point                  # EPSG:3035

    def score(self, text: str) -> int:
        """3 a name exactly; 2 the same loose key; 1 a name that
        contains it; 0 no match."""
        low, key = text.strip().lower(), loose(text)
        names = [n for n in self.names if n]
        if any(n.lower() == low for n in names):
            return 3
        keys = [loose(n) for n in names]
        if key and key in keys:
            return 2
        if key and len(key) >= 4 and any(key in k for k in keys):
            return 1
        return 0


def ranked(cands: list, text: str) -> list:
    scored = [(c.score(text), c) for c in cands]
    scored = [(sc, c) for sc, c in scored if sc > 0]
    scored.sort(key=lambda x: (-x[0], x[1].source != "plai",
                               len(x[1].names[0] or "")))
    return scored


def latlon(p: Point) -> str:
    lon, lat = TO_4326.transform(p.x, p.y)
    return f"{lat:.5f},{lon:.5f}"


# ── Data ───────────────────────────────────────────────────────

@dataclass
class Way:
    osm_id: str
    name: str | None
    tags: dict
    geom: MultiLineString        # EPSG:3035


@dataclass
class Place:
    pid: str
    name: str
    kind: str
    source: str                  # "plai" or "osm"
    geom: Point                  # EPSG:3035
    is_host: bool = False
    extra: dict = field(default_factory=dict)


class Ground:
    """Heights from a GeoTIFF in EPSG:3035, bilinear; flat if none."""

    def __init__(self, path: Path | None, bounds):
        self.arr = None
        self.path = path
        if path is None or not path.exists():
            return
        import rasterio
        from rasterio.windows import from_bounds
        with rasterio.open(path) as ds:
            if ds.crs and ds.crs.to_epsg() != 3035:
                sys.exit(f"{path}: expected EPSG:3035, got {ds.crs}")
            minx, miny, maxx, maxy = bounds
            win = from_bounds(minx - 100, miny - 100, maxx + 100,
                              maxy + 100, ds.transform).round_offsets(
                              ).round_lengths()
            self.arr = ds.read(1, window=win, boundless=True,
                               fill_value=np.nan).astype("float64")
            if ds.nodata is not None:
                self.arr[self.arr == ds.nodata] = np.nan
            self.tf = ds.window_transform(win)

    @property
    def known(self) -> bool:
        return self.arr is not None

    def heights(self, xs: np.ndarray, ys: np.ndarray) -> np.ndarray:
        if self.arr is None:
            return np.zeros(len(xs))
        inv = ~self.tf
        cols, rows = inv * (xs, ys)
        cols, rows = np.asarray(cols) - 0.5, np.asarray(rows) - 0.5
        c0 = np.clip(np.floor(cols).astype(int), 0,
                     self.arr.shape[1] - 2)
        r0 = np.clip(np.floor(rows).astype(int), 0,
                     self.arr.shape[0] - 2)
        fc, fr = np.clip(cols - c0, 0, 1), np.clip(rows - r0, 0, 1)
        a = self.arr
        z = (a[r0, c0] * (1 - fc) * (1 - fr) + a[r0, c0 + 1] * fc
             * (1 - fr) + a[r0 + 1, c0] * (1 - fc) * fr
             + a[r0 + 1, c0 + 1] * fc * fr)
        return np.nan_to_num(z, nan=float(np.nanmean(z))
                             if np.isfinite(z).any() else 0.0)


class PostgisSource:
    def __init__(self, instance_db: str):
        import psycopg
        self.fw = psycopg.connect(connect_timeout=5)
        self.inst_db = instance_db
        self.psycopg = psycopg

    def ways(self, bbox):
        sql = """
            SELECT osm_type || osm_id, name, tags, ST_AsBinary(geom)
              FROM reference_sa.osm_line
             WHERE geom && ST_MakeEnvelope(%s, %s, %s, %s, 3035)
               AND (tags ? 'highway'
                    OR (osm_type = 'R'
                        AND tags->>'route' IN ('hiking', 'foot')))"""
        with self.fw.cursor() as cur:
            cur.execute(sql, bbox)
            for oid, name, tags, g in cur:
                geom = wkb.loads(bytes(g))
                yield Way(oid, name, tags, geom)

    def waterways(self, bbox):
        """Rivers and streams, which a joined gap may not cross."""
        with self.fw.cursor() as cur:
            cur.execute("""
                SELECT ST_AsBinary(geom) FROM reference_sa.osm_line
                 WHERE geom && ST_MakeEnvelope(%s, %s, %s, %s, 3035)
                   AND tags->>'waterway' IN ('river', 'stream', 'canal')""",
                        bbox)
            geoms = [wkb.loads(bytes(g)) for (g,) in cur]
        return unary_union(geoms) if geoms else None

    def osm_places(self, bbox):
        sql = """
            SELECT osm_id, name, tags, ST_AsBinary(geom)
              FROM reference_sa.osm_point
             WHERE geom && ST_MakeEnvelope(%s, %s, %s, %s, 3035)
               AND (tags ?| array['tourism', 'natural', 'amenity',
                                  'historic', 'waterway'])"""
        with self.fw.cursor() as cur:
            cur.execute(sql, bbox)
            for oid, name, tags, g in cur:
                kind = open_place_kind(tags)
                if kind:
                    yield Place(f"osm:N{oid}", name or kind, kind,
                                "osm", wkb.loads(bytes(g)),
                                extra={"osm": f"node/{oid}"})

    def plai_places(self, bbox):
        sql = """
            SELECT id, title, location_type, category, offers, season,
                   is_host, ST_AsBinary(ST_Transform(geom, 3035))
              FROM instance.entry_public
             WHERE ST_Transform(geom, 3035)
                   && ST_MakeEnvelope(%s, %s, %s, %s, 3035)"""
        try:
            conn = self.psycopg.connect(dbname=self.inst_db,
                                        connect_timeout=5)
        except self.psycopg.Error as e:
            print(f"stage_planner: Plai places not read ({e})",
                  file=sys.stderr)
            return
        with conn, conn.cursor() as cur:
            cur.execute(sql, bbox)
            for (eid, title, ltype, cat, offers, season, is_host,
                 g) in cur:
                yield Place(f"plai:{eid}", title, ltype or cat, "plai",
                            wkb.loads(bytes(g)), bool(is_host),
                            {"category": cat, "offers": offers,
                             "season": season})

    def landscape(self, bbox, ground: "Ground") -> "Landscape":
        """Villages and farmsteads from osm_point, land cover from
        osm_polygon (used only when canopy.tif is absent), and the
        canopy beside the ground model."""
        env = "ST_MakeEnvelope(%s, %s, %s, %s, 3035)"
        land = Landscape()
        canopy = ground.path.with_name("canopy.tif") if ground.path else None
        if canopy and canopy.exists():
            land.canopy = Ground(canopy, bbox)
        # With the canopy, OSM land cover is needed for settlements only.
        cover_kinds = ("('residential', 'farmyard')" if land.canopy
                       else "('residential', 'farmyard', 'forest', "
                            "'meadow', 'grass')")
        natural = ("('none')" if land.canopy else
                   "('wood', 'grassland', 'heath', 'fell', 'scrub')")
        settled, points = [], []
        with self.fw.cursor() as cur:
            cur.execute(f"""
                SELECT tags->>'place', ST_AsBinary(geom)
                  FROM reference_sa.osm_point
                 WHERE geom && {env}
                   AND tags->>'place' IN ('city', 'town', 'village',
                       'hamlet', 'suburb', 'isolated_dwelling', 'farm')""",
                        bbox)
            for kind, g in cur:
                pt = wkb.loads(bytes(g))
                if kind in SETTLEMENT_RADIUS_M:
                    settled.append(pt.buffer(SETTLEMENT_RADIUS_M[kind]))
                else:
                    points.append((pt, Q_FARMSTEAD))
            cur.execute(f"""
                SELECT coalesce(tags->>'landuse', tags->>'natural'),
                       ST_AsBinary(ST_Intersection(geom, {env}))
                  FROM reference_sa.osm_polygon
                 WHERE geom && {env}
                   AND (tags->>'landuse' IN {cover_kinds}
                        OR tags->>'natural' IN {natural})""", bbox * 2)
            cover = {"settled": [], "open": [], "forest": []}
            for kind, g in cur:
                poly = wkb.loads(bytes(g))
                if kind in ("residential", "farmyard"):
                    cover["settled"].append(poly)
                elif kind in ("forest", "wood"):
                    cover["forest"].append(poly)
                else:
                    cover["open"].append(poly)
        settled += [p.buffer(SETTLEMENT_GAP_M) for p in cover["settled"]]
        land.settled = unary_union(settled) if settled else None
        land.open_land = unary_union(cover["open"]) if cover["open"] else None
        land.forest = unary_union(cover["forest"]) if cover["forest"] else None
        land.points = points
        return land

    def border_strip(self, bbox, width_m):
        sql = """
            WITH env AS (
                SELECT ST_MakeEnvelope(%s, %s, %s, %s, 3035) AS e),
            ua AS (
                SELECT ST_Union(geom) AS g FROM reference.admin_unit
                 WHERE country = 'UA' AND level = 'country')
            SELECT ST_AsBinary(ST_Intersection(ua.g, ST_Buffer(
                       ST_Intersection(ST_Boundary(ua.g),
                                       ST_Expand(env.e, %s)), %s)))
              FROM ua, env WHERE ua.g IS NOT NULL"""
        with self.fw.cursor() as cur:
            cur.execute(sql, (*bbox, width_m, width_m))
            row = cur.fetchone()
        if not row or row[0] is None:
            return None
        return wkb.loads(bytes(row[0]))

    # Plai's extent in the Ukrainian Carpathians (tools/terrain.py),
    # where a name is looked for.
    EXTENT = (22.1, 47.7, 26.0, 49.6)

    def candidates(self, text: str) -> list:
        out = []
        try:
            conn = self.psycopg.connect(dbname=self.inst_db,
                                        connect_timeout=5)
            with conn, conn.cursor() as cur:
                cur.execute("""SELECT title, location_type,
                                      ST_AsBinary(ST_Transform(geom, 3035))
                                 FROM instance.entry_public""")
                for title, ltype, g in cur:
                    out.append(Candidate([title], ltype or "Plai place",
                                         "plai", wkb.loads(bytes(g))))
        except self.psycopg.Error as e:
            print(f"stage_planner: Plai places not read ({e})",
                  file=sys.stderr)
        x0, y0 = TO_3035.transform(self.EXTENT[0], self.EXTENT[1])
        x1, y1 = TO_3035.transform(self.EXTENT[2], self.EXTENT[3])
        with self.fw.cursor() as cur:
            cur.execute("""
                SELECT name, tags->>'name:uk', tags->>'name:en',
                       tags->>'name:ru', tags->>'alt_name',
                       tags->>'old_name',
                       coalesce(tags->>'place', tags->>'natural',
                                tags->>'tourism', tags->>'historic',
                                tags->>'amenity'),
                       ST_AsBinary(geom)
                  FROM reference_sa.osm_point
                 WHERE geom && ST_MakeEnvelope(%s, %s, %s, %s, 3035)
                   AND name IS NOT NULL
                   AND (tags ? 'place'
                        OR tags->>'natural' IN ('peak', 'hill', 'saddle',
                                                'ridge', 'spring')
                        OR tags ? 'tourism' OR tags ? 'historic'
                        OR tags->>'amenity' = 'place_of_worship')""",
                        (min(x0, x1), min(y0, y1), max(x0, x1),
                         max(y0, y1)))
            for (*names, kind, g) in cur:
                out.append(Candidate(names, kind or "place", "osm",
                                     wkb.loads(bytes(g))))
        return out


class FileSource:
    def __init__(self, paths: Path, places: Path | None,
                 strip: Path | None, areas: Path | None = None):
        self.paths, self.places_f, self.strip_f = paths, places, strip
        self.areas_f = areas
        self._places = None

    @staticmethod
    def _features(path: Path):
        return json.loads(path.read_text(encoding="utf-8"))["features"]

    @staticmethod
    def _tags(props: dict) -> dict:
        tags = props.get("tags")
        if isinstance(tags, str):
            tags = json.loads(tags)
        return dict(tags) if tags else {k: v for k, v in props.items()
                                        if isinstance(v, str)}

    def ways(self, bbox):
        box = _box(bbox)
        for i, f in enumerate(self._features(self.paths)):
            g = to_3035(shape(f["geometry"]))
            if not g.intersects(box):
                continue
            if g.geom_type == "LineString":
                g = MultiLineString([g])
            props = f.get("properties") or {}
            tags = self._tags(props)
            yield Way(str(props.get("osm_id", f"f{i}")),
                      tags.get("name"), tags, g)

    def waterways(self, bbox):
        box = _box(bbox)
        geoms = []
        for f in self._features(self.paths):
            tags = self._tags(f.get("properties") or {})
            if tags.get("waterway") in ("river", "stream", "canal"):
                g = to_3035(shape(f["geometry"]))
                if g.intersects(box):
                    geoms.append(g)
        return unary_union(geoms) if geoms else None

    def _all_places(self):
        if self._places is None:
            self._places = []
            if self.places_f:
                for i, f in enumerate(self._features(self.places_f)):
                    props = f.get("properties") or {}
                    tags = self._tags(props)
                    is_host = bool(props.get("is_host"))
                    kind = (props.get("kind") or open_place_kind(tags)
                            or ("host" if is_host else None))
                    if not kind:
                        continue
                    name = props.get("title") or tags.get("name") or kind
                    self._places.append(Place(
                        str(props.get("id", f"p{i}")), name, kind,
                        props.get("source", "file"),
                        to_3035(shape(f["geometry"])), is_host,
                        {k: props[k] for k in ("offers", "season",
                                               "category") if k in props}))
        return self._places

    def osm_places(self, bbox):
        box = _box(bbox)
        return [p for p in self._all_places() if p.geom.within(box)]

    def plai_places(self, bbox):
        return []

    def landscape(self, bbox, ground: "Ground") -> "Landscape":
        """From the places file: villages and farmsteads by their
        place tag; from --areas, land cover polygons tagged as in OSM;
        a canopy.tif beside the ground file if there is one."""
        land = Landscape()
        settled, points = [], []
        for f in self._features(self.places_f) if self.places_f else []:
            tags = self._tags(f.get("properties") or {})
            kind = tags.get("place")
            if kind in SETTLEMENT_RADIUS_M:
                settled.append(to_3035(shape(f["geometry"])).buffer(
                    SETTLEMENT_RADIUS_M[kind]))
            elif kind in ("isolated_dwelling", "farm"):
                points.append((to_3035(shape(f["geometry"])), Q_FARMSTEAD))
        cover = {"settled": [], "open": [], "forest": []}
        for f in self._features(self.areas_f) if self.areas_f else []:
            tags = self._tags(f.get("properties") or {})
            kind = tags.get("landuse") or tags.get("natural")
            poly = to_3035(shape(f["geometry"]))
            if kind in ("residential", "farmyard"):
                cover["settled"].append(poly.buffer(SETTLEMENT_GAP_M))
            elif kind in ("forest", "wood"):
                cover["forest"].append(poly)
            elif kind in ("meadow", "grass", "grassland", "heath", "fell",
                          "scrub"):
                cover["open"].append(poly)
        settled += cover["settled"]
        land.settled = unary_union(settled) if settled else None
        land.open_land = unary_union(cover["open"]) if cover["open"] else None
        land.forest = unary_union(cover["forest"]) if cover["forest"] else None
        land.points = points
        if ground.path:
            canopy = ground.path.with_name("canopy.tif")
            if canopy.exists():
                land.canopy = Ground(canopy, bbox)
        return land

    def border_strip(self, bbox, width_m):
        if not self.strip_f:
            return None
        return unary_union([to_3035(shape(f["geometry"]))
                            for f in self._features(self.strip_f)])

    def candidates(self, text: str) -> list:
        out = []
        for f in self._features(self.places_f) if self.places_f else []:
            props = f.get("properties") or {}
            tags = self._tags(props)
            names = [props.get("title"), tags.get("name"),
                     tags.get("name:uk"), tags.get("name:en")]
            if any(names):
                out.append(Candidate(
                    [n for n in names if n],
                    tags.get("place") or props.get("kind") or "place",
                    props.get("source", "file"),
                    to_3035(shape(f["geometry"]))))
        return out


def _box(bbox):
    from shapely.geometry import box
    return box(*bbox)


# ── The network ────────────────────────────────────────────────

def why_not(tags: dict, party: Party) -> str | None:
    """Why this party does not walk a way, or None if it does."""
    hw = tags.get("highway")
    if hw is None:
        return "not a highway in OSM"
    if hw in NEVER_WALKED:
        return f"highway={hw} is never walked"
    foot = tags.get("foot")
    if foot == "no":
        return "foot=no"
    if (tags.get("access") in ("no", "private")
            and foot not in ("yes", "designated", "permissive")):
        return f"access={tags.get('access')}"
    sac = tags.get("sac_scale")
    if sac in SAC and SAC.index(sac) > SAC.index(party.max_sac):
        return f"sac_scale={sac} is harder than this party walks"
    vis = tags.get("trail_visibility")
    if (vis in VISIBILITY
            and VISIBILITY.index(vis) > VISIBILITY.index(
                party.max_visibility)):
        return f"trail_visibility={vis} is fainter than this party walks"
    return None


def walkable(tags: dict, party: Party) -> str | None:
    """"path", "minor" (a minor road), "main" (a main road), or None
    if not walked by this party."""
    if why_not(tags, party):
        return None
    hw = tags.get("highway")
    if hw == "track" and tags.get("tracktype") == "grade1":
        return "minor"
    if hw in PATH_HIGHWAYS:
        return "path"
    if hw in MAIN_ROADS:
        return "main"
    return "minor"


def _insert_vertex(coords: list, pt: Point) -> tuple:
    """Put pt into a line's coordinates where it lies along it; the
    vertex used, existing or new."""
    line = LineString(coords)
    d = line.project(pt)
    acc = 0.0
    for i in range(1, len(coords)):
        seg = math.dist(coords[i - 1], coords[i])
        if acc + seg >= d:
            if d - acc < 0.1:
                return coords[i - 1]
            if acc + seg - d < 0.1:
                return coords[i]
            q = line.interpolate(d)
            coords.insert(i, (q.x, q.y))
            return (q.x, q.y)
        acc += seg
    return coords[-1]


def _heading(coords: list, at_end: bool):
    """The direction a line leaves by at one end, as a unit vector,
    measured over its last 30 m or so."""
    pts = coords[::-1] if at_end else coords
    x0, y0 = pts[0]
    for x, y in pts[1:]:
        if math.dist((x0, y0), (x, y)) >= 30.0:
            break
    d = math.dist((x0, y0), (x, y))
    return None if d < 0.5 else ((x0 - x) / d, (y0 - y) / d)


def join_dangling(parts: list, water=None) -> int:
    """Join path ends that meet nothing. Within JOIN_GAP_M, to the
    nearest way; within JOIN_OBVIOUS_M, only an obvious connection:
    ahead of the path (JOIN_ANGLE_DEG) and across no water. parts are
    [coords, tags, osm_id, kind], changed in place; a connector is a
    way of highway "gap". Returns how many were joined."""
    count: dict = {}
    for coords, *_ in parts:
        for c in {_key(c) for c in coords}:
            count[c] = count.get(c, 0) + 1
    lines = [LineString(c) for c, *_ in parts]
    tree = STRtree(lines)
    if water is not None and not water.is_empty:
        shapely.prepare(water)
    else:
        water = None
    cos_max = math.cos(math.radians(JOIN_ANGLE_DEG))
    joined = []
    for i, (coords, tags, oid, kind) in enumerate(parts):
        for at_end, end in ((False, coords[0]), (True, coords[-1])):
            if count.get(_key(end), 0) > 1:
                continue
            pt = Point(end)
            heading = _heading(coords, at_end)
            options = []
            for j in tree.query(pt, predicate="dwithin",
                                distance=JOIN_OBVIOUS_M):
                if j == i:
                    continue
                on = lines[j].interpolate(lines[j].project(pt))
                d = on.distance(pt)
                if d > JOIN_GAP_M:
                    if kind != "path" or heading is None:
                        continue
                    vx, vy = (on.x - pt.x) / d, (on.y - pt.y) / d
                    if vx * heading[0] + vy * heading[1] < cos_max:
                        continue
                    if water is not None and water.intersects(
                            LineString([end, (on.x, on.y)])):
                        continue
                options.append((d, j))
            if not options:
                continue
            d, j = min(options)
            at = _insert_vertex(parts[j][0], pt)
            if math.dist(at, end) >= 0.1:
                joined.append([[tuple(end), tuple(at)],
                               {"highway": "gap",
                                "gap_m": round(math.dist(at, end))},
                               f"gap:{oid}", "path"])
            count[_key(end)] = 2
    parts.extend(joined)
    return len(joined)


def _key(xy) -> tuple[int, int]:
    return (round(xy[0] * 10), round(xy[1] * 10))   # 0.1 m


@dataclass
class Landscape:
    """What makes a path rich, in EPSG:3035."""
    marked: object = None        # hiking and foot route relations
    open_land: object = None     # OSM land cover, when no canopy
    forest: object = None        # OSM land cover, when no canopy
    settled: object = None       # within SETTLEMENT_GAP_M of a village
    canopy: "Ground" = None      # surface minus ground, if present
    points: list = field(default_factory=list)   # (Point, weight)

    def prepare(self):
        self._tree = STRtree([p for p, _ in self.points]) \
            if self.points else None
        for name in ("marked", "open_land", "forest", "settled"):
            g = getattr(self, name)
            if g is not None and not g.is_empty:
                shapely.prepare(g)
            else:
                setattr(self, name, None)

    def quality(self, seg: LineString, xs, ys, zs) -> tuple:
        """The path's richness, 0 to Q_MAX, and metres of each kind."""
        n = len(xs)
        share = lambda mask: float(np.count_nonzero(mask)) / n
        inside = lambda g: (shapely.contains_xy(g, xs, ys) if g is not None
                            else np.zeros(n, bool))
        marked = inside(self.marked)
        if self.canopy is not None and self.canopy.known:
            c = self.canopy.heights(xs, ys)
            open_ = c < OPEN_MAX_M
            forest = c >= FOREST_MIN_M
        else:
            open_ = inside(self.open_land)
            forest = inside(self.forest)
        settled = inside(self.settled)
        high = zs >= PLAI_MIN_ELE
        plai = open_ & high
        meadow = open_ & ~high
        wild = forest & ~settled
        q = (Q_MARKED * share(marked) + Q_PLAI * share(plai)
             + Q_FOREST * share(wild) + Q_MEADOW * share(meadow))
        if self._tree is not None:
            near = self._tree.query(seg, predicate="dwithin",
                                    distance=ENCOUNTER_M)
            span = min(1.0, ENCOUNTER_SPAN_M / max(seg.length, 1.0))
            q += sum(self.points[i][1] for i in near) * span
        L = seg.length
        kinds = {"marked": share(marked) * L, "plai": share(plai) * L,
                 "forest": share(wild) * L, "meadow": share(meadow) * L}
        return min(q, Q_MAX), kinds


@dataclass
class Network:
    G: nx.DiGraph
    xy: dict                     # node -> (x, y)
    lines: dict                  # edge id -> LineString (u to v)
    tree: STRtree
    node_ids: list
    ground: "Ground" = None
    pace: float = 1.0
    land: Landscape = None


def profile(seg: LineString, ground: Ground):
    """Samples along a segment every SAMPLE_M: x, y and height."""
    n = max(2, int(math.ceil(seg.length / SAMPLE_M)) + 1)
    pts = [seg.interpolate(d) for d in np.linspace(0, seg.length, n)]
    xs = np.array([p.x for p in pts])
    ys = np.array([p.y for p in pts])
    zs = ground.heights(xs, ys) if ground.known else np.zeros(n)
    return xs, ys, zs


def climb_of(zs) -> tuple[float, float]:
    dz = np.diff(zs)
    return float(dz[dz > 0].sum()), float(-dz[dz < 0].sum())


def climb(seg: LineString, ground: Ground) -> tuple[float, float]:
    """Ascent and descent along a segment, from u to v, in metres."""
    if not ground.known:
        return 0.0, 0.0
    return climb_of(profile(seg, ground)[2])


def add_segment(G, net_lines, xy, eid, seg, kind, oid, tags, ground,
                land, pace, marked_ok=True):
    """One segment, both ways, with its time, its kind and how rich."""
    u, v = _key(seg.coords[0]), _key(seg.coords[-1])
    xy[u], xy[v] = seg.coords[0], seg.coords[-1]
    xs, ys, zs = profile(seg, ground)
    up, down = climb_of(zs)
    q, kinds = land.quality(seg, xs, ys, zs)
    footpath = kind == "path" and tags.get("highway") in FOOTPATHS
    kinds["footpath"] = seg.length if footpath else 0.0
    if footpath:
        q = min(Q_MAX, q + Q_FOOTPATH)
    # a marked trail on a minor road or a track is a path
    # 0 on a path; on a road, what a minute of it weighs. A marked
    # trail on a minor road or a track is a path.
    if kind == "main":
        road = MAIN_ROAD_WEIGHT
    elif kind == "minor" and not (marked_ok and kinds["marked"]
                                  > 0.5 * seg.length):
        road = MINOR_ROAD_WEIGHT
    else:
        road = 0.0
    net_lines[eid] = seg
    for a, b, rise, fall, d in ((u, v, up, down, 1), (v, u, down, up, -1)):
        t = din_minutes(seg.length, rise, fall) * pace
        old = G.get_edge_data(a, b)
        if old is None or way_cost(old, 0.0) > way_cost(
                {"time": t, "road": road, "q": q}, 0.0):
            G.add_edge(a, b, eid=eid, dir=d, time=t, road=road, q=q,
                       kinds=kinds, length=seg.length, up=rise, down=fall,
                       highway=tags.get("highway"), name=tags.get("name"),
                       osm=oid)


def way_cost(d: dict, lam: float) -> float:
    """What a segment weighs: a road outweighs any path; on a path,
    the walking time, lightened by how rich the path is."""
    w = d["time"] * (d["road"] if d["road"] else
                     (1.0 - lam * d["q"]))
    return w * d.get("alt", 1.0)


def build_network(ways, ground: Ground, party: Party,
                  strip, land: Landscape, water=None) -> Network:
    marked = []
    parts = []                   # (LineString, tags, osm_id, kind)
    for w in ways:
        if w.tags.get("route") in ("hiking", "foot") and \
                not w.tags.get("highway"):
            marked.append(w.geom)
            continue
        kind = walkable(w.tags, party)
        if kind is None:
            continue
        for ls in w.geom.geoms:
            if len(ls.coords) >= 2:
                parts.append([list(ls.coords), w.tags, w.osm_id, kind])
    land.marked = unary_union(marked).buffer(10) if marked else None
    land.prepare()
    join_dangling(parts, water)
    parts = [(LineString(c), t, o, k) for c, t, o, k in parts]

    # Nodes where ways meet: any vertex used by two or more lines,
    # and every line's ends.
    count: dict = {}
    for ls, *_ in parts:
        seen = set()
        for c in ls.coords:
            k = _key(c)
            if k not in seen:
                count[k] = count.get(k, 0) + 1
                seen.add(k)

    G = nx.DiGraph()
    xy, lines = {}, {}
    eid = 0
    for ls, tags, oid, kind in parts:
        coords = list(ls.coords)
        start = 0
        for i in range(1, len(coords)):
            k = _key(coords[i])
            if i == len(coords) - 1 or count.get(k, 0) > 1:
                seg = LineString(coords[start:i + 1])
                start = i
                if seg.length < 0.05:
                    continue
                if strip is not None and seg.intersects(strip):
                    continue
                if _key(seg.coords[0]) == _key(seg.coords[-1]):
                    continue
                eid += 1
                add_segment(G, lines, xy, eid, seg, kind, oid, tags,
                            ground, land, party.pace)
    if G.number_of_nodes() == 0:
        sys.exit("stage_planner: no walkable paths in this area")
    # Keep the largest connected part, so a snap never lands on an
    # island the route cannot leave.
    biggest = max(nx.weakly_connected_components(G), key=len)
    G = G.subgraph(biggest).copy()
    node_ids = list(G.nodes)
    tree = STRtree([Point(xy[n]) for n in node_ids])
    return Network(G, xy, lines, tree, node_ids, ground, party.pace, land)


def snap(net: Network, p: Point) -> tuple:
    """Join a point to the nearest point on the nearest path: split
    that path there with a new node, so a route reaches a house in
    the middle of a long path, not the junction at its end. Returns
    the node and the distance from the point to the path."""
    G = net.G
    eids = sorted({d["eid"] for _, _, d in G.edges(data=True)})
    tree = STRtree([net.lines[e] for e in eids])
    e = eids[tree.nearest(p)]
    line = net.lines[e]
    d = line.project(p)
    on = line.interpolate(d)
    off = on.distance(p)
    u, v = _key(line.coords[0]), _key(line.coords[-1])
    if d < 2.0:
        return u, off + d
    if line.length - d < 2.0:
        return v, off + line.length - d
    data = [G[x][y] for x, y in ((u, v), (v, u))
            if G.has_edge(x, y) and G[x][y]["eid"] == e]
    base = data[0]
    w = _key((on.x, on.y))
    net.xy[w] = (on.x, on.y)
    for x, y in ((u, v), (v, u)):
        if G.has_edge(x, y) and G[x][y]["eid"] == e:
            G.remove_edge(x, y)
    kind = "main" if base["road"] and base["highway"] in MAIN_ROADS else \
        ("minor" if base["road"] else "path")
    for seg in (substring(line, 0, d), substring(line, d, line.length)):
        new = max(net.lines) + 1
        add_segment(G, net.lines, net.xy, new, seg, kind, base["osm"],
                    {"highway": base["highway"], "name": base["name"]},
                    net.ground, net.land, net.pace,
                    marked_ok=not base["road"])
    net.node_ids.append(w)
    net.tree = STRtree([Point(net.xy[n]) for n in net.node_ids])
    return w, off


# ── Route, band, places ────────────────────────────────────────

@dataclass
class Route:
    nodes: list
    line: LineString
    length: float
    minutes: float
    up: float
    down: float
    along: dict                  # node -> (metres, minutes) from start
    legs: list                   # per edge: highway, name, osm


def route_between(net: Network, a, b, lam: float = 0.0) -> Route | None:
    """The way between two nodes for one weight of richness, lam: 0
    is the most direct way on paths, 1 the richest the paths allow."""
    try:
        nodes = nx.dijkstra_path(net.G, a, b,
                                 weight=lambda u, v, d: way_cost(d, lam))
    except nx.NetworkXNoPath:
        return None
    return make_route(net, nodes)


def the_way(net: Network, a, b, allowance: float) -> tuple:
    """The richest way within the allowance: the most direct way on
    paths first, then the weight of richness raised as far as the
    walk stays within (1 + allowance) of it. Returns the way, the
    most direct way, and the weight used."""
    direct = route_between(net, a, b, 0.0)
    if direct is None:
        return None, None, 0.0
    budget = direct.minutes * (1.0 + allowance)
    best, best_lam = direct, 0.0
    richest = route_between(net, a, b, 1.0)
    if richest.minutes <= budget:
        return richest, direct, 1.0
    lo, hi = 0.0, 1.0
    for _ in range(8):
        lam = (lo + hi) / 2
        r = route_between(net, a, b, lam)
        if r.minutes <= budget:
            best, best_lam, lo = r, lam, lam
        else:
            hi = lam
    return best, direct, best_lam


def make_route(net: Network, nodes: list) -> Route:
    coords, legs = [], []
    length = minutes = up = down = 0.0
    along = {nodes[0]: (0.0, 0.0)}
    for a, b in zip(nodes, nodes[1:]):
        e = net.G[a][b]
        seg = net.lines[e["eid"]]
        cs = list(seg.coords) if e["dir"] == 1 else list(seg.coords)[::-1]
        coords.extend(cs if not coords else cs[1:])
        length += e["length"]
        minutes += e["time"]
        up += e["up"]
        down += e["down"]
        along.setdefault(b, (length, minutes))
        legs.append({k: e[k] for k in ("highway", "name", "osm", "road",
                                         "kinds", "length")})
    return Route(nodes, LineString(coords), length, minutes, up, down,
                 along, legs)


def gaps_on(net: Network, r: Route) -> list[dict]:
    """The joined gaps a route walks: length and where."""
    out = []
    for u, v in zip(r.nodes, r.nodes[1:]):
        d = net.G[u][v]
        if d["highway"] == "gap":
            mid = net.lines[d["eid"]].interpolate(0.5, normalized=True)
            lon, lat = TO_4326.transform(mid.x, mid.y)
            out.append({"gap_m": round(d["length"]),
                        "lat": round(lat, 5), "lon": round(lon, 5)})
    return out


def what_the_way_holds(r: Route) -> dict:
    """Kilometres on roads, on marked trails, over the plai, in
    forest and over meadows."""
    km = lambda m: round(m / 1000, 1)
    roads = sum(l["length"] for l in r.legs if l["road"])
    out = {"roads_km": km(roads)}
    for k in ("footpath", "marked", "plai", "forest", "meadow"):
        out[f"{k}_km"] = km(sum(l["kinds"].get(k, 0.0) for l in r.legs))
    return out


def reach_points(r: Route, a_pt: Point, b_pt: Point):
    """Draw a route on to its start and end where they lie off the
    path, and count those metres at the off-path pace."""
    coords = list(r.line.coords)
    extra = 0.0
    if Point(coords[0]).distance(a_pt) > 1.0:
        extra += Point(coords[0]).distance(a_pt)
        coords.insert(0, (a_pt.x, a_pt.y))
    if Point(coords[-1]).distance(b_pt) > 1.0:
        extra += Point(coords[-1]).distance(b_pt)
        coords.append((b_pt.x, b_pt.y))
    r.line = LineString(coords)
    r.length += extra
    r.minutes += extra / OFF_PATH_M_PER_MIN


def alternatives(net: Network, a, b, best: Route, n: int, lam: float,
                 penalty=1.5, max_shared=0.6) -> list[Route]:
    """Make the edges already used dearer and route again; keep a
    candidate that shares less than max_shared of its length with
    every route found so far. The graph is restored afterwards."""
    G = net.G
    saved: dict = {}
    found, last = [best], best
    try:
        for _ in range(n * 4):
            if len(found) > n:
                break
            for u, v in zip(last.nodes, last.nodes[1:]):
                for x, y in ((u, v), (v, u)):
                    if G.has_edge(x, y):
                        saved.setdefault((x, y), G[x][y].get("alt", 1.0))
                        G[x][y]["alt"] = G[x][y].get("alt", 1.0) * penalty
            last = route_between(net, a, b, lam)
            if last is None:
                break
            if all(shared(net, last, r) < max_shared for r in found):
                found.append(last)
    finally:
        for (x, y), c in saved.items():
            G[x][y]["alt"] = c
    return found[1:]


def _eids(net: Network, r: Route) -> set:
    return {net.G[u][v]["eid"] for u, v in zip(r.nodes, r.nodes[1:])}


def shared(net: Network, r: Route, other: Route) -> float:
    """The share of r's length that also lies on other."""
    common = _eids(net, r) & _eids(net, other)
    return sum(net.lines[e].length for e in common) / max(r.length, 1)


def reach_from(net: Network, route: Route, minutes: float):
    """Walking minutes from the route to every node within reach,
    and the route node each is left from."""
    dist, paths = nx.multi_source_dijkstra(
        net.G, set(route.nodes), cutoff=minutes, weight="time")
    origin = {n: p[0] for n, p in paths.items()}
    return dist, origin


def band(net: Network, route: Route, dist: dict) -> list:
    """Nested rings, inner to outer: (minutes, opacity, polygon)."""
    # Every reached path, sampled every BAND_STEP_M with the minutes
    # it takes to get there from the route; the route itself is 0.
    xs, ys, ts = [], [], []
    for u, tu in dist.items():
        for v, e in net.G[u].items():
            if e["time"] <= 0:
                continue
            seg = net.lines[e["eid"]]
            if e["dir"] == -1:
                seg = LineString(list(seg.coords)[::-1])
            on_route = tu == 0 and dist.get(v) == 0
            n = max(2, int(seg.length // BAND_STEP_M) + 2)
            for d in np.linspace(0, seg.length, n):
                t = 0.0 if on_route else tu + e["time"] * d / seg.length
                if t > BAND_MINUTES[-1]:
                    break
                p = seg.interpolate(d)
                xs.append(p.x)
                ys.append(p.y)
                ts.append(t)
    xs, ys, ts = map(np.asarray, (xs, ys, ts))
    pts = shapely.points(xs, ys)
    rings = []
    for T, opacity in zip(BAND_MINUTES, BAND_OPACITY):
        keep = ts <= T
        # A pilgrim may step off the path for the minutes left, up
        # to OFF_PATH_CAP_M; the circle shrinks as the minutes do,
        # which is what makes the edge soft.
        radii = np.clip((T - ts[keep]) * OFF_PATH_M_PER_MIN,
                        PATH_HALF_WIDTH_M, OFF_PATH_CAP_M)
        poly = shapely.union_all(shapely.buffer(pts[keep], radii,
                                                quad_segs=6))
        poly = poly.union(route.line.buffer(PATH_HALF_WIDTH_M))
        # Close small gaps and round the edge: the band is fuzzy by
        # design — it speaks for reach, never for parcels (S-14).
        poly = poly.buffer(60, 8).buffer(-60, 8).simplify(5)
        rings.append((T, opacity, poly))
    return rings


def public_host(entry: dict) -> dict:
    """What the public answer says of a host (SP-3): their name and
    their detour time, nothing else — no place, no offer, no kind,
    no kilometre along the route."""
    return {"name": entry["name"], "is_host": True,
            "detour_min": entry["detour_min"],
            "order": entry.get("order", 0)}


def for_audience(entries: list[dict], audience: str) -> list[dict]:
    if audience == "curator":
        return entries
    return [public_host(e) if e.get("is_host") else e for e in entries]


def places_along(net: Network, route: Route, places: list[Place],
                 dist: dict, origin: dict, outer, reach_min: float,
                 strip, audience: str, month: str | None) -> list[dict]:
    out = []
    for p in places:
        if strip is not None and p.geom.intersects(strip):
            continue
        if not p.geom.intersects(outer):
            continue
        if month and p.is_host and p.extra.get("season"):
            if month.lower()[:3] not in p.extra["season"].lower():
                continue
        best = None
        # The nearest few nodes, so a place beside a path that the
        # route skirts is reached by the shorter way.
        for i in net.tree.query(p.geom.buffer(OFF_PATH_CAP_M)):
            n = net.node_ids[i]
            if n not in dist:
                continue
            off = Point(net.xy[n]).distance(p.geom)
            t = dist[n] + off / OFF_PATH_M_PER_MIN
            if best is None or t < best[0]:
                best = (t, n)
        if best is None or best[0] > reach_min:
            continue
        t, n = best
        km, mins = route.along.get(origin[n], (0.0, 0.0))
        lon, lat = TO_4326.transform(p.geom.x, p.geom.y)
        out.append({
            "id": p.pid, "name": p.name, "kind": p.kind,
            "source": p.source, "is_host": p.is_host,
            "detour_min": round(t, 1),
            "on_the_way": t < 1.0,
            "route_km": round(km / 1000, 2),
            "route_min": round(mins),
            "lat": round(lat, 7), "lon": round(lon, 7),
            **{k: v for k, v in p.extra.items() if v},
        })
    out.sort(key=lambda d: (d["route_km"], d["detour_min"]))
    for i, d in enumerate(out):
        d["order"] = i
    return for_audience(out, audience)


# ── Output ─────────────────────────────────────────────────────

def hm(minutes: float) -> str:
    h, m = divmod(int(round(minutes)), 60)
    return f"{h}:{m:02d}"


def feature(geom, **props):
    return {"type": "Feature", "geometry": mapping(to_4326(geom)),
            "properties": props}


def place_feature(p: dict) -> dict:
    """A place as a feature; a host in the public answer has no
    geometry at all (RFC 7946 §3.2 allows null)."""
    geom = ({"type": "Point", "coordinates": [p["lon"], p["lat"]]}
            if "lon" in p else None)
    return {"type": "Feature", "geometry": geom,
            "properties": {**p, "role": "place"}}


def describe(p: dict) -> str:
    where = ("on the way" if p.get("on_the_way")
             else f"{p['detour_min']:.0f} min off")
    km = f"km {p['route_km']:>5.1f}" if "route_km" in p else " " * 8
    kind = (f" ({p['kind']})" if p.get("kind") and p["kind"] != p["name"]
            else "" if p.get("kind") else " (host)")
    return f"  {km}  {where:>12}  {p['name']}{kind}"


def write_geojson(path: Path, routes, rings, places, summary, ends=()):
    feats = []
    for T, opacity, poly in reversed(rings):
        feats.append(feature(poly, role="band", minutes=T,
                             fill_opacity=opacity))
    outer = rings[-1][2] if rings else None
    if outer is not None:
        polys = getattr(outer, "geoms", [outer])
        for poly in polys:
            feats.append(feature(LineString(poly.exterior.coords), role="boundary",
                                 minutes=rings[-1][0]))
    for i, r in enumerate(routes):
        feats.append(feature(r.line, role="route" if i == 0
                             else "alternative", rank=i,
                             km=round(r.length / 1000, 2),
                             time=hm(r.minutes), up_m=round(r.up),
                             down_m=round(r.down)))
    for p in places:
        feats.append(place_feature(p))
    for role, label, pt, off in ends:
        feats.append(feature(pt, role=role, name=label,
                             off_path_m=round(off)))
    for g in summary.get("gaps", []):
        feats.append({"type": "Feature",
                      "geometry": {"type": "Point",
                                   "coordinates": [g["lon"], g["lat"]]},
                      "properties": {"role": "gap", **g}})
    fc = {"type": "FeatureCollection", "features": feats,
          "properties": summary}
    path.write_text(json.dumps(fc, ensure_ascii=False, indent=1),
                    encoding="utf-8")


HTML = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Route preview</title>
<link rel="stylesheet"
 href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">
<style>
 html,body{margin:0;height:100%;font:14px/1.4 Inter,system-ui,sans-serif}
 #map{position:absolute;inset:0 0 0 340px}
 aside{position:absolute;inset:0 auto 0 0;width:340px;overflow:auto;
  padding:14px 16px;box-sizing:border-box;background:#faf8f3;color:#222}
 h1{font:600 17px/1.3 Lora,Georgia,serif;margin:0 0 6px}
 .sum{color:#555;margin:0 0 12px}
 li{margin:0 0 8px} small{color:#666}
 @media (max-width:700px){#map{inset:45% 0 0 0}aside{inset:0 0 55% 0;width:auto}}
</style></head><body>
<aside><h1>__TITLE__</h1><p class="sum">__SUM__</p><ol id="list"></ol>
<p><small>__NOTICE__</small></p></aside><div id="map"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
<script>
const data = __DATA__;
const map = L.map('map');
// Plai's own base map, the one the Pathways application shows:
// OpenStreetMap drawn by Mapservice, with the ground model's relief.
// OpenStreetMap's tile servers refuse a page opened from a file.
L.tileLayer.wms('__WMS__', {
 layers: '__WMS_LAYERS__', format: 'image/png', version: '1.3.0',
 tileSize: 512, zoomOffset: 0, maxZoom: 18,
 attribution: '© OpenStreetMap contributors, ODbL · relief GEDTM30 · Plai, UBEC Mapservice'
}).addTo(map);
const layer = L.geoJSON(data, {
 style: f => {
  const p = f.properties;
  if (p.role === 'band') return {stroke:false, fillColor:'#2f6f4f', fillOpacity:p.fill_opacity};
  if (p.role === 'boundary') return {color:'#2f6f4f', weight:1.2, opacity:.55, dashArray:'4 6'};
  if (p.role === 'route') return {color:'#9a3412', weight:4};
  if (p.role === 'alternative') return {color:'#9a3412', weight:2.5, opacity:.6, dashArray:'6 6'};
  return {};
 },
 pointToLayer: (f, ll) => {
  const r = f.properties.role;
  if (r === 'start' || r === 'end') return L.circleMarker(ll, {radius:9, color:'#fff', weight:2.5,
   fillColor: r === 'start' ? '#15803d' : '#9a3412', fillOpacity:1});
  if (r === 'gap') return L.circleMarker(ll, {radius:6, color:'#c2410c', weight:2,
   fillColor:'#fff', fillOpacity:1});
  return L.circleMarker(ll, {radius:6, color:'#fff', weight:1.5,
   fillColor: f.properties.is_host ? '#b45309' : '#1d4ed8', fillOpacity:1}); },
 onEachFeature: (f, l) => { const p = f.properties;
  if (p.role === 'start' || p.role === 'end') l.bindPopup(`<b>${p.role === 'start' ? 'Start' : 'End'}:</b> ${p.name}`
   + (p.off_path_m > 1 ? `<br>${p.off_path_m} m from the nearest path` : ''));
  if (p.role === 'gap') l.bindPopup(`A gap of ${p.gap_m} m joined here — `
   + 'the paths do not meet on the map. Check it on the ground.');
  if (p.role === 'place') l.bindPopup(`<b>${p.name}</b><br>${p.kind}<br>`
   + `${p.detour_min} min off the route at km ${p.route_km}`); }
}).addTo(map);
map.fitBounds(layer.getBounds(), {padding:[20,20]});
// A click anywhere gives that point, and the command that asks the
// planner what way lies there.
map.on('click', e => {
 if (e.originalEvent && e.originalEvent.target && e.originalEvent.target.closest
     && e.originalEvent.target.closest('.leaflet-interactive')) return;
 const ll = `${e.latlng.lat.toFixed(5)},${e.latlng.lng.toFixed(5)}`;
 L.popup().setLatLng(e.latlng).setContent(
  `<b>${ll}</b><br><code style="font-size:12px;user-select:all">`
  + `python3 /tmp/stage_planner.py inspect "${ll}"</code>`).openOn(map);
});
const ol = document.getElementById('list');
for (const f of data.features.filter(f => f.properties.role === 'place')) {
 const p = f.properties, li = document.createElement('li');
 const kind = p.kind ? (p.kind === p.name ? '' : ` — ${p.kind}`) : ' — host';
 li.innerHTML = `<b>${p.name}</b>${kind}<br><small>`
  + (p.route_km === undefined ? '' : `km ${p.route_km} · `)
  + (p.on_the_way ? 'on the way' : `${p.detour_min} min off the route, one way`) + '</small>';
 ol.appendChild(li);
}
</script></body></html>
"""


def write_html(path: Path, geojson_path: Path, summary: dict,
               title: str = "Route preview"):
    data = geojson_path.read_text(encoding="utf-8")
    s = summary["route"]
    text = (f"{s['km']} km · {s['time']} walking · ↑{s['up_m']} m "
            f"↓{s['down_m']} m · places within {summary['reach_min']:g} "
            "min of the route")
    html = (HTML.replace("__TITLE__", title)
            .replace("__SUM__", text)
            .replace("__NOTICE__", " · ".join(summary["notices"]))
            .replace("__WMS__", PLAI_WMS)
            .replace("__WMS_LAYERS__", ",".join(PLAI_WMS_LAYERS))
            .replace("__DATA__", data))
    path.write_text(html, encoding="utf-8")


# ── Command ────────────────────────────────────────────────────

def resolve(src, text: str) -> Point:
    """A point from "lat,lon" or a name. A name is taken when one
    place matches it best; when several match equally, they are
    listed and the planner stops, rather than guess."""
    p = parse_latlon(text)
    if p is not None:
        return p
    found = ranked(src.candidates(text), text)
    if not found:
        sys.exit(f"stage_planner: no place called {text!r} on Plai or "
                 "in OSM — give it as \"lat,lon\" (a map app copies "
                 "it), or try `find`")
    best = found[0][0]
    top = [c for sc, c in found if sc == best]
    # Two points under 300 m apart are one place mapped twice.
    if len(top) > 1 and any(c.geom.distance(top[0].geom) > 300
                            for c in top[1:]):
        lines = "\n".join(f"  {c.names[0]} ({c.kind}, {c.source}) "
                          f"{latlon(c.geom)}" for c in top[:10])
        sys.exit(f"stage_planner: {len(top)} places match {text!r}; "
                 f"give the one you mean as \"lat,lon\":\n{lines}")
    c = top[0]
    if best < 3:
        print(f"stage_planner: {text!r} taken as {c.names[0]} "
              f"({c.kind}, {c.source}) at {latlon(c.geom)}",
              file=sys.stderr)
    return c.geom


def cmd_inspect(args) -> int:
    """What lies at a point: the nearest ways, whether this party
    walks each and why not, and whether each joins the network the
    planner routes on."""
    pt = parse_latlon(args.point)
    if pt is None:
        sys.exit("stage_planner: inspect needs \"lat,lon\"")
    party = PARTY[args.party]
    src = (PostgisSource(args.instance_db) if args.source == "postgis"
           else FileSource(Path(args.paths), None, None))
    near = (pt.x - 150, pt.y - 150, pt.x + 150, pt.y + 150)
    ways = [w for w in src.ways(near)
            if w.tags.get("highway") and w.geom.distance(pt) <= 150]
    if not ways:
        print("No way within 150 m of that point in OSM.")
        return 1
    box = (pt.x - 3000, pt.y - 3000, pt.x + 3000, pt.y + 3000)
    net = build_network(src.ways(box), Ground(None, box), party, None,
                        Landscape(), src.waterways(box))
    lines = [net.lines[d["eid"]] for _, _, d in net.G.edges(data=True)]
    tree = STRtree(lines) if lines else None
    ways.sort(key=lambda w: w.geom.distance(pt))
    for w in ways[:args.limit]:
        t = w.tags
        keys = ("highway", "name", "sac_scale", "trail_visibility",
                "access", "foot", "tracktype", "surface")
        desc = ", ".join(f"{k}={t[k]}" for k in keys if t.get(k))
        print(f"{w.geom.distance(pt):5.0f} m  OSM way {w.osm_id}: {desc}")
        reason = why_not(t, party)
        if reason:
            print(f"         not walked by a {args.party}: {reason}")
            continue
        on = (tree is not None and any(
            lines[i].distance(w.geom) < 0.5 and
            lines[i].within(w.geom.buffer(0.5))
            for i in tree.query(w.geom.buffer(0.5))))
        if on:
            kind = walkable(t, party)
            what = ("a footpath, first among paths"
                    if t.get("highway") in FOOTPATHS else
                    "a road for vehicles, walked only when nothing else "
                    "joins" if kind in ("minor", "main") else "a path")
            print(f"         walked, joined to the network: {what}")
        else:
            print("         walkable, but not joined to the network around "
                  "it: its ends meet no other way within "
                  f"{JOIN_GAP_M:g} m, so the planner cannot reach it")
    return 0


def cmd_find(args) -> int:
    src = (PostgisSource(args.instance_db) if args.source == "postgis"
           else FileSource(Path(args.paths or "/dev/null"),
                           Path(args.places) if args.places else None,
                           None))
    found = ranked(src.candidates(args.text), args.text)
    if not found:
        print(f"Nothing called {args.text!r} on Plai or in OSM.")
        return 1
    label = {3: "exact", 2: "same name", 1: "contains"}
    for sc, c in found[:args.limit]:
        others = [n for n in c.names[1:] if n and n != c.names[0]]
        also = f" — also {', '.join(dict.fromkeys(others))}" if others else ""
        print(f"  {latlon(c.geom):>20}  {label[sc]:<9}  {c.names[0]} "
              f"({c.kind}, {c.source}){also}")
    return 0


def _lonlat(p: Point) -> list:
    lon, lat = TO_4326.transform(p.x, p.y)
    return [round(lon, 7), round(lat, 7)]


def criteria(args) -> dict:
    """The criteria a route was made with, so a saved stretch can
    be remade the same way or compared with one made otherwise."""
    return {"version": VERSION, "party": args.party,
            "pace": PARTY[args.party].pace,
            "din_33466": [DIN_FLAT_KMH, DIN_UP_MH, DIN_DOWN_MH],
            "road_weight": {"minor": MINOR_ROAD_WEIGHT,
                            "main": MAIN_ROAD_WEIGHT},
            "allowance": args.allowance,
            "quality": {"footpath": Q_FOOTPATH, "marked": Q_MARKED,
                        "plai": Q_PLAI,
                        "plai_min_ele": PLAI_MIN_ELE, "forest": Q_FOREST,
                        "meadow": Q_MEADOW, "places": Q_PLACE,
                        "plai_place": Q_PLAI_PLACE,
                        "farmstead": Q_FARMSTEAD, "max": Q_MAX},
            "border_strip_m": (None if args.allow_border_strip
                               else BORDER_STRIP_M),
            "band_minutes": list(BAND_MINUTES), "reach_min": args.reach}


def cmd_corridor(args) -> int:
    """Join stretches — files `route` wrote — into one corridor:
    the union of their bands ring by ring, one boundary, one list
    of places with the shortest detour each was reached by. Nothing
    is drawn that a stretch did not draw: a corridor speaks for its
    stretches and their places, never for land between them
    (S-14)."""
    stretches = []
    for path in args.stretches:
        if not Path(path).exists():
            sys.exit(f"stage_planner: {path} does not exist — did "
                     "`route` stop before writing it?")
        fc = json.loads(Path(path).read_text(encoding="utf-8"))
        props = fc.get("properties") or {}
        if "stretch" not in props:
            sys.exit(f"stage_planner: {path} is not a stretch "
                     "(written by `route` v0.2 or later)")
        stretches.append((path, fc, props))

    by_min: dict = {}
    lines, places, rows, ends, gaps = [], {}, [], {}, []
    offset_km = offset_min = 0.0
    notices = {OSM_NOTICE}
    prev_end = None
    for pos, (path, fc, props) in enumerate(stretches):
        notices.update(props.get("notices", []))
        st = props["route"]
        km = st["km"]
        h, m = st["time"].split(":")
        mins = int(h) * 60 + int(m)
        gap = None
        for f in fc["features"]:
            p = f["properties"]
            # A host in a public answer has no geometry (SP-3).
            g = to_3035(shape(f["geometry"])) if f["geometry"] else None
            if p["role"] == "band":
                by_min.setdefault(p["minutes"], [p["fill_opacity"], []])
                by_min[p["minutes"]][1].append(g)
            elif p["role"] == "route":
                lines.append(g)
                if prev_end is not None:
                    gap = round(Point(g.coords[0]).distance(prev_end))
                prev_end = Point(g.coords[-1])
            elif p["role"] == "gap":
                gaps.append(f)
            elif p["role"] in ("start", "end"):
                ends.setdefault(p["role"], [])
                ends[p["role"]].append((g, p))
            elif p["role"] == "place":
                q = {k: v for k, v in p.items() if k != "role"}
                if args.audience == "public" and q.get("is_host"):
                    q = public_host(q)
                else:
                    q["route_km"] = round(q["route_km"] + offset_km, 2)
                    q["route_min"] = round(q["route_min"] + offset_min)
                    q["stretch"] = props["stretch"].get("name") or path
                q["_at"] = (pos, q.get("order", 0))
                key = q.get("id") or ("host", q["name"])
                old = places.get(key)
                if old is None or q["detour_min"] < old["detour_min"]:
                    places[key] = q
        rows.append({"stretch": props["stretch"].get("name") or path,
                     "from": props["stretch"]["from"],
                     "to": props["stretch"]["to"], **st,
                     "gap_m_from_previous": gap})
        offset_km += km
        offset_min += mins

    rings = []
    for T in sorted(by_min):
        opacity, polys = by_min[T]
        rings.append((T, opacity, unary_union(polys)))
    if not rings:
        sys.exit("stage_planner: the stretches carry no band")
    found = sorted(places.values(), key=lambda d: d.pop("_at"))
    for i, d in enumerate(found):
        d["order"] = i
    total = {"km": round(sum(r["km"] for r in rows), 2),
             "time": hm(offset_min),
             "up_m": sum(r["up_m"] for r in rows),
             "down_m": sum(r["down_m"] for r in rows)}
    summary = {
        "tool": f"stage_planner corridor v{VERSION}",
        "corridor": {"name": args.name, "stretches": rows},
        "audience": args.audience, "route": total,
        "reach_min": max(T for T, _, _ in rings),
        "notices": sorted(notices),
        "stored": "nothing — saving a corridor is the Curator's, on Plai",
    }
    feats = []
    for T, opacity, poly in reversed(rings):
        feats.append(feature(poly, role="band", minutes=T,
                             fill_opacity=opacity))
    for poly in getattr(rings[-1][2], "geoms", [rings[-1][2]]):
        feats.append(feature(LineString(poly.exterior.coords), role="boundary",
                             minutes=rings[-1][0]))
    for row, line in zip(rows, lines):
        feats.append(feature(line, role="route", **{
            k: row[k] for k in ("stretch", "km", "time", "up_m",
                                "down_m")}))
    for p in found:
        feats.append(place_feature(p))
    feats.extend(gaps)
    for role, pick in (("start", 0), ("end", -1)):
        if ends.get(role):
            g, p = ends[role][pick]
            feats.append(feature(g, **p))
    out = Path(args.out)
    out.write_text(json.dumps({"type": "FeatureCollection",
                               "features": feats,
                               "properties": summary},
                              ensure_ascii=False, indent=1),
                   encoding="utf-8")
    if args.html:
        write_html(Path(args.html), out, summary,
                   args.name or "Corridor preview")

    print(f"Corridor{' ' + args.name if args.name else ''}: "
          f"{len(rows)} stretches, {total['km']} km, {total['time']} "
          f"walking, ↑{total['up_m']} m ↓{total['down_m']} m")
    for r in rows:
        gap = r["gap_m_from_previous"]
        note = f" — {gap} m from the previous end" if gap and gap > 50 else ""
        print(f"  {r['stretch']}: {r['from']} → {r['to']}, {r['km']} km, "
              f"{r['time']}{note}")
    print(f"Places within reach: {len(found)}")
    for p in found:
        print(describe(p))
    print(f"Written: {out}" + (f", {args.html}" if args.html else ""))
    return 0


def cmd_route(args) -> int:
    party = PARTY[args.party]
    if args.source == "postgis":
        src = PostgisSource(args.instance_db)
        dem = Path(args.dem) if args.dem else Path(
            os.environ.get("DATA_ROOT", "/data/ubec_mapservice"),
            "terrain", "ground.tif")
    else:
        if not args.paths:
            sys.exit("stage_planner: --source files needs --paths")
        src = FileSource(Path(args.paths),
                         Path(args.places) if args.places else None,
                         Path(args.border_strip) if args.border_strip
                         else None,
                         Path(args.areas) if args.areas else None)
        dem = Path(args.dem) if args.dem else None

    a_pt, b_pt = resolve(src, args.start), resolve(src, args.end)
    gap = a_pt.distance(b_pt)
    margin = max(3000.0, 0.35 * gap)
    bbox = (min(a_pt.x, b_pt.x) - margin, min(a_pt.y, b_pt.y) - margin,
            max(a_pt.x, b_pt.x) + margin, max(a_pt.y, b_pt.y) + margin)

    notices = [OSM_NOTICE]
    strip = None
    if not args.allow_border_strip:
        strip = src.border_strip(bbox, BORDER_STRIP_M)
        if strip is None or strip.is_empty:
            strip = None
            if args.source == "files" and not args.border_strip:
                notices.append("Border strip not checked (no file given)")
        else:
            for label, pt in (("start", a_pt), ("end", b_pt)):
                if pt.intersects(strip):
                    sys.exit(f"stage_planner: the {label} is inside the "
                             "five-kilometre border strip (S-8); no stage "
                             "there is suggested until the Curator holds "
                             "the permit route")
    else:
        notices.append("Border strip allowed by the Curator (S-8)")

    ground = Ground(dem, bbox)
    if ground.known:
        notices.append(GEDTM_CREDIT)
    else:
        notices.append("No ground heights: times are for the flat")

    places = list(src.osm_places(bbox)) + list(src.plai_places(bbox))
    land = src.landscape(bbox, ground)
    land.points += [(pl.geom, Q_PLAI_PLACE if pl.source == "plai"
                     else Q_PLACE.get(pl.kind, 0.3)) for pl in places]
    if land.canopy is not None and land.canopy.known:
        notices.append("Forest and open land: canopy height from the "
                       "ground and surface models")
    net = build_network(src.ways(bbox), ground, party, strip, land,
                        src.waterways(bbox))
    a, a_off = snap(net, a_pt)
    b, b_off = snap(net, b_pt)
    for label, off in (("start", a_off), ("end", b_off)):
        if off > SNAP_WARN_M:
            print(f"stage_planner: the {label} is {off:.0f} m from the "
                  "nearest path — check the point", file=sys.stderr)

    best, direct, lam = the_way(net, a, b, args.allowance)
    if best is None:
        sys.exit("stage_planner: no route between these two points "
                 "with this party's limits")
    routes = [best] + alternatives(net, a, b, best, args.alternatives,
                                   lam)
    # The last metres off the path, drawn to the points themselves.
    for r in routes + [direct]:
        reach_points(r, a_pt, b_pt)

    dist, origin = reach_from(net, best, max(BAND_MINUTES[-1],
                                             args.reach))
    rings = band(net, best, dist)
    found = places_along(net, best, places, dist, origin, rings[-1][2],
                         args.reach, strip, args.audience, args.month)

    summary = {
        "tool": f"stage_planner route v{VERSION}",
        # What a saved stretch carries besides its line (spec §4).
        "stretch": {"name": args.name, "from": args.start,
                    "to": args.end,
                    "start": _lonlat(a_pt), "end": _lonlat(b_pt),
                    "criteria": criteria(args)},
        "audience": args.audience, "party": args.party,
        "month": args.month, "reach_min": args.reach,
        "route": {"km": round(best.length / 1000, 2),
                  "time": hm(best.minutes),
                  "up_m": round(best.up), "down_m": round(best.down)},
        "the_way": what_the_way_holds(best),
        "gaps": gaps_on(net, best),
        "alternatives": [{"km": round(r.length / 1000, 2),
                          "time": hm(r.minutes), "up_m": round(r.up),
                          "down_m": round(r.down),
                          **what_the_way_holds(r)} for r in routes[1:]],
        # The reference the allowance is measured against.
        "direct": {"km": round(direct.length / 1000, 2),
                   "time": hm(direct.minutes),
                   "allowance": args.allowance,
                   "richness_weight": round(lam, 3)},
        "snap_m": {"start": round(a_off), "end": round(b_off)},
        "notices": notices,
        "stored": "nothing — saving a stretch is the Curator's, on Plai",
    }

    out = Path(args.out)
    ends = [("start", args.start, a_pt, a_off), ("end", args.end, b_pt, b_off)]
    write_geojson(out, routes, rings, found, summary, ends)
    if args.html:
        write_html(Path(args.html), out, summary,
                   args.name or "Route preview")

    s = summary["route"]
    print(f"Route: {s['km']} km, {s['time']} walking, ↑{s['up_m']} m "
          f"↓{s['down_m']} m ({args.party})")
    print(f"  start {a_off:.0f} m and end {b_off:.0f} m from the "
          "nearest path")
    w = summary["the_way"]
    print(f"  the way: {w['footpath_km']} km on footpaths, "
          f"{w['marked_km']} km on marked trails, "
          f"{w['plai_km']} km over the plai, {w['forest_km']} km in "
          f"forest, {w['meadow_km']} km over meadows; "
          f"{w['roads_km']} km on roads for vehicles")
    for g in summary["gaps"]:
        print(f"  a gap of {g['gap_m']} m joined at {g['lat']},{g['lon']} "
              "— check it on the ground")
    for i, r in enumerate(summary["alternatives"], 1):
        print(f"  alternative {i}: {r['km']} km, {r['time']}, "
              f"↑{r['up_m']} m ↓{r['down_m']} m — {r['footpath_km']} km "
              f"footpaths, {r['marked_km']} km marked, {r['roads_km']} km "
              "roads")
    print(f"Places within {args.reach:g} min of the route: {len(found)}")
    for p in found:
        print(describe(p))
    print(f"Written: {out}" + (f", {args.html}" if args.html else ""))
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Trans-Carpathian Pathways stage planner")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("route", help="one route, its band and places")
    r.add_argument("--from", dest="start", required=True,
                   help='"lat,lon" or a place name')
    r.add_argument("--to", dest="end", required=True,
                   help='"lat,lon" or a place name')
    r.add_argument("--party", choices=sorted(PARTY), default="couple")
    r.add_argument("--month", help="jan … dec: hosts open that month")
    r.add_argument("--reach", type=float, default=10.0,
                   help="minutes off the route to list places (5 to 10)")
    r.add_argument("--alternatives", type=int, default=2)
    r.add_argument("--allowance", type=float, default=WAY_ALLOWANCE,
                   help="how much more walking the way may take than "
                        "the most direct way on paths (0.5 = half again)")
    r.add_argument("--audience", choices=("public", "curator"),
                   default="public",
                   help="public lists no host; curator lists them")
    r.add_argument("--name", help="the stretch's name, if it is one")
    r.add_argument("--allow-border-strip", action="store_true",
                   help="the Curator's flag, once the permit route is "
                        "held in writing and done (S-8)")
    r.add_argument("--source", choices=("postgis", "files"),
                   default="postgis")
    r.add_argument("--instance-db", default="ubec_i_plai")
    r.add_argument("--paths", help="files: GeoJSON of ways, EPSG:4326")
    r.add_argument("--places", help="files: GeoJSON of places")
    r.add_argument("--border-strip", help="files: GeoJSON polygon")
    r.add_argument("--areas", help="files: land cover polygons, OSM tags")
    r.add_argument("--dem", help="GeoTIFF of ground heights, EPSG:3035")
    r.add_argument("--out", default="route.geojson")
    r.add_argument("--html", help="also write a map preview here")
    c = sub.add_parser("corridor",
                       help="join stretches into one corridor")
    c.add_argument("stretches", nargs="+",
                   help="files `route` wrote, in walking order")
    c.add_argument("--name", help="the corridor's name")
    c.add_argument("--audience", choices=("public", "curator"),
                   default="public")
    c.add_argument("--out", default="corridor.geojson")
    c.add_argument("--html", help="also write a map preview here")
    i = sub.add_parser("inspect", help="what way lies at a point, and "
                       "whether the planner walks it")
    i.add_argument("point", help='"lat,lon"')
    i.add_argument("--party", choices=sorted(PARTY), default="couple")
    i.add_argument("--limit", type=int, default=5)
    i.add_argument("--source", choices=("postgis", "files"),
                   default="postgis")
    i.add_argument("--instance-db", default="ubec_i_plai")
    i.add_argument("--paths", help="files: GeoJSON of ways")
    f = sub.add_parser("find", help="which places a name matches")
    f.add_argument("text", help="a name, in Latin or Cyrillic")
    f.add_argument("--limit", type=int, default=15)
    f.add_argument("--source", choices=("postgis", "files"),
                   default="postgis")
    f.add_argument("--instance-db", default="ubec_i_plai")
    f.add_argument("--paths", help=argparse.SUPPRESS)
    f.add_argument("--places", help="files: GeoJSON of places")
    args = ap.parse_args(argv)
    if args.cmd == "corridor":
        return cmd_corridor(args)
    if args.cmd == "find":
        return cmd_find(args)
    if args.cmd == "inspect":
        return cmd_inspect(args)
    if not 1 <= args.reach <= 30:
        ap.error("--reach is minutes, 1 to 30")
    return cmd_route(args)


if __name__ == "__main__":
    sys.exit(main())
