"""SOFÍA model sheet for the Christmas special "Happy Compliance" (sofia_xmas.py). Writes sofia_sheet_xmas_v1.png
at 2400x1560 (drawn at 1200x780, 2x). The v4 office look (sofia_v4.py) is shown beside it for comparison."""
import sys
import cairo
import kit
import brand
import sofia_v4 as sf4
import sofia_xmas_v2 as sx
from kit import Ctx, INK
from charsheets import corp

W2, H2 = 1200, 780
GREY = (0.35, 0.40, 0.50)
ACCENT = (0.80, 0.90, 0.86)
WALL = kit.WALL
LABELS = []


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


def head_at(k, cx, cy, s, kind, look=(0, 0)):
    hy = -300 * sx.H + 78 - 44
    sx.sofia(k, cx, cy - hy * s, s, "stand", kind, look=look, badge=False)


def main(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "SOFÍA", 68, 44, 28, bold=True)
    corp(c, "Christmas special \"Happy Compliance\"  ·  main character  ·  glamorous nurse costume", 172, 44, 13, col=GREY)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    t = "UPTIMEZ INC. · CHARACTER MODEL SHEET · XMAS v2"
    corp(c, t, W2 - 24 - c.text_extents(t).x_advance, 30, 10, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()

    # 1. front, full body with the two ornaments
    c.set_source_rgb(*ACCENT); c.rectangle(24, 80, 240, 450); c.fill()
    sx.sofia(k, 144, 512, 1.18, "hold2", "neutral", seed=71)
    corp(c, "FRONT · HOLDING THE TWO ORNAMENTS", 32, 524, 9, col=brand.NAVY, bold=True)

    # 2. office look vs costume
    corp(c, "OFFICE LOOK (v4)  AND  COSTUME", 284, 92, 10, bold=True)
    boxed(c, 284, 98, 330, 210)
    c.save(); c.rectangle(284, 98, 330, 210); c.clip()
    sf4.sofia(k, 370, 296, 0.6, "stand", "neutral", seed=73, folder="none")
    sx.sofia(k, 528, 296, 0.6, "stand", "neutral", seed=73)
    c.restore()
    corp(c, "Same face, hair, hoops and height. v2: waist, hips, shaped legs, heels.", 290, 322, 9, col=GREY)

    # 3. expressions
    corp(c, "EXPRESSIONS  (\"furious\" is new)", 284, 348, 10, bold=True)
    exprs = [("neutral", (0, 0)), ("unimpressed", (0.8, 0)), ("horrified", (0.8, 0)),
             ("furious", (0.8, 0)), ("knowing", (0.7, 0)), ("closed", (0, 0))]
    for i, (e, lk) in enumerate(exprs):
        x, y = 284 + (i % 3) * 112, 354 + (i // 3) * 92
        boxed(c, x, y, 106, 86, e, fill=(1, 0.99, 0.97) if e != "furious" else (0.99, 0.93, 0.92))
        c.save(); c.rectangle(x, y, 106, 86); c.clip()
        head_at(k, x + 53, y + 44, 0.44, e, lk)
        c.restore()

    # 4. poses
    corp(c, "POSES", 634, 92, 10, bold=True)
    poses = [("hang", "smile", "decorating (before Don)"), ("hold2", "unimpressed", "shots 1-4"),
             ("fists", "furious", "shot 5"), ("give", "knowing", "shot 10: the handoff")]
    for i, (p, f, lab) in enumerate(poses):
        x = 634 + i * 137
        boxed(c, x, 98, 131, 210, lab)
        c.save(); c.rectangle(x, 98, 131, 210); c.clip()
        sx.sofia(k, x + (44 if p == "give" else 66), 290, 0.56, p, f, look=(0.8, 0), seed=80 + i)
        c.restore()

    # 5. details
    corp(c, "DETAILS", 634, 348, 10, bold=True)
    boxed(c, 634, 354, 170, 178, "cap: red heart, not a cross")
    c.save(); c.rectangle(634, 354, 170, 160); c.clip()
    head_at(k, 719, 500, 1.25, "neutral")
    c.restore()
    boxed(c, 812, 354, 170, 178, "ornament: big, glossy, gold cap")
    sx.ornament(k, 897, 448, 52, 90)
    boxed(c, 990, 354, 186, 178, "collar, stethoscope, belt, badge")
    c.save(); c.rectangle(990, 354, 186, 160); c.clip()
    sx.sofia(k, 1083, 615, 0.9, "stand", "neutral", seed=91)
    c.restore()

    # 6. phone-size check on the office wall colour
    corp(c, "PHONE-SIZE CHECK  (as small as she gets in the wide shot, on the wall colour)", 24, 556, 10, bold=True)
    c.set_source_rgb(*WALL); c.rectangle(24, 562, 590, 190); c.fill()
    c.set_source_rgb(*kit.FLOOR); c.rectangle(24, 722, 590, 30); c.fill()
    for i, (p, f) in enumerate((("hold2", "unimpressed"), ("hold2", "horrified"), ("fists", "furious"), ("give", "knowing"))):
        sx.sofia(k, 100 + i * 140, 736, 0.42, p, f, look=(0.8, 0), seed=95 + i)
    # 7. notes
    corp(c, "NOTES", 634, 556, 10, bold=True)
    notes = ["White dress, red trim, red belt with the gold buckle from her office belt.",
             "Cap carries a red heart: the red cross emblem is legally protected.",
             "Hoops, red lips and winged liner are unchanged: she must read as Sofía at a glance.",
             "The camera treats her as in every episode; the joke is on Don and the robot.",
             "The two ornaments hang from her fingers at hip level, apart, so they read as baubles.",
             "No lines in this film: unimpressed -> horrified -> furious -> knowing carry her part."]
    for i, n in enumerate(notes):
        corp(c, "·  " + n, 634, 580 + i * 24, 11, col=INK)
    flush(c)
    surf.write_to_png(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "sofia_sheet_xmas_v2.png")
