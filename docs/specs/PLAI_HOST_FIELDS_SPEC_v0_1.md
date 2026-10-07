---
title: "PLAI_HOST_FIELDS_SPEC_v0_1"
subtitle: "What a Plai point carries for Trans-Carpathian Pathways"
author: "Michel Garand"
date: "October 2026"
version: "v0.1"
lang: "en"
license: "CC BY-SA 4.0"
project: "Trans-Carpathian Pathways"
status: "draft — for Michel's review; nothing here is built"
---

*A specification for one Plai migration in `ubec_mapservice`,
proposed as `db/instances/plai/003_host_fields.sql`, with the
scheme, view and proof changes that go with it. It is not the
migration. It is built there, in that repository's own way and
on Michel's word for that change, and where this document and
the mapservice prompt disagree about the stack, the mapservice
prompt is right. Read against mapservice `b9edde4` (prompt
v0.66): Plai's step A (`plai/001`, the entry fields) and step B
(`plai/002`, one photo) built and running on the host.*

* * *

## 1. What It Rests On

Every column below traces to one of these. Where a line in this
document is Claude's proposal rather than a decision, it says so.

| Item   | Michel's word, October 7, 2026                            |
|--------|-----------------------------------------------------------|
| OI-P2  | Pathways is a view of Plai; its fields come by Plai migration |
| OI-P4  | Each host has their own account and owns their row        |
| OI-P5  | `viewpoint` becomes a location type                       |
| OI-P6  | One point with a list of offers; season, capacity, languages, access |
| OI-P7  | A home is published at the point entered                  |
| OI-P8  | Four forms of payment: fixed, suggested, work, `ubec-pay` |
| OI-P13 | The host chooses the forms, per offer (first half only)   |

Consequences that need no new decision:
- No new owner or on-behalf column (OI-P4): the host saves their
  own row, as every Plai entrant does.
- No rule on the geometry (OI-P7): the point is published as
  entered, behind the curator's publish, as today.
- No image column (step B already built it).

* * *

## 2. The Closed Lists

Five new tables in the shape of `plai/001`'s two —
`code text PRIMARY KEY CHECK (code ~ '^[a-z][a-z0-9_]*$')`,
`label text NOT NULL`, `ordinal int NOT NULL` — owned by the
instance role, readable by the entry and curator roles. Labels
in English, as Plai's lists are for now; a change is a new
migration.

**`instance.entry_offer`** — the proposal's four offers
(OI-P6).

| code       | label           | ordinal |
|------------|-----------------|---------|
| `lodging`  | Overnight stay  | 10      |
| `meal`     | A meal          | 20      |
| `guiding`  | Local guidance  | 30      |
| `workshop` | A workshop      | 40      |

**`instance.entry_payment`** — the four forms (OI-P8).

| code        | label                              | ordinal |
|-------------|------------------------------------|---------|
| `fixed`     | Fixed contribution                 | 10      |
| `suggested` | Suggested contribution             | 20      |
| `work`      | Exchange of work                   | 30      |
| `ubec`      | ubec-pay or a community currency   | 40      |

**`instance.entry_month`** — the season (OI-P6): `jan` January
10 … `dec` December 120.

**`instance.entry_language`** — languages the host speaks
(OI-P6). The eight named in the starting prompt, each labelled
in English with its own name beside it:

| code | label                     | ordinal |
|------|---------------------------|---------|
| `uk` | Ukrainian — українська    | 10      |
| `en` | English                   | 20      |
| `de` | German — Deutsch          | 30      |
| `fr` | French — français         | 40      |
| `pl` | Polish — polski           | 50      |
| `ro` | Romanian — română         | 60      |
| `sk` | Slovak — slovenčina       | 70      |
| `hu` | Hungarian — magyar        | 80      |

Which others belong (Czech, Rusyn, Romani, Serbian, Russian …)
is open — Q2 in §8. The codes are ISO 639-1, so a later row is
unambiguous.

**`instance.entry_access`** — how the place is reached (OI-P6).

| code         | label                    | ordinal |
|--------------|--------------------------|---------|
| `foot`       | On foot only             | 10      |
| `car`        | By car                   | 20      |
| `pram`       | With a pram              | 30      |
| `wheelchair` | With a wheelchair        | 40      |

**`instance.entry_location_type`** gains one row (OI-P5):
`('viewpoint', 'Viewpoint', 135)` — between "Spring or well"
and "Forest or woodland site".

* * *

## 3. The Columns

All on `instance.entry`, all nullable, so that every place on
Plai that is not a host — an orchard, a spring, a viewpoint —
carries nothing new.

