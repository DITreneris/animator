"""ONE STAR v14, shot 1.1 (25 Nov, Tomas: "the first joke physical, I miss action"): the film opens on Don and the
robot, medium. The buzz throws the phone out of Don's hand, it bounces off the robot's head, the robot catches it and
its visor shows the one star. Then the wide: every head on Don. KEY POSES ONLY (stills for approval, no motion yet).
  python3 cs_scene1_v14.py [out_dir]"""
import math
import sys
import cs_film_v13 as f13
f13.setup()
import cs_scene1 as s1
from cs_scene1 import S, at, base, sb, kit, cp, ellipse, rect, phone_held, fist, INK
from cs_board import impact

CAM = (409, 672, 3.25)                                     # v5 (the review): 18% closer, legs out                                     # Don and the robot, both whole heads, the series' face size
KEYS = {"A": "0.00 BUZZ", "B": "0.20 FLIGHT", "C": "0.45 BONK", "D": "0.85 one star"}


def _rr(c, x, y, w, h, r):
    c.new_path()
    c.arc(x + w - r, y + r, r, -math.pi / 2, 0); c.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    c.arc(x + r, y + h - r, r, math.pi / 2, math.pi); c.arc(x + r, y + r, r, math.pi, 1.5 * math.pi); c.close_path()


def _phone(k, x, y, ang, s=1.0, lit=True, ghost=None):
    """Don's phone in the air, its screen to us (v2, Tomas: "detail the falling phone"). 14 x 24 units like the held one.
    The screen is the post in small: the garage's avatar, ONE gold star of five (the story), two grey lines and the red
    one. A dark edge down one side gives it thickness; ghost (dx, dy, dang): one faint copy behind it, the way it came."""
    c = k.c
    if ghost:
        c.save(); c.translate(x + ghost[0], y + ghost[1]); c.rotate(ang + ghost[2]); c.scale(s, s)
        _rr(c, -7, -12, 14, 24, 2.4); c.set_source_rgba(0.10, 0.11, 0.14, 0.12); c.fill(); c.restore()
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    _rr(c, -6.2, -11.2, 14, 24, 2.4); c.set_source_rgba(0, 0, 0, 0.18); c.fill()            # its shadow on the wall
    _rr(c, -7.9, -12, 14, 24, 2.4); c.set_source_rgb(0.30, 0.32, 0.38); c.fill()            # the edge: its thickness
    _rr(c, -7, -12, 14, 24, 2.4); c.set_source_rgb(*s1.PHONE); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(1.1); c.stroke()
    if lit:                                                                    # v3 (the review): a thinner bezel, the rating first
        _rr(c, -6.0, -10.7, 12.0, 21.4, 1.4); c.set_source_rgb(0.95, 0.96, 1.0); c.fill()
        c.set_source_rgb(0.10, 0.11, 0.14); c.arc(0, -11.35, 0.45, 0, 6.3); c.fill()           # its camera
        c.set_source_rgb(0.80, 0.62, 0.20); c.arc(-4.1, -8.2, 1.3, 0, 6.3); c.fill()           # the garage's avatar
        c.set_source_rgb(0.25, 0.27, 0.33); c.rectangle(-2.1, -8.9, 6.6, 1.4); c.fill()        # 10 GARAGES
        _star(c, -2.9, -3.2, 3.0, (1.0, 0.72, 0.10))                                           # the one star, 20% bigger
        cp.T(c, "1/5", 0.5, -1.8, 3.7, col=(0.12, 0.13, 0.17), center=False)                   # and said in figures
        for i in range(4):                                                                     # the four it didn't get: darker, bigger
            _star(c, -3.6 + i * 2.5, 2.3, 1.07, (0.56, 0.58, 0.64))
        c.set_source_rgb(0.62, 0.64, 0.70); c.rectangle(-4.8, 4.9, 8.4, 1.1); c.fill()
        c.set_source_rgb(*cp.RED); c.rectangle(-4.8, 7.0, 9.0, 1.6); c.fill()                  # "My lawyer will call."
        c.set_source_rgba(1, 1, 1, 0.45); c.move_to(-6.0, -5.0); c.line_to(-1.8, -10.7); c.line_to(0.4, -10.7)
        c.line_to(-6.0, -1.8); c.close_path(); c.fill()                                        # the glint across the glass
    c.restore()


