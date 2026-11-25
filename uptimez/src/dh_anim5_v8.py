"""DADDY'S HOME v8, scene 5 "The Filter": v7's scene (dh_anim5.sc, its clock, takes and mix) with v8's bubbles and checks
(dh_anim_v8), and the shots that failed the hands audit and the set gate redrawn:
  - the throne on its set mark (452, was 418 in 7.1a', 7.3, 7.5, 7.7); Don in front of it moves with it
  - 7.1a', 7.2b: Mom and Sofía on two floor lines (they overlapped on one: "one stands behind the other" needs depth)
  - 7.2a, 7.2a': the hand with the brush comes in from the left edge as a hand and a cuff stub (insert_cuff), not a
    sleeve bar ("a tube", rules: inserts)
  - 7.6: the invoice held at its edge by his fingers, drawn first, the hand over it (it hid his hand)
  - 7.8: Pam's mug in her hand (it hung beside it) and her arm below her eyes (it crossed her glasses, lesson 163)
  python3 dh_anim5_v8.py [gate|nobub]  ->  ../daddys-home/dh_s5_anim_v8.mp4"""
import math
import sys
import cairo
import kit
import hands_ps as hp
import dh_props as dp
import dh_scenes as ds
import dh_layout as dl
import dh_anim5 as V7
import dh_anim_v8 as E
import of_scenes as osc
from kit import Ctx, INK

sc = V7.sc
F = V7.F
SET_THR = dl.CH[0]                                          # 452

# ---- the set: the throne on its mark; Don, standing in front of it in v7 at THR5 + 12, with it
V7.THR5 = ds.THR5 = SET_THR
V7.DON5 = ds.DON5 = (SET_THR + 12, F + 26)
# ---- depth: Mom nearer the lens than Sofía (v7: feet F+8 and F+4, overlapping)
V7.MOM5 = ds.MOM5 = (648, F + 22)
V7.SOF5 = ds.SOF5 = (552, F + 2)                          # round 2: further apart ("they look merged")


# ---- 7.2a, 7.2a': the hand and the brush, from the left edge
# Round 3 (whole-film mute test 2/2: "a fist hits the machine", "a fist-bump / a handshake"): v7's brush was 4 cm under the
# fist. Bigger, the orange grip out past the fist (rules: a tool's handle shows), the tuft on the machine's light grey panel
# (on the dark group head it was lost, 2/2). Stills test, 2 viewers: "a fist holding a tool, not a handshake" 2/2.
BRUSH_S = [2.0]
TIP_DX = [56.0]                                             # how far onto the machine's front the tuft goes
TIP_DY = [-24.0]                                            # up off the dark group head onto the grey panel


def brush_hand(k, back, touch):
    hx = V7.MX - 62 * V7.MZ - back
    hy = V7.MY - 92 * V7.MZ
    c = k.c
    bs = BRUSH_S[0]
    bx = hx + 8 + TIP_DX[0] - 27 * bs                       # the tuft's tip on the machine
    hy += TIP_DY[0]
    hand = (bx - 23 * bs, hy + 4 + 5)                       # the fist on the middle of the orange grip
    d = osc.insert_cuff(c, hand, (hand[0] - 200, hand[1] + 30), 26 * 0.62, ds._co.SKIN, V7.dc.SUIT, cuff=(0.97, 0.97, 0.95), stub=120)
    V7.dc.brush(k, bx, hy + 4, bs, 0.0)                     # the brush, then the fingers over it
    hp.draw(k, "grab", hand[0], hand[1], 26, ds._co.SKIN, d, 1)
    if touch:
        ds._lines(k, [(hx + 14, hy - 10, hx + 24, hy - 20), (hx + 18, hy + 4, hx + 30, hy + 4), (hx + 14, hy + 18, hx + 24, hy + 28)])


V7.brush_hand = brush_hand


