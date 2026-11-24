"""Daddy's Home v8, scene 3 (The Green Star): the six key frames of shot list v2, for Tomas's look before any animation.
New file; v7 (dh_scenes, dh_film_v7) is not touched. Bubbles here are placed by hand to show the room the shot leaves
them; in the animation they come from dh_say as before.
  python3 dh_s3_v8.py  -> /tmp/out/dh_s3_v8/<frame>.png and the sheet dh_s3_v8_frames.png"""
import os
import sys
import math
import cairo
import kit
import hands_ps as hp
import fs_storyboard as sb
import dh_props as dp
import dh_poses as dq
import dh_layout as dl
import dh_scenes as ds
import dh_say as dsay
import dh_speech as SP
import dh_back as db
import pam_bc as pb
import sofia_cs as scs
from kit import Ctx, INK

F = sb.F
CH = dp.CHAIR
OUT = os.environ.get("DH8_OUT", "/tmp/out/dh_s3_v8")
FACES = {}                                                  # frame -> [(who, sx, sy, r)] measured from the rigs, in 540 units


def to_screen(cam, x, y, r=0.0):
    cx, cy, z = cam
    return (270 + (x - cx) * z, 480 + (y - cy) * z, r * z)


def bubble(c, text, box_xy, tip, maxw=300):
    """A bubble in the series style (dh_say._draw), box at box_xy (its top left), the tail to tip."""
    c.save(); c.select_font_face(kit.FONT); c.set_font_size(31)
    lines, bw, bh = SP._lines(c, text, maxw)
    bx, by = box_xy
    mx = max(bx + 28, min(bx + bw - 28, tip[0]))
    if tip[1] > by + bh:
        tail = [(mx - 12, by + bh - 3), tip, (mx + 12, by + bh - 3)]
    else:
        ex = bx + 3 if tip[0] > bx + bw else bx + bw - 3
        ty = max(by + 15, min(by + bh - 15, tip[1]))
        tail = [(ex, ty - 11), tip, (ex, ty + 11)]
    dsay._draw(c, lines, bx, by, bw, bh, tail, False)
    c.restore()
    return (bx, by, bw, bh)


def frame(name, cam, people, fg=None, bubbles=(), robot=False, hands=None):
    """people(k, o): the rigs, in set units; fg(k): the foreground, in 540 units, drawn after everyone."""
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1080, 1920); c = cairo.Context(surf); c.scale(2, 2)
    k = Ctx(c, 0)
    kit.HAND[0] = hp.hand
    sh = dl.shot(name, [], people, "", rb=robot, chair=False, cam=cam, ymin=0)
    cam_used = dl.draw(sh, k)
    if fg:
        c.save(); c.identity_matrix(); c.scale(2, 2); fg(k, cam_used); c.restore()
    c.save(); c.identity_matrix(); c.scale(2, 2)
    for text, xy, tip in bubbles:
        bubble(c, text, xy, tip(cam_used) if callable(tip) else tip)
    c.restore()
    kit.HAND[0] = None
    os.makedirs(OUT, exist_ok=True)
    surf.write_to_png(os.path.join(OUT, name + ".png"))
    return cam_used


# ---------------------------------------------------------------- 3A: over Don's shoulder, the robot and its screen
CAM_3A = (292, 640, 3.0)
CAM_3Az = (292, 640, 3.0)                 # no push: the robot's box is held still, so its antenna must be (24 Nov)                                  # the end of the small push (the screen stays whole)


SCREEN = [None]


def a_people(k, o):
    rx, ry = o["robot"]["screen"]
    SCREEN[0] = (rx + 60, ry - 92, 80)                    # v8: on the wall to the robot's right, so both speakers have
    dp.star_screen(k, *SCREEN[0], green=False)           # clear wall above them for their bubbles


def a_fg(point):
    def f(k, cam):
        if point:                                          # his left arm (screen left), straight up past the robot at the screen
            db.don_back(k, 492, 800, 1.0, arm=(352, 600, "point_s"), side=-1)
        else:
            db.don_back(k, 492, 800, 1.0, side=-1)
    return f



# ---------------------------------------------------------------- foreground pieces (540 units, near the lens)

