"""Paper-cutout art kit for Uptime Inc. storyboards.
Every shape gets jittered edges, a drop shadow and a dark outline. A 12 fps 'boil'
re-jitters edges 12 times a second so held panels still feel alive."""
import math
import random
import cairo
import numpy as np

W, H = 540, 960
INK = (0.16, 0.11, 0.09)
FONT = "Lilita One"
MONO = "DejaVu Sans"

WALL = (0.91, 0.86, 0.76)
FLOOR = (0.70, 0.60, 0.47)
DESK = (0.55, 0.38, 0.24)
PAPER = (0.98, 0.97, 0.93)
SCREEN = (0.62, 0.84, 0.95)

PEOPLE = {
    "MAX": dict(skin=(0.95, 0.76, 0.49), body=(0.52, 0.56, 0.62), hair=(0.10, 0.09, 0.09), glasses=True, h=1.0),
    "RUSH": dict(skin=(0.62, 0.42, 0.26), body=(0.93, 0.93, 0.95), hair=(0.06, 0.05, 0.05), tie=(0.72, 0.14, 0.2), h=0.96),
    "PAM": dict(skin=(1.0, 0.86, 0.67), body=(0.40, 0.27, 0.58), hair=(0.30, 0.17, 0.09), bob=True, h=1.02),
    "DON": dict(skin=(0.96, 0.78, 0.66), body=(0.13, 0.13, 0.17), hair=(0.55, 0.55, 0.55), tie=(0.80, 0.10, 0.12),
                bald=True, h=1.12),
}


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def lerp(a, b, t):
    return a + (b - a) * t


class Ctx:
    """Holds the cairo context and the current boil index (0..2)."""
    def __init__(self, c, boil):
        self.c = c
        self.boil = boil

    def rng(self, seed):
        return random.Random(seed * 131 + self.boil * 7919)


def _poly(c, pts):
    c.move_to(*pts[0])
    for p in pts[1:]:
        c.line_to(*p)
    c.close_path()


def rough_rect_pts(k, x, y, w, h, seed, j=2.2):
    r = k.rng(seed)
    pts = []
    for (ax, ay), (bx, by) in [((x, y), (x + w, y)), ((x + w, y), (x + w, y + h)),
                               ((x + w, y + h), (x, y + h)), ((x, y + h), (x, y))]:
        n = max(2, int(math.hypot(bx - ax, by - ay) / 40))
        for i in range(n):
            u = i / n
            pts.append((lerp(ax, bx, u) + r.uniform(-j, j), lerp(ay, by, u) + r.uniform(-j, j)))
    return pts


def rough_ellipse_pts(k, cx, cy, rx, ry, seed, n=26, j=0.045):
    r = k.rng(seed)
    return [(cx + math.cos(a) * rx * (1 + r.uniform(-j, j)), cy + math.sin(a) * ry * (1 + r.uniform(-j, j)))
            for a in (2 * math.pi * i / n for i in range(n))]


def cut(k, pts, fill, shadow=True, outline=True, lw=2.6, alpha=1.0):
    c = k.c
    if shadow:
        c.save()
        c.translate(3.5, 4)
        _poly(c, pts)
        c.set_source_rgba(0, 0, 0, 0.22 * alpha)
        c.fill()
        c.restore()
    _poly(c, pts)
    c.set_source_rgba(*fill, alpha)
    c.fill_preserve()
    if outline:
        c.set_source_rgba(*INK, alpha)
        c.set_line_width(lw)
        c.set_line_join(cairo.LINE_JOIN_ROUND)
        c.stroke()
    else:
        c.new_path()


def rect(k, x, y, w, h, fill, seed, **kw):
    cut(k, rough_rect_pts(k, x, y, w, h, seed), fill, **kw)


def ellipse(k, cx, cy, rx, ry, fill, seed, **kw):
    cut(k, rough_ellipse_pts(k, cx, cy, rx, ry, seed), fill, **kw)


