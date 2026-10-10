"""Draw the white paper's three diagrams as SVG in English and Ukrainian.

The three show the regenerative approach against sustainable
development: where each approach aims (a line from degenerating to
regenerating), what each approach sees (three pillars to balance
against a nested living place), and the two flows in the same
mountains (extraction, which sustainability moderates, against the
regenerative loop Pathways builds). Drawn with diagrams.py's helpers
and palette, measured with the real Inter font so no label overruns.

Writes docs/whitepaper/assets/{aims,sees,flows}_{en,uk}.svg. Run on its
own, or through build_whitepaper.py, which runs it first.

SPDX-License-Identifier: AGPL-3.0-or-later

Changelog:
  v0.2 — 2026-10-09 — each diagram carries its BCP 47 language tag.
  v0.1 — 2026-10-09 — initial (Michel's word: the regeneration
         approach woven into the white paper, compared with
         sustainable development, with diagrams).
"""
from pathlib import Path

from diagrams import ACCENT, EDGE, INK, QUIET, TERRA, fits, svg, t, tagged

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "whitepaper" / "assets"
PALE = "#e3ddd0"
MOSS = "#5b7a4a"          # a quiet green for the living side


def th(x, y, text, size=12, weight="regular", fill=INK, anchor="start"):
    """Text on a white ground, for a label that sits on a line."""
    from diagrams import width
    w = width(text, size, weight) + 8
    x0 = {"start": x - 4, "middle": x - w / 2, "end": x - w + 4}[anchor]
    return (f'<rect x="{x0:.1f}" y="{y - size * 0.95:.1f}" width="{w:.1f}" height="{size * 1.3:.1f}" fill="#ffffff"/>'
            + t(x, y, text, size, weight, fill, anchor))


def wrap(text, size, weight, avail):
    """Break text into lines that fit avail, on spaces."""
    from diagrams import width
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if width(trial, size, weight) <= avail:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(x, y, text, size, avail, weight="regular", fill=INK, anchor="start", lh=None):
    lh = lh or size * 1.4
    out = []
    for i, line in enumerate(wrap(text, size, weight, avail)):
        out.append(t(x, y + i * lh, line, size, weight, fill, anchor))
    return out, y + len(wrap(text, size, weight, avail)) * lh


# ---------------------------------------------------------------- aims
def aims(L):
    """A line from degenerating to regenerating; three approaches placed on it."""
    VW, H = 600, 330
    left, right = 40, VW - 40
    y = 150
    body = [t(16, 32, L["title"], 16, "semibold")]
    fits(L["title"], 16, "semibold", VW - 32, "title")
    zero = left + (right - left) * 0.5
    # the line, the zero mark, the arrow heads
    body.append(f'<line x1="{left}" y1="{y}" x2="{right}" y2="{y}" stroke="{EDGE}" stroke-width="1.5" '
                'marker-end="url(#arrow)" marker-start="url(#arrow)"/>')
    body.append(f'<line x1="{zero}" y1="{y - 26}" x2="{zero}" y2="{y + 26}" stroke="{INK}" stroke-width="1.5"/>')
    # band labels under the line
    bands = [(left + 4, "start", L["b1"]), (zero, "middle", L["b2"]), (right - 4, "end", L["b3"])]
    for x, a, (big, small) in bands:
        fits(big, 12.5, "semibold", 190, big)
        body.append(t(x, y + 48, big, 12.5, "semibold", INK, a))
        lines, _ = para(x, y + 66, small, 11, 190, fill=QUIET, anchor=a)
        body += lines
    # the three markers above the line
    marks = [(0.18, TERRA, L["m1"]), (0.5, EDGE, L["m2"]), (0.86, ACCENT, L["m3"])]
    for f, col, (name, note) in marks:
        x = left + (right - left) * f
        body.append(f'<circle cx="{x:.1f}" cy="{y}" r="7" fill="{col}"/>')
        fits(name, 12.5, "semibold", 170, name)
        body.append(t(x, y - 58, name, 12.5, "semibold", INK, "middle"))
        lines, _ = para(x, y - 40, note, 11, 170, fill=QUIET, anchor="middle")
        body += lines
    # the sentence at the foot
    lines, yy = para(16, H - 42, L["foot"], 11.5, VW - 32, fill=INK)
    body += lines
    return svg(VW, int(yy) + 10, L["title"], body)


