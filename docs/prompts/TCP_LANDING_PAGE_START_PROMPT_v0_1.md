---
title: "TCP_LANDING_PAGE_START_PROMPT_v0_1"
subtitle: "Starting prompt — the landing page of tcp.ubec.network, ready for the public review"
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
reworks the landing page of `https://tcp.ubec.network/` so that it
can carry the project into its public review. It touches this
repository's `site/` and `build/build_site.py`; it touches nothing
in `ubec_mapservice` and no data on Plai.*

* * *

## 0. What this conversation is for

The site at `https://tcp.ubec.network/` has stood since October 9,
2026: one landing page in English and Ukrainian with the vision,
the mission, the regenerative test, "Where we are", and three
links out — Plai, the field writing, and the stewardship address.
It was opened by `docs/prompts/TCP_WEB_PRESENCE_START_PROMPT_v0_2`,
whose Gates A to D are closed; its record is `site/README.md`.

Since then the project has moved, and the page has not:

- **The drafts go out for public review.** The white paper, the
  proposal, the co-creator agreement and the project overview were
  stress-tested on October 10
  (`docs/reviews/PUBLIC_DRAFTS_STRESS_TESTS_v0_1.md`) and
  corrected. The documents themselves now say that "the documents
  published for review are on the project's site". Today they are
  not: the page carries no document at all.
