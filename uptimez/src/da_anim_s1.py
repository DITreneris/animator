"""THE DOUBLE AGENT (episode 15): stage 7, scene 1 (1.1-1.5, 0:00-0:06.8), the 540 preview (Tomas 28 Nov: "darom";
1.3 keeps the pain hops, the release is not its own gag).

Drawings change 15 times a second, the frames at 30 fps. Every shot's world, rigs, marks and camera are the layouts'
(da_layouts, the cameras their framing search chose) and 1.1's are the locked S8r's (da_s8r v4 layout, canon hands):
only the cast moves. Nothing shared is changed: S8r's leg and roll drawers are swapped only inside this module's
1.1 render and put back after each frame.

  1.1  frame 0 held 0.4 s (the loop seam), then the back foot steps back onto the roll's tongue (thk), the tug goes on,
       he lifts the foot and the roll comes up with it; he looks down at it
  1.2  motion test E v2 (the shin whack)
  1.3  motion test F v2 (pain hops, then the shoes), with the roll on his raised sole (continuity from 1.2)
  1.3c his eyes follow the shoe, the eyebrow twitches twice
  1.3b the ringed hand hangs the tag; the tag swings and settles; the hand goes
  1.4  Sofia crosses with the box, it catches the armrest, the clips spill and land where the pile is from 1.5 on;
       she goes on out; the robot kneels; Don looks at the clips, then at the robot
  1.5  he grabs the roll on his sole, rips it off, drops it; it bounces once by the throne

  python3 da_anim_s1.py   ->  ../the-double-agent/da_anim_s1_v1.mp4 (540, with the animatic v2's sound for 0-6.8 s)
                              and da_anim_s1_v1_8fps.png (the strip)
"""
import math
import os
import random
import subprocess
import sys

import cairo

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import da_layouts as L                                             # noqa: E402
import da_motion as M                                              # noqa: E402
from da_layouts import F, MARKS, SC, dp, sd, ds, kit, rig_hands, shadow, _head, CLIP_S  # noqa: E402
from da_motion import ease, ease_out, seg, frame, camera_of, FPS, DRAW  # noqa: E402

EP = os.path.join(HERE, "..", "the-double-agent")
VER = 24
OOF_TAKE = "A"
SHOTS = [("1.1", 1.4), ("1.2", 0.8), ("1.3", 1.0), ("1.3c", 0.6), ("1.3b", 1.0), ("1.4", 1.2), ("1.5", 2.0)]


def drawn(t):
    """the drawing's time: 15 drawings a second."""
    return math.floor(t * DRAW + 1e-6) / DRAW


# ---- 1.1 (S8r) -----------------------------------------------------------------------------------------------------------
def s11_surface(t):
    import da_s8r as R
    td = drawn(t)
    if td < 0.4:                                                     # the seam: frame 0 itself
        return _s8r(R, None)
    step = ease(seg(td, 0.40, 0.60))                                 # 3 drawings: the back foot steps back onto the tongue
    up = ease(seg(td, 0.80, 1.07))                                   # 4 drawings: he lifts it, the roll comes with it
    jig = 3 * math.sin(td * 30) if td >= 1.07 else 0                 # the roll swinging under the shoe
    st = dict(dx=13 * step, lift=10 * math.sin(math.pi * step) + 46 * up, up=up, jig=jig, td=td, tailg=seg(td, 1.07, 1.33),
              face="shock" if td >= 0.67 else "confused", look=(0.4, 1.0) if td >= 0.67 else (-1, 0))
    return _s8r(R, st)


_SETUP = []


def _s8r(R, st):
    if not _SETUP:
        import hands_v4 as hv
        import da_hand_gate as g
        import da_arms
        da_arms.setup(); hv.enable(); g.install(); _SETUP.append(1)
    R.V2[0] = True; R.use("v4")
    legs0, roll0, tug0 = R._tug_legs, R.roll_on_floor, R.don_tug
    if st:
        R._tug_legs = lambda k, x, feet, s: _tug_legs(R, k, x, feet, s, st)
        R.roll_on_floor = lambda k: roll0(k) if st["up"] <= 0 else None
        R.don_tug = lambda k, arms, x=None, feet=None, s=None: _don_tug(R, k, arms, st)
    try:
        with ds.no_badges():
            surf, _ = R.render("start", scale=1)
    finally:
        R._tug_legs, R.roll_on_floor, R.don_tug = legs0, roll0, tug0
    return surf


def _tug_legs(R, k, x, feet, s, st):
    """R._tug_legs (narrow stance) with the screen-right (back) leg's foot moved by (dx, -lift)."""
    import don_v4 as dv
    c = k.c
    INK, cut = kit.INK, kit.cut
    c.save(); c.translate(x, feet); c.scale(s, s)
    w = dp.WAIST_Y
    dx, ly = st["dx"], -st["lift"]
    c.set_source_rgba(0, 0, 0, 0.22); c.save(); c.translate(-34, 2); c.scale(30, 5)
    c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
    c.set_source_rgba(0, 0, 0, 0.22 * (1 - min(1, st["lift"] / 40))); c.save(); c.translate(30 + dx, 2); c.scale(26, 5)
    c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
    legs = ([(-48, w - 2), (-1, w - 2), (-6, -10), (-52, -10)],
            [(1, w - 2), (48, w - 2), (52 + dx, -10 + ly), (6 + dx, -10 + ly)])
    shoes = ([(-56, -12), (-4, -12), (-2, 2), (-58, 2)],
             [(2 + dx, -12 + ly), (58 + dx, -12 + ly), (60 + dx, 2 + ly), (0 + dx, 2 + ly)])
    creases = (((-24, w + 14), (-31, -14)), ((26, w + 14), (29 + dx, -14 + ly)))
    for lg in legs:
        cut(k, lg, dv.KHAKI, shadow=False, lw=2)
    c.set_source_rgb(*INK); c.set_line_width(1.6)
    for a_, b_ in creases:
        c.move_to(*a_); c.line_to(*b_); c.stroke()
    for sh in shoes:
        cut(k, sh, R.SHOE, shadow=False, lw=2)
    c.restore()
    st["heel"] = (x + (6 + dx) * s, feet + (2 + ly) * s)            # the back shoe's heel corner, world
    st["sole"] = (x + (30 + dx) * s, feet + (2 + ly) * s)
    return x + 56 * s


def _tail(k, rx, cy, td, grow=1.0):
    """the roll's loose end, trailing and flapping (rough cut test 28 Nov, 3/3: the roll on his shoe read as "a wheel he
    kicks"): a ribbon of the line's own tape unwinding from it says tape."""
    w_ = math.sin(td * 14.0)
    L.tape_strip(k, [(rx - 13, cy + 10), (rx - 30 * grow, cy + (40 + 6 * w_) * grow + 10),
                     (rx - (52 + 9 * w_) * grow, cy + 56 * grow + 10), (rx - (74 - 7 * w_) * grow, cy + (50 - 5 * w_) * grow + 10)], 8.0)


