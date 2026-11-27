"""The Double Agent (episode 15): 5.2, the still before motion (S3 · MC), with the hand library v3 (Tomas 27 Nov: "library
v3 tvirtinam", "darom"). Script v4: his cup rattles on the saucer, coffee slops into it; he sips from the cup, the saucer
held out in his other hand, eyes never leaving the office; he notices how it looks, lifts his little finger.

This is the held pose of the sip (the finger up), one still, checked before any motion:
  - Don (don_ps, the approved rig, ps_scenes' scale 0.60 at don_mid) on the front desk v4 room (ps_set.room, 14's state);
  - his rig's own hands not drawn at the two wrists (of_cast.held); there, the library's hands (hand_lib_v3):
    screen right (his left), CUP_GRIP at the cheek, the cup on the thumb's side toward his mouth, the little finger
    out away from it; screen left (his right), SAUCER_SUPPORT, out low, level;
  - left and right by the canon's hands_lr (copied verbatim, 27 Nov; da_arms is for the locked frames only, PR #11):
    the library hands take hands_lr.side() and are logged for hands_lr.check();
  - the arms solved for the shoulders the rig draws (da_s8r._ik / _arm_log), the elbows out (cup) and low (saucer);
  - da_hand_gate on the frame: the job list, POLE, CROSS, AIR, SEEN (the cup's and the saucer's china round the hands).

  python3 da_s52.py  -> ../the-double-agent/da_s52_still_v1.png and da_s52_review_v1.png (full size, crops, 270 px)
"""
import math
import os
import sys

import cairo
from PIL import Image

import kit
from kit import Ctx
import fs_storyboard_v17 as sbv
import ps_set as pss
import da_set as ds
import don_ps as dp
import hands_ps as hp
import hands_v4 as hv
import of_cast as oc
import da_arms
import da_s8r as r8
import da_hands as dh
import hand_lib_v3 as hl
import hand_lib_sheet_v3 as hs

W, H = 540, 960
F = pss.F
DON = (522, F + 330, ds.SC["don"])                              # da_set.establish: Don on his side, his office in view
CAM = [None]                                                     # MC, set from his head in render(): head to belt
SKIN = hs.SKIN
HW = 17 * 1.15 * 1.25 * DON[2]                                  # the rig's own hand size at his scale (kit.arm w 17 x 1.15, hands_ps
                                                                 # x 1.25): v1 used 17 x 0.60 and drew hands a third too small
LOOK = (1, -0.4)                                                 # to his office (zone C, up and screen right; da_set)


def _ik_low(S_, T, l1):
    a = r8._ik(S_, T, l1, l1, +1); b = r8._ik(S_, T, l1, l1, -1)
    ey = lambda q: S_[1] + l1 * math.cos(math.radians(q[0]))
    return a if ey(a) >= ey(b) else b


def solve():
    x, f, s = DON
    lg = r8._arm_log(lambda k: dp.don(k, x, f, s, (0, 0, 0, 0), "neutral", LOOK, hands=False))
    (SL, l1, _), (SR, r1, _) = lg[0], lg[1]
    s2 = cairo.ImageSurface(cairo.FORMAT_RGB24, 2, 2); c2 = cairo.Context(s2); c2.scale(2, 2)
    head = dp.don(Ctx(c2, 0), x, f, s, (0, 0, 0, 0), "neutral", LOOK, hands=False)["head"]
    hr = 50 * s
    WR = (head[0] + hr * 1.55, head[1] + hr * 1.05)               # the cup hand's wrist, below and outside his cheek
    aR = r8._ik(SR, WR, r1, r1, +1)                              # the elbow out to the right
    WL = (SL[0] - 0.95 * l1, SL[1] + 1.35 * l1)                  # the saucer hand, out low on his other side
    aL = _ik_low(SL, WL, l1)
    return dict(WR=WR, WL=WL, aR=aR, aL=aL, head=head)


