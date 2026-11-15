"""v4 (tg_sb_v3.py = v3, kept), after a frame check: shot 1's pull-up ends a little further left, so the banner
reads "THANKFUL" whole and the tail lands on Don; shot 11 is framed wider so the whole turkey leg reads (bone,
frill, bitten end) over the glowing screen, and "OK. SIGNED." points at the covered screen, not the hat.
SILENT STORYBOARD v3 (tg_sb_v2.py = v2, tg_sb_v1.py = v1, kept) for "Raises for Everyone", 35.0 s, 540x960.
v3: three emoji reaction pops (no words, one emoji each, a round tinted bubble with no tail, beside the head):
Sofía 🙄 in 4b, Sofía 😮‍💨 in 8d, Pam 💗 while she pats her hair in 9. 4b and 8d grow to 0.8 s so the pops read;
everything after 4b moves 0.3 s later, everything after 8d 0.6 s later (the shot functions below keep the v2 times
and are re-timed by PANELS).

v2: 34.4 s.
v2: a new ending. With the verdict covered, Don slides the form to the ROBOT: "Sign it." From behind the turkey
leg, muffled: "OK. SIGNED." The last image is the form itself (the same one as shot 2): the robot's squiggle on
the signature line and a red stamp, 100% SATISFACTION. Then frame 0: Don slaps down the next form.

v1 notes: 33.0 s. Lines are shown as bubbles
(timed to the estimated read), no sound yet. Camera grammar after the set review: close-ups carry the jokes (faces
25-35 % bigger than the set frames), wides only to orient, two tilted shots only (5 and 11), the pauses protected.

 1   0.0- 2.6  ECU: Don's hand slaps the form down by the turkey (frame 0), the camera pulls up to Don grinning,
               the banner and the table. DON: "Raises for everyone! Sign here."
 2   2.6- 3.9  insert: the form, readable
 3   3.9- 7.0  tight two-shot, a slow push to Pam. SOFÍA: "Still hoping for a raise?"  PAM: "I'm expecting."
 4   7.0- 8.8  Don, low, the tie big: "Boy or girl? HA!" (slaps the table)
 4b  8.8- 9.3  Sofía: one eyebrow
 5   9.3-10.9  TILTED robot close-up, red flash: POLICY VIOLATION. (the word is the screen)
 6  10.9-11.9  Don: the smile freezes; he taps the form
 7  11.9-16.7  Pam and the form. PAM: "A raise for saying we don't want one?"  DON (off): "Now you're getting it."
               Pam pushes the form back: "No."
 8a 16.7-18.3  Don, low, the turkey in the foreground: tears off a leg, points it: "You failed."
 8b 18.3-19.9  SOFÍA: "She refused. She didn't fail."
 8c 19.9-21.4  Don takes a big bite instead of answering: "Same thing here." (mouth full)
 8d 21.4-21.9  Sofía closes her eyes
 9  21.9-25.3  fixed medium on Pam: she rises into frame, pats her hair (blush), tugs the cardigan, stares.
               PAM: "You're a walking policy violation."
10a 25.3-26.8  Don, smug, turns to the robot: "HR. Back me up."
10b 26.8-28.9  Don and the robot: it scans Pam (far left), then Don; silence; ACCURATE. in green; Don freezes mid-bite
10c 28.9-29.4  Sofía: the tiny smile
11  29.4-32.4  TILTED: one beat of collapse, the grin comes back, the drumstick over the word, the form slid to
               the robot. DON: "Sign it."  ROBOT (muffled, behind the leg): "OK. SIGNED."
11b 32.4-34.4  insert: the form, signed by the robot; the stamp 100% SATISFACTION slams down. Loop to frame 0."""
import math
import cairo
import kit
from kit import clamp, ease, lerp, INK, ellipse
import anim
import tg_set as ts
import sofia_tg as st
import pam_tg as pt
import don_tg as dt
import robot_tg as rt
import xmas_bubbles as xb
import brand

