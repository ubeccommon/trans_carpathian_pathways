---
title: "TCP_DOCUMENTATION_START_PROMPT_v0_1"
subtitle: "Starting prompt — the project's documentation as one set: the landing page, the white paper and the user guide"
author: "Michel Garand"
date: "October 2026"
version: "v0.1"
lang: "en"
license: "CC BY-SA 4.0"
project: "Trans-Carpathian Pathways"
status: "to paste as the first message of a new conversation"
---

*Paste everything below the line as the first message of a new
conversation in the Claude Project "Trans Carpathian Pathway". It
brings the project's documentation into one set, from the landing
page of `https://tcp.ubec.network/` through the white paper to the
user guide of Plai. It writes the Pathways tree
(`ubeccommon/trans_carpathian_pathways`); it reads the map service
(`ubeccommon/ubec_mapservice`) and never writes it.*

* * *

## 0. What this conversation is for

The documents were written one by one, each in its own
conversation: the site on October 9, the drafts for public review
stress-tested on October 10, the German and Polish translations on
October 11, the user manual through October 10. Since then the map
service has moved past them. On October 11 and 12 the pathway
planner was built into Plai's Pathways application
(`ubec_plai_hub_tcp`) and closed on the host on Michel's "looks
good":

- anyone plans a way from a start to an end, by name or by
  coordinates, and sees the route, its band and the places within
  reach;
- a visitor keeps a link and a download, and nothing is stored;
- a steward or the Curator names and saves it as a **stretch**,
  opens it again, edits it on the map, routes it again, sees its
  history and restores a version;
- stretches are put in walking order as a **corridor**;
- only the Curator publishes, and a published stretch or corridor
  is never changed in place: its saver's changes go into a draft
  of it.

None of this is in the user manual (v0.8 covers places only). The
landing page's "Where we are" still says "the map is built; the
network is not yet" and says nothing of the planner. The white
paper names the planner twice.

There is also a drift in the record itself. The latest prompt
(v0.65), decisions (v0.8), reasoning (v0.4) and planner spec (v0.4)
are on the branch `stage-planner-route`, and `main` still has
prompt v0.61, decisions v0.4 and reasoning v0.3. The site is built
from `main`.

This conversation makes the documentation one set that a reader
can follow from the front door inward:

1. **The landing page:** what the project is, where it stands
   today, the documents to read, how to recognise the project, how
   to answer the review. It is the most public thing the project
   has.
2. **The white paper:** the case, revised where the work has moved
   it, on Michel's word only (SP-6).
3. **The user guide:** how to use Plai, for each kind of reader —
   a visitor, a host, a steward, the Curator — places, the
   planner, stretches and corridors, each step checked against the
   map service as it is.

The overview, the proposal and the co-creator agreement are in the
set too: they are read for consistency, and are changed only where
Michel says so.

Not in scope: any change to the map service or its data; Plai's
screens (a wording on a screen that should change is handed back
as a note); the Ghost blog and the field writing; any page that
names, pictures, locates or links to a host.

## 1. Load order — before any work

1. Attach `ubeccommon/trans_carpathian_pathways` with **push**
   access, and `ubeccommon/ubec_mapservice` with **read** access.
   Clone both. In the Pathways tree, fetch both `main` and
   `stage-planner-route`, and say what each holds that the other
   does not. Nothing is written before Gate A settles which branch
   the work is done on.
2. In the Pathways tree, read the latest
   `docs/TRANS_CARPATHIAN_PATHWAYS_CLAUDE_PROMPT` (on the branch,
   v0.65): §1, §2, §7 and §9 whole, and every paragraph on the
   site, the name of whoever walks, the drafts for public review
   and the planner. Then read `docs/DECISIONS_CHECKLIST` (latest)
   and `docs/TRANS_CARPATHIAN_PATHWAYS_REASONING` (latest).
3. Read the site's record and how it is built:
   - `site/README.md` whole (v0.18): the menu, the documents'
     pages, the four languages, the accessibility checks, the
     deploy;
   - `site/content/` (the landing pages in four languages) and
     `site/static/style.css`;
   - `build/build_site.py`: what it builds, copies and refuses;
   - `docs/prompts/TCP_LANDING_PAGE_START_PROMPT_v0_1.md`: its
     Gate A questions are still unanswered (site README, status
     line), and this conversation takes them over.
