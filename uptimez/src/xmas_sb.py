"""SILENT STORYBOARD v1 for the Christmas special "Happy Compliance" (UptimeZ Inc.), 27.5 s, 540x960.
Built on the set (xmas_set.py), the four costume modules and the two approved motion tests (shot 8 = test A,
shot 10 = test B v2, reused frame for frame). Speech bubbles carry every line for sound-off viewers.

 1   0.0- 2.4  Don alone in the doorway, mid-shave (frame 0 reads on a phone): "Sorry. Getting ready for the ball."
 1b  2.4- 3.4  the wide: the party stares
 2   3.4- 5.0  Sofía and Pam: unimpressed, deadpan
 3   5.0- 6.2  close-up: the two red ornaments in Sofía's hands
 4   6.2- 9.2  Don: eyes drop to the ornaments, smirk: "Nice balls. I've got two for you."
 5   9.2-11.5  Sofía and Pam: a 0.3 s still beat, then horrified, then furious; Pam's fists clench
 6  11.5-13.1  the door: the Santa robot rolls in, pompom alarm
 7  13.1-15.5  robot and Don: the rigid point: "Inappropriate balls detected."  Don clutches his robe
 8  15.5-19.5  the censoring (motion test A): three slaps, the cascade, Sofía's two, smug
 9  19.5-21.2  robot and Don: "Violation resolved."  Don's relieved thumbs-up
10  21.2-25.0  Pam (motion test B v2): the handoff, the mask, the hero: "Human in the loop."
10b 25.0-25.7  Don: the smile drops (sweat drop)
11  25.7-27.5  robot to camera: "Happy compliance!"  off-screen thud, the razor slides in; one bar peels off,
               the pompom flashes red: it starts again (loop)"""
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
import cafe_kit as ck
import day1_sb_v3 as sb
import xmas_test_a as ta
import xmas_test_b as tb

DURATION = 27.5
RAW_T = 0.0
DON_HY = -300 * kit.PEOPLE["DON"]["h"] + 78 - 44        # head centre above the feet
PAM_HY = -300 * kit.PEOPLE["PAM"]["h"] + 78 - 44
SOF_HY = -300 * sx.H + 78 - 44


def u(t, t0, d):
    return clamp((t - t0) / d)


def world(k, cam, draw):
    c = k.c
    c.save(); xs.with_cam(c, cam); draw(); c.restore()


def top(cam, x, feet, hy, s=1.0, lift=62):
    return xs.to_screen(cam, x, feet + hy * s - lift)


# ------------------------------------------------------------------ 1  Don in the doorway
CAM1 = (700, 560, 1.7)


def s1(k, t, tl):
    def draw():
        xs.set_dressing(k, boil=int(t * 4)); xs.door(k, open_amt=1.0); xs.tree(k)
        x = lerp(726, 700, ease(u(t, 0, 0.35)))
        bob = -6 * math.sin(math.pi * u(t, 0, 0.35))
        dx.don(k, x, xs.FEET + bob, 1.0, dx.POSE_RAZOR, "smug", look=(-0.5, 0))
    world(k, CAM1, draw)
    if 0.1 <= t < 2.35:
        sb.bubble(k, "Sorry. Getting ready\nfor the ball.", top(CAM1, 700, xs.FEET, DON_HY), "up", size=28, t=t, t0=0.1)


# ------------------------------------------------------------------ 1b  the wide
CAM1B = (440, 470, 0.85)


def s1b(k, t, tl):
    def draw():
        xs.set_dressing(k, boil=int(t * 4)); xs.door(k, open_amt=1.0); xs.tree(k)
        px.pam(k, xs.POS["pam"], xs.FEET_BACK, 0.95, px.POSE_THERMOS, "neutral", look=(0.9, 0), thermos_in_hand=True)
        sx.sofia(k, xs.POS["sofia"], xs.FEET, 1.0, "hold2", "unimpressed", look=(0.9, 0))
        dx.don(k, xs.POS["don_door"], xs.FEET, 1.0, dx.POSE_RAZOR, "smug", look=(-0.6, 0))
    world(k, CAM1B, draw)


# ------------------------------------------------------------------ 2  Sofía and Pam stare
CAM2 = (330, 570, 1.6)


