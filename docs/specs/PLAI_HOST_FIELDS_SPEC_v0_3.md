---
title: "PLAI_HOST_FIELDS_SPEC_v0_3"
subtitle: "What a Plai point carries for Trans-Carpathian Pathways"
author: "Michel Garand"
date: "October 2026"
version: "v0.3"
lang: "en"
license: "CC BY-SA 4.0"
project: "Trans-Carpathian Pathways"
status: "settled on Michel's word, October 7; ready to build as plai/003; nothing built"
---

*A specification for one Plai migration in `ubec_mapservice`,
proposed as `db/instances/plai/003_host_fields.sql`, with the
scheme, view and proof changes that go with it. It is not the
migration. It is built there, in that repository's own way and
on Michel's word for that change, and where this document and
the mapservice prompt disagree about the stack, the mapservice
prompt is right. Read against mapservice `b9edde4` (prompt
v0.66): Plai's step A (`plai/001`, the entry fields) and step B
(`plai/002`, one photo) built and running on the host. The rules
that tree imposes on this migration are in
`docs/reviews/UBEC_MAPSERVICE_STATE_REVIEW_v0_1.md` §4; its nine
findings against v0.2 are applied here.*

* * *

## 1. What It Rests On

Every column below traces to one of these. Where a line in this
document is Claude's proposal rather than a decision, it says so.

| Item   | Michel's word, October 7, 2026                            |
|--------|-----------------------------------------------------------|
| OI-P2  | Pathways is a view of Plai; its fields come by Plai migration |
| OI-P4  | Each host has their own account and owns their row        |
| OI-P5  | `viewpoint` becomes a location type                       |
| OI-P6  | One point with a list of offers; season, capacity, languages, reach |
| OI-P7  | A home is published at the point entered                  |
| OI-P8  | Four forms of payment: fixed, suggested, work, `ubec-pay` |
| OI-P13 | The host chooses the forms, per offer (first half only)   |
| Q1     | Naming a form of payment for an offer is optional          |
| Q2     | Twelve languages: the eight, and Czech, Rusyn, Romani, Russian |
| Q3     | No new consent pair; the host fields are public once published |
| Q5     | No amount on the map; the Curator holds it for the pilot    |
| Q6     | An empty season reads "ask the Curator", not "all year"     |
| Q7     | `category` stays, as what the place mainly is; `offers` is the host's list |
| Q8     | The reach column is named `reach`, not `access`            |
| Q4     | Hosts are a style on the entry layer, not a second layer    |

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
(OI-P6). It stands beside Plai's `category`, not in place of it
(Q7): `category` stays required and single, "what this place
mainly is" — a farm's category may be produce while it also
offers a bed and a meal; `offers` is the host's list and nothing
else reads it. The entrant's form labels the two apart (§7).

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
(OI-P6, Q2). Twelve, each labelled in English with its own name
beside it:

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
| `cs` | Czech — čeština           | 90      |
| `rue`| Rusyn — русиньскый        | 100     |
| `rom`| Romani — romani čhib      | 110     |
| `ru` | Russian — русский         | 120     |

The codes are ISO 639-1 where a two-letter code exists, and
ISO 639-3 otherwise (`rue`, `rom`), so a later row is
unambiguous.

**`instance.entry_reach`** — how the place is reached (OI-P6; Q8:
`reach`, since `access` already names who may open an instance in
`instance.meta` and in `instance.py`).

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
| `reach`             | `text`     | codes of `entry_reach`, comma-joined          |
| `capacity_lodging`  | `smallint` | beds                                          |
| `capacity_meal`     | `smallint` | people at one meal                            |
| `capacity_guiding`  | `smallint` | people on one walk                            |
| `capacity_workshop` | `smallint` | people at one workshop                        |
| `pay_lodging`       | `text`     | codes of `entry_payment`, comma-joined; optional (Q1) |
| `pay_meal`          | `text`     | as above, for a meal                          |
| `pay_guiding`       | `text`     | as above, for guidance                        |
| `pay_workshop`      | `text`     | as above, for a workshop                      |

Capacity and payment are per offer because OI-P13 put the choice
of payment with the host per offer, and a bed count means nothing
for a walk. Four fixed offers make four pairs of columns rather
than a child table: the Digitizer edits one row per point and has
no form for rows beneath it.

None of the twelve begins `show_` or `consent_`: template 008 and
the tools read those prefixes as the consent convention, and
`verify` would take any other column so named as a gate.

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
   `reach`.
