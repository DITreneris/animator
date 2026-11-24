"""Daddy's Home v8, scene 4 (The Wrong Man): the key frames of shot list v2 (daddys-home-s4-shot-list-v2.md), for
Tomas's look before any animation. New file; v7 is not touched. Bubbles placed by hand to show the room; in the
animation dh_speech places them.
  python3 dh_s4_v8.py [frames]  ->  /tmp/out/dh_s4_v8/<frame>.png"""
import os
import sys
import math
import cairo
import kit
import hands_ps as hp
import fs_storyboard as sb
import dh_props as dp
import dh_cast as dc
import dh_layout as dl
import dh_scenes as ds
import dh_back as db
import dh_s3_v8 as S3
from kit import Ctx, INK

F, CH = sb.F, dp.CHAIR
S3.OUT = os.environ.get("DH8_OUT", "/tmp/out/dh_s4_v8")
to_screen, frame = S3.to_screen, S3.frame
GS = dl.GS
VX, VF = 364, F + 8                                         # the visitor where v7 has him (TOUR[1] - 14)
THR4 = ds.THR4
LINE = ds.LINE


# ---------------------------------------------------------------- 4A: the visitor in, over the robot's head
CAM_4A = (147, 669, 2.6)


def a_people(k, o):
    hp.reset("relax", "grab")
    dc.repairman(k, 128, F + 8, GS, case=True, look=(0.6, 0))


def a_fg(k, cam):
    import fs_film18 as f18
    f18.robot_back(k, 470, 1260, 2.3)                       # its head and antenna at the right edge, near


# ---------------------------------------------------------------- 4B: the line
CAM_4B = (471, 712, 2.45)


def b_people(k, o):
    dp.ceo_chair(k, THR4, CH[1], CH[2])
    hp.reset("quiet", "quiet")
    sb.mfs.mom(k, LINE[0][0], LINE[0][1], dl.MS, "stand", "sweet", look=(-1, 0))
    hp.reset("palm", "palm")
    ds.scs.sofia(k, LINE[2][0], LINE[2][1], dl.SS, "hold", "recover", look=(-1, 0))
    hp.reset("fist", "fist")
    sb.don(k, LINE[1][0], LINE[1][1], 0.60, "vest", "happy", look=(-1, 0))


# ---------------------------------------------------------------- 4C: "We've been expecting you."
CAM_4C = (451, 682, 3.2)


def c_people(k, o):
    dp.ceo_chair(k, THR4, CH[1], CH[2])
    hp.reset("palm", "relax")
    sb.don(k, LINE[1][0], LINE[1][1], 0.60, (-104, -24, 30, 10), "happy", look=(-1, 0))


# ---------------------------------------------------------------- 4D: Pam, the machine beside her
PAM = ds.PAM
CAM_4D = (699, 700, 2.35)
CAM_4D2 = (668, 690, 3.6)                                 # the mug beat closer, as v7 (MCU)


def d_people(k, o):
    hp.reset("quiet", "quiet")
    ds.pb.pam(k, PAM[0], PAM[1], dl.PS, "stand", "neutral", look=(-0.7, 0.8), glasses="up")


def d_fg(k, cam):
    S3.counter_near(k, cam, COUNTER[0])
COUNTER = [600]


# ---------------------------------------------------------------- 4D'': the mug, smaller, held by its handle
def d2_people(k, o):
    """Rules page: one hand per wrist; the object, then the fingers over it. The rig draws her hand (logged), the mug is
    drawn at that hand, and the SAME hand call is made again on top (the grip's second pass, as cs_scene1.grip_rect)."""
    hp.reset("quiet", "grab")
    calls = []
    real = kit.HAND[0]

    def rec(*a):
        calls.append((hp._N[0], a, a[0].c.get_matrix()))     # the hand's own coordinates: the rig's matrix at the call
        return real(*a)
    kit.HAND[0] = rec
    try:
        q = ds.pb.pam(k, PAM[0], PAM[1], dl.PS, (-8, 0, 60, 110), "neutral", look=(0.2, 0.9), glasses="up")
    finally:
        kit.HAND[0] = real
    c = k.c
    n0, a, m = calls[-1]                                     # her right hand (screen right, drawn second)
    hx, hy = a[1], a[2]
    c.save(); c.set_matrix(m)
    s = 1.1                                                  # in her hand's units (PS 0.54): about 60 % of v7's mug
    c.save(); c.translate(hx, hy); c.rotate(2.75); c.scale(s, s); c.translate(-26, 0)   # held by its handle: the body clear of her fist
    c.set_source_rgb(*INK); c.set_line_width(4); c.new_path(); c.arc(13, 0, 9, -1.4, 1.4); c.stroke()   # the handle, showing
    c.set_source_rgb(0.98, 0.98, 0.96); c.set_line_width(2); c.new_path(); c.arc(13, 0, 9, -1.4, 1.4); c.stroke()
    kit.cut(k, [(-10, -12), (10, -12), (9, 12), (-9, 12)], (0.36, 0.62, 0.80), shadow=False, lw=2)
    kit.ellipse(k, 0, -12, 10, 3.2, (0.15, 0.12, 0.10), 3551, shadow=False, lw=1.6)
    c.restore()
    hp._N[0] = n0; hp.hand(*a)                               # the same hand, again, over the mug
    c.restore()


