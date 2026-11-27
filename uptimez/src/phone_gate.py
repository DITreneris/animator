"""The phone gate (26 Nov, series hands/phones plan, Tomas: "the phones are not fixed, every frame carefully"): every HELD
phone a film draws must be drawn by the canon's grip (hands_v4's v4c, phone_grip v4c without the sheet's forearm).

install(): wraps the series' phone painters. A painter called with no hands_v4 v4c grip on the call stack is a fault,
logged once per call site with the number of drawings: FAULTS[site] = count. A phone that is not held (in the air,
on a table) is listed in NOT_HELD by its call site's function name and is not a fault.
selftest(): a planted fault (of_cast.phone_grip's old grip called directly) must be caught, and a v4c grip must pass.

    import phone_gate; phone_gate.install(); ... render ...; phone_gate.report()  -> True when no faults"""
import sys
import traceback
import collections

PAINTERS = [("of_cast", "phone"), ("cs_scene1", "phone_held"), ("cs_scene1", "grip"), ("dh_scenes", "_phone_in_hand"),
            ("dh_scenes", "_chair_phone"), ("dh_scenes", "_arm_phone")]
LEAF = {("of_cast", "phone")}       # the phone body itself: gated whoever replaced it (One Star wraps it)
NOT_HELD = set()                    # call-site function names whose phone is not in a hand (falling, on a desk)
FAULTS = collections.Counter()
SEEN = collections.Counter()
_ON = [False]


def _in_v4c():
    """Innermost first: the old grip (of_cast.phone_grip itself) before any hands_v4 grip means the old drawing."""
    f = sys._getframe(2)
    while f is not None:
        fn, name = f.f_code.co_filename, f.f_code.co_name
        if fn.endswith("of_cast.py") and name == "phone_grip":
            return False
        if fn.endswith("hands_v4.py") and name in ("_v4c_any", "phone_grip"):
            return True
        f = f.f_back
    return False


def _site():
    for fr in reversed(traceback.extract_stack()[:-3]):
        if not fr.filename.endswith(("phone_gate.py", "hands_v4.py", "of_cast.py")) or fr.name not in ("phone", "phone_grip"):
            return "%s:%d %s" % (fr.filename.rsplit("/", 1)[-1], fr.lineno, fr.name), fr.name
    return "?", "?"


def _wrap(mod, name, fn):
    def w(*a, **kw):
        if _ON[0]:
            site, fname = _site()
            SEEN[site] += 1
            if fname not in NOT_HELD and not _in_v4c():
                FAULTS["%s.%s from %s" % (mod, name, site)] += 1
        return fn(*a, **kw)
    w._gate = fn
    return w


def install(mods=None):
    """Wrap every painter whose module is loaded (or importable)."""
    import importlib
    for mod, name in PAINTERS:
        if mods is not None and mod not in mods:
            continue
        try:
            m = importlib.import_module(mod)
        except Exception:
            continue
        fn = getattr(m, name, None)
        if fn is None or hasattr(fn, "_gate") or (getattr(fn, "__module__", mod) != mod and (mod, name) not in LEAF):
            continue                                    # replaced by a film's own drawer: what it paints is gated below it
        setattr(m, name, _wrap(mod, name, fn))
    _ON[0] = True


def report(out=print):
    out("phone gate: %d faults at %d sites (%d phone drawings seen)" % (sum(FAULTS.values()), len(FAULTS), sum(SEEN.values())))
    for site, n in FAULTS.most_common():
        out("  FAIL %s  x%d" % (site, n))
    return not FAULTS


def selftest():
    """A planted old grip must fail; a v4c grip must pass."""
    import kit
    import cairo
    import hands_v4
    import of_cast as oc
    hands_v4.enable(phone="v4c")
    hands_v4.ALL_V4C[0] = True
    install(["of_cast"])
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, 200, 200)
    k = kit.Ctx(cairo.Context(surf), 0) if hasattr(kit, "Ctx") else None
    if k is None:
        import of_scenes
        k = of_scenes.Ctx(cairo.Context(surf), 0)
    FAULTS.clear()
    oc.phone_grip(k, 100, 120, 1.0, None, body_x=200)              # the canon: must pass
    ok_pass = not FAULTS
    hands_v4._ORIG["phone_grip"](k, 100, 120, 1.0, None, body_x=200)   # planted: the old grip, directly
    ok_fail = bool(FAULTS)
    FAULTS.clear(); SEEN.clear()
    return ok_pass and ok_fail


if __name__ == "__main__":
    print("phone gate selftest:", "PASS" if selftest() else "FAIL")
