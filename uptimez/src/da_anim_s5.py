"""THE DOUBLE AGENT (episode 15): stage 7, scene 5 (5.1-5.4, 0:34.44-0:43.44), the 540 preview. Tomas 28 Nov
(/grill-me): 5.2 animated up to its locked still; in 5.3 the cup flies off the saucer and the saucer stays in his hand;
5.4 Mom's fists on her hips; the noir sting for 5.1 now, synthesized.

  5.1  S9 C: through the glass, her mustard mug on Father's table in a pool of light; a slow push in; the sting
  5.2  S3 MC: the cup rattles on its saucer, slops; he lifts it, sips, his eyes on the office; he notices how it looks
       and lifts his little finger (da_s52_anim: the last 0.6 s is the locked still)
  5.3  S1 W: he charges at the glass, the cup on its saucer on his palm; his foot lands on the robot's clips, they
       spray; all of him in the air, turning; the cup flies off the saucer into its own puddle; he lands and slides
       on his back and stops dead at his own tape, the empty saucer still up on his palm
  5.3b I: the cup tumbling, the coffee's arc, the splash right at the tape, not over it
  5.4  S7 M: Mom slides in round the counter's end and plants herself between him and the glass, fists on her
       hips, chin up; Don shrinks back; the robot freezes, a clip held up in its gripper, its head tips

  python3 da_anim_s5.py   ->  ../the-double-agent/da_anim_s5_v1.mp4, da_anim_s5_v1_8fps.png
"""
import math
import os
import sys

import cairo

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import da_cups as cu                                               # noqa: E402
import da_anim_s1 as A                                             # noqa: E402
import da_anim_s3 as C                                             # noqa: E402
import da_layouts as L                                             # noqa: E402
from da_layouts import F, MARKS, SC, dp, sd, ds, kit, rig_hands, shadow, tilted, _head, CLIP_S  # noqa: E402
from da_motion import ease, ease_out, seg, frame, camera_of, FPS, DRAW  # noqa: E402

EP = os.path.join(HERE, "..", "the-double-agent")
VER = 12
import da_runner as RN                                             # noqa: E402
T0 = 34.44
SHOTS = [("5.2", 2.8), ("5.3", 2.0), ("5.3b", 0.6), ("5.4", 2.6)]   # 5.1 plays in scene 4 now (story chain v1, fix A)
drawn = A.drawn
CAMS = {}
CS = cu.CUP_FLOOR
declare = C.declare


def don_rig(x, f, face, look, knee=0.0, s_=None):
    return lambda kk, a4: dp.don(kk, x, f, s_ or SC["don"], a4, face, look, knee=knee, hands=False)


