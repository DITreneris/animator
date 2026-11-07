"""Prompt Telephone v04.3 - v04.2 plus: a rebuilt opening (big DON, words fly out of his mouth in sync,
frame-0 punch-in, fist slam on a foreground desk), lip-sync from the voice, blinks and breathing.
New module only: kit.py, pt4.py, pt42.py and every earlier version are untouched (wrapped at runtime)."""
import json
import math
import random
import kit
import pt4
import pt42
from kit import W, H, INK, rect, ellipse, sfx, ease, clamp, lerp, file_sheet

import os as _os
SYNC = json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "pt43_sync.json")))
ENV = SYNC["env"]
CUES = SYNC["cues"]
SLAM = SYNC["slam"]
STATE = {"t": 0.0, "who": None, "skin": (1, 1, 1), "seed": 0}

# ---------------------------------------------------------------- runtime wrappers: lip-sync, blinks, breathing
_orig_face = kit.face_draw
ARC_FACES = ("happy", "pleased", "smug", "squint", "hollow")


def face_draw_live(k, x, y, face, look, glasses=False, seed=0):
    _orig_face(k, x, y, face, look, glasses=glasses, seed=seed)
    f = int(STATE["t"] * 30)
    who = STATE["who"]
    c = k.c
    # blink: 3 frames every ~2.5-3.5 s, offset per character
    if face not in ARC_FACES and ((f + STATE["seed"] * 13) % 84) < 3:
        for sx in (-17, 17):
            ellipse(k, x + sx, y, 15, 15, STATE["skin"], 9000 + sx, shadow=False, outline=False)
            c.set_source_rgb(*INK); c.set_line_width(4)
            c.move_to(x + sx - 11, y + 2); c.line_to(x + sx + 11, y + 2); c.stroke()
    # lip-sync: the mouth opens with this speaker's voice level
    if who in ENV and 0 <= f < 450:
        o = ENV[who][f]
        if o > 0.12:
            my = y + 28
            ellipse(k, x, my, 19, 12, STATE["skin"], 9100, shadow=False, outline=False)  # hide the drawn mouth
            ellipse(k, x, my + 2, 13 + 5 * o, 3 + 14 * o, (0.35, 0.08, 0.08), 9101, shadow=False, lw=2)


kit.face_draw = face_draw_live

_branded = pt42.branded_person


def person_live(k, name, x, feet, s=1.0, pose="stand", face="neutral", seed=1, look=(0, 0), seated=False, badge=True):
    STATE["who"] = name if name in ENV else None
    STATE["skin"] = kit.PEOPLE[name]["skin"]
    STATE["seed"] = seed
    breathe = math.sin(2 * math.pi * STATE["t"] / 2.4 + seed) * 2.2 * s
    out = _branded(k, name, x, feet + breathe, s, pose, face, seed, look, seated, badge)
    STATE["who"] = None
    return out


pt4.person = person_live
pt42.branded_person = person_live


def live(fn):
    def g(k, t, tl):
        STATE["t"] = t
        fn(k, t, tl)
    g.__name__ = fn.__name__
    return g


# ---------------------------------------------------------------- the new opening
WORDS = [("BOLD!", 150), ("AUTHENTIC!", 240), ("VIRAL!", 330)]
DON_X, HEAD_Y, S = 190, 560, 3.0
MOUTH = (DON_X, HEAD_Y + 96)
SUIT = kit.PEOPLE["DON"]["body"]
SKIN = kit.PEOPLE["DON"]["skin"]


def s1_open(k, t, tl):
    STATE["t"] = t
    c = k.c
    # punch-in: frame 0 starts close on DON's open mouth and pulls back over 0.35 s
    z = lerp(1.7, 1.0, ease(clamp(tl / 0.35)))
    c.save()
    c.translate(MOUTH[0], MOUTH[1])
    c.scale(z, z)
    c.translate(-MOUTH[0], -MOUTH[1])
    pt4.accent_wall(k, "DON")
    pt42.wall_sign(k, 296, 412, 32)
    slamming = t >= SLAM - 0.2
    person_live(k, "DON", DON_X, HEAD_Y + 302 * S, S, pose="stand" if slamming else "point_r",
                face="panic", seed=63, look=(0.4, -0.2))
    # foreground desk with papers
    rect(k, -30, 862, W + 60, 130, (0.45, 0.30, 0.19), 1200)
    hit = clamp((t - SLAM) / 0.35)
    r = random.Random(4)
    for i in range(5):
        px, rot = 90 + i * 85, r.uniform(-0.3, 0.3)
        lift = math.sin(hit * math.pi) * r.uniform(80, 160) if t >= SLAM else 0
        file_sheet(k, px + hit * r.uniform(-40, 40), 868 - lift, 70, 46, "", 1210 + i, rot=rot + hit * r.uniform(-2, 2))
    # the fist: winds up, then comes down on the desk at SLAM
    if slamming:
        u = ease(clamp((t - (SLAM - 0.2)) / 0.2))
        fx, fy = lerp(470, 420, u), lerp(560, 850, u)
        sx, sy = DON_X + 40 * S, HEAD_Y + 302 * S - 732
        c.set_line_cap(1); c.set_line_width(70); c.set_source_rgb(*SUIT)
        c.move_to(sx, sy); c.line_to(fx, fy - 40); c.stroke()
        ellipse(k, fx, fy, 48, 42, SKIN, 1220)
        c.set_source_rgb(*INK); c.set_line_width(3)
        for kx in (-18, 0, 18):
            c.move_to(fx + kx, fy - 20); c.line_to(fx + kx, fy - 2); c.stroke()
    c.restore()
    # words fly out of his mouth, each on its stressed syllable (screen space, after the punch-in)
    for word, y in WORDS:
        cue = CUES[word]
        if t >= cue - 0.01:
            u = ease(clamp((t - cue) / 0.22))
            x0, y0 = MOUTH
            x, yy = lerp(x0 + 40, 290, u), lerp(y0 - 20, y, u)
            c.save()
            c.translate(x, yy)
            sc = lerp(0.35, 1.0, u)
            c.scale(sc, sc)
            pt4.big_tile(k, word, 0, 0, 1300 + y)
            c.restore()
            if u < 1:  # speed lines
                c.set_source_rgba(*INK, 0.6); c.set_line_width(3)
                for d in (-14, 0, 14):
                    c.move_to(x - 60, yy + d + 30); c.line_to(x - 120, yy + d + 60); c.stroke()
    if SLAM <= t < SLAM + 0.5:
        sfx(k, "SLAM!", 400, 760, 64, rot=0.1)


PANELS = [(0.0, 2.0, s1_open), (2.0, 3.5, live(pt4.s2_pam)), (3.5, 5.0, live(pt4.s3_rush)),
          (5.0, 8.2, live(pt4.s4_laptop)), (8.2, 11.0, live(pt42.s4_post)), (11.0, 13.8, live(pt42.s5_don)),
          (13.8, 15.0, live(pt4.s6_roll))]

overlay = pt42.overlay


def shake(t):
    for t0, amp in ((SLAM, 12), (7.6, 7)):
        d = t - t0
        if 0 <= d < 0.25:
            return math.sin(d * 60) * amp * (1 - d / 0.25)
    return 0
