"""OFFICE NOIR 4: the cast's looks, v2 (23 Nov). v1 is pinned as on4_cast_v1.py. v2, after the outside audit (Tomas:
"Improve"): the mask a thin band with almond holes and cat-eye flicks (v1 read as goggles: round holes ringed the eyes);
heavy lids for the slump; the slump bent and lowered; the point at the sign out and away from the head; the point at
herself into her chest; the envelope gripped in the fist (lesson 179); the coat a lighter charcoal than her gloves and
trousers (v1 was one black mass); Don read as a traffic cop by what he does (the whistle in his mouth, a white glove
held out, a bigger star), not by a word (POLICE would not read at 270 px).
v1 (23 Nov). Stage 3 (look and set). Costumes on the series' rigs, never redesigns
(CLAUDE.md), each drawn beside the series look first (lesson 86):
  PAM-CAT   Pam as the episode-14 rig draws her (pm_ps: pam_bc's head, the berry lips, the one hand), with:
            - no readers (glasses off): in her dream she sees without them;
            - a narrow cat-eye half mask whose holes are big enough that her eyes AND brows stay in sight (lesson 163:
              the face carries the joke);
            - two cat ears on her bob; her grey streak stays (it says Pam at a glance, in black and white too);
            - a charcoal coat with a wide collar and a belt, dark trousers, dark boots, DARK gloves (the shadows' gloves
              are pale: that is their one mark, so hers must not be);
  PAM, awake  her series look, and a sleep mask with two small cat ears: down over her eyes asleep (7.1), pushed up on
            her forehead awake (7.3). The real twin of the dream's mask (the Office Noir rule).
  DON, cop  Don as the episode-14 rig draws him (don_ps: the headset, the vest, the ketchup stain, the DON tag), no cap
            (Tomas, 23 Nov: his bald head is how he is known), with a star badge pinned on the vest, a whistle on a cord,
            white gloves.
The dream figures are shown through the Office Noir 2 grade (engine_on TONE v3) on the street's lit-wall grey, and at
phone size.
  python3 on4_cast.py  ->  ../office-noir-4/on4_cast_sheet_v1.png, on4_cast_phone_v1.png"""
import math
import cairo
import kit
import pam_bc as pb
import pam_mf as pm
import pam_xmas as px
import pm_ps
import hands_ps as hp
import don_ps
import engine_on as eng
from kit import Ctx, INK, cut, ellipse

COAT = (0.31, 0.30, 0.32)
COAT_DARK = (0.12, 0.12, 0.13)
COLLAR = (0.40, 0.39, 0.41)
SUIT_LEG = (0.12, 0.12, 0.13)
SUIT_LEG_DARK = (0.05, 0.05, 0.06)
BOOT = (0.06, 0.06, 0.07)
GLOVE_DARK = (0.10, 0.10, 0.11)
MASK = (0.04, 0.04, 0.05)
EAR = (0.07, 0.07, 0.08)
EAR_IN = (0.32, 0.30, 0.32)
SLEEP = (0.93, 0.70, 0.76)          # the sleep mask, pink
SLEEP_DARK = (0.72, 0.46, 0.54)
GLOVE_WHITE = (0.96, 0.96, 0.94)
BADGE = (0.85, 0.72, 0.30)
BT, HY = pm.BT, pm.HY

CAT_POSES = {   # body units (pm.ik); (left hand, right hand) shapes of hands_ps
    "hero": (pm.ik(-1, -50, -128) + pm.ik(1, 50, -128), ("fist", "fist")),        # 1.1 fists on hips
    "sag": ((-4, 0, 4, 0), ("relax_s", "relax_s")),                                # 1.3 the pose let go (bent: see pam_cat)
    "point_up": ((-8, 0) + pm.ik(1, 118, HY - 30), ("relax_s", "point")),          # 4.3 at the sign: out and up, clear of her head
    "point_me": ((-8, 0) + pm.ik(1, -4, BT + 40), ("relax_s", "point")),           # 4.3 then at herself: into her chest
    "lift": ((-8, 0) + pm.ik(1, 110, BT + 96), ("relax_s", "grab")),               # 5.3 the hand into his coat
    "triumph": ((-8, 0) + pm.ik(1, 62, HY - 80), ("relax_s", "fist")),             # 6.3 the envelope held high, off her ear
}
ENV_BIG = [1.0]                    # board v9 (opt-in): 1.25 = the held envelope a quarter bigger
HUNT = [0.0]                       # (24 Nov, two reviews: "too friendly"; Tomas agreed) her hunting face, 0..1: the lids come down over her eyes, the smile is small and to one side
MASK_TILT = [0.0]                  # (24 Nov, the crash) the half mask knocked askew: radians about the head's middle; 0 draws as before
MASK_UP_V2 = [False]               # board v9 (opt-in): pushed up, the sleep mask keeps its stitched eyes and sits smaller


