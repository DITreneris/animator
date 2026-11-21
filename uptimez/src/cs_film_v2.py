"""ONE STAR (episode 11): the whole film from the six scenes (cs_scene1..6, each already rendered at 1080) with one
sound track: the fourteen lines on each scene's own clock, the phones' buzz, and effects under the wordless
stretches (cs_sfx). Video is copied, never encoded twice.
  python3 cs_film.py [out_dir] [tag]  ->  one_star_<tag>.mp4, one_star_<tag>_timing.json"""
import importlib
import json
import os
import subprocess
import sys
import numpy as np
import soundfile as sf
import cs_sfx as fx
import cs_animatic as an

SR, DPS = 48000, 12
MODS = ["cs_scene%d" % i for i in range(1, 7)]
T = lambda shot, d: (shot, d)

# (shot, drawing in the shot, effect, gain)
FX = [
    ("1.4", 34, fx.tap(), 0.30), ("1.4b", 3, fx.tap(420), 0.22),
    ("2.1a", 0, fx.ring(), 0.14), ("2.1", 10, fx.tap(300), 0.20), ("2.2", 23, fx.beep(), 0.12),
    ("3.1", 4, fx.whirr(2.3), 0.10), ("3.3", 0, fx.rustle(0.45), 0.30), ("3.5b", 2, fx.tap(260), 0.25),
    ("4.2", 1, fx.rustle(0.25), 0.22), ("4.2", 5, fx.rustle(0.25), 0.22), ("4.2", 9, fx.rustle(0.75), 0.32),
    ("4.3a", 3, fx.rustle(0.22), 0.25), ("4.3c", 1, fx.whoosh(0.3), 0.20), ("4.3b", 2, fx.rustle(0.5), 0.28),
    ("4.3b", 16, fx.tap(), 0.25), ("4.3b", 19, fx.tape(0.35), 0.18), ("4.4", 4, fx.whoosh(0.3), 0.22),
    ("5.2", 3, fx.scratch(0.36), 0.22), ("5.2", 8, fx.scratch(0.78), 0.22), ("5.2", 21, fx.rustle(0.3), 0.18),
    ("5.3", 14, fx.tap(420), 0.22), ("5.3", 15, fx.chime(), 0.16), ("5.4b", 16, fx.tap(300), 0.22),
    ("6.3", 7, fx.tap(), 0.26), ("6.3b", 3, fx.tap(420), 0.20), ("6.5", 1, fx.whoosh(0.25), 0.18),
]
FX += [("3.2", d, fx.step(), 0.22) for d in range(0, 24, 3)]
FX += [("4.1", d, fx.step(), 0.22) for d in (0, 3, 5)]
FX += [("5.1", d, fx.step(), 0.20) for d in (0, 2, 5)]
FX += [("3.4", int(round(i * 15 / 12.0)), fx.key(), 0.22) for i in range(12)]
FX += [("5.3", d, fx.key(), 0.20) for d in range(3, 12)]
FX += [("6.2", d, fx.key(), 0.20) for d in range(4, 13)]
BUZZ = [("1.1", 0.05, 1.15, 0.7), ("6.3", 0.0, 0.35, 0.35), ("6.3", 0.75, 0.25, 0.25), ("6.6a", 0.0, 0.45, 0.5)]


def main(out_dir, tag):
    start, lines, vids, n = {}, [], [], 0
    for mn in MODS:
        m = importlib.import_module(mn)
        t0 = n / float(DPS)
        for key, t in m.schedule():
            lines.append((key, t0 + t, m.TAKES))
        for shot, nd, _ in m.SHOTS:
            start[shot] = n; n += nd
        vids.append(os.path.abspath(os.path.join(out_dir, "%s_%s.mp4" % (mn, m.V.split()[0]))))
    total = n / float(DPS)
    a = np.zeros(int((total + 0.2) * SR))

    def put(x, t, g=1.0):
        p = int(t * SR)
        if p < len(a):
            a[p:p + len(x)] += g * x[:len(a) - p]
    meta = json.load(open(lines[0][2] + "/takes.json"))
    voice = np.zeros_like(a)
    for key, t, takes in lines:
        x, _ = sf.read("%s/%s.wav" % (takes, key))
        p = int(t * SR); voice[p:p + len(x)] += x[:len(voice) - p]
    a += voice / max(1e-9, np.abs(voice).max()) * 0.7
    for shot, d, x, g in FX:
        put(x, (start[shot] + d) / float(DPS), g * 0.6)
    for shot, off, ln, g in BUZZ:
        put(an.buzz(ln), start[shot] / float(DPS) + off, g * 0.7)
    tmp = "/tmp/cs_film"; os.makedirs(tmp, exist_ok=True)
    sf.write(tmp + "/a.wav", (a / max(1.0, np.abs(a).max() / 0.9)).astype(np.float32), SR)
    with open(tmp + "/list.txt", "w") as f:
        f.write("".join("file '%s'\n" % v for v in vids))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", tmp + "/list.txt", "-an", "-c:v", "copy",
                    tmp + "/v.mp4"], check=True)
    r_ = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", tmp + "/a.wav", "-af", "ebur128", "-f", "null", "-"],
                        capture_output=True, text=True)
    cur = float([x for x in r_.stderr.split("\n") if "I:" in x][-1].split("I:")[1].split("LUFS")[0])
    out = os.path.join(out_dir, "one_star_%s.mp4" % tag)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp + "/v.mp4", "-i", tmp + "/a.wav", "-map", "0:v", "-map", "1:a",
                    "-af", "volume=%.2fdB,alimiter=limit=0.60:attack=1:release=60:level=disabled" % (-11.0 - cur),
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart",
                    tmp + "/o.part.mp4"], check=True)
    os.replace(tmp + "/o.part.mp4", out)
    json.dump({"total": round(total, 3),
               "shots": [{"shot": k, "line": {"key": k, "who": meta[k]["who"], "text": meta[k]["text"], "t0": round(t, 3),
                                              "t1": round(t + meta[k]["len"], 3)}} for k, t, _ in lines]},
              open("one_star_%s_timing.json" % tag, "w"), indent=1)
    print("wrote", out, "%d drawings, %.2f s, %d lines, %d effects" % (n, total, len(lines), len(FX)))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "../customer-success", sys.argv[2] if len(sys.argv) > 2 else "rough_v2")
