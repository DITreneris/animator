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
    return o, (o["head"][0], o["head"][1], R["don"] * SC["don"])


def robot(k, where, **kw):
    x, f = at(where) if isinstance(where, str) else where
    o = rp.robot(k, x, f, SC["robot"], **kw)
    sx, sy = o["screen"]
    return o, (sx, sy, R["robot"] * SC["robot"])


def sofia(k, where, pose="stand", face="smile", look=(0, 0)):
    x, f = at(where) if isinstance(where, str) else where
    o = sp.sofia(k, x, f, SC["sofia"], pose, face, look=look)
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


def cast_11(down=False, last=False):
    def f(k):
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


def cast_14(k):
    heads = {}
    dx_ = 200
    t_ = 0
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
        dp.tape_strip(k, o["hands"][0], o["hands"][1], SC["don"])
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
    _, heads["robot"] = robot(k, "rob_throne", arms=((-8, 0), (-120, -30)), visor=None)
    return heads


def cast_22(k):
    heads = {}
    _, heads["don"] = don(k, "don_throne", "push", "squint", (-1, -0.3))
    return heads


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


def cast_53(k):
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


def fg_56(k):
    """Pam near, on the stool, frozen with the blind; the frame's left, her eyes over to Sofía crossing."""
    s_ = 0.54 * 2.2
    tmp = cairo.ImageSurface(cairo.FORMAT_RGB24, 4, 4)
    hh = pm.pam(Ctx(cairo.Context(tmp), 0), 140, 1060 - 98 * s_, s_, "rail", "frozen", (1, 0.1))["hands"]
    pm.blind_rail(k, hh[0], hh[1], s_)                               # v3: the blind hangs from her rail
    o = pm.pam(k, 140, 1060 - 98 * s_, s_, "rail", "frozen", (1, 0.1), late=False)
    pm.rail_bar(k, o["hands"][0], o["hands"][1], s_)
    import hands_ps as hp
    hp.redraw_late(k)
    return {"pam": (o["head"][0], o["head"][1], R["pam"] * s_)}


def cast_57(k):
    heads = {}
    _, heads["sofia"] = sofia(k, (660, F + 40), "stand", "smile", (-1, -0.2))
    return heads


def cast_61(k):
    """behind: Mom on the tape turned away, Pam's reach across it, Sofía past the line with COO?; the throne's card."""
    heads = {}
    _, heads["mom"] = mom(k, "mom_tape", "folded", "stern", (1, -0.6))                      # v3: eyes away, up
    o, heads["sofia"] = sofia(k, (640, F + 40), "chest", "smile", (0.2, 0.6))                # v3: eyes on her CV, not Don
    hx, hy = o["hands"][0]
    sp.cv_coo(k, hx + 4, hy + (40 if FIX_V4[0] else 4), 0.8)    # held at her chest, COO? up; v4: lower, off her face
    o, heads["pam"] = pam(k, (tape_x(55) - 40, F + 55), "reach", "avert", (1, 0.6), mug=False)  # v3: eyes on her lit phone
    if FIX_V4[0]:                                            # v4 (Tomas 24 Nov): small, flat, under her fingers, away from
        pss.pam_phone(k, o["hands"][1][0] + 4, o["hands"][1][1] + 8, 1.6, lit=True)   # Sofía's CV (upright read as hers)
    else:
        pss.pam_phone(k, o["hands"][1][0] + 30, o["hands"][1][1] + 10, 1.4, lit=True)
    return heads


def fg_61(k):
    """Don, near, big, front-left on his side, facing us: drawn in frame units."""
    o = dp.don(k, 170, 1150, 0.60 * 2.5, "vest", "smug", (0, 0), chin=1)
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