def _don_tug(R, k, arms, st):
    """R.don_tug with the face and look of this drawing; then (once lifted) the roll hanging under the back sole."""
    c = k.c
    x, feet, s = R.L["DON_X"], R.L["DON_FEET"], R.DON[2]
    wy = feet + dp.WAIST_Y * s
    c.save()
    c.translate(x, wy); c.rotate(R.L["LEAN"]); c.translate(-x, -wy)
    c.rectangle(x - 400, feet - 2000, 800, 2000 + dp.WAIST_Y * s + 2); c.clip()
    o = dp.don(k, x, feet, s, arms, st["face"], st["look"], lean=0.0, hands=False)
    c.restore()
    _tug_legs(R, k, x, feet, s, st)
    if st["up"] > 0:
        rx0, rf, rs = R.L["ROLL"]
        r = (26 + 15) * rs
        sx, sy = st["sole"]
        hang = (sx + 10 + st["jig"], sy + r * 0.8)                     # the roll's centre under the sole
        cx = rx0 + (hang[0] - rx0) * st["up"]
        cy = (rf - r) + (hang[1] - (rf - r)) * st["up"]
        kit.cut(k, [(st["heel"][0] + 2, st["heel"][1] - 1), (st["heel"][0] + 10, st["heel"][1] + 1),
                    (cx + 4, cy - r + 6), (cx - 4, cy - r + 4)], L.pss.TAPE, shadow=False, lw=1.6)   # the tongue
        if st["up"] >= 1:                                              # (1.1's frame 0 and the loop seam untouched)
            _tail(k, cx, cy, st.get("td", 0.0), grow=min(1.0, st.get("tailg", 1.0)))
        c.save(); c.translate(cx, cy); c.scale(rs, rs)
        for col, lw in ((kit.INK, 30), (L.pss.TAPE, 25)):
            c.set_source_rgb(*col); c.set_line_width(lw); c.new_path(); c.arc(0, 0, 26, 0, 2 * math.pi); c.stroke()
        c.set_source_rgb(0.80, 0.62, 0.10); c.set_line_width(3); c.new_path(); c.arc(0, 0, 16, 0, 2 * math.pi); c.stroke()
        c.restore()
    return o


# ---- the hand canon in motion (Tomas 28 Nov, "darom": the gate on every drawing) ------------------------------------------
def robot_canon(k_, x, f, jobs, tilt=0.0, look=(0, 0)):
    """the robot (layouts' rp.robot at SC) with the canon's two hands (CANON.md: at rest and the gripper), as S8r's
    _robot_v2: the arms solved by two-bone IK for the shoulders the rig really draws, the elbow bent (no pole), the canon
    head drawn at each wrist with the elbow pin. jobs: {-1: ("rest" | "grip", T or None), 1: ...} by screen side;
    a rest arm with T None hangs, bent a little."""
    import da_s8r as r8
    import da_hand_gate as g
    s = SC["robot"]
    td = math.degrees(tilt)

    def measure(arms):
        out = []
        orig = kit.arm

        def arm(kk, sx, sy, a1, a2, col, skin, seed, ln=48, w=17):
            r = orig(kk, sx, sy, a1, a2, col, skin, seed, ln=ln, w=w)
            m = kk.c.get_matrix()
            out.append(((m.transform_point(sx, sy)[0] / 2, m.transform_point(sx, sy)[1] / 2),
                        (m.transform_point(*r)[0] / 2, m.transform_point(*r)[1] / 2), ln * math.hypot(m.xx, m.yx) / 2))
            return r
        kit.arm = arm
        try:
            r8._arm_log(lambda kk: L.rp.robot(kk, x, f, s, arms=arms, tilt=tilt, look=look))
        finally:
            kit.arm = orig
        return out
    base = measure(None)
    order = sorted(range(len(base)), key=lambda i: base[i][0][0])            # screen-left arm first
    side_of = {order[0]: -1, order[1]: 1}
    ang = [None, None]
    for i in range(2):
        S_, _, l_ = base[i]
        side = side_of[i]
        job, T = jobs.get(side, ("rest", None))
        if T is None:
            T = (S_[0] + side * 0.35 * l_, S_[1] + 1.82 * l_)
        a1, a2 = r8._ik(S_, T, l_, l_, side)
        if abs(a2) < 24:                                                         # never a pole: bend it
            a2 = 24 * (1 if a2 >= 0 else -1) if a2 != 0 else 24 * -side
        ang[i] = [a1 + td, a2]
    for _ in range(2):                                                           # the tilt's sign: measured, corrected
        got = measure(tuple(tuple(a) for a in ang))
        for i in range(2):
            side = side_of[i]
            job, T = jobs.get(side, ("rest", None))
            if T is None:
                continue
            S_, H_, l_ = got[i]
            e = math.degrees(math.atan2(T[0] - S_[0], T[1] - S_[1]) - math.atan2(H_[0] - S_[0], H_[1] - S_[1]))
            ang[i][0] += e
    wr = []
    orig = kit.arm

    def arm(kk, sx, sy, a1, a2, col, skin, seed, ln=48, w=17):
        r = orig(kk, sx, sy, a1, a2, col, skin, seed, ln=ln, w=w)
        fdir = math.radians(a1 + a2); e1 = math.radians(a1)
        wr.append((kk.c.get_matrix(), r, (math.sin(fdir), math.cos(fdir)), w, (sx + ln * math.sin(e1), sy + ln * math.cos(e1))))
        return r
    shadow(k_, x, f + 2, 36)
    kit.arm = arm
    try:
        o = L.rp.robot(k_, x, f, s, arms=tuple(tuple(a) for a in ang), tilt=tilt, look=look)
    finally:
        kit.arm = orig
    c = k_.c
    for i, (m, (hx, hy), d, w, (ex, ey)) in enumerate(wr[:2]):
        job = jobs.get(side_of[i], ("rest", None))[0]
        c.save(); c.set_matrix(m)
        c.new_path(); c.arc(ex, ey, 8 * w / 22.0, 0, 2 * math.pi); c.set_source_rgb(*kit.INK); c.fill()
        (g.robot_grip if job == "grip" else g.robot_rest)(k_, hx, hy, d, w)
        c.restore()
    return _head(o, "robot")


def don_lib(k_, x, f, face, look, jobs=None, knee=0.0, pose="stand", s_=None):
    """Don with the library's hands (rig_hands): arms with no job hang, RELAXED (the canon's quiet)."""
    s_ = s_ or SC["don"]
    o = rig_hands(k_, lambda kk, a4: dp.don(kk, x, f, s_, a4, face, look, knee=knee, hands=False), s_, jobs or {})
    return _head(o, "don")


