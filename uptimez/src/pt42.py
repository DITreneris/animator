"""Prompt Telephone v04.2 - v04.1 plus UptimeZ Inc. branding and a professional-network post card.
B1 the post comes from the UptimeZ Inc. company page (full-screen card at the reveal)
B2 a wall sign with the lockup behind DON in frame 0
B3 a mini mark clipped to every name badge
B4 DON's framed portrait ("FOUNDER & CHIEF VISIONARY") behind his reaction
New module only: pt4.py, kit.py, brand.py and earlier versions are untouched (pt4.person is wrapped at runtime)."""
import math
import cairo
import kit
import pt4
import brand
from kit import W, H, INK, rect, ellipse, text, sfx, bubble, ease, clamp, lerp

MUTED = (0x59 / 255, 0x66 / 255, 0x7F / 255)
FEED = (0.93, 0.94, 0.95)


# ---------------------------------------------------------------- B3: mini mark on every badge
_orig_person = kit.person


def branded_person(k, name, x, feet, s=1.0, pose="stand", face="neutral", seed=1, look=(0, 0), seated=False, badge=True):
    out = _orig_person(k, name, x, feet, s, pose, face, seed, look, seated, badge)
    if badge:
        p = kit.PEOPLE[name]
        body_top = -300 * p["h"] + 78
        bx = (8 if p.get("tie") else -22)
        c = k.c
        c.save()
        c.translate(x, feet)
        c.scale(s, s)
        brand.mark(c, bx + 13, body_top + 22, 11, zzz=False)   # clipped above the badge
        c.restore()
    return out


pt4.person = branded_person  # runtime only: shots reused from pt4 now draw branded badges


# ---------------------------------------------------------------- B2: wall sign behind DON
def wall_sign(k, x, y, h):
    c = k.c
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    c.set_font_size(h * 0.42)
    wm = c.text_extents("UPTIMEZ INC.").x_advance
    rect(k, x - 12, y - 10, h * 1.22 + wm + 26, h + 20, (1, 1, 1), 870, lw=2)
    brand.lockup(c, x, y, h)


def s1_don(k, t, tl):
    pt4.accent_wall(k, "DON")
    wall_sign(k, 290, 450, 40)
    branded_person(k, "DON", 250, 1230, 1.9, pose="point_r", face="panic", seed=63, look=(0.3, 0))
    pt4.tile_bubble(k, ["BOLD!", "AUTHENTIC!", "VIRAL!"], 270, 112, (220, 560), 400)
    if 0.25 < tl < 0.75:
        sfx(k, "SLAM!", 420, 700, 60, rot=0.1, fill=(1, 1, 1))