def r_reach(s, k, o, t, tt, n):                             # 7.2a: the hand comes in, slowly; in the frame from its first drawing
    brush_hand(k, V7.seq(t, [34, 26, 18, 12, 8]), False)   # (v7 64 -> 22: with the bigger brush the hand started off the edge)


sc.DRAW["7.2a"] = r_reach


# ---- 7.1a (round 2, cold test: "the case hangs in the air by his head"): his hand on its handle all the way down
def r_bang(s, k, o, t, tt, n):
    import dh_poses as dq
    i = V7.idx(t)
    x, feet, s_ = 648, V7.VIS[1], V7.GS
    dy = V7.seq(t, [-70, -24, 5, -3, 0])
    cy = F - 216 + dy
    V7.dc.tool_case(k, 716, cy, 0.62)                       # the case, then his hand over its handle
    tx, ty = (700 - x) / s_, (cy + 26 - feet) / s_         # its near end (the handle on top is out of his reach: the arm went straight)
    pose = (-6, 3) + dq.ik(dq.co.SH[0], dq.co.BT + 26, tx, ty, dq.co.LN1, dq.co.LN2, 1)
    hp.reset("relax", "grab")
    V7.dc.repairman(k, x, feet, s_, pose=pose, case=False, look=(1, 0.2)); ds._sticker(k, x, feet)
    if i in (2, 3):
        ds._lines(k, [(716 + math.cos(a_) * 44, F - 196 + math.sin(a_) * 30, 716 + math.cos(a_) * (66 + 8 * (i == 2)), F - 196 + math.sin(a_) * (48 + 6 * (i == 2)))
                      for a_ in (-2.6, -2.1, -1.0, -0.5)])


# ---- 7.6: the invoice, drawn first at his hand; his figure (and fingers) over it
def r_inv(s, k, o, t, tt, n):
    dx = V7.seq(t, [-26, -8, 3, 0])
    bob = -2 if (s.speaking("7.6", tt) and n % 2) else 0
    x = V7.VIS[0] - 70 + dx
    import dh_poses as dq
    pose = (-6, 3) + dq.ik(dq.co.SH[0], dq.co.BT + 26, 150, dq.co.BT + 96, dq.co.LN1, dq.co.LN2, 1)
    scratch = Ctx(cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 4, 4)), 0)
    real = getattr(V7.dc.repairman, "_real", V7.dc.repairman)
    hx, hy = real(scratch, x, V7.VIS[1], V7.GS, pose=pose, case=False)["hands"][1]
    s_ = V7.GS
    with V7.A.About(k.c, V7.VIS[0] - 70, V7.VIS[1], 1.0, 1.0, bob):
        c = k.c
        c.save(); c.translate(hx + 44 * s_, hy - 14 * s_); c.rotate(0.10); c.scale(1.5 * s_, 1.5 * s_)
        kit.rect(k, -32, -44, 64, 88, (0.99, 0.98, 0.94), 3240, lw=2)
        kit.text(k, "INVOICE", 0, -28, 9, INK)
        kit.text(k, "$80", 0, 10, 34, (0.80, 0.12, 0.12))
        c.restore()
        V7.dc.repairman(k, x, V7.VIS[1], s_, pose=pose, case=False, look=(1, 0))
    ds._sticker(k, x, V7.VIS[1] + bob)
    if s.speaking("7.6", tt):
        o["say"] = ("The coffee machine.", V7.vtip(V7.VIS[0] - 70, -1), -1, False, -30, 150)


