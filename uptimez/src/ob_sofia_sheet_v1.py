"""v1, pinned. THE ONBOARDING: Sofia's sheet, v1. Her office look with pearls for gold, the tablet with the sheet clipped to it,
and the faces of this film: in control, appraising the Client. Writes ob_sofia_v1.png at 2400x3000 (drawn at
1200x1500, 2x) and ob_sofia_phone_v1.png (four 360x640 frames at the size they will have on a phone)."""
import sys
import math
import cairo
import kit
import brand
import sofia_ob_v1 as so
import client_ob_v3 as co
import don_v4 as dv
from kit import Ctx, INK, rect, ellipse
from charsheets import corp, wrap

V = "v1"
W2, H2 = 1200, 1500
GREY = (0.35, 0.40, 0.50)
FLOOR = (0.72, 0.63, 0.50)
# face, pose, look, lean, label, note
FACES = [("tiny", (-0.8, 0.0), 0, "CAUGHT", "she smiles before she knows"),
         ("smile", (-0.8, -0.1), -5, "SWEET", "the question"),
         ("appraise", (-0.8, 1.0), 0, "EYES DOWN", "reading him"),
         ("appraise", (-0.8, 0.45), 0, "EYES UP", "back to his face"),
         ("oh", (-0.8, 0.45), 0, "OH...", "low, drawn out"),
         ("knowing", (1.0, 0.1), 0, "TO DON", "one glance, once"),
         ("breath", (0, 0), -4, "A BREATH", "close to him, beat 06"),
         ("knowing", (-0.5, 0.9), 0, "THE TROPHY", "his thumbprint")]


def room(c, x, y, w, h, floor_h):
    c.set_source_rgb(*kit.WALL); c.rectangle(x, y, w, h); c.fill()
    c.set_source_rgb(*FLOOR); c.rectangle(x, y + h - floor_h, w, floor_h); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(1.6); c.move_to(x, y + h - floor_h); c.line_to(x + w, y + h - floor_h); c.stroke()


def framed(c, x, y, w, h, draw, floor_h=0, fill=None):
    c.save(); c.rectangle(x, y, w, h); c.clip()
    if floor_h:
        room(c, x, y, w, h, floor_h)
    else:
        c.set_source_rgb(*(fill or kit.WALL)); c.rectangle(x, y, w, h); c.fill()
    draw()
    c.restore()
    c.set_source_rgb(*INK); c.set_line_width(1.2); c.rectangle(x, y, w, h); c.stroke()


def callout(c, x0, y0, x1, y1, label, right=False):
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(x0, y0); c.line_to(x1, y1); c.stroke()
    c.arc(x0, y0, 2.6, 0, 2 * math.pi); c.fill()
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    w = c.text_extents(label).x_advance
    tx = x1 - w - 8 if right else x1 + 8
    c.set_source_rgb(1, 1, 1); c.rectangle(tx - 6, y1 - 10, w + 12, 20); c.fill_preserve()
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.0); c.stroke()
    corp(c, label, tx, y1 + 3.5, 10, bold=True)


def cv_insert(c, k, x, y, s):
    """The insert of beat 06: the sheet in her hand. A CV first; then the number, circled, and a small heart."""
    c.save(); c.translate(x, y); c.scale(s, s)
    c.save(); c.rotate(-0.05)
    rect(k, -62, -84, 124, 168, so.PAPER, 31, lw=2)
    rect(k, -50, -72, 38, 44, (0.98, 0.86, 0.50), 32, shadow=False, lw=1.6)           # her portrait
    ellipse(k, -31, -48, 11, 11, so.SKIN, 33, shadow=False, lw=1.4)
    c.set_source_rgb(*so.RED); c.set_line_width(2); c.move_to(-35, -43); c.line_to(-27, -43); c.stroke()
    c.set_source_rgb(*INK); c.select_font_face("Inter", 0, 1); c.set_font_size(15); c.move_to(-4, -58); c.show_text("CV")
    c.set_source_rgb(0.62, 0.62, 0.64); c.set_line_width(3); c.set_line_cap(1)
    for yy, x0, x1 in ((-46, -4, 46), (-36, -4, 38), (-14, -50, 48), (-3, -50, 40), (8, -50, 46), (19, -50, 30)):
        c.move_to(x0, yy); c.line_to(x1, yy); c.stroke()
    c.set_source_rgb(*INK); c.select_font_face("Inter", 0, 1); c.set_font_size(12.5); c.move_to(-44, 52); c.show_text("555 0142")
    c.set_source_rgb(*so.RED); c.set_line_width(2.6)
    c.save(); c.translate(-14, 47); c.scale(38, 14); c.arc(0, 0, 1, 0.2, 2 * math.pi + 0.5); c.restore(); c.stroke()
    c.save(); c.translate(40, 46); c.scale(0.9, 0.9)                                  # the small heart
    c.move_to(0, 6); c.curve_to(-14, -6, -6, -14, 0, -5); c.curve_to(6, -14, 14, -6, 0, 6); c.close_path(); c.fill()
    c.restore()
    c.restore()
    # her hand, from the lower right: the bracelet says whose
    c.save(); c.translate(54, 96); c.rotate(-0.55)
    kit.cut(k, [(-13, 60), (13, 60), (15, 8), (-15, 8)], so.SKIN, shadow=False, lw=2)                # the wrist
    for i, t in enumerate((-12, -6, 0, 6, 12)):
        so.pearl(k, t, 26, 5.2, 40 + i, lw=1.5)
    ellipse(k, 0, -2, 21, 19, so.SKIN, 46, shadow=False, lw=2)
    for i, (fx, ln) in enumerate(((-15, 26), (-5, 31), (5, 30), (15, 24))):
        kit.cut(k, [(fx - 5, -8), (fx + 5, -8), (fx + 5, -8 - ln), (fx - 5, -8 - ln)], so.SKIN, shadow=False, lw=1.8)
        kit.cut(k, [(fx - 4.2, -8 - ln + 9), (fx + 4.2, -8 - ln + 9), (fx + 4.2, -8 - ln), (fx - 4.2, -8 - ln)], so.RED,
                shadow=False, lw=1.2)
    c.restore()
    c.restore()


