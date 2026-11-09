"""Saved to Cloud S1v3.2 - version B extended to 21.5 s, with the animation pass.
9 shots: DON asks -> PAM backs up -> cloud gulps -> cloud holds it in (laugh 1) -> ACHOO ->
"Nice. Shared." (laugh 2) -> CAN MY BOSS SEE THIS? -> DON: "Nice. Shared." (laugh 3) -> sniff tag.
New module only: reuses s131 props; kit, pt4, pt42, s1, s131 unchanged (face drawing wrapped at runtime).
Render with engine_v.py (length from DURATION)."""
import json
import math
import os
import random
import kit
import pt4
import pt42
import s1
import s131
import anim
from kit import W, H, INK, rect, ellipse, text, file_sheet, monitor, popup, sfx, bubble, ease, clamp, lerp

DURATION = 21.5
RAW_T = 0.0                       # set by engine_v each frame (unquantised time, for camera moves)
_HERE = os.path.dirname(os.path.abspath(__file__))
SYNC = json.load(open(os.path.join(_HERE, "s132_sync.json")))
ENV = SYNC["env"]
NF = len(ENV["PAM"])
STATE = {"t": 0.0, "who": None, "skin": (1, 1, 1), "seed": 0, "brow": 0.0}
ARC_FACES = ("happy", "pleased", "smug", "squint", "hollow")
person = pt42.branded_person
private_file, page, cloud, big_button, sky = s131.private_file, s131.page, s131.cloud, s131.big_button, s131.sky
WIN = (0.96, 0.95, 0.92)

# ---------------------------------------------------------------- faces: lip-sync, blinks, DON's eyebrow
_orig_face = kit.face_draw


def face_live(k, x, y, face, look, glasses=False, seed=0):
    _orig_face(k, x, y, face, look, glasses=glasses, seed=seed)
    who, f, c = STATE["who"], int(STATE["t"] * 30), k.c
    if who is None:
        return
    if face not in ARC_FACES and ((f + STATE["seed"] * 13) % 84) < 3:          # blink
        for sx in (-17, 17):
            ellipse(k, x + sx, y, 15, 15, STATE["skin"], 9000 + sx, shadow=False, outline=False)
            c.set_source_rgb(*INK); c.set_line_width(4)
            c.move_to(x + sx - 11, y + 2); c.line_to(x + sx + 11, y + 2); c.stroke()
    if who in ENV and 0 <= f < NF and ENV[who][f] > 0.12:                      # lip-sync
        o = ENV[who][f]
        ellipse(k, x, y + 28, 19, 12, STATE["skin"], 9100, shadow=False, outline=False)
        ellipse(k, x, y + 30, 13 + 5 * o, 3 + 14 * o, (0.35, 0.08, 0.08), 9101, shadow=False, lw=2)
    if who == "DON" and STATE["brow"] > 0:                                     # one eyebrow up
        b = STATE["brow"]
        c.set_source_rgb(*INK); c.set_line_width(5)
        c.move_to(x + 4, y - 24 - 8 * b); c.curve_to(x + 12, y - 34 - 10 * b, x + 24, y - 34 - 10 * b, x + 32, y - 26 - 8 * b)
        c.stroke()


kit.face_draw = face_live


def who(name, k, x, feet, s, pose="stand", face="neutral", seed=1, look=(0, 0), breathe=True):
    STATE.update(who=name, skin=kit.PEOPLE[name]["skin"], seed=seed)
    b = math.sin(2 * math.pi * STATE["t"] / 2.4 + seed) * 2.2 * s if breathe else 0
    out = person(k, name, x, feet + b, s, pose, face, seed, look)
    STATE["who"] = None
    return out


def fly(k, t, t0, dur, a, b, w, seed, arc=90, end_scale=0.45):
    u = (t - t0) / dur
    if 0 <= u <= 1:
        e = ease(u)
        x, y = lerp(a[0], b[0], e), lerp(a[1], b[1], e) - math.sin(e * math.pi) * arc
        sc = lerp(1, end_scale, e)
        file_sheet(k, x, y, w * sc, w * 1.25 * sc, "", seed, rot=e * 2.5 + math.sin(t * 9 + seed) * 0.2)


def squashed(k, cx, base, sx, sy, fn):
    c = k.c
    c.save()
    anim.squash(c, cx, base, sx, sy)
    fn()
    c.restore()


