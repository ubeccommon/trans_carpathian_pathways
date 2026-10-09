"""Draw the two proposal diagrams (network, roadmap) as SVG in English and Ukrainian.

Text is measured with the real Inter font so no label overruns its box.
Palette taken from the project logo.

Writes docs/proposal/assets/{network,roadmap}_{en,uk}.svg. Run on its own,
or through build_pdf.py, which runs it first.

The Inter font is looked for in INTER_FONT_DIR, else in
/usr/share/fonts/opentype/inter (Debian and Ubuntu's fonts-inter).

SPDX-License-Identifier: AGPL-3.0-or-later

Changelog:
  v0.3 — 2026-10-09 — each diagram carries its BCP 47 language tag (Michel's word:
         language tags in every file).
  v0.2 — 2026-10-07 — moved into the repository: writes to
         docs/proposal/assets/, font directory overridable, main().
  v0.1 — 2026-10-07 — initial, in the Claude Project.
"""
import os
from pathlib import Path
from xml.sax.saxutils import escape

from PIL import ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "proposal" / "assets"
FONT_DIR = Path(os.environ.get("INTER_FONT_DIR", "/usr/share/fonts/opentype/inter"))

INK = "#1d2027"
QUIET = "#5d5a52"
EDGE = "#8f8878"
ACCENT = "#c98a2e"       # ochre from the logo
ACCENT_FILL = "none"     # no fill: printer friendly, the ochre border carries the accent
TERRA = "#9a362b"        # terracotta from the logo

_fonts = {}


def width(text, size, weight="regular"):
    key = (size, weight)
    if key not in _fonts:
        name = {"regular": "Inter-Regular.otf", "semibold": "Inter-SemiBold.otf"}[weight]
        _fonts[key] = ImageFont.truetype(str(FONT_DIR / name), size=int(size * 10))
    return _fonts[key].getlength(text) / 10


def fits(text, size, weight, avail, where):
    w = width(text, size, weight)
    if w > avail:
        raise ValueError(f"{where}: '{text}' is {w:.0f} wide, {avail:.0f} available")


def t(x, y, text, size=12, weight="regular", fill=INK, anchor="start"):
    fw = "600" if weight == "semibold" else "400"
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="Inter" font-size="{size}" '
            f'font-weight="{fw}" fill="{fill}" text-anchor="{anchor}">{escape(text)}</text>')


def svg(w, h, title, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{escape(title)}">'
            '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" '
            f'markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{EDGE}"/>'
            '</marker></defs>' + "".join(body) + "</svg>")


# ---------------------------------------------------------------- network
def network(L):
    """A loop in two rows: Hosts -> Plai map -> Curator <-> Traveler -> Hosts."""
    W, GAP = 236, 128
    xL, xR = 16, 16 + 236 + 128
    VW = xR + W + 16
    y0 = 60
    LS, NS = 12.5, 14            # line size, name size
    body = [t(16, 32, L["title"], 16, "semibold")]
    fits(L["title"], 16, "semibold", VW - 32, "title")

    def bh(lines):
        return 48 + 18 * (len(lines) - 1) + 18

    def box(x, y, name, lines, main=False):
        fill = ACCENT_FILL if main else "none"
        stroke, sw = (ACCENT, 2) if main else (EDGE, 1.25)
        out = [f'<rect x="{x}" y="{y}" width="{W}" height="{bh(lines)}" rx="8" fill="{fill}" '
               f'stroke="{stroke}" stroke-width="{sw}"/>', t(x + 14, y + 27, name, NS, "semibold")]
        fits(name, NS, "semibold", W - 28, name)
        for i, line in enumerate(lines):
            fits(line, LS, "regular", W - 28, name)
            out.append(t(x + 14, y + 48 + 18 * i, line, LS, fill=INK if main else QUIET))
        return out

    hT = max(bh(L["hosts"][1]), bh(L["plai"][1]))
    y1 = y0 + hT + 76
    hB = max(bh(L["curator"][1]), bh(L["traveler"][1]))
    arrow = f'fill="none" stroke="{EDGE}" stroke-width="1.25" marker-end="url(#arrow)"'
    cL, cR = xL + W / 2, xR + W / 2
    body += [
        f'<path d="M{xL + W} {y0 + 48}H{xR}" {arrow}/>',                 # hosts -> plai
        f'<path d="M{cR} {y0 + bh(L["plai"][1])}V{y1}" {arrow}/>',       # plai -> curator
        f'<path d="M{xR} {y1 + 34}H{xL + W}" {arrow}/>',                 # curator -> traveler
        f'<path d="M{xL + W} {y1 + 64}H{xR}" {arrow}/>',                 # traveler -> curator
        f'<path d="M{cL} {y1}V{y0 + bh(L["hosts"][1])}" {arrow}/>',      # traveler -> hosts
    ]
    body += box(xL, y0, *L["hosts"])
    body += box(xR, y0, *L["plai"])
    body += box(xR, y1, *L["curator"], main=True)
    body += box(xL, y1, *L["traveler"])
    mx = xL + W + GAP / 2
    for key in ("suggests", "asks"):
        fits(L[key], LS, "regular", GAP - 12, key)
    body.append(t(mx, y1 + 26, L["suggests"], LS, fill=QUIET, anchor="middle"))
    body.append(t(mx, y1 + 82, L["asks"], LS, fill=QUIET, anchor="middle"))
    fits(L["walks"], LS, "regular", xR - cL - 24, "walks")
    body.append(t(cL + 12, (y0 + hT + y1) / 2 + 4, L["walks"], LS, fill=QUIET))
    return svg(VW, y1 + hB + 20, L["title"], body)


