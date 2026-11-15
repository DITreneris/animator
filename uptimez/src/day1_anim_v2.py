"""ANIMATED LOOP v2 (day1_anim.py = v1 is kept). v2 changes:
- mouth shapes from the phonemes of each line (day1_visemes.json): closed lips on m/b/p, lip under teeth
  on f/v, open, wide, round and small-round vowels; the robot's screen mouth follows the same openness;
- matched loop frame: after the screen resets, the coffee rewinds back up into the machine, the evening
  light fades back to morning and the camera settles on exactly the framing the film opens on; the film
  now opens on that close-up and pulls back to Sofía before her first press.

v1 notes: ANIMATED LOOP v1 of "How Sofía Survived Day One" (25 s, 540x960 rough). Built on storyboard v3
(day1_sb_v3.py, kept as is): same set, shots, bubbles and timing. This file adds the motion:

- pose-to-pose easing with a small overshoot instead of pose snaps (never across a cut);
- lip-sync for Don, Sofía and the robot from the real voice takes (day1_lips.json, sound_day1_v2.py);
- blinks (Sofía, Pam, robot), eased eye darts, Sofía's hair and hoops trailing her head turns;
- Pam types, Don nods on his own words, a slow 2.5 % push-in on every static shot;
- the loop: after the overflow the coffee maker's screen flips back to WAITING FOR APPROVAL and the
  tap closes, so the last second hands over to the 9:00 opening.
"""
import functools
import json
import math
import os
import cairo
import kit
import anim
import sofia as sf
import pt42
import day1_kit as dk
import day1_sb_v3 as sb
from kit import rect, ellipse, INK
from anim import clamp, ease, lerp, back_out

DURATION = sb.DURATION
RAW_T = 0.0
F = 1 / 30
CUTS = [s[0] for s in sb.SHOTS]
_HERE = os.path.dirname(os.path.abspath(__file__))
LIPS = json.load(open(os.path.join(_HERE, "day1_lips.json")))
VIS = json.load(open(os.path.join(_HERE, "day1_visemes.json")))
OPEN = {"": 0.0, "M": 0.0, "F": 0.25, "C": 0.4, "U": 0.45, "E": 0.55, "O": 0.75, "A": 1.0}
CU = (sb.CM_X, 690, 3.0)                                   # the loop frame: coffee maker close-up
OPEN_CAM = (190, 720, 1.9)                                 # the opening medium on Sofía
RESET = 24.5                                               # coffee maker screen flips back: the loop point gag

BLINKS = {"sof": (1.0, 4.3, 7.15, 11.95, 13.7, 16.3, 19.95, 21.55, 24.0),
          "pam": (9.3, 18.42, 19.2),                       # 18.42: one slow blink into the camera
          "rob": (4.8, 7.3, 10.95, 13.9, 16.45, 21.95)}


@functools.lru_cache(maxsize=4096)
def _base(fi):
    return sb.state(fi * F)


def base(t):
    return _base(int(round(t / F)))


def same_shot(t_a, t_b):
    return not any(t_a < c <= t_b for c in CUTS)


def eased(t, get, dur, overshoot=False):
    """Value of get(state) at t, blended from its previous value for `dur` seconds after it changes.
    Tuples of numbers only. A change that happens on a cut is not eased."""
    cur = get(base(t))
    n = int(round(dur / F))
    for i in range(1, n + 1):
        prev = get(base(t - i * F))
        if prev != cur:
            tc = t - (i - 1) * F                           # first frame of the new value
            if not same_shot(tc - F, tc) or not same_shot(tc, t):
                return cur
            u = clamp((t - tc + F) / dur)
            e = back_out(u, 1.4) if overshoot else ease(u)
            return tuple(lerp(a, b, e) for a, b in zip(prev, cur))
    return cur


def blinking(who, t, frames=5):       # 5 frames = two drawings of the 12 fps boil
    return any(0 <= t - b < frames * F for b in BLINKS[who])