def text(k, s, x, y, size, col=INK, font=FONT, bold=False, center=True, rot=0.0):
    c = k.c
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    c.select_font_face(font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    c.set_font_size(size)
    e = c.text_extents(s)
    c.move_to(-e.width / 2 - e.x_bearing if center else 0, e.height / 2 if center else 0)
    c.set_source_rgb(*col)
    c.show_text(s)
    c.restore()


def paper_texture(seed=3):
    rng = np.random.default_rng(seed)
    n = rng.normal(0, 1, (H // 2, W // 2))
    n = (n - n.min()) / (n.max() - n.min())
    a = (n * 255).astype(np.uint8)
    img = np.zeros((H // 2, W // 2, 4), np.uint8)
    img[..., 0] = img[..., 1] = img[..., 2] = a
    img[..., 3] = 255
    surf = cairo.ImageSurface.create_for_data(memoryview(img).cast("B"), cairo.FORMAT_ARGB32, W // 2, H // 2)
    return surf, img


_TEX = paper_texture()


def grain(k, amount=0.07):
    c = k.c
    c.save()
    c.scale(2, 2)
    c.set_source_surface(_TEX[0], (k.boil % 3) * -3, 0)
    c.paint_with_alpha(amount)
    c.restore()


# ---------- props ----------
def file_sheet(k, x, y, w, h, label, seed, rot=0.0, big=False, fill=PAPER):
    c = k.c
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    rect(k, -w / 2, -h / 2, w, h, fill, seed)
    # fold corner
    c.move_to(w / 2 - w * 0.22, -h / 2)
    c.line_to(w / 2, -h / 2 + w * 0.22)
    c.set_source_rgb(*INK)
    c.set_line_width(2)
    c.stroke()
    if label:
        size = (w * 0.2 if big else max(9, w * 0.16))
        text(k, label, 0, 0, size, INK)
    c.restore()


def desk(k, x, y, w, seed):
    rect(k, x, y, w, 26, DESK, seed)
    rect(k, x + 12, y + 26, 16, 110, (0.45, 0.30, 0.19), seed + 1)
    rect(k, x + w - 28, y + 26, 16, 110, (0.45, 0.30, 0.19), seed + 2)


def monitor(k, x, y, w, h, seed, screen=SCREEN):
    rect(k, x + w / 2 - 8, y + h, 16, 22, (0.3, 0.3, 0.33), seed + 1)
    rect(k, x, y, w, h, (0.2, 0.2, 0.23), seed)
    rect(k, x + 7, y + 7, w - 14, h - 14, screen, seed + 2, shadow=False, lw=1.5)


def popup(k, x, y, w, h, line1, seed, col=(1, 1, 1), check=False, warn=False):
    rect(k, x, y, w, h, col, seed)
    if check:
        ellipse(k, x + 22, y + h / 2, 12, 12, (0.25, 0.75, 0.35), seed + 3, shadow=False)
        text(k, "✓", x + 22, y + h / 2, 17, (1, 1, 1), font=MONO, bold=True)
    if warn:
        ellipse(k, x + 22, y + h / 2, 12, 12, (0.95, 0.75, 0.15), seed + 3, shadow=False)
        text(k, "!", x + 22, y + h / 2, 17, INK, font=MONO, bold=True)
    c = k.c
    c.save()
    c.select_font_face(FONT)
    c.set_font_size(19)
    c.move_to(x + 42, y + h / 2 + 7)
    c.set_source_rgb(*INK)
    c.show_text(line1)
    c.restore()


def door(k, x, y, w, h, seed, open_amt=0.0, sign="DOWNLOADS"):
    rect(k, x - 8, y - 8, w + 16, h + 8, (0.45, 0.33, 0.22), seed)  # frame
    rect(k, x, y, w, h, (0.12, 0.10, 0.10), seed + 1, shadow=False)  # dark opening
    if open_amt < 1:
        ww = w * (1 - open_amt)
        rect(k, x, y, ww, h, (0.80, 0.62, 0.42), seed + 2)
        ellipse(k, x + ww - 16, y + h * 0.55, 6, 6, (0.85, 0.75, 0.2), seed + 3, shadow=False, lw=1.5)
    rect(k, x + w / 2 - 75, y - 52, 150, 34, (1, 1, 1), seed + 4)
    text(k, sign, x + w / 2, y - 35, 22, INK)


def sfx(k, s, x, y, size, rot=-0.12, fill=(1.0, 0.86, 0.15)):
    c = k.c
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    c.select_font_face(FONT)
    c.set_font_size(size)
    e = c.text_extents(s)
    c.move_to(-e.width / 2 - e.x_bearing, e.height / 2)
    c.text_path(s)
    c.set_line_width(size * 0.16)
    c.set_line_join(cairo.LINE_JOIN_ROUND)
    c.set_source_rgb(*INK)
    c.stroke_preserve()
    c.set_source_rgb(*fill)
    c.fill()
    c.restore()


def bubble(k, s, tx, ty, y=128, size=40, pop=1.0):
    c = k.c
    c.select_font_face(FONT)
    c.set_font_size(size)
    e = c.text_extents(s)
    bw, bh = e.width + 52, size + 40
    bx = clamp(tx - bw / 2, 26, 460 - bw)
    c.save()
    c.translate(bx + bw / 2, y + bh / 2)
    c.scale(pop, pop)
    c.translate(-(bx + bw / 2), -(y + bh / 2))
    tail_x = clamp(tx, bx + 34, bx + bw - 34)
    pts = rough_rect_pts(k, bx, y, bw, bh, 900 + len(s), j=1.6)
    tail = [(tail_x - 15, y + bh - 3), (clamp(tx, 30, 510), min(ty, y + bh + 70)), (tail_x + 15, y + bh - 3)]
    cut(k, tail, (1, 1, 1))
    cut(k, pts, (1, 1, 1))
    _poly(c, tail)
    c.set_source_rgb(1, 1, 1)
    c.fill()
    c.select_font_face(FONT)
    c.set_font_size(size)
    c.move_to(bx + 26 - e.x_bearing, y + bh / 2 + e.height / 2 - 2)
    c.set_source_rgb(*INK)
    c.show_text(s)
    c.restore()


# ---------- people ----------
ARM_POSES = {  # (left upper, left fore, right upper, right fore) degrees; 0 = down, +90 = right, 180 = up
    "stand": (-8, 0, 8, 0),
    "panic": (-150, -110, 150, 110),       # hands on head
    "shock": (-160, -20, 160, 20),         # arms up
    "type": (-50, 60, 50, -60),            # forearms forward onto desk
    "point_r": (-8, 0, 95, 0),
    "point_l": (-95, 0, 8, 0),
    "hold_up": (-10, 0, 168, 0),           # right arm straight up
    "reach_r": (-20, 0, 80, 10),
    "back": (-60, -40, 60, 40),            # leaning away, hands up front
    "click": (-8, 0, 55, -40),
    "pleased": (-35, 110, 35, -110),       # hands on hips
}


def arm(k, sx, sy, a1, a2, col, skin, seed, ln=48, w=17):
    c = k.c
    d = lambda a: (math.sin(math.radians(a)), math.cos(math.radians(a)))
    ex, ey = sx + d(a1)[0] * ln, sy + d(a1)[1] * ln
    hx, hy = ex + d(a1 + a2)[0] * ln, ey + d(a1 + a2)[1] * ln
    for (ax, ay, bx, by) in ((sx, sy, ex, ey), (ex, ey, hx, hy)):
        ang = math.atan2(by - ay, bx - ax)
        nx, ny = -math.sin(ang) * w / 2, math.cos(ang) * w / 2
        cut(k, [(ax + nx, ay + ny), (bx + nx, by + ny), (bx - nx, by - ny), (ax - nx, ay - ny)], col, shadow=False, lw=2)
    ellipse(k, hx, hy, w * 0.6, w * 0.6, skin, seed, shadow=False, lw=2)
    return hx, hy


BADGE_HOOK = None   # callable(k, name, person_dict, body_top, seed), drawn under the arms; None = classic tag


def person(k, name, x, feet, s=1.0, pose="stand", face="neutral", seed=1, look=(0, 0), seated=False, badge=True):
    """Draws a person; returns dict of key points (head, hands) in canvas coords."""
    p = PEOPLE[name]
    c = k.c
    c.save()
    c.translate(x, feet)
    c.scale(s, s)
    hgt = 300 * p["h"]
    body_top = -hgt + 78
    # body (slightly tapered)
    bw = 86
    r = k.rng(seed)
    body = [(-bw / 2 + 4, body_top), (bw / 2 - 4, body_top), (bw / 2 + 4, 0), (-bw / 2 - 4, 0)]
    body = [(px + r.uniform(-1.5, 1.5), py + r.uniform(-1.5, 1.5)) for px, py in body]
    cut(k, body, p["body"])
    if p.get("tie"):
        cut(k, [(0, body_top + 4), (-10, body_top + 70), (0, body_top + 86), (10, body_top + 70)], p["tie"], shadow=False, lw=1.8)
    if badge and BADGE_HOOK is not None:                 # optional custom badge (set by a film module)
        BADGE_HOOK(k, name, p, body_top, seed)
    elif badge:
        rect(k, -22 if not p.get("tie") else 8, body_top + 34, 36, 22, (1, 1, 1), seed + 40, shadow=False, lw=1.6)
        text(k, name, (-4 if not p.get("tie") else 26), body_top + 45, 11, INK)
    a = ARM_POSES[pose]
    hands = []
    for side, (u, f) in ((-1, (a[0], a[1])), (1, (a[2], a[3]))):
        hands.append(arm(k, side * 40, body_top + 14, u, f, p["body"], p["skin"], seed + 10 + side))
    # head
    hy = body_top - 44
    ellipse(k, 0, hy, 50, 50, p["skin"], seed + 20)
    # hair
    if p.get("bald"):  # added for DON: shiny dome, side tufts only
        rect(k, -54, hy - 4, 12, 26, p["hair"], seed + 24, shadow=False, lw=2)
        rect(k, 42, hy - 4, 12, 26, p["hair"], seed + 25, shadow=False, lw=2)
        c.set_source_rgba(1, 1, 1, 0.55)
        c.save(); c.translate(-14, hy - 30); c.rotate(-0.5); c.scale(1, 0.45)
        c.arc(0, 0, 14, 0, 2 * math.pi); c.restore(); c.fill()
    else:
        hp = rough_ellipse_pts(k, 0, hy - 8, 52, 46, seed + 21)
        hp = [q for q in hp if q[1] < hy - 12] + [(48, hy - 14), (-48, hy - 14)]
        hp.sort(key=lambda q: math.atan2(q[1] - (hy - 8), q[0]))
        cut(k, hp, p["hair"], shadow=False, lw=2)
    if p.get("bob"):
        rect(k, -54, hy - 18, 16, 54, p["hair"], seed + 22, shadow=False, lw=2)
        rect(k, 38, hy - 18, 16, 54, p["hair"], seed + 23, shadow=False, lw=2)
    face_draw(k, 0, hy + 4, face, look, glasses=p.get("glasses", False), seed=seed + 30)
    c.restore()
    head = (x, feet + hy * s)
    return {"head": head, "hands": [(x + hx * s, feet + hy_ * s) for hx, hy_ in hands]}


def face_draw(k, x, y, face, look, glasses=False, seed=0):
    c = k.c
    lx, ly = look
    big = face in ("shock", "panic")
    if face in ("happy", "pleased", "smug"):
        for sx in (-17, 17):
            c.set_source_rgb(*INK)
            c.set_line_width(4)
            c.arc(sx, y + 2, 9, math.pi * 1.15, math.pi * 1.85)
            c.stroke()
    elif face == "hollow":  # dead-eyed: dark rings, tiny pupils, heavy lids
        for sx in (-17, 17):
            ellipse(k, sx, y, 12, 12, (0.55, 0.5, 0.55), seed + sx + 7, shadow=False, lw=2)
            ellipse(k, sx, y + 2, 2.5, 2.5, INK, seed + sx + 8, shadow=False, outline=False)
            c.set_source_rgb(*INK)
            c.set_line_width(4)
            c.move_to(sx - 13, y - 3)
            c.line_to(sx + 13, y - 3)
            c.stroke()
    elif face == "squint":
        for sx in (-17, 17):
            c.set_source_rgb(*INK)
            c.set_line_width(4)
            c.move_to(sx - 9, y)
            c.line_to(sx + 9, y)
            c.stroke()
    else:
        for sx in (-17, 17):
            ellipse(k, sx, y, 13 if big else 10, 13 if big else 10, (1, 1, 1), seed + sx, shadow=False, lw=2)
            ellipse(k, sx + lx * 4, y + ly * 4, 4.5, 4.5, INK, seed + sx + 1, shadow=False, outline=False)
    c.set_source_rgb(*INK)
    c.set_line_width(4)
    # brows
    if face in ("panic", "confused"):
        c.move_to(-26, y - 20); c.line_to(-9, y - 15); c.stroke()
        c.move_to(9, y - 15); c.line_to(26, y - 24); c.stroke()
    elif face == "smug" or face == "pleased":
        c.move_to(-26, y - 16); c.line_to(-9, y - 18); c.stroke()
        c.move_to(9, y - 18); c.line_to(26, y - 16); c.stroke()
    if glasses:
        c.set_line_width(3)
        for sx in (-17, 17):
            c.arc(sx, y, 15, 0, 2 * math.pi)
            c.stroke()
    # mouth
    my = y + 28
    if face == "panic":
        ellipse(k, 0, my, 14, 9, (0.35, 0.08, 0.08), seed + 5, shadow=False, lw=2)
    elif face == "shock":
        ellipse(k, 0, my, 9, 12, (0.35, 0.08, 0.08), seed + 5, shadow=False, lw=2)
    elif face in ("happy", "pleased"):
        c.arc(0, my - 6, 13, 0.15 * math.pi, 0.85 * math.pi)
        c.stroke()
    elif face == "smug":
        c.move_to(-12, my); c.curve_to(-4, my + 4, 6, my + 2, 14, my - 6); c.stroke()
    elif face == "confused":
        c.move_to(-12, my + 2); c.curve_to(-4, my - 4, 4, my + 6, 12, my); c.stroke()
    else:
        c.move_to(-11, my); c.line_to(11, my); c.stroke()


def office_bg(k, seed=100, window=False, door_pos=None):
    rect(k, -20, -20, W + 40, 700, WALL, seed, shadow=False, outline=False)
    rect(k, -20, 680, W + 40, 320, FLOOR, seed + 1, shadow=False)
    # baseboard
    rect(k, -20, 670, W + 40, 16, (0.62, 0.5, 0.36), seed + 2, shadow=False, lw=2)
