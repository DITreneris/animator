"""THE OFFER (episode 13): the cast's key poses for layout v2 (the poses each shot's action needs). Nothing here changes
an older module: the rigs are episode 12's (dh_cast, dh_poses) and episodes 9-11's (client_ob), driven from outside.

- arms_to(): the four arm angles that put a rig's hands on points in set units (cand_bc.ik), either hand by nearness.
- guard(): a bodyguard with his hands where the shot needs them, and his head turned (turn -1..1: the face, the
  glasses and the earpiece slide to that side; the head's outline stays).
- father(): as episode 12 (face "hard", "low", "talk", "brow"; look), with hands placed.
- client_*: STAND-INS until Tomas's redraw (22 Nov): lying under the car, bent under the bonnet, the watch, the phone
  held out, sat on the creeper. Same rig (client_ob), the face "plain" with the lids lower.
- don_throne(): Don in the throne with his face, look and arms (the phone held up, DAD), and the sweat.
- robot(): episode 12's robot_state (the head turn, "turn"), and its visor's screen point for a card."""
import math
import cairo
import kit
import client_ob as co
import dh_cast as dc
import dh_poses as dq
import dh_props as dp
import fs_storyboard as sb
from cand_bc import ik, _d
from kit import INK, rect, ellipse, cut

SHX, SHY = co.SH[0], co.BT + 26                            # the shoulder on the Client's rig (the bodyguards share it)
TOP_CAR = [True]                                           # v2 (23 Nov): the overhead shows the car's side and the lit floor (False: v1)

# --- one hand per wrist (23 Nov, hand audit, decided) -------------------------------------------------------------------
# Every hand drawn in a frame is logged in frame units: the rigs' own hands (HAND_LOG) and the grips that are hands
# themselves (GRIP_LOG: a held phone, a fist round a lamp or a lighter, a clutch). of_scenes.render() resets them per
# frame and fails the frame on a rig hand under a grip (two hands at one wrist) or a phone thumb on the outer side.
HAND_LOG, GRIP_LOG = [], []
HAND_TOL = 16.0                                            # frame units: a rig hand this near a grip is the same wrist
HELD_OFF = [False]                                         # planted fault: held() draws the rig hands under the grips too


def _real(c):
    return c.get_target().get_width() > 100                # pass 1 of a frame draws on a 4 x 4 scratch surface


def log_grip(c, kind, x, y, thumb=None, want=None):
    if _real(c):
        GRIP_LOG.append(dict(kind=kind, at=c.user_to_device(x, y), thumb=thumb, want=want))


def held(k, draw, where):
    """draw() draws a rig and returns its record; where(o) -> the points (same user units) where grips will be drawn.
    The rig's own hands at those points are not drawn (one hand per wrist); its other hands are drawn as they were,
    straight after the rig. Use it wherever a prop with its own hand (phone_grip, thumb_fist...) is held."""
    c = k.c
    base = kit.HAND[0]
    rec = []
    kit.HAND[0] = lambda k_, hx, hy, *a: rec.append((k_, k_.c.get_matrix(), hx, hy, a))
    try:
        o = draw()
    finally:
        kit.HAND[0] = base
    pts = [c.user_to_device(*p) for p in where(o)]
    tol = HAND_TOL * 1.6
    for k_, m, hx, hy, a in rec:
        cc = k_.c
        cc.save(); cc.set_matrix(m)
        dx, dy = cc.user_to_device(hx, hy)
        if HELD_OFF[0] or not any(math.hypot(dx - px, dy - py) < tol for px, py in pts):
            base(k_, hx, hy, *a)
        cc.restore()
    return o


def inner_thumb(x, body_x, back=False):
    """the thumb's side on a held phone, screen to us: toward the body's middle; with the phone's back to us
    (at the ear), the other side."""
    t = 1 if body_x > x else -1
    return -t if back else t



def ik_low(sx, sy, tx, ty, ln1, ln2):
    """v1 (23 Nov): ik with the elbow BELOW the line to the hand (a forearm that rises to a held prop, so the prop stands
    on the fist and never covers the forearm)."""
    vx, vy = tx - sx, ty - sy
    D = max(abs(ln1 - ln2) + 0.5, min(math.hypot(vx, vy), ln1 + ln2 - 0.5))
    angD = math.degrees(math.atan2(vx, vy))
    al = math.degrees(math.acos((ln1 * ln1 + D * D - ln2 * ln2) / (2 * ln1 * D)))
    be = math.degrees(math.acos((ln1 * ln1 + ln2 * ln2 - D * D) / (2 * ln1 * ln2)))
    best = None
    for sg in (1, -1):
        a1 = angD + sg * al
        ey = sy + math.cos(math.radians(a1)) * ln1
        if best is None or ey > best[0]:
            best = (ey, a1, -sg * (180 - be))
    return best[1], best[2]


ELBOW_LOW = [False]                                        # v1 (23 Nov): set while a guard holds a prop up in front of him


def arms_to(x, feet, s, flip=False, targets=(), rest=None):
    """targets: points (X, Y) in set units for the hands; each goes to the nearer free shoulder. rest: the pose of an
    arm with no target (default: hanging)."""
    m = -1 if flip else 1
    free = {-1: None, 1: None}
    for X, Y in targets:
        tx, ty = (X - x) / s * m, (Y - feet) / s
        side = min((sd for sd in free if free[sd] is None), key=lambda sd: abs(sd * SHX - tx))
        free[side] = ik_low(side * SHX, SHY, tx, ty, co.LN1, co.LN2) if ELBOW_LOW[0] else ik(side * SHX, SHY, tx, ty, co.LN1, co.LN2, side)
    out = []
    for side in (-1, 1):
        out += list(free[side] or (rest[0:2] if side == -1 and rest else rest[2:4] if rest else (side * -4, 2)))
    return tuple(out)


def guard(k, x, feet, s, flip=False, targets=(), turn=0.0, seed=1600):
    pose = arms_to(x, feet, s, flip, targets, rest=dc.GUARD_POSE) if targets else None
    o = dc.guard(k, x, feet, s, pose=pose, flip=flip, seed=seed)
    if turn:
        _turn_head(k, x, feet, s, flip, turn, seed)
    return o


