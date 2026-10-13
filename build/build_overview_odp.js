// Trans-Carpathian Pathways — Project Overview: the Slides deck (docs/overview/deck/) rebuilt as .pptx,
// then converted to .odp with LibreOffice. Usage, from the repository root:
//   node build/build_overview_odp.js /tmp/overview.pptx docs/overview/deck/assets/day70_warm_wind_on_the_path.png
//   soffice --headless --convert-to odp --outdir docs/overview /tmp/overview.pptx
// then rename the result to Trans-Carpathian_Pathways_Overview.odp. Faces: DejaVu Serif and DejaVu Sans.
// Coordinates are written in the deck's own 1920×1080 px space; P() turns px into inches (13.333" wide).
const pptxgen = require("pptxgenjs");
const path = require("path");

const OUT = process.argv[2] || "deck.pptx";
const COVER = process.argv[3];
const SERIF = "DejaVu Serif", SANS = "DejaVu Sans";
const P = (v) => v / 144;

const C = {
  navy: "1B1F38", night: "161A33", cream: "F5EEDC", sand: "EAE0C8", card: "FFFBF2",
  border: "D8CCB0", border2: "D2C6AE", body: "3A3F52", muted: "5E5A4C", muted2: "57544A",
  red: "9A3B2B", green: "2F5D48", gold: "E0A04A", moon: "F1E6C6", soft: "D2CBB8",
  rule: "3C4266", pill: "EAE0C8", line: "B9A98A", onRed: "FBF4E6", onRedSoft: "F3D9C6",
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.title = "Trans-Carpathian Pathways — Project Overview";
pres.author = "Michel Garand";
pres.theme = { headFontFace: SERIF, bodyFontFace: SANS };

function t(s, text, o) {
  s.addText(text, {
    x: P(o.x), y: P(o.y), w: P(o.w), h: P(o.h),
    fontFace: o.serif ? SERIF : SANS, fontSize: o.size / 2, color: o.color,
    bold: !!o.bold, italic: !!o.italic, align: o.align || "left", valign: o.valign || "top",
    margin: 0, isTextBox: true, lineSpacingMultiple: o.lh || 1.2, fit: "none",
    charSpacing: o.cs, paraSpaceAfter: o.psa, objectName: o.name,
  });
}
function card(s, x, y, w, h, fill, line, lw) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: P(x), y: P(y), w: P(w), h: P(h), fill: { color: fill },
    line: { color: line, width: lw || 0.75 }, rectRadius: P(16),
  });
}
function rule(s, x, y, w, color, px) {
  s.addShape(pres.shapes.RECTANGLE, { x: P(x), y: P(y), w: P(w), h: P(px || 2), fill: { color }, line: { color, width: 0 } });
}
function header(s, eyebrow, title, dark) {
  t(s, eyebrow.toUpperCase(), { x: 128, y: 128, w: 1664, h: 36, size: 24, color: dark ? C.gold : C.red, cs: 1.5 });
  t(s, title, { x: 128, y: 172, w: 1664, h: 84, size: 60, serif: true, color: dark ? C.moon : C.navy, lh: 1.1 });
}
function footer(s, text, color) {
  t(s, text, { x: 128, y: 980, w: 1664, h: 36, size: 24, color });
}
function bullets(items, color) {
  return items.map((it, i) => ({ text: it, options: { bullet: { indent: 18 }, breakLine: i < items.length - 1, color } }));
}
let section = null;
function slide(bg, sec) {
  if (sec && sec !== section) { pres.addSection({ title: sec }); section = sec; }
  const s = pres.addSlide({ sectionTitle: section });
  s.background = { color: bg };
  return s;
}

const S1 = "The project and its idea", S2 = "Why now", S3 = "How it works", S4 = "What guides it",
  S5 = "Where it goes", S6 = "Where it stands, honestly", S7 = "What we ask";

