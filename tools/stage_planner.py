#!/usr/bin/env python3
# Trans-Carpathian Pathways — stage planner, `route` and `corridor`, v0.2
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
3. finds the route, and up to two alternatives;
4. draws a band on both sides of it: the land a pilgrim reaches in
   2.5, 5, 7.5 and 10 minutes off the route, walked on the network
   and a little off it — nested rings, densest at the route and
   fading outwards, with the outer edge as the boundary;
5. lists the places inside that reach, in the order the route
   meets them, each with its one-way detour in minutes.

The criteria (starting prompt §6, §7; decisions S-8, S-15):

- Time is DIN 33466: 4 km/h on the flat, 300 m/h up, 500 m/h down;
  a segment takes the larger of its horizontal and vertical times
  plus half the smaller. The party scales it (`PARTY`).
- Off the beaten path: paths, tracks and footways are neutral;
  village roads cost a little more, main roads much more, trunk
  roads and motorways are not walked (`HIGHWAY_FACTOR`).
- A marked hiking route is preferred a little (`MARKED_FACTOR`).
- The logic of encounter: a segment that passes near a published
  Plai place or an open place (a viewpoint, a spring, a chapel) is
  preferred a little (`ENCOUNTER_FACTOR`).
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
Curator may save a route as a stretch and manage it, and stretches
are combined into a corridor (`corridor`). Saving is Plai's change,
not this tool's: the tool writes files and nothing else (spec
`docs/specs/PATHWAYS_STAGE_PLANNER_SPEC_v0_1.md`).

`--audience public` (the default) lists no host, so nothing it
writes puts a host's place in a file anyone may pass on (open data
spec §2: a host is never a waypoint in a public file); hosts stay
on Plai's map, where they are public and clickable (S-1).
`--audience curator` lists them, for the Curator's own planning.

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
published Plai place's title, or a village or hamlet in OSM.

A corridor from stretches, each a file `route` wrote:

    python3 tools/stage_planner.py corridor --name "Hutsul corridor" \\
        stretch_1.geojson stretch_2.geojson --out corridor.geojson

Changelog:
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

VERSION = "0.2"

# ── Criteria ───────────────────────────────────────────────────
# Every number here is a proposal until Michel or the Curator sets
# it; each is named so it can be changed in one place.

DIN_FLAT_KMH = 4.0          # DIN 33466
DIN_UP_MH = 300.0
DIN_DOWN_MH = 500.0

# Preference on walking time: 1.0 neutral, higher avoided, None
# never walked. The reported time is always the real DIN time.
HIGHWAY_FACTOR: dict[str, float | None] = {
    "path": 1.0, "footway": 1.0, "bridleway": 1.0, "track": 1.0,
    "steps": 1.1, "pedestrian": 1.1, "cycleway": 1.2,
    "living_street": 1.2, "service": 1.2, "unclassified": 1.3,
    "residential": 1.3, "road": 1.5,
    "tertiary": 1.6, "tertiary_link": 1.6,
    "secondary": 2.5, "secondary_link": 2.5,
    "primary": 4.0, "primary_link": 4.0,
    "trunk": None, "trunk_link": None,
    "motorway": None, "motorway_link": None,
    "construction": None, "proposed": None, "abandoned": None,
    "raceway": None, "bus_guideway": None, "platform": None,
}
MARKED_FACTOR = 0.85        # on a hiking or foot route relation
ENCOUNTER_FACTOR = 0.90     # passes within ENCOUNTER_M of a place
ENCOUNTER_M = 100.0
MIN_FACTOR = 0.70           # floor on the product of preferences

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

    def find_place(self, name: str) -> Point | None:
        like = name.strip()
        try:
            conn = self.psycopg.connect(dbname=self.inst_db,
                                        connect_timeout=5)
            with conn, conn.cursor() as cur:
                cur.execute("""SELECT ST_AsBinary(ST_Transform(geom, 3035))
                                 FROM instance.entry_public
                                WHERE title ILIKE %s
                                ORDER BY length(title) LIMIT 1""",
                            (like,))
                row = cur.fetchone()
                if row:
                    return wkb.loads(bytes(row[0]))
        except self.psycopg.Error:
            pass
        with self.fw.cursor() as cur:
            cur.execute("""
                SELECT ST_AsBinary(geom) FROM reference_sa.osm_point
                 WHERE tags ? 'place'
                   AND (name ILIKE %s OR tags->>'name:uk' ILIKE %s
                        OR tags->>'name:en' ILIKE %s
                        OR tags->>'name:de' ILIKE %s)
                 ORDER BY CASE tags->>'place' WHEN 'village' THEN 1
                          WHEN 'town' THEN 1 WHEN 'hamlet' THEN 2
                          ELSE 3 END LIMIT 1""", (like,) * 4)
            row = cur.fetchone()
        return wkb.loads(bytes(row[0])) if row else None


