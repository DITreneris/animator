"""SOFIA, "The Best Candidate": model sheet v2 (sofia_bc_sheet_v1.py = v1, kept). v2 after the audit: cracks,
recovers, notices, judges us; one scale and one eye line across the four frames; the earrings settle after her face.
Writes sofia_bc_sheet_v2.png at 2400x2020 (1200x1010, 2x) and sofia_bc_phone_v2.png (four 360x640 frames)."""
import sys
import cairo
import kit
import brand
import sofia_mf as sm
import sofia_bc as sb
from kit import Ctx, INK
from charsheets import corp
from pam_sheet_mf import boxed, flush

W2, H2 = 1200, 1010
GREY = (0.35, 0.40, 0.50)
ACCENT = (0.90, 0.92, 0.96)
WARM = (1.0, 0.95, 0.93)
TABLE = (0.47, 0.34, 0.24)
TABLE_TOP = (0.60, 0.46, 0.33)
k = None


def box(x, y, w, h, draw, label=None, warm=False):
    c = k.c
    boxed(c, x, y, w, h, label, fill=WARM if warm else (1, 1, 1))
    c.save(); c.rectangle(x, y, w, h); c.clip(); draw(); c.restore()


def panel(x, y, u, draw_her, on_table=None):
    """A 180x320 frame: the wall, Sofía from the waist up, the panel table across the bottom."""
    c = k.c
    c.set_source_rgb(*kit.WALL); c.rectangle(x, y, 180 * u, 320 * u); c.fill()
    draw_her()
    kit.rect(k, x - 6 * u, y + 246 * u, 192 * u, 14 * u, TABLE_TOP, 811, shadow=False, lw=2 * u)
    c.set_source_rgb(*TABLE); c.rectangle(x, y + 259 * u, 180 * u, 61 * u); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(2 * u); c.move_to(x, y + 259 * u); c.line_to(x + 180 * u, y + 259 * u); c.stroke()
    if on_table:
        on_table()


def gag_fluster(x, y, u=1.0):
    panel(x, y, u, lambda: sb.sofia(k, x + 82 * u, y + 372 * u, 0.98 * u, "chest", "flustered", lag=(11, 0), pen_drop=0.3,
                                    seed=7))


def gag_yes(x, y, u=1.0):
    panel(x, y, u, lambda: sb.sofia(k, x + 82 * u, y + 372 * u, 0.98 * u, "paddle", "smile", paddle="YES", blush=0.45,
                                    lag=(-8, 0), seed=7))


def gag_side(x, y, u=1.0):
    panel(x, y, u, lambda: sb.sofia(k, x + 82 * u, y + 372 * u, 0.98 * u, "fold", "sideeye", seed=7))


def gag_cam(x, y, u=1.0):
    panel(x, y, u, lambda: sb.sofia(k, x + 82 * u, y + 372 * u, 0.98 * u, "fold", "deadpan", seed=7))


