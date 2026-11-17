"""v1, pinned. THE ONBOARDING: the acting sheet (v1). Don, Pam and the Client in the actions script v1 gives them, and Sofia's
redrawn CAUGHT. No new costumes. Writes ob_cast_v1.png at 2400x2580 (drawn at 1200x1290, 2x) and ob_cast_phone_v1.png
(four 360x640 frames at phone size: the handover, the set-down, Pam's finger, the floor)."""
import sys
import cairo
import kit
import brand
import acts_ob_v1 as ac
import sofia_ob as so
import ob_sofia_sheet as sh
from kit import Ctx, INK
from charsheets import corp, wrap

V = "v1"
W2, H2 = 1200, 1290
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
        for i in range(9):
            ac.strips(k, x + 20 + i * 23, F(y, h) + 6, 0.5, n=1, seed=i, fan=0.0)
        ac.pam(k, x + w / 2 + 10, F(y, h), 0.64, "kneel")

    def stand_pocket(x, y, w, h):
        ac.co.client(k, x + w / 2, F(y, h), 0.46, "stand", "confident", look=(0.6, 0.0))
    rows = [
        ("DON  ·  small and tight; he never knowingly lies, he does not look", [
            ("HAND OUT", "beat 04: an open hand", don("hand_out", dx=26)),
            ("HE HAS IT", "\"We'll take care of it.\"", don("holds", dx=14)),
            ("SETS IT DOWN", "eyes on her, not on it", don("set_down", dx=22, shred=0.35)),
            ("LOOKS AWAY", "3.9: caught staring", don("away")),
            ("THE BROWS", "3.11, 6.7: he keeps selling", don("jealous")),
        ]),
        ("PAM  ·  no lines; she has already started", [
            ("TYPING", "before anyone has moved", pam("typing")),
            ("A FINGER UP", "5.1: she saw the slot", pam("finger", dx=-12)),
            ("SHE LOWERS IT", "5.3: eyes on Don", pam("lower", dx=-8)),
            ("EMPTY HANDS", "6.9: Sofía has the tablet", pam("empty")),
            ("THE FLOOR", "beat 09: her bare hands", strips_floor),
        ]),
        ("THE CLIENT  ·  not careless: he hands it over", [
            ("GIVES IT", "4.2: to the CEO's hand", cli("give", dx=-34)),
            ("THE HANDOVER", "one action, both in frame", handover),
            ("THE WATCH", "5.4 and 10.3", cli("watch")),
            ("THE STRIP", "10.1: it settles in his palm", cli("palm", dx=-16)),
            ("POCKETS IT", "10.3: he does not know", stand_pocket),
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

    corp(c, "SOFÍA  ·  what the mute test changed", 24, y + 4, 10.5, col=GREY, bold=True)
    BUST = (0, so.HY + 22)
    sof = [
        ("REAL", "6.6: half a second", PW, lambda x, yy, w, h: sh.at(k, x + w / 2, yy + h / 2 - 8, 1.25, BUST, "low", "real",
                                                                    look=(-0.6, 0.0))),
        ("CAUGHT, redrawn", "6.7: lips flat, eyes to Don", PW * 2 + GAP,
         lambda x, yy, w, h: (sh.at(k, x + 150, yy + h / 2 - 8, 1.25, BUST, "low", "caught", look=(1.0, 0.0)),
                              ac.don(k, x + 360, yy + h / 2 + 26 + 302 * 0.82, 0.82, "jealous", look=(-1, -0.1)))),
        ("THE PEARL", "3.7: an insert, and she rolls it", PW, lambda x, yy, w, h: sh.at(k, x + w / 2, yy + h / 2 + 4, 2.3,
                                                                                    (8, so.BODY_TOP + 10), "pinch", "oh",
                                                                                    look=(-0.9, -0.2))),
    ]
    x0 = 24
    for lab, note, w, fn in sof:
        panel(c, x0, y + 12, w, PH, fn, floor_h=0)
        corp(c, lab, x0, y + 12 + PH + 15, 10, bold=True)
        corp(c, note, x0, y + 12 + PH + 29, 8.6, col=GREY)
        x0 += w + GAP
    wrap(c, "RULES FROM THE TEST. A reaction shares a frame with its cause. A turn is an action, not a glance: Pam's "
         "finger, the handover, the pearl rolled. Don's stain stays below the frame line in his reaction close-ups.",
         x0 + 4, y + 30, 10, PW - 8, col=GREY)
    wrap(c, "No new costumes: Don is his office self, Pam is as in The Best Candidate.", x0 + 4, y + 150, 10, PW - 8, col=GREY)
    surf.write_to_png(out)


def phone(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1440, 640)
    c = cairo.Context(surf)
    k = Ctx(c, 0)

    def f1():                                              # the handover
        ac.client(k, 100, 596, 0.74, "give")
        ac.don(k, 300, 596, 0.74, "hand_out")

    def f2():                                              # he stands it in the shredder, eyes on her
        ac.shredder(k, 130, 596, 1.15, fill=0.35)
        ac.don(k, 204, 596, 1.15, "set_down")

    def f3():                                              # Pam's finger
        ac.pam(k, 170, 596, 1.25, "finger")

    def f4():                                              # the floor
        for i in range(12):
            ac.strips(k, 22 + i * 29, 604, 0.8, n=1, seed=i, fan=0.0)
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
