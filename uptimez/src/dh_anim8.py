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

# v2 (22 Nov, after the scene 8 review, Tomas: "let it find it, FOUND"): the robot's view is marked as its camera (tint,
# lines, REC, HR CAM) so the corners read as a viewfinder; FOUND locks on the price tag, $49,999, the answer to "Find. My
# money."; in 11.6 Father's phone is out to the side and big, the phone on the throne's arm is big and lit with DAD on it,
# and Don's eyes slide down to it without turning his head. v1: dh_anim8_v1.py
sc = Scene(8, "v2", ds.S8, takes=[("10.1", "10.1", 0.04), ("10.2", "10.2", 0.04), ("10.4a", "10.4a", 0.02), ("11.6", "11.6", 0.30)])


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


POV8 = ds.POV8
TK = (ds.THR5 - 52 * CH[2], CH[1] - 404 * CH[2])             # the tag's knot on the crown, in the room
TAG_BOX = (TK[0] - 46 * CH[2] - 7, TK[1] + 30 * CH[2] - 7, 92 * CH[2] + 14, 54 * CH[2] + 14)


def hr_cam(k, n):
    """v2: what the robot sees is its camera: a cold tint, scan lines, REC and HR CAM in the corner (world units, POV8's frame)."""
    c = k.c
    hw, hh = 270 / POV8[2], 480 / POV8[2]
    x0, y0 = POV8[0] - hw, POV8[1] - hh
    c.set_source_rgba(0.35, 0.75, 1.0, 0.10); c.rectangle(x0, y0, 2 * hw, 2 * hh); c.fill()
    c.set_source_rgba(0.05, 0.10, 0.15, 0.07); c.set_line_width(1.0)
    yy = y0
    while yy < y0 + 2 * hh:
        c.move_to(x0, yy); c.line_to(x0 + 2 * hw, yy); c.stroke(); yy += 3.2
    tx, ty = x0 + 26 / POV8[2] * 2.2, y0 + 128 / POV8[2]
    if (n // 4) % 2 == 0:
        kit.ellipse(k, tx, ty, 4.2, 4.2, (0.92, 0.12, 0.12), 4400, shadow=False, lw=0)
    kit.text(k, "REC", tx + 18, ty + 3.5, 9, (0.92, 0.12, 0.12))
    kit.text(k, "HR CAM", POV8[0] + hw - 34, ty + 3.5, 9, (0.20, 0.85, 0.40))


def found(k, u):
    """FOUND: the viewfinder closes in on the price tag (u 0..1), then locks, green."""
    c = k.c
    x, y, w, h = TAG_BOX
    g = 1.0 + 1.6 * (1 - u)
    cx, cy = x + w / 2, y + h / 2
    w2, h2 = w * g, h * g
    c.set_source_rgb(0.20, 0.85, 0.40); c.set_line_width(3.4 if u >= 1 else 2.6); c.set_line_cap(1)
    if u >= 1:
        c.rectangle(cx - w2 / 2, cy - h2 / 2, w2, h2); c.stroke()
        c.rectangle(cx - 34, cy - h2 / 2 - 20, 68, 17); c.fill()
        kit.text(k, "FOUND", cx, cy - h2 / 2 - 7.5, 11, (0.03, 0.10, 0.05))
    else:
        for sx in (-1, 1):
            for sy in (-1, 1):
                ex, ey = cx + sx * w2 / 2, cy + sy * h2 / 2
                c.move_to(ex - sx * 12, ey); c.line_to(ex, ey); c.line_to(ex, ey - sy * 12); c.stroke()


def r_pov(x0, x1, face, sweat, lock_at=None):
    def f(s, k, o, t, tt, n):
        u = A.ease(min(1.0, t / 0.25))
        dx = x0 + (x1 - x0) * u
        searching = lock_at is not None and t >= lock_at - 0.17
        ds.s8_pov(dx, brackets=not searching, face=face, sweat=sweat, lock=False)(k, o)
        if searching:
            found(k, min(1.0, (t - (lock_at - 0.17)) / 0.17))
        hr_cam(k, n)
    return f


def r_still(fn):                                           # the freeze: nothing moves
    def f(s, k, o, t, tt, n):
        fn(k, o)
    return f


def ringing_phone(k, lit, n):
    """v2: Don's phone on the throne's gold arm, big enough to read: lit, DAD on it, buzzing marks."""
    c = k.c
    x, y = ds.ARM8
    c.save(); c.translate(x + (1.5 if n % 2 else -1.5), y); c.rotate(-0.08)
    kit.rect(k, -22, -9, 44, 16, (0.06, 0.06, 0.08), 3900, lw=2)
    c.set_source_rgb(*((0.55, 0.80, 1.0) if lit else (0.20, 0.22, 0.28))); c.rectangle(-19, -7, 38, 11); c.fill()
    if lit:
        kit.text(k, "DAD", 0, 2.5, 8, (0.05, 0.08, 0.14))
    c.restore()
    if lit:
        c.set_source_rgb(1, 1, 1); c.set_line_width(2.6); c.set_line_cap(1)
        for sx in (-1, 1):
            for r_ in (28, 37):
                c.new_path(); c.arc(x, y - 2, r_, (-0.55 if sx > 0 else math.pi - 0.55), (0.55 if sx > 0 else math.pi + 0.55)); c.stroke()


def r_call(s, k, o, t, tt, n):
    """11.6 (v2): Father holds his phone out to the side, clear of Don, and presses one button. Behind Don, on the gold arm,
    his phone lights up: DAD. Don's eyes go down to it; his head doesn't turn. "Answer it." """
    i = idx(t)
    pressed = i >= 2
    dp.ceo_chair(k, ds.THR5, CH[1], CH[2])
    ds._arm_phone_off = True
    f_ = dc.father(k, FA2[0], FA2[1], FS, pose=(-20, -130, 8, 0), face="hard", look=(1, 0))
    hx, hy = f_["hands"][0]
    c = k.c
    c.save(); c.translate(hx - 4, hy - 30)
    kit.rect(k, -14, -26, 28, 50, (0.06, 0.06, 0.08), 3801, lw=2.2)
    c.set_source_rgb(0.55, 0.80, 1.0); c.rectangle(-11, -22, 22, 40); c.fill()
    kit.ellipse(k, 0, 8, 7, 7, (0.20, 0.75, 0.30), 3802, shadow=False, lw=1.4)                  # the call button
    kit.ellipse(k, 6 if not pressed else 1, 10 if not pressed else 8, 7, 6, (0.86, 0.68, 0.56), 3803, shadow=False, lw=1.8)   # his thumb
    c.restore()
    if i == 2:
        ds._lines(k, [(hx - 22, hy - 44, hx - 30, hy - 52), (hx + 14, hy - 44, hx + 22, hy - 52)])
    look = (1, 0.15) if i < 4 else ((0.6, 0.7) if i < 6 else (0.85, 0.9))
    d = dq.don_zipped(k, ds.DON6[0] - 6, ds.DON6[1] + 9, DS_, face="shock", look=look)
    A.fear(k, d["head"], DS_, "o")
    ds._sweat8(k, d["head"], 2)
    ringing_phone(k, pressed and (n % 3 != 2), n)
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
                "10.6b": r_pov(0, -30, "neutral", 1), "10.6c": lambda s, k, o, t, tt, n: da._rb("lean_l")(k, o),
                "10.6d": r_pov(-30, 46, "panic", 2, lock_at=0.25),
                "11.1": r_still(ds.s8_father("hard", look=(1, 0))), "11.2": r_still(ds.s8_pov(0, brackets=False, sweat=2)),
                "11.3": r_still(ds.s8_mom), "11.4": r_still(ds.s8_pam), "11.5": r_still(ds.s8_vis),
                "11.6": r_call})
sc.INS.update({"10.1": i_star, "11.7": i_end})
sc.shot["11.6"] = dict(sc.shot["11.6"], cam=(382, 710, 2.05), ymin=100)     # v2: Father's phone and Don's, both whole in the frame
T = sc.T0
sc.sfx = [(fx.rustle(0.3), T["9.6'"] + 0.05, 0.6), (fx.beep(1500.0, 0.06), T["10.6d"] + 0.12, 0.3),                                   # the CV, into the pocket
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