- **The record is public** (Michel's word, October 11, D-3): the
  repository `ubeccommon/trans_carpathian_pathways` is the
  project's record, and the white paper says so. The page does not
  link to it, and the build's check allows links out only to
  `mapservice.ubec.network` and `pilgrims.ubec.network`.
- **The documents promise the site things.** The agreement (§7)
  and the proposal (Safety) say that the border-zone rules are
  given in writing by the Curator to every pilgrim who comes
  through the Curator, "and the project publishes them for anyone
  who comes directly". Nothing publishes them yet. The agreement
  and the proposal also tell people how to recognise the project:
  nobody from it asks for money in advance, a password or a
  passport, and it writes only from `stewardship@ubec.network`. A
  public page is where a pilgrim, a host or a stranger checks that.
- **The page is behind its own sources.** Its footer says "Drawn
  from the white paper v0.3 and the proposal v0.2"; they are now
  v0.9 and v0.7. "Where we are" says no Curator is named, which
  the decisions call the project lead for now (D-5, open), and
  says nothing of the test of the concept, which runs with the
  public review (D-4, decided October 11).
- **The name of whoever walks** is now the Pilgrim of the Plai —
  *прочанин плаю* (October 10). The page uses it; it does not yet
  say what the plai is.

This conversation makes the landing page the front door of the
public review: what the project is, where it stands, the drafts to
read and how to answer them, how to recognise the project, the
border rules for those who come directly, and where the record
is — without becoming a directory, a booking page or a form.

Not in scope: Plai's look and the map; any page that names,
pictures, locates or links to a host; any form; the Ghost blog;
any change in `ubec_mapservice`.

## 1. Load order — before any work

1. Attach `ubeccommon/trans_carpathian_pathways` with **push**
   access and clone it. `ubec_mapservice` is not needed; read it
   only if a question about the host comes up, and never write it
   from this conversation.
2. Read, in this tree, the latest
   `docs/TRANS_CARPATHIAN_PATHWAYS_CLAUDE_PROMPT` §1, §2 (the
   paragraphs headed "The site", "The name for whoever walks",
   "The drafts for public review, stress-tested" and "Three of
   the review's decisions"), §7 and §9.
3. Read `site/README.md` whole, `site/content/index_en.md` and
   `index_uk.md`, `site/static/style.css`,
   `site/nginx/tcp.ubec.network` (its Content-Security-Policy) and
   `build/build_site.py` (what it builds and what it refuses).
4. Read `docs/reviews/PUBLIC_DRAFTS_STRESS_TESTS_v0_1.md` §1 and
   §5, and the hostile reader's findings in §3: the page is the
   most public thing the project has.
5. Read the sources the page draws from, at their current
   versions: the white paper's summary, §4.3, §10 and §11; the
   proposal's summary, Safety and "How to take part"; the
   agreement's §3, §5, §7 and the pilgrim's part; the project
   overview. Find their files by name in `docs/`, latest version.
6. Check, with the GitHub API, whether the repository is public
   yet. Michel's word is that it is; the switch on GitHub is his.
   The page links to it only once it answers publicly.
7. Only then begin, with Gate A.

## 2. What is known already, and binds the page

From `site/README.md` and Michel's word, already given:

- **One static page in two languages,** built by
  `python3 build/build_site.py` from `site/content/` and
  `site/static/` into `site/dist/` (untracked), deployed by
  `rsync` to `/var/www/tcp.ubec.network` on ubec-common, verified
  from outside. No script, no inline style, no cookie, nothing
  loaded from another server; the vhost's Content-Security-Policy
  refuses anything else and the build refuses a page that tries.
- **WCAG 2.2 AA and BCP 47** (October 9): the build checks
  language tags, headings, `alt`, link names, the title and every
  colour pair in its `CONTRAST` table; a person checks keyboard,
  screen reader, zoom, text spacing and the text over the picture.
- **The marks and the fonts.** The UBEC mark for the site; the
  Plai emblem only beside the link to Plai. Inter and Lora, served
  from the site. No Google Fonts.
- **The picture.** Michel's "Warm wind on the path" (day 70) heads
  the page, the name inside its frame. Its licence is not yet
  stated, so the footer's CC BY-SA line names the text and the
  marks only.
- **The palette** of the PDFs: terracotta, ochre, night blue, two
  greens, cream, ink.
- **Every text on the page is drawn from a document in `docs/`**
  and names its version; the site is never a second source of
  truth. When a source changes, the page follows and is rebuilt.

## 3. What the public review asks of the page

From the stress tests of October 9 and 10, binding here:

- **No host, ever.** The page never names, pictures, locates or
  links to a host, and does not link to a host's point on Plai.
- **The stage, honestly.** No promise of income to a host or of a
  journey to a pilgrim. The map is built; the network is not yet.
  Gate 3 opens after off-host backups and the data-protection
  read.
- **How to recognise the project**, in the agreement's words: it
  writes only from `stewardship@ubec.network`; nobody from it asks
  for money in advance, a deposit, a password, or a passport or a
  copy of it; a pilgrim pays the host, as agreed.
- **Nothing operational.** The page says nothing about the server,
  its users, its paths, the backup plan or who holds which key.
  "The service depends on one person, and no deputy is yet named"
  is as far as it goes, and only if Michel wants it there.
- **The border rules,** if the page carries them, as the white
  paper §10.2 states them, with its sources and date, and the line
  that it is not legal advice; never a route, a stage or a village
  inside the strip.
- **The Ukrainian has not been read in the corridor** (D-2, open).
  Until it has, the Ukrainian page says so, in one line.
- **Attribution.** Claims about named third parties appear on the
  page only as the white paper now attributes them.

## 4. Gates

Gate by gate; a gate opens on Michel's word. Claude proposes,
Michel decides, and nothing of Claude's is recorded as decided.

- **Gate A — the content.** An inventory of what the page holds
  today against §0 and §3, and a proposed outline for the reworked
  page, section by section, each with its source document and
  version. The decisions in §5 put to Michel in one list. Output:
  the outline and his answers, recorded in `site/README.md`.
- **Gate B — the text and the look.** The page's text in English,
  then Ukrainian, drawn from the sources; at most two directions
  for any change to the layout, as built pages in the tree Michel
  can open at phone and desktop width. The look stays the one the
  site has unless he asks otherwise.
- **Gate C — built in the tree.** `site/content/` and, where
  needed, `site/static/` and `build/build_site.py`: the documents
  for review copied into `site/dist/` from `docs/` by the build,
  so that the PDFs on the site are always the committed ones; the
  build's link allowlist widened for `github.com` only if the
  repository is public; the build's checks passing; every new
  colour pair in `CONTRAST`. README, the page's versions and
  changelogs, the starting prompt bumped; one commit.
- **Gate D — on the host.** Michel deploys from schiff and
  verifies; he looks on his phone and his computer; the person's
  checks of `site/README.md` run again for what changed. Closes on
  his "looks good".

## 5. Open — for Michel, at Gate A

- **Which documents go on the page for review**, and in which
  form: the PDFs only, or the PDFs and a page each. The four the
  review named — white paper, proposal, agreement, overview — and
  whether the reasoning and the open-data specification join them
  after the light edit the review asked for.
- **How the review is answered:** by email to the stewardship
  address, by issues on the public repository, or both; and until
  when, if a date.
- **The record:** a link to the repository on the page, once it is
  public, and how it is labelled.
- **The border rules:** on the landing page, on a page of their
  own, or in a document linked from the page.
- **"How to recognise the project":** on the landing page or
  beside the contact line.
- **"Where we are"** in its new form: the test of the concept with
  the review (D-4); the first Curator (D-5, open — the page can
  stay silent on it until he decides).
- **The Pilgrim of the Plai:** whether the page says, in a line,
  what the plai is.
- **Still open from the review, and touching the page:** the
  Ukrainian name (D-1); the reading in the corridor, the byline
  with Zhyva Khata, a Ukrainian-speaking contact (D-2); the backups
  line (D-6). The page waits on these or says they are open.
- **The picture's licence,** so the footer can name it.
- **More than one page:** whether the site stays one page or gains
  a page for the documents.

## 6. Working rules

- Python for any tool; the whole site reproducible from the tree
  by one command; nothing that lives only on the server; no
  secrets and no access details in the tree.
- No script, no cookie, no third-party request, no form.
- Both languages changed together, each file's `version` and
  `changelog` bumped.
- Pull before any edit; one current version of each document;
  commits from a pulled tree.
- At the end of each working session: what was pushed, and the
  commands Michel runs, with the real paths —
  on schiff, as `farmer`:

  ```bash
  cd /home/farmer/projects/plai && git pull --ff-only
  python3 build/build_site.py deploy ubec@ubec-common /var/www/tcp.ubec.network
  python3 build/build_site.py verify https://tcp.ubec.network
  ```

  A change to `site/nginx/tcp.ubec.network` is installed on
  ubec-common by hand, as `site/README.md` step 4 says; a pull
  does not install it.

* * *

*Changelog*
- v0.1 — 2026-10-11 — initial, on Michel's word: the landing page
  readied for the public review, after the stress tests of October
  10 and the decisions of October 11 (the record public, the test
  with the review, no ratings without consent).