def declare(sid, k_, t, extra=()):
    """this drawing's hand jobs (the-double-agent-hand-jobs-v1.md, scene 1) and the props a hand may hold."""
    import da_hand_gate as g
    rows = JOBS_S1[sid](t)
    g.jobs(*rows) if rows else g.nohands()
    for name, r in extra:
        g.prop(k_, name, *r)


JOBS_S1 = {
    "1.2": lambda t: (("don", "R", "clutch", "clutch: the throne's left armrest, held from 1.1"),
                      ("don", "L", "palm", "palm: the hand he lets go with, flung open by the whack")),
    "1.3": lambda t: ((("don", "L", "palm", "palm: arms out for balance, hopping"), ("don", "R", "palm", "palm: the same"))
                      if drawn(t) < 0.60 else (("don", "L", "quiet", "quiet: snapped upright, arms at his sides"),
                                               ("don", "R", "quiet", "quiet"))) + (
                      ("robot", "L", "robot_grip" if drawn(t) < 0.13 else "robot_rest", "gripper on the arm post -> at rest: lets go"),
                      ("robot", "R", "robot_rest", "at rest")),
    "1.3c": lambda t: (("don", "L", "quiet", "quiet"), ("don", "R", "quiet", "quiet")),
    "1.3b": lambda t: (("father", "R", "pinch" if drawn(t) < 0.47 else "palm",
                        "pinch: the tag's knot (Father sheet v6) -> palm: let go, leaving"),) if drawn(t) < 0.80 else
                      (),
    "1.4": lambda t: (("don", "L", "quiet", "quiet"), ("don", "R", "quiet", "quiet"),
                      ("sofia", "L", "clutch", "board_two: the box's left edge (her sheet v4 carry, the library's CLUTCH)"),
                      ("sofia", "R", "clutch", "board_two: the box's right edge"),
                      ("robot", "L", "robot_grip" if drawn(t) >= 0.60 else "robot_rest", "gripper at a clip / at rest"),
                      ("robot", "R", "robot_rest", "at rest")),
    "1.5": lambda t: (("don", "L", "quiet", "quiet"), ("don", "R", "quiet", "quiet: hands-free, he yanks it off with the foot")),
}


# ---- 1.2 (motion test E v2, then the cold test s1 v1 fixes, 28 Nov) -----------------------------------------------------
def s12_cast(t):
    """E v2 with: the tongue as flat tape (L.tape_strip); the contact held 2 drawings longer with bigger marks; then
    he grabs his shin with one hand and hops once on the hit leg's other foot."""
    s_ = SC["don"]
    x0, f = MARKS["don_hop"]
    arm = (L.TX - 66 * L.TS, F - 150 * L.TS)

    def bez(p0, p1, p2, u):
        return ((1 - u) ** 2 * p0[0] + 2 * u * (1 - u) * p1[0] + u * u * p2[0],
                (1 - u) ** 2 * p0[1] + 2 * u * (1 - u) * p1[1] + u * u * p2[1])

    def cast(k_):
        c = k_.c
        td = drawn(t)
        hop = seg(td, 0.67, 0.80)
        lift = 16 * math.sin(math.pi * hop) if 0 < hop < 1 else 0
        x = x0
        L.DON_FEET[0] = (x, f)
        shin = (x - 18 * s_, f - 70 * s_)
        up = ease(seg(td, 0.0, 0.20))
        kick = seg(td, 0.20, 0.40)
        hit = td >= 0.40
        knee = 0.45 + 0.55 * up if not hit else 1.0
        if 0.20 <= td < 0.40:
            knee = 1.0 - 0.35 * math.sin(math.pi * kick)
        sole = L.sole_of(x, f, s_, knee)
        hang = (sole[0] + 6, sole[1] + 40)
        ctrl = (sole[0] + 120, sole[1] - 110)
        if td < 0.20:
            roll = (hang[0] + 6 * math.sin(td * 40), hang[1])
        elif not hit:
            roll = bez(hang, ctrl, (shin[0] + 6, shin[1]), ease(kick))
        else:
            roll = (shin[0] + 6, shin[1])
        jolt = 0
        if hit and td < 0.60:
            jolt = 8 if td < 0.47 else 4
        face = "shock" if td < 0.20 else "panic" if td < 0.40 else ("squint" if td < 0.67 else "panic")
        look = (0.4, 1.0) if td < 0.40 else (0.6, 0.6)
        grab = td >= 0.53                                              # the hand goes to the shin
        declare("1.2", k_, t, [("armrest L", (arm[0] - 34, arm[1] - 20, 52, 34))])
        c.save(); c.translate(0, jolt - lift)
        shadow(k_, x, f + 2 - jolt + lift, 40 - lift)
        o = rig_hands(k_, lambda kk, a4: dp.don(kk, x, f, s_, a4, face, look, knee=knee, hands=False), s_,
                      {1: dict(T=(arm[0] - 10, arm[1] + 4 - jolt + lift), pose="CLUTCH", out=1, reach=True),
                       -1: dict(T=(x - (125 + (10 if grab and int(td * DRAW) % 2 else 0)) * s_, f - (215 if hit else 200) * s_),
                                pose="PALM", out=-1, reach=True)})        # (cold test s1 r2: shaken up high it read "grabs his head": hip height)        # (the shin grab can't reach: the hand shakes in pain instead)
        c.restore()
        if 0.33 <= td < 0.40:
            c.set_source_rgba(*L.INK, 0.55); c.set_line_width(2.0); c.set_line_cap(1)
            for i in range(3):
                pa = bez(hang, ctrl, (shin[0] + 6, shin[1]), 0.35 + 0.12 * i)
                c.new_path(); c.move_to(*pa); c.line_to(roll[0] + 10, roll[1] - 4 + 6 * i); c.stroke()
            c.set_line_cap(0)
        sy = -lift + (jolt if hit else 0)
        L.tape_strip(k_, [(sole[0] - 4, sole[1] - 1 + sy), ((sole[0] + roll[0]) / 2 + 8, (sole[1] + roll[1]) / 2 + 12 + sy),
                          (roll[0] + 14, roll[1] - 8 + sy)], 9.0)
        _tail(k_, roll[0], roll[1] + sy, td)
        L.roll_at(k_, roll[0], roll[1] + 18 + sy)
        if hit and td < 0.67:                                          # the hit marks: 4 drawings, bigger
            c.set_source_rgb(*L.INK); c.set_line_width(3.4); c.set_line_cap(1)
            big = td < 0.54
            for a_ in (-2.7, -2.2, -1.7, -1.2, 2.5, 2.0):
                r0, r1 = 26, (54 if big else 42)
                c.new_path(); c.move_to(shin[0] + r0 * math.cos(a_), shin[1] + 18 + r0 * math.sin(a_) + sy)
                c.line_to(shin[0] + r1 * math.cos(a_), shin[1] + 18 + r1 * math.sin(a_) + sy); c.stroke()
            c.set_line_cap(0)
        return {"don": _head(o, "don")}
    return cast


