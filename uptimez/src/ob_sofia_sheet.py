"""THE ONBOARDING: Sofia's sheet, v3 (ob_sofia_sheet_v2.py = v2, ob_sofia_sheet_v1.py = v1, both kept), after the
second performance audit: an "interested" face of her own (the look no longer reads as sarcasm), a smaller "Oh...",
fingertips together under one pearl, a recovery that keeps a trace of the smile, and two props instead of one that
changes: her clipboard, Pam's tablet. Writes ob_sofia_v3.png at 2400x3000 (drawn at 1200x1500, 2x) and
ob_sofia_phone_v3.png (four 360x640 frames: control, interest, betrayal, recovery). The reaction chain with Don and
the Client is a storyboard, not a sheet: ob_chain.py."""
import sys
import math
import cairo
import kit
import brand
import sofia_ob as so
import don_v4 as dv
from kit import Ctx, INK, rect, ellipse
from charsheets import corp, wrap

V = "v3"
W2, H2 = 1200, 1500
GREY = (0.35, 0.40, 0.50)
FLOOR = (0.72, 0.63, 0.50)
DOWN, UP = (-0.8, 1.0), (-0.8, -0.2)
# face, look, lean, label, note
FACES = [("smile", (-0.8, 0.0), 0, "PRACTISED", "the door, the question"),
         ("appraise", DOWN, 0, "EYES DOWN", "reading him"),
         ("appraise", UP, 0, "EYES UP", "still reading"),
         ("interested", (-0.9, -0.2), 0, "INTERESTED", "she likes what she read"),
         ("oh", (-0.9, -0.2), 0, "OH...", "small, low, drawn out"),
         ("recover", (-0.8, -0.1), 0, "RECOVERED", "a moment too late"),
         ("real", (-0.6, 0.0), 0, "REAL", "half a second, beat 06"),
         ("tiny", (1.0, 0.0), 0, "CAUGHT", "she presses it back")]


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


def at(k, cx, cy, s, local, *a, **kw):
    """Draw her so that the point `local` (her own coordinates, feet at 0, 0) lands on (cx, cy)."""
    return so.sofia(k, cx - local[0] * s, cy - local[1] * s, s, *a, **kw)


def callout(c, x0, y0, x1, y1, label, right=False):
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(x0, y0); c.line_to(x1, y1); c.stroke()
    c.arc(x0, y0, 2.6, 0, 2 * math.pi); c.fill()
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    w = c.text_extents(label).x_advance
    tx = x1 - w - 8 if right else x1 + 8
    c.set_source_rgb(1, 1, 1); c.rectangle(tx - 6, y1 - 10, w + 12, 20); c.fill_preserve()
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.0); c.stroke()
    corp(c, label, tx, y1 + 3.5, 10, bold=True)


def hand_insert(c, k, x, y, ang, seed=40):
    """Her hand in an insert, from below: the bracelet says whose."""
    c.save(); c.translate(x, y); c.rotate(ang)
    kit.cut(k, [(-13, 60), (13, 60), (15, 8), (-15, 8)], so.SKIN, shadow=False, lw=2)
    for i, t in enumerate((-12, -6, 0, 6, 12)):
        so.pearl(k, t, 26, 5.2, seed + i, lw=1.5)
    ellipse(k, 0, -2, 21, 19, so.SKIN, seed + 6, shadow=False, lw=2)
    for fx, ln in ((-15, 26), (-5, 31), (5, 30), (15, 24)):
        kit.cut(k, [(fx - 5, -8), (fx + 5, -8), (fx + 5, -8 - ln), (fx - 5, -8 - ln)], so.SKIN, shadow=False, lw=1.8)
        kit.cut(k, [(fx - 4.2, -8 - ln + 9), (fx + 4.2, -8 - ln + 9), (fx + 4.2, -8 - ln), (fx - 4.2, -8 - ln)], so.RED,
                shadow=False, lw=1.2)
    c.restore()


