#!/usr/bin/env python3
# Trans-Carpathian Pathways — tests for the stage planner, v0.4
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


def main() -> int:
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
