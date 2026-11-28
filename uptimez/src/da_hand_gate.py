"""The Double Agent (episode 15): the hand gate. A frame whose hands break the canon fails the build.

Why (Tomas, 26 Nov, "12 kartu"): twelve rounds of hand fixes in this episode, each found by him or an outside review
and not by me. The canon (DITreneris/uptimez docs/rules-hands-and-phones.md, CANON.md "Hands") is checked here, by
code, on every frame, before anyone looks at it. hand_gate.py (The Offer) already checks a rig hand under a grip; its
check() is reused for that rule.

How: install() records every hand and arm while a frame draws:
  - hands_ps.draw (the outermost one, after da_arms.setup() and hands_v4.enable()): the shape, where, the forearm's
    direction, the thumb side passed in. hands_ps.redraw_at / redraw_late are the canon second pass over a held prop:
    not recorded twice.
  - kit.arm, acts_ob.arm, da_arms._arm (whichever a rig swaps in): shoulder, elbow, hand, the bend.
  - of_cast.GRIP_LOG: clutches and the other prop hands.
  - robot_grip() / robot_rest() below: the robot's two canon hands (CANON.md: "The robot has two: at rest and the
    gripper"), drawn here so they are logged.
A scene declares, BEFORE drawing (the job list, step 2 of the fix): jobs(...) one line per hand (who, side, job, the
canon table row it uses), prop(...) the rects a hand may hold, solid(...) the rects nothing may pass through.

The rules (each a real fault from the twelve rounds):
  JOB      no job list, or the hands drawn are not the hands listed (a hand nobody planned)
  LEGACY   a shape the canon table does not list for new shots (relax, cup, tuck, two, salute, point_s, beckon...)
  WRIST    two hands at one wrist (hand_gate.check, and two recorded hands within 3 units)
  POLE     an elbow bent under 20 degrees that does not hang (a forearm more than 25 degrees off straight down)
  CROSS    two forearms of one person crossing, or a hand past the far shoulder (an arm across the chest)
  THUMB    two left hands: a hanging forearm whose thumb side was not mirrored (da_arms.setup() not run)
  AIR      a holding hand (grab, pinch, clutch, phone_grip, handle_grip) touching no declared prop
  ROBOT    a robot hand on a prop or inside a solid without the canon gripper
  LAYER    a rig drawn twice through a mask, or clipped with the cut showing (S8r v3: scraps and a seam at the belt)
  FEET     a shoe overlapping a solid (S8r v3: the throne's caster on Don's shoe)
  MISREAD  a job still listed after three misreads by audits or viewers (the canon: change the gesture)
  SEEN     (on the finished frame) the held prop's own colours missing round a holding hand: covered, or off it.
           Limit: one colour shared by several parts of a prop (the throne's gold rim beside its gold post) counts too.
What it cannot see (say so, do not pretend): a held prop covered by a rig drawn after it (S8r v2a: the clutch on
Don's belly passed, the armrest was under him), a robot arm hidden under the badge, a hand that reads small at phone size,
whether the gesture reads. Those are the full-size crops (step 3), looked at by me before anything is sent.

  python3 da_hand_gate.py selftest   -> every planted fault from the twelve rounds must fail, the fixed S8r must pass
"""
import math
import subprocess
import sys

import kit

CANON_JOBS = ("quiet", "point", "point_t", "grab", "clutch", "pinch", "fist", "palm", "thumb", "phone_grip",
              "handle_grip", "board_two", "tap_insert", "robot_rest", "robot_grip")
PENDING = ("pinch_pinky", "saucer_hold")                         # new rows tested in this film, awaiting the canon table
LEGACY = ("relax", "relax_s", "cup", "tuck", "two", "two_s", "salute", "point_s", "beckon")
LIB_JOB = {"RELAXED": "quiet", "GRAB": "grab", "CLUTCH": "clutch", "PINCH": "pinch", "PALM": "palm", "FIST": "fist",
           "CUP_GRIP": "pinch_pinky", "SAUCER_SUPPORT": "saucer_hold",
           "CUP_GRIP_TUCK": "pinch_pinky"}   # (28 Nov, 5.2) the same grip, the little finger in (da_s52_anim)   # hand_lib_v4's poses -> the canon table's jobs
