"""v2 (v1 pinned in pam_sheet_ss_v1.py). PAM model sheet for "Secret Santa" (pam_ss.py v2). Writes pam_sheet_ss_v2.png at 2400x2260 (drawn at 1200x1000,
2x): the look (Mandatory Fun office purple + the dusty-rose nude, clearly rosy), faces and poses by shot, the rose
speaking mouths, details (the glasses on the chain, natural vs rose lips, the lipstick and the kissed gift tag),
9:16 camera crops on the drawings, and the glasses arc that tracks her through the film.
v2 (review): 7A hurt / 7B decides, a closed shy proud, stronger incredulous, the glasses held out (4), a fresh tag
on 16, the whisper lean, rose closed mouths, the tag before/after strip, the tag in the 9 and 15 close-ups."""
import sys
import math
import cairo
import kit
import brand
import pam_mf as pm
import pam_ss as ps
import sofia_ss as ss
import don_v4 as dv
import props_ss as props
from kit import Ctx, INK
from charsheets import corp
from pam_sheet_mf import boxed, flush, pop
from sofia_sheet_mf import HY as SHY

W2, H2 = 1200, 1130
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


def heart(c, x, y, r, col):
    c.move_to(x, y + r * 1.1)
    c.curve_to(x - r * 1.6, y - r * 0.2, x - r * 0.8, y - r * 1.4, x, y - r * 0.5)
    c.curve_to(x + r * 0.8, y - r * 1.4, x + r * 1.6, y - r * 0.2, x, y + r * 1.1); c.close_path()
    c.set_source_rgb(*col); c.fill()


