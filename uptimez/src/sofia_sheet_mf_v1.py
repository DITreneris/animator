"""SOFÍA model sheet for "Mandatory Fun" (sofia_mf.py). Writes sofia_sheet_mf_v1.png at 2400x1560 (1200x780, 2x)."""
import sys
import cairo
import kit
import brand
import sofia_v4 as sf4
import sofia_tg as stg
import sofia_mf_v1 as sm
import pam_tg as pt
import iwry_mouths as im
from kit import Ctx, INK
from charsheets import corp

W2, H2 = 1200, 780
GREY = (0.35, 0.40, 0.50)
ACCENT = (0.84, 0.92, 0.92)
LABELS = []
HY = -300 * sm.H + 78 - 44
WOOD = (0.55, 0.36, 0.22)


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


def table_top(c, x, y, w):
    c.set_source_rgb(*WOOD); c.rectangle(x, y, w, 10); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(1.4); c.rectangle(x, y, w, 10); c.stroke()
    c.set_source_rgb(0.42, 0.27, 0.16); c.rectangle(x, y + 10, w, 300); c.fill()
    c.set_source_rgb(*INK); c.rectangle(x, y + 10, w, 300); c.stroke()


def head_at(k, cx, cy, s, kind, look=(0, 0), lag=(0, 0), mouth=None):
    sm.sofia(k, cx, cy - HY * s, s, "stand", kind, look=look, lag=lag, badge=False, mouth=mouth)


def at_table(k, x, feet, s, pose, face, look, nb_state="open", turn=0.0, pen_on=True, bx=None, by=None, h=None):
    """Seated at the table: the figure, then the table top at her hands, the notebook and the pen in front."""
    c = k.c
    o = sm.sofia(k, x, feet, s, pose, face, look=look, seed=82)
    (lx, ly), (rx, ry) = o["hands"]
    ty = max(ly, ry) + 4 * s
    c.save()
    if bx is not None:
        c.rectangle(bx, by, 4000, h); c.clip()
    table_top(c, x - 70 * s, ty, 140 * s)
    sm.notebook(k, x + 2 * s, ty + 4 * s, s * 0.62, nb_state, turn)
    for hx, hy_ in o["hands"]:
        kit.ellipse(k, hx, min(hy_, ty + 2 * s), 8.5 * s, 8.5 * s, sm.SKIN, 1403, shadow=False, lw=2 * s)
    if pen_on and pose in ("write",):
        sm.pen(k, rx, min(ry, ty + 2 * s), s, 0.55)
    c.restore()
    return o