HOLDING = ("grab", "pinch", "clutch", "phone_grip", "handle_grip") + PENDING
ROBOT_SKIN = (0.36, 0.38, 0.43)                                  # waiter_kit.STEEL_DARK: the robot's arms pass it as skin
METAL = (0.55, 0.58, 0.62)                                       # the canon sheet's robot metal

S = [2.0]                                                        # device units per frame unit
HANDS, ARMS, ROBOT, PROPS, SOLIDS, JOBS = [], [], [], [], [], []
LAYERS, FEET, MISREADS = [], [], {}
_IN_REDRAW = [0]
_ON = [False]


def _f(c, x, y):
    dx, dy = c.user_to_device(x, y)
    return dx / S[0], dy / S[0]


def _real(c):
    try:
        return c.get_target().get_width() > 0
    except Exception:
        return True


# ---- declarations (written before the drawing) ---------------------------------------------------------------------

VESSELS = []   # 28 Nov (Tomas: "visi puodeliai laikomi bet kaip"): every cup, mug, saucer and jug as its drawer drew it


def vessel(k, name, state, handle=None, base=None, rect=None):
    """registered by the vessel's own drawer (da_cups), never by the caller at a wrist. state: 'rest' (on a surface),
    'free' (falling), 'held', 'unknown' (drawn past da_cups: fails). handle, base: user points; rect: user (x, y, w, h)."""
    c = k.c
    if not _real(c) or _IN_REDRAW[0]:
        return
    x, y, w, h = rect
    pts = [_f(c, x + a * w, y + b * h) for a in (0, 1) for b in (0, 1)]
    R = (name, min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts))
    VESSELS.append(dict(name=name, state=state, handle=_f(c, *handle) if handle else None,
                        base=_f(c, *base) if base else None, rect=R))
    PROPS.append(R)


NO_HANDS = [False]


def nohands():
    """a drawing declared with no hand in it (28 Nov, animation: a hand leaves the frame): any hand drawn fails JOB."""
    NO_HANDS[0] = True


def jobs(*rows):
    """rows: (who, side, job, canon row). side "L"/"R" = screen left/right."""
    for r in rows:
        assert len(r) == 4, r
        JOBS.append(tuple(r))


COLORS = {}                                                      # prop name -> its colours (0..1), for the SEEN rule


def prop(k, name, x, y, w, h, colors=None):
    c = k.c
    pts = [_f(c, x + a * w, y + b * h) for a in (0, 1) for b in (0, 1)]
    PROPS.append((name, min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts)))
    if colors:
        COLORS[name] = colors


def solid(k, name, x, y, w, h):
    c = k.c
    pts = [_f(c, x + a * w, y + b * h) for a in (0, 1) for b in (0, 1)]
    SOLIDS.append((name, min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts)))


def layer(why):
    """a rig drawn in pieces or twice (a mask, a clip whose cut shows): the joins showed in S8r v3 (audit 27 Nov)."""
    LAYERS.append(why)


def foot(k, name, x, y, w, h):
    c = k.c
    pts = [_f(c, x + a * w, y + b * h) for a in (0, 1) for b in (0, 1)]
    FEET.append((name, min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts)))


def misreads(d):
    """{(who, side, job): times an outside audit or viewer misread it}: the canon's "three times changes the gesture"."""
    MISREADS.update(d)


def reset():
    for l_ in (HANDS, ARMS, ROBOT, PROPS, SOLIDS, JOBS, LAYERS, FEET):
        del l_[:]
    COLORS.clear(); MISREADS.clear(); NO_HANDS[0] = False; VESSELS.clear()
    import of_cast as oc
    del oc.GRIP_LOG[:]


