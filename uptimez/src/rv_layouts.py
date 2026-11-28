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
import rv_hands as rh
rh.setup()
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
        3: ["3.1", "3.2", "3.3", "3.4", "3.5", "3.6", "3.7", "3.8", "3.9", "3.10"],
        4: ["4.1", "4.2", "4.3", "4.4", "4.5"],
        5: ["5.1", "5.2", "5.3", "5.4", "5.5", "5.6", "5.7", "5.8", "5.9", "5.10", "5.11"],
        6: ["6.1", "6.2", "6.3", "6.4", "6.5", "6.6", "6.7", "6.8", "6.9", "6.10"],
        7: ["7.1", "7.2"]}
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
LIGHT_V3 = [True]    # on for episode 16's layouts (Tomas 28 Nov: the five test frames OK, with the corrections v3b);
                     # was opt-in (Tomas 28 Nov, the night-lighting review, "Darom, kaip sakai"): the light tells the story,
                     # on top of the locked night (rv_night_cast v6 stays as it is). Four layers, all from the sources
                     # already in the room: (1) a warm pool on the floor under the throne (not a spotlight: Tomas's
                     # "warm rim" stays); (2) Pam's monitor on her face; (3) the coffee machine's glow in its needle's
                     # colour, on its body and the counter (rv_scenes.states); (4) contact shadows a little darker.
                     # Inserts can ask for "intimate": the room 15 % darker round a bright centre (the robot's tear).
NEEDLE_COL = {"green": (0.35, 0.90, 0.45), "yellow": (1.0, 0.85, 0.25), "orange": (1.0, 0.55, 0.15),
              "red": (0.91, 0.36, 0.27)}


def light_v3(sid, spec, heads):
    """the extra glows and lights for a frame (LIGHT_V3)."""
    g, li = list(spec["glows"]), list(spec["lights"])
    if spec.get("rim", True) is not None and not spec.get("no_pool"):   # the throne in the room (not its inserts)
        g.append((TX, TF + 4, 120, 30, bp.NIGHT_WARM, 0.425))   # v3b: -15 %     # (1) the warm pool on the floor under the throne
    if "pam" in heads:                                          # (2) her monitor on her face
        hx, hy, r = heads["pam"]
        g.append((hx - r * 0.3, hy + r * 0.1, r * 1.2, r * 1.1, bp.NIGHT_MONITOR, 0.45))
        li.append((hx, hy, 90, 0.8))
    col = NEEDLE_COL[sc.states()[sid]["needle"]]                 # (3) the machine in its needle's colour
    g.append((MX + 36 * MS, MB - 108 * MS, 30, 24, col, 0.42))   # v3b: the halo -30 %, tighter (the needle's contrast)
    g.append((MX, MB + 6, 120, 26, col, 0.28))                   # v3b: the spill on the counter -20 % (Pam's eyes)
    li.append((MX, MB - 60, 150, 0.6))
    return g, li
POSE = {}                                                      # shot -> "stand-in" note for the sheet


def head(o, who, key="head"):
    x, y = o[key][:2]
    return (x, y, R[who] * SC[who])


def rot(px, py, ox, oy, a):
    """a point drawn inside rotate(a) about (ox, oy), in the outer coordinates."""
    dx, dy = px - ox, py - oy
    return (ox + dx * math.cos(a) - dy * math.sin(a), oy + dx * math.sin(a) + dy * math.cos(a))


_shadow0 = nc._shadow


def _shadow_v3(k, x, f, w, a=0.30):
    return _shadow0(k, x, f, w, a + 0.10 if LIGHT_V3[0] else a)   # (4) contact shadows a little darker


nc._shadow = _shadow_v3


FATHER_SKIN = (0.94, 0.80, 0.68)


def held_sheet(k, h, draw_sheet, name, half_w=20, down=40, pose="CLUTCH", **_old):
    """a sheet, card, tag or chair in a hand the rig freed (rh.without_hands), BY THE CANON'S FUNCTION (28 Nov, outside
    review: "vis dar nesilaikom ranku canon"): the thing first, then the hand over it.
      CLUTCH  row clutch -> of_cast.clutch: the back of the hand on the thing's top edge, four fingers down over its
              front, the thumb under; draw_sheet(k, P) puts the thing's TOP EDGE at P (its middle under the hand).
      PINCH   row pinch -> hands_ps "pinch" (hands_v4's sheet shape): draw_sheet(k, P) puts the thing at the fingertips P.
    Declared to the gate (its AIR rule). The forearm reaches the hand from behind the thing, or from above it."""
    import hands_ps as hp
    if pose == "CLUTCH":
        P = rh.clutch(k, h)
    else:
        x, y, d, w = rh._local(k, h)
        P = (x + d[0] * 0.95 * w, y + d[1] * 0.95 * w)
    if nc._PASS[0] != "mask":
        rh.prop(k, name, P[0] - half_w - 4, P[1] - 8, 2 * half_w + 8, down + 10)
        draw_sheet(k, P)
    if pose == "CLUTCH":
        rh.clutch_draw(k, h, P)
    else:
        x, y, d, w = rh._local(k, h)
        hp.draw(k, "pinch", x, y, w, h["skin"], d, h["arm"])
    return P


