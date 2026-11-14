"""Three hair/earring options for Sofía's Christmas look, side by side. Writes sofia_xmas_options_v1.png."""
import sys, cairo
import kit, sofia_xmas as sx
from kit import Ctx
from charsheets import corp
W2, H2 = 1200, 640
surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
c = cairo.Context(surf); c.scale(2, 2)
c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
k = Ctx(c, 0)
opts = [("A  ·  now: hoops, long hair", "hoops", "long", (0, 0)),
        ("B  ·  sparkling bauble earrings, long hair", "bauble", "long", (0, 0)),
        ("B in motion: earrings swing on a head turn", "bauble", "long", (7, 0)),
        ("C  ·  bauble earrings, one side braid", "bauble", "braid", (0, 0))]
for i, (lab, ear, hair, lag) in enumerate(opts):
    x = 24 + i * 292
    c.set_source_rgb(*kit.WALL); c.rectangle(x, 24, 276, 560); c.fill()
    sx.sofia(k, x + 138, 560, 1.3, "fists" if i != 2 else "stand", "neutral" if i != 2 else "unimpressed",
             look=(0, 0) if i != 2 else (0.9, 0), lag=lag, seed=71, ear=ear, hair=hair)
    corp(c, lab, x + 4, 608, 12, bold=True)
surf.write_to_png(sys.argv[1] if len(sys.argv) > 1 else "sofia_xmas_options_v1.png")
