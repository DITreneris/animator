"""PICK A SIDE (episode 14): the scene file, v1 (stage 4, series/production-process.md). From here on this file is the
episode: every shot with its camera, who is in frame and where, the props' state, the line. Generated from it:

  python3 ps_scenes.py [out_dir]  ->  ps_layout_s<N>_v1.png   a layout sheet per scene, every shot at 270 with its checks
                                      pick-a-side-script-v8.md  the script (generated; do not edit by hand)

The pictures, lines and sizes come from script v7 (approved shot by shot through stop 2 and the blocking, 23 Nov),
the timing from the recorded takes (ps_timing_v2.json; 2.1b, 1.2a/b take the script's lengths). Staging from the floor
plan v3 (ps_plan.py) and Tomas's /grill-me (23 Nov): 1.1 Don faces us; 1.2 split; 2.11 he pushes it onto his side;
6.1 Don big front-left on his side, Sofía small back-right past the line. One key pose per shot: the motion is stage 6.
The checks are uz_check's (scale: no story face in the bottom quarter or under the buttons; signs whole or out) and
the loop's (6.2 against 1.1, drawn by the same code). The build stops (exit 1) on a failure not listed in KNOWN."""
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
def S(id_, cam, room=None, cast=None, draw=None, story=None):
    """cam: (fx, fy, z) | [names] (framed by the series' rule on their faces) | "screen" (an insert drawn in frame units).
    room: ps_set.room's state; cast: fn(k) -> {name: head}; draw: fn(k) for an insert; story: the faces checked."""
    return dict(id=id_, cam=cam, room=room or {}, cast=cast, draw=draw, story=story)


S2 = (112, 515, 2.05)                                       # 1.1 / 6.2: the door, knees up, no floor
ROOM1 = dict(blind="up")
ROOM2 = dict(blind="torn", tape=True)                       # from 2.1: the tape; the throne spun from 2.2
ROOM2S = dict(blind="torn", tape=True, spun=True)
ROOM3 = dict(blind="torn", tape=True, spun=True, silhouette=True)
ROOM5 = dict(blind="rehung", tape=True, spun=True, phone="lit")


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
    _, heads["pam"] = pam(k, (300, F + 20), "cup_mid", "doubt", (0.6, 0))
    _, heads["mom"] = mom(k, (370, F + 16), "folded", "unimpressed", (-0.6, 0))
    _, heads["sofia"] = sofia(k, (440, F + 24), "hip_out", "smile", (-1, 0))
    tmp = cairo.ImageSurface(cairo.FORMAT_RGB24, 4, 4)
    hh = dp.don(Ctx(cairo.Context(tmp), 0), 200, F + 90, SC["don"], "stand", "neutral", (0, 0))["head"]
    dp.blind_cape(k, hh, SC["don"])
    o, heads["don"] = don(k, (200, F + 90), "lift_roll", "hollow", (0, 0))
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
    _, heads["don"] = don(k, (430, F + 110), "salute", "pleased", (0.6, 0), chin=1)
    _, heads["pam"] = pam(k, (500, F + 104), "half_salute", "quiet", (-0.6, 0))
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
    _, heads["don"] = don(k, (tape_x(140) - 120, F + 140), "vest", "smug", (-1, 0), chin=1)
    _, heads["robot"] = robot(k, "rob_tape", arms=((-95, 0), (95, 0)), tilt=0.10)
    return heads


def cast_211(k):
    heads = {}
    _, heads["robot"] = robot(k, (tape_x(140) - 10, F + 140), arms=((-95, 0), (95, 0)), tilt=-0.16)
    heads["don"] = dp.bumped(k, tape_x(140) - 110, F + 140, SC["don"])["head"] + (R["don"] * SC["don"],)
    heads["don"] = (heads["don"][0], heads["don"][1], R["don"] * SC["don"])
    return heads


def cast_212(k):
    heads = {}
    _, heads["sofia"] = sofia(k, "sof_heel", "fold", "smile", (-1, 0))
    return heads


def cast_31(k):
    heads = {}
    _, heads["mom"] = mom(k, "mom_tape", "folded", "unimpressed", (-1, 0))
    _, heads["don"] = don(k, (tape_x(140) - 120, F + 140), "thumbs", "grin", (0, -0.3), chin=1)
    _, heads["robot"] = robot(k, "rob_tape", selfie=1.0, arms=((-95, 0), (160, 0)))
    return heads


def cast_33(k):
    heads = {}
    _, heads["robot"] = robot(k, "rob_tape", selfie=0.6, phone="public", visor="public", arms=((-95, 0), (120, 40)))
    return heads


