"""Sound for the Christmas special "Happy Compliance". Voices (Kokoro): Don am_onyx, Sofía af_bella, the robot
voice B from last episode (am_echo, robotized; its shout treatment), Pam one of three auditioned British voices.
Usage: KOKORO_DIR=... python3 sound_xmas.py audition   -> xmas_pam_auditions.mp4 (+ wavs in xmas_voices/)"""
import os
import sys
import subprocess
import numpy as np
import soundfile as sf
import sound_iwry as si

SR = si.SR
PAMS = {   # voice, speed, note
    "A": ("bf_emma", 0.92, "dry, flat, unimpressed"),
    "B": ("bf_alice", 0.92, "clipped, office-proper"),
    "C": ("bf_isabella", 0.90, "low, tired, deadpan"),
}


def say(txt, voice, speed=1.0, lang="en-us"):
    a, sr = si.K.create(txt, voice=voice, speed=speed, lang=lang)
    a = np.asarray(a, dtype=np.float64)
    if sr != SR:
        a = np.interp(np.linspace(0, len(a) - 1, int(len(a) * SR / sr)), np.arange(len(a)), a)
    idx = np.where(np.abs(a) > 0.01)[0]
    a = a[max(0, idx[0] - 600):idx[-1] + 2400]
    return a / np.sqrt(np.mean(a ** 2)) * 0.11


def best_take(txt, voice, speed, lang):
    """Three takes at slightly different speeds; keep the one with the smallest sample jump (no clicks)."""
    best = None
    for f in (1.0, 0.97, 1.03):
        a = say(txt, voice, speed * f, lang)
        j = float(np.abs(np.diff(a)).max())
        if best is None or j < best[0]:
            best = (j, a)
    return best[1]


def pam_line(txt, key):
    v, sp, _ = PAMS[key]
    return best_take(txt, v, sp, "en-gb" if v.startswith("b") else "en-us")


def audition():
    import cairo
    import kit
    import pam_xmas as px
    os.makedirs("xmas_voices", exist_ok=True)
    lines = ["Eww.", "Human in the loop."]
    FPS, Wd = 10, 540
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, Wd, Wd)
    audio, frames = [], []
    for key, (v, sp, note) in PAMS.items():
        parts = []
        for txt in lines:
            parts += [pam_line(txt, key), np.zeros(int(0.5 * SR))]
        a = np.concatenate([np.zeros(int(0.5 * SR))] + parts)
        n = int(np.ceil(len(a) / SR * FPS))
        a = np.concatenate([a, np.zeros(n * SR // FPS - len(a))])
        sf.write(f"xmas_voices/pam_{key}_{v}.wav", a, SR)
        c = cairo.Context(surf)
        c.set_source_rgb(0.88, 0.85, 0.94); c.paint()
        k = kit.Ctx(c, 0)
        hy = -300 * kit.PEOPLE["PAM"]["h"] + 78 - 44
        px.pam(k, 150, 250 - hy * 1.2, 1.2, "stand", "neutral", mask="down", cape=False)
        c.set_source_rgb(0.12, 0.16, 0.27)
        c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        for txt, size, y in (("PAM", 70, 200), (f"{key}  {v}", 38, 270)):
            c.set_font_size(size); e = c.text_extents(txt); c.move_to(390 - e.x_advance / 2, y); c.show_text(txt)
        c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        c.set_font_size(20); e = c.text_extents(note); c.move_to(390 - e.x_advance / 2, 320); c.show_text(note)
        c.set_font_size(18)
        for i, l in enumerate(("\"Eww.\"", "\"Human in the loop.\"")):
            e = c.text_extents(l); c.move_to(390 - e.x_advance / 2, 380 + i * 28); c.show_text(l)
        surf.flush()
        frames += [bytes(surf.get_data())] * n
        audio.append(a)
    mix = np.concatenate(audio)
    sf.write("/tmp/xmas_aud.wav", mix, SR)
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{Wd}x{Wd}",
                          "-r", str(FPS), "-i", "-", "-i", "/tmp/xmas_aud.wav", "-af", "loudnorm=I=-16:TP=-2",
                          "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-shortest",
                          "xmas_pam_auditions.mp4"], stdin=subprocess.PIPE)
    for f in frames:
        p.stdin.write(f)
    p.stdin.close(); p.wait()
    print("audition", round(len(mix) / SR, 1), "s")


if __name__ == "__main__":
    if sys.argv[1:] == ["audition"]:
        audition()


# ------------------------------------------------------------------ the film's sound (storyboard v2 timing)
from sound_iwry import tt, lp, add, env, ting, bloop, squeak, rattle, clank, tick, lock, servo, bell, clink

DUR = 28.9
L = int(SR * DUR)
rng = np.random.default_rng(31)
LINES = [   # (who, text, start, slot end, how)
    ("DON", "Sorry. Getting ready for the ball.", 0.15, 2.35, ("am_onyx", 1.0)),
    ("SOF", "Eww.", 3.62, 4.75, ("af_bella", 0.95)),
    ("PAM", "Eww.", 3.60, 4.75, "pam"),
    ("DON", "Nice balls... I've got two for you.", 6.85, 9.45, ("am_onyx", 0.9)),
    ("ROB", "Inappropriate balls detected!", 13.75, 15.8, "shout"),
    ("ROB", "Violation resolved.", 19.95, 21.5, "normal"),
    ("SOF", "Get him.", 21.95, 22.55, ("af_bella", 0.9)),
    ("PAM", "Human in the loop.", 23.05, 24.5, "pam"),
    ("SOF", "Merry Christmas, Don.", 25.6, 26.9, ("af_bella", 0.95)),
    ("ROB", "Happy compliance!", 27.0, 28.3, "normal"),
]
TAKES = []


def noise(d):
    return rng.standard_normal(int(d * SR))


def thunk(d=0.25, f=95):
    t = tt(d)
    body = np.sin(2 * np.pi * f * t * (1 + 0.8 * np.exp(-t * 40))) * np.exp(-t * 18)
    slap = lp(noise(d), 3) * np.exp(-t * 70) * 0.7
    return body + slap


def boom():
    t = tt(0.9)
    return (np.sin(2 * np.pi * 52 * t * (1 + 1.2 * np.exp(-t * 20))) * np.exp(-t * 6)
            + lp(noise(0.9), 20) * np.exp(-t * 12) * 1.2)


def whoosh(d=0.2):
    t = tt(d)
    n = noise(d)
    return (n - lp(n, 8)) * np.sin(np.pi * t / d) ** 2 * 0.5


def scrape(d, f=0.0):
    t = tt(d)
    n = noise(d)
    gr = (n - lp(n, 2)) * (0.6 + 0.4 * np.sin(2 * np.pi * (38 + f) * t))
    return gr * np.minimum(1, np.minimum(t, d - t) / 0.03) * 0.5


def chirp():
    """The robot's alarm chirp: two quick up-sweeps."""
    out = []
    for i in range(2):
        t = tt(0.12)
        f = 900 + 1400 * t / 0.12
        out += [np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / 0.12), np.zeros(int(0.04 * SR))]
    return np.concatenate(out)


