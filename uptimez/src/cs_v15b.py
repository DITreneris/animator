"""ONE STAR v15b (25 Nov, Tomas's review of 0:26-0:30: "OK idea, FAIL animation"). Keep the plan's geometry, its
colours, 99% CONFIDENT and the camera; fix the hand, the paper and the pauses, and give the Client a progression.
  3.3   Don proud of it: a smug, half-lidded smirk between the words; the series' hands gripping the sheet's corners.
  3.4   REVEAL, no hand (0.5 s); the Client's hand (palm, thumb, three fingers curled, the index out: hands2's point,
        cuff and sleeve from the bottom edge) taps COURT A, then COURT B, each a small press and a pause, the wrist
        leading; it goes back down; then the clean plan, held, easing in on 99% CONFIDENT.
  3.4b  (new, 0.83 s) the Client with the sheet in both hands: he does not get it (looking down, plain), he gets it
        (dawning), he looks up at Don.
  3.5   the crumple and the ball are paper: facets in three blues, white grid scraps and edges, a shadow side.
install() after cs_film_v14.setup(), before cs_say.install()."""
import math
import cs_scene1 as s1
import cs_scene3 as s3
import cs_v14 as V
import cs_v14_gags as g
import cs_hands as ch
import hands2
import kit
from cs_scene1 import S, at, base, sb, ellipse
from kit import INK

DPS = 12


def ease(u):
    return s1.ease(u)


def lerp(a, b, u):
    return tuple(x + (y - x) * u for x, y in zip(a, b))


# ---- 3.3 -------------------------------------------------------------------------------------------------------------

def s3_3(k, d):
    """17 drawings. Don unrolls the AI's sheet to the Client: "Recovered."; between the words and after, the smug,
    half-lidded smirk of a man who thinks he has saved the day."""
    t = d / float(DPS)
    talk = 0.0
    if s3.LINE33[0] <= t <= s3.LINE33[1]:
        talk = (1.0, 0.5, 1.0, 0.0)[int((t - s3.LINE33[0]) * DPS / 2) % 4]
    U = ease(d / 5.0)
    g.REC.clear()

    def ex(k_, o):
        (lx, ly), (rx, ry) = o["don"]["hands"]
        top = min(ly, ry) - 4
        w = abs(rx - lx) + 30
        h = 20 + 100 * U
        cx = (lx + rx) / 2
        s3.ai_sheet(k_, cx, top, w, 120, 0.0, show=h / 120.0)
        if U < 1:
            ellipse(k_, cx, top + h, w / 2 + 2, 5, (0.16, 0.38, 0.78), 993, shadow=False, lw=1.4)
        sk = kit.PEOPLE["DON"]["skin"]
        mine = [i for i, r in enumerate(g.REC) if tuple(round(v, 2) for v in r[3]) == tuple(round(v, 2) for v in sk)]
        for i in mine[-2:]:                                                         # his own hands over the corners
            g.again(k_, i, "grab")

    with s1.A.Don(s1.A.MOUTH, talk), s1.Breath(sb, "don", s1.br(d, 0.0, 0.010)), s3.Client(), s1.Breath(sb, "client", s1.br(d, 0.4)):
        S(k, s3.CAM33, auto=False, portrait="hang", extra=ex,
          **base(rb=False, sf=False, pm=False, mm=False, door=0.0,
                 cl=at("client", x=340, face="plain", look=(1, 0.5)),
                 dn=at("don", x=450, pose=s3.HOLD, face="smug" if talk == 0 else "happy", look=(-1, -0.2))))


# ---- 3.4 -------------------------------------------------------------------------------------------------------------

N34 = 26
COURT_A = (206.0, 676.0)                                    # the plan's two courts (frame, at zoom 1): the tip lands on the
COURT_B = (334.0, 676.0)                                    # circle, above its label
HAND_W = 84.0


def _hand_at(k, tip, press=0.0, lean=0.0):
    """The Client's right hand from the bottom edge: sleeve, cuff, hands2's point (palm, thumb, curled fingers)."""
    tx, ty = tip[0], tip[1] + press
    a = math.radians(12 + lean)                                                    # the forearm leans in from the lower right
    L = 1.55 * HAND_W                                                              # wrist to fingertip
    wx, wy = tx + math.sin(a) * L, ty + math.cos(a) * L
    bx, by = wx + math.sin(a) * 400, wy + math.cos(a) * 400
    hands2.arm(k, bx, by, wx, wy, HAND_W, (0.42, 0.44, 0.24), s3.SKIN_CL, cuff=(0.98, 0.97, 0.94), pose="point", side=1, seed=951)