def _coat_costume(badge=True):
    """The coat's front instead of her cardigan's: no white collar, no lanyard, no badge, no keys (they say office);
    a double row of dark buttons and the seams."""
    def hook(k, name_, p, bt, seed):
        c = k.c
        c.set_source_rgb(*COAT_DARK); c.set_line_width(2.4)
        c.move_to(-6, bt + 8); c.line_to(-6, pm.HEM - 4); c.stroke()
        for i, by in enumerate((40, 66, 120)):
            for sx in (-1, 1):
                ellipse(k, sx * 14, bt + by, 3.4, 3.4, (0.34, 0.34, 0.36), seed + 90 + i * 2 + (sx > 0), shadow=False, lw=1.2)
        for yy in (pm.HEM - 4, pm.HEM - 9):
            c.move_to(-40, yy); c.line_to(41, yy); c.stroke()
    return hook


class _swap:
    def __init__(self, *items):
        self.items = items

    def __enter__(self):
        self.old = [(m, n, m[n] if isinstance(m, (dict, list)) else getattr(m, n)) for m, n, _ in self.items]
        for m, n, v in self.items:
            if isinstance(m, (dict, list)):
                m[n] = v
            else:
                setattr(m, n, v)

    def __exit__(self, *a):
        for m, n, v in self.old:
            if isinstance(m, (dict, list)):
                m[n] = v
            else:
                setattr(m, n, v)


def _gloved(colour):
    def h(k, hx, hy, w, skin, seed, d, side):
        return hp.hand(k, hx, hy, w, colour, seed, d, side)
    return h


def ears(k, hx, hy, s, col=EAR, inner=EAR_IN, size=1.0):
    """Two cat ears standing on the bob (head-centre units: the hair's top is about 55 above the eyes)."""
    c = k.c
    c.save(); c.translate(hx, hy); c.scale(s * size, s * size)
    for sx in (-1, 1):
        cut(k, [(sx * 14, -50), (sx * 40, -40), (sx * 36, -82)], col, shadow=False, lw=2.2)
        cut(k, [(sx * 20, -50), (sx * 35, -45), (sx * 33, -70)], inner, shadow=False, outline=False)
    c.restore()


def half_mask(k, hx, hy, s):
    """v2: a thin band over the bridge with almond holes and cat-eye flicks up at the outer corners. The almond's edges
    cross the top and bottom of her eye whites a little, so the eyes read narrower and surer, never as goggles (v1);
    the brows (about 3 above the eyes' top) still show in the holes. Eyes at (+-17, +4) in head units."""
    c = k.c
    c.save(); c.translate(hx, hy); c.scale(s, s); c.rotate(MASK_TILT[0])
    c.new_path()
    c.move_to(-54, -22); c.curve_to(-40, -14, -16, -15, 0, -8); c.curve_to(16, -15, 40, -14, 54, -22)      # the flicks
    c.curve_to(46, -6, 40, 12, 28, 16); c.curve_to(16, 18, 6, 15, 0, 10); c.curve_to(-6, 15, -16, 18, -28, 16)
    c.curve_to(-40, 12, -46, -6, -54, -22); c.close_path()
    for sx in (-1, 1):                                   # almond holes, pointed at both ends
        c.new_sub_path()
        c.move_to(sx * 3, 3); c.curve_to(sx * 8, -10, sx * 26, -11, sx * 33, -3)
        c.curve_to(sx * 26, 14, sx * 9, 15, sx * 3, 3); c.close_path()
    c.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    c.set_source_rgb(*MASK); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.0); c.stroke()
    c.set_fill_rule(cairo.FILL_RULE_WINDING)
    c.restore()


