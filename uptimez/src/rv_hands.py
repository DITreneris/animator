"""Approved. (episode 16): the hands by the canon (Tomas 28 Nov: "atrakinam ir sutvarkom pagal taisykles").

The canon is DITreneris/uptimez docs/rules-hands-and-phones.md (main 81c0ac7). The audit of 28 Nov found this
episode's stills drawn past it: no hands_lr, no hands_v4, `relax` everywhere, `clutch` asked of hands_ps (which has no
such shape and drew `relax`), Father on kit's old hand, no gate. setup() puts every rv_ drawing script on the canon:

  1 left and right   hands_lr.setup() (the thumb on side arm x sign(sin a)); episode 15's da_arms rule, which its
                     modules install at import, is switched off for this process (the canon: "anything drawn after it
                     uses hands_lr"). Episode 15's own scripts never import this module.
  2 the sheet        hands_v4.enable(): grab, pinch and fist as on the class sheet v4.
  3 rest is quiet    hands_ps.reset turns `relax` into `quiet` (a shared rig is patched from the episode: don_ps and
                     pm_ps default to `relax`; they are not edited).
  4 one hand         Father (dh_cast) draws with kit's old hand unless kit.HAND is the canon's: father() here sets it.
  5 the gate         episode 15's da_hand_gate, installed; check(sid, jobs) runs its rules on a drawn frame.
Not covered (said, not hidden): the Client's rig has its own hand (client_ps.hand: fist, palm, point), as in episodes
13-15; the gate does not see it.
"""
import kit

_SET = [False]


def setup():
    if _SET[0]:
        return
    import da_sheets                                            # episode 15's modules first: they run da_arms.setup() at import
    import da_arms
    import hands_lr
    import hands_v4 as hv
    import hands_ps as hp
    import da_hand_gate as g
    da_arms._fix = lambda arm, d: arm                           # 1: hands_lr decides the side, alone
    hands_lr.setup()
    hv.enable()                                                 # 2
    keep = hp.reset

    def reset(left="quiet", right="quiet"):                     # 3
        q = lambda g_: "quiet" if g_ in ("relax", "relax_s") else g_
        return keep(q(left), q(right))
    hp.reset = reset
    g.install()                                                 # 5
    import rv_props                                             # 7 (28 Nov): the props as episode 15 ends (the price's
    rv_props.setup_canon()                                      # swing ticket, the REVIEW card v2), retired ones gated
    import hand_lib_v4 as hl                                    # 6 (28 Nov, the FUNC rule): episode 15's rig_hands hangs
    lib = hl.draw_lr                                            # an arm with no job as the library's RELAXED; here that
                                                                # arm gets the canon's quiet, by hands_ps (Pam at her desk)
    def draw_lr(k, pose, x, y, d, w, skin, arm, *a, **kw):
        import math
        if pose != "RELAXED":
            return lib(k, pose, x, y, d, w, skin, arm, *a, **kw)
        hp.draw(k, "quiet", x, y, w * 1.2, skin, d, arm)
        return math.atan2(d[1], d[0]), arm
    hl.draw_lr = draw_lr
    g.S[0] = 1.0                                                # the stills are drawn at 540x960: device = frame units
    _SET[0] = True


def father(k, x, feet, s, hands=("quiet", "quiet"), **kw):
    """dh_cast.father with the canon's hand (4)."""
    import dh_cast as dc
    import hands_ps as hp
    old = kit.HAND[0]; kit.HAND[0] = hp.hand; hp.reset(*hands)
    try:
        return dc.father(k, x, feet, s, **kw)
    finally:
        kit.HAND[0] = old


def begin():
    """before a frame is drawn: the gate's lists empty, a new hands_lr frame (a still: a cut)."""
    import da_hand_gate as g
    import hands_lr
    g.reset()
    import rv_props
    del rv_props.PROP_FAULTS[:]
    del hands_lr.LOG[:]
    hands_lr.frame(cut=True)


def check(jobs=None):
    """after it: the gate's faults; jobs: [(who, side, job, row)] or None (no hands)."""
    import da_hand_gate as g
    _dedupe()
    if jobs:
        g.jobs(*jobs)
    else:
        g.nohands()
    import rv_props
    return [f for f in g.check() if not _other_figure(f)] + func_faults() + rv_props.props_faults()


