"""Voices for "Customer Success" (episode 11), the fourteen lines of script v7. Every voice is the series' own and the
one episode 10 used (sound_fs.take): Don am_onyx, Sofía af_bella, the robot voice B, the Client am_fenrir four
semitones down. Don's three "Approved." are episode 10's own take (fs_voices/film_v9/4.3.wav), copied unchanged, so
the runner is the same voice and the same read. Takes are trimmed to the voiced span, measured, and checked by Whisper
(three windows: the take alone, with 0.3 s of room before it, with 0.3 s after; scored by letters, with the line's key
word heard exactly).
  python3 sound_cs.py takes [key ...]   -> cs_voices/film_v1/<key>.wav and takes.json
  python3 sound_cs.py check             -> Whisper on every take
Needs the Kokoro model (KOKORO_DIR) and, for check, the sherpa-onnx Whisper model (ASR_DIR)."""
import os
import sys
import json
import shutil
import numpy as np
import soundfile as sf
import sound_bc as bc
import sound_ob as ob
import sound_fs as sfs

SR = 48000
OUT = "cs_voices/film_v1"
APPROVED = "fs_voices/film_v9/4.3.wav"                    # ep 10's "Approved."
FILM = [  # key (shot + who), who, the line, what the voice is given (None = the line), how
    ("1.2r", "ROBOT", "Repair. Human approval required.", "Repair, human approval required.", None),   # else "Repairs"
    ("1.2d", "DON", "Approved.", None, "ep10"),
    ("1.3", "CLIENT", "Friday. The bank. Nine o'clock.", "Friday, the bank. Nine o'clock.", None),   # ep 10's read of "Friday, the bank."
    ("2.1", "DON", "Your Customer Success Report.", None, "warm"),
    ("2.4", "CLIENT", "I need my plan. Not a report.", None, "slow"),
    ("4.4", "ROBOT", "The result was obtained by a h-human.", "The result was obtained by a h... human.", None),
    ("5.2", "ROBOT", "Report change. Human approval required.", None, None),
    ("5.3", "DON", "Approved.", None, "ep10"),
    ("5.4", "SOFIA", "He's not looking at you.", None, "low"),
    ("6.1", "CLIENT", "Your number.", None, None),
    ("6.5", "DON", "Customer success.", "Customer. Success.", None),   # else "Customers exist"
    ("6.9r", "ROBOT", "Reply drafted. Human approval required.", None, None),
    ("6.9d", "DON", "Approved.", None, "ep10"),
    ("6.11", "SOFIA", "Nobody noticed.", None, "low"),
]
# script v8 (20 Nov): the post is the crisis. Five new lines; the other eight are film_v1's takes, copied unchanged.
#   python3 sound_cs.py takes_v2 / check_v2  ->  cs_voices/film_v2
OUT_V2 = "cs_voices/film_v2"
FILM_V2 = [  # key, film_v1 take to reuse (or None), who, the line, given, how
    ("1.4r", "6.9r", "ROBOT", "Reply drafted. Human approval required.", None, None),
    ("1.4d", "6.9d", "DON", "Approved.", None, "ep10"),
    ("2.1", None, "DON", "Let's fix this together.", None, "warm"),
    ("2.2", None, "CLIENT", "Nine o'clock. Your office.", None, "phone"),
    ("3.1r", None, "ROBOT", "Blueprint generated. Human approval required.", "Blue print generated, human approval required.", None),   # else "Luprent"
    ("3.1d", "5.3", "DON", "Approved.", None, "ep10"),
    ("3.3", None, "DON", "Recovered.", None, "proud"),
    ("3.5", None, "CLIENT", "I have ten garages.", None, None),   # read slower, the end is lost
    ("4.4", "4.4", "ROBOT", "The result was obtained by a h-human.", None, None),
    ("5.1", "6.1", "CLIENT", "Your number.", None, None),
    ("5.4s", "5.4", "SOFIA", "He's not looking at you.", None, "low"),
    ("5.4d", "6.5", "DON", "Customer success.", None, None),
    ("6.5", "6.11", "SOFIA", "Nobody noticed.", None, "low"),
]


