"""THE DOUBLE AGENT (episode 15): 5.2 animated. First up to its locked still (da_s52); then (Tomas 28 Nov, after the
cold test read the cup at his cheek as "a phone": "atrakinam ir sutvarkom") unlocked: the cup goes to his MOUTH and
tips for the sip. The rig, the camera and the cup and saucer are the still's; the hands are now the episode's library
(hand_lib_v4, gated like every other shot).

  0.00-0.80  the cup on its saucer at his chest, his fist on its handle: it rattles, coffee slops into the saucer
  0.80-1.27  he lifts the cup to his cheek (the little finger tucked in) and the saucer goes out low to his side
  1.27-1.93  the sip: the cup at his lips, tipped; his eyes on his office over it
  1.93-2.13  his eyes drop to his hand: how it looks; the little finger comes out; eyes back up, as if he meant it
  2.13-2.80  held: the cup lowered to his chin, the little finger out, smug
"""
import math

import cairo

import kit
from kit import Ctx
import fs_storyboard_v17 as sbv
import da_set as ds
import don_ps as dp
import hands_ps as hp
import of_cast as oc
import da_s8r as r8
import da_s52 as S
import hand_lib_v4 as hl
import hand_lib_sheet_v3 as hs

# the fist round the handle with the little finger tucked in (CUP_GRIP's outline, its finger's five points pulled in)
_cg = hl.POSES["CUP_GRIP"]
_out = list(_cg["outline"])
_i = _out.index((0.88, -0.50))
_out[_i:_i + 5] = [(0.92, -0.44), (0.97, -0.40)]
hl.POSES.setdefault("CUP_GRIP_TUCK", dict(outline=_out, lines=_cg["lines"], contacts=_cg["contacts"]))

COFFEE = (0.36, 0.22, 0.12)


def _lerp(a, b, u):
    return (a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u)


def _ease(x):
    x = min(1.0, max(0.0, x)); return x * x * (3 - 2 * x)


def _seg(t, a, b):
    return min(1.0, max(0.0, (t - a) / (b - a)))


def _wrist_for(SR, r1, Hh, side_guess=1):
    """the cup hand's wrist that puts the CUP_GRIP's handle contact on Hh (a few fixed-point steps through the IK)."""
    import hands_lr as lr
    W = (Hh[0] - 18, Hh[1] + 10)
    for _ in range(6):
        a = r8._ik(SR, W, r1, r1, +1)
        d = (math.sin(math.radians(sum(a))), math.cos(math.radians(sum(a))))
        ang = math.atan2(d[1], d[0]); side = lr.side(+1, d)
        P = hl.to_screen("CUP_GRIP", W[0], W[1], ang, S.HW, side, hl.contact("CUP_GRIP", "handle"))
        W = (W[0] + Hh[0] - P[0], W[1] + Hh[1] - P[1])
    return W


