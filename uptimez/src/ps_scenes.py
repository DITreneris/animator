"""PICK A SIDE (episode 14): the scene file, v1 (stage 4, series/production-process.md). From here on this file is the
episode: every shot with its camera, who is in frame and where, the props' state, the line. Generated from it:

  python3 ps_scenes.py [out_dir]  ->  ps_layout_s<N>_v2.png   a layout sheet per scene, every shot at 270 with its checks
                                      pick-a-side-script-v8.md  the script (generated; do not edit by hand)

The pictures, lines and sizes come from script v7 (approved shot by shot through stop 2 and the blocking, 23 Nov),
the timing from the recorded takes (ps_timing_v2.json; 2.1b, 1.2a/b take the script's lengths). Staging from the floor
plan v3 (ps_plan.py) and Tomas's /grill-me (23 Nov): 1.1 Don faces us; 1.2 split; 2.11 he pushes it onto his side;
6.1 Don big front-left on his side, Sofía small back-right past the line. One key pose per shot: the motion is stage 6.
The checks are uz_check's (scale: no story face in the bottom quarter or under the buttons; signs whole or out) and
the loop's (6.2 against 1.1, drawn by the same code). The build stops (exit 1) on a failure not listed in KNOWN.
v2 (23 Nov, Tomas "taisyk"): two-plane shots (6.1, 5.6) draw the near character as a foreground layer in frame units
(one scale for a whole room reads a near man as sunk, lesson 181); DON on the floor smaller, beside the tape
(ps_set.MARK_SMALL); S2 raised so the faces clear the bottom quarter; the wides framed on the faces that tell them;
cameras off the signs. v1 is ps_scenes_v1.py.
v3 (board v1's cold test, 3 viewers, 23 Nov): no screen over the door; the CV in the guard's hand (5.2) and in Sofía's
(5.5); Sofía big, astride the tape (5.6); the blind hangs from Pam's rail; 3.6 the guard's phone lit at his face; 6.1
the others' eyes off Don. v2 is ps_scenes_v2.py."""
import json
import math
import os
import re
import sys
import textwrap
import cairo
import kit
import uz_check as uz
import cs_frame as cf
import fs_storyboard_v17 as sbv
import ps_set as pss
import don_ps as dp
import robot_ps as rp
import sofia_ps as sp
import pm_ps as pm
import client_ps as cps
import dh_props as dhp
from kit import Ctx, INK

pss.MARK_SMALL[0] = True
pss.NO_SCREEN[0] = True
pss.NO_DOOR_CONFETTI[0] = True                              # v4 (24 Nov): no confetti by the door (cold viewers: "blue squiggles?")
rp.SUN_UP[0] = True                                         # v4: the sun with an up-arrow ("more light", not a gear)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "pick-a-side")
SCRIPT = os.path.join(OUT, "pick-a-side-script-v7.md")
TIMING = os.path.join(OUT, "ps_timing_v2.json")
W, H = 540, 960
F = pss.F
SC = dict(don=0.60, sofia=0.56, pam=0.54, mom=0.54, robot=rp.S_OFFICE)
R = dict(don=50, sofia=46, pam=48, mom=50, robot=50)       # head radius in body units (uz_check's faces)


def tape_x(dy):
    """The tape's middle at depth dy below the floor line (it splays toward the camera)."""
    return pss.LINE_X + dy * 28 / 160


# --- where everyone stands (the floor plan v3, world units; feet = F + dy) --------------------------------------------
P = dict(
    don_cord=(64, 0), rob_cord=(186, 4), don_door=(84, 10),
    trio_pam=(520, 40), trio_mom=(592, 34), trio_sof=(662, 44),
    don_mid=(420, 125), pam_don=(490, 55), mom_tape=(tape_x(15) + 4, 15), sof_heel=(tape_x(90) + 10, 90),
    rob_tape=(tape_x(140), 140), rob_side=(470, 140), don_throne=(380, 60), rob_throne=(500, 30),
    don_line=(tape_x(150) - 56, 150), pam_stool=(110, 90), sof_door=(250, 60), sof_far=(650, 60),
    don_front=(330, 160), pam_reach=(tape_x(55) - 30, 55),
)


def at(name):
    x, dy = P[name]
    return x, F + dy


# --- the cast, each drawn by its approved rig; returns its head (x, y, r) in world units -----------------------------
def don(k, where, pose="stand", face="neutral", look=(0, 0), **kw):
    x, f = at(where) if isinstance(where, str) else where
    o = dp.don(k, x, f, SC["don"], pose, face, look, **kw)
    HANDS_LOG.extend(o["hands"])
    return o, (o["head"][0], o["head"][1], R["don"] * SC["don"])


def robot(k, where, **kw):
    x, f = at(where) if isinstance(where, str) else where
    o = rp.robot(k, x, f, SC["robot"], **kw)
    HANDS_LOG.extend(o["hands"])
    sx, sy = o["screen"]
    return o, (sx, sy, R["robot"] * SC["robot"])


def sofia(k, where, pose="stand", face="smile", look=(0, 0), lean=0.0):
    x, f = at(where) if isinstance(where, str) else where
    o = sp.sofia(k, x, f, SC["sofia"], pose, face, look=look, lean=lean)
    return o, (o["head"][0], o["head"][1], R["sofia"] * SC["sofia"])


def pam(k, where, pose="stand", face="neutral", look=(0, 0), **kw):
    x, f = at(where) if isinstance(where, str) else where
    o = pm.pam(k, x, f, SC["pam"], pose, face, look, **kw)
    return o, (o["head"][0], o["head"][1], R["pam"] * SC["pam"])


def mom(k, where, pose="folded", face="unimpressed", look=(0, 0), **kw):
    x, f = at(where) if isinstance(where, str) else where
    o = pm.mom(k, x, f, SC["mom"], pose, face, look, **kw)
    return o, (o["head"][0], o["head"][1], R["mom"] * SC["mom"])


# --- the shots ----------------------------------------------------------------------------------------------------------
def S(id_, cam, room=None, cast=None, draw=None, story=None, fg=None):
    """cam: (fx, fy, z) | [names] (framed by the series' rule on their faces) | "screen" (an insert drawn in frame units).
    room: ps_set.room's state; cast: fn(k) -> {name: head}; draw: fn(k) for an insert; story: the faces checked."""
    return dict(id=id_, cam=cam, room=room or {}, cast=cast, draw=draw, story=story, fg=fg)


S2 = (112, 590, 2.05)                                       # 1.1 / 6.2: the door; v2 raised: the faces above the bottom quarter
ROOM1 = dict(blind="up")
ROOM2 = dict(blind="torn", tape=True)                       # from 2.1: the tape; the throne spun from 2.2
ROOM2S = dict(blind="torn", tape=True, spun=True)
ROOM3 = dict(blind="torn", tape=True, spun=True, silhouette=True)
ROOM5 = dict(blind="rehung", tape=True, spun=True, phone="lit")
ROOM3P = dict(blind="torn", tape=True, spun=True, silhouette="phone")      # v3: 3.6, the guard's phone lit at his face


def _tug_11(k):
    """v4 (Tomas 24 Nov, /grill-me, the third cold test: 0 of 3 saw the robot pull): the board's 1.1 is motion test A's
    key frame: both hands on their cords, the cords taut to the hands, the blind half down, the robot hauling it back up."""
    import acts_ob as ac
    heads, c, n = {}, k.c, 0.45
    top = pss.GY0 - 10 + 12
    x, f = at("don_cord"); x += 26
    hd = (pss.CORD_L + 2, f - 310 * SC["don"] + (150 * SC["don"]) * n)
    to = lambda p: ((p[0] - x) / SC["don"], (p[1] - f) / SC["don"])
    o, heads["don"] = don(k, (x, f), ac._pose(1.12, left=to(hd)), "confused", (-0.4, -0.6))
    rx, rf = at("rob_cord")
    o2, heads["robot"] = robot(k, (rx - 18, rf), arms=((-180, 0), (8, 0)), visor="sun")   # a step left, clear of the door
    #                                     frame; the near arm straight up on the glass, the grip at its tip
    for cx, hand, pull in ((pss.CORD_L, o["hands"][0], pss.PULL), (pss.CORD_R, o2["hands"][0], pss.PULL_R)):
        hx, hy = hand
        c.set_source_rgb(*pss.CORD); c.set_line_width(4.0); c.set_line_cap(1)
        c.move_to(cx, top); c.line_to(hx, hy); c.stroke(); c.set_line_cap(0)
        c.save(); c.translate(hx, hy + 6); c.scale(5, 8); c.new_path(); c.arc(0, 0, 1, 0, 6.3); c.restore()
        c.set_source_rgb(*pull); c.fill_preserve(); c.set_source_rgb(*kit.INK); c.set_line_width(1.4); c.stroke()
    return heads


def light_in(k):
    """v4 (Tomas 24 Nov: the sun icon read as "a sun", never "more light"): when the blind is down, daylight falls
    through the bare glass onto whoever is in front of it: three warm bands, no new words."""
    c = k.c
    x0, y0, w, h = pss.GX0, pss.GY0, pss.GW, pss.GH
    c.save()
    c.rectangle(x0, y0, w, h + 60); c.clip()                 # through the glass and onto the floor in front, not the wall
    for i, (a, b) in enumerate(((0.10, 0.30), (0.42, 0.58), (0.72, 0.92))):
        c.new_path()
        c.move_to(x0 + w * a + 40, y0); c.line_to(x0 + w * b + 40, y0)
        c.line_to(x0 + w * b - 30, y0 + h + 60); c.line_to(x0 + w * a - 30, y0 + h + 60); c.close_path()
        c.set_source_rgba(1.0, 0.90, 0.45, 0.34); c.fill()
    c.restore()


def cast_11(down=False, last=False):
    def f(k):
        if FIX_V4[0] and not down:
            return _tug_11(k)
        heads = {}
        _, heads["don"] = don(k, "don_cord", (-168, 6, 8, 0) if not down else (-150, -20, 8, 0),
                              "squint" if not down else "smug", (-0.4, -0.6))
        arms = ((-8, 0), (172, -4)) if (not down or last) else ((-8, 0), (8, 0))
        _, heads["robot"] = robot(k, "rob_cord", arms=arms, visor="sun" if down else None)
        if down:
            k.c.set_source_rgba(0.05, 0.05, 0.10, 0.30); k.c.rectangle(-400, 0, 1800, 1200); k.c.fill()
        return heads
    return f


def cast_12a(k):
    heads = {}
    o, heads["don"] = don(k, "don_door", "stand", "shock", (0, 0))
    dp.blind_over(k, o["head"], SC["don"])
    if FIX_V4[0]:
        light_in(k)
    _, heads["robot"] = robot(k, (pss.GX0 + 196, F + 4), visor="sun")
    return heads


def cast_trio(cup="cup_mid", pf="frozen"):
    def f(k):
        heads = {}
        _, heads["pam"] = pam(k, "trio_pam", cup, pf, (-1, -0.1))
        _, heads["mom"] = mom(k, "trio_mom", "folded", "unimpressed", (-1, 0))
        _, heads["sofia"] = sofia(k, "trio_sof", "hip_out", "smile", (-1, 0))
        return heads
    return f


def cast_13(k):
    heads = {}
    o, heads["don"] = don(k, "don_door", "stand", "neutral", (0, 0))
    dp.blind_over(k, o["head"], SC["don"])
    return heads


