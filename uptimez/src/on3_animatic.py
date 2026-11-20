"""OFFICE NOIR 3: the animatic, v1 (20 Nov). The whole-film rough (film_on3 v7) with scratch voices and a few effects.
What it is for: the length with the lines in, whether each shot has room for its line, and how the lines sit on the
pictures. It is not the film's sound: no music, no room, no rain; the takes are first takes, not auditioned, and the
speech check has not been run on them. Voices are the series' own: the Client (and his narration) am_fenrir, four
semitones down (sound_ob.client_line); Mom voice F (sound_bc.mom); Pam key A (sound_xmas.pam_line); the Referee a
scratch British voice (bm_george).
Timing: a shot is held on its last drawing when its line needs longer; a line never starts before the one before it has
ended. Narration may run on over the next shot; a spoken line may not.
Writes  on3_voices/animatic_v1/*.wav, takes.json        the takes and their lengths
        on3_animatic_timing_v1.json                     every shot: start, length, lines; every effect
        ../office-noir-3/on3_animatic_v1.mp4            540 x 960, 30 fps, AAC
  KOKORO_DIR=/tmp/kokoro python3 on3_animatic.py"""
import json
import math
import os
import subprocess
import sys
import cairo
import numpy as np
import soundfile as sf

os.environ.setdefault("KOKORO_DIR", "/tmp/kokoro")
import sound_on as so
import sound_bc as bc
import sound_ob as sob
import sound_xmas as sx
import ring_rough_on3 as rr
import film_on3 as fm

V = "v1"
SR = so.SR
VOICES = "on3_voices/animatic_" + V
FPS = 30
GAP = 0.15

# shot -> [(who, line, take key, offset into the shot)]
LINES = {
    "2.0": [("N", "They say I know how business is done.", "n1", 0.0)],     # over the bill, after the punch (1.1 is 0.6 s)
    "2.1": [("N", "One fight.", "n2", 0.6)],
    "2.2": [("MOM", "Where are you going, skunk?", "m1", 0.6)],
    "2.4": [("MOM", "Everything you need is in there.", "m2", 0.5)],
    "2.4b": [("N", "A lot of money.", "n3", 0.1)],
    "2.5": [("N", "One woman.", "n4", 0.2)],
    "3.1": [("N", "I don't ask.", "n5", 0.2)],
    "3.2": [("N", "I'm the one who asks the questions.", "n6", 0.1)],
    "4.3": [("CLIENT", "How much?", "c1", 0.3), ("MOM", "One hundred bucks.", "m3", 0.3)],
    "4.4": [("N", "I name my price.", "n7", 0.6)],
    "4.4a": [("MOM", "For the fight.", "m4", 0.1)],
    "5.1c": [("PAM", "I'll help you undress.", "p1", 0.1), ("PAM", "Ah. Too late. The bell.", "p2", 2.3)],
    "5.4": [("MOM", "Approved.", "m5", 0.9)],
    "5.6": [("N", "I don't break. I break even.", "n8", 0.2)],
    "6.1": [("PAM", "Some punch. Others patch.", "p3", 0.8)],
    "6.2": [("N", "They beat me. They cheated me.", "n9", 0.0)],
    "6.3": [("N", "They robbed me.", "n10", 1.4)],
    "7.1": [("N", "But I didn't quit.", "n11", 0.1)],
    "7.2b": [("REFEREE", "Break!", "r1", 0.2)],
    "7.4": [("MOM", "Approved.", "m6", 0.7)],
}
# effect, shot, offset into the shot
FX = [("punch", "1.1", 0.30), ("snap", "3.2c", 0.42), ("bell", "5.1c", 1.55), ("bell", "5.2a", 0.0), ("click", "5.4b", 0.15),
      ("punch", "5.5", 0.97), ("pop", "6.2a", 0.2), ("pop", "6.2a", 0.5), ("pop", "6.2b", 0.3), ("pop", "6.2b", 0.9), ("stamp", "6.4", 0.34),
      ("click", "7.4b", 0.15), ("punch", "7.5", 0.75), ("chime", "8.1", 0.05), ("buzz", "8.2", 0.2), ("buzz", "8.3", 0.1), ("buzz", "8.3", 0.8),
      ("buzz", "8.3b", 0.05), ("bell", "8.5", 0.75)]


