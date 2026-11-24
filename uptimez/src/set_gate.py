"""The set gate (24 Nov, Tomas: "darom ir padarom scenos gates, kad isimintu").

Daddy's Home v8 scene 3 moved the throne between shots (404 in 3E, 540 in 3F; the set has it at 452) and put Sofia
"behind" Mom on the same floor line, so she was neither behind nor beside her: a floating head. Nothing measured the
staging against the set, so nothing stopped it. This gate does, on every drawing:

  1. A set prop off its mark (`PROPS`, from series/front-desk-set.md), unless the episode lists the move.
  2. Two people whose figures overlap on screen with their feet on the same floor line (within `SAME_LINE`): one of
     them must stand further back (feet higher) to be "behind".
  3. A person who is somewhere else after a cut (more than `CUT_JUMP` world units), unless the episode lists the walk.
  4. A person whose feet are above the floor line (the wall's foot, F): standing on the wall. Off the floor on purpose
     (a leap: `air`) or behind something that hides the feet (the counter: `behind`) is listed by the episode.

It logs the draw calls themselves (the rigs' and props' own functions, wrapped), so it sees what was drawn, in world
units. Use: `install()` once; `begin(sid)` before each drawing; `faults()` after it; `cut_faults()` at the end.
A change to the set is made in series/front-desk-set.md first, then in `PROPS` here.
"""
import math

F = 800
PROPS = {"throne": (452, F + 8, 0.60)}          # front-desk-set.md v5: the CEO chair on Don's mark, zone B
SAME_LINE = 12                                  # feet closer than this (world units) are one floor line
CUT_JUMP = 40                                   # a person further than this from where he was before the cut has moved
FLOOR_TOL = 2                                   # feet this far above the wall's foot still stand on the floor
WIDTH = 130                                     # a person's width in world units at scale 1, hair and arms (for "overlap on screen")

LOG = []                                        # this drawing: (kind, name, x, feet, s)
SEQ = []                                        # every drawing: (sid, [(kind, name, x, feet, s)])
_INSTALLED = [False]


def _wrap(mod, fn_name, kind, name, xi=1, fi=2, si=3, s_default=1.0):
    real = getattr(mod, fn_name)
    if getattr(real, "_set_gate", False):
        return

    def logged(*a, **kw):
        try:
            x, feet = float(a[xi]), float(a[fi])
            s = float(a[si]) if len(a) > si else float(kw.get("s", kw.get("cs", s_default)))
            LOG.append((kind, name, x, feet, s))
        except Exception:
            pass
        return real(*a, **kw)
    logged._set_gate = True
    logged._real = real                         # for measuring passes on a scratch surface (not part of the drawing)
    setattr(mod, fn_name, logged)


def install():
    """Wrap the series' rigs and set props (each is logged once per call, in world units)."""
    if _INSTALLED[0]:
        return
    import dh_props, mom_fs, pam_bc, sofia_cs, fs_storyboard, dh_cast
    _wrap(dh_props, "ceo_chair", "prop", "throne")
    _wrap(fs_storyboard, "don", "person", "don")
    _wrap(dh_cast, "repairman", "person", "visitor")
    _wrap(mom_fs, "mom", "person", "mom")
    _wrap(pam_bc, "pam", "person", "pam")
    _wrap(sofia_cs, "sofia", "person", "sofia")
    _INSTALLED[0] = True


def begin(sid):
    del LOG[:]
    SEQ.append((sid, LOG))


def end():
    """Keep this drawing's log (begin() starts a new list for the next)."""
    if SEQ:
        sid, _ = SEQ[-1]
        SEQ[-1] = (sid, list(LOG))


