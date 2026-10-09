---
title: "TRANS_CARPATHIAN_PATHWAYS_CLAUDE_PROMPT_v0_37"
subtitle: "Starting Prompt — Trans-Carpathian Pathways on Plai"
author: "Michel Garand"
date: "October 2026"
version: "v0.37"
lang: "en"
license: "CC BY-SA 4.0"
project: "Trans-Carpathian Pathways"
status: "living draft — every decision below marked open is open"
---

*Starting prompt for the Claude Project "Trans Carpathian
Pathway" and each conversation in it. Trans-Carpathian Pathways
is a project that runs on Plai, the Carpathian hub instance of
UBEC Mapservice. It does not own the stack; it is the first
project to ask Plai for things Plai does not yet do. Source
text: the proposal "Trans-Carpathian Pathways — Draft v0.1",
October 2026. Repository: `ubeccommon/trans_carpathian_pathways`;
the copy of this document in its `docs/` is the source of truth,
and the Project copy is replaced with it at each version.*

* * *

## 1. Load Order — Before Any Work

1. Attach and clone `ubeccommon/trans_carpathian_pathways` with
   push access, and `ubeccommon/ubec_mapservice` with read access
   only. `ubec_mapservice` is never written from a Pathways
   conversation unless Michel says so for a named change.
2. Read the latest version of this document in the repository's
   `docs/` fully.
3. Read, in the mapservice tree, the latest
   `docs/UBEC_MAPSERVICE_CLAUDE_PROMPT` §1, §2 and §4, and in §3
   the entries headed "The Carpathian hub and Plai", "The
   Carpathian hub as an instance" and "Plai's entry surface".
   Those bind Plai, and so bind this project. Where this
   document and the mapservice prompt disagree on anything about
   the stack, the mapservice prompt is right and this document
   is corrected.
4. Read `db/instances/plai/` and `mapbender/instances/plai/` —
   what a Plai point carries today.
5. Only then begin.

Pull before any edit to a document; the version you bump is the
one you pulled. Michel pushes to this repository from his own
clone too. When a session spans more than a day, re-clone and
re-read before acting on memory.

* * *

## 2. What This Project Is

A living network of hosts, a pathway that emerges from where
they are, and Curators who hold a stretch of it, across the
Carpathian arc. First corridor: the Hutsul highlands of western
Ukraine. Not a tourism platform, not a booking service, not a
product (proposal §9).

What this project builds is mostly not software. It is hosts
found, a Curator established, a corridor walked. Software is
built only where that work needs it, and on Plai, under
Mapservice's rule — work to need: a capability is built when an
instance requires it, not before.

**Where the work lives — Michel's word, October 7, 2026
(OI-P1).** This repository holds the project's documents, the
proposal and its build, and any Pathways tool. Plai migrations —
anything that changes what a Plai point carries — stay in
`ubec_mapservice`; this repository specifies them, it does not
hold them.

**Relation to Plai — Michel's word, October 7, 2026 (OI-P2):**
Pathways is a view of Plai's own entries, not an instance of its
own. A host is a Plai point whose category is lodging, meals,
guiding or learning; what Pathways needs beyond step A is added
to Plai by a Plai migration in `ubec_mapservice`; there is no
`pathways` database. One place for a host to enter, one consent
model, one curator queue.

What bore on it, read in mapservice at `edb1419` (prompt v0.64):
- Mapservice defines an instance as one initiative; Pathways is
  a project of the Carpathian Hub Initiative, whose instance is
  Plai.
- Every YAML application is private, and what people see is a
  copy made in Mapbender's backend whose security tab grants
  view to the public, logged-in users, groups or single users.
  So a Pathways map is a backend copy of Plai with its own
  audience, not a second instance.
- A separate instance would isolate less than it seems: one
  connections file holds write access to every instance's
  database (mapservice prompt §8, credential concentration).
- The wartime protection of a host's home is the published
  location rule (OI-P7), a gate in Plai's published view of the
  kind the contact fields already have — not a database
  boundary. (OI-P7 was then decided the same day: the exact
  point, as today. §5.)

The option not taken, for the record: (b), its own instance
`pathways` reading Plai at render time only, which would have
kept the list of private homes out of the database that holds
the range-wide open map.

**The user manual — Michel's word, October 8, 2026.** One manual
for entrants and curators, English and Ukrainian, built to one A4
PDF like the proposal, with Plai's emblem on its cover:
`docs/manual/`, built by `build/build_manual.py`. It is read
against Plai as it stands — the entries scheme v0.7, the curation
scheme v0.6, template 008's rules (mapservice `1c1c192`) — and
quotes every screen label in English, since Plai's screens are
English; the Ukrainian text glosses them. When a Plai form or
rule changes, the manual is checked against it and rebuilt. It
says what the stack cannot yet do: no password-reset mail (no
mailer is set), so a forgotten password goes to the administrator.
Manual v0.3 carries Michel's screenshots, taken on the host the
evening of October 8 with no test entry: the list of maps, the
login page, the toolbar, "My places" and the form in three parts,
cropped and kept in `docs/manual/img/` without their metadata, the
same pictures in both languages. They showed two things the text
had not said: required fields are outlined in red on screen, not
starred, and "Select by current extent only", ticked when the panel
opens, lists only the places in view. Still to come from him: the
curator's form, the public popup on a published place, and the
"State" list below the agreement.

**The co-creator agreement — Michel's word, October 8, 2026.**
One agreement for every role that builds the project — host,
pathway steward, Curator, traveler, contributor, partner
initiative, funder, and the administrator — English and
Ukrainian, built to one A4 PDF like the proposal:
`docs/agreement/`, built by `build/build_agreement.py`. It is a
draft for Michel's word, not for signing: items A-1 to A-7 are
open (who answers for the project, rights in entries, how payment
passes, a deputy administrator, governing law, retention, how
each role signs), and the cover and every footer say "Draft".
It follows the project review
(`docs/reviews/TRANS_CARPATHIAN_PATHWAYS_PROJECT_REVIEW_v0_1.md`),
whose §5 lists Claude's own proposals in the draft so none is read
as decided, and whose drifts and risks are not yet acted on.

