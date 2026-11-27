"""Hand library v3 (27 Nov, Tomas: "one more round" after v2's viewers, 2/2 on the actions, both on the same
faults: the mug "perched on the knuckles", the little finger "a hitchhiker's thumb, a spike"; the plate and the hand one
shape, "a wing, a fish". v3: a cupped palm with a gap of air under the saucer, the forearm rising into it; a shorter
little finger. The cup's handle is the sheet's: big enough to show above and below the fist.)

Hand library v2 (27 Nov, after two cold viewers on v1: the little finger read as a spatula, a tongue, a blade
"stuck onto the side"; the fingers merged with the cup; the saucer hand as a wing, a fish, a paddle, its wrist
"pinched" to a point. v1 kept as hand_lib_v1.py.)

Hand library v1 (sandbox; Tomas 27 Nov: "kol nesutvarkem nekisk ranku prie kanono" - not the canon, not a film).

Why (the outside audit of the 5.2 sheets, 27 Nov, and every hand round before it): our hands, the canon's included
(hands_ps, hands_v4, of_cast.clutch), are built from separate strokes: an oval palm and a capsule per finger, each
from its own root, of one width end to end. They read as tentacles stuck to the wrist, a thumb that holds nothing,
a hand glued to the sleeve. Here a hand is ONE closed outline: the wrist, the back of the hand, the knuckle line,
fingers that taper, the thumb growing from the heel of the palm, drawn as one shape with a few inner lines.

Three poses (the ones 5.2 needs), side view, each with its contact points, left and right as mirror images:
  RELAXED          at rest, the fingers together and a little curled, the thumb along the front
  CUP_GRIP         a cup's handle in the curled index, the thumb pressing on top, the little finger out
  SAUCER_SUPPORT   palm up, level, the fingers flat under the saucer, their tips up round the far rim, the thumb over
                   the near rim (the thumb is the hand's second pass, over the saucer: one hand, two passes)

Hand-local frame: the wrist's middle at (0, 0), +x out along the hand, +y the thumb's side (mirrored by `side`),
units of w (the hand's width at the knuckles; male 17, female 15 at character scale 1, as the canon).
  draw(k, pose, x, y, ang, w, skin, side, obj=None)   obj(k): the held object, drawn in the hand's own frame
  contact(pose, name) -> local point, e.g. contact("CUP_GRIP", "handle")
"""
import math

from kit import INK

LW = 2.0


def _smooth(c, pts, closed=True):
    """a closed Catmull-Rom curve through pts (as cubic Beziers)."""
    n = len(pts)
    c.move_to(*pts[0])
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0, p1, p2, p3 = pts[(i - 1) % n], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        if not closed:
            p0 = pts[max(i - 1, 0)]; p3 = pts[min(i + 2, n - 1)]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6.0, p1[1] + (p2[1] - p0[1]) / 6.0)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6.0, p2[1] - (p3[1] - p1[1]) / 6.0)
        c.curve_to(c1[0], c1[1], c2[0], c2[1], p2[0], p2[1])
    if closed:
        c.close_path()


# ---- the poses: outline points (clockwise from the wrist's top), inner lines, contacts ----------------------------
# y < 0: the back of the hand / the little finger's side; y > 0: the thumb's side.

POSES = {
    "RELAXED": dict(
        outline=[(0.00, -0.30), (0.30, -0.36), (0.62, -0.40), (0.86, -0.36), (1.10, -0.24), (1.30, -0.06),
                 (1.36, 0.10), (1.26, 0.20), (1.06, 0.18), (0.98, 0.30), (0.80, 0.40), (0.52, 0.44),
                 (0.26, 0.40), (0.00, 0.30)],
        lines=[[(0.70, -0.30), (0.96, -0.18), (1.16, 0.02)],                     # between the fingers, tapering
               [(0.70, -0.16), (0.92, -0.04), (1.06, 0.12)],
               [(0.42, 0.30), (0.62, 0.30), (0.86, 0.26)]],                      # the thumb's edge on the palm
        contacts={}),
    "CUP_GRIP": dict(                                                            # the fist round the handle + the little finger
        outline=[(0.00, -0.30), (0.30, -0.36), (0.66, -0.42), (0.88, -0.50), (1.00, -0.58), (1.08, -0.58),
                 (1.06, -0.50), (0.96, -0.42), (0.96, -0.34), (1.12, -0.22), (1.22, -0.02), (1.14, 0.16),
                 (1.20, 0.24), (1.10, 0.34), (0.86, 0.36), (0.56, 0.42), (0.26, 0.40), (0.00, 0.30)],
        lines=[[(0.92, -0.30), (1.04, -0.14), (1.06, 0.02)],                     # the curled fingers' tips, folded in
               [(0.84, -0.22), (0.96, -0.04), (0.94, 0.10)],
               [(0.50, 0.30), (0.78, 0.24), (1.04, 0.20)]],                      # the thumb lying over the handle
        contacts={"handle": (1.10, 0.06)}),
    "SAUCER_SUPPORT": dict(                                                      # palm up, the hand level
        outline=[(0.00, -0.32), (0.30, -0.36), (0.56, -0.22), (0.86, -0.16), (1.14, -0.22), (1.40, -0.32), (1.56, -0.46),
                 (1.64, -0.38), (1.60, -0.18), (1.50, -0.06), (1.40, -0.12), (1.30, -0.02), (1.18, -0.08),
                 (1.06, 0.00), (0.90, -0.02), (0.60, 0.04), (0.30, 0.14), (0.00, 0.32)],
        lines=[[(1.40, -0.20), (1.40, -0.12)], [(1.20, -0.18), (1.18, -0.08)]],  # between the fingertips under it
        thumb=[(0.12, -0.24), (0.20, -0.46), (0.34, -0.60), (0.52, -0.66), (0.60, -0.56), (0.46, -0.44),
               (0.34, -0.28)],
        contacts={"saucer": (0.98, -0.36), "touch": (1.40, -0.34), "far_rim": (1.56, -0.40), "near_rim": (0.30, -0.48)}),
        # v3: the saucer rests on the heel of the palm and the fingers ("touch"), air under its middle (the cupped palm)
}
# SAUCER_SUPPORT is drawn palm up: its -y is UP on screen whatever the side (the saucer lies on it), so it is not
# mirrored in y; `side` mirrors it in x (the hand reaching screen left or right).