// 1 — cover
{
  const s = slide(C.night, S1);
  if (COVER) s.addImage({ path: COVER, x: 0, y: 0, w: P(1920), h: P(1080), altText: "" });
  t(s, "UBEC · ZHYVA KHATA · OCTOBER 2026", { x: 112, y: 96, w: 1100, h: 40, size: 26, color: C.gold, cs: 2 });
  t(s, "Trans-Carpathian Pathways", { x: 112, y: 146, w: 1180, h: 100, size: 76, serif: true, color: C.moon, lh: 1.1 });
  t(s, "A living network of hosts, paths and Curators across the Carpathian arc", { x: 112, y: 262, w: 1080, h: 110, size: 34, color: "E4DCC4", lh: 1.35 });
  t(s, "Project overview", { x: 112, y: 404, w: 640, h: 40, size: 26, color: "C9C3D6" });
  s.addNotes("Introduce yourself as Michel Garand of UBEC, the Ubuntu Bioregional Economic Commons, and name the co-initiators, Zhyva Khata, led by Vasyl Yuskiv, and Tepla Gora, led by Andriy Grushetsky. Trans-Carpathian Pathways is meant for the whole Carpathian arc. It starts with one corridor in the Hutsul highlands of Ukraine, from Vorokhta through Verkhovyna to Kosiv. This is an honest overview: what the project is, why now, how it works, what exists, what does not yet exist, and what is still unsolved.");
}

// 2 — the idea
{
  const s = slide(C.red, S1);
  t(s, "THE IDEA IN ONE LINE", { x: 128, y: 240, w: 1664, h: 40, size: 28, color: C.onRedSoft, cs: 2 });
  t(s, "Travel that keeps a way of life alive, rather than putting it on display.", { x: 128, y: 304, w: 1520, h: 290, size: 80, serif: true, color: C.onRed, lh: 1.12 });
  t(s, "Hosts share what they really have — a bed, a meal, guidance, a craft — from where they live. A Pilgrim of the Plai comes to learn, not to look.", { x: 128, y: 630, w: 1440, h: 160, size: 36, color: C.onRedSoft, lh: 1.4 });
  footer(s, "Trans-Carpathian Pathways · 02", C.onRedSoft);
  s.addNotes("This is the whole project in one sentence. Whoever comes is a Pilgrim of the Plai: the plai is the old Carpathian path through the high pastures, from which the map takes its name, and the pilgrimage is to the mountain and its people, not to a shrine. Encounter rather than extraction: a pilgrim sleeps under a roof, eats at a table, learns how something is made, and leaves money and attention with the person who holds the knowledge. The host gains a reason, and a means, to keep that knowledge alive.");
}

// 3 & 4 — four stat cards
function statSlide(bg, sec, eyebrow, title, stats, numColor, cardFill, cardLine, statement, foot, footColor, notes) {
  const s = slide(bg, sec);
  header(s, eyebrow, title);
  const w = 392, y = 298, h = 392;
  stats.forEach(([num, text], i) => {
    const x = 128 + i * (w + 32);
    card(s, x, y, w, h, cardFill, cardLine);
    t(s, num, { x: x + 40, y: y + 40, w: w - 80, h: 92, size: 80, serif: true, color: numColor, lh: 1 });
    t(s, text, { x: x + 40, y: y + 140, w: w - 80, h: 190, size: 26, color: C.body, lh: 1.4 });
  });
  t(s, statement, { x: 128, y: 740, w: 1580, h: 130, size: 30, color: C.navy, lh: 1.4 });
  footer(s, foot, footColor);
  s.addNotes(notes);
}
statSlide(C.cream, S2, "Why now", "The mountains are being re-valued from outside", [
  ["6.5×", "A house in Polianytsia, where Bukovel lies, against one in Verkhovyna (Oct 2025)"],
  ["×4.4", "Tourist-tax receipts in Ivano-Frankivsk oblast, 2021 to 2025"],
  ["1.5 GW", "Wind power proposed on Zakarpattia's high ridges, Svydovets among them"],
  ["+690%", "Polish farmland prices over the 12-year transition after joining the EU"],
], C.red, C.card, C.border,
  "The Carpathian Eight commits to cultural landscapes and shared cultural routes, yet energy is 68% of its listed project value. Culture has a sentence; it does not yet have an instrument.",
  "Sources: Zaxid.net; oblast tourism department; CEE Bankwatch; Bórawski et al. 2019; Kyiv Post · 03", C.muted,
  "An average house was listed at about 11.7 million hryvnia in Polianytsia against 1.8 million in Verkhovyna in October 2025: that gap is the pressure the corridor now faces. Oblast tourist-tax receipts rose from 10.4 million hryvnia in 2021 to 46.2 million in 2025. Wind farms are proposed on the high meadows, and the Svydovets mega-resort would cover 1,430 hectares. Accession will in time open Ukraine's land to buyers from across the Union; Poland and Romania show what that did. At the September 2026 summit, energy was 7.28 of the 10.7 billion dollars of listed projects. None of this is an argument against energy or work in the mountains; it is an argument that the mountains' future is being decided quickly, and mostly by people who will not live in them.");