def tapered(draw):
    """the canon arm (rules-hands, "The arm": the wrist narrower than the forearm, a real elbow): E15's da_arms.tapered
    around one shot's drawing; opt-in per shot, so the locked frames stay as they are (cold v5: "tube arms" 5.3/5.10/5.11)."""
    import da_arms
    def d(k):
        with da_arms.tapered():
            return draw(k)
    return d


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
    return dict(file=os.path.join(EP, "rv_K1_v8.png"))


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
        o_f, held = rh.without_hands(k, lambda: dc.father(k, LINE_X + 50, F + 38, SC["father"], pose=(-30, -40, 20, 0),
                                                         look=(-1, 0.3)), (0,))
        held_sheet(k, held[0], lambda k_, P: pr.folding_chair(k_, P[0], P[1] + 150 * CHAIR_S * 0.9 - 2, CHAIR_S * 0.9,
                                                              "folded"), "the folded chair", 14, 130)
        o_d = rpo.don_on_back(k, TX - 30, F + 110, SC["don"], "B", arm=(-8, 0, 124, -48), cup_k=1.5)
        return {"father": head(o_f, "father"), "robot": head(o_r, "robot", "screen"),
                "don": (o_d["head"][0], o_d["head"][1], R["don"] * SC["don"])}
    g, li = glows_room()
    POSE["1.4"] = "Father holds the folded chair by its top edge (clutch)"
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
                    rh.prop(k, "the washer", wx - 10, wy - 10, hx + 4 - (wx - 10), 20)   # to the pinch's root (wrist)
                    c.save(); c.translate(wx, wy); c.rotate(-0.25); pr.washer(k, 0, 0, 0.9); c.restore()
                import hands_ps as hp                               # 28 Nov: rows pinch / quiet by their function
                hp.draw(k, "pinch" if held else "quiet", hx, hy, W_HAND * 1.2, cob.SKIN, (-1, 0.08), 1)
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
    o = rh.father(k, x, vfeet, s, look=look)
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
                if word == "TOMORROW":                                         # the ringed hand at its corner: the
                    import hand_lib_v4 as hl                                   # library's PINCH (canon: thumb and index
                    tip = (hx + 56, hy + 2)                                    # meeting), the wrist stub and velvet
                    wr = (tip[0] + 1.28 * 20, tip[1] - 2)                      # sleeve out of the frame's right edge
                    kit.cut(k, [(wr[0] + 150, wr[1] - 30), (wr[0] + 150, wr[1] + 16), (wr[0] + 22, wr[1] + 11),
                                (wr[0] + 22, wr[1] - 11)], (0.45, 0.10, 0.16), lw=2)          # the sleeve, tapering
                    kit.cut(k, [(wr[0] + 24, wr[1] - 8), (wr[0] + 24, wr[1] + 8), (wr[0] - 2, wr[1] + 6),
                                (wr[0] - 2, wr[1] - 6)], FATHER_SKIN, shadow=False, lw=2)     # the wrist, narrower
                    rh.prop(k, "the tag", hx - 62, hy - 66, wr[0] + 4 - (hx - 62), 90)   # to the pinch's root: the
                                                                       # gate measures a hands_ps hand at its wrist
                    import hands_ps as hp                              # 28 Nov: row pinch by its function
                    hp.draw(k, "pinch", wr[0], wr[1], 24, FATHER_SKIN, (-1, 0.03), 1)
                    kit.ellipse(k, wr[0] - 10, wr[1] + 4, 3, 3, (0.93, 0.74, 0.22), 4732, shadow=False, lw=1)   # the ring
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
        h["don"] = head(dp.don(k, 340, F + 68, SC["don"], (-62, -36, 62, 36), "shock", look=(1, -0.2),
                               hands=("palm", "palm")), "don")
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
        o_r = rp.robot(k, rx, F + 48, SC["robot"], arms=((-8, 0), (58, 40)), look=(1, -0.3))
        gx, gy = o_r["hands"][1]
        drawn(lambda: pr.report(k, gx + 14, gy - 4, 0.6))
        o_f = rpo.father_folding(k, LINE_X + 10, F + 30, SC["father"], "B", chair_s=CHAIR_S, look=(-1, 0),
                                 arms=(-75, -55, 30, -26), hands=("palm", "quiet"))   # v2: the palm up, toward it
        return {"robot": head(o_r, "robot", "screen"), "father": (o_f["head"][0], o_f["head"][1],
                                                                  R["father"] * SC["father"])}
    g, li = glows_room(robot_screen=(LINE_X - 90, F - 60))
    POSE["2.3"] = "Father's raised palm: stand-in (arm control to the sandbox)"
    return dict(cam=(LINE_X - 30, F - 110, 1.9), draw=draw, glows=g, lights=li)


RC_DX = 0    # 28 Nov: 32 when the price hung under the armrest ("B"); on the crown ("A") the close is as locked


def robot_close(screen_kind=None, badge=True, drop=False, flat=False):
    def draw(k):
        nc._room(k, pam_behind=False)
        x, f = ROBOT_HOME[0] + 220 + RC_DX, F + 40
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
                c.set_source_rgba(1, 1, 1, 0.9 if LIGHT_V3[0] else 0.7)
                c.arc(-1.5, 1, 1.4, 0, 2 * math.pi); c.fill()     # its glint (v3: brighter)
                c.restore()
        drawn(scr)
        return {"robot": head(o, "robot", "screen")}
    x, f = ROBOT_HOME[0] + 220 + RC_DX, F + 40
    return dict(cam=(x, f - 114 * SC["robot"] - 10, 5.0), draw=draw, glows=[(x, f - 55, 40, 32, bp.NIGHT_MONITOR, 0.45)],
                lights=[(x, f - 55, 150, 1.0)], search=False, no_pool=True)   # v3b: as v1 (the review: "a gold fog,
                                                                         # the robot levitates"); only the glint


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


def palm_mug(k, wx, wy, w, ms, skin, side=1):
    """the hand library's SAUCER_SUPPORT (episode 15's cups canon, "on a palm"): the palm up and level at the wrist
    (wx, wy), Pam's mug standing on it, the thumb over its near rim: a waiter's catch (Don's cup on his palm, 1.2)."""
    import hand_lib_v4 as hl
    import da_cups as cups
    cups.install()
    P = hl.POSES["SAUCER_SUPPORT"]["contacts"]["saucer"]
    bx, by = hl.to_screen("SAUCER_SUPPORT", wx, wy, 0.0, w, side, P)
    hl.draw_lr(k, "SAUCER_SUPPORT", wx, wy, (0, -1), w, skin, side, reach=side,   # logged by the gate and hands_lr
               obj=lambda k_: cups.mug(k_, bx, by - 1, ms, handle=-1, kind="mustard", state="held"))
    return bx, by


def client_flat(k, x, floor, mug_hand=None):
    """3.7-4.2: the Client flat on the floor at the counter's foot, on his back, head to screen left. REUSED: the
    canon's "lying on the creeper, face up" (client_of.profile laid down, of_cast.client_under; The Offer).
    v2 (the hand review, 28 Nov; canon: "a mug is held by its handle"; episode 15's cups canon: CUP_GRIP): his elbow on
    the floor, the forearm straight up; the hand library's CUP_GRIP on the mug's handle, the mug first, the thumb over
    the handle's top (one hand, two passes); the coffee level; his other arm out of sight along
    his side (v1's "brown fragment")."""
    import client_of as cof
    import client_ob as co
    import da_cups as cups
    import hand_lib_v4 as hl
    cups.install()
    c = k.c
    s_ = SC["client"]
    T = (x, floor - 6)
    L_ = lambda X, Y: (-(Y - T[1]), X - T[0])
    sh = (T[0] + (co.BT + 30) * s_, T[1] - 4 * s_)             # his near shoulder, laid down
    elbow = (sh[0] + co.LN1 * s_ * 0.92, floor - 4)
    hand_pt = (elbow[0], elbow[1] - co.LN2 * s_ * 0.98)         # the forearm straight up
    near = hand_pt                                              # v2b: the same arm in both keys (a: open, b: the mug)
    far = (T[0] + (co.BT + 90) * s_, T[1] - 18 * s_)           # v2b: inside his chest, out of sight ("a loose hand")
    def body_shadow():                                          # v3b (the review: "no contact under the head, shoulders,
        c.save(); c.translate(T[0] + (co.HY * 0.5) * s_, floor + 2)   # back and heels"): one long soft shadow under him
        c.scale(-co.HY * 0.56 * s_, 9); c.set_source_rgba(0, 0, 0, 0.30); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
    drawn(body_shadow)
    c.save(); c.translate(*T); c.rotate(-math.pi / 2)
    o = cof.profile(k, 0, 0, s_, facing=1, look_up=0.0, hands=[L_(*near), L_(*far)])
    c.restore()
    hx, hy = o["head"]
    def hold():
        w = 20.0                                                # v2b: smaller, so the handle shows past the fist
        wx, wy = hand_pt[0], hand_pt[1] + 0.35 * w
        kit.ellipse(k, hand_pt[0], hand_pt[1], 13, 12, co.SKIN, 4830, shadow=False, lw=0)   # the rig's round hand, hidden
        if not mug_hand:                                        # a: the palm open, up, under where the mug will fall
            import hands_ps as hp                               # 28 Nov: row palm by its function
            hp.draw(k, "palm", wx, wy, w * 1.2, co.SKIN, (0, -1), 1)
            return
        palm_mug(k, hand_pt[0] - 4, hand_pt[1] + 2, w, cups.MUG_FLOOR * 0.95, co.SKIN)   # v3 (Tomas: "another grip
                                                                # or the saucer hold"): the mug standing on his level palm
    drawn(hold)
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
                def steam_():
                    steam(k, MX + 40 * MS, MB - 60 * MS)
                    dial(k, "3.7")
                drawn(steam_)
            return h
        g, li = glows_room()
        return dict(cam=(760, F - 50, 1.55), draw=draw, glows=g, lights=li)
    def insert():
        """c (Tomas 28 Nov, after two attempts at the lying hand): an insert, the hand alone: his forearm up from the
        frame's bottom edge (the owner implied: he lies below; rules: "at the frame's edge, a hand with a short wrist
        stub passes"), the watch on its strap; v2 (Tomas: "CUP_GRIP failed: another grip or the saucer hold"): Pam's
        mug standing on his level palm (SAUCER_SUPPORT), the coffee level; steam drifting above."""
        import client_ob as co
        import hand_lib_v4 as hl
        import da_cups as cups
        P = (MX - 40, F - 40)                                    # where the hand is, in front of the counter's foot
        def draw(k):
            nc._room(k, pam_behind=False)
            def it():
                cups.install()
                c = k.c
                w = 30.0
                wx, wy = P[0], P[1]
                kit.cut(k, [(wx - 17, wy + 210), (wx + 17, wy + 210), (wx + 11, wy + 4), (wx - 11, wy + 4)], co.SKIN,
                        shadow=False, lw=2)                    # the forearm from the edge, narrower at the wrist
                kit.cut(k, [(wx - 13, wy + 46), (wx + 13, wy + 46), (wx + 13, wy + 56), (wx - 13, wy + 56)],
                        (0.16, 0.12, 0.10), shadow=False, lw=1.4)                           # the watch's strap
                kit.ellipse(k, wx + 2, wy + 51, 9, 9, co.GOLD, 4840, shadow=False, lw=1.6)  # its face (the canon watch)
                kit.ellipse(k, wx + 2, wy + 51, 5.8, 5.8, (0.10, 0.16, 0.14), 4841, shadow=False, lw=1.0)
                bx, by = palm_mug(k, wx, wy, w * 1.2, cups.MUG_FLOOR * 1.7, co.SKIN)   # v2: the mug on his palm
                steam(k, bx + 30, by - 70, seed=4850)
            drawn(it)
            return {}
        return dict(cam=(P[0] + 20, P[1] - 20, 4.2), draw=draw, glows=[(P[0], P[1] - 40, 50, 40, bp.NIGHT_WARM, 0.25)],
                    lights=[(P[0], P[1] - 40, 160, 0.9)], search=False, no_pool=True, insert=True)
    POSE["3.7"] = "v2: a: down BEFORE the steam, b: the catch; c: the insert of the hand (CUP_GRIP)"
    return [key("a"), key("b"), insert()]


