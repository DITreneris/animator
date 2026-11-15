"""Animatic timing for "Raises for Everyone": storyboard v3 (tg_sb.py, 35.0 s) re-timed to the real voice takes.
Four shots hold longer at their end (the last moment is held, the next shot starts later); nothing inside a shot moves.
  8b +0.25 s  Sofía's "She refused. She didn't fail." (1.76 s take)
  8c +0.30 s  Don's "Same thing here." (1.19 s, mouth full)
  9  +0.40 s  Pam's "You're a walking policy violation." (2.05 s, slow and deadpan)
  11 +0.65 s  the robot's muffled "Okay. Signed." (1.26 s)
-> 36.6 s. remap(t) turns a storyboard-v3 time into an animatic time (for lines and effects)."""
EXTRA = {"s8b": 0.25, "s8c": 0.30, "s9_v3": 0.40, "s11": 0.65}


def build(panels):
    """[(t0, t1, fn)] in v3 time -> [(t0', t1', fn, shift, v3_t1)] in animatic time."""
    out, shift = [], 0.0
    for t0, t1, fn in panels:
        ext = EXTRA.get(fn.__name__, 0.0)
        out.append((t0 + shift, t1 + shift + ext, fn, shift, t1))
        shift += ext
    return out


def remap(t, panels):
    shift = 0.0
    for t0, t1, fn in panels:
        if t0 <= t < t1:
            return t + shift
        shift += EXTRA.get(fn.__name__, 0.0)
    return t + shift


def duration(panels):
    return panels[-1][1] + sum(EXTRA.get(fn.__name__, 0.0) for _, _, fn in panels)


def remap_end(t, panels):
    """A shot-end time (the slot a line must fit in): includes that shot's own hold."""
    for t0, t1, fn in panels:
        if t0 < t <= t1:
            return remap(t - 1e-6, panels) + 1e-6 + EXTRA.get(fn.__name__, 0.0)
    return remap(t, panels)
