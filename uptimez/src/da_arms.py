"""The Double Agent (episode 15): kit.arm tapered, opt-in (Tomas 26 Nov, /grill-me: "fix it in the episode, opt-in").
The hands canon (rules-hands, "The arm"): the wrist is narrower than the forearm, the upper arm wider, the elbow a real
joint; equal widths read as a rubber tube. kit.arm draws both segments at one width (17), for Don, Father and every
kit.person. This module patches kit.arm from the episode (the canon: a shared rig is patched from the episode), so
kit.py and every shipped film stay as they are.
  with da_arms.tapered():  ...draw Don / Father...
Upper arm: w + 3 at the shoulder to w + 1 at the elbow; forearm: w at the elbow to w - 4 at the wrist; a round elbow
cap of the upper arm's width. Everything else (the rim, the hand hook, the return value) is kit.arm's."""
import contextlib
import math
import kit
from kit import cut


def _arm(k, sx, sy, a1, a2, col, skin, seed, ln=48, w=17):
    c = k.c
    d = lambda a: (math.sin(math.radians(a)), math.cos(math.radians(a)))
    ex, ey = sx + d(a1)[0] * ln, sy + d(a1)[1] * ln
    hx, hy = ex + d(a1 + a2)[0] * ln, ey + d(a1 + a2)[1] * ln
    for (ax, ay, bx, by), (wa, wb) in (((sx, sy, ex, ey), (w + 3, w + 1)), ((ex, ey, hx, hy), (w, w - 4))):
        ang = math.atan2(by - ay, bx - ax)
        n = (-math.sin(ang), math.cos(ang))
        pts = [(ax + n[0] * wa / 2, ay + n[1] * wa / 2), (bx + n[0] * wb / 2, by + n[1] * wb / 2),
               (bx - n[0] * wb / 2, by - n[1] * wb / 2), (ax - n[0] * wa / 2, ay - n[1] * wa / 2)]
        cut(k, pts, col, shadow=False, lw=2)
        if kit.ARM_RIM[0] and sum(col) < 0.6:
            c.new_path(); c.move_to(*pts[0]); c.line_to(*pts[1]); c.move_to(*pts[2]); c.line_to(*pts[3])
            c.set_source_rgb(*kit.ARM_RIM[0]); c.set_line_width(2.2); c.stroke()
    c.new_path(); c.arc(ex, ey, (w + 1) / 2 - 0.5, 0, 2 * math.pi); c.set_source_rgb(*col); c.fill()   # the elbow, round
    if kit.HAND[0]:
        kit.HAND[0](k, hx, hy, w * 1.15, skin, seed, d(a1 + a2), 1 if a2 >= 0 else -1)
    else:
        kit.ellipse(k, hx, hy, w * 0.6, w * 0.6, skin, seed, shadow=False, lw=2)
    return hx, hy


@contextlib.contextmanager
def tapered():
    orig = kit.arm
    kit.arm = _arm
    try:
        yield
    finally:
        kit.arm = orig


@contextlib.contextmanager
def inward_thumbs():
    """Opt-in (Tomas 26 Nov: "two left hands on Pam?"). hands_ps and hands_v4 put the thumb on side arm * sign(cos a) of
    the forearm (a: its angle on screen). For an arm hanging down, the two forearms lean to opposite sides of vertical,
    cos a changes sign between them, and both thumbs land on the same screen side: two left hands. For a forearm closer
    to vertical than to level this puts each thumb toward the body (front view, palms to the thighs): the arm passed on
    becomes arm * sign(sin a) * sign(cos a). Level forearms keep the old rule. Wraps hands_ps.draw (after
    hands_v4.enable(), so it wraps the sheet's rows too)."""
    import hands_ps as hp
    orig = hp.draw

    def draw(k, g, hx, hy, w, skin, d, arm):
        a = math.atan2(d[1], d[0])
        sn, cs = math.sin(a), math.cos(a)
        if abs(sn) > abs(cs) and abs(cs) > 1e-6:
            arm = arm * (1 if sn > 0 else -1) * (1 if cs > 0 else -1)
        return orig(k, g, hx, hy, w, skin, d, arm)
    hp.draw = draw
    try:
        yield
    finally:
        hp.draw = orig


_SET = [False]


def _fix(arm, d):
    a = math.atan2(d[1], d[0])
    sn, cs = math.sin(a), math.cos(a)
    if abs(sn) > abs(cs) and abs(cs) > 1e-6:
        return arm * (1 if sn > 0 else -1) * (1 if cs > 0 else -1)
    return arm


def setup():
    """inward_thumbs for the whole process (episode 15's sheets and frames): wraps hands_ps.draw before any
    hands_v4.enable() stores it, and hands_v4.draw's own rows (grab, pinch, fist), once each, so no hand is adjusted
    twice. Call it at the top of an episode 15 drawing script; every older script is untouched."""
    if _SET[0]:
        return
    import hands_ps as hp
    import hands_v4 as hv
    assert not hv._ORIG, "da_arms.setup() must run before hands_v4.enable()"
    o_hp, o_hv = hp.draw, hv.draw
    hp.draw = lambda k, g, hx, hy, w, skin, d, arm: o_hp(k, g, hx, hy, w, skin, d, _fix(arm, d))

    def hv_draw(k, g, hx, hy, w, skin, d, arm):
        if g in hv.DRAW and hp.GLOVE[0] is None:
            arm = _fix(arm, d)
        return o_hv(k, g, hx, hy, w, skin, d, arm)
    hv.draw = hv_draw
    _SET[0] = True