def steam(k, x, y, seed=4820):
    """v3b (the review: "soap bubbles"): a jet of steam as ragged, overlapping wisps that widen, drift and thin out as
    they rise; no outline."""
    import random
    rnd = random.Random(seed)
    c = k.c
    for i in range(14):
        u = i / 13.0
        cx_ = x + 8 + 70 * u + rnd.uniform(-6, 6) + 18 * math.sin(u * 3.2)
        cy_ = y - 20 - 150 * u + rnd.uniform(-5, 5)
        rx, ry = 6 + 26 * u + rnd.uniform(0, 5), 4 + 14 * u + rnd.uniform(0, 4)
        c.save(); c.translate(cx_, cy_); c.rotate(rnd.uniform(-0.6, 0.6)); c.scale(rx, ry)
        g_ = cairo.RadialGradient(0, 0, 0.1, 0, 0, 1)
        a = 0.78 * (1 - u) + 0.10
        g_.add_color_stop_rgba(0, 0.96, 0.97, 1.0, a); g_.add_color_stop_rgba(1, 0.96, 0.97, 1.0, 0.0)
        c.set_source(g_); c.arc(0, 0, 1, 0, 2 * math.pi); c.fill(); c.restore()


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
            c.set_source_rgb(0.03, 0.03, 0.03); c.save(); c.translate(x, y - 33); c.scale(1, 0.32)
            c.arc(0, 0, 25, 0, 2 * math.pi); c.restore(); c.fill()                           # the tar, a dome over the rim
            c.save(); c.translate(x, y - 35); c.scale(1, 0.5); c.arc(0, 0, 22, math.pi, 2 * math.pi); c.restore(); c.fill()
            c.set_source_rgba(1, 1, 1, 0.5); c.set_line_width(2); c.save(); c.translate(x - 6, y - 40); c.scale(1, 0.4)
            c.arc(0, 0, 9, 3.6, 4.6); c.restore(); c.stroke()                                # its oily shine
            for col, lw in ((INK, 8), ((0.80, 0.82, 0.86), 5)):                              # the spoon, upright, still
                c.set_source_rgb(*col); c.set_line_width(lw); c.set_line_cap(1)
                c.move_to(x + 4, y - 44); c.line_to(x + 8, y - 82); c.stroke()            # v3b: shorter ("too long")
            c.set_line_cap(0)
            kit.ellipse(k, x + 8, y - 86, 7, 9, (0.80, 0.82, 0.86), 4801, shadow=False, lw=1.8)
            c.set_source_rgba(1, 1, 1, 0.75); c.set_line_width(2.4); c.set_line_cap(1)          # v3b: tar's hard glints
            c.move_to(x - 14, y - 40); c.line_to(x - 6, y - 43); c.stroke()                     # ("melted chocolate")
            c.move_to(x + 12, y - 41); c.line_to(x + 16, y - 40); c.stroke(); c.set_line_cap(0)
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



# ---- Act IV: almost decided --------------------------------------------------------------------------------------------
def card_on_seat(k):
    pr.name_card(k, TX, SEAT_Y - 2, 0.42)                       # the Client's tent card on the throne's seat


def s41():
    """4.1 S1 W: Father props the Client's name card on the throne's seat; Don's face falls: he is losing the chair."""
    def draw(k):
        nc._room(k)
        drawn(lambda: pss.throne(k))
        drawn(lambda: card_on_seat(k))
        o = rpo.father_folding(k, LINE_X, F + 30, SC["father"], "B", chair_s=CHAIR_S, look=(-1, 0.3),
                               arms=(-58, -32, 30, -26), hands=("quiet", "quiet"))
        h = {"father": (o["head"][0], o["head"][1], R["father"] * SC["father"])}
        nc._shadow(k, 360, F + 80, 34)
        h["don"] = head(dp.don(k, 360, F + 78, SC["don"], "stand", "panic", look=(1, 0.3)), "don")
        return h
    g, li = glows_room()
    POSE["4.1"] = "Father's hand leaving the card: stand-in"
    return dict(cam=(450, F - 110, 1.45), draw=draw, glows=g, lights=li)


def father_smile(k, o, s_):
    """a barely visible smile over dh_cast.father's flat mouth (the rig has only 'hard' and 'talk'; v2, 4.2's "contempt"
    2/2): the line kept, its screen-right corner lifted, a small crease beside it."""
    c = k.c
    hx, hy = o["head"][:2]
    my = hy + 31.5 * s_
    c.set_source_rgb(*INK); c.set_line_width(4.2 * s_); c.set_line_cap(1)
    c.new_path(); c.move_to(hx - 10 * s_, my + 0.5 * s_)
    c.curve_to(hx - 2 * s_, my + 2.2 * s_, hx + 6 * s_, my + 1.0 * s_, hx + 12 * s_, my - 3.2 * s_); c.stroke()
    c.set_line_width(1.6 * s_); c.new_path(); c.move_to(hx + 13 * s_, my - 7 * s_); c.line_to(hx + 15 * s_, my - 1 * s_)
    c.stroke(); c.set_line_cap(0)