NO_STRIP_14 = [True]
TRIO_DX_14 = [0]                                            # tried 150/220 (review round 1): the frame goes too wide; kept


def cast_14(k):
    heads = {}
    dx_ = 200
    t_ = TRIO_DX_14[0] if FIX_V4[0] else 0             # v4 review round 1: the trio further off, his box between
    _, heads["pam"] = pam(k, (300 + t_, F + 20), "cup_mid", "doubt", (0.6, 0))
    _, heads["mom"] = mom(k, (370 + t_, F + 16), "folded", "unimpressed", (-0.6, 0))
    _, heads["sofia"] = sofia(k, (440 + t_, F + 24), "hip_out", "smile", (-1, 0))
    tmp = cairo.ImageSurface(cairo.FORMAT_RGB24, 4, 4)
    hh = dp.don(Ctx(cairo.Context(tmp), 0), dx_, F + 90, SC["don"], "stand", "neutral", (0, 0))["head"]
    dp.blind_cape(k, hh, SC["don"])
    if FIX_V4[0]:                                            # v4 (Tomas 24 Nov): the roll in his other hand (frame left), so
        p_ = dp.POSES["lift_roll"]                           # his bubble sits on his right with a short tail, clear of it
        o, heads["don"] = don(k, (dx_, F + 90), (-p_[2], -p_[3], -p_[0], -p_[1]), "hollow", (0, 0), hands=("fist", "fist"))
        dp.cape_rail(k, o["head"], SC["don"])
        if not NO_STRIP_14[0]:                               # round 1 fix: the strip between his hands framed his box
            dp.tape_strip(k, o["hands"][0], o["hands"][1], SC["don"])   # like a sign he holds (2 of 3): the roll alone
        dp.tape_roll(k, *o["hands"][0], SC["don"] * 0.9)
        return heads
    o, heads["don"] = don(k, (dx_, F + 90), "lift_roll", "hollow", (0, 0))
    dp.cape_rail(k, o["head"], SC["don"])
    dp.tape_strip(k, o["hands"][1], o["hands"][0], SC["don"])
    dp.tape_roll(k, *o["hands"][1], SC["don"] * 0.9)
    return heads


def cast_scene2(don_pose="point_roll", don_face="confused", don_look=(1, 0), pam_pose="stand", pam_at="pam_don",
                rob=None, sof_pose="stand", don_at="don_mid", chin=1, extra=None, mom_look=(-1, 0)):
    def f(k):
        heads = {}
        order = []
        order.append((P["mom_tape"][1], "mom", lambda: mom(k, "mom_tape", "folded", "unimpressed", mom_look)))
        order.append((P[pam_at][1], "pam", lambda: pam(k, pam_at, pam_pose, "neutral", (-0.6, 0))))
        order.append((P["sof_heel"][1], "sofia", lambda: sofia(k, "sof_heel", sof_pose, "smile", (-1, 0))))
        if rob:
            order.append((P[rob[0]][1], "robot", lambda: robot(k, rob[0], **rob[1])))
        order.append((P[don_at][1], "don", lambda: don(k, don_at, don_pose, don_face, don_look, chin=chin)))
        for _, n, fn in sorted(order, key=lambda t: t[0]):
            o, heads[n] = fn()
            if n == "don" and extra:
                extra(k, o)
        return heads
    return f


def cast_21(k):
    """2.1 (v3, the second cold test: 2 of 3 thought Pam laid the tape): Don in the foreground, the roll in his fist,
    the tape running from it back through the group."""
    heads = cast_trio("stand", "shock")(k)
    x, f = tape_x(175) - 46, F + 175
    o, heads["don"] = don(k, (x, f), (-8, 0, 40, 60), "confused", (1, -0.4), chin=1)
    hx, hy = o["hands"][1]
    c = k.c                                                                  # the strip from the roll down to the floor's line
    for col, w in ((INK, 11), (pss.TAPE, 8)):
        c.set_source_rgb(*col); c.set_line_width(w); c.new_path(); c.move_to(hx, hy)
        c.curve_to(hx + 4, hy + 40, tape_x(175) - 4, f - 20, tape_x(175), f); c.stroke()
    dp.tape_roll(k, hx, hy, SC["don"] * 0.9, ang=0.2)
    return heads


def roll_up(k, o):
    """2.3 (v3): the roll held up and out, not across Pam."""
    dp.tape_roll(k, *o["hands"][1], SC["don"] * 0.9)


def roll_point(k, o):
    dp.tape_roll(k, o["hands"][1][0] + 10, o["hands"][1][1], SC["don"] * 0.9, ang=0.6)


def cast_21b(k):
    heads = {}
    if FIX_V4[0]:                                            # review round 1 (both reviewers: the sign changes with no cause):
        o, heads["robot"] = robot(k, "rob_throne", arms=((-150, -10), (-8, 0)), visor=None)  # the card in its claw,
        hx, hy = o["hands"][0]                              # going onto the throne's side: the act on screen
        pss.robot_card(k, hx + 14, hy - 44, SC["robot"] * 1.3, ang=-0.12)
        c = k.c; c.set_source_rgb(*kit.INK); c.set_line_width(2.6); c.set_line_cap(1)   # SLAP: the card pressed on (cold
        cx_, cy_ = hx + 14, hy - 44                          # test: nobody saw who put it there)
        for ang in (-2.6, -2.1, -1.6, 0.5, 1.0):
            import math as m_
            r0, r1 = 66 * SC["robot"] * 1.3 / 0.66 * 0.66, 84 * SC["robot"] * 1.3 / 0.66 * 0.66
            c.move_to(cx_ + m_.cos(ang) * r0, cy_ + m_.sin(ang) * r0 * 0.7); c.line_to(cx_ + m_.cos(ang) * r1, cy_ + m_.sin(ang) * r1 * 0.7); c.stroke()
        c.set_line_cap(0)     # pressed on the throne's back by its edge
        return heads
    _, heads["robot"] = robot(k, "rob_throne", arms=((-8, 0), (-120, -30)), visor=None)
    return heads


def cast_22(k):
    heads = {}
    _, heads["don"] = don(k, "don_throne", "push", "squint", (-1, -0.3))
    return heads


_cast_24_v3 = cast_scene2("stand", "neutral", (1, 0), chin=0)


def cast_24(k):
    """review round 1 (R1: Pam's choice is a glance): v4 she has just hopped over the tape onto Don's side, her cup held
    level (cup_mid): two landing marks at her shoes. v3 as before."""
    if not FIX_V4[0]:
        return _cast_24_v3(k)
    heads = _cast_scene2_24(k)
    x, f = at("pam_don")
    c = k.c; c.set_source_rgb(*kit.INK); c.set_line_width(2.4); c.set_line_cap(1)
    for sd in (-1, 1):                                       # the landing: short strokes out from her shoes
        c.move_to(x + sd * 26, f + 2); c.line_to(x + sd * 44, f - 6); c.stroke()
        c.move_to(x + sd * 28, f + 10); c.line_to(x + sd * 48, f + 10); c.stroke()
    c.set_line_cap(0)
    return heads


_cast_scene2_24 = cast_scene2("stand", "neutral", (1, 0), pam_pose="cup_mid", chin=0)


def cast_25(k):
    heads = {}
    _, heads["don"] = don(k, (372, F + 62), "salute", "pleased", (0.6, 0), chin=1)          # v2: behind the marker, clear of the card
    _, heads["pam"] = pam(k, (530, F + 56), "half_salute", "quiet", (-0.6, 0))
    return heads


def cast_26(k):
    heads = {}
    _, heads["mom"] = mom(k, "mom_tape", "folded", "unimpressed", (-1, 0), chin=True)
    return heads


def cast_27(k):
    heads = {}
    _, heads["sofia"] = sofia(k, "sof_heel", "stand", "smile", (-1, 0))
    return heads


def cast_29(k):
    heads = {}
    _, heads["robot"] = robot(k, (300, F + 60), visor="barrier")
    return heads


def cast_29b(k):
    heads = {}
    _, heads["sofia"] = sofia(k, "sof_heel", "stand", "smile", (-1, 0))
    return heads


def cast_210(k):
    heads = {}
    _, heads["don"] = don(k, (tape_x(140) - 190, F + 140), "vest", "smug", (-1, 0), chin=1)
    _, heads["robot"] = robot(k, "rob_tape", arms=((-95, 0), (95, 0)), tilt=0.10)
    return heads


def cast_211(k):
    heads = {}
    _, heads["robot"] = robot(k, (tape_x(140) - 10, F + 140), arms=((-95, 0), (95, 0)), tilt=-0.16)
    heads["don"] = dp.bumped(k, tape_x(140) - 150, F + 170, SC["don"])["head"] + (R["don"] * SC["don"],)
    heads["don"] = (heads["don"][0], heads["don"][1], R["don"] * SC["don"])
    return heads


def cast_212(k):
    heads = {}
    _, heads["sofia"] = sofia(k, "sof_heel", "fold", "smile", (-1, 0))
    return heads


def cast_31(k):
    heads = {}
    md = 15
    _, heads["mom"] = mom(k, (tape_x(md) + 4, F + md), "folded", "unimpressed", (-1, 0))
    _, heads["don"] = don(k, (tape_x(140) - 190, F + 140), "thumbs", "grin", (0, -0.3), chin=1)
    _, heads["robot"] = robot(k, "rob_tape", selfie=1.0, arms=((-95, 0), (160, 0)))
    return heads


def cast_33(k):
    heads = {}
    _, heads["robot"] = robot(k, "rob_tape", selfie=0.6, phone="public", visor="public", arms=((-95, 0), (120, 40)))
    return heads


def cast_34(k):
    heads = {}
    _, heads["don"] = don(k, (tape_x(140) - 190, F + 140), "thumbs", "grin", (0, -0.3), chin=1)
    return heads


def cast_36(k):
    heads = {}
    _, heads["don"] = don(k, (300, F + 150), "thumbs", "grin", (0, -0.3), chin=1)
    return heads


def cast_37(k):
    heads = {}
    _, heads["pam"] = pam(k, "pam_don", "cup_chin", "doubt", (-1, 0))
    return heads


LARM_53, CAN_53 = [(-130, -80)], [0.0]
TREAT_53 = (286, 752, 2.05)                                  # GAGS_V5: 5.3b's camera, close on bodyguard 2 and the robot (Pam and the
GUARD_S = 0.56 / 0.52 * 0.60                                 # signs out of frame); the guard at Daddy's Home's scale against Don


def cast_53_treat(k):
    """5.3b (Tomas's picks, 25 Nov): bodyguard 2, one step inside the door, has handed the robot an oil can; it holds it
    up beside its head, a drop on the spout, a heart on its visor. Sofía has gone on to the tape (5.5).
    The robot has rolled 30 px to him from its 5.3a mark. Cold test round 4: the can, the treat and the delight read 2 of 2."""
    import dh_cast as dc
    heads = {}; c = k.c
    og = dc.guard(k, 196, F + 46, GUARD_S, pose=(dc.GUARD_POSE[0], dc.GUARD_POSE[1], 10, 20))   # his giving hand still out
    heads["guard"] = (og["head"][0], og["head"][1], 40 * GUARD_S)
    rxy, arms = (312, F + 50), (LARM_53[0], (20, 10))        # the can in its near hand, raised, over his dark suit: its face clear
    c.push_group(); orb, _ = robot(k, rxy, arms=arms); c.pop_group()
    rh = orb["hands"][0]
    _, heads["robot"] = robot(k, rxy, arms=arms, visor="heart", look=(-1, -0.4))
    cs, ca = 1.15, CAN_53[0]                                    # the can held BY ITS HANDLE: its base placed so the loop handle sits
    hx_, hy_ = rp.CAN_HANDLE[0] * cs, rp.CAN_HANDLE[1] * cs  # on the hand the rig returns, then the same hand again on top (224)
    rp.oil_can(k, rh[0] - (hx_ * math.cos(ca) - hy_ * math.sin(ca)), rh[1] - (hx_ * math.sin(ca) + hy_ * math.cos(ca)), cs, ca)
    rp.hand_again(k, rh[0], rh[1], SC["robot"])
    HANDS_LOG.extend(orb["hands"]); HANDS_LOG.extend(og["hands"])
    return heads


