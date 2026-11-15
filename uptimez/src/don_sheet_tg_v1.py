"""DON model sheet for the Thanksgiving film "Raises for Everyone" (don_tg.py). Writes don_sheet_tg_v1.png
at 2400x1560 (drawn at 1200x780, 2x)."""
import sys
import cairo
import kit
import brand
import don_v4 as dv
import don_tg_v1 as dt
import sofia_tg as st
from kit import Ctx, INK
from charsheets import corp

W2, H2 = 1200, 780
GREY = (0.35, 0.40, 0.50)
ACCENT = (0.80, 0.86, 0.93)
LABELS = []
HY = -300 * kit.PEOPLE["DON"]["h"] + 78 - 44


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


def form(c, x, y, w, ang=0.0):
    h = w * 1.3
    c.save(); c.translate(x, y); c.rotate(ang)
    c.set_source_rgb(1, 1, 1); c.rectangle(-w / 2, -h / 2, w, h); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(1.4); c.stroke()
    c.set_source_rgb(*brand.GREEN); c.rectangle(-w / 2 + 2, -h / 2 + 2, w - 4, h * 0.1); c.fill()
    c.set_source_rgb(*INK); c.rectangle(-w * 0.38, -h * 0.12, w * 0.76, h * 0.07); c.fill()
    c.set_source_rgb(0.6, 0.6, 0.6)
    for i in range(3):
        c.rectangle(-w * 0.38, h * 0.02 + i * h * 0.07, w * 0.6, h * 0.025); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(1); c.move_to(-w * 0.3, h * 0.38); c.line_to(w * 0.3, h * 0.38); c.stroke()
    c.restore()


def table(c, x, y, w):
    c.set_source_rgb(0.55, 0.36, 0.22); c.rectangle(x, y, w, 14); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(1.6); c.rectangle(x, y, w, 14); c.stroke()
    c.set_source_rgb(0.98, 0.95, 0.88); c.rectangle(x, y + 14, w, 60); c.fill()
    c.set_source_rgb(*INK); c.rectangle(x, y + 14, w, 60); c.stroke()


def screen(c, x, y, w, h, word, col):
    c.set_source_rgb(0.75, 0.77, 0.80); c.rectangle(x - 8, y - 8, w + 16, h + 16); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(2); c.stroke()
    c.set_source_rgb(0.08, 0.10, 0.12); c.rectangle(x, y, w, h); c.fill()
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(h * 0.22)
    tw = c.text_extents(word).x_advance
    c.set_source_rgb(*col); c.move_to(x + (w - tw) / 2, y + h * 0.62); c.show_text(word)


def head_at(k, cx, cy, s, face, look=(0, 0)):
    dt.don(k, cx, cy - HY * s, s, "stand", face, look=look)