# ---- 1.3 with the roll on his raised sole --------------------------------------------------------------------------------
def s13_cast(t):
    """1.3 (F v2's timing): the robot's gripper on the throne's arm post, then it lets go (at rest); Don hops back
    twice with his arms out (palms), the roll on his raised sole; library hands, canon robot hands."""
    def cast(k_):
        h = {}
        s_ = SC["don"]
        x0, f = MARKS["don_hop"]
        td = drawn(t)
        rel = td >= 0.13
        hop = seg(td, 0.20, 0.53)
        x = x0 + 64 - 64 * ease(hop)
        lift = 34 * abs(math.sin(math.pi * 2 * hop)) if 0 < hop < 1 else 0
        dx = int(round(50 * (1 - ease(seg(td, 0.13, 0.40))))) if rel else 50
        post = (L.TX + 66 * L.TS + dx, F - 140 * L.TS)                 # the throne's right arm post
        declare("1.3", k_, t, [("arm post R", (post[0] - 8, post[1] - 20, 22, 46))])
        c = k_.c                                                       # Father's shadow first (28 Nov audit): it slides
        sh = ease(seg(td, 0.0, 0.13))                                  # in over the floor from the left, the robot sees it
        sx_ = 120 + 330 * sh + 60 * seg(td, 0.53, 0.93)                # and lets go; it stays, creeping with his walk
        c.save(); c.translate(sx_, F + 70); c.scale(230, 34)
        g_ = cairo.RadialGradient(0, 0, 0.2, 0, 0, 1); g_.add_color_stop_rgba(0, 0.10, 0.06, 0.08, 0.34)
        g_.add_color_stop_rgba(1, 0.10, 0.06, 0.08, 0.0)
        c.set_source(g_); c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.fill(); c.restore()
        if not rel:
            h["robot"] = robot_canon(k_, 590, F + 18, {-1: ("grip", (post[0] + 8, post[1]))}, tilt=0.14,
                                     look=(-1, 0.2 + 0.8 * sh))       # its eyes drop to the shadow
        else:
            h["robot"] = robot_canon(k_, 590, F + 18, {}, tilt=-0.05, look=(-1, 0.6))
        shadow(k_, x, f + 2, 40 - lift * 0.6)
        lean = -0.10 * math.sin(math.pi * hop) if 0 < hop < 1 else 0.0
        if not rel:
            lean -= 0.12
        k_.c.save(); k_.c.translate(0, -lift)
        wy = f - 150 * s_
        k_.c.save(); k_.c.translate(x, wy); k_.c.rotate(lean); k_.c.translate(-x, -wy)
        flap = 14 * math.sin(math.pi * 4 * hop) if 0 < hop < 1 else 0
        snap = td >= 0.60                                              # the owner's foot in: he snaps upright (28 Nov audit)
        if snap:
            st = 1.045 if td < 0.67 else 1.02                         # one drawing past it, then held
            k_.c.translate(x, f); k_.c.scale(1 / st ** 0.5, st); k_.c.translate(-x, -f)
        jobs_ = {} if snap else {-1: dict(T=(x - 105 * s_, f - (255 + flap) * s_), pose="PALM", out=-1, reach=True),
                                  1: dict(T=(x + 105 * s_, f - (255 - flap) * s_), pose="PALM", out=1, reach=True)}
        h["don"] = don_lib(k_, x, f, "shock", (1, -0.6) if td >= 0.53 else (-1, -0.2), knee=0.7, jobs=jobs_)
        k_.c.restore()
        sole = L.sole_of(x, f, s_, 0.7)
        L.tape_strip(k_, [(sole[0] - 4, sole[1]), (sole[0] + 2, sole[1] + 8)], 9.0)
        _tail(k_, sole[0] + 4, sole[1] + 12, td)
        L.roll_at(k_, sole[0] + 4, sole[1] + 30)
        k_.c.restore()
        L.DON_FEET[0] = (x, f)
        return h
    return cast


def s13_near(t):
    """Father's walk past the lens (28 Nov audit: weight, four poses): 8 drawings from 0.47, after Don's hops (one
    thing at a time), his shadow already on the floor since 0.0; the last is the rise toward the layout's key pose."""
    td = drawn(t)
    if td < 0.465:
        return None
    n = int(round((td - 0.4667) * DRAW))
    if n >= len(WALK):
        return lambda k_, cam_: L.father_step(k_, cam_)

    def near(k_, cam_, n=n):
        father_walk(k_, cam_, n)
    return near


# the walk's drawings (28 Nov audit, "kojų biomechanika"): entering -> contact (left) -> passing -> swing -> contact
# (right heel) -> down (weight, hips lowest) -> push-off (the trailing heel up) -> up. Feet planted on the floor never
# slide; the hips carry the weight (the bob), the body decelerates as he plants (heavy, sure).
WALK = [  # ox (hips, frame units), bob (+ = down), R foot (x off tx0, lift, toe angle), L foot (x off tx0, lift, angle)
    (-270, 0, (-250, 0, 0.0), (-360, 36, 0.22)),         # entering from the left edge: the left leg lifting behind
    (-170, 2, (-250, 30, 0.26), (-120, 0, -0.28)),       # the left heel down (contact); the right pushing off behind
    (-96, -6, (-120, 52, 0.30), (-120, 0, 0.0)),         # passing: the right leg swinging under him, the left planted
    (-72, -2, (-20, 40, 0.10), (-120, 0, 0.0)),          # the swing: reaching forward
    (-52, 2, (58, 0, -0.28), (-120, 0, 0.0)),            # contact: the right heel down, the toe up
    (-34, 14, (58, 0, 0.0), (-120, 6, 0.12)),            # down: the weight on the right, its knee bent; the left heel lifts
    (-18, 4, (58, 0, 0.0), (-112, 34, 0.26)),            # push-off: off the left toe
    (-6, -2, (58, 0, 0.0), (-96, 78, 0.34)),             # up: the left leg rising toward the key pose
]


