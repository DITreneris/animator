"""ONE STAR v20 (26 Nov, Tomas: "elbows, hands, fingers ****: frame by frame, what is OK, what is bad"; the audit and
the review's picks). Opt-in through install(); v19 rebuilds as before. Rules: docs/rules-hands-and-phones.md.
- 4.3s the 7 over his shoulder (224, 225: the owner in the shot, both bones, the elbow inside the frame): the back of his
  head and his shoulders (fs_film31.client_back), his own arm up from the shoulder, the strip's face to him and to us;
  his thumb across its front below the 7, his fingertips round its far edge (review 02). v19: a long olive sleeve
  from the bottom edge to mid-frame, a fist over half the 7 ("a tube", "capsules").
"""
import math
import cairo
import kit
import cs_scene1 as s1
import cs_scene4 as s4
import cs_props as cp
import fs_storyboard as sb

INK = (0.13, 0.12, 0.14)
WALL = (0.91, 0.86, 0.75)


def _taper(k, a, b, wa, wb, col, lw=4.0):
    """A limb part from a to b, wa wide at a, wb at b, round ends: the outline first, then the fill."""
    c = k.c
    (ax, ay), (bx, by) = a, b
    th = math.atan2(by - ay, bx - ax)
    nx, ny = math.cos(th + math.pi / 2), math.sin(th + math.pi / 2)
    for pass_ in (0, 1):
        c.new_path()
        c.move_to(ax + nx * wa / 2, ay + ny * wa / 2); c.line_to(bx + nx * wb / 2, by + ny * wb / 2)
        c.arc_negative(bx, by, wb / 2, th + math.pi / 2, th - math.pi / 2)
        c.line_to(ax - nx * wa / 2, ay - ny * wa / 2)
        c.arc_negative(ax, ay, wa / 2, th - math.pi / 2, th - 1.5 * math.pi)
        c.close_path()
        if pass_ == 0:
            c.set_source_rgb(*INK); c.set_line_width(lw * 2); c.stroke()
        else:
            c.set_source_rgb(*col); c.fill()


def _ik(s, t, l1, l2, out=1):
    (sx, sy), (tx, ty) = s, t
    d = min(math.hypot(tx - sx, ty - sy), l1 + l2 - 1e-3)
    a = math.atan2(ty - sy, tx - sx)
    b = math.acos(max(-1, min(1, (l1 * l1 + d * d - l2 * l2) / (2 * l1 * d))))
    e = a - out * b
    return (sx + l1 * math.cos(e), sy + l1 * math.sin(e))


def s4_3s(k, d):
    """10 drawings (0.8 s), over his right shoulder: the strip up in his own hand, the 7 to him and to us."""
    import client_ob as co
    import fs_film31 as f31
    c = k.c
    v = co.LOOKS["B"]
    J, JD = v["jacket"], v["dark"]
    br_ = 2.5 * math.sin(2 * math.pi * d / float(s1.DPS) / 4.0)
    up = s1.ease(d / 4.0)                                                         # the strip comes up into view, then holds
    sb.bg(c, WALL)
    g = cairo.LinearGradient(0, 0, 0, 960); g.add_color_stop_rgba(0, 1, 1, 1, 0.10); g.add_color_stop_rgba(1, 0, 0, 0, 0.10)
    c.set_source(g); c.paint()
    c.set_source_rgb(0.36, 0.40, 0.47); c.rectangle(486, 0, 26, 960); c.fill()   # the glass door's post behind (his view)
    c.set_source_rgb(0.80, 0.88, 0.93); c.rectangle(512, 0, 40, 960); c.fill()
    S = 2.5
    hx0, feet = 150.0, 1700.0 + br_
    _back(k, hx0, feet, S)
    sh = (hx0 + 58 * S, feet + (co.BT + 14) * S)                                  # his right shoulder (screen right)
    hand = (352.0, 600.0 - 60 * up)
    el = _ik(sh, hand, 215.0, 205.0, out=-1)                                       # the elbow out to the right, in frame
    _taper(k, sh, el, 84, 64, J)                                                  # the upper arm, wider
    _taper(k, el, hand, 62, 46, J)                                                # the forearm, to a narrower wrist
    sk = co.SKIN
    ang = math.atan2(hand[1] - el[1], hand[0] - el[0])
    c.save(); c.translate(*hand); c.rotate(ang + math.pi / 2)
    s4.rect(k, -26, -6, 52, 16, (0.98, 0.97, 0.94), 775, shadow=False, lw=2.4)      # the shirt cuff at his wrist
    c.restore()
    # the strip, its face to him and to us, held by its foot: the hand behind it, the thumb in front
    cx, cy = hand[0] - 10, hand[1] - 250
    c.save(); c.translate(cx, cy); c.rotate(-0.07)
    for i, yy in enumerate((152, 180, 208)):                                       # three fingertips round its far edge
        _taper(k, (60, yy + 2), (96, yy - 2), 26, 24, sk, lw=2.2)
    _taper(k, (6, 266), (16, 206), 84, 76, sk, lw=2.6)                             # the back of his hand, under its foot
    s4.rect(k, -80, -230, 160, 450, s4.BLUE, 774, lw=4)
    c.set_source_rgb(*cp.RED); c.set_line_width(12); c.new_path(); c.arc(0, -70, 70, 0, 6.3); c.stroke()
    cp.T(c, "7", 0, -22, 136, col=(1, 1, 1))
    c.set_source_rgb(1, 1, 1); c.set_line_width(5); c.rectangle(-38, 40, 76, 56); c.stroke()
    for yy in (54, 68, 82):
        c.move_to(-38, yy); c.line_to(38, yy); c.stroke()
    _taper(k, (-20, 232), (-46, 150), 34, 28, sk, lw=2.6)                          # his thumb up its front, under the lines
    c.restore()


