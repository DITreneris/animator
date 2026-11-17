"""v2, pinned.
THE ONBOARDING: the animation, v2 (ob_anim_v1.py = v1, kept), after the audit of 17 Nov: in 3.11 Don takes hold of his vest
and pulls it straight (acts_ob "tug", "tug_down") instead of two fists on his stomach; the frame on the wall in 3.1 is
set_ob v4 (a larger plate, nothing inside); in 3.1 he holds the drawing lower, so his mouth shows while he speaks.
Nothing else changed. Below, the notes of v1.
THE ONBOARDING: the animation, v1: BEAT 03 FIRST (the grill of 17 Nov), on storyboard v3 and script v5.
The question, "Oh...", the pearl, and Don seeing it: the 12 shots 3.1 to 3.12, 1080 x 1920. The other nine beats are
built the same way once this one is approved.
What moves, 12 drawings a second (30 frames a second out):
  - mouths from the takes (sound_ob.film_visemes: phonemes on the drawing grid) on whoever has the line. "Oh..." is
    not a viseme: it is her face (lips parted, one corner up), for as long as the take lasts;
  - her eyes: down him in six drawings, back up in five, then the lids relax. She does not blink from 3.4 to 3.10:
    the look is the action. The Client blinks (he is unaware); Don blinks once, before he covers;
  - the drawing opens as he speaks and springs shut after his line; the pearl turns between finger and thumb and
    stops the moment she sees that Don saw; Don's sales smile drops, then comes back too wide, hands on his vest;
  - camera: a slow push-in on every single, stepped with the drawings; a tilt down him for 3.5 (her look);
  - one emoji pop, on Don's silent reaction (3.9); none on Sofia: her face is the joke;
  - light: a warm key from the upper left and a soft vignette, under the bubbles; paper grain.
Composed for 9:16 here (the storyboard had them as wide tiles): the three-shot 3.1, with OUR FIRST CLIENT on the wall
behind them, empty; the two-shot 3.8, Sofia large in front, the Client behind her with his drawing.
Arms are acts_ob v3 (whole, the elbow hangs). Timing: the animatic's table, each shot rounded to whole drawings.
  python3 ob_anim.py timing             -> ob_anim_timing_v1.json (the whole film, on the drawing grid)
  python3 ob_anim.py stills OUT t ...   -> OUT/ob_anim_<t>.png (t in seconds of the film), 540 x 960
  python3 ob_anim.py sheet OUT.png      -> one drawing in every 1/3 s of the beat, on one sheet
  python3 ob_anim.py render OUT.mp4 [w] -> the beat, silent
  python3 ob_anim.py film OUT.mp4       -> render at 1080 + the beat's sound (sound_ob_mix), muxed"""
import json
import math
import os
import subprocess
import sys
import cairo
import kit
import emoji
import ob_animatic as an
import ob_sofia_sheet as sh
import sofia_ob as so
import client_ob as co
import don_v4 as dv
import acts_ob_v3 as ac
import set_ob as st
from kit import Ctx, INK, ellipse

V = "v2"
BEAT = "3"
W, H, FPS = 540, 960, 30
HERE = os.path.dirname(os.path.abspath(__file__))
TK = json.load(open(os.path.join(HERE, "ob_voices", "film", "takes.json")))
Z = W / 172.0                                              # a storyboard tile at full frame
FLOOR_COL = (0.72, 0.63, 0.50)
BUST, EYES = (0, so.HY + 22), (0, so.HY + 12)
g12 = lambda x: round(x * 12) / 12.0