**The agreement on every Plai entry — Michel's word, October 8,
2026.** Whoever creates a point ticks that they have read the
co-creator agreement and accept it, a link to it beside the tick.
His answers: build now and link draft v0.2; serve the PDF from
Mapservice, since this repository is private; record the tick,
the version and the time; purge the two rows of his host-fields
look first. Built in `ubec_mapservice` as `plai/004` (`064c34a`,
its prompt v0.80): `agreement_accepted` required, the version
from `instance.meta agreement_version` and the time given by the
database and kept on every save, none of it public; the entries
scheme v0.8; the PDF at `/ubec/agreement/`, its file named for its
version. Proven locally (`verify plai vt` 99 of 99), and on the
host the same afternoon after the look's two rows were purged:
`verify plai vt` 96 of 96, the leak pass 519 of 519, none skipped
(mapservice `bbc6a36`, its prompt v0.81). Left: Plai's user copy
made again and exported, and Michel's look as a throwaway entrant. A new version of the agreement on Plai is a new PDF
there, a new link in the scheme and a new `agreement_version` — a
Plai migration. The user manual v0.2 says what the entrant and
the curator see.

**The reasoning — Michel's word, October 9, 2026.** Why the
project exists and the reasons behind its principles, in
`docs/TRANS_CARPATHIAN_PATHWAYS_REASONING_v0_1.md`, English first,
Ukrainian once it settles. His direction, recorded there: the two
forces — the mountains re-valued from outside (tourism and
property, energy on the high meadows, EU accession, the Carpathian
Eight launched in Bukovel in September 2026, ageing holders) and
the people who keep them alive, newcomers among them; that a
community's spokesmen are asked who they speak for, this project
included ("no one speaks for a community"); and corridors of
cultural, natural and landscape stewardship that emerge from the
places and paths, grounded in spirituality and relationship, not
wilderness ("people and land are one and the same"). Twelve
tensions are set out there with what answers them and what is
open (T-1 to T-12), for Michel's word. Two bear on other
documents: T-10, the corridors cannot draw on a host's place while
the agreement's §5 says "for nothing else"; and the proposal that
its §5 become the one list of principles (project review D-6).

**The white paper — Michel's word, October 9, 2026.** A
comprehensive review of the project's documents and in-depth
background research, written as a white paper for readers outside
the project: `docs/whitepaper/`, English first, built to one A4 PDF
by `build/build_whitepaper.py` in the proposal's styles (24 pages,
81 numbered sources). Research in four strands the same day: the
region's pressures in figures (property, tourist tax, livestock,
displaced people, Svydovets, Runa, the C8 declaration's text,
accession and the Polish and Romanian land precedents); comparable
initiatives (Via Transilvanica, Via Dinarica, the Czech and Slovak
clubs, Bergsteigerdörfer, ADEPT, the Camino's donativo, Fairbnb)
with their lessons; the legal frame (Procedure 297 for hosting from
the home, the five-kilometre border strip and the 31st detachment's
order, advisories, data law in both jurisdictions, the tour-product
and package-travel definitions); and the theory (High Nature Value
grassland evidence, IUCN V, UNESCO's continuing landscape, ubuntu
and its critics, Ostrom, CARE, staged authenticity, elite capture).
Checked by a separate agent against the documents and the sources:
24 findings, all taken in — among them that the paper must not
present the draft agreement's proposals (no ratings, no commission,
money reported at each gate, no open licence) as decided, and that
Gate 1 is passed in fact but not yet closed in §8 (review D-1,
still open). Appendix A records that proposal v0.3 is due (D-2,
D-3, D-4, D-6). The legal strand's "needs a lawyer" list is in the
paper's §9 and bears on the two legal reads the agreement names.