IN43A = [False]


def hold_front(k, skin, x0, y0, w, h, side=-1):
    """4.3a (v20): the strip's back to us, so his FINGERS are on our side: the heel of his hand past its right edge and
    three fingers across its foot, below the middle (v19: the series' fist round its foot, with his watch and the
    VISITOR badge, read as one lump; review 02: "fingers like joined ovals, the thumb lost")."""
    lw = 0.05 * w
    fh = 0.085 * h
    _taper(k, (x0 + w * 1.10, y0 + h * 0.86), (x0 + w * 0.95, y0 + h * 0.70), w * 0.62, w * 0.56, skin, lw=lw)   # the heel
    for i in range(3):
        yy = y0 + h * (0.64 + i * 0.105)
        _taper(k, (x0 + w * 1.02, yy), (x0 + w * 0.16 + i * w * 0.05, yy + 0.01 * h), fh, fh * 0.92, skin, lw=lw)


def _grip(k, skin, x0, y0, w, h, side=-1):
    if IN43A[0]:
        return hold_front(k, skin, x0, y0, w, h, side)
    return _OLD_GRIP[0](k, skin, x0, y0, w, h, side)


_OLD_GRIP = [None]


def pen52(k, px, py):
    """5.2 (v20, review 05: "the pen dominates, the hand is hardly there, the pen writes by itself"): a thinner pen
    (-25 %), her hand in a tripod you can read: the back of her hand above the pen, her index finger along its top to
    near the tip, her thumb pinching it from the near side; her purple sleeve and cuff out of the top edge."""
    import cs_grips as g
    c = k.c
    ux, uy = 0.62, -0.78                                                          # up the pen, from its tip
    nx, ny = -uy, ux                                                              # across it (toward her palm side)
    L = 150.0
    def at(t, o=0.0):
        return (px + ux * t + nx * o, py + uy * t + ny * o)
    sk = s4.SKIN_PAM
    wrist = at(150, 26)
    top = c.device_to_user(0, 0)[1]
    far = (wrist[0] + 0.55 * (wrist[1] - top + 60), top - 60)                      # the forearm, off the top edge
    _taper(k, far, wrist, 62, 50, s4.PURPLE, lw=3.0)                              # her sleeve
    _taper(k, at(150, 26), at(140, 22), 54, 52, g.PAM_CUFF, lw=2.6)               # its cuff
    _taper(k, at(124, 18), at(92, 10), 64, 54, sk, lw=2.6)                        # the back of her hand
    _taper(k, at(90, -6), at(58, -8), 20, 18, sk, lw=2.2)                         # the middle finger under the pen
    c.set_line_cap(1)
    c.set_source_rgb(*INK); c.set_line_width(11.0); c.move_to(*at(0)); c.line_to(*at(L)); c.stroke()
    c.set_source_rgb(*s5_pen()); c.set_line_width(7.5); c.move_to(*at(8)); c.line_to(*at(L)); c.stroke()
    c.set_source_rgb(0.85, 0.85, 0.88); c.set_line_width(7.5); c.move_to(*at(0)); c.line_to(*at(8)); c.stroke()   # its tip
    _taper(k, at(96, 10), at(34, 5), 22, 18, sk, lw=2.2)                          # the index finger along its top
    _taper(k, at(92, -20), at(40, -9), 26, 20, sk, lw=2.2)                        # the thumb, pinching from the near side


