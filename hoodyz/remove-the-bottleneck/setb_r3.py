"""Remove the Bottleneck: set B (Tomas, 23 Nov): its own office. A dark teal wall (white robots read against it),
warm wood floor, the PIPELINE board (a tiny Hoody stuck in the bottleneck, circled red) and the AI AUTOMATION crate,
long, lying on the floor, lid up from frame 0 (the meme's plant)."""
import math, cairo
import office as P
from office import INK, WHITE, NAVY, YEL, RED, GREY, rr, fs, ell, limb, txt, hx, lerp, W, H, FLOOR
WALL0, WALL1, FLOORC, SKIRT = hx('4f6f7a'), hx('3c5862'), hx('8a6a4a'), hx('2e4650')
PLY, PLY_D = hx('e3c08a'), hx('b98d52')

def room(c):
    g = cairo.LinearGradient(0, 0, 0, FLOOR); g.add_color_stop_rgb(0, *WALL0); g.add_color_stop_rgb(1, *WALL1)
    c.rectangle(0, 0, W, FLOOR); c.set_source(g); c.fill()
    c.rectangle(0, FLOOR, W, H - FLOOR); c.set_source_rgb(*FLOORC); c.fill()
    for i in range(0, W + 120, 120): c.move_to(i, FLOOR); c.line_to(i - 60, H); c.set_source_rgba(0, 0, 0, .12); c.set_line_width(4); c.stroke()
    c.rectangle(0, FLOOR - 40, W, 40); c.set_source_rgb(*SKIRT); c.fill()

GREEN = hx('2bbf5a')
def _mix(p, q, k): return tuple(a_ + (b_ - a_) * k for a_, b_ in zip(p, q))
def board(c, x, y, w=440, h=300, flow=0.0, f=0, alarm=0.0):
    """PIPELINE. flow 0 (frame 0): tasks pour in wide and jam at one neck - a tiny Hoody, circled red. flow 1 (he is out
    of the room): the whole board goes green, the tasks stream through, a big tick. alarm 0..1: a red flash as he comes
    back. The colour change is the part that reads on a phone."""
    fill = _mix(_mix(WHITE, hx('c9f5d6'), flow), hx('ffc9c9'), alarm)
    rr(c, x, y, w, h, 10); fs(c, fill, 7)
    txt(c, 'PIPELINE', x + w / 2, y + 38, 36, _mix(NAVY, hx('15803d'), flow), lw=0)
    cx, cy = x + w / 2, y + 172
    for q in (-1, 1):
        c.move_to(x + 30, cy + q * 84); c.line_to(cx - 44, cy + q * 24); c.line_to(cx + 44, cy + q * 24); c.line_to(x + w - 30, cy + q * 84)
    c.set_source_rgb(*NAVY); c.set_line_width(7); c.stroke()
    if flow > .5:                                                        # flowing: blocks stream through the neck
        for i in range(8):
            bx = x + 40 + (i * (w - 80) / 8 + f * 26) % (w - 80); by = cy + ((i % 3) - 1) * 34 * min(1, abs(bx - cx) / 130)
            rr(c, bx - 12, by - 8, 24, 16, 3); fs(c, hx('8fd6ff'), 3)
        c.move_to(x + w - 120, y + 62); c.line_to(x + w - 92, y + 92); c.line_to(x + w - 36, y + 26)
        c.set_source_rgb(*INK); c.set_line_width(22); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke_preserve(); c.set_source_rgb(*GREEN); c.set_line_width(13); c.stroke()
        return
    for i in range(5): rr(c, x + 44 + i * 20, cy - 46 + (i % 2) * 40, 24, 16, 3); fs(c, hx('8fd6ff'), 3)
    rr(c, x + w - 80, cy - 8, 24, 16, 3); fs(c, hx('8fd6ff'), 3)                                       # one gets through
    ell(c, cx, cy - 2, 22, 22); fs(c, hx('3a2a22'), 3); ell(c, cx, cy + 4, 14, 12); fs(c, hx('ffd9b8'), 3)   # tiny Hoody
    ell(c, cx, cy, 48 + 14 * alarm, 48 + 14 * alarm); c.set_source_rgb(*RED); c.set_line_width(7 + 5 * alarm); c.stroke()
    txt(c, '!!', cx + 70 + 6 * alarm, cy - 52, 42 + 26 * alarm, RED, lw=0)

