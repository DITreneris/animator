"""SOFIA, "Office Noir", v2 (sofia_on_v1.py = v1, kept). v2 after the review: no lip gloss in noir (same key red as
the heart, nothing brighter); hoops at 35 %; the nail file tilted at about 40 degrees between separated hands,
its textured end showing, with stroke=0..1 moving it along its axis; her own mouths at full size (Secret Santa
had them 20 % smaller); faces "side" (pupils in the corners, one brow up: her "unimpressed" brows), "brow" (one
brow up without looking up) and "smirk" (the smallest smirk on "darling", still looking down); hair softened:
a 1940s wave over her screen-right eye and two loose curved strands.
v1 notes: the femme fatale under the desk lamp, and the false suspect. Built on sofia_ss
(untouched; its colours are swapped only while she is drawn, then restored):
- her lips are the episode's key red (HEART, #D21F2B): the lipstick clue, the same red as the heart, so both stay
  full red in the noir pass;
- gold hoops instead of the Secret Santa crystal drops; HOOP_GOLD and HOOP_SHINE are accent keys at 50 %;
- dark burgundy nails (not the key red: only her lips match the heart);
- a dark blouse; the thin gold belt becomes black (gold is kept for the hoops only); no badge;
- pose "file": filing her nails at chest height, the nail file in her screen-right hand;
- faces she uses: "bored" (lids half down, eyes on her nails), "knowing" (I sign my work, darling), "closed"
  (the purr), "side" (a side-eye at Don, no head turn).
Usage: o = sofia_noir(k, x, feet, s, pose, face_kind, look, lag, mouth, lean, seed)"""
import math
import kit
import sofia_ss as ss
import sofia_v4 as sv
import sofia_tg as stg
import sofia_mf as sm
from kit import INK, ellipse

HEART = (0xD2 / 255, 0x1F / 255, 0x2B / 255)
HOOP_GOLD = (0.86, 0.68, 0.24)
HOOP_SHINE = (1.0, 0.88, 0.50)
HOOP_EDGE = (0.45, 0.30, 0.05)
BLOUSE_DARK = (0.13, 0.13, 0.15)
BLOUSE_DARK_SHADE = (0.05, 0.05, 0.06)
BELT_BLACK = (0.06, 0.06, 0.07)
FILE_COL = (0.70, 0.66, 0.72)
NAIL = (0.36, 0.10, 0.14)            # dark burgundy, not the key red: only her lips match the heart
ACCENTS = [(HEART, 1.0), (HOOP_GOLD, 0.35), (HOOP_SHINE, 0.35)]

POSES = {"file": (-34, 128, 26, -70), "bored": (-10, 30, 14, -34)}


def hoop(k, x, y, lgx=0.0, spark=0.0, seed=0):
    """Replaces sofia_ss.teardrop while she is drawn: a big gold hoop hanging from the lobe at (x, y)."""
    c = k.c
    r = sm.HOOP_R
    hx0, hy0 = x + lgx * 0.4, y + 2 + r
    c.set_source_rgb(*INK); c.set_line_width(9); c.new_path(); c.arc(hx0, hy0, r, 0, 2 * math.pi); c.stroke()
    c.set_source_rgb(*HOOP_GOLD); c.set_line_width(6); c.new_path(); c.arc(hx0, hy0, r, 0, 2 * math.pi); c.stroke()
    c.set_source_rgb(*HOOP_EDGE); c.set_line_width(1.6); c.new_path(); c.arc(hx0, hy0, r - 2.8, 0, 2 * math.pi); c.stroke()
    c.set_source_rgb(*HOOP_SHINE); c.set_line_width(2.4); c.new_path(); c.arc(hx0, hy0, r, 1.15 * math.pi, 1.55 * math.pi)
    c.stroke()


def nail_file(k, x, y, ang=-0.7, s=1.0):
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    c.new_path(); c.move_to(-2, 0); c.line_to(2, 0); c.line_to(3, -34); c.line_to(0, -38); c.line_to(-3, -34); c.close_path()
    c.set_source_rgb(*FILE_COL); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.4); c.stroke()
    c.set_source_rgba(0, 0, 0, 0.35); c.set_line_width(0.6)
    for i in range(6):
        c.move_to(-2, -8 - i * 4); c.line_to(2, -10 - i * 4); c.stroke()
    c.restore()


_SWAP = [(sv, "RED"), (stg, "RED"), (sm, "RED"), (ss, "RED"), (ss, "BLOUSE"), (ss, "BLOUSE_SHADE"), (ss, "GOLD"),
         (ss, "GOLD_LIGHT"), (ss, "teardrop")]


def wave(k, hx, hy, s, seed=0):
    """The 1940s wave over her screen-right eye, and two loose strands on the other side."""
    c = k.c
    c.save(); c.translate(hx, hy + 6 * s); c.scale(s, s)
    kit.cut(k, [(-6, -52), (22, -50), (46, -34), (50, -6), (42, 10), (30, 6), (26, -12), (12, -28), (-4, -36)],
            ss.HAIR, shadow=False, lw=2)
    c.set_source_rgb(*INK); c.set_line_width(1.6)
    c.new_path(); c.move_to(4, -44); c.curve_to(26, -40, 40, -26, 40, -4); c.stroke()
    c.set_source_rgb(*ss.HAIR_SHINE); c.set_line_width(3); c.set_line_cap(1)
    c.new_path(); c.move_to(12, -42); c.curve_to(28, -38, 36, -28, 38, -16); c.stroke()
    c.set_source_rgb(*INK); c.set_line_width(2)
    for (x0, y0, x1, y1, x2, y2) in ((-34, -40, -46, -10, -40, 20), (-26, -42, -36, -16, -30, 12)):
        c.new_path(); c.move_to(x0, y0); c.curve_to(x1, y1, x2, y2 - 10, x2 + 4, y2); c.stroke()
    c.set_line_cap(0)
    c.restore()