def _star(c, x, y, r, col):
    c.new_path()
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        q = r if i % 2 == 0 else r * 0.45
        c.line_to(x + math.cos(a) * q, y + math.sin(a) * q)
    c.close_path(); c.set_source_rgb(*col); c.fill()


def _whoosh(c, pts):
    c.set_source_rgba(0.15, 0.12, 0.10, 0.55); c.set_line_width(1.4); c.set_line_cap(1)
    for (x0, y0, x1, y1, x2, y2) in pts:
        c.move_to(x0, y0); c.curve_to(x1, y1, x1, y1, x2, y2); c.stroke()


def _zz(c, x, y, r, n=3):
    """Short speed marks behind a thing, r = the angle it came FROM (no path line: that read as a cord)."""
    c.set_source_rgb(0.15, 0.12, 0.10); c.set_line_width(1.0); c.set_line_cap(1)
    for i in range(n):
        a = r + (i - (n - 1) / 2.0) * 0.22
        q = 6 if i == (n - 1) // 2 else 4
        c.move_to(x + math.cos(a) * 17, y + math.sin(a) * 17); c.line_to(x + math.cos(a) * (17 + q), y + math.sin(a) * (17 + q)); c.stroke()


def _buzz(c, x, y, w, h=16, lw=2.2, k_=0.75):
    h, lw = h * k_, lw * k_
    c.set_source_rgb(*cp.RED); c.set_line_width(lw); c.set_line_cap(1)
    for sgn in (-1, 1):
        for off in (0, 6 * k_):
            x0 = x + sgn * (w + off)
            c.move_to(x0, y - h / 2.0)
            for i in range(4):
                c.line_to(x0 + sgn * (3.5 * k_ if i % 2 == 0 else 0), y - h / 2.0 + h / 4.0 * (i + 1))
            c.stroke()


ROBOT = {"A": {}, "B": {}, "C": dict(head_rot=-0.19, head_dx=-5, wobble=-0.05), "D": {}}       # C: the head knocked 11 degrees, the antenna whipping


def key(k, name):
    pose = {"A": kit.ARM_POSES["phone_r"], "B": (-160, -20, 160, 20), "C": (-150, -120, 140, 100), "D": (-8, 0, 8, 0)}[name]
    face = {"A": "caught", "B": "shock", "C": "shock", "D": "neutral"}[name]
    look = {"A": (0.1, 1.0), "B": (-0.9, -0.8), "C": (-1, 0.3), "D": (-1, 0.35)}[name]
    rb = at("robot", arm="paddle" if name == "D" else "none")
    orig = sb.rm.robot

    def rob(*a_, **kw):
        kw.update(ROBOT[name]); return orig(*a_, **kw)

    def ex(k_, o):
        c_ = k_.c
        sx, sy = o["robot"]["screen"]
        rr = 50 * sb.SC["robot"]
        (lx, ly), (rx, ry) = o["don"]["hands"]
        if name == "A":                                                           # frame 0: it is already shaking in his hand
            hx, hy = max((lx, ly), (rx, ry), key=lambda p: -p[1])
            phone_held(k_, hx, hy, sb.SC["don"], ang=-0.32, buzz=False, d=0, seed=941)
            fist(k_, hx, hy, sb.SC["don"], kit.PEOPLE["DON"]["skin"], 945)
            _buzz(c_, hx, hy - 10, 13, 20)
        if name == "B":                                                           # out of his open hands, spinning, clear of both of them
            px, py = sx + 0.25 * rr, sy - rr * 4.9
            _zz(c_, px, py, 0.9)
            _phone(k_, px, py, -0.9, 1.35)
            _buzz(c_, px, py, 17, 14, 1.8)
        if name == "C":                                                           # BONK: on the dome, the head knocked over
            px, py = sx - 2, sy - rr * 1.30
            _zz(c_, px + 4, py - 12, -0.9)
            c_.save(); c_.translate(px, py + 4); c_.scale(0.55, 0.55); impact(c_, 0, 0, 40); c_.restore()
            _phone(k_, px + 2, py - 13, 0.5, 1.35)
        if name == "D":                                                           # in its claw; the visor is the punch line
            hx, hy = o["robot"]["hands"][1]
            _phone(k_, hx, hy - 10, -0.2, 1.25)
            ellipse(k_, sx, sy, 0.86 * rr, 0.68 * rr, (0.06, 0.08, 0.12), 990, shadow=False, lw=1.6)
            _star(c_, sx - 0.36 * rr, sy - 0.02 * rr, 0.44 * rr, (1.0, 0.75, 0.1))
            cp.T(c_, "1/5", sx + 0.08 * rr, sy + 0.20 * rr, 0.52 * rr, col=(0.95, 0.96, 1.0), center=False)

    sb.rm.robot = rob
    try:
        S(k, CAM, auto=False, portrait="hang", extra=ex,
          **base(cl=False, sf=False, pm=False, mm=False, door=0.0, rb=rb, dn=at("don", pose=pose, face=face, look=look)))
    finally:
        sb.rm.robot = orig