def guard_arm_front(k, x, feet, s, flip, target, skin, seed=1660, w=25.0, hand=True, from_elbow=True, upper=None, lower=None, cuff=True, draw=True, short=None):
    """v2 (23 Nov, Office Noir 3's motion_on3._sleeves, lesson 245): an arm drawn again IN FRONT (the guard behind the
    car reaching over it, the Client's arm whose rig sleeve breaks): the same IK as arms_to, ONE smooth sleeve, a cuff, the
    episode's hand. from_elbow: only the forearm (the rig's own upper arm and shoulder stay; a whole front arm read as a
    pole from his neck). upper/lower: the sleeve's colours (default the black suit). Returns the hand and its direction."""
    c = k.c
    m = -1 if flip else 1
    tx, ty = (target[0] - x) / s * m, (target[1] - feet) / s
    side = min((-1, 1), key=lambda sd: abs(sd * SHX - tx))
    a1, a2 = ik(side * SHX, SHY, tx, ty, co.LN1, co.LN2, side)
    W = lambda px, py: (x + m * px * s, feet + py * s)
    sx, sy = side * SHX, SHY
    ex, ey = sx + _d(a1)[0] * co.LN1, sy + _d(a1)[1] * co.LN1
    hx, hy = ex + _d(a1 + a2)[0] * co.LN2, ey + _d(a1 + a2)[1] * co.LN2
    qx, qy = ex + (hx - ex) * 0.80, ey + (hy - ey) * 0.80
    S, E, H, Q = W(sx, sy), W(ex, ey), W(hx, hy), W(qx, qy)
    if not draw:
        dx, dy = H[0] - E[0], H[1] - E[1]; L = math.hypot(dx, dy) or 1.0
        return H, (dx / L, dy / L)
    up_c = upper or (0.11, 0.11, 0.13)
    lo_c = lower or up_c
    if not from_elbow:
        for col, lw in ((INK, w + 5), (up_c if short is None else lo_c, w)):
            c.set_source_rgb(*col); c.set_line_width(lw); c.set_line_cap(1); c.set_line_join(1)
            c.new_path(); c.move_to(*S); c.line_to(*E); c.stroke()
        if short is not None:                                                           # a short sleeve: the shirt to its hem, then skin
            M = (S[0] + (E[0] - S[0]) * short, S[1] + (E[1] - S[1]) * short)
            for col, lw, cap in ((INK, w + 5, 0), (up_c, w + 1, 1)):
                c.set_source_rgb(*col); c.set_line_width(lw); c.set_line_cap(cap)
                c.new_path(); c.move_to(*S); c.line_to(*M); c.stroke()
            c.set_line_cap(1)
    for col, lw in ((INK, w + 5), (lo_c, w)):
        c.set_source_rgb(*col); c.set_line_width(lw); c.set_line_cap(1); c.set_line_join(1)
        c.new_path(); c.move_to(*E); c.line_to(*(Q if cuff else H)); c.stroke()
    if not from_elbow:                                                                  # the joint, no seam
        c.new_path(); c.arc(E[0], E[1], w / 2, 0, 2 * math.pi); c.set_source_rgb(*(up_c if short is None else lo_c)); c.fill()
    dx, dy = H[0] - E[0], H[1] - E[1]; L = math.hypot(dx, dy) or 1.0; dx, dy = dx / L, dy / L
    if cuff:
        for col, lw in ((INK, w + 3), ((0.97, 0.97, 0.95), w - 1)):                      # the white cuff
            c.set_source_rgb(*col); c.set_line_width(lw); c.set_line_cap(0)
            c.new_path(); c.move_to(Q[0] - dx * (1 if col == INK else 0), Q[1] - dy * (1 if col == INK else 0)); c.line_to(Q[0] + dx * 7, Q[1] + dy * 7); c.stroke()
    if hand:
        cartoon_hand(k, H[0], H[1], w * 0.9, skin, seed, (dx, dy), side * m)
    return H, (dx, dy)


def _turn_head(k, x, feet, s, flip, turn, seed):
    """the head again over itself, the features slid toward `turn` (screen units: -1 left, 1 right)."""
    c = k.c
    hy = co.HY
    m = -1 if flip else 1
    c.save(); c.translate(x, feet); c.scale(s, s)
    c.translate(0, hy + 55); c.scale(co.HEAD, co.HEAD); c.translate(0, -(hy + 55))
    pts = co._head_pts(k, hy, seed + 20)
    cut(k, pts, co.SKIN)
    hair = (0.13, 0.11, 0.10)
    cut(k, [(-47, hy - 4), (-49, hy - 30), (-38, hy - 52), (-10, hy - 62), (22, hy - 60), (44, hy - 46), (49, hy - 26),
            (47, hy - 4), (42, hy - 24), (26, hy - 38), (0, hy - 41), (-26, hy - 38), (-42, hy - 24)], hair, shadow=False, lw=2)
    dx = 22 * turn
    ex_ = 44 if turn < 0 else -44                                                  # the ear on the side he turns from
    ellipse(k, ex_, hy + 2, 7.5, 12, co.SKIN, seed + 27, shadow=False, lw=2)
    c.save(); c.translate(dx, 0)
    co._face(k, hy + 4, "plain", (turn, 0), None, seed + 30, "none")
    for sx in (-1, 1):
        sq = 0.75 if sx * turn < 0 else 1.0                                       # the far lens, foreshortened
        cut(k, [(sx * 4, hy - 12), (sx * 4 + sx * 34 * sq, hy - 13), (sx * 4 + sx * 32 * sq, hy + 8), (sx * 4 + sx * 16 * sq, hy + 13),
                (sx * 6, hy + 8)], (0.03, 0.03, 0.04), shadow=False, lw=2)
    c.set_source_rgb(0.03, 0.03, 0.04); c.set_line_width(4)
    c.move_to(-6, hy - 9); c.line_to(6, hy - 9); c.stroke()
    c.restore()
    c.restore()


