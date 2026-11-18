"""v5, pinned (the locked cast of sheet v5 and storyboard v1). noir2_cast.py is current.
OFFICE NOIR 2 (working title "The Shadow of Fate"): the cast of Sofia's dream, v1. Script v1, 17 Nov.
Nothing here changes an earlier module: every look is put on while the figure is drawn and taken off again.
  sofia()      Sofia as she is in The Onboarding (sofia_ob: her face, her hair, the short strand of pearls), in a belted
               trench coat with the collar up, sleeves pushed to the elbow so the bracelet and her nails show. Lips and
               nails are the first film's key red (sofia_on.HEART), the only colour that survives the noir pass.
               Poses: "n_walk" (the rolled umbrella under her arm), "n_lips" (lipstick, at the shop window), "n_tap"
               (one nail on the napkin), "n_beckon" (one nail, slowly), "n_hide" (a hand over her mouth, the roll held
               to her chest), "n_blower" (awake: what she is holding).
  shadow()     The Client with no face: his own figure (client_ob) filled black, a hat, and only what catches the
               light: the hat's rim, his collar, the gear pin, the watch, and the hand that reaches.
  bartender()  The nice macho of The Best Candidate in a white jacket and a black bow tie, one glass, one cloth.
               brow=True is the one eyebrow.
  mom_up()     Mom with her arm up. as_shadow=True: her Office Noir figure (curlers, housecoat) with a handbag, filled
               black, three big curler bumps on the crown. as_shadow=False: Mom as she is at work (mom_bc), the same
               arm, a champagne bottle in it. The two are drawn from one pose so the cut can match.
  Props: umbrella(), napkin(), coupe(), bottle(), blower(). The blueprint roll is acts_ob.roll (The Onboarding's)."""
import math
import cairo
import kit
import sofia_ob as so
import sofia_bc as sbc
import sofia_v4 as sv
import sofia_on as son
import client_ob as co
import cand_bc as cb
import mom_on as mo
import mom_bc as mb
import don_on as d
import acts_ob as ac
from kit import INK, cut, rect, ellipse

KEY = son.HEART                                            # the one red
ACCENTS = [(KEY, 1.0)]
TRENCH = (0.91, 0.87, 0.77)                               # light, so it stands off her face and off the night
TRENCH_DARK = (0.70, 0.65, 0.54)
TRENCH_EDGE = (0.52, 0.47, 0.38)
BLACK = (0.045, 0.045, 0.055)
WHITE_JACKET = (0.97, 0.97, 0.95)
WHITE_SHADE = (0.80, 0.80, 0.80)

BT, HY = so.BODY_TOP, so.HY
_UMB = so._ik(-1, -30, BT + 96)                            # the arm the umbrella is under
so.POSES.update({                                          # new names only; nothing earlier uses them
    "n_walk": _UMB + so.REST,
    "n_lips": _UMB + so._ik(1, 20, HY + 40),
    "n_tap": so.LOW + so._ik(1, 62, BT + 74),
    "n_beckon": so.LOW + so._ik(1, 27, BT + 36),
    "n_hide": so._ik(-1, -6, BT + 50) + so._ik(1, 40, BT + 10),
    "n_blower": so._ik(-1, -12, BT + 44) + so._ik(1, 12, BT + 44),
})


class _swap:
    """Module values changed for one drawing and put back."""
    def __init__(self, *items):
        self.items = items

    def __enter__(self):
        self.old = [getattr(m, n) for m, n, _ in self.items]
        for m, n, v in self.items:
            setattr(m, n, v)

    def __exit__(self, *a):
        for (m, n, _), v in zip(self.items, self.old):
            setattr(m, n, v)


# ---------------------------------------------------------------- Sofia
def _trench(k, bt, seed):
    """Drawn where her blazer is: a belted trench coat to the knee, double-breasted, the collar up."""
    c = k.c
    cut(k, [(-41, bt + 96), (41, bt + 96), (52, bt + 176), (-52, bt + 176)], TRENCH, shadow=False, lw=2.2)   # the skirt of it
    c.set_source_rgb(*TRENCH_EDGE); c.set_line_width(1.6); c.move_to(8, bt + 106); c.line_to(11, bt + 174); c.stroke()
    for sx in (-1, 1):
        cut(k, [(sx * 39, bt - 1), (sx * 13, bt - 1), (sx * 2, bt + 52), (sx * 2, bt + 100), (sx * 41, bt + 100),
                (sx * 44, bt + 40)], TRENCH, shadow=False, lw=2.2)
    cut(k, [(-2, bt + 52), (10, bt + 50), (10, bt + 100), (-2, bt + 100)], TRENCH, shadow=False, lw=1.6)      # the overlap
    for sx in (-1, 1):
        cut(k, [(sx * 13, bt - 1), (sx * 35, bt - 7), (sx * 31, bt + 34), (sx * 4, bt + 54)], TRENCH_DARK, shadow=False,
            lw=1.8)                                        # a wide lapel
        cut(k, [(sx * 13, bt + 2), (sx * 27, bt - 24), (sx * 39, bt - 6), (sx * 26, bt + 8)], TRENCH, shadow=False, lw=1.8)
    for bx, by in ((-9, 64), (15, 64), (-9, 82), (15, 82)):
        ellipse(k, bx, bt + by, 3.4, 3.4, (0.22, 0.19, 0.15), seed + 50 + bx + by, shadow=False, lw=1.2)
    rect(k, -42, bt + 93, 84, 11, TRENCH_DARK, seed + 60, shadow=False, lw=1.8)                                  # the belt
    rect(k, -3, bt + 90, 15, 17, (0.20, 0.18, 0.15), seed + 61, shadow=False, lw=1.6)
    rect(k, 1, bt + 94, 7, 9, TRENCH_DARK, seed + 62, shadow=False, lw=1.0)


