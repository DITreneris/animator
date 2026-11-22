"""SOFÍA in "Daddy's Home" (episode 12): the power suit. Tomas, 21 Nov, /grill-me: a power suit, cream, her hair loose as it
was, and she changes for the visit: episode 11's look (sofia_cs, wine) until beat 8; from 8.4 she is back in this, CV
in hand. Dressed for the investor, not for Don.
Built like sofia_cs: the same rig (sofia_ob), colours swapped in and put back, so nothing older changes.
- a cream blazer with wide padded shoulders and peaked lapels edged in gold, two gold buttons;
- a black silk top under it (the cream reads against it, and against the black and burgundy of Father's people);
- a cream pencil skirt; her triangle earrings and her hair stay.
  o = sofia(k, x, feet, s, pose, face_kind, look, ...)      the same signature as sofia_cs.sofia
  python3 sofia_dh.py  -> ../daddys-home/dh_sofia_v1.png"""
import math
import cairo
import kit
import sofia_v4 as sf
import sofia_ss as ss
import sofia_bc as sbc
import sofia_ob as so
import sofia_cs as scs
from kit import Ctx, INK, cut, ellipse, rect
from sofia_v4 import GOLD, GOLD_LIGHT

CREAM = (0.99, 0.97, 0.91)                                 # lighter than the office wall (0.91, 0.86, 0.76), so she stands off it
CREAM_SHADE = (0.84, 0.78, 0.64)
SILK = (0.09, 0.09, 0.11)
SILK_SHADE = (0.20, 0.20, 0.23)


def _suit(base):
    def blazer(k, body_top, seed):
        c = k.c
        for sx in (-1, 1):                                   # the shoulders: padded, wider than she is
            cut(k, [(sx * 30, body_top - 4), (sx * 52, body_top + 2), (sx * 54, body_top + 20), (sx * 40, body_top + 26)],
                CREAM, shadow=False, lw=2.2)
        cut(k, [(-17, body_top - 1), (17, body_top - 1), (14, body_top + 118), (-14, body_top + 118)], SILK, shadow=False, lw=1.6)   # the black silk top
        cut(k, [(0, body_top + 30), (-11, body_top - 2), (11, body_top - 2)], sf.SKIN, shadow=False, lw=1.6)    # its V neck
        base(k, body_top, seed)
        for sx in (-1, 1):                                   # peaked lapels, a gold edge
            cut(k, [(sx * 15, body_top - 1), (sx * 34, body_top - 5), (sx * 37, body_top + 12), (sx * 27, body_top + 14),
                    (sx * 25, body_top + 36), (sx * 9, body_top + 54)], CREAM, shadow=False, lw=1.8)
            c.set_source_rgb(*GOLD); c.set_line_width(1.6); c.set_line_cap(1)
            c.move_to(sx * 34, body_top - 4); c.line_to(sx * 36, body_top + 11); c.line_to(sx * 27, body_top + 13)
            c.line_to(sx * 25, body_top + 35); c.stroke()
            c.set_source_rgb(*CREAM_SHADE); c.set_line_width(1.6)   # a flap pocket
            c.move_to(sx * 19, body_top + 94); c.line_to(sx * 34, body_top + 93); c.stroke()
        ellipse(k, 12, body_top + 86, 3.6, 3.6, GOLD, seed + 49, shadow=False, lw=1.4)     # the second button
    return blazer


def sofia(k, x, feet, s=1.0, pose="hold", face_kind="smile", look=(0, 0), lag=(0, 0), seed=7, badge=True, lean=0.0,
          mouth=None, sparkle=0.0, tablet_kind="auto"):
    old = (scs.WINE, scs.WINE_SHADE, scs.SATIN, scs._collar)
    scs.WINE, scs.WINE_SHADE, scs.SATIN = CREAM, CREAM_SHADE, CREAM_SHADE
    scs._collar = lambda k_, bt, sd: None                      # the wine look's satin collar is not this suit's
    old_ss = (ss.BLOUSE, ss.BLOUSE_SHADE, sf.BLOUSE)
    base = sbc._blazer
    sbc._blazer = _suit(base)
    try:
        # sofia_cs sets blouse and skirt to its WINE (now cream); the silk top is drawn over the blouse's V afterwards
        o = scs.sofia(k, x, feet, s, pose, face_kind, look, lag, seed, badge, lean, mouth, sparkle, tablet_kind)
    finally:
        sbc._blazer = base
        scs.WINE, scs.WINE_SHADE, scs.SATIN, scs._collar = old
    return o


def cv(k, x, y, s=1.0, ang=-0.08, seed=3100):
    """Her CV (episode 9's sheet): held out in 9.6."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    rect(k, -26, -36, 52, 72, (0.99, 0.98, 0.95), seed, lw=2)
    kit.text(k, "CV", 0, -18, 15, INK)
    ellipse(k, -12, 2, 7, 7, (0.90, 0.74, 0.62), seed + 1, shadow=False, lw=1.3)
    c.set_source_rgb(*INK); c.set_line_width(1.6)
    for yy in (-4, 4, 16, 24):
        c.move_to(2 if yy < 10 else -18, yy); c.line_to(20, yy); c.stroke()
    c.restore()


def sheet(out="../daddys-home/dh_sofia_v1.png"):
    Wd, Hd, Z = 1500, 1000, 2.2
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, Wd, Hd); c = cairo.Context(surf)
    c.set_source_rgb(*kit.WALL); c.paint()
    c.set_source_rgb(*kit.FLOOR); c.rectangle(0, 880, Wd, 120); c.fill()
    k = Ctx(c, 0)
    kit.text(k, "DADDY'S HOME · SOFÍA · the power suit · v1", Wd / 2, 46, 34, INK)
    kit.text(k, "she changes for the visit: episode 11's look until beat 8, the suit from 8.4", Wd / 2, 82, 19, INK, font=kit.MONO)
    F = 900
    S = 0.56 * Z
    scs.sofia(k, 190, F, S, "hold", "smile", look=(0.6, 0))
    sofia(k, 520, F, S, "stand", "smile", look=(-0.6, 0))
    sofia(k, 850, F, S, "lapel", "interested", look=(0.8, 0))
    o2 = sofia(k, 1190, F, S, "stand", "caught", look=(0.8, 0.1))
    cv(k, o2["hands"][1][0] + 26, o2["hands"][1][1] - 10, 1.5) if isinstance(o2, dict) and "hands" in o2 else None
    for name, note, x in (("EPISODE 11", "the wine look: beats 1 to 7", 190), ("THE SUIT", "cream, black silk, gold edges", 520),
                          ("8.4", "she walks back in, smoothing a lapel", 850), ("9.6", "the CV is taken; the smile stays", 1190)):
        kit.text(k, name, x, 940, 24, INK); kit.text(k, note, x, 968, 15, INK, font=kit.MONO)
    surf.write_to_png(out); print("wrote", out)


if __name__ == "__main__":
    sheet()
