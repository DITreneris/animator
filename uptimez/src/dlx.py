"""UptimeZ Inc. - Downloads Expedition v08 (v7 kept as dlx_v7.py; v6..v1 likewise).
v08: RUSH's first line in a bubble beside his mouth (he stops at x 330), his arm reaches behind his head on the
handover so only the hand shows on the brim.
v07: bubble tails at the speaker's mouth side / head, the blast starts below the DOWNLOADS sign with no
ghost copies, RUSH's arm bends around his face, RUMBLE in the sky, the tower spits out FINAL (29),
the promptanatomy.app card only with TAG=1.
v06: 0.6 s less wide hold before MAX, MAX reacts to "Downloads.", shorter beard, a visible helmet tug,
smear frames on the blast, a pile that sheds sheets before the RUMBLE.
v5 (director pass after the fourth review): props are parented to bodies and drawn in a fixed order.
- The hard hat sits on the head (brim above the eyes) and the lamp beam starts at the lamp: one beam, cut
  out of a darkness layer.
- Name badges are redrawn last, inside each body's transform, so nothing crops or covers them.
- PAM's face sits fully above her desk; her point is a short arm up toward the door.
- Speech bubbles have their tail tip at the speaker's head and never cross a sign or a label.
- No face close-up: after the SAVE card the scene stays wide. FINAL (28) lands on RUSH's hard hat like a lid,
  he squashes under it, face clear below. MAX walks in from the door side, asks, gets the helmet (RUSH slides it
  out, the sheet drops onto his hair), turns and walks into DOWNLOADS. The door snaps open and shut.
- Six sheets in the avalanche, all leaving the frame; at most three pages flutter afterwards.
- promptanatomy.app chip on the building card.
One module, ENDING = "A" | "B" (B adds RUSH: "Downloads."). Render: engine_v.py dlx_a|dlx_b."""
import json
import math
import os
import random
import cairo
import kit
import pt42
import anim
import brand
import dlx_kit as dk
TAG = os.environ.get("TAG", "0") == "1"      # v07: promptanatomy.app card on the building (off = clean version)
from kit import W, H, INK, rect, ellipse, text, file_sheet, monitor, sfx, ease, clamp, lerp, cut, rough_rect_pts

ENDING = "A"
DURATION = 23.0
RAW_T = 0.0
HERE = os.path.dirname(os.path.abspath(__file__))
STATE = {"t": 0.0, "who": None, "skin": (1, 1, 1), "seed": 0}
QA = []                      # per frame: (kind, (x0, y0, x1, y1), size_px); kinds: face, eyes, label, cover, tailmiss
ENV = {}

DOOR = (80, 330, 160, 340)       # x, y, w, h
HOOK = (34, 430)
PAM_X, DESK_Y, PAM_FEET = 460, 650, 832     # PAM's head at y 560, so her whole face is above the desk top
MON = (320, 545, 85, 85)                    # monitor left of her face
SIGN = (296, 236, 30)            # UPTIMEZ INC. wall sign: x, y, h
RX, RF, RS = 300, 900, 1.25      # RUSH under FINAL (28): x, feet, scale
MX, MF, MS = 90, 1010, 1.15      # MAX beside the door
SQ = 0.72                        # how far FINAL (28) squashes RUSH

# timing (s, film time before the 0.6 s trim in beat 4); voices: RUSH 0.6, MAX 17.85, B: RUSH 19.05
T_RUSH_LINE, T_MAX_LINE, T_B_LINE = 0.6, 17.85, 19.05
CUTS = [(8.0, 0.6), (15.5, 0.6)]   # film-time cuts (dlx_a / dlx_b and sound_dlx apply them): pile start, wide hold
POINT = anim.key((-140, -20, 8, 0))       # PAM: short point up toward the door
LEFT_UP = anim.key((-168, 0, 8, 0))       # RUSH: left arm up (trophy, helmet)
TAGS = [  # name, emoji, start, end, character key
    ("RUSH", ["\U0001F3C3", "\U0001F4A6", "\U0001F4C2"], 0.12, 0.6, "rush1"),   # v07: off before his line, so its tail never crosses the tag
    ("PAM", ["\U0001F4BE", "\U0001F4BE", "\U0001F607"], 1.6, 2.45, "pam"),
    ("KEVIN", ["\U0001F480", "\U0001F4C1", "⏳"], 5.85, 6.75, "kevin"),
]


def env():
    if ENV.get("_ending") != ENDING:
        ENV.clear()
        ENV.update(json.load(open(os.path.join(HERE, f"dlx_{ENDING.lower()}_sync.json")))["env"])
        ENV["_ending"] = ENDING
    return ENV


def tag(k, t, i, anchor):
    """Emoji name tag beside a character, while the action continues. anchor = (tail x, tail y, box cx, box cy)."""
    import emoji                                    # colour emoji renderer (standalone copy of s134.draw_emoji)
    name, emo, t0, t1, _ = TAGS[i]
    if not t0 <= t < t1:
        return
    tx, ty, bx, by = anchor
    u = (t - t0) / (t1 - t0)
    pop = 0.6 + 0.4 * anim.back_out(clamp((t - t0) / 0.15)) if u < 0.85 else 1 - (u - 0.85) / 0.15 * 0.4
    w, h = 190, 112
    x0, y0 = bx - w / 2, by - h / 2
    c = k.c
    c.save()
    c.translate(bx, by); c.scale(max(0.02, pop), max(0.02, pop)); c.translate(-bx, -by)
    tail = [(bx - 14, y0 + h - 3), (tx, ty), (bx + 14, y0 + h - 3)] if ty > by else \
           [(bx - 14, y0 + 3), (tx, ty), (bx + 14, y0 + 3)]
    cut(k, tail, (1, 1, 1))
    cut(k, rough_rect_pts(k, x0, y0, w, h, 960 + i, j=1.4), (1, 1, 1))
    c.select_font_face(kit.FONT); c.set_font_size(34)
    e = c.text_extents(name)
    c.move_to(bx - e.width / 2 - e.x_bearing, y0 + 42); c.set_source_rgb(*INK); c.show_text(name)
    for j, ch in enumerate(emo):
        emoji.draw_emoji(c, ch, bx + (j - 1) * 52, y0 + 82, 40)
    c.restore()
    qa("label", (x0, y0, x0 + w, y0 + h), 34)