def father(k, x, feet, s, face="hard", look=(1, 0), targets=()):
    pose = "stand"
    if targets:
        # Father is Don's rig (kit.person, h 1.12): its shoulders at (+-40, -300 h + 92), arms 48 + 48
        h = 1.12
        sy = -300 * h + 78 + 14
        free = {}
        for X, Y in targets:
            tx, ty = (X - x) / s, (Y - feet) / s
            side = -1 if tx < 0 else 1
            free[side] = ik(side * 40, sy, tx, ty, 48, 48, side)
        pose = tuple(list(free.get(-1, (-8, 0))) + list(free.get(1, (8, 0))))
    dc.BROW_UP[0] = 14 if face == "brow2" else 9; dc.BROW_DARK[0] = face == "brow2"                                # v8: his one move, big enough to read
    dc.MOUTH_CODE[0] = FATHER_MOUTH[0]; dc.BLINK[0] = blink("father")
    try:
        o = dc.father(k, x, feet, s, pose=pose, face="brow" if face == "brow2" else face, look=look)
    finally:
        dc.BROW_UP[0] = 9; dc.BROW_DARK[0] = False; dc.MOUTH_CODE[0] = None; dc.BLINK[0] = False
    _stubble(k, o["head"], s, low=face == "low")
    return o


def _stubble(k, head, s, low=False):
    """episode 13 only (22 Nov, decided: 3 of 4 cold viewers read him as a woman): a grey shadow on the jaw and the
    upper lip, so the face reads as a man's. Drawn over dh_cast's father; episode 12 is untouched."""
    c = k.c
    hx, hy = head
    c.save(); c.translate(hx, hy + (6 if low else 0) * s); c.scale(s, s)
    sh = (0.40, 0.38, 0.38, 0.32)
    c.new_path()                                                     # the jaw, under the mouth, cheek to cheek
    c.move_to(-36, 22); c.curve_to(-34, 38, -18, 45, 0, 45); c.curve_to(18, 45, 34, 38, 36, 22)
    c.curve_to(28, 30, 18, 36, 0, 37); c.curve_to(-18, 36, -28, 30, -36, 22); c.close_path()
    c.set_source_rgba(*sh); c.fill()
    c.new_path()                                                     # the upper lip
    c.move_to(-13, 25); c.curve_to(-6, 22, 6, 22, 13, 25); c.line_to(12, 28); c.curve_to(5, 26.5, -5, 26.5, -12, 28); c.close_path()
    c.set_source_rgba(*sh); c.fill()
    c.set_source_rgba(0.28, 0.26, 0.26, 0.6)                         # the stipple, on the jaw only
    import random
    rnd = random.Random(1313)
    n = 0
    while n < 46:
        px, py = rnd.uniform(-35, 35), rnd.uniform(24, 44)
        edge_top = 22 + 15 * (1 - (abs(px) / 36) ** 2)               # under the inner curve
        edge_bot = 45 - 23 * (abs(px) / 36) ** 2
        if not (edge_top <= py <= edge_bot):
            continue
        n += 1
        c.arc(px, py, 1.0, 0, 2 * math.pi); c.fill()
    c.restore()


def _narrow(fn):
    def f(*a, **kw):
        old = co.FACES["plain"]
        co.FACES["plain"] = dict(old, lid=0.30, eye=9.8)                      # the lids lower: not wide-eyed
        try:
            return fn(*a, **kw)
        finally:
            co.FACES["plain"] = old
    return f


MOUTH = [None]                                             # the film's lip sync: a mouth code for the Client this drawing
FATHER_MOUTH = [None]; DON_MOUTH = [None]                  # v2 (23 Nov, decided): lip sync for every speaker with a mouth
NOW = [None]                                               # v1 (23 Nov, decided: no frozen frames): the film's clock this drawing


LOOP_T = [None]                                            # the film's length: breaths fit it a whole number of times (the loop)


def _fit(period):
    T = LOOP_T[0]
    return T / max(1, round(T / period)) if T else period


def blink(name):
    """a blink, 2 drawings, on each face's own clock (the film's time, so a cut doesn't reset it); never in the
    first or the last half second (frame 0 and the loop's last frame stay the same drawing)."""
    if NOW[0] is None:
        return False
    if NOW[0] < 0.5 or (LOOP_T[0] and NOW[0] > LOOP_T[0] - 0.5):
        return False
    period, off = {"client": (3.3, 0.4), "father": (4.1, 1.7), "don": (2.9, 2.2)}.get(name, (3.7, 0.0))
    return (NOW[0] + off) % period < 0.13


def breath(name):
    """a slow breath, the body taller by up to 0.7 % about the feet, each on its own phase."""
    if NOW[0] is None:
        return 0.0
    ph = {"client": 0.0, "father": 1.3, "g1": 2.1, "g2": 0.7, "don": 1.9, "pam": 2.6, "robot": 0.0}.get(name, 0.5)
    P = _fit(3.4)                                          # a whole number of breaths in the film: the loop's join holds
    return 0.007 * math.sin(2 * math.pi * (NOW[0] + ph * P / 3.4) / P) if name != "robot" else 0.0


@_narrow
def client(k, x, feet, s, look=(-1, 0), targets=(), clip_hip=False, face="bored"):
    pose = arms_to(x, feet, s, False, targets) if targets else "open"
    c = k.c
    if clip_hip:
        hip = feet + co.HIP * s
        c.save(); c.rectangle(x - 300, hip - 500, 600, 506); c.clip()
    import client_of as cof                                   # the garage outfit (client_of v1, 22 Nov)
    old_f = old_g = None
    if blink("client"):                                       # v1 (23 Nov): his blink, every lid shut for 2 drawings
        old_f, old_g = dict(co.FACES), dict(cof.FACES)        # (the garage faces are client_of's own table)
        co.FACES.update({kk: dict(vv, lid=0.98) for kk, vv in co.FACES.items()})
        cof.FACES.update({kk: dict(vv, lid=0.98) for kk, vv in cof.FACES.items()})
    try:
        o = cof.client(k, x, feet, s, pose, face, look=look, mouth=MOUTH[0])
    finally:
        if old_f is not None:
            co.FACES.clear(); co.FACES.update(old_f); cof.FACES.clear(); cof.FACES.update(old_g)
    if clip_hip:
        c.restore()
    return o


