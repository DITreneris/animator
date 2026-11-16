"""MOM model sheet for "Office Noir" (mom_on.py), v2 (mom_sheet_on_v1.py = v1, kept). v2 after the review: the
pearl chain leaves the face at the hinges; four big curlers; the shout stares down-left at Don with lower inner
brows; shot 10 becomes 10A (DONNIE! with the head thrust, then a frozen stare) and 10B (Don frozen, the fedora
lifts a few pixels); the heart is 30 % bigger and the fingertip stops just above it. Writes mom_sheet_on_v2.png
and mom_phone_on_v2.png.
v1 notes: Writes mom_sheet_on_v1.png at 2400x2260 (drawn at 1200x1130,
2x) and mom_phone_on_v1.png (shot 10 at phone size and as a grid thumbnail).
Sections: the front figure, turnaround (front, three-quarter, back) with a height line-up next to Pam and Don,
the three poses, the four faces, details (curlers + hairnet, glasses on the pearl chain, the mug, slippers,
palette with a measured no-red check), and shot 10 as a 9:16 crop (colour, high angle, stand-ins for Don and
the bed)."""
import sys
import math
import cairo
import numpy as np
import kit
import brand
import mom_on as m
import pam_ss as ps
import don_ss as ds
from kit import Ctx, INK, ellipse, rect
from charsheets import corp, wrap
from pam_sheet_mf import boxed, flush

W2, H2 = 1200, 1130
GREY = (0.35, 0.40, 0.50)
BG = (0.97, 0.96, 0.93)
WASH = (0.93, 0.95, 0.94)
HEART = (0xD2 / 255, 0x1F / 255, 0x2B / 255)
k = None


def clip(x, y, w, h, fn, fill=(1, 1, 1), label=None):
    boxed(k.c, x, y, w, h, label, fill=fill)
    k.c.save(); k.c.rectangle(x, y, w, h); k.c.clip(); fn(); k.c.restore()


def heart_path(c, x, y, s):
    c.move_to(x, y + 0.9 * s)
    c.curve_to(x - 1.6 * s, y - 0.1 * s, x - 0.9 * s, y - 1.1 * s, x, y - 0.45 * s)
    c.curve_to(x + 0.9 * s, y - 1.1 * s, x + 1.6 * s, y - 0.1 * s, x, y + 0.9 * s)
    c.close_path()


def don_standin(kk, x, y, sc, eyes="shut", lift=0.0):
    """Don stand-in head + fedora (step 4 replaces it). eyes: "shut" (asleep/defeated) or "open" (frozen)."""
    c = kk.c
    c.save(); c.translate(x, y); c.scale(sc, sc)
    ellipse(kk, 0, 0, 52, 50, (0.96, 0.78, 0.66), 804)
    c.set_source_rgb(*INK); c.set_line_width(4)
    for ex in (-18, 18):
        if eyes == "open":
            ellipse(kk, ex, 2, 9, 9, (1, 1, 1), 806 + ex, shadow=False, lw=2)
            ellipse(kk, ex - 2, 4, 2.6, 2.6, INK, 807 + ex, shadow=False, outline=False)
        else:
            c.new_path(); c.arc(ex, 4, 8, 0.1 * math.pi, 0.9 * math.pi); c.stroke()
    c.set_source_rgb(*INK); c.set_line_width(4)
    c.new_path(); c.move_to(-10, 30); c.line_to(10, 30); c.stroke() if eyes == "open" else None
    if eyes != "open":
        c.new_path(); c.move_to(-12, 30); c.curve_to(-4, 24, 4, 24, 12, 30); c.stroke()
    c.translate(0, -lift)
    kit.cut(kk, [(-74, -34), (74, -40), (66, -26), (-66, -20)], (0.24, 0.23, 0.26), shadow=False)
    kit.cut(kk, [(-44, -36), (-38, -84), (40, -88), (44, -40)], (0.24, 0.23, 0.26), shadow=False)
    c.restore()


def bedroom(kk):
    c = kk.c
    c.set_source_rgb(0.96, 0.92, 0.80); c.rectangle(0, 0, 540, 960); c.fill()          # cream wall
    for i in range(9):                                                                  # warm light flooding in
        c.set_source_rgba(1.0, 0.95, 0.70, 0.08); c.move_to(-40, 0); c.line_to(120 + i * 40, 0)
        c.line_to(260 + i * 60, 960); c.line_to(-40, 960); c.close_path(); c.fill()
    rect(kk, -10, -10, 90, 520, m.MUSTARD, 801, shadow=False, lw=2)                       # curtain, yanked open
    c.set_source_rgb(*m.MUSTARD_DARK); c.set_line_width(2)
    for x in (18, 40, 62):
        c.move_to(x, 0); c.line_to(x + 4, 500); c.stroke()
    rect(kk, -20, 560, 600, 420, (0.70, 0.84, 0.94), 802)                                 # the bed, from above
    rect(kk, 30, 590, 250, 110, (0.98, 0.95, 0.88), 803)                                  # pillow