statSlide(C.sand, S2, "Not wilderness", "The meadows were made, and people keep them", [
  ["−31%", "Cattle in private households of Ivano-Frankivsk oblast, 2021 to 2024"],
  ["100+", "Craft workshops in Kosiv; its painted ceramics on UNESCO's list since 2019"],
  ["2020", "Ukraine's first geographical indication: Hutsul brynza, from six polonynas"],
  ["17,000", "Displaced people registered in Kosiv, Yaremche and Vorokhta hromadas (2025)"],
], C.green, C.cream, C.border2,
  "The high pastures were cleared by herders and stay rich only while they are mown and grazed. What needs protecting is the relationship between people and land.",
  "Sources: Suspilne; ReHERIT; UNESCO; Janišová et al. 2024 · 04", C.muted2,
  "The polonynas were cleared by Vlach pastoralists from the fourteenth and fifteenth centuries; grassland studies on both sides of the Ukrainian–Romanian border find management explains plant richness better than soil or slope, and that depopulation and falling livestock drive the change. Where grazing stops, green alder moves in. Meanwhile a craft economy survives, herders won Ukraine's first protected cheese name, and the war has brought people as well as pressure: the 17,000 are registrations, not residents. Families and newcomers are also coming to learn and live the Hutsul way of life; that we know only from anecdote, and counting them is work for the first corridor. Pathways stands with this second movement.");

// 5 — model
{
  const s = slide(C.cream, S3);
  header(s, "How it works", "Three things interlock");
  const w = 533, y = 296, h = 372;
  [
    ["Hosts", C.red, "People who share something real from where they live, and describe it as it is. Each sets their own months, capacity, languages and access."],
    ["The pathway", C.green, "Not drawn from above. It emerges as hosts join, follows existing trails, and links springs, viewpoints and places worth arriving at."],
    ["Curators and stewards", C.navy, "People of the corridor. The Curator suggests, never sells, a journey and holds the safety knowledge; stewards care for each stretch."],
  ].forEach(([h3, col, p], i) => {
    const x = 128 + i * (w + 32);
    card(s, x, y, w, h, C.card, C.border);
    t(s, h3, { x: x + 40, y: y + 40, w: w - 80, h: 52, size: 36, serif: true, color: col });
    t(s, p, { x: x + 40, y: y + 108, w: w - 80, h: 240, size: 26, color: C.body, lh: 1.45 });
  });
  const py = 712;
  t(s, "A host can offer", { x: 128, y: py + 12, w: 280, h: 40, size: 28, color: C.navy });
  let x = 432;
  [["a bed", 150], ["a meal", 170], ["local guidance", 300], ["a workshop", 230]].forEach(([label, w2]) => {
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: P(x), y: P(py), w: P(w2), h: P(64), fill: { color: C.pill }, line: { color: C.pill, width: 0 }, rectRadius: P(32) });
    t(s, label, { x, y: py, w: w2, h: 64, size: 28, color: C.navy, align: "center", valign: "middle" });
    x += w2 + 24;
  });
  footer(s, "Trans-Carpathian Pathways · 05", C.muted);
  s.addNotes("Hosts are not service providers; they choose to share what they have. The pathway is the line that joins them, adjusted by the Curator for terrain, season, capacity and the human logic of a journey. The Curator is usually a local farmer, teacher or walker, and reads every place before it is published. The pathway steward cares for a stretch and may enter a place for a host who cannot. Pilgrims need no account. A pilgrim can be a family for an afternoon or someone walking for a month.");
}

// 6 — journey
{
  const s = slide(C.sand, S3);
  header(s, "A journey", "From a host's point to a pilgrim's door");
  const w = 307, y = 300;
  rule(s, 164, y + 35, 1356, C.line, 2);
  [
    ["The host places their point", "On Plai, with the Curator or a steward beside them, consenting field by field."],
    ["The Curator reads it", "Publishes it or holds it. Safety knowledge stays off the platform."],
    ["A pilgrim asks", "Says how much time they have, who comes along, and what they hope for."],
    ["The Curator suggests", "A route between hosts, by season and capacity. Suggested, never sold."],
    ["The pilgrim walks", "Stays, eats, learns, and pays the host directly, in the form the host chose."],
  ].forEach(([h3, p], i) => {
    const x = 128 + i * (w + 32);
    s.addShape(pres.shapes.OVAL, { x: P(x), y: P(y), w: P(72), h: P(72), fill: { color: C.red }, line: { color: C.red, width: 0 } });
    t(s, String(i + 1), { x, y, w: 72, h: 72, size: 32, serif: true, color: C.onRed, align: "center", valign: "middle" });
    t(s, h3, { x, y: y + 92, w, h: 84, size: 32, serif: true, color: C.navy, lh: 1.2 });
    t(s, p, { x, y: y + 192, w, h: 200, size: 26, color: C.body, lh: 1.45 });
  });
  t(s, "A pilgrim may also find a published host on the map and go directly. Pilgrims need no account.", { x: 128, y: 748, w: 1580, h: 84, size: 28, color: C.body, lh: 1.4 });
  footer(s, "Trans-Carpathian Pathways · 06", C.muted2);
  s.addNotes("Each host chooses, for each offer, how they are paid: a fixed contribution, a suggested contribution, an exchange of work, or ubec-pay or a community currency. Payment passes directly from pilgrim to host; the project, its Curators and stewards hold no money for stays and take no share. A host may place their point at a nearby meeting place rather than the house, and say so. Every host can withdraw their place at any time; withdrawal removes it from every map and export on Plai, though not from copies someone may already have made.");
}

