"""DADDY'S HOME v8, scene 3 "The Green Star", animated from shot list v2 (daddys-home-s3-shot-list-v2.md) and the frames
Tomas approved on 24 Nov ("animuojam 3 scena, gates, patikra"). Same clock, same takes, same sound as v7 (dh_anim3):
only the pictures change. v7 is untouched; this file reuses its timing, mouths and mix.
  3A (3.1 + 3.2)  over Don's shoulder: his arm goes up to the screen; the robot answers; a small push; his hand drops
                  toward the pad
  3B, 3B'         the inserts: the thumb (the series hand, pressing), then the green star
  3C (3.4)        Pam, MCU, behind the counter, the green in her lenses
  3D (3.5)        Don, CU, the fist goes up and pumps again on "sees"; the robot's head beside him
  3E (4.1-4.2)    one held frame: Mom thumps the arm, Sofía sits, then explodes out; the throne rolls on its casters
  3F (4.3)        Mom MCU scrubbing; Sofía frozen behind her, her eyes go to the tag, then to Mom
  python3 dh_anim3_v8.py [nobub]  ->  ../daddys-home/dh_s3_anim_v8.mp4 and dh_s3_anim_v8_strip.png
  (nobub: no bubbles, no sound, for the cold mute test -> /tmp/dh_s3_v8_mute.mp4)"""
import math
import os
import subprocess
import sys
import cairo
import kit
import hands_ps as hp
import fs_storyboard as sb
import dh_props as dp
import dh_layout as dl
import dh_scenes as ds
import dh_anim1 as A
import dh_anim3 as V7
import dh_back as db
import dh_s3_v8 as S
from kit import Ctx, INK

V = "v8"
DPS, F, CH = V7.DPS, sb.F, dp.CHAIR
OUT = "../daddys-home"
ROWS, T0, TOTAL = V7.ROWS, V7.T0, V7.TOTAL
seq, loud, code, speaking = V7.seq, V7.loud, V7.code, V7.speaking
SKIN = kit.PEOPLE["DON"]["skin"]
# 24 Nov (Tomas: "Don sako GRUN"): "Make it green." from dh_voices/film_v8/3.1.wav: the v1 take's "Make it" and a clean
# "green" cut from the front of "Green ones." (a phrase-final "green" comes out "groan" in this voice: F2 1219 Hz;
# the new one 1979 Hz, Whisper "Make it green." 3/3). The v7 take is left as it is.
import numpy as _np, soundfile as _sf
V7.WAV["3.1"] = _np.asarray(_sf.read("dh_voices/film_v8/3.1.wav")[0], dtype=_np.float64)
NOBUB = [False]


def lerp(a, b, u):
    return tuple(x + (y - x) * u for x, y in zip(a, b))


