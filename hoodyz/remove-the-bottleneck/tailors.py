"""Remove the Bottleneck: the tailor key pose (scene C) - can MY AI's four copies read as little tailors?
Each copy has a yellow tape measure round its neck, and one prop: round glasses + notebook, a pincushion on its wrist,
a tape round his waist, a ruler held up while standing on another copy's shoulders. Hoody, arms out, flattered.
v2 (audit 23 Nov): straight arms, open palms; four different jobs (height, inside leg, waist, the spec sheet);
tapes with ticks and held ends; the bubble's tail to Hoody; the spec sheet shows a crate to his size, not a suit.
Usage: python3 tailors.py -> kp_tailors.png"""
import os, sys, math, cairo
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import office as P
from office import K, A, INK, WHITE, NAVY, YEL, RED, GREY, rr, fs, ell, limb, txt, hx, lerp, W, H, FLOOR, HS, AS
TAPE = hx('ffd23f'); PIN = hx('e8475a')

def head_of(x, gy): return (x, gy - 280 * AS)
def tape_neck(c, x, gy, s=AS):
    """A tape measure draped round its neck, both ends hanging down its chest, with tick marks."""
    hx_, hy = x, gy - 280 * s + 92 * s
    for q in (-1, 1):
        pts = [(hx_ - q * 40 * s, hy - 4 * s), (hx_ + q * 30 * s, hy + 30 * s), (hx_ + q * 46 * s, hy + 120 * s)]
        limb(c, pts, 16 * s, TAPE)
        for i in range(5):
            t = .25 + .15 * i; px = lerp(pts[1][0], pts[2][0], t); py = lerp(pts[1][1], pts[2][1], t)
            c.move_to(px - 5 * s, py); c.line_to(px + 5 * s, py); c.set_source_rgb(*INK); c.set_line_width(2.5); c.stroke()
def glasses(c, x, gy, s=AS):
    """Little round tailor's glasses, gold frames (dark frames vanish on the black visor)."""
    cx, cy = x, gy - 280 * s - 8 * s
    for q in (-1, 1): ell(c, cx + q * 38 * s, cy, 30 * s, 30 * s); c.set_source_rgb(*hx('f2c14e')); c.set_line_width(8); c.stroke()
    c.move_to(cx - 8 * s, cy); c.line_to(cx + 8 * s, cy); c.stroke()
def pincushion(c, px, py, s=AS):
    ell(c, px, py, 26 * s, 18 * s); fs(c, PIN, 5)
    for a in (-1.2, -.6, 0, .6, 1.2):
        c.move_to(px + 10 * s * math.sin(a), py - 10 * s); c.line_to(px + 26 * s * math.sin(a), py - 34 * s * math.cos(a * .5))
        c.set_source_rgb(*GREY); c.set_line_width(3); c.stroke(); ell(c, px + 26 * s * math.sin(a), py - 34 * s * math.cos(a * .5), 4, 4); fs(c, YEL, 2)
def notebook(c, px, py, s=1.0):
    """The spec sheet - and the joke under the setup: it is not a suit, it is a crate drawn to his size (arrows up, stripes)."""
    c.save(); c.translate(px, py); c.rotate(-.12); c.scale(s, s)
    rr(c, -62, -78, 124, 156, 10); fs(c, WHITE, 5)
    rr(c, -38, -44, 76, 92, 4); c.set_source_rgb(*INK); c.set_line_width(4); c.stroke()            # the crate, to his size
    for i in range(3): c.move_to(-34 + i * 24, 40); c.line_to(-22 + i * 24, 28); c.stroke()         # hazard stripes
    for dx in (-10, 10): c.move_to(dx, -6); c.line_to(dx, -30); c.move_to(dx - 7, -22); c.line_to(dx, -30); c.line_to(dx + 7, -22); c.stroke()   # this way up
    c.move_to(50, -44); c.line_to(50, 48); c.set_source_rgb(*RED); c.set_line_width(3); c.stroke()  # his height, in red
    for y in (-44, 48): c.move_to(44, y); c.line_to(56, y); c.stroke()
    c.restore()
