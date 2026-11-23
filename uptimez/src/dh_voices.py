"""Voice auditions for "Daddy's Home" (episode 12): Father and the coffee-machine repairman (the VISITOR).
Father is Don aged: lower, slower, never raised. Don is am_onyx (about 94 Hz); the Client is am_fenrir -4 and is not
used here, so the three big men stay apart. Each card: the voice's own lines, then against Don's.
  python3 dh_voices.py takes     -> dh_voices/audition/<letter>_<tag>.wav, measured, Whisper on each
  python3 dh_voices.py audition  -> ../daddys-home/dh_father_voices_v1.mp4, dh_visitor_voices_v1.mp4
Needs KOKORO_DIR and, for the check, ASR_DIR."""
import os
import sys
import json
import subprocess
import numpy as np
import soundfile as sf
import sound_on as so
import sound_bc as bc
import sound_ob as ob
import sound_fs as sfs

SR = 48000
OUT = "dh_voices/audition"
FATHER_LINES = [("donnie", "Donnie."), ("people", "My people come first. Five o'clock."), ("today", "Today."),
                ("approved", "Approved."), ("green", "I prefer green in cash."), ("money", "Good. Find my money."),
                ("answer", "Answer it.")]
VISITOR_LINES = [("inspect", "I'm here to inspect the machine."), ("fixed", "Fixed."), ("coffee", "Coffee machine.")]
# letter -> (voice or (voice, voice, share of the second), speed, semitones, note)
FATHER = {
    "A": ("am_onyx", 0.82, -3.0, "Don's own voice, aged: slower, three semitones down"),
    "B": (("am_onyx", "bm_george", 0.45), 0.84, -3.0, "Don with an older, drier grain"),
    "C": ("bm_george", 0.86, -4.0, "a different man: old, dry, clipped"),
    "D": (("am_onyx", "am_michael", 0.40), 0.80, -5.0, "the lowest and slowest"),
}
VISITOR = {
    "A": ("am_adam", 1.00, -1.0, "dry and practical"),
    "B": ("am_liam", 0.96, -2.0, "even, a little bored"),
    "C": ("am_puck", 0.98, -2.5, "lighter, a tradesman"),
}
# CHOSEN (21 Nov, Tomas, by ear, from dh_father_voices_v1.mp4 and dh_visitor_voices_v1.mp4): Father B, the repairman A.
FATHER_VOICE, VISITOR_VOICE = "B", "A"


def father_line(txt):
    return one(FATHER[FATHER_VOICE], txt)


def visitor_line(txt):
    return one(VISITOR[VISITOR_VOICE], txt)


DON_REPLY = {"father": ("Yes, Dad.", "Tomorrow?"), "visitor": ("Of course. We've been expecting you.", "With our AI?")}


def one(spec, txt):
    v, sp, semis, _ = spec
    voice = so.blend(v[0], v[1], v[2]) if isinstance(v, tuple) else v
    return ob.trim(np.asarray(bc.norm(ob.warm(so.pitch(so.dry(txt, voice, sp), semis))), dtype=np.float64))


def takes():
    os.makedirs(OUT, exist_ok=True)
    import sherpa_onnx as so_
    d = os.environ.get("ASR_DIR", "/home/claude/models/asr/sherpa-onnx-whisper-base.en") + "/"
    r = so_.OfflineRecognizer.from_whisper(encoder=d + "base.en-encoder.int8.onnx", decoder=d + "base.en-decoder.int8.onnx",
                                          tokens=d + "base.en-tokens.txt")
    meta = {"_don_f0": round(float(bc.f0(bc.don("Zero results. In 0.2 seconds."))))}
    for who, cands, lines in (("father", FATHER, FATHER_LINES), ("visitor", VISITOR, VISITOR_LINES)):
        for letter, spec in cands.items():
            f0s, tot, ok = [], 0.0, 0
            for tag, txt in lines:
                a = one(spec, txt)
                sf.write("%s/%s_%s_%s.wav" % (OUT, who, letter, tag), a.astype(np.float32), SR)
                a16 = np.interp(np.linspace(0, len(a) - 1, int(len(a) * 16000 / SR)), np.arange(len(a)), a)
                pad = np.zeros(4800)
                heard = []
                for w in (a16, np.concatenate([pad, a16]), np.concatenate([a16, pad])):
                    s = r.create_stream(); s.accept_waveform(16000, w.astype(np.float32)); r.decode_stream(s)
                    heard.append(s.result.text.strip())
                good = sum(1 for h in heard if sfs._match(h, " ".join(sfs._words(txt))))
                ok += good >= 2
                f0s.append(float(bc.f0(a))); tot += len(a) / float(SR)
                meta["%s_%s_%s" % (who, letter, tag)] = dict(len=round(len(a) / float(SR), 2), asr=heard, ok=good)
                print("%-7s %s %-8s %4.2f s  %d/3  %s" % (who, letter, tag, len(a) / float(SR), good, heard[0]), flush=True)
            meta["%s_%s" % (who, letter)] = dict(f0=round(float(np.median(f0s))), total=round(tot, 2), lines_ok=ok, of=len(lines))
            print("== %s %s: %d Hz, %.2f s spoken, %d of %d lines heard" % (who, letter, np.median(f0s), tot, ok, len(lines)), flush=True)
    json.dump(meta, open(OUT + "/measure.json", "w"), indent=1)