def lip(who, t):
    """Mouth openness 0..1 from the voice take: held for 2 frames, in 3 steps, like the 12 fps boil."""
    f = int(round(t / F)) // 2 * 2
    v = max(LIPS[who][min(f, len(LIPS[who]) - 1)], LIPS[who][min(f + 1, len(LIPS[who]) - 1)])
    return 0.0 if v < 0.12 else (0.4 if v < 0.4 else (0.7 if v < 0.75 else 1.0))


def vis(who, t):
    i = int(round(t * 12))
    return VIS[who][i] if 0 <= i < len(VIS[who]) else ""


def sof_angles(p):
    return tuple(sf.POSES.get(p) or kit.ARM_POSES[p])


def state(t):
    s = dict(base(t))
    # --- eased poses
    s["don_pose"] = anim.key(eased(t, lambda b: tuple(anim.angles(b["don_pose"])), 0.22, True))
    pam_named = s["pam_pose"]
    pa = eased(t, lambda b: tuple(anim.angles(b["pam_pose"])), 0.22, True)
    if pam_named == "type" and pa == tuple(anim.angles("type")):       # typing: forearms tap alternately
        k_ = int(t * 10) % 2
        pa = (pa[0], pa[1] + (7 if k_ else 0), pa[2], pa[3] - (0 if k_ else 7))
    s["pam_pose"] = anim.key(pa)
    s["sof_named"] = s["sof_pose"]
    s["sof_pose"] = anim.key(eased(t, lambda b: sof_angles(b["sof_pose"]), 0.22, True))
    dk.ROBOT_POSES["_anim"] = eased(t, lambda b: tuple(dk.ROBOT_POSES[b["rob_pose"]]), 0.25, True)
    s["rob_pose"] = "_anim"
    # --- eased eyes and tilts
    for key in ("sof_look", "pam_look", "rob_look"):
        s[key] = eased(t, lambda b, key=key: tuple(b[key]), 0.13)
    s["rob_tilt"] = eased(t, lambda b: (b["rob_tilt"],), 0.2, True)[0]
    # hair and hoops trail her eye/head turns for a few frames
    l0 = eased(t - 3 * F, lambda b: tuple(b["sof_look"]), 0.13) if same_shot(t - 3 * F, t) else s["sof_look"]
    s["sof_lag"] = ((l0[0] - s["sof_look"][0]) * 5.0, 0)
    # --- lip-sync, blinks, small acting
    s["don_mouth"], s["sof_mouth"] = vis("DON", t), vis("SOF", t)
    s["rob_talk"] = OPEN[vis("ROB", t)] + (0.12 if vis("ROB", t) == "M" else 0)    # a thin line on closed lips
    s["don_tilt"] = s["don_tilt"] + 0.022 * OPEN[s["don_mouth"]]              # he nods along with himself
    s["sof_blink"] = blinking("sof", t)
    if blinking("pam", t, 8 if 18.3 < t < 18.8 else 5):
        s["pam_face"] = "squint"
    if blinking("rob", t):
        s["rob_eyes"] = "flat"
    # --- loop ending: overflow a little earlier, then the screen resets and the tap closes
    s["stream"] = True
    if t >= 23.25:
        s["overflow"] = clamp((t - 24.0) / 0.45)
    if t >= RESET:                                        # screen resets, then the coffee rewinds into the machine
        r = ease(clamp((t - RESET - 0.05) / 0.3))
        s.update(cm="waiting", pour=1 - r, overflow=1 - ease(clamp((t - RESET) / 0.25)), stream=0.02 < 1 - r and r > 0)
    return s


# ------------------------------------------------------------------ face overlays (mouths, lids)
ACT = {}


