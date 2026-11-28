"""THE DOUBLE AGENT (episode 15): stage 7, scene 2 (2.1-2.4, 0:06.8-0:16.28), the 540 preview (Tomas 28 Nov:
"Proced" after scene 1 v20). The same pipeline as da_anim_s1 (its helpers: drawn, don_lib, robot_canon, the hand
gate on every drawing, the frame-synced sound): the layouts' worlds, marks and cameras; only the cast moves.

  2.1  S7 W: Don walks to his line (two steps, the bob, the toes stop at the tape) and stares; the robot crouched on
       Father's side picks clips, the gripper down and up twice (tik, tik). Inside the glass: the meeting as a still
       state (the background rule: the other space is a state).
  2.2  S8 M: Father's right foot already up on Don's desk; his left comes up, its heel nudges Don's gold desk photo
       (DON · CEO) over, face down (clack), and rests on it. "I paid for it." at 1.0 s (take A), his mouth on the take.
  2.3  S3 MC: Don's fists to his vest's hem, one hard tug down (vest snap), chin up, the stretch; held, offended.
  2.4  S3 M: Don raises the gift (the mustard mug, gold bow) to her; Pam's hand opens on her old blue mug: it falls
       and shatters at her feet; she takes the gift in both hands and holds it to her chest; Don turns away, pleased.

  python3 da_anim_s2.py   ->  ../the-double-agent/da_anim_s2_v1.mp4, da_anim_s2_v1_8fps.png
"""
import math
import os
import sys

import cairo

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import da_cups as cu                                              # noqa: E402
import da_anim_s1 as A                                             # noqa: E402
import da_layouts as L                                             # noqa: E402
from da_layouts import F, MARKS, SC, dp, pm, ds, kit, rig_hands, shadow, _head  # noqa: E402
from da_motion import ease, ease_out, seg, frame, camera_of, FPS, DRAW  # noqa: E402

EP = os.path.join(HERE, "..", "the-double-agent")
VER = 9
T0 = 6.8                                                           # the scene's start in the film
SHOTS = [("2.1", 1.5), ("2.2", 3.28), ("2.3", 1.2), ("2.4", 2.8)]
drawn = A.drawn
CAMS = {}

JOBS = {
    "2.1": lambda t: (("don", "L", "quiet", "quiet: walking"), ("don", "R", "quiet", "quiet"),
                      ("robot", "L", "robot_grip" if _pick(t)[0] > 0.05 else "robot_rest", "gripper: picking a clip"),
                      ("robot", "R", "robot_rest", "at rest")),
    "2.3": lambda t: (("don", "L", "clutch" if drawn(t) >= 0.20 else "quiet", "clutch: the vest's hem (an edge)"),
                      ("don", "R", "clutch" if drawn(t) >= 0.20 else "quiet", "clutch: the vest's hem")),
    "2.4": lambda t: _jobs24(t),
}


def declare(sid, k_, t, props=()):
    import da_hand_gate as g
    rows = JOBS[sid](t)
    g.jobs(*rows) if rows else g.nohands()
    for name, r in props:
        g.prop(k_, name, *r)


# ---- 2.1 -------------------------------------------------------------------------------------------------------------------
def _pick(t):
    """the robot's two picks: (how far down 0..1, the gripper closed on a clip)."""
    td = drawn(t)
    for t0 in (0.27, 0.87):                                           # (2.1 is 1.5 s now: story chain v1's budget)
        u = seg(td, t0, t0 + 0.6)
        if 0 < u < 1:
            down = math.sin(math.pi * u)
            return down, 0.3 < u < 0.75
    return 0.0, False


