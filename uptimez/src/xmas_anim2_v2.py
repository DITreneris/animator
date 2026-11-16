"""ANIMATION v2 of the Christmas special "Happy Compliance": the approved v1 (xmas_anim.py, untouched) with, per
frame and only for this render:
- Pam v4 (pam_xmas3 + xmas_pam3): the canon head, deadpan pressed lips, the side-eye at Don in the still beat,
  "Human in the loop." said with the mask up, then the visible drop over her readers, the push-in and the hold;
- the banner on two rows, "MERRY CHRISTMAS" over "TO ALL", inside the widest frame (it read "Y CHRISTMAS TO AL");
- the company sign moved in (it was cropped to "UPTIME" at 4 s) and lower in the last shot (its top was cut);
- Sofia's badge raised above her forearm (the arm hid its A: "SOFI");
- the razor on the floor without Don's fingers (it read as a cut-off hand), bigger, with a blob of foam;
- every bubble tail aimed at the speaker and stopping at the edge of the head ("Eww." keeps its two tails).
v2 (xmas_anim2_v1.py = v1 kept), after the frame review: no cropped words anywhere:
- the banner rows sit where every camera shows them whole or not at all ("MERRY CHRISTMAS" y 176, "TO ALL" y 208
  under MERRY); the company sign is left out of the shots whose camera would cut it (6, 7, 9), the incident board
  out of shot 8, the door's PARTY sign out of 10b;
- tails reach the speaker's mouth from the side: the box stays where it was, the tip lands at the cheek at mouth
  height on the side facing the frame centre, so it points at the mouth without covering eyes or mouth.
Render: python3 engine_v.py xmas_anim2 (540) / python3 engine_hd.py xmas_anim2 (1080)."""
import math
import kit
import brand
from kit import INK, rect, text, ellipse, cut, ease, clamp
import xmas_anim as xa
import xmas_set as xs
import xmas_sb_v2 as sb
import sofia_xmas as sx
import don_xmas as dx
import pt42
import xmas_pam3 as route
import xmas_bubbles as xb

RAW_T = 0.0
DURATION = xa.DURATION
SHOT11 = (26.9, 28.9)
NO_SIGN = ((11.8, 13.4), (13.4, 15.8), (19.8, 21.5))               # shots 6, 7, 9 (cameras 6 and 7)
NO_BOARD = ((15.8, 19.8),)                                          # shot 8 (motion test A's camera)
NO_PARTY = ((13.4, 15.8), (19.8, 21.5), (25.5, 26.9))         # shots 7, 9 and 10b
TIPS = {}
_saved = {}


def banner2(k, x0=None, x1=None, y=None, words=None):
    """Two rows of bunting, the same flags, both inside the widest camera (world x 118-550)."""
    xs_banner = _saved["banner"]
    xs_banner(k, 140, 520, 176, "MERRY CHRISTMAS")
    step = (520 - 140) / 15
    xs_banner(k, 140, 140 + 6 * step, 208, "TO ALL")                 # under MERRY: out of the push-in's frame


def wall2(k):
    c = k.c
    rect(k, -600, -400, 2200, xs.FLOOR_Y + 400, kit.WALL, 100, shadow=False, outline=False)
    rect(k, -600, xs.FLOOR_Y, 2200, 900, kit.FLOOR, 101, shadow=False)
    rect(k, -600, xs.FLOOR_Y - 10, 2200, 16, (0.62, 0.5, 0.36), 102, shadow=False, lw=2)
    t = xa.ACT.get("t", 0.0)
    y = 340 if SHOT11[0] <= t < SHOT11[1] else 300                  # lower in the last shot's tight frame
    if not any(a <= t < b for a, b in NO_SIGN):                      # left out where the camera would cut it
        pt42.wall_sign(k, 340, y, 30)


def badge_high(k, body_top, seed):
    """Sofia's badge, raised above the forearm of her ornament pose."""
    c = k.c
    rect(k, 5, body_top + 30, 34, 20, (1, 1, 1), seed + 40, shadow=False, lw=1.8)
    c.set_source_rgb(*brand.GREEN); c.rectangle(8, body_top + 32, 28, 3.5); c.fill()
    text(k, "SOFÍA", 22, body_top + 42, 9.5, INK)


