"""v1, pinned (cast sheet v1, script v1: the trench and the umbrella). noir2_cast.py is current.
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
