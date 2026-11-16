"""THE BEST CANDIDATE: cast sheet v3 (bc_cast_sheet_v1.py, _v2.py kept). v3 after the second audit: the page is for
judging character, so it keeps the line-up, the silhouette test, full-body acting poses and one signature gag per
character as a 9:16 frame; faces and mouth strips moved to bc_tech_sheet.py. Each row answers, with the sound off:
who is this, and why is Don wrong about them?
Writes bc_cast_sheet_v3.png at 2400x2800 (drawn at 1200x1400, 2x) and bc_cast_phone_v3.png (four 360x640 frames).
Mom is the Office Noir design (mom_on.py); her slot is a marked placeholder until that module is in the repo."""
import sys
import math
import cairo
import numpy as np
import kit
import brand
import cand_bc as cb
import don_bc as db
import props_bc as props
import sofia_mf as sm
import pam_ss as ps
import robot_mf as rm
from kit import Ctx, INK
from charsheets import corp
from pam_sheet_mf import boxed, flush

W2, H2 = 1200, 1400
GREY = (0.35, 0.40, 0.50)
ACCENT = (0.90, 0.92, 0.96)
WARM = (1.0, 0.95, 0.93)
k = None


def clip_box(x, y, w, h, draw, fill=None, label=None, frame=False):
    c = k.c
    if frame:
        c.save(); c.rectangle(x, y, w, h); c.clip()
        c.set_source_rgb(*(fill or kit.WALL)); c.rectangle(x, y, w, h); c.fill()
        draw()
        c.restore()
        c.set_source_rgb(*INK); c.set_line_width(1.6); c.rectangle(x, y, w, h); c.stroke()
        if label:
            corp(c, label, x, y + h + 13, 9, col=brand.NAVY, bold=True)
    else:
        boxed(c, x, y, w, h, label, fill=fill or (1, 1, 1))
        c.save(); c.rectangle(x, y, w, h); c.clip(); draw(); c.restore()


def room(x, y, w, h, floor=0.80):
    c = k.c
    c.set_source_rgb(*kit.WALL); c.rectangle(x, y, w, h); c.fill()
    c.set_source_rgb(*kit.FLOOR); c.rectangle(x, y + h * floor, w, h * (1 - floor)); c.fill()
    c.set_source_rgb(0.62, 0.5, 0.36); c.rectangle(x, y + h * floor - h * 0.012, w, h * 0.016); c.fill()


def chair(x, seat, floor, w=70, col=(0.30, 0.33, 0.40)):
    kit.rect(k, x - w / 2 + 4, seat - w * 1.2, w - 8, w * 1.15, col, 801, lw=2)
    for sx in (-1, 1):
        kit.rect(k, x + sx * (w / 2 - w * 0.1) - w * 0.04, seat + w * 0.1, w * 0.08, floor - seat - w * 0.1, (0.22, 0.22, 0.25),
                 803 + sx, shadow=False, lw=1.6)
    kit.rect(k, x - w / 2, seat, w, w * 0.16, col, 802, lw=2)


def silhouette(draw, x, y, w, h):
    """Draws draw(kk) (coordinates local to the box) as a flat ink shape: the faces-hidden test."""
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


def mom_placeholder(x, feet, s):
    """A marked gap, not a design: Mom is drawn by mom_on.py (Office Noir)."""
    c = k.c
    c.save(); c.translate(x, feet); c.scale(s, s)
    c.set_source_rgb(*GREY); c.set_line_width(2.4); c.set_dash([7, 6])
    c.arc(0, -262, 46, 0, 2 * math.pi); c.stroke()
    for cx_ in (-30, -10, 10, 30):
        c.arc(cx_, -306, 11, 0, 2 * math.pi); c.stroke()
    c.move_to(-44, -214); c.line_to(44, -214); c.line_to(52, 0); c.line_to(-52, 0); c.close_path(); c.stroke()
    c.set_dash([])
    c.restore()
    corp(c, "MOM", x - 15, feet - 120 * s, 12, col=GREY, bold=True)
    corp(c, "Office Noir design", x - 42, feet - 96 * s, 8.5, col=GREY)


# ---------------------------------------------------------------- the signature gags (drawn in a 180x320 frame)
def gag_small(x, y, u=1.0):
    room(x, y, 180 * u, 320 * u)
    chair(x + 90 * u, y + 196 * u, y + 262 * u, 84 * u)
    cb.small(k, x + 90 * u, y + 196 * u, 0.78 * u, "hug", "hopeful", look=(0.3, -0.4), cv=True, seated=True, seed=600)


def gag_macho(x, y, u=1.0):
    room(x, y, 180 * u, 320 * u)
    cb.macho(k, x + 34 * u, y + 338 * u, 0.58 * u, "pinch", "warm", look=(0.9, 0.35), pen=True, seed=700)


def gag_don_a(x, y, u=1.0):
    room(x, y, 180 * u, 320 * u, 0.9)
    db.don(k, x + 52 * u, y + 420 * u, 0.86 * u, db.POSE_DISMISS, "flat", look=(-0.7, 0.9), board="front", tense=True,
           marks=2, seed=500)


