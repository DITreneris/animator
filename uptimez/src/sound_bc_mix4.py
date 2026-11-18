"""v4.1 (18 Nov): no beeps; the car is an engine rolling closer under "He's applying for your job." and the tilt, a
handbrake, the engine cut, then his door. v4 (18 Nov), a copy of sound_bc_mix.py (kept, unchanged) for bc_anim4.py: it reads bc_timing_v4.json and
writes bc_mix_v4.wav / bc_mix_master_v4.wav. Changes: the phone buzzes once more after "First candidate." (he does not
move), in place of the buzz under the line; under the last shots a car reverses (three muffled beeps) and its door
shuts outside before the creak, so the loop says that Father, who was parking, is the next candidate.

The mix for "The Best Candidate": voices, effects, room tone and a looping waiting-room bed, from bc_timing.json.
The loop is in the sound too:
  - the bed is a four-bar vamp (maj7, m7, m7, dominant: chords and a bass, no tune), and the film is exactly a whole
    number of four-bar phrases long (the tempo is set from the film's length), so the replay restarts on the beat;
  - every tail that runs past the end wraps round to the start (si.add), and the door's creak straddles the loop
    point, so there is no silence and no click at the join;
  - the level is one constant gain to -14 LUFS (not a dynamic normaliser, which would breathe across the join).
The bed is ducked under every voice. It stops dead on "I'd make you apologize." and comes back, as if nothing had
happened, on "Good boy."; it stops dead again on "DONNIE!" and returns with the door.
  python3 sound_bc.py mix  ->  bc_mix.wav (48 kHz stereo)"""
import json
import subprocess
import numpy as np
import soundfile as sf
import sound_iwry as si
import sound_xmas as sx
import sound_on as so

SR = 48000
rng = np.random.default_rng(57)


def fx(a, peak):
    a = np.asarray(a, dtype=np.float64)
    return a / (np.abs(a).max() + 1e-9) * peak


def fade(a, fi=0.004, fo=0.02):
    a = a.copy()
    n, m = int(fi * SR), int(fo * SR)
    a[:n] *= np.linspace(0, 1, n); a[-m:] *= np.linspace(1, 0, m)
    return a


def tone(f, d, decay=6.0, harm=((1, 1.0), (2, 0.3), (3, 0.12))):
    t = np.arange(int(d * SR)) / SR
    return sum(g * np.sin(2 * np.pi * f * h * t) for h, g in harm) * np.exp(-decay * t)


def buzz_phone(d):
    """A phone on a table: bursts of a low motor hum that rattles the wood."""
    t = np.arange(int(d * SR)) / SR
    a = np.sin(2 * np.pi * 168 * t) * (0.6 + 0.4 * np.sign(np.sin(2 * np.pi * 168 * 2 * t)))
    a += si.lp(rng.standard_normal(len(t)), 40) * 0.5
    gate = ((t % 0.5) < 0.3).astype(float)
    return fade(a * si.lp(gate, int(0.01 * SR)), 0.01, 0.03)


def buzzer(d=0.38):
    t = np.arange(int(d * SR)) / SR
    a = np.sign(np.sin(2 * np.pi * 196 * t)) * 0.6 + np.sign(np.sin(2 * np.pi * 277 * t)) * 0.4
    return fade(si.lp(a, 6), 0.004, 0.03)


def chime(notes, gap=0.11, d=0.5):
    out = np.zeros(int((gap * (len(notes) - 1) + d) * SR) + 8)
    for i, f in enumerate(notes):
        a = tone(f, d, 7.0, ((1, 1.0), (2.76, 0.25), (5.4, 0.08)))
        i0 = int(i * gap * SR); out[i0:i0 + len(a)] += a
    return out


