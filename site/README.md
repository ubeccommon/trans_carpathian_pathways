---
title: "tcp.ubec.network — the site"
version: "v0.11"
date: "2026-10-11"
lang: "en"
license: "CC BY-SA 4.0"
project: "Trans-Carpathian Pathways"
status: "Gate A record of the first site, the menu and the documents' pages; the landing page's rework for the public review waits on Michel's Gate A answers (docs/prompts/TCP_LANDING_PAGE_START_PROMPT_v0_1.md)"
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
  `pilgrims.ubec.network`. What weighed: Ghost keeps its pages in a
  database on the server, not in the record; by default it loads
  scripts and offers a sign-up form; it has no paired pages in two
  languages; and it is one more service for one person to keep.
- **A menu above the picture, on every page:** About (the landing
  page), the proposal, the white paper with its chapters in a
  drop-down (the proposal before the white paper, Michel's word the
  same morning), the co-creator agreement with its parts and the roles of
  Part II in a drop-down, the overview, the map (Plai) and the field
  writing. The drop-downs are `<details name="menu">`: no script, one
  open at a time, reached by keyboard.
- **A page per document and language** (`/whitepaper/`, `/proposal/`,
  `/agreement/`, `/overview/`, and under `/uk/`), built by
  `build/build_site.py` from the latest file of each in `docs/`, with
  its diagrams and its committed PDF copied in. The page names the
  file and version it was built from and links to it in the record.
  The site holds no copy of a document's words of its own.
- **The map link** — in the menu and on the landing page — opens the
  Pathways application on Plai, `ubec_plai_hub_tcp`, on the first
  corridor around Verkhovyna (Michel's word, October 11). The check
  allows that application and the map service's front page, and no
  other path on it: never a link to a point.
- **The overview** exists in English only; the Ukrainian menu shows it
  as «Огляд (англійською)» and leads to the English page.
- **Every Ukrainian page says, in one line,** that the Ukrainian texts
  have not yet been read by people in the corridor (D-2, open).
- **Links out.** The site's own pages link to Plai's front page, the
  field writing, the stewardship address and, the repository being
  public since October 11, the record on GitHub — that repository's
  path only. Inside a document's text, links to the sources it cites
  go anywhere over https; nothing on any page loads from another
  server, and nothing links to a point on Plai. *(Claude's proposal,
  in place until Michel's word.)*

Still open, from the landing-page prompt §5 and Gate A put to Michel
on October 11: the landing page's own text (the mission and "Where we
are" are behind their sources), how the review is answered, how to
recognise the project, the border rules for those who come directly,
the record's link on the landing page, and the picture's licence. The
overview's line "available in English and Ukrainian on request" now
contradicts the site and waits on his word.

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