DURATION = 35.0
RAW_T = 0.0
SEAT = ts.FEET + 66              # storyboard: seated a touch higher than the set sheet (more torso over the table)
DON_FEET = ts.FEET + 56          # storyboard: Don stands closer to the table so his hands reach it
POSE_SLAP_DOWN = (-8, 0, 16, 2)  # the slap: right arm straight down onto the form
POSE_TAP_DOWN = (-8, 0, 22, -6)  # the tap: right hand on the table, finger on the form
DON_HY = -300 * kit.PEOPLE["DON"]["h"] + 78 - 44
PAM_HY = -300 * kit.PEOPLE["PAM"]["h"] + 78 - 44
SOF_HY = -300 * st.H + 78 - 44
ROB_HY = rt.w.HEAD_Y
X = dict(sofia=175, pam=300, don=560, robot=650)


def u(t, t0, d):
    return clamp((t - t0) / d)


def world(k, cam, draw, rot=0.0):
    c = k.c
    c.save()
    if rot:                                                  # a tilted (Dutch) camera: rotate about the frame centre
        c.translate(270, 480); c.rotate(rot); c.scale(1.12, 1.12); c.translate(-270, -480)
    ts.with_cam(c, cam); draw(); c.restore()


def top(cam, x, feet, hy, lift=62):
    return ts.to_screen(cam, x, feet + hy - lift)


def legs_at(t):
    return 2 if t < 17.0 else 1


def room(k, t):
    ts.set_dressing(k, boil=int(t * 4))


def sofia(k, t, x=X["sofia"], pose="stand", face="neutral", look=(0.9, 0), lean=0):
    ts.seated(k, lambda: st.sofia(k, x, SEAT, 1.0, pose, face, look=look, lean=lean, seed=95))


HELD = []


def pam(k, x=X["pam"], feet=SEAT, pose="stand", face="neutral", look=(0.8, 0), form=False, mouth=None):
    """form=True: the form is held up over the table edge (drawn later by held_form, after the table)."""
    out = {}
    ts.seated(k, lambda: out.update(pt.pam(k, x, feet, 1.0, pose, face, look=look, seed=96, mouth=mouth)))
    HELD[:] = [out["hands"]] if form else []


def held_form(k):
    for hands in HELD:
        pt.form_held(k, [(hx, hy - 14) for hx, hy in hands], 1.0, 960)
    HELD.clear()


# ------------------------------------------------------------------ 1  the slap, then the pull-up to Don
CAM1A = (605, 590, 3.0)
CAM1B = (446, 528, 1.04)


def _form0():
    sc = kit.Ctx(cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 4, 4)), 0)
    hx, hy = dt.don(sc, X["don"], DON_FEET, 1.0, POSE_SLAP_DOWN, "grin", seed=98)["hands"][1]
    return (hx, ts.TABLE_TOP + 9)


FORM0 = _form0()


def cam1(t):
    v = ease(u(t, 0.45, 1.0))
    return tuple(lerp(a, b, v) for a, b in zip(CAM1A, CAM1B))


def slap_lines(k, x, y, s=1.0):
    c = k.c
    c.set_source_rgb(*INK); c.set_line_width(2.4); c.set_line_cap(1)
    for a_ in (-2.7, -2.25, -0.9, -0.45):
        c.move_to(x + math.cos(a_) * 22 * s, y + math.sin(a_) * 14 * s)
        c.line_to(x + math.cos(a_) * 34 * s, y + math.sin(a_) * 22 * s); c.stroke()


def s1(k, t, tl):
    cam = cam1(RAW_T)
    land = u(t, 0.0, 0.17)

    def draw():
        room(k, t)
        sofia(k, t, face="neutral", look=(0.9, 0))
        pam(k, face="neutral")
        rt.robot(k, X["robot"], ts.FEET_BACK, 1.0, "stand", "eager", seed=97)
        pose = anim.tween((-8, 0, 60, 60), POSE_SLAP_DOWN, land) if land < 1 else anim.key(POSE_SLAP_DOWN)
        o = dt.don(k, X["don"], DON_FEET, 1.0, pose, "grin", look=(-0.6, 0.4), seed=98)
        ts.table(k, 2, form_at=FORM0)
        hx, hy = o["hands"][1]
        ellipse(k, hx, max(hy, ts.TABLE_TOP - 30), 10, 10, dt.SKIN, 990, shadow=False, lw=2)   # the hand over the edge
        if 0.12 <= t < 0.6:
            slap_lines(k, FORM0[0], FORM0[1] - 6)
    world(k, cam, draw)
    xb.speech(k, "Raises for everyone!\nSign here.", [(400, -40)] if t < 0.9 else top(cam, X["don"], DON_FEET, DON_HY),
              t, -0.4, at=(270, 200))