// 7 — Plai
{
  const s = slide(C.cream, S3);
  header(s, "Plai", "The map already exists");
  t(s, "An open-source map of the whole Carpathian range, run by UBEC on its own server in the European Union.", { x: 128, y: 298, w: 960, h: 90, size: 30, color: C.navy, lh: 1.4 });
  s.addText(bullets([
    "A host's place sits exactly where they put it",
    "Consent field by field: each person decides what is shown",
    "Withdrawal removes a place from every map and export",
    "Host fields, relief and contour lines, built and tested",
    "No advertising, no tracking, no data sold or lent",
  ], C.body), { x: P(128), y: P(432), w: P(960), h: P(360), fontFace: SANS, fontSize: 14, margin: 0, isTextBox: true, valign: "top", lineSpacingMultiple: 1.35, paraSpaceAfter: 6 });
  card(s, 1152, 298, 640, 500, C.navy, C.navy);
  t(s, "plai", { x: 1200, y: 346, w: 544, h: 66, size: 56, serif: true, italic: true, color: C.gold });
  t(s, "In the speech of these mountains, a path that follows a ridge from one pasture to the next.", { x: 1200, y: 432, w: 544, h: 130, size: 28, color: "E6DFD0", lh: 1.45 });
  t(s, [
    { text: "The name also recalls the Lviv society " }, { text: "Plai", options: { italic: true } },
    { text: " of 1924, which joined the study of the land, trail marking and the first Ukrainian mountain shelter." },
  ], { x: 1200, y: 600, w: 544, h: 170, size: 24, color: "C9C3B4", lh: 1.45 });
  footer(s, "Trans-Carpathian Pathways · 07", C.muted);
  s.addNotes("The project does not start from zero. Plai is the Carpathian hub of UBEC Mapservice: PostgreSQL and PostGIS, MapServer and Mapbender, about 32 million features from OpenStreetMap with hiking routes drawn on top, and since October 2026 relief and contour lines from the GEDTM30 ground model. Pathways is a view of Plai's entries, not a separate system: one place to enter, one consent model, one Curator queue. Photos are cleaned of location and camera data before storage. Every entrant ticks that they have read the co-creator agreement. Everything can be exported at any time, so no community depends on UBEC to keep its own data. The project claims no descent from the 1924 society; it takes the name in the same spirit.");
}