def faults(sid=None, log=None, moves=(), air=(), behind=()):
    """This drawing's faults. moves: {(sid, prop): max distance} a prop may travel from its mark in that shot (a roll,
    a jolt). air: {(sid, person)} a person off the floor on purpose (a jump)."""
    log = LOG if log is None else log
    moves = dict(moves)
    out = []
    for kind, name, x, feet, s in log:
        if kind == "prop" and name in PROPS:
            px, pf, ps_ = PROPS[name]
            d = math.hypot(x - px, feet - pf)
            if d > moves.get((sid, name), 4) or abs(s - ps_) > 0.02:
                out.append("SET %s off its mark (%d, %d, %.2f): at (%d, %d, %.2f)" % (name, px, pf, ps_, x, feet, s))
    people = [(n, x, f, s) for k, n, x, f, s in log if k == "person"]
    for n, x, f, s in people:                   # 24 Nov (Tomas: "is she pinned to the wall?"): 3F Sofía at F-40
        if f < F - FLOOR_TOL and (sid, n) not in air and (sid, n) not in behind:
            out.append("FLOOR %s's feet at %d, above the floor line (%d): standing on the wall" % (n, f, F))
    seen = {}
    for n, x, f, s in people:                   # a rig drawn twice in one drawing (an iso redraw) is one person
        seen.setdefault(n, (n, x, f, s))
    people = list(seen.values())
    for i in range(len(people)):
        for j in range(i + 1, len(people)):
            a, b = people[i], people[j]
            if (sid, a[0]) in air or (sid, b[0]) in air:
                continue
            overlap = abs(a[1] - b[1]) < 0.5 * WIDTH * (a[3] + b[3])
            if overlap and abs(a[2] - b[2]) < SAME_LINE:
                out.append("DEPTH %s and %s overlap on one floor line (feet %d, %d): one must stand further back"
                           % (a[0], b[0], a[2], b[2]))
    return list(dict.fromkeys(out))             # a prop drawn twice in one drawing (an iso redraw) is one fault


def cut_faults(seq=None, walks=()):
    """People who are elsewhere after a cut. walks: {(sid_before, sid_after, person)} a walk the cut hides on purpose."""
    seq = SEQ if seq is None else seq
    out = []
    last = {}                                   # person -> (sid, x, feet) at his last drawing
    prev_sid = None
    for sid, log in seq:
        here = {}
        for k, n, x, f, s in log:
            if k == "person":
                here.setdefault(n, (x, f))
        if prev_sid is not None and sid != prev_sid:
            for n, (x, f) in here.items():
                if n in last and last[n][0] == prev_sid and (prev_sid, sid, n) not in walks:
                    if math.hypot(x - last[n][1], f - last[n][2]) > CUT_JUMP:
                        out.append("CUT %s -> %s: %s moved from (%d, %d) to (%d, %d)" % (prev_sid, sid, n, last[n][1], last[n][2], x, f))
        for n, (x, f) in here.items():
            last[n] = (sid, x, f)
        prev_sid = sid
    return out


def selftest():
    """Each planted fault must fail; the set as written must pass."""
    ok = [("prop", "throne", 452, 808, 0.60), ("person", "mom", 300, 808, 0.54), ("person", "sofia", 400, 804, 0.56)]
    assert not faults("x", ok), faults("x", ok)
    bad_throne = [("prop", "throne", 540, 808, 0.60)]
    assert faults("x", bad_throne) and faults("x", bad_throne)[0].startswith("SET")
    assert not faults("x", [("prop", "throne", 460, 808, 0.60)], moves={("x", "throne"): 10})
    same_line = [("person", "mom", 446, 808, 0.54), ("person", "sofia", 410, 804, 0.56)]   # v8 round 7, 3F
    assert any(f.startswith("DEPTH") for f in faults("3F", same_line))
    behind = [("person", "mom", 446, 808, 0.54), ("person", "sofia", 410, 776, 0.50)]
    assert [f for f in faults("3F", behind) if f.startswith("FLOOR")]          # "behind" her, but on the wall (round 9)
    deeper = [("person", "mom", 446, 830, 0.54), ("person", "sofia", 410, 804, 0.50)]
    assert not faults("3F", deeper)                                            # behind her on the floor: further back, still on it
    assert not faults("4D", [("person", "pam", 692, 728, 0.5)], behind={("4D", "pam")})   # at her counter: feet hidden
    assert not faults("J", same_line, air={("J", "sofia")})
    seq = [("3E", [("person", "mom", 300, 808, 0.54)]), ("3F", [("person", "mom", 446, 808, 0.54)])]   # v8: 300 -> 446
    assert cut_faults(seq) and cut_faults(seq)[0].startswith("CUT")
    assert not cut_faults(seq, walks={("3E", "3F", "mom")})
    assert not cut_faults([("3E", [("person", "mom", 300, 808, 0.54)]), ("3F", [("person", "mom", 310, 808, 0.54)])])
    return True


if __name__ == "__main__":
    print("set_gate selftest ok" if selftest() else "FAIL")
