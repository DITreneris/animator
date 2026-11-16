"""v2, pinned (the current file is v3). THE BEST CANDIDATE: cast sheet v2 (bc_cast_sheet_v1.py = v1, kept). v2 after the outside audit: three archetypes
that read as silhouettes (hunched and uneven / a huge inverted V / a stiff rectangle), a silhouette test on the
sheet, the tiny cookie tin, Don at 0 % enthusiasm.
v1 notes: cast sheet v1. The two new candidates (cand_bc.py), Don as HEAD OF TALENT (don_bc.py) and the
props (props_bc.py), with a height line-up against the regular cast. Mom is the existing Office Noir design
(mom_on.py); her slot in the line-up is a marked placeholder until that module is in the repo.
Writes bc_cast_sheet_v2.png at 2400x3040 (drawn at 1200x1520, 2x) and bc_cast_phone_v2.png (three 360x640 frames)."""
import sys
import math
import cairo
import numpy as np
import kit
import brand
import cand_bc_v2 as cb
import don_bc_v2 as db
import don_v4 as dv
import props_bc_v2 as props
import sofia_mf as sm
import pam_ss as ps
import robot_mf as rm
from kit import Ctx, INK
from charsheets import corp
from pam_sheet_mf import boxed, flush

W2, H2 = 1200, 1520
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
        c.set_source_rgb(*INK); c.set_line_width(1.2); c.rectangle(x, y, w, h); c.stroke()
        if label:
            corp(c, label, x, y + h + 12, 8.5, col=GREY, bold=True)
    else:
        boxed(c, x, y, w, h, label, fill=fill or (1, 1, 1))
        c.save(); c.rectangle(x, y, w, h); c.clip(); draw(); c.restore()


def chair(x, seat, floor, w=70, col=(0.30, 0.33, 0.40)):
    c = k.c
    kit.rect(k, x - w / 2 + 4, seat - 86, w - 8, 80, col, 801, lw=2)
    for sx in (-1, 1):
        kit.rect(k, x + sx * (w / 2 - 8) - 3, seat + 8, 6, floor - seat - 8, (0.22, 0.22, 0.25), 803 + sx, shadow=False, lw=1.6)
    kit.rect(k, x - w / 2, seat, w, 12, col, 802, lw=2)


