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
import kit
import client_ob as co
import dh_cast as dc
import dh_poses as dq
import dh_props as dp
import fs_storyboard as sb
from cand_bc import ik, _d
from kit import INK, rect, ellipse, cut

SHX, SHY = co.SH[0], co.BT + 26                            # the shoulder on the Client's rig (the bodyguards share it)


def arms_to(x, feet, s, flip=False, targets=(), rest=None):
    """targets: points (X, Y) in set units for the hands; each goes to the nearer free shoulder. rest: the pose of an
    arm with no target (default: hanging)."""
    m = -1 if flip else 1
    free = {-1: None, 1: None}
    for X, Y in targets:
        tx, ty = (X - x) / s * m, (Y - feet) / s
        side = min((sd for sd in free if free[sd] is None), key=lambda sd: abs(sd * SHX - tx))
        free[side] = ik(side * SHX, SHY, tx, ty, co.LN1, co.LN2, side)
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
    return dc.father(k, x, feet, s, pose=pose, face=face, look=look)


def _narrow(fn):
    def f(*a, **kw):
        old = co.FACES["plain"]
        co.FACES["plain"] = dict(old, lid=0.30, eye=9.8)                      # the lids lower: not wide-eyed
        try:
            return fn(*a, **kw)
        finally:
            co.FACES["plain"] = old
    return f


@_narrow
def client(k, x, feet, s, look=(-1, 0), targets=(), clip_hip=False, face="bored"):
    pose = arms_to(x, feet, s, False, targets) if targets else "open"
    c = k.c
    if clip_hip:
        hip = feet + co.HIP * s
        c.save(); c.rectangle(x - 300, hip - 500, 600, 506); c.clip()
    import client_of as cof                                   # the garage outfit (client_of v1, 22 Nov)
    o = cof.client(k, x, feet, s, pose, face, look=look)
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


def client_sit(k, x, floor, s, look=(-1, -0.2), rag_hands=True):
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
    hands = (x - 44, seat - 54)
    o = client(k, x, hip_feet, s, look=look, targets=[(hands[0] - 6, hands[1]), (hands[0] + 10, hands[1] + 4)], clip_hip=True)
    if rag_hands:
        rag(k, hands[0] + 2, hands[1] + 2, 1.1)
    return o


def client_bent(k, x, feet, s, look=(-1, 0), hands=None, lean=0.75):
    """bent over the engine bay (to his front, screen left): client_of v2's true profile, tipped from the hips."""
    import client_of as cof
    o = cof.profile(k, x, feet, s, facing=-1, lean=lean, hands=hands)
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


def watch_pose(x, feet, s):
    """the left wrist up at his chest, turned: the watch face to his eyes."""
    hip = feet + co.HIP * s
    return [(x + 22, hip - 74)]                                                    # his watch hand (screen right)


def don_throne(k, x, floor, s, face="happy", look=(1, 0), pose=None, sweat=0, phone_dad=False, forward=0.0):
    """Don in the throne: dq.don_seated's own drawing, with his arms and face set (pose: kit angles); forward: he sits up."""
    c = k.c
    cs = s
    dp.ceo_chair(k, x, floor, cs)
    seat_y = floor - 110 * cs + 4 * s
    feet = seat_y - dq.WAIST * s
    c.save(); c.rectangle(x - 200 * s, seat_y - 400 * s, 400 * s, 400 * s + 2); c.clip()
    c.save(); c.translate(x, seat_y); c.rotate(-0.10 * forward); c.translate(-x, -seat_y)
    o = sb.don(k, x, feet, s, pose or (-150, -110, 150, 110), face, look=look)
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
        phone(k, px + 4 * s, py - 30 * s, s * 1.15, scr, ang=0.05)
    return o


TURN_DX = 34                                               # the head's slide at a full turn (ep 12 used 14: too small)


def robot(k, x, feet, s, turn=0.0):
    """turn 0..1: its head turning toward Don (episode 12's 10.5a at 1); the smile never changes."""
    if turn <= 0:
        return dq.robot_state(k, x, feet, s, "idle")
    return dq.rm.robot(k, x, feet, s, (0.0, 0, 0, (-8, 0), (8, 0)), "eager", (turn, 0), 1, head_dx=TURN_DX * turn, head_rot=0.0)
