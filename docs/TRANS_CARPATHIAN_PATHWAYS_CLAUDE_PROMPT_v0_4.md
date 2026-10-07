---
title: "TRANS_CARPATHIAN_PATHWAYS_CLAUDE_PROMPT_v0_4"
subtitle: "Starting Prompt — Trans-Carpathian Pathways on Plai"
author: "Michel Garand"
date: "October 2026"
version: "v0.4"
lang: "en"
license: "CC BY-SA 4.0"
project: "Trans-Carpathian Pathways"
status: "living draft — every decision below marked open is open"
---

*Starting prompt for the Claude Project "Trans Carpathian
Pathway" and each conversation in it. Trans-Carpathian Pathways
is a project that runs on Plai, the Carpathian hub instance of
UBEC Mapservice. It does not own the stack; it is the first
project to ask Plai for things Plai does not yet do. Source
text: the proposal "Trans-Carpathian Pathways — Draft v0.1",
October 2026. Repository: `ubeccommon/trans_carpathian_pathways`;
the copy of this document in its `docs/` is the source of truth,
and the Project copy is replaced with it at each version.*

* * *

## 1. Load Order — Before Any Work

1. Attach and clone `ubeccommon/trans_carpathian_pathways` with
   push access, and `ubeccommon/ubec_mapservice` with read access
   only. `ubec_mapservice` is never written from a Pathways
   conversation unless Michel says so for a named change.
2. Read the latest version of this document in the repository's
   `docs/` fully.
3. Read, in the mapservice tree, the latest
   `docs/UBEC_MAPSERVICE_CLAUDE_PROMPT` §1, §2 and §4, and in §3
   the entries headed "The Carpathian hub and Plai", "The
   Carpathian hub as an instance" and "Plai's entry surface".
   Those bind Plai, and so bind this project. Where this
   document and the mapservice prompt disagree on anything about
   the stack, the mapservice prompt is right and this document
   is corrected.
4. Read `db/instances/plai/` and `mapbender/instances/plai/` —
   what a Plai point carries today.
5. Only then begin.

Pull before any edit to a document; the version you bump is the
one you pulled. Michel pushes to this repository from his own
clone too. When a session spans more than a day, re-clone and
re-read before acting on memory.

* * *

## 2. What This Project Is

A living network of hosts, a pathway that emerges from where
they are, and Curators who hold a stretch of it, across the
Carpathian arc. First corridor: the Hutsul highlands of western
Ukraine. Not a tourism platform, not a booking service, not a
product (proposal §9).

What this project builds is mostly not software. It is hosts
found, a Curator established, a corridor walked. Software is
built only where that work needs it, and on Plai, under
Mapservice's rule — work to need: a capability is built when an
instance requires it, not before.

**Where the work lives — Michel's word, October 7, 2026
(OI-P1).** This repository holds the project's documents, the
proposal and its build, and any Pathways tool. Plai migrations —
anything that changes what a Plai point carries — stay in
`ubec_mapservice`; this repository specifies them, it does not
hold them.

**Relation to Plai — Michel's word, October 7, 2026 (OI-P2):**
Pathways is a view of Plai's own entries, not an instance of its
own. A host is a Plai point whose category is lodging, meals,
guiding or learning; what Pathways needs beyond step A is added
to Plai by a Plai migration in `ubec_mapservice`; there is no
`pathways` database. One place for a host to enter, one consent
model, one curator queue.

What bore on it, read in mapservice at `edb1419` (prompt v0.64):
- Mapservice defines an instance as one initiative; Pathways is
  a project of the Carpathian Hub Initiative, whose instance is
  Plai.
- Every YAML application is private, and what people see is a
  copy made in Mapbender's backend whose security tab grants
  view to the public, logged-in users, groups or single users.
  So a Pathways map is a backend copy of Plai with its own
  audience, not a second instance.
- A separate instance would isolate less than it seems: one
  connections file holds write access to every instance's
  database (mapservice prompt §8, credential concentration).
- The wartime protection of a host's home is the published
  location rule (OI-P7), a gate in Plai's published view of the
  kind the contact fields already have — not a database
  boundary.

The option not taken, for the record: (b), its own instance
`pathways` reading Plai at render time only, which would have
kept the list of private homes out of the database that holds
the range-wide open map.

* * *

## 3. The First Corridor

Proposal order: Vorokhta → Kosiv → Verkhovyna. **Recommended
order, pending OI-P3:** Vorokhta → Verkhovyna → Kosiv — down
from the mountain gateway, through high-pasture country, to the
craft centre and its market, without doubling back.

Straight-line distances between town centres (approximate
coordinates, great circle — the walked distance will be longer,
measured on the walk, not here):

| Leg                    | Straight line |
|------------------------|---------------|
| Vorokhta → Verkhovyna  | about 24 km   |
| Verkhovyna → Kosiv     | about 27 km   |
| Vorokhta → Kosiv       | about 39 km   |

So the corridor is some 50 km as the crow flies in the
recommended order, which on paths is plausibly a walk of four to
six days — the Curator and the walk set the real figure.
Intermediate villages are candidate nodes, found as hosts are
found, not assigned in advance.