def cast_53(k):
    if GAGS_V5[0] and CAMKEY[0] == TREAT_53:
        return cast_53_treat(k)
    heads = {}
    pm.stool(k, P["pam_stool"][0], F + P["pam_stool"][1], SC["pam"])
    pf = (P["pam_stool"][0], F + P["pam_stool"][1] - 98 * SC["pam"])
    tmp = cairo.ImageSurface(cairo.FORMAT_RGB24, 4, 4)
    hh = pm.pam(Ctx(cairo.Context(tmp), 0), *pf, SC["pam"], "rail", "frozen", (1, -0.1))["hands"]
    pm.blind_rail(k, hh[0], hh[1], SC["pam"])                       # v3: the blind hangs from her rail (not "cheering")
    o, heads["pam"] = pam(k, pf, "rail", "frozen", (1, -0.1), late=False)
    pm.rail_bar(k, o["hands"][0], o["hands"][1], SC["pam"])
    import hands_ps as hp
    hp.redraw_late(k)
    if FIX_V4[0]:                                            # review round 1: who is welcomed? the robot clear of her, she has
        _, heads["robot"] = robot(k, (330, F + 40), arms=((-60, 0), (60, 0)))   # the CV (given in 5.2) in her hand
        o, heads["sofia"] = sofia(k, (215, F + 60), "walk", "smile", (1, 0))
        hx, hy = o["hands"][1]
        sp.cv_coo(k, hx + 6, hy + 10, 0.6)
    else:
        _, heads["robot"] = robot(k, (230, F + 40), arms=((-8, 0), (60, 0)))
        _, heads["sofia"] = sofia(k, "sof_door", "walk", "smile", (-1, 0))
    _, heads["don"] = don(k, "don_line", "stand", "neutral", (1, 0))
    return heads


def cast_54(k):
    heads = {}
    _, heads["don"] = don(k, "don_line", "balance", "neutral", (0.7, 1.0), knee=1.0)
    return heads


def cast_56(k):
    heads = {}
    _, heads["sofia"] = sofia(k, (tape_x(60) + 4, F + 60), "walk", "smile", (1, -0.1))   # v3: astride the tape, stepping over
    return heads


PAM_X_56 = [160]                                            # her own frame (Sofía out): her box clear of the button rail


def fg_56(k):
    """Pam near, on the stool, frozen with the blind; the frame's left, her eyes over to Sofía crossing."""
    s_ = 0.54 * 2.2
    px = PAM_X_56[0] if FIX_V4[0] else 140                   # round 5: Pam in from the edge, the wall on her left for her line
    tmp = cairo.ImageSurface(cairo.FORMAT_RGB24, 4, 4)
    hh = pm.pam(Ctx(cairo.Context(tmp), 0), px, 1060 - 98 * s_, s_, "rail", "frozen", (1, 0.1))["hands"]
    pm.blind_rail(k, hh[0], hh[1], s_)                               # v3: the blind hangs from her rail
    o = pm.pam(k, px, 1060 - 98 * s_, s_, "rail", "frozen", (1, 0.1), late=False)
    pm.rail_bar(k, o["hands"][0], o["hands"][1], s_)
    import hands_ps as hp
    hp.redraw_late(k)
    return {"pam": (o["head"][0], o["head"][1], R["pam"] * s_)}


def cast_57(k):
    heads = {}
    _, heads["sofia"] = sofia(k, (660, F + 40), "stand", "smile", (-1, -0.2))
    return heads


CV_61 = [1.3]
SOF_61 = [712]                                              # review round 1: Sofía right of Pam's phone, the phone seen buzzing


def cast_61(k):
    """behind: Mom on the tape turned away, Pam's reach across it, Sofía past the line with COO?; the throne's card."""
    heads = {}
    _, heads["mom"] = mom(k, "mom_tape", "folded", "stern", (1, -0.6))                      # v3: eyes away, up
    o, heads["sofia"] = sofia(k, (SOF_61[0] if FIX_V4[0] else 640, F + 40), "chest", "smile", (0.2, 0.6))   # v3: eyes on CV
    hx, hy = o["hands"][0]
    if GAGS_V5[0]:                                           # outside review, 25 Nov: the CV 18 % smaller and lower, her face clear
        was = sp.CV_FONT[0]
        if V55[0] == "C":                                    # outside review of A/B/C (P1): the word 12 % bigger here, to read on a phone
            sp.CV_FONT[0] = 25
        sp.cv_coo(k, hx + 4, hy + 40, CV_61[0] * 0.82)
        sp.CV_FONT[0] = was      # on her hand, as board v3 (the hand sheet: lowered, it left the hand)
    else:
        sp.cv_coo(k, hx + 4, hy + (40 if FIX_V4[0] else 4), CV_61[0] if FIX_V4[0] else 0.8)   # at her chest, COO? up; v4 lower
    if FIX_V4[0]:                                            # review round 1 (Tomas: the loop's trigger): Pam's phone on the
        x_, y_ = pss.PHONE_AT                                # counter buzzes behind Don, 5.7's own phone small and upright
        k.c.save(); k.c.translate(x_, y_ - 26); k.c.rotate(-0.08)   # (bare arcs read as "a blue spiral", cold test)
        pss.phone_close(k, 0, 0, 0.34, lit=True, buzz=True)
        k.c.restore()
    o, heads["pam"] = pam(k, (tape_x(55) - 40, F + 55), "reach", "avert", (1, 0.6), mug=False)  # v3: eyes on her lit phone
    if not FIX_V4[0]:                                        # v4 (cold test, 3 fixes, 0 of 3 read a phone in her hand): no phone in
        pss.pam_phone(k, o["hands"][1][0] + 30, o["hands"][1][1] + 10, 1.4, lit=True)   # 6.1; its owner is read in 5.7 (her hand)
    return heads


DON_X_61 = [110]


FACE_61B = ["shock"]
SPRING_61B = [1.0]                                           # motion test I: the spring's height (overshoot), 1.0 = the board


def fg_61b(k):
    """6.1b (Tomas 24 Nov, Office Noir 1's startle as the model: the cat hisses, his eyes go round, the hat jumps): the
    phone behind him buzzes; eyes round and over to it, his one hair sprung straight up (no hat), two jump strokes."""
    s_ = 0.60 * 2.5
    o = dp.don(k, DON_X_61[0], 1150, s_, "vest", FACE_61B[0], (1, -1), chin=0)
    hx, hy = o["head"]
    c = k.c
    import fs_storyboard as fsb
    hs = 1.7 if fsb.SET4[0] else 1.0
    c.save(); c.translate(hx, hy); c.scale(s_, s_)             # the sprung hair, from the curl's root
    c.set_source_rgb(*kit.INK); c.set_line_width(4.6 if fsb.SET4[0] else 2.4); c.set_line_cap(1); c.set_line_join(1)
    c.move_to(2, -50)
    sp_ = SPRING_61B[0]
    for i in range(5):                                     # a spring, straight up
        c.line_to(2 + (6 if i % 2 == 0 else -6) * hs, -50 - (7 + 7 * i) * hs * sp_)
    c.line_to(2, -50 - 42 * hs * sp_); c.stroke()
    for sd in (-1, 1):                                     # the jump: strokes either side of it
        c.move_to(sd * 16 * hs, -50 - 30 * hs * sp_); c.line_to(sd * 26 * hs, -50 - 38 * hs * sp_); c.stroke()
    c.set_line_cap(0); c.set_line_join(0)
    c.restore()
    return {"don": (hx, hy, R["don"] * s_)}


def fg_61(k):
    """Don, near, big, front-left on his side, facing us: drawn in frame units."""
    o = dp.don(k, DON_X_61[0] if FIX_V4[0] else 170, 1150, 0.60 * 2.5, "vest", "smug", (0, 0), chin=1)   # v4: left, the tape seen
    return {"don": (o["head"][0], o["head"][1], R["don"] * 0.60 * 2.5)}


# the inserts, in frame units (540 x 960)
def ins_heel(k):
    k.c.set_source_rgb(*kit.FLOOR); k.c.paint()
    sp.heel(k, 330, 620, 1.3)


def ins_photo(k, flash=True):
    c = k.c
    c.set_source_rgb(0.08, 0.08, 0.09); c.paint()
    ph = rp.team_photo(184, 184)
    c.save(); c.translate(18, 230); c.scale(504 / 184, 504 / 184); c.set_source_surface(ph, 0, 0); c.paint(); c.restore()
    if flash:
        c.set_source_rgba(1, 1, 1, 0.35); c.paint()


def ins_screen(kind):
    def f(k):
        k.c.set_source_rgb(0.20, 0.20, 0.24); k.c.paint()
        rp.phone_screen(k, 270, 500, 2.3, kind)
    return f


def ins_booth_wide(k):
    """4.1: the empty velvet booth under 12's neon motto (dh_props' neon, drawn here without 12's phone and hands)."""
    c = k.c
    c.set_source_rgb(0.10, 0.03, 0.05); c.paint()
    cps.booth_room(k, W, H, 700, 640)
    cps.table(k, W, 640)
    for i, (txt, sz) in enumerate((("THE HOUSE", 34), ("ALWAYS", 48), ("COLLECTS", 48))):
        yy = 170 + i * 58
        c.set_source_rgba(*dhp.NEON, 0.16); c.rectangle(120, yy - 40, 300, 54); c.fill()
        kit.text(k, txt, 270, yy, sz + 2, dhp.NEON)
        kit.text(k, txt, 270, yy, sz, (1.0, 0.86, 0.88))
    if GAGS_V5[0]:                                           # Tomas, 25 Nov (the red room read as "another film" 3 of 3): the
        _post_bridge(k)                                      # #TeamDon post we just saw posted, on bodyguard 1's phone, in his hand


def _post_bridge(k):
    """4.1 bridge: the same #TeamDon screen as 3.5, on the phone the silhouette lifted in 3.6, now in a black-sleeved hand
    under the neon: the office and the booth share one prop (the cold-viewer skill: two places need one visible link)."""
    c = k.c
    import of_cast as ocs
    px, py, ps_ = 270, 560, 1.25
    palm, body_x = (300, 690), 520                           # his right hand from the bottom right (his body off frame, right)
    c.set_source_rgb(0.06, 0.06, 0.08); c.new_path()             # his sleeve
    c.move_to(540, 960); c.line_to(540, 800); c.line_to(330, 700); c.line_to(300, 760); c.line_to(420, 960); c.close_path(); c.fill()
    ocs.phone_grip(k, palm[0], palm[1], 1.4, body_x=body_x, part="back", skin=(0.91, 0.67, 0.55))   # 13's approved phone hand,
    rp.phone_screen(k, px, py, ps_, "posted")                                                         # the big screen between
    ocs.phone_grip(k, palm[0], palm[1], 1.4, body_x=body_x, part="front", skin=(0.91, 0.67, 0.55))
    want = ocs.inner_thumb(palm[0], body_x, False)
    grip("phone", palm, want, want)


