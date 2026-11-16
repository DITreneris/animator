"""Animation v2, pinned (uptimez_bc_anim_v2.mp4).
THE BEST CANDIDATE: full animation v1 on storyboard v3 (bc_sb.py), set v4, script v5.
The storyboard's 64 panels, re-timed to the real voice takes (a shot is held for its line; a voice is never sped
up), then animated:
  - mouths from the takes (sound_bc.py: phonemes on the 12 fps drawing grid), on whoever has the line; every other
    mouth is the storyboard's (shut);
  - blinks (Sofia, Pam, Don, the small one, the macho; Mom does not blink when she is stern), a slow breath in every
    body, Sofia's earrings swinging;
  - the actions: the door, the phone, the finger, the pen, the chair legs, the paddle and the fingertip, the snap
    upright, the stamp, the scrub, the lapel, the walk round the table, the one tilted frame;
  - camera: a slow push-in on every shot that can take one without cutting a sign, stepped with the drawings;
    bubbles stay in screen space, pop in on the first syllable and never move with the camera;
  - light: a warm key from the upper left, a soft vignette, and the BIAS MONITOR's colour on the room when it rules
    (a flash, then a glow), under the bubbles;
  - the loop: the last drawing is the first one (the door half open), checked pixel for pixel.
  python3 bc_anim.py timing            -> bc_timing.json (shot starts, line starts, sound cues)
  python3 bc_anim.py stills OUT t ...  -> OUT/bc_anim_<t>.png at 540 x 960
  python3 bc_anim.py qa                -> the bubble rules of qa_bc.py on a frame every 1/3 s
  python3 bc_anim.py render OUT [1080] -> OUT silent video, one file per section joined without re-encoding"""
import json
import math
import os
import subprocess
import sys
import cairo
import kit
import bc_sb_anim_v2 as B
import bc_set as S
import cand_bc as cb
import don_bc as db
import don_mf as dm
import mom_bc as mb
import pam_bc as pb
import pam_mf
import sofia_bc as sb
import sofia_v4 as sf4
import props_bc as props
from kit import INK, cut, rect, ellipse

HERE = os.path.dirname(os.path.abspath(__file__))
FPS = 30
TK = json.load(open(os.path.join(HERE, "bc_voices", "takes.json")))
X = S.POS

# shot -> (take, lead before the line, hold after it). A speaking shot is exactly lead + line + hold.
# v2 (the tightening pass): the air is cut, not the lines. Leads and holds are trimmed to what a cut needs; the holds
# that are jokes keep their length (after each of Don's questions, after "apologize", after "Good boy.", before the tilt).
LINES = {"s_first": ("first", 0.2, 0.25), "s_pov": ("three", 0.2, 0.25), "s_half": ("half", 0.2, 0.3),
         "s_q1": ("q1", 0.2, 0.4), "s_data": ("data", 0.15, 0.35), "s_short": ("short", 0.25, 0.4),
         "s_robot_height": ("r_height", 0.15, 0.0), "s_dropped": ("dropped", 0.3, 0.25), "s_thanks": ("thanks", 0.3, 0.4),
         "s_q2": ("q2", 0.12, 0.35), "s_okay": ("okay", 0.2, 0.35), "s_true": ("true", 0.25, 0.4),
         "s_distracting": ("distracting", 0.12, 0.2), "s_whom": ("whom", 0.15, 0.35), "s_push": ("r_looks", 0.35, 0.0),
         "s_no_worries": ("worries", 0.2, 0.3), "s_mom_door": ("morning", 0.5, 0.25),
         "s_experience": ("experience", 0.1, 0.15), "s_forty": ("forty", 0.2, 0.4), "s_five": ("five", 0.15, 0.0),
         "s_ageism": ("r_ageism", 0.25, 0.2), "s_family_q": ("family", 0.2, 0.2), "s_family": ("r_family", 0.2, 0.25),
         "s_q3": ("q3", 0.4, 0.45), "s_apologize": ("apologize", 0.45, 0.5), "s_sorry": ("sorry", 0.12, 0.25),
         "s_sorry_client": ("sorry2", 0.35, 0.3), "s_good_boy": ("goodboy", 0.35, 0.5),
         "s_verdict": ("verdict", 0.3, 0.0), "s_approved": ("approved", 0.4, 0.35),
         "s_welcome": ("welcome", 0.35, 0.05), "s_shout": ("donnie", 0.08, 0.3), "s_father": ("father", 0.25, 0.3),
         "s_why": ("why", 0.2, 0.25), "s_job": ("job", 0.25, 0.5)}
HOLD = {"s_door": 1.0, "s_small_low": 1.0, "s_cross": 0.58, "s_pen_goes": 1.0, "s_chain": 1.5, "s_mom_sits": 1.0,
        "s_pause": 2.0, "s_leaves": 0.83, "s_lick": 0.83, "s_scrub": 1.25, "s_lapel": 1.5, "s_door_end": 1.17}
# silent shots against the storyboard's estimate; the long pause is the script's "about two seconds"
# A line that runs on over the next shot: the cut falls in the silence before its last sentence, so that sentence
# lands on the insert ("Proceed." on the red cross and on the fingertip, "Hired." on the stamp).
SPLIT = {"s_robot_height": False, "s_push": True, "s_verdict": True}     # True: the next shot is held for the rest


def cut_in(key):
    g = TK[key]["gaps"][-1]
    return (g[0] + g[1]) / 2


SPEAKER = {"DON": ("don", "don_up"), "SOF": ("sofia",), "PAM": ("pam",), "SMALL": ("small",), "MACHO": ("macho",),
           "MOM": ("mom_up", "mom_sit"), "ROB": ("robot",)}


def build():
    """Shot starts and lengths, the lines' start times, and the sound cues."""
    shots, lines, t = [], [], 0.0
    names = [s[4].__name__ for s in B.SHOTS]
    for n, sh in enumerate(B.SHOTS):
        name, d = names[n], HOLD.get(names[n], sh[3] - sh[2])
        if name in LINES:                                  # a speaking shot is as long as its line needs, no longer
            key, lead, hold = LINES[name]
            ln = TK[key]["len"]
            d = round(lead + cut_in(key), 2) if name in SPLIT else max(1.0, round(lead + ln + hold, 2))
            lines.append({"key": key, "who": TK[key]["who"], "t0": round(t + lead, 3), "t1": round(t + lead + ln, 3),
                          "shot": name})
        elif n and SPLIT.get(names[n - 1]):                # the rest of the line that started in the shot before
            d = max(d, round(lines[-1]["t1"] - t + 0.25, 2))
        d = round(math.ceil(d * 12 - 1e-6) / 12, 4)        # whole drawings
        shots.append({"id": sh[0], "name": name, "sec": sh[1], "t0": round(t, 4), "d": d})
        t = round(t + d, 4)
    return {"shots": shots, "lines": lines, "total": t}


