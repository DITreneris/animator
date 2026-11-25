"""ONE STAR v15 speech bubbles (25 Nov, Tomas /grill-me): the repo's bubble (speech.py's box, tail and type, The
Offer's settings) on the ten lines spoken in frame; the four lines a screen carries (the post, "Stupid human.", the
call, Pam's reply) get none. Rules and the per-line plan: customer-success/one-star-bubbles-lessons-v1.md.
- the speaker is found, not guessed: every rig drawn is logged with its head in frame space (540 x 960);
- each line is placed by its own rule (PLAN): beside the face at mouth height (L / R), or over Don's bare crown or the
  robot's antenna (T), or, for the robot's first line, beside its visor (V: Don's hand is on the antenna then);
- the tail is 15 px past the box (speech.GAP), its tip on the cheek's outline, the crown, the antenna or the visor rim;
- one bubble per line and picture, LOCKED: drawn once at the drawing 60 % into the line, and that layer (the frame with
  minus without) laid over every drawing of the line (lesson 1017; The Offer's lock_bubble), so a breath, a lunge or a
  camera ease does not move it;
- speech_gate.check runs on the drawing it was placed on; FAULTS lists what failed.
install() is opt-in."""
import json
import math
import cairo
import numpy as np
import speech
import speech_gate as gate
import kit
import cs_scene1 as s1
import fs_storyboard as sb

REG = []
K = {"don": 50.0, "robot": 52.0, "client": 54.0, "pam": 44.0, "sofia": 44.0, "mom": 44.0}   # head radius, rig units
ON = [False]
LOCK = {}                                  # (key, shot) -> (patch surface, box, tip)
FAULTS = []
PLACED = []                                # (key, shot, d, box, tip)

# form: L / R (beside the face), T (crown or antenna), V (beside the robot's visor). dx, dy move the box; w its widest row
PLAN = {
    "1.4r": dict(form="V", w=140, size=24),
    "1.4d": dict(form="T", w=220, dx=-40),
    "2.1": dict(form="L", w=150),
    "3.1r": dict(form="T", w=200, dx=-62),
    "3.1d": dict(form="T", w=220, dx=-30),
    "3.3": dict(form="T", w=220),
    "3.5": dict(form="L", w=120, dx=-4),
    "4.2p": dict(form="L", w=120),
    "4.4": dict(form="T", w=160, size=22, left=1, dy=-4),
    "5.1": dict(form="L", w=160),
    "5.4d": dict(form="T", w=260, dx=20, dy=-4),
    "6.5": dict(form="L", w=150),
}
WHO = {"DON": "don", "ROBOT": "robot", "CLIENT": "client", "PAM": "pam", "SOFIA": "sofia"}
PROTECT = {}                               # key -> [(x0, y0, x1, y1)] the line's frame keeps clear (540 space)


def _log(name, mod, fn):
    f = getattr(mod, fn)
    if getattr(f, "_say", False):
        return

    def g(k, x, feet, s=1.0, *a, **kw):
        o = f(k, x, feet, s, *a, **kw)
        try:
            c = k.c
            hi = c.get_target().get_width() / 540.0
            if abs(c.get_target().get_device_scale()[0] - hi) > 1e-6:
                return o                                                           # a scratch surface, not the frame
            hx, hy = c.user_to_device(*o["head"])
            m = c.get_matrix()
            sc = math.sqrt(abs(m.xx * m.yy - m.xy * m.yx)) / hi
            scr = None
            if name == "robot" and "screen" in o:
                scr = tuple(v / hi for v in c.user_to_device(*o["screen"]))
            rec = dict(who=name, x=hx / hi, y=hy / hi, r=K[name] * s * sc, screen=scr)
            if rec["y"] + rec["r"] > 0 and not any(q["who"] == name and abs(q["x"] - rec["x"]) < 40 and abs(q["y"] - rec["y"]) < 40
                                                   for q in REG):
                REG.append(rec)
        except Exception:
            pass
        return o
    g._say = True
    g._orig = f
    setattr(mod, fn, g)


