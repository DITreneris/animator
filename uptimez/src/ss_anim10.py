"""ANIMATION v10 of "Secret Santa" (18 Nov), the final: v9 (ss_anim9.py, kept) with three last touches:
- shot 4, after the lens insert: Pam no longer holds the glasses out (one viewer still saw "a spoon"); they hang on her
  bead chain and her hands come together as she melts;
- shot 15, after the tags insert: the wide shot is reframed onto Pam, Don and Sofia (she was almost out of frame), so
  Sofia's unimpressed look away from TO: SOFIA (heart) is the last reaction;
- Don's one-word "Sofia." is a new, clearer take (ss_sound_v9.py; Whisper heard the old one as "Soviet").
Module protocol for engine_v / engine_hd: PANELS, DURATION, RAW_T, shake."""
import ss_anim9 as M9
import ss_anim6 as M6
import ss_anim5 as M5
import ss_anim4 as M4
import ss_sb as sb
import ss_set as S
import xmas_bubbles as xb

DURATION = M9.DURATION
RAW_T = 0.0
X = S.POS
CAM15_END = (650, 470, 1.0)                       # Pam, Don and Sofia; the robot has had its tick in the insert


def s4_after(k, t, tl):
    """sb.s4b after the lens insert, with the glasses on her chain and her hands together."""
    fx = sb.S4_FIX[0]

    def draw():
        S.backdrop(k, t=tl)
        lean = -sb.lerp(0, 8 if fx else 14, sb.ease((tl - 0.8) / 0.4))
        d = sb.ds.don(k, X["pam"] + (165 if fx else 130), S.FEET, 1.0, "stand", "smug", look=(-1, 0.4),
                      shades="down", lean=lean, mouth=sb.talk(tl, 1.25, 2.3))
        o = sb.ps.pam(k, X["pam"] - 40, S.FEET, 1.0, sb.ps.POSE_SHY, "dinner" if tl > 2.0 else "hopeful",
                      look=(1, -0.35), glasses="chain", lean=2)
        return o, d
    cam = sb.CAM4F if fx else sb.CAM4B
    o, d = sb.world(k, tl, "s4b", cam, draw)
    if tl > 1.2:
        xb.speech(k, "Agent Santa.\nLicensed to gift.", sb.above(cam, d["head"], 70), t, 1.25, size=26, at=(380, 190))
    if tl > 2.05:
        hx, hy = S.to_screen(cam, X["pam"] - 70, S.FEET - 330)
        sb.pop_heart(k, hx, hy, tl, 2.05, 0.6, 28)


def s4_new(k, t, tl):
    if M4.G0 <= tl < M4.G1:
        return M4.glasses_insert(k, t, tl)
    return s4_after(k, t, tl) if tl >= M4.G1 else sb.s4b(k, t, tl)


def s15_new(k, t, tl):
    if M4.I0 <= tl < M4.I1:
        return M5._tags_insert(k, t, tl)
    if tl < M4.I1:
        return M4.s15_wide(k, t, tl)
    keep = sb.CAM15B
    sb.CAM15B = CAM15_END
    try:
        return M4.s15_wide(k, t, tl)
    finally:
        sb.CAM15B = keep


_NEW = {"s4b": s4_new, "s15b": s15_new}
_rows = []
for a0, a1, fn, t0, t1, ks in M6._rows:
    if fn.__name__ in _NEW:
        fn = M5.cam(fn.__name__, _NEW[fn.__name__])
    _rows.append((a0, a1, fn, t0, t1, ks))
PANELS = [(a0, a1, M5._wrap(a0, a1, fn, t0, t1, ks)) for a0, a1, fn, t0, t1, ks in _rows]


def shake(t):
    return M9.shake(t)