| Column              | Type       | Holds                                        |
|---------------------|------------|----------------------------------------------|
| `offers`            | `text`     | codes of `entry_offer`, comma-joined          |
| `season`            | `text`     | codes of `entry_month`, comma-joined          |
| `languages`         | `text`     | codes of `entry_language`, comma-joined       |
| `access`            | `text`     | codes of `entry_access`, comma-joined         |
| `capacity_lodging`  | `smallint` | beds                                          |
| `capacity_meal`     | `smallint` | people at one meal                            |
| `capacity_guiding`  | `smallint` | people on one walk                            |
| `capacity_workshop` | `smallint` | people at one workshop                        |
| `pay_lodging`       | `text`     | codes of `entry_payment`, comma-joined        |
| `pay_meal`          | `text`     | as above, for a meal                          |
| `pay_guiding`       | `text`     | as above, for guidance                        |
| `pay_workshop`      | `text`     | as above, for a workshop                      |

Capacity and payment are per offer because OI-P13 put the choice
of payment with the host per offer, and a bed count means nothing
for a walk. Four fixed offers make four pairs of columns rather
than a child table: the Digitizer edits one row per point and has
no form for rows beneath it.

**Why comma-joined text, not an array or a link table.** Read at
Digitizer 3.0.0-RC3 (`aaec85e`, `DataManagerBundle/…/FormUtil.js`
and `FormRenderer.js`): a select with `multiple: true` is saved as
one value, its choices joined by `,` (or the element's
`data-multiselect-separator`), and as null when nothing is
chosen; it is read back by splitting on the same separator. A
`text[]` column would refuse that string. So the column is text,
and the database, not the form, holds it to the list (§4).

**Why `smallint` is safe in the form.** Read at the same tag
(`DataSourceBundle/Component/Meta/TableMeta.php`,
`Column.php`): an empty string sent to a numeric column is
replaced by the column's safe default, which is null for a
nullable column. An empty capacity field is saved as null, not
refused.

* * *

## 4. What the Database Holds the Rows To

Added to Plai's normalizer, `instance.entry_plai_normalize()`,
which already fires before template 008's trigger
(`entry_a_plai_normalize` sorts first by name):

1. **Each comma-joined column is cleaned and checked.** Split on
   `,`, trim each part, drop empties and duplicates, refuse any
   code not in its table (`RAISE` naming the column and the
   code), and write the codes back in ordinal order — so the
   stored value is canonical and a re-save changes nothing.
   Nothing chosen is null. This is load-bearing, not tidiness:
   template 008 returns a published row to submitted when an
   entrant's save changes any column, comparing value by value
   (`008_entry_rules.sql`), so `meal,lodging` saved over
   `lodging,meal` would unpublish a host who changed nothing.
2. **Offers decide what else stands.** Where an offer is not in
   `offers`, its `capacity_*` and `pay_*` are set to null rather
   than refused: a host who unticks lodging and leaves the bed
   count in the form has not said anything false.
3. **Capacity is a small positive number.** `CHECK` on each
   `capacity_*`: null, or 1 to 99.
4. **"On foot only" excludes "By car".** Refused if both are in
   `access`.
5. **A host is a place with offers.** Nothing else ties an offer
   to a category or a type: a farm, a guesthouse and a shepherd's
   hut can all offer a bed.

Proposed, for Michel (Q1 in §8): a listed offer must name at
least one form of payment — refused otherwise — because OI-P8 is
to be settled "before the first traveler, not after", and a host
point that offers a bed without saying on what terms leaves it
to be settled at the door.

Grants, by the lesson of step A (an update writes back every
column its scheme loaded, so a missing grant is a failed save):
`UPDATE` on all twelve columns to the entry role and to the
curator role. Template 008's trigger puts back every column of a
curator's save but the state and the `show_*` columns — read in
`008_entry_rules.sql`, by key over the whole row, so new columns
are covered with no change there — and the grant lets a
curator's save succeed without letting a curator change a host's
answers.

* * *

## 5. What the Public Sees

**No new consent pair** — Claude's proposal, traced to the step
A rule that a place's descriptive fields (name, types, category,
offering) are public once the entry is published, and to OI-P7,
which leaves the location as entered. Offers, season, capacity,
payment forms, languages and access describe the place and its
terms, not the person; the host chooses to enter them, and the
curator chooses whether the entry is published at all. The
contact fields and the photo stay gated as they are. If Michel
wants any of these gated per field (capacity of a home, say),
template 008's `consent_C`/`show_C` convention takes it with no
new mechanism — Q3 in §8.

**The published view** `instance.entry_public` grows, at its
end, after `image_html`:

