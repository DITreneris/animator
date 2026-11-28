"""Approved. (episode 16): the layouts, v1 (stage 4.3; Tomas 28 Nov /grill-me: real frames, one act at a time).

Every shot's key frame at 540x960 (shown at 270) in the locked night (rv_night_cast v6: the grade, LOCK_CAST, glows
only at their sources), drawn from the scene file's records (rv_scenes.STAGE / TEXT / states(): nothing about a shot is
typed here twice) with the drawings that exist: the night room (rv_night_cast._room), the cast's rigs (episode 15's
scales, da_layouts.SC), the props (rv_props), the pose sandbox (rv_poses). K1 is the locked file (rv_keys.k1). One map,
shot -> draw function, printed and asserted (lesson 109). Key poses only (stand-ins marked): the motion is stage 6.

  python3 rv_layouts.py [act ...]  ->  ../the-review/rv_layout_act<N>_v1.png (+ _feed: the sheet at half size)

The checks on every frame (exit 1 on a failure not in KNOWN): signs whole or out (uz_check.check_signs), the story
faces out of the apps' zones (uz_check.check_scale, measured where the rigs drew them), every face of the shot's cast
inside the frame under the top bar, and Don on the side of the tape the scene file gives him (rv_scenes.STAGE "don").
Runs on a checkout with episode 15's modules, as rv_night_cast and rv_keys.
"""
import math
import os
import sys
import textwrap

import cairo

import kit
from kit import Ctx, INK
import bp_frame as bp
import fs_storyboard_v17 as sbv
import fs_set4 as s4
import ps_set as pss
import da_set as ds
import da_layouts as L
import da_props as dpr
import dh_props as dprops
import rv_night as rn
import rv_night_cast as nc
import rv_props as pr
import rv_poses as rpo
import rv_scenes as sc
import don_ps as dp
import pm_ps as pm
import robot_ps as rp
import dh_cast as dc
import client_ps as cp
import uz_check as uz

HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.join(HERE, "..", "the-review")
W, H = 540, 960
F = pss.F
SC, R = L.SC, L.R
TX, TF, TS = pss.THRONE
LINE_X = pss.LINE_X                                            # the tape, world x 560
MIN_SIGN = 5
CHAIR_S = 0.9                                                  # the folding chair at Father's scale (0.62 drew a child's chair)
ACTS = {1: ["1.1", "1.2", "1.3", "1.4", "1.5", "1.6", "1.7"], 2: ["2.1", "2.2", "2.3", "2.4", "2.5", "2.6", "2.7"],
        3: ["3.1", "3.2", "3.3", "3.4", "3.5", "3.6", "3.7", "3.8", "3.9", "3.10"]}
CLIENT_NO_RAG = [True]                                         # Tomas 28 Nov ("1"): in episode 16 the Client has no rag
                                                               # (its red read as blood at night, 1/2; no action uses it).
                                                               # client_ps is not edited: its CLEAN overlay draws only
                                                               # the rag, so it is skipped while this episode draws.
_overlay0 = cp.overlay


def _overlay_e16(k, x, feet, s, turn=0.0, seed=4400):
    if CLIENT_NO_RAG[0] and cp.CLEAN[0]:
        return
    return _overlay0(k, x, feet, s, turn, seed)


cp.overlay = _overlay_e16
import client_of as _cof                                       # and the rag in his back pocket: client_of's own opt-out
_cof.POCKET_RAG[0] = not CLIENT_NO_RAG[0]                      # (The Offer v48); cold test 1.6 "a bloody hand" 2/2
pr.SOFIA_V5[0] = True                                          # 28 Nov: episode 15's characters refreshed (Sofía v5; the
                                                               # Client's CLEAN comes with da_set)
KNOWN = {}                                                     # (shot, check) -> reason
POSE = {}                                                      # shot -> "stand-in" note for the sheet


def head(o, who, key="head"):
    x, y = o[key][:2]
    return (x, y, R[who] * SC[who])


def rot(px, py, ox, oy, a):
    """a point drawn inside rotate(a) about (ox, oy), in the outer coordinates."""
    dx, dy = px - ox, py - oy
    return (ox + dx * math.cos(a) - dy * math.sin(a), oy + dx * math.sin(a) + dy * math.cos(a))


def drawn(fn):
    """props are drawn in the colour pass only (the mask pass keeps the people: the cast light)."""
    if nc._PASS[0] != "mask":
        fn()


def glows_room(robot_screen=None, throne=True):
    g = [(nc.MON[0], nc.MON[1], 46, 34, bp.NIGHT_MONITOR, 0.45), (nc.MACH[0], nc.MACH[1], 60, 44, bp.NIGHT_MONITOR, 0.30)]
    g += nc._machine_glow()
    li = [(nc.DOOR[0], nc.DOOR[1], 260, 0.9), (nc.MON[0], nc.MON[1], 200, 0.9), (nc.MACH[0], nc.MACH[1], 180, 0.7)]
    if robot_screen:
        g.append((robot_screen[0], robot_screen[1], 40, 32, bp.NIGHT_MONITOR, 0.30))
        li.append((robot_screen[0], robot_screen[1], 150, 0.6))
    if throne:
        li.append((TX, F - 200, 160, 0.4))
    return g, li


# ---- Act I ------------------------------------------------------------------------------------------------------------
def s11():
    """1.1 frame 0: the locked K1 v6 (rv_keys.k1, the same code at both ends)."""
    return dict(file=os.path.join(EP, "rv_K1_v6.png"))


def don_on_back(k, x, f, cup=True):
    """1.2: Don flat on his back, head to screen left, eyes shut, his screen-right arm straight up with the empty cup
    (rv_poses: a new pose; stand-in until its silhouette test). The rig rotated a quarter turn about his feet."""
    c = k.c
    a = -math.pi / 2
    c.save(); c.translate(x, f); c.rotate(a); c.translate(-x, -f)
    o = dp.don(k, x, f, SC["don"], (-8, 0, 92, 2), "squint", (0, 0), hands=("relax", "grab"))
    c.restore()
    hx, hy = rot(o["head"][0], o["head"][1], x, f, a)
    if cup:
        wx, wy = rot(x + 98 * SC["don"], f - 230 * SC["don"], x, f, a)        # the raised hand, roughly (stand-in)
        drawn(lambda: dpr.cup_and_saucer(k, wx + 2, wy - 18, 0.8))
    return (hx, hy, R["don"] * SC["don"])


