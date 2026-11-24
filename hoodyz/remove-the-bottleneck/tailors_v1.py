"""Remove the Bottleneck: the tailor key pose (scene C) - can MY AI's four copies read as little tailors?
Each copy has a yellow tape measure round its neck, and one prop: round glasses + notebook, a pincushion on its wrist,
a tape round his waist, a ruler held up while standing on another copy's shoulders. Hoody, arms out, flattered.
Usage: python3 tailors.py -> kp_tailors.png"""
import os, sys, math, cairo
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import office as P
from office import K, A, INK, WHITE, NAVY, YEL, RED, GREY, rr, fs, ell, limb, txt, hx, lerp, W, H, FLOOR, HS, AS
TAPE = hx('ffd23f'); PIN = hx('e8475a')

def head_of(x, gy): return (x, gy - 280 * AS)
def tape_neck(c, x, gy, s=AS):
    """A tape measure draped round its neck, both ends hanging down its chest, with tick marks."""
    hx_, hy = x, gy - 280 * AS + 92 * s
    for q in (-1, 1):
        pts = [(hx_ - q * 40 * s, hy - 4 * s), (hx_ + q * 30 * s, hy + 30 * s), (hx_ + q * 46 * s, hy + 120 * s)]
        limb(c, pts, 16 * s, TAPE)
        for i in range(5):
            t = .25 + .15 * i; px = lerp(pts[1][0], pts[2][0], t); py = lerp(pts[1][1], pts[2][1], t)
            c.move_to(px - 5 * s, py); c.line_to(px + 5 * s, py); c.set_source_rgb(*INK); c.set_line_width(2.5); c.stroke()
def glasses(c, x, gy, s=AS):
    """Little round tailor's glasses, gold frames (dark frames vanish on the black visor)."""
    cx, cy = x, gy - 280 * AS - 8 * s
    for q in (-1, 1): ell(c, cx + q * 38 * s, cy, 30 * s, 30 * s); c.set_source_rgb(*hx('f2c14e')); c.set_line_width(8); c.stroke()
    c.move_to(cx - 8 * s, cy); c.line_to(cx + 8 * s, cy); c.stroke()
def pincushion(c, px, py, s=AS):
    ell(c, px, py, 26 * s, 18 * s); fs(c, PIN, 5)
    for a in (-1.2, -.6, 0, .6, 1.2):
        c.move_to(px + 10 * s * math.sin(a), py - 10 * s); c.line_to(px + 26 * s * math.sin(a), py - 34 * s * math.cos(a * .5))
        c.set_source_rgb(*GREY); c.set_line_width(3); c.stroke(); ell(c, px + 26 * s * math.sin(a), py - 34 * s * math.cos(a * .5), 4, 4); fs(c, YEL, 2)
def notebook(c, px, py, s=1.0):
    c.save(); c.translate(px, py); c.rotate(-.15); rr(c, -40, -54, 80, 108, 8); fs(c, WHITE, 5)
    for i in range(4): c.move_to(-26, -30 + i * 20); c.line_to(26 - (i == 3) * 20, -30 + i * 20); c.set_source_rgb(*GREY); c.set_line_width(3); c.stroke()
    c.restore()
def ruler(c, x, y0, y1):
    rr(c, x - 12, y0, 24, y1 - y0, 4); fs(c, hx('e8c27a'), 4)
    for i in range(int((y1 - y0) // 24)): c.move_to(x - 12, y0 + 12 + i * 24); c.line_to(x - 2 - (i % 2) * 4, y0 + 12 + i * 24); c.set_source_rgb(*INK); c.set_line_width(2); c.stroke()

def kp(c):
    P.room(c); P.desk(c); P.laptop(c); c.save(); c.translate(690, P.DESK_Y); P.mug(c, 0, 0, 1.0); c.restore()
    hx0 = 520
    # copy D sits on the desk behind, glasses on, writing the measurements down (its face clear of the notebook)
    xd, gd = 900, P.DESK_Y + 40
    nb = (xd + 120, gd - 250)
    A.myai(c, xd, gd, AS, eye='happy', look=(-16, 6), arms=(P.ai_pose(-1, P.ai_local(xd, gd, AS, (nb[0] - 150, nb[1] + 30)), P.DOWN), P.ai_pose(1, P.ai_local(xd, gd, AS, nb), P.DOWN)))
    notebook(c, nb[0] + 20, nb[1] - 30); glasses(c, xd, gd); tape_neck(c, xd, gd)
    # copy A on the floor, left; copy B stands on its head and holds the ruler up beside his
    x1, g1 = 175, FLOOR
    x2, g2 = 175, FLOOR - (280 + 95) * AS
    A.myai(c, x1, g1, AS, eye='happy', look=(14, -18), arms=(P.ai_pose(-1, P.ai_local(x1, g1, AS, (x1 - 70, g2 - 30)), P.UP), P.ai_pose(1, P.ai_local(x1, g1, AS, (x1 + 70, g2 - 30)), P.UP)))
    tape_neck(c, x1, g1)
    rx = x2 + 175
    A.myai(c, x2, g2, AS, eye='happy', look=(16, -14), rot=.04, arms=('down', P.ai_pose(1, P.ai_local(x2, g2, AS, (rx - 6, g2 - 330)), P.UP)))
    tape_neck(c, x2, g2)
    shL, shR, head = P.hoody_standing(c, hx0, FLOOR, 'smug', bow=0, gaze=0, side=1)
    ruler(c, rx, head[1] - 250, FLOOR - 10)
    A.myai  # (B's hand is over the ruler: drawn again below)
    hb = A.hand_at(x2, g2, AS, 1, P.ai_pose(1, P.ai_local(x2, g2, AS, (rx - 6, g2 - 330)), P.UP)); ell(c, hb[0], hb[1], 22, 22); fs(c, WHITE, 6)
    # his arms out, like at the tailor's, over everyone
    P.hoody_arm(c, shL, (shL[0] - 210, shL[1] - 40), HS, pref=P.UP, hand='palm')
    P.hoody_arm(c, shR, (shR[0] + 210, shR[1] - 40), HS, pref=P.UP, hand='palm')
    # copy C, right: pulls the tape round his waist; a pincushion on its other wrist
    x3, g3 = 830, FLOOR
    waist = (hx0, FLOOR - 300 * HS - 40)
    tr = (hx0 + 150, waist[1] + 6); tl = (hx0 - 150, waist[1])
    c.move_to(tl[0], tl[1]); c.curve_to(hx0 - 60, waist[1] + 46, hx0 + 60, waist[1] + 46, tr[0], tr[1]); c.set_source_rgb(*TAPE); c.set_line_width(16); c.stroke()
    pc = P.ai_pose(-1, P.ai_local(x3, g3, AS, (tr[0] + 20, tr[1] + 10)), P.DOWN)
    A.myai(c, x3, g3, AS, eye='happy', look=(-18, -8), arms=(pc, P.ai_pose(1, P.ai_local(x3, g3, AS, (x3 + 120, g3 - 330)), P.DOWN)))
    tape_neck(c, x3, g3); pincushion(c, *A.hand_at(x3, g3, AS, 1, P.ai_pose(1, P.ai_local(x3, g3, AS, (x3 + 120, g3 - 330)), P.DOWN)))
    P.bubble(c, ['NEW SUIT?'], 74, (head[0] + 40, head[1] - 210), 560, 520)
    P.topbar(c)

if __name__ == '__main__':
    S = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); kp(cairo.Context(S)); S.write_to_png(os.path.join(HERE, 'kp_tailors.png')); print('ok')
