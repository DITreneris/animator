"""Mute-test frames: xmas_anim10 without speech bubbles, shouts or sound words."""
import xmas_anim10 as M
import xmas_bubbles as xb
import xmas_anim2 as A2
A2.speech4 = lambda *a, **k: None
xb.speech = lambda *a, **k: None
xb.shout = lambda *a, **k: None
xb.burst = lambda *a, **k: None
import xmas_anim8 as M8
M8._burst0 = xb.burst
PANELS, DURATION, shake = M.PANELS, M.DURATION, M.shake
RAW_T = 0.0
