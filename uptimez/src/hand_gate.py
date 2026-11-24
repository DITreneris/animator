"""The Offer hand check. The faults of_scenes already names, in one place.

A rig hand under a grip is two hands at one wrist. A phone's thumb faces the body
(want); the outer side, or a phone with no body side, fails the build.
"""
import math


def check(grips, hands, tol):
    out = []
    for g in grips:
        gx, gy = g["at"]
        for hx, hy in hands:
            if math.hypot(hx - gx, hy - gy) < tol:
                out.append("HAND two at one wrist: a rig hand under the %s at (%d, %d)" % (g["kind"], gx, gy))
                break
        if g["kind"] == "phone":
            if g["want"] is None:
                out.append("HAND a phone held without body_x at (%d, %d): its thumb side unchecked" % (gx, gy))
            elif g["thumb"] != g["want"]:
                out.append("HAND a phone's thumb on the outer side at (%d, %d)" % (gx, gy))
    return out


def selftest():
    """Each planted fault must fail. A phone with its thumb toward the body, and a lamp, must pass."""
    tol = 16.0
    two = check([dict(kind="phone", at=(100, 200), thumb=1, want=1)], [(108, 204)], tol)
    outer = check([dict(kind="phone", at=(40, 50), thumb=-1, want=1)], [], tol)
    bare = check([dict(kind="phone", at=(40, 50), thumb=1, want=None)], [], tol)
    clean = check([dict(kind="phone", at=(40, 50), thumb=1, want=1)], [(200, 200)], tol)
    lamp = check([dict(kind="lamp", at=(10, 10), thumb=None, want=None)], [(80, 80)], tol)
    bad = []
    if not any(m.startswith("HAND two at one wrist") for m in two):
        bad.append("two hands at one wrist passed")
    if not any("outer side" in m for m in outer):
        bad.append("a thumb on the outer side passed")
    if not any("without body_x" in m for m in bare):
        bad.append("a phone without body_x passed")
    if clean:
        bad.append("a clean phone failed: %s" % clean)
    if lamp:
        bad.append("a lamp failed: %s" % lamp)
    if bad:
        for line in bad:
            print("FAIL", line)
        return 1
    print("hand_gate selftest ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(selftest())
