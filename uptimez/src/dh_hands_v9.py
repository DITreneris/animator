"""Daddy's Home v9 (26 Nov, series hands/phones plan, Tomas "2-3-4"): the film's held phones in the canon's grip.
Opt-in: install() replaces three drawers for the v9 render only; v8 and earlier draw as before.

- dh_scenes._phone_in_hand (Don's call, 0.4-0.7b: at his ear, then lowered): its own 14 x 27 rectangle and a hands2
  "grip" -> of_cast.phone_grip, which hands_v4 (ALL_V4C) draws as v4c: at the ear its back to us, lowered its lit screen.
- dh_anim8.r_call (11.6, "Answer it."): Father's phone was a rectangle with an oval thumb -> phone_grip v4c, the
  thumb pressing the green button (thumb_tip) once he presses.
- dh_props.booth (the post on the table, 0.2-0.3): the guard's hands2 "grip" on the phone's left edge -> of_cast.clutch
  (the canon's edge grip: the back of the hand outside, four fingers over the front), turned to the edge.
The phones and hands keep v8's places, sizes and timings."""
import math
import kit
import of_cast as oc

_ORIG = {}
SKIN_DON = None


def _lit_screen(c):
    c.set_source_rgb(0.55, 0.80, 1.0); c.rectangle(-18, -34, 36, 66); c.fill()


def phone_in_hand(k, d, lit=True, side=1, at_ear=False):
    """v8's _phone_in_hand, the same places: lowered, the phone (centre hx - 4, hy - 8, turned -0.25) on his palm;
    at the ear (head + (31, -4), turned 0.12) its back to us, the hand round it."""
    skin = kit.PEOPLE["DON"]["skin"]
    hx, hy = d["hands"][1 if side > 0 else 0]
    s = 14.0 / 44.0                                   # v8's phone was 14 wide: phone_grip's 44 x 76 at this scale
    if at_ear:
        cx, cy, ang = d["head"][0] + 31, d["head"][1] - 4, 0.12
    else:
        cx, cy, ang = hx - 4, hy - 8, -0.25
    px, py = cx - 22 * s * math.sin(ang), cy + 22 * s * math.cos(ang)     # the palm under the phone's centre
    real = oc.phone

    def rimmed(k_, x, y, s_, screen=None, ang_=0.0, face_out=True):
        """The Offer v58's pale edge on a phone's back (PHONE_RIM there): at his ear, on the dark throne, two cold
        viewers of v9's first render read the black back as "a hand on his ear"."""
        real(k_, x, y, s_, screen, ang_, face_out)
        if not screen:
            c = k_.c
            c.save(); c.translate(x, y); c.rotate(ang_); c.scale(s_, s_)
            c.set_source_rgb(0.70, 0.74, 0.80); c.set_line_width(1.8); c.new_path(); c.rectangle(-18.5, -34.5, 37, 69); c.stroke()
            c.restore()
    oc.phone = rimmed
    try:
        oc.phone_grip(k, px, py, s, screen=(_lit_screen if lit and not at_ear else None), ang=ang, skin=skin,
                      body_x=d["head"][0], back=at_ear)
    finally:
        oc.phone = real


def _call_screen(pressed):
    def f(c):
        c.set_source_rgb(0.55, 0.80, 1.0); c.rectangle(-19, -34, 38, 68); c.fill()
        c.set_source_rgb(0.20, 0.75, 0.30); c.arc(0, 12.6, 11, 0, 2 * math.pi); c.fill_preserve()   # the call button
        c.set_source_rgb(*kit.INK); c.set_line_width(1.6); c.stroke()
    return f


def r_call(s, k, o, t, tt, n):
    """dh_anim8.r_call with the phone in phone_grip v4c (the rest is v8's code, line for line)."""
    import dh_anim8 as a8
    import dh_scenes as ds
    import dh_props as dp
    import dh_cast as dc
    i = a8.idx(t)
    pressed = i >= 2
    dp.ceo_chair(k, ds.THR5, a8.CH[1], a8.CH[2])
    ds._arm_phone_off = True
    f_ = dc.father(k, a8.FA2[0], a8.FA2[1], a8.FS, pose=(-20, -130, 8, 0), face="hard", look=(1, 0))
    hx, hy = f_["hands"][0]
    sc = 28.0 / 44.0                                  # v8's phone: 28 x 50 centred at (hx - 4, hy - 30)
    cx, cy = hx - 4, hy - 30
    tip = (0.0, -22.0 + 12.6) if pressed else None    # the thumb on the green button, in the grip's units from the palm
    oc.phone_grip(k, cx, cy + 22 * sc, sc, screen=_call_screen(pressed), skin=dc.SKIN_F, body_x=a8.FA2[0], thumb_tip=tip)
    if i == 2:
        ds._lines(k, [(hx - 22, hy - 44, hx - 30, hy - 52), (hx + 14, hy - 44, hx + 22, hy - 52)])
    look = (1, 0.15) if i < 4 else ((0.6, 0.7) if i < 6 else (0.85, 0.9))
    d = a8.dq.don_zipped(k, ds.DON6[0] - 6, ds.DON6[1] + 9, a8.DS_, face="shock", look=look)
    a8.A.fear(k, d["head"], a8.DS_, "o")
    ds._sweat8(k, d["head"], 2)
    a8.ringing_phone(k, pressed and (n % 3 != 2), n)
    a8.father_mouth(k, a8.HDF, s.loud("11.6", tt))
    if s.speaking("11.6", tt):
        o["say"] = a8.say_f("Answer it.")


def _booth(k, *a, **kw):
    """dp.booth with the guard's hand on the phone's left edge as of_cast.clutch."""
    import hands2 as h2
    real = h2.hand

    def hand(k_, x, y, ang, w, skin, pose="open", side=1, seed=0, nail=True):
        if pose == "grip" and (x, y) == (96, 690):
            c = k_.c
            c.save(); c.translate(140, 690); c.rotate(-math.pi / 2 + 0.08)   # the edge's top turned to the left edge
            oc.clutch(k_, 0, 0, w * 0.95, skin)
            c.restore()
            return
        return real(k_, x, y, ang, w, skin, pose, side, seed, nail)
    import dh_props as dp
    real_e = dp.ellipse

    def ellipse(k_, x, y, rx, ry, col, seed, *a_, **kw_):
        if (x, y, rx, ry) == (150, 690, 40, 34):                # v8's guard's hand (hands2 off): the same clutch
            return hand(k_, 96, 690, 0.0, 70, col, "grip")
        return real_e(k_, x, y, rx, ry, col, seed, *a_, **kw_)
    h2.hand, dp.ellipse = hand, ellipse
    try:
        return _ORIG["booth"](k, *a, **kw)
    finally:
        h2.hand, dp.ellipse = real, real_e


def install():
    if _ORIG:
        return
    import dh_scenes as ds
    import dh_anim8 as a8
    import dh_props as dp
    _ORIG.update(pih=ds._phone_in_hand, r_call=a8.r_call, booth=dp.booth)
    ds._phone_in_hand = phone_in_hand

    a8.r_call = r_call
    a8.sc.DRAW["11.6"] = r_call                       # the scene's map holds the function itself (lesson 109)
    dp.booth = _booth
