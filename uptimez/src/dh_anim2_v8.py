"""DADDY'S HOME v8, scene 2 "Good News": v7's scene (dh_anim2: its own clock, shots and mix, not a dh_anim.Scene) through
dh_anim_v8 (v8 bubbles, dead zones, set_gate, a mode without bubbles) by a small bridge (Bridge below), with the shots that
failed redrawn:
  - the throne on its set mark (452) in 2.3a-2.5' as in 1.x and 2.2 (v7: 400 from 2.3a on, a jump of 52 at the cut)
  - 2.3b "...was invested.": the shove with his palm on the throne's arm and the elbow bent, the hand on it until it
    rolls out of reach (v7: a straight arm ending in a mitten, "a pole" 2/2 in the whole-film mute test; rules: reach,
    contact all the way, a shape per state)
  - 2.2 "I didn't steal anything!": see JUMP below (v7: the "shock" pose, both fists beside his ears; rules: a hand at
    the ear = a phone)
  python3 dh_anim2_v8.py [gate|nobub]  ->  ../daddys-home/dh_s2_anim_v8.mp4"""
import math
import sys
import cairo
import kit
import hands_ps as hp
import fs_storyboard as sb
import dh_props as dp
import dh_scenes as ds
import dh_anim2 as V7
import dh_anim_v8 as E
import dh_anim3_v8 as A3

F, CH, DS_ = V7.F, V7.CH, V7.DS_
SET_THR = 452
D2 = SET_THR - 400                                          # v7 had the throne at 400 from 2.3a on


class Bridge:
    """What dh_anim_v8 reads from a dh_anim.Scene, made from a module with ROWS, T0, SHOT, DRAW, TOTAL and sound()."""
    def __init__(self, m, phone=True):
        self.m = m
        self.rows, self.T0, self.total, self.phone = m.ROWS, m.T0, m.TOTAL, phone
        self.shot = {s: dict(m.SHOT[s]) for s, _ in m.ROWS}
        self.DRAW = {s: (lambda f: (lambda sc, k, o, t, tt, n: f(k, o, t, tt, n)))(m.DRAW[s]) for s, _ in m.ROWS}
        self.INS, self.SHIFT, self._cam0, self.PRE = {}, {}, {}, None

    def sound(self, out):
        self.m.sound(out)


sc = Bridge(V7)

# ---- the set: the throne on its mark from 2.3a on; Don's step out and the roll, the same distances from it
V7.ROLL = [x + D2 for x in V7.ROLL]
V7.DONX2 = V7.DONX2 + D2
for sid in ("2.3a", "2.3b", "2.5"):
    cx, cy, z = sc.shot[sid]["cam"]
    sc.shot[sid]["cam"] = (cx + D2, cy, z)
_chair = dp.ceo_chair


def _ceo_chair(k, x, *a, **kw):                             # v7's literal 400s and its roll-back x in 2.3a, 2.5, 2.5'
    return _chair(k, x + D2 if x < SET_THR - 30 else x, *a, **kw)


V7.dp = type(sys)("dp_v8")                                  # dh_anim2 reaches the chair through its own dp name only
V7.dp.__dict__.update(dp.__dict__); V7.dp.ceo_chair = _ceo_chair


def _seq_dx(vals):
    return [v + D2 for v in vals]


def r_hand(k, o, t, tt, n):                                 # 2.3a: v7's step out, from the throne on its mark
    _plan()
    _ceo_chair(k, 400, CH[1], CH[2], seat_drop=1.0)
    x = V7.seq(t, [v for v in _seq_dx([424, 452, 476]) if v < V7.DONX2] + [V7.DONX2])
    pose = V7.seq(t, PUSH[0])
    if x < V7.DONX2:
        ds._lines(k, [(x - 34, F + 14, x - 50, F + 14), (x - 34, F + 24, x - 54, F + 24)])
    hp.reset("palm", "relax")
    d = V7.don_at(k, x, F + 26, pose, "smug", (1, -0.3), tt)
    V7.A.mouth(k, d["head"], DS_, V7.loud("2.3", tt))
    if V7.speaking("2.3", tt):
        o["say"] = ("The money...", V7.cheek(d, side=1), 1, False)


