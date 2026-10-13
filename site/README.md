---
title: "tcp.ubec.network — the site"
version: "v0.22"
date: "2026-10-13"
lang: "en"
license: "CC BY-SA 4.0"
project: "Trans-Carpathian Pathways"
status: "Gate A record of the first site, the menu and the documents' pages, and of the documentation as one set (docs/prompts/TCP_DOCUMENTATION_START_PROMPT_v0_1.md); Gate B, the landing page for the public review, built in the tree on October 13 — Gate E on the host next"
---

# tcp.ubec.network

The project's own place on the web: a small, bilingual, static site
that says what Trans-Carpathian Pathways is. Opened by
`docs/prompts/TCP_WEB_PRESENCE_START_PROMPT_v0_2.md`; reworked for the
public review from `docs/prompts/TCP_LANDING_PAGE_START_PROMPT_v0_1.md`.
A landing page and a page for each document published for review, in two
languages, under one menu.

## The menu and the documents — Michel's word, October 11, 2026

- **Our own build, not Ghost.** Asked whether the site should move to
  Ghost, Michel chose to build on what the site has: the static build
  in this tree. Ghost stays where it is, for the field writing at
  `soilandpeace.ubec.network`. What weighed: Ghost keeps its pages in a
  database on the server, not in the record; by default it loads
  scripts and offers a sign-up form; it has no paired pages in two
  languages; and it is one more service for one person to keep.