def sofia_noir(k, x, feet, s=1.0, pose="file", face_kind="bored", look=(0.2, 0.9), lag=(0, 0), mouth=None, lean=0.0,
               seed=7, nails=True, stroke=0.0, hair=True):
    saved = [(m, n, getattr(m, n)) for m, n in _SWAP if hasattr(m, n)]
    new = {"RED": HEART, "BLOUSE": BLOUSE_DARK, "BLOUSE_SHADE": BLOUSE_DARK_SHADE, "GOLD": BELT_BLACK,
           "GOLD_LIGHT": BELT_BLACK, "teardrop": hoop}
    old_poses = dict(ss.POSES)
    ss.POSES.update(POSES)
    fk, lk = face_kind, look
    if face_kind == "bored":
        fk, lk = "neutral", (0.2, 0.9)
    elif face_kind == "side":
        fk, lk = "unimpressed", (-1.0, 0.05)
    elif face_kind == "brow":
        fk, lk = "unimpressed", (0.2, 0.9)
    elif face_kind == "smirk":
        fk, lk = "knowing", (0.2, 0.9)
    orig_arm = sv._arm

    def arm_dark_nails(*a, **kw):
        sv.RED = NAIL
        try:
            return orig_arm(*a, **kw)
        finally:
            sv.RED = HEART
    sv._arm = arm_dark_nails
    try:
        for m, n, _ in saved:
            setattr(m, n, new[n])
        out = ss.sofia(k, x, feet, s, pose=pose, face_kind=fk, look=lk, lag=lag, seed=seed, badge=False, lean=lean,
                       mouth=None)
    finally:
        sv._arm = orig_arm
        for m, n, v in saved:
            setattr(m, n, v)
        ss.POSES.clear(); ss.POSES.update(old_poses)
    c = k.c
    hx, hy = out["head"]
    my = hy + 33 * s
    if mouth:                                          # full-size speech mouths (Secret Santa scaled them to 0.8)
        import iwry_mouths as im
        ellipse(k, hx + 1 * s, hy + 32 * s, 21 * s, 12 * s, sv.SKIN, seed + 66, shadow=False, outline=False)
        c.save(); c.translate(hx, my); c.scale(1.1 * s, 1.1 * s)
        im.mouth(k, 0, 0, mouth, sv.SKIN, lip_col=HEART, inner=(0.30, 0.05, 0.07), erase=(1, 1), seed=seed + 67)
        c.restore()
    elif fk not in ("horrified", "curious", "surprised"):     # no gloss in noir: paint the gloss line out
        c.set_source_rgb(*HEART); c.set_line_width(2.4 * s); c.set_line_cap(1)
        c.new_path(); c.move_to(hx - 4 * s, hy + 35 * s); c.line_to(hx + 2 * s, hy + 35 * s); c.stroke(); c.set_line_cap(0)
    if face_kind in ("bored",):                        # heavy lids: the top half of each eye under a lid
        for sx in (-1, 1):
            ex, ey = hx + sx * 18 * s, hy + 4 * s
            c.save(); c.new_path(); c.arc(ex, ey, 11 * s, 0, 2 * math.pi); c.clip()
            c.set_source_rgb(*sv.SKIN); c.rectangle(ex - 12 * s, ey - 13 * s, 24 * s, 12 * s); c.fill(); c.restore()
            c.set_source_rgb(*INK); c.set_line_width(3 * s)
            c.new_path(); c.move_to(ex - 11 * s, ey - 1 * s); c.line_to(ex + 11 * s, ey - 1 * s); c.stroke()
    if hair:
        wave(k, hx, hy, s, seed)
    if pose == "file" and nails:
        (lx, ly), (rx, ry) = out["hands"]
        for i in range(4):                              # her left fingers spread up, nails toward the file
            a = -2.0 + i * 0.28
            fx, fy = lx + math.cos(a) * 12 * s, ly + math.sin(a) * 12 * s
            ellipse(k, fx, fy, 3.4 * s, 5 * s, sv.SKIN, seed + 95 + i, shadow=False, lw=1.4 * s)
            ellipse(k, fx + math.cos(a) * 3 * s, fy + math.sin(a) * 3 * s, 2 * s, 2.4 * s, NAIL, seed + 99 + i,
                    shadow=False, outline=False)
        ang = -0.70                                       # about 40 degrees, pointing up-left at her fingers
        dx = math.sin(ang) * (stroke - 0.5) * 12 * s
        dy = -math.cos(ang) * (stroke - 0.5) * 12 * s
        nail_file(k, rx - 2 * s + dx, ry - 4 * s + dy, ang=ang, s=1.25 * s)
        ellipse(k, rx, ry, 9 * s, 9 * s, sv.SKIN, seed + 90, shadow=False, lw=2 * s)
    return out
