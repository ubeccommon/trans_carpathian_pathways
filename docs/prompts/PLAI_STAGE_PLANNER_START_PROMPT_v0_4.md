---
title: "PLAI_STAGE_PLANNER_START_PROMPT_v0_4"
subtitle: "Starting prompt — the pathway planner on Plai: a planned pathway saved in the database and edited after"
author: "Michel Garand"
date: "October 2026"
version: "v0.4"
lang: "en"
license: "CC BY-SA 4.0"
project: "Trans-Carpathian Pathways"
status: "to paste as the first message of a new conversation"
---

*Paste everything below the line as the first message of a new
conversation in the Claude Project "Trans Carpathian Pathway".
It works on the pathway planner inside the map service, starting
from Michel's question of October 11, 2026.*

* * *

## 0. The question this conversation starts from

> **When a pathway is created by the planner, is it saved in the
> database so we can edit it after?**

**As things stand: no.** The planner
(`tools/stage_planner.py` v0.13) computes on request and writes
only files: a `.geojson` (the route, band and places, with a
`stretch` block holding everything needed to remake it) and an
`.html` preview. Nothing reaches a database. The tables a saved
stretch would live in (`instance_sa.stretch`, `corridor`,
`corridor_stretch`, as Plai migration `plai/008`, spec §4 and §7)
are designed on paper and not built.

This conversation's work is to make the answer **yes**, inside
the map service:

1. **Plan:** the planner proposes a route in Plai's Pathways
   application (`ubec_plai_hub_tcp`).
2. **Save:** a logged-in steward or Curator saves it as a
   **draft stretch** in Plai's database.
3. **Edit:** it can be opened again later, edited with Mapbender's
   Digitizer (via points, avoid points, a line of one's own, a GPX
   track), routed again, and saved again.
4. **Publish:** only a Curator publishes it; withdrawal removes it
   from every service.
5. **Remember:** saved and walked stretches become the planner's
   best knowledge, preferred on the next plan (step three of three,
   spec §3a).

Not in scope: re-tuning what the engine decides (its numbers are
Michel's or the Curator's to change, in the Pathways
conversation); the multi-day `stages` piece; the white paper,
proposal or plan, which are revised only when Michel says so
(SP-6).

## 1. Load order — before any work

1. Attach `ubeccommon/ubec_mapservice` with **push** access and
   `ubeccommon/trans_carpathian_pathways` with **read** access.
   Clone both. In the Pathways tree, switch to the branch
   **`stage-planner-route`**: the planner is there and is not yet
   merged to `main`. This conversation writes `ubec_mapservice` on
   Michel's word of October 11, 2026, for this named change.
2. In the mapservice tree, read the latest
   `docs/UBEC_MAPSERVICE_CLAUDE_PROMPT`: §1, §2, §4, §5 and §9, and
   in §3 the entries on the Carpathian hub and Plai, Plai's entry
   surface and the map search. Its rules bind this work:
   - one instance, one database;
   - no secrets; reproducible from the tree;
   - licence classes are held by the database (ODbL in
     `instance_sa`);
   - exposure is a decision: a leak pass over every new endpoint
     before it faces anyone;
   - logs kept short;
   - the checker before any `.md`;
   - commits authored as Michel Garand, from a pulled tree.
3. In the Pathways tree, read in full:
   - `docs/specs/PATHWAYS_STAGE_PLANNER_SPEC_v0_4.md`, especially
     §3a (the three steps), §3b (the editor, integrated in the map
     service), §4 (a stretch), §6 (where it runs) and §7 (a
     corridor);
   - `tools/stage_planner.py` and `tools/README.md`: the engine,
     its `route`, `corridor`, `find` and `inspect` commands, and
     its `--via`, `--avoid` and `--known` flags;
   - `docs/specs/PATHWAYS_OPEN_DATA_SPEC_v0_3.md` §2: a host is
     never a waypoint in a public file.
4. In the mapservice tree, read what this work follows:
   - `db/instances/plai/`: the entry tables, the host fields, the
     published view `entry_public`, the publication states and
     their guards, and any history or audit an entry already keeps;
   - how Plai's Digitizer saves an entry today: its feature type in
     `mapbender/exports/ubec_plai_hub_tcp.yaml` and the Plai
     entry applications, which table and SRID it writes, and how
     the saver's Mapbender identity and group reach the row;
   - `stack/search/` (`app.py`, `Dockerfile`), the migrations that
     gave it its role (015, 016), `stack/docker-compose.yml` and
     `stack/nginx/mapservice.ubec.network`: the precedent for a
     small service;
   - `tools/terrain.py`: where `ground.tif` lives and how it is
     mounted.
