"""OFFICE NOIR 4: Seven Lives. Stage 2 of series/production-process.md: the voices and the timing (23 Nov).
Script v3 (approved at stop 1). Four lines, and one optional remark for Tomas to decide by ear:
  n1  1.3  PAM (narration)  "I know how to survive."
  n2  2.4  PAM (narration)  "I know where to see what others do not see."
  n3  3.6  PAM (narration)  "I am like a cat. I have seven lives."
  s1  7.2  SOFIA            "Only for you."
  r1  8.1  PAM (awake)      "Some shine. Others brew."   (open decision 1; not in the timing unless REMARK)
Pam's narration is auditioned three ways (her British voice by audition, lower and drier than her office voice):
  A  bf_emma, her series voice, 2 semitones down, spoken at 0.90, the noir chain (as Sofia's narration in Office Noir 2)
  B  bf_emma, 3 semitones down, at 0.84, longer pauses
  C  bf_isabella (Christmas audition C: low, tired, deadpan), 1 semitone down, at 0.88
Each phrase: four takes, the first whose pitch falls (a noir narrator states, she does not ask; on3_narr_noir).
Each line: heard by the recognizer in three windows (series standard), else taken again at another pace.
  KOKORO_DIR=/tmp/kokoro python3 on4_voices.py audition   -> ../office-noir-4/on4_voices_audition_v1.mp4, on4_voices/audition_v1/
  KOKORO_DIR=/tmp/kokoro python3 on4_voices.py timing [A|B|C] [remark]
                                                          -> ../office-noir-4/on4_timing_v1.json, on4_voices_timing_v1.mp4"""
import os
import sys
import json
import subprocess
import numpy as np
import soundfile as sf
import scipy.signal as sg

os.environ.setdefault("KOKORO_DIR", "/tmp/kokoro")
import sound_on as so
import sound_ob as sob
import sound_bc as bc
import sound_xmas as sx
import sound_fs as sfs

SR = so.SR
OUT = "on4_voices"
COMMA, STOP, TURN = 0.30, 0.50, 0.60
LINES = {   # key: (shot, who, [(phrase, pause after)])
    "n1": ("1.3", "PAM_N", [("I know how to survive.", 0)]),
    "n2": ("2.4", "PAM_N", [("I know where to see", COMMA), ("what others do not see.", 0)]),
    "n3": ("3.6", "PAM_N", [("I am like a cat.", STOP), ("I have seven lives.", 0)]),
    "s1": ("7.2", "SOFIA", [("Only for you.", 0)]),
    "r1": ("8.1", "PAM", [("Some shine.", STOP), ("Others brew.", 0)]),
}
KINDS = {   # voice, lang, speed, semitones, pause factor, note
    "A": ("bf_emma", "en-gb", 0.90, -2.0, 1.0, "Pam's own voice, 2 semitones down, slower"),
    "B": ("bf_emma", "en-gb", 0.84, -3.0, 1.4, "Pam's own voice, 3 down, slower still, longer pauses"),
    "C": ("bf_isabella", "en-gb", 0.88, -1.0, 1.0, "a lower, tired voice, 1 semitone down"),
}
PAM_AWAKE = ("bf_emma", "en-gb", 0.92)          # her series voice (sound_xmas.PAMS A)
SOFIA = ("af_bella", "en-us", 1.0)
_R = [None]


def recognizer():
    if _R[0] is None:
        import sherpa_onnx as so_
        d = os.environ.get("ASR_DIR", "/home/claude/models/asr/sherpa-onnx-whisper-base.en") + "/"
        _R[0] = so_.OfflineRecognizer.from_whisper(encoder=d + "base.en-encoder.int8.onnx", decoder=d + "base.en-decoder.int8.onnx",
                                                   tokens=d + "base.en-tokens.txt")
    return _R[0]


def heard3(a):
    """The series' three windows: the take alone, with air before, with air after."""
    r = recognizer()
    a16 = np.interp(np.linspace(0, len(a) - 1, int(len(a) * 16000 / SR)), np.arange(len(a)), a)
    a16 = a16 / (np.abs(a16).max() + 1e-9) * 0.7
    pad = np.zeros(4800)
    out = []
    for w in (a16, np.concatenate([pad, a16]), np.concatenate([a16, pad])):
        s = r.create_stream(); s.accept_waveform(16000, w.astype(np.float32)); r.decode_stream(s)
        out.append(s.result.text.strip())
    return out


