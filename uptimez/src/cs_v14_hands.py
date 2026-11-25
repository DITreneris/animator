"""ONE STAR v14, the hands round (25 Nov, Tomas: "0:13 Don's elbow, 0:32 Pam's hand, 0:57 Pam's hand; go through every
hand"). Rules applied (docs/rules-hands-and-phones.md): fixed bones, target in reach; never route a hand past the
shoulder; a target too near the shoulder folds the arm into a lump (231); one target path per hand per shot; one
gesture per line; a phone's holder visible, upright to be read; one story word per screen.
  2.1  the call: the phone at his ear folded his arm over his head (the ear is 28 units from a 58-unit arm's shoulder).
       Now the phone is held in front of him (the 2.2 insert IS that screen) and he talks into his headset (mic down:
       sales mode, as scripted); after the flick his hand goes back down to his side (the hand on heart landed on the
       phone).
  4.1  Pam: STOP palm, then straight up to her glasses, and down bent: one path, no straight "pole" between; the palm
       1.5x (was 2.0, read as bigger than her face).
  6.3  Pam at the counter: her arm from her own shoulder, the sleeve outlined against her jacket, the elbow out; her
       other hand on the counter (both arms, mid-frame)."""
import math
import cs_scene1 as s1
import cs_scene2 as s2
import cs_scene4 as s4
import cs_scene6 as s6
import cs_hands as ch
import kit
import hands_ps as hp
from cs_scene1 import S, at, base, sb, ellipse
from kit import INK

DPS = 12


def ease(u):
    return s1.ease(u)


def lerp(a, b, u):
    return tuple(x + (y - x) * u for x, y in zip(a, b))


# ---- 2.1 -------------------------------------------------------------------------------------------------------------

PHONE_L = (5, 40)                                          # his screen-left arm: the phone held up in front, to be read
HEART2 = (474.0, 712.0)                                    # lower on the vest: 39 units from the shoulder, the arm bends


def _right_arm(d, pts):
    from cand_bc import ik
    g = s2._grip(pts)
    d = d - s2.FLICK_AT + 2
    if d < 0:
        tx, ty = s2.REST_R
    elif d <= 2:
        tx, ty = lerp(s2.REST_R, g, ease(d / 2.0))
    elif d <= 6:
        tx, ty = g
    else:                                                                          # then back down to his side on a curve
        u = ease((d - 6) / 6.0)                                                    # outward, never across the shoulder. The
        tx, ty = lerp(g, s2.REST_R, u)                                             # hand on heart is dropped: with the phone
        tx += 0 * math.sin(math.pi * u)                                            # in front, it landed on the phone (one gesture a line)
    return ik(s2.SH_R[0], s2.SH_R[1], tx, ty, s2.LN, s2.LN, -1)


def _shapes21():
    d = s1.CUR_D[0] - s2.FLICK_AT + 2
    right = "grab" if 0 <= d <= 6 else "quiet"
    return ["quiet", right]


def s2_1(k, d):
    """26 drawings (as v13). The phone held up in front of him, its screen to him (the call he made, 2.1a); he flicks
    his mic down to his mouth (sales mode) and talks into it; then his hand flat on his heart; the sales smile."""
    t = d / float(DPS)
    pts = s2._boom(d)
    a1, a2 = _right_arm(d, pts)
    talk = 0.0
    if s2.LINE21 <= t <= s2.LINE21 + 1.5:
        talk = (1.0, 0.5, 1.0, 0.0)[int((t - s2.LINE21) * DPS / 2) % 4]

    def back(k_):
        s2.cs_cal.wall(k_, s2.cs_cal.THU, t=d / float(DPS))

    def ex(k_, o):
        (lx, ly), (rx, ry) = o["don"]["hands"]
        hx, hy = (lx, ly) if lx < rx else (rx, ry)
        s1.phone_held(k_, hx, hy, sb.SC["don"], ang=0.22, buzz=False, d=d, seed=941)
        s1.fist(k_, hx, hy, sb.SC["don"], kit.PEOPLE["DON"]["skin"], 945)

    with s1.A.Don(pts, talk), s1.Breath(sb, "don", s1.br(d, 0.0, 0.010)):
        u = ease((d - s2.PAN21[0]) / float(s2.PAN21[1] - s2.PAN21[0]))
        cam = tuple(a_ + (b_ - a_) * u for a_, b_ in zip(s2.CAL21, s2.CAM21))
        S(k, cam, auto=False, portrait="hang", back=back, extra=ex,
          **base(cl=False, sf=False, pm=False, mm=False, rb=False, door=0.0,
                 dn=at("don", pose=PHONE_L + (a1, a2), face="happy", look=(-0.3, 0.6) if d < 6 else (1, 0))))


