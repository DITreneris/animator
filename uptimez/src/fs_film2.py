"""FIRST SEARCH (episode 10): the film on shot list v2 (first-search/fs_shot_list_v2.md, picked 19 Nov): 20 shots
instead of 36. Where the next beat happens in the same place with the same people, the camera moves instead of cutting:
a merged shot keeps one camera (its first beat's) for all its beats, and a camera move (a push-in, a pull-back, a tilt)
runs over the drawing. A push-in that ends on a thing cuts to that thing's insert at the same size (a match cut).

The long pacing (picked 19 Nov): the same timeline as fs_film_long (animatic v26's), so the voices and effects sit
where they sat; "Eww." is Happy Compliance's (fs_voices/film_v10).

  python3 fs_film2.py [dir] [540|1080]   -> fs_film2_long_540.mp4 / fs_film2_long_1080.mp4
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
from kit import Ctx
import fs_storyboard as sb
import fs_animatic as an
import fs_anim as fa
import sound_xmas as sx
import sound_bc_mix as bm
import sound_iwry as si
import sound_ob_mix as om
import sound_fs_music as mus
import iwry_mouths as im
import client_ob as co
import sofia_fs as sfs
import mom_fs as mfs

HERE = os.path.dirname(os.path.abspath(__file__))
W, H, DR = 540, 960, 15
SR = an.SR
VOICES = "fs_voices/film_v10"
TIMING, LEAD = "fs_timing_v26.json", 0.15

# (new shot, the old shots it is made of: their drawings are its beats, in order)
LIST2 = [("A", ["1.1a", "1.1b"]), ("B", ["1.2", "1.3"]), ("C", ["2.1", "2.2", "2.3"]), ("D", ["3.2"]),
         ("E", ["3.1", "3.3", "3.4"]), ("F", ["4.1", "4.2", "4.3", "4.4"]), ("H", ["4.5", "5.1", "5.2"]),
         ("I", ["5.2b"]), ("J", ["5.2c"]), ("K", ["5.3"]), ("L", ["6.1b"]), ("M", ["6.2a", "6.2b"]), ("N", ["7.1"]),
         ("O", ["7.2", "7.3"]), ("P", ["7.4"]), ("Q", ["7.5", "8.1"]), ("R", ["8.2"]), ("S", ["9.1"]), ("T", ["9.2"]),
         ("U", ["9.3", "9.4", "9.5"])]
# the drawing each old shot's time shows in its merged shot (None: the merged shot's lead drawing carries on)
DRAW = {"2.1": "2.2", "2.3": "2.2", "4.2": "4.1", "4.3": "4.1", "4.4": "4.1", "4.5": "5.1", "5.2": "5.1",
        "8.1": "7.5", "9.3": "9.3"}
# a merged shot shares one camera: the camera of this drawing
SHARE = {"E": "3.3", "F": "4.1", "H": "5.1", "Q": "7.5"}
FORCE = [None]
ANCH = {}
ANCHD = {}                                                 # drawing -> its anchors


def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


class _forced:
    """While FORCE is set: every scene is drawn through that camera (no autoframe, no banner slide)."""
    def __enter__(self):
        self.f, self.af, self.br = sb._scene4, sb._autoframe, sb._banner_rule
        f0 = self.f
        def s4(k, cam, *a):
            if FORCE[0]:
                old = sb.CAM4[0]
                sb.CAM4[0] = FORCE[0]
                try:
                    return f0(k, cam, *a)
                finally:
                    sb.CAM4[0] = old
            return f0(k, cam, *a)
        sb._scene4 = s4
        sb._autoframe = lambda cam4, heads: FORCE[0] or self.af(cam4, heads)
        sb._banner_rule = lambda cam4, heads, cam0: FORCE[0] or self.br(cam4, heads, cam0)
        return self
    def __exit__(self, *e):
        sb._scene4, sb._autoframe, sb._banner_rule = self.f, self.af, self.br


class _anchors:
    """Where things land on the canvas: the card, the tablet, the screen (for the moves and overlays)."""
    def __enter__(self):
        fs = sb.fs
        self.p2, self.tb, self.sc = fs.phone2, fs.tablet_upgrade, fs.screen
        p2, tb, sc = self.p2, self.tb, self.sc
        def phone2(k, x, y, s=1.0, kind="bank", *a, **kw):
            if kind == "cal":
                ANCH["card"] = k.c.user_to_device(x, y) + (k.c.user_to_device_distance(92 * s, 0)[0],)
            return p2(k, x, y, s, kind, *a, **kw)
        def tablet(k, x, y, s=1.0, *a, **kw):
            ANCH["tablet"] = k.c.user_to_device(x, y) + (k.c.user_to_device_distance(140 * s, 0)[0],)
            return tb(k, x, y, s, *a, **kw)
        def screen(k, kind, x, y, w, h, *a, **kw):
            p0 = k.c.user_to_device(x, y); p1 = k.c.user_to_device(x + w, y + h)
            ANCH["screen"] = (p0[0], p0[1], p1[0], p1[1])
            return sc(k, kind, x, y, w, h, *a, **kw)
        fs.phone2, fs.tablet_upgrade, fs.screen = phone2, tablet, screen
        return self
    def __exit__(self, *e):
        sb.fs.phone2, sb.fs.tablet_upgrade, sb.fs.screen = self.p2, self.tb, self.sc


def drawing_for(key, t_old):
    if key == "1.3" and t_old < 1.2:                        # B: the push-in onto the card runs on into 1.3's time
        return "1.2"
    return DRAW.get(key, key)


def draw_beat(key, t_old, ln_old, fns, S, Z):
    """The drawing for old shot `key` (DRAW maps it to the drawing its time shows) at its own time, on a canvas Z times
    the frame (for the digital moves). Returns (surface, heads, avoid), heads and boxes in frame units."""
    d = drawing_for(key, t_old)
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(W * S * Z), int(H * S * Z)); surf.set_device_scale(S * Z, S * Z)
    c = cairo.Context(surf); k = Ctx(c, 0)
    sb.bg(c)
    sb.ANIM.clear(); sb.ANIM.update(fa.motion_all(d, t_old, ln_old))
    sb.ANIM.update(EXTRA.get(d if d != DRAW.get(key, key) else key, {}))
    sb.HEADS.clear(); sb.AVOID.clear()
    ANCH.clear()
    with sb._norm(record_only=True):
        fns[d](k)
    ANCHD.setdefault(d, {}).update(ANCH)
    return surf, dict(sb.HEADS), list(sb.AVOID)


EXTRA = {"1.2": {"card": True}, "1.3": {}, "5.2": {"cl_look": (1, -0.2), "cl_face": "suspicious"},
         "4.5": {"cl_face": "plain"}, "8.1": {"q_plan": True}}


def move(shot, u, ln, t):
    """The digital camera over a merged shot: (focus x, focus y, zoom) in frame units; zoom 1 = the board's framing."""
    a = dict(ANCHD.get("1.2", {})); a.update({k_: v for k_, v in ANCHD.get("2.2", {}).items() if k_ == "tablet"})
    if shot == "B":                                        # the push-in onto the card, then the insert (match cut)
        if "card" in a and t < 2.2:
            cx, cy, w = a["card"]
            zt = min(5.0, 0.62 * 540 / max(1, w))
            v = ease((t - 0.7) / 1.5)
            return (270 + (cx - 270) * v, 480 + (cy - 480) * v, 1 + (zt - 1) * v)
    if shot == "C":                                        # his eyes light up (close on his face), then pull back
        h = HEADS_LEAD.get("don")
        if h and t < 1.0:
            v = 1 - ease((t - 0.45) / 0.55)
            return (270 + (h[0] - 270) * v, 480 + (h[1] + 40 - 480) * v, 1 + 0.9 * v)
    if shot == "E":                                        # the tilt up with her, onto the plaster (into 3.4)
        if 2.6 <= t < 3.0:
            v = ease((t - 2.6) / 0.4)
            return (270, 480 - 260 * v, 1 + 0.25 * v)
    if shot == "F":                                        # the push-in onto the robot's screen at APPROVED
        h = HEADS_LEAD.get("robot")
        if h and t > 5.0:
            v = ease((t - 5.0) / 1.2)
            return (270 + (h[0] - 270) * v, 480 + (h[1] + 1.4 * h[2] - 480) * v, 1 + 1.1 * v)
    if shot == "O":                                        # the push-in onto the lick (into 7.3)
        h = HEADS_LEAD.get("mom")
        if h and 0.55 <= t < 0.9:
            v = ease((t - 0.55) / 0.35)
            return (270 + (h[0] - 270) * v, 480 + (h[1] - 480) * v, 1 + 1.2 * v)
    if shot == "U":                                        # the pull-back from the healed portrait to Don under it
        if 1.2 <= t < 2.6:
            p = PORT_AT.get("p")
            if p:
                v = 1 - ease((t - 1.2) / 1.4)
                return (270 + (p[0] - 270) * v, 480 + (p[1] - 480) * v, 1 + 1.6 * v)
    if shot == "A":
        return (270, 480, 1.0)
    return (270, 480, 1 + 0.03 * u)                        # the board's framing, a slow push