# ------------------------------------------------------------------ props and sets
def gear_hook(k, helmet=True, rope=True):
    x, y = HOOK
    rect(k, x - 4, y - 6, 8, 16, (0.4, 0.4, 0.42), 700, shadow=False)
    if rope:
        c = k.c
        for i in range(3):
            c.save(); c.translate(x, y + 60 + i * 4); c.scale(1, 1.3)
            c.arc(0, 0, 22, 0, 2 * math.pi)
            c.set_source_rgb(*dk.ROPE); c.set_line_width(6); c.stroke_preserve()
            c.set_source_rgb(*INK); c.set_line_width(1); c.stroke(); c.restore()
    if helmet:
        dk.helmet(k, x, y + 40, 0.45, lamp=0)


def cave_in_door(k, open_amt):
    x, y, w, h = DOOR
    c = k.c
    c.save(); c.rectangle(x, y, w * open_amt + 1, h); c.clip()
    rect(k, x, y, w, h, (0.10, 0.09, 0.09), 710, shadow=False, outline=False)
    for i in range(6):
        sc = 1 - i * 0.14
        c.set_source_rgba(0.9, 0.88, 0.8, 0.55 * sc)
        c.rectangle(x + w / 2 - 80 * sc, y + 40 + i * 48, 50 * sc, 10 * sc); c.fill()
        c.rectangle(x + w / 2 + 30 * sc, y + 60 + i * 48, 50 * sc, 10 * sc); c.fill()
    c.set_source_rgba(1, 1, 1, 0.15)
    c.move_to(x + w / 2 - 6, y); c.line_to(x + w / 2 - 70, y + h); c.line_to(x + w / 2 + 70, y + h); c.line_to(x + w / 2 + 6, y)
    c.fill()
    c.restore()


def punch(t0, dur=0.2):
    """Kinetic scale for a label that appears at t0: overshoot, then settle."""
    u = (STATE["t"] - t0) / dur
    return 1.0 if t0 is None or u >= 1 else max(0.02, anim.back_out(clamp(u), 2.2))


def flash(k, t, t0):
    """Impact frame: two frames of white over the shot at t0."""
    d = t - t0
    if 0 <= d < 0.14:
        c = k.c
        c.set_source_rgba(1, 1, 1, 0.8 if d < 0.07 else 0.35)
        c.rectangle(-20, -20, W + 40, H + 40); c.fill()


def big_file(k, x, y, w, h, s, rot, seed, size, register=True, pop_t=None):
    c = k.c
    c.save(); c.translate(x, y); c.rotate(rot)
    if pop_t is not None:
        sc = punch(pop_t); c.scale(sc, sc)
    file_sheet(k, 0, 0, w, h, "", seed)
    text(k, s, 0, 0, size, INK)
    c.restore()
    c.select_font_face(kit.FONT); c.set_font_size(size)
    tw = c.text_extents(s).x_advance                 # v07: measured, not estimated
    if register:
        qa("label", (x - tw / 2, y - size / 2, x + tw / 2, y + size / 2), size)


def speed_lines(k, x, y, n=7, length=120, alpha=0.6):
    c = k.c
    c.set_source_rgba(0.2, 0.2, 0.22, alpha); c.set_line_width(3)
    r = random.Random(int(x))
    for i in range(n):
        yy = y + r.uniform(-120, 120)
        c.move_to(x + 40, yy); c.line_to(x + 40 + length * r.uniform(0.5, 1), yy); c.stroke()


def whip(k, tl, dur=0.14):
    u = clamp(tl / dur)
    if u >= 1:
        return 0.0
    c = k.c
    c.set_source_rgba(1, 1, 1, 0.5 * (1 - u))
    r = random.Random(int(tl * 100))
    for _ in range(14):
        c.rectangle(-20, r.uniform(0, H), W + 40, r.uniform(3, 12)); c.fill()
    return (1 - ease(u)) * 260


def cave_dark(k, seed=740):
    c = k.c
    rect(k, -20, -20, W + 40, H + 40, (0.12, 0.11, 0.11), seed, shadow=False, outline=False)
    r = random.Random(3)
    for i in range(18):
        file_sheet(k, r.uniform(-20, W + 20), r.uniform(80, 900), 70, 50, "", seed + 1 + i, rot=r.uniform(-0.5, 0.5))
    c.set_source_rgba(0, 0, 0, 0.55); c.rectangle(-20, -20, W + 40, H + 40); c.fill()


def save_window(k, t):
    c = k.c
    rect(k, -20, -20, W + 40, H + 40, (0.18, 0.18, 0.2), 800, shadow=False, outline=False)
    rect(k, 40, 250, 460, 400, (0.55, 0.78, 0.95), 801)
    rect(k, 40, 250, 460, 46, brand.NAVY, 803, shadow=False)                 # branded title bar
    brand.mark(c, 52, 257, 32, zzz=False)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(20)
    c.set_source_rgb(1, 1, 1); c.move_to(94, 280); c.show_text("UptimeZ Drive")
    label(k, "FINAL (28)", 270, 372, 54, pop_t=13.55)
    pressed = 14.2 <= t < 14.35
    rect(k, 150, 440 + (4 if pressed else 0), 240, 84, brand.GREEN if not pressed else (0.15, 0.55, 0.35), 802)
    label(k, "SAVE", 270, 482 + (4 if pressed else 0), 44, (1, 1, 1))
    cx, cy = lerp(430, 300, ease(clamp((t - 13.6) / 0.5))), lerp(610, 500, ease(clamp((t - 13.6) / 0.5)))
    c.set_source_rgb(1, 1, 1)
    c.move_to(cx, cy); c.line_to(cx, cy + 34); c.line_to(cx + 9, cy + 26); c.line_to(cx + 22, cy + 26); c.close_path()
    c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2); c.stroke()


