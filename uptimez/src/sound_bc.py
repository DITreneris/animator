"""Voices and sound for "The Best Candidate" (script v5, storyboard v3).
Voices (Kokoro, the series cast): Don am_onyx, Sofia af_bella, Pam bf_emma, the robot voice B (am_echo, robotized),
Mom voice F from Office Noir (bf_alice with 30 % bm_lewis, aged): soft and unhurried until "DONNIE!", which is shouted.
New in this film, cast without auditions (the person judges them in the rough animation):
  the small one   am_eric, two semitones up: the highest and quickest of the male voices, bright and eager;
  the nice macho  am_michael, two semitones down: warm and unhurried, and well above Don's 87 Hz so the two never blur.
  python3 sound_bc.py takes   -> bc_voices/<key>.wav and bc_voices/takes.json (length, speaker, mouth shapes at 12 fps)
  python3 sound_bc.py mix     -> bc_mix.wav from bc_timing.json (written by bc_anim.py timing)
The mouth shapes use the series' method (ss_visemes.py): the line's phonemes spread over its voiced span, vowels
longer, every m/b/p and f/v kept."""
import os
import sys
import json
import numpy as np
import soundfile as sf
import sound_iwry as si
import sound_xmas as sx
import sound_on as so

SR = 48000
OUT = "bc_voices"
rng = np.random.default_rng(41)
MAP = {"a": "A", "æ": "A", "ɐ": "A", "ɑ": "A", "ʌ": "A", "ə": "C", "ɛ": "E", "e": "E", "ɪ": "E", "i": "E",
       "ɜ": "E", "o": "O", "ɔ": "O", "u": "U", "ʊ": "U", "w": "U", "ɹ": "U", "p": "M", "b": "M", "m": "M",
       "f": "F", "v": "F"}
VOWELS = set("aæɐɑʌəɛeɪiɜoɔuʊ")
SKIP = set("ˈˌ.?!,;:—-… ")


def norm(a, g=0.11):
    return a / np.sqrt(np.mean(a ** 2)) * g


def don(txt, speed=1.0, g=0.11):
    return so.dry(txt, si.DON, speed, g=g)


def sofia(txt, speed=1.0, g=0.11):
    return so.dry(txt, si.SOF, speed, g=g)


def small(txt, speed=1.0):
    return norm(so.pitch(so.dry(txt, "am_eric", speed), 2.0))


def macho(txt, speed=1.06):
    return norm(so.pitch(so.dry(txt, "am_michael", speed), -2.0))


def mom_take(txt, speed):
    fem, male, share, sp, lang, _ = so.MOMS2["F"]
    v = so.blend(fem, male, share)
    a = np.asarray(si.K.create(txt, voice=v, speed=sp * speed, lang=lang)[0], dtype=np.float64)
    a = np.interp(np.linspace(0, len(a) - 1, int(len(a) * SR / 24000)), np.arange(len(a)), a)
    idx = np.where(np.abs(a) > 0.01)[0]
    return a[max(0, idx[0] - 600):idx[-1] + 2400]


def mom(txt, speed=1.0, semis=0.0, g=0.11):
    a = so.age(mom_take(txt, speed))
    return norm(so.pitch(a, semis) if semis else a, g)


def mom_shout(txt):
    return so.shout_hard(so.age(mom_take(txt, 0.9)), drive=5.5, strain=1.2)


def robot(txt, speed=1.12):
    """Voice B, a little quicker than in the earlier films: it reads rulings, it does not converse."""
    v, sp, semis, ring, comb, _ = si.ROBOTS["B"]
    return si.robotize(si.say(txt, v, sp * speed), semis, ring, comb)


def phones(text):
    out = []
    for ch in si.K.tokenizer.phonemize(text, "en-us"):
        if ch == "ː" and out:
            out[-1][1] += 1.0
        elif ch not in SKIP:
            out.append([MAP.get(ch, "C"), 2.2 if ch in VOWELS else (1.3 if MAP.get(ch) == "M" else 1.0)])
    return out


