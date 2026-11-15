"""SILENT STORYBOARD v2 (review polish; iwry_sb.py / iwry_sb_v1.py = v1, kept). v2: the robot rolls in hunched
so its head passes below Don's face, then rises at its spot; its eyes turn to Sofía before the arm snaps out;
on the whisper it tucks its arms in and tilts its head toward Don; bigger whisper text; metal separated
from the buns (dark gap, darker rims, one highlight) and a small settle when the dome lifts; narrative loop
ending: Sofía's eyes go to Don, then to us, a resigned blink, one hoop swinging a beat late, the bolt drops
during the hold, and Don's pun starts again.

v1 notes: SILENT STORYBOARD v1 for "I Will Replace You" (UptimeZ Inc.), concept v4: 12 shots, 25 s, no audio.
Built on iwry_common (set, per-shot staging, cameras) with the approved motion-test acting for shots 6-11.
Timing is the v4 beat sheet. Writes nothing itself: render with engine_v.py."""
import math
import anim
import iwry_common as ic
import day1_sb_v3 as sb
import cafe_kit as ck
from iwry_common import u, state, shot, head_top, to_screen
from anim import ease, lerp, back_out

DURATION = 25.0
RAW_T = 0.0
W = ic.w
ic.CAMS = dict(ic.CAMS)
ic.CAMS[9] = (238, 615, 1.60, "point")                  # framed a little higher: less table front
ic.CAMS[4] = (262, 640, 1.25, "\"sir?\"")                # a little toward Sofía, so her raised finger reads
FINGER = (-14, 40, 158, 14)
STAND_S = (-8, 0, 8, 0)


def sofx(a, b, v):
    return tuple(lerp(x, y, v) for x, y in zip(a, b))


# ------------------------------------------------------------------ 1  the pun (0-3)
def s1(t, tl):
    lean = ease(u(t, 0.0, 0.6))                          # movement in the first second
    return state(stage=1, robot=None, don_x=lerp(380, 362, lean), don_face="grin", don_look=(-1, 0.5),
                 sof_face="neutral", sof_look=(0.3, 0))


def b1(k, t, out, cam):
    if 0.2 <= t < 2.95:
        sb.bubble(k, "Nice hoops.\nCan I get in your loop?", head_top(out, "don", cam), "up", size=28, t=t, t0=0.2)


# ------------------------------------------------------------------ 2  Sofía's comeback (3-4.8)
def s2(t, tl):
    return state(stage=2, robot=None, sof_face="unimpressed", sof_look=(0.9, 0))


def b2(k, t, out, cam):
    if 3.15 <= t < 4.75:
        sb.bubble(k, "You're out\nof the loop.", head_top(out, "sof", cam, 80), "up", size=32, t=t, t0=3.15)


# ------------------------------------------------------------------ 3  the robot arrives (4.8-7.4)
def s3(t, tl):
    v = ease(u(t, 4.8, 1.1))
    moving = t < 5.9
    wob = 0.05 * math.sin(t * 15) if moving else 0.0
    rise = ease(u(t, 5.9, 0.22))                        # straightens up eagerly once it arrives
    hunch = (0.04, 34, 46, (25, -60), (-25, 60))       # passes below Don's face
    stand = W.POSES["stand"]
    pose = tuple(lerp(a, b, rise) if not isinstance(a, tuple) else (lerp(a[0], b[0], rise), lerp(a[1], b[1], rise))
                 for a, b in zip(hunch, stand))
    return state(stage=3, robot_x=lerp(560, 282, v), r_pose=pose, r_locked=False, r_tray=None,
                 r_front=moving,
                 r_wobble=wob, r_face="eager", r_look=(1, 0),
                 sof_face="unimpressed" if t < 5.4 else "smile", sof_look=(0.9, -0.1) if t >= 5.4 else (0.6, 0),
                 don_face="smug", don_look=(-0.6, 0))


def b3(k, t, out, cam):
    if 5.6 <= t < 7.35:
        hx, hy = to_screen(out["sof"]["head"], cam)
        ck.thought(k, "Replace him.", (hx + 10, hy - 70), 200, 190, size=32)


