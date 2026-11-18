"""OFFICE NOIR 2: the animatic, v1. Storyboard v5 held for its timings, with scratch voices. 17 Nov.
What it is for: the length, and whether each shot has time for its line. It is not the film's sound: no music, no
room, no rain, one pop. The takes are first takes, not auditioned, and the speech check has not been run on them.
Timing: every frame gets the script's planned time; a frame with a line gets at least lead + take + tail; everything
is rounded up to a twelfth of a second, as the films are.
Writes  on2_voices/animatic_v1/*.wav and takes.json   the takes and their lengths
        on2_animatic_timing_v1.json                   every frame: start, length, line
        ../office-noir-2/on2_animatic_v1.mp4          540 x 960, 30 fps
  KOKORO_DIR=/tmp/kokoro python3 on2_animatic.py [folder]"""
import json
import math
import os
import subprocess
import sys
import cairo
import numpy as np
import soundfile as sf

os.environ.setdefault("KOKORO_DIR", "/tmp/kokoro")
import on2_board as b
import sound_on as so
import sound_bc as bc
import sound_ob as sob
import sound_xmas as sx

V = "v1"
SR = so.SR
VOICES = "on2_voices/animatic_" + V
LEAD, TAIL = 0.25, 0.42
W, H, FPS = b.W, b.H, 30
SAFE = (18, 96, 522, 820)

# frame index in on2_board.FRAMES -> [(who, caption, take key)]
LINES = {
    "1.1": [("N", "New Year's Eve.", "n1")],
    "2.1": [("N", "A woman like me doesn't walk alone.", "n2")],
    "2.6": [("N", "I don't run. I give them something to chase.", "n3")],
    "5.3": [("SOFÍA", "The usual.", "s1")],
    "5.4": [("N", "He sent a note. They always send a note.", "n4")],
    "6.2": [("N", "Everybody had lost it. I found it in one drawer.", "n5")],
    "7.2": [("MOM", "You! Not near Donnie's desk!", "m1"), ("THE SHADOW", "I only want my—", "c1")],
    "8.1": [("MOM", "Happy New Year, dear.", "m2")],
    "8.5": [("PAM", "Some dream. Others sweep.", "p1")],
}


def trim(a, thr=0.012):
    idx = np.where(np.abs(a) > thr * np.max(np.abs(a)) / 0.1)[0]
    if not len(idx):
        return a
    return a[max(0, idx[0] - int(0.02 * SR)):min(len(a), idx[-1] + int(0.10 * SR))]


def takes():
    os.makedirs(VOICES, exist_ok=True)
    narr = lambda t: so._sof(so.SOF, None, 0.0, 0.95, -2.0, t)          # her voice, two semitones down: the first film's audition
    pv, psp, _ = sx.PAMS["A"]
    made = {
        "n1": narr("New Year's Eve."),
        "n2": narr("A woman like me doesn't walk alone."),
        "n3": narr("I don't run. I give them something to chase."),
        "n4": narr("He sent a note. They always send a note."),
        "n5": narr("Everybody had lost it. I found it in one drawer."),
        "s1": bc.sofia("The usual."),
        "m1": bc.mom_shout("You! Not near Donnie's desk!"),
        "c1": sob.client_line("I only want my"),
        "m2": bc.mom("Happy New Year, dear."),
        "p1": bc.norm(so.dry("Some dream. Others sweep.", pv, 1.0)),      # two sentences at pace 1.0: what the mix heard in The Onboarding
    }
    meta = {}
    for key, a in made.items():
        a = trim(np.asarray(a, dtype=np.float64))
        if key == "m1":
            a = a / np.sqrt(np.mean(a ** 2)) * 0.15
        if key == "c1":                                                  # cut off by the pop
            a = so.cut_off(a, len(a) / SR - 0.06)
        sf.write("%s/%s.wav" % (VOICES, key), a.astype(np.float32), SR)
        meta[key] = round(len(a) / SR, 3)
    json.dump(meta, open(VOICES + "/takes.json", "w"), indent=1)
    return meta


def up12(x):
    return math.ceil(x * 12 - 1e-6) / 12.0


def timing(meta):
    fr = b.FRAMES
    out, t = [], 0.0
    for i, (sid, t0, fn, tilt, colour, said, post) in enumerate(fr):
        planned = (fr[i + 1][1] - t0) if i + 1 < len(fr) else 2.0
        cues, need = [], 0.0
        for who, cap, key in LINES.get(sid, []) if (sid not in ("4.1", "6.7") or True) else []:
            pass
        lines = LINES.get(sid, [])
        if sid in ("4.1", "6.7"):
            lines = []
        at = LEAD
        for who, cap, key in lines:
            cues.append({"who": who, "caption": cap, "take": key, "at": round(at, 3), "len": meta[key]})
            at += meta[key] + 0.15
        if cues:
            need = at - 0.15 + (0.04 if sid == "7.2" else TAIL)          # the pop cuts the Shadow off
        dur = up12(max(planned, need))
        out.append({"n": i + 1, "shot": sid, "start": round(t, 4), "len": round(dur, 4), "planned": round(planned, 3), "cues": cues})
        t += dur
    return out


