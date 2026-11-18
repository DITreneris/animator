"""ANIMATION v9 of "Secret Santa" (18 Nov), the final: v8 (ss_anim8.py, kept) without the SOFIA name plate that v5 put
on the front of her desk (Tomas: not needed; it sits low on the desk front and is not part of the set). The sound is
v8's (ss_mix_v8.wav). Module protocol for engine_v / engine_hd: PANELS, DURATION, RAW_T, shake."""
import ss_anim8 as M8
import ss_anim5 as M5
import ss_set as S

DURATION = M8.DURATION
RAW_T = 0.0
S.desk = M5._desk0                              # the desk as it was, no plate
PANELS = M8.PANELS


def shake(t):
    return M8.shake(t)
