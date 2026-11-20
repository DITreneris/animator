"""FIRST SEARCH (episode 10): film v4 (19 Nov), from the director's notes and the cold test of film v3 (two fresh viewers
got the joke; both lost the thread at 8-16 s and in Mom's act, and listed some twenty drawing faults). fs_film2.py
(films v2 and v3) is kept. Picked by /grill-me:

- the opening: the Client walks in, the door slams, THEN the portrait drops and hits Don on the head (it stays there,
  crooked; stars; he sags); the Client comes empty-handed (his roll was shredded in episode 9);
- 8-16 s: the screen goes red (an insert), Don takes fright (no silent shouting), "It found nothing.", and Sofía on the
  chair sticks the plaster on (that shot had fallen out of v3, and its bubble ran 0.9 s late);
- Mom's act: her mug is back (WORLD'S BEST MOM); one "Eww."; the thumb scrub is in the open; her arms are redrawn
  (round elbows, cuffs, hands with a thumb);
- the plan: Pam shows the Client the plan taped together WRONG; he is furious (he comes back angry in episode 11);
  the rescue at the shredder is out;
- bubbles are placed again when the drawing changes; "Garage eleven" is no longer on the portrait; frame 0 and the last
  frame are the same room.

One timeline in the film's own order (fs_timing_film4.json); the voices, effects and theme A follow it.

  python3 fs_film4.py [dir] [540|1080]   -> fs_film4_540.mp4 / fs_film4_1080.mp4
"""
import os
import sys
import json
import math
import shutil
import subprocess
import numpy as np
import soundfile as sf
import cairo
import kit
from kit import Ctx, INK, ellipse
import fs_storyboard as sb
import fs_animatic as an
import fs_anim as fa
import fs_film2 as f2
import sound_xmas as sx
import sound_iwry as si
import sound_bc_mix as bm
import sound_ob_mix as om
import sound_fs_music as mus
import client_ob as co
import mom_fs as mfs
import mom_bc
import mom_on
import acts_ob as ac

HERE = os.path.dirname(os.path.abspath(__file__))
W, H, DR = 540, 960, 15
SR = an.SR
F = sb.F
VOICES, LEAD = "fs_voices/film_v10", 0.15
ease = f2.ease

# ---------------------------------------------------------------- the shot list: (shot, [(key, drawing, seconds or None)])
A_LEN = 4.6
LIST = [
    ("A", [("1.1a", "open", A_LEN)]),
    ("B", [("1.2", "1.2", 1.6), ("1.3", "1.3", 1.4)]),
    ("C", [("2.1", "2.2", None), ("2.2", "2.2", None), ("2.3", "2.2", None)]),
    ("D", [("3.2", "3.2", None)]),
    ("E0", [("3.1", "red", 0.8)]),
    ("E", [("3.1b", "fright", 0.8), ("3.3", "3.3", None)]),
    ("E2", [("3.4", "3.4", None)]),
    ("F", [("4.1", "4.1", None), ("4.2", "4.1", None), ("4.3", "4.1", None), ("4.4", "4.1", None)]),
    ("G", [("4.5", "4.5", None)]),
    ("H", [("5.1", "5.1", 1.3), ("5.2", "5.1", None)]),
    ("I", [("5.2b", "5.2b", None)]),
    ("J", [("5.2c", "memory", 0.9)]),
    ("K", [("5.3", "5.3", None)]),
    ("L", [("6.1b", "momdesk", None)]),
    ("M", [("6.2a", "6.2a", 1.0), ("6.2b", "6.2b", None)]),
    ("N", [("7.1", "7.1", None)]),
    ("O", [("7.2", "7.2", None), ("7.3", "7.3", None)]),
    ("P", [("7.4", "7.4", None)]),
    ("Q", [("7.5", "7.5", None)]),
    ("Q2", [("8.1", "8.1", None)]),
    ("R", [("8.2", "show", 1.1), ("8.3", "fury", 1.0)]),
    ("S", [("9.1", "9.1", None)]),
    ("T", [("9.2", "9.2", None)]),
    ("U", [("9.3", "9.3", None), ("9.4", "9.4", None), ("9.5", "9.5", None)]),
]
SHARE = {"E": "3.3", "F": "4.1", "H": "5.1"}               # one camera for the shot: this drawing's
CAMD = {"5.1": (275, 690, 2.0), "momdesk": (846, 628, 3.2), "7.2": (565, 610, 2.0), "7.4": (392, 640, 1.9),
        "show": (400, 668, 2.3), "fury": (400, 668, 2.3), "2.2": (352, F - 190, 2.1)}
