"""The Double Agent (episode 15): the hand sheet (rules-hands §0.4: "the hand sheet is this film's jobs at one scale").
Every hand of the job list (the-double-agent-hand-jobs-v1.md, script v4), drawn with the hand library v4 (Tomas 27 Nov:
"Library v3 style" for every job; the canon gets it after 15) and the episode's props (da_props.py), left and right by
the canon's hands_lr. One tile per job: the shot, who, the job, the canon row; the hand at the cast's scale (male 17,
female 15) with what it holds, at the contact point the library names.

  python3 da_hand_sheet.py  -> ../the-double-agent/da_hand_sheet_v1.png (each job at 2x) and _feed.png (the same tiles
                               at the size a medium shot shows them, then at 270 px: the hand and its object must read)
The job -> library pose: quiet RELAXED, grab GRAB, clutch CLUTCH, pinch PINCH, palm PALM, fist FIST, the cup CUP_GRIP,
the saucer SAUCER_SUPPORT; board_two: two CLUTCH at the board's upper corners (the canon's row); the robot: the canon's
gripper and rest (da_hand_gate.robot_grip / robot_rest).
"""
import math
import os
import sys

import cairo
from PIL import Image

import kit
from kit import Ctx, INK
import hands_lr as lr
import hands_v4 as hv
import hand_lib_v4 as hl
import hand_lib_sheet_v3 as s3
import hand_lib_sheet_v4 as s4h
import da_props as pr
import da_set as ds
import da_sheets as dsh
import client_ob as cob
import acts_ob as ac
import sofia_da as sd
import mom_fs as mf
import don_ps as dp
import da_hands as dh

MALE, FEMALE = (0.96, 0.78, 0.66), (0.99, 0.86, 0.66)
OILY = (0.86, 0.70, 0.58)
TILE = 260
NAVY = (0.14, 0.20, 0.33)


def W(sex):
    return (17 if sex == "m" else 15) * 1.15 * 1.25           # the rig's hand at character scale 1


def at(pose, x, y, d, w, arm, name):
    ang = math.atan2(d[1], d[0])
    s_ = lr.side(arm, d) if pose != "SAUCER_SUPPORT" else arm
    return hl.to_screen(pose, x, y, 0 if pose == "SAUCER_SUPPORT" else ang, w, s_, hl.contact(pose, name))


def one(k, pose, x, y, d, w, skin, arm, obj=None, back=None):
    s3.forearm(k, x, y, math.atan2(d[1], d[0]) if pose != "SAUCER_SUPPORT" else (0.0 if arm > 0 else math.pi) - 0.45 * arm, w, skin=skin)
    hl.draw_lr(k, pose, x, y, d, w, skin, arm, obj=obj, back_obj=back, reach=arm)


# ---- each job: (shot, who, job, canon row, draw(k)) in a tile centred at (0, 0) ------------------------------------

def j_quiet(k, sex="m", skin=MALE):
    one(k, "RELAXED", 0, -40, (0, 1), 1.6 * W(sex), skin, 1)


def j_palm(k, d=(0.25, -1.0), sex="m", skin=MALE, arm=1, y=40):
    one(k, "PALM", 0, y, d, 1.6 * W(sex), skin, arm)


def j_fist(k, d=(0, 1), sex="m", skin=MALE):
    one(k, "FIST", 0, -40, d, 1.6 * W(sex), skin, 1)


def j_grab(k, draw_obj, d=(1.0, 0.0), sex="m", skin=MALE, arm=1, x=-40):
    w = 1.6 * W(sex)
    P = at("GRAB", x, 0, d, w, arm, "object")
    draw_obj(k, P, w)
    one(k, "GRAB", x, 0, d, w, skin, arm)


def j_pinch(k, draw_obj, d=(math.cos(-0.5), math.sin(-0.5)), sex="m", skin=MALE, arm=1, behind=False):
    """behind: the object is drawn first and the fingers over it (the knitting; the canon: "draw the object, then the
    fingers over it"); otherwise what hangs from the tip is drawn after (a tag on its string hangs in front)."""
    w = 1.6 * W(sex)
    x, y = -50, 30
    P = at("PINCH", x, y, d, w, arm, "tip")
    if behind:
        draw_obj(k, P, w)
    one(k, "PINCH", x, y, d, w, skin, arm)
    if not behind:
        draw_obj(k, P, w)


