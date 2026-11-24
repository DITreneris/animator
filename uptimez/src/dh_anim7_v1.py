"""DADDY'S HOME (episode 12): the animation pass, scene 7 "The Arrival" (scene sheet v5, 10.05 s). The engine is
dh_anim.Scene. Between and inside the key drawings: the fist knocking on the glass, the line-up not breathing, the door
open, the bodyguards stepping apart in step, Father's one step in, the scanner beam sweeping, Don's thumb going up and
staying there, shaking, after "Approved.", the robot's tick and its happy hop.
  KOKORO_DIR=/tmp/kokoro python3 dh_anim7.py [hi]  ->  ../daddys-home/dh_s7_anim_v1.mp4, dh_s7_anim_v1_strip.png"""
import math
import sys
import kit
import fs_storyboard as sb
import dh_cast as dc
import dh_props as dp
import dh_poses as dq
import dh_layout as dl
import dh_animatic as da
import dh_scenes as ds
import dh_anim1 as A
import cs_sfx as fx
from dh_anim import Scene, seq, idx, don_at, cheek, DPS, DS_, F, CH
from kit import INK

FS, GS, PS, MS = ds.FS, ds.GS, ds.PS, ds.MS
FA1, FA2, LINE6, THR5, DON6 = ds.FA1, ds.FA2, ds.LINE6, ds.THR5, ds.DON6

sc = Scene(7, "v1", ds.S7, takes=[("9.3", "9.3", 0.04), ("9.4", "9.4'", 0.12), ("9.5", "9.5", 0.06)])


def i_knock(s, k, o, t, tt, n):                             # 9.1: one fist on the glass: knock, knock, knock
    pass