# ---- the robot's two canon hands -----------------------------------------------------------------------------------

def _frame(k, x, y, d, w):
    """move to the wrist, +x along the forearm, canon units (the canon arm is 22 wide)."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(math.atan2(d[1], d[0])); f = w / 22.0; c.scale(f, f)
    return c


def robot_rest(k, x, y, d, w):
    """bp_hand_sheet._robot_rest's head: a metal ball at the wrist."""
    if _real(k.c):
        ROBOT.append(dict(job="robot_rest", at=_f(k.c, x, y)))
    c = _frame(k, x, y, d, w)
    c.new_path(); c.arc(16, 0, 18, 0, 2 * math.pi); c.set_source_rgb(*METAL); c.fill_preserve()
    c.set_source_rgb(*kit.INK); c.set_line_width(2.4); c.stroke()
    c.restore()


def robot_grip(k, x, y, d, w):
    """bp_hand_sheet._robot_grip's head, exactly (canon units, the arm 22 wide): the block from 14 to 50 along the
    forearm, 44 across; two jaws from (4, -+20) to (40, -+28) on its sides. What it holds sits under the block, the jaws
    on either side of it. (27 Nov: my v2/v3a had moved the jaws 46 units past the block: not the canon.)"""
    if _real(k.c):
        ROBOT.append(dict(job="robot_grip", at=_f(k.c, x, y)))
    c = _frame(k, x, y, d, w)
    c.rectangle(14, -22, 36, 44); c.set_source_rgb(0.25, 0.27, 0.30); c.fill_preserve()
    c.set_source_rgb(*kit.INK); c.set_line_width(2.2); c.stroke()
    c.set_line_cap(1)
    for y0, y1 in ((-20, -28), (20, 28)):
        for col, lw in ((kit.INK, 12), (METAL, 7)):
            c.set_source_rgb(*col); c.set_line_width(lw); c.new_path(); c.move_to(4, y0); c.line_to(40, y1); c.stroke()
    c.set_line_cap(0)
    c.restore()


GRIP_HOLD = 32                                                   # canon units along the forearm: the middle of the block


# ---- recording -----------------------------------------------------------------------------------------------------

def _wrap_arm(fn):
    if getattr(fn, "_gate", False):
        return fn

    def arm(k, sx, sy, a1, a2, col, skin, seed, ln=48, w=17):
        out = fn(k, sx, sy, a1, a2, col, skin, seed, ln=ln, w=w)
        c = k.c
        if _ON[0] and not _IN_REDRAW[0] and _real(c):
            d = lambda a: (math.sin(math.radians(a)), math.cos(math.radians(a)))
            ex, ey = sx + d(a1)[0] * ln, sy + d(a1)[1] * ln
            robot = tuple(round(v, 2) for v in skin) == ROBOT_SKIN
            ARMS.append(dict(s=_f(c, sx, sy), e=_f(c, ex, ey), h=_f(c, *out), a1=a1, a2=a2, robot=robot))
        return out
    arm._gate = True
    return arm