def s12():
    """1.2 S4 C, v2: rv_poses.don_on_back "B" (the silhouette test: the knee up reads alive and asleep 2/2), his arm
    up at an angle with the cup on his palm, larger (v1: "a pole with a dish", 2/2); the folded paper beside him."""
    def draw(k):
        nc._room(k, pam_behind=False)
        drawn(lambda: pss.throne(k))
        drawn(lambda: pr.report(k, TX - 150, F + 112, 0.55))
        o = rpo.don_on_back(k, TX - 40, F + 96, SC["don"], "B", arm=(-8, 0, 124, -48), cup_k=1.5)
        return {"don": (o["head"][0], o["head"][1], R["don"] * SC["don"])}
    g, li = glows_room()
    POSE["1.2"] = "don_on_back B (silhouette 2/2)"
    return dict(cam=(TX - 10, F + 30, 2.0), draw=draw, glows=g, lights=li)


def s13():
    """1.3 S6 M: Pam behind the counter in her monitor's glow, MY GARAGES open; her mug by the machine, needle green."""
    def draw(k):
        h = nc._room(k, pam_behind=True)
        drawn(lambda: dpr.plan_open_v2(k, nc.MON[0] + 22, F - 96, 0.62))
        drawn(lambda: dial(k, "1.3"))
        h2 = {}
        if "pam" in h:
            h2["pam"] = (h["pam"][0], h["pam"][1], R["pam"] * SC["pam"])
        return h2
    g, li = glows_room()
    POSE["1.3"] = "Pam pushed in (v2: the machine at the edge)"
    return dict(cam=(nc.MON[0] + 6, F - 190, 2.7), draw=draw, glows=g, lights=li)


def s14():
    """1.4 S1 W, v2 (review: "the chair's unfolding is the move"): tighter on the tape; Father, in from A, holds the
    folded chair out by its top, about to snap it open on the tape; Don on the floor in front, the cup up; behind the
    throne the robot hooks the tag back."""
    def draw(k):
        nc._room(k)
        o_r = rp.robot(k, TX - 70, F - 6, SC["robot"], look=(1, -0.6))
        drawn(lambda: pss.throne(k))
        nc._shadow(k, LINE_X + 50, F + 40, 30)
        o_f = dc.father(k, LINE_X + 50, F + 38, SC["father"], pose=(-30, -40, 20, 0), look=(-1, 0.3))
        hx, hy = o_f["hands"][0]
        drawn(lambda: pr.folding_chair(k, hx - 4, hy + 150 * CHAIR_S * 0.9, CHAIR_S * 0.9, "folded"))
        o_d = rpo.don_on_back(k, TX - 30, F + 110, SC["don"], "B", arm=(-8, 0, 124, -48), cup_k=1.5)
        return {"father": head(o_f, "father"), "robot": head(o_r, "robot", "screen"),
                "don": (o_d["head"][0], o_d["head"][1], R["don"] * SC["don"])}
    g, li = glows_room()
    POSE["1.4"] = "Father's hold on the folded chair: stand-in"
    return dict(cam=(500, F - 90, 1.45), draw=draw, glows=g, lights=li)


def s15():
    """1.5 v3 (Tomas 28 Nov, G6 back to premises: the reaching arm read "a huge limb" 2/2): an INSERT at the chair's
    short leg. The Client's hand comes in from the frame's right edge, a rolled white sleeve and a short wrist stub
    (rules: "at the frame's edge, a hand with a short wrist stub passes"), Holding a thing (grab), and pushes the washer
    under the leg. Two keys: a: the gap under the short leg, the hand coming in with the washer; b: the washer under
    it, the leg down, the hand leaving. His face is seen next in 1.6, back on his feet."""
    import hand_lib_v4 as hl
    import client_ob as cob
    leg = (LINE_X + 38 * CHAIR_S, F + 30)
    W_HAND = 17 * 1.3

    def washer_flat(k, x, y):                                   # lying on the floor: seen low, an ellipse
        c = k.c
        c.save(); c.translate(x, y); c.scale(1.0, 0.42); pr.washer(k, 0, 0, 1.0); c.restore()

    def key(state, wx, wy, held):
        def draw(k):
            nc._room(k, pam_behind=False)
            drawn(lambda: pss.throne(k))
            drawn(lambda: pr.folding_chair(k, LINE_X, F + 30, CHAIR_S, state))
            c = k.c
            def hand():
                if not held:
                    washer_flat(k, wx, wy)
                # the hand: PINCH (thumb and index meet) on the washer's edge, or resting back from it (RELAXED)
                pose = "PINCH" if held else "RELAXED"
                tip = hl.POSES["PINCH"]["contacts"]["tip"]           # along the forearm: the hand points to -x
                hx = wx + (tip[0] * W_HAND if held else 30)
                hy = wy + (0 if held else -2)
                ex = hx + 140
                L.dp._cap(c, [(ex, hy - 14), (hx + 36, hy - 4)], 26, (0.96, 0.94, 0.88), 2.0)   # the rolled sleeve
                L.dp._cap(c, [(hx + 40, hy - 4), (hx + 6, hy)], 16, cob.SKIN, 2.0)              # the wrist stub
                if held:
                    c.save(); c.translate(wx, wy); c.rotate(-0.25); pr.washer(k, 0, 0, 0.9); c.restore()
                hl.draw_lr(k, pose, hx, hy, (-1, 0.08), W_HAND, cob.SKIN, 1)
            drawn(hand)
            return {}
        return dict(cam=(leg[0] + 18, leg[1] - 28, 6.0), draw=draw, glows=[], lights=[(leg[0], leg[1] - 60, 160, 0.6)],
                    search=False)
    gap = 9 * CHAIR_S                                           # rv_props.folding_chair's short leg, off the floor
    return [key("wobble", leg[0] + 7, leg[1] - gap * 0.4, True),  # a: the gap under the leg, the washer going in
            key("open", leg[0] + 2, leg[1] + 1, False)]             # b: under the leg, the leg down on it, the hand back


def father_seated(k, x, seat_y, floor_y, lean=0.0, look=(1, 0)):
    """Father on the folding chair (stand-in until the sandbox has his seat; rv_poses' lesson: a front-on seat reads as
    standing unless the seat shows): the chair's back panel behind his ribs, his rig clipped above the belt with the
    belt on the seat, the seat's front edge drawn ACROSS his lap, short thighs toward us, shins to the floor."""
    c = k.c
    s = SC["father"]
    waist = -98 * 1.12
    vfeet = seat_y - waist * s
    c.save(); c.translate(x, seat_y); c.rotate(lean); c.translate(-x, -seat_y)
    c.save(); c.rectangle(x - 400, seat_y - 2000, 800, 2000 + 4); c.clip()
    o = dc.father(k, x, vfeet, s, look=look)
    c.restore(); c.restore()
    TROU, SHOE = (0.12, 0.11, 0.12), (0.06, 0.05, 0.06)
    for side in (-1, 1):
        L.dp._cap(c, [(x + side * 14, floor_y - 30), (x + side * 18, floor_y - 6)], 16, TROU, 2.0)
        kit.cut(k, [(x + side * 18 - 12, floor_y - 8), (x + side * 18 + 14, floor_y - 8), (x + side * 18 + 15, floor_y),
                    (x + side * 18 - 13, floor_y)], SHOE, shadow=False, lw=2)
        kit.cut(k, [(x + side * 2, seat_y - 4), (x + side * 30, seat_y - 4), (x + side * 32, seat_y + 22),
                    (x + side * 2, seat_y + 22)], TROU, shadow=False, lw=2)        # the thighs, toward us
    kit.cut(k, [(x - 40 * CHAIR_S, seat_y + 2), (x + 40 * CHAIR_S, seat_y + 2), (x + 36 * CHAIR_S, seat_y + 12),
                (x - 36 * CHAIR_S, seat_y + 12)], pr.SEAT, lw=2.2)                # the seat's edge across his lap
    hx, hy = rot(o["head"][0], o["head"][1], x, seat_y, lean)
    return (hx, hy, R["father"] * SC["father"])