# ---- the motion: 16 drawings of the gag (0-1.33 s at 12 a second), then 10 of the wide -------------------------------------

NG, NW = 16, 10
N11 = NG + NW
HEAD = {5: (-0.19, -5, -0.05), 6: (0.09, 2, 0.03), 7: (-0.04, 0, 0.0)}             # the knock, the rebound, settling
STAND = (-8, 0, 8, 0)
UP = (-160, -20, 160, 20)
ONHEAD = (-150, -120, 140, 100)
GEO = {}


def _mix(a, b, t):
    t = s1.ease(t)
    return tuple(x + (y - x) * t for x, y in zip(a, b))


def _geo():
    """Where the phone starts (his hand), lands (the dome) and ends (the claw): measured from the rigs, once."""
    if GEO:
        return GEO
    for nm, arm in (("hand", "none"), ("claw", "paddle")):
        def ex(k_, o, nm=nm):
            if nm == "hand":
                (lx, ly), (rx, ry) = o["don"]["hands"]
                GEO["hand"] = max((lx, ly), (rx, ry), key=lambda p: -p[1])
                GEO["screen"] = o["robot"]["screen"]
            else:
                GEO["claw"] = o["robot"]["hands"][1]
        s1.draw(lambda k, d: S(k, CAM, auto=False, portrait="hang", extra=ex,
                               **base(cl=False, sf=False, pm=False, mm=False, door=0.0, rb=at("robot", arm=arm),
                                      dn=at("don", pose=kit.ARM_POSES["phone_r"]))), 0)
    return GEO


def _arc(p0, p1, t, lift):
    return (p0[0] + (p1[0] - p0[0]) * t, p0[1] + (p1[1] - p0[1]) * t - lift * 4 * t * (1 - t))