HEEL_42 = (330, 470)
FINGER_42 = [1.0]                                            # motion test J: 0 = off the frame's edge, 1 = on her heel                                        # where Sofía's heel lands in the pushed-in photo (frame px)


def ins_prints(k):
    c = k.c
    c.set_source_rgb(0.10, 0.05, 0.06); c.paint()
    if FIX_V4[0]:
        return _prints_v4(k)
    rp.phone_screen(k, 270, 520, 2.3, "posted")
    for (x, y) in ((270, 452), (324, 548)):                 # the oily fingertip: a print on Pam, then one on the heel
        c.save(); c.translate(x, y); c.rotate(0.3); c.scale(14, 19)
        c.set_source_rgba(0.08, 0.05, 0.03, 0.55); c.arc(0, 0, 1, 0, 6.3); c.fill(); c.restore()
        c.set_source_rgba(0.02, 0.01, 0.0, 0.5); c.set_line_width(1.2)
        for r_ in (5, 9, 13):
            c.new_path(); c.save(); c.translate(x, y); c.rotate(0.3); c.scale(r_ / 13 * 1.0, r_ / 13 * 1.35)
            c.arc(0, 0, 10, 0.3, 5.9); c.restore(); c.stroke()


def _prints_v4(k):
    """review round 1 (both reviewers, Tomas's pick): not 3.5's post again but the push-in: the posted photo big, the
    Client's dirty fingertip landing on Sofía's heel over the tape: "That one." is chosen on screen. Lessons 753, 911, 925:
    the hand + a wrist stub only, from the frame's top-right edge, his oily print on the heel."""
    import of_scenes as ofs
    import hands_ps as hp
    import client_ob as cob
    c = k.c
    s_ = 7.0                                                 # the phone's own heel point: (22.3, 13.6) in its units
    px, py = HEEL_42[0] - 22.3 * s_ - 100, HEEL_42[1] - 13.6 * s_ + 46   # measured: her heel sits 100 px right, 46 up
    import ps_checks as pc
    pc.NO_DECLARE[0] = True                                  # the screen fills the frame: the story rect is the heel + finger
    try:
        rp.phone_screen(k, px, py, s_, "posted")
    finally:
        pc.NO_DECLARE[0] = False
    hx, hy = HEEL_42
    pc.protect(c, "the heel under his finger", hx - 70, hy - 110, hx + 90, hy + 120)                                         # his oily print, then the finger on it
    if FINGER_42[0] >= 1.0:                                  # the print only once the finger has landed
        c.save(); c.translate(hx + 4, hy + 6); c.rotate(0.3); c.scale(16, 21)
        c.set_source_rgba(0.08, 0.05, 0.03, 0.45); c.arc(0, 0, 1, 0, 6.3); c.fill(); c.restore()
    w = 84
    d = (-0.55, -0.83)                                       # up-left from below the photo: the finger, not his hand, over her
    back = (1.0 - FINGER_42[0]) * 320                        # motion: it comes in along its own line from the edge
    wx, wy = hx - d[0] * (1.35 * w + back), hy - d[1] * (1.35 * w + back)
    ofs.insert_cuff(c, (wx, wy), (wx - d[0] * 60, wy - d[1] * 60), w, cob.SKIN, (0.95, 0.94, 0.90), cuff=(0.95, 0.94, 0.90))
    hp.draw(k, "point", wx, wy, w, cob.SKIN, d, 1)
    grip("point", (wx, wy))
    c.set_source_rgba(0.12, 0.07, 0.03, 0.75)               # grease on the knuckles and under the nail (his hands, canon)
    for (ox, oy, r) in ((-6, 8, 9), (10, -4, 7)):
        c.new_path(); c.arc(wx + ox, wy + oy, r, 0, 6.3); c.fill()
    tx_, ty_ = wx + d[0] * 1.22 * w, wy + d[1] * 1.22 * w
    c.new_path(); c.arc(tx_, ty_, 5, 0, 6.3); c.fill()


CLOSE_43 = [1.45, -345, -302]                                  # GAGS_V5: 4.3b, the bodyguards close (x' = s x + tx)
BOOTH_PART_V4 = {0: (1.25, -230, -220), 1: (1.25, 100, -220), 2: (CLOSE_43[0], CLOSE_43[1], CLOSE_43[2])}   # round 5: 4.3a on the Client, 4.3b on Father (x' = s x + tx)


def ins_booth_43(k):
    c = k.c
    c.set_source_rgb(0.10, 0.03, 0.05); c.paint()
    t = BOOTH_PART_V4.get(PART[0]) if FIX_V4[0] else None
    if t is None:
        return _booth_43(k)
    s_, tx, ty = t                                           # one speaker per key frame, the other off the edge: the box's wall
    c.save(); c.translate(tx, ty); c.scale(s_, s_)           # is clear (3 of 3 cold viewers guessed who said each line)
    h = _booth_43(k)
    c.restore()
    return {n: (x * s_ + tx, y * s_ + ty, r * s_) for n, (x, y, r) in h.items() if -40 < x * s_ + tx < W + 40}


def _booth_guards(k, seat, tbl):
    """4.3 (Tomas's picks, 25 Nov): Father's two bodyguards stand behind the bench either side of the oily Client; as he
    leans in they turn away, mirrored, and pinch their noses; three green stink lines rise off him (ep 9: he smells of gas
    and oil). Upright they read as "holding a hostage" (2 of 2); pinching, with the lines, as the smell (2 of 2)."""
    import dh_cast as dc
    import hands_ps as hp
    c = k.c
    heads = {}
    gs = 0.95
    for i, gx in enumerate((300, 548)):
        sgn, flip = (-1, False) if i == 0 else (1, True)
        c.save(); c.rectangle(-200, -200, 1400, tbl + 200); c.clip()          # behind the bench: nothing of them under the table
        c.translate(gx, tbl); c.rotate(sgn * 0.13); c.translate(-gx, -tbl)
        dc.ARM_FRONT[0] = 1                                  # the pinching arm is HIS OWN, drawn after his head (dh_cast, opt-in):
        try:                                                 # one hand per wrist (179, 208). A second hand drawn on top of the
            o = dc.guard(k, gx, seat + 10, gs, pose=(dc.GUARD_POSE[0], dc.GUARD_POSE[1], -100, -60), flip=flip)
        finally:                                             # rig's hidden one failed hand_gate ("two at one wrist", 4.5 px apart)
            dc.ARM_FRONT[0] = None
        HANDS_LOG.extend(o["hands"])
        if PLANT_HAND[0]:                                    # the gate's planted fault: a foreign hand on the rig's hand
            nose = min(o["hands"], key=lambda h: h[1])
            hp.draw(k, "fist", nose[0] + 3, nose[1] + 3, 30 * gs, (0.91, 0.67, 0.55), (0.7, -0.7), 1)
            grip("pinch", (nose[0] + 3, nose[1] + 3))
        c.restore()
        a = sgn * 0.13                                       # his head where the lean put it (for the bubbles to keep off)
        dx, dy = o["head"][0] - gx, o["head"][1] - tbl
        heads["guard%d" % (i + 1)] = (gx + dx * math.cos(a) - dy * math.sin(a), tbl + dx * math.sin(a) + dy * math.cos(a), 44 * gs)
    for j, x in enumerate((352, 424, 496)):
        y = seat - 400 - 18 * (j % 2)
        for col, lw in (((0.10, 0.16, 0.05), 11), ((0.56, 0.78, 0.22), 6)):
            c.set_source_rgb(*col); c.set_line_width(lw); c.set_line_cap(1); c.new_path(); c.move_to(x, y + 110)
            c.curve_to(x - 30, y + 80, x + 30, y + 60, x, y + 36); c.curve_to(x - 26, y + 18, x + 20, y + 8, x, y - 10); c.stroke()
    c.set_line_cap(0)
    return heads


def _booth_43(k):
    import dh_cast as dc
    c = k.c
    seat, tbl = 760, 700
    cps.booth_room(k, W, H, seat, tbl)
    guards = _booth_guards(k, seat, tbl) if GAGS_V5[0] else {}
    cps.handprint(k, 430, seat - 150, 1.6, 0.2)
    cps.phone_on_table(k, 230, tbl - 90, 1.2, prints=True)
    fs_ = 0.62 / 0.52 * 1.15
    of = dc.father(k, 110, seat + 170, fs_, face="hard", look=(0.6, 0.5))
    import client_on3 as co
    cx, s = (424 if FIX_V4[0] else 400), 1.15                    # v4: 24 px right, room for his bubble beside his hand
    if FIX_V4[0] and PART[0] == 1:                           # round 1 fix: 4.3b is Father's line; the Client's pointing arm at
        tg = [(cx - 40, tbl - 6), (cx + 40, tbl - 6)]        # the frame's edge made the speaker a guess: his hands down here
        oc_ = cps.cast_client(k, cx, seat - co.HIP * s, s, look=(-1.2, 1.4), targets=tg, clip_hip=True)
    else:
        oc_ = cps.cast_client(k, cx, seat - co.HIP * s, s, look=(-1.2, 1.4), targets=[(265, tbl - 128), (cx + 40, tbl - 6)],
                              clip_hip=True, hands={-1: "point"}, aim=(230, tbl - 122))
    cps.table(k, W, tbl)
    return dict({"father": of["head"] + (50 * fs_,), "client": oc_["head"] + (56 * s,)}, **guards)


def ins_cv(hand=False):
    """5.2 (v3): the CV in the guard's dark sleeve, his hand with the gold pen at the ?: whose hand writes is seen."""
    def f(k):
        import hands_ps as hp
        c = k.c
        c.set_source_rgb(0.80, 0.86, 0.90); c.paint()
        sp.cv_coo(k, 250, 540, 3.0)
        low = GAGS_V5[0] and sp.CV_AT[0] == "bottom"           # "C": he writes at the sheet's foot: hand, pen and sleeve 270 px down
        c.save()
        if low:
            c.translate(*PEN_C[0])
        c.set_source_rgb(0.08, 0.08, 0.10); c.new_path()                      # his sleeve, from the right
        c.move_to(560, 330); c.line_to(560, 470); c.line_to(420, 440); c.line_to(410, 380); c.close_path(); c.fill()
        c.set_source_rgb(0.97, 0.97, 0.95); c.rectangle(398, 372, 22, 74); c.fill()   # the cuff
        c.save(); c.translate(372, 420); c.rotate(-0.9)
        if GAGS_V5[0]:                                       # outside review: "is the hand holding the paper?" a real pen: long,
            c.set_source_rgb(*INK); c.rectangle(-8, -128, 16, 140); c.fill()               # outlined, a dark nib on the ?
            c.set_source_rgb(*sp.HEEL_GOLD); c.rectangle(-5.5, -125.5, 11, 135); c.fill()
            c.set_source_rgb(*INK); c.move_to(-8, -128); c.line_to(0, -150); c.line_to(8, -128); c.close_path(); c.fill()
        else:
            c.set_source_rgb(*sp.HEEL_GOLD); c.rectangle(-4, -70, 8, 76); c.fill()
        c.restore()                                          # the gold pen
        hp.draw(k, "fist", 392, 410, 70, (0.80, 0.62, 0.50), (-1.0, 0.1), -1)
        c.restore()
        grip("pen", (392 + (PEN_C[0][0] if low else 0), 410 + (PEN_C[0][1] if low else 0)))
    return f


