"""SOFÍA model sheet v4 for the next film, drawn with sofia_v4.py (glow-up: liner and lashes, fuller hair
with shine, fuller glossy red lips, 1.6x hoops, teal wrap blouse with a belt). sofia_sheet.py (v2) is kept.
Writes sofia_sheet_v4.png at 2400x1560 (drawn at 1200x780, 2x)."""
import sys
import cairo
import kit
import brand
import pt42
import sofia_v4 as sf
import sofia as sf_v2
import don_v4
from kit import Ctx, INK
from charsheets import corp, wrap

W2, H2 = 1200, 780
GREY = (0.35, 0.40, 0.50)
ACCENT = (0.93, 0.80, 0.62)        # v4 panel: warm sand, so the teal blouse, red and gold pop


def boxed(c, x, y, w, h, label=None, fill=(1, 1, 1)):
    c.set_source_rgb(*fill); c.rectangle(x, y, w, h); c.fill()
    c.set_source_rgb(0.85, 0.83, 0.78); c.set_line_width(1); c.rectangle(x, y, w, h); c.stroke()
    LABELS.append((x, y, w, h, label))


LABELS = []


def flush_labels(c):
    for x, y, w, h, label in LABELS:
        if label:
            c.set_source_rgb(1, 1, 1); c.rectangle(x + 1, y + h - 17, w - 2, 16); c.fill()
            corp(c, label, x + 6, y + h - 5, 9, col=GREY)
    LABELS.clear()


def head_at(k, cx, cy, s, kind, look=(0, 0), lag=(0, 0)):
    """Sofía with her head centred at (cx, cy)."""
    hy = -300 * sf.H + 78 - 44
    sf.sofia(k, cx, cy - hy * s, s, "stand", kind, look=look, lag=lag, badge=False, folder="none")


