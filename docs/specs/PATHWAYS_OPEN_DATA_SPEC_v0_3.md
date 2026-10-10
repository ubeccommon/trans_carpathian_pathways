---
title: "PATHWAYS_OPEN_DATA_SPEC_v0_3"
subtitle: "How pilgrims carry the pathway into their own map apps — files, links, OpenStreetMap and an API"
author: "Michel Garand"
date: "October 2026"
version: "v0.3"
lang: "en"
license: "CC BY-SA 4.0"
project: "Trans-Carpathian Pathways"
status: "specification for Michel's word — the geo: link built (plai/006, October 9, 2026); the rest not built; six decisions open (§9)"
---

*A specification for how the pathway and its places reach the map
apps pilgrims already use — Organic Maps, OsmAnd, Locus, a Garmin
— and how partners may read the open layers by machine. It belongs
to module T1 and its connector "T1 → others" in the module map
(`docs/TRANS_CARPATHIAN_PATHWAYS_MODULES_v0_3.md`). It is not the
build: what touches Plai is built in `ubec_mapservice`, in that
repository's own way and on Michel's word for each change, and
where this document and the mapservice prompt disagree about the
stack, the mapservice prompt is right. Michel's question, October
9, 2026: can pilgrims integrate Plai's places and the pathways
into their apps, and which standards apply? The short answer: the
pathway yes, openly; the hosts one at a time, never in bulk.*

* * *

## 1. What It Rests On

| Item | Decided | What it means here |
|------|---------|--------------------|
| No app for pilgrims | white paper §7, the lessons table | The project builds no app; it meets pilgrims in the apps they have |
| S-1 | Michel's word, Oct 9 | Host points are public and clickable during the pilot |
| S-14 | Michel's word, Oct 9 | Withdrawal removes a point from Plai, not from copies; hosts are told so |
| A-2 | as drafted, to confirm | Entries are not released under an open licence |
| OI-P7 | Michel's word, Oct 7 | A home is published at the point entered |
| OI-P10 | **open** | A route drawn from OSM is computed and unstored, or stored under ODbL in `instance_sa` |
| S-8 | Michel's word, Oct 9 | No stage in the border strip is suggested until the permit route is held and done once |
| S-15 | Michel's word, Oct 9 | Plai holds no confidential information |
| Agreement §5 | draft v0.6 | No tracking of what visitors do; no data handed on |
| Agreement, contributor part | draft v0.6 | Never a host's home, or a place marked as hosting, in OpenStreetMap without the host |
| Modules §3, §6 | Michel's word, Oct 9 | ISO 19115 metadata for a layer published for others; marking settled at Gate 4 |
| S-23 | built, Oct 9 | The public face has request thresholds and short logs (vhost v0.5) |

And the stress tests' scenario "The scraper" (stress test two, A):
what the public map shows can be collected by anyone. Nothing
here may make that easier.

## 2. Three Kinds of Data, Three Rules

| Kind | What | Licence | How it travels |
|------|------|---------|----------------|
| **A — the pathway** | Stage lines and the corridor's route, drawn on OSM's paths | ODbL 1.0, © OpenStreetMap contributors (a work derived from OSM) | Openly: OpenStreetMap (§3.1), stage files (§3.2), the API (§3.5) |
| **B — places nobody hosts** | A viewpoint, a spring, a mountain hut or hikers' shelter (never an air-raid shelter), a chapel, entered by the Curator or a steward | ODbL 1.0, by the entrant's choice *(proposal, §9 D-5)* | Openly: in OSM when the thing is physical and verifiable; in stage files; in the API |
| **C — hosts** | A Plai point with at least one offer: very often a home | Not open (A-2); the host's, consented field by field | One at a time (§3.4), or in one pilgrim's journey file from the Curator (§3.3). **Never** in bulk, never in OSM, never in the API |

A host's place is never a waypoint in a public file, whatever the
app, the partner or the purpose.

## 3. The Channels

### 3.1 OpenStreetMap — the strongest integration

Apps built on OpenStreetMap data, Organic Maps and OsmAnd among
them, carry what is in OSM to every pilgrim at their next map
update, with no file and nothing from the project on the phone.

