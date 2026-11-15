"""v2 (sofia_sheet_mf_v1.py writes v1 from sofia_mf_v1.py). SOFÍA model sheet for "Mandatory Fun" (sofia_mf.py).
Writes sofia_sheet_mf_v2.png at 2400x1560 (1200x780, 2x)."""
import sys
import cairo
import kit
import brand
import sofia_v4 as sf4
import sofia_tg as stg
import sofia_mf as sm
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


def at_table(k, x, feet, s, pose, face, look, nb_state="open", turn=0.0, pen_on=True, bx=None, by=None, h=None, ty=None):
    """Seated at the table: the figure, then the table top at her hands, the notebook and the pen in front."""
    c = k.c
    o = sm.sofia(k, x, feet, s, pose, face, look=look, seed=82)
    (lx, ly), (rx, ry) = o["hands"]
    if ty is None:
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
    o["ty"] = ty
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
    t = "UPTIMEZ INC. · CHARACTER MODEL SHEET · MANDATORY FUN v2"
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
    corp(c, "FACES  (four that read apart, even small)", 284, 348, 10, bold=True)
    faces = [("neutral", (0, 0.6), "flat (writing)"), ("eyebrow", (0.9, 0.1), "\"For what?\""),
             ("unimpressed", (0.8, 0), "unimpressed"), ("done", (0, 0), "done (exhale)")]
    for i, (e, lk, lab) in enumerate(faces):
        x, y = 284 + i * 83, 354
        boxed(c, x, y, 79, 92, lab, fill=(1, 1, 1) if i != 1 else (0.95, 0.97, 1.0))
        c.save(); c.rectangle(x, y, 79, 92); c.clip()
        head_at(k, x + 40, y + 40, 0.46, e, lk)
        c.restore()
    corp(c, "MOUTHS, 20 % smaller: rest · \"For what?\" F · O · speaking A", 284, 466, 9, col=GREY, bold=True)
    for i, m in enumerate((None, "F", "O", "A")):
        x, y = 284 + i * 83, 472
        boxed(c, x, y, 79, 60)
        c.save(); c.rectangle(x, y, 79, 60); c.clip()
        head_at(k, x + 40, y + 26, 0.42, "eyebrow", (0.9, 0.1), mouth=m)
        c.restore()

    # 4. the comedy rhythm, seated
    corp(c, "HER RHYTHM  (shot 4: glance · eyebrow · page turn · back to writing)", 634, 92, 10, bold=True)
    beats = [("write", "neutral", (0.9, 0.0), "open", 0.0, False, "1. a glance at Don"),
             ("write", "eyebrow", (0.9, 0.1), "open", 0.0, False, "2. one eyebrow up"),
             ("page", "unimpressed", (0.0, 0.9), "open", 0.45, False, "3. the page turn"),
             ("write", "neutral", (0, 0.9), "open", 0.0, True, "4. back to writing")]
    ty0 = None
    for i, (p, f, lk, st_, tn, pen_on, lab) in enumerate(beats):
        x = 634 + i * 136
        boxed(c, x, 98, 132, 210, lab, fill=(1, 1, 1) if i != 2 else (0.95, 0.97, 1.0))
        c.save(); c.rectangle(x, 98, 132, 192); c.clip()
        o_ = at_table(k, x + 66, 318, 0.58, p, f, lk, st_, tn, pen_on=pen_on,
                      ty=None if ty0 is None else ty0 + (x + 66) * 0)
        if ty0 is None: ty0 = o_["ty"]
        c.restore()

    # 5. the exit, one continuous action
    corp(c, "THE EXIT  (shot 11: close · stand, to the chest · walk left, the notebook stays put)", 634, 348, 10, bold=True)
    boxed(c, 634, 354, 88, 178, "close")
    c.save(); c.rectangle(634, 354, 88, 160); c.clip()
    at_table(k, 678, 590, 0.5, "close", "neutral", (0, 0.6), "closed", 0.0, pen_on=False)
    c.restore()
    for i, (ph, lab) in enumerate(((None, "stand, to chest"), (0.25, "walk"), (0.75, "walk"))):
        x = 726 + i * 90
        boxed(c, x, 354, 86, 178, lab)
        c.save(); c.rectangle(x, 354, 86, 160); c.clip()
        sm.sofia(k, x + 46, 524, 0.4, "carry" if ph is None else "walk", "neutral", look=(-0.9, 0), seed=84 + i,
                 step=ph, carry=True, lag=(8 if ph else 0, 0))
        c.restore()
    boxed(c, 998, 354, 178, 178, "page lifts 45-60 deg; hoops off the jaw")
    sm.notebook(k, 1050, 470, 0.8, "open", 0.4, seed=1500)
    c.save(); c.rectangle(1100, 356, 74, 156); c.clip()
    head_at(k, 1150, 420, 0.7, "neutral", (0.3, 0), lag=(10, 0))
    c.restore()

    # 6. phone-size check: Sofía's eyes on the notebook, Pam facing the action
    corp(c, "PHONE-SIZE CHECK  (Sofía's eyes on the notebook, Pam's on the action: the contrast reads before a word)", 24, 556, 10, bold=True)
    c.set_source_rgb(*kit.WALL); c.rectangle(24, 562, 590, 190); c.fill()
    c.save(); c.rectangle(24, 562, 590, 190); c.clip()
    at_table(k, 120, 745, 0.42, "write", "neutral", (0, 0.9), "open", 0.0)
    pt.pam(k, 225, 745, 0.42, "stand", "neutral", look=(0.9, 0), seed=96)
    at_table(k, 330, 745, 0.42, "page", "unimpressed", (0, 0.9), "open", 0.45)
    table_top(c, 180, 690, 90)
    sm.sofia(k, 520, 742, 0.42, "walk", "neutral", look=(-0.9, 0), step=0.25, carry=True, lag=(10, 0), seed=99)
    c.restore()

    # 7. notes
    corp(c, "NOTES", 634, 556, 10, bold=True)
    notes = ["Office v4 clothes and hair, the newer figure, visible block heels: one rig in every pose.",
             "Four faces that read apart: flat, the side-eye with one eyebrow, unimpressed, done (exhale).",
             "Her rhythm: glance, eyebrow, page turn, back to writing. The page turn gets a close-up.",
             "The page lifts 45-60 degrees over the spine; her other hand holds the book flat.",
             "Exit: close, stand, notebook to the chest, walk left; the notebook never moves; the free arm swings.",
             "Hoops 1.3x, set off the jaw, darker inside. Speaking mouths 20 % smaller."]
    for i, n in enumerate(notes):
        corp(c, "·  " + n, 634, 580 + i * 24, 11, col=INK)
    flush(c)
    surf.write_to_png(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "sofia_sheet_mf_v2.png")
