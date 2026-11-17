"""v4, pinned.
THE ONBOARDING: the acting sheet, v4 (ob_cast_sheet_v3.py = v3, kept): the arms of acts_ob v3: the elbow hangs, and an
arm is one piece with a rounded elbow. Nothing else changed. Below, the notes of v3.
THE ONBOARDING: the acting sheet, v3 (ob_cast_sheet_v2.py = v2, kept): Sofia's hand on the pearl redrawn in curves
(sofia_ob "pearl", hands_ob.hold_pearl), with a close view of the hand alone. Below, the notes of v2.
THE ONBOARDING: the acting sheet, v2 (ob_cast_sheet_v1.py = v1, kept), after the acting audit: real hands, faces that
follow the action, the strips as a mess. Below, the notes of v1. THE ONBOARDING: the acting sheet (v1). Don, Pam and the Client in the actions script v1 gives them, and Sofia's
redrawn CAUGHT. No new costumes. Writes ob_cast_v2.png at 2400x2580 (drawn at 1200x1290, 2x) and ob_cast_phone_v2.png
(four 360x640 frames at phone size: the handover, Pam's finger, the pearl, the floor)."""
import sys
import cairo
import kit
import brand
import acts_ob as ac
import sofia_ob as so
import ob_sofia_sheet as sh
from kit import Ctx, INK
from charsheets import corp, wrap

V = "v4"
W2, H2 = 1200, 1330
GREY = (0.35, 0.40, 0.50)
FLOOR = (0.72, 0.63, 0.50)
PW, PH, GAP = (W2 - 48 - 4 * 8) / 5.0, 232, 8


def room(c, x, y, w, h, floor_h):
    c.set_source_rgb(*kit.WALL); c.rectangle(x, y, w, h); c.fill()
    if floor_h:
        c.set_source_rgb(*FLOOR); c.rectangle(x, y + h - floor_h, w, floor_h); c.fill()
        c.set_source_rgb(*INK); c.set_line_width(1.4); c.move_to(x, y + h - floor_h); c.line_to(x + w, y + h - floor_h); c.stroke()


def panel(c, x, y, w, h, draw, floor_h=18):
    c.save(); c.rectangle(x, y, w, h); c.clip()
    room(c, x, y, w, h, floor_h)
    draw(x, y, w, h)
    c.restore()
    c.set_source_rgb(*INK); c.set_line_width(1.2); c.rectangle(x, y, w, h); c.stroke()