**The stress tests — Michel's word, October 9, 2026.** Three,
each by a separate agent that had not seen the white paper
written: a sceptical funder (money over five years), a red-team
reviewer (adversaries and failures), an anthropologist of rural
development (capture and co-option). Recorded as delivered in
`docs/reviews/TRANS_CARPATHIAN_PATHWAYS_STRESS_TESTS_v0_1.md`,
with what they demand in common and 24 decisions for Michel
(S-1 to S-24) tied to the document each would change. The five
demands all three share: the Curator is assumed to stand between
the map and the door and nothing makes it so (host points public,
in their own colour, with the hosting details on the click — the
security tab of the Pathways copy is the unused lever, S-1); one
person holds everything and the agreement's promises fail for any
six weeks he is unreachable (A-1, A-4, the first Curator not the
lead, Mapbender's database not in the backup, S-9, S-11, S-12);
one lawful defined form of payment out of four and no cost-carrier
after the grant (S-2, S-3, S-16); a corridor speaks for its points,
never for a place (S-14, S-18); and hosts are promised a withdrawal
the map cannot keep once a point is copied, while the manual
contradicts the meeting-place option (S-4, S-14, S-22). One finding
was an inconsistency inside the white paper and is corrected in
its v0.2 (§12). Every other finding waits on Michel's word;
nothing is decided by the tests.

**Regeneration against sustainable development — Michel's word,
October 9, 2026.** Before the stress tests' decisions are taken
up, the regeneration approach is woven into the white paper and
set against sustainable development, which was applied where it
was convenient and neglected where it would bite: white paper
v0.3, a new §5 "From sustaining to regenerating" (Brundtland 1987;
the UN's 2025 finding that only 35% of the Goals' targets are on
track or progressing; the UNEP/UNWTO definition's four claimants
with the industry among them; Bukovel's own Sustainable Development
Office beside the Svydovets plan; Lyle, Reed's nested trajectory,
Mang & Reed, Gibbons), a table of question, unit and measure, and
three diagrams drawn by `build/diagrams_whitepaper.py` into
`docs/whitepaper/assets/` in both languages: where each approach
aims (a line from degenerating through zero to regenerating),
what each sees (three pillars to balance against a nested living
place), and two flows in the same mountains (the line of
extraction against the regenerative loop). The summary, §4.2, the
signs of success and the ask carry it; the regenerative test — is
the place more alive and more able to go on than before the
pathway — stands behind the signs. The paper's former §5–§12 are
now §6–§13; the stress-test review cites v0.1/v0.2 numbers.

**The white paper in Ukrainian — Michel's word, October 9, 2026.**
`Trans-Carpathian_Pathways_White_Paper_UK.md`, a translation of the
English v0.3 made the same day in seven parts against one glossary
drawn from the Ukrainian proposal and agreement (господар,
доглядач стежки, Куратор, мандрівник, угода співтворців, перехід,
внесок, регенерація, сталий розвиток, тяглий ландшафт, Карпатська
вісімка), checked for structure against the English — the same
17 sections, 29 subsections, 38 table rows, 169 paragraphs and
89 citations, the Ukrainian diagrams in place — and built into
the one PDF after the English (59 pages). Judgement calls the
translators flagged: stewardship → догляд (to match доглядач),
Lake Herashaska → озеро Герашаська, conviviality →
конвівіальність, draft agreement → проєкт угоди throughout.
Neither this text nor the diagram labels have yet been read by
anyone in the corridor; §12 of the paper says the Ukrainian should
in the end come from them.

**The site — Michel's word, October 9, 2026.** A presence on the
web at `tcp.ubec.network`, opened by its own conversation from
`docs/prompts/TCP_WEB_PRESENCE_START_PROMPT_v0_1.md`: a small,
bilingual, static site that says what the project is, carries the
documents as PDFs and pages, names how to take part, and links to
Plai and the field writing; never a map, a directory of hosts, a
booking page or a form. The UBEC mark, not the Plai emblem;
fonts served locally; no third-party request from any page.
The prompt binds the site to the stress tests — no host listed or
located (S-1), partners and declined requests (S-19), the stage
said plainly, no form (agreement §5) — and leaves to Gate A where
the site lives, who manages DNS and TLS for `ubec.network`, and
whether the vhost is a mapservice change. Serving the white paper
from Mapservice, left open the same morning, is answered if the
site publishes it. The decisions S-1 to S-24 still wait — Michel's word, October 9:
they will be taken later; the questions are listed one per line
in `docs/DECISIONS_CHECKLIST_v0_1.md`, with the agreement's
A-items and the review's drifts still due.

**The site, Gate A — Michel's word, October 9, 2026.** The site is
the project's, apart from the map service: its source, its build
(`build/build_site.py`) and its nginx vhost are in this repository's
`site/`, and nothing is changed in `ubec_mapservice` for it. It links
to the map service. It is served from `/var/www/tcp.ubec.network` on
ubec-common, with an A/AAAA record for `tcp` pointing at that host.
For now it is one landing page, in English and Ukrainian, with a
vision and a mission statement. Those are drafted from the white paper
v0.3 and the proposal v0.2 and wait on his word. What was found and
what is still open — the documents on the site, pictures, partners
(S-19), the access log and indexing, both of which are in place as
Claude's proposals — is recorded in `site/README.md`.

**Michel's answers to the decisions checklist — October 9, 2026.**
Carried into agreement v0.3, proposal v0.3 and manual v0.4 (both
languages, PDFs rebuilt) and recorded in `docs/DECISIONS_CHECKLIST_v0_2.md`
with what stays open. Decided:
- **S-1** — host points are public during the pilot, and the
  public may click them; a traveler need not contact the Curator
  before visiting. The Curator is not a gatekeeper. (§4, §7.)
- **S-11 / A-1** — Michel personally for now; a core body is to be
  formed in the near future and will hold the Plai instance, the
  marks and the controller role.
- **S-12 / A-4** — there is no second person today; Michel holds
  both roles; the core body decides the deputy. The stewardship
  mailbox must be verified to reach the deputy once named.
- **S-9** — the first Curator is Michel for now, named before the
  first hosts; the core body decides thereafter, and later
  Curators are named by all co-creators.
- **S-2 / A-3 / OI-P13** — payment passes directly from traveler to
  host. Closed.
- **S-3 / OI-P8** — ubec-pay kept among the four forms and defined
  in one paragraph (agreement §8; Claude's wording for his word).
- **S-16** — a contribution defined in one paragraph (agreement
  §8; Claude's wording); Curators and stewards are paid roles,
  terms decided once a financing plan is secured.
- **S-21** — a budget recommendation and a pilot length in
  proposal v0.3 (eighteen months, about €25,700; Claude's for his
  word).
- **S-4 / OI-P7** — the Curator proposes nothing; a host may place
  the point at a nearby meeting place and must then say so in
  the place's own information.
- **S-14** — the agreement and the sign-on sheet say withdrawal
  removes a point from Plai, not from copies; a separate,
  revocable consent for the use of a place in any submission to a
  public body; corridors as fuzzy bands, never parcels; a corridor
  is **not** presented with a count of consents against residents.
- **S-22** — no guidance against surnames in a place's name.
- **S-6** — no fixed ceiling; the Curator keeps an overview of the
  carrying capacity of each host, each stretch and the pathway.
- **S-17** — a hold beyond 30 days carries a written reason.
- **S-5 / OI-P12** — travelers from abroad are responsible for
  their own preparation and are told so in the agreement's
  traveler part. Closed.
- **S-8** — no stage inside the border strip is suggested to
  anyone until the permit route is held in writing and done once;
  a stage register, one sheet per stage.
- **S-15** — Plai holds no confidential information.
- **S-13 / S-20** — a minimal incident record kept by the Curator
  and the deputy, retention under A-6; a traveler's identity is
  not seen before a journey.
- **S-18** — the first corridor's co-creators decide Phase 2
  governance; the first corridor gets a partnership note of its
  own.
- **S-19** — a public list of partners from the start.
- **S-23** — done in `ubec_mapservice` the same day (its commit
  `0a5aa99`, prompt v0.82, README v0.43): Mapbender's own database
  in the backup (`backup.py` v0.8, a `mapbender` target with a
  whole restore, proven on a throwaway cluster); abuse control on
  the public face (vhost v0.5: its own log directory, a short
  format, seven-day rotation, three request thresholds answered
  with 429). The third change fell with S-1. And the agreement at
  draft v0.3 on Plai: the PDF served beside v0.2, the entries
  scheme v0.9, `plai/005` setting `agreement_version` to `v0.3`.
  **On the host the same midday, Michel's run** (mapservice prompt
  v0.84): `005` applied; `verify plai vt` 96 of 96, the agreement
  checks proving `v0.3`; the vhost installed with its log directory
  and rotation, the leak pass 519 of 519; `backup.py prove` 15 of
  15 with the first dump of Mapbender's database; the user copy
  made again; the form's link opening the v0.3 PDF. Closed on his
  "looks good". What F5 still asks — a timer, encryption, an
  off-host copy — is not built, and Gate 3 waits on the last.
- **S-24** — the white paper stays a draft; no v0.4 now.
- **A-7** — hosts sign on paper with the Curator, in Ukrainian.
- **D-1** — Gate 1 closed (§8). **D-2, D-3, D-4, D-6** — proposal
  v0.3.
Still open, with Michel's answer read as far as it goes: S-10
(when Phase 1 ends — the three options restated, none chosen);
S-17's second number (review by another after how many days) and
the kin question, which he asked to have explained; S-18's
entrenched clauses; S-19's "Part I in full, §3 included" for
partners; S-14's hromada-council step; OI-P11 (the proposal's
seven or Plai's nine, both named); S-7 (what Gate 4 records — to be
defined); A-2 (read as the drafted option, to confirm); A-5; A-6.

**Partners — Michel's word, October 9, 2026.** The search for
those who would fund, help build, help run and scientifically
report the first corridor's prototype opens in its own
conversation from `docs/prompts/TCP_PARTNERS_START_PROMPT_v0_1.md`:
four kinds of partner (funders, creators, implementers, scientific
reporters), four gates (the needs, a sourced long list, a short
list with each one's fit and conditions, the material to approach
them with — a bilingual prototype brief and a study sketch), its
documents in `docs/partners/`. It explores and commits nothing;
every approach is Michel's. The prototype it serves is the pilot
as proposal v0.3 sets it out, measured by whether the co-creators
could do their part and wanted to go on.

**Partners, Gates A and B — Michel's word, October 9, 2026.** The
needs (`docs/partners/NEEDS_v0_2.md`): nine with a cost line, five
without. Michel's additions: the concept is being tested now on a
short stretch between two places he named, kept unnamed in the
documents since either may be a host's place; his two candidates,
Änderwerk gGmbH (a Berlin fiscal host) and the NGO Alliance of
Development (Verkhovyna district); and "everything is open" — none
of the partners prompt's §5 items decided. The long list
(`docs/partners/LONG_LIST_v0_1.md`, now v0.2): a review of the project as a
partner would read it, and thirty-nine candidates across the four
kinds, sourced and dated, for him to strike and add. What it found:
the grantee holds back fifteen of the thirty-nine; no fund or grant
instrument was found in the Carpathian Convention or the C8; a "plai" route of
twelve QR stops already runs in Verkhovyna, led by Alliance of
Development; a partner profile of Verkhovynskyi National Park lists
keeping meadows by horse grazing; the oblast tourism office and the green tourism union ask
for what the project refuses. Open, from the review: whether the
test enters anyone's place on Plai, which would bring Gate 3's
backup condition with it; what the test records (S-7).

**The project in modules — Michel's question, October 9, 2026.**
Should the project be one comprehensive whole of building blocks
and the blocks that connect them? Claude's answer, for his word, in
`docs/TRANS_CARPATHIAN_PATHWAYS_MODULES_v0_1.md`: yes, as a map and
not as a plan — a spine (relationship, spirituality, regeneration,
and the regenerative test), four blocks (the corridor, heritage,
infrastructure, the commons) and twelve modules, each active, named
or later, with the long list's candidates as their possible holders;
the standards kept in the connectors between modules. A module opens
only when a gate needs it and someone holds it. The precedent, from
Michel's link stezhky.org: the society *Plai*, Lviv 1924, which
joined regional studies, nature protection, trail marking and the
first Ukrainian mountain shelter (Plisce, 1933–35). The same review
rewrote the long list's trail-marking entry (v0.2).

**The modules, adopted — Michel's word, October 9, 2026.** All six
points of the module map, as proposed (`docs/TRANS_CARPATHIAN_PATHWAYS_MODULES_v0_2.md`):
the four blocks and twelve modules are how the project describes
itself; active now P1, P2, P3, T1, T2, G1, T3 and T4, and named H1,
H2, G2, G3 — a named module opens on a gate's need and a holder, on his
word; relationship, spirituality and regeneration stay the spine;
marking is settled at Gate 4 (§8); the standards — a BCP 47 language
tag in every document, page, PDF and diagram, WCAG 2.2 AA for the site,
ISO 19115 with an INSPIRE-compatible profile only for a layer published
for others, CARE for the people in any study and FAIR for the data that
may be open; and the society *Plai* of 1924 named in the white paper as
the name's precedent. Done the same day: white paper v0.4 in both
languages, its S-24 "no v0.4 now" superseded for this change; the four
PDF builds and the two diagram builds tag their language, all rebuilt;
the site's stylesheet v0.4 and build v0.4 meet and check WCAG 2.2 AA,
what only a person can check listed in `site/README.md` v0.7. The
repository's own README has no front matter and stays English.

**The Appalachian Trail — Michel's word, October 9, 2026.** Added to
the white paper's §7 as the eighth case, in both languages (white
paper v0.5, PDF rebuilt, 60 pages): MacKaye's 1921 proposal of a trail
with shelter, community and farm camps on land held in common, of
which only the trail was built; the federation of some thirty
maintaining clubs, each with its section, under the Appalachian Trail
Conservancy and the National Park Service; and the corridor bought
under the 1968 and 1978 acts against landowners' resistance, compulsory
purchase made a last resort. Three rows in the lessons table: keep the
living part of the vision, a federation of section-keepers, a corridor
from consent. Sources 91–93.