def main(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "DON", 68, 44, 28, bold=True)
    corp(c, "Thanksgiving film \"Raises for Everyone\"  ·  the boss  ·  sincerely thinks he is generous", 140, 44, 13,
         col=GREY)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    t = "UPTIMEZ INC. · CHARACTER MODEL SHEET · THANKSGIVING v1"
    corp(c, t, W2 - 24 - c.text_extents(t).x_advance, 30, 10, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()

    # 1. front
    c.set_source_rgb(*ACCENT); c.rectangle(24, 80, 240, 450); c.fill()
    dt.don(k, 144, 512, 1.12, "stand", "grin", seed=71)
    corp(c, "FRONT · FLAG TIE · GRIN", 32, 524, 9, col=brand.NAVY, bold=True)

    # 2. office v4 vs Thanksgiving, with Sofía v2 for height
    corp(c, "OFFICE v4  ·  THANKSGIVING  ·  WITH SOFÍA v2", 284, 92, 10, bold=True)
    boxed(c, 284, 98, 330, 210)
    c.save(); c.rectangle(284, 98, 330, 210); c.clip()
    dv.don(k, 345, 296, 0.55, seed=74)
    dt.don(k, 452, 296, 0.55, seed=74)
    st.sofia(k, 556, 296, 0.55, "stand", "neutral", look=(-0.8, 0), seed=73)
    c.restore()
    corp(c, "Same Don; only the tie (and a new gravy drip) changes.", 290, 322, 9, col=GREY)

    # 3. faces
    corp(c, "FACES IN THIS FILM", 284, 348, 10, bold=True)
    faces = [("grin", "shot 1: grin"), ("laugh", "shot 4: HA!"), ("drop", "shot 6: freezes"),
             ("chew", "shot 8: chewing"), ("smug", "shot 10: smug"), ("deflated", "shot 11: collapse")]
    for i, (e, lab) in enumerate(faces):
        x, y = 284 + (i % 3) * 112, 354 + (i // 3) * 92
        boxed(c, x, y, 106, 86, lab)
        c.save(); c.rectangle(x, y, 106, 86); c.clip()
        head_at(k, x + 53, y + 40, 0.44, e)
        c.restore()

    # 4. poses
    corp(c, "POSES", 634, 92, 10, bold=True)
    poses = [(dt.POSE_SLAP, "grin", None, "1: slap"), (dt.POSE_LAUGH, "laugh", None, "4: HA!"),
             (dt.POSE_TAP, "drop", None, "6: tap"), (dt.POSE_TEAR, "chew", (0, 0, 1), "8: tear"),
             (dt.POSE_POINT, "smug", (1, -8, 1), "8: point"), (dt.POSE_BACKME, "smug", None, "10: back me up")]
    for i, (p, f, leg, lab) in enumerate(poses):
        x = 634 + i * 91
        boxed(c, x, 98, 87, 210, lab)
        c.save(); c.rectangle(x, 98, 87, 210); c.clip()
        o = dt.don(k, x + 38, 286, 0.4, p, f, look=(0.7, 0), seed=80 + i, leg=leg)
        if p is dt.POSE_TAP:
            dt.tapping_finger(k, o["hands"][1], 0.4)
        c.restore()

    # 5. finale + turkey-leg bites
    corp(c, "FINALE  (shot 11: leg over the verdict, form slid back)", 634, 348, 10, bold=True)
    boxed(c, 634, 354, 300, 178, "\"Sign it.\"")
    c.save(); c.rectangle(634, 354, 300, 160); c.clip()
    scratch = Ctx(cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 4, 4)), 0)
    hx, hy = dt.don(scratch, 742, 600, 0.62, dt.POSE_BLOCK, "deflated", seed=88)["hands"][1]
    sw, sh = 76, 50                                       # the leg, held flat, lies across the word
    screen(c, hx - 4, hy - sh / 2, sw, sh, "ACCURATE.", (0.25, 0.85, 0.35))
    dt.don(k, 742, 600, 0.62, dt.POSE_BLOCK, "deflated", look=(-0.6, 0.2), seed=88, leg=(3, 0, 1, 1.5))
    table(c, 634, 492, 300)
    form(c, 668, 500, 30, 0.3)
    c.restore()
    corp(c, "TURKEY LEG  (bites 0 · 1 · 2 · 3 across the film)", 944, 348, 10, bold=True)
    boxed(c, 944, 354, 232, 178, "frill in the fist; meat side out")
    for i in range(4):
        dt.turkey_leg(k, 966 + (i % 2) * 110, 392 + (i // 2) * 66, 1.0, 0, i, 600 + i)
    # 6. phone-size check: Don at the head of the table
    corp(c, "PHONE-SIZE CHECK  (two-shot size, behind the table: tie, gravy and leg read?)", 24, 556, 10, bold=True)
    c.set_source_rgb(*kit.WALL); c.rectangle(24, 562, 590, 190); c.fill()
    for i, (p, f, leg) in enumerate(((dt.POSE_SLAP, "grin", None), (dt.POSE_POINT, "chew", (1, -8, 1)),
                                     (dt.POSE_BACKME, "smug", None), (dt.POSE_BLOCK, "deflated", (3, 0, 1, 1.5)))):
        dt.don(k, 90 + i * 145, 770, 0.42, p, f, look=(0.6, 0), seed=95 + i, leg=leg)
    table(c, 24, 700, 590)
    # 7. notes
    corp(c, "NOTES", 634, 556, 10, bold=True)
    notes = ["Office v4 kept: vest, shirt, khakis, badge, the ketchup squiggle.",
             "Classic loud flag tie: blue canton with stars under the knot, red-white stripes.",
             "Gravy drip on the tie beside the ketchup. Never mentioned.",
             "No napkin: the tie stays visible. No other new accessories.",
             "Turkey leg: paper frill in his fist, bites grow 0 → 3 from shot 8 to 11.",
             "He means every word: the grin is sincere, the collapse lasts one beat."]
    for i, n in enumerate(notes):
        corp(c, "·  " + n, 634, 580 + i * 24, 11, col=INK)
    flush(c)
    surf.write_to_png(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "don_sheet_tg_v1.png")