# ---- 4.1 -------------------------------------------------------------------------------------------------------------

GLASS41 = (120, 95)                                        # beside her temple, at the glasses' arm (158, 38: a finger over her head; 162, 70: over her brow)


def s4_1(k, d):
    """24 drawings (as v13), one path for her free hand: down -> STOP palm at him (d2-9) -> up to her glasses (d10-12),
    pushing them into her hair -> down again, bent (d15-19)."""
    px = 96 + (175 - 96) * ease(d / 7.0)
    cx = 318 - (318 - 285) * ease(d / 6.0)
    REST = (8, 0)
    if d < 10:
        st = ease((d - 2) / 3.0)
        arm = lerp(REST, s4.STOP41, st)
        s4.HAND41[0] = "palm" if st > 0.75 else ("grab" if st > 0.2 else "quiet")
    elif d < 15:
        u = ease((d - 10) / 2.0)
        arm = lerp(s4.STOP41, GLASS41, u)
        s4.HAND41[0] = "point" if u > 0.6 else "palm"
    else:
        u = ease((d - 15) / 3.0)
        a1 = GLASS41[0] + (REST[0] - GLASS41[0]) * u
        a2 = GLASS41[1] + (REST[1] - GLASS41[1]) * u + 60 * math.sin(math.pi * u)  # v16: bent on the way down, not folded (231): no level arm at him (a pole, a point)
        arm = (a1, a2)
        s4.HAND41[0] = "relax" if u > 0.3 else "point"
    lean = -3.0 * ease((d - 5) / 3.0) * (1 - ease((d - 10) / 4.0))

    def pre(k_):
        o = s4.pam(k_, px, s4.ROLL_ARM + arm, "neutral", (1, -0.2), glasses="up" if d >= 12 else "low", d=d)
        hx, hy = min(o["hands"])
        c = k_.c
        c.save(); c.translate(hx - 1, hy - 4); c.rotate(-0.08)
        s4.rect(k_, -6, -44, 12, 62, s4.BLUE, 995, lw=1.6)
        c.set_source_rgba(0.98, 0.96, 0.86, 0.9); c.rectangle(-6.5, -14, 13, 6); c.fill()
        ellipse(k_, 0, -44, 6, 2.4, (0.30, 0.52, 0.92), 996, shadow=False, lw=1.2)
        c.restore()
        ellipse(k_, hx, hy, 5.0, 5.4, s4.SKIN_PAM, 997, shadow=False, lw=1.2)

    with s4.Strip("edge"), s4.s3.Client(lean=lean, edge=False), s1.Breath(sb, "client", s1.br(d, 0.4)):
        S(k, s4.CAM41, auto=False, portrait=False, pre=pre,
          **base(door=0.6, rb=False, sf=False, dn=False, pm=False, mm=False,
                 cl=at("client", x=cx, face="suspicious", look=(-1, 0.25))))


# ---- 6.3 -------------------------------------------------------------------------------------------------------------

HAND63 = ["grab"]
SLEEVE = (0.33, 0.21, 0.46)                                 # a shade under her jacket's purple: the sleeve reads against it


