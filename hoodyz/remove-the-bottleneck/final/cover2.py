"""Cover v2 (audit 24 Nov): the carry, thumb and FASTER! kept; no poster, no list on the wall (less text); HARV fully inside the
frame; the series bar 15 % smaller. Cover only: the film is untouched."""
import sys, os, cairo
sys.argv = ['film.py']; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'rough'))
import film as F
F.B.poster = lambda *a, **k: None; F.wall_list = lambda *a, **k: None
_h = F.KP.harv
F.KP.harv = lambda c_, x, gy, **k: _h(c_, x, gy, **{**k, 'clip': False})     # round 2: without the clipboard he no longer hides the first carrier's face
S = F.draw(F.START['F'] + 39, bar=False)
tmp = cairo.ImageSurface(cairo.FORMAT_ARGB32, F.W, F.H); F.KP.bar(cairo.Context(tmp))
c = cairo.Context(S); c.translate(F.W / 2, 292); c.scale(.85, .85); c.translate(-F.W / 2, -292); c.set_source_surface(tmp, 0, 0); c.paint()
S.write_to_png(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cover_v2.png'))
