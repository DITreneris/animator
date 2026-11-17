"""v1, pinned.
THE ONBOARDING: the Client's look options, v1. Three looks for the garage owner (client_ob.LOOKS), full figure
with the blueprint, two faces each, and a height line-up against Sofia, Don and the nice macho.
Writes ob_client_looks_v1.png at 2400x3000 (drawn at 1200x1500, 2x) and ob_client_looks_phone_v1.png (three
360x640 frames: each look beside Don, at the size it will have on a phone)."""
import sys
import cairo
import kit
import brand
import client_ob_v1 as co
import cand_bc as cb
import don_bc as db
import sofia_bc as sb
from kit import Ctx, INK
from charsheets import corp, wrap

V = "v1"
W2, H2 = 1200, 1500
GREY = (0.35, 0.40, 0.50)
FLOOR = (0.72, 0.63, 0.50)
NOTES = {
    "A": ("A · THE FLAT CAP", "Rust work jacket, flat cap, a salt-and-pepper moustache. The oldest-looking and the "
          "most 'garage'. The cap hides his hair, so the head is one clear shape at phone size."),
    "B": ("B · GREY TEMPLES", "Olive jacket, hair swept back and grey at the temples, a day's stubble. The most "
          "'successful owner': closest to rugged and warm, and the easiest face to act with."),
    "C": ("C · THE BEARD", "Charcoal jacket with a cream collar, short curls, a kept beard going grey at the chin. "
          "The roughest. The beard hides part of the mouth, which costs some lip-sync."),
}


def room(c, x, y, w, h, floor_h):
    c.set_source_rgb(*kit.WALL); c.rectangle(x, y, w, h); c.fill()
    c.set_source_rgb(*FLOOR); c.rectangle(x, y + h - floor_h, w, floor_h); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(1.6); c.move_to(x, y + h - floor_h); c.line_to(x + w, y + h - floor_h); c.stroke()


def framed(c, x, y, w, h, draw, floor_h=0):
    c.save(); c.rectangle(x, y, w, h); c.clip()
    if floor_h:
        room(c, x, y, w, h, floor_h)
    else:
        c.set_source_rgb(*kit.WALL); c.rectangle(x, y, w, h); c.fill()
    draw()
    c.restore()
    c.set_source_rgb(*INK); c.set_line_width(1.2); c.rectangle(x, y, w, h); c.stroke()


def main(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "THE ONBOARDING", 68, 44, 28, bold=True)
    corp(c, "the Client  ·  three looks for the garage owner  ·  pick one", 330, 44, 13, col=GREY)
    t = "UPTIMEZ INC. · LOOK OPTIONS · " + V
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    corp(c, t, W2 - 24 - c.text_extents(t).x_advance, 30, 10, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()
    wrap(c, "Brief: owns ten garages across the city and built them himself. Rugged and warm, mid-forties, a head taller "
         "than Don. A clean work jacket with a gear-and-wrench patch (a symbol, no words), a rag in the back pocket, "
         "oil in the creases of his hands, a good watch, a ring of keys with his car's fob, a VISITOR badge. The blue "
         "roll is his blueprint: the only blue thing in the film, so nothing he wears is blue.", 24, 86, 11, W2 - 48,
         col=GREY)

    bw, bh, gap = 372, 560, 18
    for i, v in enumerate("ABC"):                          # the full figure
        x0 = 24 + i * (bw + gap)
        framed(c, x0, 136, bw, bh, lambda v=v, x0=x0: co.client(k, x0 + bw / 2 + 8, 136 + bh - 26, 1.1, "roll", "warm",
                                                                look=(0.5, 0.0), variant=v, roll=True), floor_h=40)
        corp(c, NOTES[v][0], x0, 136 + bh + 22, 14, bold=True)
        wrap(c, NOTES[v][1], x0, 136 + bh + 40, 10.5, bw - 6, col=GREY)

    y1, hh = 800, 250
    corp(c, "THE FACE  ·  warm (how he arrives) and puzzled (what the office does to him)", 24, y1 - 10, 10.5, col=GREY,
         bold=True)
    for i, v in enumerate("ABC"):
        x0 = 24 + i * (bw + gap)

        def heads(v=v, x0=x0):
            for j, (face, lk) in enumerate((("warm", (0.5, 0.0)), ("puzzled", (0.7, -0.2)))):
                co.client(k, x0 + 96 + j * 180, y1 + hh * 0.50 - co.HY * 1.28, 1.28, "stand", face, look=lk, variant=v)
        framed(c, x0, y1, bw, hh, heads)

    y2, lh = 1100, 372
    corp(c, "HEIGHT LINE-UP  ·  Sofia, Don, the three looks, the nice macho from The Best Candidate", 24, y2 - 10, 10.5,
         col=GREY, bold=True)

    def lineup():
        F = y2 + lh - 22
        s = 0.66
        sb.sofia(k, 110, F, s, "stand", "smile", look=(1, 0))
        o = db.don(k, 268, F, s, "stand", "flat", look=(1, 0))
        tops = []
        for i, v in enumerate("ABC"):
            q = co.client(k, 470 + i * 196, F, s, "stand", "warm", look=(-0.5, 0), variant=v)
            tops.append(q["top"])
        cb.macho(k, 1070, F, s, "stand", "smile", look=(-0.5, 0))
        don_top = F + (db.HY - 54) * s
        c.set_source_rgb(*GREY); c.set_line_width(1.0); c.set_dash([6, 5])
        for yy in (don_top, tops[1]):
            c.move_to(40, yy); c.line_to(W2 - 40, yy); c.stroke()
        c.set_dash([])
        corp(c, "Don's crown", 48, don_top - 5, 9, col=GREY)
        corp(c, "the Client's crown: a head above Don, taller than the macho", 48, tops[1] - 5, 9, col=GREY)
    framed(c, 24, y2, W2 - 48, lh, lineup, floor_h=30)
    surf.write_to_png(out)


def phone(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1080, 640)
    c = cairo.Context(surf)
    k = Ctx(c, 0)
    for i, v in enumerate("ABC"):
        c.save(); c.translate(i * 360, 0); c.rectangle(0, 0, 360, 640); c.clip()
        room(c, 0, 0, 360, 640, 70)
        db.don(k, 300, 592, 0.92, "stand", "flat", look=(-1, -0.4))
        co.client(k, 132, 592, 0.92, "roll", "warm", look=(0.8, 0.1), variant=v, roll=True)
        c.set_source_rgb(1, 1, 1); c.rectangle(10, 10, 34, 30); c.fill()
        c.set_source_rgb(*INK); c.set_line_width(1.2); c.rectangle(10, 10, 34, 30); c.stroke()
        kit.text(k, v, 27, 33, 22, INK)
        c.restore()
        c.set_source_rgb(*INK); c.set_line_width(2); c.rectangle(i * 360, 0, 360, 640); c.stroke()
    surf.write_to_png(out)


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "../the-onboarding"
    main("%s/ob_client_looks_%s.png" % (d, V))
    phone("%s/ob_client_looks_phone_%s.png" % (d, V))
    print("wrote", d)
