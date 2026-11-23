"""UptimeZ: the shared checker (series/production-process.md, rule 2). It runs on every render, and a failed check stops
the build with the shot, the frame and the reason.

Two halves:
  1. A RECORDER installed in the renderer's process before it builds. It records what is drawn, frame by frame:
     the text on the set (signs), the speech bubbles and where their tails end, the faces (sb.HEADS) after the camera,
     every arm a character rig draws (and whether it is visible), effect marks, and which function drew each shot.
     It needs no change to the renderer: it wraps cairo.Context, kit.arm, the character functions and the bubble code
     from outside. New code that draws a limb or an effect mark by hand must declare it (limb(), mark()), or the
     checker cannot see it.
  2. CHECKS on the records and on the encoded film: drawing map, scale, signs, tails, limbs, strays, text, loop,
     sound, format.

A frame is composed in two steps in our builders: the shot is drawn on a scene surface (ARGB32, set units), the camera
(move()) maps it onto the 540x960 frame (RGB24). The recorder tells them apart by the surface's format; render at 1080
(scale 2) so the frame surface is never the same size as a dry 540 pass.

Every check is validated on a failure we really had (uz_check_validate.py); a check that never failed is not a check.
"""
import math
import sys

import importlib
import types
import cairo

W, H = 540, 960
SAFE = (18, 96, 522, 820)          # bubbles and cards (CLAUDE.md, G5)
BOTTOM, RAIL = 720, (470, 380, 860)  # faces: not in the apps' bottom quarter, not under the right-hand buttons
MOUTH = (0.15, 1.50, 1.70)         # a tail tip must be between y+0.15r and y+1.5r of the face point (eye level), |dx| <= 1.7r
EDGE = 2.0                         # px of slack at the frame's edge


# ---------------------------------------------------------------------------------------------------- the recorder
class Rec:
    def __init__(self):
        self.frames = []            # one dict per composed frame
        self.scene = None           # what the scene surface collected since it was made
        self.cam = None             # the last move(): (fx, fy, z)
        self.owner = []             # the character being drawn (a stack)
        self.speech = None          # inside a bubble: the fills
        self.map = {}               # drawing -> the function that drew it
        self.shot = None

    def new_scene(self):
        self.scene = dict(text=[], arms=[], marks=[], strokes=[])

    def new_frame(self, heads):
        f = dict(shot=self.shot, cam=self.cam, heads=heads, scene=self.scene or {}, bubbles=[], text=[])
        self.frames.append(f)
        return f


R = Rec()
_Context = cairo.Context


def _dev(c, x, y):
    return c.user_to_device(x, y)


def _bbox(c, x0, y0, x1, y1):
    pts = [_dev(c, x, y) for x, y in ((x0, y0), (x1, y0), (x0, y1), (x1, y1))]
    return (min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts))


def _seen(c, x, y):
    """the point is inside the current clip (the clip's real shape, not its bounding box)."""
    try:
        return bool(c.in_clip(x, y))
    except Exception:
        return True


def _clip(c):
    try:
        return _bbox(c, *c.clip_extents())
    except Exception:
        return (-1e9, -1e9, 1e9, 1e9)


class RecCtx(_Context):
    """cairo.Context that records. role: 'scene' (ARGB32, big), 'frame' (RGB24, the output), or None (dry, tiny)."""

    def __init__(self, surf):
        _Context.__init__(self)
        self.role = None
        try:
            w, h = surf.get_width(), surf.get_height()
            fmt = surf.get_format()
        except Exception:
            return
        if fmt == cairo.FORMAT_RGB24 and w >= 2 * W and h >= 2 * H:
            self.role = "frame"
            R.new_frame(dict(R.heads_now()))
        elif fmt == cairo.FORMAT_ARGB32 and w >= 2 * W and h >= 2 * H:
            self.role = "scene"
            R.new_scene()

    def show_text(self, s):
        if self.role and s.strip():
            x, y = self.get_current_point()
            e = self.text_extents(s)
            bb = _bbox(self, x + e.x_bearing, y + e.y_bearing, x + e.x_bearing + e.width, y + e.y_bearing + e.height)
            item = dict(text=s, bbox=bb, clip=_clip(self))
            if self.role == "scene" and R.scene is not None:
                R.scene["text"].append(item)
            elif self.role == "frame" and R.frames:
                (R.speech["text"] if R.speech is not None else R.frames[-1]["text"]).append(item)
        return _Context.show_text(self, s)

    def fill(self):
        if self.role == "frame" and R.speech is not None:
            R.speech["fills"].append([_dev(self, *p[1][-2:]) for p in self.copy_path_flat() if p[1]])
        return _Context.fill(self)

    def fill_preserve(self):
        if self.role == "frame" and R.speech is not None:
            R.speech["fills"].append([_dev(self, *p[1][-2:]) for p in self.copy_path_flat() if p[1]])
        return _Context.fill_preserve(self)

    def stroke(self):
        if self.role == "scene" and R.scene is not None and R.owner == []:
            segs = _segments(self)
            if segs:
                R.scene["strokes"].append(dict(segs=segs, clip=_clip(self)))
        return _Context.stroke(self)


