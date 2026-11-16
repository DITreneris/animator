"""v1, pinned (the current file is v2). PAM, "The Best Candidate": model sheet v1 (pam_bc.py: her Secret Santa look with fresh lipstick and a brooch).
Writes pam_bc_sheet_v1.png at 2400x2020 (1200x1010, 2x) and pam_bc_phone_v1.png (four 360x640 frames)."""
import sys
import cairo
import kit
import brand
import pam_ss as ps
import pam_bc_v1 as pb
import mom_bc as mb
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


def panel(x, y, u, draw_her):
    """A 180x320 frame: the wall, Pam from the waist up, the panel table across the bottom."""
    c = k.c
    c.set_source_rgb(*kit.WALL); c.rectangle(x, y, 180 * u, 320 * u); c.fill()
    draw_her()
    kit.rect(k, x - 6 * u, y + 246 * u, 192 * u, 14 * u, TABLE_TOP, 811, shadow=False, lw=2 * u)
    c.set_source_rgb(*TABLE); c.rectangle(x, y + 259 * u, 180 * u, 61 * u); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(2 * u); c.move_to(x, y + 259 * u); c.line_to(x + 180 * u, y + 259 * u); c.stroke()


def gag_lower(x, y, u=1.0):
    panel(x, y, u, lambda: pb.pam(k, x + 60 * u, y + 374 * u, 1.0 * u, pb.POSE_LOWER, "fade", look=(-1, 0.1), paddle="YES"))


def gag_kind(x, y, u=1.0):
    panel(x, y, u, lambda: pb.pam(k, x + 92 * u, y + 374 * u, 1.0 * u, pb.POSE_WRITE, "peer", note="KIND", pen=True))


def gag_ask(x, y, u=1.0):
    panel(x, y, u, lambda: pb.pam(k, x + 84 * u, y + 374 * u, 1.0 * u, pb.POSE_ASK, "neutral", mouth="E", pen=True))


def gag_mirror(x, y, u=1.0):
    c = k.c
    c.set_source_rgb(*kit.WALL); c.rectangle(x, y, 180 * u, 320 * u); c.fill()
    c.set_source_rgb(*kit.FLOOR); c.rectangle(x, y + 286 * u, 180 * u, 34 * u); c.fill()
    c.set_source_rgb(0.62, 0.5, 0.36); c.rectangle(x, y + 282 * u, 180 * u, 5 * u); c.fill()
    mb.mom(k, x + 52 * u, y + 366 * u, 0.64 * u, "bag", "unimpressed", look=(0.9, 0.3), seed=70)
    pb.pam(k, x + 134 * u, y + 366 * u, 0.64 * u, pb.POSE_MIRROR, "mirror", note="", lean=-4)