def tower(k, t, shake_amt=0.0, open_win=0.0):
    """The UptimeZ tower from outside: glass and window grid, lockup sign with the tagline."""
    c = k.c
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, 0.55, 0.78, 0.95); g.add_color_stop_rgb(1, 0.85, 0.92, 0.98)
    c.set_source(g); c.rectangle(-20, -20, W + 40, H + 40); c.fill()
    for i, (bx, bw, bh) in enumerate(((10, 90, 360), (450, 110, 420))):        # neighbours
        rect(k, bx, 870 - bh, bw, bh, (0.62, 0.68, 0.76), 1200 + i)
    jx = math.sin(t * 60) * 4 * shake_amt
    c.save(); c.translate(jx, 0)
    rect(k, 120, 260, 300, 610, brand.NAVY, 1210)
    for row in range(11):
        for col in range(5):
            lit = (row * 7 + col * 3) % 5 != 0
            wx, wy = 140 + col * 56, 290 + row * 52
            rect(k, wx, wy, 40, 34, (0.98, 0.9, 0.55) if lit else (0.35, 0.42, 0.55), 1220 + row * 5 + col,
                 shadow=False, lw=1.5)
    WX, WY = 140 + 2 * 56, 290 + 7 * 52             # the window that spits out a page
    if open_win > 0:
        rect(k, WX, WY, 40, 34, (0.1, 0.1, 0.12), 1290, shadow=False, lw=1.5)
    rect(k, 150, 170, 240, 74, (1, 1, 1), 1295, lw=2)
    brand.lockup(c, 162, 181, 52, tagline=True)
    c.restore()
    qa("label", (150, 170, 390, 244), 26)
    rect(k, -20, 868, W + 40, 120, (0.55, 0.55, 0.52), 1296, shadow=False)
    return WX + 20 + jx, WY + 17




def qa(kind, box, size=0):
    QA.append((kind, tuple(box), size))


def label(k, s, x, y, size, col=INK, pop_t=None):
    if pop_t is not None:
        c = k.c
        sc = punch(pop_t)
        c.save(); c.translate(x, y); c.scale(sc, sc); text(k, s, 0, 0, size, col); c.restore()
    else:
        text(k, s, x, y, size, col)
    w = size * 0.55 * len(s)
    qa("label", (x - w / 2, y - size / 2, x + w / 2, y + size / 2), size)


# ------------------------------------------------------------------ faces: lip-sync + blink
_orig_face = kit.face_draw


def face_live(k, x, y, face, look, glasses=False, seed=0):
    _orig_face(k, x, y, face, look, glasses=glasses, seed=seed)
    who, f, c = STATE["who"], int(STATE["t"] * 30), k.c
    if who is None:
        return
    if face not in ("happy", "pleased", "smug", "hollow") and ((f + STATE["seed"] * 13) % 84) < 3:
        for sx in (-17, 17):
            ellipse(k, x + sx, y, 15, 15, STATE["skin"], 9000 + sx, shadow=False, outline=False)
            c.set_source_rgb(*INK); c.set_line_width(4)
            c.move_to(x + sx - 11, y + 2); c.line_to(x + sx + 11, y + 2); c.stroke()
    o = talk(who)
    if o:
        ellipse(k, x, y + 28, 19, 12, STATE["skin"], 9100, shadow=False, outline=False)
        ellipse(k, x, y + 30, 13 + 5 * o, 3 + 14 * o, (0.35, 0.08, 0.08), 9101, shadow=False, lw=2)


kit.face_draw = face_live


def talk(name):
    e, f = env().get(name), int(STATE["t"] * 30)
    return e[f] if e and 0 <= f < len(e) and e[f] > 0.12 else 0.0


def badge(k, name, x, feet, s):
    """Name badge redrawn last, inside the body's transform: never cropped, never under an arm or a rope."""
    p = kit.PEOPLE[name]
    bt = -300 * p["h"] + 78
    bx = 12 if p.get("tie") else -17
    if name == "PAM":                                # she sits behind the desk: badge high on the chest, above its top
        bt -= 22
    c = k.c
    c.save(); c.translate(x, feet); c.scale(s, s)
    rect(k, bx, bt + 30, 34, 21, (1, 1, 1), 9300, shadow=False, lw=1.4)
    c.set_source_rgb(*brand.GREEN); c.rectangle(bx + 3, bt + 32, 28, 3.5); c.fill()
    c.select_font_face(kit.FONT); c.set_font_size(11)
    e = c.text_extents(name)
    size = min(11.0, 11.0 * 27 / e.width)
    c.set_font_size(size); e = c.text_extents(name)
    c.move_to(bx + 17 - e.width / 2 - e.x_bearing, bt + 46); c.set_source_rgb(*INK); c.show_text(name)
    c.restore()


def register_face(hx, hy, s, sy=1.0):
    qa("face", (hx - 50 * s, hy - 50 * s * sy, hx + 50 * s, hy + 50 * s * sy))
    qa("eyes", (hx - 38 * s, hy - 15 * s * sy, hx + 38 * s, hy + 15 * s * sy))


def who(name, k, fn, x, feet, s, *a, seed=1, register=True, **kw):
    STATE.update(who=name, skin=kit.PEOPLE[name]["skin"], seed=seed)
    p = fn(k, x, feet, s, *a, badge=False, **kw) if fn is dk.rush else fn(k, name, x, feet, s, *a, badge=False, **kw)
    STATE["who"] = None
    badge(k, name, x, feet, s)
    if register:
        register_face(*p["head"], s)
    return p


def rush(k, x, feet, s, look, pose="stand", face="neutral", lamp=1.0, seed=31, register=True, gaze=(0, 0),
         helmet_on=True):
    p = who("RUSH", k, dk.rush, x, feet, s, look, pose=pose, face=face, seed=seed, t=STATE["t"], lamp=lamp,
            register=register, gaze=gaze, helmet_on=helmet_on)
    o = talk("RUSH") if look == "after" else 0
    if o:                                            # the beard covers the face's mouth: draw the talking mouth on top
        c = k.c
        c.save(); c.translate(x, feet); c.scale(s, s)
        ellipse(k, 0, -254 + 32, 13 + 5 * o, 3 + 14 * o, (0.35, 0.08, 0.08), 9102, shadow=False, lw=2)
        c.restore()
    if helmet_on and look != "office" and register:
        hx, hy = p["head"]                           # the hat brim is a prop: QA checks it never reaches the eyes
        qa("cover", (hx - 70 * s, hy - 32 * s, hx + 70 * s, hy - 20 * s))
    return p


def person(k, name, x, feet, s, pose="stand", face="neutral", look=(0, 0), seed=1, register=True):
    return who(name, k, pt42.branded_person, x, feet, s, pose=pose, face=face, look=look, seed=seed,
               register=register)


def lamp_pos(x, feet, s):
    """Where RUSH's head lamp is (dk.helmet: lamp at head y - 64*s)."""
    return x, feet - 254 * s - 64 * s


