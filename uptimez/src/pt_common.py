"""Prompt Telephone v03 - shared panels for variants A (BOLD) and B (BALD typo)."""
import math
from kit import (W, H, INK, PAPER, rect, ellipse, text, file_sheet, desk, monitor, sfx, bubble,
                 person, office_bg, ease, clamp, lerp, cut, rough_rect_pts, FONT)

TILE_H = 52


def tile(k, word, x, y, seed, rot=0.0, size=34):
    """One word of the order, as its own cutout tile (so it can fall out)."""
    c = k.c
    c.select_font_face(FONT)
    c.set_font_size(size)
    w = c.text_extents(word).width + 30
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    rect(k, -w / 2, -TILE_H / 2, w, TILE_H, (1, 1, 1), seed, lw=2.2)
    text(k, word, 0, 0, size, INK)
    c.restore()
    return w


def word_bubble(k, words, cx, top, tail_to, seed, gone=(), falling=None):
    """Bubble holding stacked word tiles. `gone` = words already dropped (slot closes).
    `falling` = (word, u, land_xy): that word animates from its slot to the floor."""
    shown = [w for w in words if w not in gone]
    n = len(shown)
    bh = 30 + n * (TILE_H + 10)
    bw = 300
    bx = cx - bw / 2
    tail = [(cx - 16, top + bh - 2), tail_to, (cx + 16, top + bh - 2)]
    cut(k, tail, (1, 1, 1))
    cut(k, rough_rect_pts(k, bx, top, bw, bh, seed, j=1.6), (1, 1, 1))
    k.c.move_to(*tail[0]); k.c.line_to(*tail[1]); k.c.line_to(*tail[2]); k.c.close_path()
    k.c.set_source_rgb(1, 1, 1); k.c.fill()
    slots = {}
    for i, w in enumerate(shown):
        y = top + 20 + TILE_H / 2 + i * (TILE_H + 10)
        slots[w] = (cx, y)
        if falling and falling[0] == w and falling[1] > 0:
            continue
        tile(k, w, cx, y, seed + 10 + i)
    if falling and falling[1] > 0:
        w, u, (lx, ly) = falling
        sx, sy = slots.get(w, (cx, top + 40))
        x = lerp(sx, lx, u) + math.sin(u * math.pi) * 40
        y = sy + (ly - sy) * u * u
        tile(k, w, x, y, seed + 30, rot=u * 0.9)


def floor_word(k, word, x, y, rot, seed):
    tile(k, word, x, y, seed, rot=rot, size=30)


def cat(k, x, y, seed=700):
    """CACHE, asleep: curled body, head, ears, tail."""
    ellipse(k, x, y, 46, 26, (0.1, 0.09, 0.1), seed)
    ellipse(k, x + 38, y - 10, 20, 18, (0.1, 0.09, 0.1), seed + 1)
    cut(k, [(x + 26, y - 22), (x + 30, y - 38), (x + 38, y - 24)], (0.1, 0.09, 0.1), shadow=False, lw=1.5)
    cut(k, [(x + 40, y - 24), (x + 50, y - 38), (x + 52, y - 20)], (0.1, 0.09, 0.1), shadow=False, lw=1.5)
    c = k.c
    c.set_source_rgb(0.85, 0.85, 0.6)
    c.set_line_width(2)
    for ex in (x + 32, x + 44):
        c.move_to(ex - 4, y - 10); c.line_to(ex + 4, y - 10); c.stroke()
    text(k, "z", x + 70, y - 46, 22, INK)


