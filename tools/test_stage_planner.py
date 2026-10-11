#!/usr/bin/env python3
# Trans-Carpathian Pathways — tests for the stage planner, v0.10
# SPDX-License-Identifier: AGPL-3.0-or-later
"""A made-up valley near Verkhovyna, built in a temporary folder:
a secondary road on the valley floor, contour paths on both slopes
(one marked as a hiking route, one too hard for anyone), tracks
across them, a ridge to the south inside a border strip, and a few
places — two to find, three that must never be listed.

Run from the repository root:  python3 tools/test_stage_planner.py
Nothing here is real data; the real check is on the host.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import stage_planner as sp  # noqa: E402

X0, Y0 = sp.TO_3035.transform(24.79, 48.15)
LEN = 8000.0


def ll(x, y):
    lon, lat = sp.TO_4326.transform(X0 + x, Y0 + y)
    return [round(lon, 8), round(lat, 8)]


def height(x, y):
    return 650 + 450 * (1 - math.exp(-(y / 1100.0) ** 2)) \
        + 40 * math.sin(x / 1300.0)


def build(tmp: Path):
    xs = [i * 1000.0 for i in range(9)]
    rows = {0: "secondary", 600: "path", 1200: "path", -600: "path",
            -1200: "path"}
    feats = []
    for y, hw in rows.items():
        # vertices every 100 m, so each crossing is a shared vertex
        coords = [ll(x, y) for x in np.arange(0, LEN + 1, 100.0)]
        tags = {"highway": hw, "name": f"row {y}"}
        if y == 1200:
            tags["sac_scale"] = "demanding_alpine_hiking"
        feats.append({"type": "Feature", "properties": {"tags": tags},
                      "geometry": {"type": "LineString",
                                   "coordinates": coords}})
    for x in xs:
        coords = [ll(x, y) for y in np.arange(-1200, 1201, 100.0)]
        feats.append({"type": "Feature",
                      "properties": {"tags": {"highway": "track"}},
                      "geometry": {"type": "LineString",
                                   "coordinates": coords}})
    feats.append({"type": "Feature", "properties": {"tags": {
        "type": "route", "route": "hiking", "name": "Marked trail"}},
        "geometry": {"type": "LineString", "coordinates": [
            ll(x, 600) for x in np.arange(0, LEN + 1, 100.0)]}})
    (tmp / "paths.geojson").write_text(json.dumps(
        {"type": "FeatureCollection", "features": feats}))

    def pt(x, y, **props):
        return {"type": "Feature", "properties": props,
                "geometry": {"type": "Point", "coordinates": ll(x, y)}}

    places = [
        pt(3000, 700, tags={"tourism": "viewpoint", "name": "Kamin"}),
        pt(5000, 640, tags={"natural": "spring", "name": "Dzherelo"}),
        pt(6000, 660, title="Hutsul house", is_host=True,
           offers="Overnight stay · A meal", season="", source="plai"),
        pt(4500, 60, tags={"amenity": "shelter",
                           "bunker_type": "personnel_shelter",
                           "name": "Ukryttia"}),
        pt(4000, 2600, tags={"tourism": "viewpoint", "name": "Far"}),
        pt(2000, -1300, tags={"tourism": "viewpoint", "name": "Ridge"}),
        pt(0, 0, tags={"place": "village", "name": "Startove"}),
        pt(4000, 600, tags={"place": "hamlet", "name": "Тепла Гора"}),
        pt(1000, 300, tags={"place": "hamlet", "name": "Dvi Khaty"}),
        pt(7000, 300, tags={"place": "hamlet", "name": "Dvi Khaty"}),
    ]
    (tmp / "places.geojson").write_text(json.dumps(
        {"type": "FeatureCollection", "features": places}))

    strip = [ll(-500, -2000), ll(LEN + 500, -2000), ll(LEN + 500, -900),
             ll(-500, -900), ll(-500, -2000)]
    (tmp / "strip.geojson").write_text(json.dumps(
        {"type": "FeatureCollection", "features": [{
            "type": "Feature", "properties": {},
            "geometry": {"type": "Polygon", "coordinates": [strip]}}]}))

    import rasterio
    from rasterio.transform import from_origin
    res = 30.0
    w, h = int((LEN + 2000) / res), int(6000 / res)
    left, top = X0 - 1000, Y0 + 3000
    arr = np.empty((h, w), "float32")
    for r in range(h):
        for c in range(w):
            arr[r, c] = height(left + (c + .5) * res - X0,
                               top - (r + .5) * res - Y0)
    with rasterio.open(tmp / "ground.tif", "w", driver="GTiff",
                       height=h, width=w, count=1, dtype="float32",
                       crs="EPSG:3035",
                       transform=from_origin(left, top, res, res)) as ds:
        ds.write(arr, 1)


def run(tmp: Path, *extra, out_name="out.geojson") -> dict:
    out = tmp / out_name
    cmd = [sys.executable, str(HERE / "stage_planner.py"), "route",
           "--source", "files", "--paths", str(tmp / "paths.geojson"),
           "--places", str(tmp / "places.geojson"),
           "--border-strip", str(tmp / "strip.geojson"),
           "--dem", str(tmp / "ground.tif"),
           "--from", "Startove", "--to",
           "{1},{0}".format(*ll(LEN, 0)),
           "--out", str(out), "--html", str(tmp / "out.html"), *extra]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print(res.stdout, res.stderr, sep="")
    assert res.returncode == 0, res.returncode
    return json.loads(out.read_text())


GEOJSON_TYPES = {"Point", "MultiPoint", "LineString", "MultiLineString",
                 "Polygon", "MultiPolygon", "GeometryCollection"}


def assert_geojson(fc: dict):
    """Only RFC 7946 geometry types, or null (a host, SP-3)."""
    for x in fc["features"]:
        g = x["geometry"]
        assert g is None or g["type"] in GEOJSON_TYPES, g and g["type"]


def tiny_network(edges):
    """A network by hand: (u, v, minutes, q, road) both ways."""
    import networkx as nx
    from shapely.geometry import LineString
    G, lines, xy = nx.DiGraph(), {}, {}
    pos = {"A": (0, 0), "B": (1000, 0), "S": (500, 400), "R": (500, -10),
           "P": (500, -500)}
    for i, (u, v, t, q, road) in enumerate(edges, 1):
        lines[i] = LineString([pos[u], pos[v]])
        xy[u], xy[v] = pos[u], pos[v]
        for a, b, d in ((u, v, 1), (v, u, -1)):
            G.add_edge(a, b, eid=i, dir=d, time=t, q=q, road=road,
                       kinds={"marked": 0, "plai": 0, "forest": 0,
                              "meadow": 0},
                       length=lines[i].length, up=0, down=0,
                       highway="path", name=None, osm=str(i))
    return sp.Network(G, xy, lines, None, list(G.nodes))


def test_the_way():
    # direct path A-B 60 min, plain; scenic A-S-B 80 min, rich
    net = tiny_network([("A", "B", 60, 0.0, 0),
                        ("A", "S", 40, 0.6, 0),
                        ("S", "B", 40, 0.6, 0)])
    way, direct, _ = sp.the_way(net, "A", "B", 0.5)
    assert direct.nodes == ["A", "B"] and way.nodes == ["A", "S", "B"]
    way, _, _ = sp.the_way(net, "A", "B", 0.2)      # 80 > 72: too far
    assert way.nodes == ["A", "B"], way.nodes
    R = sp.MINOR_ROAD_WEIGHT
    # 10 minutes of village road against 40 on a path: the path
    net = tiny_network([("A", "R", 5, 0.0, R), ("R", "B", 5, 0.0, R),
                        ("A", "P", 20, 0.0, 0), ("P", "B", 20, 0.0, 0)])
    way, direct, _ = sp.the_way(net, "A", "B", 0.0)
    assert way.nodes == ["A", "P", "B"], way.nodes
    # against 200 on a path: a short road linking paths is walked
    net = tiny_network([("A", "R", 5, 0.0, R), ("R", "B", 5, 0.0, R),
                        ("A", "P", 100, 0.0, 0), ("P", "B", 100, 0.0, 0)])
    way, _, _ = sp.the_way(net, "A", "B", 0.0)
    assert way.nodes == ["A", "R", "B"], way.nodes
    # and a road where nothing else joins
    net = tiny_network([("A", "R", 5, 0.0, R), ("R", "B", 5, 0.0, R)])
    way, _, _ = sp.the_way(net, "A", "B", 0.5)
    assert way.nodes == ["A", "R", "B"]


def test_footpaths_first():
    """A footpath beside a marked track: the footpath, though longer;
    a path drawn 6 m short of the track is joined to it."""
    from shapely.geometry import LineString, MultiLineString
    W = lambda oid, coords, **tags: sp.Way(oid, None, tags,
                                           MultiLineString([coords]))
    ways = [W("track", [(0, 0), (1000, 0)], highway="track"),
            W("route", [(0, 0), (1000, 0)], type="route", route="hiking"),
            W("path", [(0, 0), (500, 150), (1000, 0)], highway="path"),
            W("short", [(500, -200), (500, -6)], highway="path")]
    box = (-100, -300, 1100, 300)
    net = sp.build_network(ways, sp.Ground(None, box), sp.PARTY["couple"],
                           None, sp.Landscape())
    a, _ = sp.snap(net, sp.Point(0, 0))
    b, _ = sp.snap(net, sp.Point(1000, 0))
    way, direct, _ = sp.the_way(net, a, b, 0.5)
    assert direct.length < 1001, direct.length          # the track
    assert way.length > 1040, "the footpath, not the marked track"
    assert sp.what_the_way_holds(way)["footpath_km"] >= 1.0
    c, _ = sp.snap(net, sp.Point(500, -200))
    assert sp.route_between(net, c, b) is not None, "short path joined"


def test_obvious_gaps():
    """A path stopping 50 m short of a track, heading at it: joined.
    Heading past it: not joined. With a stream in the gap: not
    joined."""
    from shapely.geometry import LineString, MultiLineString
    W = lambda oid, coords, **tags: sp.Way(oid, None, tags,
                                           MultiLineString([coords]))
    box = (-100, -400, 1100, 400)

    def joined(ways, water=None):
        net = sp.build_network(ways, sp.Ground(None, box),
                               sp.PARTY["couple"], None, sp.Landscape(),
                               water)
        a, _ = sp.snap(net, sp.Point(0, 0))
        b, _ = sp.snap(net, sp.Point(550, 300))
        r = sp.route_between(net, a, b)
        return r, net

    track = W("t", [(550, -300), (550, 300)], highway="track")
    r, net = joined([W("p", [(0, 0), (500, 0)], highway="path"), track])
    assert r is not None, "a 50 m gap ahead of the path is joined"
    gaps = sp.gaps_on(net, r)
    assert len(gaps) == 1 and gaps[0]["gap_m"] == 50, gaps
    # heading north, the track 50 m to the side: no obvious connection
    side = [W("p", [(0, 0), (500, 0), (500, 200)], highway="path"),
            W("t", [(550, 100), (550, 300)], highway="track")]
    net = sp.build_network(side, sp.Ground(None, box), sp.PARTY["couple"],
                           None, sp.Landscape())
    assert net.G.number_of_nodes() <= 3, "the sideways track stays apart"
    # a stream in the gap
    stream = LineString([(525, -400), (525, 400)])
    _, net = joined([W("p", [(0, 0), (500, 0)], highway="path"), track],
                    water=stream)
    assert not any(d["highway"] == "gap"
                   for _, _, d in net.G.edges(data=True)), \
        "no gap joined across a stream"


def test_roads_last_resort():
    """150 m of village road between two paths: a link, walked. 400 m:
    a last resort, passed by for a path round. A road where nothing
    else joins: walked, and named as the last resort."""
    from shapely.geometry import MultiLineString
    W = lambda oid, coords, **tags: sp.Way(oid, None, tags,
                                           MultiLineString([coords]))
    box = (-100, -100, 1100, 900)

    def way(road_to, detour=True):
        ways = [W("p1", [(0, 0), (400, 0)], highway="path"),
                W("r", [(400, 0), (road_to, 0)], highway="residential"),
                W("p2", [(road_to, 0), (1000, 0)], highway="path")]
        if detour:
            ways.append(W("d", [(0, 0), (500, 800), (1000, 0)],
                          highway="path"))
        net = sp.build_network(ways, sp.Ground(None, box),
                               sp.PARTY["couple"], None, sp.Landscape())
        a, _ = sp.snap(net, sp.Point(0, 0))
        b, _ = sp.snap(net, sp.Point(1000, 0))
        r, _, _ = sp.the_way(net, a, b, 0.5)
        return r, sp.road_links_on(net, r)

    r, roads = way(550)
    assert r.length < 1001 and len(roads) == 1 and roads[0]["link"] \
        and roads[0]["m"] == 150, (r.length, roads)
    r, roads = way(800)
    assert r.length > 1800 and not roads, (r.length, roads)
    r, roads = way(800, detour=False)
    assert len(roads) == 1 and not roads[0]["link"], roads


def main() -> int:
    test_the_way()
    test_footpaths_first()
    test_obvious_gaps()
    test_roads_last_resort()
    # DIN 33466 by hand
    assert sp.din_minutes(4000, 0, 0) == 60
    assert sp.din_minutes(0, 300, 0) == 60
    assert sp.din_minutes(0, 0, 500) == 60
    assert sp.din_minutes(4000, 300, 0) == 90
    # a Latin spelling meets the Cyrillic name
    for a, b in (("Zhyva Khata", "Жива Хата"), ("Tepla Gora", "Тепла Гора"),
                 ("Verkhovyna", "Верховина"), ("Kosiv", "Косів")):
        assert sp.loose(a) == sp.loose(b), (a, b)

    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        build(tmp)
        fc = run(tmp, "--audience", "curator")
        f = fc["features"]
        route = next(x for x in f if x["properties"]["role"] == "route")
        from shapely.geometry import shape
        line = sp.to_3035(shape(route["geometry"]))
        strip = sp.to_3035(shape(json.loads(
            (tmp / "strip.geojson").read_text())["features"][0]
            ["geometry"]))
        assert not line.intersects(strip), "route enters the strip"
        # off the beaten path: most of it not on the valley road
        on_road = line.intersection(
            sp.to_3035(shape({"type": "LineString", "coordinates":
                              [ll(0, 0), ll(LEN, 0)]})).buffer(5))
        assert on_road.length < 0.35 * line.length, on_road.length
        # never on the too-hard row
        hard = sp.to_3035(shape({"type": "LineString", "coordinates":
                                 [ll(0, 1200), ll(LEN, 1200)]}))
        assert line.intersection(hard.buffer(5)).length < 1

        names = {x["properties"]["name"] for x in f
                 if x["properties"]["role"] == "place"}
        assert {"Kamin", "Dzherelo", "Hutsul house"} <= names, names
        assert not names & {"Ukryttia", "Far", "Ridge"}, names
        for x in f:
            p = x["properties"]
            if p["role"] == "place":
                assert p["detour_min"] <= 10

        bands = sorted((x for x in f if x["properties"]["role"] == "band"),
                       key=lambda x: x["properties"]["minutes"])
        assert len(bands) == 4
        areas = [sp.to_3035(shape(b["geometry"])).area for b in bands]
        assert areas == sorted(areas), areas
        assert any(x["properties"]["role"] == "boundary" for x in f)
        assert_geojson(fc)
        assert sp.OSM_NOTICE in fc["properties"]["notices"]
        # the way stays within its allowance over the most direct way
        d = fc["properties"]["direct"]
        hmin = lambda t: int(t.split(":")[0]) * 60 + int(t.split(":")[1])
        assert hmin(fc["properties"]["route"]["time"]) <= \
            hmin(d["time"]) * (1 + d["allowance"]) + 2, (fc["properties"])
        assert fc["properties"]["stored"].startswith("nothing")
        assert fc["properties"]["stretch"]["criteria"]["party"] == "couple"

        # public, the default: a host by name and detour time only
        fc = run(tmp, "--party", "family")
        hosts = [x for x in fc["features"]
                 if x["properties"].get("is_host")]
        assert len(hosts) == 1, hosts
        assert hosts[0]["geometry"] is None
        assert set(hosts[0]["properties"]) == {
            "name", "is_host", "detour_min", "order", "role"}, hosts
        orders = [x["properties"]["order"] for x in fc["features"]
                  if x["properties"]["role"] == "place"]
        assert orders == sorted(orders) == list(range(len(orders)))

        # a point beside a long path joins it there, not at a junction
        side = "{1},{0}".format(*ll(2500, 640))
        fc = run(tmp, "--from", side, out_name="side.geojson")
        r = next(x for x in fc["features"]
                 if x["properties"]["role"] == "route")
        line = sp.to_3035(shape(r["geometry"]))
        first, joined = (sp.Point(line.coords[0]),
                         sp.Point(line.coords[1]))
        start = sp.to_3035(shape({"type": "Point",
                                  "coordinates": ll(2500, 640)}))
        assert first.distance(start) < 1, "the route reaches the point"
        assert joined.distance(sp.to_3035(shape(
            {"type": "Point", "coordinates": ll(2500, 600)}))) < 2, \
            "joined mid-path, not at a junction"
        roles = {x["properties"]["role"] for x in fc["features"]}
        assert {"start", "end"} <= roles, roles
        assert_geojson(fc)
        # a road is walked where nothing else reaches the point
        onroad = "{1},{0}".format(*ll(4500, 0))
        fc = run(tmp, "--from", onroad, out_name="onroad.geojson")
        assert fc["properties"]["route"]["km"] > 0

        # inspect says what lies at a point
        res = subprocess.run(
            [sys.executable, str(HERE / "stage_planner.py"), "inspect",
             "{1},{0}".format(*ll(2500, 600)), "--source", "files",
             "--paths", str(tmp / "paths.geojson")],
            capture_output=True, text=True)
        assert res.returncode == 0 and "footpath, first among paths" in \
            res.stdout, res.stdout + res.stderr
        res = subprocess.run(
            [sys.executable, str(HERE / "stage_planner.py"), "inspect",
             "{1},{0}".format(*ll(2500, 1200)), "--source", "files",
             "--paths", str(tmp / "paths.geojson")],
            capture_output=True, text=True)
        assert "harder than this party walks" in res.stdout, res.stdout

        # a Latin name finds a Cyrillic place
        fc = run(tmp, "--to", "Tepla Gora", out_name="tg.geojson")
        assert fc["properties"]["route"]["km"] > 4
        # two places of one name far apart: listed, not guessed
        res = subprocess.run(
            [sys.executable, str(HERE / "stage_planner.py"), "route",
             "--source", "files", "--paths", str(tmp / "paths.geojson"),
             "--places", str(tmp / "places.geojson"),
             "--from", "Dvi Khaty", "--to", "Startove"],
            capture_output=True, text=True)
        assert res.returncode != 0 and "2 places match" in res.stderr, \
            res.stderr
        # find
        res = subprocess.run(
            [sys.executable, str(HERE / "stage_planner.py"), "find",
             "tepla hora", "--source", "files",
             "--places", str(tmp / "places.geojson")],
            capture_output=True, text=True)
        assert res.returncode == 0 and "Тепла Гора" in res.stdout, res
        # a missing stretch file is said plainly
        res = subprocess.run(
            [sys.executable, str(HERE / "stage_planner.py"), "corridor",
             str(tmp / "nope.geojson")], capture_output=True, text=True)
        assert "does not exist" in res.stderr and "Traceback" not in \
            res.stderr, res.stderr

        # two stretches joined into a corridor
        mid = "{1},{0}".format(*ll(4000, 600))
        end = "{1},{0}".format(*ll(LEN, 0))
        a = run(tmp, "--audience", "curator", "--name", "West",
                "--to", mid, out_name="west.geojson")
        b = run(tmp, "--audience", "curator", "--name", "East",
                "--from", mid, "--to", end, out_name="east.geojson")
        pa = run(tmp, "--name", "West", "--to", mid,
                 out_name="west_public.geojson")
        pb = run(tmp, "--name", "East", "--from", mid, "--to", end,
                 out_name="east_public.geojson")
        res = subprocess.run(
            [sys.executable, str(HERE / "stage_planner.py"), "corridor",
             str(tmp / "west_public.geojson"),
             str(tmp / "east_public.geojson"),
             "--out", str(tmp / "corridor_public.geojson")],
            capture_output=True, text=True)
        assert res.returncode == 0, res.stderr
        cpub = json.loads((tmp / "corridor_public.geojson").read_text())
        assert_geojson(cpub)
        h = [x for x in cpub["features"] if x["properties"].get("is_host")]
        assert len(h) == 1 and h[0]["geometry"] is None, h
        for aud, host in (("curator", True), ("public", False)):
            # host: whether the host's place may be in the answer
            cmd = [sys.executable, str(HERE / "stage_planner.py"),
                   "corridor", "--name", "Test corridor",
                   "--audience", aud, str(tmp / "west.geojson"),
                   str(tmp / "east.geojson"),
                   "--out", str(tmp / "corridor.geojson"),
                   "--html", str(tmp / "corridor.html")]
            res = subprocess.run(cmd, capture_output=True, text=True)
            print(res.stdout, res.stderr, sep="")
            assert res.returncode == 0
            c = json.loads((tmp / "corridor.geojson").read_text())
            assert_geojson(c)
            cp = c["properties"]
            assert abs(cp["route"]["km"] - a["properties"]["route"]["km"]
                       - b["properties"]["route"]["km"]) < 0.02
            assert cp["corridor"]["stretches"][1][
                "gap_m_from_previous"] == 0
            names = {x["properties"]["name"] for x in c["features"]
                     if x["properties"].get("role") == "place"}
            assert {"Kamin", "Dzherelo"} <= names, names
            assert "Hutsul house" in names, names
            h = next(x for x in c["features"]
                     if x["properties"].get("is_host"))
            assert (h["geometry"] is not None) == host, h
            assert ("route_km" in h["properties"]) == host, h
            bands = sorted((x for x in c["features"]
                            if x["properties"]["role"] == "band"),
                           key=lambda x: x["properties"]["minutes"])
            areas = [sp.to_3035(shape(x["geometry"])).area for x in bands]
            assert len(areas) == 4 and areas == sorted(areas)

    print("stage_planner: all tests pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
