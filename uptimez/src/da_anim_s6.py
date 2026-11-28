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
VER = 10
T0 = 43.44
SHOTS = [("6.1", 1.4), ("6.2", 1.2), ("6.3", 1.0), ("6.4", 2.23), ("6.5", 1.0), ("6.6", 1.0), ("6.7", 1.1),
         ("6.8", 2.72), ("6.8b", 0.6)]
drawn = A.drawn
CAMS = {}
declare = C.declare
pam_held = C.pam_held
TAKES = {"6.2": ("B", 0.6), "6.4": ("B", 0.6)}   # da_timing_v4's picks and take_at; 6.8's "Keep infiltrating." dropped
                                                   # (Tomas 28 Nov /grill-me: the mask gag carries the beat on mute)
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


MEDAL_ANG = [-0.34]                                                # as he slapped it on: crooked, until she straightens it


def medal(k, x, y, ang=None, prop=False):
    """a short strip of his own yellow tape (Tomas 28 Nov /grill-me: "the tape medal"): stuck on his spy's chest."""
    import ps_set as pss
    c = k.c
    ang = MEDAL_ANG[0] if ang is None else ang
    c.save(); c.translate(x, y); c.rotate(ang)
    kit.cut(k, [(-13, -6), (13, -6), (13, 6), (-13, 6)], pss.TAPE, shadow=False, lw=1.8)
    c.set_source_rgb(0.13, 0.11, 0.12)                                 # (cold test 28 Nov: both took a blank strip for a sticky
    for i in range(10):                                                # note) his pen star on it: a decoration
        r_ = 4.6 if i % 2 == 0 else 1.9
        a_ = -math.pi / 2 + i * math.pi / 5
        (c.move_to if i == 0 else c.line_to)(r_ * math.cos(a_), r_ * math.sin(a_))
    c.close_path(); c.fill()
    c.restore()
    if prop:
        import da_hand_gate as g_
        g_.prop(k, "tape strip", x - 14, y - 10, 28, 20)


def medal_at(px, pf):
    return (px - 9, pf - 104)                                          # on her cardigan, over her heart


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
    """v2 (Tomas 28 Nov /grill-me: a gag for 6.1-6.7, "the tape medal"): suspicion -> delight, and he decorates her: a
    strip of his own yellow tape out of his vest pocket, pressed onto her cardigan like a medal, one pat. She looks down
    at it. A two-shot now (6.2's camera). "You're spying for me?" """
    td = drawn(t)

    def cast(k_):
        h = {}
        x0, f = MARKS["don_counter"][0] + 24, MARKS["don_counter"][1]
        s_ = SC["don"]
        px, pf = 626, F + 60
        M = medal_at(px, pf)
        joy = td >= 0.47
        step = ease(seg(td, 0.8, 1.13))                                # a half step in to her with it
        x = x0 + 16 * step - 16 * ease(seg(td, 1.47, 1.8)); L.DON_FEET[0] = (x, f)
        has = 0.6 <= td < 1.2                                          # the strip in his fingers
        pat = 1.2 <= td < 1.4
        on_her = td >= 1.2
        rows = [("don", "R", "pinch" if has else ("palm" if pat else "quiet"),
                 "quiet -> PINCH: a strip of his tape -> palm: one pat on it -> quiet"),
                ("don", "L", "quiet", "quiet"),
                ("pam", "L", "pinch", "PINCH: the page"), ("pam", "R", "quiet", "quiet")]
        declare(tuple(rows), k_)
        rig = don_rig(x, f, "hard" if not joy else ("grin" if td < 1.4 else "happy"), (1, 0.1 if td < 0.87 else 0.5))
        pocket = (x + 16, f - 108)
        u = ease(seg(td, 0.87, 1.2))
        tgt = (pocket[0] + (M[0] - pocket[0]) * u, pocket[1] - 26 * math.sin(math.pi * min(1, seg(td, 0.6, 0.87))) * (1 - u)
               + (M[1] - pocket[1]) * u)
        dj = {}
        if has:
            dj[1] = S_pinch(tgt, rig, s_)
            tgt = (tgt[0] + dj[1]["miss"][0], tgt[1] + dj[1]["miss"][1])
        elif pat:
            dj[1] = dict(T=(M[0] - 16, M[1] + 2), pose="PALM", out=1, reach=True)
        shadow(k_, x, f + 2, 40)
        kit.MOUTH[0] = 0.8 if talking("6.4", t) else None
        try:
            o = rig_hands(k_, rig, s_, dj)
        finally:
            kit.MOUTH[0] = None
        h["don"] = _head(o, "don")
        shadow(k_, px, pf + 2, 32)
        plook = (-1, 0.3) if td < 1.27 else (-0.3, 1.0)                # then down at her medal
        op = rig_hands(k_, lambda kk, a4: pam_held(kk, px, pf, SC["pam"], a4, "neutral" if td < 1.27 else "doubt", plook,
                                                   mug=False), SC["pam"], {-1: page_job((px - 70, pf - 166))},
                       sex="f", skin=FEMALE)
        h["pam"] = _head(op, "pam")
        if on_her:
            medal(k_, *M)
        if has:
            medal(k_, tgt[0], tgt[1], prop=True)                       # in his fingertips, over everything
        return h
    return cast


