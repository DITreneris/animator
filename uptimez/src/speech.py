"""One speech bubble for a new episode. 540 user space.

No character imports: not bc_sb, not a rig, not fs_animatic. Films already shipped
keep kit.bubble and fs_animatic.speech. The safe rect and the 10-20 px tail live
in speech_gate, and draw() returns the box and the tip it actually painted.
"""
import math

import cairo

import kit
from kit import Ctx, cut
from speech_gate import SAFE, TAIL_MIN, TAIL_MAX

GAP = (TAIL_MIN + TAIL_MAX) // 2   # 15 px past the box; the outline eats about one px
ROBOT = [False]   # opt-in (ep 14, Tomas 24 Nov): mono speakers on the series' tinted bubble, bold. Off: as before
TINT = (0.90, 0.96, 1.0)
CLEAR = [False]   # opt-in (ep 14, Tomas 24 Nov): prefer the wall with no other face beside the box. Off: as before

# Opt-in looks (24 Nov, The Offer). The defaults keep every earlier render byte-identical.
SIZE = [26]        # the text size of a person's line
MONO_SIZE = [24]   # the robot's
MAX_W = [220]      # the widest a line may wrap to before it takes a second row
MONO_BOLD = [False]
SIGNS_FIRST = [False]   # rather a narrower box than one over a story prop
TOP_FIRST = [False]                                     # opt-in (The Offer v47): with `above`, the box over the head wins when it fits


def _weight(font):
    return cairo.FONT_WEIGHT_BOLD if ((MONO_BOLD[0] or ROBOT[0]) and font == kit.MONO) else cairo.FONT_WEIGHT_NORMAL


def _crowded(box, others):
    """Another face level with the box and within its width (plus a head) on that side: the speaker becomes a guess."""
    x0, y0, x1, y1 = box
    for fx, fy, fr in others:
        if x0 - fr * 1.2 <= fx <= x1 + fr * 1.2 and y0 - fr * 1.6 <= fy <= y1 + fr * 1.6:
            return True
    return False


def _bold(mono):
    return mono and ROBOT[0]


def _wrap(c, text, size, font, max_w):
    c.select_font_face(font, cairo.FONT_SLANT_NORMAL, _weight(font))
    c.set_font_size(size)
    rows, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if cur and c.text_extents(trial).x_advance > max_w:
            rows.append(cur)
            cur = word
        else:
            cur = trial
    if cur:
        rows.append(cur)
    return rows or [text]


def _metrics(k, text, mono, max_w=None):
    max_w = MAX_W[0] if max_w is None else max_w
    c = k.c
    font = kit.MONO if mono else kit.FONT
    size = MONO_SIZE[0] if mono else SIZE[0]
    rows = _wrap(c, text, size, font, max_w)
    lead = size * 1.15
    width = 0
    for row in rows:
        c.select_font_face(font, cairo.FONT_SLANT_NORMAL, _weight(font))
        c.set_font_size(size)
        width = max(width, c.text_extents(row).x_advance)
    return rows, size, font, width + 28, lead * len(rows) + 18


def _over_face(box, face):
    x0, y0, x1, y1 = box
    hx, hy, r = face
    return x0 < hx + r * 0.8 and x1 > hx - r * 0.8 and y0 < hy + r * 0.8 and y1 > hy - r * 0.8


def _hits(box, faces, avoid, safe=SAFE):
    if box[0] < safe[0] or box[1] < safe[1] or box[2] > safe[2] or box[3] > safe[3]:
        return True
    if any(_over_face(box, f) for f in faces):
        return True
    for a in avoid:
        if box[0] < a[2] and box[2] > a[0] and box[1] < a[3] and box[3] > a[1]:
            return True
    return False


def _clamp(box, safe=SAFE):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    x0 = min(max(x0, safe[0]), safe[2] - w)
    y0 = min(max(y0, safe[1]), safe[3] - h)
    return (x0, y0, x0 + w, y0 + h)