def _trim(a):
    idx = np.where(np.abs(a) > 0.02 * np.max(np.abs(a)))[0]
    return a[max(0, idx[0] - int(0.01 * SR)):min(len(a), idx[-1] + int(0.06 * SR))]


def phrase(txt, voice, lang, speed, order):
    """Takes in order of pace; the first whose pitch falls by 4 Hz from its first third to its last, else the one that falls most."""
    best = None
    for f in order:
        a = _trim(np.asarray(sx.say(txt, voice, speed * f, lang), dtype=np.float64))
        a = a / np.sqrt(np.mean(a ** 2)) * 0.11
        p0, p1 = sob.slope(a)
        if best is None or p0 - p1 > best[1]:
            best = (a, p0 - p1, f, p0, p1)
        if p0 - p1 > 4.0:
            break
    return best


def noir(a, semis):
    """Her voice close and dry: lowered, a little chest, the very top rolled off, a slow compressor, a touch of tape, a small room."""
    a = so.pitch(a, semis)
    b, a_ = sg.butter(2, 260 / (SR / 2), "low"); a = a + sg.lfilter(b, a_, a) * 0.35
    b, a_ = sg.butter(2, 7500 / (SR / 2), "low"); a = sg.lfilter(b, a_, a)
    b, a_ = sg.butter(2, 80 / (SR / 2), "high"); a = sg.lfilter(b, a_, a)
    env = np.sqrt(sg.lfilter(*sg.butter(1, 8 / (SR / 2), "low"), a ** 2) + 1e-9)
    mid = np.median(env[env > 0.2 * env.max()])
    a = a * np.where(env > mid, (env / mid) ** (1 / 2.5 - 1), 1.0)
    a = np.tanh(a * 4.0) / 4.0
    return bc.norm(so.room(a, 0.06))


def line(key, kind="A", order=(1.0, 0.96, 1.04, 0.92)):
    shot, who, parts = LINES[key]
    if who == "PAM_N":
        voice, lang, speed, semis, pf, _ = KINDS[kind]
    elif who == "PAM":
        (voice, lang, speed), semis, pf = PAM_AWAKE, 0.0, 1.0
    else:
        (voice, lang, speed), semis, pf = SOFIA, 0.0, 1.0
    seq, log = [], []
    for txt, gap in parts:
        a, fall, f, p0, p1 = phrase(txt, voice, lang, speed, order)
        seq += [a, np.zeros(int(gap * pf * SR * 2 ** (semis / 12)))]      # the pause is written as heard, after the lowering
        log.append(dict(phrase=txt, speed=round(speed * f, 3), pitch_start=round(p0, 1), pitch_end=round(p1, 1), falls=bool(fall > 0)))
    a = np.concatenate(seq)
    a = noir(a, semis) if who == "PAM_N" else bc.norm(a)
    return a, log


def take(key, kind="A"):
    """A take that the recognizer hears in at least 2 of 3 windows; another pace until it does."""
    want = " ".join(sfs._words(" ".join(p for p, _ in LINES[key][2])))
    for order in ((1.0, 0.96, 1.04, 0.92), (0.96,), (1.04,), (0.92,), (1.08,)):
        a, log = line(key, kind, order)
        h = heard3(a)
        ok = sum(1 for x in h if sfs._match(x, want))
        if ok >= 2:
            break
    sat = float(np.mean(np.abs(a / (np.abs(a).max() + 1e-9)) > 0.98))
    return a, dict(key=key, shot=LINES[key][0], who=LINES[key][1], kind=kind if LINES[key][1] == "PAM_N" else None, text=want,
                   len=round(len(a) / SR, 2), asr=h, ok=ok, phrases=log, saturated=round(sat * 100, 2))


def _card(c, lines_, y, size=30):
    c.select_font_face("Special Elite", 0, 0)
    for i, (txt, sz) in enumerate(lines_):
        c.set_font_size(sz)
        words, row, rows = txt.split(), "", []
        for w in words:
            if c.text_extents((row + " " + w).strip()).x_advance > 470:
                rows.append(row); row = w
            else:
                row = (row + " " + w).strip()
        rows.append(row)
        for r_ in rows:
            e = c.text_extents(r_)
            c.move_to(270 - e.x_advance / 2, y); c.show_text(r_); y += sz * 1.35
        y += 14
    return y


