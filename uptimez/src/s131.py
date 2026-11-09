"""Saved to Cloud S1v3.1 - rough A/B animatic. 6 shots, 15 s. PAM -> CLOUD -> DON.
A and B differ only in shot 5 (the private page): A = three searches, B = one line.
New module only: s1.py, kit.py, pt4.py, pt42.py are untouched (face drawing wrapped at runtime for lip-sync).
Run through s131a.py / s131b.py."""
import json
import math
import os
import random
import kit
import pt4
import pt42
import s1
from kit import W, H, INK, PAPER, rect, ellipse, text, file_sheet, monitor, popup, sfx, bubble, ease, clamp, lerp

VARIANT = "B"
_HERE = os.path.dirname(os.path.abspath(__file__))
SYNC = json.load(open(os.path.join(_HERE, "s131_sync.json")))
ENV = SYNC["env"]
STATE = {"t": 0.0, "who": None, "skin": (1, 1, 1)}
PRIV = (0.96, 0.62, 0.66)       # PAM's private file: pink, bigger than the rest
DESK_TOP = (0.62, 0.44, 0.28)
person = pt42.branded_person

# ---------------------------------------------------------------- lip-sync (runtime wrapper)
_orig_face = kit.face_draw


def face_live(k, x, y, face, look, glasses=False, seed=0):
    _orig_face(k, x, y, face, look, glasses=glasses, seed=seed)
    who, f = STATE["who"], int(STATE["t"] * 30)
    if who in ENV and 0 <= f < 450 and ENV[who][f] > 0.12:
        o = ENV[who][f]
        ellipse(k, x, y + 28, 19, 12, STATE["skin"], 9100, shadow=False, outline=False)
        ellipse(k, x, y + 30, 13 + 5 * o, 3 + 14 * o, (0.35, 0.08, 0.08), 9101, shadow=False, lw=2)


kit.face_draw = face_live


def who(name, k, *a, **kw):
    STATE["who"], STATE["skin"] = name, kit.PEOPLE[name]["skin"]
    out = person(k, name, *a, **kw)
    STATE["who"] = None
    return out


# ---------------------------------------------------------------- props
def private_file(k, x, y, w, seed, rot=0.0):
    c = k.c
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    h = w * 1.2
    rect(k, -w / 2, -h / 2, w, h, PRIV, seed)
    text(k, "PAM", 0, -h * 0.12, w * 0.24, INK)
    text(k, "PRIVATE", 0, h * 0.16, w * 0.17, (0.7, 0.08, 0.12))
    c.restore()


def cloud(k, cx, cy, s, face, seed=62, puff=1.0, cheeks=False):
    s1.cloud(k, cx, cy, s, face=face, seed=seed, puff=puff)
    if cheeks:
        for sx in (-0.32, 0.32):
            ellipse(k, cx + sx * s, cy + 0.14 * s, 0.09 * s, 0.06 * s, (1, 0.75, 0.75), seed + 20, shadow=False, outline=False)


def big_button(k, x, y, w, h, pressed):
    col = (0.17, 0.42, 0.75) if pressed else (0.25, 0.55, 0.9)
    rect(k, x, y + (3 if pressed else 0), w, h, col, 140)
    text(k, "BACK UP ALL", x + w / 2, y + h / 2 + (3 if pressed else 0), 22, (1, 1, 1))


def fly(k, t, t0, dur, a, b, w, seed, arc=90):
    u = (t - t0) / dur
    if 0 <= u <= 1:
        e = ease(u)
        x, y = lerp(a[0], b[0], e), lerp(a[1], b[1], e) - math.sin(e * math.pi) * arc
        sc = lerp(1, 0.45, e)
        file_sheet(k, x, y, w * sc, w * 1.25 * sc, "", seed, rot=e * 2.5)


def sky(k):
    rect(k, -20, -20, W + 40, H + 40, s1.SKY, 80, shadow=False, outline=False)


def frame_edges(k):
    rect(k, -20, 120, 44, 760, (0.96, 0.95, 0.92), 81)
    rect(k, -20, 860, W + 40, 140, (0.96, 0.95, 0.92), 82)


# ---------------------------------------------------------------- shots
def sh1_backup(k, t, tl):
    STATE["t"] = t
    kit.office_bg(k)
    pt42.wall_sign(k, 40, 250, 34)
    s1.window(k, 330, 210, 170, 190, 70)
    cloud(k, 415, 300, 52, "sleepy", seed=61)
    kit.desk(k, 30, 600, 330, 24)
    monitor(k, 50, 440, 280, 160, 26)
    if tl < 1.35:
        big_button(k, 105, 490, 170, 56, 0.1 < tl < 0.35)
    else:
        popup(k, 62, 498, 256, 44, "Saved to cloud", 27, check=True)
    for i in range(5):
        fly(k, t, 0.2 + i * 0.2, 0.55, (190, 500), (415, 300), 60, 150 + i, arc=110)
    who("PAM", k, 430, 980, 1.3, pose="click" if tl < 0.6 else "pleased", face="pleased" if tl > 0.6 else "neutral",
        seed=42, look=(-1, 0.3))


def sh2_swell(k, t, tl):
    STATE["t"] = t
    sky(k)
    steps = [2.15, 2.55, 2.9, 3.2]
    n = sum(ease(clamp((t - s) / 0.25)) for s in steps)
    sz = 170 + 24 * n
    face = "sleepy" if t < 2.6 else "wide"
    cloud(k, 290, 430, sz, face, puff=1 + 0.05 * n, cheeks=t >= 2.6)
    for i, t0 in enumerate((2.0, 2.4, 2.75)):
        fly(k, t, t0, 0.4, (-60, 900), (290, 440), 90, 160 + i, arc=60)
    u = (t - 3.0) / 0.35
    if u >= 0:
        e = ease(clamp(u))
        private_file(k, lerp(-60, min(440, 290 + sz * 0.72), e), lerp(900, 520, e), 104, 170, rot=lerp(1.5, 0.35, e))
    frame_edges(k)
    if t >= 3.3:
        popup(k, 50, 130, 420, 56, "Cloud storage almost full", 28, warn=True)