def mouth(k, x, my, code, lip_col=None, inner=(0.40, 0.07, 0.08), skin=(1, 1, 1), seed=0):
    """One mouth shape at (x, my). lip_col: Sofía's red lip ring (None = ink outline only)."""
    c = k.c
    ellipse(k, x + 1, my - 2, 19, 11, skin, seed + 90, shadow=False, outline=False)     # clear the face's mouth
    col = lip_col or INK
    if code == "M":                                        # pressed lips, a touch puffed
        if lip_col:
            ellipse(k, x, my, 11, 4.2, lip_col, seed + 91, shadow=False, outline=False)
        c.set_source_rgb(*INK); c.set_line_width(3.2 if not lip_col else 1.8)
        c.move_to(x - 10, my); c.curve_to(x - 4, my + 1.5, x + 4, my + 1.5, x + 10, my); c.stroke()
        return
    w, h = {"A": (9, 11), "E": (12, 5.5), "O": (7.5, 8.5), "U": (4.8, 5.5), "F": (10, 4), "C": (9, 5.5)}[code]
    c.save(); c.translate(x, my); c.scale(w, h); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    c.set_source_rgb(*inner); c.fill_preserve()
    c.set_source_rgb(*col); c.set_line_width(3.2 if lip_col else 2.2); c.stroke()
    if code in ("E", "F", "C"):                            # upper teeth
        c.save(); c.translate(x, my); c.scale(w, h); c.arc(0, 0, 0.82, math.pi, 2 * math.pi); c.restore()
        c.save(); c.clip()
        c.set_source_rgb(1, 1, 1); c.rectangle(x - w, my - h, 2 * w, h * (0.75 if code == "F" else 0.5)); c.fill()
        c.restore()
    if code == "F":                                        # lower lip tucked up under the teeth
        c.set_source_rgb(*col); c.set_line_width(3 if lip_col else 2.4)
        c.move_to(x - w + 2, my + 1); c.curve_to(x - 3, my - 2, x + 3, my - 2, x + w - 2, my + 1); c.stroke()
    if code in ("A", "O"):                                 # tongue
        c.save(); c.translate(x, my + h * 0.55); c.scale(w * 0.55, h * 0.3); c.arc(0, 0, 1, math.pi, 2 * math.pi); c.restore()
        c.set_source_rgb(0.80, 0.33, 0.35); c.fill()


def _don_face(orig):
    def face_draw(k, x, y, face, look, glasses=False, seed=0):
        orig(k, x, y, face, look, glasses=glasses, seed=seed)
        code = ACT.get("don_mouth", "")
        if seed == 530 and code:                           # Don (person seed 500 + 30)
            mouth(k, x, y + 28, code, skin=kit.PEOPLE["DON"]["skin"], seed=seed)
    return face_draw


def _sof_face(orig):
    def face(k, x, y, kind="neutral", look=(0, 0), seed=0):
        orig(k, x, y, kind, look, seed)
        c = k.c
        if ACT.get("sof_blink") and kind not in ("knowing", "flirty"):
            for sx in (-17, 17):
                if kind == "wink" and sx > 0:
                    continue
                ellipse(k, x + sx, y, 12.5, 12.5, sf.SKIN, seed + sx + 70, shadow=False, outline=False)
                c.set_source_rgb(*INK); c.set_line_width(3.5)
                c.arc(x + sx, y - 3, 10, 0.15 * math.pi, 0.85 * math.pi); c.stroke()
        code = ACT.get("sof_mouth", "")
        if code:
            mouth(k, x, y + 29, code, lip_col=sf.RED, inner=(0.45, 0.06, 0.08), skin=sf.SKIN, seed=seed)
    return face


def world(k, st):
    kit.BADGE_HOOK = sb.person_badge
    sf.BADGE_HOOK = (lambda k_, bt, seed: sb.day1_sticker(k_, 2, bt + 30)) if st["sof_badge"] == "day1" else \
        (lambda k_, bt, seed: sb.staff_badge(k_, "SOFÍA", 3, bt + 32, 39, 10))
    kf, sff = kit.face_draw, sf.face
    kit.face_draw, sf.face = _don_face(kf), _sof_face(sff)
    ACT.update(don_mouth=st["don_mouth"], sof_mouth=st["sof_mouth"], sof_blink=st["sof_blink"])
    try:
        return _world(k, st)
    finally:
        kit.BADGE_HOOK = None
        sf.BADGE_HOOK = None
        kit.face_draw, sf.face = kf, sff