def laptop(k, x, y, w, seed, screen="face", typed="", post=None, enter=False):
    """Deadpan laptop. screen: 'face' | 'chat' | 'post'."""
    h = w * 0.62
    rect(k, x - 18, y + h, w + 36, 22, (0.55, 0.56, 0.6), seed)  # base
    rect(k, x, y, w, h, (0.18, 0.18, 0.21), seed + 1)              # lid
    sx, sy, sw, sh = x + 10, y + 10, w - 20, h - 20
    rect(k, sx, sy, sw, sh, (0.95, 0.97, 1.0), seed + 2, shadow=False, lw=1.5)
    c = k.c
    if screen in ("face", "chat"):
        # deadpan face: two dots and a flat line
        fy = sy + sh * (0.32 if screen == "chat" else 0.45)
        for dx in (-0.14, 0.14):
            ellipse(k, sx + sw / 2 + dx * sw, fy, 7, 7, INK, seed + 5 + int(dx * 100), shadow=False, outline=False)
        c.set_source_rgb(*INK); c.set_line_width(4)
        c.move_to(sx + sw / 2 - 22, fy + 26); c.line_to(sx + sw / 2 + 22, fy + 26); c.stroke()
    if screen == "chat":
        bx, by, bw, bh = sx + 14, sy + sh - 92, sw - 28, 76
        rect(k, bx, by, bw, bh, (1, 1, 1), seed + 8, shadow=False, lw=2)
        if typed:
            c.select_font_face(FONT); c.set_font_size(62)
            c.move_to(bx + 16, by + 62); c.set_source_rgb(*INK); c.show_text(typed)
        if enter:
            text(k, "↵", bx + bw - 26, by + bh / 2, 30, (0.2, 0.5, 0.9), font="DejaVu Sans")
    if screen == "post":
        post(k, sx, sy, sw, sh)


def don_head_photo(k, x, y, s, seed):
    """A photo of DON's bald head (for the B post)."""
    ellipse(k, x, y, 70 * s, 70 * s, (0.96, 0.78, 0.66), seed)
    c = k.c
    c.set_source_rgba(1, 1, 1, 0.6)
    c.save(); c.translate(x - 22 * s, y - 34 * s); c.rotate(-0.5); c.scale(1, 0.45)
    c.arc(0, 0, 20 * s, 0, 2 * math.pi); c.restore(); c.fill()
    rect(k, x - 76 * s, y - 4 * s, 14 * s, 30 * s, (0.55, 0.55, 0.55), seed + 1, shadow=False, lw=1.5)
    rect(k, x + 62 * s, y - 4 * s, 14 * s, 30 * s, (0.55, 0.55, 0.55), seed + 2, shadow=False, lw=1.5)


def post_bold(k, sx, sy, sw, sh):
    text(k, "BOLD", sx + sw / 2, sy + sh / 2 + 4, sw * 0.27, INK)


def post_bald(k, sx, sy, sw, sh):
    rect(k, sx + 18, sy + 12, sw - 36, sh - 78, (0.75, 0.86, 0.95), 880, shadow=False, lw=1.5)
    don_head_photo(k, sx + sw / 2, sy + 12 + (sh - 78) / 2 + 20, (sh - 78) / 170, 881)
    text(k, "BALD", sx + sw / 2, sy + sh - 36, 48, INK)