def whip(k, tl, dur=0.14):
    """Whip-pan streaks over the first frames of a shot; returns the x offset for the scene."""
    u = clamp(tl / dur)
    if u >= 1:
        return 0.0
    c = k.c
    c.set_source_rgba(1, 1, 1, 0.55 * (1 - u))
    r = random.Random(int(tl * 100))
    for _ in range(14):
        y = r.uniform(0, H)
        c.rectangle(-20, y, W + 40, r.uniform(3, 12))
        c.fill()
    return (1 - ease(u)) * 260


def office_window(k, x=330, y=280, w=170, h=190):
    s1.window(k, x, y, w, h, 70)


# ---------------------------------------------------------------- 1: DON walks in, asks
def sh1_don_asks(k, t, tl):
    STATE["t"] = t
    kit.office_bg(k)
    pt42.wall_sign(k, 40, 250, 34)
    office_window(k)
    cloud(k, 415, 375, 50, "sleepy", seed=61)
    walking = t < 1.1
    x = lerp(40, 150, ease(clamp(t / 1.1)))
    if walking:
        pose, bob = anim.walk(t)
    else:
        pose, bob = anim.keyed(t, [(0, "stand"), (1.1, (-8, 0, 40, -60))], dur=0.2), 0
    who("PAM", k, 400, 980, 1.25, pose="stand", face="neutral", seed=42, look=(-1, 0))
    who("DON", k, x, 1000 + bob, 1.35, pose=pose, face="neutral", seed=63, look=(1, 0), breathe=not walking)


# ---------------------------------------------------------------- 2: PAM slams BACK UP ALL
def sh2_backup(k, t, tl):
    STATE["t"] = t
    kit.office_bg(k)
    office_window(k)
    sz = 50 + 4 * sum(ease(clamp((t - h) / 0.2)) for h in (3.0, 3.2, 3.4, 3.6))
    gx, gy = anim.gulp(t, (3.0, 3.2, 3.4, 3.6), amt=0.18)
    squashed(k, 415, 410, gx, gy, lambda: cloud(k, 415, 375, sz, "sleepy", seed=61))
    kit.desk(k, 20, 620, 330, 24)
    monitor(k, 40, 455, 280, 165, 26)
    if t < 3.85:
        big_button(k, 95, 510, 170, 56, 2.58 < t < 2.8)
    else:
        popup(k, 52, 518, 256, 44, "Saved to cloud", 27, check=True)
    for i in range(5):
        fly(k, t, 2.65 + i * 0.17, 0.5, (180, 520), (415, 380), 60, 150 + i, arc=120)
    pose = anim.keyed(t, [(2.5, "stand"), (2.5, (-150, -30, 8, 0)), (2.58, (-60, 45, 8, 0)), (3.0, "pleased")], dur=0.08)
    who("PAM", k, 430, 1000, 1.35, pose=pose, face="pleased" if t > 3.0 else "neutral", seed=42,
        look=(-1, 0.3))
    if t < 3.2:   # DON leaving at the left edge
        who("DON", k, lerp(60, -160, ease(clamp((t - 2.5) / 0.7))), 1000, 1.35, pose=anim.walk(t)[0],
            face="neutral", seed=63, breathe=False)


# ---------------------------------------------------------------- 3: the cloud gulps each file
HITS3 = (4.75, 5.15, 5.55, 5.95)


def sh3_gulp(k, t, tl):
    STATE["t"] = t
    c = k.c
    c.save()
    c.translate(whip(k, RAW_T - 4.5), 0)
    sky(k)
    n = sum(ease(clamp((t - h) / 0.2)) for h in HITS3)
    sz = 160 + 26 * n
    gx, gy = anim.gulp(t, HITS3, amt=0.16)
    face = "sleepy" if t < 5.2 else "wide"
    squashed(k, 290, 430 + sz * 0.45, gx, gy, lambda: cloud(k, 290, 430, sz, face, puff=1 + 0.05 * n, cheeks=t >= 5.2))
    for i, t0 in enumerate(HITS3[:3]):
        fly(k, t, t0 - 0.3, 0.3, (-60, 900), (290, 450), 90, 160 + i, arc=40)
    u = (t - 5.6) / 0.35
    if u >= 0:
        e = ease(clamp(u))
        private_file(k, lerp(-60, min(440, 290 + sz * 0.72), e), lerp(900, 520, e), 104, 170, rot=lerp(1.5, 0.35, e))
    s131.frame_edges(k)
    c.restore()
    if t >= 6.05:
        popup(k, 50, 130, 420, 56, "Cloud storage almost full", 28, warn=True)