def s42():
    """4.2 S6 MC: Father leans to the Client, flat under the counter, the mug still on his palm; a barely visible
    smile, for the Client only; v3: leaning TOWARD him, his finger at the mug, clearly apart. FATHER: "Good hands." """
    import hands_ps as hp
    def draw(k):
        h = counter_people(k)
        h["client"] = client_flat(k, 900, F + 80, mug_hand=True)
        nc._shadow(k, 650, F + 30, 34)
        def fa():
            o_ = rh.father(k, 650, F + 28, SC["father"], hands=("quiet", "point"), pose=(-8, 0, 50, 30), look=(1, 1.0))
            father_smile(k, o_, SC["father"])
            return o_
        o = L.tilted(k, 650, F + 28, 0.24, fa)
        h["father"] = head(o, "father")
        drawn(lambda: dial(k, "4.2"))
        return h
    g, li = glows_room()
    POSE["4.2"] = "v3: leaning to him, the finger at the mug, a sly smile (overlay)"
    return dict(cam=(700, F - 70, 1.9), draw=draw, glows=g, lights=li)


def s43():
    """4.3 S4 MC v3 (the gesture changed after two misreads): two keys at his belt: a: his palms up, apart, low in front
    of him, eyes down on them; b: turned over, backs up, still looking."""
    def key(hands):
        def draw(k):
            nc._room(k, pam_behind=False)
            drawn(lambda: pss.throne(k))
            nc._shadow(k, TX - 60, F + 60, 34)
            o = dp.don(k, TX - 60, F + 58, SC["don"], (-28, 46, 28, -46), "confused", look=(0, 1.0), hands=hands)
            return {"don": head(o, "don")}
        g, li = glows_room()
        return dict(cam=(TX - 60, F - 100, 2.4), draw=draw, glows=g, lights=li)
    POSE["4.3"] = "v3: two keys, palms up then turned over, low and apart"
    return [key(("palm", "palm")), key(("quiet", "quiet"))]


def s44():
    """4.4 S6 M v3: two keys: a: Pam's eyes on Father (screen left, up); b: on the robot at the frame's left edge, the
    refused report still in its gripper. PAM: "Did anyone review the business?" """
    def key(look, robot_in):
        def draw(k):
            h = counter_people(k, pam=False)
            c = k.c                                             # behind the counter: only above its top
            c.save(); c.rectangle(0, 0, 2000, MB - 4); c.clip()
            o = pm.pam(k, nc.MON[0] + 20, F - 72, SC["pam"], "stand", "neutral", look=look, mug=False)
            c.restore()
            h["pam"] = head(o, "pam")
            if robot_in:
                with no_badge():
                    nc._shadow(k, nc.MON[0] - 105, F + 32, 24)
                    o_r = rp.robot(k, nc.MON[0] - 105, F + 30, SC["robot"], arms=((-8, 0), (40, 30)), look=(1, 0))
                gx, gy = o_r["hands"][1]
                drawn(lambda: pr.report(k, gx + 10, gy, 0.6))
            drawn(lambda: dial(k, "4.4"))
            return h
        g, li = glows_room()
        return dict(cam=(nc.MON[0] - 50, F - 130, 1.9), draw=draw, glows=g, lights=li)
    POSE["4.4"] = "v3: two keys, her eyes to Father, then to the robot (in frame)"
    return [key((-1, -0.4), False), key((-1, 0.6), True)]


def s45():
    """4.5 S1 W: nobody moves; in A the robot's head lifts."""
    def draw(k):
        h = {}
        hp_ = nc._room(k)
        drawn(lambda: pss.throne(k))
        drawn(lambda: card_on_seat(k))
        with no_badge():
            nc._shadow(k, ROBOT_HOME[0], F + 14, 26)
            o_r = rp.robot(k, ROBOT_HOME[0], F + 12, SC["robot"], arms=((-8, 0), (40, 30)), look=(1, -0.8))
        gx, gy = o_r["hands"][1]
        drawn(lambda: pr.report(k, gx + 10, gy, 0.6))
        h["robot"] = head(o_r, "robot", "screen")
        h["father"] = father_on_chair(k, look=(-1, 0))
        nc._shadow(k, 380, F + 80, 34)
        h["don"] = head(dp.don(k, 380, F + 78, SC["don"], "stand", "neutral", look=(1, 0)), "don")
        nc._shadow(k, 300, F + 40, 28)
        pr.sofia_ceo(k, 300, F + 38, SC["sofia"], "hold", "smile", look=(1, 0))
        return h
    g, li = glows_room(robot_screen=(ROBOT_HOME[0], F - 50))
    POSE["4.5"] = "the robot's head up (look): key pose"
    return dict(cam=(420, F - 110, 1.15), draw=draw, glows=g, lights=li)



# ---- Act V: the robot returns ------------------------------------------------------------------------------------------
def s51():
    """5.1 S2 M: the robot at its station, head up. ROBOT: "Yes." """
    def draw(k):
        nc._room(k, pam_behind=False)
        with no_badge():
            nc._shadow(k, ROBOT_HOME[0], F + 14, 26)
            o = rp.robot(k, ROBOT_HOME[0], F + 12, SC["robot"], arms=((-8, 0), (40, 30)), look=(1, -0.8))
        gx, gy = o["hands"][1]
        drawn(lambda: pr.report(k, gx + 10, gy, 0.6))
        return {"robot": head(o, "robot", "screen")}
    g, li = glows_room(robot_screen=(ROBOT_HOME[0], F - 50))
    return dict(cam=(ROBOT_HOME[0] + 20, F - 70, 2.6), draw=draw, glows=g, lights=li)


def s52():
    """5.2 S1 W: it rolls to Father; the report unfurls from its chest, accordion-folding over Don's shoes; Don steps
    back; the paper follows."""
    def draw(k):
        nc._room(k)
        drawn(lambda: pss.throne(k))
        h = {"father": father_on_chair(k, look=(-1, 0.4))}
        rx = LINE_X - 110
        with no_badge():
            nc._shadow(k, rx, F + 30, 26)
            o = rp.robot(k, rx, F + 28, SC["robot"], arms=((-8, 0), (44, 36)), look=(1, -0.2))
        h["robot"] = head(o, "robot", "screen")
        gx, gy = o["hands"][1]
        drawn(lambda: pr.report(k, rx - 10, gy + 6, 0.9, unfurl=1.6))         # the strip down and along to Don
        nc._shadow(k, rx - 230, F + 90, 34)
        h["don"] = head(L.tilted(k, rx - 230, F + 88, -0.12, lambda: dp.don(k, rx - 230, F + 88, SC["don"],
                                                                             (-62, -36, 62, 36), "shock", look=(1, 0.8),
                                                                             hands=("palm", "palm"))), "don")
        return h
    g, li = glows_room(robot_screen=(LINE_X - 110, F - 40))
    POSE["5.2"] = "Don stepping back from the paper: stand-in (balance, leaning back)"
    return dict(cam=(400, F - 80, 1.25), draw=draw, glows=g, lights=li)