def r_peek(k, o, t, tt, n):                                 # 2.5: v7's roll-back, from off the left edge to its mark
    x = V7.seq(t, _seq_dx([150, 176, 214, 252, 286, 308, 318]))
    dp.TAG_ANG[0] = V7.seq(t, [0.5, 0.6, 0.6, 0.5, 0.4, 0.3, 0.2])
    dp.ceo_chair(k, x, CH[1], CH[2], lean=0.06, seat_drop=1.0)
    ds._lines(k, [(x - 78, F - 150, x - 56, F - 150), (x - 82, F - 110, x - 60, F - 110)])
    V7.don_at(k, V7.DONX2, F + 26, (-8, 0, 8, 0), "happy", (1, 0), tt)   # hands down (v7 "vest", clasped: "a handshake" 2/2)


# ---- 2.3a, 2.3b: the hand on the throne's arm, then the shove. PUSH[0]: 2.3a's poses (v7's, its last on the arm);
# PUSH[1]: 2.3b's, picked to keep the palm on the arm while it is in reach (search below), then bent and down.
PUSH = [[(-8, 0, 8, 0), (-14, 0, 12, 0), (-30, -6, 8, 0), (-64, -12, 8, 0), (-82, -18, 8, 0), (-78, -16, 8, 0)], None]
GRIP = [None]                                               # the hand's place on the throne, from the chair's x (2.3a's last drawing)


def _hand_at(x, pose, face="smug", look=(1, 0)):
    k = kit.Ctx(cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 4, 4)), 0)
    real = getattr(sb.don, "_real", sb.don)
    return real(k, x, F + 26, DS_, pose, face, look=look)["hands"][0]


def _solve(x_don, target, bend=(-110, -39)):
    best = None
    for a1 in range(-140, -9, 3):
        for a2 in range(bend[0], bend[1], 3):               # the elbow bent at least 40 degrees (2/2 "a pole" at 15)
            hx, hy = _hand_at(x_don, (a1, a2, 8, 0))
            e = math.hypot(hx - target[0], hy - target[1])
            if best is None or e < best[0]:
                best = (e, (a1, a2, 8, 0))
    return best


def _plan():
    """Round 2: where he stops (nearer the throne than v7's step, so the bent arm reaches its arm) and the poses."""
    if PUSH[1]:
        return PUSH[1]
    gx, gy = _hand_at(V7.DONX2, (-82, -18, 8, 0))           # v7's hand on the throne's arm (its last reach), chair at ROLL[0]
    GRIP[0] = (gx - V7.ROLL[0], gy)
    for dx in range(0, -60, -3):
        e, p = _solve(V7.DONX2 + dx, (V7.ROLL[0] + GRIP[0][0], GRIP[0][1]))
        if e < 4.0:
            break
    V7.DONX2 = V7.DONX2 + dx
    PUSH[0] = PUSH[0][:3] + [(-40, -50, 8, 0), (p[0] * 0.8, p[1], 8, 0), p]
    poses = []
    for x in V7.ROLL:
        e, q = _solve(V7.DONX2, (x + GRIP[0][0], GRIP[0][1]))
        poses.append((q, e < 6.0))
    PUSH[1] = poses
    return poses


def _push_poses():
    return _plan()