# script v10 (20 Nov): the AI's site plan insults him; Sofía's last line. Two new lines; the rest is film_v2, unchanged.
#   python3 sound_cs.py takes_v3 / check_v3  ->  cs_voices/film_v3
OUT_V3 = "cs_voices/film_v3"
FILM_V3 = [(k, k, w, l, None, None) for k, w, l in (
    ("1.4r", "ROBOT", "Reply drafted. Human approval required."), ("1.4d", "DON", "Approved."),
    ("2.1", "DON", "Let's fix this together."), ("2.2", "CLIENT", "Nine o'clock. Your office."),
    ("3.1r", "ROBOT", "Blueprint generated. Human approval required."), ("3.1d", "DON", "Approved."),
    ("3.3", "DON", "Recovered."), ("4.4", "ROBOT", "The result was obtained by a h-human."), ("5.1", "CLIENT", "Your number."),
    ("5.4s", "SOFIA", "He's not looking at you."), ("5.4d", "DON", "Customer success."))] + [
    ("3.5", None, "CLIENT", "Is this a joke?", None, None),
    ("6.5", None, "SOFIA", "Still one star.", None, "low"),
]


def takes_v3():
    global OUT_V2, FILM_V2, OUT
    o2, f2, o = OUT_V2, FILM_V2, OUT
    OUT, OUT_V2, FILM_V2 = o2, OUT_V3, FILM_V3                         # copy from film_v2 into film_v3
    try:
        takes_v2()
    finally:
        OUT_V2, FILM_V2, OUT = o2, f2, o


def check_v3():
    global OUT_V2, FILM_V2
    o2, f2, k35 = OUT_V2, FILM_V2, KEY["3.5"]
    KEY["3.5"] = "joke"                                                   # 3.5 is a new line in v3
    OUT_V2, FILM_V2 = OUT_V3, FILM_V3
    try:
        return check_v2()
    finally:
        OUT_V2, FILM_V2, KEY["3.5"] = o2, f2, k35


OUT_V4 = "cs_voices/film_v4"
FILM_V4_NEW = [                                            # One Star v15/v16 (Tomas): the post in the Client's voice, the reply
    ("1.2", "CLIENT", "Paid $999. They lost my blueprint. My lawyer will call.",       # in the robot's
     "Paid nine hundred ninety-nine. They lost my blueprint. My lawyer will call."),   # ("nine ninety-nine" was heard "9.99")
    ("1.4b", "ROBOT", "Shut off! Our AI does not lose files!", None),                 # 4 reads tried: this one 1/1 word-perfect
]


def takes_v4():
    """film_v3 copied unchanged, and the two new lines."""
    os.makedirs(OUT_V4, exist_ok=True)
    meta = json.load(open(OUT_V3 + "/takes.json"))
    for k in meta:
        shutil.copyfile("%s/%s.wav" % (OUT_V3, k), "%s/%s.wav" % (OUT_V4, k))
    for key, who, line, give in FILM_V4_NEW:
        a = ob.trim(np.asarray(sfs.take(key, who, give or line, None), dtype=np.float64))
        sf.write("%s/%s.wav" % (OUT_V4, key), a.astype(np.float32), SR)
        meta[key] = dict(who=who, text=line, len=round(len(a) / float(SR), 3), f0=round(float(bc.f0(a))),
                         rms=round(float(np.sqrt(np.mean(a ** 2))), 3), peak=round(float(np.abs(a).max()), 3), source="kokoro")
        print("%-5s %-6s %5.2f s  %s" % (key, who, meta[key]["len"], line), flush=True)
    json.dump(meta, open(OUT_V4 + "/takes.json", "w"), indent=1)


def phone_line(a):
    """A voice through a phone: 300-3400 Hz, a little crushed."""
    from scipy.signal import butter, sosfilt
    sos = butter(4, [300, 3400], btype="bandpass", fs=SR, output="sos")
    b = sosfilt(sos, a)
    b = np.tanh(b * 2.2) / np.tanh(2.2)
    return b / max(1e-9, np.abs(b).max()) * 0.8


def takes_v2():
    os.makedirs(OUT_V2, exist_ok=True)
    meta, old = {}, json.load(open(OUT + "/takes.json"))
    for key, src, who, line, give, how in FILM_V2:
        if src:
            shutil.copyfile("%s/%s.wav" % (OUT, src), "%s/%s.wav" % (OUT_V2, key))
            meta[key] = dict(old[src]); meta[key]["source"] = "film_v1 " + src
            continue
        a = np.asarray(sfs.take(key, who, give or line, None if how == "phone" else how), dtype=np.float64)
        if how == "phone":
            a = phone_line(a)
        a = ob.trim(a)
        sf.write("%s/%s.wav" % (OUT_V2, key), a.astype(np.float32), SR)
        meta[key] = dict(who=who, text=line, len=round(len(a) / float(SR), 3), f0=round(float(bc.f0(a))),
                         rms=round(float(np.sqrt(np.mean(a ** 2))), 3), peak=round(float(np.abs(a).max()), 3), source="kokoro")
        print("%-5s %-6s %5.2f s  %s" % (key, who, meta[key]["len"], line), flush=True)
    json.dump(meta, open(OUT_V2 + "/takes.json", "w"), indent=1)
    print("spoken in all: %.2f s" % sum(m["len"] for m in meta.values()))