def scene(k, sol):
    import da_hand_gate as g
    c = k.c
    x, f, s = DON
    ds._floor_on(c)
    ds.room(k, inside=False)                                     # (the office cast is out of this camera) episode 15's set: the front desk, the tape, the office glass
    ds._tape_seam(c)
    if g._ON[0]:
        g.jobs(("don", "R", "cup_grip", "library v3 CUP_GRIP: the cup's handle in the fist, the little finger out"),
               ("don", "L", "saucer_support", "library v3 SAUCER_SUPPORT: the saucer level on the palm, the thumb over its rim"))
    old = kit.HAND[0]; kit.HAND[0] = hp.hand; hp.reset("quiet", "quiet")
    try:
        o = oc.held(k, lambda: dp.don(k, x, f, s, sol["aL"] + sol["aR"], "neutral", LOOK, hands=False),
                    lambda o_: [sol["WR"], sol["WL"]])
    finally:
        kit.HAND[0] = old
    # the cup hand: the forearm's direction from the solved angles (lean 0: local = screen)
    import hands_lr as lr
    dR = (math.sin(math.radians(sum(sol["aR"]))), math.cos(math.radians(sum(sol["aR"]))))
    angR = math.atan2(dR[1], dR[0])
    side = lr.side(+1, dR)                                       # the canon's side (raised: the thumb toward his head)
    Hh = hl.to_screen("CUP_GRIP", sol["WR"][0], sol["WR"][1], angR, HW, side, hl.contact("CUP_GRIP", "handle"))
    Y1 = hl.to_screen("CUP_GRIP", sol["WR"][0], sol["WR"][1], angR, HW, side, (1.10, 1.06))
    body_left = 1 if Y1[0] < Hh[0] else -1
    cup_s = 1.1 * HW / 26.0
    hl.LWS[0] = DON[2]
    hl.draw_lr(k, "CUP_GRIP", sol["WR"][0], sol["WR"][1], dR, HW, SKIN, +1,
               back_obj=lambda k_: hs.big_cup(k_, Hh[0], Hh[1], cup_s, body_left, HW, DON[2]))
    oc.log_grip(c, "cup_grip", *Hh)
    r = 0.42 * HW
    xe = Hh[0] - body_left * 0.80 * r
    bx0, bx1 = (xe - 1.15 * HW, xe) if body_left > 0 else (xe, xe + 1.15 * HW)
    g.prop(k, "cup", min(bx0, Hh[0]) - 2, Hh[1] - 1.7 * r, abs(bx1 - bx0) + abs(Hh[0] - xe) + 6, 3.2 * r,
           colors=(dh.CHINA, dh.CHINA_D)) if g._ON[0] else None
    # the saucer hand
    Sp = hl.to_screen("SAUCER_SUPPORT", sol["WL"][0], sol["WL"][1], 0, HW, -1, hl.contact("SAUCER_SUPPORT", "saucer"))
    Tp = hl.to_screen("SAUCER_SUPPORT", sol["WL"][0], sol["WL"][1], 0, HW, -1, hl.contact("SAUCER_SUPPORT", "touch"))
    hl.draw_lr(k, "SAUCER_SUPPORT", sol["WL"][0], sol["WL"][1], (-1.0, 0.0), HW, SKIN, -1, reach=-1,
               obj=lambda k_: hs.saucer_at(k_, Sp[0], Sp[1], 0.95 * HW / 30.0, DON[2]))
    hl.LWS[0] = 1.0
    oc.log_grip(c, "saucer_support", *Tp)
    if g._ON[0]:
        sw = 0.95 * HW
        g.prop(k, "saucer", Sp[0] - sw - 2, Sp[1] - 0.75 * sw, 2 * sw + 4, 0.75 * sw + 6, colors=(dh.CHINA, dh.CHINA_D))
    return o


def render(scale=2):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W * scale, H * scale)
    c = cairo.Context(s); c.scale(scale, scale)
    c.set_source_rgb(*kit.WALL); c.paint()
    k = Ctx(c, 0)
    sol = solve()
    hx, hy = sol["head"]
    CAM[0] = (hx - 16, hy + 56, 2.5)                              # his chest at the frame's middle
    c.save(); sbv.view(c, *CAM[0])
    scene(k, sol)
    c.restore()
    return s


def main(out_dir="../the-double-agent"):
    import da_hand_gate as g
    import hands_lr as lr
    lr.setup(); hv.enable(); g.install()                         # the canon's left/right (not da_arms: PR #11)
    for kind in ("cup_grip", "saucer_support"):
        if kind not in g.PENDING:
            g.PENDING = g.PENDING + (kind,)
            g.HOLDING = g.HOLDING + (kind,)
    g.reset(); lr.reset_log(); lr.frame(cut=True)
    s = render()
    s.flush()
    ok = g.report("5.2 still", g.check() + g.check_seen(s) + ["THUMB hands_lr: %s" % (f,) for f in lr.check()])
    print("    hands_lr: %d hands logged, check %s" % (len(lr.LOG), "clean" if not lr.check() else lr.check()))
    p = os.path.join(out_dir, "da_s52_still_v1.png")
    s.write_to_png(p)
    im = Image.open(p).convert("RGB")
    full = im.resize((540, 960))
    tile = im.resize((270, 480))
    out = Image.new("RGB", (540 + 20 + 520, 960), (255, 255, 255))
    out.paste(full, (0, 0))
    y = 0
    for box in ((560, 700, 1080, 1220), (0, 900, 520, 1420)):
        cr = im.crop(box)
        out.paste(cr.resize((520, 520 * cr.height // cr.width)) if cr.width != 520 else cr, (560, y)); y += 526
    out.paste(tile, (560 + 520 - 270, 960 - 480 + 0) if y + 480 > 960 else (560, y))
    out.save(os.path.join(out_dir, "da_s52_review_v1.png"))
    print("wrote da_s52_still_v1.png, da_s52_review_v1.png")
    return ok


if __name__ == "__main__":
    sys.exit(0 if main(*sys.argv[1:]) else 1)
