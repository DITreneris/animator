"""Prompt Telephone v04.1 - 6 shots, 15 s.
DON order -> PAM strikes AUTHENTIC -> RUSH sprays VIRAL -> one laptop shot (Bald. / Did you mean: Bold? / NO / BALD portrait)
-> DON: "Finally. A post about me." -> laptop eye-roll.
New module only: kit.py, pt_common.py and every earlier version are untouched."""
import math
import kit
from kit import (W, H, INK, rect, ellipse, text, file_sheet, desk, sfx, bubble, person, office_bg,
                 ease, clamp, lerp, cut, rough_rect_pts, FONT)

kit.ARM_POSES.setdefault("heart", (-8, 0, 30, -150))    # right hand on chest (runtime-only addition)
kit.ARM_POSES.setdefault("spray", (-8, 0, 120, -30))     # right arm out holding a bottle

ACCENT = {"DON": (0.86, 0.30, 0.28), "PAM": (0.60, 0.47, 0.78), "RUSH": (0.30, 0.66, 0.66)}
TILE_H = 74


def accent_wall(k, who):
    """Same office, plus one accent-coloured wall panel behind the character."""
    office_bg(k)
    rect(k, 70, 70, 400, 600, ACCENT[who], 300 + len(who), shadow=False, lw=2)


def big_tile(k, word, x, y, seed, rot=0.0, size=52, strike=0.0, mist=0.0):
    c = k.c
    c.select_font_face(FONT)
    c.set_font_size(size)
    w = c.text_extents(word).width + 36
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    rect(k, -w / 2, -TILE_H / 2, w, TILE_H, (1, 1, 1), seed, lw=2.4)
    text(k, word, 0, 0, size, INK)
    if strike > 0:  # red marker line drawn progressively
        c.set_source_rgb(0.85, 0.1, 0.1)
        c.set_line_width(9)
        c.set_line_cap(1)
        x0 = -w / 2 + 6
        c.move_to(x0, 6)
        c.line_to(x0 + (w - 12) * strike, -4 + 8 * math.sin(strike * 9))
        c.stroke()
    if mist > 0:  # sanitiser mist puffs over the tile
        for i in range(7):
            a = i / 7 * 2 * math.pi
            r = 24 + 26 * mist
            c.arc(math.cos(a) * r * 1.6, math.sin(a) * r * 0.6, 14 + 10 * mist, 0, 2 * math.pi)
            c.set_source_rgba(0.85, 0.95, 1.0, 0.75 * (1 - mist * 0.5))
            c.fill()
    c.restore()
    return w


def tile_bubble(k, words, cx, top, tail_to, seed, hide=(), extra=None):
    """Bubble with stacked big tiles. `hide` = words not drawn in their slot.
    `extra(k, slots)` draws animated tiles on top. Returns slot centres."""
    n = len(words)
    bh = 26 + n * (TILE_H + 12)
    bw = 410
    bx = max(24, min(cx - bw / 2, 470 - bw))
    tail = [(bx + bw / 2 - 18, top + bh - 2), tail_to, (bx + bw / 2 + 18, top + bh - 2)]
    cut(k, tail, (1, 1, 1))
    cut(k, rough_rect_pts(k, bx, top, bw, bh, seed, j=1.6), (1, 1, 1))
    k.c.move_to(*tail[0]); k.c.line_to(*tail[1]); k.c.line_to(*tail[2]); k.c.close_path()
    k.c.set_source_rgb(1, 1, 1); k.c.fill()
    slots = {}
    for i, w in enumerate(words):
        y = top + 18 + TILE_H / 2 + i * (TILE_H + 12)
        slots[w] = (bx + bw / 2, y)
        if w not in hide:
            big_tile(k, w, bx + bw / 2, y, seed + 10 + i)
    if extra:
        extra(k, slots)
    return slots


def fall(u, sx, sy, lx, ly, side=1):
    return lerp(sx, lx, u) + side * math.sin(u * math.pi) * 50, sy + (ly - sy) * u * u


# ---------------------------------------------------------------- shot 1: DON's order
def s1_don(k, t, tl):
    accent_wall(k, "DON")
    person(k, "DON", 250, 1230, 1.9, pose="point_r", face="panic", seed=63, look=(0.3, 0))
    tile_bubble(k, ["BOLD!", "AUTHENTIC!", "VIRAL!"], 270, 112, (220, 560), 400)
    if 0.25 < tl < 0.75:
        sfx(k, "SLAM!", 420, 700, 60, rot=0.1, fill=(1, 1, 1))


