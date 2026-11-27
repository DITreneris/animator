"""Voices for The Blueprint (16:9). Writes only bp_voices/. The ob_, fs_ and cs_voices folders are shipped records
and are read, never written.

Inherited lines (the-blueprint-line-ledger-v1.md): all 37 are copied byte for byte from the shipped takes in git,
ob_voices/film_v10, fs_voices/film_v13 and cs_voices/film_v10. The Onboarding's "Oh..." is film_v10's cleaned take.
They are not regenerated: 26 Nov 2026, this machine's Kokoro does not reproduce them ("Approved." 0.783 s against the
shipped 0.718 in kokoro-onnx 0.4.4 and 0.4.7, so below the package, in the phonemizer). Rebuilt, First Search's 4.1
was heard as "make the zero grain" and 1.2 sent Whisper into a loop, where the shipped takes pass 3 of 3.
Gates (`gate`): a copied take is byte-identical to its source; every take is heard by Whisper in at least 2 of 3
windows with its key word; a second build is byte-identical to bp_voices/ (`rebuild`), so these takes are stable from
here on.
New lines: the six night lines, Sofía af_bella and Pam voice A (sound_xmas.PAMS["A"], bf_emma), the voice of the
scoop (ob 9.1) and of "Check your pocket." Local only: the Kokoro licence is open, so they are not for a public master.

  python3 bp_voices.py build      -> bp_voices/<key>.wav and bp_voices/takes.json
  python3 bp_voices.py gate       -> copies and Whisper on every take, drift reported; exit 1 on a fail
  python3 bp_voices.py pick       -> Whisper on each CANDIDATES delivery; the first 3 of 3 goes into GIVE by hand
  python3 bp_voices.py rebuild    -> builds again into /tmp and compares md5 with bp_voices/; exit 1 on a difference
  python3 bp_voices.py plant      -> each gate on a known wrong take; exit 1 unless every plant fails
  python3 bp_voices.py audition   -> ../the-blueprint/voices/bp_night_takes_v1.wav (the six night lines, 0.6 s apart)
  python3 bp_voices.py table      -> the 43 lines as a markdown table
Needs KOKORO_DIR and ASR_DIR."""
import difflib
import json
import os
import re
import shutil
import sys

import numpy as np
import soundfile as sf

SR = 48000
SRC = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(SRC, "bp_voices")


