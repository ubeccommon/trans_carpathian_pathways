# tools/

## stage_planner.py — `route`, `corridor` and `find`, v0.6

The stage planner (starting prompt §6; spec
`docs/specs/PATHWAYS_STAGE_PLANNER_SPEC_v0_3.md`). Public, on
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

`--audience public` (the default) names published hosts with their
detour time only (SP-3); `--audience
curator` lists them in full, for the Curator's own planning.

The measure is the way, not the time (Michel's word, October 11,
2026): the least road for vehicles first, then the richest way on
paths within `--allowance` (0.5: up to half again the most direct
way on paths). Each run says what the way holds — km on marked
trails, over the plai, in forest, over meadows, and on roads.

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

### Run on Plai's data, on ubec-common — the first real run

Michel's word, October 11, 2026 (SP-5): Verkhovyna – Zhyva Khata –
Tepla Gora – Kosiv, as three stretches joined into one corridor.

From schiff, copy the file over, then run it in Mapservice's
environment, which reads the paths, places and border from the
database and the heights from `$DATA_ROOT/terrain/ground.tif`:

```bash
scp /home/farmer/projects/plai/tools/stage_planner.py ubec-common:/tmp/
ssh ubec-common
cd /home/ubec/ubec_commons/ubec_mapservice && source tools/hostenv.sh
pip install networkx shapely pyproj rasterio     # once, into .venv

python3 /tmp/stage_planner.py route --name "Verkhovyna – Zhyva Khata" \
    --from "Verkhovyna" --to "Zhyva Khata" --party couple --month oct \
    --out /tmp/stretch_1.geojson --html /tmp/stretch_1.html
python3 /tmp/stage_planner.py route --name "Zhyva Khata – Tepla Gora" \
    --from "Zhyva Khata" --to "Tepla Gora" --party couple --month oct \
    --out /tmp/stretch_2.geojson --html /tmp/stretch_2.html
python3 /tmp/stage_planner.py route --name "Tepla Gora – Kosiv" \
    --from "Tepla Gora" --to "Kosiv" --party couple --month oct \
    --out /tmp/stretch_3.geojson --html /tmp/stretch_3.html
python3 /tmp/stage_planner.py corridor --name "Verkhovyna – Kosiv" \
    /tmp/stretch_1.geojson /tmp/stretch_2.geojson /tmp/stretch_3.geojson \
    --out /tmp/corridor.geojson --html /tmp/corridor.html
```

A point is a published Plai place's title, a village, peak or other
named place in OSM — in Latin or Cyrillic, "Tepla Gora" finds Тепла
Гора — or `"lat,lon"` as a map app copies it. Before the run, see
what each name matches:

```bash
python3 /tmp/stage_planner.py find "Zhyva Khata"
python3 /tmp/stage_planner.py find "Tepla Gora"
```

If a name matches nothing, or several places far apart, give that
point as `"lat,lon"` instead, the same in both stretches it joins. Add `--audience curator` to see hosts in
full.

Then, on schiff, bring the previews back and open them:

```bash
scp "ubec-common:/tmp/{stretch_1,stretch_2,stretch_3,corridor}.html" /home/farmer/projects/plai/
xdg-open /home/farmer/projects/plai/corridor.html
```

The `.html` and `.geojson` files are answers, not records: they
are not committed. With `--audience curator` they can hold hosts,
so they are not passed on.