# ------------------------------------------------------------------ 2  insert: the form
def form_insert(k, t):
    c = k.c
    c.set_source_rgb(*ts.WOOD); c.paint()
    c.set_source_rgb(*ts.WOOD_DARK); c.set_line_width(3)
    for gy in range(80, 960, 90):
        c.move_to(0, gy); c.curve_to(180, gy + 14, 360, gy - 10, 540, gy + 6); c.stroke()
    c.save(); c.translate(270, 470); c.rotate(-0.06)
    kit.rect(k, -200, -270, 400, 540, (1, 1, 1), 1300, lw=3)
    c.set_source_rgb(*brand.GREEN); c.rectangle(-196, -266, 392, 52); c.fill()
    brand.mark(c, -184, -258, 36, zzz=False)
    kit.text(k, "UPTIMEZ INC.  ·  HR", 20, -232, 22, (1, 1, 1), font="Inter", bold=True)
    kit.text(k, "EMPLOYEE SATISFACTION", 0, -150, 26, INK, font="Inter", bold=True)
    kit.text(k, "FORM 11-B  ·  THANKSGIVING", 0, -118, 14, (0.45, 0.45, 0.45), font="Inter")
    for i, ln in enumerate(("I AM HAPPY WITH", "MY CURRENT", "SALARY.")):
        kit.text(k, ln, 0, -40 + i * 46, 38, INK, font="Inter", bold=True)
    c.set_source_rgb(*INK); c.set_line_width(2.4)
    c.move_to(-140, 196); c.line_to(140, 196); c.stroke()
    kit.text(k, "Signature", -100, 222, 14, (0.45, 0.45, 0.45), font="Inter")
    c.restore()


def s2(k, t, tl):
    form_insert(k, t)


# ------------------------------------------------------------------ 3  Sofía and Pam, tight, a slow push to Pam
def s3(k, t, tl):
    v = ease(u(t, 3.9, 3.1))
    cam = (lerp(240, 262, v), lerp(478, 474, v), lerp(2.15, 2.30, v))

    def draw():
        room(k, t)
        sofia(k, t, x=X["sofia"] + 22, pose="aside", look=(0.9, 0.2), lean=7)
        pam(k, pose=pt.POSE_READ, face="read" if t < 5.8 else "neutral", look=(0, 0.9) if t < 5.8 else (-0.6, 0), form=True)
        ts.table(k, 2, props=False)
        held_form(k)
    world(k, cam, draw)
    if 3.95 <= t < 5.75:
        xb.speech(k, "Still hoping\nfor a raise?", top(cam, X["sofia"] + 22, SEAT, SOF_HY, 40), t, 3.95)
    if 5.85 <= t < 7.0:
        xb.speech(k, "I'm expecting.", top(cam, X["pam"], SEAT, PAM_HY, 40), t, 5.85)


# ------------------------------------------------------------------ 4  Don, low: Boy or girl? HA!
CAM4 = (548, 560, 2.0)


def s4(k, t, tl):
    hit = t >= 8.05

    def draw():
        room(k, t)
        rt.robot(k, X["robot"] + 20, ts.FEET_BACK, 1.0, "stand", "eager", seed=97)
        pose = dt.POSE_LAUGH if hit else dt.POSE_SLAP
        dt.don(k, X["don"] - 12, DON_FEET, 1.0, pose, "laugh" if hit else "grin", look=(-0.8, 0.3), seed=98)
        ts.table(k, 2, props=True)
        if 8.05 <= t < 8.4:
            slap_lines(k, X["don"] + 50, ts.TABLE_TOP + 4, 1.3)
    world(k, CAM4, draw)
    if 7.05 <= t < 8.8:
        xb.speech(k, "Boy or girl? HA!", top(CAM4, X["don"] - 12, DON_FEET, DON_HY, 50), t, 7.05)


def s4b(k, t, tl):
    cam = (200, 470, 2.6)

    def draw():
        room(k, t)
        sofia(k, t, x=X["sofia"] + 22, face="eyebrow", look=(0.9, 0))
        ts.table(k, 2, props=False)
    world(k, cam, draw)


