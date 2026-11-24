"""OFFICE NOIR 4: the moving rough, v2 (24 Nov; v1 pinned as on4_rough_v1.py). Tomas's picks: 3.3-3.5 in the side camera
(on4_motion T6), 2 s moved from the stage to the office (on4_scenes DUR), every line voiced (seven new takes with the
series' voices, checked by the recognizer), effects, and the Office Noir band (sound_on_jazz.groove) cut by the story's
silences (lesson 107): dead on the bump, dead on "Well?"; no music awake. Voices dry. No bubbles yet.

  python3 on4_motion.py && python3 on4_rough.py  ->  ../office-noir-4/on4_rough_v2.mp4 (540x960, 24 fps, AAC, -15 LUFS)"""
import json
import os
import shutil
import subprocess
import numpy as np
import soundfile as sf
import on4_scenes as sc
import on4_voices as vo

FPS = 12
SR = 48000
MOT = {("1.1", "1.2"): ("T1", 0, 39), ("2.2", "2.3"): ("T2", 0, None), ("2.4",): ("T7", 0, None), ("3.6",): ("T8", 0, None), ("6.0",): ("T9", 0, None), ("6.05",): ("T10", 0, None), ("6.07",): ("T11", 0, None), ("3.1", "3.2"): ("T3", 0, None),
       ("3.3", "3.3b", "3.4", "3.5"): ("T6", 0, None), ("6.3", "6.6"): ("T4", 0, -8), ("8.1", "8.2"): ("T5", 0, -7)}
OUT = os.path.join(sc.OUT, "on4_rough_v13.mp4")
NEW = {   # key: (shot, seconds into the shot, who, text)
    "c1": ("2.2", 2.1, "CLIENT", "Mine until it's done."),
    "d1": ("3.1", 1.5, "DON", "Traffic flows."),
    "d2": ("3.3", 1.9, "DON", "Not a scratch."),
    "f1": ("3.4", 1.0, "FATHER", "For the boys."),
    "p1": ("4.1", 0.9, "PAM", "There you are."),
    "p2": ("5.3", 1.75, "PAM", "Easy."),
    "p3": ("6.3", 0.9, "PAM", "Well?"),
}


MOVE7 = {"n2": ("2.1", 0.1), "n1": ("1.3", 0.3)}            # n1 earlier (24 Nov, Tomas: longer pauses between the narrator's sentences)                                # v7: "I know where to see..." over the spying (2.1-2.2); 2.4 gets its own two lines
NARR = {   # v4 (Tomas: the pauses are too long, the narrator is missing): two more of her boasts over the long gaps
    "n4": ("1.4", 0.3, "Nobody follows me."),              # as the two shadows come up behind her
    "n5": ("5.1", -0.45, "Nobody sees me coming."),          # as she walks through the club and nobody looks
    "n6": ("2.4", 0.7, "I know how to climb."),            # v7 (Tomas): up the ladder; she goes over the rail on its heels
    "n7": ("2.4", 32 / 12.0 + 0.75, "I know how to fall."),   # out of the bin, the peel on her ear
}


def narr_takes(kind):
    """the narrator's new lines, made as takes_v1's were (on4_voices.take: falling pitch, the noir chain, the recognizer)"""
    d = os.path.join(vo.OUT, "takes_v3"); os.makedirs(d, exist_ok=True)
    logp = os.path.join(d, "takes.json")
    log = json.load(open(logp)) if os.path.exists(logp) else {}
    for key, (shot, lead, txt) in NARR.items():
        p = os.path.join(d, key + ".wav")
        if os.path.exists(p) and key in log:
            continue
        vo.LINES[key] = (shot, "PAM_N", [(txt, 0)])
        a, m = vo.take(key, kind)
        sf.write(p, np.asarray(a, dtype=np.float32), vo.SR); log[key] = m
        print("take", key, m["ok"], m["asr"][0], m["len"])
    json.dump(log, open(logp, "w"), indent=1)
    return d