def build():
    """The whole film on the drawing grid: the animatic's leads and tails, every length a whole number of drawings."""
    shots, t = [], 0.0
    for shot, tm in an.TIMING.items():
        row = dict(shot=shot, t0=round(t, 4))
        if isinstance(tm, tuple):
            lead = g12(tm[0])
            d = max(1 / 12.0, math.ceil((lead + TK[shot]["len"] + tm[1]) * 12 - 0.35) / 12.0)
            row["line"] = dict(who=TK[shot]["who"], text=TK[shot]["text"], t0=round(t + lead, 4),
                               t1=round(t + lead + TK[shot]["len"], 4))
        else:
            d = g12(tm)
        row["d"] = round(d, 4)
        shots.append(row); t = round(t + d, 4)
    return dict(total=t, fps=FPS, shots=shots)


T = build()
SHOT = {s["shot"]: s for s in T["shots"]}
MINE = [s for s in T["shots"] if s["shot"].split(".")[0] == BEAT]
T0, T1 = MINE[0]["t0"], MINE[-1]["t0"] + MINE[-1]["d"]
CUR = dict(t=0.0, tl=0.0, d=1.0, u=0.0, shot="", n=0)


# ---------------------------------------------------------------- time
def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def seg(a, b):
    return ease((CUR["tl"] - a) / max(b - a, 1e-6))


def within(a, b):
    return a - 1e-6 <= CUR["tl"] < b - 1e-6


def blink(*starts):
    return any(within(a, a + 2 / 12.0) for a in starts)


def code():
    """The mouth shape of this shot's speaker now: "" at rest inside the shot, a letter while he speaks."""
    ln = SHOT[CUR["shot"]].get("line")
    if not ln:
        return None
    vis = TK[CUR["shot"]].get("vis") or []
    i = int(round((CUR["t"] - ln["t0"]) * 12))
    return vis[i] if 0 <= i < len(vis) else ""


def speaking(pad=0.0):
    ln = SHOT[CUR["shot"]].get("line")
    return bool(ln) and ln["t0"] - 1e-6 <= CUR["t"] < ln["t1"] + pad


def lerp(a, b, x):
    return tuple(p + (q - p) * x for p, q in zip(a, b))


# ---------------------------------------------------------------- the cast, with lids
def _lids(k, pts, r, skin):
    c = k.c
    for x, y in pts:
        ellipse(k, x, y, r * 1.08, r * 1.08, skin, 5, shadow=False, outline=False)
        c.set_source_rgb(*INK); c.set_line_width(max(1.6, r * 0.26)); c.set_line_cap(1)
        c.move_to(x - r * 0.85, y + r * 0.10); c.curve_to(x - r * 0.3, y + r * 0.48, x + r * 0.3, y + r * 0.48, x + r * 0.85, y + r * 0.10)
        c.stroke()


def client(k, x, feet, s, pose, face, look, shut=False, mouth=None, **kw):
    o = co.client(k, x, feet, s, pose, face, look=look, mouth=mouth or None, **kw)
    if shut:
        hx, hy = o["head"]
        R = co.FACES[face]["eye"]
        _lids(k, [(hx - 17 * s, hy - 1 * s), (hx + 17 * s, hy - 1 * s)], (R + 0.6) * s, co.SKIN)
    return o


def don(k, x, feet, s, act=None, look=None, raw=None, shut=False):
    if raw:
        with ac.arms():
            o = dv.don(k, x, feet, s, raw[0], raw[1], look=look or (-1, 0))
    else:
        o = ac.don(k, x, feet, s, act, look)
    if shut:
        hx, hy = o["head"]
        _lids(k, [(hx - 17 * s, hy + 5 * s), (hx + 17 * s, hy + 5 * s)], 11.8 * s, kit.PEOPLE["DON"]["skin"])
    return o


def sofia_at(k, x, y, s, pt, pose, face, look, lean=0, mouth=None, roll=0.0, rise=0.0, sway=True):
    so.ROLLING[0], so.RISE[0] = roll, rise
    try:
        lag = (1.4 * math.sin(2 * math.pi * CUR["t"] / 1.5), 0) if sway else (0, 0)       # her earrings
        return sh.at(k, x, y, s, pt, pose, face, look=look, lean=lean, mouth=mouth or None, lag=lag)
    finally:
        so.ROLLING[0], so.RISE[0] = 0.0, 0.0