4. Read the review that binds every public page:
   `docs/reviews/PUBLIC_DRAFTS_STRESS_TESTS_v0_1.md` whole, and
   §5 of `docs/reviews/TRANS_CARPATHIAN_PATHWAYS_STRESS_TESTS_v0_1.md`.
5. Read the documents of the set at their current versions, in
   English, with their Ukrainian beside them:
   - the white paper (v0.9) and `build/build_whitepaper.py`;
   - the user manual (`docs/manual/`, v0.8) and
     `build/build_manual.py`;
   - the overview (v0.5), the proposal (v0.7), the co-creator
     agreement (v0.7) and the implementation plan (v0.3);
   - `docs/translations/GLOSSARY_DE_PL_v0_1.md`, for the German
     and Polish translations of the overview, the proposal and
     the white paper.
6. Read the planner as the record describes it: on the branch,
   `docs/specs/PATHWAYS_STAGE_PLANNER_SPEC_v0_4.md` (§2, §3a, §3b,
   §4, §7) and `tools/README.md`.
7. Read the map service as it stands, for the user guide. Read
   only, at its current `main`:
   - `README.md` §8: the planner, stretches and corridors;
   - `stack/planner/static/planner.js`: the "Plan a way" panel;
     its header changelog lists what it does, version by version;
   - `mapbender/instances/plai/pathways.yaml`: the schemes "My
     stretches", "My corridors" and the Curator's lists, their
     labels and help texts, exactly as the screen shows them;
   - the headers of `db/instances/plai/008_stretches.sql`,
     `009_corridors.sql` and `010_published_edits.sql`: what is
     saved, who may do what, what is never stored;
   - the latest `docs/UBEC_MAPSERVICE_CLAUDE_PROMPT`, its last
     paragraphs: what was proven on the host, and when.
8. Check, with the GitHub API, whether the Pathways repository is
   public. Michel's word is that it is (D-3); the switch on GitHub
   is his. The site links to it only once it answers publicly.
9. Only then begin, with Gate A.

## 2. What is known already

- **One record.** The Pathways repository is the project's record
  (D-3). Every text on the site is drawn from a document in
  `docs/`, and the site names its version; the site is never a
  second source of truth. One current version of each document.
- **The site** is a static build, `python3 build/build_site.py`,
  from `site/content/`, `site/static/` and `docs/` into
  `site/dist/`. It has a landing page in English, Ukrainian,
  German and Polish, a menu (About, Overview, Proposal, White
  paper, Co-creator agreement, Plai, Field writing), and a page and
  PDF for each document. It has no script, no cookie, no form and
  nothing from another server, and its Content-Security-Policy
  refuses them. It is checked against WCAG 2.2 AA and BCP 47 by the
  build and by a person. Links to the map open in a new tab. The
  field writing is at `soilandpeace.ubec.network`.
- **Languages.** English first; Ukrainian beside it for every
  public document. German and Polish are Claude's translations of
  the overview, the proposal and the white paper. Each says, on the
  page and on the PDF cover, that nobody whose language it is has
  read it yet. The Ukrainian has not been read in the corridor
  either (D-2, open), and the pages say so.
- **The name for whoever walks** is the Pilgrim of the Plai —
  *прочанин плаю* (October 10). Screen labels on Plai are quoted
  as they stand.
- **The public documents are revised only when Michel says so**
  (SP-6): the white paper, the proposal, the plan and the module
  map. Claude proposes the change, with its reason; Michel decides
  each one.
- **The user manual** (v0.8, English and Ukrainian, one PDF of the
  two) explains accounts, the map page, entering a place, the form
  field by field, what happens to a place, what the public sees,
  the Curator's queue, and what to do when something goes wrong.
  Its screenshots are Michel's, cropped and without metadata.
