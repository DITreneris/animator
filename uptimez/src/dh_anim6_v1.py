"""DADDY'S HOME (episode 12): the animation pass, scene 6 "Mom" (scene sheet v5, 6.6 s). The engine is dh_anim.Scene.
Between and inside the key drawings: the filter lifted off his head, his recoil and surrender, her thumb, the tissue, the
zip pulled up to his chin as her line ends, Sofía walking back in, Pam planted and labelled, Sofía's smile going tight.
  KOKORO_DIR=/tmp/kokoro python3 dh_anim6.py [hi]  ->  ../daddys-home/dh_s6_anim_v1.mp4, dh_s6_anim_v1_strip.png"""
import math
import sys
import kit
import fs_storyboard as sb
import dh_props as dp
import dh_poses as dq
import dh_layout as dl
import dh_animatic as da
import dh_scenes as ds
import dh_anim1 as A
import cs_sfx as fx
from dh_anim import Scene, seq, idx, don_at, cheek, DPS, DS_, F, CH
from kit import INK

SS, PS, MS = ds.SS, ds.PS, ds.MS
THR5, DON6, MOM6, SOF6, LINE6 = ds.THR5, ds.DON6, ds.MOM6, ds.SOF6, ds.LINE6
sdh, _mb = ds.sdh, ds._mb
HEAD = (DON6[0], DON6[1] - 302 * DS_)

sc = Scene(6, "v1", ds.S6, takes=[("8.2", "8.2'", 0.04), ("8.3", "8.3", 0.06)])


def r_peel(s, k, o, t, tt, n):                              # 8.2: she lifts the filter off him between two fingers
    u = seq(t, [0.0, 0.45, 0.85, 1.0])
    dp.ceo_chair(k, THR5, CH[1], CH[2])
    d = sb.don(k, DON6[0], DON6[1], DS_, "stand", "neutral", look=(-0.7, -0.5))
    dp.coffee_run(k, d["head"], DS_)
    sb.mfs.mom(k, MOM6[0], MOM6[1], MS, ds._mom_pose("peel", _mb.wipe_at(96, _mb.HY - 40)), "glare", look=(0.8, -0.5), bag=False)
    dp.wet_filter(k, d["head"][0] + 4 - 44 * u, d["head"][1] - 25 - 15 * u, 0.80 - 0.14 * u, -0.16 - 0.39 * u, drips=u > 0.3)
    if 0 < u < 1:
        ds._lines(k, [(d["head"][0] - 8, d["head"][1] - 40, d["head"][0] - 4, d["head"][1] - 52), (d["head"][0] + 10, d["head"][1] - 40, d["head"][0] + 14, d["head"][1] - 52)])


def r_lick(s, k, o, t, tt, n):                              # 8.2': the thumb is coming; he goes back on his heels
    rot = seq(t, [0.03, 0.09, 0.11, 0.09])
    dp.ceo_chair(k, THR5, CH[1], CH[2])
    c = k.c
    c.save(); c.translate(DON6[0] + 4, DON6[1]); c.rotate(rot); c.translate(-DON6[0] - 4, -DON6[1])
    d = sb.don(k, DON6[0] + 4, DON6[1], DS_, (-50, -168, 50, 168), "shock", look=(-1, 0))
    A.fear(k, d["head"], DS_, "hope", s.loud("8.2", tt))
    dp.coffee_run(k, d["head"], DS_)
    c.restore()
    sb.mfs.mom(k, MOM6[0] + seq(t, [0, 4, 8, 10]), MOM6[1], MS, "lick", "sweet", look=(0.8, -0.3), bag=False)
    dp.wet_filter(k, MOM6[0] - 34, F - 86, 0.6, 0.4)
    if s.speaking("8.2", tt):
        o["say"] = ("Mom! I'm...", (d["head"][0] + 30, d["head"][1] + 16), 1, False, 60, 170)


def r_thumb(s, k, o, t, tt, n):                             # 8.2'': it is on his scalp before he has finished the sentence
    c = k.c
    c.save(); c.translate(1.5 if n % 2 else -1.5, 0); ds.s6_thumb(k, o); c.restore()
    A.mouth(k, HEAD, DS_, s.loud("8.2", tt))
    if s.speaking("8.2", tt):
        o["say"] = ("...the CEO!", (HEAD[0] + 27, HEAD[1] + 16), 1, False, 60, 170)


def r_scrub(s, k, o, t, tt, n):                             # 8.2''': one big wipe at the stain
    c = k.c
    c.save(); c.translate(0, 2 if n % 2 else -2); ds.s6_scrub(k, o); c.restore()


