---
title: "TRANS_CARPATHIAN_PATHWAYS_CLAUDE_PROMPT_v0_64"
subtitle: "Starting Prompt — Trans-Carpathian Pathways on Plai"
author: "Michel Garand"
date: "October 2026"
version: "v0.64"
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
pathway steward, Curator, pilgrim, contributor, partner
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
`docs/TRANS_CARPATHIAN_PATHWAYS_REASONING_v0_4.md`, English first,
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
доглядач стежки, Куратор, мандрівник (since October 10,
прочанин плаю), угода співтворців, перехід,
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
`docs/prompts/TCP_WEB_PRESENCE_START_PROMPT_v0_2.md`: a small,
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
  public may click them; a pilgrim need not contact the Curator
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
- **S-2 / A-3 / OI-P13** — payment passes directly from pilgrim to
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
- **S-5 / OI-P12** — pilgrims from abroad are responsible for
  their own preparation and are told so in the agreement's
  pilgrim part. Closed.
- **S-8** — no stage inside the border strip is suggested to
  anyone until the permit route is held in writing and done once;
  a stage register, one sheet per stage.
- **S-15** — Plai holds no confidential information.
- **S-13 / S-20** — a minimal incident record kept by the Curator
  and the deputy, retention under A-6; a pilgrim's identity is
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
conversation from `docs/prompts/TCP_PARTNERS_START_PROMPT_v0_2.md`:
four kinds of partner (funders, creators, implementers, scientific
reporters), four gates (the needs, a sourced long list, a short
list with each one's fit and conditions, the material to approach
them with — a bilingual prototype brief and a study sketch), its
documents in `docs/partners/`. It explores and commits nothing;
every approach is Michel's. The prototype it serves is the pilot
as proposal v0.3 sets it out, measured by whether the co-creators
could do their part and wanted to go on.

**Partners, Gates A and B — Michel's word, October 9, 2026.** The
needs (`docs/partners/NEEDS_v0_3.md`): nine with a cost line, five
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
points of the module map, as proposed (`docs/TRANS_CARPATHIAN_PATHWAYS_MODULES_v0_3.md`):
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

**Open data for pilgrims' apps — Michel's question, October 9,
2026.** Can pilgrims carry Plai's places and the pathways into
their own apps (Organic Maps and others), and which standards? The
specification, for his word: `docs/specs/PATHWAYS_OPEN_DATA_SPEC_v0_3.md`.
Three kinds of data: the pathway (OSM-derived, ODbL) and places
nobody hosts travel openly — OpenStreetMap by survey, stage files in
GPX 1.1, GeoJSON (RFC 7946) and KML 2.3, an OGC API – Features
service for partners when one asks; hosts travel one at a time, by a
`geo:` link (RFC 5870) in the map's click, or in one pilgrim's
journey file from the Curator — never in bulk, never in OSM, never
in the API. Six decisions open (D-1 to D-6); OI-P10 among them closed since, October 11 (§6).
Its development and build open in their own conversation, on
Michel's word the same day, from
`docs/prompts/TCP_OPEN_DATA_START_PROMPT_v0_2.md`: six gates — the
decisions and two facts (the MapServer version, the click's
template); the `geo:` link; the export tool and validator on
invented data; the stages stored and published after Gate 4; the
API on a partner's need; a guide for OpenStreetMap mappers after
Gate 4.