def s3_4(k, d):
    """26 drawings (2.17 s). d0-5 the plan alone. d6-8 the hand comes up from the bottom; d9 taps COURT A (d10 press);
    d11-13 over to COURT B, the wrist leading; d14 taps; d15-17 it goes back down out of the frame; d18-25 the clean
    plan, easing in on 99% CONFIDENT."""
    c = k.c
    e = ease((d - 18) / 7.0)
    z = 1.12 - 0.12 * ease((d - 1) / 5.0) + 0.30 * e                               # settles, then eases in on the title
    c.save(); c.translate(270, 520 - 230 * e); c.scale(z, z); c.translate(-270, -(520 - 320 * e))
    old = s3.cp.PROPS4[0]; s3.cp.PROPS4[0] = False
    try:
        s3.cp.ai_site(k)
    finally:
        s3.cp.PROPS4[0] = old
    c.set_source_rgb(0.20, 0.45, 0.85); c.rectangle(36, 126, 468, 128); c.fill()
    s3.cp.T(c, "SITE PLAN", 270, 170, 42, col=(1, 1, 1))
    s3.cp.T(c, "RECOVERED BY AI", 270, 208, 29, col=(0.85, 0.92, 1.0))
    s3.cp.T(c, "99% CONFIDENT", 270, 248, 38, col=(1, 0.9, 0.3))
    low = (COURT_A[0] + 40, 1000)
    if 6 <= d <= 17:
        if d <= 8:
            tip = lerp(low, COURT_A, ease((d - 5) / 3.0)); press = 0
        elif d <= 10:
            tip = COURT_A; press = 5 if d == 10 else 0
        elif d <= 13:
            tip = lerp(COURT_A, COURT_B, ease((d - 10) / 3.0)); press = 0
            tip = (tip[0], tip[1] - 14 * math.sin(math.pi * (d - 10) / 3.0))      # up a little between the taps
        elif d <= 14:
            tip = COURT_B; press = 5
        else:
            tip = lerp(COURT_B, (COURT_B[0] + 40, 1040), ease((d - 14) / 3.0)); press = 0
        _hand_at(k, tip, press, lean=4 if d >= 11 else 0)
    c.restore()


# ---- 3.4b -------------------------------------------------------------------------------------------------------------

N34b = 10
CAM34b = (268, 640, 3.2)
HOLD_CL = (25, 100, -25, -100)


def s3_4b(k, d):
    """10 drawings (0.83 s). The Client close, the sheet open in both hands, its back to us (the plan showing through).
    d0-3 he looks down at it, blank; d4-6 it dawns on him; d7-9 his eyes come up to Don (off right)."""
    g.REC.clear()
    face = "plain" if d < 4 else "dawning"
    look = (0.1, 1.0) if d < 7 else (1, -0.1)

    def ex(k_, o):
        (lx, ly), (rx, ry) = o["client"]["hands"]
        c = k_.c
        x0, x1 = min(lx, rx) - 16, max(lx, rx) + 16
        y0, y1 = min(ly, ry) - 10, min(ly, ry) + 120
        c.save()
        kit.rect(k_, x0, y0, x1 - x0, y1 - y0, (0.22, 0.47, 0.86), 987, shadow=True, lw=2.2)
        c.set_source_rgba(1, 1, 1, 0.22); c.set_line_width(1.2)                       # the plan's lines through the paper
        cx = (x0 + x1) / 2
        c.new_path(); c.arc(cx, y0 + 26, 13, 0, 6.3); c.stroke()
        c.rectangle(cx - 6, y0 + 40, 12, 46); c.stroke()
        for sx in (-1, 1):
            c.new_path(); c.arc(cx + sx * 12, y0 + 96, 14, 0, 6.3); c.stroke()
        c.restore()
        sk = s3.SKIN_CL
        mine = [i for i, r in enumerate(g.REC) if tuple(round(v, 2) for v in r[3]) == tuple(round(v, 2) for v in sk)]
        for i in mine[-2:]:
            g.again(k_, i, "grab")

    old = sb.pocket_strip
    sb.pocket_strip = lambda *a_, **kw: None
    try:
        with s3.Client(edge=False), s1.Breath(sb, "client", s1.br(d, 0.4, 0.012)):
            S(k, CAM34b, auto=False, portrait=False, extra=ex,
              **base(rb=False, sf=False, dn=False, pm=False, mm=False, door=0.0,
                     cl=at("client", pose=HOLD_CL, face=face, look=look)))
    finally:
        sb.pocket_strip = old


