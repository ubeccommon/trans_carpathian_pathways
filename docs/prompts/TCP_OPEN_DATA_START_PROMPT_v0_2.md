---
title: "TCP_OPEN_DATA_START_PROMPT_v0_2"
subtitle: "Starting prompt — developing and implementing the open-data specification"
author: "Michel Garand"
date: "October 2026"
version: "v0.2"
lang: "en"
license: "CC BY-SA 4.0"
project: "Trans-Carpathian Pathways"
status: "to paste as the first message of a new conversation"
---

*Paste everything below the line as the first message of a new
conversation in the Claude Project "Trans Carpathian Pathway". It
develops and builds `docs/specs/PATHWAYS_OPEN_DATA_SPEC` — how
pilgrims carry the pathway into the map apps they already use,
and how partners read the open layers by machine. It works in this
repository and, for named changes on Michel's word, in
`ubec_mapservice`. It never puts a host into a file, a feed, an API
or OpenStreetMap.*

* * *

## 0. What this conversation is for

The specification is written (v0.1, October 9, 2026) and nothing
of it is built. Its answer to Michel's question: the pathway and
the places nobody hosts travel openly — through OpenStreetMap, as
stage files in GPX, GeoJSON and KML, and through an OGC API –
Features service for partners; the hosts travel one at a time, by
a `geo:` link in the map's click, or in one pilgrim's journey file
from the Curator, and never in bulk.

This conversation takes it from paper to the ground, gate by gate,
in the specification's own order (§8): what can serve now, now;
what needs walked stages, after Gate 4; what needs a partner, when
one asks. Work to need is the rule — a capability is built when the
project needs it, not before — and where a gate would build ahead
of need, the conversation says so and Michel decides.

Not in scope: the host fields, the site's design, the stage
planner (Gate 5 of the project), anything a Curator holds off Plai.

## 1. Load order — before any work

1. Attach `ubeccommon/trans_carpathian_pathways` with **push**
   access and `ubeccommon/ubec_mapservice` with **read** access;
   push to `ubec_mapservice` only for a change Michel names at its
   gate, and only that change. Clone both.
2. Read, in this tree:
   - the latest `docs/TRANS_CARPATHIAN_PATHWAYS_CLAUDE_PROMPT` —
     §2 (the decisions, the modules, the open-data paragraph), §5
     (what a host carries), §6 (the planner and OI-P10), §7, §8, §9;
   - `docs/specs/PATHWAYS_OPEN_DATA_SPEC` at its latest version,
     **whole** — it is the work;
   - `docs/TRANS_CARPATHIAN_PATHWAYS_MODULES` at its latest version,
     §3 (the connectors and their standards) and §6;
   - the agreement, `docs/agreement/…_EN.md`, §5, §6, §7 and the
     contributor's part;
   - the stress tests,
     `docs/reviews/TRANS_CARPATHIAN_PATHWAYS_STRESS_TESTS_v0_1.md`,
     stress test two, scenario A, "The scraper" — what this work
     must not make easier;
   - `docs/specs/PLAI_HOST_FIELDS_SPEC_v0_5.md` and
     `docs/reviews/UBEC_MAPSERVICE_STATE_REVIEW_v0_1.md` — how a
     Plai change is specified, built and proven;
   - the user manual, `docs/manual/Plai_User_Manual_EN.md`, §6 —
     what the click shows today, which Gate B changes.