def _scene(k, WR, WL, reachL, cup_pose, look, jig=(0, 0), slop=0.0, cup_on_saucer=False, tip=0.0, face="neutral"):
    import da_hand_gate as g
    c = k.c
    g.jobs(("don", "R", "pinch_pinky", "CUP_GRIP: the cup by its handle (the little finger in, then out)"),
           ("don", "L", "saucer_hold", "SAUCER_SUPPORT: the saucer on his palm"))
    x, f, s = S.DON
    ds._floor_on(c)
    ds.room(k, inside=False)
    ds._tape_seam(c)
    lg = r8._arm_log(lambda k_: dp.don(k_, x, f, s, (0, 0, 0, 0), "neutral", look, hands=False))
    (SL, l1, _), (SR, r1, _) = lg[0], lg[1]
    aR = r8._ik(SR, WR, r1, r1, +1)
    aL = S._ik_low(SL, WL, l1)

    def fk(S_, a, ln):                                         # where the arm really ends (a wrist past its reach
        d1 = (math.sin(math.radians(a[0])), math.cos(math.radians(a[0])))   # is clamped by the IK): the hand goes there
        d2 = (math.sin(math.radians(a[0] + a[1])), math.cos(math.radians(a[0] + a[1])))
        return (S_[0] + ln * (d1[0] + d2[0]), S_[1] + ln * (d1[1] + d2[1]))
    WR, WL = fk(SR, aR, r1), fk(SL, aL, l1)
    old = kit.HAND[0]; kit.HAND[0] = hp.hand; hp.reset("quiet", "quiet")
    try:
        o = oc.held(k, lambda: dp.don(k, x, f, s, aL + aR, face, look, hands=False), lambda o_: [WR, WL])
    finally:
        kit.HAND[0] = old
    import hands_lr as lr
    HW = S.HW
    hl.LWS[0] = s
    # the saucer first when the cup stands on it (the cup over it), else after the cup hand as the still has it
    dL = (1.0, 0.0) if reachL > 0 else (-1.0, 0.0)
    Sp = hl.to_screen("SAUCER_SUPPORT", WL[0], WL[1], 0, HW, reachL, hl.contact("SAUCER_SUPPORT", "saucer"))
    ss = 0.95 * HW / 30.0

    def saucer(k_):
        hs.saucer_at(k_, Sp[0], Sp[1], ss, s)
        g.vessel(k_, "saucer", "held", base=Sp, rect=(Sp[0] - 30 * ss, Sp[1] - 14 * ss, 60 * ss, 16 * ss))
        if slop > 0:                                          # the slopped coffee in its well
            kit.ellipse(k_, Sp[0] + 3, Sp[1] - 11 * ss, 11 * ss * min(1, slop), 3.4 * ss * min(1, slop), COFFEE, 7123,
                        shadow=False, lw=1.0)
    if cup_on_saucer:
        hl.draw_lr(k, "SAUCER_SUPPORT", WL[0], WL[1], dL, HW, S.SKIN, -1, reach=reachL, obj=saucer)
    dR = (math.sin(math.radians(sum(aR))), math.cos(math.radians(sum(aR))))
    angR = math.atan2(dR[1], dR[0])
    side = lr.side(+1, dR)
    Hh = hl.to_screen(cup_pose, WR[0], WR[1], angR, HW, side, hl.contact(cup_pose, "handle"))
    Y1 = hl.to_screen(cup_pose, WR[0], WR[1], angR, HW, side, (1.10, 1.06))
    body_left = 1 if Y1[0] < Hh[0] else -1
    cup_s = 1.1 * HW / 26.0
    def cup(k_):
        c.save(); c.translate(*Hh); c.rotate(-body_left * tip); c.translate(-Hh[0], -Hh[1])    # tipped about its handle
        hs.big_cup(k_, Hh[0], Hh[1], cup_s, body_left, HW, s)
        c.restore()
        xe = Hh[0] - body_left * 0.80 * r_
        g.vessel(k_, "cup", "held", handle=Hh, base=(xe - body_left * 0.575 * HW, Hh[1] + 1.35 * r_),
                 rect=(min(xe, xe - body_left * 1.15 * HW) - 2, Hh[1] - 1.7 * r_, 1.15 * HW + 4, 3.2 * r_))
    r_ = 0.42 * HW
    c.save(); c.translate(*jig)
    hl.draw_lr(k, cup_pose, WR[0], WR[1], dR, HW, S.SKIN, +1, back_obj=cup)
    c.restore()
    if not cup_on_saucer:
        hl.draw_lr(k, "SAUCER_SUPPORT", WL[0], WL[1], dL, HW, S.SKIN, -1, reach=reachL, obj=saucer)
    hl.LWS[0] = 1.0
    return o, Hh, Sp


def frame(t, scale=1):
    """one frame of 5.2 at t seconds (the drawings change 15 times a second), at S.W x S.H * scale. The still's camera
    (fs_storyboard_v17.view) is framed for its 1080 render: drawn at 2 and scaled down, as da_s52.render(2) is."""
    big = _frame2(t)
    if scale == 2:
        return big
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, S.W * scale, S.H * scale)
    c = cairo.Context(surf); c.scale(scale / 2.0, scale / 2.0)
    c.set_source_surface(big, 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD); c.paint()
    return surf


