"""DADDY'S HOME (episode 12): the animation pass, scene 4 "The Wrong Man" (scene sheet v4, 14.9 s). The engine is
dh_anim.Scene. Between and inside the key drawings: the visitor walking in, the three snapping into a line, Don's arm
sweeping the room open, Pam's eyes going down and her mug tipping, the shredder eating a page, Don's sidestep in front
of it, the PREMIUM sticker slapped on, the robot talked over, the visitor's look down and up.
  KOKORO_DIR=/tmp/kokoro python3 dh_anim4.py [hi]  ->  ../daddys-home/dh_s4_anim_v1.mp4, dh_s4_anim_v1_strip.png"""
import math
import sys
import kit
import fs_storyboard as sb
import dh_cast as dc
import dh_props as dp
import dh_layout as dl
import dh_animatic as da
import dh_scenes as ds
import dh_anim1 as A
import cs_sfx as fx
from dh_anim import Scene, seq, idx, don_at, cheek, DPS, DS_, F, CH
from kit import INK

PAM, SS, PS, MS, GS = ds.PAM, ds.SS, ds.PS, ds.MS, ds.GS
LINE, THR4, TOUR, SHRED_X = ds.LINE, ds.THR4, ds.TOUR, ds.SHRED_X
scs, pb = ds.scs, ds.pb
VX = TOUR[1][0] - 14                                        # the visitor's place in the tour shots

# v2 (22 Nov, after the scene 4 review): Don's line is "Premium. On us." (so "Then make it lifetime." tops it; 6.1'' is 1.5 s);
# Pam's mug is a mug (the one from scene 5), white and empty inside; the slap has a burst and rocks him back; at the end his
# whole body tips to look at the sticker and comes up again. v1: dh_anim4_v1.py
sc = Scene(4, "v2", ds.S4,
           takes=[("5.2", "5.1", 0.35), ("5.3", "5.3", 0.10), ("6.1a", "6.1", 0.06), ("6.1b", "6.1''", 0.10), ("6.2", "6.2", 0.04), ("6.3", "6.3", 0.06)],
           cut={"6.2": "6.3"})                              # the robot is talked over on purpose


def vis_tip(x, feet, side=1):                               # beside the visitor's mouth
    h = dl.hc(x, feet, GS)
    return (h[0] + side * h[2] * 0.62, h[1] + h[2] * 0.5)


def shredding(k, n):
    """The shredder running: the page goes down into it a little every drawing, the shreds jump from side to side."""
    c = k.c
    top = F - 96
    c.save(); c.translate(SHRED_X + 2 + (1 if n % 2 else -1), top - 20 + (n % 6) * 3.5); c.rotate(0.06)
    c.rectangle(-40, -60, 80, 60 + 14 - (n % 6) * 3.5); c.clip()        # what is still above the slot
    kit.rect(k, -17, -30, 34, 44, (0.99, 0.98, 0.95), 3560, lw=1.8)
    c.set_source_rgb(*INK); c.set_line_width(1.3)
    for yy in (-20, -12, -4):
        c.move_to(-11, yy); c.line_to(11, yy); c.stroke()
    c.restore()
    sg = 1 if n % 2 else -1
    ds._lines(k, [(SHRED_X - 30, top - 6, SHRED_X - 42 - 3 * sg, top - 16), (SHRED_X + 34, top - 6, SHRED_X + 46 + 3 * sg, top - 16),
                  (SHRED_X - 34, top + 14, SHRED_X - 48 + 3 * sg, top + 14), (SHRED_X + 38, top + 14, SHRED_X + 52 - 3 * sg, top + 14)])


def r_door(s, k, o, t, tt, n):                              # 5.1: a knock, and he is already in
    x = seq(t, [84, 98, 112, 122, 128])
    bob = seq(t, [0, -5, 0, -4, 0]) + (-2 if (s.speaking("5.2", tt) and n % 2) else 0)
    with A.About(k.c, x, F + 8, 1.0, 1.0, bob):
        dc.repairman(k, x, F + 8, GS, look=(0.6, 0))
    if idx(t) < 4:
        ds._lines(k, [(x - 42, F - 6, x - 54, F - 6), (x - 40, F + 4, x - 56, F + 4)])
    if s.speaking("5.2", tt):
        o["say"] = ("I'm here to inspect the machine.", vis_tip(128, F + 8), 1, False, 30, 190)