def s5_pen():
    import cs_scene5 as s5
    return s5.PEN


_OLD_PHONE = [None]


def _phone_in_claw(k, x, y, ang, s=1.0, lit=True, ghost=None):
    """cs_scene1_v14._phone, and when it is the robot's (the one call shape: ang -0.2, scale 1.25, its hand 10 below),
    the robot's claw round its foot: two grey prongs up its sides over the phone (v19: the phone sat on the end of its
    stick, "floating beside the hand"; rules 179, 208: a prop is held at the hand)."""
    _OLD_PHONE[0](k, x, y, ang, s, lit, ghost)
    if abs(ang + 0.2) > 1e-6 or abs(s - 1.25) > 1e-6:
        return
    c = k.c
    grey = (0.62, 0.64, 0.68)
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    c.set_line_cap(1)
    for col, w in ((INK, 4.6), (grey, 2.6)):
        c.set_source_rgb(*col); c.set_line_width(w)
        c.move_to(-8.6, 4); c.line_to(-8.6, 13.4); c.line_to(8.6, 13.4); c.line_to(8.6, 4); c.stroke()
    c.restore()


_OLD_CLUTCH = [None]


def clutch(k, x, y, w, skin=None):
    """of_cast.clutch for One Star (v20; review: "four equal capsules read as claws or nails"): the same grip, the
    back of the hand over the edge and the fingers curled down over the front, but the fingers of unequal length
    (index, middle, ring, little), shorter, tapering to the tip, a little fanned; no white knuckle dots."""
    import of_cast as oc
    skin = skin or oc.SKIN_LIGHT
    c = k.c
    oc.log_grip(c, "clutch", x, y)
    c.save(); c.translate(x, y)
    _taper(k, (-0.58 * w, 0.26 * w), (-0.64 * w, 0.52 * w), 0.22 * w, 0.18 * w, skin, lw=1.1)          # the thumb, under
    c.save(); c.translate(0, -0.16 * w); c.scale(0.62 * w, 0.30 * w); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    c.set_source_rgb(*skin); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.2); c.stroke()
    for kx, ln, fan in ((-0.40, 0.34, -0.05), (-0.13, 0.40, -0.01), (0.14, 0.37, 0.02), (0.40, 0.28, 0.06)):
        _taper(k, (kx * w, -0.04 * w), ((kx + fan) * w, (ln - 0.04) * w), 0.23 * w, 0.18 * w, skin, lw=1.1)
    c.restore()


_OLD_HANDLE = [None]


def handle_grip(k, x, y, w, ang, skin=None):
    """of_cast.handle_grip for One Star (v20: Pam's tube in 4.1, "fingers stacked like capsules"): the back of the hand
    behind the handle, four curled fingers of unequal size across it (index biggest, little smallest), touching like
    a fist, the thumb over them toward the index."""
    import of_cast as oc
    skin = skin or oc.SKIN_LIGHT
    c = k.c
    oc.log_grip(c, "handle", x, y)
    c.save(); c.translate(x, y); c.rotate(ang)
    c.save(); c.translate(0.0, 0.10 * w); c.scale(0.62 * w, 0.46 * w); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()   # its back
    c.set_source_rgb(*skin); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(0.08 * w); c.stroke()
    for fx, rw, rh in ((-0.40, 0.17, 0.36), (-0.12, 0.17, 0.40), (0.15, 0.16, 0.37), (0.39, 0.13, 0.30)):
        c.save(); c.translate(fx * w, 0.10 * w); c.scale(rw * w, rh * w); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        c.set_source_rgb(*skin); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(0.06 * w); c.stroke()
    _taper(k, (-0.52 * w, -0.24 * w), (0.04 * w, -0.34 * w), 0.24 * w, 0.20 * w, skin, lw=0.035 * w)   # the thumb over them
    c.restore()


_OLD_OCPHONE = [None]