def ease(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


# ------------------------------------------------------------------ 3A: over Don's shoulder (3.1 + 3.2)
DONB = (370, 650)                                           # round 3: higher (his crown out of the bottom quarter), the tail beside the screen
def cam_3a(tt):
    return lerp(S.CAM_3A, S.CAM_3Az, ease((tt - T0["3.2"]) / 1.0))


ARM = [None]                                                # the hand's (x, y, shape) for this drawing
ARM_UP = [[(250, 520, "point_s"), (248, 524, "point_s")]]   # 3.1's arm (a test swaps it: rules §0.6, a new gesture)
JUMP_OUT = [True]                                           # 4.2: she leaps out of the frame on the left (3F: she peeks back in)
JUMP_ARC = [True]                                           # 4.2: anticipation, arc and landing (False: rounds 2-7)
SHOULDER = [(140, 100)]                                           # don_arm sh_at for 3A (None: v8 round 7, drawn over his back)
ARM_BEND = [None]                                           # don_arm bend (None: his default, the elbow out)
SOF_LAP = [(-12, 70, 12, -70)]                              # 3E: Sofía's hands on her clipboard in her lap (None: v7's, on the gold arm by Mom's cloth: "a handshake", 4 cold tests)
MOM_DOWN = [True]                                           # 3E after Sofía sits: Mom holds the cloth in both hands at her waist (silhouette test 24 Nov: no contact read)


def wall_mount(k, x, y, w):
    """Round 8 (Tomas: "1 + laikiklis"): the rating screen bolted to the wall, a grey mounting plate wider than it and a
    bolt at each corner. Cold tests: when Don's arm dropped the screen "stayed in the air", so his raised arm "held" it."""
    h = w * 0.62
    kit.rect(k, x - w / 2 - 6, y - h / 2 - 6, w + 12, h + 12, (0.55, 0.57, 0.60), 3700, shadow=False, lw=2.0)
    for sx_ in (-1, 1):
        for sy_ in (-1, 1):
            kit.ellipse(k, x + sx_ * (w / 2 + 2), y + sy_ * (h / 2 + 2), 2.6, 2.6, (0.82, 0.84, 0.86), 3701, shadow=False, lw=1.2)


def r_3a(k, o, t, tt, n):
    rx, ry = o["robot"]["screen"]
    S.SCREEN[0] = (rx + 60, ry - 92, 80)          # round 3: narrower, so both tails pass beside it
    wall_mount(k, *S.SCREEN[0])
    dp.star_screen(k, *S.SCREEN[0], green=False)
    dp._T(k.c, "1 / 5", S.SCREEN[0][0], ry - 92 + 80 * 0.62 * 0.40, 7.0, col=(1, 1, 1))
    o["robot_head"] = (rx, ry)
    i = int(tt * DPS + 1e-6)                                # drawings since the scene began
    j = i - int(T0["3.2"] * DPS)
    if j < 0:                                               # 3.1: up to the screen in four drawings, then held
        ARM[0] = seq(t, ARM_UP[0])     # round 7: the tip stops short of the screen (cold test: touching it read as holding the sign)     # under the screen, nearly at full reach (a bent elbow swung out; higher, the hand hid "1/5")     # caught already pointing at the screen, left of his box
    else:                                                   # his hand drops as the robot answers (its box goes above its antenna)
        ARM[0] = seq(j / float(DPS), [(294, 1240, "relax")])   # dropped: straight down, out of the frame (a swing crossed his head or the robot)


def fg_3a(k, cam, tt, n, box):
    dy = -2 if (speaking("3.1", tt) and n % 2) else 0
    sh_ = SHOULDER[0] or (118, 132)
    sx_, sy_ = DONB[0] - sh_[0], DONB[1] + sh_[1] + dy      # his raised arm, shoulder to hand: no box over it
    hx_, hy_ = ARM[0][0], ARM[0][1]
    AVOID_EXTRA[:] = []
    if hy_ < 900:                                           # the arm as a chain of small rects along it, not one big box
        for i_ in range(6):
            u_ = i_ / 5.0; px_, py_ = hx_ + (sx_ - hx_) * u_, hy_ + (sy_ - hy_) * u_
            AVOID_EXTRA.append((px_ - 22, py_ - 40, px_ + 22, py_ + 40))
    if SHOULDER[0]:                                         # round 8 (245, 224): the arm drawn first, from his shirt's shoulder
        db.don_arm(k, DONB[0], DONB[1] + dy, 1.0, ARM[0], side=-1, cuff=True, bend=ARM_BEND[0], sh_at=SHOULDER[0])
        hd = db.don_back(k, DONB[0], DONB[1] + dy, 1.0, side=-1)   # his back over the arm's root: it grows out of his shoulder
    else:
        hd = db.don_back(k, DONB[0], DONB[1] + dy, 1.0, side=-1)
        db.don_arm(k, DONB[0], DONB[1] + dy, 1.0, ARM[0], side=-1, cuff=True, bend=ARM_BEND[0])
    if not NOBUB[0]:
        if speaking("3.1", tt):
            say(k, "Make it green.", DONB, n)
        if speaking("3.2", tt):
            hx, hy, _ = S.to_screen(cam, *box["robot_head"])
            say(k, "Human approval required.", (hx, hy), n)


# ------------------------------------------------------------------ 3B: the thumb, the series hand pressing
def r_thumb(k, c, t, tt, n):
    AVOID_EXTRA[:] = []
    dx = seq(t, [150, 40, -6, 0])
    c.set_source_rgb(0.86, 0.88, 0.90); c.paint()                                           # the robot's chest plate
    kit.rect(k, 110, 300, 320, 380, (0.10, 0.13, 0.18), 3501, lw=4)
    for r_ in (40, 62, 84, 106):
        c.set_source_rgb(0.30, 0.75, 0.95); c.set_line_width(5); c.new_path(); c.arc(270, 470, r_, 0.4, 2.74); c.stroke()
    dp._T(c, "APPROVE", 270, 640, 34, col=(0.80, 0.88, 0.95))
    if dx <= 0:
        c.set_source_rgb(0.30, 0.95, 0.55); c.set_line_width(7)
        for r_ in (126, 150):
            c.new_path(); c.arc(270, 470, r_ + (8 if n % 2 else 0), 0, 2 * math.pi); c.stroke()
    c.save(); c.translate(dx, 0)
    # rules page (24 Nov): a press is a fingertip (point); at the frame's edge, the hand and a short cuff stub
    # (of_scenes.insert_cuff) running out of the nearest edge, the sleeve no wider than the arm
    import of_scenes as osc
    hand, w = (400, 490), 104
    d = osc.insert_cuff(c, hand, (640, 560), w * 0.62, SKIN, (0.98, 0.98, 0.96), cuff=(0.98, 0.98, 0.96), stub=190)
    # round 7 (cold test: the ketchup read as nail polish): a shirt cuff, as his white sleeves in 3A, with a gold cufflink
    nx_, ny_ = -d[1], d[0]                                  # across the arm
    for off_ in (96, 134):                                   # the cuff's two seams
        cx_, cy_ = hand[0] - d[0] * off_, hand[1] - d[1] * off_
        c.set_source_rgb(*kit.INK); c.set_line_width(3.2); c.new_path()
        c.move_to(cx_ + nx_ * 30, cy_ + ny_ * 30); c.line_to(cx_ - nx_ * 30, cy_ - ny_ * 30); c.stroke()
    bx_, by_ = hand[0] - d[0] * 115 - nx_ * 16, hand[1] - d[1] * 115 - ny_ * 16
    kit.ellipse(k, bx_, by_, 11, 9, (0.95, 0.76, 0.22), 3512, shadow=False, lw=2.4)      # the cufflink
    hp.draw(k, "point_t", hand[0], hand[1], w, SKIN, d, 1)   # the index on the pad, the thumb tucked (review 2: "a bent finger")
    c.restore()
    return ("Approved.", (468, 452), 1, False, 0) if speaking("3.3", tt) else None


# ------------------------------------------------------------------ 3C: Pam
import contextlib, pam_xmas as _px


@contextlib.contextmanager
def pam_legs():
    """Review 2 (24 Nov): her beige trousers on the beige booth read as part of it. The same colour, opt-in here: the
    inner half of each leg 15 % darker, a heavier outline, and a contact shadow under her shoes."""
    old = _px._legs

    def legs(k, seed, stance=1.0):
        c = k.c
        c.save(); c.set_source_rgba(0.10, 0.08, 0.06, 0.28)          # the contact shadow
        c.translate(0, -2); c.scale(48, 7); c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.fill(); c.restore()
        old(k, seed, stance)
        mid = tuple(v * 0.86 for v in _px.TROUSERS); dark = tuple(v * 0.74 for v in _px.TROUSERS)
        for sx_ in (-15 * stance, 15 * stance):
            top = sx_ / stance; o = 1 if sx_ > 0 else -1
            c.new_path()                                                # the whole leg a step down from the booth's beige
            c.move_to(top - 11, _px.HEM - 6); c.line_to(top + 11, _px.HEM - 6); c.line_to(sx_ + 10, -12); c.line_to(sx_ - 10, -12); c.close_path()
            c.set_source_rgb(*mid); c.fill()
            c.new_path()                                                # the inner half, in shade
            c.move_to(top - o * 11, _px.HEM - 6); c.line_to(top, _px.HEM - 6); c.line_to(sx_, -12); c.line_to(sx_ - o * 10, -12); c.close_path()
            c.set_source_rgb(*dark); c.fill()
            c.set_source_rgb(*_px.TROUSERS_DARK); c.set_line_width(1.6); c.new_path()   # the crease again
            c.move_to(top, _px.HEM + 6); c.line_to(sx_, -16); c.stroke()
            c.new_path()                                                # the heavier outline
            c.move_to(top - 11, _px.HEM - 6); c.line_to(sx_ - 10, -12); c.move_to(top + 11, _px.HEM - 6); c.line_to(sx_ + 10, -12)
            c.set_source_rgb(*kit.INK); c.set_line_width(3.4); c.stroke()
            ellipse_ = kit.ellipse                                      # the shoe again, over the shading
            ellipse_(k, sx_ + o * 3, -6, 15, 8, _px.TRAINER, seed + 70 + sx_, lw=2)
    _px._legs = legs
    try:
        yield
    finally:
        _px._legs = old


def r_pam(k, o, t, tt, n):
    look = (-1, -0.35) if (speaking("3.4", tt) or t < 0.2) else (-0.2, -0.1)   # the line, then one flat glance off it
    one = t >= 0.25                                         # round 7: ONE finger up beside her face, held (the doubt as an action)
    hp.reset("quiet", "point_t" if one else "quiet")
    pose = (-8, 0, 75, 95) if one else "stand"              # silhouette test 2 (24 Nov), variant 4: the arm out, the finger well clear of her head (beside the ear read as a phone)
    with pam_legs():
        q = ds.pb.pam(k, S.PAM[0], S.PAM[1], dl.PS, pose, "incredulous" if one else "neutral", look=look, glasses="up", mouth=code("3.4", tt))
    o["head"] = q["head"]


def fg_3c(k, cam, tt, n, box):
    AVOID_EXTRA[:] = []
    S.c_fg(k, cam)
    if not NOBUB[0] and speaking("3.4", tt):
        hx, hy, _ = S.to_screen(cam, *box["head"])
        say(k, "It's still one.", (hx, hy), n)


# ------------------------------------------------------------------ 3D: Don, the fist
def r_don(k, o, t, tt, n):
    pose = (-8, 0, 170, -30)                                # up from the first drawing: a rising arm crossed his crown
    if 1.05 <= t < 1.22:                                    # up again on "sees"
        pose = (-8, 0, 182, -44)
    hp.reset("relax", "fist")
    d = V7.don_at(k, S.DON3[0], S.DON3[1], pose, "smug", (1, 0), tt, still=True)
    A.mouth(k, d["head"], V7.DS_, loud("3.5", tt))
    o["head"] = d["head"]


def fg_3d(k, cam, tt, n, box):
    AVOID_EXTRA[:] = []
    S.ROBOT_NEAR[0] = (10, 780, 110)                        # round 3: lower, clear of the bubble on Don's left
    S.d_fg(k, cam)
    if not NOBUB[0] and speaking("3.5", tt):
        hx, hy, _ = S.to_screen(cam, *box["head"])
        say(k, "Green is all he sees.", (hx, hy), n)


# ------------------------------------------------------------------ 3E: one held frame (4.1, 4.1', 4.2)
THR = dl.CH[0]                                              # round 10 (set gate): the throne on its set mark, 452, in every shot (was 404 in 3E, 540 in 3F)
MOMX = 366                                                  # 24 Nov (Tomas, /grill-me): 3E and 3F back to round 2's staging;
                                                            # the camera moves for a bubble, the people don't (lessons 358)


import mom_bc as _mb
WIPE_FAR = _mb.wipe_at(118, _mb.BT + 20)                     # her cloth on the throne's side, above the arm (cold test: Sofía's
                                                            # palm on the arm beside the cloth read as a handshake, 3 times)


def throned(k, *a):
    """V7.sofia_throned with her arms set by SOF_LAP (opt-in): v7 lays them along the gold arms, beside Mom's cloth."""
    so = V7.scs.so
    old = so.POSES["throned"]
    if SOF_LAP[0] is not None:
        so.POSES["throned"] = SOF_LAP[0]
    try:
        return V7.sofia_throned(k, *a)
    finally:
        so.POSES["throned"] = old


def mom_e(k, o, tt, n, look=(0.6, 0.8), dy=0):
    out = T0["4.1"] + 0.35 <= tt < T0["4.1'"]          # round 7: on "fired", her free hand points OUT (screen left: the door)
    rest = MOM_DOWN[0] and tt >= T0["4.1'"]            # round 8: once Sofía sits, both hands on the cloth at her waist (no hand near Sofía's)
    hp.reset("point_t" if out else ("fist" if rest else "quiet"), "fist")
    pose = (_mb.mo.ik(-1, -_mb.SH_X - 92, _mb.BT + 50) + WIPE_FAR[2:]) if out else (_mb.POSES["bag"] if rest else WIPE_FAR)
    with A.About(k.c, MOMX, F + 8, 1.0, 1.0, dy):
        m = sb.mfs.mom(k, MOMX, F + 8, dl.MS, pose, "sweet", look=look, mouth=code("4.1", tt))
    o["head"] = m["head"]
    o["mom_hand"] = m["hands"][0] if out else None
    return m


def r_thump(k, o, t, tt, n):
    i = min(20, int(t * DPS + 1e-6))
    sd = seq(t, [1.0, 1.0, 0.45, -0.08, 0.04, 0.0])
    dp.ceo_chair(k, THR, CH[1], CH[2], seat_drop=sd, puff=(i == 2))
    if i in (2, 3):                                        # PFFT: two short marks off the seat, no more
        ds._lines(k, [(THR - 34, CH[1] - 128 * CH[2], THR - 34, CH[1] - 146 * CH[2]), (THR + 34, CH[1] - 128 * CH[2], THR + 34, CH[1] - 146 * CH[2])])
    m = mom_e(k, o, tt, n, (0.6, 0.6), 0)               # (her thump bob moved her cheek off the held tail)
    if i >= 4:
        V7.scrub(k, m["hands"][1][0], m["hands"][1][1], n)


def r_sits(k, o, t, tt, n):
    i = min(30, int(t * DPS + 1e-6))
    dp.ceo_chair(k, THR, CH[1], CH[2])
    hp.reset("palm", "palm")
    if i < 2:                                               # arriving, from the right, mid-step
        ds.scs.sofia(k, THR + (70, 34)[i], F + 4, dl.SS, "hold", "smile", look=(-0.6, 0.2))
    else:
        with A.About(k.c, THR, CH[1], 1.0, 1.0, (7, -3, 0)[min(2, i - 2)]):
            throned(k, THR, CH[1], CH[2], "smile", (-0.6, 0))
    m = mom_e(k, o, tt, n)
    if not (MOM_DOWN[0] and tt >= T0["4.1'"]):
        V7.scrub(k, m["hands"][1][0], m["hands"][1][1], n)


def r_up(k, o, t, tt, n):
    """4.2 (round 2): four drawings of held fright in the throne, then she goes up and to the left, the clipboard the
    same way, the throne right on its casters (three short lines behind it, gone when it stops). Mom scrubs on."""
    i = min(20, int(t * DPS + 1e-6))
    j = max(0, i - V7.HOLD); tj = j / float(DPS)
    cx = seq(tj, [THR, THR + 5, THR + 8, THR + 10, THR + 10, THR + 10])   # a jolt, not a roll: the tag stays whole in frame
    dp.TAG_ANG[0] = seq(tj, [0, 0.5, 0.6, 0.3, -0.2, 0.1, 0])
    dp.ceo_chair(k, cx, CH[1], CH[2])
    if i < V7.HOLD:
        if JUMP_ARC[0] and i == V7.HOLD - 1:                # round 8 (lesson 21): the anticipation, pressed down into the seat
            with A.About(k.c, THR, CH[1], 1.04, 0.93):     # (0.88 pushed her face down under the app buttons)
                throned(k, THR, CH[1], CH[2], "horrified", (-1, 0))
        else:
            throned(k, THR, CH[1], CH[2], "horrified", (-1, 0) if i else (-0.6, 0))
    else:
        if 1 <= j <= 3:
            tx = cx - 78
            ds._lines(k, [(tx - 22, F - 120, tx - 2, F - 120), (tx - 30, F - 86, tx - 4, F - 86), (tx - 22, F - 52, tx - 2, F - 52)])
        if JUMP_OUT[0]:                                     # round 9 (Tomas: "she should jump further and leave the frame"):
            up = [34, 62, 72, 62, 44, 28, 20][min(j, 6)]    # one leap left, behind Mom, out past the left edge
            sx_ = THR + (40 - THR) * min(1.0, (j + 1) / 6.0)
            sy = [1.14, 1.06, 1.0, 1.0, 1.02, 1.04, 1.04][min(j, 6)]
        elif JUMP_ARC[0]:                                   # round 8: up, over, down onto the floor (cold test: "lifted, no crouch, no arc";
            up = [34, 60, 70, 54, 24, 0, 0][min(j, 6)]      # she hung at 58 above the seat to the end; peak 70 keeps her face under the title bar)
            sx_ = THR + (352 - THR) * min(1.0, (j + 1) / 5.0)      # off the throne at once: at THR her face sits under the app buttons
            sy = [1.14, 1.06, 1.0, 1.02, 1.06, 0.94, 1.0][min(j, 6)]   # stretch going up, squash on landing (0.86 read as "shorter, another girl"), settle
        else:
            up = seq(tj, [34, 60, 66, 62, 58, 58, 58])
            sx_ = THR + (352 - THR) * min(1.0, (j + 1) / 4.0)
            sy = seq(tj, [1.08, 1.04, 1, 1, 1, 1, 1])
        hp.reset("palm", "palm")
        with A.About(k.c, sx_, F + 4 - up, 2.0 - sy, sy):
            ds.scs.sofia(k, sx_, F + 4 - up, dl.SS, "show", "horrified", look=(0.4, -0.6), lean=-0.2, tablet_kind="none")
        u = min(1.0, (j + 1) / 7.0)
        ds._clip(k, 372 - 72 * u, F - 150 - 150 * math.sin(u * 2.4) + 28 * u, -0.3 - 2.4 * u)
        if j <= 2:
            ds._lines(k, [(sx_ - 14, F - 30, sx_ - 20, F - 18), (sx_ + 14, F - 30, sx_ + 20, F - 18)])
    m = mom_e(k, o, tt, n)
    if not (MOM_DOWN[0] and tt >= T0["4.1'"]):
        V7.scrub(k, m["hands"][1][0], m["hands"][1][1], n)


def fg_3e(k, cam, tt, n, box):
    AVOID_EXTRA[:] = []
    if box.get("mom_hand"):                                 # her pointing hand stays clear of the box
        hx_, hy_, _ = S.to_screen(cam, *box["mom_hand"])
        AVOID_EXTRA.append((hx_ - 40, hy_ - 40, hx_ + 40, hy_ + 40))
    AVOID_EXTRA.append((300, 380, 540, 860))               # round 10: the throne side (Sofía, the rail) is not this line's wall
    if not NOBUB[0] and speaking("4.1", tt):
        hx, hy, _ = S.to_screen(cam, *box["head"])
        line = "He once fired a man..." if tt < T0["4.1'"] else "...for sitting in that chair."
        say(k, line, (hx, hy), n)


# ------------------------------------------------------------------ 3F: "Different chair." (round 2's staging)
SOF3F = 300                                                 # round 9: she peeks back in from the left edge (was 410, behind Mom: "a floating head")
def r_mom(k, o, t, tt, n):
    dp.ceo_chair(k, THR, CH[1], CH[2])                     # on its mark, to her right as in 3E (she stands beside it)
    after = tt - (V7.AT["4.3"] + len(V7.WAV["4.3"]) / float(V7.SR))
    hp.reset("palm", "palm")
    if after < 0:                                           # frozen; her eyes go up to the price
        lk = (0.2, -0.2) if t < 0.35 else (0.55, -0.7)
        ds.scs.sofia(k, SOF3F, F - 40, dl.SS * 0.92, "show", "horrified", look=lk, lean=0.14, tablet_kind="none")
    else:                                                   # after the line: flat, her eyes slide to Mom
        u = min(1.0, after / 0.17)
        ds.scs.sofia(k, SOF3F, F - 40, dl.SS * 0.92, "show", "deadpan", look=(0.55 + 0.45 * u, -0.7 + 0.9 * u), lean=0.14 - 0.10 * u, tablet_kind="none")
    hp.reset("quiet", "fist")
    m = sb.mfs.mom(k, MOMX, F + 8, dl.MS, "wipe", "sweet", look=(0.5, 0.9), mouth=code("4.3", tt))
    V7.scrub(k, m["hands"][1][0], m["hands"][1][1], n)
    o["head"] = m["head"]


def fg_3f(k, cam, tt, n, box):
    if not NOBUB[0] and speaking("4.3", tt):
        hx, hy, _ = S.to_screen(cam, *box["head"])
        say(k, "Different chair.", (hx, hy), n)
    AVOID_EXTRA[:] = []


# ------------------------------------------------------------------ bubbles: speech.draw, checked by speech_gate (CLAUDE.md, 24 Nov)
HELD = {}                                                   # text -> the box and side chosen at the line's first drawing
R_HELD = {}                                                 # the head radius each line was first measured with
from speech_gate import RAIL                                # the app's buttons (CLAUDE.md "Text"): one rect, the gate's
AVOID_EXTRA = []                                            # this drawing's other no-go rects (Don's raised arm in 3A)
CHECKS = []                                                 # (n, text, faults) for every bubble drawn
BOXES = []                                                  # (n, text, box) for the zone audit


def _avoid():
    """The logged signs (price tag, screen, filter), redrawn alone by dh_speech: one rect per piece."""
    import dh_speech as SP
    from scipy import ndimage
    out = []
    if SP.KEEP:
        lab, nl = ndimage.label(SP.keep_mask())
        for sl in ndimage.find_objects(lab):
            out.append((sl[1].start, sl[0].start, sl[1].stop, sl[0].stop))
    return out


def say(k, text, near, n=0, name=None):
    """One line. near is a point near the speaker's head in the frame (picks the logged rig); None = off the frame.
    The face, the mouth and the cheek edges are measured on this drawing (dh_say.measure); the box, the tail and the
    check are the series' (speech.draw, speech_gate.check). The box is held for the line; only the tail follows."""
    import speech, speech_gate
    import dh_speech as SP
    import dh_say as SY
    surf = k.c.get_target()
    before = speech_gate.snapshot(surf)
    k.c.save(); k.c.identity_matrix(); k.c.scale(surf.get_width() / 540.0, surf.get_width() / 540.0)
    try:
        if near is None:
            box, tip = speech.draw(k, text, None, name=name)
            BOXES.append((n, text, box))
            CHECKS.append((n, text, speech_gate.check(surf, box, tip, [], before=before))); return
        rec = SP.pick(near)
        ms = SY.measure(rec)
        hx, hy = SP._frame_matrix(rec).transform_point(*rec["head_u"])
        r = ms["r"]; mx, my = ms["m"]
        if text in R_HELD and r > 1.15 * R_HELD[text]:      # a hand raised beside the head is measured as head (Pam's "one"
            r = R_HELD[text]                                # finger: r 63 -> 109, the box pushed onto her face); keep the line's first r
        R_HELD.setdefault(text, r)
        faces, others = [], []
        for o_ in SP.REG:
            if o_ is rec:
                continue
            try:
                mo = SY.measure(o_); ox, oy = SP._frame_matrix(o_).transform_point(*o_["head_u"])
                if math.hypot(ox - hx, oy - hy) > 0.5 * r:      # a rig logged twice (the iso redraw) is the speaker, not another face
                    others.append((ox, oy, mo["r"]))
            except Exception:
                pass
        head = (hx, hy, r)
        above = aim = None
        if rec.get("kind") == "antenna" or ms.get("bald"):
            above = (ms["top"][0], ms["top"][1] + 1.5)      # the antenna, or a bare crown
        else:
            side = HELD[text][1] if text in HELD else None
            if side is None:                                # the side with more wall at mouth height
                side = -1 if (ms["eL"] - 18) > (522 - ms["eR"]) else 1
            aim = ((ms["eL"] - 1.0) if side < 0 else (ms["eR"] + 1.0), my)   # the cheek's outline at mouth height
        signs = _avoid() + list(AVOID_EXTRA)                # kept clear by the box and checked by the gate
        avoid = signs + [RAIL]
        avoid += [(ox - 1.05 * orr, oy - 1.05 * orr, ox + 1.05 * orr, oy + 1.05 * orr) for ox, oy, orr in others]   # whole heads, hair too
        box, tip = speech.draw(k, text, head, mouth=(mx, my), above=above, aim=aim, others=others, avoid=avoid)
        if text not in HELD:
            HELD[text] = (box, -1 if (tip and tip[0] < hx) else 1)
        BOXES.append((n, text, box))
        CHECKS.append((n, text, speech_gate.check(surf, box, tip, others + [head], above=above, aim=aim, before=before,
                                                  avoid=signs)))
    finally:
        k.c.restore()


# ------------------------------------------------------------------ the frame
SHOTS = {"3.1": ("3A", r_3a, fg_3a, True), "3.2": ("3A", r_3a, fg_3a, True),
         "3.4": ("3C", r_pam, fg_3c, False), "3.5": ("3D", r_don, fg_3d, False),
         "4.1": ("3E", r_thump, fg_3e, False), "4.1'": ("3E", r_sits, fg_3e, False), "4.2": ("3E", r_up, fg_3e, False),
         "4.3": ("3F", r_mom, fg_3f, False)}
SHIFT = {}                                                  # sid -> (dx, dy[, zoom factor]) in set units
CAMS = {"3C": S.CAM_3C, "3D": S.CAM_3D, "3E": (346, 540, 1.45), "3F": (398, 690, 2.3)}   # round 10: setup S3 on the throne's mark (3E), and closer on Mom (3F)
INS = {"3.3": r_thumb, "3.3'": V7.r_green}


def frame(tt, n, hi=1):
    sid = [s for s, _ in ROWS if T0[s] <= tt + 1e-6][-1]
    t = tt - T0[sid]
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540 * hi, 960 * hi); c = cairo.Context(surf); c.scale(hi, hi)
    k = Ctx(c, 0)
    dp.TAG_ANG[0] = 0.0
    kit.HAND[0] = hp.hand
    try:
        if sid in INS:
            line_ = INS[sid](k, c, t, tt, n)
            c.identity_matrix(); c.scale(hi, hi)
            if line_ and not NOBUB[0]:                     # his hand only, his face off the frame: a named card
                say(k, line_[0], None, n, name="DON")
            return surf, sid
        name, draw, fg, robot = SHOTS[sid]
        cam = cam_3a(tt) if name == "3A" else CAMS[name]
        if sid in SHIFT:                                    # the camera moved for this line's bubble (lessons 358), as v7's SHIFT3
            dx_, dy_, f_ = (SHIFT[sid] + (1.0,))[:3]
            cam = (cam[0] + dx_, cam[1] + dy_, cam[2] * f_)
        box = {}

        def fn(k_, o_):
            box.update(o_)
            draw(k_, box, t, tt, n)
        sh = dl.shot(name, [], fn, "", rb=robot, chair=False, cam=cam, ymin=0)
        cam = dl.draw(sh, k)
        c.identity_matrix(); c.scale(hi, hi)
        fg(k, cam, tt, n, box)
    finally:
        kit.HAND[0] = None
    return surf, sid