def install():
    """after da_arms.setup() and hands_v4.enable()."""
    import hands_ps as hp
    import acts_ob as ac
    import da_arms
    if _ON[0]:
        return
    kit.arm = _wrap_arm(kit.arm)
    ac.arm = _wrap_arm(ac.arm)
    da_arms._arm = _wrap_arm(da_arms._arm)
    inner = hp.draw

    def draw(k, g, hx, hy, w, skin, d, arm):
        c = k.c
        if not _IN_REDRAW[0] and _real(c):
            ux, uy = c.user_to_device_distance(*d)
            n = math.hypot(ux, uy) or 1.0
            HANDS.append(dict(g=g, at=_f(c, hx, hy), d=(ux / n, uy / n), d_user=tuple(d), arm=arm, w=w * c.get_matrix()[0] / S[0]))
        return inner(k, g, hx, hy, w, skin, d, arm)
    hp.draw = draw
    import hand_lib_v4 as hl                                     # 28 Nov: the episode's library hands (rig_hands) were
    inner_lr = hl.draw_lr                                        # drawn past the gate: logged now, by their canon job

    def draw_lr(k, pose, x, y, d, w, skin, arm, *a, **kw):
        c = k.c
        r = inner_lr(k, pose, x, y, d, w, skin, arm, *a, **kw)
        if not _IN_REDRAW[0] and _real(c):
            ux, uy = c.user_to_device_distance(*d)
            n = math.hypot(ux, uy) or 1.0
            ang, side = r
            cons = {nm: _f(c, *hl.to_screen(pose, x, y, ang, w, side, pt))        # its contacts, where it drew them
                    for nm, pt in hl.POSES[pose].get("contacts", {}).items()}
            HANDS.append(dict(g=LIB_JOB.get(pose, pose), at=_f(c, x, y), d=(ux / n, uy / n), d_user=tuple(d), arm=arm,
                              w=w * c.get_matrix()[0] / S[0], lib=pose, contacts=cons))
        return r
    hl.draw_lr = draw_lr
    for name in ("redraw_at", "redraw_late"):
        orig = getattr(hp, name)

        def again(*a, _o=orig, **kw):
            _IN_REDRAW[0] += 1
            try:
                return _o(*a, **kw)
            finally:
                _IN_REDRAW[0] -= 1
        setattr(hp, name, again)
    _ON[0] = True


class paused:
    """with paused(): a second pass of a rig already recorded (drawn again over a prop): not counted twice."""
    def __enter__(self):
        _IN_REDRAW[0] += 1

    def __exit__(self, *a):
        _IN_REDRAW[0] -= 1


# ---- the rules -----------------------------------------------------------------------------------------------------

def _inside(p, r, pad):
    return r[1] - pad <= p[0] <= r[3] + pad and r[2] - pad <= p[1] <= r[4] + pad


def _cross(p1, p2, q1, q2):
    def o(a, b, c_):
        return (b[0] - a[0]) * (c_[1] - a[1]) - (b[1] - a[1]) * (c_[0] - a[0])
    return o(p1, p2, q1) * o(p1, p2, q2) < 0 and o(q1, q2, p1) * o(q1, q2, p2) < 0


FRAME = (0, 0, 540, 960)                                         # frame units: hands outside it are not seen


ELBOW_ON = [False]