T = build()
SHOT = {s["name"]: s for s in T["shots"]}
DURATION = T["total"]
CUR = {"t": 0.0, "tl": 0.0, "d": 1.0, "u": 0.0, "name": "", "mon": "idle", "mon_t": 0.0, "push": 0.0, "shake": (0, 0)}
PUSH = {}                                                  # shot -> how far it may push in (set by safe_pushes)


# ---------------------------------------------------------------- time helpers
def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def seg(a, b):
    """0 -> 1 between a and b seconds into the shot, eased."""
    return ease((CUR["tl"] - a) / max(b - a, 1e-6))


def back(x, s=1.7):
    x = max(0.0, min(1.0, x)) - 1
    return x * x * ((s + 1) * x + s) + 1


def lerp(a, b, x):
    return tuple(p + (q - p) * x for p, q in zip(a, b))


def step():
    return int(round(CUR["t"] * 12))


def line_of_shot():
    for ln in T["lines"]:
        if ln["shot"] == CUR["name"]:
            return ln
    return None


def code(who):
    """The mouth shape `who` is making now, "" at rest, None if he has no line here."""
    for ln in T["lines"]:
        if ln["who"] == who and ln["t0"] - 1e-6 <= CUR["t"] < ln["t1"] + 0.25:
            i = int(round((CUR["t"] - ln["t0"]) * 12))
            vis = TK[ln["key"]]["vis"]
            return vis[i] if 0 <= i < len(vis) else ""
    ln = line_of_shot()
    return "" if ln and ln["who"] == who else None


def blinking(period, phase):
    if CUR["name"] in ("s_eyes_jealous", "s_eyes_afraid", "s_tilt", "s_stain", "s_push_cu") or \
            (CUR["name"] == "s_pause" and CUR["u"] < 0.6):
        return False
    return (CUR["t"] + phase) % period < 2 / 12.0


def sway(k, x, feet, phase, fn):
    c = k.c
    a = 0.006 * math.sin(2 * math.pi * CUR["t"] / 3.1 + phase)
    c.save(); c.translate(x, feet); c.scale(1, 1 + a); c.translate(-x, -feet)
    try:
        return fn()
    finally:
        c.restore()


def lids(k, pts, r, skin, ring=False):
    c = k.c
    for x, y in pts:
        ellipse(k, x, y, r, r, skin, 5, shadow=False, outline=False)
        c.set_source_rgb(*INK); c.set_line_width(max(1.6, r * 0.26)); c.set_line_cap(1)
        if ring:
            c.new_path(); c.arc(x, y, r + 1, 0, 2 * math.pi); c.stroke()
        c.new_path(); c.move_to(x - r * 0.8, y + r * 0.1); c.curve_to(x - r * 0.3, y + r * 0.45, x + r * 0.3, y + r * 0.45,
                                                                      x + r * 0.8, y + r * 0.1)
        c.stroke()


# ---------------------------------------------------------------- the cast, animated (wrapped round bc_sb's)
O = {n: getattr(B, n) for n in ("sofia", "don", "pam", "don_up", "mom_up", "mom_sit", "small", "macho", "robot",
                                "bubble", "world", "wood")}
O["backdrop"], O["table"] = S.backdrop, S.table


def _sofia(k, pose="write", face="neutral", look=(-1, 0), **kw):
    cd = code("SOF")
    if cd is not None:
        kw["mouth"] = cd or None
    if blinking(3.9, 2.1) and not kw.get("mouth") and face in ("neutral", "smile", "tiny", "curious", "eyebrow"):
        face = "closed"
    if tuple(kw.get("lag", (0, 0))) == (0, 0):
        kw["lag"] = (1.6 * math.sin(2 * math.pi * CUR["t"] / 1.5), 0)
    return sway(k, X["sofia"], S.SEAT, 3.1, lambda: O["sofia"](k, pose, face, look, **kw))


def _don_lids(k, x, my, face):
    if face not in ("smug", "panic", "happy", "pleased") and blinking(4.3, 1.2):
        lids(k, [(x - 17, my - 26), (x + 17, my - 26)], 11.5, db.SKIN)


def _don_mouth(kw, face):
    cd = code("DON")
    if cd is not None:
        kw["mouth"] = cd or ("M" if face == "pout" else None)


def _don(k, pose=None, face="flat", look=(-0.6, 0.9), **kw):
    _don_mouth(kw, face)
    out = sway(k, X["don"], S.SEAT, 1.7, lambda: O["don"](k, pose, face, look, **kw))
    _don_lids(k, X["don"], S.SEAT + db.HY + 30, face)
    return out


def _don_up(k, x, pose, face, feet=None, **kw):
    _don_mouth(kw, face)
    f = S.FEET if feet is None else feet
    out = sway(k, x, f, 1.7, lambda: O["don_up"](k, x, pose, face, feet=feet, **kw))
    if not kw.get("lean"):
        _don_lids(k, x, f + db.HY + 30, face)
    return out


def _pam(k, pose=None, face="neutral", look=(-1, 0), **kw):
    cd = code("PAM")
    if cd is not None:
        kw["mouth"] = cd or None
    out = sway(k, X["pam"], S.SEAT, 0.0, lambda: O["pam"](k, pose, face, look, **kw))
    if blinking(3.4, 0.9) and out and "head" in out and face not in ("approve", "frozen"):
        hx, hy = out["head"]
        c = k.c
        c.save(); c.rectangle(hx - 60, hy - 30, 120, 38); c.clip()
        for sx in (-17, 17):
            ellipse(k, hx + sx, hy - 1, 13.5, 13.5, pam_mf.SKIN, 5, shadow=False, outline=False)
        c.restore()
        c.set_source_rgb(*INK); c.set_line_width(3.6); c.set_line_cap(1)
        for sx in (-17, 17):
            ex = hx + sx
            c.move_to(ex - 11, hy + 1); c.curve_to(ex - 4, hy + 5, ex + 4, hy + 5, ex + 11, hy + 1); c.stroke()
    return out


