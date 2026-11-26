"""Speech-bubble tails for Perfect Trip v3 - the thank-you v2 system, standalone.
One style for the whole film: a curved wedge from the bubble's edge to a tip that stops GAP px short of the speaker.
Hoody: the tip sits 20 px beside the ear at mouth height. Robot: 20 px off the head's shoulder - never the antenna.
Every box drawn is logged in BOXES for the safe-zone gate (safe.py)."""
import math
from trip_photos import R
from kit import WHITE, NAVY, rr, fs, txt

GAP = 20
SAFE = dict(x0=60, x1=960, y0=210, y1=1600)
KMAX = max(R.back(i / 200) for i in range(201))
BOXES = []                                             # (label, x0, y0, x1, y1) drawn this frame

def sit_ear(x, side=1, y=1190):                        # a seated Hoody (head radius ~140 at scale 1): beside the ear, at the mouth
    return (x + side * (141 + GAP), y)
def robot_top(x, gy, s, side=-1, dx=80):                      # MY AI: off the shoulder of the head dome, beside the antenna (head half-width 108 s)
    return (x + side * dx * s, gy - 375 * s - GAP)
def robot_side(x, gy, s, side=-1):                     # MY AI: beside the head, at visor height
    return (x + side * (108 * s + GAP), gy - 288 * s)

def _tail(c, b, tip, w, bend):
    dx, dy = tip[0] - b[0], tip[1] - b[1]; L = math.hypot(dx, dy) or 1; ux, uy = dx / L, dy / L; px, py = -uy, ux
    m = (b[0] + dx * .5 + px * L * bend, b[1] + dy * .5 + py * L * bend)
    c.move_to(b[0] - px * w / 2, b[1] - py * w / 2)
    c.curve_to(m[0] - px * w * .18, m[1] - py * w * .18, m[0] - px * w * .05, m[1] - py * w * .05, *tip)
    c.curve_to(m[0] + px * w * .05, m[1] + py * w * .05, m[0] + px * w * .22, m[1] + py * w * .22, b[0] + px * w / 2, b[1] + py * w / 2)
    c.close_path()

def bubble(c, lines, r, tip, cy=500, size=66, cx=540, bend=.16):
    """Same call as R.bubble (r = frames since it popped), tip = where the tail stops. bend > 0 curves one way, < 0 the other."""
    k = R.back(r / 5) if r < 5 else 1
    if k <= .03: return
    c.save(); c.select_font_face('Lilita One'); c.set_font_size(size)
    w = max(c.text_extents(l).width for l in lines) + 90; h = len(lines) * size * 1.12 + 56; c.restore()
    cx = min(max(cx, SAFE['x0'] + KMAX * w / 2 + 2), SAFE['x1'] - KMAX * w / 2 - 2)
    cy = min(max(cy, SAFE['y0'] + KMAX * h / 2 + 2), SAFE['y1'] - KMAX * h / 2 - 2)
    BOXES.append((' '.join(lines), cx - k * w / 2, cy - k * h / 2, cx + k * w / 2, cy + k * h / 2))
    if tip[1] > cy + h / 2: b = (min(max(tip[0], cx - w / 2 + 70), cx + w / 2 - 70), cy + h / 2 - 12)         # tip below: from the bottom edge
    elif tip[1] < cy - h / 2: b = (min(max(tip[0], cx - w / 2 + 70), cx + w / 2 - 70), cy - h / 2 + 12)
    else: b = (cx + (w / 2 - 12) * (1 if tip[0] > cx else -1), min(max(tip[1], cy - h / 2 + 40), cy + h / 2 - 40))   # tip beside: from the side
    c.save(); c.translate(cx, cy); c.scale(k, k); c.translate(-cx, -cy)
    _tail(c, b, tip, 60, bend); fs(c, WHITE, 8)
    rr(c, cx - w / 2, cy - h / 2, w, h, 40); fs(c, WHITE, 8)
    _tail(c, b, tip, 44, bend); c.set_source_rgb(*WHITE); c.fill()                      # open the seam
    lh = size * 1.12; y0 = cy - (len(lines) - 1) * lh / 2
    for i, l in enumerate(lines): txt(c, l, cx, y0 + i * lh, size, NAVY, lw=0)
    c.restore()