def father_walk(k, cam, u):
    fx, fy, z = cam
    c = k.c
    ys = 652.0
    wy = fy + (ys - 480) / z
    tx0 = 270 + (L.tape_x(wy) - fx) * z
    BLK, BLK_L = L.dc.BLACK, L.dc.BLACK_L
    VEL, VEL_L = L.dc.VELVET, L.dc.VELVET_L
    n = min(len(WALK) - 1, max(0, int(u)))
    ox, bob, (rx, rl, ra), (lx, ll, la) = WALK[n]
    tx = tx0 + ox
    sway = 0.03 if n in (4, 5) else (-0.02 if n in (6, 7) else (-0.02 if n == 1 else 0.0))      # the pelvis tips over the weight-bearing leg
    hw = 0.22 if n <= 5 else (0.6 if n == 6 else 1.0)          # Tomas 28 Nov "tvarkom": the hips in profile while he walks
    hc = tx - 7                                                # (one pivot: the legs pass, they don't cross); he turns
    hipL, hipR = (hc - 47 * hw, 214 + bob), (hc + 47 * hw, 214 + bob)   # square to the lens over the last two drawings
    pR = (tx0 + rx, ys - 22 - rl)
    pL = (tx0 + lx, ys - 22 - ll)

    def knee(hip, foot, bend):
        mx, my = (hip[0] + foot[0]) / 2, (hip[1] + foot[1]) / 2
        return (mx + bend, my)
    kR = knee(hipR, pR, 26 if n == 5 else (18 if n in (1, 2, 3) else 8))
    kL = knee(hipL, pL, 30 if n >= 6 or n == 0 else (6 if n == 5 else 4))
    for p_, l_ in ((pR, rl), (pL, ll)):                                  # contact shadows: darker when planted
        if l_ < 10:
            c.set_source_rgba(0, 0, 0, 0.26)
            c.save(); c.translate(p_[0], ys + 4); c.scale(60, 8); c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
    jw = 0.55 + 0.45 * hw                                      # the body narrows in profile with the hips
    c.save(); c.translate(tx, 214 + bob); c.rotate(sway); c.scale(jw, 1); c.translate(-tx, -(214 + bob))
    kit.cut(k, [(tx - 98, 160 + bob), (tx + 86, 160 + bob), (tx + 82, 236 + bob), (tx - 94, 236 + bob)], BLK, lw=2.4)
    c.restore()
    FAR = (BLK[0] * 0.55, BLK[1] * 0.55, BLK[2] * 0.55)                  # the far leg: darker, a touch narrower (it
    L._leg(k, hipL, kL, pL, 70, 58, 52, FAR, BLK)                         # reads as behind when the legs cross in profile)
    L._oxford(k, pL[0] - 20, pL[1] + 16, 98, la, 4830, lift=ll > 10)
    L._leg(k, hipR, kR, pR, 76, 62, 56, BLK, BLK_L)
    L._oxford(k, pR[0] - 40, pR[1] + 16, 98, ra, 4820, lift=rl > 10)
    c.save(); c.translate(ox, bob); c.translate(tx0, 214); c.rotate(sway); c.scale(jw, 1); c.translate(-tx0, -214)   # the jacket
    t_ = tx0
    c.new_path()
    c.move_to(t_ - 172, 88); c.line_to(t_ + 160, 88); c.curve_to(t_ + 166, 150, t_ + 158, 196, t_ + 142, 214)
    c.curve_to(t_ + 100, 222, t_ + 40, 220, t_ + 6, 200); c.curve_to(t_ - 30, 222, t_ - 110, 224, t_ - 156, 214)
    c.curve_to(t_ - 172, 190, t_ - 178, 140, t_ - 172, 88); c.close_path()
    c.set_source_rgb(*VEL); c.fill_preserve(); c.set_source_rgb(*kit.INK); c.set_line_width(2.4); c.stroke()
    c.set_source_rgb(0.20, 0.04, 0.07); c.set_line_width(3.0)
    c.new_path(); c.move_to(t_ - 6, 88); c.curve_to(t_ - 2, 140, t_ + 2, 170, t_ + 6, 200); c.stroke()
    c.set_source_rgba(*VEL_L, 0.9); c.set_line_width(3.2); c.set_line_cap(1)
    for sx in (-1, 1):
        c.new_path(); c.move_to(t_ + sx * 140, 100); c.curve_to(t_ + sx * 148, 140, t_ + sx * 144, 180, t_ + sx * 132, 206)
        c.stroke()
    c.set_line_cap(0)
    c.restore()


# ---- 1.3c ----------------------------------------------------------------------------------------------------------------
def s13c_cast(t):
    td = drawn(t)

    def cast(k_):
        x, f = MARKS["don_hop"]; L.DON_FEET[0] = (x, f); s_ = SC["don"]
        shadow(k_, x, f + 2, 40)
        lx = -0.2 + 1.2 * ease(seg(td, 0.0, 0.27))                     # his eyes follow the shoe left to right
        declare("1.3c", k_, t)
        hx, hy, r_ = don_lib(k_, x, f, "shock", (lx, 0.9 - 0.3 * seg(td, 0.0, 0.27)), knee=1.0)
        sole = L.sole_of(x, f, s_)                                     # the roll still on his sole (1.2 -> 1.5)
        _tail(k_, sole[0] + 4, sole[1] + 12, td)
        L.roll_at(k_, sole[0] + 4, sole[1] + 30)
        d_ = int(round(td * DRAW))
        if d_ in (5, 7):                                               # the twitch: two drawings, a beat apart (28 Nov:
            L._twitch(k_.c, hx + 6, hy - r_ * 0.78, 2.0)              # bigger, and the eye under it narrows)
            _lid(k_.c, hx + r_ * 0.33, hy + r_ * 0.05, r_ * 0.30)
        elif td >= 0.33:
            L._twitch(k_.c, hx + 6, hy - r_ * 0.62, 1.3)
        return {"don": (hx, hy, r_)}
    return cast


def _lid(c, ex, ey, er):
    """the upper lid down over the top 60% of one eye (skin, an ink edge)."""
    c.save(); c.new_path(); c.arc(ex, ey, er * 1.12, 0, 2 * math.pi); c.clip()
    c.set_source_rgb(0.96, 0.78, 0.66); c.rectangle(ex - er * 1.3, ey - er * 1.3, er * 2.6, er * 1.3 + er * 0.25); c.fill()
    c.restore()
    c.set_source_rgb(*kit.INK); c.set_line_width(3.0); c.set_line_cap(1)
    c.new_path(); c.move_to(ex - er * 1.05, ey + er * 0.25); c.line_to(ex + er * 1.05, ey + er * 0.25); c.stroke(); c.set_line_cap(0)