**Open data for travelers' apps — Michel's question, October 9,
2026.** Can travelers carry Plai's places and the pathways into
their own apps (Organic Maps and others), and which standards? The
specification, for his word: `docs/specs/PATHWAYS_OPEN_DATA_SPEC_v0_1.md`.
Three kinds of data: the pathway (OSM-derived, ODbL) and places
nobody hosts travel openly — OpenStreetMap by survey, stage files in
GPX 1.1, GeoJSON (RFC 7946) and KML 2.3, an OGC API – Features
service for partners when one asks; hosts travel one at a time, by a
`geo:` link (RFC 5870) in the map's click, or in one traveler's
journey file from the Curator — never in bulk, never in OSM, never
in the API. Six decisions open (D-1 to D-6), among them OI-P10.

* * *

## 3. The First Corridor

**The order — Michel's word, October 7, 2026 (OI-P3):**
Vorokhta → Verkhovyna → Kosiv — down from the mountain gateway,
through high-pasture country, to the craft centre and its
market, without doubling back. (The first draft's order,
Vorokhta → Kosiv → Verkhovyna, not taken.)

Straight-line distances between town centres (approximate
coordinates, great circle — the walked distance will be longer,
measured on the walk, not here):

| Leg                    | Straight line |
|------------------------|---------------|
| Vorokhta → Verkhovyna  | about 24 km   |
| Verkhovyna → Kosiv     | about 27 km   |
| Vorokhta → Kosiv       | about 39 km   |

