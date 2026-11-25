"""ONE STAR v14c (25 Nov, Tomas's picks, /grill-me): the round after v14b.
  4.1   Pam pushes her glasses up with ONE finger at her temple; then the hand goes back out to STOP height and down,
        never across her face (the drop crossed her eyes on one drawing: change the gesture, not its place, 178).
  2.1   the mic is down from the start (sales mode already): no flick, his free hand stays at his side.
  1.2 / 6.2  the post's rating is ONE big gold star and "1/5", the same mark as the flying phone and the robot's visor
        (one story word per screen); the UPDATE keeps it unchanged.
  1.4   +8 drawings: when his arm is home, the robot tosses his phone back; he catches it without looking (so he can
        call from it in 2.1).
  4.2b  Pam's finger aims above his pocket, clear of his hand (two hands close read as a handshake).
  6.6a / 6.6  the loop's answer: the phones buzz again and this time Don clamps his to his chest with both hands, proud;
        at 0:00 it flies out of them again."""
import math
import cs_scene1 as s1
import cs_scene2 as s2
import cs_scene4 as s4
import cs_scene6 as s6
import cs_props as cp
import cs_v14 as V
import cs_v14_hands as H
import cs_v14_gags as g
import cs_scene1_v14 as v14
import cs_hands as ch
import kit
from cs_scene1 import S, at, base, sb, ellipse
from cs_board import X
from kit import INK

DPS = 12


def ease(u):
    return s1.ease(u)


def lerp(a, b, u):
    return tuple(x + (y - x) * u for x, y in zip(a, b))


# ---- 4.1 ---------------------------------------------------------------------------------------------------------------

def s4_1(k, d):
    """24 drawings. STOP palm at him (d2-9); one finger up to her temple, the glasses into her hair (d10-12); the hand
    back out to the STOP place (d13-15) and straight down at her side (d16-19)."""
    px = 96 + (175 - 96) * ease(d / 7.0)
    cx = 318 - (318 - 285) * ease(d / 6.0)
    REST = (8, 0)
    if d < 10:
        st = ease((d - 2) / 3.0)
        arm = lerp(REST, s4.STOP41, st)
        s4.HAND41[0] = "palm" if st > 0.75 else ("grab" if st > 0.2 else "quiet")
    elif d < 13:
        arm = lerp(s4.STOP41, H.GLASS41, ease((d - 10) / 2.0))
        s4.HAND41[0] = "point"
    elif d < 16:
        arm = lerp(H.GLASS41, s4.STOP41, ease((d - 13) / 2.0))
        s4.HAND41[0] = "relax"
    else:                                                                         # down in two drawings, folded: an angle blend
        arm = (10, 40) if d == 16 else REST                                        # from STOP swung the forearm level at him
        s4.HAND41[0] = "quiet"
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
        s1.PH_DEV.append(c.user_to_device(hx, hy))                                # her rig's own hand stays out (two-pass)
        import of_cast as _oc                                                      # v15f: the series' fist round the roll
        _oc.handle_grip(k_, hx - 1, hy - 6, 13.0, -0.08 + math.pi / 2, skin=s4.SKIN_PAM)

    with s4.Strip("edge"), s4.s3.Client(lean=lean, edge=False), s1.Breath(sb, "client", s1.br(d, 0.4)):
        S(k, s4.CAM41, auto=False, portrait=False, pre=pre,
          **base(door=0.6, rb=False, sf=False, dn=False, pm=False, mm=False,
                 cl=at("client", x=cx, face="suspicious", look=(-1, 0.25))))


# ---- 2.1 ---------------------------------------------------------------------------------------------------------------

