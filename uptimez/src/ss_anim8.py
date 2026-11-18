"""ANIMATION v8 of "Secret Santa" (18 Nov), the final: v7 (ss_anim7.py, kept) with the lipstick open from frame 0.
Capped, it was a black-and-gold tube that read as a marker; the uncap at about 1 s happened behind the stamp, and
after the kiss. Now frame 0 (and the last frame) shows the open lipstick, its dusty-rose angled tip up, the cap gone;
there is no later uncap (the wide shot after it already has it open). The print on the glass and the robot's stamp
move up and right, clear of the lipstick. The sound is v5's, less nothing: its cap pop now lands on nothing visible,
so v8 uses ss_sound_v8.py (v5 without the pop).
Module protocol for engine_v / engine_hd: PANELS, DURATION, RAW_T, shake."""
import ss_anim7 as M7
import ss_anim6 as M6
import ss_set_sheet as sss
import sofia_sheet_ss as sfs

DURATION = M7.DURATION
RAW_T = 0.0
M6.KX, M6.KY = 62, 58                          # the print and the stamp: up and right, off the lipstick
_hand0 = sss.pam_hand
_lip0 = sfs.pam_hand_lipstick


def pam_hand(k, uncap=0.0):
    sfs.pam_hand_lipstick = lambda k2, x, y, s, u, *a, **kw: _lip0(k2, x, y, s, 1.0, lift_max=900)
    try:
        return _hand0(k, 1.0)
    finally:
        sfs.pam_hand_lipstick = _lip0


sss.pam_hand = pam_hand
PANELS = M7.PANELS


def shake(t):
    return M7.shake(t)