def lines():
    import importlib
    out = {}
    for i in range(1, 7):
        m = importlib.import_module("cs_scene%d" % i)
        meta = json.load(open(m.TAKES + "/takes.json"))
        starts, n = [], 0
        for sh, nd, _ in m.SHOTS:
            starts.append((sh, n, nd)); n += nd
        for key, t in m.schedule():
            if key not in PLAN:
                continue
            ln = meta[key]["len"]
            d0 = int(round(t * 12)); d1 = int(math.ceil((t + ln) * 12))           # on with the first syllable, off a drawing after
            for sh, a, nd in starts:
                if a <= d0 < a + nd:
                    out[key] = (sh, d0 - a, min(nd - 1, d1 - a), meta[key]["text"], WHO[meta[key]["who"]])
    return out


LINES = {}


def _active(shot, d):
    for key, (sh, d0, d1, text, who) in LINES.items():
        if sh == shot and d0 <= d <= d1:
            return key, text, who, d0, d1
    return None


def _place(k, key, text, who):
    spk = [r for r in REG if r["who"] == who]
    if not spk:
        return None
    sp = max(spk, key=lambda r: r["r"])
    big = {}
    for r_ in REG:                                                                  # one head per rig: at 1080 a second, half-size
        if r_["who"] not in big or r_["r"] > big[r_["who"]]["r"]:                    # copy is logged (a scratch draw); keep the frame's
            big[r_["who"]] = r_
    faces = [(r_["x"], r_["y"], r_["r"]) for r_ in big.values() if r_["r"] > 6]
    p = PLAN[key]
    mono = who == "robot"
    if mono:
        text = text.upper()
    keep = speech.MONO_SIZE[0], speech.SIZE[0]
    if "size" in p:
        speech.MONO_SIZE[0] = speech.SIZE[0] = p["size"]
    try:
        rows, size, font, bw, bh = speech._metrics(k, text, mono, p["w"])
    finally:
        speech.MONO_SIZE[0], speech.SIZE[0] = keep
    hx, hy, r = sp["x"], sp["y"], sp["r"]
    G = speech.GAP
    above = None
    f = p["form"]
    if f == "T":
        if mono:
            sx, sy = sp["screen"]
            tip = (sx, sy - 1.42 * r * 50.0 / K["robot"] - 4)
        else:
            tip = (hx, hy - 0.98 * r)
        above = tip
        x0 = tip[0] - bw / 2.0 + p.get("dx", 0)
        if "left" in p:                                                            # the box's left edge from the tip (a sign beside it)
            x0 = tip[0] + p["left"]
        y1 = tip[1] - G + p.get("dy", 0)
        box = (x0, y1 - bh, x0 + bw, y1)
    elif f == "V":
        sx, sy = sp["screen"]
        tip = (sx - 0.80 * r * 50.0 / K["robot"], sy)
        x1 = tip[0] - G
        y0 = tip[1] - bh * 0.5 + p.get("dy", 0)
        box = (x1 - bw, y0, x1, y0 + bh)
    else:
        my = hy + 0.35 * r
        side = -1 if f == "L" else 1
        tip = (hx + side * 0.84 * r, my)
        y0 = my - bh * 0.5 + p.get("dy", 0)
        if side < 0:
            box = (tip[0] - G - bw + p.get("dx", 0), y0, tip[0] - G + p.get("dx", 0), y0 + bh)
            tip = (tip[0] + min(0, p.get("dx", 0)) * 0, tip[1])
        else:
            box = (tip[0] + G, y0, tip[0] + G + bw, y0 + bh)
    return box, tip, rows, size, font, faces, above, mono