# ------------------------------------------------------------------ speech bubbles
def speech(k, t, s, cx, cy, tip, t0, t1, speaker=None, size=40):
    """Bubble box centred near (cx, cy), tail tip at `tip` (next to the speaker's head). Rows split on '\\n'.
    speaker = (head x, head y, scale): QA flags a tail that ends away from the head."""
    if not t0 <= t < t1:
        return
    c = k.c
    c.select_font_face(kit.FONT); c.set_font_size(size)
    rows = s.split("\n")
    ex = [c.text_extents(r) for r in rows]
    bw = max(e.x_advance for e in ex) + 52
    lh = size * 1.12
    bh = lh * len(rows) + 34
    bx = clamp(cx - bw / 2, 26, W * 0.88 - 2 - bw)
    by = cy - bh / 2
    pop = 0.85 + 0.15 * ease(clamp((t - t0) / 0.12))
    c.save(); c.translate(bx + bw / 2, by + bh / 2); c.scale(pop, pop); c.translate(-(bx + bw / 2), -(by + bh / 2))
    tx, ty = tip
    if ty > by + bh:
        m = clamp(tx, bx + 34, bx + bw - 34); tail = [(m - 15, by + bh - 3), (tx, ty), (m + 15, by + bh - 3)]
    elif ty < by:
        m = clamp(tx, bx + 34, bx + bw - 34); tail = [(m - 15, by + 3), (tx, ty), (m + 15, by + 3)]
    elif tx < bx:
        m = clamp(ty, by + 22, by + bh - 22); tail = [(bx + 3, m - 13), (tx, ty), (bx + 3, m + 13)]
    else:
        m = clamp(ty, by + 22, by + bh - 22); tail = [(bx + bw - 3, m - 13), (tx, ty), (bx + bw - 3, m + 13)]
    cut(k, tail, (1, 1, 1))
    cut(k, rough_rect_pts(k, bx, by, bw, bh, 900 + len(s), j=1.6), (1, 1, 1))
    kit._poly(c, tail); c.set_source_rgb(1, 1, 1); c.fill()
    c.set_source_rgb(*INK)
    for i, (r, e) in enumerate(zip(rows, ex)):
        c.move_to(bx + bw / 2 - e.x_advance / 2, by + 17 + lh * (i + 0.5) + size * 0.36); c.show_text(r)
    c.restore()
    qa("label", (bx, by, bx + bw, by + bh), size)
    if speaker and math.hypot(tx - speaker[0], ty - speaker[1]) > 95 * speaker[2]:
        qa("tailmiss", (tx, ty, tx, ty))


# ------------------------------------------------------------------ light
def beam_poly(sx, sy, tx, ty, spread):
    ang = math.atan2(ty - sy, tx - sx)
    L = math.hypot(tx - sx, ty - sy) + 500
    nx, ny = -math.sin(ang), math.cos(ang)
    ex, ey = sx + math.cos(ang) * L, sy + math.sin(ang) * L
    return [(sx + nx * 5, sy + ny * 5), (ex + nx * spread, ey + ny * spread), (ex - nx * spread, ey - ny * spread),
            (sx - nx * 5, sy - ny * 5)]


def dark_beam(k, src, tgt, spread=170, dark=0.6, glow=0.2):
    """One beam whose tip is the lamp: darkness everywhere else, a warm glow inside."""
    c = k.c
    pts = beam_poly(*src, *tgt, spread)
    c.save(); c.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    c.rectangle(-40, -40, W + 80, H + 80); kit._poly(c, pts)
    c.set_source_rgba(0, 0, 0, dark); c.fill(); c.restore()
    kit._poly(c, pts); c.set_source_rgba(1, 0.95, 0.6, glow); c.fill()


def beam(k, sx, sy, tx, ty, spread=170, a=0.3):
    kit._poly(k.c, beam_poly(sx, sy, tx, ty, spread)); k.c.set_source_rgba(1, 0.95, 0.6, a); k.c.fill()


# ------------------------------------------------------------------ sets
def office(k, door_open=0.0, hook=(True, True), pam=True, pam_pose="type", pam_face="neutral"):
    kit.office_bg(k)
    pt42.wall_sign(k, *SIGN)
    qa("label", (SIGN[0] - 12, SIGN[1] - 10, SIGN[0] + 150, SIGN[1] + SIGN[2] + 10), 20)
    door_set(k, door_open)
    gear_hook(k, *hook)
    if pam:
        monitor(k, *MON, 730)
        person(k, "PAM", PAM_X, PAM_FEET, 1.0, pose=pam_pose, face=pam_face, look=(-1, 0.4), seed=44)
        kit.desk(k, PAM_X - 135, DESK_Y, 220, 731)
        qa("cover", (PAM_X - 135, DESK_Y, PAM_X + 85, DESK_Y + 136))


def door_set(k, open_amt):
    x, y, w, h = DOOR
    kit.door(k, x, y, w, h, 720, open_amt=open_amt)
    qa("label", (x + w / 2 - 75, y - 52, x + w / 2 + 75, y - 18), 22)
    if open_amt > 0:
        cave_in_door(k, open_amt)


def door_slab(k, shut):
    """The door swinging shut over whatever is in the doorway (one slab, snapping)."""
    if shut <= 0:
        return
    x, y, w, h = DOOR
    rect(k, x, y, w * shut, h, (0.80, 0.62, 0.42), 722)
    if shut >= 1:
        ellipse(k, x + w - 16, y + h * 0.55, 6, 6, (0.85, 0.75, 0.2), 723, shadow=False, lw=1.5)


def snap_open(t, t0, dur=0.15):
    return ease(clamp((t - t0) / dur))


def poof(k, x, y, u, n=9, r0=40, r1=120):
    """Impact lines radiating from a landing point (instead of dust discs)."""
    if not 0 <= u < 1:
        return
    c = k.c
    c.set_source_rgba(*INK, 1 - u); c.set_line_width(4); c.set_line_cap(cairo.LINE_CAP_ROUND)
    for i in range(n):
        a = math.pi + i * math.pi / (n - 1)
        ra, rb = lerp(r0, r1, u), lerp(r0 + 30, r1 + 50, u)
        c.move_to(x + math.cos(a) * ra, y + math.sin(a) * ra * 0.5)
        c.line_to(x + math.cos(a) * rb, y + math.sin(a) * rb * 0.5); c.stroke()


def flutter_pages(k, t, t0, n=3, seed=5):
    """At most three pages drifting down the left edge, clear of every face and line."""
    r = random.Random(seed)
    for i in range(n):
        x, y, rot = anim.flutter(r.uniform(28, 60), r.uniform(-200, -40), t - t0, i, fall=r.uniform(110, 150), sway=12)
        if y < H + 60:
            file_sheet(k, x, y, 44, 56, "", 860 + i, rot=rot)
            qa("cover", (x - 28, y - 32, x + 28, y + 32))