def counter_near(k, cam, y=800):
    """the counter's top edge, near: a wood band across the bottom (cs_v19.counter, its y given here)."""
    c = k.c
    kit.rect(k, -20, y, 580, 980 - y, (0.62, 0.48, 0.34), 1903, shadow=False, lw=3)
    c.set_source_rgb(0.74, 0.60, 0.44); c.rectangle(-20, y + 4, 580, 18); c.fill()
    c.set_source_rgba(0, 0, 0, 0.18); c.rectangle(-20, y + 22, 580, 10); c.fill()


def shredder_near(k, cam):
    """the shredder's top corner at the bottom left, near: its slot and the sheet in it. No sign in frame."""
    c = k.c
    kit.cut(k, [(-30, 790), (150, 770), (170, 990), (-30, 990)], (0.30, 0.31, 0.34), shadow=False, lw=3)
    c.set_source_rgb(0.12, 0.12, 0.14); c.rectangle(-10, 800, 140, 12); c.fill()
    c.save(); c.translate(60, 790); c.rotate(-0.05)
    kit.rect(k, -46, -70, 92, 76, (0.99, 0.98, 0.95), 3611, shadow=False, lw=2.4)
    c.set_source_rgb(0.6, 0.6, 0.62); c.set_line_width(2)
    for yy in (-56, -44, -32):
        c.move_to(-34, yy); c.line_to(34, yy); c.stroke()
    c.restore()


ROBOT_NEAR = [(10, 560, 120)]


def robot_near(k, cam):
    """the robot's head and antenna, near, cut by the left edge: it is still beside him. Head only: no badge in frame."""
    c = k.c
    x, y, r = ROBOT_NEAR[0]
    c.set_source_rgb(*INK); c.set_line_width(5); c.move_to(x + 20, y - r); c.line_to(x + 26, y - r - 50); c.stroke()
    kit.ellipse(k, x + 26, y - r - 58, 14, 14, (0.98, 0.80, 0.20), 3621, shadow=False, lw=3)        # the antenna ball
    kit.ellipse(k, x, y, r, r * 0.92, (0.97, 0.96, 0.92), 3622, shadow=False, lw=4)                # the white rim
    kit.ellipse(k, x + 4, y + 2, r * 0.84, r * 0.76, (0.10, 0.15, 0.30), 3623, shadow=False, lw=3)  # the face screen
    for ex in (-10, 46):
        kit.ellipse(k, x + ex, y - 10, 15, 16, (0.62, 0.95, 1.0), 3624 + ex, shadow=False, lw=0.01)
    c.set_source_rgb(0.62, 0.95, 1.0); c.set_line_width(6); c.set_line_cap(1)
    c.new_path(); c.arc(x + 18, y + 18, 26, 0.5, 2.6); c.stroke(); c.set_line_cap(0)


def green_light(k, x, y, r, a=0.22):
    """the screen's green on whoever faces it: a soft wash, strongest at (x, y)."""
    c = k.c
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, 0.30, 0.95, 0.45, a); g.add_color_stop_rgba(1, 0.30, 0.95, 0.45, 0.0)
    c.set_source(g); c.paint()


# ---------------------------------------------------------------- 3C: Pam, MCU, behind the counter
PAM = (652, F + 6)
CAM_3C = (636, 708, 3.2)                  # round 3: v7's size (r 64): at 74 her bob blocks the tail


def c_people(k, o):
    hp.reset("quiet", "quiet")
    q = pb.pam(k, PAM[0], PAM[1], dl.PS, "stand", "neutral", look=(-1, -0.35), glasses="up")
    GL[0] = q
GL = [None]


def c_fg(k, cam):
    hx, hy, r = to_screen(cam, *dl.hp(PAM[0], PAM[1], dl.PS))
    c = k.c
    for sx_ in (-1, 1):                                    # the green star in her lenses
        c.save(); c.translate(hx + sx_ * 0.40 * r - 0.05 * r, hy + GLY[0] * r); c.scale(0.30 * r, 0.17 * r)
        c.new_path(); c.arc(0, 0, 1, 0, 6.2832); c.restore()
        c.set_source_rgba(0.25, 0.90, 0.40, 0.16); c.fill()                # review 24 Nov: half, the eyes stay readable
        x0 = hx + sx_ * 0.40 * r - 0.05 * r                 # round 3: the green star itself, small, in each lens
        sx0, sy0, rr = x0 + 0.08 * r, hy + GLY[0] * r - 0.05 * r, 0.075 * r
        c.new_path()
        for j in range(10):
            a_ = -math.pi / 2 + j * math.pi / 5
            q = rr if j % 2 == 0 else rr * 0.45
            (c.move_to if j == 0 else c.line_to)(sx0 + math.cos(a_) * q, sy0 + math.sin(a_) * q)
        c.close_path(); c.set_source_rgba(0.25, 0.85, 0.40, 0.95); c.fill()
    counter_near(k, cam, 818)                            # review 3 (24 Nov): at 690 it cut her at the shins, "no shoes"; below the soles (794)
