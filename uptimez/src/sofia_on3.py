"""v2 (sofia_on3_v1.py = v1, kept), after the outside review of sheet v1 (19 Nov): the design is kept; two things
that carry her were too quiet at phone size:
- the hoop keeps two thirds of its gold in the dream (v1: a third, which on a thin ring at 270 px was grey);
- a new face, "spotted": the appraising smirk with the pupils hard into the corner toward him and the brow on that
  side lifted, so the close says she has seen someone, not that she is posing.
card_ang turns the card in "r_card" (default as v1).
SOFIA, "Office Noir 3: The Last Round", v1: the ring look (Tomas, 19 Nov, /grill-me).
She walks the round card in the Client's dream. What Tomas picked:
- a SHORT SATIN LEOTARD, 1940s: black satin, a sweetheart neckline, an ivory bow on the hip; bare arms and shoulders
  (black, because in the dream her blonde hair goes white: an ivory leotard and the hair were one pale shape);
- LONG HAIR in waves over her right shoulder (screen-left), the other ear showing (sofia_ss SWEPT);
- GOLD HOOPS: one shows, on the ear the waves leave free; it swings with `lag`;
- BLACK PATENT HEELS (not red: the film's red is the Client's robe and gloves), a white glint on each toe;
- STOCKINGS WITH A SEAM (a dark welt on the thigh; the seam is on the back view, legs_back());
- a black RIBBON at her neck, a white FEATHER in her hair, a BEAUTY MARK;
- her LIPS keep their colour: the first film's key red (sofia_on.HEART), the only colour on her in the dream.
Built on The Onboarding's Sofia (sofia_ob: her faces and poses). sofia_ob, sofia_bc, sofia_ss and sofia_v4 draw
exactly as before: their colours and hooks are swapped for the length of one call and restored.
Usage: sofia(k, x, feet, s, pose, face_kind, look, lag, seed, lean, mouth, card)
Poses (new names only): "r_hips", "r_card" (the card held high in one hand, the other on her hip), "r_side" (the card down at her side),
"r_down" (both arms down). card: None, or the text on it ("ROUND 1", "LAST ROUND")."""
import math
import kit
import sofia_v4 as sf
import sofia_ss as ss
import sofia_bc as sbc
import sofia_mf as sm
import sofia_ob as so
import sofia_on as son
import sofia_cs as cs
from kit import INK, cut, ellipse, text
from sofia_v4 import GOLD, GOLD_LIGHT

KEY = son.HEART                                            # the one red: her lips
SATIN = (0.09, 0.09, 0.11)                                 # black satin: it stands off her hair, her skin and the lit haze
SATIN_SHADE = (0.40, 0.40, 0.47)                           # its seams, lighter than the cloth
SHEEN = (0.80, 0.82, 0.90)
IVORY = (0.95, 0.93, 0.88)
IVORY_EDGE = (0.62, 0.60, 0.56)
PATENT = (0.05, 0.05, 0.06)
RIBBON = (0.06, 0.06, 0.07)
RIBBON_EDGE = (0.45, 0.45, 0.50)
SHEER = (0.66, 0.50, 0.40)                                 # the stockings: her skin, a tone down
WELT = (0.30, 0.22, 0.18)
FEATHER = (0.98, 0.98, 0.96)
FEATHER_SHADE = (0.74, 0.76, 0.80)
CARD = (0.98, 0.97, 0.94)
ACCENTS = [(KEY, 1.0), (GOLD, 0.65), (GOLD_LIGHT, 0.65)]   # the noir pass: lips in full; v2: the hoop keeps two thirds of its gold
HOOP_R = sm.HOOP_R                                         # the Mandatory Fun hoop: her big one
BT, HY = so.BODY_TOP, so.HY

so.POSES.update({                                          # new names only; nothing earlier uses them
    "r_hips": so._ik(-1, -37, BT + 100) + so._ik(1, 37, BT + 100),
    "r_card": so._ik(-1, -88, HY - 22) + so._ik(1, 37, BT + 100),   # one arm up, the card high beside her head
    "r_side": so._ik(-1, -62, BT + 96) + so._ik(1, 37, BT + 100),
    "r_down": so.LOW + so.REST,
})

