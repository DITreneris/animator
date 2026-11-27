"""The Double Agent (episode 15): S8r, the floor seen from the office side (Tomas, stop 1: a new background). It is the
push's end (9.1) and the film's frame 0 (1.1), so one function draws both, and the loop is a state (lesson 183): what
changes during the episode is drawn where this camera cannot see it, and the start and the end must come out byte for
byte the same (md5).

Read before drawing (26 Nov): series/front-desk-set.md (v4; ep 14's tape, throne, tag); CANON.md "Scenes"; the
characters canon (Don don_ps with the curl and headset, the HR robot's production look); the locked S8 v7, whose far
plane this is, pushed in: the same plain far wall, floor and tape line, Don screen right on his side, the robot screen
left, the throne between them, its front and the $49,999 tag to us.

The state table (script v4 "The loop seam"), and how this camera hides each change:
- REVIEW · TOMORROW: Father hangs it on the throne's BACK (script 1.3 from S1, the floor camera, sees the back). From
  here the throne's front is to us: drawn first, under the chair, it is covered.
- The gap in the tape (Don's strip, 7.1): the throne stands over it; from this side the tape runs on BEHIND the throne,
  and the gap is the stretch its back and seat cover (y 480-560). Drawn first, covered.
- The last paperclip: behind the seat, the same way (its base's thin legs would show it under the caster).
- The roll: behind Don's back foot in both (7.4 stages it there), untouched: the step onto it is at 0:00.4, after frame 0.
- The blue shards (2.4): by the counter's end, off this frame.

  python3 da_s8r.py still  -> ../the-double-agent/da_s8r_v1.png  (start | end side by side) and the md5 check
Canon hands (hands_v4, quiet/grab) with da_arms.setup() (left and right mirrored)."""
import hashlib
import os
import sys
import math
import cairo
import kit
from kit import Ctx, INK, cut, rect, ellipse
import fs_set4 as s4
import ps_set as pss
import don_ps as dp
import robot_ps as rp
import dh_props as dhp
import da_arms

W, H = 540, 960
HZ = 430                                                       # the far wall meets the floor
FEET = 704                                                     # their floor line: the roll and the feet above y 720
THRONE = (238, FEET + 4, 1.15)                                 # M: the crown under the top bar (y 96), less empty wall
ROBOT = (94, FEET + 2, 0.92)
DON = (366, FEET + 8, 1.15)
ROLL = (436, FEET - 6, 0.70)
SKIRT = (0.80, 0.74, 0.62)
V2 = [False]                                                   # opt-in: the hands fixed to the canon (26 Nov, after "12 kartu")


def tape_at(t):
    """The tape's centre and half width, t 0 (the frame's bottom) .. 1 (the far wall)."""
    x0, y0, x1, y1 = 214, H, 286, HZ
    return x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, 34 * (1 - t) + 7 * t


def _t_of_y(y):
    return (H - y) / float(H - HZ)


def tape(k):
    c = k.c
    xa, ya, wa = tape_at(0.0); xb, yb, wb = tape_at(1.0)
    c.new_path(); c.move_to(xa - wa, ya); c.line_to(xa + wa, ya); c.line_to(xb + wb, yb); c.line_to(xb - wb, yb); c.close_path()
    c.set_source_rgb(*pss.TAPE); c.fill_preserve(); c.set_source_rgb(0.30, 0.22, 0.02); c.set_line_width(2.2); c.stroke()


def gap(k):
    """The bare floor where Don peeled his strip, right under the throne's base (end state only)."""
    c = k.c
    ya, yb = 560, 470                                           # behind the throne's back and seat, from this side
    (xa, _, wa), (xb, _, wb) = tape_at(_t_of_y(ya)), tape_at(_t_of_y(yb))
    c.new_path(); c.move_to(xa - wa - 1, ya); c.line_to(xa + wa + 1, ya); c.line_to(xb + wb + 1, yb); c.line_to(xb - wb - 1, yb)
    c.close_path(); c.set_source_rgb(*kit.FLOOR); c.fill_preserve()
    c.set_source_rgba(0.55, 0.46, 0.32, 0.35); c.fill()