def _world(k, st):
    """Same set and draw order as storyboard v3; differences: Sofía's folder follows her named pose,
    her hair lag, and the coffee maker's tap can close."""
    c = k.c
    PAM, ROB, DON, DESK_TOP = sb.PAM, sb.ROB, sb.DON, sb.DESK_TOP
    rect(k, -400, -400, 1600, 1060, kit.WALL, 100, shadow=False, outline=False)
    rect(k, -400, 660, 1600, 900, kit.FLOOR, 101, shadow=False)
    rect(k, -400, 650, 1600, 16, (0.62, 0.5, 0.36), 102, shadow=False, lw=2)
    pt42.wall_sign(k, 470, 380, 30)
    px, pf = st["pam"]
    if px == PAM[0]:
        pt42._orig_person(k, "PAM", px, pf, 1.0, pose=st["pam_pose"], face=st["pam_face"], look=st["pam_look"], seed=44)
        kit.desk(k, 640, DESK_TOP, 170, 731)
        rect(k, 646, DESK_TOP + 24, 158, 106, (0.55, 0.40, 0.28), 732)
        dk.thermos(k, 676, DESK_TOP + 2)
    else:
        kit.desk(k, 640, DESK_TOP, 170, 731)
        rect(k, 646, DESK_TOP + 24, 158, 106, (0.55, 0.40, 0.28), 732)
    tx, ty, trx, tryy = sb.TRACK
    if st["part"] > 0.5:
        dk.railway(k, tx, ty, trx, tryy, front=False)
    rbx, rbf = st["rob"]
    rob = None
    if st["don_x"] != DON[0]:
        sb.shadow(k, st["don_x"], DON[1] + 2, 50, 9)
    robot = lambda: dk.robot(k, rbx, rbf, 1.0, st["rob_pose"], st["rob_eyes"], look=st["rob_look"], tilt=st["rob_tilt"],
                             talk=st["rob_talk"], paper=st["rob_paper"], badge="DON 2.0")
    if rbf == ROB[1]:
        rob = robot()
    c.save()
    dx = st["don_x"]
    c.translate(dx, DON[1]); c.rotate(st["don_tilt"]); c.translate(-dx, -DON[1])
    don = pt42._orig_person(k, "DON", dx, DON[1], 1.0, pose=st["don_pose"], face=st["don_face"],
                            look=st["don_look"], seed=500)
    c.restore()
    kit.desk(k, 320, DESK_TOP, 200, 501)
    rect(k, 326, DESK_TOP + 24, 188, 116, (0.55, 0.40, 0.28), 502)
    if rbf != ROB[1]:
        sb.shadow(k, rbx, rbf + 2, 56, 10)
        rob = robot()
    btn = None
    if st["part"] > 0.5:
        dk.railway(k, tx, ty, trx, tryy, front=True)
        if st["train"] is not None:
            btn = dk.train(k, tx, ty, trx, tryy, st["train"], button_y=DESK_TOP - 16, pressed=st["pressed"], plaque=True)
    if st["don_press"]:
        p = kit.PEOPLE["DON"]
        body_top = DON[1] - 300 * p["h"] + 78
        kit.arm(k, st["don_x"] - 40, body_top + 14, sb.DON_PRESS_ARM[0], sb.DON_PRESS_ARM[1], p["body"], p["skin"], 509)
    if st["part"] < 1:
        off = 520 * ease(st["part"])
        dk.partition(k, 315 + off, 640 + off, 640, 860)
    dk.counter(k, -60, 200, sb.COUNTER)
    dk.coffee_maker(k, sb.CM_X, sb.COUNTER, 1.0, st["cm"], pour=st["pour"], overflow=st["overflow"],
                    sticker_at=sb.STICKER_V2, stream=st["stream"])
    if px != PAM[0]:
        sb.shadow(k, px, pf + 2)
        pam = pt42._orig_person(k, "PAM", px, pf, 1.0, pose=st["pam_pose"], face=st["pam_face"], look=st["pam_look"], seed=44)
        hx, hy = pam["hands"][1]
        dk.thermos(k, hx + 6, hy + 30)
    sx, sfeet = st["sof"]
    sb.shadow(k, sx, sfeet + 2, 44, 9)
    named = st["sof_named"]
    folder = "tuck" if not st["sof_mug"] and named in ("stand", "tuck") and sx != sb.SOF_A[0] else \
        ("offer" if named == "offer" else "none")
    sof = sf.sofia(k, sx, sfeet, 1.0, st["sof_pose"], st["sof_face"], look=st["sof_look"], lag=st["sof_lag"], seed=7,
                   folder=folder)
    if st["sof_mug"]:
        hx, hy = sof["hands"][1]
        dk.mug(k, hx + 4, hy + 8, 1.0, steam=1.0)
    return {"don": don, "rob": rob, "sof": sof, "btn": btn}


