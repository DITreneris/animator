"""THE DOUBLE AGENT (episode 15): stage 7, scene 3 (3.1-3.5, 0:16.28-0:27.84), the 540 preview. Tomas 28 Nov
(/grill-me): 3.3 the Client's hand from the door's crack only; 3.4 Mom slides like a door (no steps); mouths now, on
the takes; commit and push after the scene passes its cold test and the hand gate.

  3.1  S3 MC: Don, not turning, lifts his empty cup over his shoulder upside down and shakes it twice; "Pam! Coffee."
  3.2  S6 M: Pam behind the counter tips the jug: the stream into HER mustard mug; his cup and saucer beside it
  3.2b I: the two cups: hers big and steaming, his tiny
  3.3  S7 M: Pam comes with both (her mug, his cup and saucer); the office door opens a hand's width; only the Client's
       hand comes out of the crack and takes her mug back in; she follows it on reflex, his cup still in her other
       hand. Behind, Mom gets up. "Pam. We need you." (from the door: no mouth seen)
  3.4  S7 M: the wall: Don on his toes behind Mom leans left: she slides left; right: she slides right; he feints
       (his head only): she doesn't move. Held on her; then "Your rule, sweetheart." (her mouth on the take)
  3.5  S8 MC: Pam's mustard mug set down before Father, her hand on it; its steam; he looks at it

  python3 da_anim_s3.py   ->  ../the-double-agent/da_anim_s3_v1.mp4, da_anim_s3_v1_8fps.png
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import da_cups as cu                                               # noqa: E402
import da_anim_s1 as A                                             # noqa: E402
import da_anim_s2 as B                                             # noqa: E402
import da_layouts as L                                             # noqa: E402
from da_layouts import F, MARKS, SC, dp, pm, ds, kit, rig_hands, shadow, _head  # noqa: E402
from da_motion import ease, ease_out, seg, frame, camera_of, FPS, DRAW  # noqa: E402

EP = os.path.join(HERE, "..", "the-double-agent")
VER = 10
T0 = 16.28
SHOTS = [("3.1", 1.61), ("3.2", 1.2), ("3.2b", 0.7), ("3.3", 2.4), ("3.4", 4.05), ("3.5", 1.6)]
drawn = A.drawn
CAMS = {}
TAKES = {"3.1": ("B", 0.15), "3.3": ("B", 0.6), "3.4": ("A", 2.0)}   # da_timing_v4's picks and take_at
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


def pam_held(kk, *a, **kw):
    """pm.pam under rig_hands: pm_ps sets kit.HAND to its own hand on every call, so the rig's hands were drawn too
    (the scene 3 gate: 'relax' x2 at her arm ends, under the library's); here its hand is the one rig_hands set."""
    import hands_ps as hp_
    cur, orig = kit.HAND[0], hp_.hand
    hp_.hand = cur
    try:
        return pm.pam(kk, *a, **kw)
    finally:
        hp_.hand = orig


def declare(rows, k_, props=()):
    import da_hand_gate as g
    g.jobs(*rows) if rows else g.nohands()
    for name, r in props:
        g.prop(k_, name, *r)


# ---- 3.1 -------------------------------------------------------------------------------------------------------------------
def s31_cast(t):
    td = drawn(t)

    def cast(k_):
        x, f = MARKS["don_counter"][0] + 24, MARKS["don_counter"][1]
        L.DON_FEET[0] = (x, f); s_ = SC["don"]
        shadow(k_, x, f + 2, 40)
        up = ease(seg(td, 0.0, 0.27))
        shake = 10 * math.sin(2 * math.pi * 2 * seg(td, 0.47, 0.93)) if 0.47 <= td < 0.93 else 0
        T = (x - 130 * s_ + shake + (1 - up) * 70 * s_, f - (400 - (1 - up) * 190) * s_)

        def cup_up(kk, P, w):
            c = kk.c; u = 1.35
            cx_, top = P[0] - 16 * u, P[1] - 4 * u
            kit.cut(kk, [(cx_ - 9 * u, top), (cx_ + 9 * u, top), (cx_ + 13 * u, top + 26 * u), (cx_ - 13 * u, top + 26 * u)],
                    (0.98, 0.98, 0.96), shadow=False, lw=1.8)
            kit.ellipse(kk, cx_, top + 26 * u, 13 * u, 3.6 * u, (0.86, 0.86, 0.84), 3101, shadow=False, lw=1.6)
            c.set_source_rgb(*kit.INK); c.set_line_width(4.2)
            c.new_path(); c.arc(cx_ + 12 * u, top + 12 * u, 6 * u, -1.4, 1.4); c.stroke()
            c.set_source_rgb(0.98, 0.98, 0.96); c.set_line_width(2.0)
            c.new_path(); c.arc(cx_ + 12 * u, top + 12 * u, 6 * u, -1.4, 1.4); c.stroke()
            import da_hand_gate as g_                                  # the cups canon: the cup itself says it's held
            g_.vessel(kk, "cup", "held", handle=P, base=(cx_, top),     # (upside down: its foot is up)
                      rect=(cx_ - 14 * u, top - 2 * u, 34 * u, 30 * u))
        declare((("don", "L", "pinch_pinky", "CUP_GRIP: the empty cup by its handle, up over his shoulder"),
                 ("don", "R", "quiet", "quiet")), k_)
        kit.MOUTH[0] = 0.8 if talking("3.1", t) else None
        try:
            o = rig_hands(k_, lambda kk, a4: dp.don(kk, x, f, s_, a4, "smug", (-0.4, -0.1), chin=1, hands=False), s_,
                          {-1: dict(T=T, pose="CUP_GRIP", out=-1, reach=True, obj=cup_up, contact="handle")})
        finally:
            kit.MOUTH[0] = None
        W_ = o["wrists"][-1]
        if 0.47 <= td < 0.93:                                          # the shake marks, only while it shakes
            c = k_.c; c.set_source_rgb(*kit.INK); c.set_line_width(2.2); c.set_line_cap(1)
            for r_ in (26, 34):
                c.new_path(); c.arc(W_[0] - 22, W_[1] + 18, r_, 2.6, 3.7); c.stroke()
            c.set_line_cap(0)
        return {"don": _head(o, "don")}
    return cast


# ---- 3.2 -------------------------------------------------------------------------------------------------------------------
def s32_parts(t):
    td = drawn(t)
    px, pf = 662, F - 128                                              # (a step back from the jug: the arm out, not folded)
    mug = (748, F - 156)
    tilt = 0.25 + 0.80 * ease(seg(td, 0.0, 0.27))
    pouring = td >= 0.27

    ms = cu.MUG_FLOOR * SC["pam"] / 0.54

    def pam_back(k_):                                                  # the cups canon: the jug by its handle
        T = (mug[0] - 50 - 4 * (1 - tilt), mug[1] - 84)
        declare((("pam", "R", "pinch_pinky", "CUP_GRIP: the jug by its handle"), ("pam", "L", "quiet", "quiet")), k_)
        got = {}
        o = rig_hands(k_, lambda kk, a4: pam_held(kk, px, pf, SC["pam"], a4, "neutral", (1, 0.9), mug=False), SC["pam"],
                      {1: cu.by_handle(T, 0.75, kind="jug", tilt_jug=tilt, got=got, out=1)}, sex="f", skin=L.FEMALE)
        L.STREAM[0] = got.get("lip")
        return {"pam": _head(o, "pam")}

    def cast(k_):
        h = {}
        cu.mug(k_, mug[0], mug[1], ms, handle=1, state="rest", name="mug")
        cu.cup_saucer(k_, mug[0] - 70, mug[1] - 2, cu.CUP_FLOOR, state="rest")
        if pouring and L.STREAM[0]:
            cu.stream(k_, L.STREAM[0], mug, ms, wob=1.5 * math.sin(td * 40))
        h["mug"] = (mug[0], mug[1] - 14, 16)
        return h
    return cast, pam_back


# ---- 3.2b ------------------------------------------------------------------------------------------------------------------
def s32b_surface(t):
    import cairo
    from kit import Ctx
    td = drawn(t)
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, L.W, L.H)
    c = cairo.Context(surf); k = Ctx(c, 0)
    c.set_source_rgb(*kit.WALL); c.paint()
    kit.cut(k, [(-20, 560), (560, 560), (560, 980), (-20, 980)], (0.93, 0.89, 0.80), lw=3)
    kit.cut(k, [(-20, 560), (560, 560), (560, 600), (-20, 600)], (0.86, 0.82, 0.72), shadow=False, lw=2)
    cu.mug(k, 190, 720, 6.0, handle=1, state="rest", name="mug")       # the cups canon's ceramic mug
    c.set_source_rgba(1, 1, 1, 0.75); c.set_line_width(7); c.set_line_cap(1)        # the steam, rising and curling
    for i, dx in enumerate((-40, 0, 40)):
        ph = td * 5 + i * 1.3
        c.new_path(); c.move_to(190 + dx, 500 - 10 * (ph % 1))
        c.curve_to(170 + dx + 8 * math.sin(ph), 440, 215 + dx - 8 * math.sin(ph), 400, 190 + dx + 6 * math.sin(ph * 1.3), 340)
        c.stroke()
    c.set_line_cap(0)
    cu.cup_saucer(k, 430, 720, 6.0 * cu.CUP_FLOOR / cu.MUG_FLOOR, state="rest")   # one size per space
    import da_hand_gate as g
    g.nohands()
    return surf


