"""THE DOUBLE AGENT (episode 15): the four motion tests (stage 6; Tomas 27 Nov: all four, before the animation).

Each test is the hardest moment of one beat at film rate: the drawings change 15 times a second (acting), the frames
at 30 fps; anticipation -> action -> settle -> hold (lessons 21, 334, 112). The world, the rigs, the marks and the
camera are the layouts' (da_layouts: floor_world, rig_hands, the ground gate's rules); only the cast moves.

  A  5.3  the slip: he runs at the line, his foot lands on the clips, all of him in the air, the clips fly, he lands
          and slides, and stops dead at his own tape
  B  3.4  Mom the goalkeeper: he steps left, she steps with him; right, she steps with him; a feint: she does not move
  C  7.2  the tape gate: he lifts his peeled strip like a boom barrier, chin up; Pam walks through under it
  D  6.5-6.7  Pam's choice: her mouth opens to correct him, her eyes go up to the glass, her mouth shuts

  python3 da_motion.py [A B C D]   ->  da_motion_<X>_v2.mp4 and da_motion_<X>_v2_8fps.png (v1: the first round, 27 Nov) (the cold-viewer strip)
"""
import math
import os
import subprocess
import sys

import cairo

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import da_layouts as L                                             # noqa: E402
from da_layouts import F, MARKS, SC, dp, pm, sd, ds, dpr, kit, rig_hands, shadow, tilted, _head, CLIP_S, FEMALE  # noqa
from kit import Ctx                                                # noqa: E402

EP = os.path.join(HERE, "..", "the-double-agent")
FPS, DRAW = 30, 15


def ease(x):
    x = min(1.0, max(0.0, x)); return x * x * (3 - 2 * x)


def ease_out(x):
    x = min(1.0, max(0.0, x)); return 1 - (1 - x) ** 3


def seg(t, a, b):
    """0 before a, 1 after b, linear between."""
    return min(1.0, max(0.0, (t - a) / (b - a))) if b > a else float(t >= a)


def overshoot(x, k=1.15):
    x = min(1.0, max(0.0, x)); return 1 + (k - 1) * math.sin(math.pi * x) if x > 0.5 else ease_out(x * 2) * k if x < 0.5 else 1


def camera_of(sid):
    """the camera the layout chose for this shot (its framing search), to keep the test framed like the board."""
    got = {}
    real = L._draw

    def spy(s, args, fr, cam):
        got["cam"], got["fr"] = cam, fr
        return real(s, args, fr, cam)
    L._draw = spy
    try:
        L.render(sid)
    finally:
        L._draw = real
    return got["cam"], got["fr"]


def frame(cast, cam, office=None, tag=True, clips=12, dutch=0.0, back=()):
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, L.W, L.H)
    c = cairo.Context(surf); k = Ctx(c, 0)
    c.set_source_rgb(*kit.WALL); c.paint()
    c.save()
    if dutch:
        c.translate(270, 480); c.rotate(dutch); c.scale(1.12, 1.12); c.translate(-270, -480)
    L.sbv.view(c, *cam); ds._floor_on(c)
    L.floor_world(k, cast=cast, tag=tag, clips=clips, office=office, back=back)
    c.restore()
    return surf