def _scalp(SY):
    """v8 only: when dh_say's bare-scalp search (offsets to 0.3 r) finds the curl or the shine, look further out on the
    crown (0.35 to 0.55 r): the first outline pixel there, with skin or its shine under it and nothing above."""
    import numpy as np
    orig = SY.measure
    if getattr(orig, "_v8", False):
        return

    def measure(rec):
        fresh = "meas" not in rec
        out = orig(rec)
        if fresh and rec.get("name") == "don" and not out["bald"]:
            N, S_, (mx, my), r = out["N"], out["S"], out["m"], out["r"]
            light = (out["fc"]["a"].sum(-1) > 600)
            for off in (-0.35, -0.45, -0.55, 0.35, 0.45):
                x = int(mx + off * r)
                col = np.nonzero(N[:int(my), x])[0] if 0 <= x < 540 else []
                if not len(col):
                    continue
                y0 = int(col.min())
                if N[max(0, y0 - 30):max(0, y0 - 4), max(0, x - 8):x + 9].any():
                    continue
                below = S_[y0 + 4:y0 + 14, x - 3:x + 4] | light[y0 + 4:y0 + 14, x - 3:x + 4]
                if below.mean() > 0.6:
                    out["top"], out["bald"] = (float(x), y0 + 2), True
                    break
        return out
    measure._v8 = True
    SY.measure = measure


