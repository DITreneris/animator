"""THE DOUBLE AGENT (episode 15): stage 7, scene 6 (6.1-6.8b, 0:43.44-0:55.39), the 540 preview. Tomas 28 Nov
(/grill-me): 6.4 Don's delight is both palms out to her ("you!"), not the thumbs; 6.5-6.7 motion test D v5 with its
polish (the eyes up over 4 drawings, a shoulder drop); 6.3 held 1.0 s; 6.8 Pam only leans in.

  6.1  S6 M: Pam steps out of the office door with the robot's printed minutes, toward Don; Mom knits, not looking up
  6.2  S3 M: Don narrows his eyes at her; she holds out the page: "I took notes." (runs on into 6.3)
  6.3  I: the page: AGENDA: WITHOUT HIM, her fingers at its corner
  6.4  S3 MC: suspicion -> delight, both palms out to her: "You're spying for me?"
  6.5  C: Pam's mouth opens to correct him; her eyes go up, to the glass
  6.6  S9 C: her view: the Client waiting, his blueprint rolled in his hands, looking at her
  6.7  C: her eyes come back; her mouth shuts; her shoulders drop: chosen
  6.8  S3 MC: Don looks left, right (Pam half a metre away), pulls his headset mic to his lips, whispers: "Keep
       infiltrating."; Pam leans in to hear
  6.8b C: Pam looks at his mic, then at him

  python3 da_anim_s6.py   ->  ../the-double-agent/da_anim_s6_v1.mp4, da_anim_s6_v1_8fps.png
"""
import math
import os
import sys

import cairo

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import da_cups as cu                                               # noqa: E402
import da_anim_s1 as A                                             # noqa: E402
import da_anim_s2 as B                                             # noqa: E402
import da_anim_s3 as C                                             # noqa: E402
import da_layouts as L                                             # noqa: E402
from da_layouts import F, MARKS, SC, dp, pm, ds, kit, rig_hands, shadow, tilted, _head, FEMALE  # noqa: E402
from da_motion import ease, ease_out, seg, frame, camera_of, FPS, DRAW  # noqa: E402

EP = os.path.join(HERE, "..", "the-double-agent")
VER = 2
T0 = 43.44
SHOTS = [("6.1", 1.4), ("6.2", 1.2), ("6.3", 1.0), ("6.4", 2.23), ("6.5", 1.0), ("6.6", 1.0), ("6.7", 0.8),
         ("6.8", 2.72), ("6.8b", 0.6)]
drawn = A.drawn
CAMS = {}
declare = C.declare
pam_held = C.pam_held
TAKES = {"6.2": ("B", 0.6), "6.4": ("B", 0.6), "6.8": ("B", 0.9)}   # da_timing_v4's picks and take_at
ENV = {}


def env(sid):
    if sid not in ENV:
        letter, at = TAKES[sid]
        ENV[sid] = B._voice_env(os.path.join(HERE, "da_voices", "takes", "%s_%s.wav" % (sid, letter)), at)
    return ENV[sid]


def talking(sid, t):
    st, on, _, _ = env(sid)
    n = int((drawn(t) - st) * DRAW)
    return 0 <= n < len(on) and on[n]


def page_job(T, s=0.44, ang=0.05):
    def obj(kk, P, w):
        import da_hand_gate as g_
        L._page(kk, P, w, s, ang)
        g_.prop(kk, "page", P[0] - 60 * s, P[1] - 8, 120 * s, 150 * s)   # the page hangs from her fingertips
    return dict(T=T, pose="PINCH", out=-1, reach=True, contact="tip", obj=obj)


def don_rig(x, f, face, look, chin=0):
    return lambda kk, a4: dp.don(kk, x, f, SC["don"], a4, face, look, chin=chin, hands=False)


def _mom_folded(k_, look):
    import da_hand_gate as g_
    with g_.paused():                                                  # (as scene 4: the fold read by CROSS/AIR as faults)
        return L.mom(k_, "mom_desk_s", "folded", "unimpressed", look=look)