# ------------------------------------------------------------------ 4  ignored (7.4-10.2)
def s4(t, tl):
    up = ease(u(t, 7.45, 0.25))
    down = ease(u(t, 9.0, 0.6))
    pose = sofx(sofx(STAND_S, FINGER, up), STAND_S, down)
    leaving = t >= 9.8
    lv = ease(u(t, 9.8, 0.4))
    return state(stage=4, robot_x=lerp(300, 420, lv), r_pose="travel" if leaving else "stand", r_front=leaving,
                 r_wobble=0.06 * math.sin(t * 15) if leaving else 0.0, r_face="eager", r_look=(1, 0),
                 sof_pose=pose, sof_face="smile" if t < 8.0 else "unimpressed", sof_look=(0.9, 0),
                 don_face="neutral", don_look=(-0.3, 0.5) if t >= 8.9 else (-0.8, 0))


def b4(k, t, out, cam):
    if 7.6 <= t < 8.9:
        sb.bubble(k, "Ready to order, sir?", head_top(out, "robot", cam, 75), "up", size=28, t=t, t0=7.6)
    if 8.95 <= t < 9.95:
        sb.bubble(k, "Two cheeseburgers.", head_top(out, "don", cam), "up", size=28, t=t, t0=8.95)


# ------------------------------------------------------------------ 5  the wide (10.2-11.7)
def s5(t, tl):
    v = u(t, 10.2, 1.5)
    return state(stage=5, robot="wide", robot_x=lerp(640, 520, v), r_wobble=0.06 * math.sin(t * 15),
                 sof_face="unimpressed", sof_look=(0.6, 0), don_face="neutral")


# ------------------------------------------------------------------ 6  the reveal (11.7-14.3)
def s6(t, tl):
    settle = u(t, 12.15, 0.25)                          # a tiny settle as the dome comes off
    dy = -3 * math.sin(math.pi * settle) if 0 < settle < 1 else 0.0
    return state(stage=6, robot=None, burgers=True, burger_v=3, burger_dy=dy, dome=u(t, 11.85, 0.35),
                 slip=u(t, 12.8, 0.4))


# ------------------------------------------------------------------ 7  Don (14.3-16.1)
def s7(t, tl):
    lift = u(t, 14.3, 0.25)
    pose = tuple(lerp(a, b, ease(lift)) for a, b in zip((-8, 0, 20, 0), (-8, 0, 128, 28)))
    return state(stage=7, don_pose=pose, don_face="shock" if t >= 14.4 else "neutral", don_look=(0, -0.3),
                 don_wrench=lift >= 1, oil_drop=u(t, 14.95, 0.3) if t >= 14.95 else None, r_face="proud")


def b7(k, t, out, cam):
    if 14.55 <= t < 16.05:
        sb.bubble(k, "WHAT IS THIS?!", head_top(out, "don", cam), "up", size=34, t=t, t0=14.55)


# ------------------------------------------------------------------ 8  "Are you hiring, sir?" (16.1-18.1)
def s8(t, tl):
    tie = ease(u(t, 16.25, 0.2)) * (1 - ease(u(t, 16.85, 0.25)))      # one motivated move: the bow-tie tug
    return state(stage=8, r_pose=W.blend("stand", "tie", tie), r_face="pleading", r_look=(0.4, -0.2),
                 r_talk=(0.5 if int(t * 8) % 2 == 0 else 0.15) if 16.5 <= t < 17.6 else 0.0)


def b8(k, t, out, cam):
    if 16.5 <= t < 18.0:
        sb.bubble(k, "Are you hiring, sir?", head_top(out, "robot", cam, 75), "up", size=30, t=t, t0=16.5)


# ------------------------------------------------------------------ 9  the point (18.1-20.1)
def s9(t, tl):
    snap = u(t, 18.25, 0.17)                           # eyes go to Sofía first (18.1), then the arm snaps out
    e = min(1.0, back_out(snap, 1.6)) if snap < 1 else 1.0
    return state(stage=9, r_pose=W.blend("tie", "lock", e), r_locked=snap >= 0.6,
                 r_face="stern" if snap >= 0.5 else "eager", r_look=(-1.6, 0.1),
                 r_talk=0.9 if 18.35 <= t < 19.6 and int(t * 8) % 2 == 0 else 0.0,
                 sof_face="horrified" if t >= 18.4 else "unimpressed", sof_look=(0.8, 0))


