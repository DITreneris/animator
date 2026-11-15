"""v2 (pam_sheet_mf_v1.py writes v1 from pam_mf_v1.py). After the review: the cuff redrawn (props_mf v2),
the gaze progression and three smiles for 10 / 11A / 11B / 12, 11A and 11B labels, the cuff on the wrist nearest
Don, Don's stand-in cuffed with his arm down (no hand-holding read).
PAM model sheet for "Mandatory Fun" (pam_mf.py). Writes pam_sheet_mf_v2.png at 2400x1560
(drawn at 1200x780, 2x). Don appears only as a stand-in (Thanksgiving look) until his AI Police sheet exists."""
import sys
import math
import cairo
import kit
import brand
import pt42
import pam_tg as pt
import pam_mf as pm
import props_mf as pr
import don_tg as dt
import sofia_mf as sm
import emoji as _emoji
from kit import Ctx, INK
from charsheets import corp

W2, H2 = 1200, 780
GREY = (0.35, 0.40, 0.50)
ACCENT = (0.93, 0.91, 0.96)
PINK = (1.00, 0.91, 0.93)
LABELS = []
HY = pm.HY


def boxed(c, x, y, w, h, label=None, fill=(1, 1, 1)):
    c.set_source_rgb(*fill); c.rectangle(x, y, w, h); c.fill()
    c.set_source_rgb(0.85, 0.83, 0.78); c.set_line_width(1); c.rectangle(x, y, w, h); c.stroke()
    LABELS.append((x, y, w, h, label))


def flush(c):
    for x, y, w, h, label in LABELS:
        if label:
            c.set_source_rgb(1, 1, 1); c.rectangle(x + 1, y + h - 17, w - 2, 16); c.fill()
            corp(c, label, x + 6, y + h - 5, 9, col=GREY)
    LABELS.clear()