**Open data, the facts and Gate B — Michel's word, October 9,
2026.** Plai's MapServer is 8.6.5, built with `OGCAPI_SERVER`
(his `mapserv -v` on the host), so an API on a partner's need asks
no upgrade, only configuration; no mapfile enables OGC API today,
which MapServer then refuses. The click is MapServer's HTML
template, written from `instance.meta entry_info_fields`,
`_labels` and `_html`; until now it served no geometry in any
format. D-1 to D-6 and the starting prompt's other questions are
still open. Michel opened Gate B: built in mapservice as
`plai/006` (`967c94c`, its prompt v0.85, README v0.44) — the click
on a published place carries "Open in your map app", labelled
"Location", second after the name, a `geo:` link (RFC 5870, with
Android's `q=` for a pin) to the published point to seven
decimals; `verify` and the leak pass prove it is the point,
latitude first, to 2 cm, and on published places only. Proven
locally (`verify plai vt` 101 of 101, the leak pass's six new
checks passing), and on the host the same afternoon, Michel's run
(mapservice prompt v0.86): `verify plai vt` 98 of 98, the leak pass
525 of 525, none skipped. Left: Plai's user copy made again,
Michel's look on a phone —
on iPhones a `geo:` link opens only an app that claims the scheme
— and then the user manual's §6 in both languages.

**The implementation plan — Michel's word, October 10, 2026.**
A document with a very concise summary and description of the
project whose main theme is an implementation plan — a
step-by-step guide with to-do lists:
`docs/IMPLEMENTATION_PLAN_v0_1.md`. The project in one page;
eight steps from the open decisions through the body, the stack,
the money, the test stretch, Gate 3, Gate 4, the record and open
data, to Phase 2, each a to-do list with state (done, in
progress, to do), holder and what it waits on; the dates from the
long list; what not to do on the way; the next thirty days in
order. It decides nothing and is corrected as gates close; a
conversation that closes a gate ticks the plan too. The same day,
on his word, the Ukrainian text
(`docs/IMPLEMENTATION_PLAN_UK_v0_1.md`, not yet read by anyone in
the corridor) and the bilingual PDF
(`docs/IMPLEMENTATION_PLAN_EN-UK.pdf`, from `build/build_plan.py`,
which reads the latest version of each text).

**The initiators — Michel's word, October 10, 2026.** The
project is initiated by two: "Initiated by UBEC (Ubuntu
Bioregional Economic Commons), led by Michel Garand, and Zhyva
Khata, led by Vasyl Yuskiv." In Ukrainian: «Ініціатори — UBEC
(Ubuntu Bioregional Economic Commons) під керівництвом Мішеля
Ґарана (Michel Garand) та «Жива хата» (Zhyva Khata) під
керівництвом Василя Юськіва (Vasyl Yuskiv).» — the Ukrainian
spelling of both names is Claude's, for Vasyl's word. Replaced
wherever an initiator was named: the README; the agreement v0.4
§1 and the proposal v0.4 (summary table and "How to take part"),
both languages; the white paper v0.6 §11, whose line on the legal
body now names both; the implementation plan v0.2 §1; the site's
landing page v0.3. PDFs rebuilt. Unchanged, for his word: who
answers for the project and holds the data (A-1, Michel
personally until the core body); the byline "UBEC / Carpathian
Hub Initiative" on every cover and opener; the tensions that say
the map was built by an initiative led by one person (reasoning
T-5, white paper §12); Zhyva Khata's place in the agreement and
the core body. Plai links and records agreement draft v0.7
(`plai/007`, October 11, 2026); each later draft is a mapservice
change of its own.