# ---- the paper ball -------------------------------------------------------------------------------------------------

BLUES = ((0.24, 0.50, 0.90), (0.18, 0.40, 0.80), (0.13, 0.31, 0.66))


def ball(k, x, y, rad, seed=0):
    """A crumpled sheet: an irregular outline, facets in three blues (lit side up-left), white scraps of the grid and
    of the paper's edge, an ink outline."""
    c = k.c
    n = 11
    pts = []
    for i in range(n):
        a = i * 2 * math.pi / n + 0.2
        q = 1.0 + 0.16 * math.sin(i * 2.3 + seed) + 0.08 * math.cos(i * 4.1)
        pts.append((x + math.cos(a) * rad * q, y + math.sin(a) * rad * q * 0.94))
    for i in range(n):                                                             # facets: triangles to an off-centre core
        p0, p1 = pts[i], pts[(i + 1) % n]
        core = (x - rad * 0.12, y - rad * 0.10)
        mid_a = math.atan2((p0[1] + p1[1]) / 2 - y, (p0[0] + p1[0]) / 2 - x)
        lit = math.cos(mid_a + 2.4)                                                # light from the upper left
        col = BLUES[0] if lit > 0.35 else (BLUES[1] if lit > -0.4 else BLUES[2])
        c.new_path(); c.move_to(*core); c.line_to(*p0); c.line_to(*p1); c.close_path()
        c.set_source_rgb(*col); c.fill()
    c.set_source_rgba(1, 1, 1, 0.85); c.set_line_width(max(0.7, rad * 0.07)); c.set_line_cap(1)
    for i in (1, 4, 7):                                                            # scraps of the grid, white
        p = pts[i]
        c.move_to(x + (p[0] - x) * 0.25, y + (p[1] - y) * 0.25); c.line_to(x + (p[0] - x) * 0.7, y + (p[1] - y) * 0.7)
    c.stroke()
    c.set_source_rgb(0.97, 0.98, 1.0)                                              # a white torn edge showing
    c.new_path(); c.move_to(*pts[2]); c.line_to(*pts[3]); c.line_to(x + (pts[3][0] - x) * 0.82, y + (pts[3][1] - y) * 0.82)
    c.close_path(); c.fill()
    c.set_source_rgb(0.08, 0.20, 0.45); c.set_line_width(max(0.6, rad * 0.05))     # the folds
    for i in (0, 3, 6, 9):
        p = pts[i]
        c.move_to(x - rad * 0.12, y - rad * 0.10); c.line_to(x + (p[0] - x) * 0.9, y + (p[1] - y) * 0.9)
    c.stroke()
    c.new_path(); c.move_to(*pts[0])
    for p in pts[1:]:
        c.line_to(*p)
    c.close_path(); c.set_source_rgb(*INK); c.set_line_width(max(1.0, rad * 0.11)); c.set_line_join(1); c.stroke()


# ---- install ------------------------------------------------------------------------------------------------------------

def _set(shots, name, entry):
    shots[[x[0] for x in shots].index(name)] = entry


def install():
    _set(s3.SHOTS, "3.3", ("3.3", s3.N33, s3_3))
    _set(s3.SHOTS, "3.4", ("3.4", N34, s3_4))
    if not any(x[0] == "3.4b" for x in s3.SHOTS):
        i = [x[0] for x in s3.SHOTS].index("3.4") + 1
        s3.SHOTS.insert(i, ("3.4b", N34b, s3_4b))
    s3.N34 = N34
    g._ball = ball
    ch._BYFN.clear()
    import cs_film
    import cs_sfx as fx
    cs_film.FX += [("3.4", 10, fx.tap(180.0), 0.16), ("3.4", 14, fx.tap(180.0), 0.16)]