def new_takes():
    """the seven lines, cached in on4_voices/takes_v2 with what the recognizer heard"""
    import sound_on as so
    import sound_fs as sfs
    import dh_voices as dv
    d = os.path.join(vo.OUT, "takes_v2"); os.makedirs(d, exist_ok=True)
    logp = os.path.join(d, "takes.json")
    log = json.load(open(logp)) if os.path.exists(logp) else {}
    for key, (shot, lead, who, txt) in NEW.items():
        p = os.path.join(d, key + ".wav")
        if os.path.exists(p) and key in log:
            continue
        if who == "DON":
            a = so.dry(txt, "am_onyx", 1.0)
        elif who == "CLIENT":
            a = so.pitch(so.dry(txt, "am_fenrir", 1.0), -4.0)
        elif who == "FATHER":
            v = dv.FATHER[dv.FATHER_VOICE][0]       # Father voice B, but 0.8 speed and -1.5 semitones: at -3 a three-word line is not recognized
            a = so.pitch(so.dry(txt.rstrip(".") + "...", so.blend(*v), 0.8), -1.5)
        else:
            a = so.dry(txt, vo.PAM_AWAKE[0], vo.PAM_AWAKE[2], vo.PAM_AWAKE[1])
        a = np.asarray(a, dtype=np.float64); a = a / (np.sqrt(np.mean(a ** 2)) + 1e-9) * 0.11
        h = vo.heard3(a); want = " ".join(sfs._words(txt))
        log[key] = dict(shot=shot, who=who, text=txt, asr=h, ok=sum(1 for x in h if sfs._match(x, want)), len=round(len(a) / vo.SR, 2))
        sf.write(p, a.astype(np.float32), vo.SR)
        print("take", key, log[key]["ok"], h[0])
    json.dump(log, open(logp, "w"), indent=1)
    return d, log


SCENE3 = [False]                                            # (24 Nov, Tomas: "the music goes and it is dreary and silent, why?") the crossing after the bump: a short silence, then the bass alone; the engine idling, the night, the glove's squeak, each bill, the shadows' steps, his whistle; the bump as a tap and a thud (on4_motion.CRASH)
RETAKE = {}                                                 # key -> wav: a later take of a line of NEW (on4_film sets it)
STOP_GAP = 0.75                                             # (24 Nov, Tomas) where a speaker puts a full stop inside a take: at least this much silence


def stops(a, text):
    """a take with more than one sentence: the silence at each full stop widened to STOP_GAP (the longest quiet stretches
    inside the take are the stops)"""
    n_ = sum(text.count(ch) for ch in ".?!") - 1
    if n_ < 1:
        return a
    w = int(0.02 * SR); env = np.sqrt(np.convolve(a ** 2, np.ones(w) / w, "same"))
    quiet = env < 0.06 * env.max()
    runs = []; j = 0; L = len(a)
    while j < L:
        if quiet[j]:
            k_ = j
            while k_ < L and quiet[k_]:
                k_ += 1
            if j > 0.15 * SR and k_ < L - 0.15 * SR:
                runs.append((k_ - j, j, k_))
            j = k_
        else:
            j += 1
    out = a
    for ln, j0, j1 in sorted(sorted(runs, reverse=True)[:n_], key=lambda r_: -r_[1]):
        add = int(STOP_GAP * SR) - ln
        if add > 0:
            mid = (j0 + j1) // 2
            out = np.concatenate([out[:mid], np.zeros(add), out[mid:]])
    return out


def load(p):
    a, sr = sf.read(p)
    if a.ndim > 1:
        a = a.mean(1)
    if sr != SR:
        a = np.interp(np.arange(0, len(a), sr / SR), np.arange(len(a)), a)
    return a.astype(np.float64)