# ------------------------------------------------------------------ beats
def b1_question(k, t, tl):
    STATE["t"] = t
    point = anim.keyed(t, [(0, "type"), (1.55, POINT)], dur=0.2)
    office(k, door_open=snap_open(t, 2.2), pam_pose=point)
    sprint = clamp(t / 0.45)
    x = lerp(640, 330, ease(sprint))                 # v08: stops further right, room for his bubble
    if sprint < 1:
        pose, bob = anim.walk(t, speed=7, swing=40)
        speed_lines(k, x, 760)
        for i in range(3):                           # pages flapping off him, out of the right edge
            file_sheet(k, x + 70 + i * 50 + t * 300, 820 + i * 40, 44, 54, "", 880 + i, rot=t * 8 + i)
    else:
        pose = anim.keyed(t, [(0.45, "panic"), (2.1, (-40, 0, -100, 0))], dur=0.15)
        bob = 0
    c = k.c
    if sprint < 1:                                   # smear: stretched along the run
        c.save(); anim.squash(c, x, 960, 1.28, 0.92)
    else:                                            # panic jitter until the door opens
        jr = random.Random(int(t * 12))
        x += jr.uniform(-3, 3) if t < 2.2 else 0
    p = rush(k, x, 960 + bob, 1.0, "office", pose=pose, face="panic" if t < 2.7 else "shock", register=sprint >= 1)
    if sprint < 1:
        c.restore()
    hx, hy = p["head"]
    tag(k, t, 0, (hx - 20, hy - 70, min(max(120, hx - 70), 300), hy - 170))
    tag(k, t, 1, (PAM_X - 15, 505, 300, 445))
    speech(k, t, "Where's\nthe final?", 127, hy + 28, (hx - 54, hy + 28), T_RUSH_LINE, 1.6, speaker=(hx, hy, 1.0),
           size=36)                                    # v08: beside his mouth, short tail


def b2_gear(k, t, tl):
    STATE["t"] = t
    c = k.c
    if t < 3.9:
        office(k, door_open=1.0, hook=(t < 3.0, t < 3.45), pam=False)
        on = t >= 3.1
        pose = LEFT_UP if 3.0 <= t < 3.1 else "stand"
        slam = 3.1 <= t < 3.2
        if slam:
            c.save(); anim.squash(c, 165, 1010, 1.08, 0.9)
        p = rush(k, 165, 1010, 1.35, "expedition" if on else "office", pose=pose,
                 face="shock" if t < 3.1 else "neutral", helmet_on=on)
        if slam:
            c.restore()
        if 3.0 <= t < 3.1:                           # helmet off the hook, up in his hand, about to slam on
            hx, hy = p["hands"][0]
            dk.helmet(k, hx + 30, hy + 60, 1.2, lamp=0)
        return
    rect(k, -20, -20, W + 40, H + 40, (0.13, 0.12, 0.12), 739, shadow=False, outline=False)
    c.save(); c.translate(whip(k, RAW_T - 3.9), 0)
    dk.cave(k, labels=False)
    u = ease(clamp((t - 3.95) / 1.0))
    c.set_source_rgb(*dk.ROPE); c.set_line_width(3)
    c.move_to(W / 2, 180); c.line_to(W / 2, lerp(250, 560, u)); c.stroke()
    feet = lerp(330, 640, u)
    rush(k, W / 2, feet, 0.42, "expedition", pose="hold_up", face="neutral", register=False)
    c.restore()
    hy = feet - 254 * 0.42
    speech(k, t, "Hellooo?", 130, hy, (W / 2 - 28, hy), 4.1, 4.95, speaker=(W / 2, hy, 0.6))


def b3_kevin(k, t, tl):
    STATE["t"] = t
    c = k.c
    if t < 5.6:                                       # the lamp beam sweeps the dark, searching
        cave_dark(k)
        dk.kevin(k, 400, 760, 1.05, final_size=21)
        sweep = ease(clamp((t - 5.0) / 0.6))
        dark_beam(k, lamp_pos(150, 980, 1.2), (lerp(-100, 400, sweep), lerp(250, 620, sweep)))
        rush(k, 150, 980, 1.2, "expedition", pose="stand", face="neutral")
        return
    if t < 6.8:                                       # crash zoom onto KEVIN (RUSH is off-frame left)
        z = lerp(1.6, 1.45, ease(clamp((RAW_T - 5.6) / 1.2))) * (1 + 0.15 * (1 - ease(clamp((RAW_T - 5.6) / 0.15))))
        c.save(); anim.camera(c, 400, 640, z, dx=-130, dy=-40)
        cave_dark(k)
        beam(k, -200, 300, 400, 620, a=0.35)
        dk.kevin(k, 400, 760, 1.05, final_size=21)
        c.restore()
        sy = 600 + (581.5 - 640) * z                  # skull centre after the camera move
        ly = 600 + (713.8 - 640) * z                  # FINAL (3) label
        qa("face", (270 - 46 * z, sy - 44 * z, 270 + 46 * z, sy + 44 * z))
        qa("label", (270 - 55 * z, ly - 11 * z, 270 + 55 * z, ly + 11 * z), 21 * z)
        tag(k, t, 2, (270, sy - 48 * z, 270, sy - 48 * z - 110))
        flash(k, t, math.ceil(5.6 * 12) / 12)              # first drawn frame of the zoom (12 fps)
        return
    cave_dark(k)                                      # RUSH: eyes pop, then a clear salute, then moves on
    salute = anim.keyed(t, [(6.8, "stand"), (7.05, (-8, 0, 150, 69)), (7.6, "stand")], dur=0.12)
    x = lerp(240, -160, ease(clamp((t - 7.65) / 0.35)))
    dark_beam(k, lamp_pos(x, 1240, 2.0), (x + 380, 560), spread=150, dark=0.45)
    rush(k, x, 1240, 2.0, "expedition", pose=salute, face="shock" if t < 7.05 else "neutral")


