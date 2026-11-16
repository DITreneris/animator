"""THE BEST CANDIDATE: technical reference v3 (faces and mouth shapes, moved off the cast sheet after the second
audit). For animation, not for judging character. Writes bc_tech_sheet_v3.png at 2400x1640 (1200x820, 2x)."""
import sys
import cairo
import kit
import brand
import cand_bc as cb
import don_bc as db
from kit import Ctx
from charsheets import corp
from pam_sheet_mf import boxed, flush

GREY = (0.35, 0.40, 0.50)
WARM = (1.0, 0.95, 0.93)
W2, H2 = 1200, 820


def main(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "THE BEST CANDIDATE", 68, 44, 28, bold=True)
    corp(c, "technical reference v3  ·  faces and mouths", 400, 44, 13, col=GREY)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()

    def box(x, y, w, h, draw, label, warm=False):
        boxed(c, x, y, w, h, label, fill=WARM if warm else (1, 1, 1))
        c.save(); c.rectangle(x, y, w, h); c.clip(); draw(); c.restore()

    rows = [
        ("1 · THE SMALL ONE", [("hopeful", "wired (default)"), ("proud", "manic"), ("neutral", "the stare"), ("crushed", "crushed")],
         lambda x, y, f, m: cb.small(k, x, y - cb.S_HY * 0.8, 0.8, "stand", f, mouth=m, seed=610), 6, 14),
        ("2 · THE NICE MACHO", [("smile", "the grin (default)"), ("warm", "warm"), ("listen", "listening"), ("gracious", "gracious")],
         lambda x, y, f, m: cb.macho(k, x, y - cb.M_HY * 0.66, 0.66, "stand", f, mouth=m, seed=710), 0, 12),
        ("DON · HEAD OF TALENT", [("flat", "flat (default)"), ("pout", "\"Too distracting.\""), ("sheepish", "sheepish"), ("beam", "beam"),
                                  ("mortified", "mortified")],
         lambda x, y, f, m: db.don(k, x, y - db.HY * 0.72, 0.72, "stand", f, mouth=m, seed=510), 0, 12),
    ]
    for r, (title, faces, draw, dy, mdy) in enumerate(rows):
        y = 92 + r * 244
        corp(c, title, 24, y - 6, 12, bold=True)
        corp(c, "FACES", 24, y + 14, 10, bold=True)
        for i, (f, lab) in enumerate(faces):
            x = 24 + i * 112
            box(x, y + 20, 106, 122, lambda x=x, f=f: draw(x + 53, y + 76 + dy, f, None), lab, warm=(i == len(faces) - 1))
        corp(c, "MOUTHS  (M E F O A C U)", 620, y + 14, 10, bold=True)
        base = faces[2][0] if r < 2 else "flat"
        for i, m in enumerate(("M", "E", "F", "O", "A", "C", "U")):
            x = 620 + i * 79
            box(x, y + 20, 74, 122, lambda x=x, m=m: draw(x + 37, y + 70 + dy, base if r != 2 else "neutral", m), m)
    flush(c)
    surf.write_to_png(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "bc_tech_sheet_v3.png")