MOM_MAP = {"A": "A", "O": "O", "E": "E", "U": "O", "C": "E", "F": "E", "M": None, "": None}


def _mom_up(k, x, feet, s, pose, face, **kw):
    cd = code("MOM")
    if cd is not None:
        kw["mouth"] = MOM_MAP[cd]
    return sway(k, x, feet, 2.3, lambda: O["mom_up"](k, x, feet, s, pose, face, **kw))


def _mom_sit(k, **kw):
    cd = code("MOM")
    if cd is not None:
        kw["mouth"] = MOM_MAP[cd]
    return O["mom_sit"](k, **kw)


def _small(k, pose, face, x=None, seated=True, **kw):
    cd = code("SMALL")
    if cd is not None:
        kw["mouth"] = cd or None
    xx = X["chair"] if x is None else x
    feet = S.CHAIR_SEAT if seated else S.FEET
    o = sway(k, xx, feet + (92 if seated else 0), 0.7, lambda: O["small"](k, pose, face, x=x, seated=seated, **kw))
    if blinking(2.3, 0.4) and face != "crushed" and o and "head" in o:
        hx, hy = o["head"]
        lids(k, [(hx - 20.5, hy + 5), (hx + 20.5, hy + 9.5)], 17.5, cb.S_SKIN, ring=True)
    return o


def _macho(k, pose, face, x=None, feet=None, s=1.0, seated=False, **kw):
    cd = code("MACHO")
    if cd is not None:
        kw["mouth"] = cd or None
    xx = X["chair"] if x is None else x
    ff = S.FEET if feet is None else feet
    o = sway(k, xx, ff, 4.0, lambda: O["macho"](k, pose, face, x=x, feet=feet, s=s, seated=seated, **kw))
    if blinking(4.8, 3.0) and CUR["name"] != "s_thanks":
        my = ff + (cb.M_HY + 40 + (56 if seated else 0)) * s
        lids(k, [(xx - 18 * s, my - 38 * s), (xx + 18 * s, my - 38 * s)], 10 * s, cb.M_SKIN)
    return o


def _robot(k, pose="stand", talk=0.0):
    cd = code("ROB")
    tk = {"A": 1.0, "O": 0.8, "E": 0.6, "C": 0.45, "U": 0.45, "F": 0.3}.get(cd or "", 0.0)
    return O["robot"](k, pose, talk=tk)


def _backdrop(k, door_open=0.0, state="idle", t=0.0, **kw):
    if state != CUR["mon"]:                                # the flash is for the moment it rules, not for every cut
        CUR["mon"], CUR["mon_t"] = state, (CUR["t"] if CUR["name"] in ONSET else -10.0)
    return O["backdrop"](k, door_open, state, CUR["t"], **kw)


def _table(k, items=True, phone=None):
    if phone == "buzz" and step() % 4 >= 2:
        phone = "still"                                    # it buzzes in bursts
    return O["table"](k, items, phone)


def light(k, world_lit=True):
    """Screen space, over the picture and under the bubbles."""
    c = k.c
    if world_lit:
        g = cairo.LinearGradient(0, 0, 420, 620)
        g.add_color_stop_rgba(0, 1.0, 0.96, 0.84, 0.16); g.add_color_stop_rgba(1, 1.0, 0.96, 0.84, 0.0)
        c.set_source(g); c.paint()
        mon = next((b for n, b in B.QA["labels"] if n == "monitor"), None)
        if mon and CUR["mon"] != "idle" and mon[2] > 0 and mon[0] < 540 and mon[3] > 0:
            col = (0.85, 0.12, 0.14) if CUR["mon"] in ("ageism", "family") else (0.12, 0.72, 0.38)
            a = 0.07 + 0.22 * math.exp(-max(0.0, CUR["t"] - CUR["mon_t"]) / 0.3)
            mx, my = (mon[0] + mon[2]) / 2, (mon[1] + mon[3]) / 2
            g = cairo.RadialGradient(mx, my, 0, mx, my, 560)   # on the room, not on the screen itself
            g.add_color_stop_rgba(0, *col, 0.0); g.add_color_stop_rgba(0.30, *col, 0.0)
            g.add_color_stop_rgba(0.46, *col, a); g.add_color_stop_rgba(1, *col, 0.0)
            c.set_source(g); c.paint()
    g = cairo.RadialGradient(270, 450, 300, 270, 450, 660)
    g.add_color_stop_rgba(0, 0.10, 0.07, 0.05, 0.0); g.add_color_stop_rgba(1, 0.10, 0.07, 0.05, 0.30)
    c.set_source(g); c.paint()


def _world(k, cam, draw):
    cam = S.CAMS[cam] if isinstance(cam, str) else cam
    z = cam[2] * (1 + CUR["push"] * CUR["u"])
    cam = (cam[0], cam[1], z) + tuple(cam[3:])
    c = k.c
    sx, sy = CUR["shake"]
    c.save(); c.translate(sx, sy)
    O["world"](k, cam, draw)
    c.restore()
    if CUR["name"] not in ("s_eyes_jealous", "s_eyes_afraid"):
        light(k)


def _wood(k):
    O["wood"](k)


def _bubble(k, lines, who, form="T", size=30, kind="normal", **kw):
    ln = line_of_shot()
    if ln is None or CUR["t"] < ln["t0"] - 1e-6:
        return
    age = CUR["t"] - ln["t0"]
    pop = 0.86 + 0.14 * ease(age / 0.12)
    c = k.c
    if kind == "shout" and age < 0.6:
        j = (-1) ** step() * 3
        kw["dx"], kw["dy"] = kw.get("dx", 0) + j, kw.get("dy", 0) - j
    if pop >= 0.999:
        return O["bubble"](k, lines, who, form, size, kind, **kw)
    c.push_group()
    O["bubble"](k, lines, who, form, size, kind, **kw)
    pat = c.pop_group()
    x0, y0, x1, y1 = B.QA["bubbles"][-1]["box"]
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    c.save(); c.translate(cx, cy); c.scale(pop, pop); c.translate(-cx, -cy)
    c.set_source(pat); c.paint()
    c.restore()


for _n, _f in (("sofia", _sofia), ("don", _don), ("pam", _pam), ("don_up", _don_up), ("mom_up", _mom_up),
               ("mom_sit", _mom_sit), ("small", _small), ("macho", _macho), ("robot", _robot), ("bubble", _bubble),
               ("world", _world), ("wood", _wood)):
    setattr(B, _n, _f)
