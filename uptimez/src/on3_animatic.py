"""OFFICE NOIR 3: the animatic, v1 (20 Nov). The whole-film rough (film_on3 v7) with scratch voices and a few effects.
What it is for: the length with the lines in, whether each shot has room for its line, and how the lines sit on the
pictures. It is not the film's sound: no music, no room, no rain; the takes are first takes, not auditioned, and the
speech check has not been run on them. Voices are the series' own: the Client (and his narration) am_fenrir, four
semitones down (sound_ob.client_line); Mom voice F (sound_bc.mom); Pam key A (sound_xmas.pam_line); the Referee a
scratch British voice (bm_george).
Timing: a shot is held on its last drawing when its line needs longer; a line never starts before the one before it has
ended. Narration may run on over the next shot; a spoken line may not.
Writes  on3_voices/animatic_v1/*.wav, takes.json        the takes and their lengths
        on3_animatic_timing_v1.json                     every shot: start, length, lines; every effect
        ../office-noir-3/on3_animatic_v1.mp4            540 x 960, 30 fps, AAC
  KOKORO_DIR=/tmp/kokoro python3 on3_animatic.py"""
import json
import math
import os
import subprocess
import sys
import cairo
import numpy as np
import soundfile as sf

os.environ.setdefault("KOKORO_DIR", "/tmp/kokoro")
import sound_on as so
import sound_bc as bc
import sound_ob as sob
import sound_xmas as sx
import ring_rough_on3 as rr
import film_on3 as fm

V = "v28"
SR = so.SR
VOICES = "on3_voices/animatic_" + V
FPS = 30
GAP = 0.20                                                  # v5: air between lines, as in Office Noir 2
LEAD = 0.15                                                 # a narration line never starts on the cut

