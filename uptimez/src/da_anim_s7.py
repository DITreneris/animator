"""THE DOUBLE AGENT (episode 15): stage 7, scene 7 (7.2-7.4, 0:55.39-1:05.34), the 540 preview. Tomas 28 Nov
(/grill-me, after "no gag built on sound"): 7.2's payoff is in the picture: Pam crosses his line in front of his bow,
the mask (6.8's page with its eye holes) at her face; 7.3's cause is in the picture: Don seen small through the glass
behind Father, bowing and waving; Father's eyes go to the glass (he doesn't turn), then "Let him play.".

  7.2  S3 MC: at his own line Don bows low, both palms rolled out toward the office; Pam walks across the tape in front
       of him, the mask at her face. "Approved."
  7.3  S8 MC: the Client slides MY GARAGES across the desk to Pam, "Don't lose it."; behind the glass Don waves her
       on; Father's eyes go to the glass and back; "Let him play."; he nods once
  7.4  S1 M: the robot, after the last clip under the throne's caster, rolls the throne toward the gap in his line;
       Don, proud, sees his chair going, lunges, clutches the armrest and hauls it back. "NOT THE CHAIR!"

  python3 da_anim_s7.py   ->  ../the-double-agent/da_anim_s7_v1.mp4, da_anim_s7_v1_8fps.png
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
import da_anim_s6 as S6                                            # noqa: E402
import da_layouts as L                                             # noqa: E402
from da_layouts import F, MARKS, SC, dp, sd, ds, kit, rig_hands, shadow, tilted, _head, FEMALE, CLIP_S, TX, TS  # noqa
from da_motion import ease, ease_out, seg, frame, camera_of, FPS, DRAW  # noqa: E402

EP = os.path.join(HERE, "..", "the-double-agent")
VER = 5
T0 = 55.39
SHOTS = [("7.2", 2.8), ("7.3", 4.15), ("7.4", 3.0)]
drawn = A.drawn
CAMS = {}
declare = C.declare
pam_held = C.pam_held
TAKES = {"7.2": ("7.2", "B", 1.0), "7.3a": ("7.3", "B", 0.8), "7.3b": ("7.3", "B", 2.35), "7.4": ("7.4", "B", 1.4),
         "7.4g": ("7.4", "C", 0.75)}                               # take -> (its shot, the pick, take_at)
ENV = {}


def env(name):
    if name not in ENV:
        _, letter, at = TAKES[name]
        ENV[name] = B._voice_env(os.path.join(HERE, "da_voices", "takes", "%s_%s.wav" % (name, letter)), at)
    return ENV[name]


def talking(name, t):
    st, on, _, _ = env(name)
    n = int((drawn(t) - st) * DRAW)
    return 0 <= n < len(on) and on[n]


def don_rig(x, f, face, look, s_=None):
    return lambda kk, a4: dp.don(kk, x, f, s_ or SC["don"], a4, face, look, hands=False)


# ---- 7.2 -------------------------------------------------------------------------------------------------------------------
def s72_cast(t):
    td = drawn(t)

    def cast(k_):
        import da_hand_gate as g_
        h = {}
        c = k_.c
        f = F + 70; x = L.tape_x(f) - 46; s_ = SC["don"]; L.DON_FEET[0] = (x, f)
        ang = 0.40 * ease(seg(td, 0.13, 0.53))                         # the bow, at the waist
        roll = ease(seg(td, 0.2, 0.67))                                # his arms roll out toward the office
        t_stick = 0.5 + 2.2 * (60 / 190.0)                             # when she is beside his bowed head
        carry = S6.ease(S6.seg(td, t_stick - 0.4, t_stick))             # she lifts it off her cardigan, in plain view
        HOLD = 0.4                                                     # (rough cut test 28 Nov, 3/3 "he took her star"): she
        stick = t_stick - 0.4 <= td < t_stick + HOLD + 0.07            # stops, her palm stays on his head 0.4 s, his eyes
        stuck = td >= t_stick + 0.07                                   # roll up at it; then she walks on
        seen = t_stick + 0.07 <= td < t_stick + HOLD + 0.27
        declare((("don", "L", "palm", "palm: rolled out toward the office"), ("don", "R", "palm", "palm"),
                 ("pam", "L", "pinch", "PINCH: the mask at her face"),
                 ("pam", "R", "palm" if stick else "quiet", "quiet -> palm: his tape medal pressed onto his bowed head")), k_)
        shadow(k_, x, f + 2, 40)
        jobs = {1: dict(T=(x + (60 + 130 * roll) * s_, f - (150 + 50 * roll) * s_), pose="PALM", out=1, reach=True),
                -1: dict(T=(x + (20 + 120 * roll) * s_, f - (130 + 30 * roll) * s_), pose="PALM", out=-1, reach=True)}
        kit.MOUTH[0] = 0.8 if talking("7.2", t) else None
        draw = lambda: rig_hands(k_, don_rig(x, f, "grin" if seen else "happy", (0.2, -1.0) if seen else (1, 0.3)), s_, jobs)
        hy = f - 150 * s_
        try:
            c.save(); c.rectangle(-5000, hy, 10000, 5000); c.clip()    # his legs, upright (L.bow, the gate paused for
            with g_.paused():                                          # this first pass)
                draw()
            c.restore()
            c.save(); c.rectangle(-5000, -5000, 10000, hy + 5000 + 2); c.clip()
            c.translate(x, hy); c.rotate(ang); c.translate(-x, -hy); o = draw(); c.restore()
        finally:
            kit.MOUTH[0] = None
        hx, hy0, r_ = _head(o, "don")
        dx, dy = hx - x, hy0 - hy
        h["don"] = (x + dx * math.cos(ang) - dy * math.sin(ang), hy + dx * math.sin(ang) + dy * math.cos(ang), r_)
        # Pam: across his line in front of him, the mask up, toward the office (screen right)
        tw = td if td < t_stick else (t_stick if td < t_stick + HOLD else
                                      t_stick + (td - t_stick - HOLD) * (2.7 - t_stick) / (2.7 - t_stick - HOLD))
        walk = seg(tw, 0.5, 2.7)
        px = L.tape_x(f + 30) - 92 + 190 * walk                       # from his side, over the tape, on toward the office
        pf = f + 30
        step = math.sin(math.pi * 2 * walk * 3) if not (t_stick <= td < t_stick + HOLD) else 0
        rigp = lambda k2, a4: pam_held(k2, px, pf, SC["pam"], a4, "neutral", (-1, -0.3) if stick else (1, 0.0), mug=False)
        with g_.paused():
            kk = kit.Ctx(cairo.Context(cairo.ImageSurface(cairo.FORMAT_RGB24, 8, 8)), 0)
            phx, phy, _ = _head(rig_hands(kk, rigp, SC["pam"], {}, sex="f", skin=FEMALE), "pam")
        pc = (phx, phy - S6.HOLE_DY + 1)
        pj = S6.pinch_at((pc[0] - 18, pc[1] + 28), rigp, SC["pam"], -1, -1, sex="f", skin=FEMALE)
        shadow(k_, px, pf + 2, 32)
        c.save(); c.translate(0, -3 * abs(step))
        dh = h["don"]
        top = (dh[0] + 6, dh[1] - dh[2] * 0.9)                         # the top of his bowed head
        pjobs = {-1: pj}
        if stick:
            a_ = (px + 34, pf - 96)
            hT = (a_[0] + (top[0] + 14 - a_[0]) * carry, a_[1] + (top[1] + 10 - a_[1]) * carry)
            pjobs[1] = dict(T=hT, pose="PALM", out=1, reach=True)
        op = rig_hands(k_, rigp, SC["pam"], pjobs, sex="f", skin=FEMALE)
        if not stuck:
            if stick:
                S6.medal(k_, hT[0] - 12, hT[1] - 8, ang=0.5 * carry, prop=True)
            else:
                S6.medal(k_, *S6.medal_at(px, pf))
        S6.page_holes(k_, pc[0], pc[1], 2)
        c.restore()
        if stuck:
            S6.medal(k_, top[0], top[1], ang=0.5)                      # his own line, on his own head
        h["pam"] = _head(op, "pam")
        return h
    return cast


# ---- 7.3 -------------------------------------------------------------------------------------------------------------------
_OUT = {}
_S73 = {}


def _out_don(pose, face):
    def fn(k):
        import da_s8r as r8
        shadow(k, 330, r8.FEET + 10, 70)
        dp.don(k, 330, r8.FEET + 8, 1.15, pose, face, look=(0, 0.2))
    return fn


OUTS = {"stand": _out_don((-8, 0, 8, 0), "happy"), "up": _out_don((-10, 0, 168, 0), "happy"),
        "out": _out_don((-8, 0, 130, 20), "happy")}


def s73_surface(t):
    import da_s8 as s8
    import dh_cast as dhc
    import da_hand_gate as g
    td = drawn(t)
    n = int(round(td * DRAW))
    if n in _S73:
        return _S73[n]
    slide = ease_out(seg(td, 0.27, 0.8))                               # the plan across the desk, from his side to hers
    wave = "stand" if td < 1.07 else ("up" if int(td * DRAW) // 3 % 2 else "out")   # Don behind the glass, waving her on
    glance = 1.33 <= td < 2.33                                         # Father's eyes to the glass, not his head
    talk = talking("7.3b", t)
    nod = 5.0 * math.sin(math.pi * seg(td, 3.3, 3.7)) if 3.3 <= td < 3.7 else 0.0
    keep_plan, keep_floor, keep_father = s8.PLAN_AT, L.s8r_floor, dhc.father
    s8.PLAN_AT = (keep_plan[0] - 96 * (1 - slide), keep_plan[1], keep_plan[2])

    def floor(cast):
        key = [k_ for k_, v in OUTS.items() if v is cast][0]
        if key not in _OUT:
            _OUT[key] = keep_floor(cast)
        return _OUT[key]

    busy = []

    def father(k, x, feet, s=1.0, pose="stand", face="hard", look=(0, 0), seed=1500):
        if nod and not busy:                                           # (the nod's two passes call father again)
            dhc.FATHER_NOD[0] = nod; busy.append(1)
        if glance:                                                     # (cold test: "never looks at the window") his eyes
            dhc.BROW_UP[0] = 6                                         # hard over and up, one brow with them
            return keep_father(k, x, feet, s, pose, "brow", (-1.0, -1.0), seed)
        return keep_father(k, x, feet, s, pose, "talk" if talk else face, look, seed)
    L.s8r_floor = floor; dhc.father = father
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, L.W, L.H)
    c = cairo.Context(surf); k = kit.Ctx(c, 0)
    c.set_source_rgb(*kit.WALL); c.paint()
    try:
        def draw(k_):
            hh = L.s8_compose(k_, pam_in=True, plan="open", client="over", outside=OUTS[wave])
            if 0.1 < slide < 0.95:                                     # its slide marks
                cc = k_.c; cc.set_source_rgb(*L.INK); cc.set_line_width(2.2); cc.set_line_cap(1)
                for yy in (652, 668, 684):
                    cc.new_path(); cc.move_to(s8.PLAN_AT[0] - 118, yy); cc.line_to(s8.PLAN_AT[0] - 92, yy); cc.stroke()
                cc.set_line_cap(0)
            return hh
        with g.paused():                                               # S8's layers: their own gate (as 3.5)
            L.crop(k, 1.12, 262, 548, draw)                           # (wider than the layout's 1.35: the glass and Don in it)
    finally:
        s8.PLAN_AT, L.s8r_floor, dhc.father = keep_plan, keep_floor, keep_father
        dhc.FATHER_NOD[0] = 0.0
    g.nohands()
    _S73[n] = surf
    return surf


# ---- 7.4 -------------------------------------------------------------------------------------------------------------------
STAR74 = [330, 600]


def _dx74(td):
    """the throne's roll: out toward the gap with the robot's pull, then hauled back and forth (cold test: 46 was
    "easy to miss": a chair's width now)."""
    if td < 1.07:
        return 84 * ease(seg(td, 0.13, 0.93))
    u = td - 1.07
    return 84 - 50 * ease(seg(u, 0.0, 0.33)) + 16 * math.sin(2 * math.pi * 1.6 * max(0.0, u - 0.33)) * (1 if u > 0.33 else 0)


def s74_cast(t):
    td = drawn(t)
    DX = _dx74(td)

    def cast(k_):
        h = {}
        c = k_.c
        clip = (TX + DX + 62 * TS, F + 4)                              # the last clip, under the throne's near caster:
        rx, rf = clip[0] + 58, F + 30                                  # the robot's gripper on it, hard by the chair (cold
                                                                       # test: apart from it, no link to the chair's roll)
        declare((("robot", "L", "robot_grip", "the gripper down on the clip"), ("robot", "R", "robot_rest", "at rest"),
                 ("don", "R", "quiet" if td < 1.0 else "clutch", "quiet -> CLUTCH: the throne's armrest"),
                 ("don", "L", "quiet" if td < 1.0 else "palm", "quiet -> palm: flung back for balance")), k_,
                [("clip", (clip[0] - 16, clip[1] - 22, 34, 30))])
        h["robot"] = A.robot_canon(k_, rx, rf, {-1: ("grip", (clip[0] + 2, clip[1] - 12))}, tilt=-0.35, look=(-1, 0.9))
        old = sd.CLIPS_V2[0]; sd.CLIPS_V2[0] = True
        try:
            sd.paperclip(k_, clip[0], clip[1], CLIP_S * 2.6, 0.3)
        finally:
            sd.CLIPS_V2[0] = old
        c.set_source_rgb(1, 0.95, 0.55); c.set_line_cap(1)             # its glint: the thing it wants
        for a_ in range(8):
            r0, r1 = (16, 30) if a_ % 2 == 0 else (14, 22)
            c.set_line_width(3.0 if a_ % 2 == 0 else 2.0)
            c.new_path(); c.move_to(clip[0] + r0 * math.cos(a_ * 0.785), clip[1] - 8 + r0 * math.sin(a_ * 0.785))
            c.line_to(clip[0] + r1 * math.cos(a_ * 0.785), clip[1] - 8 + r1 * math.sin(a_ * 0.785)); c.stroke()
        c.set_line_cap(0)
        if 0.13 < td < 0.93 or td > 1.4:                               # the casters' roll marks
            c.set_source_rgb(*L.INK); c.set_line_width(1.8); c.set_line_cap(1)
            sgn = 1 if td < 1.07 else (1 if math.cos(2 * math.pi * 1.6 * (td - 1.4)) > 0 else -1)
            for yy in (F - 6, F + 2):
                c.new_path(); c.move_to(TX + DX - sgn * 70 * TS, yy); c.line_to(TX + DX - sgn * 96 * TS, yy); c.stroke()
            c.set_line_cap(0)
        h["clip"] = (clip[0], clip[1], 20)
        s_ = SC["don"]
        f = F + 64
        arm = (TX + DX - 66 * TS, F - 150 * TS)                        # the near armrest, where the chair is now
        lunge = ease_out(seg(td, 0.8, 1.0))
        grab_x = arm[0] - 52                                           # where his arm reaches the armrest (58 long)
        x = 330 + (grab_x - 330) * lunge if td < 1.07 else grab_x      # then he goes with the chair, hauling
        L.DON_FEET[0] = (x, f)
        shadow(k_, x, f + 2, 44)
        if td < 0.53:
            face, look, lean, jobs = "happy", (-1, 0.0), 0.0, {}       # proud, his eyes shut, turned from it
        elif td < 0.8:
            face, look, lean, jobs = "shock", (1, -0.1), 0.0, {}       # he sees it going
        else:
            face, look = "panic", (1, -0.1)
            lean = 0.14 * lunge if td < 1.07 else -0.10                # in for the grab, then back on his heels
            ca, sa = math.cos(-lean), math.sin(-lean)

            def loc(p):
                dx, dy = p[0] - x, p[1] - f
                return (x + dx * ca - dy * sa, f + dx * sa + dy * ca)
            jobs = {} if td < 1.0 else {1: dict(T=loc((arm[0] - 4, arm[1] - 2)), pose="CLUTCH", out=1, reach=True),
                                         -1: dict(T=(x - 50, f - 150), pose="PALM", out=-1, reach=True)}
            # (one hand on the armrest, the other flung back for balance: both on it put an arm across his chest)
            if td >= 1.0:
                import da_hand_gate as g_
                g_.prop(k_, "armrest", arm[0] - 30, arm[1] - 20, 60, 50)
        kit.MOUTH[0] = 1.0 if (talking("7.4", t) or talking("7.4g", t)) else None
        try:
            o = tilted(k_, x, f, lean, lambda: rig_hands(k_, don_rig(x, f, face, look), s_, jobs))
        finally:
            kit.MOUTH[0] = None
        h["don"] = _head(o, "don")
        hd = h["don"]                                                  # (rough cut test: the star on his head in 7.2 was gone
        if td < 0.8:                                                   # here) it rides on his head; the lunge throws it off
            STAR74[:] = [hd[0] + 4, hd[1] - hd[2] * 0.92]
            S6.medal(k_, STAR74[0], STAR74[1], ang=0.3)
        else:
            u = min(1.0, (td - 0.8) / 0.47)
            sx_ = STAR74[0] - 46 * u
            sy_ = min(f + 6, STAR74[1] - 60 * u + 330 * u * u)
            S6.medal(k_, sx_, sy_, ang=0.3 - 5.0 * u if u < 1 else 0.1)
        return h
    return cast, DX


# ---- render, gate, sound ---------------------------------------------------------------------------------------------------
def render_shot(sid, t):
    if sid == "7.2":
        return frame(s72_cast(t), CAMS[sid][0], tag=True, clips=1, office=dict(client="seated", sofia=True, roll="held"))
    if sid == "7.3":
        return s73_surface(t)
    if sid == "7.4":
        cast, DX = s74_cast(t)
        return frame(cast, CAMS[sid][0], tag=False, clips=0, office=dict(client="seated", sofia=False, pam="with_plan"),
                     throne_dx=DX if abs(DX) > 0.5 else 0.5)
    raise KeyError(sid)


STARTS = {}
_acc = 0.0
for _s, _d in SHOTS:
    STARTS[_s] = _acc; _acc += _d

CUES = [
    (STARTS["7.2"] + 0.4, "quiet steps", 0.5),
    (STARTS["7.3"] + 0.27, "paper slide", 0.8),
    (STARTS["7.4"] + 0.13, "casters", 0.7),
    (STARTS["7.4"] + 1.07, "squeaks of the tug", 0.8),
    (STARTS["7.4"] + 1.9, "tug's squeak", 0.7),
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
    for name, (sid, _, _) in TAKES.items():
        st, _, v, _ = env(name)
        i = int((STARTS[sid] + st) * sr)
        m[i:i + len(v)] += 0.6 * v[:max(0, n - i)] / (np.max(np.abs(v)) + 1e-9)
    m /= max(1.0, np.max(np.abs(m)) / 0.89)
    m.astype(np.float32).tofile(path)
    return path


GATED = ("7.2", "7.4")                                             # 7.3: S8's layers, their own gate


HITS = {'7.4': 1.07}   # shot -> the hit's time in it: a 3-drawing camera knock (Tomas 28 Nov)


def build():
    import subprocess
    from PIL import Image, ImageDraw
    import da_hand_gate as g
    import hands_v4 as hv
    import da_arms
    da_arms.setup(); hv.enable(); g.install(); cu.install(); A._SETUP.append(1)
    for sid in ("7.2", "7.4"):
        CAMS[sid] = camera_of(sid)
    tmp = "/tmp/da_anim_s7"; os.makedirs(tmp, exist_ok=True)
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
    out = os.path.join(EP, "da_anim_s7_v%d.mp4" % VER)
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
    png = os.path.join(EP, "da_anim_s7_v%d_8fps.png" % VER)
    S.save(png)
    print("wrote", out, png, n, "frames")


if __name__ == "__main__":
    build()