def s21_cast(t):
    td = drawn(t)

    def cast(k_):
        h = {}
        rx, _ = MARKS["robot_pile"]
        down, closed = _pick(t)
        clip = (rx - 46, F + 92)
        declare("2.1", k_, t, [("clip", (clip[0] - 12, clip[1] - 12, 24, 24))])
        jobs = {-1: ("grip", (clip[0] + 2, clip[1] - 30 + 26 * down))} if down > 0.05 else {}
        h["robot"] = A.robot_canon(k_, rx, F + 60, jobs, tilt=0.25 + 0.12 * down, look=(-0.3, 1))
        if closed or down < 0.05:                                     # the clip on the floor until it's taken
            if not closed:
                L.sd.paperclip(k_, clip[0], clip[1], L.CLIP_S, 0.5)
        x1, f = MARKS["don_s7"]
        walk = seg(td, 0.0, 0.93)                                     # two steps in, decelerating; the toes stop
        x = x1 - 120 * (1 - ease_out(walk))
        step = math.sin(math.pi * 2 * walk)
        bob = -6 * abs(step) if walk < 1 else 0
        knee = 0.32 * max(0.0, step) if walk < 1 else 0.0
        L.DON_FEET[0] = (x, f)
        shadow(k_, x, f + 2, 44)
        c = k_.c
        c.save(); c.translate(0, bob)
        br = 1 + 0.01 * math.sin(2 * math.pi * 1.1 * t)
        c.translate(x, f); c.scale(1, br); c.translate(-x, -f)
        face = "confused" if td < 1.0 else ("squint" if int(round(td * DRAW)) == 24 else "confused")
        h["don"] = A.don_lib(k_, x, f, face, (1, -0.5), knee=knee)
        c.restore()
        return h
    return cast


# ---- 2.2 (S8, inside Don's office) -------------------------------------------------------------------------------------------
TAKE22 = "A"


def _voice_env(path, start, sr=48000):
    """drawing -> loud enough to show an open mouth: the take's level per drawing (15/s)."""
    import numpy as np
    import soundfile as sf
    a, sr_ = sf.read(path)
    i = np.where(np.abs(a) > 0.02 * np.abs(a).max())[0]
    a = a[i[0]:i[-1]]
    step = int(sr_ / DRAW)
    lv = [float(np.sqrt(np.mean(a[j:j + step] ** 2))) for j in range(0, len(a), step)]
    top = max(lv)
    return start, [v > 0.18 * top for v in lv], a, sr_


ENV22 = None


def father_talks(t):
    global ENV22
    if ENV22 is None:
        ENV22 = _voice_env(os.path.join(HERE, "da_voices", "takes", "2.2_%s.wav" % TAKE22), 1.0)
    st, on, _, _ = ENV22
    n = int((drawn(t) - st) * DRAW)
    return 0 <= n < len(on) and on[n]