def _bubble_layer(surf_with, surf_without):
    from scipy import ndimage
    w, h = surf_with.get_width(), surf_with.get_height()
    surf_with.flush(); surf_without.flush()
    A = np.ndarray((h, surf_with.get_stride() // 4, 4), np.uint8, surf_with.get_data())[:, :w].copy()
    B = np.ndarray((h, surf_without.get_stride() // 4, 4), np.uint8, surf_without.get_data())[:, :w]
    m = ndimage.binary_fill_holes(np.abs(A.astype(int) - B.astype(int))[..., :3].max(axis=2) > 0)
    patch = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    dst = np.ndarray((h, patch.get_stride() // 4, 4), np.uint8, patch.get_data())
    dst[:, :w][m] = A[m]
    dst[:, :w][m, 3] = 255
    patch.mark_dirty()
    return patch


def _copy(base):
    w, h = base.get_width(), base.get_height()
    out = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    base.flush()                                                                   # the bytes, not a paint: a device-scaled
    src = np.ndarray((h, base.get_stride()), np.uint8, base.get_data())             # source paints at half size
    np.ndarray((h, out.get_stride()), np.uint8, out.get_data())[:] = src[:, :out.get_stride()]
    out.mark_dirty()
    hi = w / 540.0
    if hi != 1:
        out.set_device_scale(hi, hi)
    return out


def _lock(od, fn, shot, key, text, who, d0, d1):
    dref = int(round(d0 + 0.6 * (d1 - d0)))
    REG.clear()
    base = od(fn, dref)
    with_ = _copy(base)
    c = cairo.Context(with_)
    k = kit.Ctx(c, 0)
    pl = _place(k, key, text, who)
    if pl is None:
        FAULTS.append((shot, dref, key, ["no %s in the frame" % who])); LOCK[(key, shot)] = None
        return
    box, tip, rows, size, font, faces, above, mono = pl
    before = gate.snapshot(with_)
    speech._paint(k, box, tip, rows, size, font, mono)
    with_.flush()
    try:
        fl = gate.check(with_, box, tip, faces, above=above, aim=tip if (mono or above) else None, before=before,
                        avoid=PROTECT.get(key, []), fill=speech.TINT if mono else None)
    except Exception as e:
        fl = ["check failed: %r" % e]
    if fl:
        FAULTS.append((shot, dref, key, fl))
    PLACED.append((key, shot, dref, tuple(round(v) for v in box), tuple(round(v) for v in tip)))
    LOCK[(key, shot)] = (_bubble_layer(with_, base), box, tip)


def install():
    if ON[0]:
        return
    ON[0] = True
    import client_ob, pam_bc, sofia_cs, mom_fs, robot_mf
    speech.SIZE[0], speech.MONO_SIZE[0], speech.MAX_W[0] = 30, 26, 300               # The Offer's (lesson 954); mono 26 to fit
    speech.MONO_BOLD[0] = True
    speech.ROBOT[0] = True                                                           # the robot's own tinted bubble
    # frame for the bubble (lesson 358), not the bubble for the frame:
    d14 = 90.0 / s1.TWO14_IN[2]                                                      # 1.4: the robot 90 px right: wall on its left
    s1.TWO14 = (s1.TWO14[0] - d14,) + s1.TWO14[1:]
    s1.TWO14_IN = (s1.TWO14_IN[0] - d14,) + s1.TWO14_IN[1:]
    import cs_v14
    cs_v14.ARM14[0] = "none"
    import cs_scene2 as s2, cs_scene4 as s4
    s2.PAN21 = (0, 3)                                                                # 2.1: the pan lands before the line
    s4.CAM42b = (221, 690, 2.2)                                                      # 4.2b: Pam off the left edge: wall beside her
    s4.CAM44 = (s4.CAM44[0] + 60.0 / s4.CAM44[2],) + s4.CAM44[1:]                    # 4.4: both 60 px left: wall right of the sign
    _log("don", sb, "don")
    _log("client", client_ob, "client")
    _log("pam", pam_bc, "pam")
    _log("sofia", sofia_cs, "sofia")
    _log("mom", mom_fs, "mom")
    _log("robot", robot_mf, "robot")
    LINES.update(lines())
    od, odi = s1.draw, s1._draw_in

    def _draw_in(fn, k, d):
        REG.clear()
        return odi(fn, k, d)

    def draw(fn, d):
        import cs_hands as ch
        if not ch._BYFN:
            ch.begin_fn(fn)
        shot = ch._BYFN.get(fn)
        a = _active(shot, d) if shot is not None else None
        if a is not None and (a[0], shot) not in LOCK:
            _lock(od, fn, shot, *a)
        surf = od(fn, d)
        if a is not None and LOCK.get((a[0], shot)):
            patch = LOCK[(a[0], shot)][0]
            c = cairo.Context(surf)
            hi = surf.get_width() / 540.0
            c.scale(1 / hi, 1 / hi)
            c.set_source_surface(patch, 0, 0); c.paint()
        return surf
    s1._draw_in = _draw_in
    s1.draw = draw