# ---- 6.1 -------------------------------------------------------------------------------------------------------------------
def s61_parts(t):
    td = drawn(t)

    def mom_back(k_):
        return {"mom": _mom_folded(k_, (0.2, 1.0))}

    def cast(k_):
        out = ease_out(seg(td, 0.0, 0.9))                              # out of the door's gap, two steps toward Don
        x, f = 900 - 70 * out, F + 26
        step = math.sin(math.pi * 2 * seg(td, 0.0, 0.9)) if td < 0.9 else 0
        L.office_door_open(k_, 0.55 * (1 - ease(seg(td, 0.4, 1.0))) + 0.02, knob_y=F - 72)   # it swings shut behind her
        declare((("pam", "L", "pinch", "PINCH: the printed minutes"), ("pam", "R", "quiet", "quiet")), k_)
        shadow(k_, x, f + 2, 32)
        k_.c.save(); k_.c.translate(0, -3 * abs(step))
        o = tilted(k_, x, f, -0.08, lambda: rig_hands(
            k_, lambda kk, a4: pam_held(kk, x, f, SC["pam"], a4, "neutral", (-1, 0.2), mug=False), SC["pam"],
            {-1: page_job((x - 60 * SC["pam"] / 0.54, f - 190), 0.40, -0.1)}, sex="f", skin=FEMALE))
        k_.c.restore()
        return {"pam": _head(o, "pam")}
    return cast, mom_back


# ---- 6.2 / 6.4 / 6.8: the two at his counter ---------------------------------------------------------------------------------
def s62_cast(t):
    td = drawn(t)

    def cast(k_):
        h = {}
        dx_, df_ = MARKS["don_counter"][0] + 24, MARKS["don_counter"][1]; L.DON_FEET[0] = (dx_, df_)
        px, pf = 626, F + 60
        declare((("pam", "L", "pinch", "PINCH: the page held out to him"), ("pam", "R", "quiet", "quiet"),
                 ("don", "L", "quiet", "quiet"), ("don", "R", "quiet", "quiet")), k_)
        shadow(k_, dx_, df_ + 2, 40)
        narrow = td >= 0.27                                            # his eyes narrow at her
        o = rig_hands(k_, don_rig(dx_, df_, "hard" if narrow else "confused", (1, 0.1)), SC["don"], {})
        h["don"] = _head(o, "don")
        shadow(k_, px, pf + 2, 32)
        reach = ease(seg(td, 0.0, 0.33))                               # the page comes out to him
        T = (px - 40 - 30 * reach, pf - 132 - 6 * reach)                # (below his headset: the cold test lost it behind the page)
        mouth = "A" if talking("6.2", t) else None
        op = rig_hands(k_, lambda kk, a4: pam_held(kk, px, pf, SC["pam"], a4, "neutral", (-1, 0.3), mug=False,
                                                   mouth=mouth), SC["pam"], {-1: page_job(T)}, sex="f", skin=FEMALE)
        h["pam"] = _head(op, "pam")
        h["page"] = (T[0] - 10, T[1] + 20, 30)
        return h
    return cast


def s64_cast(t):
    td = drawn(t)

    def cast(k_):
        x, f = MARKS["don_counter"][0] + 24, MARKS["don_counter"][1]; L.DON_FEET[0] = (x, f)
        s_ = SC["don"]
        shadow(k_, x, f + 2, 40)
        joy = ease(seg(td, 0.47, 0.6))                                 # suspicion -> delight: both palms out to her: "you!"
        face = "hard" if td < 0.47 else "grin"
        kit.MOUTH[0] = 0.8 if talking("6.4", t) else None
        rows = [("don", "L", "quiet" if joy < 0.05 else "palm", "quiet -> palm: both palms out to her, \"you!\""),
                ("don", "R", "quiet" if joy < 0.05 else "palm", "quiet -> palm")]
        declare(tuple(rows), k_)
        jobs = {}
        if joy >= 0.05:
            jobs[1] = dict(T=(x + (40 + 70 * joy) * s_ / 0.6, f - (150 + 40 * joy) * s_ / 0.6), pose="PALM", out=1,
                           reach=True)                                 # both palms out toward her (screen right): the far
            jobs[-1] = dict(T=(x - (40 + 40 * joy) * s_ / 0.6, f - (140 + 30 * joy) * s_ / 0.6), pose="PALM", out=-1,
                            reach=True)                                # the near one open on his own side (an arm across
                                                                       # his chest fails the gate's CROSS): arms open, "you!"
        c = k_.c
        c.save(); c.translate(x, f); c.rotate(0.06 * joy); c.translate(-x, -f)   # leaning in to her
        try:
            o = rig_hands(k_, don_rig(x, f, face, (1, 0.0), chin=0), s_, jobs)
        finally:
            c.restore(); kit.MOUTH[0] = None
        return {"don": _head(o, "don")}
    return cast