# ---- FUNC (28 Nov, outside review "vis dar nesilaikom ranku canon"): the canon table names a FUNCTION per job ---------
# clutch -> of_cast.clutch (and hands_v4.board_two, two of them); point, grab, pinch, fist, palm, quiet -> hands_ps (via
# kit.HAND or hands_ps.draw, with hands_v4.enable()). This episode drew its held hands with episode 15's hand library
# (hand_lib_v4), which the gate counted by job name: 0 faults, and an outside review and two cold viewers saw
# "pasted", "a sticker", "no fingers round it". A library hand is a fault unless its job is one of episode 15's pending
# rows (the library's own tested shapes: pinch_pinky, saucer_hold).
def func_faults():
    import da_hand_gate as g
    return ["FUNC '%s' at (%d, %d) drawn by hand_lib_v4 (%s): the canon row's function is %s" %
            ((h["g"],) + tuple(int(v) for v in h["at"]) + (h["lib"], CANON_FUNC.get(h["g"], "?")))
            for h in g.HANDS if h.get("lib") and h["g"] not in g.PENDING]


CANON_FUNC = {"clutch": "of_cast.clutch", "board_two": "hands_v4.board_two", "grab": "hands_ps", "pinch": "hands_ps",
              "palm": "hands_ps", "fist": "hands_ps", "quiet": "hands_ps", "point": "hands_ps"}


def clutch(k, h, name=None, rect=None, lift=0.30):
    """row clutch, by its canon function: of_cast.clutch at the wrist the rig freed (without_hands), the back of the
    hand on the edge's top, four fingers down over its front, the thumb under. The thing held is drawn BEFORE this
    (object, then fingers). The forearm reaches the hand from behind the thing (below it) or from above it.
    Returns the point on the edge's top (current user units), where the caller puts the thing's top edge."""
    x, y, d, w = _local(k, h)
    P = (x + d[0] * lift * w, y + d[1] * lift * w)
    return P


def clutch_draw(k, h, P):
    import of_cast as oc
    x, y, d, w = _local(k, h)
    oc.clutch(k, P[0], P[1], w, h["skin"])


def selftest():
    """a planted library CLUTCH must fail FUNC; the canon of_cast.clutch at the same wrist must pass it."""
    import cairo
    import da_hand_gate as g
    import hand_lib_v4 as hl
    setup()
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960)
    k = kit.K(s) if hasattr(kit, "K") else type("K", (), {"c": cairo.Context(s)})()
    ok = True
    begin(); hl.draw_lr(k, "CLUTCH", 200, 300, (0, -1), 20, MALE, 1)
    f1 = func_faults(); ok &= bool(f1)
    print("plant (library CLUTCH):", "FAIL as it must" if f1 else "PASSED: the rule is broken", f1[:1])
    begin()
    import of_cast as oc
    oc.clutch(k, 200, 300, 20, MALE)
    f2 = func_faults(); ok &= not f2
    print("canon (of_cast.clutch):", "PASS" if not f2 else "FAIL", f2[:1])
    return ok



def _other_figure(fault):
    """hands_lr.check pairs a hand with the NEAREST other hand; two people standing close get paired across (3.9: Don's
    right hand with Father's left) and a correct hand is reported "turned away from the body". Such a fault is dropped
    only when the hand is right against its own partner, the hand logged next to it by the same rig."""
    import re
    import hands_lr
    m = re.match(r"THUMB hands_lr: \((\d+), (\d+), 'thumb turned away from the body'\)", fault)
    if not m:
        return False
    idx = int(m.group(2))
    rows = {r[1]: r for r in hands_lr.LOG}
    r = rows.get(idx)
    for j in (idx - 1, idx + 1):
        n = rows.get(j)
        if r and n and abs(n[2][0] - r[2][0]) < 6 * r[6] and abs(n[2][1] - r[2][1]) < 2.5 * r[6] \
                and r[5] == hands_lr._sgn(n[2][0] - r[2][0]) and n[5] == hands_lr._sgn(r[2][0] - n[2][0]):
            return True                                         # thumbs toward each other: mirrored, toward the body
    return False


def drawn():
    import da_hand_gate as g
    _dedupe()
    return sorted([h["g"] for h in g.HANDS] + [r["job"] for r in g.ROBOT])


# ---- a rig's hand replaced by a holding hand (the canon: one hand per wrist; the object, then the fingers over it) ----
MALE = (0.96, 0.78, 0.66)