def cast_34(k):
    heads = {}
    _, heads["don"] = don(k, (tape_x(140) - 120, F + 140), "thumbs", "grin", (0, -0.3), chin=1)
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
    _, heads["pam"] = pam(k, (P["pam_stool"][0], F + P["pam_stool"][1] - 98 * SC["pam"]), "rail", "frozen", (1, -0.1))
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
    _, heads["sofia"] = sofia(k, (tape_x(60) + 20, F + 60), "walk", "smile", (1, 0))
    pm.stool(k, P["pam_stool"][0], F + P["pam_stool"][1], SC["pam"])
    _, heads["pam"] = pam(k, (P["pam_stool"][0], F + P["pam_stool"][1] - 98 * SC["pam"]), "rail", "frozen", (1, -0.1))
    return heads


def cast_57(k):
    heads = {}
    _, heads["sofia"] = sofia(k, (660, F + 40), "stand", "smile", (-1, -0.2))
    return heads


def cast_61(k):
    heads = {}
    _, heads["robot"] = robot(k, "rob_cord", arms=((-8, 0), (172, -4)))
    _, heads["mom"] = mom(k, "mom_tape", "folded", "stern", (1, -0.2))
    _, heads["sofia"] = sofia(k, "sof_far", "stand", "smile", (-0.4, 0))
    _, heads["pam"] = pam(k, "pam_reach", "reach", "avert", (1, 0.4), mug=False)
    _, heads["don"] = don(k, "don_front", "vest", "smug", (0, 0), chin=1)
    return heads


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
    dhp.MOTTO[0] = True
    try:
        dhp.booth(k)
    finally:
        dhp.MOTTO[0] = False


def ins_prints(k):
    c = k.c
    c.set_source_rgb(0.10, 0.05, 0.06); c.paint()
    rp.phone_screen(k, 270, 520, 2.3, "posted")
    cps.handprint(k, 250, 400, 0.55, 0.1)                   # the oily finger: on Pam, then on the heel
    cps.handprint(k, 340, 470, 0.55, -0.2)


def ins_booth_43(k):
    import dh_cast as dc
    c = k.c
    c.set_source_rgb(0.10, 0.03, 0.05); c.paint()
    seat, tbl = 760, 700
    cps.booth_room(k, W, H, seat, tbl)
    cps.handprint(k, 430, seat - 150, 1.6, 0.2)
    cps.phone_on_table(k, 230, tbl - 90, 1.2, prints=True)
    dc.father(k, 110, seat + 170, 0.62 / 0.52 * 1.15, face="hard", look=(0.6, 0.5))
    import client_on3 as co
    cx, s = 400, 1.15
    cps.cast_client(k, cx, seat - co.HIP * s, s, look=(-1.2, 1.4), targets=[(265, tbl - 128), (cx + 40, tbl - 6)],
                    clip_hip=True, hands={-1: "point"}, aim=(230, tbl - 122))
    cps.table(k, W, tbl)


def ins_cv(hand=False):
    def f(k):
        k.c.set_source_rgb(*kit.WALL); k.c.paint()
        sp.cv_coo(k, 270, 520, 3.0)
    return f


def ins_phone_57(k):
    k.c.set_source_rgb(0.55, 0.48, 0.40); k.c.paint()
    pss.phone_close(k, 270, 520, 1.8)


SHOTS = [
    S("1.1", S2, ROOM1, cast_11()),
    S("1.2a", (pss.GX0 + 110, 560, 1.7), dict(blind="torn"), cast_12a),
    S("1.2b", ["pam", "mom", "sofia"], dict(blind="torn", phone="dark"), cast_trio()),
    S("1.3", ["don"], dict(blind="torn"), cast_13),
    S("1.4", ["don", "pam", "mom", "sofia"], dict(blind="torn", phone="dark"), cast_14),
    S("2.1", (480, 860, 1.1), ROOM2, cast_trio("stand", "shock")),
    S("2.1b", ["robot"], ROOM2, cast_21b),
    S("2.2", ["don"], ROOM2S, cast_22),
    S("2.3", ["don"], ROOM2S, cast_scene2(extra=roll_point), story=["don"]),
    S("2.4", (470, 640, 0.90), ROOM2S, cast_scene2("stand", "neutral", (1, 0), chin=0)),
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
    S("3.6", (220, 600, 1.05), ROOM3, cast_36),
    S("3.7", ["pam"], ROOM3, cast_37),
    S("4.1", "screen", draw=ins_booth_wide),
    S("4.2", "screen", draw=ins_prints),
    S("4.3", "screen", draw=ins_booth_43),
    S("5.1", (100, 560, 1.8), dict(blind="torn", tape=True, spun=True, silhouette=True), lambda k: {}),
    S("5.2", "screen", draw=ins_cv()),
    S("5.3", (380, 640, 0.92), dict(blind="rehung", tape=True, spun=True), cast_53),
    S("5.4", ["don"], ROOM5, cast_54),
    S("5.5", "screen", draw=ins_cv(True)),
    S("5.6", ["pam", "sofia"], ROOM5, cast_56),
    S("5.7", "screen", draw=ins_phone_57),
    S("6.1", (430, 620, 1.05), ROOM5, cast_61, story=["don", "sofia"]),
    S("6.2", S2, dict(blind="rehung"), cast_11(down=False, last=True)),
]
SCENE_OF = lambda sid: int(sid.split(".")[0])
KNOWN = {}                                                   # (shot, check) -> why it is allowed