def creak(d):
    """A door on its hinge: a squeak whose pitch wanders up as it opens."""
    t = np.arange(int(d * SR)) / SR
    f = 300 + 260 * (t / d) ** 1.5 + 40 * np.sin(2 * np.pi * 3.1 * t)
    ph = 2 * np.pi * np.cumsum(f) / SR
    a = np.sign(np.sin(ph)) * 0.5 + np.sin(ph * 2.01) * 0.5
    a = a - si.lp(a, 24)
    env = (0.35 + 0.65 * np.abs(np.sin(2 * np.pi * 7.3 * t + np.sin(2 * np.pi * 1.7 * t)))) * np.sin(np.pi * t / d) ** 0.6
    return a * env


def scrub(d, rate=3.0):
    t = np.arange(int(d * SR)) / SR
    n = rng.standard_normal(len(t))
    n = si.lp(n - si.lp(n, 5), 3)
    return fade(n * (0.25 + 0.75 * np.abs(np.sin(2 * np.pi * rate * t))) ** 2, 0.02, 0.05)


def steps(n, gap, peak=1.0):
    out = np.zeros(int((n * gap + 0.2) * SR) + 8)
    for i in range(n):
        a = fx(sx.slipper(0.11), peak * (0.8 + 0.2 * (i % 2)))
        i0 = int(i * gap * SR); out[i0:i0 + len(a)] += a
    return out


# ------------------------------------------------------------------ the bed
CHORDS = [(48, (60, 64, 67, 71)), (45, (57, 60, 64, 67)), (50, (57, 60, 65, 69)), (43, (59, 62, 65, 69))]   # C, Am7, Dm7, G9-ish


def car(d_in, d_out):
    """A car outside, through a wall: a low four-cylinder thrum (30 Hz firing, harmonics to ~300 Hz, so a phone speaker
    still carries it) and tyre hiss, rolling closer for d_in s while it slows, then the engine cut: a short sag and
    nothing. Returns (signal, sample of the cut)."""
    n_in, n_out = int(d_in * SR), int(d_out * SR)
    n = n_in + n_out
    t = np.arange(n) / SR
    x = np.clip(t / d_in, 0, 1)
    f = 34 - 6 * x                                                            # it slows down as it rolls in
    f[n_in:] = 28 * (1 - 0.35 * np.clip((t[n_in:] - d_in) / d_out, 0, 1))    # the cut: the revs sag
    ph = 2 * np.pi * np.cumsum(f) / SR
    thr = sum(np.sin(h * ph + h * 0.7) / h ** 0.8 for h in range(1, 10))
    thr *= 1 + 0.25 * np.sin(ph / 2)                                           # the lumpy idle
    tyre = si.lp(rng.standard_normal(n), 9) * 0.35 * (1 - x) ** 0.5
    amp = (0.15 + 0.85 * x ** 1.6)                                             # closer and louder
    amp[n_in:] *= np.exp(-(t[n_in:] - d_in) * 9)
    sig = si.lp(thr * amp + tyre * amp, 14)                                    # muffled by the wall
    return fx(fade(sig, 0.3, 0.02), 0.07), n_in


def ratchet(d):
    """A handbrake pulled up: quick plastic clicks, a little faster at the top."""
    out = np.zeros(int(d * SR))
    t = 0.0
    while t < d - 0.02:
        a = so.metal_click(2300, 0.012)
        i = int(t * SR); out[i:i + len(a)] += a[:len(out) - i]
        t += 0.032 - 0.012 * t / d
    return si.lp(out, 3)


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def ep(m, d):
    """A soft electric-piano note: a sine, a bell partial that dies fast, a slow tremolo."""
    t = np.arange(int(d * SR)) / SR
    f = hz(m)
    a = np.sin(2 * np.pi * f * t) * np.exp(-2.2 * t) + 0.25 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-9 * t)
    return a * (1 + 0.12 * np.sin(2 * np.pi * 4.6 * t)) * np.minimum(1, t / 0.006)