def ins_prints(k):
    c = k.c
    c.set_source_rgb(0.10, 0.05, 0.06); c.paint()
    rp.phone_screen(k, 270, 520, 2.3, "posted")
    for (x, y) in ((270, 452), (324, 548)):                 # the oily fingertip: a print on Pam, then one on the heel
        c.save(); c.translate(x, y); c.rotate(0.3); c.scale(14, 19)
        c.set_source_rgba(0.08, 0.05, 0.03, 0.55); c.arc(0, 0, 1, 0, 6.3); c.fill(); c.restore()
        c.set_source_rgba(0.02, 0.01, 0.0, 0.5); c.set_line_width(1.2)
        for r_ in (5, 9, 13):
            c.new_path(); c.save(); c.translate(x, y); c.rotate(0.3); c.scale(r_ / 13 * 1.0, r_ / 13 * 1.35)
            c.arc(0, 0, 10, 0.3, 5.9); c.restore(); c.stroke()


def ins_booth_43(k):
    import dh_cast as dc
    c = k.c
    c.set_source_rgb(0.10, 0.03, 0.05); c.paint()
    seat, tbl = 760, 700
    cps.booth_room(k, W, H, seat, tbl)
    cps.handprint(k, 430, seat - 150, 1.6, 0.2)
    cps.phone_on_table(k, 230, tbl - 90, 1.2, prints=True)
    fs_ = 0.62 / 0.52 * 1.15
    of = dc.father(k, 110, seat + 170, fs_, face="hard", look=(0.6, 0.5))
    import client_on3 as co
    cx, s = (424 if FIX_V4[0] else 400), 1.15                    # v4: 24 px right, room for his bubble beside his hand
    oc_ = cps.cast_client(k, cx, seat - co.HIP * s, s, look=(-1.2, 1.4), targets=[(265, tbl - 128), (cx + 40, tbl - 6)],
                          clip_hip=True, hands={-1: "point"}, aim=(230, tbl - 122))
    cps.table(k, W, tbl)
    return {"father": of["head"] + (50 * fs_,), "client": oc_["head"] + (56 * s,)}


def ins_cv(hand=False):
    """5.2 (v3): the CV in the guard's dark sleeve, his hand with the gold pen at the ?: whose hand writes is seen."""
    def f(k):
        import hands_ps as hp
        c = k.c
        c.set_source_rgb(0.80, 0.86, 0.90); c.paint()
        sp.cv_coo(k, 250, 540, 3.0)
        c.set_source_rgb(0.08, 0.08, 0.10); c.new_path()                      # his sleeve, from the right
        c.move_to(560, 330); c.line_to(560, 470); c.line_to(420, 440); c.line_to(410, 380); c.close_path(); c.fill()
        c.set_source_rgb(0.97, 0.97, 0.95); c.rectangle(398, 372, 22, 74); c.fill()   # the cuff
        c.save(); c.translate(372, 420); c.rotate(-0.9)
        c.set_source_rgb(*sp.HEEL_GOLD); c.rectangle(-4, -70, 8, 76); c.fill(); c.restore()   # the gold pen
        hp.draw(k, "fist", 392, 410, 70, (0.80, 0.62, 0.50), (-1.0, 0.1), -1)
    return f


def cast_55(k):
    """5.5 (v3): at the door, Sofía takes the CV, COO? up beside her face."""
    heads = {}
    o, heads["sofia"] = sofia(k, (290, F + 60), "press", "smile", (-0.6, -0.3))
    hx, hy = o["hands"][0]
    sp.cv_coo(k, hx - 30, hy - 6, 1.1)                                      # in her outstretched hand, toward the door
    return heads


