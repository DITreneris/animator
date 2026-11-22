"""OFFICE NOIR 3: the walkers turned to the side, v4 (v1 to v3 pinned). v4 (a second outside review, of sheet v2: "the
bodies do not pass the weight from one leg to the other"; and cold tests 49, 50): from the knees down first. A leg is
as long as the hip is high at UP, so the carrying leg is straight there and bent at DOWN; the heel lands toe up, the
foot is flat while it carries, the heel peels off before the toe; the free leg's knee comes through ahead of the other;
the far leg is another tone, the hips are apart. Don walks as he does in the film: bent over his glass, creeping. Her
late hair is off until the legs read (it tore her edge).
v3 (v1, v2 pinned). v3 (an outside review of v2, 21 Nov: "not a real side
view: the faces stay frontal; the walk is legs waving; arm and leg layers collide; nothing has weight"):
  * the front drawing is TURNED, not narrowed: drawn off to the side and wrapped round an upright cylinder, row by row
    (TURN degrees): the face goes to the side he walks to, the far side shortens, the back of the hood, hat or hair comes
    round; a new outline is drawn round the turned shape, as thick as the limbs';
  * the near arm hangs from the near shoulder on the body's trailing side, the far one from the leading edge, behind;
  * one walk cycle each, with weight: CONTACT, DOWN (the pelvis lowest just after the heel lands), PASSING, UP; an arm
    goes forward with the opposite leg; the shoulders turn a little against the hips;
  * each walks as himself: the Client heavy, leaning in, short hard steps, his gloves late; Don slow, long steps, his
    head still, his coat's hem late; she light and short-stepped, her hair late, the umbrella steady;
The drawings themselves are not changed (Don's hat, her umbrella's size, the Client's face are as they are in the film).
v2 (v1 pinned: drawn from nothing, and Tomas: "very bad profiles, the
proportions are not kept, bad graphics, 1/10").

v2 is not a new drawing of anyone. Each figure is its OWN front drawing (the same head, face, clothes, colours and line),
turned three quarters: the head and body are the front drawing narrowed (Q), its eyes to where it goes; only what has to
change to walk is new, and it is built from the front drawing's own parts and measures: two legs seen from the side with
a knee (the front's trousers, tights, shoes), and two arms from one shoulder, the far one behind the body, the near one
over it (the front's own sleeve, glove and hand code).

  client(k, x, feet, s, dir_, cig, folder, face)
  don(k, x, feet, s, dir_, bent)
  her(k, x, feet, s, dir_)
x is where they are on the ground: the step is taken from it (no sliding). Each returns {"head": (x, y)}; the Client
also "tip" (the end of his cigarette)."""
import math
import contextlib
import cairo
import numpy as np
from scipy import ndimage
import kit
from kit import cut, ellipse, INK, Ctx
import client_on3 as b
import noir2_cast as n2
import motion_on3 as mo
import sofia_ob as sob
import sofia_v4 as sf
import sofia_bc as sbc

TAU = 2 * math.pi
Q = 0.70                                                     # how narrow the front drawing is when it is turned
d = n2.d


def stride(u, a, up):
    """One foot through a step. Returns (ahead, lift, pitch). On the ground (the first half) it goes back under him: it
    lands on the heel, toe up, is flat while it carries, and the heel peels off before the toe. In the air it swings
    through, toe down first, toe up before it lands."""
    u = u % 1.0
    if u < 0.5:
        if u < 0.07:
            p = -0.42 * (1 - u / 0.07)
        elif u < 0.30:
            p = 0.0
        else:
            p = 0.62 * ((u - 0.30) / 0.20) ** 1.3
        return a * (1 - 4 * u), 0.0, p
    q = (u - 0.5) / 0.5
    e = q * q * (3 - 2 * q)
    return -a + 2 * a * e, up * math.sin(math.pi * q) ** 0.8, 0.62 - 1.04 * q ** 0.7


def _ankle(hipx, f, ah, toe, heel):
    """Where the ankle is (x, y; y up is negative) for a foot f whose sole is ah under the ankle: the lowest part of the
    turned foot is on the ground (plus its lift), so a heel that peels off raises the ankle."""
    extra = toe * math.sin(f[2]) if f[2] > 0 else heel * math.sin(-f[2])
    return hipx + f[0], -(f[1] + extra) - ah


