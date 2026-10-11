---
title: "PATHWAYS_STAGE_PLANNER_SPEC_v0_3"
subtitle: "The planner anyone may use, the stretches a Curator saves, and the corridors made of them"
author: "Michel Garand"
date: "October 2026"
version: "v0.3"
lang: "en"
license: "CC BY-SA 4.0"
project: "Trans-Carpathian Pathways"
status: "specification — all seven items decided (Michel's word, October 11, 2026); the engine built and tested on a made-up valley (tools/stage_planner.py v0.4); the first real run, Verkhovyna to Kosiv, next; the page, the service and saving on Plai not built — they come before Gate 3"
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

Built as `tools/stage_planner.py` v0.4; its opening comment holds
every rule and number. In short:

- **In:** a start and an end, each as the user enters it —
  *Michel's word, October 11, 2026:* a host's name, a place
  published on Plai, a named place in OpenStreetMap (a village, a
  peak), or otherwise coordinates as `lat,lon` or a point placed on
  the map; the party (solo, couple, group, family); the month; how
  far off the route to look (5 to 10 minutes). A route asked for to
  or from a host ends at the host's published point: the host
  placed it (OI-P7), and it is one host the user chose, as Plai's
  "Open in your map app" link serves one place at a time — the list
  along the way still names other hosts with their detour time
  only (§5).
- **Network:** OpenStreetMap's paths, tracks and roads from
  `reference_sa.osm_line`, read across, never joined.
- **Time:** DIN 33466 from GEDTM30 ground heights, per direction;
  the party scales it.
- **The measure — the pathway is the way.** *Michel's word,
  October 11, 2026, after the first corridor:* "It's not a question
  of saving time or taking the shortest path ... the pathway is the
  way." So the planner seeks, in order: roads only as the last
  resort — *his word again the same afternoon:* "we are not looking
  for the shortest or fastest way to destination. Roads are only the
  last resort." A stretch of road between paths longer than 300 m is
  walked only where nothing else joins; a shorter one — a village
  crossing, a few hundred metres along a river — links two paths and
  is part of the way, and every road stretch a route walks is named,
  link or last resort (the 300 m is Claude's proposal; 0 allows no
  link at all); then, on paths, the richest way within an allowance (half
  again the most direct way on paths, proposed): footpaths first —
  *Michel's word the same day:* the dotted brown line on Plai's map
  (a path or footway) has priority over the red line (a marked
  hiking route) — then marked trails, the old plai over open high
  ground, forest away from settlements,
  meadows, and the places passed — springs, chapels and crosses,
  viewpoints, waterfalls, hosts, farmsteads, and whatever stewards
  find when they walk the path and enter on Plai. Forest and open
  land come from the canopy height (surface minus ground) beside the
  ground model. Time is reported, as a limit, never as the measure;
  the "quickest way" is no longer shown. The weights are Claude's
  proposal until Michel has looked at a corridor drawn with them
  (engine v0.6).
- **Obvious connections.** *Michel's word, October 11, 2026:* OSM
  paths often stop short of the way they meet. A path end is joined
  within 10 m to the nearest way, and up to 80 m where the
  connection is obvious: the path, carried on the way it was
  heading, meets the other way, and the gap crosses no river or
  stream. Every gap a route walks is listed and marked on the map,
  for a steward to check on the ground and for OSM to be mended.
- **Criteria besides:** trunk roads are not walked; a marked trail
  is a path, unless it runs on a main road; a marked trail and
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
| `id`, `name` | its name, in English first (SP-7), tagged `en` (BCP 47) so other languages can join it later |
| `geom` | the route line, EPSG:3035, ODbL |
| `band` | the four rings, kept so the map draws them without the planner; ODbL |
| `from_label`, `to_label`, `start_geom`, `end_geom` | as entered |
| `criteria` | the party, the numbers and the planner's version it was made with (jsonb), so it can be remade the same way |
| `km`, `minutes`, `up_m`, `down_m` | as the planner reported |
| `state` | Plai's publication vocabulary: a stretch saved by a steward or a Curator is a draft, public only once a Curator publishes it, and it leaves every service on withdrawal |
| `saved_by` | the account that saved it, a steward's or a Curator's |
| `curator` | the Curator who published it |
| `steward` | who cares for it, if anyone |
| `note` | the saver's own words, e.g. the state of a ford, in English first (SP-7) — public only if the Curator chooses |

**Never stored with a stretch: its list of places.** The list is
asked for again each time it is shown, from what is published that
day. A host who withdraws leaves every stretch at once; a stored
list would keep them.

