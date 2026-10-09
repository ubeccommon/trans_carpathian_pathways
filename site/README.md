---
title: "tcp.ubec.network — the site"
version: "v0.1"
date: "2026-10-09"
license: "CC BY-SA 4.0"
project: "Trans-Carpathian Pathways"
status: "Gate A record and the landing page; everything marked proposal waits on Michel's word"
---

# tcp.ubec.network

The project's own place on the web: a small, bilingual, static site
that says what Trans-Carpathian Pathways is. Opened by
`docs/prompts/TCP_WEB_PRESENCE_START_PROMPT_v0_1.md`. For now it is one
landing page in two languages, with the vision and the mission.

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

That writes `site/dist/` (untracked) from `content/` and `static/`, and
checks it. The check confirms that every reference resolves, that
nothing loads from another server, that links out go only to the map
service, the field writing and the stewardship address, that every
element is closed, and that there is no script and no inline style.
Open `site/dist/index.html` in a browser to look before deploying.

To change a text, edit `content/index_en.md` and `content/index_uk.md`
together, bump each one's `version` and `changelog`, and rebuild.

## First deploy (Gate D)

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

   If a server on port 80 already answers ACME challenges for any name,
   this is enough:

   ```bash
   sudo certbot certonly --webroot -w /var/lib/letsencrypt -d tcp.ubec.network
   ```

   If it fails with a 404 on the challenge, install the port-80 half
   first, then take the certificate:

   ```bash
   sed '/^# --- TLS/,$d' tcp.ubec.network | sudo tee /etc/nginx/sites-available/tcp.ubec.network >/dev/null
   sudo ln -sf /etc/nginx/sites-available/tcp.ubec.network /etc/nginx/sites-enabled/
   sudo nginx -t && sudo systemctl reload nginx
   sudo certbot certonly --webroot -w /var/lib/letsencrypt -d tcp.ubec.network
   ```

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
| `static/style.css` | The look: the PDFs' palette and type |
| `static/fonts/` | Inter and Lora, their OFL texts, `SOURCES.txt` |
| `static/assets/ubec_mark.svg` | The UBEC mark, copied from ubec_mapservice |
| `static/robots.txt`, `static/humans.txt` | Who made it, and that it may be indexed |
| `nginx/tcp.ubec.network` | The vhost for ubec-common |
| `../build/build_site.py` | Build, check, deploy, verify |
| `../build/site_fonts.py` | Puts the fonts in `static/fonts/` from their releases, by hand |

* * *

*Changelog*
- v0.1 — 2026-10-09 — initial: the Gate A record, Michel's word on
  where the site lives and what it is for now, and the landing page in
  English and Ukrainian.
