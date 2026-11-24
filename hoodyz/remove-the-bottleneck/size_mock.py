"""Remove the Bottleneck: size study (Tomas, 24 Nov: "aren't the robots too big? they don't read as small and innocent").
Three sizes for the COPIES (MY AI itself keeps the series size): 1.0 (now), 0.8 (the cartoon's height), 0.68 (four fit
side by side). Top row: the four with Hoody. Bottom row: the carry, HARV at the series size. -> size_mock.png"""
import os, sys, math, cairo
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'rough'))
import office as P, setb as B, kp as KP, film as F
from office import A, INK, WHITE, NAVY, txt, hx, lerp, W, H, FLOOR, HS, AS
RW = 367                                                                # one robot's width at the series size, ears included
def four(c, k):
    B.room(c); B.board(c, *F.BOARD); B.crate(c, F.CX, FLOOR, lid=1, slot=True, slot_x=50)
    shL, shR, head = F.hoody(c, 800, 'smug', side=-1); F.mug_arm(c, shL)
    P.hoody_arm(c, shR, (shR[0] + 60, shR[1] + 180), HS, pref=P.RIGHT, hand='grip')
    w = RW * k; n = 4; span = 640 - 30; step = min(w + 14, (span - w) / (n - 1))
    for i in range(n):
        A.myai(c, 30 + w / 2 + i * step, FLOOR, AS * k, eye='happy' if i % 2 == 0 else 'open', look=(16, -10), arms=('wave' if i == 1 else 'down', 'down'))
    KP.bar(c)
def carry(c, k):
    B.room(c); B.board(c, *F.BOARD)
    ht = FLOOR - (280 + 95) * AS * k - 10; x0 = 330
    for i, dx in enumerate((70, 235, 400, 565)):
        A.myai(c, x0 + dx, FLOOR, AS * k, eye='happy' if i % 2 == 0 else 'open', look=(-16, -4), walk=i * 1.6, arms=('up', 'up'))
    sl = B.crate(c, x0, ht, lid=0, stamp=1.0, slot=True, slot_x=50, rot=.02)
    F.thumb_up(c, sl, 1.0)
    KP.harv(c, 150, FLOOR + 10, mouth='fond')
    KP.bar(c)
if __name__ == '__main__':
    ks = (1.0, .8, .68); s = .33; sw, sh = int(W * s), int(H * s)
    out = cairo.ImageSurface(cairo.FORMAT_RGB24, 3 * sw + 40, 2 * sh + 110); c = cairo.Context(out); c.set_source_rgb(1, 1, 1); c.paint()
    for j, fn in enumerate((four, carry)):
        for i, k in enumerate(ks):
            S = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); fn(cairo.Context(S), k)
            c.save(); c.translate(10 + i * (sw + 10), 70 + j * (sh + 10)); c.scale(s, s); c.set_source_surface(S); c.paint(); c.restore()
    for i, (k, name) in enumerate(zip(ks, ('1.0  now', '0.8  the cartoon', '0.68  four fit'))):
        txt(c, name, 10 + i * (sw + 10) + sw / 2, 36, 30, NAVY, lw=0)
    out.write_to_png(os.path.join(HERE, 'size_mock.png')); print('ok')
