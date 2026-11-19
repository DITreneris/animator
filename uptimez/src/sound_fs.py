"""Voices for "First Search" (episode 10), the nine lines of script v5. Every voice is the series' own: Don am_onyx,
Sofía af_bella, the robot voice B (sound_bc.robot), Mom voice F (sound_bc.mom), the Client voice B of episode 9
(sound_ob.client_line: am_fenrir four semitones down). Takes are trimmed to the voiced span (20 ms of air), measured,
and checked by Whisper (three windows: the take alone, with 0.3 s of room before it, with 0.3 s after).
  python3 sound_fs.py takes [shot ...]   -> fs_voices/film/<shot>.wav and takes.json
  python3 sound_fs.py check              -> Whisper on every take
Needs the Kokoro model (KOKORO_DIR) and, for check, the sherpa-onnx Whisper model (ASR_DIR)."""
import os
import sys
import json
import numpy as np
import soundfile as sf
import sound_bc as bc
import sound_ob as ob

SR = 48000
FILM = [  # shot, who, the line, what the voice is given (None = the line), how
    ("1.2", "CLIENT", "Friday, the bank. I need my blueprint.", None, None),
    ("2.2", "DON", "Garage eleven. Guaranteed by Friday.", None, "warm"),
    ("3.3", "SOFIA", "It's the red. It looks bad.", None, "low"),
    ("4.1", "DON", "Can you make the zero green?", "Can you make the zero... green?", None),   # else "grain"
    ("4.2", "ROBOT", "Interface change. Human approval required.", None, None),
    ("4.3", "DON", "Approved.", None, None),
    ("5.2", "CLIENT", "Where's my blueprint?", None, "slow"),
    ("5.3", "DON", "We fixed the red.", "wi fˈɪkst ðə ɹɛd.", "phonemes"),   # stressed, Whisper hears "ride"
    ("6.1", "MOM", "Young man.", None, None),
]
OUT = "fs_voices/film"
# script v6 (18 Nov): the shots renumbered for the new order; two new lines (3.3 Sofía, 5.3 Don). The other seven are
# v1's takes, copied unchanged. python3 sound_fs.py takes_v6 / check_v6
FILM_V6 = [  # new shot, v1 take to reuse (or None), who, the line, given, how
    ("1.2", "1.2", "CLIENT", "Friday, the bank. I need my blueprint.", None, None),
    ("2.2", "2.2", "DON", "Garage eleven. Guaranteed by Friday.", None, "warm"),
    ("3.3", None, "SOFIA", "It found nothing.", None, "low"),
    ("4.1", "4.1", "DON", "Can you make the zero green?", "Can you make the zero... green?", None),
    ("4.2", "4.2", "ROBOT", "Interface change. Human approval required.", None, None),
    ("4.3", "4.3", "DON", "Approved.", None, None),
    ("5.2", "5.2", "CLIENT", "Where's my blueprint?", None, "slow"),
    ("5.3", None, "DON", "The zero's green.", None, "proud"),
    ("7.1", "6.1", "MOM", "Young man.", None, None),
]
OUT_V6 = "fs_voices/film_v6"


def take(shot, who, txt, how):
    if who == "CLIENT":
        a = ob.client_line(txt)
        if how == "slow":                                   # read a little slower: he means it
            a = np.interp(np.linspace(0, len(a) - 1, int(len(a) * 1.10)), np.arange(len(a)), a)
        return a
    if who == "SOFIA":
        return bc.sofia(txt, 0.95 if how == "low" else 1.0, g=0.10 if how == "low" else 0.11)
    if who == "ROBOT":
        return bc.robot(txt)
    if who == "MOM":                                        # the aged voice's tail hiss read as "man's": cut it
        a = np.asarray(bc.mom(txt, 0.92), dtype=np.float64)
        i = np.where(np.abs(a) > 0.18 * np.abs(a).max())[0]
        b = a[max(0, i[0] - 960):i[-1] + 960].copy(); f = 960; b[-f:] *= np.linspace(1, 0, f)
        return b
    if how == "phonemes":                                   # Don's own voice, the line given as phonemes
        import sound_iwry as si
        a, sr = si.K.create(txt, voice=si.DON, speed=0.86, lang="en-us", is_phonemes=True)
        a = np.asarray(a, dtype=np.float64)
        a = np.interp(np.linspace(0, len(a) - 1, int(len(a) * SR / sr)), np.arange(len(a)), a)
        return bc.norm(a)
    return bc.don(txt, 0.96 if how in ("warm", "proud") else 1.0)


