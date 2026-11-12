"""Props and new characters for "How Sofía Survived Day One": the robot, the coffee maker, the railway,
the partition, Pam's thermos. Same flat paper-cutout kit as the series.
World convention (storyboard set): floor line at y 640; heads of the seated Don and the robot at y 528."""
import math
import kit
import brand
from kit import INK, cut, rect, ellipse, text

ROBOT_BODY = (0.80, 0.83, 0.87)
ROBOT_DARK = (0.30, 0.33, 0.38)
SCREEN = (0.10, 0.16, 0.20)
SCREEN_INK = (0.45, 0.95, 0.70)
TIE = (0.80, 0.10, 0.12)
MACHINE = (0.28, 0.30, 0.34)
METAL = (0.70, 0.72, 0.75)
COFFEE = (0.36, 0.20, 0.10)
TRACK = (0.45, 0.30, 0.18)
TRAIN = (0.20, 0.45, 0.78)
GREEN = (0.20, 0.70, 0.40)
PARTITION = (0.62, 0.66, 0.72)

ROBOT_POSES = {   # same convention as kit.arm: 0 = down, +90 = right, 180 = up
    "stand": (-10, 0, 10, 0),
    "tug": (-10, 0, -20, -140),       # right hand up at its tie knot (copies Don)
    "wave": (-10, 0, 112, -42),       # Don's lazy wave toward Pam
    "hold": (-60, 60, 60, -60),       # holding a paper in front
}


def robot(k, x, feet, s=1.0, pose="stand", eyes="neutral", look=(0, 0), tilt=0.0, talk=0.0, seed=300,
          paper=False, badge=None):
    """Waist-high robot on wheels; head (a screen) centred at feet - 302*s, level with Don's seated head.
    Returns head and hands in canvas coordinates."""
    c = k.c
    c.save(); c.translate(x, feet); c.scale(s, s)
    for wx in (-30, 30):                                  # wheels
        ellipse(k, wx, -14, 15, 15, ROBOT_DARK, seed + wx, lw=2)
    rect(k, -8, -262, 16, 40, ROBOT_DARK, seed + 3, shadow=False, lw=1.6)   # neck, joins the head
    rect(k, -46, -230, 92, 210, ROBOT_BODY, seed + 1)    # body
    rect(k, -30, -170, 60, 34, METAL, seed + 2, shadow=False, lw=1.6)
    c.set_source_rgb(*INK); c.set_line_width(1.6)
    for i in range(3):
        c.move_to(-22 + i * 22, -162); c.line_to(-22 + i * 22, -144); c.stroke()
    cut(k, [(0, -228), (-8, -208), (0, -180), (8, -208)], TIE, shadow=False, lw=1.6)   # tiny red tie
    if badge:                                            # company badge on the chest plate (v3 storyboard)
        rect(k, -6, -181, 12, 7, (0.45, 0.47, 0.52), seed + 41, shadow=False, lw=1.3)
        rect(k, -33, -176, 66, 38, (1, 1, 1), seed + 40, shadow=False, lw=1.6)
        c.set_source_rgb(*brand.GREEN); c.rectangle(-31.5, -174.5, 63, 10); c.fill()
        brand.mark(c, -29, -173.5, 8, zzz=False)
        text(k, badge, 0, -150, 13, INK, font="Inter", bold=True)
    a = ROBOT_POSES[pose]
    hands = []
    for side, (u, f) in ((-1, (a[0], a[1])), (1, (a[2], a[3]))):
        hands.append(kit.arm(k, side * 50, -218, u, f, ROBOT_DARK, METAL, seed + 10 + side, ln=48, w=15))
    # head: a screen, tilted with Don's head tilt
    c.save(); c.translate(0, -302); c.rotate(tilt)
    rect(k, -62, -52, 124, 104, ROBOT_BODY, seed + 20)
    rect(k, -50, -40, 100, 80, SCREEN, seed + 21, shadow=False, lw=1.8)
    lx, ly = look[0] * 9, look[1] * 6
    c.set_source_rgb(*SCREEN_INK)
    if eyes == "happy":
        c.set_line_width(5)
        for ex in (-20, 20):
            c.arc(ex + lx, -2 + ly, 9, math.pi * 1.15, math.pi * 1.85); c.stroke()
    elif eyes == "flat":
        c.set_line_width(5)
        for ex in (-20, 20):
            c.move_to(ex - 9 + lx, -6 + ly); c.line_to(ex + 9 + lx, -6 + ly); c.stroke()
    else:
        for ex in (-20, 20):
            c.rectangle(ex - 6 + lx, -16 + ly, 12, 18 if eyes != "wide" else 24); c.fill()
    c.set_line_width(4)
    if talk > 0.05:
        c.rectangle(-12, 14, 24, 4 + 10 * talk); c.fill()
    else:
        c.move_to(-12, 18); c.line_to(12, 18); c.stroke()
    ellipse(k, 0, -62, 6, 6, (0.95, 0.30, 0.25), seed + 22, shadow=False, lw=1.5)   # antenna light
    c.set_source_rgb(*INK); c.set_line_width(2); c.move_to(0, -56); c.line_to(0, -52); c.stroke()
    c.restore()
    if paper:
        (ax, ay), (bx, by) = hands
        kit.file_sheet(k, (ax + bx) / 2, (ay + by) / 2 - 16, 60, 74, "", seed + 30)
    c.restore()
    return {"head": (x, feet - 302 * s), "hands": [(x + hx * s, feet + hy * s) for hx, hy in hands]}


