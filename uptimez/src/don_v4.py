"""DON v4: the next-film costume. Same head, height and face as before (kit.PEOPLE["DON"]); the
costume is new:
- an open navy fleece vest (company swag: small UptimeZ mark on the chest, stand-up collar, zip tape),
- a white shirt underneath, no tie, sleeves are the shirt,
- khaki trousers with a belt,
- a ketchup stain on the shirt, always there, never mentioned: a bottle squiggle, a smear and a dot,
- the staff badge from the Day One storyboards, clipped to the vest.
Draws through kit.person with kit.BADGE_HOOK (drawn after the body, before the arms), so the older
DON and every older episode are untouched.
Usage: p = don(k, x, feet, s, pose="stand", face="neutral", look=(0, 0), seed=500, badge=True, stain=True)"""
import math
import kit
import brand
from kit import INK, cut, rect, ellipse

SHIRT = (0.97, 0.97, 0.95)
VEST = (0.14, 0.20, 0.33)
VEST_SHADE = (0.10, 0.15, 0.26)
ZIP = (0.62, 0.64, 0.68)
KHAKI = (0.78, 0.70, 0.52)
BELT = (0.30, 0.20, 0.12)
KETCHUP = (0.90, 0.22, 0.08)      # tomato red, warmer than blood
KETCHUP_DARK = (0.66, 0.12, 0.04)


def staff_badge(k, name, x0, y0, w=38, size=10.5):
    """The Day One company badge: clip, white card, green band with the logo mark, name."""
    c = k.c
    rect(k, x0 + w / 2 - 6, y0 - 5, 12, 7, (0.45, 0.47, 0.52), 1701, shadow=False, lw=1.3)
    rect(k, x0, y0, w, 27, (1, 1, 1), 1700 + len(name), shadow=False, lw=1.6)
    c.set_source_rgb(*brand.GREEN); c.rectangle(x0 + 1.5, y0 + 1.5, w - 3, 8); c.fill()
    brand.mark(c, x0 + 3, y0 + 2, 7, zzz=False)
    kit.text(k, name, x0 + w / 2, y0 + 18.5, size, INK)


def ketchup(k, x, y, seed=0):
    """A ketchup squiggle (the shape a squeeze bottle leaves) plus a small smear and a dot: reads as a
    condiment, not a wound (a dark round blob with a drip did, in the first try)."""
    c = k.c
    c.set_line_cap(1); c.set_line_join(1)
    c.move_to(x - 10, y)
    for i in range(4):                                   # four bumps, slightly diagonal
        x0 = x - 10 + i * 5.5
        c.curve_to(x0 + 1.5, y - 7 - i * 1.2, x0 + 4, y - 7 - i * 1.2, x0 + 5.5, y - i * 1.2)
    c.set_source_rgb(*KETCHUP_DARK); c.set_line_width(6.2); c.stroke_preserve()
    c.set_source_rgb(*KETCHUP); c.set_line_width(4.2); c.stroke()
    c.save(); c.translate(x + 9, y + 9); c.rotate(-0.5); c.scale(5, 2.2)       # smear where he rubbed it
    c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    c.set_source_rgba(*KETCHUP, 0.8); c.fill()
    c.set_source_rgb(*KETCHUP); c.arc(x - 9, y + 8, 1.8, 0, 2 * math.pi); c.fill()
    c.set_source_rgba(1, 1, 1, 0.8); c.arc(x - 3, y - 6, 1.1, 0, 2 * math.pi); c.fill()   # wet shine


