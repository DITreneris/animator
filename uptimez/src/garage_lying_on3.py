"""Office Noir 3, shot 8.2: the Client lying on the sofa, drawn anew as a standalone picture.

NOT imported by the film. `python3 garage_lying_on3.py` writes office-noir-3/on3_garage_lying_v1.png (1080x1920).

What was wrong in garage_on3._lying_side: his head was the whole standing boxer, turned and clipped to a circle, so the
robe and shoulders of that boxer showed inside the circle beside his face; his body was a pile of straight quads.
Here the head is clipped to the head's own outline, and the body is one figure: neck, shoulder, chest, waist, hip, legs.
"""
import math
import cairo
import garage_on3 as ga
import client_on3 as b
from kit import Ctx, cut, ellipse, INK

Q = ga.Q
SKIN, CREAM = ga.SKIN, ga.CREAM
SKIN_D = (0.80, 0.58, 0.45)
PILLOW = (0.86, 0.82, 0.68)


def _spline(pts, n=10, closed=True):
    """Catmull-Rom through pts."""
    out = []; m = len(pts)
    rng = range(m) if closed else range(m - 1)
    for i in rng:
        p0, p1, p2, p3 = (pts[(i + j - 1) % m] if closed else pts[min(max(i + j - 1, 0), m - 1)] for j in range(4))
        for s in range(n):
            t = s / n
            out.append(tuple(0.5 * ((2 * p1[a]) + (-p0[a] + p2[a]) * t + (2 * p0[a] - 5 * p1[a] + 4 * p2[a] - p3[a]) * t * t
                                    + (-p0[a] + 3 * p1[a] - 3 * p2[a] + p3[a]) * t ** 3) for a in (0, 1)))
    if not closed:
        out.append(pts[-1])
    return out


def _tube(k, pts, w, col, lw=3.0, caps=(True, True)):
    """A limb: a smooth line through pts, half-width w[i] at each, round at the ends."""
    line = _spline(pts, 12, closed=False); n = len(line)
    ws = []
    for i in range(n):
        u = i / (n - 1) * (len(w) - 1); j = min(int(u), len(w) - 2); ws.append(w[j] + (w[j + 1] - w[j]) * (u - j))
    L, R = [], []
    for i, (x, y) in enumerate(line):
        x0, y0 = line[max(i - 1, 0)]; x1, y1 = line[min(i + 1, n - 1)]
        d = math.hypot(x1 - x0, y1 - y0) or 1; nx, ny = -(y1 - y0) / d, (x1 - x0) / d
        L.append((x + nx * ws[i], y + ny * ws[i])); R.append((x - nx * ws[i], y - ny * ws[i]))

    def cap(i, j, wv, flip):
        (x, y), (xp, yp) = line[i], line[j]
        a0 = math.atan2(y - yp, x - xp)
        return [(x + math.cos(a0 + s * math.pi / 2 * q / 4) * wv, y + math.sin(a0 + s * math.pi / 2 * q / 4) * wv)
                for s in (flip,) for q in range(-3, 4)]
    poly = L[:]
    if caps[1]:
        poly += cap(n - 1, n - 2, ws[-1], 1)
    poly += R[::-1]
    if caps[0]:
        poly += cap(0, 1, ws[0], 1)
    cut(k, poly, col, shadow=False, lw=lw)


def _blob(k, pts, col, lw=3.2, n=10):
    cut(k, _spline(pts, n), col, shadow=False, lw=lw)


def _line(c, pts, col, lw):
    c.set_source_rgb(*col); c.set_line_width(lw); c.set_line_cap(1); c.set_line_join(1)
    q = _spline(pts, 10, closed=False)
    c.move_to(*q[0])
    for p in q[1:]:
        c.line_to(*p)
    c.stroke(); c.set_line_cap(0)


def head(k, hx, hy, ang, face="exhausted", look=(-0.2, 0.6), s=Q):
    """His head and nothing else: the boxer drawn whole, clipped to the head's own outline (not to a circle)."""
    c = k.c
    c.save(); c.translate(hx, hy); c.rotate(ang); c.translate(4 * s, -b.HY * s)
    c.save(); c.scale(s, s); b._upper(c); b._head_xf(c, face)
    pts = b.co._head_pts(k, b.HY, 920)
    c.new_path(); c.move_to(pts[0][0] * 1.04, b.HY + (pts[0][1] - b.HY) * 1.04)
    for qx, qy in pts[1:]:
        c.line_to(qx * 1.04, b.HY + (qy - b.HY) * 1.04)
    c.close_path()
    c.rectangle(-60, b.HY - 84, 120, 80)
    for sx in (-1, 1):
        c.save(); c.translate(sx * 48, b.HY + 2); c.scale(10, 15); c.new_sub_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    c.restore(); c.clip()
    g = b.GOWN, b.GOWN_SHADE
    b.GOWN = b.GOWN_SHADE = INK                             # what is left of the body at the clip's edge reads as outline
    try:
        b.boxer(k, 0, 0, s, "b_walk", face, look, awake=True)
    finally:
        b.GOWN, b.GOWN_SHADE = g
    c.restore()