class FileSource:
    def __init__(self, paths: Path, places: Path | None,
                 strip: Path | None):
        self.paths, self.places_f, self.strip_f = paths, places, strip
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

    def border_strip(self, bbox, width_m):
        if not self.strip_f:
            return None
        return unary_union([to_3035(shape(f["geometry"]))
                            for f in self._features(self.strip_f)])

    def find_place(self, name: str) -> Point | None:
        """A place's title or any feature's name, villages included."""
        low = name.strip().lower()
        for f in self._features(self.places_f) if self.places_f else []:
            props = f.get("properties") or {}
            tags = self._tags(props)
            names = {props.get("title"), tags.get("name"),
                     tags.get("name:uk"), tags.get("name:en")}
            if low in {n.lower() for n in names if n}:
                return to_3035(shape(f["geometry"]))
        return None


def _box(bbox):
    from shapely.geometry import box
    return box(*bbox)


# ── The network ────────────────────────────────────────────────

def walkable(tags: dict, party: Party) -> float | None:
    """The preference factor for a way, or None if not walked."""
    hw = tags.get("highway")
    if hw is None:
        return None
    factor = HIGHWAY_FACTOR.get(hw, 1.3)
    if factor is None:
        return None
    foot = tags.get("foot")
    if foot == "no":
        return None
    if (tags.get("access") in ("no", "private")
            and foot not in ("yes", "designated", "permissive")):
        return None
    sac = tags.get("sac_scale")
    if sac in SAC and SAC.index(sac) > SAC.index(party.max_sac):
        return None
    vis = tags.get("trail_visibility")
    if (vis in VISIBILITY
            and VISIBILITY.index(vis) > VISIBILITY.index(
                party.max_visibility)):
        return None
    return factor


def _key(xy) -> tuple[int, int]:
    return (round(xy[0] * 10), round(xy[1] * 10))   # 0.1 m


@dataclass
class Network:
    G: nx.DiGraph
    xy: dict                     # node -> (x, y)
    lines: dict                  # edge id -> LineString (u to v)
    tree: STRtree
    node_ids: list