# ---------------------------------------------------------------- shot 2: PAM strikes AUTHENTIC
def s2_pam(k, t, tl):
    accent_wall(k, "PAM")
    person(k, "PAM", 250, 1230, 1.85, pose="point_r", face="smug", seed=49, look=(0.6, -0.8))
    strike = ease(clamp((tl - 0.15) / 0.4))
    u = clamp((tl - 0.75) / 0.45)

    def extra(k, slots):
        sx, sy = slots["AUTHENTIC!"]
        if u <= 0:
            big_tile(k, "AUTHENTIC!", sx, sy, 412, strike=strike)
        else:
            x, y = fall(u, sx, sy, 120, 900, side=-1)
            big_tile(k, "AUTHENTIC!", x, y, 412, rot=-u * 1.1, strike=1.0)

    tile_bubble(k, ["BOLD!", "AUTHENTIC!", "VIRAL!"], 270, 112, (230, 560), 410, hide=("AUTHENTIC!",), extra=extra)
    if strike > 0 and u <= 0:  # the marker
        k.c.save(); k.c.translate(lerp(110, 400, strike), 236); k.c.rotate(0.6)
        rect(k, -9, -60, 18, 70, (0.85, 0.1, 0.1), 430, lw=2); k.c.restore()
    if u >= 1 and tl < 1.45:
        sfx(k, "CLUNK", 300, 860, 44, rot=-0.1, fill=(1, 1, 1))


# ---------------------------------------------------------------- shot 3: RUSH sprays VIRAL
def s3_rush(k, t, tl):
    accent_wall(k, "RUSH")
    recoil = tl > 0.45
    p = person(k, "RUSH", 230 if not recoil else 210, 1230, 1.85, pose="spray",
               face="panic" if recoil else "shock", seed=39, look=(0.7, -0.8))
    mist = clamp((tl - 0.15) / 0.35) if tl < 0.75 else 0.0
    push = clamp((tl - 0.75) / 0.45)

    def extra(k, slots):
        sx, sy = slots["VIRAL"]
        if push <= 0:
            big_tile(k, "VIRAL", sx, sy, 422, mist=mist)
        else:
            x, y = fall(push, sx, sy, 470, 900)
            big_tile(k, "VIRAL", x, y, 422, rot=push * 1.2)

    tile_bubble(k, ["BOLD", "VIRAL"], 270, 112, (220, 560), 420, hide=("VIRAL",), extra=extra)
    # sanitiser bottle in the right hand
    hx, hy = p["hands"][1]
    rect(k, hx - 14, hy - 50, 28, 56, (0.92, 0.97, 1.0), 440, lw=2)
    rect(k, hx - 6, hy - 64, 12, 16, (0.3, 0.66, 0.66), 441, lw=2)
    text(k, "+", hx, hy - 22, 26, (0.3, 0.66, 0.66))
    if 0.15 < tl < 0.6:
        sfx(k, "PSSHT", 330, 470, 42, rot=-0.08, fill=(1, 1, 1))
    if push >= 1:
        sfx(k, "CLUNK", 360, 860, 40, rot=0.1, fill=(1, 1, 1))


# ---------------------------------------------------------------- shot 4: one continuous laptop shot
LX, LY, LW = 25, 250, 490
LH = LW * 0.64
SX, SY, SW, SH = LX + 12, LY + 12, LW - 24, LH - 24


def laptop_frame(k):
    rect(k, LX - 18, LY + LH, LW + 36, 26, (0.55, 0.56, 0.6), 500)
    rect(k, LX, LY, LW, LH, (0.18, 0.18, 0.21), 501)
    rect(k, SX, SY, SW, SH, (0.95, 0.97, 1.0), 502, shadow=False, lw=1.5)


def laptop_face(k, cx, cy, look=(0.0, 0.0), roll=0.0, scale=1.0):
    """Deadpan face: two dots + a flat line. roll 0..1 sends the pupils up and around (eye-roll)."""
    for dx in (-48, 48):
        ex = cx + dx * scale
        if roll > 0:
            a = -math.pi / 2 - roll * math.pi * 0.9
            ox, oy = math.cos(a) * 14 * scale, math.sin(a) * 14 * scale
            ellipse(k, ex, cy, 22 * scale, 22 * scale, (1, 1, 1), 510 + dx, shadow=False, lw=2.5)
            ellipse(k, ex + ox, cy + oy, 8 * scale, 8 * scale, INK, 511 + dx, shadow=False, outline=False)
        else:
            ellipse(k, ex + look[0] * 10 * scale, cy + look[1] * 8 * scale, 9 * scale, 9 * scale, INK, 512 + dx,
                    shadow=False, outline=False)
    c = k.c
    c.set_source_rgb(*INK)
    c.set_line_width(5 * scale)
    c.move_to(cx - 30 * scale, cy + 40 * scale)
    c.line_to(cx + 30 * scale, cy + 40 * scale)
    c.stroke()


def don_portrait(k, x0, y0, w, h):
    """DON's own head and shoulders (same drawing as the character), clipped into a photo."""
    c = k.c
    rect(k, x0, y0, w, h, (0.72, 0.85, 0.95), 520, shadow=False, lw=1.5)
    c.save()
    c.rectangle(x0, y0, w, h)
    c.clip()
    sc = h / 200 * 1.85
    person(k, "DON", x0 + w / 2, y0 + h * 0.52 + 302 * sc, sc, pose="stand", face="smug", seed=64, badge=False)
    c.restore()