HEADS_LEAD = {}
PORT_AT = {}


def overlay(shot, key, t, t_old, c, tf):
    """Things drawn over the frame in a merged shot: the thumb coming in (C), the sweep to green (H), APPROVED (F)."""
    if shot == "C" and key == "2.3" and "tablet" in ANCHD.get("2.2", {}):
        x, y, w = ANCHD["2.2"]["tablet"]
        x, y = tf(x, y)
        v = ease(t_old / 0.35)
        sb.thumb(Ctx(c, 0), x + 30, y + 40 + 260 * (1 - v), 0.9, sb.SKIN_CL, oil=True, ang=2.55, who="client")
    if shot == "H" and key == "4.5" and "screen" in ANCHD.get("5.1", {}):
        x0, y0, x1, y1 = ANCHD["5.1"]["screen"]
        (x0, y0), (x1, y1) = tf(x0, y0), tf(x1, y1)
        v = ease(t_old / 0.9)                              # the red half wiped to green, left to right
        bx0, by0 = x0 + (x1 - x0) * 0.08, y0 + (y1 - y0) * 0.50
        bx1, by1 = x1 - (x1 - x0) * 0.08, y1 - (y1 - y0) * 0.10
        xm = bx0 + (bx1 - bx0) * (0.5 + 0.5 * v)
        if xm < bx1:
            c.set_source_rgb(0.86, 0.15, 0.17); c.rectangle(xm, by0, bx1 - xm, by1 - by0); c.fill()
    if shot == "F" and key in ("4.3", "4.4"):
        h = HEADS_LEAD.get("robot")
        if h:
            x, y = tf(h[0], h[1] + 1.45 * h[2]); r = h[2]
            z = tf(1, 0)[0] - tf(0, 0)[0]
            sw, sh = 1.7 * r * z, 0.55 * r * z
            c.set_source_rgb(0.12, 0.13, 0.16); c.rectangle(x - sw / 2 - 4, y - sh / 2 - 4, sw + 8, sh + 8); c.fill()
            c.set_source_rgb(0.20, 0.72, 0.40); c.rectangle(x - sw / 2, y - sh / 2, sw, sh); c.fill()
            c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
            c.set_font_size(sh * 0.5); e = c.text_extents("APPROVED")
            c.set_source_rgb(1, 1, 1); c.move_to(x - e.x_advance / 2, y + e.height / 2); c.show_text("APPROVED")