def _mp4(audio, cards, out):
    """cards: [(t0, t1, [(text, size)])]; black frames with the card of the moment, the audio under them."""
    import cairo
    a = audio / (np.abs(audio).max() + 1e-9) * 0.7
    sf.write("/tmp/_on4.wav", a.astype(np.float32), SR)
    n = int(len(a) / SR * 30) + 1
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", "540x960", "-r", "30", "-i", "-",
                          "-i", "/tmp/_on4.wav", "-c:v", "libx264", "-crf", "20", "-preset", "veryfast", "-pix_fmt", "yuv420p",
                          "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-shortest", out + ".tmp.mp4"], stdin=subprocess.PIPE)
    last, buf = -1, None
    for i in range(n):
        T = i / 30.0
        cur = next((j for j, (t0, t1, _) in enumerate(cards) if t0 <= T < t1), None)
        if cur != last:
            s = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(s)
            c.set_source_rgb(0.07, 0.07, 0.08); c.paint(); c.set_source_rgb(0.93, 0.90, 0.82)
            if cur is not None:
                _card(c, cards[cur][2], 300)
            buf, last = bytes(s.get_data()), cur
        p.stdin.write(buf)
    p.stdin.close(); p.wait()
    if p.returncode == 0:
        os.replace(out + ".tmp.mp4", out)


def audition(out="../office-noir-4/on4_voices_audition_v1.mp4"):
    d = OUT + "/audition_v1"; os.makedirs(d, exist_ok=True)
    seq, cards, t, meta = [np.zeros(int(0.5 * SR))], [], 0.5, []
    plan = [(k, kind) for kind in KINDS for k in ("n1", "n2", "n3")] + [("s1", None), ("r1", None)]
    for k, kind in plan:
        a, m = take(k, kind or "A")
        name = "%s_%s" % (k, kind) if kind else k
        sf.write("%s/%s.wav" % (d, name), a.astype(np.float32), SR)
        m["file"] = name; meta.append(m)
        label = ("PAM, narration %s" % kind) if kind else ("SOFIA" if k == "s1" else "PAM, awake (the remark, open)")
        note = KINDS[kind][5] if kind else ""
        cards.append((t - 0.3, t + len(a) / SR + 0.5, [(label, 34), (note, 20), ('"%s"' % " ".join(p for p, _ in LINES[k][2]), 28)]))
        seq += [a, np.zeros(int(0.9 * SR))]; t += len(a) / SR + 0.9
        print("%-4s %-5s %-2s %5.2f s  heard %d/3  sat %.2f%%  | %s" % (k, m["who"], kind or "", m["len"], m["ok"], m["saturated"], m["asr"][0]), flush=True)
    json.dump(meta, open(d + "/takes.json", "w"), indent=1)
    _mp4(np.concatenate(seq), cards, out)
    return meta


# Script v3's shots and their planned lengths (s). A shot with a line is lengthened when the line needs more:
# the line starts LEAD after the shot starts and the shot runs at least TAIL past its end.
SHOTS = [("1.1", 1.0), ("1.2", 1.6), ("1.3", 2.6), ("1.4", 2.8),
         ("2.1", 2.2), ("2.2", 1.6), ("2.3", 2.0), ("2.4", 3.2),
         ("3.1", 2.4), ("3.2", 1.4), ("3.3", 3.2), ("3.4", 1.8), ("3.5", 2.0), ("3.6", 2.8),
         ("4.1", 2.6), ("4.2", 1.4), ("4.3", 3.0),
         ("5.1", 2.0), ("5.2", 1.0), ("5.3", 3.6),
         ("6.1", 1.4), ("6.2", 1.2), ("6.3", 2.0), ("6.4", 0.9), ("6.5", 1.6), ("6.6", 2.2),
         ("7.1", 1.4), ("7.2", 3.2), ("7.3", 1.4), ("7.4", 1.6), ("7.5", 1.8),
         ("8.1", 2.6), ("8.2", 1.2)]
