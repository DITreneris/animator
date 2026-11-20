"""OFFICE NOIR 3: the narrator, noir, v1 (20 Nov). Tomas: "the voice we use now, lowered a bit, a real noir sound; think
about the pauses between sentences and the intonation before generating."
The man: the film's own (am_fenrir). What changes:
  lower     5 semitones down (was 4)
  slower    the speech itself at 0.90 (was 1.00), so the words are slower, not only the recording
  pauses    a line is spoken phrase by phrase and the silences are written, not left to the model: 0.30 s at a comma,
            0.50 s between two sentences, 0.60 s before a line's turn (the half that undoes the first half)
  intonation  every phrase ends on a full stop and is chosen, out of four takes, for a pitch that falls from its first
            third to its last (measured before lowering); a noir narrator states, he does not ask
  the sound close and dry: more chest (a low shelf), less top (rolled off above 6.5 kHz), a little tape (soft
            saturation), level held even (a slow compressor), a small dark room, very low
PHRASES: key -> [(phrase, silence after it)]. take(key) -> the line. build() -> the audition and every take.
  KOKORO_DIR=/tmp/kokoro python3 on3_narr_noir.py"""
import os
import json
import subprocess
import numpy as np
import soundfile as sf
import scipy.signal as sg

os.environ.setdefault("KOKORO_DIR", "/tmp/kokoro")
import sound_on as so
import sound_bc as bc
import sound_ob as sob
import sound_xmas as sx

SR = so.SR
OUT = "on3_voices/narr_noir_v1"
VOICE, SPEED, SEMIS = "am_fenrir", 0.90, -5.0
COMMA, STOP, TURN = 0.30, 0.50, 0.60
PHRASES = {
    "n1": [("Word is.", COMMA), ("I know how business works.", 0)],
    "n2": [("One fight.", 0)],
    "n2b": [("My manager.", TURN), ("Also my mother.", 0)],
    "n3": [("One folder.", 0)],
    "n4": [("One woman.", 0)],
    "n4b": [("One number.", COMMA), ("I never called.", 0)],
    "n5": [("Nothing scares me.", 0)],
    "n6": [("I make my own fire.", 0)],
    "n6b": [("If you want to survive, you need to bargain.", 0)],      # one phrase: the comma is the model's own, the fall comes at the end
    "n7": [("I name my price.", 0)],
    "n7b": [("I don't believe in signs.", 0)],
    "n7c": [("I always hit first.", 0)],
    "n8": [("I don't break.", TURN), ("I break even.", 0)],
    "n9": [("It was a fair fight.", 0)],
    "n11": [("But I didn't quit.", 0)],
    "n12": [("Ten garages.", STOP), ("That was the plan.", 0)],
    "n13": [("I'll call her back tomorrow.", 0)],
    "n14": [("Tomorrow.", 0)],
}
_LOG = {}


def _trim(a):
    idx = np.where(np.abs(a) > 0.02 * np.max(np.abs(a)))[0]
    return a[max(0, idx[0] - int(0.01 * SR)):min(len(a), idx[-1] + int(0.06 * SR))]


def phrase(txt, order=(1.0, 0.96, 1.04, 0.92)):
    """Four takes; the first whose pitch falls from its first third to its last, else the one that rises least."""
    best = None
    for f in order:
        a = _trim(np.asarray(sx.say(txt, VOICE, SPEED * f, "en-us"), dtype=np.float64))
        a = a / np.sqrt(np.mean(a ** 2)) * 0.11
        p0, p1 = sob.slope(a)
        fall = p0 - p1
        if best is None or fall > best[1]:
            best = (a, fall, f, p0, p1)
        if fall > 4.0:
            break
    return best


def noir(a):
    a = so.pitch(a, SEMIS)
    b, a_ = sg.butter(2, 190 / (SR / 2), "low"); a = a + sg.lfilter(b, a_, a) * 0.55            # chest
    b, a_ = sg.butter(2, 6500 / (SR / 2), "low"); a = sg.lfilter(b, a_, a)                       # no top
    b, a_ = sg.butter(2, 60 / (SR / 2), "high"); a = sg.lfilter(b, a_, a)
    env = np.sqrt(sg.lfilter(*sg.butter(1, 8 / (SR / 2), "low"), a ** 2) + 1e-9)                 # a slow compressor, 2.5 to 1 above the middle
    mid = np.median(env[env > 0.2 * env.max()])
    a = a * np.where(env > mid, (env / mid) ** (1 / 2.5 - 1), 1.0)
    a = np.tanh(a * 5.0) / 5.0                                                                   # a little tape
    return bc.norm(so.room(a, 0.07))


