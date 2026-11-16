"""MOM, "The Best Candidate": model sheet v2 (mom_bc_sheet_v1.py = v1, kept). v2 after the audit: four beats
(the act, the tissue, DONNIE!, the scrub), the tissue touching her tongue and then the vest, Don obeying.
Writes mom_bc_sheet_v2.png at 2400x2160 (1200x1080, 2x) and mom_bc_phone_v2.png (four 360x640 frames)."""
import sys
import cairo
import numpy as np
import kit
import brand
import mom_on as mo
import mom_bc as mb
import don_bc as db
import cand_bc as cb
from kit import Ctx, INK
from charsheets import corp
from pam_sheet_mf import boxed, flush

W2, H2 = 1200, 1080
GREY = (0.35, 0.40, 0.50)
ACCENT = (0.90, 0.92, 0.96)
WARM = (1.0, 0.95, 0.93)
k = None


def box(x, y, w, h, draw, label=None, warm=False):
    c = k.c
    boxed(c, x, y, w, h, label, fill=WARM if warm else (1, 1, 1))
    c.save(); c.rectangle(x, y, w, h); c.clip(); draw(); c.restore()


def room(x, y, w, h, floor=0.86):
    c = k.c
    c.set_source_rgb(*kit.WALL); c.rectangle(x, y, w, h); c.fill()
    c.set_source_rgb(*kit.FLOOR); c.rectangle(x, y + h * floor, w, h * (1 - floor)); c.fill()
    c.set_source_rgb(0.62, 0.5, 0.36); c.rectangle(x, y + h * floor - h * 0.012, w, h * 0.016); c.fill()