def gag(k, d):
    g = _geo()
    rr = 50 * sb.SC["robot"]
    sx0, sy0 = g["screen"]
    dome = (sx0 - 2, sy0 - rr * 1.30 - 13)
    claw = (g["claw"][0], g["claw"][1] - 10)
    hand = (g["hand"][0], g["hand"][1] - 8)
    if d <= 1:
        pose, face, look = kit.ARM_POSES["phone_r"], "caught", (0.1, 1.0)
    elif d <= 4:
        pose, face = UP, "shock"
    elif d <= 10:
        pose, face = _mix(UP, ONHEAD, (d - 4) / 2.0), "shock"
    else:                                                                         # he freezes, hands on his head, mouth shut
        pose, face = ONHEAD, "neutral"
    # the phone
    spin = None
    if d <= 1:
        ph = None
    elif d <= 4:                                                                  # 2, 3, 4: up and over to the robot
        ph = {2: (hand[0] - 56, hand[1] - 60),                                    # out beside his head (never across his face),
              3: ((hand[0] + dome[0]) / 2.0 - 20, sy0 - rr * 5.4),                 # over the top between them,
              4: (dome[0] + 12, dome[1] - 34)}[d]                                 # and down on the robot
        spin = -0.3 - 0.75 * (d - 1)
    elif d == 5:
        ph = dome; spin = 0.35                                                     # the spin is braking
    elif d <= 7:                                                                  # off the dome, up, into the claw
        t = (d - 5) / 3.0
        ph = _arc(dome, claw, t, 26); spin = (0.10, -0.10)[d - 6]                 # near upright: the screen can be read
    else:
        ph = claw; spin = -0.2
    if 2 <= d <= 9:
        look = (max(-1.0, min(1.0, (ph[0] - 430) / 40.0)), max(-1.0, min(1.0, (ph[1] - 640) / 40.0)))
    elif d >= 10:
        look = (-1, 0.35)
    if d == 9:
        look = (-1, 0.35)
    hr = HEAD.get(d)
    arm = "paddle" if d >= 8 else "none"
    orig = sb.rm.robot

    def rob(*a_, **kw):
        if hr:
            kw.update(head_rot=hr[0], head_dx=hr[1], wobble=hr[2])
        if d in (6, 7):                                                           # its arm coming up for the catch
            a_ = list(a_); u = (0.55, 0.9)[d - 6]
            a_[4] = (0.0, 0, 0, (-20, 0), (20 + 130 * u, 24 * u))
        return orig(*a_, **kw)

    def ex(k_, o):
        c_ = k_.c
        sx, sy = o["robot"]["screen"]
        if d <= 1:
            hx, hy = g["hand"]
            j = 1.6 if d % 2 else -1.6
            phone_held(k_, hx + j, hy, sb.SC["don"], ang=-0.32 + 0.05 * j, buzz=False, d=0, seed=941)
            fist(k_, hx, hy, sb.SC["don"], kit.PEOPLE["DON"]["skin"], 945)
            _buzz(c_, hx, hy - 10, 13, 20)
        else:
            if d in (2, 3, 4):
                pv = {2: hand, 3: (hand[0] - 56, hand[1] - 60), 4: ((hand[0] + dome[0]) / 2.0 - 20, sy0 - rr * 5.4)}[d]
                _zz(c_, ph[0], ph[1], math.atan2(pv[1] - ph[1], pv[0] - ph[0]))
            if d == 2:                                                            # torn out of his hand: a burst where it was
                c_.save(); c_.translate(hand[0], hand[1] - 6); c_.scale(0.34, 0.34); impact(c_, 0, 0, 40); c_.restore()
            if d in (2, 3, 4):
                _buzz(c_, ph[0], ph[1], 17, 14, 1.8)
            if d == 5:
                c_.save(); c_.translate(ph[0], ph[1] + 17); c_.scale(0.55, 0.55); impact(c_, 0, 0, 40); c_.restore()
            if d >= 8:
                ellipse(k_, sx, sy, 0.86 * rr, 0.68 * rr, (0.06, 0.08, 0.12), 990, shadow=False, lw=1.6)
            if d >= 9:
                z = 1.3 if d == 9 else 1.0                                       # it pops on, a drawing oversize
                _star(c_, sx - 0.36 * rr, sy - 0.02 * rr, 0.44 * rr * z, (1.0, 0.75, 0.1))
                cp.T(c_, "1/5", sx + 0.08 * rr, sy + 0.20 * rr, 0.52 * rr, col=(0.95, 0.96, 1.0), center=False)
            gh = {2: (8, 9, 0.35), 3: (9, 6, 0.4), 4: (-6, -7, 0.3)}.get(d)                # v3: none after the hit
            _phone(k_, ph[0], ph[1], spin, 1.35 if d <= 7 else 1.25, ghost=gh)
            PH_AT[0] = c_.user_to_device(ph[0], ph[1])

    sb.rm.robot = rob
    sy_d = 0.965 if d == 2 else (1.02 if d == 3 else s1.br(d))                    # the start: down a hair, then up
    try:
        with s1.Breath(sb, "don", sy_d):
            S(k, CAM, auto=False, portrait="hang", extra=ex,
              **base(cl=False, sf=False, pm=False, mm=False, door=0.0, rb=at("robot", arm=arm if d not in (6, 7) else "none"),
                     dn=at("don", pose=pose, face=face, look=look)))
    finally:
        sb.rm.robot = orig