# ---------------------------------------------------------------- v2b (19 Nov, the director's QA): the opening and the mouths
CUR_T = [0.0]
TALK = {}                                                   # name -> mouth code (iwry_mouths: M A E O U F C, "" rest)
DOOR_CAM = (178, 596, 2.05)


A_LEN = 4.4                                               # v3: the opening, longer (was 2.0 s): the film grows 2.4 s
DOOR_CAM = (150, 648, 1.65)                                # the door, framed like frame 0 (clear of the dead zone)
T_OPEN, T_IN, T_SHUT, T_SLAM = 1.5, 1.7, 2.2, 2.5          # the door opens, he steps in, it slides shut, slams
T_BACK0, T_BACK1 = 2.6, 3.5                                # the camera back to Don (slow)
T_DROP0, T_DROP1 = 3.55, 3.8                               # the portrait falls; lands round his neck (BONK)


def opening(k):
    """A, 4.4 s (the director, 19 Nov): Don under the portrait (frame 0); the camera eases over to the glass door; the
    Client walks in; the door slides shut and slams; the wall shakes; the camera eases back to Don, the portrait still
    trembling; it drops onto his head and hangs from his neck by its wire; he does not blink."""
    t = CUR_T[0]
    c = k.c
    v = ease((t - 0.5) / 1.0) - ease((t - T_BACK0) / (T_BACK1 - T_BACK0))
    cam = tuple(a + (b - a) * v for a, b in zip(sb.WIDE27, DOOR_CAM))
    sh = 7 * math.sin(2 * math.pi * 13 * (t - T_SLAM)) * math.exp(-(t - T_SLAM) * 5) if t > T_SLAM else 0.0
    FORCE[0] = (cam[0] + sh / cam[2], cam[1] + 0.5 * sh / cam[2], cam[2])
    op = 0.85 * ease((t - T_OPEN) / 0.25) - 0.85 * ease((t - T_SHUT) / (T_SLAM - T_SHUT))
    wob = 0.09 * math.sin(2 * math.pi * 5 * (t - T_SLAM)) * math.exp(-(t - T_SLAM) * 0.9) if t > T_SLAM else 0.0
    s_p = sb.fs.PORTRAIT_S * 0.88

    def ex(k_, o):
        c_ = k_.c
        hx, hy = o["don"]["head"]
        r = 50 * sb.SC["don"]
        nx, ny = hx, hy + 0.95 * r
        px0, py0 = sb.PORT27
        if t < T_DROP0:                                     # on its nail; after the slam, trembling
            sb.fs.portrait(k_, px0, py0 + (-4 if T_SLAM < t < T_SLAM + 0.06 else 0), s_p, ang=wob, crack=False,
                           patch=False)
        else:
            u = min(1.0, (t - T_DROP0) / (T_DROP1 - T_DROP0))
            cy_end = ny + 82 * s_p / 1.12
            x_ = px0 + (nx - px0) * u
            y_ = py0 + (cy_end - py0) * u * u
            sw = (-0.16 * math.sin(2 * math.pi * 2.2 * (t - T_DROP1)) * math.exp(-(t - T_DROP1) * 3)) if t > T_DROP1 else 0.25 * u
            if t > T_DROP1:                                 # the wire round his neck
                c_.set_source_rgb(0.35, 0.33, 0.30); c_.set_line_width(1.6)
                c_.move_to(x_ - 34, y_ - 66 * s_p / 1.12); c_.line_to(nx - 18, ny - 6); c_.stroke()
                c_.move_to(x_ + 34, y_ - 66 * s_p / 1.12); c_.line_to(nx + 18, ny - 6); c_.stroke()
            sb.fs.portrait(k_, x_, y_, s_p, ang=sw, crack=t > T_DROP1, patch=False)
    landed = t > T_DROP1
    dip = 5 if T_DROP1 < t < T_DROP1 + 0.1 else 0
    walk = ease((t - T_IN) / 0.7)
    bob = -4 * abs(math.sin(math.pi * 3 * walk)) if 0 < walk < 1 else 0
    sb.scene(k, screen="query", portrait=None, door=max(0.0, op), rb=dict(x4=True, state="eager"),
             cl=False if t < T_IN else dict(x4=True, x=70 + 90 * walk, feet=sb.F - 14 + bob, pose="arrive",
                                            face="confident", look=(1, 0) if t < T_SLAM else (1, -0.4)),
             sf=False if t < 0.9 else dict(x4=True, face="charm", look=(-1, 0)),
             dn=dict(x4=True, feet=sb.F + 16 + dip, face="neutral" if landed else "happy",
                     look=(0, -0.6) if landed else (0, 0)), extra=ex)