# ---- 3.3 -------------------------------------------------------------------------------------------------------------------
_S33 = {}                                                          # 3.3's drawings render in order


def s33_parts(t):
    td = drawn(t)
    x1, f = MARKS["pam_door"]
    mx0, my0 = 852, F - 66                                             # where the hand meets her mug: her waist (the layout's F-112 was over her shoulder)

    def mom_back(k_):
        rise = ease(seg(td, 1.0, 1.4))                                 # Mom gets up behind her desk
        mx, mf = MARKS["mom_desk_s"]
        k_.c.save(); k_.c.translate(0, 26 * (1 - rise))
        o = L.mom(k_, (mx, mf), "fists", "glare", look=(1, 0))
        k_.c.restore()
        return {"mom": o}

    def cast(k_):
        h = {}
        c = k_.c
        walk = seg(td, 0.0, 1.0)
        x = x1 - 40 - 26 * (1 - ease_out(walk))                        # stops a step short of the door: his hand must come
                                                                       # out to her (cold test s3: "a tiny dark hand")
        follow = ease(seg(td, 1.47, 2.13))                             # she follows her mug on reflex: pulled after it,
        x += 62 * follow                                               # leaning in, into the crack's mouth
        step = math.sin(math.pi * 2 * walk) if walk < 1 else 0
        bob = -4 * abs(step)
        crack = ease(seg(td, 0.73, 1.0))                               # a forearm's width, held open
        reach = ease(seg(td, 1.0, 1.27))                               # his hand out of the crack to her mug
        back = ease(seg(td, 1.33, 1.73))                               # and back in with it
        take = 1.26 <= td < 1.32                                       # one drawing: her fist on its handle, his on its body
        got = td >= 1.32                                               # then it's his: her hand opens after it
        cx_ = 898                                                      # the crack, at the door's hinge side
        ms = cu.MUG_FLOOR * SC["pam"] / 0.54
        cw = cu.hand_w(1.3 * SC["client"])                             # his hand (bigger: the cold test missed it)
        hand_out = reach > 0 and back < 1
        pT = (x + 36, f - 72) if not got else (x + 44 + 18 * follow, f - 80)   # her hand out to her right, toward the door
        cupT = (x - 16, f - 88)                                        # (cold test 28 Nov: further out, the camera cut it)
        rows = [("pam", "R", "pinch_pinky" if not got else "palm", "CUP_GRIP: her mug by its handle -> palm: after it"),
                ("pam", "L", "saucer_hold", "SAUCER_SUPPORT: his cup and saucer on her palm")]
        if hand_out:
            rows.append(("client", "R", "grab" if (take or got) else "palm",
                         "palm: reaching out of the crack -> GRAB: her mug's body, his thumb across its front"))
        declare(tuple(rows), k_)
        # the door: a dark sliver at its hinge side
        if crack > 0:
            kit.cut(k_, [(cx_ - 2, 470), (cx_ + 30 * crack, 470), (cx_ + 30 * crack, F), (cx_ - 2, F)], (0.12, 0.09, 0.08),
                    shadow=False, lw=1.4)
        shadow(k_, x, f + 2, 32)
        lean = 0.16 * follow
        hold = {}
        pj = {-1: cu.on_palm(cupT, cu.CUP_FLOOR, kind="cup", out=-1)}
        pj[1] = cu.by_handle(pT, ms, out=-1, name="mug", got=hold) if not got else \
            dict(T=pT, pose="PALM", out=1, reach=True)
        c.save(); c.translate(0, bob); c.translate(x, f); c.rotate(lean); c.translate(-x, -f)
        o = rig_hands(k_, lambda kk, a4: pam_held(kk, x, f, SC["pam"], a4, "doubt" if td < 1.27 else "shock",
                                                 (1, -0.2), mug=False), SC["pam"], pj, sex="f", skin=L.FEMALE)
        c.restore()
        h["pam"] = _head(o, "pam")
        if "base" in hold:
            _S33["base"] = hold["base"]
        B0 = _S33.get("base", (mx0 + 26, my0 + 14))                    # the mug's base where her hold had it
        B = None
        if got and back < 1:                                           # in his hand, back into the crack
            B = (B0[0] + (cx_ + 16 - B0[0]) * back, B0[1] - 6 * back)
        if hand_out:                                                   # his forearm out of the crack (the clean Client's
            import hand_lib_v4 as hl                                   # skin, his white T-shirt cuff)
            skin = (0.80, 0.66, 0.54)
            grip = B or B0
            if take or got:                                            # GRAB: fingers behind its wall, thumb in front
                HT = (grip[0] + 6 * ms + 0.86 * cw, grip[1] - 15 * ms)
            else:
                end = (B0[0] + 6 * ms + 0.86 * cw, B0[1] - 15 * ms)
                HT = (cx_ + 6 - (cx_ + 6 - end[0]) * reach, end[1])
            k_.c.save(); k_.c.rectangle(cx_ - 300, 0, 300 + 30 * max(crack, 0.3), 2000); k_.c.clip()
            kit.cut(k_, [(cx_ + 40, HT[1] - 12), (HT[0] - 4, HT[1] - 10), (HT[0] - 4, HT[1] + 10), (cx_ + 40, HT[1] + 12)],
                    skin, lw=2.2)                                     # the wrist into the hand: no gap to the cuff
            kit.cut(k_, [(cx_ + 40, HT[1] - 15), (cx_ + 6, HT[1] - 14), (cx_ + 6, HT[1] + 14), (cx_ + 40, HT[1] + 15)],
                    (0.97, 0.97, 0.95), lw=2.2)                       # his white T-shirt's sleeve, in the crack
            k_.c.restore()
            hl.draw_lr(k_, "GRAB" if (take or got) else "PALM", HT[0], HT[1], (-1, 0.0 if (take or got) else -0.4), cw,   # (retest: fingers up, clear of the crack)
                       skin, 1)
            if B:                                                      # the mug after his fingers: they're behind it
                cu.mug(k_, B[0], B[1], ms, handle=-1, state="held", name="mug")
            if take or B:
                cu.thumb_on_body(k_, grip[0], grip[1], ms, 1, cw, skin)
        h["mug"] = (mx0, my0 - 14, 16)
        return h
    return cast, mom_back