def gag_don_b(x, y, u=1.0):
    room(x, y, 180 * u, 320 * u, 0.9)
    db.don(k, x + 84 * u, y + 420 * u, 0.86 * u, db.POSE_HIRED, "beam", look=(0.6, 0.2), seed=500)


def main(out):
    global k
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "THE BEST CANDIDATE", 68, 44, 28, bold=True)
    corp(c, "cast v3  ·  character and acting  ·  sound off: who are they, and why is Don wrong?", 400, 44, 13, col=GREY)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    t = "UPTIMEZ INC. · CHARACTER SHEET · v3"
    corp(c, t, W2 - 24 - c.text_extents(t).x_advance, 30, 10, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()

    # ---------------------------------------------------------------- 1. line-up + silhouettes
    y0 = 92
    corp(c, "HEIGHT LINE-UP  (same scale; the panel, then the candidates in interview order)", 24, y0 - 6, 10, bold=True)
    boxed(c, 24, y0, 800, 280)
    F, S = y0 + 244, 0.5
    c.set_source_rgb(0.85, 0.83, 0.78); c.set_line_width(1)
    for hh in (100, 200, 300, 400):
        c.move_to(36, F - hh * S); c.line_to(812, F - hh * S); c.stroke()
    c.set_source_rgb(*INK); c.set_line_width(1.6); c.move_to(36, F); c.line_to(812, F); c.stroke()
    rm.robot(k, 80, F, S, "stand", "eager", seed=901)
    sm.sofia(k, 176, F, S, "stand", "neutral", seed=7)
    ps.pam(k, 272, F, S, "stand", "neutral", glasses="chain", seed=40)
    db.don(k, 374, F, S, db.POSE_PEN, "flat", board="front", tense=True, seed=500)
    c.set_source_rgb(*GREY); c.set_line_width(1.2); c.set_dash([4, 4]); c.move_to(440, y0 + 14); c.line_to(440, F + 8)
    c.stroke(); c.set_dash([])
    cb.small(k, 500, F, S, "hug", "hopeful", cv=True, seed=600)
    cb.macho(k, 634, F, S, "stand", "smile", seed=700)
    mom_placeholder(768, F, S)
    for x, lab in ((80, "HR ROBOT"), (176, "SOFÍA"), (272, "PAM"), (374, "DON"), (500, "1 · SMALL ONE"),
                   (634, "2 · NICE MACHO"), (768, "3 · \"OLD LADY\"")):
        c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(9)
        corp(c, lab, x - c.text_extents(lab).x_advance / 2, F + 22, 9, col=brand.NAVY, bold=True)
    corp(c, "SILHOUETTE TEST  (faces hidden)", 840, y0 - 6, 10, bold=True)
    boxed(c, 840, y0, 336, 280)
    sil = [(52, lambda kk: cb.small(kk, 52, 244, S, "stand", "hopeful", sweat=False, seed=600), "crooked, angular"),
           (164, lambda kk: cb.macho(kk, 164, 244, S, "stand", "smile", seed=700), "impossible V"),
           (286, lambda kk: db.don(kk, 286, 244, S, "stand", "flat", tense=True, seed=500), "stiff rectangle")]
    for sx_, fn, lab in sil:
        silhouette(fn, 840, y0, 336, 252)
        c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(9)
        corp(c, lab, 840 + sx_ - c.text_extents(lab).x_advance / 2, F + 22, 9, col=brand.NAVY, bold=True)
    c.set_source_rgb(*INK); c.set_line_width(1.6); c.move_to(852, F); c.line_to(1164, F); c.stroke()

    def row(y, title, sub, front, poses, gags, lines):
        corp(c, title, 24, y - 6, 12, bold=True)
        corp(c, sub, 24 + 11.5 * len(title) * 0.72 + 20, y - 6, 10, col=GREY)
        c.set_source_rgb(*ACCENT); c.rectangle(24, y, 200, 290); c.fill()
        front()
        for i, (draw, lab, warm) in enumerate(poses):
            x = 240 + i * 162
            clip_box(x, y, 154, 290, lambda x=x, draw=draw: draw(x), fill=WARM if warm else None, label=lab)
        gx = 240 + len(poses) * 162 + 8
        for i, (g, lab) in enumerate(gags):
            x = gx + i * 171
            clip_box(x, y, 163, 290, lambda x=x, g=g: g(x, y, 163 / 180.0), frame=True)
            c.set_source_rgb(*brand.NAVY); c.rectangle(x, y, 163, 17); c.fill()
            corp(c, lab, x + 6, y + 12.5, 8.5, col=(1, 1, 1), bold=True)
        tx = gx + len(gags) * 171 + 4
        boxed(c, tx, y, W2 - 24 - tx, 290)
        yy = y + 22
        for kind, txt in lines:
            if kind == "h":
                corp(c, txt, tx + 10, yy, 9, col=brand.NAVY, bold=True); yy += 15
            else:
                corp(c, txt, tx + 10, yy, 9.5, col=INK); yy += 14.5
            if kind == "g":
                yy += 7

    # ---------------------------------------------------------------- 2. the small one
    y1 = 420
    row(y1, "1 · THE SMALL ONE", "three degrees, zero social skills",
        lambda: (cb.small(k, 124, y1 + 268, 1.08, "stand", "hopeful", seed=600),
                 corp(c, "an adult genius, not a schoolboy", 32, y1 + 284, 8.5, col=brand.NAVY, bold=True)),
        [(lambda x: cb.small(k, x + 77, y1 + 250, 0.92, "finger", "proud", seed=621), "\"Three degrees.\"", False),
         (lambda x: cb.small(k, x + 58, y1 + 250, 0.92, "offer", "hopeful", cv=True, tiptoe=1.0, look=(0.6, -0.5), seed=623),
          "offers it, on tiptoe", False),
         (lambda x: cb.small(k, x + 77, y1 + 250, 0.92, "sag", "crushed", look=(0, 0.6), seed=622), "\"Too short.\"", True)],
        [(gag_small, "SIGNATURE GAG")],
        [("h", "SOUND OFF, WE SEE"), ("t", "A CV bigger than his torso,"), ("t", "three ticks on the cover."),
         ("t", "Feet that don't reach the"), ("g", "floor. Two different socks."),
         ("h", "WHY DON IS WRONG"), ("t", "He is the best on paper."), ("t", "Don never opens the paper."),
         ("g", "He looks at the chair legs."),
         ("h", "DESIGN"), ("t", "Taped glasses, one lens low;"), ("t", "eye bags, stubble, hairline;"),
         ("t", "a fist-sized tie knot;"), ("t", "one sweat drop, not three.")])

    # ---------------------------------------------------------------- 3. the nice macho
    y2 = 750
    row(y2, "2 · THE NICE MACHO", "muscles of a superhero, manners of a kindergarten teacher",
        lambda: (cb.macho(k, 124, y2 + 270, 0.56, "stand", "smile", glint=True, seed=700),
                 corp(c, "arms +35 %, harder taper", 32, y2 + 284, 8.5, col=brand.NAVY, bold=True)),
        [(lambda x: cb.macho(k, x + 77, y2 + 262, 0.5, "tin", "smile", tin=True, seed=721), "the tiny tin", False),
         (lambda x: cb.macho(k, x + 58, y2 + 262, 0.44, "wave", "smile", glint=True, seed=723), "hello", False),
         (lambda x: cb.macho(k, x + 77, y2 + 262, 0.42, "shrug", "gracious", seed=722), "\"No worries.\"", True)],
        [(gag_macho, "SIGNATURE GAG")],
        [("h", "SOUND OFF, WE SEE"), ("t", "A man too wide for the"), ("t", "frame returning a pen with"),
         ("g", "two fingertips. Pinky out."),
         ("h", "WHY DON IS WRONG"), ("t", "Strong, kind and capable:"), ("t", "nothing to object to. So:"),
         ("g", "\"Too distracting.\""),
         ("h", "THE PANEL REACTS"), ("t", "Sofía: flustered, drops"), ("t", "her own pen. Pam: cool,"),
         ("t", "watches the manners,"), ("t", "writes one word: KIND.")])

    # ---------------------------------------------------------------- 4. Don
    y3 = 1080
    row(y3, "DON · HEAD OF TALENT", "recognizes talent instantly, if it is his mother",
        lambda: (db.don(k, 124, y3 + 268, 0.7, db.POSE_PEN, "flat", board="front", tense=True, seed=500),
                 corp(c, "the pen never lands", 32, y3 + 284, 8.5, col=brand.NAVY, bold=True)),
        [(lambda x: db.don(k, x + 77, y3 + 270, 0.62, db.POSE_HIDE, "sheepish", board="back", seed=521),
          "Mom walks in: hides the doodle", True),
         (lambda x: db.don(k, x + 77, y3 + 270, 0.62, "stand", "mortified", seed=522), "the reveal: \"Mom...\"", True)],
        [(gag_don_a, "CANDIDATES 1 AND 2"), (gag_don_b, "CANDIDATE 3")],
        [("h", "SOUND OFF"), ("t", "Two red crosses,"), ("t", "no look up, a"),
         ("t", "finger at the"), ("t", "door. Then the"), ("t", "only smile in"), ("g", "the film."),
         ("h", "INVERSION"), ("t", "Least qualified"), ("t", "in the room:"), ("t", "the man with"),
         ("g", "the clipboard.")])

    flush(c)
    surf.write_to_png(out)


def phone(out):
    """Four frames at real phone size (360x640 each): the three signature gags, Don's as before and after."""
    global k
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1440, 640)
    c = cairo.Context(surf)
    k = Ctx(c, 0)
    for i, g in enumerate((gag_small, gag_macho, gag_don_a, gag_don_b)):
        c.save(); c.rectangle(360 * i, 0, 360, 640); c.clip()
        g(360 * i, 0, 2.0)
        c.restore()
        c.set_source_rgb(*INK); c.set_line_width(3); c.rectangle(360 * i, 0, 360, 640); c.stroke()
    surf.write_to_png(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "bc_cast_sheet_v3.png")
    phone(sys.argv[2] if len(sys.argv) > 2 else "bc_cast_phone_v3.png")