def s4_laptop(k, t, tl):
    office_bg(k)
    laptop_frame(k)
    T = 5.0 + tl
    c = k.c
    if T < 8.2:
        laptop_face(k, SX + SW / 2, SY + 70, look=(0, 0.6))
        # chat box with the typo
        bx, by, bw, bh = SX + 16, SY + SH - 96, SW - 32, 80
        rect(k, bx, by, bw, bh, (1, 1, 1), 530, shadow=False, lw=2)
        typed = "Bald."
        n = int(clamp((T - 5.0) / 0.45) * len(typed) + 0.999)
        c.select_font_face(FONT); c.set_font_size(64)
        c.move_to(bx + 18, by + 64); c.set_source_rgb(*INK); c.show_text(typed[:n])
        if T < 5.5:  # RUSH's hands typing
            for hx in (170 + (int(T * 12) % 2) * 10, 350 - (int(T * 12) % 2) * 10):
                ellipse(k, hx, LY + LH + 40, 28, 22, (0.62, 0.42, 0.26), 540 + hx)
        if T >= 6.5:  # "Did you mean: Bold?"
            dx, dy, dw, dh = SX + 30, SY + 30, SW - 60, 180
            rect(k, dx, dy, dw, dh, (1, 1, 1), 550, lw=2.5)
            text(k, "Did you mean:", dx + dw / 2, dy + 38, 34, INK)
            text(k, "Bold?", dx + dw / 2, dy + 82, 46, INK)
            pressed = T >= 7.6
            rect(k, dx + 30, dy + 118, 150, 50, (0.25, 0.7, 0.35), 551, lw=2)
            text(k, "Yes", dx + 105, dy + 143, 30, (1, 1, 1))
            nc = (0.75, 0.1, 0.1) if pressed else (0.55, 0.55, 0.58)
            rect(k, dx + dw - 180, dy + 118 + (4 if pressed else 0), 150, 50, nc, 552, lw=2)
            text(k, "NO", dx + dw - 105, dy + 143 + (4 if pressed else 0), 30, (1, 1, 1))
            # RUSH's arm: approaches from the lower right, stabs the right edge of NO, then pulls back
            fu = ease(clamp((T - 7.0) / 0.6)) * (1 - ease(clamp((T - 7.85) / 0.25)))
            fx, fy = lerp(600, dx + dw - 46, fu), lerp(LY + LH + 160, dy + 158, fu)
            ang = math.atan2(fy - (fy + 300), (fx + 140) - fx)
            k.c.save(); k.c.translate(fx, fy); k.c.rotate(-0.45)
            rect(k, -16, 18, 34, 320, (0.93, 0.93, 0.95), 553, lw=2)   # RUSH's white sleeve
            ellipse(k, 0, 8, 17, 20, (0.62, 0.42, 0.26), 554, shadow=False, lw=2)
            k.c.restore()
            if pressed and T < 8.1:
                sfx(k, "THUD!", 380, 170, 60, rot=0.1)
    else:
        # the post: DON's face and bald head, captioned BALD
        don_portrait(k, SX + 20, SY + 14, SW - 40, SH - 92)
        text(k, "BALD", SX + SW / 2, SY + SH - 40, 58, INK)
        if T < 8.6:
            sfx(k, "POP", 440, 200, 48, rot=0.1, fill=(1, 1, 1))


# ---------------------------------------------------------------- shot 5: DON's reaction
def s5_don(k, t, tl):
    accent_wall(k, "DON")
    lean = ease(clamp(tl / 0.8))
    s = lerp(1.9, 2.25, lean)
    moved = tl > 0.6
    p = person(k, "DON", 270, lerp(1230, 1350, lean), s, pose="heart" if moved else "stand",
               face="happy" if moved else "shock", seed=65, look=(0, 0.4))
    hx, hy = p["head"]
    if moved:  # a single tear
        drop = clamp((tl - 0.9) / 1.6)
        ellipse(k, hx + 34 * s / 2, hy + 18 + drop * 60, 7, 10, (0.45, 0.8, 1.0), 560, shadow=False, lw=1.5)


# ---------------------------------------------------------------- shot 6: the eye-roll
def s6_roll(k, t, tl):
    office_bg(k)
    laptop_frame(k)
    look = (-1.0, -0.2) if tl < 0.45 else (0, 0)
    roll = clamp((tl - 0.45) / 0.5)
    laptop_face(k, SX + SW / 2, SY + SH / 2 - 20, look=look, roll=roll, scale=1.6)


PANELS = [(0.0, 2.0, s1_don), (2.0, 3.5, s2_pam), (3.5, 5.0, s3_rush), (5.0, 10.5, s4_laptop),
          (10.5, 13.8, s5_don), (13.8, 15.0, s6_roll)]

LINES = [(10.9, 11.95, "...Finally.", 270, 470, 46), (12.0, 13.8, "A post about me.", 270, 470, 44)]


def overlay(k, t, tl, name):
    for (s, e, txt, ax, ay, size) in LINES:
        if s <= t < e:
            pop = 0.85 + 0.15 * ease(clamp((t - s) / 0.12))
            bubble(k, txt, ax, ay, size=size, pop=pop)


def shake(t):
    for t0, amp in ((0.3, 9), (7.6, 7)):
        d = t - t0
        if 0 <= d < 0.25:
            return math.sin(d * 60) * amp * (1 - d / 0.25)
    return 0
