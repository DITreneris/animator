"""S1v3.3 without the sniff tag (ends on DON's eyebrow). See s133.py."""
import s133
from s133 import overlay, shake  # noqa: F401

s133.END = 20.5
DURATION = s133.duration(20.5)
RAW_T = 0.0


def frame(k, t, tl):
    s133.RAW_T = RAW_T
    s133.frame(k, t, tl)


PANELS = [(0.0, DURATION, frame)]