def caption(sf_, cues):
    """The lines of this frame, in a band above the bottom of the safe area. Narration is in italics."""
    cc = cairo.Context(sf_)
    rows = []
    for cu in cues:
        txt = cu["caption"] if cu["who"] == "N" else "%s: %s" % (cu["who"], cu["caption"])
        cc.select_font_face("Inter", cairo.FONT_SLANT_ITALIC if cu["who"] == "N" else cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cc.set_font_size(23)
        line = ""
        for wd in txt.split():
            trial = (line + " " + wd).strip()
            if cc.text_extents(trial).x_advance > SAFE[2] - SAFE[0] - 36 and line:
                rows.append((line, cu["who"] == "N")); line = wd
            else:
                line = trial
        rows.append((line, cu["who"] == "N"))
    hh = len(rows) * 30 + 22
    y0 = SAFE[3] - hh
    cc.set_source_rgba(0.04, 0.04, 0.06, 0.82); cc.rectangle(SAFE[0], y0, SAFE[2] - SAFE[0], hh); cc.fill()
    for j, (line, it) in enumerate(rows):
        cc.select_font_face("Inter", cairo.FONT_SLANT_ITALIC if it else cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cc.set_font_size(23); cc.set_source_rgb(1, 1, 1)
        e = cc.text_extents(line); cc.move_to((W - e.x_advance) / 2, y0 + 33 + j * 30); cc.show_text(line)


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(r.stderr[-2000:])
    return r


def main(folder):
    meta = takes()
    T = timing(meta)
    json.dump(T, open("on2_animatic_timing_%s.json" % V, "w"), indent=1)
    total = T[-1]["start"] + T[-1]["len"]
    tmp = "/tmp/on2/anim_" + V
    os.makedirs(tmp, exist_ok=True)
    lst = []
    for i, row in enumerate(T):
        sf_ = b.render(i)
        if row["cues"]:
            caption(sf_, row["cues"])
        png = "%s/f_%02d.png" % (tmp, i); sf_.write_to_png(png)
        seg, part = "%s/s_%02d.mp4" % (tmp, i), "%s/s_%02d.part.mp4" % (tmp, i)
        run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", png, "-vf",
             "format=yuv420p,loop=-1:1,trim=duration=%.5f" % row["len"], "-c:v", "libx264", "-crf", "18", "-preset", "veryfast",
             "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-r", str(FPS), part])
        os.replace(part, seg)
        lst.append("file '%s'" % seg)
    open(tmp + "/list.txt", "w").write("\n".join(lst) + "\n")
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", tmp + "/list.txt", "-c", "copy", tmp + "/video.mp4"])
    mix = np.zeros(int((total + 0.5) * SR))
    for row in T:
        for cu in row["cues"]:
            a, _ = sf.read("%s/%s.wav" % (VOICES, cu["take"]))
            p = int((row["start"] + cu["at"]) * SR); mix[p:p + len(a)] += a[:len(mix) - p]
        if row["shot"] == "7.3":
            a = np.asarray(so.pop(), dtype=np.float64)
            a = a / np.max(np.abs(a)) * 0.6
            p = int(row["start"] * SR); mix[p:p + len(a)] += a[:len(mix) - p]
    mix = np.tanh(mix * 2.2) / 2.2 * 1.6
    sf.write(tmp + "/mix.wav", mix.astype(np.float32), SR)
    out = "%s/on2_animatic_%s.mp4" % (folder, V)
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp + "/video.mp4", "-i", tmp + "/mix.wav", "-map", "0:v", "-map", "1:a",
         "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-shortest", tmp + "/out.part.mp4"])
    os.replace(tmp + "/out.part.mp4", out)
    return out, T, total


if __name__ == "__main__":
    out, T, total = main(sys.argv[1] if len(sys.argv) > 1 else "../office-noir-2")
    print("wrote", out, "%.2f s" % total, len(T), "frames")
    for row in T:
        if row["len"] > row["planned"] + 0.01:
            print("  %2d  %-5s planned %.2f -> %.2f  (%s)" % (row["n"], row["shot"], row["planned"], row["len"], ", ".join(c["take"] for c in row["cues"])))