def cv_insert(c, k, x, y, s, hers=False):
    """The insert of beat 06: the sheet in her hand. An application: her portrait, lines, her number circled.
    hers (opt-in, the animation): the portrait has her blonde hair, on a blue ground. Two cold viewers took the bare
    face for a bald man's and could not tell whose CV it was."""
    c.save(); c.translate(x, y); c.scale(s, s)
    c.save(); c.rotate(-0.05)
    rect(k, -62, -84, 124, 168, so.PAPER, 31, lw=2)
    rect(k, -50, -72, 38, 44, (0.74, 0.84, 0.94) if hers else (0.98, 0.86, 0.50), 32, shadow=False, lw=1.6)
    if hers:
        blonde = (0.97, 0.86, 0.52)
        kit.cut(k, [(-46, -31), (-45, -52), (-40, -63), (-31, -67), (-22, -63), (-17, -52), (-16, -31)], blonde, shadow=False, lw=1.5)
    ellipse(k, -31, -48, 11, 11, so.SKIN, 33, shadow=False, lw=1.4)
    if hers:
        kit.cut(k, [(-43, -50), (-40, -61), (-31, -64), (-22, -61), (-19, -50), (-24, -56), (-33, -58), (-39, -55)], blonde,
                shadow=False, lw=1.3)
    c.set_source_rgb(*so.RED); c.set_line_width(2); c.move_to(-35, -43); c.line_to(-27, -43); c.stroke()
    c.set_source_rgb(*INK); c.select_font_face("Inter", 0, 1); c.set_font_size(15); c.move_to(-4, -58); c.show_text("CV")
    c.set_source_rgb(0.62, 0.62, 0.64); c.set_line_width(3); c.set_line_cap(1)
    for yy, x0, x1 in ((-46, -4, 46), (-36, -4, 38), (-14, -50, 48), (-3, -50, 40), (8, -50, 46), (19, -50, 30)):
        c.move_to(x0, yy); c.line_to(x1, yy); c.stroke()
    c.set_source_rgb(*INK); c.select_font_face("Inter", 0, 1); c.set_font_size(12.5); c.move_to(-44, 52); c.show_text("555 0142")
    c.set_source_rgb(*so.RED); c.set_line_width(2.6)
    c.save(); c.translate(-14, 47); c.scale(38, 14); c.arc(0, 0, 1, 0.2, 2 * math.pi + 0.5); c.restore(); c.stroke()
    c.restore()
    hand_insert(c, k, 54, 96, -0.55)
    c.restore()


def device_insert(c, k, x, y, s, done=False):
    """The insert of beat 06: Pam's tablet, the screen to camera. Before the tap: one button. After: a tick and his
    thumbprint. The same screen, two states; never the tick before the tap."""
    c.save(); c.translate(x, y); c.scale(s, s)
    c.save(); c.rotate(0.04)
    rect(k, -58, -80, 116, 160, so.TABLET, 51, lw=2)
    rect(k, -49, -70, 98, 140, so.SCREEN, 52, shadow=False, lw=1.6)
    c.set_source_rgb(0.62, 0.66, 0.72); c.set_line_width(4); c.set_line_cap(1)
    for yy, x1 in ((-52, 26), (-38, 8)):
        c.move_to(-36, yy); c.line_to(x1, yy); c.stroke()
    so.button(k, 0, 20, 29, done=done, seed=53)
    c.restore()
    hand_insert(c, k, 62, 92, -0.50, seed=60)
    c.restore()