def ins_phone_57(k):
    k.c.set_source_rgb(0.55, 0.48, 0.40); k.c.paint()
    if FIX_V4[0]:                                            # v4 (cold test: "Don's phone?" 2 of 3): beside it, Pam's blue mug
        pss.phone_close(k, 230, 520, 1.8)
        k.c.save(); k.c.translate(430, 600); k.c.scale(2.4, 2.4)           # its handle joined to the body (mug_at hides
        k.c.set_source_rgb(*INK); k.c.set_line_width(4); k.c.new_path(); k.c.arc(-18, 0, 10, 1.57, 4.71); k.c.stroke()
        k.c.restore()                                                      # the gap behind her fingers)
        pm.mug_at(k, 430, 600, 2.4)
        return
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
    S("2.4", ["don", "pam"], ROOM2S, cast_scene2("stand", "neutral", (1, 0), chin=0)),
    S("2.5", ["don", "pam"], ROOM2S, cast_25),
    S("2.6", ["mom"], ROOM2S, cast_26),
    S("2.7", ["sofia"], ROOM2S, cast_27),
    S("2.8", "screen", draw=ins_heel),
    S("2.9", ["robot"], ROOM2S, cast_29),
    S("2.9b", ["sofia"], ROOM2S, cast_29b),
    S("2.10", ["don", "robot"], ROOM2S, cast_210),
    S("2.11", ["don", "robot"], ROOM2S, cast_211),
    S("2.12", ["sofia"], ROOM2S, cast_212),
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
FIX_V4 = [False]
SHIFT_V4 = {"2.5": (40, 0, 0.72), "2.10": (80, 0, 0.8), "6.1": (0, -60, 0.9)}   # wall beside the speaker for bc_sb's bubble (lesson 358)
SPLIT_V4 = ("3.1", "4.3")       # two lines said in turn (3.1 the robot, then Mom; 4.3 the Client, then Father) whose bubbles
PART = [None]                    # can't both sit beside their faces: the board shows one key frame per line


def board_keys(sh, line):
    """-> [(label, surface, faults)]: one key frame, or one per line for a split shot."""
    if FIX_V4[0] and sh["id"] in SPLIT_V4:
        out = []
        for i in range(len(says(line))):
            PART[0] = i
            try:
                surf, msgs = board_frame(sh, line)
                out.append((sh["id"] + "abcd"[i], surf, msgs + (_CHK[0]() if _CHK[0] else [])))
            finally:
                PART[0] = None
        return out
    if FIX_V4[0] and sh["id"] in KEYS_V4:
        out = []
        for i, cam_ in enumerate(KEYS_V4[sh["id"]]):
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
IN_HAND_V4 = ("6.1",)
CAM_V4 = {}
KEYS_V4 = {"5.4": [(700, 700, 0.8), None]}                  # Tomas 24 Nov: 5.4a wide (his door, DON · CEO, across the tape),
CAMKEY = [None]                                             # 5.4b the medium (the foot over the line); the camera pushes in
KNOWN_V4 = {}                                               # 1.4's exception lifted: the roll moved to his other hand
DARK_V4 = ("5.4", "5.5", "5.6")                             # Pam's phone dark until 5.7 (the continuity row; ROOM5 had it lit)
INS_UP = {"3.5": 34, "4.2": 54, "5.7": 12}                 # the phone inserts: the phone's bottom edge out of the bottom quarter
LAST = [{}]                                                 # the last render's faces in frame units (for the board)
_last_cam = [None]                                          # the last render's camera (the motion tests hold one camera)


class TextRec(cairo.Context):
    """keeps every text shown (in device units) for uz_check.check_signs."""
    def __init__(self, surf):
        super().__init__()
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
    _floor_on(c, sh["room"])
    pss.room(k, **dict(dict(phone=None), **sh["room"]))
    heads = sh["cast"](k) if sh["cast"] else {}
    c.restore()
    return heads


