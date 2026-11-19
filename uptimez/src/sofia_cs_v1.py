"""v1, pinned: uptimez-sofia-cs-v1-sheet.png. sofia_cs.py is current.
SOFIA, "Customer Success" (episode 11), v1: dressed for him (Tomas, 18 Nov /grill-me: "dressed for him",
big geometric earrings, waves over one shoulder). It is Friday and the Client comes back; she has dressed for a man
who spends the episode looking at Pam, which is under her one line, "He's not looking at you."
Built on The Onboarding's Sofía (sofia_ob: her faces, poses, the clipboard and the tablet), with this episode's look:
- A WINE BLAZER-DRESS: the blazer, the top and the skirt all one deep wine, the lapels in a lighter satin edged in
  gold; no pearls (the strand is off), a gold cuff on her wrist instead of the pearl bracelet;
- BIG GEOMETRIC EARRINGS: an open gold triangle on a stud, point down, about twice her hoop; they swing with `lag`;
- WAVES: all her hair over her right shoulder (screen-left) in three scallops, her other ear showing (sofia_ss SWEPT).
Every pose and face of sofia_ob works here. sofia_ob, sofia_bc and sofia_ss draw exactly as before: their colours
and hooks are swapped for the length of one call and restored.
Usage: sofia(k, x, feet, s, pose, face_kind, look, lag, seed, badge, lean, mouth, sparkle, tablet_kind)"""
import math
import kit
import sofia_v4 as sf
import sofia_ss as ss
import sofia_bc as sbc
import sofia_ob as so
from kit import INK, cut, ellipse
from sofia_v4 import GOLD, GOLD_LIGHT

WINE = (0.42, 0.07, 0.18)
WINE_SHADE = (0.30, 0.04, 0.12)
SATIN = (0.62, 0.16, 0.30)
TRI = sbc.DROP * 0.95                                      # the triangle's height: about twice her hoop
HY, BODY_TOP = so.HY, so.BODY_TOP
POSES = so.POSES


def triangle(k, x, y, lgx=0.0, spark=0.0, seed=0):
    """A gold stud at the lobe (x, y) and an open gold triangle under it, point down; it swings with lgx."""
    if x < 0:                                              # that ear is under the waves
        return
    c = k.c
    c.save(); c.translate(x, y + 3); c.rotate(-lgx * 0.05)
    h, w = TRI, TRI * 0.82
    pts = [(-w / 2, 4), (w / 2, 4), (0, 4 + h)]
    for col, lw in ((INK, 7.0), (GOLD, 4.2)):
        c.set_source_rgb(*col); c.set_line_width(lw); c.set_line_join(0)
        c.move_to(*pts[0]); c.line_to(*pts[1]); c.line_to(*pts[2]); c.close_path(); c.stroke()
    c.set_source_rgb(*GOLD_LIGHT); c.set_line_width(1.6)
    c.move_to(pts[0][0] + 3, 5); c.line_to(pts[1][0] - 6, 5); c.stroke()
    c.restore()
    ellipse(k, x, y, 4.6, 4.6, GOLD, seed, shadow=False, lw=1.7)


def _gold_bead(k, x, y, r, seed, lw=1.5):
    """The cuff: drawn where the pearl bracelet was, as gold."""
    ellipse(k, x, y, r * 1.05, r * 1.05, GOLD, seed, shadow=False, lw=lw)


def _collar(k, body_top, seed):
    """The satin lapels, edged in gold, over the blazer."""
    c = k.c
    for sx in (-1, 1):
        cut(k, [(sx * 15, body_top - 1), (sx * 32, body_top - 3), (sx * 27, body_top + 34), (sx * 9, body_top + 52)],
            SATIN, shadow=False, lw=1.8)
        c.set_source_rgb(*GOLD); c.set_line_width(1.6)
        c.move_to(sx * 32, body_top - 2); c.line_to(sx * 27, body_top + 33); c.stroke()


def sofia(k, x, feet, s=1.0, pose="hold", face_kind="smile", look=(0, 0), lag=(0, 0), seed=7, badge=True, lean=0.0,
          mouth=None, sparkle=0.0, tablet_kind="auto"):
    old = (ss.BLOUSE, ss.BLOUSE_SHADE, ss.SKIRT, sf.BLOUSE, sbc.BLAZER, sbc.BLAZER_EDGE, so.drop, so.strand, so.pearl,
           ss.SWEPT[0], sbc._blazer)
    base_blazer = sbc._blazer

    def blazer(k_, body_top, seed_):
        base_blazer(k_, body_top, seed_)
        _collar(k_, body_top, seed_)
    ss.BLOUSE, ss.BLOUSE_SHADE, ss.SKIRT, sf.BLOUSE = WINE, WINE_SHADE, WINE, WINE
    sbc.BLAZER, sbc.BLAZER_EDGE = WINE, SATIN
    so.drop, so.strand, so.pearl = triangle, (lambda k_, seed_: None), _gold_bead
    ss.SWEPT[0] = True
    sbc._blazer = blazer
    try:
        return so.sofia(k, x, feet, s, pose, face_kind, look, lag, seed, badge, lean, mouth, sparkle, tablet_kind)
    finally:
        (ss.BLOUSE, ss.BLOUSE_SHADE, ss.SKIRT, sf.BLOUSE, sbc.BLAZER, sbc.BLAZER_EDGE, so.drop, so.strand, so.pearl,
         ss.SWEPT[0], sbc._blazer) = old
