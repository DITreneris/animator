"""Animation helpers for the paper-cutout kit: pose tweening, walk cycle, squash and stretch,
paper flutter, camera moves. Registers tweened poses in kit.ARM_POSES at runtime; kit.py is unchanged."""
import math
import kit
from kit import clamp, ease, lerp

_POSES = kit.ARM_POSES


def back_out(u, s=1.6):
    """Ease with overshoot; never returns exactly 0 scale problems (callers use it for offsets)."""
    u = clamp(u)
    return 1 + (s + 1) * (u - 1) ** 3 + s * (u - 1) ** 2


def angles(pose):
    return _POSES[pose] if isinstance(pose, str) else tuple(pose)


def key(a):
    """Register a tuple of arm angles as a pose name the kit can draw."""
    k = "_tw_" + "_".join(str(int(round(x))) for x in a)
    if k not in _POSES:
        _POSES[k] = tuple(a)
    return k


def tween(a, b, u, overshoot=False):
    """Pose name between pose a and pose b (names or angle tuples), u in 0..1."""
    e = back_out(u) if overshoot else ease(clamp(u))
    A, B = angles(a), angles(b)
    return key([lerp(x, y, e) for x, y in zip(A, B)])


def keyed(t, keys, overshoot=True, dur=0.18):
    """keys = [(time, pose), ...]; returns the pose name at time t, tweening dur seconds into each key."""
    name = lambda q: q if isinstance(q, str) else key(q)
    cur = name(keys[0][1])
    for i in range(1, len(keys)):
        tk, pk = keys[i]
        if t < tk:
            break
        u = (t - tk) / dur
        cur = tween(keys[i - 1][1], pk, u, overshoot) if u < 1 else name(pk)
    return cur


def walk(t, speed=4.0, swing=18):
    """Arm swing + body bob for a front-facing cutout sliding sideways."""
    ph = t * speed * 2 * math.pi
    pose = key((-8 + swing * math.sin(ph), 8, 8 + swing * math.sin(ph), -8))
    bob = -abs(math.sin(ph)) * 7
    return pose, bob


def squash(c, cx, base_y, sx, sy):
    """Scale about a base point (bottom centre). Use inside c.save()/c.restore()."""
    c.translate(cx, base_y)
    c.scale(max(0.02, sx), max(0.02, sy))
    c.translate(-cx, -base_y)


def gulp(t, hits, amt=0.12, dur=0.3):
    """Squash pulses at each hit time: returns (sx, sy)."""
    v = 0.0
    for h in hits:
        d = (t - h) / dur
        if 0 <= d < 1:
            v += math.sin(d * math.pi) * math.exp(-d * 2)
    return 1 + amt * v, 1 - amt * v


def flutter(x0, y0, t, seed, fall=160, sway=40):
    """Position and rotation of a falling page that sways and spins."""
    ph = seed * 1.7
    x = x0 + math.sin(t * 2.4 + ph) * sway
    y = y0 + t * fall
    rot = math.sin(t * 2.4 + ph + 0.8) * 0.7
    return x, y, rot


def camera(c, cx, cy, zoom=1.0, dx=0.0, dy=0.0):
    """Zoom about (cx, cy) and pan. Use inside c.save()/c.restore()."""
    c.translate(cx + dx, cy + dy)
    c.scale(zoom, zoom)
    c.translate(-cx, -cy)