So the corridor is some 50 km as the crow flies in the
recommended order, which on paths is plausibly a walk of four to
six days — the Curator and the walk set the real figure.
Intermediate villages are candidate nodes, found as hosts are
found, not assigned in advance.

Before any stage is published:
- Check border-zone rules for any stage near the Romanian
  border (the Chornohora ridge); a stage that needs a permit
  says so.
- Each overnight host has a stated nearest shelter during
  air-raid alerts, held by the Curator, not published.

* * *

## 4. Roles, and How They Meet Plai's Accounts

| Role            | Does                                   | Plai                      |
|-----------------|----------------------------------------|---------------------------|
| Host            | enters their own place, or has it entered | `PLAI_ENTRANT`, or none |
| Pathway steward | cares for a stretch; enters for a host, adds places along the way | `PLAI_STEWARD` |
| Curator         | publishes or holds; also enters        | `PLAI_CURATOR` and `PLAI_ENTRANT` |
| Traveler        | sees published points; may go directly | no account                |

**The Curator is not a gatekeeper — Michel's word, October 9,
2026 (S-1):** host points are public and clickable during the
pilot; a traveler may ask the Curator for a journey or find a
published host and go directly. Every Curator duty towards
travelers in the agreement applies to those who come through the
Curator. The first Curator is Michel, named before the first hosts;
the core body, once formed, decides thereafter, and later Curators
are named by all co-creators (S-9). Curators and stewards are paid
roles, their terms decided once a financing plan is secured
(S-16).

**The pathway steward — Michel's word, October 8, 2026:** a new
role, someone who cares for a stretch of pathway and may add for
a host and add places along the way. On Plai a steward is an
entrant: the group means "may enter", not "is a host"; what a
steward enters is their row, under their name, as when the
Curator enters for a host (above). The stretch a steward cares
for is the project's knowledge, not a column. The Curator keeps
the whole: publishing, and the living map of who can receive
whom. The proposal's "become a Curator and hold a stretch" line
moves to the steward in its next version.

Accounts are made by the administrator in Mapbender's backend,
and Mapbender 5.0.0-RC2 requires an email on every account.

**A host who does not enter alone — Michel's word, October 7,
2026 (OI-P4):** the host has their own account and the Curator
sits beside them while they enter. The host owns their row and
edits or withdraws it themselves; the Curator stays a curator and
never creates. No Plai change follows from it.

What it carries, from the stack as it stands:
- Every host account is made by the administrator in Mapbender's
  backend, in `PLAI_ENTRANT`, with a unique email (Mapbender
  5.0.0-RC2 requires one). A host without an email needs one
  before they can be entered.
- Each host is a login, and a login is a trace (Mapservice §4,
  minimal accounts).
- Real accounts wait for Mapservice's own condition: backups
  before any real account, the off-host copy on Michel's
  computer.

**Amended — Michel's word, October 8, 2026:** the Curator also
enters points — for a host who cannot, and for places along the
way (a viewpoint, a spring). No change to Plai: the Curator's
Mapbender account is put in `PLAI_ENTRANT` as well as
`PLAI_CURATOR` (or in `PLAI_ADMIN`, which the application treats
as both), so both schemes show; what it creates goes through the
entry role under the Curator's name, and the database rule that
the curator role never creates stands. Such a point is the
Curator's row — the host cannot edit or withdraw it themselves,
their consent is on paper and the `data_consent` tick is the
Curator's on their behalf; a hand-over of ownership would be a
Plai migration (option (c) below), not yet asked for.

The option not taken, for the record: (c) a Plai migration adding
"entered on behalf of" and a later hand-over of ownership.

* * *

## 5. What a Host Carries — the Gap Against Plai Steps A and B

The proposal's five offers against Plai's category list
(`db/instances/plai/001_entry_fields.sql`):

| Proposal offer   | Plai category           | Fit                     |
|------------------|-------------------------|-------------------------|
| Overnight stay   | `lodging`               | yes                     |
| A meal           | `meals`                 | yes                     |
| Local guidance   | `guiding`               | yes                     |
| A workshop       | `learning`, `crafts`    | yes — two codes         |
| A view           | —                       | no: a view is a place, not an offer |

**A view — Michel's word, October 7, 2026 (OI-P5):** a new
location type `viewpoint`, "Viewpoint", in Plai's list, that
anyone or the Curator may map; not a host offer.

**What a host point carries — Michel's word, October 7, 2026
(OI-P6):** one point with a list of offers, not a point per
offer — one place, one consent set, one photo. And four fields
beside it, all of them:

- **Season** — the months open. Day-to-day availability stays
  with the Curator, never a calendar; a calendar is the first
  step to a booking service.
- **Capacity** — beds; people at a meal, a walk, a workshop.
  Small whole numbers.
