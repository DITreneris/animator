"""DADDY'S HOME v8, scene 8 "Find My Money": v7's scene (dh_anim8.sc: clock, takes, mix) through dh_anim_v8 (v8 bubbles,
dead zones, set_gate), on the set as scene 7 v8 left it (dh_anim7_v8: the throne on its mark, Father at 376, Don's hand up,
palm open), with the shots that failed redrawn:
  - Father's lines (10.2, 10.4a, 10.4a', 11.1): the two-shot of 9.4' (v7: Father close, Don's raised arm in the edge of the
    frame behind the price tag, his body cut: "an arm without a body, holding the tag", hands audit #6)
  - 9.6, 9.6' (the CV): Sofía holds her own CV up; then the bodyguard has it and her hands are down (v7: her arm straight out
    to his hand on the CV, "a handshake", hands audit; rules, Gestures: two people's hands near = a handshake)
  python3 dh_anim8_v8.py [gate|nobub]  ->  ../daddys-home/dh_s8_anim_v8.mp4"""
import sys
import math
import kit
import dh_layout as dl
import dh_scenes as ds
import dh_cast as dc
import dh_anim7_v8 as A7                                    # the set and Don's raised hand, as scene 7 v8 left them
import dh_anim6_v8 as A6                                    # sofia_with_cv: her CV in her hand (scene 6 v8)
import dh_anim8 as V8
import dh_anim_v8 as E
import dh_anim3_v8 as A3

sc = V8.sc
F, CH, DS_ = V8.F, V8.CH, V8.DS_
N = [0]

# ---- the set: what scene 8 reads at import time, recomputed on the marks
ds.ARM8 = (ds.THR5 + 66, 705)
ds.POV8 = V8.POV8 = (ds.THR5 + 10, 694, 2.15)
V8.TK = (ds.THR5 - 52 * CH[2], CH[1] - 404 * CH[2])
V8.TAG_BOX = (V8.TK[0] - 46 * CH[2] - 7, V8.TK[1] + 30 * CH[2] - 7, 92 * CH[2] + 14, 54 * CH[2] + 14)
V8.FA2 = ds.FA2
V8.HDF = dl.hd(ds.FA2[0], ds.FA2[1], ds.FS)
sc.CARD = {"I prefer green in cash.": "FATHER"}             # 10.1: his line over the star screen (dh_anim_v8 named it DON)
FCAM = (A7.CAM2[0], A7.CAM2[1] + 22, A7.CAM2[2])            # the two-shot of 9.4', a step down: the banner over the throne out
sc.CAM8 = {sid: FCAM for sid in ("10.2", "10.4a", "10.4a'", "11.1")}   # Father's lines in the two-shot: Don whole
for sid_ in ("10.2", "10.4a", "10.4a'", "11.1", "11.6"):     # the heads on the marks; the portrait pushed out of the top
    sc.shot[sid_] = dict(sc.shot[sid_], heads=[dl.hd(ds.FA2[0], ds.FA2[1], ds.FS), ds.HD6], ymin=150)
sc.CAM8.update({sid: ds.POV8 for sid in ("10.5b", "10.6b", "10.6d")})
sc.CAM8["10.3"] = (ds.DON6[0] + 10, 640, 2.6)               # Don close: his raised hand in the frame with him
sc.CAM8["11.2"] = sc.CAM8["10.3"]
sc.CAM8["11.3"] = (ds.LINE6[2][0] + 34, 668, 2.9)
sc.CAM8["11.4"] = (ds.LINE6[1][0] + 8, 620, 4.0)             # closer: her sign whole and big, the shredder's SHRED out of the frame (v7: "SHRE" behind her leg)
sc.CAM8["11.6"] = (A7.CAM2[0] + 6, 690, 1.9)                # Father's phone and Don's, both whole