MOVES = {"B", "C", "F", "O", "U"}
EXTRA = {"1.2": {"card": True}, "5.2": {"cl_look": (1, -0.2), "cl_face": "suspicious"}, "5.1": {"cl_face": "puzzled"}}
STATE = {"open": "1.1a", "red": "3.1", "fright": "3.3", "memory": "5.2c", "momdesk": "6.1b", "show": "8.2",
         "fury": "8.2"}                                    # whose board state (portrait, sleeves, hair) a new drawing has
CUR_T = f2.CUR_T
TALK = f2.TALK
FORCE = f2.FORCE

# ---------------------------------------------------------------- the opening
T_OPEN, T_IN, T_SHUT, T_SLAM = 1.5, 1.7, 2.2, 2.5
T_BACK0, T_BACK1 = 2.6, 3.5
T_DROP0, T_DROP1 = 3.60, 3.74
DOOR_CAM = f2.DOOR_CAM


def opening(k):
    """Don under the portrait (frame 0); the camera eases to the door; the Client walks in (empty-handed); the door
    slides shut and slams; the wall shakes; back to Don, the portrait trembling; it drops onto his head: he sags, stars,
    and it stays there, crooked."""
    t = CUR_T[0]
    v = ease((t - 0.5) / 1.0) - ease((t - T_BACK0) / (T_BACK1 - T_BACK0))
    cam = tuple(a + (b - a) * v for a, b in zip(sb.WIDE27, DOOR_CAM))
    sh = 7 * math.sin(2 * math.pi * 13 * (t - T_SLAM)) * math.exp(-(t - T_SLAM) * 5) if t > T_SLAM else 0.0
    if t > T_DROP1:
        sh += 9 * math.sin(2 * math.pi * 12 * (t - T_DROP1)) * math.exp(-(t - T_DROP1) * 7)
    FORCE[0] = (cam[0] + sh / cam[2], cam[1] + 0.5 * sh / cam[2], cam[2])
    op = 0.85 * ease((t - T_OPEN) / 0.25) - 0.85 * ease((t - T_SHUT) / (T_SLAM - T_SHUT))
    wob = 0.10 * math.sin(2 * math.pi * 5 * (t - T_SLAM)) * math.exp(-(t - T_SLAM) * 0.8) if t > T_SLAM else 0.0
    s_p = sb.fs.PORTRAIT_S * 0.88
    hit = t >= T_DROP1
    sag = 20 * math.exp(-(t - T_DROP1) * 5) * abs(math.cos(2 * math.pi * 2.2 * (t - T_DROP1))) + 5 if hit else 0

    def ex(k_, o):
        c_ = k_.c
        hx, hy = o["don"]["head"]
        r = 50 * sb.SC["don"]
        px0, py0 = sb.PORT27
        if t < T_DROP0:                                     # on its nail: a hop on the slam, then trembling
            up = -10 * math.exp(-(t - T_SLAM) * 9) if t > T_SLAM else 0
            sb.fs.portrait(k_, px0, py0 + up, s_p, ang=wob, crack=False, patch=False)
        else:
            u = min(1.0, (t - T_DROP0) / (T_DROP1 - T_DROP0))
            y_end = hy - r - 99 * 0.88 + 16                 # its bottom edge on his scalp
            x_ = px0 + (hx - 14 - px0) * u
            y_ = py0 + (y_end - py0) * u * u
            sb.fs.portrait(k_, x_, y_, s_p, ang=0.30 * u + (0.05 * math.sin(2 * math.pi * 6 * (t - T_DROP1)) *
                                                           math.exp(-(t - T_DROP1) * 4) if hit else 0),
                           crack=hit, patch=False)
        if hit:
            if t < T_DROP1 + 0.2:
                sb.lines(c_, hx, hy - r, 9, 46, 78, 200, 340)                    # the impact
            sb.stars(c_, hx, hy - 6, 58, 5, t * 7)                             # round his head
    sb.V32[0] = False                                       # frame 0's room (as the last frame's)
    try:
        sb.scene(k, screen="query", portrait=None, door=max(0.0, op), rb=dict(x4=True, state="eager"),
                 cl=False if t < T_IN else dict(x4=True, x=70 + 90 * ease((t - T_IN) / 0.7),
                                                feet=F - 14 - (4 * abs(math.sin(math.pi * 3 * ease((t - T_IN) / 0.7)))
                                                               if T_IN < t < T_IN + 0.7 else 0),
                                                pose="arrive", face="confident", look=(1, 0) if t < T_SLAM else (1, -0.4)),
                 sf=False if t < 0.9 else dict(x4=True, face="charm", look=(-1, 0)),
                 dn=dict(x4=True, feet=F + 16 + sag, face="shock" if hit else "happy", look=(0, -1) if hit else (0, 0)),
                 extra=ex)
    finally:
        sb.V32[0] = True