def clip(k, x, y):
    c = k.c
    c.set_source_rgb(0.42, 0.44, 0.48); c.set_line_width(1.6)
    c.new_path(); c.move_to(x - 5, y - 2); c.line_to(x + 5, y - 2); c.arc(x + 5, y, 2, -math.pi / 2, math.pi / 2); c.line_to(x - 4, y + 2)
    c.stroke()


def review_tag_on_back(k, x, feet, s):
    """REVIEW · TOMORROW on the throne's back, at the crown's right point (drawn first: the throne's front covers it)."""
    c = k.c
    c.save(); c.translate(x, feet - 300 * s); c.scale(s, s)
    kit.cut(k, [(-30, 0), (30, 0), (30, 34), (-30, 34)], (0.99, 0.97, 0.90), shadow=False, lw=2.2)
    c.restore()


def room(k):
    c = k.c
    c.set_source_rgb(*kit.WALL); c.rectangle(0, 0, W, HZ); c.fill()
    rect(k, -6, HZ - 14, W + 12, 16, SKIRT, 5701, shadow=False, lw=1.8)
    c.set_source_rgb(*kit.FLOOR); c.rectangle(0, HZ + 2, W, H - HZ); c.fill()
    tape(k)


TAG_FONT = 19                                                   # 23 ran past the card's inner rule at this size

# The job list (step 2 of the 26 Nov fix, written before the drawing). Each hand, its job, its row in the canon table
# (docs/rules-hands-and-phones.md "The jobs"; CANON.md Hands: the robot has two, at rest and the gripper):
JOBS_V2 = (
    ("don", "L", "clutch", "clutch: a fist on an edge, fingers over its front (script 7.4: he grabs an armrest)"),
    ("don", "R", "fist", "fist: the free arm back for balance as he leans away (effort, holds nothing)"),
    ("robot", "R", "robot_grip", "gripper: the jaws round the throne's left arm post, under the armrest"),
    ("robot", "L", "robot_rest", "at rest: the back arm hanging, clear of the HR badge"),
)
JOBS_V4 = (
    ("don", "L", "clutch", "clutch: on the armrest's pad left of his body, fingers over its gold front, thumb under it"),
    ("don", "R", "quiet", "quiet: the free hand hanging (the fist read as a lump in two audits, 26-27 Nov)"),
    ("robot", "R", "robot_grip", "gripper: the block across the throne's left arm post"),
    ("robot", "L", "robot_rest", "at rest: the back arm hanging, clear of the HR badge"),
)
# The rule "the same misread three times changes the gesture", counted (the outside audits of 27 Nov, S8r v2 and v3).
MISREADS = {("don", "L", "clutch"): 2, ("don", "R", "fist"): 2, ("robot", "R", "robot_grip"): 2}
DON_R_QUIET = (4.0, 8.0)
# Where each hand lands: solved below (_ik) for the shoulders the rigs really draw (measured on a scratch surface), so a
# moved mark never leaves a hand in the air. Rig angles are local: local = screen + the lean in degrees.
DON_LEAN = 0.10                                                 # 0.14 read as a stiff board tipped over (the audit)
DON_FEET_V2 = FEET + 2                                          # just BEHIND the throne's right arm (its base at FEET + 4)
DON_X_V3 = 356                                                  # v3 (audit 27 Nov): 10 left, so the roll stays out of the rail
ROLL_V3 = (441, DON_FEET_V2, 0.60)                              # stands on the floor right of his back shoe, tail to its toe
SHOE = (0.24, 0.18, 0.13)                                       # don_ps._legs' shoe (Pick a Side)
DON_FRONT = [False]                                             # planted fault for the gate: Don in front of the armrest (v2a)
CLUTCH_T = (104, -178)                                          # the right armrest's top, near its outer end (throne units)
POST_T = (-90, -166)                                            # v2: the post's top (its jaws ended by the robot's head)
POST_X = -90                                                    # v3: the grip slides down the post until the jaws clear the head
DON_R = (6.0, 10.0)                                             # R: hangs, a little bent, the fist shut (effort)
ROBOT_BACK = (-8.0, 0.0)                                        # the back arm hangs, clear of the badge


