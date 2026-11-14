"""SILENT STORYBOARD v2 for "Happy Compliance" (xmas_sb.py = v1, kept), 28.9 s, 540x960.
v2 after review: the razor sits at Don's jaw so both eyes show; Don's eyes drop to the ornaments and we cut to
his point of view before the line; Sofía and Pam get their voices back ("Eww." together, Sofía's "Get him." at
the handoff, her sweet "Merry Christmas, Don." before the thud); the HR lettering fits its badge; every bubble
is sized from its text, pops in, and the shout shakes; THUD is a comic burst.

 1   0.0- 2.4  Don in the doorway, razor at the jaw: "Sorry. Getting ready for the ball."
 1b  2.4- 3.4  the wide
 2   3.4- 5.2  Sofía and Pam: "Eww."  (one box, two tails)
 4a  5.2- 5.9  Don: his eyes drop to Sofía's hands
 3   5.9- 6.7  his point of view: the two red ornaments
 4b  6.7- 9.5  Don: "Nice balls. I've got two for you."
 5   9.5-11.8  still beat 0.3 s, then horrified, then furious; Pam's fists
 6  11.8-13.4  the robot rolls in
 7  13.4-15.8  "INAPPROPRIATE BALLS DETECTED."
 8  15.8-19.8  the censoring (motion test A)
 9  19.8-21.5  "Violation resolved."  Don's thumbs-up
10  21.5-25.5  the handoff (Sofía: "Get him."), the mask, "Human in the loop." (motion test B v2)
10b 25.5-26.9  Don's smile drops; Sofía off-screen, sweetly: "Merry Christmas, Don."
11  26.9-28.9  "Happy compliance!"  THUD off-screen, the razor slides in; a bar falls; the alarm: loop"""
import math
import kit
from kit import clamp, ease, lerp, INK
import anim
import xmas_set as xs
import sofia_xmas as sx
import pam_xmas as px
import don_xmas as dx
import don_v4 as dv
import santa_robot as sr
import xmas_test_a as ta
import xmas_test_b as tb
import xmas_bubbles as xb

sr.HR_FIX = True
DURATION = 28.9
RAW_T = 0.0
DON_HY = -300 * kit.PEOPLE["DON"]["h"] + 78 - 44
PAM_HY = -300 * kit.PEOPLE["PAM"]["h"] + 78 - 44
SOF_HY = -300 * sx.H + 78 - 44
ROB_HY = -238


def u(t, t0, d):
    return clamp((t - t0) / d)


def world(k, cam, draw):
    c = k.c
    c.save(); xs.with_cam(c, cam); draw(); c.restore()


def top(cam, x, feet, hy, lift=62):
    return xs.to_screen(cam, x, feet + hy - lift)


def blink(t, times, d=0.15):
    return any(0 <= t - b < d for b in times)


# ------------------------------------------------------------------ 1  Don in the doorway
CAM1 = (700, 560, 1.7)


def s1(k, t, tl):
    def draw():
        xs.set_dressing(k, boil=int(t * 4)); xs.door(k, open_amt=1.0); xs.tree(k)
        x = lerp(726, 700, ease(u(t, 0, 0.35)))
        bob = -6 * math.sin(math.pi * u(t, 0, 0.35))
        dx.don(k, x, xs.FEET + bob, 1.0, dx.POSE_JAW, "smug" if not blink(t, (1.9,)) else "neutral", look=(-0.5, 0))
    world(k, CAM1, draw)
    if 0.1 <= t < 2.35:
        xb.speech(k, "Sorry. Getting ready\nfor the ball.", top(CAM1, 700, xs.FEET, DON_HY), t, 0.1)


# ------------------------------------------------------------------ 1b  the wide
CAM1B = (440, 470, 0.85)


def s1b(k, t, tl):
    def draw():
        xs.set_dressing(k, boil=int(t * 4)); xs.door(k, open_amt=1.0); xs.tree(k)
        px.pam(k, xs.POS["pam"], xs.FEET_BACK, 0.95, px.POSE_THERMOS, "neutral", look=(0.9, 0), thermos_in_hand=True)
        sx.sofia(k, xs.POS["sofia"], xs.FEET, 1.0, "hold2", "unimpressed", look=(0.9, 0))
        dx.don(k, xs.POS["don_door"], xs.FEET, 1.0, dx.POSE_JAW, "smug", look=(-0.6, 0))
    world(k, CAM1B, draw)


# ------------------------------------------------------------------ 2  "Eww."
CAM2 = (330, 570, 1.6)


