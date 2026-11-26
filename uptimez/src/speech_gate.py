"""The speech check. One safe rect, one tail length, measured on the pixels just painted.

speech.draw uses these numbers. uz_check imports SAFE from here so it is not copied again.
A caller-supplied tip is not trusted: the tip is the white pixel farthest past the box.
"""
import math

import cairo

SAFE = (18, 96, 522, 820)   # x0, y0, x1, y1 at 540x960 (CLAUDE.md, G5)
SAFE_16X9 = (24, 24, 936, 516)  # same inset idea at 960x540; 9:16 callers keep SAFE
RAIL = (470, 380, 540, 860)  # the app's button rail: no text there (CLAUDE.md "Text", G3 dead zones)
TAIL_MIN, TAIL_MAX = 10, 20


def _as_faces(faces):
    if not faces:
        return []
    if isinstance(faces, dict):
        return list(faces.values())
    return list(faces)


def _over_face(box, face):
    x0, y0, x1, y1 = box
    hx, hy, r = face
    return x0 < hx + r * 0.8 and x1 > hx - r * 0.8 and y0 < hy + r * 0.8 and y1 > hy - r * 0.8


def _dist(tip, box):
    x, y = tip
    dx = max(box[0] - x, 0, x - box[2])
    dy = max(box[1] - y, 0, y - box[3])
    return math.hypot(dx, dy)


def snapshot(surface):
    """A copy of the frame before the bubble is painted. Eyes and teeth are already in it."""
    import numpy as np
    surface.flush()
    w, h = surface.get_width(), surface.get_height()
    stride = surface.get_stride() // 4
    return np.ndarray((h, stride, 4), np.uint8, surface.get_data())[:, :w].copy()


def _buffer(surface):
    import numpy as np
    surface.flush()
    w, h = surface.get_width(), surface.get_height()
    stride = surface.get_stride() // 4
    return np.ndarray((h, stride, 4), np.uint8, surface.get_data())[:, :w]


def _farthest(white, box, sx, sy):
    import numpy as np
    x0, y0 = (box[0] - 2) * sx, (box[1] - 2) * sy
    x1, y1 = (box[2] + 2) * sx, (box[3] + 2) * sy
    ys, xs = np.nonzero(white)
    if len(xs) == 0:
        return None
    outside = ~((xs >= x0) & (xs <= x1) & (ys >= y0) & (ys <= y1))
    if not outside.any():
        return None
    ux = (xs[outside] + 0.5) / sx
    uy = (ys[outside] + 0.5) / sy
    dx = np.maximum(np.maximum(box[0] - ux, 0), ux - box[2])
    dy = np.maximum(np.maximum(box[1] - uy, 0), uy - box[3])
    dist = np.hypot(dx, dy)
    i = int(dist.argmax())
    return (float(ux[i]), float(uy[i])), float(dist[i])


def _attached(white, box, sx, sy):
    """White pixels outside the box that touch its edge. An eye across the frame does not."""
    import numpy as np
    found = _farthest(white, box, sx, sy)
    if found is None:
        return None
    x0, y0 = (box[0] - 2) * sx, (box[1] - 2) * sy
    x1, y1 = (box[2] + 2) * sx, (box[3] + 2) * sy
    ys, xs = np.nonzero(white)
    ux = (xs + 0.5) / sx
    uy = (ys + 0.5) / sy
    outside = ~((xs >= x0) & (xs <= x1) & (ys >= y0) & (ys <= y1))
    dx = np.maximum(np.maximum(box[0] - ux, 0), ux - box[2])
    dy = np.maximum(np.maximum(box[1] - uy, 0), uy - box[3])
    near = outside & (np.hypot(dx, dy) <= 8)
    if not near.any():
        return None
    seen = np.zeros(white.shape, np.bool_)
    seen[ys[near], xs[near]] = True
    region = np.zeros(white.shape, np.bool_)
    region[ys[outside], xs[outside]] = True
    region &= white
    for _ in range(512):
        nxt = seen.copy()
        nxt[1:] |= seen[:-1]
        nxt[:-1] |= seen[1:]
        nxt[:, 1:] |= seen[:, :-1]
        nxt[:, :-1] |= seen[:, 1:]
        nxt[1:, 1:] |= seen[:-1, :-1]
        nxt[1:, :-1] |= seen[:-1, 1:]
        nxt[:-1, 1:] |= seen[1:, :-1]
        nxt[:-1, :-1] |= seen[1:, 1:]
        nxt &= region
        if np.array_equal(nxt, seen):
            break
        seen = nxt
    return _farthest(seen, box, sx, sy)