# v4 (27 Nov, the second S8r audit + Tomas "sutvarkom vartus ir piesini"): v3 stood Don BEHIND the throne's arm and
# drew him twice through a mask, his top clipped and turned at the belt: the joins showed (a white and a grey scrap at
# the belt, a seam, a lever sliver, a caster on his shoe). v4: one Don, in FRONT of the throne, drawn once; the throne a
# little smaller (1.0) and the robot 6 left, so each stands clear of what it holds; the roll behind his back heel.
LAYOUTS = {
    "v3": dict(THRONE=(238, FEET + 4, 1.15), ROBOT=(94, FEET + 2, 0.92), DON_X=356, DON_FEET=FEET + 2,
               ROLL=(441, FEET + 2, 0.60), ROLL_BEHIND=False, LAYERED=True, LEAN=0.10, CLUTCH_T=(104, -178),
               FREE="fist", STANCE="braced", CLUTCH="of_cast"),
    "v4": dict(THRONE=(232, FEET + 4, 1.0), ROBOT=(88, FEET + 2, 0.92), DON_X=384, DON_FEET=FEET + 14,
               ROLL=(446, FEET - 4, 0.60), ROLL_BEHIND=True, LAYERED=False, LEAN=0.06, CLUTCH_T=None,
               FREE="quiet", STANCE="narrow", CLUTCH="v4"),
}
L = {}


def use(name):
    """the marks of one layout (v3 kept so the gate's planted faults rebuild it)."""
    global THRONE, ROBOT
    L.clear(); L.update(LAYOUTS[name]); L["name"] = name
    THRONE, ROBOT = L["THRONE"], L["ROBOT"]
    _SOLVED.clear()


def _throne_pt(p):
    tx, tf, ts = THRONE
    x, y = p
    cs, sn = math.cos(0.04), math.sin(0.04)
    return tx + ts * (x * cs - y * sn), tf + ts * (x * sn + y * cs)


def _tug_legs(k, x, feet, s):
    """v3 (audit: "legs a cardboard board, no feet"): the legs stand; only the top leans. Front view like the rig. The
    screen-left leg braced out toward the throne, the screen-right one under him; a shoe under each (don_ps._legs' shoe),
    a contact shadow under each shoe."""
    import don_v4 as dv
    c = k.c
    c.save(); c.translate(x, feet); c.scale(s, s)
    w = WAIST_Y = dp.WAIST_Y
    for sx_, sw in ((-34, 30), (30, 26)):                       # contact shadows first
        c.set_source_rgba(0, 0, 0, 0.22); c.save(); c.translate(sx_, 2); c.scale(sw, 5)
        c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
    if L.get("STANCE") == "narrow":                             # v4: feet under him, the front one a little out
        legs = ([(-48, w - 2), (-1, w - 2), (-6, -10), (-52, -10)], [(1, w - 2), (48, w - 2), (52, -10), (6, -10)])
        shoes = ([(-56, -12), (-4, -12), (-2, 2), (-58, 2)], [(2, -12), (58, -12), (60, 2), (0, 2)])
        creases = (((-24, w + 14), (-31, -14)), ((26, w + 14), (29, -14)))
    else:
        legs = ([(-44, w - 6), (0, w - 6), (-14, -10), (-58, -10)], [(2, w - 6), (46, w - 6), (50, -10), (6, -10)])
        shoes = ([(-64, -12), (-10, -12), (-8, 2), (-66, 2)], [(2, -12), (54, -12), (56, 2), (0, 2)])
        creases = (((-24, w + 14), (-35, -14)), ((26, w + 14), (28, -14)))
    for lg in legs:
        cut(k, lg, dv.KHAKI, shadow=False, lw=2)
    c.set_source_rgb(*INK); c.set_line_width(1.6)
    for a_, b_ in creases:
        c.move_to(*a_); c.line_to(*b_); c.stroke()
    import da_hand_gate as g
    for sh in shoes:
        cut(k, sh, SHOE, shadow=False, lw=2)
        if g._ON[0]:
            xs = [p_[0] for p_ in sh]; ys = [p_[1] for p_ in sh]
            g.foot(k, "don shoe", min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys))
    c.restore()
    return x + 56 * s                                            # the back shoe's toe, screen right


def _lean_pt(p):
    """a point of the leaning top half, on screen (don_tug rotates it about the belt)."""
    x, feet, s = L["DON_X"], L["DON_FEET"], DON[2]
    wy = feet + dp.WAIST_Y * s
    dx_, dy_ = p[0] - x, p[1] - wy
    cs, sn = math.cos(L["LEAN"]), math.sin(L["LEAN"])
    return x + dx_ * cs - dy_ * sn, wy + dx_ * sn + dy_ * cs