# ---- 1.3b ----------------------------------------------------------------------------------------------------------------
def s13b_cast(t):
    td = drawn(t)
    TX, TS = L.TX, L.TS
    hx0, hy0 = TX - 56 * TS, F - 432 * TS

    def cast(k_):
        c = k_.c
        hang = td >= 0.27                                              # the hand brings it in (4 drawings), lets go
        ang = 0.0
        if hang:
            tt = td - 0.27
            ang = 0.35 * math.exp(-4.5 * tt) * math.cos(2 * math.pi * 2.2 * tt)   # the swing, settling
        come = ease(seg(td, 0.0, 0.27)); go = ease(seg(td, 0.47, 0.80))
        hx, hy = hx0 + 120 * (1 - come) + 220 * go, hy0 - 30 * (1 - come) - 40 * go
        c.save()
        if hang:
            c.translate(hx0, hy0); c.rotate(ang); c.translate(-hx0, -hy0)
        else:
            c.translate(hx - hx0, hy - hy0)
        L.tag_on_back(k_)
        c.restore()
        declare("1.3b", k_, t, [("tag knot", (hx0 - 14, hy0, 28, 34) if hang else (hx - 14, hy, 28, 34))])
        if td < 0.80:                                                  # Father's ringed hand (the hands canon, 28 Nov):
            import hand_lib_v4 as hl                                   # the library's PINCH at the knot, his velvet sleeve
            px, py = (hx0, hy0 + 12) if (hang and td < 0.47) else (hx, hy + 12)
            if td >= 0.47:                                             # it has let go: the hand open, leaving
                px, py = hx + 6, hy + 4
            d = (-0.97, 0.24)
            w = 17 * 1.15 * 1.25 * SC["father"]
            kit.cut(k_, [(px + 170, py - 44), (px + 170, py - 2), (px + 6, py + 7), (px - 1, py - 9)],
                    (0.45, 0.10, 0.16), lw=2)                         # the sleeve (velvet) up to the wrist, the cuff on it
            kit.cut(k_, [(px + 4, py - 10), (px + 11, py - 11), (px + 13, py + 8), (px + 6, py + 8)], (0.96, 0.94, 0.90), lw=1.6)
            hl.draw_lr(k_, "PINCH" if td < 0.47 else "PALM", px, py, d, w, L.MALE, 1)
            kit.ellipse(k_, px - 0.45 * w, py - 0.05 * w, 2.6, 2.6, (0.93, 0.74, 0.22), 4732, shadow=False, lw=1)   # the ring
        return {"tag": (hx0, hy0 + 30, 30)}
    return cast


# ---- 1.4 ----------------------------------------------------------------------------------------------------------------
def _spots():
    TX, TS = L.TX, L.TS
    r = random.Random(4710)
    sp = [(r.uniform(TX + 20, 700), F + r.uniform(4, 60), r.uniform(-3.1, 3.1)) for _ in range(30)]
    return sp[:29] + [(TX + 24 * TS, F + 6, 0.3)]


def s14_cast(t):
    td = drawn(t)
    TX = L.TX
    spots = _spots()
    catch = 0.33
    land = [catch + 0.10 + 0.45 * (i / 29.0) ** 0.8 for i in range(30)]

    def cast(k_):
        c = k_.c
        h = {}
        lookx = 1 if td < 0.4 else (0.6 if td < 0.8 else 1.0)
        looky = 0.5 if td < 0.4 else (1.0 if td < 0.8 else 0.6)
        dx_, df_ = MARKS["don_hop"]; L.DON_FEET[0] = (dx_, df_)
        shadow(k_, dx_, df_ + 2, 40)
        br = 1 + 0.012 * math.sin(2 * math.pi * 1.2 * t)               # breathing; a blink as the clips land; a flinch
        fl = 4 if catch + 0.07 <= td < catch + 0.20 else 0             # at the spill (micro-motion, 28 Nov audit)
        c.save(); c.translate(dx_, df_); c.scale(1, br); c.translate(-dx_ - fl, -df_)
        h["don"] = don_lib(k_, dx_, df_, "squint" if int(round(td * DRAW)) == 9 else "confused", (lookx, looky))
        c.restore()
        walk = seg(td, 0.0, 1.2)
        bx = TX + 30 + 62 * ease(seg(td, 0.0, catch)) + 160 * ease(seg(td, catch + 0.13, 1.2))
        bf = F + 40
        bob = 4 * abs(math.sin(math.pi * 4 * walk))
        jerk = 6 if catch <= td < catch + 0.13 else 0                   # the box caught on the armrest: she checks
        shadow(k_, bx, bf + 2, 32)
        c.save(); c.translate(-jerk, -bob)
        if catch <= td < catch + 0.13:                                  # two steps, stopped at the catch, then on
            ph = 0.5
        else:
            ph = 2.0 * (td / catch) * 0.5 if td < catch else 0.5 + 2.0 * (td - catch - 0.13) / (1.2 - catch - 0.13)
        legs = []
        for i in (0, 1):
            sw = math.sin(math.pi * 2 * ph + (0 if i == 0 else math.pi))
            legs.append((14 * sw, 10 * max(0.0, sw)))
        sd.ss.LEGS[0] = tuple(legs)
        try:
            o = sd.with_board(k_, bx, bf, SC["sofia"], "box", face_kind="smile", look=(1, 0),
                              full=0.5 * (1 - seg(td, catch, catch + 0.5)))
        finally:
            sd.ss.LEGS[0] = None
        c.restore()
        h["sofia"] = (o["head"][0], o["head"][1], L.R["sofia"] * SC["sofia"])
        import da_hand_gate as g_                                       # her carry: both hands clutch the box's edges
        (hlx, hly), (hrx, hry) = o["hands"]
        k_.c.save(); k_.c.translate(-jerk, -bob)
        g_.prop(k_, "box", hlx - 12, hly - 26, hrx - hlx + 24, 46)
        k_.c.restore()
        old = sd.CLIPS_V2[0]; sd.CLIPS_V2[0] = True                    # the clips in the air: from the box's corner
        try:
            src = (bx - 24 + jerk, bf - 120 * SC["sofia"] - bob)   # the box's tipped corner
            for i, (x, y, a) in enumerate(spots):
                t0 = catch + 0.02 * (i % 8)
                if t0 <= td < land[i]:
                    u = (td - t0) / (land[i] - t0)
                    px = src[0] + (x - src[0]) * u
                    py = src[1] + (y - src[1]) * u * u - 40 * math.sin(math.pi * u)
                    sd.paperclip(k_, px, py, CLIP_S, a + 8 * u)
        finally:
            sd.CLIPS_V2[0] = old
        kneel = ease(seg(td, 0.47, 0.73))                             # earlier and lower (cold test s1 v1)
        clip = (TX + 108, F + 64)                                      # the clip it reaches for (one of the pile's)
        declare("1.4", k_, t, [("clip", (clip[0] - 10, clip[1] - 8, 20, 16))])
        rj = {-1: ("grip", (clip[0] + 4, clip[1] - 6))} if td >= 0.60 else {}
        h["robot"] = robot_canon(k_, TX + 150, F + 70 + 14 * kneel, rj, tilt=0.45 * kneel, look=(-1, kneel))
        if td >= 0.60:
            sd.paperclip(k_, clip[0], clip[1], CLIP_S, 0.4)
        return h
    return cast


def s14_clips(t):
    td = drawn(t)
    catch = 0.33
    land = [catch + 0.10 + 0.45 * (i / 29.0) ** 0.8 for i in range(30)]
    return [i for i in range(30) if td >= land[i]]