def install_speech():
    import dh_say as SY
    import dh_speech as SP
    SY.install()
    _scalp(SY)
    SP.CARD["Approved."] = "DON"                            # the insert: his hand only, his face off the frame (a card, lessons 551)
    SP._wrap(db, "don_back", "antenna", False)              # Don from behind: the tail comes down onto his bald crown
    SP._fresh(sys.modules[__name__], "frame")
    return SY


def sound(out):
    """v7's mix (dh_anim3.sound), with one change: the fist's whoosh sat 0.05 s before "Green is all he sees." and Whisper
    heard "Brain" in the mix (an effect on a line's first word masks it); it now comes after the line."""
    import numpy as np, soundfile as sf_
    import cs_sfx as fx
    SR = V7.SR
    mix = np.zeros(int((TOTAL + 0.3) * SR))

    def put(a, at_, g=1.0):
        i0 = int(at_ * SR); a = a[:max(0, len(mix) - i0)]; mix[i0:i0 + len(a)] += a * g
    for key, at_ in V7.TAKES:
        put(V7.WAV[key], at_)
    put(fx.tap(220.0), T0["3.3"] + 0.17, 0.6)
    put(fx.chime(), T0["3.3'"] + 0.05, 0.6)
    put(fx.whoosh(0.2), V7.AT["3.5"] + len(V7.WAV["3.5"]) / float(SR) + 0.05, 0.3)   # the fist, after the line
    put(fx.step(), T0["4.1"] + 0.17, 0.7)
    put(fx.whoosh(0.3), T0["4.1"] + 0.19, 0.45)
    put(fx.rustle(0.3), T0["4.1'"] + 0.17, 0.4)
    put(fx.whoosh(0.3), T0["4.2"] + 0.06 + 0.33, 0.6)
    put(fx.scratch(0.4), T0["4.2"] + 0.10 + 0.33, 0.3)
    put(fx.step(), T0["4.2"] + 0.84, 0.6)
    put(fx.tap(140.0), T0["4.2"] + 0.80, 0.5)
    sf_.write(out, mix, SR)