def don_tug(k, arms, x=None, feet=None, s=None):
    """Don, once: the rig's top leaning L["LEAN"] about the belt (not about the feet: the whole man tipped read as a
    board), its own legs cut off under the belt, the standing legs and shoes of _tug_legs. v4 draws the legs AFTER the
    top, over the cut (v3 drew them first: the cut showed as a seam, the shirt's tail and the zip's tab poked out of it)."""
    import da_hand_gate as g
    dx, df, dsc = DON
    x = L["DON_X"] if x is None else x
    feet = L["DON_FEET"] if feet is None else feet
    s = dsc if s is None else s
    c = k.c
    v3 = L["name"] == "v3"
    if v3:
        _tug_legs(k, x, feet, s)
        if g._ON[0]:
            g.layer("Don's top clipped at the belt over legs drawn first (the cut shows)")
    wy = feet + dp.WAIST_Y * s
    c.save()
    c.translate(x, wy); c.rotate(L["LEAN"]); c.translate(-x, -wy)
    c.rectangle(x - 400, feet - 2000, 800, 2000 + dp.WAIST_Y * s + 2); c.clip()
    o = dp.don(k, x, feet, s, arms, "confused", (-1, 0), lean=0.0, hands=False)
    c.restore()
    if not v3:
        _tug_legs(k, x, feet, s)
    return o


def roll_on_floor(k):
    """v3 (audit: "no contact with the floor or the tape"): the episode 14 roll standing on its edge, its sticky tongue
    lying flat on the floor to the toe of Don's back shoe (1.1, 0:00.4: that foot steps back onto it)."""
    x, floor, s = L["ROLL"]
    r = (26 + 15) * s
    c = k.c
    c.set_source_rgba(0, 0, 0, 0.22); c.save(); c.translate(x, floor + 1); c.scale(r * 1.1, 4)
    c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
    if L["ROLL_BEHIND"]:                                        # v4: behind his back heel; the tongue down to it
        hx, hy = L["DON_X"] + 40 * DON[2], L["DON_FEET"] - 4
        cut(k, [(x - 4, floor - 1), (x + 4, floor + 2), (hx + 6, hy + 3), (hx - 4, hy - 1)], pss.TAPE, shadow=False, lw=1.6)
        c.set_source_rgba(1, 1, 1, 0.55); c.set_line_width(1.2)
        c.move_to(x - 1, floor + 1); c.line_to(hx + 1, hy + 1); c.stroke()
    else:
        toe = L["DON_X"] + 56 * DON[2]
        cut(k, [(x - 6, floor - 2), (x - 6, floor + 3), (toe - 8, floor + 4), (toe - 12, floor - 1)], pss.TAPE, shadow=False, lw=1.6)
        c.set_source_rgba(1, 1, 1, 0.55); c.set_line_width(1.2)            # the sticky side's sheen
        c.move_to(x - 12, floor); c.line_to(toe - 4, floor + 1); c.stroke()
    c.save(); c.translate(x, floor - r); c.scale(s, s)
    for col, lw in ((INK, 30), (pss.TAPE, 25)):
        c.set_source_rgb(*col); c.set_line_width(lw); c.new_path(); c.arc(0, 0, 26, 0, 2 * math.pi); c.stroke()
    c.set_source_rgb(0.80, 0.62, 0.10); c.set_line_width(3); c.new_path(); c.arc(0, 0, 16, 0, 2 * math.pi); c.stroke()
    c.restore()


def pad_again(k, sx=1):
    """v3: the right armrest's pad once more over Don's second pass (his torso is behind it; only his arm is in front),
    as dh_props.ceo_chair draws it."""
    tx, tf, ts = THRONE
    c = k.c
    c.save(); c.translate(tx, tf); c.scale(ts, ts); c.rotate(0.04)
    cut(k, [(sx * 72, -178), (sx * 114, -178), (sx * 116, -160), (sx * 74, -160)], dhp.LEATHER, lw=2.2)
    c.restore()


