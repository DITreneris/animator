"""ANIMATION v2 of the Christmas special "Happy Compliance": the approved v1 (xmas_anim.py, untouched) with, per
frame and only for this render:
- Pam v4 (pam_xmas3 + xmas_pam3): the canon head, deadpan pressed lips, the side-eye at Don in the still beat,
  "Human in the loop." said with the mask up, then the visible drop over her readers, the push-in and the hold;
- the banner on two rows, "MERRY CHRISTMAS" over "TO ALL", inside the widest frame (it read "Y CHRISTMAS TO AL");
- the company sign moved in (it was cropped to "UPTIME" at 4 s) and lower in the last shot (its top was cut);
- Sofia's badge raised above her forearm (the arm hid its A: "SOFI");
- the razor on the floor without Don's fingers (it read as a cut-off hand), bigger, with a blob of foam;
- every bubble tail aimed at the speaker and stopping at the edge of the head ("Eww." keeps its two tails).
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

RAW_T = 0.0
DURATION = xa.DURATION
SHOT11 = (26.9, 28.9)
_saved = {}


def banner2(k, x0=None, x1=None, y=None, words=None):
    """Two rows of bunting, the same flags, both inside the widest camera (world x 118-550)."""
    xs_banner = _saved["banner"]
    xs_banner(k, 140, 520, 192, "MERRY CHRISTMAS")
    step = (520 - 140) / 15
    xs_banner(k, 330 - 3 * step, 330 + 3 * step, 240, "TO ALL")


def wall2(k):
    c = k.c
    rect(k, -600, -400, 2200, xs.FLOOR_Y + 400, kit.WALL, 100, shadow=False, outline=False)
    rect(k, -600, xs.FLOOR_Y, 2200, 900, kit.FLOOR, 101, shadow=False)
    rect(k, -600, xs.FLOOR_Y - 10, 2200, 16, (0.62, 0.5, 0.36), 102, shadow=False, lw=2)
    t = xa.ACT.get("t", 0.0)
    y = 340 if SHOT11[0] <= t < SHOT11[1] else 300                  # lower in the last shot's tight frame
    pt42.wall_sign(k, 340, y, 30)                                    # spans x 325-482: inside every camera


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
    """Tails stop at the edge of the head, pointing down at the mouth (people: the hair or cap line; the robot:
    the rim of its screen under the Santa hat)."""
    new = lift * 0.52 if lift >= 100 else lift - 20
    return _saved["top"](cam, x, feet, hy, new)


def _on():
    _saved.update(banner=xs.banner, wall=xs.wall, razor=dx.razor, top=sb.top, hook=sx.BADGE_HOOK)
    xs.banner, xs.wall, dx.razor, sb.top = banner2, wall2, razor_floor, top2
    sx.BADGE_HOOK = badge_high
    route.apply()


def _off():
    route.restore()
    xs.banner, xs.wall, dx.razor, sb.top = _saved["banner"], _saved["wall"], _saved["razor"], _saved["top"]
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