# ---- Don's hand. v7's _thumb_don: the rectangle thumb and "(( ))" marks ("a phone" 2/2 in scene 7). v8 round 1: scene 7's
# raised palm held through scene 8 read "a wave or an oath, not an action" and "a pole" 2/2. Round 2 (Tomas: "lowers it slowly
# in 10.2"): over Father's first line the hand comes down; then his hands are at his sides.
LOWER = [0.0]
DOWN = (-8, 0, 8, 0)


def _thumb_don(k, face="neutral", look=(-1, 0.5), sink=9, shake=True):
    u = LOWER[0]
    up = A7.THUMB[(-146, -34, 4, 0)]
    keep = dict(A7.THUMB), list(A7.GEST)
    if u > 0:                                               # down by the arm's own angles, the elbow unbending last
        p = [a + (b - a) * u for a, b in zip(up, DOWN)]
        p[3] += 60 * math.sin(math.pi * u)                  # the elbow stays bent on the way down: never a straight arm out
        A7.THUMB[(-146, -34, 4, 0)] = tuple(p)
    if u >= 1:
        A7.GEST[:] = ["relax", "relax"]
    try:
        return A7.thumb_don(k, N[0], False, shake and u == 0, face, look, sink)
    finally:
        A7.THUMB.clear(); A7.THUMB.update(keep[0]); A7.GEST[:] = keep[1]


ds._thumb_don = _thumb_don


# ---- 9.6, 9.6': the CV. v7: her arm straight out to his hand on it ("a handshake"); v8 round 1: she held it at her far side and
# it was in his pocket on the cut ("it jumps, I never see it change hands" 2/2). Round 2 (Tomas: "he takes it from the top"):
# she holds it up on his side; his hand comes to its top edge and draws it away, her fingers still on its lower edge.
import cairo
import math


def _sofia_hand(x, face, look):
    scratch = kit.Ctx(cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 4, 4)), 0)
    real = getattr(ds.sdh.sofia, "_real", ds.sdh.sofia)
    return real(scratch, x, ds.SOF6[1], ds.SS, "hold", face, look=look, tablet_kind="none")["hands"][1]


CV_S = 0.85                                                 # big enough to read as a sheet between two hands (v7 0.62)
SKIN_S = (0.84, 0.66, 0.52)


def _cv_held(k, hx, hy, u, face):
    """Sofía, then the CV in front of her (its centre over her near hand, raised), her fingers on its lower edge.
    u 0..1: drawn away toward him by its top edge. Returns the CV's top-edge grip point."""
    cx, cy = hx + 12 + 30 * u, hy - 26 - 10 * u
    ds.sdh.sofia(k, ds.SOF6[0], ds.SOF6[1], ds.SS, "hold", face, look=(1, -0.2), tablet_kind="none")
    ds.sdh.cv(k, cx, cy, CV_S, 0.06 - 0.06 * u)
    if u < 0.7:
        kit.ellipse(k, cx - 4 - 30 * u, cy + 30, 6, 7, SKIN_S, 3120, shadow=False, lw=1.6)   # hers, on its lower edge
    return cx + 6, cy - 30


def _guard_to(k, wx, wy):
    """The second bodyguard, his screen-left hand at (wx, wy) by IK in his body units (world = post + local * GS)."""
    co = dc.co
    tx, ty = (wx - ds.GU7[0]) / ds.GS, (wy - ds.GU7[1]) / ds.GS
    sx, sy = -co.SH[0], co.SH[1]
    d = math.hypot(tx - sx, ty - sy); m = 0.98 * (co.LN1 + co.LN2)
    if d > m:                                               # keep it in reach: never a straight arm (179)
        tx, ty = sx + (tx - sx) * m / d, sy + (ty - sy) * m / d
    pose = dc.ik(sx, co.BT + 26, tx, ty, co.LN1, co.LN2, -1) + (5, -2)
    return dc.guard(k, ds.GU7[0], ds.GU7[1], ds.GS, pose=pose)