def main(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "THE ONBOARDING", 68, 44, 28, bold=True)
    corp(c, "Sofía  ·  v3: interest that reads as interest", 330, 44, 13, col=GREY)
    t = "UPTIMEZ INC. · CHARACTER MODEL SHEET · " + V
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    corp(c, t, W2 - 24 - c.text_extents(t).x_advance, 30, 10, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()

    framed(c, 24, 84, 300, 560, lambda: so.sofia(k, 24 + 150, 84 + 560 - 26, 1.42, "hold", "smile", look=(-0.8, 0.0)),
           floor_h=42)
    corp(c, "PROFESSIONAL", 24, 662, 11, bold=True)
    wrap(c, "A straight back and the practised smile. Her clipboard at her hip, her CV on it from the first beat. "
         "The pearls are not touched.", 24, 678, 10, 296, col=GREY)

    def close():
        s = 2.25
        cx, feet = 342 + 165, 84 + 250 - so.HY * s
        so.sofia(k, cx, feet, s, "hold", "smile", look=(-0.6, 0.0))
        ear = (cx + 53 * s, feet + (so.HY + 22 + 21) * s)
        mid = so.strand_pts()[6]
        callout(c, ear[0], ear[1] + 4, 342 + 322, 84 + 446, "one pearl; it swings", right=True)
        callout(c, cx + mid[0] * s, feet + mid[1] * s + 4, 342 + 150, 84 + 500, "one short strand")
        callout(c, 342 + 93, 84 + 536, 342 + 150, 84 + 536, "the bracelet")
    framed(c, 342, 84, 330, 560, close)
    corp(c, "THE PEARLS  ·  locked", 342, 662, 11, bold=True)
    wrap(c, "Drop earrings, one strand at the collarbone, a one-row bracelet on the hand that acts. White on ink-navy, "
         "with a soft shadow on the hair.", 342, 678, 10, 326, col=GREY)

    def look():
        s = 1.12
        feet = 84 + 122 - so.HY * s
        so.sofia(k, 690 + 84, feet, s, "low", "appraise", look=UP)
        so.sofia(k, 690 + 244, feet, s, "low", "interested", look=(-0.9, -0.2))
        so.sofia(k, 690 + 404, feet, s, "necklace", "oh", look=(-0.9, -0.2))
    framed(c, 690, 84, 486, 250, look)
    corp(c, "READING HIM  ·  INTERESTED  ·  \"OH...\"", 690, 352, 11, bold=True)
    wrap(c, "While she reads him the face is fixed and only the pupils travel. Then it answers: the lids relax, the arched "
         "brow comes down, both soften. On \"Oh...\" the lips barely part, and two fingertips, together, lift one pearl.",
         690, 368, 10, 482, col=GREY)

    def poses():
        F = 430 + 214 - 14
        so.sofia(k, 690 + 84, F, 0.60, "show", "recover", look=(-0.9, -0.15), lean=2)
        device_insert(c, k, 690 + 204, 430 + 96, 0.70)
        device_insert(c, k, 690 + 312, 430 + 96, 0.70, done=True)
        cv_insert(c, k, 690 + 418, 430 + 90, 0.70)
    framed(c, 690, 430, 486, 214, poses, floor_h=20)
    corp(c, "\"TAP HERE.\"  ·  BEFORE THE TAP  ·  AFTER IT  ·  THE CV", 690, 662, 11, bold=True)
    wrap(c, "Two props. The clipboard is hers; taking Pam's tablet, she tucks it under her arm. The button is a disc "
         "in a ring; the tick and his thumbprint come only after the tap. The CV: a number circled, no heart.", 690, 678,
         10, 482, col=GREY)

    y1, hh = 756, 200
    corp(c, "THE FACES  ·  control, reading, interest, betrayal, recovery; and the one thing she would rather hide",
         24, y1 - 10, 10.5, col=GREY, bold=True)
    fw = (W2 - 48 - 7 * 6) / 8.0
    for i, (face, lk, lean, lab, note) in enumerate(FACES):
        x0 = 24 + i * (fw + 6)
        framed(c, x0, y1, fw, hh, lambda face=face, lk=lk, lean=lean, x0=x0: so.sofia(
            k, x0 + fw / 2, y1 + hh * 0.52 - so.HY * 0.92, 0.92, "low", face, look=lk, lean=lean))
        corp(c, lab, x0, y1 + hh + 15, 10, bold=True)
        corp(c, note, x0, y1 + hh + 29, 8.6, col=GREY)

    y2 = 1030
    corp(c, "BEAT 03, THE CHAIN  ·  her action, his reaction, her recovery (the full strip: ob_chain)", 24, y2 - 10, 10.5, col=GREY, bold=True)
    sw, sh = (820 - 5 * 6) / 6.0, 250
    eyes, pearl_pt = (0, so.HY + 4), (9, so.BODY_TOP + 27)
    shots = [
        ("1  she reads him", "tight on her eyes", lambda cx, cy: at(k, cx, cy - 8, 1.85, (0, so.HY + 12), "low", "appraise",
                                                                    look=DOWN)),
        ("2  she likes it", "the same shot, held", lambda cx, cy: at(k, cx, cy - 8, 1.85, (0, so.HY + 12), "low", "interested",
                                                                     look=(-0.9, -0.2))),
        ("3  one pearl", "fingers and strand", lambda cx, cy: at(k, cx, cy + 22, 2.3, pearl_pt, "necklace", "oh",
                                                                 look=(-0.9, -0.2))),
        ("4  Don sees it", "his reaction, after hers", lambda cx, cy: dv.don(k, cx, cy + 372, 1.25, "stand", "neutral",
                                                                             look=(-1, 0.3))),
        ("5  she catches him", "and does not flinch", lambda cx, cy: at(k, cx, cy - 6, 1.5, (0, so.HY + 22), "necklace",
                                                                        "sideeye", look=(1.0, 0.1))),
        ("6  recovered", "a moment too late", lambda cx, cy: at(k, cx, cy - 6, 1.5, (0, so.HY + 22), "low", "recover",
                                                                look=(-0.8, -0.1))),
    ]
    for i, (lab, note, fn) in enumerate(shots):
        x0 = 24 + i * (sw + 6)
        framed(c, x0, y2, sw, sh, lambda fn=fn, x0=x0: fn(x0 + sw / 2, y2 + sh / 2))
        corp(c, lab, x0, y2 + sh + 15, 10, bold=True)
        corp(c, note, x0, y2 + sh + 29, 8.6, col=GREY)
    wrap(c, "Then Don knows, and the Client, who saw none of it, asks the only thing he came to ask.", 24, y2 + sh + 50, 10, 820,
         col=GREY)

    corp(c, "THE PEARL RULE  ·  every episode", 862, y2 - 10, 10.5, col=GREY, bold=True)
    mw, mh = (314 - 2 * 6) / 3.0, 116
    chest = (9, so.BODY_TOP + 40)
    rule = [("COMPOSED", "untouched", ("low", "smile", (-0.6, 0)), "auto"),
            ("INTERESTED", "lifts one pearl", ("necklace", "interested", (-0.9, -0.2)), "auto"),
            ("WON", "smooths her lapel", ("lapel", "knowing", (-0.5, 0.4)), "auto")]
    for i, (lab, note, (pose, face, lk), tk) in enumerate(rule):
        x0 = 862 + i * (mw + 6)
        framed(c, x0, y2, mw, mh, lambda pose=pose, face=face, lk=lk, tk=tk, x0=x0: at(
            k, x0 + mw / 2, y2 + mh / 2, 1.5, chest, pose, face, look=lk, tablet_kind=tk))
        corp(c, lab, x0, y2 + mh + 15, 10, bold=True)
        corp(c, note, x0, y2 + mh + 29, 8.6, col=GREY)
    wrap(c, "Threatened (she adjusts the strand too fast) is kept for another episode. Once an episode at most, or it "
         "becomes a tic.", 862, y2 + mh + 50, 10, 310, col=GREY)
    wrap(c, "WHAT SHE FEELS AGAINST WHAT SHE SHOWS. She hides the feeling, never her calm: when Don sees the pearl she "
         "looks straight back at him. The real smile, half a second, is the one thing that gets out. No blush.", 862,
         y2 + mh + 100, 10, 310, col=GREY)
    wrap(c, "Locked: the design and these intentions. Not locked: the exact drawings.", 862, y2 + mh + 176, 10, 310, col=GREY)

    y3 = 1392
    corp(c, "WHAT CHANGED FROM v2", 24, y3, 10.5, col=GREY, bold=True)
    wrap(c, "INTERESTED is new: the look was built on her unimpressed face and read as sarcasm; now the reading ends in "
         "relaxed lids and softened brows. \"Oh...\" is smaller. The two fingertips are together (apart, they were a "
         "V-sign) and one pearl rises clear of the rest. RECOVERED is new: she never goes back to the plain smile after "
         "the look. Two props instead of one that changed: her clipboard and Pam's tablet. The button is a disc until it "
         "is tapped. The chain now runs action, reaction, recovery.", 24, y3 + 16, 10, W2 - 48, col=GREY)
    surf.write_to_png(out)


def phone(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1440, 640)
    c = cairo.Context(surf)
    k = Ctx(c, 0)

    def f1():                                              # professional
        room(c, 0, 0, 360, 640, 70)
        so.sofia(k, 184, 596, 1.25, "hold", "smile", look=(-0.8, 0.0))

    def f2():                                              # interest: she likes what she read
        c.set_source_rgb(*kit.WALL); c.rectangle(0, 0, 360, 640); c.fill()
        so.sofia(k, 180, 300 - so.HY * 2.1, 2.1, "low", "interested", look=(-0.9, -0.2), lean=-2)

    def f3():                                              # betrayal: one pearl moves
        c.set_source_rgb(*kit.WALL); c.rectangle(0, 0, 360, 640); c.fill()
        so.sofia(k, 180, 300 - so.HY * 2.1, 2.1, "necklace", "oh", look=(-0.9, -0.2))

    def f4():                                              # recovery: the device, her eyes still on him
        room(c, 0, 0, 360, 640, 70)
        so.sofia(k, 222, 596, 1.25, "show", "recover", look=(-0.9, -0.15), lean=2)
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
