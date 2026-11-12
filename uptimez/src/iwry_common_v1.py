"""Shared drawing for the "I Will Replace You" motion tests and storyboard: the set with an animatable
state dict, per-shot staging (cafe_kit.STAGE), cameras (cafe_set_sheet.CAMS) and bubbles."""
import math
import cairo
import kit
import anim
import pt42
import waiter_kit as w
import cafe_kit as ck
import sofia_v4 as sf
import don_v4 as dv
import day1_sb_v3 as sb
from cafe_set_sheet import CAMS
from kit import INK
from anim import clamp, ease, lerp, back_out

W, H = 540, 960
NO_BUBBLES = False      # QA: render without bubbles to measure what they cover
LAST = {}               # QA: key points and camera of the last drawn frame


def u(t, t0, d):
    return clamp((t - t0) / d)


def state(**kw):
    """Defaults for one frame of the set; override per frame."""
    s = dict(stage="true", sof_x=None, robot_x=None, don_x=None,
             robot="table", r_pose="stand", r_face="eager", r_look=(1, 0), r_wobble=0.0, r_tray=None, r_talk=0.0,
             r_locked=None, r_head_dx=None, r_head_rot=None,
             sof_pose="stand", sof_face="neutral", sof_look=(0.6, 0),
             don_pose="stand", don_face="smug", don_look=(-0.6, 0), don_chin=0, don_thumb=False, don_wrench=False,
             burgers=False, dome=None, slip=0.0, oil_drop=None, edge_bolt=None, robot_feet=None, r_front=False)
    s.update(kw)
    st = ck.STAGE[s["stage"]]
    for key, who in (("sof_x", "sof"), ("robot_x", "robot"), ("don_x", "don")):
        if s[key] is None:
            s[key] = st[who]
    return s


def world(k, s):
    """Draws the set for state s; returns key points (world coordinates)."""
    c = k.c
    out = {}
    ck.room(k)
    ck.menu_board(k, 80, 330)
    pt42.wall_sign(k, 310, 340, 30)
    ck.counter(k, 760)
    ck.pam_corner(k)
    sx, rx, dx = s["sof_x"], s["robot_x"], s["don_x"]
    if sx is not None:
        ck.chair_back(k, sx, ck.SOF[1] - 214, 1250)
    if dx is not None:
        ck.chair_back(k, dx, ck.DON[1] - 244, 1251)
    draw_robot = lambda: w.robot(k, rx, ck.ROBOT[1], 1.0, s["r_pose"], s["r_face"], look=s["r_look"],
                               wobble=s["r_wobble"], tray=s["r_tray"], talk=s["r_talk"], seed=1501,
                               locked=s["r_locked"], head_dx=s["r_head_dx"], head_rot=s["r_head_rot"])
    if s["robot"] == "table" and rx is not None and not s["r_front"]:
        out["robot"] = draw_robot()
    if sx is not None:
        sp = s["sof_pose"]
        sp = anim.key(sp) if isinstance(sp, tuple) else sp
        out["sof"] = ck.seated(k, lambda: sf.sofia(k, sx, ck.SOF[1], 1.0, sp, s["sof_face"],
                                                   look=s["sof_look"], folder="none"))
    if dx is not None:
        dp = s["don_pose"]
        dp = anim.key(dp) if isinstance(dp, tuple) else dp
        out["don"] = ck.seated(k, lambda: dv.don(k, dx, ck.DON[1], 1.0, dp, s["don_face"], look=s["don_look"],
                                                 chin=s["don_chin"]))
        hx, hy = out["don"]["hands"][1]
        if s["don_thumb"]:
            dv.thumbs_up(k, (hx, hy))
        if s["don_wrench"]:
            ck.wrench(k, hx - 4, hy - 34, 0.9, 0.2)
        if s["oil_drop"] is not None:                       # a drop falling from the wrench onto his shirt
            v = s["oil_drop"]
            body_top = ck.DON[1] - 300 * kit.PEOPLE["DON"]["h"] + 78
            ox, oy0, oy1 = dx + 14, hy + 30, body_top + 96
            oy = lerp(oy0, oy1, ease(v))
            c.set_source_rgb(*ck.OIL)
            if v < 1:
                c.save(); c.translate(ox, oy); c.scale(3.2, 4.6); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
            else:
                c.save(); c.translate(ox, oy1); c.scale(6, 4); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
    if s["robot"] == "table" and rx is not None and s["r_front"]:   # entering or leaving: passes in front of Don
        out["robot"] = ck.seated(k, draw_robot)
    ck.table(k)
    if s["robot"] == "wide" and rx is not None:              # front plane, rolling back from the counter
        out["robot"] = w.robot(k, rx, s["robot_feet"] or 975, 1.0, "travel", "eager", tray="dome",
                               wobble=s["r_wobble"], side=-1, seed=1500)
    if s["edge_bolt"] is not None:                           # the slipped bolt tips off the table edge (shot 12)
        v = s["edge_bolt"]
        bx = 186 + 14 * v
        by = ck.TABLE_TOP - 12 + (0 if v < 0.35 else 120 * ((v - 0.35) / 0.65) ** 2)
        ck.bolt(k, bx, by, 0.75, 1.5 + 2.0 * max(0, v - 0.15), 1399)
    if s["burgers"]:
        ck.bolt_burger(k, 250, ck.TABLE_TOP - 6, 0.7, wrench_out=False)
        ck.bolt_burger(k, 335, ck.TABLE_TOP - 6, 0.7)
        if s["slip"] > 0:                                  # one bolt slips off the left bun onto the table
            v = s["slip"]
            bx = lerp(250 + 31, 250 + 58, ease(v))
            by = lerp(ck.TABLE_TOP - 27, ck.TABLE_TOP - 12, v * v)
            if v >= 1:
                by = ck.TABLE_TOP - 12
            ck.bolt(k, bx, by, 0.75, lerp(0.12, 1.5, ease(v)), 1399)
    if s["dome"] is not None:                              # the big dome over both plates, lifted up and away
        v = s["dome"]
        dxo, dyo = lerp(0, 90, ease(v)), lerp(0, -170, ease(v))
        c.save(); c.translate(292 + dxo, ck.TABLE_TOP - 8 + dyo); c.rotate(0.35 * ease(v))
        w.dome_tray(k, 0, 0, w=200, dome=1.0, seed=1601)
        c.restore()
    return out


def cam_xf(c, cam, push=0.0):
    cx, cy, z = cam[0], cam[1], cam[2] * (1 + push)
    c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-cx, -cy)
    return (cx, cy, z)


def to_screen(p, cam):
    return (W / 2 + (p[0] - cam[0]) * cam[2], H / 2 + (p[1] - cam[1]) * cam[2])


def head_top(out, who, cam, lift=70):
    hx, hy = out[who]["head"]
    return to_screen((hx, hy - lift), cam)


def shot(cam_n, draw_state, bubbles=(), push=0.0):
    """A panel function: camera cam_n (from CAMS), draw_state(t, tl) -> state dict, bubbles(t, out, cam, k)."""
    def fn(k, t, tl):
        s = draw_state(t, tl)
        c = k.c
        c.save()
        cam = cam_xf(c, CAMS[cam_n], push * tl)          # the engine already adds a 3% push-in per panel
        out = world(k, s)
        c.restore()
        if not NO_BUBBLES:
            for b in bubbles:
                b(k, t, out, cam)
        LAST["out"], LAST["cam"] = out, cam
    return fn