def sticker(c, x, y, s=1.0, rot=-.06, rts=0.0):
    """BOTTLENECK REMOVED.: a paper sticker slapped over the crate's own plate (so it can come off again).
    rts 0..1: RETURN TO SENDER stamped across it in red (nobody wants the bottleneck)."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    rr(c, -214, -100, 428, 200, 10); fs(c, hx('fff6d8'), 6)
    for q in (-1, 1): c.save(); c.translate(q * 196, -92); c.rotate(q * .6); rr(c, -34, -12, 68, 24, 3); c.set_source_rgba(1, .82, .25, .85); c.fill(); c.restore()   # tape
    txt(c, 'BOTTLENECK', 0, -34, 58, INK, lw=0); txt(c, 'REMOVED.', 0, 34, 58, INK, lw=0)
    if rts > 0:
        k = 1 + .5 * (1 - rts)
        c.save(); c.rotate(-.16); c.scale(k, k)
        rr(c, -196, -78, 392, 156, 12); c.set_source_rgba(1, 1, 1, .78); c.fill()
        rr(c, -196, -78, 392, 156, 12); c.set_source_rgb(*RED); c.set_line_width(9); c.stroke()
        txt(c, 'RETURN TO', 0, -30, 60, RED, lw=0); txt(c, 'SENDER', 0, 36, 68, RED, lw=0); c.restore()
    c.restore()

def crate(c, x0, gy, L=640, h=330, lid=1.0, label='AI AUTOMATION', stamp=0.0, rot=0.0, slot=False, slot_x=None, rts=0.0):
    """The long plywood crate, lying down; lid hinged on the back edge (lid 1 = up, 0 = shut). Its plate (always there);
    stamp 0..1: the BOTTLENECK REMOVED sticker slapped over the plate (rts: RETURN TO SENDER across it); a hand slot
    (slot_x from the left end; default near the right end). Returns the slot's centre."""
    c.save(); c.translate(x0, gy); c.rotate(rot)
    if lid > 0:                                                         # the lid, standing open behind the crate (we see its inside)
        lh = 230 * lid; sk = 40 * lid
        c.move_to(0, -h); c.line_to(L, -h); c.line_to(L + sk, -h - lh); c.line_to(sk, -h - lh); c.close_path(); fs(c, PLY_D, 7)
        for xx in (L * .25, L * .5, L * .75): c.move_to(xx, -h); c.line_to(xx + sk, -h - lh); c.set_source_rgba(0, 0, 0, .15); c.set_line_width(5); c.stroke()
        c.move_to(0, -h); c.line_to(L, -h); c.set_source_rgb(*hx('3a2a14')); c.set_line_width(16); c.stroke()     # the dark inside
    rr(c, 0, -h, L, h, 6); fs(c, PLY, 7)
    for yy in (-h + 26, -26): c.rectangle(0, yy - 12, L, 24); c.set_source_rgb(*PLY_D); c.fill()
    for xx in (0, L / 2): c.move_to(xx + 30, -h + 38); c.line_to(xx + L / 2 - 30, -38); c.set_source_rgb(*PLY_D); c.set_line_width(16); c.stroke()
    if lid <= 0:
        rr(c, -6, -h - 22, L + 12, 30, 6); fs(c, PLY_D, 6)              # shut
    rr(c, 0, -h, L, h, 6); c.set_source_rgb(*INK); c.set_line_width(7); c.stroke()
    for i in range(6): c.move_to(L / 2 - 150 + i * 56, -54); c.line_to(L / 2 - 120 + i * 56, -84); c.set_source_rgb(*INK); c.set_line_width(14); c.stroke()
    for dx in (0, 34):
        c.move_to(40 + dx, -h + 150); c.line_to(40 + dx, -h + 100); c.move_to(28 + dx, -h + 114); c.line_to(40 + dx, -h + 98); c.line_to(52 + dx, -h + 114)
    c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    if label:
        rr(c, L / 2 - 170, -h + 90, 340, 110, 8); fs(c, WHITE, 5)
        a, b = label.split(' ', 1); txt(c, a, L / 2, -h + 124, 44, INK, lw=0); txt(c, b, L / 2, -h + 170, 40, INK, lw=0)
    if stamp > 0:
        sticker(c, L / 2 + 30, -h / 2 - 20, 1 + .4 * (1 - stamp), rts=rts)      # clear of the hand slot at the left end
    sl = None
    if slot:
        sx = L - 120 if slot_x is None else slot_x
        rr(c, sx, -h + 60, 70, 26, 10); c.set_source_rgb(*hx('3a2a14')); c.fill(); sl = c.user_to_device(sx + 35, -h + 73)
    c.restore()
    return sl
