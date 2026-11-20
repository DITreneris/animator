"""OFFICE NOIR 3: a new voice for Don, audition v1 (20 Nov). Tomas: the narrator takes Don's voice (am_onyx, the Noir 1
recipe); Don, who has three short lines in this film, gets another. It has to be told from the narrator at once: higher,
quicker, drier (no lowering, no room). Each card: the narrator says one line first, then the candidate says Don's lines.
  KOKORO_DIR=/tmp/kokoro python3 on3_don_audition.py -> ../office-noir-3/on3_don_audition_v1.mp4"""
import os
import subprocess
import numpy as np
import soundfile as sf
import cairo

os.environ.setdefault("KOKORO_DIR", "/tmp/kokoro")
import sound_on as so
import sound_bc as bc

SR = so.SR
LINES = ["Just looking.", "The woman in the photo…", "Recognize her?", "Case closed."]
KINDS = {"1": ("am_michael", 1.08, "en-us", "American, lighter, brisk"),
         "2": ("am_eric", 1.08, "en-us", "American, dry, matter of fact"),
         "3": ("bm_daniel", 1.05, "en-gb", "British, a detective with a glass")}


def build(out="../office-noir-3/on3_don_audition_v1.mp4"):
    narr = so.noir_vo("It was a fair fight.")
    files = []
    os.makedirs("on3_voices/don_audition_v1", exist_ok=True)
    for kind, (v, sp, lang, note) in KINDS.items():
        seq = [np.zeros(int(0.5 * SR)), narr, np.zeros(int(0.8 * SR))]
        for ln in LINES:
            seq += [bc.norm(so.dry(ln, v, sp, lang)), np.zeros(int(0.6 * SR))]
        a = np.concatenate(seq); a = a / np.max(np.abs(a)) * 0.7
        wav = "on3_voices/don_audition_v1/%s.wav" % kind; sf.write(wav, a.astype(np.float32), SR)
        s = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(s)
        c.set_source_rgb(0.07, 0.07, 0.08); c.paint(); c.set_source_rgb(0.93, 0.90, 0.82); c.select_font_face("Special Elite", 0, 0)
        c.set_font_size(56); c.move_to(50, 330); c.show_text("DON")
        c.set_font_size(150); c.move_to(50, 470); c.show_text(kind)
        c.set_font_size(20); c.move_to(50, 540); c.show_text(note)
        c.move_to(50, 600); c.show_text("first the narrator, then Don")
        png, mp4 = "/tmp/_d_%s.png" % kind, "/tmp/_d_%s.mp4" % kind; s.write_to_png(png)
        subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-i", png, "-i", wav, "-vf",
                               "format=yuv420p,loop=-1:1,trim=duration=%.3f" % (len(a) / SR), "-c:v", "libx264", "-crf", "20", "-preset", "veryfast",
                               "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-shortest", mp4])
        files.append(mp4)
    open("/tmp/_d.txt", "w").write("".join("file '%s'\n" % p for p in files))
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", "/tmp/_d.txt", "-c", "copy", out])


if __name__ == "__main__":
    build()