def pad_piping(k):
    """v3 (audit: the hand on a dark pad over a dark vest did not read as a grip): a gold piping round both armrest pads'
    top and front, the throne's own trim (episode opt-in, drawn over the throne; dh_props untouched)."""
    tx, tf, ts = THRONE
    c = k.c
    c.save(); c.translate(tx, tf); c.scale(ts, ts); c.rotate(0.04)
    for sx in (-1, 1):
        a, b = sx * 72, sx * 114
        for col, lw in ((INK, 7.0), (dhp.GOLD, 4.5)):
            c.set_source_rgb(*col); c.set_line_width(lw); c.set_line_join(1)
            c.new_path(); c.move_to(a, -177); c.line_to(b, -177); c.line_to(b + sx * 2, -161); c.stroke()
    c.restore()


def _ik(S, T, l1, l2, out):
    """screen kit angles (a1, a2) putting the hand at T; out = +1/-1 picks the elbow's side (+1: screen right)."""
    dx, dy = T[0] - S[0], T[1] - S[1]
    D = min(math.hypot(dx, dy), l1 + l2 - 0.01)
    base = math.degrees(math.atan2(dx, dy))
    al = math.degrees(math.acos((l1 * l1 + D * D - l2 * l2) / (2 * l1 * D)))
    be = math.degrees(math.acos((l1 * l1 + l2 * l2 - D * D) / (2 * l1 * l2)))
    sides = [(base + al, -(180 - be)), (base - al, 180 - be)]
    ex = [S[0] + l1 * math.sin(math.radians(a)) for a, _ in sides]
    return sides[0] if (ex[0] - ex[1]) * out > 0 else sides[1]


def _arm_log(draw):
    """draw() on a scratch surface; every kit/acts_ob arm's shoulder, elbow length and skin, in frame units."""
    import acts_ob as ac
    log = []
    olds = (kit.arm, ac.arm)

    def wrap(fn):
        def arm(k_, sx, sy, a1, a2, col, skin, seed, ln=48, w=17):
            m = k_.c.get_matrix()
            log.append(((m.transform_point(sx, sy)[0] / 2, m.transform_point(sx, sy)[1] / 2), ln * math.hypot(m.xx, m.yx) / 2, skin))
            return fn(k_, sx, sy, a1, a2, col, skin, seed, ln=ln, w=w)
        return arm
    import da_hand_gate as g
    kit.arm, ac.arm = wrap(kit.arm), wrap(ac.arm)
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, 2, 2); c = cairo.Context(s); c.scale(2, 2)
    on = g._ON[0]; g._ON[0] = False                            # a scratch drawing: nothing for the gate
    try:
        draw(Ctx(c, 0))
    finally:
        kit.arm, ac.arm = olds
        g._ON[0] = on
    return log


_SOLVED = {}