def rag(k, x, y, s=1.0):
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    cut(k, [(-16, -8), (-4, -14), (12, -10), (18, 2), (8, 12), (-6, 10), (-18, 4)], (0.92, 0.88, 0.80), lw=2)
    c.set_source_rgba(0.35, 0.30, 0.25, 0.7); c.set_line_width(1.4)
    for a, b in (((-10, -6), (6, 4)), ((-4, -10), (10, -2)), ((-14, 2), (2, 8))):
        c.move_to(*a); c.line_to(*b); c.stroke()
    c.set_source_rgba(0.15, 0.12, 0.10, 0.45)
    for px, py in ((-6, 0), (8, -4)):
        c.arc(px, py, 3, 0, 2 * math.pi); c.fill()
    c.restore()


def phone(k, x, y, s, screen=None, ang=0.0, face_out=True):
    """a phone in a hand; screen: None (its back), or a function(c) drawing in a 40 x 72 box."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    rect(k, -22, -38, 44, 76, (0.08, 0.09, 0.12), 3501, lw=2)
    if screen and face_out:
        import of_set as gs_
        gs_.protect(c, "a phone screen", -22, -38, 22, 38)
        c.save(); c.rectangle(-19, -34, 38, 68); c.clip()
        c.set_source_rgb(0.96, 0.97, 0.98); c.paint()
        screen(c)
        c.restore()
    c.restore()


def creeper(k, x, y, s=1.0):
    """the mechanic's creeper, side on: a padded board on four castors."""
    c = k.c
    rect(k, x - 70 * s, y - 10 * s, 140 * s, 14 * s, (0.80, 0.16, 0.14), 3510, lw=2.2)
    rect(k, x - 64 * s, y - 18 * s, 54 * s, 9 * s, (0.20, 0.20, 0.22), 3511, shadow=False, lw=1.6)   # the head pad
    for wx in (-58, -22, 22, 58):
        c.set_source_rgb(*INK); c.rectangle(x + wx * s - 2 * s, y + 4 * s, 4 * s, 6 * s); c.fill()
        ellipse(k, x + wx * s, y + 13 * s, 6 * s, 6 * s, (0.30, 0.30, 0.32), 3512 + wx, shadow=False, lw=1.6)


def client_sit(k, x, floor, s, look=(-1, -0.2), rag_hands=True, face="bored", wipe=0.0, hands_at=None):
    """sat up on the creeper: the board on the floor, his seat on it, knees up, the rag between his hands."""
    creeper(k, x - 20, floor - 14, 0.9)
    seat = floor - 30
    c = k.c
    for sx, (kx, fx) in ((-1, (x - 62, x - 90)), (1, (x - 30, x - 56))):           # knees up, feet out to the left
        for col, lw in ((INK, 30 * s / 0.52), ((0.17, 0.22, 0.34), 25 * s / 0.52)):
            c.set_source_rgb(*col); c.set_line_width(lw); c.set_line_cap(1)
            c.move_to(x + sx * 8, seat); c.line_to(kx, seat - 44); c.line_to(fx, floor - 6); c.stroke()
        cut(k, [(fx - 18, floor - 14), (fx + 8, floor - 14), (fx + 10, floor), (fx - 20, floor)], (0.42, 0.27, 0.14), shadow=False, lw=2)
    hip_feet = seat - co.HIP * s
    hands = (x - 44 + 10 * wipe, seat - 54 + 3 * wipe)                        # wipe -1..1: the rag worked between the hands
    if hands_at is not None:                                                 # v2 (23 Nov): the rag pressed down on the fire
        hands = hands_at
    o = client(k, x, hip_feet, s, look=look, targets=[(hands[0] - 6, hands[1]), (hands[0] + 10, hands[1] + 4)], clip_hip=True,
               face=face)
    if rag_hands:
        rag(k, hands[0] + 2, hands[1] + 2, 1.1)
    return o


def client_bent(k, x, feet, s, look=(-1, 0), hands=None, lean=0.75, head34=None):
    """bent over the engine bay (to his front, screen left): client_of v2's true profile, tipped from the hips."""
    import client_of as cof
    o = cof.profile(k, x, feet, s, facing=-1, lean=lean, hands=hands, head34=head34)
    hip = feet + co.HIP * s
    hx, hy = o["head"]                                                        # the head, tipped forward with him
    rx, ry = hx - x, hy - hip
    o["head"] = (x + rx * math.cos(-lean) - ry * math.sin(-lean), hip + rx * math.sin(-lean) + ry * math.cos(-lean))
    mx, my = -47 * s * cof.co.HEAD, (cof.co.HY + 34 * cof.co.HEAD) * s - co.HIP * s   # the mouth, at the front of the profile
    o["mouth"] = (x + mx * math.cos(-lean) - my * math.sin(-lean), hip + mx * math.sin(-lean) + my * math.cos(-lean))
    return o


def client_lying(k, s=1.6, sway=0.0, wrench_up=False):
    """UNDER THE CAR (frame units): on his back, head left, face up into the light; the wrench hand by the sump."""
    c = k.c
    c.save(); c.translate(270, 560); c.rotate(-math.pi / 2)
    o = client(k, 0, -80 + 372 * s, s, look=(0, -1))
    c.restore()
    hx, hy = o["head"]
    head = (270 + hy, 560 - hx, 55 * s)
    if wrench_up:                                                              # his hand up at the sump, the wrench in it
        wx, wy = 330 + sway, 380
        c.set_source_rgb(0.40, 0.45, 0.33); c.set_line_width(34); c.set_line_cap(1)
        c.move_to(360, 520); c.line_to(wx, wy + 30); c.stroke()
        ellipse(k, wx, wy + 14, 22, 20, co.SKIN, 3520, lw=2.2)
        c.set_source_rgb(0.66, 0.68, 0.70); c.set_line_width(9); c.move_to(wx - 4, wy); c.line_to(wx - 30, wy - 60); c.stroke()
        c.set_source_rgb(*INK); c.set_line_width(2); c.arc(wx - 32, wy - 64, 10, 0.8, 5.5); c.stroke()
    return head