def _vis(code, i):
    return code[i] if 0 <= i < len(code) else ""


class _mouths:
    """Mouth shapes on the faces' own mouths (The Onboarding's way): Don and Sofía get iwry_mouths over theirs, the
    Client his own mouth=, Mom her A / E / O. Don's mic is up while he talks (it read as a moustache)."""
    def __enter__(self):
        self.don, self.cl, self.sf, self.mom = sb.don, sb.client, sfs.sofia, mfs.mom
        d0, c0, s0, m0 = self.don, self.cl, self.sf, self.mom

        def don(k, x, feet, s, pose="stand", face="neutral", look=(-1, 0)):
            code = TALK.get("don")
            old = sb.DON_STATE[0]
            if code is not None and old:
                sb.DON_STATE[0] = ("up", old[1])
            try:
                o = d0(k, x, feet, s, pose, face, look)
            finally:
                sb.DON_STATE[0] = old
            if code:
                c = k.c
                hx, hy = o["head"]
                c.save(); c.translate(hx, hy); c.scale(s, s); im.don_mouth(k, (0, 0), code); c.restore()
            return o

        def client(k, x, feet, s, pose="stand", face="confident", look=(0.9, 0)):
            code = TALK.get("client")
            o = co.client(k, x, feet, s, pose, face, look, mouth=code or None)
            sb.pocket_strip(k, o, s, x, feet)
            return o

        def sofia(k, x, feet, s=1.0, *a, **kw):
            o = s0(k, x, feet, s, *a, **kw)
            code = TALK.get("sofia")
            if code:
                c = k.c
                hx, hy = o["head"]
                c.save(); c.translate(hx, hy); c.scale(s, s); im.sof_mouth(k, (0, 0), code); c.restore()
            return o

        def mom(k, x, feet, s=1.0, pose="bag", face="sweet", *a, **kw):
            code = TALK.get("mom")
            if code and kw.get("mouth") is None:
                kw["mouth"] = {"A": "A", "O": "O", "U": "O", "E": "E", "C": "E", "F": "E"}.get(code)
            return m0(k, x, feet, s, pose, face, *a, **kw)
        sb.don, sb.client, sfs.sofia, mfs.mom = don, client, sofia, mom
        return self

    def __exit__(self, *e):
        sb.don, sb.client, sfs.sofia, mfs.mom = self.don, self.cl, self.sf, self.mom