def r_line(s, k, o, t, tt, n):                              # 5.2: they snap into a line
    dm, dd, dsf = seq(t, [(-30, 22, 34), (7, -5, -8), (0, 0, 0)])
    i = idx(t)
    dp.ceo_chair(k, THR4, CH[1], CH[2])
    sb.mfs.mom(k, LINE[0][0] + dm, LINE[0][1], MS, "stand", "sweet", look=(-1, 0))
    scs.sofia(k, LINE[2][0] + dsf, LINE[2][1], SS, "hold", "recover", look=(-1, 0))
    don_at(k, LINE[1][0] + dd, LINE[1][1], "vest" if i else (-30, -8, 30, 8), "happy", (-1, 0), tt, still=True)
    if i <= 1:
        for x_ in (LINE[0][0] + 40, LINE[2][0] + 46):
            ds._lines(k, [(x_, F - 60, x_ + 16, F - 60), (x_ + 2, F - 30, x_ + 20, F - 30)])
    if i >= 1:
        ds._lines(k, [(LINE[1][0] - 40, F - 190, LINE[1][0] - 52, F - 198), (LINE[1][0] + 40, F - 190, LINE[1][0] + 52, F - 198)])


def r_don(s, k, o, t, tt, n):                               # 5.3: one arm sweeps the room open to him
    dp.ceo_chair(k, THR4, CH[1], CH[2])
    pose = seq(t, [(-20, -4, 30, 10), (-60, -14, 30, 10), (-116, -32, 30, 10), (-100, -20, 30, 10), (-104, -24, 30, 10)])
    d = don_at(k, LINE[1][0], LINE[1][1], pose, "happy", (-1, 0), tt)
    A.mouth(k, d["head"], DS_, s.loud("5.3", tt))
    if s.speaking("5.3", tt):
        o["say"] = ("Of course." if s.since("5.3", tt) < 0.72 else "We've been expecting you.", cheek(d, 1), 1, False, 74, 170)


def r_pam_look(s, k, o, t, tt, n):                          # 5.4: her eyes go down to what he is carrying
    look = seq(t, [(-1, 0), (-1, 0.2), (-0.8, 0.6), (-0.7, 0.8)])
    pb.pam(k, PAM[0], PAM[1], PS, "stand", "neutral", look=look, glasses="up")


def i_pass(s, k, c, t, tt, n):                              # 5.4': what she sees; the camera leans in
    z = 1.0 + 0.05 * A.ease(t / 0.7)
    c.save(); c.translate(270, 480); c.scale(z, z); c.translate(-270, -480)
    da.INSERTS["5.4i"](k, c)
    c.restore()


def r_pam_cup(s, k, o, t, tt, n):                           # 5.4'': the mug goes over: nothing. She nearly says it
    ang = seq(t, [0.0, 0.9, 2.1, 2.9, 2.75])
    i = idx(t)
    look = (0.2, 0.9) if i < 6 else ((-0.8, 0.1) if i < 9 else (0.2, 0.9))
    q = pb.pam(k, PAM[0], PAM[1], PS, (-8, 0, 60, 110), "neutral", look=look, glasses="up", mouth=(sc_small() if 6 <= i < 9 else None))
    c = k.c
    hx, hy = q["hands"][1]
    c.save(); c.translate(hx + 4, hy - 20); c.rotate(ang); c.scale(1.5, 1.5)
    c.set_source_rgb(*INK); c.set_line_width(5); c.new_path(); c.arc(12, 1, 7.5, -1.3, 1.3); c.stroke()          # the handle
    c.set_source_rgb(0.36, 0.62, 0.80); c.set_line_width(2.4); c.new_path(); c.arc(12, 1, 7.5, -1.3, 1.3); c.stroke()
    kit.cut(k, [(-10, -12), (10, -12), (9, 12), (-9, 12)], (0.36, 0.62, 0.80), shadow=False, lw=2)
    u = min(1.0, ang / 2.0)                                 # as it tips, its mouth turns to us: white, a dry brown ring, nothing in it
    kit.ellipse(k, 0, -12, 10, 3.2 + 5.5 * u, (0.97, 0.96, 0.92), 3551, shadow=False, lw=1.8)
    if u > 0.5:
        c.set_source_rgb(0.62, 0.48, 0.34); c.set_line_width(1.4); c.save(); c.translate(0, -12); c.scale(1, 0.75); c.new_path(); c.arc(0, 0, 6, 0, 2 * math.pi); c.restore(); c.stroke()
    c.restore()
    if 3 <= i <= 4:                                         # one last drop that isn't there
        ds._lines(k, [(hx + 2, hy + 6, hx + 2, hy + 14)])