def solve():
    """Don's L arm onto the armrest, the elbow out to the left (Tomas 27 Nov: the arm in front of the throne); the
    robot's front gripper's block across the post's middle (the post seen above and below it), the forearm rising from
    the lower left, the elbow down by its side (out to the right it stood on the post and hid it; up, the jaws met its
    head: audit 27 Nov). From the real shoulders."""
    if _SOLVED:
        return _SOLVED
    lg = _arm_log(lambda k: don_tug(k, (0, 0, 0, 0)))
    S, l1, _ = lg[0]
    if L["CLUTCH_T"]:
        T = _throne_pt(L["CLUTCH_T"])
    else:                                                       # v4: on the pad, a hand's width left of his torso's edge
        tx, tf, ts = THRONE
        edge = S[0] - 10                                        # the sleeve's outer side
        u = min(108.0, max(76.0, ((edge - 16 - tx) / ts)))
        T = _throne_pt((u, -178))
    side = -1 if L["name"] == "v3" else +1                      # v4: in front of him, the elbow by his side
    a1, a2 = _ik(S, T, l1, l1, side)
    Ld = math.degrees(L["LEAN"])
    _SOLVED["don"] = (a1 + Ld, a2) + (DON_R if L["FREE"] == "fist" else DON_R_QUIET)
    _SOLVED["clutch"] = T
    E = (S[0] + l1 * math.sin(math.radians(a1)), S[1] + l1 * math.cos(math.radians(a1)))
    _SOLVED["don_arm"] = (S, E, T)
    rx, rf, rs = ROBOT
    head = {}

    def rob(k):
        head["h"] = rp.robot(k, rx, rf, rs, arms=(ROBOT_BACK, (0, 0)), tilt=-0.16, look=(1, 0))["head"]
    lr = _arm_log(rob)
    Sf, r1, _ = lr[1]
    H = head["h"]
    w = 12 * rs
    import da_hand_gate as g
    jaw = g.GRIP_HOLD * w / 22.0
    tip = 50 * w / 22.0
    best = None
    for yy in range(-160, -112):                                # where on the post: the block across it
        J = _throne_pt((POST_X, yy))
        for i in range(220, 340):                               # the forearm rising to it from the lower left: 110..170
            f = i / 2.0
            u = (math.sin(math.radians(f)), math.cos(math.radians(f)))
            W = (J[0] - jaw * u[0], J[1] - jaw * u[1])
            E = (W[0] - r1 * u[0], W[1] - r1 * u[1])
            if E[1] < Sf[1] + 20 or E[0] > J[0] - 20:           # the elbow down by its side, clear left of the post
                continue
            err = abs(math.hypot(E[0] - Sf[0], E[1] - Sf[1]) - r1)
            Tp = (W[0] + tip * u[0], W[1] + tip * u[1])
            clear = math.hypot(Tp[0] - H[0], Tp[1] - H[1]) - 50 * rs
            if err > 0.6 or clear < 8:
                continue
            key = (abs(yy + 140), err)                          # nearest the post's middle (seen above and below the block)
            if best is None or key < best[0]:
                best = (key, f, E, yy, err)
    _, f, E, yy, err = best
    up = math.degrees(math.atan2(E[0] - Sf[0], E[1] - Sf[1]))
    T_ = math.degrees(-0.16)
    _SOLVED["robot"] = (ROBOT_BACK, (up + T_, f - up))          # local = screen + the tilt (T_ < 0)
    _SOLVED["robot_err"] = err
    _SOLVED["post_y"] = yy
    return _SOLVED


def throne_rects(k):
    """The throne's parts a hand may hold (prop) and the parts nothing passes through (solid), in its own units."""
    import da_hand_gate as g
    if not g._ON[0]:
        return
    tx, tf, ts = THRONE
    c = k.c
    c.save(); c.translate(tx, tf); c.scale(ts, ts); c.rotate(0.04)
    for sx in (-1, 1):
        g.prop(k, "armrest %+d" % sx, min(sx * 72, sx * 116), -180, 44, 22, colors=(dhp.GOLD,))   # the piping: LEATHER is within reach of INK
        g.prop(k, "arm post %+d" % sx, min(sx * 80, sx * 100), -172, 20, 62, colors=(dhp.GOLD, dhp.GOLD_D))
    g.solid(k, "back", -70, -330, 140, 226)
    g.solid(k, "seat", -84, -110, 168, 34)
    c.restore()
    c.save(); c.translate(tx, tf); c.scale(ts, ts)
    for a in (-1, -0.5, 0.5, 1):                                 # the casters (dh_props: (a * 70, -6), 9 x 8)
        g.solid(k, "caster", a * 70 - 10, -15, 20, 18)
    c.restore()


CLUTCH_W = 24.0
CLUTCH_W_V4 = 20.0                                              # v4: his other hand's size (measured on the frame)
ARM_PASS_W = 32.0                                               # the second pass's band round his left arm (frame units)
LEGS_PASS = ((336, 598, 120, 60), (270, 624, 66, 30))       # beside the seat; under its front edge (y 621)


def clutch_v4(k, x, y, w, skin):
    """EXCEPTION, recorded 27 Nov: a hand made in the episode, not the canon's of_cast.clutch (the canon: "An episode does
    not get its own hands file"). It is in the locked S8r v4, so it stays (the freeze rule); no new shot uses it; the
    library (hand_lib_v3) replaces it when a clutch row is drawn there.
    v4 (two audits: "five parallel tubes"): of_cast.clutch's hand, with its thumb UNDER the pad (not drawn: the pad is
    in front of it; v3's hung in front and read as a fifth finger), the four fingers of unequal length (hands_ps
    PALM_VAR's idea), the knuckle marks smaller."""
    import of_cast as oc
    c = k.c
    oc.log_grip(c, "clutch", x, y)
    c.save(); c.translate(x, y)
    c.save(); c.translate(0, -0.18 * w); c.scale(0.60 * w, 0.30 * w); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    c.set_source_rgb(*skin); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.0); c.stroke()
    for kx, ln in ((-0.40, 0.34), (-0.13, 0.42), (0.14, 0.40), (0.41, 0.30)):     # little .. index, screen left to right
        oc._capsule(c, kx * w, -0.05 * w, kx * w, ln * w, 0.21 * w, skin)
        c.set_source_rgb(0.99, 0.93, 0.88); c.arc(kx * w, -0.01 * w, 0.045 * w, 0, 2 * math.pi); c.fill()
    c.restore()