def bed(total, bars):
    """bars of 4/4 over `total` seconds. Returns (left, right, bar length)."""
    bar = total / bars
    beat = bar / 4
    L = int(round(total * SR))
    l, r = np.zeros(L), np.zeros(L)
    comp = (0.0, 1.5, 2.5, 3.5)                              # a lazy bossa comp
    for b in range(bars):
        root, notes = CHORDS[b % 4]
        t0 = b * bar
        for j, off in enumerate(comp):
            for i, m in enumerate(notes):
                a = ep(m, beat * 1.6) * (0.55 if j else 0.8)
                pan = 0.35 + 0.1 * i                        # the chord spread a little across the pair
                si.add(l, a * (1 - pan), t0 + off * beat + i * 0.004)
                si.add(r, a * pan, t0 + off * beat + i * 0.004)
        for off, m in ((0.0, root), (1.5, root + 7), (2.0, root + 12), (3.5, root + 7)):
            t = np.arange(int(beat * 1.2 * SR)) / SR
            a = np.sin(2 * np.pi * hz(m) * t) * np.exp(-3.5 * t) * np.minimum(1, t / 0.008) * 0.9
            si.add(l, a * 0.5, t0 + off * beat); si.add(r, a * 0.5, t0 + off * beat)
        for e in range(8):                                   # a shaker on the eighths, the off-beats louder
            n = rng.standard_normal(int(0.05 * SR))
            a = (n - si.lp(n, 4)) * np.exp(-np.arange(len(n)) / (0.012 * SR)) * (0.16 if e % 2 else 0.09)
            si.add(l, a * 0.35, t0 + e * beat / 2); si.add(r, a * 0.65, t0 + e * beat / 2)
    for x in (l, r):                                         # it comes out of a ceiling speaker
        x -= si.lp(x, int(SR / 260))
        x[:] = si.lp(x, 7)
    return l, r, bar