def silhouette(draw, x, y, w, h):
    tmp = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(w * 2), int(h * 2))
    tc = cairo.Context(tmp); tc.scale(2, 2)
    draw(Ctx(tc, 0))
    tmp.flush()
    a = np.frombuffer(tmp.get_data(), np.uint8).reshape(int(h * 2), tmp.get_stride() // 4, 4)
    on = a[..., 3] > 120
    a[...] = 0
    a[on] = (int(INK[2] * 255), int(INK[1] * 255), int(INK[0] * 255), 255)
    tmp.mark_dirty()
    c = k.c
    c.save(); c.translate(x, y); c.scale(0.5, 0.5); c.set_source_surface(tmp, 0, 0); c.paint(); c.restore()


def gag_sweet(x, y, u=1.0):
    room(x, y, 180 * u, 320 * u)
    mb.mom(k, x + 90 * u, y + 404 * u, 0.8 * u, "bag", "sweet", seed=70)


def gag_lick(x, y, u=1.0):
    room(x, y, 180 * u, 320 * u)
    mb.mom(k, x + 80 * u, y + 470 * u, 1.0 * u, "lick", "stern", look=(1.0, 0.35), seed=70)


def _two(x, y, u, face, thrust, look):
    room(x, y, 180 * u, 320 * u)
    db.don(k, x + 132 * u, y + 404 * u, 0.8 * u, "stand", "obey", tense=True, seed=500)
    mb.mom(k, x + 52 * u, y + 404 * u, 0.8 * u, mb.wipe_at(80, db.BT + 96) if not thrust else "hip", face, look=look,
           thrust=thrust, seed=70, bag=False)


def gag_shout(x, y, u=1.0):
    _two(x, y, u, "shout", 0.7, (0.9, 0.3))


def gag_scrub(x, y, u=1.0):
    _two(x, y, u, "stern", 0.0, (0.9, 0.9))


def main(out):
    global k
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "MOM", 68, 44, 28, bold=True)
    corp(c, "\"The Best Candidate\"  ·  candidate 3, \"a sweet old lady\"  ·  sweet to the panel, never to Don", 150, 44, 13,
         col=GREY)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    t = "UPTIMEZ INC. · CHARACTER MODEL SHEET · v2"
    corp(c, t, W2 - 24 - c.text_extents(t).x_advance, 30, 10, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()

    y0 = 92
    c.set_source_rgb(*ACCENT); c.rectangle(24, y0, 250, 420); c.fill()
    mb.mom(k, 149, y0 + 396, 1.0, "bag", "sweet", seed=70)
    corp(c, "FRONT · the interview outfit", 32, y0 + 412, 9, col=brand.NAVY, bold=True)

    corp(c, "THE SAME WOMAN  (Office Noir, then the interview)", 290, y0 - 6, 10, bold=True)
    boxed(c, 290, y0, 380, 250)
    mo.mom(k, 362, y0 + 236, 0.6, "stand", "stern", seed=70)
    mb.mom(k, 482, y0 + 236, 0.6, "stand", "stern", seed=70, bag=False)
    for i, n in enumerate(("same head, glasses,", "pearl chain, body", "", "housecoat colours", "on a wool coat", "",
                           "one housecoat flower", "as a brooch", "", "ONE curler she", "forgot (the clue)")):
        corp(c, n, 556, y0 + 32 + i * 14.5, 9.2, col=brand.NAVY if n.startswith("ONE") or n.startswith("forgot") else INK,
             bold=n.startswith("ONE") or n.startswith("forgot"))

    corp(c, "FACES", 686, y0 - 6, 10, bold=True)
    faces = [("sweet", (0, 0), 0.0, "sweet: the act", False), ("stern", (-0.9, 0.2), 0.0, "stern: Don only", False),
             ("unimpressed", (0, 0), 0.0, "\"No.\" (to Pam)", False), ("shout", (0.9, 0.5), 0.5, "\"DONNIE!\"", True)]
    for i, (f, lk, th, lab, warm) in enumerate(faces):
        x = 686 + i * 124
        box(x, y0, 118, 250 - 134, lambda x=x, f=f, lk=lk, th=th: mb.mom(k, x + 59, y0 + 64 - mb.HY * 0.62, 0.62, "stand", f,
                                                                       look=lk, thrust=th, seed=70, bag=False), lab, warm)
    corp(c, "MOTHER AND SON: ONE SILHOUETTE, ONE RAISED EYEBROW", 686, y0 + 142, 10, bold=True)
    boxed(c, 686, y0 + 148, 490, 102)
    sil = [(60, lambda kk: db.don(kk, 60, 96, 0.24, "stand", "flat", tense=True, seed=500)),
           (140, lambda kk: mb.mom(kk, 140, 96, 0.24, "stand", "stern", seed=70, bag=False, curler=False)),
           (240, lambda kk: cb.small(kk, 240, 96, 0.24, "stand", "hopeful", sweat=False, seed=600)),
           (320, lambda kk: cb.macho(kk, 320, 96, 0.24, "stand", "smile", seed=700))]
    for sx_, fn in sil:
        silhouette(fn, 686, y0 + 148, 490, 100)
    for i, (fn, lab) in enumerate(((lambda xx: db.don(k, xx, y0 + 196 - db.HY * 0.42, 0.42, "stand", "flat", seed=500), "his look"),
                                   (lambda xx: mb.mom(k, xx, y0 + 198 - mb.HY * 0.4, 0.4, "stand", "unimpressed", seed=70,
                                                      bag=False), "her look"))):
        xx = 1052 + i * 62
        c.save(); c.rectangle(xx - 29, y0 + 156, 58, 74); c.clip(); fn(xx); c.restore()
        c.set_source_rgb(0.85, 0.83, 0.78); c.set_line_width(1); c.rectangle(xx - 29, y0 + 156, 58, 74); c.stroke()
        corp(c, lab, xx - 20, y0 + 243, 8.5, col=GREY, bold=True)

    y1 = y0 + 276
    corp(c, "POSES", 290, y1 - 6, 10, bold=True)
    poses = [("bag", "sweet", dict(), "the handbag, both hands", False),
             ("thread", "stern", dict(look=(-0.9, 0.2)), "clue 3: \"a thread\"", False),
             ("lick", "stern", dict(look=(0.9, 0.3)), "8: licks the tissue", True),
             ("hip", "unimpressed", dict(), "9: looks Pam up and down", False)]
    for i, (p, f, kw, lab, warm) in enumerate(poses):
        x = 290 + i * 224
        box(x, y1, 214, 144, lambda x=x, p=p, f=f, kw=kw: mb.mom(k, x + (124 if p == "thread" else 107), y1 + 139, 0.36, p, f,
                                                                seed=70, **kw), lab, warm)

    y2 = 548
    corp(c, "HER FOUR BEATS  (9:16, sound off)", 24, y2 - 6, 10, bold=True)
    for i, (g, lab) in enumerate(((gag_sweet, "4-6 · THE ACT (HOLD IT)"), (gag_lick, "8 · THE TISSUE"),
                                  (gag_shout, "8 · \"DONNIE!\" (BRIEF)"), (gag_scrub, "8 · THE SCRUB (THE FRAME)"))):
        x = 24 + i * 232
        c.save(); c.rectangle(x, y2, 222, 394); c.clip(); g(x, y2, 222 / 180.0); c.restore()
        c.set_source_rgb(*INK); c.set_line_width(1.6); c.rectangle(x, y2, 222, 394); c.stroke()
        c.set_source_rgb(*brand.NAVY); c.rectangle(x, y2, 222, 19); c.fill()
        corp(c, lab, x + 8, y2 + 13.5, 9.5, col=(1, 1, 1), bold=True)
    tx = 24 + 4 * 232
    boxed(c, tx, y2, W2 - 24 - tx, 394)
    yy = y2 + 22
    for kind, txt in [("h", "THE FUNNY FRAME"), ("t", "Not the shout. The scrub:"), ("t", "tight lips, eyes on the"),
                      ("t", "stain, and the boss"), ("g", "standing still for it."),
                      ("h", "DON"), ("t", "Strained smile, no teeth,"), ("t", "eyes sideways at her,"),
                      ("g", "shoulders up, one sweat bead."),
                      ("h", "CLUES, IN ORDER"), ("t", "1  Don sits up straight"), ("t", "2  \"One difficult project\""),
                      ("t", "3  the thread on his collar"), ("t", "4  the curler she forgot"), ("g", "5  silhouette, eyebrow"),
                      ("h", "RULES"), ("t", "Sweet is an act. She"), ("t", "calls him DONNIE.")]:
        if kind == "h":
            corp(c, txt, tx + 10, yy, 9, col=brand.NAVY, bold=True); yy += 15.5
        else:
            corp(c, txt, tx + 10, yy, 9.4, col=INK); yy += 14.5
        if kind == "g":
            yy += 7
    boxed(c, 24, y2 + 412, W2 - 48, 60)
    corp(c, "OPTIONAL MICRO-GAG FOR THE STORYBOARD", 36, y2 + 432, 9, col=brand.NAVY, bold=True)
    corp(c, "Don leans away by an inch. Without looking up from the stain, she pulls him back by the lapel. Costs about 0.6 s; "
            "I would take it only if the cut has room.", 36, y2 + 452, 9.6, col=INK)
    flush(c)
    surf.write_to_png(out)


def phone(out):
    global k
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1440, 640)
    c = cairo.Context(surf)
    k = Ctx(c, 0)
    for i, g in enumerate((gag_sweet, gag_lick, gag_shout, gag_scrub)):
        c.save(); c.rectangle(360 * i, 0, 360, 640); c.clip()
        g(360 * i, 0, 2.0)
        c.restore()
        c.set_source_rgb(*INK); c.set_line_width(3); c.rectangle(360 * i, 0, 360, 640); c.stroke()
    surf.write_to_png(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "mom_bc_sheet_v2.png")
    phone(sys.argv[2] if len(sys.argv) > 2 else "mom_bc_phone_v2.png")