def j_clutch(k, draw_bar, d=(0.25, 1.0), sex="m", skin=MALE, arm=1):
    w = 1.6 * W(sex)
    x, y = 0, -50
    P = at("CLUTCH", x, y, d, w, arm, "edge")
    draw_bar(k, P, w)
    one(k, "CLUTCH", x, y, d, w, skin, arm)


def j_board_two(k, draw_board, bw, bh, sex="f", skin=FEMALE):
    """the canon's board_two: the board first, then a CLUTCH at each upper corner, the forearms coming down."""
    w = 1.3 * W(sex)
    draw_board(k)
    for arm in (-1, 1):
        cx, cy = arm * (bw / 2 - 0.30 * w), -bh / 2
        d = (-arm * 0.35, 1.0)
        n = math.hypot(*d); d = (d[0] / n, d[1] / n)
        ex = hl.contact("CLUTCH", "edge")[0] * w
        x, y = cx - d[0] * ex, cy - d[1] * ex                   # the wrist, so the knuckles land on the board's top edge
        one(k, "CLUTCH", x, y, d, w, skin, arm)


def j_cup(k, sex="m", skin=MALE):
    w = 1.6 * W(sex)
    d = (math.sin(0.35), -math.cos(0.35))
    x, y = 20, 60
    s_ = lr.side(1, d)
    ang = math.atan2(d[1], d[0])
    H = hl.to_screen("CUP_GRIP", x, y, ang, w, s_, hl.contact("CUP_GRIP", "handle"))
    Y1 = hl.to_screen("CUP_GRIP", x, y, ang, w, s_, (1.10, 1.06))
    one(k, "CUP_GRIP", x, y, d, w, skin, 1,
        back=lambda k_: s3.big_cup(k_, H[0], H[1], 1.1 * w / 26.0, 1 if Y1[0] < H[0] else -1, w))


def j_saucer(k, sex="m", skin=MALE, slop=False):
    w = 1.6 * W(sex)
    x, y = 40, 20
    Sp = hl.to_screen("SAUCER_SUPPORT", x, y, 0, w, -1, hl.contact("SAUCER_SUPPORT", "saucer"))
    def obj(k_):
        s3.saucer_at(k_, Sp[0], Sp[1], 0.95 * w / 30.0)
        if slop:
            kit.ellipse(k_, Sp[0] + 6, Sp[1] - 12, 8, 2.4, dh.COFFEE, 7401, shadow=False, lw=0.8)
    one(k, "SAUCER_SUPPORT", x, y, (-1, 0), w, skin, -1, obj=obj)


def bar(col, ln=2.6, th=0.5):
    def f(k, P, w):
        kit.cut(k, [(P[0] - ln * w / 2, P[1]), (P[0] + ln * w / 2, P[1]), (P[0] + ln * w / 2, P[1] + th * w),
                    (P[0] - ln * w / 2, P[1] + th * w)], col, shadow=False, lw=2)
    return f


def mug_body(col):
    def f(k, P, w):
        kit.cut(k, [(P[0] - 0.42 * w, P[1] - 0.6 * w), (P[0] + 0.42 * w, P[1] - 0.6 * w), (P[0] + 0.40 * w, P[1] + 0.7 * w),
                    (P[0] - 0.40 * w, P[1] + 0.7 * w)], col, shadow=False, lw=2)
        c = k.c; c.set_source_rgb(*INK); c.set_line_width(4); c.new_path()
        c.arc(P[0] + 0.62 * w, P[1], 0.26 * w, -1.5, 1.5); c.stroke()
    return f


def thermos(k, P, w):
    kit.cut(k, [(P[0] - 0.27 * w, P[1] - 1.0 * w), (P[0] + 0.27 * w, P[1] - 1.0 * w), (P[0] + 0.27 * w, P[1] + 0.9 * w),
                (P[0] - 0.27 * w, P[1] + 0.9 * w)], (0.55, 0.62, 0.66), shadow=False, lw=2)


def tape_roll_at(k, P, w):
    c = k.c
    for col, lw in ((INK, 0.62 * w), ((0.95, 0.78, 0.18), 0.50 * w)):
        c.set_source_rgb(*col); c.set_line_width(lw); c.new_path(); c.arc(P[0], P[1], 0.42 * w, 0, 2 * math.pi); c.stroke()


