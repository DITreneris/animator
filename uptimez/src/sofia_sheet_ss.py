"""v2 (v1 pinned in sofia_sheet_ss_v1.py). SOFIA model sheet for "Secret Santa" (sofia_ss.py). Writes sofia_sheet_ss_v1.png at 2400x1560 (drawn at
1200x780, 2x): the look, the earrings of the episode, faces and poses by shot, the frame-0 / loop close-up (Pam's
hand uncapping the lipstick, Sofia soft behind it with the sparkle) and a phone-size check.
v2 (review): OLD / FINAL labels, black lacquer cap + bigger lift + lighter blur on frame 0, and a row of
camera crops on the existing drawings (compact push-in, knowing, eyebrow) with the eyebrow timing. Writes
sofia_sheet_ss_v2.png at 2400x2000, plus ss_frame0_phone_v2.png (frame 0 at true 540x960)."""
import sys
import math
import cairo
import kit
import brand
import sofia_mf as sm
import sofia_ss as ss
import pam_mf as pm
import don_v4 as dv
import props_ss as props
from kit import Ctx, INK
from charsheets import corp
from sofia_sheet_mf import boxed, flush, HY

W2, H2 = 1200, 1000
GREY = (0.35, 0.40, 0.50)
ACCENT = (0.99, 0.95, 0.90)
ROSE_BG = (1.0, 0.95, 0.95)


def head_at(k, cx, cy, s, kind, look=(0, 0), lag=(0, 0), mouth=None, sparkle=0.0):
    ss.sofia(k, cx, cy - HY * s, s, "stand", kind, look=look, lag=lag, badge=False, mouth=mouth, sparkle=sparkle)