def coat_details(k, x, feet, s):
    """The coat's wide collar and its belt, over the charcoal body."""
    c = k.c
    c.save(); c.translate(x, feet); c.scale(s, s)
    for sx in (-1, 1):
        cut(k, [(0, BT + 6), (sx * 36, BT - 2), (sx * 44, BT + 20), (sx * 8, BT + 58)], COLLAR, shadow=False, lw=2.0)
    cut(k, [(-44, BT + 96), (44, BT + 96), (44, BT + 108), (-44, BT + 108)], COAT_DARK, shadow=False, lw=1.6)
    cut(k, [(-9, BT + 93), (9, BT + 93), (9, BT + 111), (-9, BT + 111)], (0.55, 0.55, 0.57), shadow=False, lw=1.4)
    c.restore()


ENV_SEAL = [False]                 # board v6 (opt-in): a small red heart seal where the flap meets, as on the office envelope


def envelope(k, x, y, s, open_=False):
    """The dream's envelope (the warm tone) held by its edge."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(-0.12); c.scale(s, s)
    cut(k, [(-30, -22), (30, -22), (30, 20), (-30, 20)], (0.93, 0.82, 0.58), shadow=False, lw=2)
    c.set_source_rgb(*INK); c.set_line_width(1.6); c.move_to(-30, -22); c.line_to(0, 2); c.line_to(30, -22); c.stroke()
    if ENV_SEAL[0]:
        seal(c, 0, 4, 7 * HEART[0])
    c.restore()


HEART = [1.0]                                              # (24 Nov) the heart's size on the dream envelope: the film's one red


def seal(c, x, y, r):
    """the red heart seal (the series' neon red, kept by the grade)"""
    c.new_path(); c.move_to(x, y + r * 0.9)
    c.curve_to(x - r * 1.5, y - r * 0.2, x - r * 0.6, y - r * 1.3, x, y - r * 0.45)
    c.curve_to(x + r * 0.6, y - r * 1.3, x + r * 1.5, y - r * 0.2, x, y + r * 0.9); c.close_path()
    c.set_source_rgb(0.93, 0.13, 0.22); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(max(1.0, r * 0.18)); c.stroke()


def pam_cat(k, x, feet, s=0.54, pose="hero", face="proud", look=(0, 0), seed=40, env=False):
    """Pam-Cat. Returns the rig's points. pose "sag": the whole figure bent forward and settled lower (a slump, not a
    stand). With the envelope ("triumph", or env=True) the figure is drawn once off-screen to find the fist, the
    envelope is laid there, and the figure is drawn over it, so the fist grips its lower edge (lesson 179)."""
    c = k.c
    p, gest = CAT_POSES.get(pose, (pose, ("relax_s", "relax_s")))

    def draw():
        with _swap((kit.PEOPLE["PAM"], "body", COAT), (pm, "PURPLE", COAT), (pm, "PURPLE_DARK", COAT_DARK),
                   (px, "TROUSERS", SUIT_LEG), (px, "TROUSERS_DARK", SUIT_LEG_DARK), (px, "TRAINER", BOOT),
                   (kit.HAND, 0, _gloved(GLOVE_DARK)), (pm, "_costume", _coat_costume)):
            hp.reset(*gest)
            o_ = pb.pam(k, x, feet, s, p, face, look, seed, glasses="off", brooch=False, badge=False)
            coat_details(k, x, feet, s)
            hp.redraw_late(k)
        hx_, hy_ = o_["head"]
        if HUNT[0] > 0.02:                                   # over the drawn face, under the mask (pam_ss keeps its own face hook, so this is laid on the head's point)
            SK = kit.PEOPLE["PAM"]["skin"]; hv = HUNT[0]
            c.save(); c.translate(hx_, hy_); c.scale(s, s)
            for sx in (-17, 17):                             # the lids: skin down over the top of each eye, a lash line under it
                c.save(); c.new_path(); c.arc(sx, 4, 13.5, 0, 2 * math.pi); c.clip()
                ly_ = 4 - 13.5 + 27 * 0.52 * hv - (2.0 if sx > 0 else 0.0) * hv        # one a little higher: not a matched pair
                c.set_source_rgb(*SK); c.rectangle(sx - 15, -12, 30, ly_ + 12); c.fill()
                c.set_source_rgb(*INK); c.set_line_width(2.6); c.move_to(sx - 14, ly_ + sx * 0.06 * hv); c.line_to(sx + 14, ly_ - sx * 0.06 * hv); c.stroke()
                c.restore()
            c.set_source_rgb(*SK); c.save(); c.translate(0, 31); c.scale(19, 11); c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
            c.set_source_rgb(0.62, 0.20, 0.26); c.set_line_width(3.6); c.set_line_cap(1)          # the smile: shut, small, up at one corner
            c.move_to(-8, 31); c.curve_to(-2, 33.5, 5, 33, 11, 27.5 - 1.5 * hv); c.stroke()
            c.set_line_cap(0)
            c.restore()
        ears(k, hx_, hy_, s)
        half_mask(k, hx_, hy_, s)
        return o_

    if pose == "sag":                                    # bent forward a little, settled 4 % lower, head tipped down
        c.save(); c.translate(x, feet); c.scale(1.0, 0.96); c.rotate(math.radians(4)); c.translate(-x, -feet)
    if env or pose == "triumph":
        c.push_group(); o = draw(); c.pop_group()           # find the fist
        rx, ry = o["hands"][1]
        envelope(k, rx + 2 * s, ry - 30 * s * ENV_BIG[0], s * 1.2 * ENV_BIG[0])
    o = draw()
    if pose == "sag":
        c.restore()
    return o


def sleep_mask(k, hx, hy, s, up=False):
    """The real twin: a pink sleep mask with two small cat ears, over the eyes (asleep) or pushed up (awake)."""
    c = k.c
    dy = -30 if up else 3
    v2 = up and MASK_UP_V2[0]
    if v2:
        dy = -26; s = s * 0.82
    c.save(); c.translate(hx, hy + dy); c.scale(s, s)
    c.set_source_rgb(*SLEEP_DARK); c.set_line_width(3)
    c.move_to(-46, -2); c.line_to(-58, -6); c.stroke(); c.move_to(46, -2); c.line_to(58, -6); c.stroke()
    cut(k, [(-46, -14), (46, -14), (44, 12), (8, 16), (0, 10), (-8, 16), (-44, 12)], SLEEP, shadow=False, lw=2)
    if not up or v2:                                     # closed eyes stitched on it, asleep
        c.set_source_rgb(*SLEEP_DARK); c.set_line_width(2.4)
        for sx in (-1, 1):
            c.new_path(); c.arc(sx * 20, -2, 9, 0.2, math.pi - 0.2); c.stroke()
    c.restore()
    ears(k, hx, hy + dy + 40, s, SLEEP, SLEEP_DARK, 0.55)


def pam_awake(k, x, feet, s=0.54, mask="down", face="neutral", look=(0, 0), pose="stand"):
    o = pm_ps.pam(k, x, feet, s, pose, face, look, mug=False, glasses="off" if mask == "down" else "low")
    hx, hy = o["head"]
    if mask:
        sleep_mask(k, hx, hy, s, up=(mask == "up"))
    return o


def whistle(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.set_source_rgb(0.78, 0.78, 0.80); c.rectangle(-9, -5, 18, 10); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.6); c.stroke()
    c.new_path(); c.arc(-9, 0, 6, 0, 2 * math.pi); c.set_source_rgb(0.78, 0.78, 0.80); c.fill_preserve(); c.set_source_rgb(*INK); c.stroke()
    c.restore()


def star(c, x, y, r, col=BADGE):
    c.new_path()
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        (c.move_to if i == 0 else c.line_to)(x + math.cos(a) * rr, y + math.sin(a) * rr)
    c.close_path(); c.set_source_rgb(*col); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.4); c.stroke()