def build_network(ways, ground: Ground, party: Party,
                  strip, places: list[Place]) -> Network:
    marked = []
    parts = []                   # (LineString, tags, osm_id, factor)
    for w in ways:
        if w.tags.get("route") in ("hiking", "foot") and \
                not w.tags.get("highway"):
            marked.append(w.geom)
            continue
        f = walkable(w.tags, party)
        if f is None:
            continue
        for ls in w.geom.geoms:
            if len(ls.coords) >= 2:
                parts.append((ls, w.tags, w.osm_id, f))

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
    marked_u = unary_union(marked).buffer(10) if marked else None
    places_u = (unary_union([p.geom for p in places]).buffer(ENCOUNTER_M)
                if places else None)

    G = nx.DiGraph()
    xy, lines = {}, {}
    eid = 0
    for ls, tags, oid, factor in parts:
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
                u, v = _key(seg.coords[0]), _key(seg.coords[-1])
                if u == v:
                    continue
                xy[u], xy[v] = seg.coords[0], seg.coords[-1]
                up, down = climb(seg, ground)
                f = factor
                if marked_u is not None and seg.within(marked_u):
                    f *= MARKED_FACTOR
                if places_u is not None and seg.intersects(places_u):
                    f *= ENCOUNTER_FACTOR
                f = max(f, MIN_FACTOR)
                eid += 1
                lines[eid] = seg
                for a, b, rise, fall, d in ((u, v, up, down, 1),
                                           (v, u, down, up, -1)):
                    t = din_minutes(seg.length, rise, fall) * party.pace
                    cost = t * f
                    old = G.get_edge_data(a, b)
                    if old is None or old["cost"] > cost:
                        G.add_edge(a, b, eid=eid, dir=d, time=t,
                                   cost=cost, length=seg.length,
                                   up=rise, down=fall,
                                   highway=tags.get("highway"),
                                   name=tags.get("name"), osm=oid)
    if G.number_of_nodes() == 0:
        sys.exit("stage_planner: no walkable paths in this area")
    # Keep the largest connected part, so a snap never lands on an
    # island the route cannot leave.
    biggest = max(nx.weakly_connected_components(G), key=len)
    G = G.subgraph(biggest).copy()
    node_ids = list(G.nodes)
    tree = STRtree([Point(xy[n]) for n in node_ids])
    return Network(G, xy, lines, tree, node_ids)


def climb(seg: LineString, ground: Ground) -> tuple[float, float]:
    """Ascent and descent along a segment, from u to v, in metres."""
    if not ground.known:
        return 0.0, 0.0
    n = max(2, int(math.ceil(seg.length / SAMPLE_M)) + 1)
    pts = [seg.interpolate(d) for d in np.linspace(0, seg.length, n)]
    z = ground.heights(np.array([p.x for p in pts]),
                       np.array([p.y for p in pts]))
    dz = np.diff(z)
    return float(dz[dz > 0].sum()), float(-dz[dz < 0].sum())


def snap(net: Network, p: Point) -> tuple:
    i = net.tree.nearest(p)
    n = net.node_ids[i]
    return n, Point(net.xy[n]).distance(p)


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


def route_between(net: Network, a, b, weight="cost") -> Route | None:
    try:
        nodes = nx.dijkstra_path(net.G, a, b, weight=weight)
    except nx.NetworkXNoPath:
        return None
    return make_route(net, nodes)


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
        legs.append({k: e[k] for k in ("highway", "name", "osm")})
    return Route(nodes, LineString(coords), length, minutes, up, down,
                 along, legs)


def alternatives(net: Network, a, b, best: Route, n: int,
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
                        saved.setdefault((x, y), G[x][y]["cost"])
                        G[x][y]["cost"] *= penalty
            last = route_between(net, a, b)
            if last is None:
                break
            if all(shared(net, last, r) < max_shared for r in found):
                found.append(last)
    finally:
        for (x, y), c in saved.items():
            G[x][y]["cost"] = c
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


def places_along(net: Network, route: Route, places: list[Place],
                 dist: dict, origin: dict, outer, reach_min: float,
                 strip, audience: str, month: str | None) -> list[dict]:
    out = []
    for p in places:
        if audience == "public" and p.is_host:
            continue
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
    return out


# ── Output ─────────────────────────────────────────────────────

def hm(minutes: float) -> str:
    h, m = divmod(int(round(minutes)), 60)
    return f"{h}:{m:02d}"


def feature(geom, **props):
    return {"type": "Feature", "geometry": mapping(to_4326(geom)),
            "properties": props}


def write_geojson(path: Path, routes, rings, places, summary):
    feats = []
    for T, opacity, poly in reversed(rings):
        feats.append(feature(poly, role="band", minutes=T,
                             fill_opacity=opacity))
    outer = rings[-1][2] if rings else None
    if outer is not None:
        polys = getattr(outer, "geoms", [outer])
        for poly in polys:
            feats.append(feature(poly.exterior, role="boundary",
                                 minutes=rings[-1][0]))
    for i, r in enumerate(routes):
        feats.append(feature(r.line, role="route" if i == 0
                             else "alternative", rank=i,
                             km=round(r.length / 1000, 2),
                             time=hm(r.minutes), up_m=round(r.up),
                             down_m=round(r.down)))
    for p in places:
        feats.append({"type": "Feature",
                      "geometry": {"type": "Point",
                                   "coordinates": [p["lon"], p["lat"]]},
                      "properties": {"role": "place", **p}})
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
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',
 {maxZoom: 18, attribution: '© OpenStreetMap contributors'}).addTo(map);