S.backdrop, S.table = _backdrop, _table


LOOP_DOOR = 0.56                                           # how far the door is open where the film joins itself


# ---------------------------------------------------------------- the shots that move (the rest play as boarded)
def a_door(k):
    op = LOOP_DOOR + (0.9 - LOOP_DOOR) * seg(0, CUR["d"])
    B.world(k, "door", lambda: S.backdrop(k, op, "idle", ficus_sway=2.5 * math.sin(CUR["tl"] * 5) * (1 - CUR["u"])))


def a_door_end(k):
    x = CUR["tl"] / max(CUR["d"] - 1 / 12, 1e-6)
    op = LOOP_DOOR if x > 0.995 else LOOP_DOOR * ease(x)             # the last drawing is frame 0, exactly
    B.world(k, "door", lambda: S.backdrop(k, op, "clear"))


def a_phone47(k):
    B.wood(k)
    j = (-1) ** step() * 3 if CUR["u"] < 0.62 else 0
    hin = seg(0.1, 0.45)
    flip = seg(CUR["d"] * 0.62, CUR["d"] * 0.9)
    c = k.c
    c.save(); c.translate(244 + j, 440); c.scale(max(0.04, abs(1 - 2 * flip)), 1); c.translate(-244, -440)
    if flip < 0.5:
        props.phone(k, 244, 440, 3.5, "missed", True, rot=-0.05)
    else:
        c.save(); c.translate(244, 440); c.rotate(-0.05)
        rect(k, -161, -273, 322, 546, (0.10, 0.10, 0.13), 0, lw=5)
        c.restore()
    c.new_path(); c.restore()
    hx, hy = 398 + 170 * (1 - hin) - 60 * flip, 706
    cut(k, [(560, hy - 122), (hx + 38, hy - 62), (hx + 60, hy + 38), (560, hy + 38)], db.BLAZER, lw=3)
    cut(k, [(hx + 40, hy - 62), (hx + 60, hy + 38), (hx + 46, hy + 44), (hx + 26, hy - 54)], (0.96, 0.96, 0.94), lw=2.4)
    ellipse(k, hx, hy, 44, 36, db.SKIN, 951, lw=3)
    rect(k, hx - 58, hy - 20, 46, 17, db.SKIN, 952, shadow=False, lw=2.6)
    light(k, False)


def a_half(k):
    p = lerp(cb.POSES_SMALL["sit"], cb.POSES_SMALL["finger"], back(seg(0.05, 0.3)))

    def d():
        S.backdrop(k, 0.0, "idle")
        B.small(k, p, "proud", look=(0.7, -0.1))
    B.world(k, "small_say", d)
    B.bubble(k, ["And", "a half."], "small", "R", 34, dy=34)


def a_short(k):
    ln = line_of_shot()
    said = CUR["t"] >= ln["t1"] + 0.1
    arm = lerp(db.POSE_PEN[:2], B.POSE_POINT_L[:2], back(ease((CUR["t"] - ln["t0"]) / 0.22)))

    def d():
        S.backdrop(k, 0.0, "proceed_height" if said else "idle")
        B.sofia(k, "paddle", "neutral", paddle="YES")
        o = B.don(k, arm + B.POSE_POINT_L[2:], "flat", look=(-1.0, 0.7), tense=True)
        p = B.pam(k, pb.pm.ik(-1, -58, pb.BT - 16 + 26 * seg(ln["t1"] - SHOT["s_short"]["t0"] + 0.2, CUR["d"])) + (8, 0),
                  "dip")
        hx, hy = p["hands"][0]
        props.paddle(k, hx, hy - 2, 0.9, -0.10, "YES", 130)
        S.table(k, phone="still")
        props.clipboard(k, o["hands"][1][0] + 2, o["hands"][1][1] - 26, 0.9, 0.08, 91, side="front",
                        marks=1 if said else 0)
        ellipse(k, o["hands"][1][0], o["hands"][1][1] + 8, 10, 10, db.SKIN, 92, shadow=False, lw=2)
        hx, hy = o["hands"][0]
        rect(k, hx - 22, hy - 4, 19, 8, db.SKIN, 94, shadow=False, lw=2)
    B.world(k, "panel", d)
    B.bubble(k, "Too short.", "don", "T", 34)


def a_cross(k):
    B.wood(k)
    drawn = CUR["u"] > 0.3
    props.clipboard(k, 262, 520, 7.0, -0.05, 91, side="front", marks=1 if drawn else 0)
    lift = seg(CUR["d"] * 0.35, CUR["d"])
    wig = 10 * math.sin(CUR["tl"] * 40) if not drawn else 0
    props.ballpen(k, 384 + wig + 60 * lift, 462 + wig + 46 * lift, 5.0, math.pi - 0.62)
    light(k, False)


def a_small_out(k):
    x = 300 - 46 * CUR["u"]
    bob = -4 * abs(math.sin(CUR["tl"] * 7))

    def d():
        S.backdrop(k, 0.6, "proceed_height")
        k.c.save(); k.c.translate(0, bob)
        B.small(k, "hug", "crushed", x=x, seated=False, cv=True, look=(-0.4, 0.8))
        k.c.restore()
    B.world(k, "door", d)


def a_loom(k):
    p = lerp(cb.POSES_MACHO["stand"], cb.POSES_MACHO["wave"], 0.5 + 0.5 * math.sin(CUR["tl"] * 7) * seg(0.1, 0.4))
    rise = 26 * (1 - back(seg(0, 0.35)))                    # he straightens up from under the door frame

    def d():
        S.backdrop(k, 0.0, "idle")
        B.macho(k, p, "smile", feet=S.FEET + rise, glint=CUR["u"] > 0.4)
    B.world(k, "loom", d)


def a_legs(k):
    drop = back(seg(0, 0.22), 2.6)
    cx = X["chair"]

    def d():
        S.backdrop(k, 0.0, "idle", with_chair=drop < 0.5)
        if drop >= 0.5:
            B.bent_chair(k, cx)
        k.c.save(); k.c.translate(0, -34 * (1 - drop))
        B.macho(k, "sit", "smile", seated=True)
        k.c.restore()
        if drop >= 0.5:
            B.ticks(k, [(cx - 92, 690, cx - 108, 682), (cx - 94, 706, cx - 112, 706), (cx + 92, 690, cx + 108, 682),
                        (cx + 94, 706, cx + 112, 706)], 1.6)
            kit.text(k, "creak", cx - 76, 762, 15, INK, font="Permanent Marker", rot=-0.12)
    B.world(k, "legs", d)


