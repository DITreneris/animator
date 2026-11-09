"""Downloads Expedition, ending B. See dlx.py.
Applies the 0.6 s trim at the start of the pile beat as a time map (new time -> film time) and forwards the
engine's unquantised time to dlx."""
import dlx

dlx.ENDING = "B"
DURATION = dlx.DURATION - dlx.TRIM
RAW_T = 0.0


def old(t):
    return t if t < dlx.TRIM_AT else t + dlx.TRIM


def new(x):
    return x if x <= dlx.TRIM_AT else max(dlx.TRIM_AT, x - dlx.TRIM)


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