def s53():
    """5.3 S3 MC: the gripper tears off one sheet and holds it out to Father across a clear gap; Father takes it in his
    fingertips (pinch)."""
    import hands_ps as hp
    def draw(k):
        nc._room(k, pam_behind=False)
        drawn(lambda: pss.throne(k))
        rx = LINE_X - 170
        with no_badge():
            nc._shadow(k, rx, F + 30, 26)
            o = rp.robot(k, rx, F + 28, SC["robot"], arms=((-8, 0), (52, 46)), look=(1, -0.2))
        gx, gy = o["hands"][1]
        of = rpo.father_folding(k, LINE_X + 10, F + 30, SC["father"], "B", chair_s=CHAIR_S, look=(-1, 0.3),
                                arms=(-20, -90, 30, -26), hold=(0,))   # v5: elbow bent, the sheet at
                                                                                            # his chest (was a pole, cold 1/2)
        held_sheet(k, of["held"][0], lambda k_, P: pr.invoice(k_, P[0] - 12, P[1] + 58 * 0.45, 0.45, ang=0.0),
                   "the invoice", 22, 52)                     # canon clutch on its top edge near the corner, the words
                                                                     # clear (28 Nov)
        return {"robot": head(o, "robot", "screen"), "father": (of["head"][0], of["head"][1], R["father"] * SC["father"])}
    g, li = glows_room(robot_screen=(LINE_X - 170, F - 40))
    POSE["5.3"] = "the sheet in Father's clutch (its edge) at his chest, the elbow bent, the gripper let go, a clear gap"
    return dict(cam=(LINE_X - 60, F - 110, 1.9), draw=tapered(draw), glows=g, lights=li)


def s54():
    """5.4 S3 I: the sheet: COFFEE MACHINE REPAIR · $80 · UNPAID (a red stamp)."""
    def draw(k):
        def it():                                               # an insert: Father's dark velvet behind the sheet
            kit.cut(k, [(TX - 200, F - 600), (TX + 200, F - 600), (TX + 200, F), (TX - 200, F)], (0.31, 0.04, 0.10),
                    shadow=False, lw=0)
            pr.invoice(k, TX, F - 300, 1.0, ang=-0.04)
        drawn(it)
        return {}
    return dict(cam=(TX, F - 300, 3.6), draw=draw, glows=[(TX, F - 300, 70, 70, bp.NIGHT_WARM, 0.2)],
                lights=[(TX, F - 300, 200, 0.8)], search=False, no_pool=True, insert=True)


def s55():
    """5.5 S3 MC: Father folds it into his inside pocket and reads the report, the only one reading anything."""
    def draw(k):
        nc._room(k, pam_behind=False)
        drawn(lambda: pss.throne(k))
        of = rpo.father_folding(k, LINE_X + 10, F + 30, SC["father"], "B", chair_s=CHAIR_S, look=(0, 1.0),
                                arms=(-30, 70, 30, -70), hold=(0, 1))
        hx, hy = of["head"]
        import hands_v4 as hv                                   # row board_two, its canon function (28 Nov)
        PL = rh.clutch(k, of["held"][0]); PR = rh.clutch(k, of["held"][1])
        w = rh._local(k, of["held"][0])[3]
        mx, my = (PL[0] + PR[0]) / 2, (PL[1] + PR[1]) / 2
        bw = abs(PR[0] - PL[0]) + 0.84 * w                      # the clutches land on the two upper corners
        sw = bw / 60.0; bh = 40 * sw
        if nc._PASS[0] != "mask":
            rh.prop(k, "the report", mx - bw / 2 - 4, my - 8, bw + 8, bh + 12)
        hv.board_two(k, mx, my + bh / 2, bw, bh, 0.0, w, of["held"][0]["skin"], of["held"][1]["skin"],
                     lambda k_: pr.report(k_, mx, my + bh / 2, sw) if nc._PASS[0] != "mask" else None)
        return {"father": (hx, hy, R["father"] * SC["father"])}
    g, li = glows_room()
    POSE["5.5"] = "reading: the report in two hands (hands_v4.board_two: a clutch at each upper corner)"
    return dict(cam=(LINE_X + 10, F - 120, 2.4), draw=draw, glows=g, lights=li)


def s56():
    """5.6 S3 I: the robot's screen: UPTIME 100%."""
    return robot_close("UPTIME 100%", badge=False)


def s57():
    """5.7 S4 C: Don: his eyes close mid-yawn, his head nods, he jerks awake."""
    def draw(k):
        nc._room(k, pam_behind=False)
        drawn(lambda: pss.throne(k))
        nc._shadow(k, TX - 70, F + 60, 34)
        o = L.tilted(k, TX - 70, F + 58, 0.06, lambda: dp.don(k, TX - 70, F + 58, SC["don"], "stand", "squint",
                                                              look=(0, 0.6)))
        return {"don": head(o, "don")}
    g, li = glows_room()
    POSE["5.7"] = "the nod (squint, the head forward): key pose of three (the yawn, the nod, the jerk)"
    return dict(cam=(TX - 70, F - 159, 3.2), draw=draw, glows=g, lights=li,
                search=False)   # 28 Nov: by hand; with episode 15's price tag the search kept no frame with his hands


def s58():
    """5.8 S3 I: the robot's screen: SALARY $0."""
    return robot_close("SALARY $0", badge=False)


def s59():
    """5.9 S3 MC: Father straightens in his cheap chair; his eye goes up to the $49,999 tag on the crown (28 Nov:
    episode 15's swing ticket, style A, on the crown's LEFT point; v1-v2 had episode 14's card on the right).
    FATHER (slow, quiet): "There it is." """
    def draw(k):
        nc._room(k, pam_behind=False)
        drawn(lambda: pss.throne(k))
        of = rpo.father_folding(k, LINE_X + 10, F + 30, SC["father"], "A", chair_s=CHAIR_S, look=(-1, -1.0))
        tx_, tf_, ts_ = pss.THRONE
        tag = (tx_ - 52 * ts_, tf_ - 347 * ts_)                 # the card's middle (dh_props "A": knot -52, -404)
        def eyeline():                                          # a faint dotted line from his eye to the tag (layout only)
            c = k.c; c.set_source_rgba(0.95, 0.85, 0.4, 0.55); c.set_line_width(1.6); c.set_dash([4, 5])
            c.move_to(of["head"][0] - 8, of["head"][1] - 6); c.line_to(*tag); c.stroke(); c.set_dash([])
        drawn(eyeline)
        return {"father": (of["head"][0], of["head"][1], R["father"] * SC["father"])}
    g, li = glows_room()
    POSE["5.9"] = "v3: his eyes up to the tag on the crown's left point, the tag and his face in one frame"
    return dict(cam=(TX + 70, F - 250, 2.0), draw=draw, glows=g, lights=li)


DX510 = TX - 112   # 5.10 v5: Don beside the throne (sandbox 28 Nov: four trials; in front of it his hand had no edge)


