"""Set sheet for the Thanksgiving film "Raises for Everyone" (tg_set.py) with the four characters, and 9:16 frames
for the key shots: does everyone fit behind the table, and do faces and the form read? Writes tg_set_sheet_v1.png."""
import sys
import cairo
import kit
import brand
import tg_set as ts
import sofia_tg as st
import pam_tg as pt
import don_tg as dt
import robot_tg as rt
import robot_sheet_tg as rs
from kit import Ctx, INK
from charsheets import corp
from sofia_sheet_v4 import boxed, flush_labels

W2, H2 = 1200, 780
GREY = (0.35, 0.40, 0.50)
SEAT = ts.FEET + ts.SEAT_DROP


def wide(k, legs=2):
    ts.set_dressing(k)
    rt.robot(k, ts.POS["robot"], ts.FEET_BACK, 1.0, "stand", "eager", seed=97)
    ts.seated(k, lambda: st.sofia(k, ts.POS["sofia"], SEAT, 1.0, "aside", "neutral", look=(0.9, 0), lean=5, seed=95))
    ts.seated(k, lambda: pt.pam(k, ts.POS["pam"], SEAT, 1.0, "stand", "neutral", look=(0.8, 0), seed=96))
    dt.don(k, ts.POS["don"], ts.FEET, 1.0, dt.POSE_SLAP, "grin", look=(-0.6, 0), seed=98)
    ts.table(k, legs, form_at=(ts.POS["form"], ts.TABLE_TOP + 8))


def shot1(k):          # frame 0: the form slapped down next to the turkey, under Don's hand
    ts.set_dressing(k)
    o = dt.don(k, ts.POS["don"], ts.FEET, 1.0, dt.POSE_SLAP, "grin", look=(-0.6, 0.3), seed=98)
    hx, hy = o["hands"][1]
    ts.table(k, 2, form_at=(hx - 6, ts.TABLE_TOP + 8))
    from kit import ellipse
    ellipse(k, hx - 6, ts.TABLE_TOP + 4, 11, 8, dt.SKIN, 990, shadow=False, lw=2)     # the hand, flat on the form
    k.c.set_source_rgb(*INK); k.c.set_line_width(2); k.c.set_line_cap(1)
    for a_ in (-2.6, -2.2, -0.9, -0.5):                                              # slap lines
        import math
        k.c.move_to(hx - 6 + math.cos(a_) * 22, ts.TABLE_TOP + 4 + math.sin(a_) * 16)
        k.c.line_to(hx - 6 + math.cos(a_) * 32, ts.TABLE_TOP + 4 + math.sin(a_) * 24); k.c.stroke()


def shot3(k):          # Sofía leans to Pam
    ts.set_dressing(k)
    ts.seated(k, lambda: st.sofia(k, ts.POS["sofia"] + 20, SEAT, 1.0, "aside", "neutral", look=(0.9, 0.2), lean=7, seed=95))
    ts.seated(k, lambda: pt.pam(k, ts.POS["pam"], SEAT, 1.0, pt.POSE_READ, "read", seed=96, form=True))
    ts.table(k, 2)


def shot5(k):          # the robot snaps to Don: red
    ts.set_dressing(k)
    rt.robot(k, ts.POS["robot"] + 40, ts.FEET_BACK, 1.0, "stand", "violation", seed=97, side=-1, head_dx=8, head_rot=0.16)
    dt.don(k, ts.POS["don"] - 30, ts.FEET, 1.0, dt.POSE_LAUGH, "laugh", seed=98)
    ts.table(k, 2)


def shot8(k):          # Don tears the leg off; Sofía corrects him
    ts.set_dressing(k)
    ts.seated(k, lambda: st.sofia(k, ts.POS["pam"] + 30, SEAT, 1.0, "correct", "neutral", look=(0.9, 0), lean=-3, seed=95))
    dt.don(k, ts.POS["don"] - 40, ts.FEET, 1.0, dt.POSE_POINT, "smug", look=(-0.8, 0), seed=98, leg=(0, 172, 1))
    ts.table(k, 1)


def shot9(k):          # Pam stands, primps
    ts.set_dressing(k)
    pt.pam(k, ts.POS["pam"], ts.FEET + 8, 1.0, pt.POSE_PRIMP, "soft", look=(0.9, 0.9), seed=96)
    ts.table(k, 1)


def shot11(k):         # the leg over the verdict, the form slid back
    ts.set_dressing(k)
    s = 1.0
    scratch = Ctx(cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 4, 4)), 0)
    hx, hy = dt.don(scratch, ts.POS["don"] - 30, ts.FEET, s, dt.POSE_BLOCK, "grin", seed=98)["hands"][1]
    sx_, sy_ = hx + 47 * s * 1.5, hy
    rt.robot(k, sx_, sy_ - rt.w.HEAD_Y * s, s, "stand", "accurate", seed=97)
    dt.don(k, ts.POS["don"] - 30, ts.FEET, s, dt.POSE_BLOCK, "grin", look=(-0.8, 0.3), seed=98, leg=(3, 0, 1, 1.5))
    lx, ly = dt.don(scratch, ts.POS["don"] - 30, ts.FEET, s, dt.POSE_BLOCK, "grin", seed=98)["hands"][0]
    ts.table(k, 1, form_at=(lx - 4, ts.TABLE_TOP + 8))