def s16():
    """1.6 S3 M: Father sits and leans hard to one side; the chair doesn't budge. His eyes go to the throne, then to
    the Client (behind the counter, on his feet)."""
    def draw(k):
        nc._room(k, pam_behind=False)
        nc._shadow(k, 700, F + 6, 34)
        o_c = cp.client(k, 700, F + 4, SC["client"], look=(-1, 0))
        drawn(lambda: pss.throne(k))
        drawn(lambda: pr.folding_chair(k, LINE_X, F + 30, CHAIR_S, "open"))
        o = rpo.father_folding(k, LINE_X, F + 30, SC["father"], "B", lean_side=-0.16, chair_s=CHAIR_S,
                               look=(-1, -0.3), head_level=True)
        h = {"father": (o["head"][0], o["head"][1], R["father"] * SC["father"])}
        h["client"] = head(o_c, "client")
        return h
    g, li = glows_room()
    POSE["1.6"] = "father_folding B (silhouette 2/2), head level"
    return dict(cam=(LINE_X + 40, F - 120, 1.45), draw=draw, glows=g, lights=li)


def s17():
    """1.7 S3 I, v2: two keys (review: "show the flip TOMORROW -> TODAY in one close"; cold 2/2: "a sign on a door"):
    the throne's back seen high, the gold crown over its top edge so it is the throne; the ringed hand turns the tag:
    a: TOMORROW, the hand on it; b: TODAY, the tag still swinging."""
    def key(word, swing):
        def draw(k):
            hx, hy = TX, F - 300
            def back_and_tag():
                c = k.c
                kit.cut(k, [(hx - 150, hy - 70), (hx + 150, hy - 70), (hx + 150, hy + 220), (hx - 150, hy + 220)],
                        (0.20, 0.16, 0.15), shadow=False, lw=0)
                kit.cut(k, [(hx - 150, hy - 84), (hx + 150, hy - 84), (hx + 150, hy - 66), (hx - 150, hy - 66)],
                        pss.dp.GOLD, shadow=False, lw=2)                       # the back's gold top edge
                c.save(); c.translate(hx, hy - 84)                            # the crown over it (its band and points)
                kit.cut(k, [(-70, 0), (70, 0), (70, -24), (-70, -24)], pss.dp.GOLD, shadow=False, lw=2)
                kit.cut(k, [(-70, -24), (-58, -74), (-30, -34), (0, -86), (30, -34), (58, -74), (70, -24)],
                        pss.dp.GOLD, shadow=False, lw=2)
                for px_, py_ in ((-58, -74), (0, -86), (58, -74)):
                    kit.ellipse(k, px_, py_ - 6, 7, 7, (0.70, 0.10, 0.16), 4740, shadow=False, lw=1.6)
                c.restore()
                c.set_source_rgb(0.28, 0.23, 0.21); c.set_line_width(2); c.move_to(hx, hy - 66); c.line_to(hx, hy + 220)
                c.stroke()
                c.save(); c.translate(hx, hy - 66); c.rotate(swing); c.translate(-hx, -(hy - 66))
                pr.review_tag(k, hx, hy - 66, 1.25, word)
                c.restore()
                if word == "TOMORROW":                                         # the ringed hand on its corner
                    ex, ey = hx + 52, hy + 4
                    kit.cut(k, [(ex + 160, ey - 40), (ex + 160, ey - 4), (ex + 14, ey + 8), (ex + 8, ey - 12)],
                            (0.45, 0.10, 0.16), lw=2)
                    kit.ellipse(k, ex + 4, ey - 2, 10, 8, (0.94, 0.80, 0.68), 4731, shadow=False, lw=2)
                    kit.ellipse(k, ex + 8, ey + 3, 3, 3, (0.93, 0.74, 0.22), 4732, shadow=False, lw=1)
            drawn(back_and_tag)
            return {}
        return dict(cam=(TX, F - 320, 3.0), draw=draw, glows=[], lights=[(TX, F - 300, 200, 0.6)],
                    rim=lambda k_: None, search=False)
    return [key("TOMORROW", 0.05), key("TODAY", -0.10)]


# ---- Act II: the rejections -------------------------------------------------------------------------------------------
SEAT_Y = 742                                                   # the throne's seat (rv_keys.SEAT)
ROBOT_HOME = (232, F + 4)                                      # its station in A (fs_set4.HOME)


class no_badge(object):
    """the robot without its HR badge (Sofía has it from 2.5): rv_keys._no_hr_badge."""
    def __enter__(self):
        import rv_keys as rk
        self.cm = rk._no_hr_badge(); self.cm.__enter__(); return self

    def __exit__(self, *a):
        self.cm.__exit__(*a)


def sofia_in_throne(k, face="smile", look=(0, -0.3)):
    """REUSED: dh_scenes._sofia_seated (Daddy's Home, approved): the rig cut at the seat, the skirt over her knees, her
    shins and heels; in her CEO suit (rv_props.sofia_ceo over episode 15's v5)."""
    c = k.c
    x, seat_y, floor = TX, SEAT_Y, TF
    s_ = SC["sofia"]
    feet = seat_y + 122 * s_
    c.save(); c.rectangle(x - 150, seat_y - 400, 300, 400 + 2); c.clip()
    o = pr.sofia_ceo(k, x, feet, s_, "hold", face, look=look)
    c.restore()
    kit.cut(k, [(x - 30, seat_y - 2), (x + 30, seat_y - 2), (x + 34, seat_y + 22), (x - 34, seat_y + 22)],
            pr.CEO_SUIT[0] if isinstance(pr.CEO_SUIT[0], tuple) else (0.10, 0.10, 0.12), shadow=False, lw=2)
    for sx in (-1, 1):
        kit.cut(k, [(x + sx * 14 - 7, seat_y + 22), (x + sx * 14 + 7, seat_y + 22), (x + sx * 13 + 5, floor - 4),
                    (x + sx * 13 - 5, floor - 4)], (0.16, 0.15, 0.18), shadow=False, lw=1.8)
        kit.cut(k, [(x + sx * 13 - 9, floor - 6), (x + sx * 13 + 11, floor - 6), (x + sx * 13 + 13, floor + 2),
                    (x + sx * 13 - 9, floor + 2)], (0.08, 0.07, 0.08), shadow=False, lw=1.6)
    return head(o, "sofia")


