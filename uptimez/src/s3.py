"""S3 - Check Downloads. Six panels, 15 s."""
import math
import random
from kit import (W, H, INK, PAPER, rect, ellipse, text, file_sheet, desk, monitor, popup, door,
                 sfx, bubble, person, office_bg, ease, clamp, lerp, rough_ellipse_pts, cut)

LABELS = ["FINAL", "FINAL (3)", "invoice (38).pdf", "setup_2016.exe", "FINAL (14)", "IMG_0001",
          "New folder (7)", "FINAL (9)", "contract_v2.pdf", "FINAL (21)", "meme.gif", "FINAL (6)"]


def hoard(k, x0, y0, x1, y1, seed, n=40):
    r = random.Random(seed)
    for i in range(n):
        x = r.uniform(x0, x1)
        y = lerp(y1, y0, (i / n) ** 0.8) + r.uniform(-20, 20)
        file_sheet(k, x, y, 70, 88, LABELS[i % len(LABELS)] if i % 3 == 0 else "", seed + i, rot=r.uniform(-0.6, 0.6))


def p1_ask(k, t, tl):
    office_bg(k)
    door(k, 30, 330, 140, 340, 11, open_amt=0.0)
    # RUSH standing, monitor turned to the side so his face reads
    person(k, "RUSH", 250, 720, 1.15, pose="panic", face="panic", seed=30, look=(-1, 0))
    desk(k, 170, 600, 160, 20)
    monitor(k, 175, 500, 90, 76, 21)
    # PAM seated on the right, typing, never looking up
    person(k, "PAM", 430, 790, 1.05, pose="type", face="neutral", seed=40, look=(1, 0.8))
    desk(k, 360, 640, 200, 22)
    monitor(k, 470, 530, 80, 90, 23)


def p2_door(k, t, tl):
    office_bg(k)
    oa = ease(clamp((tl - 0.1) / 0.6))
    # contents behind the door: a hoard of files, drawn first then the door over it
    door(k, 90, 250, 300, 560, 12, open_amt=1.0)
    k.c.save()
    k.c.rectangle(90, 250, 300, 560)
    k.c.clip()
    hoard(k, 100, 260, 380, 800, 77, n=55)
    k.c.restore()
    if oa < 1:
        rect(k, 90, 250, 300 * (1 - oa), 560, (0.80, 0.62, 0.42), 13)
    person(k, "RUSH", 450, 960, 1.15, pose="back", face="shock", seed=31, look=(-1, -0.3))


def _pile(k, u, seed=5):
    # growing paper mound across the bottom
    top = lerp(900, 560, u)
    pts = [(-30, 1000), (-30, top + 120), (120, top + 30), (270, top), (420, top + 40), (580, top + 140), (580, 1000)]
    cut(k, pts, PAPER, shadow=True)
    r = random.Random(seed)
    for i in range(int(10 + 30 * u)):
        x = r.uniform(0, 540)
        y = r.uniform(top + 20, 960)
        file_sheet(k, x, y, 66, 82, LABELS[i % len(LABELS)] if i % 4 == 0 else "", 500 + i, rot=r.uniform(-0.8, 0.8))
    return top


def p3_avalanche(k, t, tl):
    office_bg(k)
    door(k, 20, 280, 200, 420, 14, open_amt=1.0)
    u = ease(clamp(tl / 2.2))
    # RUSH being buried (drawn before the pile)
    if u < 0.85:
        person(k, "RUSH", 330, 760 + u * 60, 1.0, pose="shock", face="shock", seed=32, look=(-1, -0.5))
    _pile(k, u)
    # flying sheets from the door
    r = random.Random(9)
    for i in range(16):
        st = r.uniform(0, 2.2)
        a = (tl - st) / 0.9
        if 0 <= a <= 1:
            x = lerp(120, r.uniform(200, 520), a)
            y = lerp(420, r.uniform(560, 860), a) - math.sin(a * math.pi) * 120
            file_sheet(k, x, y, 74, 92, LABELS[i % len(LABELS)], 700 + i, rot=a * r.uniform(-3, 3))
    sfx(k, "RUMBLE!", 300, 230, 64, rot=0.08)