# ---- A: 5.3 the slip -----------------------------------------------------------------------------------------------------
def test_a(t):
    """v2 (the motion test's viewers: no cause, the take-off one drawing, the hang a stiff hover, the legs a box):
    two drawings of the foot landing on the clips and them spraying before he leaves the floor; bigger clips; a short
    hang still turning; his legs bent on the floor; a shorter end."""
    s_ = SC["don"]
    x0, f = 420, F + 290
    tape = L.tape_x(f)
    xs = 520
    clips0 = [(xs + dx, f + dy, a) for dx, dy, a in ((4, 2, 0.4), (18, 5, 2.0), (30, 1, -0.8), (12, -2, 1.2), (40, 4, 2.6))]

    def cast(k_):
        c = k_.c
        td = math.floor(t * DRAW) / DRAW
        run = seg(td, 0.0, 0.40)
        flip = ease(seg(td, 0.48, 0.80))                                   # over 4-5 drawings, not one
        hang = seg(td, 0.70, 0.82)
        drop = ease(seg(td, 0.82, 0.96))
        slide = ease_out(seg(td, 0.90, 1.12))
        x = x0 + (xs - x0) * run if td < 0.40 else xs + (tape - 150 - xs) * slide
        if td > 0.9:
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
                    if py < f and tt < 0.25:                                  # their flight ticks
                        c.set_source_rgb(*L.INK); c.set_line_width(1.6); c.set_line_cap(1)
                        c.new_path(); c.move_to(px - 10, py + 12); c.line_to(px - 3, py + 4); c.stroke(); c.set_line_cap(0)
        finally:
            sd.CLIPS_V2[0] = old
        if td >= 0.48:                                                     # the mug: up, over, down into its own puddle
            tt = min(td - 0.48, 0.55); u = tt / 0.55
            cxp = xs + 40 + (tape - 30 - xs - 40) * u
            cyp = (f - 300 * s_) + ((f - 2) - (f - 300 * s_)) * u - 220 * math.sin(math.pi * u)
            c.save(); c.translate(cxp, cyp); c.rotate(8 * tt if u < 1 else math.pi * 0.5)
            __import__("da_hands").cup(k_, 0, 0, 1.2, 1); c.restore()
        if td >= 1.0:
            kit.ellipse(k_, tape - 30, f + 4, 34 * min(1, (td - 0.95) * 5), 8, (0.30, 0.18, 0.10), 5301, shadow=False, lw=1.2)
        shadow(k_, x, f + 2, 40 + 40 * max(flip, float(td >= 0.96)))
        if td < 0.40:                                                      # the run
            knee = 0.7 if int(td * DRAW) % 2 else 0.0
            c.save(); c.translate(0, -6 * abs(math.sin(td * 2 * math.pi * 3.3)))
            o = tilted(k_, x, f, 0.12, lambda: dp.don(k_, x, f, s_, "stand", "smug", (1, -0.2), knee=knee))
            hx, hy, r_ = _head(o, "don")
            c.save(); c.translate(hx + r_ * 1.5, hy + r_ * 2.6); __import__("da_hands").cup(k_, 0, 0, 1.2, 1); c.restore()
            c.restore()                                                     # his cup in hand (v2: "from nowhere")
            return {"don": _head(o, "don")}
        if td < 0.52:                                                      # the contact: his foot shoots out on the clips
            o = tilted(k_, x, f, -0.10 - 0.25 * seg(td, 0.40, 0.52),
                       lambda: dp.don(k_, x, f, s_, "stand", "shock", (1, 0.6), knee=1.0))
            return {"don": _head(o, "don")}
        ang = -0.35 + (-2.05 + 0.35) * flip - 0.12 * hang                  # thrown back, past flat, still turning
        ang += (-1.57 + 2.17) * drop
        hip = (x - 10, f - 190 * s_)
        lift = (80 * s_) * min(1.0, flip * 1.3) * (1 - drop) - (190 - 34) * s_ * drop
        face = "shock" if td < 0.96 else "panic"
        c.save(); c.translate(0, -lift); c.translate(*hip); c.rotate(ang); c.translate(-hip[0], -hip[1])
        try:
            o = rig_hands(k_, lambda kk, a4: dp.don(kk, x, f, s_, a4, face, (1, -0.6), knee=0.6, hands=False), s_,
                          {-1: dict(T=(x - 140 * s_, f - 330 * s_), pose="PALM", out=-1, reach=True),
                           1: dict(T=(x + 140 * s_, f - 330 * s_), pose="PALM", out=1, reach=True)})
        finally:
            c.restore()
        return {"don": _head(o, "don")}
    return cast