def _walk(x, s, dir_, a, up, rise):
    u = x / (4.0 * a * s) * dir_
    return u, stride(u, a, up), stride(u + 0.5, a, up), -rise * abs(math.sin(TAU * u)), math.sin(TAU * u)


def _knee(hip, foot, l1, l2):
    dx, dy = foot[0] - hip[0], foot[1] - hip[1]
    dd = max(1.0, min(math.hypot(dx, dy), l1 + l2 - 0.5))
    a0 = math.atan2(dy, dx)
    a1 = math.acos(max(-1.0, min(1.0, (l1 * l1 + dd * dd - l2 * l2) / (2 * l1 * dd))))
    return hip[0] + l1 * math.cos(a0 - a1), hip[1] + l1 * math.sin(a0 - a1)      # the knee, bent forward


def _board(k, p0, p1, w0, w1, col, lw=2.2):
    """A cut-out limb: a paper board from p0 to p1, as the front drawings' trouser legs are."""
    g = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    nx, ny = -math.sin(g), math.cos(g)
    cut(k, [(p0[0] + nx * w0 / 2, p0[1] + ny * w0 / 2), (p1[0] + nx * w1 / 2, p1[1] + ny * w1 / 2),
            (p1[0] - nx * w1 / 2, p1[1] - ny * w1 / 2), (p0[0] - nx * w0 / 2, p0[1] - ny * w0 / 2)], col, shadow=False, lw=lw)


def _leg(k, hip, f, w, col, ll, ah=20, toe=30, heel=12, seam=None, taper=(0.92, 0.84)):
    """hip to knee to ankle; returns the ankle. ll: the length of thigh and of shin. The knee is a round of the same
    cloth, so the two boards read as one leg."""
    c = k.c
    ank = _ankle(hip[0], f, ah, toe, heel)
    kn = _knee(hip, ank, ll, ll)
    _board(k, hip, kn, w, w * taper[0], col)
    _board(k, kn, ank, w * taper[0], w * taper[1], col)
    c.new_path(); c.arc(kn[0], kn[1], w * taper[0] * 0.47, 0, TAU); c.set_source_rgb(*col); c.fill()
    if seam:
        c.set_source_rgb(*seam); c.set_line_width(2.0); c.set_line_cap(1)
        c.new_path(); c.move_to(*hip); c.line_to(*kn); c.line_to(*ank); c.stroke(); c.set_line_cap(0)
    return ank


@contextlib.contextmanager
def _swap(*triples):
    old = [(o, n, getattr(o, n)) for o, n, _ in triples]
    for o, n, v in triples:
        setattr(o, n, v)
    try:
        yield
    finally:
        for o, n, v in old:
            setattr(o, n, v)


TURN = 31.0                                                  # degrees the front drawing is turned from facing us
NARROW = 0.80                                                # and how much narrower it is drawn (a body is less deep than wide)


def _cycle(x, s, dir_, a, up, drop):
    """Where he is in his step, from where he stands. Returns u, near foot, far foot, pelvis (down +), swing (near leg
    ahead +1 .. behind -1)."""
    u = x / (4.0 * a * s) * dir_
    return u, stride(u, a, up), stride(u + 0.5, a, up), drop * math.cos(2 * TAU * (u - 0.09)), math.cos(TAU * u)