def _don_held(k, sol):
    import hands_ps as hp
    import of_cast as oc
    old_h = kit.HAND[0]
    kit.HAND[0] = hp.hand; hp.reset("quiet", L["FREE"]); hp._N[0] = 1   # the L hand is the clutch: R is the rig's 2nd
    try:
        return oc.held(k, lambda: don_tug(k, sol["don"]), lambda o_: [sol["clutch"]])
    finally:
        kit.HAND[0] = old_h


def _don_over_throne(k, sol):
    """Tomas 27 Nov ("arm in front of throne"): Don stands behind the throne's right arm, but his left arm reaches round
    the throne's back to its armrest, and his legs stand in front of its lever. Don once more, after the throne, shown
    only inside a band round that arm and a box round his legs (a mask), the gate paused (one Don, recorded once)."""
    import da_hand_gate as g
    import hands_ps as hp
    import of_cast as oc
    c = k.c
    tw, th = c.get_target().get_width(), c.get_target().get_height()
    mask = cairo.ImageSurface(cairo.FORMAT_A8, tw, th)
    mc = cairo.Context(mask); mc.set_matrix(c.get_matrix())
    S, E, T = sol["don_arm"]
    mc.set_line_width(ARM_PASS_W); mc.set_line_cap(1); mc.set_line_join(1)
    mc.move_to(*S); mc.line_to(*E); mc.line_to(*T); mc.stroke()
    for r in LEGS_PASS:                                         # his legs over the lever (its red knob read as a stain)
        mc.rectangle(*r)
    mc.fill()
    c.push_group()
    with g.paused():
        g.layer("Don drawn twice: a second pass through a mask round his arm and legs")
        _don_held(k, sol)
    c.pop_group_to_source()
    c.save(); c.identity_matrix(); c.mask_surface(mask, 0, 0); c.restore()


def _robot_v2(k, heads, sol):
    import da_hand_gate as g
    rx, rf, rs = ROBOT
    s4.shadow(k, rx, rf + 2, 60)
    wrists = []                                                 # the robot's wrists where its rig really drew them
    orig = kit.arm

    def arm(k_, sx, sy, a1, a2, col, skin, seed, ln=48, w=17):
        out = orig(k_, sx, sy, a1, a2, col, skin, seed, ln=ln, w=w)
        f = math.radians(a1 + a2)
        e1 = math.radians(a1)
        wrists.append((k_.c.get_matrix(), out, (math.sin(f), math.cos(f)), w, (sx + ln * math.sin(e1), sy + ln * math.cos(e1))))
        return out
    kit.arm = arm
    try:
        o = rp.robot(k, rx, rf, rs, arms=sol["robot"], tilt=-0.16, look=(1, 0))
    finally:
        kit.arm = orig
    heads["robot"] = o.get("head") if isinstance(o, dict) else None
    c = k.c
    for (m, (hx, hy), d, w, (ex, ey)), job in zip(wrists, ("rest", "grip")):   # its canon hands, in the arm's own space
        c.save(); c.set_matrix(m)
        c.new_path(); c.arc(ex, ey, 8 * w / 22.0, 0, 2 * math.pi); c.set_source_rgb(*INK); c.fill()   # the elbow pin (canon)
        (g.robot_rest if job == "rest" else g.robot_grip)(k, hx, hy, d, w)
        c.restore()