def sc_small():
    from dh_anim import M_SMALL
    return M_SMALL


def r_shred(s, k, o, t, tt, n):                             # 6.1: the shredder in plain view, eating a page
    dp.ceo_chair(k, THR4 - 30, CH[1], CH[2])
    shredding(k, n)
    dc.repairman(k, VX, TOUR[1][1], GS, case=True, look=(1, 0.4))
    d = don_at(k, 440, F + 26, "vest", "happy", (-1, 0), tt)
    A.mouth(k, d["head"], DS_, s.loud("6.1a", tt))
    if s.speaking("6.1a", tt):
        o["say"] = ("Complete...", cheek(d, 1), 1, False, 20, 190)


def r_tour(s, k, o, t, tt, n):                              # 6.1': one step sideways and he is in front of it
    dp.ceo_chair(k, THR4 - 30, CH[1], CH[2])
    shredding(k, n)
    dc.repairman(k, VX, TOUR[1][1], GS, case=True, look=(1, 0.1 if idx(t) > 2 else 0.4))
    x = seq(t, [452, 478, 510, 506])
    pose = seq(t, ["vest", (-30, -6, 30, 6), (-58, -10, 58, 10), (-52, -8, 52, 8)])
    d = don_at(k, x, F + 26, pose, "happy", (-1, 0), tt)
    A.mouth(k, d["head"], DS_, s.loud("6.1a", tt))
    if idx(t) < 4:
        ds._lines(k, [(x - 54, F - 4, x - 36, F - 4), (x - 58, F + 10, x - 38, F + 10)])
    if s.speaking("6.1a", tt):
        o["say"] = ("...transparency.", cheek(d, 1), 1, False, 0, 190)


def r_card(s, k, o, t, tt, n):                              # 6.1'': a big gold sticker, slapped over his pass
    i = idx(t)
    dp.ceo_chair(k, THR4 - 30, CH[1], CH[2])
    hit = i >= 3
    with A.About(k.c, VX, TOUR[1][1], 1.0, 1.0, 0):
        dc.repairman(k, VX - (11 if i == 3 else (5 if i == 4 else 0)), TOUR[1][1], GS, case=True, look=(1, 0.1) if i < 5 else (0.2, 1))
    if hit:
        z = seq(t - 3.0 / DPS, [1.25, 0.94, 1.0])
        c = k.c
        cx, cy = VX - 10 * GS, TOUR[1][1] + (ds.co_BT + 80) * GS
        c.save(); c.translate(cx, cy); c.scale(z, z); c.translate(-cx, -cy)
        ds._sticker(k, VX, TOUR[1][1])
        c.restore()
    pose = seq(t, [(-52, -8, 52, 8), (-30, 60, 20, 4), (-120, -30, 8, 0), (-92, -2, 8, 0), (-88, -4, 8, 0)])
    d = don_at(k, seq(t, [506, 498, 486, 480]), F + 26, pose, "happy", (-1, 0), tt)
    A.mouth(k, d["head"], DS_, s.loud("6.1b", tt))
    if i in (3, 4):                                         # the slap: a burst right round the sticker
        cx, cy = VX - 10 * GS, TOUR[1][1] + (ds.co_BT + 80) * GS
        r0, r1 = (34, 54) if i == 3 else (40, 50)
        ds._lines(k, [(cx + math.cos(a_) * r0, cy + math.sin(a_) * r0, cx + math.cos(a_) * r1, cy + math.sin(a_) * r1)
                      for a_ in [j * math.pi / 5 + 0.3 for j in range(10)]])
    if s.speaking("6.1b", tt):
        o["say"] = ("Premium." if s.since("6.1b", tt) < 0.62 else "On us.", cheek(d, 1), 1, False, 0, 190)