def turned(k, x, feet, s, dir_, box, draw, turn=None, lean=0.0, rows=None, pre=None):
    """draw(k2) draws the front figure standing at (x, feet). It is drawn aside, then each row of it is wrapped round a
    cylinder about the figure's axis and turned; a new outline goes round it. box: (left, top, right, bottom) in the
    figure's units about its feet. rows(yu) -> a sideways shift in units for the row yu units above the feet (a late
    hem). pre(arr, to_units): changes the front picture before it is turned (late hair). Returns what draw returned."""
    c = k.c
    M = c.get_matrix()
    px = abs(M.xx) * s                                       # one figure unit in pixels
    ax, fy = c.user_to_device(x, feet)
    x0, y0 = int(math.floor(ax + box[0] * px)) - 6, int(math.floor(fy + box[1] * px)) - 6
    w, h = int(math.ceil((box[2] - box[0]) * px)) + 12, int(math.ceil((box[3] - box[1]) * px)) + 12
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h); surf.set_device_offset(-x0, -y0)
    c2 = cairo.Context(surf); c2.set_matrix(M)
    shot = mo.CLOCK["shot"]; mo.CLOCK["shot"] = None         # the plain figure: this picture is not the one on the screen
    try:
        o = draw(Ctx(c2, k.boil))
    finally:
        mo.CLOCK["shot"] = shot
    surf.flush()
    A = np.ndarray((h, w, 4), np.uint8, surf.get_data(), 0, (surf.get_stride(), 4, 1)).astype(np.float32)
    axl = ax - x0
    if pre:
        pre(A, axl, fy - y0, px)
    al = A[:, :, 3] > 24
    cols = np.arange(w, dtype=np.float32)
    any_ = al.any(axis=1)
    left = np.where(any_, np.argmax(al, axis=1), axl); right = np.where(any_, w - 1 - np.argmax(al[:, ::-1], axis=1), axl)
    R = np.maximum(np.maximum(axl - left, right - axl), 1.0)
    R = np.maximum(R, ndimage.median_filter(R, size=max(3, int(7 * px) | 1)))
    R = np.maximum(R, ndimage.gaussian_filter1d(R, 2.5 * px))[:, None]      # a notch or a point a few rows high does not turn on its own (a torn edge)
    e = 4.2 * px + 1.0                                       # the front drawing's own edge line is left behind
    th = math.radians(TURN if turn is None else turn) * dir_
    shift = np.zeros((h, 1), np.float32)
    if rows:
        shift[:, 0] = [rows((fy - y0 - r) / px) * px * dir_ for r in range(h)]
    t = (cols[None, :] - axl - shift) / (R * NARROW)
    inside = np.abs(t) <= 1.0
    ph = np.arcsin(np.clip(t, -1, 1)) - th
    back = (ph < -math.pi / 2) | (ph > math.pi / 2)          # past the edge: the back of him
    st = np.sin(np.clip(ph, -math.pi / 2, math.pi / 2))
    sx = np.clip(axl + st * np.maximum(R - e, 0.5), 0, w - 1.001)
    i0 = np.floor(sx).astype(np.int64); fr = (sx - i0)[:, :, None]
    rr = np.arange(h)[:, None]
    out = A[rr, i0] * (1 - fr) + A[rr, i0 + 1] * fr
    # the back is plain: the colour he has just inside that edge, row by row, evened out down the figure (a mirrored
    # or stretched edge made hatching and smears)
    band = max(3, int(7 * px))
    ecol = np.zeros((h, 4), np.float32)
    for r in range(h):
        if any_[r]:
            xe = int(round(axl - math.copysign(max(R[r, 0] - e - 1, 0), th)))
            seg = A[r, max(0, min(xe, xe + int(math.copysign(band, th)))):max(xe, xe + int(math.copysign(band, th))) + 1]
            seg = seg[seg[:, 3] > 250]
            if len(seg):
                ecol[r] = np.median(seg, axis=0)
    okr = ecol[:, 3] > 0
    if okr.any():
        wgt = ndimage.gaussian_filter1d(okr.astype(np.float32), 5 * px) + 1e-6
        ecol = ndimage.gaussian_filter1d(ecol * okr[:, None], 5 * px, axis=0) / wgt[:, None]
        ecol[:, 3] = 255.0
        hit = back & inside & (out[:, :, 3] > 128)
        out[hit] = np.broadcast_to(ecol[:, None, :], out.shape)[hit]
    out *= (inside & any_[:, None])[:, :, None]
    a = out[:, :, 3]
    hard = a > 128                                           # a paper edge, not a soft one
    out *= hard[:, :, None]; a[...] = np.where(hard, 255.0, 0.0)
    lw = max(1.0, 1.15 * px)
    r_ = int(math.ceil(lw)); yy, xx = np.mgrid[-r_:r_ + 1, -r_:r_ + 1]
    grown = ndimage.maximum_filter(a, footprint=(xx * xx + yy * yy) <= lw * lw + 0.5)
    ink = np.zeros_like(out); ink[:, :, 3] = grown
    ink[:, :, 0] = INK[2] * grown; ink[:, :, 1] = INK[1] * grown; ink[:, :, 2] = INK[0] * grown
    k_ = (a / 255.0)[:, :, None]
    res = np.clip(out + ink * (1 - k_), 0, 255).astype(np.uint8)
    img = cairo.ImageSurface.create_for_data(bytearray(res.tobytes()), cairo.FORMAT_ARGB32, w, h, w * 4)
    c.save(); c.identity_matrix()
    if lean:
        c.translate(ax, fy); c.rotate(lean * dir_); c.translate(-ax, -fy)
    c.set_source_surface(img, x0, y0); c.paint(); c.restore()
    return o