def r_push(s_, k, o, t, tt, n):                              # 2.3b: the shove; it rolls out of the frame on a squeaking wheel
    x = V7.seq(t, V7.ROLL)
    i = min(len(V7.ROLL) - 1, int(t * V7.DPS + 1e-6))
    dp.TAG_ANG[0] = V7.seq(t, [0, -0.25, -0.6, -0.7, -0.5, -0.3, -0.1, 0])
    dp.ceo_chair(k, x, CH[1], CH[2], lean=-0.10 if 1 <= i <= 4 else -0.03, seat_drop=1.0)
    if 2 <= i <= 5:
        ds._lines(k, [(x + 74, F - 170, x + 108, F - 170), (x + 80, F - 130, x + 114, F - 130), (x + 74, F - 90, x + 108, F - 90), (x + 78, F - 20, x + 102, F - 20)])
    poses = _push_poses()
    p, on = poses[i]
    if not on:                                              # out of reach: the follow-through, bent, then down
        j = i - next(q for q, (_, ok) in enumerate(poses) if not ok)
        p = [(-70, -40, 8, 0), (-46, -30, 8, 0), (-24, -14, 8, 0), (-8, 0, 8, 0)][min(j, 3)]
    hp.reset("palm" if on else "relax", "relax")
    d = V7.don_at(k, V7.DONX2, F + 26, p, "smug", (1, 0), tt)
    V7.A.mouth(k, d["head"], DS_, V7.loud("2.3", tt))
    if V7.speaking("2.3", tt):
        o["say"] = ("...was invested.", V7.cheek(d, side=1), 1, False)


# ---- 2.2: "I didn't steal anything!" (JUMP[0] replaces v7's "shock" pose, both fists beside his ears)
# Test (2 viewers, v7 and 3 poses): v7's fists "holding the price tag" 2/2; open palms raised beside his head, elbows bent:
# "hands up, not me", "don't shoot" ("clearest" 2/2, no phone 2/2); the lower poses read "by his headset".
JUMP = [(-100, -90, 100, 90)]


def r_jump(k, o, t, tt, n):
    shock = kit.ARM_POSES["shock"]
    if JUMP[0]:
        kit.ARM_POSES["shock"] = (JUMP_L[0] or JUMP[0][:2]) + tuple(JUMP[0][2:])
        hp.reset(*JUMP_G)
    try:
        V7.r_jump(k, o, t, tt, n)
    finally:
        kit.ARM_POSES["shock"] = shock
        hp.reset()


JUMP_G = ("palm", "palm")

sc.DRAW.update({"2.2": lambda s_, k, o, t, tt, n: r_jump(k, o, t, tt, n),
                "2.3a": lambda s_, k, o, t, tt, n: r_hand(k, o, t, tt, n),
                "2.3b": r_push,
                "2.5": lambda s_, k, o, t, tt, n: r_peek(k, o, t, tt, n)})

sc.SHIFT = {"1.3": (64, 52),                                  # her head and box up, out of the button rail (v7's frame: the box in it)
            "2.2": (0, 10, 0.84)}                          # wider and right: wall for his box (v7: no wall, the box on his face)
JUMP_L = [(-50, -110)]                                      # round 2: one palm up read "touching his ear/headset" 2/2; both palms
#                                                             again (2/2 in stills), the near one at his shoulder: off the price tag and under his box

SET_MOVES = {("2.3b", "throne"): 400, ("2.5", "throne"): 400, ("2.5'", "throne"): 60}   # the shove, the roll back, the bump
SET_AIR = {("2.2", "don")}                                   # his jump
SET_BEHIND, SET_WALKS, ENTRANCES = set(), set(), set()
FLYING = ("2.3b", "2.5", "2.5'")                            # the throne and its tag roll out of the frame and back in
sc.shot["2.5'"]["cam"] = (496, 684, 2.2)                    # a step right and down: the tag's swing on the bump stays out of the title bar


def frame8(tt, n, hi=1):
    A3.AVOID_EXTRA[:] = []
    if "Is he coming alone?" not in A3.HELD:                # 1.3, moved up: her box on her right, the wall above the rail
        A3.HELD["Is he coming alone?"] = (None, 1)
    return E.frame(sc, tt, n, hi)


if __name__ == "__main__":
    me = sys.modules[__name__]
    if "gate" in sys.argv[1:]:
        sys.exit(1 if E.gate(sc, me, SET_MOVES, SET_AIR, SET_BEHIND, SET_WALKS, entrances=ENTRANCES, flying=FLYING) else 0)
    if "nobub" in sys.argv[1:]:
        E.NOBUB[0] = True
    E.run(sc, me, 2)