# ---- 3.4 -------------------------------------------------------------------------------------------------------------------
def s34_cast(t):
    td = drawn(t)

    def cast(k_):
        h = {}
        c = k_.c
        rx = MARKS["robot_pile"][0] + 40
        declare((("robot", "L", "robot_rest", "at rest"), ("robot", "R", "robot_grip", "gripper up, frozen"),
                 ("don", "L", "quiet", "quiet"), ("don", "R", "quiet", "quiet"),
                 ("mom", "L", "fist", "FIST: on her hip (Mom v1, the hand library)"),
                 ("mom", "R", "fist", "FIST: on her hip")), k_)
        L.rp.HEAD_ROT[0] = -0.105 * ease(seg(td, 0.6, 0.87))          # (review 28 Nov) frozen, gripper up: its head tips
        try:                                                           # 6 degrees, the smile identical
            h["robot"] = A.robot_canon(k_, rx, F + 64, {1: ("grip", (rx + 46, F + 64 - 150 * SC["robot"]))}, tilt=0.1,
                                       look=(-1, -0.4))
        finally:
            L.rp.HEAD_ROT[0] = None
        # Don: the leans (left, right), then the feint (his head only)
        lean_l = math.sin(math.pi * seg(td, 0.20, 0.67)) if 0.20 <= td < 0.67 else 0
        lean_r = math.sin(math.pi * seg(td, 0.87, 1.33)) if 0.87 <= td < 1.33 else 0
        feint = math.sin(math.pi * seg(td, 1.67, 1.87)) if 1.67 <= td < 1.87 else 0
        dxd = 0 * lean_l + 44 * lean_r                               # (left: the frame's edge; he tips his head out instead)                               # (cold test s3: the moves were too small)
        x, f = MARKS["don_peek"]; x += dxd
        L.DON_FEET[0] = (x, f)
        shadow(k_, x, f + 2, 36)
        c.save(); c.translate(0, -12 * SC["don"] / 0.6)
        ang = 0.12 - 0.20 * lean_l + 0.22 * lean_r - 0.34 * feint
        dface = "confused" if td < 2.0 else ("shock" if td < 2.6 else "confused")
        hd = {}
        c.translate(x, f); c.rotate(ang); c.translate(-x, -f)
        hd["h"] = rig_hands(k_, lambda kk, a4: dp.don(kk, x, f, SC["don"], a4, dface, (1, -0.8), chin=1, hands=False),
                            SC["don"], {})
        c.restore()
        hx, hy, r_ = _head(hd["h"], "don")
        h["don"] = (hx, hy - 12, r_)
        c.set_source_rgb(*kit.INK); c.set_line_width(1.8); c.set_line_cap(1)
        for ddx in (-14, 10):
            c.new_path(); c.move_to(x + ddx, f - 2); c.line_to(x + ddx, f - 10); c.stroke()
        c.set_line_cap(0)
        # Mom: slides like a door (no steps), a beat after him; never on the feint
        ul, ur = seg(td, 0.33, 0.80), seg(td, 1.0, 1.47)
        sl = -54 * math.sin(math.pi * ul) if 0 < ul < 1 else 0
        sr = 54 * math.sin(math.pi * ur) if 0 < ur < 1 else 0
        mx, mf = MARKS["mom_wall"]
        mx += 24                                                       # (her curler sat at his ear: "a phone?", cold test s3)
        for u_, sgn in ((ul, -1), (ur, 1)):                            # her slide's speed lines, behind her, while she moves
            if 0.1 < u_ < 0.6:
                c.set_source_rgb(*kit.INK); c.set_line_width(2.2); c.set_line_cap(1)
                bx = mx + 54 * sgn * math.sin(math.pi * u_)
                for yy in (-150, -110, -70):
                    c.new_path(); c.move_to(bx - sgn * 62, mf + yy * SC["mom"] / 0.6)
                    c.line_to(bx - sgn * 92, mf + yy * SC["mom"] / 0.6); c.stroke()
                c.set_line_cap(0)
        mouth = "E" if talking("3.4", t) else None                    # (review 28 Nov: a smaller mouth, ~-20 %)
        st34 = env("3.4")[0]                                           # "Your rule, sweetheart.": the fake sweetness, from
        mface = "sweetheart" if drawn(t) >= st34 - 0.07 else "unimpressed"   # the line on: the smile, her eyes unchanged
        h["mom"] = L.mom(k_, (mx + sl + sr, mf), "fists", mface, look=(-1, 0.2), chin=True, mouth=mouth)
        return h
    return cast