**The project overview — Michel's word, October 10, 2026.**
Michel has the chance to present the project to the Department of
Culture and Tourism in Kosiv. A handout and a presentation were
first written for that audience (prompt v0.47); the same day, on his
word, the presentation is not for Kosiv: it presents the project,
which is not only Kosiv, as an honest, comprehensive and concise
overview, English first, Ukrainian to follow. Both were rewritten
and moved from `docs/kosiv/` to `docs/overview/`. The handout,
`docs/overview/PROJECT_OVERVIEW_v0_5.md`, is drawn from the white
paper and the implementation plan and decides nothing: in brief,
why now (with the white paper's sources), how it works,
regeneration against sustainable development, across the arc (the
three phases; corridors only from consent), what it will not do,
working in wartime and within the law, where it stands (in place;
not yet — no host named, one person holds everything, the budget
proposed, not decided), what is not solved, how we will know, and
what we ask of people in the mountains, partners, funders, and
communities and institutions. Its editable copy is the Claude doc
of the same title. The presentation is a seventeen-slide deck with
speaker notes, made in Claude's Slides; its source is kept in
`docs/overview/deck/` (`deck.json` and one `slides/<id>.html` per
slide), and a LibreOffice copy,
`docs/overview/Trans-Carpathian_Pathways_Overview.odp`, is built by
`build/build_overview_odp.js` (pptxgenjs, then LibreOffice's
converter) with the open DejaVu faces. The cover's background is
Michel's image *Day 70 — warm wind on the path*
(`docs/overview/deck/assets/`, the SVG as given and a 1920×1080 PNG
from it); in the Slides deck it is referenced by the deck's own
asset address. Both carry the Pilgrim of the Plai. Not yet: the
UBEC logo on the cover; a contact for Vasyl Yuskiv; the Ukrainian
texts.

**The name for whoever walks — Michel's word, October 10, 2026.**
Whoever comes on foot through the network is the **Pilgrim of
the Plai** — in Ukrainian *прочанин плаю*, *прочанка плаю* — and
no longer the traveler. The name stands in full in role tables,
Part II and III of the agreement, headings and the first mention
in a document; *pilgrim* and *прочанин* (plural *прочани*,
genitive *прочан*) in running text. *Plai* in the name is the path —
the Hutsul and Romanian word for the old way through the high
pastures — from which the map takes its name; the agreement, the
proposal and the white paper gloss it once so that the two are
not read as one. *Прочанин* is from *проща*, the pilgrimage still
walked in the region and set apart there from tourism as inner
work, and is related to *прощати*, to forgive. The proposal
"Plaiar" (*плаяр*) was weighed and not taken: no person-word on
*плай* is recorded in Hutsul speech, and *-ар* names a trade —
the steward's, not the guest's. Carried into the agreement v0.5,
the proposal v0.5, the white paper v0.7 (§4.3 gives the name and
its roots), the manual v0.5, the reasoning v0.2 (T-3), the module
map v0.3, the decisions checklist v0.4, the implementation plan
v0.3, the Kosiv handout v0.2 and the deck's source, the
open-data specification v0.2, the partners' needs and long list
v0.3, the three starting prompts v0.2, the site's landing page
v0.4 and the diagrams; PDFs rebuilt. Left as they were:
"traveler" where a text speaks of travel in general (the
critique of extractive travel, travel advisories), of the
literature (Goodwin & Santilli), of other projects (Via
Transilvanica) or quotes the law;
the reviews, which are dated records; and every changelog. The
deck in Claude's Slides and the handout's Claude doc are their own
copies and follow the repository. Still open: whether the project
says outright that it borrows no one's faith (T-3, white paper
§12). Not yet heard: the name said aloud in the corridor, to
Vasyl Yuskiv and the first hosts.

**The pilgrim in Plai's form — Michel's word, October 10, 2026.**
The one screen that still said "traveler" — the host group's
heading in Plai's form — now reads "If you host pilgrims":
mapservice `750dbf4`, Plai's entries scheme v0.10, its prompt
v0.91. A label only; no column, list or check changes. The full
name stays off the form, where the plai would read as the map.
Carried here into the manual v0.6 (both languages) and the
host-fields specification v0.6. Closed on the host the same
evening, Michel's run: rendered, the heading changed in the user
copy's form, his look, the copy exported (mapservice `43d2cae`,
recorded in its prompt v0.92). The manual's Figures 5 and 6
retaken from the form by Michel the same evening, both showing
the new heading; manual v0.7.