| View column         | From                                         |
|---------------------|----------------------------------------------|
| `offers`            | labels, in ordinal order, joined by ` · `     |
| `season`            | labels, joined by ` · `                       |
| `languages`         | labels, joined by ` · `                       |
| `access`            | labels, joined by ` · `                       |
| `capacity_lodging` … `capacity_workshop` | the numbers          |
| `pay_lodging` … `pay_workshop` | labels, joined by ` · `        |
| `is_host`           | `offers IS NOT NULL`                          |

Labels are resolved in the view, from the list tables, so the
click, every export (`backup.py` reads the view) and any later
Pathways map read one place. `is_host` is the one thing a
Pathways map filters on (§6).

**The click** (`instance.meta`): `entry_info_fields` and
`entry_info_labels` gain the new view columns but `is_host`,
labelled "Offers", "Season", "Languages", "Access", "Beds",
"At a meal", "On a walk", "At a workshop", "Terms — overnight",
"Terms — meal", "Terms — guidance", "Terms — workshop". An empty
value prints nothing, as today.

* * *

## 6. The Pathways Map

OI-P2: a Pathways map is a backend copy of Plai with its own
audience, not a second instance. What a copy cannot do by itself
is show hosts only: it draws the layers the instance's mapfile
offers. So one more layer is needed, over the same published
view, filtered on `is_host` — a filter in the mapfile's SQL, not
in the front end, as Mapservice §4 requires.

How that layer is declared — a second entry-layer block in the
mapfile template for instances that ask for it, or a row in
`instance.layer` over a view — is Mapservice's to decide (Q4 in
§8). This specification asks only that it read
`instance.entry_public` and filter on `is_host`, so that the
publication state, every consent gate and withdrawal hold for it
exactly as for the entry layer.

* * *

## 7. The Forms and the Proofs

**Entrant's scheme** (`mapbender/instances/plai/entries.yaml`):
the twelve columns join `fields`; after "Offering", a group
headed "If you host travelers":

- `offers` — select, `multiple: true`, from `entry_offer`;
- per offer, `capacity_<offer>` — input `type: number`, min 1,
  max 99 — and `pay_<offer>` — select, `multiple: true`, from
  `entry_payment`, titled by the offer ("Overnight stay — how
  you are paid");
- `season`, `languages`, `access` — select, `multiple: true`,
  from their tables.

The `__OPTIONS <table>__` line the renderer already expands
serves every list. A multiple select must have no empty option
(read at `FormRenderer.js`: select2's own rule).

**Curator's scheme** (`curation.yaml`): the same twelve in
`fields`, shown read-only, because the curator's save writes back
what it loaded.

**Proofs**, in mapservice's own tools:
- `instance.meta entry_probe` gains values for every new column
  that `verify` and the leak pass insert — one offer at least,
  its capacity and payment, one each of the lists.
- `verify` gains refusals: an unknown code in each list column,
  `foot` with `car`, a capacity of 0 and of 100; and the
  clearing: a capacity and a payment for an offer not listed,
  null after save; a re-save of a canonical row, unchanged.
- The leak pass: the new view columns appear only for published
  rows, in every format of the click, and the hosts layer of §6
  returns no row the entry layer would not.
- A browser save as a throwaway entrant with every list filled,
  and a curator's publish of it — the step A lesson that no tool
  here sees what the Digitizer actually writes.

* * *

## 8. Open, for Michel

- **Q1** — Must each listed offer name at least one form of
  payment (§4)? Proposed: yes.
- **Q2** — The language list beyond the eight (§2).
- **Q3** — Any of the new fields gated by its own consent pair
  rather than public once published (§5)? Proposed: none.
- **Q4** — How the hosts layer is declared (§6): Mapservice's
  word, on the mapservice side.
- **Q5** — A fixed contribution has an amount, and this
  specification carries none: whether an amount (and a currency)
  is on the map, or stays with the Curator like availability.
  Proposed: with the Curator for the pilot.
- **Q6** — Whether `season` left empty reads "ask the Curator"
  (proposed) or "all year".

Not here, and why: how payment passes (OI-P13, second half —
it decides whether the project holds money, not what a point
carries); Ukrainian labels for every list (Plai's lists are
English for now, multilingual later, a Plai-wide change); the
stage planner (Gate 5).

* * *

*Changelog*
- v0.1 — 2026-10-07 — initial draft, from starting prompt v0.7
  (OI-P2, P4–P8, P13 first half) and Plai at mapservice
  `b9edde4`; multiple selects and empty numbers read at
  Digitizer 3.0.0-RC3 `aaec85e`.