def b4_pull(k, t, tl):
    STATE["t"] = t
    c = k.c
    rect(k, -20, -20, W + 40, H + 40, (0.12, 0.11, 0.11), 750, shadow=False, outline=False)
    wob = math.sin(t * 30) * lerp(4, 8, clamp((t - 9.6) / 0.4)) * clamp((t - 9.6) / 0.2)
    r = random.Random(7)
    lean = -0.035 * ease(clamp((t - 9.55) / 0.25))   # anticipation: the pile leans before it goes
    sag = ease(clamp((t - 9.05) / 0.5))              # the gap left by FINAL (27) makes the top slide
    c.save(); c.translate(wob + 330, 900); c.rotate(lean); c.translate(-330, -900)
    for i in range(70):
        yy = 900 - i * 13
        half = 240 - i * 2.8
        top = clamp((i - 25) / 45)
        file_sheet(k, 330 + r.uniform(-half, half) - 30 * sag * top, yy + 40 * sag * top, 80, 56, "", 751 + i,
                   rot=r.uniform(-0.35, 0.35) + 0.2 * sag * top)
    c.restore()
    pulled = ease(clamp((t - 9.0) / 0.2))
    pose = anim.keyed(t, [(8, "stand"), (8.6, "reach_r"), (9.0, (-30, 0, 70, 20))], dur=0.15)
    rx = lerp(170, 130, pulled)
    wind = 8.85 <= t < 9.0
    snap_ = 9.0 <= t < 9.15
    c.save()
    if wind or snap_:
        anim.squash(c, rx, 990, 0.9 if wind else 1.14, 1.07 if wind else 0.93)
    p = rush(k, rx, 990, 1.15, "expedition", pose=pose,
             face="happy" if 9.2 <= t < 9.75 else ("shock" if t >= 9.75 else "neutral"))
    c.restore()
    if t < 9.0:                                      # in the pile, drawn over his reaching hand
        big_file(k, 400, 790, 130, 90, "FINAL (27)", 0.05, 760, 24, pop_t=8.6)
    else:                                            # parented to his hand
        hx, hy = p["hands"][1]
        big_file(k, hx + 58, hy - 30, 130, 90, "FINAL (27)", 0.05, 760, 24)
    for j in range(6):                               # v06: the top sheds sheets before it goes (under the word)
        u = (t - 9.6 - j * 0.1) / 0.7
        if 0 < u < 1:
            side = -1 if j % 2 else 1
            file_sheet(k, 330 + side * (40 + 260 * u), 60 + j * 24 + 900 * u * u, 80, 56, "", 1500 + j,
                       rot=side * (0.3 + 4 * u))
    if t >= 9.8:
        sfx(k, "RUMBLE", 300, 300, 76, rot=-0.08)
        qa("label", (130, 260, 470, 340), 76)


SHEETS = [(-170, 260), (-170, 640), (-120, 1100), (90, 1160), (-60, -170), (220, -190)]   # avalanche exits


def b5_beard(k, t, tl):
    STATE["t"] = t
    office(k, door_open=1.0, hook=(False, False), pam=True, pam_pose="type")
    c = k.c
    x, y, w, h = DOOR
    d = t - 10.5
    ox, oy = x + w / 2, y + h / 2 + 40
    for i, (ex, ey) in enumerate(SHEETS):            # six sheets blast out and leave the frame
        u = ease(clamp((d - i * 0.04) / 0.55), )
        if 0 < u < 1:
            file_sheet(k, lerp(ox, ex, u), lerp(oy, ey, u), 90, 112, "", 770 + i, rot=i + d * 7)
    if d >= 0.7:
        flutter_pages(k, t, 11.2)
    if d < 0.5:                                      # RUSH shoots out of the door, slightly tumbling, smeared
        u = d / 0.5
        oy0 = oy + 150                               # v07: starts below the DOWNLOADS sign
        ang = math.atan2(960 - oy0, RX - ox)

        def flyer(uu, alpha):
            if uu < 0:
                return
            px, py = lerp(ox, RX, ease(uu)), lerp(oy0, 960, ease(uu))
            if alpha < 1:
                c.push_group()
            c.save(); c.translate(px, py)
            c.rotate(ang); c.scale(1.22, 0.86); c.rotate(-ang)              # stretched along the flight
            c.rotate(-0.2 * (1 - uu))
            rush(k, 0, 0, lerp(0.9, 1.25, uu), "expedition", pose="shock", face="shock", register=False)
            c.restore()
            if alpha < 1:
                c.pop_group_to_source(); c.paint_with_alpha(alpha)

        c.set_source_rgba(0.2, 0.2, 0.22, 0.55); c.set_line_width(3)
        px, py = lerp(ox, RX, ease(u)), lerp(oy0, 960, ease(u))
        for i in range(6):                           # speed lines trailing along the path, at body height
            off = (i - 2.5) * 22
            nx, ny = -math.sin(ang) * off, math.cos(ang) * off
            L0, L1 = 90, 160 + 20 * (i % 3)
            c.move_to(px + nx - math.cos(ang) * L0, py - 150 + ny - math.sin(ang) * L0)
            c.line_to(px + nx - math.cos(ang) * L1, py - 150 + ny - math.sin(ang) * L1); c.stroke()
        flyer(u, 1.0)
        sc = lerp(0.9, 1.25, u)                      # his head and hat, so QA sees what he flies across
        qa("cover", (px - 75 * sc, py - 330 * sc, px + 75 * sc, py - 200 * sc))
        return
    land = 1 - 0.15 * math.exp(-(d - 0.5) * 12)
    raise_ = t >= 12.5
    pose = anim.keyed(t, [(11.0, "stand"), (12.5, LEFT_UP)], dur=0.15)
    c.save(); anim.squash(c, RX, 960, 2 - land, land)
    p = rush(k, RX, 960, RS, "after", pose=pose, face="hollow" if not raise_ else "happy",
             lamp=0.5 + 0.5 * (int(t * 8) % 2))
    c.restore()
    poof(k, RX, 965, (d - 0.5) / 0.3)
    if t >= 12.65:                                   # the trophy appears once the arm is up
        hx, hy = p["hands"][0]
        lift = anim.back_out(clamp((t - 12.65) / 0.25))
        big_file(k, hx - 4, hy - 72 * lift, 150, 100, "FINAL (27)", -0.06, 780, 28)
        if t < 13.2:                                 # ta-da sparkle
            for i in range(6):
                a2 = i * math.pi / 3 + t * 3
                ellipse(k, hx - 4 + math.cos(a2) * 95, hy - 72 + math.sin(a2) * 70, 6, 6, (1, 0.9, 0.3), 790 + i,
                        shadow=False, lw=1)
        hx, hy = p["head"]
        speech(k, t, "Got it!", 372, 440, (hx + 40, hy - 62), 12.7, 13.45, speaker=(hx, hy, RS))