def a_pen_goes(k):
    f = seg(0.25, 0.8)

    def d():
        B.panel(k, "idle", so=dict(pose="chest", face="flustered", look=(-1, -0.1), lag=(11 * math.cos(CUR["tl"] * 6), 0)),
                do=False, pa=False)
        x = X["sofia"] - 40 - 62 * f
        y = S.TABLE_TOP - 10 + 150 * f * f
        props.pen(k, x, y, 1.0, 0.4 + 5.0 * f)
    B.world(k, "sofia", d)


def a_boot(k):
    cx = X["chair"]
    f = back(seg(0, 0.36), 1.2)

    def d():
        S.backdrop(k, 0.0, "idle", with_chair=False)
        B.macho(k, "sit", "smile", seated=True)
        x = cx - 78 - 90 * (1 - f)
        props.pen(k, x, S.FEET + 6, 0.8, 0.12 + 6 * (1 - f))
        if f < 0.98:
            B.ticks(k, [(x - 26, S.FEET - 4, x - 18, S.FEET - 1), (x - 30, S.FEET + 12, x - 20, S.FEET + 11)], 0.9)
    B.world(k, "boot", d)


def a_dropped(k):
    p = lerp(cb.POSES_MACHO["stand"], cb.POSES_MACHO["pinch_near"], back(seg(0.05, 0.38)))
    up = seg(0.05, 0.3) > 0.6

    def d():
        S.backdrop(k, 0.0, "idle")
        B.macho(k, "pinch_near" if up else p, "warm", look=(0.9, 0.3), pen=up)
    B.world(k, "loom_say", d)
    B.bubble(k, ["You dropped", "this."], "macho", "R", 26, dy=-44)


def a_thanks(k):
    hin = back(seg(0, 0.3), 1.0)

    def d():
        B.panel(k, "idle", so=dict(pose="aside", face="tiny", look=(-1, -0.8), lag=(-7 * math.cos(CUR["tl"] * 5), 0),
                                   blush=0.7), do=False, pa=False)
        B.macho(k, "pinch_low", "warm", x=X["sofia"] - 292 - 70 * (1 - hin), feet=S.FEET + 96, s=1.3, look=(0.9, 0.6),
                pen=True)
    B.world(k, "sofia", d)
    del B.HEADS["macho"]; B.QA["faces"][:] = [f for f in B.QA["faces"] if f[0] != "macho"]
    B.bubble(k, "Thank you.", "sofia", "T", 32)


def a_chain(k):
    d_ = CUR["d"]
    dl = lerp((-0.4, 0.9), (-1, 0.1), seg(d_ * 0.25, d_ * 0.4))
    pl = lerp((-0.2, 0.4), (-1, 0.0), seg(d_ * 0.5, d_ * 0.65))
    B.world(k, "panel", lambda: B.panel(k, "idle", so=dict(pose="aside", face="smile", look=(-1, -0.4), blush=0.6),
                                        do=dict(face="pout" if CUR["u"] > 0.3 else "flat", look=dl, tense=True, mouth="M"),
                                        pa=dict(pose=pb.POSE_WRITE, face="peer" if CUR["u"] > 0.55 else "neutral", look=pl,
                                                note="KIND" if CUR["u"] > 0.75 else None, pen=True)))


def a_true(k):
    up = back(seg(0.0, 0.2), 2.2)
    sb.POSES["_a"] = lerp(sb.POSES["aside"], sb.POSES["paddle"], up)
    ln = line_of_shot()
    dies = CUR["t"] > ln["t0"] + 0.25
    B.world(k, "sofia_don", lambda: B.panel(k, "idle", so=dict(pose="_a", face="smile", look=(-1, -0.3), paddle="YES",
                                                                blush=0.6),
                                            do=dict(face="drop" if dies else "smug", look=(-1, 0.0), mouth="M" if dies else None),
                                            pa=dict(face="peer")))
    B.bubble(k, "That's so true.", "sofia", "T", 30)


def _push(k, f):
    """f: 0 the paddle is up, 1 his fingertip has pushed it down."""
    sb.POSES["_a"] = lerp(sb.POSES["paddle"], (-12, 24, 74, 104), f)
    S.backdrop(k, 0.0, "proceed_looks" if CUR["t"] > SHOT["s_push"]["t0"] + 0.3 else "idle")
    so = B.sofia(k, "_a", "unimpressed", look=(1, -0.2), paddle="YES")
    px, py = so["hands"][1]                                 # his fingertip rides the paddle's rim all the way down
    o = B.don(k, dm.ik(-1, px + 6.6 - X["don"], py - 99 - S.SEAT) + (8, 0), "flat", look=(-1, -0.3), tense=True,
              board=None)
    B.pam(k, face="peer")
    S.table(k, phone="still")
    hx, hy = o["hands"][0]
    rect(k, hx - 5, hy + 4, 9, 22, db.SKIN, 953, shadow=False, lw=2)
    if 0.05 < f < 0.95:
        B.ticks(k, [(hx - 34, hy + 14, hx - 34, hy + 30), (hx + 30, hy + 14, hx + 30, hy + 30)], 1.6)


def a_push(k):
    B.world(k, "sofia_don", lambda: _push(k, 0.45 * seg(0.9, CUR["d"])))


def a_push_cu(k):
    B.world(k, "paddle", lambda: _push(k, 0.45 + 0.55 * seg(0.05, CUR["d"] * 0.7)))
    B.HEADS.clear(); B.QA["faces"][:] = []


def a_no_worries(k):
    p = lerp(cb.POSES_MACHO["sit"], cb.POSES_MACHO["shrug"], back(seg(0.1, 0.4)))

    def d():
        S.backdrop(k, 0.0, "proceed_looks")
        B.macho(k, p, "gracious", seated=True, look=(0.8, 0.1))
    B.world(k, "macho_say", d)
    B.bubble(k, "No worries.", "macho", "R", 30)


def a_mom_door(k):
    op = 0.35 + 0.55 * seg(0, 0.45)
    xin = seg(0.1, 0.6)

    def d():
        S.backdrop(k, op, "idle", ficus_sway=2.0 * math.sin(CUR["tl"] * 5) * (1 - CUR["u"]))
        B.mom_up(k, X["door"] + 2 + 20 * xin, S.FLOOR_Y + 52 - 3 * abs(math.sin(xin * math.pi * 2)), 0.96, "bag", "sweet")
    B.world(k, "door", d)
    B.bubble(k, ["Good morning,", "everyone."], "mom", "R", 26)