LEAD = {"1.3": 0.7, "2.4": 0.3, "3.6": 0.5, "7.2": 1.2, "8.1": 0.4}     # 1.3 after the sag starts; 7.2 as the envelope goes in
TAIL = 0.5
WHAT = {"1.1": "Frame 0. Pam-Cat's hero pose, Sofia walking at her", "1.2": "0:01 Sofia sidesteps her", "1.3": "The pose sags",
        "1.4": "The shadows run to the taillights", "2.1": "The fire escape, the car below", "2.2": "The back seat",
        "2.3": "Insert: two taps, into his coat", "2.4": "Pam drops down the ladder", "3.1": "Don waves the car through",
        "3.2": "The bump", "3.3": "Don wipes the bumper", "3.4": "The ringed hand drops the bills", "3.5": "They step over her",
        "3.6": "She sits up", "4.1": "The club, the marquee lights up", "4.2": "Insert: the marquee", "4.3": "She points at it, at herself",
        "5.1": "The club inside", "5.2": "Insert: the map", "5.3": "The lift from the coat", "6.1": "Into the spotlight",
        "6.2": "Insert: Sofia's CV", "6.3": "The triumph pose; the music stops", "6.4": "Insert: the glove on the lamp",
        "6.5": "The light leaves her (the cover)", "6.6": "Her arm comes down", "7.1": "Awake: asleep on the counter, arm up",
        "7.2": "Sofia posts the envelope", "7.3": "She wakes", "7.4": "Insert: COFFEE ROTA", "7.5": "She counts the PAMs",
        "8.1": "Mask down, head down", "8.2": "The lamp: the loop"}


def timing(kind="A", remark=False, out_json="../office-noir-4/on4_timing_v1.json", out_mp4="../office-noir-4/on4_voices_timing_v1.mp4"):
    d = OUT + "/takes_v1"; os.makedirs(d, exist_ok=True)
    keys = ["n1", "n2", "n3", "s1"] + (["r1"] if remark else [])
    by_shot = {}
    for k in keys:
        a, m = take(k, kind)
        sf.write("%s/%s.wav" % (d, k), a.astype(np.float32), SR)
        by_shot[m["shot"]] = (k, a, m)
    t, shots, cards = 0.0, [], []
    audio = np.zeros(int(90 * SR))
    for sid, plan in SHOTS:
        dur = plan
        row = dict(shot=sid, start=round(t, 2), planned=plan, what=WHAT[sid])
        if sid in by_shot:
            k, a, m = by_shot[sid]
            need = LEAD[sid] + m["len"] + TAIL
            dur = max(plan, need)
            t0 = t + LEAD[sid]; i0 = int(t0 * SR); audio[i0:i0 + len(a)] += a
            row.update(line=k, who=m["who"], text=m["text"], line_start=round(t0, 2), line_len=m["len"], asr_ok=m["ok"])
            cards.append((t, t + dur, [(sid, 40), (WHAT[sid], 22), ('"%s"' % " ".join(p for p, _ in LINES[k][2]), 28)]))
        else:
            cards.append((t, t + dur, [(sid, 40), (WHAT[sid], 22)]))
        row["dur"] = round(dur, 2); shots.append(row); t += dur
    audio = audio[:int(t * SR)]
    meta = dict(script="office-noir-4-script-v3.md", narration=kind, narration_note=KINDS[kind][5], remark=remark,
                length=round(t, 2), lines={k: by_shot[s][2] for s, (k, _, _) in by_shot.items()}, shots=shots)
    meta["lines"] = {k: m for (k, a, m) in by_shot.values()}
    json.dump(meta, open(out_json, "w"), indent=1)
    _mp4(audio, cards, out_mp4)
    bad = [k for k, m in meta["lines"].items() if m["ok"] < 2]
    print("length %.2f s, %d lines, heard 2 of 3 or better: %d of %d%s" % (t, len(keys), len(keys) - len(bad), len(keys),
          ("  FAILED: " + ", ".join(bad)) if bad else ""))
    return meta


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "audition"
    if cmd == "audition":
        audition()
    elif cmd == "timing":
        kind = next((x for x in sys.argv[2:] if x in KINDS), "A")
        m = timing(kind, "remark" in sys.argv[2:])
        if any(v["ok"] < 2 for v in m["lines"].values()):
            sys.exit(1)