def feet_anim(t):
    """L.feet_on_desk, animated: the right foot already up; the left comes up from below the desk's edge, its heel
    nudges the standing gold photo (DON · CEO) over onto its face, then rests on it."""
    td = drawn(t)
    BLACK, BLACK_L = L.dc.BLACK, L.dc.BLACK_L
    up = ease(seg(td, 0.13, 0.53))                                    # the left leg rising onto the desk
    tip = ease(seg(td, 0.53, 0.73))                                   # the photo tipping over (clack at 0.73)

    def draw(k):
        c = k.c
        heads = {}
        # the photo: standing on its easel, then over onto its face (seen from its back as it goes)
        px, py = 300, 714
        if tip < 1:                                                   # (1.35x: a speck at phone size in cold test s2)
            c.save(); c.translate(px, py); c.scale(1.35, 1.35 * max(0.12, math.cos(tip * math.pi / 2)))
            kit.cut(k, [(-24, -50), (24, -50), (24, 0), (-24, 0)], (0.83, 0.66, 0.24), lw=2)
            kit.cut(k, [(-18, -44), (18, -44), (18, -6), (-18, -6)], (0.72, 0.82, 0.90), shadow=False, lw=1.4)
            if tip < 0.4:
                dp.don(k, 0, -6, 0.13, "stand", "smug", (0, 0))
                c.select_font_face(kit.FONT); c.set_font_size(6); c.set_source_rgb(*kit.INK)
                e = c.text_extents("DON · CEO"); c.move_to(-e.x_advance / 2, -1); c.show_text("DON · CEO")
            c.restore()
        else:
            kit.cut(k, [(267, 706), (334, 701), (338, 715), (264, 720)], (0.62, 0.48, 0.18), lw=2)      # face down (1.35x)
            kit.cut(k, [(272, 707), (329, 703), (331, 711), (270, 715)], (0.83, 0.66, 0.24), shadow=False, lw=1)
        kit.cut(k, [(304, 612), (368, 612), (372, 640), (300, 640)], BLACK, lw=2)                  # his lap
        for sx in (-1, 1):
            kit.cut(k, [(336 + sx * 4, 600), (336 + sx * 38, 598), (336 + sx * 40, 626), (336 + sx * 8, 630)], L.dc.VELVET,
                    shadow=False, lw=1.8)
        # the left foot's path: below the desk's edge -> up -> against the photo's top -> pressing it -> resting on it
        if tip <= 0:                                                  # from his lap (the knee drawn up) out over the desk
            fx_l, fy_l = (330 - 26 * up, 652 + 32 * up)               # to the photo's top
        else:
            fx_l, fy_l = (304 - 4 * tip, 684 + 6 * tip)               # pressing it over, then resting on it
        kn = (306 - 8 * (1 - up), 628 + 30 * up) if tip <= 0 else (308, 660)
        legs = (((318, 638), kn, (fx_l, fy_l), 4800, True),
                ((354, 638), (360, 658), (342, 678), 4810, True))
        for i, ((hx, hy), (kx, ky), (fx, fy), seed, shown) in enumerate(legs):
            if not shown:
                continue
            dp._cap(c, [(hx, hy), (kx, ky)], 30, BLACK, lw=2.2)
            dp._cap(c, [(kx, ky), (fx, fy - 18)], 26, BLACK, lw=2.2)
            c.set_source_rgb(*BLACK_L); c.set_line_width(1.6)
            c.new_path(); c.move_to(hx, hy + 2); c.line_to(kx, ky); c.line_to(fx, fy - 20); c.stroke()
            c.set_source_rgba(0, 0, 0, 0.30 if i == 0 else 0.28); c.save()
            c.translate(fx + (2 if i == 0 else -12), fy + (18 if i == 0 else 4)); c.scale(22 if i == 0 else 18, 5 if i == 0 else 9)
            c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
            L._sole_to_us(k, fx, fy, 19, 25, seed)
        heads["feet"] = (320, 684, 34)
        return heads
    return draw


def s22_surface(t):
    import dh_cast as dc
    keep_f, keep_father = L.feet_on_desk, dc.father
    talk = father_talks(t)
    td = drawn(t)                                                      # v2 (Tomas 28 Nov: the feet on the desk "look very
    reach = ease(seg(td, 0.13, 0.47)) - ease(seg(td, 0.8, 1.13))       # bad"): upright in Don's chair he leans in, one finger
    tip = ease(seg(td, 0.53, 0.73))                                    # on the photo's top, tips it onto its face (clack at
    z = L.PHOTO_AT[2]                                                  # 0.73), sits back; then "I paid for it."
    top = L.PHOTO_AT[1] - 50 * z * (max(0.10, math.cos(tip * math.pi)) if tip < 0.5 else 0.0)
    L.PHOTO22.update(reach=reach, tip=tip, feet=706 + 16 * reach, top=top)
    L.PHOTO22_MODE[0] = "finger"
    dc.father = lambda k, x, feet, s=1.0, pose="stand", face="hard", look=(0, 0), seed=1500: keep_father(
        k, x, feet, s, pose, "talk" if talk else face, look, seed)
    try:
        surf, _ = L.render("2.2")
    finally:
        L.feet_on_desk, dc.father = keep_f, keep_father
        L.PHOTO22_MODE[0] = "down_heel"
    return surf