def rag(k, P, w):
    kit.cut(k, [(P[0] - 0.5 * w, P[1] - 0.4 * w), (P[0] + 0.3 * w, P[1] - 0.6 * w), (P[0] + 0.5 * w, P[1] + 0.5 * w),
                (P[0] - 0.4 * w, P[1] + 0.6 * w)], (0.80, 0.88, 0.95), shadow=False, lw=1.8)


def roll_blue(k, P, w):
    cob.blueprint_roll(k, P[0], P[1], 0.0, 3.2 * w, 0.30 * w)


def string_end(col, ln=1.2):
    def f(k, P, w):
        c = k.c; c.set_source_rgb(*col); c.set_line_width(0.14 * w); c.set_line_cap(1)
        c.move_to(*P); c.line_to(P[0] + 0.2 * w, P[1] + ln * w); c.stroke(); c.set_line_cap(0)
    return f


def mic_boom(k, P, w):
    c = k.c
    c.set_source_rgb(*INK); c.set_line_width(0.16 * w); c.set_line_cap(1)
    c.move_to(P[0] - 1.3 * w, P[1] - 0.8 * w); c.line_to(P[0] + 0.4 * w, P[1] + 0.2 * w); c.stroke(); c.set_line_cap(0)
    kit.ellipse(k, P[0] + 0.5 * w, P[1] + 0.26 * w, 0.18 * w, 0.18 * w, INK, 7402, shadow=False, lw=1.2)


def needle(k, P, w):
    c = k.c
    for col, lw in ((INK, 0.16 * w), ((0.75, 0.75, 0.80), 0.09 * w)):
        c.set_source_rgb(*col); c.set_line_width(lw); c.move_to(P[0] - 1.4 * w, P[1] + 0.6 * w); c.line_to(P[0] + 0.6 * w, P[1] - 0.3 * w); c.stroke()
    mf.knitting(k, P[0] - 1.7 * w, P[1] + 1.7 * w, 0.02 * w * 1.6)   # clear of the hand: DON whole (half hidden it reads ON)


JOBS = [
    ("1.1", "Don", "the armrest", "clutch", lambda k: j_clutch(k, bar((0.12, 0.10, 0.10), 3.0, 0.45))),
    ("1.1", "Don", "the free hand", "quiet", lambda k: j_quiet(k)),
    ("1.2", "Don", "flung open", "palm", lambda k: j_palm(k, (0.6, -0.8))),
    ("1.3", "Father", "hangs the tag", "pinch", lambda k: j_pinch(k, lambda k_, P, w: dsh._tag(k_, P[0], P[1], w / 34.0))),
    ("1.4", "Sofía", "folder + clip box", "board_two", lambda k: j_board_two(k, lambda k_: sd.clip_box(k_, 0, 30, 2.0), 110, 60)),
    ("1.5", "Don", "pulls the roll off", "grab", lambda k: j_grab(k, tape_roll_at)),
    ("2.2", "Father", "on the armrest", "quiet", lambda k: j_quiet(k)),
    ("2.3", "Don", "the vest's hem", "clutch", lambda k: j_clutch(k, bar(NAVY, 2.4, 0.6))),
    ("2.4", "Don", "presents the mug", "grab", lambda k: j_grab(k, mug_body(ds.MUG), (1.0, -0.2))),
    ("2.4", "Pam", "lets the blue mug go", "palm", lambda k: j_palm(k, (0.2, 1.0), "f", FEMALE, 1, -50)),
    ("3.1", "Don", "a hand up", "palm", lambda k: j_palm(k)),
    ("3.2", "Pam", "the thermos", "grab", lambda k: j_grab(k, thermos, (1.0, 0.0), "f", FEMALE)),
    ("3.3", "Pam", "her mug", "grab", lambda k: j_grab(k, mug_body(ds.MUG), (1.0, 0.0), "f", FEMALE)),
    ("3.3", "Client", "takes her mug", "grab", lambda k: j_grab(k, mug_body(ds.MUG), (-1.0, 0.1), "m", OILY, -1, 40)),
    ("3.4", "Mom", "knits", "pinch", lambda k: j_pinch(k, needle, sex="f", skin=FEMALE, behind=True)),
    ("3.5", "Pam", "wipes, the cloth", "grab", lambda k: j_grab(k, rag, (1.0, 0.0), "f", FEMALE)),
    ("4.2", "Pam", "her notepad", "clutch", lambda k: j_clutch(k, bar((0.98, 0.96, 0.82), 1.6, 1.4), sex="f", skin=FEMALE)),
    ("5.2", "Don", "sips, little finger out", "new: cup", lambda k: j_cup(k)),
    ("5.2", "Don", "the saucer, coffee in it", "new: saucer", lambda k: j_saucer(k, slop=True)),
    ("5.3", "Don", "windmilling", "palm", lambda k: j_palm(k, (0.9, -0.4))),
    ("5.4", "Mom", "hands on hips", "fist", lambda k: j_fist(k, (-0.5, 1.0))),
    ("6.1", "Pam", "the minutes, by the corner", "clutch", lambda k: j_clutch(k, lambda k_, P, w: pr.minutes(k_, P[0] + 1.45 * w, P[1] + 1.55 * w, w / 32.0), sex="f", skin=FEMALE)),
    ("6.6", "Client", "the rolled plan", "grab", lambda k: j_grab(k, roll_blue, (0.0, 1.0), "m", OILY, 1, 0)),
    ("6.8", "Don", "the headset's mic", "pinch", lambda k: j_pinch(k, mic_boom)),
    ("7.1", "Don", "peels the strip", "pinch", lambda k: j_pinch(k, string_end((0.95, 0.78, 0.18), 1.6))),
    ("7.3", "Client", "slides the plan", "palm", lambda k: j_palm(k, (0.0, 1.0), "m", OILY, 1, -60)),
    ("7.3", "Pam", "takes MY GARAGES", "board_two", lambda k: j_board_two(k, pr._plan, 124 * 1.4, 84 * 1.4)),
    ("7.4", "Don", "dives for the armrest", "clutch", lambda k: j_clutch(k, bar((0.12, 0.10, 0.10), 3.0, 0.45), (-0.3, 1.0))),
]