# ---------------------------------------------------------------- roadmap
def roadmap(L):
    VW = 600
    left, right = 16, VW - 16
    split = 262                     # items column starts here
    gap = 64                        # space between phases, gate sits in it
    body = [t(16, 32, L["title"], 16, "semibold")]
    fits(L["title"], 16, "semibold", VW - 32, "title")
    y = 54
    for i, (name, scope, items) in enumerate(L["phases"]):
        main = i == 0
        h = max(30 + 20 * (len(items) - 1) + 22, 76)
        fill = ACCENT_FILL if main else "none"
        stroke, sw = (ACCENT, 2) if main else (EDGE, 1.25)
        body.append(f'<rect x="{left}" y="{y}" width="{right - left}" height="{h}" rx="8" '
                    f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
        body.append(t(left + 16, y + 30, name, 13.5, "semibold"))
        body.append(t(left + 16, y + 50, scope, 12, fill=INK if main else QUIET))
        fits(name, 13.5, "semibold", split - left - 30, name)
        fits(scope, 12, "regular", split - left - 30, scope)
        body.append(f'<line x1="{split - 14}" y1="{y + 14}" x2="{split - 14}" y2="{y + h - 14}" '
                    f'stroke="#e3ddd0" stroke-width="1"/>')
        for k, item in enumerate(items):
            fits(item, 12.5, "regular", right - split - 22, name)
            cy = y + 30 + 20 * k
            body.append(f'<circle cx="{split + 3}" cy="{cy - 4}" r="2.5" '
                        f'fill="{ACCENT if main else EDGE}"/>')
            body.append(t(split + 13, cy, item, 12.5, fill=INK if main else QUIET))
        y += h
        if i < len(L["gates"]):
            gx, gy = left + 34, y + gap / 2
            body.append(f'<line x1="{gx}" y1="{y}" x2="{gx}" y2="{y + gap}" stroke="{EDGE}" '
                        f'stroke-width="1.25" marker-end="url(#arrow)"/>')
            body.append(f'<polygon points="{gx - 11},{gy} {gx},{gy - 11} {gx + 11},{gy} {gx},{gy + 11}" '
                        f'fill="{TERRA}"/>')
            g1, g2 = L["gates"][i]
            fits(g1, 12.5, "semibold", right - gx - 26, "gate")
            fits(g2, 12, "regular", right - gx - 26, "gate")
            body.append(t(gx + 22, gy - 3, g1, 12.5, "semibold"))
            body.append(t(gx + 22, gy + 14, g2, 12, fill=QUIET))
            y += gap
    return svg(VW, y + 20, L["title"], body)


EN = {
    "network": {
        "title": "Hosts make the map; the Curator turns it into a journey",
        "hosts": ("Hosts", ["Place themselves on the map", "Bed, meal, guidance, craft",
                            "Consent, field by field"]),
        "plai": ("Plai map", ["Hosts become points", "Paths drawn between them",
                              "Season, capacity, access"]),
        "curator": ("Pathway Curator", ["Knows terrain and people", "Refines the pathway",
                                        "Suggests, never prescribes"]),
        "traveler": ("Traveler", ["Brings time, company, wish", "An afternoon to a month"]),
        "suggests": "suggests a path", "asks": "asks",
        "walks": "walks, stays, eats, learns",
    },
    "roadmap": {
        "title": "The pilot corridor comes first; the whole arc follows",
        "phases": [
            ("Phase 1 — Prototype", "Hutsul corridor · now",
             ["Find and connect the first hosts", "Build host tools on Plai",
              "Establish the first Curator", "Walk the corridor end to end",
              "Document and refine"]),
            ("Phase 2 — First expansion", "Ukrainian Carpathians",
             ["Curators in neighbouring corridors", "Stage planner built from pilot data",
              "Host entry opened more widely", "Entry forms in local languages"]),
            ("Phase 3 — Trans-Carpathian", "Across the arc's countries",
             ["Partner initiatives in each country", "A cross-border Curator network",
              "One pathway across the arc"]),
        ],
        "gates": [("Gate: the corridor walked and documented",
                   "Phase 2 opens when the pilot has proved itself on the ground"),
                  ("Gate: the Ukrainian arc curated",
                   "Phase 3 opens when partners abroad are found")],
    },
}

UK = {
    "network": {
        "title": "Господарі творять мапу; Куратор перетворює її на подорож",
        "hosts": ("Господарі", ["Позначають себе на мапі", "Нічліг, їжа, супровід, ремесло",
                                "Згода — поле за полем"]),
        "plai": ("Мапа Плай", ["Господарі стають точками", "Між ними — стежки",
                               "Сезон, місткість, доступ"]),
        "curator": ("Куратор стежки", ["Знає рельєф і людей", "Уточнює маршрут",
                                       "Радить, а не нав'язує"]),
        "traveler": ("Мандрівник", ["Час, компанія, бажання", "Від пообіддя до місяця"]),
        "suggests": "радить шлях", "asks": "питає",
        "walks": "іде, ночує, їсть, учиться",
    },
    "roadmap": {
        "title": "Спершу пілотний коридор, потім уся карпатська дуга",
        "phases": [
            ("Фаза 1 — Прототип", "Гуцульський коридор · зараз",
             ["Знайти й об'єднати перших господарів", "Інструменти для господарів на Плаї",
              "Знайти першого Куратора", "Пройти коридор від початку до кінця",
              "Задокументувати й удосконалити"]),
            ("Фаза 2 — Перше розширення", "Українські Карпати",
             ["Куратори в сусідніх коридорах", "Планувальник етапів на даних пілоту",
              "Ширший доступ для господарів", "Форми внесення місцевими мовами"]),
            ("Фаза 3 — Транскарпатська", "Країни всієї дуги",
             ["Партнерські ініціативи в кожній країні", "Транскордонна мережа Кураторів",
              "Одна стежка через усю дугу"]),
        ],
        "gates": [("Перехід: коридор пройдено й задокументовано",
                   "Фаза 2 починається, коли пілот довів себе на місці"),
                  ("Перехід: українська дуга має Кураторів",
                   "Фаза 3 починається, коли знайдено партнерів за кордоном")],
    },
}


def tagged(svg_text, lang):
    """Each diagram says its language (BCP 47), as every document does."""
    return svg_text.replace("<svg ", f'<svg lang="{lang}" ', 1)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for lang, L in (("en", EN), ("uk", UK)):
        (OUT / f"network_{lang}.svg").write_text(tagged(network(L["network"]), lang), encoding="utf-8")
        (OUT / f"roadmap_{lang}.svg").write_text(tagged(roadmap(L["roadmap"]), lang), encoding="utf-8")
        print("wrote diagrams", lang)


if __name__ == "__main__":
    main()