def _costume(stain, badge, name="DON"):
    def hook(k, name_, p, body_top, seed):
        c = k.c
        bt = body_top
        waist = bt + 150
        # trousers and belt below the vest
        cut(k, [(-45, waist), (45, waist), (47, 0), (-47, 0)], KHAKI, shadow=False, lw=2)
        c.set_source_rgb(*INK); c.set_line_width(1.6)
        c.move_to(0, waist + 14); c.line_to(0, -4); c.stroke()
        rect(k, -45, waist - 6, 90, 12, BELT, seed + 61, shadow=False, lw=1.6)
        rect(k, -7, waist - 8, 14, 16, ZIP, seed + 62, shadow=False, lw=1.4)
        # shirt collar points at the neck
        for sx in (-1, 1):
            cut(k, [(0, bt + 2), (sx * 16, bt - 2), (sx * 12, bt + 16)], SHIRT, shadow=False, lw=1.6)
        if stain:
            ketchup(k, 0, bt + 92, seed + 70)
        # open vest: two panels leaving a strip of shirt down the middle
        for sx in (-1, 1):
            panel = [(sx * 11, bt + 4), (sx * 40, bt), (sx * 44, waist + 2), (sx * 15, waist + 2)]
            cut(k, panel, VEST, shadow=False, lw=2)
            c.set_source_rgb(*ZIP); c.set_line_width(2.6)                               # zip tape on the edge
            c.move_to(sx * 13, bt + 10); c.line_to(sx * 16.5, waist); c.stroke()
            c.set_source_rgb(*VEST_SHADE); c.set_line_width(2.2)                        # fleece texture seam
            c.move_to(sx * 33, bt + 30); c.curve_to(sx * 30, bt + 70, sx * 34, bt + 110, sx * 32, waist - 6); c.stroke()
            cut(k, [(sx * 9, bt - 6), (sx * 28, bt - 4), (sx * 30, bt + 10), (sx * 12, bt + 10)], VEST,
                shadow=False, lw=1.8)                                                      # stand-up collar
        c.set_source_rgb(*ZIP)                                                             # zip pull, hanging open
        c.rectangle(-17, bt + 12, 4, 9); c.fill()
        brand.mark(c, -36, bt + 30, 12, zzz=False)                                        # embroidered company mark
        if badge:
            staff_badge(k, name, 14, bt + 34, 29, 8)
    return hook


def _face_wrap(orig, chin):
    """Extra faces for the next film without touching kit: "grin" (open eyes + smile, for the thumbs-up)
    and chin > 0 (features lifted: chin up, for "flattered")."""
    def face_draw(k, x, y, face, look, glasses=False, seed=0):
        y2 = y - 7 * chin
        if face == "grin":
            orig(k, x, y2, "neutral", look, glasses=glasses, seed=seed)
            c = k.c
            ellipse(k, x + 1, y2 + 26, 19, 9, kit.PEOPLE["DON"]["skin"], seed + 90, shadow=False, outline=False)
            c.set_source_rgb(*INK); c.set_line_width(4); c.set_line_cap(1)
            c.arc(x, y2 + 14, 15, 0.2 * math.pi, 0.8 * math.pi); c.stroke()
        else:
            orig(k, x, y2, face, look, glasses=glasses, seed=seed)
    return face_draw


def don(k, x, feet, s=1.0, pose="stand", face="neutral", look=(0, 0), seed=500, badge=True, stain=True, chin=0):
    old_p = dict(kit.PEOPLE["DON"])
    old_hook = kit.BADGE_HOOK
    old_face = kit.face_draw
    if face == "grin" or chin:
        kit.face_draw = _face_wrap(old_face, chin)
    p = dict(old_p); p["body"] = SHIRT; p.pop("tie", None)
    kit.PEOPLE["DON"] = p
    kit.BADGE_HOOK = _costume(stain, badge)
    try:
        return kit.person(k, "DON", x, feet, s, pose=pose, face=face, seed=seed, look=look, badge=True)
    finally:
        kit.PEOPLE["DON"] = old_p
        kit.BADGE_HOOK = old_hook
        kit.face_draw = old_face


# ---------------------------------------------------------------- "I Will Replace You" additions
POSE_THUMB = (-8, 0, 40, 120)      # right forearm up in front, ready for a thumbs-up
POSE_WRENCH = (-8, 0, 128, 28)     # right hand raised, holding up the greasy wrench
POSE_CHEST = (-8, 0, -30, -125)    # flattered: right hand on his chest (draw with chin=1)


def thumbs_up(k, hand, s=1.0, seed=520):
    """A fist with the thumb up, drawn over the hand point returned by don()."""
    c = k.c
    hx, hy = hand
    skin = kit.PEOPLE["DON"]["skin"]
    c.save(); c.translate(hx, hy); c.scale(s, s)
    rect(k, -10, -9, 20, 18, skin, seed, shadow=False, lw=2)
    c.set_source_rgb(*INK); c.set_line_width(1.4)
    for yy in (-3, 3):
        c.move_to(-9, yy); c.line_to(4, yy); c.stroke()
    rect(k, -4, -26, 8, 18, skin, seed + 1, shadow=False, lw=2)
    c.restore()