# ---------------------------------------------------------------- 4D': the pass, bigger, the case at the edge
def d1_insert(k, c):
    c.set_source_rgb(0.08, 0.08, 0.10); c.paint()
    c.save(); c.translate(270, 430); c.rotate(-0.04); c.scale(1.25, 1.25)
    kit.rect(k, -110, -130, 220, 250, (0.99, 0.98, 0.95), 3570, lw=4)                   # the pass
    kit.ellipse(k, 0, -50, 46, 46, (0.12, 0.12, 0.14), 3571, shadow=False, lw=2)
    c.set_source_rgb(0.99, 0.98, 0.95); c.set_line_width(5)
    c.rectangle(-18, -62, 30, 26); c.stroke(); c.new_path(); c.arc(18, -50, 8, -1.4, 1.4); c.stroke()
    dp._T(c, "COFFEE", 0, 40, 36)
    dp._T(c, "SERVICE", 0, 82, 36)
    c.restore()
    c.set_source_rgb(0.25, 0.45, 0.85); c.set_line_width(10); c.move_to(250, 120); c.line_to(270, 260); c.line_to(290, 120); c.stroke()  # the lanyard
    kit.rect(k, 330, 760, 260, 170, (0.78, 0.80, 0.84), 3572, lw=3)                     # the case, at the edge
    kit.ellipse(k, 440, 790, 22, 10, (0.97, 0.97, 0.95), 3573, shadow=False, lw=2)      # the cup on it


# ---------------------------------------------------------------- 4E (c): the sticker
CAM_4E = (438, 682, 2.35)


def e_people(k, o):
    dp.ceo_chair(k, THR4 + 15, CH[1], CH[2])               # 15 right of 4B/4C: its tag clear of his head (v7: 30 left, covered)
    hp.reset("relax", "grab")
    dc.repairman(k, VX, VF, GS, case=True, look=(0.2, 1))
    ds._sticker(k, VX, VF)
    hp.reset("palm", "relax")
    sb.don(k, 480, F + 26, 0.60, (-92, -6, 8, 0), "happy", look=(-1, 0))   # his palm on the sticker
    ds._lines(k, [(VX + 14, F - 150, VX + 26, F - 160), (VX + 18, F - 128, VX + 32, F - 128)])


# ---------------------------------------------------------------- 4F: the robot, MCU, over the visitor's shoulder
CAM_4F = (250, 662, 4.75)


def f_fg(k, cam):
    db.visitor_back(k, 520, 760, 1.25)


# ---------------------------------------------------------------- 4H: the visitor, MCU, over Don's shoulder
CAM_4H = (348, 648, 3.1)


def h_people(k, o):
    hp.reset("relax", "grab")
    dc.repairman(k, VX, VF, GS, case=True, look=(-0.3, 0.2))
    ds._sticker(k, VX, VF)


def h_fg(k, cam):
    db.don_back(k, 60, 840, 1.0, side=1)


def main(only=None):
    todo = only or ["4A", "4B", "4C", "4D", "4D1", "4D2", "4E", "4F", "4H"]
    ds.ARM_PHONE[0] = True
    if "4A" in todo:
        frame("4A", CAM_4A, a_people, a_fg)
    if "4B" in todo:
        frame("4B", CAM_4B, b_people, None)
    if "4C" in todo:
        frame("4C", CAM_4C, c_people, None)
    if "4D" in todo:
        frame("4D", CAM_4D, d_people, d_fg)
    if "4D1" in todo:
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1080, 1920); c = cairo.Context(surf); c.scale(2, 2)
        d1_insert(Ctx(c, 0), c); os.makedirs(S3.OUT, exist_ok=True); surf.write_to_png(os.path.join(S3.OUT, "4D1.png"))
    if "4D2" in todo:
        COUNTER[0] = 880; frame("4D2", CAM_4D2, d2_people, d_fg); COUNTER[0] = 600
    if "4E" in todo:
        frame("4E", CAM_4E, e_people, None)
    if "4F" in todo:
        frame("4F", CAM_4F, lambda k, o: None, f_fg, robot=True)
    if "4H" in todo:
        frame("4H", CAM_4H, h_people, h_fg)


if __name__ == "__main__":
    main(sys.argv[1:] or None)
