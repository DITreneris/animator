"""The Double Agent (episode 15): the silhouette test for 5.2, the one job in script v4 with no canon row (rules-hands
0.2: three solid black silhouettes side by side, 270 px wide each, two cold viewers; keep the one both read as meant,
then add the row). Job list: the-double-agent-hand-jobs-v1.md.

5.2 (script v4): his cup rattles on the saucer, coffee slops into it; he drinks from the saucer, eyes on the office;
he notices how it looks, lifts his little finger and goes on as if he meant to.
  A  the saucer in both hands like a bowl at his mouth, the little finger of one hand out
  B  the saucer on one hand's fingertips at his mouth, the little finger out; the cup in the other hand at his chest
  C  the saucer by its rim, thumb on top, raised from the side; the little finger out stiff; the other hand hanging

  python3 da_sil_saucer.py  -> ../the-double-agent/da_sil_saucer_v1.png (silhouettes, 3 x 270 px) and _colour.png
"""
import math
import os
import sys

import cairo
from PIL import Image

import kit
from kit import Ctx, INK, cut, ellipse
import da_arms
import hands_v4 as hv
import hands_ps as hp
import don_ps as dp
import da_s8r as r8

W, H, S, X, FEET = 360, 600, 1.25, 192, 585
SKIN = (0.96, 0.78, 0.66)
CHINA = (0.98, 0.97, 0.94)
COFFEE = (0.40, 0.24, 0.12)


def _shoulders():
    lg = r8._arm_log(lambda k: dp.don(k, X, FEET, S, (0, 0, 0, 0), "neutral", (1, 0), hands=False))
    s2 = cairo.ImageSurface(cairo.FORMAT_RGB24, 2, 2); c2 = cairo.Context(s2); c2.scale(2, 2)
    o = dp.don(Ctx(c2, 0), X, FEET, S, (0, 0, 0, 0), "neutral", (1, 0), hands=False)
    return lg[0], lg[1], o["head"]


def saucer(k, x, y, tilt=0.0, coffee=True):
    c = k.c
    c.save(); c.translate(x, y); c.rotate(tilt)
    ellipse(k, 0, 0, 34 * S, 7.5 * S, CHINA, 7101, shadow=False, lw=2)
    if coffee:
        ellipse(k, 0, -1 * S, 15 * S, 3 * S, COFFEE, 7102, shadow=False, lw=1.2)
    c.restore()


def cup(k, x, y, big=1.0):
    """(x, y): the bottom of its body; the handle on the right, where his fingers hold it."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(S * big, S * big)
    c.set_source_rgb(*INK); c.set_line_width(4); c.new_path(); c.arc(12, -8, 6, -1.4, 1.4); c.stroke()
    cut(k, [(-11, -16), (11, -16), (8, 0), (-8, 0)], CHINA, shadow=False, lw=2)
    c.restore()


def pinky(k, x, y, ang, ln=15):
    """the little finger, out: a capsule from the hand's edge (ang: radians on screen, 0 = right)."""
    c = k.c
    ex, ey = x + math.cos(ang) * ln * S, y + math.sin(ang) * ln * S
    for col, lw in ((INK, 8.5 * S), (SKIN, 5.2 * S)):
        c.set_source_rgb(*col); c.set_line_width(lw); c.set_line_cap(1)
        c.new_path(); c.move_to(x, y); c.line_to(ex, ey); c.stroke()
    c.set_line_cap(0)


def _arms_to(L, R, TL, TR, outL=-1, outR=+1):
    (SL, l1, _), (SR, r1, _) = L, R
    a = r8._ik(SL, TL, l1, l1, outL) if TL else (0.0, 0.0)
    b = r8._ik(SR, TR, r1, r1, outR) if TR else (0.0, 0.0)
    return a + b