def check(tol=3.0):
    import of_cast as oc
    import hand_gate
    import da_arms
    out = []
    off = [h for h in HANDS if not (FRAME[0] - 20 <= h["at"][0] <= FRAME[2] + 20 and FRAME[1] - 20 <= h["at"][1] <= FRAME[3] + 20)]
    if off:                                                      # the set's own cast far outside the camera (5.2)
        print("    note: %d hand(s) outside the frame, not checked: %s" % (len(off), sorted(set(h["g"] for h in off))))
        HANDS[:] = [h for h in HANDS if h not in off]
    grips = [dict(g, at=(g["at"][0] / S[0], g["at"][1] / S[0])) for g in oc.GRIP_LOG]
    # JOB: the hands drawn are the hands listed
    if not JOBS and not NO_HANDS[0]:
        out.append("JOB no job list: every hand needs its job and its canon row written before the drawing")
    drawn = sorted([h["g"] for h in HANDS] + [g["kind"] for g in grips if g["kind"] in CANON_JOBS + PENDING] + [r["job"] for r in ROBOT])
    listed = sorted(j[2] for j in JOBS)
    if (JOBS or NO_HANDS[0]) and drawn != listed:
        out.append("JOB drawn %s, listed %s" % (drawn, listed))
    for j in JOBS:
        if j[2] not in CANON_JOBS + PENDING:
            out.append("JOB %s %s: '%s' is not a canon job" % (j[0], j[1], j[2]))
        elif j[2] in PENDING:
            print("    note: %s %s '%s' is a new row, tested in this film, not yet in the canon table" % j[:3])
    # LAYER
    for why in LAYERS:
        out.append("LAYER %s" % why)
    # FEET: a shoe on a solid (S8r v3: his shoe under a caster, the two blacks one blob)
    for f in FEET:
        for s_ in SOLIDS:
            if f[1] < s_[3] - 1 and s_[1] < f[3] - 1 and f[2] < s_[4] - 1 and s_[2] < f[4] - 1:
                out.append("FEET %s overlaps the %s at (%d, %d)" % (f[0], s_[0], (s_[1] + s_[3]) / 2, (s_[2] + s_[4]) / 2))
    # MISREAD
    for j in JOBS:
        n = MISREADS.get(tuple(j[:3]), 0)
        if n >= 3:
            out.append("MISREAD %s %s '%s' misread %d times: change the gesture (canon rule)" % (j[0], j[1], j[2], n))
    # LEGACY
    for h in HANDS:
        if h["g"] in LEGACY:
            out.append("LEGACY '%s' at (%d, %d): not in the canon table for new shots" % ((h["g"],) + tuple(h["at"])))
    # WRIST
    pts = [h["at"] for h in HANDS]
    out += hand_gate.check(grips, pts, 8.0)
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            if math.hypot(pts[i][0] - pts[j][0], pts[i][1] - pts[j][1]) < tol:
                out.append("WRIST two hands drawn at (%d, %d)" % pts[i])
    # POLE
    for a in ARMS:
        fore = (a["a1"] + a["a2"]) % 360
        off_down = min(fore, 360 - fore)
        if abs(a["a2"]) < 20 and off_down > 25:
            out.append("POLE %s elbow bent %d deg, forearm %d deg off down, hand at (%d, %d)"
                       % ("robot" if a["robot"] else "a", abs(a["a2"]), off_down, a["h"][0], a["h"][1]))
    # ELBOW (28 Nov, outside review of 4.1): an inverted V, the elbow lifted over the shoulder while the hand hangs
    # below it (Pam "hanging" the cup from a raised elbow; IK picked the elbow side by x on a level reach)
    for a in (ARMS if ELBOW_ON[0] else ()):                     # opt-in per shot: a raised elbow is right for drinking or
        L_ = math.hypot(a["e"][0] - a["s"][0], a["e"][1] - a["s"][1]) or 1   # a mask held up (5.2, 6.8): frozen shots keep their gate
        if a["s"][1] - a["e"][1] > 0.25 * L_ and a["h"][1] - a["e"][1] > 0.25 * L_:
            out.append("ELBOW %s elbow %d px over the shoulder, hand %d px under it, hand at (%d, %d)"
                       % ("robot" if a["robot"] else "a", a["s"][1] - a["e"][1], a["h"][1] - a["e"][1], a["h"][0], a["h"][1]))
    # CROSS: arms in pairs (one rig draws its two arms one after the other, shoulders level)
    i = 0
    while i + 1 < len(ARMS):
        A, B = ARMS[i], ARMS[i + 1]
        if A["robot"] == B["robot"] and abs(A["s"][1] - B["s"][1]) < 30 and abs(A["s"][0] - B["s"][0]) < 160:
            if _cross(A["e"], A["h"], B["e"], B["h"]) or _cross(A["s"], A["e"], B["e"], B["h"]) or _cross(B["s"], B["e"], A["e"], A["h"]):
                out.append("CROSS forearms crossed at shoulders (%d, %d) and (%d, %d)" % (A["s"] + B["s"]))
            L, R = (A, B) if A["s"][0] < B["s"][0] else (B, A)
            if abs(R["s"][0] - L["s"][0]) >= 12 and (L["h"][0] > R["s"][0] + 4 or R["h"][0] < L["s"][0] - 4):
                # (28 Nov, 5.3) shoulders under 12 apart on screen: a body seen end on (lying, flipping in the air),
                # its left and right not readable from x: the forearms' crossing above still applies
                out.append("CROSS an arm across the chest: hand past the far shoulder (shoulders x %d, %d)" % (L["s"][0], R["s"][0]))
            i += 2
        else:
            i += 1
    # THUMB: the canon's hands_lr (27 Nov, PR #11) for everything drawn from now on; da_arms only for the frames locked
    # with it (S8r v4, S8 v7); neither set up: the old hands_ps rule, two left hands.
    import hands_lr as lr
    if lr._SET[0]:
        for f in lr.check():
            out.append("THUMB hands_lr: %s" % (f,))
    else:
        for h in HANDS:
            if h["g"] in ("quiet", "grab", "pinch", "fist", "point", "palm") and abs(h["d_user"][1]) > abs(h["d_user"][0]):
                final = da_arms._fix(h["arm"], h["d_user"]) if da_arms._SET[0] else h["arm"]
                if final != da_arms._fix(h["arm"], h["d_user"]):
                    out.append("THUMB two left hands: the hanging hand at (%d, %d) not mirrored (neither hands_lr nor "
                               "da_arms set up)" % h["at"])
    # AIR
    holders = [(h["g"], (list(h["contacts"].values()) or [h["at"]])[0] if h.get("contacts") else h["at"], h["w"])
               for h in HANDS if h["g"] in HOLDING] + \
              [(g["kind"], g["at"], 8.0) for g in grips if g["kind"] in HOLDING]
    for g, p, w in holders:
        if not any(_inside(p, r, max(4.0, w * 0.35)) for r in PROPS):
            out.append("AIR a '%s' at (%d, %d) holds nothing declared" % ((g,) + tuple(p)))
    # VESSEL: a held cup is held by its handle (CUP_GRIP), on a palm (SAUCER_SUPPORT), or taken by its body (GRAB)
    lib = [h for h in HANDS if h.get("lib")]
    used = set()
    for v in VESSELS:
        if v["state"] == "unknown":
            out.append("VESSEL %s drawn past da_cups (its size and its hold unchecked)" % v["name"])
            continue
        if v["state"] != "held":
            continue
        ok = False
        for i, h in enumerate(lib):
            tol = max(5.0, h["w"] * 0.6)
            if h["lib"] in ("CUP_GRIP", "CUP_GRIP_TUCK") and v["handle"] and math.hypot(h["contacts"]["handle"][0] - v["handle"][0],
                                                                      h["contacts"]["handle"][1] - v["handle"][1]) <= tol:
                ok = True; used.add(i)
            if h["lib"] == "SAUCER_SUPPORT" and v["base"] and math.hypot(h["contacts"]["saucer"][0] - v["base"][0],
                                                                          h["contacts"]["saucer"][1] - v["base"][1]) <= tol:
                ok = True; used.add(i)
            if h["lib"] == "GRAB" and _inside(h["contacts"]["object"], v["rect"], 2.0):
                ok = True; used.add(i)
        if not ok:
            out.append("VESSEL %s held by no hand: no CUP_GRIP at its handle (%s), no palm under its base, no GRAB on "
                       "its body" % (v["name"], v["handle"]))
    for i, h in enumerate(lib):
        if h["lib"] in ("CUP_GRIP", "CUP_GRIP_TUCK", "SAUCER_SUPPORT") and i not in used:
            out.append("VESSEL a %s at (%d, %d) holds no cup, mug or saucer" % ((h["lib"],) + tuple(h["at"])))
    # ROBOT
    rob_hands = [a["h"] for a in ARMS if a["robot"]]
    for p in rob_hands:
        on = [r[0] for r in PROPS + SOLIDS if _inside(p, r, 2.0)]
        gr = any(r["job"] == "robot_grip" and math.hypot(r["at"][0] - p[0], r["at"][1] - p[1]) < 6 for r in ROBOT)
        if on and not gr:
            out.append("ROBOT a robot hand at (%d, %d) on/in %s without the canon gripper" % ((p[0], p[1]) + (on,)))
    for r in ROBOT:
        if not any(math.hypot(r["at"][0] - p[0], r["at"][1] - p[1]) < 6 for p in rob_hands):
            out.append("ROBOT a %s at (%d, %d) on no robot wrist" % ((r["job"],) + tuple(r["at"])))
    return out


