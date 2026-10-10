---
title: "TCP_WEB_PRESENCE_START_PROMPT_v0_2"
subtitle: "Starting prompt — the project's presence on the web at tcp.ubec.network"
author: "Michel Garand"
date: "October 2026"
version: "v0.2"
lang: "en"
license: "CC BY-SA 4.0"
project: "Trans-Carpathian Pathways"
status: "to paste as the first message of a new conversation"
---

*Paste everything below the line as the first message of a new
conversation in the Claude Project "Trans Carpathian Pathway". It
opens the project's own place on the web: a site at
`https://tcp.ubec.network/` that says what Trans-Carpathian
Pathways is, carries its documents, and tells people how to take
part. It touches this repository and, for the vhost,
`ubec_mapservice`; it touches no data on Plai.*

* * *

## 0. What this conversation is for

Trans-Carpathian Pathways has no address of its own on the web.
Its documents live in a private repository; its map, Plai, is a
Mapbender application at `https://mapservice.ubec.network/` whose
landing page is a list of applications; the agreement PDF is
served from there at `/ubec/agreement/` because the repository is
private; Michel's field writing is a Ghost blog at
`https://pilgrims.ubec.network/`. A funder, a partner initiative
in Romania, a hromada council or a journalist who hears of the
project has nowhere to send a browser.

This conversation builds that place: `https://tcp.ubec.network/`,
a small, bilingual, static site that says what the project is,
carries the proposal, the white paper, the co-creator agreement
and the manual as PDFs and as pages, names how to take part and
whom to write to, links to Plai and to the field writing, and is
honest about the stage the project is at. It is the public face of
the project; it is not a map, not a directory of hosts, not a
booking page, and not a blog.

Not in scope: Plai's look (the face prompt,
`docs/prompts/UBEC_MAPSERVICE_FACE_START_PROMPT`), the Ghost blog,
any page that lists or locates a host, any form that collects a
person's data, and any change to what Plai carries.

## 1. Load order — before any work

1. Attach `ubeccommon/trans_carpathian_pathways` with **push**
   access and `ubeccommon/ubec_mapservice` with **read** access
   (push only if Michel decides at Gate A that the vhost lives in
   the mapservice tree, and then only for that change). Clone
   both.
2. Read, in this tree, the latest
   `docs/TRANS_CARPATHIAN_PATHWAYS_CLAUDE_PROMPT` whole — §2 (what
   the project is and where its work lives), §7 (principles), §9
   (open items) — and the README.
3. Read the white paper,
   `docs/whitepaper/Trans-Carpathian_Pathways_White_Paper_EN.md`,
   in full: it is the site's source text. Read the proposal's
   summary and "How to take part", the agreement's §3 and §6
   (principles; the name and the marks), and the stress-test
   review
   `docs/reviews/TRANS_CARPATHIAN_PATHWAYS_STRESS_TESTS_v0_1.md`
   §1 and §5 — the site must not undo what the tests ask for (§3
   below).
4. Read `build/build_pdf.py` (the palette and the page styles),
   `build/diagrams.py` and `build/diagrams_whitepaper.py` (the
   drawing style, the fonts), and `docs/proposal/assets/` and
   `docs/whitepaper/assets/` (what pictures exist).
5. In the mapservice tree, read `stack/nginx/` and
   `stack/docker-compose.yml` (how `mapservice.ubec.network` is
   served and by what), README §10, and the prompt's §4 principles
   that bind anything on the host: reproducible from the tree,
   nothing living only on the server, no secrets, commits as
   Michel Garand from a pulled tree.
6. Only then begin, with Gate A.

## 2. What is known already

**The name.** `tcp.ubec.network` — Trans-Carpathian Pathways. The
three letters also name a network protocol; noted once here and
not a reason to change it unless Michel says so.

**What exists to put on it**, all CC BY-SA 4.0, all in this tree:
- The proposal, English and Ukrainian, one PDF (`docs/proposal/`).
- The white paper v0.3, English and Ukrainian, one PDF of 59
  pages, with three diagrams in both languages as SVG
  (`docs/whitepaper/`).
- The co-creator agreement v0.2, both languages, one PDF, a draft
  with seven items open (`docs/agreement/`).