def cartoon_hand(k, hx, hy, w, skin, seed, d, side):
    """episode 13's hand for everyone (23 Nov, decided): a chunky cartoon hand, a palm, three fingers and a thumb,
    a bold outline, turned along the forearm (d) with the thumb on the elbow's inner side."""
    c = k.c
    if abs(skin[0] - skin[2]) < 0.08 and abs(skin[0] - skin[1]) < 0.08:                    # grey: the robot keeps its claw
        ellipse(k, hx, hy, w * 0.6, w * 0.6, skin, seed, shadow=False, lw=2)
        return
    if _real(c):
        HAND_LOG.append(c.user_to_device(hx, hy))
    w = w * 1.25
    a = math.atan2(d[1], d[0])
    c.save(); c.translate(hx, hy); c.rotate(a)
    sk = skin
    def blob(x, y, rx, ry, rot=0.0):
        c.save(); c.translate(x, y); c.rotate(rot); c.scale(rx, ry); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        c.set_source_rgb(*sk); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.0); c.stroke()
    c.new_path()                                                                             # the wrist: out of the sleeve,
    c.move_to(-0.55 * w, -0.30 * w); c.line_to(0.05 * w, -0.34 * w)                         # narrower than the forearm
    c.line_to(0.05 * w, 0.34 * w); c.line_to(-0.55 * w, 0.30 * w); c.close_path()
    c.set_source_rgb(*sk); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.0); c.stroke()
    blob(0.10 * w, side * 0.48 * w, 0.30 * w, 0.17 * w, side * 0.7)                         # the thumb
    for j, fy in enumerate((-0.30, 0.0, 0.30)):                                              # three fingers, curled
        blob(0.62 * w, fy * w, 0.26 * w, 0.17 * w)
    blob(0.18 * w, 0.0, 0.50 * w, 0.46 * w)                                                  # the palm, over the knuckles' roots
    c.set_source_rgb(*INK); c.set_line_width(1.4)                                            # the knuckle creases
    for fy in (-0.15, 0.15):
        c.move_to(0.48 * w, fy * w); c.line_to(0.64 * w, fy * w); c.stroke()
    c.restore()


def thumb_fist(k, hx, hy, w, skin, d, point):
    """v1 (23 Nov, hand audit, decided): cartoon_hand's own fist with the thumb OUT, pointing along `point` (radians,
    user units): the same wrist, palm, blobs and outline weight as everyone's hand, the fingers curled in, the thumb
    long. Used for 2.5's thumb jerked away ("Without him.")."""
    c = k.c
    log_grip(c, "thumb fist", hx, hy)
    w = w * 1.25
    a = math.atan2(d[1], d[0])
    sk = skin
    def blob(x, y, rx, ry, rot=0.0):
        c.save(); c.translate(x, y); c.rotate(rot); c.scale(rx, ry); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        c.set_source_rgb(*sk); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.0); c.stroke()
    c.save(); c.translate(hx, hy)
    pa = point - a                                                                           # the thumb, in the hand's frame
    c.rotate(a)
    c.new_path()                                                                             # the wrist, as cartoon_hand's
    c.move_to(-0.55 * w, -0.30 * w); c.line_to(0.05 * w, -0.34 * w)
    c.line_to(0.05 * w, 0.34 * w); c.line_to(-0.55 * w, 0.30 * w); c.close_path()
    c.set_source_rgb(*sk); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.0); c.stroke()
    tx, ty = 0.18 * w + 0.80 * w * math.cos(pa), 0.80 * w * math.sin(pa)
    blob(0.18 * w + 0.42 * w * math.cos(pa), 0.42 * w * math.sin(pa), 0.52 * w, 0.18 * w, pa)   # the thumb, out
    blob(0.18 * w, 0.0, 0.50 * w, 0.46 * w)                                                  # the palm (the fist's back)
    for j, fy in enumerate((-0.26, 0.0, 0.26)):                                              # three fingers curled IN, short
        blob(0.52 * w, fy * w, 0.16 * w, 0.15 * w)
    blob(tx - 0.10 * w * math.cos(pa), ty - 0.10 * w * math.sin(pa), 0.17 * w, 0.15 * w, pa)  # its tip, over the palm's edge
    c.restore()


SKIN_LIGHT = (0.96, 0.80, 0.70)


def _capsule(c, x0, y0, x1, y1, w, col):
    for cc, lw in ((INK, w + 4.0), (col, w)):
        c.set_source_rgb(*cc); c.set_line_width(lw); c.set_line_cap(1)
        c.move_to(x0, y0); c.line_to(x1, y1); c.stroke()


def phone_grip(k, x, y, s, screen=None, ang=0.0, skin=SKIN_LIGHT, thumb=None, wrist=None, body_x=None, back=False, part="all",
               ink=1.0):
    """v3 hands (iteration 2): a phone HELD. (x, y) is the PALM (where the arm ends), the phone stands on it: the palm
    behind its lower half, the thumb crossing the front of one edge, three fingertips round the other. No wrist stub:
    the arm itself runs into the palm. v4 (23 Nov, hand audit): the thumb's side is COMPUTED from body_x (the holder's
    middle, same units): toward the body (inner_thumb). A call without body_x, or a thumb= that disagrees, fails G5.
    part: "back" (the palm only), "front" (the thumb and fingertips only), "all"; an insert that draws its own big
    phone between the two keeps this same hand. ink: the outline's weight, for a hand drawn very large."""
    c = k.c
    want = None if body_x is None else inner_thumb(x, body_x, back)
    if thumb is None:
        thumb = want if want is not None else -1
    if part in ("all", "back"):
        log_grip(c, "phone", x, y, thumb, want)
        c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
        c.save(); c.scale(26, 22); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()             # the palm, behind
        c.set_source_rgb(*skin); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.2 * ink); c.stroke()
        c.restore()
    py = y - 22 * s                                                                        # the phone's centre, above the palm
    if part == "all":
        phone(k, x + 22 * s * math.sin(ang), py + 22 * s * (1 - math.cos(ang)), s, screen, ang=ang)
    if part in ("all", "front"):
        c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
        tx = 22 * thumb
        for cc, lw in ((INK, 11 + 4.0 * ink), (skin, 11)):                                  # the thumb over the front edge, low
            c.set_source_rgb(*cc); c.set_line_width(lw); c.set_line_cap(1)
            c.move_to(tx * 1.12, 10); c.line_to(tx * 0.86, -8); c.stroke()
        for fy in (-30, -16, -2):                                                          # three fingertips round the other
            c.save(); c.translate(-tx * 1.03, fy); c.scale(8.5, 6.2); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
            c.set_source_rgb(*skin); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.0 * ink); c.stroke()
        c.restore()