def _segments(c):
    """the stroked path as separate straight segments (move_to + one line_to each), in set units; [] if it is not
    made only of those."""
    out, cur = [], None
    for kind, pts in c.copy_path():
        if kind == cairo.PATH_MOVE_TO:
            cur = _dev(c, *pts)
        elif kind == cairo.PATH_LINE_TO and cur is not None:
            p = _dev(c, *pts)
            out.append((cur, p)); cur = None
        else:
            return []
    return out


def _heads_now():
    import fs_storyboard as sb
    return {k: tuple(v) for k, v in sb.HEADS.items()}


R.heads_now = _heads_now


def limb(c, owner, hand):
    """declare a limb drawn by hand (not by a rig): owner and the hand's point in user coordinates."""
    if getattr(c, "role", None) == "scene" and R.scene is not None:
        R.scene["arms"].append(dict(owner=owner, hand=_dev(c, *hand), vis=_seen(c, *hand), how="declared"))


def mark(c, owner, xy):
    """declare an effect mark (lines, dashes, puffs, stars) and whom it belongs to (None: nobody)."""
    if getattr(c, "role", None) == "scene" and R.scene is not None:
        R.scene["marks"].append(dict(owner=owner, at=_dev(c, *xy)))


def _has(m):
    try:
        importlib.import_module(m)
        return True
    except Exception:
        return False


def install(film):
    """wrap everything from outside, in the renderer's process, before it builds."""
    import kit
    import acts_ob as ac
    import fs_animatic as an
    import fs_storyboard as sb
    cairo.Context = RecCtx

    depth = [0]

    def arm_wrap(f0):
        def arm(k, *a, **kw):
            depth[0] += 1
            try:
                hand = f0(k, *a, **kw)
            finally:
                depth[0] -= 1
            c = k.c
            if depth[0] == 0 and getattr(c, "role", None) == "scene" and R.scene is not None and R.owner and hand is not None:
                R.scene["arms"].append(dict(owner=R.owner[-1], hand=_dev(c, *hand[:2]), vis=_seen(c, *hand[:2]), how="rig"))
            return hand
        arm._uz = True
        return arm

    class _Kit(types.ModuleType):              # every arm swapped into kit (acts_ob.arms, pam_fs's pushed sleeves) is
        def __setattr__(self, n, v):           # wrapped as it goes in; an arm inside an arm is counted once
            if n == "arm" and callable(v) and not getattr(v, "_uz", False):
                v = arm_wrap(v)
            types.ModuleType.__setattr__(self, n, v)
    if not isinstance(kit, _Kit) and type(kit) is types.ModuleType:
        kit.__class__ = _Kit
    for mod in (kit, ac):
        if not getattr(mod.arm, "_uz", False):
            mod.arm = arm_wrap(mod.arm)

    def who_wrap(name, f0):
        def f(*a, **kw):
            R.owner.append(name)
            try:
                return f0(*a, **kw)
            finally:
                R.owner.pop()
        f._uz = True
        return f
    import pam_bc as pb
    import mom_fs as mfs
    import sofia_fs as sfs
    for mod, attr, name in ((sb, "don", "don"), (sb, "client", "client"), (sb, "robot", "robot"), (pb, "pam", "pam"),
                            (ac, "pam", "pam"), (mfs, "mom", "mom"), (sfs, "sofia", "sofia")) + tuple(
                            (importlib.import_module(m), "robot", "robot") for m in ("robot_mf", "waiter_kit") if _has(m)):
        if hasattr(mod, attr) and not getattr(getattr(mod, attr), "_uz", False):
            setattr(mod, attr, who_wrap(name, getattr(mod, attr)))

    s0 = an.speech

    def speech(c, k, text, head, *a, **kw):
        R.speech = dict(text=[], fills=[], head=_dev(c, head[0], head[1]) + (head[2] * _scale(c),) if head else None, said=text)
        try:
            return s0(c, k, text, head, *a, **kw)
        finally:
            if R.frames:
                R.frames[-1]["bubbles"].append(R.speech)
            R.speech = None
    an.speech = speech

    if hasattr(film, "plain_bubble"):
        p0 = film.plain_bubble

        def plain_bubble(c, text, x, y, tip, *a, **kw):
            R.speech = dict(text=[], fills=[], head=None, said=text, tip=_dev(c, *tip))
            try:
                return p0(c, text, x, y, tip, *a, **kw)
            finally:
                if R.frames:
                    R.frames[-1]["bubbles"].append(R.speech)
                R.speech = None
        film.plain_bubble = plain_bubble

    m0 = film.move

    def move(*a, **kw):
        R.cam = m0(*a, **kw)
        R.shot = a[0] if a else None
        return R.cam
    film.move = move

    wrappers = {}                                     # frame id -> drawing, for <locals> wrapper frames

    def prof(frame, event, arg):                      # which functions draw each shot: what draw() calls, and what the
        if event != "call":                           # wrappers it calls (sb._with_state, the film's own) call in turn
            return
        b = frame.f_back
        if b is None:
            return
        d = None
        if b.f_code.co_name == "draw" and b.f_code.co_filename == film.__file__:
            d = b.f_locals.get("drawing")
        elif id(b) in wrappers:
            d = wrappers[id(b)]
        if d is None:
            return
        R.map.setdefault(d, set()).add("%s.%s" % (frame.f_globals.get("__name__"), frame.f_code.co_qualname))
        if "<locals>" in frame.f_code.co_qualname:
            wrappers[id(frame)] = d
    sys.setprofile(prof)


