"""OFFICE NOIR 3: the narrator, clean, audition v3 (20 Nov). Tomas on audition v2: "a very dirty voice; how did we do
Don's voice in Noir 1?" Noir 1 (sound_on.noir_vo): a man low by nature (am_onyx), spoken at 1.1, lowered 2 semitones
only, a quarter of it darkened, a small room. No saturation, no compressor, no bass shelf, and the lowering was small.
Audition v2 was dirty because it had all three and a 5-semitone lowering by plain resampling.
Here, the Noir 1 recipe, with v2's written pauses and falling phrases kept:
  D   Noir 1 itself: Don's voice, as it narrated that film (for the ear)
  F2  the Client's voice (am_fenrir) through the Noir 1 recipe: 2 semitones, spoken at 0.95
  F3  the same, 3 semitones, spoken at 0.90
Writes ../office-noir-3/on3_narration_audition_v3.mp4
  KOKORO_DIR=/tmp/kokoro python3 on3_narr_clean.py"""
import os
import subprocess
import numpy as np
import soundfile as sf
import cairo

os.environ.setdefault("KOKORO_DIR", "/tmp/kokoro")
import sound_on as so
import sound_xmas as sx
import sound_ob as sob
import on3_narr_noir as nn

SR = so.SR
KINDS = {"D": ("am_onyx", 1.10, -2.0, "Noir 1: Don's voice, as it was"),
         "F2": ("am_fenrir", 0.95, -2.0, "the Client's voice, the Noir 1 way: 2 semitones, clean"),
         "F3": ("am_fenrir", 0.90, -3.0, "the same, 3 semitones, a little slower")}
KEYS = ["n1", "n2b", "n8", "n12", "n14"]


def clean(a, semis):
    a = so.pitch(a, semis)
    a = a * 0.75 + so.si.lp(a, 5) * 0.25
    a = so.room(a)
    return a / np.sqrt(np.mean(a ** 2)) * 0.12


def take(key, kind, pace=1.0):
    v, sp, semis, _ = KINDS[kind]
    sp = sp * pace
    parts = []
    for txt, gap in nn.PHRASES[key]:
        best = None
        for f in (1.0, 0.96, 1.04):                           # the phrase whose pitch falls most
            a = nn._trim(np.asarray(sx.say(txt, v, sp * f, "en-us"), dtype=np.float64)); a = a / np.sqrt(np.mean(a ** 2)) * 0.11
            p0, p1 = sob.slope(a)
            if best is None or p0 - p1 > best[1]:
                best = (a, p0 - p1)
        parts += [best[0], np.zeros(int(gap * SR / 2 ** (-semis / 12)))]
    return clean(np.concatenate(parts), semis)


def build(out="../office-noir-3/on3_narration_audition_v3.mp4"):
    files = []
    for kind in KINDS:
        seq = [np.zeros(int(0.5 * SR))]
        for key in KEYS:
            seq += [take(key, kind), np.zeros(int(0.7 * SR))]
        a = np.concatenate(seq); a = a / np.max(np.abs(a)) * 0.7
        os.makedirs("on3_voices/narr_audition_v3", exist_ok=True)
        wav = "on3_voices/narr_audition_v3/%s.wav" % kind; sf.write(wav, a.astype(np.float32), SR)
        s = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(s)
        c.set_source_rgb(0.07, 0.07, 0.08); c.paint(); c.set_source_rgb(0.93, 0.90, 0.82); c.select_font_face("Special Elite", 0, 0)
        c.set_font_size(150); e = c.text_extents(kind); c.move_to(270 - e.x_advance / 2, 420); c.show_text(kind)
        c.set_font_size(20); y, row = 520, ""
        for w in KINDS[kind][3].split():
            if c.text_extents(row + " " + w).x_advance > 440:
                c.move_to(50, y); c.show_text(row.strip()); y += 30; row = w
            else:
                row += " " + w
        c.move_to(50, y); c.show_text(row.strip())
        png, mp4 = "/tmp/_c_%s.png" % kind, "/tmp/_c_%s.mp4" % kind; s.write_to_png(png)
        subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-i", png, "-i", wav, "-vf",
                               "format=yuv420p,loop=-1:1,trim=duration=%.3f" % (len(a) / SR), "-c:v", "libx264", "-crf", "20", "-preset", "veryfast",
                               "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-shortest", mp4])
        files.append(mp4)
    open("/tmp/_c.txt", "w").write("".join("file '%s'\n" % p for p in files))
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", "/tmp/_c.txt", "-c", "copy", out])


if __name__ == "__main__":
    build()