def s2_1(k, d):
    """26 drawings. The phone held in front of him, the mic at his mouth (sales mode). v15c (Tomas's review: "not just
    panic; he must try desperately to look competent while panicking inside"): a progression, not one level.
    d0-4 the professional: a confident grin, calm eyes. d5- the worry grows: brows up at their inner ends (the right one
    higher), eyes wide; he says the line through a clenched, too-wide grin; his eyes go to the phone, away, back; a big
    drop slides down off his scalp; he sinks a little into his shoulders. After the line: the forced grin, held."""
    from cand_bc import ik
    t = d / float(DPS)
    a1, a2 = ik(s2.SH_R[0], s2.SH_R[1], s2.REST_R[0], s2.REST_R[1], s2.LN, s2.LN, -1)
    talk = 0.0
    if s2.LINE21 <= t <= s2.LINE21 + 1.5:
        talk = (1.0, 0.5, 1.0, 0.2)[int((t - s2.LINE21) * DPS / 2) % 4]
    worry = ease((d - 4) / 5.0)
    face = "neutral" if d < 5 else "shock"
    look = ((1, 0) if d < 9 else (0.2, 0.9) if d < 12 else (-0.9, -0.3) if d < 15 else (1, 0))
    sink = 1.0 - 0.022 * worry

    def back(k_):
        s2.cs_cal.wall(k_, s2.cs_cal.THU, t=d / float(DPS))

    def ex(k_, o):
        (lx, ly), (rx, ry) = o["don"]["hands"]
        hx, hy = (lx, ly) if lx < rx else (rx, ry)
        j = (1.2, -0.8, 0.9, -1.3)[d % 4] * worry                                 # the phone shakes in his hand
        s1.phone_held(k_, hx + j, hy + 0.5 * j, sb.SC["don"], ang=0.22 + 0.03 * j, buzz=False, d=d, seed=941)
        s1.fist(k_, hx + j, hy + 0.5 * j, sb.SC["don"], kit.PEOPLE["DON"]["skin"], 945)
        if d >= 6:
            _sweat(k_, o["don"]["head"], sb.SC["don"], d)

    with _Face(s1.A.MOUTH, talk, worry), s1.Breath(sb, "don", s1.br(d, 0.0, 0.010) * sink):
        u = ease((d - s2.PAN21[0]) / float(s2.PAN21[1] - s2.PAN21[0]))
        cam = tuple(a_ + (b_ - a_) * u for a_, b_ in zip(s2.CAL21, s2.CAM21))
        S(k, cam, auto=False, mic="down", portrait="hang", back=back, extra=ex,
          **base(cl=False, sf=False, pm=False, mm=False, rb=False, door=0.0,
                 dn=at("don", pose=H.PHONE_L + (a1, a2), face=face, look=look)))


class _Face(s1.A.Don):
    """Don's signs (boom, hair) with the forced grin and the worried brows drawn first, in his head's own units."""
    def __init__(self, pts, talk, worry):
        s1.A.Don.__init__(self, pts, 0.0)
        self.say, self.worry = talk, worry

    def __enter__(self):
        s1.A.Don.__enter__(self)
        inner = sb.don_signs
        say, worry = self.say, self.worry

        def signs(k, head, s, mic, hair):
            c = k.c
            hx, hy = head
            c.save(); c.translate(hx, hy); c.scale(s, s); c.set_line_cap(1); c.set_line_join(1)
            skin = s1.A.kit_skin_don()
            ellipse(k, 0, 31, 17, 15, skin, 714, shadow=False, outline=False)              # the face's own mouth covered
            o = 7.0 * say
            c.new_path()                                                                   # the grin: too wide, corners up,
            c.move_to(-18, 22); c.curve_to(-9, 27, 9, 27, 18, 22)                          # teeth clenched; talking, the jaw
            c.curve_to(13, 33 + o, -13, 33 + o, -18, 22); c.close_path()                   # drops a little, teeth still showing
            c.set_source_rgb(0.98, 0.97, 0.94); c.fill_preserve()
            c.set_source_rgb(*INK); c.set_line_width(2.6); c.stroke()
            if o > 0.5:
                c.new_path(); c.move_to(-12, 27.5); c.curve_to(-4, 29 + o * 0.5, 4, 29 + o * 0.5, 12, 27.5)
                c.curve_to(8, 29.5 + o, -8, 29.5 + o, -12, 27.5); c.close_path()
                c.set_source_rgb(0.40, 0.10, 0.10); c.fill()
            c.set_line_width(1.3)
            for x in (-9, -3, 3, 9):                                                       # the teeth
                c.move_to(x, 24.5 + abs(x) * -0.1); c.line_to(x, 26.5); c.stroke()
            if worry > 0.05:                                                               # brows up at their inner ends,
                c.set_source_rgb(0.13, 0.11, 0.12); c.set_line_width(4.4)                  # the right one higher
                lift = 4.0 * worry
                c.move_to(-29, -11); c.line_to(-8, -13 - lift); c.stroke()
                c.move_to(29, -12); c.line_to(8, -15 - 1.4 * lift); c.stroke()
            c.restore()
            inner(k, head, s, mic, hair)
        sb.don_signs = signs
        return self