V55 = [None]                                                 # 25 Nov, HR? over her mouth in 5.5: "A" the word smaller in 5.5,
                                                             # "B" her CV hand lower (pose chest_low), "C" the word at the sheet's foot
STEP_55 = [1.0, "chest", 0.0, 0.0, 0.0]                      # motion test K: progress onto the tape, her pose, extra x and y, lean
                                                             # (a planted-foot gait; the legs via sofia_ss.LEGS, set by ps_motion)


def cast_55(k):
    """5.5 (v3): at the door, Sofía takes the CV, COO? up beside her face."""
    heads = {}
    if FIX_V4[0]:                                            # review round 1 (R1's top 2): her choice is a step: astride the
        pose_ = "chest_low" if GAGS_V5[0] and V55[0] == "B" and STEP_55[1] == "chest" else STEP_55[1]
        o, heads["sofia"] = sofia(k, (tape_x(60) + 4 - (1.0 - STEP_55[0]) * 60 + STEP_55[2], F + 60 + STEP_55[3]),
                                  pose_, "smile", (-1, -0.2), lean=STEP_55[4])   # astride the tape, the CV at her chest
        hx, hy = o["hands"][0]                              # in the hand the pose returns (lesson 655), as in 6.1
        if GAGS_V5[0]:                                       # outside review, 25 Nov: smaller and lower, her face clear
            was = sp.CV_FONT[0]
            if V55[0] == "A":                                # 5.5 only: the word at COO?'s old size, her mouth clear
                sp.CV_FONT[0] = 15
            sp.cv_coo(k, hx + 4, hy + 10, 0.75)             # on her hand (the hand sheet: 28 px lower, it hung beside the hand)
            sp.CV_FONT[0] = was
        else:
            sp.cv_coo(k, hx + 4, hy + 6, 0.9)
        return heads
    o, heads["sofia"] = sofia(k, (290, F + 60), "press", "smile", (-0.6, -0.3))
    hx, hy = o["hands"][0]
    sp.cv_coo(k, hx - 30, hy - 6, 1.1)                                      # in her outstretched hand, toward the door
    return heads


HOLD_57 = [True]


def ins_phone_57(k):
    k.c.set_source_rgb(0.55, 0.48, 0.40); k.c.paint()
    if FIX_V4[0]:                                            # v4 (cold test: "Don's phone?" 2 of 3): beside it, Pam's blue mug
        pss.phone_close(k, 230, 520, 1.8)
        k.c.save(); k.c.translate(430, 600); k.c.scale(2.4, 2.4)           # its handle joined to the body (mug_at hides
        k.c.set_source_rgb(*INK); k.c.set_line_width(4); k.c.new_path(); k.c.arc(-18, 0, 10, 1.57, 4.71); k.c.stroke()
        k.c.restore()                                                      # the gap behind her fingers)
        pm.mug_at(k, 430, 600, 2.4)
        import hands_ps as hp_, pam_mf as pmf_              # v4 (Tomas 24 Nov, hands page): the owner in the frame: Pam's cardigan
        c = k.c; ex, ey, hx, hy = 575, 1000, 350, 690        # sleeve in from the corner, her fingertip on the phone's edge, below
        d = ((hx - ex) / math.hypot(hx - ex, hy - ey), (hy - ey) / math.hypot(hx - ex, hy - ey))   # the words
        for col, lw in ((INK, 118), (pmf_.PURPLE, 110)):
            c.set_source_rgb(*col); c.set_line_width(lw); c.set_line_cap(0); c.move_to(ex, ey); c.line_to(hx - d[0] * 20, hy - d[1] * 20); c.stroke()
        hp_.draw(k, "grab" if HOLD_57[0] else "point", hx, hy, 66, pmf_.SKIN, d, 1)   # round 1 fix: a tap read as
        return                                               # her SENDING it (2 of 3); a grip round its edge receives it
    pss.phone_close(k, 270, 520, 1.8)


SHOTS = [
    S("1.1", S2, ROOM1, cast_11()),
    S("1.2a", (pss.GX0 + 110, 560, 1.7), dict(blind="torn"), cast_12a),
    S("1.2b", ["pam", "mom", "sofia"], dict(blind="torn", phone="dark"), cast_trio()),
    S("1.3", ["don"], dict(blind="torn"), cast_13),
    S("1.4", ["don", "pam", "mom", "sofia"], dict(blind="torn", phone="dark"), cast_14),
    S("2.1", (520, 820, 1.0), dict(ROOM2, mark=False), cast_21),
    S("2.1b", ["robot"], ROOM2, cast_21b),
    S("2.2", ["don"], ROOM2S, cast_22),
    S("2.3", ["don"], ROOM2S, cast_scene2(don_pose="lift_roll", extra=roll_up), story=["don"]),
    S("2.4", ["don", "pam"], ROOM2S, cast_24),
    S("2.5", ["don", "pam"], ROOM2S, cast_25),
    S("2.6", ["mom"], ROOM2S, cast_26),
    S("2.7", ["sofia"], ROOM2S, cast_27),
    S("2.8", "screen", draw=ins_heel),
    S("2.9", ["robot"], ROOM2S, cast_29),
    S("2.9b", ["sofia"], ROOM2S, cast_29b),
    S("2.10", ["don", "robot"], ROOM2S, cast_210),
    S("2.11", ["don", "robot"], ROOM2S, cast_211),
    # 2.12 cut (review round 1, both reviewers: a third copy of 2.7 / 2.9b's framing; Tomas's pick)
    S("3.1", ["don", "robot", "mom"], ROOM3, cast_31),
    S("3.2", "screen", draw=ins_photo),
    S("3.3", ["robot"], ROOM3, cast_33),
    S("3.4", ["don"], ROOM3, cast_34),
    S("3.5", "screen", draw=ins_screen("posted")),
    S("3.6", (220, 600, 1.05), ROOM3P, cast_36),
    S("3.7", ["pam"], ROOM3, cast_37),
    S("4.1", "screen", draw=ins_booth_wide),
    S("4.2", "screen", draw=ins_prints),
    S("4.3", "screen", draw=ins_booth_43),
    S("5.1", (100, 560, 1.8), dict(blind="torn", tape=True, spun=True, silhouette=True), lambda k: {}),
    S("5.2", "screen", draw=ins_cv()),
    S("5.3", ["pam", "robot", "sofia"], dict(blind="rehung", tape=True, spun=True), cast_53),
    S("5.4", ["don"], ROOM5, cast_54),
    S("5.5", ["sofia"], ROOM5, cast_55),
    S("5.6", (tape_x(60) - 90, F - 150, 1.7), ROOM5, cast_56, fg=fg_56, story=["pam", "sofia"]),
    S("5.7", "screen", draw=ins_phone_57),
    S("6.1", (580, F - 170, 1.30), ROOM5, cast_61, fg=fg_61, story=["don", "sofia"]),
    S("6.1b", (580, F - 170, 1.30), ROOM5, cast_61, fg=fg_61b, story=["don"]),   # review round 1: the loop's cause
    S("6.2", S2, dict(blind="rehung"), cast_11(down=False, last=True)),
]
SCENE_OF = lambda sid: int(sid.split(".")[0])
SHRED_OK = "the shredder's SHRED behind the throne or the cast reads as part of a label, no other word (fs_set4's prop)"
# v4: the drawing map (lesson 109): the shots restaged in v3/v4, and the function that must draw them (ps_checks.check_map)
EXPECT = {"2.1": "cast_21", "2.5": "cast_25", "2.10": "cast_210", "2.11": "cast_211", "3.1": "cast_31", "3.4": "cast_34",
          "5.5": "cast_55", "6.1": "cast_61"}

KNOWN = {(sid, "SIGN partly covered: 'SHRED'"): SHRED_OK for sid in
         ("1.2b", "2.1", "2.1b", "2.3", "2.4", "2.5", "2.11", "3.1", "3.4", "3.7", "5.4")}   # (shot, check) -> why it is allowed
KNOWN[("5.4", "SIGN partly covered: 'DON'")] = ("the gag: his raised shoe hovers over his own name on the line for 0.6 s; "
                                                 "the name is whole before and after the lift")
SHIFT = {"1.2b": (120, 0, 1.1), "1.4": (-40, 0, 0.9), "2.1": (0, 0, 1.0), "2.2": (-160, 0, 0.9), "2.3": (0, 0, 0.8),
         "2.4": (0, 0, 0.9), "2.5": (0, 0, 0.9), "2.6": (-20, 30, 1.1), "2.7": (140, 0, 0.8), "2.9b": (140, 0, 0.8),
         "2.12": (140, 0, 0.8), "3.1": (0, 0, 0.9), "3.3": (120, 0, 0.9), "3.4": (-40, 0, 0.8), "3.6": (-60, 0, 0.9), "3.7": (0, 0, 0.9), "5.1": (0, 20, 1.0),
         "5.4": (25, 0, 1.0), "5.5": (110, 0, 0.9), "6.1": (0, 0, 0.9)}   # v2: off the signs


# --- render and check ---------------------------------------------------------------------------------------------------
# v4 (opt-in, FIX_V4: the board v3 and `check`; the layout sheets v3 stay as approved): the faults the series' checks found
GAGS_V5 = [False]                                            # opt-in (25 Nov, Tomas's picks + the outside review of the stills):
                                                             # HR? in place of COO? (sofia_ps.CV_WORD), the CV smaller and lower
GRIPS_LOG, HANDS_LOG, PLANT_HAND = [], [], [False]         # the hand gate (25 Nov): hands drawn outside a rig (a grip, an insert's
                                                             # hand) and the rig hands of the frame, in the drawing's own units


def grip(kind, at_, thumb=None, want=None):
    """Declare a hand drawn outside a rig. hand_gate fails it when a rig's hand lies under it (two hands at one wrist)."""
    GRIPS_LOG.append(dict(kind=kind, at=tuple(at_), thumb=thumb, want=want))


def hand_checks():
    import hand_gate
    return hand_gate.check(GRIPS_LOG, HANDS_LOG, 16.0)


def hands_validate():
    """The gate on a known failure first: 4.3 with a foreign hand planted on the guard's own must fail; 4.3 as drawn must pass."""
    import cairo as _c
    was = (FIX_V4[0], GAGS_V5[0], sp.CV_WORD[0])
    gags_v5()
    res = []
    for plant in (True, False):
        PLANT_HAND[0] = plant; del GRIPS_LOG[:]; del HANDS_LOG[:]
        try:
            PART[0] = 0
            _booth_43(Ctx(_c.Context(_c.ImageSurface(_c.FORMAT_RGB24, W, H)), 0))
        finally:
            PART[0] = None; PLANT_HAND[0] = False
        res.append(hand_checks())
    FIX_V4[0], GAGS_V5[0], sp.CV_WORD[0] = was
    del GRIPS_LOG[:]; del HANDS_LOG[:]
    ok = bool(res[0]) and not res[1]
    print("hands   %s | planted: %s | real: %s" % ("OK " if ok else "BAD", (res[0][:1] or ["(nothing caught)"])[0][:80], res[1][:1] or "pass"))
    return ok


PEN_C = [(30, 300)]                                          # "C": the hand, pen and sleeve at the sheet's foot; the nib just
                                                             # under the ? (outside review P0: not over it)