def rolling(start, stop=None):
    """The pearl's turn, one value a drawing, from `start` seconds into the shot; frozen at `stop`."""
    seq = (0.5, 1.0, 0.5, 0.01, -0.5, -1.0, -0.5, 0.01)
    tl = min(CUR["tl"], stop) if stop is not None else CUR["tl"]
    if tl < start:
        return 0.0
    return seq[int(round((tl - start) * 12)) % len(seq)]


# ---------------------------------------------------------------- the frame around a shot
def tile(k, fit=1.0, push=0.03, focus=(270, 400), dy=0.0):
    """Storyboard tile coordinates (172 x 306) at full frame, with the push-in. Returns after c.save()."""
    c = k.c
    z = 1 + push * CUR["u"]
    c.save()
    c.translate(focus[0], focus[1]); c.scale(z, z); c.translate(-focus[0], -focus[1] + dy)
    c.translate(W / 2.0, H); c.scale(fit * Z, fit * Z); c.translate(-86, -306)


def wall(k):
    k.c.set_source_rgb(*kit.WALL); k.c.paint()


def light(k):
    c = k.c
    g = cairo.LinearGradient(0, 0, 420, 620)
    g.add_color_stop_rgba(0, 1.0, 0.96, 0.84, 0.16); g.add_color_stop_rgba(1, 1.0, 0.96, 0.84, 0.0)
    c.set_source(g); c.paint()
    g = cairo.RadialGradient(270, 450, 300, 270, 450, 660)
    g.add_color_stop_rgba(0, 0.10, 0.07, 0.05, 0.0); g.add_color_stop_rgba(1, 0.10, 0.07, 0.05, 0.30)
    c.set_source(g); c.paint()


def bubble(k, who, text, bx, by, tx, ty, size, since):
    """The animatic's bubble, in screen space; it pops in over two drawings from `since` (seconds into the shot)."""
    n = int(round((CUR["tl"] - since) * 12))
    if n < 0:
        return
    pop = (0.82, 1.05)[n] if n < 2 else 1.0
    c = k.c
    c.save(); c.translate(tx, ty); c.scale(pop, pop); c.translate(-tx, -ty)
    an.BUBBLES["_a"] = (who, bx, by, tx, ty, size)
    try:
        an.bubble(k, "_a", text)
    finally:
        del an.BUBBLES["_a"]
    c.restore()


def say(k, bx, by, tx, ty, size):
    ln = SHOT[CUR["shot"]]["line"]
    lead = ln["t0"] - SHOT[CUR["shot"]]["t0"]
    if CUR["t"] < ln["t1"] + 0.25 - 1e-6:
        bubble(k, ln["who"], ln["text"], bx, by, tx, ty, size, lead)


