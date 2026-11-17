"""v2, pinned. THE ONBOARDING: Sofia's sheet, v2 (ob_sofia_sheet_v1.py = v1, kept), after the performance audit: the design is
kept and the acting is corrected. Eyes that travel, a hand that lifts one pearl, an "Oh..." that is not surprise, one
real smile she catches, the pearl rule, and beat 03 as six shots. Writes ob_sofia_v2.png at 2400x3000 (drawn at
1200x1500, 2x) and ob_sofia_phone_v2.png (four 360x640 frames: professional, appraisal, the slip, the recovery)."""
import sys
import math
import cairo
import kit
import brand
import sofia_ob_v2 as so
import don_v4 as dv
from kit import Ctx, INK, rect, ellipse
from charsheets import corp, wrap

V = "v2"
W2, H2 = 1200, 1500
GREY = (0.35, 0.40, 0.50)
FLOOR = (0.72, 0.63, 0.50)
DOWN, UP = (-0.8, 1.0), (-0.8, -0.2)
# face, look, lean, label, note
FACES = [("smile", (-0.8, 0.0), 0, "PRACTISED", "the door, the question"),
         ("appraise", DOWN, 0, "EYES DOWN", "reading him"),
         ("appraise", UP, 0, "EYES UP", "back to his face"),
         ("oh", UP, 0, "OH...", "low, drawn out"),
         ("knowing", (1.0, 0.1), 0, "WHO NOTICED", "one glance, once"),
         ("real", (-0.6, 0.0), 0, "REAL", "half a second, beat 06"),
         ("tiny", (1.0, 0.0), 0, "CAUGHT", "she presses it back"),
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


def cv_insert(c, k, x, y, s):
    """The insert of beat 06: the sheet in her hand. An application: her portrait, lines, her number circled."""
    c.save(); c.translate(x, y); c.scale(s, s)
    c.save(); c.rotate(-0.05)
    rect(k, -62, -84, 124, 168, so.PAPER, 31, lw=2)
    rect(k, -50, -72, 38, 44, (0.98, 0.86, 0.50), 32, shadow=False, lw=1.6)
    ellipse(k, -31, -48, 11, 11, so.SKIN, 33, shadow=False, lw=1.4)
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


def device_insert(c, k, x, y, s):
    """The insert of beat 06: the screen to camera, one button, nothing else to do."""
    c.save(); c.translate(x, y); c.scale(s, s)
    c.save(); c.rotate(0.04)
    rect(k, -58, -80, 116, 160, so.TABLET, 51, lw=2)
    rect(k, -49, -70, 98, 140, so.SCREEN, 52, shadow=False, lw=1.6)
    c.set_source_rgb(0.62, 0.66, 0.72); c.set_line_width(4); c.set_line_cap(1)
    for yy, x1 in ((-52, 26), (-38, 8)):
        c.move_to(-36, yy); c.line_to(x1, yy); c.stroke()
    ellipse(k, 0, 18, 33, 33, (0.30, 0.74, 0.46), 53, shadow=False, lw=2.2)
    c.set_source_rgb(1, 1, 1); c.set_line_width(7); c.set_line_cap(1); c.set_line_join(1)
    c.move_to(-14, 18); c.line_to(-4, 29); c.line_to(16, 6); c.stroke()
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
    corp(c, "Sofía  ·  v2: the same design, the acting corrected", 330, 44, 13, col=GREY)
    t = "UPTIMEZ INC. · CHARACTER MODEL SHEET · " + V
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    corp(c, t, W2 - 24 - c.text_extents(t).x_advance, 30, 10, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()

    framed(c, 24, 84, 300, 560, lambda: so.sofia(k, 24 + 150, 84 + 560 - 26, 1.42, "hold", "smile", look=(-0.8, 0.0)),
           floor_h=42)
    corp(c, "PROFESSIONAL", 24, 662, 11, bold=True)
    wrap(c, "A straight back and the practised smile. The tablet at her hip, a sheet clipped to its back from the "
         "first beat. The pearls are not touched.", 24, 678, 10, 296, col=GREY)

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
        so.sofia(k, 690 + 84, feet, s, "low", "appraise", look=DOWN)
        so.sofia(k, 690 + 244, feet, s, "low", "appraise", look=UP)
        so.sofia(k, 690 + 404, feet, s, "necklace", "oh", look=UP)
    framed(c, 690, 84, 486, 250, look)
    corp(c, "EYES DOWN  ·  EYES UP  ·  \"OH...\"", 690, 352, 11, bold=True)
    wrap(c, "The lids, the brows and the mouth do not move; only the pupils travel. Down: on the lower rim. Up: against "
         "the lid, white below. On \"Oh...\" the lips part, one corner higher, and two fingers lift one pearl.", 690, 368,
         10, 482, col=GREY)

    def poses():
        F = 430 + 214 - 14
        so.sofia(k, 690 + 104, F, 0.60, "show", "smile", look=(-0.9, -0.15), lean=2)
        device_insert(c, k, 690 + 262, 430 + 98, 0.86)
        cv_insert(c, k, 690 + 402, 430 + 86, 0.80)
    framed(c, 690, 430, 486, 214, poses, floor_h=20)
    corp(c, "\"TAP HERE.\"  ·  THE DEVICE INSERT  ·  THE CV INSERT", 690, 662, 11, bold=True)
    wrap(c, "She presents the device and keeps her eyes on him. The insert turns the screen to camera: one button. The "
         "CV is an application: her portrait, her number circled, no heart.", 690, 678, 10, 482, col=GREY)

    y1, hh = 756, 200
    corp(c, "THE FACES  ·  professional, then interested, then back in control; and the one thing she would rather hide",
         24, y1 - 10, 10.5, col=GREY, bold=True)
    fw = (W2 - 48 - 7 * 6) / 8.0
    for i, (face, lk, lean, lab, note) in enumerate(FACES):
        x0 = 24 + i * (fw + 6)
        framed(c, x0, y1, fw, hh, lambda face=face, lk=lk, lean=lean, x0=x0: so.sofia(
            k, x0 + fw / 2, y1 + hh * 0.52 - so.HY * 0.92, 0.92, "low", face, look=lk, lean=lean))
        corp(c, lab, x0, y1 + hh + 15, 10, bold=True)
        corp(c, note, x0, y1 + hh + 29, 8.6, col=GREY)

    y2 = 1030
    corp(c, "BEAT 03 IN SIX SHOTS  ·  her action first, Don's reaction after it", 24, y2 - 10, 10.5, col=GREY, bold=True)
    sw, sh = (820 - 5 * 6) / 6.0, 250
    eyes, pearl_pt = (0, so.HY + 4), (9, so.BODY_TOP + 27)
    shots = [
        ("1  the question", "medium, eye level", lambda cx, cy: at(k, cx, cy - 18, 0.95, (0, so.HY + 40), "hold", "smile",
                                                                    look=(-0.8, -0.1), lean=-4)),
        ("2  eyes down", "tight on her eyes", lambda cx, cy: at(k, cx, cy - 8, 1.85, (0, so.HY + 12), "low", "appraise",
                                                                look=DOWN)),
        ("3  eyes up", "the same shot, held", lambda cx, cy: at(k, cx, cy - 8, 1.85, (0, so.HY + 12), "low", "appraise",
                                                                  look=UP)),
        ("4  one pearl", "fingers and strand", lambda cx, cy: at(k, cx, cy + 22, 2.3, pearl_pt, "necklace", "oh", look=UP)),
        ("5  who noticed", "her glance, once", lambda cx, cy: at(k, cx, cy - 6, 1.5, (0, so.HY + 22), "necklace", "knowing",
                                                                 look=(1.0, 0.1))),
        ("6  Don", "the reaction, after hers", lambda cx, cy: dv.don(k, cx, cy + 372, 1.25, "stand", "neutral", look=(-1, 0))),
    ]
    for i, (lab, note, fn) in enumerate(shots):
        x0 = 24 + i * (sw + 6)
        framed(c, x0, y2, sw, sh, lambda fn=fn, x0=x0: fn(x0 + sw / 2, y2 + sh / 2))
        corp(c, lab, x0, y2 + sh + 15, 10, bold=True)
        corp(c, note, x0, y2 + sh + 29, 8.6, col=GREY)
    wrap(c, "Then the Client asks the only thing he came to ask, and her opening goes nowhere.", 24, y2 + sh + 50, 10, 820,
         col=GREY)

    corp(c, "THE PEARL RULE  ·  every episode", 862, y2 - 10, 10.5, col=GREY, bold=True)
    mw, mh = (314 - 2 * 6) / 3.0, 116
    chest = (9, so.BODY_TOP + 40)
    rule = [("COMPOSED", "untouched", ("low", "smile", (-0.6, 0)), "auto"),
            ("INTERESTED", "lifts one pearl", ("necklace", "appraise", UP), "auto"),
            ("WON", "smooths her lapel", ("lapel", "knowing", (-0.5, 0.4)), "auto")]
    for i, (lab, note, (pose, face, lk), tk) in enumerate(rule):
        x0 = 862 + i * (mw + 6)
        framed(c, x0, y2, mw, mh, lambda pose=pose, face=face, lk=lk, tk=tk, x0=x0: at(
            k, x0 + mw / 2, y2 + mh / 2, 1.5, chest, pose, face, look=lk, tablet_kind=tk))
        corp(c, lab, x0, y2 + mh + 15, 10, bold=True)
        corp(c, note, x0, y2 + mh + 29, 8.6, col=GREY)
    wrap(c, "Threatened (she adjusts the strand too fast) is kept for another episode. Once an episode at most, or it "
         "becomes a tic.", 862, y2 + mh + 50, 10, 310, col=GREY)
    wrap(c, "IN CONTROL, with one thing she would rather hide: the real smile, half a second, when he respects a result. "
         "She presses it back and checks who noticed. No blush.", 862, y2 + mh + 100, 10, 310, col=GREY)
    wrap(c, "She never sees the shredder. She is looking at him.", 862, y2 + mh + 162, 10, 310, col=GREY)

    y3 = 1392
    corp(c, "WHAT CHANGED FROM v1", 24, y3, 10.5, col=GREY, bold=True)
    wrap(c, "The design is the same and is locked. The eyes are redrawn so the pupils travel (v1: the two drawings were "
         "almost one). The hand on the pearls has two fingers apart, lifting one pearl (v1: a ball and two marks). "
         "\"Oh...\" is parted lips, not a round mouth. REAL and CAUGHT are new: her one loss of composure, without a blush. "
         "The strand sits clear of the badge; in the close-ups the tablet hangs at her side. The CV has no heart. The "
         "device has its own insert. Beat 03 is laid out as shots, with Don's reaction after her action.", 24, y3 + 16, 10,
         W2 - 48, col=GREY)
    surf.write_to_png(out)


def phone(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1440, 640)
    c = cairo.Context(surf)
    k = Ctx(c, 0)

    def f1():                                              # professional
        room(c, 0, 0, 360, 640, 70)
        so.sofia(k, 184, 596, 1.25, "hold", "smile", look=(-0.8, 0.0))

    def f2():                                              # appraisal: eyes down him
        c.set_source_rgb(*kit.WALL); c.rectangle(0, 0, 360, 640); c.fill()
        so.sofia(k, 180, 300 - so.HY * 2.1, 2.1, "low", "appraise", look=DOWN, lean=-2)

    def f3():                                              # the slip: "Oh...", eyes up, one pearl
        c.set_source_rgb(*kit.WALL); c.rectangle(0, 0, 360, 640); c.fill()
        so.sofia(k, 180, 300 - so.HY * 2.1, 2.1, "necklace", "oh", look=UP)

    def f4():                                              # the recovery: she presents the device, eyes on him
        room(c, 0, 0, 360, 640, 70)
        so.sofia(k, 226, 596, 1.25, "show", "smile", look=(-0.9, -0.15), lean=2)
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
