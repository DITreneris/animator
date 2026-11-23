"""ONE STAR (episode 11): the whole film from the six scenes (cs_scene1..6, each already rendered at 1080) with one
sound track: the fourteen lines on each scene's own clock, the phones' buzz, effects (cs_sfx), and, v3 (Tomas, 21 Nov,
choice A), the office music of episode 9: sparse vibes, chords only (sound_ob_music, bed A), ducked under every line.
The music is cut three times and comes back three times:
  0:00  the phones' buzz cuts it dead (the film's end runs into this: the loop);  back on Don's "Approved." (1.4)
  3.5   dead on "Is this a joke?";  back with one warm chord as the 7 goes into the gap (4.3b)
  6.5   out for "Still one star.";  back for Don puffing up, into the loop
Stereo: voices and effects in the middle, the vibes spread. Video is copied, never encoded twice.
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
# v3: the pass for what was still mute (Tomas: "are the effects enough, what to add")
FX += [("1.2", d, fx.pop(520 + 40 * i), 0.10) for i, d in enumerate((4, 9, 13, 18, 26, 36))]       # the reactions landing
FX += [("1.4", d, fx.key(), 0.14) for d in (4, 6, 8, 10, 12)]                                     # REPLY types on its visor
FX += [("1.4", 36, fx.pop(880), 0.14), ("3.1", 33, fx.pop(880), 0.14)]                            # its green tick
FX += [("2.2", 8, fx.pop(600), 0.12), ("2.2", 14, fx.pop(700), 0.12)]                             # 9:00, CLIENT fill in
FX += [("3.1", 31, fx.rustle(0.3), 0.20)]                                                         # the sheet curls on the floor
FX += [("3.2", 0, fx.door(0.5), 0.20), ("3.5", 17, fx.step(), 0.22)]                              # the door; he turns to go
FX += [("4.1", 12, fx.key(), 0.20), ("4.2b", 3, fx.whoosh(0.22), 0.14)]                           # her glasses; her arm
FX += [("4.3c", 5, fx.rustle(0.18), 0.20)]                                                        # the strip turned to us
FX += [("4.4", 0, fx.sweep(600, 200, 0.45), 0.10)]                                                # its visor dims: power down
FX += [("5.1", 8, fx.whoosh(0.22), 0.12)]                                                         # his phone comes up
FX += [("6.1", d, fx.key(), 0.14) for d in (1, 3, 4, 6, 9, 10)]                                   # he types at the door
FX += [("6.2", 4, fx.scratch(0.25), 0.18)]                                                        # the strike-through
FX += [("6.3", 16, fx.rustle(0.15), 0.14), ("6.6a", 8, fx.tap(220), 0.18)]                        # the corner lifted; his vest
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
    # ---- the music (v3) ----
    import sound_ob_music as om
    import sound_iwry as si
    L = len(a)
    at = lambda shot, d: (start[shot] + d) / float(DPS)
    line = dict((k, t) for k, t, _ in lines)
    bars = 8 * max(1, int(round(total / 3.1 / 8)))
    bl, br_, bar = om.bed(L / float(SR), bars, "A")
    env = si.lp(np.abs(voice / max(1e-9, np.abs(voice).max()) * 0.7), int(0.06 * SR))
    duck = si.lp(1 - 0.6 * np.clip(env / 0.05, 0, 1), int(0.08 * SR))
    la = int(0.25 * SR)
    duck = si.lp(np.minimum(duck, np.concatenate([duck[la:], np.ones(la)])), int(0.05 * SR))
    gate = np.ones(L)
    CUTS = [(0.05, line["1.4d"] + 0.05), (line["3.5"] - 0.04, at("4.3b", 16)), (at("6.5", 0), line["6.5"] + 0.875 + 0.25)]
    for t0, t1 in CUTS:
        i0, i1 = int(t0 * SR), int(t1 * SR)
        gate[i0:i1] = 0.0
        n_ = int(0.012 * SR); gate[max(0, i0 - n_):i0] = np.linspace(1, 0, n_)[-(i0 - max(0, i0 - n_)):] if i0 else gate[0:0]
        m_ = int(0.35 * SR); gate[i1:i1 + m_] = np.linspace(0, 1, m_)[:max(0, min(m_, L - i1))]
    g = om.GAIN["A"] * 1.35
    ml, mr = bl[:L] * duck * gate * g, br_[:L] * duck * gate * g
    t7 = at("4.3b", 16)                                                            # the 7 goes in: one warm chord (Cmaj9)
    for i, m in enumerate((60, 64, 67, 71, 74)):
        x = om.vibe(m, 2.6) * (0.9 - 0.08 * i) * 0.085
        p = int((t7 + i * 0.045) * SR); pan = 0.34 + 0.08 * i
        ml[p:p + len(x)] += x[:L - p] * (1 - pan); mr[p:p + len(x)] += x[:L - p] * pan
    talk = env > 0.02
    db = lambda x: 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)
    vox = voice / max(1e-9, np.abs(voice).max()) * 0.7
    print("music: %d bars, %.1f bpm, voice over music %.1f dB, cuts %s" % (
        bars, 240 / bar, db(vox[talk]) - db(((ml + mr) / 2)[talk] + 1e-9), [(round(x, 2), round(y, 2)) for x, y in CUTS]))
    st = np.stack([a + ml, a + mr], axis=1)
    sf.write(tmp + "/a.wav", (st / max(1.0, np.abs(st).max() / 0.9)).astype(np.float32), SR)
    with open(tmp + "/list.txt", "w") as f:
        f.write("".join("file '%s'\n" % v for v in vids))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", tmp + "/list.txt", "-an", "-c:v", "copy",
                    tmp + "/v.mp4"], check=True)
    r_ = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", tmp + "/a.wav", "-af", "ebur128", "-f", "null", "-"],
                        capture_output=True, text=True)
    cur = float([x for x in r_.stderr.split("\n") if "I:" in x][-1].split("I:")[1].split("LUFS")[0])
    out = os.path.join(out_dir, "one_star_%s.mp4" % tag)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp + "/v.mp4", "-i", tmp + "/a.wav", "-map", "0:v", "-map", "1:a",
                    "-af", "volume=%.2fdB,alimiter=limit=0.56:attack=1:release=60:level=disabled" % (-11.6 - cur),
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart",
                    tmp + "/o.part.mp4"], check=True)
    os.replace(tmp + "/o.part.mp4", out)
    json.dump({"total": round(total, 3),
               "shots": [{"shot": k, "line": {"key": k, "who": meta[k]["who"], "text": meta[k]["text"], "t0": round(t, 3),
                                              "t1": round(t + meta[k]["len"], 3)}} for k, t, _ in lines]},
              open("one_star_%s_timing.json" % tag, "w"), indent=1)
    print("wrote", out, "%d drawings, %.2f s, %d lines, %d effects" % (n, total, len(lines), len(FX)))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "../customer-success", sys.argv[2] if len(sys.argv) > 2 else "rough_v3")