def father_on_chair(k, look=(-1, 0)):
    o = rpo.father_folding(k, LINE_X, F + 30, SC["father"], "B", chair_s=CHAIR_S, look=look)
    return (o["head"][0], o["head"][1], R["father"] * SC["father"])


def s21():
    """2.1 S1 W: Don scrambles up; Sofía is quicker and sits in the throne, chin up; Father's eyes go past her."""
    def draw(k):
        nc._room(k)
        drawn(lambda: pss.throne(k))
        h = {"sofia": sofia_in_throne(k, "smile", (0.3, -0.5))}
        h["father"] = father_on_chair(k, look=(-1, -0.2))
        nc._shadow(k, 340, F + 70, 34)
        h["don"] = head(dp.don(k, 340, F + 68, SC["don"], "balance", "shock", look=(1, -0.2)), "don")
        return h
    g, li = glows_room()
    POSE["2.1"] = "Sofía seated: REUSED dh_scenes (Don scrambling: stand-in)"
    return dict(cam=(470, F - 110, 1.3), draw=draw, glows=g, lights=li)


def s22():
    """2.2 S3 MC: Sofía gets up, smoothing her skirt; her eyes already on the robot (screen left)."""
    def draw(k):
        nc._room(k, pam_behind=False)
        drawn(lambda: pss.throne(k))
        nc._shadow(k, TX + 60, F + 40, 28)
        o = pr.sofia_ceo(k, TX + 60, F + 38, SC["sofia"], "hold", "smile", look=(-1, 0.1))
        return {"sofia": head(o, "sofia")}
    g, li = glows_room()
    POSE["2.2"] = "smoothing the skirt: stand-in (her hold pose)"
    return dict(cam=(TX + 40, F - 150, 2.0), draw=draw, glows=g, lights=li)


def s23():
    """2.3 S2 M: the robot rolls up to Father holding out the report; Father's palm up before it can present it."""
    import hands_ps as hp
    def draw(k):
        nc._room(k, pam_behind=False)
        drawn(lambda: pss.throne(k))
        rx = LINE_X - 130                                       # v2: a clear gap between the report and his palm
        nc._shadow(k, rx, F + 50, 26)
        o_r = rp.robot(k, rx, F + 48, SC["robot"], arms=((-8, 0), (80, 10)), look=(1, -0.3))
        gx, gy = o_r["hands"][1]
        drawn(lambda: pr.report(k, gx + 14, gy - 4, 0.6))
        o_f = rpo.father_folding(k, LINE_X + 10, F + 30, SC["father"], "B", chair_s=CHAIR_S, look=(-1, 0),
                                 arms=(-75, -55, 30, -26), hands=("palm", "quiet"))   # v2: the palm up, toward it
        return {"robot": head(o_r, "robot", "screen"), "father": (o_f["head"][0], o_f["head"][1],
                                                                  R["father"] * SC["father"])}
    g, li = glows_room(robot_screen=(LINE_X - 90, F - 60))
    POSE["2.3"] = "Father's raised palm: stand-in (arm control to the sandbox)"
    return dict(cam=(LINE_X - 30, F - 110, 1.9), draw=draw, glows=g, lights=li)


def robot_close(screen_kind=None, badge=True, drop=False, flat=False):
    def draw(k):
        nc._room(k, pam_behind=False)
        x, f = ROBOT_HOME[0] + 220, F + 40
        if badge:
            o = rp.robot(k, x, f, SC["robot"], look=(0, 0))
        else:
            with no_badge():
                o = rp.robot(k, x, f, SC["robot"], look=(0, 0))
        sx, sy = o["screen"][:2]
        def scr():
            if screen_kind:
                pr.screen(k, sx, sy, 50 * SC["robot"] * 1.16, screen_kind)
            elif flat:                                          # its two eyes, the smile gone: a dark screen, two dots
                c = k.c; r_ = 50 * SC["robot"] * 1.0
                c.set_source_rgb(0.05, 0.08, 0.14); c.arc(sx, sy, r_, 0, 2 * math.pi); c.fill()
                c.set_source_rgb(0.55, 0.85, 1.0)
                for ex in (-8, 9):
                    c.arc(sx + ex, sy - 8, 3.2, 0, 2 * math.pi); c.fill()
                c.set_line_width(2); c.move_to(sx - 7, sy + 8); c.line_to(sx + 7, sy + 8); c.set_source_rgb(0.55, 0.85, 1.0); c.stroke()
            if drop:                                            # one oil drop rolling down its face (v2: from its eye,
                c = k.c                                          # a wet trail above it: a tear, not a crack)
                c.set_source_rgba(0.12, 0.11, 0.10, 0.55); c.set_line_width(3); c.set_line_cap(1)
                c.move_to(sx + 9, sy - 8); c.line_to(sx + 9, sy + 2); c.stroke(); c.set_line_cap(0)
                c = k.c
                c.save(); c.translate(sx + 9, sy + 4); c.scale(1.8, 1.8)               # v2: big enough at 270
                c.move_to(0, -6); c.curve_to(5, 0, 5, 6, 0, 7); c.curve_to(-5, 6, -5, 0, 0, -6); c.close_path()
                c.set_source_rgb(0.12, 0.11, 0.10); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1); c.stroke()
                c.set_source_rgba(1, 1, 1, 0.7); c.arc(-1.5, 1, 1.4, 0, 2 * math.pi); c.fill()
                c.restore()
        drawn(scr)
        return {"robot": head(o, "robot", "screen")}
    x, f = ROBOT_HOME[0] + 220, F + 40
    return dict(cam=(x, f - 114 * SC["robot"] - 10, 5.0), draw=draw, glows=[(x, f - 55, 40, 32, bp.NIGHT_MONITOR, 0.45)],
                lights=[(x, f - 55, 150, 1.0)], search=False)


def s24():
    """2.4 S3 I: the robot's screen: POSITION VACANT (it left HR to apply)."""
    return robot_close("POSITION VACANT", badge=True)