def s2(k, t, tl):
    def draw():
        xs.set_dressing(k, boil=int(t * 4)); xs.tree(k)
        px.pam(k, 420, xs.FEET_BACK, 0.95, px.POSE_THERMOS, "neutral" if not blink(t, (4.75,)) else "squint",
               look=(0.9, 0), thermos_in_hand=True)
        sx.sofia(k, 235, xs.FEET, 1.0, "hold2", "unimpressed" if not blink(t, (4.9,)) else "closed", look=(0.9, 0))
    world(k, CAM2, draw)
    if 3.6 <= t < 4.75:
        xb.speech(k, "Eww.", [top(CAM2, 235, xs.FEET, SOF_HY, 70), top(CAM2, 420, xs.FEET_BACK, PAM_HY * 0.95, 60)],
                  t, 3.6, size=34)


# ------------------------------------------------------------------ 4a  Don's eyes drop
CAM4 = (600, 545, 1.9)


def s4a(k, t, tl):
    look = (-0.7, 0) if t < 5.4 else (-0.8, 0.9)

    def draw():
        xs.set_dressing(k, boil=int(t * 4)); xs.door(k, open_amt=1.0)
        dx.don(k, 600, xs.FEET, 1.0, dx.POSE_JAW, "neutral", look=look)       # open eyes: we see them drop
    world(k, CAM4, draw)


# ------------------------------------------------------------------ 3  his point of view
def s3(k, t, tl):
    z = lerp(2.3, 2.6, ease(u(t, 5.9, 0.8)))                 # a slow push in: he is staring
    cam = (196, 660, z)

    def draw():
        xs.set_dressing(k, boil=int(t * 4)); xs.tree(k)
        sx.sofia(k, 196, xs.FEET, 1.0, "hold2", "unimpressed", look=(0.9, 0))
    world(k, cam, draw)


# ------------------------------------------------------------------ 4b  the line
def s4b(k, t, tl):
    look = (-0.8, 0.9) if t < 8.2 else (-0.8, 0)              # down at the balls, then up to her on "two"

    def draw():
        xs.set_dressing(k, boil=int(t * 4)); xs.door(k, open_amt=1.0)
        pose = anim.tween(dx.POSE_JAW, dx.POSE_LINE, u(t, 6.8, 0.25), overshoot=True)
        dx.don(k, 600, xs.FEET, 1.0, kit.ARM_POSES[pose], "neutral" if t < 8.2 else "smug", look=look,
               chin=0.6 if t >= 8.2 else 0.0)                               # eyes on the balls, smug on "two"
    world(k, CAM4, draw)
    if 6.85 <= t < 9.45:
        xb.speech(k, "Nice balls.\nI've got two for you.", top(CAM4, 600, xs.FEET, DON_HY), t, 6.85)


# ------------------------------------------------------------------ 5  the reaction
def s5(k, t, tl):
    sface = "unimpressed" if t < 9.8 else ("horrified" if t < 10.7 else "furious")

    def draw():
        xs.set_dressing(k, boil=int(t * 4)); xs.tree(k)
        ppose = px.POSE_THERMOS if t < 10.3 else px.POSE_FISTS
        px.pam(k, 420, xs.FEET_BACK, 0.95, ppose, "neutral" if t < 10.3 else "squint", look=(0.9, 0),
               thermos_in_hand=t < 10.3)
        lag = (-6 * math.sin(math.pi * u(t, 9.8, 0.3)), 0)
        sx.sofia(k, 235, xs.FEET, 1.0, "hold2", sface, look=(0.9, 0), lag=lag)
    world(k, CAM2, draw)


# ------------------------------------------------------------------ 6  the robot comes in
CAM6 = (650, 560, 1.4)


def s6(k, t, tl):
    def draw():
        xs.set_dressing(k, boil=int(t * 4)); xs.door(k, open_amt=1.0)
        v = ease(u(t, 11.8, 0.9))
        sr.robot(k, lerp(800, 640, v), xs.FEET, 1.0, "travel", "eager" if t < 12.7 else "stern", side=-1,
                 wobble=0.08 * math.sin(t * 22) * (1 - v), alarm=int(t * 6) % 2 == 0)
    world(k, CAM6, draw)


# ------------------------------------------------------------------ 7  the point
CAM7 = (575, 570, 1.6)


def s7(k, t, tl):
    snap = u(t, 13.55, 0.15)

    def draw():
        xs.set_dressing(k, boil=int(t * 4)); xs.door(k, open_amt=1.0)
        early = t < 13.8
        dx.don(k, 650, xs.FEET, 1.0, dx.POSE_JAW if early else dx.POSE_CLUTCH, "smug" if early else "shock",
               look=(-0.8, 0), razor_in_hand=early)
        pose = sr.w.blend("stand", "detect", min(1.0, anim.back_out(snap, 1.6))) if snap < 1 else "detect"
        sr.robot(k, 500, xs.FEET, 1.0, pose, "stern", side=-1, alarm=True, locked=snap >= 0.6)
    world(k, CAM7, draw)
    if 13.75 <= t < 15.75:
        xb.shout(k, "INAPPROPRIATE\nBALLS DETECTED.", top(CAM7, 470, xs.FEET, ROB_HY, 108), t, 13.75, cx=250, cy=200)