def pyjama_heart(kk, hx, hy, hs):
    c = kk.c
    rect(kk, 40, 730, 300, 230, (0.62, 0.78, 0.92), 805)                                  # pyjama torso
    c.set_source_rgb(0.45, 0.60, 0.78); c.set_line_width(2)
    c.move_to(175, 735); c.line_to(175, 960); c.stroke()
    rect(kk, hx - hs * 1.5, hy - hs * 1.15, hs * 3.0, hs * 2.4, (0.66, 0.81, 0.94), 808, shadow=False, lw=1.6)  # pocket
    heart_path(c, hx, hy, hs)
    c.set_source_rgb(*HEART); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.6); c.stroke()


def shot10(kk, thrust=1.0, face="shout", mouth=None):
    """Shot 10A at 540x960: colour, high angle. Mom looms from screen right, stares down-left at Don and points
    at the heart; the fingertip stops just above it. The heart is 30 % bigger than v1 (39 vs 30)."""
    c = kk.c
    bedroom(kk)
    dummy = cairo.ImageSurface(cairo.FORMAT_ARGB32, 4, 4)                                 # where will the tip be?
    tip = m.mom(Ctx(cairo.Context(dummy), 0), 575, 1010, 2.4, pose="loom", face=face, lean=-12,
                look=(-0.9, 0.8), thrust=thrust)["tip"]
    hs = 39
    hx, hy = tip[0] + 2, tip[1] + 14 + 0.75 * hs
    pyjama_heart(kk, hx, hy, hs)
    don_standin(kk, 175, 660, 1.35)
    m.mom(kk, 575, 1010, 2.4, pose="loom", face=face, lean=-12, look=(-0.9, 0.8), thrust=thrust, mouth=mouth)
    kit.text(kk, "stand-ins: Don, the bed", 200, 950, 15, (0.4, 0.4, 0.45))
    return (hx, hy)


def shot10b(kk, heart_at):
    """Shot 10B: Don, frozen. Eyes open, the fedora lifted a few pixels; the heart in the same place."""
    c = kk.c
    bedroom(kk)
    pyjama_heart(kk, heart_at[0], heart_at[1], 39)
    don_standin(kk, 175, 660, 1.35, eyes="open", lift=4)
    kit.text(kk, "stand-in: Don", 200, 950, 15, (0.4, 0.4, 0.45))


def red_pixels():
    """Mom alone in every pose and face: count strongly red pixels (hue within 20 deg of red, sat > 0.45)."""
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1400, 520)
    c = cairo.Context(surf); c.set_source_rgb(1, 1, 1); c.paint()
    kk = Ctx(c, 0)
    for i, (pose, face, view) in enumerate([("stand", "stern", "front"), ("hip_mug", "unimpressed", "front"),
                                            ("loom", "shout", "front"), ("folded", "proud", "three"),
                                            ("stand", "stern", "back")]):
        m.mom(kk, 140 + i * 270, 500, 1.3, pose=pose, face=face, view=view)
    surf.flush()
    a = np.ndarray((520, 1400, 4), np.uint8, surf.get_data())[..., :3].astype(float) / 255
    b, g, r = a[..., 0], a[..., 1], a[..., 2]
    mx, mn = a.max(-1), a.min(-1)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    red = (r == mx) & (sat > 0.45) & (mx > 0.35) & (np.abs(g - b) < 0.25 * (mx - mn) + 0.02) & (g < r * 0.6)
    return int(red.sum())