def make_shot(t0, t1, cam, bubbles, ding_at):
    def fn(k, t, tl):
        st = state(t)
        if t0 == 0.0:                                      # opens on the loop frame, pulls back to Sofía
            v = ease(clamp(t / 0.3))
            cm = tuple(lerp(a, b, v) for a, b in zip(CU, OPEN_CAM))
        elif t0 == sb.SHOTS[-1][0]:                        # push in, then settle back on the exact loop frame
            z = 1 + 0.025 * clamp((t - t0) / (RESET - t0)) * (1 - ease(clamp((t - RESET) / 0.35)))
            cm = (CU[0], CU[1], CU[2] * z)
        else:
            cm = cam(t) if callable(cam) else (cam[0], cam[1], cam[2] * (1 + 0.025 * (t - t0) / (t1 - t0)))   # slow push-in
        c = k.c
        c.save()
        c.translate(270, 480); c.scale(cm[2], cm[2]); c.translate(-cm[0], -cm[1])
        out = world(k, st)
        c.restore()
        look(k, t)
        for b0, b1, s, who, side in bubbles:
            if b0 <= t < b1:
                sm = sb.to_screen(sb.anchor(who, side, st, out), cm)
                if side in ("left", "right") and who != "rob":
                    sm = (sm[0] + (58 if side == "right" else -58) * cm[2], sm[1])
                sb.bubble(k, s, sm, side, t=t, t0=b0)
        if out["btn"] is not None and t1 > sb.DINGS[0] and t0 < sb.DINGS[-1] + 0.6:
            bs = sb.to_screen(out["btn"], cm)
            dx_, dy_ = ding_at if ding_at else (min(bs[0] + 70, 430), bs[1] + 60)
            sb.ding(k, t, dx_, dy_, btn=bs, z=cm[2] / 2.0)
        elif 23.2 <= t < RESET:
            sb.ding(k, t, 300, 330)
        sb.clock_card(k, t)
    fn.__name__ = f"shot_{t0:04.1f}"
    return fn


def look(k, t):
    """Storyboard v3's grade, but the evening light fades back to morning after the reset (the loop)."""
    c = k.c
    w = 1.0 if 20.2 <= t < RESET else (1 - ease(clamp((t - RESET - 0.05) / 0.3)) if t >= RESET else 0.0)
    if w > 0:
        c.save(); c.set_operator(cairo.OPERATOR_MULTIPLY)
        c.set_source_rgb(1.0 - 0.0 * w, 1 - 0.07 * w, 1 - 0.17 * w); c.paint(); c.restore()
    g = cairo.RadialGradient(270, 470, 300, 270, 470, 640)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.15, 0.08, 0.02, 0.14)
    c.set_source(g); c.paint()


PANELS = [(t0, t1, make_shot(t0, t1, cam, b, d)) for t0, t1, cam, b, d in sb.SHOTS]


def shake(t):
    return 0