def squashed_rush(k, t, sq, lamp, gaze=(0, 0), face="hollow", helmet_on=True, pose="stand"):
    """RUSH squashed under FINAL (28) at (RX, RF). Returns head (x, y) and the helmet top in canvas coords."""
    c = k.c
    c.save(); anim.squash(c, RX, RF, 1 + (1 - sq) * 0.45, sq)
    rush(k, RX, RF, RS, "after", pose=pose, face=face, lamp=lamp, register=False, gaze=gaze, helmet_on=helmet_on)
    c.restore()
    hy = RF - 254 * RS * sq
    register_face(RX, hy, RS, sq)
    if helmet_on:
        qa("cover", (RX - 70 * RS * 1.1, hy - 32 * RS * sq, RX + 70 * RS * 1.1, hy - 20 * RS * sq))
    top = RF - (254 + 78) * RS * sq if helmet_on else hy - 50 * RS * sq
    return (RX, hy), top


def lid(k, bottom, register=True):
    """FINAL (28) resting on top of RUSH (its bottom edge on his hat, later on his hair)."""
    big_file(k, RX, bottom - 85, 200, 170, "FINAL (28)", -0.03, 812, 34, register=register)


def wide_after(k, t, sq, lamp, gaze=(0, 0), face="hollow", helmet_on=True, lid_bottom=None, pam_pose="type"):
    office(k, door_open=1.0, hook=(False, False), pam=True, pam_pose=pam_pose)
    head, top = squashed_rush(k, t, sq, lamp, gaze=gaze, face=face, helmet_on=helmet_on)
    lid(k, top if lid_bottom is None else lid_bottom)
    return head


def b6_save(k, t, tl):
    """SAVE card -> FINAL (28) falls on RUSH's hard hat (THUNK) -> wide: MAX walks in and asks."""
    STATE["t"] = t
    c = k.c
    if t < 14.6:
        save_window(k, t)
        return
    if t < 15.2:
        office(k, door_open=1.0, hook=(False, False), pam=True, pam_pose="click")
        sq = lerp(1.0, SQ, ease(clamp((t - 14.95) / 0.12)))
        sq = sq - 0.04 * math.sin(clamp((t - 15.07) / 0.13) * math.pi)           # little bounce
        if t < 14.95:
            p = rush(k, RX, RF, RS, "after", pose="stand", face="shock", lamp=1.0, gaze=(0, -1))
            hx, hy = p["hands"][1]
            big_file(k, hx + 20, hy - 4, 110, 74, "FINAL (27)", 0.05, 780, 22)
            fall = ease(clamp((t - 14.6) / 0.35))
            big_file(k, RX, lerp(-200, RF - (254 + 78) * RS - 85, fall), 200, 170, "FINAL (28)", -0.03, 812, 34,
                     register=fall >= 1)
            return
        head, top = squashed_rush(k, t, sq, 1.0)
        lid(k, top)
        u = ease(clamp((t - 14.95) / 0.45))           # FINAL (27) slips out and slides away, bottom right
        if u < 1:
            big_file(k, lerp(400, 640, u), lerp(770, 1080, u), 110, 74, "FINAL (27)", u * 4, 780, 22, register=False)
        sc = punch(14.95, 0.15)
        c.save(); c.translate(300, 185); c.scale(sc, sc); sfx(k, "THUNK!", 0, 0, 60, rot=-0.06); c.restore()
        qa("label", (300 - 100, 155, 300 + 100, 215), 60)
        flash(k, t, math.ceil(14.95 * 12) / 12)
        return
    lamp = 0.0 if 16.6 <= t < 19.05 else (0.35 if t >= 19.05 else 0.5 + 0.5 * (int(t * 6) % 2))
    gaze = (0, 0) if t < 16.4 else (-0.8, 0.1)
    head = wide_after(k, t, SQ, lamp, gaze=gaze)
    walk = clamp((t - 16.2) / 0.7)
    if walk > 0:                                     # MAX walks in from the left, beside the door
        pose, bob = anim.walk(t, speed=3, swing=22) if walk < 1 else ("stand", 0)
        mx = lerp(-90, MX, walk)
        look = (-1.0, -0.4) if 19.15 <= t < 19.7 else (0.8, 0.2)          # v06: eyes to the door, then back
        gx, gy = anim.gulp(t, [19.45], amt=0.1)
        c.save(); anim.squash(c, mx, MF, gx, gy)
        pm = person(k, "MAX", mx, MF + bob, MS, pose=pose, face="neutral", look=look, seed=33)
        c.restore()
        hx, hy = pm["head"]
        speech(k, t, "Got the\noriginal?", 112, 585, (hx + 6, hy - 60), T_MAX_LINE, 19.0, speaker=(hx, hy, MS), size=32)
    if ENDING == "B":
        speech(k, t, "Downloads.", RX, 760, (RX, head[1] + 40), T_B_LINE, 19.9, speaker=(*head, RS), size=38)


