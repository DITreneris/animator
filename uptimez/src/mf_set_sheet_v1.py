"""v1 (pinned; mf_set_sheet.py writes v2). Set sheet for "Mandatory Fun" (mf_set.py) with the four characters (sofia_mf v2, don_mf v2, pam_mf v2,
robot_mf v2) and 9:16 frames for the key shots. Writes mf_set_sheet_v1.png at 2400x1560 (drawn at 1200x780, 2x)."""
import sys
import math
import cairo
import kit
import brand
import mf_set_v1 as ms
import sofia_mf as sm
import don_mf as dm
import pam_mf as pm
import robot_mf as rm
import props_mf as pr
import emoji as _emoji
from kit import Ctx, INK
from charsheets import corp
from sofia_sheet_v4 import boxed, flush_labels

W2, H2 = 1200, 780
GREY = (0.35, 0.40, 0.50)
SEAT = ms.FEET + ms.SEAT_DROP
X = ms.POS
PAM_ARM = pm.ik(-1, -34, pm.BT + 52) + (8, 0)          # seated, the cuffed left forearm resting on the table


def sofia_writing(k, look=(0, 0.6), face="neutral", turn=0.0):
    o = {}
    ms.seated(k, lambda: o.update(sm.sofia(k, X["sofia"], SEAT, 1.0, "write", face, look=look, seed=95)))
    return o


def sofia_props(k, o, state="open", turn=0.0):
    (lx, ly), (rx, ry) = o["hands"]
    sm.notebook(k, X["sofia"] + 2, ms.TABLE_TOP + 4, 0.62, state, turn)
    for hx, hy in o["hands"]:
        kit.ellipse(k, hx, min(hy, ms.TABLE_TOP + 2), 8.5, 8.5, sm.SKIN, 1403, shadow=False, lw=2)
    sm.pen(k, rx, min(ry, ms.TABLE_TOP + 2), 1.0, 0.55)


def pam_seated(k, pose="stand", face="neutral", **kw):
    o = {}
    ms.seated(k, lambda: o.update(pm.pam(k, X["pam"], SEAT, 1.0, pose, face, seed=96, **kw)))
    return o


def base(k, door_open=0.0, empty_chair=True):
    ms.set_dressing(k, door_open)
    for key in ("sofia", "pam") + (("don",) if empty_chair else ()):
        ms.chair_back(k, X[key], seed=130)