- **Languages the host speaks** — a closed list.
- **Access** — reachable on foot only, by car, with a pram, with
  a wheelchair. Feeds the family-with-small-children journey.

Plai's step B (one photo per place, cleaned of metadata, mapservice
`plai/002`) was built and run on the host the same day, so images
are no longer a Pathways need. What these decisions ask of Plai is
specified in `docs/specs/PLAI_HOST_FIELDS_SPEC`; it is built in
`ubec_mapservice` as a Plai migration, not here.

**How a host is paid — Michel's word, October 7, 2026 (OI-P8):**
four forms, all of them: a fixed contribution, a suggested
contribution, exchange of work, and `ubec-pay` or a community
currency. Gift, the fifth form named in v0.1, was not among
them. Who chooses among the four — Michel's word, October 7,
2026 (OI-P13, first half): the host, per offer, so each offer on
a point says which forms the host accepts. OI-P13's second half closed —
Michel's word, October 9, 2026: payment passes directly from
traveler to host; the project, its Curators and its stewards hold
no money for stays and take no share (agreement §8).

**Published location of a private home — Michel's word,
October 7, 2026 (OI-P7):** the exact point, as today. Plai's
precision is free and a published point is the point entered,
for a home as for any other place; nothing in Plai changes. The
host decides where they place the point, the Curator decides
whether the entry is published, and the contact fields stay
gated by `consent_C` and `show_C` as step A built them.

Said before the decision and kept for the record: for a host's
home, published exactly, in wartime, with a name on it, the
point is an address.

The options not taken: a generalised point always published for
a home, the exact one passed through the Curator; and the host
deciding, generalised by default, through a consent and show
pair on the geometry.

The outward proposal said otherwise ("A home is not a public
pin"); proposal v0.2, October 7, corrects it in both languages.

**Amended — Michel's word, October 9, 2026 (S-4):** the Curator
proposes nothing about where a point goes. A host may place the
point at a nearby meeting place instead of the house, and must
then say so plainly in the place's own information (the
description), so a traveler knows the point is not the house.
Nothing in Plai changes; the manual v0.4 and the agreement v0.3
say it. And the host is told, in the agreement and on the sign-on
sheet, that a published point may be copied and that withdrawal
removes it from Plai, not from copies (S-14).

**ubec-pay — Michel's word, October 9, 2026 (S-3):** kept among
the four forms and defined in one paragraph in agreement §8 — a
settlement in a community currency or in a mutual-credit account
UBEC keeps for its commons, not money; the project runs no payment
system; the hryvnia the only legal tender; the wording Claude's,
for his word. **A contribution is not a price** is defined beside
it (S-16), the wording likewise Claude's.

* * *

## 6. The Stage Planner (the proposal's "spatial algorithm")

Specified here, not built. Built only when the first corridor
has enough hosts to need it — with five hosts, the Curator plans
on paper.

**What it is for:** the Curator. It proposes; the Curator
disposes. It never answers a traveler directly.

**Input**
- Published host points with their offers, season, capacity,
  languages, access.