# ------------------------------------------------------------------ 5  TILTED: POLICY VIOLATION.
def s5(k, t, tl):
    cam = (652, 400, 2.5)
    snap = anim.back_out(u(t, 9.3, 0.16), 1.8)

    def draw():
        room(k, t)
        rt.robot(k, X["robot"], ts.FEET_BACK, 1.0, "stand", "violation", seed=97, side=-1,
                 head_dx=8 * snap, head_rot=0.16 * snap)
    world(k, cam, draw, rot=0.19)
    if t < 9.42:                                             # the red flash on the cut
        k.c.set_source_rgba(1, 0.15, 0.1, 0.35); k.c.paint()


# ------------------------------------------------------------------ 6  Don: the smile freezes; the tap
CAM6 = (560, 520, 2.2)


def s6(k, t, tl):
    def draw():
        room(k, t)
        o = dt.don(k, X["don"], DON_FEET, 1.0, POSE_TAP_DOWN, "freeze" if t < 11.5 else "grin", look=(-0.3, 0), seed=98)
        ts.table(k, 2, form_at=FORM0)
        hx, hy = o["hands"][1]
        ellipse(k, hx, hy, 10, 10, dt.SKIN, 990, shadow=False, lw=2)
        dt.tapping_finger(k, (hx, hy), 1.0, ang=-0.3 + (0.15 if int(t * 8) % 2 else 0))
    world(k, CAM6, draw)


# ------------------------------------------------------------------ 7  Pam and the form
CAM7 = (300, 480, 2.3)


def s7(k, t, tl):
    pushing = t >= 15.75

    def draw():
        room(k, t)
        if not pushing:
            pam(k, pose=pt.POSE_READ, face="read" if t < 13.0 else "neutral", look=(0, 0.9) if t < 13.0 else (0.8, 0),
                form=True)
            ts.table(k, 2, props=False)
            held_form(k)
        else:
            pam(k, pose=pt.POSE_PUSH, face="stare", look=(0.8, 0))
            ts.table(k, 2, props=False, form_at=(lerp(350, 450, ease(u(t, 15.75, 0.6))), ts.TABLE_TOP + 8))
    world(k, CAM7, draw)
    if 12.0 <= t < 14.45:
        xb.speech(k, "A raise for saying\nwe don't want one?", top(CAM7, X["pam"], SEAT, PAM_HY, 40), t, 12.0)
    if 14.5 <= t < 15.7:
        xb.speech(k, "Now you're getting it.", [(600, 330)], t, 14.5, at=(300, 210))
    if 15.85 <= t < 16.7:
        xb.speech(k, "No.", top(CAM7, X["pam"], SEAT, PAM_HY, 40), t, 15.85, size=34)


# ------------------------------------------------------------------ 8  You failed. / She refused. / Same thing here.
CAM8 = (545, 560, 2.0)


def s8a(k, t, tl):
    tearing = t < 17.3

    def draw():
        room(k, t)
        if tearing:
            dt.don(k, X["don"] - 10, DON_FEET, 1.0, dt.POSE_TEAR, "grin", look=(-0.6, 0.6), seed=98,
                   leg=(0, lerp(170, 120, u(t, 16.8, 0.4)), 1))
        else:
            dt.don(k, X["don"] - 10, DON_FEET, 1.0, dt.POSE_POINT, "smug", look=(-0.9, 0), seed=98, leg=(0, 178, 1))
        ts.table(k, legs_at(t), props=True)
    world(k, CAM8, draw)
    if 17.35 <= t < 18.3:
        xb.speech(k, "You failed.", top(CAM8, X["don"] - 10, DON_FEET, DON_HY, 50), t, 17.35)


def s8b(k, t, tl):
    cam = (215, 480, 2.4)

    def draw():
        room(k, t)
        sofia(k, t, x=X["sofia"] + 30, pose="correct", look=(0.9, 0), lean=-3)
        ts.table(k, 1, props=False)
    world(k, cam, draw)
    if 18.35 <= t < 19.9:
        xb.speech(k, "She refused.\nShe didn't fail.", top(cam, X["sofia"] + 30, SEAT, SOF_HY, 40), t, 18.35)