def b9(k, t, out, cam):
    if 18.42 <= t < 19.95:
        hx, hy = out["robot"]["head"]
        ck.shout(k, "I WILL\nREPLACE YOU!", to_screen((hx - 10, hy - 30), cam), 300, 190, size=44)


# ------------------------------------------------------------------ 10  the whisper (20.1-21.9)
def s10(t, tl):
    col = ease(u(t, 20.4, 0.3))
    wob = 0.04 * math.sin((t - 21.8) * 14) if t >= 21.8 else 0.0
    lk, ln = W.POSES["lock"], W.POSES["lean"]
    tucked = (ln[0], ln[1], ln[2], (14, -40), (-14, 40))          # arms drawn in close to the body
    pose = tuple(lerp(a, b, col) if not isinstance(a, tuple) else (lerp(a[0], b[0], col), lerp(a[1], b[1], col))
                 for a, b in zip(lk, tucked))
    return state(stage=10, r_pose=pose, r_locked=col < 0.3,
                 r_face="stern" if col < 0.3 else "timid", r_look=(lerp(-1, 0.7, col), lerp(0, -0.8, col)),
                 r_wobble=wob, r_head_dx=lerp(0, 10, col), r_head_rot=lerp(0, 0.12, col),
                 r_talk=(0.5 if int(t * 8) % 2 == 0 else 0.15) if 20.75 <= t < 21.75 else 0.0,
                 don_face="neutral", don_look=(-0.8, 0))


def b10(k, t, out, cam):
    if 20.75 <= t < 21.9:
        hx, hy = out["robot"]["head"]
        ck.whisper(k, "If that's okay, sir?", to_screen((hx + 20, hy - 40), cam), 260, 225, size=35)


# ------------------------------------------------------------------ 11  "Approved." (21.9-23.4)
def s11(t, tl):
    if t < 22.4:
        return state(stage=11, don_pose=(-8, 0, -30, -125), don_face="smug", don_chin=1, don_look=(0, -0.2))
    if t < 22.7:                                            # the glance at Sofía, hand still on his chest
        return state(stage=11, don_pose=(-8, 0, -30, -125), don_face="grin", don_look=(-1, 0))
    return state(stage=11, don_pose=(-8, 0, 40, 120), don_face="grin", don_look=(-0.4, 0), don_thumb=True)


def b11(k, t, out, cam):
    if 22.75 <= t < 23.4:
        sb.bubble(k, "Approved.", head_top(out, "don", cam), "up", size=34, t=t, t0=22.75)


# ------------------------------------------------------------------ 12  to camera (23.4-25)
def s12(t, tl):
    """Narrative loop: eyes slide to Don (off right), then to us, a resigned blink, the hoops swing a beat late;
    the bolt drops during the hold; Don's pun starts again."""
    to_don = ease(u(t, 23.4, 0.3))
    to_us = ease(u(t, 23.85, 0.2))
    lx = lerp(lerp(0.4, 1.0, to_don), 0.0, to_us)
    sw = t - 23.9                                       # hoops (and hair) trail the head turn
    lag = (7 * math.sin(sw * 11) * math.exp(-sw * 4), 0) if sw > 0 else (0, 0)
    face = "closed" if 24.15 <= t < 24.35 else "unimpressed"
    return state(stage=12, sof_face=face, sof_look=(lx, 0), sof_lag=lag,
                 edge_bolt=u(t, 24.5, 0.3))                      # rests on the edge in view, then tips off


PANELS = [
    (0.0, 3.0, shot(1, s1, (b1,))), (3.0, 4.8, shot(2, s2, (b2,))), (4.8, 7.4, shot(3, s3, (b3,))),
    (7.4, 10.2, shot(4, s4, (b4,))), (10.2, 11.7, shot(5, s5)), (11.7, 14.3, shot(6, s6)),
    (14.3, 16.1, shot(7, s7, (b7,))), (16.1, 18.1, shot(8, s8, (b8,))), (18.1, 20.1, shot(9, s9, (b9,))),
    (20.1, 21.9, shot(10, s10, (b10,))), (21.9, 23.4, shot(11, s11, (b11,))), (23.4, 25.0, shot(12, s12)),
]