def tape_line(c, pts, w=16):
    """A tape measure laid along a path (with tick marks), not a belt."""
    c.move_to(*pts[0])
    if len(pts) == 4: c.curve_to(*pts[1], *pts[2], *pts[3])
    else: c.line_to(*pts[1])
    c.set_source_rgb(*TAPE); c.set_line_width(w); c.stroke()
    p0, p1 = pts[0], pts[-1]; n = int(math.hypot(p1[0] - p0[0], p1[1] - p0[1]) // 22)
    for i in range(1, n):
        u = i / n
        if len(pts) == 4:
            q = [(1 - u) ** 3 * a_ + 3 * (1 - u) ** 2 * u * b_ + 3 * (1 - u) * u * u * c_ + u ** 3 * d_ for a_, b_, c_, d_ in zip(*pts)]
        else: q = [lerp(a_, b_, u) for a_, b_ in zip(p0, p1)]
        L = 7 if i % 2 else 4; c.move_to(q[0], q[1] - L); c.line_to(q[0], q[1] + L * .4)
    c.set_source_rgb(*INK); c.set_line_width(2.5); c.stroke()
def ruler(c, x, y0, y1):
    rr(c, x - 12, y0, 24, y1 - y0, 4); fs(c, hx('e8c27a'), 4)
    for i in range(int((y1 - y0) // 24)): c.move_to(x - 12, y0 + 12 + i * 24); c.line_to(x - 2 - (i % 2) * 4, y0 + 12 + i * 24); c.set_source_rgb(*INK); c.set_line_width(2); c.stroke()

def kp(c):
    P.room(c); P.desk(c); P.laptop(c); c.save(); c.translate(690, P.DESK_Y); P.mug(c, 0, 0, 1.0); c.restore()
    hx0 = 520
    # D (on the desk, right): the spec sheet, glasses on; it holds the sheet up to the light, clear of its face
    xd, gd = 920, P.DESK_Y - 18 + 60 * AS                                # sitting on the desk's edge, legs over it
    nb = (xd + 45, gd - 205)                                             # the sheet held at its chest, below its face
    old = A.limb
    A.limb = lambda c_, pts, *a: None if pts in ([(-34, 205), (-34, 280)], [(34, 205), (34, 280)]) else old(c_, pts, *a)
    pd = P.ai_pose(1, P.ai_local(xd, gd, AS, (nb[0] + 10, nb[1] + 30)), P.DOWN)
    try: A.myai(c, xd, gd, AS, eye='happy', look=(-4, 14), arms=(P.ai_pose(-1, P.ai_local(xd, gd, AS, (nb[0] - 60, nb[1] + 20)), P.DOWN), pd))
    finally: A.limb = old
    for q in (-1, 1): limb(c, [(xd + q * 34 * AS, gd - 75 * AS), (xd + q * 40 * AS, gd - 30 * AS), (xd + q * 46 * AS, gd + 50 * AS)], 34 * AS, WHITE)
    glasses(c, xd, gd); tape_neck(c, xd, gd)
    notebook(c, nb[0], nb[1], 1.15)
    # A (floor, left) steadies B on its head with one hand and runs a tape up his inside leg with the other;
    # B (on A's head) holds the ruler up beside his head
    x1, g1 = 175, FLOOR
    x2, g2 = 175, FLOOR - (280 + 95) * AS
    ankle = (hx0 - 40, FLOOR - 40); crotch = (hx0 - 8, FLOOR - 360)
    pa = P.ai_pose(1, P.ai_local(x1, g1, AS, (ankle[0] - 60, ankle[1] - 20)), P.DOWN)
    A.myai(c, x1, g1, AS, eye='happy', look=(16, 4), arms=(P.ai_pose(-1, P.ai_local(x1, g1, AS, (x1 - 60, g2 - 20)), P.UP), pa))
    tape_neck(c, x1, g1)
    rx = x2 + 175
    pb = P.ai_pose(1, P.ai_local(x2, g2, AS, (rx - 6, g2 - 330)), P.UP)
    A.myai(c, x2, g2, AS, eye='happy', look=(16, -14), rot=.04, arms=('down', pb))
    tape_neck(c, x2, g2)
    shL, shR, head = P.hoody_standing(c, hx0, FLOOR, 'smug', bow=0, gaze=0, side=1)
    ruler(c, rx, head[1] - 250, FLOOR - 10)
    hb = A.hand_at(x2, g2, AS, 1, pb); ell(c, hb[0], hb[1], 22, 22); fs(c, WHITE, 6)
    tape_line(c, [crotch, ankle], 14)                                    # the inside leg
    ha = A.hand_at(x1, g1, AS, 1, pa); ell(c, ha[0], ha[1], 22, 22); fs(c, WHITE, 6); c.move_to(ha[0] + 20, ha[1]); c.line_to(*ankle); c.set_source_rgb(*TAPE); c.set_line_width(14); c.stroke()
    # his arms straight out, palms open: being fitted
    P.hoody_arm(c, shL, (shL[0] - 280, shL[1] + 10), HS, pref=P.UP, hand='palm', ang=math.pi)       # straight out
    P.hoody_arm(c, shR, (shR[0] + 200, shR[1] - 230), HS, pref=P.DOWN, hand='palm', ang=-.8)       # lifted, as the tailor asks
    # C (right, floor): pulls the tape tight round his waist; pins on its other wrist
    x3, g3 = 760, FLOOR
    wy = FLOOR - 300 * HS - 40
    end = (hx0 + 175, wy + 30)
    tape_line(c, [(hx0 - 150, wy - 4), (hx0 - 60, wy + 40), (hx0 + 60, wy + 44), (hx0 + 148, wy + 10)], 16)
    c.move_to(hx0 + 148, wy + 10); c.line_to(*end); c.set_source_rgb(*TAPE); c.set_line_width(16); c.stroke()
    pc = P.ai_pose(-1, P.ai_local(x3, g3, AS, end), P.DOWN)
    pr = P.ai_pose(1, P.ai_local(x3, g3, AS, (x3 + 110, g3 - 300)), P.DOWN)
    A.myai(c, x3, g3, AS, eye='happy', look=(-18, -8), rot=.06, arms=(pc, pr))       # leaning back: the tape is tight
    tape_neck(c, x3, g3); pincushion(c, *A.hand_at(x3, g3, AS, 1, pr))
    P.bubble(c, ['NEW SUIT?'], 74, (head[0] + 90, head[1] - 175), 560, 470)
    P.topbar(c)

if __name__ == '__main__':
    S = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); kp(cairo.Context(S)); S.write_to_png(os.path.join(HERE, 'kp_tailors.png')); print('ok')