# ---- 3.5 -------------------------------------------------------------------------------------------------------------------
def s35_surface(t):
    td = drawn(t)
    mug_at = (304, 676)
    keep = L.s8_compose

    def compose(k_, **kw):
        h = keep(k_, **kw)
        c = k_.c                                                       # the steam off her mug
        c.set_source_rgba(1, 1, 1, 0.7); c.set_line_width(2.2); c.set_line_cap(1)
        for i, dx in enumerate((-6, 4)):
            ph = td * 4 + i * 1.7
            c.new_path(); c.move_to(mug_at[0] + dx, mug_at[1] - 30)
            c.curve_to(mug_at[0] + dx - 5 * math.sin(ph), mug_at[1] - 40, mug_at[0] + dx + 5 * math.sin(ph), mug_at[1] - 48,
                       mug_at[0] + dx, mug_at[1] - 58 - 4 * (ph % 1))
            c.stroke()
        c.set_line_cap(0)
        return h
    L.s8_compose = compose
    L.S8_MUG[0] = lambda k, x, y, s: cu.mug(k, x, y, s, handle=1, state="rest")   # Tomas 28 Nov: the ceramic mug, as 3.2-3.3
    try:
        surf, _ = L.render("3.5")
    finally:
        L.s8_compose = keep
        L.S8_MUG[0] = None
    return surf


