"""v5, pinned. THE ONBOARDING: the animation, v5 (ob_anim_v4.py = v4, kept), after the cold mute test of v4 (two fresh viewers, frames
only; both told back four of the five beats; what both misread is fixed here and has not been tested again):
  - Pam on the floor: both asked whether she had fallen. 8.5 is longer (1.67 s): she looks at his hand, at the floor,
    kneels, puts a hand on a strip and lifts it to the others; in the hold of beat 09 she picks up two more;
  - the CV: its portrait has her blonde hair (it read as a bald man's, so nobody knew whose it was);
  - the tablet changing hands (6.1) is inside the frame; it had left by the left edge;
  - the handshake: Don stands further off, so the two open hands stop short of each other with the gap between them,
    and the robot comes up in that gap. The card shot (7.1) keeps the same framing.
THE ONBOARDING: the animation, v4 (ob_anim_v3.py = v3, kept): THE WHOLE FILM, ten beats, on storyboard v3 and script v6.
Beat 03 was approved as the look (v1 to v3); the other nine beats are built the same way, and three things change for
all ten, to meet the series' render standard (uptimez/CLAUDE.md, G3 and G5):
  - bubbles: every box inside the safe area (20, 96, 475, 816), never on a face. A tail ends beside the speaker's mouth:
    a short one from a box level with it ("R", "L"), or a curved one round the outside of the head from a box above
    ("A"); on Don's bare scalp and the robot's antenna it may come straight down ("T"). An off-screen speaker gets a
    caption with no tail (6.8). The robot's last ruling has no bubble: the stamp on the glass is its caption;
  - so a speaking single is framed wider than the storyboard's close-up, with clear wall beside the face;
  - "Oh..." (3.7) is two set-ups: the insert of the strand (her hand takes the pearl), then her whole face for the
    line, the pearl turning. The film has 56 set-ups for 55 shot numbers.
The two-shots with the door, the desk or the shredder in them are taken on the set (set_ob v4) through a camera; both
wide shots use set_ob.cam(). The robot shows one signal (set_ob.ONE_SIGNAL): words on its screen, the symbol on its paddle.
What moves, 12 drawings a second (30 frames a second out): mouths from the takes on whoever has the line; blinks;
the actions of script v6; a slow push-in on every single; the door, the ficus in its draught, the roll into the
shredder and the bin filling, the paddle, the payment, the cannon (a flash, a shake, a burst) and blue strips that
keep falling to the last frame; two emoji pops on silent reactions (Don 3.9, Pam 5.3).
  python3 ob_anim.py timing              -> ob_anim_timing_v4.json and a table
  python3 ob_anim.py stills OUT t ...    -> OUT/ob_anim_<t>.png (seconds of the film), 540 x 960
  python3 ob_anim.py sheet OUT.png [beat]-> one drawing in every 1/3 s
  python3 ob_anim.py qa                  -> the bubble and framing rules on every drawing that has a bubble (exit 1 on a miss)
  python3 ob_anim.py film OUT.mp4        -> 1080 x 1920, one file a beat, joined, with the mix"""
import json
import math
import os
import subprocess
import sys
import cairo
import kit
import emoji
import iwry_mouths as im
import ob_animatic as an
import ob_sofia_sheet as sh
import ob_chain as ch
import sofia_ob as so
import client_ob as co
import don_v4 as dv
import pam_mf as pm
import acts_ob_v4 as ac
import set_ob as st
import hands_ob as hd
from kit import Ctx, INK, ellipse, rect, cut

V = "v5"
W, H, FPS = 540, 960, 30
HERE = os.path.dirname(os.path.abspath(__file__))
TK = json.load(open(os.path.join(HERE, "ob_voices", "film", "takes.json")))
Z = W / 172.0                                              # a storyboard tile at full frame
F = st.FLOOR
FLOOR_COL = (0.72, 0.63, 0.50)
SAFE = (20, 96, 475, 816)
MONO = "DejaVu Sans Mono"
g12 = lambda x: round(x * 12) / 12.0
TIMING = dict(an.TIMING)
TIMING["3.7"] = (0.75, 0.40)                               # the insert first, then her face for the line
TIMING["8.5"] = 1.67                                       # v5: time to see her go down and pick one up
st.ONE_SIGNAL[0] = True
PX = [1.0]                                                 # device pixels to one design pixel, for this drawing
ANCH, QA = {}, {"bubbles": [], "faces": []}
OPT = {"bubbles": True, "plain": False, "fault": None}


def build():
    """The whole film on the drawing grid: the animatic's leads and tails, every length a whole number of drawings."""
    shots, n = [], 0                                        # n counts drawings: a cut can only fall on one
    for shot, tm in TIMING.items():
        row = dict(shot=shot, n0=n, t0=n / 12.0)
        if isinstance(tm, tuple):
            ld = int(round(tm[0] * 12))
            nd = max(1, int(math.ceil((ld / 12.0 + TK[shot]["len"] + tm[1]) * 12 - 0.35)))
            row["line"] = dict(who=TK[shot]["who"], text=TK[shot]["text"], t0=(n + ld) / 12.0,
                               t1=(n + ld) / 12.0 + TK[shot]["len"])
        else:
            nd = int(round(tm * 12))
        row["nd"], row["d"] = nd, nd / 12.0
        shots.append(row); n += nd
    return dict(total=n / 12.0, fps=FPS, shots=shots)


T = build()
SHOT = {s["shot"]: s for s in T["shots"]}
BEATS = sorted({s["shot"].split(".")[0] for s in T["shots"]}, key=int)
CUR = dict(t=0.0, tl=0.0, d=1.0, u=0.0, shot="", n=0)
BOOM = SHOT["8.2"]["t0"] + 1 / 12.0                         # the cannon


def beat_span(b):
    mine = [s for s in T["shots"] if s["shot"].split(".")[0] == b]
    return mine[0]["t0"], mine[-1]["t0"] + mine[-1]["d"]


# ---------------------------------------------------------------- time
def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def seg(a, b):
    return ease((CUR["tl"] - a) / max(b - a, 1e-6))


def within(a, b):
    return a - 1e-6 <= CUR["tl"] < b - 1e-6


def after(a):
    return CUR["tl"] >= a - 1e-6


def blink(*starts):
    return any(within(a, a + 2 / 12.0) for a in starts)


def line():
    return SHOT[CUR["shot"]].get("line")


def lead():
    return line()["t0"] - SHOT[CUR["shot"]]["t0"]


def said():
    return line()["t1"] - SHOT[CUR["shot"]]["t0"]


def code():
    """The mouth shape of this shot's speaker now: "" at rest inside the shot, a letter while he speaks."""
    ln = line()
    if not ln:
        return None
    vis = TK[CUR["shot"]].get("vis") or []
    i = int(round((CUR["t"] - ln["t0"]) * 12))
    return vis[i] if 0 <= i < len(vis) else ""


def speaking(pad=0.0):
    ln = line()
    return bool(ln) and ln["t0"] - 1e-6 <= CUR["t"] < ln["t1"] + pad


# ---------------------------------------------------------------- where things are, in design pixels
BASE = [None]                                              # device -> design, for this drawing (a sheet draws tiles anywhere)


def D(k, x, y):
    return BASE[0].transform_point(*k.c.user_to_device(x, y))


def DL(k, d):
    X, Y = k.c.user_to_device_distance(d, 0)
    return math.hypot(X, Y) / PX[0]


def _reg(k, who, hx, hy, s, m, cw, hw, top, fr, skin):
    a = dict(m=D(k, hx, hy + m * s), cw=DL(k, cw * s), hw=DL(k, hw * s), top=D(k, hx, hy - top * s), c=D(k, hx, hy + 8 * s),
             r=DL(k, fr * s), skin=skin)
    ANCH[who] = a
    if fr:
        QA["faces"].append((who, a["c"], a["r"]))
    return a


# ---------------------------------------------------------------- the cast
def _lids(k, pts, r, skin):
    c = k.c
    for x, y in pts:
        ellipse(k, x, y, r * 1.08, r * 1.08, skin, 5, shadow=False, outline=False)
        c.set_source_rgb(*INK); c.set_line_width(max(1.6, r * 0.26)); c.set_line_cap(1)
        c.move_to(x - r * 0.85, y + r * 0.10); c.curve_to(x - r * 0.3, y + r * 0.48, x + r * 0.3, y + r * 0.48, x + r * 0.85, y + r * 0.10)
        c.stroke()


