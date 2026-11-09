"""S1 - Saved to the Cloud. Six panels, 15 s."""
import math
import random
from kit import (W, H, INK, PAPER, rect, ellipse, text, file_sheet, desk, monitor, popup,
                 sfx, bubble, person, office_bg, ease, clamp, lerp, cut, rough_rect_pts)

SKY = (0.62, 0.82, 0.95)
CLOUD = (0.99, 0.99, 1.0)
FOLDER = (0.95, 0.80, 0.45)


def window(k, x, y, w, h, seed, open_amt=0.0):
    rect(k, x - 10, y - 10, w + 20, h + 20, (0.96, 0.95, 0.92), seed)  # frame
    rect(k, x, y, w, h, SKY, seed + 1, shadow=False)
    if open_amt < 1:
        pw = w / 2 * (1 - open_amt)
        for px in (x, x + w - pw):
            rect(k, px, y, pw, h, (0.78, 0.9, 0.98), seed + 2 + int(px), shadow=False, lw=2)


def cloud(k, cx, cy, s, face="sleepy", seed=60, puff=1.0):
    blobs = [(-0.55, 0.1, 0.42), (-0.2, -0.25, 0.5), (0.25, -0.2, 0.48), (0.6, 0.12, 0.4), (0.0, 0.2, 0.55)]
    for i, (bx, by, br) in enumerate(blobs):
        ellipse(k, cx + bx * s * puff, cy + by * s, br * s * puff, br * s * 0.85, CLOUD, seed + i)
    c = k.c
    c.set_source_rgb(*INK)
    c.set_line_width(5)
    ey = cy - 0.05 * s
    for sx in (-0.2, 0.2):
        x = cx + sx * s
        if face in ("sleepy",):
            c.move_to(x - 16, ey); c.line_to(x + 16, ey); c.stroke()
        elif face in ("squeeze", "sneeze"):
            c.move_to(x - 16, ey - 10); c.line_to(x + 8, ey); c.line_to(x - 16, ey + 10); c.stroke() if sx < 0 else None
            if sx > 0:
                c.move_to(x + 16, ey - 10); c.line_to(x - 8, ey); c.line_to(x + 16, ey + 10); c.stroke()
        else:  # cough
            c.arc(x, ey, 9, 0, 2 * math.pi); c.stroke()
    my = cy + 0.18 * s
    if face == "sleepy":
        c.move_to(cx - 18, my); c.curve_to(cx - 6, my + 8, cx + 6, my + 8, cx + 18, my); c.stroke()
    elif face == "cough":
        ellipse(k, cx, my, 16, 12, (0.35, 0.1, 0.1), seed + 9, shadow=False)
    elif face == "squeeze":
        ellipse(k, cx - 0.32 * s, my - 4, 20, 14, (1, 0.75, 0.75), seed + 10, shadow=False, outline=False)
        ellipse(k, cx + 0.32 * s, my - 4, 20, 14, (1, 0.75, 0.75), seed + 11, shadow=False, outline=False)
        c.set_source_rgb(*INK)
        c.move_to(cx - 10, my); c.line_to(cx + 10, my); c.stroke()
    elif face == "sneeze":
        ellipse(k, cx, my + 6, 34, 26, (0.35, 0.1, 0.1), seed + 12, shadow=False)


def folder(k, x, y, w, seed, rot=0.0):
    c = k.c
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    h = w * 0.72
    rect(k, -w / 2, -h / 2 - 10, w * 0.38, 16, FOLDER, seed + 1, shadow=False)
    rect(k, -w / 2, -h / 2, w, h, FOLDER, seed)
    text(k, "CONFIDENTIAL", 0, 0, w * 0.13, (0.75, 0.1, 0.1), rot=-0.15)
    c.restore()


def wedding_photo(k, x, y, seed, rot=-0.1):
    c = k.c
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    rect(k, -60, -46, 120, 92, (1, 1, 1), seed)
    rect(k, -50, -36, 100, 72, (0.85, 0.93, 0.98), seed + 1, shadow=False, lw=1.5)
    c.set_source_rgb(*INK)
    c.set_line_width(3)
    for sx, col in ((-16, (1, 1, 1)), (16, (0.15, 0.15, 0.2))):
        ellipse(k, sx, -14, 8, 8, (0.95, 0.8, 0.6), seed + 3 + sx, shadow=False, lw=1.5)
        cut(k, [(sx - 10, 30), (sx + 10, 30), (sx + 6, -4), (sx - 6, -4)], col, shadow=False, lw=1.5)
    text(k, "♥", 0, -28, 18, (0.85, 0.15, 0.25), font="DejaVu Sans")
    c.restore()


def p1_save(k, t, tl):
    office_bg(k)
    window(k, 330, 230, 170, 200, 70)
    cloud(k, 420, 300, 70, seed=61)
    person(k, "MAX", 90, 740, 1.05, pose="stand", face="confused", seed=50, look=(1, 0))
    desk(k, 150, 640, 360, 24)
    monitor(k, 165, 510, 190, 140, 26)
    popup(k, 171, 552, 178, 44, "Saved to cloud", 27, check=True)
    pam_pose = "point_r" if tl >= 1.25 else "click"
    person(k, "PAM", 430, 800, 1.0, pose=pam_pose, face="neutral", seed=42,
           look=(0.6, -1) if tl >= 1.25 else (-1, 0.3))
    rect(k, 360, 640, 150, 24, (0.55, 0.38, 0.24), 29)  # desk edge in front of PAM