CROSSBELT = [True]                 # v3 (23 Nov, Tomas: "drop it"): False in layouts v2; cold viewers read it as a wand
DON_POSES = {"stop": ((-8, 0, 92, -6), ("relax", "palm")),        # 3.1 a white glove held out flat: traffic, wait
             "wave": ((-8, 0, 70, 70), ("relax", "palm")),         # 3.1/3.4 waving the car on
             "stand": ((-8, 0, 8, 0), ("relax", "relax")),
             "inspect": ((-110, -50, 8, 0), ("palm", "relax"))}     # v4b, 3.3: the white glove held up at his eye: clean


def don_cop(k, x, feet, s=0.60, pose="stop", face="neutral", look=(0, 0), whistle_in=True):
    """Don the traffic cop: no cap. A white crossbelt, a star on the vest, white gloves, the whistle in his mouth on its
    cord, and the gesture of the job (a glove held out)."""
    p, hands = DON_POSES.get(pose, (pose, None))
    with _swap((hp, "hand", _wrap_white(hp.hand))):
        o = don_ps.don(k, x, feet, s, p, face, look, hands=hands)
    hx, hy = o["head"]
    c = k.c
    if CROSSBELT[0]:                                                                  # the crossbelt (v3: off; read as a wand)
        c.set_source_rgb(*INK); c.set_line_width(13 * s); c.set_line_cap(0)
        c.move_to(hx + 40 * s, hy + 66 * s); c.line_to(hx - 34 * s, hy + 196 * s); c.stroke()
        c.set_source_rgb(*GLOVE_WHITE); c.set_line_width(10 * s)
        c.move_to(hx + 40 * s, hy + 66 * s); c.line_to(hx - 34 * s, hy + 196 * s); c.stroke()
    star(c, hx - 44 * s, hy + 104 * s, 22 * s)
    c.set_source_rgb(0.30, 0.30, 0.32); c.set_line_width(2.4 * s)                    # the cord, from the whistle to the neck
    if whistle_in:
        c.move_to(hx + 12 * s, hy + 34 * s); c.curve_to(hx + 30 * s, hy + 60 * s, hx + 26 * s, hy + 80 * s, hx + 14 * s, hy + 90 * s); c.stroke()
        whistle(c, hx + 10 * s, hy + 31 * s, s * 1.3)                                  # in his mouth
        c.set_source_rgb(*INK); c.set_line_width(2.2 * s)                               # his cheeks puffed: two arcs
        for sx in (-1, 1):
            c.new_path(); c.arc(hx + sx * 30 * s, hy + 26 * s, 9 * s, -0.6 if sx > 0 else math.pi - 0.6, 0.6 if sx > 0 else math.pi + 0.6); c.stroke()
    else:
        c.move_to(hx - 18 * s, hy + 80 * s); c.curve_to(hx - 10 * s, hy + 120 * s, hx + 6 * s, hy + 130 * s, hx + 14 * s, hy + 132 * s); c.stroke()
        whistle(c, hx + 18 * s, hy + 134 * s, s)
    return o