def p4_gotit(k, t, tl):
    office_bg(k)
    door(k, 20, 280, 200, 420, 14, open_amt=1.0)
    rise = ease(clamp(tl / 0.35))
    person(k, "RUSH", 290, lerp(1000, 720, rise), 1.1, pose="hold_up", face="happy", seed=33)
    # FINAL (27) in his raised hand
    file_sheet(k, 360, lerp(560, 300, rise), 130, 160, "FINAL (27)", 801, rot=0.08, big=True)
    _pile(k, 0.75)


def p5_thunk(k, t, tl):
    office_bg(k)
    door(k, 20, 280, 200, 420, 14, open_amt=1.0)
    drop = clamp(tl / 0.35)
    if drop < 1:
        person(k, "RUSH", 290, 720, 1.1, pose="hold_up", face="shock", seed=33, look=(0, -1))
        file_sheet(k, 360, 300, 130, 160, "FINAL (27)", 801, rot=0.08, big=True)
        _pile(k, 0.75)
        file_sheet(k, 290, lerp(-500, 380, drop ** 2), 440, 540, "FINAL (28)", 900, rot=-0.05, big=True)
    else:
        _pile(k, 0.75)
        # flattened: his arm pokes out from under FINAL (28), still holding FINAL (27)
        rect(k, 470, 470, 20, 80, (0.93, 0.93, 0.95), 950, shadow=False)
        ellipse(k, 480, 470, 13, 13, (0.62, 0.42, 0.26), 951, shadow=False)
        file_sheet(k, 482, 420, 95, 115, "FINAL (27)", 801, rot=0.25, big=True)
        file_sheet(k, 270, 690, 470, 330, "FINAL (28)", 900, rot=-0.06, big=True)
        # feet sticking out the bottom-left
        rect(k, 40, 830, 50, 22, (0.15, 0.12, 0.12), 952)
        rect(k, 96, 838, 50, 22, (0.15, 0.12, 0.12), 953)
        if tl - 0.35 < 0.5:
            c = k.c
            c.set_source_rgb(*INK)
            c.set_line_width(4)
            for a in (-2.8, -2.4, -0.6, -0.3):
                c.move_to(270 + math.cos(a) * 250, 650 + math.sin(a) * 180)
                c.line_to(270 + math.cos(a) * 300, 650 + math.sin(a) * 220)
                c.stroke()
        sfx(k, "THUNK!", 270, 300, 96, rot=-0.1)


def p6_updated(k, t, tl):
    office_bg(k)
    person(k, "PAM", 230, 860, 1.4, pose="type", face="smug", seed=41, look=(1, 0.4))
    desk(k, 60, 680, 460, 23)
    monitor(k, 330, 470, 190, 200, 24)
    popup(k, 342, 550, 166, 46, "FINAL (28)", 25, check=True)


PANELS = [(0.0, 2.0, p1_ask), (2.0, 5.0, p2_door), (5.0, 8.0, p3_avalanche),
          (8.0, 11.0, p4_gotit), (11.0, 13.0, p5_thunk), (13.0, 15.0, p6_updated)]

LINES = [  # (start, end, text, anchor_x, anchor_y)
    (0.05, 1.15, "Where's the final?!", 250, 330),
    (1.2, 2.0, "Downloads.", 430, 420),
    (8.4, 10.6, "GOT IT!", 290, 420),
    (13.25, 15.0, "Just updated it.", 230, 420),
]


def shake(t):
    d = t - 11.35
    return math.sin(d * 60) * 10 * (1 - d / 0.25) if 0 <= d < 0.25 else 0


def overlay(k, t, tl, name):
    for (s, e, txt, ax, ay) in LINES:
        if s <= t < e:
            pop = 0.85 + 0.15 * ease(clamp((t - s) / 0.12))
            bubble(k, txt, ax, ay, pop=pop)