# ---------------------------------------------------------------- new drawings
def red(k):
    """E0, an insert: the search runs again: 0 RESULTS, red, buzzing."""
    c = k.c
    sb.bg(c)
    t = CUR_T[0]
    j = 4 * math.sin(2 * math.pi * 16 * t)
    sb.fs.screen(k, "red", 40 + j, 300, 460, 290, cursor=False)
    c.set_source_rgb(*INK); c.set_line_width(4); c.set_line_cap(1)
    for sx_ in (-1, 1):
        for i in range(3):
            c.new_path(); c.arc(270 + sx_ * 250, 445, 40 + i * 16, -0.5 if sx_ > 0 else math.pi - 0.5,
                                0.5 if sx_ > 0 else math.pi + 0.5); c.stroke()


def fright(k):
    """E: the red is on them: Don takes fright (his hands to his head, eyes on the screen), Sofía looks at it too."""
    sb.scene(k, cam=(262, 590, 2.3), sf=dict(face="drop", look=(-1.2, -0.3)),
             dn=dict(face="panic", pose="panic", look=(-1, -0.5)), cl=False, rb=False)


def memory(k):
    """J: last week (episode 9): the roll going into the shredder."""
    sb.f_m52c(k)
    c = k.c
    kit.text(k, "LAST WEEK", 300, 122, 34, (1, 1, 1))
    c.save(); c.translate(388, 300); c.rotate(-0.08)
    kit.rect(k, -86, -24, 172, 48, (0.98, 0.97, 0.94), 1400, shadow=False, lw=2.4)
    c.restore()
    kit.text(k, "MY GARAGES", 388, 300, 24, (0.10, 0.20, 0.55))


def momdesk(k):
    """L: Mom at her desk: her nameplate and her mug (WORLD'S BEST MOM). "Machines." """
    def ex(k_, o):
        mfs.mug(k_, 902, F - 198, 0.6)
    sb.scene(k, mm=dict(face="glare", look=(-1.2, 0.4), chin=True, feet=F - 112), pm=False, cl=False, rb=False, sf=False,
             dn=False, extra=ex)


_PLAN = [None]


