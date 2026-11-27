"""Pick a Side (episode 14): the film's 14 lines, stage 2 of series/production-process.md (spoken lines v3, approved
23 Nov: "irasinek balsus"). Built from of_voices.py (episode 13), which is untouched. The series' own voices, no
auditions: Don am_onyx (sound_bc.don), the robot voice B (sound_bc.robot), Mom voice F (sound_fs.take: the aged voice,
its tail hiss cut), Pam voice A bf_emma (sound_xmas.pam_line, as in 8-12). Each take gets Whisper in three windows, a short
line the line before as context (lesson 121); then a timing file from script v4's shot table, each shot lengthened where
its take needs more than the script gave it, so the real length is known.
  python3 ps_voices.py takes   -> ps_voices/takes/<shot>.wav, takes.json
  python3 ps_voices.py timing  -> ../pick-a-side/ps_timing_v2.json, ps_voices_v2.mp4 (the lines at their times, with cards)
v2 (23 Nov, /grill-me "too few lines"): script v5, 19 lines: Sofía, the Client, Father, the robot and Mom one more each.
Needs the Kokoro model (KOKORO_DIR, default src/models) and ASR_DIR."""
import os
import sys
import json
import subprocess
import numpy as np
import soundfile as sf
import sound_ob as ob
import sound_bc as bc
import sound_fs as sfs
import re
import sound_xmas as sx
import dh_voices as dv

SR = 48000
OUT = "ps_voices/takes"
SCRIPT = "../pick-a-side/pick-a-side-script-v5.md"   # v1 (ps_voices_v1.py): script v4, 14 lines
# shot, who, the line, what the voice is given (None = the line), speed
LINES = [
    ("1.3", "DON", "This meeting does not exist.", "This. Meeting. Does not exist.", 0.88),     # a whisper, every word apart
    ("1.4", "DON", "My father has a meeting. Without me.", "My father has a meeting... Without me.", 0.94),
    ("2.3", "DON", "Pick a side.", "Pick. A. Side.", 0.92),                  # three hard words
    ("2.5", "DON", "Pam. My general.", "Pam. My general.", 0.92),          # solemn
    ("2.6", "MOM", "I don't pick sides, Donnie.", None, 1.0),
    ("2.9", "ROBOT", "Border breach. One heel.", None, 1.0),
    ("2.9b", "SOFIA", "Diplomatic heel.", None, 1.0),                    # v2: flat, not moving
    ("2.10a", "DON", "And you?", None, 1.0),
    ("2.10b", "ROBOT", "Both.", "Both. Sides.", 1.0),                    # v2 (26 Nov): cut after "Both" (CUT): alone,
                                                                           # the robot's "Both." was heard "Bose" 4/4
    ("3.1a", "ROBOT", "Smile. Recording.", None, 1.0),                   # v2
    ("3.1b", "MOM", "Chin up, Donnie.", None, 1.0),                      # v2: soft, from the tape
    ("3.3", "ROBOT", "Public post? Human approval required.", None, 1.0),
    ("3.4", "DON", "Approved.", None, 1.0),
    ("3.7", "PAM", "Some pose. Others notice.", None, 1.0),
    ("4.3a", "CLIENT", "That one.", None, 1.0),                          # v2: flat, pointing
    ("4.3b", "FATHER", "Invite her.", "Invite hur.", 1.0),                    # v2: calm; "her" spelt "hur": voice B swallowed it (0/3)
    ("5.3", "ROBOT", "Welcome.", None, 1.0),
    ("5.6", "PAM", "Some draw lines. Others cross them.", None, 1.0),
    ("6.1", "DON", "Everyone's with me.", None, 0.94),                     # sincere, warm
]
LEAD, TAIL = 0.15, 0.35          # a line starts 0.15 s into its shot and leaves 0.35 s after it


def take(who, txt, speed=1.0):
    if who == "DON":
        a = bc.don(txt, speed)
        return a * 0.75 if txt.startswith("This.") else a           # the whisper: quieter, the mix keeps it under
    if who == "PAM":
        return bc.norm(sx.pam_line(txt, "A"))
    if who == "ROBOT":
        return bc.robot(txt)
    if who == "SOFIA":
        return bc.sofia(txt, 0.95, g=0.10)                           # low, flat
    if who == "FATHER":
        return dv.father_line(txt)                                   # voice B, as in 12 and 13
    return sfs.take("", who, txt, None)                              # Mom (the aged voice, its tail hiss cut), the Client (flat)