// 8 & 14 — dark 3×2 grids
function gridSlide(sec, eyebrow, title, items, titleSize, foot, notes) {
  const s = slide(C.navy, sec);
  header(s, eyebrow, title, true);
  const w = 517, H = 240;
  items.forEach(([h3, p], i) => {
    const x = 128 + (i % 3) * (w + 56), y = 300 + Math.floor(i / 3) * (H + 40);
    rule(s, x, y, w, C.rule, 2);
    t(s, h3, { x, y: y + 22, w, h: 90, size: titleSize, serif: true, color: C.gold, lh: 1.15, valign: "bottom" });
    t(s, p, { x, y: y + 124, w, h: 116, size: 25, color: C.soft, lh: 1.45 });
  });
  footer(s, foot, "B9B2A2");
  s.addNotes(notes);
}
// 9 regeneration and 10 lessons are tables
function tableSlide(bg, sec, eyebrow, title, rows, colW, size, rowH, opts) {
  const s = slide(bg, sec);
  header(s, eyebrow, title);
  const head = rows[0].map((h) => ({ text: h, options: { bold: true, color: C.moon, fill: { color: C.navy } } }));
  const body = rows.slice(1).map((r, i) => r.map((c, j) => {
    const o = { color: C.navy, fill: { color: i % 2 === opts.band ? C.sand : bg } };
    if (j === 0) { if (opts.firstMuted) o.color = C.muted; else o.bold = true; }
    if (opts.highlight && i === rows.length - 2 && j === 2) { o.color = C.red; o.bold = true; }
    return { text: c, options: o };
  }));
  s.addTable([head, ...body], {
    x: P(128), y: P(298), w: P(1664), colW: colW.map((f) => P(1664 * f)), rowH: [P(rowH[0]), ...body.map(() => P(rowH[1]))],
    fontFace: SANS, fontSize: size / 2, valign: "middle", margin: [P(10), P(20), P(10), P(20)],
    border: { type: "solid", pt: 0.5, color: opts.borderColor },
  });
  return s;
}
gridSlide(S4, "Guards", "What the project will not do", [
  ["No booking calendar", "Availability is a conversation with the Curator, not slots to fill."],
  ["No ratings", "None without the host's consent: a score teaches a host to perform for the score."],
  ["No commission", "The project takes no share of what a pilgrim pays a host."],
  ["No staged tradition", "The encounter is real, or it is nothing."],
  ["No one speaks for a community", "A host speaks for their own place; the project for itself."],
  ["No data sold", "Nothing sold, lent or tracked; every host can withdraw."],
], 36, "Trans-Carpathian Pathways · 08",
  "Each refusal answers a known failure of community tourism elsewhere. A calendar is the first step to a booking service, which turns a host into a supplier with slots to fill. Ratings turn hosts into performers. The cooperative alternative to Airbnb, Fairbnb, kept a commission and went into liquidation. A corridor shown to a ministry or a funder is the places of named hosts, never what a community wants; only a community can say that.");

{
  const s = tableSlide(C.cream, S4, "The approach", "Regeneration, not only sustainability", [
    ["", "Sustainable development", "Regeneration"],
    ["The question", "How can this continue with less harm?", "What does this place need to become more itself?"],
    ["The people", "A stakeholder group whose needs are addressed", "Participants in the place's life, who know it"],
    ["The place", "A site where generic standards apply", "The source of the design, each one different"],
    ["The aim", "Neutral: no net harm", "Net positive: more alive than before"],
  ], [0.2, 0.4, 0.4], 28, [66, 96], { band: 1, firstMuted: true, highlight: true, borderColor: C.border });
  t(s, "Where the meadows were made by mowing and grazing, holding still means losing. Less harm is not enough.", { x: 128, y: 806, w: 1560, h: 90, size: 30, color: C.navy, lh: 1.4 });
  footer(s, "After Reed (2007) and Gibbons (2020) · 09", C.muted);
  s.addNotes("Sustainable development, defined in 1987, asks how an activity can continue with less harm; it balances economy, society and environment, and the industry is one of the parties whose needs it balances. Bukovel has a sustainability office; the same owners planned the Svydovets mega-resort. That is not bad faith; it is what the frame does. Regeneration, after Reed and Gibbons, starts from the place: its question, its people, its own measure of health. Doing no harm remains the floor, not the aim. Two cautions: regeneration can be co-opted as sustainability was, and nobody certifies it. The defence is the measure, not the word.");
}
{
  const s = tableSlide(C.sand, S4, "What others learned", "Built on the lessons of comparable projects", [
    ["Project", "What it taught", "What Pathways does"],
    ["Via Transilvanica", "Upkeep is the cost that recurs", "A named steward for every stretch"],
    ["Via Dinarica", "$7M and 12 years, still donor-dependent", "People before software; steward before grant"],
    ["Czech and Slovak clubs", "A marker per section keeps a trail alive", "The pathway steward"],
    ["Community tourism", "6 of 15 “successes” paid their way", "Nothing built for pilgrims who may not come"],
    ["Fairbnb", "Imitating the incumbent ended in liquidation", "No calendar, ratings or commission"],
    ["Appalachian Trail", "A corridor imposed turned owners against it", "Corridors only from consent"],
  ], [0.22, 0.39, 0.39], 25, [62, 80], { band: 0, borderColor: C.border2 });
  footer(s, "Sources in the white paper, §7 · 10", C.muted2);
  s.addNotes("Via Transilvanica in Romania: about 1,400 kilometres built by one NGO with volunteers, an annual budget over 2.5 million euro, and 300 to 400 kilometres of marking to refresh every year; visitor counts drift between estimates. Via Dinarica: donor-built from 2010, still relying on a donor-funded support centre. The Czech club keeps about 43,000 kilometres marked with a volunteer assigned to each section; Slovakia renewed only 1,200 kilometres in 2025 for lack of funds. Goodwin and Santilli found only six of fifteen community-tourism projects economically sustainable, and many lodgings at about 5 per cent occupancy. The Appalachian Trail began in 1921 as a project of regional planning: the trail was built, the community camps were not, and compulsory purchase of a corridor met hard resistance. The lesson Pathways takes: keep the living part of the vision, not only the path.");
}

