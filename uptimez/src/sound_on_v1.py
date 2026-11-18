"""Voices and sound for "Office Noir: The Secret of a Stolen Heart" (grill, 16 Nov).
Voices (Kokoro): Don am_onyx (series voice). His noir voice-over is the same take pitched down 2 semitones by
resampling (so also ~12 % slower), a gentle low-pass and a small close room; his on-screen lines stay dry.
Sofia af_bella, the robot voice B (am_echo, robotized), Pam audition A (bf_emma), Mom: three auditioned voices,
each with the shout treatment on "DONNIE!" (soft clip, a semitone up, more level).
Usage:
  python3 sound_on.py takes        -> on_voices/*.wav + on_voices/takes.json (measured lengths)
  python3 sound_on.py audition     -> on_mom_auditions.mp4 (the three Moms, both lines)
  python3 sound_on.py mix MOMKEY   -> on_mix.wav for the animatic timing in on_timing.json"""
import os
import sys
import json
import subprocess
import numpy as np
import soundfile as sf
import sound_iwry as si
import sound_xmas as sx

SR = si.SR
OUT = "on_voices"
DON, SOF = "am_onyx", "af_bella"
MOMS = {   # voice, speed, lang, note
    "A": ("bf_isabella", 0.95, "en-gb", "British, low, stern"),
    "B": ("af_sarah", 1.0, "en-us", "American, brisk, nasal"),
    "C": ("bf_lily", 0.95, "en-gb", "British, sharp, posh"),
}


def pitch(a, semis):
    f = 2 ** (semis / 12)
    return np.interp(np.arange(0, len(a) - 1, f), np.arange(len(a)), a)


def room(a, mix=0.16):
    """A small close room: a few early reflections, no long tail."""
    b = a.copy()
    for ms, g in ((11, 0.55), (19, 0.40), (31, 0.28), (47, 0.18)):
        d = int(ms / 1000 * SR)
        b[d:] += a[:-d] * g * mix * 2
    return b


def noir_vo(txt, speed=1.1):          # 1.1 then -2 semitones: deep, and only ~2 % slower than his voice
    a = sx.best_take(txt, DON, speed, "en-us")
    a = pitch(a, -2.0)
    a = a * 0.75 + si.lp(a, 5) * 0.25                              # warmer, a little darker
    a = room(a)
    a = np.concatenate([a, np.zeros(int(0.06 * SR))])
    return a / np.sqrt(np.mean(a ** 2)) * 0.12


def dry(txt, voice, speed, lang="en-us", g=0.11):
    a = sx.best_take(txt, voice, speed, lang)
    return a / np.sqrt(np.mean(a ** 2)) * g


def cut_off(a, keep):
    """Cut a line dead at `keep` seconds (a 12 ms fade only, to avoid a click)."""
    n = min(len(a), int(keep * SR)); b = a[:n].copy(); f = int(0.012 * SR)
    b[-f:] *= np.linspace(1, 0, f)
    return b


def mom_shout(a):
    a = pitch(a, 1.0)
    peak = np.max(np.abs(a))
    b = np.tanh(a / peak * 3.0) / np.tanh(3.0) * peak               # harder knee than Don's shout, no buzz
    d = int(0.010 * SR); c = b.copy(); c[d:] += b[:-d] * 0.2
    return c / np.sqrt(np.mean(c ** 2)) * 0.19


# v2 after "the woman should be old and shout": each Mom is a blend of a female voice with a little of an older male
# voice (lower, rougher), then aged (a slow wobble, a dry rasp) and really shouted (drawn-out "Donnie!", a hard
# drive, a bright presence lift, a semitone of strain); "Up! Time for work!" is shouted too.
MOMS2 = {   # female, male, male share, speed, lang, note
    "D": ("bf_isabella", "bm_george", 0.28, 0.92, "en-gb", "British grandma, low and rough"),
    "E": ("af_sarah", "am_michael", 0.25, 0.95, "en-us", "American, nasal, piercing"),
    "F": ("bf_alice", "bm_lewis", 0.30, 0.92, "en-gb", "British, shrill, strict"),
}


def blend(fem, male, share):
    return si.K.get_voice_style(fem) * (1 - share) + si.K.get_voice_style(male) * share


