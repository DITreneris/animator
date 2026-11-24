"""DADDY'S HOME: the regression guard for the restaging. The approved animation v7 must keep drawing exactly as it
does: three drawings of every shot (first, middle, last), with their bubbles, hashed.
  python3 dh_baseline.py save 1 2 ...   -> ../daddys-home/dh_v7_baseline.json (the scenes named; merged into the file)
  python3 dh_baseline.py check [1 2 ...] -> exit 1 and the shots that differ, if v7 no longer draws the same
New work goes in new files and behind flags (dh_film_v8 and on); this check is run before every send."""
import sys
import json
import hashlib
import os

PATH = os.environ.get("DH_BASE", "../daddys-home/dh_v7_baseline.json")


def hashes(n):
    import dh_say as SY
    SY.install()
    import dh_scenes as ds
    if n <= 3:
        import dh_anim1, dh_anim2, dh_anim3
        m = {1: dh_anim1, 2: dh_anim2, 3: dh_anim3}[n]; frame, R, T0, total = m.frame, m.ROWS, m.T0, m.TOTAL
        ds.ARM_PHONE[0] = n != 1
    else:
        m = __import__("dh_anim%d" % n); frame, R, T0, total = m.sc.frame, m.sc.rows, m.sc.T0, m.sc.total
        ds.ARM_PHONE[0] = m.sc.phone
    SY.plan_scene(lambda tt, k: frame(tt, k, 1), total)
    out = {}
    for sid, d in R:
        for tag, tt in (("a", T0[sid] + 0.02), ("m", T0[sid] + d / 2.0), ("z", T0[sid] + d - 0.05)):
            s = frame(tt, int(tt * 30), 1)[0]; s.flush()
            out["%d|%s|%s" % (n, sid, tag)] = hashlib.md5(bytes(s.get_data())).hexdigest()
    return out


if __name__ == "__main__":
    mode, scenes = sys.argv[1], [int(a) for a in sys.argv[2:]] or list(range(1, 9))
    old = json.load(open(PATH)) if os.path.exists(PATH) else {}
    bad = []
    for n in scenes:
        h = hashes(n)
        if mode == "save":
            old.update(h); json.dump(old, open(PATH, "w"), indent=0, sort_keys=True)
            print("scene", n, "saved", len(h), flush=True)
        else:
            d = [k for k, v in h.items() if old.get(k) != v]
            bad += d
            print("scene", n, "same" if not d else "DIFFERENT: %s" % " ".join(d), flush=True)
    sys.exit(1 if bad else 0)