// 11 — across the arc
{
  const s = slide(C.cream, S5);
  header(s, "Across the arc", "One corridor first, then the whole range");
  const w = 485, y = 298, h = 404;
  [
    ["PHASE 1 · NOW", "The Hutsul corridor", "Vorokhta, Verkhovyna, Kosiv: the first hosts, a Curator, the corridor walked in two seasons.", true],
    ["PHASE 2", "The Ukrainian Carpathians", "Using what the pilot taught. The first corridor's co-creators decide how the project is governed.", false],
    ["PHASE 3", "Across borders", "Partner initiatives in Poland, Slovakia, Romania and beyond, under the same commitments.", false],
  ].forEach(([label, h3, p, now], i) => {
    const x = 128 + i * (w + 104);
    card(s, x, y, w, h, C.card, now ? C.red : C.border, now ? 1.5 : 0.75);
    t(s, label, { x: x + 36, y: y + 36, w: w - 72, h: 34, size: 24, bold: true, color: now ? C.red : C.muted });
    t(s, h3, { x: x + 36, y: y + 82, w: w - 72, h: 92, size: 36, serif: true, color: C.navy, lh: 1.2 });
    t(s, p, { x: x + 36, y: y + 186, w: w - 72, h: 170, size: 25, color: C.body, lh: 1.45 });
    if (i < 2) s.addShape(pres.shapes.RIGHT_ARROW, { x: P(x + w + 24), y: P(y + h / 2 - 16), w: P(56), h: P(32), fill: { color: C.line }, line: { color: C.line, width: 0 } });
  });
  t(s, "Over time, the places hosts share trace corridors where culture, landscape and nature need care as one whole: drawn from consent, never imposed, speaking only for the people on them.", { x: 128, y: 748, w: 1600, h: 90, size: 28, color: C.navy, lh: 1.4 });
  footer(s, "No phase is tied to a date: each opens when the one before has proved itself · 11", C.muted);
  s.addNotes("The Carpathian arc is one living region across the borders of seven countries or more. Pathways is bioregional before it is national. A partner initiative in each country opens its own corridor, in its own language, with its own hosts, stewards and Curators, under the same commitments on data, consent, safety and money, and with the right to leave with its data. Which countries come first is still open. On corridors, three conditions: a host agreed to be on a map, not to become evidence in a protection case, so that use needs their separate consent; a corridor crosses land of people who never joined; and a protection designation can itself raise land prices and ban the mowing that made the meadows.");
}

// 12 — law
{
  const s = slide(C.sand, S5);
  header(s, "Conditions", "Designed for wartime, within the law");
  const w = 816, H = 250;
  [
    ["The border strip", "Within 5 km of the state line, leaving a village needs a border-guard permit. No stage there until the permit route is held in writing."],
    ["Pilgrims from abroad", "Western governments advise against travel. Each pilgrim reads their own advice; the Curator briefs those who come through the Curator."],
    ["Hosting from home", "Up to 30 places without a business, if the host declares the income and keeps a guest register (Procedure 297)."],
    ["Data", "Held in Germany; contacts and photo shown only by the host's tick; handed to no one unless the law compels it."],
  ].forEach(([h3, p], i) => {
    const x = 128 + (i % 2) * (w + 32), y = 290 + Math.floor(i / 2) * (H + 24);
    card(s, x, y, w, H, C.cream, C.border2);
    t(s, h3, { x: x + 32, y: y + 30, w: w - 64, h: 48, size: 36, serif: true, color: C.navy });
    t(s, p, { x: x + 32, y: y + 90, w: w - 64, h: 120, size: 25, color: C.body, lh: 1.45 });
  });
  t(s, "Two legal reads come first: data protection before the first real account, tourism and tax law before the first pilgrim.", { x: 128, y: 850, w: 1600, h: 80, size: 26, color: C.navy, lh: 1.4 });
  footer(s, "Not legal advice; sources in the white paper, §10 · 12", C.muted2);
  s.addNotes("The pilot begins in Ukraine during the war, and is designed around that fact rather than despite it. The curfew in Ivano-Frankivsk oblast runs from midnight to five; during an air-raid alert a journey pauses. In Verkhovyna raion, a border-detachment order restricts routes to Pip Ivan, Pozhyzhevska and Lake Brebeneskul. Each host answers for their own tax and registrations, and may register as a sole proprietor instead; whether serving meals needs a food registration is a grey zone. A payment for a bed is income whatever it is called, which is why the project takes no money and means to sell no tourist product; whether its shape needs any licence, and which data-protection law governs it, are the first legal reads. The case for inviting pilgrims at all, solidarity, income and witness, and the case against, risk to guests and a home made visible, are both real.");
}