def gift_tag(c, x, y, s, rot=-0.08, bars=(), blank=False, bar_style=1, big=False, kiss_k=1.0, kiss=True, kiss_dx=0.0):
    """The cream tag: printed TO: / FROM:, her handwriting, the dusty-rose kiss. bars: which of "from", "to", "kiss"
    the robot has stamped out (black bars; the printed TO: and FROM: stay readable). blank: a fresh tag."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.move_to(-34, -20); c.line_to(26, -20); c.line_to(38, 0); c.line_to(26, 20); c.line_to(-34, 20); c.close_path()
    c.set_source_rgb(*CREAM); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.6); c.stroke()
    c.arc(28, 0, 3, 0, 2 * math.pi); c.stroke()
    corp(c, "TO:", -29, -6, 6.5, col=GREY, bold=True)
    corp(c, "FROM:", -30, 10, 5.5, col=GREY, bold=True)
    if not blank and big:               # set sheet v2: the handwritten names bigger, the printed labels unchanged
        corp(c, "DON", -14, -5, 10.5, col=(0.20, 0.20, 0.45), bold=True)
        heart(c, 13, -9.5, 4.0, RED)
        corp(c, "PAM", -9, 12, 10.5, col=(0.20, 0.20, 0.45), bold=True)
    elif not blank:
        corp(c, "DON", -13, -6, 8, col=(0.20, 0.20, 0.45), bold=True)
        heart(c, 10, -9, 3.2, RED)
        corp(c, "PAM", -8, 10, 8, col=(0.20, 0.20, 0.45), bold=True)
    c.set_source_rgb(0.08, 0.08, 0.10)
    if bar_style == 2:                  # robot sheet v2: a clear gap between the bars and a cream edge, so stacked
        rects = {"to": (-14, -15, 30, 10), "from": (-9, 3, 24, 10), "kiss": (17, 3, 12, 10)}   # bars never merge
        if big:
            rects = {"to": (-15, -15, 33, 12), "from": (-10, 2.5, 27, 12), "kiss": (19, 3, 11, 10)}
        if kiss_k != 1.0:                # storyboard v2: the bigger kiss gets a bigger bar
            rects["kiss"] = (13.5 + kiss_dx, 3.5, 19, 14)
        for key in ("to", "from", "kiss"):
            if key in bars:
                c.rectangle(*rects[key]); c.set_source_rgb(0.08, 0.08, 0.10); c.fill_preserve()
                c.set_source_rgb(*CREAM); c.set_line_width(1.4); c.stroke()
    else:
        if "to" in bars:
            c.rectangle(-15, -15, 31, 12); c.fill()
        if "from" in bars:
            c.rectangle(-10, 1, 25, 12); c.fill()
        if "kiss" in bars:
            c.rectangle(16, 3, 13, 10); c.fill()
    c.restore()
    if not kiss:
        pass
    elif not blank and "kiss" not in bars and kiss_k != 1.0:
        props.kiss(k, x + (23 + kiss_dx) * s, y + 10.5 * s, 0.26 * kiss_k * s, ang=-0.12 + rot)
    elif not blank and "kiss" not in bars:
        props.kiss(k, x + (24 if big else 21) * s, y + 9 * s, 0.26 * s)


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
    t = "UPTIMEZ INC. · CHARACTER MODEL SHEET · SECRET SANTA v2"
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
    for lx, lw, lab, col in ((318, 112, "OLD · MANDATORY FUN", GREY), (444, 160, "FINAL · lips rosy from shot 2", RED)):
        c.set_source_rgb(1, 1, 1); c.rectangle(lx, 104, lw, 16); c.fill()
        c.set_source_rgb(*col); c.set_line_width(1.2); c.rectangle(lx, 104, lw, 16); c.stroke()
        corp(c, lab, lx + 6, 116, 8.5, col=col, bold=True)
    corp(c, "Same Pam, same figure. Shot 1: natural lips. Shot 2 on: dusty rose. Never glamorous.", 290, 322, 9,
         col=GREY)

    # 3. faces by shot
    corp(c, "FACES, BY SHOT  (hurt, pride and disbelief must not look alike)", 284, 348, 10, bold=True)
    faces = [("neutral", (0.9, 0), None, "low", "O", "1: whisper"),
             ("hopeful", (-0.9, -0.1), "rose", "chain", None, "5: hopeful"),
             ("hurt", (0, 0), "rose", "chain", None, "7A: hurt"), ("decide", (0, 0), "rose", "chain", None, "7B: decides"),
             ("proud", (0, 0), "rose", "chain", None, "9: proud"), ("incredulous", (0, 0), "rose", "low", None, "15: no.")]
    for i, (f, lk, lp, g, m, lab) in enumerate(faces):
        x, y = 284 + i * 55.5, 354
        clip_box(x, y, 52.5, 92, lambda x=x, y=y, f=f, lk=lk, lp=lp, g=g, m=m: head(x + 26, y + 36, 0.62, f, lk, lp, g, m),
                 fill=ROSE_BG if f in ("hurt", "proud") else None, label=lab)
    corp(c, "MOUTHS, DUSTY ROSE  (two closed holds + speech)", 284, 466, 10, bold=True)
    mouths = [("rest", None, "rest"), ("pressed", None, "pressed"), ("neutral", "M", "M"), ("neutral", "E", "E"),
              ("neutral", "F", "F"), ("neutral", "O", "O"), ("neutral", "A", "A"), ("neutral", "C", "C")]
    for i, (f, m, lab) in enumerate(mouths):
        x, y = 284 + i * 41.5, 472
        clip_box(x, y, 39, 58, lambda x=x, y=y, f=f, m=m: head(x + 19, y - 6, 0.9, f, (0, 0), "rose", "chain", m),
                 fill=ROSE_BG if i < 2 else None, label=lab)

    # 4. poses
    corp(c, "POSES", 634, 92, 10, bold=True)
    poses = [(ps.POSE_WHISPER, "neutral", dict(look=(1, 0), lips=None, mouth="O", lean=4), "1: whisper"),
             ("stand", "neutral", dict(look=(-0.4, 0.2), apply=True), "2: puts it on"),
             (ps.POSE_GLASSES_OUT, "hopeful", dict(glasses="hand", look=(-1, 0)), "4: glasses off"),
             (ps.POSE_SHY, "hopeful", dict(glasses="chain", look=(-1, -0.1), lean=-4), "5: the chain"),
             (ps.POSE_SHY, "hurt", dict(glasses="chain"), "7A: sinks"),
             (ps.POSE_TABLE, "decide", dict(look=(0.2, 0.9)), "16: fresh tag")]
    for i, (pose, f, kw, lab) in enumerate(poses):
        x = 634 + i * 90.5
        def d(x=x, pose=pose, f=f, kw=kw, i=i, lab=lab):
            ps.pam(k, x + 44, 286 + (4 if lab.startswith("7A") else 0), 0.50, pose, f, seed=80 + i, **kw)
            if lab.startswith("5"):
                pop(k, "\U0001F497", x + 68, 126, 10)
            if lab.startswith("16"):
                gift_tag(c, x + 44, 238, 0.62, rot=0.05, blank=True)
        clip_box(x, 98, 87, 210, d, fill=ROSE_BG if i == 3 else None, label=lab)

    # 5. details
    corp(c, "DETAILS", 634, 348, 10, bold=True)
    def glasses_detail():
        head(676, 404, 0.82, "neutral", (0, 0), "rose", "low")
        head(762, 404, 0.82, "neutral", (0, 0), "rose", "chain")
    clip_box(634, 354, 170, 160, glasses_detail, label="on · one resting spot (5–14)")
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
        corp(c, "capped", 1002, 494, 7.5, col=GREY); corp(c, "open", 1038, 494, 7.5, col=GREY)
        gift_tag(c, 1124, 418, 1.2)
    clip_box(990, 354, 186, 160, tag_detail, fill=ROSE_BG, label="lipstick capped · open · her tag")

    # 6. 9:16 camera crops
    y0 = 562
    corp(c, "9:16 CROPS ON THE DRAWINGS  (stand-ins for the others)", 24, y0 - 6, 10, bold=True)
    W, H, G = 98, 174, 104

    def c1():
        x = 24
        ss.sofia(k, x + 92, y0 + 300, 0.82, "stand", "neutral", look=(-0.7, 0.1), badge=False, seed=91)
        ps.pam(k, x + 12, y0 + 312, 0.82, ps.POSE_WHISPER, "neutral", look=(1, 0), lips=None, mouth="O", lean=5,
               seed=92)
    clip_box(24, y0, W, H, c1, frame=True, label="1: whisper, leaning in")

    def c5():
        x = 24 + G
        dv.don(k, x + 82, y0 + 300, 0.70, seed=93)
        ps.pam(k, x + 26, y0 + 300, 0.70, ps.POSE_SHY, "hopeful", look=(1, -0.2), glasses="chain", seed=94)
        pop(k, "\U0001F497", x + 44, y0 + 30, 10)
    clip_box(24 + G, y0, W, H, c5, frame=True, label="5: to Don, one heart")

    def soft_sofia(x):
        def bg(lc):
            ss.sofia(Ctx(lc, 0), x + 82, y0 + 52 - SHY * 0.8, 0.8, "stand", "eyebrow", look=(0.8, 0), badge=False, seed=95)
        props.soft(c, bg, 1.8)

    def c7a():
        x = 24 + 2 * G
        soft_sofia(x)
        head(x + 40, y0 + 112, 1.05, "hurt", (0, 0), "rose", "chain")
    clip_box(24 + 2 * G, y0, W, H, c7a, frame=True, fill=None, label="7A: hurt (0.5 s)")

    def c7b():
        x = 24 + 3 * G
        soft_sofia(x)
        head(x + 40, y0 + 104, 1.05, "decide", (0.8, 0.4), "rose", "chain")
        c.set_source_rgb(0.78, 0.18, 0.20); c.rectangle(x + 70, y0 + 138, 40, 40); c.fill()     # her present
        c.set_source_rgb(*props.LIP_GOLD); c.rectangle(x + 86, y0 + 138, 6, 40); c.fill()
        c.set_source_rgb(*INK); c.set_line_width(1.6); c.rectangle(x + 70, y0 + 138, 40, 40); c.stroke()
    clip_box(24 + 3 * G, y0, W, H, c7b, frame=True, label="7B: on the present")

    def c9():
        x = 24 + 4 * G
        head(x + 49, y0 + 84, 1.12, "proud", glasses="chain")
        gift_tag(c, x + 52, y0 + 168, 1.25, rot=-0.04)
    clip_box(24 + 4 * G, y0, W, H, c9, frame=True, fill=ROSE_BG, label="9: proud, on the tag")

    def c15():
        x = 24 + 5 * G
        head(x + 49, y0 + 84, 1.12, "incredulous")
        gift_tag(c, x + 46, y0 + 168, 1.25, rot=0.06, bars=("from", "to", "kiss"))
    clip_box(24 + 5 * G, y0, W, H, c15, frame=True, label="15: barred tag. no.")

    # 7. the tag, before and after (for the robot's three stamps)
    corp(c, "THE TAG: HER COURAGE, THEN HR", 660, y0 - 6, 10, bold=True)
    boxed(c, 660, y0, 516, 174)
    states = [((), "8: signed + kissed"), (("from",), "11: sender (sensible)"), (("from", "to"), "12: recipient (absurd)"),
              (("from", "to", "kiss"), "13: the kiss (cruel)")]
    for i, (b, lab) in enumerate(states):
        x = 724 + i * 126
        gift_tag(c, x, y0 + 70, 1.35, rot=-0.05, bars=b)
        corp(c, lab, x - 54, y0 + 124, 9, col=GREY, bold=True)
    corp(c, "Printed TO: and FROM: stay readable under the bars, so you see exactly what was removed.", 672, y0 + 156,
         9, col=GREY)

    # 8. the glasses arc
    y1 = 790
    corp(c, "THE GLASSES ARC  (one gesture that tracks her through the film)", 24, y1 - 6, 10, bold=True)
    boxed(c, 24, y1, 1152, 180)
    arc = [("1–3", "stand", "neutral", dict(look=(-0.6, 0)), "on, low on the nose"),
           ("4", ps.POSE_GLASSES_OUT, "hopeful", dict(glasses="hand", look=(-1, 0)), "off, for Don"),
           ("5–8", ps.POSE_SHY, "hopeful", dict(glasses="chain", look=(-1, -0.1)), "on the chain"),
           ("9", ps.POSE_SHY, "proud", dict(glasses="chain"), "still on the chain"),
           ("15", "stand", "incredulous", dict(), "back on, to read the tag"),
           ("16", ps.POSE_TABLE, "decide", dict(look=(0.2, 0.9)), "fresh tag")]
    c.save(); c.rectangle(24, y1, 1152, 180); c.clip()
    for i, (sh, pose, f, kw, lab) in enumerate(arc):
        x = 110 + i * 192
        ps.pam(k, x, y1 + 160, 0.40, pose, f, seed=120 + i, **kw)
        if sh == "16":
            gift_tag(c, x, y1 + 128, 0.5, rot=0.05, blank=True)
        corp(c, sh, x + 44, y1 + 40, 16, col=brand.NAVY, bold=True)
        corp(c, lab, x + 44, y1 + 58, 9, col=GREY)
        if i < len(arc) - 1:
            c.set_source_rgb(*GREY); c.set_line_width(1.6)
            c.move_to(x + 120, y1 + 110); c.line_to(x + 150, y1 + 110); c.stroke()
            c.move_to(x + 144, y1 + 105); c.line_to(x + 150, y1 + 110); c.line_to(x + 144, y1 + 115); c.stroke()
    c.restore()

    # 9. notes
    y2 = 996
    corp(c, "NOTES", 24, y2, 10, bold=True)
    notes = ["Mandatory Fun office look unchanged: purple cardigan, bob with the grey lock, lanyard, keys.",
             "Dusty rose from shot 2: full lips when she speaks; closed holds use thin lips with an ink line.",
             "Glasses: on (1–3), out between her fingers (4), one resting spot on the chain (5–14), back on (15–16).",
             "7 is two beats: 7A hurt for about 0.5 s (brows up, eyes down, she sinks), 7B decides (eyes refocus).",
             "9: a shy closed smile, lids lowered on the tag, a blush. Her sweetest moment, so the stamp is unfair.",
             "15: further than her everyday look: lids down, heavy brows, a short flat mouth, a frozen stare at the tag.",
             "16: brave, not sad: she straightens, a fresh blank tag, the uncap (the loop). No second heart.",
             "One heart pop only, never glamorous, never tearful. The others on this sheet are stand-ins."]
    for i, n in enumerate(notes):
        corp(c, "·  " + n, 24 + (i % 2) * 588, y2 + 24 + (i // 2) * 30, 10, col=INK)
    flush(c)
    surf.write_to_png(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "pam_sheet_ss_v2.png")