def build(variant):
    typed = "Bold." if variant == "A" else "Bald."
    post = post_bold if variant == "A" else post_bald

    def p1_order(k, t, tl):
        office_bg(k)
        slam = ease(clamp(tl / 0.25))
        person(k, "PAM", 410, 800, 1.0, pose="stand", face="shock", seed=46, look=(-1, -0.3))
        desk(k, 300, 640, 230, 24)
        file_sheet(k, lerp(260, 380, slam), lerp(520, 628, slam), 90, 60, "", 870, rot=0.2)
        person(k, "DON", 160, 860, 1.2, pose="point_r", face="panic", seed=60, look=(1, 0))
        word_bubble(k, ["BOLD!", "AUTHENTIC!", "VIRAL!"], 200, 118, (180, 430), 600)
        if 0.15 < tl < 0.6:
            sfx(k, "SLAM!", 400, 560, 54, rot=0.1, fill=(1, 1, 1))

    def p2_pam(k, t, tl):
        office_bg(k)
        person(k, "RUSH", 470, 820, 1.0, pose="stand", face="panic", seed=36, look=(-1, 0))
        person(k, "PAM", 200, 800, 1.15, pose="point_r", face="confused", seed=47, look=(1, 0))
        u = clamp((tl - 0.7) / 0.55)
        if u >= 1:
            word_bubble(k, ["BOLD!", "VIRAL!"], 210, 118, (200, 430), 610)
            floor_word(k, "AUTHENTIC!", 150, 900, 0.9, 611)
            if tl < 1.6:
                sfx(k, "CLUNK", 300, 830, 40, rot=-0.1, fill=(1, 1, 1))
        else:
            word_bubble(k, ["BOLD!", "AUTHENTIC!", "VIRAL!"], 210, 118, (200, 430), 610,
                        falling=("AUTHENTIC!", u, (150, 900)))

    def p3_rush(k, t, tl):
        office_bg(k)
        person(k, "RUSH", 170, 800, 1.15, pose="panic", face="panic", seed=37, look=(1, 0.3))
        desk(k, 250, 660, 280, 24)
        laptop(k, 330, 540, 160, 650, screen="face")
        u = clamp((tl - 0.6) / 0.55)
        if u >= 1:
            word_bubble(k, ["BOLD"], 210, 118, (180, 400), 620)
            floor_word(k, "VIRAL!", 330, 905, -0.6, 621)
            if tl < 1.5:
                sfx(k, "CLUNK", 420, 830, 40, rot=0.1, fill=(1, 1, 1))
        else:
            word_bubble(k, ["BOLD", "VIRAL"], 210, 118, (180, 400), 620,
                        falling=("VIRAL", u, (330, 905)))

    def p4_type(k, t, tl):
        office_bg(k)
        n = int(clamp(tl / 0.45) * len(typed) + 0.999)   # typed by 7.45 s, readable for 1 s
        laptop(k, 50, 300, 440, 660, screen="chat", typed=typed[:n], enter=tl > 1.1)
        # RUSH's hands on the keys
        for hx in (180 + (int(tl * 12) % 2) * 10, 340 - (int(tl * 12) % 2) * 10):
            ellipse(k, hx, 600, 26, 20, (0.62, 0.42, 0.26), 671 + hx)

    def p5_reveal(k, t, tl):
        office_bg(k)
        laptop(k, 50, 300, 440, 660, screen="post" if tl > 0.1 else "chat", typed=typed, post=post)
        if tl > 0.1 and tl < 0.5:
            sfx(k, "POP", 420, 250, 44, rot=0.1, fill=(1, 1, 1))

    def p6_freeze(k, t, tl):
        office_bg(k)
        floor_word(k, "VIRAL!", 380, 905, -0.6, 621)
        floor_word(k, "AUTHENTIC!", 120, 900, 0.3, 611)
        cat(k, 110, 870)
        person(k, "PAM", 70, 790, 0.85, pose="stand", face="shock", seed=48, look=(1, 0))
        person(k, "RUSH", 470, 790, 0.85, pose="shock", face="panic", seed=38, look=(-1, 0))
        desk(k, 170, 640, 230, 24)
        laptop(k, 210, 520, 150, 690, screen="post", post=post)
        person(k, "DON", 260, 900, 1.05, pose="stand", face="shock", seed=61, look=(0, 1))

    def p7_genius(k, t, tl):
        office_bg(k)
        face = "shock" if tl < 0.25 else "pleased"
        person(k, "DON", 270, 1180, 2.0, pose="pleased" if tl > 0.25 else "stand", face=face, seed=62)

    panels = [(0.0, 2.5, p1_order), (2.5, 4.5, p2_pam), (4.5, 7.0, p3_rush), (7.0, 8.5, p4_type),
              (8.5, 10.5, p5_reveal), (10.5, 12.0, p6_freeze), (12.0, 15.0, p7_genius)]

    lines = [(12.3, 13.45, "...Finally.", 270, 430, 44), (13.45, 15.0, "Something I understand.", 270, 430, 32)]

    def overlay(k, t, tl, name):
        for (s, e, txt, ax, ay, size) in lines:
            if s <= t < e:
                pop = 0.85 + 0.15 * ease(clamp((t - s) / 0.12))
                bubble(k, txt, ax, ay, size=size, pop=pop)

    def shake(t):
        d = t - 0.25
        return math.sin(d * 60) * 8 * (1 - d / 0.25) if 0 <= d < 0.25 else 0

    return panels, overlay, shake
