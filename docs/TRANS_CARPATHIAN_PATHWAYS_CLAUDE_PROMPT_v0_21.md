---
title: "TRANS_CARPATHIAN_PATHWAYS_CLAUDE_PROMPT_v0_21"
subtitle: "Starting Prompt — Trans-Carpathian Pathways on Plai"
author: "Michel Garand"
date: "October 2026"
version: "v0.21"
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
  boundary. (OI-P7 was then decided the same day: the exact
  point, as today. §5.)

The option not taken, for the record: (b), its own instance
`pathways` reading Plai at render time only, which would have
kept the list of private homes out of the database that holds
the range-wide open map.

**The user manual — Michel's word, October 8, 2026.** One manual
for entrants and curators, English and Ukrainian, built to one A4
PDF like the proposal, with Plai's emblem on its cover:
`docs/manual/`, built by `build/build_manual.py`. It is read
against Plai as it stands — the entries scheme v0.7, the curation
scheme v0.6, template 008's rules (mapservice `1c1c192`) — and
quotes every screen label in English, since Plai's screens are
English; the Ukrainian text glosses them. When a Plai form or
rule changes, the manual is checked against it and rebuilt. It
says what the stack cannot yet do: no password-reset mail (no
mailer is set), so a forgotten password goes to the administrator.
Manual v0.3 carries Michel's screenshots, taken on the host the
evening of October 8 with no test entry: the list of maps, the
login page, the toolbar, "My places" and the form in three parts,
cropped and kept in `docs/manual/img/` without their metadata, the
same pictures in both languages. They showed two things the text
had not said: required fields are outlined in red on screen, not
starred, and "Select by current extent only", ticked when the panel
opens, lists only the places in view. Still to come from him: the
curator's form, the public popup on a published place, and the
"State" list below the agreement.

**The co-creator agreement — Michel's word, October 8, 2026.**
One agreement for every role that builds the project — host,
pathway steward, Curator, traveler, contributor, partner
initiative, funder, and the administrator — English and
Ukrainian, built to one A4 PDF like the proposal:
`docs/agreement/`, built by `build/build_agreement.py`. It is a
draft for Michel's word, not for signing: items A-1 to A-7 are
open (who answers for the project, rights in entries, how payment
passes, a deputy administrator, governing law, retention, how
each role signs), and the cover and every footer say "Draft".
It follows the project review
(`docs/reviews/TRANS_CARPATHIAN_PATHWAYS_PROJECT_REVIEW_v0_1.md`),
whose §5 lists Claude's own proposals in the draft so none is read
as decided, and whose drifts and risks are not yet acted on.

**The agreement on every Plai entry — Michel's word, October 8,
2026.** Whoever creates a point ticks that they have read the
co-creator agreement and accept it, a link to it beside the tick.
His answers: build now and link draft v0.2; serve the PDF from
Mapservice, since this repository is private; record the tick,
the version and the time; purge the two rows of his host-fields
look first. Built in `ubec_mapservice` as `plai/004` (`064c34a`,
its prompt v0.80): `agreement_accepted` required, the version
from `instance.meta agreement_version` and the time given by the
database and kept on every save, none of it public; the entries
scheme v0.8; the PDF at `/ubec/agreement/`, its file named for its
version. Proven locally (`verify plai vt` 99 of 99), and on the
host the same afternoon after the look's two rows were purged:
`verify plai vt` 96 of 96, the leak pass 519 of 519, none skipped
(mapservice `bbc6a36`, its prompt v0.81). Left: Plai's user copy
made again and exported, and Michel's look as a throwaway entrant. A new version of the agreement on Plai is a new PDF
there, a new link in the scheme and a new `agreement_version` — a
Plai migration. The user manual v0.2 says what the entrant and
the curator see.

**The reasoning — Michel's word, October 9, 2026.** Why the
project exists and the reasons behind its principles, in
`docs/TRANS_CARPATHIAN_PATHWAYS_REASONING_v0_1.md`, English first,
Ukrainian once it settles. His direction, recorded there: the two
forces — the mountains re-valued from outside (tourism and
property, energy on the high meadows, EU accession, the Carpathian
Eight launched in Bukovel in September 2026, ageing holders) and
the people who keep them alive, newcomers among them; that a
community's spokesmen are asked who they speak for, this project
included ("no one speaks for a community"); and corridors of
cultural, natural and landscape stewardship that emerge from the
places and paths, grounded in spirituality and relationship, not
wilderness ("people and land are one and the same"). Twelve
tensions are set out there with what answers them and what is
open (T-1 to T-12), for Michel's word. Two bear on other
documents: T-10, the corridors cannot draw on a host's place while
the agreement's §5 says "for nothing else"; and the proposal that
its §5 become the one list of principles (project review D-6).

