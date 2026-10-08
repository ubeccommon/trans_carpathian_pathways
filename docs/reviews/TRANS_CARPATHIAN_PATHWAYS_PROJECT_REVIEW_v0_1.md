---
title: "TRANS_CARPATHIAN_PATHWAYS_PROJECT_REVIEW_v0_1"
subtitle: "The project as a whole, read before a co-creator agreement"
author: "Michel Garand"
date: "October 2026"
version: "v0.1"
lang: "en"
license: "CC BY-SA 4.0"
project: "Trans-Carpathian Pathways"
status: "read-only review; nothing in either tree was changed"
---

*What Trans-Carpathian Pathways holds at commit `becc0a3`
(starting prompt v0.16, proposal v0.2, user manual v0.1,
host-fields specification v0.5), what Plai holds for it at
mapservice `67ae732` (prompt v0.79), where the documents have
drifted from the decisions, what the project risks as it moves
from software to people, and what a co-creator agreement must
settle. Michel's word, October 8: a comprehensive review of the
project and a co-creator agreement for its many roles. Both trees
read from fresh clones; both PDFs rebuilt from the tree in a
scratch copy. No host was reached: every host figure here is the
mapservice prompt's own record. Nothing here is legal advice;
where a point turns on law, it says who should check it.*

* * *

## 1. What Was Read

In this tree: the README; the starting prompt v0.16 whole; the
proposal v0.2 in both languages; the user manual v0.1 in English;
the host-fields specification v0.5; the mapservice state review
v0.1; the face start prompt v0.1; `build/build_pdf.py`,
`build_manual.py`, `diagrams.py` and `logo.py`.

In `ubec_mapservice`: the prompt v0.79 — its §3 entries on Plai,
the face and the backdrop, its §4 principles and §8 open items;
`db/instances/plai/001` to `003`; Plai's two Digitizer schemes,
the entry form's privacy notice among them; the last fifteen
commits, `73d99bc` to `67ae732`.

Run: `build_pdf.py` and `build_manual.py` in a scratch copy of the
tree, Python packages from `build/requirements.txt`. Both build;
the four diagrams come out byte for byte as committed; the
proposal is 15 pages and the manual 14, as committed. The build is
reproducible from the tree.

* * *

## 2. Where the Project Stands

| Gate | State on October 8 |
|------|--------------------|
| 0 — Decisions | Closed October 7: OI-P1 to OI-P8 |
| 1 — Plai in a browser | Passed in fact on October 8; "pending" in §8 |
| 2 — Host fields | Closed October 8: `plai/003`, seen end to end |
| 3 — First hosts | Waits on backups with an off-host copy |
| 4 — First walk | Not begun |
| 5 — Planner | Only if Gate 4 shows a need |

What exists:

- The outward proposal, English and Ukrainian, one A4 PDF.
- The user manual for entrants and curators, both languages, one
  PDF, with the stewardship address and an honest line on what the
  stack cannot yet do.
- On Plai: the host fields and hosts drawn in ochre (`plai/003`);
  the stewards' group (`727aeec`); points only in the Digitizer
  (`1c1c192`); a user copy exported with Plai's emblem as its
  picture (`67ae732`); the UBEC mark and Michel's backdrop on the
  landing and login pages.
- Two rows in Plai's entry table from Michel's host-fields look;
  the leak pass's publication section now skips (mapservice
  `ebe82a6`).

What does not exist yet, and bears on people rather than software:

- Any host, steward or Curator by name; any real account.
- Backups with an off-host copy — the mapservice condition for any
  real account.
