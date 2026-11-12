"""DON model sheet v4 for the next film, drawn with don_v4.py (open navy fleece vest with the company
mark, white shirt, khakis, staff badge, the ketchup stain nobody mentions). The older DON sheet
(characters/uptimez-don-sheet.png, charsheets.py) is kept.
Writes don_sheet_v4.png at 2400x1560 (drawn at 1200x780, 2x)."""
import sys
import cairo
import kit
import brand
import pt42
import don_v4 as dv
import sofia_v4 as sf
from kit import Ctx, INK
from charsheets import corp, wrap
from sofia_sheet_v4 import boxed, flush_labels

W2, H2 = 1200, 780
GREY = (0.35, 0.40, 0.50)
ACCENT = (0.80, 0.86, 0.93)          # pale blue panel, so the navy vest and the red stain read
HY = -300 * kit.PEOPLE["DON"]["h"] + 78 - 44


def head_at(k, cx, cy, s, face, look=(0, 0), pose="stand"):
    dv.don(k, cx, cy - HY * s, s, pose, face, look=look)


def main(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "DON", 68, 44, 28, bold=True)
    corp(c, "Team lead  ·  approves everything without looking  ·  dresses like a CEO", 140, 44, 13, col=GREY)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    tw = c.text_extents("UPTIMEZ INC. · CHARACTER MODEL SHEET · v4").x_advance
    corp(c, "UPTIMEZ INC. · CHARACTER MODEL SHEET · v4", W2 - 24 - tw, 30, 10, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()

    # 1. front, full body
    c.set_source_rgb(*ACCENT); c.rectangle(24, 80, 240, 450); c.fill()
    dv.don(k, 144, 512, 1.18, "stand", "neutral", seed=71)
    corp(c, "FRONT · NEUTRAL", 32, 524, 9, col=brand.NAVY, bold=True)

    # 2. height line-up with Sofía v4
    corp(c, "HEIGHT LINE-UP", 284, 92, 10, bold=True)
    boxed(c, 284, 98, 330, 210)
    c.save(); c.rectangle(284, 98, 330, 210); c.clip()
    c.set_source_rgb(0.85, 0.83, 0.78); c.set_line_width(1)
    for gy in range(118, 300, 30):
        c.move_to(284, gy); c.line_to(614, gy); c.stroke()
    pt42.branded_person(k, "PAM", 350, 296, 0.6, seed=72)
    sf.sofia(k, 449, 296, 0.6, "stand", "neutral", seed=73)
    dv.don(k, 548, 296, 0.6, seed=74)
    c.restore()
    corp(c, "PAM 1.02  ·  SOFÍA 1.02  ·  DON 1.12", 290, 322, 9, col=GREY)

    # 3. expressions
    corp(c, "EXPRESSIONS", 284, 348, 10, bold=True)
    for i, (e, lk) in enumerate([("neutral", (0, 0)), ("smug", (0, 0)), ("happy", (0, 0)),
                                 ("pleased", (0, 0)), ("shock", (0, 0)), ("confused", (0.4, 0))]):
        x, y = 284 + (i % 3) * 112, 354 + (i // 3) * 92
        boxed(c, x, y, 106, 86, e, fill=(1, 0.99, 0.97) if e != "smug" else (0.93, 0.95, 0.98))
        c.save(); c.rectangle(x, y, 106, 74); c.clip()
        head_at(k, x + 53, y + 36, 0.5, e, look=lk)
        c.restore()

    # 4. poses
    corp(c, "POSES", 634, 92, 10, bold=True)
    for i, (ps, fk, lbl) in enumerate([("stand", "smug", "approves"), ("point_l", "happy", "\"Pam?\""),
                                       ("pleased", "pleased", "\"Perfect.\""), ("type", "neutral", "at his desk"),
                                       ("shock", "shock", "caught")]):
        x = 634 + i * 110
        boxed(c, x, 98, 104, 210, lbl)
        c.save(); c.rectangle(x, 98, 104, 196); c.clip()
        dv.don(k, x + 52, 286, 0.5, ps, fk, seed=80 + i)
        c.restore()

    # 5. the stain at phone size
    corp(c, "THE KETCHUP STAIN", 634, 348, 10, bold=True)
    for i, (s, lbl) in enumerate([(1.9, "close-up"), (1.0, "medium"), (0.55, "wide (still reads)")]):
        x = 634 + i * 112
        boxed(c, x, 354, 106, 130, lbl, fill=kit.WALL)
        c.save(); c.rectangle(x, 354, 106, 116); c.clip()
        stain_y = HY + 44 + 92                         # stain relative to the head centre
        dv.don(k, x + 53, 420 - stain_y * s, s, "stand", "smug")
        c.restore()
    wrap(c, "A bottle squiggle, a smear and a dot on the white shirt between the open vest panels. "
            "Always there, never mentioned; tomato red, warmer than blood.", 634, 504, 10, 330)

    # 6. old vs new
    corp(c, "WHAT CHANGED", 984, 348, 10, bold=True)
    boxed(c, 984, 354, 92, 130, "Day One", fill=(1, 0.99, 0.97))
    c.save(); c.rectangle(984, 354, 92, 116); c.clip()
    pt42.branded_person(k, "DON", 1030, 520, 0.5, seed=90)
    c.restore()
    boxed(c, 1084, 354, 92, 130, "next film", fill=(0.93, 0.95, 0.98))
    c.save(); c.rectangle(1084, 354, 92, 116); c.clip()
    dv.don(k, 1130, 520, 0.5, seed=91)
    c.restore()

    # 7. colours
    corp(c, "COLOURS", 24, 560, 10, bold=True)
    sw = [("skin", kit.PEOPLE["DON"]["skin"]), ("vest", dv.VEST), ("shirt", dv.SHIRT), ("khakis", dv.KHAKI),
          ("tufts", kit.PEOPLE["DON"]["hair"]), ("ketchup", dv.KETCHUP), ("belt", dv.BELT), ("zip", dv.ZIP)]
    for i, (lbl, col) in enumerate(sw):
        x, y = 24 + (i % 4) * 66, 568 + (i // 4) * 84
        c.set_source_rgb(*col); c.rectangle(x, y, 58, 40); c.fill()
        c.set_source_rgb(*INK); c.set_line_width(1); c.rectangle(x, y, 58, 40); c.stroke()
        corp(c, lbl, x, y + 54, 9, bold=True)
        corp(c, "#%02X%02X%02X" % tuple(int(v * 255) for v in col), x, y + 66, 9, col=GREY)

    # 8. notes
    corp(c, "WHO HE IS", 300, 560, 10, bold=True)
    wrap(c, "The team lead who wants to look like a tech CEO: company fleece vest, lanyard energy, approves "
            "everything without reading it. He wants Sofía's attention and has no idea about the ketchup.",
         300, 578, 11, 420)
    corp(c, "COSTUME", 300, 650, 10, bold=True)
    wrap(c, "Open navy fleece vest with the UptimeZ mark, white shirt, no tie, khakis with a belt, staff badge "
            "on the vest. The robot copied his old red tie; whether DON 2.0 updates its outfit is a story choice.",
         300, 668, 11, 420)
    corp(c, "VOICE", 760, 560, 10, bold=True)
    wrap(c, "Smooth, slow, self-satisfied (Kokoro am_onyx); nods along with his own lines.", 760, 578, 11, 410)
    corp(c, "STYLE RULES", 760, 626, 10, bold=True)
    wrap(c, "Same head, height and face as before; the vest panels never cover the stain, and the badge sits "
            "clear of his arms in every pose.", 760, 644, 11, 410)
    corp(c, "Drawn with don_v4.py, the same code the film will use.", 24, 762, 9, col=GREY)
    flush_labels(c)
    surf.write_to_png(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "don_sheet_v4.png")