def weight(text):
    return sum(w for _, w in phones(text))


def cut_at(a, said, whole):
    """Cut a take off after the part that is `said` of the `whole` sentence, by phoneme weight over the voiced span."""
    e = np.sqrt(si.lp(a ** 2, int(0.02 * SR)))
    v = np.where(e > 0.12 * e.max())[0]
    keep = (v[0] + (v[-1] - v[0]) * weight(said) / weight(whole)) / SR
    return so.cut_off(a, keep)


# key: (who, the words as heard, the words for the mouth, how to make it)
LINES = [
    ("first", "DON", "First candidate.", lambda: don("First candidate.")),
    ("three", "SOF", "Three degrees?", lambda: sofia("Three degrees?")),
    ("half", "SMALL", "And a half.", lambda: small("And a half.")),
    ("q1", "DON", "What if I made a mistake?", lambda: don("What if I made a mistake?", 0.95)),
    ("data", "SMALL", "I'd show you the data.", lambda: small("I'd show you the data.")),
    ("short", "DON", "Too short.", lambda: don("Too short.")),
    ("r_height", "ROB", "Height is not protected. Proceed.", lambda: robot("Height is not protected. Proceed.")),
    ("dropped", "MACHO", "You dropped this.", lambda: macho("You dropped this.")),
    ("thanks", "SOF", "Thank you.", lambda: sofia("Thank you.", 0.92, 0.095)),
    ("q2", "DON", "And you. What if I made a mistake?", lambda: don("And you. What if I made a mistake?", 1.06, 0.125)),
    ("okay", "MACHO", "Everybody makes mistakes. It's okay.", lambda: macho("Everybody makes mistakes. It's okay.")),
    ("true", "SOF", "That's so true.", lambda: sofia("That's so true.", 0.95)),
    ("distracting", "DON", "Too distracting.", lambda: don("Too distracting.")),
    ("whom", "SOF", "For whom?", lambda: sofia("For whom?", 0.95)),
    ("r_looks", "ROB", "Attractiveness is not protected. Proceed.",
     lambda: robot("Attractiveness is not protected. Proceed.")),
    ("worries", "MACHO", "No worries.", lambda: macho("No worries.")),
    ("morning", "MOM", "Good morning, everyone.", lambda: mom("Good morning, everyone.")),
    ("experience", "ROB", "Experience?", lambda: robot("Experience?")),
    ("forty", "MOM", "Forty years. One very difficult client.", lambda: mom("Forty years. One very difficult client.")),
    ("five", "SOF", "Where do you see yourself in five",
     lambda: cut_at(sofia("Where do you see yourself in five years?"), "Where do you see yourself in five",
                    "Where do you see yourself in five years?")),
    ("r_ageism", "ROB", "Ageism detected.", lambda: robot("Ageism detected.")),
    ("family", "PAM", "Any family in the company?", lambda: norm(sx.pam_line("Any family in the company?", "A"))),
    ("r_family", "ROB", "Family status is protected. Withdrawn.",
     lambda: robot("Family status is protected. Withdrawn.")),
    ("q3", "DON", "What if I made a mistake?", lambda: don("What if I... made a mistake?", 0.88, 0.07)),
    ("apologize", "MOM", "I'd make you apologize.", lambda: mom("I'd make you apologize.", 0.86, -1.0, 0.12)),
    ("sorry", "DON", "Sorry.", lambda: don("Sorry.", 1.08)),
    ("sorry2", "DON", "Sorry.", lambda: don("Sorry.", 0.95, 0.10)),
    ("goodboy", "MOM", "Good boy.", lambda: mom("Good boy.", 0.92)),
    ("verdict", "ROB", "She made him answer the client. Hired.",
     lambda: robot("She made him answer the client. Hired.")),
    ("approved", "DON", "Approved.", lambda: don("Approved.", 0.9, 0.06)),
    ("welcome", "DON", "Welcome ab", lambda: cut_at(don("Welcome aboard."), "Welcome ab", "Welcome aboard")),
    ("donnie", "MOM", "Donnie! Your vest!", lambda: mom_shout("Donnie! Your vest!")),
    ("father", "MOM", "Donnie. Father is parking.", lambda: mom("Donnie. Father is parking.")),
    ("why", "DON", "Why?", lambda: don("Why?")),
    ("job", "MOM", "He's applying for your job.", lambda: mom("He's applying for your job.", 0.95)),
]