TURNW = {"sofia": 2, "pam": 4, "mom": 5}


def wide(k, d):
    """The wide, v13's 1.1 from its turn: the others' phones buzz, every head comes round to Don, one after another.
    Don's hands are empty; the robot has his phone, the star on its visor."""
    buzz = d <= 6
    lk = {n: ((-1, 0.05) if d >= t else (0.1, 1.0)) for n, t in TURNW.items()}
    got = {}
    rr = 50 * sb.SC["robot"]

    def back(k_):
        import cs_cal
        cs_cal.wall(k_, cs_cal.THU, t=d / 12.0)
        c_ = k_.c
        feet = sb.F + 6
        c_.save(); c_.translate(575, feet); c_.scale(1.0, s1.br(d, 0.3)); c_.translate(-575, -feet)
        got["pam"] = s1.pb.pam(k_, 575, feet, sb.SC["pam"], kit.ARM_POSES["phone_r"], "neutral", lk["pam"], glasses="up")
        c_.restore()
        (lx, ly), (rx, ry) = got["pam"]["hands"]
        phone_held(k_, rx, ry, sb.SC["pam"], ang=-0.2, buzz=buzz, d=d, seed=931)
        fist(k_, rx, ry, sb.SC["pam"], s1.A.SKIN_PAM, 935)

    def ex(k_, o):
        (lx, ly), (rx, ry) = o["sofia"]["hands"]
        hx, hy = max((lx, ly), (rx, ry), key=lambda p: -p[1])
        phone_held(k_, hx, hy, sb.SC["sofia"], ang=-0.15, buzz=buzz, d=d + 951, seed=951)
        fist(k_, hx, hy, sb.SC["sofia"], kit.PEOPLE.get("SOFIA", {}).get("skin", (0.98, 0.84, 0.74)), 955)
        if "mom" in got:
            (lx, ly), (rx, ry) = got["mom"]["hands"]
            hx, hy = max((lx, ly), (rx, ry), key=lambda p: -p[1])
            phone_held(k_, hx, hy, sb.SC["mom"], ang=-0.1, buzz=buzz, d=d + 3, seed=961)
            fist(k_, hx, hy, sb.SC["mom"], kit.PEOPLE.get("MOM", {}).get("skin", (0.95, 0.80, 0.70)), 965)
        sx, sy = o["robot"]["screen"]
        ellipse(k_, sx, sy, 0.86 * rr, 0.68 * rr, (0.06, 0.08, 0.12), 990, shadow=False, lw=1.6)
        _star(k_.c, sx - 0.36 * rr, sy - 0.02 * rr, 0.44 * rr, (1.0, 0.75, 0.1))
        cp.T(k_.c, "1/5", sx + 0.08 * rr, sy + 0.20 * rr, 0.52 * rr, col=(0.95, 0.96, 1.0), center=False)
        hx, hy = o["robot"]["hands"][1]
        _phone(k_, hx, hy - 10, -0.2, 1.25)

    om = sb.mfs.mom

    def mw(*a_, **kw):
        r = om(*a_, **kw); got["mom"] = r; return r
    sb.mfs.mom = mw
    try:
        with s1.Breath(sb, "don", s1.br(d)), s1.Breath(s1.sofia_fs, "sofia", s1.br(d, 0.6)), s1.Breath(sb.mfs, "mom", s1.br(d, 0.15)):
            S(k, s1.WIDE1, auto=False, back=back, extra=ex,
              **base(cl=False, door=0.0, rb=at("robot", arm="paddle"),
                     dn=at("don", pose=ONHEAD, face="neutral", look=(-1, 0.3)),
                     sf=at("sofia", pose="phone_r", face="caught" if d >= TURNW["sofia"] else "smile", look=lk["sofia"]),
                     pm=False, mm=dict(x=650, x4=True, pose="phone_r", face="sweet", look=lk["mom"])))
    finally:
        sb.mfs.mom = om