- The user manual v0.3, both languages, one PDF, with screenshots
  of Plai (`docs/manual/`).
- The reasoning document and the two reviews, English only.
- The Plai emblem (`docs/proposal/assets/plai_emblem_mark.svg`,
  cropped to `logo.png`) and the network diagram and roadmap in
  both languages.

**The marks and the fonts — Michel's word, already given.** The
UBEC mark (the green ring, "UBEC" between two green rules) is used
for everything that is not a Plai application; the round Hutsul
Plai emblem is used only for Plai applications. Both are Michel's,
CC BY-SA 4.0. So the site carries the UBEC mark as its own, and
the Plai emblem only where it points at Plai. No Google Fonts:
every font open-source and served from the site itself. Inter and
Lora, which the PDFs use, are both under the SIL Open Font License
and can be served locally.

**The palette and the type** the PDFs already use, from Plai's
emblem and `build_pdf.py`: terracotta `#a2352a` and `#9a362b`,
ochre `#c98a2e`, night blue `#161a33`, two greens `#2a3f2a` and
`#3f5e39`, cream `#e8dcb8` and `#f1e6c6`, ink `#1b1410` and
`#1d2027`; Inter for text, Lora for titles. The site should read
as the fourth member of the set the proposal, the manual, the
agreement and the white paper already form.

**The host.** `mapservice.ubec.network` is served on ubec-common
by the nginx in `stack/nginx/` in front of the Mapbender container
(compose v0.15 at the last reading); `pilgrims.ubec.network` is
Ghost. Where DNS for `ubec.network` is managed, how TLS
certificates are issued there, and whether a static site should be
a third vhost on the same nginx or live elsewhere, are not in
either tree and are Gate A's first questions.

**What the project promises visitors already**, and the site
inherits: no advertising, no tracking of what visitors do, logs no
longer than abuse control needs (agreement §5). A static site with
no third-party request — no fonts, scripts, analytics, embeds or
maps loaded from anyone else's server — keeps that promise by
construction.

## 3. What the stress tests ask of the site

The three stress tests of October 9
(`docs/reviews/TRANS_CARPATHIAN_PATHWAYS_STRESS_TESTS_v0_1.md`)
bear on a public site directly, and the site must be built so that
it does not reopen what they closed or pre-empt what waits on
Michel's word:

- **The bypass (S-1).** Every safety promise assumes a pilgrim
  reaches a host through the Curator. The site therefore never
  lists, locates, pictures or links to a host. It says how a
  pilgrim reaches the Curator, and that is the only door. Whether
  host points on Plai are public or logged-in during the pilot is
  S-1, Michel's decision, not the site's.
- **Pathways™ (S-11, S-19).** The site is the first place the
  project can say who is and is not a partner, and record requests
  it declined. It carries the name and the mark; whether they
  become registered marks is A-1 and S-11, not the site's to
  decide, but the site states the licence on its documents (CC
  BY-SA) and the agreement's §6 line on the name.
- **What the project can show (test 1).** The site does not
  promise hosts an income or pilgrims a journey. It states the
  stage: Gates 0 and 2 closed, no host yet by name, the agreement
  a draft. A page that reads as an open service misleads the first
  person who writes in.
- **No form (test 2).** No contact form, newsletter or sign-up: a
  `mailto:` to `stewardship@ubec.network`, which the agreement
  names. A form is a dataset with no basis in the agreement's §5.
- **Copies (S-14).** Nothing on the site shows where anyone lives.
  Photographs, if any, show land, paths, craft and people who
  agreed, never an identifiable home; origin and licence recorded
  beside each, as the catalogue does for data.

## 4. Gates

Gate by gate; a gate opens on Michel's word. Claude proposes,
Michel decides, and nothing of Claude's is recorded as decided.

- **Gate A — what is there, and the decisions.** The host as it
  is: DNS, TLS, the nginx vhosts, where a static site would sit
  (Michel answers; Claude cannot reach the host). The content
  inventory from §2 checked against the tree. Michel's word on the
  open items in §5. Output: a one-page record in this tree,
  `docs/prompts/` or `site/README`, of what was found and decided.