3. Read, in the mapservice tree, the latest
   `docs/UBEC_MAPSERVICE_CLAUDE_PROMPT` §1, §2 and §4, and in §3
   the entries on the Carpathian hub, Plai and its entry surface;
   `db/instances/plai/` (the migrations, `001` to `005` today) and
   `mapbender/instances/plai/`; the feature-info template that
   shapes the click; `verify` and `leak_pass.py`; `stack/nginx/`
   (the public face's thresholds, vhost v0.5); and how MapServer is
   built in `stack/` — whether it is version 8 with OGC API support.
4. Only then begin, with Gate A.

## 2. What is known already

**The data, in three kinds** (spec §2). A — the pathway: stage
lines drawn on OSM's paths, so ODbL. B — places nobody hosts
(viewpoints, springs, shelters), entered by the Curator or a
steward. C — hosts: a Plai point with at least one offer, very
often a home, consented field by field, not under an open licence
(A-2 as drafted). A and B travel openly; C never in bulk.

**The apps.** Organic Maps imports KML, KMZ, KMB, GPX and GeoJSON
files opened from mail, a messenger or cloud storage; its pages
mention no live layers. OsmAnd, Locus and Garmin devices read GPX.
Apps built on OSM carry what is in OSM at their next map update.

**The standards** (spec §3, §4). GPX 1.1 first; GeoJSON per RFC
7946 (WGS 84 only); KML 2.3 and KMZ; the `geo:` URI per RFC 5870;
OGC API – Features, Part 1: Core, with GeoJSON and an OpenAPI 3
description; ISO 19115 metadata in an INSPIRE-compatible profile
for each open series; SPDX licence identifiers (`ODbL-1.0`); the
attribution "© OpenStreetMap contributors"; BCP 47 language tags in
every file name and file.

**The stack, as recorded** (prompt v0.37 and the state review).
Plai is the Carpathian hub instance of UBEC Mapservice:
PostgreSQL/PostGIS, MapServer, Mapbender 5.0.0-RC2 with the
Digitizer. Plai's migrations run to `plai/005`; the entries scheme
is at v0.9; the agreement on Plai at `v0.3`. On the host, October
9: `verify plai vt` 96 of 96, the leak pass 519 of 519. The leak
pass expects exactly the layers it knows — any new advertised
layer or collection must be added to it. Mapbender keeps a WMS
source's capabilities from its first import: a new layer reaches
an application only after a reload, and the public user copy is a
snapshot made again after each change. MapServer serves OGC API –
Features from version 8 when built `WITH_OGCAPI`; whether Plai's
build has it is not yet known.

**What does not exist yet.** Any stage: stages exist once the
corridor is walked (Gate 4 of the project). Any host on Plai:
Gate 3 has not opened, and waits on backups with an off-host copy.
A decision on OI-P10, on marking (settled at Gate 4), or on any of
the spec's D-1 to D-6.

**Where things are.** This repository on Michel's computer:
`/home/farmer/projects/plai`, as `farmer` on schiff. The
mapservice checkout on the host: `/home/ubec/ubec_commons/ubec_mapservice`,
as `ubec` on ubec-common, reached from schiff with `ssh ubec-common`
(the alias `site/README.md`, "First deploy", step 0 sets up; the
address stays out of every tree).
Every command given to Michel uses these paths, never a
placeholder.

## 3. What binds every gate

- **No host in bulk, ever.** No public file, no API response, no
  OSM edit, no test fixture carries a host. A test proves it for
  every public file and every collection.
- **No tracking.** No keys, accounts, cookies or analytics on any
  file or service; logs as short as abuse control needs.
- **Nothing confidential** (S-15): no shelter for alerts, no stage
  state, no pilgrim's data in any file.
- **The border strip** (S-8): no stage inside it in a public file
  until the permit route is held in writing and done once.
- **Licence in the file.** Every file and collection carries its
  licence, attribution, version, date and language.
- **Proven before shown.** A Plai change passes `verify` and the
  leak pass, extended to cover it, locally and then on the host,
  before Michel's look.
- **Test data is invented.** Fixtures are made-up stages and
  places in an invented valley, never a real host, never a real
  home (the agreement's contributor part).

## 4. Gates

A gate opens on Michel's word. Claude proposes; Michel decides.

- **Gate A — decisions and facts.** Michel's word on D-1 to D-6
  (spec §9) and on how the export tool reads Plai (§5 below). Two
  facts gathered first, read-only: the MapServer version and
  whether it carries OGC API support (Michel runs `mapserv -v` in
  the MapServer container on the host, the exact command given
  from the tree), and the feature-info template the click uses.
  Output: the spec at its next version with the decisions and the
  facts.
- **Gate B — the `geo:` link (spec §3.4).** The one part that
  serves now, adding nothing in bulk. A mapservice change on
  Michel's word: the click on a published place carries
  `geo:<lat>,<lon>` for that place's published point, labelled in
  English as Plai's screens are; the leak pass asserts the link
  equals the published point and appears on published places only;
  `verify` extended. Proven locally, then on the host: render,
  `cache:clear`, the WMS source reloaded if needed, the user copy
  made again; Michel's look on a phone, the link opening in an
  app. Then the user manual's §6 checked against it and rebuilt in
  both languages.
- **Gate C — the tools (spec §3.2, §3.3, §4, §7).** In this
  repository, Python, in the mapservice tool style: an export tool
  that writes stage files (GPX 1.1, GeoJSON, KML 2.3; one per stage
  and language; licence, attribution, version, date, the "this
  file does not update" line, the permit note) and their ISO 19115
  records; the same tool writing a journey file, on the Curator's
  machine only, with the hosts of that journey; a validator — GPX
  and KML against their schemas, GeoJSON against RFC 7946, the
  no-host test, the licence and language check. Proven on invented
  fixtures. *This gate builds ahead of the walked stages;* the
  conversation says so, and Michel decides whether it runs before
  Gate 4 or after.
- **Gate D — the stages stored and published.** After the project's
  Gate 4, when stages exist. OI-P10 as decided at Gate A: a Plai
  migration storing stage lines in `instance_sa` under ODbL, built
  in mapservice on his word, with `verify` and the leak pass. The
  first real files written, validated, and served where D-6 says;
  if from the site, `build/build_site.py` copies and checks them
  (no host, licence present) and its README says so.
- **Gate E — the API (spec §3.5).** Only when a partner asks
  (D-4). Collections `stages` and `places`, no hosts; the vhost's
  thresholds; the leak pass extended to the API. If MapServer is
  not version 8 with OGC API support, the conversation records the
  gap and stops: an upgrade is Mapservice's decision, not this
  project's.
- **Gate F — OpenStreetMap (spec §3.1).** After Gate 4's marking
  decision (D-3). A short guide for mappers, English and Ukrainian:
  what goes in by survey (missing paths, springs, shelters,
  viewpoints, and the route relation if the pathway is marked),
  what never goes in (a host, a home, a tag that says a place
  hosts), and OSM's import guidelines. No import from Plai. The
  editing is done by mappers under OSM's rules.

Order: A, then B. C on Michel's word, before or after Gate 4. D
and F after Gate 4. E on a partner's need.

## 5. Open — for Michel, at Gate A

- **D-1 to D-6**, as the spec states them, with its proposals.
- **How the export tool reads Plai.** Options: a read-only database
  role on Plai's published view, a mapservice change, with its
  credential outside every tree; the OGC API of Gate E; or a
  GeoJSON dump Michel makes on the host at each release. The
  journey file reads the published fields of the journey's hosts
  only, and runs only on the Curator's own machine.
- **Who runs the export.** Michel, at each change, by one command;
  or a timer on the host. A timer on the host is a mapservice
  change.
- **What the `geo:` link is called** in the click: "Open in your map
  app" is proposed; Plai's screens are English and the manual
  glosses them in Ukrainian.

## 6. Working rules

- Pull before any edit, in both trees; the version you bump is the
  one you pulled. Michel pushes from his own clones too.
- In `ubec_mapservice`: only the change Michel names at its gate,
  under that tree's rules — its prompt and README bumped and the
  change recorded as his word with its date, every `.md` passing
  `check_ubec_standard.py`, 74-character lines, a changelog in
  every file; long host runs in tmux; the vhost reinstalled after
  any commit touching `stack/nginx/`; `cache:clear` after every
  `render`.
- In this tree: documents under the project's standard — front
  matter with `lang`, a changelog, English first, Ukrainian for
  what leaves the project; tools in `tools/`, code under AGPL-3.0;
  the starting prompt bumped when a gate closes, and the main
  prompt recording it.
- No secret in any tree; no real host's data in any test, fixture,
  issue or screenshot.
- Commits as Michel Garand <stewardship@ubec.network>, with the
  co-author line.
- Every command for Michel uses the real paths in §2.
- At the end of each working session: what was pushed in each
  tree, what Michel should pull and where, what he runs on the host
  and in what order, and which decision the next gate waits on.

* * *

*Changelog*
- v0.1 — 2026-10-09 — initial, on Michel's word: the open-data
  specification v0.1 to be developed and built, in six gates.