def S_pinch(target, rig, scale):
    return pinch_at(target, rig, scale, 1, 1)


def pinch_at(target, rig, scale, arm, out, others=None, **kw):
    """a PINCH job whose fingertips land on `target`: the wrist found by probing where the tip goes (2 passes)."""
    import da_hand_gate as g_
    T = (target[0] + 10 * arm, target[1] + 12)
    for _ in range(3):
        got = {}
        jobs = dict(others or {})
        jobs[arm] = dict(T=T, pose="PINCH", out=out, reach=True, contact="tip",
                         obj=lambda kk, P, w: got.__setitem__("P", P))
        with g_.paused():
            kk = kit.Ctx(cairo.Context(cairo.ImageSurface(cairo.FORMAT_RGB24, 8, 8)), 0)
            rig_hands(kk, rig, scale, jobs, **kw)
        miss = (got["P"][0] - target[0], got["P"][1] - target[1])
        T = (T[0] - miss[0], T[1] - miss[1])
    got = {}
    jobs = dict(others or {})
    jobs[arm] = dict(T=T, pose="PINCH", out=out, reach=True, contact="tip", obj=lambda kk, P, w: got.__setitem__("P", P))
    with g_.paused():
        kk = kit.Ctx(cairo.Context(cairo.ImageSurface(cairo.FORMAT_RGB24, 8, 8)), 0)
        rig_hands(kk, rig, scale, jobs, **kw)
    j = dict(T=T, pose="PINCH", out=out, reach=True)
    j["miss"] = (got["P"][0] - target[0], got["P"][1] - target[1])   # where the arm could not take it: the prop follows
    return j


PS = 0.55                                                          # the page's size in the two-shot (44 x 66)
HOLE_DX, HOLE_DY, HOLE_R = 9.5, -19, 7.0                          # the eye holes, from the page's middle (her eyes' spacing)


def page_holes(k, cx, cy, n=0, ang=0.0, s=PS):
    """the printed page with n eye holes poked through it (what is behind shows through them); registers as a prop."""
    import da_hand_gate as g_
    c = k.c
    holes = [(-HOLE_DX, HOLE_DY), (HOLE_DX, HOLE_DY)][:n]
    ca, sa = math.cos(ang), math.sin(ang)
    pts = [(cx + hx * ca - hy * sa, cy + hx * sa + hy * ca) for hx, hy in holes]
    if pts:                                                            # on its own layer, the holes cut out of it
        c.push_group()
        L.dpr.minutes(k, cx, cy, s, ang)
        c.set_operator(cairo.OPERATOR_CLEAR)
        for px, py in pts:
            c.new_path(); c.arc(px, py, HOLE_R, 0, 2 * math.pi); c.fill()
        c.set_operator(cairo.OPERATOR_OVER)
        c.pop_group_to_source(); c.paint()
    else:
        L.dpr.minutes(k, cx, cy, s, ang)
    for i, (px, py) in enumerate(pts):                                 # the torn edge of each hole
        c.set_source_rgb(*kit.INK); c.set_line_width(1.8); c.new_path()
        c.arc(px, py, HOLE_R, 0, 2 * math.pi); c.stroke()             # (round: the ragged 8-gon read as "square")
    g_.prop(k, "page", cx - 40 * s - 4, cy - 60 * s - 4, 80 * s + 8, 120 * s + 8)
    return pts