# ---- 5.1 -------------------------------------------------------------------------------------------------------------------
def s51_surface(t):
    """v2 (the outside review 28 Nov, Tomas "tvarkom"): the mug stays the one thing to see (27 Nov, A), but the light
    has a source now: a warm cone from a lamp above, out of frame, on the mug and catching the near half of Father's
    face; the dark is a cool noir blue, not the day's colours under black; the mug is the canon's ceramic one (the old
    cut-out mug at 4.4x read as "a folded paper bag"), with its contact shadow; thin steam that thins out; Father blinks
    once, slowly."""
    import da_hand_gate as g
    import dh_cast as dhc
    td = drawn(t)
    mx, my = ds.WIN[0] + ds.WIN[2] * 0.5 + 34, ds.WIN[1] + ds.WIN[3] - 122

    def mug_drawer(k_, x, y, s_):
        c_ = k_.c
        c_.set_source_rgba(0, 0, 0, 0.30); c_.save(); c_.translate(x + 2, y + 1); c_.scale(17 * s_ / 0.62, 3.2 * s_ / 0.62)
        c_.new_path(); c_.arc(0, 0, 1, 0, 2 * math.pi); c_.restore(); c_.fill()                 # its contact shadow
        cu.mug(k_, x, y, s_ * 0.92 / 0.9, handle=1, state="rest", name="mug")
    office = dict(client=None, sofia=False, mug=True, mug_drawer=mug_drawer)
    push = ease(seg(td, 0.0, 1.4))
    cam = (mx - 18, my - 10 - 4 * push, 4.4 + 0.5 * push)            # a slow push in on the mug

    def light(k_, cam_):
        fx, fy, z = cam_
        sx, sy = (mx - fx) * z + 270, (my + 4 - fy) * z + 480           # the mug on screen
        c = k_.c
        c.set_operator(cairo.OPERATOR_MULTIPLY)                         # the whole room cool (noir), before the dark
        c.set_source_rgb(0.62, 0.66, 0.80); c.paint()
        c.set_operator(cairo.OPERATOR_OVER)
        lx, ly = sx - 22, sy - 60                                        # the light's centre: on the mug, his face at its edge
        gr = cairo.RadialGradient(lx, ly, 30, lx, ly, 230)               # the dark round it: #191C25
        gr.add_color_stop_rgba(0, 0.098, 0.110, 0.145, 0.0); gr.add_color_stop_rgba(0.28, 0.098, 0.110, 0.145, 0.0)
        gr.add_color_stop_rgba(1, 0.098, 0.110, 0.145, 0.80 + 0.06 * push)
        c.set_source(gr); c.paint()
        lamp = (sx - 40, -40)                                            # the lamp, above and out of frame: its cone
        cone = cairo.LinearGradient(lamp[0], lamp[1], lamp[0], sy + 40)
        cone.add_color_stop_rgba(0, 0.906, 0.753, 0.541, 0.0); cone.add_color_stop_rgba(0.6, 0.906, 0.753, 0.541, 0.10)
        cone.add_color_stop_rgba(1, 0.906, 0.753, 0.541, 0.0)
        c.new_path(); c.move_to(lamp[0] - 30, lamp[1]); c.line_to(lamp[0] + 30, lamp[1])
        c.line_to(sx + 120, sy + 30); c.line_to(sx - 230, sy + 30); c.close_path(); c.set_source(cone); c.fill()
        c.set_operator(cairo.OPERATOR_ADD)                               # the warm pool where it lands (#E7C08A), smaller
        gr = cairo.RadialGradient(sx - 6, sy - 34, 0, sx - 6, sy - 34, 120)
        gr.add_color_stop_rgba(0, 0.906, 0.753, 0.541, 0.26); gr.add_color_stop_rgba(1, 0.906, 0.753, 0.541, 0.0)
        c.set_source(gr); c.paint()
        c.set_operator(cairo.OPERATOR_OVER)
        fade = 1 - 0.75 * push                                           # its steam: thin, broken, thinning out
        c.set_line_width(1.8); c.set_line_cap(1)
        for i, dx in enumerate((-8, 7)):
            ph = td * 3.2 + i * 1.7
            x0, y0 = sx + dx, sy - 64
            c.set_dash([10, 7], (ph * 9) % 17)
            gr = cairo.LinearGradient(0, y0, 0, y0 - 100)
            gr.add_color_stop_rgba(0, 1, 1, 1, 0.50 * fade); gr.add_color_stop_rgba(1, 1, 1, 1, 0.0)
            c.set_source(gr)
            c.new_path(); c.move_to(x0, y0)
            c.curve_to(x0 - 9 * math.sin(ph), y0 - 30, x0 + 9 * math.sin(ph), y0 - 60, x0 + 3 * math.sin(ph * 1.3), y0 - 100)
            c.stroke()
        c.set_dash([]); c.set_line_cap(0)

    def cast(k_):
        g.nohands()
        return {}
    keep = dhc.BLINK[0]
    dhc.BLINK[0] = 0.47 <= td < 0.73                                   # one slow blink (4 drawings)
    try:
        return frame(cast, cam, office=office, tag=True, clips=14, near=light)
    finally:
        dhc.BLINK[0] = keep


