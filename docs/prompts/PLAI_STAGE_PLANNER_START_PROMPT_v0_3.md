---
title: "PLAI_STAGE_PLANNER_START_PROMPT_v0_3"
subtitle: "Starting prompt — the stage planner's page, service and saved stretches on Plai"
author: "Michel Garand"
date: "October 2026"
version: "v0.3"
lang: "en"
license: "CC BY-SA 4.0"
project: "Trans-Carpathian Pathways"
status: "to paste as the first message of a new conversation"
---

*Paste everything below the line as the first message of a new
conversation in the Claude Project "Trans Carpathian Pathway".
It builds, in `ubec_mapservice`, what makes the stage planner
public on Plai: a service, a page, and the tables a saved stretch
and a corridor live in. Michel's word, October 11, 2026 (SP-2):
the page and service run on Plai and come before the first hosts
(Gate 3).*

* * *

## 0. What this conversation is for

The stage planner is public: anybody plans with it; a steward may
save a draft; only a Curator publishes a stretch, and joins
stretches into a corridor. Its engine exists and is tested on a
made-up valley — `tools/stage_planner.py` v0.4 in the Pathways
tree — but runs today only by hand on ubec-common. This
conversation gives it a page and a service on Plai, and gives a
saved stretch somewhere to live.

Not in scope: changing what the engine decides (its numbers are as proposed, on Michel's word,
SP-4; a change is his or the Curator's, in the Pathways
conversation); the
multi-day `stages` piece; the white paper, proposal or plan
(revised only when Michel says so, SP-6).

## 1. Load order — before any work

1. Attach `ubeccommon/ubec_mapservice` with **push** access and
   `ubeccommon/trans_carpathian_pathways` with **read** access.
   Clone both. This conversation writes `ubec_mapservice`, on
   Michel's word of October 11, 2026 for this named change.
2. Read the latest `docs/UBEC_MAPSERVICE_CLAUDE_PROMPT` in the
   mapservice tree: §1, §2, §4, §5, §9, and in §3 the entries on
   the Carpathian hub and Plai, Plai's entry surface and the map
   search. Its rules bind this work: one instance, one database;
   no secrets; reproducible from the tree; licence classes held by
   the database (segregate in `instance_sa`); exposure is a
   decision — the leak pass over every new endpoint before it
   faces anyone; logs short; the checker before any `.md`; commits
   authored as Michel Garand from a pulled tree.
3. In the Pathways tree, read in full:
   `docs/specs/PATHWAYS_STAGE_PLANNER_SPEC_v0_4.md` (what to
   build), `tools/stage_planner.py` and `tools/README.md` (the
   engine), and `docs/specs/PATHWAYS_OPEN_DATA_SPEC_v0_3.md` §2 (a
   host is never a waypoint in a public file).
4. In the mapservice tree, read the precedent this follows:
   `stack/search/` (`app.py`, `Dockerfile`) and the migrations that
   gave it its role (015, 016); `stack/docker-compose.yml`;
   `stack/nginx/mapservice.ubec.network`; `db/instances/plai/`
   (the entry, the host fields, the published view `entry_public`,
   the publication states); `tools/terrain.py` (where
   `ground.tif` lives and how it is mounted);
   `mapbender/exports/ubec_plai_hub_tcp.yaml` (the Pathways
   application).
5. Only then begin, with Gate A.

## 2. What is known already

- **The engine.** Python; networkx in memory; reads
  `reference_sa.osm_line` and `osm_point` and `reference.admin_unit`
  in the framework database, `instance.entry_public` in Plai's,
  and `terrain/ground.tif`; writes nothing but its answer.
  `route` and `corridor`; `--audience public` names published
  hosts with only their detour time (SP-3), `--audience curator`
  lists them in full. Not yet run on Plai's data.
- **The precedent.** The map search is a small Starlette service
  in its own image, on the compose network only, through a role
  that may read nothing but its table, with a two-second limit on
  every statement. The planner service is the same shape with more
  to read and more time to think.
- **Saving.** Spec §4 and §7: `instance_sa.stretch`,
  `instance_sa.corridor`, `instance_sa.corridor_stretch`, as Plai
  migration `plai/008`; a stretch saved by a steward
  (`PLAI_STEWARD`) or a Curator (`PLAI_CURATOR`) is a draft until
  a Curator publishes it; the list of places is never stored.