def _scale(c):
    a = c.user_to_device_distance(1.0, 0.0)
    return math.hypot(*a)


# ---------------------------------------------------------------------------------------------------- the checks
def _cam(f, x, y):
    fx, fy, z = f["cam"]
    return ((x - fx) * z + 270, (y - fy) * z + 480)


def _cam_box(f, b):
    x0, y0 = _cam(f, b[0], b[1]); x1, y1 = _cam(f, b[2], b[3])
    return (min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1))


def faces(f):
    """the faces in frame units: name -> (x, y, r)."""
    if not f.get("cam"):
        return {}
    z = f["cam"][2]
    return {k: _cam(f, v[0], v[1]) + (v[2] * z,) for k, v in f["heads"].items()}


def _inter(a, b):
    return (max(a[0], b[0]), max(a[1], b[1]), min(a[2], b[2]), min(a[3], b[3]))


def check_signs(f):
    """every text on the set: whole in the frame or out of it (what a clip hides doesn't count)."""
    out = []
    for t in f["scene"].get("text", []):
        v = _inter(t["bbox"], t["clip"])
        if v[2] - v[0] < 1 or v[3] - v[1] < 1:
            continue
        b = _cam_box(f, v)
        if b[2] <= 0 or b[0] >= W or b[3] <= 0 or b[1] >= H:
            continue
        if b[0] < -EDGE or b[2] > W + EDGE or b[1] < -EDGE or b[3] > H + EDGE:
            out.append("SIGN cut by the frame: %r at %s" % (t["text"], tuple(round(q) for q in b)))
    return out


