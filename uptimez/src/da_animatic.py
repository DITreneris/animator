"""THE DOUBLE AGENT (episode 15): the animatic v1 (27 Nov; Tomas /grill-me: key poses on the timing, no in-betweens;
the effects already in; 15 drawings a second for the film later, 30 fps camera).

Every shot of the scene file (da_scenes.ORDER) is its layout key pose (da_layouts.render, the same drawing as the
sheets, without the sheet's text), held for its length from da_timing_v4.json; the sound is the recorded voices v4
(da_voices.timing) plus the effects each shot's `sound` field names, synthesized here and cued at the shot's start.

  python3 da_animatic.py [out_dir]   ->  da_animatic_v2.mp4 (v1: 27 Nov, 42 shots) (540x960, 30 fps; not committed, .gitignore)

The loop: the last shot (9.1) ends where 1.1 starts; the room tone runs through the seam (no dead stop).
"""
import json
import os
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.join(HERE, "..", "the-double-agent")
FPS, SR = 30, 48000
RNG = np.random.default_rng(15)


# ---- effects: small synthesized sounds, named by the words in the scene file's `sound` field --------------------------
def _env(n, a=0.004, d=0.08):
    t = np.arange(n) / SR
    return np.minimum(1, t / a) * np.exp(-t / d)


def _noise(sec):
    return RNG.standard_normal(int(sec * SR))


def _lp(x, k):
    return np.convolve(x, np.ones(k) / k, mode="same")


def _tone(f, sec, d=0.06, a=0.002):
    n = int(sec * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * f * t) * _env(n, a, d)


def _sweep(f0, f1, sec, d=0.2):
    n = int(sec * SR); t = np.arange(n) / SR
    ph = 2 * np.pi * (f0 * t + (f1 - f0) * t * t / (2 * sec))
    return np.sin(ph) * _env(n, 0.005, d)


def squeak():
    return seq((0, 0.5 * _sweep(1900, 2700, 0.14, 0.08)), (0, 0.3 * _sweep(2300, 1800, 0.12, 0.06)))


def click(f=2400, d=0.012):
    n = int(0.05 * SR)
    return _tone(f, 0.05, d)[:n] + 0.3 * _lp(_noise(0.05), 3)[:n] * _env(n, 0.001, 0.008)


def thud(f=70):
    n = int(0.35 * SR)
    return _tone(f, 0.35, 0.12, 0.003)[:n] + 0.2 * _lp(_noise(0.35), 40)[:n] * _env(n, 0.002, 0.05)


def noise_burst(sec, k, d):
    return _lp(_noise(sec), k) * _env(int(sec * SR), 0.004, d)


def beep():
    return 0.6 * _tone(1000, 0.16, 0.5, 0.004) * (np.arange(int(0.16 * SR)) < 0.14 * SR)


def pings(n, lo=2500, hi=5200, span=0.35):
    out = np.zeros(int((span + 0.1) * SR))
    for _ in range(n):
        i = int(RNG.uniform(0, span) * SR); w = _tone(RNG.uniform(lo, hi), 0.08, 0.02)
        out[i:i + len(w)] += 0.5 * w[:len(out) - i]
    return out


def heels(n=2, gap=0.32):
    out = np.zeros(int((n * gap + 0.2) * SR))
    for j in range(n):
        w = click(900, 0.02)
        i = int(j * gap * SR); out[i:i + len(w)] += w[:len(out) - i]
    return out


def seq(*parts):
    """(offset_s, sound) pairs into one buffer."""
    n = max(int(o * SR) + len(w) for o, w in parts)
    out = np.zeros(n)
    for o, w in parts:
        i = int(o * SR); out[i:i + len(w)] += w
    return out