def main(out):
    global k
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "SOFÍA", 68, 44, 28, bold=True)
    corp(c, "\"The Best Candidate\"  ·  on the panel  ·  the only one doing the job, and the first to work it out", 176, 44,
         13, col=GREY)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    t = "UPTIMEZ INC. · CHARACTER MODEL SHEET · v2"
    corp(c, t, W2 - 24 - c.text_extents(t).x_advance, 30, 10, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()

    y0 = 92
    c.set_source_rgb(*ACCENT); c.rectangle(24, y0, 240, 400); c.fill()
    sb.sofia(k, 144, y0 + 378, 1.02, "stand", "neutral", seed=7)
    corp(c, "FRONT · office v4 + the panel blazer", 32, y0 + 392, 9, col=brand.NAVY, bold=True)

    corp(c, "OFFICE v4, THEN THE PANEL", 280, y0 - 6, 10, bold=True)
    boxed(c, 280, y0, 300, 230)
    sm.sofia(k, 350, y0 + 218, 0.56, "stand", "neutral", seed=7)
    sb.sofia(k, 462, y0 + 218, 0.56, "stand", "neutral", seed=7)
    for i, n in enumerate(("hoops out,", "fringe in", "", "blazer,", "sleeves", "pushed up")):
        corp(c, n, 520, y0 + 60 + i * 14.5, 9.2, col=INK)

    corp(c, "THE EARRINGS ACT TOO  (they settle about 0.4 s after her face does)", 596, y0 - 6, 10, bold=True)
    steps = [("flustered", (11, 0), 1.0, "1  startled: the chains fly"), ("smile", (-8, 0), 0.45, "2  face recovered, chains still going"),
             ("neutral", (0, 0), None, "3  settled")]
    for i, (f, lg, bl, lab) in enumerate(steps):
        x = 596 + i * 196
        box(x, y0, 188, 230, lambda x=x, f=f, lg=lg, bl=bl: sb.sofia(k, x + 94, y0 + 104 - sb.HY * 1.25, 1.25, "stand", f, lag=lg,
                                                                    blush=bl, seed=7), lab, warm=(i == 0))

    y1 = y0 + 254
    corp(c, "FACES", 280, y1 - 6, 10, bold=True)
    faces = [("neutral", (0, 0), (0, 0), "professional", False), ("flustered", (0, 0), (10, 0), "cracks", True),
             ("smile", (0, 0), (0, 0), "recovers", False), ("sideeye", (0, 0), (0, 0), "notices", False),
             ("deadpan", (0, 0), (0, 0), "judges us", False)]
    for i, (f, lk, lg, lab, warm) in enumerate(faces):
        x = 280 + i * 124
        box(x, y1, 118, 146, lambda x=x, f=f, lk=lk, lg=lg, i=i: sb.sofia(k, x + 59, y1 + 66 - sb.HY * 0.78, 0.78, "stand", f,
                                                                          look=lk, lag=lg, blush=0.4 if i == 2 else None,
                                                                          seed=7), lab, warm)
    box(900, y1, 276, 146, lambda: sb.sofia(k, 1030, y1 + 196, 0.62, "ask", "neutral", mouth="E", seed=7),
        "5: \"Where do you see yourself in five years?\"")

    y2 = 536
    corp(c, "HER FOUR BEATS  (9:16, sound off, behind the panel table)", 24, y2 - 6, 10, bold=True)
    for i, (g, lab) in enumerate(((gag_fluster, "3 · THE MACHO: ONE CRACK"), (gag_yes, "3 · RECOVERED: YES"),
                                  (gag_side, "6-7 · \"I SAW THAT\""), (gag_cam, "8 · LOOKS AT US (HOLD 0.6 s)"))):
        x = 24 + i * 232
        c.save(); c.rectangle(x, y2, 222, 394); c.clip(); g(x, y2, 222 / 180.0); c.restore()
        c.set_source_rgb(*INK); c.set_line_width(1.6); c.rectangle(x, y2, 222, 394); c.stroke()
        c.set_source_rgb(*brand.NAVY); c.rectangle(x, y2, 222, 19); c.fill()
        corp(c, lab, x + 8, y2 + 13.5, 9.5, col=(1, 1, 1), bold=True)
    tx = 24 + 4 * 232
    boxed(c, tx, y2, W2 - 24 - tx, 394)
    yy = y2 + 22
    for kind, txt in [("h", "THE MACHO"), ("t", "Hand to her chest, the pen"), ("t", "gone, the earrings"),
                      ("t", "swinging. One second."), ("g", "Then the paddle goes up."),
                      ("h", "AGAINST PAM"), ("t", "Pam stays cool and writes"), ("t", "KIND. Two different"),
                      ("g", "reasons for the same YES."),
                      ("h", "THE MOM SECTION"), ("t", "She asks the standard"), ("t", "question and is ruled"),
                      ("t", "ageist. After that she"), ("t", "watches: the curler, the"), ("t", "thread, Don's posture."),
                      ("g", "She gets there first."),
                      ("h", "RULE"), ("t", "She never says it."), ("t", "She looks at us: one"), ("t", "eyebrow, flat mouth.")]:
        if kind == "h":
            corp(c, txt, tx + 10, yy, 9, col=brand.NAVY, bold=True); yy += 15.5
        else:
            corp(c, txt, tx + 10, yy, 9.4, col=INK); yy += 14.5
        if kind == "g":
            yy += 7
    flush(c)
    surf.write_to_png(out)


def phone(out):
    global k
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1440, 640)
    c = cairo.Context(surf)
    k = Ctx(c, 0)
    for i, g in enumerate((gag_fluster, gag_yes, gag_side, gag_cam)):
        c.save(); c.rectangle(360 * i, 0, 360, 640); c.clip()
        g(360 * i, 0, 2.0)
        c.restore()
        c.set_source_rgb(*INK); c.set_line_width(3); c.rectangle(360 * i, 0, 360, 640); c.stroke()
    surf.write_to_png(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "sofia_bc_sheet_v2.png")
    phone(sys.argv[2] if len(sys.argv) > 2 else "sofia_bc_phone_v2.png")
