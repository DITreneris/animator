"""THE ONBOARDING: the Client, sheet v3 (ob_client_looks_v2.py = v2, ob_client_looks_v1.py = the three look options,
both kept). Look B again, after the second design audit and the note "he is a worker, not a businessman": the same
man and the same olive, dressed and carried as the owner of ten garages. Writes ob_client_looks_v3.png at 2400x3000
(drawn at 1200x1500, 2x) and ob_client_looks_phone_v3.png (four 360x640 frames at the size they will have on a
phone)."""
import sys
import cairo
import kit
import brand
import client_ob as co
import cand_bc as cb
import don_bc as db
import sofia_bc as sb
from kit import Ctx, INK
from charsheets import corp, wrap

V = "v3"
W2, H2 = 1200, 1500
GREY = (0.35, 0.40, 0.50)
FLOOR = (0.72, 0.63, 0.50)
FACES = [("confident", "how he walks in", (0.5, 0.0)), ("warm", "to Sofia", (0.6, 0.1)),
         ("puzzled", "the pitch", (0.6, -0.1)), ("suspicious", "zero results", (0.7, 0.1)),
         ("shock", "the robot, between two palms", (0.5, 0.3)), ("exhausted", "one form", (0.2, 0.3)),
         ("relief", "one tap", (0.4, 0.2)), ("dawning", "the strip in his palm", (-0.7, 0.0))]


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


def silhouette(c, x, feet, s, **kw):
    """The figure as a flat shape: what is left of him with the face and the colours taken away."""
    sw, sh = int(340 * s), int(470 * s)
    tmp = cairo.ImageSurface(cairo.FORMAT_ARGB32, sw * 2, sh * 2)
    tc = cairo.Context(tmp); tc.scale(2, 2)
    co.client(Ctx(tc, 0), sw / 2, sh - 12 * s, s, **kw)
    c.save(); c.translate(x - sw / 2, feet - sh + 12 * s); c.scale(0.5, 0.5)
    c.set_source_rgb(0.20, 0.22, 0.28); c.mask_surface(tmp, 0, 0)
    c.restore()