def pop(k, ch, x, y, since, r=40):
    """One emoji in a round tinted bubble, no tail: a silent reaction only."""
    n = int(round((CUR["tl"] - since) * 12))
    if n < 0:
        return
    s = (0.55, 1.14, 0.96)[n] if n < 3 else 1.0
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    c.set_source_rgba(0, 0, 0, 0.18); c.arc(3, 4, r, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(1.0, 0.95, 0.93); c.arc(0, 0, r, 0, 2 * math.pi); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(2.6); c.stroke()
    emoji.draw_emoji(c, ch, 0, 2, r * 1.15)
    c.restore()


# ---------------------------------------------------------------- beat 03, shot by shot
def s3_1(k):
    """Three-shot: he shows them the drawing; it springs shut in his hand. She looks at him, not at it."""
    c = k.c
    ln = SHOT["3.1"]["line"]; lead = ln["t0"] - SHOT["3.1"]["t0"]; end = ln["t1"] - SHOT["3.1"]["t0"]
    snap = g12(end + 0.12)
    z = 1 + 0.025 * CUR["u"]
    c.save(); c.translate(270, 560); c.scale(z, z); c.translate(-270, -560)
    wall(k)
    c.set_source_rgb(*FLOOR_COL); c.rectangle(-20, 870, W + 40, 120); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(2); c.move_to(-20, 870); c.line_to(W + 20, 870); c.stroke()
    st.first_client(k, 404, 176, 1.45)
    c.translate(-16, 400.4); c.scale(1.6, 1.6)                               # the storyboard's wide tile
    fl = 300
    opening = seg(0.08, 0.33)
    shut = CUR["tl"] >= snap - 1e-6
    don(k, 296, fl, 0.80, "stand", (-1.0, 0.75) if shut and CUR["tl"] < snap + 0.5 else (-1.0, 0.35), shut=blink(1.0))
    sofia_at(k, 214, fl, 0.80, (0, 0), "hold", "closed" if blink(1.67) else "smile", (-0.9, -0.3))
    jolt = -3 if within(snap, snap + 1 / 12.0) else 0
    client(k, 80, fl, 0.56, "open", "plain", (0.8, 0.0), shut=blink(snap + 1 / 12.0), mouth=code(), roll=False)
    if shut or opening <= 0:                                                 # sprung shut (or not yet open): the roll
        n = int(round((CUR["tl"] - snap) * 12)) if shut else 9
        ac.roll(k, 96, 168 + jolt + (2 if n == 1 else 0), 0.92, math.pi / 2 - 0.10, ln=118)
    else:
        w = 0.35 + 0.65 * opening * (1.06 if within(0.25, 0.34) else 1.0)
        bob = -1.5 if code() in ("A", "O", "E") else 0.0
        c.save(); c.translate(96, 168 + bob); c.scale(w, 1); ac.blueprint_open(k, 0, 0, 0.92); c.restore()
    for hx in ((96 - 62 * 0.92 * (1 if not shut else 0.95)), (96 + 62 * 0.92 * (1 if not shut else 0.95))):   # his hands on it
        if shut or opening <= 0 or opening > 0.9:
            ellipse(k, hx, 170 + (jolt if shut else 0), 9, 9, co.SKIN, 931, shadow=False, lw=1.6)
    c.restore()
    light(k)
    say(k, 18, 322, 112, 488, 26)


def s3_2(k):
    """Sweet, her head a little to one side."""
    wall(k); tile(k, fit=0.78, push=0.035, focus=(200, 520))
    cd = code()
    sofia_at(k, 86, 149, 1.7, BUST, "hold", "closed" if blink(0.0) else "smile", (-0.8, -0.1), lean=-4 - 1.5 * seg(0.1, 0.6),
             mouth=cd)
    k.c.restore(); light(k)
    say(k, None, 60, 200, 205, 28)


def s3_3(k):
    """Plain. A fact."""
    wall(k); tile(k, push=0.03, focus=(270, 420))
    ln = SHOT["3.3"]["line"]; end = ln["t1"] - SHOT["3.3"]["t0"]
    client(k, 90, 143 - (co.HY + 10) * 1.05, 1.05, "open", "plain", (0.7, 0.0), shut=blink(g12(end + 0.08)), mouth=code())
    k.c.restore(); light(k)
    say(k, None, 50, 254, 152, 32)


def s3_4(k):
    """Her eyes go down him: six drawings."""
    wall(k); tile(k, push=0.02, focus=(270, 470))
    n = max(0, min(6, int(round((CUR["tl"] - 1 / 12.0) * 12))))
    sofia_at(k, 86, 145, 2.3, EYES, "low", "appraise", (-0.8, -0.2 + 1.2 * n / 6.0), sway=False)
    k.c.restore(); light(k)


def s3_5(k):
    """What they are on: him. The camera goes down him as her eyes did. He is unaware: he blinks."""
    wall(k)
    tilt = -150 * seg(0.0, 0.55)
    tile(k, push=0.0, dy=tilt)
    client(k, 90, 143 - (co.HY + 10) * 0.80, 0.80, "open", "plain", (0.0, 0.0), shut=blink(0.33))
    k.c.restore(); light(k)


def s3_6(k):
    """They come back up: five drawings. Then the lids relax and the brows soften."""
    wall(k); tile(k, push=0.03, focus=(270, 470))
    n = max(0, min(5, int(round(CUR["tl"] * 12))))
    if CUR["tl"] < 0.5 - 1e-6:
        sofia_at(k, 86, 145, 2.3, EYES, "low", "appraise", (-0.8, 1.0 - 1.2 * n / 5.0), sway=False)
    else:
        sofia_at(k, 86, 145, 2.3, EYES, "low", "interested", (-0.9, -0.2), sway=False)
    k.c.restore(); light(k)


def s3_7(k):
    """Her hand comes up from below, takes one pearl, and rolls it. "Oh..." """
    wall(k); tile(k, push=0.03, focus=(250, 520))
    face = "oh" if speaking(0.08) else "interested"
    pt = (16, so.BODY_TOP + 18)
    if CUR["tl"] < 1 / 12.0 - 1e-6:
        sofia_at(k, 86, 157, 2.5, pt, "low", face, (-0.9, -0.2), sway=False)
    else:
        rise = 1.0 if CUR["tl"] < 2 / 12.0 - 1e-6 else 0.45 if CUR["tl"] < 3 / 12.0 - 1e-6 else 0.0
        sofia_at(k, 86, 157, 2.5, pt, "pearl", face, (-0.9, -0.2), roll=rolling(0.5), rise=rise, sway=False)
    k.c.restore(); light(k)
    say(k, 270, 215, 226, 252, 36)


def s3_8(k):
    """She rolls the pearl, her eyes on him. He is looking at his drawing."""
    c = k.c
    z = 1 + 0.03 * CUR["u"]
    c.save(); c.translate(330, 430); c.scale(z, z); c.translate(-330, -430)
    wall(k)
    c.set_source_rgb(*FLOOR_COL); c.rectangle(-20, 872, W + 40, 120); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(2); c.move_to(-20, 872); c.line_to(W + 20, 872); c.stroke()
    client(k, 116, 900, 1.16, "arrive", "plain", (-0.6, 1.4), shut=blink(0.5))
    sofia_at(k, 384, 452, 3.5, BUST, "pearl", "interested", (-1.0, -0.1), roll=rolling(0.0))
    c.restore(); light(k)


def s3_9(k):
    """Don has seen it. The sales smile; then he goes still, and his eyes go down."""
    wall(k); tile(k, push=0.045, focus=(270, 380))
    if CUR["tl"] < 3 / 12.0 - 1e-6:
        o = don(k, 86, 163 + 302, 1.0, raw=("stand", "grin"), look=(-1.2, 0.1))
    else:
        o = don(k, 86, 163 + 302, 1.0, "still", (-0.3, 1.5) if CUR["tl"] >= 5 / 12.0 - 1e-6 else (-1.2, 0.1))
    k.c.restore(); light(k)
    pop(k, "\U0001F494", 414, 300, 7 / 12.0, r=52)


def s3_10(k):
    """She sees that he saw. Her hand stops mid-roll; her mouth closes; she does not look away."""
    wall(k); tile(k, push=0.03, focus=(270, 430))
    if CUR["tl"] < 3 / 12.0 - 1e-6:
        sofia_at(k, 86, 149, 1.7, BUST, "pearl", "interested", (-1.0, -0.1), roll=rolling(0.0))
    elif CUR["tl"] < 4 / 12.0 - 1e-6:
        sofia_at(k, 86, 149, 1.7, BUST, "pearl", "interested", (1.0, 0.0), roll=rolling(0.0, 3 / 12.0), sway=False)
    else:
        sofia_at(k, 86, 149, 1.7, BUST, "pearl", "caught", (1.0, 0.0), roll=rolling(0.0, 3 / 12.0), sway=False)
    k.c.restore(); light(k)


def s3_11(k):
    """The vest. The smile comes back, too wide."""
    wall(k); tile(k, push=0.03, focus=(270, 380))
    if CUR["tl"] < 4 / 12.0 - 1e-6:
        don(k, 86, 163 + 302, 1.0, "still", (-0.3, 1.5), shut=within(1 / 12.0, 3 / 12.0))
    else:                                                  # he takes hold of it, pulls once, and holds
        don(k, 86, 163 + 302, 1.0, "tug_down" if within(6 / 12.0, 8 / 12.0) else "tug")
    k.c.restore(); light(k)


def s3_12(k):
    """He saw none of it."""
    wall(k); tile(k, push=0.03, focus=(270, 440))
    ln = SHOT["3.12"]["line"]; end = ln["t1"] - SHOT["3.12"]["t0"]
    feet, s = 143 - (co.HY + 10) * 0.80, 0.80
    lift = -4 if code() in ("A", "E", "O") and within(0.6, 1.2) else 0        # "this": the roll, in his hand
    pose = co.POSES["open"][:2] + co._ik(1, 66, co.BT + 74 + lift)
    o = client(k, 80, feet, s, pose, "plain", (0.7, 0.0), shut=blink(0.0, g12(end + 0.08)), mouth=code(), roll=False)
    hx, hy = o["hands"][1]
    ac.roll(k, hx + 4 * s, hy - 26 * s, s, 0.20, ln=150)
    ellipse(k, hx, hy, co.HAND * s, co.HAND * s, co.SKIN, 971, shadow=False, lw=2 * s)
    k.c.restore(); light(k)
    say(k, None, 40, 236, 216, 28)


ANIM = {"3.1": s3_1, "3.2": s3_2, "3.3": s3_3, "3.4": s3_4, "3.5": s3_5, "3.6": s3_6, "3.7": s3_7, "3.8": s3_8,
        "3.9": s3_9, "3.10": s3_10, "3.11": s3_11, "3.12": s3_12}


# ---------------------------------------------------------------- drawing and rendering
def shot_at(t):
    for s in T["shots"]:
        if s["t0"] - 1e-6 <= t < s["t0"] + s["d"] - 1e-6:
            return s
    return T["shots"][-1]


def draw(c, t, w=540):
    """The drawing for film time t (quantised to the 12 fps grid) into a context w pixels wide."""
    tq = math.floor(t * 12 + 1e-6) / 12.0
    s = shot_at(tq)
    CUR.update(t=tq, tl=tq - s["t0"], d=s["d"], u=(tq - s["t0"]) / s["d"], shot=s["shot"], n=int(round(tq * 12)))
    c.save(); c.scale(w / float(W), w / float(W))
    c.rectangle(0, 0, W, H); c.clip()
    k = Ctx(c, CUR["n"] % 3)
    ANIM[s["shot"]](k)
    kit.grain(k, 0.06)
    c.restore()


def still(t, w=540):
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, w, w * 16 // 9)
    draw(cairo.Context(surf), t, w)
    return surf


def sheet(out, step=1 / 3.0, cols=9, s=0.5):
    ts, t = [], T0
    while t < T1 - 1e-6:
        ts.append(t); t += step
    tw, th = int(W * s), int(H * s)
    rows = (len(ts) + cols - 1) // cols
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, cols * (tw + 6) + 6, rows * (th + 26) + 6)
    c = cairo.Context(surf); c.set_source_rgb(0.16, 0.16, 0.18); c.paint()
    for i, t in enumerate(ts):
        x, y = 6 + (i % cols) * (tw + 6), 6 + (i // cols) * (th + 26)
        c.save(); c.translate(x, y); c.rectangle(0, 0, tw, th); c.clip(); draw(c, t, tw); c.restore()
        c.set_source_rgb(1, 1, 1); c.select_font_face("Inter", 0, 1); c.set_font_size(13)
        c.move_to(x, y + th + 17); c.show_text("%s  %.2f s" % (shot_at(t)["shot"], t - T0))
    surf.write_to_png(out)


def render(out, w=1080):
    """One encoded file for the beat: 30 fps out, a new drawing 12 times a second."""
    h = w * 16 // 9
    tmp = out[:-4] + ".part.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", "%dx%d" % (w, h),
                          "-r", str(FPS), "-i", "-", "-vf", "scale=out_color_matrix=bt709", "-c:v", "libx264", "-preset",
                          "veryfast", "-crf", "17", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries",
                          "bt709", "-color_trc", "bt709", "-an", tmp], stdin=subprocess.PIPE)
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    c = cairo.Context(surf)
    f0, f1 = int(round(T0 * FPS)), int(round(T1 * FPS))
    prev, buf = None, None
    for f in range(f0, f1):
        key = int(math.floor(f / float(FPS) * 12 + 1e-6))
        if key != prev:
            c.set_source_rgb(1, 1, 1); c.paint()
            draw(c, f / float(FPS), w)
            surf.flush(); buf = bytes(surf.get_data()); prev = key
        p.stdin.write(buf)
    p.stdin.close()
    if p.wait() != 0:
        raise SystemExit("ffmpeg failed")
    os.replace(tmp, out)
    print("wrote", out, "%.2f s, %d frames" % (T1 - T0, f1 - f0))