def audition(who):
    import cairo
    cands, lines = (FATHER, FATHER_LINES) if who == "father" else (VISITOR, VISITOR_LINES)
    meta = json.load(open(OUT + "/measure.json"))
    gap = lambda s: np.zeros(int(s * SR))
    don = [ob.trim(np.asarray(bc.don(t), dtype=np.float64)) for t in DON_REPLY[who]]
    parts = []
    for letter, spec in cands.items():
        t = {tag: sf.read("%s/%s_%s_%s.wav" % (OUT, who, letter, tag))[0] for tag, _ in lines}
        seq = [gap(0.5)]
        for tag, _ in lines:
            seq += [t[tag], gap(0.5)]
        if who == "father":                                   # then against Don: the call, and the ending
            seq += [gap(0.5), t["people"], gap(0.25), don[1], gap(0.25), t["today"], gap(0.8), t["money"], gap(0.9)]
        else:
            seq += [gap(0.5), t["inspect"], gap(0.25), don[0], gap(0.8), t["fixed"], gap(0.3), don[1], gap(0.25), t["coffee"], gap(0.9)]
        a = np.concatenate(seq)
        FPS = 10
        nfr = int(np.ceil(len(a) / float(SR) * FPS)); a = np.concatenate([a, np.zeros(nfr * SR // FPS - len(a))])
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 540); c = cairo.Context(surf)
        c.set_source_rgb(0.16, 0.05, 0.08) if who == "father" else c.set_source_rgb(0.10, 0.11, 0.13); c.paint()
        v = spec[0]; name = v if isinstance(v, str) else "%s + %d%% %s" % (v[0], round(v[2] * 100), v[1])
        m = meta["%s_%s" % (who, letter)]
        rows = [(("FATHER " if who == "father" else "REPAIRMAN ") + letter, 50, 110, 1), (name, 20, 160, 0),
                ("speed %.2f  ·  %+.1f semitones" % (spec[1], spec[2]), 17, 190, 0),
                ("%d Hz  ·  Don %d Hz" % (m["f0"], meta["_don_f0"]), 17, 218, 0), (spec[3], 18, 262, 0),
                ("his lines: %.1f s  ·  Whisper %d of %d" % (m["total"], m["lines_ok"], m["of"]), 16, 300, 0),
                ("first each line alone,", 15, 380, 0), ("then against Don", 15, 402, 0)]
        for txt, size, y, bold in rows:
            c.set_source_rgb(0.96, 0.90, 0.78); c.select_font_face("Inter", 0, bold); c.set_font_size(size)
            e = c.text_extents(txt); c.move_to(270 - e.x_advance / 2, y); c.show_text(txt)
        png = "/tmp/dh_aud_%s_%s.png" % (who, letter); wav = png[:-3] + "wav"; tmp = png[:-4] + ".tmp.mp4"; mp4 = png[:-3] + "mp4"
        surf.write_to_png(png); sf.write(wav, a, SR); d = len(a) / float(SR)
        subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", png, "-i", wav, "-vf",
                               "format=yuv420p,loop=-1:1,trim=duration=%.3f" % d, "-af", "loudnorm=I=-16:TP=-2,aresample=48000",
                               "-c:v", "libx264", "-crf", "20", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-r", str(FPS),
                               "-c:a", "aac", "-b:a", "160k", "-t", "%.3f" % d, tmp])
        os.rename(tmp, mp4); parts.append(mp4)
    out = "../daddys-home/dh_%s_voices_v1.mp4" % who
    open("/tmp/dh_aud.txt", "w").write("".join("file '%s'\n" % p for p in parts))
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", "/tmp/dh_aud.txt", "-c", "copy",
                           out + ".tmp.mp4"])
    os.rename(out + ".tmp.mp4", out); print("wrote", out)


