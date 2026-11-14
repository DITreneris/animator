"""PAM model sheet for the Christmas special "Happy Compliance" (pam_xmas.py): her first full-size figure.
Writes pam_sheet_xmas_v1.png at 2400x1560 (drawn at 1200x780, 2x)."""
import sys
import cairo
import kit
import brand
import pam_xmas as px
import don_xmas as dx
import sofia_xmas as sx
from kit import Ctx, INK
from charsheets import corp
from sofia_sheet_v4 import boxed, flush_labels

W2, H2 = 1200, 780
GREY = (0.35, 0.40, 0.50)
ACCENT = (0.88, 0.85, 0.94)
HY = -300 * kit.PEOPLE["PAM"]["h"] + 78 - 44


def head_at(k, cx, cy, s, face, mask, look=(0, 0)):
    px.pam(k, cx, cy - HY * s, s, "stand", face, look=look, mask=mask, cape=False)


def main(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "PAM", 68, 44, 28, bold=True)
    corp(c, "Christmas special \"Happy Compliance\"  ·  a five-minute superhero  ·  the only one who acts", 140, 44, 13, col=GREY)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    t = "UPTIMEZ INC. · CHARACTER MODEL SHEET · XMAS v2"
    corp(c, t, W2 - 24 - c.text_extents(t).x_advance, 30, 10, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()

    # 1. front: the payoff stance
    c.set_source_rgb(*ACCENT); c.rectangle(24, 80, 240, 450); c.fill()
    c.save(); c.rectangle(24, 80, 240, 450); c.clip()
    px.pam(k, 144, 512, 1.22, px.POSE_HERO, "neutral", mask="down", seed=71, **px.HERO)
    c.restore()
    corp(c, "FRONT · MASK DOWN (SHOT 10)", 32, 524, 9, col=brand.NAVY, bold=True)

    # 2. the cast line-up
    corp(c, "HEIGHT LINE-UP", 284, 92, 10, bold=True)
    boxed(c, 284, 98, 330, 210)
    c.save(); c.rectangle(284, 98, 330, 210); c.clip()
    sx.sofia(k, 350, 296, 0.6, "hold2", "unimpressed", seed=73)
    px.pam(k, 449, 296, 0.6, px.POSE_THERMOS, "neutral", mask="neck", thermos_in_hand=True, seed=72)
    dx.don(k, 548, 296, 0.6, dx.POSE_RAZOR, "smug", seed=74)
    c.restore()
    corp(c, "SOFÍA 1.02  ·  PAM 1.02  ·  DON 1.12", 290, 322, 9, col=GREY)

    # 3. expressions, mask up and down
    corp(c, "EXPRESSIONS  (deadpan is her default)", 284, 348, 10, bold=True)
    for i, (e, m, lab) in enumerate([("neutral", "neck", "deadpan"), ("hollow", "neck", "dead inside"),
                                     ("squint", "neck", "annoyed"), ("shock", "neck", "the line"),
                                     ("neutral", "down", "mask down"), ("squint", "down", "mask down, angry")]):
        x, y = 284 + (i % 3) * 112, 354 + (i // 3) * 92
        boxed(c, x, y, 106, 86, lab, fill=(1, 0.99, 0.97) if m == "neck" else (0.95, 0.93, 0.99))
        c.save(); c.rectangle(x, y, 106, 70); c.clip()
        head_at(k, x + 53, y + 30, 0.44, e, m)
        c.restore()

    # 4. poses in story order
    corp(c, "POSES", 634, 92, 10, bold=True)
    poses = [(px.POSE_THERMOS, "neutral", "neck", True, False, "shots 1-2: deadpan"),
             (px.POSE_FISTS, "squint", "neck", False, False, "shot 5: fists"),
             (px.POSE_TAKE, "neutral", "down", False, True, "shot 10: takes it"),
             (px.POSE_HERO, "neutral", "down", False, False, "shot 10: the hero")]
    for i, (ps, fk, m, th, orn, lbl) in enumerate(poses):
        x = 634 + i * 137
        boxed(c, x, 98, 131, 210, lbl)
        c.save(); c.rectangle(x, 98, 131, 194); c.clip()
        px.pam(k, x + (54 if orn else 66), 290, 0.54, ps, fk, mask=m, thermos_in_hand=th, orn=orn, seed=80 + i,
               **(px.HERO if ps == px.POSE_HERO else {}))
        c.restore()

    # 5. details
    corp(c, "DETAILS", 634, 348, 10, bold=True)
    boxed(c, 634, 354, 170, 178, "mask: at her neck, then on")
    c.save(); c.rectangle(634, 354, 170, 162); c.clip()
    head_at(k, 678, 418, 0.62, "neutral", "neck")
    head_at(k, 762, 418, 0.62, "neutral", "down")
    c.restore()
    boxed(c, 812, 354, 170, 178, "towel cape, safety pin, \"P\"")
    c.save(); c.rectangle(812, 354, 170, 162); c.clip()
    px.pam(k, 897, 690, 1.25, "stand", "neutral", mask=None)
    c.restore()
    boxed(c, 990, 354, 186, 178, "cardigan buttoned one hole off; keys")
    c.save(); c.rectangle(990, 354, 186, 162); c.clip()
    px.pam(k, 1083, 590, 1.3, "stand", "neutral", mask=None, cape=False)
    c.restore()

    # 6. phone-size check
    corp(c, "PHONE-SIZE CHECK  (as small as she gets in the wide shot, on the wall colour)", 24, 556, 10, bold=True)
    c.set_source_rgb(*kit.WALL); c.rectangle(24, 562, 590, 190); c.fill()
    c.set_source_rgb(*kit.FLOOR); c.rectangle(24, 722, 590, 30); c.fill()
    for i, (ps, fk, m, th, orn) in enumerate(((px.POSE_THERMOS, "neutral", "neck", True, False),
                                               (px.POSE_FISTS, "squint", "neck", False, False),
                                               (px.POSE_TAKE, "neutral", "down", False, True),
                                               (px.POSE_HERO, "neutral", "down", False, False))):
        px.pam(k, 100 + i * 140, 736, 0.42, ps, fk, mask=m, thermos_in_hand=th, orn=orn, seed=95 + i,
               **(px.HERO if ps == px.POSE_HERO else {}))

    # 7. notes
    corp(c, "NOTES", 634, 556, 10, bold=True)
    notes = ["Her clothes are the most sensible outfit in the building: that is the joke.",
             "Purple cardigan buttoned one hole off (one side hangs low), lanyard with too many keys.",
             "Cape: a dark-blue bath towel, stripes and fringe, corners safety-pinned at the neck.",
             "Mask: cardboard, taped, uneven holes. Hangs at her neck until shot 10, then goes on.",
             "A paper \"P\" taped on crooked. No emblem or ears from any real superhero.",
             "Shot 10: feet wide, elbows out, towel spread, chin up; the face stays flat.",
             "Line: \"Human in the loop.\" A superhero body, a compliance-officer face."]
    for i, n in enumerate(notes):
        corp(c, "·  " + n, 634, 580 + i * 24, 11, col=INK)
    flush_labels(c)
    surf.write_to_png(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "pam_sheet_xmas_v2.png")