def s8r(k, state="start"):
    """Frame 0 (state "start") and the push's end (state "end"): Don and the robot tug the throne across the line; Don's
    back foot is beside the roll. Returns the heads (for the dead-zone check)."""
    import hands_ps as hp
    room(k)
    tx, tf, ts = THRONE
    if state == "end":                                         # everything that changed, under the throne
        gap(k)
        clip(k, tx + 6, 540)                                    # behind the seat: "under the caster", from this side
        review_tag_on_back(k, tx, tf, ts)
    sol = solve() if V2[0] else None
    layered = V2[0] and L["LAYERED"]
    if V2[0]:
        import da_hand_gate as g
        import of_cast as oc
        if g._ON[0]:
            g.jobs(*(JOBS_V2 if L["name"] == "v3" else JOBS_V4))
            g.misreads(MISREADS)
        roll_on_floor(k)
        if layered and not DON_FRONT[0]:                       # v3: Don first, behind the throne's right arm
            od = _don_held(k, sol)
    s4.shadow(k, tx, tf + 2, 120)
    old = dhp.TAG[0], dhp.TAG_FONT[0]; dhp.TAG[0] = True
    if V2[0]:
        dhp.TAG_FONT[0] = TAG_FONT                              # the price inside its gold rule (the S8r audit)
    try:
        dhp.ceo_chair(k, tx, tf, ts, lean=0.04)
    finally:
        dhp.TAG[0], dhp.TAG_FONT[0] = old
    throne_rects(k)
    heads = {}
    if V2[0]:
        pad_piping(k)
        _robot_v2(k, heads, sol)
        if not layered or DON_FRONT[0]:                        # v4 (and the planted v2a): one Don, in front
            od = _don_held(k, sol)
        else:
            _don_over_throne(k, sol)
            pad_again(k); pad_piping(k)
        cx, cy = sol["clutch"]
        skin = getattr(dp, "SKIN", oc.SKIN_LIGHT)
        if L["CLUTCH"] == "v4":
            clutch_v4(k, cx, cy - 1, CLUTCH_W_V4, skin)        # the fingers over the pad, last
        else:
            oc.clutch(k, cx, cy - 2, CLUTCH_W, skin)
        heads["don"] = _lean_pt(od["head"])
        return heads
    rx, rf, rs = ROBOT
    s4.shadow(k, rx, rf + 2, 60)
    o = rp.robot(k, rx, rf, rs, arms=((60, 20), (88, 6)), tilt=-0.16, look=(1, 0))
    heads["robot"] = o.get("head") if isinstance(o, dict) else None
    lx, ly, ls = ROLL
    dp.tape_roll(k, lx, ly, ls, ang=0.3)
    dx, df, dsc = DON
    s4.shadow(k, dx, df + 2, 70)
    od = dp.don(k, dx, df, dsc, (-92, -6, -78, 12), "confused", (-1, 0), lean=0.14, hands=("grab", "grab"))
    heads["don"] = od["head"]
    return heads


use("v4")


def render(state, scale=2):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W * scale, H * scale)
    c = cairo.Context(s); c.scale(scale, scale)
    heads = s8r(Ctx(c, 0), state)
    return s, heads


def still(out_dir="../the-double-agent", v2=True):
    """v2 (default from 26 Nov): the canon hands, and the hand gate fails the build before anything is written."""
    import hands_v4 as hv
    import da_hand_gate as g
    da_arms.setup(); hv.enable(); g.install()
    V2[0] = v2
    use("v4" if v2 else "v3")
    ok = True
    for st in ("start", "end"):
        g.reset()
        sf, _ = render(st)
        sf.flush()
        ok = g.report("S8r %s" % st, g.check() + (g.check_seen(sf) if v2 else [])) and ok
    if v2 and not ok:
        print("S8r: not written (the hand gate failed)")
        return False
    a, heads = render("start")
    b, _ = render("end")
    tag = "v4" if v2 else "v1"
    ma, mb = (hashlib.md5(bytes(x.get_data())).hexdigest() for x in (a, b))
    a.write_to_png(os.path.join(out_dir, "da_s8r_frame0_%s.png" % tag))
    b.write_to_png(os.path.join(out_dir, "da_s8r_end_%s.png" % tag))
    print("frame 0 (start) md5", ma)
    print("9.1 end (end)   md5", mb)
    print("LOOP SEAM:", "PASS, byte for byte" if ma == mb else "FAIL, the states differ on screen")
    for n, h in heads.items():
        if h:
            print("%-6s head at (%.0f, %.0f)%s" % (n, h[0], h[1], "  DEAD ZONE" if (h[1] > 720 or (h[0] > 470 and 380 < h[1] < 860)) else ""))
    return ma == mb


if __name__ == "__main__":
    sys.exit(0 if still(*sys.argv[2:]) else 1)