* * *

## 3. The First Corridor

**The order — Michel's word, October 7, 2026 (OI-P3):**
Vorokhta → Verkhovyna → Kosiv — down from the mountain gateway,
through high-pasture country, to the craft centre and its
market, without doubling back. (The first draft's order,
Vorokhta → Kosiv → Verkhovyna, not taken.)

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

| Role            | Does                                   | Plai                      |
|-----------------|----------------------------------------|---------------------------|
| Host            | enters their own place, or has it entered | `PLAI_ENTRANT`, or none |
| Pathway steward | cares for a stretch; enters for a host, adds places along the way | `PLAI_STEWARD` |
| Curator         | publishes or holds; also enters        | `PLAI_CURATOR` and `PLAI_ENTRANT` |
| Traveler        | sees published points                  | no account                |

**The pathway steward — Michel's word, October 8, 2026:** a new
role, someone who cares for a stretch of pathway and may add for
a host and add places along the way. On Plai a steward is an
entrant: the group means "may enter", not "is a host"; what a
steward enters is their row, under their name, as when the
Curator enters for a host (above). The stretch a steward cares
for is the project's knowledge, not a column. The Curator keeps
the whole: publishing, and the living map of who can receive
whom. The proposal's "become a Curator and hold a stretch" line
moves to the steward in its next version.

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

**Amended — Michel's word, October 8, 2026:** the Curator also
enters points — for a host who cannot, and for places along the
way (a viewpoint, a spring). No change to Plai: the Curator's
Mapbender account is put in `PLAI_ENTRANT` as well as
`PLAI_CURATOR` (or in `PLAI_ADMIN`, which the application treats
as both), so both schemes show; what it creates goes through the
entry role under the Curator's name, and the database rule that
the curator role never creates stands. Such a point is the
Curator's row — the host cannot edit or withdraw it themselves,
their consent is on paper and the `data_consent` tick is the
Curator's on their behalf; a hand-over of ownership would be a
Plai migration (option (c) below), not yet asked for.

The option not taken, for the record: (c) a Plai migration adding
"entered on behalf of" and a later hand-over of ownership.

* * *

## 5. What a Host Carries — the Gap Against Plai Steps A and B

The proposal's five offers against Plai's category list
(`db/instances/plai/001_entry_fields.sql`):

| Proposal offer   | Plai category           | Fit                     |
|------------------|-------------------------|-------------------------|
| Overnight stay   | `lodging`               | yes                     |
| A meal           | `meals`                 | yes                     |
| Local guidance   | `guiding`               | yes                     |
| A workshop       | `learning`, `crafts`    | yes — two codes         |
| A view           | —                       | no: a view is a place, not an offer |

**A view — Michel's word, October 7, 2026 (OI-P5):** a new
location type `viewpoint`, "Viewpoint", in Plai's list, that
anyone or the Curator may map; not a host offer.

**What a host point carries — Michel's word, October 7, 2026
(OI-P6):** one point with a list of offers, not a point per
offer — one place, one consent set, one photo. And four fields
beside it, all of them:

- **Season** — the months open. Day-to-day availability stays
  with the Curator, never a calendar; a calendar is the first
  step to a booking service.
- **Capacity** — beds; people at a meal, a walk, a workshop.
  Small whole numbers.
- **Languages the host speaks** — a closed list.
- **Access** — reachable on foot only, by car, with a pram, with
  a wheelchair. Feeds the family-with-small-children journey.

Plai's step B (one photo per place, cleaned of metadata, mapservice
`plai/002`) was built and run on the host the same day, so images
are no longer a Pathways need. What these decisions ask of Plai is
specified in `docs/specs/PLAI_HOST_FIELDS_SPEC`; it is built in
`ubec_mapservice` as a Plai migration, not here.