# key, who, text, source folder, source key, key word for Whisper
INHERIT = [
    ("ob_3.1", "CLIENT", "Ten garages. And I keep losing this.", "ob_voices/film_v10", "3.1", "garages"),
    ("ob_3.2", "SOFIA", "Does your missus love your garages?", "ob_voices/film_v10", "3.2", "garages"),
    ("ob_3.3", "CLIENT", "I live alone.", "ob_voices/film_v10", "3.3", "alone"),
    ("ob_3.7", "SOFIA", "Oh...", "ob_voices/film_v10", "3.7", None),
    ("ob_3.12", "CLIENT", "Can it find this when I lose it?", "ob_voices/film_v10", "3.12", "find"),
    ("ob_4.1", "DON", "Here, you will never lose anything again.", "ob_voices/film_v10", "4.1", "never"),
    ("ob_4.3", "DON", "We'll take care of it.", "ob_voices/film_v10", "4.3", "care"),
    ("ob_5.4", "CLIENT", "One month. I ask, you find it.", "ob_voices/film_v10", "5.4", "month"),
    ("ob_5.5", "DON", "Approved.", "ob_voices/film_v10", "5.5", "approved"),
    ("ob_8.1", "ROBOT", "FIRST CUSTOMER. CELEBRATION REQUIRED.", "ob_voices/film_v10", "8.1", "celebration"),
    ("ob_8.3", "DON", "SOFÍA! WE HAVE A CUSTOMER!", "ob_voices/film_v10", "8.3", "customer"),
    ("ob_9.1", "PAM", "Some shit, others scoop.", "ob_voices/film_v10", "9.1", "scoop"),
    ("ob_10.4", "ROBOT", "ONBOARDING COMPLETE.", "ob_voices/film_v10", "10.4", "complete"),
    ("fs_1.2", "CLIENT", "Friday, the bank. I need my blueprint.", "fs_voices/film_v13", "1.2", "blueprint"),
    ("fs_2.2", "DON", "Garage eleven. Guaranteed by Friday.", "fs_voices/film_v13", "2.2", "eleven"),
    ("fs_t1", "CLIENT", "Friday. Or I sue.", "fs_voices/film_v13", "t1", "sue"),
    ("fs_3.3", "SOFIA", "It found nothing.", "fs_voices/film_v13", "3.3", "nothing"),
    ("fs_4.1", "DON", "Can you make the zero green?", "fs_voices/film_v13", "4.1", "green"),
    ("fs_4.2", "ROBOT", "Interface change. Human approval required.", "fs_voices/film_v13", "4.2", "approval"),
    ("fs_4.3", "DON", "Approved.", "fs_voices/film_v13", "4.3", "approved"),
    ("fs_5.2", "CLIENT", "Where's my blueprint?", "fs_voices/film_v13", "5.2", "blueprint"),
    ("fs_x1", "DON", "Where is his blueprint?", "fs_voices/film_v13", "x1", "blueprint"),
    ("fs_x2", "SOFIA", "Ask the machine.", "fs_voices/film_v13", "x2", "machine"),
    ("fs_x3", "ROBOT", "Zero results.", "fs_voices/film_v13", "x3", "results"),
    ("fs_7.1", "MOM", "Young man.", "fs_voices/film_v13", "7.1", "man"),
    ("fs_t2", "CLIENT", "See you in court.", "fs_voices/film_v13", "t2", "court"),
    ("cs_1.2", "CLIENT", "Paid $999. They lost my blueprint. My lawyer will call.", "cs_voices/film_v10", "1.2", "lawyer"),
    ("cs_1.4r", "ROBOT", "Reply drafted. Human approval required.", "cs_voices/film_v10", "1.4r", "approval"),
    ("cs_1.4d", "DON", "Approved.", "cs_voices/film_v10", "1.4d", "approved"),
    ("cs_1.4b", "DON", "Stupid human.", "cs_voices/film_v10", "1.4b", "stupid"),
    ("cs_3.5", "CLIENT", "Is this a joke?", "cs_voices/film_v10", "3.5", "joke"),
    ("cs_4.2p", "PAM", "Check your pocket.", "cs_voices/film_v10", "4.2p", "pocket"),
    ("cs_4.4", "ROBOT", "The result was obtained by a h-human.", "cs_voices/film_v10", "4.4", "obtained"),
    ("cs_5.1", "CLIENT", "Your number.", "cs_voices/film_v10", "5.1", "number"),
    ("cs_5.4d", "DON", "Customer success.", "cs_voices/film_v10", "5.4d", "success"),
    ("cs_6.3p", "PAM", "Some post. Others find.", "cs_voices/film_v10", "6.3p", "post"),
    ("cs_6.5", "SOFIA", "Still one star.", "cs_voices/film_v10", "6.5", "star"),
]
NIGHT = [
    ("n1", "SOFIA", "Put recovered on it.", "recovered"),
    ("n2", "PAM", "Recovered from what?", "what"),
    ("n3", "SOFIA", "He needs a page by Friday.", "page"),
    ("n4", "PAM", "He needs the bays.", "bays"),
    ("n5", "SOFIA", "I won't draw one.", "draw"),
    ("n6", "PAM", "I'm matching them.", "matching"),
]
NUM = {"11": "eleven", "0": "zero", "999": "nine hundred ninety nine", "1": "one"}


def _ref(rel, key):
    with open(os.path.join(SRC, rel, "takes.json"), encoding="utf-8") as f:
        return json.load(f)[key]


def _phonemes(ph, voice, speed, lang):
    import sound_bc as bc
    import sound_iwry as si
    a, sr = si.K.create(ph, voice=voice, speed=speed, lang=lang, is_phonemes=True)
    a = np.asarray(a, dtype=np.float64)
    return bc.norm(np.interp(np.linspace(0, len(a) - 1, int(len(a) * SR / sr)), np.arange(len(a)), a))