- Short access logs — a mapservice principle with no
  implementation yet (its project review's F13, second half).
- A mailer: "Forgot password?" sends nothing.
- A legal body named anywhere in either tree.
- Any written terms beyond the form's five-sentence privacy
  notice.
- A licence, or any statement of rights, on what an entrant
  enters.
- Any word on how a funder's money is held or accounted for.

The software is ahead of the agreements between people. That is
the right order for a map — the consent model had to be proven
before anyone was asked to trust it — and it is the reason this
review comes now: Gate 3 is the first gate whose work is a promise
made to a person.

* * *

## 3. Drift — the Documents Against the Decisions

- **D-1 — Gate 1.** Prompt §8 still says Gate 1 is "pending on the
  mapservice side". Michel's look on October 8, recorded under
  Gate 2, was that very look: a Digitizer save worked in a browser
  as entrant and as curator. Close Gate 1 with the same date.
- **D-2 — The steward is missing from the proposal.** Prompt v0.13
  (October 8) said the proposal's "become a Curator and hold a
  stretch" line moves to the steward in its next version. The
  proposal is still v0.2: its summary has "Curators who hold each
  stretch", its "How to take part" table offers a local walker the
  Curator's role, and the steward appears nowhere, in either
  language.
- **D-3 — Who enters.** The proposal's pilot step 2 says each host
  places themselves "each with their own account", and its safety
  section says "The host places the point". OI-P4 was amended on
  October 8: the Curator, and the steward, may enter for a host
  who cannot. Both lines need "or a Curator or steward enters for
  them, with their agreement".
- **D-4 — The proposal's contact.** "Contact address to be added
  before this document is sent." The contact has been
  `stewardship@ubec.network` since August 31 (mapservice prompt
  §8); the manual and the entry form already use it.
- **D-5 — "Every community can take its data with it."** True as
  an export, and promised in two places in the proposal. On what
  terms anyone may then use what was exported is said nowhere
  (R-3).
- **D-6 — One list of principles, two wordings.** The proposal has
  eight principles ending "Data stays with the people" and "human
  to land"; the prompt's §7 has seven, "human to nature", and no
  data principle. One should be the source and the other copy it.
- **D-7 — Prompt §9's order.** OI-P15 sits before OI-P14 and
  OI-P13 last. Cosmetic.
- **D-8 — Deletion.** Mapservice's principle is that users can
  delete their account with their rows; on Plai today a person
  writes to the stewardship address and the administrator runs
  `purge` (manual §5). Not a fault — the honest statement is what
  the agreement must carry.

* * *

## 4. Risks

**R-1 — One person holds everything.** Michel is the lead, the
only administrator, the maker of every account, the one who resets
every password (no mailer), the operator of every host run, the
only name under "Help", and by the mapservice prompt the holder of
the backup decryption key. If he cannot be reached for three weeks
— in wartime, a real possibility — no host can be added, no
forgotten password reset, and if the only key is his, no backup
restored. A co-creator agreement promises things on the project's
behalf; it should also say who keeps those promises when the lead
cannot. Proposed: a named deputy administrator with a backend
account, the key held in a sealed copy by a second person, and a
stated notice period if the service must stop.

**R-2 — No legal body.** "UBEC" is the initiator in every
document, but neither tree names its legal form, and the entry
form's notice puts the data "in the care of Michel Garand". As
things stand, the controller of every host's data is Michel
personally. The server is in Germany, so the EU's data protection
law governs that data although the hosts are in Ukraine. The
notice says who, where, what is public, withdrawal and deletion;
it does not say the purpose, the legal basis (consent), how long
data is kept, the right of access and correction, or the right to
complain to a supervisory authority. Someone who knows German data
protection law should read the notice and the agreement's §5
before the first real account; the fix is a few sentences, not a
system.

**R-3 — Nothing says who may use what is entered.** Code is AGPL,
documents CC BY-SA; entries and photos carry nothing. Two promises
pull against each other here. The proposal says every community
can take its data; the consent model says an entrant can withdraw
at any time and the place leaves every map and every export. An
open licence cannot keep the second promise: CC BY-SA and ODbL
cannot be revoked, so a host's home released under either could be
copied and republished forever, after the host withdrew it, in
wartime. Recommended: the entrant keeps every right in what they
enter; they allow UBEC to store it, show it as they consented and
a Curator chose, back it up and hand it back; the permission ends
with withdrawal. An export is the entrant's and their community's,
not an open dataset. Places that are nobody's home — a viewpoint,
a spring — could be released openly later, by a separate decision.

**R-4 — The project's legal shape turns on OI-P13.** Whether
payment passes directly or through the Curator or `ubec-pay` is
not only a question of who holds money. A project or a Curator
that takes payment for a bed and a guided walk on one journey may
come within Ukraine's rules for tour operators and, for travelers
booked from the EU, within the EU's package travel rules, with
their duties of liability and insolvency cover. Payment passing
directly from traveler to host, with the Curator suggesting and
never selling, keeps Pathways what the proposal says it is — not a
booking service. Recommended: settle OI-P13 as direct before the
first traveler, write "the project holds no money for stays" into
the agreement, and have that shape confirmed by someone who knows
Ukrainian tourism law.

**R-5 — Hosts' own obligations.** A host who receives paying
guests may owe registration, tax or a tourist levy, and under
martial law may have rules to follow when receiving foreigners.
The project cannot check these and must not seem to. The agreement
says each host answers for their own, and the Curator says so
plainly at the first visit.

**R-6 — Wartime knowledge with no written duty.** Shelters,
border-zone rules and stage conditions stay with the Curator and
are never published (prompt §3, §7). Stewards and Curators will
also know who hosts, where, for how much, and who is coming when.
Nothing yet binds any of them to keep that confidential, to use it
only for the pathway, or to hand it over on leaving.

**R-7 — A home at its exact point is safe only as an informed
choice.** OI-P7 publishes a home where its host places it; the
prompt and the manual's chapter for curators record that such a
point is an address. The entry form says nothing of it, and the
manual's chapter for entrants says only "take care". The
agreement's host part should make it an acknowledgement at
signing, and say the host may place the point at a nearby meeting
place instead.

**R-8 — Test rows on Plai.** Michel's two rows from the
host-fields look are in the entry table, so the leak pass skips
its publication section and `verify` needs `--force`. Before the
first host: purge them, and run the full proof once more on an
empty Plai — the last time it can run there (state review F-3).

**R-9 — One-hour sessions on a mountain connection.** A host
entering slowly with the Curator beside them loses what they have
not saved after an hour, and there is no mail to recover a
password. Both are Mapservice's decisions, already recorded there;
raised again because Gate 3 is where they bite.

**R-10 — Paid roles with no terms.** The proposal funds "a paid
role for the first Curator". Who pays, from which money, for what,
and what the Curator owes in return are written nowhere. The
agreement should leave pay to a separate written arrangement and
say that one exists.

**R-11 — People in photographs and stories.** The project will
walk a corridor, document it and write about it — the proposal's
pilot step 5 and Michel's own Carpathian writing. Hosts, their
children and their homes will be in those photographs and texts.
Plai's photo consent covers Plai only.

* * *

## 5. What a Co-Creator Agreement Must Settle

- **Every role in the trees**, and one more: host, pathway
  steward, Curator, traveler, contributor (developer, mapper,
  translator), partner initiative, funder — and the administrator,
  who owes the others as much as they owe the project.
- **Data:** consent field by field as built; withdrawal; deletion
  on request; export; no sale, no tracking, short logs (mapservice
  §4); encrypted off-host backups; what happens on a breach; the
  R-2 gaps.
- **Rights:** code AGPL-3.0-or-later and documents CC BY-SA 4.0,
  inbound as outbound; entries and photos as in R-3; people in
  photographs and stories (R-11); OpenStreetMap credited.
- **Money:** OI-P8 and OI-P13's first half as decided; the second
  half as R-4 recommends; no commission; funders' money accounted
  for openly; paid roles in writing (R-10).
- **Safety:** R-6 and R-7; anyone may stop; alerts and shelters
  first.
- **Continuity:** R-1.
- **Decisions:** gates, Michel's word in Phase 1, and a promise to
  ask the corridor how it is governed before Phase 2.
- **The counterparty and the law:** R-2.
- **Honesty about the stack:** what the manual already says — no
  mail, one-hour sessions, deletion by request.

**Claude's proposals in the draft, beyond the open items**, so
none is read as decided: "No ratings" added to the principles; no
commission and no payment for sending travelers; deletion within
30 days of a request; three months' notice before an ending; a
host's choice of a nearby meeting place for their point; the
Curator asking a host once more before a home goes public; a
traveler's details deleted after the journey; mappers never adding
a host's home to OpenStreetMap unasked; a funder's money reported
at each gate. Each stands until Michel's word changes it.

The draft agreement,
`docs/agreement/Trans-Carpathian_Pathways_Co-Creator_Agreement_EN.md`
v0.1, does each of these and marks every point that waits on
Michel's word as open.

* * *

## 6. Before Any Change — in Order

1. Michel's word on the agreement's open items, one at a time:
   **A-1** the counterparty (Michel personally, an existing UBEC
   body, or a body to be formed); **A-2** rights in entries (R-3,
   recommended: the entrant keeps them, a revocable permission to
   UBEC); **A-3** OI-P13's second half (R-4, recommended: direct);
   **A-4** a deputy administrator and the key's second holder
   (R-1); **A-5** governing law and the dispute route; **A-6**
   retention of withdrawn entries and travelers' details; **A-7**
   how each role signs (recommended for hosts: on paper with the
   Curator at the first visit, in Ukrainian, the form's ticks
   still governing each field).
2. The agreement v0.2 with his answers; then its Ukrainian text
   and one bilingual PDF, built by a `build/build_agreement.py` in
   the proposal's styles, as the proposal and the manual are.
3. The privacy notice in Plai's entry form brought into line with
   the agreement's §5 — a change in `ubec_mapservice`, on Michel's
   word for that change.
4. Proposal v0.3 in both languages: D-2, D-3, D-4, D-6, and a line
   pointing to the agreement.
5. Starting prompt v0.17: D-1 closed, D-7 put in order, the
   agreement and A-1 to A-7 recorded as decided.
6. The legal reads named in R-2 and R-4, before the first real
   account and the first traveler respectively.
7. Then Gate 3, after Mapservice's backups and R-8.

* * *

*Changelog*
- v0.1 — 2026-10-08 — initial, read at `becc0a3` and mapservice
  `67ae732` (prompt v0.79); both PDFs rebuilt from the tree; eight
  drifts, eleven risks, seven open items for the co-creator
  agreement.