# ---- v4 (23 Nov, Tomas: "more serious, and a comic prop"): a real traffic cop, and the STOP / GO paddle -------------------
NEON = (0.93, 0.13, 0.22)                   # on4_street.NEON: the accent pass keys on it
CAP_WHITE = (0.95, 0.95, 0.93)
CAP_BAND = (0.10, 0.11, 0.16)
SILVER = (0.80, 0.81, 0.84)
GO_GREEN = (0.16, 0.58, 0.32)


def traffic_cap(k, hx, hy, s):
    """A real traffic policeman's peaked cap, his size: a white top, a dark band, a black visor, a silver badge."""
    c = k.c
    c.save(); c.translate(hx, hy - 44 * s); c.scale(s, s)
    cut(k, [(-50, 0), (-60, -30), (-44, -44), (44, -44), (60, -30), (50, 0)], CAP_WHITE, shadow=False, lw=2.4)   # the top
    cut(k, [(-50, 0), (50, 0), (50, 16), (-50, 16)], CAP_BAND, shadow=False, lw=2.2)                              # the band
    c.move_to(-46, 14); c.curve_to(-26, 34, 26, 34, 46, 14); c.close_path()                                        # the visor
    c.set_source_rgb(0.04, 0.04, 0.06); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.2); c.stroke()
    c.move_to(0, -28); c.line_to(11, -22); c.line_to(10, -8); c.line_to(0, -1); c.line_to(-10, -8); c.line_to(-11, -22)
    c.close_path(); c.set_source_rgb(*SILVER); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.6); c.stroke()
    c.restore()


def shield(c, x, y, r):
    """the metal badge on his vest (no star: it read as 'a star he's holding')."""
    c.save(); c.translate(x, y); c.scale(r / 44, r / 44)
    c.move_to(0, -22); c.line_to(18, -14); c.line_to(16, 8); c.line_to(0, 22); c.line_to(-16, 8); c.line_to(-18, -14); c.close_path()
    c.set_source_rgb(*SILVER); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2); c.stroke()
    c.restore()


