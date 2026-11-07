"""New end panels shared by S3-B and S3-C. Imports the original S3 panels; changes nothing in s3.py."""
import math
from kit import (W, H, INK, PAPER, rect, ellipse, text, file_sheet, desk, monitor, sfx, bubble,
                 person, office_bg, ease, clamp, lerp)
import s3


def pam_save(k, tl, label, face="neutral", flick=1):
    """Close-up insert: PAM clicks SAVE on a new version. Shows the cause on screen."""
    office_bg(k)
    person(k, "PAM", 150, 980, 1.55, pose="click", face=face, seed=44, look=(1, 0.3))
    rect(k, 250, 380, 280, 250, (0.2, 0.2, 0.23), 70)
    rect(k, 262, 392, 256, 226, (0.62, 0.84, 0.95), 71, shadow=False, lw=1.5)
    text(k, label, 390, 450, 34, INK)
    pressed = any(abs(tl - (0.12 + i * 0.14)) < 0.06 for i in range(flick))
    rect(k, 300, 500, 180, 70, (0.25, 0.55, 0.9) if not pressed else (0.15, 0.35, 0.65), 72)
    text(k, "SAVE", 390, 535, 40, (1, 1, 1))
    # cursor
    cx, cy = 420, 548
    k.c.move_to(cx, cy); k.c.line_to(cx, cy + 34); k.c.line_to(cx + 9, cy + 26); k.c.line_to(cx + 22, cy + 30)
    k.c.close_path(); k.c.set_source_rgb(1, 1, 1); k.c.fill_preserve(); k.c.set_source_rgb(*INK); k.c.set_line_width(2); k.c.stroke()
    if pressed:
        sfx(k, "CLICK!", 390, 330, 48, rot=-0.08, fill=(1, 1, 1))


def p_save28(k, t, tl):
    pam_save(k, tl, "FINAL (28)")


def p_save29(k, t, tl):
    pam_save(k, tl, "FINAL (29)", face="smug")


def p_crawl(k, t, tl):
    """RUSH crawls out from under FINAL (28), dazed."""
    office_bg(k)
    s3.door(k, 20, 280, 200, 420, 14, open_amt=1.0)
    s3._pile(k, 0.75)
    rise = ease(clamp(tl / 0.5))
    file_sheet(k, 322, 760, 400, 290, "FINAL (28)", 900, rot=-0.06, big=True)
    person(k, "RUSH", 82, lerp(1180, 930, rise), 1.1, pose="stand", face="confused", seed=34, look=(0.3, 0))


def p_shadow(k, t, tl):
    """A huge shadow grows over RUSH; FINAL (29) descends from above."""
    office_bg(k)
    s3.door(k, 20, 280, 200, 420, 14, open_amt=1.0)
    s3._pile(k, 0.75)
    look_up = tl > 0.35
    file_sheet(k, 322, 760, 400, 290, "FINAL (28)", 900, rot=-0.06, big=True)
    person(k, "RUSH", 82, 930, 1.1, pose="shock" if look_up else "stand",
           face="shock" if look_up else "confused", seed=34, look=(0, -1) if look_up else (0.3, 0))
    u = ease(clamp(tl / 1.2))
    # shadow
    k.c.save()
    k.c.translate(150, 640)
    k.c.scale(1, 0.75)
    k.c.arc(0, 0, lerp(80, 420, u), 0, 2 * math.pi)
    k.c.restore()
    k.c.set_source_rgba(0, 0, 0, 0.18 + 0.42 * u)
    k.c.fill()
    # the bottom of FINAL (29) entering from the top
    bottom = lerp(-40, 330, u)
    rect(k, 20, bottom - 700, 500, 700, PAPER, 960)
    text(k, "FINAL (29)", 270, bottom - 90, 64, INK)


def p_black(k, t, tl):
    k.c.set_source_rgb(0.04, 0.03, 0.03)
    k.c.paint()
    sfx(k, "THUNK!", 270, 470, 110, rot=-0.1)


def p_slump(k, t, tl):
    """RUSH back at his desk, covered in paper, dead-eyed."""
    office_bg(k)
    s3.door(k, 30, 330, 140, 340, 11, open_amt=1.0)
    person(k, "RUSH", 330, 800, 1.15, pose="stand", face="hollow", seed=35, look=(0, 0.6))
    for i, (x, y, r) in enumerate([(262, 620, 0.4), (395, 640, -0.5), (335, 428, 0.2), (300, 700, -0.2)]):
        file_sheet(k, x, y, 60, 76, "", 980 + i, rot=r)
    desk(k, 210, 660, 300, 20)
    monitor(k, 400, 560, 100, 90, 21)


def p_max_asks(k, t, tl):
    p_slump(k, t, tl)
    walk = ease(clamp(tl / 0.35))
    person(k, "MAX", lerp(-80, 110, walk), 760, 1.1, pose="stand", face="neutral", seed=52, look=(1, 0))


PANELS_HEAD = [(0.0, 2.0, s3.p1_ask), (2.0, 5.0, s3.p2_door), (5.0, 8.0, s3.p3_avalanche),
               (8.0, 10.7, s3.p4_gotit), (10.7, 11.2, p_save28), (11.2, 12.5, s3.p5_thunk)]

LINES_HEAD = [
    (0.05, 1.15, "Where's the final?!", 250, 330),
    (1.2, 2.0, "Downloads.", 430, 420),
    (8.4, 10.4, "GOT IT!", 290, 420),
]


def shake(t):
    d = t - 11.55
    return math.sin(d * 60) * 10 * (1 - d / 0.25) if 0 <= d < 0.25 else 0


def make_overlay(lines):
    def overlay(k, t, tl, name):
        for (s, e, txt, ax, ay) in lines:
            if s <= t < e:
                pop = 0.85 + 0.15 * ease(clamp((t - s) / 0.12))
                bubble(k, txt, ax, ay, pop=pop)
    return overlay