- **A menu above the picture, on every page,** in the logical order
  (Michel's word the same morning): About (the landing page), the
  overview, the proposal, the white paper with its chapters in a
  drop-down, the co-creator agreement with its parts and the roles of
  Part II in a drop-down, the map (Plai) and the field writing. The
  same order in both languages. The drop-downs are `<details name="menu">`: no script, one
  open at a time, reached by keyboard.
- **A page per document and language** (`/whitepaper/`, `/proposal/`,
  `/agreement/`, `/overview/`, and under `/uk/`), built by
  `build/build_site.py` from the latest file of each in `docs/`, with
  its diagrams and its committed PDF copied in. The page names the
  file and version it was built from and links to it in the record.
  The site holds no copy of a document's words of its own.
- **The field writing** — in the menu and on the landing page — is
  Soil and Peace at `https://soilandpeace.ubec.network/` (Michel's
  word, October 11; the first pages linked `pilgrims.ubec.network`,
  another of his blogs). The build allows that host and no longer the
  other.
- **The map link** — in the menu and on the landing page — opens the
  Pathways application on Plai, `ubec_plai_hub_tcp`, on the first
  corridor around Verkhovyna (Michel's word, October 11). The check
  allows that application and the map service's front page, and no
  other path on it: never a link to a point. It opens in a new tab,
  and so does the field writing (Michel's word, the same morning), with `rel="noopener"`, an arrow
  after its name, and "opens in a new tab" for a screen reader.
- **The overview** is in English, and since October 13 in Ukrainian too
  (`docs/overview/PROJECT_OVERVIEW_UK_v0_5.md`, Michel's word; Claude's
  translation of the English v0.5, not yet read in the corridor), with its
  page under `/uk/overview/`; the German and Polish menus show it in
  English.
- **Every Ukrainian page says, in one line,** that the Ukrainian texts
  have not yet been read by people in the corridor (D-2, open).
- **Links out.** The site's own pages link to Plai's front page, the
  field writing, the stewardship address and, the repository being
  public since October 11, the record on GitHub — that repository's
  path only. Inside a document's text, links to the sources it cites
  go anywhere over https; nothing on any page loads from another
  server, and nothing links to a point on Plai. *(Claude's proposal,
  in place until Michel's word.)*

**On the host — Michel's "looks good", October 11, 2026:** the menu,
the documents' pages, the map in its own tab, deployed from schiff and
looked at.

## German and Polish — Michel's word, October 11, 2026

- **A landing page in each** (`/de/`, `/pl/`), Claude's translation of
  the English page v0.6, and the menu in each. Every German and Polish
  page says, in one line, that it is a translation not yet read by
  someone whose language it is, and that the documents are in English
  and Ukrainian.
- **The overview, the proposal and the white paper in German and Polish**
  (Michel's word, the same morning): Claude's translations of the English
  overview v0.5, proposal v0.7 and white paper v0.9, in `docs/` beside
  their sources (`*_DE.md`, `*_PL.md`, `PROJECT_OVERVIEW_{DE,PL}_v0_5.md`),
  with their diagrams and a PDF each for the proposal and the white paper
  (`*_DE.pdf`, `*_PL.pdf`; the EN-UK PDFs unchanged). The words are in
  `docs/translations/GLOSSARY_DE_PL_v0_1.md`. Checked twice: a script
  (every source number in order, every URL, heading, table row and
  figure), then a separate reader in each language against the English;
  their findings taken in, the EU Package Travel Directive quoted from
  its official German and Polish texts. Every translation says, on the
  page and on the PDF's cover, that nobody whose language it is has read
  it yet.
- **On the host — Michel's "looks good", October 11, 2026:** deployed
  from `main` at `1ea198a`, 17 pages, the four German and Polish PDFs
  among the 53 files `verify` fetched from the site's own name alone;
  his look at the German and Polish documents, their PDFs and the
  language list.
- **The co-creator agreement stays in English and Ukrainian** until it
  has settled and a native reader is lined up: in the German and Polish
  menus it carries a small EN tag, and a screen reader hears «auf
  Englisch» or «po angielsku».
- **The name stays English** in both: «Transkarpatien» in German and
  «Zakarpacie» in Polish name Zakarpattia oblast, the same misreading
  the review found in «Транскарпатські» (D-1). Under the name, the
  German and Polish pages show the Ukrainian name, the corridor's own.
- **The words chosen**, recorded in each file's changelog: German
  place names in German transliteration (Worochta, Werchowyna, Kossiw),
  the pathway steward as Wegepatin and Wegepate, paired forms for
  people (Gastgebende, Kuratorinnen und Kuratoren); Polish place names
  in their Polish forms (Worochta, Werchowyna, Kosów), the pilgrim as
  *pielgrzym płaju* — *płaj* is a word of the Polish Carpathians too —
  and the steward as *opiekun szlaku*. *(Claude's proposals, for a
  speaker of each language.)*
- **The language switch is now a list** of the four, each by its own
  name, in the old switch's place; `hreflang` for all four and
  `x-default` on every landing page.

The questions the landing-page prompt §5 left open on October 11 are
answered below (the documentation as one set, Gate A, October 13).

## The documentation as one set — Gate A, Michel's word, October 13, 2026

The documents were written one by one; the map service moved past
them. A conversation of its own
(`docs/prompts/TCP_DOCUMENTATION_START_PROMPT_v0_1.md`) read the set
at this tree's `91063ba` and the map service's `9356c18`, and took
over the landing-page prompt's Gate A. Found, as it bears on the
site: the landing page's footer cites white paper v0.3 and proposal
v0.2 (now v0.9 and v0.7); the mission gives "Curators who hold each
stretch", which the pathway steward holds since October 8; "Where we
are" says "No host, steward or Curator is named" and nothing of the
planner, which is public on Plai since October 11 ("Plan a way"); the
border rules the agreement §7 and the proposal promise to publish for
those who come directly are published nowhere; the recognition line
("writes only from stewardship@ubec.network; nobody asks for money in
advance, a deposit, a password or a passport") is in the agreement
and the proposal and not on the site; the manual (v0.8) is not on the
site and knows neither the planner nor the `geo:` link; the
repository answers the GitHub API publicly. *Michel's word, October
13: Claude's proposals taken as the answers — each Claude's wording,
for his word:*

- **The branches.** `main` fast-forwarded to `stage-planner-route`
  (`91063ba`): prompt v0.65, decisions v0.8, reasoning v0.4, the
  planner spec v0.4 and `tools/` are on the branch the site is built
  from. The site's four documents did not change.
- **Which documents for review:** the overview, the proposal, the
  white paper and the co-creator agreement, as pages and PDFs, as
  now. The reasoning and the open-data specification not this round.
- **How the review is answered:** by mail to the stewardship address
  and by issues on the public repository; no closing date — the
  review runs as long as the drafts are drafts, and the page says so.
- **The record:** linked from the landing page, labelled "The
  project's record on GitHub" / «Запис проєкту на GitHub»; the build
  already allows that one path.
- **The border rules:** a section of the landing page, "If you come
  directly", stating them as white paper §10.2 does — with its
  sources, its reading date and the line that this is not legal
  advice — and linking to §10.2 on the white paper's page; never a
  route, a stage or a village inside the strip.
- **How to recognise the project:** on the landing page beside the
  contact line, in the agreement's words.
- **"Where we are":** what is built today — the map with its host
  fields, the planner public on Plai ("Plan a way"), the documents in
  four languages, the record public; what is not — no host or steward
  named, the agreement a draft, the corridor not walked; the test of
  the concept runs with the public review (D-4); and the first
  Curator in one wording, the same in every document (D-5): *the
  project lead is the first Curator for now, until a core body is
  formed.*
- **The planner on the page:** named in "Where we are" and in the map
  link's line; the link stays the Pathways application
  `ubec_plai_hub_tcp`.
- **The plai in a line:** one line under the mission says what the
  plai is — the old way through the high pastures, from which the map
  takes its name.
- **The picture's licence:** CC BY-SA 4.0, as the text and the marks;
  the footer names it.
- **One page or more:** the menu stands; the user guide gains a page,
  "Guide" / «Посібник», after the co-creator agreement, with its PDF,
  built from `docs/manual/` by `build/build_site.py` like the others.
- **The documents:** the white paper is revised this round (v0.10),
  the proposal (v0.8), the overview (v0.6, with a Ukrainian text at
  last) and the plan follow where the change reaches them; the
  Ukrainian and the German and Polish follow the English, each still
  saying who has not read it.
- **Still open, and the pages say so:** the Ukrainian name (D-1) and
  the reading in the corridor (D-2) wait on Vasyl Yuskiv and two
  residents; the backups line (D-6) says off-host backups are the
  condition of the first real account.

Gates B (the landing page: outline, English, Ukrainian, German and
Polish, built and checked), C (the white paper and what follows it)
and D (the user guide in four parts) follow, each closing with one
commit; Gate E on the host, on Michel's "looks good".

## The landing page for the public review — Gate B, Michel's word, October 13, 2026

Built from the sources at their current versions, section by section;
every sentence on the page is drawn from a document in `docs/`, and
the footer names them (white paper v0.9, proposal v0.7, agreement
v0.7).

| Section | What it says | Source |
| --- | --- | --- |
| Vision | unchanged | white paper summary, §9 |
| Mission | the pathway steward cares for each stretch, the Curator holds the whole; one line on the plai and the Pilgrim of the Plai | proposal (summary, roles); white paper §4.3 |
| The regenerative test | unchanged | white paper §5, §12 |
| Where we are | built: the map with its host fields, "Plan a way" public on Plai, a steward or Curator keeps stretches and corridors, the Curator publishes; the documents in four languages; the record public. Not yet: no host or steward named; the first Curator is the project lead for now, until a core body is formed; the agreement a draft; the corridor not walked; the first hosts after off-host backups and the data-protection read. The test of the concept with the review | white paper §11 as corrected at Gate A; overview "Where the project stands"; prompt v0.66 §2, §6; mapservice `9356c18` |
| Read, and answer | the four drafts with links to their pages; EN/UK, DE/PL translations unread by their speakers, the Ukrainian unread in the corridor; mail or an issue on the record; no closing date | prompt v0.66 Gate A; review §5 D-2 |
| If you come directly | own preparation (advice, martial law, insurance, cash, permits); curfew, alerts, the five-kilometre strip, the permit, the Verkhovyna district, routes to Chornohora closed or restricted; no stage inside the strip suggested; the sources named and dated, "not legal advice"; a link to §10.2. Never a route, a stage or a village inside the strip | white paper §10 intro, §10.2 [54][55]; agreement §7, pilgrim part; proposal, Safety |
| How to recognise the project | writes only from the stewardship address; nobody asks for money in advance, a deposit, a password, a passport or a copy; the pilgrim pays the host; the project holds no money for stays and takes no share | agreement Part II (host, pilgrim), §8; proposal, Safety |
| Elsewhere | the map, with "Plan a way" named; the field writing; the record on GitHub ("The project's record on GitHub"; an issue answers the review); write to us | — |

English first (landing page v0.8), then Ukrainian (v0.8; the note that
the corridor has not read it stays), then German and Polish (v0.3,
Claude's translations of the English v0.8, each saying so). The
picture's licence is CC BY-SA 4.0 and the footer names it. The
stylesheet (v0.8) sets a list inside a block like a document's. Links
inside the page are written relative per language (pandoc encodes a
placeholder inside an href). The build's checks pass on all 17 pages;
the English and Ukrainian pages were looked at headless at 390 and
1280 px wide: nothing cut off, nothing scrolling sideways. Gate E —
deploy from schiff, verify, Michel's look on phone and computer, and
the person's accessibility checks below for the new sections — closes
on his "looks good".

## Gate A — what was found

Read on October 9, 2026, at this tree's `39d7a5c` (starting prompt
v0.27) and ubec_mapservice's `bbc6a36` (its prompt v0.81).

- **The host.** ubec-common runs the system nginx in front of the map
  service's containers. Each vhost is installed by hand from a tree into
  `/etc/nginx/sites-available/`. Certificates come from certbot with
  the webroot `/var/lib/letsencrypt`, which `mapservice.ubec.network`
  and `erdpuls.ubec.network` already use. A static site is one more
  vhost of that kind.
- **The marks.** The UBEC mark exists only in ubec_mapservice
  (`mapbender/branding/logo.svg`, v0.1, CC BY-SA 4.0). It is copied
  unchanged to `static/assets/ubec_mark.svg`, with its origin in its
  header. The Plai emblem is this tree's
  `docs/proposal/assets/plai_emblem_mark.svg`. The build crops it to its
  circle and uses it only beside the link to Plai.
- **The fonts.** Neither tree held any font file. Inter 4.1 and Lora
  (Lora-Cyrillic at `2d53b44`) are now in `static/fonts/` with their
  OFL texts. `build/site_fonts.py` put them there, and
  `static/fonts/SOURCES.txt` records each file's origin and SHA-256.
  Lora is re-encoded as WOFF2 but not subset, because its Reserved Font
  Name would not survive a subset.
- **The documents.** Proposal v0.2, white paper v0.3, agreement v0.2
  (draft) and manual v0.3 are all committed as PDFs. There are three
  reviews, not the two the prompt counts. Proposal v0.2 still carries
  its known drifts: the contact line "to be added", no steward, and a
  Curator who "holds a stretch". The covers of the proposal, the white
  paper and the agreement carry the Plai emblem, though none of them is
  a Plai application. None of the documents is on the site yet.

## Gate A — decided

Michel's word, October 9, 2026:

- **The site is the project's, apart from the map service.** Its
  source, its build and its vhost are in this tree
  (`nginx/tcp.ubec.network`). Nothing is changed in ubec_mapservice.
- **It links to the map service**: Plai, at
  `https://mapservice.ubec.network/`.
- **It is served from `/var/www/tcp.ubec.network` on ubec-common.**
- **DNS:** an A/AAAA record for `tcp` pointing at ubec-common.
- **A landing page for now, with a vision and a mission statement.**

## In place until Michel's word — Claude's proposals

- **The text.** The vision, the mission, the regenerative test and
  "Where we are" are drafted from white paper v0.3 (summary, §5, §9 and
  §11) and proposal v0.2 (summary and cover), in both languages. The
  Ukrainian follows the white paper's glossary, and nobody from the
  corridor has read it yet.
- **No access log.** The vhost logs errors only (agreement §5).
- **Indexed.** `robots.txt` allows everything, and there is no
  `noindex`.
- **The picture.** Michel's word, October 9: his "Warm wind on the
  path" (day 70, from his field writing) heads the landing page. It is
  an SVG with no text, no location and no outside reference, copied
  unchanged but for a comment that records its origin. Its licence is
  not yet stated, so the footer's CC BY-SA line still names the text
  and the marks only.
- **The field writing** is linked as "Soil and Peace — Carpathian
  Dispatch".
- **Still open from the starting prompt §5:** which documents go on
  the site, pictures, partners and declined requests (S-19), and the
  page count once there is more than one page.

## What the page holds, and what it never will

It shows the name in both languages, the tagline, the vision, the
mission, the regenerative test, the stage said plainly, and three links
out: the map, the field writing and `mailto:stewardship@ubec.network`.

It does not name, picture, locate or link to any host. It has no form.
It promises no income and no journey. It runs no script and sets no
cookie, and it loads nothing from any other server. The vhost's
Content-Security-Policy refuses anything else, and the build's check
refuses a page that tries.

## Build

Needs Python 3 and pandoc; nothing from pip.

```bash
cd /home/farmer/projects/plai && git pull --ff-only
python3 build/build_site.py
```

That writes `site/dist/` (untracked) from `content/`, `static/` and the
documents in `docs/` named in the build's `DOCS`, and checks it. The
check confirms that every reference and every chapter link resolves,
that nothing loads from another server, that the site's own links out
go only to the map service's front page, the field writing, the
stewardship address and the record on GitHub, that every element is
closed, and that there is no script and no inline style. Open
`site/dist/index.html` in a browser to look before deploying.

To change the landing page, edit `content/index_en.md` and
`content/index_uk.md` together, bump each one's `version` and
`changelog`, and rebuild. To change a document's page, change the
document in `docs/`; the next build follows. To add a document to the
menu, add it to `DOCS` in `build/build_site.py`.

## Accessibility — WCAG 2.2 AA

Michel's word, October 9, 2026 (module map, §3): the site meets WCAG
2.2 at level AA, and every page and part says its language in a BCP 47
tag (`en`, `uk`).

**What the build checks**, every time (`build/build_site.py`, v0.4):
the page's language and every `lang` and `hreflang` as a BCP 47 tag;
one `h1` and no skipped heading level; `alt` on every picture; a name
on every link; a title; and the contrast of every colour pair the
stylesheet uses, by its `CONTRAST` table — 4.5:1 for text, 3:1 for
focus outlines. A new colour pair in `style.css` gets a line in that
table.

**What was changed for it** (stylesheet v0.4): the focus outline was
ochre on paper, 2.8:1, and is now night blue on light ground and ochre
on the night head; the arrow before each link in the list is silent to
screen readers; the name in the picture keeps a floor in `rem`, so it
grows when only the text is enlarged; the UBEC mark beside its name has
an empty `alt`, so the name is not read twice.

**What only a person can check**, before the first deploy and after any
change to the head:

- With the keyboard alone, every link is reached in order, its outline
  visible, and the skip link appears first.
- A screen reader (NVDA or VoiceOver) reads each page in its own
  language, the other language's name in the other.
- At 200% zoom, and at 200% text-only zoom, nothing is cut off; at 320
  px wide nothing scrolls sideways.
- With WCAG's text spacing applied (line height 1.5, paragraphs 2,
  letters 0.12, words 0.16), the name in the picture stays readable.
- The name, the other language's name and the tagline are read against
  the picture itself, at their darkest and lightest points — the build
  cannot measure text over a picture.
- The language switch is at least 24 by 24 px.

## First deploy (Gate D)

0. **The host's name on schiff.** `ubec-common` is the host's own
   name, not one schiff's DNS knows. Give ssh an alias for it once, in
   `/home/farmer/.ssh/config`, with the address you already ssh to, and
   every command below works as written. The address stays out of the
   tree, as every access detail of the host does:

   ```
   Host ubec-common
       HostName <the address you ssh to>
       User ubec
   ```

1. **DNS.** Add A and AAAA records for `tcp.ubec.network` with
   ubec-common's addresses.
2. **On ubec-common, the directory:**

   ```bash
   sudo install -d -o ubec -g ubec -m 755 /var/www/tcp.ubec.network
   ```

3. **The certificate.** Copy the vhost to ubec-common, from schiff:

   ```bash
   scp /home/farmer/projects/plai/site/nginx/tcp.ubec.network ubec@ubec-common:
   ```

   On ubec-common no other server answers the challenge for a new name
   (the first try, October 9, got a redirect to https and a 503), so the
   port-80 half goes in first, then the certificate:

   ```bash
   sed '/^# --- TLS/,$d' tcp.ubec.network | sudo tee /etc/nginx/sites-available/tcp.ubec.network >/dev/null
   sudo ln -sf /etc/nginx/sites-available/tcp.ubec.network /etc/nginx/sites-enabled/
   sudo nginx -t && sudo systemctl reload nginx
   sudo certbot certonly --webroot -w /var/lib/letsencrypt -d tcp.ubec.network
   ```

   Never leave the whole file in `sites-enabled` without its
   certificate: `nginx -t` fails, and the next reload or reboot of
   nginx fails with it, for every site on the host.

4. **The vhost, whole:**

   ```bash
   sudo install -m 644 tcp.ubec.network /etc/nginx/sites-available/
   sudo ln -sf /etc/nginx/sites-available/tcp.ubec.network /etc/nginx/sites-enabled/
   sudo nginx -t && sudo systemctl reload nginx
   ```

5. **The site, from schiff:**

   ```bash
   cd /home/farmer/projects/plai && git pull --ff-only
   python3 build/build_site.py deploy ubec@ubec-common /var/www/tcp.ubec.network
   python3 build/build_site.py verify https://tcp.ubec.network
   ```

   `verify` fetches both pages and every file they load, and checks for
   the security headers and the absence of cookies. It passes only if
   the one host it contacted is `tcp.ubec.network`.

After that, every change is step 5 alone. A change to
`nginx/tcp.ubec.network` is step 4 again, because a pull does not
install it.

Tested before the first commit: the vhost loaded in nginx 1.24 with a
throwaway certificate, and both pages, the stylesheet, the fonts and the
marks were served. A dotfile was refused, port 80 redirected, and no
access line was written. A headless browser at phone width loaded both
pages with all four fonts and both marks, contacted no host but the
site's own, and logged no policy violation.

## Files

| Path | What it is |
| --- | --- |
| `content/index_en.md`, `content/index_uk.md` | The landing page's text, one file per language |
| `../docs/` (white paper, proposal, agreement, overview) | The documents' pages, built from them; never copied into `site/` |
| `static/style.css` | The look: the PDFs' palette and type |
| `static/fonts/` | Inter and Lora, their OFL texts, `SOURCES.txt` |
| `static/assets/ubec_mark.svg` | The UBEC mark, copied from ubec_mapservice |
| `static/assets/warm_wind_on_the_path.svg` | Michel's picture "Warm wind on the path" (day 70), the head of the landing page |
| `static/robots.txt`, `static/humans.txt` | Who made it, and that it may be indexed |
| `nginx/tcp.ubec.network` | The vhost for ubec-common |
| `../build/build_site.py` | Build, check, deploy, verify |
| `../build/site_fonts.py` | Puts the fonts in `static/fonts/` from their releases, by hand |

* * *

*Changelog*
- v0.22 — 2026-10-13 — the third initiator, Michel's word: Tepla Gora, led by Andriy Grushetsky, in the
  initiator line of every landing page (en/uk v0.9, de/pl v0.4); the documents' pages follow their files
  (overview v0.6, proposal v0.8, white paper v0.10, agreement v0.8).
- v0.21 — 2026-10-13 — the overview in Ukrainian, Michel's word: a page under /uk/overview/,
  the Ukrainian landing page and menu pointing to it. Build v0.14; landing page uk v0.8 amended.
- v0.20 — 2026-10-13 — the landing page for the public review, Gate B, Michel's word: the
  outline with its sources, the page in English, Ukrainian, German and Polish, built and
  checked. Landing pages en/uk v0.8, de/pl v0.3, stylesheet v0.8.
- v0.19 — 2026-10-13 — the documentation as one set, Gate A, Michel's word: what was found against the
  site, and Claude's proposals taken as the answers to the landing-page prompt's §5 — the four documents for review,
  mail and issues, the record linked, the border rules and the recognition line on the page, "Where we are" as built,
  one wording for the first Curator, the plai in a line, the picture CC BY-SA 4.0, a page for the guide. `main`
  fast-forwarded to the planner branch.
- v0.18 — 2026-10-11 — the field writing at soilandpeace.ubec.network,
  Michel's word. Build v0.13, landing pages en/uk v0.7, de/pl v0.2.
- v0.17 — 2026-10-11 — the German and Polish documents closed on the host,
  Michel's "looks good".
- v0.16 — 2026-10-11 — the overview, the proposal and the white paper
  in German and Polish, Michel's word. Build v0.12.
- v0.15 — 2026-10-11 — German and Polish, Michel's word; his "looks
  good" on the menu as deployed. Build v0.11, stylesheet v0.7, landing
  pages en and uk v0.6, de and pl v0.1.
- v0.14 — 2026-10-11 — the field writing opens in a new tab too, Michel's
  word. Build v0.10.
- v0.13 — 2026-10-11 — the map opens in a new tab, Michel's word. Build
  v0.9, stylesheet v0.6.
- v0.12 — 2026-10-11 — the overview second in the menu, in both
  languages, Michel's word. Build v0.8.
- v0.11 — 2026-10-11 — the map link opens the Pathways application on
  the corridor, Michel's word. Build v0.7, landing page v0.5.
- v0.10 — 2026-10-11 — the proposal before the white paper in the
  menu, Michel's word. Build v0.6.
- v0.9 — 2026-10-11 — Michel's word: our own build, not Ghost; a menu
  above the picture on every page; a page per document and language,
  built from `docs/`, with its PDF. Build v0.5, stylesheet v0.5. (v0.8
  of October 10 had no line here.)
- v0.7 — 2026-10-09 — WCAG 2.2 AA and BCP 47 language tags, Michel's
  word: what the build checks, what was changed, what a person checks.
- v0.6 — 2026-10-09 — the name inside the picture's frame (Michel's word):
  left of the moon and above the ridge at every width; on a narrow screen
  the name alone, on two lines, with the other language's name and the
  tagline below the picture. Stylesheet and pictures referenced with
  `?v=` and their hash, so a cached old copy is never shown.
- v0.5 — 2026-10-09 — Michel's picture in the head of the landing page.
- v0.4 — 2026-10-09 — step 3: the port-80 half first, always, after the
  first certificate request failed; the warning against a vhost
  enabled without its certificate.
- v0.3 — 2026-10-09 — step 0 names no address: the alias takes the one
  Michel already uses; access details stay out of the tree.
- v0.2 — 2026-10-09 — step 0: the ssh alias for ubec-common on schiff,
  after `scp` could not resolve the name.
- v0.1 — 2026-10-09 — initial: the Gate A record, Michel's word on
  where the site lives and what it is for now, and the landing page in
  English and Ukrainian.