def measured_tip(surface, box, before=None, fill=None):
    """The tail tip in 540 user space, and how far past the box it sits.
    With `before` (snapshot() just before the bubble), only pixels the bubble changed.
    Without it, only the white that touches the box. Eyes and teeth are white too, and are not the tip.
    None when the bubble has no tail (a named card)."""
    import numpy as np
    px = _buffer(surface)
    white = (px[:, :, 0] >= 248) & (px[:, :, 1] >= 248) & (px[:, :, 2] >= 248)
    if fill is not None:                                   # a tinted bubble (speech.ROBOT): its fill counts as the paper
        bgr = [round(255 * v) for v in fill[::-1]]
        white |= (np.abs(px[:, :, :3].astype(np.int16) - np.array(bgr, np.int16)).max(axis=2) <= 4)
    sx, sy = surface.get_device_scale()
    if before is not None:
        changed = np.abs(px.astype(np.int16) - before.astype(np.int16))[..., :3].max(axis=2) > 30
        return _farthest(white & changed, box, sx, sy)
    return _attached(white, box, sx, sy)


def _overlap(a, b):
    return a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]


def check(surface, box, tip, faces, above=None, aim=None, before=None, avoid=(), fill=None, safe=None):
    """Fail on a long tail, a tip on hair, eyes or the mouth, a box outside the safe rect, in the button rail, over a face,
    or over a rect the caller keeps clear (avoid: the signs, story props and hands drawn in this frame).
    fill: a tinted bubble's paper (speech.ROBOT), so its tail is seen.
    safe replaces SAFE. The 9:16 button rail applies only when safe is omitted.
    above is a bare-scalp or antenna point. aim is a tip the caller measured on this frame
    (a visor rim, the mouth a profile drew, a voice in the dark). A tip landing on either is allowed.
    before is snapshot() from just before this bubble. Returns a list of faults. Empty means it may ship."""
    msgs = []
    x0, y0, x1, y1 = box
    rect = SAFE if safe is None else safe
    if x0 < rect[0] or y0 < rect[1] or x1 > rect[2] or y1 > rect[3]:
        msgs.append("BUBBLE outside the safe area %s" % (tuple(round(v) for v in box),))
    if rect == SAFE and _overlap(box, RAIL):
        msgs.append("BUBBLE in the right button rail %s" % (tuple(round(v) for v in box),))
    for a in avoid:
        if _overlap(box, a):
            msgs.append("BUBBLE over a sign or prop kept clear %s" % (tuple(round(v) for v in a),))
            break
    for face in _as_faces(faces):
        if _over_face(box, face):
            msgs.append("BUBBLE over a face")
            break
    found = measured_tip(surface, box, before, fill) if surface is not None else None
    if tip is None:
        if found is not None and found[1] > 2:
            msgs.append("TAIL on a named card")
        return msgs
    if found is None:
        msgs.append("TAIL not painted")
        return msgs
    painted, length = found
    if math.hypot(painted[0] - tip[0], painted[1] - tip[1]) > 12:
        msgs.append("TAIL painted tip is not the reported tip")
    if length > TAIL_MAX:
        msgs.append("TAIL too long: %.0f px past the box" % length)
    elif length < TAIL_MIN:
        msgs.append("TAIL too short: %.0f px past the box" % length)
    allowed = any(p is not None and math.hypot(painted[0] - p[0], painted[1] - p[1]) <= 12
                  for p in (above, aim))
    if not allowed:
        f_list = _as_faces(faces)
        near = [f for f in f_list if math.hypot(painted[0] - f[0], painted[1] - f[1]) <= f[2] * 1.35]
        if f_list and not near:
            msgs.append("TAIL away from every face at (%.0f, %.0f)" % painted)
        for hx, hy, r in near:
            if painted[1] < hy - 0.05 * r:
                msgs.append("TAIL on hair or eyes at (%.0f, %.0f)" % painted)
                break
            if painted[1] > hy + 0.95 * r:
                msgs.append("TAIL below the chin at (%.0f, %.0f)" % painted)
                break
            mouth = (hx, hy + 0.35 * r)
            if math.hypot(painted[0] - mouth[0], painted[1] - mouth[1]) < 0.28 * r:
                msgs.append("TAIL on the mouth at (%.0f, %.0f)" % painted)
                break
            if math.hypot(painted[0] - hx, painted[1] - hy) < 0.35 * r:
                msgs.append("TAIL on hair or eyes at (%.0f, %.0f)" % painted)
                break
    return msgs