# ---- 1.5 ----------------------------------------------------------------------------------------------------------------
def s15_cast(t):
    """1.5 v2 (Tomas 28 Nov /grill-me: "with physics: he kicks it, the tape runs out across the room, comes back and
    sticks again", to his other shoe, rewinding as it comes): hands-free still (his arm can't reach his sole). He plants
    the roll, kicks it away: it rolls off out of frame paying out a line of tape from his sole along the floor; he is
    pleased; the tape goes taut; the roll comes back up its own tape, winding it in; he hops the foot over it; it passes
    behind his legs and stops against his other shoe, the last of the tape across both ankles. He looks down."""
    td = drawn(t)

    def cast(k_):
        c = k_.c
        x, f = MARKS["don_hop"]; L.DON_FEET[0] = (x, f)
        s_ = SC["don"]
        if td < 0.27:
            knee = 1.0 - 0.65 * ease(seg(td, 0.0, 0.20))               # the stuck foot down, the roll on the floor
        elif td < 0.47:
            knee = 0.35 + 0.75 * math.sin(math.pi * seg(td, 0.27, 0.47)) * (1 if td < 0.40 else 0.7)   # the kick
        elif td < 1.33:
            knee = 0.06 + 0.29 * (1 - ease(seg(td, 0.47, 0.67)))       # down, standing (0.06: the same legs, with shoes)
        elif td < 1.67:
            knee = 0.06 + 0.8 * math.sin(math.pi * seg(td, 1.33, 1.67))   # the hop over it as it comes back
        else:
            knee = 0.06
        sole = L.sole_of(x, f, s_, knee)
        fl = f - 16                                                    # the roll's centre when it is on the floor
        start = (sole[0] + 8, fl)
        FAR = 640                                                      # out of frame, screen right
        END = (x - 56 * s_ - 15, fl)                                   # against the outside of his other shoe
        out_u, back_u = ease_out(seg(td, 0.40, 0.80)), ease(seg(td, 1.27, 1.6))
        if td < 0.27:
            roll = (sole[0] + 6, min(sole[1] + 14, fl))
        elif td < 0.40:
            roll = start
        elif td < 1.27:
            roll = (start[0] + (FAR - start[0]) * out_u, fl - 7 * abs(math.sin(math.pi * 2 * out_u)) * (1 - out_u))
        else:
            roll = (FAR + (END[0] - FAR) * back_u, fl)
        back = td >= 1.27 and roll[0] < x + 60                         # behind his legs while it passes them
        declare("1.5", k_, t)
        shadow(k_, x, f + 2, 40)
        if td < 0.27:
            face, look = "confused", (1, 0.9)
        elif td < 0.47:
            face, look = "squint", (1, 0.9)
        elif td < 1.13:
            face, look = "smug", (1, 0.5)                              # that's that
        elif td < 1.6:
            face, look = "shock", (1, 0.7)                             # the tape goes taut; it is coming back
        else:
            face, look = "confused", (-0.6, 1.0)                       # down at his other shoe
        rot = (roll[0] - start[0]) / 19.0 if td >= 0.40 else 0.0

        def tape():
            if td < 0.27:
                L.tape_strip(k_, [(sole[0] - 4, sole[1]), (sole[0], sole[1] + 6)], 9.0)
            elif td < 1.6:                                             # from his sole along the floor to the roll
                taut = 1.13 <= td < 1.27
                wob = 0 if taut or td >= 1.27 else 3 * math.sin(td * 40)
                mid = ((sole[0] + roll[0]) / 2, f + 1 + wob + (0 if knee < 0.2 else -6))
                L.tape_strip(k_, [(sole[0] - 2, sole[1] + 1), mid, (roll[0] - 8, f + 1)], 7.0)
            else:                                                      # the last of it: across both his ankles
                L.tape_strip(k_, [(sole[0] + 4, f - 5), (x - 20 * s_, f - 7), (END[0] + 8, f - 6)], 7.0)
        if back:
            tape(); L.roll_at(k_, roll[0], roll[1] + 18, rot=rot)
        br = 1 + 0.012 * math.sin(2 * math.pi * 1.2 * t)               # breathing
        c.save(); c.translate(x, f); c.scale(1, br); c.translate(-x, -f)
        h = {"don": don_lib(k_, x, f, face, look, knee=knee)}
        c.restore()
        if not back or td >= 1.6:
            tape(); L.roll_at(k_, roll[0], roll[1] + 18, rot=rot)
        c.set_source_rgb(*kit.INK); c.set_line_width(2.2); c.set_line_cap(1)
        if 0.40 <= td < 0.53:                                          # the kick's marks at his toe
            for a_ in (-0.5, 0.0, 0.5):
                c.new_path(); c.move_to(start[0] + 16 * math.cos(a_), start[1] + 16 * math.sin(a_))
                c.line_to(start[0] + 30 * math.cos(a_), start[1] + 30 * math.sin(a_)); c.stroke()
        if 0.47 <= td < 0.8 or 1.27 <= td < 1.6:                       # its speed lines, behind it
            sg = -1 if td < 1 else 1
            for yy in (-8, 4):
                c.new_path(); c.move_to(roll[0] + sg * 26, roll[1] + yy); c.line_to(roll[0] + sg * 48, roll[1] + yy); c.stroke()
        if 1.13 <= td < 1.27:                                          # taut: the line twangs
            for dx_ in (40, 90):
                c.new_path(); c.move_to(sole[0] + dx_, f - 7); c.line_to(sole[0] + dx_ + 6, f - 13); c.stroke()
        if 1.6 <= td < 1.8:                                            # it stops against his shoe
            for a_ in (2.4, 3.14, 3.9):
                c.new_path(); c.move_to(END[0] + 24 * math.cos(a_), END[1] + 24 * math.sin(a_))
                c.line_to(END[0] + 36 * math.cos(a_), END[1] + 36 * math.sin(a_)); c.stroke()
        c.set_line_cap(0)
        return h
    return cast


# ---- the sound, on the drawings (Tomas 28 Nov /grill-me: scene 1 synced now) --------------------------------------------
CUES = [  # (seconds, the animatic's FX word, gain): each on the drawing that makes it
    (0.00, "casters squeak", 0.5),     # the tug, through the seam
    (0.60, "thk", 1.0),                # 1.1: the back foot lands on the tongue (the step's last drawing)
    (0.87, "rip", 0.25),               # 1.1: the foot comes up, the tongue peels off the floor (short)
    (1.80, "thwack", 1.0),             # 1.2: the contact drawing (0.40 into the shot)
    (2.33, "slow heels", 0.6),         # 1.3: Father off screen; the robot lets go on the next drawing
    (3.53, "border beep", 0.8),        # 1.3c: the first twitch
    (4.07, "tag flick", 0.8),          # 1.3b: the hand lets go of the tag
    (5.13, "clatter", 1.0),            # 1.4: the box catches; the clips land
    (5.80, "tik", 0.6),                # 1.4: the robot's pincer
    (6.40, "thk", 0.8),                # 1.5 v2: the kick
    (6.42, "long peel", 0.5),          # the tape paying out as the roll runs off
    (7.13, "tik", 0.8),                # taut
    (7.27, "skrrt", 0.6),              # it comes back up its tape
    (7.60, "thk", 1.0),                # against his other shoe
]