def _turn_x(xu, r, turn=None, dir_=1):
    r = r * 1.0
    """Where a point xu units from the axis on the front drawing (on a row r units half-wide) is after the turn."""
    th = math.radians(TURN if turn is None else turn)
    return math.sin(math.asin(max(-1.0, min(1.0, xu * dir_ / r))) + th) * r * NARROW


# ---- the Client: heavy, leaning in, short hard steps; his gloves late ------------------------------------------------
def _trainer(k, ank, pitch):
    c = k.c
    c.save(); c.translate(ank[0], ank[1] + 20); c.rotate(pitch)
    ellipse(k, 9, -3, 33, 7, b.SOLE, 31, shadow=False, lw=2)
    ellipse(k, 7, -11, 31, 12, b.TRAINER, 32, shadow=False, lw=2)
    c.restore()


def _client_leg(k, hip, f, col, ll):
    ank = _leg(k, hip, f, 48, col, ll, ah=20, toe=38, heel=22, seam=b.CHAR_LINE)
    cut(k, [(ank[0] - 21, ank[1] - 8), (ank[0] + 21, ank[1] - 8), (ank[0] + 20, ank[1] + 7), (ank[0] - 20, ank[1] + 7)], b.CHAR_DARK, shadow=False, lw=1.8)   # the cuff
    _trainer(k, ank, f[2])


def _client_arm(k, sx, sy, u, f, seed, shoulder=True):
    """The front drawing's own arm (the same limb, shoulder and glove), hung from a shoulder."""
    hx, hy = b.limb(k, sx, sy, u, f, b.LN1, b.LN2, 50, 43, b.CHAR, b.CHAR, b.CHAR, 4, seed)
    if shoulder:
        ellipse(k, sx, sy - 1, 24, 21, b.CHAR, seed + 4, shadow=False, lw=2)
    ex, ey = sx + b._d(u)[0] * b.LN1, sy + b._d(u)[1] * b.LN1
    ux, uy = (hx - ex) / b.LN2, (hy - ey) / b.LN2
    b._glove(k, hx, hy, ux, uy, 1, seed + 60)
    return hx, hy


def _no_shoulder(orig):
    def e(k, x, y, rx, ry, *a, **kw):
        if (rx, ry) == (24, 21):
            return None
        return orig(k, x, y, rx, ry, *a, **kw)
    return e