def v55(v):
    """Pick the 5.5 fix: A, B or C (see V55)."""
    V55[0] = v
    sp.CV_AT[0] = "bottom" if v == "C" else "top"
    p_ = sp.sbc.POSES["chest"]
    sp.sbc.POSES["chest_low"] = (p_[0], 100, p_[2], p_[3])   # her CV hand's forearm lowered (the stills: mouth clear at 100)


def gags_v5(on=True):
    """Board v4: FIX_V4 plus Tomas's picks of 25 Nov (HR? on the CV, the treat, the bodyguards, the CV smaller)."""
    FIX_V4[0] = on or FIX_V4[0]; GAGS_V5[0] = on; sp.CV_WORD[0] = "HR?" if on else "COO?"
    v55("C" if on else None)                                 # Tomas, 25 Nov (after an outside review of A/B/C): C, HR? at the foot


FIX_V4 = [False]
SHIFT_V4 = {"2.5": (40, 0, 0.72), "2.10": (80, 0, 0.8), "6.1": (-216, -210, 1.33), "6.1b": (-216, -210, 1.33), "5.6": (480, -40, 1.0), "2.6": (-45, -90, 1.0), "5.5": (0, -40, 1.15), "5.3": (60, 0, 1.1)}   # round 1: grid-searched, no cut sign   # 2.6: her feet on the tape in frame   # 6.1: review round 1 (Sofía and COO? big, the phone buzzing; grid-searched)   # 5.6: round 5, Sofía out of Pam's key frame (Tomas: the frame Pam's only)   # wall beside the speaker for bc_sb's bubble (lesson 358)
SPLIT_V4 = ("3.1", "4.3", "2.10")   # 2.10: review round 1, "BOTH." on its own frame, the robot big, arms across the tape       # two lines said in turn (3.1 the robot, then Mom; 4.3 the Client, then Father) whose bubbles
PART = [None]                    # can't both sit beside their faces
PART_SHIFT_V4 = {("3.1", 0): (-230, -175, 1.9), ("2.10", 1): (-380, -100, 1.4)}   # 2.10b: the robot on the tape, arms across             # (dx, dy, zoom) per split key frame: 3.1a in on the robot,
#                                                             its line over its antenna, Mom above it (round 5; grid-searched): the board shows one key frame per line


def board_keys(sh, line):
    """-> [(label, surface, faults)]: one key frame, or one per line for a split shot."""
    if FIX_V4[0] and sh["id"] in SPLIT_V4:
        out = []
        parts = list(range(len(says(line))))
        if GAGS_V5[0] and sh["id"] == "4.3":                  # Tomas, 25 Nov (the noses read 1 of 3 at board size): a close on the
            parts = [0, 2, 1]                                 # two bodyguards between the Client's line and Father's, no line
        for i, part in enumerate(parts):
            PART[0] = part
            try:
                surf, msgs = board_frame(sh, line)
                out.append((sh["id"] + "abcd"[i], surf, msgs + (_CHK[0]() if _CHK[0] else [])))
            finally:
                PART[0] = None
        return out
    if FIX_V4[0] and (sh["id"] in KEYS_V4 or (GAGS_V5[0] and sh["id"] in KEYS_V5)):
        out = []
        for i, cam_ in enumerate(KEYS_V5[sh["id"]] if GAGS_V5[0] and sh["id"] in KEYS_V5 else KEYS_V4[sh["id"]]):
            CAMKEY[0] = cam_
            try:
                surf, msgs = board_frame(sh, line)
                out.append((sh["id"] + "abcd"[i], surf, msgs + (_CHK[0]() if _CHK[0] else [])))
            finally:
                CAMKEY[0] = None
        return out
    surf, msgs = board_frame(sh, line)
    return [(sh["id"], surf, msgs + (_CHK[0]() if _CHK[0] else []))]


_CHK = [None]                                               # check_all's per-frame checks (run right after each key frame)
DEBUG_V4, WHY = [False], [""]                                               # board key frames that show one of the shot's lines each
IN_HAND_V4 = ()                                             # review round 1: 6.1 keeps the counter phone (lit, buzzing)
ROOM_V4 = {"1.1": dict(blind="down", u=0.45 * 0.92, dim=False, cords=False)}
ROOM_V4["6.2"] = ROOM_V4["1.1"]                              # review round 1: the loop's last frame IS frame 0 (lessons 257, 659)   # 1.1: the tug's key frame (cords to hands)
CAM_V4 = {}
KEYS_V4 = {"5.4": [(700, 700, 0.8), None]}                  # Tomas 24 Nov: 5.4a wide (his door, DON · CEO, across the tape),
KEYS_V5 = {"5.3": [None, TREAT_53]}                         # GAGS_V5: 5.3a the door as it was, 5.3b the treat
CAMKEY = [None]                                             # 5.4b the medium (the foot over the line); the camera pushes in
KNOWN_V4 = {}                                               # 1.4's exception lifted: the roll moved to his other hand
DARK_V4 = ("5.4", "5.5", "5.6")                             # Pam's phone dark until 5.7 (the continuity row; ROOM5 had it lit)
INS_UP = {"3.5": 34, "4.2": 54, "5.7": 12}                 # the phone inserts: the phone's bottom edge out of the bottom quarter
LAST = [{}]                                                 # the last render's faces in frame units (for the board)
_last_cam = [None]                                          # the last render's camera (the motion tests hold one camera)


class TextRec(cairo.Context):
    """keeps every text shown (in device units) for uz_check.check_signs."""
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


def _floor_on(c, room):
    """v2/v3: the floor (set_ob's colour) and the tape run on below the world's edge (y 960), for the low shots."""
    c.set_source_rgb(0.72, 0.63, 0.50); c.rectangle(-2000, F, 5000, 3000); c.fill()
    c.set_source_rgb(*kit.WALL); c.rectangle(-2000, -2000, 5000, 2000 + F); c.fill()
    if room.get("tape"):
        x0 = pss.LINE_X
        def at(y):
            return x0 + 34 * (y - F) / 160, 8.5 + 11.5 * (y - F) / 160
        (ca, ha), (cb_, hb) = at(958), at(1600)
        c.new_path(); c.move_to(ca - ha, 958); c.line_to(ca + ha, 958); c.line_to(cb_ + hb, 1600); c.line_to(cb_ - hb, 1600)
        c.close_path(); c.set_source_rgb(*pss.TAPE); c.fill_preserve(); c.set_source_rgb(0.30, 0.22, 0.02); c.set_line_width(2.4)
        c.stroke()


def _pass(k, sh, cam):
    c = k.c
    c.save()
    if cam:
        sbv.view(c, *cam)
    room_ = ROOM_V4.get(sh["id"], sh["room"]) if FIX_V4[0] else sh["room"]
    _floor_on(c, room_)
    pss.room(k, **dict(dict(phone=None), **room_))
    heads = sh["cast"](k) if sh["cast"] else {}
    c.restore()
    return heads


def render(sh):
    """-> (surface 540x960, the faults)."""
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    c = TextRec(surf); k = Ctx(c, 0)
    c.set_source_rgb(*kit.WALL); c.paint()
    pss.GUARD_CUES[0] = pss.PLATE_BIG[0] = pss.TAG_OFF[0] = FIX_V4[0]; rp.HEART[0] = FIX_V4[0]          # v4's set cues travel with the v4 staging
    if sh["cam"] == "screen":
        if FIX_V4[0] and sh["id"] in INS_UP:
            c.set_source_rgb(*kit.WALL); c.paint(); c.translate(0, -INS_UP[sh["id"]])
        h = sh["draw"](k) or {}
        LAST[0] = {n: tuple(v) for n, v in h.items()}
        return surf, []
    cam = sh["cam"]
    if GAGS_V5[0] and CAMKEY[0] is not None:                 # a key frame with its own cast (5.3b): no faces to frame by
        cam = CAMKEY[0]
    if isinstance(cam, list):
        tmp = cairo.ImageSurface(cairo.FORMAT_RGB24, 4, 4)
        h0 = _pass(Ctx(cairo.Context(tmp), 0), sh, None)
        cam = cf.face_cam([h0[n] for n in cam])
    shift = SHIFT_V4 if FIX_V4[0] and sh["id"] in SHIFT_V4 else SHIFT
    if FIX_V4[0] and (sh["id"], PART[0]) in PART_SHIFT_V4:   # round 5: one split key frame's own framing (lesson 358)
        shift = {sh["id"]: PART_SHIFT_V4[(sh["id"], PART[0])]}
    if sh["id"] in shift and not NO_SHIFT[0]:                 # the content moved (frame px) / zoomed, off the signs
        dx, dy, zm = shift[sh["id"]]
        z = cam[2] * zm
        cam = (cam[0] - dx / z, cam[1] - dy / z, z)
    _last_cam[0] = cam
    if FIX_V4[0] and sh["id"] in DARK_V4:
        sh = dict(sh, room=dict(sh["room"], phone="dark"))
    if FIX_V4[0] and CAMKEY[0] is not None:                  # v4: a key frame's own camera (KEYS_V4)
        cam = CAMKEY[0]; _last_cam[0] = cam
    if FIX_V4[0] and sh["id"] in IN_HAND_V4:                 # one phone: in her hand, so not on the counter as well
        sh = dict(sh, room=dict(sh["room"], phone=None))
    heads = _pass(k, sh, cam)
    fx, fy, z = cam
    if sh["fg"]:                                              # the near layer, in frame units; its heads back to world units
        for n, (x, y, r) in sh["fg"](k).items():
            heads[n] = ((x - 270) / z + fx, (y - 480) / z + fy, r / z)
    text = []
    for t in c.texts:
        b = t["bbox"]
        text.append(dict(text=t["text"], bbox=((b[0] - 270) / z + fx, (b[1] - 480) / z + fy, (b[2] - 270) / z + fx,
                                               (b[3] - 480) / z + fy), clip=t["clip"]))
    f = dict(cam=cam, heads=heads, scene=dict(text=text), bubbles=[], shot=sh["id"])
    LAST[0] = uz.faces(f)
    SIGNS_V4[:] = [t["bbox"] for t in c.texts if t["bbox"][3] - t["bbox"][1] >= 9]
    msgs = uz.check_signs(f) + uz.check_scale(f, sh["story"]) + covered(sh, cam, surf, c.texts)
    msgs = [m for m in msgs if (sh["id"], m.split(" at ")[0].split(" (")[0]) not in KNOWN]
    return surf, msgs


def covered(sh, cam, surf, texts):
    """v2 (lesson 295): a sign partly hidden by someone standing in front of it reads as another word ("ON" for DON).
    The same frame without the cast: a sign whose pixels differ over 10-88 % of its box is partly covered (a third of DON hidden reads ON)."""
    import numpy as np
    bare = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    cb = TextRec(bare); kb = Ctx(cb, 0); cb.set_source_rgb(*kit.WALL); cb.paint()
    cb.save(); sbv.view(cb, *cam)
    room_ = ROOM_V4.get(sh["id"], sh["room"]) if FIX_V4[0] else sh["room"]
    _floor_on(cb, room_)
    pss.room(kb, **dict(dict(phone=None), **room_)); cb.restore()
    surf.flush(); bare.flush()
    A = np.ndarray((H, W, 4), np.uint8, surf.get_data()).astype(int)
    B = np.ndarray((H, W, 4), np.uint8, bare.get_data()).astype(int)
    out = []
    room_texts = [(b["text"], tuple(round(v) for v in b["bbox"])) for b in cb.texts]
    for t in texts:                                           # only the set's own signs (not badges on the cast)
        if (t["text"], tuple(round(v) for v in t["bbox"])) not in room_texts:
            continue
        x0, y0, x1, y1 = [int(round(v)) for v in t["bbox"]]
        x0, y0, x1, y1 = max(0, x0), max(0, y0), min(W, x1), min(H, y1)
        if x1 - x0 < 4 or y1 - y0 < 3:
            continue
        d = (np.abs(A[y0:y1, x0:x1] - B[y0:y1, x0:x1])[..., :3].max(axis=2) > 24).mean()
        if 0.10 < d < 0.88:
            out.append("SIGN partly covered: %r (%d %%)" % (t["text"], round(100 * d)))
    return out