def main(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "THE ONBOARDING", 68, 44, 28, bold=True)
    corp(c, "Sofía  ·  pearls for gold, and in control", 330, 44, 13, col=GREY)
    t = "UPTIMEZ INC. · CHARACTER MODEL SHEET · " + V
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    corp(c, t, W2 - 24 - c.text_extents(t).x_advance, 30, 10, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()

    framed(c, 24, 84, 300, 560, lambda: so.sofia(k, 24 + 150, 84 + 560 - 26, 1.42, "hold", "smile", look=(-0.8, 0.0)),
           floor_h=42)
    corp(c, "AT THE DOOR", 24, 662, 11, bold=True)
    wrap(c, "Her office look from The Best Candidate. The tablet is at her hip, a sheet clipped to its back from the "
         "first beat: the CV.", 24, 678, 10, 296, col=GREY)

    def close():
        s = 2.25
        cx, feet = 342 + 165, 84 + 250 - so.HY * s
        so.sofia(k, cx, feet, s, "hold", "smile", look=(-0.6, 0.0), tablet_kind=None)
        ear = (cx + 53 * s, feet + (so.HY + 22 + 21) * s)
        mid = so.strand_pts()[6]
        callout(c, ear[0], ear[1] + 4, 342 + 322, 84 + 446, "one pearl; it swings", right=True)
        callout(c, cx + mid[0] * s, feet + mid[1] * s + 4, 342 + 150, 84 + 500, "one short strand, on the lapels")
        callout(c, 342 + 93, 84 + 536, 342 + 150, 84 + 536, "the bracelet")
    framed(c, 342, 84, 330, 560, close)
    corp(c, "THE PEARLS", 342, 662, 11, bold=True)
    wrap(c, "Drop earrings, one strand at the collarbone, a one-row bracelet on the hand that acts. White on ink-navy, "
         "with a soft shadow on the hair.", 342, 678, 10, 326, col=GREY)

    def look():
        s = 1.12
        feet = 84 + 122 - so.HY * s
        so.sofia(k, 690 + 84, feet, s, "hold", "appraise", look=(-0.8, 1.0))
        so.sofia(k, 690 + 244, feet, s, "hold", "appraise", look=(-0.8, 0.45))
        so.sofia(k, 690 + 404, feet, s, "necklace", "oh", look=(-0.8, 0.45))
    framed(c, 690, 84, 486, 250, look)
    corp(c, "EYES DOWN  ·  EYES UP  ·  \"OH...\"", 690, 352, 11, bold=True)
    wrap(c, "She reads him like a CV: half lids, her one raised eyebrow, a small closed smile. Hold the low look for "
         "six drawings. On \"Oh...\" two fingers go to the strand. No blush anywhere in this film.", 690, 368, 10, 482,
         col=GREY)

    def poses():
        F = 430 + 214 - 14
        so.sofia(k, 690 + 122, F, 0.60, "show", "smile", look=(-0.8, 0.45), lean=-5)
        so.sofia(k, 690 + 270, F, 0.60, "trophy", "knowing", look=(-0.9, 0.5))
        cv_insert(c, k, 690 + 396, 430 + 86, 0.80)
    framed(c, 690, 430, 486, 214, poses, floor_h=20)
    corp(c, "\"TAP HERE.\"  ·  THE TROPHY  ·  THE INSERT", 690, 662, 11, bold=True)
    wrap(c, "The screen is to us, so the viewer sees the one button. At the end she looks at his print like a signed "
         "deal, not a keepsake. In the inserts the bracelet says whose hand it is.", 690, 678, 10, 482, col=GREY)

    y1, hh = 756, 200
    corp(c, "THE FACES  ·  in film order (three are new: EYES DOWN / EYES UP, OH..., A BREATH; the others she already had)",
         24, y1 - 10, 10.5, col=GREY, bold=True)
    fw = (W2 - 48 - 7 * 6) / 8.0
    for i, (face, lk, lean, lab, note) in enumerate(FACES):
        x0 = 24 + i * (fw + 6)
        framed(c, x0, y1, fw, hh, lambda face=face, lk=lk, lean=lean, x0=x0: so.sofia(
            k, x0 + fw / 2, y1 + hh * 0.52 - so.HY * 0.92, 0.92, "hold", face, look=lk, lean=lean, tablet_kind=None))
        corp(c, lab, x0, y1 + hh + 15, 10, bold=True)
        corp(c, note, x0, y1 + hh + 29, 8.6, col=GREY)

    y2, lh = 1030, 330
    corp(c, "BEAT 03  ·  \"I live alone.\"  ·  \"Oh...\"", 24, y2 - 10, 10.5, col=GREY, bold=True)

    def beat():
        F = y2 + lh - 20
        s = 0.62
        s = 0.70
        co.client(k, 250, F, s, "open", "confident", look=(0.8, 0.1))
        so.sofia(k, 470, F, s, "necklace", "oh", look=(-0.9, 0.45))
        dv.don(k, 660, F, s, "stand", "shock", look=(-1, -0.1))
    framed(c, 24, y2, 820, lh, beat, floor_h=28)
    wrap(c, "IN CONTROL. With the macho she lost her cool; that was her one crack. With the Client she is choosing: "
         "sweet, calm, sure of herself.", 862, y2 + 24, 10, 310, col=GREY)
    wrap(c, "ONE GLANCE AT DON, once, after \"Oh...\": she knows. Then she never looks at him again. She is not cruel; "
         "he is simply no longer in the room.", 862, y2 + 98, 10, 310, col=GREY)
    wrap(c, "ONE PERSONAL QUESTION. Everything else she says is office language, which is why \"Everything you need is "
         "in there\" works.", 862, y2 + 172, 10, 310, col=GREY)
    wrap(c, "SHE NEVER SEES THE SHREDDER. She is looking at him.", 862, y2 + 246, 10, 310, col=GREY)

    y3 = 1392
    corp(c, "WHAT IS NEW", 24, y3, 10.5, col=GREY, bold=True)
    wrap(c, "Pearls replace the gold fringe earrings: a single drop on each ear, one short strand, a bracelet on her "
         "screen-left wrist. The tablet with the CV clipped to it, in three states. Three faces built on ones she has. "
         "Four gestures, four jobs: the smile (attraction), the look and the strand on \"Oh...\" (she finds out), the CV "
         "(she acts), the tablet (the trophy). Kept: the teal blouse, the ink-navy blazer, the gold belt, the badge, her "
         "raised eyebrow.", 24, y3 + 16, 10, W2 - 48, col=GREY)
    surf.write_to_png(out)


def phone(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1440, 640)
    c = cairo.Context(surf)
    k = Ctx(c, 0)

    def f1():                                              # at the door
        room(c, 0, 0, 360, 640, 70)
        so.sofia(k, 184, 596, 1.25, "hold", "smile", look=(-0.8, 0.0))

    def f2():                                              # the look: eyes down him (a close single: in a two-shot
        c.set_source_rgb(*kit.WALL); c.rectangle(0, 0, 360, 640); c.fill()   # her eyes are too small to read)
        so.sofia(k, 180, 300 - so.HY * 2.1, 2.1, "hold", "appraise", look=(-0.8, 1.0))

    def f3():                                              # "Oh..."
        c.set_source_rgb(*kit.WALL); c.rectangle(0, 0, 360, 640); c.fill()
        so.sofia(k, 180, 300 - so.HY * 2.1, 2.1, "necklace", "oh", look=(-0.8, 0.45))

    def f4():                                              # the trophy
        room(c, 0, 0, 360, 640, 70)
        so.sofia(k, 200, 596, 1.25, "trophy", "knowing", look=(-0.9, 0.5))
    for i, fn in enumerate((f1, f2, f3, f4)):
        c.save(); c.translate(i * 360, 0); c.rectangle(0, 0, 360, 640); c.clip()
        fn()
        c.restore()
        c.set_source_rgb(*INK); c.set_line_width(2); c.rectangle(i * 360, 0, 360, 640); c.stroke()
    surf.write_to_png(out)


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "../the-onboarding"
    main("%s/ob_sofia_%s.png" % (d, V))
    phone("%s/ob_sofia_phone_%s.png" % (d, V))
    print("wrote", d)