def age(a, wob=0.007, rate=5.2, rasp=0.03):
    """Older: a slow wobble in pitch (a variable-rate read), a dry breathy rasp riding the voice's envelope."""
    t = np.arange(len(a)) / SR
    pos = np.cumsum(1 + wob * np.sin(2 * np.pi * rate * t + 0.6 * np.sin(2 * np.pi * 1.3 * t)))
    pos = pos[pos < len(a) - 1]
    b = np.interp(pos, np.arange(len(a)), a)
    env = np.sqrt(si.lp(b ** 2, int(0.015 * SR)))
    n = np.random.default_rng(7).standard_normal(len(b))
    n = si.lp(n - si.lp(n, 3), 2)                                   # a band of hiss, 2-8 kHz-ish
    return b + n * env * rasp * 3


def shout_hard(a, drive=5.0, strain=1.0):
    a = pitch(a, strain)
    a = a + (a - si.lp(a, 6)) * 0.35                                 # presence: the shout's bite
    peak = np.max(np.abs(a))
    b = np.tanh(a / peak * drive) / np.tanh(drive) * peak
    d = int(0.009 * SR); c = b.copy(); c[d:] += b[:-d] * 0.22         # a short hard room, no tail
    return c / np.sqrt(np.mean(c ** 2)) * 0.21


def mom2_lines(key):
    fem, male, share, sp, lang, _ = MOMS2[key]
    v = blend(fem, male, share)
    take = lambda txt, spd: np.asarray(si.K.create(txt, voice=v, speed=spd, lang=lang)[0], dtype=np.float64)

    def clean(a):
        a = np.interp(np.linspace(0, len(a) - 1, int(len(a) * SR / 24000)), np.arange(len(a)), a)
        idx = np.where(np.abs(a) > 0.01)[0]
        return a[max(0, idx[0] - 600):idx[-1] + 2400]
    donnie = shout_hard(age(clean(take("Donnieeee!", sp * 0.78))), drive=6.0, strain=1.5)
    up = shout_hard(age(clean(take("Up! Time for work!", sp * 1.0))), drive=4.0, strain=1.0) * 0.9
    return donnie, up


def mom_lines(key):
    if key in MOMS2:
        return mom2_lines(key)
    v, sp, lang, _ = MOMS[key]
    donnie = mom_shout(sx.best_take("Donnie!", v, sp * 0.9, lang))
    up = dry("Up. Time for work.", v, sp * 1.05, lang, g=0.14)
    return donnie, up


LINES = {   # name: builder
    "vo1": lambda: noir_vo("Monday. Somebody left Pam a heart. Unsigned."),
    "vo_drink": lambda: noir_vo("One drink."),
    "vo_inf": lambda: noir_vo("One informant."),
    "vo_boss": lambda: noir_vo("One boss."),
    "don_sofia": lambda: dry("Sofia. Did you steal my heart?", DON, 0.95),   # v4: the noir pickup line (the title)
    "sofia": lambda: _sof(SOF, None, 0.0, 1.0, -2.0, "I sign my work... darling."),   # v5: audition A, lower, a pause
    "robot": lambda: si.robotize(si.say("Suspect identified.", "am_echo", 1.15), 2, 0.20, 0.45),   # voice B, quicker
    "pam": lambda: sx.pam_line("You left me your heart.", "A"),
    "don_object": lambda: dry("Objection.", DON, 0.92),                # v2: one dry word (replaced, kept)
    "don_framed": lambda: si.don_shout(dry("I was framed!", DON, 1.0)),  # v3: indignant (the audit's pun)
    "vo6": lambda: vo6_build(),                                    # v2: he brags on
    # v4: the robot is Don's partner
    "vo_partner": lambda: noir_vo("My partner. Never blinks."),
    "robot_you": lambda: si.robotize(si.say("You.", "am_echo", 1.0), 2, 0.20, 0.45),
}


_VO6 = {}


def vo6_build():
    """v2: "Nobody tells me what to do." then the list, each word its own take with a real pause (one take rushed
    the list into a blur): "Whiskey." .. "Cards." .. "Money." The split mark is kept for the cut to the brag beat."""
    gap = lambda x: np.zeros(int(x * SR))
    first = noir_vo("Nobody tells me what to do.")
    parts = [first, gap(0.18), noir_vo("Whiskey."), gap(0.12), noir_vo("Money."), gap(0.12), noir_vo("Women.")]   # v5
    _VO6["split"] = (len(first) + int(0.09 * SR)) / SR
    return np.concatenate(parts)


