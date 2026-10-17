# tools/

## stage_planner.py — `route`, `corridor`, `find` and `inspect`, v0.13

The stage planner (starting prompt §6; spec
`docs/specs/PATHWAYS_STAGE_PLANNER_SPEC_v0_5.md`). Public, on
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
2026): roads only as the last resort — any continuous run of road
longer than 300 m in a route is walked only where nothing else
joins, and a shorter one links two paths and is part of the way;
every road stretch a route walks is named — then the richest way on
paths within `--allowance` (0.5: up to half again the most direct
way on paths). Footpaths come first — the dotted brown line on
Plai's map before the red line of a marked route. Through towns
and villages the direct way on streets to the next path, unless a
point defined on Plai draws it elsewhere. Each run says
what the way holds — km on footpaths, on marked trails, over the
plai, in forest, over meadows, and on roads.

When a route passes by a path you expected it to take, ask what
the planner knows of that path:

```bash
python3 /tmp/stage_planner.py inspect "<lat,lon of a point on the path>"
```

A click on the preview's map gives that point and the command,
ready to copy.

Paths that stop short of the way they meet are joined: within 10 m
always, and up to 80 m where the path, carried on, meets the other
way and the gap crosses no river or stream. Every gap a route walks
is printed with its place and drawn as a ring on the map — a steward
checks it on the ground, and OSM can be mended.

It names the ways within 150 m of the point, and for each whether
the party walks it and, if not, why (too hard by its `sac_scale`,
`access=private`, …), or whether it is cut off from the network.

### Editing a route — step two of three

The planner proposes; a steward or Curator edits (spec §3a, §3b):

```bash
python3 /tmp/stage_planner.py route --from "Verkhovyna" --to "Zhiva Khata" \
    --via "48.1561,24.8402" \
    --avoid "48.1571,24.8531" \
    --known /tmp/walk.gpx \
    --out /tmp/stretch_1.geojson --html /tmp/stretch_1.html
```

`--via` the way passes there, in order, repeat for more; `--avoid`
closes the ways within 50 m (`--avoid-m`); `--known` a GPX track
walked, or a stretch saved — a way even where OSM has none, and
preferred above everything else. A click on the preview's map gives
any point as `lat,lon`. The stretch keeps what was set, so it can be
remade.

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

## fetch_pathways_basemaps.py and georeference_sheets.py — historic sheets for tracing, v0.1

For the stretches where OSM is not usable. Traced geometry stays in
the project (Michel's word, October 17, 2026) — the tracing grants of
Esri, Bing and Maxar reach only work that goes back into OSM, so what
remains for private tracing is public-domain material: the
Austro-Hungarian Third Military Survey. Its Spezialkarte 1:75 000
sheets (1880s) draw footpaths and mule tracks explicitly — the
historic alignment of the corridor's ways, before the Soviet forestry
roads.

Both scripts run on the host or any machine with open internet; the
sandbox Claude works in cannot reach the archives.

`fetch_pathways_basemaps.py` downloads into `pathways_basemaps/`
(`--out` to change):

- `historic/sdoum_75k/` — Spezialkarte sheets for the Hutsul corridor,
  matched by name (Żabie, Kuty, Kosów, Worochta, Mikuliczyn, Hryniawa,
  Burkut …) and by grid position (Zones 12–14, Kolonnen XXXI–XXXII)
  from the mapywig archive indexed at igrek.amzp.pl. If the index
  layout differs from what the scraper expects, it prints what it
  found and names the series to open in a browser.
- `historic/gkm_200k/` — Generalkarte 1:200 000 overview sheets 42-47
  and 42-48, from Wikimedia Commons.
- `oam/` — whatever OpenAerialMap holds for the corridor, CC-BY 4.0.
  Empty as of October 17, 2026 (`found: 0` for 24.3–25.4 E,
  47.8–48.5 N) — our own drone flights would be the first coverage;
  re-running picks up new uploads.

`georeference_sheets.py` turns the scans into tracing layers. Every
Spezialkarte sheet covers an exact 30′ × 15′ graticule cell, so its
corner coordinates follow from the Zone and Kolonne alone (longitudes
counted from Ferro, Greenwich + 17°40′); what is entered by hand, once
per sheet, is the pixel position of the four neatline corners. Needs
the GDAL command line (`sudo apt install gdal-bin`), nothing from
`requirements.txt`.

```bash
python3 tools/georeference_sheets.py init pathways_basemaps/historic/sdoum_75k
# fill in sheets.csv: zone, kol, the four corner-pixel pairs
python3 tools/georeference_sheets.py warp pathways_basemaps/historic/sdoum_75k --tiles 8 15
```

`warp` writes `georef/<sheet>.tif` (EPSG:4326; `--merc` for 3857,
GCP + thin-plate-spline, internal overviews) and, with `--tiles`, XYZ
tiles under `tiles/<sheet>/` that can be served as static files beside
the mapservice. The computed corners are printed for checking against
the values in the sheet margin (the margin shows Ferro); the csv's
override columns win where the printed values differ.

Accuracy: corner-pinning carries the 1880s survey's own distortion —
tens of metres in high relief. Right for finding the historic
alignment; where a stretch needs precision, that sheet is refined in
the QGIS Georeferencer against local points — churches, bridges,
confluences — of which the corridor has plenty. Wiring the layers into
Plai is a mapservice step, taken when mapservice work resumes.