- **A start and an end** (Michel's word, October 11, 2026): a
  host's name, a place published on Plai, a named place in OSM, or
  otherwise coordinates typed as `lat,lon` or a point placed on the
  map. The page offers all of them; the engine already takes the
  first four, and a point placed on the map reaches it as
  `lat,lon`.
- **Before Gate 3** there are few hosts or none: the page must be
  worth opening with open places only, and say that hosts appear
  as they join.

## 3. Gates

Gate by gate; a gate opens on Michel's word. Claude proposes,
Michel decides, and nothing of Claude's is recorded as decided.

- **Gate A — the first real run.** On ubec-common, by hand, as
  `tools/README.md` says (SP-5): three stretches, Verkhovyna to Zhyva Khata, Zhyva Khata to Tepla Gora, Tepla Gora to Kosiv, then
  `corridor` over the three. Michel looks at the routes, the bands
  and the lists, and says what is wrong with them. A name the
  engine cannot find — Zhyva Khata if it is not yet a published
  place — is given as `lat,lon`. Timings recorded: how long the network takes
  to build for a corridor-sized box. Nothing is built before this.
- **Gate B — the design, as a list.** For Michel's word, each item
  with the lever it uses in the tree:
  - the service: its image, its role and exactly what that role
    may read and write, its time limits, how the browser reaches
    it (an nginx location, or through Mapbender) and its abuse
    thresholds;
  - how the engine reaches the service: copied into the image from
    a pinned Pathways commit, or vendored — one home for the code;
  - `plai/008`: the three tables, their guards and grants, and how
    a save reaches them with the saver's Mapbender identity and
    group;
  - the page: inside the Pathways application or beside it; what
    a visitor sees, in the languages decided (§4), WCAG 2.2 AA;
  - the pathway editor for stewards and Curators (spec §3b): via
    and avoid points on the map, a line of one's own, a GPX upload,
    the gap and road checks, notes, save and publish, history — and
    what of it reaches the engine as `--via`, `--avoid`, `--known`;
  - how stretches and corridors are drawn on Plai's map for
    everyone once published, and how withdrawal removes them.
- **Gate C — built in the tree.** The service, the migration, the
  page and the map layers as files in `ubec_mapservice`; tests;
  README and prompt bumped; checker PASS; one commit as Michel
  Garand. The Pathways tree is not written from this conversation;
  what Pathways must record is handed back as a short note.
- **Gate D — on the host.** Michel pulls, migrates, builds,
  restarts, reloads nginx if its file changed, and runs the leak
  pass over every new endpoint and answer: in the public answer no
  host has a place, an offer, a kind, a kilometre or a geometry.
  Then he plans a route on the page, edits it as a steward — a via
  point through Verkhovyna, an avoid point, a line of his own, a
  GPX track — saves the draft, publishes it as the Curator, plans
  again near it and sees the published stretch preferred, withdraws a test host and sees it
  leave every answer. Closes on his "looks good" — and with it,
  Pathways Gate 5.

## 4. Open — for Michel, when they arise

- The page's address and name.
- The page's languages: English first, as SP-7 decided for a
  stretch's name and note until a multilingual Mapservice is
  explored, or English and Ukrainian from the start.
- Whether a visitor may download the answer as GPX as well as
  GeoJSON (the open data spec's stage files).
- How long the service may think before it says no, and how many
  answers one visitor may ask for in an hour.

## 5. Working rules

- Python for any tool and the service; no secrets; everything in
  the tree and mounted, nothing only on the server.
- In every pull or host command, the real checkout paths: on
  ubec-common `/home/ubec/ubec_commons/ubec_mapservice` as `ubec`;
  on schiff `/home/farmer/projects/plai` as `farmer`; `ssh
  ubec-common` from schiff.
- Verify every Mapbender claim against its source at the pinned
  tag before stating it.
- At the end of each working session: what was pushed, what
  Michel should pull, and on which host.

* * *

*Changelog*
- v0.3 — 2026-10-11 — the three steps and the pathway editor, Michel's word: Gate B designs the editor (spec v0.4 §3b), Gate D walks it.
- v0.2, amended 2026-10-11 — a start and an end: a host's name, a Plai or OSM place, coordinates or a point placed on the map.
- v0.2 — 2026-10-11 — SP-4 to SP-7, Michel's word: Gate A is
  Verkhovyna – Zhyva Khata – Tepla Gora – Kosiv as one corridor;
  a stretch's name and note in English first; the page's languages
  open. Spec v0.3.
- v0.1 — 2026-10-11 — initial, from Michel's word on SP-1, SP-2 and
  SP-3; engine `tools/stage_planner.py` v0.3; spec v0.2.
