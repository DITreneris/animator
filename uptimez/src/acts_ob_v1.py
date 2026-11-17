"""v1, pinned. THE ONBOARDING: the acting of Don, Pam and the Client (v1), from script v1 and the grill of 17 Nov. No new costumes:
Don is his office self (don_v4: fleece vest, lanyard, the ketchup stain), Pam is as in The Best Candidate (pam_bc), the
Client is sheet v3 (client_ob). Nothing in those modules is changed: this file only poses them and adds the props.
DON: small and tight. "hand_out" (an open hand for the roll), "holds" (he has it), "set_down" (his eyes on Sofia,
  off right; his other hand stands the roll in what is beside him, without looking), "away" (caught staring: he looks
  away and a hand goes to his vest), "jealous" (two short brows; he keeps selling), "hand_up" (beat 08).
PAM: no lines. "typing" (before anyone has moved), "finger" (she lifts a finger to interrupt), "lower" (she looks at
  Don, and lowers it), "empty" (Sofia has taken the tablet), "kneel" (on her knees, a fist full of blue strips).
THE CLIENT: "give" (he hands the roll over; he does not leave it lying), "watch" (his silent signature),
  "palm" (the strip settles in it), and his existing "stand" for pocketing it.
The shredder stands on the floor beside Don, a slot in its top and a clear bin: it looks like somewhere you might
stand a roll. That is the accident."""
import math
import kit
import don_v4 as dv
import pam_bc as pb
import client_ob as co
import sofia_ob as so
from kit import INK, cut, rect, ellipse

BLUE = (0.16, 0.38, 0.80)
STRIP = (0.20, 0.42, 0.84)
LN = 48


def _ik(sx, sy, side, tx, ty):
    dx, dy = tx - sx, ty - sy
    d = min(math.hypot(dx, dy), 2 * LN - 0.2)
    base, a = math.degrees(math.atan2(dx, dy)), math.degrees(math.acos(d / (2 * LN)))
    return (base + side * a, -side * 2 * a)


def _pose(h, left=None, right=None):
    """Arm angles for a kit person of height factor h; left/right are hand targets in the person's own coordinates."""
    sy = -300 * h + 78 + 14
    L = _ik(-40, sy, -1, *left) if left else (-8, 0)
    R = _ik(40, sy, 1, *right) if right else (8, 0)
    return tuple(L) + tuple(R)


def strips(k, x, y, s, n=7, seed=3, fan=1.0):
    r = k.rng(seed) if hasattr(k, "rng") else None
    c = k.c
    for i in range(n):
        a = (-0.9 + 1.8 * i / max(1, n - 1)) * fan + (0.12 if i % 2 else -0.10)
        c.save(); c.translate(x, y); c.rotate(a)
        rect(k, -3.2 * s, -34 * s, 6.4 * s, 34 * s, STRIP, seed + i, shadow=False, lw=1.2 * s)
        c.set_source_rgb(1, 1, 1); c.set_line_width(1.0 * s); c.move_to(0, -30 * s); c.line_to(0, -8 * s); c.stroke()
        c.restore()


def shredder(k, x, floor, s=1.0, fill=0.0, seed=20):
    """A floor shredder: a slot in the top, a clear bin below. fill 0..1: blue strips in the bin."""
    c = k.c
    c.save(); c.translate(x, floor); c.scale(s, s)
    rect(k, -34, -112, 68, 112, (0.34, 0.36, 0.42), seed, lw=2.2)
    rect(k, -30, -64, 60, 58, (0.86, 0.92, 0.96), seed + 1, shadow=False, lw=1.6)          # the clear bin
    if fill > 0:
        c.save(); c.rectangle(-29, -63, 58, 56); c.clip()
        hgt = 50 * fill
        for i in range(int(26 * fill) + 3):
            xx = -27 + (i * 37 % 54); yy = -8 - (i * 23 % max(6, int(hgt)))
            c.save(); c.translate(xx, yy); c.rotate((i * 0.9) % 3.1)
            c.set_source_rgb(*STRIP); c.rectangle(-9, -1.8, 18, 3.6); c.fill()
            c.set_source_rgb(1, 1, 1); c.rectangle(-6, -0.4, 12, 0.8); c.fill()
            c.restore()
        c.restore()
    rect(k, -24, -108, 48, 9, (0.12, 0.12, 0.15), seed + 2, shadow=False, lw=1.4)          # the slot
    ellipse(k, 22, -84, 3.2, 3.2, (0.30, 0.74, 0.46), seed + 3, shadow=False, lw=1.0)
    c.restore()