const layer = L.geoJSON(data, {
 style: f => {
  const p = f.properties;
  if (p.role === 'band') return {stroke:false, fillColor:'#2f6f4f', fillOpacity:p.fill_opacity};
  if (p.role === 'boundary') return {color:'#2f6f4f', weight:1.2, opacity:.55, dashArray:'4 6'};
  if (p.role === 'route') return {color:'#9a3412', weight:4};
  if (p.role === 'alternative') return {color:'#9a3412', weight:2.5, opacity:.6, dashArray:'6 6'};
  return {};
 },
 pointToLayer: (f, ll) => L.circleMarker(ll, {radius:6, color:'#fff', weight:1.5,
  fillColor: f.properties.is_host ? '#b45309' : '#1d4ed8', fillOpacity:1}),
 onEachFeature: (f, l) => { const p = f.properties;
  if (p.role === 'place') l.bindPopup(`<b>${p.name}</b><br>${p.kind}<br>`
   + `${p.detour_min} min off the route at km ${p.route_km}`); }
}).addTo(map);
map.fitBounds(layer.getBounds(), {padding:[20,20]});
const ol = document.getElementById('list');
for (const f of data.features.filter(f => f.properties.role === 'place')) {
 const p = f.properties, li = document.createElement('li');
 li.innerHTML = `<b>${p.name}</b> — ${p.kind}<br><small>km ${p.route_km} · `
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
            .replace("__DATA__", data))
    path.write_text(html, encoding="utf-8")


# ── Command ────────────────────────────────────────────────────

def resolve(src, text: str) -> Point:
    p = parse_latlon(text)
    if p is None:
        p = src.find_place(text)
    if p is None:
        sys.exit(f"stage_planner: no place called {text!r} — give "
                 "\"lat,lon\" or a published place's name")
    return p


def _lonlat(p: Point) -> list:
    lon, lat = TO_4326.transform(p.x, p.y)
    return [round(lon, 7), round(lat, 7)]