# ---------------------------------------------------------------- sees
def sees(L):
    """Left: three pillars to balance. Right: nested in a living place."""
    VW = 600
    body = [t(16, 32, L["title"], 16, "semibold")]
    fits(L["title"], 16, "semibold", VW - 32, "title")
    top = 60
    # two panels
    pw = 272
    xs = [16, VW - 16 - pw]
    heads = [L["left_head"], L["right_head"]]
    for x, head in zip(xs, heads):
        fits(head, 13, "semibold", pw, head)
        body.append(t(x + pw / 2, top + 14, head, 13, "semibold", INK, "middle"))
    cy = top + 150
    # left: three overlapping circles
    cx = xs[0] + pw / 2
    r = 58
    pts = [(cx - 40, cy - 22), (cx + 40, cy - 22), (cx, cy + 44)]
    for (px, py), lab in zip(pts, L["pillars"]):
        body.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r}" fill="none" stroke="{EDGE}" stroke-width="1.25"/>')
    # labels outside the circles
    body.append(t(pts[0][0] - 30, pts[0][1] - r - 8, L["pillars"][0], 12, "semibold", INK, "middle"))
    body.append(t(pts[1][0] + 30, pts[1][1] - r - 8, L["pillars"][1], 12, "semibold", INK, "middle"))
    body.append(t(pts[2][0], pts[2][1] + r + 16, L["pillars"][2], 12, "semibold", INK, "middle"))
    body.append(th(cx, cy + 4, L["balance"], 11, "regular", QUIET, "middle"))
    # right: nested circles
    cx2 = xs[1] + pw / 2
    rings = [(118, L["rings"][0], MOSS), (82, L["rings"][1], EDGE), (46, L["rings"][2], ACCENT)]
    for rr, lab, col in rings:
        body.append(f'<circle cx="{cx2:.1f}" cy="{cy:.1f}" r="{rr}" fill="none" stroke="{col}" stroke-width="1.5"/>')
    body.append(th(cx2, cy - 118 + 4, L["rings"][0], 12, "semibold", MOSS, "middle"))
    body.append(th(cx2, cy - 82 + 4, L["rings"][1], 12, "semibold", INK, "middle"))
    body.append(t(cx2, cy + 4, L["rings"][2], 12, "semibold", INK, "middle"))
    # the cycle words between the rings
    body.append(th(cx2, cy + 82 + 4, L["cycle"], 11, "regular", QUIET, "middle"))
    fits(L["cycle"], 11, "regular", 150, "cycle")
    # what each measures
    yb = cy + 150
    for x, (q, a) in zip(xs, L["measures"]):
        fits(q, 11, "semibold", pw, q)
        body.append(t(x + pw / 2, yb, q, 11, "semibold", QUIET, "middle"))
        lines, _ = para(x + pw / 2, yb + 17, a, 11.5, pw, fill=INK, anchor="middle")
        body += lines
    body.append(f'<line x1="{VW / 2}" y1="{top + 30}" x2="{VW / 2}" y2="{yb + 40}" stroke="{PALE}" stroke-width="1"/>')
    return svg(VW, yb + 70, L["title"], body)