_SKIP = [(-1.0, -1.0, -1.0), (-2.0, -2.0, -2.0)]           # stand-ins for the blouse and the skirt: not drawn


def hoop(k, x, y, lgx=0.0, spark=0.0, seed=0):
    """One big gold hoop on the ear the waves leave free; it hangs from the lobe and swings with lgx."""
    if x < 0:
        return
    c = k.c
    c.save(); c.translate(x + 3, y + 2); c.rotate(max(-0.2, min(0.2, -lgx * 0.05)))
    for col, lw in ((INK, 8.4), (GOLD, 5.4)):
        c.set_source_rgb(*col); c.set_line_width(lw); c.arc(0, HOOP_R, HOOP_R, 0, 2 * math.pi); c.stroke()
    c.set_source_rgb(*GOLD_LIGHT); c.set_line_width(1.8)
    c.arc(0, HOOP_R, HOOP_R, 1.15 * math.pi, 1.55 * math.pi); c.stroke()
    c.restore()


def _bare_arm(k, sx, sy, a1, a2, seed, ln=48, w=17):
    """A bare arm from the shoulder to the hand: no sleeve, no cuff."""
    dd = lambda a: (math.sin(math.radians(a)), math.cos(math.radians(a)))
    ex, ey = sx + dd(a1)[0] * ln, sy + dd(a1)[1] * ln
    hx, hy = ex + dd(a1 + a2)[0] * ln, ey + dd(a1 + a2)[1] * ln
    for (ax, ay, bx, by), w0, w1 in (((sx, sy, ex, ey), w, w * 0.9), ((ex, ey, hx, hy), w * 0.9, w * 0.74)):
        g = math.atan2(by - ay, bx - ax)
        nx, ny = -math.sin(g), math.cos(g)
        cut(k, [(ax + nx * w0 / 2, ay + ny * w0 / 2), (bx + nx * w1 / 2, by + ny * w1 / 2),
                (bx - nx * w1 / 2, by - ny * w1 / 2), (ax - nx * w0 / 2, ay - ny * w0 / 2)], so.SKIN, shadow=False, lw=2)
    ellipse(k, ex, ey, w * 0.40, w * 0.40, so.SKIN, seed + 2, shadow=False, outline=False)     # the elbow, closed
    ellipse(k, sx, sy, w * 0.50, w * 0.50, so.SKIN, seed + 3, shadow=False, outline=False)     # the shoulder, closed
    ellipse(k, hx, hy, w * 0.56, w * 0.56, so.SKIN, seed, shadow=False, lw=2)
    return hx, hy