def s68_cast(t):
    """v2 (Tomas 28 Nov: no gag built on sound; option 1): Don takes her page, pokes two eye holes through it with his
    finger and hands it back, a spy's mask; she holds it up to her face. The whisper is gone; "Keep infiltrating." may
    play over it, the picture doesn't need it.
      0.00-0.33  she holds the page out; he beams
      0.33-0.60  he takes it by its top corner (her hand lets go on that drawing) and brings it to his chest
      0.67-1.20  two jabs of his other hand: a hole each
      1.27-1.60  he holds it out to her, proud
      1.60-2.00  she takes it (his hand lets go on that drawing) and lifts it to her face
      2.00-2.72  held: her eyes in the holes; he points both palms at his work"""
    td = drawn(t)

    def cast(k_):
        import da_hand_gate as g_
        h = {}
        c = k_.c
        x, f = MARKS["don_counter"][0] + 24, MARKS["don_counter"][1]; L.DON_FEET[0] = (x, f); s_ = SC["don"]
        px, pf = 614, F + 62
        with g_.paused():                                              # where her head is (the mask goes there)
            kk = kit.Ctx(cairo.Context(cairo.ImageSurface(cairo.FORMAT_RGB24, 8, 8)), 0)
            phx, phy, pr_ = _head(rig_hands(kk, lambda k2, a4: pam_held(k2, px, pf, SC["pam"], a4, "neutral", (-1, 0.1),
                                                                       mug=False), SC["pam"], {}, sex="f", skin=FEMALE), "pam")
        H = (x + 62, f - 150)                                          # where the page changes hands, between them
        chest = (x + 14, f - 96)                                       # the page's middle at his belly, under his face
        face_c = (phx, phy - HOLE_DY + 1)                              # the page's middle with its holes on her eyes
        n = 0 if td < 0.8 else (1 if td < 1.07 else 2)
        his = 0.33 <= td < 1.6
        if td < 0.33:
            pc = H
        elif td < 1.27:
            pc = (H[0] + (chest[0] - H[0]) * ease(seg(td, 0.33, 0.6)), H[1] + (chest[1] - H[1]) * ease(seg(td, 0.33, 0.6)))
        elif td < 1.6:
            u = ease(seg(td, 1.27, 1.53)); pc = (chest[0] + (H[0] - chest[0]) * u, chest[1] + (H[1] - chest[1]) * u)
        else:
            u = ease(seg(td, 1.6, 2.0)); pc = (H[0] + (face_c[0] - H[0]) * u, H[1] + (face_c[1] - H[1]) * u)
        jab = max(math.sin(math.pi * seg(td, 0.67, 0.87)), math.sin(math.pi * seg(td, 0.93, 1.13)))   # in and out, twice
        jab = jab if 0.67 <= td < 1.13 else 0.0
        hole_i = 0 if td < 0.9 else 1
        tgt = (pc[0] + (-HOLE_DX, HOLE_DX)[hole_i], pc[1] + HOLE_DY)
        rows = [("don", "R", "pinch" if his else "quiet", "PINCH: the page by its top corner -> quiet, proud"),
                ("don", "L", "pinch" if 0.67 <= td < 1.13 else "quiet", "PINCH: his fingertip through the paper, twice"),
                ("pam", "L", "pinch" if not his else "quiet", "PINCH: the page -> quiet -> PINCH: the mask at her face"),
                ("pam", "R", "quiet", "quiet")]
        declare(tuple(rows), k_)
        # Don
        shadow(k_, x, f + 2, 40)
        dj = {}
        if 0.67 <= td < 1.13:                                          # (before any probe: the probes must solve as the drawing)
            __import__("da_hand_gate").arms_ok("6.8: poking holes in the page he holds at his chest: the poking arm folds")
        if his:
            corner = (pc[0] + 40 * PS - 4, pc[1] - 60 * PS + 2)        # its top right corner, in his fingertips
            dj[1] = pinch_at(corner, don_rig(x, f, "grin", (1, 0.3)), s_, 1, 1)
            pc = (pc[0] + dj[1]["miss"][0], pc[1] + dj[1]["miss"][1])
            tgt = (pc[0] + (-HOLE_DX, HOLE_DX)[hole_i], pc[1] + HOLE_DY)
        if 0.67 <= td < 1.13:
            dj[-1] = pinch_at((tgt[0] - 14 + 14 * jab, tgt[1] + 8 - 8 * jab), don_rig(x, f, "grin", (1, 0.3)), s_, -1, -1)
        dface = "grin" if td < 1.2 else "happy"                        # (cold test: a frown while poking read as anger,
                                                                       # the mask as mockery) eager all through
        dlook = (1, 0.3) if td < 0.6 or td >= 1.27 else (0.3, 1.0)
        kit.MOUTH[0] = 0.5 if ("6.8" in TAKES and talking("6.8", t)) else None
        try:
            o = rig_hands(k_, don_rig(x, f, dface, dlook), s_, dj)
        finally:
            kit.MOUTH[0] = None
        h["don"] = _head(o, "don")
        # Pam (before the page when it is at her face: her eyes show through it)
        shadow(k_, px, pf + 2, 32)
        pj = {}
        if not his:
            hold = (pc[0] - 18, pc[1] + 28) if td >= 1.6 else (pc[0] + 40 * PS - 3, pc[1] - 60 * PS + 6)
            pj[-1] = pinch_at(hold, lambda k2, a4: pam_held(k2, px, pf, SC["pam"], a4, "neutral", (-1, 0.1), mug=False),
                              SC["pam"], -1, -1, sex="f", skin=FEMALE)   # (her screen-left hand, on the page's near edge)
            pc = (pc[0] + pj[-1]["miss"][0], pc[1] + pj[-1]["miss"][1])
        plook = (-1, 0.1) if td < 0.6 else ((-1, 0.6) if td < 1.6 else (-1, 0.0))
        pface = "neutral" if td < 0.67 else "doubt"
        op = rig_hands(k_, lambda kk2, a4: pam_held(kk2, px, pf, SC["pam"], a4, pface, plook, mug=False), SC["pam"], pj,
                       sex="f", skin=FEMALE)
        h["pam"] = _head(op, "pam")
        medal(k_, *medal_at(px, pf), ang=0.0)                           # straight since 6.7
        page_holes(k_, pc[0], pc[1], n, ang=0.04 if his else 0.0)
        if jab > 0.6:                                                  # the poke's little burst
            c.set_source_rgb(*kit.INK); c.set_line_width(1.6); c.set_line_cap(1)
            for a_ in (-2.4, -1.57, -0.7):
                c.new_path(); c.move_to(tgt[0] + 9 * math.cos(a_), tgt[1] + 9 * math.sin(a_))
                c.line_to(tgt[0] + 15 * math.cos(a_), tgt[1] + 15 * math.sin(a_)); c.stroke()
            c.set_line_cap(0)
        h["page"] = (pc[0], pc[1], 30)
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
    medal(k_, medal_at(px, pf)[0], medal_at(px, pf)[1] + 4 * drop)
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
    """v2 (story chain v1, fix D: Pam chooses): her eyes come back down to him, her mouth shuts; then, saying nothing,
    she straightens the crooked medal on her cardigan with two fingertips. She is in."""
    td = drawn(t)

    def cast(k_):
        u = ease(seg(td, 0.0, 0.2))                                    # her eyes come back down
        look = (0.7 - 0.7 * u, -0.7 + 0.7 * u)
        if td < 0.13:
            return pam_close(k_, "A", "doubt", look)
        if td < 0.27:
            return pam_close(k_, "E", "neutral", look)                 # the mouth closing
        px, pf = 626, F + 60
        import da_hand_gate as g_
        g_.arms_ok("6.7: her fingertips on the medal on her own chest: the elbow folds as it must")
        fix = ease(seg(td, 0.47, 0.73))
        ang = -0.34 * (1 - fix)
        on = 0.33 <= td < 0.87
        M = medal_at(px, pf)
        declare((("pam", "L", "quiet", "quiet"),
                 ("pam", "R", "pinch" if on else "quiet", "quiet -> PINCH: the medal's corner, turned straight -> quiet")),
                k_, [("tape strip", (M[0] - 20, M[1] - 16, 44, 36))] if on else [])
        shadow(k_, px, pf + 2, 32)
        rig = lambda kk, a4: pam_held(kk, px, pf, SC["pam"], a4, "neutral", (-0.2, 1.0) if on else (-0.6, 0.0), mug=False,
                                      mouth="M")
        jobs = {}
        if on:
            corner = (M[0] + 12 * math.cos(ang), M[1] + 5 + 12 * math.sin(ang))   # its near corner: her other hand (the
            jobs[1] = pinch_at(corner, rig, SC["pam"], 1, 1, sex="f", skin=FEMALE)   # same-side arm folds into a knot)
        o = rig_hands(k_, rig, SC["pam"], jobs, sex="f", skin=FEMALE)
        medal(k_, M[0], M[1], ang=ang)
        return {"pam": _head(o, "pam")}
    return cast