def s510():
    """5.10 S4 MC: Don, smiling proudly at Father (he thinks Father admires the chair), tilts the throne's back to show
    it. DON: "It reclines." """
    def draw(k):
        keep = pss.throne                                       # the room's own throne off: only the tilted one
        pss.throne = lambda *a, **kw: None
        try:
            nc._room(k, pam_behind=False)
        finally:
            pss.throne = keep
        c = k.c
        def thr():
            c.save(); c.translate(TX, SEAT_Y); c.rotate(0.16); c.translate(-TX, -SEAT_Y)   # the back, tilted back a little
            pss.throne(k); c.restore()
        drawn(thr)
        nc._shadow(k, DX510, F + 60, 34)                         # v5: beside the throne, not in front of it; the elbow
        o = dp.don(k, DX510, F + 58, SC["don"], (-8, 0, 40, 75), "grin", look=(1, -0.2),
                   hands=("quiet", "palm"))                     # row palm by its function (hands_ps through the rig's
                                                                # kit.HAND), flat on the back's edge (cold r3: 2/2 reads)
        def push_lines():                                       # two motion marks at the back's top: it tips back
            c.set_source_rgb(*INK); c.set_line_width(2.4); c.set_line_cap(1)
            for i in range(2):
                c.move_to(TX + 60 + i * 10, SEAT_Y - 150 - i * 12); c.curve_to(TX + 76 + i * 10, SEAT_Y - 140 - i * 12,
                                                                                  TX + 80 + i * 10, SEAT_Y - 124 - i * 12,
                                                                                  TX + 78 + i * 10, SEAT_Y - 110 - i * 12)
                c.stroke()
            c.set_line_cap(0)
        drawn(push_lines)
        return {"don": head(o, "don")}
    g, li = glows_room()
    POSE["5.10"] = "beside the throne, his open palm pressing the back's gold edge, the elbow bent, the back tipping"

    def rim(k_):                                                # the warm rim on the tilted throne (one tag, not two)
        k_.c.save(); k_.c.translate(TX, SEAT_Y); k_.c.rotate(0.16); k_.c.translate(-TX, -SEAT_Y)
        pss.throne(k_); k_.c.restore()
    return dict(cam=(TX - 14, F - 170, 1.52), draw=tapered(draw), glows=g, lights=li, rim=rim,
                search=False)   # v5: the tag whole (G3), Don whole; the search kept cutting the tag


def s511():
    """5.11 S3 M: Father takes the Client's card off the throne: the card in one hand, the report in the other. Doubt.
    Behind, small on the counter: the needle in the orange.
    28 Nov, canon: the card held up by its top edge (of_cast.clutch, the forearm behind it from below), the report
    resting on his knee, his other hand on its top edge from above (of_cast.clutch). No palm on a sheet (no canon row)."""
    def draw(k):
        nc._room(k, pam_behind=False)
        drawn(lambda: pss.throne(k))
        of = rpo.father_folding(k, LINE_X + 10, F + 30, SC["father"], "B", chair_s=CHAIR_S, look=(-0.4, 0.3),
                                arms=ARMS511, hold=(0, 1))
        hx, hy = of["head"]
        held_sheet(k, of["held"][0], lambda k_, P: pr.name_card(k_, P[0] - 14, P[1] + 50 * 0.5, 0.5), "the Client's card",
                   26, 30)
        held_sheet(k, of["held"][1], lambda k_, P: pr.report(k_, P[0], P[1] + 20 * 0.7, 0.7), "the report", 22, 30)
        drawn(lambda: dial(k, "5.11"))
        return {"father": (hx, hy, R["father"] * SC["father"])}
    g, li = glows_room()
    POSE["5.11"] = "the card held up by its top edge, the report on his knee held by its top edge, his eyes on the card"
    return dict(cam=CAM511[0], draw=tapered(draw), glows=g, lights=li, search=False)


ARMS511 = (-5, -110, 25, -50)    # sandbox 28 Nov, 4 trials: the card whole, the palm on the knee
CAM511 = [(LINE_X - 2, F - 110, 2.6)]   # by hand: the plaque out above, the floor tape out below (G3)


# ---- Act VI: human approval required -----------------------------------------------------------------------------------
def robot_in_throne(k, kind, look=(1, 0)):
    """the robot set on the throne's cushion (K2's staging, rv_keys.k2), badge-free; its screen shows `kind`."""
    import rv_keys as rk
    with no_badge():
        r = rp.robot(k, TX, SEAT_Y + 4, SC["robot"], look=look)
    sx, sy = r["screen"][:2]
    face = rk._don_head if kind == "APPROVER: CEO" else None
    drawn(lambda: pr.screen(k, sx, sy, 50 * SC["robot"] * 1.16, kind, face_fn=face))
    return head(r, "robot", "screen")


HIPS = (-62, 80, 62, -80)   # fists on the hips, elbows out (rules: no crossed forearms; don_ps "vest" read as
                            # "crossed arms / hugging himself", cold 6.7 v1; three trials on a sheet, this one at the waist)


def s61():
    """6.1 S1 W: the robot sits in the throne, formally. Its screen: HUMAN APPROVAL REQUIRED (the same drawing as 3.3)."""
    def draw(k):
        nc._room(k)
        drawn(lambda: pss.throne(k))
        h = {"robot": robot_in_throne(k, "HUMAN APPROVAL REQUIRED")}
        h["father"] = father_on_chair(k, look=(-1, -0.2))
        nc._shadow(k, 360, F + 80, 34)
        h["don"] = head(dp.don(k, 360, F + 78, SC["don"], "stand", "shock", look=(1, -0.4)), "don")
        return h
    g, li = glows_room(robot_screen=(TX, SEAT_Y - 55))
    return dict(cam=(450, F - 120, 1.4), draw=draw, glows=g, lights=li)


def s62():
    """6.2 S3 MC: K2 v3, locked (rv_keys.k2): APPROVER: CEO with Don's face; Father's finger stops."""
    return dict(file=os.path.join(EP, "rv_K2_v6.png"))


def s63():
    """6.3 S1 W: Father turns to Don. Everyone turns to Don: Sofía, Pam, the robot, the Client's eyes over the
    counter's edge."""
    def draw(k):
        h = {}
        nc._room(k, pam_behind=False)
        c = k.c
        c.save(); c.rectangle(0, 0, 4000, MB - 4); c.clip()     # behind the counter: Pam, and the Client's eyes over it
        h["pam"] = head(pm.pam(k, nc.MON[0] + 20, F - 72, SC["pam"], "stand", "neutral", look=(-1, 0.2), mug=False), "pam")
        h["client"] = head(cp.client(k, 720, MB + 40 + 300 * SC["client"], SC["client"], look=(-1, 0.3)), "client")
        c.restore()
        drawn(lambda: pss.throne(k))
        h["robot"] = robot_in_throne(k, "APPROVER: CEO", look=(-1, 0.2))
        h["father"] = father_on_chair(k, look=(-1, 0.2))
        nc._shadow(k, 300, F + 40, 28)
        h["sofia"] = head(pr.sofia_ceo(k, 300, F + 38, SC["sofia"], "hold", "smile", look=(1, 0.3)), "sofia")
        nc._shadow(k, 390, F + 90, 34)
        h["don"] = head(dp.don(k, 390, F + 88, SC["don"], "stand", "panic", look=(0, 0)), "don")
        return h
    g, li = glows_room(robot_screen=(TX, SEAT_Y - 55))
    POSE["6.3"] = "every head to Don: key pose"
    return dict(cam=(500, F - 110, 1.15), draw=draw, glows=g, lights=li)


