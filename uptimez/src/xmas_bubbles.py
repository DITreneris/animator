"""Speech bubbles and effects for "Happy Compliance" (storyboard v2 on), drawn in screen space (540 x 960).
- every box is sized from the measured text with fixed padding, and kept inside the safe area;
- bubbles pop in with a small overshoot; the shout box shakes for its first 0.45 s;
- one box can carry several tails (a line said in unison), or point off-screen (a speaker out of frame);
- burst(): a bold comic sound word (THUD) in a spiky star."""
import math
import kit
from kit import INK, clamp, ease
import anim

W, H = 540, 960
SAFE = (18, 96, 522, 820)          # x0, y0, x1, y1: clear of the app's top bar and bottom captions
PAD_X, PAD_Y = 24, 16
FONT = kit.FONT


def _measure(c, lines, size):
    c.select_font_face(FONT); c.set_font_size(size)
    tw = max(c.text_extents(l).x_advance for l in lines)
    return tw, size * 1.14


def _pop(t, t0, d=0.18):
    u = clamp((t - t0) / d)
    return max(0.02, min(1.08, anim.back_out(u, 2.2))) if u < 1 else 1.0


def _round_rect(c, x, y, w, h, r):
    c.new_sub_path()
    c.arc(x + w - r, y + r, r, -math.pi / 2, 0); c.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    c.arc(x + r, y + h - r, r, math.pi / 2, math.pi); c.arc(x + r, y + r, r, math.pi, 1.5 * math.pi)
    c.close_path()


def _tail(c, bx, by, bw, bh, ax, ay, width=13):
    """Tail from the box edge nearest the anchor to the anchor."""
    cx, cy = bx + bw / 2, by + bh / 2
    if ay > by + bh:
        ex, ey = clamp(ax, bx + 26, bx + bw - 26), by + bh - 2
        return [(ex - width, ey), (ax, ay), (ex + width, ey)]
    if ay < by:
        ex, ey = clamp(ax, bx + 26, bx + bw - 26), by + 2
        return [(ex - width, ey), (ax, ay), (ex + width, ey)]
    ex = bx + 2 if ax < cx else bx + bw - 2
    ey = clamp(ay, by + 18, by + bh - 18)
    return [(ex, ey - width), (ax, ay), (ex, ey + width)]


def speech(k, s, anchors, t, t0, side="up", size=28, at=None, fill=(1, 1, 1), italic_sweet=False):
    """anchors: one (x, y) or a list (several tails). side "up" = box above the first anchor; at = (cx, cy)
    centres the box there instead. An anchor outside the frame gives a tail running off the edge."""
    c = k.c
    if isinstance(anchors, tuple):
        anchors = [anchors]
    lines = s.split("\n")
    tw, lh = _measure(c, lines, size)
    max_w = SAFE[2] - SAFE[0] - 2 * PAD_X
    while tw > max_w and size > 16:                              # never let text run out of the box
        size -= 1; tw, lh = _measure(c, lines, size)
    bw, bh = tw + 2 * PAD_X, lh * len(lines) + 2 * PAD_Y
    if at:
        bx, by = at[0] - bw / 2, at[1] - bh / 2
    else:
        ax = sum(a[0] for a in anchors) / len(anchors)
        ay = min(a[1] for a in anchors)
        bx, by = ax - bw / 2, ay - 34 - bh
    bx = clamp(bx, SAFE[0], SAFE[2] - bw)
    by = clamp(by, SAFE[1], SAFE[3] - bh)
    p = _pop(t, t0)
    c.save(); c.translate(bx + bw / 2, by + bh / 2); c.scale(p, p); c.translate(-(bx + bw / 2), -(by + bh / 2))
    fixed = []
    for ax_, ay_ in anchors:                                     # a box pushed down by the safe area can end up
        if bx - 4 <= ax_ <= bx + bw + 4 and by - 4 <= ay_ <= by + bh + 14:   # over its own anchor: point the
            ay_ = by + bh + 16                                   # tail straight down to the head instead
        fixed.append((ax_, ay_))
    tails = [_tail(c, bx, by, bw, bh, ax_, ay_) for ax_, ay_ in fixed]
    c.set_line_join(1)
    for tl in tails:                                             # outlines first, then fills: one clean shape
        c.move_to(*tl[0]); c.line_to(*tl[1]); c.line_to(*tl[2]); c.close_path()
    _round_rect(c, bx, by, bw, bh, 16)
    c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    for tl in tails:
        c.move_to(*tl[0]); c.line_to(*tl[1]); c.line_to(*tl[2]); c.close_path()
    _round_rect(c, bx, by, bw, bh, 16)
    c.set_source_rgb(*fill); c.fill()
    c.select_font_face(FONT); c.set_font_size(size); c.set_source_rgb(*INK)
    for i, l in enumerate(lines):
        e = c.text_extents(l)
        c.move_to(bx + bw / 2 - e.x_advance / 2, by + PAD_Y + lh * i + size * 0.88); c.show_text(l)
    if italic_sweet:                                             # a small heart: said sweetly
        c.set_source_rgb(0.86, 0.10, 0.16)
        hx, hy, hs = bx + bw - 10, by + 8, 7
        c.move_to(hx, hy + hs * 0.9); c.curve_to(hx - hs * 1.5, hy - hs * 0.2, hx - hs * 0.7, hy - hs * 1.2, hx, hy - hs * 0.4)
        c.curve_to(hx + hs * 0.7, hy - hs * 1.2, hx + hs * 1.5, hy - hs * 0.2, hx, hy + hs * 0.9); c.fill()
    c.restore()


