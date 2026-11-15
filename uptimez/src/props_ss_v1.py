"""Secret Santa props shared by the sheets, storyboard and animation (v1):
- lipstick(k, x, y, s, ang, uncap): Pam's dusty-rose nude, a gold cap; uncap 0..1 slides the cap off;
- compact(k, x, y, s, ang, open_): Sofia's round gold compact mirror; open_ 0..1 swings the lid up;
- kiss(k, x, y, s): a dusty-rose lipstick kiss mark (reads on cream);
- soft(c, draw, radius): draws `draw()` into a layer and blurs it (background softness for close-ups)."""
import math
import cairo
import numpy as np
from PIL import Image, ImageFilter
from kit import INK, ellipse, rect

DUSTY_ROSE = (0.80, 0.47, 0.50)
DUSTY_ROSE_DARK = (0.62, 0.32, 0.36)
LIP_GOLD = (0.86, 0.66, 0.26)
LIP_GOLD_LIGHT = (1.0, 0.88, 0.55)
MIRROR = (0.80, 0.90, 0.97)


def lipstick(k, x, y, s=1.0, ang=0.0, uncap=0.0, seed=0):
    """(x, y) = the base of the tube; it points up (ang rotates). Length about 46 units at s=1."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    rect(k, -7, -20, 14, 20, LIP_GOLD, seed + 1, shadow=False, lw=1.8)              # the gold base
    c.set_source_rgb(*LIP_GOLD_LIGHT); c.rectangle(-4.5, -18, 2.5, 16); c.fill()
    rect(k, -6, -26, 12, 6, (0.70, 0.52, 0.18), seed + 2, shadow=False, lw=1.4)    # the collar
    c.move_to(-5, -26); c.line_to(-5, -36); c.line_to(5, -42); c.line_to(5, -26); c.close_path()   # the bullet
    c.set_source_rgb(*DUSTY_ROSE); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.6); c.stroke()
    c.set_source_rgba(1, 1, 1, 0.45); c.set_line_width(1.6); c.move_to(-3, -28); c.line_to(-3, -36); c.stroke()
    if uncap < 1.0:                                                                  # the cap, sliding off
        lift = 26 * uncap
        c.save(); c.translate(0, -lift); c.rotate(0.5 * uncap)
        rect(k, -7.5, -46, 15, 22, LIP_GOLD, seed + 3, shadow=False, lw=1.8)
        c.set_source_rgb(*LIP_GOLD_LIGHT); c.rectangle(-5, -44, 2.5, 18); c.fill()
        c.restore()
    c.restore()


def compact(k, x, y, s=1.0, ang=0.0, open_=1.0, seed=0):
    """(x, y) = the hinge; the base hangs below it, the lid swings up showing the mirror."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    ellipse(k, 0, 15, 17, 15, LIP_GOLD, seed + 1, shadow=False, lw=1.8)             # the base
    ellipse(k, 0, 15, 12, 10.5, (0.93, 0.82, 0.74), seed + 2, shadow=False, lw=1.2)  # powder
    if open_ > 0:
        c.save(); c.scale(1, max(0.08, open_))
        ellipse(k, 0, -15, 17, 15, LIP_GOLD, seed + 3, shadow=False, lw=1.8)        # the lid
        ellipse(k, 0, -15, 13, 11.5, MIRROR, seed + 4, shadow=False, lw=1.4)        # the mirror
        c.set_source_rgba(1, 1, 1, 0.8); c.set_line_width(2.2)
        c.move_to(-7, -20); c.line_to(-1, -26); c.stroke()
        c.restore()
    c.restore()


def kiss(k, x, y, s=1.0, ang=-0.12):
    """A lipstick kiss: two lobed upper lips and a fuller lower lip, with the print's creases."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    c.move_to(-16, 0)
    c.curve_to(-12, -9, -5, -9, 0, -3)
    c.curve_to(5, -9, 12, -9, 16, 0)
    c.curve_to(10, 11, -10, 11, -16, 0); c.close_path()
    c.set_source_rgba(*DUSTY_ROSE, 0.92); c.fill()
    c.set_source_rgba(*DUSTY_ROSE_DARK, 0.9); c.set_line_width(1.0)
    c.move_to(-14, 0.5); c.curve_to(-6, 2.5, 6, 2.5, 14, 0.5); c.stroke()          # the parting line
    for i in range(-3, 4):
        c.move_to(i * 3.6, 2.5); c.line_to(i * 3.9, 7); c.stroke()                  # creases
    c.restore()


def sparkle(c, x, y, r, a=1.0):
    """A 4-point sparkle star."""
    if a <= 0:
        return
    c.save(); c.translate(x, y)
    c.move_to(0, -r); c.curve_to(r * 0.12, -r * 0.12, r * 0.12, -r * 0.12, r, 0)
    c.curve_to(r * 0.12, r * 0.12, r * 0.12, r * 0.12, 0, r)
    c.curve_to(-r * 0.12, r * 0.12, -r * 0.12, r * 0.12, -r, 0)
    c.curve_to(-r * 0.12, -r * 0.12, -r * 0.12, -r * 0.12, 0, -r); c.close_path()
    c.set_source_rgba(1, 1, 1, a); c.fill_preserve()
    c.set_source_rgba(0.95, 0.85, 0.45, a * 0.8); c.set_line_width(max(0.8, r * 0.08)); c.stroke()
    c.restore()


def soft(c, draw, radius=6.0):
    """Draw `draw()` into a transparent layer the size of the current target and composite it blurred."""
    tgt = c.get_target()
    w, h = tgt.get_width(), tgt.get_height()
    lay = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    lc = cairo.Context(lay); lc.set_matrix(c.get_matrix())
    draw(lc)
    lay.flush()
    a = np.ndarray((h, w, 4), np.uint8, lay.get_data()).copy()
    img = Image.frombuffer("RGBA", (w, h), a.tobytes(), "raw", "RGBA", 0, 1)
    sx = abs(c.get_matrix()[0])
    img = img.filter(ImageFilter.GaussianBlur(radius * sx))
    b = np.asarray(img).copy()
    out = cairo.ImageSurface.create_for_data(memoryview(b), cairo.FORMAT_ARGB32, w, h, w * 4)
    c.save(); c.identity_matrix(); c.set_source_surface(out, 0, 0); c.paint(); c.restore()