**The drafts for public review, stress-tested — Michel's word,
October 10, 2026.** Asked which drafts could be made public for
review, Claude named the white paper, the proposal, the co-creator
agreement and the project overview, with the reasoning and the
open-data specification after a light edit; the partners' lists,
the reviews, the prompts, the checklist and the plan stay
private. On his word, three stress tests of those six were run the
same evening by separate agents — the corridor reader, the hostile
reader, the fact-checker — and are recorded with every finding and
what was done with it in
`docs/reviews/PUBLIC_DRAFTS_STRESS_TESTS_v0_1.md`. Their common
finding: the drafts were behind the decisions of October 9. The
corrections were taken in on his word: white paper v0.8, proposal
v0.6, agreement v0.6, overview v0.4 (the doc, the deck and its
LibreOffice copy too), reasoning v0.3, open-data specification
v0.3, manual v0.8 (the password line); PDFs rebuilt. Among them:
S-14's corridor consent drafted at last in agreement §5 and as an
optional tick; the three D-6 principles in the agreement's list;
the record described as it then was, the repository being private;
how to recognise the project, and that nobody from it asks for
money in advance, a password or a passport; the deputy as not yet
named; the border rules for those who come directly; the Bukovel
forgery case kept apart from the resort's owners and NGO figures
attributed; the toloka, the polonynas, the displaced and the
newcomer reworded; «господиня» named. Nothing Michel decided was
changed. Twenty-five decisions are put to him in the review's §5,
eight of them before the drafts go out: the Ukrainian name, a
reading in the corridor, the record, the test of the concept, the
first Curator, the backups line, no ratings, and the agreement
version Plai records. The texts now say that the documents
published for review are on the project's site, which holds only
once they are.

