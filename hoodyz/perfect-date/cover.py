"""Perfect Date cover: the gap wide (him in the sky, the couple walking off below) with the title. Writes cover.png."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import cairo, render as R
from kit import txt, NAVY, WHITE, YEL, INK

f = R.SHOTS[13][1] + 18                                                  # shot 14, the heart up over the couple
S = R.draw(f); c = cairo.Context(S)
c.save(); c.translate(690, 560); c.rotate(-.05)
txt(c, 'PERFECT', 0, 0, 150, YEL, lw=14)
txt(c, 'DATE', 0, 150, 190, WHITE, lw=16)
c.restore()
S.write_to_png(os.path.join(HERE, 'cover.png')); print('cover ok, frame', f)
