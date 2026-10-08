---
title: "UBEC_MAPSERVICE_FACE_START_PROMPT_v0_1"
subtitle: "Starting prompt — the look of Mapservice's landing and login pages"
author: "Michel Garand"
date: "October 2026"
version: "v0.1"
lang: "en"
license: "CC BY-SA 4.0"
project: "Trans-Carpathian Pathways"
status: "to paste as the first message of a new conversation"
---

*Paste everything below the line as the first message of a new
conversation in the Claude Project "Trans Carpathian Pathway".
It opens the aesthetics of the two pages a visitor meets before
any map: the landing page (the list of applications) and the
login page. It touches `ubec_mapservice`, not Plai's data.*

* * *

## 0. What this conversation is for

The two pages a visitor meets at `https://mapservice.ubec.network/`
before any map: the **landing page**, Mapbender's list of
applications, where today one card says "Plai — Trans Carpathian
Pathway" beside a grey picture placeholder under the heading
"Applications"; and the **login page**, Mapbender's own, with its
default backdrop. Both carry the placeholder mark `UBEC`
(`mapbender/branding/logo.svg`, "placeholder mark, v0.1 — replace
with the network's own logo") that has been outstanding since
Phase 1, step 5 (mapservice prompt §8, "Branding mark").

Not in scope: the map page itself, its toolbar and credits (done
in October), the Digitizer's forms, or any data. Those have their
own conversations.

## 1. Load order — before any work

1. Attach `ubeccommon/ubec_mapservice` with **push** access and
   `ubeccommon/trans_carpathian_pathways` with **read** access.
   Clone both.
2. Read the latest `docs/UBEC_MAPSERVICE_CLAUDE_PROMPT` in the
   mapservice tree: §1, §2, §4, §5, §9, and in §3 the entries
   "Development original and user copy", "Who may open an
   instance" and "Plai's host fields". Its rules bind this work:
   reproducible from the tree, nothing living only on the server;
   no secrets; the leak pass through the public face after any
   change to what the public sees; the checker before any `.md`;
   commits authored as Michel Garand from a pulled tree; pull
   before any edit.
3. Read `stack/docker-compose.yml` (the `mapbender` service and
   what it mounts), `mapbender/config/ubec_branding.yaml`,
   `mapbender/branding/logo.svg`, `stack/nginx/` and README §10.
4. In the Pathways tree, read
   `docs/proposal/assets/plai_emblem_mark.svg` (the round Hutsul
   emblem), `build/diagrams.py` (the palette and the fonts the
   proposal uses) and
   `docs/TRANS_CARPATHIAN_PATHWAYS_CLAUDE_PROMPT` §2 and §7 (what
   the project is and its principles).
5. Clone Mapbender core at the starter's pinned tag,
   `mapbender/mapbender` `v5.0.0-RC2` (`00f4c7e`), read-only, and
   read the files in §3 below before proposing anything. Verify
   every lever against that source, not recall (mapservice §9).
6. Only then begin, with Gate A.

## 2. What is known already

**The stack's branding today** (compose v0.15): the container is
built from the starter at `v5.0.0-RC2`; `ubec_branding.yaml` is
mounted at `config/packages/` and sets two parameters,
`branding.project_name: 'UBEC Mapservice'` and `branding.logo:
'ubec/logo.svg'`; `mapbender/branding/` is mounted read-only under
the web root at `/ubec`. After a change to either: `cache:clear`
in the container. Nothing else about the look is in the tree.

**What the two pages draw from, read at `v5.0.0-RC2`.** In
`src/Mapbender/CoreBundle/Resources/config/mapbender.yaml`, the
site parameters, to be set in the site's own parameters file
(`ubec_branding.yaml` is that file here):

| Parameter | Used where |
|---|---|
| `branding.project_name` | page titles; the backend |
| `branding.logo` | the login page, the backend, templates |
| `branding.splashscreen_image` | an application's splash screen; one image, or a map of application slug to image with a `default` |
| `branding.login_backdrop`, `branding.login_backdrop_hq` | the login page's background; the default is a photograph of the Môle du Raoulic by Jörg Thomsen |
| `mapbender.sitelinks` | links below the login box and the backend content, each `{link, text}` |
| `mapbender.asset_overrides` | a map from an internal template, CSS or JavaScript reference to a replacement (`Asset/ApplicationAssetOverrides.php`) |

The pages themselves: the landing page is
`src/Mapbender/CoreBundle/Resources/views/Welcome/list.html.twig`,
extending `@MapbenderManager/layouts/blocklist.html.twig`, one
card per application with its title, slug ("URL Title"),
description, and a screenshot where the application has one
(`application_screenshot_path`); the login page is
`Resources/views/Login/login.html.twig` with `box.html.twig`,
`form_box.html.twig` and `info_box.html.twig`, extending
`@MapbenderCore/index.html.twig`. A Symfony site overrides any of
them by a file of the same path under the application's
`templates/bundles/MapbenderCoreBundle/`, which for this stack
means a new read-only mount in compose, as the branding directory
is mounted today. An application's screenshot and description are
set in Mapbender's backend on the application itself, and a copy
is exported into `mapbender/exports/` after every backend change
(README §8).

**The palette and the type that already exist**, from Plai's
emblem and the proposal's build: terracotta `#a2352a` and
`#9a362b`, ochre `#c98a2e`, night blue `#161a33`, two greens
`#2a3f2a` and `#3f5e39`, cream `#e8dcb8` and `#f1e6c6`, ink
`#1b1410` and `#1d2027`; Inter for text, Lora for titles. The
map's host points draw in ochre. Whether the network's own mark
and the Plai emblem are the same thing is Michel's word (§4).

**Sessions.** The login lasts one hour (`cookie_lifetime: 3600`,
the starter's default, unchanged by the stack). Known, recorded,
and a separate decision — but this conversation touches the login
page, so it is the place to raise it once.

## 3. Gates

Gate by gate; a gate opens on Michel's word. Claude proposes,
Michel decides, and nothing of Claude's is recorded as decided.

- **Gate A — what is there.** Both pages as a visitor sees them
  today, logged out, at phone and desktop width (Michel supplies
  screenshots; Claude cannot open a browser). Every lever listed
  in §2 confirmed at the tag, and a short list of what each page
  can and cannot become without replacing its template. Shown to
  Michel as a list.
- **Gate B — the proposal.** Two or three directions for the
  two pages, each as a static mock-up Michel can look at (an HTML
  page or an image), in the palette and type above, with the
  emblem where Michel says it goes, bilingual where text appears
  (English and Ukrainian, as the proposal is). Each direction
  says which levers it uses and whether it needs a template
  override. Michel picks one or asks for another.
- **Gate C — built in the tree.** The chosen direction as files
  in `ubec_mapservice`: `ubec_branding.yaml` bumped, assets under
  `mapbender/branding/`, any template override under a directory
  the compose file mounts read-only, the application's screenshot
  and description set in the backend and the copy exported. Every
  image's origin and licence recorded in the file or beside it,
  as the catalogue does for data; no photograph that shows an
  identifiable home. README bumped, prompt bumped, checker PASS,
  one commit as Michel Garand.
- **Gate D — on the host.** Michel pulls, `cache:clear`, reloads
  the vhost if `stack/nginx/` changed, runs the leak pass through
  the public face, and looks. Closes on his "looks good".

## 4. Open — for Michel, at Gate A or when he wants

- **The mark.** Is the network's own logo the Plai emblem, or
  does UBEC have a mark of its own for the landing page, with
  Plai's emblem on its card? Michel supplies whichever is
  missing.
- **The backdrop.** A photograph of the Carpathians for the login
  page, or none: whose, under what licence, and not a home.
- **Language.** The pages' text comes from Mapbender's own
  translations; which locale the site shows, and whether the
  card's title and description are bilingual.
- **The card.** Its title today is "Plai — Trans Carpathian
  Pathway" and its description "User application Carpathian Hub
  - PLai. Its own database; reference layers read across." Both
  are set in the backend; what they should say is Michel's word,
  with the screenshot.
- **The session length**, raised once here, settled wherever
  Michel wants.

## 5. Working rules

- Python for any tool; no secrets; everything in the tree and
  mounted, nothing only on the server.
- Verify every Mapbender claim at `v5.0.0-RC2` before stating it;
  a lever that is not in that source does not exist.
- Documents under the mapservice standard; every file versioned
  with a changelog.
- At the end of each working session: what was pushed, what
  Michel should pull, and on which host.

* * *

*Changelog*
- v0.1 — 2026-10-08 — initial, after Gate 2 of Pathways closed;
  levers read at Mapbender core `00f4c7e` (`v5.0.0-RC2`).