def pop(k, x, y, r):
    c = k.c
    c.set_source_rgba(0, 0, 0, 0.12); c.arc(x + 3, y + 4, r, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(1.0, 0.91, 0.93); c.arc(x, y, r, 0, 2 * math.pi); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(2.4); c.stroke()
    _emoji.draw_emoji(c, "\U0001F497", x, y, r * 1.25)


def chain_on_table(k, don_cuff):
    """Pam's cuffed wrist on the table; the chain to Don's cuff (drawn over the table)."""
    (px_, py_) = (X["pam"] - 52, ms.TABLE_TOP - 2)
    kit.ellipse(k, px_ - 8, py_, 9, 9, pm.SKIN, 7, shadow=False, lw=2)
    pc = pr.cuff(k, px_ + 6, py_ - 1, 1.0, math.pi / 2, loop_side=1)
    pr.chain(k, don_cuff[0], don_cuff[1], pc[0], pc[1], 1.0, sag=0.0 if don_cuff[0] < X["don"] - 60 else 0.2)


def wide(k):
    base(k)
    rm.robot(k, X["robot"], ms.FEET_BACK, 1.0, "stand", "eager", seed=97)
    o = sofia_writing(k)
    pam_seated(k, "stand", "read")
    ms.table(k)
    sofia_props(k, o)


def shot1(k):              # frame 0: the slide slams on, the robot beside it
    base(k)
    rm.robot(k, X["robot"], ms.FEET_BACK, 1.0, "stand", "eager", talk=0.6, seed=97)
    c = k.c
    x, y, w, h = ms.SCREEN
    c.set_source_rgb(*INK); c.set_line_width(3); c.set_line_cap(1)            # the slam
    for a in (-2.4, -2.0, -1.1, -0.7):
        c.move_to(x + w / 2 + math.cos(a) * (w * 0.62), y + h / 2 + math.sin(a) * (h * 0.7))
        c.line_to(x + w / 2 + math.cos(a) * (w * 0.72), y + h / 2 + math.sin(a) * (h * 0.82)); c.stroke()


def shot3(k):              # the door bangs open: Don's hero pose
    base(k, door_open=1.0)
    dm.don(k, X["door"] + 20, ms.FLOOR_Y + 40, 0.95, dm.POSE_HERO, "hero", seed=98)


def shot4(k):              # Don leans over Sofia's notebook; Pam at the edge, 💗
    base(k, empty_chair=False)
    o = sofia_writing(k, look=(0, 0.6))
    pam_seated(k, "stand", "peer", look=(-1, -0.2))
    ms.chair_back(k, X["don"], seed=130)
    dm.don(k, X["don"] - 40, ms.FEET, 1.0, dm.POSE_LEAN, "wink", lean=-7, look=(-1, 0.5), seed=98)
    ms.table(k)
    sofia_props(k, o)
    pop(k, X["pam"] - 40, 420, 24)


def shot5(k):              # three-shot: Pam's finger, Don's sulk (eyes on Sofia), Sofia writes
    base(k, empty_chair=False)
    o = sofia_writing(k)
    pam_seated(k, pm.POSE_FINGER, "hopeful", finger=True, look=(-0.8, 0))
    dm.don(k, X["don"], ms.FEET, 1.0, dm.POSE_CROSS, "pout", look=(-1, 0), seed=98)
    ms.table(k)
    sofia_props(k, o)


def shot8(k):              # the robot holds Don's cuffs, freezes amber, turned to Pam beyond Don
    base(k, empty_chair=False)
    o = sofia_writing(k)
    pam_seated(k, "stand", "neutral", look=(-1, 0))
    dm.don(k, X["don"], ms.FEET, 1.0, dm.POSE_CLUTCH, "indignant", belt_cuffs_on=False, look=(-1, 0), seed=98)
    ms.table(k)
    sofia_props(k, o)
    rm.robot(k, X["robot"] + 90, ms.FEET + 30, 1.1, rm.POSE_TURN_CUFFS, "approval", cuffs=True, seed=97,
             **rm.TURN_HEAD)


def shot11(k):             # wide: Sofia out through the door, Don lunges after her, the chain to Pam yanks him
    base(k, door_open=0.6, empty_chair=False)
    sm.sofia(k, X["door"] + 120, ms.FEET, 1.0, "walk", "neutral", look=(-0.9, 0), step=0.25, carry=True, seed=99)
    pam_seated(k, PAM_ARM, "neutral", look=(-1, 0))
    rm.robot(k, X["robot"], ms.FEET_BACK, 1.0, "stand", "eager", seed=97)
    d = dm.don(k, X["don"] - 30, ms.FEET, 1.0, dm.POSE_LUNGE, "snap", lean=-20, look=(-1, 0), cuff="R",
               belt_cuffs_on=False, cap=(-6, -6, -18), seed=98)
    ms.table(k)
    chain_on_table(k, d["cuff"])


def shot12(k):             # the beam crosses Don, lands on Pam: FUN DETECTED
    base(k, empty_chair=False)
    ms.seated(k, lambda: dm.don(k, X["don"], SEAT - 20, 1.0, dm.POSE_STIFF, "panic", belt_cuffs_on=False, seed=98))
    p_ = pam_seated(k, PAM_ARM, "happy")
    o = rm.robot(k, X["robot"], ms.FEET_BACK, 1.0, "stand", "detected", seed=97)
    ms.table(k)
    chain_on_table(k, (X["don"] + 44, ms.TABLE_TOP - 6))
    kit.ellipse(k, X["don"] + 36, ms.TABLE_TOP - 2, 9, 9, dm.SKIN, 8, shadow=False, lw=2)
    pr.cuff(k, X["don"] + 46, ms.TABLE_TOP - 4, 1.0, math.pi / 2, loop_side=1)
    rm.scan_beam(k, o["screen"], p_["head"], 50, 0.6, col=rm.GREEN)


FRAMES = [("1 · frame 0: the slide", shot1, ms.CAMS["slide"]), ("3 · the door bangs", shot3, ms.CAMS["door"]),
          ("4 · leans in; Pam's heart", shot4, ms.CAMS["two"]), ("5 · sulk vs finger", shot5, (700, 520, 1.25)),
          ("8 · cuffs, turns to Pam", shot8, (610, 470, 1.15)), ("11 · exit and yank", shot11, ms.CAMS["exit"]),
          ("12 · FUN DETECTED", shot12, (640, 480, 1.1))]


def frame(c, k, x, y, sc, cam, draw):
    c.save(); c.rectangle(x, y, 540 * sc, 960 * sc); c.clip()
    c.translate(x, y); c.scale(sc, sc); ms.with_cam(c, cam); draw(k)
    c.restore()
    c.set_source_rgb(*INK); c.set_line_width(1.2); c.rectangle(x, y, 540 * sc, 960 * sc); c.stroke()


def main(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "THE TRAINING ROOM", 68, 44, 28, bold=True)
    corp(c, "\"Mandatory Fun\"  ·  door, slide, robot, table  ·  seats: Sofía, Don, Pam", 376, 44, 13, col=GREY)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    t = "UPTIMEZ INC. · SET SHEET · MANDATORY FUN v1"
    corp(c, t, W2 - 24 - c.text_extents(t).x_advance, 30, 10, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()

    # 1. world view
    corp(c, "THE SET (WORLD VIEW)  ·  shot 2 as staged", 24, 92, 10, bold=True)
    c.save(); c.rectangle(24, 98, 590, 330); c.clip()
    c.translate(24, 98); c.scale(0.6, 0.6); c.translate(-12, -170)
    wide(k)
    c.restore()
    c.set_source_rgb(*INK); c.set_line_width(1.2); c.rectangle(24, 98, 590, 330); c.stroke()
    corp(c, "Door far left · the screen and the robot · the table: Sofía, Don's empty chair, Pam.", 24, 444, 9, col=GREY)

    # 2. the slide, the door
    corp(c, "THE SLIDE  (frame 0 and the loop: the title card)", 24, 476, 10, bold=True)
    c.set_source_rgb(*kit.WALL); c.rectangle(24, 482, 380, 270); c.fill()
    ms.slide(k, 44, 500, 340, 230)
    corp(c, "THE DOOR  (shut / banged open)", 420, 476, 10, bold=True)
    for j, op in enumerate((0.0, 1.0)):
        x0 = 420 + j * 98
        c.save(); c.rectangle(x0, 482, 94, 270); c.clip()
        c.set_source_rgb(*kit.WALL); c.paint()
        c.translate(x0 + 47, 482); c.scale(0.5, 0.5); c.translate(-ms.POS["door"], ms.FLOOR_Y * -1 + 520)
        ms.wall(k); ms.door(k, op)
        c.restore()
        c.set_source_rgb(*INK); c.set_line_width(1.2); c.rectangle(x0, 482, 94, 270); c.stroke()

    # 3. 9:16 frames
    corp(c, "9:16 FRAMES FOR THE KEY SHOTS  (one seating throughout; does everyone fit; do the props read?)", 634, 92, 10,
         bold=True)
    sc = 0.24
    for i, (lab, fn, cam) in enumerate(FRAMES):
        if i < 4:
            x, y = 634 + i * 137, 98
        else:
            x, y = 634 + (i - 4) * 137, 362
        frame(c, k, x, y, sc, cam, fn)
        corp(c, lab, x, y + 960 * sc + 12, 9, col=GREY)

    # 4. notes
    corp(c, "NOTES", 1050, 362, 10, bold=True)
    notes = ["Bare room: Day One wall,", "UptimeZ sign, nothing else.", "", "Door far left: Don in (3),",
             "Sofía out (11).", "", "Slide = title card = loop.", "", "Seats fixed: Sofía, Don's", "empty chair, Pam.",
             "", "The robot stays left, so", "its beam crosses Don", "to reach Pam (12)."]
    for i, n in enumerate(notes):
        corp(c, n, 1050, 384 + i * 15, 10, col=INK)
    surf.write_to_png(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "mf_set_sheet_v1.png")