def razor_floor(k, hand, s=1.0, ang=-0.9, seed=540):
    """The razor on its own (no fingers), a size bigger, with a blob of foam on the blade."""
    t = xa.ACT.get("t", 0.0)
    if not (SHOT11[0] <= t < SHOT11[1]):
        return _saved["razor"](k, hand, s, ang, seed)
    c = k.c
    hx, hy = hand
    s *= 1.3
    c.save(); c.translate(hx, hy); c.scale(s, s); c.rotate(ang)
    rect(k, -4, -30, 8, 40, dx.RAZOR, seed, shadow=False, lw=1.8)                   # the handle
    rect(k, -11, -40, 22, 10, (0.88, 0.90, 0.93), seed + 1, shadow=False, lw=1.8)   # the head
    c.set_source_rgb(*INK); c.set_line_width(1.2); c.move_to(-9, -35); c.line_to(9, -35); c.stroke()
    for fx, fy, r in ((-5, -44, 5), (2, -46, 6), (8, -43, 4.5)):                     # the foam
        ellipse(k, fx, fy, r, r, (1, 1, 1), seed + 5, shadow=False, lw=1.2)
    c.restore()


def top2(cam, x, feet, hy, lift=62):
    """v2: the anchor that places the box is unchanged; the tail's tip is moved to the cheek at mouth height, on the
    side facing the frame centre (remembered here, swapped in by _tail2)."""
    a = _saved["top"](cam, x, feet, hy, lift)
    hx, hy_s = xs.to_screen(cam, x, feet + hy)
    z = cam[2]
    robot = lift >= 100
    r, my = (60 * z, 14 * z) if robot else (47 * z, 27 * z)
    side = 1 if hx < 270 else -1
    TIPS[(round(a[0], 1), round(a[1], 1))] = (hx + side * r, hy_s + my)
    return a


def _tail2(c, bx, by, bw, bh, ax, ay, width=13):
    tip = TIPS.get((round(ax, 1), round(ay, 1)))
    if tip:
        ax, ay = tip
    return _saved["tail"](c, bx, by, bw, bh, ax, ay, width)


def board2(k, x, y, w=118, h=86):
    t = xa.ACT.get("t", 0.0)
    if any(a <= t < b for a, b in NO_BOARD):
        return
    _saved["board"](k, x, y, w, h)


def door2(k, x=None, open_amt=0.0):
    t = xa.ACT.get("t", 0.0)
    x = xs.POS["door_x"] if x is None else x
    if not any(a <= t < b for a, b in NO_PARTY):
        return kit.door(k, x, xs.FLOOR_Y - 250, 110, 250, 960, open_amt=open_amt, sign="PARTY")
    c = k.c; y = xs.FLOOR_Y - 250
    c.save(); c.rectangle(x - 40, y - 12, 200, 400); c.clip()                 # the door without its sign above it
    try:
        kit.door(k, x, y, 110, 250, 960, open_amt=open_amt, sign="PARTY")
    finally:
        c.restore()


def _on():
    _saved.update(banner=xs.banner, wall=xs.wall, razor=dx.razor, top=sb.top, hook=sx.BADGE_HOOK, tail=xb._tail,
                  board=xs.incident_board, door=xs.door)
    xs.banner, xs.wall, dx.razor, sb.top = banner2, wall2, razor_floor, top2
    xb._tail, xs.incident_board, xs.door = _tail2, board2, door2
    sx.BADGE_HOOK = badge_high
    route.apply()


def _off():
    route.restore()
    xs.banner, xs.wall, dx.razor, sb.top = _saved["banner"], _saved["wall"], _saved["razor"], _saved["top"]
    xb._tail, xs.incident_board, xs.door = _saved["tail"], _saved["board"], _saved["door"]
    TIPS.clear()
    sx.BADGE_HOOK = _saved["hook"]


def _wrap(fn):
    def panel(k, t, tl):
        xa.RAW_T = RAW_T
        _on()
        try:
            fn(k, t, tl)
        finally:
            _off()
    panel.__name__ = getattr(fn, "__name__", "panel")
    return panel


PANELS = [(t0, t1, _wrap(fn)) for t0, t1, fn in xa.PANELS]