def tile(job, scale=2.0, size=TILE):
    shot, who, what, row, fn = job
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, int(size * scale), int(size * scale))
    c = cairo.Context(s); c.scale(scale, scale)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    lr.frame(cut=True)
    c.save(); c.translate(size / 2, size / 2 + 14); fn(k); c.restore()
    c.select_font_face("Inter", 0, 1); c.set_source_rgb(*INK)
    c.set_font_size(11); c.move_to(8, 16); c.show_text("%s  %s: %s" % (shot, who, what))
    c.select_font_face("Inter", 0, 0); c.set_font_size(10); c.set_source_rgb(0.35, 0.35, 0.35)
    c.move_to(8, 30); c.show_text("canon row: " + row)
    s.flush()
    return Image.frombuffer("RGB", (s.get_width(), s.get_height()), bytes(s.get_data()), "raw", "BGRX", 0, 1)


def main(out_dir="../the-double-agent"):
    lr.setup(); hv.enable(); lr.reset_log()
    ims = [tile(j) for j in JOBS]
    cols = 6
    rows = (len(ims) + cols - 1) // cols
    tw, th = ims[0].size
    sheet = Image.new("RGB", (cols * tw, rows * th), (255, 255, 255))
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % cols) * tw, (i // cols) * th))
    sheet.save(os.path.join(out_dir, "da_hand_sheet_v1.png"))
    # the feed: a medium shot shows a hand at about 0.6 of this sheet's size; the feed is half of that again
    fw, fh = int(tw * 0.6 / 2 / 2), int(th * 0.6 / 2 / 2)
    feed = Image.new("RGB", (cols * fw, rows * fh), (255, 255, 255))
    for i, im in enumerate(ims):
        feed.paste(im.resize((fw, fh), Image.LANCZOS), ((i % cols) * fw, (i // cols) * fh))
    feed.save(os.path.join(out_dir, "da_hand_sheet_v1_feed.png"))
    f = lr.check()
    print("wrote da_hand_sheet_v1.png (%d jobs), _feed.png; hands_lr: %s" % (len(JOBS), "clean" if not f else f))
    return not f


if __name__ == "__main__":
    sys.exit(0 if main(*sys.argv[1:]) else 1)