- **The planner on Plai, as built.** What follows is the summary;
  the user guide states only what the map service's tree and
  Michel's screens show.
  - *Plan a way:* From and To are typed as a name, which brings up
    a list of places, or as coordinates, or picked on the map. Via
    and avoid points, the party and the month can be added.
  - *The answer:* the route and its band are drawn on the map, and
    beside them the places within reach and what the planner
    doubts. A public answer names a host by name and detour time
    only (SP-3).
  - *A visitor* keeps a link and a download; nothing is stored.
  - *A steward or the Curator* saves the way as a stretch with a
    name and a note. "My saved ways" lists their stretches and
    corridors, with buttons to open, change, send to the Curator,
    withdraw or copy each one.
  - *In "My stretches"* the line is edited by hand:
    - a point snaps to another line only within about 3 m;
    - a click on a vertex, or Delete or Backspace with the pointer
      on it, removes the vertex;
    - Escape undoes the last change;
    - pieces drawn by hand become known ways, which routing again
      follows.

    Every save is a version, and a version can be restored.
  - *Make a corridor:* stretches in walking order, one's own or
    published ones. A gap of more than 50 m is said, never joined.
    The corridor gets a name and is saved as a draft.
  - *Publishing:* only the Curator publishes. A stretch is
    published once it has a route; a corridor once every stretch
    in it is published. A published one is changed through a draft
    of it. Withdrawal takes it off the public map at once, and out
    of every published corridor.

## 3. What binds every document in the set

From the stress tests and the decisions, binding here:

- **No host, ever,** on the site or in a public document: never
  named, pictured, located or linked to, including a host's point
  on Plai. A host's own place in the user guide is described as
  the host's, never shown.
- **The stage, honestly.** No promise of income to a host or of a
  journey to a pilgrim. Say what is built and what is not yet.
- **How to recognise the project,** in the agreement's words: it
  writes only from `stewardship@ubec.network`; nobody from it asks
  for money in advance, a deposit, a password, or a passport or a
  copy of it.
- **Nothing operational** in a public document: no server details,
  no users, no paths, no backup plan, no keys.
- **The border rules** only as the white paper §10.2 states them,
  with their sources and date and the line that this is not legal
  advice; never a route, a stage or a village inside the strip.
- **Attribution.** Claims about named third parties only as the
  white paper attributes them.
- **Consistency.** One fact, one wording across the set. Where two
  documents disagree, the disagreement is listed for Michel, not
  quietly resolved.

## 4. Handed back from the map service — to record here

The map-service conversation of October 11 to 13 could not write
the Pathways tree. What it built and decided, and the Pathways
record should now carry, each for Michel's word before it is
written:

