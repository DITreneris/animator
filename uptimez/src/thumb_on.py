"""v2 (thumb_on_v1.py = v1, kept): the new name, "Office Noir: The Secret of a Stolen Heart", on three typewriter
cards ("OFFICE NOIR" / "The Secret of a" / "Stolen Heart"); the picture is unchanged.
v1 notes: Cover for "Office Noir: The Red Heart" (1080x1920, drawn natively at 1080 with the film's own kit). Inside the
centre the profile grids crop to (y 120-840 at the 540x960 drawing scale): Don in his trench and fedora under a
hard side light and the blinds, holding his magnifier over the red heart on his lapel (the clue that convicts him,
the only red in the picture); Mom's curler shadow already looms on the wall behind him (the boss, planted); the rain
window and the agency door. The title is two typewriter caption cards, as in the film.
Usage: python3 thumb_on.py out.png"""
import sys
import math
import cairo
import kit
from kit import Ctx
import don_on as d
import props_on as pr
import on_set as st
import engine_on as eng
import on_sb as sb
import props_sheet_on as psh
import on_film as of

X, FEET, S = 205, 1250, 2.35


def scene(kk):
    st.office_back(kk, t=0.6, door_x=700, window_x=24)
    c = kk.c                                                   # a pool of light on the wall, so her shadow reads
    g = cairo.RadialGradient(440, 420, 30, 440, 420, 260)
    g.add_color_stop_rgba(0, 0.95, 0.93, 0.88, 0.55); g.add_color_stop_rgba(1, 0.95, 0.93, 0.88, 0)
    c.set_source(g); c.rectangle(0, 0, 540, 960); c.fill()
    st.mom_shadow(kk, 440, 905, 1.15, skew=-0.12, alpha=0.92, head=1.6, big=True)
    d.don_noir(kk, X, FEET, S, face="cynic", look=(0.5, 0.9), brim=0.55, outline=True, heart_on=True)


def light(c):
    st.blinds(c, 0, 80, 540, 760, angle=-0.30, amount=0.30)
    st.hard_side(c, 330, 0.10, 0.40)
    st.key_light(c, X, FEET + d.HY * S, 170, 0.28)
    st.vignette(c, 0.30)


def main(out):
    of.hi_on()
    try:
        d.FEDORA_BAND, d.FEDORA_RIM = (0.42, 0.42, 0.44), True
        base = sb.noir(scene, light)
        pic = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)
        c = cairo.Context(pic)
        c.set_source_surface(base, 0, 0); c.paint()
        hx, hy = X + d.LAPEL_HEART[0] * S, FEET + d.LAPEL_HEART[1] * S        # the magnifier over the heart
        lx, ly, r, rot = hx + 4, hy - 2, 58, 0.85
        pr.lens_view(c, base, lx, ly, r, zoom=1.8, rot=rot)
        k = Ctx(c, 0)                                                        # his hand on the handle
        ex, ey = lx + math.cos(rot) * r * 1.95, ly + math.sin(rot) * r * 1.95
        kit.ellipse(k, ex, ey, 9 * S, 8 * S, (0.80, 0.80, 0.80), 980, shadow=False, lw=2.2)
        psh.caption(c, "OFFICE NOIR", 24, 150, 58)
        psh.caption(c, "The Secret of a", 24, 150 + 58 * 1.9, 34)
        psh.caption(c, "Stolen Heart", 24, 150 + 58 * 1.9 + 34 * 1.9, 34)
        surf = of.ORIG["surface"](cairo.FORMAT_ARGB32, 1080, 1920)
        cs = cairo.Context(surf); cs.scale(2, 2); cs.set_source_surface(pic, 0, 0); cs.paint()
        surf.write_to_png(out)
    finally:
        of.hi_off()
        d.FEDORA_BAND, d.FEDORA_RIM = None, False


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "on_cover_v2.png")