FX = [  # (word in the sound field, the sound): first match wins per phrase
    ("casters squeak", lambda: seq((0, squeak()), (0.28, squeak()))),
    ("casters", lambda: seq((0, squeak()), (0.22, squeak()), (0.44, squeak()))),
    ("squeaks of the tug", lambda: 0.5 * seq((0, squeak()), (0.3, squeak()))),
    ("tug's squeak", lambda: seq((0, 0.4 * squeak()), (0.3, 0.7 * squeak()), (0.6, squeak()))),
    ("thk", lambda: click(500, 0.02)),
    ("thwack", lambda: seq((0, 0.8 * noise_burst(0.12, 6, 0.03)), (0, thud(110)))),
    ("slow heels", lambda: heels(3, 0.42)),
    ("heels", lambda: heels(2, 0.3)),
    ("border beep", beep),
    ("tag flick", lambda: noise_burst(0.06, 2, 0.01)),
    ("clatter", lambda: pings(9)),
    ("tik", lambda: _tone(5200, 0.05, 0.01)),
    ("rip", lambda: noise_burst(0.35, 2, 0.2) * np.abs(np.sin(np.linspace(0, 40, int(0.35 * SR))))),
    ("thud", thud),
    ("creak", lambda: 0.4 * _sweep(180, 140, 0.4, 0.3)),
    ("clack", lambda: click(1200, 0.02)),
    ("vest snap", lambda: noise_burst(0.07, 3, 0.015)),
    ("shatter", lambda: seq((0, noise_burst(0.3, 1, 0.08)), (0, pings(12, 3000, 7000, 0.25)))),
    ("pour", lambda: 0.5 * noise_burst(0.7, 25, 0.6)),
    ("door", lambda: seq((0, click(700, 0.03)), (0.05, 0.6 * thud(90)))),
    ("chair scrape", lambda: 0.4 * noise_burst(0.3, 12, 0.2)),
    ("swishes", lambda: seq((0, 0.4 * noise_burst(0.15, 6, 0.08)), (0.3, 0.4 * noise_burst(0.15, 6, 0.08)))),
    ("shoe squeaks", lambda: seq((0, 0.6 * _sweep(2600, 3400, 0.09, 0.06)), (0.35, 0.6 * _sweep(2600, 3400, 0.09, 0.06)))),
    ("needles", lambda: seq(*[(0.12 * j, 0.3 * _tone(4200, 0.03, 0.006)) for j in range(4)])),
    ("wipe squeak", lambda: 0.4 * _sweep(1500, 2100, 0.25, 0.2)),
    ("cup on saucer", lambda: 0.6 * _tone(2600, 0.15, 0.05)),
    ("quiet steps", lambda: 0.4 * heels(3, 0.25)),
    ("rattle", lambda: seq(*[(0.05 * j, 0.25 * _tone(2800 + 200 * (j % 2), 0.03, 0.008)) for j in range(8)])),
    ("slurp", lambda: 0.4 * noise_burst(0.3, 30, 0.25)),
    ("skid", lambda: 0.5 * _lp(_noise(0.4), 4) * _env(int(0.4 * SR), 0.01, 0.3)),
    ("cup clink", lambda: 0.5 * _tone(3100, 0.1, 0.04)),
    ("skrrt", lambda: seq((0, 0.6 * _lp(_noise(0.3), 3) * _env(int(0.3 * SR), 0.005, 0.2)), (0.32, thud(80)))),
    ("splash", lambda: 0.7 * noise_burst(0.25, 10, 0.1)),
    ("paper slide", lambda: 0.35 * noise_burst(0.35, 4, 0.25)),
    ("paper", lambda: 0.35 * noise_burst(0.15, 3, 0.08)),
    ("mic tap", lambda: 0.6 * thud(160)),
    ("long peel", lambda: 0.4 * noise_burst(0.6, 2, 0.5) * np.linspace(0.3, 1, int(0.6 * SR))),
    ("pen", lambda: seq(*[(0.06 * j, 0.15 * noise_burst(0.04, 2, 0.02)) for j in range(5)])),
]


def effects(sound):
    """the effect buffers a shot's `sound` field asks for, each with its offset in the shot (in order, 0.12 s in)."""
    out, t, low = [], 0.12, sound.lower()
    for phrase in low.replace(";", ",").replace("→", ",").split(","):
        for word, fn in FX:
            if word in phrase:
                w = fn(); out.append((t, w)); t += len(w) / SR + 0.05
                break
    return out


# ---- picture and sound -------------------------------------------------------------------------------------------------
def build(out_dir=EP):
    sys.path.insert(0, HERE)
    import da_layouts as L
    tm = json.load(open(os.path.join(EP, "da_timing_v4.json")))
    tmp = "/tmp/da_animatic"; os.makedirs(tmp, exist_ok=True)
    lst, total_f = [], 0
    for i, s in enumerate(tm["shots"]):
        surf, msgs = L.render(s["shot"])
        png = os.path.join(tmp, "%02d_%s.png" % (i, s["shot"]))
        surf.write_to_png(png)
        end_f = int(round((s["start"] + s["len"]) * FPS))
        n = end_f - total_f; total_f = end_f
        lst.append((png, n))
    with open(os.path.join(tmp, "list.txt"), "w") as f:
        for png, n in lst:
            f.write("file '%s'\nduration %.6f\n" % (png, n / FPS))
        f.write("file '%s'\n" % lst[-1][0])
    # the voices: v4's mix, read back as samples
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(EP, "da_voices_v4.mp4"), "-f", "f32le", "-ac", "1",
                          "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    voice = np.frombuffer(raw, dtype=np.float32).astype(np.float64)
    n = int(total_f / FPS * SR)
    mix = np.zeros(n); mix[:min(n, len(voice))] += voice[:n]
    tone = 0.004 * _lp(_noise(n / SR + 0.1), 200)[:n]                    # the room tone, through the seam
    mix += tone
    cues = []
    for s in tm["shots"]:
        rec = __import__("da_scenes").TEXT[s["shot"]]
        for off, w in effects(rec["sound"]):
            i = int((s["start"] + off) * SR)
            g = 0.18 / (np.max(np.abs(w)) + 1e-9)                          # effects under the voices
            mix[i:i + len(w)] += g * w[:max(0, n - i)]
            cues.append((s["shot"], round(s["start"] + off, 2)))
    mix /= max(1.0, np.max(np.abs(mix)) / 0.89)
    wav = os.path.join(tmp, "mix.f32")
    mix.astype(np.float32).tofile(wav)
    out = os.path.join(out_dir, "da_animatic_v2.mp4")   # v2 28 Nov: 3.4b, 7.1 cut; 7.2 the close bow
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(tmp, "list.txt"),
                    "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", wav,
                    "-vf", "fps=%d,format=yuv420p" % FPS, "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                    "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
                    "-af", "loudnorm=I=-15:TP=-1.5:LRA=11", "-ar", str(SR), "-c:a", "aac", "-b:a", "160k",
                    "-shortest", out], check=True)
    print("wrote %s: %d frames (%.2f s), %d effect cues" % (out, total_f, total_f / FPS, len(cues)))
    return out, cues


if __name__ == "__main__":
    build(*sys.argv[1:])