def s68_cast(t):
    td = drawn(t)

    def cast(k_):
        import da_hand_gate as g_
        h = {}
        x, f = MARKS["don_counter"][0] + 24, MARKS["don_counter"][1]; L.DON_FEET[0] = (x, f); s_ = SC["don"]
        look = (1, 0.3)
        if 0.2 <= td < 0.53:
            look = (-1, 0.0)                                           # left
        elif 0.53 <= td < 0.87:
            look = (1, 0.0)                                            # right (Pam right there)
        dface = "neutral" if td < 0.87 else "smug"                     # (his eyes open for the look left and right)
        with g_.paused():                                              # where his head is (for the mic)
            kk = kit.Ctx(cairo.Context(cairo.ImageSurface(cairo.FORMAT_RGB24, 8, 8)), 0)
            hx, hy, r_ = _head(rig_hands(kk, don_rig(x, f, dface, look), s_, {}), "don")
        pull = ease(seg(td, 0.87, 1.0))
        # the boom from his headset's ear piece, pulled round to his lips; his fingers pinch it near the mic
        ear = (hx + r_ * 0.95, hy - r_ * 0.1)
        rest = (hx + r_ * 1.05, hy + r_ * 0.35)
        lips = (hx + r_ * 0.28, hy + r_ * 0.55)
        tip = (rest[0] + (lips[0] - rest[0]) * pull, rest[1] + (lips[1] - rest[1]) * pull)

        def boom(kk_, P, w):
            c = kk_.c
            c.set_source_rgb(0.20, 0.20, 0.22); c.set_line_width(4.0 * s_ / 0.6); c.set_line_cap(1)
            c.new_path(); c.move_to(*ear)
            c.curve_to(ear[0] + r_ * 0.1, ear[1] + r_ * 0.5, tip[0] + r_ * 0.35, tip[1] + r_ * 0.1, tip[0], tip[1]); c.stroke()
            c.set_line_cap(0)
            kit.ellipse(kk_, tip[0], tip[1], r_ * 0.13, r_ * 0.10, (0.10, 0.10, 0.12), 6801, shadow=False, lw=1.2)
        rows = [("don", "R", "pinch" if pull > 0 else "quiet", "quiet -> PINCH: the mic's boom at his lips"),
                ("don", "L", "quiet", "quiet"), ("pam", "L", "quiet", "quiet"), ("pam", "R", "quiet", "quiet")]
        declare(tuple(rows), k_, [("mic", (tip[0] - 16, tip[1] - 14, 40, 28))] if pull > 0 else [])
        shadow(k_, x, f + 2, 40)
        jobs = {}
        if pull > 0:
            jobs[1] = dict(T=(tip[0] + r_ * 0.55, tip[1] + r_ * 0.35), pose="PINCH", out=1, reach=True, contact="tip",
                           obj=boom, behind=True)
        kit.MOUTH[0] = 0.35 if talking("6.8", t) else None             # a whisper: the mouth barely open
        try:
            o = rig_hands(k_, don_rig(x, f, dface, look), s_, jobs)
        finally:
            kit.MOUTH[0] = None
        if pull <= 0:
            boom(k_, None, 0)
        h["don"] = _head(o, "don")
        px, pf = 648, F + 62                                           # (cold test: at 604 his arm to the mic crossed her:
        lean = 0.20 * ease(seg(td, 1.07, 1.4))                         # "his arm round her") half a metre off; she leans in
        shadow(k_, px, pf + 2, 32)
        op = tilted(k_, px, pf, -lean, lambda: rig_hands(
            k_, lambda kk2, a4: pam_held(kk2, px, pf, SC["pam"], a4, "neutral", (-1, 0.1), mug=False), SC["pam"], {},
            sex="f", skin=FEMALE))
        h["pam"] = _head(op, "pam")
        return h
    return cast