# ---------------------------------------------------------------- flows
def flows(L):
    """Left: the line of extraction. Right: the regenerative loop."""
    VW = 600
    body = [t(16, 32, L["title"], 16, "semibold")]
    fits(L["title"], 16, "semibold", VW - 32, "title")
    top = 60
    pw = 272
    xs = [16, VW - 16 - pw]
    for x, head in zip(xs, [L["left_head"], L["right_head"]]):
        fits(head, 13, "semibold", pw, head)
        body.append(t(x + pw / 2, top + 14, head, 13, "semibold", INK, "middle"))
    arrow = f'fill="none" stroke="{EDGE}" stroke-width="1.25" marker-end="url(#arrow)"'
    # left: a straight chain downward
    bw, bh = 224, 40
    x0 = xs[0] + (pw - bw) / 2
    y = top + 36
    for i, lab in enumerate(L["chain"]):
        body.append(f'<rect x="{x0}" y="{y}" width="{bw}" height="{bh}" rx="8" fill="none" stroke="{EDGE}" stroke-width="1.25"/>')
        fits(lab, 12, "regular", bw - 16, lab)
        body.append(t(x0 + bw / 2, y + 25, lab, 12, "regular", INK, "middle"))
        if i < len(L["chain"]) - 1:
            body.append(f'<path d="M{x0 + bw / 2} {y + bh}V{y + bh + 22}" {arrow}/>')
        y += bh + 24
    yl_end = y
    # right: a loop of five boxes, laid out by hand, straight arrows between edges
    cx, y0 = xs[1] + pw / 2, top + 36 + 25
    lw, lh = 90, 50
    centres = [(cx, y0), (cx + 84, y0 + 95), (cx + 58, y0 + 200), (cx - 58, y0 + 200), (cx - 84, y0 + 95)]
    for (px, py), lab in zip(centres, L["loop"]):
        main = lab == L["loop"][0]
        body.append(f'<rect x="{px - lw / 2:.1f}" y="{py - lh / 2:.1f}" width="{lw}" height="{lh}" rx="8" fill="none" '
                    f'stroke="{ACCENT if main else EDGE}" stroke-width="{2 if main else 1.25}"/>')
        lines = wrap(lab, 10.5, "regular", lw - 10)
        assert len(lines) <= 3, lab
        yy = py - (len(lines) - 1) * 6.5 + 4
        for k, line in enumerate(lines):
            body.append(t(px, yy + k * 13, line, 10.5, "regular", INK, "middle"))
    segs = [((cx + 30, y0 + 25), (cx + 84 - 20, y0 + 95 - 25)),        # top -> right
            ((cx + 84 - 6, y0 + 95 + 25), (cx + 58 + 16, y0 + 200 - 25)),  # right -> bottom right
            ((cx + 58 - 45, y0 + 200), (cx - 58 + 45, y0 + 200)),       # bottom right -> bottom left
            ((cx - 58 - 16, y0 + 200 - 25), (cx - 84 + 6, y0 + 95 + 25)),  # bottom left -> left
            ((cx - 84 + 20, y0 + 95 - 25), (cx - 30, y0 + 25))]         # left -> top
    for (ax, ay), (bx, by) in segs:
        body.append(f'<path d="M{ax:.1f} {ay:.1f}L{bx:.1f} {by:.1f}" {arrow}/>')
    cy, R = y0 + 100, 100
    body.append(t(cx, y0 + 152, L["loop_centre"], 11, "semibold", ACCENT, "middle"))
    fits(L["loop_centre"], 11, "semibold", 120, "centre")
    # the net effect under each
    yb = max(yl_end, y0 + 200 + lh / 2 + 24) + 10
    for x, (q, a) in zip(xs, L["net"]):
        fits(q, 11, "semibold", pw, q)
        body.append(t(x + pw / 2, yb, q, 11, "semibold", QUIET, "middle"))
        lines, _ = para(x + pw / 2, yb + 17, a, 11.5, pw, fill=INK, anchor="middle")
        body += lines
    body.append(f'<line x1="{VW / 2}" y1="{top + 30}" x2="{VW / 2}" y2="{yb + 46}" stroke="{PALE}" stroke-width="1"/>')
    return svg(VW, yb + 76, L["title"], body)