def _zones(c):
    c.set_source_rgb(0.85, 0.1, 0.1); c.set_line_width(1.5); c.set_dash([6, 4])
    c.move_to(0, cf.BOTTOM); c.line_to(W, cf.BOTTOM); c.stroke()
    c.rectangle(cf.RAIL[0], cf.RAIL[1], W - cf.RAIL[0], cf.RAIL[2] - cf.RAIL[1]); c.stroke(); c.set_dash([])
    c.set_source_rgba(0.1, 0.1, 0.1, 0.18); c.rectangle(0, 0, W, 96); c.fill()


def script_rows():
    """v4: the shot text lives in ps_text.py (lifted from script v7): id -> (scene, size, picture, action, line, fx)."""
    import ps_text as tx
    scenes = []
    for sid in tx.ORDER:
        if tx.SHOTS[sid]["scene"] not in scenes:
            scenes.append(tx.SHOTS[sid]["scene"])
    rows = {sid: dict(tx.SHOTS[sid]) for sid in tx.ORDER}
    if GAGS_V5[0]:                                           # board v4: the changed rows, and COO? reads HR? everywhere
        for sid, r in rows.items():
            r.update(tx.TEXT_V5.get(sid, {}))
            for f_, v in r.items():
                if isinstance(v, str):
                    r[f_] = v.replace("COO?", "HR?")
    return rows, scenes


def timing():
    """v4: the scene file owns the timing: the recorded takes (ps_voices, timing v2) for the shots that had them, the
    shot's own length for 1.2a/b and 2.1b (new since): -> {shot: length}."""
    rows, _ = script_rows()
    got = {r["shot"]: r["len"] for r in json.load(open(TIMING))["shots"]}
    got.update(LEN_V4)                                       # review round 1: shots trimmed since the takes
    return {sid: got.get(sid, rows[sid]["script"]) for sid in rows}


LEN_V4 = {"2.11": 1.6}                                      # one push, not three (Tomas 24 Nov)


def write_timing(out=os.path.join(OUT, "ps_timing_v3.json")):
    """ps_timing_v3.json: every shot of the scene file with its start, length and its takes (where each line starts)."""
    rows, _ = script_rows()
    old = {r["shot"]: r for r in json.load(open(TIMING))["shots"]}
    tm = timing()
    shots, t = [], 0.0
    for sid in rows:
        o = old.get(sid, {})
        shots.append(dict(shot=sid, scene=rows[sid]["scene"], start=round(t, 2), len=round(tm[sid], 2),
                          takes=o.get("takes", []), take_at=o.get("take_at", []), line=rows[sid]["line"] or None))
        t += tm[sid]
    json.dump(dict(total=round(t, 2), source="ps_scenes.py v4 (takes: ps_voices takes v2)", shots=shots),
              open(out, "w"), indent=1, ensure_ascii=False)
    print("wrote", out, "%.2f s" % t)
    return shots


def write_script(out=None):
    """The script, generated from the scene file and ps_text (never edited by hand). v9 with GAGS_V5 (board v4)."""
    import ps_text as tx
    ver = 9 if GAGS_V5[0] else 8
    out = out or os.path.join(OUT, "pick-a-side-script-v%d.md" % ver)
    rows, scenes = script_rows()
    shots = {r["shot"]: r for r in write_timing()}
    total = sum(r["len"] for r in shots.values())
    L = ["# Pick a Side: the script, v%d (GENERATED)" % ver, "",
         "UptimeZ Inc. · episode 14 · **generated by `src/ps_scenes.py script%s` on %s: do not edit.** The words live in "
         % ((" v5", "25 Nov") if GAGS_V5[0] else ("", "24 Nov")) +
         "`src/ps_text.py`, the staging and timing in `src/ps_scenes.py`; the takes in `src/ps_voices/takes/` (19 lines). "
         "v1–v7 were written by hand and are kept. **%d shots, %.1f s.**" % (len(rows), total), ""]
    for name in ("G0: the series check", "G1: protect list", "Line budget"):
        L += ["## " + name, "", tx.SECTIONS[name], ""]
    for sc in scenes:
        ids = [sid for sid in rows if rows[sid]["scene"] == sc]
        t0 = shots[ids[0]]["start"]; dur = sum(shots[i]["len"] for i in ids)
        L += ["## %s · %d:%04.1f · %.1f s" % (sc, t0 // 60, t0 % 60, dur), "",
              "| Shot | At | s | Size | Picture | Action → reaction | Line | Sound |", "|---|---|---|---|---|---|---|---|"]
        for sid in ids:
            r, sh = rows[sid], shots[sid]
            L.append("| %s | %d:%04.1f | %.1f | %s | %s | %s | %s | %s |" % (sid, sh["start"] // 60, sh["start"] % 60, sh["len"],
                     r["size"], r["picture"], r["action"], r["line"] or "—", r["fx"] or "—"))
        L.append("")
    for name in tx.SECTIONS:
        if name not in ("G0: the series check", "G1: protect list", "Line budget"):
            L += ["## " + name, "", tx.SECTIONS[name], ""]
    text = "\n".join(L)
    if GAGS_V5[0]:                                           # the sections (protect list, props) say HR? too
        text = text.replace("COO?", "HR?")
    open(out, "w").write(text)
    print("wrote", out)


def layout_sheet(n, shots, rows, out):
    cols, tw, th = 4, 270, 480
    nr = (len(shots) + cols - 1) // cols
    SW, SH = 30 + cols * (tw + 30), 110 + nr * (th + 130)
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, SW, SH); c = cairo.Context(s)
    c.set_source_rgb(0.96, 0.95, 0.92); c.paint()
    c.select_font_face("Inter", 0, 1); c.set_font_size(22); c.set_source_rgb(*INK); c.move_to(30, 44)
    c.show_text("PICK A SIDE · layout v4 · %s" % rows[shots[0]["id"]]["scene"])
    c.select_font_face("Inter", 0, 0); c.set_font_size(13); c.set_source_rgb(0.3, 0.3, 0.3); c.move_to(30, 70)
    c.show_text("generated by ps_scenes.py · each frame at 270 · red: the apps' zones · checks: uz_check scale + signs")
    fails = []
    for i, sh in enumerate(shots):
        surf, msgs = render(sh)
        _zones(cairo.Context(surf))
        x = 30 + (i % cols) * (tw + 30); y = 90 + (i // cols) * (th + 130)
        c.save(); c.translate(x, y); c.scale(0.5, 0.5); c.set_source_surface(surf, 0, 0); c.paint(); c.restore()
        r = rows[sh["id"]]
        c.select_font_face("Inter", 0, 1); c.set_font_size(12); c.set_source_rgb(*INK)
        for j, ln in enumerate(textwrap.wrap("%s  %s · %s" % (sh["id"], r["size"], r["picture"].replace("**", "")), 42)[:3]):
            c.move_to(x, y + th + 18 + j * 16); c.show_text(ln)
        if r["line"]:
            c.set_source_rgb(0.2, 0.3, 0.6); c.move_to(x, y + th + 70); c.show_text(r["line"][:48])
        ok = not msgs
        c.set_source_rgb(*((0.1, 0.45, 0.2) if ok else (0.8, 0.1, 0.1))); c.move_to(x, y + th + 90)
        c.show_text("OK" if ok else ("FAIL: " + "; ".join(m.split(" at ")[0] for m in msgs))[:62])
        fails += [(sh["id"], m) for m in msgs]
    s.write_to_png(out)
    return fails


def loop_check():
    import numpy as np
    a = render(SHOTS[0])[0]; b = render(SHOTS[-1])[0]
    A = np.ndarray((H, W, 4), np.uint8, a.get_data()).astype(int)
    B = np.ndarray((H, W, 4), np.uint8, b.get_data()).astype(int)
    return int((np.abs(A - B)[..., :3].max(axis=2) > 8).sum())


def main(out=OUT):
    rows, scenes = script_rows()
    missing = [r for r in rows if r not in {s["id"] for s in SHOTS}]
    if missing:
        print("shots in ps_text with no staging:", missing); sys.exit(1)
    fails = []
    for n in sorted({SCENE_OF(s["id"]) for s in SHOTS}):
        shots = [s for s in SHOTS if SCENE_OF(s["id"]) == n]
        p = os.path.join(out, "ps_layout_s%d_v4.png" % n)
        fails += layout_sheet(n, shots, rows, p)
        print("wrote", p, flush=True)
    tm = timing()
    print("timing: %.1f s over %d shots" % (sum(tm.values()), len(tm)))
    d = loop_check()
    print("loop: 6.2 against 1.1, %d px differ (the robot's arm up, the room's state)" % d)
    for sid, m in fails:
        print("FAIL", sid, m)
    if fails:
        sys.exit(1)
    print("all layout frames pass")


# --- stage 5: the board (one key frame per shot at 540, its lines in bubbles, the apps' overlay) ------------------------
SPEAKER = {"DON": "don", "ROBOT": "robot", "MOM": "mom", "PAM": "pam", "SOFÍA": "sofia", "CLIENT": "client", "FATHER": "father"}


def says(line):
    """'DON: "x" · ROBOT: "y"' -> [("don", "x"), ("robot", "y")]."""
    out = []
    for part in line.split(" · "):
        m = re.match(r'([A-ZÍ]+)[^:]*:\s*"(.*)"', part.strip())
        if m:
            out.append((SPEAKER[m.group(1)], m.group(2)))
    return out


def board_frame(sh, line):
    import fs_animatic as an
    if FIX_V4[0]:
        import ps_checks as pc
        pc.install_scene(sys.modules[__name__]); pc.begin()      # the story props get declared as they are drawn
        del BUBBLES_V4[:]
    CUR_SHOT[0] = sh["id"]
    surf, msgs = render(sh)
    fc = dict(LAST[0])
    c = cairo.Context(surf); k = Ctx(c, 0)
    taken = []
    lines_ = says(line)
    if FIX_V4[0]:                                             # the people's bubbles first (beside the face); the robot's
        lines_ = sorted(lines_, key=lambda w: w[0] == "robot")   # comes down onto its antenna wherever is left
        if PART[0] is not None:                               # a split shot's key frame: one of its lines
            lines_ = [says(line)[PART[0]]] if PART[0] < len(says(line)) else []
        if GAGS_V5[0] and CAMKEY[0] == TREAT_53:              # "Welcome." is said on 5.3a; 5.3b has no line
            lines_ = []
    for who, txt in lines_:
        if who not in fc:
            msgs.append("BUBBLE %s: %s speaks but is not in the frame" % (sh["id"], who)); continue
        hx, hy, r = fc[who]
        if FIX_V4[0]:
            import speech_gate
            before = speech_gate.snapshot(surf)
            box = bubble_v4(k, who, txt, fc, taken)
            taken.append(box)
            rec = BUBBLES_V4[-1]
            import speech as sp_
            msgs.extend(speech_gate.check(surf, rec["box"], rec["tip"], list(fc.values()), above=rec["above"],
                                           before=before, fill=sp_.TINT if who == "robot" else None))
            continue
        if who == "robot":
            tail = (hx - r * 0.62, hy - r * 0.62, 2)
        else:
            tail = (hx, hy + r * 0.08, r * 0.72)
        others = [v for n, v in fc.items() if n != who]
        box = an.speech(c, k, txt.upper() if who == "robot" else txt, (hx, hy, r), others, mono=(who == "robot"), size=26,
                        taken=tuple(taken), tail_head=tail, top_tip_at=None)
        taken.append(box)
        x0, y0, x1, y1 = box
        if x0 < 18 or y0 < 96 or x1 > 522 or y1 > 720:
            msgs.append("BUBBLE %s outside the safe area %s" % (sh["id"], tuple(round(v) for v in box)))
        for n, (fx_, fy_, fr) in fc.items():
            if x0 < fx_ + fr * 0.8 and x1 > fx_ - fr * 0.8 and y0 < fy_ + fr * 0.8 and y1 > fy_ - fr * 0.8:
                msgs.append("BUBBLE %s over %s's face" % (sh["id"], n))
    return surf, msgs



# --- v4 bubbles: speech.draw and speech_gate. Opt-in (FIX_V4): board v2 and the layout sheets v3 draw as before.
def bubble_v4(k, who, text, fc, taken):
    """-> the box drawn. speech.draw places it: beside the face when that wall is clear, from above only for the robot's
    antenna. FIX_V4 only; the v3 sheets stay on fs_animatic.speech."""
    import speech
    import ps_checks as pc
    head = fc[who]
    mono = who == "robot"
    above = (head[0], head[1] - head[2] * 1.48) if mono else None   # just over the antenna's ball (ball top at 1.42 r)
    if who == "don" and CUR_SHOT[0] in DON_OVER:             # review round 1: over Don's bare scalp (allowed: no hair), so the
        above = (head[0], head[1] - head[2] * 1.02)          # wall beside him keeps the tape and Sofía's CV clear

    mouth = (head[0], head[1] + 0.35 * head[2])
    avoid = list(taken)
    if who == "don" and CUR_SHOT[0] in DON_OVER_ONLY:        # 1.4: the box on his free side, off the trio
        hx_, hy_, r_ = head
        avoid.append((hx_ + r_ * 0.9, hy_ - r_ * 0.6, hx_ + 300, hy_ + r_ * 1.4))   # the trio's side closed: his left wall
    for name, a0, b0, a1, b1 in pc.PROTECT:
        avoid.append((a0, b0, a1, b1))
    avoid.extend(SIGNS_V4)
    import speech_gate as sg_
    avoid.append(sg_.RAIL)                                   # main's gate (24 Nov): no box in the app's button rail
    speech.ROBOT[0] = speech.CLEAR[0] = True                 # the series' robot bubble: tinted, bold mono; the wall with no
    if mono and CUR_SHOT[0] in ROBOT_WALL:                   # other face beside it (Tomas 24 Nov, round 5)
        hx, hy, r = head                                     # 3.1a: its line read as Don's on Don's side of its visor; that
        side = ROBOT_WALL[CUR_SHOT[0]]                       # wall closed (Mom stands over its antenna: no box fits above)
        avoid.append((hx - 300, hy - r * 1.2, hx - r * 0.9, hy + r * 1.2) if side > 0 else
                     (hx + r * 0.9, hy - r * 1.2, hx + 300, hy + r * 1.2))
    try:
        box, tip = speech.draw(k, text, head, mouth=mouth, above=above, mono=mono,
                               others=[v for n, v in fc.items() if n != who], avoid=avoid)
    finally:
        speech.ROBOT[0] = speech.CLEAR[0] = False
    if above and tip and abs(tip[0] - above[0]) < 8 and abs(tip[1] - above[1]) < 8:
        form = "T"
    elif tip and tip[0] >= head[0]:
        form = "R"
    else:
        form = "L"
    BUBBLES_V4.append(dict(who=who, form=form, tip=tip, box=box, text=text, face=head, above=above))
    return box


BUBBLES_V4 = []
CUR_SHOT = [None]
NO_SHIFT = [False]                                           # a motion test passes a camera already shifted (ps_motion)
DON_OVER = ("6.1",)
DON_OVER_ONLY = ()                                  # 1.4: the box over his scalp, not over the trio (read as a held sign)
ROBOT_WALL = {"3.1": 1}                                     # round 5: the robot's line on this side of its visor only (+1 right)
SIGNS_V4 = []                                               # the set's signs drawn in this frame (frame px), kept clear


def app_overlay(c):
    """a plain mock of a short-video app (no real app, no brand): the top bar, the buttons, the caption block."""
    import math
    c.save()
    c.set_source_rgba(0, 0, 0, 0.28); c.rectangle(0, 0, W, 70); c.fill()
    c.set_source_rgba(1, 1, 1, 0.85); c.select_font_face("Inter", 0, 1); c.set_font_size(17)
    c.move_to(170, 44); c.show_text("Following      For you")
    for i, y in enumerate((470, 560, 650, 740)):
        c.set_source_rgba(0, 0, 0, 0.30); c.arc(500, y, 24, 0, 2 * math.pi); c.fill()
        c.set_source_rgba(1, 1, 1, 0.92); c.set_line_width(3); c.arc(500, y, 15, 0, 2 * math.pi); c.stroke()
    g = cairo.LinearGradient(0, 720, 0, 960)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.0); g.add_color_stop_rgba(1, 0, 0, 0, 0.55)
    c.set_source(g); c.rectangle(0, 720, W, 240); c.fill()
    c.set_source_rgba(1, 1, 1, 0.92); c.set_font_size(18); c.move_to(20, 840); c.show_text("@uptimez")
    c.restore()


