"""Voice auditions for "How Sofía Survived Day One": 3 options each for Don and Sofía, 2 robot treatments
built from Don's voice. Writes day1_voice_auditions.mp4 (label cards + audio) and one WAV per option in
day1_voices/. Usage: python3 day1_voices.py"""
import os, subprocess
import numpy as np
import soundfile as sf
import cairo
from kokoro_onnx import Kokoro

SR = 48000
KD = os.environ.get("KOKORO_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "models"))
K = Kokoro(os.path.join(KD, "kokoro-v1.0.int8.onnx"), os.path.join(KD, "voices-v1.0.bin"))
OUT = "day1_voices"
os.makedirs(OUT, exist_ok=True)

DON_LINES = ["I approve everything.", "Trained it myself.", "Pam?", "Perfect."]
SOF_LINES = ["Can you help me?", "Pam?"]
ROB_LINES = ["Pam?", "Can you help me?"]


def resample(a, sr):
    if sr == SR:
        return a
    n = int(len(a) * SR / sr)
    return np.interp(np.linspace(0, len(a) - 1, n), np.arange(len(a)), a)


def say(txt, voice, speed):
    a, sr = K.create(txt, voice=voice, speed=speed, lang="en-us")
    a = resample(np.asarray(a, dtype=np.float64), sr)
    idx = np.where(np.abs(a) > 0.01)[0]
    a = a[max(0, idx[0] - 800):idx[-1] + 2400]
    return a / max(1e-6, np.max(np.abs(a))) * 0.7


def join(clips, gap=0.35):
    g = np.zeros(int(gap * SR))
    out = []
    for c in clips:
        out += [c, g]
    return np.concatenate(out)


def robotize(a, semis, ring, comb):
    """Pitch up by resampling (shorter and higher, like a small copy), ring-modulate, add a short comb."""
    f = 2 ** (semis / 12)
    b = np.interp(np.arange(0, len(a) - 1, f), np.arange(len(a)), a)
    t = np.arange(len(b)) / SR
    b = b * (1 - ring) + b * np.sin(2 * np.pi * 62 * t) * ring * 1.6
    d = int(0.0045 * SR)
    c = b.copy()
    c[d:] += b[:-d] * comb
    c[2 * d:] += b[:-2 * d] * comb * 0.5
    return c / max(1e-6, np.max(np.abs(c))) * 0.7


OPTIONS = []   # (group, label, note, audio)
for lab, v, sp, note in [("A", "am_fenrir", 1.0, "deep, booming boss (Don's voice in Prompt Telephone)"),
                         ("B", "am_onyx", 1.0, "smooth, slow, self-satisfied"),
                         ("C", "bm_george", 1.0, "British, pompous manager")]:
    OPTIONS.append(("DON", f"{lab}  {v}", note, join([say(l, v, sp) for l in DON_LINES])))
for lab, v, sp, note in [("A", "af_heart", 1.0, "warm, friendly, natural"),
                         ("B", "af_bella", 1.0, "brighter, more playful"),
                         ("C", "af_sarah", 0.95, "calm, a little dry")]:
    OPTIONS.append(("SOFÍA", f"{lab}  {v}", note, join([say(l, v, sp) for l in SOF_LINES])))
base = [say(l, "am_fenrir", 1.0) for l in ROB_LINES]
OPTIONS.append(("ROBOT", "A  light", "Don +4 semitones, light metal: still clearly Don", join([robotize(c, 4, 0.18, 0.35) for c in base])))
OPTIONS.append(("ROBOT", "B  strong", "Don +6 semitones, heavy metal: toy-robot Don", join([robotize(c, 6, 0.45, 0.6) for c in base])))

FPS, W = 10, 540
audio, frames = [], []
surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, W)
for grp, lab, note, a in OPTIONS:
    a = np.concatenate([np.zeros(int(0.5 * SR)), a, np.zeros(int(0.4 * SR))])
    n = int(np.ceil(len(a) / SR * FPS))
    a = np.concatenate([a, np.zeros(n * SR // FPS - len(a))])
    sf.write(f"{OUT}/{grp.replace('Í', 'I')}_{lab.split()[0]}_{lab.split()[1]}.wav", a, SR)
    c = cairo.Context(surf)
    c.set_source_rgb(0.91, 0.86, 0.76); c.paint()
    c.set_source_rgb(0.12, 0.16, 0.27)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    for txt, size, y in ((grp, 84, 210), (lab, 46, 300)):
        c.set_font_size(size); e = c.text_extents(txt); c.move_to((W - e.x_advance) / 2, y); c.show_text(txt)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    c.set_font_size(21); e = c.text_extents(note); c.move_to((W - e.x_advance) / 2, 360); c.show_text(note)
    surf.flush()
    frames += [bytes(surf.get_data())] * n
    audio.append(a)
mix = np.concatenate(audio)
sf.write("/tmp/day1_aud.wav", mix, SR)
p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{W}", "-r", str(FPS),
                      "-i", "-", "-i", "/tmp/day1_aud.wav", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
                      "-shortest", "day1_voice_auditions.mp4"], stdin=subprocess.PIPE)
for f in frames:
    p.stdin.write(f)
p.stdin.close(); p.wait()
print("total", round(len(mix) / SR, 1), "s;", [(g, l, round(len(a) / SR, 1)) for g, l, _, a in OPTIONS])
