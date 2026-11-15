"""v2 (don_sheet_tg_v1.py writes v1 from don_tg_v1.py). DON model sheet for the Thanksgiving film
"Raises for Everyone" (don_tg.py). Writes don_sheet_tg_v2.png
at 2400x1560 (drawn at 1200x780, 2x)."""
import sys
import cairo
import kit
import brand
import don_v4 as dv
import don_tg as dt
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
    t = "UPTIMEZ INC. · CHARACTER MODEL SHEET · THANKSGIVING v2"
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
    corp(c, "Same Don; only the tie (and a new gravy splat) changes.", 290, 322, 9, col=GREY)

    # 3. faces
    corp(c, "FACES IN THIS FILM", 284, 348, 10, bold=True)
    faces = [("grin", "shot 1: grin"), ("laugh", "shot 4: HA!"), ("freeze", "shot 6: freeze (new)"),
             ("chew", "shot 8: chewing"), ("smug", "shot 10: smug (new)"), ("collapse", "shot 11: collapse (new)")]
    for i, (e, lab) in enumerate(faces):
        x, y = 284 + (i % 3) * 112, 354 + (i // 3) * 92
        boxed(c, x, y, 106, 86, lab)
        c.save(); c.rectangle(x, y, 106, 86); c.clip()
        head_at(k, x + 53, y + 40, 0.44, e)
        c.restore()

    # 4. poses
    corp(c, "POSES", 634, 92, 10, bold=True)
    poses = [(dt.POSE_SLAP, "grin", None, "1: slap"), (dt.POSE_LAUGH, "laugh", None, "4: HA!"),
             (dt.POSE_TAP, "freeze", None, "6: tap, frozen"), (dt.POSE_POINT, "smug", (1, -35, 1), "8: \"You failed.\""),
             (dt.POSE_BITE, "chew", (1, -150, 1), "8: bite, no answer"), (dt.POSE_BACKME, "smug", (2, 100, 0), "10: back me up")]
    for i, (p, f, leg, lab) in enumerate(poses):
        x = 634 + i * 91
        boxed(c, x, 98, 87, 210, lab)
        c.save(); c.rectangle(x, 98, 87, 210); c.clip()
        o = dt.don(k, x + (22 if p is dt.POSE_POINT else 38), 286, 0.4, p, f, look=(0.7, 0), seed=80 + i, leg=leg)
        if p is dt.POSE_TAP:
            dt.tapping_finger(k, o["hands"][1], 0.4)
        c.restore()

    # 5. shots 10-11 as three beats: freeze mid-bite -> collapse -> recovery
    corp(c, "SHOTS 10-11:  FREEZE MID-BITE  >  COLLAPSE (1 beat)  >  RECOVERY, \"Sign it.\"", 634, 348, 10, bold=True)
    boxed(c, 634, 354, 416, 178, "he learns nothing: the grin comes back as the leg covers the verdict")
    c.save(); c.rectangle(634, 354, 416, 160); c.clip()
    dt.don(k, 684, 590, 0.55, dt.POSE_FREEZE_BITE, "bite_freeze", look=(0.8, -0.2), seed=86, leg=(2, -110, 1))
    dt.don(k, 790, 590, 0.55, dt.POSE_SLUMP, "collapse", seed=87, leg=(3, 95, 1), slump=1.3)
    scratch = Ctx(cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 4, 4)), 0)
    o = dt.don(scratch, 892, 590, 0.55, dt.POSE_BLOCK, "grin", seed=88)
    hx, hy = o["hands"][1]
    screen(c, hx - 4, hy - 22, 68, 44, "ACCURATE.", (0.25, 0.85, 0.35))
    o = dt.don(k, 892, 590, 0.55, dt.POSE_BLOCK, "grin", look=(-0.8, 0.3), seed=88, leg=(3, 0, 1, 1.5))
    table(c, 634, 494, 416)
    lx, ly = o["hands"][0]
    form(c, lx - 6, 502, 26, 0.3)                          # the form right under his sliding hand
    for x_, n in ((672, "10"), (776, "11a"), (850, "11b")):
        corp(c, n, x_, 372, 11, col=GREY, bold=True)
    c.restore()
    corp(c, "LEG  (bites 0-3)", 1058, 348, 10, bold=True)
    boxed(c, 1058, 354, 118, 178, "frill in the fist")
    for i in range(4):
        dt.turkey_leg(k, 1072, 378 + i * 36, 0.62, 0, i, 600 + i)
    # 6. phone-size check: Don at the head of the table
    corp(c, "PHONE-SIZE CHECK  (two-shot size, behind the table: tie, gravy and leg read?)", 24, 556, 10, bold=True)
    c.set_source_rgb(*kit.WALL); c.rectangle(24, 562, 590, 190); c.fill()
    c.save(); c.rectangle(24, 562, 590, 190); c.clip()
    for i, (p, f, leg, sl) in enumerate(((dt.POSE_SLAP, "grin", None, 0), (dt.POSE_TAP, "freeze", None, 0),
                                         (dt.POSE_BITE, "chew", (1, -150, 1), 0),
                                         (dt.POSE_SLUMP, "collapse", (3, 95, 1), 1.0),
                                         (dt.POSE_BLOCK, "grin", (3, 0, 1, 1.5), 0))):
        dt.don(k, 74 + i * 112, 770, 0.42, p, f, look=(0.6, 0), seed=95 + i, leg=leg, slump=sl)
    c.restore()
    table(c, 24, 700, 590)
    # 7. notes
    corp(c, "NOTES", 634, 556, 10, bold=True)
    notes = ["Office v4 kept: vest, shirt, khakis, badge, the ketchup squiggle. No new costume details.",
             "Loud flag tie; gravy splat 1.5x so it survives a phone screen.",
             "Six faces that escalate: grin, HA!, freeze, chew, smug, collapse.",
             "Turkey leg acts: points at Pam, bites instead of answering, freezes, covers the verdict.",
             "Collapse is one beat: posture sinks, brows up, mouth sags.",
             "Then the grin returns: he learns nothing. \"Sign it.\""]
    for i, n in enumerate(notes):
        corp(c, "·  " + n, 634, 580 + i * 24, 11, col=INK)
    flush(c)
    surf.write_to_png(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "don_sheet_tg_v2.png")