def s68b_cast(t):
    """v2: close on her: the mask at her face, her eyes in its holes going to him; then she lowers it: flat."""
    td = drawn(t)

    def cast(k_):
        import da_hand_gate as g_
        px, pf = 614, F + 62
        with g_.paused():
            kk = kit.Ctx(cairo.Context(cairo.ImageSurface(cairo.FORMAT_RGB24, 8, 8)), 0)
            phx, phy, pr_ = _head(rig_hands(kk, lambda k2, a4: pam_held(k2, px, pf, SC["pam"], a4, "neutral", (-1, 0.1),
                                                                       mug=False), SC["pam"], {}, sex="f", skin=FEMALE), "pam")
        low = ease(seg(td, 0.33, 0.53))                                # she lowers it to her chin
        pc = (phx, phy - HOLE_DY + 1 + 34 * low)
        declare((("pam", "L", "pinch", "PINCH: the mask"), ("pam", "R", "quiet", "quiet")), k_)
        shadow(k_, px, pf + 2, 32)
        look = (-1, 0.0)
        hold = (pc[0] - 18, pc[1] + 28)                                # its lower near corner (the hold her arm reaches)
        rigp = lambda kk2, a4: pam_held(kk2, px, pf, SC["pam"], a4, "neutral", look, mug=False)
        pj = pinch_at(hold, rigp, SC["pam"], -1, -1, sex="f", skin=FEMALE)
        pc = (pc[0] + pj["miss"][0], pc[1] + pj["miss"][1])
        o = rig_hands(k_, rigp, SC["pam"], {-1: pj}, sex="f", skin=FEMALE)
        medal(k_, *medal_at(px, pf), ang=0.0)                           # straight since 6.7
        page_holes(k_, pc[0], pc[1], 2)
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
    ds.ROLL_V2[0] = True                                               # the plan readable in his fists (this shot only)
    try:
        return frame(cast, cam, office=office, tag=True, clips=6, near=light)
    finally:
        ds.ROLL_V2[0] = False


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
        return frame(s64_cast(t), (CAMS.get("6.2") or CAMS.setdefault("6.2", camera_of("6.2")))[0], tag=True, clips=6)      # (the medal: a two-shot)
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
    (STARTS["6.8"] + 0.75, "tik", 0.7), (STARTS["6.8"] + 1.02, "tik", 0.7),   # the two pokes
    (STARTS["6.8"] + 1.6, "paper", 0.5),
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


GATED = tuple(s for s, _ in SHOTS)


def build():
    import subprocess
    from PIL import Image, ImageDraw
    import da_hand_gate as g
    import hands_v4 as hv
    import da_arms
    da_arms.setup(); hv.enable(); g.install(); cu.install(); A._SETUP.append(1)
    g.ARM_RULES[0] = True; L.ELBOW_RULE[0] = True                     # (Tomas's deep audit 28 Nov: every arm, every drawing)
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