def client(k, x, feet, s=1.0, dir_=1, cig=False, folder=False, face="hard"):
    drop = 11.0
    u, f0, f1, yb, sw = _cycle(x, s, dir_, 40.0, 30.0, drop)
    c = k.c
    lean = 0.075                                                                            # into it
    late = math.cos(TAU * (u - 0.10))                                                       # his gloves, a tenth of a step behind his arms
    hip = (0, b.HIP - 8 + yb)
    ll = (-(b.HIP - 8) + drop - 20) / 2.0                                                    # straight when he is highest
    sy = b.BT + 34

    def unit(tilt=False):
        c.save(); c.translate(x, feet); c.scale(s * dir_, s)
        if tilt:
            c.translate(0, yb); c.rotate(lean)

    unit()
    _client_leg(k, (hip[0] + 4, hip[1]), f1, tuple(v * 0.66 for v in b.CHAR), ll)          # the far leg: darker, so the two are told apart
    c.restore()
    unit(True)
    _client_arm(k, 84, sy - 6, 18 * sw + 10, 62 + 10 * late, 911, shoulder=False)                # the far arm: from the leading edge, behind him
    c.restore()
    unit(); _client_leg(k, (hip[0] - 4, hip[1]), f0, b.CHAR, ll); c.restore()

    def front(k2):
        with _swap((b, "limb", lambda k_, sx, sy_, a1, a2, *a, **kw: (sx, sy_ + 150)), (b, "_glove", lambda *a, **kw: None),
                   (b, "_lower_street", lambda *a, **kw: None), (b, "ellipse", _no_shoulder(b.ellipse))):
            return b.boxer(k2, x, feet + yb * s, s, "b_walk", face, (0.75 * dir_, 0.0), outfit="street", cig=cig)

    o = turned(k, x, feet + yb * s, s, dir_, (-130, -500, 130, -150), front, turn=TURN - 4.0 * sw, lean=lean)     # his shoulders against his hips
    hx_ = _turn_x(-4, 74) * dir_
    head = c.user_to_device(x + hx_ * s, feet + (yb + b.HY) * s)
    tip = c.user_to_device(x + dir_ * 78 * s, feet + (yb + b.HY + 52) * s)
    unit(True)
    if folder:                                                                              # the folder, clamped under his near arm
        c.save(); c.translate(-30, b.BT + 100); c.rotate(-0.14); cut(k, [(-34, -24), (36, -24), (36, 26), (-34, 26)], b.IVORY, shadow=False, lw=2); c.restore()
        _client_arm(k, -46, sy, 6, 74, 913, shoulder=False)
    else:
        _client_arm(k, -46, sy, -18 * sw + 10, 62 - 10 * late, 913, shoulder=False)                # the near arm: back when the near leg is forward; his gloves up at his belt, not at his knees                          # the near arm: back when the near leg is forward
    c.restore()
    return {"head": c.device_to_user(*head), "tip": c.device_to_user(*tip)}


# ---- Don: slow, long steps, his head still; his coat's hem late -------------------------------------------------------
def _don_arm(k, sx, sy, u, f, glass=False):
    """mo._sleeves' sleeve, cuff and hand, one arm from one shoulder."""
    c = k.c
    dd = lambda g: (math.sin(math.radians(g)), math.cos(math.radians(g)))
    ln = 48
    ex, ey = sx + dd(u)[0] * ln, sy + dd(u)[1] * ln
    hx, hy = ex + dd(u + f)[0] * ln, ey + dd(u + f)[1] * ln
    qx, qy = hx - dd(u + f)[0] * 9, hy - dd(u + f)[1] * 9
    if glass:
        n2.magnifier(k, hx, hy, 1.0, math.radians(100 - (u + f) * 0.2))
    for w, colr in ((23, INK), (19, d.TRENCH)):
        c.set_source_rgb(*colr); c.set_line_width(w); c.set_line_cap(0 if colr == INK else 1); c.set_line_join(1)
        c.new_path(); c.move_to(sx, sy - (2 if colr == INK else 0)); c.curve_to(ex, ey, ex, ey, qx, qy); c.stroke()
    c.set_line_cap(0)
    for w, colr in ((23, INK), (19, d.TRENCH_SHADE)):                                       # the cuff
        c.set_source_rgb(*colr); c.set_line_width(w)
        c.new_path(); c.move_to(qx - dd(u + f)[0] * (2 if colr == INK else 0), qy - dd(u + f)[1] * (2 if colr == INK else 0))
        c.line_to(qx + dd(u + f)[0] * 6, qy + dd(u + f)[1] * 6); c.stroke()
    ang = math.atan2(dd(u + f)[1], dd(u + f)[0])
    c.save(); c.translate(hx, hy); c.rotate(ang)
    c.new_path(); c.move_to(-8, -8); c.curve_to(2, -11, 13, -9, 15, -3); c.curve_to(16, 4, 10, 9, 0, 9); c.line_to(-8, 8); c.close_path()
    c.set_source_rgb(*d.SKIN); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2); c.stroke()
    c.restore()
    return hx, hy


def _don_leg(k, hip, f, col, ll):
    c = k.c
    ank = _leg(k, hip, f, 28, col, ll, ah=10, toe=28, heel=14, taper=(0.96, 0.92))
    c.save(); c.translate(ank[0], ank[1] + 10); c.rotate(f[2])
    cut(k, [(-14, -13), (10, -13), (28, -5), (28, 0), (-14, 0)], mo.SHOE, shadow=False, lw=1.8)      # the front drawing's walking shoe
    c.restore()


