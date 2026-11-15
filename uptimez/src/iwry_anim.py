"""ANIMATION v2 (iwry_anim_v1.py = v1, kept). v2: Don's mouth is drawn after don_v4's "grin" wrapper, so
the grin smile no longer paints over it (shot 1 pun and "Approved." were stuck on the smile).

v1 notes: ANIMATION v1 of "I Will Replace You" (540x960 rough of the release version). Built on the silent storyboard v2
(iwry_sb_v2.py, kept as is): same set, shots, cameras, bubbles and timing. This file adds the acting:

- lip-sync from the real voice takes (iwry_visemes.json from iwry_lips_w2_d2.json): closed lips on m/b/p,
  lip under teeth on f/v, open, wide, round and small-round vowels; Sofía keeps her red lips; the robot's
  screen mouth follows the same openness (smaller on the whisper, wider on the shout);
- blinks for Sofía, Don and Pam; the robot's screen blinks on every face change and now and then;
- eased eye darts (no snaps), Sofía's hair and hoops trailing her eye turns, Don nodding along with
  himself, Don's lean-in with a small overshoot, Sofía's recoil on the shout, the thumbs-up popping in,
  Pam typing in the background.
Render with engine_v.py (540) or engine_hd.py (1080)."""
import json
import math
import os
import anim
import kit
import sofia_v4 as sf
import iwry_common as ic
import iwry_sb_v2 as sb
import iwry_mouths as mo
import don_v4 as dv
from kit import ellipse, INK
from anim import ease, lerp, back_out, clamp

DURATION = sb.DURATION
RAW_T = 0.0
F = 1 / 12                                                   # one drawing of the 12 fps boil
_HERE = os.path.dirname(os.path.abspath(__file__))
VIS = json.load(open(os.path.join(_HERE, "iwry_visemes.json")))
OPEN = mo.OPEN
CUTS = [p[0] for p in sb.PANELS]
SHOTS = [(p[0], p[1], fn) for p, fn in zip(sb.PANELS, (sb.s1, sb.s2, sb.s3, sb.s4, sb.s5, sb.s6, sb.s7, sb.s8,
                                                        sb.s9, sb.s10, sb.s11, sb.s12))]
WHISPER = (20.7, 22.0)
SHOUT = (18.4, 19.9)

BLINKS = {"sof": (1.7, 4.45, 6.9, 9.55, 11.0, 17.05, 21.25),       # + the scripted resigned blink at 24.15
          "don": (1.25, 5.05, 9.7, 16.6, 20.45, 23.0),
          "pam": (10.85,),
          "rob": (6.6, 9.3, 17.3, 21.45)}


def shot_of(t):
    for i, (t0, t1, fn) in enumerate(SHOTS):
        if t0 <= t < t1:
            return i
    return len(SHOTS) - 1


def base(t):
    i = shot_of(t)
    t0, t1, fn = SHOTS[i]
    return fn(t, t - t0)


def same_shot(a, b):
    return shot_of(a) == shot_of(b)


def smooth_look(t, key):
    """Eye darts over two drawings instead of a snap (never across a cut)."""
    w, acc, tot = (0.5, 0.3, 0.2), [0.0, 0.0], 0.0
    for n, wt in enumerate(w):
        tt = t - n * F
        if tt < 0 or not same_shot(tt, t):
            break
        lk = base(tt)[key]
        acc[0] += lk[0] * wt; acc[1] += lk[1] * wt; tot += wt
    return (acc[0] / tot, acc[1] / tot)


def blinking(who, t, n=2):
    return any(0 <= t - b < n * F - 1e-6 for b in BLINKS[who])


def vis(who, t):
    i = int(round(t * 12))
    return VIS[who][i] if 0 <= i < len(VIS[who]) else ""


def state(t):
    s = dict(base(t))
    i = shot_of(t)
    # --- eyes
    for key in ("sof_look", "don_look", "r_look"):
        s[key] = smooth_look(t, key)
    if same_shot(t - 2 * F, t) and t >= 2 * F:
        l0 = smooth_look(t - 2 * F, "sof_look")
        s["sof_lag"] = (s["sof_lag"][0] + (l0[0] - s["sof_look"][0]) * 6.0, s["sof_lag"][1])
    # --- lip-sync
    s["don_mouth"], s["sof_mouth"] = vis("DON", t), vis("SOF", t)
    rc = vis("ROB", t)
    gain = 0.55 if WHISPER[0] <= t < WHISPER[1] else (1.0 if SHOUT[0] <= t < SHOUT[1] else 0.8)
    s["r_talk"] = OPEN[rc] * gain + (0.1 if rc == "M" else 0.0)
    s["don_tilt"] = s["don_tilt"] + 0.02 * OPEN[s["don_mouth"]]          # he nods along with himself
    # --- blinks
    s["sof_blink"] = blinking("sof", t) and s["sof_face"] not in ("horrified", "closed")
    s["don_blink"] = blinking("don", t) and s["don_face"] not in ("shock",)
    if blinking("pam", t):
        s["pam_face"] = "squint"
    prev_face = base(t - F)["r_face"] if t >= F and same_shot(t - F, t) else s["r_face"]
    if (prev_face != s["r_face"] or blinking("rob", t, 1)) and s["r_face"] != "blink":
        s["r_face"] = "blink"
    # --- Pam types
    pa = list(anim.angles("type"))
    if int(t * 10) % 2:
        pa[1] += 7
    else:
        pa[3] -= 7
    s["pam_pose"] = tuple(pa)
    # --- small acting
    if i == 0:                                                   # Don's lean-in lands with a small overshoot
        s["don_x"] = lerp(380, 362, back_out(clamp(t / 0.6), 1.4))
    if i == 8 and t >= 18.4:                                     # Sofía recoils from the shout
        s["sof_dx"] = -8 * min(1.15, back_out(clamp((t - 18.4) / 0.2), 1.6))
    if i == 10 and s["don_thumb"]:                               # thumbs-up pops in
        s["don_thumb_scale"] = max(0.02, back_out(clamp((t - 22.7) / 0.2), 1.8))
    return s


