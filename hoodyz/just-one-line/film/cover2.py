"""Cover v2 (audit 24 Nov): JUST ONE LINE. as a title (no tail: it is nobody's speech here) over the APPROVED stamp, instead of a
second APPROVED; the 47 bigger; no BUT... bubble over Hoody's body; the series bar 15 % smaller. Cover only: the film is untouched."""
import sys, os, cairo
sys.argv = ['film.py']
import film as F
P = F.P
def laptop_big(c, n=None, tick=False, glow=0.0):
    x0, x1, y0, y1 = P.LAP['x0'], P.LAP['x1'], P.LAP['y0'], P.LAP['y1']
    P.rr(c, x0, y0, x1 - x0, y1 - y0, 14); P.fs(c, P.hx('1d2233'), 7)
    P.rr(c, x0 + 14, y0 + 14, x1 - x0 - 28, y1 - y0 - 28, 8); c.set_source_rgb(*P.hx('0f1424')); c.fill()
    cx = (x0 + x1) / 2
    P.txt(c, 'FILES', cx, y0 + 48, 36, P.hx('8fd6ff'), lw=0); P.txt(c, 'CHANGED', cx, y0 + 86, 36, P.hx('8fd6ff'), lw=0)
    P.txt(c, str(n), cx - 4, y0 + 180, 150, P.hx('5df08a'), lw=0)      # (round 2: bigger again, and the small tick is gone: it competed with the chart's)
_card = P.card
def card(c, x, y, s=1.0, rot=0.0, stamp=False):                          # round 2: a stamped card shows only APPROVED, not three texts on top of each other
    if not stamp: return _card(c, x, y, s, rot, stamp)
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    P.rr(c, -95, -62, 190, 124, 10); P.fs(c, P.WHITE, 6)
    c.save(); c.rotate(-.2); P.rr(c, -86, -30, 172, 60, 8); c.set_source_rgba(.85, .1, .15, .95); c.set_line_width(7); c.stroke()
    P.txt(c, 'APPROVED', 0, 0, 38, P.hx('d0182a'), lw=0); c.restore(); c.restore()
P.card = card
_old = P.laptop; _base = _old
def laptop(c, n=None, tick=False, glow=0.0):
    _base(c, None, False, glow)                                          # the desk and the frame, without the readout
    if n is not None: laptop_big(c, n, tick, glow)
P.laptop = laptop
P.NIGHT = F.night(F.START['H'] + 58)                                  # the same night tint as in the film
S, c = F.shot_H(58)
txt = 'JUST ONE LINE.'
c.save(); c.select_font_face('Lilita One'); c.set_font_size(78); w = c.text_extents(txt).width + 110; c.restore()
P.rr(c, 540 - w / 2, 410, w, 124, 40); P.fs(c, P.WHITE, 7); P.txt(c, txt, 540, 472, 78, P.INK, lw=0)
tmp = cairo.ImageSurface(cairo.FORMAT_ARGB32, F.W, F.H); P.topbar(cairo.Context(tmp))
c.identity_matrix(); c.translate(F.W / 2, 292); c.scale(.85, .85); c.translate(-F.W / 2, -292); c.set_source_surface(tmp, 0, 0); c.paint()
S.write_to_png(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cover_v2.png'))
