---
title: "UBEC_MAPSERVICE_STATE_REVIEW_v0_1"
subtitle: "The mapservice tree and Plai, read before any Pathways change"
author: "Michel Garand"
date: "October 2026"
version: "v0.1"
lang: "en"
license: "CC BY-SA 4.0"
project: "Trans-Carpathian Pathways"
status: "read-only review; nothing in ubec_mapservice was touched"
---

*What `ubeccommon/ubec_mapservice` holds at commit `b9edde4`
(October 7, 2026, prompt v0.66, README v0.32), what Plai is on
the host by that tree's own record, what binds a Plai migration,
and what the host-fields specification (`PLAI_HOST_FIELDS_SPEC`
v0.2) must change before `plai/003` is built. Michel's word,
October 7: a comprehensive review before any update or change.
Read from a fresh clone; the checker, `check_ubec_standard.py`,
run read-only and passing 7 of 7. No host was reached: every
host figure here is the prompt's own record.*

* * *

## 1. What Was Read

The whole of `docs/UBEC_MAPSERVICE_CLAUDE_PROMPT_v0_66.md` (§1 to
§9, the settings text, the changelog head); README v0.32 §8 to
§15; the project review v0.5's status table and F5, F12, F13,
F14; every file of `db/instance_template/` (001 to 008, 002 and
008 in full); `db/instances/plai/001` and `002` in full; Plai's
two Digitizer schemes v0.3; the application template v0.19 and
the mapfile template v0.16 at their entry fences; `instance.py`
v0.27 (header, `entry_info`, `instance_forms`,
`render_instance_files`, `apply_migrations`, `verify`'s probe),
`migrate.py` v0.6, `leak_pass.py` v1.13 (the expected layer set,
`NEVER_SERVED`, `publication_checks`), `backup.py` v0.7's role;
`stack/docker-compose.yml` v0.15 and `.env.example` v0.5 (keys
only); and, at the Digitizer's pinned tag 3.0.0-RC3 (`aaec85e`),
`FormRenderer.js`, `FormUtil.js`, `DataRepository.php`,
`TableMeta.php` and `Column.php`.

* * *

## 2. The Tree at b9edde4

Clean working tree, 130 commits, 128 authored as Michel Garand
and two on September 14 as "Claude (sandbox)". The last ten
commits are all October 7, from the entry surface's step A to
step B on the host. Versions, each from its own header:

| Part | Version | Note |
|------|---------|------|
| Starting prompt | v0.66 | step B on the host |
| README | v0.32 | §8 the photo, §15 open items |
| Framework migrations | 001 to 020 | 020 the style's last columns |
| Instance template | 001 to 008 | 008 the entry rules |
| Plai's own migrations | 001, 002 | fields; the photo |
| Plai's schemes | v0.3 | entries, curation |
| Application template | v0.19 | login button |
| Mapfile template | v0.16 | entry columns from the instance |
| `instance.py` | v0.27 | `entry_info_html`, uploads |
| `migrate.py` | v0.6 | `<name>/NNN` ledger prefix |
| `leak_pass.py` | v1.13 | the media route |
| `backup.py` | v0.7 | photos dumped with rows |
| `entry_images.py` | v0.2 | lock in `$UBEC_EXCHANGE` |
| `roles.py` | v0.7 | 74 checks on the host |
| `osm_base.py` | v1.0 | Organic Maps style |
| Compose | v0.15 | `media` service |
| Vhost | v0.4 | `/media/`, CSP on attachments |

The project review (`UBEC_MAPSERVICE_PROJECT_REVIEW_v0_5`) still
carries its September 20 status table. F12 (row ownership) and
half of F13 (an account deleted with its rows) were closed by
template 008 and `instance.py purge` on October 7; the review
document does not say so yet. Document drift, F16's own kind.

Still open there and bearing on Pathways: **F5**, no backup
routine and no off-host copy — the tree holds commands, not a
timer, and `backup.py` cannot dump Mapbender's own database, where
every account lives; **F13**'s second half, logs not short;
**F14**, images float with no pull routine. The prompt's own
condition for Plai — "backups before any real account: the
off-host copy goes to Michel's own computer during the test
phase, and he holds the decryption key" — has nothing in the tree
that implements it. Whether it exists in the operator's notes is
not visible from here.

* * *

## 3. Plai on the Host, by the Tree's Record

- Instance `plai`, title "Plai — Carpathian hub", extent the
  Outlook polygon's bounds, created October 4 as loaded; profile
  `hub` and precision `free` since October 7.
- Template 008 and `plai/001`, `plai/002` applied; `verify plai
  vt` 76 of 76; the leak pass through the public face 518 of 518,
  none skipped. The test places are purged: **the entry table is
  empty**.
- What a point carries: a name, one location type and one
  category from two lists of 18, an offering, contact name, email
  (required) and mobile, each contact field under a consent and
  show pair, a stored-data consent with its time, and one photo
  under its own pair, cleaned by a timer and served at
  `/media/plai/<id>.jpg` only where the published view shows it.
- The development original is **private** (root only). **No user
  copy of Plai exists**: `mapbender/exports/` holds the Greenbelt
  copy alone, and the prompt's rule is that what users see is a
  backend copy whose security tab grants view. Making it is the
  release step in README §8, and the pooler question is to be
  settled before that copy "goes wide".
- Accounts: made by the administrator in Mapbender's backend, in
  `PLAI_ENTRANT`, `PLAI_CURATOR` and `PLAI_ADMIN`, titles exact;
  Mapbender 5.0.0-RC2 requires a unique email on each. The tree
  records a throwaway entrant and curator used for Michel's look;
  whether they still exist is a backend fact. **No real account
  yet**, by the prompt's own condition.
- The base map: OpenStreetMap over nine countries by the Organic
  Maps style, names and search, the credits; 25 GB of 98 on
  `/data`; GetMap 0.45 to 1.17 s at every scale tried;
  capabilities 2.87 s; two render-role connections a request.
- The map page: a login link in the toolbar, inside the entry
  fence; after login a user lands on the application list.

* * *

## 4. What Binds a Plai Migration

Read from the tools and templates, not from recollection. Each
line is a rule `plai/003` must satisfy or a fact it rests on.

**The file and its ledger**
- `db/instances/plai/003_<name>.sql`, name `^\d{3}_[a-z0-9_]+\.sql$`,
  recorded as `plai/003_…` with its SHA-256. `001` and `002` are
  applied on the host and **must never be edited**: a changed
  hash stops every later run (`migrate.py`).
- One transaction; placeholders `__INSTANCE_ROLE__`,
  `__ENTRY_ROLE__`, `__CURATOR_ROLE__`, `__MAPSERVER_ROLE__`,
  never a role name. Every new table `OWNER TO __INSTANCE_ROLE__`.
- Applied by `instance.py migrate plai` (template first, then
  `db/instances/plai/`), followed by `render` and Mapbender's
  `cache:clear`. A throwaway instance under another name **does
  not** receive Plai's own migrations (`apply_migrations` keys
  them on the instance's name).

**The function and the view**
- `instance.entry_plai_normalize()` was replaced whole by `002`
  (`CREATE OR REPLACE`), carrying `001`'s lines; `003` replaces it
  whole again, carrying both. It fires before template 008's
  trigger by name order (`entry_a_plai_normalize` before
  `entry_before_write`), so what 008 compares is the normalised
  row.
- `instance.entry_public` likewise: `CREATE OR REPLACE VIEW` keeps
  the existing columns in their order and may only append.
  Template 002's six come first, then `001`'s six, then `002`'s
  two; `003`'s go after `image_html`.
- The render role reads the view and nothing of the table; the
  list tables need `GRANT SELECT` to the entry and curator roles
  (the form's `__OPTIONS` lines are read as the superuser at
  render, but the Digitizer's own reads are the roles').

**Template 008's conventions, which the tools read by name**
- `show_C` beside `consent_C` beside `C` is the consent pair;
  `verify` and the leak pass find the pairs by those prefixes, and
  008's trigger clears or refuses on them. So **no new column may
  begin `show_` or `consent_`** unless it is such a pair.
- A curator's save is put back to the old row for every key but
  `state` and `show_*`, over the whole row as JSON — new columns
  are covered with no change to 008.
- An entrant's save to a published row that changes any key but
  the states, dates, unit, precision and `consent_*` returns it to
  submitted, compared value by value. A list column must therefore
  be stored canonically (sorted, trimmed, deduplicated) or a
  re-save that reorders a list unpublishes the host.
- The Digitizer writes back every column named in a scheme's
  `fields`; a column there without an `UPDATE` grant fails the
  whole save. Every new column that either scheme lists needs its
  grant to that role.

**What the click and the leak pass require**
- `instance.meta entry_info_fields` names columns of
  `entry_public`, never `id` or `geom`; `render` exits on any
  other name. `entry_info_labels` is JSON; `entry_info_html` names
  columns ending `_html` printed unescaped.
- `leak_pass.py` judges a click by **substring**: no response may
  contain `owner`, `state`, `created_at`, `updated_at`,
  `withdrawn_at`, `source_id`, `geom`, `data_consent`, `consent_`
  or `show_`, case-insensitively. A label, an option label or a
  probe value carrying one of those strings ("estate", "homeowner")
  is a false leak. Every label in the specification was checked
  against the list; none carries one.
- The leak pass's publication section **inserts a probe row and
  skips when the entry table already holds rows**; `verify`
  refuses an instance holding entries unless `--force`. Both ran
  clean on Plai because it is empty.
- `entry_probe` (JSON in `instance.meta`) supplies the probe row's
  values for the instance's own `NOT NULL` columns; its values go
  through psycopg as typed Python values, so a `smallint` column
  takes an integer there.

**The forms**
- `__OPTIONS <table>__` expands only for tables named
  `entry_[a-z0-9_]+`, reading `code, label` ordered by
  `ordinal, code`, and exits if the table is empty. Labels are
  JSON-quoted with `ensure_ascii=False`, so Cyrillic and
  diacritics pass.
- At Digitizer 3.0.0-RC3: a select with `multiple: true` saves
  its choices joined by `,` (or `data-multiselect-separator`),
  null when none, and must carry no empty option; an empty string
  posted to a numeric nullable column is saved as null
  (`TableMeta::prepareUpdateData`, `Column::getSafeDefault`).
- An element's `roles:` names groups by title; a scheme's `roles:`
  is the Digitizer's own role string. Both stay as they are.

**The map and the application**
- The entry layer is one fenced block in each template, its
  columns from `entry_info_fields`. Application layer keys are
  computed in `render_instance_files` (`admin_key`, `ENTRY_KEY`,
  `first_level`), so a second entry-derived layer changes that
  arithmetic.
- Mapbender stores a WMS source's capabilities at first import
  (README §15): a new mapfile layer reaches an application only
  after `mapbender:wms:reload:url` or a re-import, and a user copy
  is a snapshot that must be made again.
- `leak_pass.py` expects exactly `admin_unit`, `entry`, the base
  map's names and the registry's layers; any other advertised
  layer fails "instance advertises only its known layers".

**The working rules of that tree**
- Commits authored as Michel Garand from the host's checkout;
  pull before work, push after; GitHub the only meeting point.
- `check_ubec_standard.py` PASS before any `.md` is presented;
  74-character lines; changelog in every file; one current version
  per document; the prompt and the README bumped with each change
  and the change recorded as Michel's word with its date.
- Long host runs in tmux; the vhost reinstalled after any commit
  touching `stack/nginx/`; `cache:clear` after every `render`.

* * *

## 5. The Specification Against the Tree

What `PLAI_HOST_FIELDS_SPEC_v0_2` gets right needs no list. What
it must change or decide before `003` is written:

- **F-1 — Category and offers overlap.** Plai's `category` is one
  code per point, `NOT NULL`, and its list already holds
  `lodging`, `meals`, `guiding`, `learning`, `crafts`. The
  specification adds `offers`, a list from a second table of
  four. A host with a bed and a meal then carries a category and
  an overlapping list, and nothing says which one the map, the
  click and a later Pathways filter read. Three ways out, for
  Michel's word (Q7): keep both, `category` as "what this place
  mainly is" and `offers` as the host's list; or make `offers`
  the host columns alone and leave `category` to non-hosts; or
  drop the new `entry_offer` table and derive `offers` from the
  existing categories, which forecloses "one point, several
  offers". The first is recommended; the specification must say
  it either way, and the entrant's form must label the two so a
  host is not asked the same thing twice.
- **F-2 — `access` names two things.** `instance.meta` already
  holds a key `access` (who may open the instance), and
  `instance.py access` is a command. A column `instance.entry.access`
  is legal and unambiguous to PostgreSQL, but every grep and every
  reader of the tools will meet both. Rename the column (Q8):
  `reach` or `access_by`; recommended `reach`.
- **F-3 — The proofs can only run while Plai is empty.** Verify
  refuses an instance with entries and the leak pass skips its
  publication section, and no throwaway can carry Plai's own
  migrations. So `003` must be built, proven locally on an
  instance named `plai`, applied on the host and proven there
  **before the first real host enters** — which fixes the order
  Gate 2 before Gate 3 as a hard constraint, not a preference.
  Every later Plai migration has the same problem once hosts
  exist; a framework answer (`create beta --like plai`, or
  `restore --bare` of a Plai dump under another name) is
  Mapservice's to decide and worth raising with `003`.
- **F-4 — Q4, the hosts layer, has three shapes**, each a
  different size of framework change:
  - (a) *A style, not a layer.* `is_host` joins the entry layer's
    SELECT (not its whitelist) and a second `CLASS` with an
    `EXPRESSION` on it draws hosts differently. No new layer, no
    key arithmetic, no leak-pass change, no WMS reload beyond the
    render. The Pathways map is then a backend copy of Plai
    showing every published place, hosts marked.
  - (b) *A second entry-derived layer*, `hosts`, over the same
    view with `WHERE is_host`, declared by an `instance.meta` key
    and rendered by `instance.py`: template changes in both files,
    key arithmetic, `leak_pass.py`'s expected set and whitelist, a
    feature-info template, a WMS source reload. A backend copy can
    then show hosts alone.
  - (c) *A registry row* in `instance.layer` over a view: refused
    by design — the registry requires a `source_id` under the
    licence guards and is for loaded files.
  Recommended for the pilot: (a), with (b) when a hosts-only map
  is actually wanted. Michel's word, on the mapservice side.
- **F-5 — The curator's scheme need not list the new columns.** A
  column absent from `fields` is neither loaded nor written back,
  so the curator can be shown the host fields read-only by listing
  them, or shown nothing by leaving them out; 008 keeps them
  either way. The specification lists them; either is right.
- **F-6 — Labels under the leak pass's substring rule.** Every
  list label and click label in the specification passes. The
  rule must be kept in mind for any label added in review, and
  for the Ukrainian labels when they come.
- **F-7 — `entry_probe` carries typed values.** The specification
  must state the probe JSON with an integer for a capacity and a
  comma-joined string for each list, and the leak pass's
  "no field without consent" check will skip them, rightly, since
  none has a pair.
- **F-8 — The payment table's label.** "ubec-pay or a community
  currency" is an option label; `ubec-pay` has no definition in
  either tree. Fine as a label; the specification should say it
  names a form, not a system that exists.
- **F-9 — Nothing in the specification touches 008, the template,
  `backup.py` or the media route.** Confirmed against each: 008
  covers new columns by shape; `backup.py` reads the view; the
  media route reads `image_file` only. `verify` and `leak_pass.py`
  need the refusal and clearing checks the specification lists,
  and `leak_pass.py` only changes if (b) is chosen.

* * *

## 6. Before Any Change — in Order

1. Michel's word on F-1 (Q7), F-2 (Q8) and F-4 (Q4); the
   specification bumped to v0.3 with them.
2. Michel's word that `plai/003` is the named change this
   conversation may make in `ubec_mapservice`, and push access
   attached; else the specification is handed to a mapservice
   conversation as it stands.
3. The mapservice condition on real accounts — backups with an
   off-host copy (F5) — confirmed by Michel from the operator's
   notes or scheduled, since Gate 3 waits on it regardless of
   `003`.
4. Then the build, in that tree's own order: `003` and the two
   schemes; `instance.py` only if (b); `verify` and `leak_pass.py`
   extended; proven locally on an instance named `plai` in its
   host state (template 008, `plai/001`, `plai/002`, precision
   free, profile hub); the prompt and README bumped; checker
   PASS; committed as Michel Garand after a pull; then on the
   host by Michel — migrate, render, `cache:clear`, `verify plai
   vt`, the leak pass through the public face — and his look in a
   browser as a throwaway entrant and curator, the step A lesson
   that no tool here sees what the Digitizer writes.

* * *

*Changelog*
- v0.1 — 2026-10-07 — initial, read at mapservice `b9edde4`
  (prompt v0.66, README v0.32) and Digitizer 3.0.0-RC3
  `aaec85e`; nine findings against host-fields spec v0.2.
