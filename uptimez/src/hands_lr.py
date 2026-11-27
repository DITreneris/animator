"""Left and right hands are mirrored: on a hanging arm the thumb is toward the body (Tomas 26 Nov, 27 Nov).

The canon's module for docs/rules-hands-and-phones.md, "The hand itself". hands_ps.py and of_cast.py are not
edited, so shipped films keep their drawing (the freeze rule). A new drawing script calls setup() once, before
hands_v4.enable() when it uses hands_v4.

hands_ps puts the thumb on local side s = arm * sign(cos a) of the forearm (a: its angle on screen, cos 0 counts
as +). A mirror image turns a into 180 - a and arm into -arm, and must turn s into -s. That rule never does: two
forearms hanging down lean to opposite sides of vertical, and both thumbs land on one screen side, two left hands;
two forearms out level get one thumb up and one down. Here, at every angle:

  s = arm * sign(sin a)      hanging: the thumb toward the body; raised: toward the head; mirror pairs mirror

Animator's da_arms.setup() (episode 15) used this only for forearms nearer vertical and kept the old rule for
level ones, so level and raised pairs stayed unmirrored, and at 45 degrees one arm switched rules inside a move
and its thumb jumped across the hand in one frame. Here the side only changes when a forearm crosses level, and
inside shot() every hand keeps the side of its first drawing in that shot. A hand is known by its place in the frame's drawing order, so call
frame() before each frame. Without shot() each drawing gets the rule on its own.

  hands_lr.setup()
  with hands_lr.shot():
      for t in times:
          hands_lr.frame()
          draw_frame(t)

LOG holds what was drawn, for check(): two hands of one figure in a mirror pose that are not mirrored (two left
hands), a hanging thumb turned away from the body, and a thumb that changed sides between two frames of a shot.
"""
import contextlib
import math

_SET = [False]
_SHOT = [None]           # {index: side} inside shot(), else None
_IDX = [0]
_FRAME = [0]
LOG = []                 # (frame, index, (x, y) device, a device, side, thumb x direction, w device)
CUTS = set()             # frames that start a new pose
MODE = ["fix"]           # "old": draw as hands_ps does, only log it (the before picture, and the gate's own test)


def _sgn(v):
    return 1 if v >= 0 else -1


def side(arm, d):
    """The local side of the forearm the thumb goes on. arm: -1 screen-left, 1 screen-right."""
    return arm * _sgn(math.sin(math.atan2(d[1], d[0])))


def arm_for(s, d):
    """The arm to hand hands_ps so its own rule, arm * sign(cos a), puts the thumb on side s."""
    a = math.atan2(d[1], d[0])
    return s * _sgn(math.cos(a))


def _record(k, hx, hy, w, d, s):
    c = k.c
    x, y = c.user_to_device(hx, hy)
    fx, fy = c.user_to_device_distance(d[0], d[1])
    a = math.atan2(fy, fx)
    tx, _ty = c.user_to_device_distance(-d[1] * s, d[0] * s)     # local +y, times the side
    ww = abs(c.user_to_device_distance(w, 0)[0]) or w
    LOG.append((_FRAME[0], _IDX[0], (x, y), a, s, _sgn(tx) if abs(tx) > 1e-9 else 0, ww))


def _pick(k, hx, hy, w, d, arm):
    if MODE[0] == "old":                                           # hands_ps as it is, logged for check()
        s = arm * _sgn(math.cos(math.atan2(d[1], d[0])))
        _record(k, hx, hy, w, d, s)
        _IDX[0] += 1
        return arm
    s = side(arm, d)
    if _SHOT[0] is not None:
        s = _SHOT[0].setdefault(_IDX[0], s)
    _record(k, hx, hy, w, d, s)
    _IDX[0] += 1
    return arm_for(s, d)


def setup():
    """Wraps hands_ps.draw for the whole process, and hands_v4's own rows when hands_v4 is importable."""
    if _SET[0]:
        return
    import hands_ps as hp
    try:
        import hands_v4 as hv
    except ImportError:
        hv = None
    if hv is not None:
        assert not getattr(hv, "_ORIG", None), "hands_lr.setup() must run before hands_v4.enable()"
    o_hp = hp.draw

    def hp_draw(k, g, hx, hy, w, skin, d, arm):
        return o_hp(k, g, hx, hy, w, skin, d, _pick(k, hx, hy, w, d, arm))
    hp.draw = hp_draw
    if hv is not None:
        o_hv = hv.draw

        def hv_draw(k, g, hx, hy, w, skin, d, arm):
            if g in hv.DRAW and hp.GLOVE[0] is None:
                arm = _pick(k, hx, hy, w, d, arm)
            return o_hv(k, g, hx, hy, w, skin, d, arm)
        hv.draw = hv_draw
    _SET[0] = [hp, o_hp, hv, hv.draw if hv else None, o_hv if hv else None]


def teardown():
    """Puts hands_ps.draw (and hands_v4.draw) back. For sheets that draw before and after in one process."""
    if not _SET[0]:
        return
    hp, o_hp, hv, _w, o_hv = _SET[0]
    hp.draw = o_hp
    if hv is not None:
        hv.draw = o_hv
    _SET[0] = False


@contextlib.contextmanager
def shot():
    saved = _SHOT[0]
    _SHOT[0] = {}
    _IDX[0] = 0
    try:
        yield
    finally:
        _SHOT[0] = saved


def frame(cut=False):
    """Before each frame. cut: this frame does not continue the last one (a new pose), so no jump is checked."""
    _FRAME[0] += 1
    _IDX[0] = 0
    if cut:
        CUTS.add(_FRAME[0])


def check(log=None):
    """Faults in the drawn hands: (frame, index, what). Hands are paired within one figure's reach."""
    log = LOG if log is None else log
    faults = []
    frames = {}
    for row in log:
        frames.setdefault(row[0], []).append(row)
    for f, rows in sorted(frames.items()):
        for r in rows:
            (x, y), w = r[2], r[6]
            mates = [m for m in rows if m is not r and abs(m[2][0] - x) < 6 * w and abs(m[2][1] - y) < 2.5 * w]
            if not mates:
                continue
            m = min(mates, key=lambda m: abs(m[2][0] - x))
            mirror = abs(math.remainder(r[3] - (math.pi - m[3]), 2 * math.pi)) < math.radians(25)
            if mirror and r[4] == m[4] and r[1] < m[1]:
                faults.append((f, r[1], "two %s hands (with hand %d)" % ("left" if r[5] < 0 else "right", m[1])))
            hanging = abs(math.sin(r[3])) > abs(math.cos(r[3])) and math.sin(r[3]) > 0
            if mirror and hanging and r[4] != m[4] and r[5] != _sgn(m[2][0] - x):
                faults.append((f, r[1], "thumb turned away from the body"))
    last = {}
    for row in log:
        f, i, _p, a, s = row[:5]
        prev = last.get(i)
        if prev and prev[0] == f - 1 and f not in CUTS and prev[2] != s and abs(math.remainder(a - prev[1], 2 * math.pi)) < math.radians(60):
            faults.append((f, i, "thumb changed sides between frames"))
        last[i] = (f, a, s)
    return faults


def reset_log():
    LOG.clear()
    CUTS.clear()
    _FRAME[0] = 0
    _IDX[0] = 0