def _sweat(k, head, s, d):
    """Two drops off his bald scalp, one after the other, running down to the ear and gone; a third flicks off."""
    hx, hy = head
    for i, (ox, oy, ph) in enumerate(((-40, -38, 0), (42, -32, 7), (-46, -14, 13))):
        u = ((d + ph) % 18) / 18.0
        if i == 0:                                                                 # the big one slides all the way, once
            u = min(1.0, (d - 6) / 16.0)
        x = hx + ox * s
        y = hy + (oy + 34 * u) * s
        r = (5.6 if i == 0 else 3.6) * s * (1 - 0.2 * u)
        c = k.c
        c.new_path(); c.move_to(x, y - 2.4 * r); c.curve_to(x + 1.1 * r, y - 0.6 * r, x + r, y + r, x, y + r)
        c.curve_to(x - r, y + r, x - 1.1 * r, y - 0.6 * r, x, y - 2.4 * r); c.close_path()
        c.set_source_rgb(0.62, 0.84, 0.98); c.fill_preserve(); c.set_source_rgb(*kit.INK); c.set_line_width(1.0); c.stroke()


# ---- the rating: one big star -------------------------------------------------------------------------------------------

def _big_rating(c, x, y, n_on, size=34):
    """The post's rating as the film's one story mark: a big gold star and 1/5 (the flying phone and the visor's)."""
    if size != 44 or n_on != 1:
        return _stars_v13(c, x, y, n_on, size)
    v14._star(c, x + 18, y + 6, 46, (1.0, 0.72, 0.10))
    c.set_source_rgb(*kit.INK); c.set_line_width(2.2)
    c.new_path()
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        q = 46 if i % 2 == 0 else 46 * 0.45
        c.line_to(x + 18 + math.cos(a) * q, y + 6 + math.sin(a) * q)
    c.close_path(); c.stroke()
    cp.T(c, "1/5", x + 78, y + 30, 70, col=(0.12, 0.13, 0.17), center=False)


_stars_v13 = cp._stars


# ---- 1.4: the toss back ---------------------------------------------------------------------------------------------------

N14 = 55
TOSS = (4.10, 4.42)                                         # the phone in the air, claw to his hand (s)


def s1_4(k, d):
    t = d / float(DPS)
    if t < TOSS[0]:
        return V.s1_4(k, min(d, 46)) if d < 47 else _toss(k, d)
    return _toss(k, d)