# shot -> [(who, line, take key, offset into the shot)]
LINES = {                                                    # v6: the lines, proposal v2 (on3_lines_proposal_v2.md)
    "1.1": [("N", "Word is, I know how business works.", "n1", 0.15)],      # v14: it starts on the punch (it began on the poster and pushed everything after it)
    "2.1": [("N", "One fight.", "n2", 0.15)],
    "2.2": [("MOM", "Where are you going, skunk?", "m1", 0.3), ("N", "My manager. Also my mother.", "n2b", 0.3)],
    "2.4": [("MOM", "Everything you need is in there.", "m2", 0.5)],
    "2.4b": [("N", "One folder.", "n3", 0.1)],
    "2.5": [("N", "One woman.", "n4", 0.2)],
    "2.7": [("N", "One number I never called.", "n4b", 0.3)],
    "2.6": [("SOFIA", "Call me.", "s1", 1.05)],
    "3.1": [("N", "Nothing scares me.", "n5", 0.2)],
    "3.2": [("N", "I make my own fire.", "n6", 0.1)],
    "3.4d": [("DON", "Just looking.", "d1", 0.15)],
    "4.1": [("N", "If you want to survive, you need to bargain.", "n6b", 0.15)],     # v21 (Tomas: "is it in its place? maybe after Just looking."): on his way in to her desk, as the set-up of "How much?" / "I name my price."; the alley's reveal of Don plays without a voice over it
    "4.3": [("CLIENT", "How much?", "c1", 0.3), ("MOM", "One hundred bucks.", "m3", 0.3)],
    "4.4": [("N", "I name my price.", "n7", 0.6)],
    "4.4a": [("MOM", "Your ticket. You're fighting.", "m4", 0.1)],
    "4.4t": [("N", "I don't believe in signs.", "n7b", 0.15)],
    "5.1a": [("SOFIA", "Round one.", "s2", 0.8)],
    "5.1c": [("PAM", "I'll help you undress.", "p1", 0.1), ("PAM", "Too late. The bell.", "p2", 1.95)],
    "5.2": [("N", "I always hit first.", "n7c", 0.2)],                # v7 (Tomas, at 0:50): the narrator, briefly, on the fight
    "5.3": [("ROBOT", "Human approval required.", "rb1", 0.2)],
    "5.5": [("MOM", "Approved.", "m5", 0.0), ("N", "I don't break. I break even.", "n8", 1.15)],   # v17: the narrator starts on the fall (on the count it held the corner for 1.3 s)                       # v16: she presses first; the word comes off the button (it came half a second before it)
    "6.1": [("PAM", "Some punch. Others patch.", "p3", 0.5)],
    "6.2": [("N", "It was a fair fight.", "n9", 0.0)],
    "6.3": [("DON", "The woman in the photo…", "d2", 0.3), ("DON", "Recognize her?", "d3", 2.0)],
    "6.4": [("DON", "Case closed.", "d4", 0.45)],
    "7.1": [("N", "But I didn't quit.", "n11", 0.1)],
    "7.2": [("N", "Ten garages. That was the plan.", "n12", 0.05)],   # v17 (Tomas: "start it earlier"): over his punches; 7.3 is no longer held for it
    "7.2b": [("REFEREE", "Break!", "r1", 0.75)],
    "7.3": [("ROBOT", "Human approval still pending.", "rb2", 1.45)],        # v18: pre-laps the cut to it
    "7.4c": [("MOM", "Approved.", "m6", 0.0)],                       # v17: her office is not shown a second time: the button, the tick, her word
    "8.3": [("N", "I'll call her back tomorrow.", "n13", 0.5)],
    "8.4": [("N", "Tomorrow.", "n14", 0.5)],
}
FX = [("punch", "1.1", 1.06), ("punch", "7.2", 0.58), ("punch", "7.2", 1.76), ("snap", "3.2c", 0.42), ("bell", "5.1c", 1.55), ("bell", "5.2a", 0.0), ("click", "5.4b", 0.15), ("stamp", "5.4b", 0.17),
      ("punch", "5.5", 0.67), ("pop", "6.2a", 0.2), ("pop", "6.2a", 0.5), ("pop", "6.2b", 0.3), ("pop", "6.2b", 0.9), ("stamp", "6.4", 0.34),
      ("click", "7.4b", 0.15), ("punch", "7.5", 0.75), ("chime", "8.1", 0.05), ("buzz", "8.2", 0.2), ("buzz", "8.3", 0.1), ("buzz", "8.3", 0.8),
      ("buzz", "8.3b", 0.05), ("bell", "8.5", 0.75)]


def trim(a, thr=0.012):
    idx = np.where(np.abs(a) > thr * np.max(np.abs(a)) / 0.1)[0]
    if not len(idx):
        return a
    return a[max(0, idx[0] - int(0.02 * SR)):min(len(a), idx[-1] + int(0.10 * SR))]


_ASR = []