def umbrella(k, x, y, s=1.0, ang=0.22, seed=300):
    """Rolled and strapped; (x, y) is where her hand holds it. The first of the film's three rolls."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    c.set_source_rgb(*INK); c.set_line_width(5); c.set_line_cap(1)
    c.move_to(0, -66); c.line_to(0, -84); c.stroke()                                         # the shaft
    c.new_path(); c.arc(-9, -84, 9, -math.pi, 0); c.stroke()                                  # the crook
    cut(k, [(-7, -66), (7, -66), (4, 74), (-4, 74)], (0.13, 0.13, 0.16), shadow=False, lw=2)
    c.set_source_rgb(0.34, 0.34, 0.38); c.set_line_width(1.4)
    for xx in (-2.5, 2.5):
        c.move_to(xx, -60); c.line_to(xx * 0.6, 70); c.stroke()
    rect(k, -8, -28, 16, 6, (0.30, 0.30, 0.34), seed, shadow=False, lw=1.2)                    # the strap
    c.set_source_rgb(0.75, 0.75, 0.78); c.set_line_width(3); c.move_to(0, 74); c.line_to(0, 88); c.stroke()
    c.restore()


def _nail_finger(k, x, y, s, ang=0.0, seed=310):
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    cut(k, [(-4.2, 2), (-4.2, -22), (0, -26), (4.2, -22), (4.2, 2)], so.SKIN, shadow=False, lw=1.8)
    c.set_source_rgb(*KEY); c.set_line_width(4.4); c.set_line_cap(1); c.move_to(0, -23); c.line_to(0, -18); c.stroke()
    c.restore()


def blower(k, x, y, s=1.0, out=0.0, ang=0.0, seed=320):
    """The party blower: out=0 rolled up tight at her chest (the third roll), out=1 unrolled and tooting."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    PAPER, STRIPE = (0.98, 0.84, 0.25), (0.16, 0.62, 0.86)
    rect(k, -30, -5, 24, 10, (0.95, 0.95, 0.92), seed, shadow=False, lw=1.6)                   # the mouthpiece
    ln = 14 + 74 * out
    cut(k, [(-6, -7), (-6 + ln, -8), (-6 + ln, 8), (-6, 7)], PAPER, shadow=False, lw=1.8)
    c.set_source_rgb(*STRIPE); c.set_line_width(3.4)
    for i in range(int(ln // 12) + 1):
        xx = -2 + i * 12
        if xx < -6 + ln - 3:
            c.move_to(xx, -6.4); c.line_to(xx + 5, 6.4); c.stroke()
    r = 15 * (1 - out) + 4                                                                     # what is still rolled
    ellipse(k, -6 + ln + r * 0.7, 0, r, r, PAPER, seed + 1, shadow=False, lw=1.8)
    c.set_source_rgb(*STRIPE); c.set_line_width(2.2)
    c.new_path(); c.arc(-6 + ln + r * 0.7, 0, r * 0.55, 0.5, 5.2); c.stroke()
    c.restore()


def sofia(k, x, feet, s=1.0, pose="n_walk", face="interested", look=(-0.8, 0.0), mouth=None, lean=0.0, umbrella_=None,
          roll=False, blow=None, lipstick=False, coat=True, seed=7):
    """Returns {"head", "hands"}. coat=False is Sofia as she is at the party (her own blazer, in colour)."""
    items = [(sv, "RED", KEY), (so, "RED", KEY)]
    if coat:
        items += [(sbc, "_blazer", _trench), (sbc, "BLAZER", TRENCH), (sbc, "BLAZER_EDGE", TRENCH_EDGE)]
    with _swap(*items):
        o = so.sofia(k, x, feet, s, pose, face, look=look, badge=False, tablet_kind=None, lean=lean, mouth=mouth, seed=seed)
    (lx, ly), (rx, ry) = o["hands"]
    c = k.c
    if umbrella_ if umbrella_ is not None else pose in ("n_walk", "n_lips"):
        umbrella(k, lx + 2 * s, ly - 4 * s, s, 0.24)
        ellipse(k, lx, ly, 8.5 * s, 8.5 * s, so.SKIN, seed + 330, shadow=False, lw=1.8 * s)
    if lipstick or pose == "n_lips":
        c.save(); c.translate(rx - 4 * s, ry - 6 * s); c.rotate(-0.5); c.scale(s, s)
        rect(k, -3.4, -2, 6.8, 15, (0.12, 0.12, 0.14), seed + 331, shadow=False, lw=1.3)
        cut(k, [(-2.6, -2), (-2.6, -9), (2.6, -12), (2.6, -2)], KEY, shadow=False, lw=1.1)
        c.restore()
    if pose in ("n_tap", "n_beckon"):
        _nail_finger(k, rx - 1 * s, ry - 5 * s, s, -0.5 if pose == "n_tap" else 0.15, seed + 332)
    if roll or pose == "n_hide":
        ac.roll(k, lx + 10 * s, ly - 2 * s, s * 0.62, 0.55, ln=150)
        ellipse(k, lx, ly, 8.5 * s, 8.5 * s, so.SKIN, seed + 333, shadow=False, lw=1.8 * s)
    if pose == "n_hide":                                   # her hand over her mouth: four fingers across it, the nails red
        hx, hy = o["head"]
        c.save(); c.translate(hx + 2 * s, hy + 33 * s); c.rotate(-0.16); c.scale(s, s)
        ellipse(k, 17, 1, 13, 14, so.SKIN, seed + 340, shadow=False, lw=1.7)                  # the back of her hand
        for i, fy in enumerate((-9.6, -3.4, 2.8, 9.0)):
            c.save(); c.translate(-4, fy); c.rotate(0.05 * (i - 1.5))
            ellipse(k, 0, 0, 15, 3.5, so.SKIN, seed + 341 + i, shadow=False, lw=1.5)
            c.set_source_rgb(*KEY); c.set_line_width(3.4); c.set_line_cap(1); c.move_to(-13, 0); c.line_to(-9.5, 0); c.stroke()
            c.restore()
        c.restore()
    if blow is not None or pose == "n_blower":
        blower(k, (lx + rx) / 2 + 6 * s, (ly + ry) / 2 - 2 * s, s * 0.85, out=blow or 0.0, ang=-0.12)
        for hx_, hy_ in ((lx, ly), (rx, ry)):
            ellipse(k, hx_, hy_ + 3 * s, 8.5 * s, 8.5 * s, so.SKIN, seed + 334 + int(hx_), shadow=False, lw=1.8 * s)
    return o


# ---------------------------------------------------------------- the Shadow
def shadow(k, x, feet, s=1.0, pose="open", hat_tilt=-0.10, lit_hand=1, look_down=0.0, seed=400):
    """The Client as a shadow with a hat. pose: a client_ob pose name or four angles. lit_hand: 1 = his screen-right
    hand catches the light (the one that reaches), 0 = the other, None = neither. Returns {"head", "hands"}."""
    c = k.c
    c.push_group()
    o = co.client(k, x, feet, s, pose, "plain", look=(0, 0), roll=False, badge=False)
    body = c.pop_group()
    c.set_source_rgb(*BLACK); c.mask(body)
    hx, hy = o["head"]
    with _swap((d, "FEDORA", BLACK), (d, "FEDORA_BAND", (0.16, 0.16, 0.18)), (d, "FEDORA_RIM", True)):
        d.fedora(k, hx + 2 * s * look_down, hy - 38 * s + 5 * s * look_down, 1.28 * s, hat_tilt + 0.10 * look_down, seed)
    bt = co.BT
    c.save(); c.translate(x, feet); c.scale(s, s)
    c.set_source_rgb(0.70, 0.70, 0.72); c.set_line_width(2.0); c.set_line_cap(1)             # the collar's edge
    for sx in (-1, 1):
        c.move_to(sx * 32, bt - 12); c.line_to(sx * 56, bt - 17); c.line_to(sx * 54, bt + 12); c.stroke()
    c.set_source_rgb(0.92, 0.92, 0.90)                                                        # the pin: four short rays
    for a in range(4):
        c.save(); c.translate(-44, bt + 20); c.rotate(a * math.pi / 4); c.set_line_width(1.6)
        c.move_to(-6, 0); c.line_to(6, 0); c.stroke(); c.restore()
    c.restore()
    if lit_hand is not None:
        wx, wy = o["hands"][lit_hand]
        ellipse(k, wx, wy, co.HAND * s, co.HAND * s, co.SKIN, seed + 3, shadow=False, lw=2 * s)
        sd = 1 if lit_hand else -1
        ellipse(k, wx - sd * 20 * s, wy - 14 * s, 8.5 * s, 8.5 * s, (0.20, 0.20, 0.22), seed + 4, shadow=False, lw=1.8 * s)   # the watch
        ellipse(k, wx - sd * 20 * s, wy - 14 * s, 4.6 * s, 4.6 * s, (0.92, 0.92, 0.88), seed + 5, shadow=False, lw=1.0 * s)
    return o


# ---------------------------------------------------------------- the Bartender
def bartender(k, x, feet, s=1.0, brow=False, look=(-0.6, 0.0), seed=700):
    """One glass, held up in front of him, and the cloth in his other hand. brow=True: one eyebrow, and nothing else."""
    with _swap((cb, "M_SHIRT", WHITE_JACKET), (cb, "M_SHIRT_DARK", WHITE_SHADE), (cb, "M_JEANS", (0.10, 0.10, 0.12)),
               (cb, "M_JEANS_DARK", (0.05, 0.05, 0.06)), (cb, "M_BELT", (0.08, 0.08, 0.09))):
        o = cb.macho(k, x, feet, s, "pinch_near", "plain", look=look, badge=False, seed=seed)
    c = k.c
    c.save(); c.translate(x, feet); c.scale(s, s)
    by = cb.M_BT + 6                                                                           # the bow tie
    for sx in (-1, 1):
        cut(k, [(0, by), (sx * 15, by - 8), (sx * 15, by + 8)], (0.07, 0.07, 0.08), shadow=False, lw=1.6)
    ellipse(k, 0, by, 3.6, 4.4, (0.07, 0.07, 0.08), seed + 40, shadow=False, lw=1.2)
    c.restore()
    hx, hy = o["head"]
    if brow:                                                                                   # his screen-right brow, up
        c.save(); c.translate(hx, hy); c.scale(s, s)
        ellipse(k, 20, BROW_Y, 15, 6.5, cb.M_SKIN, seed + 41, shadow=False, outline=False)
        c.set_source_rgb(*cb.M_HAIR); c.set_line_width(5.6); c.set_line_cap(1)
        c.move_to(9, BROW_Y - 7); c.curve_to(16, BROW_Y - 15, 26, BROW_Y - 14, 32, BROW_Y - 8); c.stroke()
        c.restore()
    (lx, ly), (rx, ry) = o["hands"]
    c.save(); c.translate(rx + 2 * s, ry - 16 * s); c.scale(s, s)                              # the glass
    c.set_source_rgba(0.90, 0.95, 1.0, 0.55); c.rectangle(-13, -24, 26, 42); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(1.8); c.rectangle(-13, -24, 26, 42); c.stroke()
    c.set_source_rgba(1, 1, 1, 0.85); c.set_line_width(2.2); c.move_to(-8, -18); c.line_to(-8, 8); c.stroke()
    c.restore()
    cut(k, [(lx - 15 * s, ly - 10 * s), (lx + 13 * s, ly - 14 * s), (lx + 17 * s, ly + 26 * s), (lx - 3 * s, ly + 34 * s),
            (lx - 19 * s, ly + 18 * s)], (0.94, 0.94, 0.92), shadow=False, lw=1.8 * s)        # the cloth
    return o


BROW_Y = -17                                               # his brows, above the middle of his head (set by eye on the sheet)


# ---------------------------------------------------------------- Mom
UP = (-142, mo.BT - 26)                                    # her hand, out toward him (he is always screen left) and up
AIM = math.atan2(-56, -100)                                # the line from her shoulder through her hand
mo.POSES["_up"] = mo.ik(-1, UP[0], UP[1]) + mo.ik(1, 46, mo.SASH + 6)
mb.POSES["_up"] = mo.ik(-1, UP[0], UP[1]) + mo.ik(1, 46, mb.WAIST + 4)


def bottle(k, x, y, s=1.0, ang=0.0, popped=True, seed=500):
    """Champagne; (x, y) is the hand on its body, the neck up. popped: the foil torn, a wisp at the mouth."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    G = (0.10, 0.30, 0.20)
    cut(k, [(-13, 26), (-13, -18), (-6, -34), (-5, -62), (5, -62), (6, -34), (13, -18), (13, 26)], G, shadow=False, lw=2)
    rect(k, -6.5, -62, 13, 20, (0.86, 0.70, 0.26), seed, shadow=False, lw=1.4)                 # the foil
    rect(k, -11, -8, 22, 20, (0.96, 0.94, 0.88), seed + 1, shadow=False, lw=1.3)               # the label
    if popped:
        c.set_source_rgba(1, 1, 1, 0.75); c.set_line_width(3.2); c.set_line_cap(1)
        c.move_to(0, -66); c.curve_to(-9, -78, 9, -88, -2, -102); c.stroke()
    c.restore()


def handbag(k, x, y, s=1.0, seed=510):
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    c.set_source_rgb(*INK); c.set_line_width(3); c.new_path(); c.arc(0, 2, 13, math.pi, 0); c.stroke()
    cut(k, [(-21, 2), (21, 2), (25, 34), (-25, 34)], (0.30, 0.20, 0.16), shadow=False, lw=2)
    ellipse(k, 0, 6, 3.4, 3.4, (0.86, 0.70, 0.26), seed, shadow=False, lw=1.1)
    c.restore()


def mom_up(k, x, feet, s=1.0, as_shadow=True, seed=70):
    """Mom, her arm out toward him and up. One pose for the shadow on the wall and for the woman with the bottle:
    in the shadow the thing in her hand is only long and dark, along her arm; in colour it is a champagne bottle,
    its mouth toward him, the cork gone."""
    c = k.c
    tilt = AIM + math.pi / 2                               # the bottle's neck continues the arm
    if as_shadow:
        c.push_group()
        o = mo.mom(k, x, feet, s, pose="_up", face="shout", look=(-0.8, 0.0), seed=seed)
        (lx, ly), (rx, ry) = o["hands"]
        handbag(k, rx, ry + 4 * s, s)
        c.save(); c.translate(lx, ly); c.rotate(tilt); c.scale(s, s)
        cut(k, [(-12, 22), (-12, -20), (-6, -34), (-5, -60), (5, -60), (6, -34), (12, -20), (12, 22)], BLACK, shadow=False, lw=2)
        c.restore()
        c.save(); c.translate(x, feet); c.scale(s, s)      # the outline that is hers: three big curlers on the crown
        top = mo.HY - 58
        for bx, by, r in ((-44, top + 6, 17), (0, top - 12, 19), (44, top + 6, 17)):
            c.new_path(); c.arc(bx, by, r, 0, 2 * math.pi); c.set_source_rgb(0, 0, 0); c.fill()
        c.restore()
        fig = c.pop_group()
        c.set_source_rgb(*BLACK); c.mask(fig)
        return o
    o = mb.mom(k, x, feet, s, pose="_up", face="sweet", look=(-0.8, 0.0), seed=seed, bag=None)
    (lx, ly), (rx, ry) = o["hands"]
    handbag(k, rx, ry + 4 * s, s)
    bottle(k, lx, ly, s, tilt, popped=True)
    ellipse(k, lx, ly, 9 * s, 9 * s, mo.SKIN, seed + 20, shadow=False, lw=1.8 * s)
    return o


# ---------------------------------------------------------------- props
def napkin(k, x, y, s=1.0, back=False, ang=-0.06, seed=600):
    """His note: ten small boxes in two rows and a question mark. back=True: her answer in lipstick."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    rect(k, -62, -46, 124, 92, (0.97, 0.96, 0.93), seed, lw=1.8)
    c.set_source_rgb(0.86, 0.85, 0.82); c.set_line_width(1.0)
    c.rectangle(-56, -40, 112, 80); c.stroke()                                                # the embossed edge
    if not back:
        c.set_source_rgb(*INK); c.set_line_width(2.2); c.set_line_join(1)
        for r in range(2):
            for i in range(5):
                c.rectangle(-52 + i * 17, -28 + r * 26, 13, 17); c.stroke()
        c.select_font_face("Inter", 0, 1); c.set_font_size(44); c.move_to(34, 18); c.show_text("?")
    else:
        c.set_source_rgb(*KEY); c.set_line_cap(1); c.set_line_join(1)
        c.save(); c.translate(-30, -14); c.rotate(-0.62)                                       # the telephone, as on her CV
        c.set_line_width(6.0); c.arc(0, 12, 20, math.pi * 1.20, math.pi * 1.80); c.stroke()
        for sx in (-1, 1):
            c.save(); c.translate(sx * 16, 1.5); c.rotate(sx * 0.55); c.set_line_width(8.6)
            c.move_to(-3, 2.5); c.line_to(3, 2.5); c.stroke(); c.restore()
        c.restore()
        c.select_font_face("Permanent Marker", 0, 0); c.set_font_size(23); c.move_to(-50, 30); c.show_text("555 0142")
    c.restore()


def coupe(k, x, y, s=1.0, seed=620):
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    c.set_source_rgb(*INK); c.set_line_width(2.4); c.set_line_cap(1)
    c.move_to(0, 0); c.line_to(0, -30); c.stroke()
    c.new_path(); c.save(); c.translate(0, 0); c.scale(13, 3.4); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.stroke()
    c.new_path(); c.move_to(-22, -52); c.curve_to(-20, -34, 20, -34, 22, -52); c.close_path()
    c.set_source_rgba(0.96, 0.93, 0.78, 0.9); c.fill_preserve(); c.set_source_rgb(*INK); c.stroke()
    c.set_source_rgba(1, 1, 1, 0.9)
    for bx, by in ((-8, -46), (3, -42), (10, -48)):
        c.new_path(); c.arc(bx, by, 1.6, 0, 2 * math.pi); c.fill()
    c.restore()


def paper_hat(k, x, y, s=1.0, ang=0.0, seed=640):
    """A party hat; (x, y) is the middle of its rim. Never red: red is hers."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    cut(k, [(-22, 0), (0, -52), (22, 0)], (0.98, 0.84, 0.25), shadow=False, lw=2)
    c.set_source_rgb(0.16, 0.62, 0.86); c.set_line_width(4)
    c.save(); c.new_path(); c.move_to(-22, 0); c.line_to(0, -52); c.line_to(22, 0); c.close_path(); c.clip()
    for i in range(-2, 5):
        c.move_to(-30, -8 - i * 14); c.line_to(30, -20 - i * 14); c.stroke()
    c.restore()
    ellipse(k, 0, -54, 6, 6, (0.95, 0.95, 0.92), seed, shadow=False, lw=1.4)
    c.restore()


# ======================================================================================================================
# v2 (17 Nov, concept v4 and script v2). noir2_cast_v1.py = v1, pinned. Everything above is unchanged; these are new names.
#   star()       Sofia in the dream: a strapless red gown, long red gloves, diamond drops, no pearls, a black wrap worn
#                low on her elbows, a tube clutch. Poses "g_*". run=True: the hem gathered in both hands, a stride.
#   star_back()  the same figure from behind (new drawing: hair, bare shoulders, gloves, the wrap across her back).
#   party()      awake: a plain red party dress with sleeves, her pearls, sugar on one cheek.
#   detective()  Don in his Office Noir hat and coat with a magnifying glass; wrap=True: her wrap over his arm.
#   sweeper()    Pam in her Office Noir look with a flat cap, a broom and a dustpan.
#   beggar()     the robot with a tin cup and a card; reach=True: its arm out with her coin and the tag.
#   Props: clutch, compact2, wrap_flying, magnifier, glass_view, broom, dustpan, cup, coin_tag, rich_hand, taxi, bays,
#          napkin2 (the ten bays with the L-shaped corner), plan_open2, stamp_page, doughnut, footprints, powder_puff.
import sofia_ss as ss
import props_ss
import pam_on as pn
import robot_on as rn

LOOK = [2]                                                 # opt-in: 3 = cast sheet v3 (17 Nov, after the design audit): the wrap at
#                                                            her elbows with a pale edge, the long gown in the run, the L-shaped
#                                                            bay filled, grey banknotes with numerals, Pam's apron, Don's rim
#                                                            light. 2 draws exactly as cast sheet v2 (noir2_cast_v2.py, pinned).
#                                                            4 = cast sheet v4: her hair from behind is as long as from the front,
#                                                            the wrap is one soft piece of cloth, her gloved hand has a palm, a
#                                                            thumb and a finger that curls, her shoulders slope. 3 = sheet v3.
#                                                            5 = the locked cast (17 Nov): the wrap's two front ends are half as
#                                                            long and rounded, close to her forearms. 4 = sheet v4.
WRAP_PALE = (0.80, 0.80, 0.84)
GOWN_SHADE = (0.60, 0.07, 0.11)                            # folds; kept by the noir pass with the key red
ACCENTS2 = [(KEY, 1.0), (GOWN_SHADE, 1.0)]
DIAMOND = (0.97, 0.98, 1.0)
DIAMOND_SHADE = (0.66, 0.74, 0.86)
WRAP = (0.07, 0.07, 0.09)
WRAP_EDGE = (0.42, 0.42, 0.46)
SILVER = (0.84, 0.85, 0.88)
SILVER_DARK = (0.50, 0.52, 0.58)
NOTE = (0.90, 0.93, 0.86)

so.POSES.update({                                          # new names only
    "g_stand": _UMB + so.REST,                             # the clutch under her arm
    "g_pose": _UMB + so._ik(1, 36, BT + 96),               # out of the taxi: a hand on her hip
    "g_mirror": _UMB + so._ik(1, 30, HY + 50),             # the compact held up
    "g_run": so._ik(-1, -36, BT + 116) + so._ik(1, 36, BT + 116),
    "g_fan": _UMB + so._ik(1, 6, HY + 80),                 # somebody's banknotes in front of her mouth; her eyes over them
    "g_count": so.LOW + so._ik(1, 62, BT + 74),
    "g_beckon": so.LOW + so._ik(1, 27, BT + 36),
    "g_hide": so._ik(-1, -6, BT + 50) + so._ik(1, 40, BT + 10),
    "g_blower": so._ik(-1, -12, BT + 44) + so._ik(1, 12, BT + 44),
    "g_run3": so._ik(-1, -50, BT + 52) + so._ik(1, 58, BT + 84),     # v3: arms pumping, the gown left alone
    "g_beckon3": so.LOW + so._ik(1, 44, HY + 66),                    # v3: the finger up beside her chin
    "g_offer": so._ik(-1, -74, BT + 58) + so.REST,                   # v3: her hand held out to him, and left in the air
    "g_down": so.LOW + so.REST,                                      # v4: both arms down
    "g_drop": so.LOW + so._ik(1, 72, BT + 62),                       # the board: a coin let go, without looking
})


def _seg(k, ax, ay, bx, by, w0, w1, col, lw=2.0):
    g = math.atan2(by - ay, bx - ax)
    nx, ny = -math.sin(g), math.cos(g)
    cut(k, [(ax + nx * w0 / 2, ay + ny * w0 / 2), (bx + nx * w1 / 2, by + ny * w1 / 2), (bx - nx * w1 / 2, by - ny * w1 / 2),
            (ax - nx * w0 / 2, ay - ny * w0 / 2)], col, shadow=False, lw=lw)


def _glove_arm(k, sx, sy, a1, a2, seed, ln=48, w=17):
    """A bare upper arm, and a glove from above the elbow to the fingertips."""
    dd = lambda a: (math.sin(math.radians(a)), math.cos(math.radians(a)))
    ex, ey = sx + dd(a1)[0] * ln, sy + dd(a1)[1] * ln
    hx, hy = ex + dd(a1 + a2)[0] * ln, ey + dd(a1 + a2)[1] * ln
    _seg(k, sx, sy, ex, ey, w, w, so.SKIN)
    gx, gy = sx + (ex - sx) * 0.46, sy + (ey - sy) * 0.46
    _seg(k, gx, gy, ex, ey, w + 3, w + 1, KEY)                                                  # the glove's top
    _seg(k, ex, ey, hx, hy, w, w * 0.86, KEY)
    ellipse(k, ex, ey, w * 0.52, w * 0.52, KEY, seed + 2, shadow=False, outline=False)          # the elbow, closed
    ellipse(k, hx, hy, w * 0.6, w * 0.6, KEY, seed, shadow=False, lw=2)
    return hx, hy


def _glint(c, x, y, r, lw=1.4):
    c.save(); c.set_line_cap(1)
    for col, extra in ((INK, 1.6), ((1, 1, 1), 0.0)):
        c.set_source_rgb(*col); c.set_line_width(lw + extra)
        c.move_to(x - r, y); c.line_to(x + r, y); c.move_to(x, y - r); c.line_to(x, y + r); c.stroke()
    c.restore()


def diamond(k, x, y, lgx=0.0, spark=0.0, seed=0):
    """A stud and one long drop, cut like a stone; it swings with lag."""
    c = k.c
    c.save(); c.translate(x, y + 1); c.rotate(-lgx * 0.045)
    c.set_source_rgb(*INK); c.set_line_width(2.6); c.move_to(0, 2); c.line_to(0, 12); c.stroke()
    c.set_source_rgb(*DIAMOND); c.set_line_width(1.2); c.move_to(0, 2); c.line_to(0, 12); c.stroke()
    cut(k, [(0, 10), (7.5, 21), (0, 38), (-7.5, 21)], DIAMOND, shadow=False, lw=1.7)
    c.set_source_rgb(*DIAMOND_SHADE); c.set_line_width(1.1)
    c.move_to(-7.5, 21); c.line_to(7.5, 21); c.move_to(0, 10); c.line_to(-2.5, 21); c.line_to(0, 38)
    c.move_to(0, 10); c.line_to(2.5, 21); c.stroke()
    ellipse(k, 0, 0, 4.6, 4.6, DIAMOND, seed, shadow=False, lw=1.6)
    c.restore()
    _glint(c, x + (5 if x > 0 else -5), y + 16, 5.5 + 3 * spark)


def _pale_edge(c, pts, lw=1.5, closed=False):
    c.save(); c.set_source_rgb(*WRAP_PALE); c.set_line_width(lw); c.set_line_cap(1); c.set_line_join(1)
    c.new_path(); c.move_to(*pts[0])
    for q in pts[1:]:
        c.line_to(*q)
    if closed:
        c.close_path()
    c.stroke(); c.restore()


def _cloth(c, d_, fill=None, lw=2.0):
    """A smooth filled shape from a list of path commands: ("M", x, y), ("C", x1, y1, x2, y2, x, y), ("L", x, y)."""
    c.new_path()
    for cmd in d_:
        if cmd[0] == "M":
            c.move_to(cmd[1], cmd[2])
        elif cmd[0] == "L":
            c.line_to(cmd[1], cmd[2])
        else:
            c.curve_to(*cmd[1:])
    c.close_path()
    c.set_source_rgb(*(fill or WRAP)); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(lw); c.set_line_join(1); c.stroke()


def _curve(c, pts, col, lw):
    c.new_path(); c.move_to(pts[0], pts[1]); c.curve_to(*pts[2:])
    c.set_source_rgb(*col); c.set_line_width(lw); c.set_line_cap(1); c.stroke()


def _tail4(k, s, side, ln=1.0):
    """v4: one end of the wrap as cloth: it leaves the elbow, swells, and narrows to a fringed point."""
    c = k.c
    g = side
    if LOOK[0] >= 5 and ln == 1.0:                         # v5: a short rounded end, like the end of a stole
        _cloth(c, [("M", g * 1, -9), ("C", g * 15, -12, g * 20, 4, g * 19, 20), ("C", g * 19, 33, g * 13, 40, g * 8, 40),
                   ("C", g * 2, 40, g * -1, 32, g * -1, 20), ("C", g * -1, 8, g * -2, -3, g * 1, -9)])
        _curve(c, (g * 13, -3, g * 17, 8, g * 16, 24, g * 10, 35), WRAP_PALE, 1.5)
        c.set_source_rgb(*WRAP_PALE); c.set_line_width(1.3); c.set_line_cap(1)
        for fx in (3, 8, 13):
            c.move_to(g * fx, 39.5); c.line_to(g * fx, 46.5); c.stroke()
        return
    _cloth(c, [("M", g * 2, -9), ("C", g * 20, -12, g * 27, 12, g * 23, 36 * ln), ("C", g * 21, 52 * ln, g * 15, 62 * ln, g * 12, 70 * ln),
               ("C", g * 8, 56 * ln, g * 4, 42 * ln, g * 1, 22 * ln), ("C", g * -1, 10, g * -2, -2, g * 2, -9)])
    _curve(c, (g * 17, -2, g * 22, 14, g * 20, 38 * ln, g * 14, 58 * ln), WRAP_PALE, 1.5)
    c.set_source_rgb(*WRAP_PALE); c.set_line_width(1.3); c.set_line_cap(1)
    for fx, fy in ((10, 68), (13, 72), (16, 66)):
        c.move_to(g * fx, fy * ln); c.line_to(g * (fx + 1), (fy + 9) * ln); c.stroke()


def hand(k, x, y, s=1.0, ang=0.0, curl=0.0, flip=1, seed=336):
    """v4: her gloved hand with one finger out. (x, y) is the wrist end of the palm; ang turns the whole hand (0 = the
    finger straight up). curl 0..1: the index finger straight, then curling back toward the palm: the beckon.
    flip=-1 mirrors it."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s * flip, s)
    ellipse(k, 0, -9, 11.5, 11, KEY, seed, shadow=False, lw=1.9)                                  # the palm
    for i, (fx, fy) in enumerate(((2.5, -19.5), (8.0, -17.0), (11.5, -11.5))):                    # three fingers, folded
        ellipse(k, fx, fy, 4.6, 4.2, KEY, seed + 1 + i, shadow=False, lw=1.6)
    c.save(); c.translate(-10.5, -6); c.rotate(-0.75)                                            # the thumb
    ellipse(k, 0, -5, 4.2, 8.5, KEY, seed + 5, shadow=False, lw=1.7)
    c.restore()
    c.save(); c.translate(-5.5, -17)                                                             # the index finger
    c.rotate(-0.10 + 0.25 * curl)
    cut(k, [(-4, 2), (-4, -15), (4, -15), (4, 2)], KEY, shadow=False, lw=1.7)
    c.translate(0, -15); c.rotate(1.9 * curl)
    cut(k, [(-3.8, 2), (-3.8, -11), (0, -15), (3.8, -11), (3.8, 2)], KEY, shadow=False, lw=1.7)
    ellipse(k, 0, 1, 3.9, 3.9, KEY, seed + 6, shadow=False, outline=False)                        # the knuckle, closed
    c.restore()
    c.set_source_rgb(*GOWN_SHADE); c.set_line_width(1.3); c.set_line_cap(1)
    c.move_to(-4, -4); c.curve_to(0, -1, 5, -2, 8, -6); c.stroke()
    c.restore()


def _gown_run(k, bt, seed):
    """v3: the same gown, running to screen right: the hem streams behind her, one leg comes through the slit."""
    c = k.c
    body = [(-41, bt + 30), (-22, bt + 23), (0, bt + 35), (22, bt + 23), (41, bt + 30), (42, bt + 46), (30, bt + 100),
            (45, bt + 134), (38, -62), (36, 0), (-34, -1), (-78, -8), (-116, -30), (-92, -40), (-64, -58), (-45, bt + 134),
            (-30, bt + 100), (-42, bt + 46)]
    cut(k, body, KEY, lw=2.2)
    c.set_source_rgb(*GOWN_SHADE); c.set_line_width(2.0); c.set_line_cap(1)
    c.arc(-19, bt + 38, 15, 0.15 * math.pi, 0.82 * math.pi); c.stroke()
    c.arc(19, bt + 38, 15, 0.18 * math.pi, 0.85 * math.pi); c.stroke()
    for i, (x0, x1) in enumerate(((-28, 26), (-27, 20), (-24, 26))):
        c.move_to(x0, bt + 84 + i * 8); c.curve_to(x0 + 16, bt + 90 + i * 8, x1 - 16, bt + 80 + i * 8, x1, bt + 86 + i * 8); c.stroke()
    for (x0, y0, x1, y1, x2, y2) in ((-30, bt + 130, -50, -60, -100, -30), (-8, bt + 136, -30, -50, -70, -10),
                                     (14, bt + 140, 4, -50, -24, -4)):
        c.move_to(x0, y0); c.curve_to(x0, (y0 + y1) / 2, x1, y1, x2, y2); c.stroke()
    _seg(k, 26, -98, 58, -58, 18, 14, so.SKIN)                                                  # her thigh, through the slit
    _seg(k, 58, -58, 54, -16, 13, 9, so.SKIN)
    ellipse(k, 58, -58, 7.5, 7.5, so.SKIN, seed + 3, shadow=False, outline=False)
    cut(k, [(47, -17), (61, -17), (78, -2), (78, 0), (60, 0), (56, -6), (52, 0), (47, 0)], KEY, shadow=False, lw=1.8)
    cut(k, [(24, bt + 138), (40, bt + 134), (38, -62), (30, -86)], KEY, shadow=False, lw=2)       # the slit's edge, over her thigh
    c.save(); c.translate(-96, -58); c.rotate(-0.9)                                              # her other shoe, kicked up behind
    cut(k, [(-8, -6), (8, -6), (14, 4), (-4, 4), (-8, 10), (-11, 4)], KEY, shadow=False, lw=1.6)
    c.restore()


def _gown(k, bt, seed, hem=-11.0, lift=False, wrap=True, run=False):
    c = k.c
    if wrap and LOOK[0] >= 4:                              # v4: one soft swag behind her, from elbow to elbow
        _cloth(c, [("M", -66, bt + 52), ("C", -52, bt + 118, 52, bt + 118, 66, bt + 52), ("L", 74, bt + 66),
                   ("C", 58, bt + 146, -58, bt + 146, -74, bt + 66)])
        _curve(c, (-70, bt + 70, -54, bt + 138, 54, bt + 138, 70, bt + 70), WRAP_PALE, 1.5)
    elif wrap and LOOK[0] >= 3:                            # v3: the wrap hangs behind her, from elbow to elbow
        sw = [(-70, bt + 52), (70, bt + 52), (72, bt + 78), (44, bt + 112), (-44, bt + 112), (-72, bt + 78)]
        cut(k, sw, WRAP, shadow=False, lw=2)
        _pale_edge(c, [(-68, bt + 78), (-44, bt + 108), (44, bt + 108), (68, bt + 78)])
    if LOOK[0] >= 4:                                       # v4: shoulders that slope, so the skin does not read as a collar
        c.set_source_rgb(*ss.HAIR_SHADE); c.rectangle(-42, bt - 4, 84, 16); c.fill()               # her hair, behind her neck
        cut(k, [(-16, bt - 5), (16, bt - 5), (41, bt + 9), (43, bt + 40), (-43, bt + 40), (-41, bt + 9)], so.SKIN, shadow=False, lw=2)
    else:
        cut(k, [(-40, bt - 1), (40, bt - 1), (43, bt + 40), (-43, bt + 40)], so.SKIN, shadow=False, lw=2)   # bare shoulders
    c.set_source_rgb(0.80, 0.56, 0.43); c.set_line_width(1.6); c.set_line_cap(1)
    for sx in (-1, 1):                                     # the collarbones
        if LOOK[0] >= 4:
            c.move_to(sx * 7, bt + 15); c.line_to(sx * 27, bt + 12); c.stroke()
        else:
            c.move_to(sx * 8, bt + 9); c.line_to(sx * 30, bt + 5); c.stroke()
    if run:
        return _gown_run(k, bt, seed)
    if lift:                                               # gathered up in her fists: the hem at her knees
        body = [(-41, bt + 30), (-22, bt + 23), (0, bt + 35), (22, bt + 23), (41, bt + 30), (42, bt + 46), (30, bt + 100),
                (46, bt + 132), (58, -70), (30, -52), (0, -62), (-30, -52), (-58, -70), (-46, bt + 132), (-30, bt + 100),
                (-42, bt + 46)]
    else:
        body = [(-41, bt + 30), (-22, bt + 23), (0, bt + 35), (22, bt + 23), (41, bt + 30), (42, bt + 46), (30, bt + 100),
                (45, bt + 134), (38, -58), (56, hem), (-56, hem), (-38, -58), (-45, bt + 134), (-30, bt + 100), (-42, bt + 46)]
    cut(k, body, KEY, lw=2.2)
    c.set_source_rgb(*GOWN_SHADE); c.set_line_width(2.0); c.set_line_cap(1)
    c.arc(-19, bt + 38, 15, 0.15 * math.pi, 0.82 * math.pi); c.stroke()
    c.arc(19, bt + 38, 15, 0.18 * math.pi, 0.85 * math.pi); c.stroke()
    for i, (x0, x1) in enumerate(((-28, 26), (-27, 20), (-24, 26))):                            # ruching at the waist
        c.move_to(x0, bt + 84 + i * 8); c.curve_to(x0 + 16, bt + 90 + i * 8, x1 - 16, bt + 80 + i * 8, x1, bt + 86 + i * 8); c.stroke()
    if lift:
        for x0, x1 in ((-36, -50), (36, 50), (-14, -22), (14, 22)):
            c.move_to(x0, bt + 124); c.line_to(x1, -64 if abs(x0) > 20 else -58); c.stroke()
    else:
        c.move_to(-12, bt + 128); c.curve_to(-20, -90, -30, -50, -44, hem - 3); c.stroke()
        c.move_to(20, bt + 140); c.curve_to(22, -80, 30, -40, 40, hem - 3); c.stroke()
        c.set_source_rgb(*INK); c.set_line_width(1.8)                                           # the slit
        c.move_to(10, bt + 150); c.line_to(18, hem); c.stroke()


def clutch(k, x, y, s=1.0, ang=0.0, seed=660):
    """Her evening bag: a short silver tube. The first of the three rolls."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    rect(k, -24, -8, 48, 16, SILVER, seed, shadow=False, lw=1.8)
    for ex in (-24, 24):
        ellipse(k, ex, 0, 4.2, 8, SILVER if ex < 0 else (0.96, 0.96, 0.98), seed + 1 + ex, shadow=False, lw=1.6)
    c.set_source_rgb(*SILVER_DARK); c.set_line_width(1.2)
    for lx in (-10, 0, 10):
        c.move_to(lx, -7); c.line_to(lx, 7); c.stroke()
    ellipse(k, 0, -8, 3.2, 2.4, (0.98, 0.98, 1.0), seed + 5, shadow=False, lw=1.2)                # the clasp
    c.restore()


def compact2(k, x, y, s=1.0, ang=0.0, hat=False, seed=670):
    """Her compact, open, the mirror toward us. hat=True: the hat in it, over her shoulder."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    ellipse(k, 0, 17, 17, 14, SILVER, seed + 1, shadow=False, lw=1.8)
    ellipse(k, 0, 17, 12, 9.5, (0.95, 0.90, 0.86), seed + 2, shadow=False, lw=1.2)               # the powder
    ellipse(k, 0, -17, 19, 19, SILVER, seed + 3, shadow=False, lw=2)
    ellipse(k, 0, -17, 15, 15, (0.74, 0.80, 0.86), seed + 4, shadow=False, lw=1.4)               # the mirror
    if hat:
        c.save(); c.new_path(); c.arc(0, -17, 14, 0, 2 * math.pi); c.clip()
        c.set_source_rgb(*BLACK)
        c.new_path(); c.move_to(-6, -6); c.line_to(13, -6); c.line_to(11, -19); c.line_to(7, -22); c.line_to(3, -20); c.line_to(-1, -22)
        c.line_to(-4, -19); c.close_path(); c.fill()
        c.save(); c.translate(4, -12); c.scale(13, 2.6); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
        c.rectangle(-4, -10, 16, 12); c.fill()
        c.restore()
    c.set_source_rgba(1, 1, 1, 0.85); c.set_line_width(2.2); c.set_line_cap(1); c.move_to(-10, -24); c.line_to(-5, -29); c.stroke()
    c.restore()


def _drape(k, ex, ey, s, seed, side=1, sh=None):
    """One end of the wrap: along the upper arm from below the shoulder (sh) to the elbow, and a tail hanging from the
    elbow on the outside. (ex, ey) is the elbow, in canvas units."""
    c = k.c
    if sh is not None:
        ax, ay = sh[0] + (ex - sh[0]) * 0.34, sh[1] + (ey - sh[1]) * 0.34
        _seg(k, ax, ay, ex, ey, 23 * s, 22 * s, WRAP)
        c.set_source_rgb(*WRAP_EDGE); c.set_line_width(1.3 * s); c.set_line_cap(1)
        c.move_to(ax + side * 5 * s, ay + 2 * s); c.line_to(ex + side * 5 * s, ey - 2 * s); c.stroke()
    c.save(); c.translate(ex + side * 6 * s, ey); c.scale(s, s)
    cut(k, [(-8, -8), (8, -8), (9, 36), (side * 3, 46), (-8, 38)], WRAP, shadow=False, lw=2)
    c.set_source_rgb(*WRAP_EDGE); c.set_line_width(1.3); c.set_line_cap(1)
    c.move_to(0, -2); c.line_to(1, 34); c.stroke()
    for fx in (-6, 0, 6):                                                                     # the fringe
        c.move_to(fx, 40 + (4 if fx == 0 else 0)); c.line_to(fx + 1, 49 + (4 if fx == 0 else 0)); c.stroke()
    c.restore()


def _drape3(k, ex, ey, s, seed, side=1):
    """v3: one end of the wrap, over the crook of an elbow and down the outside of her arm. The glove stays in sight."""
    c = k.c
    c.save(); c.translate(ex, ey); c.scale(s, s)
    if LOOK[0] >= 4:                                       # v4: cloth, not a frame
        _cloth(c, [("M", -13, -6), ("C", -6, -11, 6, -11, 13, -6), ("C", 15, 0, 14, 5, 12, 8), ("C", 5, 4, -5, 4, -12, 8),
                   ("C", -14, 5, -15, 0, -13, -6)])
        _curve(c, (-10, 3, -4, -1, 4, -1, 10, 3), WRAP_PALE, 1.3)
        c.translate(side * 8, 2)
        _tail4(k, s, side)
        c.restore()
        return
    band = [(-12, -8), (12, -8), (12, 6), (-12, 6)]
    cut(k, band, WRAP, shadow=False, lw=2)
    tail = [(side * 6, -6), (side * 22, -6), (side * 24, 44), (side * 16, 56), (side * 7, 46)]
    cut(k, tail, WRAP, shadow=False, lw=2)
    _pale_edge(c, [(side * 9.5, -2), (side * 10.5, 42), (side * 16, 51), (side * 21, 42), (side * 19.5, -2)], 1.6)
    _pale_edge(c, [(-9, 2.5), (9, 2.5)], 1.4)
    c.set_source_rgb(*WRAP_PALE); c.set_line_width(1.3); c.set_line_cap(1)
    for fx in (9, 15, 21):                                                                    # the fringe
        c.move_to(side * fx, 50 if fx != 15 else 57); c.line_to(side * (fx + 1), 59 if fx != 15 else 66); c.stroke()
    c.restore()


def wrap_flying(k, x, y, s=1.0, ang=-0.5, seed=680):
    """The wrap, off her shoulders and in the air."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    if LOOK[0] >= 4:                                       # v4: a ribbon of cloth, turning over in the air
        _cloth(c, [("M", -76, 4), ("C", -50, -30, -16, -22, 6, -6), ("C", 26, 8, 52, -26, 80, -14), ("C", 72, -2, 66, 8, 62, 16),
                   ("C", 44, 4, 26, 30, 2, 18), ("C", -18, 8, -44, 6, -64, 22), ("C", -66, 14, -72, 10, -76, 4)])
        _curve(c, (-66, 6, -44, -18, -16, -12, 4, 2), WRAP_PALE, 1.6)
        _curve(c, (4, 2, 26, 16, 50, -14, 70, -8), WRAP_PALE, 1.6)
        c.set_source_rgb(*WRAP_PALE); c.set_line_width(1.3); c.set_line_cap(1)
        for fx, fy, dx, dy in ((-74, 8, -9, 4), (-70, 14, -9, 6), (-66, 20, -8, 8), (78, -10, 10, -2), (72, 0, 10, 2), (66, 10, 10, 5)):
            c.move_to(fx, fy); c.line_to(fx + dx, fy + dy); c.stroke()
        c.restore()
        return
    cut(k, [(-70, -6), (-30, -18), (10, -8), (48, -20), (74, -4), (60, 12), (20, 6), (-20, 16), (-62, 10)], WRAP, lw=2)
    if LOOK[0] >= 3:
        _pale_edge(c, [(-66, -3), (-30, -14), (10, -4), (48, -16), (70, -3)], 1.6)
        _pale_edge(c, [(-60, 7), (-20, 12), (20, 2), (58, 8)], 1.6)
    c.set_source_rgb(*(WRAP_PALE if LOOK[0] >= 3 else WRAP_EDGE)); c.set_line_width(1.4); c.set_line_cap(1)
    c.move_to(-56, 0); c.curve_to(-30, -10, 0, 2, 56, -8); c.stroke()
    for fx, fy in ((-70, -6), (-66, 2), (-62, 10)):
        c.move_to(fx, fy); c.line_to(fx - 11, fy + 2); c.stroke()
    for fx, fy in ((74, -4), (68, 4), (60, 12)):
        c.move_to(fx, fy); c.line_to(fx + 11, fy + 3); c.stroke()
    c.restore()


def _elbows(pose, x, feet, s):
    a = so.POSES[pose]
    dd = lambda g: (math.sin(math.radians(g)), math.cos(math.radians(g)))
    return [(x + (so.SH[i][0] + dd(a[2 * i])[0] * so.LN) * s, feet + (so.SH[i][1] + dd(a[2 * i])[1] * so.LN) * s) for i in (0, 1)]


def _glove_finger(k, x, y, s, ang=0.0, seed=310):
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    cut(k, [(-4.4, 2), (-4.4, -22), (0, -27), (4.4, -22), (4.4, 2)], KEY, shadow=False, lw=1.8)
    c.restore()


def money(k, x, y, s=1.0, ang=0.0, n=5, seed=690):
    """A fan of banknotes; (x, y) is where the fingers hold it."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    for i in range(n):
        c.save(); c.rotate((i - (n - 1) / 2.0) * 0.30)
        if LOOK[0] >= 3:                                   # v3: grey-green, a band, numerals: money, not cards
            rect(k, -13, -56, 26, 50, (0.66, 0.74, 0.62), seed + i, shadow=False, lw=1.5)
            c.set_source_rgb(0.30, 0.38, 0.30); c.set_line_width(1.2); c.rectangle(-9.5, -52, 19, 42); c.stroke()
            c.new_path(); c.save(); c.translate(0, -31); c.scale(5.2, 8); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
            c.set_source_rgb(0.84, 0.88, 0.80); c.fill_preserve(); c.set_source_rgb(0.30, 0.38, 0.30); c.stroke()
            c.set_source_rgb(0.16, 0.22, 0.16); c.select_font_face("Inter", 0, 1); c.set_font_size(6.2)
            c.move_to(-8.6, -45.5); c.show_text("100"); c.move_to(-2.8, -12.4); c.show_text("100")
            c.restore(); continue
        rect(k, -12, -52, 24, 46, NOTE, seed + i, shadow=False, lw=1.5)
        c.set_source_rgb(0.42, 0.50, 0.40); c.set_line_width(1.1)
        c.rectangle(-8.5, -48, 17, 38); c.stroke()
        c.new_path(); c.save(); c.translate(0, -29); c.scale(5, 7.5); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.stroke()
        c.restore()
    c.restore()


def star(k, x, feet, s=1.0, pose="g_stand", face="interested", look=(-0.8, 0.0), mouth=None, lean=0.0, lag=(0, 0),
         wrap=True, bag=None, run=False, mirror=False, fan=False, roll=False, lipstick=False, sparkle=0.0, seed=7,
         curl=0.6):
    """Sofia in the dream, v2. Returns {"head", "hands"}. bag=None: the clutch is drawn in the poses that carry it."""
    v3 = LOOK[0] >= 3
    running = v3 and (run or pose == "g_run3")
    lift = (run or pose == "g_run") and not running
    if running:
        pose = "g_run3"

    def builder(badge):
        return lambda k_, bt, seed_: _gown(k_, bt, seed_, lift=lift, wrap=wrap and not lift and not running, run=running)
    items = [(sv, "RED", KEY), (so, "RED", KEY), (sbc, "_hook", builder), (so, "strand", lambda *a, **kw: None),
             (so, "pearl", lambda *a, **kw: None), (so, "drop", diamond), (sv, "_arm", _glove_arm),
             (ss, "TIGHTS", so.SKIN), (ss, "PUMPS", KEY)]
    if lift:
        orig = ss.sofia
        items.append((ss, "sofia", lambda *a, **kw: orig(*(a[:11] + (0.23,) + a[12:]), **kw)))   # a stride
    with _swap(*items):
        o = so.sofia(k, x, feet, s, pose, face, look=look, lag=lag, badge=False, tablet_kind=None, lean=lean, mouth=mouth,
                     sparkle=sparkle, seed=seed)
    (lx, ly), (rx, ry) = o["hands"]
    c = k.c
    if wrap and v3 and not running and not lean:
        for i, (ex, ey) in enumerate(_elbows(pose, x, feet, s)):
            if ey > feet + (so.SH[i][1] + 26) * s:           # only on an arm that hangs
                _drape3(k, ex, ey, s, seed + 350 + i, side=-1 if i == 0 else 1)
    elif wrap and not lift and not lean and not running:
        for i, (ex, ey) in enumerate(_elbows(pose, x, feet, s)):
            shx, shy = x + so.SH[i][0] * s, feet + so.SH[i][1] * s
            if ey > shy + 26 * s:                           # only on an arm that hangs; a raised arm has let it slip
                _drape(k, ex, ey, s, seed + 350 + i, side=-1 if i == 0 else 1, sh=(shx, shy))
    if bag if bag is not None else pose in ("g_stand", "g_pose", "g_mirror", "g_fan"):
        clutch(k, lx + 13 * s, ly - 10 * s, s * 0.95, -0.22, seed + 360)
        ellipse(k, lx, ly, 10.2 * s, 10.2 * s, KEY, seed + 361, shadow=False, lw=2 * s)
    if mirror or pose == "g_mirror":
        compact2(k, rx + 2 * s, ry - 22 * s, s * 0.9, 0.12, hat=mirror == "hat", seed=seed + 362)
        ellipse(k, rx, ry, 10.2 * s, 10.2 * s, KEY, seed + 363, shadow=False, lw=2 * s)
    if fan or pose == "g_fan":
        money(k, rx, ry - 2 * s, s * 1.15, 0.0, 5, seed + 364)
        ellipse(k, rx, ry, 10.2 * s, 10.2 * s, KEY, seed + 365, shadow=False, lw=2 * s)
    if lipstick:
        c.save(); c.translate(rx - 4 * s, ry - 6 * s); c.rotate(-0.5); c.scale(s, s)
        rect(k, -3.4, -2, 6.8, 15, (0.12, 0.12, 0.14), seed + 331, shadow=False, lw=1.3)
        cut(k, [(-2.6, -2), (-2.6, -9), (2.6, -12), (2.6, -2)], KEY, shadow=False, lw=1.1)
        c.restore()
    if pose in ("g_count", "g_beckon"):
        _glove_finger(k, rx - 1 * s, ry - 5 * s, s, -0.5 if pose == "g_count" else 0.15, seed + 332)
    if pose == "g_beckon3" and LOOK[0] >= 4:               # v4: a hand: palm, thumb, and one finger curling toward her
        hand(k, rx, ry + 6 * s, s * 1.5, 0.12, curl, 1, seed + 336)
    elif pose == "g_beckon3":                              # the finger, large, curling toward her
        _glove_finger(k, rx - 2 * s, ry - 6 * s, s * 1.45, -0.42, seed + 332)
        ellipse(k, rx, ry, 11.5 * s, 11.5 * s, KEY, seed + 335, shadow=False, lw=2 * s)
    if roll or pose == "g_hide":
        ac.roll(k, lx + 10 * s, ly - 2 * s, s * 0.62, 0.55, ln=150)
        ellipse(k, lx, ly, 10.2 * s, 10.2 * s, KEY, seed + 333, shadow=False, lw=2 * s)
    if pose == "g_hide":                                   # her gloved hand over her mouth
        hx, hy = o["head"]
        c.save(); c.translate(hx + 2 * s, hy + 33 * s); c.rotate(-0.16); c.scale(s, s)
        ellipse(k, 17, 1, 13, 14, KEY, seed + 340, shadow=False, lw=1.7)
        for i, fy in enumerate((-9.6, -3.4, 2.8, 9.0)):
            c.save(); c.translate(-4, fy); c.rotate(0.05 * (i - 1.5))
            ellipse(k, 0, 0, 15, 3.5, KEY, seed + 341 + i, shadow=False, lw=1.5)
            c.restore()
        c.restore()
    return o


def star_back(k, x, feet, s=1.0, step=None, wrap=True, lag=(0, 0), seed=7):
    """Sofia walking away from us. step: 0..1 through a stride, None = standing."""
    c = k.c
    ph = step if step is not None else 0.0
    bob = -4 * abs(math.sin(math.pi * 2 * ph)) if step is not None else 0.0
    c.save(); c.translate(x, feet + bob); c.scale(s, s)
    bt, hy = BT, HY
    lgx, lgy = lag
    for i, sx_ in enumerate((-14, 14)):                    # her heels, from behind
        sw = math.sin(math.pi * 2 * ph + (0 if i == 0 else math.pi)) if step is not None else 0.0
        c.save(); c.translate(7 * sw, -9 * max(0.0, sw))
        cut(k, [(sx_ - 6, -40), (sx_ + 6, -40), (sx_ + 4.5, -12), (sx_ - 4.5, -12)], so.SKIN, shadow=False, lw=1.8)
        cut(k, [(sx_ - 6.5, -14), (sx_ + 6.5, -14), (sx_ + 5, -2), (sx_ + 2, -2), (sx_ + 1.5, 0), (sx_ - 1.5, 0), (sx_ - 2, -2),
                (sx_ - 5, -2)], KEY, shadow=False, lw=1.6)
        c.restore()
    sway = 5 * math.sin(math.pi * 2 * ph) if step is not None else 0.0
    cut(k, [(-42, bt + 44), (42, bt + 44), (30, bt + 100), (45, bt + 134), (38, -58), (56 + sway, -16), (-56 + sway, -16),
            (-38, -58), (-45, bt + 134), (-30, bt + 100)], KEY, lw=2.2)                           # the gown
    c.set_source_rgb(*GOWN_SHADE); c.set_line_width(2.0); c.set_line_cap(1)
    c.move_to(0, bt + 104); c.curve_to(-2, -90, 2 + sway * 0.5, -50, sway, -18); c.stroke()
    c.move_to(-26, bt + 132); c.curve_to(-30, -90, -34, -50, -46 + sway, -19); c.stroke()
    c.move_to(26, bt + 132); c.curve_to(30, -90, 34, -50, 46 + sway, -19); c.stroke()
    cut(k, [(-40, bt - 1), (40, bt - 1), (43, bt + 46), (-43, bt + 46)], so.SKIN, shadow=False, lw=2)       # her bare back
    c.set_source_rgb(0.80, 0.56, 0.43); c.set_line_width(1.6); c.move_to(0, bt + 8); c.line_to(0, bt + 44); c.stroke()
    swing = 16 * math.sin(math.pi * 2 * ph) if step is not None else 0.0
    arms = [(-39, -12 + swing, 8), (39, 12 + swing, -8)]
    elbows = []
    for sx, a1, a2 in arms:
        _glove_arm(k, sx, bt + 14, a1, a2, seed + 9 + sx, w=15)
        elbows.append((sx + math.sin(math.radians(a1)) * 48, bt + 14 + math.cos(math.radians(a1)) * 48))
    if wrap and LOOK[0] >= 4:                              # v4: the swag hangs below her hair, the ends outside her arms
        (ax, ay), (bx, by) = elbows
        _cloth(c, [("M", ax - 14, ay - 8), ("C", ax + 6, bt + 150, bx - 6, bt + 150, bx + 14, by - 8), ("L", bx + 16, by + 12),
                   ("C", bx - 10, bt + 182, ax + 10, bt + 182, ax - 16, ay + 12)])
        _curve(c, (ax - 12, ay + 6, ax + 8, bt + 172, bx - 8, bt + 172, bx + 12, by + 6), WRAP_PALE, 1.6)
        for i, (ex, ey) in enumerate(elbows):
            c.save(); c.translate(ex + (-10 if i == 0 else 10), ey + 2)
            _tail4(k, 1.0, -1 if i == 0 else 1)
            c.restore()
    elif wrap:                                             # across her back, from elbow to elbow
        (ax, ay), (bx, by) = elbows
        cut(k, [(ax - 12, ay - 26), (bx + 12, by - 26), (bx + 13, by + 4), (0, max(ay, by) + 16), (ax - 13, ay + 4)], WRAP, lw=2)
        c.set_source_rgb(*(WRAP_PALE if LOOK[0] >= 3 else WRAP_EDGE)); c.set_line_width(1.4 if LOOK[0] < 3 else 1.7)
        c.move_to(ax - 6, ay - 16); c.curve_to(-10, ay, 10, by, bx + 6, by - 16); c.stroke()
        if LOOK[0] >= 3:
            c.move_to(ax - 8, ay + 1); c.curve_to(-10, max(ay, by) + 16, 10, max(ay, by) + 16, bx + 8, by + 1); c.stroke()
        c.restore()
        for i, (ex, ey) in enumerate(elbows):
            if LOOK[0] >= 3:
                _drape3(k, x + ex * s, feet + bob + ey * s, s, seed + 350 + i, side=-1 if i == 0 else 1)
            else:
                _drape(k, x + ex * s, feet + bob + ey * s, s, seed + 350 + i, side=-1 if i == 0 else 1)
        c.save(); c.translate(x, feet + bob); c.scale(s, s)
    back = [(-52 + lgx, hy - 30), (-72 + lgx * 1.4, bt + 30), (-66 + lgx * 1.8, bt + 96 + lgy), (-46 + lgx * 1.8, bt + 108 + lgy),
            (-18 + lgx * 1.8, bt + 102 + lgy), (18 + lgx * 1.8, bt + 102 + lgy), (46 + lgx * 1.8, bt + 108 + lgy),
            (66 + lgx * 1.8, bt + 96 + lgy), (72 + lgx * 1.4, bt + 30), (52 + lgx, hy - 30)]
    if wrap and LOOK[0] < 4:                               # v2, v3: her hair gathered forward over one shoulder (too short)
        back = [(-52, hy - 30), (-58, hy + 30), (-40, hy + 52), (-14, hy + 58), (14, hy + 58), (40, hy + 52), (58, hy + 30), (52, hy - 30)]
    cut(k, back, ss.HAIR, lw=2.2)
    if LOOK[0] >= 4:                                       # v4: the same long hair as from the front, down to her waist
        c.set_source_rgb(*ss.HAIR_SHADE); c.set_line_width(2.2); c.set_line_cap(1)
        for sx, top, bot in ((-46, hy + 30, bt + 96), (-24, hy + 44, bt + 100), (0, hy + 40, bt + 98), (24, hy + 44, bt + 100), (46, hy + 30, bt + 96)):
            c.move_to(sx + lgx, top); c.curve_to(sx * 1.08 + lgx * 1.4, (top + bot) / 2, sx * 1.10 + lgx * 1.7, bot - 20, sx * 1.04 + lgx * 1.8, bot + lgy); c.stroke()
    ellipse(k, 0, hy, 54, 52, ss.HAIR, seed + 20, shadow=False, lw=2)
    c.set_source_rgb(*INK); c.set_line_width(2)
    c.move_to(0, hy - 52); c.curve_to(-3, hy - 30, 3, hy, 0, hy + 40); c.stroke()                 # the parting
    c.set_source_rgb(*ss.HAIR_SHADE); c.set_line_width(2.2); c.set_line_cap(1)
    for sx in (-1, 1):
        c.move_to(sx * 22, hy - 30); c.curve_to(sx * 30, hy, sx * 30, hy + 24, sx * 24, hy + 48); c.stroke()
    c.set_source_rgb(*ss.HAIR_SHINE); c.set_line_width(4.5)
    c.move_to(-34, hy - 32); c.curve_to(-18, hy - 42, 12, hy - 42, 32, hy - 32); c.stroke()
    for sx in (-1, 1):                                     # the diamonds, just showing
        _glint(c, sx * 57, hy + 34, 6)
    c.restore()
    return {"head": (x, feet + bob + hy * s)}


def party(k, x, feet, s=1.0, pose="g_blower", face="caught", look=(0.7, 0.0), mouth=None, sugar=True, hat=True,
          blow=None, seed=7):
    """Awake: a plain red party dress with sleeves to the elbow, her pearls, icing sugar on one cheek."""
    def builder(badge):
        def hook(k_, bt, seed_):
            c = k_.c
            cut(k_, [(-38, bt - 1), (38, bt - 1), (42, bt + 40), (30, bt + 100), (54, -78), (-54, -78), (-30, bt + 100),
                     (-42, bt + 40)], KEY, lw=2.2)
            cut(k_, [(-17, bt - 1), (17, bt - 1), (11, bt + 13), (0, bt + 17), (-11, bt + 13)], so.SKIN, shadow=False, lw=1.8)
            c.set_source_rgb(*GOWN_SHADE); c.set_line_width(2.0); c.set_line_cap(1)
            c.move_to(-30, bt + 100); c.curve_to(-10, bt + 105, 10, bt + 105, 30, bt + 100); c.stroke()
            c.move_to(-12, bt + 106); c.line_to(-20, -80); c.move_to(14, bt + 106); c.line_to(22, -80); c.stroke()
        return hook
    with _swap((sv, "RED", KEY), (so, "RED", KEY), (sbc, "_hook", builder), (sbc, "BLAZER", KEY)):
        o = so.sofia(k, x, feet, s, pose, face, look=look, badge=False, tablet_kind=None, mouth=mouth, seed=seed)
    (lx, ly), (rx, ry) = o["hands"]
    hx, hy = o["head"]
    c = k.c
    if sugar:                                              # on her screen-right cheek, where she lay on the doughnut
        for i, (dx, dy, r) in enumerate(((27, 14, 7.5), (35, 22, 5.5), (22, 25, 5.0), (31, 6, 3.6), (40, 13, 3.0), (17, 15, 2.6))):
            ellipse(k, hx + dx * s, hy + dy * s, r * s, r * 0.82 * s, (1, 1, 1), seed + 370 + i, shadow=False, lw=1.0 * s)
    if hat:
        paper_hat(k, hx - 24 * s, hy - 54 * s, 0.92 * s, -0.42)
    if blow is not None or pose == "g_blower":
        blower(k, (lx + rx) / 2 + 6 * s, (ly + ry) / 2 - 2 * s, s * 0.85, out=blow or 0.0, ang=-0.12)
        for hx_, hy_ in ((lx, ly), (rx, ry)):
            ellipse(k, hx_, hy_ + 3 * s, 8.5 * s, 8.5 * s, so.SKIN, seed + 334 + int(hx_), shadow=False, lw=1.8 * s)
    return o


# ---------------------------------------------------------------- the ten bays, the napkin, the plan
def bays(c, x, y, w, lw=2.2):
    """Ten bays in two rows of five; the last one is L-shaped. (x, y) is the top left; w is one bay's width."""
    h = w * 1.25
    c.save(); c.set_line_join(1); c.set_line_cap(1); c.set_line_width(lw)
    c.new_path()
    c.move_to(x, y); c.line_to(x + 5 * w, y); c.line_to(x + 5 * w, y + h * 1.45); c.line_to(x + 5.9 * w, y + h * 1.45)
    c.line_to(x + 5.9 * w, y + 2 * h); c.line_to(x, y + 2 * h); c.close_path(); c.stroke()
    c.move_to(x, y + h); c.line_to(x + 5 * w, y + h); c.stroke()
    for i in range(1, 5):
        c.move_to(x + i * w, y); c.line_to(x + i * w, y + 2 * h); c.stroke()
    if LOOK[0] >= 3:                                       # v3: the odd bay is solid, so it reads black on white and white on dark
        c.new_path(); c.move_to(x + 4 * w, y + h); c.line_to(x + 5 * w, y + h); c.line_to(x + 5 * w, y + h * 1.45)
        c.line_to(x + 5.9 * w, y + h * 1.45); c.line_to(x + 5.9 * w, y + 2 * h); c.line_to(x + 4 * w, y + 2 * h); c.close_path()
        c.fill_preserve(); c.stroke()
    c.restore()


def napkin2(k, x, y, s=1.0, back=False, ang=-0.06, seed=600):
    """v2 of his note: the ten bays with the L-shaped corner, and a question mark. back=True: her answer (as v1)."""
    if back:
        return napkin(k, x, y, s, True, ang, seed)
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    rect(k, -62, -46, 124, 92, (0.97, 0.96, 0.93), seed, lw=1.8)
    c.set_source_rgb(0.86, 0.85, 0.82); c.set_line_width(1.0); c.rectangle(-56, -40, 112, 80); c.stroke()
    c.set_source_rgb(*INK)
    bays(c, -52, -27, 13.5, 2.3)
    c.select_font_face("Inter", 0, 1); c.set_font_size(40); c.move_to(34, 4); c.show_text("?")
    c.restore()


def plan_open2(k, x, y, s=1.0, ang=0.0, seed=610):
    """The roll, a hand's width unrolled: the same ten bays, white on blue. (x, y) is the middle of the open part."""
    c = k.c
    BLUE, BLUE_D = (0.16, 0.36, 0.72), (0.10, 0.24, 0.52)
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    rect(k, -66, -44, 118, 88, BLUE, seed, lw=2)
    c.set_source_rgb(0.95, 0.97, 1.0)
    bays(c, -56, -28, 15.5, 2.4)
    rect(k, 46, -50, 26, 100, BLUE_D, seed + 1, lw=2)                                           # the rest, still rolled
    ellipse(k, 59, -50, 13, 5, (0.90, 0.93, 0.98), seed + 2, shadow=False, lw=1.6)
    ellipse(k, 59, 50, 13, 5, BLUE_D, seed + 3, shadow=False, lw=1.6)
    c.restore()


def stamp_page(k, x, y, s=1.0, ang=-0.08, seed=620):
    """His notebook page, stamped."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    rect(k, -50, -34, 100, 68, (0.96, 0.95, 0.90), seed, lw=1.8)
    c.set_source_rgb(0.74, 0.76, 0.80); c.set_line_width(1.0)
    for ly in (-22, -10, 2, 14, 26):
        c.move_to(-42, ly); c.line_to(42, ly); c.stroke()
    c.rotate(-0.16)
    c.set_source_rgb(*INK); c.set_line_width(3.0); c.rectangle(-44, -19, 88, 38); c.stroke()
    c.select_font_face("Inter", 0, 1); c.set_font_size(15.5)
    for i, t in enumerate(("CASE", "CLOSED")):
        e = c.text_extents(t); c.move_to(-e.width / 2 - e.x_bearing, -3 + i * 16); c.show_text(t)
    c.restore()


# ---------------------------------------------------------------- Detective Don
def magnifier(k, x, y, s=1.0, ang=0.5, seed=700, r=19.0):
    """(x, y) is the hand on the handle; the lens is up along ang (radians from straight up, clockwise)."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    rect(k, -3.4, -22, 6.8, 30, (0.16, 0.15, 0.17), seed, shadow=False, lw=1.6)
    c.new_path(); c.arc(0, -22 - r, r, 0, 2 * math.pi); c.set_source_rgba(0.80, 0.90, 0.98, 0.45); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(6.0); c.arc(0, -22 - r, r, 0, 2 * math.pi); c.stroke()
    c.set_source_rgb(*SILVER); c.set_line_width(2.6); c.arc(0, -22 - r, r, 0, 2 * math.pi); c.stroke()
    c.set_source_rgba(1, 1, 1, 0.9); c.set_line_width(2.4); c.set_line_cap(1)
    c.arc(0, -22 - r, r - 6, math.pi * 1.10, math.pi * 1.42); c.stroke()
    c.restore()


def glass_view(k, x, y, r, what="eye", seed=710):
    """What his glass shows, large: "eye" (his, on her), "phone" (the lipstick telephone), "prints" (her heel prints
    ending at a broom)."""
    c = k.c
    c.save(); c.new_path(); c.arc(x, y, r, 0, 2 * math.pi); c.clip()
    if what == "eye":
        c.set_source_rgb(*d.SKIN); c.paint()
        c.set_source_rgb(*BLACK); c.rectangle(x - r, y - r, 2 * r, r * 0.42); c.fill()             # the hat's brim
        c.save(); c.translate(x, y + r * 0.12)
        c.new_path(); c.save(); c.scale(r * 0.66, r * 0.46); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        c.set_source_rgb(1, 1, 1); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(3.2); c.stroke()
        c.new_path(); c.arc(r * 0.16, 0, r * 0.30, 0, 2 * math.pi); c.set_source_rgb(0.30, 0.42, 0.56); c.fill_preserve()
        c.set_source_rgb(*INK); c.set_line_width(2.4); c.stroke()
        c.new_path(); c.arc(r * 0.16, 0, r * 0.14, 0, 2 * math.pi); c.fill()
        c.set_source_rgb(1, 1, 1); c.new_path(); c.arc(r * 0.07, -r * 0.09, r * 0.06, 0, 2 * math.pi); c.fill()
        c.set_source_rgb(*INK); c.set_line_width(6.5); c.set_line_cap(1)
        c.move_to(-r * 0.62, -r * 0.52); c.line_to(r * 0.66, -r * 0.66); c.stroke()               # the brow
        c.restore()
    elif what == "phone":
        c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
        c.set_source_rgb(*KEY); c.set_line_cap(1); c.set_line_join(1)
        g = r / 34.0
        c.save(); c.translate(x - 2 * g, y - 4 * g); c.rotate(-0.62); c.scale(g, g)
        c.set_line_width(7.0); c.arc(0, 12, 20, math.pi * 1.20, math.pi * 1.80); c.stroke()
        for sx in (-1, 1):
            c.save(); c.translate(sx * 16, 1.5); c.rotate(sx * 0.55); c.set_line_width(9.6)
            c.move_to(-3, 2.5); c.line_to(3, 2.5); c.stroke(); c.restore()
        c.restore()
        c.select_font_face("Permanent Marker", 0, 0); c.set_font_size(11.5 * g); c.move_to(x - 27 * g, y + 25 * g); c.show_text("555 0142")
    elif LOOK[0] >= 3:                                     # v3: three clear heel prints, the last one half swept, a whole broom
        c.set_source_rgb(0.46, 0.46, 0.49); c.paint()
        g = r / 42.0
        c.set_source_rgb(0.38, 0.38, 0.41); c.set_line_width(1.2 * g)                               # the paving
        for i in range(-3, 4):
            c.move_to(x - r, y + i * 15 * g); c.line_to(x + r, y + i * 15 * g); c.stroke()
        for i, (px, py) in enumerate(((-30, 9), (-13, -8), (4, 9))):
            c.save(); c.translate(x + px * g, y + py * g); c.rotate(-0.12); c.scale(g, g)
            c.set_source_rgb(1, 1, 1)
            c.new_path(); c.move_to(-2, -5.5); c.curve_to(8, -8, 15, -3, 15, 0); c.curve_to(15, 3, 8, 8, -2, 5.5); c.close_path(); c.fill()
            c.new_path(); c.arc(-8.5, 0, 3.0, 0, 2 * math.pi); c.fill()
            c.restore()
        c.set_source_rgba(1, 1, 1, 0.55); c.set_line_width(5 * g); c.set_line_cap(1)                 # what the broom has smeared
        c.move_to(x + 10 * g, y + 4 * g); c.line_to(x + 19 * g, y - 3 * g); c.stroke()
        c.save(); c.translate(x + 27 * g, y + 2 * g); c.rotate(0.22); c.scale(g, g)
        c.set_source_rgb(*INK); c.set_line_width(8); c.move_to(4, -12); c.line_to(22, -60); c.stroke()
        c.set_source_rgb(0.72, 0.56, 0.36); c.set_line_width(4.6); c.move_to(4, -12); c.line_to(22, -60); c.stroke()
        rect(k, -9, -22, 13, 44, (0.50, 0.36, 0.22), seed + 5, shadow=False, lw=1.8)
        cut(k, [(-9, -22), (-9, 22), (-27, 27), (-27, -27)], (0.86, 0.74, 0.46), shadow=False, lw=1.8)
        c.set_source_rgb(0.50, 0.40, 0.20); c.set_line_width(1.3)
        for i in range(-3, 4):
            c.move_to(-10, i * 6); c.line_to(-26, i * 7.4); c.stroke()
        c.restore()
    else:
        c.set_source_rgb(0.42, 0.42, 0.45); c.paint()
        footprints(k, x - r * 0.72, y + r * 0.08, r / 42.0, n=3, step=22)
        c.save(); c.translate(x + r * 0.55, y + r * 0.1); c.rotate(-0.25)
        for i in range(9):
            c.set_source_rgb(0.80, 0.68, 0.40); c.set_line_width(3.2 * r / 42.0); c.set_line_cap(1)
            c.move_to((i - 4) * 3.4 * r / 42.0, -r * 0.5); c.line_to((i - 4) * 5.0 * r / 42.0, r * 0.5); c.stroke()
        c.restore()
    c.restore()
    c.set_source_rgb(*INK); c.set_line_width(max(5.0, r * 0.11)); c.new_path(); c.arc(x, y, r, 0, 2 * math.pi); c.stroke()
    c.set_source_rgb(*SILVER); c.set_line_width(max(2.2, r * 0.045)); c.new_path(); c.arc(x, y, r, 0, 2 * math.pi); c.stroke()
    c.set_source_rgba(1, 1, 1, 0.85); c.set_line_width(max(2.0, r * 0.05)); c.set_line_cap(1)
    c.new_path(); c.arc(x, y, r - r * 0.16, math.pi * 1.10, math.pi * 1.36); c.stroke()


def glass_handle(k, x, y, r, ang=0.75, seed=715):
    """v3: the handle of the glass and the fist that holds it, so the eye in it has an owner. Draw before glass_view."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang)
    rect(k, -r * 0.10, r * 0.96, r * 0.20, r * 1.0, (0.16, 0.15, 0.17), seed, shadow=False, lw=2.2)
    ellipse(k, 0, r * 1.62, r * 0.36, r * 0.30, d.SKIN, seed + 1, shadow=False, lw=2.4)
    for i in range(4):
        ellipse(k, -r * 0.05, r * (1.40 + i * 0.145), r * 0.33, r * 0.085, d.SKIN, seed + 2 + i, shadow=False, lw=1.6)
    c.restore()


def footprints(k, x, y, s=1.0, n=4, step=26, seed=720):
    """Her heel prints in powder, walking to screen right: a sole and a dot, left and right."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    for i in range(n):
        px, py = i * step, (-7 if i % 2 else 7)
        c.set_source_rgba(1, 1, 1, 0.95)
        c.new_path(); c.save(); c.translate(px + 5, py); c.scale(7.5, 4.2); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
        c.new_path(); c.arc(px - 7, py, 2.4, 0, 2 * math.pi); c.fill()
    c.restore()


def powder_puff(k, x, y, s=1.0, seed=730):
    """The compact on the stones, and its powder in the air."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    for i, (dx, dy, r, a) in enumerate(((0, -16, 26, 0.55), (-24, -8, 18, 0.5), (24, -10, 19, 0.5), (-8, -36, 16, 0.42),
                                        (16, -34, 14, 0.4), (-38, 2, 10, 0.4), (40, 0, 11, 0.4))):
        c.set_source_rgba(1, 1, 1, a); c.new_path(); c.arc(dx, dy, r, 0, 2 * math.pi); c.fill()
    ellipse(k, -6, 2, 15, 5.5, SILVER, seed, shadow=False, lw=1.6)
    ellipse(k, 12, -2, 14, 7, SILVER, seed + 1, shadow=False, lw=1.6)
    ellipse(k, 12, -2, 10, 4.6, (0.74, 0.80, 0.86), seed + 2, shadow=False, lw=1.0)
    c.restore()


def detective(k, x, feet, s=1.0, pose="look", face="squint", look=(0.8, 0.5), lean=0.0, glass=True, wrap=False,
              napkin_in_band=False, seed=500):
    """Don as the detective: his Office Noir hat and coat. pose: "look" (the glass held out low), "up" (the glass
    raised to his eye), "stamp" (the notebook), or four angles."""
    a = {"look": (-10, 4) + d.dm.ik(1, 52, d.BT + 84), "up": (-10, 4) + d.dm.ik(1, 30, d.HY + 16),
         "stamp": d.dm.ik(-1, -20, d.BT + 70) + d.dm.ik(1, 24, d.BT + 50)}.get(pose, pose)
    v3 = LOOK[0] >= 3
    brim = 1.0
    if v3:
        if pose == "look" and wrap:                        # her wrap held up and away from him, by two fingers
            a = d.dm.ik(-1, -62, d.BT + 30) + a[2:]
        elif pose == "proud":                              # the stamped page held up to the room, a fist on his hip
            a = d.dm.ik(-1, -44, d.BT + 104) + d.dm.ik(1, 58, d.HY + 6)
            brim = 0.25
    with _swap(*([(d, "FEDORA_RIM", True)] if v3 else [])):
        o = d.don_noir(k, x, feet, s, a, face, look, brim=brim, outline=False, heart_on=False, lean=lean, seed=seed)
    c = k.c
    (lx, ly), (rx, ry) = o["hands"]
    if v3 and pose == "proud":
        hx, hy = o["head"]
        ellipse(k, hx + 1 * s, hy + 29 * s, 24 * s, 12 * s, d.SKIN, seed + 75, shadow=False, outline=False)   # the grin
        c.set_source_rgb(*INK); c.set_line_width(3.2 * s); c.set_line_cap(1)
        c.new_path(); c.move_to(hx - 17 * s, hy + 23 * s); c.curve_to(hx - 8 * s, hy + 39 * s, hx + 12 * s, hy + 39 * s, hx + 20 * s, hy + 21 * s); c.stroke()
        c.set_line_width(2.0 * s); c.move_to(hx + 20 * s, hy + 17 * s); c.line_to(hx + 23 * s, hy + 23 * s); c.stroke()
        stamp_page(k, rx + 4 * s, ry - 30 * s, s * 0.78, 0.10, seed + 71)
        ellipse(k, rx, ry, 10 * s, 10 * s, d.SKIN, seed + 72, shadow=False, lw=2 * s)
        if napkin_in_band:
            c.save(); c.translate(hx + 30 * s, hy - 40 * s); c.rotate(0.35); c.scale(s, s)
            rect(k, -9, -16, 18, 22, (0.97, 0.96, 0.93), seed + 70, shadow=False, lw=1.4)
            c.set_source_rgb(*KEY); c.set_line_width(2.2); c.set_line_cap(1); c.move_to(-4, -8); c.line_to(4, -10); c.stroke()
            c.restore()
        return o
    if LOOK[0] >= 4 and wrap:                              # v4: the same cloth, hanging from his finger and thumb
        c.save(); c.translate(lx, ly + 4 * s); c.scale(s, s)
        _cloth(c, [("M", -5, 0), ("C", -2, -3, 2, -3, 5, 0), ("C", 20, 14, 26, 50, 20, 88), ("C", 18, 104, 12, 114, 8, 122),
                   ("C", 4, 110, 0, 100, -4, 104), ("C", -8, 110, -12, 116, -16, 124), ("C", -22, 104, -26, 50, -5, 0)])
        _curve(c, (4, 6, 16, 22, 20, 56, 14, 96), WRAP_PALE, 1.6)
        _curve(c, (-4, 8, -16, 30, -18, 70, -14, 104), WRAP_PALE, 1.4)
        c.set_source_rgb(*WRAP_PALE); c.set_line_width(1.3); c.set_line_cap(1)
        for fx, fy in ((6, 120), (10, 122), (-14, 122), (-18, 124)):
            c.move_to(fx, fy); c.line_to(fx + 1, fy + 10); c.stroke()
        c.restore()
        for i, dx in enumerate((-4, 4)):
            ellipse(k, lx + dx * s, ly + 5 * s, 4 * s, 7 * s, d.SKIN, seed + 76 + i, shadow=False, lw=1.5 * s)
        wrap = False
    elif v3 and wrap:
        c.save(); c.translate(lx, ly + 4 * s); c.scale(s, s)
        body = [(-9, 0), (9, 0), (17, 30), (20, 96), (10, 112), (-4, 100), (-16, 104), (-19, 34)]
        cut(k, body, WRAP, shadow=False, lw=2)
        _pale_edge(c, [(-6, 6), (-15, 34), (-13, 98), (-4, 95), (10, 106), (16, 94), (13, 32), (6, 6)], 1.7)
        c.set_source_rgb(*WRAP_PALE); c.set_line_width(1.3); c.set_line_cap(1)
        for fx, fy in ((-14, 104), (-8, 101), (2, 104), (9, 111), (16, 103)):
            c.move_to(fx, fy); c.line_to(fx + 1, fy + 11); c.stroke()
        c.restore()
        for i, dx in enumerate((-4, 4)):                                                         # finger and thumb, pinching it
            ellipse(k, lx + dx * s, ly + 5 * s, 4 * s, 7 * s, d.SKIN, seed + 76 + i, shadow=False, lw=1.5 * s)
        wrap = False
    if napkin_in_band:
        hx, hy = o["head"]
        c.save(); c.translate(hx + 30 * s, hy - 40 * s); c.rotate(0.35); c.scale(s, s)
        rect(k, -9, -16, 18, 22, (0.97, 0.96, 0.93), seed + 70, shadow=False, lw=1.4)
        c.set_source_rgb(*KEY); c.set_line_width(2.2); c.set_line_cap(1); c.move_to(-4, -8); c.line_to(4, -10); c.stroke()
        c.restore()
    if wrap:                                               # her wrap, over his screen-left forearm
        c.save(); c.translate(lx + 4 * s, ly - 20 * s); c.scale(s, s)
        cut(k, [(-17, -8), (17, -10), (19, 52), (6, 66), (-15, 54)], WRAP, shadow=False, lw=2)
        c.set_source_rgb(*WRAP_EDGE); c.set_line_width(1.3); c.set_line_cap(1)
        c.move_to(-8, -2); c.line_to(-6, 50); c.move_to(6, -3); c.line_to(9, 52); c.stroke()
        for fx in (-10, -3, 4, 11):
            c.move_to(fx, 56); c.line_to(fx + 1, 68); c.stroke()
        c.restore()
    if pose == "stamp":
        stamp_page(k, (lx + rx) / 2, (ly + ry) / 2 - 24 * s, s * 0.66, -0.06, seed + 71)
        for hx_, hy_ in ((lx, ly), (rx, ry)):
            ellipse(k, hx_, hy_, 10 * s, 10 * s, d.SKIN, seed + 72 + int(hx_), shadow=False, lw=2 * s)
    elif glass:
        magnifier(k, rx, ry, s, 0.9 if pose == "look" else -0.5, seed + 73)
        ellipse(k, rx, ry, 10 * s, 10 * s, d.SKIN, seed + 74, shadow=False, lw=2 * s)
    return o


# ---------------------------------------------------------------- Pam, sweeping
def broom(k, x0, y0, x1, y1, s=1.0, seed=740):
    """A street broom from the top of its handle (x0, y0) to the head on the ground (x1, y1)."""
    c = k.c
    c.set_source_rgb(*INK); c.set_line_width(7.4 * s); c.set_line_cap(1); c.move_to(x0, y0); c.line_to(x1, y1); c.stroke()
    c.set_source_rgb(0.72, 0.56, 0.36); c.set_line_width(4.2 * s); c.move_to(x0, y0); c.line_to(x1, y1); c.stroke()
    g = math.atan2(y1 - y0, x1 - x0) - math.pi / 2
    c.save(); c.translate(x1, y1); c.rotate(g); c.scale(s, s)
    rect(k, -30, -6, 60, 12, (0.50, 0.36, 0.22), seed, shadow=False, lw=1.8)
    cut(k, [(-30, 6), (30, 6), (36, 30), (-36, 30)], (0.84, 0.72, 0.44), shadow=False, lw=1.8)
    c.set_source_rgb(0.56, 0.44, 0.22); c.set_line_width(1.3)
    for i in range(-4, 5):
        c.move_to(i * 6.4, 8); c.line_to(i * 7.6, 28); c.stroke()
    c.restore()


def dustpan(k, x, y, s=1.0, full=True, seed=750):
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    cut(k, [(-26, 0), (26, 0), (20, -18), (-20, -18)], (0.42, 0.44, 0.48), shadow=False, lw=1.8)
    rect(k, -3.5, -40, 7, 24, (0.30, 0.31, 0.34), seed, shadow=False, lw=1.5)
    if full:
        for dx, dy, r in ((-10, -6, 6), (2, -8, 7), (12, -5, 5)):
            c.set_source_rgba(1, 1, 1, 0.95); c.new_path(); c.arc(dx, dy, r, 0, 2 * math.pi); c.fill()
    c.restore()


def flat_cap(k, x, y, s=1.0, seed=760):
    """A sweeper's cap; (x, y) is the middle of its band, on her brow line."""
    c = k.c
    CAPC, CAPD = (0.34, 0.35, 0.38), (0.20, 0.21, 0.24)
    c.save(); c.translate(x, y); c.scale(s, s)
    cut(k, [(-46, 2), (-50, -14), (-34, -30), (0, -36), (36, -30), (52, -14), (48, 2)], CAPC, shadow=False, lw=2)
    cut(k, [(-48, 0), (48, 0), (62, 8), (40, 12), (-44, 8)], CAPD, shadow=False, lw=2)           # the peak
    ellipse(k, 0, -34, 5, 3.4, CAPD, seed, shadow=False, lw=1.4)
    c.restore()


def sweeper(k, x, feet, s=1.0, pose="lean", face="neutral", look=(0, 0), seed=40):
    """Pam with a broom. pose: "lean" (both hands on the handle, at rest), "sweep" (the broom across her, working)."""
    ik = pn.pm.ik
    a = {"lean": ik(-1, 16, pn.BT + 66) + ik(1, 28, pn.BT + 30), "sweep": ik(-1, -8, pn.BT + 92) + ik(1, 34, pn.BT + 56)}[pose]
    items = []
    if LOOK[0] >= 3:                                       # v3: a pale sweeper's apron, under her arms
        APRON, APRON_D = (0.93, 0.92, 0.88), (0.70, 0.69, 0.66)
        orig = pn._costume

        def costume(badge=True):
            base = orig(badge)

            def hook(k_, name_, p_, bt, seed_):
                base(k_, name_, p_, bt, seed_)
                c = k_.c
                cut(k_, [(-21, bt + 40), (21, bt + 40), (24, pn.HEM - 12), (44, pn.HEM - 8), (42, -34), (-42, -34), (-44, pn.HEM - 8),
                         (-24, pn.HEM - 12)], APRON, shadow=False, lw=2)
                c.set_source_rgb(*INK); c.set_line_width(2.0)
                for sx in (-1, 1):                                                               # the straps
                    c.move_to(sx * 21, bt + 40); c.line_to(sx * 30, bt + 4); c.stroke()
                c.set_source_rgb(*APRON_D); c.set_line_width(1.6)
                c.move_to(-44, pn.HEM - 8); c.line_to(44, pn.HEM - 8); c.stroke()
                c.rectangle(-17, pn.HEM + 6, 34, 24); c.stroke()                                  # one pocket
            return hook
        items = [(pn, "_costume", costume)]
    with _swap(*items):
        o = pn.pam_noir(k, x, feet, s, a, face, look, roll=False, seed=seed)
    hx, hy = o["head"]
    flat_cap(k, hx, hy - 30 * s, s * 1.02, seed + 60)
    (lx, ly), (rx, ry) = o["hands"]
    if pose == "lean":
        dx, dy = lx - rx, ly - ry
        broom(k, rx - dx * 0.5, ry - dy * 0.5, rx + dx * 4.4, feet - 16 * s, s, seed + 61)
    else:
        dx, dy = lx - rx, ly - ry
        broom(k, rx - dx * 0.4, ry - dy * 0.4, lx + dx * 1.5, feet - 14 * s, s, seed + 61)
    for hx_, hy_ in ((lx, ly), (rx, ry)):
        ellipse(k, hx_, hy_, 9 * s, 9 * s, pn.ps.SKIN, seed + 62 + int(hx_), shadow=False, lw=1.8 * s)
    return o


# ---------------------------------------------------------------- the robot, at the door
def cup(k, x, y, s=1.0, seed=770):
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    cut(k, [(-13, -16), (13, -16), (10, 14), (-10, 14)], SILVER, shadow=False, lw=1.8)
    ellipse(k, 0, -16, 13, 4.2, (0.30, 0.31, 0.34), seed, shadow=False, lw=1.6)
    c.set_source_rgb(*SILVER_DARK); c.set_line_width(1.2); c.move_to(-11, -4); c.line_to(11, -4); c.move_to(-10.5, 6); c.line_to(10.5, 6); c.stroke()
    c.restore()


def battery_card(k, x, y, s=1.0, ang=0.04, seed=780):
    """A piece of cardboard with an empty battery drawn on it."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    rect(k, -30, -20, 60, 40, (0.74, 0.60, 0.42), seed, lw=1.8)
    c.set_source_rgb(*INK); c.set_line_width(3.0); c.set_line_join(1)
    c.rectangle(-18, -9, 32, 18); c.stroke(); c.rectangle(14, -4, 5, 8); c.fill()
    c.set_line_width(4.0); c.set_line_cap(1); c.move_to(-12, -4); c.line_to(-12, 4); c.stroke()   # one bar left
    c.restore()


def coin_tag(k, x, y, s=1.0, ang=0.0, seed=790):
    """Her coin, handed back, and the tag on it."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    ellipse(k, 0, 0, 11, 11, (0.93, 0.93, 0.90), seed, shadow=False, lw=1.8)
    c.set_source_rgb(*SILVER_DARK); c.set_line_width(1.2); c.new_path(); c.arc(0, 0, 7.5, 0, 2 * math.pi); c.stroke()
    c.set_source_rgb(*INK); c.set_line_width(1.4); c.move_to(0, 11); c.line_to(2, 24); c.stroke()
    c.translate(2, 24); c.rotate(0.05)                                                            # the tag hangs under it
    cut(k, [(-44, 8), (-36, 0), (36, 0), (44, 8), (44, 36), (-44, 36)], (0.98, 0.95, 0.80), shadow=False, lw=1.8)
    c.set_source_rgb(*INK); c.select_font_face("Inter", 0, 1); c.set_font_size(11.5)
    for i, t in enumerate(("PENDING", "APPROVAL")):
        e = c.text_extents(t); c.move_to(-e.width / 2 - e.x_bearing, 16 + i * 13); c.show_text(t)
    c.restore()


def big_coin(k, x, y, r, seed=795):
    c = k.c
    ellipse(k, x, y, r, r, (0.95, 0.95, 0.92), seed, shadow=False, lw=max(1.6, r * 0.14))
    c.set_source_rgb(*SILVER_DARK); c.set_line_width(max(1.0, r * 0.10)); c.new_path(); c.arc(x, y, r * 0.66, 0, 2 * math.pi); c.stroke()


def coin_steps(k, x, feet, s=1.0, step=1, seed=900):
    """v3: the gag in three drawings. 1: her coin drops into its cup. 2: the arm is already out, across her path.
    3: the coin again, in its claw, with the tag."""
    c = k.c
    o = rn.robot_noir(k, x, feet, s, "stand" if step == 1 else (0.0, 0, 0, (-20, 0), (84, -2)), "eager", (0.7, -0.2) if step == 1 else (0.9, 0.0),
                      cap=False, seed=seed)
    hx, hy = o["head"]
    (lx, ly), (rx, ry) = o["hands"]
    battery_card(k, x - 2 * s, hy + 150 * s, s * 0.9, 0.05, seed + 20)
    cup(k, lx, ly - 16 * s, s * 1.5, seed + 21)
    ellipse(k, lx, ly, 8 * s, 8 * s, (0.20, 0.20, 0.22), seed + 23, shadow=False, lw=1.6 * s)
    if step == 1:
        big_coin(k, lx + 2 * s, ly - 70 * s, 13 * s, seed + 24)
        c.set_source_rgb(1, 1, 1); c.set_line_width(2.2 * s); c.set_line_cap(1)
        for dx in (-9, 0, 9):                                                                    # it is falling
            c.move_to(lx + (2 + dx) * s, ly - 92 * s); c.line_to(lx + (2 + dx) * s, ly - (112 if dx else 122) * s); c.stroke()
        return o
    bx, by = rx + 86 * s, ry - 8 * s
    for col, w in ((INK, 13 * s), (SILVER, 8.5 * s)):
        c.set_source_rgb(*col); c.set_line_width(w); c.set_line_cap(1); c.move_to(rx, ry); c.line_to(bx, by); c.stroke()
    for t in (0.25, 0.5, 0.75):
        ellipse(k, rx + (bx - rx) * t, ry + (by - ry) * t, 7.5 * s, 7.5 * s, SILVER_DARK, seed + 22 + int(t * 8), shadow=False, lw=1.6 * s)
    for sy in (-1, 1):
        c.set_source_rgb(*INK); c.set_line_width(6.5 * s); c.move_to(bx, by); c.line_to(bx + 15 * s, by + sy * 13 * s); c.stroke()
        c.set_source_rgb(*SILVER); c.set_line_width(3.4 * s); c.move_to(bx, by); c.line_to(bx + 15 * s, by + sy * 13 * s); c.stroke()
    if step == 2:
        c.set_source_rgb(1, 1, 1); c.set_line_width(2.2 * s)                                         # how fast it came out
        for dy in (-22, -32, 20):
            c.move_to(rx + 6 * s, ry + dy * s); c.line_to(bx - 14 * s, by + dy * s); c.stroke()
    else:
        big_coin(k, bx + 17 * s, by, 13 * s, seed + 24)
        c.save(); c.translate(bx + 17 * s, by + 13 * s); c.scale(s * 1.35, s * 1.35)
        c.set_source_rgb(*INK); c.set_line_width(1.4); c.move_to(0, 0); c.line_to(2, 12); c.stroke()
        c.translate(2, 12); c.rotate(0.05)
        cut(k, [(-44, 8), (-36, 0), (36, 0), (44, 8), (44, 36), (-44, 36)], (0.98, 0.95, 0.80), shadow=False, lw=1.8)
        c.set_source_rgb(*INK); c.select_font_face("Inter", 0, 1); c.set_font_size(11.5)
        for i, t in enumerate(("PENDING", "APPROVAL")):
            e = c.text_extents(t); c.move_to(-e.width / 2 - e.x_bearing, 16 + i * 13); c.show_text(t)
        c.restore()
    o["claw"] = (bx + 17 * s, by)
    return o


def beggar(k, x, feet, s=1.0, state="eager", look=(0, 0), reach=False, seed=900):
    """The robot by the bar door: no cap, a tin cup, a card. reach=True: its arm across her path, the coin handed back."""
    o = rn.robot_noir(k, x, feet, s, (0.0, 0, 0, (-20, 0), (80, -4)) if reach else "stand", state, look, cap=False, seed=seed)
    hx, hy = o["head"]
    (lx, ly), (rx, ry) = o["hands"]
    battery_card(k, x - 2 * s, hy + 150 * s, s * 0.9, 0.05, seed + 20)
    cup(k, lx, ly - 14 * s, s * 1.1, seed + 21)
    ellipse(k, lx, ly, 8 * s, 8 * s, (0.20, 0.20, 0.22), seed + 23, shadow=False, lw=1.6 * s)
    if reach:
        c = k.c
        ax, ay = rx, ry                                    # its own arm, and what telescopes out of it
        bx, by = rx + 70 * s, ry - 10 * s
        for col, w in ((INK, 13 * s), (SILVER, 8.5 * s)):
            c.set_source_rgb(*col); c.set_line_width(w); c.set_line_cap(1); c.move_to(ax, ay); c.line_to(bx, by); c.stroke()
        for t in (0.25, 0.5, 0.75):                                                               # the telescoping joints
            jx, jy = ax + (bx - ax) * t, ay + (by - ay) * t
            ellipse(k, jx, jy, 7.5 * s, 7.5 * s, SILVER_DARK, seed + 22 + int(t * 8), shadow=False, lw=1.6 * s)
        coin_tag(k, bx + 12 * s, by - 2 * s, s * 1.0, 0.0, seed + 30)
        for sy in (-1, 1):                                                                        # the claw
            c.set_source_rgb(*INK); c.set_line_width(6 * s); c.move_to(bx, by); c.line_to(bx + 12 * s, by + sy * 11 * s); c.stroke()
            c.set_source_rgb(*SILVER); c.set_line_width(3 * s); c.move_to(bx, by); c.line_to(bx + 12 * s, by + sy * 11 * s); c.stroke()
        o["coin"] = (bx + 12 * s, by - 2 * s)
    return o


# ---------------------------------------------------------------- the rich men, the taxi, the doughnut
def rich_hand(k, x, y, s=1.0, ang=0.0, what="money", flip=1, seed=800):
    """A hand out of the dark: a black sleeve, a white cuff with a link. (x, y) is the hand; the arm comes from
    behind it along ang (radians; 0 = from screen left, pointing right). what: "money" or "coupe"."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s * flip, s)
    cut(k, [(-150, -17), (-34, -15), (-34, 15), (-150, 19)], BLACK, shadow=False, lw=2)
    rect(k, -36, -14, 18, 28, (0.97, 0.97, 0.95), seed, shadow=False, lw=1.8)
    ellipse(k, -27, 6, 2.8, 2.8, SILVER, seed + 1, shadow=False, lw=1.2)
    ellipse(k, -4, 0, 16, 13, d.SKIN, seed + 2, shadow=False, lw=2)
    c.restore()
    hx, hy = x + math.cos(ang) * 4 * s * flip, y + math.sin(ang) * 4 * s * flip
    if what == "money":
        money(k, hx, hy - 4 * s, s * 0.95, 0.0, 4, seed + 3)
    else:
        coupe(k, hx + 2 * s * flip, hy + 32 * s, s * 0.9, seed + 3)
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s * flip, s)
    for i, fy in enumerate((-7, -1, 5)):                                                         # fingers, closed over it
        ellipse(k, 6, fy, 9, 3.6, d.SKIN, seed + 4 + i, shadow=False, lw=1.5)
    c.restore()


def taxi(k, x, y, s=1.0, door=0.0, seed=820):
    """A night cab from the side, nose to screen left. (x, y) is the kerb under the middle of it. door: 0..1, the rear
    door swung open toward us. No name, no number: a roof light and a checker stripe."""
    c = k.c
    BODY, BODY_D, GLASS = (0.22, 0.22, 0.25), (0.12, 0.12, 0.14), (0.52, 0.58, 0.66)
    c.save(); c.translate(x, y); c.scale(s, s)
    for wx in (-104, 96):
        ellipse(k, wx, -22, 26, 26, (0.07, 0.07, 0.08), seed + wx, shadow=False, lw=2.2)
        ellipse(k, wx, -22, 12, 12, SILVER, seed + wx + 1, shadow=False, lw=1.6)
    cut(k, [(-176, -34), (-172, -66), (-120, -78), (-84, -124), (70, -126), (120, -82), (168, -74), (176, -40), (176, -30),
            (130, -30), (126, -48), (66, -48), (62, -30), (-70, -30), (-74, -48), (-134, -48), (-138, -30), (-176, -30)],
        BODY, lw=2.4)
    cut(k, [(-74, -116), (-10, -116), (-10, -84), (-104, -84)], GLASS, shadow=False, lw=1.8)      # the front window
    cut(k, [(0, -116), (64, -116), (98, -84), (0, -84)], GLASS, shadow=False, lw=1.8)             # the rear window
    for i in range(18):                                                                          # the checker stripe
        for r in range(2):
            if (i + r) % 2 == 0:
                c.set_source_rgb(0.95, 0.95, 0.92)
            else:
                c.set_source_rgb(*BLACK)
            c.rectangle(-150 + i * 17, -76 + r * 8, 17, 8); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(1.4); c.rectangle(-150, -76, 306, 16); c.stroke()
    rect(k, -30, -146, 60, 20, (0.99, 0.93, 0.62), seed + 5, shadow=False, lw=1.8)                 # the roof light
    c.set_source_rgb(*INK); c.select_font_face("Inter", 0, 1); c.set_font_size(15)
    e = c.text_extents("TAXI"); c.move_to(-e.width / 2 - e.x_bearing, -131); c.show_text("TAXI")
    ellipse(k, -170, -56, 7, 9, (0.99, 0.96, 0.78), seed + 6, shadow=False, lw=1.6)                # a headlamp
    c.set_source_rgb(*SILVER); c.set_line_width(3.0); c.set_line_cap(1); c.move_to(-178, -34); c.line_to(-150, -34); c.stroke()
    if door > 0:                                                                                 # the rear door, open
        c.set_source_rgb(*BODY_D); c.rectangle(2, -114, 60, 82); c.fill()                         # the dark inside
        w = 60 * (1 - 0.72 * door)
        cut(k, [(64, -118), (64 + w, -112), (64 + w + 4, -36), (64, -32)], BODY, lw=2.2)
        cut(k, [(68, -110), (60 + w, -105), (62 + w, -84), (68, -84)], GLASS, shadow=False, lw=1.6)
    else:
        c.set_source_rgb(*INK); c.set_line_width(1.6); c.move_to(-4, -120); c.line_to(-4, -34); c.stroke()
        c.move_to(64, -118); c.line_to(64, -50); c.stroke()
    c.restore()


def doughnut(k, x, y, s=1.0, seed=840):
    """A sugared doughnut on a paper plate, one bite gone."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    ellipse(k, 0, 8, 38, 9, (0.97, 0.97, 0.95), seed, lw=1.8)
    ellipse(k, 0, -2, 24, 13, (0.80, 0.58, 0.32), seed + 1, shadow=False, lw=2)
    ellipse(k, 0, -5, 22, 9.5, (1, 1, 1), seed + 2, shadow=False, lw=1.2)
    ellipse(k, 0, -4, 6.5, 2.8, (0.62, 0.42, 0.22), seed + 3, shadow=False, lw=1.2)
    ellipse(k, 22, -8, 8, 7, (0.97, 0.97, 0.95), seed + 4, shadow=False, outline=False)          # the bite
    for dx, dy in ((-30, 9), (-22, 12), (28, 11)):
        c.set_source_rgb(1, 1, 1); c.new_path(); c.arc(dx, dy, 2.2, 0, 2 * math.pi); c.fill()
    c.restore()