def main(out, phone_out):
    global k
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(*BG); c.paint()
    k = Ctx(c, 0)
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "MOM", 68, 44, 28, bold=True)
    corp(c, "\"Office Noir\"  ·  the reality check  ·  never softens", 150, 44, 13, col=GREY)
    corp(c, "UPTIMEZ INC. · CHARACTER MODEL SHEET · OFFICE NOIR v2", 890, 34, 9.5, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 70); c.line_to(W2 - 24, 70); c.stroke()

    # front, big
    c.set_source_rgb(*WASH); c.rectangle(28, 92, 280, 528); c.fill()
    m.mom(k, 168, 590, 1.38)
    corp(c, "FRONT · TEAL + MUSTARD HOUSECOAT · NO RED", 36, 612, 9.5, bold=True)

    # turnaround + line-up
    corp(c, "TURNAROUND  +  HEIGHT NEXT TO PAM AND DON", 330, 104, 10.5, bold=True)

    def turn():
        m.mom(k, 385, 352, 0.62, view="front")
        m.mom(k, 470, 352, 0.62, view="three", face="unimpressed")
        m.mom(k, 555, 352, 0.62, view="back")
        ps.pam(k, 630, 352, 0.62)
        ds.don(k, 690, 352, 0.62, shades="off")
        c.set_source_rgba(*GREY, 0.6); c.set_line_width(0.8); c.set_dash([3, 3])
        for yy in (352 + (m.HY - 66) * 0.62, 352 + (ps.HY - 62) * 0.62):
            c.move_to(338, yy); c.line_to(716, yy); c.stroke()
        c.set_dash([])
    clip(330, 112, 390, 250, turn, label="front · three-quarter · back · Pam · Don (stand-ins)")

    # poses
    corp(c, "POSES", 740, 104, 10.5, bold=True)
    poses = [("loom", "shout", -10, "10A: DONNIE! (thrust)"), ("hip_mug", "stern", 0, "hand on hip, the mug"),
             ("folded", "unimpressed", 0, "arms folded (doorway)")]
    for i, (pose, face, lean, lab) in enumerate(poses):
        x0 = 740 + i * 146
        clip(x0, 112, 140, 250, (lambda pose=pose, face=face, lean=lean, x0=x0:
                                  m.mom(k, x0 + 72 + (14 if lean else 0), 352, 0.62, pose=pose, face=face, lean=lean, look=(-0.9, 0.8) if lean else (0, 0), thrust=1.0 if lean else 0.0)),
             fill=(1, 1, 1), label=lab)

    # faces
    corp(c, "FACES  (one look says she runs the house)", 330, 390, 10.5, bold=True)
    faces = [("stern", "stern \u00b7 default", (0, 0)), ("shout", "shout \u00b7 at Don", (-0.9, 0.8)),
             ("unimpressed", "unimpressed", (0, 0)), ("proud", "proud \u00b7 rare, later", (0, 0))]
    for i, (face, lab, lk) in enumerate(faces):
        x0 = 330 + i * 98
        clip(x0, 398, 92, 120, (lambda face=face, x0=x0, lk=lk: m.mom(k, x0 + 46, 398 + 74 - m.HY * 0.8, 0.8,
                                                                       face=face, look=lk)),
             fill=WASH, label=lab)
    corp(c, "MOUTHS FOR SPEECH (mauve, no red)", 330, 546, 10.5, bold=True)
    for i, mo in enumerate(("rest", "E", "O", "A")):
        x0 = 330 + i * 98
        clip(x0, 554, 92, 66, (lambda mo=mo, x0=x0: m.mom(k, x0 + 46, 554 + 6 - (m.HY + 28) * 1.1, 1.1, face="stern",
                                                          mouth=None if mo == "rest" else mo)),
             fill=WASH, label=mo)

    # details
    corp(c, "DETAILS", 740, 390, 10.5, bold=True)

    def det_curlers():
        c.save(); c.translate(810, 470 - (m.HY - 36) * 1.35); c.scale(1.35, 1.35)
        m._hair_and_curlers(k, 70)
        c.restore()
    clip(740, 398, 140, 120, det_curlers, fill=WASH, label="curlers under a hairnet")

    def det_glasses():
        c.save(); c.translate(956, 445 - m.HY * 1.4); c.scale(1.4, 1.4); m._glasses(c); c.restore()
    clip(886, 398, 140, 120, det_glasses, fill=WASH, label="heavy frames, pearl chain")

    def det_mug():
        m._mug(k, 1070, 446, 1.7)
        m._slipper(k, 1150 - 4, 0) if False else None
        c.save(); c.translate(1138, 488); c.scale(0.8, 0.8); m._slipper(k, 0, 9); c.restore()
    clip(1032, 398, 140, 120, det_mug, fill=WASH, label="#1 MOM mug · slipper")

    sw = [(m.TEAL, "teal"), (m.TEAL_DARK, "quilting"), (m.MUSTARD, "mustard"), (m.CREAM, "cream"),
          (m.LILAC, "lilac"), (m.HAIR, "hair"), (m.MAUVE, "mauve lips"), (m.PEARL, "pearl")]
    boxed(c, 740, 530, 432, 90, "palette · measured: " + f"{RED} strongly red pixels in all poses and faces")
    for i, (col, name) in enumerate(sw):
        x0 = 752 + i * 52
        c.set_source_rgb(*col); c.rectangle(x0, 540, 40, 30); c.fill()
        c.set_source_rgb(*INK); c.set_line_width(0.8); c.rectangle(x0, 540, 40, 30); c.stroke()
        corp(c, name, x0, 584, 7.5, col=GREY)
        corp(c, "#%02X%02X%02X" % tuple(int(round(v * 255)) for v in col), x0, 594, 6.5, col=GREY)

    # shot 10 crop + phone tests
    corp(c, "SHOT 10A: 9:16 CROP (COLOUR, HIGH ANGLE)  +  PHONE TESTS", 28, 652, 10.5, bold=True)
    s10 = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)
    heart_at = shot10(Ctx(cairo.Context(s10), 0))
    s10.write_to_png("/tmp/on_shot10.png")
    beats = []
    for (th, fc, mo) in ((1.0, "shout", None), (1.0, "stern", None)):
        sb = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)
        shot10(Ctx(cairo.Context(sb), 0), thrust=th, face=fc, mouth=mo); beats.append(sb)
    sb = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)
    shot10b(Ctx(cairo.Context(sb), 0), heart_at); beats.append(sb)

    def place(x, y, w):
        c.save(); c.translate(x, y); sc = w / 540; c.scale(sc, sc)
        c.set_source_surface(s10, 0, 0); c.get_source().set_filter(cairo.FILTER_BEST); c.paint(); c.restore()
        c.set_source_rgb(*INK); c.set_line_width(1); c.rectangle(x, y, w, w * 960 / 540); c.stroke()
    place(28, 662, 240)
    corp(c, "the crop (stand-ins for Don and the bed)", 28, 1100, 9, col=GREY)
    place(290, 662, 120)
    corp(c, "phone, in feed", 290, 885, 9, col=GREY)
    place(290, 900, 54)
    corp(c, "grid thumbnail", 290, 1010, 9, col=GREY)

    notes = [
        "Formidable, never grotesque: no warts, no extra wrinkles. Her power is authority and familiarity.",
        "Read order in 10A: her face, the finger, the heart (30 % bigger, the tip stops just above it), then Don.",
        "Priority on the head: glasses and four big curlers first; the pearl chain is secondary, outside the face.",
        "No red anywhere on her (measured above): red belongs to the heart.",
    ]
    corp(c, "NOTES", 440, 664, 10.5, bold=True)
    y = 684
    for n in notes:
        y = wrap(c, "· " + n, 440, y, 9.5, 730, col=(0.2, 0.22, 0.28)) + 20
    corp(c, "SHOT 10A, THEN 10B: SHOUT, FREEZE, CUT TO DON", 440, 800, 10.5, bold=True)
    labs = ["10A \u00b7 24.8 s: \"DONNIE!\", head thrust", "10A \u00b7 25.6\u201327.0 s: \"Up. Time for work.\" Then still",
            "10B \u00b7 27.0\u201330.0 s: Don frozen, fedora +4 px"]
    for i, sb in enumerate(beats):
        x0, y0, w = 440 + i * 150, 812, 140
        c.save(); c.translate(x0, y0); c.scale(w / 540, w / 540)
        c.set_source_surface(sb, 0, 0); c.get_source().set_filter(cairo.FILTER_BEST); c.paint(); c.restore()
        c.set_source_rgb(*INK); c.set_line_width(1); c.rectangle(x0, y0, w, w * 960 / 540); c.stroke()
        wrap(c, labs[i], x0, y0 + w * 960 / 540 + 14, 8.5, w, col=GREY)
    flush(c)
    surf.write_to_png(out)

    # phone file: the crop at a typical phone size next to a feed-grid thumbnail
    ps_ = cairo.ImageSurface(cairo.FORMAT_ARGB32, 760, 760)
    cp = cairo.Context(ps_); cp.set_source_rgb(*BG); cp.paint()
    for (x, w, lab) in ((20, 390, "phone width, 390 px"), (440, 130, "feed tile"), (600, 70, "grid thumb")):
        cp.save(); cp.translate(x, 20); sc = w / 540; cp.scale(sc, sc)
        cp.set_source_surface(s10, 0, 0); cp.get_source().set_filter(cairo.FILTER_BEST); cp.paint(); cp.restore()
        corp(cp, lab, x, 20 + w * 960 / 540 + 18, 13, col=GREY)
    ps_.write_to_png(phone_out)


RED = red_pixels()
if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "mom_sheet_on_v2.png",
         sys.argv[2] if len(sys.argv) > 2 else "mom_phone_on_v2.png")