// 13 & 15 — two-column cards with lists
function twoCol(bg, sec, eyebrow, title, cols, size, H, after, afterY, afterSize, foot, notes) {
  const s = slide(bg, sec);
  header(s, eyebrow, title);
  const w = 816, y = 290;
  cols.forEach(([h3, color, items], i) => {
    const x = 128 + i * (w + 32);
    card(s, x, y, w, H, C.card, C.border);
    t(s, h3, { x: x + 36, y: y + 34, w: w - 72, h: 48, size: 36, serif: true, color });
    s.addText(bullets(items, C.body), { x: P(x + 36), y: P(y + 96), w: P(w - 72), h: P(H - 120), fontFace: SANS, fontSize: size / 2, margin: 0, isTextBox: true, valign: "top", lineSpacingMultiple: 1.35, paraSpaceAfter: 6 });
  });
  t(s, after, { x: 128, y: afterY, w: 1600, h: 90, size: afterSize, color: C.navy, lh: 1.4 });
  footer(s, foot, C.muted);
  s.addNotes(notes);
}
twoCol(C.cream, S6, "Where it stands · October 2026", "The map is ready; the people are not yet", [
  ["In place", C.green, [
    "Proposal, white paper, co-creator agreement and manual, in English and Ukrainian",
    "Plai with host fields, consent, terrain and the pathway planner",
    "Decisions on record; Gates 0 to 2 and 5 closed",
    "A test of the concept, with the public review",
  ]],
  ["Not yet", C.red, [
    "Any host or steward by name; the first Curator is the project lead for now",
    "Off-host backups, the condition for a real account",
    "A legal body: today one person holds it all",
    "Money: a pilot budget proposed, not decided",
    "The Ukrainian texts read in the corridor",
  ]],
], 25, 410, "Gate 5, the planner public, taken before Gate 3. Next: Gate 3, three to five hosts; then Gate 4, the corridor walked.", 744, 26,
  "A gate opens when its work is done, not on a date · 13",
  "The software is ahead of the agreements between people. That is the right order for a map, since the consent model had to be proven before anyone was asked to trust it; Gate 3 is the first gate whose work is a promise made to a person. The co-creator agreement is still a draft with items open: the rights in entries, governing law and retention. The pilot budget proposed is about 25,700 euro over eighteen months from the first hosts, mostly the Curator, stewards, host visits, walking the corridor and the legal reads; it waits on a grantee. Gate 4 walks Vorokhta to Kosiv once per season for two seasons, recording distance, time and what a pilgrim needed at each stage. Gate 5, the pathway planner public on Plai, was taken before Gate 3: anyone plans a way, stewards and Curators keep stretches and corridors, the Curator publishes.");

gridSlide(S6, "Honestly", "What we have not solved", [
  ["The map and “no performance”", "A pin that says “workshop” invites its host to become what the pin says."],
  ["Paid, but not a transaction", "What makes a contribution differ from a price, in words host and pilgrim share."],
  ["The Curator's power", "The memory of the path also decides who appears on it. Who chooses the Curator?"],
  ["The map as a buyer's guide", "In a rising market, old houses at exact points are a scouting list."],
  ["Enough", "How many pilgrims a village can receive before encounter becomes throughput."],
  ["Begun from outside", "The map was built by an initiative led by one person. What passes to the corridor, and when?"],
], 34, "Twelve tensions are set out in the reasoning document · 14",
  "We keep these tensions in view rather than resolving them on paper. Guards exist for each: the honest offer, no calendar and no ratings, and a Curator who reads every place before publishing; capacity per offer; a host may place their point at a nearby meeting place and tell pilgrims the rest in person; the agreement's dispute route; and the promise that before Phase 2 the first corridor's hosts, stewards and Curators decide how the project is governed. What is also not known yet: the age of the corridor's landholders, how many newcomers have settled and why, and what accession is already doing to land prices. The first visits must learn these.");

