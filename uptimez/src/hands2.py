"""Hands with fingers for UptimeZ (23 Nov, Tomas: "the hands are bad everywhere").

From the lessons: a hand always comes out of a sleeve, and the sleeve from a body or the frame's edge (71, 245);
an insert shows the owner's sleeve (58); an idle hand is a palm and a thumb, no finger rods (Office Noir 3 v8);
a held prop sits where the hand is (70, 399). Drawn like cast_on3._open_hand (Office Noir 3): fingers as rounded
strokes with an ink edge, the palm over their roots; here with poses and any skin colour.

hand(k, x, y, ang, w, skin, pose, side) — the wrist at (x, y), the hand pointing along ang; w: the forearm's width
(the hand scales with it); side: +1/-1 which side the thumb is on (mirror for the other hand).
poses: "open" (four fingers out), "point" (the index out, the rest curled), "press" (a fist, the thumb out, pressing),
       "grip" (curled round something: knuckles in front, the thumb along the top), "relax" (palm and thumb).
arm(k, x0, y0, x1, y1, w, sleeve_col, skin, cuff=None, pose=..., side=...) — a sleeve from (x0, y0) (off frame or a
shoulder) to the wrist at (x1, y1), a cuff, and the hand at the wrist pointing on along the arm."""
import math
import kit

INK = (0.13, 0.11, 0.12)


def _cap(c, x0, y0, x1, y1, wd, skin, edge=2.2):
    c.set_line_cap(1)
    c.set_source_rgb(*INK); c.set_line_width(wd + 2 * edge); c.new_path(); c.move_to(x0, y0); c.line_to(x1, y1); c.stroke()
    c.set_source_rgb(*skin); c.set_line_width(wd); c.new_path(); c.move_to(x0, y0); c.line_to(x1, y1); c.stroke()
    c.set_line_cap(0)


def hand(k, x, y, ang, w, skin, pose="open", side=1, seed=0, nail=True):
    c = k.c
    u = w                                                   # one forearm width
    e = max(1.4, u * 0.045)
    c.save(); c.translate(x, y); c.rotate(ang)
    fw = u * 0.22                                           # a finger's width
    rows = [-0.30, -0.10, 0.10, 0.30]                       # across the hand, index first on the thumb's side
    if side < 0:
        rows = rows[::-1]
    rows = [r * -1 for r in rows]                           # the index on the thumb's side (thumb at +side)
    if pose == "relax":
        _cap(c, u * 0.28, side * u * 0.30, u * 0.58, side * u * 0.50, fw * 1.05, skin, e)            # the thumb
        kit.ellipse(k, u * 0.42, 0, u * 0.44, u * 0.40, skin, seed, shadow=False, lw=e * 1.1)
        c.set_source_rgb(*INK); c.set_line_width(e * 0.7)                                          # the fingers' lines
        for r in (-0.13, 0.04, 0.2):
            c.new_path(); c.move_to(u * 0.66, r * u); c.line_to(u * 0.84, r * u * 1.1); c.stroke()
        c.restore(); return
    lens = {"open": (0.62, 0.70, 0.66, 0.52), "point": (0.78, 0.16, 0.16, 0.14), "press": (0.15, 0.15, 0.14, 0.12),
            "grip": (0.20, 0.22, 0.21, 0.18)}[pose]
    idx_row = side * 0.30
    order = sorted([-0.30, -0.10, 0.10, 0.30], key=lambda r: -r * side)   # index (thumb side) first
    for i, r in enumerate(order):
        L = lens[i] * u
        spread = (r * 0.18) if pose == "open" else 0.0
        x0, y0 = u * 0.62, r * u * 0.92
        x1, y1 = x0 + L * math.cos(spread), y0 + L * math.sin(spread)
        _cap(c, x0, y0, x1, y1, fw, skin, e)
        if nail and L > 0.4 * u:
            c.set_source_rgb(min(1, skin[0] + 0.06), min(1, skin[1] + 0.08), min(1, skin[2] + 0.10))
            c.new_path(); c.arc(x1 - fw * 0.1, y1, fw * 0.26, 0, 2 * math.pi); c.fill()
    if pose in ("grip", "press"):                           # the curled fingers' knuckles: a row of bumps in front
        for r in order:
            kit.ellipse(k, u * 0.80, r * u * 0.92, fw * 0.62, fw * 0.55, skin, seed + int(r * 100), shadow=False, lw=e)
    kit.ellipse(k, u * 0.42, 0, u * 0.44, u * 0.42, skin, seed + 7, shadow=False, lw=e * 1.1)      # the palm, over the roots
    if pose == "press":                                     # the thumb straight out ahead, pressing
        _cap(c, u * 0.40, side * u * 0.32, u * 1.08, side * u * 0.20, fw * 1.25, skin, e)
        if nail:
            c.set_source_rgb(min(1, skin[0] + 0.06), min(1, skin[1] + 0.08), min(1, skin[2] + 0.10))
            c.new_path(); c.arc(u * 1.02, side * u * 0.20, fw * 0.34, 0, 2 * math.pi); c.fill()
    elif pose == "grip":
        _cap(c, u * 0.30, side * u * 0.38, u * 0.72, side * u * 0.46, fw * 1.15, skin, e)
    else:
        _cap(c, u * 0.30, side * u * 0.36, u * 0.62, side * u * 0.62, fw * 1.15, skin, e)
    c.restore()


def arm(k, x0, y0, x1, y1, w, sleeve_col, skin, cuff=None, pose="open", side=1, seed=0, taper=0.86, bunch=False):
    """A sleeve from (x0, y0) to the wrist (x1, y1), a cuff or a bunched edge, then the hand on along the arm."""
    c = k.c
    ang = math.atan2(y1 - y0, x1 - x0); L = math.hypot(x1 - x0, y1 - y0)
    c.save(); c.translate(x0, y0); c.rotate(ang)
    kit.cut(k, [(-4, -w / 2), (L, -w * taper / 2), (L, w * taper / 2), (-4, w / 2)], sleeve_col, shadow=False, lw=max(2, w * 0.03))
    if cuff:
        kit.rect(k, L - w * 0.16, -w * taper / 2 - 2, w * 0.18, w * taper + 4, cuff, seed + 1, shadow=False, lw=max(1.6, w * 0.025))
    elif bunch:
        c.set_source_rgb(*INK); c.set_line_width(max(1.4, w * 0.02))
        for i in range(3):
            xx = L - 4 - i * w * 0.11
            c.new_path(); c.move_to(xx, -w * taper / 2 + 3); c.curve_to(xx + 4, -w / 6, xx + 4, w / 6, xx, w * taper / 2 - 3); c.stroke()
    c.restore()
    hand(k, x1 + math.cos(ang) * (-w * 0.04), y1 + math.sin(ang) * (-w * 0.04), ang, w * taper * 1.22, skin, pose, side, seed + 3)


ON = [False]                                               # opt-in: the films switch these hands on