# ---------------------------------------------------------------- B1: the post card
def post_card(k, tl):
    c = k.c
    c.set_source_rgb(*FEED)
    c.paint()
    grow = ease(clamp(tl / 0.25))
    c.save()
    c.translate(270, 480)
    c.scale(lerp(0.55, 1.0, grow), lerp(0.55, 1.0, grow))
    c.translate(-270, -480)
    rect(k, 22, 118, 496, 680, (1, 1, 1), 880, lw=2.2)
    # header: company page
    brand.mark(c, 40, 136, 56, zzz=False)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    c.set_font_size(22); c.set_source_rgb(*brand.NAVY); c.move_to(110, 158); c.show_text("UptimeZ Inc.")
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    c.set_font_size(14); c.set_source_rgb(*MUTED)
    c.move_to(110, 179); c.show_text("12,847 followers")
    c.move_to(110, 198); c.show_text("Promoted · 1m ·")
    c.arc(234, 193, 6, 0, 2 * math.pi); c.set_line_width(1.5); c.stroke()          # globe-ish
    c.move_to(228, 193); c.line_to(240, 193); c.stroke()
    c.set_font_size(22); c.move_to(470, 160); c.show_text("···")
    # caption in corporate-speak
    c.set_font_size(18); c.set_source_rgb(*brand.NAVY)
    c.move_to(40, 240); c.show_text("Thrilled to unveil our BOLD new")
    c.move_to(40, 264); c.show_text("direction.")
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    c.move_to(128, 264); c.show_text("#Leadership")
    # the image: DON's face and bald head, captioned BALD (always the biggest thing)
    pt4.don_portrait(k, 40, 284, 460, 300)
    rect(k, 40, 584, 460, 80, (1, 1, 1), 881, shadow=False, lw=1.5)
    text(k, "BALD", 270, 624, 70, INK)
    # reactions: count climbs once the post is live
    n = int(2431 * ease(clamp((tl - 0.4) / 1.2)))
    for i, col in enumerate(((0.25, 0.55, 0.85), (0.86, 0.3, 0.28), (0.95, 0.75, 0.15))):
        ellipse(k, 52 + i * 18, 694, 12, 12, col, 890 + i, shadow=False, lw=1.5)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    c.set_font_size(15); c.set_source_rgb(*MUTED)
    c.move_to(104, 700); c.show_text("Don and {:,} others".format(n) if n else "Don")
    c.set_source_rgb(0.85, 0.86, 0.88); c.set_line_width(1.5)
    c.move_to(36, 722); c.line_to(504, 722); c.stroke()
    # action bar
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    c.set_font_size(16); c.set_source_rgb(*MUTED)
    for lbl, x in (("Like", 46), ("Comment", 150), ("Repost", 290), ("Send", 420)):
        c.move_to(x, 762); c.show_text(lbl)
    c.restore()


def s4_post(k, t, tl):
    post_card(k, tl)


# ---------------------------------------------------------------- B4: DON's portrait behind his reaction
def portrait_frame(k, x, y, w, h):
    rect(k, x - 10, y - 10, w + 20, h + 20, (0.62, 0.48, 0.2), 900)       # gilt frame
    pt4.don_portrait(k, x, y, w, h)
    rect(k, x + 6, y + h + 16, w - 12, 26, (0.85, 0.72, 0.38), 901, lw=1.5)  # brass plate
    c = k.c
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    c.set_font_size(8.5); c.set_source_rgb(*INK)
    e = c.text_extents("FOUNDER & CHIEF VISIONARY")
    c.move_to(x + w / 2 - e.width / 2, y + h + 33); c.show_text("FOUNDER & CHIEF VISIONARY")


def s5_don(k, t, tl):
    pt4.accent_wall(k, "DON")
    portrait_frame(k, 360, 560, 130, 120)
    lean = ease(clamp(tl / 0.8))
    s = lerp(1.9, 2.25, lean)
    moved = tl > 0.6
    p = branded_person(k, "DON", 250, lerp(1230, 1350, lean), s, pose="heart" if moved else "stand",
                       face="happy" if moved else "shock", seed=65, look=(0, 0.4))
    hx, hy = p["head"]
    if moved:
        drop = clamp((tl - 0.9) / 1.6)
        ellipse(k, hx + 34 * s / 2, hy + 18 + drop * 60, 7, 10, (0.45, 0.8, 1.0), 560, shadow=False, lw=1.5)


PANELS = [(0.0, 2.0, s1_don), (2.0, 3.5, pt4.s2_pam), (3.5, 5.0, pt4.s3_rush), (5.0, 8.2, pt4.s4_laptop),
          (8.2, 11.0, s4_post), (11.0, 13.8, s5_don), (13.8, 15.0, pt4.s6_roll)]

LINES = [(11.3, 12.25, "...Finally.", 250, 470, 46), (12.3, 13.8, "A post about me.", 250, 470, 44)]


def overlay(k, t, tl, name):
    for (s, e, txt, ax, ay, size) in LINES:
        if s <= t < e:
            pop = 0.85 + 0.15 * ease(clamp((t - s) / 0.12))
            bubble(k, txt, ax, ay, size=size, pop=pop)


shake = pt4.shake