twoCol(C.cream, S6, "How we will know", "Success is not counted in pilgrims", [
  ["Signs of success", C.green, [
    "Hosts still hosting after three seasons, on their own terms",
    "A young person learning a craft or a meadow's work because the path brought them together",
    "Curators and stewards from the corridor choose the next one",
    "Pilgrims' money staying in the villages",
  ]],
  ["Signs of failure", C.red, [
    "Costumes and staged meals",
    "Prices along the path rising faster than around it",
    "One village saturated while others see no one",
    "A Curator become an agent",
  ]],
], 26, 478, "One test behind both: is this place more alive, and more able to go on, than before the pathway?", 808, 30,
  "Proposed in the white paper, §12 · 15",
  "These are proposed, and they are how the project means to be caught if it fails. Gate 4 records what can be counted honestly: enquiries, journeys, host-nights, earnings in aggregate, Curator hours, and houses sold on the corridor and whether they were on the map. A stop rule is planned: if two seasons fall below a set number of journeys, the paid role ends, hosts are told, and their data is handed back. A last failure sign: the project described by how many pilgrims it moved.");

// 16 — ask
{
  const s = slide(C.sand, S7);
  header(s, "What we ask", "Ways to take part");
  const w = 804;
  [
    ["People in the mountains", "Hosts, stewards and a first Curator; and the questions a village wants answered first."],
    ["Partners along the arc", "A corridor in your country and language, under the same commitments on data, consent, safety and money."],
    ["Funders", "A planning-and-legal grant first, then the pilot: people before software. No say over what is published; no data."],
    ["Institutions", "Hear Pathways as one concrete form of the cultural landscapes and shared routes the Carpathian Eight and Convention name."],
  ].forEach(([h3, p], i) => {
    const x = 128 + (i % 2) * (w + 56), y = 298 + Math.floor(i / 2) * 216;
    t(s, String(i + 1), { x, y: y - 6, w: 64, h: 84, size: 72, serif: true, color: C.red, lh: 1 });
    t(s, h3, { x: x + 92, y, w: w - 92, h: 50, size: 36, serif: true, color: C.navy });
    t(s, p, { x: x + 92, y: y + 60, w: w - 92, h: 130, size: 26, color: C.body, lh: 1.45 });
  });
  t(s, "Everything is open: the documents, the code and the record of every decision.", { x: 128, y: 760, w: 1600, h: 44, size: 26, color: C.body });
  footer(s, "Trans-Carpathian Pathways · 16", C.muted2);
  s.addNotes("The pilot asks people on the ground first and software second, because the map already exists. Funding pays for finding and visiting hosts, a paid first Curator under a written arrangement, walking the corridor, the two legal reads, translation and hosting. A funder gets an open account at each gate, but no say over what is published or which journeys are suggested, and no access to hosts' or pilgrims' data. We also seek technical contributors. Communities: not endorsement but attention, a reading, and word passed to people who already host, teach, herd or mow that the project exists, so that they decide for themselves whether to come forward. Ukraine holds the presidency of the Carpathian Convention after its eighth conference at the end of 2026. Documents are under CC BY-SA 4.0 and code under AGPL-3.0; all of them, and the record of every decision, are in the public repository ubeccommon/trans_carpathian_pathways.");
}

// 17 — close
{
  const s = slide(C.navy, S7);
  t(s, "TRANS-CARPATHIAN PATHWAYS", { x: 128, y: 128, w: 1664, h: 40, size: 28, color: C.gold, cs: 2 });
  t(s, "Is this place more alive, and more able to go on, than before the pathway?", { x: 128, y: 330, w: 1540, h: 300, size: 80, serif: true, color: C.moon, lh: 1.12 });
  [
    ["Michel Garand", " · UBEC", "stewardship@ubec.network"],
    ["Vasyl Yuskiv", " · Zhyva Khata", "Co-initiator"],
    ["Andriy Grushetsky", " · Tepla Gora", "Co-initiator"],
    ["The documents", "", "github.com/ubeccommon"],
  ].forEach(([name, org, sub], i) => {
    const x = 128 + i * 540;
    t(s, [{ text: name, options: { bold: true } }, { text: org }], { x, y: 832, w: 520, h: 44, size: 32, color: C.moon });
    t(s, sub, { x, y: 884, w: 520, h: 40, size: 28, color: "C9C3B4" });
  });
  s.addNotes("End on the project's one test. Offer the proposal and the white paper, in English and Ukrainian. Invite questions.");
}

pres.writeFile({ fileName: OUT }).then((f) => console.log("wrote", f));