def check_v2():
    global OUT, FILM
    sfs.NUM.setdefault("9", "nine"); sfs.NUM.setdefault("10", "ten")      # Whisper writes the numbers as digits
    o, f = OUT, FILM
    OUT, FILM = OUT_V2, [(k, w, l, g, h) for k, _, w, l, g, h in FILM_V2]
    try:
        return check()
    finally:
        OUT, FILM = o, f


KEY = {"6.5": "star", "3.1r": "blueprint", "3.5": "garages", "2.2": "office", "1.4r": "reply", "1.2r": "repair", "4.4": "human", "5.2": "report", "6.9r": "reply", "6.11": "nobody", "2.4": "plan", "1.3": "bank"}


def takes(only=None):
    os.makedirs(OUT, exist_ok=True)
    p = OUT + "/takes.json"
    meta = json.load(open(p)) if os.path.exists(p) else {}
    for key, who, line, give, how in FILM:
        if only and key not in only:
            continue
        if how == "ep10":
            shutil.copyfile(APPROVED, "%s/%s.wav" % (OUT, key))
            a, _ = sf.read(APPROVED)
        else:
            a = ob.trim(np.asarray(sfs.take(key, who, give or line, how), dtype=np.float64))
            sf.write("%s/%s.wav" % (OUT, key), a.astype(np.float32), SR)
        meta[key] = dict(who=who, text=line, len=round(len(a) / float(SR), 3), f0=round(float(bc.f0(a))),
                         rms=round(float(np.sqrt(np.mean(a ** 2))), 3), peak=round(float(np.abs(a).max()), 3),
                         source="ep 10 film_v9 4.3" if how == "ep10" else "kokoro")
        m = meta[key]
        print("%-5s %-6s %5.2f s  f0 %3d Hz  rms %.3f  peak %.2f  %s" % (key, who, m["len"], m["f0"], m["rms"], m["peak"], line),
              flush=True)
    json.dump(meta, open(p, "w"), indent=1)
    print("spoken in all: %.2f s" % sum(m["len"] for m in meta.values()))
    return meta


def check():
    import sherpa_onnx as so_
    d = os.environ.get("ASR_DIR", "/home/claude/models/asr/sherpa-onnx-whisper-base.en") + "/"
    r = so_.OfflineRecognizer.from_whisper(encoder=d + "base.en-encoder.int8.onnx", decoder=d + "base.en-decoder.int8.onnx",
                                          tokens=d + "base.en-tokens.txt")
    meta = json.load(open(OUT + "/takes.json"))
    bad = 0
    for key, who, line, give, how in FILM:
        a, sr = sf.read("%s/%s.wav" % (OUT, key))
        a16 = np.interp(np.linspace(0, len(a) - 1, int(len(a) * 16000 / sr)), np.arange(len(a)), a)
        pad = np.zeros(int(0.3 * 16000))
        heard = []
        for w in (a16, np.concatenate([pad, a16]), np.concatenate([a16, pad])):
            s = r.create_stream(); s.accept_waveform(16000, w.astype(np.float32)); r.decode_stream(s)
            heard.append(s.result.text.strip())
        want = " ".join(sfs._words(line.replace("h-human", "human")))
        ok = sum(1 for h in heard if sfs._match(h, want, KEY.get(key)))
        meta[key]["asr"] = heard
        meta[key]["asr_ok"] = ok
        bad += ok < 2
        print("%-5s %d/3  %-42s | %s" % (key, ok, line, " | ".join(heard)), flush=True)
    json.dump(meta, open(OUT + "/takes.json", "w"), indent=1)
    print("FAIL" if bad else "PASS", "(%d lines under 2 of 3)" % bad)
    return bad


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "takes"
    if cmd == "takes":
        takes(sys.argv[2:] or None)
    elif cmd == "check":
        sys.exit(1 if check() else 0)
    elif cmd == "takes_v2":
        takes_v2()
    elif cmd == "check_v2":
        sys.exit(1 if check_v2() else 0)
    elif cmd == "takes_v3":
        takes_v3()
    elif cmd == "check_v3":
        sys.exit(1 if check_v3() else 0)
    elif cmd == "takes_v4":
        takes_v4()