def s25():
    """2.5 S3 MC: Sofía has unpinned the HR card from its chest and pins it on her jacket, checking it hangs straight;
    the robot, badge gone, looks to the corner she points it to."""
    import robot_tg as rt
    def draw(k):
        nc._room(k, pam_behind=False)
        rx = TX - 70
        with no_badge():
            nc._shadow(k, rx, F + 50, 26)
            o_r = rp.robot(k, rx, F + 48, SC["robot"], look=(-1, -0.2))
        nc._shadow(k, TX + 40, F + 52, 28)
        o_s = pr.sofia_ceo(k, TX + 40, F + 50, SC["sofia"], "hold", "smile", look=(-0.6, 0.6))
        hx, hy = o_s["head"][:2]
        def card():
            c = k.c
            c.save(); c.translate(hx + 16 * SC["sofia"], hy + 120 * SC["sofia"]); c.scale(0.5, 0.5)
            rt.tg_badge(k, -29, -20, 5010)
            c.restore()
        drawn(card)
        return {"sofia": head(o_s, "sofia"), "robot": head(o_r, "robot", "screen")}
    g, li = glows_room(robot_screen=(TX - 70, F - 10))
    POSE["2.5"] = "the HR card on her lapel; her pinch and the point: stand-ins"
    return dict(cam=(TX - 60, F - 130, 2.1), draw=draw, glows=g, lights=li)


def s26():
    """2.6 S3 C: two keys: a: one oil drop rolls down the robot's face (its face flat, not smiling: v2, "a smug wink");
    b: the screen goes flat: NOTED."""
    return [robot_close(None, badge=False, drop=True, flat=True), robot_close("NOTED.", badge=False)]


def s27():
    """2.7 S1 W: it rolls to its station in A, the report still in its gripper; Don watches it go, pleased."""
    def draw(k):
        nc._room(k)
        drawn(lambda: pss.throne(k))
        rx = ROBOT_HOME[0]                                       # v2: at its station, apart from Don ("Don holds a paper")
        with no_badge():
            nc._shadow(k, rx, F + 14, 26)
            o_r = rp.robot(k, rx, F + 12, SC["robot"], arms=((-8, 0), (40, 30)), look=(-1, 0.2))
        gx, gy = o_r["hands"][1]
        drawn(lambda: pr.report(k, gx + 10, gy, 0.6))
        h = {"robot": head(o_r, "robot", "screen")}
        h["father"] = father_on_chair(k, look=(-1, 0))
        nc._shadow(k, 420, F + 70, 34)
        h["don"] = head(dp.don(k, 420, F + 68, SC["don"], "stand", "pleased", look=(-1, 0)), "don")
        return h
    g, li = glows_room(robot_screen=(ROBOT_HOME[0] + 40, F - 50))
    POSE["2.7"] = "key pose"
    return dict(cam=(400, F - 110, 1.25), draw=draw, glows=g, lights=li)



# ---- Act III: the coffee ----------------------------------------------------------------------------------------------
MX, MB, MS = dprops.MACHINE                                   # the machine on the counter (770, 634, 0.72)
MUG_AT = (MX - 72, MB)                                        # Pam's mustard mug, by the machine


def dial(k, sid):
    """the needle as the scene file has it at the end of the shot (rv_scenes.states)."""
    pr.gauge(k, MX, MB, MS, sc.states()[sid]["needle"])


def mug_on_counter(k):
    import da_cups as cups
    cups.install()
    cups.mug(k, MUG_AT[0], MUG_AT[1], cups.MUG_FLOOR * 0.9, handle=-1, kind="mustard")


def counter_people(k, client=None, don=None, pam=True):
    """the counter's end (S6): the room with Pam behind at her monitor; the Client on the customer side, Don at the
    machine. client: None | ("stand", look) | "lying"; don: None | dict(x, f, pose, face, look, hands, knee)."""
    h = {}
    hp_ = nc._room(k, pam_behind=pam)
    if pam and "pam" in hp_:
        h["pam"] = (hp_["pam"][0], hp_["pam"][1], R["pam"] * SC["pam"])
    if client and client != "lying":
        nc._shadow(k, 640, F + 10, 34)
        h["client"] = head(cp.client(k, 640, F + 8, SC["client"], look=client[1]), "client")
    if don:
        nc._shadow(k, don["x"], don["f"] + 2, 34)
        h["don"] = head(dp.don(k, don["x"], don["f"], SC["don"], don.get("pose", "stand"), don.get("face", "neutral"),
                               don.get("look", (0, 0)), hands=don.get("hands")), "don")
    return h


def s31():
    """3.1 S1 W: Don steps over his own tape to the counter (Father's side), glancing down at the line; Father
    watches from his chair on the tape."""
    def draw(k):
        nc._room(k)
        drawn(lambda: pss.throne(k))
        h = {"father": father_on_chair(k, look=(1, 0.4))}
        nc._shadow(k, LINE_X + 26, F + 120, 34)
        h["don"] = head(dp.don(k, LINE_X + 26, F + 118, SC["don"], "stand", "neutral", look=(-0.3, 1.0), knee=0.7), "don")
        return h
    g, li = glows_room()
    POSE["3.1"] = "the step over the tape (don_ps knee): key pose"
    return dict(cam=(560, F - 60, 1.4), draw=draw, glows=g, lights=li)


def s32():
    """3.2 S6 MC: at the machine for the first time in his life, the filter in upside down; the Client, customer
    side, watches; Pam behind doesn't move. DON (to Father, proud): "I usually delegate." """
    def draw(k):
        h = counter_people(k, client=("stand", (1, 0.2)), don=dict(x=760, f=F + 46, face="smug", look=(-1, -0.2)))
        drawn(lambda: (dial(k, "3.2"), mug_on_counter(k)))
        return h
    g, li = glows_room()
    g += [(MX, MB - 60, 50, 40, bp.NIGHT_MONITOR, 0.30)]
    POSE["3.2"] = "the upside-down filter: stand-in (in the animatic)"
    return dict(cam=(720, F - 150, 1.9), draw=draw, glows=g, lights=li)


def panel_insert(kind=None, needle_sid=None, shudder=False):
    def draw(k):
        nc._room(k, pam_behind=False)
        def it():
            if kind:
                pr.screen(k, MX, MB - 108 * MS, 30, kind, shape="rect")
            if needle_sid:
                dial(k, needle_sid)
            if shudder:                                         # three shake lines either side
                c = k.c; c.set_source_rgb(*INK); c.set_line_width(2.4); c.set_line_cap(1)
                for sd in (-1, 1):
                    for i in range(3):
                        x0 = MX + sd * (48 + i * 8); c.move_to(x0, MB - 100 + i * 14); c.line_to(x0 + sd * 8, MB - 96 + i * 14)
                        c.stroke()
                c.set_line_cap(0)
        drawn(it)
        return {}
    cx = MX + (36 * MS if needle_sid and not kind else 0)
    return dict(cam=(cx, MB - 100 * MS, 6.0 if needle_sid and not kind else 4.2), draw=draw,
                glows=[(MX, MB - 80, 50, 40, bp.NIGHT_MONITOR, 0.4)], lights=[(MX, MB - 80, 160, 1.0)])