def heard(a):
    """What a speech recogniser hears in a take (Whisper base.en, through sherpa-onnx), lower case, letters only."""
    import sherpa_onnx, re
    if not _ASR:
        d = os.environ.get("ASR_DIR", "/tmp/asr/sherpa-onnx-whisper-base.en")
        _ASR.append(sherpa_onnx.OfflineRecognizer.from_whisper(encoder=d + "/base.en-encoder.int8.onnx", decoder=d + "/base.en-decoder.int8.onnx",
                                                               tokens=d + "/base.en-tokens.txt", num_threads=2))
    st = _ASR[0].create_stream()
    x = np.concatenate([np.zeros(SR // 4), a / (np.max(np.abs(a)) + 1e-9) * 0.7, np.zeros(SR // 4)]).astype(np.float32)
    st.accept_waveform(SR, x); _ASR[0].decode_stream(st)
    return re.sub(r"[^a-z' ]", "", st.result.text.lower().replace("-", " ").replace("$100", "one hundred").replace("100", "one hundred")).split()


def _words(t):
    import re
    return re.sub(r"[^a-z' ]", "", t.lower().replace("-", " ")).split()


def takes():
    """v5: up to five takes of every line (as written, then 6% and 12% slower, 7% and 13% quicker); the first one a
    speech recogniser hears word for word is the take; if none is, the one with the fewest words wrong, and the line is
    listed in speech_check.json to be re-voiced."""
    os.makedirs(VOICES, exist_ok=True)
    pv, psp, _ = sx.PAMS["A"]
    cv, csp, csem, _ = sob.CANDS[sob.CLIENT]
    client = lambda t, f: bc.norm(sob.warm(so.pitch(so.dry(t, cv, csp * f), csem)))
    import on3_narr_clean as nc
    say = {"CLIENT": client, "MOM": lambda t, f: bc.mom(t, f), "SOFIA": lambda t, f: bc.sofia(t, f), "ROBOT": lambda t, f: bc.robot(t, 1.12 * f),
           "DON": lambda t, f: bc.norm(so.dry(t, "am_michael", 1.08 * f)),          # v6: Don's voice 1 of his audition; the narrator has am_onyx
           "PAM": lambda t, f: bc.norm(so.dry(t, pv, 1.0 * f)), "REFEREE": lambda t, f: bc.norm(so.dry(t, "bm_george", 1.05 * f))}
    meta, log = {}, {}
    for shot, ls in LINES.items():
        for who, text, key, _ in ls:
            import hashlib
            cp = "on3_voices/cache/%s_%s" % (who, hashlib.md5(("v6|" + who + "|" + text).encode()).hexdigest()[:12])
            if os.path.exists(cp + ".wav"):                   # v7: a take chosen once is kept; only new lines are recorded
                a = sf.read(cp + ".wav")[0]; sf.write("%s/%s.wav" % (VOICES, key), a.astype(np.float32), SR)
                meta[key] = round(len(a) / SR, 3); log[key] = json.load(open(cp + ".json")); continue
            tried, best = [], None
            for f in (1.0, 0.94, 1.07, 0.88, 1.13):
                if who == "N":                                # v6: the narrator: Don's voice, the Noir 1 recipe, phrase by phrase with written pauses
                    a = np.asarray(nc.take(key, "D", f), dtype=np.float64)
                else:
                    a = trim(np.asarray(say[who](text, f), dtype=np.float64))
                h = heard(a)
                want = _words(text)
                import difflib
                miss = len(want) + len(h) - 2 * sum(m_.size for m_ in difflib.SequenceMatcher(None, want, h).get_matching_blocks())
                tried.append((f, " ".join(h), miss))
                if best is None or miss < best[2]:
                    best = (a, f, miss)
                if miss == 0:
                    break
            a, f, miss = best
            ok = miss == 0
            sf.write("%s/%s.wav" % (VOICES, key), a.astype(np.float32), SR)
            meta[key] = round(len(a) / SR, 3); log[key] = {"who": who, "line": text, "speed": f, "heard_ok": ok, "tried": tried}
            os.makedirs("on3_voices/cache", exist_ok=True)
            sf.write(cp + ".wav", a.astype(np.float32), SR); json.dump(log[key], open(cp + ".json", "w"))
    json.dump(meta, open(VOICES + "/takes.json", "w"), indent=1)
    json.dump(log, open(VOICES + "/speech_check.json", "w"), indent=1)
    return meta


SEEN = ("CLIENT", "PAM", "REFEREE", "SOFIA", "DON")
NO_BUBBLE = ("Human approval required.",)                    # v16: the robot's own screen says it, in its view of him (the same words twice)
HOLD_N = ("4.3", "4.4a")  # v23 (Tomas, option 1): 4.3 waits until she has named the price: over 4.4 her line read as his;                                          # v7: a narration line that must end before the next shot (the robot speaks on its first frame)                      # their mouths are on the screen: the shot waits for the line
_ENV = {}


_VIS = {}


def _visemes(text):
    """The line's letters as mouth shapes, in order: a wide A, E with teeth, a round O, a small U, lips shut (M),
    the lip under the teeth (F), a part-open rest (C). A space is a short shut."""
    out = []
    for wd in text.lower().split():
        i = 0
        while i < len(wd):
            ch, two = wd[i], wd[i:i + 2]
            if two in ("th", "sh", "ch", "ng"):
                out.append("C"); i += 2; continue
            if two in ("oo", "ou", "ow"):
                out.append("O"); i += 2; continue
            if two in ("ee", "ea", "ai", "ay", "ie"):
                out.append("E"); i += 2; continue
            v = "A" if ch == "a" else "E" if ch in "ei" else "O" if ch == "o" else "U" if ch in "uw" else "M" if ch in "mbp" else "F" if ch in "fv" else "C" if ch.isalpha() else None
            if v and not (out and out[-1] == v and v in "CM"):
                out.append(v)
            i += 1
        out.append("M")
    return out[:-1] or ["M"]


def _mouth(key, tl, text=""):
    """v14: the mouth for a drawing of this take, on twos: the line's own shapes spread over its length, and shut where
    the take is silent (it was open by loudness alone: three shapes, whatever was said)."""
    if key not in _ENV:
        a, _ = sf.read("%s/%s.wav" % (VOICES, key)); n = SR // 12
        e = np.array([np.sqrt(np.mean(a[i:i + n] ** 2)) for i in range(0, len(a), n)]); _ENV[key] = (e / (e.max() + 1e-9), len(a) / SR)
        _VIS[key] = _visemes(text)
    e, ln = _ENV[key]
    i = int(tl * 12)
    if not (0 <= i < len(e)) or e[i] < 0.08:
        return None
    seq = _VIS[key]
    return seq[min(len(seq) - 1, int((int(tl * 12) / 12.0) / ln * len(seq)))]


def schedule(meta):
    """-> shots [(name, start, dur, fn, base dur)], lines [(start, end, who, text, key)], and what was held and by how much."""
    shots, lines, held = [], [], []
    T, prev_end = 0.0, 0.0
    for name, dur, fn in fm.FILM:
        need = dur
        for who, text, key, off in LINES.get(name, []):
            st = max(T + (max(off, LEAD) if who == "N" and name != "2.0" else off), prev_end + GAP)
            en = st + meta[key]
            lines.append((round(st, 3), round(en, 3), who, text, key))
            prev_end = en
            need = max(need, (en + 0.2 - T) if (who in SEEN or name in HOLD_N) else (st + min(meta[key], 0.5) - T))      # v3: a line whose speaker is not seen talking runs on over the next shot
        need = math.ceil(need * FPS - 1e-6) / FPS
        if need > dur + 1e-6:
            held.append((name, round(need - dur, 2)))
        shots.append((name, round(T, 3), need, fn, dur))
        T += need
    return shots, lines, held, T


def _fx(kind):
    t = lambda d: np.arange(int(d * SR)) / SR
    rng = np.random.default_rng(7)
    if kind == "punch":
        x = t(0.28); a = np.sin(2 * np.pi * (90 * np.exp(-x * 9) + 38) * x) * np.exp(-x * 14) * 0.9
        n = rng.standard_normal(len(x)) * np.exp(-x * 60) * 0.5
        return a + np.convolve(n, np.ones(24) / 24, "same")
    if kind == "stamp":
        x = t(0.20); return np.sin(2 * np.pi * 70 * x) * np.exp(-x * 22) * 0.7 + rng.standard_normal(len(x)) * np.exp(-x * 90) * 0.2
    if kind == "bell":
        x = t(1.6); return sum(g * np.sin(2 * np.pi * f * x) * np.exp(-x * d) for f, g, d in ((784, 0.5, 2.6), (1568, 0.3, 3.4), (2352, 0.18, 4.6), (3140, 0.1, 6.0))) * 0.55
    if kind == "click":
        x = t(0.05); return np.sin(2 * np.pi * 1400 * x) * np.exp(-x * 120) * 0.5 + rng.standard_normal(len(x)) * np.exp(-x * 300) * 0.3
    if kind == "snap":
        x = t(0.06); return rng.standard_normal(len(x)) * np.exp(-x * 110) * 0.45
    if kind == "pop":
        x = t(0.35); return np.convolve(rng.standard_normal(len(x)), np.ones(6) / 6, "same") * np.exp(-x * 16) * 0.45
    if kind == "chime":
        x = t(0.7); return (np.sin(2 * np.pi * 880 * x) * np.exp(-x * 5) + np.sin(2 * np.pi * 1318.5 * np.maximum(x - 0.16, 0)) * np.exp(-np.maximum(x - 0.16, 0) * 5) * (x > 0.16)) * 0.3
    if kind == "buzz":
        x = t(0.55); return np.sign(np.sin(2 * np.pi * 155 * x)) * (np.sin(2 * np.pi * 9 * x) > -0.2) * np.minimum(1, (0.55 - x) * 20) * 0.16
    raise KeyError(kind)


OUTSIDE = ("2.", "3.")                                       # the street and the alley: rain
RING = ("5.", "6.", "7.")                                    # the hall: a crowd
AWAKE = ("8.",)


def _noise(n, lo, hi, seed):
    rng = np.random.default_rng(seed); x = rng.standard_normal(n)
    X = np.fft.rfft(x); f = np.fft.rfftfreq(n, 1.0 / SR); X[(f < lo) | (f > hi)] = 0
    y = np.fft.irfft(X, n); return y / (np.max(np.abs(y)) + 1e-9)


def mix(shots, lines, total):
    """v5: scratch music and rooms under the lines. The first Noir's band (sound_on_jazz) from the bill to the white
    flash, ducked under every voice; rain on the street and in the alley, through the wall at the desk; a crowd's murmur
    in the hall; a quiet room when he is awake, and no music there. A scratch mix: the final one is iteration 4."""
    import sound_on_jazz as oj
    n = int(total * SR)
    start, zone = {}, np.zeros((4, n))                       # rain, through the wall, hall, room
    for name, st, dur, fn, base in shots:
        start.setdefault(name, st)
        i, j = int(st * SR), min(n, int((st + dur) * SR))
        z = 0 if name.startswith(OUTSIDE) else 2 if name.startswith(RING) else 3 if name.startswith(AWAKE) and name != "8.5" else 1 if name.startswith("4.") else None
        if z is not None:
            zone[z, i:j] = 1.0
    k = int(0.25 * SR); win = np.hanning(k) / np.hanning(k).sum()
    zone = np.array([np.convolve(z, win, "same") for z in zone])           # a quarter second across each change of place
    wake = start.get("8.1", total)
    voice = np.zeros(n + SR)
    for st, en, who, text, key in lines:
        a, sr = sf.read("%s/%s.wav" % (VOICES, key)); i = int(st * SR)
        voice[i:i + len(a)] += a
    voice = voice[:n]
    music = np.zeros(n + SR); oj.groove(music, 0.6, wake, level=0.85); music = music[:n]
    music[int(wake * SR):] = 0.0
    m0 = int((wake - 0.12) * SR); music[m0:int(wake * SR)] *= np.linspace(1, 0, int(wake * SR) - m0)   # cut off by the flash
    env = np.convolve((np.abs(voice) > 0.01).astype(float), np.ones(int(0.3 * SR)) / int(0.3 * SR), "same")
    rain = so.rain(total + 0.5)[:n]
    hall = _noise(n, 180, 900, 11) * (0.75 + 0.25 * np.sin(2 * np.pi * 0.23 * np.arange(n) / SR)) * 0.5
    room = _noise(n, 60, 400, 12) * 0.25
    fxb, fx = np.zeros(n + 3 * SR), []
    for kind, shot, off in FX:
        if shot not in start:
            continue
        a = _fx(kind); i = int((start[shot] + off) * SR); fx.append((kind, shot, round(start[shot] + off, 3)))
        fxb[i:i + len(a)] += a
    out = (voice * 1.0 + music * (0.24 - 0.14 * env) + rain * (0.50 * zone[0] + 0.10 * zone[1]) + hall * 0.10 * zone[2] * (1 - 0.4 * env)
           + room * 0.05 * zone[3] + fxb[:n] * 0.55)
    return np.tanh(out * 1.6) / 1.6, fx


MOM_AT = {"4.3": (322, 338), "5.4": (268, 562), "7.4": (268, 562),       # her cheek, level with her mouth, where she is on the screen
          "2.2": (330, 600), "2.4": (536, 420), "4.4a": (318, 880, -1)}   # v25: her sleeve, under the ticket she pushes       # out of sight: the tail goes to the car, or off the edge she is at
CLIENT_AT = {"4.3": (96, 302)}
SOFIA_AT = {"2.6": (412, 462, 1), "5.1a": (440, 630)}        # (x, y) or (x, y, side): which side of the tip the bubble sits                              # he speaks with his back to us: the tail goes to his hood


# v26 (Tomas: "small meaningful pauses, e.g. after Word is"): the voice already pauses there; the card now pauses with it:
# the first phrase alone until the voice goes on (seconds into the take).
SPLIT = {"n1": ("Word is,", 1.20), "n2b": ("My manager.", 1.66), "n8": ("I don't break.", 1.52), "n12": ("Ten garages.", 1.73)}


def _card(c, text, y0=100):
    """Narration: typewriter on cream cards with a black edge, at the top under the bar, two rows at most (Office Noir 2)."""
    c.select_font_face("Special Elite", 0, 0); c.set_font_size(30)
    rows, line = [], ""
    for wd in text.split():
        trial = (line + " " + wd).strip()
        if c.text_extents(trial).x_advance > 522 - 18 - 40 and line:
            rows.append(line); line = wd
        else:
            line = trial
    rows.append(line)
    assert len(rows) <= 2, rows
    y = y0
    for ln in rows:
        w = c.text_extents(ln).x_advance + 24
        c.set_source_rgba(0, 0, 0, 0.45); c.rectangle(22, y + 4, w, 42); c.fill()
        c.set_source_rgb(0.93, 0.90, 0.82); c.rectangle(18, y, w, 42); c.fill()
        c.set_source_rgb(0.06, 0.06, 0.07); c.set_line_width(2.6); c.rectangle(18, y, w, 42); c.stroke()
        c.move_to(30, y + 30); c.show_text(ln); y += 48
    return y


_BOX = {}                                                    # v22: (line, shot) -> where its bubble was put on its first drawing


def _bubble(c, text, tip, top=100, avoid=(), key=None):
    """A spoken line: a white bubble, black edge; its tail to the speaker's cheek, level with the mouth. tip None: the
    speaker is out of the frame: no tail, at the top right. v7: avoid: boxes (x0, y0, x1, y1) of every head on the
    screen; the bubble takes the first place, nearest the speaker, that covers none of them and stays in the safe area."""
    c.select_font_face("Inter", 0, 1); c.set_font_size(24)

    def wrap(width):
        rows, line = [], ""
        for wd in text.split():
            trial = (line + " " + wd).strip()
            if c.text_extents(trial).x_advance > width and line:
                rows.append(line); line = wd
            else:
                line = trial
        rows.append(line)
        return rows, max(c.text_extents(r_).x_advance for r_ in rows) + 36, 30 * len(rows) + 26
    rows, w, h = wrap(270)
    if tip is None and avoid:                                # v19: a bigger head on the screen: a narrower bubble beside it before one across it
        for width in (270, 180, 140):
            rows, w, h = wrap(width)
            if any(all(bx + w < x0 or bx > x1 or by + h < y0 or by > y1 for x0, y0, x1, y1 in avoid) for bx, by in ((522 - w - 6, top + 10), (24, top + 10), (522 - w - 6, top + 90), (24, top + 90))):
                break
        else:
            rows, w, h = wrap(270)

    def clear(bx, by):
        return all(bx + w < x0 or bx > x1 or by + h < y0 or by > y1 for x0, y0, x1, y1 in avoid)
    if key in _BOX:                                          # v22 (Tomas: "the bubbles jump when they move; it is hard to read"): the bubble stays where it
        rows, w, h, bx, by, side = _BOX[key]                 # was first put for this line in this shot; only its tail follows the mouth
    elif tip is None:
        cands = [(522 - w - 6, top + 10), (24, top + 10), (522 - w - 6, top + 90), (24, top + 90)]
        bx, by = next((p for p in cands if clear(*p)), cands[0]); side = 1
    else:
        side0 = tip[2] if len(tip) > 2 else (1 if tip[0] < 270 else -1)
        cands = []
        for up in (130, 180, 240, 90, 300):
            for side in (side0, -side0):
                for off in (46, 110, -40):
                    bx = min(522 - w, max(18, tip[0] + side * off - (0 if side > 0 else w)))
                    cands.append((bx, max(top, tip[1] - up - h), side))
        bx, by, side = next((p for p in cands if clear(p[0], p[1]) and p[1] + h < tip[1] - 30), cands[0])
    if key is not None:
        _BOX.setdefault(key, (rows, w, h, bx, by, side))
    if tip is not None:
        tx = min(bx + w - 26, max(bx + 26, tip[0] + side * 30))
        c.new_path(); c.move_to(tx - 13, by + h - 4); c.line_to(tip[0], tip[1]); c.line_to(tx + 13, by + h - 4); c.close_path()
        c.set_source_rgb(1, 1, 1); c.fill_preserve(); c.set_source_rgb(0.06, 0.06, 0.07); c.set_line_width(3); c.set_line_join(1); c.stroke()
    r_ = 16
    def box():
        c.new_path(); c.arc(bx + r_, by + r_, r_, math.pi, 1.5 * math.pi); c.arc(bx + w - r_, by + r_, r_, 1.5 * math.pi, 0)
        c.arc(bx + w - r_, by + h - r_, r_, 0, 0.5 * math.pi); c.arc(bx + r_, by + h - r_, r_, 0.5 * math.pi, math.pi); c.close_path()
    box(); c.set_source_rgb(0.06, 0.06, 0.07); c.set_line_width(6); c.stroke()
    box(); c.set_source_rgb(1, 1, 1); c.fill()
    if tip is not None:                                      # the tail's root, open into the bubble
        c.new_path(); c.move_to(tx - 11.5, by + h - 5); c.line_to(tx + 11.5, by + h - 5); c.line_to(tx + 10.5, by + h + 2.5); c.line_to(tx - 10.5, by + h + 2.5); c.close_path()
        c.set_source_rgb(1, 1, 1); c.fill()
    c.set_source_rgb(0.06, 0.06, 0.07)
    for i, r2 in enumerate(rows):
        c.move_to(bx + 18, by + 36 + 30 * i); c.show_text(r2)


def _heads(shot):
    """Every head on this drawing, as a box on the finished frame: the tracked figures and Mom where she sits."""
    heads, zoom = fm.mo.CLOCK.get("heads") or {}, fm.mo.CLOCK.get("zoom")
    out = []
    pts = [(hx, hy, 62 * sc) for hx, hy, sc in heads.values()]
    if shot in MOM_AT and MOM_AT[shot][0] < 530 and shot not in ("2.2",):
        pts.append((MOM_AT[shot][0] - 20, MOM_AT[shot][1] - 40, 70))
    for hx, hy, r in pts:
        if zoom:
            (fx_, fy_), z = zoom
            hx, hy, r = fx_ + (hx - fx_) * z, fy_ + (hy - fy_) * z, r * z
        out.append((hx - r, hy - r * 1.25, hx + r, hy + r * 0.9))
    return out


def _tip(who, shot):
    heads, zoom = fm.mo.CLOCK.get("heads") or {}, fm.mo.CLOCK.get("zoom")
    if who in heads and not (who == "CLIENT" and shot in CLIENT_AT) and not (who == "SOFIA" and shot == "5.1a" and False):
        hx, hy, sc = heads[who]
        side = 1 if hx < 270 else -1
        p = (hx + side * 30 * sc, hy + 30 * sc)
    else:
        p = {"MOM": MOM_AT, "CLIENT": CLIENT_AT, "SOFIA": SOFIA_AT}.get(who, {}).get(shot)
        if p is None:
            return None
    if zoom:
        (fx_, fy_), z = zoom
        p = (fx_ + (p[0] - fx_) * z, fy_ + (p[1] - fy_) * z) + tuple(p[2:])
    return p


def _text(surf, shot, now):
    """now: [(who, text)] being spoken on this drawing. Cards for the narration, bubbles for the spoken lines; on the
    screen only while the line is heard."""
    if not now:
        return surf
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(s)
    c.set_source_surface(surf, 0, 0); c.paint()
    top = 100
    for who, text in now:
        if who == "N":
            top = _card(c, text) + 6
    for who, text in now:
        if who != "N" and text not in NO_BUBBLE:
            _bubble(c, text, _tip(who, shot), top, _heads(shot), key=(text, shot))
    return s


def build(out):
    meta = takes()
    shots, lines, held, total = schedule(meta)
    FN, SH = {}, []
    for i, (name, st, dur, fn, base) in enumerate(shots):
        key = "%02d_%s" % (i, name)

        def f(t, fn=fn, base=base, st=st, name=name):
            T = st + t
            fm.mo.CLOCK["T_ext"] = T                                    # the clock runs on through a held drawing: they breathe
            fm.mo.CLOCK["say"] = {who: _mouth(key_, T - a, text) for a, b_, who, text, key_ in lines if a <= T < b_ and who in SEEN}
            s = fn(min(t, base - 1.0 / FPS))
            return _text(s, name, [(who, SPLIT[k_][0] if k_ in SPLIT and T - a < SPLIT[k_][1] else text) for a, b_, who, text, k_ in lines if a - 0.05 <= T < b_ + 0.15])
        FN[key] = f; SH.append((key, dur))
    audio, fx = mix(shots, lines, total)
    d = os.path.dirname(os.path.abspath(out))
    wav, silent = os.path.join(d, "_on3_animatic.wav"), os.path.join(d, "_on3_animatic_silent.mp4")
    sf.write(wav, audio.astype(np.float32), SR)
    rr.SHOTS, rr.FN = tuple(SH), FN
    rr.render(silent)
    ln = "loudnorm=I=-15:TP=-1.5:LRA=11"                         # v5: two passes: measure, then set, so the level lands on -15
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", wav, "-af", ln + ":print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
    j = json.loads(r[r.rindex("{"):r.rindex("}") + 1])
    ln2 = ln + ":measured_I=%s:measured_TP=%s:measured_LRA=%s:measured_thresh=%s:offset=%s:linear=true" % (
        j["input_i"], j["input_tp"], j["input_lra"], j["input_thresh"], j["target_offset"])
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                           "-af", ln2, "-ar", "48000", "-c:a", "aac", "-b:a", "160k", out])
    os.remove(silent); os.remove(wav)
    json.dump({"length": round(total, 3), "shots": [(n, s_, round(d_, 3), round(b_, 3)) for n, s_, d_, _, b_ in shots],
               "lines": lines, "effects": fx, "held": held}, open("on3_animatic_timing_%s.json" % V, "w"), indent=1)
    return total, held, lines


if __name__ == "__main__":
    total, held, lines = build(sys.argv[1] if len(sys.argv) > 1 else "../office-noir-3/on3_animatic_%s.mp4" % V)
    print("%.1f s" % total); print("held:", held)
    for l in lines:
        print(l[:4])