SEEN_R = 20.0                                                    # frame units round the hand
SEEN_MIN = 24                                                    # samples (every 2nd device pixel) of the prop's own colours
                                                                 # there; a share failed: dark leather is within reach of INK
SEEN_TOL = 40                                                    # colour distance, 0..255


def check_seen(surface):
    """SEEN (audit 27 Nov; S8r v2a passed AIR with the clutch on Don's belly, the armrest under his body): in the frame
    as drawn, the held prop's own colours must show round each holding hand. Run on the finished surface."""
    import of_cast as oc
    out = []
    W_, H_ = surface.get_width(), surface.get_height()
    stride = surface.get_stride()
    data = surface.get_data()
    holders = [(h["g"], h["at"]) for h in HANDS if h["g"] in HOLDING] + \
              [(g["kind"], (g["at"][0] / S[0], g["at"][1] / S[0])) for g in oc.GRIP_LOG if g["kind"] in HOLDING] + \
              [(r["job"], r["at"]) for r in ROBOT if r["job"] == "robot_grip"]
    for g, p in holders:
        props = [r for r in PROPS if _inside(p, r, 6.0) and r[0] in COLORS]
        if not props:
            continue
        r = props[0]
        cols = [tuple(int(v * 255) for v in col) for col in COLORS[r[0]]]
        n = hit = 0
        x0, x1 = int(max(r[1], p[0] - SEEN_R) * S[0]), int(min(r[3], p[0] + SEEN_R) * S[0])
        y0, y1 = int(max(r[2], p[1] - SEEN_R) * S[0]), int(min(r[4], p[1] + SEEN_R) * S[0])
        for yy in range(max(0, y0), min(H_, y1), 2):
            for xx in range(max(0, x0), min(W_, x1), 2):
                i = yy * stride + xx * 4
                b_, g_, r_ = data[i], data[i + 1], data[i + 2]
                n += 1
                if any((r_ - c_[0]) ** 2 + (g_ - c_[1]) ** 2 + (b_ - c_[2]) ** 2 < SEEN_TOL ** 2 for c_ in cols):
                    hit += 1
        if hit < SEEN_MIN:
            out.append("SEEN a '%s' at (%d, %d): its %s shows in %d samples round it (needs %d): covered or off it"
                       % (g, p[0], p[1], r[0], hit, SEEN_MIN))
    return out


