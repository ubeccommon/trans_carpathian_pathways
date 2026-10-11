# tools/

## stage_planner.py — `route`, v0.1

The routing core of the stage planner (starting prompt §6): from a
start and an end, the route by the project's criteria, up to two
alternatives and the quickest way beside them, a fuzzy band of
2.5, 5, 7.5 and 10 minutes' reach on both sides of the route with
its outer edge as the boundary, and the places within reach in the
order the route meets them, each with its one-way detour.

The criteria, the numbers behind them and who it answers are in the
file's opening comment; every number is named at the top of the
file so it can be changed in one place. It computes on request and
stores nothing (OI-P10); its output carries the ODbL notice and the
GEDTM30 credit.

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

A point is a published Plai place's title, a village or hamlet's
name in OSM, or `"lat,lon"` as a map app copies it. Then, on
schiff, bring the preview back and open it:

```bash
scp ubec-common:/tmp/route.html ubec-common:/tmp/route.geojson /home/farmer/projects/plai/
xdg-open /home/farmer/projects/plai/route.html
```

`route.html` and `route.geojson` are answers, not records: they
are not committed (OI-P10), and with `--audience curator` (the
default) they can hold hosts, so they are not passed on.