def sound(tm, d, total):
    import sound_on as so
    import sound_on_jazz as jz
    import sound_iwry as iw
    n = int((total + 0.2) * SR)
    def put(buf, a, t, g=1.0):
        a = np.asarray(a, dtype=np.float64); j = int(t * SR)
        if j >= len(buf):
            return
        a = a[:len(buf) - j]; buf[j:j + len(a)] += a * g
    def rs(a, sr):
        return a if sr == SR else np.interp(np.arange(0, len(a), sr / SR), np.arange(len(a)), a)
    st_ = lambda s: tm[s]["start"]
    voice = np.zeros(n); fx = np.zeros(n); mus = np.zeros(n)
    marks = []
    for key, ln in d["lines"].items():
        t = st_(MOVE7[key][0]) + MOVE7[key][1] if key in MOVE7 else st_(ln["shot"]) + vo.LEAD.get(ln["shot"], 0.3)
        put(voice, stops(load(os.path.join(vo.OUT, "takes_v1", key + ".wav")), " ".join(p_[0] for p_ in vo.LINES[key][2])), t); marks.append((key, round(t, 2)))
    d2, _ = new_takes()
    for key, (shot, lead, who, txt) in NEW.items():
        t = st_(shot) + lead
        put(voice, load(RETAKE.get(key, os.path.join(d2, key + ".wav"))), t); marks.append((key, round(t, 2)))
    d3 = narr_takes(d.get("narration", "A"))
    for key, (shot, lead, txt) in NARR.items():
        t = st_(shot) + lead
        put(voice, load(os.path.join(d3, key + ".wav")), t); marks.append((key, round(t, 2)))
    # the office (v4): its own sounds instead of words. Room tone, the machine, her steps, paper, the head going down
    import sound_day1 as dd
    import sound_xmas as sx
    rng = np.random.default_rng(7)
    o0, o1 = st_("7.1"), st_("8.2")
    L = int((o1 - o0) * SR); tt_ = np.arange(L) / SR
    k = np.ones(600) / 600
    tone = np.convolve(rng.standard_normal(L), k, "same") * 0.9 + 0.012 * np.sin(2 * np.pi * 100 * tt_)
    tone *= np.clip(np.minimum(tt_ / 0.15, (o1 - o0 - tt_) / 1.5), 0, 1)
    put(fx, tone, o0, 0.14)                                                                         # about 28 dB under her line (measured)
    put(fx, rs(so.hiss(1.1), so.SR), o0 + 0.1, 0.30)                                                # the machine lets off steam
    put(fx, rs(dd.pour(0.9), dd.SR), st_("7.5") + 0.3, 0.10)                                        # and drips on
    for j in range(3):                                                                              # Sofia comes up to the counter
        put(fx, rs(sx.slipper(0.11), getattr(sx, "SR", SR)), st_("7.2") + 0.15 + j * 0.36, 0.5 + 0.1 * (j % 2))
    for t0 in (st_("7.3") + 0.2, st_("7.5") + 1.2):                                                 # paper: the rota, then in her hands
        put(fx, rs(so.swish(0.22), so.SR), t0, 0.22); put(fx, rs(so.swish(0.16), so.SR), t0 + 0.2, 0.16)
    put(fx, rs(so.thump(), so.SR), st_("8.1") + 0.5, 0.45)                                          # her head back on the counter
    span31 = tm["3.1"]["dur"] + tm["3.2"]["dur"]
    bump = st_("3.1") + span31 * 21.0 / 32.0                 # T3's hit drawing
    toot = st_("3.1") + span31 * 12.0 / 32.0
    thud = None
    if SCENE3[0]:
        import on4_motion as m_
        bump = st_("3.1") + span31 * m_.T3_MARKS["bump"]; toot = st_("3.1") + span31 * m_.T3_MARKS["toot"]
        thud = st_("3.1") + span31 * m_.T3_MARKS["thud"] if "thud" in m_.T3_MARKS else None
    C0 = 0.67                                                                                       # v5: the cat first (8 drawings)
    put(fx, rs(so.hiss(0.5), so.SR), 0.25, 0.45)                                                     # the cat across the lens: hiss and yowl
    ty = np.arange(int(0.42 * SR)) / SR; fq = 620 + 900 * np.sin(np.pi * ty / 0.42) ** 0.7 + 40 * np.sin(2 * np.pi * 31 * ty)
    yowl = np.sin(2 * np.pi * np.cumsum(fq) / SR); yowl = np.tanh((yowl + 0.5 * np.sin(4 * np.pi * np.cumsum(fq) / SR)) * 2.0)
    put(fx, yowl * np.minimum(ty / 0.02, 1) * np.minimum((0.42 - ty) / 0.08, 1) * 0.10, 0.27)
    put(fx, rs(so.thump(), so.SR), 0.33, 0.8)
    put(fx, rs(so.swish(0.3), so.SR), 0.72 + C0, 0.9); put(fx, rs(so.thump(), so.SR), 0.85 + C0, 1.6)       # the punch
    put(fx, rs(so.swish(0.9), so.SR), 1.0 + C0, 0.5)                                                     # the shadow runs down the wall
    t_ = np.arange(int(0.5 * SR)) / SR                                                             # the whistle's toot
    if not (SCENE3[0] and thud is not None):                 # with the tap he blows on the tap; the flip's toot sat on "Traffic flows."
        put(fx, np.sin(2 * np.pi * (2300 + 60 * np.sin(2 * np.pi * 38 * t_)) * t_) * np.minimum(t_ / 0.02, 1) * np.exp(-np.maximum(t_ - 0.35, 0) / 0.05) * 0.12, toot)
    put(fx, rs(so.hiss(0.5), so.SR), bump - 0.45, 0.5)                                              # the tyres
    put(fx, rs(so.thump(), so.SR), bump, 2.0 if thud is None else 0.9)
    if SCENE3[0]:
        def whistle(t0, dur_, g=0.12):
            tw = np.arange(int(dur_ * SR)) / SR
            put(fx, np.sin(2 * np.pi * (2300 + 60 * np.sin(2 * np.pi * 38 * tw)) * tw) * np.minimum(tw / 0.02, 1) * np.exp(-np.maximum(tw - dur_ * 0.7, 0) / 0.04) * g, t0)
        t6 = lambda i: st_("3.3") + i / 12.0                                                         # T6's drawings, 12 a second
        if thud is not None:
            whistle(bump, 0.22)                                                                      # his whistle on the tap
            put(fx, rs(so.thump(), so.SR), thud, 2.2); put(fx, rs(so.swish(0.12), so.SR), thud + 0.01, 0.5)   # she lands
        if SCENE3[0] == "cross":                             # (24 Nov) the crossing in four shots (on4_cross): the sounds on its drawings
            import on4_cross as xc
            T3N = float(len(m_.TESTS["T3"]())) if False else 48.0
            W, R, B, G = (lambda i: st_("3.3") + i / 12.0), (lambda i: st_("3.3b") + i / 12.0), (lambda i: st_("3.4") + i / 12.0), (lambda i: st_("3.5") + i / 12.0)
            e0, e1 = st_("3.1") + span31 * 15.0 / T3N, B(8)                                          # the engine: in with the car, idling, away with it
            te = np.arange(int((e1 - e0) * SR)) / SR
            f0 = 44 + 3 * np.sin(2 * np.pi * 0.7 * te) + 22 * np.clip((te - (R(33) - e0)) / 1.2, 0, 1); ph = 2 * np.pi * np.cumsum(f0) / SR
            eng = sum(np.sin(h * ph + h) / h for h in range(1, 7)) * (0.75 + 0.25 * np.sin(ph / 2))
            eng *= np.clip(np.minimum(te / 0.5, (e1 - e0 - te) / 0.6), 0, 1)
            put(fx, eng, e0, 0.05)
            n0, n1 = st_("3.1"), st_("3.6") + 2.5                                                    # the night over the whole crossing: never dead zero
            Ln = int((n1 - n0) * SR); tn = np.arange(Ln) / SR
            night = np.convolve(np.random.default_rng(11).standard_normal(Ln), np.ones(400) / 400, "same") * np.clip(np.minimum(tn / 0.3, (n1 - n0 - tn) / 0.6), 0, 1)
            put(fx, night, n0, 0.16)
            for i in (3, 7, 11, 15):                                                                 # Don's steps to the bonnet; round the tail
                put(fx, rs(so.thump(), so.SR), W(i), 0.22)
            for i in (3, 8):
                put(fx, rs(so.thump(), so.SR), R(i), 0.25)
            for i in (xc.NW + 3, xc.NW + 9, xc.NW + 15):                                             # his glove along the bonnet
                tq = np.arange(int(0.13 * SR)) / SR
                put(fx, np.sin(2 * np.pi * np.cumsum(1700 + 5200 * tq + 90 * np.sin(2 * np.pi * 55 * tq)) / SR) * np.sin(np.pi * tq / 0.13) ** 2 * 0.05, W(i))
            put(fx, rs(so.swish(0.25), so.SR), R(xc.NR - 3), 0.25)                                    # the glass down
            for q in range(6):                                                                       # each of hers flicked up over the roof
                put(fx, rs(so.swish(0.07), so.SR), R(xc.NR + 7 + q * 1.5), 0.30)
            for i in (xc.NR + 20, xc.NR + 23):                                                       # GO, to the car: after Father's line
                whistle(R(i), 0.16, 0.07)
            for q in range(6):                                                                       # each bill lands on her
                put(fx, rs(so.swish(0.07), so.SR), B(q * 1.6 + 9), 0.40)
            for j, i in enumerate((1, 3, 5, 7, 9)):                                                  # the two bodyguards walk in
                put(fx, rs(so.thump(), so.SR), G(i), 0.40 if j % 2 else 0.55)
            for q in range(6):                                                                       # he picks them up, one by one
                put(fx, rs(so.swish(0.05), so.SR), G(xc.TAKE + 1.2 + q * 2.0), 0.22)
            put(fx, rs(so.swish(0.3), so.SR), G(xc.LIFT), 0.45)                                      # up she goes
            for j, i in enumerate(range(xc.GO + 1, 52, 2)):                                          # and away with her
                put(fx, rs(so.thump(), so.SR), G(i), 0.40 if j % 2 else 0.55)
        else:
            e0, e1 = st_("3.1") + span31 * 15.0 / 46.0, t6(64)                                           # the engine: in with the car, idling, away with it
            te = np.arange(int((e1 - e0) * SR)) / SR
            f0 = 44 + 3 * np.sin(2 * np.pi * 0.7 * te); ph = 2 * np.pi * np.cumsum(f0) / SR
            eng = sum(np.sin(h * ph + h) / h for h in range(1, 7)) * (0.75 + 0.25 * np.sin(ph / 2))
            eng *= np.clip(np.minimum(te / 0.5, (e1 - e0 - te) / 0.9), 0, 1)
            put(fx, eng, e0, 0.05)
            n0, n1 = st_("3.1"), st_("3.6") + 2.5                                                        # the night over the whole crossing: never dead zero
            Ln = int((n1 - n0) * SR); tn = np.arange(Ln) / SR
            night = np.convolve(np.random.default_rng(11).standard_normal(Ln), np.ones(400) / 400, "same") * np.clip(np.minimum(tn / 0.3, (n1 - n0 - tn) / 0.6), 0, 1)
            put(fx, night, n0, 0.16)
            for i in (12, 18, 24, 30):                                                                   # his glove along the bonnet
                tq = np.arange(int(0.13 * SR)) / SR
                put(fx, np.sin(2 * np.pi * np.cumsum(1700 + 5200 * tq + 90 * np.sin(2 * np.pi * 55 * tq)) / SR) * np.sin(np.pi * tq / 0.13) ** 2 * 0.05, t6(i))
            for i in (71, 74):                                                                           # GO, to the car: after Father's line (two toots under it and it was not heard)
                whistle(t6(i), 0.16, 0.06)
            for j in range(6):                                                                           # each bill lands on her
                put(fx, rs(so.swish(0.07), so.SR), t6(59 + j * 1.5), 0.30)
            for j, i in enumerate((61, 63, 65, 67, 77, 79, 81, 83)):                                     # the two shadows: in, and away with her
                put(fx, rs(so.thump(), so.SR), t6(i), (0.45 if j % 2 else 0.6) * (0.5 if i < 70 else 1.0))
    if SCENE3[0] != "cross":
        put(fx, rs(so.swish(0.6), so.SR), st_("3.4") + 0.9, 0.35)                                   # the bills
    put(fx, rs(iw.clink(), getattr(iw, "SR", SR)), st_("7.2") + 2.4, 0.8)                           # her mug set down
    crash = st_("2.4") + 32 / 12.0                                                                  # v6: T7's lid
    put(fx, rs(so.swish(0.3), so.SR), crash - 0.27, 0.6)                                            # she goes over
    tc = np.arange(int(0.7 * SR)) / SR
    clang = sum(np.sin(2 * np.pi * f_ * tc) * np.exp(-tc / d_) for f_, d_ in ((212, 0.22), (317, 0.16), (540, 0.10), (873, 0.07))) * 0.10
    put(fx, clang + np.random.default_rng(3).standard_normal(len(tc)) * np.exp(-tc / 0.03) * 0.12, crash)
    put(fx, rs(so.thump(), so.SR), crash, 1.4)
    put(fx, rs(so.metal_click(900, 0.12), so.SR), crash + 0.55, 0.5)                                # the lid lifts
    put(fx, rs(so.swish(0.2), so.SR), crash + 1.3, 0.4); put(fx, rs(so.pop(), so.SR), crash + 1.62, 0.5)   # the peel flicked, landed
    put(fx, rs(so.thump(), so.SR), st_("3.6") + 16 / 12.0, 1.3)                                     # v9: dropped at the club's door
    a0 = st_("6.0")                                                                                 # v13: her act: the band is silent; a snare and a cymbal
    import scipy.signal as sg_
    def roll(d, lvl0=0.5, lvl1=1.0):
        n_ = int(d * SR); tt_ = np.arange(n_) / SR
        nz = rng.standard_normal(n_)
        bb, aa = sg_.butter(2, [900 / (SR / 2), 6000 / (SR / 2)], "band"); nz = sg_.lfilter(bb, aa, nz)
        hits = (1 - (tt_ * 26 % 1.0)) ** 3                                                           # 26 strokes a second
        return nz * hits * (lvl0 + (lvl1 - lvl0) * tt_ / d) * np.minimum(tt_ / 0.03, 1) * 0.30
    def cymbal(d=0.7):
        n_ = int(d * SR); tt_ = np.arange(n_) / SR
        nz = rng.standard_normal(n_); bb, aa = sg_.butter(2, 5000 / (SR / 2), "high"); nz = sg_.lfilter(bb, aa, nz)
        return nz * np.exp(-tt_ / 0.22) * 0.22 + np.sin(2 * np.pi * 180 * tt_) * np.exp(-tt_ / 0.04) * 0.25
    for t0, d, cy in ((0.0, 0.90, 0.92), (1.17, 0.90, 2.08), (2.35, 0.65, 3.0)):
        put(fx, roll(d), a0 + t0); put(fx, cymbal(), a0 + cy)
    for j in range(4):
        put(fx, rs(so.swish(0.12), so.SR), a0 + 0.1 + j * 0.2, 0.3)                                  # the knives turning
    put(fx, rs(so.thump(), so.SR), a0 + 0.84, 0.5)                                                  # into the boards
    put(fx, rs(so.hiss(0.2), so.SR), a0 + 1.42, 0.3)                                                # the small puff
    put(fx, rs(so.hiss(0.6), so.SR), a0 + 1.58, 0.9); put(fx, rs(so.thump(), so.SR), a0 + 1.6, 0.6)  # the fire
    tl = np.arange(int(0.7 * SR)) / SR
    put(fx, np.sin(2 * np.pi * (330 + 520 * tl / 0.7) * tl) * np.minimum(tl / 0.1, 1) * np.minimum((0.7 - tl) / 0.2, 1) * 0.05, a0 + 2.35)   # she rises
    j0 = int(st_("6.05") * SR); fx[j0:int(st_("6.07") * SR) + int(1.4 * SR)] = 0.0                  # the booth, and her hanging there: nothing at all
    f0 = st_("6.07")
    put(fx, rs(so.thump(), so.SR), f0 + 18 / 12.0, 1.5)                                             # the boards
    put(fx, rs(so.thump(), so.SR), f0 + 23 / 12.0, 1.1)                                             # and sat down
    for j in (32, 33, 34):
        put(fx, rs(so.swish(0.14), so.SR), f0 + j / 12.0, 0.3)                                      # the coat brushed off
    if "4.4" in tm:                                                                                 # the final film: her way in, the knife at the envelope
        for j in range(4):
            put(fx, rs(sx.slipper(0.11), getattr(sx, "SR", SR)), st_("4.4") + 0.15 + j * 0.3, 0.45)
        put(fx, rs(so.swish(0.5), so.SR), st_("4.4") + 1.35, 0.5)                                    # the curtain
        put(fx, rs(so.metal_click(900, 0.12), so.SR), st_("6.1") + 0.6, 0.6)                         # the knife out of the boards
        put(fx, rs(so.swish(0.25), so.SR), st_("6.1") + 0.98, 0.6)                                   # the slit
    r0 = st_("8.2") - 0.8
    rain = rs(so.rain(total - r0 + 0.1), so.SR); rain[:int(0.8 * SR)] *= np.linspace(0, 1, int(0.8 * SR))
    put(fx, rain, r0, 1.2)
    put(fx, rs(so.rain(1.2), so.SR) * np.linspace(1, 0, len(rs(so.rain(1.2), so.SR))), 0.0, 1.2)    # the rain runs through the loop's seam
    # the band: in the dream only; dead on the bump (back when she sits up), dead on "Well?"; nothing awake
    crash = st_("2.4") + 32 / 12.0
    band = [(1.0, crash, {}), (crash + 1.6, bump, {}), (st_("3.6") + 2.5, st_("6.0"), {})]
    if SCENE3[0] and thud is not None:                       # dead on the tap; she falls in silence; 1.5 s after she lands the bass walks alone, to the club
        band.insert(2, (thud + 1.5, st_("3.6") + 2.5, dict(drums=0, comp=False)))
    for t0, t1, kw_ in band:
        jz.groove(mus, t0, t1, level=0.8, **kw_)
        j = int(t1 * SR); mus[max(0, j - 144):j] *= np.linspace(1, 0, len(mus[max(0, j - 144):j])); mus[j:] = 0.0   # cut dead (3 ms off the edge: a full-scale step rang to +0.4 dBFS in the AAC)
    mus_end = int(st_("6.0") * SR); mus[max(0, mus_end - 144):mus_end] *= np.linspace(1, 0, len(mus[max(0, mus_end - 144):mus_end])); mus[mus_end:] = 0.0
    if "4.4" in tm:                                                                                 # the final film: the band and the effects give way under every line
        env = np.ones(n)                                                                            # (two lines were not recognized inside the mix, lesson 107)
        nz = np.nonzero(np.abs(voice) > 1e-4)[0]
        if len(nz):
            on = np.zeros(n); on[nz] = 1.0
            w = int(0.25 * SR); on = np.convolve(on, np.ones(w) / w, "same")
            env = 1.0 - 0.92 * np.clip(on * 3.0, 0, 1)
        mus = mus * env; fx = fx * (0.5 + 0.5 * env)
    mix = voice * 1.0 + fx * 0.7 + mus * 0.22
    return mix[:int(total * SR)], marks, dict(bump=round(bump, 2), toot=round(toot, 2))