# ---- 7.8: the mug in her hand, her arm under her eyes
def r_pam(s, k, o, t, tt, n):
    sip = t < 0.22
    pm = ds.pb.pm
    pose = (-8, 0) + (pm.ik(1, 6, pm.HY + 58) if sip else pm.ik(1, 30, pm.BT + 60))    # to the middle of her mouth, tipped (round 2: at her chin side it read "a phone"), then at her chest
    calls = []
    realh = kit.HAND[0]

    def rec(*a):
        calls.append((hp._N[0], a, a[0].c.get_matrix()))
        return realh(*a)
    hp.reset("quiet", "grab")
    kit.HAND[0] = rec
    try:
        q = ds.pb.pam(k, V7.PAM5[0], V7.PAM5[1], V7.PS, pose, "neutral", look=(-0.2, 0.6), glasses="up",
                      mouth=None if sip else s.code("7.8", tt))
    finally:
        kit.HAND[0] = realh
    c = k.c
    n0, a, m = calls[-1]                                   # her screen-right hand: the mug in its coordinates, then the hand again
    c.save(); c.set_matrix(m)
    c.save(); c.translate(a[1], a[2]); c.rotate(-0.9 if sip else 0.0); c.scale(1.3, 1.3); c.translate(-2, -18)
    c.set_source_rgb(*INK); c.set_line_width(5); c.new_path(); c.arc(12, 1, 7.5, -1.3, 1.3); c.stroke()
    c.set_source_rgb(0.36, 0.62, 0.80); c.set_line_width(2.4); c.new_path(); c.arc(12, 1, 7.5, -1.3, 1.3); c.stroke()
    kit.cut(k, [(-10, -12), (10, -12), (9, 12), (-9, 12)], (0.36, 0.62, 0.80), shadow=False, lw=2)
    kit.ellipse(k, 0, -12, 10, 3.2, (0.42, 0.26, 0.14), 3580, shadow=False, lw=1.6)       # coffee in it: hers works
    c.restore()
    hp._N[0] = n0; hp.hand(*a)
    mx, my = m.transform_point(a[1], a[2] - 34)
    c.restore()
    c.save(); c.identity_matrix()
    c.restore()
    c.set_source_rgba(1, 1, 1, 0.85); c.set_line_width(3); c.set_line_cap(1)
    w = math.sin(tt * 5) * 4
    inv = cairo.Matrix(*k.c.get_matrix()); inv.invert()
    sx, sy = inv.transform_point(mx, my)
    for ddx in (-6, 6):
        c.move_to(sx + ddx, sy); c.curve_to(sx + ddx + 6 + w, sy - 10, sx + ddx - 6 - w, sy - 18, sx + ddx + 2, sy - 28); c.stroke()
    if s.speaking("7.8", tt):
        o["say"] = ("Some inspect." if s.since("7.8", tt) < 0.95 else "Others drink.", (q["head"][0] - 44 * V7.PS, q["head"][1] + 30 * V7.PS), -1, False, -10, 170)


sc.DRAW.update({"7.6": r_inv, "7.8": r_pam})   # r_bang (round 2) not used: his hand on the case at head height read "on the phone" 2 of 2, worse than v7's case alone
SET_MOVES = {}
SET_AIR = {("7.1a'", "don"), ("7.1a'", "sofia"), ("7.1a'", "mom")}   # the room's flinch: off the floor on purpose
SET_BEHIND = set()
SET_WALKS = set()
sc.SHIFT.update({"7.3": (34, 0), "7.5": (34, 0), "7.7": (34, 0)})   # the camera follows Don (+34 with the throne): his face out of the app buttons
FLYING = {"7.2a''", "7.2b", "7.3"}                       # the filter leaves by the top, crosses the room, and lands on him from the top (7.3's first drawing)
ENTRANCES = {("7.6", "repairman")}                          # the invoice slides in from the edge


def frame8(tt, n, hi=1):
    return E.frame(sc, tt, n, hi)


if __name__ == "__main__":
    me = sys.modules[__name__]
    if "gate" in sys.argv[1:]:
        sys.exit(1 if E.gate(sc, me, SET_MOVES, SET_AIR, SET_BEHIND, SET_WALKS, entrances=ENTRANCES, flying=FLYING) else 0)
    if "nobub" in sys.argv[1:]:
        E.NOBUB[0] = True
    E.run(sc, me, 5)