- **What goes in:** the paths themselves where they are missing or
  wrong; physical places nobody hosts (springs, mountain huts and
  hikers' shelters — never an air-raid shelter — viewpoints) where a mapper has seen them; and, once Gate 4 has
  settled marking, the pathway as a hiking route relation
  (`type=route`, `route=hiking`).
- **What never goes in:** a host's place, a home, or any tag that
  says a place hosts (the agreement's contributor part).
- **How:** by mappers on the ground under OSM's own rules — survey,
  not import. OSM's import guidelines apply to anything added in
  bulk; the project imports nothing from Plai into OSM.
- **The condition:** OSM maps what can be verified on the ground.
  An unmarked, emergent pathway is a weak route relation; a marked
  one is a good one. The route goes in only on Gate 4's marking
  decision (§9 D-3).

### 3.2 Stage files — for any app, offline

One file per stage and per language, and one for the whole
corridor, served as static files with no tracking.

- **Formats:**
  - **GPX 1.1** — the first format, read by every app and device:
    the stage as a track (`trk`), places of kinds A and B as
    waypoints (`wpt`).
  - **GeoJSON** (RFC 7946) — for apps and partners that prefer it:
    WGS 84 coordinates only, no other CRS.
  - **KML 2.3** (OGC) and **KMZ** — for Google Earth and others.
  Organic Maps imports all three.
- **What each file carries:** the stage's name and description in
  its language; its version and date; the licence (`ODbL-1.0`) and
  the attribution "© OpenStreetMap contributors"; a line telling
  the pilgrim that the file does not update and that the stage's
  state is held by the Curator; where a stage lies in the border
  strip, that a permit is needed and how (S-8).
- **What no file carries:** a host; a shelter for air-raid alerts,
  or anything else the Curator holds (S-15); a pilgrim's data.
- **Names:** `tcp_<corridor>_<stage>_<lang>_v<version>.<ext>`, the
  language a BCP 47 tag (`en`, `uk`), as every file in the project.
- **Withdrawal:** a stage or a place withdrawn is gone from the
  next version, which is published at once; the old files say on
  their face where the current version is.

### 3.3 The journey file — one pilgrim, from the Curator

For a pilgrim who asks the Curator for a journey, the Curator may
send one GPX file for that journey: its stages, and the hosts on it
as waypoints, with only the fields the public map already shows for
them (S-1). *(Open, for Michel's word: whether the waypoints carry
names, or are numbered and unnamed with names and contacts sent
separately, since a pilgrim's phone may be searched at a
checkpoint.)* The file says, in its description, that it was made for
this journey and that withdrawal cannot reach it once sent. It is
made by a tool, never by hand-copying a list, and nothing about it
is kept beyond the incident record's rules.

### 3.4 One place at a time — "open in your map app"

The click on a published place on Plai's public map carries a link
in the `geo:` URI scheme (RFC 5870) — `geo:<lat>,<lon>` — which
phones open in whatever map app the pilgrim uses. One place, one
tap, nothing collected. This is the one change that serves hosts
now, without bulk. **Built** October 9, 2026 as `plai/006` in
`ubec_mapservice`: "Open in your map app", a `geo:` link with
Android's `q=` to seven decimals, proven by `verify` and the leak
pass. On iPhones a `geo:` link opens only an app that claims the
scheme.

### 3.5 The API — for partners, not pilgrims

- **Standard:** OGC API – Features, Part 1: Core, with the GeoJSON
  encoding and an OpenAPI 3 description, coordinates in CRS84. It
  is the successor to WFS, readable by QGIS, by scripts and by a
  partner's own site.
- **Collections:** `stages` (kind A) and `places` (kind B). **No
  collection for hosts.**
- **Where:** Plai's MapServer, which serves OGC API – Features from
  version 8 when built with `WITH_OGCAPI` (`mapserv -v` shows
  `SUPPORTS=OGCAPI_SERVER`). Plai's MapServer is 8.6.5, built with
  OGC API support (October 9, 2026); enabling it is configuration
  only. A framework change, Mapservice's to decide.
- **Rules:** no keys and no accounts; no cookies; the vhost's
  thresholds and short logs; paging limits; the leak pass extended
  to the API so it advertises only the open collections.
- **When:** when a partner asks for it — work to need. Until then,
  the files serve.

## 4. Metadata and Licence, In Every File

- **ISO 19115** metadata, in an INSPIRE-compatible profile, for each
  open series — the stage files and the API's collections — as
  decided for a layer published for others (modules §6).
- **Licence identifiers** as SPDX: `ODbL-1.0` for kinds A and B;
  the documents that describe them, `CC-BY-SA-4.0`.
- **Attribution** "© OpenStreetMap contributors" wherever OSM-derived
  geometry appears, as ODbL requires.
- **Version and date** on every file and every collection; a short
  record of changes beside the files.

## 5. Privacy and Safety

- No tracking, no analytics, no accounts, no keys, no cookies — for
  files and API alike (agreement §5).
- Logs as short as abuse control needs, under the vhost's
  thresholds (S-23).
- Nothing confidential in any file or response (S-15).
- No stage inside the border strip in any public file until S-8's
  condition is met.
- Hosts never in bulk (§2). A request to add them — from a partner,
  a funder, an app — is declined and listed with the declined
  requests if S-19's list includes them.

## 6. What Each Part Asks, and of Whom

| Part | Where it is built | Needs first |
|------|-------------------|-------------|
| `geo:` link in the click (§3.4) | `ubec_mapservice`, `plai/006`; leak pass | Done, October 9, 2026 |
| Stage lines stored (§2 A) | `ubec_mapservice`, a Plai migration into `instance_sa` | OI-P10 decided (§9 D-1); stages walked (Gate 4) |
| Stage and journey files (§3.2, §3.3) | This repository, `tools/export_stages.py` *(proposal)*, reading Plai's published view | Stage lines stored; D-2, D-6 |
| OSM (§3.1) | Mappers, under OSM's rules (long list C-3) | Gate 4's marking decision (D-3) |
| API (§3.5) | `ubec_mapservice`, MapServer 8.6.5, OGC API built in | A partner's need (D-4) |
| Metadata (§4) | Beside each open series | The series existing |

## 7. Proofs

- Every GPX file valid against the GPX 1.1 schema; every GeoJSON file
  against RFC 7946 (WGS 84, right-hand polygons); every KML file
  against KML 2.3.
- A test that **no public file and no API response contains a
  host**: every waypoint and feature checked against Plai's hosts.
- A test that a withdrawn stage or place is gone from the next
  version and from the API at once.
- The leak pass extended to the `geo:` link and to the API.
- Every file carries its licence, attribution, version, date and
  language.

## 8. Order of Work

1. **Done:** the `geo:` link (§3.4), `plai/006`, October 9, 2026.
2. **After Gate 4:** the stages exist only once walked. Then OI-P10,
   the stage lines stored, and the stage files.
3. **With Gate 4's marking decision:** the route in OSM, or not.
4. **When a partner asks:** the API.

## 9. Open — for Michel

- **D-1 — OI-P10.** A downloadable stage is a stored route. *Proposal:*
  store stage lines in `instance_sa`, published under ODbL, which
  closes the "computed and never stored" option.
- **D-2 — Hosts in files.** *Proposal:* one at a time (§3.4) and in a
  journey file from the Curator (§3.3) only. The alternative is a
  separate consent tick, "may appear in downloadable files", a Plai
  migration — not proposed.
- **D-3 — The route in OpenStreetMap.** Settled with marking at
  Gate 4.
- **D-4 — The API on Plai.** *Proposal:* when a partner asks, after
  the MapServer version is checked.
- **D-5 — Places nobody hosts.** *Proposal:* the Curator or steward
  who enters them releases them under ODbL, so they can travel
  openly with the route; a host's place stays under A-2.
- **D-6 — Where the files are served.** *Proposal:* from the site,
  `tcp.ubec.network`, as static downloads — not a map, not a list
  of hosts, so within the site's rules — or from Plai.

## Sources

Read October 9, 2026.

1. Organic Maps, "How to import bookmarks and tracks" (KML, KMZ, KMB,
   GPX, GeoJSON) — https://organicmaps.app/faq/bookmarks/how-to-import/
2. MapServer, "OGC API: Features" (MapServer 8, `WITH_OGCAPI`) —
   https://mapserver.org/ogc/ogc_api.html
3. RFC 5870, "A Uniform Resource Identifier for Geographic Locations
   ('geo' URI)" — https://www.rfc-editor.org/rfc/rfc5870
4. RFC 7946, "The GeoJSON Format" — https://www.rfc-editor.org/rfc/rfc7946
5. GPX 1.1 schema — https://www.topografix.com/GPX/1/1/
6. OGC KML 2.3 — https://www.ogc.org/standards/kml/
7. OGC API – Features, Part 1: Core — https://www.ogc.org/standards/ogcapi-features/
8. Open Database License 1.0 — https://opendatacommons.org/licenses/odbl/1-0/
9. OpenStreetMap, import guidelines — https://wiki.openstreetmap.org/wiki/Import/Guidelines

* * *

*Changelog*
- v0.3 — 2026-10-10 — the public-drafts stress tests
  (docs/reviews/PUBLIC_DRAFTS_STRESS_TESTS_v0_1.md): the `geo:` link
  recorded as built and the MapServer version as known; no air-raid
  shelter among the open places; the scraper line worded so as not
  to point the way; the journey file's named waypoints put to
  Michel.
- v0.2 — 2026-10-10 — the Pilgrim of the Plai.
- v0.1 — 2026-10-09 — initial, on Michel's question: three kinds of
  data and three rules; OpenStreetMap, stage files, the journey
  file, the `geo:` link and the API, with their standards; metadata
  and licence in every file; privacy and safety; who builds what;
  proofs; the order of work; six decisions open.