def vo6_marks(meta):
    """v2: vo6 plays whole. vo6_split: the sentence pause after "do." (the cut to the bragging beat);
    vo6_end: where "Money." stops sounding (DONNIE! lands there)."""
    a, _ = sf.read(f"{OUT}/vo6.wav")
    e = np.sqrt(si.lp(a ** 2, int(0.02 * SR)))
    loud = e > 0.02
    runs, i = [], 0
    while i < len(a):                                              # silent runs longer than 120 ms
        if not loud[i]:
            j = i
            while j < len(a) and not loud[j]:
                j += 1
            if j - i > int(0.12 * SR):
                runs.append((i, j))
            i = j
        else:
            i += 1
    inner = [r for r in runs if r[0] > int(0.3 * SR) and r[1] < len(a) - 1]
    meta["vo6_split"] = round(_VO6["split"] if "split" in _VO6 else (inner[0][0] + inner[0][1]) / 2 / SR, 3)
    meta["vo6_end"] = round(float(np.where(loud)[0][-1]) / SR, 3)
    meta.pop("vo6_cut", None)


def takes():
    os.makedirs(OUT, exist_ok=True)
    meta = {}
    for name, fn in LINES.items():
        a = fn()
        sf.write(f"{OUT}/{name}.wav", a, SR)
        meta[name] = round(len(a) / SR, 3)
    for key in MOMS:
        dn, up = mom_lines(key)
        sf.write(f"{OUT}/mom_{key}_donnie.wav", dn, SR); sf.write(f"{OUT}/mom_{key}_up.wav", up, SR)
        meta[f"mom_{key}_donnie"] = round(len(dn) / SR, 3); meta[f"mom_{key}_up"] = round(len(up) / SR, 3)
    vo6_marks(meta)
    json.dump(meta, open(f"{OUT}/takes.json", "w"), indent=1)
    for k, v in meta.items():
        print(f"{k:16s} {v:6.2f} s")