SHOTS = [("1 · frame 0: the form", shot1, (590, 590, 2.1)), ("3 · Sofía and Pam", shot3, ts.CAMS["two_shot"]),
         ("5 · robot: red", shot5, (620, 470, 1.55)), ("8 · \"You failed.\"", shot8, (430, 500, 1.4)),
         ("9 · Pam stands", shot9, ts.CAMS["pam_cu"]), ("11 · \"Sign it.\"", shot11, (600, 470, 1.45))]


def frame(c, k, x, y, sc, cam, draw):
    c.save(); c.rectangle(x, y, 540 * sc, 960 * sc); c.clip()
    c.translate(x, y); c.scale(sc, sc); ts.with_cam(c, cam); draw(k)
    c.restore()
    c.set_source_rgb(*INK); c.set_line_width(1.2); c.rectangle(x, y, 540 * sc, 960 * sc); c.stroke()


def main(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "THE OFFICE, THANKSGIVING", 68, 44, 28, bold=True)
    corp(c, "\"Raises for Everyone\"  ·  Day One wall, the long table", 486, 44, 13, col=GREY)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    t = "UPTIMEZ INC. · SET SHEET · THANKSGIVING v1"
    corp(c, t, W2 - 24 - c.text_extents(t).x_advance, 30, 10, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()

    # 1. world view
    corp(c, "THE SET (WORLD VIEW)", 24, 92, 10, bold=True)
    c.save(); c.rectangle(24, 98, 470, 330); c.clip()
    c.translate(24 + (470 - 820 * 0.43) / 2, 98 + 8); c.scale(0.43, 0.43); c.translate(60, -60)
    wide(k)
    c.restore()
    c.set_source_rgb(*INK); c.set_line_width(1.2); c.rectangle(24, 98, 470, 330); c.stroke()
    corp(c, "Sofía and Pam sit on the left; Don stands at the head; the robot is behind his shoulder.", 24, 444, 9,
         col=GREY)

    # 2. the table: before and after shot 8, and the banner's footnote
    corp(c, "THE TABLE  (before shot 8  /  after: one leg gone)", 24, 476, 10, bold=True)
    for i, legs in enumerate((2, 1)):
        x = 24 + i * 238
        boxed(c, x, 482, 230, 150, "turkey, two sad sides, form" if legs == 2 else "a bare stump where the leg was")
        c.save(); c.rectangle(x, 482, 230, 134); c.clip()
        c.set_source_rgb(*kit.WALL); c.rectangle(x, 482, 230, 134); c.fill()
        c.translate(x + 115 - 420 * 0.56, 482 + 70 - ts.TABLE_TOP * 0.56); c.scale(0.56, 0.56)
        ts.table(k, legs, form_at=(ts.POS["form"], ts.TABLE_TOP + 8))
        c.restore()
    boxed(c, 24, 640, 468, 122, "the banner; its footnote is meant to be found, not read")
    c.save(); c.rectangle(24, 640, 468, 106); c.clip()
    c.set_source_rgb(*kit.WALL); c.rectangle(24, 640, 468, 106); c.fill()
    c.translate(258 - 410 * 1.0, 693 - 185 * 1.0)
    ts.banner(k, 200, 160)
    c.restore()

    # 3. 9:16 frames
    corp(c, "9:16 FRAMES FOR THE KEY SHOTS  (does everyone fit; do faces and the form read?)", 514, 92, 10, bold=True)
    sc = 0.205
    for i, (lab, fn, cam) in enumerate(SHOTS):
        x = 514 + i * 114
        frame(c, k, x, 98, sc, cam, fn)
        corp(c, lab, x, 98 + 960 * sc + 14, 9, col=GREY)

    # 4. notes
    corp(c, "NOTES", 514, 344, 10, bold=True)
    notes = ["Same wall, floor and UptimeZ sign as Day One and Christmas: viewers know the place.",
             "One leaf garland, one printed banner, the table. No desk flag: the flag is Don's tie.",
             "Banner: THANKFUL FOR OUR EMPLOYEES*, footnote \"*terms and conditions apply\". Never pointed at.",
             "Sofía and Pam sit (the table hides everything below the chest); Don stands: the boss towers.",
             "Pam rises for shot 9: the only time a seated character stands.",
             "Table: roast turkey (2 legs, then 1), MASH and STUFFING tubs with $1.99 stickers, two paper pumpkins.",
             "The form lies by Don's place; it slides to Pam (7) and back (11) along the table top.",
             "Shot 11 uses the 1.5x drumstick: the word is gone, the green glow stays."]
    for i, n in enumerate(notes):
        corp(c, "·  " + n, 514, 368 + i * 24, 11, col=INK)
    flush_labels(c)
    surf.write_to_png(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "tg_set_sheet_v1.png")