# ---- 6.3 the page ----------------------------------------------------------------------------------------------------------
def s63_surface(t):
    import hand_lib_v4 as hl
    import da_hand_gate as g
    td = drawn(t)
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, L.W, L.H)
    c = cairo.Context(surf); k_ = kit.Ctx(c, 0)
    z = 1.0 + 0.05 * ease(seg(td, 0.0, 1.0))                           # a slow push
    c.translate(270, 480); c.scale(z, z); c.translate(-270, -480)
    g.jobs(("pam", "L", "pinch", "PINCH: her fingers on the page's corner"))
    g.prop(k_, "page", 60, 250, 460, 470)
    c.set_source_rgb(0.72, 0.63, 0.50); c.paint()
    kit.cut(k_, [(-40, 700), (170, 640), (200, 760), (-40, 860)], (0.40, 0.24, 0.50), lw=3)
    L.dpr.minutes(k_, 290, 470, 2.9, -0.04)
    hl.LWS[0] = 2.6
    hl.draw_lr(k_, "PINCH", 186, 640, (0.7, -0.7), 58, FEMALE, -1)
    hl.LWS[0] = 1.0
    return surf


# ---- 6.5 / 6.7 Pam close ---------------------------------------------------------------------------------------------------
def pam_close(k_, mouth, face, look, drop=0.0):
    px, pf = 626, F + 60
    declare((("pam", "L", "quiet", "quiet"), ("pam", "R", "quiet", "quiet")), k_)
    shadow(k_, px, pf + 2, 32)
    k_.c.save(); k_.c.translate(0, 4 * drop)                           # her shoulders drop
    o = rig_hands(k_, lambda kk, a4: pam_held(kk, px, pf, SC["pam"], a4, face, look, mug=False, mouth=mouth),
                  SC["pam"], {}, sex="f", skin=FEMALE)
    k_.c.restore()
    return {"pam": _head(o, "pam")}


def s65_cast(t):
    td = drawn(t)

    def cast(k_):
        if td < 0.27:
            return pam_close(k_, "M", "neutral", (-0.6, 0.0))
        if td < 0.67:
            return pam_close(k_, "A", "doubt", (-0.6, 0.0))           # she opens her mouth to correct him
        u = seg(td, 0.67, 0.93)                                        # her eyes go up, to the glass (4 drawings)
        return pam_close(k_, "A", "doubt", (-0.6 + 1.3 * u, -0.7 * u))
    return cast


def s67_cast(t):
    td = drawn(t)

    def cast(k_):
        u = ease(seg(td, 0.0, 0.2))                                    # her eyes come back down
        look = (0.7 - 0.7 * u, -0.7 + 0.7 * u)
        if td < 0.13:
            return pam_close(k_, "A", "doubt", look)
        if td < 0.27:
            return pam_close(k_, "E", "neutral", look)                 # the mouth closing
        return pam_close(k_, "M", "neutral", (0.0, 0.0), drop=ease(seg(td, 0.27, 0.47)))   # shut: chosen
    return cast


def s68b_cast(t):
    td = drawn(t)

    def cast(k_):
        px, pf = 604, F + 60
        declare((("pam", "L", "quiet", "quiet"), ("pam", "R", "quiet", "quiet")), k_)
        shadow(k_, px, pf + 2, 32)
        look = (-1, 0.15) if td < 0.33 else (-1, -0.45)                # at his mic, then at him
        o = rig_hands(k_, lambda kk, a4: pam_held(kk, px, pf, SC["pam"], a4, "doubt", look, mug=False), SC["pam"], {},
                      sex="f", skin=FEMALE)
        return {"pam": _head(o, "pam")}
    return cast


