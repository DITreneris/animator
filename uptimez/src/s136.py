"""Saved to Cloud S1v3.6 - S1v3.5 plus the final polish:
1 the doodle is ~40% bigger in DON's last shot and sits centre-right, clear of the app buttons
4 the cloud and PAM's file move 30 px left in shots 3-5 (out of the right-hand button column)
6 "15 SECONDS EARLIER..." gets its own bigger bar between the heads and the wall sign
(audio fixes 2-3 are in sound_s136.py; the 1080x1920 render is engine_hd.py)
New module only: patches s132/s133/s135 at runtime."""
import kit
import s132
import s133
import s135
import anim
import pt4
import pt42
from kit import W, H, INK, rect, text, ease, clamp, lerp

SHIFT = -30


def shifted(fn):
    def g(k, t, tl):
        s132.sky(k)                    # fills the strip the shift uncovers
        c = k.c
        c.save()
        c.translate(SHIFT, 0)
        fn(k, t, tl)
        c.restore()
    g.__name__ = fn.__name__
    return g


def sh8_don(k, t, tl):
    """DON holds the doodle up beside his face, bigger and nearer the centre."""
    s132.STATE["t"] = t
    c = k.c
    z = 1 + 0.06 * ease(clamp((s132.RAW_T - 17.0) / 3.5))
    c.save()
    anim.camera(c, 230, 560, z)
    pt4.accent_wall(k, "DON")
    pt42.portrait_frame(k, 330, 110, 140, 130)
    up = ease(clamp((t - 17.2) / 0.6))
    s132.STATE["brow"] = ease(clamp((t - 19.6) / 0.15))
    pose = anim.keyed(t, [(17.0, "stand"), (17.4, (-8, 0, 120, 30))], dur=0.4, overshoot=False)
    s132.who("DON", k, 130, 1250, 2.05, pose=pose, face="neutral", seed=63, look=(0.0, lerp(1, 0, up)))
    s132.STATE["brow"] = 0.0
    lift = ease(clamp((t - 17.0) / 0.4))
    c.save()
    c.translate(350, lerp(980, 575, lift))
    c.scale(0.55, 0.55)
    s135.page(k, 0, 0, 470, 400, 0.05)
    c.restore()
    c.restore()


WRAP = {"sh3_gulp": shifted, "sh4_hold": shifted, "sh5_achoo": shifted}
s132.PANELS = [(a, b, sh8_don if fn.__name__ == "sh8_don" else WRAP.get(fn.__name__, lambda f: f)(fn))
               for (a, b, fn) in s132.PANELS]


def caption(k, T):
    if s133.COLD + s133.REW - 0.05 <= T < s133.COLD + s133.REW + 0.9:
        rect(k, 50, 352, 440, 70, (1, 1, 1), 970)
        text(k, "15 SECONDS EARLIER...", 270, 387, 36, INK)


s133.caption = caption

DURATION = s133.duration(21.5)
RAW_T = 0.0


def frame(k, t, tl):
    s133.RAW_T = RAW_T
    s133.frame(k, t, tl)


PANELS = [(0.0, DURATION, frame)]
shake = s133.shake
overlay = s133.overlay