def b7_handover(k, t, tl):
    """RUSH grips the brim, tugs twice, and pops the hard hat out from under FINAL (28) (the sheet drops onto his
    hair); it hops onto MAX."""
    STATE["t"] = t
    c = k.c
    out = t >= 20.2
    office(k, door_open=1.0, hook=(False, False), pam=True)
    jig = 4 * math.sin((t - 20.0) * 2 * math.pi / 0.1) if 20.0 <= t < 20.2 else 0.0
    drop = ease(clamp((t - 20.2) / 0.1))
    hat_top = RF - (254 + 78) * RS * SQ
    caught = t >= 20.55
    u = ease(clamp((t - 20.2) / 0.35))

    def hat_xy():
        v = clamp((u - 0.4) / 0.6)
        return lerp(head[0], MX, u), lerp(head[1], MF - 266 * MS, v) - math.sin(v * math.pi) * 50

    def flying_hat():                                # slides out sideways (brim stays above his eyes), then hops onto MAX
        dk.helmet(k, *hat_xy(), lerp(RS, MS, u), lamp=0)

    sxq = 1 + (1 - SQ) * 0.45
    shx, shy = RX + 40 * RS * sxq, RF - 196 * RS * SQ
    gx = RX + 70 * RS * sxq                          # the brim's right end
    gy = RF - (254 + 26) * RS * SQ + (40 * ease(clamp((t - 20.2) / 0.1)) if out else 0)
    r = ease(clamp((t - 19.95) / 0.06))
    reach = 19.95 <= t < 20.3
    c.save(); c.translate(jig, 0)                    # the two yanks jiggle him and the sheet
    if reach:                                        # v08: the arm goes up behind his head, so his face hides it
        ex, ey = lerp(shx, RX + 95, r), lerp(shy, RF - 250, r)
        hx_, hy_ = lerp(shx, gx, r), lerp(shy, gy, r)
        for (ax, ay, bx, by) in ((shx, shy, ex, ey), (ex, ey, hx_, hy_)):
            ang = math.atan2(by - ay, bx - ax)
            nx, ny = -math.sin(ang) * 8.5, math.cos(ang) * 8.5
            cut(k, [(ax + nx, ay + ny), (bx + nx, by + ny), (bx - nx, by - ny), (ax - nx, ay - ny)],
                (0.93, 0.93, 0.95), shadow=False, lw=2)
    head, top = squashed_rush(k, t, SQ, 0.35, gaze=(-0.8, 0.1), face="hollow" if t < 20.2 else "shock",
                              helmet_on=not out)
    if out and not caught and u < 0.5:              # still under the sheet: drawn behind it
        flying_hat()
    lid(k, lerp(hat_top, top, drop) if out else top)
    if reach:                                        # only the hand shows, gripping the brim
        ellipse(k, lerp(shx, gx, r), lerp(shy, gy, r), 11, 11, kit.PEOPLE["RUSH"]["skin"], 822, shadow=False, lw=2)
        qa("cover", (gx - 12, gy - 12, gx + 12, gy + 12))
    c.restore()
    sq = 1.0
    if caught and t < 20.65:
        sq = 0.9
    c.save(); anim.squash(c, MX, MF, 2 - sq, sq)
    pm = person(k, "MAX", MX, MF, MS, pose="stand", face="neutral" if not caught else "shock",
                look=(0.8, 0.2), seed=33)
    if caught:
        dk.helmet(k, *pm["head"], MS, lamp=1.0)
        hx, hy = pm["head"]
        qa("cover", (hx - 70 * MS, hy - 32 * MS, hx + 70 * MS, hy - 20 * MS))
    c.restore()
    if out and not caught and u >= 0.5:
        flying_hat()
    if ENDING == "B":                                # the line runs to 20.08
        speech(k, t, "Downloads.", RX, 760, (RX, head[1] + 40), T_B_LINE, 20.1, speaker=(*head, RS), size=38)


def b8_door(k, t, tl):
    """MAX turns and walks into DOWNLOADS; the door snaps shut behind him."""
    STATE["t"] = t
    c = k.c
    office(k, door_open=1.0, hook=(False, False), pam=True)
    x, y, w, h = DOOR
    u = ease(clamp((t - 20.8) / 0.7))
    if t < 21.6:
        sc = lerp(MS, 0.62, u)
        mx, mf = lerp(MX, x + w / 2, u), lerp(MF, y + h - 2, u)
        pose, bob = anim.walk(t, speed=3, swing=18) if 0 < u < 1 else ("stand", 0)
        c.save()
        if u > 0.5:                                  # inside the doorway: the frame hides his edges
            c.rectangle(x, 0, w, y + h); c.clip()
        pm = person(k, "MAX", mx, mf + bob, sc, pose=pose, face="neutral", look=(-1, -0.2), seed=33, register=u < 0.5)
        dk.helmet(k, *pm["head"], sc, lamp=1.0)
        c.restore()
    door_slab(k, ease(clamp((t - 21.6) / 0.1)))
    squashed_rush(k, t, SQ, 0.0, gaze=(-0.8, 0.1), face="hollow", helmet_on=False)
    lid(k, RF - 254 * RS * SQ - 50 * RS * SQ)


def b9_exterior(k, t, tl):
    """Pull back through the wall to the UptimeZ tower; it shakes; a window spits out a page at the camera."""
    STATE["t"] = t
    c = k.c
    z = lerp(6.0, 1.0, ease(clamp((RAW_T - 21.9) / 0.35)))
    shake_amt = clamp((t - 22.3) / 0.1) * (1 - clamp((t - 22.6) / 0.15))
    c.save()
    anim.camera(c, 272, 381, z, dx=0, dy=0)
    wx, wy = tower(k, t, shake_amt, open_win=1.0 if t >= 22.5 else 0.0)
    c.restore()
    if z > 1.0:
        QA.clear()
    elif TAG and t >= 22.2:                          # promptanatomy.app card, only in the TAG=1 version
        a = ease(clamp((t - 22.2) / 0.15))
        c.save(); c.translate(270, 778); c.scale(max(0.02, a), max(0.02, a)); c.translate(-270, -778)
        rect(k, 125, 744, 290, 68, (1, 1, 1), 1297, lw=2)
        c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        for txt, yy, sz, col in (("Name the exact file.", 773, 22, INK), ("promptanatomy.app", 801, 20, brand.NAVY)):
            c.set_font_size(sz); e = c.text_extents(txt)
            c.move_to(270 - e.width / 2 - e.x_bearing, yy); c.set_source_rgb(*col); c.show_text(txt)
        c.restore()
        qa("label", (125, 744, 415, 812), 20)
    if t >= 22.5:                                    # FINAL (29) flies at the camera, like the pages at frame 0
        u = ease(clamp((t - 22.5) / 0.5))
        px, py = lerp(wx, 430, u), lerp(wy, 640, u) - math.sin(u * math.pi) * 120
        w_, h_ = lerp(20, 150, u), lerp(25, 110, u)
        big_file(k, px, py, w_, h_, "FINAL (29)", u * 0.4 - 0.2, 1299, max(2, lerp(3, 26, u)), register=u > 0.95)
    if 22.3 <= t < 22.65:                            # in the sky above the roof, not on the facade
        sfx(k, "RUMBLE", 270, 128, 50, rot=0.05)
        qa("label", (160, 103, 380, 153), 50)


PANELS = [(0.0, 3.0, b1_question), (3.0, 5.0, b2_gear), (5.0, 8.0, b3_kevin), (8.0, 10.5, b4_pull),
          (10.5, 13.5, b5_beard), (13.5, 19.9, b6_save), (19.9, 20.7, b7_handover), (20.7, 21.9, b8_door),
          (21.9, 23.0, b9_exterior)]


def overlay(k, t, tl, name):
    pass                     # bubbles and tags are drawn inside the beats, so their layout is per shot


def shake(t):
    for t0, a in ((9.8, 6), (10.98, 8), (14.95, 12), (21.7, 5)):
        d = t - t0
        if 0 <= d < 0.35:
            return math.sin(d * 55) * a * (1 - d / 0.35)
    return 0