def roll(k, x, y, s, ang, ln=150, seed=71):
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    co.blueprint_roll(k, 0, 0, ang, ln, 11.5, seed)
    c.restore()


def don(k, x, feet, s=1.0, act="stand", look=None, seed=500):
    H = kit.PEOPLE["DON"]["h"]
    sy = -300 * H + 92
    acts = {
        "stand": ((-8, 0, 8, 0), "neutral", (-1, 0)),
        "hand_out": (_pose(H, left=(-116, sy + 34)), "grin", (-1, -0.2)),
        "holds": (_pose(H, left=(-76, sy + 62)), "grin", (-1, -0.2)),
        "set_down": (_pose(H, left=(-66, sy + 86)), "neutral", (1, -0.1)),
        "away": (dv.POSE_CHEST, "neutral", (-1, -0.5)),
        "jealous": ((-8, 0, 8, 0), "neutral", (1, 0.0)),
        "hand_up": ((-10, 0, 168, 0), "grin", (1, 0.0)),
    }
    pose, face, lk = acts[act]
    kit.ARM_POSES["_ob"] = pose
    try:
        o = dv.don(k, x, feet, s, "_ob", face, look=look or lk, seed=seed, chin=1 if act == "away" else 0)
    finally:
        del kit.ARM_POSES["_ob"]
    c = k.c
    hx, hy = o["hands"][0]
    if act == "hand_out":                                  # an open hand, palm up
        cut(k, [(hx - 20 * s, hy - 7 * s), (hx + 6 * s, hy - 9 * s), (hx + 8 * s, hy + 7 * s), (hx - 22 * s, hy + 5 * s)],
            kit.PEOPLE["DON"]["skin"], shadow=False, lw=2 * s)
        c.set_source_rgb(*INK); c.set_line_width(1.4 * s)
        for dx in (-14, -8, -2):
            c.move_to(hx + dx * s, hy - 7 * s); c.line_to(hx + (dx - 1) * s, hy + 3 * s); c.stroke()
    elif act in ("holds", "set_down"):
        if act == "set_down":                              # the lower end is already in the slot
            roll(k, hx, hy + 6 * s, s, 0.0, ln=96)
        else:
            roll(k, hx, hy - 6 * s, s, -0.25, ln=140)
        ellipse(k, hx, hy, 10.2 * s, 10.2 * s, kit.PEOPLE["DON"]["skin"], seed + 70, shadow=False, lw=2 * s)
    if act == "jealous":                                   # small and tight: two short brows
        ex, ey = o["head"]
        c.set_source_rgb(*INK); c.set_line_width(4.2 * s); c.set_line_cap(1)
        c.move_to(ex - 40 * s, ey - 27 * s); c.line_to(ex - 14 * s, ey - 20 * s); c.stroke()
        c.move_to(ex + 40 * s, ey - 27 * s); c.line_to(ex + 14 * s, ey - 20 * s); c.stroke()
    return o