def sh3_sneeze(k, t, tl):
    STATE["t"] = t
    sky(k)
    sneezed = t >= 5.62
    if not sneezed:
        u = ease(clamp(tl / 1.6))
        sz = 280 + 30 * u
        cloud(k, 290, 450, sz, "squeeze", puff=1.25 + 0.1 * u)
        private_file(k, min(440, 290 + sz * 0.72), 540, 104, 170, rot=0.35)
        sfx(k, "ah... ah..." if t >= 4.85 else "ah...", 280, 150, 52, rot=-0.06, fill=(1, 1, 1))
        return
    d = t - 5.62
    cloud(k, 290, 430, 300, "sneeze", puff=1.15)
    r = random.Random(5)
    a = ease(clamp(d / 0.7))
    for i in range(30):
        ang = r.uniform(0, 2 * math.pi)
        dist = a * r.uniform(160, 650)
        file_sheet(k, 290 + math.cos(ang) * dist, 470 + math.sin(ang) * dist * 1.2, 64, 80, "", 420 + i, rot=ang * 3 + d)
    private_file(k, lerp(500, -120, a), lerp(540, 980, a), 104, 170, rot=0.35 - 3 * a)
    sfx(k, "ACHOO!", 280, 190, 104, rot=-0.12)


def sh4_shared(k, t, tl):
    STATE["t"] = t
    kit.office_bg(k)
    r = random.Random(9)
    for i in range(14):   # pages drift down either side; her face stays clear
        x = r.choice([r.uniform(20, 140), r.uniform(400, 520)])
        y = (r.uniform(-200, 900) + tl * r.uniform(120, 220)) % 1100 - 100
        file_sheet(k, x, y, 58, 72, "", 700 + i, rot=math.sin(tl * 2 + i) * 0.6)
    who("PAM", k, 270, 1090, 1.9, pose="pleased", face="pleased", seed=44)


def page(k, cx, cy, w, h, rot, variant):
    c = k.c
    c.save()
    c.translate(cx, cy)
    c.rotate(rot)
    rect(k, -w / 2, -h / 2, w, h, PAPER, 480)
    rect(k, -w / 2, -h / 2, w, 62, PRIV, 481, shadow=False)
    text(k, "PAM / PRIVATE", 0, -h / 2 + 32, 26, (0.7, 0.08, 0.12))
    if variant == "B":
        text(k, "CAN MY BOSS", 0, -14, 50, INK)
        text(k, "SEE THIS?", 0, 58, 50, INK)
    else:
        text(k, "SEARCH HISTORY", 0, -h / 2 + 100, 22, (0.45, 0.45, 0.5))
        for i, s in enumerate(("what is the cloud", "how to unshare", "how to look busy on camera")):
            text(k, s, 0, -18 + i * 54, 26, INK)
    c.restore()


def sh5_desk(k, t, tl):
    STATE["t"] = t
    if t < 11.0:
        kit.office_bg(k)
        rect(k, -20, 300, W + 40, 700, DESK_TOP, 490)             # DON's desk, from above
        rect(k, 330, 820, 190, 70, (0.18, 0.18, 0.2), 491)        # nameplate
        text(k, "CEO", 425, 846, 30, (0.95, 0.82, 0.35))
        text(k, "DON", 425, 875, 15, (1, 1, 1))
        ellipse(k, 80, 860, 42, 42, (0.95, 0.95, 0.97), 492)      # mug
        ellipse(k, 80, 860, 30, 30, (0.35, 0.22, 0.14), 493, shadow=False)
        e = ease(clamp((t - 8.6) / 0.42))
        page(k, lerp(-300, 270, e), 540, 470, 400, lerp(-0.5, -0.03, e), VARIANT)
        return
    kit.office_bg(k)   # cut to PAM: jaw drop
    who("PAM", k, 270, 1100, 2.3, pose="stand", face="shock" if t < 11.4 else "panic", seed=45)


def sh6_don(k, t, tl):
    STATE["t"] = t
    pt4.accent_wall(k, "DON")
    up = ease(clamp((t - 12.15) / 0.45))
    p = who("DON", k, 190, 1230, 2.3, pose="point_r", face="neutral", seed=63, look=(0.0, lerp(1, 0, up)))
    hx, hy = p["hands"][1]
    c = k.c
    c.save()
    c.translate(min(hx, 430), hy - 40 + lerp(40, 0, up))
    c.scale(0.42, 0.42)
    page(k, 0, 0, 470, 400, 0.05, VARIANT)
    c.restore()


PANELS = [(0.0, 2.0, sh1_backup), (2.0, 4.0, sh2_swell), (4.0, 6.5, sh3_sneeze),
          (6.5, 8.5, sh4_shared), (8.5, 12.0, sh5_desk), (12.0, 15.0, sh6_don)]

LINES = [(0.3, 1.7, "All backed up!", 430, 600),
         (6.95, 8.45, "Nice. Shared.", 270, 520),
         (12.85, 14.6, "Nice. Shared.", 190, 470)]


def shake(t):
    d = t - 5.62
    return math.sin(d * 55) * 10 * (1 - d / 0.35) if 0 <= d < 0.35 else 0


def overlay(k, t, tl, name):
    for (s, e, txt, ax, ay) in LINES:
        if s <= t < e:
            bubble(k, txt, ax, ay, pop=0.85 + 0.15 * ease(clamp((t - s) / 0.12)))