EN = {
    "aims": {
        "title": "Where each approach aims",
        "b1": ("Degenerating", "The place loses what made it: people, knowledge, meadows"),
        "b2": ("Zero", "No net harm — the aim of sustainability"),
        "b3": ("Regenerating", "The place grows more alive and more able to go on"),
        "m1": ("Resort tourism", "Less harm each year, more of it"),
        "m2": ("Sustainable tourism", "The same model with its damage reduced"),
        "m3": ("Pathways", "Every visit adds to the place's capacity to continue"),
        "foot": "Sustainability asks how to do less harm. Regeneration asks what this place needs to become more itself, and builds from there. The first is a ceiling on damage; the second is a direction.",
    },
    "sees": {
        "title": "What each approach sees",
        "left_head": "Sustainable development",
        "right_head": "Regeneration",
        "pillars": ["Economy", "Society", "Environment"],
        "balance": "a balance to strike",
        "rings": ["The living land", "The people who live with it", "Their economy"],
        "cycle": "work · knowledge · care",
        "measures": [("It measures", "Impact reduced, targets met, harm offset"),
                     ("It measures", "The health of the whole, and its capacity to go on")],
    },
    "flows": {
        "title": "Two flows in the same mountains",
        "left_head": "Extraction, which sustainability moderates",
        "right_head": "Regeneration, which Pathways builds",
        "chain": ["A visitor comes for a view", "A resort sells the view",
                  "The fee leaves the valley", "The meadow is scenery, unmown",
                  "The holder grows old and sells"],
        "loop": ["Meadow mown, craft in use", "Knowledge kept by doing",
                 "A host offers what is real", "A pilgrim arrives and learns",
                 "A reason and means to stay"],
        "loop_centre": "the place itself",
        "net": [("Net effect", "Less harm per visitor; the trend unchanged"),
                ("Net effect", "Each visit adds to the place's capacity to continue")],
    },
}

UK = {
    "aims": {
        "title": "Куди веде кожен підхід",
        "b1": ("Занепад", "Місце втрачає те, що його творило: людей, знання, полонини"),
        "b2": ("Нуль", "Без шкоди в підсумку — мета сталості"),
        "b3": ("Відновлення", "Місце стає живішим і здатнішим тривати далі"),
        "m1": ("Курортний туризм", "Щороку менше шкоди — і більше туризму"),
        "m2": ("Сталий туризм", "Та сама модель зі зменшеною шкодою"),
        "m3": ("Стежки", "Кожен приїзд додає місцю сили тривати"),
        "foot": "Сталість питає, як завдавати менше шкоди. Регенерація питає, що потрібно цьому місцю, щоб стати ще більше собою, і будує від цього. Перше — стеля для шкоди; друге — напрямок.",
    },
    "sees": {
        "title": "Що бачить кожен підхід",
        "left_head": "Сталий розвиток",
        "right_head": "Регенерація",
        "pillars": ["Економіка", "Суспільство", "Довкілля"],
        "balance": "рівновага між трьома",
        "rings": ["Жива земля", "Люди, що живуть із нею", "Їхня економіка"],
        "cycle": "праця · знання · турбота",
        "measures": [("Вимірює", "Зменшений вплив, досягнуті цілі, компенсована шкода"),
                     ("Вимірює", "Здоров'я цілого та його здатність тривати")],
    },
    "flows": {
        "title": "Два потоки в тих самих горах",
        "left_head": "Видобування, яке сталість пом'якшує",
        "right_head": "Регенерація, яку будують Стежки",
        "chain": ["Гість приїздить по краєвид", "Курорт продає краєвид",
                  "Плата покидає долину", "Полонина — декорація, некошена",
                  "Господар старіє і продає"],
        "loop": ["Полонина кошена, ремесло живе", "Знання живе в руках",
                 "Господар дає справжнє", "Прочанин приходить, вчиться",
                 "Причина й змога лишитися"],
        "loop_centre": "саме це місце",
        "net": [("У підсумку", "Менше шкоди на гостя; напрямок той самий"),
                ("У підсумку", "Кожен приїзд додає місцю сили тривати")],
    },
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for lang, L in (("en", EN), ("uk", UK)):
        (OUT / f"aims_{lang}.svg").write_text(tagged(aims(L["aims"]), lang), encoding="utf-8")
        (OUT / f"sees_{lang}.svg").write_text(tagged(sees(L["sees"]), lang), encoding="utf-8")
        (OUT / f"flows_{lang}.svg").write_text(tagged(flows(L["flows"]), lang), encoding="utf-8")
        print("wrote white paper diagrams", lang)


if __name__ == "__main__":
    main()