# ---- 5.2 -------------------------------------------------------------------------------------------------------------------
def s52_surface(t):
    import da_s52_anim as S52
    import da_hand_gate as g
    g.arms_ok("5.2: drinking, the cup at his mouth: the elbow folds as it must")   # (FOLD/ELBOW, written exception)
    return S52.frame(t, 1)                                             # (unlocked 28 Nov: gated like the rest)


# ---- 5.3 -------------------------------------------------------------------------------------------------------------------
def s53_cast(t):
    """the motion test A v4 (passed rounds 3-4), on the cups canon: the cup on its saucer on his palm."""
    import da_hands as dh
    import da_hand_gate as g
    td = drawn(t)
    s_ = SC["don"]
    x0, f = 420, F + 290
    tape = L.tape_x(f)
    xs = 520
    clips0 = [(xs + dx, f + dy, a) for dx, dy, a in ((4, 2, 0.4), (18, 5, 2.0), (30, 1, -0.8), (12, -2, 1.2), (40, 4, 2.6))]

    def cast(k_):
        c = k_.c
        run = seg(td, 0.0, 0.40)
        flip = ease(seg(td, 0.48, 0.86))                               # (the test's polish: one more drawing at the take-off)
        hang = seg(td, 0.76, 0.88)
        drop = ease(seg(td, 0.88, 1.02))
        slide = ease_out(seg(td, 0.96, 1.2))
        stop = tape - 190                                              # dead at his own line: his shoes at the tape, not over
        x = x0 + (xs - x0) * run if td < 0.40 else xs + (stop - xs) * slide
        if td > 0.96:                                                  # his skid on the floor
            c.set_source_rgba(0.25, 0.18, 0.12, 0.55); c.set_line_cap(1); c.set_line_width(4)
            c.new_path(); c.move_to(xs, f); c.line_to(x - 30, f); c.stroke(); c.set_line_cap(0)
        old = sd.CLIPS_V2[0]; sd.CLIPS_V2[0] = True
        try:
            for i, (cx, cy, a) in enumerate(clips0):
                if td < 0.42:
                    sd.paperclip(k_, cx, cy, CLIP_S * 1.6, a)
                else:
                    tt = td - 0.42; vx = 140 + 50 * i; vy = -(420 + 70 * (i % 3))
                    px = cx + vx * tt; py = cy + vy * tt + 0.5 * 1400 * tt * tt
                    if py > f + 6:
                        tl = (-vy + math.sqrt(vy * vy + 2 * 1400 * (f + 6 - cy))) / 1400
                        px, py = cx + vx * tl, f + 6
                    sd.paperclip(k_, px, py, CLIP_S * 1.7, a + 6 * tt)
                    if py < f and tt < 0.25:
                        c.set_source_rgb(*L.INK); c.set_line_width(1.6); c.set_line_cap(1)
                        c.new_path(); c.move_to(px - 10, py + 12); c.line_to(px - 3, py + 4); c.stroke(); c.set_line_cap(0)
        finally:
            sd.CLIPS_V2[0] = old
        flying = td >= 0.48
        if flying:                                                     # the cup off its saucer: up, over, down into its puddle
            tt = min(td - 0.48, 0.42); u = tt / 0.42                     # (cold test: it hung at the top: quicker)
            cxp = xs + 40 + (tape - 64 - xs - 40) * u                  # (lands short of the tape: his side)
            cyp = (f - 300 * s_) + ((f - 2) - (f - 300 * s_)) * u - 220 * math.sin(math.pi * u)
            c.save(); c.translate(cxp, cyp); c.rotate(10 * tt if u < 1 else math.pi * 0.5)
            dh.cup(k_, 0, 0, 1.2, 1)
            g.vessel(k_, "cup", "free" if u < 1 else "rest", handle=None, base=(0, 0), rect=(-16, -26, 36, 30))
            c.restore()
        if td >= 1.03:                                                 # its puddle, short of the tape
            kit.ellipse(k_, tape - 64, f + 4, 34 * min(1, (td - 0.98) * 5), 8, (0.30, 0.18, 0.10), 5301, shadow=False, lw=1.2)
        shadow(k_, x, f + 2, 40 + 40 * max(flip, float(td >= 1.02)))
        rows = [("don", "L", "saucer_hold", "SAUCER_SUPPORT: the saucer, as 5.2 left it, all through the fall")]
        if td < 0.52:
            rows.append(("don", "R", "pinch_pinky" if not flying else "quiet", "CUP_GRIP: the cup by its handle -> it flies"))
            declare(tuple(rows), k_)
            knee = (0.7 if int(td * DRAW) % 2 else 0.0) if td < 0.40 else 1.0
            ang = 0.12 if td < 0.40 else -0.10 - 0.25 * seg(td, 0.40, 0.52)
            bob = -6 * abs(math.sin(td * 2 * math.pi * 3.3)) if td < 0.40 else 0
            face = "smug" if td < 0.40 else "shock"
            c.save(); c.translate(0, bob)
            jobs = {-1: cu.on_palm((x - 50 * s_ / 0.6, f - 130 * s_ / 0.6), CS, kind="saucer", out=-1)}
            if not flying:                                             # (cold test: as 5.2 left them) the cup up by its
                jobs[1] = cu.by_handle((x + 46 * s_ / 0.6, f - 200 * s_ / 0.6), 0.9 * CS, kind="cup", out=1)   # handle
            o = tilted(k_, x, f, ang, lambda: rig_hands(k_, don_rig(x, f, face, (1, -0.2), knee=knee), s_, jobs))
            c.restore()
            return {"don": _head(o, "don")}
        rows.append(("don", "R", "palm", "palm: flung out"))
        declare(tuple(rows), k_)
        ang = -0.35 + (-2.05 + 0.35) * flip - 0.12 * hang              # thrown back, past flat, still turning
        ang += (-1.57 + 2.17) * drop
        hip = (x - 10, f - 190 * s_)
        lift = (80 * s_) * min(1.0, flip * 1.3) * (1 - drop) - (190 - 34) * s_ * drop
        face = "shock" if td < 1.02 else ("panic" if td < 1.4 else "confused")
        look = (1, -0.6) if td < 1.4 else (1, -1.0)                    # then he looks at the line by his head
        c.save(); c.translate(0, -lift); c.translate(*hip); c.rotate(ang); c.translate(-hip[0], -hip[1])
        try:
            o = rig_hands(k_, don_rig(x, f, face, look, knee=0.6), s_,
                          {1: dict(T=(x + 140 * s_, f - 330 * s_), pose="PALM", out=1, reach=True),
                           -1: cu.on_palm((x - 120 * s_, f - 320 * s_), CS, kind="saucer", out=-1)})
        finally:
            c.restore()
        return {"don": _head(o, "don")}
    return cast


