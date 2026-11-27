"""SUPERSEDED (27 Nov) by the hand library v3 (hand_lib_v3.py). Kept only so the 5.2 silhouette tests it drew
(da_sil_saucer.py cup, cup2) and the library sheets that borrow its cup and colours rebuild. The canon: "An episode
does not get its own hands file"; no new shot calls cup_in_pinch, pinch_pinky or saucer_hold.

The Double Agent (episode 15): the 5.2 hands, the one new row of this film (the-double-agent-hand-jobs-v1.md).
Opt-in: nothing here is called by any other film.

Tomas 27 Nov ("Pinky on the cup"; then the outside audit of the cup sheet, "tobulinam"): the props were laid on the
wrist point, not in a hand built to hold them: the saucer pierced by the wrist, the hand hanging under it like a hook;
the cup's handle hidden behind the pinch; the little finger a sausage stuck on the hand's edge. Here:
  cup(k, ...)            the cup: grey-white china, its top an ellipse, a C handle on the hand's side
  pinch_pinky(c, ...)    the canon pinch (hands_v4._pinch, sheet v2), the little finger out of the hand's own mass,
                         its root under the mass (drawn first), so it grows out of the hand
  cup_in_pinch(k, ...)   the hand at the wrist, turned toward the cup (a wrist bend, max 60 deg), its pinch tip ON the
                         handle; drawn: the cup, the handle, the hand over the handle
  saucer_hold(k, ...)    the saucer ON the hand: palm up, level (whatever the forearm does), the fingertips at the far
                         rim, the saucer over the palm, the thumb over the near rim
Both log their grip for da_hand_gate (kinds "pinch_pinky", "saucer_hold": the new row, pending the canon)."""
import math

import kit
from kit import INK
import hands_ps as hp
import hands_v4 as hv
import of_cast as oc

CHINA = (0.90, 0.91, 0.93)                                     # not the shirt's white: the audit ("white on white")
CHINA_D = (0.74, 0.76, 0.80)
COFFEE = (0.40, 0.24, 0.12)


def pinch_pinky(c, w, skin, arm):
    """hands_v4._pinch with the little finger out: from under the three-finger mass, away from the thumb, a little up."""
    s_ = hv._side(arm); t = 0.20 * w
    hp._cap(c, [(0.40 * w, -s_ * 0.24 * w), (0.52 * w, -s_ * 0.48 * w), (0.60 * w, -s_ * 0.66 * w)], t, skin)  # sideways, not along the index (a V)
    hv._pinch(c, w, skin, arm)


def cup(k, x, y, s, side=1):
    """(x, y): the middle of its bottom; side: +1 the handle on the right. Returns the handle's middle."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    hx = side * 15
    c.set_line_cap(1)
    for col, lw in ((INK, 7.0), (CHINA, 3.6)):                 # the handle, a C
        c.set_source_rgb(*col); c.set_line_width(lw); c.new_path()
        if side > 0:
            c.arc(hx, -12, 6.5, -1.5, 1.5)
        else:
            c.arc_negative(hx, -12, 6.5, -1.64, 1.64)
        c.stroke()
    c.set_line_cap(0)
    kit.cut(k, [(-13, -24), (13, -24), (10, 0), (-10, 0)], CHINA, shadow=False, lw=2)
    c.set_source_rgb(*CHINA_D); c.set_line_width(1.2); c.new_path(); c.move_to(-10, -4); c.line_to(10, -4); c.stroke()
    kit.ellipse(k, 0, -24, 13, 3.6, CHINA_D, 7111, shadow=False, lw=1.6)            # its top, an ellipse
    kit.ellipse(k, 0, -23.4, 9.5, 2.2, COFFEE, 7112, shadow=False, lw=0.8)
    c.restore()
    return x + side * (15 + 6.5) * s, y - 12 * s


def cup_in_pinch(k, wx, wy, d, w, skin, arm, toward, s_cup, max_bend=60.0):
    """the hand at the wrist (wx, wy), the forearm along d; the hand turned toward `toward` (the cup's side, the mouth),
    at most max_bend degrees off the forearm; the pinch tip on the handle; the cup beyond it."""
    c = k.c
    a_f = math.atan2(d[1], d[0])
    a_t = math.atan2(toward[1] - wy, toward[0] - wx)
    diff = (a_t - a_f + math.pi) % (2 * math.pi) - math.pi
    diff = max(-math.radians(max_bend), min(math.radians(max_bend), diff))
    a = a_f + diff
    tip = (wx + 1.02 * w * math.cos(a), wy + 1.02 * w * math.sin(a))
    side = 1 if math.cos(a) < 0 else -1                        # the handle faces the hand
    bx = tip[0] - side * (15 + 6.5) * s_cup
    by = tip[1] + 12 * s_cup
    cup(k, bx, by, s_cup, side)
    oc.log_grip(c, "pinch_pinky", *tip)                        # where it holds: thumb and index on the handle
    arm_eff = arm if math.cos(a) >= 0 else -arm
    c.save(); c.translate(wx, wy); c.rotate(a)
    pinch_pinky(c, w, skin, arm_eff)
    c.restore()
    x0 = min(bx - 14 * s_cup, tip[0]); x1 = max(bx + 14 * s_cup, tip[0])
    return (x0 - 2, by - 26 * s_cup, x1 - x0 + 4, 28 * s_cup)      # the cup and its handle, for the gate


def saucer_hold(k, wx, wy, d, w, skin, out, s_sau):
    """the saucer on a palm-up hand, level; out = -1/+1: the hand reaches screen left/right from the wrist."""
    c = k.c
    hx, hy = wx + out * 0.42 * w, wy + 0.06 * w              # the palm's middle, under the saucer
    oc.log_grip(c, "saucer_hold", hx, hy)
    hp._cap(c, [(wx, wy), (hx, hy)], 0.62 * w, skin)                               # the wrist into the palm
    hp._blob(c, hx, hy, 0.44 * w, 0.20 * w, skin)                                  # the palm, seen from its edge
    sx, sy = hx + out * 0.08 * w, hy - 0.20 * w                # the saucer sits on the palm
    hp._cap(c, [(hx, sy + 6.5 * s_sau), (sx + out * 26 * s_sau, sy + 6.5 * s_sau)], 0.20 * w, skin)   # the fingers along its underside
    kit.ellipse(k, sx, sy, 30 * s_sau, 7 * s_sau, CHINA, 7121, shadow=False, lw=2)
    kit.ellipse(k, sx, sy - 1.2 * s_sau, 14 * s_sau, 3 * s_sau, CHINA_D, 7122, shadow=False, lw=1.2)
    fx = sx + out * 26 * s_sau                                 # their tips curl up round the far rim
    hp._cap(c, [(fx, sy + 6.5 * s_sau), (fx + out * 0.06 * w, sy + 1.5 * s_sau)], 0.20 * w, skin)
    hp._cap(c, [(wx + out * 0.12 * w, wy - 0.04 * w), (sx - out * 16 * s_sau, sy - 3 * s_sau)], 0.22 * w, skin)   # the thumb over the near rim
    return (sx - 30 * s_sau, sy - 8 * s_sau, 60 * s_sau, 16 * s_sau)
