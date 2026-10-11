---
title: "PATHWAYS_STAGE_PLANNER_SPEC_v0_2"
subtitle: "The planner anyone may use, the stretches a Curator saves, and the corridors made of them"
author: "Michel Garand"
date: "October 2026"
version: "v0.2"
lang: "en"
license: "CC BY-SA 4.0"
project: "Trans-Carpathian Pathways"
status: "specification — SP-1, SP-2 and SP-3 decided (Michel's word, October 11, 2026); the engine built and tested on a made-up valley (tools/stage_planner.py v0.3); not yet run on Plai's data; the page, the service and saving on Plai not built — they come before Gate 3; four items open (§9)"
---

*A specification for the stage planner — the proposal's "spatial
algorithm" — after Michel's word of October 11, 2026. It belongs
to module T1 in the module map. The engine lives in this
repository's `tools/`; what touches Plai — the tables a saved
stretch lives in, the page anyone plans from — is built in
`ubec_mapservice`, in that repository's own way and on Michel's
word for each change, and where this document and the mapservice
prompt disagree about the stack, the mapservice prompt is right.*

* * *

## 1. The Decision

*Michel's word, October 11, 2026:* pilgrims, stewards and
Curators can use the planner directly. It is public, so anybody
can use it. The Curator can create a route, save it and manage
it. These individual stretches can be combined to create a
corridor.

What it replaces: the starting prompt §6 said the planner was the
Curator's alone and never answered a pilgrim directly, and was to
be built only once the corridor had hosts enough to need it. The
reasoning's principle "The Curator as memory" ruled out an
algorithm answering a pilgrim.

What stays: a tool proposes, a person decides. Anyone may ask the
planner for a way; only a Curator makes a way the project's, by
saving it, and only a Curator joins stretches into a corridor.
Nothing the planner says is a booking, a promise that a host will
receive, or a statement that a stretch is safe today.

What it settles: OI-P10. A route the planner answers with is
computed and gone; a stretch the Curator saves is stored, in
Plai's `instance_sa`, under ODbL 1.0, as a work derived from
OpenStreetMap — class A of the open data spec, which travels
openly.

## 2. Who Does What

| Who | Plans | Downloads the answer | Saves a stretch | Joins stretches into a corridor | Publishes or withdraws |
|---|---|---|---|---|---|
| Anyone, the pilgrim included | yes | yes, hosts by name and detour time only (§5) | no | no | no |
| Pathway steward | yes | yes, hosts by name and detour time only | a draft (SP-1) | no | no |
| Curator | yes, and may list hosts in full | yes | yes | yes | yes — their own stretches and the drafts stewards save |

The Curator works from their Plai account, in `PLAI_CURATOR`; a
steward saves drafts from theirs, in `PLAI_STEWARD`; nobody else
needs an account to plan (minimal accounts). *SP-1, Michel's word,
October 11, 2026:* the steward may save a draft, and only the
Curator publishes it.

## 3. What the Planner Does

Built as `tools/stage_planner.py` v0.3; its opening comment holds
every rule and number. In short:

- **In:** a start and an end — a published Plai place, a village
  in OSM, or a point as `lat,lon`; the party (solo, couple, group,
  family); the month; how far off the route to look (5 to 10
  minutes).
- **Network:** OpenStreetMap's paths, tracks and roads from
  `reference_sa.osm_line`, read across, never joined.
- **Time:** DIN 33466 from GEDTM30 ground heights, per direction;
  the party scales it.
- **Criteria:** off the beaten path (village roads cost a little,
  main roads much, trunk roads are not walked); a marked trail and
  passing near a place preferred a little; the party's SAC grade
  and trail visibility; never inside the five-kilometre border
  strip (S-8); never an air-raid shelter listed.
- **Out:** the route; up to two alternatives; the quickest way
  beside them, so what the criteria cost in time is seen; a band
  of 2.5, 5, 7.5 and 10 minutes' reach on both sides, densest at
  the route and fading outwards, its outer edge the boundary; the
  places within reach in the order the route meets them, each with
  its one-way detour. GeoJSON, and a map preview.