WHO2 = {"DON": ["don"], "SOFIA": ["sofia"], "CLIENT": ["client"], "MOM": ["mom"], "PAM+SOFIA": ["sofia"]}


def build(d, S=1, music="A"):
    an.VOICES = VOICES
    an.TAKES = json.load(open(os.path.join(HERE, VOICES, "takes.json")))
    rows = json.load(open(os.path.join(d, TIMING)))
    grow = A_LEN - (rows[0]["len"] + rows[1]["len"])        # v3: the opening is longer; everything after it moves
    rows[1]["len"] = round(rows[1]["len"] + grow, 3)
    for r in rows[2:]:
        r["start"] = round(r["start"] + grow, 3)
    json.dump(rows, open(os.path.join(d, "fs_timing_film3.json"), "w"), indent=1)
    old = {r["shot"]: r for r in rows}
    fns = {s: fn for s, _, fn, _ in sb.SHOTS}
    total = rows[-1]["start"] + rows[-1]["len"]
    lines_abs = []
    voice = np.zeros(int((total + 1) * SR))
    for s in [r["shot"] for r in rows]:
        if s in an.LINE_OF:
            key = an.LINE_OF[s]
            m = an.TAKES[key]
            wav = os.path.join(HERE, VOICES, "%s.wav" % key)
            a, _ = sf.read(wav)
            a = a.mean(1) if a.ndim > 1 else a
            t0 = old[s]["start"] + LEAD
            an._at(voice, a, t0, 1.0)
            import sound_bc as bc
            vis = bc.visemes(np.asarray(a, dtype=np.float64), m["text"]) if m["who"] != "ROBOT" else []
            lines_abs.append((m["who"], m["text"], t0, t0 + m["len"], vis))
    out_dir = "/tmp/fs_film2_%d" % (540 * S)
    shutil.rmtree(out_dir, ignore_errors=True); os.makedirs(out_dir)
    n = 0
    fns["1.1a"] = sb._with_state("1.1a", opening)            # the new opening (both of A's beats)
    DRAW["1.1b"] = "1.1a"
    with _forced(), _anchors(), _mouths():
        for shot, keys in LIST2:
            t0s = old[keys[0]]["start"]
            ln = sum(old[k_]["len"] for k_ in keys)
            FORCE[0] = None
            ANCHD.clear(); HEADS_LEAD.clear(); PORT_AT.clear()
            CUR_T[0] = 0.0; TALK.clear()
            lead_draw = SHARE.get(shot)                    # the shared camera: the lead drawing's own
            if lead_draw:
                draw_beat(lead_draw, 0.0, old[lead_draw]["len"] if lead_draw in old else 1.0, fns, 1, 1)
                FORCE[0] = sb.LASTCAM[0]
            first = DRAW.get(keys[0], keys[0])
            _, hl, _ = draw_beat(keys[0] if not lead_draw else lead_draw, 0.0, 1.0, fns, 1, 1)
            HEADS_LEAD.update(hl)
            if os.environ.get("FS_DEBUG"):
                print(shot, "lead heads", {k_: tuple(round(v) for v in h) for k_, h in hl.items()}, "force", FORCE[0])
            if shot == "U":                                # where the portrait hangs in frame 0
                surf, hl2, _ = draw_beat("9.4", 0.0, 1.0, fns, 1, 1)
                p = sb.PORT27
                PORT_AT["p"] = (270 + (p[0] - sb.WIDE27[0]) * sb.WIDE27[2], 480 + (p[1] - sb.WIDE27[1]) * sb.WIDE27[2])
            for k_ in keys:                                # anchors of every beat (the card, the tablet, the screen)
                draw_beat(k_, 0.0, old[k_]["len"], fns, 1, 1)
            local = [(w, tx, a - t0s, b - t0s, e) for w, tx, a, b, e in lines_abs if a < t0s + ln and b + 0.25 > t0s]
            fa.BUB.clear()
            for j in range(int(round(ln * DR))):
                t = j / DR
                key = keys[-1]
                for k_ in keys:
                    if t < old[k_]["start"] - t0s + old[k_]["len"] - 1e-6:
                        key = k_; break
                t_old = t - (old[key]["start"] - t0s)
                Z = 3 if shot in ("B", "C", "E", "F", "O", "U") else 1                # room to push in, sharp
                act = [x for x in local if x[2] - 0.1 <= t < x[3] + 0.05]
                TALK.clear()
                for who, text, a0, a1, vis in act:
                    for nm in WHO2.get(who, []):
                        TALK[nm] = _vis(vis, int((t - a0) * 12) + 1) or "M"
                CUR_T[0] = t
                drawing = drawing_for(key, t_old)
                surf_b, heads, avoid = draw_beat(key, t_old, old[key]["len"], fns, S, Z)
                fx, fy, z = move(shot, t / ln, ln, t)
                out = cairo.ImageSurface(cairo.FORMAT_RGB24, W * S, H * S); out.set_device_scale(S, S)
                c0 = cairo.Context(out)
                sb.bg(c0)                                  # beyond the drawing's edge (a tilt): the wall
                c0.save(); c0.translate(270, 480); c0.scale(z, z); c0.translate(-fx, -fy)
                pat = cairo.SurfacePattern(surf_b); pat.set_filter(cairo.FILTER_GOOD)
                c0.set_source(pat); c0.paint(); c0.restore()
                tf = lambda x, y: ((x - fx) * z + 270, (y - fy) * z + 480)
                heads_t = {nm: tf(x, y) + (r * z,) for nm, (x, y, r) in heads.items()}
                overlay(shot, key, t, t_old, c0, tf)
                for who, text, a0, a1, env in local:
                    if a0 <= t < a1 + 0.25:
                        bk = (shot, text)
                        if bk not in fa.BUB:
                            fa.BUB[bk] = (heads_t, [tf(b[0], b[1]) + tf(b[2], b[3]) for b in avoid])
                        hh, av = fa.BUB[bk]
                        sb.AVOID[:] = av
                        nn = int(round((t - max(a0, 0)) * DR))
                        pop = (0.82, 1.05)[nn] if (nn < 2 and a0 >= 0) else 1.0
                        dry = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); dc = cairo.Context(dry)
                        box = fa._say_box(dc, Ctx(dc, 0), who, text, hh)
                        bx, by = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
                        c0.save(); c0.translate(bx, by); c0.scale(pop, pop); c0.translate(-bx, -by)
                        an.say(c0, Ctx(c0, 0), who, text, hh)
                        c0.restore()
                out.write_to_png("%s/f%05d.png" % (out_dir, n)); n += 1
            FORCE[0] = None
    sb.ANIM.clear(); fa.MOUTH[0] = None
    oldlead = an.LEAD
    an.LEAD = LEAD
    try:
        m = an.mix(rows, total)
    finally:
        an.LEAD = oldlead
    m = m[:len(voice)] if len(m) >= len(voice) else np.pad(m, (0, len(voice) - len(m)))
    m[:int(A_LEN * SR)] = 0.0                              # the animatic's opening is gone; the new one:
    an._at(m, om.door(0.30), T_OPEN, 0.30)                 # the glass door slides open
    for i_ in range(3):                                    # his steps in
        an._at(m, sx.thunk(0.04, 600), T_IN + 0.08 + i_ * 0.24, 0.12)
    an._at(m, om.door(0.25), T_SHUT, 0.25)                 # it slides shut...
    an._at(m, sx.thunk(0.3, 80), T_SLAM, 0.90)             # ...and slams; the wall shakes
    an._at(m, si.servo(0.25, 700, 760), T_DROP0 - 0.25, 0.10)   # the wire slipping off the nail
    an._at(m, sx.whoosh(0.2), T_DROP0, 0.25)
    an._at(m, sx.thunk(0.35, 150), T_DROP1, 1.0)           # BONK
    an._at(m, bm.chime([2400, 3100], 0.03, 0.4), T_DROP1 + 0.04, 0.12)
    at = {r["shot"]: r["start"] for r in rows}
    for i in range(3):
        an._at(m, sx.thunk(0.04, 700), at["7.2"] + 0.05 + i * 0.25, 0.05)
    env = (np.abs(voice) > 0.01).astype(float)
    env = si.lp(env, int(SR * 0.35)); env = env / max(1e-6, env.max())
    b = mus.bed(music, len(voice) / SR, T_DROP1 + 0.1)     # the theme starts on the bonk
    b = b[:len(voice)] if len(b) >= len(voice) else np.pad(b, (0, len(voice) - len(b)))
    mix = m + b * (0.16 - 0.12 * np.clip(env * 4, 0, 1))
    mix = mix[:int(total * SR)]
    mix *= 0.5 / max(1e-6, np.abs(mix).max())
    wav = os.path.join(out_dir, "mix.wav")
    sf.write(wav, np.stack([mix, mix], 1).astype(np.float32), SR)
    out = os.path.join(d, "fs_film3_%s_%d.mp4" % (music, 540 * S))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(DR), "-i", "%s/f%%05d.png" % out_dir, "-i", wav,
                    "-vf", "fps=30,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p", "-c:v", "libx264",
                    "-preset", "veryfast", "-crf", "18", "-colorspace", "bt709", "-color_primaries", "bt709",
                    "-color_trc", "bt709", "-color_range", "tv", "-frames:v", str(int(round(total * 30))),
                    "-af", "loudnorm=I=-14.5:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
                    "-t", "%.3f" % total, "-movflags", "+faststart", out], check=True)
    for _ in range(2):                                     # two passes to the target (single-pass loudnorm fell short)
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
    print("wrote", out, "%.2f s, %d shots" % (total, len(LIST2)))
    return out


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "../first-search"
    build(d, 2 if (len(sys.argv) > 2 and sys.argv[2] == "1080") else 1, sys.argv[3] if len(sys.argv) > 3 else "A")
