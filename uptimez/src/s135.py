"""Saved to Cloud S1v3.5 - S1v3.4 with a picture payoff: PAM's private page holds her ballpoint doodle of
DON with horns, tail and pitchfork ("BOSS", "MAKE IT BOLD!"), instead of "CAN MY BOSS SEE THIS?".
DON holds it up beside his own face, under his gilded portrait. The doodle also shows on the page that
slaps the lens in the cold open. New module only: patches s131/s132/s133/s134 at runtime.
Render with engine_v.py: s135 (sniff tag) or s135n (ends on DON). Audio = s134's mix."""
import math
import cairo
import kit
import s131
import s132
import s133
import s134  # noqa: F401  (emoji name tags, 1.0 s freezes)
import anim
import pt4
import pt42
from kit import INK, rect, text, ease, clamp, lerp

PEN = (0.13, 0.2, 0.55)          # ballpoint blue
RED = (0.86, 0.2, 0.18)
MARKER = "Permanent Marker"


def wob(k, pts, closed=False, lw=4.5, col=PEN, fill=None, j=2.0, seed=0):
    """A wobbly pen line through pts (local coords)."""
    c = k.c
    r = k.rng(7000 + seed)
    q = [(x + r.uniform(-j, j), y + r.uniform(-j, j)) for x, y in pts]
    c.move_to(*q[0])
    for x, y in q[1:]:
        c.line_to(x, y)
    if closed:
        c.close_path()
    if fill:
        c.set_source_rgb(*fill)
        c.fill_preserve()
    c.set_source_rgb(*col)
    c.set_line_width(lw)
    c.set_line_join(cairo.LINE_JOIN_ROUND)
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.stroke()


def circle_pts(cx, cy, rx, ry, n=28):
    return [(cx + rx * math.cos(2 * math.pi * i / n), cy + ry * math.sin(2 * math.pi * i / n)) for i in range(n)]


def doodle(k, cx, cy, s=1.0):
    """PAM's doodle of DON as a devil. Drawn around (cx, cy) at scale s, in page-local coords."""
    c = k.c
    c.save()
    c.translate(cx, cy)
    c.scale(s, s)
    # horns (behind the head)
    wob(k, [(-48, -40), (-70, -118), (-22, -62)], closed=True, fill=RED, seed=1)
    wob(k, [(48, -40), (70, -118), (22, -62)], closed=True, fill=RED, seed=2)
    # body: little suit triangle + red tie
    wob(k, [(-46, 58), (46, 58), (60, 150), (-60, 150)], closed=True, fill=(0.85, 0.85, 0.9), seed=3)
    wob(k, [(0, 60), (-12, 92), (0, 122), (12, 92)], closed=True, fill=RED, lw=3, seed=4)
    # tail: curly line from his back, arrow tip
    wob(k, [(55, 130), (100, 140), (128, 118), (120, 90), (100, 96)], lw=4, seed=5)
    wob(k, [(92, 84), (106, 90), (96, 104)], closed=True, fill=RED, lw=3, seed=6)
    # pitchfork in his hand
    wob(k, [(-60, 120), (-118, -10)], lw=4.5, seed=7)
    wob(k, [(-136, -6), (-130, -38), (-118, -10), (-112, -44), (-100, -16), (-96, -44)], lw=4, seed=8)
    # head: bald dome, shine, grey tufts
    wob(k, circle_pts(0, 0, 58, 62), closed=True, fill=(0.98, 0.86, 0.76), seed=9)
    wob(k, [(-24, -42), (-12, -50)], lw=3.5, seed=10)
    for sx in (-1, 1):
        wob(k, [(sx * 56, -12), (sx * 68, -6), (sx * 58, 2), (sx * 70, 8), (sx * 58, 16)], lw=3.5, seed=11 + sx)
    # face: angry brows, dot eyes, jagged frown
    wob(k, [(-36, -20), (-10, -10)], lw=5, seed=13)
    wob(k, [(36, -20), (10, -10)], lw=5, seed=14)
    for sx in (-20, 20):
        c.set_source_rgb(*PEN)
        c.arc(sx, -2, 5, 0, 2 * math.pi)
        c.fill()
    wob(k, [(-24, 34), (-14, 26), (-4, 34), (6, 26), (16, 34), (24, 28)], lw=4, seed=15)
    # angry lines
    for i, (x, y) in enumerate(((-86, -60), (86, -66), (-96, -30))):
        wob(k, [(x, y), (x + (8 if x > 0 else -8), y - 14)], lw=3.5, seed=20 + i)
    c.restore()