- **Stores:** nothing.

The band is reach, walked: it is narrow where the side paths climb
and wide where they are easy. It is fuzzy by design and speaks for
the walk, never for land (S-14: fuzzy bands, never parcels).

## 4. A Stretch

A route the Curator saves. Proposed for Plai, as one migration in
`ubec_mapservice` (`plai/008`), table `instance_sa.stretch`:

| Column | What |
|---|---|
| `id`, `name` | the Curator's name for it, in BCP 47-tagged languages as Plai's other text |
| `geom` | the route line, EPSG:3035, ODbL |
| `band` | the four rings, kept so the map draws them without the planner; ODbL |
| `from_label`, `to_label`, `start_geom`, `end_geom` | as entered |
| `criteria` | the party, the numbers and the planner's version it was made with (jsonb), so it can be remade the same way |
| `km`, `minutes`, `up_m`, `down_m` | as the planner reported |
| `state` | Plai's publication vocabulary: a stretch saved by a steward or a Curator is a draft, public only once a Curator publishes it, and it leaves every service on withdrawal |
| `saved_by` | the account that saved it, a steward's or a Curator's |
| `curator` | the Curator who published it |
| `steward` | who cares for it, if anyone |
| `note` | the Curator's own words, e.g. the state of a ford — public only if the Curator chooses |

**Never stored with a stretch: its list of places.** The list is
asked for again each time it is shown, from what is published that
day. A host who withdraws leaves every stretch at once; a stored
list would keep them.

The engine already writes what a stretch carries (`route` v0.3:
the `stretch` block of its output). Saving is Plai's: a steward or
the Curator saves from the planner's page while logged in (§6);
the Curator publishes from the same page or the backend.

## 5. Hosts in What the Planner Says

*SP-3, Michel's word, October 11, 2026:* the public answer names
published hosts with only their detour time.

- **The public answer** (`--audience public`, the default) names
  each published host within reach by the name they published and
  their one-way detour in minutes, in the order the route meets
  them — and nothing else: no place, no offer, no kind, no
  kilometre along the route, no geometry (in the file, a feature
  with a null geometry, RFC 7946 §3.2). So a host is never a
  waypoint in a public file (open data spec §2), while a pilgrim
  learns that someone receives near the way. The host's place
  stays where it already is: on Plai's map, public and clickable
  (S-1), one at a time.
- **The Curator's answer** (`--audience curator`) lists hosts in
  full — place, offers, whether open in the month — for the
  Curator's own planning and for one pilgrim's journey file (open
  data spec §3.3).
- A host who withdraws leaves every answer at once: the list is
  never stored (§4).

## 6. Where It Runs

The engine runs today on ubec-common in Mapservice's environment,
by hand (`tools/README.md`). *SP-2, Michel's word, October 11,
2026:* the public page and service run on Plai, and they come
before the first hosts (Gate 3). They are Mapservice's change,
built in `ubec_mapservice` in its own way, from the start prompt
`docs/prompts/PLAI_STAGE_PLANNER_START_PROMPT_v0_1.md`. As
specified:

- **A small service** on ubec-common behind the system nginx,
  calling the engine, reading `reference_sa` with the render
  role's rights and Plai's published view, writing nothing but a
  Curator's save; the abuse-control thresholds of the vhost; no
  per-viewer log beyond what abuse control needs (logs short).
- **A page** in Plai's Pathways application (`ubec_plai_hub_tcp`):
  two points on the map or two names, the party and the month; the
  band, the route, the list beside it; a download. Logged in, a
  steward or a Curator also saves; a Curator publishes. Ukrainian
  and English first (BCP 47), WCAG 2.2 AA.
- **With few hosts or none:** before Gate 3 the list holds open
  places only — viewpoints, springs, huts, chapels — and the page
  says that hosts appear as they join.
- **Before it faces anyone:** Mapservice's leak pass over every
  endpoint and answer — exposure is a decision.

Not proposed: pgRouting in the database image. It would be a
framework change for one project's need, and the engine is fast
enough for a corridor's paths.