def main(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "THE ONBOARDING", 68, 44, 28, bold=True)
    corp(c, "the Client  ·  look B, v3: the owner, not the mechanic", 330, 44, 13, col=GREY)
    t = "UPTIMEZ INC. · CHARACTER MODEL SHEET · " + V
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    corp(c, t, W2 - 24 - c.text_extents(t).x_advance, 30, 10, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()

    # the figure, its silhouette, and the two faces the comedy runs between
    framed(c, 24, 84, 400, 560, lambda: co.client(k, 24 + 214, 84 + 560 - 28, 1.18, "arrive", "confident",
                                                  look=(0.5, 0.0)), floor_h=42)
    corp(c, "HOW HE WALKS IN", 24, 662, 11, bold=True)
    wrap(c, "A good jacket worn open over a white shirt, a hand in his trouser pocket, the blueprint under his arm. "
         "He owns ten garages; the oil in the creases of his hands says he still opens a bonnet.", 24, 678, 10, 396,
         col=GREY)
    framed(c, 442, 84, 250, 560, lambda: silhouette(c, 442 + 150, 84 + 560 - 90, 0.85, pose="arrive",
                                                    face="confident"), fill=(0.93, 0.92, 0.88))
    corp(c, "THE SILHOUETTE", 442, 662, 11, bold=True)
    wrap(c, "The roll behind his shoulder, the jacket swept back, the elbow out from the pocket.", 442, 678, 10, 246, col=GREY)

    def pair():
        co.client(k, 710 + 126, 84 + 250 * 0.60 - co.HY * 1.36, 1.36, "open", "confident", look=(0.6, 0.0))
        co.client(k, 710 + 352, 84 + 250 * 0.60 - co.HY * 1.36, 1.36, "open", "shock", look=(0.6, 0.3))
    framed(c, 710, 84, 466, 250, pair)
    corp(c, "CONFIDENT, THEN SHOCK", 710, 352, 11, bold=True)
    wrap(c, "At ease when he walks in, not tired. The shock is his own: the brows go up unevenly, the pupils sit "
         "off-centre, the jaw drops to one side.", 710, 368, 10, 462, col=GREY)

    def poses():
        F = 420 + 224 - 16
        co.client(k, 710 + 84, F, 0.46, "offer", "warm", look=(0.7, 0.0))
        co.client(k, 710 + 256, F, 0.46, "stand", "suspicious", look=(0.7, 0.1))
        co.client(k, 710 + 392, F, 0.46, "open", "relief", look=(0.5, 0.1))
    framed(c, 710, 420, 466, 224, poses, floor_h=22)
    corp(c, "AN OPEN HAND  ·  WAITING  ·  HANDS FREE", 710, 662, 11, bold=True)
    wrap(c, "The roll leaves his arm in beat 03. After beat 06 the welcome pack sits where it was.", 710, 678, 10, 462,
         col=GREY)

    y1, hh = 742, 214
    corp(c, "THE FACES  ·  the confidence comes apart one step at a time (which beat gets which face is settled in the script)", 24, y1 - 10, 10.5, col=GREY, bold=True)
    fw = (W2 - 48 - 7 * 6) / 8.0
    for i, (face, note, lk) in enumerate(FACES):
        x0 = 24 + i * (fw + 6)
        framed(c, x0, y1, fw, hh, lambda face=face, lk=lk, x0=x0: co.client(k, x0 + fw / 2 + 3, y1 + hh * 0.60 - co.HY * 0.98,
                                                                            0.98, "open", face, look=lk))
        corp(c, face.upper(), x0, y1 + hh + 15, 10, bold=True)
        corp(c, note, x0, y1 + hh + 29, 8.6, col=GREY)

    y2, lh = 1030, 330
    corp(c, "HEIGHT LINE-UP  ·  Sofia, Don, the Client, the nice macho from The Best Candidate", 24, y2 - 10, 10.5, col=GREY,
         bold=True)

    def lineup():
        F = y2 + lh - 20
        s = 0.60
        sb.sofia(k, 150, F, s, "stand", "smile", look=(1, 0))
        db.don(k, 340, F, s, "stand", "flat", look=(1, 0))
        q = co.client(k, 600, F, s, "arrive", "confident", look=(-0.5, 0))
        cb.macho(k, 900, F, s, "stand", "smile", look=(-0.5, 0))
        don_top = F + (db.HY - 54) * s
        c.set_source_rgb(*GREY); c.set_line_width(1.0); c.set_dash([6, 5])
        for yy in (don_top, q["top"]):
            c.move_to(40, yy); c.line_to(1010, yy); c.stroke()
        c.set_dash([])
        corp(c, "Don's crown", 48, don_top - 5, 9, col=GREY)
        corp(c, "the Client's crown", 48, q["top"] - 5, 9, col=GREY)
    framed(c, 24, y2, W2 - 48, lh, lineup, floor_h=28)
    wrap(c, "Not a fourth caricature. Don, Pam and the robot make the chaos; he is the one normal adult in the room, and "
         "his reactions are what make it funny.", 1030, y2 + 60, 10, 140, col=GREY)

    y3 = 1392
    corp(c, "WHAT CHANGED FROM v2", 24, y3, 10.5, col=GREY, bold=True)
    wrap(c, "v2 read as a worker because everything he wore was a uniform: knit cuffs, a zip, a sewn company patch, a rag "
         "and a bunch of keys, under a tired face. Now: an open field jacket with a cord collar over a white open-necked "
         "shirt, a belt, shirt cuffs, the watch; the gear is a small collar pin; one car fob at the belt; a hand in the "
         "trouser pocket; a face at ease, a crooked closed smile for Sofia, a new SUSPICIOUS, a shock of his own, an open "
         "hand to shake. Kept: the body, the grey temples, the broad neck, the uneven face, the olive, VISITOR, nothing "
         "blue but the blueprint.", 24, y3 + 16, 10, W2 - 48, col=GREY)
    surf.write_to_png(out)


def phone(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1440, 640)
    c = cairo.Context(surf)
    k = Ctx(c, 0)

    def f1():                                              # he walks in: the two-second test
        room(c, 0, 0, 360, 640, 70)
        co.client(k, 176, 596, 1.0, "arrive", "confident", look=(0.7, 0.0))

    def f2():                                              # beside Don, an open hand out
        room(c, 0, 0, 360, 640, 70)
        db.don(k, 308, 592, 0.70, "stand", "flat", look=(-1, -0.4))
        co.client(k, 118, 592, 0.70, "offer", "warm", look=(0.8, 0.1))

    def f3():                                              # with Sofia: would she look twice?
        room(c, 0, 0, 360, 640, 70)
        sb.sofia(k, 296, 592, 0.72, "stand", "smile", look=(-1, -0.2))
        co.client(k, 126, 592, 0.72, "arrive", "warm", look=(0.8, 0.1))

    def f4():                                              # the robot has just come between the palms
        c.set_source_rgb(*kit.WALL); c.rectangle(0, 0, 360, 640); c.fill()
        co.client(k, 176, 330 - co.HY * 2.1, 2.1, "open", "shock", look=(0.6, 0.4))
    for i, fn in enumerate((f1, f2, f3, f4)):
        c.save(); c.translate(i * 360, 0); c.rectangle(0, 0, 360, 640); c.clip()
        fn()
        c.restore()
        c.set_source_rgb(*INK); c.set_line_width(2); c.rectangle(i * 360, 0, 360, 640); c.stroke()
    surf.write_to_png(out)


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "../the-onboarding"
    main("%s/ob_client_looks_%s.png" % (d, V))
    phone("%s/ob_client_looks_phone_%s.png" % (d, V))
    print("wrote", d)