5. **A host is a place with offers.** Nothing else ties an offer
   to a category or a type: a farm, a guesthouse and a shepherd's
   hut can all offer a bed.

Naming a form of payment for a listed offer is optional —
Michel's word, October 7 (Q1). An offer with none is saved; its
terms are then the Curator's to give, like day-to-day
availability. (Proposed and not taken: refusing an offer without
a form of payment.) The label "ubec-pay or a community currency"
names a form the host accepts, not a system that exists in either
tree; nothing here depends on one.

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

**No new consent pair** — Michel's word, October 7 (Q3), as
proposed, traced to the step A rule that a place's descriptive
fields (name, types, category, offering) are public once the
entry is published, and to OI-P7, which leaves the location as
entered. Offers, season, capacity,
payment forms, languages and reach describe the place and its
terms, not the person; the host chooses to enter them, and the
curator chooses whether the entry is published at all. The
contact fields and the photo stay gated as they are. Should any
of these need gating later, template 008's `consent_C`/`show_C`
convention takes it with no new mechanism.

No amount is shown for a fixed or a suggested contribution —
Michel's word, October 7 (Q5): the form of payment is on the
map, the figure stays with the Curator for the pilot. No amount
or currency column is specified.

An empty season reads "ask the Curator" — Michel's word,
October 7 (Q6): the view gives null, the click prints nothing,
and nothing on the map says "all year" unless the host chose all
twelve months.

**The published view** `instance.entry_public` grows, at its
end, after `image_html`:

| View column         | From                                         |
|---------------------|----------------------------------------------|
| `offers`            | labels, in ordinal order, joined by ` · `     |
| `season`            | labels, joined by ` · `                       |
| `languages`         | labels, joined by ` · `                       |
| `reach`             | labels, joined by ` · `                       |
| `capacity_lodging` … `capacity_workshop` | the numbers          |
| `pay_lodging` … `pay_workshop` | labels, joined by ` · `        |
| `is_host`           | `offers IS NOT NULL`                          |

Labels are resolved in the view, from the list tables, so the
click, every export (`backup.py` reads the view) and any later
Pathways map read one place. `is_host` is the one thing a
Pathways map filters on (§6).

**The click** (`instance.meta`): `entry_info_fields` and
`entry_info_labels` gain the new view columns but `is_host`,
labelled "Offers", "Season", "Languages", "Reach", "Beds",
"At a meal", "On a walk", "At a workshop", "Terms — overnight",
"Terms — meal", "Terms — guidance", "Terms — workshop". An empty
value prints nothing, as today.

No label, option label or probe value above contains `owner`,
`state`, `geom`, `source_id`, `created_at`, `updated_at`,
`withdrawn_at`, `data_consent`, `consent_` or `show_`:
`leak_pass.py` judges a click by substring, and any such string
in a response is a failed check. Every label here was run against
that list (review §5, F-6); a label added later is run against it
too.

* * *

## 6. The Pathways Map

OI-P2: a Pathways map is a backend copy of Plai with its own
audience, not a second instance. Michel's word, October 7 (Q4),
on the review's recommendation: hosts are a **style on the one
entry layer**, not a second layer. `is_host` joins the entry
layer's `SELECT` in the mapfile — not its whitelist, so the click
never carries it — and a second `CLASS` with an `EXPRESSION` on
it draws a host with its own symbol and colour. The Pathways map
is then a backend copy of Plai showing every published place,
hosts marked; a copy can also uncheck the layers it does not
want.

What this avoids, recorded so the choice reads as one: a second
`hosts` layer would have meant both templates, the application's
key arithmetic in `instance.py`, `leak_pass.py`'s expected layer
set and whitelist, a feature-info template and a Mapbender WMS
source reload — the shape to take when a hosts-only map is
actually wanted, which the pilot does not need. A registry row
over a view is refused by design: `instance.layer` requires a
`source_id` under the licence guards and is for loaded files.

What it asks of Mapservice: the mapfile template's entry block
gains the column and the class, read from the instance — a hub
without `is_host` renders as today. The leak pass's rule that a
click on the entry layer serves the whitelist and nothing else
already covers it.

* * *

## 7. The Forms and the Proofs

**Entrant's scheme** (`mapbender/instances/plai/entries.yaml`):
the twelve columns join `fields`; "Category" keeps its place and
is titled "Category — what this place mainly is" (Q7); after
"Offering", a group headed "If you host travelers":