def _toss(k, d):
    """After his arm is home: the robot flicks the phone back, an arc over to his hand, which comes up and closes on
    it without a look (he is still smug, looking off)."""
    from cand_bc import ik
    t = d / float(DPS)
    g.REC.clear()
    u = ease((t - TOSS[0]) / (TOSS[1] - TOSS[0]))
    catch = (V.REST14[0] - 4, V.REST14[1] - 16)
    if t < TOSS[0]:
        hand_t = V._arm14(t)[0]                                                    # still coming home from the visor
    elif t < TOSS[1] + 0.1:
        hand_t = lerp(V.REST14, catch, ease((t - TOSS[0]) / 0.25))
    else:
        hand_t = lerp(catch, V.REST14, ease((t - TOSS[1] - 0.1) / 0.25))
    a1, a2 = ik(V.SH14[0], V.SH14[1], hand_t[0], hand_t[1], g.LN, g.LN, 1)
    held = t >= TOSS[1]

    def ex(k_, o):
        c_ = k_.c
        sx, sy = o["robot"]["screen"]
        rr = 50 * sb.SC["robot"]
        ellipse(k_, sx, sy, 0.80 * rr, 0.62 * rr, (0.06, 0.08, 0.12), 990, shadow=False, lw=1.6)
        c_.set_source_rgb(*cp.GRN); c_.set_line_width(0.12 * rr); c_.set_line_cap(1)
        c_.move_to(sx - 0.3 * rr, sy); c_.line_to(sx - 0.08 * rr, sy + 0.22 * rr); c_.line_to(sx + 0.34 * rr, sy - 0.25 * rr); c_.stroke()
        cx_, cy_ = o["robot"]["hands"][1]
        hx, hy = o["don"]["hands"][0]
        if t < TOSS[0]:
            v14._phone(k_, cx_, cy_ - 10, -0.2, 1.25)
        elif not held:
            px = cx_ + (hx - cx_) * u
            py = cy_ - 10 + (hy - 6 - cy_ + 10) * u - 40 * 4 * u * (1 - u)
            v14._phone(k_, px, py, -0.2 + 6.0 * u, 1.25)
            v14._zz(c_, px, py, math.pi + 0.6)
        else:
            v14._phone(k_, hx, hy - 6, 0.15, 1.25, lit=False)
            g.again(k_, 0, "grab")

    with s1.A.Don(s1.A.UP, 0.0), s1.Breath(sb, "don", s1.br(d)), s1.Breath(sb, "robot", s1.br(d, 0.5, 0.006)):
        rb_arm = ("paddle" if not held else "none") if V.ARM14[0] == "paddle" else "none"
        S(k, s1.TWO14_IN, auto=False, portrait="hang", extra=ex,
          **base(cl=False, sf=False, pm=False, mm=False, door=0.0, rb=at("robot", arm=rb_arm),
                 dn=at("don", x=X["don"] - V.STEP, pose=(a1, a2, 8, 0), face="smug", look=(1, -0.3))))


def _shapes14():
    if s1.CUR_D[0] >= 47:
        t = s1.CUR_D[0] / float(DPS)
        return ["grab" if t >= TOSS[0] else ("point" if t < V.BACK + 0.2 else "quiet"), "quiet"]
    return V._shapes14()


# ---- 6.6a / 6.6: the clutch --------------------------------------------------------------------------------------------

CLUTCH = (25, 100, -25, -100)                                # both hands in front of his chest (3.3's hold)


def _phone_between(k, o, d, buzz):
    """v15f: the phone in his right hand (the series' phone grip, its back to us, the thumb toward his middle), his
    left hand flat over its foot, clamping it to his chest."""
    import of_cast as _oc
    (lx, ly), (rx, ry) = o["don"]["hands"]
    mx, my = (lx + rx) / 2.0, (ly + ry) / 2.0 - 4
    j = (1.5 if d % 2 else -1.5) if buzz else 0.0
    sk = kit.PEOPLE["DON"]["skin"]
    c = k.c
    for hx, hy in ((lx, ly), (rx, ry)):
        s1.PH_DEV.append(c.user_to_device(hx, hy))
    hx_ = o["don"]["head"][0]
    _oc.phone_grip(k, mx + j, my + 10, 0.42, screen=None, ang=0.0, skin=sk, body_x=hx_, back=True)
    _oc.ps_hand(k, "palm", mx - 22, my + 18, 17, sk, d=(0.7, -0.7), arm=-1)        # v15g: flat beside it, not over it
    if buzz:
        v14._buzz(k.c, mx, my - 6, 15, 16, 1.8)