def render(sh):
    """-> (surface 540x960, the faults)."""
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    c = TextRec(surf); k = Ctx(c, 0)
    c.set_source_rgb(*kit.WALL); c.paint()
    pss.GUARD_CUES[0] = pss.PLATE_BIG[0] = FIX_V4[0]          # v4's set cues travel with the v4 staging
    if sh["cam"] == "screen":
        if FIX_V4[0] and sh["id"] in INS_UP:
            c.set_source_rgb(*kit.WALL); c.paint(); c.translate(0, -INS_UP[sh["id"]])
        h = sh["draw"](k) or {}
        LAST[0] = {n: tuple(v) for n, v in h.items()}
        return surf, []
    cam = sh["cam"]
    if isinstance(cam, list):
        tmp = cairo.ImageSurface(cairo.FORMAT_RGB24, 4, 4)
        h0 = _pass(Ctx(cairo.Context(tmp), 0), sh, None)
        cam = cf.face_cam([h0[n] for n in cam])
    shift = SHIFT_V4 if FIX_V4[0] and sh["id"] in SHIFT_V4 else SHIFT
    if sh["id"] in shift:                                     # the content moved (frame px) / zoomed, off the signs
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
    _floor_on(cb, sh["room"])
    pss.room(kb, **dict(dict(phone=None), **sh["room"])); cb.restore()
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
    return {sid: dict(tx.SHOTS[sid]) for sid in tx.ORDER}, scenes


def timing():
    """v4: the scene file owns the timing: the recorded takes (ps_voices, timing v2) for the shots that had them, the
    shot's own length for 1.2a/b and 2.1b (new since): -> {shot: length}."""
    rows, _ = script_rows()
    got = {r["shot"]: r["len"] for r in json.load(open(TIMING))["shots"]}
    return {sid: got.get(sid, rows[sid]["script"]) for sid in rows}


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