def criteria(args) -> dict:
    """The criteria a route was made with, so a saved stretch can
    be remade the same way or compared with one made otherwise."""
    return {"version": VERSION, "party": args.party,
            "pace": PARTY[args.party].pace,
            "din_33466": [DIN_FLAT_KMH, DIN_UP_MH, DIN_DOWN_MH],
            "highway_factor": HIGHWAY_FACTOR,
            "marked": MARKED_FACTOR, "encounter": ENCOUNTER_FACTOR,
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
        fc = json.loads(Path(path).read_text(encoding="utf-8"))
        props = fc.get("properties") or {}
        if "stretch" not in props:
            sys.exit(f"stage_planner: {path} is not a stretch "
                     "(written by `route` v0.2 or later)")
        stretches.append((path, fc, props))

    by_min: dict = {}
    lines, places, rows = [], {}, []
    offset_km = offset_min = 0.0
    notices = {OSM_NOTICE}
    prev_end = None
    for path, fc, props in stretches:
        notices.update(props.get("notices", []))
        st = props["route"]
        km = st["km"]
        h, m = st["time"].split(":")
        mins = int(h) * 60 + int(m)
        gap = None
        for f in fc["features"]:
            p, g = f["properties"], to_3035(shape(f["geometry"]))
            if p["role"] == "band":
                by_min.setdefault(p["minutes"], [p["fill_opacity"], []])
                by_min[p["minutes"]][1].append(g)
            elif p["role"] == "route":
                lines.append(g)
                if prev_end is not None:
                    gap = round(Point(g.coords[0]).distance(prev_end))
                prev_end = Point(g.coords[-1])
            elif p["role"] == "place":
                if args.audience == "public" and p.get("is_host"):
                    continue
                q = dict(p)
                q["route_km"] = round(q["route_km"] + offset_km, 2)
                q["route_min"] = round(q["route_min"] + offset_min)
                q["stretch"] = props["stretch"].get("name") or path
                old = places.get(q["id"])
                if old is None or q["detour_min"] < old["detour_min"]:
                    places[q["id"]] = q
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
    found = sorted(places.values(),
                   key=lambda d: (d["route_km"], d["detour_min"]))
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
        feats.append(feature(poly.exterior, role="boundary",
                             minutes=rings[-1][0]))
    for row, line in zip(rows, lines):
        feats.append(feature(line, role="route", **{
            k: row[k] for k in ("stretch", "km", "time", "up_m",
                                "down_m")}))
    for p in found:
        feats.append({"type": "Feature",
                      "geometry": {"type": "Point",
                                   "coordinates": [p["lon"], p["lat"]]},
                      "properties": p})
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
        where = ("on the way" if p.get("on_the_way")
                 else f"{p['detour_min']:.0f} min off")
        print(f"  km {p['route_km']:>5.1f}  {where:>12}  {p['name']} "
              f"({p['kind']})")
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
                         else None)
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
    net = build_network(src.ways(bbox), ground, party, strip, places)
    a, a_off = snap(net, a_pt)
    b, b_off = snap(net, b_pt)
    for label, off in (("start", a_off), ("end", b_off)):
        if off > SNAP_WARN_M:
            print(f"stage_planner: the {label} is {off:.0f} m from the "
                  "nearest path", file=sys.stderr)

    best = route_between(net, a, b)
    if best is None:
        sys.exit("stage_planner: no route between these two points "
                 "with this party's limits")
    routes = [best] + alternatives(net, a, b, best, args.alternatives)
    fastest = route_between(net, a, b, weight="time")

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
                  "time": hm(best.minutes + (a_off + b_off)
                             / OFF_PATH_M_PER_MIN),
                  "up_m": round(best.up), "down_m": round(best.down)},
        "alternatives": [{"km": round(r.length / 1000, 2),
                          "time": hm(r.minutes), "up_m": round(r.up),
                          "down_m": round(r.down)} for r in routes[1:]],
        # What the criteria cost: the quickest way, for the Curator
        # to weigh against the route the criteria chose.
        "fastest": {"km": round(fastest.length / 1000, 2),
                    "time": hm(fastest.minutes), "up_m": round(fastest.up),
                    "down_m": round(fastest.down)},
        "snap_m": {"start": round(a_off), "end": round(b_off)},
        "notices": notices,
        "stored": "nothing — saving a stretch is the Curator's, on Plai",
    }

    out = Path(args.out)
    write_geojson(out, routes, rings, found, summary)
    if args.html:
        write_html(Path(args.html), out, summary,
                   args.name or "Route preview")

    s = summary["route"]
    print(f"Route: {s['km']} km, {s['time']} walking, ↑{s['up_m']} m "
          f"↓{s['down_m']} m ({args.party})")
    for i, r in enumerate(summary["alternatives"], 1):
        print(f"  alternative {i}: {r['km']} km, {r['time']}, "
              f"↑{r['up_m']} m ↓{r['down_m']} m")
    f = summary["fastest"]
    print(f"  quickest way: {f['km']} km, {f['time']}, ↑{f['up_m']} m "
          f"↓{f['down_m']} m")
    print(f"Places within {args.reach:g} min of the route: {len(found)}")
    for p in found:
        where = ("on the way" if p["on_the_way"]
                 else f"{p['detour_min']:.0f} min off")
        print(f"  km {p['route_km']:>5.1f}  {where:>12}  {p['name']} "
              f"({p['kind']})")
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
    args = ap.parse_args(argv)
    if args.cmd == "corridor":
        return cmd_corridor(args)
    if not 1 <= args.reach <= 30:
        ap.error("--reach is minutes, 1 to 30")
    return cmd_route(args)


if __name__ == "__main__":
    sys.exit(main())
