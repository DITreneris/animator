"""Rough animatic renderer. Every frame is a pure function of (variant, frame).
Usage: python3 render.py A [frames...]   -> raw BGRA to stdout, or PNGs if frames given."""
import sys
import math
import cairo
from timing import VARIANTS, SHARED, N, bubbles

W, H = 540, 960
NAVY = (0.043, 0.063, 0.125)
CYAN = (0.21, 0.89, 1.0)
ORANGE = (1.0, 0.43, 0.0)
WHITE = (0.96, 0.97, 0.99)
FONT = "Lilita One"

v = sys.argv[1]
T = VARIANTS[v]
BUBBLES = bubbles(v)

FLOOR_Y = 760
COLD_CAM = (382, 526, 1.7)
MED_CAM = (305, 545, 1.45)
CU_CAM = (440, 455, 2.5)
PUSH_CAM = (322, 556, 1.52)


# ---------- helpers ----------
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def ease_out(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def lerp(a, b, t):
    return a + (b - a) * t


def seg(f, a, b):
    return clamp((f - a) / max(1, (b - a)))


def rrect(c, x, y, w, h, r):
    c.new_sub_path()
    c.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    c.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    c.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    c.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
    c.close_path()


def text_c(c, s, x, y, size, col=(0, 0, 0)):
    c.select_font_face(FONT)
    c.set_font_size(size)
    e = c.text_extents(s)
    c.move_to(x - e.width / 2 - e.x_bearing, y)
    c.set_source_rgb(*col)
    c.show_text(s)


# ---------- state ----------
def floor_num(f):
    if f < 45:
        return 3
    if f < 120:
        return 1
    if f < 180:
        return 2
    return 3


def wobble(f, amp=1.0):
    # period of 15 frames -> exactly 30 cycles in the loop, so frame 450 == frame 0
    return math.sin(2 * math.pi * f / 15) * amp


def pile_amount(f):
    if f < 45:
        return 1.0
    if f >= T["pounce"]:
        return ease_out((f - T["pounce"]) / (N - T["pounce"]))
    return 0.0


def camera(f):
    if f < 45:
        return COLD_CAM
    p0 = T["pounce"]
    if f >= p0:
        u = ease_out((f - p0) / (N - p0))
        return tuple(lerp(a, b, u) for a, b in zip(CU_CAM, COLD_CAM))
    if f >= T["cu"]:
        return CU_CAM
    if f >= T["glow"]:  # push-in during the glow, then hold still (true freeze)
        u = ease(seg(f, T["glow"], T["hatch"]))
        return tuple(lerp(a, b, u) for a, b in zip(MED_CAM, PUSH_CAM))
    return MED_CAM


def jolt(f):
    d = f - T["thunk"]
    if 0 <= d < 10:
        return math.sin(d * 2.4) * 9 * (1 - d / 10)
    return 0.0


# story positions (world x) before the pounce
def story_x(f):
    savi = 400 if f < 180 else lerp(400, 434, ease(seg(f, 183, 200)))
    user = lerp(150, 292, ease(seg(f, 48, 66)))
    if f >= 120:
        user = lerp(292, 304, ease(seg(f, 124, 140)))
    if f >= 180:
        user = lerp(304, 318, ease(seg(f, 184, 200)))
    dead = lerp(140, 228, ease(seg(f, 124, 142)))
    if f >= 180:
        dead = lerp(228, 248, ease(seg(f, 184, 200)))
    pm = lerp(130, 176, ease(seg(f, 184, 202)))
    return savi, user, dead, pm


PILE = {"savi": (400, -4), "user": (250, 11), "dead": (508, -10), "pm": (205, 6)}


def actors(f):
    """returns dict name -> (x, lean_deg, visible)"""
    p = pile_amount(f)
    if f < 45:
        sx, ux, dx, px = 0, 0, 0, 0
    else:
        sx, ux, dx, px = story_x(min(f, T["pounce"]))
    wob = wobble(f, 1.6) * p
    flail = 0.0
    if f >= T["pounce"]:
        dur = N - T["pounce"]
        flail = math.sin((f - T["pounce"]) * 0.9) * 10 * (1 - p) * (1.6 if dur > 50 else 1.0)
    out = {}
    out["savi"] = (lerp(sx, PILE["savi"][0], p), lerp(0, PILE["savi"][1], p) + wob, True)
    out["user"] = (lerp(ux, PILE["user"][0], p), lerp(0, PILE["user"][1], p) - wob + flail, f >= 48 or f < 45)
    out["dead"] = (lerp(dx, PILE["dead"][0], p), lerp(0, PILE["dead"][1], p) + wob - flail, f >= 124 or f < 45)
    out["pm"] = (lerp(px, PILE["pm"][0], p), lerp(0, PILE["pm"][1], p) - wob + flail, f >= 184 or f < 45)
    return out


def savi_expr(f):
    if f < 45:
        return "smug"
    if f >= T["pounce"]:
        return "smug" if pile_amount(f) > 0.55 else "sheepish"
    if f >= T["cu"]:
        return "sheepish"
    if f >= T["glow"]:
        return "wide"
    return "smug"


def human_mood(f, name):
    if f >= T["pounce"] or f < 45:
        return "angry" if name != "dead" else "panic"
    if f >= T["thunk"]:
        return "shock"
    if f >= T["glow"]:
        return "shock"
    mood = {"user": "flat", "dead": "panic", "pm": "angry"}[name]
    if name == "user" and f >= 120:
        mood = "annoyed"
    return mood


TURN_DUR = 24 if v == "A" else 14


def gaze_schedule():
    # (start_frame, target, blend_frames)
    return [(0, "savi", 0), (T["glow"], "chest", 10), (T["thunk"], "cube", 4),
            (T["turn"], "savi", TURN_DUR), (T["pounce"], "savi", 0)]


def gaze_point(f, targets):
    sched = gaze_schedule()
    cur, prev, start, dur = sched[0][1], sched[0][1], 0, 0
    for i, (st, tg, d) in enumerate(sched):
        if f >= st:
            prev = cur if i else tg
            cur, start, dur = tg, st, d
    u = 1.0 if dur == 0 else ease(seg(f, start, start + dur))
    a, b = targets[prev], targets[cur]
    return (lerp(a[0], b[0], u), lerp(a[1], b[1], u))


# arm poses: (left_shoulder_deg, left_elbow_deg, right_shoulder_deg, right_elbow_deg)
# 0 = hanging down, +90 = pointing right, 180 = up
POSES = {
    "down": (-8, 0, 8, 0),
    "hold": (-8, 0, 20, 75),
    "phone": (-8, 0, 140, 15),
    "sweep": (-20, 70, 95, 0),
    "shock": (-150, -35, 150, 35),
    "reach_r": (150, 15, 165, 5),
    "reach_l": (-165, -5, -150, -15),
}


def pose_schedule(name):
    reach = "reach_r"
    sc = {
        "user": [(0, "R"), (45, "hold"), (T["glow"], "down"), (T["thunk"], "shock"), (T["turn"], "down"), (T["pounce"], "R")],
        "dead": [(0, "R"), (45, "down"), (135, "phone"), (180, "down"), (T["thunk"], "shock"), (T["turn"], "down"), (T["pounce"], "R")],
        "pm": [(0, "R"), (45, "down"), (192, "sweep"), (238, "down"), (T["thunk"], "shock"), (T["turn"], "down"), (T["pounce"], "R")],
    }[name]
    return sc


def arm_angles(f, name, side):
    sched = pose_schedule(name)
    def resolve(p):
        if p == "R":
            return POSES["reach_l" if side < 0 else "reach_r"]
        return POSES[p]
    cur, prev, start = sched[0][1], sched[0][1], 0
    for i, (st, p) in enumerate(sched):
        if f >= st:
            prev = cur if i else p
            cur, start = p, st
    blend = 3 if cur == "shock" else 6
    u = 1.0 if start in (0, 45) else ease(seg(f, start, start + blend))
    a, b = resolve(prev), resolve(cur)
    ang = [lerp(x, y, u) for x, y in zip(a, b)]
    if cur == "sweep":  # the PM sweeps the arm across the other two
        ang[2] = lerp(60, 115, ease(seg(f, 192, 222)))
    if f >= T["pounce"]:
        k = (1 - pile_amount(f)) * 25
        ang[0] += math.sin(f * 1.1) * k
        ang[2] += math.sin(f * 1.3 + 1) * k
    return ang


def draw_arm(c, sx, sy, a1, a2, col, hand, ln=58, w=18):
    def d(a):
        r = math.radians(a)
        return math.sin(r), math.cos(r)
    ex, ey = sx + d(a1)[0] * ln, sy + d(a1)[1] * ln
    hx, hy = ex + d(a1 + a2)[0] * ln, ey + d(a1 + a2)[1] * ln
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.set_line_join(cairo.LINE_JOIN_ROUND)
    c.set_line_width(w)
    c.set_source_rgb(*col)
    c.move_to(sx, sy)
    c.line_to(ex, ey)
    c.line_to(hx, hy)
    c.stroke()
    c.arc(hx, hy, w * 0.62, 0, 2 * math.pi)
    c.set_source_rgb(*hand)
    c.fill()


def cube_state(f):
    """returns ('chest'|'air'|'floor', x, y) in world coords relative to SAVI or absolute"""
    if f < T["hatch"] or f < 45:
        return ("chest", 0, 0)
    if f >= T["pounce"]:
        u = seg(f, T["pounce"] + 6, T["pounce"] + (N - T["pounce"]) * 0.7)
        if u >= 1:
            return ("chest", 0, 0)
        return ("zip", u, 0)
    if f < T["thunk"]:
        u = seg(f, T["hatch"], T["thunk"])
        return ("air", u, 0)
    return ("floor", 0, 0)


def hatch_open(f):
    if f < 45:
        return 0.0
    if f >= T["pounce"]:
        u = seg(f, T["pounce"] + (N - T["pounce"]) * 0.7, T["pounce"] + (N - T["pounce"]) * 0.72 + 2)
        return 1 - u
    return ease_out(seg(f, T["hatch"], T["hatch"] + 4))


def glow_level(f):
    if f < 45 or f >= T["pounce"]:
        return 0.0
    if f >= T["hatch"]:
        return clamp(1 - (f - T["hatch"]) / 20)
    if f >= T["glow"]:
        return ease(seg(f, T["glow"], T["hatch"]))
    return 0.0


# ---------- drawing ----------
def draw_bg(c, f):
    c.set_source_rgb(*NAVY)
    c.paint()
    # blurred city lights drifting down; drift is periodic over the loop
    drift = (f / N) * 320
    for i, (bx, by, r, col) in enumerate([
        (80, 200, 140, (0.85, 0.2, 0.6)), (430, 120, 170, (0.25, 0.3, 0.8)),
        (300, 520, 200, (0.7, 0.15, 0.55)), (60, 700, 150, (0.2, 0.5, 0.9)),
        (470, 860, 160, (0.8, 0.2, 0.5)), (250, 40, 120, (0.3, 0.2, 0.7))]):
        for k in (-1, 0, 1):
            y = (by + drift) % 320 + k * 320 + (i // 2) * 320 - 320
            y = ((by + drift + 960) % 1280) - 160 + k * 1280
            g = cairo.RadialGradient(bx, y, 0, bx, y, r)
            g.add_color_stop_rgba(0, *col, 0.35)
            g.add_color_stop_rgba(1, *col, 0.0)
            c.set_source(g)
            c.arc(bx, y, r, 0, 2 * math.pi)
            c.fill()


def draw_elevator(c, f):
    # floor slab
    c.set_source_rgb(0.09, 0.11, 0.18)
    c.rectangle(-200, FLOOR_Y, 1000, 400)
    c.fill()
    c.set_source_rgba(*CYAN, 0.5)
    c.set_line_width(3)
    c.move_to(-200, FLOOR_Y)
    c.line_to(800, FLOOR_Y)
    c.stroke()
    # glass frame
    c.set_source_rgba(*CYAN, 0.25)
    c.set_line_width(4)
    for x in (20, 488):
        c.move_to(x, 140)
        c.line_to(x, FLOOR_Y)
        c.stroke()
    c.move_to(20, 140)
    c.line_to(488, 140)
    c.stroke()
    # doors (back wall, left)
    open_amt = 0.0
    for d in (SHARED["ding1"], SHARED["ding2"], SHARED["ding3"]):
        if d <= f < d + 30:
            open_amt = max(open_amt, ease(seg(f, d, d + 6)) * (1 - ease(seg(f, d + 22, d + 30))))
    c.set_source_rgb(0.16, 0.19, 0.28)
    c.rectangle(80, 330, 140, FLOOR_Y - 330)
    c.fill()
    leaf = 70 * (1 - open_amt)
    c.set_source_rgb(0.32, 0.36, 0.46)
    c.rectangle(80, 330, leaf, FLOOR_Y - 330)
    c.rectangle(220 - leaf, 330, leaf, FLOOR_Y - 330)
    c.fill()
    # floor counter, beside the doors at mid-height (decoration)
    rrect(c, 230, 400, 58, 40, 6)
    c.set_source_rgb(0.02, 0.03, 0.06)
    c.fill()
    text_c(c, "%02d" % floor_num(f), 259, 430, 30, CYAN)


COMPANY = "UPTIME INC."
NAMES = {"user": ("MAX", "DEV"), "dead": ("RUSH", "SALES"), "pm": ("PAM", "PROJECT MGR")}


def draw_badge(c, bx, by, name, role):
    w, h = 54, 60
    rrect(c, bx - w / 2, by, w, h, 6)
    c.set_source_rgb(0.98, 0.98, 1.0)
    c.fill()
    c.save()
    rrect(c, bx - w / 2, by, w, h, 6)
    c.clip()
    c.rectangle(bx - w / 2, by, w, 14)
    c.set_source_rgb(*CYAN)
    c.fill()
    c.restore()
    c.select_font_face("DejaVu Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    c.set_font_size(5.6)
    e = c.text_extents(COMPANY)
    c.move_to(bx - e.width / 2 - e.x_bearing, by + 10)
    c.set_source_rgb(0.04, 0.06, 0.12)
    c.show_text(COMPANY)
    text_c(c, name, bx, by + 39, 18 if len(name) <= 3 else 15.5, (0.05, 0.05, 0.1))
    c.select_font_face("DejaVu Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    c.set_font_size(6)
    e = c.text_extents(role)
    c.move_to(bx - e.width / 2 - e.x_bearing, by + 51)
    c.set_source_rgb(0.35, 0.38, 0.45)
    c.show_text(role)


def draw_human(c, name, x, lean, f, targets, savi_x):
    mood = human_mood(f, name)
    gx, gy = gaze_point(f, targets)
    skin = {"user": (0.95, 0.76, 0.49), "dead": (0.62, 0.42, 0.26), "pm": (1.0, 0.86, 0.67)}[name]
    body = {"user": (0.54, 0.56, 0.6), "dead": (0.9, 0.9, 0.92), "pm": (0.36, 0.25, 0.55)}[name]
    hair = {"user": (0.08, 0.08, 0.1), "dead": (0.05, 0.05, 0.05), "pm": (0.25, 0.14, 0.08)}[name]
    hgt = {"user": 300, "dead": 285, "pm": 305}[name]
    side = 1 if savi_x >= x else -1
    c.save()
    c.translate(x, FLOOR_Y)
    c.rotate(math.radians(lean))
    rrect(c, -42, -hgt + 70, 84, hgt - 70, 26)
    c.set_source_rgb(*body)
    c.fill()
    if name == "dead":
        c.move_to(0, -hgt + 76); c.line_to(-9, -hgt + 150); c.line_to(0, -hgt + 165); c.line_to(9, -hgt + 150)
        c.close_path(); c.set_source_rgb(0.7, 0.13, 0.2); c.fill()
    if name == "pm":
        c.set_source_rgb(0.23, 0.7, 0.45); c.set_line_width(5)
        c.move_to(-18, -hgt + 74); c.line_to(0, -hgt + 122); c.line_to(18, -hgt + 74); c.stroke()
    if name == "user" and 45 <= f < T["glow"]:  # laptop held in front
        c.set_source_rgb(0.75, 0.77, 0.8)
        rrect(c, 4, -hgt + 150, 74, 48, 5)
        c.fill()
    nm, rl = NAMES[name]
    bpos = {"user": (0, -hgt + 104), "dead": (0, -hgt + 112), "pm": (0, -hgt + 120)}[name]
    if name == "user":  # lanyard
        c.set_source_rgb(*CYAN); c.set_line_width(4)
        c.move_to(-20, -hgt + 74); c.line_to(0, -hgt + 106); c.line_to(20, -hgt + 74); c.stroke()
    draw_badge(c, bpos[0], bpos[1], nm, rl)
    # arms
    a = arm_angles(f, name, side)
    sh_y = -hgt + 92
    draw_arm(c, -38, sh_y, a[0], a[1], body, skin)
    draw_arm(c, 38, sh_y, a[2], a[3], body, skin)
    # head: tilts and dips toward the gaze target
    hx0, hy0 = x, FLOOR_Y - hgt + 30
    dx, dy = gx - hx0, gy - hy0
    dist = math.hypot(dx, dy) + 1e-6
    ux, uy = dx / dist, dy / dist
    hy = -hgt + 30 + uy * 8
    c.save()
    c.translate(ux * 5, hy)
    c.rotate(math.radians(clamp(ux * 10, -12, 12) - lean * 0.6))
    R = 46
    c.arc(0, 0, R, 0, 2 * math.pi); c.set_source_rgb(*skin); c.fill()
    c.arc(0, -7, R + 1, math.pi * 1.05, math.pi * 1.95); c.close_path(); c.set_source_rgb(*hair); c.fill()
    if name == "pm":
        c.rectangle(-R - 1, -12, 14, 46); c.rectangle(R - 13, -12, 14, 46); c.fill()
    big = mood in ("shock", "panic")
    for sx in (-16, 16):
        c.arc(sx, 2, 12 if big else 9.5, 0, 2 * math.pi); c.set_source_rgb(1, 1, 1); c.fill()
        c.arc(sx + ux * 5, 2 + uy * 5, 5.5, 0, 2 * math.pi); c.set_source_rgb(0.05, 0.05, 0.08); c.fill()
    c.set_line_width(5); c.set_source_rgb(*hair)
    for sx, sg in ((-16, 1), (16, -1)):
        if mood in ("angry", "annoyed"):
            c.move_to(sx - 11 * sg, -20); c.line_to(sx + 11 * sg, -11)
        elif mood == "flat":
            c.move_to(sx - 11, -15); c.line_to(sx + 11, -15)
        else:
            c.move_to(sx - 11, -19); c.line_to(sx + 11, -22)
        c.stroke()
    if name == "user":
        c.set_source_rgb(0.1, 0.1, 0.1); c.set_line_width(3)
        for sx in (-16, 16):
            c.arc(sx, 2, 14, 0, 2 * math.pi); c.stroke()
    c.set_source_rgb(0.3, 0.08, 0.08); c.set_line_width(5)
    if mood == "shock":
        c.save(); c.translate(0, 26); c.scale(1, 1.3); c.arc(0, 0, 8, 0, 2 * math.pi); c.restore(); c.fill()
    elif mood == "panic":
        c.save(); c.translate(0, 26); c.scale(1.5, 0.8); c.arc(0, 0, 9, 0, 2 * math.pi); c.restore(); c.fill()
    elif mood == "angry":
        rrect(c, -14, 20, 28, 12, 4); c.fill()
    else:
        c.move_to(-12, 26); c.line_to(12, 26); c.stroke()
    if name == "dead" and mood == "panic":
        frozen = T["thunk"] <= f < T["pounce"]
        c.set_source_rgba(*CYAN, 0.9)
        c.arc(38, -16 + (0 if frozen else f % 20), 5, 0, 2 * math.pi); c.fill()
    c.restore()
    c.restore()


def draw_savi(c, x, lean, f, cube_floor_x):
    expr = savi_expr(f)
    c.save()
    c.translate(x, FLOOR_Y)
    c.rotate(math.radians(lean))
    bob = 0
    if 99 <= f < 118:  # proud nod on "Locally."
        bob = math.sin(seg(f, 99, 118) * math.pi * 2) * 6
    # arms (behind body): squashed up in the pile, scratching head in close-up
    if pile_amount(f) > 0.5:
        sa = (-160, 20, 160, -20)
    elif T["cu"] <= f < T["pounce"]:
        sa = (-10, 0, 165, 55)
    else:
        sa = (-10, 0, 10, 0)
    c.save()
    draw_arm(c, -46, -250, sa[0], sa[1], (0.86, 0.88, 0.92), WHITE, ln=62, w=20)
    c.restore()
    # body
    rrect(c, -50, -280, 100, 280, 34)
    c.set_source_rgb(*WHITE)
    c.fill()
    # name plate
    rrect(c, -30, -272, 60, 22, 6)
    c.set_source_rgb(0.03, 0.03, 0.05)
    c.fill()
    text_c(c, "SAVI", 0, -255, 17, CYAN)
    # chest panel
    rrect(c, -30, -240, 60, 60, 10)
    c.set_source_rgb(0.12, 0.55, 0.68)
    c.fill()
    # glow halo
    gl = glow_level(f)
    if gl > 0:
        g = cairo.RadialGradient(0, -210, 0, 0, -210, 90)
        g.add_color_stop_rgba(0, *ORANGE, 0.75 * gl)
        g.add_color_stop_rgba(1, *ORANGE, 0)
        c.set_source(g)
        c.arc(0, -210, 90, 0, 2 * math.pi)
        c.fill()
    st = cube_state(f)
    if st[0] == "chest":
        pulse = 1 + 0.18 * math.exp(-((f - 15) / 4) ** 2) if f < 45 else 1
        c.save()
        c.translate(0, -210)
        draw_cube(c, 30 * pulse)
        c.restore()
    # hatch (glass)
    ho = hatch_open(f)
    c.save()
    c.translate(-30, -240)
    c.rotate(-ho * 1.9)
    rrect(c, 0, 0, 60, 60, 10)
    c.set_source_rgba(0.75, 0.95, 1.0, 0.22)
    c.fill_preserve()
    c.set_source_rgba(*CYAN, 0.9)
    c.set_line_width(3)
    c.stroke()
    c.restore()
    # head
    hy = -340 + bob
    c.arc(0, hy, 58, 0, 2 * math.pi)
    c.set_source_rgb(*WHITE)
    c.fill()
    rrect(c, -46, hy - 26, 92, 52, 22)
    c.set_source_rgb(0.03, 0.03, 0.05)
    c.fill()
    c.set_source_rgb(*CYAN)
    c.set_line_width(6)
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    for sx in (-20, 20):
        if expr == "smug":
            c.arc(sx, hy + 6, 11, math.pi * 1.1, math.pi * 1.9)
            c.stroke()
        elif expr == "wide":
            c.arc(sx, hy, 11, 0, 2 * math.pi)
            c.stroke()
        elif expr == "sheepish":
            s = 1 if sx < 0 else -1
            c.move_to(sx - 9 * s, hy - 8)
            c.line_to(sx + 7 * s, hy)
            c.line_to(sx - 9 * s, hy + 8)
            c.stroke()
        else:
            c.arc(sx, hy, 5, 0, 2 * math.pi)
            c.fill()
    if expr == "sheepish":  # little sweat/blush lines
        c.set_line_width(3)
        c.set_source_rgba(*CYAN, 0.7)
        for k in range(3):
            c.move_to(-30 + k * 10, hy + 40)
            c.line_to(-36 + k * 10, hy + 50)
            c.stroke()
    if T["cu"] <= f < T["pounce"] or pile_amount(f) > 0.5:  # right arm in front
        draw_arm(c, 46, -250, sa[2], sa[3], (0.86, 0.88, 0.92), WHITE, ln=62, w=20)
    else:
        draw_arm(c, 46, -250, sa[2], sa[3], (0.86, 0.88, 0.92), WHITE, ln=62, w=20)
    c.restore()


def draw_cube(c, s):
    g = cairo.RadialGradient(0, 0, 0, 0, 0, s * 1.6)
    g.add_color_stop_rgba(0, *ORANGE, 0.55)
    g.add_color_stop_rgba(1, *ORANGE, 0)
    c.set_source(g)
    c.arc(0, 0, s * 1.6, 0, 2 * math.pi)
    c.fill()
    c.rectangle(-s / 2, -s / 2, s, s)
    c.set_source_rgb(*ORANGE)
    c.fill_preserve()
    c.set_source_rgb(1, 1, 1)
    c.set_line_width(3)
    c.stroke()


def draw_cube_free(c, f, savi_x):
    st = cube_state(f)
    chest = (savi_x, FLOOR_Y - 210)
    land = (savi_x - 70, FLOOR_Y - 15)
    if st[0] == "air":
        u = st[1]
        x = lerp(chest[0], land[0], u)
        y = chest[1] + (land[1] - chest[1]) * u * u
        ang = u * 2.2
    elif st[0] == "floor":
        x, y, ang = land[0], land[1], 2.2
    elif st[0] == "zip":
        u = ease(st[1])
        x = lerp(land[0], chest[0], u)
        y = lerp(land[1], chest[1], u) - math.sin(u * math.pi) * 60
        ang = 2.2 * (1 - u)
    else:
        return
    c.save()
    c.translate(x, y)
    c.rotate(ang)
    draw_cube(c, 30)
    c.restore()
    if st[0] == "floor":  # tag + impact lines
        c.set_source_rgb(1, 1, 1)
        rrect(c, x - 34, y + 16, 68, 14, 3)
        c.fill()
        c.select_font_face("DejaVu Sans Mono")
        c.set_font_size(8)
        c.set_source_rgb(0.1, 0.1, 0.1)
        c.move_to(x - 31, y + 26)
        c.show_text("Q3_deck_FINAL")
        d = f - T["thunk"]
        if d < 8:
            c.set_source_rgba(1, 1, 1, 1 - d / 8)
            c.set_line_width(3)
            for a in (-2.6, -2.0, -1.1, -0.5):
                c.move_to(x + math.cos(a) * 22, y + math.sin(a) * 22)
                c.line_to(x + math.cos(a) * (34 + d * 3), y + math.sin(a) * (34 + d * 3))
                c.stroke()


# ---------- screen-space overlays ----------
def speaker_screen(name, f, world_to_screen, acts):
    key = {"SAVI": "savi", "USER": "user", "DEAD": "dead", "PM": "pm"}[name]
    x = acts[key][0]
    hy = FLOOR_Y - (340 if key == "savi" else 270)
    return world_to_screen(x, hy)


def draw_bubble(c, text, tx, ty, f, start):
    size = 42
    c.select_font_face(FONT)
    c.set_font_size(size)
    e = c.text_extents(text)
    bw, bh = e.width + 56, 82
    bx = clamp(tx - bw / 2, 30, 460 - bw)
    by = 130
    pop = 1.0 if start == 0 else ease_out(seg(f, start, start + 3)) * 0.15 + 0.85
    c.save()
    c.translate(bx + bw / 2, by + bh / 2)
    c.scale(pop, pop)
    c.translate(-(bx + bw / 2), -(by + bh / 2))
    # tail toward speaker
    tx2 = clamp(tx, bx + 30, bx + bw - 30)
    c.move_to(tx2 - 16, by + bh - 2)
    c.line_to(clamp(tx, 20, 520), min(ty - 40, by + bh + 60))
    c.line_to(tx2 + 16, by + bh - 2)
    c.close_path()
    c.set_source_rgb(1, 1, 1)
    c.fill()
    rrect(c, bx, by, bw, bh, 28)
    c.fill()
    c.select_font_face(FONT)
    c.set_font_size(size)
    c.move_to(bx + 28 - e.x_bearing, by + bh / 2 + e.height / 2 - 2)
    c.set_source_rgb(0.07, 0.07, 0.1)
    c.show_text(text)
    c.restore()


def draw_toast(c, f):
    if not (46 <= f < 92):
        return
    a = ease(seg(f, 46, 50)) * (1 - ease(seg(f, 86, 92)))
    c.save()
    c.translate(0, 360)
    c.translate(0, (1 - a) * -20)
    rrect(c, 90, 250, 360, 64, 18)
    c.set_source_rgba(0.13, 0.15, 0.22, 0.95 * a)
    c.fill()
    rrect(c, 104, 264, 36, 36, 9)
    c.set_source_rgba(0.2, 0.75, 0.35, a)
    c.fill()
    c.set_source_rgba(1, 1, 1, a)
    c.set_line_width(5)
    c.move_to(112, 283)
    c.line_to(120, 291)
    c.line_to(133, 274)
    c.stroke()
    c.select_font_face(FONT)
    c.set_font_size(26)
    c.move_to(152, 291)
    c.show_text("Q3_deck_FINAL saved")
    c.restore()


def draw_device(c, f, start, end, kind):
    if not (start <= f < end):
        return
    a = ease_out(seg(f, start, start + 5)) * (1 - ease(seg(f, end - 5, end)))
    if kind == "phone":
        w, h, x0, y0 = 170, 290, 40, 470
    else:
        w, h, x0, y0 = 300, 210, 40, 520
    c.save()
    c.translate(0, (1 - a) * 300)
    c.rotate(math.radians(-6 if kind == "phone" else 4))
    rrect(c, x0, y0, w, h, 22)
    c.set_source_rgb(0.08, 0.08, 0.1)
    c.fill()
    rrect(c, x0 + 10, y0 + 12, w - 20, h - 24, 14)
    c.set_source_rgb(0.95, 0.96, 0.98)
    c.fill()
    # empty folder icon
    fx, fy = x0 + w / 2, y0 + h * 0.42
    c.set_source_rgb(0.55, 0.6, 0.7)
    rrect(c, fx - 40, fy - 26, 80, 54, 6)
    c.fill()
    rrect(c, fx - 40, fy - 34, 34, 14, 4)
    c.fill()
    text_c(c, "0 items", fx, y0 + h * 0.8, 34, (0.15, 0.15, 0.2))
    c.restore()


# ---------- frame ----------
def render(f, surface):
    c = cairo.Context(surface)
    draw_bg(c, f)
    cx, cy, z = camera(f)
    jy = jolt(f)
    acts = actors(f)

    def w2s(x, y):
        return ((x - cx) * z + W / 2, (y - cy) * z + H / 2 + jy)

    c.save()
    c.translate(W / 2, H / 2 + jy)
    c.scale(z, z)
    c.translate(-cx, -cy)
    draw_elevator(c, f)
    savi_x = acts["savi"][0]
    land_x = savi_x - 70
    targets = {"savi": (savi_x, FLOOR_Y - 340), "chest": (savi_x, FLOOR_Y - 210),
               "cube": (land_x, FLOOR_Y)}
    pile = pile_amount(f)
    def hum(n):
        x, lean, vis = acts[n]
        if vis:
            draw_human(c, n, x, lean, f, targets, savi_x)
    if pile < 0.5:
        for n in ("pm", "dead", "user"):
            hum(n)
        draw_savi(c, savi_x, acts["savi"][1], f, land_x)
    else:
        hum("pm")
        draw_savi(c, savi_x, acts["savi"][1], f, land_x)
        hum("dead")
        hum("user")
    draw_cube_free(c, f, savi_x)
    c.restore()

    # overlays (screen space)
    draw_toast(c, f)
    draw_device(c, f, 135, 180, "phone")
    draw_device(c, f, 192, 236, "tablet")
    for (s, e, who, txt) in BUBBLES:
        if s <= f <= e:
            tx, ty = speaker_screen(who, f, w2s, acts)
            draw_bubble(c, txt, tx, ty, f, s)


if __name__ == "__main__":
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    if len(sys.argv) > 2:
        for fr in sys.argv[2:]:
            render(int(fr), surf)
            surf.write_to_png(f"frame_{v}_{int(fr):03d}.png")
    else:
        out = sys.stdout.buffer
        for fr in range(N):
            render(fr, surf)
            surf.flush()
            out.write(bytes(surf.get_data()))