def board(out=OUT, frames_dir="/tmp/ps_board_v3", tag="v3"):
    """every shot's key frame at 540 in frames_dir (bubbles, no overlay: for the cold viewers) and two sheets at 270 with
    the apps' overlay, time, shot and line."""
    rows, _ = script_rows()
    tm = timing()
    os.makedirs(frames_dir, exist_ok=True)
    for f_ in os.listdir(frames_dir):
        os.remove(os.path.join(frames_dir, f_))
    frames, fails, t = [], [], 0.0
    n = 0
    for sh in SHOTS:
        r = rows[sh["id"]]
        keys = board_keys(sh, r["line"])
        for j, (label, surf, msgs) in enumerate(keys):
            n += 1
            p = os.path.join(frames_dir, "%02d.png" % n); surf.write_to_png(p)
            frames.append((label, t + j * tm[sh["id"]] / len(keys), r["line"], p))
            fails += [(label, m) for m in msgs]
        t += tm[sh["id"]]
    half = (len(frames) + 1) // 2
    for j, part in enumerate((frames[:half], frames[half:])):
        cols, tw, th = 5, 270, 480
        nr = (len(part) + cols - 1) // cols
        SW, SH = 30 + cols * (tw + 24), 90 + nr * (th + 70)
        s = cairo.ImageSurface(cairo.FORMAT_RGB24, SW, SH); c = cairo.Context(s)
        c.set_source_rgb(0.12, 0.12, 0.14); c.paint()
        c.select_font_face("Inter", 0, 1); c.set_font_size(22); c.set_source_rgb(1, 1, 1); c.move_to(30, 44)
        c.show_text("PICK A SIDE · board v3 · %d of 2 · every shot's key frame at 270, under the apps' overlay" % (j + 1))
        for i, (sid, t0, line, p) in enumerate(part):
            x = 30 + (i % cols) * (tw + 24); y = 70 + (i // cols) * (th + 70)
            fr = cairo.ImageSurface.create_from_png(p)
            g = cairo.Context(fr); app_overlay(g)
            c.save(); c.translate(x, y); c.scale(0.5, 0.5); c.set_source_surface(fr, 0, 0); c.paint(); c.restore()
            c.select_font_face("Inter", 0, 1); c.set_font_size(13); c.set_source_rgb(1, 1, 1)
            c.move_to(x, y + th + 20); c.show_text("%s · %d:%04.1f" % (sid, t0 // 60, t0 % 60))
            if line:
                c.select_font_face("Inter", 0, 0); c.set_font_size(11); c.set_source_rgb(0.75, 0.82, 1.0)
                for li, ln in enumerate(textwrap.wrap(line.replace("**", ""), 46)[:2]):   # review round 1: not cut mid-word
                    c.move_to(x, y + th + 38 + li * 14); c.show_text(ln)
        o = os.path.join(out, "ps_board_%s_%d.png" % (tag, j + 1)); s.write_to_png(o); print("wrote", o)
    for sid, m in fails:
        print("FAIL", sid, m)
    return fails


def check_all(frames_dir=None):
    """v4 (Tomas 24 Nov: all the series' checks): every shot rendered with ps_checks wired in (limbs, tails, strays, the
    drawing map, Don the tallest, story props out of the dead zones), on its board frame (bubbles drawn). Fails the build."""
    import ps_checks as pc
    if not pc.validate():
        print("a check missed its planted fault"); return ["validate"]
    if not hands_validate():
        print("the hand gate missed its planted fault"); return ["validate"]
    pc.install_scene(sys.modules[__name__])
    FIX_V4[0] = True
    rows, _ = script_rows()
    fails = [("map", m) for m in pc.check_map(SHOTS, EXPECT)]
    _CHK[0] = lambda: pc.frame_checks(sys.modules[__name__], LAST[0]) + hand_checks()
    orig = globals()["board_frame"]
    def bf(sh, line):
        pc.begin(); del GRIPS_LOG[:]; del HANDS_LOG[:]; return orig(sh, line)
    globals()["board_frame"] = bf
    try:
        for sh in SHOTS:
            for label, surf, msgs in board_keys(sh, rows[sh["id"]]["line"]):
                if frames_dir:
                    os.makedirs(frames_dir, exist_ok=True); surf.write_to_png(os.path.join(frames_dir, label + ".png"))
                msgs = [m for m in msgs if (label, m.split(":")[0]) not in KNOWN_V4]
                fails += [(label, m) for m in msgs]
                print("%-5s %s" % (label, "ok" if not msgs else "; ".join(msgs)), flush=True)
    finally:
        globals()["board_frame"] = orig; _CHK[0] = None
    print("%d shots, %d faults" % (len(SHOTS), len(fails)))
    return fails


if __name__ == "__main__":
    V5 = "v5" in sys.argv[2:]                                  # `check v5`, `board v5`: with GAGS_V5 (board v4)
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        if V5:
            gags_v5()
        sys.exit(1 if check_all("/tmp/ps_check_v5" if V5 else "/tmp/ps_check") else 0)
    if len(sys.argv) > 1 and sys.argv[1] == "script":
        if V5:
            gags_v5()
        write_script(); sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == "board":
        FIX_V4[0] = True                                      # board v3: with the fixes the checks found
        if V5:
            gags_v5(); sys.exit(1 if board(frames_dir="/tmp/ps_board_v4", tag="v4") else 0)
        sys.exit(1 if board() else 0)
    main(sys.argv[1] if len(sys.argv) > 1 else OUT)
