"""Downloads Expedition, ending A. See dlx.py.
Applies the cuts in dlx.CUTS (film time, seconds) as a time map (new time -> film time) and forwards the
engine's unquantised time to dlx. v06: two cuts, 0.6 s at the start of the pile beat and 0.6 s of the wide
hold before MAX walks in."""
import dlx

dlx.ENDING = "A"
DURATION = dlx.DURATION - sum(d for _, d in dlx.CUTS)
RAW_T = 0.0


def old(t):
    for at, d in dlx.CUTS:
        if t >= at:
            t += d
    return t


def new(x):
    out = x
    for at, d in dlx.CUTS:
        if x >= at + d:
            out -= d
        elif x > at:
            out -= x - at
    return out


def _wrap(fn, a_old):
    def g(k, t, tl):
        dlx.RAW_T = old(RAW_T)
        to = old(t)
        fn(k, to, to - a_old)
    g.__name__ = fn.__name__
    return g


PANELS = [(new(a), new(b), _wrap(fn, a)) for (a, b, fn) in dlx.PANELS]


def shake(t):
    return dlx.shake(old(t))


overlay = dlx.overlay