def main(hi=1):
    tmp = "/tmp/dh_s3_%s%s" % (V, "_mute" if NOBUB[0] else ""); os.makedirs(tmp, exist_ok=True)
    ds.ARM_PHONE[0] = True
    me = sys.modules[__name__]
    N = int(round(TOTAL * DPS)); lst = []; tiles = []
    for n in range(N):
        surf, sid = me.frame(n / float(DPS), n, hi)
        p = "%s/d_%04d.png" % (tmp, n); surf.write_to_png(p)
        lst.append("file '%s'\nduration %.5f\n" % (p, 1.0 / DPS))
        if n % 3 == 0:
            tiles.append((p, sid, n / float(DPS)))
    lst.append("file '%s'\n" % p)
    open(tmp + "/list.txt", "w").write("".join(lst))
    if NOBUB[0]:
        out = "/tmp/dh_s3_v8_mute.mp4"
        subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", tmp + "/list.txt",
                               "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-crf", "19", "-preset", "veryfast", "-t", "%.3f" % TOTAL, out])
        print("wrote", out); return
    sound(tmp + "/a.wav")
    out = "%s/dh_s3_anim_%s.mp4" % (OUT, V)
    part = out[:-4] + ".tmp.mp4"
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", tmp + "/list.txt", "-i", tmp + "/a.wav",
                           "-vf", "fps=30,format=yuv420p", "-af", "loudnorm=I=-16:TP=-2:LRA=11,aresample=48000", "-c:v", "libx264", "-crf", "19",
                           "-preset", "veryfast", "-c:a", "aac", "-b:a", "160k", "-t", "%.3f" % TOTAL, part])
    os.rename(part, out)
    cols = 12; tw, th = 180, 320; rows_ = (len(tiles) + cols - 1) // cols
    sheet = cairo.ImageSurface(cairo.FORMAT_RGB24, cols * tw, rows_ * (th + 18)); c = cairo.Context(sheet)
    c.set_source_rgb(1, 1, 1); c.paint()
    for i, (p, sid, tt) in enumerate(tiles):
        im_ = cairo.ImageSurface.create_from_png(p)
        x, y = (i % cols) * tw, (i // cols) * (th + 18)
        c.save(); c.translate(x, y + 18); c.scale(tw / float(im_.get_width()), th / float(im_.get_height())); c.set_source_surface(im_, 0, 0); c.paint(); c.restore()
        c.set_source_rgb(0, 0, 0); c.select_font_face("Inter", 0, 1); c.set_font_size(12); c.move_to(x + 4, y + 13); c.show_text("%s  %.2f" % (sid, tt))
    sheet.write_to_png("%s/dh_s3_anim_%s_strip.png" % (OUT, V))
    print("wrote", out, "%.2f s, %d drawings" % (TOTAL, N))


ZONES = dict(top=96, bottom=720, left=18, right=522)         # CLAUDE.md G3 / "Text": the title bar, the caption quarter, the edges;
                                                            # the button rail is speech_gate.RAIL


ENTRANCES = {("4.1'", "sofia")}                             # she comes in from the right edge, mid-step
EXITS = {("4.2", "sofia"), ("4.3", "sofia")}                # leaving past the edge (4.2) and peeking back in from it (4.3): the edge is the point


SET_MOVES = {("4.2", "throne"): 12}                          # set_gate: the throne's jolt when she leaps off it
SET_AIR = {("4.2", "sofia")}                                # set_gate: off the floor on purpose (the leap)
SET_WALKS = {("4.2", "4.3", "sofia")}                       # set_gate: she leapt out of the frame (4.2) and peeks back in, further back, behind Mom (4.3)


def zone_faults(rect, what):
    """The dead zones a rect (x0, y0, x1, y1) reaches into. what: 'face' (out of the bottom quarter and the rail),
    'sign' (whole under the title bar and off the edges), 'bubble' (speech_gate checks those)."""
    x0, y0, x1, y1 = rect
    out = []
    if y0 < ZONES["top"]:
        out.append("under the title bar")
    if x0 < ZONES["left"] or x1 > ZONES["right"] + 18:
        out.append("at the frame's edge")
    if what == "face":
        if y1 > ZONES["bottom"]:
            out.append("in the caption quarter")
        if x1 > RAIL[0] and y1 > RAIL[1] and y0 < RAIL[3]:
            out.append("under the buttons")
    return out


def gate():
    """Every drawing of the scene with its bubbles; speech_gate's faults per line, and faces and signs in the apps'
    dead zones (24 Nov, Tomas: "check also TikTok, YT, Reels dead zones"). Exit 1 on any."""
    import collections
    import dh_speech as SP
    import dh_say as SY
    install_speech(); ds.ARM_PHONE[0] = True
    me = sys.modules[__name__]
    HELD.clear(); R_HELD.clear(); del CHECKS[:]
    import set_gate
    set_gate.install(); del set_gate.SEQ[:]
    zc = collections.Counter(); sc = collections.Counter()
    for n in range(int(round(TOTAL * DPS))):
        set_gate.begin(None)
        surf, sid = me.frame(n / float(DPS), n, 1)
        set_gate.SEQ[-1] = (sid, list(set_gate.LOG))
        for f_ in set_gate.faults(sid, moves=SET_MOVES, air=SET_AIR):
            sc[(sid, f_)] += 1
        if sid in INS:                                      # inserts: the v7 drawings, no faces to place
            continue
        seen = []
        for rec in SP.REG:
            try:
                ms = SY.measure(rec); hx, hy = SP._frame_matrix(rec).transform_point(*rec["head_u"])
            except Exception:
                continue
            if any(math.hypot(hx - a, hy - b) < 0.5 * ms["r"] for a, b in seen):
                continue                                    # the same rig logged twice
            seen.append((hx, hy)); r = ms["r"] * 0.8
            if -r < hx < 540 + r and -r < hy < 960 + r:
                for f_ in zone_faults((hx - r, hy - r, hx + r, hy + r), "face"):
                    if f_ in ("at the frame's edge", "under the buttons") and (sid, rec.get("name")) in ENTRANCES and n - int(T0[sid] * DPS) < 2:
                        continue
                    if f_ == "at the frame's edge" and (sid, rec.get("name")) in EXITS:
                        continue                            # an entrance caught mid-step at the edge (G2b), 2 drawings
                    zc[("face %s" % rec.get("name"), sid, f_)] += 1
        for a in _avoid():
            for f_ in zone_faults(a, "sign"):
                zc[("sign", sid, f_)] += 1
    by = collections.OrderedDict()
    for n, text, faults in CHECKS:
        b = by.setdefault(text, [0, 0, collections.Counter()]); b[0] += 1
        if faults:
            b[1] += 1; b[2].update(faults)
    bad = 0
    for text, (nn, nf, cnt) in by.items():
        print("%-30s %3d drawings %3d with faults  %s" % (text, nn, nf, dict(cnt)))
        bad += nf
    print("speech_gate: %d bubble drawings, %d with faults" % (len(CHECKS), bad))
    for (what, sid, f_), v in sorted(zc.items()):
        print("ZONE %-14s %-5s %-22s %d drawings" % (what, sid, f_, v))
    print("dead zones: %d drawings with a face or sign in them" % sum(zc.values()))
    for (sid, f_), v in sorted(sc.items()):
        print("SET %-5s %s  %d drawings" % (sid, f_, v))
    cuts = set_gate.cut_faults(walks=SET_WALKS)
    for f_ in cuts:
        print(f_)
    print("set: %d drawings off the set, %d cuts that move someone" % (sum(sc.values()), len(cuts)))
    return bad + sum(zc.values()) + sum(sc.values()) + len(cuts)


if __name__ == "__main__":
    if "gate" in sys.argv[1:]:
        sys.exit(1 if gate() else 0)
    if "remux" in sys.argv[1:]:                             # new sound only: the pictures are copied
        tmp = "/tmp/dh_s3_%s" % V; sound(tmp + "/a.wav")
        out = "%s/dh_s3_anim_%s.mp4" % (OUT, V)
        subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", out, "-i", tmp + "/a.wav", "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                               "-af", "loudnorm=I=-16:TP=-2:LRA=11,aresample=48000", "-c:a", "aac", "-b:a", "160k", "-t", "%.3f" % TOTAL, out[:-4] + ".tmp.mp4"])
        os.rename(out[:-4] + ".tmp.mp4", out); print("remuxed", out); sys.exit()
    if "nobub" in sys.argv[1:]:
        NOBUB[0] = True
        main(1)
    else:
        install_speech()                                    # the rigs logged for measuring; bubbles by speech.draw
        HELD.clear(); R_HELD.clear(); del CHECKS[:]
        main(1)
        bad = [c_ for c_ in CHECKS if c_[2]]
        print("speech_gate on the render: %d bubble drawings, %d with faults" % (len(CHECKS), len(bad)))