def main(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "THE ONBOARDING", 68, 44, 28, bold=True)
    corp(c, "the acting  ·  Don, Pam, the Client, and Sofía's CAUGHT", 330, 44, 13, col=GREY)
    t = "UPTIMEZ INC. · ACTING SHEET · " + V
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    corp(c, t, W2 - 24 - c.text_extents(t).x_advance, 30, 10, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()

    F = lambda y, h: y + h - 14
    don = lambda act, s=0.60, dx=0, shred=None: (lambda x, y, w, h: (
        ac.shredder(k, x + w / 2 + dx - 40, F(y, h), s, fill=shred) if shred is not None else None,
        ac.don(k, x + w / 2 + dx, F(y, h), s, act)))
    pam = lambda act, s=0.64, dx=0: (lambda x, y, w, h: ac.pam(k, x + w / 2 + dx, F(y, h), s, act))
    cli = lambda act, s=0.46, dx=0: (lambda x, y, w, h: ac.client(k, x + w / 2 + dx, F(y, h), s, act))

    def handover(x, y, w, h):
        ac.client(k, x + 62, F(y, h), 0.40, "give")
        ac.don(k, x + 184, F(y, h), 0.40, "hand_out")

    def strips_floor(x, y, w, h):
        ac.scatter(k, x + 8, x + w - 8, F(y, h) - 2, 0.55, n=16)
        ac.pam(k, x + w / 2 + 10, F(y, h), 0.64, "kneel")

    def stand_pocket(x, y, w, h):
        ac.client(k, x + w / 2, F(y, h), 0.46, "pocket")
    rows = [
        ("DON  ·  small and tight; he never knowingly lies, he does not look", [
            ("HAND OUT", "beat 04: an open palm", don("hand_out", dx=30)),
            ("HE HAS IT", "pleased with himself", don("holds", dx=14)),
            ("SETS IT DOWN", "eyes on her, not on it", don("set_down", dx=22, shred=0.35)),
            ("LOOKS AWAY", "3.9: caught; his head goes too", don("away")),
            ("MORE PROFESSIONAL", "3.11, 6.7: not angry", don("pro")),
        ]),
        ("PAM  ·  no lines; she has already started", [
            ("TYPING", "before anyone has moved", pam("typing")),
            ("A FINGER UP", "5.1: a hand, not a stick", pam("finger", dx=-12)),
            ("SHE LOWERS IT", "5.3: eyes on Don", pam("lower", dx=-8)),
            ("EMPTY HANDS", "6.9: Sofía has the tablet", pam("empty")),
            ("THE FLOOR", "beat 09: a mess, her bare hands", strips_floor),
        ]),
        ("THE CLIENT  ·  not careless: he hands it over", [
            ("HESITATES", "4.2: it matters to him", cli("hesitate", dx=-10)),
            ("THE HANDOVER", "one action, both in frame", handover),
            ("THE WATCH", "5.4, 10.3: his eyes go to it", cli("watch")),
            ("THE STRIP", "10.1: it settles in his palm", cli("palm", dx=-16)),
            ("POCKETS IT", "10.3: his face stays with them", stand_pocket),
        ]),
    ]
    y = 86
    for title, panels in rows:
        corp(c, title, 24, y + 4, 10.5, col=GREY, bold=True)
        for i, (lab, note, fn) in enumerate(panels):
            x0 = 24 + i * (PW + GAP)
            panel(c, x0, y + 12, PW, PH, fn)
            corp(c, lab, x0, y + 12 + PH + 15, 10, bold=True)
            corp(c, note, x0, y + 12 + PH + 29, 8.6, col=GREY)
        y += 12 + PH + 52

    def hand_close(x, yy, w, h):
        import hands_ob as hd
        cx, cy = x + w / 2 - 6, yy + 74
        pts = [(cx - 78 + i * 39, cy + 30 - (30 if i == 2 else 5 if abs(i - 2) == 1 else 0)) for i in range(5)]
        c.set_source_rgb(*INK); c.set_line_width(1.6)
        c.move_to(*pts[0])
        for q in pts[1:]:
            c.line_to(*q)
        c.stroke()
        for i, q in enumerate(pts):
            so.pearl(k, q[0], q[1], 13.5 if i == 2 else 12.5, 80 + i, lw=2.0)
        hd.hold_pearl(k, pts[2][0], pts[2][1], 3.3, 0.42, so.SKIN, so.RED, 96)

    corp(c, "SOFÍA  ·  what the mute test and the audits changed", 24, y + 4, 10.5, col=GREY, bold=True)
    BUST = (0, so.HY + 22)
    sof = [
        ("REAL", "6.6: half a second", PW, lambda x, yy, w, h: sh.at(k, x + w / 2, yy + h / 2 - 8, 1.25, BUST, "low", "real",
                                                                    look=(-0.6, 0.0))),
        ("CAUGHT, redrawn", "6.7: lips flat, eyes to Don", PW * 2 + GAP,
         lambda x, yy, w, h: (sh.at(k, x + 150, yy + h / 2 - 8, 1.25, BUST, "low", "caught", look=(1.0, 0.0)),
                              ac.don(k, x + 360, yy + h / 2 + 26 + 302 * 0.82, 0.82, "pro", look=(-1.3, -0.1)))),
        ("THE PEARL", "3.7: thumb and index, one pearl", PW, lambda x, yy, w, h: sh.at(k, x + w / 2, yy + h / 2 + 4, 2.5,
                                                                                    (16, so.BODY_TOP + 18), "pearl", "oh",
                                                                                    look=(-0.9, -0.2))),
        ("THE HAND", "bent fingers, red nails; she rolls it", PW, hand_close),
    ]
    x0 = 24
    for lab, note, w, fn in sof:
        panel(c, x0, y + 12, w, PH, fn, floor_h=0)
        corp(c, lab, x0, y + 12 + PH + 15, 10, bold=True)
        corp(c, note, x0, y + 12 + PH + 29, 8.6, col=GREY)
        x0 += w + GAP
    wrap(c, "FROM v2: Sofía's hand is drawn in curves. The index finger bends in over one side of the pearl, the thumb "
         "meets it from the other, the other fingers are curled, and her red nails show. The pearl sits between the two "
         "tips and is lifted clear of the strand. In the film it rolls; her hand freezes when Don notices.", 24,
         y + 12 + PH + 52, 10, W2 - 48, col=GREY)
    surf.write_to_png(out)


def phone(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1440, 640)
    c = cairo.Context(surf)
    k = Ctx(c, 0)

    def f1():                                              # the handover
        ac.client(k, 100, 596, 0.74, "give")
        ac.don(k, 300, 596, 0.74, "hand_out")

    def f2():                                              # Pam's finger
        ac.pam(k, 170, 596, 1.25, "finger")

    def f3():                                              # the pearl
        c.set_source_rgb(*kit.WALL); c.rectangle(0, 0, 360, 640); c.fill()
        so.sofia(k, 172, 300 - so.HY * 2.1, 2.1, "pearl", "oh", look=(-0.9, -0.2))

    def f4():                                              # the floor
        ac.scatter(k, 14, 346, 588, 1.0, n=18)
        ac.pam(k, 196, 596, 1.25, "kneel")
    for i, fn in enumerate((f1, f2, f3, f4)):
        c.save(); c.translate(i * 360, 0); c.rectangle(0, 0, 360, 640); c.clip()
        room(c, 0, 0, 360, 640, 70)
        fn()
        c.restore()
        c.set_source_rgb(*INK); c.set_line_width(2); c.rectangle(i * 360, 0, 360, 640); c.stroke()
    surf.write_to_png(out)


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "../the-onboarding"
    main("%s/ob_cast_%s.png" % (d, V))
    phone("%s/ob_cast_phone_%s.png" % (d, V))
    print("wrote", d)
