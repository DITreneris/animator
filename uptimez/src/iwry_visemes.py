"""Mouth shapes (visemes) for "I Will Replace You", from the phonemes of each line (the Day One method,
day1_visemes.py). Lines and loudness come from the final takes in the mix (iwry_lips_w2_d2.json).
Each line's phonemes (Kokoro's phonemizer) are spread over the voiced part of its take, found from the
per-frame loudness in day1_lips.json; vowels get more time than consonants and every m/b/p and f/v keeps
at least one drawing, so the lips visibly close on "Pam?" and "Perfect.". Sampled on the film's 12 fps
drawing grid. Writes iwry_visemes.json: {"DON"|"SOF"|"ROB": [code per 1/12 s]}.
Codes: "" rest (the face's own mouth), M closed lips, A open, E wide, O round, U small round,
F lip under teeth, C small open with teeth."""
import json
from kokoro_onnx import Kokoro

K = Kokoro("/home/claude/models/kokoro-v1.0.int8.onnx", "/home/claude/models/voices-v1.0.bin")
LIPS = json.load(open("iwry_lips_w2_d2.json"))
STEPS = 25 * 12
MAP = {"a": "A", "æ": "A", "ɐ": "A", "ɑ": "A", "ʌ": "A", "ə": "C", "ɛ": "E", "e": "E", "ɪ": "E", "i": "E",
       "ɜ": "E", "o": "O", "ɔ": "O", "u": "U", "ʊ": "U", "w": "U", "ɹ": "U", "p": "M", "b": "M", "m": "M",
       "f": "F", "v": "F"}
VOWELS = set("aæɐɑʌəɛeɪiɜoɔuʊ")
SKIP = set("ˈˌ.?!, ")


def phones(text):
    out = []
    for ch in K.tokenizer.phonemize(text, "en-us"):
        if ch == "ː" and out:
            out[-1][1] += 1.0                           # long vowel: more time
        elif ch not in SKIP:
            out.append([MAP.get(ch, "C"), 2.2 if ch in VOWELS else (1.3 if MAP.get(ch) == "M" else 1.0)])
    return out


vis = {w: [""] * STEPS for w in ("DON", "SOF", "ROB")}
for who, text, t0, slot in LIPS["lines"]:
    e = LIPS[who]
    f0, f1 = int(round(t0 * 30)), min(int(round(slot * 30)), len(e))
    voiced = [f for f in range(f0, f1) if e[f] > 0.12]
    ts, te = voiced[0] / 30, (voiced[-1] + 1) / 30
    s0, s1 = int(round(ts * 12)), max(int(round(te * 12)), int(round(ts * 12)) + 1)
    ph = phones(text)
    total = sum(w for _, w in ph)
    bounds, acc = [], 0.0
    for code, w in ph:
        bounds.append((acc / total, (acc + w) / total, code))
        acc += w
    n = s1 - s0
    seq = []
    for i in range(n):
        x = (i + 0.5) / n
        seq.append(next(c for a, b, c in bounds if a <= x < b or b == 1.0))
    # every closure (m/b/p) and lip-under-teeth (f/v) keeps a drawing: put a missing one on its nearest step
    for a, b, code in bounds:
        if code in ("M", "F"):
            i = min(n - 1, int((a + b) / 2 * n))
            if code not in seq[max(0, i - 1):i + 2]:
                seq[i] = code
    for i, code in enumerate(seq):
        vis[who][s0 + i] = code
    print(f"{who} {text:24s} {ts:5.2f}-{te:5.2f} {''.join(c for c, _ in ph):18s} -> {''.join(seq)}")
json.dump(vis, open("iwry_visemes.json", "w"))