- **Spec §2:** a steward saves a corridor as a draft, and only the
  Curator publishes it (Michel's word, October 12). This changes
  §2, where only the Curator joined stretches into a corridor.
- **Spec §7:** a corridor is published only once every stretch in
  it is published.
- **Editing a published stretch or corridor** puts the changes in
  its saver's draft of it, and the published one stays public until
  the Curator publishes the draft (map service `plai/010`, October
  12).
- **A visitor** keeps a link and a download, and nothing is stored
  for them (Michel's word, October 12).
- **The engine** runs in the map service at Pathways commit
  `99ba6d8`, fetched and checked by hash at build. A change to the
  engine reaches Plai only when that pin is moved.
- **A finding for the engine:** beside a rich place, the engine
  prefers the footpath over a known way drawn by hand. The weight
  given to a footpath at its richest (`Q_MAX` 0.9) and to a known
  way (`KNOWN_WEIGHT` 0.2) explain it. Whether a steward's
  hand-drawn way should win there is Michel's call.
- **To be confirmed against SP-3:** a published stretch that
  begins or ends at a host's door shows on the public map where
  that host is. Whether stretches may end at a host, or end short
  of it, is open.

## 5. Gates

Gate by gate; a gate opens on Michel's word. Claude proposes,
Michel decides, and nothing of Claude's is recorded as decided.

- **Gate A — the set as it stands.** Read as §1 says, then report
  to Michel:
  - every document of the set: its versions per language, where it
    lives (tree, page, PDF), its reader, and its sources;
  - the drift: each place where a document no longer says what is
    true, or where two documents disagree, with the line and the
    fact;
  - the branches: what `stage-planner-route` holds that `main`
    lacks, and a proposal for one current version of each
    document;
  - a proposed shape for the set: which reader enters where, and
    which document leads to which;
  - the user guide's outline: its readers, chapters and
    screenshots needed;
  - §6's questions, in one list.

  Output: the report, Michel's answers recorded in the latest
  prompt and in `site/README.md`, and this starting prompt
  committed in `docs/prompts/`. Nothing else is built before this.
- **Gate B — the landing page.** The landing page prompt's Gate A
  to C, taken over here: the outline section by section with its
  sources, then the text in English, then in Ukrainian, then German
  and Polish following. "Where we are" says what is built today.
  Built in the tree, checks passing.
- **Gate C — the white paper.** Each proposed change listed with
  its reason and the section it touches, for Michel's word one by
  one. Then the English, then the Ukrainian, then the German and
  Polish following, the PDFs rebuilt and the page's version line
  bumped. The overview and the proposal follow where a change
  reaches them, again on his word.
- **Gate D — the user guide.** The manual extended, or split by
  reader, as Gate A decides: places as now, then the planner,
  stretches, editing, history, corridors and publishing. Each step
  is checked against the map service's tree at its current commit.
  The screenshots are listed for Michel to take; until he has, a
  figure says so. English first, then Ukrainian, one PDF of the
  two, and a page on the site if Gate A says so.
- **Gate E — on the host.** Michel pulls on schiff, deploys,
  verifies from outside, and looks on his phone and computer; the
  person's accessibility checks of `site/README.md` run again for
  what changed. Closes on his "looks good".

Gates B, C and D may run in the order Michel chooses; each closes
with one commit, the README and prompt bumped.

## 6. Open — for Michel, at Gate A

- **The branches:** merge `stage-planner-route` into `main` first,
  so that the latest prompt, decisions, reasoning and spec are one
  current version on the branch the site is built from — or keep
  the planner's code off `main` and bring over only the documents.
- **The landing page prompt's open questions** (its §5): which
  documents for review and in which form; how the review is
  answered and until when; the link to the record; where the border
  rules stand; "how to recognise the project"; "Where we are"; the
  plai in a line; the picture's licence; one page or more.
- **The planner on the landing page:** whether and how the page
  points to "Plan a way" on Plai.
- **The white paper:** whether this round revises it, and which of
  §4's points it carries; whether a public document names the
  engine's numbers at all.
- **The user guide:**
  - one manual for all, or one per reader (visitor and pilgrim,
    host, steward, Curator);
  - its name ("Plai — User Manual" today);
  - whether it gains a page on the site beside the PDF;
  - whether German and Polish follow it.
- **The handed-back notes of §4:** each recorded as it stands, or
  changed first.
- **Still open from the review,** touching the whole set: the
  Ukrainian name (D-1); the reading in the corridor, the byline
  with Zhyva Khata, a Ukrainian-speaking contact (D-2); the backups
  line (D-6); the first Curator named (D-5).

## 7. Working rules

- Python for any tool. The whole site and every PDF reproducible
  from the tree by one command each; nothing that lives only on the
  server. No secrets and no access details in the tree.
- Pull before any edit; commits authored as Michel Garand, from a
  pulled tree. One current version of each document; a new version
  renames the file where the file carries its version.
- Every document changed in English and Ukrainian together, each
  file's `version` and `changelog` bumped; German and Polish follow
  the English, each still saying who has not read it.
- Every claim about Plai's screens checked against the map
  service's tree at its current commit and against Michel's
  screenshots before it is written. The map service is never
  written from this conversation; a wording on a screen that
  should change is handed back as a note.
- The build's checks pass before every commit; WCAG 2.2 AA and BCP
  47 hold on every page.
- At the end of each working session, say what was pushed and give
  the commands Michel runs, with the real paths. On schiff, as
  `farmer`:

  ```bash
  cd /home/farmer/projects/plai && git pull --ff-only
  python3 build/build_site.py deploy ubec@ubec-common /var/www/tcp.ubec.network
  python3 build/build_site.py verify https://tcp.ubec.network
  ```

  ubec-common is reached from schiff with `ssh ubec-common`. A
  change to `site/nginx/tcp.ubec.network` is installed on
  ubec-common by hand, as `site/README.md` says; a pull does not
  install it.

* * *

*Changelog*
- v0.1 — 2026-10-13 — initial, on Michel's word: one conversation
  for the documentation as a set, from the landing page to the
  white paper to the user guide. It takes over the landing page
  prompt v0.1's open Gate A, and carries the notes handed back from
  the map service's planner work (October 11 to 13: stretches,
  corridors, editing, publishing, `plai/010`).