def s1_1(k, d):
    gag(k, d) if d < NG else wide(k, d - NG)


def strip(out, ds=None, cols=9, tw=240):
    import cairo
    ds = list(range(N11)) if ds is None else ds
    th = tw * 960 // 540
    rows = (len(ds) + cols - 1) // cols
    big = cairo.ImageSurface(cairo.FORMAT_RGB24, tw * cols, (th + 26) * rows)
    cc = cairo.Context(big); cc.set_source_rgb(1, 1, 1); cc.paint()
    for i, d in enumerate(ds):
        sf_ = s1.draw(s1_1, d)
        x, y = (i % cols) * tw, (i // cols) * (th + 26) + 26
        cc.save(); cc.translate(x, y); cc.scale(tw / 540.0, tw / 540.0); cc.set_source_surface(sf_, 0, 0); cc.paint(); cc.restore()
        cc.set_source_rgb(0.8, 0, 0); cc.select_font_face("Inter", 0, 1); cc.set_font_size(16); cc.move_to(x + 6, y - 7); cc.show_text("d%d  %.2f s" % (d, d / 12.0))
    big.write_to_png(out)


def sheet(out):
    import cairo
    W, H = 540 * s1.HI[0], 960 * s1.HI[0]
    tw = 432; th = tw * 960 // 540
    big = cairo.ImageSurface(cairo.FORMAT_RGB24, tw * 4, th + 40)
    cc = cairo.Context(big); cc.set_source_rgb(1, 1, 1); cc.paint()
    for i, n in enumerate("ABCD"):
        s = s1.draw(lambda k, d, n=n: key(k, n), 0)
        cc.save(); cc.translate(i * tw, 40); cc.scale(tw / 540.0, tw / 540.0); cc.set_source_surface(s, 0, 0); cc.paint(); cc.restore()
        cc.set_source_rgb(0.8, 0, 0); cc.select_font_face("Inter", 0, 1); cc.set_font_size(22); cc.move_to(i * tw + 10, 28); cc.show_text("%s  %s" % (n, KEYS[n]))
    big.write_to_png(out)


PH_AT = [None]                                             # the flying phone's place in device px (for the detail sheet)


def phone_sheet(out):
    """The flying phone alone, big; then every drawing of its flight (d2-d8), cropped round it from the film's frames."""
    import cairo
    from PIL import Image, ImageDraw, ImageFont
    def solo(fn, w=420, h=560, z=17):
        sf_ = cairo.ImageSurface(cairo.FORMAT_RGB24, w, h)
        c = cairo.Context(sf_); c.set_source_rgb(*kit.WALL); c.paint()
        c.translate(w / 2, h / 2); c.scale(z, z); fn(kit.Ctx(c, 0), c)
        sf_.write_to_png("/tmp/ha/_solo.png"); return Image.open("/tmp/ha/_solo.png").convert("RGB")
    a = solo(lambda k, c: _phone(k, 0, 0, 0.0))
    def fl(k, c):
        _zz(c, 0, 0, 0.75); _phone(k, 0, 0, -0.9, ghost=(4, 4, 0.3)); _buzz(c, 0, 0, 16, 12, 1.2)
    b = solo(fl, w=540, z=13)
    c270 = solo(lambda k, c: _phone(k, 0, 0, -0.9, 1.35), 120, 120, 3.25 / 2)
    c540 = solo(lambda k, c: _phone(k, 0, 0, -0.9, 1.35), 160, 160, 3.25)
    s1.HI[0] = 2
    crops = []
    for d in range(2, 9):
        sf_ = s1.draw(s1_1, d); sf_.write_to_png("/tmp/ha/_f.png")
        im = Image.open("/tmp/ha/_f.png").convert("RGB")
        x, y = PH_AT[0][0] * 2, PH_AT[0][1] * 2
        crops.append(im.crop((int(x - 170), int(y - 190), int(x + 170), int(y + 190))).resize((255, 285), Image.LANCZOS))
    W = 1900
    sheet = Image.new("RGB", (W, 1010), (255, 255, 255))
    dr = ImageDraw.Draw(sheet)
    try:
        f1 = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-Bold.otf", 24)
    except Exception:
        f1 = ImageFont.load_default()
    red = (200, 0, 0)
    dr.text((20, 12), "ONE STAR v14 \u00b7 the flying phone, v3 (25 Nov)", fill=red, font=f1)
    sheet.paste(a, (20, 60)); dr.text((20, 626), "upright: star + 1/5 first, thinner bezel", fill=red, font=f1)
    sheet.paste(b, (560, 60)); dr.text((560, 626), "in flight: ghost 12%, marks behind it", fill=red, font=f1)
    sheet.paste(c540, (1200, 60)); dr.text((1200, 226), "its size in the 540 film", fill=red, font=f1)
    sheet.paste(c270, (1200, 300)); dr.text((1200, 426), "its size in the feed (270 px)", fill=red, font=f1)
    for i, im in enumerate(crops):
        sheet.paste(im, (20 + i * 267, 700)); dr.text((26 + i * 267, 670), "d%d  %.2f s" % (i + 2, (i + 2) / 12.0), fill=red, font=f1)
    sheet.save(out)


LINE12 = 1.42                                              # the Client's post starts after the star has landed (was 0.58)
SFX = [(3, "whoosh", 0.16), (5, "tap", 0.55), (8, "key", 0.22), (9, "chime", 0.34)]   # (drawing, cs_sfx, gain): out, BONK, the catch, the star


def install():
    """Shot 1.1 becomes the gag and the wide (26 drawings, 2.17 s; was 17, 1.42 s). The scene's own test sound gets the
    effects; the film's mix takes them from SFX (cs_film_v14)."""
    import numpy as np
    import cs_sfx as fx
    s1.N11 = N11
    s1.SHOTS = [("1.1", N11, s1_1)] + [x for x in s1.SHOTS if x[0] != "1.1"]
    f13.LINE12 = LINE12
    s1.V = "v14"

    def sound(total, out):
        """The scene's own test sound: the lines, a short hard buzz (0.05-0.36 s, cut by the flight), the effects, then
        nothing under the star until the Client's post."""
        import json
        import soundfile as sf
        import cs_animatic as an
        meta = json.load(open(s1.TAKES + "/takes.json"))
        a = np.zeros(int((total + 0.3) * s1.SR))
        for key, t0 in s1.schedule():
            x, _ = sf.read("%s/%s.wav" % (s1.TAKES, key))
            p_ = int(t0 * s1.SR); a[p_:p_ + len(x)] += x[:len(a) - p_]
        z = an.buzz(0.31) * 0.8; p_ = int(0.05 * s1.SR); a[p_:p_ + len(z)] += z
        for d, name, g in SFX:
            z = (getattr(fx, name)(220.0) if name == "tap" else getattr(fx, name)()) * g
            p_ = int(d / 12.0 * s1.SR); a[p_:p_ + len(z)] += z[:len(a) - p_]
        sf.write(out, (a / max(1e-9, np.abs(a).max()) * 0.7).astype(np.float32), s1.SR)
        json.dump({"shots": [{"shot": k, "line": {"key": k, "who": meta[k]["who"], "text": meta[k]["text"], "t0": round(t0, 3),
                                                    "t1": round(t0 + meta[k]["len"], 3)}} for k, t0 in s1.schedule()]},
                  open("cs_scene1_timing_%s.json" % s1.V, "w"), indent=1)
    s1.sound = sound


if __name__ == "__main__" and "phone" in sys.argv:
    s1.HI[0] = 1
    phone_sheet("/tmp/ha/os14_phone_detail_v2.png"); sys.exit(0)

if __name__ == "__main__" and "scene" in sys.argv:
    install()
    s1.HI[0] = 1 if "lo" in sys.argv else 2
    s1.main([a for a in sys.argv[1:] if a not in ("scene", "lo")][0])
    sys.exit(0)

if __name__ == "__main__":
    strip((sys.argv[1] if len(sys.argv) > 1 else "/tmp/ha") + "/os14_open_strip_v2.png")
    sheet((sys.argv[1] if len(sys.argv) > 1 else "/tmp/ha") + "/os14_open_keys_v7.png")