# ---------------------------------------------------------------- 4: holding it in; PAM shoves it back
def sh4_hold(k, t, tl):
    STATE["t"] = t
    kit.office_bg(k)
    rect(k, 230, 110, 300, 430, WIN, 71)                       # big window, right
    rect(k, 244, 124, 272, 402, s1.SKY, 72, shadow=False)
    wob = math.sin(t * 22) * 0.05 * clamp((t - 6.5) / 0.3) * (1 - clamp((t - 7.4) / 0.2))
    hits = (8.6, 9.25)
    gx, gy = anim.gulp(t, hits, amt=0.2)
    sz = 190 + 25 * ease(clamp((t - 9.25) / 0.2))
    squashed(k, 380, 470, gx + wob, gy - wob,
             lambda: cloud(k, 380, 330, sz, "squeeze" if 6.6 < t < 7.4 else "wide", puff=1.3, cheeks=True))
    private_file(k, 470, 400, 80, 170, rot=0.35)
    if 7.4 <= t < 7.75:
        sfx(k, "hic!", 330, 170, 46, rot=0.1, fill=(1, 1, 1))
    # the hiccuped file: out to PAM's hand, then shoved back in
    if 7.4 <= t < 7.9:
        u = ease((t - 7.4) / 0.5)
        file_sheet(k, lerp(330, 250, u), lerp(360, 600, u) - math.sin(u * math.pi) * 120, 66, 82, "", 777, rot=u * 4)
    # desk edge + laptop in the foreground
    pose = anim.keyed(t, [(6.5, "stand"), (7.85, "reach_r"), (8.25, (-8, 0, 70, -10)), (8.6, "pleased"),
                          (8.85, (-8, 0, 150, 20)), (9.0, (-8, 0, 60, -50)), (9.3, "pleased")], dur=0.12)
    p = who("PAM", k, 160, 1010, 1.4, pose=pose,
            face="shock" if 7.4 <= t < 7.9 else ("smug" if t >= 8.6 else "neutral"), seed=42, look=(1, -0.5))
    if 7.9 <= t < 8.6:
        hx, hy = p["hands"][1]
        file_sheet(k, hx + 10, hy - 30, 66, 82, "", 777, rot=0.3)
    rect(k, -20, 830, W + 40, 150, kit.DESK, 495)
    rect(k, 300, 760, 200, 80, (0.2, 0.2, 0.23), 496)
    big_button(k, 320, 770, 160, 50, 8.98 < t < 9.15)
    if t >= 9.05:
        fly(k, t, 9.05, 0.2, (400, 760), (380, 380), 50, 778, arc=40)


# ---------------------------------------------------------------- 5: ah... ah... ACHOO (crash zoom)
def sh5_achoo(k, t, tl):
    STATE["t"] = t
    c = k.c
    sky(k)
    if t < 11.08:
        u = ease(clamp(tl / 1.5))
        squashed(k, 290, 720, 1 - 0.08 * u, 1 + 0.15 * u,
                 lambda: cloud(k, 290, 450, 280, "squeeze", puff=1.25))
        private_file(k, 440, 560, 104, 170, rot=0.35)
        sfx(k, "ah... ah..." if t >= 10.4 else "ah...", 280, 150, 52, rot=-0.06, fill=(1, 1, 1))
        return
    d = RAW_T - 11.08
    z = 1 + 0.25 * (1 - ease(clamp(d / 0.25)))
    c.save()
    anim.camera(c, 290, 430, z)
    sx, sy = (1.12, 0.9) if d < 0.15 else (1.0, 1.0)
    squashed(k, 290, 700, sx, sy, lambda: cloud(k, 290, 430, 300, "sneeze", puff=1.15))
    r = random.Random(5)
    a = ease(clamp(d / 0.45))
    for i in range(30):
        ang = r.uniform(0, 2 * math.pi)
        dist = 120 + a * r.uniform(160, 650)
        file_sheet(k, 290 + math.cos(ang) * dist, 470 + math.sin(ang) * dist * 1.2, 64, 80, "", 420 + i,
                   rot=ang * 3 + d * r.uniform(-4, 4))
    private_file(k, lerp(500, -120, a), lerp(540, 980, a), 104, 170, rot=0.35 - 3 * a)
    c.restore()
    sfx(k, "ACHOO!", 280, 190, 104 * z, rot=-0.12)


# ---------------------------------------------------------------- 6: Nice. Shared. (paper rain)
def sh6_shared(k, t, tl):
    STATE["t"] = t
    kit.office_bg(k)
    r = random.Random(9)
    for i in range(16):
        x0 = r.choice([r.uniform(20, 130), r.uniform(410, 520)])
        x, y, rot = anim.flutter(x0, r.uniform(-300, 400), tl, i, fall=r.uniform(120, 200), sway=30)
        file_sheet(k, x, y, 58, 72, "", 700 + i, rot=rot)
    pose = anim.keyed(t, [(12, "stand"), (12.15, "pleased")], dur=0.15)
    who("PAM", k, 270, 1090, 1.9, pose=pose, face="pleased", seed=44)