- The path network: OpenStreetMap footways, paths and tracks in
  `reference_sa.osm_line` (Plai's base map, already loaded).
- Terrain: a DEM for ascent and descent (source and licence to
  be recorded at load — OI-P9).
- The request: start, end or loop; days; party (family, solo,
  couple, group); mode (walk, cycle, drive); month.

**Edge cost — walking:** DIN 33466 hiking time: 4 km/h on the
flat, 300 m/h ascent, 500 m/h descent; segment time = the larger
of the horizontal and vertical times plus half the smaller.
Family and group profiles scale it; the Curator sets the scale.

**Constraint, not optimisation:** each day ends at a host with an
overnight offer, open that month, with capacity for the party;
each day stays under the party's limit in hours and ascent. Among
plans that satisfy that, prefer more distinct encounters (a meal,
a workshop, a viewpoint passed) over less time — "the logic of
encounter, not just efficiency". Output: two or three candidate
stage plans with times, ascent and the hosts met, for the
Curator to change.

**Licence (OI-P10).** A route drawn from OpenStreetMap is a work
derived from an ODbL source. Mapservice's rule: segregate data
is combined at render time and never joined into a project's
tables. So either the planner computes on request and stores
nothing, or a stored route line lives in `instance_sa.*` and is
published under ODbL. Decide before the first route is saved.

**Where it runs.** The stack's image (`postgis/postgis:18-3.6`)
has no pgRouting. Default proposal: a Python tool, in the
mapservice tool style, that reads a corridor's paths and hosts,
builds the graph in memory (networkx), and writes nothing but its
answer. Adding pgRouting to the image is a framework change and
Mapservice's to decide. If built, the tool lives in this
repository's `tools/`.

* * *

## 7. Principles — Operational

From the proposal §8, binding:

- **Honest offer** — hosts offer only what they actually have.
- **No performance** — the encounter is real or it is nothing.
- **Organic growth** — the network grows from the inside out.
- **Curator as memory** — the human holds what the algorithm
  cannot; the planner is the Curator's tool.
- **The traveler arrives** — the journey is undergone, not
  consumed.
- **Off the beaten path** — where people live, not where tourists
  are sent.
- **A pathway of relationships** — human to human, human to
  nature.

Inherited from Mapservice and binding here: one instance, one
database; no secrets in any repository; consent and publication
as columns; minimal accounts; exposure is a decision; licence
recorded at use.

Added here:

- **A home is published at the point entered** (OI-P7): the
  host places it, the Curator publishes or holds the entry.
- **No calendar.** Availability beyond season stays a
  conversation with the Curator.
- **Safety is the Curator's to hold**, not the traveler's to
  find: shelter, the state of each stage, alerts — off the
  platform. **Plai holds no confidential information** (Michel's
  word, October 9, 2026, S-15). The border-zone rules are public
  law and are told to every traveler in writing.
- **The Curator is not a gatekeeper** (Michel's word, October 9,
  2026, S-1): travelers may find a published host and go
  directly; travelers are responsible for their own preparation
  (S-5).
- **No one speaks for a community** and **Not wilderness**
  (Michel's direction, October 9, 2026; reasoning §5), now in the
  proposal's and the agreement's lists too (D-6).

* * *

## 8. Gates — Phase 1

Gate-by-gate: a gate opens on Michel's word, not on a date.

- **Gate 0 — Decisions.** OI-P1 to OI-P8 answered or explicitly
  deferred. All eight answered on Michel's word, October 7, 2026.
- **Gate 1 — Plai in a browser.** Michel's look as a throwaway
  entrant and curator. **Closed October 8, 2026, on Michel's
  word**: the browser look recorded under Gate 2 was that look — a
  Digitizer save worked as entrant and as curator (review D-1;
  recorded here October 9).
- **Gate 2 — Host fields.** One Plai migration, `plai/003`, for
  what `docs/specs/PLAI_HOST_FIELDS_SPEC` says (OI-P5, OI-P6,
  OI-P13, Q1 to Q8), with `verify` and the leak pass extended to
  the new fields and hosts drawn as a style on the entry layer.
  The published location stays the point entered (OI-P7).
  **Built October 7, 2026, on Michel's word** — mapservice
  `a386165`, proven locally (spec v0.4); on the host the same
  day, verify 91 of 91, the leak pass 519 of 519. **Closed
  October 8, 2026, on Michel's word**, after his look in a
  browser: a place entered and published, a workshop host with a
  capacity and three languages published and drawn in ochre to
  the public, the click carrying every host field. The look found
  two faults older than `003` and fixed in mapservice the same
  morning — every scheme had listed its `fields` without `id`
  since step A, so a publish was refused and an edit inserted a
  second row (`e203e3f`); and `PLAI_STEWARD` became a group of its
  own (`727aeec`). Mapservice at `d0456b4`, prompt v0.72.
  **Gate 2 closes before Gate 3 opens, as a hard constraint**
  (state review v0.1, F-3): Mapservice's proofs refuse or skip an
  instance that holds entries and no throwaway carries Plai's own
  migrations, so `003` can only be proven while Plai is empty.
- **Gate 3 — First hosts.** Three to five hosts in the corridor,
  entered by the route OI-P4 chose, one Curator named. Opens only
  after Mapservice's own condition on real accounts is met —
  backups with an off-host copy, which nothing in that tree yet
  implements (its review's F5; state review v0.1 §2).
- **Gate 4 — First walk.** The corridor walked end to end. What
  is recorded: walked distance and time per stage, what was
  missing, what a traveler needed and did not have. And settled
  here, after the walk (Michel's word, October 9, 2026): whether
  the pathway is marked, and to which standard.
- **Gate 5 — Planner, if needed.** Built only if Gate 4 shows the
  Curator needs it, against the stages actually walked as its
  test cases.

* * *

## 9. Open Items

- **OI-P1** — Closed, Michel's word, October 7, 2026: the
  repository `ubeccommon/trans_carpathian_pathways` for
  documents, the proposal build and tools; Plai migrations stay
  in `ubec_mapservice`. §2.
- **OI-P2** — Closed, Michel's word, October 7, 2026: a view of
  Plai's entries, fields by Plai migration, a Pathways map as a
  backend copy of Plai. §2.
- **OI-P3** — Closed, Michel's word, October 7, 2026: Vorokhta →
  Verkhovyna → Kosiv. §3.
- **OI-P4** — Closed, Michel's word, October 7, 2026: the host's
  own account, the Curator beside them while they enter; amended
  October 8: the Curator also enters, for a host who cannot and
  for places along the way, from an account in both groups. §4.
- **OI-P5** — Closed, Michel's word, October 7, 2026: location
  type `viewpoint`. §5.
- **OI-P6** — Closed, Michel's word, October 7, 2026: one point
  with a list of offers; season, capacity, languages, access.
  §5.
- **OI-P7** — Closed, Michel's word, October 7, 2026: the exact
  point, as today. §5.
- **OI-P8** — Closed, Michel's word, October 7, 2026: fixed
  contribution, suggested contribution, exchange of work, and
  `ubec-pay` or a community currency. §5.
- **OI-P9** — DEM source and licence, at Gate 5 only.
- **OI-P10** — Route licence: computed and unstored, or stored
  under ODbL in `instance_sa`. §6.
- **OI-P11** — The Phase 3 country list: the proposal names seven
  countries; the Outlook boundary that sets Plai's extent
  reaches nine, Austria and Bulgaria included (mapservice
  prompt §3).
- **OI-P12** — Closed, Michel's word, October 9, 2026: a traveler
  from abroad is responsible for their own preparation and travel
  and informs themselves, in their own country, about advisories,
  insurance, martial law, cash and permits; the agreement's
  traveler part says so, and the Curator repeats it to those who
  come through them.
- **OI-P15** — Closed, Michel's word, October 8, 2026:
  `PLAI_STEWARD` is a group of its own. Built in mapservice
  `727aeec` (`instance.py entry-groups`, application template
  v0.20, Plai's entries scheme v0.5); on the host: `entry-groups
  plai STEWARD`, `render`, `cache:clear`, the group made in the
  backend. §4.
- **OI-P14** — A place nobody hosts (a viewpoint, a spring,
  entered by the Curator) still needs a `category` and a contact
  email, as every Plai point does since `plai/001`. For the pilot:
  "Something else" and the Curator's email. Whether such a place
  should need neither is a Plai change (`plai/004`), on Michel's
  word.
- **OI-P13** — Closed. First half, Michel's word, October 7, 2026:
  the host chooses, per offer. Second half, Michel's word,
  October 9, 2026: payment passes directly from traveler to host.
  §5.

* * *

*Changelog*
- v0.37 — 2026-10-09 — the open-data specification v0.1 recorded.
- v0.36 — 2026-10-09 — the Appalachian Trail in the white paper, v0.5.
- v0.35 — 2026-10-09 — the module map adopted, all six points;
  white paper v0.4; language tags and WCAG 2.2 AA implemented.
- v0.34 — 2026-10-09 — the module map v0.1 on Michel's question;
  stezhky.org reviewed; long list v0.2.
- v0.33 — 2026-10-09 — partners Gates A and B recorded: the needs
  v0.2 with Michel's additions, the test stretch, the long list.
- v0.32 — 2026-10-09 — the starting prompt for the partners
  conversation recorded.
- v0.31 — 2026-10-09 — S-23 and the agreement v0.3 closed on the
  host, Michel's "looks good".
- v0.30 — 2026-10-09 — S-23 and the agreement v0.3 built in
  mapservice (`0a5aa99`); what remains to run on the host.
- v0.29 — 2026-10-09 — Michel's answers to the decisions checklist
  carried into agreement v0.3, proposal v0.3, manual v0.4; Gate 1
  closed; OI-P12 and OI-P13 closed; OI-P7 and OI-P8 amended; what
  stays open listed.
- v0.28 — 2026-10-09 — the site's Gate A on Michel's word: in this
  repository, apart from the map service; a landing page with vision
  and mission (`site/`).
- v0.27 — 2026-10-09 — the decisions checklist recorded; S-1 to
  S-24 wait on Michel's word, later.
- v0.26 — 2026-10-09 — the starting prompt for the site at
  `tcp.ubec.network` recorded.
- v0.25 — 2026-10-09 — the white paper in Ukrainian; one PDF in
  both languages.
- v0.24 — 2026-10-09 — white paper v0.3: regeneration woven in and
  set against sustainable development, three diagrams in both
  languages; sections renumbered.
- v0.23 — 2026-10-09 — three stress tests recorded, 24 decisions
  put to Michel (S-1 to S-24); white paper v0.2 corrects its §12.
- v0.22 — 2026-10-09 — the white paper v0.1, Michel's word:
  documents reviewed, four research strands, 24-page PDF, checked
  by a separate agent.
- v0.21 — 2026-10-09 — the reasoning document v0.1, Michel's word:
  why now, corridors of stewardship, the principles with their
  reasons, tensions T-1 to T-12.
- v0.20 — 2026-10-08 — manual v0.3: Michel's screenshots in both
  languages; three more wanted.
- v0.19 — 2026-10-08 — `plai/004` on the host: verify 96 of 96,
  the leak pass 519 of 519.
- v0.18 — 2026-10-08 — the agreement on every Plai entry,
  Michel's word: mapservice `plai/004` (`064c34a`); manual v0.2.
- v0.17 — 2026-10-08 — the co-creator agreement, Michel's word:
  every role, English and Ukrainian, one PDF in `docs/agreement/`,
  a draft with A-1 to A-7 open; the project review v0.1 recorded.
- v0.16 — 2026-10-08 — the user manual, Michel's word: entrants
  and curators, bilingual PDF in `docs/manual/`, Plai's emblem on
  the cover.
- v0.15 — 2026-10-08 — Gate 2 closed on Michel's word after the
  browser look; what the look found recorded; spec v0.5.
- v0.14 — 2026-10-08 — OI-P15 closed on Michel's word:
  `PLAI_STEWARD` a group of its own, built in mapservice `727aeec`.
- v0.13 — 2026-10-08 — the pathway steward, Michel's word: a new
  role, an entrant on Plai; the roles table rewritten; OI-P15
  opened for a group of its own.
- v0.12 — 2026-10-08 — OI-P4 amended on Michel's word: the
  Curator also enters points, from an account in both groups;
  OI-P14 opened, the shape of a place nobody hosts.
- v0.11 — 2026-10-07 — Gate 2 built on Michel's word (mapservice
  `a386165`, spec v0.4); closes on his host run and browser look.
- v0.10 — 2026-10-07 — the mapservice state review
  (`docs/reviews/UBEC_MAPSERVICE_STATE_REVIEW_v0_1.md`) read and
  its findings applied on Michel's word in spec v0.3: hosts a
  style on the entry layer (Q4), `category` beside `offers` (Q7),
  `reach` for `access` (Q8). Gate 2 before Gate 3 recorded as a
  hard constraint; Gate 3 waits on Mapservice's backup condition.
- v0.9 — 2026-10-07 — the proposal's contrary line on a home
  recorded as corrected (proposal v0.2).
- v0.8 — 2026-10-07 — OI-P3 closed on Michel's word: Vorokhta →
  Verkhovyna → Kosiv. Gate 0's eight items all answered. The
  host-fields specification settled at v0.2 but for its Q4.
- v0.7 — 2026-10-07 — OI-P5 and OI-P6 closed and OI-P13's first
  half, on Michel's word: `viewpoint` a location type; one point
  with a list of offers; season, capacity, languages, access; the
  host chooses payment forms per offer. Plai's step B (photo)
  recorded as built (mapservice `b9edde4`, prompt v0.66). The
  host fields go to `docs/specs/PLAI_HOST_FIELDS_SPEC`.
- v0.6 — 2026-10-07 — OI-P8 closed on Michel's word: four forms
  of payment, gift not among them; OI-P13 opened for who chooses
  among them and how payment passes. Gate 0's four blocking
  items are answered.
- v0.5 — 2026-10-07 — OI-P7 closed on Michel's word: a home is
  published at the point entered, as today; the principle "not a
  map pin by default" replaced; Gate 2 no longer carries a
  location rule; the proposal's contrary line flagged.
- v0.4 — 2026-10-07 — OI-P4 closed on Michel's word: each host
  has their own account and enters with the Curator beside them;
  what follows from Plai's accounts recorded.
- v0.3 — 2026-10-07 — OI-P2 closed on Michel's word: Pathways is
  a view of Plai, not its own instance; what bore on it recorded
  from mapservice `edb1419` (prompt v0.64), including the
  per-application viewing rights that give a Pathways map its
  own audience.
- v0.2 — 2026-10-07 — moved into the repository, whose copy is
  now the source of truth; OI-P1 closed on Michel's word (this
  repository; Plai migrations stay in `ubec_mapservice`); load
  order clones both repositories, mapservice read-only; a
  planner, if built, goes in `tools/`. Read against mapservice
  commit `30e6b48` (its prompt v0.62).
- v0.1 — 2026-10-07 — initial, from proposal Draft v0.1 and
  Plai at mapservice commit `7a5ce95` (entry surface step A).
