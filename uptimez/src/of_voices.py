"""The Offer (episode 13): the film's lines, stage 2 of series/production-process.md.
Voices as cast: the Client am_fenrir -4 (sound_ob.client_line, read flat), Father voice B (dh_voices), the robot and Don as
in episode 12. Each take gets Whisper in three windows (sound_fs._match), then a timing file: every shot of script v3
(of_script_v4.py; v1 used of_script_v3.py) lengthened where its line needs more than the script gave it, so the real length is known.
  python3 of_voices.py takes   -> of_voices/takes/<shot>.wav, takes.json
  python3 of_voices.py timing  -> ../the-offer/of_timing_v1.json, of_voices_v1.mp4 (the lines at their times, with cards)
Needs KOKORO_DIR and ASR_DIR."""
import os
import sys
import json
import subprocess
import numpy as np
import soundfile as sf
import sound_ob as ob
import sound_bc as bc
import sound_fs as sfs
import dh_voices as dv

SR = 48000
OUT = "of_voices/takes"
# shot, who, the line, what the voice is given (None = the line)
LINES = [
    ("0.5", "CLIENT", "Is it wrong?", None),
    ("0.9", "CLIENT", "Off the car.", None),
    ("1.4", "CLIENT", "Burn them. Your son loses his only customer.", None),
    ("2.1", "FATHER", "My son says his machine finds anything.", None),
    ("2.2", "CLIENT", "It found nothing.", None),
    ("2.4", "FATHER", "How would you run his company?", "How would you run his company."),   # flat: no question he needs answered
    ("2.5", "CLIENT", "Without him.", None),
    ("2.6", "FATHER", "And then?", "And then."),          # v2 (22 Nov, Tomas): "And?" was heard as "wind"
    ("2.8b", "CLIENT", "One month. I ask. She finds it.", None),
    ("2.8c", "FATHER", "Done.", None),
    ("2.9", "FATHER", "Put it in the calendar.", None),
    ("3.2", "ROBOT", "New meeting. Agenda: without him.", None),
    ("3.3", "DON", "Without who?", None),
    ("3.4b", "ROBOT", "Calendar says... you'll see.", "Calendar says. You'll see."),     # v3 (23 Nov): nobody answers
    ("3.5b", "DON", "Pam?", None),
]
LEAD, TAIL = 0.15, 0.35          # a line starts 0.15 s into its shot and leaves 0.35 s after it


def take(who, txt):
    if who == "FATHER":
        return dv.father_line(txt)
    if who == "DON":
        return bc.don(txt)
    return sfs.take("", who, txt, None)            # the Client (flat), the robot


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
    for shot, who, line, give in LINES:
        if only and shot not in only:
            continue
        a = ob.trim(np.asarray(take(who, give or line), dtype=np.float64))
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
    import of_script_v4 as s3
    out = []
    for title, where, sh in s3.S:
        for n, s, pic, line in sh:
            out.append(dict(scene=title, shot=n, script=s, picture=pic, line=line))
    return out


def timing(out_json="../the-offer/of_timing_v2.json", out_mp4="../the-offer/of_voices_v2.mp4"):
    meta = json.load(open(OUT + "/takes.json"))
    rows, t = [], 0.0
    for r in shots():
        L = meta.get(r["shot"])
        need = LEAD + L["len"] + TAIL if L else 0.0
        ln = round(max(r["script"], need), 2)
        rows.append(dict(r, start=round(t, 2), len=ln, take=r["shot"] if L else None, longer=round(ln - r["script"], 2)))
        t += ln
    json.dump(dict(total=round(t, 2), script_total=round(sum(r["script"] for r in rows), 2), shots=rows), open(out_json, "w"), indent=1)
    print("script %.1f s -> with the takes %.1f s" % (sum(r["script"] for r in rows), t))
    for r in rows:
        if r["longer"] > 0:
            print("  %-5s +%.2f s  (%s)" % (r["shot"], r["longer"], meta[r["take"]]["text"]))
    # the listening file: each line at its time, a card per shot (shot, who, the line, the picture in short)
    import cairo
    n = int(np.ceil(t * SR)); a = np.zeros(n)
    for r in rows:
        if r["take"]:
            w, _ = sf.read("%s/%s.wav" % (OUT, r["take"]))
            i = int((r["start"] + LEAD) * SR); a[i:i + len(w)] += w[:max(0, n - i)]
    wav = "/tmp/of_voices.wav"; sf.write(wav, a, SR)
    fr = "/tmp/of_cards"; os.makedirs(fr, exist_ok=True)
    for f in os.listdir(fr):
        os.remove(os.path.join(fr, f))
    lst = []
    for i, r in enumerate(rows):
        s = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(s)
        c.set_source_rgb(0.12, 0.13, 0.16); c.paint()
        def txt(x, y, size, s_, col=(0.95, 0.93, 0.88), bold=0):
            c.set_source_rgb(*col); c.select_font_face("Inter", 0, bold); c.set_font_size(size); c.move_to(x, y); c.show_text(s_)
        txt(30, 140, 18, "THE OFFER · voices v2 · %s" % r["scene"], (0.75, 0.75, 0.80))
        txt(30, 200, 44, r["shot"], bold=1)
        txt(150, 200, 22, "%d:%04.1f  ·  %.2f s%s" % (r["start"] // 60, r["start"] % 60, r["len"],
                                                      ("  (+%.2f)" % r["longer"]) if r["longer"] > 0 else ""), (0.75, 0.75, 0.80))
        y = 270
        if r["line"]:
            for part in _wrap(r["line"].replace('"', "\u201c", 1).replace('"', "\u201d", 1), 26):
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