def main(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "SOFÍA", 68, 44, 28, bold=True)
    corp(c, "\"Mandatory Fun\"  ·  the straight woman  ·  office v4 look on the newer figure", 172, 44, 13, col=GREY)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    t = "UPTIMEZ INC. · CHARACTER MODEL SHEET · MANDATORY FUN v1"
    corp(c, t, W2 - 24 - c.text_extents(t).x_advance, 30, 10, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()

    # 1. front
    c.set_source_rgb(*ACCENT); c.rectangle(24, 80, 240, 450); c.fill()
    sm.sofia(k, 144, 512, 1.18, "stand", "neutral", seed=71)
    corp(c, "FRONT · OFFICE v4, NEWER FIGURE", 32, 524, 9, col=brand.NAVY, bold=True)

    # 2. lineage
    corp(c, "OFFICE v4  ·  THANKSGIVING v2  ·  MANDATORY FUN", 284, 92, 10, bold=True)
    boxed(c, 284, 98, 330, 210)
    c.save(); c.rectangle(284, 98, 330, 210); c.clip()
    sf4.sofia(k, 345, 296, 0.56, "stand", "neutral", seed=73, folder="none")
    stg.sofia(k, 449, 296, 0.56, "stand", "neutral", seed=73)
    sm.sofia(k, 553, 296, 0.56, "stand", "neutral", seed=73)
    c.restore()
    corp(c, "v4 clothes and hair, the newer figure and heels, hoops 1.3x.", 290, 322, 9, col=GREY)

    # 3. faces + mouths
    corp(c, "FACES  (she reacts by not reacting)", 284, 348, 10, bold=True)
    faces = [("neutral", (0, 0), "flat"), ("unimpressed", (0, 0.9), "\"For what?\""),
             ("unimpressed", (0.8, 0), "unimpressed"), ("closed", (0, 0), "done")]
    for i, (e, lk, lab) in enumerate(faces):
        x, y = 284 + i * 83, 354
        boxed(c, x, y, 79, 92, lab)
        c.save(); c.rectangle(x, y, 79, 92); c.clip()
        head_at(k, x + 40, y + 40, 0.46, e, lk)
        c.restore()
    corp(c, "\"For what?\"  mouths F · O · U · A · C", 284, 466, 9, col=GREY, bold=True)
    for i, m in enumerate(("F", "O", "U", "A", "C")):
        x, y = 284 + i * 67, 472
        boxed(c, x, y, 63, 60)
        c.save(); c.rectangle(x, y, 63, 60); c.clip()
        head_at(k, x + 31, y + 26, 0.42, "unimpressed", (0, 0.9), mouth=m)
        c.restore()

    # 4. poses: at the table, then the walk-out
    corp(c, "POSES  (seated at the table, then the exit in shot 11)", 634, 92, 10, bold=True)
    panels = [("write", "unimpressed", (0, 0.9), "open", 0.0, "4: writing"),
              ("page", "unimpressed", (0.3, 0.9), "open", 0.55, "4: the page turn"),
              ("close", "neutral", (0, 0.6), "closed", 0.0, "11: closes it")]
    for i, (p, f, lk, st_, tn, lab) in enumerate(panels):
        x = 634 + i * 91
        boxed(c, x, 98, 87, 210, lab)
        c.save(); c.rectangle(x, 98, 87, 192); c.clip()
        at_table(k, x + 44, 330, 0.5, p, f, lk, st_, tn)
        c.restore()
    for i, (ph, lab) in enumerate(((None, "11: stands, carries it"), (0.25, "11: walks out"), (0.75, "(stride 2)"))):
        x = 634 + (i + 3) * 91
        boxed(c, x, 98, 87, 210, lab)
        c.save(); c.rectangle(x, 98, 87, 192); c.clip()
        sm.sofia(k, x + 44, 286, 0.42, "carry" if ph is None else "walk", "neutral", look=(-0.9, 0), seed=84 + i,
                 step=ph, carry=True, lag=(6 if ph else 0, 0))
        c.restore()

    # 5. props and hoops
    corp(c, "NOTEBOOK + PEN  ·  HOOPS SWING (head turn left · still · right)", 634, 348, 10, bold=True)
    boxed(c, 634, 354, 270, 178, "open · page turning · closed  (phone size: shape, not text)")
    for i, (st_, tn) in enumerate((("open", 0.0), ("open", 0.5), ("closed", 0.0))):
        sm.notebook(k, 680 + i * 88, 420, 0.62, st_, tn, seed=1500 + i)
    sm.pen(k, 700, 480, 1.0, 0.9)
    for i, lg in enumerate((-14, 0, 14)):
        x = 912 + i * 89
        boxed(c, x, 354, 85, 178, "")
        c.save(); c.rectangle(x, 354, 85, 178); c.clip()
        head_at(k, x + 42, 430, 0.62, "neutral", (lg / 9, 0), lag=(lg, 0))
        c.restore()

    # 6. phone-size check: at the training table beside Pam
    corp(c, "PHONE-SIZE CHECK  (at the table beside Pam: does she read as the one trying to learn?)", 24, 556, 10, bold=True)
    c.set_source_rgb(*kit.WALL); c.rectangle(24, 562, 590, 190); c.fill()
    c.save(); c.rectangle(24, 562, 590, 190); c.clip()
    at_table(k, 120, 745, 0.42, "write", "unimpressed", (0, 0.9), "open", 0.0)
    ts_y = 745 + (HY + 300 * sm.H - 78 + 44) * 0      # (same seat height for Pam)
    pt.pam(k, 225, 745, 0.42, "stand", "neutral", look=(0.6, 0.6), seed=96)
    at_table(k, 330, 745, 0.42, "page", "unimpressed", (0.3, 0.9), "open", 0.55)
    table_top(c, 180, 690, 90)
    sm.sofia(k, 520, 742, 0.42, "walk", "neutral", look=(-0.9, 0), step=0.25, carry=True, lag=(10, 0), seed=99)
    c.restore()

    # 7. notes
    corp(c, "NOTES", 634, 556, 10, bold=True)
    notes = ["Office v4 clothes and hair exactly: teal wrap blouse, black skirt, belt, long hair, side part.",
             "The newer figure from Christmas carries forward: waist, hips, shaped legs, black pumps.",
             "Big gold hoops, 1.3x, dark outline; they swing on head turns and the walk-out.",
             "The straight woman: no comeback, no emoji. A page turn is her answer.",
             "Notebook writing is unreadable on purpose: only the page turn has to read.",
             "Exit (shot 11): closes it, stands, carries it to her chest, walks out left."]
    for i, n in enumerate(notes):
        corp(c, "·  " + n, 634, 580 + i * 24, 11, col=INK)
    flush(c)
    surf.write_to_png(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "sofia_sheet_mf_v1.png")