def _say(who, txt, speed=None):
    """A line in the series voice: Don and Sofía as sound_bc, Pam voice A. "/.../" is given as phonemes."""
    import sound_bc as bc
    import sound_iwry as si
    import sound_xmas as sx
    if who == "PAM":
        v, sp, _ = sx.PAMS["A"]
        if txt.startswith("/"):
            return _phonemes(txt.strip("/"), v, speed or sp, "en-gb")
        return bc.norm(sx.best_take(txt, v, speed or sp, "en-gb"))
    if txt.startswith("/"):
        return _phonemes(txt.strip("/"), si.DON if who == "DON" else si.SOF, speed or 1.0, "en-us")
    return (bc.don if who == "DON" else bc.sofia)(txt, speed or 1.0)


# Picked by measurement (`pick`), 26 Nov 2026: the first candidate Whisper hears in 3 of 3 windows with the key word.
# Given as written, "He needs the bays." is heard "the baeza" 3 of 3, and "Recovered from what?" "from water": the rise
# Kokoro puts on "?" adds a syllable. Without the "?" Whisper still hears a question.
GIVE = {"n2": "/ɹɪkˈʌvəd fɹɒm wˈɒt/", "n4": "He needs the bays!"}
CANDIDATES = {
    "n4": ("PAM", "bays", ["He needs the bays.", "He needs the bays!", "He needs... the bays.",
                           "/hiː nˈiːdz ðə bˈeɪz./", "/hiː nˈiːdz ðə bˈeɪz!/"]),
    "n2": ("PAM", "what", ["Recovered from what?", "Recovered... from what?", "Recovered from what?!",
                           "Recovered. From what?", "/ɹɪkˈʌvəd fɹɒm wˈɒt?/", "/ɹɪkˈʌvəd fɹəm wˈʌt?/",
                           "/ɹɪkˈʌvəd fɹɒm wˈɒʔ?/", "Recovered from... what?", "Recovered? From what?",
                           "/ɹɪkˈʌvəd fɹɒm wˈɒt/", "/ɹɪkˈʌvəd. fɹɒm wˈɒt?/"]),
}


def pick(only=None):
    import sound_ob as ob
    meta = json.load(open(os.path.join(OUT, "takes.json"), encoding="utf-8"))
    chosen = {}
    for key, (who, word, cands) in CANDIDATES.items():
        if only and key not in only:
            continue
        for txt in cands:
            a = ob.trim(np.asarray(_say(who, txt), dtype=np.float64))
            ok, heard = whisper_score(a, meta[key]["text"], word)
            print("%-7s %d/3  %5.3f s  %-40s | %s" % (key, ok, len(a) / float(SR), txt, " | ".join(heard)), flush=True)
            if ok == 3 and key not in chosen:
                chosen[key] = txt
    print("chosen", chosen)
    return chosen


def _night(who, txt):
    import sound_ob as ob
    return ob.trim(np.asarray(_say(who, txt), dtype=np.float64))


def _stats(a):
    import sound_bc as bc
    return dict(len=round(len(a) / float(SR), 3), f0=round(float(bc.f0(a))),
                rms=round(float(np.sqrt(np.mean(a ** 2))), 3), peak=round(float(np.abs(a).max()), 3))