# ---- 2.3 -------------------------------------------------------------------------------------------------------------------
def s23_cast(t):
    td = drawn(t)

    def cast(k_):
        x, f = MARKS["don_counter"]; L.DON_FEET[0] = (x, f)
        s_ = SC["don"]
        shadow(k_, x, f + 2, 40)
        declare("2.3", k_, t, [("hem L", (x - 50 * s_, f - 178 * s_, 34 * s_, 26 * s_)),
                               ("hem R", (x + 16 * s_, f - 170 * s_, 34 * s_, 26 * s_))])
        tug = seg(td, 0.27, 0.40)                                     # the hard tug: 2 drawings
        pull = 12 * math.sin(math.pi * tug) if 0 < tug < 1 else 0
        st = 1.0 + (0.035 if 0.33 <= td < 0.47 else (0.015 if td >= 0.47 else 0.0))   # the stretch, chin up
        c = k_.c
        c.save(); c.translate(x, f); c.scale(1, st); c.translate(-x, -f)
        br = 1 + 0.01 * math.sin(2 * math.pi * 1.1 * t)
        c.translate(x, f); c.scale(1, br); c.translate(-x, -f)
        if td < 0.20:                                                 # the hands come to the hem
            o = rig_hands(k_, lambda kk, a4: dp.don(kk, x, f, s_, a4, "confused", (1, -0.2), hands=False), s_, {})
        else:
            fc = "confused" if td < 0.67 else "smug"                  # offended through the tug (cold test s2), then smug
            o = rig_hands(k_, lambda kk, a4: dp.don(kk, x, f, s_, a4, fc, (1, -0.4), chin=1 if td >= 0.33 else 0,
                                                    hands=False), s_,
                          {-1: dict(T=(x - 34 * s_, f - (168 - pull) * s_), pose="CLUTCH", out=-1),
                           1: dict(T=(x + 34 * s_, f - (160 - pull) * s_), pose="CLUTCH", out=1)})
        if td >= 0.40:                                                # the crooked hem (the audit's cheap gag)
            kit.cut(k_, [(x - 46 * s_, f - 150 * s_), (x - 12 * s_, f - 156 * s_), (x - 14 * s_, f - 142 * s_)],
                    (0.14, 0.20, 0.33), shadow=False, lw=1.6)
        c.restore()
        return {"don": _head(o, "don")}
    return cast


# ---- 2.4 -------------------------------------------------------------------------------------------------------------------
# the cups canon (28 Nov, da_cup_sheet_v2): her blue mug by its handle; it slips (her hand opens, PALM) and falls free;
# his gift stands on his palm (SAUCER_SUPPORT); on the drawing he lets go she has it by its handle and his open hand is
# back at his side: never two people's hands on it in one drawing
def _jobs24(t):
    td = drawn(t)
    don_r = "saucer_hold" if td < 1.20 else "palm"
    pam_r = "pinch_pinky" if td < 0.80 else ("palm" if td < 1.20 else "quiet")
    pam_l = "quiet" if td < 0.93 else ("palm" if td < 1.20 else "pinch_pinky")
    return (("don", "R", don_r, "SAUCER_SUPPORT: the gift on his palm -> palm: let go, his hand back at his side"),
            ("don", "L", "quiet", "quiet"),
            ("pam", "R", pam_r, "CUP_GRIP: the blue mug by its handle -> palm: it slips -> quiet"),
            ("pam", "L", pam_l, "quiet -> palm: reaching for its handle (no touch) -> CUP_GRIP: the gift by its handle"))


def pam_held(*a, **kw):
    import da_anim_s3
    return da_anim_s3.pam_held(*a, **kw)


_GAVE = {}
_FELL = {"base": (690.0, 760.0)}                                # 2.4's drawings render in order


