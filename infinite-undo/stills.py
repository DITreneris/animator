"""Key poses for review. Usage: python3 stills.py 07 [..]  ->  still_07.png"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import cairo
import undo as U
from undo import R, K, Sh, A, DESK, W, H

AI_X, AI_GY, AI_S = 850, 1207, .9           # MY AI behind the desk, behind the cat: the chest disc just above the cat's back
HOODY_X, HOODY_SEAT = 190, 1330

def hoody_lunge(c, f, rot=.22, expr='shock'):
    R.hoody(c, HOODY_X, HOODY_SEAT, 1.0, expr=expr, pose='sit', arms=('rest', 'out'), rot=rot, f=f, blink=False)

def shot07(c, f=0):
    """The human fountain: the cat drinks from the arc and works UNDO with its tail; Hoody rocks in his lunge; ITS DRINK."""
    c.save(); c.translate(540, 1100); c.scale(1.25, 1.25); c.translate(-540, -1060)   # the wide, framed tight on the gag
    U.room(c)
    A.myai(c, AI_X, AI_GY, AI_S, eye='happy', arms=('offer', 'down'), tilt=-6)
    cx, cy, r = U.undo_disc(c, AI_X, AI_GY, AI_S, glow=1.0, press=.6)
    U.ghost(c, lambda c: hoody_lunge(c, f, rot=.08), -50, op=.28)                 # where he was a moment ago
    U.cyan_rim(c, lambda c: hoody_lunge(c, f), width=9)
    U.chevrons(c, 120, 900, .9, n=2)
    U.desk_front(c)
    U.laptop(c, 500, DESK)
    lip = U.glass(c, 300, DESK, tip=1.05, fill=.35)
    mouth = U.cat_drink(c, 790, DESK + 4, .85, f, lap=1.0, tail_to=(cx + 20, cy + 22))
    pts = U.arc_pts(lip, mouth, 990)
    U.water(c, pts, f, rewind=1.0, pulse=1.0)
    U.chevrons(c, *pts[8], .7, n=2, ang=math.atan2(pts[9][1] - pts[7][1], pts[9][0] - pts[7][0]))
    U.counter(c, 560, 850, 12, k=.85)
    c.restore()
    Sh.topbar(c, 'ITS DRINK')

SHOTS = {'07': shot07}
if __name__ == '__main__':
    for k in sys.argv[1:]:
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
        SHOTS[k](c, 0); s.write_to_png(os.path.join(HERE, f'still_{k}.png')); print('ok', k)
