"""v1 (pinned; imports pam_ss_v1). PAM model sheet for "Secret Santa" (pam_ss.py). Writes pam_sheet_ss_v1.png at 2400x2000 (drawn at 1200x1000,
2x): the look (Mandatory Fun office purple + the dusty-rose nude, clearly rosy), faces and poses by shot, the rose
speaking mouths, details (the glasses on the chain, natural vs rose lips, the lipstick and the kissed gift tag),
9:16 camera crops on the drawings, and the glasses arc that tracks her through the film."""
import sys
import math
import cairo
import kit
import brand
import pam_mf as pm
import pam_ss_v1 as ps
import sofia_ss as ss
import don_v4 as dv
import props_ss as props
from kit import Ctx, INK
from charsheets import corp
from pam_sheet_mf import boxed, flush, pop
from sofia_sheet_mf import HY as SHY

W2, H2 = 1200, 1000
GREY = (0.35, 0.40, 0.50)
ACCENT = (0.93, 0.91, 0.96)
ROSE_BG = (1.0, 0.94, 0.95)
CREAM = (0.98, 0.95, 0.86)
RED = (0.72, 0.12, 0.16)
HY = pm.HY
k = None


def head(cx, cy, s, face, look=(0, 0), lips="rose", glasses="low", mouth=None):
    ps.pam(k, cx, cy - HY * s, s, "stand", face, look=look, lips=lips, glasses=glasses, mouth=mouth)


def clip_box(x, y, w, h, draw, fill=None, label=None, frame=False):
    c = k.c
    if frame:
        c.save(); c.rectangle(x, y, w, h); c.clip()
        c.set_source_rgb(*(fill or kit.WALL)); c.rectangle(x, y, w, h); c.fill()
        draw()
        c.restore()
        c.set_source_rgb(*INK); c.set_line_width(1.2); c.rectangle(x, y, w, h); c.stroke()
        if label:
            corp(c, label, x, y + h + 12, 8.5, col=GREY, bold=True)
    else:
        boxed(c, x, y, w, h, label, fill=fill or (1, 1, 1))
        c.save(); c.rectangle(x, y, w, h); c.clip(); draw(); c.restore()