def wrong_plan(k, x, y, s):
    """The plan taped together wrong: its five strips out of order, one upside down, crooked."""
    if _PLAN[0] is None:
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 400, 400); surf.set_device_scale(2, 2)
        sb.fs.plan_taped(Ctx(cairo.Context(surf), 0), 100, 100, 1.0)
        a = np.frombuffer(surf.get_data(), np.uint8).reshape(400, 400, 4)[:, :, 3]
        ys, xs = np.where(a > 0)
        _PLAN[0] = (surf, xs.min() / 2.0, ys.min() / 2.0, xs.max() / 2.0, ys.max() / 2.0)
    surf, x0, y0, x1, y1 = _PLAN[0]
    c = k.c
    w = (x1 - x0) / 5.0; h = y1 - y0
    c.save(); c.translate(x, y); c.scale(s, s); c.translate(-(x1 - x0) / 2.0, -h / 2.0)
    for i, (j, flip, dy, rot) in enumerate(((3, False, -5, -0.05), (0, True, 6, 0.04), (4, False, -2, 0.07),
                                            (1, False, 8, -0.06), (2, True, -6, 0.03))):
        c.save(); c.translate(i * w + w / 2, h / 2 + dy); c.rotate(rot)
        if flip:
            c.scale(1, -1)
        c.rectangle(-w / 2, -h / 2, w, h); c.clip()
        c.set_source_surface(surf, -w / 2 - (x0 + j * w), -h / 2 - y0); c.paint()
        c.restore()
        c.save(); c.translate(i * w + w / 2, h / 2 + dy); c.rotate(rot)
        c.set_source_rgb(*INK); c.set_line_width(1.6); c.rectangle(-w / 2, -h / 2, w, h); c.stroke()
        c.restore()
    for i in range(1, 5):                                  # tape over every seam, anyhow
        c.save(); c.translate(i * w, h * (0.3 if i % 2 else 0.7)); c.rotate(0.5 if i % 2 else -0.4)
        c.set_source_rgba(0.98, 0.95, 0.80, 0.95); c.rectangle(-16, -5, 32, 10); c.fill()
        c.set_source_rgb(0.55, 0.48, 0.30); c.set_line_width(1.2); c.rectangle(-16, -5, 32, 10); c.stroke()
        c.restore()
    c.restore()


def _show(k, furious):
    t = CUR_T[0]

    def ex(k_, o):
        c = k_.c
        ps = sb.SC["pam"]
        px, pf = 474, F + 10
        sb.fd.shadow(k_, px, pf + 2, 40)
        ac.pam(k_, px, pf, ps, "stand", look=(-1, -0.2), hands=((-110, -270), (-30, -270)))
        j = 3 * math.sin(2 * math.pi * 9 * t) if furious else 0
        wrong_plan(k_, px - 62 + j, pf - 196, 0.78)
        hx, hy = o["client"]["head"]
        r = 50 * 0.52
        if furious:
            c.set_source_rgba(0.90, 0.10, 0.10, 0.30)                              # he goes red
            c.new_path(); c.arc(hx, hy, r * 1.05, 0, 2 * math.pi); c.fill()
            c.set_source_rgb(0.85, 0.10, 0.12); c.set_line_width(3); c.set_line_cap(1)   # the vein
            vx, vy = hx - 14, hy - r - 4
            for a in range(4):
                ang = a * math.pi / 2 + 0.4
                c.new_path(); c.arc(vx + 7 * math.cos(ang), vy + 7 * math.sin(ang), 5, ang + 2.2, ang + 4.1); c.stroke()
            c.set_source_rgb(1, 1, 1)                                               # steam
            for i, (dx, rr) in enumerate(((-30, 9), (-40, 12), (28, 9), (38, 12))):
                yy = hy - r - 6 - (i % 2) * 14 - 10 * ((t * 2 + i * 0.3) % 1)
                c.new_path(); c.arc(hx + dx, yy, rr * 0.7, 0, 2 * math.pi)
                c.set_source_rgb(1, 1, 1); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.6); c.stroke()
    sb.scene(k, cl=dict(x4=True, x=330, feet=F + 10, face="suspicious" if furious else "dawning",
                        look=(1, 0.0) if furious else (1, 0.3), pose="stand"),
             pm=False, mm=False, sf=False, dn=False, rb=False, counter_plan=False, extra=ex)


def show(k):
    _show(k, False)


def fury(k):
    _show(k, True)