- `offers` — select, `multiple: true`, from `entry_offer`;
- per offer, `capacity_<offer>` — input `type: number`, min 1,
  max 99 — and `pay_<offer>` — select, `multiple: true`, from
  `entry_payment`, titled by the offer ("Overnight stay — how
  you are paid");
- `season`, `languages`, `reach` — select, `multiple: true`,
  from their tables.

The `__OPTIONS <table>__` line the renderer already expands
serves every list. A multiple select must have no empty option
(read at `FormRenderer.js`: select2's own rule).

**Curator's scheme** (`curation.yaml`): the same twelve in
`fields`, shown read-only, so the curator reads what they publish.
(A column absent from `fields` is neither loaded nor written
back, so leaving them out would also be safe; listing them is the
choice, for the reading.)

**Proofs**, in mapservice's own tools:
- `instance.meta entry_probe` gains values for every new column
  that `verify` and the leak pass insert, typed as the column is:
  an integer for a capacity, a comma-joined string for a list —
  `"offers": "lodging", "capacity_lodging": 2, "pay_lodging":
  "suggested", "season": "jun,jul,aug", "languages": "uk,en",
  "reach": "foot"`. None has a consent pair, so the leak pass's
  "no field without consent" check rightly passes over them.
- `verify` gains refusals: an unknown code in each list column,
  `foot` with `car`, a capacity of 0 and of 100; and the
  clearing: a capacity and a payment for an offer not listed,
  null after save; a re-save of a canonical row, unchanged.
- The leak pass: the new view columns appear only for published
  rows, in every format of the click; no change to its expected
  layer set, since §6 adds no layer.
- A browser save as a throwaway entrant with every list filled,
  and a curator's publish of it — the step A lesson that no tool
  here sees what the Digitizer actually writes.

**When the proofs can run — a hard constraint (review F-3).**
`verify` refuses an instance holding entries and the leak pass
skips its publication section when the entry table has rows, and
a throwaway instance under another name does not receive Plai's
own migrations. So `003` is built, proven locally on an instance
named `plai` in its host state, applied on the host and proven
there **before the first real host enters**. Gate 2 before Gate 3
is not an order of preference but the only order in which the
proofs exist. Later Plai migrations will meet the same wall once
hosts exist; a framework answer — a throwaway that carries another
instance's own migrations, or a bare restore of a Plai dump under
another name — is Mapservice's to decide, raised with `003`.

* * *

## 8. Open

Nothing in this specification. Settled October 7, on Michel's
word, and written into the sections above: Q1 payment optional
(§4); Q2 twelve languages (§2); Q3 no new consent pair (§5); Q4
hosts a style on the entry layer (§6); Q5 no amount on the map
(§5); Q6 an empty season reads "ask the Curator" (§5); Q7
`category` beside `offers` (§2); Q8 `reach` (§2).

Outside it, and before the first host rather than before `003`:
Mapservice's own condition on real accounts — backups with an
off-host copy (its review's F5) — which nothing in that tree yet
implements.

Not here, and why: how payment passes (OI-P13, second half —
it decides whether the project holds money, not what a point
carries); Ukrainian labels for every list (Plai's lists are
English for now, multilingual later, a Plai-wide change); the
stage planner (Gate 5).

* * *

*Changelog*
- v0.3 — 2026-10-07 — the state review's findings applied on
  Michel's word: Q7 `category` stays beside `offers`; Q8 `access`
  renamed `reach`; Q4 hosts a style on the entry layer, no second
  layer; the proofs' hard constraint (built and proven before the
  first host); typed probe values; the leak pass's substring rule
  on labels; the curator's scheme either way; `ubec-pay` names a
  form. Nothing open in the specification.
- v0.2 — 2026-10-07 — Q1, Q2, Q3, Q5 and Q6 settled on Michel's
  word: payment optional per offer; Czech, Rusyn, Romani and
  Russian join the language list; no new consent pair; no amount
  on the map; an empty season reads "ask the Curator". Only Q4,
  the mapservice side's, stays open.
- v0.1 — 2026-10-07 — initial draft, from starting prompt v0.7
  (OI-P2, P4–P8, P13 first half) and Plai at mapservice
  `b9edde4`; multiple selects and empty numbers read at
  Digitizer 3.0.0-RC3 `aaec85e`.