def client(k, hx, hy, s, pose="open", face="plain", look=(0.7, 0.0), shut=False, mouth=None, who="CLIENT", **kw):
    """The Client, placed by the centre of his head."""
    o = co.client(k, hx + 4 * s, hy - co.HY * s, s, pose, face, look=look, mouth=mouth or None, **kw)
    ox, oy = o["head"]
    if shut:
        _lids(k, [(ox - 17 * s, oy - 1 * s), (ox + 17 * s, oy - 1 * s)], (co.FACES[face]["eye"] + 0.6) * s, co.SKIN)
    _reg(k, who, ox, oy, s, 30, 45, 57, 62, 50, co.SKIN)   # the tail's cheek: beside the mouth, above his collar
    return o


def don(k, hx, hy, s, act=None, look=None, raw=None, shut=False, mouth=None, strips=False):
    """Don, placed by the centre of his head."""
    feet = hy + 302 * s
    if raw:
        with ac.arms():
            o = dv.don(k, hx, feet, s, raw[0], raw[1], look=look or (-1, 0))
    else:
        o = ac.don(k, hx, feet, s, act, look)
    ox, oy = o["head"]
    skin = kit.PEOPLE["DON"]["skin"]
    c = k.c
    if mouth:
        c.save(); c.translate(ox, oy); c.scale(s, s); im.don_mouth(k, (0, 0), mouth); c.restore()
    if shut:
        _lids(k, [(ox - 17 * s, oy + 5 * s), (ox + 17 * s, oy + 5 * s)], 11.8 * s, skin)
    if strips:                                             # what the cannon left on him
        st.confetti(k, ox - 40 * s, oy - 58 * s, ox + 40 * s, oy - 36 * s, n=6, seed=4, s=0.9 * s)
        st.confetti(k, ox - 62 * s, oy + 46 * s, ox + 62 * s, oy + 70 * s, n=5, seed=8, s=0.9 * s)
    _reg(k, "DON", ox, oy, s, 32, 39, 56, 50, 47, skin)
    return o


def sofia(k, hx, hy, s, pose, face, look, lean=0, mouth=None, roll=0.0, rise=0.0, sway=True, who="SOFIA"):
    """Sofia, placed by the centre of her head (before any lean)."""
    so.ROLLING[0], so.RISE[0] = roll, rise
    try:
        lag = (1.4 * math.sin(2 * math.pi * CUR["t"] / 1.5), 0) if sway else (0, 0)
        o = sh.at(k, hx, hy, s, (0, so.HY), pose, face, look=look, lean=lean, mouth=mouth or None, lag=lag)
    finally:
        so.ROLLING[0], so.RISE[0] = 0.0, 0.0
    h = so.HY * s
    th = math.radians(lean)
    ox, oy = hx - h * math.sin(th), hy - h + h * math.cos(th)
    _reg(k, who, ox, oy, s, 33, 40, 64, 72, 45, so.SKIN)
    return o


def pam(k, hx, hy, s, act, look=None):
    """Pam standing, placed by the centre of her head."""
    o = ac.pam(k, hx, hy - pm.HY * s, s, act, look)
    _reg(k, "PAM", hx, hy, s, 30, 40, 56, 60, 45, kit.PEOPLE["PAM"]["skin"])
    return o


def pam_floor(k, x, floor, s, up, pick=0.0):
    o = ac.pam_floor(k, x, floor, s, up, pick=pick)
    ox, oy = o["head"]
    _reg(k, "PAM", ox, oy, s, 30, 40, 56, 60, 45, kit.PEOPLE["PAM"]["skin"])
    return o


def robot(k, x, feet, s, act="idle", look=(-1, 0), side=-1):
    o = st.robot(k, x, feet, s, act, look=look, side=side)
    ox, oy = o["head"]
    _reg(k, "ROBOT", ox, oy, s, 0, 46, 46, 37, 0, None)    # a tail comes down onto the top of its screen
    QA["faces"].append(("ROBOT", D(k, ox, oy), DL(k, 40 * s)))
    return o


def rolling(start, stop=None):
    seq = (0.5, 1.0, 0.5, 0.01, -0.5, -1.0, -0.5, 0.01)
    tl = min(CUR["tl"], stop) if stop is not None else CUR["tl"]
    if tl < start:
        return 0.0
    return seq[int(round((tl - start) * 12)) % len(seq)]


# ---------------------------------------------------------------- cameras, backgrounds, light
def wall(k):
    k.c.set_source_rgb(*kit.WALL); k.c.paint()


def floor_line(k, y):
    c = k.c
    c.set_source_rgb(*FLOOR_COL); c.rectangle(-40, y, W + 80, H); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(2); c.move_to(-40, y); c.line_to(W + 40, y); c.stroke()


def push(k, amount=0.03, focus=(270, 430)):
    """c.save() and a push-in about `focus`, stepped with the drawings."""
    c = k.c
    z = 1 + amount * CUR["u"]
    c.save(); c.translate(*focus); c.scale(z, z); c.translate(-focus[0], -focus[1])


def tile(k, amount=0.03, focus=(270, 430), dy=0.0):
    """Storyboard tile coordinates (172 x 306) at full frame, for the inserts."""
    push(k, amount, focus)
    k.c.translate(0, dy); k.c.scale(Z, Z)


def world(k, x0, y0, z, open_=0.0, sway=0.0, amount=0.0, shake=(0, 0), decor=True):
    """c.save() and the set through a camera whose window starts at (x0, y0) with zoom z."""
    c = k.c
    zz = z * (1 + amount * CUR["u"])
    x0 += (W / z - W / zz) / 2.0; y0 += (H / z - H / zz) / 2.0
    c.save(); c.translate(*shake); c.scale(zz, zz); c.translate(-x0, -y0)
    st.stage(k, open_=open_, sway=sway, decor=decor)
    st.desk(k)


def wide(k, **kw):
    world(k, st.CAM[0], st.CAM[1], st.CAM[2], **kw)


TWO = (62, 286, 1.6)                                       # the handshake framing, and the card's: the same camera


def light(k):
    if OPT["plain"]:
        return
    c = k.c
    g = cairo.LinearGradient(0, 0, 420, 620)
    g.add_color_stop_rgba(0, 1.0, 0.96, 0.84, 0.16); g.add_color_stop_rgba(1, 1.0, 0.96, 0.84, 0.0)
    c.set_source(g); c.paint()
    g = cairo.RadialGradient(270, 450, 300, 270, 450, 660)
    g.add_color_stop_rgba(0, 0.10, 0.07, 0.05, 0.0); g.add_color_stop_rgba(1, 0.10, 0.07, 0.05, 0.30)
    c.set_source(g); c.paint()


def flash(k, since, col=(1, 1, 1), a=0.55):
    n = int(round((CUR["tl"] - since) * 12))
    if 0 <= n < 3 and not OPT["plain"]:
        k.c.set_source_rgba(*col, a * (1.0, 0.45, 0.15)[n]); k.c.paint()


def falling(k, n, seed=3, speed=95.0):
    """Blue strips coming down through the frame, in screen space, from the cannon to the end of the film."""
    c = k.c
    tau = CUR["t"] - BOOM
    if tau < 0 or OPT["plain"]:
        return
    for i in range(n):
        u = ((i * 7919 + seed * 131) % 1000) / 1000.0
        v = ((i * 104729 + seed * 17) % 1000) / 1000.0
        y = ((v * (H + 80) + (speed * (0.7 + 0.6 * u)) * tau) % (H + 80)) - 40
        x = 20 + u * (W - 40) + 14 * math.sin(tau * (1.5 + v) + i)
        c.save(); c.translate(x, y); c.rotate(u * 6.3 + tau * (1.2 + v) * (1 if i % 2 else -1))
        c.set_source_rgb(*ac.STRIP); c.rectangle(-12, -2.6, 24, 5.2); c.fill()
        c.set_source_rgb(1, 1, 1); c.rectangle(-8, -0.6, 13, 1.2); c.fill()
        c.restore()


