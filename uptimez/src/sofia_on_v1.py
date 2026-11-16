"""SOFIA, "Office Noir", v1: the femme fatale under the desk lamp, and the false suspect. Built on sofia_ss
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
ACCENTS = [(HEART, 1.0), (HOOP_GOLD, 0.5), (HOOP_SHINE, 0.5)]

POSES = {"file": (-24, 112, 34, -104), "bored": (-10, 30, 14, -34)}


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


def sofia_noir(k, x, feet, s=1.0, pose="file", face_kind="bored", look=(0.2, 0.9), lag=(0, 0), mouth=None, lean=0.0,
               seed=7, nails=True):
    saved = [(m, n, getattr(m, n)) for m, n in _SWAP if hasattr(m, n)]
    new = {"RED": HEART, "BLOUSE": BLOUSE_DARK, "BLOUSE_SHADE": BLOUSE_DARK_SHADE, "GOLD": BELT_BLACK,
           "GOLD_LIGHT": BELT_BLACK, "teardrop": hoop}
    old_poses = dict(ss.POSES)
    ss.POSES.update(POSES)
    fk, lk = face_kind, look
    if face_kind == "bored":
        fk, lk = "neutral", (0.2, 0.9)
    elif face_kind == "side":
        fk, lk = "neutral", (-1.0, 0.1)
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
                       mouth=mouth)
    finally:
        sv._arm = orig_arm
        for m, n, v in saved:
            setattr(m, n, v)
        ss.POSES.clear(); ss.POSES.update(old_poses)
    c = k.c
    hx, hy = out["head"]
    if face_kind in ("bored", "side"):                 # heavy lids: the top half of each eye under a lid
        for sx in (-1, 1):
            ex, ey = hx + sx * 18 * s, hy + 4 * s
            c.save(); c.new_path(); c.arc(ex, ey, 11 * s, 0, 2 * math.pi); c.clip()
            c.set_source_rgb(*sv.SKIN); c.rectangle(ex - 12 * s, ey - 13 * s, 24 * s, 12 * s); c.fill(); c.restore()
            c.set_source_rgb(*INK); c.set_line_width(3 * s)
            c.new_path(); c.move_to(ex - 11 * s, ey - 1 * s); c.line_to(ex + 11 * s, ey - 1 * s); c.stroke()
    if pose == "file" and nails:
        (lx, ly), (rx, ry) = out["hands"]
        nail_file(k, rx - 2 * s, ry - 4 * s, ang=-1.1, s=s)
        ellipse(k, rx, ry, 9 * s, 9 * s, sv.SKIN, seed + 90, shadow=False, lw=2 * s)
    return out