# ---- 5.3b ------------------------------------------------------------------------------------------------------------------
def s53b_surface(t):
    import da_hands as dh_
    import da_hand_gate as g
    import ps_set as pss
    td = drawn(t)
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, L.W, L.H)
    c = cairo.Context(surf); k_ = kit.Ctx(c, 0)
    c.set_source_rgb(0.72, 0.63, 0.50); c.paint()
    kit.cut(k_, [(330, 960), (470, 960), (420, -20), (330, -20)], pss.TAPE, shadow=False, lw=3)    # the tape
    u = ease_out(seg(td, 0.0, 0.40))
    land = td >= 0.40
    if not land:                                                       # the cup tumbling in from the top
        px, py = 40 + 150 * u, 120 + 470 * u * u
        c.save(); c.translate(px, py); c.rotate(-2.3 + 3.0 * u); dh_.cup(k_, 0, 0, 3.6, 1); c.restore()
        g.vessel(k_, "cup", "free", handle=None, base=(px, py), rect=(px - 60, py - 80, 120, 100))
        c.set_source_rgb(0.30, 0.18, 0.10); c.set_line_width(14); c.set_line_cap(1)          # the coffee's arc behind it
        c.new_path(); c.move_to(px + 30, py + 20); c.curve_to(px + 50, py + 60, 210, 520, 215, 540 + 60 * u); c.stroke()
        c.set_line_cap(0)
    else:
        sp = ease_out(seg(td, 0.40, 0.53))
        kit.ellipse(k_, 205, 640, 70 * sp, 22 * sp, (0.30, 0.18, 0.10), 5301, shadow=False, lw=2)   # the splash, his side
        # (cold test: "on the line": the splash's edge now stops 50 short of the tape)
        for dx, dy, r_ in ((-60, -30, 8), (40, -40, 7), (-20, -60, 6), (70, -10, 5)):
            kit.ellipse(k_, 205 + min(dx, 40) * sp, 640 + dy * sp, r_, r_, (0.30, 0.18, 0.10), 5302 + dx, shadow=False, lw=1.4)
        c.save(); c.translate(160, 612); c.rotate(1.57); dh_.cup(k_, 0, 0, 3.6, 1); c.restore()   # on its side
        g.vessel(k_, "cup", "rest", handle=None, base=(160, 612), rect=(90, 540, 140, 120))
    g.nohands()
    return surf