def r_robot(s, k, o, t, tt, n):                             # 6.2: helpful; talked over
    dy = -3 if (s.speaking("6.2", tt) and n % 2) else 0
    c = k.c
    c.save(); c.translate(0, dy); da._rb("idle")(k, o); c.restore()
    if s.speaking("6.2", tt):
        o["say"] = ("Premium search is non-functional.", (da.RH[0] + 24, da.RH[1] + 4), 1, False, 20, 200)


def r_life(s, k, o, t, tt, n):                              # 6.3: he doesn't turn his head or lose the smile
    dp.ceo_chair(k, THR4 - 30, CH[1], CH[2])
    d = don_at(k, 480, F + 26, "vest", "happy", (-1, 0), tt)
    A.mouth(k, d["head"], DS_, s.loud("6.3", tt))
    if s.speaking("6.3", tt):
        o["say"] = ("Then make it lifetime.", cheek(d, 1), 1, False, 60, 180)


def r_blank(s, k, o, t, tt, n):                             # 6.4: down at the sticker, then up at Don. Nothing on his face
    lean = seq(t, [0.0, 0.05, 0.09, 0.09, 0.09, 0.05, 0.0])     # v2: he tips forward to look at it, and comes back up
    c = k.c
    c.save(); c.translate(VX, TOUR[1][1] - 150 * GS); c.rotate(lean); c.translate(-VX, -(TOUR[1][1] - 150 * GS))
    dc.repairman(k, VX, TOUR[1][1], GS, case=True, look=(0.15, 1) if lean > 0 else (0.7, 0))
    ds._sticker(k, VX, TOUR[1][1])
    c.restore()


sc.DRAW.update({"5.1": r_door, "5.2": r_line, "5.3": r_don, "5.4": r_pam_look, "5.4''": r_pam_cup, "6.1": r_shred, "6.1'": r_tour,
                "6.1''": r_card, "6.2": r_robot, "6.3": r_life, "6.4": r_blank})
sc.INS["5.4'"] = i_pass
sc.SHIFT["5.4"] = sc.SHIFT["5.4''"] = (22, 0)                 # v2: Pam's bigger mug whole in the frame
sc.SHIFT["6.3"] = (-34, 0)                                 # the price tag whole in his close shot, not cut by the frame
T = sc.T0
sc.sfx = [(fx.tap(120.0), 0.02, 0.7), (fx.tap(120.0), 0.16, 0.7),                    # the knock
          (fx.step(), 0.12, 0.4), (fx.step(), 0.28, 0.4),                           # his steps
          (fx.whoosh(0.2), T["5.2"], 0.45), (fx.whoosh(0.25), T["5.3"] + 0.1, 0.3),
          (fx.tap(300.0), T["5.4''"] + 0.25, 0.4),                                   # the empty mug
          (fx.whirr(2.3), T["6.1"], 0.16), (fx.whirr(1.8), T["6.1"] + 2.2, 0.12),   # the shredder, under the tour
          (fx.step(), T["6.1'"] + 0.12, 0.4),
          (fx.pop(), T["6.1''"] + 0.25, 0.9), (fx.step(), T["6.1''"] + 0.25, 0.6)]                                        # the sticker

if __name__ == "__main__":
    sc.main(2 if (len(sys.argv) > 1 and sys.argv[1] == "hi") else 1)