def shout(k, s, anchor, t, t0, cx=270, cy=170, size=38):
    """Spiky yellow box sized to the text; pops in and shakes for its first 0.45 s."""
    c = k.c
    lines = s.split("\n")
    tw, lh = _measure(c, lines, size)
    while tw > 380 and size > 20:
        size -= 1; tw, lh = _measure(c, lines, size)
    rw, rh = tw / 2 + 52, lh * len(lines) / 2 + 42
    cx = clamp(cx, SAFE[0] + rw, SAFE[2] - rw)
    cy = clamp(cy, SAFE[1] + rh, SAFE[3] - rh)
    if t - t0 < 0.45:                                            # shake on the 12 fps grid
        f = int((t - t0) * 12)
        cx += (3, -4, 4, -3, 2, -2)[f % 6]; cy += (-2, 3, -3, 2, -1, 1)[f % 6]
    p = _pop(t, t0, 0.14)
    c.save(); c.translate(cx, cy); c.scale(p, p); c.translate(-cx, -cy)
    pts = []
    n = 24
    for i in range(n):
        a = 2 * math.pi * i / n
        r = 1.0 if i % 2 == 0 else 0.86
        pts.append((cx + math.cos(a) * rw * r * 1.1, cy + math.sin(a) * rh * r * 1.14))
    ax, ay = anchor
    tail = [(cx + (ax - cx) * 0.3 - 16, cy + (ay - cy) * 0.3), (ax, ay), (cx + (ax - cx) * 0.3 + 16, cy + (ay - cy) * 0.3 + 8)]
    for shape in (tail, pts):
        c.move_to(*shape[0])
        for q in shape[1:]:
            c.line_to(*q)
        c.close_path()
    c.set_source_rgb(*INK); c.set_line_width(6); c.set_line_join(1); c.stroke()
    for shape in (tail, pts):
        c.move_to(*shape[0])
        for q in shape[1:]:
            c.line_to(*q)
        c.close_path()
    c.set_source_rgb(1.0, 0.93, 0.45); c.fill()
    c.select_font_face(FONT); c.set_font_size(size); c.set_source_rgb(*INK)
    for i, l in enumerate(lines):
        e = c.text_extents(l)
        c.move_to(cx - e.x_advance / 2, cy - lh * len(lines) / 2 + lh * i + size * 0.88); c.show_text(l)
    c.restore()


def burst(k, word, x, y, t, t0, size=52, rot=-0.18):
    """A comic sound word in a red-and-yellow star burst."""
    c = k.c
    p = _pop(t, t0, 0.12)
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(p, p)
    c.select_font_face(FONT); c.set_font_size(size)
    e = c.text_extents(word)
    rw, rh = e.x_advance / 2 + 34, size * 0.5 + 30
    for col, sc in (((0.86, 0.12, 0.14), 1.0), ((1.0, 0.86, 0.20), 0.80)):
        pts = []
        for i in range(28):
            a = 2 * math.pi * i / 28
            r = (1.0 if i % 2 == 0 else 0.72) * sc
            pts.append((math.cos(a) * rw * r * 1.15, math.sin(a) * rh * r * 1.25))
        c.move_to(*pts[0])
        for q in pts[1:]:
            c.line_to(*q)
        c.close_path()
        c.set_source_rgb(*col); c.fill_preserve()
        c.set_source_rgb(*INK); c.set_line_width(3.5); c.stroke()
    c.move_to(-e.x_advance / 2, size * 0.36)
    c.text_path(word)
    c.set_source_rgb(1, 1, 1); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(3); c.stroke()
    c.restore()