def main(out):
    global k
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "PAM", 68, 44, 28, bold=True)
    corp(c, "\"The Best Candidate\"  ·  the lead  ·  knows Don is wrong, likes him anyway", 146, 44, 13, col=GREY)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    t = "UPTIMEZ INC. · CHARACTER MODEL SHEET · v1"
    corp(c, t, W2 - 24 - c.text_extents(t).x_advance, 30, 10, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()

    y0 = 92
    c.set_source_rgb(*ACCENT); c.rectangle(24, y0, 240, 400); c.fill()
    pb.pam(k, 144, y0 + 376, 1.1, "stand", "neutral")
    corp(c, "FRONT · lipstick and a brooch for the panel", 32, y0 + 392, 9, col=brand.NAVY, bold=True)

    corp(c, "SECRET SANTA, THEN THE PANEL", 280, y0 - 6, 10, bold=True)
    boxed(c, 280, y0, 300, 230)
    ps.pam(k, 346, y0 + 218, 0.62, "stand", "neutral", glasses="low")
    pb.pam(k, 452, y0 + 218, 0.62, "stand", "neutral")
    for i, n in enumerate(("fresh lipstick,", "a shade bolder", "", "a lilac flower", "brooch", "", "glasses on,", "low on her nose")):
        corp(c, n, 506, y0 + 50 + i * 14.5, 9.2, col=INK)

    corp(c, "THE MIRROR: WHAT SHE SHARES WITH MOM", 596, y0 - 6, 10, bold=True)
    boxed(c, 596, y0, 580, 230)
    c.save(); c.rectangle(596, y0, 380, 230); c.clip()
    mb.mom(k, 690, y0 + 116 - mb.HY * 1.0, 1.0, "stand", "sweet", seed=70, bag=False)
    pb.pam(k, 880, y0 + 122 - pb.HY * 1.0, 1.0, "stand", "mirror", lean=-4)
    c.restore()
    for i, (kind, n) in enumerate([("h", "ALREADY TRUE"), ("t", "Glasses on a bead chain."), ("t", "Hair set, a neat fringe."),
                                   ("g", ""), ("h", "ADDED HERE"), ("t", "A flower brooch, on the"), ("t", "opposite side to Mom's."),
                                   ("t", "The same shut-eyed smile,"), ("t", "copied in beat 9."),
                                   ("g", ""), ("h", "THE JOKE"), ("t", "Mom looks at a smaller,"), ("t", "younger her. \"No.\"")]):
        corp(c, n, 990, y0 + 22 + i * 15.2, 9 if kind == "h" else 9.4, col=brand.NAVY if kind == "h" else INK, bold=kind == "h")

    y1 = y0 + 254
    corp(c, "FACES", 280, y1 - 6, 10, bold=True)
    faces = [("peer", (-1, 0), "cool: the macho", False), ("fade", (-1, 0.1), "disagrees with Don", False),
             ("neutral", (0, 0), "asks", False), ("mirror", (0, 0), "Mom's smile, copied", True), ("hurt", (0, 0), "after \"No.\"", False)]
    for i, (f, lk, lab, warm) in enumerate(faces):
        x = 280 + i * 124
        box(x, y1, 118, 146, lambda x=x, f=f, lk=lk: pb.pam(k, x + 59, y1 + 64 - pb.HY * 0.82, 0.82, "stand", f, look=lk), lab,
            warm)
    box(900, y1, 276, 146, lambda: pb.pam(k, 1000, y1 + 252, 0.74, pb.POSE_YES, "hopeful", paddle="YES"),
        "2-3: YES, both times")

    y2 = 536
    corp(c, "HER FOUR BEATS  (9:16, sound off)", 24, y2 - 6, 10, bold=True)
    for i, (g, lab) in enumerate(((gag_lower, "2-3 · DON SAYS NO: DOWN, SLOWLY"), (gag_kind, "3 · THE MACHO: ONE WORD"),
                                  (gag_ask, "5 · \"ANY FAMILY HERE?\""), (gag_mirror, "9 · THE MIRROR"))):
        x = 24 + i * 232
        c.save(); c.rectangle(x, y2, 222, 394); c.clip(); g(x, y2, 222 / 180.0); c.restore()
        c.set_source_rgb(*INK); c.set_line_width(1.6); c.rectangle(x, y2, 222, 394); c.stroke()
        c.set_source_rgb(*brand.NAVY); c.rectangle(x, y2, 222, 19); c.fill()
        corp(c, lab, x + 8, y2 + 13.5, 9.5, col=(1, 1, 1), bold=True)
    tx = 24 + 4 * 232
    boxed(c, tx, y2, W2 - 24 - tx, 394)
    yy = y2 + 22
    for kind, txt in [("h", "WITH DON"), ("t", "Her paddle says YES. He"), ("t", "says no. It comes down"),
                      ("t", "slowly, her eyes on him."), ("g", "She never argues."),
                      ("h", "THE MACHO"), ("t", "Sofía drops her pen. Pam"), ("t", "watches him hand it back"),
                      ("g", "and writes: KIND."),
                      ("h", "HER QUESTION"), ("t", "\"Any family in the"), ("t", "company?\" Robot: \"Family"),
                      ("t", "status is protected.\" The"), ("t", "one question that would"), ("g", "have caught it."),
                      ("h", "THE MIRROR"), ("t", "\"Call me Pam... Mum.\""), ("t", "Mom: \"No.\"")]:
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
    for i, g in enumerate((gag_lower, gag_kind, gag_ask, gag_mirror)):
        c.save(); c.rectangle(360 * i, 0, 360, 640); c.clip()
        g(360 * i, 0, 2.0)
        c.restore()
        c.set_source_rgb(*INK); c.set_line_width(3); c.rectangle(360 * i, 0, 360, 640); c.stroke()
    surf.write_to_png(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "pam_bc_sheet_v1.png")
    phone(sys.argv[2] if len(sys.argv) > 2 else "pam_bc_phone_v1.png")