def audition(moms=None, out="on_mom_auditions.mp4"):
    import cairo
    import mom_on as mo
    from kit import Ctx
    Wd, Hd, FPS = 540, 540, 10
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, Wd, Hd)
    audio, frames = [], []
    moms = moms or {k: (v, n) for k, (v, sp, lang, n) in MOMS.items()}
    for key, (v, note) in moms.items():
        dn, up = mom_lines(key)
        a = np.concatenate([np.zeros(int(0.5 * SR)), dn, np.zeros(int(0.35 * SR)), up, np.zeros(int(0.7 * SR))])
        n = int(np.ceil(len(a) / SR * FPS)); a = np.concatenate([a, np.zeros(n * SR // FPS - len(a))])
        c = cairo.Context(surf); c.set_source_rgb(0.98, 0.95, 0.86); c.paint()
        mo.mom(Ctx(c, 0), 140, 900, 1.6, pose="hip_mug", face="shout")
        c.set_source_rgb(0.12, 0.16, 0.27); c.select_font_face("Special Elite", 0, 0)
        for txt, size, y in (("MOM  " + key, 60, 120), (v, 34, 175), (note, 17, 215),
                             ("\"DONNIE!\"", 26, 300), ("\"Up! Time for work!\"" if key in MOMS2 else "\"Up. Time for work.\"", 26, 340)):
            c.set_font_size(size); e = c.text_extents(txt); c.move_to(390 - e.x_advance / 2, y); c.show_text(txt)
        surf.flush(); frames += [bytes(surf.get_data())] * n; audio.append(a)
    mix = np.concatenate(audio); sf.write("/tmp/on_aud.wav", mix, SR)
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{Wd}x{Hd}",
                          "-r", str(FPS), "-i", "-", "-i", "/tmp/on_aud.wav", "-af", "loudnorm=I=-16:TP=-2",
                          "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-shortest",
                          out], stdin=subprocess.PIPE)
    for f in frames:
        p.stdin.write(f)
    p.stdin.close(); p.wait()
    print("audition", round(len(mix) / SR, 1), "s")


# ------------------------------------------------------------------ the animatic's sound (temp: no jazz cue yet)
rng = np.random.default_rng(31)


def tt(d):
    return np.arange(int(d * SR)) / SR


def hp(x, n):
    return x - si.lp(x, n)


def thunder(d=3.4):
    t = tt(d); n = rng.standard_normal(len(t))
    crack = hp(n, 6) * np.exp(-t / 0.05) * 0.9
    rumble = si.lp(si.lp(n, 300), 300) * 60 * np.minimum(1, t / 0.08) * np.exp(-t / 1.1)
    rumble *= 0.7 + 0.3 * np.sin(2 * np.pi * 3.1 * t) * np.sin(2 * np.pi * 0.7 * t)
    return crack * 0.5 + rumble * 0.6


def rain(d):
    t = tt(d); n = rng.standard_normal(len(t))
    b = hp(n, 4) * 0.05 + si.lp(n, 40) * 0.05
    for _ in range(int(d * 22)):                                   # droplets on the glass
        i = rng.integers(0, len(t) - 600); b[i:i + 400] += np.sin(np.arange(400) * 0.9) * np.exp(-np.arange(400) / 60) * 0.05
    return b


def drone(d):
    t = tt(d)
    a = sum(np.sin(2 * np.pi * f * t) * g for f, g in ((55, 0.5), (82.4, 0.25), (110, 0.12), (65.4, 0.18)))
    return a * (0.75 + 0.25 * np.sin(2 * np.pi * 0.18 * t)) * 0.08


def sting(root=110.0, d=2.2):
    t = tt(d); a = np.zeros(len(t))
    for f in (root, root * 1.189, root * 1.498, root * 1.888, root * 0.5):       # minor with a major 7th: noir
        ph = 2 * np.pi * f * t
        a += (np.sin(ph) + 0.35 * np.sin(2 * ph) + 0.18 * np.sin(3 * ph)) * (0.6 if f < root else 1.0)
    a = si.lp(a, 6) * np.minimum(1, t / 0.015) * np.exp(-t / 0.7)
    return a / np.max(np.abs(a)) * 0.32


def metal_click(f=3200, d=0.06):
    t = tt(d)
    return (np.sin(2 * np.pi * f * t) + 0.6 * np.sin(2 * np.pi * f * 1.63 * t)) * np.exp(-t / 0.008) * 0.35 + \
        hp(rng.standard_normal(len(t)), 3) * np.exp(-t / 0.003) * 0.3


def gun_click():
    a = np.zeros(int(0.2 * SR))
    for t0, f in ((0.0, 1900), (0.075, 2600)):
        c = metal_click(f); i = int(t0 * SR); a[i:i + len(c)] += c
    return a * 1.4


def shutter():
    a = np.zeros(int(0.12 * SR))
    for t0 in (0.0, 0.05):
        n = hp(rng.standard_normal(int(0.03 * SR)), 3) * np.exp(-tt(0.03) / 0.006) * 0.35; i = int(t0 * SR); a[i:i + len(n)] += n
    return a


def snag():
    t = tt(0.22)
    f = 260 + 900 * (t / 0.22) ** 1.6
    a = np.sin(2 * np.pi * np.cumsum(f) / SR) * (1 + 0.5 * np.sin(2 * np.pi * 38 * t)) * 0.22 * np.minimum(1, t / 0.01)
    a += hp(rng.standard_normal(len(t)), 5) * 0.06
    return np.concatenate([a, metal_click(4200) * 0.8])


def pop():
    t = tt(0.09)
    return np.sin(2 * np.pi * (200 - 600 * t) * t) * np.exp(-t / 0.02) * 0.35


def swish(d=0.45):
    t = tt(d)
    return si.lp(rng.standard_normal(len(t)), 25) * np.sin(np.pi * t / d) ** 2 * 0.35


def chirp():
    t = tt(0.09)
    return np.sin(2 * np.pi * np.cumsum(3000 + 1500 * t / 0.09) / SR) * np.sin(np.pi * t / 0.09) * 0.05


def mix(T, mom, out="on_mix.wav", music=True):
    """T: on_timing.json (beat starts, total). v2: the jazz-noir cue (sound_on_jazz) replaces the temp drone,
    ducked under every voice; rain in the noir world, cut dead on the colour cut; the bedroom: room tone and two
    birds. music=False gives the v1 temp drone (kept for comparison)."""
    tk = json.load(open(f"{OUT}/takes.json"))
    st, total = T["starts"], T["total"]
    L = int(total * SR); buf = np.zeros(L); vox = np.zeros(L)
    load = lambda n: sf.read(f"{OUT}/{n}.wav")[0]
    cut10 = st[29]                                                     # v5: the noir world dies on DONNIE!
    bed = rain(cut10) * 0.6
    bed[-int(0.004 * SR):] *= np.linspace(1, 0, int(0.004 * SR))       # cut dead
    si.add(buf, bed, 0.0)
    si.add(buf, rng.standard_normal(L - int(cut10 * SR)) * 0.004, cut10)       # bedroom room tone
    for name, t0, gain in T["cues"]:
        if name.startswith("sfx:"):
            fx = {"thunder": thunder, "sting": sting, "flask": lambda: metal_click(2800), "gun": gun_click,
                  "shutter": shutter, "snag": snag, "pop": pop, "dry": lambda: metal_click(4800, 0.03),
                  "swish": swish, "chirp": chirp, "sting_low": lambda: sting(82.4)}[name[4:]]()
            si.add(buf, fx, t0, gain)
            continue
        a = load(name)
        if name == "vo6":
            a = cut_off(a, tk["vo6_end"] + 0.03)                         # DONNIE! takes over right after "Money."
        si.add(vox, a, t0, gain)
    if music:
        import sound_on_jazz as jz
        m = jz.music(T)[:L]
        env = si.lp(np.abs(vox), int(0.06 * SR))
        duck = 1 - 0.62 * np.clip(env / 0.05, 0, 1)
        duck = si.lp(duck, int(0.08 * SR))                                   # smooth the ducking
        mm = np.zeros(L); mm[:len(m)] = m
        si.add(buf, mm * duck[:L] * 0.26, 0.0)                                # the cue sits under the voices
    else:
        s6, e6 = st[17], st[21]
        dr = drone(cut10); g = np.ones(len(dr)); i0, i1 = int(s6 * SR), int(e6 * SR); r = int(0.08 * SR)
        g[i0:i1] = 0.0; g[i0 - r:i0] = np.linspace(1, 0, r); g[i1:i1 + r] = np.linspace(0, 1, r)
        si.add(buf, dr * g, 0.0)
    buf = buf + vox
    buf = np.tanh(buf * 1.2) / 1.2
    sf.write(out, buf.astype(np.float32), SR)
    return out


# ------------------------------------------------------------------ v5 auditions: Sofia's remark, Don's trio
SOFS = {   # key: (label, builder)
    "0": ("dabartine (af_bella)", lambda: dry("I sign my work, darling.", SOF, 0.92)),
    "A": ("Bella zemiau, letai, pauze", lambda: _sof(SOF, None, 0.0, 1.0, -2.0, "I sign my work... darling.")),
    "B": ("Bella + britiska (isabella 30 %)", lambda: _sof(SOF, "bf_isabella", 0.30, 1.0, -1.5,
                                                         "I sign my work... darling.", "en-gb")),
    "C": ("Nicole, alsuojanti", lambda: _sof("af_nicole", None, 0.0, 1.0, -1.5, "I sign my work... darling.")),
    "D": ("Bella + gilumas (vyr. 15 %)", lambda: _sof(SOF, "am_michael", 0.15, 1.0, -1.0,
                                                    "I sign my work. Darling.")),
}


def _sof(voice, other, share, speed, semis, txt, lang="en-us"):
    v = si.K.get_voice_style(voice)
    if other:
        v = v * (1 - share) + si.K.get_voice_style(other) * share
    a = np.asarray(si.K.create(txt, voice=v, speed=speed, lang=lang)[0], dtype=np.float64)
    a = np.interp(np.linspace(0, len(a) - 1, int(len(a) * SR / 24000)), np.arange(len(a)), a)
    idx = np.where(np.abs(a) > 0.01)[0]
    a = pitch(a[max(0, idx[0] - 600):idx[-1] + 2400], semis)
    a = a * 0.8 + si.lp(a, 4) * 0.2                                   # a touch darker
    return a / np.sqrt(np.mean(a ** 2)) * 0.11


def vo6_words(words):
    gap = lambda x: np.zeros(int(x * SR))
    parts = [noir_vo("Nobody tells me what to do."), gap(0.18)]
    for i, w in enumerate(words):
        parts += [noir_vo(w + ".")] + ([gap(0.12)] if i < len(words) - 1 else [])
    a = np.concatenate(parts)
    e = np.sqrt(si.lp(a ** 2, int(0.02 * SR)))
    return a[:np.where(e > 0.02)[0][-1] + int(0.03 * SR)]


def audition3(out="on_auditions_v5.mp4"):
    import cairo
    Wd, Hd, FPS = 540, 540, 10
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, Wd, Hd)
    audio, frames = [], []
    donnie = sf.read(f"{OUT}/mom_F_donnie.wav")[0]
    items = [(f"SOFIA {k}", lab, fn()) for k, (lab, fn) in SOFS.items()]
    for k, words in (("1", ("Whiskey", "Women", "Money")), ("2", ("Whiskey", "Money", "Women"))):
        items.append((f"DON {k}", ". ".join(words) + ". -> DONNIE!", np.concatenate([vo6_words(words), donnie])))
    for title, lab, a in items:
        a = np.concatenate([np.zeros(int(0.4 * SR)), a, np.zeros(int(0.8 * SR))])
        n = int(np.ceil(len(a) / SR * FPS)); a = np.concatenate([a, np.zeros(n * SR // FPS - len(a))])
        c = cairo.Context(surf); c.set_source_rgb(0.08, 0.08, 0.09); c.paint()
        c.set_source_rgb(0.95, 0.93, 0.86); c.select_font_face("Special Elite", 0, 0)
        for txt, size, y in ((title, 64, 230), (lab, 24, 300)):
            c.set_font_size(size); e = c.text_extents(txt); c.move_to(270 - e.x_advance / 2, y); c.show_text(txt)
        surf.flush(); frames += [bytes(surf.get_data())] * n; audio.append(a)
    mix = np.concatenate(audio); sf.write("/tmp/on_aud3.wav", mix, SR)
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{Wd}x{Hd}",
                          "-r", str(FPS), "-i", "-", "-i", "/tmp/on_aud3.wav", "-af", "loudnorm=I=-16:TP=-2",
                          "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-shortest", out],
                         stdin=subprocess.PIPE)
    for f in frames:
        p.stdin.write(f)
    p.stdin.close(); p.wait()
    print("audition", round(len(mix) / SR, 1), "s")


if __name__ == "__main__":
    if sys.argv[1] == "extra":                         # only the named takes, the rest of takes.json kept
        meta = json.load(open(f"{OUT}/takes.json"))
        for n in sys.argv[2:]:
            a = LINES[n](); sf.write(f"{OUT}/{n}.wav", a, SR); meta[n] = round(len(a) / SR, 3); print(n, meta[n])
            if n == "vo6":
                vo6_marks(meta); print("split", meta["vo6_split"], "end", meta["vo6_end"])
        json.dump(meta, open(f"{OUT}/takes.json", "w"), indent=1)
    elif sys.argv[1] == "audition3":
        audition3()
    elif sys.argv[1] == "audition2":                     # the old, shouting Moms; their takes into on_voices/
        os.makedirs(OUT, exist_ok=True)
        meta = json.load(open(f"{OUT}/takes.json"))
        for k in MOMS2:
            dn, up = mom2_lines(k)
            sf.write(f"{OUT}/mom_{k}_donnie.wav", dn, SR); sf.write(f"{OUT}/mom_{k}_up.wav", up, SR)
            meta[f"mom_{k}_donnie"] = round(len(dn) / SR, 3); meta[f"mom_{k}_up"] = round(len(up) / SR, 3)
        json.dump(meta, open(f"{OUT}/takes.json", "w"), indent=1)
        audition({k: (f, "+ %s %d%%  \u00b7  %s" % (m.split("_")[1], sh * 100, n.split(", ", 1)[1]))
                  for k, (f, m, sh, sp, lg, n) in MOMS2.items()}, "on_mom_auditions_v2.mp4")
    else:
        {"takes": takes, "audition": audition}[sys.argv[1]]()