def oc_phone(k, x, y, s, screen=None, ang=0.0, face_out=True):
    """of_cast.phone for One Star (v20, 6.6a: "the phone and his hands one black blob on his navy vest"): its back
    keeps its colour, with a light rim round it and the camera's two lenses at the top, so it reads as a phone's
    back on anything dark."""
    _OLD_OCPHONE[0](k, x, y, s, screen, ang, face_out)
    if screen and face_out:
        return
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    c.set_source_rgb(0.62, 0.65, 0.72); c.set_line_width(2.6)
    c.rectangle(-18.5, -34.5, 37, 69); c.stroke()                                 # the rim
    c.set_source_rgb(0.30, 0.32, 0.38); c.rectangle(-15, -31, 16, 22); c.fill()     # the camera's block
    for yy in (-26, -15):
        c.set_source_rgb(0.70, 0.74, 0.82); c.arc(-7, yy, 4.2, 0, 2 * math.pi); c.fill()
        c.set_source_rgb(0.10, 0.11, 0.14); c.arc(-7, yy, 2.2, 0, 2 * math.pi); c.fill()
    c.restore()


_OLD_PLAN = [None]
BAY7 = (132, 468, 112, 196)                                                       # bay 7 on the plan surface (measured)
TITLE = (150, 222, 300, 72)                                                       # its MY GARAGES label


def plan_surface(state, flip=None):
    """s4._plan_surface (v20, review 01: "the garages, numbers, tapes and rings all compete: one must see at once that
    the 7 was found"): the other bays toned down 38 % toward the plan's blue; bay 7 and the title label left bright."""
    sf = _OLD_PLAN[0](state, flip)
    c = cairo.Context(sf)
    c.set_operator(cairo.OPERATOR_ATOP)
    c.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    c.rectangle(0, 0, 540, 960)
    for x, y, w, h in (BAY7, TITLE):
        c.rectangle(x, y, w, h)
    c.set_source_rgba(0.16, 0.32, 0.72, 0.38); c.fill()
    return sf


def plant(k, side, dx=0):
    """cs_v19.plant (v20, review 06: "green spears out of the floor, over their feet"): 20 % smaller, broader leaves with
    round tips and unequal lengths, out of a pot's rim at the corner, so it reads as a desk plant close to us."""
    c = k.c
    bx = (20 if side == "left" else 520) + dx
    sgn = 1 if side == "left" else -1
    base = 925
    for i, (ang, ln, w) in enumerate(((-1.20, 232, 66), (-0.80, 262, 74), (-0.42, 196, 62), (-1.55, 178, 56))):
        a = ang if sgn > 0 else math.pi - ang
        tx, ty = bx + math.cos(a) * ln, base + math.sin(a) * ln
        nx, ny = -math.sin(a) * w / 2, math.cos(a) * w / 2
        mx, my = bx + math.cos(a) * ln * 0.55, base + math.sin(a) * ln * 0.55
        ux, uy = math.cos(a), math.sin(a)
        c.new_path(); c.move_to(bx, base)
        c.curve_to(mx + nx, my + ny, tx + nx * 0.8 - ux * 20, ty + ny * 0.8 - uy * 20, tx, ty)    # round tip
        c.curve_to(tx - nx * 0.8 - ux * 20, ty - ny * 0.8 - uy * 20, mx - nx, my - ny, bx, base); c.close_path()
        c.set_source_rgb(*((0.20, 0.42, 0.26) if i % 2 else (0.26, 0.50, 0.30))); c.fill_preserve()
        c.set_source_rgb(*INK); c.set_line_width(3); c.stroke()
        c.set_source_rgba(0.10, 0.25, 0.14, 0.6); c.set_line_width(2)                 # its middle vein
        c.move_to(bx + ux * 20, base + uy * 20); c.line_to(bx + ux * ln * 0.8, base + uy * ln * 0.8); c.stroke()
    px = bx - 70 if side == "left" else bx - 90                                     # the pot's rim at the corner
    s4.rect(k, px, base - 6, 160, 80, (0.72, 0.42, 0.28), 7020, shadow=False, lw=3)
    c.set_source_rgba(0, 0, 0, 0.15); c.rectangle(px, base + 10, 160, 8); c.fill()


# ---- gates (v20): what the geometric gates did not see --------------------------------------------------------------

INSERT_LOG = []                                                                    # (shot, d, length of sleeve in frame units)
CUR = ["", 0]
_OLD_CUFF = [None]


def _frame_pt(c, x, y):
    X, Y = c.user_to_device(x, y)
    ds = c.get_target().get_device_scale()[0]
    return X / ds, Y / ds


