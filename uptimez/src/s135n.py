"""S1v3.5 without the sniff tag. See s135.py."""
import s135
import s133

s133.END = 20.5
DURATION = s133.duration(20.5)
RAW_T = 0.0


def frame(k, t, tl):
    s133.RAW_T = RAW_T
    s133.frame(k, t, tl)


PANELS = [(0.0, DURATION, frame)]
shake = s135.shake
overlay = s135.overlay
