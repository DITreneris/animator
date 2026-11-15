"""Mouth shapes (visemes) for "How Sofía Survived Day One", from the phonemes of each line.
Each line's phonemes (Kokoro's phonemizer) are spread over the voiced part of its take, found from the
per-frame loudness in day1_lips.json; vowels get more time than consonants and every m/b/p and f/v keeps
at least one drawing, so the lips visibly close on "Pam?" and "Perfect.". Sampled on the film's 12 fps
drawing grid. Writes day1_visemes.json: {"DON"|"SOF"|"ROB": [code per 1/12 s]}.
Codes: "" rest (the face's own mouth), M closed lips, A open, E wide, O round, U small round,
F lip under teeth, C small open with teeth."""
import json
import os
from kokoro_onnx import Kokoro

KD = os.environ.get("KOKORO_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "models"))
K = Kokoro(os.path.join(KD, "kokoro-v1.0.int8.onnx"), os.path.join(KD, "voices-v1.0.bin"))
LIPS = json.load(open("day1_lips.json"))
STEPS = 25 * 12
LINES = [("DON", "I approve everything.", 3.35, 5.5), ("DON", "Trained it myself.", 5.75, 7.4),
         ("DON", "Pam?", 8.05, 9.0), ("SOF", "Can you help me?", 12.55, 14.3), ("ROB", "Pam?", 15.0, 16.2),
         ("DON", "Perfect.", 16.95, 17.8), ("ROB", "Can you help me?", 20.9, 21.8), ("SOF", "Pam?", 22.05, 22.8)]
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
for who, text, t0, slot in LINES:
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
json.dump(vis, open("day1_visemes.json", "w"))