def pam(k, x, feet, s=1.0, act="stand", look=None, floor=None, seed=40):
    H = kit.PEOPLE["PAM"]["h"]
    sy = -300 * H + 92
    hold = (-20, sy + 62)
    acts = {
        "stand": ((-8, 0, 8, 0), (-0.6, 0.0)),
        "typing": (_pose(H, left=hold, right=(14, sy + 50)), (-0.2, 0.9)),
        "finger": (_pose(H, left=hold, right=(90, sy - 26)), (-0.9, 0.6)),
        "lower": (_pose(H, left=hold, right=(60, sy + 22)), (-0.8, -0.1)),
        "empty": (_pose(H, left=(-22, sy + 60), right=(22, sy + 60)), (-0.2, 0.9)),
        "kneel": (_pose(H, left=(-74, sy + 70), right=(26, sy + 40)), (-0.7, 0.9)),
    }
    pose, lk = acts[act]
    c = k.c
    drop = 106 * s if act == "kneel" else 0
    if act == "kneel":
        c.save(); c.rectangle(x - 400 * s, feet - 700 * s, 800 * s, 700 * s); c.clip()
    try:
        o = pb.pam(k, x, feet + drop, s, pose, "neutral", look=look or lk, seed=seed, lean=-7.0 if act == "kneel" else 0.0)
    except Exception:
        kit.ARM_POSES["_ob"] = pose
        try:
            o = pb.pam(k, x, feet + drop, s, "_ob", "neutral", look=look or lk, seed=seed, lean=-7.0 if act == "kneel" else 0.0)
        finally:
            del kit.ARM_POSES["_ob"]
    if act == "kneel":
        c.restore()
    skin = kit.PEOPLE["PAM"]["skin"]
    (lx, ly), (rx, ry) = o["hands"]
    if act in ("typing", "finger", "lower"):               # her tablet, the form on it
        so.tablet(k, lx + 22 * s, ly - 12 * s, -0.08, "form", seed + 80) if s == 1.0 else _scaled(k, lx + 22 * s, ly - 12 * s, s, seed)
        ellipse(k, lx, ly, 10 * s, 10 * s, skin, seed + 81, shadow=False, lw=2 * s)
        if act == "typing":
            ellipse(k, rx, ry, 10 * s, 10 * s, skin, seed + 82, shadow=False, lw=2 * s)
    if act == "finger":                                    # one finger, up
        for col, w in ((INK, 8.4), (skin, 5.6)):
            c.set_source_rgb(*col); c.set_line_width(w * s); c.set_line_cap(1)
            c.move_to(rx, ry - 4 * s); c.line_to(rx + 2 * s, ry - 27 * s); c.stroke()
        ellipse(k, rx, ry, 10 * s, 10 * s, skin, seed + 83, shadow=False, lw=2 * s)
    if act == "kneel":                                     # a fist full of strips, and one more being picked up
        strips(k, rx, ry - 4 * s, s, n=7, seed=seed + 60, fan=0.55)
        ellipse(k, rx, ry, 10.5 * s, 10.5 * s, skin, seed + 84, shadow=False, lw=2 * s)
    return o


def _scaled(k, x, y, s, seed):
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    so.tablet(k, 0, 0, -0.08, "form", seed + 80)
    c.restore()


def client(k, x, feet, s=1.0, act="give", look=None, seed=900):
    hang = co.POSES["open"][:2]
    acts = {
        "give": (hang + co._ik(1, 166, co.BT + 92), "confident", (0.8, 0.0)),
        "watch": (hang + co._ik(1, 52, co.BT + 74), "confident", (0.5, 1.0)),
        "palm": (hang + co._ik(1, 112, co.BT + 112), "puzzled", (0.7, 1.0)),
    }
    pose, face, lk = acts[act]
    o = co.client(k, x, feet, s, pose, face, look=look or lk, seed=seed)
    c = k.c
    hx, hy = o["hands"][1]
    if act == "give":                                      # the roll, held out
        roll(k, hx + 22 * s, hy - 2 * s, s, math.pi / 2 - 0.12, ln=150)
        ellipse(k, hx, hy, co.HAND * s, co.HAND * s, co.SKIN, seed + 71, shadow=False, lw=2 * s)
    elif act == "palm":                                    # one strip, settling
        c.save(); c.translate(hx + 2 * s, hy - 30 * s); c.rotate(0.5)
        rect(k, -5 * s, -24 * s, 10 * s, 48 * s, STRIP, seed + 72, lw=1.6 * s)
        c.set_source_rgb(1, 1, 1); c.set_line_width(1.6 * s); c.move_to(0, -18 * s); c.line_to(0, 6 * s); c.stroke()
        c.arc(0, 12 * s, 4 * s, 0, math.pi); c.stroke()
        c.restore()
    return o