def mix(sec, path):
    import numpy as np
    import da_animatic as A
    sr = A.SR
    n = int(sec * sr)
    m = 0.004 * A._lp(A._noise(sec + 0.1), 200)[:n]                    # the room tone (as the animatic's)
    for t0, word, gain in CUES:
        fn = dict(A.FX)[word]
        w = fn()
        if word == "rip" and t0 < 1:
            w = w[:int(0.12 * sr)]
        i = int(t0 * sr)
        g = 0.18 * gain / (np.max(np.abs(w)) + 1e-9)
        m[i:i + len(w)] += g * w[:max(0, n - i)]
    import soundfile as sf_                                           # Don's "Oof" on the contact drawing (take A, 28 Nov)
    v, _ = sf_.read(os.path.join(HERE, "da_voices", "takes", "1.2_%s.wav" % OOF_TAKE))
    v = v[int(0.3 * sr) - 240:]
    i = int(1.80 * sr); m[i:i + len(v)] += 0.55 * v[:max(0, n - i)]
    m /= max(1.0, np.max(np.abs(m)) / 0.89)
    m.astype(np.float32).tofile(path)
    return path


# ---- the frames ----------------------------------------------------------------------------------------------------------
def floor_frame(sid, cast, kw, near=None, clips_idx=None):
    cam, _ = CAMS[sid]
    if clips_idx is not None:                                         # 1.4: only the clips already landed
        def cast2(k_, base=cast):
            old = sd.CLIPS_V2[0]; sd.CLIPS_V2[0] = True
            try:
                for i in clips_idx:
                    x, y, a = _spots()[i]
                    sd.paperclip(k_, x, y, CLIP_S, a)
            finally:
                sd.CLIPS_V2[0] = old
            return base(k_)
        cast = cast2
    return frame(cast, cam, near=near, **kw)


CAMS = {}


def render_shot(sid, t):
    if sid == "1.1":
        return s11_surface(t)
    if sid == "1.2":
        return floor_frame(sid, s12_cast(t), dict(tag=False, clips=0))
    if sid == "1.3":
        dx = int(round(50 * (1 - ease(seg(t, 0.13, 0.40))))) if t >= 0.13 else 50
        td = drawn(t)                                                  # the throne rocks on its casters when it lurches
        rock = 0.06 * math.exp(-5.0 * (td - 0.20)) * math.sin(2 * math.pi * 2.4 * (td - 0.20)) if td >= 0.20 else 0.0
        orig = L.pss.throne                                            # (the crown wobbles: 28 Nov audit); this render only

        def rocking(k_, *a, **kw):
            x_, f_, _ = L.pss.THRONE
            k_.c.save(); k_.c.translate(x_, f_); k_.c.rotate(rock); k_.c.translate(-x_, -f_)
            try:
                return orig(k_, *a, **kw)
            finally:
                k_.c.restore()
        L.pss.throne = rocking
        try:
            return floor_frame(sid, s13_cast(t), dict(tag=False, clips=0, haze=0.18, throne_dx=dx), near=s13_near(t))
        finally:
            L.pss.throne = orig
    if sid == "1.3c":
        return floor_frame(sid, s13c_cast(t), dict(tag=False, clips=0))
    if sid == "1.3b":
        return floor_frame(sid, s13b_cast(t), dict(tag=False, clips=0))
    if sid == "1.4":
        return floor_frame(sid, s14_cast(t), dict(tag=True, clips=0), clips_idx=s14_clips(t))
    if sid == "1.5":
        return floor_frame(sid, s15_cast(t), dict(tag=True, clips=29))
    raise KeyError(sid)


HITS = {'1.2': 0.4, '1.5': 1.6}   # shot -> the hit's time in it: a 3-drawing camera knock (Tomas 28 Nov)


def build():
    from PIL import Image, ImageDraw
    for sid, _ in SHOTS:
        if sid != "1.1":
            CAMS[sid] = camera_of(sid)
    import da_hand_gate as g                                     # the hand gate on every drawing (Tomas 28 Nov)
    import hands_v4 as hv
    import da_arms
    da_arms.setup(); hv.enable(); g.install(); _SETUP.append(1)
    tmp = "/tmp/da_anim_s1"; os.makedirs(tmp, exist_ok=True)
    n = 0; marks = []; faults = []
    with ds.no_badges(), L.don_legs(), L.sofia_lib_hands(), L.face_guard():
        for sid, dur in SHOTS:
            marks.append((n, sid))
            for i in range(int(round(dur * FPS))):
                g.reset()
                surf = render_shot(sid, i / FPS)
                if sid in HITS:                                        # the hit's accent (da_motion.shaken)
                    surf = __import__("da_motion").shaken(surf, i / FPS - HITS[sid])
                if i % 2 == 0:                                         # a drawing (15/s): its hands checked
                    faults += ["%s %.2fs  %s" % (sid, i / FPS, f) for f in g.check()]
                surf.write_to_png(os.path.join(tmp, "%04d.png" % n)); n += 1
    if faults:
        print("HAND GATE FAIL: %d" % len(faults))
        for f in faults[:40]:
            print("  " + f)
        raise SystemExit(1)
    print("hand gate: PASS on %d drawings" % (n // 2))
    out = os.path.join(EP, "da_anim_s1_v%d.mp4" % VER)
    wav = mix(n / FPS, os.path.join(tmp, "mix.f32"))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", os.path.join(tmp, "%04d.png"),
                    "-f", "f32le", "-ar", "48000", "-ac", "1", "-i", wav, "-map", "0:v", "-map", "1:a",
                    "-vf", "format=yuv420p", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                    "-af", "loudnorm=I=-15:TP=-1.5:LRA=11", "-ar", "48000",
                    "-c:a", "aac", "-b:a", "160k", "-shortest", out], check=True)
    step = FPS // 8
    picks = list(range(0, n, step))
    tw, th, per = 200, 356, 18
    rows = (len(picks) + per - 1) // per
    S = Image.new("RGB", (per * (tw + 6) + 6, rows * (th + 30) + 6), (245, 244, 240)); d = ImageDraw.Draw(S)
    for j, i in enumerate(picks):
        im = Image.open(os.path.join(tmp, "%04d.png" % i)).convert("RGB").resize((tw, th), Image.LANCZOS)
        X, Y = 6 + (j % per) * (tw + 6), 6 + (j // per) * (th + 30)
        sid = [s for a, s in marks if a <= i][-1]
        S.paste(im, (X, Y + 22)); d.text((X + 2, Y + 4), "%d  %s  %.2fs" % (j + 1, sid, i / FPS), fill=(20, 20, 20))
    png = os.path.join(EP, "da_anim_s1_v%d_8fps.png" % VER)
    S.save(png)
    print("wrote", out, png, n, "frames")


if __name__ == "__main__":
    build()