def build(out=OUT):
    os.makedirs(out, exist_ok=True)
    meta = {}
    for key, who, text, rel, skey, word in INHERIT:
        ref = _ref(rel, skey)
        path = os.path.join(out, key + ".wav")
        shutil.copyfile(os.path.join(SRC, rel, skey + ".wav"), path)
        a = sf.read(path)[0].astype(np.float64)
        how = "copied"
        st = _stats(a)
        meta[key] = dict(who=who, text=text, source="%s %s" % (rel, skey), how=how, word=word,
                         ref_len=ref["len"], ref_f0=ref.get("f0"), drift_ms=round((st["len"] - ref["len"]) * 1000), **st)
        print("%-8s %-6s %-7s %5.3f s (shipped %5.3f, %+4d ms)  f0 %3d (shipped %s)  %s" % (
            key, who, how, st["len"], ref["len"], meta[key]["drift_ms"], st["f0"], ref.get("f0"), text), flush=True)
    for key, who, text, word in NIGHT:
        a = _night(who, GIVE.get(key, text))
        sf.write(os.path.join(out, key + ".wav"), a.astype(np.float32), SR)
        meta[key] = dict(who=who, text=text, source="new, night scene", how="new", word=word,
                         local_only=True, **_stats(a))
        print("%-8s %-6s new     %5.3f s  f0 %3d  %s" % (key, who, meta[key]["len"], meta[key]["f0"], text), flush=True)
    with open(os.path.join(out, "takes.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=1, ensure_ascii=False)
    return meta


def _md5(path):
    import hashlib
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


# ---- the gates
_REC = []


def recognizer():
    if not _REC:
        import sherpa_onnx as so_
        d = os.environ.get("ASR_DIR", os.path.expanduser("~/models/asr/sherpa-onnx-whisper-base.en")) + "/"
        _REC.append(so_.OfflineRecognizer.from_whisper(encoder=d + "base.en-encoder.int8.onnx",
                                                       decoder=d + "base.en-decoder.int8.onnx",
                                                       tokens=d + "base.en-tokens.txt"))
    return _REC[0]


def hear(a, sr=SR):
    a16 = np.interp(np.linspace(0, len(a) - 1, int(len(a) * 16000 / sr)), np.arange(len(a)), a)
    s = recognizer().create_stream()
    s.accept_waveform(16000, a16.astype(np.float32))
    recognizer().decode_stream(s)
    return s.result.text.strip()


def words(s):
    s = re.sub(r"[^a-z0-9' ]", " ", s.lower().replace("$", " "))
    return [NUM.get(w, w) for w in s.split()]


def match(heard, want, key=None, th=0.88):
    """Letters, not words (the series QA standard). The key word must be heard exactly."""
    h = words(heard)
    if key and key not in h:
        return False
    a = "".join(h).replace("'", "")
    b = "".join(words(want)).replace("'", "")
    return difflib.SequenceMatcher(None, a, b).ratio() >= th


def windows(a, sr=SR):
    pad = np.zeros(int(0.3 * sr))
    return [a, np.concatenate([pad, a]), np.concatenate([a, pad])]


def whisper_score(a, text, key):
    heard = [hear(w) for w in windows(a)]
    return sum(1 for h in heard if match(h, text, key)), heard


def gate_take(m, path):
    faults = []
    a = sf.read(path)[0].astype(np.float64)
    if m["how"] == "copied":
        rel, skey = m["source"].split()
        src = os.path.join(SRC, rel, skey + ".wav")
        if _md5(path) != _md5(src):
            faults.append("copy differs from %s" % os.path.relpath(src, SRC))
    if m["text"] != "Oh...":
        ok, heard = whisper_score(a, m["text"], m.get("word"))
        m["asr"], m["asr_ok"] = heard, ok
        if ok < 2:
            faults.append("whisper %d/3: %s" % (ok, " | ".join(heard)))
    return faults


def gate(out=OUT):
    path = os.path.join(out, "takes.json")
    meta = json.load(open(path, encoding="utf-8"))
    bad = 0
    for key, m in meta.items():
        faults = gate_take(m, os.path.join(out, key + ".wav"))
        bad += bool(faults)
        drift = "" if m.get("drift_ms") is None else "%+4d ms" % m["drift_ms"]
        print("%-8s %-7s %-4s %s  %s" % (key, m["how"], "FAIL" if faults else "ok", drift,
                                        "; ".join(faults) or (m.get("asr") or ["(a vowel: no ASR)"])[0]), flush=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=1, ensure_ascii=False)
    print("FAIL" if bad else "PASS", "(%d of %d takes)" % (bad, len(meta)))
    return bad


def rebuild(tmp="/tmp/bp_voices_rebuild"):
    shutil.rmtree(tmp, ignore_errors=True)
    build(tmp)
    diff = [k for k in json.load(open(os.path.join(OUT, "takes.json"), encoding="utf-8"))
            if _md5(os.path.join(tmp, k + ".wav")) != _md5(os.path.join(OUT, k + ".wav"))]
    print("rebuild", "identical" if not diff else "DIFFERS: %s" % diff)
    return diff


def plant(tmp="/tmp/bp_voices_plant"):
    """Each gate must fail on a known wrong take, or it is not a gate."""
    import sound_bc as bc
    import sound_on as so
    meta = json.load(open(os.path.join(OUT, "takes.json"), encoding="utf-8"))
    os.makedirs(tmp, exist_ok=True)
    caught = 0
    # copy: One Star's 6.5 one semitone up, filed as the copy
    p = os.path.join(tmp, "cs_6.5.wav")
    sf.write(p, so.pitch(sf.read(os.path.join(OUT, "cs_6.5.wav"))[0], 1.0).astype(np.float32), SR)
    f = gate_take(dict(meta["cs_6.5"]), p)
    caught += any(x.startswith("copy") for x in f)
    print("%-52s %s  %s" % ("copy: 6.5 a semitone up", "caught" if f else "MISSED", "; ".join(f)), flush=True)
    # whisper: the take of a different line under this line's text
    f = gate_take(dict(meta["fs_x2"]), os.path.join(OUT, "fs_x3.wav"))
    caught += any(x.startswith("whisper") for x in f)
    print("%-52s %s  %s" % ("whisper: Zero results. filed as Ask the machine.", "caught" if f else "MISSED", "; ".join(f)),
          flush=True)
    # rebuild: Sofía's night line at speed 0.80 instead of 1.0 must not hash like the kept take.
    # (0.96 hashed like 1.0 on "Approved.": Kokoro rounds each phoneme's frames, so a small change can leave a word as it was.)
    p = os.path.join(tmp, "n5.wav")
    import sound_ob as ob
    sf.write(p, ob.trim(np.asarray(bc.sofia("I won't draw one.", 0.80), dtype=np.float64)).astype(np.float32), SR)
    hit = _md5(p) != _md5(os.path.join(OUT, "n5.wav"))
    caught += hit
    print("%-52s %s" % ("rebuild: I won't draw one. at speed 0.80", "caught" if hit else "MISSED"), flush=True)
    print("plants caught %d of 3" % caught)
    return caught == 3


def table():
    """The Stop 2 table, from takes.json after `gate`."""
    meta = json.load(open(os.path.join(OUT, "takes.json"), encoding="utf-8"))
    print("| Key | Who | Line | Source | Length | f0 | Whisper |")
    print("|---|---|---|---|---:|---:|---|")
    for key, m in meta.items():
        src = m["source"] if m["how"] == "copied" else "new" + (", given `%s`" % GIVE[key] if key in GIVE else "")
        asr = "%d of 3" % m["asr_ok"] if "asr_ok" in m else "a vowel, not scored"
        print("| %s | %s | %s | %s | %.3f s | %d | %s |" % (key, m["who"], m["text"], src, m["len"], m["f0"], asr))


def audition():
    meta = json.load(open(os.path.join(OUT, "takes.json"), encoding="utf-8"))
    gap = np.zeros(int(0.6 * SR))
    parts = []
    for key, _, _, _ in NIGHT:
        parts += [sf.read(os.path.join(OUT, key + ".wav"))[0].astype(np.float64), gap]
    out = os.path.join(SRC, "..", "the-blueprint", "voices")
    os.makedirs(out, exist_ok=True)
    path = os.path.normpath(os.path.join(out, "bp_night_takes_v1.wav"))
    sf.write(path, np.concatenate(parts).astype(np.float32), SR)
    print(path, "  ".join("%s %.2f s" % (k, meta[k]["len"]) for k, _, _, _ in NIGHT))
    return path


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "build"
    if cmd == "build":
        build()
    elif cmd == "gate":
        sys.exit(1 if gate() else 0)
    elif cmd == "pick":
        pick(sys.argv[2:] or None)
    elif cmd == "rebuild":
        sys.exit(1 if rebuild() else 0)
    elif cmd == "plant":
        sys.exit(0 if plant() else 1)
    elif cmd == "audition":
        audition()
    elif cmd == "table":
        table()
    else:
        raise SystemExit("build | gate | pick | rebuild | plant | audition | table")