def handle_grip(k, x, y, w, ang, skin=SKIN_LIGHT):
    """a fist ROUND a handle (the lamp, the lighter's case): drawn over it; ang: the handle's axis. Four finger bands
    across the handle, the thumb over them, the back of the hand behind."""
    c = k.c
    log_grip(c, "handle", x, y)
    c.save(); c.translate(x, y); c.rotate(ang)
    for i, fx in enumerate((-0.42, -0.14, 0.14, 0.42)):                                    # the curled fingers, across it
        c.save(); c.translate(fx * w, 0.05 * w); c.scale(0.16 * w, 0.40 * w); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        c.set_source_rgb(*skin); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.0); c.stroke()
    _capsule(c, -0.50 * w, -0.30 * w, 0.20 * w, -0.42 * w, 0.22 * w, skin)                   # the thumb over them
    c.restore()


def clutch(k, x, y, w, skin=SKIN_LIGHT):
    """v3 (iteration 2): a fist CLUTCHING an edge, (x, y) on the edge's top: the back of the hand on top of it, four
    fingers curling DOWN over its front (long, side by side, the knuckles white), the thumb under it."""
    c = k.c
    log_grip(c, "clutch", x, y)
    c.save(); c.translate(x, y)
    _capsule(c, -0.60 * w, 0.30 * w, -0.66 * w, 0.62 * w, 0.20 * w, skin)                    # the thumb, under the edge
    c.save(); c.translate(0, -0.18 * w); c.scale(0.60 * w, 0.30 * w); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    c.set_source_rgb(*skin); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.2); c.stroke()
    for kx in (-0.40, -0.13, 0.14, 0.41):                                                   # four fingers, down over the front
        _capsule(c, kx * w, -0.05 * w, kx * w, 0.42 * w, 0.22 * w, skin)
        c.set_source_rgb(0.99, 0.93, 0.88); c.arc(kx * w, -0.02 * w, 0.07 * w, 0, 2 * math.pi); c.fill()   # white knuckles
    c.restore()


def client_under(k, s=1.6, sway=0.0, look=(1.0, 0.6), wrench_t=0.0):
    """v3 (22 Nov, after the 5/10 audit): UNDER THE CAR, a SIDE cutaway, in frame units: the classic mechanic's view.
    He lies on his back on the creeper (client_of.profile laid down: head left, face up), the car's underside above
    him (the floor pan, the exhaust pipe, a bracket bolted to it, a wheel at the edge). BOTH arms up into it: the far
    hand holds the pipe, the near hand's wrench sits ON the bolt; his face tipped up to it. sway: the underside drops
    toward his face (the slam). wrench_t: the wrench's small turn while he works."""
    import client_of as cof
    c = k.c
    dy = abs(sway) * 1.2
    T = (730, 640)                                                                         # his feet (off the right edge)
    # the underside, above him
    c.save(); c.translate(sway * 0.3, dy)
    rect(k, -20, 250, 580, 70, (0.22, 0.23, 0.26), 3529, lw=3)                              # the floor pan
    ellipse(k, 40, 300, 110, 110, (0.07, 0.07, 0.08), 3530, lw=3)                          # a wheel, cut by the edge
    ellipse(k, 40, 300, 50, 50, (0.42, 0.43, 0.46), 3531, lw=2.4)
    for col, lw in ((INK, 22), ((0.42, 0.43, 0.46), 16)):                                 # the exhaust pipe, under the pan
        c.set_source_rgb(*col); c.set_line_width(lw); c.set_line_cap(1)
        c.move_to(120, 360); c.line_to(560, 352); c.stroke()
    for hx_ in (150, 470):                                                                # its rubber hangers up to the pan
        c.set_source_rgb(*INK); c.set_line_width(6); c.move_to(hx_, 318); c.line_to(hx_, 350); c.stroke()
    rect(k, 410, 334, 130, 48, (0.34, 0.35, 0.38), 3527, lw=2.6)                           # the muffler: a fat can on it
    c.set_source_rgb(0.25, 0.26, 0.29); c.set_line_width(2)
    for mx in (440, 475, 510):
        c.move_to(mx, 336); c.line_to(mx, 380); c.stroke()
    rect(k, 268, 316, 96, 92, (0.38, 0.39, 0.42), 3532, lw=2.6)                             # the bracket, bolted up
    for bx in (292, 340):
        ellipse(k, bx, 392, 10, 10, (0.72, 0.73, 0.76), 3533 + bx, lw=2)
        c.set_source_rgb(*INK); c.set_line_width(2); c.move_to(bx - 5, 392); c.line_to(bx + 5, 392); c.stroke()
    c.restore()
    bolt = (292 + sway * 0.3, 392 + dy)
    rect(k, 40, T[1] + 26, 700, 22, (0.24, 0.24, 0.26), 3528, lw=2)                          # the creeper under his back
    # him, laid down: local (x, y) -> frame (T.x + y, T.y - x)
    L = lambda X, Y: (-(Y - T[1]), X - T[0])
    near = (bolt[0] + 30, bolt[1] + 74)                                                    # the wrench fist, a wrench's length below
    far = (190, 372 + dy)                                                                  # the far hand on the pipe
    c.save(); c.translate(*T); c.rotate(-math.pi / 2)
    o = cof.profile(k, 0, 0, s, facing=1, look_up=0.0, hands=[L(*near), L(*far)])
    c.restore()
    hx, hy = o["head"]
    r = 55 * s
    head = (T[0] + hy + 0.30 * r, T[1] - hx + 0.10 * r, 0.6 * r)                            # the tail's aim: his cheek (the face points up)
    a_ = -1.3 + 0.3 * math.sin(wrench_t)
    for col, lw in ((INK, 14), ((0.72, 0.74, 0.76), 9)):                                   # the wrench, fist to bolt
        c.set_source_rgb(*col); c.set_line_width(lw); c.set_line_cap(1)
        c.move_to(near[0] - 4, near[1] - 16); c.line_to(bolt[0], bolt[1] + 12); c.stroke()
    c.set_source_rgb(*INK); c.set_line_width(3.5); c.new_path(); c.arc(bolt[0], bolt[1], 14, a_, a_ + 4.6); c.stroke()
    return head