def pop(k, ch, x, y, r):
    """The emoji pop as it looks fully open (tg_sb.reaction at its hold)."""
    c = k.c
    c.set_source_rgba(0, 0, 0, 0.12); c.arc(x + 2, y + 3, r, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(*PINK); c.arc(x, y, r, 0, 2 * math.pi); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(1.6); c.stroke()
    _emoji.draw_emoji(c, ch, x, y, r * 1.25)


def table(c, x, y, w, h=60):
    c.set_source_rgb(0.55, 0.36, 0.22); c.rectangle(x, y, w, 14); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(1.6); c.rectangle(x, y, w, 14); c.stroke()
    c.set_source_rgb(0.98, 0.95, 0.88); c.rectangle(x, y + 14, w, h); c.fill()
    c.set_source_rgb(*INK); c.rectangle(x, y + 14, w, h); c.stroke()


def head_at(k, cx, cy, s, face, look=(0, 0), mouth=None, glasses="low"):
    pm.pam(k, cx, cy - HY * s, s, "stand", face, look=look, mouth=mouth, glasses=glasses)


def main(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "PAM", 68, 44, 28, bold=True)
    corp(c, "\"Mandatory Fun\"  ·  the human in the loop  ·  reading glasses on a chain", 140, 44, 13, col=GREY)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    t = "UPTIMEZ INC. · CHARACTER MODEL SHEET · MANDATORY FUN v2"
    corp(c, t, W2 - 24 - c.text_extents(t).x_advance, 30, 10, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()

    # 1. front
    c.set_source_rgb(*ACCENT); c.rectangle(24, 80, 240, 450); c.fill()
    pm.pam(k, 144, 512, 1.18, "stand", "neutral", seed=71)
    corp(c, "FRONT · OFFICE PURPLE, GLASSES LOW", 32, 524, 9, col=brand.NAVY, bold=True)

    # 2. office / Thanksgiving / Mandatory Fun
    corp(c, "OFFICE  ·  THANKSGIVING v2  ·  MANDATORY FUN", 284, 92, 10, bold=True)
    boxed(c, 284, 98, 330, 210)
    c.save(); c.rectangle(284, 98, 330, 210); c.clip()
    pt42.branded_person(k, "PAM", 345, 296, 0.56, seed=72)
    pt.pam(k, 449, 296, 0.56, "stand", "neutral", seed=72)
    pm.pam(k, 553, 296, 0.56, "stand", "neutral", seed=72)
    c.restore()
    corp(c, "Office purple on the Thanksgiving figure; no brooch. New: reading glasses on a chain.", 290, 322, 9,
         col=GREY)

    # 3. faces, one per beat
    corp(c, "FACES, BY SHOT  (deadpan base; one leak in 4; loud only in 9)", 284, 348, 10, bold=True)
    faces = [("read", (0, 1), "low", "2: reading"), ("peer", (0, 0), "low", "4: the leak"),
             ("hopeful", (0.6, 0), "low", "5: hopeful"), ("fade", (0.6, 0), "low", "5: it fades"),
             ("approve", (0, 0), "flash", "9: APPROVED!")]
    for i, (e, lk, g, lab) in enumerate(faces):
        x, y = 284 + i * 66, 354
        boxed(c, x, y, 63, 92, lab, fill=(0.99, 0.93, 0.92) if e == "peer" else (1, 1, 1))
        c.save(); c.rectangle(x, y, 63, 92); c.clip()
        head_at(k, x + 31, y + 40, 0.4, e, lk, glasses=g)
        if e == "peer":
            pop(k, "\U0001F497", x + 50, y + 14, 10)
        c.restore()
    corp(c, "THREE SMILES + THE GAZE  (down · away · at Don · straight out)", 284, 466, 9,
         col=GREY, bold=True)
    row2 = [("quiet", (0, 0), "low", None, "10: private"), ("avert", (0, 0), "up", None, "11A: away"),
            ("dinner", (0, 0), "up", None, "11B: at Don"), ("dinner", (0, 0), "up", "O", "11B: \"So...\""),
            ("happy", (0, 0), "low", None, "12: full")]
    for i, (e, lk, g, m, lab) in enumerate(row2):
        x, y = 284 + i * 66, 472
        boxed(c, x, y, 63, 60, lab, fill=(0.93, 0.98, 0.93) if e == "happy" else (1, 1, 1))
        c.save(); c.rectangle(x, y, 63, 60); c.clip()
        head_at(k, x + 31, y + 22, 0.42, e, lk, mouth=m, glasses=g)
        c.restore()

    # 4. poses
    corp(c, "POSES  (Don's toy cuff on the wrist nearest him, screen left, from shot 10)", 634, 92, 10, bold=True)
    poses = [(pm.POSE_FINGER, "hopeful", dict(finger=True), "5: one finger"),
             (pm.POSE_APPROVE, "approve", dict(glasses="flash"), "9: APPROVED!"),
             (pm.POSE_CUFF, "quiet", dict(cuff="L", cuff_open=0.35), "10: the 2nd cuff"),
             (pm.POSE_GLASSES, "avert", dict(glasses="up", cuff="L", finger="bridge"), "11A: glasses up"),
             (pm.POSE_SHY, "dinner", dict(glasses="up", cuff="L", lean=-4), "11B: \"So... dinner?\""),
             ("stand", "happy", dict(cuff="L"), "12: fun detected")]
    for i, (p, f, kw, lab) in enumerate(poses):
        x = 634 + i * 91
        hot = f in ("approve", "happy")
        boxed(c, x, 98, 87, 210, lab, fill=(0.93, 0.98, 0.93) if f == "happy" else
              ((1.0, 0.97, 0.88) if f == "approve" else (1, 1, 1)))
        c.save(); c.rectangle(x, 98, 87, 210); c.clip()
        o = pm.pam(k, x + 44, 290, 0.48, p, f, look=(0.7, 0), seed=80 + i, **kw)
        if "cuff" in o:                                    # the chain runs off toward Don
            cx_, cy_ = o["cuff"]
            pr.chain(k, cx_, cy_, x - 6, cy_ + 12, 0.48, sag=0.25)
            if f == "quiet":
                pr.click(k, cx_ + 10, cy_ - 8, 0.7)
        if f == "approve":
            c.set_source_rgb(*pr.TOY_YELLOW_DARK); c.set_line_width(2); c.set_line_cap(1)
            hx, hy = o["hands"][1]
            for a in (-0.6, -0.1, 0.4):
                c.move_to(hx + 9 * math.sin(a), hy - 9 * math.cos(a)); c.line_to(hx + 17 * math.sin(a), hy - 17 * math.cos(a))
                c.stroke()
        c.restore()

    # 5. details
    corp(c, "DETAILS", 634, 348, 10, bold=True)
    boxed(c, 634, 354, 170, 178, "half-moons low, eyes over the top")
    c.save(); c.rectangle(634, 354, 170, 160); c.clip()
    head_at(k, 719, 440, 1.05, "peer", (0.3, -0.5))
    c.restore()
    boxed(c, 812, 354, 170, 178, "low  ·  flash (9)  ·  straightened (11)")
    c.save(); c.rectangle(812, 354, 170, 160); c.clip()
    for j, (g, f) in enumerate((("low", "neutral"), ("flash", "approve"), ("up", "dinner"))):
        c.save(); c.rectangle(812 + j * 57, 354, 56, 160); c.clip()
        head_at(k, 840 + j * 57, 425, 0.5, f, (0, 0), glasses=g)
        c.restore()
    c.restore()
    boxed(c, 990, 354, 186, 178, "ring round the wrist, hinge, keyhole, loop")
    c.save(); c.rectangle(990, 354, 186, 160); c.clip()
    kit.cut(k, [(1030, 412), (1100, 412), (1100, 440), (1030, 440)], pm.PURPLE, shadow=False, lw=2)   # sleeve
    kit.cut(k, [(1100, 417), (1126, 417), (1126, 435), (1100, 435)], pm.SKIN, shadow=False, lw=2)     # wrist
    kit.ellipse(k, 1134, 426, 14, 14, pm.SKIN, 5, shadow=False, lw=2)                               # hand
    lx, ly = pr.cuff(k, 1113, 426, 1.35, math.pi / 2, loop_side=1)
    pr.chain(k, lx, ly, 996, ly + 26, 1.35, sag=0.25)
    c.restore()

    # 6. phone-size check: shot 2, shot 4, shots 11-12 (Don as a stand-in)
    corp(c, "PHONE-SIZE CHECK  (2: reading with Sofía  ·  4: the leak at Don  ·  12: chained together, she's the happy one)",
         24, 556, 10, bold=True)
    c.set_source_rgb(*kit.WALL); c.rectangle(24, 562, 590, 190); c.fill()
    c.save(); c.rectangle(24, 562, 590, 190); c.clip()
    sm.sofia(k, 74, 760, 0.42, "write", "neutral", look=(0, 0.6), seed=95)
    pm.pam(k, 160, 760, 0.42, pm.POSE_TABLE, "read", seed=96)
    dt.don(k, 268, 770, 0.42, "stand", "grin", look=(-0.8, 0.2), seed=98)
    pm.pam(k, 350, 760, 0.42, "stand", "peer", look=(-0.8, -0.5), seed=97)
    pop(k, "\U0001F497", 372, 616, 13)
    d = dt.don(k, 470, 770, 0.42, "stand", "collapse", look=(0.6, 0.2), seed=100)
    o = pm.pam(k, 570, 760, 0.42, pm.POSE_TABLE, "happy", seed=99)
    c.restore()
    table(c, 24, 700, 590)
    c.save(); c.rectangle(24, 562, 590, 190); c.clip()        # the cuffed hands rest on the table, chain between
    dhx, phx = 470 + 22, 570 - 22
    for hx_ in (dhx, phx):
        kit.ellipse(k, hx_, 703, 4.2, 4.2, pm.SKIN, 7, shadow=False, lw=1.2)
    a_ = pr.cuff(k, dhx - 3, 697, 0.5, 0.0, loop_side=1)
    b_ = pr.cuff(k, phx + 3, 697, 0.5, 0.0, loop_side=-1)
    pr.chain(k, a_[0], a_[1], b_[0], b_[1], 0.5, sag=0.15)
    c.restore()
    corp(c, "Don: stand-in (his AI Police sheet is next)", 30, 746, 8, col=GREY)

    # 7. notes
    corp(c, "NOTES", 634, 556, 10, bold=True)
    notes = ["Kept: office purple on the Thanksgiving figure, grey lock, calm lid, glasses low on a chain.",
             "Cuff: a ring round the wrist nearest Don, hinge, keyhole, a loop the chain hangs from.",
             "Gaze tells it: 4 at Don over the glasses (wider eyes, one corner up), the heart pop on top.",
             "10 down at her wrist, a private smile. 11A glasses up, eyes away. 11B sideways at Don.",
             "Three smiles: private (10), shy half with pink cheeks (11B), full only for the scan (12).",
             "Loud once: \"APPROVED!\" (9). Never sly: no raised brow, no grin before 12."]
    for i, n in enumerate(notes):
        corp(c, "·  " + n, 634, 580 + i * 24, 11, col=INK)
    flush(c)
    surf.write_to_png(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "pam_sheet_mf_v2.png")
