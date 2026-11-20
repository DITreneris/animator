"""FIRST SEARCH: the G5 speech check on a final film. Every line, cut from the final mix (the AAC), three windows (as
cut, with 0.3 s more before, with 0.3 s more after), heard by Whisper; a line passes at 2 of 3. A lone word gets the
line before it as context.  python3 fs_film_qa.py film.mp4 fs_timing_vN.json lead"""
import os
import re
import sys
import json
import subprocess
import numpy as np
import sherpa_onnx as so_
import fs_animatic as an


NONWORDS = {"eww", "ew"}


def words(t):
    return re.sub(r"[^a-z ]", " ", t.lower()).split()


def match(heard, want):
    h, w = words(heard), words(want)
    if not w:
        return True
    hit = sum(1 for x in w if any(x == y or (len(x) > 3 and (x in y or y in x)) for y in h))
    return hit / len(w) >= 0.6


def main(film, timing, lead):
    d = os.environ.get("ASR_DIR", "/home/claude/models/asr/sherpa-onnx-whisper-base.en") + "/"
    r = so_.OfflineRecognizer.from_whisper(encoder=d + "base.en-encoder.int8.onnx", decoder=d + "base.en-decoder.int8.onnx",
                                          tokens=d + "base.en-tokens.txt")
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", film, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    a = np.frombuffer(pcm, np.float32)
    rows = json.load(open(timing))
    at = {x["shot"]: x["start"] for x in rows}
    bad, prev = 0, None
    for s in sorted(an.LINE_OF, key=lambda x: at[x]):                    # in film order (the context is the line before)
        key = an.LINE_OF[s]
        m = an.TAKES[key]
        t0, t1 = at[s] + lead, at[s] + lead + m["len"]
        want = m["text"]
        if want.strip(".!? ").lower() in NONWORDS:                      # "Eww." is not a word Whisper can spell: it is
            w = a[int(t0 * 16000):int(t1 * 16000)]                       # checked as heard (loud enough in the mix)
            rms = float(np.sqrt(np.mean(w ** 2))) if len(w) else 0.0
            ok = rms > 0.02
            bad += not ok
            print("%-5s %s   %-45s | a sound, not a word: rms %.3f" % (s, "ok " if ok else "LOW", want, rms), flush=True)
            prev = (t0, t1)
            continue
        lone = len(words(want)) <= 2 and prev
        heard = []
        for p0, p1 in ((0.05, 0.15), (0.35, 0.15), (0.05, 0.45)):
            s0 = max(0, int((t0 - p0) * 16000)); s1 = int((t1 + p1) * 16000)
            w = a[s0:s1]
            if lone:
                pt0, pt1 = prev
                w = np.concatenate([a[int(pt0 * 16000):int(pt1 * 16000)], np.zeros(4000, np.float32), w])
            st = r.create_stream(); st.accept_waveform(16000, w.astype(np.float32)); r.decode_stream(st)
            heard.append(st.result.text.strip())
        ok = sum(1 for h in heard if match(h, want))
        bad += ok < 2
        print("%-5s %d/3  %-45s | %s" % (s, ok, want, " | ".join(heard)), flush=True)
        prev = (t0, t1)
    print("PASS" if not bad else "FAIL", "(%d lines under 2 of 3)" % bad)
    return bad


if __name__ == "__main__":
    sys.exit(1 if main(sys.argv[1], sys.argv[2], float(sys.argv[3])) else 0)
