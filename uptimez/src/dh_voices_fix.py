"""Daddy's Home, film takes: Pam's remark (7.8) and second reads of the lines Whisper lost. For each key, the readings are
tried in order and the first heard in at least 2 of 3 windows is kept in dh_voices/film_v1; the old take is kept as
<key>_v1.wav. A reading may be several pieces joined with a pause ("Good." | "Find my money.").
  python3 dh_voices_fix.py"""
import os
import json
import shutil
import numpy as np
import soundfile as sf
import sound_bc as bc
import sound_ob as ob
import sound_fs as sfs
import dh_voices as dv

SR = 48000
OUT = dv.FILM_OUT
TRY = {   # key: (who, the line, [readings]); a reading is a list of (text, speed or None) pieces, joined with 0.32 s
    "7.8": ("PAM", "Some inspect. Others drink.", [[("Some inspect. Others drink.", None)], [("Some inspect.", None), ("Others drink.", None)]]),
    "3.1": ("DON", "Make it green.", [[("Make it, green.", 0.94)], [("Make it greeen.", 0.94)], [("Make it", 0.96), ("green.", 0.92)]]),
    "10.4a": ("FATHER", "Good. Find my money.", [[("Good.", None), ("Find my money.", None)], [("Good.", None), ("Find my money!", 0.92)],
                                                  [("Good.", None), ("Find. My money.", None)]]),
    "10.1": ("FATHER", "I prefer green in cash.", [[("I prefer green. In cash.", None)], [("I prefer green", None), ("in cash.", None)],
                                                    [("I prefer green in cash!", 0.92)]]),
    "10.2": ("FATHER", "You said it finds anything.", [[("You said, it finds anything.", None)], [("You said it finds anything!", 0.92)],
                                                        [("You said", None), ("it finds anything.", None)]]),
}


def piece(who, txt, sp):
    if who == "FATHER":
        v, s0, semis, note = dv.FATHER[dv.FATHER_VOICE]
        a = dv.one((v, sp or s0, semis, note), txt)
    elif who == "DON":
        a = bc.don(txt, sp or 1.0)
    else:
        a = dv.film_take(who, txt, None)
    return ob.trim(np.asarray(a, dtype=np.float64))


def main():
    import sherpa_onnx as so_
    d = os.environ.get("ASR_DIR", "/home/claude/models/asr/sherpa-onnx-whisper-base.en") + "/"
    r = so_.OfflineRecognizer.from_whisper(encoder=d + "base.en-encoder.int8.onnx", decoder=d + "base.en-decoder.int8.onnx",
                                          tokens=d + "base.en-tokens.txt")
    meta = json.load(open(OUT + "/takes.json"))
    for key, (who, line, readings) in TRY.items():
        best = None
        for n, rd in enumerate(readings):
            parts = []
            for i, (txt, sp) in enumerate(rd):
                if i:
                    parts.append(np.zeros(int(0.32 * SR)))
                parts.append(piece(who, txt, sp))
            a = np.concatenate(parts)
            a16 = np.interp(np.linspace(0, len(a) - 1, int(len(a) * 16000 / SR)), np.arange(len(a)), a)
            pad = np.zeros(4800); heard = []
            for w in (a16, np.concatenate([pad, a16]), np.concatenate([a16, pad])):
                s = r.create_stream(); s.accept_waveform(16000, w.astype(np.float32)); r.decode_stream(s)
                heard.append(s.result.text.strip())
            good = sum(1 for h in heard if sfs._match(h, " ".join(sfs._words(line))))
            print("%-5s try %d  %4.2f s  %d/3  %s | %s" % (key, n + 1, len(a) / float(SR), good, " | ".join(t for t, _ in rd), heard), flush=True)
            if best is None or good > best[0]:
                best = (good, a, heard, rd)
            if good == 3:
                break
        good, a, heard, rd = best
        p = "%s/%s.wav" % (OUT, key)
        if os.path.exists(p) and not os.path.exists(p[:-4] + "_v1.wav"):
            shutil.copy(p, p[:-4] + "_v1.wav")
        sf.write(p, a.astype(np.float32), SR)
        meta[key] = dict(who=who, text=line, len=round(len(a) / float(SR), 2), asr=heard, ok=good, given=[t for t, _ in rd])
        print("== %s kept: %d/3, %.2f s" % (key, good, len(a) / float(SR)), flush=True)
    json.dump(meta, open(OUT + "/takes.json", "w"), indent=1)
    print("spoken: %.1f s in %d lines; heard at least 2 of 3: %d" % (sum(m["len"] for m in meta.values()), len(meta),
                                                                     sum(1 for m in meta.values() if m["ok"] >= 2)))


if __name__ == "__main__":
    main()
