"""Sets for "Office Noir", v2 (on_set_v1.py = v1, kept). v2 after the review: the agency lettering bigger and
the frosted glass lighter; mom_shadow() gives Mom's wall shadow an oversized head with exaggerated curlers, the
#1 MOM mug at her hip and the pearl beads, so it is unmistakably her; key_light() is one large lit area on a face
(no extra lamp, reflected from the shot's source); sweat_drop() for 10B.
v1 notes: Sets for "Office Noir", v1 (all 540x960 plates, drawn in colour; the dream ones go through engine_on's accent
pass and then the light). Grill, 16 Nov: the office door's frosted glass reads DON - PRIVATE INVESTIGATIONS (his
dream rewrites the office into his agency; the lettering is drawn readable, not mirrored, so it reads in the first
second); rain only outside the window; the bedroom has a soft cream wallpaper with tiny mustard stars; the street
corner is a lit brick wall, a streetlamp and wet pavement.
Plates: office_back(k, t) (wall, window with rain, the door), pam_desk(k) (desk, monitor, the heart),
sofia_desk(k) (the lamp's desk), street(k, t), bedroom(k).
Light (drawn after the accent pass): blinds(c, ...) the slatted shadows, lamp_cone(c, ...), side_light (engine_on),
soft_glow(c, ...) for Pam, rain(c, ...) streaks on glass (moves with t)."""
import math
import random
import cairo
import kit
import props_on as pr
import don_on as d
from kit import INK, cut, rect, ellipse

WALL_N = (0.42, 0.40, 0.38)
WAINSCOT = (0.30, 0.26, 0.22)
WOOD = (0.36, 0.28, 0.20)
FROST = (0.93, 0.94, 0.93)          # v2: lighter (v1 0.82, 0.84, 0.84)
NIGHT = (0.12, 0.13, 0.15)
BRICK = (0.48, 0.34, 0.28)
MORTAR = (0.62, 0.58, 0.54)
PAVE = (0.22, 0.22, 0.24)
STAR = (0.88, 0.67, 0.17)
WALLPAPER = (0.97, 0.93, 0.82)
TYPE = "Special Elite"


def rain(c, x, y, w, h, t=0.0, seed=1, n=46):
    """Streaks running down a pane; t in seconds moves them."""
    r = random.Random(seed)
    c.save(); c.rectangle(x, y, w, h); c.clip()
    for i in range(n):
        sx = x + r.uniform(0, w)
        speed = r.uniform(160, 320)
        ln = r.uniform(18, 46)
        sy = y + ((r.uniform(0, h + ln) + t * speed) % (h + ln)) - ln
        c.set_source_rgba(0.85, 0.88, 0.92, r.uniform(0.25, 0.55)); c.set_line_width(r.uniform(1.2, 2.4))
        c.move_to(sx, sy); c.line_to(sx - 2, sy + ln); c.stroke()
    for i in range(24):                                           # beads on the glass
        bx, by = x + r.uniform(0, w), y + r.uniform(0, h)
        c.set_source_rgba(0.9, 0.92, 0.95, 0.45); c.arc(bx, by, r.uniform(1.5, 3.5), 0, 2 * math.pi); c.fill()
    c.restore()


def window(k, x, y, w, h, t=0.0):
    c = k.c
    rect(k, x - 10, y - 10, w + 20, h + 20, WOOD, 301, lw=2.4)
    g = cairo.LinearGradient(0, y, 0, y + h)
    g.add_color_stop_rgb(0, 0.20, 0.21, 0.24); g.add_color_stop_rgb(1, *NIGHT)
    c.set_source(g); c.rectangle(x, y, w, h); c.fill()
    rain(c, x, y, w, h, t)
    c.set_source_rgb(*WOOD); c.set_line_width(8)
    c.move_to(x + w / 2, y); c.line_to(x + w / 2, y + h); c.stroke()
    c.move_to(x, y + h / 2); c.line_to(x + w, y + h / 2); c.stroke()
    c.set_source_rgba(0.85, 0.85, 0.80, 0.85); c.set_line_width(3)               # half-drawn blinds at the top
    for i in range(7):
        c.move_to(x, y + 8 + i * 9); c.line_to(x + w, y + 8 + i * 9); c.stroke()


