"""Shared helpers: unpack a GIF into PNG frames, write an ffmpeg concat list
with per-frame durations, and save a mono WAV."""
import os
import wave

import numpy as np
from PIL import Image

SR = 44100


def unpack(gif, out_dir):
    """Save every GIF frame as out_dir/frames/NNN.png and return the frame count."""
    os.makedirs(f"{out_dir}/frames", exist_ok=True)
    im = Image.open(gif)
    for i in range(im.n_frames):
        im.seek(i)
        im.convert("RGB").save(f"{out_dir}/frames/{i:03d}.png")
    return im.n_frames


def write_concat(out_dir, dur_ms):
    """Concat-demuxer list; the last frame is repeated so its duration is honoured."""
    n = len(dur_ms)
    with open(f"{out_dir}/list.txt", "w") as f:
        for i, d in enumerate(dur_ms):
            f.write(f"file 'frames/{i:03d}.png'\nduration {d / 1000}\n")
        f.write(f"file 'frames/{n - 1:03d}.png'\n")
    starts = np.cumsum([0] + list(dur_ms[:-1])) / 1000
    return starts, sum(dur_ms) / 1000


def env(n, a, d):
    """Attack-then-exponential-decay envelope, n samples long."""
    t = np.arange(n) / SR
    return np.minimum(t / max(a, 1e-5), 1) * np.exp(-t / d)


def put(buf, sig, t, g=1.0):
    """Mix sig into buf at time t (seconds), clipped to the buffer end."""
    s = int(t * SR)
    if s >= len(buf):
        return
    e = min(len(buf), s + len(sig))
    buf[s:e] += g * sig[: e - s]


def save_wav(path, x, peak=0.9):
    x = x / np.abs(x).max() * peak
    with wave.open(path, "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())
