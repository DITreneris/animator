"""THE DOUBLE AGENT (episode 15): the rough cut v1 (28 Nov; Tomas /grill-me: rough cut now, "Keep infiltrating." dropped,
room tone + stings only, no theme).

Joins the scene renders 1-7 as they stand and builds 8.1 + 9.1 from the S8 v12 layers (da_push91, V "v12"):
8.1 = the 1.5 s pull-back, then S8 v12 held to 4.24 s with Pam's "Some take sides. Others take notes." from 1.4 s;
9.1 = the 1.8 s push, its last drawing 1.1's frame 0 (S8r v5). One loudnorm pass on the whole film (-15 LUFS, TP -1.5).

  python3 da_roughcut.py   ->  ../the-double-agent/da_roughcut_v1.mp4 (540x960, 30 fps; not committed)
"""
import os
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.join(HERE, "..", "the-double-agent")
FPS, SR = 30, 48000
VER = 1
SCENES = ["da_anim_s1_v22", "da_anim_s2_v7", "da_anim_s3_v10", "da_anim_s4_v7", "da_anim_s5_v7", "da_anim_s6_v7",
          "da_anim_s7_v4"]
LEN81, LEN91 = 4.24, 1.8                                       # da_timing_v4
TAKE81 = ("B", 1.4)                                            # da_timing_v4's pick and take_at


def frames_89(tmp):
    """8.1 + 9.1 drawings at 540x960, written as PNGs; returns the count."""
    sys.path.insert(0, HERE)
    import da_push91 as pu
    from PIL import Image
    pu.V[0] = "v12"
    pull = pu.pull81(EP)
    push = pu.main(EP)
    hold = Image.open(os.path.join(EP, pu.FILES["v12"][0])).convert("RGB")
    n81 = int(round(LEN81 * FPS))
    seq = pull + [hold] * (n81 - len(pull)) + push
    for i, im in enumerate(seq):
        im.resize((540, 960), Image.LANCZOS).save(os.path.join(tmp, "%04d.png" % i))
    return len(seq), n81


def audio_89(n, n81, path):
    import da_animatic as AN
    import soundfile as sf
    sec = n / FPS
    m = 0.004 * AN._lp(AN._noise(sec + 0.1), 200)[:int(sec * SR)]
    fx = dict(AN.FX)
    for t0, word, gain in ((0.2, "squeaks of the tug", 0.35), (1.0, "pen", 0.5),
                           (n81 / FPS + 0.4, "tug's squeak", 0.6)):
        w = fx[word](); i = int(t0 * SR)
        m[i:i + len(w)] += 0.18 * gain / (np.max(np.abs(w)) + 1e-9) * w[:max(0, len(m) - i)]
    a, _ = sf.read(os.path.join(HERE, "da_voices", "takes", "8.1_%s.wav" % TAKE81[0]))
    if a.ndim > 1:
        a = a.mean(axis=1)
    i_ = np.where(np.abs(a) > 0.02 * np.abs(a).max())[0]; a = a[i_[0]:i_[-1]]
    i = int(TAKE81[1] * SR)
    m[i:i + len(a)] += 0.6 * a[:max(0, len(m) - i)] / (np.max(np.abs(a)) + 1e-9)
    m /= max(1.0, np.max(np.abs(m)) / 0.89)
    m.astype(np.float32).tofile(path)


def build():
    tmp = "/tmp/da_roughcut"; os.makedirs(tmp, exist_ok=True)
    for f in os.listdir(tmp):
        os.remove(os.path.join(tmp, f))
    n, n81 = frames_89(tmp)
    audio_89(n, n81, os.path.join(tmp, "a89.f32"))
    seg = os.path.join(tmp, "s89.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", os.path.join(tmp, "%04d.png"),
                    "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", os.path.join(tmp, "a89.f32"),
                    "-map", "0:v", "-map", "1:a", "-vf", "format=yuv420p", "-c:v", "libx264", "-preset", "veryfast",
                    "-crf", "16", "-c:a", "pcm_s16le", "-shortest", seg.replace(".mp4", ".mov")], check=True)
    ins = [os.path.join(EP, s + ".mp4") for s in SCENES] + [seg.replace(".mp4", ".mov")]
    args = ["ffmpeg", "-v", "error", "-y"]
    for f in ins:
        args += ["-i", f]
    k = len(ins)
    fil = "".join("[%d:v]setpts=PTS-STARTPTS,fps=30[v%d];[%d:a]aresample=48000,aformat=channel_layouts=mono,"
                  "asetpts=PTS-STARTPTS[a%d];" % (i, i, i, i) for i in range(k))
    fil += "".join("[v%d][a%d]" % (i, i) for i in range(k)) + "concat=n=%d:v=1:a=1[v][a];" % k
    fil += "[a]loudnorm=I=-15:TP=-1.5:LRA=11,aresample=48000,volume=3.6dB,alimiter=limit=0.6:level=false[an]"   # (AAC overshoots: CLAUDE.md)
    out = os.path.join(EP, "da_roughcut_v%d.mp4" % VER)
    args += ["-filter_complex", fil, "-map", "[v]", "-map", "[an]", "-c:v", "libx264", "-preset", "veryfast",
             "-crf", "18", "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709",
             "-colorspace", "bt709", "-c:a", "aac", "-b:a", "160k", out]
    subprocess.run(args, check=True)
    print("wrote", out)
    return out


if __name__ == "__main__":
    build()