**How a host is paid — Michel's word, October 7, 2026 (OI-P8):**
four forms, all of them: a fixed contribution, a suggested
contribution, exchange of work, and `ubec-pay` or a community
currency. Gift, the fifth form named in v0.1, was not among
them. Who chooses among the four — Michel's word, October 7,
2026 (OI-P13, first half): the host, per offer, so each offer on
a point says which forms the host accepts. Still open (OI-P13,
second half): whether payment passes host to traveler directly
or through the Curator or `ubec-pay` — whether the project holds
money.

**Published location of a private home — Michel's word,
October 7, 2026 (OI-P7):** the exact point, as today. Plai's
precision is free and a published point is the point entered,
for a home as for any other place; nothing in Plai changes. The
host decides where they place the point, the Curator decides
whether the entry is published, and the contact fields stay
gated by `consent_C` and `show_C` as step A built them.

Said before the decision and kept for the record: for a host's
home, published exactly, in wartime, with a name on it, the
point is an address.

The options not taken: a generalised point always published for
a home, the exact one passed through the Curator; and the host
deciding, generalised by default, through a consent and show
pair on the geometry.

The outward proposal said otherwise ("A home is not a public
pin"); proposal v0.2, October 7, corrects it in both languages.

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

- **A home is published at the point entered** (OI-P7): the
  host places it, the Curator publishes or holds the entry.
- **No calendar.** Availability beyond season stays a
  conversation with the Curator.
- **Safety is the Curator's to hold**, not the traveler's to
  find: shelter, border zone, alerts.

* * *

## 8. Gates — Phase 1

Gate-by-gate: a gate opens on Michel's word, not on a date.

- **Gate 0 — Decisions.** OI-P1 to OI-P8 answered or explicitly
  deferred. All eight answered on Michel's word, October 7, 2026.
- **Gate 1 — Plai in a browser.** Michel's look as a throwaway
  entrant and curator (pending on the mapservice side). Pathways
  adds nothing to Plai until a Digitizer save has worked in a
  browser.
- **Gate 2 — Host fields.** One Plai migration, `plai/003`, for
  what `docs/specs/PLAI_HOST_FIELDS_SPEC` says (OI-P5, OI-P6,
  OI-P13, Q1 to Q8), with `verify` and the leak pass extended to
  the new fields and hosts drawn as a style on the entry layer.
  The published location stays the point entered (OI-P7).
  **Built October 7, 2026, on Michel's word** — mapservice
  `a386165`, proven locally (spec v0.4); on the host the same
  day, verify 91 of 91, the leak pass 519 of 519. **Closed
  October 8, 2026, on Michel's word**, after his look in a
  browser: a place entered and published, a workshop host with a
  capacity and three languages published and drawn in ochre to
  the public, the click carrying every host field. The look found
  two faults older than `003` and fixed in mapservice the same
  morning — every scheme had listed its `fields` without `id`
  since step A, so a publish was refused and an edit inserted a
  second row (`e203e3f`); and `PLAI_STEWARD` became a group of its
  own (`727aeec`). Mapservice at `d0456b4`, prompt v0.72.
  **Gate 2 closes before Gate 3 opens, as a hard constraint**
  (state review v0.1, F-3): Mapservice's proofs refuse or skip an
  instance that holds entries and no throwaway carries Plai's own
  migrations, so `003` can only be proven while Plai is empty.
- **Gate 3 — First hosts.** Three to five hosts in the corridor,
  entered by the route OI-P4 chose, one Curator named. Opens only
  after Mapservice's own condition on real accounts is met —
  backups with an off-host copy, which nothing in that tree yet
  implements (its review's F5; state review v0.1 §2).
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
- **OI-P3** — Closed, Michel's word, October 7, 2026: Vorokhta →
  Verkhovyna → Kosiv. §3.
- **OI-P4** — Closed, Michel's word, October 7, 2026: the host's
  own account, the Curator beside them while they enter; amended
  October 8: the Curator also enters, for a host who cannot and
  for places along the way, from an account in both groups. §4.
- **OI-P5** — Closed, Michel's word, October 7, 2026: location
  type `viewpoint`. §5.
- **OI-P6** — Closed, Michel's word, October 7, 2026: one point
  with a list of offers; season, capacity, languages, access.
  §5.
- **OI-P7** — Closed, Michel's word, October 7, 2026: the exact
  point, as today. §5.
- **OI-P8** — Closed, Michel's word, October 7, 2026: fixed
  contribution, suggested contribution, exchange of work, and
  `ubec-pay` or a community currency. §5.
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
- **OI-P15** — Closed, Michel's word, October 8, 2026:
  `PLAI_STEWARD` is a group of its own. Built in mapservice
  `727aeec` (`instance.py entry-groups`, application template
  v0.20, Plai's entries scheme v0.5); on the host: `entry-groups
  plai STEWARD`, `render`, `cache:clear`, the group made in the
  backend. §4.
- **OI-P14** — A place nobody hosts (a viewpoint, a spring,
  entered by the Curator) still needs a `category` and a contact
  email, as every Plai point does since `plai/001`. For the pilot:
  "Something else" and the Curator's email. Whether such a place
  should need neither is a Plai change (`plai/004`), on Michel's
  word.
- **OI-P13** — First half closed, Michel's word, October 7, 2026:
  the host chooses, per offer. Open: whether payment passes
  directly or through the Curator or `ubec-pay`. §5. Before the
  first traveler.

* * *

*Changelog*
- v0.21 — 2026-10-09 — the reasoning document v0.1, Michel's word:
  why now, corridors of stewardship, the principles with their
  reasons, tensions T-1 to T-12.
- v0.20 — 2026-10-08 — manual v0.3: Michel's screenshots in both
  languages; three more wanted.
- v0.19 — 2026-10-08 — `plai/004` on the host: verify 96 of 96,
  the leak pass 519 of 519.
- v0.18 — 2026-10-08 — the agreement on every Plai entry,
  Michel's word: mapservice `plai/004` (`064c34a`); manual v0.2.
- v0.17 — 2026-10-08 — the co-creator agreement, Michel's word:
  every role, English and Ukrainian, one PDF in `docs/agreement/`,
  a draft with A-1 to A-7 open; the project review v0.1 recorded.
- v0.16 — 2026-10-08 — the user manual, Michel's word: entrants
  and curators, bilingual PDF in `docs/manual/`, Plai's emblem on
  the cover.
- v0.15 — 2026-10-08 — Gate 2 closed on Michel's word after the
  browser look; what the look found recorded; spec v0.5.
- v0.14 — 2026-10-08 — OI-P15 closed on Michel's word:
  `PLAI_STEWARD` a group of its own, built in mapservice `727aeec`.
- v0.13 — 2026-10-08 — the pathway steward, Michel's word: a new
  role, an entrant on Plai; the roles table rewritten; OI-P15
  opened for a group of its own.
- v0.12 — 2026-10-08 — OI-P4 amended on Michel's word: the
  Curator also enters points, from an account in both groups;
  OI-P14 opened, the shape of a place nobody hosts.
- v0.11 — 2026-10-07 — Gate 2 built on Michel's word (mapservice
  `a386165`, spec v0.4); closes on his host run and browser look.
- v0.10 — 2026-10-07 — the mapservice state review
  (`docs/reviews/UBEC_MAPSERVICE_STATE_REVIEW_v0_1.md`) read and
  its findings applied on Michel's word in spec v0.3: hosts a
  style on the entry layer (Q4), `category` beside `offers` (Q7),
  `reach` for `access` (Q8). Gate 2 before Gate 3 recorded as a
  hard constraint; Gate 3 waits on Mapservice's backup condition.
- v0.9 — 2026-10-07 — the proposal's contrary line on a home
  recorded as corrected (proposal v0.2).
- v0.8 — 2026-10-07 — OI-P3 closed on Michel's word: Vorokhta →
  Verkhovyna → Kosiv. Gate 0's eight items all answered. The
  host-fields specification settled at v0.2 but for its Q4.
- v0.7 — 2026-10-07 — OI-P5 and OI-P6 closed and OI-P13's first
  half, on Michel's word: `viewpoint` a location type; one point
  with a list of offers; season, capacity, languages, access; the
  host chooses payment forms per offer. Plai's step B (photo)
  recorded as built (mapservice `b9edde4`, prompt v0.66). The
  host fields go to `docs/specs/PLAI_HOST_FIELDS_SPEC`.
- v0.6 — 2026-10-07 — OI-P8 closed on Michel's word: four forms
  of payment, gift not among them; OI-P13 opened for who chooses
  among them and how payment passes. Gate 0's four blocking
  items are answered.
- v0.5 — 2026-10-07 — OI-P7 closed on Michel's word: a home is
  published at the point entered, as today; the principle "not a
  map pin by default" replaced; Gate 2 no longer carries a
  location rule; the proposal's contrary line flagged.
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