def _foot(k, ax, ay, ang, col=SKIN):
    """A bare foot from the ankle (ax, ay): heel, sole, toes; ang: where the toes point."""
    c = k.c
    c.save(); c.translate(ax, ay); c.rotate(ang)
    _blob(k, [(-9, -9), (8, -11), (30, -7), (40, 0), (36, 8), (10, 10), (-8, 9), (-12, 0)], col, lw=2.8, n=8)
    c.set_source_rgb(*INK); c.set_line_width(1.4)
    for tx in (27, 32):
        c.move_to(tx, 2); c.line_to(tx + 5, 6); c.stroke()
    c.restore()


def lying(k, face="exhausted", look=(-0.2, 0.6), hide=False, reach=False):
    """On his side on the seat, face to us: head on a pillow against the sofa's arm, shoulder up, waist in, hip up,
    the upper leg bent over the lower one, bare feet; the upper arm hangs over the seat's edge to the phone."""
    c = k.c
    b.co.FACES.setdefault("asleep", dict(b.co.FACES["exhausted"], lid=0.97))
    G, GS = b.GOWN, b.GOWN_SHADE
    # the pillow, propped on the sofa's arm
    c.save(); c.translate(352, 640); c.rotate(-0.30)
    _blob(k, [(-50, -24), (0, -30), (48, -24), (54, 0), (48, 26), (0, 30), (-50, 24), (-56, 0)], PILLOW, lw=3.0)
    _line(c, [(-40, 18), (-10, 22), (30, 18)], (0.70, 0.66, 0.54), 2.0)
    c.restore()
    # the lower leg (far side), straight along the seat
    _tube(k, [(150, 694), (136, 697), (124, 700)], (11, 10, 8.5), SKIN_D, lw=2.8)
    _foot(k, 122, 701, math.pi - 0.12, SKIN_D)
    _tube(k, [(214, 688), (176, 692), (142, 694)], (24, 21, 17), GS, lw=3.2, caps=(True, False))
    # his body: shoulder, chest, waist, hip, seat
    _blob(k, [(316, 640), (300, 624), (276, 626), (244, 644), (214, 640), (190, 650), (180, 676), (190, 702),
              (240, 707), (296, 705), (320, 690), (324, 664)], G, lw=3.4)
    # the upper leg, bent, its knee forward; the gown to the knee, then shin and foot
    _tube(k, [(154, 672), (134, 680), (116, 688)], (12, 11, 9), SKIN, lw=2.8)
    _foot(k, 114, 690, math.pi - 0.75)
    _tube(k, [(212, 668), (180, 664), (150, 671)], (27, 24, 19), G, lw=3.2, caps=(True, False))
    _line(c, [(143, 654), (138, 671), (145, 689)], GS, 3.0)                                       # the hem
    _line(c, [(196, 650), (188, 672), (194, 696)], GS, 2.4)                                       # a fold at the hip
    # the gown's front: bare chest in the V, the cream lapels, the belt and its knot
    cut(k, [(322, 644), (325, 684), (296, 664)], SKIN, shadow=False, lw=2.0)
    c.save(); _poly = _spline([(316, 640), (300, 624), (276, 626), (244, 644), (214, 640), (190, 650), (180, 676), (190, 702),
                               (240, 707), (296, 705), (320, 690), (324, 664)], 10)
    c.move_to(*_poly[0])
    for q in _poly[1:]:
        c.line_to(*q)
    c.close_path(); c.clip()                                                                      # the belt stays on him
    cut(k, [(236, 630), (251, 630), (250, 715), (235, 715)], CREAM, shadow=False, lw=2.4)
    c.restore()
    _tube(k, [(242, 684), (240, 700), (236, 718)], (4.5, 4.5, 4), CREAM, lw=2.0)                   # one end, over the seat
    _blob(k, [(235, 671), (244, 668), (251, 674), (250, 684), (241, 687), (234, 681)], CREAM, lw=2.2, n=6)
    if reach:                                               # up and round behind his head to the table
        _tube(k, [(300, 646), (318, 584), (384, 570), (444, 610)], (17, 16, 14, 12), G, lw=3.2)
        wx, wy, ha = 444, 610, 0.45
    # his neck, into the collar
    _tube(k, [(326, 644), (314, 652), (304, 660)], (15, 15, 16), SKIN, lw=2.6)
    _tube(k, [(306, 630), (299, 652), (304, 672), (318, 688)], (6.5, 7, 7, 6), CREAM, lw=2.2)                     # the collar round it
    head(k, 348, 622, 1.02, "asleep" if hide else face, look)
    # the upper arm: shoulder, elbow over the seat's edge, the cuff, the watch, an open hand by the phone
    if reach:
        pass
    else:
        _tube(k, [(290, 648), (276, 690), (272, 730), (286, 764)], (18, 17, 15, 12.5), G, lw=3.2)
        wx, wy, ha = 286, 764, 1.15
    c.save(); c.translate(wx, wy); c.rotate(ha)
    cut(k, [(-7, -14), (4, -14), (4, 14), (-7, 14)], GS, shadow=False, lw=2.0)                     # the cuff
    _blob(k, [(4, -10), (20, -11), (36, -8), (44, -1), (40, 8), (22, 11), (4, 10)], SKIN, lw=2.6, n=8)   # the hand
    _tube(k, [(14, -9), (22, -17), (31, -17)], (4.2, 4, 3.6), SKIN, lw=2.2)                        # the thumb
    cut(k, [(6, -11.5), (13, -11.5), (13, 11.5), (6, 11.5)], (0.85, 0.70, 0.20), shadow=False, lw=1.6)   # the watch
    c.set_source_rgb(*INK); c.set_line_width(1.4)
    for fy in (-3, 3):
        c.move_to(30, fy); c.line_to(41, fy * 0.8); c.stroke()
    c.restore()