def report(name, faults):
    print("HAND GATE %s: %s" % (name, "PASS" if not faults else "FAIL (%d)" % len(faults)))
    for f in faults:
        print("   ", f)
    return not faults


# ---- the planted faults (each one of the twelve rounds) ------------------------------------------------------------

PLANTS = {
    "s8r_v1": "S8r v1 as sent 26 Nov: pole elbows, grab on nothing, the robot's rest cap in the throne, no job list",
    "relax": "the old Father sheets: relax hands",
    "two_left": "hanging arms without da_arms.setup() (Pam's two left hands, 26 Nov; planted on Don's rig)",
    "dup": "a second hand drawn on one wrist (a prop's hand over the rig's own)",
    "robot_cap": "the robot holding with its rest cap",
    "covered": "S8r v2a: Don in front of the armrest, his clutch on his own belly (passed AIR on 26 Nov)",
    "s8r_v3": "S8r v3 (audit 27 Nov): Don drawn twice through a mask, his shoe under a caster",
    "misread": "a job misread three times and still drawn",
    "lr_old": "hands_lr in its 'old' mode (hands_ps's own rule, logged): a level mirror pair, two right hands",
    "s8r_v4": "the fixed S8r (must PASS)",
}


def plant(name):
    import cairo
    import hands_ps as hp
    import hands_v4 as hv
    import da_arms
    import don_ps as dp
    import robot_ps as rp
    if name == "lr_old":
        import hands_lr as lr
        lr.setup(); lr.MODE[0] = "old"
    elif name != "two_left":
        da_arms.setup()
    hv.enable()
    install()
    if name in ("s8r_v1", "s8r_v3", "s8r_v4", "covered", "misread"):
        import da_s8r
        da_s8r.V2[0] = name != "s8r_v1"
        da_s8r.use("v4" if name in ("s8r_v4", "misread") else "v3")
        da_s8r.DON_FRONT[0] = name == "covered"
        if name == "misread":
            da_s8r.MISREADS[("don", "L", "clutch")] = 3
        s = cairo.ImageSurface(cairo.FORMAT_RGB24, 1080, 1920)
        c = cairo.Context(s); c.scale(2, 2)
        reset()
        da_s8r.s8r(kit.Ctx(c, 0), "start")
        s.flush()
        return check() + check_seen(s)
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, 1080, 1920)
    c = cairo.Context(s); c.scale(2, 2); k = kit.Ctx(c, 0)
    reset()
    if name == "relax":
        jobs(("don", "L", "relax", "-"), ("don", "R", "relax", "-"))
        dp.don(k, 270, 800, 1.0, "stand", "neutral", hands=("relax", "relax"))
    elif name == "two_left":
        jobs(("don", "L", "quiet", "quiet"), ("don", "R", "quiet", "quiet"))
        dp.don(k, 270, 800, 1.0, (-8, 0, 8, 0), "neutral", hands=("quiet", "quiet"))
    elif name == "lr_old":
        import hands_lr as lr
        lr.reset_log(); lr.frame(cut=True)
        jobs(("don", "L", "quiet", "quiet"), ("don", "R", "quiet", "quiet"))
        dp.don(k, 270, 800, 1.0, (-20, 100, 20, -100), "neutral", hands=("quiet", "quiet"))   # forearms level, toward each other
    elif name == "dup":
        jobs(("don", "L", "quiet", "quiet"), ("don", "R", "quiet", "quiet"), ("don", "R", "fist", "fist"))
        dp.don(k, 270, 800, 1.0, (-14, 30, 14, -30), "neutral", hands=("quiet", "quiet"))
        h = HANDS[-1]
        c.save(); c.identity_matrix(); hp.draw(k, "fist", h["at"][0] * 2, h["at"][1] * 2, 40, (0.96, 0.80, 0.68), h["d_user"], 1); c.restore()
    elif name == "robot_cap":
        jobs(("robot", "L", "robot_rest", "rest"), ("robot", "R", "robot_rest", "rest"))
        o = rp.robot(k, 200, 800, 1.0, arms=((-30, -40), (40, 50)))
        hx, hy = o["hands"][1]
        prop(k, "box", hx - 10, hy - 10, 20, 20)
        for (x_, y_), dd in zip(o["hands"], ((-1, 0), (1, 0))):
            robot_rest(k, x_, y_, dd, 12)
    return check()


def selftest():
    bad = []
    for name in PLANTS:
        r = subprocess.run([sys.executable, __file__, "plant", name], capture_output=True, text=True)
        txt = r.stdout + r.stderr
        passed = "HAND GATE %s: PASS" % name in txt
        want_pass = name == "s8r_v4"
        print(("ok  " if passed == want_pass else "BAD ") + "%-10s %s -> %s" % (name, PLANTS[name], "PASS" if passed else "FAIL"))
        for line in txt.strip().splitlines()[1:]:
            print("        " + line.strip())
        if passed != want_pass:
            bad.append(name)
    print("da_hand_gate selftest", "ok" if not bad else "FAIL: %s" % bad)
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.modules["da_hand_gate"] = sys.modules["__main__"]      # the scenes import the gate by name: one set of logs
    if sys.argv[1:2] == ["plant"]:
        sys.exit(0 if report(sys.argv[2], plant(sys.argv[2])) else 1)
    sys.exit(selftest())
