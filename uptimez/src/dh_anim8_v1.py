"""DADDY'S HOME (episode 12): the animation pass, scene 8 "Find My Money" (scene sheet v4, 17.9 s), the last. The engine is
dh_anim.Scene. Between and inside the key drawings: the CV pocketed, the green star, Father's mouth and his one eyebrow,
Don's nod, the bodyguard's snap, the robot's slow turn and its leans, Don's shuffles, the viewfinder closing on the phone
(FOUND), the five held shots of the freeze (nothing moves in them), the button, the throne ringing, and the last frame,
which is frame 0: the phone buzzing on the gold arm.
  KOKORO_DIR=/tmp/kokoro python3 dh_anim8.py [hi]  ->  ../daddys-home/dh_s8_anim_v1.mp4, dh_s8_anim_v1_strip.png"""
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
from dh_anim7 import father_mouth
from kit import INK

FS, GS, SS, PS, MS = ds.FS, ds.GS, ds.SS, ds.PS, ds.MS
FA2, GU7, SOF6 = ds.FA2, ds.GU7, ds.SOF6
HDF = dl.hd(FA2[0], FA2[1], FS)

sc = Scene(8, "v1", ds.S8, takes=[("10.1", "10.1", 0.04), ("10.2", "10.2", 0.04), ("10.4a", "10.4a", 0.02), ("11.6", "11.6", 0.30)])


def say_f(txt):                                            # Father's lines: dark, from his mouth
    return (txt, (HDF[0] - 26, HDF[1] + 28 * FS), -1, True, -20, 170)     # over his own head, clear of the price tag


def r_cv(s, k, o, t, tt, n):                               # 9.6: she is already on him, the CV up at his chest
    c = k.c
    c.save(); c.translate(seq(t, [10, 3, 0]), 0); ds.s8_cv(False)(k, o); c.restore()


def r_cv2(s, k, o, t, tt, n):                              # 9.6': one bare hand has it half into his pocket
    c = k.c
    c.save(); c.translate(0, seq(t, [-4, 0])); ds.s8_cv(True)(k, o); c.restore()


def i_star(s, k, c, t, tt, n):                             # 10.1: the green star, over his shoulder; the camera leans in
    z = 1.0 + 0.06 * A.ease(t / 2.3)
    c.set_source_rgb(0.05, 0.07, 0.10); c.paint()
    c.save(); c.translate(270, 480); c.scale(z, z); c.translate(-270, -480)
    dp.star_screen(k, 270, 470, 500, green=True)
    dp._T(c, "1 / 5", 270, 600, 40, col=(1, 1, 1))
    c.restore()
    if s.speaking("10.1", tt):                              # he is off the frame, bottom left: the tail goes to the corner
        return ("I prefer green in cash.", (40, 330), -1, True, False, 150)   # at the top, as every line; the tail to his side of the frame
    return None


def r_ftalk(face, key, lines):
    def f(s, k, o, t, tt, n):
        ds.s8_father("hard")(k, o)
        father_mouth(k, HDF, s.loud(key, tt))
        if face == "brow":                                  # the eyebrow goes up over two drawings and stays
            u = seq(t, [0.5, 1.0])
            c = k.c
            c.save(); c.translate(HDF[0], HDF[1]); c.scale(FS, FS)
            kit.ellipse(k, -17, -20, 12, 6, (0.86, 0.68, 0.56), 4310, shadow=False, lw=0)
            c.set_source_rgb(0.55, 0.55, 0.58); c.set_line_width(6); c.set_line_cap(1)
            c.move_to(-28, -18 - 9 * u); c.curve_to(-20, -26 - 12 * u, -12, -26 - 12 * u, -6, -20 - 6 * u); c.stroke()
            c.restore()
        if s.speaking(key, tt):
            o["say"] = say_f(lines(s.since(key, tt)))
    return f


def r_nod(s, k, o, t, tt, n):                              # 10.3: he nods; the thumb is still up
    c = k.c
    c.save(); c.translate(0, seq(t, [0, 5, 9, 4, 0, 4, 0])); ds.s8_nod(k, o); c.restore()