def check_tails(f):
    """a tail ends beside the mouth drawn in that frame: between y+0.15r and y+1.5r of the face point, |dx| <= 1.7r."""
    out = []
    fc = faces(f)
    for b in f["bubbles"]:
        tip = b.get("tip")
        if tip is None:
            tb = [t["bbox"] for t in b["text"]]
            pts = [p for fill in b["fills"] for p in fill]
            if not tb or not pts:
                continue
            box = (min(q[0] for q in tb) - 24, min(q[1] for q in tb) - 18, max(q[2] for q in tb) + 24, max(q[3] for q in tb) + 18)
            dist = lambda p: max(box[0] - p[0], 0, p[0] - box[2]) + max(box[1] - p[1], 0, p[1] - box[3])
            tip = max(pts, key=dist)
            if dist(tip) < 6:
                continue                              # no tail drawn
        ref = b["head"] or tip
        if not fc:
            continue
        who = min(fc, key=lambda n: math.hypot(fc[n][0] - ref[0], fc[n][1] - ref[1]))
        x, y, r = fc[who]
        if not (-r < x < W + r and -r < y < H + r):
            out.append("TAIL to %s, who is off screen: %r" % (who, b["said"]))
            continue
        dy, dx = (tip[1] - y) / r, abs(tip[0] - x) / r
        if not (MOUTH[0] <= dy <= MOUTH[1] and dx <= MOUTH[2]):
            where = "above the mouth (hair, curl, crown)" if dy < MOUTH[0] else ("below the mouth" if dy > MOUTH[1] else "too far to the side")
            out.append("TAIL %s of %s: %r tip %s, face %s" % (where, who, b["said"], tuple(round(q) for q in tip),
                                                              (round(x), round(y), round(r))))
    return out


def check_limbs(f):
    """at most two visible arms per character, rig and declared together."""
    n = {}
    for a in f["scene"].get("arms", []):
        if a["vis"]:
            n[a["owner"]] = n.get(a["owner"], 0) + 1
    return ["LIMBS: %s has %d arms" % (o, k) for o, k in n.items() if k > 2]


def check_strays(f, reach=2.2):
    """loose groups of short straight strokes (dashes, speed lines: two or more, 6-110 px, within 120 px of each other)
    and declared marks, with no character within reach (in head radii, from the head down to the feet)."""
    out = []
    hs = f["heads"]
    near = lambda p: any(abs(p[0] - x) <= reach * r and y - 2.5 * r <= p[1] <= y + 9 * r for x, y, r in hs.values())
    segs = [(a, b) for s_ in f["scene"].get("strokes", []) for a, b in s_["segs"] if 6 <= math.hypot(b[0] - a[0], b[1] - a[1]) <= 110]
    mids = [((a[0] + b[0]) / 2, (a[1] + b[1]) / 2) for a, b in segs]
    seen = set()
    for i, m in enumerate(mids):
        if i in seen:
            continue
        grp = [j for j, q in enumerate(mids) if math.hypot(q[0] - m[0], q[1] - m[1]) <= 120]
        if len(grp) < 2:
            continue
        seen.update(grp)
        cx = sum(mids[j][0] for j in grp) / len(grp); cy = sum(mids[j][1] for j in grp) / len(grp)
        c = _cam(f, cx, cy)
        if 0 <= c[0] <= W and 0 <= c[1] <= H and not near((cx, cy)):
            out.append("STRAY marks (%d strokes) with no one near them at %s" % (len(grp), tuple(round(q) for q in c)))
    for m in f["scene"].get("marks", []):
        c = _cam(f, *m["at"])
        if 0 <= c[0] <= W and 0 <= c[1] <= H and (m["owner"] is None or not near(m["at"])):
            out.append("STRAY declared mark at %s" % (tuple(round(q) for q in c),))
    return out


def check_text(f):
    """bubbles and cards inside the safe area."""
    out = []
    for b in f["bubbles"]:
        for t in b["text"]:
            x0, y0, x1, y1 = t["bbox"]
            if x0 < SAFE[0] or y0 < SAFE[1] or x1 > SAFE[2] or y1 > SAFE[3]:
                out.append("TEXT outside the safe area: %r at %s" % (t["text"], tuple(round(q) for q in t["bbox"])))
    return out


def check_scale(f, story=None):
    """the faces that tell the story: not in the bottom quarter, not under the right-hand buttons."""
    out = []
    for n, (x, y, r) in faces(f).items():
        if story and n not in story:
            continue
        if not (0 <= x <= W and 0 <= y <= H):
            continue
        if y > BOTTOM:
            out.append("SCALE: %s's face in the bottom quarter (y %d)" % (n, y))
        elif x > RAIL[0] and RAIL[1] <= y <= RAIL[2]:
            out.append("SCALE: %s's face under the right-hand buttons (%d, %d)" % (n, x, y))
    return out


CHECKS = dict(signs=check_signs, tails=check_tails, limbs=check_limbs, strays=check_strays, text=check_text, scale=check_scale)