def insert_cuff(c, hand, elbow, w, skin, sleeve, cuff=None, stub=26):
    """of_scenes.insert_cuff, logged: how much sleeve shows INSIDE the frame (rules 224/225: past a short stub at the
    edge, an arm without its owner reads as "a tube" / "a pole")."""
    r = _OLD_CUFF[0](c, hand, elbow, w, skin, sleeve, cuff, stub)
    dl = math.hypot(hand[0] - elbow[0], hand[1] - elbow[1]) or 1.0
    d = ((hand[0] - elbow[0]) / dl, (hand[1] - elbow[1]) / dl)
    a = _frame_pt(c, *hand); b = _frame_pt(c, hand[0] - d[0] * (stub + 14), hand[1] - d[1] * (stub + 14))
    n, inside = 40, 0
    for i in range(n):
        t = (i + 0.5) / n
        x, y = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
        inside += 0 <= x <= 540 and 0 <= y <= 960
    INSERT_LOG.append((CUR[0], CUR[1], math.hypot(b[0] - a[0], b[1] - a[1]) * inside / float(n)))
    return r


def insert_faults(limit=200.0):
    return ["%s d%d: %.0f units of sleeve inside the frame without its owner (224/225)" % (sh, d, L)
            for sh, d, L in INSERT_LOG if L > limit]


def flat_bands(png_or_surface, rows_frac=0.20):
    """A frame's longest run of flat rows (one colour across) as a fraction of its height: an empty band (v17's 5.2)."""
    import numpy as np
    sf = png_or_surface
    w, h = sf.get_width(), sf.get_height()
    a = np.frombuffer(sf.get_data(), np.uint8).reshape(h, sf.get_stride() // 4, 4)[:, :w, :3].astype(np.int16)
    flat = a.std(axis=1).max(axis=1) < 3.0
    best = run = 0
    for f in flat:
        run = run + 1 if f else 0
        best = max(best, run)
    return best / float(h)


def _back(k, x, feet, s):
    """fs_film31.client_back without the legs (they are far below the frame): the jacket's back, collar, head."""
    import fs_film31 as f31
    old = f31.client_legs
    f31.client_legs = lambda *a, **kw: None
    try:
        f31.client_back(k, x, feet, s, 0.0)
    finally:
        f31.client_legs = old


def install():
    import cs_v19
    import of_scenes as osc
    cs_v19.PIECES["plant"] = plant
    if _OLD_CUFF[0] is None:
        _OLD_CUFF[0] = osc.insert_cuff
        osc.insert_cuff = insert_cuff
    if _OLD_PLAN[0] is None:
        _OLD_PLAN[0] = s4._plan_surface
        s4._plan_surface = plan_surface
    import of_cast as oc
    if _OLD_CLUTCH[0] is None:
        _OLD_CLUTCH[0], _OLD_HANDLE[0] = oc.clutch, oc.handle_grip
        oc.clutch, oc.handle_grip = clutch, handle_grip
        _OLD_OCPHONE[0] = oc.phone
        oc.phone = oc_phone
    import cs_scene1_v14 as v14
    if _OLD_PHONE[0] is None:
        _OLD_PHONE[0] = v14._phone
        v14._phone = _phone_in_claw
    if _OLD_GRIP[0] is None:
        _OLD_GRIP[0] = s1.grip_rect
        s1.grip_rect = _grip
        fn = dict((n, f) for n, _, f in s4.SHOTS)["4.3a"]

        def s4_3a(k, d):
            IN43A[0] = True
            try:
                return fn(k, d)
            finally:
                IN43A[0] = False
        s4.SHOTS[:] = [(n, nd, s4_3a) if n == "4.3a" else (n, nd, f) for n, nd, f in s4.SHOTS]
    s4.SHOTS[:] = [(n, nd, s4_3s) if n == "4.3s" else (n, nd, fn) for n, nd, fn in s4.SHOTS]
    import cs_scene5 as s5
    import cs_grips as g
    s5.PHONE51[0] = True
    s5.SOFIA51[0] = "sideeye"
    g.V20[0] = True
    g.PEN52[0] = pen52
    s5.SMILE52a[0] = 7                                                            # 5.2a: she smiles, blushing, from d7
    s5.BIG53[0] = True
    s5.TAPAT53[0] = (392, 700)                                                    # 5.3 the tap right of SAVE: the word shows
    s5.SHOTS[:] = [(n, 33, f) if n == "5.3" else (n, nd, f) for n, nd, f in s5.SHOTS]   # SAVED held 1.5 s (review 07)
    cp.THIN[0] = True                                                             # the full-frame phones: a thinner bezel
    g.SHIFT52[0] = 0.0                                                            # 5.2: v16's framing (v17's shift left an empty dark half)
    s4.FACE43A[0] = "dawning"                                                     # 4.3a: brows up as it dawns on him (review)