def door(k, x, y, w=150, h=380, seed=0):
    c = k.c
    rect(k, x, y, w, h, WOOD, 310 + seed, lw=2.4)
    rect(k, x + 16, y + 18, w - 32, h * 0.46, FROST, 311 + seed, shadow=False, lw=2)
    c.set_source_rgb(0.08, 0.08, 0.09)
    c.select_font_face(TYPE, 0, 0)
    c.set_font_size(44); te = c.text_extents("DON")
    c.move_to(x + w / 2 - te.x_advance / 2, y + 86); c.show_text("DON")
    for i, line in enumerate(("PRIVATE", "INVESTIGATIONS")):
        c.set_font_size(15.5); te = c.text_extents(line)
        sc_ = min(1.0, (w - 30) / te.x_advance)
        c.save(); c.translate(x + w / 2 - te.x_advance * sc_ / 2, y + 116 + i * 20); c.scale(sc_, 1)
        c.move_to(0, 0); c.show_text(line); c.restore()
    ellipse(k, x + w - 24, y + h * 0.58, 7, 7, (0.70, 0.68, 0.62), 312 + seed, shadow=False, lw=1.6)   # knob


def office_back(k, t=0.0, door_x=30, window_x=230):
    """The dream office: dark wall over wainscoting, the agency door, the rain window."""
    c = k.c
    c.set_source_rgb(*WALL_N); c.rectangle(0, 0, 540, 960); c.fill()
    rect(k, -10, 560, 560, 420, WAINSCOT, 300, shadow=False, lw=2)
    c.set_source_rgba(0, 0, 0, 0.25); c.set_line_width(2)
    for x in range(20, 540, 70):
        c.rectangle(x, 590, 54, 340); c.stroke()
    door(k, door_x, 180)
    window(k, window_x, 160, 260, 300, t)


def pam_desk(k, x=290, y=880, s=1.6, heart_on=True):
    """Pam's desk in front of the camera, her monitor and (frame 0) the heart on it."""
    c = k.c
    kit.cut(k, [(-20, y - 40), (560, y - 40), (560, 980), (-20, 980)], (0.40, 0.32, 0.25))
    pr.monitor(k, x, y - 30, s)
    hx, hy = x - 30 * s, y - 30 - 110 * s
    if heart_on:
        d.heart(c, hx, hy, 15 * s)
    return (hx, hy)


def sofia_desk(k):
    c = k.c
    c.set_source_rgb(0.10, 0.10, 0.11); c.rectangle(0, 0, 540, 960); c.fill()
    rect(k, -20, 880, 580, 200, (0.22, 0.18, 0.15), 703)


def lamp(k, x=90, y=200):
    c = k.c
    kit.cut(k, [(x - 60, y), (x + 60, y), (x + 40, y + 60), (x - 40, y + 60)], (0.30, 0.30, 0.32), shadow=False)
    c.set_source_rgb(0.30, 0.30, 0.32); c.set_line_width(10); c.move_to(x, y); c.line_to(x - 50, y - 50)
    c.line_to(x - 100, y - 50); c.stroke()


def lamp_pool(c, top=((50, 255), (130, 255)), bottom=((-60, 960), (600, 960))):
    """The lit cone under the desk lamp, drawn into the plate (light grey on the dark)."""
    c.save(); c.set_source_rgba(0.98, 0.95, 0.86, 0.55)
    c.move_to(*top[0]); c.line_to(*top[1]); c.line_to(*bottom[1]); c.line_to(*bottom[0]); c.close_path(); c.fill()
    c.restore()