def s8c(k, t, tl):
    biting = t < 20.4

    def draw():
        room(k, t)
        if biting:
            dt.don(k, X["don"] - 10, DON_FEET, 1.0, dt.POSE_BITE, "chew", seed=98, leg=(0 if t < 20.15 else 1, -150, 1))
        else:
            dt.don(k, X["don"] - 10, DON_FEET, 1.0, dt.POSE_POINT, "chew", look=(-0.9, 0), seed=98, leg=(1, 178, 1))
        ts.table(k, 1, props=True)
    world(k, CAM8, draw)
    if 20.45 <= t < 21.4:
        xb.speech(k, "Same thing here.", top(CAM8, X["don"] - 10, DON_FEET, DON_HY, 50), t, 20.45)


def s8d(k, t, tl):
    cam = (215, 470, 2.6)

    def draw():
        room(k, t)
        sofia(k, t, x=X["sofia"] + 30, face="closed", look=(0, 0))
        ts.table(k, 1, props=False)
    world(k, cam, draw)


# ------------------------------------------------------------------ 9  Pam rises (camera fixed)
CAM9 = (300, 470, 1.9)


def s9(k, t, tl):
    rise = ease(u(t, 22.1, 0.6))
    feet = lerp(SEAT, ts.FEET + 8, rise)
    if t < 22.75:
        pose, face = "stand", "neutral"
    elif t < 23.4:
        pose, face = pt.POSE_PRIMP, "soft"
    elif t < 23.8:
        pose, face = pt.POSE_TUG, "neutral"
    else:
        pose, face = "stand", "stare"

    def draw():
        room(k, t)
        pam(k, feet=feet, pose=pose, face=face, look=(0.9, 0.9) if face == "soft" else (0.9, 0))
        ts.table(k, 1, props=False)
    world(k, CAM9, draw)
    if 23.6 <= t < 25.3:
        xb.speech(k, "You're a walking\npolicy violation.", top(CAM9, X["pam"], ts.FEET + 8, PAM_HY, 40), t, 23.6)


# ------------------------------------------------------------------ 10  HR. Back me up. / scan / ACCURATE.
CAM10 = (590, 470, 1.7)


def s10a(k, t, tl):
    cam = (570, 520, 2.1)

    def draw():
        room(k, t)
        rt.robot(k, X["robot"] + 20, ts.FEET_BACK, 1.0, "stand", "eager", seed=97)
        dt.don(k, X["don"] - 10, DON_FEET, 1.0, dt.POSE_BACKME, "smug", look=(0.9, 0), seed=98, leg=(1, 100, 0))
        ts.table(k, 1, props=True)
    world(k, cam, draw)
    if 25.35 <= t < 26.8:
        xb.speech(k, "HR. Back me up.", top(cam, X["don"] - 10, DON_FEET, DON_HY, 50), t, 25.35)


def s10b(k, t, tl):
    verdict = t >= 28.05
    if t < 27.3:
        state, look, hrot = "scan", (-1.0, 0.1), 0.3          # far left: Pam
    elif t < 27.75:
        state, look, hrot = "scan", (-0.5, 0.5), 0.14         # down at Don
    elif not verdict:
        state, look, hrot = "eager", (-0.5, 0.5), 0.14        # the silence
    else:
        state, look, hrot = "accurate", (0, 0), 0.0

    def draw():
        room(k, t)
        rt.robot(k, X["robot"] + 20, ts.FEET_BACK, 1.0, "stand", state, look=look, seed=97, side=-1,
                 head_dx=6, head_rot=hrot, t=(t * 1.4) % 1.0)
        if not verdict:
            dt.don(k, X["don"] - 10, DON_FEET, 1.0, dt.POSE_BITE, "smug", look=(0.9, -0.3), seed=98, leg=(1, -150, 1))
        else:
            dt.don(k, X["don"] - 10, DON_FEET, 1.0, dt.POSE_FREEZE_BITE, "bite_freeze", look=(0.8, -0.3), seed=98,
                   leg=(2, -110, 1))
        ts.table(k, 1, props=True)
    world(k, CAM10, draw)


def s10c(k, t, tl):
    cam = (215, 470, 2.6)

    def draw():
        room(k, t)
        sofia(k, t, x=X["sofia"] + 30, face="tiny", look=(0.9, 0))
        ts.table(k, 1, props=False)
    world(k, cam, draw)


