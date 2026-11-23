"""Validate uz_check on failures we really had (series/production-process.md: a check counts only once it has caught a
known failure). Each case renders a few shots of a First Search film version at 1080 in its own process, with the
recorder installed, and says what the check must do: FAIL on the version that had the fault, PASS on the version that
fixed it.

  python3 uz_check_validate.py <src dir with the First Search builders> [case ...]

The First Search builders v33-v37 live on the uptimez-first-search-script branch (v36, v37 in PR #62)."""
import json
import os
import pickle
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import uz_check as uz  # noqa: E402

# name: (film module, shots, check, must FAIL?, text that the failure must contain, what it is)
CASES = {
    "signs_v35": ("fs_film35", "B,L,E2,T2", "signs", True, "SIGN", "SHRE 0:06, DO 0:27, R FIR 0:29, T CLIENT 0:43"),
    "signs_v36": ("fs_film36", "B,L,E2,T2", "signs", False, None, "the same shots, fixed in v36"),
    "tails_v35": ("fs_film35", "B,C,D,F,X", "tails", True, "TAIL", "tails on hair, curls and crowns"),
    "tails_v36": ("fs_film36", "B,C,D,F,X", "tails", False, None, "tails beside the mouth"),   # see ALLOW
    "strays_v36": ("fs_film36", "O", "strays", True, "STRAY", "Mom's step dashes at 0:36"),
    "strays_v37": ("fs_film37", "O", "strays", False, None, "the dashes turned off"),
    "limbs_v36": ("fs_film36", "T2", "limbs", True, "LIMBS", "Pam's three arms at 0:42"),
    "limbs_v37": ("fs_film37", "T2", "limbs", False, None, "her right body arm clipped below the shoulders"),
    "text_v36": ("fs_film36", "B,L,E2,T2", "text", False, None, "the bubbles of four shots, where they were drawn"),
    "text_up": ("fs_film36", "B,L,E2,T2", "text", True, "TEXT", "the same bubbles pushed 140 px up, into the top bar"),
    "scale_v36": ("fs_film36", "B,L,E2,T2", "scale", False, None, "the faces of four shots, where they were framed"),
    "scale_low": ("fs_film36", "B,L,E2,T2", "scale", True, "SCALE", "the same shots, the camera 330 px higher"),
    "map_v33": ("fs_film33", "R", "map", True, "MAP", "the payoff drawn by film 4's show, not show19"),
    "map_v34": ("fs_film34", "R", "map", False, None, "show19 restored"),
}
# what a scene file declares itself (uz_check.limb / mark) and the old films did not: added from outside, per case
_WRITING_ARM = """
_ls = film.lipstick
def lipstick(c, x, y, ang, sc=1.0):
    if sc == 2.1:                                   # the writing hand in _stupidcu: fist at (x + 26, y + 56)
        uz.limb(c, "pam", (x + 26, y + 56))
    return _ls(c, x, y, ang, sc)
film.lipstick = lipstick
"""
# a fault made on purpose, where history has none: the drawing is the film's, moved the way the fault would move it
_BUBBLES_UP = """
_sp = film.an.speech
def speech(c, *a, **kw):
    c.save(); c.translate(0, -140)
    try:
        return _sp(c, *a, **kw)
    finally:
        c.restore()
film.an.speech = speech
"""
_CAMERA_HIGH = """
_mv = film.move
def move(*a, **kw):
    fx, fy, z = _mv(*a, **kw)
    return fx, fy - 330 / z, z
film.move = move
"""
FIXTURES = {"limbs_v36": _WRITING_ARM, "limbs_v37": _WRITING_ARM, "text_up": _BUBBLES_UP, "scale_low": _CAMERA_HIGH}
EXPECT_MAP = {"show": "show19"}
# a fault the checker found that the fixed version still has (not a false alarm): allowed by name in that case only
ALLOW = {"tails_v36": ("INTERFACE CHANGE",)}   # the robot's HR line: its tail ends left of its head at eye level, above
                                               # the mouth on its visor (seen in the v37 frame at 0:23.8); fix in v38

DRIVER = r'''
import os, sys, pickle
sys.path.insert(0, os.getcwd()); sys.path.append(%(here)r)
import uz_check as uz
import importlib
film = importlib.import_module(%(mod)r)
%(fixture)s
uz.install(film)
film.build(%(out)r, 2)
sys.setprofile(None)
pickle.dump(dict(frames=uz.R.frames, map=uz.R.map), open(%(pkl)r, "wb"))
'''