Before any stage is published:
- Check border-zone rules for any stage near the Romanian
  border (the Chornohora ridge); a stage that needs a permit
  says so.
- Each overnight host has a stated nearest shelter during
  air-raid alerts, held by the Curator, not published.

* * *

## 4. Roles, and How They Meet Plai's Accounts

| Proposal role | Plai today                                        |
|---------------|---------------------------------------------------|
| Host          | `PLAI_ENTRANT` — enters and edits own points      |
| Curator       | `PLAI_CURATOR` — publishes or holds; never creates |
| Traveler      | no account; sees published points only            |

Accounts are made by the administrator in Mapbender's backend,
and Mapbender 5.0.0-RC2 requires an email on every account.

**A host who does not enter alone — Michel's word, October 7,
2026 (OI-P4):** the host has their own account and the Curator
sits beside them while they enter. The host owns their row and
edits or withdraws it themselves; the Curator stays a curator and
never creates. No Plai change follows from it.

What it carries, from the stack as it stands:
- Every host account is made by the administrator in Mapbender's
  backend, in `PLAI_ENTRANT`, with a unique email (Mapbender
  5.0.0-RC2 requires one). A host without an email needs one
  before they can be entered.
- Each host is a login, and a login is a trace (Mapservice §4,
  minimal accounts).
- Real accounts wait for Mapservice's own condition: backups
  before any real account, the off-host copy on Michel's
  computer.

The options not taken, for the record: (a) the Curator enters on
the host's behalf from an entrant account of their own, consent
on paper, the Curator owning the row; (c) a Plai migration adding
"entered on behalf of" and a later hand-over of ownership.

* * *

## 5. What a Host Carries — the Gap Against Plai Step A

The proposal's five offers against Plai's category list
(`db/instances/plai/001_entry_fields.sql`):

| Proposal offer   | Plai category           | Fit                     |
|------------------|-------------------------|-------------------------|
| Overnight stay   | `lodging`               | yes                     |
| A meal           | `meals`                 | yes                     |
| Local guidance   | `guiding`               | yes                     |
| A workshop       | `learning`, `crafts`    | yes — two codes         |
| A view           | —                       | no: a view is a place, not an offer |

Recommended (OI-P5): a view becomes a location type —
`viewpoint`, "Viewpoint" — that anyone or the Curator may map,
not a host offer.

What the proposal asks of a host point that Plai step A does not
hold (OI-P6, each a column or table in a Plai migration, none
built):

- **More than one offer per host.** Plai: one category per point.
  A bed, a meal and a walk at one farm is three points or one
  point with a list — decide which.
- **Availability** — the proposal deliberately keeps this with
  the Curator ("maintains the living map of who is available").
  Recommended: a season (months open) on the row; day-to-day
  availability stays with the Curator, never a calendar. A
  calendar is the first step to a booking service.
- **Capacity** — beds; people at a meal. Small integers.
- **Languages the host speaks** — a closed list (uk, en, de, fr,
  pl, ro, sk, hu, …).
- **Access** — reachable on foot only, by car, with a pram, with
  a wheelchair. Feeds the family-with-small-children journey.
- **Exchange** — see OI-P8.

**Published location of a private home (OI-P7).** Plai's
precision is free and its published point is the point entered.
For a host's home, published exactly, in wartime, with a name on
it, that is an address. Options: publish the exact point (as
today); or publish a generalised point (e.g. the village, or a
fixed offset) for `lodging` at a home, the exact point going to a
traveler through the Curator. Plai's `show_C`/`consent_C`
convention already gates contact fields; the geometry is the one
field it does not gate.

* * *

## 6. The Stage Planner (the proposal's "spatial algorithm")

Specified here, not built. Built only when the first corridor
has enough hosts to need it — with five hosts, the Curator plans
on paper.

**What it is for:** the Curator. It proposes; the Curator
disposes. It never answers a traveler directly.

**Input**
- Published host points with their offers, season, capacity,
  languages, access.