def don(k, x, feet, s=1.0, dir_=1, bent=0.0):
    drop = 5.0 - 1.5 * bent
    crouch = 12.0 * bent                                                                    # creeping: his knees never straighten
    u, f0, f1, yb, sw = _cycle(x, s, dir_, 38.0 - 12.0 * bent, 14.0 + 4.0 * bent, drop)
    yb += crouch
    c = k.c
    hip = (0, d.HEM - 46 + yb)
    ll = (-(d.HEM - 46) + drop - 10) / 2.0
    lean = math.radians(-1.5 + 11.5 * bent)                                                 # he leans back a little; over his glass, forward
    hem = math.cos(2 * TAU * (u - 0.21))                                                    # his hem: kicked forward by each knee, an eighth of a step late
    sy = d.BT + 24

    def unit(tilt=True):
        c.save(); c.translate(x, feet); c.scale(s * dir_, s)
        if tilt:
            c.translate(0, yb); c.rotate(lean)

    unit(False)
    _don_leg(k, (hip[0] + 3, hip[1]), f1, tuple(v * 0.66 for v in mo.TROUSERS), ll)
    _don_leg(k, (hip[0] - 3, hip[1]), f0, mo.TROUSERS, ll)
    c.restore()
    unit(); _don_arm(k, 42, sy - 4, 15 * sw * (1 - bent) + 4, 16); c.restore()                  # the far arm, from the leading edge, behind his coat

    def front(k2):
        c2 = k2.c
        c2.save(); c2.translate(x, feet + yb * s); c2.scale(s, s)                           # only his coat's width below the collar: the shirt arms under the front drawing's sleeves stay out
        c2.new_path(); c2.rectangle(-300, -900, 600, 900 + d.BT - 2); c2.move_to(-47, d.BT - 2); c2.line_to(47, d.BT - 2); c2.line_to(57, d.HEM + 2); c2.line_to(-57, d.HEM + 2); c2.close_path()
        c2.restore(); c2.clip()
        with _swap((mo, "_legs", lambda *a, **kw: None), (mo, "_sleeves", lambda k_, pose, col, seed, cuff=None: [(0, 0), (0, 0)])):
            return mo.don(k2, x, feet + yb * s, s, "look", "squint", (0.75 * dir_, 0.5 * bent), lean=0.0, glass=False)

    belt = -(d.BT + 127)
    o = turned(k, x, feet + yb * s, s, dir_, (-90, -430, 90, -40), front, lean=lean,
               rows=lambda yu: 4.0 * hem * max(0.0, min(1.0, (belt - yu) / (belt + d.HEM))) ** 1.3)
    hx_ = _turn_x(0, 44) * dir_
    head = c.user_to_device(x + hx_ * s * 0.2, feet + (yb + d.HY) * s)
    unit()
    if bent > 0.5:
        _don_arm(k, -22, sy, 52, 30, glass=True)                                            # his glass, held out low
    else:
        _don_arm(k, -22, sy, -15 * sw + 4, 16)
    c.restore()
    return {"head": c.device_to_user(*head)}


# ---- the woman under the umbrella: light, short steps; her hair late, the umbrella steady ------------------------------
def _her_leg(k, hip, f, col, ll):
    c = k.c
    ank = _leg(k, hip, f, 17, col, ll, ah=22, toe=17, heel=8, taper=(0.9, 0.74))
    c.save(); c.translate(ank[0], ank[1] + 22); c.rotate(f[2] * 0.8)
    cut(k, [(-8, -28), (8, -28), (17, -3), (17, 0), (-6, 0), (-8, -6)], mo.BOOT, shadow=False, lw=1.6)   # the front drawing's boot
    c.restore()