5. Only then begin, with Gate A.

## 2. What is known already

- **The engine, v0.13.** It is written in Python, holds a
  networkx graph in memory, and reads:
  - `reference_sa.osm_line`, `osm_point`, `osm_polygon` and
    `reference.admin_unit` in the framework database;
  - `instance.entry_public` in Plai's database;
  - `$DATA_ROOT/terrain/ground.tif` and `canopy.tif`.

  The measure is "the pathway is the way", not the shortest or
  fastest:
  - Footpaths (the dotted brown line) come before marked routes.
  - Roads are the last resort: a run of road over 300 m is walked
    only where nothing else joins.
  - Through towns it takes the direct way, unless a point defined
    on Plai draws it elsewhere.
  - Obvious gaps of up to 80 m between paths are joined and
    flagged.
  - Known ways (walked GPX tracks, saved stretches) are preferred
    above everything.

  Every run reports its doubts: road runs, gaps, and km through
  towns. Before an answer leaves the planner, a public answer names
  each published host with its detour time only (SP-3); a Curator's
  answer lists hosts in full.
- **The first real run (SP-5)** was made by hand on ubec-common:
  Verkhovyna, Zhiva Khata, Tepla Gora, Kosiv, as three stretches and
  one corridor of about 78 km. Two things remain wrong in it:
  - a zig-zag through Verkhovyna;
  - long last-resort roads on the third stretch.

  Both are meant to be settled by editing (step two), not by more
  tuning. That is why saving and editing come next.
- **What a stretch carries.** The engine's `stretch` block already
  holds the start and end as entered, `via`, `avoid`, `avoid_m`,
  `known` and `criteria` (the party, the numbers and the planner's
  version). Spec §4 adds the columns for `own_lines`, `tracks`,
  `gap_checks`, `road_checks`, `state`, `saved_by`, `curator`,
  `steward` and `note`. **The list of places is never stored:** it
  is asked for again each time the stretch is shown, so a withdrawn
  host leaves at once.
- **Who does what (SP-1).** Anyone plans. A steward
  (`PLAI_STEWARD`) or a Curator (`PLAI_CURATOR`) saves a draft.
  Only a Curator publishes, and only a Curator joins stretches into
  a corridor.
- **The editor is in the map service (Michel's word, October 11,
  2026).** It is not a page of its own. It lives inside the
  Pathways application, on the same map and behind the same login,
  and uses the Digitizer as Plai's entries do.
- **The precedent.** The map search is a small Starlette service
  in its own image, reachable only on the compose network, through
  a role that may read nothing but its table, with a two-second
  limit on every statement. The planner service has the same shape,
  with more to read and more time to think.

## 3. The questions to settle — for Michel's word

Claude proposes, each with the lever it uses in the tree; Michel
decides. Nothing of Claude's is recorded as decided.

1. **What is saved.** Both what the planner drew (the line and
   the band) and what made it (the start, end, via, avoid, own
   lines, tracks and criteria), so that a stretch can be shown
   without the planner and remade with it. Which of these goes in
   columns and which in jsonb; the SRID on disk (EPSG:3035 as the
   spec says) and the SRID the Digitizer edits in.
2. **Editing after, in two kinds:**
   - **Changing the inputs and routing again:** move a via point,
     add an avoid point, upload a track; the planner remakes the
     line.
   - **Hand-editing the line itself** with the Digitizer.

   When both happen, what wins? One option: a hand-drawn piece
   becomes an own line, kept as a known way, so a later re-route
   follows it rather than undoing it.
3. **History.** Whether each save keeps the version before it, as
   a version table or as Plai's own audit, if it has one. Whether
   a steward can see and restore an earlier version.
4. **Rights on a saved stretch:**
   - Whether a steward edits only their own drafts, and a Curator
     any.
   - Whether editing a published stretch makes a new draft beside
     it, with the published one staying public until the Curator
     publishes the change.
   - What withdrawal does to the corridors a stretch is in.
5. **A visitor who is not logged in.** Nothing is saved for them.
   Whether they may take the answer away as GeoJSON or GPX, or as
   a link that remakes it from its inputs. Such a link would hold
   points, never a host's place.
6. **When the save happens.**
   - Whether the band is recomputed on every save, or only by the
     planner.
   - Whether the gap and road checks a steward records stay with
     the stretch when it is routed again, if the gap or road is
     still on the way.
