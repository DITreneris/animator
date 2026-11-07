"""UptimeZ Inc. character model sheets, drawn with the same code as the episodes so they always match.
Writes 1080x1350 PNGs: one per human (body, 6 expressions, 6 poses, colours, personality, voice),
one for LAPTOP, one for CACHE, and a height line-up."""
import math
import os
import cairo
import kit
import brand
import pt42  # badge mini-marks (runtime wrapper only)
import pt4
import pt_common
from kit import Ctx, INK, rect, ellipse, text, office_bg

import os as _os
OUT = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "characters")
os.makedirs(OUT, exist_ok=True)
W2, H2 = 540, 675  # drawn at half size, written at 1080x1350

INFO = {
    "DON": ("CEO", "Shouts in capitals. Understands nothing. Softens only when something is about him.",
            "Deep and booming; whisper-soft when moved", (0.86, 0.30, 0.28)),
    "PAM": ("PROJECT MGR", "Confident editor who \"improves\" every instruction on the way down.",
            "Brisk, crisp, pleased with herself", (0.60, 0.47, 0.78)),
    "RUSH": ("SALES", "Panics first, thinks never. Types before he reads. Rejects every correction.",
            "Fast, high, breathless", (0.30, 0.66, 0.66)),
    "MAX": ("DEV", "The only sensible one. Asks the fair question, then watches it all burn.",
            "Flat and deadpan", (0.52, 0.56, 0.62)),
}
EXPR = ["neutral", "shock", "panic", "happy", "smug", "confused"]
POSES = ["stand", "point_r", "panic", "shock", "type", "pleased"]


def hexc(c):
    return "#%02X%02X%02X" % tuple(int(round(v * 255)) for v in c)


def corp(c, s, x, y, size, col=brand.NAVY, bold=False):
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    c.set_font_size(size)
    c.set_source_rgb(*col)
    c.move_to(x, y)
    c.show_text(s)


def wrap(c, s, x, y, size, width, col=brand.NAVY, lh=1.35):
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    c.set_font_size(size)
    line, yy = "", y
    for w in s.split():
        trial = (line + " " + w).strip()
        if c.text_extents(trial).x_advance > width and line:
            corp(c, line, x, yy, size, col)
            line, yy = w, yy + size * lh
        else:
            line = trial
    if line:
        corp(c, line, x, yy, size, col)
    return yy


def sheet_base(name, subtitle):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf)
    c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93)
    c.paint()
    k = Ctx(c, 0)
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, name, 68, 42, 26, bold=True)
    corp(c, subtitle, 68, 56, 10, col=(0.35, 0.40, 0.50))
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    c.set_font_size(9)
    tw = c.text_extents("UPTIMEZ INC. · CHARACTER MODEL SHEET").x_advance
    corp(c, "UPTIMEZ INC. · CHARACTER MODEL SHEET", W2 - 24 - tw, 30, 9, col=(0.35, 0.40, 0.50), bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2)
    c.move_to(24, 68); c.line_to(W2 - 24, 68); c.stroke()
    return surf, c, k


def boxed(c, x, y, w, h, label=None):
    c.set_source_rgb(1, 1, 1)
    c.rectangle(x, y, w, h); c.fill()
    c.set_source_rgb(0.85, 0.83, 0.78); c.set_line_width(1)
    c.rectangle(x, y, w, h); c.stroke()
    if label:
        corp(c, label, x + 5, y + h - 5, 7.5, col=(0.35, 0.40, 0.50))


def head_only(k, name, cx, cy, s, face, seed):
    """Draw the person so that their head is centred at (cx, cy)."""
    p = kit.PEOPLE[name]
    hy = -300 * p["h"] + 78 - 44
    pt42.branded_person(k, name, cx, cy - hy * s, s, pose="stand", face=face, seed=seed)