GLY = [0.20]


# ---------------------------------------------------------------- 3D: Don, CU, low, fist up
DON3 = (330, F + 26)
CAM_3D = (325, 655, 4.0)


def d_people(k, o):
    hp.reset("relax", "fist")
    sb.don(k, DON3[0], DON3[1], 0.60, (-8, 0, 170, -30), "smug", look=(1, 0))


def d_fg(k, cam):
    hx, hy, r = to_screen(cam, *dl.hd(DON3[0], DON3[1], 0.60))
    green_light(k, hx - 40, hy - 20, 300, 0.14)
    robot_near(k, cam)


# ---------------------------------------------------------------- 3E (c): Sofía explodes out of the throne, Mom scrubs on
THR = 404
CAM_3E = (293, 650, 1.95)                 # round 2's staging, a step back; wall on Mom's left for her two boxes, the tag whole through the roll


def e_people(k, o):
    dp.ceo_chair(k, THR + 56, CH[1], CH[2])                 # review 24 Nov: on its casters, three short lines behind it only
    tx = THR + 56 - 78
    ds._lines(k, [(tx - 22, F - 120, tx - 2, F - 120), (tx - 30, F - 86, tx - 4, F - 86), (tx - 22, F - 52, tx - 2, F - 52)])
    hp.reset("palm", "palm")
    scs.sofia(k, 352, F - 58, dl.SS, "show", "caught", look=(0.4, -0.6), lean=-0.2, tablet_kind="none")
    ds._clip(k, 300, F - 272, -0.7)
    ds._lines(k, [(338, F - 30, 332, F - 18), (366, F - 30, 372, F - 18)])
    hp.reset("relax", "fist")
    sb.mfs.mom(k, 300, F + 8, dl.MS, "wipe", "sweet", look=(0.6, 0.8))


def e_fg(k, cam):
    shredder_near(k, cam)


# ---------------------------------------------------------------- 3F: "Different chair." Mom MCU, Sofía frozen behind
CAM_3F = (476, 690, 2.6)                  # a step back and right: Mom's box on her right (her mouth's side), out of the rail


def f_people(k, o):
    hp.reset("palm", "palm")
    scs.sofia(k, 388, F - 50, dl.SS, "show", "caught", look=(1, 0), lean=0.14, tablet_kind="none")
    dp.ceo_chair(k, 491, CH[1], CH[2])
    hp.reset("relax", "fist")
    sb.mfs.mom(k, 446, F + 8, dl.MS, "wipe", "sweet", look=(0.5, 0.9))


def main(only=None):
    todo = only or ["3A0", "3A1", "3B1", "3C", "3D", "3E", "3F"]
    ds.ARM_PHONE[0] = True
    if "3B1" in todo:
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1080, 1920); c = cairo.Context(surf); c.scale(2, 2)
        ds.s3_green(Ctx(c, 0), c); surf.write_to_png(os.path.join(OUT, "3B1.png"))
    if "3C" in todo:
        frame("3C", CAM_3C, c_people, c_fg, bubbles=[("It's still one.", (10, 334), (256, 368))])
    if "3D" in todo:
        frame("3D", CAM_3D, d_people, d_fg, bubbles=[("Green is all he sees.", (24, 112), (250, 318))])
    if "3E" in todo:
        frame("3E", CAM_3E, e_people, None)
    if "3F" in todo:
        frame("3F", CAM_3F, f_people, None, bubbles=[("Different chair.", (14, 530), (294, 566))])
    if "3A0" in todo:
        frame("3A0", CAM_3A, a_people, a_fg(True), robot=True, bubbles=[("Make it green.", (300, 112), (478, 733))])
    if "3A1" in todo:
        frame("3A1", CAM_3Az, a_people, a_fg(False), robot=True, bubbles=[("Human approval required.", (20, 112), (112, 576))])


if __name__ == "__main__":
    main(sys.argv[1:] or None)