# ---- 6.6 her view ----------------------------------------------------------------------------------------------------------
def s66_surface(t):
    import da_hand_gate as g
    td = drawn(t)
    cam0 = CAMS["6.6"][0]
    push = ease(seg(td, 0.0, 1.0))
    cam = (cam0[0], cam0[1], cam0[2] * (1 + 0.06 * push))
    office = dict(client="stand", sofia=False, roll="held", client_look=(0.6, 0.9))

    def light(k_, cam_):
        gr = cairo.RadialGradient(270, 500, 60, 270, 500, 340)
        gr.add_color_stop_rgba(0, 0, 0, 0, 0.0); gr.add_color_stop_rgba(0.4, 0, 0, 0, 0.0)
        gr.add_color_stop_rgba(1, 0.05, 0.04, 0.06, 0.55)
        k_.c.set_source(gr); k_.c.paint()

    def cast(k_):
        g.nohands()
        return {}
    return frame(cast, cam, office=office, tag=True, clips=6, near=light)


# ---- render, gate, sound ---------------------------------------------------------------------------------------------------
def render_shot(sid, t):
    if sid == "6.1":
        cast, back = s61_parts(t)
        return frame(cast, CAMS[sid][0], tag=True, clips=6, back=[back])
    if sid == "6.2":
        return frame(s62_cast(t), CAMS[sid][0], tag=True, clips=6)
    if sid == "6.3":
        return s63_surface(t)
    if sid == "6.4":
        return frame(s64_cast(t), CAMS[sid][0], tag=True, clips=6)
    if sid == "6.5":
        return frame(s65_cast(t), CAMS[sid][0], tag=True, clips=6)
    if sid == "6.6":
        return s66_surface(t)
    if sid == "6.7":
        return frame(s67_cast(t), CAMS[sid][0], tag=True, clips=6)
    if sid == "6.8":
        return frame(s68_cast(t), CAMS[sid][0], tag=True, clips=6)
    if sid == "6.8b":
        return frame(s68b_cast(t), CAMS[sid][0], tag=True, clips=6)
    raise KeyError(sid)


STARTS = {}
_acc = 0.0
for _s, _d in SHOTS:
    STARTS[_s] = _acc; _acc += _d

CUES = [
    (STARTS["6.1"] + 0.0, "quiet steps", 0.5),
    (STARTS["6.1"] + 0.6, "door", 0.3),
    (STARTS["6.2"] + 0.1, "paper", 0.5),
    (STARTS["6.8"] + 0.9, "mic tap", 0.4),
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
    for sid in TAKES:
        st, _, v, _ = env(sid)
        i = int((STARTS[sid] + st) * sr)
        m[i:i + len(v)] += (0.4 if sid == "6.8" else 0.6) * v[:max(0, n - i)] / (np.max(np.abs(v)) + 1e-9)
    m /= max(1.0, np.max(np.abs(m)) / 0.89)
    m.astype(np.float32).tofile(path)
    return path


GATED = tuple(s for s, _ in SHOTS)


def build():
    import subprocess
    from PIL import Image, ImageDraw
    import da_hand_gate as g
    import hands_v4 as hv
    import da_arms
    da_arms.setup(); hv.enable(); g.install(); cu.install(); A._SETUP.append(1)
    for sid, _ in SHOTS:
        if sid != "6.3":
            CAMS[sid] = camera_of(sid)
    tmp = "/tmp/da_anim_s6"; os.makedirs(tmp, exist_ok=True)
    for f_ in os.listdir(tmp):
        os.remove(os.path.join(tmp, f_))
    n = 0; marks = []; faults = []
    with ds.no_badges(), L.don_legs(), L.sofia_lib_hands(), L.face_guard():
        for sid, dur in SHOTS:
            marks.append((n, sid))
            for i in range(int(round(dur * FPS))):
                g.reset()
                surf = render_shot(sid, i / FPS)
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
    out = os.path.join(EP, "da_anim_s6_v%d.mp4" % VER)
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
    png = os.path.join(EP, "da_anim_s6_v%d_8fps.png" % VER)
    S.save(png)
    print("wrote", out, png, n, "frames")


if __name__ == "__main__":
    build()