# ------------------------------------------------------------------ 11  TILTED: collapse, recovery, Sign it.
CAM11 = (650, 470, 1.45)


def s11(k, t, tl):
    collapse = t < 29.95
    s = 1.0

    def draw():
        room(k, t)
        scratch = kit.Ctx(cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 4, 4)), 0)
        hx, hy = dt.don(scratch, X["don"] - 30, DON_FEET, s, dt.POSE_BLOCK, "grin", seed=98)["hands"][1]
        sx_, sy_ = hx + 47 * s * 1.5, hy
        if collapse:
            rt.robot(k, sx_, sy_ - ROB_HY * s, s, "stand", "accurate", seed=97)
            dt.don(k, X["don"] - 30, DON_FEET, s, dt.POSE_SLUMP, "collapse", seed=98, leg=(2, 95, 1), slump=1.3)
            ts.table(k, 1, props=True)
            return
        up = ease(u(t, 29.95, 0.3))
        rt.robot(k, sx_, sy_ - ROB_HY * s, s, "stand", "accurate", seed=97)
        pose = anim.tween(dt.POSE_SLUMP, dt.POSE_BLOCK, up) if up < 1 else dt.POSE_BLOCK
        o = dt.don(k, X["don"] - 30, DON_FEET, s, tuple(pose) if not isinstance(pose, str) else pose, "grin",
                   look=(-0.8, 0.3), seed=98, leg=(3, lerp(95, 0, up), 1, lerp(1.0, 1.5, up)))
        slide = ease(u(t, 30.3, 0.6))                     # v2: the form goes to the robot, not to Pam
        lx = o["hands"][0][0]
        ts.table(k, 1, props=True, form_at=(lerp(lx + 30, sx_ + 10, slide), ts.TABLE_TOP + 8))
        SCREEN11[:] = [(sx_, sy_)]
    world(k, CAM11, draw, rot=-0.15)
    if 30.95 <= t < 31.65:
        xb.speech(k, "Sign it.", top(CAM11, X["don"] - 30, DON_FEET, DON_HY, 50), t, 30.95)
    if 31.7 <= t < 32.4 and SCREEN11:
        ax, ay = ts.to_screen(CAM11, *SCREEN11[0])
        xb.speech(k, "OK. SIGNED.", [(ax + 56, ay - 6)], t, 31.7, at=(400, 230), size=24, fill=(0.93, 0.98, 0.93))


SCREEN11 = []


def signed_form(k, t):
    """v2 11b: the shot-2 form, signed by a steel hand with a pen, then stamped."""
    c = k.c
    form_insert(k, t)
    prog = u(t, 32.55, 0.65)
    c.save(); c.translate(270, 470); c.rotate(-0.06)
    pts = []
    for i in range(int(60 * prog) + 1):                   # the robot's squiggle on the signature line
        a = i / 60.0
        pts.append((-120 + 240 * a, 186 - 14 * math.sin(a * 19) - 6 * math.sin(a * 41)))
    if len(pts) > 1:
        c.set_source_rgb(0.12, 0.20, 0.55); c.set_line_width(4); c.set_line_cap(1); c.set_line_join(1)
        c.move_to(*pts[0])
        for q in pts[1:]:
            c.line_to(*q)
        c.stroke()
    if t < 33.35:                                         # the steel hand with the pen, following the squiggle
        hx, hy = pts[-1]
        c.set_source_rgb(*INK); c.set_line_width(5); c.move_to(hx, hy); c.line_to(hx + 26, hy - 40); c.stroke()
        kit.rect(k, hx + 16, hy - 60, 300, 26, rt.w.STEEL, 1310, shadow=False, lw=2)
        ellipse(k, hx + 26, hy - 44, 18, 15, rt.w.STEEL_DARK, 1311, shadow=False, lw=2)
    if t >= 33.4:                                         # the stamp slams down
        sc = max(0.02, anim.back_out(u(t, 33.4, 0.18), 2.2))
        c.save(); c.translate(30, 112); c.rotate(-0.16); c.scale(sc * (1 + 0.6 * (1 - min(1, sc))), sc)
        c.set_source_rgb(0.85, 0.12, 0.12); c.set_line_width(7)
        c.rectangle(-150, -46, 300, 92); c.stroke()
        c.set_line_width(2.5); c.rectangle(-140, -36, 280, 72); c.stroke()
        kit.text(k, "100% SATISFACTION", 0, 9, 24, (0.85, 0.12, 0.12), font="Inter", bold=True)
        c.restore()
    c.restore()