def gift_tag(c, x, y, s, rot=-0.08):
    """The cream tag: printed TO: / FROM:, her handwriting, the dusty-rose kiss."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.move_to(-34, -20); c.line_to(26, -20); c.line_to(38, 0); c.line_to(26, 20); c.line_to(-34, 20); c.close_path()
    c.set_source_rgb(*CREAM); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.6); c.stroke()
    c.arc(28, 0, 3, 0, 2 * math.pi); c.stroke()
    corp(c, "TO:", -29, -6, 6.5, col=GREY, bold=True)
    corp(c, "FROM:", -30, 10, 5.5, col=GREY, bold=True)
    corp(c, "DON", -13, -6, 8, col=(0.20, 0.20, 0.45), bold=True)
    heart(c, 10, -9, 3.2, RED)
    corp(c, "PAM", -8, 10, 8, col=(0.20, 0.20, 0.45), bold=True)
    c.restore()
    props.kiss(k, x + 21 * s, y + 9 * s, 0.26 * s)


def heart(c, x, y, r, col):
    c.move_to(x, y + r * 1.1)
    c.curve_to(x - r * 1.6, y - r * 0.2, x - r * 0.8, y - r * 1.4, x, y - r * 0.5)
    c.curve_to(x + r * 0.8, y - r * 1.4, x + r * 1.6, y - r * 0.2, x, y + r * 1.1); c.close_path()
    c.set_source_rgb(*col); c.fill()


def main(out):
    global k
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "PAM", 68, 44, 28, bold=True)
    corp(c, "\"Secret Santa\"  ·  the brave one  ·  dusty rose, glasses on the chain", 140, 44, 13, col=GREY)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    t = "UPTIMEZ INC. · CHARACTER MODEL SHEET · SECRET SANTA v1"
    corp(c, t, W2 - 24 - c.text_extents(t).x_advance, 30, 10, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()

    # 1. front
    c.set_source_rgb(*ACCENT); c.rectangle(24, 80, 240, 450); c.fill()
    ps.pam(k, 144, 512, 1.18, "stand", "neutral", seed=71)
    corp(c, "FRONT · OFFICE PURPLE + DUSTY ROSE", 32, 524, 9, col=brand.NAVY, bold=True)

    # 2. Mandatory Fun / Secret Santa
    corp(c, "MANDATORY FUN  ·  SECRET SANTA", 284, 92, 10, bold=True)
    boxed(c, 284, 98, 330, 210)
    c.save(); c.rectangle(284, 98, 330, 210); c.clip()
    pm.pam(k, 380, 300, 0.58, "stand", "neutral", seed=72)
    ps.pam(k, 520, 300, 0.58, "stand", "neutral", seed=72)
    c.restore()
    for lx, lab, col in ((324, "OLD · MANDATORY FUN", GREY), (464, "FINAL — LOCKED", RED)):
        c.set_source_rgb(1, 1, 1); c.rectangle(lx, 104, 112, 16); c.fill()
        c.set_source_rgb(*col); c.set_line_width(1.2); c.rectangle(lx, 104, 112, 16); c.stroke()
        corp(c, lab, lx + 6, 116, 8.5, col=col, bold=True)
    corp(c, "Same Pam, same figure; only the lips change (from shot 2) and where the glasses are.", 290, 322, 9,
         col=GREY)

    # 3. faces by shot
    corp(c, "FACES, BY SHOT  (hopes, deflates, decides; never tearful)", 284, 348, 10, bold=True)
    faces = [("neutral", (-0.8, 0), None, "low", "O", "1: whisper"), ("hopeful", (-0.9, -0.1), "rose", "chain", None, "5: hopeful"),
             ("fade", (-0.6, 0.3), "rose", "chain", None, "7: deflates"), ("decide", (0, 0), "rose", "chain", None, "7: decides"),
             ("proud", (0, 0), "rose", "chain", None, "9: proud"), ("incredulous", (0, 0), "rose", "low", None, "15: no.")]
    for i, (f, lk, lp, g, m, lab) in enumerate(faces):
        x, y = 284 + i * 55.5, 354
        clip_box(x, y, 52.5, 92, lambda x=x, y=y, f=f, lk=lk, lp=lp, g=g, m=m: head(x + 26, y + 36, 0.62, f, lk, lp, g, m),
                 fill=ROSE_BG if f == "proud" else None, label=lab)
    corp(c, "MOUTHS, DUSTY ROSE (she talks small and narrow)", 284, 466, 10, bold=True)
    for i, m in enumerate(("M", "E", "F", "O", "A", "C")):
        x, y = 284 + i * 55.5, 472
        clip_box(x, y, 52.5, 58, lambda x=x, y=y, m=m: head(x + 26, y + 6, 0.62, "neutral", (0, 0), "rose", "chain", m),
                 label=m)

    # 4. poses
    corp(c, "POSES", 634, 92, 10, bold=True)
    poses = [("stand", "neutral", dict(look=(-0.9, 0), lips=None, mouth="O"), "1: the whisper"),
             ("stand", "neutral", dict(look=(-0.4, 0.2), apply=True), "2: puts it on"),
             (ps.POSE_GLASSES, "hopeful", dict(finger="bridge", look=(-1, 0)), "4: glasses off"),
             (ps.POSE_SHY, "hopeful", dict(glasses="chain", look=(-1, -0.1), lean=-4), "5: on the chain"),
             ("stand", "incredulous", dict(), "15: back on")]
    for i, (pose, f, kw, lab) in enumerate(poses):
        x = 634 + i * 109
        def d(x=x, pose=pose, f=f, kw=kw):
            ps.pam(k, x + 52, 286, 0.55, pose, f, seed=80 + i, **kw)
            if lab.startswith("5"):
                pop(k, "\U0001F497", x + 82, 128, 11)
        clip_box(x, 98, 105, 210, d, fill=ROSE_BG if i == 3 else None, label=lab)

    # 5. details
    corp(c, "DETAILS", 634, 348, 10, bold=True)
    def glasses_detail():
        head(676, 404, 0.82, "neutral", (0, 0), "rose", "low")
        head(762, 404, 0.82, "neutral", (0, 0), "rose", "chain")
    clip_box(634, 354, 170, 160, glasses_detail, label="glasses: on · on the chain")
    def lips_detail():
        c.save(); c.translate(897, 380); c.scale(2.6, 2.6)
        c.set_source_rgb(*pm.SKIN); c.rectangle(-32, -12, 64, 50); c.fill()
        c.set_source_rgb(*INK); c.set_line_width(3.6); c.set_line_cap(1)
        c.move_to(-24, 8); c.curve_to(-19, 10, -13, 10, -8, 7); c.stroke()
        ps.lips_along(c, 15, -20, ps.CENTRE["hopeful"])
        c.restore()
        corp(c, "natural", 828, 482, 8, col=GREY); corp(c, "dusty rose", 912, 482, 8, col=GREY)
    clip_box(812, 354, 170, 160, lips_detail, label="shot 1 natural · then rosy")
    def tag_detail():
        props.lipstick(k, 1018, 482, 1.5, 0.15, 0.0, 14, cap_col=props.CAP_BLACK)
        props.lipstick(k, 1048, 482, 1.5, 0.15, 1.0, 14, cap_col=props.CAP_BLACK)
        gift_tag(c, 1124, 418, 1.2)
    clip_box(990, 354, 186, 160, tag_detail, fill=ROSE_BG, label="her lipstick · the tag she signs")

    # 6. 9:16 camera crops
    y0 = 562
    corp(c, "9:16 CROPS ON THE DRAWINGS  (stand-ins for the others)", 24, y0 - 6, 10, bold=True)
    W, H = 100, 178

    def c1():
        ss.sofia(k, 24 + 82, y0 + 300, 0.82, "stand", "neutral", look=(-0.7, 0.1), badge=False, seed=91)
        ps.pam(k, 24 + 22, y0 + 312, 0.82, "stand", "neutral", look=(0.9, 0), lips=None, mouth="O", seed=92)
    clip_box(24, y0, W, H, c1, frame=True, label="1: whisper to Sofía")

    def c5():
        dv.don(k, 132 + 84, y0 + 300, 0.70, seed=93)
        ps.pam(k, 132 + 28, y0 + 300, 0.70, ps.POSE_SHY, "hopeful", look=(1, -0.2), glasses="chain", seed=94)
        pop(k, "\U0001F497", 132 + 46, y0 + 30, 10)
    clip_box(132, y0, W, H, c5, frame=True, label="5: to Don, one heart")

    def c7():
        def bg(lc):
            ss.sofia(Ctx(lc, 0), 240 + 84, y0 + 52 - SHY * 0.8, 0.8, "stand", "eyebrow", look=(0.8, 0), badge=False, seed=95)
        props.soft(c, bg, 1.8)
        head(240 + 40, y0 + 110, 1.05, "fade", (-0.6, 0.3), "rose", "chain")
    clip_box(240, y0, W, H, c7, frame=True, label="7: CU, Sofía soft")
    clip_box(348, y0, W, H, lambda: head(348 + 50, y0 + 84, 1.15, "proud"), frame=True, fill=ROSE_BG,
             label="9: CU, proud")
    clip_box(456, y0, W, H, lambda: head(456 + 50, y0 + 84, 1.15, "incredulous"), frame=True,
             label="15: glasses on, no.")

    # 7. notes
    corp(c, "NOTES", 634, 556, 10, bold=True)
    notes = ["Mandatory Fun office look unchanged: purple cardigan, bob with the grey lock, lanyard, keys.",
             "The dusty-rose nude reads clearly rosy from shot 2: full lips, a gloss dot; softer than Sofía's red.",
             "Glasses = her journey: on (1–3), off on the bridge (4), dropped on the chain (5–14), back on (15).",
             "Proud (9): a shy closed smile and a blush, eyes on the tag. Her high point, so the stamp is unfair.",
             "Incredulous (15, the loop): narrowed eyes, flat mouth. Disbelief, then attempt number two.",
             "Endearing, never pathetic: one breath of deflation, then a visible decision. One heart pop only.",
             "Readability from camera and timing (lesson from Sofía's review): CUs on 7, 9, 15."]
    for i, n in enumerate(notes):
        corp(c, "·  " + n, 634, 580 + i * 24, 10.5, col=INK)

    # 8. the glasses arc
    y1 = 800
    corp(c, "THE GLASSES ARC  (one gesture that tracks her through the film)", 24, y1 - 6, 10, bold=True)
    boxed(c, 24, y1, 1152, 180)
    arc = [("1–3", "stand", "neutral", dict(look=(-0.6, 0)), "on, low on the nose"),
           ("4", ps.POSE_GLASSES, "hopeful", dict(finger="bridge", look=(-1, 0)), "off, for Don"),
           ("5–8", ps.POSE_SHY, "hopeful", dict(glasses="chain", look=(-1, -0.1)), "on the chain"),
           ("9", ps.POSE_SHY, "proud", dict(glasses="chain"), "still on the chain"),
           ("15", "stand", "incredulous", dict(), "back on, to read the tag"),
           ("16", "stand", "incredulous", dict(apply=True), "attempt two")]
    c.save(); c.rectangle(24, y1, 1152, 180); c.clip()
    for i, (sh, pose, f, kw, lab) in enumerate(arc):
        x = 110 + i * 192
        ps.pam(k, x, y1 + 160, 0.40, pose, f, seed=120 + i, **kw)
        corp(c, sh, x + 44, y1 + 40, 16, col=brand.NAVY, bold=True)
        corp(c, lab, x + 44, y1 + 58, 9, col=GREY)
        if i < len(arc) - 1:
            c.set_source_rgb(*GREY); c.set_line_width(1.6)
            c.move_to(x + 120, y1 + 110); c.line_to(x + 150, y1 + 110); c.stroke()
            c.move_to(x + 144, y1 + 105); c.line_to(x + 150, y1 + 110); c.line_to(x + 144, y1 + 115); c.stroke()
    c.restore()
    flush(c)
    surf.write_to_png(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "pam_sheet_ss_v1.png")