def a_upright(k):
    snap = back(seg(0, 0.2), 3.0)
    flipped = CUR["tl"] > 0.12
    c = k.c

    def d():
        S.backdrop(k, 0.0, "idle")
        B.sofia(k)
        c.save(); c.translate(X["don"], S.SEAT); c.scale(1, 0.93 + 0.07 * snap); c.translate(-X["don"], -S.SEAT)
        B.don(k, db.POSE_HIDE if flipped else db.POSE_PEN, "sheepish", look=(-1, 0.2), board="back" if flipped else "front",
              tense=True)
        c.restore()
        B.pam(k)
        S.table(k, phone="still")
    B.world(k, "don", d)


def a_ageism(k):
    CUR["shake"] = (0, (-1) ** step() * 5) if CUR["tl"] < 0.3 else (0, 0)
    B.world(k, "sofia_don", lambda: B.panel(k, "ageism", so=dict(pose="ask", face="flustered", look=(0.6, -0.9), blush=0.0),
                                            do=dict(pose=db.POSE_HIDE, face="sheepish", look=(-1, 0.2), board="back",
                                                    tense=True), pa=dict()))
    CUR["shake"] = (0, 0)


def a_family(k):
    CUR["shake"] = (0, (-1) ** step() * 4) if CUR["tl"] < 0.25 else (0, 0)
    out = seg(CUR["d"] * 0.55, CUR["d"] * 0.85)
    c = k.c

    def d():
        S.backdrop(k, 0.0, "family")
        B.sofia(k, "fold", "neutral", look=(1, 0))
        c.save(); c.translate(X["don"], S.SEAT); c.scale(1, 1 - 0.035 * out); c.translate(-X["don"], -S.SEAT)
        B.don(k, db.POSE_HIDE, "sheepish", look=(-0.4, 1.0), board="back", tense=out < 0.5)
        c.restore()
        B.pam(k, pb.POSE_ASK, "frozen", pen=True)
        S.table(k, phone="still")
    B.world(k, "don_pam", d)
    CUR["shake"] = (0, 0)


def a_sorry(k):
    snap = back(seg(0, 0.16), 3.0)
    c = k.c

    def d():
        S.backdrop(k, 0.0, "family")
        B.sofia(k)
        c.save(); c.translate(X["don"], S.SEAT); c.scale(1, 0.94 + 0.06 * snap); c.translate(-X["don"], -S.SEAT)
        B.don(k, db.POSE_STRAIGHT, "obey", look=(-1, 0.1), tense=True)
        c.restore()
        B.pam(k)
        S.table(k, phone="buzz")
    B.world(k, "panel", d)
    B.bubble(k, "Sorry.", "don", "T", 30)


def a_pause(k):
    u = CUR["u"]
    B.world(k, "panel", lambda: B.panel(k, "family", so=dict(pose="fold", face="sideeye" if u > 0.72 else "neutral",
                                                              look=(1, 0) if u > 0.72 else (-1, 0)),
                                        do=dict(pose=db.POSE_STRAIGHT, face="obey", look=(-1, 0.1), tense=True),
                                        pa=dict(face="frozen" if u > 0.5 else "neutral", look=(-1, 0)), phone="buzz"))


def a_mom_looks(k):
    lk = lerp((0.9, 0.0), (0.9, 0.9), seg(0.05, 0.25))
    if CUR["u"] > 0.7:
        lk = (0.9, 0.0)
    B._mom(k, "mom_cu", pose="bag", face="stern", look=lk)


def a_phone_hover(k):
    B.wood(k)
    j = (-1) ** step() * 3
    props.phone(k, 244 + j, 440, 3.5, "missed", True, rot=-0.05)
    k.c.new_path()
    near = seg(0.05, CUR["d"] * 0.6) - 0.35 * seg(CUR["d"] * 0.6, CUR["d"] * 0.8) + 0.35 * seg(CUR["d"] * 0.85, CUR["d"])
    hx, hy = 392 + 110 * (1 - near), 762
    cut(k, [(560, hy - 122), (hx + 38, hy - 62), (hx + 60, hy + 38), (560, hy + 38)], db.BLAZER, lw=3)
    cut(k, [(hx + 40, hy - 62), (hx + 60, hy + 38), (hx + 46, hy + 44), (hx + 26, hy - 54)], (0.96, 0.96, 0.94), lw=2.4)
    ellipse(k, hx, hy, 44, 36, db.SKIN, 951, lw=3)
    rect(k, hx - 58, hy - 20, 46, 17, db.SKIN, 952, shadow=False, lw=2.6)
    if step() % 2:
        B.ticks(k, [(hx - 74, hy - 46, hx - 88, hy - 58), (hx - 92, hy - 14, hx - 110, hy - 16), (hx - 76, hy + 20, hx - 92, hy + 30)])
    light(k, False)


def a_answered(k):
    B.wood(k)
    on = CUR["tl"] > 0.12
    props.phone(k, 244, 440, 3.5 * (1 + 0.05 * (1 - seg(0.12, 0.3)) * on), "answered" if on else "missed", not on, rot=-0.05)
    k.c.new_path()
    if on and CUR["tl"] < 0.3:
        k.c.set_source_rgba(0.6, 1.0, 0.7, 0.35 * (1 - seg(0.12, 0.3))); k.c.paint()
    light(k, False)


def a_verdict(k):
    roll = back(seg(0, 0.45), 1.3)
    c = k.c

    def d():
        S.backdrop(k, 0.0, "clear")
        c.save(); c.translate(120 * (1 - roll), 0)
        B.robot(k, "slap_up" if CUR["u"] < 0.82 else "slap")
        c.restore()
        S.table(k, phone=None)
    B.world(k, "robot", d)
    B.bubble(k, ["She made him", "answer the client.", "Hired."], "robot", "T", 22, mono=True)