# ---------------------------------------------------------------- Mom's arms (the director: "very bad"): round elbows,
# a cuff, a hand with a thumb, turned the way the forearm goes
def mom_arm(k, sx, sy, a1, a2, col, skin, seed, ln=48, w=17):
    c = k.c
    d = lambda a: (math.sin(math.radians(a)), math.cos(math.radians(a)))
    ex, ey = sx + d(a1)[0] * ln, sy + d(a1)[1] * ln
    hx, hy = ex + d(a1 + a2)[0] * ln, ey + d(a1 + a2)[1] * ln
    fx, fy = d(a1 + a2)
    wx, wy = ex + fx * ln * 0.80, ey + fy * ln * 0.80          # the wrist
    c.set_line_join(cairo.LINE_JOIN_ROUND); c.set_line_cap(cairo.LINE_CAP_ROUND)
    for colr, lw in ((INK, w + 4.5), (col, w)):
        c.set_source_rgb(*colr); c.set_line_width(lw)
        c.new_path(); c.move_to(sx, sy); c.line_to(ex, ey); c.line_to(wx, wy); c.stroke()
    c.set_line_cap(cairo.LINE_CAP_BUTT)
    for colr, lw in ((INK, w + 7), (mfs.CREAM, w + 2.5)):       # the cuff
        c.set_source_rgb(*colr); c.set_line_width(lw)
        g = 1.2 if colr == INK else 0
        c.new_path(); c.move_to(wx - fx * (3 + g), wy - fy * (3 + g)); c.line_to(wx + fx * (3 + g), wy + fy * (3 + g))
        c.stroke()
    ang = math.atan2(fy, fx)
    c.save(); c.translate(hx, hy); c.rotate(ang)
    side = 1 if (fx * 1 - fy * 0) >= 0 else -1
    c.new_path(); c.save(); c.translate(-2, -8.5 * side); c.rotate(-0.5 * side); c.scale(5.5, 3.6)   # the thumb
    c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    c.set_source_rgb(*skin); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2); c.stroke()
    c.new_path(); c.save(); c.scale(12.5, 9.5); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()            # the palm
    c.set_source_rgb(*skin); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2); c.stroke()
    c.set_line_width(1.3); c.set_line_cap(cairo.LINE_CAP_ROUND)                                         # the fingers
    for dy in (-3.4, 0, 3.4):
        c.new_path(); c.move_to(5.5, dy); c.line_to(11, dy * 0.9); c.stroke()
    c.restore()
    return hx, hy


class _mom_arms:
    def __enter__(self):
        self.m = mfs.mom
        m0 = self.m
        g = mfs._body.__globals__

        def mom(*a, **kw):
            old = (kit.arm, mom_bc._hand, g.get("_hand"), mom_on._hand)
            kit.arm = mom_arm
            noop = lambda *a_, **kw_: None
            mom_bc._hand = noop; mom_on._hand = noop
            if "_hand" in g:
                g["_hand"] = noop
            try:
                return m0(*a, **kw)
            finally:
                kit.arm, mom_bc._hand, mom_on._hand = old[0], old[1], old[3]
                if old[2] is not None:
                    g["_hand"] = old[2]
        mfs.mom = mom
        return self

    def __exit__(self, *e):
        mfs.mom = self.m


class _no_roll:
    """The Client comes empty-handed: his roll was shredded last week."""
    def __enter__(self):
        self.c = co.client
        c0 = self.c
        co.client = lambda *a, **kw: c0(*a, **dict(kw, roll=False))
        return self

    def __exit__(self, *e):
        co.client = self.c


# ---------------------------------------------------------------- the camera inside a shot, the overlays
def move(shot, t, ln, hl, anch, port):
    if shot == "A":
        return (270, 480, 1.0)
    if shot == "B" and "card" in anch.get("1.2", {}) and t < 1.6:
        cx, cy, w = anch["1.2"]["card"]
        v = ease((t - 0.6) / 1.0)
        return (270 + (cx - 270) * 0.5 * v, 480 + (cy - 480) * 0.5 * v, 1 + 0.35 * v)
    if shot == "C" and hl.get("don") and t < 1.0:
        h = hl["don"]
        v = 1 - ease((t - 0.45) / 0.55)
        return (270 + (h[0] - 270) * v, 480 + (h[1] + 30 - 480) * v, 1 + 0.8 * v)
    if shot == "F" and hl.get("robot") and t > ln - 0.55:
        h = hl["robot"]
        v = ease((t - (ln - 0.55)) / 0.5)
        return (270 + (h[0] - 270) * v, 480 + (h[1] + 1.4 * h[2] - 480) * v, 1 + 1.0 * v)
    if shot == "O" and hl.get("mom") and 0.55 <= t < 0.9:
        h = hl["mom"]
        v = ease((t - 0.55) / 0.35)
        return (270 + (h[0] - 270) * v, 480 + (h[1] - 480) * v, 1 + 1.2 * v)
    if shot == "U" and port and 1.2 <= t < 2.6:
        v = 1 - ease((t - 1.2) / 1.4)
        return (270 + (port[0] - 270) * v, 480 + (port[1] - 480) * v, 1 + 1.6 * v)
    return (270, 480, 1 + 0.03 * t / ln)