def paddle(k, x, y, s, side="STOP", ang=0.0):
    """The comic prop: a round STOP / GO paddle on a short pole, (x, y) = the grip. STOP is the series' neon red, so it
    stays red in the noir grade; GO is green (grey in the grade, the white letters carry it)."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    c.set_source_rgb(*INK); c.set_line_width(9); c.move_to(0, 10); c.line_to(0, -96); c.stroke()
    c.set_source_rgb(0.85, 0.85, 0.86); c.set_line_width(5); c.move_to(0, 10); c.line_to(0, -96); c.stroke()
    if side == "EDGE":                                                # mid-flip: the disc edge-on, a thin ellipse
        c.save(); c.translate(0, -134); c.scale(7, 44); c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        c.set_source_rgb(0.85, 0.85, 0.86); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(3); c.stroke()
        for dx in (-26, 26):                                          # two short turn arcs
            c.new_path(); c.arc(0, -134, 52, math.pi * (1.15 if dx < 0 else -0.15), math.pi * (1.4 if dx < 0 else 0.1))
            c.set_line_width(3); c.stroke()
        c.restore()
        return
    c.new_path(); c.arc(0, -134, 44, 0, 2 * math.pi)
    c.set_source_rgb(*(NEON if side == "STOP" else GO_GREEN)); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(3); c.stroke()
    c.new_path(); c.arc(0, -134, 37, 0, 2 * math.pi); c.set_source_rgb(1, 1, 1); c.set_line_width(3); c.stroke()
    kit.text(k, side, 0, -134 + 9, 24 if side == "STOP" else 30, (1, 1, 1), bold=True)
    c.restore()


def don_cop2(k, x, feet, s=0.60, pose="stop", face="neutral", look=(0, 0), whistle_in=False, paddle_side=None, paddle_ang=0.0,
             chin=0, grip=True):
    """v4 Don the traffic cop (opt-in; don_cop is untouched): the cap, the silver shield, white gloves, the whistle on its
    cord (in his mouth on the toot), and the STOP / GO paddle in his screen-right hand."""
    c = k.c
    p, hands = DON_POSES.get(pose, (pose, None))
    if paddle_side and grip:                                          # v4b: with the paddle the hand is a grip, always
        hands = ((hands or ("relax", "relax"))[0], "grab")
    import fs_storyboard as sb_
    def body():                                                       # no headset in the dream (Office Noir took it off too);
        with _swap((hp, "hand", _wrap_white(hp.hand)), (sb_, "don_signs", lambda *a, **kw: None)):   # the cap covers his hair
            return don_ps.don(k, x, feet, s, p, face, look, hands=hands, chin=chin)
    o = None
    if paddle_side:                                                   # find the hand, lay the paddle there, draw him over it
        c.push_group(); o = body(); c.pop_group()
        rx, ry = o["hands"][1]
        paddle(k, rx, ry, s * 1.1, paddle_side, paddle_ang)
    o = body()
    hx, hy = o["head"]
    shield(c, hx - 26 * s, hy + 112 * s, 18 * s)
    c.set_source_rgb(0.30, 0.30, 0.32); c.set_line_width(2.4 * s)
    if whistle_in:                                                    # v4b: the toot reads: the cord runs to his chest, the
        c.set_line_width(3 * s)                                       # whistle big, cheeks puffed, two toot lines
        c.move_to(hx + 4 * s, hy + 36 * s); c.curve_to(hx + 2 * s, hy + 70 * s, hx - 10 * s, hy + 100 * s, hx - 18 * s, hy + 120 * s); c.stroke()
        whistle(c, hx + 8 * s, hy + 33 * s, s * 1.9)
        c.set_source_rgb(*INK); c.set_line_width(2.4 * s)
        for sx in (-1, 1):
            c.new_path(); c.arc(hx + sx * 30 * s, hy + 26 * s, 9 * s, -0.6 if sx > 0 else math.pi - 0.6, 0.6 if sx > 0 else math.pi + 0.6); c.stroke()
        c.set_line_width(3 * s)
        for dy in (-10, 6):
            c.move_to(hx + 36 * s, hy + (30 + dy) * s); c.line_to(hx + 58 * s, hy + (24 + dy * 1.6) * s); c.stroke()
    else:
        c.move_to(hx - 18 * s, hy + 80 * s); c.curve_to(hx - 10 * s, hy + 120 * s, hx + 6 * s, hy + 130 * s, hx + 14 * s, hy + 132 * s); c.stroke()
        whistle(c, hx + 18 * s, hy + 134 * s, s)
    traffic_cap(k, hx, hy, s)
    return o


def don_sheet(out="../office-noir-4/on4_don_v5.png"):
    """Don v4b, the paddle's choreography for 3.1-3.3: STOP raised to Pam's side, the flip (edge-on), GO raised to the car
    with the toot, GO lowered at rest. One grip point; the faces stern, pleased, bored; his eyes on the car throughout
    (nobody looks at her). In the sheet Pam is to his right (the paddle's side) and the car to his left."""
    W_, H_ = 4 * 300 + 40, 660
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W_ * 2, H_ * 2); s.set_device_scale(2, 2)
    c = cairo.Context(s); k = Ctx(c, 0)
    c.set_source_rgb(0.58, 0.58, 0.60); c.paint()
    labs = [("1 STOP at Pam's side", "stern; eyes on the car", dict(pose="stop", paddle_side="STOP", face="confused", chin=1, look=(-0.8, 0))),
            ("2 the flip", "edge-on, one drawing", dict(pose=(-8, 0, 92, -40), paddle_side="EDGE", face="confused", chin=1, look=(-0.8, 0))),
            ("3 GO to the car", "the toot; pleased", dict(pose="wave", paddle_side="GO", paddle_ang=0.25, whistle_in=True, face="pleased", look=(-0.8, -0.2))),
            ("4 GO at rest", "bored: 'Not a scratch.'", dict(pose="stand", paddle_side="GO", paddle_ang=0.55, face="neutral", look=(-0.7, 0.4)))]
    for i, (lab, sub, kw) in enumerate(labs):
        don_cop2(k, 150 + i * 300, 610, 0.95, **kw)
    eng.TONE = "v3"; eng.accent_pass(s, [(NEON, 1.0)])
    c = cairo.Context(s); c.set_source_rgb(0, 0, 0); c.select_font_face("Inter", 0, 1)
    for i, (lab, sub, kw) in enumerate(labs):
        c.set_font_size(18); c.move_to(20 + i * 300, 30); c.show_text(lab)
        c.select_font_face("Inter", 0, 0); c.set_font_size(14); c.move_to(20 + i * 300, 50); c.show_text(sub); c.select_font_face("Inter", 0, 1)
    c.set_font_size(15); c.move_to(20, 646); c.show_text("<- the car (his eyes)")
    c.move_to(W_ - 220, 646); c.show_text("Pam (the paddle's side) ->")
    s.write_to_png(out)
    return out