def p2_window(k, t, tl):
    rect(k, -20, -20, W + 40, H + 40, SKY, 80, shadow=False, outline=False)
    oa = ease(clamp(tl / 0.5))
    cloud(k, 330, 380, 260, face="sleepy", seed=62)
    # window frame edges in the foreground
    rect(k, -20, 120, 60, 760, (0.96, 0.95, 0.92), 81)
    rect(k, -20, 840, W + 40, 140, (0.96, 0.95, 0.92), 82)
    if oa < 1:
        rect(k, 40, 120, 500 * (1 - oa), 720, (0.78, 0.9, 0.98), 83, lw=2)
    p = person(k, "MAX", 140, 1000, 1.25, pose="reach_r", face="confused", seed=51, look=(1, -0.3))
    if tl > 0.9:
        hx, hy = p["hands"][1]
        wedding_photo(k, hx + 30, hy - 40, 90)


def p3_cough(k, t, tl):
    rect(k, -20, -20, W + 40, H + 40, SKY, 80, shadow=False, outline=False)
    face = "cough" if (int(tl * 4) % 2 == 0 and tl > 0.3) else "sleepy"
    cloud(k, 330, 360, 260, face=face, seed=62)
    rect(k, -20, 120, 60, 760, (0.96, 0.95, 0.92), 81)
    rect(k, -20, 840, W + 40, 140, (0.96, 0.95, 0.92), 82)
    person(k, "MAX", 140, 1000, 1.25, pose="reach_r", face="shock", seed=51, look=(1, -0.5))
    r = random.Random(3)
    for i in range(7):
        st = 0.3 + i * 0.35
        a = (tl - st) / 0.8
        if a >= 0:
            a = min(a, 1.0)
            x = lerp(330, r.uniform(60, 480), a)
            y = lerp(440, r.uniform(500, 760), a) - math.sin(a * math.pi) * 140
            folder(k, x, y, 110, 300 + i, rot=a * r.uniform(-2, 2))
    if tl > 0.3:
        sfx(k, "*COUGH*", 400, 600, 50, rot=0.1, fill=(1, 1, 1))
    # PAM's screen warning, as an inset card at the top
    if tl > 1.0:
        popup(k, 60, 118, 410, 56, "Cloud storage almost full", 28, warn=True)


def p4_inhale(k, t, tl):
    rect(k, -20, -20, W + 40, H + 40, SKY, 80, shadow=False, outline=False)
    u = ease(clamp(tl / 1.8))
    cloud(k, 330, 360, 260 * (1 + 0.25 * u), face="squeeze", seed=62, puff=1 + 0.15 * u)
    rect(k, -20, 120, 60, 760, (0.96, 0.95, 0.92), 81)
    rect(k, -20, 840, W + 40, 140, (0.96, 0.95, 0.92), 82)
    person(k, "MAX", lerp(140, 110, u), 1000, 1.25, pose="back", face="shock", seed=51, look=(1, -0.5))
    sfx(k, "ah... ah...", 300, 170, 50, rot=-0.06, fill=(1, 1, 1))


def p5_sneeze(k, t, tl):
    rect(k, -20, -20, W + 40, H + 40, SKY, 80, shadow=False, outline=False)
    cloud(k, 330, 330, 300, face="sneeze", seed=62, puff=1.1)
    r = random.Random(5)
    a = ease(clamp(tl / 0.8))
    for i in range(34):
        ang = r.uniform(0, 2 * math.pi)
        d = a * r.uniform(150, 650)
        x, y = 330 + math.cos(ang) * d, 380 + math.sin(ang) * d * 1.2
        if i % 4 == 0:
            folder(k, x, y, 90, 400 + i, rot=ang * 2)
        else:
            file_sheet(k, x, y, 64, 80, ["IMG_2231", "tax_2014", "passwords.txt", "Q3_deck"][i % 4] if i % 3 == 0 else "",
                       420 + i, rot=ang * 3)
    # MAX with a sheet stuck to his face
    p = person(k, "MAX", 120, 1000, 1.25, pose="shock", face="shock", seed=51)
    hx, hy = p["head"]
    file_sheet(k, hx + 4, hy + 6, 120, 140, "", 460, rot=0.12)
    sfx(k, "ACHOO!", 300, 190, 104, rot=-0.12)


def p6_shared(k, t, tl):
    office_bg(k)
    window(k, 330, 250, 170, 200, 70, open_amt=1.0)
    r = random.Random(8)
    for i in range(26):  # paper everywhere
        file_sheet(k, r.uniform(0, 540), r.uniform(150, 920), 60, 76, "", 600 + i, rot=r.uniform(-1, 1))
    p = person(k, "MAX", 120, 760, 1.1, pose="stand", face="neutral", seed=50)
    hx, hy = p["head"]
    file_sheet(k, hx + 2, hy + 6, 112, 130, "", 460, rot=0.12)
    person(k, "PAM", 370, 800, 1.15, pose="pleased", face="pleased", seed=42)
    file_sheet(k, 380, 560, 56, 70, "", 690, rot=0.4)


PANELS = [(0.0, 2.0, p1_save), (2.0, 5.0, p2_window), (5.0, 8.0, p3_cough),
          (8.0, 10.0, p4_inhale), (10.0, 12.0, p5_sneeze), (12.0, 15.0, p6_shared)]

LINES = [
    (0.1, 1.2, "Where's the file?", 90, 360),
    (1.25, 2.0, "Cloud.", 430, 420),
    (3.4, 4.7, "Who's this?", 170, 560),
    (13.0, 15.0, "Nice. Shared.", 370, 420),
]


def shake(t):
    d = t - 10.0
    return math.sin(d * 55) * 9 * (1 - d / 0.3) if 0 <= d < 0.3 else 0


def overlay(k, t, tl, name):
    for (s, e, txt, ax, ay) in LINES:
        if s <= t < e:
            pop = 0.85 + 0.15 * ease(clamp((t - s) / 0.12))
            bubble(k, txt, ax, ay, pop=pop)
