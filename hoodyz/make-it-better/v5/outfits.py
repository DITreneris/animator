"""Indoor outfits for Make It Better (home): Eva's options and Hoody at home. -> outfits.png"""
import os, sys, cairo
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import kp as S
from kp import R, E, txt, NAVY, hx, W, H
SOCK_H = hx('c9ced8'); SOCK_E = hx('ff8fa6')
panels = [('EVA OUTDOORS (now)', lambda c: E.eva(c, 540, 1800, 1.3)),
          ('A  SWEATER + SOCKS', lambda c: E.eva(c, 540, 1800, 1.3, outfit='sweater', cup=False, feet=SOCK_E, expr='charmed')),
          ('B  PARTY DRESS', lambda c: E.eva(c, 540, 1800, 1.3, outfit='dress', cup=False, expr='charmed')),
          ('HOODY AT HOME: SOCKS + HAT', None)]
def hoody_home(c):
    old = R.SHOE; R.SHOE = SOCK_H
    S.hoody(c, 0, 540, 1800, s=1.3, thumb=True)
    R.SHOE = old
panels[3] = (panels[3][0], hoody_home)
k = .42; sw, sh = int(W * k), int(H * k)
out = cairo.ImageSurface(cairo.FORMAT_ARGB32, 4 * (sw + 10) + 10, sh + 80); c = cairo.Context(out); c.set_source_rgb(1, 1, 1); c.paint()
for i, (name, fn) in enumerate(panels):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); cc = cairo.Context(s); S.room(cc, 0, tv_at=None); fn(cc)
    x = 10 + i * (sw + 10); c.save(); c.translate(x, 60); c.scale(k, k); c.set_source_surface(s); c.paint(); c.restore()
    txt(c, name, x + sw / 2, 32, 26, NAVY, lw=0)
out.write_to_png(os.path.join(HERE, 'outfits.png')); print('ok')