def takes(only=None):
    os.makedirs(OUT, exist_ok=True)
    p = OUT + "/takes.json"
    meta = json.load(open(p)) if os.path.exists(p) else {}
    for shot, who, line, give, how in FILM:
        if only and shot not in only:
            continue
        a = ob.trim(np.asarray(take(shot, who, give or line, how), dtype=np.float64))
        sf.write("%s/%s.wav" % (OUT, shot), a.astype(np.float32), SR)
        meta[shot] = dict(who=who, text=line, len=round(len(a) / float(SR), 3), f0=round(float(bc.f0(a))),
                          rms=round(float(np.sqrt(np.mean(a ** 2))), 3), peak=round(float(np.abs(a).max()), 3))
        m = meta[shot]
        print("%-4s %-6s %5.2f s  f0 %3d Hz  rms %.3f  peak %.2f  %s" % (shot, who, m["len"], m["f0"], m["rms"], m["peak"], line),
              flush=True)
    json.dump(meta, open(p, "w"), indent=1)
    print("spoken in all: %.2f s" % sum(m["len"] for m in meta.values()))
    return meta


def _words(s):
    import re
    return re.sub(r"[^a-z0-9' ]", " ", s.lower()).split()


NUM = {"11": "eleven", "0": "zero"}
KEY = {"4.1": "green", "5.3": "red", "2.2": "eleven", "1.2": "blueprint", "5.2": "blueprint"}   # the word the joke needs


def _match(heard, want, key=None, th=0.88):
    """Letters, not words (the series QA standard): similarity of the letter strings at least th, digits read as words,
    and the line's key word heard exactly."""
    import difflib
    h = " ".join(NUM.get(w, w) for w in _words(heard))
    if key and key not in h.split():
        return False
    a, b = h.replace(" ", "").replace("'", ""), want.replace(" ", "").replace("'", "")
    return difflib.SequenceMatcher(None, a, b).ratio() >= th


def check():
    import sherpa_onnx as so_
    d = os.environ.get("ASR_DIR", "/home/claude/models/asr/sherpa-onnx-whisper-base.en") + "/"
    r = so_.OfflineRecognizer.from_whisper(encoder=d + "base.en-encoder.int8.onnx", decoder=d + "base.en-decoder.int8.onnx",
                                          tokens=d + "base.en-tokens.txt")
    meta = json.load(open(OUT + "/takes.json"))
    bad = 0
    for shot, who, line, give, how in FILM:
        a, sr = sf.read("%s/%s.wav" % (OUT, shot))
        a16 = np.interp(np.linspace(0, len(a) - 1, int(len(a) * 16000 / sr)), np.arange(len(a)), a)
        pad = np.zeros(int(0.3 * 16000))
        heard = []
        for w in (a16, np.concatenate([pad, a16]), np.concatenate([a16, pad])):
            s = r.create_stream(); s.accept_waveform(16000, w.astype(np.float32)); r.decode_stream(s)
            heard.append(s.result.text.strip())
        want = " ".join(_words(line))
        ok = sum(1 for h in heard if _match(h, want, KEY.get(shot)))
        meta[shot]["asr"] = heard
        meta[shot]["asr_ok"] = ok
        bad += ok < 2
        print("%-4s %d/3  %-45s | %s" % (shot, ok, line, " | ".join(heard)), flush=True)
    json.dump(meta, open(OUT + "/takes.json", "w"), indent=1)
    print("FAIL" if bad else "PASS", "(%d lines under 2 of 3)" % bad)
    return bad


# board v7 (19 Nov): Mom's line. 7.4, the women: "Eww." (Pam's voice of Secret Santa, voice A; Sofía af_bella),
# Sofía a beat after Pam, mixed into one take. The rest: film_v6, copied unchanged. python3 sound_fs.py takes_v7
OUT_V7 = "fs_voices/film_v7"


def takes_v7():
    import shutil
    import sound_xmas as sx_
    os.makedirs(OUT_V7, exist_ok=True)
    meta = json.load(open(OUT_V6 + "/takes.json"))
    for shot in meta:
        shutil.copy("%s/%s.wav" % (OUT_V6, shot), "%s/%s.wav" % (OUT_V7, shot))
    p_ = ob.trim(np.asarray(sx_.pam_line("Eww.", "A"), dtype=np.float64))
    s_ = ob.trim(np.asarray(bc.sofia("Ew!", 1.0), dtype=np.float64))
    off = int(0.14 * SR)
    a = np.zeros(max(len(p_), off + len(s_)))
    a[:len(p_)] += p_ * 0.9; a[off:off + len(s_)] += s_ * 0.8
    a = a / np.abs(a).max() * 0.9 * float(np.abs(p_).max())
    sf.write(OUT_V7 + "/7.4.wav", a.astype(np.float32), SR)
    meta["7.4"] = dict(who="PAM+SOFIA", text="Eww.", len=round(len(a) / float(SR), 3), f0=round(float(bc.f0(a))),
                       rms=round(float(np.sqrt(np.mean(a ** 2))), 3), peak=round(float(np.abs(a).max()), 3))
    json.dump(meta, open(OUT_V7 + "/takes.json", "w"), indent=1)
    print("7.4 PAM+SOFIA %.2f s  Eww.  spoken in all %.2f s" % (meta["7.4"]["len"], sum(m["len"] for m in meta.values())))


