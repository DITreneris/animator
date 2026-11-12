"""Waiter robot model sheet for "I Will Replace You" (waiter_kit.py). Writes robot_sheet_v1.png at
2400x1560 (drawn at 1200x780, 2x)."""
import sys
import math
import cairo
import kit
import brand
import anim
import waiter_kit_v1 as w
import cafe_kit_v1 as ck
import sofia_v4 as sf
import don_v4 as dv
from kit import Ctx, INK
from charsheets import corp, wrap
from sofia_sheet_v4 import boxed, flush_labels

W2, H2 = 1200, 780
GREY = (0.35, 0.40, 0.50)
ACCENT = (0.80, 0.90, 0.93)


def silhouette(k, draw):
    """Draws `draw` as one solid ink shape: the pose must read without any interior detail."""
    c = k.c
    c.push_group()
    draw()
    pat = c.pop_group()
    c.set_source_rgb(*INK)
    c.mask(pat)


def main(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "WAITER ROBOT", 68, 44, 28, bold=True)
    corp(c, "Cafeteria TRAINEE  ·  wants a job, not Don  ·  pathetic, never evil", 290, 44, 13, col=GREY)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    tw = c.text_extents("UPTIMEZ INC. · I WILL REPLACE YOU · MODEL SHEET v1").x_advance
    corp(c, "UPTIMEZ INC. · I WILL REPLACE YOU · MODEL SHEET v1", W2 - 24 - tw, 30, 10, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()

    # 1. front
    c.set_source_rgb(*ACCENT); c.rectangle(24, 80, 240, 450); c.fill()
    w.robot(k, 144, 470, 1.32, "stand", "eager", seed=901)
    corp(c, "FRONT · EAGER", 32, 524, 9, col=brand.NAVY, bold=True)

    # 2. the three silhouettes (solid) and the same poses in colour
    corp(c, "THE THREE SILHOUETTES  (the punchline, in body shape)", 284, 92, 10, bold=True)
    for i, (p, f, lbl) in enumerate([("nervous", "timid", "1 nervous"), ("lock", "stern", "2 \"I WILL REPLACE YOU!\""),
                                       ("lean", "timid", "3 \"If that's okay, sir?\"")]):
        x = 284 + i * 128
        boxed(c, x, 98, 122, 236, lbl)
        c.save(); c.rectangle(x, 98, 122, 220); c.clip()
        cx = x + (72 if p == "lock" else 58)
        silhouette(k, lambda p=p, f=f, cx=cx: w.robot(k, cx, 210, 0.33, p, f, seed=910 + i))
        w.robot(k, cx, 316, 0.33, p, f, seed=910 + i)
        c.restore()
    wrap(c, "Read as black shapes first: small and sunk; tall, still, arm locked out; diagonal, collapsed "
            "toward Don. The wheel clamp locks only in 2.", 284, 350, 10, 380)

    # 3. screen faces
    corp(c, "SCREEN FACES", 680, 92, 10, bold=True)
    faces = [("eager", 0, "eager"), ("eager", 0.9, "eager, talking"), ("proud", 0, "proud"),
             ("pleading", 0, "pleading (not hearts)"), ("stern", 0.9, "stern, shouting"), ("timid", 0.5, "timid, whisper")]
    for i, (f, talk, lbl) in enumerate(faces):
        x, y = 680 + (i % 3) * 170, 98 + (i // 3) * 118
        boxed(c, x, y, 164, 112, lbl, fill=(0.93, 0.95, 0.98) if f == "pleading" else (1, 0.99, 0.97))
        c.save(); c.rectangle(x, y, 164, 96); c.clip()
        c.save(); c.translate(x + 82, y + 50); c.scale(1.05, 1.05)
        kit.ellipse(k, 0, 0, 50, 44, w.BODY, 950 + i)
        kit.ellipse(k, 0, 0, 40, 33, w.SCREEN, 960 + i, shadow=False, lw=1.8)
        w.screen_face(k, f, talk=talk)
        c.restore(); c.restore()

    # 4. height line-up at the table and standing
    corp(c, "HEIGHTS: AT THE TABLE, AND STANDING", 284, 398, 10, bold=True)
    boxed(c, 284, 404, 380, 196)
    c.save(); c.rectangle(284, 404, 380, 182); c.clip()
    c.translate(284, 404); c.scale(0.34, 0.34); c.translate(-20, -470)
    ck.room(k)
    ck.chair_back(k, ck.SOF[0], ck.SOF[1] - 214, 1250)
    ck.chair_back(k, ck.DON[0], ck.DON[1] - 244, 1251)
    w.robot(k, ck.ROBOT[0], ck.ROBOT[1], 1.0, "serve", "eager", look=(1, 0), tray="empty", seed=970)
    ck.seated(k, lambda: sf.sofia(k, ck.SOF[0], ck.SOF[1], 1.0, "stand", "neutral", look=(0.6, 0), folder="none"))
    ck.seated(k, lambda: dv.don(k, ck.DON[0], ck.DON[1], 1.0, "stand", "smug", look=(-0.6, 0)))
    ck.table(k)
    dv.don(k, 760, 880, 1.0, "stand", "neutral", seed=520)
    w.robot(k, 880, 880, 1.0, "stand", "eager", look=(-1, 0), seed=971, side=-1)
    c.restore()
    corp(c, "Screen at seated eye level, wheel hidden by the table. Standing: Don's chest height.",
         290, 614, 9, col=GREY)

    # 5. action poses
    corp(c, "ACTION POSES", 680, 340, 10, bold=True)
    acts = [("travel", "eager", "dome", "travel, wobbling"), ("lift", "proud", None, "lifts the dome"),
            ("tie", "pleading", None, "fixes bow tie"), ("lock", "stern", None, "points at Sofía")]
    for i, (p, f, tray, lbl) in enumerate(acts):
        x = 680 + i * 128
        boxed(c, x, 346, 122, 196, lbl)
        c.save(); c.rectangle(x, 346, 122, 180); c.clip()
        cx = x + (78 if p == "lock" else 56)
        wob = 0.08 if p == "travel" else 0.0
        rb = w.robot(k, cx, 520, 0.5, p, f, tray=tray, wobble=wob, seed=980 + i)
        if p == "lift":
            hx, hy = rb["hands"][1]
            c.save(); c.translate(hx + 4, hy + 18); c.rotate(-0.4)
            w.dome_tray(k, 0, 0, w=48, dome=1.0); c.restore()
        c.restore()

    # 6. wobble guide
    corp(c, "WOBBLE: ONLY WHILE MOVING OR NERVOUS", 680, 566, 10, bold=True)
    boxed(c, 680, 572, 250, 120)
    c.save(); c.rectangle(680, 572, 250, 106); c.clip()
    for i, (wob, a) in enumerate([(-0.10, 0.25), (0.10, 0.25), (0.0, 1.0)]):
        c.push_group()
        w.robot(k, 805, 676, 0.36, "travel", "eager", tray="empty", wobble=wob, seed=990)
        c.pop_group_to_source(); c.paint_with_alpha(a)
    c.restore()
    wrap(c, "±6° over the wheel while it rolls; the tray follows 2–3 frames late. Still during every line "
            "and every reaction hold.", 940, 584, 10, 236)

    # 7. colours + notes
    corp(c, "COLOURS", 24, 560, 10, bold=True)
    sw = [("shell", w.BODY), ("arms", w.STEEL), ("screen", w.SCREEN), ("eyes", w.GLOW),
          ("stern", w.GLOW_STERN), ("bow tie", w.TIE), ("clamp", w.CLAMP), ("wheel", (0.16, 0.16, 0.18))]
    for i, (lbl, col) in enumerate(sw):
        x, y = 24 + (i % 4) * 62, 568 + (i // 4) * 84
        c.set_source_rgb(*col); c.rectangle(x, y, 54, 40); c.fill()
        c.set_source_rgb(*INK); c.set_line_width(1); c.rectangle(x, y, 54, 40); c.stroke()
        corp(c, lbl, x, y + 54, 9, bold=True)
        corp(c, "#%02X%02X%02X" % tuple(int(v * 255) for v in col), x, y + 66, 9, col=GREY)
    corp(c, "RULES", 284, 646, 10, bold=True)
    wrap(c, "Talks only to \"sir\"; never looks at Sofía until it points. Never understands the irony. "
            "Distinct from DON 2.0 (grey box, red tie). Voice: to audition, bright and a bit nasal.",
         284, 664, 10, 380)
    corp(c, "Drawn with waiter_kit.py, the same code the film will use.", 24, 762, 9, col=GREY)
    flush_labels(c)
    surf.write_to_png(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "robot_sheet_v1.png")