# ------------------------------------------------------------------ face hooks (mouths and lids)
ACT = {}


def _don_face(orig):
    def face_draw(k, x, y, face, look, glasses=False, seed=0):
        orig(k, x, y, face, look, glasses, seed)
        if seed != 530:
            return
        c = k.c
        if ACT.get("don_blink"):
            for sx in (-17, 17):
                ellipse(k, x + sx, y, 12, 12, kit.PEOPLE["DON"]["skin"], seed + sx + 60, shadow=False, outline=False)
                c.set_source_rgb(*INK); c.set_line_width(4); c.set_line_cap(1)
                c.move_to(x + sx - 10, y + 1); c.curve_to(x + sx - 4, y + 4, x + sx + 4, y + 4, x + sx + 10, y + 1)
                c.stroke()
        code = ACT.get("don_mouth", "")
        if code and not ACT.get("in_wrap"):
            mo.mouth(k, x, y + 28, code, kit.PEOPLE["DON"]["skin"], erase=(20, 15), seed=seed)
    return face_draw


def _don_wrap(orig_wrap):
    """don_v4 draws its "grin" smile (and the chin lift) in a wrapper AROUND the face: a mouth drawn inside
    would be painted over by the smile. So the mouth goes on after the wrapper, at the lifted height."""
    def make(orig, chin):
        wrapped = orig_wrap(orig, chin)

        def face_draw(k, x, y, face, look, glasses=False, seed=0):
            ACT["in_wrap"] = True
            try:
                wrapped(k, x, y, face, look, glasses=glasses, seed=seed)
            finally:
                ACT["in_wrap"] = False
            code = ACT.get("don_mouth", "")
            if seed == 530 and code:
                mo.mouth(k, x, y - 7 * chin + 28, code, kit.PEOPLE["DON"]["skin"], erase=(20, 15), seed=seed)
        return face_draw
    return make


def _sof_face(orig):
    def face(k, x, y, kind="neutral", look=(0, 0), seed=0):
        orig(k, x, y, kind, look, seed)
        c = k.c
        if ACT.get("sof_blink"):
            for sx in (-17, 17):
                ellipse(k, x + sx, y, 13, 13, sf.SKIN, seed + sx + 70, shadow=False, outline=False)
                c.set_source_rgb(*INK); c.set_line_width(4); c.set_line_cap(1)
                c.move_to(x + sx - 11, y + 1); c.curve_to(x + sx - 4, y + 5, x + sx + 4, y + 5, x + sx + 11, y + 1)
                c.stroke()
        code = ACT.get("sof_mouth", "")
        if code:
            mo.mouth(k, x, y + 29, code, sf.SKIN, lip_col=sf.RED, inner=(0.45, 0.06, 0.08), erase=(19, 11), seed=seed)
    return face


def panel(n, bubbles):
    cam_n = n + 1

    def fn(k, t, tl):
        st = state(t)
        ACT.clear()
        ACT.update(don_mouth=st["don_mouth"], sof_mouth=st["sof_mouth"], sof_blink=st["sof_blink"],
                   don_blink=st["don_blink"])
        kf, sff, dw = kit.face_draw, sf.face, dv._face_wrap
        kit.face_draw, sf.face, dv._face_wrap = _don_face(kf), _sof_face(sff), _don_wrap(dw)
        try:
            ic.shot(cam_n, lambda t_, tl_: st, bubbles)(k, t, tl)
        finally:
            kit.face_draw, sf.face, dv._face_wrap = kf, sff, dw
    fn.__name__ = f"a{cam_n}"
    return fn


_B = {0: (sb.b1,), 1: (sb.b2,), 2: (sb.b3,), 3: (sb.b4,), 6: (sb.b7,), 7: (sb.b8,), 8: (sb.b9,), 9: (sb.b10,),
      10: (sb.b11,)}
PANELS = [(t0, t1, panel(n, _B.get(n, ()))) for n, (t0, t1, _) in enumerate(SHOTS)]