# ---- 5.4 -------------------------------------------------------------------------------------------------------------------
def s54_cast(t):
    td = drawn(t)

    def cast(k_):
        h = {}
        c = k_.c
        # the robot freezes: its gripper up with a clip, then its head tips (6 degrees), the smile unchanged
        rx, rf = 560, F + 24                                           # (rough cut test: behind Mom's legs she "rode" it;
        up = ease(seg(td, 0.2, 0.47))                                  # now between them, further back)
        T = (rx + 46, rf - (70 + 80 * up) * SC["robot"])
        L.rp.HEAD_ROT[0] = -0.105 * ease(seg(td, 1.0, 1.27)) - (0.10 if RN.on("s5", "5.4", "r2b", td) else 0.0)   # "Yourself."
        try:
            h["robot"] = A.robot_canon(k_, rx, rf, {1: ("grip", T)}, tilt=0.1, look=(-1, -0.4))
        finally:
            L.rp.HEAD_ROT[0] = None
        old = sd.CLIPS_V2[0]; sd.CLIPS_V2[0] = True
        sd.paperclip(k_, T[0] + 4, T[1] - 8, CLIP_S * 1.6, 1.2); sd.CLIPS_V2[0] = old
        # Mom: in from round the counter's end like a door sliding shut, planted; chin up
        mx, mf = MARKS["mom_wall"]
        slide = ease_out(seg(td, 0.0, 0.47))
        x_m = mx + 90 * (1 - slide)
        if 0.07 < slide < 0.9:                                         # her speed lines, behind her
            c.set_source_rgb(*kit.INK); c.set_line_width(2.2); c.set_line_cap(1)
            for yy in (-150, -110, -70):
                c.new_path(); c.move_to(x_m + 62, mf + yy * SC["mom"] / 0.6); c.line_to(x_m + 96, mf + yy * SC["mom"] / 0.6)
                c.stroke()
            c.set_line_cap(0)
        h["mom"] = L.mom(k_, (x_m, mf), "fists", "glare", look=(-1, 0.2), chin=td >= 0.6)
        # Don: stopped in front of her, he shrinks back
        x, f = MARKS["don_wall"]; L.DON_FEET[0] = (x, f)
        shrink = ease(seg(td, 0.47, 0.8))
        shadow(k_, x, f + 2, 36)
        face = "shock" if td < 0.8 else ("hard" if td < 1.75 else "confused")   # "I'll sue." at the robot; then its answer
        kit.MOUTH[0] = 0.9 if (RN.on("s5", "5.4", "r2a", td) and int(td * DRAW) % 2 == 0) else None
        o2 = tilted(k_, x, f, 0.10 * shrink, lambda: rig_hands(
            k_, don_rig(x, f, face, (1, -0.3), s_=SC["don"] * (1 - 0.06 * shrink)), SC["don"] * (1 - 0.06 * shrink), {})
            if not L.don_shoes(k_, x, f, SC["don"] * (1 - 0.06 * shrink)) else None)
        kit.MOUTH[0] = None
        h["don"] = _head(o2, "don")
        declare((("robot", "L", "robot_rest", "at rest"), ("robot", "R", "robot_grip", "the gripper up, a clip in it"),
                 ("mom", "L", "fist", "FIST: on her hip"), ("mom", "R", "fist", "FIST: on her hip"),
                 ("don", "L", "quiet", "quiet"), ("don", "R", "quiet", "quiet")), k_,
                [("clip", (T[0] - 12, T[1] - 22, 30, 30))])
        return h
    return cast