def _leotard(k, bt, seed):
    """Drawn where her blouse and skirt are: bare shoulders, the satin leotard, the stocking tops, the ribbon."""
    c = k.c
    for sx_ in (-14, 14):                                  # her thighs above the stockings, and the dark welt
        cut(k, [(sx_ - 7.5, -99.5), (sx_ + 7.5, -99.5), (sx_ + 6.9, -83), (sx_ - 6.9, -83)], so.SKIN, shadow=False,
            outline=False)
        cut(k, [(sx_ - 7.0, -84), (sx_ + 7.0, -84), (sx_ + 6.7, -78), (sx_ - 6.7, -78)], WELT, shadow=False, outline=False)
    for o in (-1, 1):                                      # her hips, outside the leg line
        cut(k, [(o * 5, -98), (o * 23.2, -98), (o * 37, -112), (o * 37, bt + 98), (o * 5, bt + 98)], so.SKIN,
            shadow=False, outline=False)
        c.set_source_rgb(*INK); c.set_line_width(1.9); c.set_line_cap(1)
        c.move_to(o * 37, bt + 100); c.line_to(o * 37.2, -112); c.line_to(o * 22.6, -99); c.stroke()
    cut(k, [(-16, bt - 5), (16, bt - 5), (41, bt + 9), (43, bt + 40), (-43, bt + 40), (-41, bt + 9)], so.SKIN,
        shadow=False, lw=2)                                # bare shoulders that slope
    c.set_source_rgb(0.80, 0.56, 0.43); c.set_line_width(1.6); c.set_line_cap(1)
    for sx in (-1, 1):                                     # the collarbones
        c.move_to(sx * 8, bt + 19); c.line_to(sx * 27, bt + 15); c.stroke()
    body = [(-41, bt + 30), (-22, bt + 22), (0, bt + 35), (22, bt + 22), (41, bt + 30), (42, bt + 48), (30, bt + 98),
            (37, bt + 106), (30, -113), (17, -101), (6, -92), (-6, -92), (-17, -101), (-30, -113), (-37, bt + 106),
            (-30, bt + 98), (-42, bt + 48)]
    cut(k, body, SATIN, lw=2.2)
    c.set_source_rgb(*SATIN_SHADE); c.set_line_width(2.0); c.set_line_cap(1)
    c.arc(-19, bt + 38, 15, 0.15 * math.pi, 0.82 * math.pi); c.stroke()                       # the bust
    c.arc(19, bt + 38, 15, 0.18 * math.pi, 0.85 * math.pi); c.stroke()
    c.move_to(0, bt + 36); c.line_to(0, bt + 64); c.stroke()                                    # the centre seam
    for i, (x0, x1) in enumerate(((-27, 20), (-24, 26))):                                       # gathered at the waist
        c.move_to(x0, bt + 88 + i * 8); c.curve_to(x0 + 16, bt + 94 + i * 8, x1 - 16, bt + 84 + i * 8, x1, bt + 90 + i * 8)
        c.stroke()
    c.set_source_rgb(*SHEEN); c.set_line_width(3.0)                                             # satin: two long highlights
    c.move_to(-31, bt + 44); c.curve_to(-27, bt + 62, -23, bt + 78, -24, bt + 92); c.stroke()
    c.move_to(-22, -116); c.curve_to(-17, -110, -12, -105, -8, -99); c.stroke()
    bx, by = 32, bt + 99                                                                         # the bow on her hip
    for sgn in (-1, 1):
        cut(k, [(bx, by), (bx + sgn * 17, by - 10), (bx + sgn * 19, by + 9)], IVORY, shadow=False, lw=1.6)
    for dx in (-5, 5):
        cut(k, [(bx - 3, by + 2), (bx + 3, by + 2), (bx + dx + 4, by + 24), (bx + dx - 3, by + 22)], IVORY, shadow=False,
            lw=1.4)
    ellipse(k, bx, by, 4.6, 4.6, IVORY, seed + 51, shadow=False, lw=1.4)
    c.set_source_rgb(*IVORY_EDGE); c.set_line_width(1.2)
    for sgn in (-1, 1):
        c.move_to(bx + sgn * 5, by - 1); c.line_to(bx + sgn * 14, by - 5); c.stroke()
    cut(k, [(-17, bt + 6), (17, bt + 6), (17, bt + 13), (-17, bt + 13)], RIBBON, shadow=False, lw=1.4)   # the ribbon at her neck
    ellipse(k, 0, bt + 15, 3.4, 4.2, IVORY, seed + 52, shadow=False, lw=1.3)                    # and its one pearl drop


def feather(k, hy, seed=0):
    """A white plume pinned above the ear that shows, curving up and back."""
    c = k.c
    c.save(); c.translate(38, hy - 36); c.rotate(0.30)
    c.move_to(0, 0); c.curve_to(-14, -26, -6, -62, 16, -82); c.curve_to(30, -62, 28, -24, 6, 0); c.close_path()
    c.set_source_rgb(*FEATHER); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.0); c.set_line_join(1); c.stroke()
    c.set_source_rgb(*FEATHER_SHADE); c.set_line_width(1.5); c.set_line_cap(1)
    c.move_to(3, -2); c.curve_to(0, -30, 6, -58, 15, -78); c.stroke()                           # the quill
    for i in range(6):
        y0 = -12 - i * 11
        c.move_to(3 + i * 1.6, y0); c.line_to(-6 + i * 2.2, y0 - 9); c.stroke()
        c.move_to(4 + i * 1.6, y0); c.line_to(17 + i * 1.3, y0 - 8); c.stroke()
    c.restore()
    ellipse(k, 39, hy - 35, 5.2, 5.2, GOLD, seed + 71, shadow=False, lw=1.5)                  # the clip
    ellipse(k, 38, hy - 36, 1.8, 1.8, GOLD_LIGHT, seed + 72, shadow=False, outline=False)