def coffee_maker(k, x, y, s=1.0, state="waiting", pour=0.0, overflow=0.0, seed=400, sticker=True, cup=True,
                 sticker_at=(-30, -40, -0.12), stream=True):
    """Machine on a counter; (x, y) = bottom centre. state: waiting | approved | off.
    sticker_at = (x, y, rotation) of the 99.9% UPTIME sticker; the default is the v1 spot, which the
    v2 storyboard moves to the lower right, clear of the coffee stream."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    rect(k, -60, -150, 120, 150, MACHINE, seed)
    rect(k, -50, -140, 100, 46, SCREEN, seed + 1, shadow=False, lw=1.8)
    if state == "waiting":
        text(k, "WAITING FOR", 0, -126, 13, (1.0, 0.75, 0.25), font="Inter", bold=True)
        text(k, "APPROVAL", 0, -108, 13, (1.0, 0.75, 0.25), font="Inter", bold=True)
    elif state == "approved":
        text(k, "APPROVED", 0, -116, 17, SCREEN_INK, font="Inter", bold=True)
    ellipse(k, 38, -74, 12, 12, (0.85, 0.20, 0.20), seed + 2, lw=2)              # BREW button
    text(k, "BREW", 38, -54, 10, (1, 1, 1), font="Inter", bold=True)
    rect(k, -30, -80, 26, 16, METAL, seed + 3, shadow=False, lw=1.5)           # spout
    if sticker:
        c.save(); c.translate(sticker_at[0], sticker_at[1]); c.rotate(sticker_at[2])
        rect(k, -30, -10, 60, 20, (1, 1, 1), seed + 4, shadow=False, lw=1.3)
        text(k, "99.9% UPTIME", 0, 1, 7.5, brand.NAVY, font="Inter", bold=True)
        c.restore()
    if cup:
        if overflow > 0:                                  # spill on the counter, under the cup
            ellipse(k, -17, -1, 22 + 26 * overflow, 5 + 3 * overflow, COFFEE, seed + 6, shadow=False, lw=1.4)
        if pour > 0 and stream:                           # stream=False: full cup, tap closed (loop reset)
            c.set_source_rgb(*COFFEE); c.rectangle(-20, -64, 6, 34 * min(1, pour * 3)); c.fill()
        rect(k, -32, -30, 30, 30, (1, 1, 1), seed + 5, shadow=False, lw=1.8)
        if pour > 0:
            lvl = min(1.0, pour) * 26
            c.set_source_rgb(*COFFEE); c.rectangle(-30, -2 - lvl, 26, lvl); c.fill()
        if overflow > 0:                                  # running down the cup's sides
            c.rectangle(-34, -30, 4, 30 * overflow); c.fill(); c.rectangle(-2, -30, 4, 30 * overflow); c.fill()
    c.restore()


def counter(k, x0, x1, top, seed=410):
    rect(k, x0, top, x1 - x0, 18, (0.55, 0.40, 0.28), seed)
    rect(k, x0 + 6, top + 18, x1 - x0 - 12, 100, (0.70, 0.56, 0.40), seed + 1)


def railway(k, cx, cy, rx, ry, front=True, seed=420):
    """Ellipse of toy track; draw the back half before the desk and the front half after it."""
    c = k.c
    a0, a1 = (0, math.pi) if front else (math.pi, 2 * math.pi)
    for off, lw in ((-6, 3), (6, 3)):
        c.set_source_rgb(*TRACK); c.set_line_width(lw)
        c.save(); c.translate(cx, cy); c.scale(rx + off, ry + off * ry / rx)
        c.arc(0, 0, 1, a0, a1); c.restore(); c.stroke()
    c.set_source_rgb(*TRACK); c.set_line_width(3)
    for i in range(18):
        a = a0 + (a1 - a0) * (i + 0.5) / 18
        px, py = cx + math.cos(a) * rx, cy + math.sin(a) * ry
        c.move_to(px - math.cos(a) * 9, py - math.sin(a) * 9 * ry / rx)
        c.line_to(px + math.cos(a) * 9, py + math.sin(a) * 9 * ry / rx); c.stroke()


def train(k, cx, cy, rx, ry, ang, button_y=None, pressed=False, seed=430, plaque=False):
    """Engine at angle `ang` on the ellipse, the APPROVE wagon just behind it; the button sits on a tall
    pedestal whose top is at button_y (desk-top height). Returns the button centre."""
    px, py = cx + math.cos(ang) * rx, cy + math.sin(ang) * ry
    bx, by = cx + math.cos(ang - 0.42) * rx, cy + math.sin(ang - 0.42) * ry
    rect(k, px - 26, py - 30, 52, 30, TRAIN, seed, lw=2)
    rect(k, px - 22, py - 46, 18, 18, TRAIN, seed + 1, shadow=False, lw=2)
    for wx in (-14, 14):
        ellipse(k, px + wx, py, 7, 7, INK, seed + 2 + wx, shadow=False, outline=False)
    rect(k, bx - 24, by - 22, 48, 22, (0.85, 0.70, 0.25), seed + 5, lw=2)
    top = by - 120 if button_y is None else button_y
    rect(k, bx - 5, top, 10, by - 22 - top, METAL, seed + 6, shadow=False, lw=1.5)
    r = 21 if not pressed else 19
    ellipse(k, bx, top - 6, r + 6, 9, (0.15, 0.40, 0.25), seed + 7, shadow=False, lw=2)
    ellipse(k, bx, top - 12 + (3 if pressed else 0), r, 12, GREEN, seed + 8, lw=2)
    if plaque:                                           # v3: label on a dark plate, readable on any background
        rect(k, bx - 31, top + 5, 62, 18, (0.12, 0.30, 0.20), seed + 9, shadow=False, lw=1.6)
    text(k, "APPROVE", bx, top + 14, 11, (1, 1, 1), font="Inter", bold=True)
    return bx, top - 12


def partition(k, x0, x1, top, bottom, seed=440):
    rect(k, x0, top, x1 - x0, bottom - top, PARTITION, seed)
    c = k.c
    c.set_source_rgba(1, 1, 1, 0.25)
    for i in range(1, 4):
        c.rectangle(x0 + (x1 - x0) * i / 4 - 1, top + 10, 2, bottom - top - 20); c.fill()


def thermos(k, x, y, s=1.0, seed=450):
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    rect(k, -12, -56, 24, 56, (0.85, 0.30, 0.35), seed)
    rect(k, -10, -66, 20, 12, (0.25, 0.25, 0.28), seed + 1, shadow=False, lw=1.6)
    c.restore()


def mug(k, x, y, s=1.0, steam=0.0, seed=460):
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    rect(k, -14, -26, 28, 26, (1, 1, 1), seed, lw=2)
    c.set_source_rgb(*INK); c.set_line_width(2.4); c.arc(16, -13, 7, -1.4, 1.4); c.stroke()
    if steam > 0:
        c.set_source_rgba(0.6, 0.6, 0.6, 0.6 * steam); c.set_line_width(2.4)
        for i, dx in enumerate((-6, 4)):
            c.move_to(dx, -32); c.curve_to(dx - 6, -42, dx + 6, -48, dx, -58); c.stroke()
    c.restore()
