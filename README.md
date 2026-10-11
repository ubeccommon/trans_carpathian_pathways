# Trans-Carpathian Pathways

A living network of hosts, a pathway that grows from where they
are, and Curators who hold each stretch of it, across the
Carpathian arc. First corridor: Vorokhta, Verkhovyna and Kosiv in
the Hutsul highlands of western Ukraine. Initiated by UBEC (Ubuntu
Bioregional Economic Commons), led by Michel Garand, and Zhyva
Khata, led by Vasyl Yuskiv.

The project runs on Plai, the Carpathian hub instance of UBEC
Mapservice (`ubeccommon/ubec_mapservice`). It does not own that
stack: what Pathways needs from Plai is specified here and built
there, as Plai migrations in `ubec_mapservice`.

## What is here

| Path | What it holds |
| --- | --- |
| `docs/TRANS_CARPATHIAN_PATHWAYS_CLAUDE_PROMPT_v*.md` | The starting prompt, latest version: load order, decisions, open items. Source of truth. |
| `docs/IMPLEMENTATION_PLAN_v*.md`, `_UK_v*.md` | The project in one page and the step-by-step plan with to-do lists, in English and Ukrainian, and the bilingual PDF (`build/build_plan.py`) |
| `docs/DECISIONS_CHECKLIST_v*.md` | The questions put to Michel, one line each, with his answers and the document each changed; what is still open |
| `docs/TRANS_CARPATHIAN_PATHWAYS_REASONING_v*.md` | Why the project exists: the pressures it answers, the vision of corridors of stewardship, the reason behind each principle, and the tensions still open |
| `docs/whitepaper/` | The white paper for readers outside the project — the case, the evidence, regeneration against sustainable development, and the design, with its sources — in English and Ukrainian, its three diagrams in both languages, and the bilingual PDF built from them |
| `docs/proposal/` | The outward proposal in English and Ukrainian, its diagrams and logo, and the bilingual PDF built from them |
| `build/` | The scripts that draw the diagrams and build the PDFs |
| `docs/manual/` | Plai's user manual for entrants and curators, in English and Ukrainian, and the bilingual PDF built from them |
| `docs/agreement/` | The co-creator agreement for every role, in English and Ukrainian, and the bilingual PDF built from them — a draft until its open items are settled |
| `docs/specs/` | Specifications for changes built elsewhere — Plai migrations in `ubec_mapservice` |
| `docs/reviews/` | Read-only reviews — of the stack Pathways runs on, of the project as a whole, and the stress tests of its design — each before a change is made |
| `docs/prompts/` | Starting prompts for conversations that open a bounded piece of work |
| `site/` | The site at tcp.ubec.network — its text in both languages, its style, fonts and mark, its nginx vhost, and the Gate A record (`site/README.md`) |
| `tools/` | The stage planner, public: `route` — a route by the project's criteria, its fuzzy band of reach and the places along it — and `corridor`, stretches joined (`tools/README.md`) |

## Building the proposal PDF

Needs Python 3, pandoc, Cairo (for CairoSVG), and the Inter and Lora fonts installed
system-wide (on Debian or Ubuntu: `fonts-inter`; Lora from Google
Fonts).

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r build/requirements.txt
python3 build/build_pdf.py
```

That one command renders `logo.png` from the emblem
`plai_emblem_mark.svg`, cropped to its circle, redraws the four
diagrams in `docs/proposal/assets/`, and writes
`docs/proposal/Trans-Carpathian_Pathways_Proposal_EN-UK.pdf`
(A4, cover then English then Ukrainian). If Inter is not in
`/usr/share/fonts/opentype/inter`, set `INTER_FONT_DIR` first.

The PDF is committed, so it can be sent without building. Rebuild
and commit it whenever either proposal text changes.

## Building the user manual

Same tools as the proposal:

```bash
python3 build/build_manual.py
```

The screenshots it shows are in `docs/manual/img/`, referenced from
both texts. It writes `docs/manual/Plai_User_Manual_EN-UK.pdf` (A4, a cover
with Plai's emblem, then English, then Ukrainian), in the
proposal's styles. The PDF is committed; rebuild and commit it
whenever either text changes, and check the texts whenever a Plai
form or rule changes.

## Building the white paper

Same tools as the proposal:

```bash
python3 build/build_whitepaper.py
```

That one command draws the three diagrams into
`docs/whitepaper/assets/` in both languages and writes
`docs/whitepaper/Trans-Carpathian_Pathways_White_Paper.pdf`
(A4, a cover, then English, then Ukrainian), in the proposal's styles. The PDF is committed; rebuild and commit it
whenever the text changes.

## Building the co-creator agreement

Same tools as the proposal:

```bash
python3 build/build_agreement.py
```

It writes `docs/agreement/Trans-Carpathian_Pathways_Co-Creator_Agreement_EN-UK.pdf`
(A4, a cover, then English, then Ukrainian, each ending with its
sign-on sheet on a page of its own), in the proposal's styles.
While the agreement is a draft, the cover and every footer say so.
The PDF is committed; rebuild and commit it whenever either text
changes, and change both texts together.

Plai links to the agreement from its entry form and records the
version each entrant accepted. That copy is served by
`ubeccommon/ubec_mapservice`, since this repository is private:
a new version shown on Plai means its PDF copied there under a
new file name, and a Plai migration there for the new version.

## Building the site

Needs Python 3 and pandoc only:

```bash
python3 build/build_site.py
```

It writes `site/dist/` (not tracked) and checks it: every reference
resolves and nothing loads from another server. Deploying and the
first install on ubec-common are in `site/README.md`.

## Taking the latest work

Clone once:

```bash
mkdir -p /home/farmer/projects
git clone git@github.com:ubeccommon/trans_carpathian_pathways.git /home/farmer/projects/plai
```

(or `https://github.com/ubeccommon/trans_carpathian_pathways.git`
without SSH keys). Thereafter:

```bash
cd /home/farmer/projects/plai && git pull --ff-only
```

Pull before any edit: work is pushed from more than one place.

## Licences

Code under the GNU Affero General Public License v3.0 or later
(`LICENSE`). Documents, the proposal and its diagrams under
Creative Commons Attribution-ShareAlike 4.0 International
(`LICENSE-docs`).
