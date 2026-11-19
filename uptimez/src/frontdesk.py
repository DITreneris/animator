"""The front desk set, for every episode from 10 on: a stable name for the current version (now set v4, fs_set4.py).
When the set changes, pin the old one as fs_set4.py stays, add fs_set5.py, and point this file at it.
Use: import frontdesk as fd; fd.draw_set(k, cast="home" | {...}); fd.HOME, fd.ZONES, fd.CX0, fd.CX1, fd.SHRED ..."""
from fs_set4 import *                                      # noqa: F401,F403
from fs_set4 import draw_set, HOME, ZONES, CX0, CX1, SHRED, PORT, OFFICE, WW, DX, shadow, counter, mom_home  # noqa