def don_close(arm=None, hands=("relax", "relax"), look=(1, -0.2), face="neutral", size=2.6, dy=0):
    def draw(k):
        nc._room(k, pam_behind=False)
        drawn(lambda: pss.throne(k))
        h = {"robot": robot_in_throne(k, "APPROVER: CEO")}
        nc._shadow(k, TX - 100, F + 70, 34)
        o = dp.don(k, TX - 100, F + 68, SC["don"], arm or "stand", face, look=look, hands=hands)
        h["don"] = head(o, "don")
        return h
    g, li = glows_room(robot_screen=(TX, SEAT_Y - 55))
    return dict(cam=(TX - 70, F - 150 + dy, size), draw=draw, glows=g, lights=li)


def s64():
    """6.4 S4 C: push in on Don's eyes: for the first time he reads what he is approving."""
    sp = don_close(look=(1, -0.6), face="confused", size=4.2, dy=-40)
    sp["cam"], sp["search"] = (392, 640, 3.2), False             # 28 Nov: at 4.2 no camera kept episode 15's price tag
    POSE["6.4"] = "his eyes on the screen: Don, the $49,999 and APPROVER: CEO with his face in one frame"   # whole or out
    return sp


def s65():
    """6.5 S4 MC: his fingertip rises toward the screen, the same gesture as 3.4, and hovers."""
    POSE["6.5"] = "the point toward the screen, clearly apart (rules: no finger at a sign)"
    return don_close(arm=(-8, 0, 118, 20), hands=("relax", "point"), look=(1, -0.5), face="neutral")


def s66():
    """6.6 S4 MC: his eyes go to the robot in his throne (v2: up to the crown: HIS chair). The hand freezes."""
    POSE["6.6"] = "v2: his eyes up to the crown, the finger frozen"
    return don_close(arm=(-8, 0, 118, 20), hands=("relax", "point"), look=(0.6, -1.0), face="shock", dy=-40)


def s67():
    """6.7 S4 M: the hand pulls back. Fists on his hips. Two full seconds of silence."""
    POSE["6.7"] = "fists on hips (rules: standing, fists on the hips, elbows out)"
    return don_close(arm=HIPS, hands=("fist", "fist"), look=(1, -0.2), face="neutral", size=2.0)


def s68():
    """6.8 S3 M: Sofía adjusts her new HR card."""
    import robot_tg as rt
    def draw(k):
        nc._room(k, pam_behind=False)
        nc._shadow(k, 300, F + 40, 28)
        o = pr.sofia_ceo(k, 300, F + 38, SC["sofia"], "hold", "smile", look=(0.3, 0.9))
        hx, hy = o["head"][:2]
        def card():
            c = k.c
            c.save(); c.translate(hx + 16 * SC["sofia"], hy + 120 * SC["sofia"]); c.scale(0.5, 0.5)
            rt.tg_badge(k, -29, -20, 5010)
            c.restore()
        drawn(card)
        return {"sofia": head(o, "sofia")}
    g, li = glows_room()
    POSE["6.8"] = "her hand at the card: stand-in (her hold pose)"
    return dict(cam=(300, F - 120, 2.4), draw=draw, glows=g, lights=li)


def s69():
    """6.9 S1 W: the robot sits dead still a beat, then rises slowly and stiffly out of the throne, formal to the last,
    and steps aside."""
    def draw(k):
        nc._room(k)
        drawn(lambda: pss.throne(k))
        with no_badge():
            nc._shadow(k, TX - 80, F + 30, 26)
            o = rp.robot(k, TX - 80, F + 28, SC["robot"], look=(1, 0))
        h = {"robot": head(o, "robot", "screen")}
        h["father"] = father_on_chair(k, look=(-1, 0))
        nc._shadow(k, 330, F + 80, 34)
        h["don"] = head(dp.don(k, 330, F + 78, SC["don"], HIPS, "neutral", look=(1, -0.2), hands=("fist", "fist")), "don")
        return h
    g, li = glows_room(robot_screen=(TX - 80, F - 40))
    POSE["6.9"] = "beside the throne, stepped aside: key pose"
    return dict(cam=(440, F - 110, 1.4), draw=draw, glows=g, lights=li)


def s610():
    """6.10 S3 MC: Father turns the tag TODAY -> TOMORROW; folds his chair and leaves with the report and the Client's
    card, the invoice in his pocket; the spilled tail stays. Don watches him go."""
    def draw(k):
        nc._room(k, pam_behind=False)
        drawn(lambda: pss.throne(k))
        drawn(lambda: pr.report(k, TX - 40, F + 60, 0.7, unfurl=1.0))   # the tail on the floor
        nc._shadow(k, LINE_X + 80, F + 30, 32)
        o, held = rh.without_hands(k, lambda: dc.father(k, LINE_X + 80, F + 28, SC["father"], look=(1, 0)), (0,))
        held_sheet(k, held[0], lambda k_, P: pr.folding_chair(k_, P[0], P[1] + 150 * CHAIR_S * 0.9 - 2, CHAIR_S * 0.9,
                                                              "folded"), "the folded chair", 14, 130)
        h = {"father": head(o, "father")}
        nc._shadow(k, TX - 110, F + 80, 34)
        h["don"] = head(dp.don(k, TX - 110, F + 78, SC["don"], HIPS, "neutral", look=(1, 0), hands=("fist", "fist")), "don")
        return h
    g, li = glows_room()
    POSE["6.10"] = "Father leaving, the folded chair in his clutch"
    return dict(cam=(500, F - 120, 1.7), draw=draw, glows=g, lights=li)



# ---- Act VII: the loop -------------------------------------------------------------------------------------------------
def s71():
    """7.1 S4 M: two keys. a: the room empty, Don stoops to the front-left caster with the folded tag; b: across the
    throne as at frame 0, the report's tail being pulled over his belly, his eyes closing (rv_poses.don_sprawl "B",
    the same pose as K1)."""
    def key_a():
        def draw(k):
            nc._room(k, pam_behind=False)
            drawn(lambda: pss.throne(k))
            drawn(lambda: pr.report(k, TX - 120, F + 70, 0.7, unfurl=1.0))   # the tail, still on the floor
            nc._shadow(k, TX - 110, F + 40, 34)
            o, held = rh.without_hands(k, lambda: dp.don(k, TX - 110, F + 38, SC["don"], (-8, 0, 40, 60), "neutral",
                                                         look=(1, 1.0), hands=False), (1,))
            held_sheet(k, held[1], lambda k_, P: pr.review_tag(k_, P[0], P[1], 0.5), "the tag", 26, 36,
                       pose="PINCH")                            # hands_ps pinch at the string's top (28 Nov)
            return {"don": head(o, "don")}
        g, li = glows_room()
        return dict(cam=(TX - 60, F - 110, 2.0), draw=draw, glows=g, lights=li)

    def key_b():
        def draw(k):
            nc._room(k, pam_behind=False)
            drawn(lambda: pss.throne(k))
            import rv_keys as rk
            drawn(lambda: rk._card_under_caster(k, TX - 80, F + 4, 1.45))        # as K1: the card under the caster
            o = rpo.don_sprawl(k, "B", report=True)
            return {"don": head(o, "don")}
        g, li = glows_room()
        return dict(cam=(454, 756, 1.96), draw=draw, glows=g, lights=li, search=False)
    POSE["7.1"] = "a: the tag unhooked, in his pinch, his eyes on the caster (the stoop: to the sandbox); b: K1's pose"
    return [key_a(), key_b()]


def s72():
    """7.2 S4 M: the same frame as 1.1 (K1 v6): behind the throne the robot's screen glows UPTIME 100%; its gripper
    reaches for the card -> frame 0."""
    return dict(file=os.path.join(EP, "rv_K1_v8.png"))