def pam_hand_lipstick(k, x, y, s, uncap, cap_col=props.CAP_BLACK, lift_max=40):
    """Pam's hand from below (purple cuff), holding the lipstick up, uncapping it with the other thumb."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    kit.cut(k, [(-22, 90), (22, 90), (18, 30), (-18, 30)], pm.PURPLE, shadow=False, lw=2)      # the sleeve
    kit.ellipse(k, 0, 18, 19, 22, pm.SKIN, 3, shadow=False, lw=2)                             # the fist
    c.set_source_rgb(*INK); c.set_line_width(1.6)
    for d in (-8, 0, 8):
        c.move_to(-16, 10 + d * 0.6 + 8); c.line_to(-4, 10 + d * 0.6 + 8); c.stroke()
    props.lipstick(k, 2, 4, 1.25, 0.0, uncap, seed=5, cap_col=cap_col, lift_max=lift_max)
    c.restore()


def frame0(k, x, y, w, h, uncap, spark, label, blur=1.5, pop=False):
    c = k.c
    c.save(); c.rectangle(x, y, w, h); c.clip()
    c.set_source_rgb(*kit.WALL); c.rectangle(x, y, w, h); c.fill()

    def bg(lc):
        k2 = Ctx(lc, 0)
        ss.sofia(k2, x + w * 0.40, y + h * 0.34 - HY * 1.0, 1.0, "stand", "neutral", look=(-0.6, 0.1), lag=(3, 0),
                 badge=False, sparkle=spark)
    props.soft(c, bg, blur)
    pam_hand_lipstick(k, x + w * 0.24, y + h * 0.74, 1.0, uncap)
    if pop:
        corp(c, "pop!", x + w * 0.04, y + h * 0.50, 10, col=brand.NAVY, bold=True)
    c.restore()
    c.set_source_rgb(*INK); c.set_line_width(1.2); c.rectangle(x, y, w, h); c.stroke()
    corp(c, label, x, y + h + 12, 8.5, col=GREY, bold=True)


def crop(x, y, w, h, label, draw, fill=None):
    c = k.c
    c.save(); c.rectangle(x, y, w, h); c.clip()
    c.set_source_rgb(*(fill or kit.WALL)); c.rectangle(x, y, w, h); c.fill()
    draw()
    c.restore()
    c.set_source_rgb(*INK); c.set_line_width(1.2); c.rectangle(x, y, w, h); c.stroke()
    corp(c, label, x, y + h + 12, 8.5, col=GREY, bold=True)


def compact_push(x, y, w, h):
    def d():
        ss.sofia(k, x + w * CP[0], y + h * CP[1], CP[2], "compact", "knowing", look=(-0.8, 0.1), compact_open=1.0,
                 sparkle=0.0, seed=96)
        pm.pam(k, x + w * CP[3], y + h * CP[4], CP[5], "stand", "hopeful", look=(0.8, -0.2), seed=95)
    crop(x, y, w, h, "2: push-in, the compact", d)


CP = (0.84, 0.92, 0.48, 0.16, 1.75, 0.62)
FACE = 0.85


def camera_row(c):
    y0 = 796
    corp(c, "v2 · CAMERA ON THE EXISTING DRAWINGS  (9:16, no new art)", 24, y0 - 6, 10, bold=True)
    W, H = 100, 178
    frame0(k, 24, y0, W, H, 0.0, 0.0, "1: frame 0, cap on")
    frame0(k, 132, y0, W, H, 0.75, 1.0, "1: +0.5 s, pop + glint", pop=True)
    compact_push(240, y0, W, H)
    crop(348, y0, W, H, "2: knowing, ~125%",
         lambda: head_at(k, 348 + W * 0.52, y0 + H * 0.42, FACE, "knowing", look=(-0.7, 0.1)))
    crop(456, y0, W, H, "7: eyebrow, ~125%",
         lambda: head_at(k, 456 + W * 0.48, y0 + H * 0.42, FACE, "eyebrow", look=(0.8, 0.0)))
    # 7: the timing strip
    x0, ty = 580, y0 + 8
    corp(c, "7 · SHE REACTS TO WHAT DON SAYS", x0, ty, 10, bold=True)
    segs = [(0.00, 0.12, "eyes", (0.55, 0.62, 0.75)), (0.12, 0.52, "HOLD the eyebrow 0.4 s", (0.72, 0.12, 0.16)),
            (0.52, 0.80, "head turns", (0.55, 0.62, 0.75))]
    sx = 520
    for a, b, lab, col in segs:
        c.set_source_rgb(*col); c.rectangle(x0 + a * sx, ty + 14, (b - a) * sx - 2, 22); c.fill()
        corp(c, lab, x0 + a * sx + 4, ty + 29, 8.5, col=(1, 1, 1), bold=True)
    for t in (0.0, 0.12, 0.52, 0.80):
        corp(c, "%.2f s" % t, x0 + t * sx, ty + 48, 8, col=GREY)
    rules = ["Eyes first, head 3 frames later: the judgement lands before she moves.",
             "Earrings: one pendulum sway (4–6 frames) on each head turn, ONE glint on shot 1's turn.",
             "The loop's 'soft sparkle' = that same single glint, not a constant twinkle.",
             "Compact: no extra insert shot; push into the hand and Pam's face inside shot 2.",
             "Frame 0: lipstick sharp, Sofía blur 1.5 (was 2.2), black cap lifts 40 (was 26), 'pop' SFX."]
    for i, r in enumerate(rules):
        corp(c, "·  " + r, x0, ty + 76 + i * 20, 10, col=INK)


def phone_test(out):
    """Frame 0 and +0.5 s at true phone size, 540x960 each, side by side."""
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1080, 960)
    c = cairo.Context(surf)
    global k
    k = Ctx(c, 0)
    for i, (u, sp, pop) in enumerate(((0.0, 0.0, False), (0.75, 1.0, True))):
        c.save(); c.translate(540 * i, 0); c.scale(540 / 100.0, 540 / 100.0)
        frame0(k, 0, 0, 100, 960 / 5.4, u, sp, "", pop=pop)
        c.restore()
    surf.write_to_png(out)


def main(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    global k
    k = Ctx(c, 0)
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "SOFÍA", 68, 44, 28, bold=True)
    corp(c, "\"Secret Santa\"  ·  Pam's stylish ally  ·  the earrings of the episode", 160, 44, 13, col=GREY)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    t = "UPTIMEZ INC. · CHARACTER MODEL SHEET · SECRET SANTA v2"
    corp(c, t, W2 - 24 - c.text_extents(t).x_advance, 30, 10, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()

    # 1. front
    c.set_source_rgb(*ACCENT); c.rectangle(24, 80, 240, 450); c.fill()
    ss.sofia(k, 144, 512, 1.18, "stand", "neutral", sparkle=0.7, seed=71)
    corp(c, "FRONT · OFFICE v4 + CRYSTAL TEARDROPS", 32, 524, 9, col=brand.NAVY, bold=True)

    # 2. Mandatory Fun / Secret Santa
    corp(c, "MANDATORY FUN  ·  SECRET SANTA", 284, 92, 10, bold=True)
    boxed(c, 284, 98, 330, 210)
    c.save(); c.rectangle(284, 98, 330, 210); c.clip()
    sm.sofia(k, 380, 300, 0.56, "stand", "neutral", seed=72)
    ss.sofia(k, 520, 300, 0.56, "stand", "neutral", sparkle=0.5, seed=72)
    c.restore()
    for lx, lab, col in ((338, "OLD · MANDATORY FUN", GREY), (466, "FINAL — LOCKED", (0.72, 0.12, 0.16))):
        c.set_source_rgb(1, 1, 1); c.rectangle(lx, 104, 112, 16); c.fill()
        c.set_source_rgb(*col); c.set_line_width(1.2); c.rectangle(lx, 104, 112, 16); c.stroke()
        corp(c, lab, lx + 6, 116, 8.5, col=col, bold=True)
    corp(c, "Gold hoops, black belt  →  crystal teardrops, a thin gold belt, glossy red. Same figure.", 290, 322, 9,
         col=GREY)

    # 3. faces
    corp(c, "FACES, BY SHOT  (dry, kind to Pam, unimpressed by Don)", 284, 348, 10, bold=True)
    faces = [("neutral", (-0.6, 0.1), None, 1.0, "1: the turn"), ("neutral", (-0.8, 0.1), "O", 0.0, "1: \"lips\""),
             ("knowing", (-0.7, 0.1), None, 0.0, "2: \"mirrors\""), ("eyebrow", (0.8, 0.0), None, 0.0, "7: eyebrow"),
             ("unimpressed", (1.0, 0.1), None, 0.0, "15: turns away")]
    for i, (e, lk, m, sp, lab) in enumerate(faces):
        x, y = 284 + i * 66, 354
        boxed(c, x, y, 63, 92, lab, fill=ROSE_BG if e == "knowing" else (1, 1, 1))
        c.save(); c.rectangle(x, y, 63, 92); c.clip()
        head_at(k, x + 31, y + 40, 0.4, e, lk, mouth=m, sparkle=sp)
        c.restore()
    corp(c, "MOUTHS  (red, glossy; they move little)", 284, 466, 9, col=GREY, bold=True)
    for i, (m, lab) in enumerate(((None, "rest"), ("F", "F"), ("O", "O"), ("A", "A"), ("E", "E"))):
        x, y = 284 + i * 66, 472
        boxed(c, x, y, 63, 60, lab)
        c.save(); c.rectangle(x, y, 63, 60); c.clip()
        head_at(k, x + 31, y + 18, 0.6, "neutral", (0, 0), mouth=m)
        c.restore()

    # 4. poses
    corp(c, "POSES", 634, 92, 10, bold=True)
    poses = [("stand", "neutral", dict(look=(-0.7, 0.1), lag=(6, 0), sparkle=1.0), "1: turns, sparkle"),
             ("compact", "neutral", dict(look=(-0.8, 0.1), compact_open=1.0), "2: the compact"),
             ("stand", "knowing", dict(look=(-0.7, 0.0)), "2: knowing smile"),
             ("stand", "eyebrow", dict(look=(0.9, 0.0)), "7: at Don"),
             ("stand", "unimpressed", dict(look=(1.0, 0.1), lean=4, lag=(-5, 0)), "15: turns away")]
    for i, (p, f, kw, lab) in enumerate(poses):
        x = 634 + i * 109
        boxed(c, x, 98, 105, 210, lab, fill=ROSE_BG if i == 0 else (1, 1, 1))
        c.save(); c.rectangle(x, 98, 105, 210); c.clip()
        ss.sofia(k, x + 52, 290, 0.5, p, f, seed=80 + i, **kw)
        c.restore()

    # 5. details
    corp(c, "DETAILS", 634, 348, 10, bold=True)
    boxed(c, 634, 354, 170, 178, "stud · link · crystal teardrop")
    c.save(); c.rectangle(634, 354, 170, 160); c.clip()
    c.set_source_rgb(*ss.HAIR); c.rectangle(634, 354, 170, 160); c.fill()
    c.save(); c.translate(690, 372); c.scale(2.6, 2.6)
    ss.teardrop(k, 0, 0, 0.0, 0.0, 1)
    c.restore()
    c.save(); c.translate(760, 372); c.scale(2.6, 2.6)
    ss.teardrop(k, 0, 0, 6.0, 1.0, 2)
    c.restore()
    corp(c, "rest", 676, 506, 8, col=INK, bold=True)
    corp(c, "sparkle, swing", 735, 506, 8, col=INK, bold=True)
    c.restore()
    boxed(c, 812, 354, 170, 178, "her compact; the thin gold belt")
    c.save(); c.rectangle(812, 354, 170, 160); c.clip()
    props.compact(k, 860, 430, 2.2, -0.1, 1.0, 9)
    props.compact(k, 860, 495, 2.2, 0.0, 0.0, 10)
    c.save(); c.translate(940, 486); c.scale(1.5, 1.5)
    kit.rect(k, -22, -4, 44, 8, ss.GOLD, 11, shadow=False, lw=1.4)
    kit.ellipse(k, 0, 0, 6, 6, ss.GOLD, 12, shadow=False, lw=1.4)
    kit.ellipse(k, 0, 0, 2.6, 2.6, ss.GOLD_LIGHT, 13, shadow=False, outline=False)
    c.restore()
    c.restore()
    boxed(c, 990, 354, 186, 178, "her red vs Pam's new dusty rose")
    c.save(); c.rectangle(990, 354, 186, 160); c.clip()
    head_at(k, 1040, 440, 1.0, "smile", (0.4, 0))
    props.lipstick(k, 1130, 488, 1.6, 0.15, 1.0, 14)
    props.kiss(k, 1132, 382, 1.1)
    c.restore()

    # 6. frame 0 / loop + phone-size check
    corp(c, "FRAME 0 = THE LOOP  ·  PHONE-SIZE CHECK", 24, 556, 10, bold=True)
    frame0(k, 24, 562, 104, 186, 0.0, 1.0, "frame 0: cap on")
    frame0(k, 136, 562, 104, 186, 0.75, 0.4, "0.5 s: pop, cap off", pop=True)
    c.set_source_rgb(*kit.WALL); c.rectangle(250, 562, 364, 186); c.fill()
    c.save(); c.rectangle(250, 562, 364, 186); c.clip()
    pm.pam(k, 300, 760, 0.42, "stand", "hopeful", look=(0.8, 0), seed=95)
    ss.sofia(k, 372, 760, 0.42, "compact", "knowing", look=(-0.8, 0.1), compact_open=1.0, sparkle=0.6, seed=96)
    dv.don(k, 486, 770, 0.38, seed=97)
    ss.sofia(k, 566, 760, 0.42, "stand", "unimpressed", look=(1.0, 0.1), lean=4, lag=(-5, 0), seed=98)
    c.restore()
    c.set_source_rgb(*INK); c.set_line_width(1.2); c.rectangle(250, 562, 364, 186); c.stroke()
    corp(c, "2: the compact with Pam  ·  15: she turns away from Don (stand-ins)", 250, 760, 8.5, col=GREY, bold=True)

    # 7. notes
    corp(c, "NOTES", 634, 556, 10, bold=True)
    notes = ["Office v4 unchanged underneath: long hair, teal wrap blouse, block heels, badge.",
             "The episode's earrings: original crystal teardrops (no logos), about the size of her hoops.",
             "Frame 0 and the loop: Pam's hand uncaps the lipstick; Sofía soft behind, the teardrop sparkles.",
             "A thin gold belt matches the earrings; her classic red lips get a touch of gloss.",
             "She is on Pam's side: the compact, the knowing smile. To Don: the eyebrow, then her back.",
             "Never a mean girl, never Don's object: the camera stays on Pam, Sofía is her stylish ally.",
             "LOCKED. Readability comes from camera, timing and one glint, never from new art."]
    for i, n in enumerate(notes):
        corp(c, "·  " + n, 634, 580 + i * 24, 11, col=INK)
    camera_row(c)
    flush(c)
    surf.write_to_png(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "sofia_sheet_ss_v2.png")
    phone_test("ss_frame0_phone_v2.png")
