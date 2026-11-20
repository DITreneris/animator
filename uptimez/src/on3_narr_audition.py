"""OFFICE NOIR 3: the narrator's audition, v1 (20 Nov). Tomas: "the voice has to be slower and heavier; now it is a silly
narrator's voice". The film's take is am_fenrir played 4 semitones down by resampling: that lowers the throat with the
pitch, which is what sounds slow-witted. Three ways to be heavier without it; the same three lines each.
  NOW  as in animatic v5 (for comparison)
  A    the same man, 2 semitones down only, spoken 15% slower
  B    A, 24% slower, with a breath between sentences
  C    another man, low by nature (bm_lewis), 1 semitone down, spoken 15% slower
Writes ../office-noir-3/on3_narration_audition_v1.mp4 and on3_voices/narr_audition_v1/*.wav
  KOKORO_DIR=/tmp/kokoro python3 on3_narr_audition.py"""
import os
import re
import subprocess
import cairo
import numpy as np
import soundfile as sf

os.environ.setdefault("KOKORO_DIR", "/tmp/kokoro")
import sound_on as so
import sound_bc as bc
import sound_ob as sob

SR = so.SR
OUT = "on3_voices/narr_audition_v1"
LINES = ["They say I know how business is done.", "I don't break. I break even.", "But I didn't quit."]
KINDS = {"NOW": ("am_fenrir", 1.00, -4.0, 0.0, "as in the film now"),
         "A": ("am_fenrir", 0.85, -2.0, 0.0, "the same man, less lowered, spoken slower"),
         "B": ("am_fenrir", 0.76, -2.0, 0.38, "A, slower still, a breath between sentences"),
         "C": ("bm_lewis", 0.85, -1.0, 0.0, "another man, low by nature")}


def say(txt, kind):
    v, sp, semis, gap, _ = KINDS[kind]
    parts = [p for p in re.split(r"(?<=[.!?])\s+", txt) if p] if gap else [txt]
    out = []
    for i, p in enumerate(parts):
        a = np.asarray(so.dry(p, v, sp), dtype=np.float64)
        idx = np.where(np.abs(a) > 0.02 * np.max(np.abs(a)))[0]; a = a[max(0, idx[0] - 400):idx[-1] + 2400]
        out.append(a)
        if i < len(parts) - 1:
            out.append(np.zeros(int(gap * SR)))
    return bc.norm(sob.warm(so.pitch(np.concatenate(out), semis)))


def card(kind, path):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(s)
    c.set_source_rgb(0.07, 0.07, 0.08); c.paint()
    c.set_source_rgb(0.93, 0.90, 0.82); c.select_font_face("Special Elite", 0, 0)
    c.set_font_size(150); e = c.text_extents(kind); c.move_to(270 - e.x_advance / 2, 420); c.show_text(kind)
    c.set_font_size(22); y = 520
    row = ""
    for w in KINDS[kind][4].split():
        if c.text_extents(row + " " + w).x_advance > 440:
            c.move_to(50, y); c.show_text(row.strip()); y += 32; row = w
        else:
            row += " " + w
    c.move_to(50, y); c.show_text(row.strip())
    s.write_to_png(path)


def build(out="../office-noir-3/on3_narration_audition_v1.mp4"):
    os.makedirs(OUT, exist_ok=True)
    parts, lens = [], {}
    for kind in KINDS:
        a = [np.zeros(int(0.5 * SR))]
        for ln in LINES:
            t = say(ln, kind); a += [t, np.zeros(int(0.6 * SR))]; lens.setdefault(kind, []).append(round(len(t) / SR, 2))
        a = np.concatenate(a); a = a / np.max(np.abs(a)) * 0.7
        wav, png, mp4 = "%s/%s.wav" % (OUT, kind), "/tmp/_aud_%s.png" % kind, "/tmp/_aud_%s.mp4" % kind
        sf.write(wav, a.astype(np.float32), SR); card(kind, png)
        subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-i", png, "-i", wav, "-vf",
                               "format=yuv420p,loop=-1:1,trim=duration=%.3f" % (len(a) / SR), "-c:v", "libx264", "-crf", "20", "-preset", "veryfast",
                               "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-shortest", mp4])
        parts.append(mp4)
    open("/tmp/_aud.txt", "w").write("".join("file '%s'\n" % p for p in parts))
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", "/tmp/_aud.txt", "-c", "copy", out])
    return lens


if __name__ == "__main__":
    print(build())