**The agreement on Plai at draft v0.7 — Michel's word, October 11,
2026 (the review's D-8).** Plai linked and recorded draft v0.3
while the agreement had reached v0.6. The agreement's own line on
the version Plai records named v0.3, so it was made to hold for
any version — agreement v0.7, nothing else changed — and v0.7 put
on Plai: mapservice `c9c253c`, `plai/007` setting
`agreement_version` to v0.7 with the two version checks, Plai's
entries scheme v0.11 linking the v0.7 PDF, proven on a throwaway
PostgreSQL 16 (its prompt v0.93). An entry that accepted an
earlier draft keeps it; no real entry exists. Closed on the host
the same morning, Michel's run: `007` applied, the user copy
exported with the v0.7 link (mapservice `74e6f03`), `verify plai vt`
98 of 98 with the agreement checks proving v0.7 (its prompt v0.94).

**Three of the review's decisions — Michel's word, October 11,
2026.** *The record is public* (D-3): the repository
`ubeccommon/trans_carpathian_pathways` is the project's record;
the white paper v0.9 and the overview say so. Checked first: no
address, password, token or key anywhere in its history; what
publishing shows is operational detail — the host's name and
users, paths, the backup plan, the October 9 scenarios. The
switch to public is Michel's, on GitHub. *The test of the
concept* (D-4) runs with the public review and changes as it
learns; the overview says so. *No ratings* (D-7) unless those
rated consent: white paper §6.3, proposal v0.7, reasoning §5,
the overview and its deck. The agreement stays at v0.7, which Plai
links: both its lines stay true, and its next version carries the
new wording with the decisions still to come. The rest of the
review's §5 is decided in due course, on his word.

**The landing page for the public review — Michel's word, October
11, 2026.** A conversation of its own reworks the landing page of
`tcp.ubec.network` into the front door of the public review: the
drafts to read and how to answer them, the stage, how to recognise
the project, the border rules for those who come directly (which
the agreement and the proposal now promise the site publishes), and
the public record. Opened from
`docs/prompts/TCP_LANDING_PAGE_START_PROMPT_v0_1.md`; four gates,
its open items for Michel at Gate A; nothing in `ubec_mapservice`.

**The site's menu and the documents' pages — Michel's word, October
11, 2026.** The site stays on its own static build, not Ghost; Ghost
keeps the field writing. Every page carries a menu above the picture:
About, the white paper with its chapters, the proposal, the
co-creator agreement with its parts and roles, the overview, Plai and
the field writing. The white paper, the proposal and the agreement
have a page in each language, the overview one in English, built by
`build/build_site.py` v0.5 from the latest file in `docs/`, with
diagrams and committed PDFs; every Ukrainian page says the Ukrainian
has not yet been read in the corridor. A document's sources are
links; nothing loads from another server; the record on GitHub is
linked, the repository being public since that morning. Recorded in
`site/README.md` v0.9. Gate A of the landing page's own text still
waits on his answers. The same morning, on his word: the menu in the
logical order — About, Overview, Proposal, White paper, Co-creator
agreement, Plai, Field writing, the same in both languages; the map
link opens the Pathways application `ubec_plai_hub_tcp` on the
corridor around Verkhovyna; and the overview v0.5 points to the site
in place of "available on request". The menu closed on the host on
his "looks good". Then, on his word, German and Polish: a landing page
in each (Claude's translation, said so on the page), the menu in each,
the documents in English and Ukrainian with an EN tag; the name kept
in English, «Transkarpatien» and «Zakarpacie» naming the oblast as
«Транскарпатські» does (D-1); a list of four languages in place of the
switch. Recorded in `site/README.md` v0.15.

**The overview, the proposal and the white paper in German and Polish —
Michel's word, October 11, 2026.** Translated by Claude from overview
v0.5, proposal v0.7 and white paper v0.9, beside their sources in
`docs/`, with diagrams in both languages and a PDF each for the proposal
and the white paper; the EN-UK PDFs unchanged. One glossary for all six,
`docs/translations/GLOSSARY_DE_PL_v0_1.md`: the name kept in English;
Gate as *Schwelle* / *próg*; the pilgrim as *Pilgerin, Pilger des Plai*
/ *pielgrzym płaju*; people and organisations under the names they write
themselves. Checked by script and by a separate reader in each language;
their findings taken in. Every translation says it has not been read by
someone whose language it is. The co-creator agreement stays in English
and Ukrainian until it settles. When an English document changes, its
German and Polish follow, or say which English version they translate.
Recorded in `site/README.md` v0.16.

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
| Pilgrim of the Plai | sees published points; may go directly | no account          |

**The Curator is not a gatekeeper — Michel's word, October 9,
2026 (S-1):** host points are public and clickable during the
pilot; a pilgrim may ask the Curator for a journey or find a
published host and go directly. Every Curator duty towards
pilgrims in the agreement applies to those who come through the
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
pilgrim to host; the project, its Curators and its stewards hold
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
description), so a pilgrim knows the point is not the house.
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

**Michel's word, October 11, 2026:** pilgrims, stewards and
Curators can use the planner directly. It is public, so anybody
can use it. The Curator can create a route, save it and manage
it; these stretches can be combined to create a corridor. This
replaces "for the Curator only, never answering a pilgrim, built
only if needed". The specification:
`docs/specs/PATHWAYS_STAGE_PLANNER_SPEC_v0_3.md`. Decided there on
Michel's word the same day: a steward may save a draft, and only
the Curator publishes it (SP-1); the public page and service run
on Plai and come before the first hosts (SP-2); the public answer
names published hosts with only their detour time (SP-3); the
numbers as proposed (SP-4); the first real run Verkhovyna – Zhyva
Khata – Tepla Gora – Kosiv, three stretches joined as a corridor
(SP-5); the public documents revised when Michel says so (SP-6); a
stretch's name and note in English first, until a multilingual
Mapservice is explored (SP-7). None open.

**What stays:** a tool proposes, a person decides. Anyone may ask
for a way; a steward may save it as a draft; only a Curator makes a
way the project's, by publishing it, and only a Curator joins
stretches into a corridor. Nothing the
planner says is a booking, a promise that a host will receive, or
a statement that a path is safe today.

**The engine:** `tools/stage_planner.py` v0.4, Python with
networkx, in memory, writing nothing but its answer. `route`: from
a start and an end (a published place, a village in OSM, or
`lat,lon`), the route by the criteria below, up to two
alternatives, the quickest way beside them; a band of 2.5, 5, 7.5
and 10 minutes' reach on both sides, fading outwards, with its
outer edge as the boundary; the places within reach in route
order with their one-way detour. `corridor`: stretches joined into
one band, one boundary, one list, gaps shown. Tested on a made-up
valley (`tools/test_stage_planner.py`); not yet run on Plai's data
— the first real run is Verkhovyna to Kosiv (SP-5).

**Input**
- Published Plai places with their offers and season, from
  `instance.entry_public`.
- The path network: OpenStreetMap footways, paths, tracks and
  roads in `reference_sa.osm_line` (Plai's base map, already
  loaded); hiking route relations for marked trails; open places
  (viewpoints, springs, peaks, mountain huts, hikers' shelters,
  chapels and crosses, heritage) in `reference_sa.osm_point`.
- Terrain: GEDTM30 v1.2 ground heights from Mapservice's
  `terrain/ground.tif` (OI-P9), sampled at 30 m along each
  segment, per direction.
- The border: `reference.admin_unit`, Ukraine at country level.
- The request: start, end; party (solo, couple, group, family);
  month; reach in minutes (5 to 10).

**Edge cost — walking:** DIN 33466 hiking time: 4 km/h on the
flat, 300 m/h ascent, 500 m/h descent; segment time = the larger
of the horizontal and vertical times plus half the smaller. The
party scales it; the Curator sets the scale.

**Criteria:** off the beaten path — paths and tracks neutral,
village roads a little dearer, main roads much dearer, trunk roads
not walked; a marked trail and passing near a place preferred a
little — "the logic of encounter, not just efficiency"; the
party's SAC grade and trail visibility as limits; never inside
the border strip (S-8); never an air-raid shelter listed. The time
reported is always the real DIN time; the criteria steer, they do
not shorten. The numbers are as proposed, on Michel's word of
October 11 (SP-4); the first real run and Gate 4's GNSS track test
them, and a change is his or the Curator's word.

**Hosts in what it says (SP-3, Michel's word, October 11):** the
public answer names each published host within reach by their
published name and one-way detour time, in route order, and
nothing else — no place, no offer, no kind, no kilometre, no
geometry — so no file anyone may pass on carries a host's place
(open data spec §2); the place stays on Plai's map, public and
clickable (S-1). The Curator's answer lists hosts in full.

**Licence (OI-P10, closed by Michel's word of October 11):** an
answer is computed and gone; a saved stretch is stored in Plai's
`instance_sa` under ODbL 1.0, as class A of the open data spec.
The list of places is never stored with a stretch: it is asked
for again each time, so a host who withdraws leaves every stretch
at once.

**Where it runs.** The stack's image (`postgis/postgis:18-3.6`)
has no pgRouting, and none is proposed. By hand today, on
ubec-common in Mapservice's environment (`tools/README.md`). For
anyone to use it: a small service and a page in the Pathways
application, and `instance_sa.stretch`, `corridor` and
`corridor_stretch` as Plai migration `plai/008`. *SP-2, Michel's
word, October 11, 2026:* the page and service run on Plai and come
before the first hosts (Gate 3); Mapservice's changes, built there
from `docs/prompts/PLAI_STAGE_PLANNER_START_PROMPT_v0_2.md`, behind
the leak pass.

**Multi-day stages** — each day ending at a host with an overnight
offer, open that month, with capacity for the party, under the
party's limit in hours and ascent — are the next piece, `stages`,
on top of `route`.

* * *

## 7. Principles — Operational

From the proposal §8, binding:

- **Honest offer** — hosts offer only what they actually have.
- **No performance** — the encounter is real or it is nothing.
- **Organic growth** — the network grows from the inside out.
- **Curator as memory** — the human holds what the algorithm
  cannot; anyone may use the planner, and only the Curator
  makes a way the project's, by saving it (§6, Michel's word,
  October 11, 2026).
- **The pilgrim arrives** — the journey is undergone, not
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
- **Safety is the Curator's to hold**, not the pilgrim's to
  find: shelter, the state of each stage, alerts — off the
  platform. **Plai holds no confidential information** (Michel's
  word, October 9, 2026, S-15). The border-zone rules are public
  law: the Curator gives them in writing to every pilgrim who
  comes through the Curator, and the project publishes them for
  anyone who comes directly.
- **The Curator is not a gatekeeper** (Michel's word, October 9,
  2026, S-1): pilgrims may find a published host and go
  directly; pilgrims are responsible for their own preparation
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
  missing, what a pilgrim needed and did not have. And settled
  here, after the walk (Michel's word, October 9, 2026): whether
  the pathway is marked, and to which standard.
- **Gate 5 — The planner public.** No longer "if needed" (Michel's
  word, October 11, 2026, §6), and no longer last: it comes before
  Gate 3's first hosts (SP-2), keeping its number. Closes when the
  page, the service and saving run on Plai behind the leak pass and
  Michel has looked at a real route on it. The stages walked at
  Gate 4 are then its test cases.

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
- **OI-P9** — Closed, Michel's word, October 10, 2026: two DEMs.
  Ground: GEDTM30 v1.2, CC BY 4.0, cited as Ho et al. 2025,
  PeerJ 13:e19673. Surface: Copernicus DEM GLO-30, shown with the
  notice "produced using Copernicus WorldDEM-30 © DLR e.V.
  2010-2014 and © Airbus Defence and Space GmbH 2014-2018 provided
  under COPERNICUS by the European Union and ESA; all rights
  reserved". Both shown at render time, never joined into a
  project's tables; FABDEM and FathomDEM set aside for their
  non-commercial licence; vertical datums checked before
  differencing; the layers themselves are Mapservice's change,
  needed for the map from Gate 3, not Gate 5. §6. Built in
  `ubec_mapservice` on Michel's "commit and build" as `6bed2e0`
  (its prompt v0.87): `tools/terrain.py` fetches both onto one
  30 m grid in EPSG:3035 for the Ukrainian Carpathians (22.1 to
  26.0 E, 47.7 to 49.6 N, about 0.75 GB on the host's `/data`),
  and render draws relief, contour lines (100 m labelled, 20 m
  between from 1:25,000) and the height of forest and buildings
  (off by default) on Plai. A WMS or WCS from elsewhere was not
  taken: a picture carries no heights. On the host the same
  morning (mapservice prompt v0.90, `44a56ba`): GEDTM30 turned out
  to be in metres though its files state a scale of 0.1, which the
  first run trusted; `terrain.py` v0.2 proves the unit against
  Copernicus, and surface minus ground now averages 5.9 m. Michel's
  look above Verkhovyna: contours 800 to 1,100 m below Synytsi
  (1,186 m), the relief clear through the forest. Plai's user copy
  carries the three layers; the leak pass passes every terrain
  check. Open: the height of a point in the click, and the stage
  planner's ascent, from the same ground file.
- **OI-P10** — Closed, by Michel's word of October 11, 2026, that
  the Curator saves stretches: an answer is computed and unstored;
  a saved stretch is stored in `instance_sa` under ODbL 1.0. §6.
- **OI-P11** — The Phase 3 country list: the proposal names seven
  countries; the Outlook boundary that sets Plai's extent
  reaches nine, Austria and Bulgaria included (mapservice
  prompt §3).
- **OI-P12** — Closed, Michel's word, October 9, 2026: a pilgrim
  from abroad is responsible for their own preparation and travel
  and informs themselves, in their own country, about advisories,
  insurance, martial law, cash and permits; the agreement's
  pilgrim part says so, and the Curator repeats it to those who
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
  October 9, 2026: payment passes directly from pilgrim to host.
  §5.

* * *

*Changelog*
- v0.64, amended 2026-10-11 — the engine at v0.4 after the first run on ubec-common: Latin names find Cyrillic ones, `find`.
- v0.64 — 2026-10-11 — SP-4 to SP-7, Michel's word: the numbers as proposed; the first real run Verkhovyna – Zhyva Khata – Tepla Gora – Kosiv; the public documents when he says so; a stretch's name and note in English first, until a multilingual Mapservice is explored. Spec v0.3, start prompt v0.2.
- v0.63 — 2026-10-11 — SP-1 to SP-3, Michel's word: a steward saves drafts, the Curator publishes; the page and service on Plai before Gate 3; the public answer names hosts with their detour time only. Spec v0.2, engine v0.3, the start prompt for the build on Plai.
- v0.62 — 2026-10-11 — the planner public, Michel's word: anyone plans; the Curator saves and manages stretches; stretches make a corridor. §6 rewritten, §7 and Gate 5 with it; OI-P10 closed; the engine at `tools/stage_planner.py` v0.2; the spec v0.1 with SP-1 to SP-7.
- v0.61 — 2026-10-11 — the overview, the proposal and the white paper in German and Polish, Michel's word.
- v0.60 — 2026-10-11 — the menu closed on the host; German and Polish on the site, Michel's word.
- v0.59 — 2026-10-11 — the menu's order, the map link to the Pathways application, the overview v0.5 pointing to the site; Michel's word.
- v0.58 — 2026-10-11 — the site's menu and the documents' pages, Michel's word: our own build, not Ghost.
- v0.57 — 2026-10-11 — the starting prompt for the landing page.
- v0.56 — 2026-10-11 — D-3, D-4, D-7 on Michel's word: the record
  public, the test with the review, no ratings without consent.
- v0.55 — 2026-10-11 — the agreement at draft v0.7 closed on the
  host: `verify plai vt` 98 of 98.
- v0.54 — 2026-10-11 — the agreement at draft v0.7, and on Plai
  (mapservice `c9c253c`, `plai/007`); D-8 taken.
- v0.53 — 2026-10-10 — the drafts for public review stress-tested;
  the corrections taken in; twenty-five decisions put to Michel.
- v0.52 — 2026-10-10 — the manual's Figures 5 and 6 retaken with
  the new heading; manual v0.7.
- v0.51 — 2026-10-10 — the pilgrim in Plai's form, closed on the
  host (mapservice `43d2cae`).
- v0.50 — 2026-10-10 — the pilgrim in Plai's form: mapservice
  `750dbf4`, "If you host pilgrims".
- v0.49 — 2026-10-10 — the project overview: the Kosiv handout and
  deck rewritten as an overview of the whole project, in
  `docs/overview/`, with a LibreOffice copy of the deck.
- v0.48 — 2026-10-10 — the Pilgrim of the Plai: the name for
  whoever walks, carried into every document.
- v0.47 — 2026-10-10 — the handout and presentation for the
  Department of Culture and Tourism in Kosiv, English.
- v0.46 — 2026-10-10 — the terrain on Plai, closed on the host.
- v0.45 — 2026-10-10 — the terrain built in mapservice
  (`6bed2e0`), not yet on the host.
- v0.44 — 2026-10-10 — elevation: two DEMs, GEDTM30 for the
  ground and Copernicus GLO-30 for the surface; OI-P9 closed.
- v0.43 — 2026-10-10 — the initiators: UBEC and Zhyva Khata.
- v0.42 — 2026-10-10 — the implementation plan in Ukrainian, and its
  PDF.
- v0.41 — 2026-10-10 — the implementation plan v0.1 recorded.
- v0.40 — 2026-10-09 — Gate B on the host: verify 98 of 98, the
  leak pass 525 of 525.
- v0.39 — 2026-10-09 — open data: the two facts, and Gate B built
  in mapservice (`plai/006`), proven locally.
- v0.38 — 2026-10-09 — the starting prompt for the open-data work.
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