# ---- render, gate, sound ---------------------------------------------------------------------------------------------------
def render_shot(sid, t):
    if sid == "5.1":
        return s51_surface(t)
    if sid == "5.2":
        return s52_surface(t)
    if sid == "5.3":
        return frame(s53_cast(t), CAMS[sid][0], tag=True, clips=12, office=dict(client="seated", sofia=True, mug=True),
                     dutch=0.12)
    if sid == "5.3b":
        return s53b_surface(t)
    if sid == "5.4":
        return frame(s54_cast(t), CAMS[sid][0], tag=True, clips=11, office=dict(client="seated", sofia=True, mug=True))
    raise KeyError(sid)


STARTS = {}
_acc = 0.0
for _s, _d in SHOTS:
    STARTS[_s] = _acc; _acc += _d


def sting():
    """the noir sting (Tomas 28 Nov: one, for 5.1's mug): a low muted-trumpet-ish fall over a double-bass pluck and a
    soft cymbal swell; synthesized here, no licences."""
    import numpy as np
    import da_animatic as AN
    sr = AN.SR
    n = int(1.5 * sr); t = np.arange(n) / sr
    env = np.minimum(1, t / 0.03) * np.exp(-t / 0.7)
    f = 233.08 * (1 - 0.06 * np.minimum(1, t / 0.9))                  # B flat, sagging a little
    horn = (np.sin(2 * np.pi * f * t) + 0.5 * np.sin(4 * np.pi * f * t) + 0.25 * np.sin(6 * np.pi * f * t)) * env
    horn *= 1 + 0.15 * np.sin(2 * np.pi * 5.5 * t)                    # a slow vibrato
    bass = np.sin(2 * np.pi * 58.27 * t) * np.exp(-t / 0.35) * np.minimum(1, t / 0.005)
    cym = AN._lp(AN._noise(1.5), 2)[:n] * np.minimum(1, t / 0.6) * np.exp(-np.maximum(0, t - 0.6) / 0.3) * 0.25
    return 0.5 * horn + 0.8 * bass + cym


CUES = [
    (STARTS["5.2"] + 0.05, "cup clink", 0.5), (STARTS["5.2"] + 0.35, "cup clink", 0.45),   # the rattle
    (STARTS["5.2"] + 0.6, "cup clink", 0.4),
    (STARTS["5.2"] + 1.35, "slurp", 0.6),
    (STARTS["5.3"] + 0.0, "shoe squeaks", 0.6),
    (STARTS["5.3"] + 0.42, "skid", 0.9),
    (STARTS["5.3"] + 0.44, "rattle", 0.7),                          # the clips spraying
    (STARTS["5.3"] + 1.0, "thud", 0.9),
    (STARTS["5.3"] + 1.03, "splash", 0.6),
    (STARTS["5.3b"] + 0.4, "splash", 0.8),
    (STARTS["5.4"] + 0.0, "swishes", 0.7),
]