def silhouette(draw, x, y, w, h):
    """Draws draw(kk) (coordinates local to the box) as a flat ink shape: the faces-hidden test."""
    tmp = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(w * 2), int(h * 2))
    tc = cairo.Context(tmp); tc.scale(2, 2)
    draw(Ctx(tc, 0))
    tmp.flush()
    a = np.frombuffer(tmp.get_data(), np.uint8).reshape(int(h * 2), tmp.get_stride() // 4, 4)
    on = a[..., 3] > 120                                  # drop shadows (alpha 0.22) stay out
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
    corp(c, "(mom_on.py)", x - 28, feet - 80 * s, 8.5, col=GREY)


def main(out):
    global k
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "THE BEST CANDIDATE", 68, 44, 28, bold=True)
    corp(c, "new cast v2  ·  90 % nervous energy, 110 % confidence, 0 % enthusiasm", 400, 44, 13, col=GREY)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    t = "UPTIMEZ INC. · CHARACTER MODEL SHEET · v2"
    corp(c, t, W2 - 24 - c.text_extents(t).x_advance, 30, 10, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()

    # ---------------------------------------------------------------- 1. line-up + silhouettes
    y0 = 92
    corp(c, "HEIGHT LINE-UP  (same scale; the panel, then the candidates in interview order)", 24, y0 - 6, 10, bold=True)
    boxed(c, 24, y0, 800, 300)
    F, S = y0 + 262, 0.52
    c.set_source_rgb(0.85, 0.83, 0.78); c.set_line_width(1)
    for hh in (100, 200, 300, 400):
        c.move_to(36, F - hh * S); c.line_to(812, F - hh * S); c.stroke()
    c.set_source_rgb(*INK); c.set_line_width(1.6); c.move_to(36, F); c.line_to(812, F); c.stroke()
    rm.robot(k, 84, F, S, "stand", "eager", seed=901)
    sm.sofia(k, 186, F, S, "stand", "neutral", seed=7)
    ps.pam(k, 288, F, S, "stand", "neutral", glasses="chain", seed=40)
    db.don(k, 396, F, S, db.POSE_PEN, "flat", board="front", tense=True, seed=500)
    c.set_source_rgb(*GREY); c.set_line_width(1.2); c.set_dash([4, 4]); c.move_to(462, y0 + 14); c.line_to(462, F + 8)
    c.stroke(); c.set_dash([])
    cb.small(k, 520, F, S, "hug", "hopeful", cv=True, seed=600)
    cb.macho(k, 640, F, S, "stand", "smile", seed=700)
    mom_placeholder(762, F, S)
    for x, lab in ((84, "HR ROBOT"), (186, "SOFÍA"), (288, "PAM"), (396, "DON"), (520, "1 · SMALL ONE"),
                   (640, "2 · NICE MACHO"), (762, "3 · \"OLD LADY\"")):
        c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(9)
        corp(c, lab, x - c.text_extents(lab).x_advance / 2, F + 22, 9, col=brand.NAVY, bold=True)
    corp(c, "SILHOUETTE TEST  (faces hidden: who is who?)", 840, y0 - 6, 10, bold=True)
    boxed(c, 840, y0, 336, 300)
    sil = [(58, lambda kk: cb.small(kk, 58, 250, S, "stand", "hopeful", sweat=False, seed=600), "hunched, uneven"),
           (168, lambda kk: cb.macho(kk, 168, 250, S, "stand", "smile", seed=700), "a huge inverted V"),
           (282, lambda kk: db.don(kk, 282, 250, S, "stand", "flat", tense=True, seed=500), "a stiff rectangle")]
    for sx_, fn, lab in sil:
        silhouette(fn, 840, y0, 336, 262)
        c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(9)
        corp(c, lab, 840 + sx_ - c.text_extents(lab).x_advance / 2, F + 22, 9, col=brand.NAVY, bold=True)
    c.set_source_rgb(*INK); c.set_line_width(1.6); c.move_to(852, F); c.line_to(1164, F); c.stroke()

    # ---------------------------------------------------------------- 2. the small one
    y1 = 430
    corp(c, "1 · THE SMALL ONE", 24, y1 - 6, 12, bold=True)
    corp(c, "90 % nervous energy  ·  perfect on paper, alarming in person  ·  no name: nobody asks", 190, y1 - 6, 10, col=GREY)
    c.set_source_rgb(*ACCENT); c.rectangle(24, y1, 230, 300); c.fill()
    cb.small(k, 139, y1 + 276, 1.22, "stand", "hopeful", seed=600)
    corp(c, "FRONT · hunched, one shoulder up", 32, y1 + 292, 9, col=brand.NAVY, bold=True)
    corp(c, "FACES", 274, y1 + 10, 10, bold=True)
    for i, (f, lk, lab) in enumerate((("hopeful", (0, -0.4), "wired (default)"), ("proud", (0, 0), "\"Three degrees.\""),
                                      ("neutral", (0.7, 0), "the stare"), ("crushed", (0, 0.5), "\"Too short.\""))):
        x = 274 + i * 100
        clip_box(x, y1 + 16, 96, 116, lambda x=x, f=f, lk=lk: cb.small(k, x + 48, y1 + 74 - cb.S_HY * 0.8, 0.8, "stand", f,
                                                                      look=lk, seed=610),
                 fill=WARM if f == "crushed" else None, label=lab)
    corp(c, "MOUTHS", 274, y1 + 154, 10, bold=True)
    for i, m in enumerate(("M", "E", "F", "O", "A", "C", "U")):
        x = 274 + i * 57
        clip_box(x, y1 + 160, 54, 62, lambda x=x, m=m: cb.small(k, x + 27, y1 + 162 - (cb.S_HY + 10) * 1.0, 1.0, "stand",
                                                                "neutral", mouth=m, seed=611), label=m)
    corp(c, "POSES", 684, y1 + 10, 10, bold=True)
    poses = [("hug", "hopeful", dict(cv=True), "hugs the CV"), ("offer", "proud", dict(cv=True, tiptoe=1.0, look=(0.6, -0.5)),
                                                               "offers it, on tiptoe"),
             ("finger", "proud", dict(), "\"I built your payroll.\""), ("sag", "crushed", dict(look=(0, 0.6)), "rejected")]
    for i, (pose, f, kw, lab) in enumerate(poses):
        x = 684 + i * 124
        clip_box(x, y1 + 16, 120, 206, lambda x=x, pose=pose, f=f, kw=kw, i=i: cb.small(k, x + (46 if pose == "offer" else 60),
                                                                                       y1 + 196, 0.74, pose, f,
                                                                                       seed=620 + i, **kw),
                 fill=WARM if pose == "sag" else None, label=lab)

    def sit():
        chair(354, y1 + 262, y1 + 292 + 16, 78)
        cb.small(k, 354, y1 + 262, 0.5, "sit", "hopeful", look=(0.5, -0.4), seated=True, seed=630)
    clip_box(274, y1 + 232, 200, 68, lambda: None)
    corp(c, "On the chair his feet don't reach", 284, y1 + 252, 9.5, col=INK)
    corp(c, "the floor: two different socks.", 284, y1 + 266, 9.5, col=INK)
    corp(c, "(see the phone frame)", 284, y1 + 284, 8.5, col=GREY)
    clip_box(484, y1 + 232, 190, 68, lambda: props.cv_brick(k, 530, y1 + 268, 0.56, -0.06, 640), label=None)
    corp(c, "The CV: as thick as a", 574, y1 + 258, 9.5, col=INK)
    corp(c, "brick, tabbed.", 574, y1 + 272, 9.5, col=INK)
    boxed(c, 684, y1 + 232, 492, 68)
    for i, n in enumerate(("Posture first: head sunk, one shoulder up, knock knees, pigeon toes. Crooked glasses, pinpoint pupils.",
                           "Suit two sizes too big, tie pulled sideways. Only two extras: the pencil and the odd socks.",
                           "He is still the right answer. Don rejects him without looking up from the clipboard.")):
        corp(c, "·  " + n, 694, y1 + 252 + i * 17, 9.5, col=INK)

    # ---------------------------------------------------------------- 3. the nice macho
    y2 = 770
    corp(c, "2 · THE NICE MACHO", 24, y2 - 6, 12, bold=True)
    corp(c, "110 % confidence, and kind with it  ·  Sofía and Pam vote YES before he sits down", 196, y2 - 6, 10, col=GREY)
    c.set_source_rgb(*ACCENT); c.rectangle(24, y2, 230, 300); c.fill()
    cb.macho(k, 139, y2 + 276, 0.6, "stand", "smile", glint=True, seed=700)
    corp(c, "FRONT · shoulders 35 % wider than v1", 32, y2 + 292, 9, col=brand.NAVY, bold=True)
    corp(c, "FACES", 274, y2 + 10, 10, bold=True)
    for i, (f, lk, lab) in enumerate((("smile", (0, 0), "the grin (default)"), ("warm", (-0.8, 0.1), "to Pam, warm"),
                                      ("listen", (0, 0), "listening"), ("gracious", (0, 0), "\"No worries.\""))):
        x = 274 + i * 100
        clip_box(x, y2 + 16, 96, 116, lambda x=x, f=f, lk=lk, i=i: cb.macho(k, x + 48, y2 + 70 - cb.M_HY * 0.64, 0.64, "stand", f,
                                                                           look=lk, glint=(i == 0), seed=710),
                 fill=WARM if f == "gracious" else None, label=lab)
    corp(c, "MOUTHS", 274, y2 + 154, 10, bold=True)
    for i, m in enumerate(("M", "E", "F", "O", "A", "C", "U")):
        x = 274 + i * 57
        clip_box(x, y2 + 160, 54, 62, lambda x=x, m=m: cb.macho(k, x + 27, y2 + 162 - (cb.M_HY + 12) * 1.0, 1.0, "stand",
                                                                "listen", mouth=m, seed=711), label=m)
    corp(c, "POSES", 684, y2 + 10, 10, bold=True)
    poses = [("pen", "warm", dict(pen=True, look=(0.8, 0.3)), "\"You dropped this.\""), ("tin", "smile", dict(tin=True),
                                                                                        "the tiny tin"),
             ("wave", "smile", dict(), "hello"), ("shrug", "gracious", dict(), "rejected, still nice")]
    for i, (pose, f, kw, lab) in enumerate(poses):
        x = 684 + i * 124
        clip_box(x, y2 + 16, 120, 206, lambda x=x, pose=pose, f=f, kw=kw, i=i: cb.macho(k, x + (44 if pose in ("pen", "wave")
                                                                                              else 60), y2 + 196, 0.34,
                                                                                       pose, f, seed=720 + i, **kw),
                 fill=WARM if pose == "shrug" else None, label=lab)
    clip_box(274, y2 + 232, 200, 68, lambda: props.cookie_tin(k, 322, y2 + 278, 0.62, 740))
    corp(c, "FOR EVERYONE, in his", 368, y2 + 252, 9.5, col=INK)
    corp(c, "handwriting. In his", 368, y2 + 266, 9.5, col=INK)
    corp(c, "hands it is tiny.", 368, y2 + 280, 9.5, col=INK)

    def button():
        cb.macho(k, 530, y2 + 266 - (cb.M_BT + 73) * 1.1, 1.1, "stand", "warm", badge=False, seed=741)
    clip_box(484, y2 + 232, 92, 68, button)
    corp(c, "Two buttons,", 584, y2 + 258, 9.5, col=INK)
    corp(c, "working hard.", 584, y2 + 272, 9.5, col=INK)
    c.set_source_rgb(0.85, 0.83, 0.78); c.set_line_width(1); c.rectangle(484, y2 + 232, 190, 68); c.stroke()
    boxed(c, 684, y2 + 232, 492, 68)
    for i, n in enumerate(("A huge inverted V: wide shoulders, big upper arms, a narrow waist, enormous hands. Normal legs: human.",
                           "Square jaw with a cleft, stubble, a dark quiff, an easy grin. He looks at whoever is speaking.",
                           "Absurdly sure of himself and still kind: Don finds nothing wrong, so: \"Too distracting.\"")):
        corp(c, "·  " + n, 694, y2 + 252 + i * 17, 9.5, col=INK)

    # ---------------------------------------------------------------- 4. Don
    y3 = 1110
    corp(c, "DON · HEAD OF TALENT", 24, y3 - 6, 12, bold=True)
    corp(c, "0 % enthusiasm  ·  self-appointed, like AI Police and Agent Santa  ·  the stain is still there", 216, y3 - 6, 10, col=GREY)
    c.set_source_rgb(*ACCENT); c.rectangle(24, y3, 230, 300); c.fill()
    db.don(k, 139, y3 + 276, 0.74, "stand", "flat", tense=True, seed=500)
    corp(c, "FRONT · office v4 + a blazer too big", 32, y3 + 292, 9, col=brand.NAVY, bold=True)
    corp(c, "OFFICE v4  ·  HEAD OF TALENT", 274, y3 + 10, 10, bold=True)
    boxed(c, 274, y3 + 16, 240, 206)

    def pair():
        dv.don(k, 334, y3 + 212, 0.5, "stand", "neutral", seed=501)
        db.don(k, 452, y3 + 212, 0.5, db.POSE_PEN, "flat", board="front", tense=True, seed=501)
    c.save(); c.rectangle(274, y3 + 16, 240, 206); c.clip(); pair(); c.restore()
    corp(c, "FACES  (new: with Mom in the room)", 534, y3 + 10, 10, bold=True)
    faces = [("flat", (0, 0), None, "2: suspicious"), ("pout", (-1, 0), None, "3: \"Too distracting.\""),
             ("sheepish", (0, 0), None, "4: sits up straight"), ("hero", (0, 0), "A", "6: \"Hired!\""),
             ("mortified", (0, 0), None, "8: \"Mom...\"")]
    for i, (f, lk, m, lab) in enumerate(faces):
        x = 534 + i * 104
        clip_box(x, y3 + 16, 100, 100, lambda x=x, f=f, lk=lk, m=m: db.don(k, x + 50, y3 + 66 - db.HY * 0.72, 0.72, "stand", f,
                                                                           look=lk, mouth=m, seed=510),
                 fill=WARM if f in ("sheepish", "mortified") else None, label=lab)
    corp(c, "POSES", 534, y3 + 138, 10, bold=True)
    poses = [(db.POSE_HIDE, "sheepish", dict(board="back"), "4: hides the doodle"),
             (db.POSE_PEN, "flat", dict(board="front", tense=True), "2: pen poised"),
             (db.POSE_HIRED, "hero", dict(mouth="A"), "6: \"Hired!\""),
             ("stand", "mortified", dict(), "8: the tissue")]
    for i, (pose, f, kw, lab) in enumerate(poses):
        x = 534 + i * 104
        clip_box(x, y3 + 144, 100, 156, lambda x=x, pose=pose, f=f, kw=kw, i=i: db.don(k, x + 50, y3 + 296, 0.4, pose, f,
                                                                                      seed=520 + i, **kw),
                 fill=WARM if i in (0, 3) else None, label=lab)
    clip_box(954, y3 + 144, 106, 156, lambda: props.talent_card(k, 1007, y3 + 212, 1.9, 0.06, 540), fill=WARM,
             label="the pass")
    clip_box(1066, y3 + 144, 110, 156, lambda: props.clipboard(k, 1121, y3 + 216, 1.25, -0.05, 541),
             label="his \"notes\"")
    boxed(c, 274, y3 + 232, 240, 68)
    for i, n in enumerate(("A stiff rectangle: shoulder pads up", "by his ears, sleeves to the knuckles.",
                           "The pen hovers. He writes nothing.")):
        corp(c, n, 284, y3 + 250 + i * 15, 9.5, col=INK)

    # ---------------------------------------------------------------- notes
    y4 = 1436
    corp(c, "NOTES", 24, y4, 10, bold=True)
    notes = ["v2 after the audit: silhouettes first (hunched / inverted V / rectangle), then faces that cannot be confused.",
             "Kept from the brief: the small one is the right answer, and the macho is kind. Neither gets a name.",
             "Mom is not redrawn here: she is the Office Noir design, in an interview outfit; her module is not in the repo yet.",
             "The stain rule is broken once, by Mom, in the last beat. It is back in the next film."]
    for i, n in enumerate(notes):
        corp(c, "·  " + n, 24 + (i % 2) * 588, y4 + 22 + (i // 2) * 22, 9.5, col=INK)
    flush(c)
    surf.write_to_png(out)


def phone(out):
    """Three frames at real phone size (360x640 each): the chair and the socks, the tiny tin, the pen that never lands."""
    global k
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1080, 640)
    c = cairo.Context(surf)
    k = Ctx(c, 0)

    def room(i):
        c.set_source_rgb(*kit.WALL); c.rectangle(0, 0, 360, 640); c.fill()
        c.set_source_rgb(*kit.FLOOR); c.rectangle(0, 520, 360, 120); c.fill()
        c.set_source_rgb(0.62, 0.5, 0.36); c.rectangle(0, 512, 360, 10); c.fill()

    def f1():
        room(0)
        chair(180, 420, 560, 150)
        cb.small(k, 180, 420, 1.45, "hug", "hopeful", look=(0.3, -0.4), cv=True, seated=True, seed=600)

    def f2():
        room(1)
        cb.macho(k, 180, 800, 1.22, "tin", "smile", tin=True, glint=True, seed=700)

    def f3():
        room(2)
        db.don(k, 176, 900, 1.75, db.POSE_PEN, "flat", board="front", tense=True, seed=500)
    for i, fr in enumerate((f1, f2, f3)):
        c.save(); c.translate(360 * i, 0); c.rectangle(0, 0, 360, 640); c.clip()
        fr()
        c.restore()
        c.set_source_rgb(*INK); c.set_line_width(3); c.rectangle(360 * i, 0, 360, 640); c.stroke()
    surf.write_to_png(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "bc_cast_sheet_v2.png")
    phone(sys.argv[2] if len(sys.argv) > 2 else "bc_cast_phone_v2.png")