HOLD = 9                           # a sign cut for fewer frames than this (0.3 s at 30 fps) is crossing the edge in a move


def run(frames=None, only=None, allow=()):
    """all frame checks; returns [(frame index, shot, check, message)], minus the known artefacts allowed by name.
    A sign counts as cut, and a bubble as outside the safe area, only when it stays so for HOLD frames in a row: one
    sliding through the edge during a camera move is not one left there."""
    bad = []
    frames = frames if frames is not None else R.frames
    runs = {}
    for i, f in enumerate(frames):
        if not f.get("cam"):
            continue
        for name, fn in CHECKS.items():
            if only and name not in only:
                continue
            for msg in fn(f):
                if any(a in msg for a in allow):
                    continue
                if name in ("signs", "text"):
                    key = (f["shot"], name, msg.split(" at ")[0])
                    r = runs.get(key)
                    if r and r[1] == i - 1:
                        r[1] = i; r[2].append((i, msg))
                    else:
                        runs[key] = r = [i, i, [(i, msg)]]
                        runs.setdefault("_all", []).append(r)
                    continue
                bad.append((i, f["shot"], name, msg))
    for r in runs.get("_all", []):
        if len(r[2]) >= HOLD:
            i, msg = r[2][len(r[2]) // 2]
            bad.append((i, frames[i]["shot"], "text" if msg.startswith("TEXT") else "signs", "%s (for %d frames)" % (msg, len(r[2]))))
    return bad


def check_map(expect, got=None):
    """the drawing map: every shot changed in this version is drawn by (calls) the function it names."""
    got = R.map if got is None else got
    out = []
    for d, fn in expect.items():
        called = got.get(d, set())
        if not any(q.split(".")[-1] == fn or q.endswith("." + fn) for q in called):
            out.append("MAP: %s does not call %s; it calls %s" % (d, fn, ", ".join(sorted(q for q in called if "<locals>" not in q))[:160]))
    return out


# ---------------------------------------------------------------------------------------------------- the encoded film
def check_film(mp4, frames=None, loop_max=3.0, lufs=(-16.0, -14.0), peak=-1.0):
    """format, loudness, true peak, and the loop seam, on the file that ships."""
    import json
    import subprocess
    out = []
    p = json.loads(subprocess.check_output(["ffprobe", "-v", "0", "-select_streams", "v", "-count_frames", "-show_entries",
                                            "stream=width,height,r_frame_rate,nb_read_frames,color_space,color_primaries,color_transfer",
                                            "-of", "json", mp4]))["streams"][0]
    if (p["width"], p["height"], p["r_frame_rate"]) != (1080, 1920, "30/1"):
        out.append("FORMAT: %sx%s at %s" % (p["width"], p["height"], p["r_frame_rate"]))
    if frames and int(p["nb_read_frames"]) != frames:
        out.append("FORMAT: %s frames, expected %d" % (p["nb_read_frames"], frames))
    for k in ("color_space", "color_primaries", "color_transfer"):
        if p.get(k) not in ("bt709",):
            out.append("FORMAT: %s is %s, not bt709" % (k, p.get(k)))
    log = subprocess.run(["ffmpeg", "-nostats", "-i", mp4, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True,
                         text=True).stderr.split("Summary:")[-1]
    I = float(log.split("I:")[1].split("LUFS")[0]); P = float(log.split("Peak:")[1].split("dBFS")[0])
    if not lufs[0] <= I <= lufs[1]:
        out.append("SOUND: %.1f LUFS (wants %.0f to %.0f)" % (I, lufs[0], lufs[1]))
    if P > peak:
        out.append("SOUND: true peak %.1f dBTP (wants <= %.0f)" % (P, peak))
    n = int(p["nb_read_frames"])
    raw = subprocess.check_output(["ffmpeg", "-v", "0", "-i", mp4, "-vf", "select='eq(n,0)+eq(n,%d)',scale=270:480" % (n - 1),
                                   "-vsync", "0", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"])
    import numpy as np
    a = np.frombuffer(raw, np.uint8).astype(float).reshape(-1, 480, 270, 3)
    if len(a) == 2:
        d = float(np.abs(a[0] - a[1]).mean())
        if d > loop_max:
            out.append("LOOP: the last frame differs from frame 0 by %.1f/255 on average (wants <= %.1f)" % (d, loop_max))
    return out, dict(lufs=I, peak=P, frames=n)
