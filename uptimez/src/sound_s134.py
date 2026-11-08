"""Audio for S1v3.4: same as sound_s133.py with 1.0 s freezes. Usage: python3 sound_s134.py s134 | s134n"""
import os
import sys
import s133
s133.FREEZE = 1.0
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sound_s133.py")).read())