7. **How a saved stretch becomes known.** Once published, or
   already as a draft, for the one who saved it. How the service
   reads saved stretches as known ways (today: `--known` with a
   file).
8. **The service and the elements:**
   - the service's image, role, grants, time limits and abuse
     thresholds;
   - how the browser reaches it: an nginx location, or through
     Mapbender;
   - how the engine reaches the image: copied from a pinned
     Pathways commit, or vendored — one home for the code;
   - which Mapbender elements carry plan, save, open, edit and
     publish, read at the pinned tag.

## 4. Gates

Gate by gate; a gate opens on Michel's word.

- **Gate A — what is there, and the answer as it stands.** Read
  as §1 says, then report to Michel:
  - how Plai saves, versions, publishes and withdraws an entry
    today;
  - what the Digitizer writes, in which table and SRID, and with
    which identity;
  - what of that a stretch can reuse;
  - a plain answer to §0's question, with what is missing to make
    it yes.

  Nothing is built before this.
- **Gate B — the design, as a list.** §3, item by item, for
  Michel's word: `plai/008` (tables, guards, grants, history), the
  service, the elements and the editor, and what a visitor sees
  (English first, SP-7; WCAG 2.2 AA).
- **Gate C — built in the tree:**
  - the migration, the service and the Mapbender application
    changes, as files in `ubec_mapservice`;
  - tests, including a save, a reopen, an edit and a save again;
  - README and prompt bumped; checker PASS;
  - one commit as Michel Garand.

  The Pathways tree is not written from this conversation; what
  Pathways must record is handed back as a short note.
- **Gate D — on the host.** Michel pulls, migrates, builds,
  restarts, and reloads nginx if its file changed. He runs the leak
  pass over every new endpoint and answer: in a public answer, no
  host has a place, an offer, a kind, a kilometre or a geometry.

  Then he walks it:
  1. Plan Verkhovyna – Zhiva Khata in the Pathways application.
  2. Save it as a steward's draft, and log out.
  3. Log in again, **open the saved draft**, and add a via point
     through Verkhovyna and an avoid point.
  4. Route it again, hand-edit a piece of the line, and save.
  5. See the earlier version in its history.
  6. Publish it as the Curator.
  7. Plan again nearby, and see the published stretch preferred.
  8. Withdraw a test host and see it leave every answer.

  Closes on his "looks good", and with it Pathways Gate 5.

## 5. Open — for Michel, when they arise

- The address and name of the planner in the Pathways application.
- Its languages: English first (SP-7), or English and Ukrainian
  from the start.
- Whether a visitor may download GPX as well as GeoJSON.
- How long the service may think before it says no, and how many
  answers one visitor may ask for in an hour.

## 6. Working rules

- Use Python for any tool and for the service. No secrets.
  Everything is in the tree and mounted; nothing lives only on the
  server.
- Use the real checkout paths in every pull or host command:
  - on ubec-common: `/home/ubec/ubec_commons/ubec_mapservice`, as
    `ubec`, after `source tools/hostenv.sh`;
  - on schiff: `/home/farmer/projects/plai`, as `farmer`;
  - from schiff, reach the host with `ssh ubec-common`.
- Verify every Mapbender claim against its source at the pinned
  tag before stating it.
- At the end of each working session, say what was pushed, what
  Michel should pull, and on which host.

* * *

*Changelog*
- v0.4 — 2026-10-11 — begins from Michel's question: is a planned pathway saved in the database so it can be edited after? Answer as things stand (no: files only); the questions of saving, editing after, history and rights (§3); Gate A reads how Plai saves and edits entries today; Gate D walks save, reopen, edit and save again. Engine v0.13 on branch `stage-planner-route`; the first real run done.
- v0.3, amended 2026-10-11 — the editor and the planner integrated in the map service, inside the Pathways application, Michel's word.
- v0.3 — 2026-10-11 — the three steps and the pathway editor, Michel's word: Gate B designs the editor (spec v0.4 §3b), Gate D walks it.
- v0.2, amended 2026-10-11 — a start and an end: a host's name, a Plai or OSM place, coordinates or a point placed on the map.
- v0.2 — 2026-10-11 — SP-4 to SP-7, Michel's word: Gate A is
  Verkhovyna – Zhyva Khata – Tepla Gora – Kosiv as one corridor;
  a stretch's name and note in English first; the page's languages
  open. Spec v0.3.
- v0.1 — 2026-10-11 — initial, from Michel's word on SP-1, SP-2 and
  SP-3; engine `tools/stage_planner.py` v0.3; spec v0.2.