def burst(k, ox, oy, since):
    """The cannon going off, in the set's coordinates."""
    tau = CUR["tl"] - since
    if tau < 0:
        return
    c = k.c
    for i in range(70):
        u = ((i * 7919 + 97) % 1000) / 1000.0
        v = ((i * 15485863 + 31) % 1000) / 1000.0
        ang = math.radians(-158 + 150 * u)
        r = (150 + 330 * v) * (1 - math.exp(-4.2 * tau))
        x, y = ox + math.cos(ang) * r * 0.9 + 26 * tau, oy + math.sin(ang) * r + 150 * tau * tau
        c.save(); c.translate(x, y); c.rotate(u * 6.3 + tau * 9 * (v - 0.5))
        c.set_source_rgb(*ac.STRIP); c.rectangle(-9, -2, 18, 4); c.fill()
        c.set_source_rgb(1, 1, 1); c.rectangle(-6, -0.5, 10, 1); c.fill()
        c.restore()


# ---------------------------------------------------------------- bubbles
def _rows(c, text, width):
    words, rows, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if c.text_extents(t).x_advance > width and cur:
            rows.append(cur); cur = w
        else:
            cur = t
    return rows + [cur]


def speak(k, form, size=26, maxw=300, at=None, side=1, gap=14, dx=0, dy=0, who=None, rows=None):
    """This shot's line, in screen space (call after the last c.restore()). See the module's notes for the forms."""
    ln = line()
    n = int(round((CUR["tl"] - lead()) * 12))
    if n < 0 or CUR["t"] >= ln["t1"] + 0.25 - 1e-6:
        return
    who = who or ln["who"]
    a = ANCH.get(who)
    c = k.c
    mono = ln["who"] == "ROBOT"
    font = (MONO, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD) if mono else (kit.FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    c.select_font_face(*font); c.set_font_size(size)
    rows = rows or _rows(c, ln["text"], maxw)
    ws = [c.text_extents(r).x_advance for r in rows]
    lh = size * 1.14
    bw, bh = max(ws) + 44, len(rows) * lh + 26
    sd = 1 if form == "R" else -1 if form == "L" else side
    if form in ("R", "L"):
        bx = a["m"][0] + a["hw"] + gap if sd > 0 else a["m"][0] - a["hw"] - gap - bw
        by = a["m"][1] - bh / 2
    elif form == "T":
        bx, by = a["top"][0] - bw / 2, a["top"][1] - gap - bh
    else:
        bx, by = at
    bx, by = bx + dx, by + dy
    bx = max(SAFE[0], min(SAFE[2] - bw, bx)); by = max(SAFE[1], min(SAFE[3] - bh, by))
    if OPT["fault"] == "box":
        by = 40
    tail, tip, inward = None, None, None
    if form in ("R", "L"):
        ex = bx + 3 if sd > 0 else bx + bw - 3
        ty = max(by + 15, min(by + bh - 15, a["m"][1]))
        tip = (a["m"][0] + sd * (a["cw"] + 1.5), a["m"][1])
        tail = [(ex, ty - 11), tip, (ex, ty + 11)]
        inward = (-sd, 0)
    elif form == "T":
        rx = max(bx + 28, min(bx + bw - 28, a["top"][0]))
        tip = (a["top"][0], a["top"][1] + 1.5)
        tail = [(rx - 12, by + bh - 3), tip, (rx + 12, by + bh - 3)]
        inward = (0, 1)
    elif form == "A":                                      # from a box above, round the outside of the head
        tip = (a["m"][0] + sd * (a["cw"] + 1.5), a["m"][1])
        bxm = max(bx + 26, min(bx + bw - 26, a["m"][0] + sd * (a["hw"] + 20)))
        b0, b1 = (bxm - 11, by + bh - 3), (bxm + 11, by + bh - 3)
        ctl = (a["m"][0] + sd * (a["hw"] + 30), a["m"][1] - 0.35 * (a["m"][1] - by - bh))
        q = lambda p0, p1, p2, t: ((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
                                   (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1])
        tail = [q(b0, (ctl[0] - 7 * sd, ctl[1]), tip, i / 8.0) for i in range(9)] + \
               [q(b1, (ctl[0] + 7 * sd, ctl[1]), tip, i / 8.0) for i in range(7, -1, -1)]
        inward = (-sd, 0)
    if tip is not None and OPT["fault"] == "tip":
        shift = (70, -40)
        tip = (tip[0] + shift[0], tip[1] + shift[1])
        tail = [tail[0], tip, tail[-1]]
    QA["bubbles"].append(dict(shot=CUR["shot"], who=who, form=form, box=(bx, by, bx + bw, by + bh), tip=tip, size=size, inward=inward))
    if not OPT["bubbles"]:
        return
    pop_ = (0.82, 1.05)[n] if n < 2 else 1.0
    px, py = tip if tip is not None else (bx + bw / 2, by + bh / 2)
    c.save(); c.translate(px, py); c.scale(pop_, pop_); c.translate(-px, -py)
    if tail:
        cut(k, tail, (1, 1, 1))
    cut(k, kit.rough_rect_pts(k, bx, by, bw, bh, 900 + len(ln["text"]), j=1.6), (1, 1, 1))
    if tail:                                               # no line where the tail leaves the box
        base = (tail[0], tail[-1])
        c.set_source_rgb(1, 1, 1); c.set_line_width(3.4)
        if form in ("R", "L"):
            c.move_to(base[0][0] + sd * 1.5, base[0][1] + 1.6); c.line_to(base[1][0] + sd * 1.5, base[1][1] - 1.6)
        else:
            c.move_to(base[0][0] + 1.6, base[0][1] + 1.2); c.line_to(base[1][0] - 1.6, base[1][1] + 1.2)
        c.stroke()
    c.select_font_face(*font); c.set_font_size(size); c.set_source_rgb(*INK)
    for i, (r, w) in enumerate(zip(rows, ws)):
        c.move_to(bx + (bw - w) / 2, by + 13 + lh * (i + 0.80)); c.show_text(r)
    c.restore()


def pop(k, chr_, x, y, since, r=48):
    """One emoji in a round tinted bubble, no tail: a silent reaction only."""
    n = int(round((CUR["tl"] - since) * 12))
    if n < 0 or not OPT["bubbles"]:
        return
    s = (0.55, 1.14, 0.96)[n] if n < 3 else 1.0
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    c.set_source_rgba(0, 0, 0, 0.18); c.arc(3, 4, r, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(1.0, 0.95, 0.93); c.arc(0, 0, r, 0, 2 * math.pi); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(2.6); c.stroke()
    emoji.draw_emoji(c, chr_, 0, 2, r * 1.15)
    c.restore()


# ================================================================ BEAT 01 · the arrival
def _staff(k, don_act="stand", dlook=(-1, 0), sof=("hold", "smile", (-0.9, -0.2)), pam_act="typing", plook=None):
    P = st.POS
    robot(k, P["robot"][0], F, P["robot"][2])
    ac.shredder(k, st.SHRED_X, F, 1.0, fill=0.0)
    x, f, s = P["pam"]
    pam(k, x, f + pm.HY * s, s, pam_act, plook)
    x, f, s = P["sofia"]
    sofia(k, x, f + so.HY * s, s, sof[0], sof[1], sof[2])
    x, f, s = P["don"]
    don(k, x, f - 302 * s, s, don_act, dlook)


def _through_glass(k, draw_, open_):
    """Somebody outside, seen through the door: drawn inside the opening, the glass over him where it has not slid away."""
    c = k.c
    x, y, w, h = st.DOOR
    c.save(); c.rectangle(x, y, w, h); c.clip()
    draw_()
    px = x - w * 0.92 * open_
    c.set_source_rgba(*st.GLASS, 0.26); c.rectangle(px, y, w, h); c.fill()
    c.restore()


def s1_1(k):
    """The glass door slides open. He walks in."""
    op = 0.85 * seg(0.08, 0.70)
    tl = CUR["tl"]
    sway = 3.2 * math.sin((tl - 0.25) * 10) * math.exp(-(tl - 0.25) * 2.4) if tl > 0.25 else 0.0
    wide(k, open_=op, sway=sway)
    step = seg(0.66, 1.42)
    x = 78 + 34 * step
    bob = -3.0 * abs(math.sin(step * math.pi * 3)) if 0 < step < 1 else 0.0
    hy = F + co.HY * 0.66 + bob
    if tl < 0.66 - 1e-6:
        _through_glass(k, lambda: client(k, x - 4 * 0.66, hy, 0.66, "arrive", "confident", (0.8, 0.0)), op)
    _staff(k, dlook=(-1, 0) if tl > 0.5 else (-0.2, 0.3), sof=("hold", "smile" if tl > 0.9 else "tiny", (-0.9, -0.2)))
    if tl >= 0.66 - 1e-6:
        client(k, x - 4 * 0.66, hy, 0.66, "arrive", "confident", (0.8, 0.0))
    k.c.restore(); light(k)


def s1_2(k):
    """One run of looks: Pam at Don, Don at Sofia, Sofia at him. Pam is already typing."""
    wall(k); push(k, 0.03, (270, 420)); floor_line(k, 904)
    pam(k, 440, 452, 1.75, "typing", (-0.9, 0.0) if within(0.17, 0.75) else (-0.2, 0.9))
    sofia(k, 284, 440, 1.75, "hold", "smile" if after(0.75) else "tiny", (-0.9, -0.2) if after(0.75) else (-0.3, 0.1))
    don(k, 112, 418, 1.75, "stand", (1, 0) if within(0.42, 1.0) else (-1, 0), shut=blink(0.25))
    k.c.restore(); light(k)


def s1_3(k):
    wall(k); push(k, 0.03, (200, 430))
    nod = 4 * math.sin(math.pi * min(1.0, max(0.0, (CUR["tl"] - lead()) / 0.33))) if after(lead()) else 0
    client(k, 140, 430 + nod, 2.3, "arrive", "confident", (0.8, 0.0), shut=blink(said() + 0.08), mouth=code())
    k.c.restore(); light(k)
    speak(k, "R", 26, 152)


def s1_4(k):
    """Don: the vest. A customer; she will see this."""
    wall(k); push(k, 0.04, (270, 420))
    act = "stand" if CUR["tl"] < 2 / 12.0 - 1e-6 else "tug_down" if within(5 / 12.0, 7 / 12.0) else "tug"
    don(k, 270, 400, 3.0, act, (1.2, 0.0) if after(6 / 12.0) else (-1, 0))
    k.c.restore(); light(k)


# ================================================================ BEAT 02 · the handshake
def _two(k, amount=0.02, **kw):
    world(k, TWO[0], TWO[1], TWO[2], amount=amount, **kw)


def _two_client(k, pose, face, look=(0.8, 0.0), x=150, **kw):
    return client(k, x - 4 * 0.66, F + co.HY * 0.66, 0.66, pose, face, look, **kw)


def _two_don(k, act, look=None, raw=None, mouth=None, x=352):
    return don(k, x, F + 14 - 302 * 0.75, 0.75, act, look, raw=raw, mouth=mouth)


def s2_1(k):
    """A hand out. His hand comes to meet it."""
    _two(k)
    robot(k, 198, F, 0.50)
    ac.shredder(k, st.SHRED_X, F, 1.0, fill=0.0)
    _two_client(k, "offer" if after(0.33) else "arrive", "confident")
    _two_don(k, "hand_out", mouth=code())
    k.c.restore(); light(k)
    speak(k, "T", 30)


def s2_2(k):
    """Before the palms meet, the robot is between them and the red paddle snaps up."""
    sh_ = (0, (-5, 4, -2)[int(round((CUR["tl"] - 1 / 12.0) * 12))]) if within(1 / 12.0, 4 / 12.0) else (0, 0)
    _two(k, shake=sh_)
    ac.shredder(k, st.SHRED_X, F, 1.0, fill=0.0)
    _two_client(k, "offer", "puzzled" if after(2 / 12.0) else "confident", (0.5, 0.6) if after(2 / 12.0) else (0.8, 0))
    _two_don(k, "hand_out", (-0.6, 0.7) if after(2 / 12.0) else None)
    if CUR["tl"] < 1 / 12.0 - 1e-6:
        robot(k, 230, F + 4, 0.54)                         # on its way in
    else:
        robot(k, 262, F + 10, 0.58, "block", look=(0, 0))
    k.c.restore(); light(k)
    flash(k, 1 / 12.0, (0.86, 0.16, 0.16), 0.22)
    speak(k, "T", 24, 170, dx=-6, dy=-150, rows=["CONTACT", "NOT", "VERIFIED."])


def s2_3(k):
    """Stranded. A bigger title."""
    wall(k); push(k, 0.03, (300, 430))
    don(k, 312, 440, 2.2, "hand_out", (-1, -0.2) if after(lead() - 0.1) else (-1.2, 0.9), mouth=code())
    k.c.restore(); light(k)
    speak(k, "T", 30, 320)


def s2_4(k):
    """What just happened? He lowers his hand."""
    wall(k); push(k, 0.03, (270, 400))
    client(k, 262, 420, 3.2, "offer" if CUR["tl"] < 5 / 12.0 - 1e-6 else "open", "puzzled", (0.8, 0.2), shut=blink(0.5), roll=False)
    k.c.restore(); light(k)


# ================================================================ BEAT 03 · the blueprint, and the question
def s3_1(k):
    """Three-shot: he shows them the plan of his ten garages; it springs shut in his hand. She looks at him, not at it."""
    c = k.c
    snap = g12(said() + 0.12)
    push(k, 0.025, (270, 560))
    wall(k); floor_line(k, 870)
    st.first_client(k, 404, 176, 1.45)
    c.save(); c.translate(-16, 400.4); c.scale(1.6, 1.6)                     # the storyboard's wide tile
    fl = 300
    opening = seg(0.08, 0.33)
    shut = after(snap)
    don(k, 296, fl - 302 * 0.80, 0.80, "stand", (-1.0, 0.75) if shut and CUR["tl"] < snap + 0.5 else (-1.0, 0.35), shut=blink(1.0))
    sofia(k, 214, fl + so.HY * 0.80, 0.80, "hold", "closed" if blink(1.67) else "smile", (-0.9, -0.3))
    jolt = -3 if within(snap, snap + 1 / 12.0) else 0
    client(k, 76, fl + co.HY * 0.56, 0.56, "open", "plain", (0.8, 0.0), shut=blink(snap + 1 / 12.0), mouth=code(), roll=False)
    if shut or opening <= 0:
        n = int(round((CUR["tl"] - snap) * 12)) if shut else 9
        ac.roll(k, 96, 168 + jolt + (2 if n == 1 else 0), 0.92, math.pi / 2 - 0.10, ln=118)
    else:
        w = 0.35 + 0.65 * opening * (1.06 if within(0.25, 0.34) else 1.0)
        bob = -1.5 if code() in ("A", "O", "E") else 0.0
        c.save(); c.translate(96, 168 + bob); c.scale(w, 1); ac.plan_open(k, 0, 0, 0.92); c.restore()
    for hx in ((96 - 62 * 0.92 * (1 if not shut else 0.95)), (96 + 62 * 0.92 * (1 if not shut else 0.95))):
        if shut or opening <= 0 or opening > 0.9:
            ellipse(k, hx, 170 + (jolt if shut else 0), 9, 9, co.SKIN, 931, shadow=False, lw=1.6)
    c.restore(); c.restore()
    light(k)
    speak(k, "A", 24, 262, at=(20, 348), side=1)


def s3_2(k):
    """Sweet."""
    wall(k); push(k, 0.035, (330, 450))
    sofia(k, 404, 420, 2.6, "hold", "closed" if blink(0.0) else "smile", (-0.8, -0.1), mouth=code())
    k.c.restore(); light(k)
    speak(k, "L", 24, 156)


def s3_3(k):
    """Plain. A fact."""
    wall(k); push(k, 0.03, (200, 430))
    client(k, 140, 430, 2.3, "open", "plain", (0.7, 0.0), shut=blink(g12(said() + 0.08)), mouth=code())
    k.c.restore(); light(k)
    speak(k, "R", 28, 152)


def _eyes_shot(k, face, look):
    """Tight on her eyes: the storyboard's tile, her eyes at its centre."""
    sofia(k, 86, 145 - 12 * 2.3, 2.3, "low", face, look, sway=False)


def s3_4(k):
    """Her eyes go down him: six drawings."""
    wall(k); tile(k, 0.02, (270, 470))
    n = max(0, min(6, int(round((CUR["tl"] - 1 / 12.0) * 12))))
    _eyes_shot(k, "appraise", (-0.8, -0.2 + 1.2 * n / 6.0))
    k.c.restore(); light(k)


def s3_5(k):
    """What they are on: him. The camera goes down him as her eyes did. He is unaware: he blinks."""
    wall(k)
    tile(k, 0.0, dy=-150 * seg(0.0, 0.55))
    client(k, 86, 133 - 10 * 0.80, 0.80, "open", "plain", (0.0, 0.0), shut=blink(0.33))
    k.c.restore(); light(k)


def s3_6(k):
    """They come back up: five drawings. Then the lids relax and the brows soften."""
    wall(k); tile(k, 0.03, (270, 470))
    n = max(0, min(5, int(round(CUR["tl"] * 12))))
    if CUR["tl"] < 0.5 - 1e-6:
        _eyes_shot(k, "appraise", (-0.8, 1.0 - 1.2 * n / 5.0))
    else:
        _eyes_shot(k, "interested", (-0.9, -0.2))
    k.c.restore(); light(k)


def s3_7(k):
    """The insert: her hand comes up from below and takes one pearl. Then her face: "Oh...", the pearl turning."""
    wall(k)
    if CUR["tl"] < 6 / 12.0 - 1e-6:
        tile(k, 0.02, (250, 520))
        hx, hy = 86 - 16 * 2.5, 157 - (so.BODY_TOP + 18 - so.HY) * 2.5
        if CUR["tl"] < 1 / 12.0 - 1e-6:
            sofia(k, hx, hy, 2.5, "low", "interested", (-0.9, -0.2), sway=False, who="-SOFIA")
        else:
            rise = 1.0 if CUR["tl"] < 2 / 12.0 - 1e-6 else 0.45 if CUR["tl"] < 3 / 12.0 - 1e-6 else 0.0
            sofia(k, hx, hy, 2.5, "pearl", "interested", (-0.9, -0.2), roll=rolling(4 / 12.0), rise=rise, sway=False, who="-SOFIA")
        k.c.restore(); light(k)
        return
    push(k, 0.03, (330, 450))
    sofia(k, 404, 400, 2.6, "pearl", "oh" if speaking(0.08) else "interested", (-0.9, -0.2), roll=rolling(4 / 12.0))
    k.c.restore(); light(k)
    speak(k, "L", 32, 120)


def s3_8(k):
    """She rolls the pearl, her eyes on him. He is looking at his drawing."""
    push(k, 0.03, (330, 430))
    wall(k); floor_line(k, 872)
    client(k, 112, 900 + co.HY * 1.16, 1.16, "arrive", "plain", (-0.6, 1.4), shut=blink(0.5))
    sofia(k, 384, 452 - 22 * 3.5, 3.5, "pearl", "interested", (-1.0, -0.1), roll=rolling(0.0))
    k.c.restore(); light(k)


def s3_9(k):
    """Don has seen it. The sales smile; then he goes still, and his eyes go down."""
    wall(k); push(k, 0.045, (270, 420))
    if CUR["tl"] < 3 / 12.0 - 1e-6:
        don(k, 270, 440, 3.1, raw=("stand", "grin"), look=(-1.2, 0.1))
    else:
        don(k, 270, 440, 3.1, "still", (-0.3, 1.5) if after(5 / 12.0) else (-1.2, 0.1))
    k.c.restore(); light(k)
    pop(k, "\U0001F494", 414, 226, 7 / 12.0, r=52)


def s3_10(k):
    """She sees that he saw. Her hand stops mid-roll; her mouth closes; she does not look away."""
    wall(k); push(k, 0.03, (270, 430))
    if CUR["tl"] < 3 / 12.0 - 1e-6:
        sofia(k, 262, 380, 5.0, "pearl", "interested", (-1.0, -0.1), roll=rolling(0.0))
    elif CUR["tl"] < 4 / 12.0 - 1e-6:
        sofia(k, 262, 380, 5.0, "pearl", "interested", (1.0, 0.0), roll=rolling(0.0, 3 / 12.0), sway=False)
    else:
        sofia(k, 262, 380, 5.0, "pearl", "caught", (1.0, 0.0), roll=rolling(0.0, 3 / 12.0), sway=False)
    k.c.restore(); light(k)


def s3_11(k):
    """He takes hold of his vest and pulls it straight. The smile comes back, too wide."""
    wall(k); push(k, 0.03, (270, 420))
    if CUR["tl"] < 4 / 12.0 - 1e-6:
        don(k, 270, 400, 3.0, "still", (-0.3, 1.5), shut=within(1 / 12.0, 3 / 12.0))
    else:
        don(k, 270, 400, 3.0, "tug_down" if within(6 / 12.0, 8 / 12.0) else "tug")
    k.c.restore(); light(k)


def _client_holds(k, hx, hy, s, face, look, lift=0, **kw):
    """The Client with the roll upright in his hand, low enough to leave his bubble clear."""
    pose = co.POSES["open"][:2] + co._ik(1, 70, co.BT + 112 + lift)
    o = client(k, hx, hy, s, pose, face, look, roll=False, **kw)
    x, y = o["hands"][1]
    ac.roll(k, x + 4 * s, y - 26 * s, s, 0.20, ln=150)
    ellipse(k, x, y, co.HAND * s, co.HAND * s, co.SKIN, 971, shadow=False, lw=2 * s)
    return o


def s3_12(k):
    """He saw none of it. The roll is in his hand."""
    wall(k); push(k, 0.03, (200, 430))
    lift = -4 if code() in ("A", "E", "O") and within(0.6, 1.2) else 0
    _client_holds(k, 140, 430, 2.3, "plain", (0.7, 0.0), lift, shut=blink(0.0, g12(said() + 0.08)), mouth=code())
    k.c.restore(); light(k)
    speak(k, "R", 26, 152)


# ================================================================ BEAT 04 · the pitch, and the handover
def s4_1(k):
    """He steps between them and sells. He believes it."""
    wall(k); push(k, 0.035, (270, 470))
    don(k, 270, 490, 2.6, raw=("pleased", "grin"), look=(-1, 0), mouth=code(), shut=blink(0.0))
    k.c.restore(); light(k)
    speak(k, "T", 28, 330)


def s4_2(k):
    """An open palm. He looks at the roll, holds it back a moment, then looks at Don."""
    _two(k)
    robot(k, 198, F, 0.50)
    ac.shredder(k, st.SHRED_X, F, 1.0, fill=0.0)
    pose = co.POSES["open"][:2] + co._ik(1, 112, co.BT + 96)
    o = client(k, 150 - 4 * 0.66, F + co.HY * 0.66, 0.66, pose, "puzzled", (0.9, 1.6) if CUR["tl"] < 0.6 - 1e-6 else (0.8, 0.0),
               roll=False)
    x, y = o["hands"][1]
    ac.roll(k, x + 4 * 0.66, y - 26 * 0.66, 0.66, 0.22, ln=150)
    ellipse(k, x, y, co.HAND * 0.66, co.HAND * 0.66, co.SKIN, 971, shadow=False, lw=1.4)
    _two_don(k, "hand_out")
    k.c.restore(); light(k)


def s4_3(k):
    """He gives it. His fingers let go a moment late."""
    _two(k)
    robot(k, 198, F, 0.50)
    ac.shredder(k, st.SHRED_X, F, 1.0, fill=0.0)
    given = after(lead())
    pose = co.POSES["open"][:2] + co._ik(1, 166, co.BT + 92)
    late = within(lead(), lead() + 3 / 12.0)
    o = client(k, 150 - 4 * 0.66, F + co.HY * 0.66, 0.66, pose if (not given or late) else "open", "confident", (0.8, 0.0), roll=False)
    if not given:
        x, y = o["hands"][1]
        ac.roll(k, x + 22 * 0.66, y - 2 * 0.66, 0.66, math.pi / 2 - 0.12, ln=150)
        ellipse(k, x, y, co.HAND * 0.66, co.HAND * 0.66, co.SKIN, 971, shadow=False, lw=1.4)
        _two_don(k, "hand_out")
    else:
        _two_don(k, "holds", mouth=code())
    k.c.restore(); light(k)
    speak(k, "T", 26, 200)


def s4_4(k):
    """His eyes go to Sofia, off right. Without looking, he sets the roll down beside him."""
    world(k, 150, 440, 2.3, amount=0.03)
    ac.shredder(k, st.SHRED_X, F, 1.0, fill=0.0)
    down = after(8 / 12.0)
    don(k, 304, F + 14 - 302 * 0.75, 0.75, "set_down" if down else "holds", (1.7, -0.2) if after(3 / 12.0) else (-1, -0.2))
    k.c.restore(); light(k)


def s4_5(k):
    """Not the in-tray: the slot. The roll goes in. Blue strips fill the clear bin."""
    wall(k); floor_line(k, 900)
    c = k.c
    g = seg(0.08, 1.15)
    jx = (1.5, -1.5, 0.8, -0.8)[CUR["n"] % 4] if 0.02 < g < 0.98 else 0
    c.save(); c.translate(jx, 0)
    top = 900 - 112 * 4.2 + 8
    c.save(); c.rectangle(0, 0, W, top + 14); c.clip()
    ac.roll(k, 270, 250 + 330 * g, 3.6, 0.0, ln=110)
    c.restore()
    ac.shredder(k, 270, 900, 4.2, fill=0.85 * g)
    c.restore(); light(k)


def s4_6(k):
    """He is looking at Don, and nods slowly."""
    wall(k); push(k, 0.03, (270, 400))
    nod = 7 * math.sin(math.pi * min(1.0, max(0.0, (CUR["tl"] - 0.2) / 0.45)))
    client(k, 262, 420 + nod, 3.2, "open", "warm", (0.8, 0.1), shut=blink(0.33))
    k.c.restore(); light(k)


# ================================================================ BEAT 05 · the silence, and the condition
def _pam_don(k, act, plook):
    wall(k); push(k, 0.025, (300, 420))
    don(k, 88, 500, 1.3, raw=("pleased", "smug"), look=(-1, 0))               # glowing, and looking the other way
    pam(k, 292, 390, 2.3, act, plook)
    k.c.restore(); light(k)


def s5_1(k):
    """Pam saw. Her eyes are on the bin; a finger goes up. He does not see her."""
    _pam_don(k, "finger" if after(4 / 12.0) else "typing", (-0.9, 0.6))


def s5_2(k):
    wall(k); push(k, 0.04, (270, 420))
    don(k, 270, 440, 3.1, raw=("pleased", "smug"), look=(-1, 0))
    k.c.restore(); light(k)


def s5_3(k):
    """Her eyes are on Don, still glowing. She lowers the finger."""
    act = "finger" if CUR["tl"] < 6 / 12.0 - 1e-6 else "lower" if CUR["tl"] < 10 / 12.0 - 1e-6 else "typing"
    _pam_don(k, act, (-0.9, -0.2) if CUR["tl"] < 10 / 12.0 - 1e-6 else (-0.3, 0.9))
    pop(k, "\U0001F910", 420, 214, 7 / 12.0, r=46)


def s5_4(k):
    """The watch. His terms."""
    wall(k); push(k, 0.03, (200, 430))
    pose = co.POSES["open"][:2] + co._ik(1, 52, co.BT + 74)
    up = after(lead() - 1 / 12.0)
    client(k, 140, 430, 2.3, pose, "confident", (0.8, 0.0) if up else (0.9, 2.2), shut=blink(g12(said() + 0.08)), mouth=code(),
           roll=False)
    k.c.restore(); light(k)
    speak(k, "R", 26, 152)


def s5_5(k):
    """No question asked. His eyes go to Sofia."""
    wall(k); push(k, 0.04, (270, 470))
    don(k, 270, 480, 2.8, raw=("stand", "grin"), look=(1.4, 0.0) if after(said() + 0.1) else (-1, 0), mouth=code())
    k.c.restore(); light(k)
    speak(k, "T", 34)


def s5_6(k):
    """She is looking at the Client."""
    wall(k); push(k, 0.03, (270, 430))
    sofia(k, 270, 420, 4.8, "low", "interested", (-0.9, -0.2))
    k.c.restore(); light(k)


# ================================================================ BEAT 06 · Sofia does it
def s6_1(k):
    """Clipboard under her arm, she takes Pam's tablet without a look."""
    wall(k); push(k, 0.03, (270, 450))
    taken = after(5 / 12.0)
    pam(k, 438, 440, 1.5, "empty" if taken else "typing", ((-0.2, 0.9) if CUR["tl"] < 9 / 12.0 - 1e-6 else (-0.9, 0.0)) if taken else None)
    sofia(k, 262, 430, 1.5, "show" if taken else "hold", "recover", (-0.9, -0.1))
    k.c.restore(); light(k)


def s6_2(k):
    """One green button. A breath, close to him. Her eyes stay on him."""
    push(k, 0.03, (270, 470)); wall(k)
    client(k, 96, 452, 1.78, "open", "confident", (0.8, 0.3), shut=blink(0.17), roll=False)
    sofia(k, 398, 440, 1.9, "show", "recover", (-0.9, -0.15), mouth=code())
    k.c.restore(); light(k)
    speak(k, "A", 28, 200, at=(190, 176), side=-1)


def _device(k, done, thumb):
    """The insert of the screen; thumb 0..1 is how far his thumb has come in."""
    c = k.c
    c.save(); c.translate(86, 153); c.scale(1.34, 1.34); c.translate(-92, -153)
    sh.device_insert(c, k, 92, 147, 0.95, done=done)
    if thumb is not None:
        a, b = (-70, 150, -0.30, 0.78), (78, 183, -0.42, 0.78)
        ch.his_thumb(c, k, *[p + (q - p) * thumb for p, q in zip(a, b)])
    c.restore()


def s6_3(k):
    wall(k); tile(k, 0.02, (270, 480))
    _device(k, False, ease(CUR["tl"] / 0.34))
    k.c.restore(); light(k)


def s6_4(k):
    """A tick. His thumbprint, in oil."""
    wall(k); tile(k, 0.02, (270, 480))
    _device(k, True, None if after(3 / 12.0) else max(0.0, 1.0 - 1.4 * CUR["tl"] / 0.25))
    k.c.restore(); light(k)
    flash(k, 0.0, (0.20, 0.66, 0.38), 0.12)


def s6_5(k):
    wall(k); push(k, 0.03, (200, 430))
    client(k, 140, 430, 2.3, "open", "warm", (0.8, 0.0), shut=blink(g12(said() + 0.08)), mouth=code())
    k.c.restore(); light(k)
    speak(k, "R", 28, 152)


def s6_6(k):
    """Her smile turns real. Six drawings."""
    wall(k); push(k, 0.03, (270, 430))
    sofia(k, 270, 420, 4.8, "low", "real" if after(1 / 12.0) else "interested", (-0.6, 0.0))
    k.c.restore(); light(k)


def s6_7(k):
    """The smile goes first. Then her eyes cut hard to Don. He saw, and has gone still."""
    wall(k); push(k, 0.03, (270, 450))
    don(k, 424, 480, 2.3, "still", (-1.2, 0.1) if CUR["tl"] < 9 / 12.0 - 1e-6 else (-0.3, 1.5))
    if CUR["tl"] < 3 / 12.0 - 1e-6:
        sofia(k, 160, 420, 3.5, "low", "real", (-0.6, 0.0))
    else:
        sofia(k, 160, 420, 3.5, "low", "caught", (-0.4, 0.0) if CUR["tl"] < 6 / 12.0 - 1e-6 else (1.0, 0.0), sway=False)
    k.c.restore(); light(k)


def s6_8(k):
    """Her CV, into the welcome pack."""
    wall(k); tile(k, 0.02, (270, 520))
    g = ease(CUR["tl"] / 0.34)
    k.c.translate(26 * (1 - g), 16 - 30 * (1 - g))
    sh.cv_insert(k.c, k, 80, 153, 1.0, hers=True)
    k.c.restore(); light(k)
    speak(k, "off", 26, 330, at=(64, 104))


def s6_9(k):
    """Pam's empty hands."""
    wall(k); push(k, 0.03, (270, 420))
    pam(k, 270, 360, 2.7, "empty", (-0.2, 0.9))
    k.c.restore(); light(k)


# ================================================================ BEAT 07 · the first dollar
def s7_1(k):
    """The handshake framing again. Don pushes the terminal between them. He taps his card."""
    _two(k)
    robot(k, 198, F, 0.50)
    ac.shredder(k, st.SHRED_X, F, 1.0, fill=0.85)
    tap = after(8 / 12.0)
    _two_client(k, "offer", "confident", (0.8, 0.5), roll=False)
    _two_don(k, "hand_out")
    st.card_terminal(k, 268, F - 96, 1.25, state="ok" if after(10 / 12.0) else None)
    rect(k, 244 + (0 if tap else -8), F - 152 + (0 if tap else -8), 26, 17, (0.20, 0.42, 0.84), 77, lw=1.6)
    k.c.restore(); light(k)


def s7_2(k):
    """PAYMENT APPROVED. $1.00. PILOT."""
    wall(k)
    n = int(round(CUR["tl"] * 12))
    z = (0.9, 1.04)[n] if n < 2 else 1.0
    c = k.c
    c.save(); c.translate(270, 470); c.scale(z, z); st.payment(c, k, 0, 0, 2.5); c.restore()
    light(k)
    flash(k, 0.0, (0.20, 0.66, 0.38), 0.25)


def s7_3(k):
    """Green at once. It leans toward the card."""
    wall(k); push(k, 0.03, (300, 480)); floor_line(k, 912)
    st.card_terminal(k, 96, 660, 4.2, state="ok")
    robot(k, 318, 900, 1.9, "approve" if after(1 / 12.0) else "idle", look=(-1, 0))
    k.c.restore(); light(k)
    speak(k, "T", 28, 240, rows=["CONTACT", "APPROVED."])


def s7_4(k):
    """He looks at his own unshaken hand. Then he pumps it. One dollar."""
    wall(k); push(k, 0.03, (270, 450))
    if CUR["tl"] < 5 / 12.0 - 1e-6:
        don(k, 300, 470, 2.2, "hand_out", (-1.2, 0.9))
    else:
        n = int(round((CUR["tl"] - 5 / 12.0) * 12))
        don(k, 300, 470 + (-10, 4, -6, 0)[min(n, 3)], 2.2, "hand_up", (1, -0.6))
    k.c.restore(); light(k)


# ================================================================ BEAT 08 · the celebration
def s8_1(k):
    """It tips the shredder's bin into the cannon."""
    wall(k); push(k, 0.03, (270, 480)); floor_line(k, 912)
    st.cannon(k, 440, 900, 2.5)
    robot(k, 226, 900, 1.9, "tip" if after(lead() + 0.5) else "idle", look=(1, 0), side=1)
    k.c.restore(); light(k)
    speak(k, "T", 24, 240, rows=["FIRST CUSTOMER.", "CELEBRATION", "REQUIRED."])


def _party(k, door=0.0, client_x=150, client_look=(0.8, 0.0), sof_x=372, don_look=(1, 0.0), plook=None, shake=(0, 0),
           boomed=True, client_face="warm"):
    wide(k, open_=door, shake=shake)
    st.cannon(k, 238, F, 1.0)
    robot(k, 176, F, 0.62, "tip" if not boomed else "idle", look=(1, 0), side=1)
    P = st.POS
    if boomed:
        ac.scatter(k, 230, 500, F + 12, 1.0, n=14, seed=9)
    x, f, s = P["pam"]
    pam(k, x, f + pm.HY * s, s, "stand", plook)
    sofia(k, sof_x, F + 3 + so.HY * 0.70, 0.70, "low", "smile" if sof_x > 360 else "recover", (-0.9, -0.2))
    client(k, client_x - 4 * 0.66, F + co.HY * 0.66, 0.66, "open", client_face, client_look, roll=False)
    x, f, s = P["don"]
    don(k, x, f - 302 * s, s, "hand_up" if boomed else "stand", don_look, strips=boomed)


def s8_2(k):
    """Boom. Blue confetti. The blast catches Don full in the face."""
    n = int(round((CUR["tl"] - 1 / 12.0) * 12))
    sh_ = ((7, -5), (-6, 4), (3, -2))[n] if 0 <= n < 3 else (0, 0)
    _party(k, shake=sh_, boomed=n >= 0, client_face="warm" if n < 0 else "shock" if n < 5 else "warm")
    burst(k, 262, F - 96, 1 / 12.0)
    k.c.restore(); light(k)
    flash(k, 1 / 12.0, (1, 1, 1), 0.6)


def s8_3(k):
    """Strips in his face and on his head, still beaming. A hand thrown up for someone to take."""
    wall(k); push(k, 0.03, (270, 480))
    don(k, 262, 500, 2.2, "hand_up", (1, 0.0), mouth=code(), strips=True)
    k.c.restore()
    falling(k, 14, 3); light(k)
    speak(k, "T", 30, 300)


def s8_4(k):
    """Sofia is walking the Client to the door."""
    g = seg(0.0, 1.0)
    _party(k, door=0.85 * seg(0.5, 1.1), client_x=150 - 34 * g, client_look=(-0.7, 0.0), sof_x=372 - 130 * g,
           don_look=(1, 0.0), plook=(-0.9, -0.5))
    k.c.restore()
    falling(k, 12, 5); light(k)


def s8_5(k):
    """She looks at his raised hand. Then at the floor, and starts down."""
    wall(k); push(k, 0.03, (270, 480)); floor_line(k, 884)
    ac.scatter(k, 40, 500, 892, 1.6, n=12, seed=9)
    if after(10 / 12.0):                                   # down, a hand on one strip, and up it comes
        pick = 0.0 if CUR["tl"] < 14 / 12.0 - 1e-6 else 0.5 if CUR["tl"] < 15 / 12.0 - 1e-6 else 1.0
        pam_floor(k, 330, 900 + (6 if within(10 / 12.0, 11 / 12.0) else 0), 1.5, False, pick)
    else:
        pam(k, 300, 900 + pm.HY * 1.5, 1.5, "stand", (-0.8, -0.6) if CUR["tl"] < 5 / 12.0 - 1e-6 else (-0.6, 1.0))
    k.c.restore()
    falling(k, 8, 7); light(k)


# ================================================================ BEAT 09 · the hand and the floor
def s9_1(k):
    """Held: his hand is still up and his eyes are on the door; she is on her knees and, once, looks up at him."""
    world(k, 142, 341, 1.55, amount=0.02)
    ac.scatter(k, 310, 490, F + 24, 1.0, n=16, seed=9)
    g = seg(0.3, 1.6)
    back = after(1.75)
    robot(k, 292, F - 10, 0.46, look=(1, 0), side=1)
    sofia(k, 226 + 150 * g, F - 6 + so.HY * 0.66, 0.66, "trophy" if back else "low", "knowing" if back else "recover",
          (-0.3, 0.6) if back else (0.9, 0.0))
    up = within(1.9, 3.1)
    pick = 0.0 if up else (0.0, 0.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0)[CUR["n"] % 8]          # she keeps collecting
    pam_floor(k, 438, F + 58, 0.66, up, pick)
    don(k, 212, F + 86 - 302 * 1.15, 1.15, "hand_up", (-1.2, -0.3), strips=True)
    k.c.restore()
    falling(k, 10, 9); light(k)


# ================================================================ BEAT 10 · the door
def s10_1(k):
    """At the door, a strip settles in his palm."""
    wall(k); push(k, 0.03, (270, 440))
    pose = co.POSES["open"][:2] + co._ik(1, 112, co.BT + 112)
    o = client(k, 236, 400, 1.7, pose, "puzzled", (0.9, 1.8), roll=False, shut=blink(0.75))
    x, y = o["hands"][1]
    g = seg(0.0, 0.6)
    ac.plan_strip(k, x + 4 + 30 * math.sin(g * 7) * (1 - g), y - 60 - 420 * (1 - g), 0.62, n=7, ang=0.5 + 2.4 * (1 - g))
    k.c.restore()
    falling(k, 5, 11); light(k)


def s10_2(k):
    """White lines on blue: a bay, and a 7."""
    wall(k); tile(k, 0.03, (270, 480))
    hd.palm(k, 90, 249, 4.4, 0.0, co.SKIN, 3)
    n = int(round(CUR["tl"] * 12))
    ac.plan_strip(k, 88, 159 + ((-4, 2)[n] if n < 2 else 0), 1.0, n=7, ang=0.35 + ((0.10, -0.04)[n] if n < 2 else 0))
    k.c.restore(); light(k)


def s10_3(k):
    """Into his pocket, his eyes already back on the room. He checks his watch, and goes."""
    wall(k); push(k, 0.03, (270, 440))
    if CUR["tl"] < 6 / 12.0 - 1e-6:
        client(k, 236, 400, 1.7, "stand", "warm", (0.8, -0.1), shut=blink(0.08), roll=False)
    else:
        pose = co.POSES["open"][:2] + co._ik(1, 52, co.BT + 74)
        client(k, 236, 400, 1.7, pose, "confident", (0.9, 2.2) if CUR["tl"] < 12 / 12.0 - 1e-6 else (-0.8, 0.0), roll=False)
    k.c.restore()
    falling(k, 3, 13); light(k)


def s10_4(k):
    """The door slides shut behind him. The robot stamps the glass. Don's hand is still up; Pam looks up at him."""
    tl = CUR["tl"]
    op = 0.85 * (1 - seg(0.0, 0.5))
    n = int(round((tl - 8 / 12.0) * 12))
    wide(k, open_=op, shake=((0, 3), (0, -2))[n] if 0 <= n < 2 else (0, 0))
    c = k.c
    _through_glass(k, lambda: ac.client(k, 112 - 14 * seg(0.0, 1.6), F + 6, 0.50, "watch", look=(-0.9, 2.2)), op)
    if n >= 0:
        st.stamp(c, st.STAMP_AT[0], st.STAMP_AT[1], 0.74 * ((1.12, 1.0)[n] if n < 2 else 1.0))
    ac.scatter(k, 214, 286, F + 10, 1.0, n=7, seed=4)
    ac.scatter(k, 322, 478, F + 30, 1.0, n=13, seed=9)
    robot(k, 204, F, 0.62, "stamp" if tl >= 5 / 12.0 - 1e-6 else "idle", look=(-1, 0), side=-1)
    don(k, 292, F + 6 - 302 * 0.72, 0.72, "hand_up", (-1.2, -0.4), strips=True)
    pam_floor(k, 446, F + 46, 0.63, tl >= 1.5 - 1e-6)
    c.restore()
    falling(k, 6, 15); light(k)


ANIM = {s["shot"]: globals()["s" + s["shot"].replace(".", "_")] for s in T["shots"]}


# ---------------------------------------------------------------- drawing and rendering
def shot_at(t):
    n = int(math.floor(t * 12 + 1e-6))
    for s in T["shots"]:
        if s["n0"] <= n < s["n0"] + s["nd"]:
            return s
    return T["shots"][-1]


def draw(c, t, w=540):
    """The drawing for film time t (quantised to the 12 fps grid) into a context w pixels wide."""
    n = int(math.floor(t * 12 + 1e-6))
    s = shot_at(t)
    tl = (n - s["n0"]) / 12.0
    CUR.update(t=n / 12.0, tl=tl, d=s["d"], u=tl / s["d"], shot=s["shot"], n=n)
    PX[0] = w / float(W)
    ANCH.clear(); QA["bubbles"] = []; QA["faces"] = []
    c.save(); c.scale(PX[0], PX[0])
    m = c.get_matrix(); m.invert(); BASE[0] = m
    c.rectangle(0, 0, W, H); c.clip()
    k = Ctx(c, 0 if OPT["plain"] else CUR["n"] % 3)
    ANIM[s["shot"]](k)
    if not OPT["plain"]:
        kit.grain(k, 0.06)
    c.restore()


def still(t, w=540):
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, w, w * 16 // 9)
    draw(cairo.Context(surf), t, w)
    return surf


def sheet(out, t0, t1, step=1 / 3.0, cols=9, s=0.5, numbers=False):
    ts, t = [], t0
    while t < t1 - 1e-6:
        ts.append(t); t += step
    tw, th = int(W * s), int(H * s)
    rows = (len(ts) + cols - 1) // cols
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, cols * (tw + 6) + 6, rows * (th + 26) + 6)
    c = cairo.Context(surf); c.set_source_rgb(0.16, 0.16, 0.18); c.paint()
    for i, t in enumerate(ts):
        x, y = 6 + (i % cols) * (tw + 6), 6 + (i // cols) * (th + 26)
        c.save(); c.translate(x, y); c.rectangle(0, 0, tw, th); c.clip(); draw(c, t, tw); c.restore()
        c.set_source_rgb(1, 1, 1); c.select_font_face("Inter", 0, 1); c.set_font_size(13)
        c.move_to(x, y + th + 17); c.show_text(("%d" % (i + 1)) if numbers else "%s  %.2f s" % (shot_at(t)["shot"], t))
    surf.write_to_png(out)
    return len(ts)


def render_beat(b, w, path):
    """One encoded file for one beat: 30 fps out, a new drawing 12 times a second."""
    t0, t1 = beat_span(b)
    h = w * 16 // 9
    tmp = path[:-4] + ".part.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", "%dx%d" % (w, h),
                          "-r", str(FPS), "-i", "-", "-vf", "scale=out_color_matrix=bt709", "-c:v", "libx264", "-preset",
                          "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries",
                          "bt709", "-color_trc", "bt709", "-an", tmp], stdin=subprocess.PIPE)
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    c = cairo.Context(surf)
    f0, f1 = int(round(t0 * FPS)), int(round(t1 * FPS))
    prev, buf = None, None
    for f in range(f0, f1):
        key = int(math.floor(f / float(FPS) * 12 + 1e-6))
        if key != prev:
            c.set_source_rgb(1, 1, 1); c.paint()
            draw(c, f / float(FPS), w)
            surf.flush(); buf = bytes(surf.get_data()); prev = key
        p.stdin.write(buf)
    p.stdin.close()
    if p.wait() != 0:
        raise SystemExit("ffmpeg failed on beat %s" % b)
    os.replace(tmp, path)
    return f1 - f0


def render(out, w=1080):
    from multiprocessing import Pool
    tmp = "/tmp/ob_anim_%s_%d" % (V, w)
    os.makedirs(tmp, exist_ok=True)
    jobs = [(b, w, os.path.join(tmp, "beat%s.mp4" % b)) for b in BEATS]
    with Pool(2) as pool:
        n = sum(pool.starmap(render_beat, jobs))
    lst = os.path.join(tmp, "list.txt")
    open(lst, "w").write("".join("file '%s'\n" % j[2] for j in jobs))
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", out])
    print("wrote", out, "%.2f s, %d frames" % (T["total"], n))


def film(out):
    """The film with its sound: the mix on this timing, one constant gain to -14 LUFS."""
    import sound_ob_mix_v2 as mx
    import sound_bc_mix as bm
    tj = os.path.join(HERE, "ob_anim_timing_%s.json" % V)
    json.dump(T, open(tj, "w"), indent=1)
    wav = os.path.join(HERE, "ob_anim_mix_%s.wav" % V)
    bm.master(mx.main("/tmp/ob_anim_mix_full.wav", timing=tj, anim=3), wav)
    silent = "/tmp/ob_anim_%s_silent.mp4" % V
    render(silent, 1080)
    tmp = out[:-4] + ".tmp.mp4"
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-i", wav, "-map", "0:v", "-map", "1:a",
                           "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", tmp])
    os.replace(tmp, out)
    print("wrote", out)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "timing"
    if cmd == "timing":
        json.dump(T, open(os.path.join(HERE, "ob_anim_timing_%s.json" % V), "w"), indent=1)
        for b in BEATS:
            t0, t1 = beat_span(b)
            print("beat %2s  %6.2f  %5.2f s" % (b, t0, t1 - t0))
        print("total %.2f s, %d shots" % (T["total"], len(T["shots"])))
    elif cmd == "stills":
        for a in sys.argv[3:]:
            still(float(a), 540).write_to_png(os.path.join(sys.argv[2], "ob_anim_%06.2f.png" % float(a)))
    elif cmd == "sheet":
        t0, t1 = beat_span(sys.argv[3]) if len(sys.argv) > 3 else (0.0, T["total"])
        sheet(sys.argv[2], t0, t1)
    elif cmd == "qa":
        import qa_ob_v1 as qa_ob
        sys.exit(1 if qa_ob.main() else 0)
    elif cmd == "film":
        film(sys.argv[2])
    elif cmd == "render":
        render(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 1080)