def _frame2(t):
    scale = 2
    td = math.floor(t * 15 + 1e-6) / 15.0
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, S.W * scale, S.H * scale)
    c = cairo.Context(surf); c.scale(scale, scale)
    c.set_source_rgb(*kit.WALL); c.paint()
    k = Ctx(c, 0)
    sol = S.solve()
    hx, hy = sol["head"]
    S.CAM[0] = (hx - 16, hy + 56, 2.5)
    c.save(); sbv.view(c, *S.CAM[0])
    x, f, s = S.DON
    HW = S.HW
    hr = 50 * s
    r = 0.42 * HW
    lg = r8._arm_log(lambda k_: dp.don(k_, x, f, s, (0, 0, 0, 0), "neutral", S.LOOK, hands=False))
    (SL, l1, _), (SR, r1, _) = lg[0], lg[1]
    # the start: the saucer at his chest on his screen-left palm (reaching in), the cup standing on it, his fist on
    # its handle on the screen-right side
    ss = 0.95 * HW / 30.0
    Sp0 = (hx + 16, hy + 3.5 * hr)                               # (cold test: at his chest it hid the vest's stain,
                                                              # which then read as a spill) at his belt, below it
    WL0 = (Sp0[0] - 0.98 * HW, Sp0[1] + 0.36 * HW)
    bw = 1.15 * HW
    Hh0 = (Sp0[0] + bw / 2 + 0.80 * r, Sp0[1] - 10 * ss - 1.35 * r)
    WR0 = _wrist_for(SR, r1, Hh0)
    lift = _ease(_seg(td, 0.80, 1.27))
    mouth = (hx, hy + 0.56 * hr)                               # kit's mouth: 28 of the head's 50 below its middle
    Hm = (hx + bw / 2 + 0.80 * r - 4, mouth[1] + 1.25 * r)      # the cup's rim at his lower lip, its body over his mouth
    Hc = (Hm[0] + 14, Hm[1] + 1.7 * hr)                         # after: lowered to his chest, the elbow down (cold
                                                               # test: at the chin it stood up "like a broken arm")
    WRm = _wrist_for(SR, r1, Hm)
    WRc = _wrist_for(SR, r1, Hc)
    down = _ease(_seg(td, 2.07, 2.27))
    WR = _lerp(WR0, _lerp(WRm, WRc, down), lift)
    WR = (WR[0], WR[1] - 14 * math.sin(math.pi * lift))       # an arc up to the cheek, not a straight line
    WL = _lerp(WL0, sol["WL"], _ease(_seg(td, 0.87, 1.27)))
    reachL = 1 if td < 1.0 else -1                             # the saucer hand turns out as it goes (a smear drawing)
    rattle = td < 0.80
    n = int(round(td * 15))
    jig = ((1.6 if n % 2 else -1.6), (-1.0 if n % 2 else 0.6)) if rattle else (0, 0)
    slop = _seg(td, 0.40, 0.73)
    look = S.LOOK
    if 1.93 <= td < 2.07:                                      # his eyes drop to his own hand
        look = (0.9, 0.5)
    pose = "CUP_GRIP" if td >= 2.0 else "CUP_GRIP_TUCK"
    tip = 0.45 * math.sin(math.pi * _seg(td, 1.27, 1.93))      # the sip: the cup tips up and back down
    face = "smug" if td >= 2.13 else "neutral"
    _scene(k, WR, WL, reachL, pose, look, jig=jig, slop=slop, cup_on_saucer=lift < 0.5, tip=tip, face=face)   # (the saucer under the cup till it's clear)
    c.restore()
    return surf


if __name__ == "__main__":
    import sys
    import da_arms
    import hands_v4 as hv
    da_arms.setup(); hv.enable()
    from PIL import Image
    ts = [0.0, 0.33, 0.6, 0.93, 1.1, 1.5, 1.95, 2.07, 2.5]
    ims = [frame(t) for t in ts]
    W = Image.new("RGB", (270 * len(ts), 480))
    for i, s_ in enumerate(ims):
        s_.write_to_png("/tmp/q/s52_%d.png" % i)
        W.paste(Image.open("/tmp/q/s52_%d.png" % i).resize((270, 480)), (i * 270, 0))
    W.save("/tmp/q/s52_strip.png")
    print("ok")