def human_sheet(name):
    role, pers, voice, accent = INFO[name]
    surf, c, k = sheet_base(name, role)
    p = kit.PEOPLE[name]
    # full body on the accent colour
    c.set_source_rgb(*accent)
    c.rectangle(24, 80, 190, 360); c.fill()
    pt42.branded_person(k, name, 119, 430, 0.92 / p["h"], pose="stand", face="neutral", seed=71)
    corp(c, "FRONT · NEUTRAL", 30, 434, 7.5, col=(1, 1, 1), bold=True)
    # expressions 3x2
    corp(c, "EXPRESSIONS", 228, 90, 9, bold=True)
    for i, e in enumerate(EXPR):
        x, y = 228 + (i % 3) * 98, 96 + (i // 3) * 92
        boxed(c, x, y, 92, 86, e)
        c.save(); c.rectangle(x, y, 92, 75); c.clip()
        head_only(k, name, x + 46, y + 38, 0.55, e, 80 + i)
        c.restore()
    # poses
    corp(c, "POSES", 228, 290, 9, bold=True)
    for i, ps in enumerate(POSES):
        x, y = 228 + (i % 3) * 98, 296 + (i // 3) * 82
        boxed(c, x, y, 92, 78, ps)
        c.save(); c.rectangle(x, y, 92, 68); c.clip()
        pt42.branded_person(k, name, x + 46, y + 66, 0.19 / p["h"], pose=ps, face="neutral", seed=90 + i, badge=False)
        c.restore()
    # colours
    corp(c, "COLOURS", 24, 462, 9, bold=True)
    sw = [("skin", p["skin"]), ("outfit", p["body"]), ("hair", p["hair"]), ("accent wall", accent)]
    if p.get("tie"):
        sw.insert(2, ("tie", p["tie"]))
    for i, (lbl, col) in enumerate(sw):
        x = 24 + i * 100
        c.set_source_rgb(*col); c.rectangle(x, 470, 92, 40); c.fill()
        c.set_source_rgb(*INK); c.set_line_width(1); c.rectangle(x, 470, 92, 40); c.stroke()
        corp(c, lbl, x, 522, 8, bold=True)
        corp(c, hexc(col), x, 533, 8, col=(0.35, 0.40, 0.50))
    # personality and voice
    corp(c, "PERSONALITY", 24, 562, 9, bold=True)
    wrap(c, pers, 24, 577, 10.5, 490)
    corp(c, "VOICE", 24, 622, 9, bold=True)
    corp(c, voice, 24, 637, 10.5)
    corp(c, "Badge: " + name + " · " + role + "   ·   always facing camera for reactions; faces never covered", 24, 660, 7.5,
         col=(0.35, 0.40, 0.50))
    surf.write_to_png(f"{OUT}/uptimez-{name.lower()}-sheet.png")


def laptop_sheet():
    surf, c, k = sheet_base("LAPTOP", "THE AI · DEADPAN")
    states = [("deadpan", dict(look=(0, 0))), ("looks at DON", dict(look=(-1, -0.2))),
              ("looks down", dict(look=(0, 0.8))), ("eye-roll", dict(roll=0.85))]
    for i, (lbl, kw) in enumerate(states):
        x, y = 24 + (i % 2) * 250, 84 + (i // 2) * 178
        boxed(c, x, y, 242, 170, lbl)
        rect(k, x + 30, y + 20, 182, 118, (0.18, 0.18, 0.21), 3000 + i)
        rect(k, x + 38, y + 28, 166, 102, (0.95, 0.97, 1.0), 3010 + i, shadow=False, lw=1.5)
        pt4.laptop_face(k, x + 121, y + 70, scale=0.75, **kw)
    corp(c, "RULES", 24, 460, 9, bold=True)
    for j, line in enumerate([
        "An ordinary laptop, not a robot or mascot. No brand logos.",
        "Face = two dots and a flat line. It never smiles.",
        "It is the only competent one: it does exactly what it is told, offers the right answer, gets overruled.",
        "Its one expression is the final eye-roll, used once, as a button after the punchline.",
    ]):
        wrap(c, "• " + line, 24, 478 + j * 34, 10.5, 490)
    corp(c, "VOICE", 24, 622, 9, bold=True)
    corp(c, "None. It speaks only through the screen: system dialogs, chimes, a tiny blip.", 24, 637, 10.5)
    surf.write_to_png(f"{OUT}/uptimez-laptop-sheet.png")


def cache_sheet():
    surf, c, k = sheet_base("CACHE", "THE OFFICE CAT · BACKGROUND ONLY")
    boxed(c, 24, 84, 492, 250, "asleep (the only pose)")
    pt4.big_tile(k, "AUTHENTIC!", 260, 280, 4000, rot=0.05)
    pt_common.cat(k, 210, 262)
    corp(c, "RULES", 24, 370, 9, bold=True)
    for j, line in enumerate([
        "Silent. Never speaks, never reacts. Always asleep.",
        "Background only: never competes with a face or a punchline.",
        "Ends up asleep on whatever the humans threw away (the dropped word tiles).",
        "Name is a tech pun: CACHE. A future episode may finally wake him.",
    ]):
        wrap(c, "• " + line, 24, 388 + j * 34, 10.5, 490)
    surf.write_to_png(f"{OUT}/uptimez-cache-sheet.png")


def lineup_sheet():
    surf, c, k = sheet_base("THE TEAM", "HEIGHT LINE-UP")
    base = 590
    c.set_source_rgb(0.80, 0.78, 0.72); c.set_line_width(1)
    for i in range(0, 8):
        y = base - i * 60
        c.move_to(24, y); c.line_to(W2 - 24, y); c.stroke()
        corp(c, str(i * 60), 26, y - 3, 7, col=(0.55, 0.58, 0.65))
    for n, x in [("DON", 92), ("PAM", 190), ("RUSH", 285), ("MAX", 378)]:
        pt42.branded_person(k, n, x, base, 0.95, pose="stand", face="neutral", seed=120 + x)
        corp(c, n, x - 15, base + 22, 11, bold=True)
    # LAPTOP on its desk, CACHE asleep in front of it
    rect(k, 430, base - 66, 92, 66, (0.45, 0.30, 0.19), 5000)
    rect(k, 440, base - 132, 72, 60, (0.18, 0.18, 0.21), 5001)
    rect(k, 445, base - 127, 62, 50, (0.95, 0.97, 1.0), 5002, shadow=False, lw=1.5)
    pt4.laptop_face(k, 476, base - 106, scale=0.33)
    pt_common.cat(k, 448, base - 26)
    corp(c, "LAPTOP + CACHE", 424, base + 22, 9, bold=True)
    corp(c, "Grid = 60 px at sheet scale. DON is the tallest and widest: he always reads as the boss.", 24, 650, 9,
         col=(0.35, 0.40, 0.50))
    surf.write_to_png(f"{OUT}/uptimez-team-lineup.png")


if __name__ == "__main__":
    for n in INFO:
        human_sheet(n)
    laptop_sheet()
    cache_sheet()
    lineup_sheet()
    print(sorted(os.listdir(OUT)))