def _ok(h, want):
    """Heard word for word; a recogniser that repeats a short line over and over has still heard it."""
    h = ["ten" if w == "10" else w for w in h]
    return h == want or (len(h) > len(want) and all(h[i] == want[i % len(want)] for i in range(len(h))))


def take(key, order=(1.0, 0.96, 1.04, 0.92)):
    parts, log = [], []
    for txt, gap in PHRASES[key]:
        a, fall, f, p0, p1 = phrase(txt, order)
        parts += [a, np.zeros(int(gap * SR / 2 ** (-SEMIS / 12)))]            # the silence is written as heard, after the lowering
        log.append({"phrase": txt, "speed": round(SPEED * f, 3), "pitch_start_hz": round(p0, 1), "pitch_end_hz": round(p1, 1), "falls": fall > 0, "pause_after": gap})
    _LOG[key] = log
    return noir(np.concatenate(parts))


def _heard(a):
    """As on3_animatic.heard, but a number keeps its digits (the recogniser writes "10 garages")."""
    import re
    import on3_animatic as an
    an.heard(a)
    st = an._ASR[0].create_stream()
    x = np.concatenate([np.zeros(SR // 4), a / (np.max(np.abs(a)) + 1e-9) * 0.7, np.zeros(SR // 4)]).astype(np.float32)
    st.accept_waveform(SR, x); an._ASR[0].decode_stream(st)
    return re.sub(r"[^a-z0-9' ]", "", st.result.text.lower().replace("-", " ")).split()


def build(out="../office-noir-3/on3_narration_audition_v2.mp4"):
    import cairo
    import on3_animatic as an
    os.makedirs(OUT, exist_ok=True)
    seq, t, marks = [np.zeros(int(0.4 * SR))], 0.4, []
    for key in PHRASES:
        text = " ".join(p for p, _ in PHRASES[key]).replace("Word is.", "Word is,").replace("One number.", "One number")
        for order in ((1.0, 0.96, 1.04, 0.92), (0.96,), (1.04,), (0.92,), (1.08,)):       # the whole line again, at another pace, until it is heard word for word
            a = take(key, order); h = _heard(a)
            if _ok(h, an._words(text)):
                break
        else:
            a = take(key); h = _heard(a)
        sf.write("%s/%s.wav" % (OUT, key), a.astype(np.float32), SR)
        _LOG[key].append({"heard": " ".join(h), "heard_ok": _ok(h, an._words(text)), "length": round(len(a) / SR, 2)})
        marks.append((t, t + len(a) / SR, text)); seq += [a, np.zeros(int(0.7 * SR))]; t += len(a) / SR + 0.7
    a = np.concatenate(seq); a = a / np.max(np.abs(a)) * 0.7
    sf.write("/tmp/_noir.wav", a.astype(np.float32), SR)
    json.dump(_LOG, open(OUT + "/takes.json", "w"), indent=1)
    n = int(len(a) / SR * 30)
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", "540x960", "-r", "30", "-i", "-", "-i", "/tmp/_noir.wav",
                          "-c:v", "libx264", "-crf", "20", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-ar", "48000", out], stdin=subprocess.PIPE)
    last, buf = None, None
    for i in range(n):
        T = i / 30.0
        cur = next((tx for s0, s1, tx in marks if s0 - 0.05 <= T < s1 + 0.2), "")
        if cur != last:
            s = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(s)
            c.set_source_rgb(0.07, 0.07, 0.08); c.paint()
            if cur:
                an._card(c, cur, 400)
            buf, last = bytes(s.get_data()), cur
        p.stdin.write(buf)
    p.stdin.close(); p.wait()
    return _LOG


if __name__ == "__main__":
    for k, v in build().items():
        print(k, v[-1]["length"], v[-1]["heard_ok"], "|", v[-1]["heard"], "|", [(q["falls"], q["pitch_start_hz"], q["pitch_end_hz"], q["speed"]) for q in v[:-1]])
