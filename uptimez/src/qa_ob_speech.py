"""The Onboarding: speech recognition on every line inside the FINAL mix (uptimez/CLAUDE.md, G5 "Speech").
Whisper base.en through sherpa-onnx (the model from the k2-fsa/sherpa-onnx GitHub releases, in on_qa.ASR_DIR), the
method of Office Noir's worker (on_qa.py): three windows per line, a short line gets the line before it as context,
scored by words or by letters, two windows of three must reach 75 %.
What it is for here: nobody in the build chain hears the film. "Oh..." was delivered with 0.15 s of breath in front
of it and was heard as "so" by the director; this check is the ear that was missing. A lone interjection is the
hardest case for Whisper, so "Oh..." is also reported by its first sound: the transcript of its own window must not
begin with an s.
  python3 qa_ob_speech.py FILM.mp4 [timing.json]      exit code 1 on a miss"""
import json
import sys
import on_qa as oq


def main(film, timing):
    T = json.load(open(timing))
    rec = oq._recognizer(); a = oq._audio(film)
    lines = [s for s in T["shots"] if "line" in s]
    bad, rows = 0, []
    for i, s in enumerate(lines):
        ln = s["line"]; t0, t1 = ln["t0"], ln["t1"] + 0.45
        if i + 1 < len(lines):
            t1 = min(t1, lines[i + 1]["line"]["t0"] - 0.02)
        w0 = t0 - 0.10
        short = ln["t1"] - ln["t0"] < 1.2
        if short and i and t0 - lines[i - 1]["line"]["t0"] < 4.5:        # a lone word: the line before as context
            w0 = lines[i - 1]["line"]["t0"] - 0.10
        want = oq._words(ln["text"]); res = []
        for d0, d1 in ((0.0, 0.0), (-0.05, 0.15), (0.05, -0.10)):
            got = oq.transcribe(rec, a, w0 + d0, t1 + d1)
            have = oq._words(got)
            if w0 < t0 - 0.2:
                have = have[-(len(want) + 2):]
            ws = oq._lcs(want, have) / len(want)
            cw, ch = "".join(want), "".join(have)
            cs = 1 - oq._lev(cw, ch) / max(1, len(cw))
            res.append((max(ws, cs if cs >= 0.85 else 0.0), got))
        n_ok = sum(sc >= 0.75 for sc, _ in res)
        ok = n_ok >= 2
        note = ""
        if ln["text"].lower().startswith("oh"):                          # its own window, alone: what is its first sound?
            alone = oq.transcribe(rec, a, t0 - 0.12, ln["t1"] + 0.30)
            first = (oq._words(alone) or [""])[0]
            note = "   alone: \"%s\"" % alone
            if first.startswith("s"):
                ok = False; note += "  <- begins with an s"
        bad += not ok
        score, got = min(res) if not ok else max(res)
        rows.append("  %-4s %-5s %-6s %d/3 %4.0f%%  want \"%s\"  heard \"%s\"%s" % (
            "ok" if n_ok == 3 and ok else "ok~" if ok else "MISS", s["shot"], ln["who"], n_ok, score * 100, ln["text"], got, note))
    print("\n".join(rows))
    print("speech: %d of %d lines heard in the final mix%s" % (len(lines) - bad, len(lines), "" if not bad else "  FAIL"))
    return bad


if __name__ == "__main__":
    sys.exit(1 if main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "ob_anim_timing_v9.json") else 0)