# ---------------------------------------------------------------- 7: the page on DON's desk; PAM drops
def sh7_page(k, t, tl):
    STATE["t"] = t
    if t < 16.0:
        kit.office_bg(k)
        rect(k, -20, 300, W + 40, 700, s131.DESK_TOP, 490)
        for hx in (90, 450):                                    # DON's sleeves and hands at the desk edge
            rect(k, hx - 45, 900, 90, 90, kit.PEOPLE["DON"]["body"], 497 + hx)
            ellipse(k, hx, 900, 30, 24, kit.PEOPLE["DON"]["skin"], 499 + hx)
        rect(k, 300, 770, 220, 84, (0.18, 0.18, 0.2), 491)
        text(k, "CEO", 410, 800, 38, (0.95, 0.82, 0.35))
        text(k, "DON", 410, 836, 17, (1, 1, 1))
        e = ease(clamp((t - 14.1) / 0.42))
        page(k, lerp(-300, 270, e), 520, 470, 400, lerp(-0.5, -0.03, e), "B")
        return
    kit.office_bg(k)
    slump = ease(clamp((t - 16.45) / 0.3))
    pose = anim.keyed(t, [(16, "stand"), (16.45, (-20, 0, 20, 0))], dur=0.25)
    who("PAM", k, 270, 1100 + 40 * slump, 2.3, pose=pose, face="shock" if t < 16.45 else "panic", seed=45)


# ---------------------------------------------------------------- 8: DON looks up: "Nice. Shared."
def sh8_don(k, t, tl):
    STATE["t"] = t
    c = k.c
    z = 1 + 0.06 * ease(clamp((RAW_T - 17.0) / 3.5))
    c.save()
    anim.camera(c, 230, 560, z)
    pt4.accent_wall(k, "DON")
    pt42.portrait_frame(k, 330, 150, 140, 130)
    up = ease(clamp((t - 17.2) / 0.6))
    STATE["brow"] = ease(clamp((t - 19.6) / 0.15))
    pose = anim.keyed(t, [(17.0, "stand"), (17.4, "point_r")], dur=0.4, overshoot=False)
    p = who("DON", k, 190, 1230, 2.3, pose=pose, face="neutral", seed=63, look=(0.0, lerp(1, 0, up)))
    STATE["brow"] = 0.0
    hx, hy = p["hands"][1]
    c.save()
    c.translate(min(hx, 430), hy - 40)
    c.scale(0.42, 0.42)
    page(k, 0, 0, 470, 400, 0.05, "B")
    c.restore()
    c.restore()


# ---------------------------------------------------------------- 9: tag: the cloud sniffs
def sh9_sniff(k, t, tl):
    STATE["t"] = t
    kit.office_bg(k)
    office_window(k, 120, 260, 300, 300)
    gx, gy = anim.gulp(t, (20.7, 20.88), amt=0.12, dur=0.18)
    squashed(k, 270, 470, gx, gy, lambda: cloud(k, 270, 400, 90, "squeeze" if t > 20.65 else "sleepy", seed=61))
    if t > 20.65:
        sfx(k, "sniff", 270, 220, 40, rot=-0.08, fill=(1, 1, 1))


PANELS = [(0.0, 2.5, sh1_don_asks), (2.5, 4.5, sh2_backup), (4.5, 6.5, sh3_gulp), (6.5, 9.5, sh4_hold),
          (9.5, 12.0, sh5_achoo), (12.0, 14.0, sh6_shared), (14.0, 17.0, sh7_page), (17.0, 20.5, sh8_don),
          (20.5, 21.5, sh9_sniff)]

LINES = [(1.2, 2.45, "Everything backed up?", 150, 600),
         (2.75, 4.0, "All backed up!", 430, 620),
         (12.3, 13.8, "Nice. Shared.", 270, 520),
         (18.5, 20.2, "Nice. Shared.", 190, 470)]


def shake(t):
    d = t - 11.08
    return math.sin(d * 55) * 10 * (1 - d / 0.35) if 0 <= d < 0.35 else 0


def overlay(k, t, tl, name):
    for (s, e, txt, ax, ay) in LINES:
        if s <= t < e:
            bubble(k, txt, ax, ay, pop=0.85 + 0.15 * ease(clamp((t - s) / 0.12)))