def s2(k, t, tl):
    def draw():
        xs.set_dressing(k, boil=int(t * 4)); xs.tree(k)
        px.pam(k, 420, xs.FEET_BACK, 0.95, px.POSE_THERMOS, "neutral" if not 4.4 <= t < 4.55 else "squint",
               look=(0.9, 0), thermos_in_hand=True)
        sx.sofia(k, 235, xs.FEET, 1.0, "hold2", "unimpressed" if not 3.9 <= t < 4.05 else "closed", look=(0.9, 0))
    world(k, CAM2, draw)


# ------------------------------------------------------------------ 3  the ornaments
CAM3 = (196, 655, 2.4)


def s3(k, t, tl):
    def draw():
        xs.set_dressing(k, boil=int(t * 4)); xs.tree(k)
        sx.sofia(k, 196, xs.FEET, 1.0, "hold2", "unimpressed", look=(0.9, 0))
    world(k, CAM3, draw)


# ------------------------------------------------------------------ 4  Don: the line
CAM4 = (600, 545, 1.9)


def s4(k, t, tl):
    look = (-0.8, 0) if t < 6.6 else (-0.7, 0.6)          # eyes drop to the ornaments
    face = "smug"

    def draw():
        xs.set_dressing(k, boil=int(t * 4)); xs.door(k, open_amt=1.0)
        pose = anim.tween(dx.POSE_RAZOR, dx.POSE_LINE, u(t, 6.4, 0.25), overshoot=True)
        dx.don(k, 600, xs.FEET, 1.0, kit.ARM_POSES[pose], face, look=look,
               chin=0.6 if t >= 8.0 else 0.0)             # chin up on "two"
    world(k, CAM4, draw)
    if 6.7 <= t < 9.15:
        sb.bubble(k, "Nice balls.\nI've got two for you.", top(CAM4, 600, xs.FEET, DON_HY), "up", size=28, t=t, t0=6.7)


# ------------------------------------------------------------------ 5  the reaction
def s5(k, t, tl):
    if t < 9.5:
        sface = "unimpressed"                               # the still beat
    elif t < 10.4:
        sface = "horrified"
    else:
        sface = "furious"

    def draw():
        xs.set_dressing(k, boil=int(t * 4)); xs.tree(k)
        ppose = px.POSE_THERMOS if t < 10.0 else px.POSE_FISTS
        px.pam(k, 420, xs.FEET_BACK, 0.95, ppose, "neutral" if t < 10.0 else "squint", look=(0.9, 0),
               thermos_in_hand=t < 10.0)
        lag = (-6 * math.sin(math.pi * u(t, 9.5, 0.3)), 0)  # the head snap shakes her hair and earrings
        sx.sofia(k, 235, xs.FEET, 1.0, "hold2", sface, look=(0.9, 0), lag=lag)
    world(k, CAM2, draw)


# ------------------------------------------------------------------ 6  the robot comes in
CAM6 = (650, 560, 1.4)


def s6(k, t, tl):
    def draw():
        xs.set_dressing(k, boil=int(t * 4)); xs.door(k, open_amt=1.0)
        v = ease(u(t, 11.5, 0.9))
        x = lerp(800, 640, v)
        wob = 0.08 * math.sin(t * 22) * (1 - v)
        sr.robot(k, x, xs.FEET, 1.0, "travel", "eager" if t < 12.4 else "stern", side=-1, wobble=wob,
                 alarm=int(t * 6) % 2 == 0)
    world(k, CAM6, draw)


# ------------------------------------------------------------------ 7  the point
CAM7 = (575, 570, 1.6)


def s7(k, t, tl):
    snap = u(t, 13.25, 0.15)

    def draw():
        xs.set_dressing(k, boil=int(t * 4)); xs.door(k, open_amt=1.0)
        dpose = dx.POSE_RAZOR if t < 13.5 else dx.POSE_CLUTCH
        dx.don(k, 650, xs.FEET, 1.0, dpose, "smug" if t < 13.5 else "shock", look=(-0.8, 0), razor_in_hand=t < 13.5)
        pose = sr.w.blend("stand", "detect", min(1.0, anim.back_out(snap, 1.6))) if snap < 1 else "detect"
        sr.robot(k, 500, xs.FEET, 1.0, pose, "stern", side=-1, alarm=True, locked=snap >= 0.6)
    world(k, CAM7, draw)
    if 13.45 <= t < 15.45:
        ax, ay = top(CAM7, 500, xs.FEET, -238, lift=110)
        ck.shout(k, "INAPPROPRIATE\nBALLS DETECTED.", (ax, ay), 280, 170, size=36)


# ------------------------------------------------------------------ 8  the censoring = motion test A
def s8(k, t, tl):
    ta.RAW_T = tl
    k.c.save(); ta.frame(k, tl, tl); k.c.restore()