def s6_6a(k, d):
    """14 drawings. His phone buzzes in his hand; this time he clamps it to his chest with both hands, swells, grins,
    eyes shut: nothing is getting away (the answer to 0:00)."""
    p = ease((d - 3) / 3.0)
    pose = lerp(kit.ARM_POSES["phone_r"], CLUTCH, p)
    face = "neutral" if d < 3 else ("grin" if d < 9 else "happy")

    def ex(k_, o):
        if p < 0.5:
            hx, hy = min(o["don"]["hands"], key=lambda q: q[1])
            s1.phone_held(k_, hx, hy, sb.SC["don"], ang=-0.25, buzz=True, d=d, seed=941)
            s1.fist(k_, hx, hy, sb.SC["don"], kit.PEOPLE["DON"]["skin"], 945)
        else:
            _phone_between(k_, o, d, buzz=d < 9)

    with s1.A.Don(s1.A.MOUTH), s1.Breath(sb, "don", s1.br(d) + 0.05 * p):
        S(k, s6.CAM66a, auto=False, mic="down", portrait=False, extra=ex,
          **base(cl=False, sf=False, rb=False, pm=False, mm=False, door=0.0,
                 dn=at("don", pose=pose, face=face, look=(0.1, 1.0))))


def s6_6(k, d):
    """The wide, every phone buzzing in its hand, every head down; Don, eyes shut, his phone clamped to his chest."""
    od, ph, fi = sb.don, s1.phone_held, s1.fist
    got = {}

    def don(k_, x, feet, s, pose="stand", face="neutral", look=(-1, 0)):
        o = od(k_, x, feet, s, CLUTCH, "happy", look)
        got["o"] = o
        return o

    def held(k_, hx, hy, s_, *a_, seed=900, **kw):
        if seed == 941 and "o" in got:
            return _phone_between(k_, {"don": got["o"]}, d, buzz=True)
        return ph(k_, hx, hy, s_, *a_, seed=seed, **kw)

    def fist(k_, hx, hy, s_, skin, seed):
        if seed == 945:
            return
        return fi(k_, hx, hy, s_, skin, seed)
    old = s1.END66[0]; s1.END66[0] = True
    sb.don, s1.phone_held, s1.fist = don, held, fist
    try:
        s1.s1_1_v13(k, d + 6)
    finally:
        sb.don, s1.phone_held, s1.fist = od, ph, fi
        s1.END66[0] = old


# ---- install -------------------------------------------------------------------------------------------------------------

def _set(shots, name, entry):
    shots[[x[0] for x in shots].index(name)] = entry


def install():
    _set(s4.SHOTS, "4.1", ("4.1", s4.N41, s4_1))
    _set(s2.SHOTS, "2.1", ("2.1", s2.N21, s2_1))
    ch.STATE["2.1"] = ("quiet", "quiet")
    cp._stars = _big_rating
    s1.N14 = N14
    _set(s1.SHOTS, "1.4", ("1.4", N14, s1_4))
    ch.STATE["1.4"] = _shapes14
    s4.POCKET = (296.0, 668.0)
    if not hasattr(s1, "s1_1_v13"):
        s1.s1_1_v13 = s1.s1_1                                                       # v13's wide (v14 replaced only the SHOTS entry)
    _set(s6.SHOTS, "6.6a", ("6.6a", s6.N66a, s6_6a))
    _set(s6.SHOTS, "6.6", ("6.6", s6.N66, s6_6))
    s6.V = s4.V = s2.V = "v14"
    ch._BYFN.clear()
    import cs_film
    import cs_sfx as fx
    cs_film.FX = [x for x in cs_film.FX if (x[0], x[1]) not in (("2.1", 10), ("6.6a", 8))]
    cs_film.FX += [("1.4", 48, fx.whoosh(0.25), 0.14), ("1.4", 52, fx.tap(240.0), 0.20), ("6.6a", 4, fx.tap(200.0), 0.22)]