def s11b(k, t, tl):
    signed_form(k, t)


def shake(t):
    t = t - 0.6                                           # v3: the stamp lands 0.6 s later
    return 7 * math.sin(t * 90) * (1 - u(t, 33.4, 0.3)) if 33.4 <= t < 33.7 else 0


PANELS_V2 = [(0.0, 2.6, s1), (2.6, 3.9, s2), (3.9, 7.0, s3), (7.0, 8.8, s4), (8.8, 9.3, s4b), (9.3, 10.9, s5),
             (10.9, 11.9, s6), (11.9, 16.7, s7), (16.7, 18.3, s8a), (18.3, 19.9, s8b), (19.9, 21.4, s8c),
             (21.4, 21.9, s8d), (21.9, 25.3, s9), (25.3, 26.8, s10a), (26.8, 28.9, s10b), (28.9, 29.4, s10c),
             (29.4, 32.4, s11), (32.4, 34.4, s11b)]


# ------------------------------------------------------------------ v3: emoji reaction pops
import emoji as _emoji

LILAC = (0.93, 0.90, 0.99)
PINK = (1.00, 0.91, 0.93)


def reaction(k, ch, x, y, tl, t0=0.08, hold=0.55, tint=LILAC, r=52):
    """A round tinted bubble with one emoji, no tail: pops in (overshoot), holds, shrinks away."""
    a = tl - t0
    if a < 0 or a > hold + 0.2:
        return
    sc = anim.back_out(clamp(a / 0.16), 1.9) if a < hold else 1 - (a - hold) / 0.2
    sc = max(0.02, sc)
    c = k.c
    c.save(); c.translate(x, y); c.scale(sc, sc)
    c.set_source_rgba(0, 0, 0, 0.12); c.arc(4, 5, r, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(*tint); c.arc(0, 0, r, 0, 2 * math.pi); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(2.6); c.stroke()
    _emoji.draw_emoji(c, ch, 0, 0, r * 1.25)
    c.restore()


def s4b_v3(k, t, tl):
    s4b(k, 8.8 + min(tl, 0.45), min(tl, 0.45))
    cam = (200, 470, 2.6)
    hx, hy = ts.to_screen(cam, X["sofia"] + 22 + 78, SEAT + SOF_HY - 36)
    reaction(k, "\U0001F644", hx, hy, tl)                              # 🙄


def s8d_v3(k, t, tl):
    s8d(k, 21.4 + min(tl, 0.45), min(tl, 0.45))
    cam = (215, 470, 2.6)
    hx, hy = ts.to_screen(cam, X["sofia"] + 30 + 78, SEAT + SOF_HY - 36)
    reaction(k, "\U0001F62E\u200D\U0001F4A8", hx, hy, tl)              # 😮‍💨


def s9_v3(k, t, tl):
    s9(k, t, tl)
    if 22.8 <= t < 23.5:                                  # v2 times: while she pats her hair; gone before she speaks
        hx, hy = ts.to_screen(CAM9, X["pam"] - 82, ts.FEET + 8 + PAM_HY - 30)
        reaction(k, "\U0001F497", hx, hy, t - 22.8, t0=0.05, hold=0.45, tint=PINK, r=46)   # 💗


def _shift(fn, d):
    def g(k, t, tl):
        fn(k, t - d, tl)
    g.__name__ = fn.__name__
    return g


PANELS = []
for (t0, t1, fn) in PANELS_V2:
    if t1 <= 8.8:
        PANELS.append((t0, t1, fn))
    elif fn is s4b:
        PANELS.append((8.8, 9.6, s4b_v3))
    elif t0 < 21.4:
        PANELS.append((t0 + 0.3, t1 + 0.3, _shift(fn, 0.3)))
    elif fn is s8d:
        PANELS.append((21.7, 22.5, s8d_v3))
    else:
        PANELS.append((t0 + 0.6, t1 + 0.6, _shift(s9_v3 if fn is s9 else fn, 0.6)))