def recognizer():
    import sherpa_onnx as so_
    d = os.environ.get("ASR_DIR", "/home/claude/models/asr/sherpa-onnx-whisper-base.en") + "/"
    return so_.OfflineRecognizer.from_whisper(encoder=d + "base.en-encoder.int8.onnx", decoder=d + "base.en-decoder.int8.onnx",
                                              tokens=d + "base.en-tokens.txt")


def takes(only=None):
    os.makedirs(OUT, exist_ok=True)
    r = recognizer()
    p = OUT + "/takes.json"
    meta = json.load(open(p)) if os.path.exists(p) else {}
    prev = None
    for shot, who, line, give, speed in LINES:
        if only and shot not in only:
            continue
        a = ob.trim(np.asarray(take(who, give or line, speed), dtype=np.float64))
        if shot in CUT:                                   # keep the first word of a longer reading (its "th" is spoken)
            a = a[:int(CUT[shot] * SR)].copy(); nf = int(0.025 * SR); a[-nf:] *= np.linspace(1, 0, nf)
        sf.write("%s/%s.wav" % (OUT, shot), a.astype(np.float32), SR)
        a16 = np.interp(np.linspace(0, len(a) - 1, int(len(a) * 16000 / SR)), np.arange(len(a)), a)
        pad = np.zeros(4800)
        heard = []
        for w in (a16, np.concatenate([pad, a16]), np.concatenate([a16, pad])):
            s = r.create_stream(); s.accept_waveform(16000, w.astype(np.float32)); r.decode_stream(s)
            heard.append(s.result.text.strip())
        good = sum(1 for h in heard if sfs._match(h, " ".join(sfs._words(line))))
        if good < 2 and prev is not None:              # lessons: a short line gets the line before as context
            pw, ptxt = prev
            p16 = np.interp(np.linspace(0, len(pw) - 1, int(len(pw) * 16000 / SR)), np.arange(len(pw)), pw)
            ctx = []
            for gap in (0.3, 0.5, 0.8):
                w = np.concatenate([p16, np.zeros(int(gap * 16000)), a16, pad])
                s = r.create_stream(); s.accept_waveform(16000, w.astype(np.float32)); r.decode_stream(s)
                ctx.append(s.result.text.strip())
            want = " ".join(sfs._words(line))
            cgood = sum(1 for h in ctx if sfs._match(h, want) or sfs._match(h, " ".join(sfs._words(ptxt + " " + line))))
            if cgood >= 2:
                heard += ["[with the line before] " + h for h in ctx]; good = cgood
        meta[shot] = dict(who=who, text=line, len=round(len(a) / float(SR), 2), asr=heard, ok=good)
        print("%-5s %-7s %4.2f s  %d/3  %-46s | %s" % (shot, who, len(a) / float(SR), good, line, heard[-1]), flush=True)
        prev = (a, line)
    json.dump(meta, open(p, "w"), indent=1)
    bad = [k for k, m in meta.items() if m["ok"] < 2]
    print("spoken: %.1f s; heard at least 2 of 3: %d of %d%s" % (sum(m["len"] for m in meta.values()),
          len(meta) - len(bad), len(meta), ("  FAILED: " + ", ".join(bad)) if bad else ""))
    if bad:
        sys.exit(1)


def shots():
    """Script v4's shot tables: | shot | at | s | size | picture | action | line | sound |."""
    out, scene = [], ""
    for ln in open(SCRIPT):
        if ln.startswith("## Scene"):
            scene = ln[3:].split("·")[0].strip() + " · " + ln.split("·")[1].strip()
        m = re.match(r"\| (\d\.\d+[a-z']*) \| \d:\d\d\.\d \| ([\d.]+) \|(.*)", ln)
        if m and scene:
            cells = [x.strip() for x in m.group(3).split("|")]
            out.append(dict(scene=scene, shot=m.group(1), script=float(m.group(2)), picture=cells[1],
                            line=cells[3] if cells[3] not in ("—", "") else None))
    return out


CUT = {"2.10b": 0.36}                                                    # shot: seconds kept


TAKES_OF = {"2.10": ("2.10a", "2.10b"), "3.1": ("3.1a", "3.1b"), "4.3": ("4.3a", "4.3b")}   # one shot, two lines