def install(g=ga):
    """Put the new figure into garage_on3 (the film's v38 calls this; nothing changes until it is called). Returns what
    was there. With it: his eyes on the phone while it lies on the floor, a contact shadow under that phone, and the
    "10" of the faded plan a little darker (review, 22 Nov)."""
    import kit, props_on3 as pr
    old = g.lying, g.phone, g.gone

    def lying2(k, face="exhausted", look=(-0.2, 0.6), hide=False, reach=False):
        lying(k, face, look if (hide or reach) else (0.9, 0.5), hide, reach)   # the phone is straight below his head; his head is turned 58 degrees

    def phone2(k, x, y, s_=1.0, ang=0.0, screen="done", back=False):
        if y > 800:                                         # the one on the floor: it lies on the floor
            c = k.c
            c.save(); c.translate(x + 5, y + 9); c.rotate(ang); c.scale(s_, s_)
            for grow, al in ((14, 0.10), (8, 0.14), (3, 0.20)):
                c.set_source_rgba(0, 0, 0, al); c.rectangle(-46 - grow, -84 - grow, 92 + 2 * grow, 168 + 2 * grow); c.fill()
            c.restore()
        old[1](k, x, y, s_, ang, screen, back)

    def gone2(k, x, y, w, h):
        old[2](k, x, y, w, h)
        c = k.c
        z = min((w - 16) / 108.0, (h - 12) / 98.0)
        c.save(); c.translate(x + w / 2 - 50 * z, y + h / 2 - 55 * z); c.scale(z, z)
        c.push_group(); kit.text(k, "10", 21, 89.5, 17, pr.LINE, bold=True); c.pop_group_to_source(); c.paint_with_alpha(0.38)
        c.restore()

    g.lying, g.phone, g.gone = lying2, phone2, gone2
    return old


def scene(scale=2, v=2, **kw):
    """8.2 in the film's own framing, with the new figure. v=1: the first picture. v=2: as install() draws it."""
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, 540 * scale, 960 * scale); s.set_device_scale(scale, scale)
    c = cairo.Context(s); k = Ctx(c, 0)
    ga._zoom(c)
    old = ga.lying, ga.phone, ga.gone
    if v == 1:
        ga.lying = lying
    else:
        install(ga)
    try:
        ga.room(k, **kw)
    finally:
        ga.lying, ga.phone, ga.gone = old
    return s


if __name__ == "__main__":
    import os, hashlib
    d = os.path.join(os.path.dirname(__file__), "..", "office-noir-3")
    for v in (1, 2):
        out = os.path.abspath(os.path.join(d, "on3_garage_lying_v%d.png" % v))
        scene(2, v).write_to_png(out); print(out, hashlib.md5(open(out, "rb").read()).hexdigest())