def _clear(box, tip, faces, avoid, signs, safe=SAFE):
    """Slide the box along its side until it clears the face and still keeps a short tail."""
    x0, y0, x1, y1 = box
    h = y1 - y0
    for dy in range(0, int(h) + 1, 2):
        for sign in ((0,) if dy == 0 else (-1, 1)):
            ny = y0 + sign * dy
            if ny < safe[1] or ny + h > safe[3]:
                continue
            if not (ny + 12 <= tip[1] <= ny + h - 12):
                continue
            nb = (x0, ny, x1, ny + h)
            blocked = signs and any(nb[0] < a[2] and nb[2] > a[0] and nb[1] < a[3] and nb[3] > a[1] for a in avoid)
            outside = nb[0] < safe[0] or nb[2] > safe[2] or nb[1] < safe[1] or nb[3] > safe[3]
            if blocked or outside or any(_over_face(nb, f) for f in faces) or _gap(tip, nb) < TAIL_MIN:
                continue
            if _gap(tip, nb) > TAIL_MAX:
                continue
            return nb
    return None


def _gap(tip, box):
    dx = max(box[0] - tip[0], 0, tip[0] - box[2])
    dy = max(box[1] - tip[1], 0, tip[1] - box[3])
    return math.hypot(dx, dy)


def _paint(k, box, tip, rows, size, font, mono=False):
    x0, y0, x1, y1 = box
    if tip is not None:
        if tip[1] >= y1 - 1:
            mid = min(max(tip[0], x0 + 18), x1 - 18)
            a, b = (mid - 11, y1), (mid + 11, y1)
        elif tip[1] <= y0 + 1:
            mid = min(max(tip[0], x0 + 18), x1 - 18)
            a, b = (mid - 11, y0), (mid + 11, y0)
        elif tip[0] >= x1 - 1:
            mid = min(max(tip[1], y0 + 14), y1 - 14)
            a, b = (x1, mid - 11), (x1, mid + 11)
        else:
            mid = min(max(tip[1], y0 + 14), y1 - 14)
            a, b = (x0, mid - 11), (x0, mid + 11)
        cut(k, [tip, a, b], TINT if _bold(mono) else (1, 1, 1), shadow=False, lw=2.0)
    cut(k, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], TINT if _bold(mono) else (1, 1, 1), shadow=True, lw=2.2)
    lead = size * 1.15
    cx = (x0 + x1) / 2
    top = y0 + (y1 - y0 - lead * len(rows)) / 2 + lead * 0.55
    for i, row in enumerate(rows):
        kit.text(k, row, cx, top + i * lead, size, font=font, center=True, bold=_weight(font) == cairo.FONT_WEIGHT_BOLD)