def s33():
    """3.3 S6 I: the panel: HUMAN APPROVAL REQUIRED."""
    return panel_insert("HUMAN APPROVAL REQUIRED")


def s34():
    """3.4 v3 (Tomas /grill-me: back to premises; "raises a hand / waves" 2/2 twice): a close at the machine. Don leans
    over the counter's end, his fingertip ON the green button beside the panel (HUMAN APPROVAL REQUIRED readable), his
    face turned away to screen left, to Father, proud. DON: "Approved." """
    def draw(k):
        nc._room(k, pam_behind=False)
        bx, by = MX - 40, MB - 78 * MS                          # the button: round, green, under the panel's left end
        def panel():
            pr.screen(k, MX - 6, MB - 108 * MS, 25, "HUMAN APPROVAL REQUIRED", shape="rect")
            kit.ellipse(k, bx, by, 6, 6, (0.20, 0.75, 0.30), 4810, shadow=False, lw=1.8)
            dial(k, "3.4")
        drawn(panel)
        c = k.c
        dx, dy = 38.4, -200.1                                    # the point hand's place on the rig (pose below), measured
        x, f = bx - dx, by - dy + 4
        c.save(); c.rectangle(x - 400, f - 2000, 800, 2000 - (f - MB) + 10); c.clip()   # behind the counter's top: his
        o = dp.don(k, x, f, SC["don"], (-8, 0, 150, 30), "grin", (-1, -0.2), hands=("relax", "point"))  # eyes open (v3b)
        c.restore()
        return {"don": head(o, "don")}
    g = [(MX, MB - 80, 50, 40, bp.NIGHT_MONITOR, 0.4)]
    POSE["3.4"] = "v3: leaning over the counter, the fingertip on the button, his face to Father"
    return dict(cam=(MX - 50, MB - 70, 3.0), draw=draw, glows=g, lights=[(MX, MB - 80, 160, 1.0)])


def s35():
    """3.5 S6 I: the needle swings into the yellow; the machine shudders a step toward the counter edge."""
    return panel_insert(None, "3.5", shudder=True)


def s36():
    """3.6 v2: a small tick from the machine: only the Client's head turns, and he leans back from it, bracing (his
    eyes on it); Don hasn't heard (cold 2/2: "nothing changes")."""
    def draw(k):
        h = counter_people(k, don=dict(x=780, f=F + 46, face="smug", look=(-1, -0.2)))
        nc._shadow(k, 640, F + 10, 34)
        o = L.tilted(k, 640, F + 8, -0.16, lambda: cp.client(k, 640, F + 8, SC["client"], look=(1, -1.0)))
        h["client"] = head(o, "client")
        def tick():
            c = k.c; c.set_source_rgb(0.98, 0.95, 0.80); c.set_line_width(3); c.set_line_cap(1)
            for a_ in (-0.5, 0.0, 0.5):
                c.move_to(MX + 60 + 6 * math.cos(a_), MB - 120 + 6 * math.sin(a_))
                c.line_to(MX + 60 + 16 * math.cos(a_), MB - 120 + 16 * math.sin(a_)); c.stroke()
            c.set_line_cap(0)
            dial(k, "3.6"); mug_on_counter(k)
        drawn(tick)
        return h
    g, li = glows_room()
    POSE["3.6"] = "v2: the Client leaning back from the machine, eyes on it"
    return dict(cam=(700, F - 150, 2.0), draw=draw, glows=g, lights=li)


def client_flat(k, x, floor, mug_hand=None):
    """3.7-4.2: the Client flat on the floor at the counter's foot, on his back, head to screen left, eyes shut.
    REUSED: of_cast.client_under's laid-down profile (The Offer, approved); the near hand up, holding Pam's mug by its
    handle (episode 15's cups canon: CUP_GRIP)."""
    import client_of as cof
    import da_cups as cups
    cups.install()
    c = k.c
    T = (x, floor - 6)
    L_ = lambda X, Y: (-(Y - T[1]), X - T[0])
    near = mug_hand or (x - 70, floor - 120)
    far = (x - 140, floor - 10)
    c.save(); c.translate(*T); c.rotate(-math.pi / 2)
    o = cof.profile(k, 0, 0, SC["client"], facing=1, look_up=0.0, hands=[L_(*near), L_(*far)])
    c.restore()
    hx, hy = o["head"]
    if mug_hand:                                                # v2: the mug where the rig really put his hand
        u, v = o["hands"][0]                                    # (cold 2/2: "a fist up", the mug apart from it)
        px, py = T[0] + v, T[1] - u
        drawn(lambda: cups.mug(k, px - 22 * 0.9, py - 4, cups.MUG_FLOOR * 0.9, handle=1, kind="mustard", state="held"))
    return (T[0] + hy, T[1] - hx, R["client"] * SC["client"])


def s37():
    """3.7 v2 (cold 2/2: "why is he down", "the failure"): two keys. a: BEFORE the steam: the Client already flat at
    the counter's foot, his eyes on Pam's mug tipping off the edge, his open hand up under it; b: the jet of steam with
    a hiss, the mug caught by its handle, his eyes shut; Pam looks at the hand."""
    import da_cups as cups
    def key(stage):
        def draw(k):
            h = counter_people(k)
            if stage == "a":
                h["client"] = client_flat(k, 900, F + 80, mug_hand=None)
                def tip():
                    cups.install()
                    c = k.c; c.save(); c.translate(MUG_AT[0] - 30, MB + 4); c.rotate(-0.6)
                    cups.mug(k, 0, 0, cups.MUG_FLOOR * 0.9, handle=-1, kind="mustard")
                    c.restore()
                    dial(k, "3.6")
                drawn(tip)
            else:
                h["client"] = client_flat(k, 900, F + 80, mug_hand=(MUG_AT[0] + 10, MB + 50))
                def steam():
                    c = k.c
                    for i_, (dx, dy, r_) in enumerate(((10, -40, 16), (24, -70, 22), (46, -104, 28), (74, -140, 32))):
                        c.set_source_rgba(0.95, 0.96, 1.0, 0.85 - i_ * 0.12)
                        c.arc(MX + 40 * MS + dx, MB - 60 * MS + dy, r_, 0, 2 * math.pi); c.fill()
                    dial(k, "3.7")
                drawn(steam)
            return h
        g, li = glows_room()
        return dict(cam=(760, F - 50, 1.55), draw=draw, glows=g, lights=li)
    POSE["3.7"] = "v2: a: down BEFORE the steam, b: the catch"
    return [key("a"), key("b")]