def scribble_text(k, s, x, y, size, col=PEN, rot=0.0):
    c = k.c
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    c.select_font_face(MARKER)
    c.set_font_size(size)
    e = c.text_extents(s)
    c.move_to(-e.width / 2 - e.x_bearing, e.height / 2)
    c.set_source_rgb(*col)
    c.show_text(s)
    c.restore()


def page(k, cx, cy, w, h, rot, variant="DOODLE"):
    c = k.c
    c.save()
    c.translate(cx, cy)
    c.rotate(rot)
    rect(k, -w / 2, -h / 2, w, h, kit.PAPER, 480)
    rect(k, -w / 2, -h / 2, w, 62, s131.PRIV, 481, shadow=False)
    text(k, "PAM / PRIVATE", 0, -h / 2 + 32, 26, (0.7, 0.08, 0.12))
    doodle(k, 10, 58, 0.95)
    # label with arrow, and the boss's catchphrase
    scribble_text(k, "BOSS", -160, -80, 34, rot=-0.12)
    wob(k, [(-150, -58), (-118, -30), (-82, -12)], lw=3.5, seed=30)
    wob(k, [(-96, -24), (-82, -12), (-98, -6)], lw=3.5, seed=31)
    c.restore()
    c.save()
    c.translate(cx, cy)
    c.rotate(rot)
    wob(k, [(78, -112), (222, -112), (222, -62), (130, -62), (104, -40), (110, -62), (78, -62)], closed=True,
        fill=(1, 1, 1), lw=3.5, seed=32)
    scribble_text(k, "MAKE IT BOLD!", 150, -88, 19, rot=-0.04)
    c.restore()


s132.page = page                 # shot 7 (DON's desk) now shows the doodle


def sh8_don(k, t, tl):
    """DON holds the doodle up beside his own face, under his gilded portrait."""
    s132.STATE["t"] = t
    c = k.c
    z = 1 + 0.06 * ease(clamp((s132.RAW_T - 17.0) / 3.5))
    c.save()
    anim.camera(c, 230, 560, z)
    pt4.accent_wall(k, "DON")
    pt42.portrait_frame(k, 330, 120, 140, 130)
    up = ease(clamp((t - 17.2) / 0.6))
    s132.STATE["brow"] = ease(clamp((t - 19.6) / 0.15))
    pose = anim.keyed(t, [(17.0, "stand"), (17.4, (-8, 0, 140, 40))], dur=0.4, overshoot=False)
    p = s132.who("DON", k, 170, 1230, 2.3, pose=pose, face="neutral", seed=63, look=(0.0, lerp(1, 0, up)))
    s132.STATE["brow"] = 0.0
    hx, hy = p["hands"][1]
    lift = ease(clamp((t - 17.0) / 0.4))
    c.save()
    c.translate(lerp(440, min(hx + 40, 405), lift), lerp(900, min(hy, 560), lift))
    c.scale(0.5, 0.5)
    page(k, 0, 0, 470, 400, 0.06)
    c.restore()
    c.restore()


s132.PANELS = [(a, b, sh8_don if fn.__name__ == "sh8_don" else fn) for (a, b, fn) in s132.PANELS]

_orig_private = s131.private_file


def private_file(k, x, y, w, seed, rot=0.0):
    if seed != 990:
        return _orig_private(k, x, y, w, seed, rot)
    c = k.c                      # the page slapping the lens in the cold open: the doodle page itself
    c.save()
    c.translate(x, y)
    c.scale(w / 330, w / 330)
    page(k, 0, 0, 470, 400, rot)
    c.restore()


s131.private_file = private_file

DURATION = s133.duration(21.5)
RAW_T = 0.0


def frame(k, t, tl):
    s133.RAW_T = RAW_T
    s133.frame(k, t, tl)


PANELS = [(0.0, DURATION, frame)]
shake = s133.shake
overlay = s133.overlay
