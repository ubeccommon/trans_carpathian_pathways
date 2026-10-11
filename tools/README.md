# tools/

## stage_planner.py — `route` and `corridor`, v0.2

The stage planner (starting prompt §6; spec
`docs/specs/PATHWAYS_STAGE_PLANNER_SPEC_v0_1.md`). Public, on
Michel's word of October 11, 2026: anyone plans with it; the
Curator saves a route as a stretch and joins stretches into a
corridor. `route`, from a
start and an end, the route by the project's criteria, up to two
alternatives and the quickest way beside them, a fuzzy band of
2.5, 5, 7.5 and 10 minutes' reach on both sides of the route with
its outer edge as the boundary, and the places within reach in the
order the route meets them, each with its one-way detour.
`corridor`: stretches `route` wrote, joined into one band, one
boundary and one list, with any gap between them shown.

The criteria, the numbers behind them and who it answers are in the
file's opening comment; every number is named at the top of the
file so it can be changed in one place. It computes on request and
writes nothing but its files; saving a stretch is Plai's, once
`plai/008` is built (spec §4). Every file carries the ODbL notice
and the GEDTM30 credit.

`--audience public` (the default) lists no host; `--audience
curator` lists them, for the Curator's own planning.

### Test, anywhere

```bash
cd /home/farmer/projects/plai && git pull --ff-only
python3 -m venv .venv && . .venv/bin/activate
pip install -r tools/requirements.txt
python3 tools/test_stage_planner.py
```

A made-up valley; it proves the arithmetic and the rules (border
strip, air-raid shelters, hosts left out for a pilgrim), not the
Hutsul paths.

### Run on Plai's data, on ubec-common

From schiff, copy the file over, then run it in Mapservice's
environment, which reads the paths, places and border from the
database and the heights from `$DATA_ROOT/terrain/ground.tif`:

```bash
scp /home/farmer/projects/plai/tools/stage_planner.py ubec-common:/tmp/
ssh ubec-common
cd /home/ubec/ubec_commons/ubec_mapservice && source tools/hostenv.sh
pip install networkx shapely pyproj rasterio     # once, into .venv
python3 /tmp/stage_planner.py route \
    --from "Zhyva Khata" --to "Tepla Gora" \
    --party couple --month oct \
    --out /tmp/route.geojson --html /tmp/route.html
```

Two stretches into a corridor, each written by `route` with
`--name` and its own `--out`:

```bash
python3 /tmp/stage_planner.py corridor --name "Hutsul corridor" \
    /tmp/stretch_1.geojson /tmp/stretch_2.geojson \
    --out /tmp/corridor.geojson --html /tmp/corridor.html
```

A point is a published Plai place's title, a village or hamlet's
name in OSM, or `"lat,lon"` as a map app copies it. Then, on
schiff, bring the preview back and open it:

```bash
scp ubec-common:/tmp/route.html ubec-common:/tmp/route.geojson /home/farmer/projects/plai/
xdg-open /home/farmer/projects/plai/route.html
```

`route.html` and `route.geojson` are answers, not records: they
are not committed. With `--audience curator` they can hold hosts,
so they are not passed on.