def twang():
    """The mask's elastic snapping on."""
    t = tt(0.35)
    f = 180 + 260 * np.exp(-t * 18)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 11) * (1 + 0.4 * np.sin(2 * np.pi * 28 * t))


def rustle(d=0.4):
    n = noise(d)
    t = tt(d)
    return (n - lp(n, 4)) * np.sin(np.pi * t / d) * 0.35


def slipper(d=0.12):
    t = tt(d)
    return lp(noise(d), 6) * np.sin(np.pi * t / d) * 0.6


def jingle(d=0.18):
    t = tt(d)
    n = noise(d)
    return (n - lp(n, 2)) * np.exp(-t * 22) * 0.6 + sum(np.sin(2 * np.pi * f * t) for f in (5200, 6900)) * np.exp(-t * 30) * 0.15


def glock(f, d=0.6):
    t = tt(d)
    return (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * f * 2.76 * t)) * np.exp(-t * 6)


def bed(t0, t1, detune=1.0):
    """Original sleigh-bell + glockenspiel loop at 128 bpm: jingles on the beats, a little tune on top."""
    out = np.zeros(int((t1 - t0) * SR) + SR)
    beat = 60 / 128
    tune = [784, 659, 698, 784, 880, 784, 659, 587]          # G E F G A G E D (an invented line)
    n = int((t1 - t0) / (beat / 2)) + 1
    for i in range(n):
        tj = i * beat / 2
        add(out, jingle(), tj, 0.55 if i % 2 == 0 else 0.3)
        if i % 2 == 0:
            add(out, glock(tune[(i // 2) % len(tune)] * detune), tj, 0.32)
    out = out[:int((t1 - t0) * SR)]
    fade = int(0.03 * SR)
    out[-fade:] *= np.linspace(1, 0, fade)                    # "stops dead": a 30 ms cut, no tail
    return out


def make_line(who, txt, how):
    if how == "pam":
        return pam_line(txt, "A")
    if who == "ROB":
        return si.robot_line(txt, "B", how)
    v, sp = how
    return best_take(txt, v, sp, "en-us")


def mix():
    voice = np.zeros(L)
    for who, txt, t0, slot, how in LINES:
        a = make_line(who, txt, how)
        g = 0.75 if txt == "Eww." else 1.0                     # the unison: two voices, one level
        add(voice, a * g, t0)
        TAKES.append((who, txt, t0, a))
        end = t0 + len(a) / SR
        print(f"{who} {txt:38s} {t0:5.2f}-{end:5.2f} slot {slot}", "OK" if end <= slot + 0.1 else "LATE")
    fx = np.zeros(L)
    for i, tj in enumerate((0.05, 0.22, 0.4)):                 # 1: slippers in, a razor scrape
        add(fx, slipper(), tj, 0.35)
    add(fx, scrape(0.45, 20), 0.55, 0.12)
    add(fx, scrape(0.3, 24), 1.5, 0.08)
    add(fx, servo(0.9, 220, 140) * 0.0, 5.9, 0.0)
    t = tt(0.9)                                                # 5: a low rising tone under Sofía's face change
    add(fx, np.sin(2 * np.pi * np.cumsum(90 + 60 * t / 0.9) / SR) * np.sin(np.pi * t / 0.9), 9.8, 0.20)
    add(fx, clink(), 10.3, 0.12)                               # Pam puts the thermos down
    add(fx, squeak(0.9), 11.8, 0.12); add(fx, rattle(0.9), 11.8, 0.08)    # 6: the robot rolls in
    for tc in (11.85, 12.35, 12.85):
        add(fx, chirp(), tc, 0.22)                             # the alarm
    add(fx, lock(), 13.6, 0.45)                                # 7: the rigid point
    # 8: the censoring (motion test A, + 15.8)
    for th, tc in ((16.3, 16.5), (16.7, 16.9), (17.1, 17.3)):
        add(fx, tick(2100), th + 0.11, 0.18); add(fx, squeak(0.12, 9), th, 0.05)    # hop landing
        add(fx, thunk(), tc, 0.55)                             # three slaps
    for tl in (17.5, 17.6, 17.7, 17.8, 17.9):
        add(fx, whoosh(0.16), tl, 0.25); add(fx, thunk(0.14, 130), tl + 0.17, 0.32)  # the cascade
    add(fx, squeak(0.25, 8), 18.1, 0.10)
    add(fx, thunk(0.3, 80), 18.38, 0.85); add(fx, thunk(0.3, 75), 18.68, 0.95)       # Sofía's two: loudest
    add(fx, squeak(0.35, 7), 18.9, 0.08)
    add(fx, bloop(), 19.3, 0.12)                               # the screen blink to smug
    add(fx, ting(), 20.45, 0.12)                               # 9: thumbs-up pop
    add(fx, rustle(0.25), 21.85, 0.25)                         # 10: the handoff
    add(fx, clink(), 22.35, 0.10)
    add(fx, rustle(0.15), 22.6, 0.3)
    add(fx, twang(), 22.78, 0.35)                              # the mask snaps on
    add(fx, rustle(0.6), 22.82, 0.45)                          # the towel lifts
    add(fx, boom(), 27.2, 0.9)                                 # 11: off-screen THUD
    add(fx, clink(), 27.25, 0.2)                               # a bauble rolls
    add(fx, scrape(0.55, 40), 27.3, 0.35)                      # the razor slides in
    add(fx, tick(1800), 28.5, 0.25)                            # the bar lands
    add(fx, chirp(), 28.35, 0.3)                               # the alarm again: the loop
    music = np.zeros(L)
    add(music, bed(0.0, 6.85), 0.0, 1.0)                       # stops dead on "Nice balls"
    add(music, bed(0.0, DUR - 27.0, detune=0.97), 27.0, 0.9)   # comes back slightly wrong
    room = lp(rng.standard_normal(L), 160) * 0.05
    venv = lp(np.abs(voice), 4800)
    duck = 1 - 0.55 * np.clip(venv / 0.05, 0, 1)
    out = voice + fx * duck + music * 0.16 * duck + room * duck
    out = np.tanh(out * 1.6) / 1.6
    out /= max(1.0, np.max(np.abs(out)) / 0.85)
    sf.write("xmas_mix_v1.wav", np.stack([out, out], 1), SR)
    import json                                                 # per-frame loudness of each take, for lip-sync
    nf = int(DUR * 30)
    lips = {"DON": [0.0] * nf, "SOF": [0.0] * nf, "PAM": [0.0] * nf, "ROB": [0.0] * nf, "lines": []}
    hop = SR // 30
    for who, txt, t0, a in TAKES:
        e = np.array([np.sqrt(np.mean(a[j:j + hop] ** 2)) for j in range(0, len(a), hop)])
        e = e / e.max()
        f0 = int(round(t0 * 30))
        for j, v in enumerate(e):
            if f0 + j < nf:
                lips[who][f0 + j] = round(float(v), 3)
        lips["lines"].append([who, txt, round(t0, 3), round(t0 + len(a) / SR, 3)])
    json.dump(lips, open("xmas_lips_v1.json", "w"))
    print("peak", round(float(np.max(np.abs(out))), 3), "duration", DUR)


if __name__ == "__main__" and sys.argv[1:] == ["mix"]:
    mix()