def card(k, x, y, s=1.0, label="ROUND 1", ang=0.0, seed=90):
    """The round card: (x, y) is the middle of its bottom edge."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    cut(k, [(-84, 0), (84, 0), (84, -92), (-84, -92)], CARD, lw=2.6)
    c.set_source_rgb(*INK); c.set_line_width(2.0); c.rectangle(-77, -85, 154, 78); c.stroke()
    words = label.split(" ")
    if len(words) == 2 and len(label) <= 8:                # ROUND 1: one row, the number large
        text(k, words[0], -20, -46, 36, INK)
        text(k, words[1], 54, -46, 60, INK)
    else:                                                  # LAST ROUND: two rows
        text(k, words[0], 0, -64, 34, INK)
        text(k, " ".join(words[1:]), 0, -29, 34, INK)
    c.restore()


def _spotted(orig_builder):
    """v2: her eyes and brows redrawn over the appraising face: pupils hard aside, the brow on that side up."""
    def builder(inner, blush, sp=None):
        base = orig_builder(inner, blush, sp)

        def face(k, x, y, kind="neutral", look=(0, 0), seed=0):
            snap = cs._snap(k.c)
            base(k, x, y, kind, look, seed)
            side = -1 if look[0] < 0 else 1
            cs._cover(k, x, y, seed, snap)
            so._eyes(k, x, y, (side * 1.5, 0.05), seed, lid=-2.5)
            for sx in (-1, 1):
                if sx == side:                             # toward him: lifted
                    cs._brow(k.c, x + sx * 27, y - 28, x + sx * 8, y - 32, lift=4)
                else:                                      # the other: low and level
                    cs._brow(k.c, x + sx * 8, y - 19, x + sx * 27, y - 18, lift=1)
        return face
    return builder


def sofia(k, x, feet, s=1.0, pose="r_hips", face_kind="smile", look=(0, 0), lag=(0, 0), seed=7, lean=0.0, mouth=None,
          card_=None, card_ang=-0.13):
    """Returns {"head", "hands"} in canvas coordinates (lean not applied to the returned points)."""
    c = k.c
    spotted = face_kind == "spotted"
    if spotted:
        face_kind = "appraise"
    orig_face = so._face
    if spotted:
        so._face = lambda o_, sp: _spotted(orig_face(o_, sp))
    old = (ss.BLOUSE, ss.SKIRT, ss.TIGHTS, ss.PUMPS, ss.SWEPT[0], ss.cut, ss.rect, ss.ellipse, sf._arm, sf.RED, so.RED,
           sbc._hook, so.strand, so.pearl, so.drop)
    base_cut, base_rect, base_ell = ss.cut, ss.rect, ss.ellipse

    def cut_(k_, pts, fill, **kw):                         # her blouse and skirt are not drawn
        if fill is _SKIP[0] or fill is _SKIP[1]:
            return
        base_cut(k_, pts, fill, **kw)

    def rect_(k_, x_, y_, w_, h_, fill, seed_, **kw):      # nor the belt
        if fill is GOLD:
            return
        base_rect(k_, x_, y_, w_, h_, fill, seed_, **kw)

    def ell_(k_, cx, cy, rx, ry, fill, seed_, **kw):       # nor its buckle
        if cx == 0 and abs(cy - (BT + 101)) < 0.01:
            return
        base_ell(k_, cx, cy, rx, ry, fill, seed_, **kw)
    ss.BLOUSE, ss.SKIRT, ss.TIGHTS, ss.PUMPS = _SKIP[0], _SKIP[1], SHEER, PATENT
    ss.SWEPT[0] = True
    ss.cut, ss.rect, ss.ellipse = cut_, rect_, ell_
    sf._arm, sf.RED, so.RED = _bare_arm, KEY, KEY
    sbc._hook = lambda badge: _leotard
    so.strand, so.pearl, so.drop = (lambda *a, **kw: None), (lambda *a, **kw: None), hoop
    try:
        o = so.sofia(k, x, feet, s, pose, face_kind, look=look, lag=lag, seed=seed, badge=True, lean=lean, mouth=mouth,
                     tablet_kind=None)
    finally:
        so._face = orig_face
        (ss.BLOUSE, ss.SKIRT, ss.TIGHTS, ss.PUMPS, ss.SWEPT[0], ss.cut, ss.rect, ss.ellipse, sf._arm, sf.RED, so.RED,
         sbc._hook, so.strand, so.pearl, so.drop) = old
    c.save(); c.translate(x, feet); c.rotate(math.radians(lean)); c.scale(s, s)
    feather(k, HY, seed)
    ellipse(k, 21, HY + 4 + 21, 2.3, 2.3, INK, seed + 73, shadow=False, outline=False)          # the beauty mark
    c.set_source_rgb(1, 1, 1); c.set_line_width(1.3); c.set_line_cap(1)                         # patent: a glint on each toe
    for sx_ in (-14, 14):
        o_ = 1 if sx_ > 0 else -1
        c.move_to(sx_ + o_ * 4, -8); c.line_to(sx_ + o_ * 8, -5); c.stroke()
    c.restore()
    (lx, ly), (rx, ry) = o["hands"]
    if card_ and pose == "r_card":                        # held high in her screen-left hand, in front of the waves
        card(k, lx - 4 * s, ly + 8 * s, s * 0.86, card_, card_ang, seed + 90)
        ellipse(k, lx, ly, 9.5 * s, 9.5 * s, so.SKIN, seed + 91, shadow=False, lw=2 * s)
    if card_ and pose == "r_side":                        # the card hanging from her screen-left hand
        card(k, lx - 34 * s, ly + 76 * s, s * 0.8, card_, 0.06, seed + 90)
        ellipse(k, lx, ly, 9.5 * s, 9.5 * s, so.SKIN, seed + 91, shadow=False, lw=2 * s)
    return o


def legs_back(k, x, feet, s=1.0, seed=7):
    """From behind, knee to floor: the seam up each calf, the patent heels. For the shot of her walking away."""
    c = k.c
    c.save(); c.translate(x, feet); c.scale(s, s)
    for sx_ in (-14, 14):
        cut(k, [(sx_ - 8.5, -100), (sx_ + 8.5, -100), (sx_ + 6, -60), (sx_ + 7.5, -42), (sx_ + 4.5, -10), (sx_ - 4.5, -10),
                (sx_ - 7.5, -42), (sx_ - 6, -60)], SHEER, shadow=False, lw=1.8)
        cut(k, [(sx_ - 7.9, -99), (sx_ + 7.9, -99), (sx_ + 7.5, -92), (sx_ - 7.5, -92)], WELT, shadow=False, outline=False)
        c.set_source_rgb(*INK); c.set_line_width(1.5); c.move_to(sx_, -92); c.line_to(sx_, -11); c.stroke()   # the seam
        cut(k, [(sx_ - 5.5, -13), (sx_ + 5.5, -13), (sx_ + 6, -5), (sx_ - 6, -5)], PATENT, shadow=False, lw=1.6)   # the heel cup
        cut(k, [(sx_ - 2.2, -5), (sx_ + 2.2, -5), (sx_ + 1.2, 0), (sx_ - 1.2, 0)], PATENT, shadow=False, lw=1.4)   # the stiletto
        c.set_source_rgb(1, 1, 1); c.set_line_width(0.9); c.move_to(sx_ - 3.6, -11.2); c.line_to(sx_ - 3.6, -8); c.stroke()
    c.restore()