def _wrap_white(orig):
    def h(k, hx, hy, w, skin, seed, d, side):
        return orig(k, hx, hy, w, GLOVE_WHITE, seed, d, side)
    return h


# ---- the sheet ------------------------------------------------------------------------------------------------------

WALL_GREY = (0.78, 0.76, 0.70)


def _panel(draw, w=300, h=520, grade=True, bg=WALL_GREY, scale=2):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, w * scale, h * scale); s.set_device_scale(scale, scale)
    c = cairo.Context(s); c.set_source_rgb(*bg); c.paint()
    c.set_source_rgb(bg[0] * 0.75, bg[1] * 0.75, bg[2] * 0.75); c.rectangle(0, h - 60, w, 60); c.fill()
    draw(Ctx(c, 0), w, h)
    if grade:
        eng.TONE = "v3"; eng.accent_pass(s, [])
    return s


def sheet(out="../office-noir-4/on4_cast_sheet_v2.png", phone_out="../office-noir-4/on4_cast_phone_v2.png"):
    S = 0.95
    rows = [
        ("THE LOOKS: series beside the episode's costume (in colour, before the grade)", [
            (lambda k, w, h: pm_ps.pam(k, w / 2, h - 60, S, "stand", "neutral", mug=False), "Pam, series (ep 14)", False),
            (lambda k, w, h: pam_cat(k, w / 2, h - 60, S, "sag", "neutral"), "PAM-CAT", False),
            (lambda k, w, h: pam_awake(k, w / 2, h - 60, S, "down"), "awake 7.1: sleep mask down", False),
            (lambda k, w, h: pam_awake(k, w / 2, h - 60, S, "up", "doubt"), "awake 7.3: pushed up", False),
            (lambda k, w, h: don_ps.don(k, w / 2, h - 60, S * 1.1, "stand", "neutral"), "Don, series (ep 14)", False),
            (lambda k, w, h: don_cop(k, w / 2 - 30, h - 60, S * 1.1, "stop", "neutral"), "DON, cop: the whistle, a glove out", False)]),
        ("PAM-CAT IN THE DREAM: the film's poses, through the noir grade", [
            (lambda k, w, h: pam_cat(k, w / 2, h - 60, S, "hero", "proud", (-0.8, -0.2)), "1.1 hero pose, eyes back", True),
            (lambda k, w, h: pam_cat(k, w / 2, h - 60, S, "sag", "hurt", (-0.6, 0.6)), "1.3 the pose sags", True),
            (lambda k, w, h: pam_cat(k, w / 2, h - 60, S, "sag", "peer", (0, 0.8)), "2.4 eyes narrow", True),
            (lambda k, w, h: pam_cat(k, w / 2, h - 60, S, "point_up", "hopeful", (0.4, -0.8)), "4.3 points at the sign", True),
            (lambda k, w, h: pam_cat(k, w / 2, h - 60, S, "point_me", "happy"), "4.3 then at herself", True),
            (lambda k, w, h: pam_cat(k, w / 2, h - 60, S, "triumph", "proud", (0, -0.4)), "6.3 the envelope high", True)]),
    ]
    PW, PH, G = 300, 520, 20
    W_ = G + 6 * (PW + G); H_ = 80 + len(rows) * (PH + 90) + 20
    sh = cairo.ImageSurface(cairo.FORMAT_RGB24, W_, H_); c = cairo.Context(sh)
    c.set_source_rgb(0.93, 0.92, 0.89); c.paint()
    c.set_source_rgb(0.1, 0.1, 0.1); c.select_font_face("Inter", 0, 1); c.set_font_size(28)
    c.move_to(G, 44); c.show_text("OFFICE NOIR 4 · the cast's looks · v2 (after the audit: mask, slump, points, envelope in the fist, the cop by his job)")
    y = 80
    phone_panels = []
    for title, items in rows:
        c.set_source_rgb(0.1, 0.1, 0.1); c.select_font_face("Inter", 0, 1); c.set_font_size(19)
        c.move_to(G, y + 18); c.show_text(title)
        x = G
        for fn, lab, grade in items:
            p = _panel(fn, PW, PH, grade, WALL_GREY if grade else (0.92, 0.90, 0.85))
            c.set_source_surface(p, x, y + 30); c.paint()
            c.set_source_rgb(0.1, 0.1, 0.1); c.select_font_face("Inter", 0, 0); c.set_font_size(16)
            c.move_to(x, y + 30 + PH + 22); c.show_text(lab)
            phone_panels.append(p)
            x += PW + G
        y += PH + 90
    sh.write_to_png(out)
    # phone check: Pam-Cat and Don at the film's size (Pam 0.54, Don 0.60 in a 540 frame) shown at 270 px wide
    ph = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960); c = cairo.Context(ph)
    c.set_source_rgb(*WALL_GREY); c.paint()
    k = Ctx(c, 0)
    pam_cat(k, 130, 700, 0.80, "hero", "proud", (0.6, 0))                 # 1.1, wide: Pam-Cat in the foreground
    don_cop(k, 390, 700, 0.80, "stop", "neutral")                       # 3.3, Don at the same size
    c.save(); c.rectangle(0, 0, 540, 360); c.clip()
    pam_cat(k, 270, 800, 2.2, "sag", "hurt", (-0.6, 0.6))                 # 1.3, the close-up: is the face readable?
    c.restore()
    eng.TONE = "v3"; eng.accent_pass(ph, [])
    small = cairo.ImageSurface(cairo.FORMAT_RGB24, 270, 480); c2 = cairo.Context(small)
    c2.scale(0.5, 0.5); c2.set_source_surface(ph, 0, 0); c2.paint()
    small.write_to_png(phone_out)
    return out


if __name__ == "__main__":
    print(sheet())