if __name__ == "__main__" and sys.argv[1] in ("takes", "audition"):
    if sys.argv[1] == "takes":
        takes()
    else:
        audition("father"); audition("visitor")


# ---------------------------------------------------------------- the film's lines (script v1.4, spoken lines v2), 21 Nov
# key (shot), who, the line, what the voice is given (None = the line), how
FILM_OUT = "dh_voices/film_v1"
FILM = [
    ("0.3", "FATHER", "Donnie.", None, None),
    ("0.4", "DON", "Dad! Great timing!", None, "bright"),
    ("0.5", "FATHER", "My men go in first. I arrive at five.", None, None),
    ("0.6", "DON", "Tomorrow?", None, "small"),
    ("0.7", "FATHER", "Today.", None, None),
    ("1.2", "DON", "Good news, everyone! My father's coming!", None, "bright"),
    ("1.3", "SOFIA", "Is he coming alone?", None, "low"),
    ("2.2", "DON", "I didn't steal anything!", None, "fast"),
    ("2.3", "DON", "The money was invested.", None, None),
    ("2.4", "PAM", "Into what?", None, None),
    ("3.1", "DON", "Make it green.", None, None),
    ("3.2", "ROBOT", "Human approval required.", None, None),
    ("3.3", "DON", "Approved.", None, None),
    ("3.4", "PAM", "It's still one.", None, None),
    ("3.5", "DON", "He won't count.", None, None),
    ("4.1", "MOM", "He once fired a man for sitting in that chair.", None, None),
    ("4.3", "MOM", "Different chair.", None, None),
    ("5.2", "VISITOR", "I'm here to inspect the machine.", None, None),
    ("5.3", "DON", "Of course. We've been expecting you.", None, "warm"),
    ("6.1a", "DON", "Complete transparency.", None, "warm"),
    ("6.1b", "DON", "Lifetime Premium. On us.", None, "warm"),
    ("6.2", "ROBOT", "Premium search is non-functional.", "Premium search is non functional.", None),
    ("6.3", "DON", "Then make it lifetime.", None, None),
    ("7.3b", "ROBOT", "Incident logged. CEO responsible.", "Incident logged. C.E.O. responsible.", None),
    ("7.4", "VISITOR", "All clear.", None, None),
    ("7.5", "DON", "The company?", None, "small"),
    ("7.6", "VISITOR", "The coffee machine.", None, None),
    ("8.2", "DON", "Mom! I'm the CEO!", "Mom! I'm the C.E.O.!", "fast"),
    ("8.3", "MOM", "Then stand like one, Donnie.", None, None),
    ("9.3", "ROBOT", "Visitor detected. Human approval required.", None, None),
    ("9.4", "FATHER", "Approved.", None, None),
    ("9.5", "ROBOT", "Welcome, majority shareholder.", None, None),
    ("10.1", "FATHER", "I prefer green in cash.", "I prefer green, in cash.", None),
    ("10.2", "FATHER", "You said it finds anything.", None, None),
    ("10.4a", "FATHER", "Good. Find my money.", "Good. Find, my money.", None),
    ("11.6", "FATHER", "Answer it.", None, None),
]


def film_take(who, txt, how):
    import sound_xmas as sx
    if who == "FATHER":
        return father_line(txt)
    if who == "VISITOR":
        return visitor_line(txt)
    if who == "PAM":                                       # Pam's voice A of the Christmas audition, until hers is picked
        return bc.norm(sx.pam_line(txt, "A"))
    if who == "DON":
        sp = {"bright": 1.06, "fast": 1.12, "small": 0.96, "warm": 0.96}.get(how, 1.0)
        return bc.don(txt, sp)
    return sfs.take("", who, txt, how)


