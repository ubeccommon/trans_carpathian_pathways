---
title: "Trans-Carpathian Pathways — Proposal (EN)"
version: "v0.2"
date: "October 2026"
lang: "en"
license: "CC BY-SA 4.0"
project: "Trans-Carpathian Pathways"
changelog:
  - "v0.2 — 2026-10-07 — corrected to Michel's decisions of October 7: a place, a home included, is shown where its host puts it (OI-P7); each host enters with their own account, the Curator beside them, so no assisted entry (OI-P4); payment forms settled, how payment passes still open (OI-P8, OI-P13); the photo moved to what is in place (Plai step B)."
  - "v0.1 — 2026-10-07 — initial."
---

![Trans-Carpathian Pathways](assets/logo.png)

# Trans-Carpathian Pathways

*A living network of place, people and path — project summary and proposal*

October 2026 · UBEC / Carpathian Hub Initiative

## Summary

Trans-Carpathian Pathways connects the people who still keep Carpathian mountain life alive with travelers who want to meet them, slowly and on foot. It is a living network of hosts, a pathway that grows from where those hosts are, and local Curators who hold each stretch of it.

The first corridor is in the Hutsul highlands of western Ukraine, between Vorokhta, Verkhovyna and Kosiv. The project runs on Plai, the Carpathian hub of UBEC Mapservice: a self-hosted map service in the EU that already carries a base map of the whole Carpathian range and a consent-controlled way for people to place themselves on it.

| | |
| --- | --- |
| What | A pilgrimage infrastructure of hosts, paths and Curators |
| Where first | Vorokhta, Verkhovyna and Kosiv, Ivano-Frankivsk region, Ukraine |
| Where next | The Ukrainian Carpathians, then across the arc's other countries |
| Built on | Plai — the Carpathian hub of UBEC Mapservice |
| Initiated by | UBEC (Ubuntu Bioregional Economic Commons) |
| Stage | Prototype: technical base in place, first hosts and Curator being sought |

We are looking for people to take part: hosts and Curators in the corridor, partners along the arc, technical contributors, and funders for the pilot.

## The need

Two problems meet in the Carpathians, and they share one answer: genuine encounter between a traveler and a place.

**Travel has become extraction.** Travelers move through places without touching them. Hosts perform hospitality instead of sharing it. The meeting between a person and a place, which is what travel was once for, has become a transaction.

**Mountain communities are thinning out.** Across the Carpathian arc, villages face depopulation, the loss of traditional knowledge and economic marginalisation. A way of life that took centuries to build is disappearing quietly. The people who still keep it are rarely on any tourist map, and they do not advertise.

A traveler who sleeps under someone's roof, eats at their table and learns how something is made leaves money and attention where they are needed. A host who shares what they actually have, without performing it, gains a reason and a means to keep it.

## The response

Trans-Carpathian Pathways builds three interlocking things: a network of hosts, a living pathway between them, and the Curator who holds it.

![How the network works: hosts, map, Curator, traveler](assets/network_en.svg)

Hosts place themselves on the map; the pathway grows from where they are; the Curator turns that map into a journey for each traveler.

**A network of hosts.** People across the arc who choose to share something real. A host offers one or more of:

| Offer | What it means |
| --- | --- |
| Overnight stay | Shelter: a room, a barn, a bed |
| A meal | Food from this place, shared or prepared |
| Local guidance | Knowledge of the land, the path and its stories |
| A workshop | A local craft, made here and taught here |

Hosts are not service providers. The offer is honest and specific, with no performance and no inflation. Viewpoints, springs and other places worth arriving at are mapped as places along the way.

**A living pathway.** The route is not designed from above. It emerges as hosts join: each host becomes a point on the map, the paths between them are traced over the mountain trail network, and the Curator adjusts the result for terrain, season, host capacity and the human logic of a journey. It grows as the network grows and contracts when hosts are away.

**The Pathway Curator.** The memory of the path, usually a local farmer, teacher or walker. The Curator knows a stretch of the pathway and its hosts, listens to each traveler's time, company and wish, suggests a route rather than prescribing one, and keeps track of who can receive whom, and when. The Curator is not a travel agent but a guide to the whole.

## Who it serves

The pathway holds anyone ready to slow down, for an afternoon or a month. Length and intensity are the traveler's choice; the Curator shapes the route around them.

| Traveler | A typical journey |
| --- | --- |
| Family with small children | A few hours: one host, one meal, one view |
| Solo traveler | Days or weeks of deep immersion |
| Couple | Slow travel at a chosen depth |
| Group of friends | Shared or split experiences along one stretch |
| Someone in transition | The pilgrimage as a personal threshold |

**Hosts** gain a fair, direct connection to travelers who come for what they actually offer, without needing to market themselves.

**Communities** gain income that stays local, and a reason for younger people to see value in knowledge that is otherwise being lost.

**Curators**, usually local people, gain a recognised role as keepers of their stretch of the path.

## The pilot corridor

The prototype runs through the Hutsul highlands of western Ukraine, one of the most culturally dense and naturally intact stretches of the Carpathian arc. Three towns anchor it:

| Place | What it holds |
| --- | --- |
| Vorokhta | Mountain gateway: forest, river, a traditional Hutsul settlement |
| Verkhovyna | High-pasture country and the first known hosts |
| Kosiv | Centre of Hutsul craft: the market, weavers and woodcarvers |

The three are roughly 25 km apart as the crow flies, so the corridor is a walk of several days. The exact route, its stages and its intermediate villages will be set by the hosts who join and confirmed by walking it, not drawn in advance.