- **Gate B — the structure and the look.** A site map of no more
  than eight pages, bilingual, with the text of each page drawn
  from the white paper and the proposal rather than written fresh;
  and two or three directions for the look as static mock-ups
  Michel can open (HTML in the tree, or images), in the palette
  and type above, the UBEC mark where it goes, at phone and
  desktop width. Each direction says what it costs to maintain.
  Michel picks one or asks for another.
- **Gate C — built in the tree.** The site as files under `site/`
  in this repository: source pages in Markdown, both languages; a
  Python build in `build/` in the style of the PDF builds that
  renders them to `site/dist/` with the fonts, the mark, the
  diagrams and the PDFs copied in from `docs/`, so that one
  command rebuilds the whole site from the tree and the PDFs on
  the site are always the committed ones; no JavaScript unless a
  page cannot work without it; a `robots.txt` and an honest
  `humans.txt`; the licence stated. Checked: every internal link
  resolves, every page validates, no request leaves the site, both
  languages complete, the text at phone width legible. README
  bumped, the starting prompt bumped, one commit as Michel Garand.
- **Gate D — on the host.** The DNS record, the vhost (in
  `stack/nginx/` in the mapservice tree if that is where Gate A
  put it, under that tree's rules and as a bounded mapservice
  change), the certificate, the deploy by `rsync` of `site/dist/`
  from a pulled tree — a `deploy` step in the Python build, with
  the host and path as arguments, never in the tree. Michel runs
  it, opens the site on his phone and his computer, and the leak
  check runs: a fetch of every page records every host it
  contacted, and the list is the site's own name only. Closes on
  his "looks good".

## 5. Open — for Michel, at Gate A or when he wants

- **Where the site lives.** A third vhost on ubec-common's nginx,
  serving `site/dist/` from a path on the host; or elsewhere. Who
  manages DNS for `ubec.network`, and how certificates are issued
  there today.
- **Which repository holds the vhost.** The site's source is in
  this tree (OI-P1); the nginx configuration for ubec-common is in
  the mapservice tree. The vhost file is a mapservice change on
  Michel's word for that change, or Gate A finds another place for
  it.
- **What the site says the project is for**, in one sentence on
  the first page, in both languages. The white paper's summary is
  the draft; Michel's word is the text.
- **The documents.** Which are published on the site: the
  proposal, the white paper and the manual, yes; the agreement
  while it is a draft, yes with its draft notice or not at all;
  the reasoning document and the reviews, Michel's word.
  Publishing the white paper here answers the question left open
  on October 9 of serving it from Mapservice.
- **The stage, said plainly.** The sentence that tells a visitor
  there is no host yet, in Michel's words.
- **Pictures.** None, the diagrams only, or photographs of
  Michel's own: whose, under what licence, no home.
- **Languages.** English and Ukrainian now, as every document; the
  arc's other languages when a partner brings them.
- **The field writing.** A link to `pilgrims.ubec.network` and no
  more, or a page that says what it is.
- **What the site is called in Ukrainian** in its title and its
  mark: «Транскарпатські стежки», as the documents say.
- **Whether a page lists partners and declined requests** from the
  start, empty, as S-19 proposes, or only once there is a partner.

## 6. Working rules

- Python for any tool; no secrets in the tree; the whole site
  reproducible from the tree by one command; nothing that lives
  only on the server.
- No third-party request from any page: fonts, images, scripts and
  styles served from `tcp.ubec.network` itself. No cookies. No
  analytics. Logs as the agreement says.
- Every text on the site is a copy of, or a quotation from, a
  document in `docs/`, with its version; when a document changes,
  the site is rebuilt. The site does not become a second source of
  truth.
- Nothing on the site names, pictures, locates or links to a host,
  and nothing promises what the stress tests say the project
  cannot yet show.
- Documents under the project's standard; every file versioned
  with a changelog; commits authored as Michel Garand from a
  pulled tree; pull before any edit.
- At the end of each working session: what was pushed, what Michel
  should pull, on which host, and what he should run.

* * *

*Changelog*
- v0.1 — 2026-10-09 — initial, after the white paper (v0.3, both
  languages) and the stress tests (v0.1); the marks and the font
  rule from Michel's earlier word.
