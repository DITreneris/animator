"""Sound for "I Will Replace You" (storyboard v2 animatic). Voices (Kokoro): Don am_onyx, Sofía af_bella,
the robot one of three auditioned voices (ROBOT=A|B|C, default A). Stings and foley only, no music, no
laugh track: subtract before adding. Tails wrap across the loop point.
Usage: python3 sound_iwry.py audition   -> iwry_robot_auditions.mp4 (+ wavs in iwry_voices/)
       ROBOT=A python3 sound_iwry.py mix -> iwry_mix_<ROBOT>.wav"""
import os
import sys
import subprocess
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

SR, DUR = 48000, 25.0
L = int(SR * DUR)
rng = np.random.default_rng(23)
KD = os.environ.get("KOKORO_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "models"))
K = Kokoro(os.path.join(KD, "kokoro-v1.0.int8.onnx"), os.path.join(KD, "voices-v1.0.bin"))

DON, SOF = "am_onyx", "af_bella"
ROBOTS = {   # voice, speed, semitones up, ring, comb, note
    "A": ("am_puck", 1.05, 3, 0.12, 0.30, "bright and eager, light metal"),
    "B": ("am_echo", 1.0, 2, 0.20, 0.45, "flatter, more speaker-like"),
    "C": ("bm_fable", 1.05, 3, 0.10, 0.25, "British, polite butler-bot"),
}


def tt(d):
    return np.arange(int(d * SR)) / SR


def lp(x, n):
    return np.convolve(x, np.ones(n) / n, mode="same")


def noise(d):
    return rng.standard_normal(int(d * SR))


def add(buf, a, t0, g=1.0):
    idx = (int(t0 * SR) + np.arange(len(a))) % len(buf)
    np.add.at(buf, idx, a * g)


def say(txt, voice, speed=1.0):
    a, sr = K.create(txt, voice=voice, speed=speed, lang="en-us")
    a = np.asarray(a, dtype=np.float64)
    if sr != SR:
        a = np.interp(np.linspace(0, len(a) - 1, int(len(a) * SR / sr)), np.arange(len(a)), a)
    idx = np.where(np.abs(a) > 0.01)[0]
    a = a[max(0, idx[0] - 600):idx[-1] + 2400]
    return a / np.sqrt(np.mean(a ** 2)) * 0.11


def robotize(a, semis, ring, comb):
    f = 2 ** (semis / 12)
    b = np.interp(np.arange(0, len(a) - 1, f), np.arange(len(a)), a)
    t = np.arange(len(b)) / SR
    b = b * (1 - ring) + b * np.sin(2 * np.pi * 70 * t) * ring * 1.6
    d = int(0.0038 * SR)
    c = b.copy()
    c[d:] += b[:-d] * comb
    c = c - lp(c, 30) * 0.5                                    # thinner, small-speaker tone
    return c / np.sqrt(np.mean(c ** 2)) * 0.11


def shout(a):
    """Bigger and harder, short tail only (no reverb: it must not spill into the whisper)."""
    b = np.tanh(a * 14) / 14 * 1.0
    d = int(0.012 * SR)
    c = b.copy()
    c[d:] += b[:-d] * 0.25
    return c / np.sqrt(np.mean(c ** 2)) * 0.15


def whisper(a):
    """Quiet, dry, airy, but fully intelligible: volume only modestly lower."""
    hp = a - lp(a, 12)
    env = lp(np.abs(a), 400)
    air = lp(rng.standard_normal(len(a)), 3) * env * 0.6
    c = hp * 0.8 + a * 0.35 + air
    return c / np.sqrt(np.mean(c ** 2)) * 0.075


def hf_bursts(a):
    """Count 20 ms windows whose high-frequency energy spikes above 4x the median: harsh 's' or clicks."""
    hp = a - lp(a, 6)
    e = np.array([np.sqrt(np.mean(hp[j:j + 960] ** 2)) for j in range(0, len(hp) - 960, 960)])
    return int((e > 4 * np.median(e)).sum()), float(np.abs(np.diff(a)).max())


def don_shout(a):
    """v2 for Don's "WHAT IS THIS?!": the robot's shout (hard tanh x14) clipped his voice into a buzz.
    Gentle instead: soft compression and a little more level; no clipping, no tail."""
    peak = np.max(np.abs(a))
    b = np.tanh(a / peak * 1.6) / np.tanh(1.6) * peak        # soft knee, at most ~1.5 dB of squash
    return b / np.sqrt(np.mean(b ** 2)) * 0.15


def buzz(a):
    """Share of samples pushed into hard saturation: a proxy for the buzz."""
    m = np.max(np.abs(a))
    return float(np.mean(np.abs(a) > 0.9 * m))


def whisper2(a):
    """v2 whisper (the v1 high-pass sharpened the 's' sounds into glitchy bursts): soften the sibilants,
    a gentle breath under the voice, quieter but fully intelligible."""
    soft = lp(a, 4)                                            # de-ess: tame the harsh top
    env = lp(np.abs(soft), 900)
    breath = lp(lp(rng.standard_normal(len(a)), 6), 3) * env * 0.35
    c = soft * 0.9 + breath
    fade = int(0.02 * SR)
    c[:fade] *= np.linspace(0, 1, fade); c[-fade:] *= np.linspace(1, 0, fade)
    return c / np.sqrt(np.mean(c ** 2)) * 0.09                 # about 5 dB under the shout: quiet, still clear


def clean_whisper(txt, key, spf=1.0):
    """Several takes at slightly different speeds; keep the one with the smallest sample jump (clicks)."""
    v, sp, semis, ring, comb, _ = ROBOTS[key]
    best = None
    for f in (1.0, 1.03, 1.06):
        a = whisper2(robotize(say(txt, v, sp * spf * f), semis, ring * 0.6, comb * 0.6))
        jump = float(np.abs(np.diff(a)).max())
        if best is None or jump < best[0]:
            best = (jump, f, a)
    print(f"  whisper take x{spf * best[1]:.2f}: max jump {best[0]:.3f}")
    return best[2]


def robot_line(txt, key, kind="normal"):
    v, sp, semis, ring, comb, _ = ROBOTS[key]
    sp = {"shout": sp * 0.92, "whisper": sp * 1.08}.get(kind, sp)
    a = robotize(say(txt, v, sp), semis, ring, comb)
    return {"shout": shout, "whisper": whisper}.get(kind, lambda x: x)(a)


# ------------------------------------------------------------------ audition
def audition():
    import cairo
    os.makedirs("iwry_voices", exist_ok=True)
    lines = [("Ready to order, sir?", "normal"), ("Are you hiring, sir?", "normal"),
             ("I WILL REPLACE YOU!", "shout"), ("If that's okay, sir?", "whisper")]
    FPS, Wd = 10, 540
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, Wd, Wd)
    audio, frames = [], []
    for key, (v, *_rest, note) in ROBOTS.items():
        parts = []
        for txt, kind in lines:
            parts += [robot_line(txt, key, kind), np.zeros(int(0.35 * SR))]
        a = np.concatenate([np.zeros(int(0.5 * SR))] + parts)
        n = int(np.ceil(len(a) / SR * FPS))
        a = np.concatenate([a, np.zeros(n * SR // FPS - len(a))])
        sf.write(f"iwry_voices/robot_{key}_{v}.wav", a, SR)
        c = cairo.Context(surf)
        c.set_source_rgb(0.91, 0.94, 0.95); c.paint()
        c.set_source_rgb(0.12, 0.16, 0.27)
        c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        for txt, size, y in (("ROBOT", 80, 210), (f"{key}  {v}", 46, 300)):
            c.set_font_size(size); e = c.text_extents(txt); c.move_to((Wd - e.x_advance) / 2, y); c.show_text(txt)
        c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        c.set_font_size(21); e = c.text_extents(note); c.move_to((Wd - e.x_advance) / 2, 360); c.show_text(note)
        surf.flush()
        frames += [bytes(surf.get_data())] * n
        audio.append(a)
    mix = np.concatenate(audio)
    sf.write("/tmp/iwry_aud.wav", mix, SR)
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{Wd}x{Wd}",
                          "-r", str(FPS), "-i", "-", "-i", "/tmp/iwry_aud.wav", "-af", "loudnorm=I=-16:TP=-2",
                          "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-shortest",
                          "iwry_robot_auditions.mp4"], stdin=subprocess.PIPE)
    for f in frames:
        p.stdin.write(f)
    p.stdin.close(); p.wait()
    print("audition", round(len(mix) / SR, 1), "s")


# ------------------------------------------------------------------ effects
def env(d, k):
    return np.exp(-tt(d) * k)


def ting():
    t = tt(0.5)
    return sum(np.sin(2 * np.pi * f * t) * g for f, g in ((2350, 1), (3720, 0.4))) * np.exp(-t * 9)


def bloop():
    t = tt(0.18)
    return np.sin(2 * np.pi * (300 + 500 * t / 0.18) * t) * np.sin(np.pi * t / 0.18)


def squeak(d, rate=5.5):
    """The robot's motif: an irregular squeaky wheel."""
    t = tt(d)
    f = 1500 + 300 * np.sin(2 * np.pi * rate * t) + 120 * np.sin(2 * np.pi * 13 * t)
    gate = np.clip(np.sin(2 * np.pi * rate * t + 1.2), 0, 1) ** 3
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * gate * np.minimum(1, np.minimum(t, d - t) / 0.05)


def rattle(d):
    t = tt(d)
    n = noise(d)
    return (n - lp(n, 3)) * (np.sin(2 * np.pi * 9 * t) > 0.6) * 0.5 * np.minimum(1, np.minimum(t, d - t) / 0.05)


def clank():
    t = tt(0.7)
    return (sum(np.sin(2 * np.pi * f * t) * g * np.exp(-t * k) for f, g, k in
                ((520, 1, 7), (1230, 0.6, 9), (2890, 0.35, 14), (4100, 0.2, 18)))
            + lp(noise(0.7), 2) * np.exp(-t * 60) * 0.6)


def tick(f=3000):
    t = tt(0.05)
    return np.sin(2 * np.pi * f * t) * np.exp(-t * 160)


def drip():
    t = tt(0.12)
    return np.sin(2 * np.pi * (380 + 1500 * t) * t) * np.exp(-t * 38)


def lock():
    """One short mechanical lock: a clamp clunk and a servo stop, no tail."""
    t = tt(0.22)
    thunk = np.sin(2 * np.pi * 90 * t * (1 + 0.6 * np.exp(-t * 50))) * np.exp(-t * 26)
    clk = (lp(noise(0.22), 2)) * np.exp(-t * 90) * 0.8
    return thunk + clk


def servo(d, f0, f1):
    t = tt(d)
    ph = 2 * np.pi * np.cumsum(np.linspace(f0, f1, len(t))) / SR
    return (np.sin(ph) + 0.3 * np.sign(np.sin(2 * ph))) * 0.35 * np.minimum(1, np.minimum(t, d - t) / 0.03)


def bell(f=1560, d=1.3):
    t = tt(d)
    return sum(g * np.sin(2 * np.pi * f * r * t) * np.exp(-t * k) for r, g, k in
               ((1, 1, 4), (2.76, 0.5, 6), (5.4, 0.25, 9), (8.9, 0.12, 14))) * np.minimum(1, t / 0.002)


def clink():
    t = tt(0.6)
    return sum(np.sin(2 * np.pi * f * t) * g for f, g in ((2900, 1), (4870, 0.6), (6700, 0.3))) * np.exp(-t * 11)


def mix(key):
    lines = [  # (who, text, start, slot end, kind)
        ("DON", "Nice hoops. Can I get in your loop?", 0.25, 2.95, ""),
        ("SOF", "You're out of the loop.", 3.2, 4.75, ""),
        ("ROB", "Ready to order, sir?", 7.6, 8.9, "normal"),
        ("DON", "Two cheeseburgers.", 8.95, 9.95, ""),
        ("DON", "WHAT IS THIS?!", 14.55, 16.05, ""),
        ("ROB", "Are you hiring, sir?", 16.5, 18.0, "normal"),
        ("ROB", "I WILL REPLACE YOU!", 18.42, 19.95, "shout"),
        ("ROB", "If that's okay, sir?", 20.75, 21.9, "whisper"),
        ("DON", "Approved.", 22.75, 23.45, ""),
    ]
    voice = np.zeros(L)
    for who, txt, t0, slot, kind in lines:
        for sp in (1.0, 1.08, 1.16, 1.24, 1.32):          # speed up only if the take overruns its bubble
            if who == "ROB" and kind == "whisper" and WHISPER_V == 2:
                a = clean_whisper(txt, key, sp)
            elif who == "ROB":
                v, s0 = ROBOTS[key][0], ROBOTS[key][1]
                a = robotize(say(txt, v, s0 * sp * {"shout": 0.92, "whisper": 1.08}.get(kind, 1)),
                             *ROBOTS[key][2:5])
                a = {"shout": shout, "whisper": whisper}.get(kind, lambda x: x)(a)
            else:
                a = say(txt, DON if who == "DON" else SOF, sp * (1.12 if txt == "WHAT IS THIS?!" else 1.0))
                if txt == "WHAT IS THIS?!":
                    a = don_shout(a) if DON_SHOUT_V == 2 else shout(a) * 0.9
            if t0 + len(a) / SR <= slot + 0.1:
                break
        add(voice, a, t0)
        TAKES.append((who, txt, t0, a))
        print(f"{who} {txt:38s} {t0:5.2f}-{t0 + len(a) / SR:5.2f} slot {slot}  speed x{sp}",
              "OK" if t0 + len(a) / SR <= slot + 0.1 else "LATE")
    fx = np.zeros(L)
    add(fx, ting(), 0.55, 0.10)                            # "hoops": quiet, so the first second isn't silent
    add(fx, bloop(), 5.6, 0.05)                            # thought: barely audible
    add(fx, squeak(1.1), 4.8, 0.10)                        # the robot rolls in (motif)
    add(fx, squeak(0.4, 7), 9.8, 0.10)                     # rolls off
    add(fx, squeak(1.5), 10.2, 0.12); add(fx, rattle(1.5), 10.2, 0.10)
    add(fx, clank(), 11.85, 0.28)                          # the metal reveal
    add(fx, tick(2400), 12.25, 0.10)                       # settle
    add(fx, tick(3300), 13.18, 0.22)                       # the bolt lands
    add(fx, drip(), 15.22, 0.25)                           # oil on Don's shirt
    add(fx, lock(), 18.3, 0.50)                            # the wheel clamps: one short lock
    add(fx, servo(0.3, 420, 180), 20.42, 0.07)             # the collapse, a soft servo down
    add(fx, squeak(0.3, 9), 21.85, 0.05)                   # nervous wobble returns
    add(fx, bell(), 22.75, 0.30)                           # "Approved." DING (Day One's bell)
    add(fx, tick(2600), 24.55, 0.12)                       # bolt tips
    add(fx, clink(), 24.82, 0.30)                          # ... and lands: the last sound before the repeat
    t = np.arange(L) / SR
    room = lp(rng.standard_normal(L), 160) * 1.1           # cafeteria murmur + far cutlery
    for tc in rng.uniform(0, DUR, 26):
        add(room, tick(rng.uniform(3500, 6000)) * 0.4, tc, 1.0)
    dip = 1 - 0.6 * np.clip(np.minimum((t - 20.1) / 0.15, (21.9 - t) / 0.15), 0, 1)    # the whisper's room dip
    room *= 0.045 * dip
    venv = lp(np.abs(voice), 4800)
    duck = 1 - 0.5 * np.clip(venv / 0.05, 0, 1)
    out = voice + fx * duck + room * duck
    out = np.tanh(out * 1.6) / 1.6
    out /= max(1.0, np.max(np.abs(out)) / 0.85)
    tag = ("_w2" if WHISPER_V == 2 else "") + ("_d2" if DON_SHOUT_V == 2 else "")
    sf.write(f"iwry_mix_{key}{tag}.wav", np.stack([out, out], 1), SR)
    if os.environ.get("LIPS"):                                   # per-frame loudness of each final take
        import json
        nf = int(DUR * 30)
        lips = {"DON": [0.0] * nf, "SOF": [0.0] * nf, "ROB": [0.0] * nf, "lines": []}
        hop = SR // 30
        for who, txt, t0, a in TAKES:
            e = np.array([np.sqrt(np.mean(a[j:j + hop] ** 2)) for j in range(0, len(a), hop)])
            e = e / e.max()
            f0 = int(round(t0 * 30))
            for j, v in enumerate(e):
                if f0 + j < nf:
                    lips[who][f0 + j] = round(float(v), 3)
            lips["lines"].append([who, txt, round(t0, 3), round(t0 + len(a) / SR, 3)])
        json.dump(lips, open(f"iwry_lips{tag}.json", "w"))
        print("lips written")
    print("peak", round(float(np.max(np.abs(out))), 3))


TAKES = []
WHISPER_V = int(os.environ.get("WHISPER", "1"))      # 2 = the de-essed, best-take whisper (animatic v2)
DON_SHOUT_V = int(os.environ.get("DONSHOUT", "1"))   # 2 = Don's shout without the hard clipping (animatic v3)

if __name__ == "__main__":
    if sys.argv[1] == "audition":
        audition()
    else:
        mix(os.environ.get("ROBOT", "A"))