def a_stamp(k):
    B.wood(k)
    hit = CUR["tl"] >= 0.17
    s = 1.9 * (1 + 1.6 * (1 - ease(CUR["tl"] / 0.17)))
    c = k.c
    j = (-1) ** step() * 6 if hit and CUR["tl"] < 0.42 else 0
    c.save(); c.translate(j, -j)
    if not hit:
        c.push_group(); S.hired_stamp(k, 262, 470, s, -0.07, paper=True); c.pop_group_to_source(); c.paint_with_alpha(0.55)
    else:
        S.hired_stamp(k, 262, 470, 1.9, -0.07, paper=True)
        B.ticks(k, [(70, 320, 44, 300), (470, 330, 496, 312), (60, 640, 34, 660), (478, 630, 504, 652)], 4)
    c.restore()
    light(k, False)


def a_approved(k):
    sag = seg(0.1, 0.5)
    c = k.c

    def d():
        S.backdrop(k, 0.0, "clear")
        B.sofia(k, "fold", "sideeye", look=(1, 0))
        c.save(); c.translate(X["don"], S.SEAT); c.scale(1, 1 - 0.04 * sag); c.translate(-X["don"], -S.SEAT)
        B.don(k, db.POSE_STRAIGHT, "obey", tense=True)
        c.restore()
        B.pam(k, face="frozen")
        S.table(k, phone="still")
    B.world(k, "panel", d)
    B.bubble(k, "…Approved.", "don", "T", 24, kind="small")


def a_leaves(k):
    x = 800 - 150 * ease(CUR["u"])
    bob = -5 * abs(math.sin(CUR["tl"] * 8))

    def d():
        S.backdrop(k, 0.0, "clear")
        B.don_up(k, x, "stand", "sheepish", feet=S.FEET_BACK + bob, look=(-1, 0.1), tense=True)
        B.sofia(k, "fold", "sideeye", look=(1 if x > 700 else 0.2, -0.8))
        B.pam(k, face="frozen")
        S.table(k, phone="still")
        B.ticks(k, [(x + 62, 400, x + 86, 400), (x + 66, 430, x + 94, 430), (x + 62, 460, x + 86, 460)], 3.2)
    B.world(k, "panel", d)


def a_welcome(k):
    arm = lerp((-8, 0, 8, 0), B.POSE_HAND_OUT, back(seg(0.1, 0.4)))
    seen = CUR["u"] > 0.55
    B._two(k, dict(pose=arm, face="sheepish", look=(-1, 0.1), tense=True),
           dict(pose="bag", face="stern" if seen else "sweet", look=(0.9, 0.9) if seen else (0.9, 0.0), bag=True))
    B.bubble(k, "Welcome ab—", "don", "T", 28)


def a_shout(k):
    CUR["shake"] = (0, (-1) ** step() * 6) if CUR["tl"] < 0.5 else (0, 0)        # up and down: sideways would cut the notice
    jump = -10 * math.sin(math.pi * seg(0.08, 0.4))
    B._two(k, dict(pose="stand", face="obey", tense=True, feet=S.FEET + jump),
           dict(pose="hip", face="shout", look=(0.9, 0.4), thrust=0.7, bag=False))
    CUR["shake"] = (0, 0)
    B.bubble(k, "DONNIE! Your vest!", "mom", "T", 32, kind="shout")


def _scrub(k, cam):
    w = 7 * math.sin(CUR["tl"] * 2 * math.pi * 3.0)
    B._two(k, dict(pose="stand", face="obey", tense=True, look=(-1, 0.6) if step() % 12 < 8 else (-0.2, -0.6)),
           dict(pose=mb.wipe_at(B.DON_X - B.MOM_X - 21 + w, db.BT + 96 + w * 0.4), face="stern", look=(0.9, 0.9), bag=False),
           cam)


def a_stain(k):
    _scrub(k, "stain")
    B.HEADS.clear(); B.QA["faces"][:] = []


def a_scrub(k):
    _scrub(k, "reveal")


def a_witnesses(k):
    u = CUR["u"]
    B.world(k, "panel", lambda: B.panel(k, "clear", so=dict(pose="fold", face="deadpan" if u > 0.45 else "sideeye",
                                                             look=(-1, 0)),
                                        do=False, pa=dict(face="approve" if u > 0.25 else "frozen", look=(-1, 0))))


def a_lapel(k):
    d_ = CUR["d"]
    away = seg(0.1, d_ * 0.45)
    yank = back(seg(d_ * 0.55, d_ * 0.7), 2.4)
    lean = 9 * away * (1 - yank)
    B._two(k, dict(pose="stand", face="obey", tense=True, lean=lean, look=(1, 0.2) if yank < 0.5 else (-1, 0.4)),
           dict(pose=mb.wipe_at(B.DON_X - B.MOM_X - 14 + lean * 2.2, db.BT + 60), face="stern", look=(0.9, 0.9), bag=False))


def a_tilt(k):
    r = 0.13 * back(seg(0, 0.3), 1.4)
    cam = S.CAMS["tilt"]
    B._two(k, dict(pose="stand", face="panic", tense=True, look=(-1, 0)),
           dict(pose="hip", face="unimpressed", look=(0.9, 0.2), bag=False),
           (cam[0], cam[1], cam[2] * (0.9 + 0.1 * seg(0, 0.3)), r))


ANIM = {"s_door": a_door, "s_door_end": a_door_end, "s_phone47": a_phone47, "s_half": a_half, "s_short": a_short,
        "s_cross": a_cross, "s_small_out": a_small_out, "s_loom": a_loom, "s_legs": a_legs, "s_pen_goes": a_pen_goes,
        "s_boot": a_boot, "s_dropped": a_dropped, "s_thanks": a_thanks, "s_chain": a_chain, "s_true": a_true,
        "s_push": a_push, "s_push_cu": a_push_cu, "s_no_worries": a_no_worries, "s_mom_door": a_mom_door,
        "s_upright": a_upright, "s_ageism": a_ageism, "s_family": a_family, "s_sorry": a_sorry, "s_pause": a_pause,
        "s_mom_looks": a_mom_looks, "s_phone_hover": a_phone_hover, "s_answered": a_answered, "s_verdict": a_verdict,
        "s_stamp": a_stamp, "s_approved": a_approved, "s_leaves": a_leaves, "s_welcome": a_welcome, "s_shout": a_shout,
        "s_stain": a_stain, "s_scrub": a_scrub, "s_witnesses": a_witnesses, "s_lapel": a_lapel, "s_tilt": a_tilt}
STATIC = {s[4].__name__: s[4] for s in B.SHOTS}
ONSET = {"s_short", "s_push", "s_ageism", "s_family", "s_approved"}
NO_PUSH = {"s_door", "s_door_end", "s_eyes_jealous", "s_eyes_afraid", "s_tilt", "s_push_cu", "s_stain",
           "s_true", "s_distracting", "s_whom", "s_five", "s_family_q", "s_family", "s_push", "s_ageism"}   # a sign at the edge