def her(k, x, feet, s=1.0, dir_=-1):
    drop = 5.0
    u, f0, f1, yb, sw = _cycle(x, s, dir_, 25.0, 19.0, drop)
    c = k.c
    hip = (0, mo.HEM_HER - 40 + yb)
    ll = (-(mo.HEM_HER - 40) + drop - 22) / 2.0
    col = [sbc.BLAZER]
    sway = math.cos(2 * TAU * (u - 0.17))                                                   # her hair: behind her body's rise and fall
    sy = sob.BODY_TOP + 16 + yb

    def unit():
        c.save(); c.translate(x, feet); c.scale(s * dir_, s)

    def arm(sx, a1, a2, seed):
        with _swap((sf, "BLOUSE", col[0])):
            return sf._arm(k, sx, sy, a1, a2, seed, w=15)

    unit()
    _her_leg(k, (hip[0] + 3, hip[1]), f1, tuple(min(1.0, v * 2.4) for v in mo.TIGHTS), ll)
    _her_leg(k, (hip[0] - 3, hip[1]), f0, mo.TIGHTS, ll)
    arm(16, 16 * sw + 2, 10, 21)                                                            # the far arm swings
    c.restore()

    def no_arm(k_, sx, sy_, a1, a2, seed, ln=48, w=17):
        col[0] = sf.BLOUSE
        return sx, sy_ + 90

    def front(k2):
        c2 = k2.c
        c2.save(); c2.rectangle(x - 400, feet - 4000, 800, 4000 + (mo.HEM_HER + 2 + yb) * s); c2.clip()     # her own front drawing, down to her hem
        with _swap((sf, "_arm", no_arm)):
            o_ = sob.sofia(k2, x, feet + yb * s, s, "low", "smile", (0.8 * dir_, 0.15), badge=False, tablet_kind=None)
        c2.restore()
        return o_

    def hair(A, axl, fy, px):
        """The two falls of hair beside her body, below her chin: their outer edges swing, late; the body does not."""
        h_, w_ = A.shape[:2]
        top, bot = fy + (sob.HY + 34) * px, fy + (mo.HEM_HER - 30) * px
        inner = 44 * px
        for r in range(max(0, int(top)), min(h_, int(bot))):
            g = ((r - top) / max(1.0, bot - top)) ** 1.2 * 9.0 * px * sway
            if abs(g) < 0.3:
                continue
            row = A[r].copy(); xs = np.arange(w_, dtype=np.float32)
            for sg in (-1, 1):
                edge = axl + sg * inner
                sel = (xs - edge) * sg > 0
                span = max(8.0, (w_ - 1 - edge) if sg > 0 else edge)
                far_ = np.abs(xs[sel] - edge) / span                         # 0 at the body, 1 out at the picture's edge
                src = np.clip(xs[sel] - g * np.minimum(1.0, far_ * 4.0), 0, w_ - 1.001)
                i0 = np.floor(src).astype(int); fr = (src - i0)[:, None]
                A[r, sel] = row[i0] * (1 - fr) + row[i0 + 1] * fr

    o = turned(k, x, feet + yb * s, s, dir_, (-110, -420, 110, -80), front, turn=TURN - 3.0 * sw)
    hx_ = _turn_x(0, 60) * dir_
    head = c.user_to_device(x + hx_ * s * 0.3, feet + (yb + sob.HY) * s)
    unit()
    hx, hy = arm(-26, -34, -152, 23)                                                        # the near arm, its elbow back, the handle at her shoulder: her hand, the handle and the umbrella are one thing, and steady
    c.save(); c.translate(hx, hy); c.rotate(0.02 * math.cos(2 * TAU * (u - 0.2))); c.translate(-hx, -hy)
    c.set_source_rgb(0.10, 0.10, 0.12); c.set_line_width(4); c.move_to(hx, hy + 12); c.line_to(hx - 4, hy - 250); c.stroke()
    c.new_path(); c.move_to(hx - 124, hy - 236); c.curve_to(hx - 98, hy - 330, hx + 90, hy - 330, hx + 116, hy - 236)
    for i in range(4):
        x0 = hx + 116 - 60 * i; c.curve_to(x0 - 10, hy - 250, x0 - 50, hy - 250, x0 - 60, hy - 236)
    c.close_path(); c.set_source_rgb(0.08, 0.08, 0.10); c.fill_preserve(); c.set_source_rgb(0.02, 0.02, 0.03); c.set_line_width(3); c.stroke()
    c.restore()
    ellipse(k, hx, hy, 9, 9, sob.SKIN, 64, shadow=False, lw=2)
    c.restore()
    return {"head": c.device_to_user(*head)}


def turn(c, x, p):
    """Call before drawing a figure standing at x: narrowed as it turns (p 0 = as drawn, 1 = at its narrowest)."""
    q = max(0.45, 1.0 - p)
    c.translate(x, 0); c.scale(q, 1); c.translate(-x, 0)