def variant(k, v, L, R, head):
    """v2 of the three (after looking at v1: front on, a saucer at the mouth and two hands round it vanish into the
    face in silhouette, and A crossed the forearms): the saucer sticks out past the cheek, the hand under its far end
    and the little finger outside the head's outline, where a silhouette can show them."""
    hx, hy = head
    mx, my = hx + 4 * S, hy + 30 * S                          # his mouth, about
    if v == "A":                                              # one hand, the other hanging
        sx, sy = mx + 40 * S, my + 4 * S
        TR = (sx + 28 * S, sy + 9 * S)
        arms = _arms_to(L, R, None, TR, -1, +1)
        dp.don(k, X, FEET, S, arms, "neutral", (1, 0), hands=("quiet", "grab"))
        saucer(k, sx, sy, -0.22)
        hp.redraw_at(k, *TR)
        pinky(k, TR[0] + 8 * S, TR[1] - 3 * S, -0.9, 18)
    elif v == "B":                                            # and the cup held out on the other side
        sx, sy = mx + 40 * S, my + 4 * S
        TR = (sx + 28 * S, sy + 9 * S)
        TL = (L[0][0] - 46 * S, L[0][1] + 62 * S)
        arms = _arms_to(L, R, TL, TR, -1, +1)
        dp.don(k, X, FEET, S, arms, "neutral", (1, 0), hands=("grab", "grab"))
        saucer(k, sx, sy, -0.22)
        cup(k, TL[0], TL[1] - 6 * S)
        hp.redraw_at(k, *TR); hp.redraw_at(k, *TL)
        pinky(k, TR[0] + 8 * S, TR[1] - 3 * S, -0.9, 18)
    else:                                                     # tipped up like a bowl, the other fist on his hip
        sx, sy = mx + 38 * S, my - 4 * S
        TR = (sx + 30 * S, sy - 10 * S)
        TL = (X - 62 * S, FEET - 110 * S)
        arms = _arms_to(L, R, TL, TR, -1, +1)
        dp.don(k, X, FEET, S, arms, "neutral", (1, 0), hands=("fist", "grab"))
        saucer(k, sx, sy, -0.62)
        hp.redraw_at(k, *TR)
        pinky(k, TR[0] + 8 * S, TR[1] - 4 * S, -1.2, 18)


def variant_cup(k, v, L, R, head):
    """Tomas 27 Nov ("Pinky on the cup"; the saucer sip read 0 of 2): the coffee slops into the saucer (on the prop), he
    drinks from the CUP with his little finger out. Three silhouettes, the cup and the finger outside the head's outline.
      A  the cup just off his lips at the cheek, elbow out, the finger level
      B  the same, the saucer in his other hand at his chest, held out to the side
      C  cup and saucer held out in front of his chest, posh, the finger out"""
    hx, hy = head
    mx, my = hx + 4 * S, hy + 30 * S
    if v == "A":
        cx, cy = mx + 92 * S, my + 10 * S
        TR = (cx + 6 * S, cy + 4 * S)
        arms = _arms_to(L, R, None, TR, -1, +1)
        dp.don(k, X, FEET, S, arms, "neutral", (1, 0), hands=("quiet", "pinch"))
        cup(k, TR[0] - 24 * S, TR[1] + 10 * S, 1.6)
        hp.redraw_at(k, *TR)
        pinky(k, TR[0] + 8 * S, TR[1] + 4 * S, 0.0, 20)
    elif v == "B":
        cx, cy = mx + 92 * S, my + 10 * S
        TR = (cx + 6 * S, cy + 4 * S)
        TL = (L[0][0] - 50 * S, L[0][1] + 58 * S)
        arms = _arms_to(L, R, TL, TR, -1, +1)
        dp.don(k, X, FEET, S, arms, "neutral", (1, 0), hands=("grab", "pinch"))
        saucer(k, TL[0], TL[1] - 6 * S, 0.0, coffee=False)
        cup(k, TR[0] - 24 * S, TR[1] + 10 * S, 1.6)
        hp.redraw_at(k, *TR); hp.redraw_at(k, *TL)
        pinky(k, TR[0] + 8 * S, TR[1] + 4 * S, 0.0, 20)
    else:
        TL = (L[0][0] - 44 * S, L[0][1] + 70 * S)
        TR = (R[0][0] + 56 * S, R[0][1] + 40 * S)
        arms = _arms_to(L, R, TL, TR, -1, +1)
        dp.don(k, X, FEET, S, arms, "neutral", (1, 0), hands=("grab", "pinch"))
        saucer(k, TL[0], TL[1] - 6 * S, 0.0, coffee=False)
        cup(k, TR[0] - 24 * S, TR[1] + 10 * S, 1.6)
        hp.redraw_at(k, *TR); hp.redraw_at(k, *TL)
        pinky(k, TR[0] + 8 * S, TR[1] + 4 * S, 0.0, 20)


def _ik_low(S_, T, l1):
    """of the two elbows, the lower one (an arm carrying a saucer: the elbow by the side)."""
    a = r8._ik(S_, T, l1, l1, +1); b = r8._ik(S_, T, l1, l1, -1)
    ey = lambda q: S_[1] + l1 * math.cos(math.radians(q[0]))
    return a if ey(a) >= ey(b) else b