def client_top(k, sway=0.0, wrench_t=0.0, s=1.12):
    """v10 (22 Nov): UNDER THE CAR, from above (frame units): the car drawn as a dashed cutaway outline with its four
    wheels, and inside it the WHOLE of him on the creeper, head left, boots right; the pipe and a bracket over his
    chest (translucent); both hands up at the bolt, the wrench ON it; his eyes on it."""
    c = k.c
    dy = abs(sway) * 0.8
    cx, cy = 300, 560                                                                      # his middle
    if TOP_CAR[0]:                                                                         # v2 (23 Nov, audit: three rounds of viewers
        EX = 430                                                                           # read "a man at a dark door"): the car's SIDE
        c.set_source_rgb(0.74, 0.73, 0.69); c.rectangle(EX, -900, 2400, 2800); c.fill()     # crosses at his knees, as in frame 0: under
        c.set_source_rgb(0.93, 0.78, 0.22); c.rectangle(EX + 250, -900, 14, 2800); c.fill() # it the dark, past it the lit floor with its
        g_ = cairo.RadialGradient(EX + 120, 820, 20, EX + 120, 820, 420)                      # yellow line and the lamp's pool, his boots
        g_.add_color_stop_rgba(0, 1.0, 0.92, 0.6, 0.45); g_.add_color_stop_rgba(1, 1.0, 0.92, 0.6, 0.0)
        c.set_source(g_); c.rectangle(EX, -900, 2400, 2800); c.fill()                       # on it; the sill in the car's blue, a tyre
        c.set_source_rgba(0, 0, 0, 0.25); c.rectangle(EX, -900, 40, 2800); c.fill()        # each side of him, half out from under it
    c.save(); c.translate(sway * 0.3, dy)                                                  # the car above him, cut away
    if not TOP_CAR[0]:
        for (wx, wy) in ((40, 360), (40, 760), (470, 360), (470, 760)):
            rect(k, wx - 30, wy - 55, 60, 110, (0.06, 0.06, 0.07), 3560 + wx + wy, lw=2.4)       # the wheels
        c.set_source_rgba(0.55, 0.65, 0.85, 0.12); c.rectangle(20, 300, 500, 520); c.fill()
        c.set_source_rgb(0.50, 0.58, 0.75); c.set_line_width(3); c.set_dash([14, 10]); c.rectangle(20, 300, 500, 520); c.stroke(); c.set_dash([])
    c.restore()
    rect(k, 60, cy - 78, 470, 156, (0.24, 0.24, 0.26), 3550, lw=2.4)                        # the creeper
    X = lambda sx, sy: (cy - sy, sx - cx)                                                  # frame -> his laid-down frame
    bolt = (262, 478 + dy)
    hands = [X(bolt[0] - 26, bolt[1] + 34), X(bolt[0] + 26, bolt[1] + 30)]
    c.save(); c.translate(cx, cy); c.rotate(-math.pi / 2)
    o = client(k, 0, 372 * s * 0.5 + 40, s, look=(-0.6, -1), targets=hands)
    c.restore()
    hx, hy = o["head"]
    head = (cx + hy, cy - hx, 55 * s)
    if TOP_CAR[0]:                                                                         # v2: the sill and the tyres OVER him (the car
        EX = 430                                                                           # is nearer the camera than he is): his knees
        c.save(); c.translate(sway * 0.3, dy)                                              # go in under the blue, the boots stay out
        c.set_source_rgba(0, 0, 0, 0.35); c.rectangle(EX, -900, 26, 2800); c.fill()        # the sill's shadow on his legs
        rect(k, EX - 46, -900, 46, 2800, (0.17, 0.36, 0.62), 3558, lw=3)
        c.set_source_rgb(0.30, 0.50, 0.76); c.rectangle(EX - 40, -900, 10, 2800); c.fill()  # its highlight
        for wy in (300, 820):
            rect(k, EX - 44, wy - 70, 80, 140, (0.08, 0.08, 0.09), 3560 + wy, lw=3)           # the tyres, half out
            c.set_source_rgb(0.32, 0.32, 0.34); c.set_line_width(5)
            for j in range(5):
                c.move_to(EX - 38, wy - 52 + j * 26); c.line_to(EX + 30, wy - 52 + j * 26); c.stroke()
        c.restore()
    c.save(); c.translate(sway * 0.3, dy)                                                  # the pipe and the bracket over his chest
    for col, lw in ((INK, 18), ((0.42, 0.43, 0.46), 12)):
        c.set_source_rgb(*col); c.set_line_width(lw); c.set_line_cap(1); c.move_to(110, 440)
        c.line_to(360 if TOP_CAR[0] else 500, 437); c.stroke()                             # v2: the pipe ends under the sill
    rect(k, 236, 446, 56, 44, (0.38, 0.39, 0.42), 3552, lw=2.2)
    c.restore()
    ellipse(k, bolt[0], bolt[1], 8, 8, (0.72, 0.73, 0.76), 3553, lw=1.8)
    a_ = -1.3 + 0.3 * math.sin(wrench_t)
    for col, lw in ((INK, 11), ((0.72, 0.74, 0.76), 7)):
        c.set_source_rgb(*col); c.set_line_width(lw); c.set_line_cap(1)
        c.move_to(bolt[0] + 24, bolt[1] + 30); c.line_to(bolt[0] + 4, bolt[1] + 8); c.stroke()
    c.set_source_rgb(*INK); c.set_line_width(3); c.new_path(); c.arc(bolt[0], bolt[1], 11, a_, a_ + 4.6); c.stroke()
    return head