# board v8 (19 Nov): Mom's three remarks. 6.1b "Machines." (muttered), 7.5 "That hussy." (muttered; "Hussy." alone was heard "Hossy"), 8.1 "Pam has a plan."
# The rest: film_v7, copied. python3 sound_fs.py takes_v8 / check_v8
OUT_V8 = "fs_voices/film_v8"
MOM_V8 = [("6.1b", "Machines.", 0.8), ("7.5", "That hussy.", 0.8), ("8.1", "Pam has a plan.", 1.0)]   # shot, line, gain


def takes_v8():
    import shutil
    os.makedirs(OUT_V8, exist_ok=True)
    meta = json.load(open(OUT_V7 + "/takes.json"))
    for shot in meta:
        shutil.copy("%s/%s.wav" % (OUT_V7, shot), "%s/%s.wav" % (OUT_V8, shot))
    for shot, line, g in MOM_V8:
        a = ob.trim(np.asarray(take(shot, "MOM", line, None), dtype=np.float64)) * g
        sf.write("%s/%s.wav" % (OUT_V8, shot), a.astype(np.float32), SR)
        meta[shot] = dict(who="MOM", text=line, len=round(len(a) / float(SR), 3), f0=round(float(bc.f0(a))),
                          rms=round(float(np.sqrt(np.mean(a ** 2))), 3), peak=round(float(np.abs(a).max()), 3))
        print("%-5s MOM %5.2f s  %s" % (shot, meta[shot]["len"], line))
    json.dump(meta, open(OUT_V8 + "/takes.json", "w"), indent=1)
    print("spoken in all %.2f s" % sum(m["len"] for m in meta.values()))


def takes_v6():
    import shutil
    os.makedirs(OUT_V6, exist_ok=True)
    old = json.load(open(OUT + "/takes.json"))
    meta = {}
    for shot, reuse, who, line, give, how in FILM_V6:
        if reuse:
            shutil.copy("%s/%s.wav" % (OUT, reuse), "%s/%s.wav" % (OUT_V6, shot))
            meta[shot] = dict(old[reuse]); meta[shot].pop("asr", None); meta[shot].pop("asr_ok", None)
        else:
            a = ob.trim(np.asarray(take(shot, who, give or line, how), dtype=np.float64))
            sf.write("%s/%s.wav" % (OUT_V6, shot), a.astype(np.float32), SR)
            meta[shot] = dict(who=who, text=line, len=round(len(a) / float(SR), 3), f0=round(float(bc.f0(a))),
                              rms=round(float(np.sqrt(np.mean(a ** 2))), 3), peak=round(float(np.abs(a).max()), 3))
        m = meta[shot]
        print("%-4s %-6s %5.2f s  %s%s" % (shot, who, m["len"], line, "  (v1 take %s)" % reuse if reuse else "  NEW"), flush=True)
    json.dump(meta, open(OUT_V6 + "/takes.json", "w"), indent=1)
    print("spoken in all: %.2f s" % sum(m["len"] for m in meta.values()))


if __name__ == "__main__":
    if sys.argv[1] == "takes_v8":
        takes_v8(); sys.exit(0)
    if sys.argv[1] == "check_v8":
        OUT, FILM = OUT_V8, [(sh, "MOM", ln, None, None) for sh, ln, g in MOM_V8]
        KEY.update({"8.1": "plan"})
        check(); sys.exit(0)
    if sys.argv[1] == "takes_v7":
        takes_v7(); sys.exit(0)
    if sys.argv[1] == "takes_v6":
        takes_v6(); sys.exit(0)
    if sys.argv[1] == "check_v6":
        global_ = globals()
        OUT, FILM = OUT_V6, [(a, c, d, e, f) for a, b, c, d, e, f in FILM_V6]
        KEY.update({"5.3": "green", "3.3": "nothing"}); KEY.pop("2.2", None); KEY["2.2"] = "eleven"
        sys.exit(1 if check() else 0)
    if sys.argv[1] == "takes":
        takes(sys.argv[2:] or None)
    elif sys.argv[1] == "check":
        sys.exit(1 if check() else 0)