def overlay(shot, key, tb, c, tf, hl, anch):
    if shot == "C" and key == "2.3" and "tablet" in anch.get("2.2", {}):
        x, y, w = anch["2.2"]["tablet"]
        x, y = tf(x, y)
        v = ease(tb / 0.35)
        sb.thumb(Ctx(c, 0), x + 30, y + 40 + 260 * (1 - v), 0.9, sb.SKIN_CL, oil=True, ang=2.55, who="client")
    if shot == "F" and key in ("4.3", "4.4") and hl.get("robot"):
        h = hl["robot"]
        if key == "4.3" and tb < 0.45:
            return
        x, y = tf(h[0], h[1] + 2.0 * h[2])
        z = tf(1, 0)[0] - tf(0, 0)[0]
        sw, sh = 1.7 * h[2] * z, 0.5 * h[2] * z
        c.set_source_rgb(0.12, 0.13, 0.16); c.rectangle(x - sw / 2 - 4, y - sh / 2 - 4, sw + 8, sh + 8); c.fill()
        c.set_source_rgb(0.20, 0.72, 0.40); c.rectangle(x - sw / 2, y - sh / 2, sw, sh); c.fill()
        c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        c.set_font_size(sh * 0.5); e = c.text_extents("APPROVED")
        c.set_source_rgb(1, 1, 1); c.move_to(x - e.x_advance / 2, y + e.height / 2); c.show_text("APPROVED")


# ---------------------------------------------------------------- the build
def timeline(d):
    old = {r["shot"]: r["len"] for r in json.load(open(os.path.join(d, "fs_timing_v26.json")))}
    rows, t = [], 0.0
    for shot, beats in LIST:
        for key, drawing, ln in beats:
            ln = old[key] if ln is None else ln
            rows.append(dict(shot=key, start=round(t, 3), len=round(ln, 3), of=shot, drawing=drawing))
            t += ln
    return rows, t