def film(out):
    """The beat with its sound: the film's mix on this timing, cut to the beat, one constant gain to -14 LUFS."""
    import numpy as np
    import soundfile as sf
    import sound_ob_mix as mx
    import sound_bc_mix as bm
    json.dump(T, open(os.path.join(HERE, "ob_anim_timing_%s.json" % V), "w"), indent=1)
    full = mx.main("/tmp/ob_anim_mix_full.wav", timing=os.path.join(HERE, "ob_anim_timing_%s.json" % V), anim=2)
    a, sr = sf.read(full)
    a = a[int(round(T0 * sr)):int(round(T1 * sr))].copy()
    n = int(0.02 * sr); a[:n] *= np.linspace(0, 1, n)[:, None]; a[-n:] *= np.linspace(1, 0, n)[:, None]
    sf.write("/tmp/ob_anim_beat.wav", a.astype("float32"), sr)
    wav = os.path.join(HERE, "ob_anim_beat%s_%s.wav" % (BEAT, V))
    bm.master("/tmp/ob_anim_beat.wav", wav)
    silent = "/tmp/ob_anim_beat%s_silent.mp4" % BEAT
    render(silent, 1080)
    tmp = out[:-4] + ".tmp.mp4"
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-i", wav, "-map", "0:v", "-map", "1:a",
                           "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", tmp])
    os.replace(tmp, out)
    print("wrote", out)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "timing"
    if cmd == "timing":
        json.dump(T, open(os.path.join(HERE, "ob_anim_timing_%s.json" % V), "w"), indent=1)
        for s in MINE:
            ln = s.get("line")
            print("%-5s %6.2f  %.3f s  %s" % (s["shot"], s["t0"] - T0, s["d"], ("%s %.2f-%.2f %s" % (
                ln["who"], ln["t0"] - T0, ln["t1"] - T0, ln["text"])) if ln else ""))
        print("beat %s: %.2f s (film %.2f to %.2f of %.2f s)" % (BEAT, T1 - T0, T0, T1, T["total"]))
    elif cmd == "stills":
        for a in sys.argv[3:]:
            still(T0 + float(a), 540).write_to_png(os.path.join(sys.argv[2], "ob_anim_%06.2f.png" % float(a)))
    elif cmd == "sheet":
        sheet(sys.argv[2])
    elif cmd == "film":
        film(sys.argv[2])
    elif cmd == "render":
        render(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 1080)