def record(src, mod, shots, fixture=""):
    keep = "/tmp/uzv_%s_%s%s.pkl" % (mod, shots.replace(",", ""), "_fx%x" % (hash(fixture) & 0xffff) if fixture else "")
    if os.path.exists(keep):
        return pickle.load(open(keep, "rb"))
    tmp = tempfile.mkdtemp(prefix="uzv_")
    pkl = os.path.join(tmp, "rec.pkl")
    env = dict(os.environ, FS_ONLY=shots)
    code = DRIVER % dict(here=HERE, mod=mod, out=tmp, pkl=pkl, fixture=fixture)
    r = subprocess.run([sys.executable, "-c", code], cwd=src, env=env, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("render failed: %s %s\n%s" % (mod, shots, r.stderr[-2000:]))
    d = pickle.load(open(pkl, "rb"))
    subprocess.run(["rm", "-rf", tmp, "/tmp/%s_1080" % mod])
    pickle.dump(d, open(keep, "wb"))
    return d


# the file that ships. The base is the First Search v37 copy as committed (540), scaled to 1080 and tagged bt709: its
# sound and its loop are the film's own. The faults are made from it.
_UP = "scale=1080:1920:flags=lanczos,setparams=colorspace=bt709:color_primaries=bt709:color_trc=bt709"
_TAGS = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709"]
FILM_CASES = {
    "film_v37": ([_UP], ["-c:a", "copy"], False, None, "v37 as shipped (scaled to 1080)"),
    "film_540": (["setparams=colorspace=bt709:color_primaries=bt709:color_trc=bt709"], ["-c:a", "copy"], True, "FORMAT",
                 "the 540 copy sent as the master"),
    "film_loud": ([_UP], ["-af", "volume=6dB", "-c:a", "aac", "-b:a", "192k"], True, "SOUND", "the mix 6 dB hot"),
    "film_seam": ([_UP], ["-c:a", "aac", "-b:a", "192k", "-t", "40"], True, "LOOP", "cut at 0:40: the last frame is not frame 0"),
    "film_untagged": (["scale=1080:1920:flags=lanczos"], ["-c:a", "copy", "-bsf:v",
                      "h264_metadata=colour_primaries=2:transfer_characteristics=2:matrix_coefficients=2"], True, "FORMAT",
                      "the colour tags left unspecified"),
}


def film_case(src, name):
    vf, extra, must_fail, needle, what = FILM_CASES[name]
    base = os.path.join(src, "..", "first-search", "fs_film37_540.mp4")
    out = "/tmp/uzv_film_%s.mp4" % name
    if not os.path.exists(out):
        tags = _TAGS if "colorspace" in vf[0] else []
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", base, "-vf", ",".join(vf), "-c:v", "libx264", "-preset", "veryfast",
                        "-crf", "18", "-pix_fmt", "yuv420p"] + tags + extra + [out], check=True)
    msgs, m = uz.check_film(out)
    failed = bool(msgs) and (needle is None or any(needle in q for q in msgs))
    return failed, must_fail, what, msgs, m


def main(src, names):
    rows, ok_all = [], True
    cache = {}
    for name in [n for n in (names or list(CASES) + list(FILM_CASES)) if n in FILM_CASES]:
        failed, must_fail, what, msgs, m = film_case(src, name)
        good = failed == must_fail
        ok_all &= good
        rows.append((name, what, "FAIL" if failed else "pass", "must fail" if must_fail else "must pass", "OK" if good else "WRONG",
                     m["frames"], msgs[:6]))
        print("%-11s %-46s %-4s (%s) %s  frames %d" % rows[-1][:6], flush=True)
        for q in msgs:
            print("      ", q[:150])
    for name in [n for n in (names or CASES) if n in CASES]:
        mod, shots, check, must_fail, needle, what = CASES[name]
        fx = FIXTURES.get(name, "")
        key = (mod, shots, fx)
        if key not in cache:
            cache[key] = record(src, mod, shots, fx)
        d = cache[key]
        if check == "map":
            msgs = uz.check_map(EXPECT_MAP, d["map"])
        else:
            msgs = [m for _, _, _, m in uz.run(d["frames"], only=[check], allow=ALLOW.get(name, ()))]
        failed = bool(msgs) and (needle is None or any(needle in m for m in msgs))
        good = failed == must_fail
        ok_all &= good
        uniq = sorted(set(msgs))
        rows.append((name, what, "FAIL" if failed else "pass", "must fail" if must_fail else "must pass",
                     "OK" if good else "WRONG", len(d["frames"]), uniq[:6]))
        print("%-11s %-46s %-4s (%s) %s  frames %d" % rows[-1][:6], flush=True)
        seen = set()
        for m in uniq:
            k = m.split(" at ")[0].split(" tip ")[0]
            if k not in seen:
                seen.add(k); print("      ", m[:150])
    json.dump(rows, open(os.path.join(HERE, "uz_check_validation.json"), "w"), indent=1)
    if not ok_all:
        print("VALIDATION FAILED: a check did not catch its known failure, or failed a fixed version")
        sys.exit(1)
    print("all checks behaved")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