def r_zip(s, k, o, t, tt, n):
    """8.3: her fist goes to the bottom of his zip while she says it, and comes up to his chin in three drawings as the
    line ends. Only then do his shoulders go up and his mouth shut."""
    end = s.AT["8.3"] + len(s.WAV["8.3"]) / 48000.0
    end -= 0.50                                             # the pull is over on "Donnie", so the zipped Don is held to the cut
    u = min(1.0, max(0.0, (tt - (end - 0.30)) / 0.25))      # 0: at his belt .. 1: at his chin
    u = (0.0, 0.4, 0.8, 1.0)[min(3, int(u * 3 + 1e-6))]
    done = u >= 1.0
    c = k.c
    if not done:
        dp.ceo_chair(k, THR5, CH[1], CH[2])
        d = sb.don(k, DON6[0], DON6[1], DS_, (-22, 6, 22, -6), "neutral", look=(-0.5, 0.6))
        hx, hy = d["head"]
        fx_, fy_ = hx - 2, hy + 34 + (1 - u) * 78
        kit.cut(k, [(fx_ - 92, fy_ + 64), (fx_ - 24, fy_ + 6), (fx_ - 10, fy_ + 22), (fx_ - 78, fy_ + 82)], sb.mfs.TEAL, shadow=False, lw=2.4)
        kit.cut(k, [(fx_ - 30, fy_ + 10), (fx_ - 20, fy_ + 2), (fx_ - 6, fy_ + 18), (fx_ - 16, fy_ + 27)], sb.mfs.MUSTARD, shadow=False, lw=2)
        kit.ellipse(k, fx_ - 6, fy_ + 6, 12, 11, ds.SKIN_M, 3600, shadow=False, lw=2.2)
        if u > 0:
            ds._lines(k, [(hx + 8, fy_ + 44, hx + 8, fy_ + 22), (hx + 15, fy_ + 40, hx + 15, fy_ + 26)])
    else:
        after = int((tt - end + 0.05) * DPS)
        with A.About(c, DON6[0], DON6[1], 1.0, (1.04, 0.98, 1.0)[min(2, max(0, after))]):
            ds.s6_zip(k, o)
    if s.speaking("8.3", tt):
        o["say"] = ("Then stand like one, Donnie.", (HEAD[0] - 80, HEAD[1] - 34), -1, False, 0, 150)     # she is off the frame's left edge: a short tail to it


def r_sofia(s, k, o, t, tt, n):                             # 8.4a: she walks back in, changed, the CV carried high
    dx = seq(t, [44, 22, 6, 0])
    bob = seq(t, [0, -5, 0, 0])
    with A.About(k.c, SOF6[0], SOF6[1], 1.0, 1.0, bob):
        sdh.sofia(k, SOF6[0] + dx, SOF6[1], SS, "lapel", "interested", look=(-0.8, -0.3))
        sdh.cv(k, SOF6[0] + dx - 50, F - 92, 0.62, -0.12)
    if dx:
        ds._lines(k, [(SOF6[0] + dx + 36, F - 4, SOF6[0] + dx + 52, F - 4), (SOF6[0] + dx + 38, F + 8, SOF6[0] + dx + 56, F + 8)])


_hs0 = ds._hand_sticker


def r_place(s, k, o, t, tt, n):                             # 8.4b: Mom plants Pam beside Don and slaps the label on her
    i = idx(t)
    ds._hand_sticker = (lambda *a, **kw: None) if i < 2 else (lambda k_, x, feet, slap=False: _hs0(k_, x, feet, slap=(i in (2, 3))))
    try:
        c = k.c
        c.save(); c.translate(seq(t, [10, -3, 0]), 0); ds.s6_place(k, o); c.restore()
    finally:
        ds._hand_sticker = _hs0


def r_left(s, k, o, t, tt, n):                              # 8.4c: the place is taken; the smile stays on, the eyes stop
    i = idx(t)
    sdh.sofia(k, SOF6[0], SOF6[1], SS, "stand", "interested" if i < 1 else "tight", look=(-1, 0))
    sdh.cv(k, SOF6[0] - 50, F - 84 + seq(t, [-8, 0, 3, 5]), 0.6, 0.1 + 0.04 * min(3, i))


def i_clock(s, k, c, t, tt, n):                             # 8.1: 16:59. One minute
    da.INSERTS["8.1"](k, c)
    if (n // 3) % 2:                                        # the colon blinks
        c.set_source_rgb(0.05, 0.07, 0.10); c.rectangle(250, 400, 44, 140); c.fill()


sc.DRAW.update({"8.2": r_peel, "8.2'": r_lick, "8.2''": r_thumb, "8.2'''": r_scrub, "8.3": r_zip, "8.4a": r_sofia, "8.4b": r_place, "8.4c": r_left})
sc.INS["8.1"] = i_clock
T = sc.T0
_zip_at = sc.AT["8.3"] + len(sc.WAV["8.3"]) / 48000.0 - 0.80
sc.sfx = [(fx.beep(880.0, 0.12), T["8.1"] + 0.05, 0.4),
          (fx.rustle(0.25), T["8.2"] + 0.08, 0.5),
          (fx.whoosh(0.2), T["8.2'"], 0.3),
          (fx.scratch(0.3), T["8.2''"] + 0.05, 0.25), (fx.rustle(0.3), T["8.2'''"], 0.5),
          (fx.sweep(300.0, 1400.0, 0.25), _zip_at, 0.6), (fx.beep(1500.0, 0.10), _zip_at + 0.27, 0.35),   # ZZZIP, eek
          (fx.step(), T["8.4a"] + 0.08, 0.35), (fx.step(), T["8.4a"] + 0.25, 0.35),
          (fx.whoosh(0.2), T["8.4b"], 0.4), (fx.pop(), T["8.4b"] + 0.17, 0.7)]

if __name__ == "__main__":
    sc.main(2 if (len(sys.argv) > 1 and sys.argv[1] == "hi") else 1)