MAP = {"1.1": s11, "1.2": s12, "1.3": s13, "1.4": s14, "1.5": s15, "1.6": s16, "1.7": s17,
       "2.1": s21, "2.2": s22, "2.3": s23, "2.4": s24, "2.5": s25, "2.6": s26, "2.7": s27,
       "3.1": s31, "3.2": s32, "3.3": s33, "3.4": s34, "3.5": s35, "3.6": s36, "3.7": s37, "3.8": s38, "3.9": s39,
       "3.10": s310, "4.1": s41, "4.2": s42, "4.3": s43, "4.4": s44, "4.5": s45,
       "5.1": s51, "5.2": s52, "5.3": s53, "5.4": s54, "5.5": s55, "5.6": s56, "5.7": s57, "5.8": s58, "5.9": s59,
       "5.10": s510, "5.11": s511, "6.1": s61, "6.2": s62, "6.3": s63, "6.4": s64, "6.5": s65, "6.6": s66, "6.7": s67,
       "6.8": s68, "6.9": s69, "6.10": s610, "7.1": s71, "7.2": s72}


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
    pr.begin_frame()
    try:
        heads = draw(k) or {}
    finally:
        nc.NO_THRONE_CONFETTI[0] = False
    c.restore()
    return checks(sid, cam, c.texts, heads) + pr.cover_faults(s)   # the search also keeps the canon signs whole or out


HAND_FAULTS = {}                                               # label -> the hand gate's faults (rv_hands, da_hand_gate)
HAND_DRAWN = {}


def hand_pass(label, sid, cam, draw):
    """the hand gate on a frame as drawn (a dry pass at the final camera): rv_scenes.HANDS[label] is its job list."""
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    c = cairo.Context(s); k = Ctx(c, 0)
    rh.begin()
    c.save(); sbv.view(c, *cam)
    nc.NO_THRONE_CONFETTI[0] = True
    try:
        import hands_lr
        with hands_lr.shot():
            draw(k)
    finally:
        nc.NO_THRONE_CONFETTI[0] = False
    c.restore()
    HAND_DRAWN[label] = rh.drawn()
    HAND_FAULTS[label] = rh.check(getattr(sc, "HANDS", {}).get(label))
    return HAND_FAULTS[label]


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
    INSERT[0] = bool(spec.get("insert"))
    if "file" in spec:
        img = cairo.ImageSurface.create_from_png(spec["file"])
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
        c.scale(W / img.get_width(), H / img.get_height()); c.set_source_surface(img, 0, 0); c.paint()
        return s, []
    draw = spec["draw"]
    cam = search(sid, spec) if spec.get("search", True) else spec["cam"]
    if LABEL[0]:
        hand_pass(LABEL[0], sid, cam, draw)
    nc.NO_THRONE_CONFETTI[0] = True
    try:
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
        c = TextRec(s); k = Ctx(c, 0)
        c.set_source_rgb(*kit.WALL); c.paint()
        c.save(); sbv.view(c, *cam); ds._floor_on(c)
        pr.begin_frame()                                        # COVER: the signs this frame draws
        heads = draw(k) or {}
        c.restore()
        fx, fy, z = cam
        floor_y = 480 + (F - fy) * z
        old = rn.FALLOFF[0], rn.GLASS_HI[0]
        rn.FALLOFF[0], rn.GLASS_HI[0] = 0.32, 0.12
        rn.RIM_SEEN[0] = True; rn.FLOOR_END[0] = False; rn.CAST_LIGHT[0] = nc.LOCK_CAST
        try:
            gl, li = light_v3(sid, spec, heads) if LIGHT_V3[0] else (spec["glows"], spec["lights"])
            rn.grade(s, cam, floor_y, gl, rim=spec.get("rim", lambda k_: pss.throne(k_)), lights=li,
                     after=lambda c_: rn.moon_patch(c_, cam), people=nc._people_mask(cam, draw))
            if LIGHT_V3[0] and spec.get("intimate"):            # the room 15 % darker round a bright centre
                cx_, cy_ = spec["intimate"]
                X, Y = 270 + (cx_ - fx) * z, 480 + (cy_ - fy) * z
                cc = cairo.Context(s)
                gr = cairo.RadialGradient(X, Y, 90, X, Y, 420)
                gr.add_color_stop_rgba(0, 0, 0, 0, 0.0); gr.add_color_stop_rgba(1, 0.02, 0.03, 0.06, 0.15 / 0.85 * 0.85)
                cc.set_source(gr); cc.paint()
        finally:
            rn.FALLOFF[0], rn.GLASS_HI[0] = old
            rn.RIM_SEEN[0] = False; rn.FLOOR_END[0] = True; rn.CAST_LIGHT[0] = None
    finally:
        nc.NO_THRONE_CONFETTI[0] = False
    return s, checks(sid, cam, c.texts, heads) + pr.cover_faults(s)


LABEL = [None]                                                 # the key's label while the sheet renders it
INSERT = [False]                                               # set while an insert key draws (a cut-in: no cast)


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
        elif sid not in ("1.1", "6.2", "7.2") and not INSERT[0]:
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
        LABEL[0] = lab
        surf, msgs = render(sid, one)
        LABEL[0] = None
        msgs = msgs + ["HAND " + f for f in HAND_FAULTS.get(lab, [])]
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




def light_test(out=os.path.join(EP, "rv_light_v3_test.png")):
    """the five frames the lighting review asked for, before (top) and after LIGHT_V3 (bottom), at 270."""
    from PIL import Image
    picks = [("2.1", 0), ("1.3", 0), ("2.6", 0), ("3.5", 0), ("3.7", 1)]
    sheet_ = Image.new("RGB", (5 * 280, 2 * 490), (255, 255, 255))
    for row, on in enumerate((False, True)):
        LIGHT_V3[0] = on
        for i, (sid, n) in enumerate(picks):
            surf, _ = render(sid, specs(sid)[n])
            surf.write_to_png("/tmp/lt.png")
            sheet_.paste(Image.open("/tmp/lt.png").convert("RGB").resize((270, 480)), (i * 280, row * 490))
    LIGHT_V3[0] = False
    sheet_.save(out); print("wrote", out)


def hands_report(acts=(1, 2, 3, 4, 5, 6, 7)):
    """the hand gate alone, every key of every act, no grade: what is drawn and what fails."""
    n = 0
    for a in acts:
        for sid in ACTS[a]:
            sp = specs(sid)
            for i, one in enumerate(sp):
                lab = sid + ("abcd"[i] if len(sp) > 1 else "")
                if "file" in one:
                    print("%-6s (a locked file)" % lab); continue
                INSERT[0] = bool(one.get("insert"))
                cam = search(sid, one) if one.get("search", True) else one["cam"]   # the camera the sheet uses
                f = hand_pass(lab, sid, cam, one["draw"])
                n += len(f)
                print("%-6s drawn %s" % (lab, HAND_DRAWN[lab]))
                for x in f:
                    print("         " + x)
    print("hand faults:", n)
    return n


if __name__ == "__main__":
    if sys.argv[1:] == ["light"]:
        light_test(); sys.exit(0)
    if sys.argv[1:2] == ["hands"]:
        sys.exit(1 if hands_report() else 0)
    sys.exit(0 if main(sys.argv[1:]) else 1)