def r_door(s, k, o, t, tt, n):
    """9.1: the door, shut, two shapes behind the glass; the fist knocks three times, one impact star at a time."""
    c = k.c
    c.push_group()
    dl.s9_1(k, o)
    pat = c.pop_group()
    c.set_source_rgba(0.16, 0.20, 0.27, 0.62); c.mask(pat)
    knocks = [i for i, at_ in enumerate((0.05, 0.27, 0.49)) if t >= at_]
    hit = any(at_ <= t < at_ + 0.09 for at_ in (0.05, 0.27, 0.49))
    fx_, fy_ = 128, 618 + (0 if hit else -10)
    c.set_source_rgba(0.10, 0.13, 0.19, 0.80); c.set_line_width(22); c.set_line_cap(1)
    c.move_to(92, 668); c.line_to(fx_ - 4, fy_ + 6); c.stroke()
    c.arc(fx_, fy_, 17, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(*INK)
    for j in knocks:                                        # each knock leaves its star, a smaller one each time, further up
        kx, ky, r0, r1, lw = ((fx_, 618, 22, 38, 3.6), (fx_ + 46, 578, 9, 19, 2.8), (fx_ + 74, 544, 6, 13, 2.2))[j]
        c.set_line_width(lw)
        for m in range(10):
            a_ = 2 * math.pi * m / 10 + 0.2
            c.move_to(kx + math.cos(a_) * r0, ky + math.sin(a_) * r0); c.line_to(kx + math.cos(a_) * r1, ky + math.sin(a_) * r1); c.stroke()


def r_line(s, k, o, t, tt, n):                              # 9.1r: three pairs of eyes on the door; not one of them breathes
    c = k.c
    c.save(); c.translate(0, -2 if idx(t) == 0 else 0); ds.s7_line(k, o); c.restore()
    hx, hy = LINE6[0][0], LINE6[0][1] - 302 * DS_
    A.sweat(k, (hx, hy + 8), DS_, min(1.0, t / 0.5), side=1)


def r_open(s, k, o, t, tt, n):                              # 9.1b: open. Two bodyguards, shoulder to shoulder. Held in silence
    dl.s9_1(k, o)


def r_gap(s, k, o, t, tt, n):                               # 9.2: they step apart together; in the gap, smaller than either: Father
    u = A.ease(min(1.0, t / 0.33))
    xl, xr = 70 + (ds.GAP7[0] - 70) * u, 180 + (ds.GAP7[1] - 180) * u
    dl._guards(k, xl, xr)
    if u > 0.3:
        dc.father(k, 125, F + 22, FS, look=(0.3, 0.1))
    if 0 < u < 1:
        ds._lines(k, [(xl + 36, F - 40, xl + 22, F - 40), (xr - 36, F - 40, xr - 22, F - 40)])


def r_step(s, k, o, t, tt, n):                              # 9.2': one slow step into the room
    ds.s7_step(k, o) if idx(t) >= 2 else ds.s7_gap(k, o)


def r_scan(s, k, o, t, tt, n):                              # 9.3: the beam sweeps down his chest; he lets it
    dc.father(k, FA1[0], FA1[1], FS, look=(1, 0))
    c = k.c
    rx, ry = o["robot"]["screen"]
    yy = FA1[1] - 270 * FS + 140 * FS * (0.5 + 0.5 * math.sin(tt * 3.2))
    c.set_source_rgba(0.95, 0.15, 0.15, 0.30); c.move_to(rx - 14, ry); c.line_to(FA1[0] + 30, yy - 14); c.line_to(FA1[0] + 30, yy + 14); c.close_path(); c.fill()
    c.set_source_rgba(0.95, 0.15, 0.15, 0.75); c.set_line_width(3); c.move_to(rx - 14, ry); c.line_to(FA1[0] + 30, yy); c.stroke()
    if s.speaking("9.3", tt):
        txt = "Visitor detected." if s.since("9.3", tt) < 1.05 else "Human approval required."
        o["say"] = (txt, (rx + 18, ry), 1, False, 20, 190)


def father_mouth(k, hd, op):
    if op > 0:
        x, y = hd[0], hd[1] + 28 * FS
        kit.ellipse(k, x, y, 15 * FS, 9 * FS, (0.86, 0.68, 0.56), 4300, shadow=False, lw=0)
        kit.ellipse(k, x, y, (8 + 2 * op) * FS, (2 + 6 * op) * FS, (0.30, 0.07, 0.07), 4301, shadow=False, lw=1.8)


def r_offer(s, k, o, t, tt, n):                             # 9.4: Don opens his mouth and the thumb goes up
    i = idx(t)
    c = k.c
    if i < 3:                                               # the arm on its way up
        dp.ceo_chair(k, THR5, CH[1], CH[2])
        dc.father(k, FA2[0], FA2[1], FS, face="hard", look=(1, 0))
        dq.don_zipped(k, DON6[0], DON6[1], DS_, pose=seq(t, [(-30, -10, 10, 0), (-80, -26, 10, 0), (-160, -44, 10, 0)]), face="happy", look=(-1, 0))
    else:
        ds.s7_thumb(True)(k, o)


def r_approved(s, k, o, t, tt, n):                          # 9.4': "Approved." The smile dies; the thumb stays up, shaking
    c = k.c
    c.save(); c.translate(0, 0)
    ds.s7_thumb(False)(k, o)
    c.restore()
    hd = (FA2[0], FA2[1] - 302 * FS)
    father_mouth(k, hd, s.loud("9.4", tt))
    if s.speaking("9.4", tt):
        o["say"] = ("Approved.", (hd[0] - 26, hd[1] + 28 * FS), -1, True, -20, 170)     # over his own head, clear of the price tag


def r_tick(s, k, o, t, tt, n):                              # 9.5: the green tick; it is delighted
    c = k.c
    dy = -3 if (s.speaking("9.5", tt) and n % 2) else 0
    c.save(); c.translate(0, dy); da._rb("tick")(k, o); c.restore()
    if s.speaking("9.5", tt):
        o["say"] = ("Welcome...", (da.RH[0] + 24, da.RH[1] + 4), 1, False, 20, 200)


def r_hop(s, k, o, t, tt, n):                               # 9.5': a happy little hop on its wheel
    c = k.c
    up = seq(t, [0, 10, 18, 14, 4, 0, 6, 2, 0])
    c.save(); c.translate(0, -up + 15); ds.s7_hop(k, o); c.restore()
    if s.speaking("9.5", tt):
        o["say"] = ("...majority shareholder.", (da.RH[0] + 24, da.RH[1] + 4 - up), 1, False, 20, 200)


sc.DRAW.update({"9.1": r_door, "9.1r": r_line, "9.1b": r_open, "9.2": r_gap, "9.2'": r_step, "9.3": r_scan, "9.4": r_offer, "9.4'": r_approved,
                "9.5": r_tick, "9.5'": r_hop})
T = sc.T0
sc.sfx = [(fx.tap(90.0), T["9.1"] + at_, 0.9) for at_ in (0.05, 0.27, 0.49)] + [
    (fx.door(0.5), T["9.1b"], 0.6),
    (fx.step(), T["9.2"] + 0.05, 0.5), (fx.step(), T["9.2"] + 0.06, 0.5),             # they step apart, in step
    (fx.step(), T["9.2'"] + 0.17, 0.8),                                               # his one step
    (fx.sweep(900.0, 600.0, 0.6), T["9.3"] + 0.05, 0.25),                             # the scanner
    (fx.whoosh(0.2), T["9.4"] + 0.05, 0.3),
    (fx.chime(), T["9.5"] + 0.03, 0.5), (fx.beep(990.0, 0.08), T["9.5'"] + 0.08, 0.3)]

if __name__ == "__main__":
    sc.main(2 if (len(sys.argv) > 1 and sys.argv[1] == "hi") else 1)