def contact(pose, name):
    return POSES[pose]["contacts"][name]


def frame(k, pose, x, y, ang, w, side):
    """move the context into the hand's frame (caller restores)."""
    c = k.c
    c.save(); c.translate(x, y)
    if pose == "SAUCER_SUPPORT":
        c.scale(side * w, w)                                   # level, palm up; side: reaching right (+1) or left (-1)
    else:
        c.rotate(ang); c.scale(w, side * w)
    return c


def to_screen(pose, x, y, ang, w, side, p):
    """a local point (a contact) on screen."""
    if pose == "SAUCER_SUPPORT":
        return x + side * w * p[0], y + w * p[1]
    lx, ly = w * p[0], side * w * p[1]
    return x + lx * math.cos(ang) - ly * math.sin(ang), y + lx * math.sin(ang) + ly * math.cos(ang)


def draw(k, pose, x, y, ang, w, skin, side=1, obj=None, back_obj=None):
    """the hand at its wrist (x, y): one outline and its inner lines; ang: the forearm's direction on screen (radians;
    SAUCER_SUPPORT stays level). back_obj(k), obj(k) draw in scene coordinates (use to_screen for the contacts):
    back_obj before the hand (the cup whose handle the fist closes on), obj after it (the saucer on the palm), then the
    hand's second pass (the thumb over the near rim): one hand, two passes, as the canon's holding rule."""
    P = POSES[pose]
    _W[0] = w
    if back_obj:
        back_obj(k)
    c = frame(k, pose, x, y, ang, w, side)
    _shape_u(c, P["outline"], skin)
    _lines_u(c, P["lines"])
    c.restore()
    if obj:
        obj(k)
    if "thumb" in P:
        c = frame(k, pose, x, y, ang, w, side)
        _shape_u(c, P["thumb"], skin)
        c.restore()


def _px(c):
    """one device pixel in the current user units (the frame is scaled by w)."""
    dx, dy = c.device_to_user_distance(1.0, 0.0)
    return math.hypot(dx, dy)


_W = [1.0]                                                       # the hand's w while it draws: line widths in frame units
LWS = [1.0]                                                      # line weight scale: a rig's character scale (Don 0.60), so the
                                                                 # hand's outline matches the rig's (5.2 still: 2 world units
                                                                 # round a 10-unit hand read as a black blob)


def _shape_u(c, pts, skin):
    c.new_path(); _smooth(c, pts)
    c.set_source_rgb(*skin); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(LW * LWS[0] / _W[0]); c.set_line_join(1); c.stroke(); c.set_line_join(0)


def _lines_u(c, lines):
    c.set_source_rgb(*INK); c.set_line_width(1.4 * LWS[0] / _W[0]); c.set_line_cap(1)
    for ln in lines:
        c.new_path(); _smooth(c, ln, closed=False); c.stroke()
    c.set_line_cap(0)


# ---- left and right by the canon (hands_lr, 27 Nov) ------------------------------------------------------------------
# Tomas 27 Nov ("taip darome"): every hand drawn from now on takes its thumb side from the canon's hands_lr (copied
# verbatim from DITreneris/uptimez src/hands_lr.py at bbf4cbb), not from a side the caller picks; and it is logged in
# hands_lr.LOG so hands_lr.check() sees it with the rig's own hands. The library's +y is the thumb's side, the same
# convention as hands_ps / hands_v4, so hands_lr.side() is used as it is.

def draw_lr(k, pose, x, y, d, w, skin, arm, obj=None, back_obj=None, reach=None):
    """draw() with the canon's side. d: the forearm's direction on screen (dx, dy); arm: -1 screen-left, +1 screen-
    right (the canon's arm). SAUCER_SUPPORT stays level, palm up, thumb up (hands_lr: level forearms keep one side up);
    reach: -1/+1 which way it reaches (default: the arm's side). Returns (ang, side) so the caller can find contacts."""
    import hands_lr as lr
    ang = math.atan2(d[1], d[0])
    if pose == "SAUCER_SUPPORT":
        s = reach if reach is not None else arm
    else:
        s = lr.side(arm, d)
        if lr._SHOT[0] is not None:
            s = lr._SHOT[0].setdefault(lr._IDX[0], s)
    lr._record(k, x, y, w, d, s)
    lr._IDX[0] += 1
    draw(k, pose, x, y, ang, w, skin, s, obj=obj, back_obj=back_obj)
    return ang, s