def build(d, S=1, music="A"):
    import sound_bc as bc
    an.VOICES = VOICES
    an.TAKES = json.load(open(os.path.join(HERE, VOICES, "takes.json")))
    an.SPEAKER["PAM+SOFIA"] = ["sofia"]                     # one "Eww." bubble (two voices)
    for kk, vv in (("5.1", "portrait"), ("2.2", "portrait"), ("8.2", "shredder"), ("8.2", "portrait")):
        sb.DROP32.setdefault(kk, set()).add(vv)
    rows, total = timeline(d)
    json.dump(rows, open(os.path.join(d, "fs_timing_film4.json"), "w"), indent=1)
    row = {r["shot"]: r for r in rows}
    fns = {s: fn for s, _, fn, _ in sb.SHOTS}
    for name, fn in (("open", opening), ("red", red), ("fright", fright), ("memory", memory), ("momdesk", momdesk),
                     ("show", show), ("fury", fury)):
        fns[name] = sb._with_state(STATE[name], fn)
    lines_abs = []
    voice = np.zeros(int((total + 1) * SR))
    for r in rows:
        s = r["shot"]
        if s in an.LINE_OF:
            m = an.TAKES[an.LINE_OF[s]]
            a, _ = sf.read(os.path.join(HERE, VOICES, "%s.wav" % an.LINE_OF[s]))
            a = a.mean(1) if a.ndim > 1 else a
            t0 = r["start"] + LEAD
            an._at(voice, a, t0, 1.0)
            vis = bc.visemes(np.asarray(a, dtype=np.float64), m["text"]) if m["who"] != "ROBOT" else []
            lines_abs.append((m["who"], m["text"], t0, t0 + m["len"], vis))
    out_dir = "/tmp/fs_film4_%d" % (540 * S)
    shutil.rmtree(out_dir, ignore_errors=True); os.makedirs(out_dir)
    anch = {}

    def draw(drawing, key, tb, ln, shared, S_, Z):
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(W * S_ * Z), int(H * S_ * Z)); surf.set_device_scale(S_ * Z, S_ * Z)
        c = cairo.Context(surf); k = Ctx(c, 0)
        sb.bg(c)
        sb.ANIM.clear(); sb.ANIM.update(fa.motion_all(drawing, tb, ln)); sb.ANIM.update(EXTRA.get(key, {}))
        if drawing == "7.4":
            sb.ANIM["shudder"] = sb.ANIM.get("shudder", 0) - 60
        FORCE[0] = CAMD.get(drawing) or shared
        CUR_T[0] = tb
        sb.HEADS.clear(); sb.AVOID.clear(); f2.ANCH.clear()
        with sb._norm(record_only=True):
            fns[drawing](k)
        anch.setdefault(drawing, {}).update(f2.ANCH)
        FORCE[0] = None
        return surf, dict(sb.HEADS), list(sb.AVOID)

    n = 0
    with f2._forced(), f2._anchors(), f2._mouths(), _mom_arms(), _no_roll():
        for shot, beats in LIST:
            t0s = row[beats[0][0]]["start"]
            ln_s = sum(row[b[0]]["len"] for b in beats)
            TALK.clear(); anch.clear()
            shared = None
            if shot in SHARE:
                draw(SHARE[shot], SHARE[shot], 0.0, 1.0, None, 1, 1)
                shared = sb.LASTCAM[0]
            _, hl, _ = draw(beats[0][1], beats[0][0], 0.0, row[beats[0][0]]["len"], shared, 1, 1)
            for key, drawing, _ in beats[1:]:
                draw(drawing, key, 0.0, row[key]["len"], shared, 1, 1)
            port = None
            if shot == "U":
                p = sb.PORT27
                port = (270 + (p[0] - sb.WIDE27[0]) * sb.WIDE27[2], 480 + (p[1] - sb.WIDE27[1]) * sb.WIDE27[2])
            local = [(w, tx, a - t0s, b - t0s, e) for w, tx, a, b, e in lines_abs if a < t0s + ln_s and b + 0.25 > t0s]
            bub = {}
            Z = 3 if shot in MOVES else 1
            for j in range(int(round(ln_s * DR))):
                t = j / DR
                acc = 0.0
                for key, drawing, _ in beats:
                    if t < acc + row[key]["len"] - 1e-6 or key == beats[-1][0]:
                        break
                    acc += row[key]["len"]
                tb = t - acc
                TALK.clear()
                for who, text, a0, a1, vis in local:
                    if a0 - 0.1 <= t < a1 + 0.05:
                        for nm in f2.WHO2.get(who, []):
                            TALK[nm] = f2._vis(vis, int((t - a0) * 12) + 1) or "M"
                surf_b, heads, avoid = draw(drawing, key, tb, row[key]["len"], shared, S, Z)
                fx, fy, z = move(shot, t, ln_s, hl, anch, port)
                out = cairo.ImageSurface(cairo.FORMAT_RGB24, W * S, H * S); out.set_device_scale(S, S)
                c0 = cairo.Context(out)
                sb.bg(c0)
                c0.save(); c0.translate(270, 480); c0.scale(z, z); c0.translate(-fx, -fy)
                pat = cairo.SurfacePattern(surf_b); pat.set_filter(cairo.FILTER_GOOD)
                c0.set_source(pat); c0.paint(); c0.restore()
                tf = lambda x, y: ((x - fx) * z + 270, (y - fy) * z + 480)
                heads_t = {nm: tf(x, y) + (r * z,) for nm, (x, y, r) in heads.items()}
                overlay(shot, key, tb, c0, tf, hl, anch)
                for who, text, a0, a1, vis in local:
                    if a0 <= t < a1 + 0.25:
                        bk = (text, drawing)                # placed again when the drawing changes
                        if bk not in bub:
                            bub[bk] = (heads_t, [tf(b[0], b[1]) + tf(b[2], b[3]) for b in avoid], t)
                        hh, av, tb0 = bub[bk]
                        sb.AVOID[:] = av
                        nn = int(round((t - tb0) * DR))
                        pop = (0.82, 1.05)[nn] if (nn < 2 and abs(tb0 - a0) < 0.07) else 1.0
                        dry = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); dc = cairo.Context(dry)
                        box = fa._say_box(dc, Ctx(dc, 0), who, text, hh)
                        bx, by = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
                        c0.save(); c0.translate(bx, by); c0.scale(pop, pop); c0.translate(-bx, -by)
                        an.say(c0, Ctx(c0, 0), who, text, hh)
                        c0.restore()
                out.write_to_png("%s/f%05d.png" % (out_dir, n)); n += 1
    sb.ANIM.clear(); TALK.clear(); FORCE[0] = None
    # ---- sound
    oldlead = an.LEAD
    an.LEAD = LEAD
    try:
        m = an.mix(rows, total)
    finally:
        an.LEAD = oldlead
    m = m[:len(voice)] if len(m) >= len(voice) else np.pad(m, (0, len(voice) - len(m)))
    m[:int(A_LEN * SR)] = 0.0
    at = {r["shot"]: r["start"] for r in rows}
    an._at(m, om.door(0.30), T_OPEN, 0.30)
    for i_ in range(3):
        an._at(m, sx.thunk(0.04, 600), T_IN + 0.08 + i_ * 0.24, 0.12)
    an._at(m, om.door(0.25), T_SHUT, 0.25)
    an._at(m, sx.thunk(0.3, 80), T_SLAM, 0.90)
    an._at(m, si.servo(0.25, 700, 760), T_DROP0 - 0.3, 0.10)
    an._at(m, sx.thunk(0.35, 150), T_DROP1, 1.0)            # BONK
    an._at(m, sx.thunk(0.12, 420), T_DROP1 + 0.01, 0.6)
    an._at(m, bm.chime([2400, 3100, 2700], 0.05, 0.5), T_DROP1 + 0.06, 0.16)   # the stars
    for i_ in range(3):
        an._at(m, sx.thunk(0.04, 700), at["7.2"] + 0.05 + i_ * 0.25, 0.05)
    an._at(m, sx.thunk(0.2, 90), at["8.3"] + 0.05, 0.5)     # his fury
    env = (np.abs(voice) > 0.01).astype(float)
    env = si.lp(env, int(SR * 0.35)); env = env / max(1e-6, env.max())
    b = mus.bed(music, len(voice) / SR, T_DROP1 + 0.1)
    b = b[:len(voice)] if len(b) >= len(voice) else np.pad(b, (0, len(voice) - len(b)))
    mix = m + b * (0.16 - 0.12 * np.clip(env * 4, 0, 1))
    mix = mix[:int(total * SR)]
    mix *= 0.5 / max(1e-6, np.abs(mix).max())
    wav = os.path.join(out_dir, "mix.wav")
    sf.write(wav, np.stack([mix, mix], 1).astype(np.float32), SR)
    out = os.path.join(d, "fs_film4_%d.mp4" % (540 * S))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(DR), "-i", "%s/f%%05d.png" % out_dir, "-i", wav,
                    "-vf", "fps=30,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p", "-c:v", "libx264",
                    "-preset", "veryfast", "-crf", "18", "-colorspace", "bt709", "-color_primaries", "bt709",
                    "-color_trc", "bt709", "-color_range", "tv", "-frames:v", str(int(round(total * 30))),
                    "-af", "loudnorm=I=-14.5:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
                    "-t", "%.3f" % total, "-movflags", "+faststart", out], check=True)
    for _ in range(2):
        r_ = subprocess.run(["ffmpeg", "-i", out, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True)
        I = float([l for l in r_.stderr.splitlines() if l.strip().startswith("I:")][-1].split()[1])
        g = -15.0 - I
        if abs(g) < 0.3:
            break
        tmp = out + ".tmp.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out, "-c:v", "copy", "-af",
                        "volume=%.2fdB,alimiter=limit=0.66:level=false" % g, "-ar", "48000", "-c:a", "aac", "-b:a",
                        "192k", "-movflags", "+faststart", tmp], check=True)
        os.replace(tmp, out)
    print("wrote", out, "%.2f s, %d shots" % (total, len(LIST)))
    return out


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "../first-search"
    build(d, 2 if (len(sys.argv) > 2 and sys.argv[2] == "1080") else 1)
