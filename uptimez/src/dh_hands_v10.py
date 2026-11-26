"""Daddy's Home v10 (26 Nov, Tomas's /grill-me after v9's cold test): v9's hands (dh_hands_v9) plus
- 11.6 "Answer it.": Father's phone is logged as a thing his box must stay off (like the price tag), so the phone and
  the pressing thumb stay clear (v9: the box covered the phone, two cold viewers of two). The box on his other side,
  Tomas's pick, was tried first: there it covered Don's face, so it stays on his side, off the phone;
- the booth (0.3-0.7): BOTH hands on the post are Father's: the left sleeve is his velvet (v9: a bodyguard's grey
  sleeve, read as "someone else's arm"), and his ring hand clutches the post's right edge, four fingers over its
  front, the ring on them (v9: a round fist, "no fingers, pasted on"). The tap (0.5) lifts the whole hand.
Opt-in: install() after dh_hands_v9.install()."""
import math
import kit
import of_cast as oc
import dh_hands_v9 as h9

_ORIG = {}


def r_call(s, k, o, t, tt, n):
    h9.r_call(s, k, o, t, tt, n)
    _keep_phone(k)
    # the box stays on his phone's side, now kept off the phone itself (its right side held Don's face: v10 try 1)


def _keep_phone(k):
    """Father's phone (where dh_hands_v9.r_call put it) logged as a thing the bubble must stay off, like the price tag."""
    import numpy as np
    import dh_speech as SP
    import dh_anim8 as a8
    import dh_cast as dc
    c = k.c
    w = c.get_target().get_width()
    if w < 270:
        return
    f_hands = LAST_HAND[0]
    if f_hands is None:
        return
    hx, hy = f_hands
    pts = [c.user_to_device(hx - 4 + dx, hy - 30 + dy) for dx in (-22, 22) for dy in (-34, 30)]
    sc_ = w / 540.0
    xs = [p_[0] / sc_ for p_ in pts]; ys = [p_[1] / sc_ for p_ in pts]
    M = np.zeros((960, 540), bool)
    x0, x1 = max(0, int(min(xs)) - 6), min(540, int(max(xs)) + 6)
    y0, y1 = max(0, int(min(ys)) - 6), min(960, int(max(ys)) + 6)
    M[y0:y1, x0:x1] = True
    SP.KEEP.append(dict(mask=M))


LAST_HAND = [None]


def booth(k, seed=2500, tap=0.0, face_down=False, post="simple"):
    import dh_props as dp
    import dh_cast as dc
    real_cut, real_e, real_rect, real_ring = dp.cut, dp.ellipse, dp.rect, dc.ring
    state = {}

    def cut(k_, pts, col, *a, **kw):
        if pts and tuple(pts[0]) == (-20, 560):                    # the left sleeve: his velvet, not a guard's grey
            return real_cut(k_, pts, dc.VELVET, *a, **kw)
        return real_cut(k_, pts, col, *a, **kw)

    def ellipse(k_, x, y, rx, ry, col, sd, *a, **kw):
        if (x, y, rx, ry) == (410, 700, 46, 38):                   # his ring fist -> a clutch on the post's right edge
            c = k_.c
            c.save(); c.translate(366, 704 - 12 * tap); c.rotate(math.pi / 2 + 0.08 - 0.10 * tap)
            oc.clutch(k_, 0, 0, 74, col)
            c.restore()
            c.save(); c.translate(334, 690 - 12 * tap); c.rotate(math.pi / 2 + 0.08)
            real_ring(k_, 0, 0, 2.0, sd + 6)                       # the ring, on his fingers over the front
            c.restore()
            state["skip"] = True
            return
        return real_e(k_, x, y, rx, ry, col, sd, *a, **kw)

    def rect(k_, x, y, w, h, col, sd, *a, **kw):
        if state.get("skip") and col == dc.SKIN_F:                 # v9's four finger blocks: the clutch has its own
            return
        return real_rect(k_, x, y, w, h, col, sd, *a, **kw)

    def ring(k_, x, y, s_=1.0, sd=1595):
        if state.get("skip"):
            return
        return real_ring(k_, x, y, s_, sd)
    dp.cut, dp.ellipse, dp.rect, dc.ring = cut, ellipse, rect, ring
    try:
        return _ORIG["booth"](k, seed, tap, face_down, post)
    finally:
        dp.cut, dp.ellipse, dp.rect, dc.ring = real_cut, real_e, real_rect, real_ring


def install():
    if _ORIG:
        return
    import dh_say as SY
    SY.SAY["Answer it."] = dict(SY.SAY.get("Answer it.", {}), form="T")   # over his head (a bare top): left was his
                                                                       # phone, right Don's face (his rig is not logged)
    import dh_anim8 as a8
    import dh_props as dp
    _ORIG["booth"] = dp.booth                                     # v9's booth (the clutch on the left edge)
    dp.booth = booth
    a8.r_call = r_call
    a8.sc.DRAW["11.6"] = r_call