# ---- B: 3.4 Mom the goalkeeper -------------------------------------------------------------------------------------------
def test_b(t):
    """v2 (viewers: her steps unseen behind him, their heads stacked, his moves pop): side by side with a gap, each
    step with a lift; the feint: she stays; his end face frustrated."""
    def cast(k_):
        h = {}
        td = math.floor(t * DRAW) / DRAW
        def don_dx(tt):
            return (-60 * ease(seg(tt, 0.25, 0.55)) + 120 * ease(seg(tt, 0.80, 1.20)) - 30 * ease(seg(tt, 1.50, 1.62))
                    + 30 * ease(seg(tt, 1.70, 1.95)))
        def mom_dx(tt):
            return -60 * ease(seg(tt, 0.33, 0.62)) + 120 * ease(seg(tt, 0.88, 1.28))
        mf = F + 40
        mx = MARKS["mom_wall"][0] + mom_dx(td)
        x, f = MARKS["mom_wall"][0] - 118 + don_dx(td), F + 40       # side by side, a body's gap, one floor line
        lift_d = 9 * math.sin(math.pi * seg(td, 0.25, 0.55)) + 9 * math.sin(math.pi * seg(td, 0.80, 1.20)) + \
            5 * math.sin(math.pi * seg(td, 1.50, 1.62))
        lift_m = 7 * math.sin(math.pi * seg(td, 0.33, 0.62)) + 7 * math.sin(math.pi * seg(td, 0.88, 1.28))
        c = k_.c
        shadow(k_, x, f + 2, 36); shadow(k_, mx, mf + 2, 36)
        face = "confused" if td < 1.7 else "panic"
        c.save(); c.translate(0, -lift_d)
        h["don"] = _head(dp.don(k_, x, f, SC["don"], "stand", face, (1, -0.3), knee=0.6 if lift_d > 4 else 0.0), "don")
        c.restore()
        c.save(); c.translate(0, -lift_m)
        h["mom"] = L.mom(k_, (mx, mf), "fists", "unimpressed", look=(1, -0.6), chin=True)   # never looking at him
        c.restore()
        return h
    return cast


# ---- C: 7.2 the tape gate ------------------------------------------------------------------------------------------------
def test_c(t):
    """v5 (28 Nov, Tomas: 1): the doorman, close: Don alone, MC, at his line: a beat upright, up on his toes a little
    (anticipation), then the deep bow at the waist with both arms rolling out toward the door off screen; held."""
    def cast(k_):
        td = math.floor(t * DRAW) / DRAW
        f = F + 70; x = L.tape_x(f) - 46; s_ = SC["don"]
        shadow(k_, x, f + 2, 40)
        up = 0.08 * math.sin(math.pi * seg(td, 0.20, 0.40))
        bow = 0.40 * ease_out(seg(td, 0.38, 0.70)) + 0.05 * math.sin(math.pi * seg(td, 0.68, 0.90))
        roll = ease_out(seg(td, 0.38, 0.75))
        TR = (x + (40 + 150 * roll) * s_, f - 200 * s_)
        TL = (x + (10 + 130 * roll) * s_, f - (190 - 30 * roll) * s_)
        o, head = L.bow(k_, x, f, s_, bow - up, lambda: rig_hands(
            k_, lambda kk, a4: dp.don(kk, x, f, s_, a4, "happy" if td > 0.35 else "smug", (1, 0.3), hands=False), s_,
            {1: dict(T=TR, pose="PALM", out=1, reach=True), -1: dict(T=TL, pose="PALM", out=-1, reach=True)}))
        return {"don": head}
    return cast