# ------------------------------------------------------------------ 9  resolved
def s9(k, t, tl):
    def draw():
        xs.set_dressing(k, boil=int(t * 4)); xs.door(k, open_amt=1.0)
        thumb = t >= 20.1
        o = dx.don(k, 650, xs.FEET, 1.0, dx.POSE_THUMB if thumb else dx.POSE_CLUTCH,
                   "grin" if thumb else "neutral", look=(-0.8, 0), razor_in_hand=False)
        if thumb:
            dv.thumbs_up(k, o["hands"][1], max(0.02, min(1.0, anim.back_out(u(t, 20.1, 0.2), 1.8))))
        sr.robot(k, 500, xs.FEET, 1.0, "stand", "smug", side=-1, talk=0.5 if 19.7 <= t < 20.8 and int(t * 8) % 2 else 0)
    world(k, CAM7, draw)
    if 19.65 <= t < 21.15:
        sb.bubble(k, "Violation resolved.", top(CAM7, 500, xs.FEET, -238, lift=112), "up", size=28, t=t, t0=19.65)


# ------------------------------------------------------------------ 10  Pam = motion test B v2 (from 0.5 s in)
def s10(k, t, tl):
    tt = 0.5 + tl
    tb.RAW_T = tt
    k.c.save(); tb.frame(k, tt, tl); k.c.restore()
    if tt >= 2.05:
        cam = tb.cam(tt)
        sb.bubble(k, "Human in the loop.", top(cam, tb.PAM_X + 10, xs.FEET, PAM_HY, lift=58), "up", size=28,
                  t=tt, t0=2.05)


# ------------------------------------------------------------------ 10b  Don's smile drops
CAM10B = (650, 545, 1.9)


def s10b(k, t, tl):
    def draw():
        xs.set_dressing(k, boil=int(t * 4)); xs.door(k, open_amt=1.0)
        dx.don(k, 650, xs.FEET, 1.0, dx.POSE_THUMB if t < 25.2 else dx.POSE_LIMP, "grin" if t < 25.2 else "neutral",
               look=(-0.8, 0), razor_in_hand=False, sweat=t >= 25.3)
    world(k, CAM10B, draw)


# ------------------------------------------------------------------ 11  happy compliance, and the loop
CAM11 = (400, 565, 1.9)


def s11(k, t, tl):
    peel = u(t, 26.9, 0.4)

    def draw():
        xs.set_dressing(k, boil=int(t * 4))
        cen = tuple(i for i in range(8) if not (i == 2 and t >= 26.9))
        xs.tree(k, censored=cen)
        if t >= 26.9:                                     # the bar from ornament 2 falls off
            ox, oy = ta.ORN[2]
            sr.censor_bar(k, ox - 6 * peel, oy + 120 * peel ** 2, 14 * 3.0 * xs.BAR_SCALE, 14 * 0.95 * xs.BAR_SCALE,
                          rot=0.08 + 2.2 * peel, seed=1200)
        talk = 0.6 if 25.85 <= t < 26.7 and int(t * 8) % 2 else 0.0
        sr.robot(k, 420, xs.FEET, 1.0, "present", "proud" if t < 27.15 else "stern", side=-1, talk=talk,
                 alarm=t >= 27.15)
        if t >= 26.05:                                    # the razor slides in along the floor, alone
            v = ease(u(t, 26.05, 0.55))
            dx.razor(k, (lerp(250, 335, v), xs.FEET - 4), 1.0, ang=1.57 + 0.5 * v + 6.0 * (1 - v), seed=1210)
    world(k, CAM11, draw)
    if 25.8 <= t < 26.9:
        sb.bubble(k, "Happy compliance!", top(CAM11, 420, xs.FEET, -238, lift=115), "up", size=30, t=t, t0=25.8)
    if 26.0 <= t < 26.25:                                 # the off-screen thud
        kit.sfx(k, "THUD", 70, 420, 46, rot=-0.2)


PANELS = [(0.0, 2.4, s1), (2.4, 3.4, s1b), (3.4, 5.0, s2), (5.0, 6.2, s3), (6.2, 9.2, s4), (9.2, 11.5, s5),
          (11.5, 13.1, s6), (13.1, 15.5, s7), (15.5, 19.5, s8), (19.5, 21.2, s9), (21.2, 25.0, s10),
          (25.0, 25.7, s10b), (25.7, 27.5, s11)]