def visemes(a, text):
    """Mouth codes on a 12 fps grid from the take's first sample: "" before and after the voiced span."""
    e = np.sqrt(si.lp(a ** 2, int(0.02 * SR)))
    v = np.where(e > 0.12 * e.max())[0]
    ts, te = v[0] / SR, v[-1] / SR
    s0, s1 = int(round(ts * 12)), max(int(round(te * 12)), int(round(ts * 12)) + 1)
    ph = phones(text)
    total = sum(w for _, w in ph)
    bounds, acc = [], 0.0
    for code, w in ph:
        bounds.append((acc / total, (acc + w) / total, code)); acc += w
    n = s1 - s0
    seq = [next(c for lo, hi, c in bounds if lo <= (i + 0.5) / n < hi or hi == 1.0) for i in range(n)]
    for lo, hi, code in bounds:
        if code in ("M", "F"):
            i = min(n - 1, int((lo + hi) / 2 * n))
            if code not in seq[max(0, i - 1):i + 2]:
                seq[i] = code
    return [""] * s0 + seq


def f0(a):
    out, n = [], int(0.04 * SR)
    for i in range(0, len(a) - n, n // 2):
        x = a[i:i + n] * np.hanning(n)
        if np.sqrt(np.mean(x ** 2)) < 0.03:
            continue
        r = np.correlate(x, x, "full")[n - 1:]
        lo, hi = int(SR / 320), int(SR / 60)
        j = lo + int(np.argmax(r[lo:hi]))
        if r[j] > 0.35 * r[0]:
            out.append(SR / j)
    return float(np.median(out)) if out else 0.0


def gaps(a):
    """Silences of 60 ms or more inside the line (start, end in seconds): where a cut can fall between sentences."""
    e = np.sqrt(si.lp(a ** 2, int(0.02 * SR)))
    q = e < 0.08 * e.max()
    v = np.where(~q)[0]
    out, i = [], v[0]
    while i < v[-1]:
        if q[i]:
            j = i
            while j < v[-1] and q[j]:
                j += 1
            if (j - i) / SR >= 0.06:
                out.append([round(i / SR, 3), round(j / SR, 3)])
            i = j
        else:
            i += 1
    return out


def takes(only=None):
    os.makedirs(OUT, exist_ok=True)
    p = f"{OUT}/takes.json"
    meta = json.load(open(p)) if only and os.path.exists(p) else {}
    for key, who, text, make in LINES:
        if only and key not in only:
            a = sf.read(f"{OUT}/{key}.wav")[0].astype(np.float64)
            meta[key]["gaps"] = gaps(a)
            continue
        a = np.asarray(make(), dtype=np.float64)
        sf.write(f"{OUT}/{key}.wav", a.astype(np.float32), SR)
        meta[key] = {"who": who, "text": text, "len": round(len(a) / SR, 3), "vis": visemes(a, text),
                     "f0": round(f0(a)), "peak": round(float(np.abs(a).max()), 3), "gaps": gaps(a),
                     "clip": round(float(np.mean(np.abs(a) > 0.98)), 4)}
        print(f"{key:12s} {who:6s} {meta[key]['len']:5.2f} s  f0 {meta[key]['f0']:4d} Hz  peak {meta[key]['peak']:.2f}  "
              f"{''.join(c or '-' for c in meta[key]['vis'])}")
    json.dump(meta, open(f"{OUT}/takes.json", "w"), indent=1)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "takes":
        takes(set(sys.argv[2:]) or None)
    elif len(sys.argv) > 1 and sys.argv[1] == "mix":
        import sound_bc_mix
        sound_bc_mix.main()