def r_cv(s, k, o, t, tt, n):                                # 9.6: she is on him, her CV held up on his side
    dx = V8.seq(t, [10, 3, 0])
    dc.guard(k, ds.GU7[0], ds.GU7[1], ds.GS, flip=True)
    c = k.c
    c.save(); c.translate(dx, 0)
    hx, hy = _sofia_hand(ds.SOF6[0], "interested", (1, -0.2))
    _cv_held(k, hx, hy, 0.0, "interested")
    c.restore()
    if dx:
        ds._lines(k, [(ds.SOF6[0] + dx - 40, F - 6, ds.SOF6[0] + dx - 56, F - 6)])


def r_cv2(s, k, o, t, tt, n):
    if t < 0.25:                                            # his hand to its top edge, then drawing it away from her
        u = V8.seq(t, [0.0, 0.5, 1.0])
        hx, hy = _sofia_hand(ds.SOF6[0], "interested", (1, -0.2))
        gx, gy = hx + 18 + 30 * u, hy - 56 - 10 * u        # its top edge, where his fingers go
        _guard_to(k, gx, gy)
        _cv_held(k, hx, hy, u, "interested" if u < 1 else "tight")
        kit.ellipse(k, gx, gy, 9, 8, ds._co.SKIN, 3700, shadow=False, lw=2.2)   # his fingers, over its top edge
        return
    co = dc.co
    pose = dc.ik(-co.SH[0], co.BT + 26, -30, co.BT + 52, co.LN1, co.LN2, -1) + (5, -2)
    g = dc.guard(k, ds.GU7[0], ds.GU7[1], ds.GS, pose=pose)
    px, py = min(g["hands"], key=lambda h: h[1])
    ds.sdh.cv(k, px + 2, py - 4, 0.6, 0.0)
    kit.cut(k, [(px - 19, py + 10), (px + 23, py + 10), (px + 21, py + 34), (px - 17, py + 34)], dc.SUIT, shadow=False, lw=2)
    k.c.set_source_rgb(0.85, 0.85, 0.88); k.c.set_line_width(1.8); k.c.move_to(px - 18, py + 11); k.c.line_to(px + 22, py + 11); k.c.stroke()
    kit.ellipse(k, px - 12, py - 2, 11, 10, ds._co.SKIN, 3700, shadow=False, lw=2.2)
    ds.sdh.sofia(k, ds.SOF6[0], ds.SOF6[1], ds.SS, "stand", "tight", look=(1, 0))


sc.DRAW.update({"9.6": r_cv, "9.6'": r_cv2})

SET_MOVES, SET_BEHIND = {}, set()
SET_AIR = {("10.4b", "sofia")}                             # the snap startles her off the floor (v7: "Sofía leaves the floor")
SET_WALKS = set()
ENTRANCES = set()


def frame8(tt, n, hi=1):
    N[0] = n
    t2 = tt - sc.T0["10.2"]
    LOWER[0] = 0.0 if t2 < 0.4 else min(1.0, V8.A.ease(min(1.0, (t2 - 0.4) / 1.4)))   # 1.4 s down, from 0.4 s into his line
    A3.AVOID_EXTRA[:] = []
    for line in ("You said it finds anything.", "Good.", "Find. My money.", "Answer it."):
        if line not in A3.HELD:                             # Father's lines: the box on his left, clear of Don (as 9.4')
            A3.HELD[line] = (None, -1)
    return E.frame(sc, tt, n, hi)


if __name__ == "__main__":
    me = sys.modules[__name__]
    if "gate" in sys.argv[1:]:
        sys.exit(1 if E.gate(sc, me, SET_MOVES, SET_AIR, SET_BEHIND, SET_WALKS, entrances=ENTRANCES) else 0)
    if "nobub" in sys.argv[1:]:
        E.NOBUB[0] = True
    E.run(sc, me, 8)