def shot_at(t):
    for s in T["shots"]:
        if s["t0"] - 1e-9 <= t < s["t0"] + s["d"] - 1e-9:
            return s
    return T["shots"][-1]


def draw(c, t_raw, w=540, x=0, y=0, last=False):
    """One drawing at time t_raw (seconds), into a w-wide box."""
    t = math.floor(t_raw * 12 + 1e-6) / 12.0
    s = shot_at(t)
    CUR.update(t=t, tl=t - s["t0"], d=s["d"], u=(t - s["t0"]) / s["d"], name=s["name"], push=PUSH.get(s["name"], 0.0),
               shake=(0, 0))
    if CUR["tl"] < 1e-6:
        CUR["mon"] = None                                  # a cut: the monitor's glow starts again
    boil = 0 if last else int(round(t * 12)) % 3
    c.save(); c.translate(x, y); c.scale(w / 540.0, w / 540.0)
    c.rectangle(0, 0, 540, 960); c.clip()
    m = c.get_matrix(); m.invert(); B._BASE[0] = m
    B.HEADS.clear()
    for v in B.QA.values():
        v[:] = []
    c.set_source_rgb(*kit.WALL); c.paint()
    k = kit.Ctx(c, boil)
    (ANIM.get(s["name"]) or STATIC[s["name"]])(k)
    kit.grain(k, 0.05)
    c.restore()
    return s


def still(t, w=540, last=False):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, w * 16 // 9)
    draw(cairo.Context(surf), t, w, last=last)
    surf.flush()
    return surf


def safe_pushes():
    """A shot may push in only as far as no sign in it gets cut and its bubble rules still hold."""
    import qa_bc_anim_v2 as qa_bc
    for s in T["shots"]:
        if s["name"] in NO_PUSH:
            PUSH[s["name"]] = 0.0
            continue
        for p in (0.035, 0.02, 0.0):
            PUSH[s["name"]] = p
            te = s["t0"] + s["d"] - 1 / 12
            if not qa_bc.check(("--", 0, 0, 0, lambda k, te=te: _qa_draw(k, te))):
                break
    json.dump(PUSH, open(os.path.join(HERE, "bc_push_v2.json"), "w"), indent=1)
    return PUSH


def _qa_draw(k, t):
    """qa_bc.check draws through B.frame; put the animated drawing for time t inside it."""
    s = shot_at(t)
    CUR.update(t=t, tl=t - s["t0"], d=s["d"], u=(t - s["t0"]) / s["d"], name=s["name"], push=PUSH.get(s["name"], 0.0),
               shake=(0, 0))
    if CUR["tl"] < 1e-6:
        CUR["mon"] = None
    (ANIM.get(s["name"]) or STATIC[s["name"]])(k)


def load_pushes():
    p = os.path.join(HERE, "bc_push_v2.json")
    PUSH.update(json.load(open(p)) if os.path.exists(p) else safe_pushes())


def qa():
    import qa_bc_anim_v2 as qa_bc
    bad, n = 0, 0
    t = 0.0
    while t < DURATION - 1e-6:
        tq = math.floor(t * 12 + 1e-6) / 12.0
        for line in qa_bc.check(("--", 0, 0, 0, lambda k, tq=tq: _qa_draw(k, tq))):
            bad += 1
            print("%6.2f s  %-15s %s" % (tq, shot_at(tq)["name"], line))
        n += 1
        t += 1 / 3
    print("checked %d frames of %.1f s: %s" % (n, DURATION, "%d problems" % bad if bad else "clean"))
    return bad


def render_section(sec, w, path):
    """One encoded file for one section: 30 fps out, a new drawing 12 times a second."""
    shots = [s for s in T["shots"] if s["sec"] == sec]
    f0, f1 = int(round(shots[0]["t0"] * FPS)), int(round((shots[-1]["t0"] + shots[-1]["d"]) * FPS))
    h = w * 16 // 9
    tmp = path + ".part.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{w}x{h}",
                          "-r", str(FPS), "-i", "-", "-vf", "scale=out_color_matrix=bt709", "-c:v", "libx264",
                          "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p", "-colorspace", "bt709",
                          "-color_primaries", "bt709", "-color_trc", "bt709", "-an", tmp], stdin=subprocess.PIPE)
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    c = cairo.Context(surf)
    prev, buf = None, None
    nlast = int(round(DURATION * FPS)) - 1
    for f in range(f0, f1):
        key = int(math.floor(f / FPS * 12 + 1e-6))
        last = key == int(math.floor(nlast / FPS * 12 + 1e-6))
        if key != prev:
            draw(c, f / FPS, w, last=last)
            surf.flush(); buf = bytes(surf.get_data()); prev = key
        p.stdin.write(buf)
    p.stdin.close()
    if p.wait() != 0:
        raise SystemExit("ffmpeg failed on section %d" % sec)
    os.replace(tmp, path)


def render(out, w=540):
    from multiprocessing import Pool
    tmp = "/tmp/bc_anim_%d" % w
    os.makedirs(tmp, exist_ok=True)
    secs = sorted({s["sec"] for s in T["shots"]})
    jobs = [(sec, w, os.path.join(tmp, "sec%d.mp4" % sec)) for sec in secs]
    with Pool(min(4, len(jobs))) as pool:
        pool.starmap(render_section, jobs)
    lst = os.path.join(tmp, "list.txt")
    open(lst, "w").write("".join("file '%s'\n" % j[2] for j in jobs))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy",
                    "-movflags", "+faststart", out], check=True)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "timing"
    if cmd == "timing":
        json.dump(T, open(os.path.join(HERE, "bc_timing.json"), "w"), indent=1)
        for s in T["shots"]:
            print("%s %-16s %6.2f  %.2f" % (s["id"], s["name"], s["t0"], s["d"]))
        print("total %.2f s, %d lines" % (T["total"], len(T["lines"])))
    elif cmd == "pushes":
        print(safe_pushes())
    else:
        load_pushes()
        if cmd == "stills":
            for a in sys.argv[3:]:
                still(float(a)).write_to_png(os.path.join(sys.argv[2], "bc_anim_%07.2f.png" % float(a)))
        elif cmd == "qa":
            sys.exit(1 if qa() else 0)
        elif cmd == "render":
            render(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 540)