def main(out="bc_mix_v4.wav"):
    T = json.load(open("bc_timing_v4.json"))
    tk = json.load(open("bc_voices/takes.json"))
    S = {s["name"]: s for s in T["shots"]}
    Ln = {ln["key"]: ln for ln in T["lines"]}
    total = T["total"]
    L = int(round(total * SR))
    vox = np.zeros(L)
    fl, fr = np.zeros(L), np.zeros(L)

    def put(a, t, pan=0.0, g=1.0):
        """pan: -1 left ... +1 right."""
        si.add(fl, a * g * (1 - max(0, pan)), t % total); si.add(fr, a * g * (1 + min(0, pan)), t % total)

    def at(name, off=0.0):
        return S[name]["t0"] + off

    for ln in T["lines"]:
        a = sf.read(f"bc_voices/{ln['key']}.wav")[0].astype(np.float64)
        si.add(vox, so.room(a, 0.10), ln["t0"])

    # ---- effects
    dend = S["s_door_end"]
    put(fx(creak(dend["d"] - 0.2 + S["s_door"]["d"]), 0.16), dend["t0"] + 0.2, -0.5)  # one creak across the loop point
    t_cut = at("s_tilt", 0.75)                                                # v4.1: Father parks, outside
    eng, cut_i = car(t_cut - Ln["job"]["t0"], 0.45)
    put(eng, Ln["job"]["t0"], 0.55)
    put(fx(ratchet(0.32), 0.05), t_cut - 0.42, 0.6)                            # the handbrake
    put(fx(si.lp(sx.thunk(0.2, 85), 4), 0.16), dend["t0"] + 0.03, 0.6)          # v4: his car door shuts
    put(fx(so.metal_click(1700, 0.04), 0.05), dend["t0"] + 0.05, 0.6)
    put(fx(creak(0.5), 0.12), at("s_mom_door", 0.05), -0.5)
    for name, off, d in (("s_phone47", 0.0, 0.55), ("s_q1", 0.9, 1.0), ("s_q2", 1.2, 1.0),
                         ("s_q3", 0.1, 2.4), ("s_sorry", 0.3, 0.6), ("s_pause", 0.0, S["s_pause"]["d"]),
                         ("s_mom_looks", 0.0, S["s_mom_looks"]["d"]), ("s_phone_hover", 0.0, S["s_phone_hover"]["d"])):
        put(fx(buzz_phone(d), 0.10 if name != "s_phone_hover" and name != "s_phone47" else 0.2), at(name, off), 0.25)
    put(fx(sx.thunk(0.12, 140), 0.25), at("s_phone47", S["s_phone47"]["d"] * 0.78), 0.2)      # face down
    put(fx(buzz_phone(0.4), 0.10), Ln["first"]["t1"] + 0.12, 0.25)                             # v4: again; ignored
    put(fx(so.metal_click(2600, 0.05), 0.2), at("s_sorry_client", 0.15), 0.25)                 # he picks it up
    put(fx(chime((880, 1175), 0.09, 0.45), 0.16), at("s_answered", 0.12))
    put(fx(sx.thunk(0.16, 120), 0.2), at("s_small_low", 0.05), -0.3)                           # the CV lands
    put(fx(so.pop(), 0.2), at("s_half", 0.12), -0.3)
    put(fx(so.pop(), 0.22), at("s_true", 0.06), -0.2)
    put(fx(chime((660, 880)), 0.15), Ln["short"]["t1"] + 0.1, 0.2)                              # PROCEED
    put(fx(chime((660, 880)), 0.15), at("s_push", 0.3), 0.2)
    put(fx(buzzer(), 0.22), at("s_ageism"), 0.2)
    put(fx(buzzer(), 0.22), at("s_family"), 0.2)
    put(fx(chime((660, 880, 1320), 0.1, 0.7), 0.15), at("s_approved", 0.0), 0.2)                # NO BIAS DETECTED
    for name in ("s_robot_height", "s_experience"):
        put(fx(si.servo(0.25, 380, 520), 0.07), at(name, 0.02), 0.5)
    put(fx(si.servo(0.5, 260, 420), 0.10), at("s_verdict", 0.0), 0.5)
    put(fx(np.concatenate([fx(si.tick(1800), 1.0)] * 2 + [np.zeros(2000)]), 0.12), at("s_cross", 0.05), 0.2)   # two strokes
    put(fx(sx.scrape(0.18), 0.10), at("s_cross", 0.05), 0.2)
    put(fx(steps(4, 0.22), 0.12), at("s_small_out", 0.05), -0.4)
    put(fx(si.squeak(0.5, 3.5), 0.16), at("s_legs", 0.14), -0.3)
    put(fx(sx.thunk(0.2, 80), 0.3), at("s_legs", 0.12), -0.3)
    put(fx(si.clink(), 0.14), at("s_pen_goes", 0.78), -0.2)
    put(fx(si.rattle(0.3), 0.08), at("s_boot", 0.0), -0.3)
    put(fx(sx.whoosh(0.16), 0.14), at("s_upright", 0.0))
    put(fx(sx.thunk(0.1, 160), 0.14), at("s_upright", 0.13))
    put(fx(sx.whoosh(0.14), 0.10), at("s_sorry", 0.0))
    put(fx(sx.whoosh(0.2), 0.14), at("s_stamp", 0.0))
    put(fx(sx.thunk(0.3, 70), 0.55), at("s_stamp", 0.17))
    put(fx(si.lock(), 0.2), at("s_stamp", 0.17))
    put(fx(steps(3, 0.3), 0.12), at("s_leaves", 0.05), 0.2)
    put(fx(sx.rustle(0.25), 0.08), at("s_lick", 0.3), -0.2)
    put(fx(scrub(S["s_stain"]["d"] + S["s_scrub"]["d"]), 0.13), at("s_stain", 0.0), -0.1)
    put(fx(so.swish(0.3), 0.2), at("s_lapel", S["s_lapel"]["d"] * 0.55), -0.1)
    put(fx(sx.boom(), 0.18), at("s_tilt", 0.0))
    t = np.arange(int(0.7 * SR)) / SR                                                         # a pitch that sinks with him
    put(fx(np.sin(2 * np.pi * np.cumsum(330 - 190 * t / 0.7) / SR) * np.exp(-2.5 * t), 0.10), at("s_tilt", 0.05))
    tn = rng.standard_normal(L)                                                               # room tone, all the way round
    tn = si.lp(tn, 60) * 0.5 + np.sin(2 * np.pi * 100 * np.arange(L) / SR) * 0.02
    fl += fx(tn, 0.012); fr += fx(np.roll(tn, 7919), 0.012)

    # ---- the bed: whole four-bar phrases, ducked, with two dead stops
    bars = 4 * max(1, int(round(total / 2.5 / 4)))
    bl, br, bar = bed(total, bars)
    env = si.lp(np.abs(vox), int(0.06 * SR))
    duck = si.lp(1 - 0.6 * np.clip(env / 0.05, 0, 1), int(0.08 * SR))
    gate = np.ones(L)

    def off(t0, t1, back=0.12):
        i0, i1 = int(t0 * SR), int(t1 * SR)
        gate[i0:i1] = 0.0
        n = int(0.012 * SR); gate[i0 - n:i0] = np.minimum(gate[i0 - n:i0], np.linspace(1, 0, n))
        m = int(back * SR); gate[i1:i1 + m] = np.minimum(gate[i1:i1 + m], np.linspace(0, 1, m))
    nb = lambda t: np.ceil(t / bar - 1e-6) * bar                                              # the next bar line
    off(Ln["apologize"]["t0"], min(nb(Ln["goodboy"]["t0"]), Ln["goodboy"]["t1"]))
    off(Ln["donnie"]["t0"], dend["t0"])
    g = 0.105
    fl += bl * duck * gate * g; fr += br * duck * gate * g
    left, right = fl + vox, fr + vox
    st = np.stack([left, right], axis=1)
    st = np.tanh(st * 1.15) / 1.15
    sf.write(out, st.astype(np.float32), SR)
    info = {"total": total, "bars": bars, "bar": round(bar, 4), "bpm": round(240 / bar, 2),
            "bed_off": [[round(Ln["apologize"]["t0"], 2), round(float(min(nb(Ln["goodboy"]["t0"]), Ln["goodboy"]["t1"])), 2)],
                        [round(Ln["donnie"]["t0"], 2), round(dend["t0"], 2)]]}
    json.dump(info, open("bc_mix_v4.json", "w"), indent=1)
    print(info)
    return out


def master(src="bc_mix_v4.wav", out="bc_mix_master_v4.wav", target=-14.0):
    """One constant gain to the target loudness (so the loop has no join), then a check of the true peak."""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", src, "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    i = float([ln for ln in r.splitlines() if ln.strip().startswith("I:")][-1].split()[1])
    a, sr = sf.read(src)
    g = 10 ** ((target - i) / 20)
    for _ in range(4):                                        # the knee takes a little back: nudge the gain to land on target
        b = 0.84 * np.tanh(a * g / 0.84)                      # about -1.5 dBFS of headroom, a soft knee, never a clip
        sf.write(out, b.astype(np.float32), sr)
        r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", out, "-af", "ebur128", "-f", "null", "-"],
                           capture_output=True, text=True).stderr
        got = float([ln for ln in r.splitlines() if ln.strip().startswith("I:")][-1].split()[1])
        if abs(got - target) < 0.15:
            break
        g *= 10 ** ((target - got) / 20)
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", out, "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    tail = [ln.strip() for ln in r.splitlines() if ln.strip().startswith(("I:", "LRA:", "Peak:"))][-3:]
    print("gain %.1f dB ->" % (20 * np.log10(g)), "  ".join(tail))
    return out


if __name__ == "__main__":
    main(); master()