def main():
    tm, d = sc._timing()
    shots = [x for _, ss in sc.SCENES for x in ss]
    ids = [x["id"] for x in shots]
    tmp = "/tmp/on4_rough"; shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    n = 0
    def put(path, count):
        nonlocal n
        for _ in range(count):
            os.symlink(path, "%s/%05d.png" % (tmp, n)); n += 1
    i = 0
    while i < len(ids):
        grp = next((g for g in MOT if g[0] == ids[i]), None)
        span = grp if grp else (ids[i],)
        end = tm[span[-1]]["start"] + tm[span[-1]]["dur"]
        count = int(round(end * FPS)) - n
        if grp:
            t, a, b = MOT[grp]
            files = sorted(os.listdir("/tmp/on4_mot/" + t))[a:b]
            if len(files) >= count:
                pick = files[:count]
            else:
                pick = [files[min(len(files) - 1, int(j * len(files) / count))] for j in range(count)]
            for f in pick:
                put("/tmp/on4_mot/%s/%s" % (t, f), 1)
        else:
            s, _ = sc.render(shots[i], 1)
            p = "%s/key_%s.png" % (tmp, ids[i]); s.write_to_png(p); put(p, count)
        i += len(span)
    total = n / FPS
    mix, marks, ev = sound(tm, d, total)
    mix = mix / max(1e-6, np.abs(mix).max()) * 0.5
    sf.write(tmp + "/a0.wav", mix.astype(np.float32), SR)
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", tmp + "/a0.wav", "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True)
    I = float([l for l in r.stderr.splitlines() if "I:" in l][-1].split("I:")[1].split("LUFS")[0])
    g = 10 ** ((-15.0 - I) / 20.0)
    for _ in range(4):                                                                              # a soft ceiling at 0.7, then measured again
        out = np.tanh(mix * g / 0.62) * 0.62
        sf.write(tmp + "/a.wav", out.astype(np.float32), SR)
        r = subprocess.run(["ffmpeg", "-hide_banner", "-i", tmp + "/a.wav", "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True)
        I2 = float([l for l in r.stderr.splitlines() if "I:" in l][-1].split("I:")[1].split("LUFS")[0])
        if abs(I2 + 15.0) < 0.3:
            break
        g *= 10 ** ((-15.0 - I2) / 20.0)
    print("lines", marks, ev, "gain %.1f dB" % (20 * np.log10(g)))
    t_ = OUT[:-4] + "_tmp.mp4"
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", tmp + "/%05d.png", "-i", tmp + "/a.wav",
                        "-vf", "fps=24,format=yuv420p", "-c:v", "libx264", "-crf", "20", "-preset", "veryfast",
                        "-c:a", "aac", "-b:a", "128k", "-t", "%.3f" % total, t_])
    if r.returncode == 0:
        os.replace(t_, OUT)
    print(OUT, n, "drawings", round(total, 2), "s")


if __name__ == "__main__":
    main()