def s38():
    """3.8 S6 I: the cup: the coffee drops in one tar-like glug; the spoon stands upright in it by itself."""
    import da_cups as cups
    def draw(k):
        nc._room(k, pam_behind=False)
        def cup():
            cups.install()
            x, y = MX - 110, MB + 2                              # v2: on the counter, away from the spout ("pours")
            cups.cup_saucer(k, x, y, 1.6, state="rest")
            c = k.c
            c.set_source_rgb(0.06, 0.04, 0.03); c.save(); c.translate(x, y - 33); c.scale(1, 0.32)
            c.arc(0, 0, 25, 0, 2 * math.pi); c.restore(); c.fill()                           # the tar, a dome over the rim
            c.save(); c.translate(x, y - 35); c.scale(1, 0.5); c.arc(0, 0, 22, math.pi, 2 * math.pi); c.restore(); c.fill()
            c.set_source_rgba(1, 1, 1, 0.5); c.set_line_width(2); c.save(); c.translate(x - 6, y - 40); c.scale(1, 0.4)
            c.arc(0, 0, 9, 3.6, 4.6); c.restore(); c.stroke()                                # its oily shine
            for col, lw in ((INK, 8), ((0.80, 0.82, 0.86), 5)):                              # the spoon, upright, still
                c.set_source_rgb(*col); c.set_line_width(lw); c.set_line_cap(1)
                c.move_to(x + 4, y - 44); c.line_to(x + 10, y - 104); c.stroke()
            c.set_line_cap(0)
            kit.ellipse(k, x + 10, y - 108, 7, 9, (0.80, 0.82, 0.86), 4801, shadow=False, lw=1.8)
        drawn(cup)
        return {}
    return dict(cam=(MX - 110, MB - 50, 5.0), draw=draw, glows=[(MX - 110, MB - 40, 50, 40, bp.NIGHT_WARM, 0.3)],
                lights=[(MX - 110, MB - 40, 160, 0.9)])


def s39():
    """3.9 S1 W: Don carries the cup back over his tape and sets it on the throne's armrest beside Father's chair;
    Father doesn't touch it."""
    import da_cups as cups
    def draw(k):
        nc._room(k)
        drawn(lambda: pss.throne(k))
        h = {"father": father_on_chair(k, look=(-1, 0.4))}
        nc._shadow(k, TX + 40, F + 60, 34)
        o = dp.don(k, TX + 10, F + 58, SC["don"], "stand", "smug", look=(1, -0.2), hands=("relax", "relax"))
        h["don"] = head(o, "don")
        def cup():
            cups.install()
            cups.cup_saucer(k, TX + 66, SEAT_Y - 40, cups.CUP_FLOOR, state="rest")      # on the armrest
        drawn(cup)
        return h
    g, li = glows_room()
    POSE["3.9"] = "v2: the cup set down on the armrest, his hands back (cold: 'cup at his mouth')"
    return dict(cam=(500, F - 110, 1.4), draw=draw, glows=g, lights=li)


def s310():
    """3.10 S3 C: Father's eyes: the cup, then away."""
    import da_cups as cups
    def draw(k):
        nc._room(k, pam_behind=False)
        drawn(lambda: pss.throne(k))
        h = {"father": father_on_chair(k, look=(-1, 0.8))}
        drawn(lambda: (cups.install(), cups.cup_saucer(k, TX + 66, SEAT_Y - 40, cups.CUP_FLOOR, state="rest")))
        return h
    g, li = glows_room()
    return dict(cam=(LINE_X - 30, F - 200, 2.8), draw=draw, glows=g, lights=li)


MAP = {"1.1": s11, "1.2": s12, "1.3": s13, "1.4": s14, "1.5": s15, "1.6": s16, "1.7": s17,
       "2.1": s21, "2.2": s22, "2.3": s23, "2.4": s24, "2.5": s25, "2.6": s26, "2.7": s27,
       "3.1": s31, "3.2": s32, "3.3": s33, "3.4": s34, "3.5": s35, "3.6": s36, "3.7": s37, "3.8": s38, "3.9": s39,
       "3.10": s310}


# ---- rendering and checks ----------------------------------------------------------------------------------------------
class TextRec(cairo.Context):
    """keeps every text shown, in device units (da_layouts.TextRec)."""
    def __new__(cls, surf):
        return super().__new__(cls, surf)

    def __init__(self, surf):
        self.texts = []

    def show_text(self, s):
        x, y = self.get_current_point()
        e = self.text_extents(s)
        pts = [self.user_to_device(x + e.x_bearing + dx, y + e.y_bearing + dy) for dx in (0, e.width) for dy in (0, e.height)]
        self.texts.append(dict(text=s, bbox=(min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts),
                                              max(p[1] for p in pts)), clip=(-1e9, -1e9, 1e9, 1e9)))
        return super().show_text(s)


def geometry(sid, cam, draw):
    """a dry pass (no grade): the texts and the faces this camera gives, and the checks on them."""
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    c = TextRec(s); k = Ctx(c, 0)
    c.save(); sbv.view(c, *cam)
    nc.NO_THRONE_CONFETTI[0] = True
    try:
        heads = draw(k) or {}
    finally:
        nc.NO_THRONE_CONFETTI[0] = False
    c.restore()
    return checks(sid, cam, c.texts, heads)


def search(sid, spec):
    """the first camera near the shot's own that passes the frame checks (offsets in frame px, a closer zoom last;
    da_layouts._render's search)."""
    base = spec["cam"]
    cands = sorted(((ox, oy, zm) for zm in (1.0, 0.92, 1.1, 0.85, 1.2) for ox in range(-180, 181, 15)
                    for oy in range(-150, 151, 15)), key=lambda o: (abs(o[2] - 1.0), abs(o[0]) + abs(o[1])))
    for ox, oy, zm in cands:
        cam = (base[0] + ox / base[2], base[1] + oy / base[2], base[2] * zm)
        if not geometry(sid, cam, spec["draw"]):
            return cam
    return base


def specs(sid):
    """a shot's key frames: one, or several (a: before, b: after) for a change of state."""
    sp = MAP[sid]()
    return sp if isinstance(sp, list) else [sp]


def render(sid, spec=None):
    """-> (surface 540x960, faults). The frame as rv_night_cast._frame draws it, with the texts recorded."""
    spec = spec or specs(sid)[0]
    if "file" in spec:
        img = cairo.ImageSurface.create_from_png(spec["file"])
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
        c.scale(W / img.get_width(), H / img.get_height()); c.set_source_surface(img, 0, 0); c.paint()
        return s, []
    draw = spec["draw"]
    cam = search(sid, spec) if spec.get("search", True) else spec["cam"]
    nc.NO_THRONE_CONFETTI[0] = True
    try:
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
        c = TextRec(s); k = Ctx(c, 0)
        c.set_source_rgb(*kit.WALL); c.paint()
        c.save(); sbv.view(c, *cam); ds._floor_on(c)
        heads = draw(k) or {}
        c.restore()
        fx, fy, z = cam
        floor_y = 480 + (F - fy) * z
        old = rn.FALLOFF[0], rn.GLASS_HI[0]
        rn.FALLOFF[0], rn.GLASS_HI[0] = 0.32, 0.12
        rn.RIM_SEEN[0] = True; rn.FLOOR_END[0] = False; rn.CAST_LIGHT[0] = nc.LOCK_CAST
        try:
            rn.grade(s, cam, floor_y, spec["glows"], rim=spec.get("rim", lambda k_: pss.throne(k_)), lights=spec["lights"],
                     after=lambda c_: rn.moon_patch(c_, cam), people=nc._people_mask(cam, draw))
        finally:
            rn.FALLOFF[0], rn.GLASS_HI[0] = old
            rn.RIM_SEEN[0] = False; rn.FLOOR_END[0] = True; rn.CAST_LIGHT[0] = None
    finally:
        nc.NO_THRONE_CONFETTI[0] = False
    return s, checks(sid, cam, c.texts, heads)