# --- render and check ---------------------------------------------------------------------------------------------------
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


def _pass(k, sh, cam):
    c = k.c
    c.save()
    if cam:
        sbv.view(c, *cam)
    pss.room(k, **dict(dict(phone=None), **sh["room"]))
    heads = sh["cast"](k) if sh["cast"] else {}
    c.restore()
    return heads


def render(sh):
    """-> (surface 540x960, the faults)."""
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    c = TextRec(surf); k = Ctx(c, 0)
    c.set_source_rgb(*kit.WALL); c.paint()
    if sh["cam"] == "screen":
        sh["draw"](k)
        return surf, []
    cam = sh["cam"]
    if isinstance(cam, list):
        tmp = cairo.ImageSurface(cairo.FORMAT_RGB24, 4, 4)
        h0 = _pass(Ctx(cairo.Context(tmp), 0), sh, None)
        cam = cf.face_cam([h0[n] for n in cam])
    heads = _pass(k, sh, cam)
    fx, fy, z = cam
    text = []
    for t in c.texts:
        b = t["bbox"]
        text.append(dict(text=t["text"], bbox=((b[0] - 270) / z + fx, (b[1] - 480) / z + fy, (b[2] - 270) / z + fx,
                                               (b[3] - 480) / z + fy), clip=t["clip"]))
    f = dict(cam=cam, heads=heads, scene=dict(text=text), bubbles=[], shot=sh["id"])
    msgs = uz.check_signs(f) + uz.check_scale(f, sh["story"])
    msgs = [m for m in msgs if (sh["id"], m.split(" at ")[0].split(" (")[0]) not in KNOWN]
    return surf, msgs


def _zones(c):
    c.set_source_rgb(0.85, 0.1, 0.1); c.set_line_width(1.5); c.set_dash([6, 4])
    c.move_to(0, cf.BOTTOM); c.line_to(W, cf.BOTTOM); c.stroke()
    c.rectangle(cf.RAIL[0], cf.RAIL[1], W - cf.RAIL[0], cf.RAIL[2] - cf.RAIL[1]); c.stroke(); c.set_dash([])
    c.set_source_rgba(0.1, 0.1, 0.1, 0.18); c.rectangle(0, 0, W, 96); c.fill()


def script_rows():
    """script v7's shot rows: id -> (size, picture, line)."""
    rows, scenes, cur = {}, [], None
    for ln in open(SCRIPT):
        if ln.startswith("## Scene"):
            cur = ln[3:].strip(); scenes.append(cur)
        m = re.match(r"\| (\d\.\d+[a-z]?) \| \d:\d\d\.\d \| ([\d.]+) \|(.*)", ln)
        if m and cur:
            cells = [x.strip() for x in m.group(3).split("|")]
            rows[m.group(1)] = dict(scene=cur, script=float(m.group(2)), size=cells[0], picture=cells[1], action=cells[2],
                                    line=cells[3] if cells[3] not in ("—", "") else "", fx=cells[4] if len(cells) > 4 else "")
    return rows, scenes


def timing():
    rows, _ = script_rows()
    tj = json.load(open(TIMING))
    got = {r["shot"]: r["len"] for r in tj["shots"]}
    got.setdefault("1.2a", got.get("1.2", 1.0) / 2); got.setdefault("1.2b", got.get("1.2", 1.0) / 2)
    return {sid: got.get(sid, rows[sid]["script"]) for sid in rows}


def layout_sheet(n, shots, rows, out):
    cols, tw, th = 4, 270, 480
    nr = (len(shots) + cols - 1) // cols
    SW, SH = 30 + cols * (tw + 30), 110 + nr * (th + 130)
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, SW, SH); c = cairo.Context(s)
    c.set_source_rgb(0.96, 0.95, 0.92); c.paint()
    c.select_font_face("Inter", 0, 1); c.set_font_size(22); c.set_source_rgb(*INK); c.move_to(30, 44)
    c.show_text("PICK A SIDE · layout v1 · %s" % rows[shots[0]["id"]]["scene"])
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
        print("shots in script v7 with no staging:", missing); sys.exit(1)
    fails = []
    for n in sorted({SCENE_OF(s["id"]) for s in SHOTS}):
        shots = [s for s in SHOTS if SCENE_OF(s["id"]) == n]
        p = os.path.join(out, "ps_layout_s%d_v1.png" % n)
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


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else OUT)