- The path network: OpenStreetMap footways, paths and tracks in
  `reference_sa.osm_line` (Plai's base map, already loaded).
- Terrain: a DEM for ascent and descent (source and licence to
  be recorded at load — OI-P9).
- The request: start, end or loop; days; party (family, solo,
  couple, group); mode (walk, cycle, drive); month.

**Edge cost — walking:** DIN 33466 hiking time: 4 km/h on the
flat, 300 m/h ascent, 500 m/h descent; segment time = the larger
of the horizontal and vertical times plus half the smaller.
Family and group profiles scale it; the Curator sets the scale.

**Constraint, not optimisation:** each day ends at a host with an
overnight offer, open that month, with capacity for the party;
each day stays under the party's limit in hours and ascent. Among
plans that satisfy that, prefer more distinct encounters (a meal,
a workshop, a viewpoint passed) over less time — "the logic of
encounter, not just efficiency". Output: two or three candidate
stage plans with times, ascent and the hosts met, for the
Curator to change.

**Licence (OI-P10).** A route drawn from OpenStreetMap is a work
derived from an ODbL source. Mapservice's rule: segregate data
is combined at render time and never joined into a project's
tables. So either the planner computes on request and stores
nothing, or a stored route line lives in `instance_sa.*` and is
published under ODbL. Decide before the first route is saved.

**Where it runs.** The stack's image (`postgis/postgis:18-3.6`)
has no pgRouting. Default proposal: a Python tool, in the
mapservice tool style, that reads a corridor's paths and hosts,
builds the graph in memory (networkx), and writes nothing but its
answer. Adding pgRouting to the image is a framework change and
Mapservice's to decide. If built, the tool lives in this
repository's `tools/`.

* * *

## 7. Principles — Operational

From the proposal §8, binding:

- **Honest offer** — hosts offer only what they actually have.
- **No performance** — the encounter is real or it is nothing.
- **Organic growth** — the network grows from the inside out.
- **Curator as memory** — the human holds what the algorithm
  cannot; the planner is the Curator's tool.
- **The traveler arrives** — the journey is undergone, not
  consumed.
- **Off the beaten path** — where people live, not where tourists
  are sent.
- **A pathway of relationships** — human to human, human to
  nature.

Inherited from Mapservice and binding here: one instance, one
database; no secrets in any repository; consent and publication
as columns; minimal accounts; exposure is a decision; licence
recorded at use.

Added here:

- **A host's home is not a map pin by default** (pending OI-P7).
- **No calendar.** Availability beyond season stays a
  conversation with the Curator.
- **Safety is the Curator's to hold**, not the traveler's to
  find: shelter, border zone, alerts.

* * *

## 8. Gates — Phase 1

Gate-by-gate: a gate opens on Michel's word, not on a date.

- **Gate 0 — Decisions.** OI-P1 to OI-P8 answered or explicitly
  deferred.
- **Gate 1 — Plai in a browser.** Michel's look as a throwaway
  entrant and curator (pending on the mapservice side). Pathways
  adds nothing to Plai until a Digitizer save has worked in a
  browser.
- **Gate 2 — Host fields.** One Plai migration for what OI-P5
  and OI-P6 decide, with `verify` and the leak pass extended to
  the new fields, the published location rule (OI-P7) among
  them.
- **Gate 3 — First hosts.** Three to five hosts in the corridor,
  entered by the route OI-P4 chose, one Curator named.
- **Gate 4 — First walk.** The corridor walked end to end. What
  is recorded: walked distance and time per stage, what was
  missing, what a traveler needed and did not have.
- **Gate 5 — Planner, if needed.** Built only if Gate 4 shows the
  Curator needs it, against the stages actually walked as its
  test cases.

* * *

## 9. Open Items

- **OI-P1** — Closed, Michel's word, October 7, 2026: the
  repository `ubeccommon/trans_carpathian_pathways` for
  documents, the proposal build and tools; Plai migrations stay
  in `ubec_mapservice`. §2.
- **OI-P2** — Closed, Michel's word, October 7, 2026: a view of
  Plai's entries, fields by Plai migration, a Pathways map as a
  backend copy of Plai. §2.
- **OI-P3** — Corridor order: Vorokhta → Verkhovyna → Kosiv. §3.
- **OI-P4** — Closed, Michel's word, October 7, 2026: the host's
  own account, the Curator beside them while they enter. §4.
- **OI-P5** — "A view" as location type `viewpoint`. §5.
- **OI-P6** — Which host fields, and multiple offers as rows or
  points. §5.
- **OI-P7** — Published location of a private home. §5.
- **OI-P8** — The exchange. The proposal names economic
  marginalisation as half the problem and says nothing of how a
  host is paid: fixed contribution, a suggested contribution,
  gift, exchange of work, or `ubec-pay`. Decide before the first
  traveler, not after.
- **OI-P9** — DEM source and licence, at Gate 5 only.
- **OI-P10** — Route licence: computed and unstored, or stored
  under ODbL in `instance_sa`. §6.
- **OI-P11** — The Phase 3 country list: the proposal names seven
  countries; the Outlook boundary that sets Plai's extent
  reaches nine, Austria and Bulgaria included (mapservice
  prompt §3).
- **OI-P12** — Travel in wartime: what the project says to a
  traveler from abroad about advisories, insurance and martial
  law, and who says it.

* * *

*Changelog*
- v0.4 — 2026-10-07 — OI-P4 closed on Michel's word: each host
  has their own account and enters with the Curator beside them;
  what follows from Plai's accounts recorded.
- v0.3 — 2026-10-07 — OI-P2 closed on Michel's word: Pathways is
  a view of Plai, not its own instance; what bore on it recorded
  from mapservice `edb1419` (prompt v0.64), including the
  per-application viewing rights that give a Pathways map its
  own audience.
- v0.2 — 2026-10-07 — moved into the repository, whose copy is
  now the source of truth; OI-P1 closed on Michel's word (this
  repository; Plai migrations stay in `ubec_mapservice`); load
  order clones both repositories, mapservice read-only; a
  planner, if built, goes in `tools/`. Read against mapservice
  commit `30e6b48` (its prompt v0.62).
- v0.1 — 2026-10-07 — initial, from proposal Draft v0.1 and
  Plai at mapservice commit `7a5ce95` (entry surface step A).
