"""v2 (sofia_cs_v1.py = v1, kept), after the outside review of the sheet (19 Nov): the design is approved; the faces
that blurred are redrawn here so the run KNOWING -> CAUGHT -> RECOVER is unmistakable:
- "interested": eyes open (lids at a quarter), ONE brow lifted, the soft closed smile: curious about him, not sceptical;
- "caught": both brows high, eyes wide open, pupils hard to the side, lips pressed flat: startled, and she hides it;
- "recover": a forced smile, too wide, teeth together, while the eyes stay wary (lids low, pupils still on whoever
  saw) and the brows stay tense: the smile has come back before she has;
- "deadpan": level brows, half lids, pupils dead centre, lips flat: no reaction at all (v1's raised brow read as annoyed).
The earring's pivot is the stud; its swing is clamped (TRI_SWING) so it never reaches the jaw on a head turn.
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
import cairo
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
    c.save(); c.translate(x, y + 3); c.rotate(max(-TRI_SWING, min(TRI_SWING, -lgx * 0.05)))   # v2: about the stud, clamped
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


TRI_SWING = 0.16                                           # v2: the most the triangle turns, in radians
OWN = {"interested": "interested", "caught": "caught", "recover": "caught", "deadpan": "caught"}   # face -> sofia_ob face under it


def _snap(c):
    """A copy of what is drawn so far (the forehead with the fringe's shadow on it, before her features)."""
    try:
        t = c.get_group_target(); t.flush()
        sx, sy = t.get_device_scale()
        snap = cairo.ImageSurface(cairo.FORMAT_ARGB32, t.get_width(), t.get_height())
        snap.set_device_scale(sx, sy)
        cc = cairo.Context(snap); cc.set_source_surface(t, 0, 0); cc.set_operator(cairo.OPERATOR_SOURCE); cc.paint()
        return snap
    except Exception:
        return None


def _cover(k, x, y, seed, snap=None):
    """Her brows and eyes taken off again, so they can be redrawn: the skin as it was before them, shadow and all."""
    c = k.c
    if snap is not None:
        c.save(); c.new_path()
        c.save(); c.translate(x, y - 24); c.scale(36, 14); c.arc(0, 0, 1, 0, 6.2832); c.restore()
        for sx in (-17, 17):
            c.save(); c.translate(x + sx, y - 2); c.scale(25, 19); c.arc(0, 0, 1, 0, 6.2832); c.restore()
        c.set_fill_rule(cairo.FILL_RULE_WINDING); c.clip()
        c.identity_matrix(); c.set_source_surface(snap, 0, 0); c.paint()
        c.restore()
        return
    c.save(); c.rectangle(x - 40, y - 37, 80, 60); c.clip()               # fallback: flat skin, below the hairline
    ellipse(k, x, y - 24, 33, 13, so.SKIN, seed + 300, shadow=False, outline=False)
    c.restore()
    for sx in (-17, 17):
        ellipse(k, x + sx, y - 1, 20, 16.5, so.SKIN, seed + 301 + sx, shadow=False, outline=False)


def _brow(c, x0, y0, x1, y1, lift=3.0, w=4.0):
    c.set_source_rgb(*INK); c.set_line_width(w); c.set_line_cap(1)
    c.move_to(x0, y0); c.curve_to(x0 + (x1 - x0) * 0.35, y0 - lift, x0 + (x1 - x0) * 0.7, y1 - lift, x1, y1); c.stroke()


def _mine(orig_builder, own):
    def builder(inner, blush, sp=None):
        base = orig_builder(inner, blush, sp)

        def face(k, x, y, kind="neutral", look=(0, 0), seed=0):
            snap = _snap(k.c)
            base(k, x, y, kind, look, seed)
            c = k.c
            my = y + 29
            if own == "interested":
                _cover(k, x, y, seed, snap)
                so._eyes(k, x, y, look, seed, lid=-8.0)
                _brow(c, x - 27, y - 20, x - 8, y - 22)
                _brow(c, x + 8, y - 31, x + 27, y - 26, lift=4)            # one brow lifted: curious
            elif own == "caught":
                _cover(k, x, y, seed, snap)
                so._eyes(k, x, y, (max(-0.9, min(0.9, look[0])), -0.1), seed, lid=-10.0)   # wide open, pupils hard aside
                _brow(c, x - 27, y - 28, x - 8, y - 32, lift=3)
                _brow(c, x + 8, y - 32, x + 27, y - 28, lift=3)
            elif own == "recover":
                _cover(k, x, y, seed, snap)
                so._eyes(k, x, y, (max(-0.9, min(0.9, look[0])), 0.2), seed, lid=-3.0)    # still wary
                _brow(c, x - 27, y - 17, x - 8, y - 15, lift=1.5)           # tense, a little in
                _brow(c, x + 8, y - 15, x + 27, y - 17, lift=1.5)
                ellipse(k, x, my, 24, 13, so.SKIN, seed + 310, shadow=False, outline=False)
                c.move_to(x - 17, my - 4); c.curve_to(x - 6, my - 1, x + 6, my - 1, x + 17, my - 4)
                c.line_to(x + 15, my + 4); c.curve_to(x + 6, my + 6, x - 6, my + 6, x - 15, my + 4); c.close_path()
                c.set_source_rgb(1, 1, 1); c.fill_preserve()
                c.set_source_rgb(*so.RED); c.set_line_width(3.6); c.set_line_join(1); c.stroke()
                c.set_source_rgb(*INK); c.set_line_width(1.2)              # teeth together
                c.move_to(x - 14, my + 0.6); c.line_to(x + 14, my + 0.6); c.stroke()
                for tx in (-7, 0, 7):
                    c.move_to(x + tx, my - 2.4); c.line_to(x + tx, my + 3.6); c.stroke()
            elif own == "deadpan":
                _cover(k, x, y, seed, snap)
                so._eyes(k, x, y, (0.0, 0.25), seed, lid=-0.5)             # half lids, dead centre
                _brow(c, x - 27, y - 19, x - 8, y - 19, lift=0.5)
                _brow(c, x + 8, y - 19, x + 27, y - 19, lift=0.5)
        return face
    return builder


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
    own = face_kind if face_kind in OWN else None
    orig_face = so._face
    if own:
        so._face = lambda o, sp: _mine(orig_face(o, sp), own)
    try:
        return so.sofia(k, x, feet, s, pose, OWN.get(face_kind, face_kind), look, lag, seed, badge, lean, mouth, sparkle,
                        tablet_kind)
    finally:
        so._face = orig_face
        (ss.BLOUSE, ss.BLOUSE_SHADE, ss.SKIRT, sf.BLOUSE, sbc.BLAZER, sbc.BLAZER_EDGE, so.drop, so.strand, so.pearl,
         ss.SWEPT[0], sbc._blazer) = old