def film_takes(only=None):
    import sherpa_onnx as so_
    os.makedirs(FILM_OUT, exist_ok=True)
    d = os.environ.get("ASR_DIR", "/home/claude/models/asr/sherpa-onnx-whisper-base.en") + "/"
    r = so_.OfflineRecognizer.from_whisper(encoder=d + "base.en-encoder.int8.onnx", decoder=d + "base.en-decoder.int8.onnx",
                                          tokens=d + "base.en-tokens.txt")
    p = FILM_OUT + "/takes.json"
    meta = json.load(open(p)) if os.path.exists(p) else {}
    prev = None
    for key, who, line, give, how in FILM:
        if only and key not in only:
            prev = key; continue
        a = ob.trim(np.asarray(film_take(who, give or line, how), dtype=np.float64))
        sf.write("%s/%s.wav" % (FILM_OUT, key), a.astype(np.float32), SR)
        a16 = np.interp(np.linspace(0, len(a) - 1, int(len(a) * 16000 / SR)), np.arange(len(a)), a)
        pad = np.zeros(4800)
        heard = []
        for w in (a16, np.concatenate([pad, a16]), np.concatenate([a16, pad])):
            s = r.create_stream(); s.accept_waveform(16000, w.astype(np.float32)); r.decode_stream(s)
            heard.append(s.result.text.strip())
        good = sum(1 for h in heard if sfs._match(h, " ".join(sfs._words(line))))
        meta[key] = dict(who=who, text=line, len=round(len(a) / float(SR), 2), asr=heard, ok=good)
        print("%-5s %-7s %4.2f s  %d/3  %-52s | %s" % (key, who, len(a) / float(SR), good, line, heard[0]), flush=True)
        prev = key
    json.dump(meta, open(p, "w"), indent=1)
    by = {}
    for m in meta.values():
        by[m["who"]] = by.get(m["who"], 0) + m["len"]
    print("spoken: %.1f s  " % sum(by.values()), {k: round(v, 1) for k, v in by.items()})
    print("heard at least 2 of 3: %d of %d" % (sum(1 for m in meta.values() if m["ok"] >= 2), len(meta)))


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "film":
    film_takes(sys.argv[2:] or None)


def pam_audition(out="../daddys-home/dh_pam_voices_v1.mp4"):
    """Pam's two lines in the three British voices of the Christmas audition, each after Don's line it answers."""
    import cairo
    import sound_xmas as sx
    gap = lambda t: np.zeros(int(t * SR))
    d1 = ob.trim(np.asarray(bc.don("The money was invested."), dtype=np.float64))
    d2 = ob.trim(np.asarray(bc.don("Approved."), dtype=np.float64))
    parts = []
    for letter, (v, sp, note) in sx.PAMS.items():
        t1 = ob.trim(np.asarray(bc.norm(sx.pam_line("Into what?", letter)), dtype=np.float64))
        t2 = ob.trim(np.asarray(bc.norm(sx.pam_line("It's still one.", letter)), dtype=np.float64))
        a = np.concatenate([gap(0.5), t1, gap(0.5), t2, gap(0.9), d1, gap(0.3), t1, gap(0.9), d2, gap(0.45), t2, gap(0.9)])
        FPS = 10
        nfr = int(np.ceil(len(a) / float(SR) * FPS)); a = np.concatenate([a, np.zeros(nfr * SR // FPS - len(a))])
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 540); c = cairo.Context(surf)
        c.set_source_rgb(0.40, 0.27, 0.58); c.paint()
        for txt, size, y, bold in (("PAM " + letter, 56, 150, 1), (v, 22, 200, 0), (note, 20, 250, 0),
                                   ("\"Into what?\"  \"It's still one.\"", 19, 330, 0), ("alone, then after Don", 16, 370, 0)):
            c.set_source_rgb(1, 1, 1); c.select_font_face("Inter", 0, bold); c.set_font_size(size)
            e = c.text_extents(txt); c.move_to(270 - e.x_advance / 2, y); c.show_text(txt)
        png = "/tmp/dh_pam_%s.png" % letter; wav = png[:-3] + "wav"; tmp = png[:-4] + ".tmp.mp4"; mp4 = png[:-3] + "mp4"
        surf.write_to_png(png); sf.write(wav, a, SR); dur = len(a) / float(SR)
        subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", png, "-i", wav, "-vf",
                               "format=yuv420p,loop=-1:1,trim=duration=%.3f" % dur, "-af", "loudnorm=I=-16:TP=-2,aresample=48000",
                               "-c:v", "libx264", "-crf", "20", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-r", str(FPS),
                               "-c:a", "aac", "-b:a", "160k", "-t", "%.3f" % dur, tmp])
        os.rename(tmp, mp4); parts.append(mp4)
    open("/tmp/dh_pam.txt", "w").write("".join("file '%s'\n" % q for q in parts))
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", "/tmp/dh_pam.txt", "-c", "copy", out + ".tmp.mp4"])
    os.rename(out + ".tmp.mp4", out); print("wrote", out)


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "pam":
    pam_audition()