def variant_cup2(k, v, L, R, head):
    """v2 of the cup sheet (outside audit 27 Nov, "tobulinam"): B (kept, 2/2 "sipping", "a bit posh") and A, with the
    hands of da_hands: the cup in a pinch with the little finger out of the hand, the handle under thumb and index;
    the saucer level on a palm-up hand. The elbows bent wider; the china grey-white. Checked by da_hand_gate."""
    import da_hands as dh
    import of_cast as oc
    import da_hand_gate as g
    hx, hy = head
    mx, my = hx + 4 * S, hy + 30 * S
    (SL, l1, _), (SR, r1, _) = L, R
    w = 24.4 * S
    WR = (mx + 96 * S, my + 22 * S)                            # the cup hand's wrist, out past the cheek
    aR = r8._ik(SR, WR, r1, r1, +1)                            # the elbow out to the right
    if v == "B":
        WL = (SL[0] - 40 * S, SL[1] + 78 * S)                   # the saucer hand, out low on the other side
        aL = _ik_low(SL, WL, l1)
    else:
        WL, aL = None, (4.0, 6.0)
    g.jobs(("don", "R", "pinch_pinky", "new row (5.2): the cup's handle in a pinch, the little finger out"),
           ("don", "L", "saucer_hold" if v == "B" else "quiet", "new row (5.2): the saucer on a palm-up hand" if v == "B" else "at rest"))
    old = kit.HAND[0]; kit.HAND[0] = hp.hand; hp.reset("quiet", "quiet")
    try:
        oc.held(k, lambda: dp.don(k, X, FEET, S, aL + aR, "neutral", (1, 0), hands=False),
                lambda o_: [WR] + ([WL] if WL else []))
    finally:
        kit.HAND[0] = old
    dR = (math.sin(math.radians(sum(aR))), math.cos(math.radians(sum(aR))))
    r_cup = dh.cup_in_pinch(k, WR[0], WR[1], dR, w, SKIN, 1, (mx + 30 * S, my), 1.45 * S)
    g.prop(k, "cup", *r_cup, colors=(dh.CHINA, dh.CHINA_D))
    if WL:
        dL = (math.sin(math.radians(sum(aL))), math.cos(math.radians(sum(aL))))
        r_s = dh.saucer_hold(k, WL[0], WL[1], dL, w, SKIN, -1, 1.25 * S)
        g.prop(k, "saucer", r_s[0], r_s[1] - 4, r_s[2], r_s[3] + 22, colors=(dh.CHINA, dh.CHINA_D))


SET = ["saucer"]


def render(v):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W * 2, H * 2)
    c = cairo.Context(s); c.scale(2, 2)
    L, R, head = _shoulders()
    {"saucer": variant, "cup": variant_cup, "cup2": variant_cup2}[SET[0]](Ctx(c, 0), v, L, R, head)
    return s


def main(out_dir="../the-double-agent"):
    da_arms.setup(); hv.enable()
    tiles, cols = [], []
    import da_hand_gate as g
    g.install()
    for v in ("BA" if SET[0] == "cup2" else "ABC"):
        g.reset()
        s = render(v)
        s.flush()
        if SET[0] == "cup2":
            g.S[0] = 2.0
            g.report("5.2 %s" % v, g.check() + g.check_seen(s))
        p = "/tmp/_sil_%s.png" % v
        s.write_to_png(p)
        im = Image.open(p).convert("RGBA")
        bg = Image.new("RGBA", im.size, (255, 255, 255, 255)); bg.alpha_composite(im)
        cols.append(bg.convert("RGB").resize((270, 450)))
        a = im.split()[3].point(lambda u: 0 if u > 40 else 255)            # solid black wherever anything is drawn
        tiles.append(a.convert("RGB").resize((270, 450)))
    stem = {"saucer": "da_sil_saucer_v3", "cup": "da_sil_cup_v1", "cup2": "da_sil_cup_v2"}[SET[0]]
    for name, ims in ((stem + ".png", tiles), (stem + "_colour.png", cols)):
        out = Image.new("RGB", (290 * len(ims) - 20, 450), (255, 255, 255))
        for i, im in enumerate(ims):
            out.paste(im.convert("RGB"), (i * 290, 0))
        out.save(os.path.join(out_dir, name))
        print("wrote", name)


if __name__ == "__main__":
    if sys.argv[1:2] in (["cup"], ["cup2"]):
        SET[0] = sys.argv.pop(1)
    main(*sys.argv[1:])