GAP = 0.25                                                            # between two lines in one shot ("And you?" / "Both.")


def timing(out_json="../pick-a-side/ps_timing_v2.json", out_mp4="../pick-a-side/ps_voices_v2.mp4"):
    meta = json.load(open(OUT + "/takes.json"))
    rows, t = [], 0.0
    for r in shots():
        ks = [k for k in TAKES_OF.get(r["shot"], (r["shot"],)) if k in meta]
        need = LEAD + sum(meta[k]["len"] for k in ks) + GAP * max(0, len(ks) - 1) + TAIL if ks else 0.0
        ln = round(max(r["script"], need), 2)
        at, offs = LEAD, []
        for k in ks:
            offs.append(round(at, 2)); at += meta[k]["len"] + GAP
        rows.append(dict(r, start=round(t, 2), len=ln, takes=ks, take_at=offs, longer=round(ln - r["script"], 2)))
        t += ln
    json.dump(dict(total=round(t, 2), script_total=round(sum(r["script"] for r in rows), 2), shots=rows), open(out_json, "w"), indent=1)
    print("script %.1f s -> with the takes %.1f s" % (sum(r["script"] for r in rows), t))
    for r in rows:
        if r["longer"] > 0:
            print("  %-5s +%.2f s  (%s)" % (r["shot"], r["longer"], " / ".join(meta[k]["text"] for k in r["takes"])))
    # the listening file: each line at its time, a card per shot (shot, who, the line, the picture in short)
    import cairo
    n = int(np.ceil(t * SR)); a = np.zeros(n)
    for r in rows:
        for k, off in zip(r["takes"], r["take_at"]):
            w, _ = sf.read("%s/%s.wav" % (OUT, k))
            i = int((r["start"] + off) * SR); a[i:i + len(w)] += w[:max(0, n - i)]
    wav = "/tmp/ps_voices.wav"; sf.write(wav, a, SR)
    fr = "/tmp/ps_cards"; os.makedirs(fr, exist_ok=True)
    for f in os.listdir(fr):
        os.remove(os.path.join(fr, f))
    lst = []
    for i, r in enumerate(rows):
        s = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(s)
        c.set_source_rgb(0.12, 0.13, 0.16); c.paint()
        def txt(x, y, size, s_, col=(0.95, 0.93, 0.88), bold=0):
            c.set_source_rgb(*col); c.select_font_face("Inter", 0, bold); c.set_font_size(size); c.move_to(x, y); c.show_text(s_)
        txt(30, 140, 18, "PICK A SIDE · voices v2 · %s" % r["scene"], (0.75, 0.75, 0.80))
        txt(30, 200, 44, r["shot"], bold=1)
        txt(150, 200, 22, "%d:%04.1f  ·  %.2f s%s" % (r["start"] // 60, r["start"] % 60, r["len"],
                                                      ("  (+%.2f)" % r["longer"]) if r["longer"] > 0 else ""), (0.75, 0.75, 0.80))
        y = 270
        if r["line"]:
            for part in _wrap(r["line"].replace("**", "").replace(" · ", " / "), 26):
                txt(30, y, 30, part, (1.0, 0.86, 0.35), 1); y += 40
            y += 20
        for part in _wrap(r["picture"].replace("**", ""), 44)[:14]:
            txt(30, y, 19, part); y += 27
        png = "%s/%03d.png" % (fr, i); s.write_to_png(png)
        lst.append("file '%s'\nduration %.3f\n" % (png, r["len"]))
    lst.append("file '%s'\n" % png)
    open(fr + "/list.txt", "w").write("".join(lst))
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", fr + "/list.txt", "-i", wav,
                           "-vf", "fps=30,format=yuv420p", "-af", "loudnorm=I=-16:TP=-2,aresample=48000", "-c:v", "libx264",
                           "-crf", "20", "-preset", "veryfast", "-c:a", "aac", "-b:a", "160k", "-t", "%.3f" % t, out_mp4])
    print("wrote", out_mp4)


def _wrap(s, n):
    out, cur = [], ""
    for w in s.split():
        if len(cur) + len(w) + 1 > n:
            out.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    return out + ([cur] if cur else [])


if __name__ == "__main__":
    if sys.argv[1] == "takes":
        takes(sys.argv[2:] or None)
    elif sys.argv[1] == "timing":
        timing()