def s24_cast(t):
    td = drawn(t)

    def cast(k_):
        h = {}
        px, pf = MARKS["pam_counter"]
        x, f = MARKS["don_gift"]; L.DON_FEET[0] = (x, f)
        s_ = SC["don"]; sp = SC["pam"]
        ms = cu.MUG_FLOOR * sp / 0.54                                  # one size per space (the sheet)
        raise_ = ease(seg(td, 0.0, 0.40))                              # Don raises the gift to her chest height
        T = (px - 66, pf - 70)                                         # his palm's end point: in his reach, at her chest, clear of his face
        start = (x + 30 * s_, f - 150 * s_)
        give = (start[0] + (T[0] - start[0]) * raise_ ** 1.6, start[1] + (T[1] - start[1]) * raise_)   # up first, then out
        home = ease(seg(td, 1.33, 1.80))                               # she draws it to her chest
        if "off" not in _FELL:                                         # her hold's wrist -> the mug's base, measured once
            import da_hand_gate as g_
            from kit import Ctx
            pr = {}
            with g_.paused():
                kk = Ctx(cairo.Context(cairo.ImageSurface(cairo.FORMAT_RGB24, 8, 8)), 0)
                rig_hands(kk, lambda k2, a4: pam_held(k2, px, pf, sp, a4, "hopeful", (-1, 0.6), mug=False), sp,
                          {-1: cu.by_handle(T, ms, kind="gift", out=1, got=pr)}, sex="f", skin=L.FEMALE)
            _FELL["off"] = (pr["base"][0] - T[0], pr["base"][1] - T[1])
        gb = _FELL.get("gave", T)                                      # the gift's base on his palm, his last drawing
        take = (gb[0] - _FELL["off"][0], gb[1] - _FELL["off"][1])     # she takes it where it stands: it doesn't jump
        chest = (px - 26, pf - 100)
        hold = (take[0] + (chest[0] - take[0]) * home, take[1] + (chest[1] - take[1]) * home)
        fall = seg(td, 0.80, 1.07)                                     # the blue mug: slips, shatters at 1.07
        mug_hand = (px + 30, pf - 88)
        declare("2.4", k_, t, [])
        def pam_part():
            # Pam
            shadow(k_, px, pf + 2, 32)
            face = "doubt" if td < 0.80 else ("shock" if td < 1.20 else ("hopeful" if td < 2.2 else "doubt"))
            pj = {}
            if td < 0.80:
                pj[1] = cu.by_handle(mug_hand, ms, kind="blue", out=-1, name="blue mug", got=_FELL)
            elif td < 1.20:
                pj[1] = dict(T=mug_hand, pose="PALM", out=-1, reach=True)   # opens where it held (cold test: not at her hip)
            if 0.93 <= td < 1.20:                                      # her hand comes to its handle (retest: it "popped"
                r = ease(seg(td, 0.93, 1.20))                          # over); short of it: one owner a drawing
                hx_ = _FELL.get("gave", T)                             # the handle: the gift's base + the canon's offset
                hx_ = (hx_[0] + cu.HC * ms, hx_[1] - 15 * ms)
                pj[-1] = dict(T=(hx_[0] + 16 + 22 * (1 - r), hx_[1] + 4 + 26 * (1 - r)), pose="PALM", out=-1, reach=True)
            if td >= 1.20:
                pj[-1] = cu.by_handle(hold, ms, kind="gift", out=1, name="gift")
            op = rig_hands(k_, lambda kk, a4: pam_held(kk, px, pf, sp, a4, face, (-1, 0.6) if td < 1.6 else (-1, 0.9),
                                                     mug=False), sp, pj, sex="f", skin=L.FEMALE)
            h["pam"] = _head(op, "pam")
            if 0.80 <= td and fall < 1:                                    # free: it falls past her open hand, turning
                bx, by = _FELL["base"]; bx -= 12                          # where her last hold had it, at her open hand
                fy = by + 6 + (pf - by - 6) * fall * fall                  # already slipping on its first drawing
                c = k_.c; c.save(); c.translate(bx, fy - 15 * ms); c.rotate(2.2 * fall); c.translate(-bx, -(fy - 15 * ms))
                cu.mug(k_, bx, fy, ms, handle=1, kind="blue", state="free", name="blue mug")
                c.restore()
            if td >= 1.07:
                L.dpr.shards_v2(k_, px - 6, pf + 8, 0.6)

        def don_part():
            # Don
            turn = ease(seg(td, 1.27, 1.67))
            xd = x + 26 * raise_ - 26 * turn                               # a half step in to her with it (no straight arm)
            shadow(k_, xd, f + 2, 40)
            dface = "grin" if td < 1.20 else "pleased"
            if td < 1.20:
                dj = {1: cu.on_palm(give, ms, kind="gift", out=-1, handle=1, got=_GAVE)}
            else:                                                          # his open hand back at his own side
                dj = {1: dict(T=(xd + 44 * s_, f - 118 * s_), pose="PALM", out=-1, reach=True)}
            od = rig_hands(k_, lambda kk, a4: dp.don(kk, xd - 14 * turn, f, s_, a4, dface, (1 - 2 * turn, 0), hands=False),
                           s_, dj)
            h["don"] = _head(od, "don")

        for part in ((don_part, pam_part) if td >= 1.20 else (pam_part, don_part)):   # the gift in her hand: in front of him
            part()
        if "base" in _GAVE:
            _FELL["gave"] = _GAVE["base"]
        gp = give if td < 1.20 else hold
        h["gift"] = (gp[0], gp[1] - 20, 14)
        return h
    return cast