def checks(sid, cam, texts, heads):
    fx, fy, z = cam
    text = []
    for t in texts:
        b = t["bbox"]
        if b[3] - b[1] < MIN_SIGN:
            continue
        text.append(dict(text=t["text"], bbox=((b[0] - 270) / z + fx, (b[1] - 480) / z + fy, (b[2] - 270) / z + fx,
                                               (b[3] - 480) / z + fy), clip=t["clip"]))
    f = dict(cam=cam, heads=heads, scene=dict(text=text), bubbles=[], shot=sid)
    st = sc.STAGE[sid]
    msgs = uz.check_signs(f) + uz.check_scale(f, st["cast"])
    faces = uz.faces(f)
    for n in st["cast"]:
        if n in faces:
            x, y, r = faces[n]
            if not (r <= x <= W - r and 96 + r <= y <= H):
                msgs.append("FRAME: %s's face out of the frame (%d, %d)" % (n, x, y))
        elif sid not in ("1.1",):
            msgs.append("CAST: %s is in the scene file's cast but not drawn" % n)
    if "don" in heads and st["don"] in "LR":
        side = "L" if heads["don"][0] < LINE_X else "R"
        if side != st["don"]:
            msgs.append("TAPE: Don's head on side %s, the scene file says %s" % (side, st["don"]))
    return [m for m in msgs if (sid, m.split(":")[0]) not in KNOWN]


def zones(c):
    import cs_frame as cf
    c.set_source_rgb(0.85, 0.1, 0.1); c.set_line_width(1.5); c.set_dash([6, 4])
    c.move_to(0, cf.BOTTOM); c.line_to(W, cf.BOTTOM); c.stroke()
    c.rectangle(cf.RAIL[0], cf.RAIL[1], W - cf.RAIL[0], cf.RAIL[2] - cf.RAIL[1]); c.stroke(); c.set_dash([])
    c.set_source_rgba(0.1, 0.1, 0.1, 0.18); c.rectangle(0, 0, W, 96); c.fill()


def sheet(act, out_dir=EP):
    tiles = []
    for sid in ACTS[act]:
        sp = specs(sid)
        for n, one in enumerate(sp):
            tiles.append((sid, one, sid + ("abcd"[n] if len(sp) > 1 else "")))
    ids = tiles
    tm = {s["shot"]: s for s in sc.timing()["shots"]}
    cols, tw, th = 4, 270, 480
    nr = (len(ids) + cols - 1) // cols
    SW, SH = 30 + cols * (tw + 30), 110 + nr * (th + 140)
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, SW, SH); c = cairo.Context(s)
    c.set_source_rgb(0.96, 0.95, 0.92); c.paint()
    c.select_font_face("Inter", 0, 1); c.set_font_size(22); c.set_source_rgb(*INK); c.move_to(30, 44)
    c.show_text("APPROVED. · layouts v2 · act %d" % act)
    c.select_font_face("Inter", 0, 0); c.set_font_size(13); c.set_source_rgb(0.3, 0.3, 0.3); c.move_to(30, 70)
    c.show_text("generated by rv_layouts.py from rv_scenes.py · each frame at 270 · red: the apps' zones · key poses only")
    fails = []
    for i, (sid, one, lab) in enumerate(ids):
        surf, msgs = render(sid, one)
        zones(cairo.Context(surf))
        x = 30 + (i % cols) * (tw + 30); y = 90 + (i // cols) * (th + 140)
        c.save(); c.translate(x, y); c.scale(0.5, 0.5); c.set_source_surface(surf, 0, 0); c.paint(); c.restore()
        t = sc.TEXT[sid]
        c.select_font_face("Inter", 0, 1); c.set_font_size(12); c.set_source_rgb(*INK)
        c.move_to(x, y + th + 18); c.show_text("%s  %s · %.1f s" % (lab, t["setup"], tm[sid]["len"]))
        c.select_font_face("Inter", 0, 0)
        for j, ln in enumerate(textwrap.wrap(t["picture"].replace("**", ""), 44)[:3]):
            c.move_to(x, y + th + 34 + j * 15); c.show_text(ln)
        if t["line"] not in ("—", ""):
            c.set_source_rgb(0.2, 0.3, 0.6); c.move_to(x, y + th + 82); c.show_text(t["line"].replace("**", "")[:46])
        ch = sc.CHANGES.get(sid, {})
        if ch:
            c.set_source_rgb(0.15, 0.40, 0.45); c.move_to(x, y + th + 98)
            c.show_text(("→ " + ", ".join("%s: %s" % kv for kv in ch.items()))[:52])
        ok = not msgs
        c.set_source_rgb(*((0.1, 0.45, 0.2) if ok else (0.8, 0.1, 0.1))); c.move_to(x, y + th + 116)
        c.show_text(("checks pass · " + POSE.get(sid, "locked" if sid == "1.1" else "key pose"))[:52] if ok
                    else ("FAIL: " + "; ".join(m.split(":")[0] for m in msgs))[:60])
        fails += [(sid, m) for m in msgs]
        surf.write_to_png("/tmp/rv_layout_%s.png" % lab)
    out = os.path.join(out_dir, "rv_layout_act%d_v2.png" % act)
    s.write_to_png(out)
    from PIL import Image
    im = Image.open(out); im.resize((im.width // 2, im.height // 2), Image.LANCZOS).save(out.replace(".png", "_feed.png"))
    print("wrote", out)
    return fails


def main(args):
    acts = [int(a) for a in args if a.isdigit()] or [1]
    for sid, fn in sorted(MAP.items()):                       # lesson 109: the map, printed
        print("  %-5s -> %s" % (sid, fn.__name__))
    assert all(MAP[s].__name__ == "s" + s.replace(".", "") for s in MAP), "the map points a shot at another's drawing"
    fails = []
    for a in acts:
        fails += sheet(a)
    for sid, m in fails:
        print("FAIL %-5s %s" % (sid, m))
    return not fails


if __name__ == "__main__":
    sys.exit(0 if main(sys.argv[1:]) else 1)