# ------------------------------------------------------------------ 8  the censoring = motion test A
def s8(k, t, tl):
    ta.RAW_T = tl
    k.c.save(); ta.frame(k, tl, tl); k.c.restore()


# ------------------------------------------------------------------ 9  resolved
def s9(k, t, tl):
    def draw():
        xs.set_dressing(k, boil=int(t * 4)); xs.door(k, open_amt=1.0)
        thumb = t >= 20.4
        o = dx.don(k, 650, xs.FEET, 1.0, dx.POSE_THUMB if thumb else dx.POSE_CLUTCH, "grin" if thumb else "neutral",
                   look=(-0.8, 0), razor_in_hand=False)
        if thumb:
            dv.thumbs_up(k, o["hands"][1], max(0.02, min(1.0, anim.back_out(u(t, 20.4, 0.2), 1.8))))
        sr.robot(k, 500, xs.FEET, 1.0, "stand", "smug", side=-1,
                 talk=0.5 if 19.95 <= t < 21.0 and int(t * 8) % 2 else 0)
    world(k, CAM7, draw)
    if 19.95 <= t < 21.45:
        xb.speech(k, "Violation resolved.", top(CAM7, 500, xs.FEET, ROB_HY, 112), t, 19.95)


# ------------------------------------------------------------------ 10  Pam = motion test B v2 (from 0.5 s in)
def s10(k, t, tl):
    tt = 0.5 + tl
    tb.RAW_T = tt
    k.c.save(); tb.frame(k, tt, tl); k.c.restore()
    cam = tb.cam(tt)
    if 0.95 <= tt < 1.55:
        xb.speech(k, "Get him.", top(cam, tb.SOF_X, xs.FEET + 6, SOF_HY, 70), tt, 0.95)
    if tt >= 2.05:
        xb.speech(k, "Human in the loop.", top(cam, tb.PAM_X + 10, xs.FEET, PAM_HY, 58), tt, 2.05)


# ------------------------------------------------------------------ 10b  the smile drops; Merry Christmas, Don
CAM10B = (650, 545, 1.9)


def s10b(k, t, tl):
    def draw():
        xs.set_dressing(k, boil=int(t * 4)); xs.door(k, open_amt=1.0)
        early = t < 25.75
        dx.don(k, 650, xs.FEET, 1.0, dx.POSE_THUMB if early else dx.POSE_LIMP, "grin" if early else "neutral",
               look=(-0.8, 0) if early else (-1.0, 0.1), razor_in_hand=False, sweat=t >= 26.1)
    world(k, CAM10B, draw)
    if 25.6 <= t < 26.85:                                       # Sofía, off-screen left, sweetly
        xb.speech(k, "Merry Christmas, Don.", [(-40, 330)], t, 25.6, at=(250, 170), italic_sweet=True)


# ------------------------------------------------------------------ 11  happy compliance, and the loop
CAM11 = (400, 565, 1.9)


def s11(k, t, tl):
    peel = u(t, 28.1, 0.4)

    def draw():
        xs.set_dressing(k, boil=int(t * 4))
        cen = tuple(i for i in range(8) if not (i == 2 and t >= 28.1))
        xs.tree(k, censored=cen)
        if t >= 28.1:
            ox, oy = ta.ORN[2]
            sr.censor_bar(k, ox - 6 * peel, oy + 120 * peel ** 2, 14 * 3.0 * xs.BAR_SCALE, 14 * 0.95 * xs.BAR_SCALE,
                          rot=0.08 + 2.2 * peel, seed=1200)
        talk = 0.6 if 27.0 <= t < 27.9 and int(t * 8) % 2 else 0.0
        sr.robot(k, 420, xs.FEET, 1.0, "present", "proud" if t < 28.35 else "stern", side=-1, talk=talk,
                 alarm=t >= 28.35)
        if t >= 27.3:                                           # the razor slides in along the floor, alone
            v = ease(u(t, 27.3, 0.55))
            dx.razor(k, (lerp(250, 335, v), xs.FEET - 4), 1.0, ang=1.57 + 0.5 * v + 6.0 * (1 - v), seed=1210)
    world(k, CAM11, draw)
    if 26.95 <= t < 28.1:
        xb.speech(k, "Happy compliance!", top(CAM11, 420, xs.FEET, ROB_HY, 115), t, 26.95, size=30)
    if 27.2 <= t < 27.6:
        xb.burst(k, "THUD", 105, 470, t, 27.2)


PANELS = [(0.0, 2.4, s1), (2.4, 3.4, s1b), (3.4, 5.2, s2), (5.2, 5.9, s4a), (5.9, 6.7, s3), (6.7, 9.5, s4b),
          (9.5, 11.8, s5), (11.8, 13.4, s6), (13.4, 15.8, s7), (15.8, 19.8, s8), (19.8, 21.5, s9),
          (21.5, 25.5, s10), (25.5, 26.9, s10b), (26.9, 28.9, s11)]