def _arm_over(k, px, a1, a2):
    """Her screen-right arm over the counter, from her own shoulder: the sleeve a shade darker with an ink edge so it
    separates from her jacket; then her other hand, resting on the counter's edge (both arms in a mid-frame shot)."""
    c = k.c
    cx, cy, z = s6.CAM63
    c.save(); c.translate(270, 480); c.scale(z, z); c.translate(-cx, -cy)
    c.translate(px, s4.PAM_FEET); c.scale(s4.PAM_S, s4.PAM_S)
    dd = lambda a: (math.sin(math.radians(a)), math.cos(math.radians(a)))
    sx_, sy_ = s4.PAM_SH_R
    ex_, ey_ = sx_ + dd(a1)[0] * s4.LN, sy_ + dd(a1)[1] * s4.LN
    wx, wy = ex_ + dd(a1 + a2)[0] * s4.LN, ey_ + dd(a1 + a2)[1] * s4.LN
    for (ax, ay, bx, by), col, hw in (((sx_, sy_, ex_, ey_), SLEEVE, 10.0), ((ex_, ey_, wx, wy), s4.SKIN_PAM, 7.5)):
        an = math.atan2(by - ay, bx - ax); nx, ny = -math.sin(an) * hw, math.cos(an) * hw
        s6.cut(k, [(ax + nx, ay + ny), (bx + nx, by + ny), (bx - nx, by - ny), (ax - nx, ay - ny)], col, shadow=False, lw=2.2)
    ellipse(k, sx_, sy_, 10.5, 10.5, SLEEVE, 996, shadow=False, lw=2.2)               # the shoulder's round, on her side
    ellipse(k, ex_, ey_, 9.5, 9.5, SLEEVE, 997, shadow=False, lw=2.2)
    c.set_source_rgb(0.98, 0.97, 0.94)                                               # the shoved-up cuff
    an = math.atan2(wy - ey_, wx - ex_)
    c.save(); c.translate(ex_ + (wx - ex_) * 0.2, ey_ + (wy - ey_) * 0.2); c.rotate(an)
    c.rectangle(-3, -8, 6, 16); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.6); c.stroke(); c.restore()
    fl = math.hypot(wx - ex_, wy - ey_) or 1.0
    ux, uy = (wx - ex_) / fl, (wy - ey_) / fl
    hp.draw(k, HAND63[0], wx - ux * 10, wy - uy * 10, 17.0, s4.SKIN_PAM, (ux, uy), 1)   # the series' hand on the phone, thumb showing
    c.restore()


def _other_hand(k, px):
    """Her screen-left hand flat on the counter's edge, the sleeve going back under her."""
    c = k.c
    x, y = 196.0, 578.0
    c.set_source_rgb(*SLEEVE)
    c.move_to(x - 34, y - 30); c.line_to(x - 10, y + 2); c.line_to(x + 18, y - 6); c.line_to(x - 4, y - 40); c.close_path()
    c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.4); c.stroke()
    ellipse(k, x + 18, y - 2, 24, 12, s4.SKIN_PAM, 998, shadow=False, lw=2.4)
    c.set_source_rgb(*INK); c.set_line_width(1.6)
    for i in range(3):
        c.move_to(x + 24 + i * 7, y - 10); c.line_to(x + 27 + i * 7, y + 6); c.stroke()


def install():
    s2.SHOTS[[x[0] for x in s2.SHOTS].index("2.1")] = ("2.1", s2.N21, s2_1)
    s4.SHOTS[[x[0] for x in s4.SHOTS].index("4.1")] = ("4.1", s4.N41, s4_1)
    for m in (s2, s4, s6):
        m.V = "v14"
    if not hasattr(s6, '_arm_over_v13'):
        s6._arm_over_v13 = s6._arm_over
    s6._arm_over = _arm_over
    ch.BIG["4.1"].update(palm=1.3, grab=1.3, point=1.3, relax=1.3)                 # one size for her hand through the shot
    ch.STATE["2.1"] = _shapes21
    s1.GLOW_A["2.1"] = 0.15                                                       # its light weak: it read as a glitch over his sleeve (5.1)
    ch._BYFN.clear()
    orig = s6.s6_3 if not hasattr(s6, "_s6_3_v13") else s6._s6_3_v13
    s6._s6_3_v13 = orig

    def s6_3(k, d):
        HAND63[0] = "grab" if 3 <= d < 20 else "quiet"                            # round the phone while she turns and lifts it
        pr = s4.pam_reach
        top = s6._fr2sc((0, 596))[1]                                               # v16: the hand never below the phone's middle:
        s4.pam_reach = lambda x, lean, target, side=-1: pr(x, lean, (target[0], min(target[1], top)), 1)   # no wrist over the edge
        try:
            orig(k, d)
        finally:
            s4.pam_reach = pr
        _other_hand(k, s6.PX63)
    s6_3.__doc__ = orig.__doc__
    s6.SHOTS[[x[0] for x in s6.SHOTS].index("6.3")] = ("6.3", s6.N63, s6_3)
    ch._BYFN.clear()