def write_script(out=os.path.join(OUT, "pick-a-side-script-v8.md")):
    """The script, generated from the scene file and ps_text (never edited by hand)."""
    import ps_text as tx
    rows, scenes = script_rows()
    shots = {r["shot"]: r for r in write_timing()}
    total = sum(r["len"] for r in shots.values())
    L = ["# Pick a Side: the script, v8 (GENERATED)", "",
         "UptimeZ Inc. · episode 14 · **generated by `src/ps_scenes.py script` on 24 Nov: do not edit.** The words live in "
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
    open(out, "w").write("\n".join(L))
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
        _wrap_capture(); CAPTURE[0] = True; SIL.clear(); del BUBBLES_V4[:]
    surf, msgs = render(sh)
    fc = dict(LAST[0])
    c = cairo.Context(surf); k = Ctx(c, 0)
    taken = []
    lines_ = says(line)
    if FIX_V4[0]:                                             # the people's bubbles first (beside the face); the robot's
        lines_ = sorted(lines_, key=lambda w: w[0] == "robot")   # comes down onto its antenna wherever is left
        if PART[0] is not None:                               # a split shot's key frame: one of its lines
            lines_ = [says(line)[PART[0]]]
    for who, txt in lines_:
        if who not in fc:
            msgs.append("BUBBLE %s: %s speaks but is not in the frame" % (sh["id"], who)); continue
        hx, hy, r = fc[who]
        if who == "robot" and FIX_V4[0]:                    # v4: beside the visor at eye height, never down onto the dome
            tail = (hx, hy, r * 0.95)
        elif who == "robot":
            tail = (hx - r * 0.62, hy - r * 0.62, 2)
        else:
            tail = (hx, hy + r * 0.08, r * 0.72)
        others = [v for n, v in fc.items() if n != who]
        if FIX_V4[0]:
            box = bubble_v4(k, who, txt, fc, taken)
            taken.append(box)
            x0, y0, x1, y1 = box
            if x0 < 18 or y0 < 96 or x1 > 522 or y1 > 720:
                msgs.append("BUBBLE %s outside the safe area %s" % (sh["id"], tuple(round(v) for v in box)))
            for n, (fx_, fy_, fr) in fc.items():
                if x0 < fx_ + fr * 0.8 and x1 > fx_ - fr * 0.8 and y0 < fy_ + fr * 0.8 and y1 > fy_ - fr * 0.8:
                    msgs.append("BUBBLE %s over %s's face" % (sh["id"], n))
            continue
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



# --- v4 bubbles (Tomas 24 Nov: "bc_sb.bubble"): the approved One Star bubble, beside the face at mouth height, a short
# tail onto the cheek's outline. bc_sb measures its own rigs; here each speaker's silhouette is captured as the rig draws
# it in this frame (CAPTURE), and bc_sb.measure's result is built from it: the mouth row, the cheek edges walked out on
# the silhouette, the crown, how far the hair runs. Opt-in (FIX_V4): board v2 and the layout sheets v3 draw as before.
CAPTURE = [False]
SIL = {}
PADB = 140


def _capture(name, f):
    import numpy as np
    def g(k, *a, **kw):
        c = k.c
        tg = c.get_target()
        if not CAPTURE[0] or getattr(tg, "get_width", lambda: 0)() != W:
            return f(k, *a, **kw)
        c.push_group()
        try:
            r = f(k, *a, **kw)
        finally:
            pat = c.pop_group()
        s_ = cairo.ImageSurface(cairo.FORMAT_ARGB32, W + 2 * PADB, H + 2 * PADB); t = cairo.Context(s_)
        t.translate(PADB, PADB); t.transform(c.get_matrix()); t.set_source(pat); t.paint(); s_.flush()
        a = np.ndarray((H + 2 * PADB, W + 2 * PADB, 4), np.uint8, s_.get_data())[..., 3] > 128
        SIL[name] = SIL[name] | a if name in SIL else a
        c.set_source(pat); c.paint()
        return r
    g.__name__ = getattr(f, "__name__", name)
    return g


def _wrap_capture():
    g = globals()
    if g.get("_captured"):
        return
    g["_captured"] = True
    for n in ("don", "robot", "sofia", "pam", "mom"):
        g[n] = _capture(n, g[n])
    cps.cast_client = _capture("client", cps.cast_client)
    import dh_cast as dc
    dc.father = _capture("father", dc.father)


def _meas(who, face):
    """bc_sb.measure's dict for a speaker drawn in this frame, from its silhouette (frame px, PADB around)."""
    import numpy as np
    import bc_sb as bs
    x, y, r = face
    sil = SIL.get(who)
    z = r / 30.0
    if who == "robot":                                       # its visor: the "mouth" at the smile, the crown the antenna
        my = y + 0.30 * r
    else:
        my = y + 0.48 * r
    cx, cy = int(round(x)) + PADB, int(round(my)) + PADB
    if sil is None or not sil[cy, cx]:
        return dict(ok=True, z=z, m=(x, my), box=(x - 4, my - 3, x + 4, my + 3), eL=x - 0.9 * r, eR=x + 0.9 * r,
                    top=(x, y - 1.05 * r), sL=x - 0.9 * r, sR=x + 0.9 * r, skin=np.zeros((H + 2 * PADB, W + 2 * PADB), bool))
    edge, reach = {}, {}
    for sd in (-1, 1):                                       # the face's outline: the silhouette's run out from the mouth,
        ends = []                                            # bounded by the head's own width (hair and a raised hand
        for row in range(cy - 2, cy + 3):                    # beside it are reach, not cheek)
            xx = cx
            while abs(xx + sd - cx) <= 1.05 * r and sil[row, xx + sd]:
                xx += sd
            ends.append(xx)
        edge[sd] = sorted(ends)[2]
        xx = edge[sd]
        while 0 < xx + sd < W + 2 * PADB - 1 and sil[cy - 2:cy + 3, xx + sd].any():
            xx += sd
        reach[sd] = xx
    band = int(round(0.35 * r))
    cols = sil[:cy, cx - band:cx + band + 1]
    rows = np.nonzero(cols.any(axis=1))[0]
    ty = int(rows.min()) if len(rows) else cy
    tx = float(np.nonzero(cols[ty])[0].mean()) + cx - band if len(rows) else cx
    return dict(ok=True, z=z, m=(x, my), box=(x - 4, my - 3, x + 4, my + 3), eL=edge[-1] - PADB, eR=edge[1] - PADB,
                top=(tx - PADB, ty - PADB), sL=reach[-1] - PADB, sR=reach[1] - PADB, skin=sil)


def _lines(text, size, mono, maxw=300):
    import bc_sb as bs
    bs._REF.select_font_face(bs.MONO if mono else kit.FONT, 0, 1 if mono else 0); bs._REF.set_font_size(size)
    out, cur = [], ""
    for w_ in text.split():
        t = (cur + " " + w_).strip()
        if cur and bs._REF.text_extents(t).x_advance > maxw:
            out.append(cur); cur = w_
        else:
            cur = t
    return out + [cur]


def bubble_v4(k, who, text, fc, taken):
    """-> the box drawn. The robot's bubble comes down onto its antenna (bc_sb's "T", its canon); a person's sits beside
    the face (R or L, whichever is clear of the other faces, the bubbles already placed and the apps' zones), else above."""
    import bc_sb as bs
    mono = who == "robot"
    size = 24 if mono else 26
    lines = _lines(text.upper() if mono else text, size, mono)
    bs.HEADS[who] = dict(meas=_meas(who, fc[who]), m=fc[who][:2], R=fc[who][2], top=fc[who][1] - fc[who][2])
    bs.SAFE = (20, 100, 470, 716)                            # ep 14: above the bottom quarter, off the buttons
    forms = ["T"] if mono else (["R", "L", "T"] if fc[who][0] < 270 else ["L", "R", "T"])
    hair = who in ("sofia", "mom")

    def clash(b):
        x0, y0, x1, y1 = b
        WHY[0] = ""
        if x0 < 18 or y0 < 96 or x1 > 522 or y1 > 720:
            WHY[0] = "safe"; return True
        for n, (fx_, fy_, fr) in fc.items():
            if x0 < fx_ + fr * 0.8 and x1 > fx_ - fr * 0.8 and y0 < fy_ + fr * 0.8 and y1 > fy_ - fr * 0.8:
                WHY[0] = "face " + n; return True
        if any(x0 < t[2] and x1 > t[0] and y0 < t[3] and y1 > t[1] for t in taken):
            WHY[0] = "bubble"; return True
        import ps_checks as pc
        for name, a0, b0, a1, b1 in pc.PROTECT:              # never over a story prop (the phones, the CV, the card, the roll)
            if x0 < a1 - 3 and x1 > a0 + 3 and y0 < b1 - 3 and y1 > b0 + 3:
                WHY[0] = "prop " + name; return True
        for t in SIGNS_V4:                                   # never over part of a sign (a sign wholly under it is out)
            if x0 < t[2] - 4 and x1 > t[0] + 4 and y0 < t[3] - 3 and y1 > t[1] + 3 and not (
                    x0 <= t[0] - 2 and x1 >= t[2] + 2 and y0 <= t[1] - 2 and y1 >= t[3] + 2):
                WHY[0] = "sign %s" % (tuple(round(v) for v in t),); return True
        return False

    ms = bs.HEADS[who]["meas"]
    my = ms["m"][1]

    def room_at(fm, dy_, nl=2):
        """the wall beside the face for a box of nl lines centred dy_ below the mouth: to the frame's safe edge or the
        next face whose rows it shares."""
        if fm == "T":
            return 300
        h2 = (nl * size * 1.12 + 26) / 2
        near = [(fx_, fr) for n, (fx_, fy_, fr) in fc.items()
                if n != who and fy_ - fr * 0.8 < my + dy_ + h2 and fy_ + fr * 0.8 > my + dy_ - h2]
        if fm == "R":
            return min([bs.SAFE[2]] + [fx_ - fr * 0.8 - 6 for fx_, fr in near if fx_ > fc[who][0]]) - \
                (ms["sR"] if hair else ms["eR"]) - 20 - 44
        return (ms["sL"] if hair else ms["eL"]) - 20 - 44 - \
            max([bs.SAFE[0]] + [fx_ + fr * 0.8 + 6 for fx_, fr in near if fx_ < fc[who][0]])
    pick, pl = forms[-1], lines
    bs.BUBBLES = False
    pdy = pdx = 0
    for fm, dy_ in [(f_, d_) for f_ in forms for d_ in ((0, -24, 24, -48, 48, 72) if f_ != "T" else (0,))]:
        ln_ = _lines(text.upper() if mono else text, size, mono, max(96, min(300, room_at(fm, dy_))))
        for _ in range(2):                                   # the wall for that many lines (a taller box meets more faces)
            ln_ = _lines(text.upper() if mono else text, size, mono, max(96, min(300, room_at(fm, dy_, len(ln_)))))
        if len(ln_) > 4:
            continue
        bs.bubble(k, ln_, who, form=fm, size=size, mono=mono, hair=hair and fm != "T", dy=dy_)
        b = bs.QA["bubbles"].pop()
        cl = clash(b["box"])
        ddx = 0
        for _ in range(3):                                   # a prop in the hand beside the face: step past it
            if not (cl and WHY[0].startswith("prop") and fm in ("R", "L")):
                break
            import ps_checks as pc
            pb = [p_ for p_ in pc.PROTECT if p_[0] == WHY[0][5:]][0]
            ddx += (pb[3] + 7 - b["box"][0]) if fm == "R" else (pb[1] - 7 - b["box"][2])
            if abs(ddx) > 80:
                break
            ln_ = _lines(text.upper() if mono else text, size, mono, max(96, min(300, room_at(fm, dy_, len(ln_)) - abs(ddx))))
            bs.bubble(k, ln_, who, form=fm, size=size, mono=mono, hair=hair, dy=dy_, dx=ddx)
            b = bs.QA["bubbles"].pop()
            cl = clash(b["box"])
        if not cl and ddx:
            pick, pl, pdy, pdx = fm, ln_, dy_, ddx; break
        if DEBUG_V4[0]:
            print("   ", who, fm, dy_, len(ln_), tuple(round(v) for v in b["box"]), WHY[0])
        if not cl:
            pick, pl, pdy, pdx = fm, ln_, dy_, 0; break
    bs.BUBBLES = True
    bs.bubble(k, pl, who, form=pick, size=size, mono=mono, hair=hair and pick != "T", dy=pdy, dx=pdx)
    b = bs.QA["bubbles"][-1]
    BUBBLES_V4.append(dict(who=who, form=pick, tip=b["tip"], box=b["box"], text=text, face=fc[who]))
    return b["box"]


BUBBLES_V4 = []
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


def board(out=OUT, frames_dir="/tmp/ps_board_v3"):
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
                c.move_to(x, y + th + 38); c.show_text(line.replace("**", "")[:52])
        o = os.path.join(out, "ps_board_v3_%d.png" % (j + 1)); s.write_to_png(o); print("wrote", o)
    for sid, m in fails:
        print("FAIL", sid, m)
    return fails


def check_all(frames_dir=None):
    """v4 (Tomas 24 Nov: all the series' checks): every shot rendered with ps_checks wired in (limbs, tails, strays, the
    drawing map, Don the tallest, story props out of the dead zones), on its board frame (bubbles drawn). Fails the build."""
    import ps_checks as pc
    if not pc.validate():
        print("a check missed its planted fault"); return ["validate"]
    pc.install_scene(sys.modules[__name__])
    FIX_V4[0] = True
    rows, _ = script_rows()
    fails = [("map", m) for m in pc.check_map(SHOTS, EXPECT)]
    _CHK[0] = lambda: pc.frame_checks(sys.modules[__name__], LAST[0])
    orig = globals()["board_frame"]
    def bf(sh, line):
        pc.begin(); return orig(sh, line)
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
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        sys.exit(1 if check_all("/tmp/ps_check") else 0)
    if len(sys.argv) > 1 and sys.argv[1] == "script":
        write_script(); sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == "board":
        FIX_V4[0] = True                                      # board v3: with the fixes the checks found
        sys.exit(1 if board() else 0)
    main(sys.argv[1] if len(sys.argv) > 1 else OUT)