# ---- D: 6.5-6.7 Pam's choice ---------------------------------------------------------------------------------------------
def test_d(t):
    def cast(k_):
        px, pf = 626, F + 60
        td = math.floor(t * DRAW) / DRAW
        shadow(k_, px, pf + 2, 32)
        inhale = math.sin(math.pi * seg(td, 0.15, 0.40)) * 4               # anticipation: a breath in
        if td < 0.30:
            mouth, face, look = "M", "neutral", (-0.6, 0.0)
        elif td < 0.55:
            mouth, face, look = "A", "doubt", (-0.6, 0.0)                    # she opens her mouth to correct him (v1 held
        elif td < 0.95:                                                     # the shock 1.5 s: too long, both viewers)
            mouth, face, look = "A", "doubt", (0.7, -0.7)                    # her eyes up to the glass (v4: one drawing,
        elif td < 1.1:                                                      # "easy to miss": now 3)
            mouth, face, look = "E", "neutral", (0.7, -0.7)                  # the mouth closing
        else:
            mouth, face, look = "M", "neutral", (0.0, 0.0)                   # shut; eyes front: chosen
        o = pm.pam(k_, px, pf, SC["pam"], "stand", face, look, mug=False, mouth=mouth)   # (v1's inhale lifted her feet
        return {"pam": _head(o, "pam")}                                                   # off the floor: dropped)
    return cast


TESTS = {
    "A": dict(sid="5.3", fn=test_a, dur=1.3, kw=dict(office=dict(client="seated", sofia=True, mug=True), clips=8),
              dutch=0.12, title="5.3 the slip"),
    "B": dict(sid="3.4", fn=test_b, dur=2.4, kw=dict(office=dict(client="stand", sofia=True, mug=True, pam="hand_on_mug"),
                                                     clips=20), title="3.4 Mom the goalkeeper"),
    "C": dict(sid="7.2", fn=test_c, dur=1.4, kw=dict(office=dict(client="seated", sofia=True, roll="held"), clips=1),
              title="7.2 the doorman"),
    "D": dict(sid="6.5", fn=test_d, dur=1.5, kw=dict(clips=6), title="6.5-6.7 Pam's choice"),
}


def build(name):
    from PIL import Image, ImageDraw
    spec = TESTS[name]
    cam, fr = camera_of(spec["sid"])
    if name == "A":                                                   # on him and the line (v1 at 0.95: too small)
        cam = (500, F + 170, cam[2] * 1.45)
    elif name == "B":                                                 # both, side by side, and their steps
        cam = (MARKS["mom_wall"][0] - 60, F - 120, cam[2] * 0.85)
    elif name == "C":                                                 # his bow whole and the door
        pass                                                          # the layout's own MC framing (camera_of)
    out = os.path.join(EP, "da_motion_%s_v5.mp4" % name)
    tmp = "/tmp/da_motion_%s" % name; os.makedirs(tmp, exist_ok=True)
    n = int(spec["dur"] * FPS)
    with ds.no_badges(), L.don_legs(), L.sofia_lib_hands(), L.face_guard():
        for i in range(n):
            t = i / FPS
            surf = frame(spec["fn"](t), cam, dutch=spec.get("dutch", 0.0), **spec["kw"])
            surf.write_to_png(os.path.join(tmp, "%03d.png" % i))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", os.path.join(tmp, "%03d.png"),
                    "-vf", "format=yuv420p", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", out], check=True)
    step = FPS // 8                                                     # the 8 fps strip for the cold viewers
    picks = list(range(0, n, step))
    tw, th = 240, 427                                                 # (180 px tiles read as "tiny" to the viewers)
    S = Image.new("RGB", (len(picks) * (tw + 6) + 6, th + 34), (245, 244, 240)); d = ImageDraw.Draw(S)
    for j, i in enumerate(picks):
        im = Image.open(os.path.join(tmp, "%03d.png" % i)).convert("RGB").resize((tw, th), Image.LANCZOS)
        S.paste(im, (6 + j * (tw + 6), 28)); d.text((8 + j * (tw + 6), 6), "%d" % (j + 1), fill=(20, 20, 20))
    png = os.path.join(EP, "da_motion_%s_v5_8fps.png" % name)
    S.save(png)
    print("wrote", out, png, n, "frames")
    return out, png


if __name__ == "__main__":
    for nm in (sys.argv[1:] or list(TESTS)):
        build(nm)
