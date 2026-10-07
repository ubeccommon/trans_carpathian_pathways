# Trans-Carpathian Pathways

A living network of hosts, a pathway that grows from where they
are, and Curators who hold each stretch of it, across the
Carpathian arc. First corridor: Vorokhta, Verkhovyna and Kosiv in
the Hutsul highlands of western Ukraine. Initiated by UBEC (Ubuntu
Bioregional Economic Commons), led by Michel Garand.

The project runs on Plai, the Carpathian hub instance of UBEC
Mapservice (`ubeccommon/ubec_mapservice`). It does not own that
stack: what Pathways needs from Plai is specified here and built
there, as Plai migrations in `ubec_mapservice`.

## What is here

| Path | What it holds |
| --- | --- |
| `docs/TRANS_CARPATHIAN_PATHWAYS_CLAUDE_PROMPT_v*.md` | The starting prompt, latest version: load order, decisions, open items. Source of truth. |
| `docs/proposal/` | The outward proposal in English and Ukrainian, its diagrams and logo, and the bilingual PDF built from them |
| `build/` | The scripts that draw the diagrams and build the PDF |
| `docs/specs/` | Specifications for changes built elsewhere — Plai migrations in `ubec_mapservice` |
| `docs/reviews/` | Read-only reviews of the stack Pathways runs on, before a change is made |
| `tools/` | Empty until a tool is needed |

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