def _blank():
    import kit
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, kit.W, kit.H)
    c = cairo.Context(surf)
    c.set_source_rgb(*kit.WALL)
    c.paint()
    return surf, c


def _eye(c, x, y):
    """a white eye already on the frame. It must not be read as a tail."""
    c.set_source_rgb(1, 1, 1)
    c.arc(x, y, 8, 0, 2 * math.pi)
    c.fill()


def _tail(c, box, tip):
    c.set_source_rgb(1, 1, 1)
    c.rectangle(box[0], box[1], box[2] - box[0], box[3] - box[1])
    c.fill()
    mid = (box[0] + box[2]) / 2
    c.move_to(mid - 8, box[3])
    c.line_to(mid + 8, box[3])
    c.line_to(*tip)
    c.close_path()
    c.fill()


def selftest():
    """Plant a long tail, a hair tip and a covered face: each must fail. A clean bubble must pass,
    including one with a white eye already on the frame and one drawn at device scale 2."""
    import kit
    from kit import Ctx
    import speech
    bad = []

    def eye_then(draw):
        surf, c = _blank()
        _eye(c, 40, 140)
        before = snapshot(surf)
        draw(c)
        return surf, before

    surf, before = eye_then(lambda c: _tail(c, (100, 180, 240, 250), (170, 320)))
    tip = (170, 320)
    got = check(surf, (100, 180, 240, 250), tip, [], before=before)
    if not any(m.startswith("TAIL too long") for m in got) or any("not the reported tip" in m for m in got):
        bad.append("a long tail passed, or the eye was taken for it: %s" % got)

    face = (200, 400, 36)
    hair = (face[0], face[1] - face[2] * 0.75)
    box = (hair[0] - 70, hair[1] - 56, hair[0] + 70, hair[1] - 16)

    def paint_hair(c):
        kit.ellipse(Ctx(c, 0), face[0], face[1] - face[2] * 0.85, 22, 16, (0.12, 0.09, 0.08), 1)
        _tail(c, box, hair)

    surf, c = _blank()
    _eye(c, 40, 140)
    before = snapshot(surf)
    paint_hair(c)
    got = check(surf, box, hair, [face], before=before)
    if not any("hair or eyes" in m for m in got) or any("not the reported tip" in m for m in got):
        bad.append("a hair tip passed, or the eye was taken for it: %s" % got)
    got = check(surf, box, hair, [face], aim=hair, before=before)
    if any("hair or eyes" in m for m in got):
        bad.append("an aimed visor tip was called hair: %s" % got)

    surf, c = _blank()
    before = snapshot(surf)
    far_box = (340, 200, 460, 250)
    far_tip = (400, 265)
    _tail(c, far_box, far_tip)
    got = check(surf, far_box, far_tip, [face], before=before)
    if not any("away from every face" in m for m in got):
        bad.append("a tail floating away from every face passed: %s" % got)

    surf, c = _blank()
    before = snapshot(surf)
    chin_tip = (face[0], face[1] + face[2] * 1.15)
    chin_box = (chin_tip[0] - 60, chin_tip[1] + 15, chin_tip[0] + 60, chin_tip[1] + 65)
    c.set_source_rgb(1, 1, 1)
    c.rectangle(chin_box[0], chin_box[1], chin_box[2] - chin_box[0], chin_box[3] - chin_box[1])
    c.fill()
    c.move_to(chin_tip[0] - 8, chin_box[1])
    c.line_to(chin_tip[0] + 8, chin_box[1])
    c.line_to(*chin_tip)
    c.close_path()
    c.fill()
    got = check(surf, chin_box, chin_tip, [face], before=before)
    if not any("below the chin" in m for m in got):
        bad.append("a tail below the chin passed: %s" % got)

    surf, c = _blank()
    face = (270, 480, 50)
    kit.ellipse(Ctx(c, 0), *face[:2], face[2], face[2] * 1.05, (0.95, 0.76, 0.49), 2)
    box = (230, 450, 320, 530)
    c.set_source_rgb(1, 1, 1)
    c.rectangle(box[0], box[1], box[2] - box[0], box[3] - box[1])
    c.fill()
    got = check(surf, box, None, [face])
    if not any("over a face" in m for m in got):
        bad.append("a covered face passed: %s" % got)

    surf, c = _blank()
    box = (0, 40, 80, 90)
    c.rectangle(0, 40, 80, 50)
    c.fill()
    got = check(surf, box, None, [])
    if not any("outside the safe area" in m for m in got):
        bad.append("a box outside SAFE passed: %s" % got)

    # a tinted robot bubble (speech.ROBOT): without fill= its tail is not seen; with it, a long tinted tail still fails
    # and a clean one passes
    tint = speech.TINT
    surf, c = _blank()
    before = snapshot(surf)
    ant_head = (270, 520, 33)
    ant = (270, 520 - 33 * 1.48)
    speech.ROBOT[0] = True
    try:
        tbox, ttip = speech.draw(Ctx(c, 0), "Border breach.", ant_head, above=ant, mono=True)
    finally:
        speech.ROBOT[0] = False
    if not any("not painted" in m for m in check(surf, tbox, ttip, [ant_head], above=ant, before=before)):
        bad.append("a tinted tail was read without fill= (the planted miss did not fail)")
    got = check(surf, tbox, ttip, [ant_head], above=ant, before=before, fill=tint)
    if got:
        bad.append("a clean tinted robot bubble failed: %s" % got)
    surf, c = _blank()
    before = snapshot(surf)
    lbox = (200, 200, 340, 250)
    c.set_source_rgb(*tint); c.rectangle(200, 200, 140, 50); c.fill()
    c.move_to(262, 250); c.line_to(278, 250); c.line_to(270, 330); c.close_path(); c.fill()
    got = check(surf, lbox, (270, 330), [(270, 370, 33)], before=before, fill=tint)
    if not any(m.startswith("TAIL too long") for m in got):
        bad.append("a long tinted tail passed: %s" % got)

    surf, c = _blank()                                       # a box in the app's button rail (CLAUDE.md "Text")
    box = (440, 500, 520, 560)
    c.set_source_rgb(1, 1, 1); c.rectangle(box[0], box[1], box[2] - box[0], box[3] - box[1]); c.fill()
    got = check(surf, box, None, [])
    if not any("button rail" in m for m in got):
        bad.append("a box in the right rail passed: %s" % got)

    surf, c = _blank()                                       # a box on a sign the caller asked to keep clear
    sign = (120, 300, 260, 340)
    box = (150, 320, 300, 380)
    c.set_source_rgb(1, 1, 1); c.rectangle(box[0], box[1], box[2] - box[0], box[3] - box[1]); c.fill()
    got = check(surf, box, None, [], avoid=[sign])
    if not any("over a sign" in m for m in got):
        bad.append("a box over a kept-clear sign passed: %s" % got)

    def clean(surf, c, before):
        head = (160, 420, 48)
        mouth = (head[0], head[1] + 0.35 * head[2])
        box, tip = speech.draw(Ctx(c, 0), "We're in.", head, mouth=mouth)
        return check(surf, box, tip, [head], before=before)

    surf, c = _blank()
    _eye(c, 40, 140)
    before = snapshot(surf)
    got = clean(surf, c, before)
    if got:
        bad.append("a clean bubble with an eye on the frame failed: %s" % got)
    got = clean(surf, c, None)
    if got:
        bad.append("a clean bubble failed when the eye was not masked: %s" % got)

    surf, c = _blank()
    head = (270, 420, 78)
    mouth = (head[0], head[1] + 0.35 * head[2])
    box, tip = speech.draw(Ctx(c, 0), "This meeting does not exist.", head, mouth=mouth)
    got = check(surf, box, tip, [head])
    if got:
        bad.append("a long line beside a centred face failed: %s" % got)

    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, kit.W * 2, kit.H * 2)
    surf.set_device_scale(2, 2)
    c = cairo.Context(surf)
    c.set_source_rgb(*kit.WALL)
    c.paint()
    _eye(c, 40, 140)
    before = snapshot(surf)
    got = clean(surf, c, before)
    if got:
        bad.append("a clean bubble at device scale 2 failed: %s" % got)

    if bad:
        for line in bad:
            print("FAIL", line)
        return 1
    print("speech_gate selftest ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(selftest())