def mix(sec, path):
    import numpy as np
    import da_animatic as AN
    sr = AN.SR
    n = int(sec * sr)
    m = 0.004 * AN._lp(AN._noise(sec + 0.1), 200)[:n]
    for t0, word, gain in CUES:
        w = dict(AN.FX)[word]()
        i = int(t0 * sr)
        g = 0.18 * gain / (np.max(np.abs(w)) + 1e-9)
        m[i:i + len(w)] += g * w[:max(0, n - i)]
    RN.add(m, "s5", STARTS)                                           # the Don x robot money lines (da_runner v2)
    m /= max(1.0, np.max(np.abs(m)) / 0.89)
    m.astype(np.float32).tofile(path)
    return path


GATED = ("5.2", "5.3", "5.3b", "5.4")


HITS = {'5.3': 1.0}   # shot -> the hit's time in it: a 3-drawing camera knock (Tomas 28 Nov)


def build():
    import subprocess
    from PIL import Image, ImageDraw
    import da_hand_gate as g
    import hands_v4 as hv
    import da_arms
    da_arms.setup(); hv.enable(); g.install(); cu.install(); A._SETUP.append(1)
    g.ARM_RULES[0] = True; L.ELBOW_RULE[0] = True                     # (Tomas's deep audit 28 Nov: every arm, every drawing)
    for sid in ("5.3", "5.4"):
        CAMS[sid] = camera_of(sid)
    tmp = "/tmp/da_anim_s5"; os.makedirs(tmp, exist_ok=True)
    for f_ in os.listdir(tmp):
        os.remove(os.path.join(tmp, f_))
    n = 0; marks = []; faults = []
    with ds.no_badges(), L.don_legs(), L.sofia_lib_hands(), L.face_guard():
        for sid, dur in SHOTS:
            marks.append((n, sid))
            for i in range(int(round(dur * FPS))):
                g.reset()
                surf = render_shot(sid, i / FPS)
                if sid in HITS:                                        # the hit's accent (da_motion.shaken)
                    surf = __import__("da_motion").shaken(surf, i / FPS - HITS[sid])
                if i % 2 == 0 and sid in GATED:
                    faults += ["%s %.2fs  %s" % (sid, i / FPS, f) for f in g.check()]
                surf.write_to_png(os.path.join(tmp, "%04d.png" % n)); n += 1
    if faults:
        print("HAND GATE FAIL: %d" % len(faults))
        seen = set()
        for f in faults:
            key = f.split("  ")[1][:50]
            if key not in seen:
                seen.add(key); print("  " + f)
        raise SystemExit(1)
    print("hand gate: PASS on %d drawings" % (n // 2))
    out = os.path.join(EP, "da_anim_s5_v%d.mp4" % VER)
    wav = mix(n / FPS, os.path.join(tmp, "mix.f32"))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", os.path.join(tmp, "%04d.png"),
                    "-f", "f32le", "-ar", "48000", "-ac", "1", "-i", wav, "-map", "0:v", "-map", "1:a",
                    "-vf", "format=yuv420p", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                    "-af", "loudnorm=I=-15:TP=-1.5:LRA=11", "-ar", "48000",
                    "-c:a", "aac", "-b:a", "160k", "-shortest", out], check=True)
    picks = list(range(0, n, FPS // 8))
    tw, th, per = 200, 356, 18
    rows = (len(picks) + per - 1) // per
    S = Image.new("RGB", (per * (tw + 6) + 6, rows * (th + 30) + 6), (245, 244, 240)); d = ImageDraw.Draw(S)
    for j, i in enumerate(picks):
        im = Image.open(os.path.join(tmp, "%04d.png" % i)).convert("RGB").resize((tw, th), Image.LANCZOS)
        X, Y = 6 + (j % per) * (tw + 6), 6 + (j // per) * (th + 30)
        sid = [s for a, s in marks if a <= i][-1]
        S.paste(im, (X, Y + 22)); d.text((X + 2, Y + 4), "%d  %s  %.2fs" % (j + 1, sid, T0 + i / FPS), fill=(20, 20, 20))
    png = os.path.join(EP, "da_anim_s5_v%d_8fps.png" % VER)
    S.save(png)
    print("wrote", out, png, n, "frames")


if __name__ == "__main__":
    build()
