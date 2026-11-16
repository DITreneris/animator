"""v1, pinned (the current file is v2). MOM, "The Best Candidate": model sheet v1 (mom_bc.py: the Office Noir character in an interview outfit).
Writes mom_bc_sheet_v1.png at 2400x2160 (1200x1080, 2x) and mom_bc_phone_v1.png (three 360x640 frames)."""
import sys
import cairo
import numpy as np
import kit
import brand
import mom_on as mo
import mom_bc_v1 as mb
import don_bc_v3 as db
import cand_bc_v3 as cb
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
    mb.mom(k, x + 90 * u, y + 404 * u, 0.8 * u, "bag", "sweet", seed=70, lean=-2)


def gag_lick(x, y, u=1.0):
    room(x, y, 180 * u, 320 * u)
    mb.mom(k, x + 84 * u, y + 470 * u, 1.0 * u, "lick", "stern", look=(0.9, 0.3), seed=70)


def gag_scrub(x, y, u=1.0):
    room(x, y, 180 * u, 320 * u)
    db.don(k, x + 136 * u, y + 404 * u, 0.8 * u, "stand", "mortified", seed=500)
    mb.mom(k, x + 54 * u, y + 404 * u, 0.8 * u, mb.wipe_at(84, db.BT + 100), "shout", look=(0.9, 0.5), thrust=0.5, seed=70)


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
    t = "UPTIMEZ INC. · CHARACTER MODEL SHEET · v1"
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
    corp(c, "MOTHER AND SON: ONE SILHOUETTE", 686, y0 + 142, 10, bold=True)
    boxed(c, 686, y0 + 148, 490, 102)
    sil = [(60, lambda kk: db.don(kk, 60, 96, 0.24, "stand", "flat", tense=True, seed=500)),
           (140, lambda kk: mb.mom(kk, 140, 96, 0.24, "stand", "stern", seed=70, bag=False, curler=False)),
           (240, lambda kk: cb.small(kk, 240, 96, 0.24, "stand", "hopeful", sweat=False, seed=600)),
           (320, lambda kk: cb.macho(kk, 320, 96, 0.24, "stand", "smile", seed=700))]
    for sx_, fn in sil:
        silhouette(fn, 686, y0 + 148, 490, 100)
    for i, n in enumerate(("Two stiff rectangles.", "Nobody on the panel", "notices. We can.")):
        corp(c, n, 1060, y0 + 186 + i * 14.5, 9.2, col=INK)

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
    corp(c, "HER THREE BEATS  (9:16, sound off)", 24, y2 - 6, 10, bold=True)
    for i, (g, lab) in enumerate(((gag_sweet, "4-6 · THE ACT"), (gag_lick, "8 · THE TISSUE"), (gag_scrub, "8 · THE REVEAL"))):
        x = 24 + i * 290
        c.save(); c.rectangle(x, y2, 276, 490); c.clip(); g(x, y2, 276 / 180.0); c.restore()
        c.set_source_rgb(*INK); c.set_line_width(1.6); c.rectangle(x, y2, 276, 490); c.stroke()
        c.set_source_rgb(*brand.NAVY); c.rectangle(x, y2, 276, 19); c.fill()
        corp(c, lab, x + 8, y2 + 13.5, 9.5, col=(1, 1, 1), bold=True)
    tx = 24 + 3 * 290 + 4
    boxed(c, tx, y2, W2 - 24 - tx, 490)
    yy = y2 + 24
    for kind, txt in [("h", "SOUND OFF, WE SEE"), ("t", "A solid old lady being"), ("t", "very sweet. Then she licks"),
                      ("t", "a tissue and scrubs the"), ("g", "boss's vest. He lets her."),
                      ("h", "WHY IT LANDS"), ("t", "The stain has been there"), ("t", "for six films and nobody"),
                      ("t", "has said a word. Only one"), ("g", "person on earth would."),
                      ("h", "CLUES, IN ORDER"), ("t", "1  Don sits up straight"), ("t", "2  \"One difficult project\""),
                      ("t", "3  the thread on his collar"), ("t", "4  the curler she forgot"), ("g", "5  the same silhouette"),
                      ("h", "RULES"), ("t", "Sweet is an act: the eyes"), ("t", "open only for Don, and"),
                      ("t", "they are never soft."), ("t", "She calls him DONNIE.")]:
        if kind == "h":
            corp(c, txt, tx + 12, yy, 9, col=brand.NAVY, bold=True); yy += 16
        else:
            corp(c, txt, tx + 12, yy, 9.6, col=INK); yy += 15
        if kind == "g":
            yy += 8
    flush(c)
    surf.write_to_png(out)


def phone(out):
    global k
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1080, 640)
    c = cairo.Context(surf)
    k = Ctx(c, 0)
    for i, g in enumerate((gag_sweet, gag_lick, gag_scrub)):
        c.save(); c.rectangle(360 * i, 0, 360, 640); c.clip()
        g(360 * i, 0, 2.0)
        c.restore()
        c.set_source_rgb(*INK); c.set_line_width(3); c.rectangle(360 * i, 0, 360, 640); c.stroke()
    surf.write_to_png(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "mom_bc_sheet_v1.png")
    phone(sys.argv[2] if len(sys.argv) > 2 else "mom_bc_phone_v1.png")