def draw(k, text, head, mouth=None, above=None, aim=None, mono=False, name=None, others=(), avoid=(), pin=None, safe=None):
    """head is (x, y, r) in 540 space, or None for a speaker who is off the frame.
    mouth is the mouth drawn in this frame. above is a bare scalp or an antenna; without it the tail stays beside the face.
    aim is a tip measured on this frame (a visor rim, a profile mouth, a voice in the dark). The box sits beside it.
    safe replaces SAFE for a frame that is not 540x960. 9:16 callers omit it.
    Returns (box, tip). tip is None on a named card."""
    if not isinstance(k, Ctx):
        k = Ctx(k, 0)
    rect = SAFE if safe is None else safe
    if mono:
        text = text.upper()
    if head is None:
        rows, size, font, bw, bh = _metrics(k, '%s: "%s"' % (name or "OFF", text), False)
        box = (rect[0] + 6, rect[1] + 8, rect[0] + 6 + bw, rect[1] + 8 + bh)
        box = _clamp(box, rect)
        _paint(k, box, None, rows, size, font)
        return box, None

    hx, hy, r = head
    my = mouth[1] if mouth is not None else hy + 0.35 * r
    faces = list(others) + [head]
    if pin is not None:                                      # opt-in (lesson 784): the box where it was put on the line's first drawing; only the tail follows the head
        side = 1 if (pin[0] + pin[2]) / 2.0 > hx else -1
        tip = aim if aim is not None else (hx + side * r * 0.82, my)
        if (TAIL_MIN + 3 <= _gap(tip, pin) <= TAIL_MAX - 1 and pin[1] + 8 <= tip[1] <= pin[3] - 8
                and not _hits(pin, faces, avoid, rect)):
            rows, size, font, _bw, _bh = _metrics(k, text, mono, max(48, pin[2] - pin[0] - 28))
            _paint(k, pin, tip, rows, size, font)
            return pin, tip

    def room_for(side, tip):
        if side > 0:
            return rect[2] - (tip[0] + GAP)
        return (tip[0] - GAP) - rect[0]

    def beside(side, tip, y, max_w, signs=True):
        """A box in the wall on this side of the tip. None when it would slide over the tip or the face.
        signs=False is the second pass: a readable line may cross a sign when that is the only wall."""
        room = room_for(side, tip)
        if room < 96 or max_w < 48:
            return None
        rows, size, font, bw, bh = _metrics(k, text, mono, min(MAX_W[0], max_w))
        if bw > room + 0.5:
            return None
        x0 = tip[0] + GAP if side > 0 else tip[0] - GAP - bw
        y0 = y - bh * 0.45
        if y0 < rect[1] or y0 + bh > rect[3]:
            y0 = min(max(y0, rect[1]), rect[3] - bh)
            if not (y0 + 8 <= tip[1] <= y0 + bh - 8):
                return None
        box = (x0, y0, x0 + bw, y0 + bh)
        box = _clear(box, tip, faces, avoid, signs, rect)
        if box is None:
            return None
        return box, tip, rows, size, font

    def overhead():
        tip = above
        room = rect[2] - rect[0]
        rows, size, font, bw, bh = _metrics(k, text, mono, min(MAX_W[0], room - 28))
        x0 = min(max(tip[0] - bw / 2, rect[0]), rect[2] - bw)
        y0 = tip[1] - GAP - bh
        if y0 < rect[1]:
            return None
        box = (x0, y0, x0 + bw, y0 + bh)
        if _hits(box, faces, avoid, rect) or _gap(tip, box) < TAIL_MIN:
            return None
        return box, tip, rows, size, font

    if aim is not None:
        away = -1 if aim[0] <= hx else 1
        tries = [(away, aim, aim[1]), (-away, aim, aim[1])]
    else:
        side0 = 1 if hx < (rect[0] + rect[2]) / 2 else -1
        tries = []
        for side in (side0, -side0):
            tip = (hx + side * r * 0.82, my)
            tries.append((side, tip, my))
    found = []
    for signs in (True, False):
        for narrow in (False, True):
            for n, (side, tip, y) in enumerate(tries):
                width = (room_for(side, tip) - 28) if narrow else MAX_W[0]
                got = beside(side, tip, y, width, signs)
                if got:
                    found.append(((_crowded(got[0], others),) if CLEAR[0] else ()) + (narrow, not signs, n, got))
    if above is not None:
        got = overhead()
        if got:
            found.append(((_crowded(got[0], others),) if CLEAR[0] else ()) + (False, False, len(tries), got))
    top_ = overhead() if (TOP_FIRST[0] and above is not None) else None
    if SIGNS_FIRST[0]:                                    # f[-4:] is (narrow, past a sign, try, got); CLEAR prefixes crowded
        found.sort(key=lambda f: f[:-4] + (f[-3], f[-4], f[-2]))
        picked = found[0][-1] if found else None
    else:
        picked = min(found, key=lambda f: f[:-1])[-1] if found else None
    if top_:
        picked = top_
    if picked is None:
        side, tip, y = max(tries, key=lambda t: room_for(t[0], t[1]))
        avail = max(56, room_for(side, tip))
        rows, size, font, bw, bh = _metrics(k, text, mono, max(40, avail - 28))
        while bw > avail and size > 15:
            size -= 1
            rows = _wrap(k.c, text, size, font, max(32, avail - 28))
            k.c.select_font_face(font, 0, 1 if mono else 0)
            k.c.set_font_size(size)
            bw = max(56, max(k.c.text_extents(s).x_advance for s in rows) + 28)
            bh = 20 + len(rows) * (size + 4)
        bw = min(bw, avail)
        x0 = tip[0] + GAP if side > 0 else tip[0] - GAP - bw
        x0 = min(max(x0, rect[0]), rect[2] - bw)
        y0 = min(max(y - bh * 0.45, rect[1]), rect[3] - bh)
        y0 = min(max(y0, tip[1] - bh + 6), tip[1] - 6)
        y0 = min(max(y0, rect[1]), rect[3] - bh)
        picked = ((x0, y0, x0 + bw, y0 + bh), tip, rows, size, font)
    box, tip, rows, size, font = picked
    _paint(k, box, tip, rows, size, font, mono)
    return box, tip