## 7. A Corridor

An ordered set of stretches with a name, made and managed by a
Curator. Proposed for Plai, in the same migration:
`instance_sa.corridor` (id, name, state, curator, note) and
`instance_sa.corridor_stretch` (corridor, stretch, position).

- **Drawn from its stretches only:** the union of their bands,
  ring by ring, with one boundary; nothing is drawn that a stretch
  did not draw (`corridor` in the engine does this today from saved
  files). A stretch withdrawn leaves every corridor it was in.
- **Shown with its gaps:** where one stretch does not end where the
  next begins, the corridor says so, rather than joining them with
  a line nobody walked.
- **It speaks for its stretches and their places, never for a
  place** (reasoning §4: a corridor is not drawn by the project; it
  emerges from the places people chose to share).
- **Before a public body:** S-14 holds unchanged — a host's place
  in any submission only with that host's separate, revocable
  consent; never presented with a count of consents against
  residents; and whether each hromada council crossed is shown the
  corridor first is still open.

## 8. Rules That Still Bind

- **The border strip (S-8).** The public planner never routes or
  lists inside it. The Curator's flag `--allow-border-strip` exists
  for a Curator who holds the permit route in writing and has done
  it once; a stretch saved with it says so in its criteria, and is
  never public until S-8's condition is written into the stage
  register.
- **Safety is the Curator's to hold (S-15).** The planner says
  nothing about the state of a path today. Its times are estimates
  for the party chosen, and its page says so.
- **The pilgrim informs themselves (OI-P12).** The page links to
  the agreement's pilgrim part.
- **No calendar, no booking.** The month narrows hosts by season
  only; availability stays a conversation with the Curator.
- **Organic growth.** A Curator saves stretches that join places
  people chose to share; the planner is not used to draw a route
  first and recruit hosts to fill it.

## 9. Open — for Michel

- **SP-1** — *Decided, Michel's word, October 11, 2026:* a steward
  may save a draft; only the Curator publishes it. §2, §4.
- **SP-2** — *Decided, Michel's word, October 11, 2026:* the public
  page and service run on Plai, and come before the first hosts
  (Gate 3). §6.
- **SP-3** — *Decided, Michel's word, October 11, 2026:* the public
  answer names published hosts with only their detour time. §5.
- **SP-4** — The numbers: the road penalties, the party paces and
  SAC limits, the reach rings. Proposed: as in the engine, until
  the first real run and a walk with a GNSS track (Gate 4) test
  them.
- **SP-5** — The first real run: Zhyva Khata to Tepla Gora, on
  ubec-common, for Michel's look at the route, the band and the
  list.
- **SP-6** — The changes to the public documents (§10): now, or at
  each document's next version.
- **SP-7** — A stretch's name and note: Ukrainian and English both
  required, or either.

## 10. Documents That Still Say Otherwise

Changed with this specification: the starting prompt v0.61 (§6,
§7, OI-P10) and v0.62 (SP-1 to SP-3, Gate order), the decisions
checklist v0.5 and v0.6, the reasoning v0.4.

Still saying the planner is the Curator's alone, or may never be
built, until their next version (SP-6):

- the white paper, English and Ukrainian (§ "No algorithm
  deciding"; the gates), and its PDF;
- the proposal, English and Ukrainian (the stage planner "a tool
  for the Curator"; "if needed"), and its PDF;
- the implementation plan, English and Ukrainian ("decide whether
  the stage planner is needed at all"), and its PDF;
- the module map (T1: "a stage planner only if Gate 4 shows
  need");
- the project overview and its deck, if they name it.

## Changelog

- v0.2 — 2026-10-11 — SP-1, SP-2 and SP-3 decided on Michel's word:
  a steward saves drafts, the Curator publishes; the page and
  service on Plai before Gate 3, from their start prompt; the public
  answer names hosts with their detour time only. The engine at
  v0.3.
- v0.1 — 2026-10-11 — initial, from Michel's word of the same day:
  public, the Curator saves and manages stretches, stretches make a
  corridor; OI-P10 settled by it; the engine at v0.2.