The engine already writes what a stretch carries (`route` v0.3 and later:
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
`docs/prompts/PLAI_STAGE_PLANNER_START_PROMPT_v0_2.md`. As
specified:

- **A small service** on ubec-common behind the system nginx,
  calling the engine, reading `reference_sa` with the render
  role's rights and Plai's published view, writing nothing but a
  Curator's save; the abuse-control thresholds of the vhost; no
  per-viewer log beyond what abuse control needs (logs short).
- **A page** in Plai's Pathways application (`ubec_plai_hub_tcp`):
  a start and an end — typed as a name or coordinates, or placed
  on the map — the party and the month; the
  band, the route, the list beside it; a download. Logged in, a
  steward or a Curator also saves; a Curator publishes. Its
  languages: open for the build (start prompt §4) — English first,
  as SP-7 decided for a stretch's name and note, or English and
  Ukrainian from the start. WCAG 2.2 AA.
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
- **SP-4** — *Michel's word, October 11, 2026: the numbers as proposed —
  the road penalties, the party paces and SAC limits, the reach
  rings, as the engine holds them. The first real run and the walk
  with a GNSS track (Gate 4) test them; a change is Michel's or the
  Curator's word. *Changed after the first run, Michel's word the
  same day:* hiking paths first, roads for vehicles only when there
  is no other way — roads now count four to fifteen times their
  walking time instead of 1.3 to 4 (engine v0.5).
- **SP-5** — *Michel's word, October 11, 2026: the first real run is
  Verkhovyna – Zhyva Khata – Tepla Gora – Kosiv: three stretches,
  Verkhovyna to Zhyva Khata, Zhyva Khata to Tepla Gora, Tepla Gora to Kosiv, joined as one corridor, on ubec-common, for Michel's look
  at the routes, the bands and the lists. It is Gate A of the start
  prompt for the build on Plai.
- **SP-6** — *Michel's word, October 11, 2026: the public documents (§10)
  are revised when Michel says so, not before.
- **SP-7** — *Michel's word, October 11, 2026: a stretch's name and note
  are in English first, until the possibilities of a multilingual
  Mapservice are explored. Then this is decided again.

**Later, not open now:** exploring a multilingual Mapservice —
what Plai's entries, stretches and pages would need to carry
Ukrainian and other languages side by side (BCP 47 tags, how a
visitor chooses). Its own conversation, when Michel opens it.

## 10. Documents That Still Say Otherwise

Changed with this specification: the starting prompt v0.62 (§6,
§7, OI-P10), v0.63 (SP-1 to SP-3, Gate order) and v0.64 (SP-4 to
SP-7), the decisions checklist v0.5 to v0.7, the reasoning v0.4.

Still saying the planner is the Curator's alone, or may never be
built, until Michel says to revise them (SP-6):

- the white paper, English and Ukrainian (§ "No algorithm
  deciding"; the gates), and its PDF; its German and Polish
  translations and their PDFs, which follow the English;
- the proposal, English and Ukrainian (the stage planner "a tool
  for the Curator"; "if needed"), and its PDF; its German and
  Polish translations and their PDFs;
- the implementation plan, English and Ukrainian ("decide whether
  the stage planner is needed at all"), and its PDF;
- the module map (T1: "a stage planner only if Gate 4 shows
  need");
- the project overview, in English, German and Polish, and its
  deck, if they name it.

## Changelog

- v0.3, amended 2026-10-11 — §3: roads the last resort, Michel's
  word; a road of up to 300 m linking two paths is part of the way
  (Claude's proposal), every road stretch named. Replaces the next.
- v0.3, amended 2026-10-11 — §3: a road weighed, not forbidden
  (six times its walking time, a main road fifteen), after the
  second corridor missed the valley path; Claude's proposal.
- v0.3, amended 2026-10-11 — §3: obvious connections joined up to
  80 m, each gap listed for a steward; Michel's word.
- v0.3, amended 2026-10-11 — §3: footpaths first, before marked
  routes, Michel's word.
- v0.3, amended 2026-10-11 — §3, the measure, Michel's word: the
  pathway is the way — the least road, then the richest way on paths
  within an allowance; time a limit, never the measure.
- v0.3, amended 2026-10-11 — SP-4 changed after the first run, on
  Michel's word: hiking paths first, roads for vehicles only when
  there is no other way.
- v0.3, amended 2026-10-11 — §3: what a start or end may be, on
  Michel's word: a host's name, a Plai place, an OSM place, or
  coordinates typed or a point placed on the map; a route to a host
  ends at the host's published point. §6: the page takes either.
- v0.3 — 2026-10-11 — SP-4 to SP-7 decided on Michel's word: the
  numbers as proposed; the first real run Verkhovyna – Zhyva Khata
  – Tepla Gora – Kosiv; the public documents revised when he says
  so; a stretch's name and note in English first, until a
  multilingual Mapservice is explored. The page's languages left
  open for the build. Amended the same day: the German and Polish
  translations, made on main meanwhile, added to §10.
- v0.2 — 2026-10-11 — SP-1, SP-2 and SP-3 decided on Michel's word:
  a steward saves drafts, the Curator publishes; the page and
  service on Plai before Gate 3, from their start prompt; the public
  answer names hosts with their detour time only. The engine at
  v0.3.
- v0.1 — 2026-10-11 — initial, from Michel's word of the same day:
  public, the Curator saves and manages stretches, stretches make a
  corridor; OI-P10 settled by it; the engine at v0.2.
