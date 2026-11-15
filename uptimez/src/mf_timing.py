"""Animatic timing for "Mandatory Fun": storyboard v2 (mf_sb.py, 33.0 s) re-timed to the real voice takes (measured:
the robot's "Failure to enjoy training. Detention required." is 2.83 s, "Human approval required." 1.62 s, Don's
"Sofia, you're under arrest." 1.52 s). Voices are never sped up. Two ways to make room:
- "hold": the shot's last moment is held longer (nothing inside it moves): s1, s3, s4, s4c, s6b, s7, s8b, s9a, s12;
- "stretch": the whole shot plays slower (s5, so Don's sulk lands after Pam's "Officer? I confess.").
remap(t) turns a storyboard time into an animatic time (for lines and effects); sb_time(a) goes back."""
EXTRA = {"s1": 0.30, "s3": 0.25, "s4": 0.35, "s4c": 0.15, "s5": 0.60, "s6b": 1.45, "s7": 0.10, "s8b": 0.70,
         "s9a": 0.15, "s12": 0.30}
STRETCH = {"s5"}


def build(panels):
    """[(t0, t1, fn)] in storyboard time -> [(a0, a1, fn, t0, t1, mode)] in animatic time."""
    out, shift = [], 0.0
    for t0, t1, fn in panels:
        ext = EXTRA.get(fn.__name__, 0.0)
        mode = "stretch" if fn.__name__ in STRETCH else "hold"
        out.append((t0 + shift, t1 + shift + ext, fn, t0, t1, mode))
        shift += ext
    return out


def remap(t, panels):
    for a0, a1, fn, t0, t1, mode in build(panels):
        if t0 <= t < t1:
            if mode == "stretch":
                return a0 + (t - t0) * (a1 - a0) / (t1 - t0)
            return a0 + (t - t0)
    b = build(panels)[-1]
    return b[1] + (t - b[4])


def sb_time(a, panels):
    """Animatic time -> (panel fn, storyboard time inside it)."""
    for a0, a1, fn, t0, t1, mode in build(panels):
        if a0 <= a < a1:
            if mode == "stretch":
                return fn, t0 + (a - a0) * (t1 - t0) / (a1 - a0)
            return fn, min(t0 + (a - a0), t1 - 1e-3)
    return panels[-1][2], panels[-1][1] - 1e-3


def duration(panels):
    return build(panels)[-1][1]