def trim(a, thr=0.012):
    idx = np.where(np.abs(a) > thr * np.max(np.abs(a)) / 0.1)[0]
    if not len(idx):
        return a
    return a[max(0, idx[0] - int(0.02 * SR)):min(len(a), idx[-1] + int(0.10 * SR))]


def takes():
    os.makedirs(VOICES, exist_ok=True)
    pv, psp, _ = sx.PAMS["A"]
    say = {"N": sob.client_line, "CLIENT": sob.client_line, "MOM": bc.mom,
           "PAM": lambda t: bc.norm(so.dry(t, pv, 1.0)), "REFEREE": lambda t: bc.norm(so.dry(t, "bm_george", 1.05))}
    meta = {}
    for shot, ls in LINES.items():
        for who, text, key, _ in ls:
            a = trim(np.asarray(say[who](text), dtype=np.float64))
            sf.write("%s/%s.wav" % (VOICES, key), a.astype(np.float32), SR)
            meta[key] = round(len(a) / SR, 3)
    json.dump(meta, open(VOICES + "/takes.json", "w"), indent=1)
    return meta


def schedule(meta):
    """-> shots [(name, start, dur, fn, base dur)], lines [(start, end, who, text, key)], and what was held and by how much."""
    shots, lines, held = [], [], []
    T, prev_end = 0.0, 0.0
    for name, dur, fn in fm.FILM:
        need = dur
        for who, text, key, off in LINES.get(name, []):
            st = max(T + off, prev_end + GAP)
            en = st + meta[key]
            lines.append((round(st, 3), round(en, 3), who, text, key))
            prev_end = en
            need = max(need, (en + 0.2 - T) if who != "N" else (st + min(meta[key], 0.8) - T))
        need = math.ceil(need * FPS - 1e-6) / FPS
        if need > dur + 1e-6:
            held.append((name, round(need - dur, 2)))
        shots.append((name, round(T, 3), need, fn, dur))
        T += need
    return shots, lines, held, T


def _fx(kind):
    t = lambda d: np.arange(int(d * SR)) / SR
    rng = np.random.default_rng(7)
    if kind == "punch":
        x = t(0.28); a = np.sin(2 * np.pi * (90 * np.exp(-x * 9) + 38) * x) * np.exp(-x * 14) * 0.9
        n = rng.standard_normal(len(x)) * np.exp(-x * 60) * 0.5
        return a + np.convolve(n, np.ones(24) / 24, "same")
    if kind == "stamp":
        x = t(0.20); return np.sin(2 * np.pi * 70 * x) * np.exp(-x * 22) * 0.7 + rng.standard_normal(len(x)) * np.exp(-x * 90) * 0.2
    if kind == "bell":
        x = t(1.6); return sum(g * np.sin(2 * np.pi * f * x) * np.exp(-x * d) for f, g, d in ((784, 0.5, 2.6), (1568, 0.3, 3.4), (2352, 0.18, 4.6), (3140, 0.1, 6.0))) * 0.55
    if kind == "click":
        x = t(0.05); return np.sin(2 * np.pi * 1400 * x) * np.exp(-x * 120) * 0.5 + rng.standard_normal(len(x)) * np.exp(-x * 300) * 0.3
    if kind == "snap":
        x = t(0.06); return rng.standard_normal(len(x)) * np.exp(-x * 110) * 0.45
    if kind == "pop":
        x = t(0.35); return np.convolve(rng.standard_normal(len(x)), np.ones(6) / 6, "same") * np.exp(-x * 16) * 0.45
    if kind == "chime":
        x = t(0.7); return (np.sin(2 * np.pi * 880 * x) * np.exp(-x * 5) + np.sin(2 * np.pi * 1318.5 * np.maximum(x - 0.16, 0)) * np.exp(-np.maximum(x - 0.16, 0) * 5) * (x > 0.16)) * 0.3
    if kind == "buzz":
        x = t(0.55); return np.sign(np.sin(2 * np.pi * 155 * x)) * (np.sin(2 * np.pi * 9 * x) > -0.2) * np.minimum(1, (0.55 - x) * 20) * 0.16
    raise KeyError(kind)