def main(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "SOFÍA", 68, 44, 28, bold=True)
    corp(c, "New hire, about 30  ·  main character  ·  charming, and she knows it", 172, 44, 13, col=GREY)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    tw = c.text_extents("UPTIMEZ INC. · CHARACTER MODEL SHEET · v4").x_advance
    corp(c, "UPTIMEZ INC. · CHARACTER MODEL SHEET · v4", W2 - 24 - tw, 30, 10, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()

    # 1. front, full body
    c.set_source_rgb(*ACCENT); c.rectangle(24, 80, 240, 450); c.fill()
    sf.sofia(k, 144, 512, 1.18, "tuck", "neutral", seed=71)
    corp(c, "FRONT · NEUTRAL · FOLDER TUCKED", 32, 524, 9, col=brand.NAVY, bold=True)

    # 2. height line-up
    corp(c, "HEIGHT LINE-UP", 284, 92, 10, bold=True)
    boxed(c, 284, 98, 330, 210)
    c.save(); c.rectangle(284, 98, 330, 210); c.clip()
    c.set_source_rgb(0.85, 0.83, 0.78); c.set_line_width(1)
    for gy in range(118, 300, 30):
        c.move_to(284, gy); c.line_to(614, gy); c.stroke()
    pt42.branded_person(k, "PAM", 350, 296, 0.6, seed=72)
    sf.sofia(k, 449, 296, 0.6, "stand", "neutral", seed=73)
    don_v4.don(k, 548, 296, 0.6, seed=74)
    c.restore()
    corp(c, "PAM 1.02  ·  SOFÍA 1.02 (same as Pam)  ·  DON 1.12", 290, 322, 9, col=GREY)

    # 3. expressions
    corp(c, "EXPRESSIONS  (\"eyebrow\" is her signature)", 284, 348, 10, bold=True)
    exprs = [("neutral", (0, 0)), ("flirty", (0.6, 0)), ("wink", (0, 0)), ("eyebrow", (0.4, 0)),
             ("surprised", (0, 0)), ("knowing", (-0.5, 0))]
    for i, (e, lk) in enumerate(exprs):
        x, y = 284 + (i % 3) * 112, 354 + (i // 3) * 92
        boxed(c, x, y, 106, 86, e, fill=(1, 0.99, 0.97) if e != "eyebrow" else (0.93, 0.97, 0.96))
        c.save(); c.rectangle(x, y, 106, 74); c.clip()
        head_at(k, x + 53, y + 34, 0.5, e, look=lk)
        c.restore()

    # 4. poses
    corp(c, "POSES FOR THE BEATS", 634, 92, 10, bold=True)
    poses = [("tuck", "flirty", (0.6, 0), (0, 0), "1 to Don"), ("twirl", "smile", (0.6, 0), (0, 0), "2-3 hair twirl"),
             ("hip", "wink", (0.6, 0), (6, 2), "3 the wink"),
             ("offer", "smile", (0.6, 0.3), (0, 0), "6 offers folder"), ("cross", "eyebrow", (1, 0), (0, 0), "8 the eyebrow")]
    for i, (ps, fk, lk, lg, lbl) in enumerate(poses):
        x = 634 + i * 110
        boxed(c, x, 98, 104, 210, lbl)
        c.save(); c.rectangle(x, 98, 104, 196); c.clip()
        sf.sofia(k, x + 52, 286, 0.52, ps, fk, look=lk, lag=lg, seed=80 + i, badge=False)
        c.restore()

    # 5. shots she gets (9:16 frames)
    corp(c, "SHOTS (9:16)", 634, 348, 10, bold=True)
    for i, (lbl, s, hx, hy) in enumerate([("medium, beat 1", 0.62, 54, 92), ("close-up, beats 5 and 8", 1.0, 52, 102)]):
        x = 634 + i * 120
        boxed(c, x, 354, 108, 180, lbl, fill=kit.WALL)
        c.save(); c.rectangle(x, 354, 108, 166); c.clip()
        fk, lk = ("flirty", (0.6, 0)) if i == 0 else ("eyebrow", (0.6, 0))
        if i == 0:
            hy0 = -300 * sf.H + 78 - 44
            sf.sofia(k, x + hx, 354 + hy - hy0 * s, s, "tuck", fk, look=lk, seed=90, badge=True)
        else:
            head_at(k, x + hx, 354 + hy, s, fk, look=lk)
        c.restore()
    # hair and hoop lag
    corp(c, "WHAT CHANGED: v2 TO v4", 880, 348, 10, bold=True)
    hy2 = -300 * sf_v2.H + 78 - 44
    for i, (mod, lbl) in enumerate([(sf_v2, "v2 (Day One)"), (sf, "v4 (next film)")]):
        x = 880 + i * 150
        boxed(c, x, 354, 144, 126, lbl, fill=(0.93, 0.97, 0.96) if i else (1, 0.99, 0.97))
        c.save(); c.rectangle(x, 354, 144, 112); c.clip()
        mod.sofia(k, x + 72, 408 - hy2 * 0.62, 0.62, "stand", "eyebrow", look=(0.4, 0), badge=False, folder="none")
        c.restore()
    wrap(c, "Liner with a small wing and two lashes; fuller hair, deep side part, shine streak; "
            "fuller red lips with gloss; hoops 1.6x and thicker; teal wrap blouse, belt with a gold buckle.",
         880, 500, 10, 300)

    # 6. colours
    corp(c, "COLOURS", 24, 560, 10, bold=True)
    sw = [("skin", sf.SKIN), ("hair", sf.HAIR), ("blouse", sf.BLOUSE), ("skirt", sf.SKIRT), ("hair shine", sf.HAIR_SHINE),
          ("lips, nails", sf.RED), ("hoops", sf.GOLD), ("belt", sf.BELT)]
    for i, (lbl, col) in enumerate(sw):
        x = 24 + (i % 4) * 66,
        x, y = 24 + (i % 4) * 66, 568 + (i // 4) * 84
        c.set_source_rgb(*col); c.rectangle(x, y, 58, 40); c.fill()
        c.set_source_rgb(*INK); c.set_line_width(1); c.rectangle(x, y, 58, 40); c.stroke()
        corp(c, lbl, x, y + 54, 9, bold=True)
        corp(c, "#%02X%02X%02X" % tuple(int(v * 255) for v in col), x, y + 66, 9, col=GREY)

    # 7. character notes
    corp(c, "WHO SHE IS", 300, 560, 10, bold=True)
    wrap(c, "Charming and playful: she flirts with Don, and he eats it up. But she notices the difference between "
            "what people say and what they do, and by the end she knows whom to ask. Flirty is a tool, not her "
            "whole personality: the comedy is her reading the room.", 300, 578, 11, 420)
    corp(c, "ACTING", 300, 650, 10, bold=True)
    wrap(c, "With Don: half-lidded smile, hair twirl, a wink. When the truth shows: the flirt drops and one "
            "eyebrow goes up. Her eyeline tells the story; reactions face camera, never covered.", 300, 668, 11, 420)
    corp(c, "VOICE", 760, 560, 10, bold=True)
    wrap(c, "Warm and playful with Don, plain and sincere with the robot (Kokoro af_bella). No put-on accent.",
         760, 578, 11, 410)
    corp(c, "STYLE RULES", 760, 626, 10, bold=True)
    wrap(c, "Same flat cutout and proportions as Pam: the glow-up is face, hair, hoops, lips and wardrobe, never "
            "body shape or camera angles. Hoops and red lips carry her at phone size; hoops stay clear of the shoulders.",
         760, 644, 11, 410)
    corp(c, "Drawn with sofia_v4.py, the same code the film will use.", 24, 762, 9, col=GREY)
    flush_labels(c)
    surf.write_to_png(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "sofia_sheet_v4.png")