def without_hands(k, draw, idxs, gestures=("quiet", "quiet")):
    """draw() draws ONE rig that calls kit.HAND (dc.father(...), dp.don(..., hands=False)) and returns its record.
    The rig's hands whose index is in idxs (0 screen-left, 1 screen-right) are NOT drawn (of_cast.held's method); the
    others are drawn with the canon hand in `gestures`. Returns (record, {idx: hand}) where hand = where the wrist is,
    in device units, for lib_hand()."""
    import math
    import hands_ps as hp
    c = k.c
    rec = []
    old = kit.HAND[0]
    kit.HAND[0] = lambda k_, hx, hy, *a: rec.append((k_.c.get_matrix(), hx, hy, a))
    try:
        o = draw()
    finally:
        kit.HAND[0] = old
    hp.reset(*gestures)
    held = {}
    for i, (m, hx, hy, a) in enumerate(rec):
        if i in idxs:
            w, skin, _seed, d = a[0], a[1], a[2], a[3]
            held[i] = dict(dev=m.transform_point(hx, hy), d=m.transform_distance(*d),
                           w=w * 1.25 * math.hypot(m.xx, m.yx), skin=skin, arm=-1 if i % 2 == 0 else 1)
        else:
            c.save(); c.set_matrix(m); hp._N[0] = i; hp.hand(k, hx, hy, *a); c.restore()
    return o, held


def _local(k, h):
    import math
    c = k.c
    x, y = c.device_to_user(*h["dev"])
    dx, dy = c.device_to_user_distance(*h["d"]); n = math.hypot(dx, dy) or 1.0
    m = c.get_matrix()
    return x, y, (dx / n, dy / n), h["w"] / math.hypot(m.xx, m.yx)


def contact(k, h, pose, name, reach=None):
    """where the library hand's contact (hand_lib_v4.POSES[pose]["contacts"][name]) will be, in the current units."""
    import math
    import hand_lib_v4 as hl
    import hands_lr
    x, y, d, w = _local(k, h)
    side = (reach if reach is not None else h["arm"]) if pose == "SAUCER_SUPPORT" else hands_lr.side(h["arm"], d)
    return hl.to_screen(pose, x, y, math.atan2(d[1], d[0]), w, side, hl.contact(pose, name))


def lib_hand(k, h, pose, back_obj=None, obj=None, reach=None, lws=0.6):
    """the hand library's pose at a wrist without_hands() freed: back_obj(k) first (the thing held), the hand over it,
    obj(k) after (a saucer on a palm). Logged by the gate and by hands_lr (hand_lib_v4.draw_lr)."""
    import hand_lib_v4 as hl
    x, y, d, w = _local(k, h)
    keep = hl.LWS[0]; hl.LWS[0] = lws
    try:
        return hl.draw_lr(k, pose, x, y, d, w, h["skin"], h["arm"], obj=obj, back_obj=back_obj, reach=reach)
    finally:
        hl.LWS[0] = keep


class second_pass(object):
    """a rig drawn again through a clip (a head kept level over a leaning body): its hands are not counted twice."""
    def __enter__(self):
        import da_hand_gate as g
        import hands_lr
        self.g = g.paused(); self.g.__enter__(); self.n = len(hands_lr.LOG); return self

    def __exit__(self, *a):
        import hands_lr
        del hands_lr.LOG[self.n:]
        self.g.__exit__(*a)


def prop(k, name, x, y, w, h):
    """a thing a holding hand may hold, declared to the gate (its AIR rule)."""
    import da_hand_gate as g
    g.prop(k, name, x, y, w, h)


def _dedupe():
    """Pam's rig (pam_bc) draws her arms twice, the second pass over her cardigan: the same hand at the same wrist is
    one hand (the canon: one hand, two passes)."""
    import da_hand_gate as g
    import hands_lr
    seen, keep = set(), []
    for h in g.HANDS:
        key = (h["g"], round(h["at"][0]), round(h["at"][1]))
        if key not in seen:
            seen.add(key); keep.append(h)
    g.HANDS[:] = keep
    seen, keep = set(), []
    for r in hands_lr.LOG:
        key = (r[0], round(r[2][0]), round(r[2][1]), r[4])
        if key not in seen:
            seen.add(key); keep.append(r)
    hands_lr.LOG[:] = keep


if __name__ == "__main__":
    import sys
    sys.exit(0 if selftest() else 1)