# ---- the frames, the gate, the sound -------------------------------------------------------------------------------------
def render_shot(sid, t):
    if sid == "2.1":
        return frame(s21_cast(t), CAMS[sid][0], tag=True, clips=28)
    if sid == "2.2":
        return s22_surface(t)
    if sid == "2.3":
        return frame(s23_cast(t), CAMS[sid][0], tag=True, clips=26)
    if sid == "2.4":
        return frame(s24_cast(t), CAMS[sid][0], tag=True, clips=25)
    raise KeyError(sid)


CUES = [  # (seconds in the scene, the animatic's FX word, gain)
    (0.20, "creak", 0.35),             # 2.1: the chair's creak behind the glass, muffled
    (0.55, "tik", 0.6), (1.15, "tik", 0.6),   # 2.1: the robot's two picks
    (1.5 + 0.73, "clack", 1.0),        # 2.2: the photo face down
    (4.78 + 0.33, "vest snap", 1.0),   # 2.3: the tug
    (5.98 + 1.07, "shatter", 1.0),     # 2.4: the blue mug
]


def mix(sec, path):
    import numpy as np
    import da_animatic as AN
    sr = AN.SR
    n = int(sec * sr)
    m = 0.004 * AN._lp(AN._noise(sec + 0.1), 200)[:n]
    for t0, word, gain in CUES:
        w = dict(AN.FX)[word]()
        if word == "creak":
            w = AN._lp(w, 900) if hasattr(AN, "_lp") else w
        i = int(t0 * sr)
        g = 0.18 * gain / (np.max(np.abs(w)) + 1e-9)
        m[i:i + len(w)] += g * w[:max(0, n - i)]
    _, _, v, _ = ENV22 or _voice_env(os.path.join(HERE, "da_voices", "takes", "2.2_%s.wav" % TAKE22), 1.0)
    i = int((2.2 + 1.0) * sr); m[i:i + len(v)] += 0.6 * v[:max(0, n - i)] / (np.max(np.abs(v)) + 1e-9)
    m /= max(1.0, np.max(np.abs(m)) / 0.89)
    m.astype(np.float32).tofile(path)
    return path


HITS = {'2.4': 1.07}   # shot -> the hit's time in it: a 3-drawing camera knock (Tomas 28 Nov)


def build():
    import subprocess
    from PIL import Image, ImageDraw
    import da_hand_gate as g
    import hands_v4 as hv
    import da_arms
    da_arms.setup(); hv.enable(); g.install(); cu.install(); A._SETUP.append(1)
    for sid, _ in SHOTS:
        if sid != "2.2":
            CAMS[sid] = camera_of(sid)
    tmp = "/tmp/da_anim_s2"; os.makedirs(tmp, exist_ok=True)
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
                if i % 2 == 0 and sid != "2.2":                        # 2.2: S8's locked layers, their own gate
                    faults += ["%s %.2fs  %s" % (sid, i / FPS, f) for f in g.check()]
                surf.write_to_png(os.path.join(tmp, "%04d.png" % n)); n += 1
    if faults:
        print("HAND GATE FAIL: %d" % len(faults))
        seen = set()
        for f in faults:
            key = f.split("  ")[1][:60]
            if key not in seen:
                seen.add(key); print("  " + f)
        raise SystemExit(1)
    print("hand gate: PASS on %d drawings" % (n // 2))
    out = os.path.join(EP, "da_anim_s2_v%d.mp4" % VER)
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
    png = os.path.join(EP, "da_anim_s2_v%d_8fps.png" % VER)
    S.save(png)
    print("wrote", out, png, n, "frames")


if __name__ == "__main__":
    build()