def mix(shots, lines, total):
    out = np.zeros(int((total + 0.5) * SR))
    start = {}
    for name, st, dur, fn, base in shots:
        start.setdefault(name, st)
    for st, en, who, text, key in lines:
        a, sr = sf.read("%s/%s.wav" % (VOICES, key)); i = int(st * SR)
        out[i:i + len(a)] += a[:len(out) - i]
    fx = []
    for kind, shot, off in FX:
        a = _fx(kind); i = int((start[shot] + off) * SR); fx.append((kind, shot, round(start[shot] + off, 3)))
        out[i:i + len(a)] += a[:len(out) - i] * 0.6
    out = out[:int(total * SR)]
    return np.tanh(out * 1.6) / 1.6, fx


def _caption(surf, who, text):
    """The line, at the top under the bar (y 96 on), inside the safe area: never in the bottom quarter."""
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(s)
    c.set_source_surface(surf, 0, 0); c.paint()
    c.select_font_face("sans", 0, 1); c.set_font_size(21)
    words, rows, row = text.split(), [], ""
    for w in words:
        if c.text_extents((row + " " + w).strip())[2] > 440:
            rows.append(row); row = w
        else:
            row = (row + " " + w).strip()
    rows.append(row)
    h = 34 + 28 * len(rows)
    c.set_source_rgba(0, 0, 0, 0.72); c.rectangle(30, 100, 480, h); c.fill()
    c.set_font_size(13); c.set_source_rgb(0.75, 0.75, 0.78); c.move_to(44, 120); c.show_text("NARRATION" if who == "N" else who)
    c.set_font_size(21); c.set_source_rgb(1, 1, 1)
    for i, r_ in enumerate(rows):
        c.move_to(44, 146 + 28 * i); c.show_text(r_)
    return s


def build(out):
    meta = takes()
    shots, lines, held, total = schedule(meta)
    FN, SH = {}, []
    for i, (name, st, dur, fn, base) in enumerate(shots):
        key = "%02d_%s" % (i, name)

        def f(t, fn=fn, base=base, st=st):
            s = fn(min(t, base - 1.0 / FPS))
            T = st + t
            for a, b_, who, text, _ in lines:
                if a - 0.05 <= T < b_ + 0.15:
                    return _caption(s, who, text)
            return s
        FN[key] = f; SH.append((key, dur))
    audio, fx = mix(shots, lines, total)
    d = os.path.dirname(os.path.abspath(out))
    wav, silent = os.path.join(d, "_on3_animatic.wav"), os.path.join(d, "_on3_animatic_silent.mp4")
    sf.write(wav, audio.astype(np.float32), SR)
    rr.SHOTS, rr.FN = tuple(SH), FN
    rr.render(silent)
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                           "-af", "loudnorm=I=-15:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "160k", out])
    os.remove(silent); os.remove(wav)
    json.dump({"length": round(total, 3), "shots": [(n, s_, round(d_, 3), round(b_, 3)) for n, s_, d_, _, b_ in shots],
               "lines": lines, "effects": fx, "held": held}, open("on3_animatic_timing_%s.json" % V, "w"), indent=1)
    return total, held, lines


if __name__ == "__main__":
    total, held, lines = build(sys.argv[1] if len(sys.argv) > 1 else "../office-noir-3/on3_animatic_%s.mp4" % V)
    print("%.1f s" % total); print("held:", held)
    for l in lines:
        print(l[:4])