def watch_pose(x, feet, s):
    """the left wrist up at his chest, turned: the watch face to his eyes."""
    hip = feet + co.HIP * s
    return [(x + 22, hip - 74)]                                                    # his watch hand (screen right)


def don_throne(k, x, floor, s, face="happy", look=(1, 0), pose=None, sweat=0, phone_dad=False, forward=0.0, phone_ear=False):
    """Don in the throne: dq.don_seated's own drawing, with his arms and face set (pose: kit angles); forward: he sits up."""
    c = k.c
    cs = s
    dp.ceo_chair(k, x, floor, cs)
    seat_y = floor - 110 * cs + 4 * s
    feet = seat_y - dq.WAIST * s
    c.save(); c.rectangle(x - 200 * s, seat_y - 400 * s, 400 * s, 400 * s + 2); c.clip()
    c.save(); c.translate(x, seat_y); c.rotate(-0.10 * forward); c.translate(-x, -seat_y)
    br_ = breath("don")                                                                 # v7 (23 Nov): he breathes in the throne
    def draw_d():
        c.save(); c.translate(x, seat_y); c.scale(1.0, 1.0 + br_); c.translate(-x, -seat_y)
        try:
            return sb.don(k, x, feet, s, pose or (-150, -110, 150, 110), face, look=look)
        finally:
            c.restore()
    o = held(k, draw_d, lambda o_: list(o_["hands"][:2])) if phone_dad else draw_d()   # v5 (hand audit): the phone and the clutch
    if DON_MOUTH[0]:                                                                    # v6 (23 Nov): his lines lip-synced,
        import iwry_mouths as im_                                                       # in the head's own (leaning) frame
        im_.don_mouth(k, o["head"], DON_MOUTH[0])
                                                                                        # are his hands there: one hand per wrist
    c.restore()
    c.restore()
    c.save(); c.translate(x, seat_y); c.scale(s, s)
    dq._leg(k, [(14, -8), (92, -22), (176, -58)], 30, 3203)
    dq._leg(k, [(-10, -8), (82, -6), (172, -40)], 30, 3204)
    dq._shoe(k, 186, -62, 1.5, 0.35, 3205); dq._shoe(k, 184, -36, 1.5, 0.20, 3206)
    c.restore()
    hx, hy = o["head"]
    for i in range(sweat):                                                     # the sweat: big drops
        dx, dy = ((40, -30), (-42, -20), (30, 6))[i]
        c.save(); c.translate(hx + dx * s, hy + dy * s); c.scale(s * 1.5, s * 1.5)
        c.move_to(0, -9); c.curve_to(7, 0, 6, 7, 0, 7); c.curve_to(-6, 7, -7, 0, 0, -9); c.close_path()
        c.set_source_rgb(0.62, 0.84, 0.95); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.6); c.stroke()
        c.restore()
    if phone_dad:
        px, py = o["hands"][0]
        def scr(c_):
            c_.set_source_rgb(0.20, 0.70, 0.35); c_.rectangle(-19, -34, 38, 68); c_.fill()
            c_.set_source_rgb(1, 1, 1); c_.select_font_face("Lilita One"); c_.set_font_size(15)
            e = c_.text_extents("DAD"); c_.move_to(-e.x_advance / 2, -2); c_.show_text("DAD")
            c_.set_font_size(8); e = c_.text_extents("calling…"); c_.move_to(-e.x_advance / 2, 12); c_.show_text("calling…")
        if phone_ear:                                                           # v4 (23 Nov, Office Noir 3's lessons 245/399): his own arm
            phone_grip(k, px + 6 * s, py, s * 0.85, None, ang=0.12, body_x=x, back=True)   # its BACK to us, against his head: on a call              # from the outer shoulder, elbow out, the phone where the pose's hand is
        else:
            phone_grip(k, px, py, s * 0.95, scr, ang=0.05, body_x=x)
        rx, ry = o["hands"][1]                                                  # v3: the other hand clutches the throne's arm
        clutch(k, rx, ry, 30 * s)
    return o


TURN_DX = 34                                               # the head's slide at a full turn (ep 12 used 14: too small)


def robot(k, x, feet, s, turn=0.0):
    """turn 0..1: its head turning toward Don (episode 12's 10.5a at 1); the smile never changes."""
    if turn <= 0:
        return dq.robot_state(k, x, feet, s, "idle")
    o = dq.rm.robot(k, x, feet, s, (0.0, 0, 0, (-8, 0), (8, 0)), "eager", (turn, 0), 1, head_dx=TURN_DX * turn * 0.5, head_rot=0.0)
    _visor_turn(k, o["screen"], 50 * s, turn)                  # v2: the face on the visor turns, not just slides
    return o


def _visor_turn(k, scr, r, u):
    """its screen face turned toward screen right by u (0..1): the eyes and the smile slide to the visor's edge, the far
    eye narrows, the smile turns into a side-on curve. The same eager smile throughout."""
    c = k.c
    sx, sy = scr
    c.set_source_rgb(0.09, 0.12, 0.24); c.arc(sx, sy, 0.86 * r, 0, 2 * math.pi); c.fill()
    cx = sx + 0.46 * r * u
    cyan = (0.45, 0.92, 1.0)
    for e, side in ((-1, "far"), (1, "near")):
        ex = cx + e * 0.30 * r * (1 - 0.45 * u)
        wx = 0.13 * r * ((1 - 0.65 * u) if side == "far" else 1.0)
        c.save(); c.translate(ex, sy - 0.10 * r); c.scale(max(0.2, wx), 0.13 * r)
        c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        c.set_source_rgba(*cyan, 0.35); c.fill_preserve() if False else None
        c.set_source_rgb(*cyan); c.fill()
    c.set_source_rgb(*cyan); c.set_line_width(0.07 * r); c.set_line_cap(1)
    c.new_path(); c.arc(cx + 0.06 * r * u, sy + 0.12 * r, 0.24 * r, 0.25 + 0.35 * u, math.pi - 0.25 - 0.15 * u); c.stroke()