Work in the corridor during the pilot:

1. Find and connect the first hosts: people who offer a bed, a meal, guidance or a craft.
2. Help them place themselves on Plai, each with their own account, with their consent and on their terms.
3. Establish the first Curator, a local person who holds the path.
4. Walk the corridor end to end as a traveler would.
5. Record what worked, what was missing and what the next corridor needs.

## Technical foundation

The project does not start from zero: its map platform already exists. Plai is the Carpathian hub of UBEC Mapservice, an open-source map service that UBEC runs on its own server in Germany, under EU jurisdiction, built on PostgreSQL/PostGIS, MapServer and Mapbender.

**In place today**

- A base map of the whole Carpathian range from OpenStreetMap: about 32 million mapped features (paths, villages, huts, springs, buildings), with hiking routes drawn on top.
- An entry surface where a person places a point exactly where they mean it and describes it: a name, a type of place, a category of offering, what is offered, and contact details.
- Consent built into the database: the entrant agrees, field by field, to what may be shown; a curator decides what is published; withdrawn entries leave every map and export.
- One photo per place, cleaned of location and camera data before it is stored, and shown only where the entrant has agreed and a curator has chosen to show it.
- Safeguards set before anything goes public: each project gets its own database, data licences are enforced by the database, and every public endpoint is tested for leaks.
- Full export at any time, so no community depends on UBEC to keep its own data.

**To be built for Pathways**

| Piece | What it does |
| --- | --- |
| Host details | More than one offer per host, season, capacity, languages spoken, accessibility, how the host is paid |
| Local languages | Entry forms in Ukrainian first, then Polish, Slovak, Romanian and others |
| Stage planner | A tool for the Curator that proposes daily stages between hosts by walking time and ascent |

The stage planner is a tool for the Curator, never a replacement. It proposes; the Curator decides. It favours encounters along the way over speed.

## Principles

These principles are operational, not aspirational: they decide every design and partnership choice.

- **Honest offer.** Hosts offer only what they actually have.
- **No performance.** The encounter is real or it is nothing.
- **Organic growth.** The network grows from the inside out, host by host, not from a plan drawn above it.
- **Curator as memory.** The human holds what the algorithm cannot.
- **The traveler arrives.** The journey is undergone, not consumed.
- **Off the beaten path.** Where people live, not where tourists are sent.
- **A pathway of relationships.** Human to human, human to land.
- **Data stays with the people.** Hosts decide what is shown, can withdraw at any time, and every community can take its data with it.

**What this is not:** not a tourism platform, not a booking service with a calendar to fill, not a performance of tradition, and not a finished product. It is an infrastructure that stays alive as the network changes.

## Safety, consent and working in wartime

The pilot begins in Ukraine during the war, and the project is designed around that fact rather than despite it.

- **The host places the point.** A place, a home included, is shown where its host puts it on the map, and only once the Curator has published it. The host can withdraw it at any time.
- **Contact details are gated.** A name, email, phone number or photo is published only where the host has agreed and the Curator has chosen to show it.
- **The Curator holds safety knowledge.** This includes the nearest shelter during air-raid alerts, any border-zone rules near the Romanian border, and current conditions on each stage. It is kept with the Curator, not published.
- **Travelers from abroad are briefed honestly.** They hear about travel advisories, insurance and martial-law conditions before they come.
- **Data is held in the EU,** on UBEC's own server, separate from any other project's data.

A pilot that works under these conditions will work anywhere on the arc.

## Roadmap

The project grows in three phases, and each opens only when the one before has proved itself on the ground.

![Roadmap: three phases, two gates](assets/roadmap_en.svg)

Phase 1 runs now in the Hutsul corridor. Phase 2 extends along the Ukrainian Carpathians, using what the pilot taught. Phase 3 crosses borders into Poland, Slovakia, Romania and the arc's other countries, with partner initiatives in each. No phase is tied to a date: a gate opens when its work is done.

## Funding

Support for the pilot would go to people on the ground first and software second. The map platform already exists, so most of the cost is human work in the corridor.

| Area | What it covers |
| --- | --- |
| Host outreach | Finding and visiting hosts, explaining the project, sitting with them while they enter their details |
| Curator | A paid role for the first Curator during the pilot |
| Walking the corridor | Test journeys, documentation, safety assessment of each stage |
| Development | Host details, local-language forms, stage planner |
| Translation | Interface and project materials in Ukrainian and later other Carpathian languages |
| Hosting and security | Server, backups and the safeguards that keep host data private |

How a host is paid is settled: each host chooses, for each offer, among a fixed contribution, a suggested contribution, exchange of work, and ubec-pay or a community currency.

Open questions, to be settled before the first traveler:

- Budget figures for each area, and the pilot's length.
- How payment passes: directly from traveler to host, or through the Curator or a community payment system.

## How to take part

There are five ways in, and each one shapes the project from here.

| You are | You can |
| --- | --- |
| A host in the corridor | Offer a bed, a meal, guidance or a craft, on your own terms |
| A local walker, farmer or teacher | Become a Curator and hold a stretch of the path |
| An initiative elsewhere on the arc | Partner on a corridor in Poland, Slovakia, Romania or beyond |
| A developer, mapper or translator | Help build Plai's host tools, the stage planner or local-language forms |
| A funder or foundation | Support the pilot corridor and its first Curator |

The project is initiated by UBEC, the Ubuntu Bioregional Economic Commons, and led by Michel Garand from the Verkhovyna area.

Contact: Michel Garand — contact address to be added before this document is sent.

*This is a living document. It will be refined as the network grows.*