def street(k, t=0.0):
    """A brick wall lit by a streetlamp, wet pavement with the lamp's reflection."""
    c = k.c
    c.set_source_rgb(*BRICK); c.rectangle(0, 0, 540, 760); c.fill()
    c.set_source_rgb(*MORTAR); c.set_line_width(2)
    for j in range(0, 760, 28):
        c.move_to(0, j); c.line_to(540, j); c.stroke()
        off = 30 if (j // 28) % 2 else 0
        for i in range(-60 + off, 560, 60):
            c.move_to(i, j); c.line_to(i, j + 28); c.stroke()
    c.set_source_rgb(*PAVE); c.rectangle(0, 760, 540, 200); c.fill()
    for i, (px, pw) in enumerate(((120, 160), (330, 120), (40, 80))):           # puddles with the lamp in them
        c.save(); c.translate(px + pw / 2, 850 + i * 30); c.scale(pw / 2, 12); c.arc(0, 0, 1, 0, 2 * math.pi)
        c.restore(); c.set_source_rgb(0.32, 0.33, 0.36); c.fill()
    c.set_source_rgba(0.95, 0.92, 0.80, 0.5); c.set_line_width(4)
    c.move_to(100, 830); c.line_to(100, 900); c.stroke()
    rect(k, 92, 40, 16, 740, (0.10, 0.10, 0.11), 320, shadow=False)                 # lamp post
    kit.cut(k, [(70, 60), (130, 60), (120, 100), (80, 100)], (0.10, 0.10, 0.11), shadow=False)


def bedroom(k, stars=True):
    """10A/10B: cream wallpaper with tiny mustard stars, the curtain yanked open, the bed seen from above."""
    import mom_on as mo
    c = k.c
    c.set_source_rgb(*WALLPAPER); c.rectangle(0, 0, 540, 960); c.fill()
    if stars:
        r = random.Random(9)
        for j in range(0, 600, 46):
            for i in range(0, 560, 46):
                sx, sy = i + (23 if (j // 46) % 2 else 0) + r.uniform(-3, 3), j + r.uniform(-3, 3)
                c.save(); c.translate(sx, sy); c.rotate(r.uniform(0, 1.2))
                c.move_to(0, -6)
                for n in range(1, 10):
                    a_ = -math.pi / 2 + n * math.pi / 5
                    rr = 6 if n % 2 == 0 else 2.6
                    c.line_to(math.cos(a_) * rr, math.sin(a_) * rr)
                c.close_path(); c.set_source_rgba(*STAR, 0.75); c.fill(); c.restore()
    for i in range(9):                                                         # warm light flooding in
        c.set_source_rgba(1.0, 0.95, 0.70, 0.08); c.move_to(-40, 0); c.line_to(120 + i * 40, 0)
        c.line_to(260 + i * 60, 960); c.line_to(-40, 960); c.close_path(); c.fill()
    rect(k, -10, -10, 90, 520, mo.MUSTARD, 801, shadow=False, lw=2)              # the curtain, yanked open
    c.set_source_rgb(*mo.MUSTARD_DARK); c.set_line_width(2)
    for x in (18, 40, 62):
        c.move_to(x, 0); c.line_to(x + 4, 500); c.stroke()
    rect(k, -20, 560, 600, 420, (0.70, 0.84, 0.94), 802)                         # the bed, from above
    rect(k, 30, 590, 250, 110, (0.98, 0.95, 0.88), 803)                          # pillow


# ---- light (after the accent pass) ------------------------------------------------------------------------------

def blinds(c, x, y, w, h, angle=-0.35, gap=26, band=12, amount=0.5):
    """The slatted shadow of venetian blinds thrown across a region (diagonal dark bands)."""
    c.save(); c.rectangle(x, y, w, h); c.clip()
    c.translate(x + w / 2, y + h / 2); c.rotate(angle)
    c.set_source_rgba(0, 0, 0, amount)
    span = int(max(w, h) * 1.6)
    for i in range(-span, span, gap):
        c.rectangle(-span, i, 2 * span, band)
    c.fill()
    c.restore()


def lamp_cone(c, top_l, top_r, bot_l, bot_r, amount=0.55):
    """Darken everything outside the lamp's cone."""
    c.save()
    c.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    c.rectangle(0, 0, 540, 960)
    c.move_to(*top_l); c.line_to(*top_r); c.line_to(*bot_r); c.line_to(*bot_l); c.close_path()
    c.set_source_rgba(0, 0, 0, amount); c.fill()
    c.restore()


def soft_glow(c, cx, cy, r, amount=0.28):
    g = cairo.RadialGradient(cx, cy, r * 0.1, cx, cy, r)
    g.add_color_stop_rgba(0, 1, 1, 1, amount); g.add_color_stop_rgba(1, 1, 1, 1, 0)
    c.save(); c.set_source(g); c.arc(cx, cy, r, 0, 2 * math.pi); c.fill(); c.restore()


def vignette(c, amount=0.5):
    g = cairo.RadialGradient(270, 480, 260, 270, 480, 700)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, amount)
    c.set_source(g); c.rectangle(0, 0, 540, 960); c.fill()



# ---- v2 ---------------------------------------------------------------------------------------------------------

def mom_shadow(k, x, feet, s, skew=-0.15, alpha=0.9, head=1.4):
    """Mom as a wall shadow that is unmistakably her: the figure with the mug at her hip, then her head again,
    `head` times bigger (the curlers and the bead chain read as a silhouette). Skewed away from the light."""
    import mom_on as mo
    sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)
    cc = cairo.Context(sf)
    kk = kit.Ctx(cc, 0)
    mo.mom(kk, 270, 900, 2.2, pose="hip_mug")
    cc.save(); cc.translate(270, 900); cc.scale(2.2, 2.2)
    cc.translate(0, mo.HY); cc.scale(head, head); cc.translate(0, -mo.HY + 8)
    mo._head(kk, "stern", (0, 0), None, 70, "front")
    top = mo.HY - 58                                       # the silhouette's signature: big curler bumps on the crown
    for (bx, by, r) in ((-46, top + 26, 15), (-24, top + 6, 16), (0, top - 2, 17), (24, top + 6, 16), (46, top + 26, 15)):
        cc.new_path(); cc.arc(bx, by, r, 0, 2 * math.pi); cc.set_source_rgb(0, 0, 0); cc.fill()
    cc.restore()
    c = k.c
    c.save()
    c.translate(x, feet); c.transform(cairo.Matrix(1, 0, skew, 1, 0, 0)); c.scale(s / 2.2, s / 2.2); c.translate(-270, -900)
    c.set_source_rgba(0.02, 0.02, 0.03, alpha); c.mask_surface(sf, 0, 0)
    c.restore()


def key_light(c, cx, cy, r, amount=0.32):
    """One large lit area on a face: the shot's own source, reflected; lifts the darkest tones around it."""
    g = cairo.RadialGradient(cx, cy, r * 0.15, cx, cy, r)
    g.add_color_stop_rgba(0, 1, 1, 1, amount); g.add_color_stop_rgba(0.6, 1, 1, 1, amount * 0.45)
    g.add_color_stop_rgba(1, 1, 1, 1, 0)
    c.save(); c.set_source(g); c.arc(cx, cy, r, 0, 2 * math.pi); c.fill(); c.restore()


def sweat_drop(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(0, -14); c.curve_to(8, -2, 10, 6, 0, 10); c.curve_to(-10, 6, -8, -2, 0, -14); c.close_path()
    c.set_source_rgb(0.78, 0.92, 1.0); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2); c.stroke()
    c.set_source_rgba(1, 1, 1, 0.9); c.arc(-3, 2, 2.4, 0, 2 * math.pi); c.fill()
    c.restore()
