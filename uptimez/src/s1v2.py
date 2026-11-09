"""S1-v2: 'Nice. Shared.' then the punch turns on PAM, and her panic save restarts the loop.
Imports the original S1 panels; changes nothing in s1.py."""
import math
from kit import (W, H, INK, PAPER, rect, ellipse, text, file_sheet, monitor, popup, sfx, bubble,
                 person, office_bg, ease, clamp, lerp)
import s1

LABEL = ["PAM'S", "SEARCH", "HISTORY"]


def p7_peel(k, t, tl):
    """MAX peels the sheet off his face; close-up of what it says."""
    if tl < 0.3:
        office_bg(k)
        p = person(k, "MAX", 270, 1000, 1.7, pose="hold_up", face="neutral", seed=53)
        hx, hy = p["head"]
        file_sheet(k, hx + lerp(0, 40, tl / 0.3), hy - lerp(0, 50, tl / 0.3), 190, 220, "", 460, rot=0.12 + tl)
        return
    office_bg(k)
    rect(k, 50, 250, 440, 520, PAPER, 461)
    for i, word in enumerate(LABEL):
        text(k, word, 270, 380 + i * 105, 74, INK)


def p8_pam_drop(k, t, tl):
    office_bg(k)
    face = "pleased" if tl < 0.15 else ("shock" if tl < 0.45 else "panic")
    person(k, "PAM", 270, 1100, 2.3, pose="stand", face=face, seed=45, look=(0, 0))


def p9_panic_save(k, t, tl):
    office_bg(k)
    person(k, "PAM", 150, 980, 1.55, pose="click", face="panic", seed=44, look=(1, 0.3))
    rect(k, 250, 380, 280, 250, (0.2, 0.2, 0.23), 70)
    rect(k, 262, 392, 256, 226, (0.62, 0.84, 0.95), 71, shadow=False, lw=1.5)
    text(k, "PAM'S SEARCH HISTORY", 390, 450, 19, INK)
    pressed = int(tl * 12) % 2 == 0
    rect(k, 300, 500, 180, 70, (0.25, 0.55, 0.9) if not pressed else (0.15, 0.35, 0.65), 72)
    text(k, "SAVE", 390, 535, 40, (1, 1, 1))
    sfx(k, "CLICK CLICK CLICK", 270, 300, 40, rot=-0.06, fill=(1, 1, 1))


def p10_saved(k, t, tl):
    office_bg(k)
    s1.window(k, 300, 180, 210, 230, 70)
    s1.cloud(k, 405, 270, 85, face="cough", seed=61)  # wide-eyed, mouth open: horror
    monitor(k, 50, 470, 380, 260, 26)
    popup(k, 70, 570, 340, 56, "Saved to cloud", 27, check=True)


PANELS = [(0.0, 2.0, s1.p1_save), (2.0, 4.5, s1.p2_window), (4.5, 7.0, s1.p3_cough),
          (7.0, 8.5, s1.p4_inhale), (8.5, 10.5, s1.p5_sneeze), (10.5, 11.8, s1.p6_shared),
          (11.8, 12.9, p7_peel), (12.9, 13.6, p8_pam_drop), (13.6, 14.3, p9_panic_save),
          (14.3, 15.0, p10_saved)]

LINES = [
    (0.1, 1.2, "Where's the file?", 90, 360),
    (1.25, 2.0, "Cloud.", 430, 420),
    (3.0, 4.3, "Who's this?", 170, 560),
    (10.6, 11.75, "Nice. Shared.", 370, 420),
]


def shake(t):
    d = t - 8.5
    return math.sin(d * 55) * 9 * (1 - d / 0.3) if 0 <= d < 0.3 else 0


def overlay(k, t, tl, name):
    for (s, e, txt, ax, ay) in LINES:
        if s <= t < e:
            pop = 0.85 + 0.15 * ease(clamp((t - s) / 0.12))
            bubble(k, txt, ax, ay, pop=pop)
