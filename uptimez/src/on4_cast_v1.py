"""OFFICE NOIR 4: the cast's looks, v1 (23 Nov). Stage 3 (look and set). Costumes on the series' rigs, never redesigns
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

COAT = (0.17, 0.16, 0.18)
COAT_DARK = (0.08, 0.08, 0.09)
COLLAR = (0.26, 0.25, 0.27)
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
    "sag": ((-6, 0, 6, 0), ("relax_s", "relax_s")),                                # 1.3 the pose let go
    "point_up": ((-8, 0) + pm.ik(1, 46, HY - 70), ("relax_s", "point")),           # 4.3 at the sign
    "point_me": ((-8, 0) + pm.ik(1, 6, BT + 36), ("relax_s", "point")),            # 4.3 then at herself
    "lift": ((-8, 0) + pm.ik(1, 110, BT + 96), ("relax_s", "grab")),               # 5.3 the hand into his coat
    "triumph": ((-8, 0) + pm.ik(1, 26, HY - 96), ("relax_s", "fist")),             # 6.3 the envelope held high
}


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
    """A narrow cat-eye mask over the bridge, flicked up at the outer corners. Its holes are large: the eyes and the
    brows (about 3 above the eyes' top) show through. Eyes at (+-17, +4) in head units."""
    c = k.c
    c.save(); c.translate(hx, hy); c.scale(s, s)
    c.new_path()
    c.move_to(-46, -16); c.curve_to(-30, -18, -10, -16, 0, -9); c.curve_to(10, -16, 30, -18, 46, -16)
    c.curve_to(44, -2, 40, 16, 30, 20); c.curve_to(18, 22, 6, 18, 0, 12); c.curve_to(-6, 18, -18, 22, -30, 20)
    c.curve_to(-40, 16, -44, -2, -46, -16); c.close_path()
    for sx in (-1, 1):                                   # the holes: wound the other way so they cut out
        c.new_sub_path(); c.save(); c.translate(sx * 18, 2); c.scale(15, 14); c.arc_negative(0, 0, 1, 2 * math.pi, 0); c.restore()
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


def envelope(k, x, y, s, open_=False):
    """The dream's envelope (the warm tone) held by its edge."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(-0.12); c.scale(s, s)
    cut(k, [(-30, -22), (30, -22), (30, 20), (-30, 20)], (0.93, 0.82, 0.58), shadow=False, lw=2)
    c.set_source_rgb(*INK); c.set_line_width(1.6); c.move_to(-30, -22); c.line_to(0, 2); c.line_to(30, -22); c.stroke()
    c.restore()


def pam_cat(k, x, feet, s=0.54, pose="hero", face="proud", look=(0, 0), seed=40, env=False):
    """Pam-Cat. Returns the rig's points."""
    p, gest = CAT_POSES.get(pose, (pose, ("relax_s", "relax_s")))
    with _swap((kit.PEOPLE["PAM"], "body", COAT), (pm, "PURPLE", COAT), (pm, "PURPLE_DARK", COAT_DARK),
               (px, "TROUSERS", SUIT_LEG), (px, "TROUSERS_DARK", SUIT_LEG_DARK), (px, "TRAINER", BOOT),
               (kit.HAND, 0, _gloved(GLOVE_DARK)), (pm, "_costume", _coat_costume)):
        hp.reset(*gest)
        o = pb.pam(k, x, feet, s, p, face, look, seed, glasses="off", brooch=False, badge=False)
        coat_details(k, x, feet, s)
        hp.redraw_late(k)
    hx, hy = o["head"]
    ears(k, hx, hy, s)
    half_mask(k, hx, hy, s)
    if env or pose == "triumph":
        rx, ry = o["hands"][1]
        envelope(k, rx + 4 * s, ry - 40 * s, s * 1.2)
        with _swap((kit.HAND, 0, _gloved(GLOVE_DARK))):
            hp.redraw_late(k)
    return o


def sleep_mask(k, hx, hy, s, up=False):
    """The real twin: a pink sleep mask with two small cat ears, over the eyes (asleep) or pushed up (awake)."""
    c = k.c
    dy = -30 if up else 3
    c.save(); c.translate(hx, hy + dy); c.scale(s, s)
    c.set_source_rgb(*SLEEP_DARK); c.set_line_width(3)
    c.move_to(-46, -2); c.line_to(-58, -6); c.stroke(); c.move_to(46, -2); c.line_to(58, -6); c.stroke()
    cut(k, [(-46, -14), (46, -14), (44, 12), (8, 16), (0, 10), (-8, 16), (-44, 12)], SLEEP, shadow=False, lw=2)
    if not up:                                           # closed eyes stitched on it, asleep
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


DON_POSES = {"wave": "stand", "bumper": "stand"}


def don_cop(k, x, feet, s=0.60, pose="stand", face="neutral", look=(0, 0), hands=None):
    """Don the traffic cop: no cap; a star badge on the vest, a whistle on a cord, white gloves."""
    with _swap((hp, "hand", _wrap_white(hp.hand))):
        o = don_ps.don(k, x, feet, s, pose, face, look, hands=hands)
    hx, hy = o["head"]
    c = k.c
    # a white crossbelt over the vest, shoulder to hip: what says "traffic cop" with no cap (lesson: a role reads in 1 s)
    c.set_source_rgb(*INK); c.set_line_width(13 * s); c.set_line_cap(0)
    c.move_to(hx + 40 * s, hy + 66 * s); c.line_to(hx - 34 * s, hy + 196 * s); c.stroke()
    c.set_source_rgb(*GLOVE_WHITE); c.set_line_width(10 * s)
    c.move_to(hx + 40 * s, hy + 66 * s); c.line_to(hx - 34 * s, hy + 196 * s); c.stroke()
    c.set_source_rgb(0.30, 0.30, 0.32); c.set_line_width(1.6 * s / 0.6)
    c.move_to(hx - 18 * s, hy + 80 * s); c.curve_to(hx - 10 * s, hy + 120 * s, hx + 6 * s, hy + 130 * s, hx + 14 * s, hy + 132 * s); c.stroke()
    whistle(c, hx + 18 * s, hy + 134 * s, s)
    star(c, hx - 44 * s, hy + 104 * s, 17 * s)
    return o


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


def sheet(out="../office-noir-4/on4_cast_sheet_v1.png", phone_out="../office-noir-4/on4_cast_phone_v1.png"):
    S = 0.95
    rows = [
        ("THE LOOKS: series beside the episode's costume (in colour, before the grade)", [
            (lambda k, w, h: pm_ps.pam(k, w / 2, h - 60, S, "stand", "neutral", mug=False), "Pam, series (ep 14)", False),
            (lambda k, w, h: pam_cat(k, w / 2, h - 60, S, "sag", "neutral"), "PAM-CAT", False),
            (lambda k, w, h: pam_awake(k, w / 2, h - 60, S, "down"), "awake 7.1: sleep mask down", False),
            (lambda k, w, h: pam_awake(k, w / 2, h - 60, S, "up", "doubt"), "awake 7.3: pushed up", False),
            (lambda k, w, h: don_ps.don(k, w / 2, h - 60, S * 1.1, "stand", "neutral"), "Don, series (ep 14)", False),
            (lambda k, w, h: don_cop(k, w / 2, h - 60, S * 1.1, "stand", "neutral"), "DON, cop: no cap", False)]),
        ("PAM-CAT IN THE DREAM: the film's poses, through the noir grade", [
            (lambda k, w, h: pam_cat(k, w / 2, h - 60, S, "hero", "proud", (-0.8, -0.2)), "1.1 hero pose, eyes back", True),
            (lambda k, w, h: pam_cat(k, w / 2, h - 60, S, "sag", "fade", (-0.8, 0)), "1.3 the pose sags", True),
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
    c.move_to(G, 44); c.show_text("OFFICE NOIR 4 · the cast's looks · v1 (costumes on the series rigs)")
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
    don_cop(k, 400, 700, 0.80, "stand", "neutral")                       # 3.3, Don at the same size
    c.save(); c.rectangle(0, 0, 540, 360); c.clip()
    pam_cat(k, 270, 800, 2.2, "sag", "fade", (-0.8, 0))                 # 1.3, the close-up: is the face readable?
    c.restore()
    eng.TONE = "v3"; eng.accent_pass(ph, [])
    small = cairo.ImageSurface(cairo.FORMAT_RGB24, 270, 480); c2 = cairo.Context(small)
    c2.scale(0.5, 0.5); c2.set_source_surface(ph, 0, 0); c2.paint()
    small.write_to_png(phone_out)
    return out


if __name__ == "__main__":
    print(sheet())