# ---- render, gate, sound ---------------------------------------------------------------------------------------------------
def render_shot(sid, t):
    if sid == "3.1":
        return frame(s31_cast(t), CAMS[sid][0], tag=True, clips=24)
    if sid == "3.2":
        cast, back = s32_parts(t)
        return frame(cast, CAMS[sid][0], tag=True, clips=23, office=dict(client="stand", sofia=True), back=[back])
    if sid == "3.2b":
        return s32b_surface(t)
    if sid == "3.3":
        cast, back = s33_parts(t)
        return frame(cast, CAMS[sid][0], tag=True, clips=22)          # (cold test s3: Mom's head in the corner read
                                                                       # as the taker or a spy: she's out of 3.3)
    if sid == "3.4":
        return frame(s34_cast(t), CAMS[sid][0], tag=True, clips=20,
                     office=dict(client="stand", sofia=True, mug=True))   # (no Pam behind the glass: her arm sat at
                                                                           # Don's ear, "a phone?", cold test s3)
    if sid == "3.5":
        return s35_surface(t)
    raise KeyError(sid)


STARTS = {}
_acc = 0.0
for _s, _d in SHOTS:
    STARTS[_s] = _acc; _acc += _d

CUES = [
    (STARTS["3.2"] + 0.27, "pour", 0.8),
    (STARTS["3.2b"] + 0.0, "pour", 0.4),
    (STARTS["3.3"] + 0.73, "door", 0.7),
    (STARTS["3.3"] + 1.0, "chair scrape", 0.6),
    (STARTS["3.4"] + 0.33, "swishes", 0.7),
    (STARTS["3.4"] + 1.0, "swishes", 0.7),
    (STARTS["3.5"] + 0.1, "cup on saucer", 0.6),
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
        m[i:i + len(v)] += 0.6 * v[:max(0, n - i)] / (np.max(np.abs(v)) + 1e-9)
    m /= max(1.0, np.max(np.abs(m)) / 0.89)
    m.astype(np.float32).tofile(path)
    return path


GATED = ("3.1", "3.2", "3.2b", "3.3", "3.4")                       # 3.5: S8's locked layers, their own gate


def build():
    import subprocess
    from PIL import Image, ImageDraw
    import da_hand_gate as g
    import hands_v4 as hv
    import da_arms
    da_arms.setup(); hv.enable(); g.install(); cu.install(); A._SETUP.append(1)
    for sid, _ in SHOTS:
        if sid not in ("3.2b", "3.5"):
            CAMS[sid] = camera_of(sid)
    tmp = "/tmp/da_anim_s3"; os.makedirs(tmp, exist_ok=True)
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
    out = os.path.join(EP, "da_anim_s3_v%d.mp4" % VER)
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
    png = os.path.join(EP, "da_anim_s3_v%d_8fps.png" % VER)
    S.save(png)
    print("wrote", out, png, n, "frames")


if __name__ == "__main__":
    build()