def r_snap(s, k, o, t, tt, n):                             # 10.4b: the bodyguard snaps to attention; Sofía leaves the floor
    c = k.c
    c.save(); c.translate(0, seq(t, [-6, 3, 0])); ds.s8_snap(k, o); c.restore()


def r_turn(s, k, o, t, tt, n):                             # 10.5a: its head turns, slowly, still smiling
    da._rb("idle" if t < 0.42 else "turn")(k, o)


def r_pov(x0, x1, face, sweat, lock_at=None):
    def f(s, k, o, t, tt, n):
        u = A.ease(min(1.0, t / 0.25))
        dx = x0 + (x1 - x0) * u
        locked = lock_at is not None and t >= lock_at
        ds.s8_pov(dx, face=face, sweat=sweat, lock=locked)(k, o)
    return f


def r_still(fn):                                           # the freeze: nothing moves
    def f(s, k, o, t, tt, n):
        fn(k, o)
    return f


def r_call(s, k, o, t, tt, n):                             # 11.6: one button; the throne rings behind Don; "Answer it."
    c = k.c
    ring = (n % 2 == 0)
    a0 = ds._arm_phone
    ds._arm_phone = lambda k_, **kw: a0(k_, ring=ring)        # it flashes: lit, dark, lit
    try:
        ds.s8_call(k, o)
    finally:
        ds._arm_phone = a0
    father_mouth(k, HDF, s.loud("11.6", tt))
    if s.speaking("11.6", tt):
        o["say"] = say_f("Answer it.")


def i_end(s, k, c, t, tt, n):                              # 11.7: frame 0. The phone on the gold arm, DAD, buzzing
    dp.dad_phone(k, True, buzz=(1.0 if n % 2 else -1.0))
    return None


sc.DRAW.update({"9.6": r_cv, "9.6'": r_cv2,
                "10.2": r_ftalk("talk", "10.2", lambda u: "You said it finds anything."),
                "10.3": r_nod,
                "10.4a": r_ftalk("hard", "10.4a", lambda u: "Good."),
                "10.4a'": r_ftalk("brow", "10.4a", lambda u: "Good." if u < 1.0 else "Find. My money."),
                "10.4b": r_snap, "10.5a": r_turn,
                "10.5b": r_pov(0, 0, "happy", 0), "10.6a": lambda s, k, o, t, tt, n: da._rb("lean_r")(k, o),
                "10.6b": r_pov(0, 30, "neutral", 1), "10.6c": lambda s, k, o, t, tt, n: da._rb("lean_l")(k, o),
                "10.6d": r_pov(30, -44, "panic", 2, lock_at=0.25),
                "11.1": r_still(ds.s8_father("hard", look=(1, 0))), "11.2": r_still(ds.s8_pov(0, brackets=False, sweat=2)),
                "11.3": r_still(ds.s8_mom), "11.4": r_still(ds.s8_pam), "11.5": r_still(ds.s8_vis),
                "11.6": r_call})
sc.INS.update({"10.1": i_star, "11.7": i_end})
T = sc.T0
sc.sfx = [(fx.rustle(0.3), T["9.6'"] + 0.05, 0.6),                                   # the CV, into the pocket
          (fx.chime(), T["10.1"] + 0.02, 0.25),
          (fx.step(), T["10.4b"] + 0.02, 0.7),                                         # the snap to attention
          (fx.whirr(0.9), T["10.5a"] + 0.05, 0.2),                                     # the head turning
          (fx.whirr(0.3), T["10.6a"], 0.18), (fx.step(), T["10.6b"] + 0.05, 0.35),
          (fx.whirr(0.3), T["10.6c"], 0.18), (fx.step(), T["10.6d"] + 0.05, 0.4),
          (fx.beep(1200.0, 0.18), T["10.6d"] + 0.25, 0.6),                             # FOUND
          (fx.tap(700.0), T["11.6"] + 0.12, 0.5),                                      # the button
          (fx.ring(0.45), T["11.6"] + 0.20, 0.45), (fx.ring(0.45), T["11.6"] + 0.85, 0.45),
          (fx.ring(0.45), T["11.7"] + 0.05, 0.5)]                                      # and frame 0 rings on into the loop

if __name__ == "__main__":
    sc.main(2 if (len(sys.argv) > 1 and sys.argv[1] == "hi") else 1)
