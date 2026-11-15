"""Animatic timing for "Secret Santa": storyboard v2 (ss_sb.py, 34.6 s) re-timed to the real voice takes
(ss_takes_v1.json). Voices are never sped up. Each panel gets a piecewise-linear time warp with knots at 0, at every
line's start and at the panel's end: a line may not start before the previous one has ended (plus GAP), and the panel
may not end before its last line has ended (plus TAIL). Only the stretch of time that needs room gets slower; the rest
of the panel (an ECU uncap, a stamp, a reaction before the first line) plays at its storyboard speed.
build(panels) -> [(a0, a1, fn, t0, t1, knots)], knots = [(sb seconds into panel, animatic seconds into panel)].
remap(t, panels): storyboard time -> animatic time; sb_local(knots, x): animatic seconds into the panel -> storyboard."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TAKES = json.load(open(os.path.join(HERE, "ss_takes_v1.json")))
GAP, TAIL = 0.15, 0.35
TAIL_BY = {"s6b": 0.45, "s15b": 0.9, "s10b": 0.25}       # the beats after a line that need air: Don's smirk, the hold


def knots_for(name, length):
    lines = sorted((l for l in TAKES if l["panel"] == name), key=lambda l: l["at"])
    ks = [(0.0, 0.0)]
    prev_end = None
    for l in lines:
        s, (ls, la) = l["at"], ks[-1]
        a = la + (s - ls)
        if prev_end is not None:
            a = max(a, prev_end + GAP)
        if s > ls:
            ks.append((s, a))
        prev_end = a + l["dur"]
    ls, la = ks[-1]
    end = la + (length - ls)
    if prev_end is not None:
        end = max(end, prev_end + TAIL_BY.get(name, TAIL))
    ks.append((length, end))
    return ks


def build(panels):
    out, shift = [], 0.0
    for t0, t1, fn in panels:
        ks = knots_for(fn.__name__, t1 - t0)
        out.append((t0 + shift, t0 + shift + ks[-1][1], fn, t0, t1, ks))
        shift += ks[-1][1] - (t1 - t0)
    return out


def _interp(ks, x, src, dst):
    for (p, q) in zip(ks, ks[1:]):
        if p[src] <= x <= q[src]:
            if q[src] == p[src]:
                return p[dst]
            return p[dst] + (x - p[src]) * (q[dst] - p[dst]) / (q[src] - p[src])
    return ks[-1][dst] + (x - ks[-1][src])


def remap(t, panels):
    for a0, a1, fn, t0, t1, ks in build(panels):
        if t0 <= t < t1:
            return a0 + _interp(ks, t - t0, 0, 1)
    b = build(panels)[-1]
    return b[1] + (t - b[4])


def sb_local(ks, x):
    return _interp(ks, x, 1, 0)


def duration(panels):
    return build(panels)[-1][1]
