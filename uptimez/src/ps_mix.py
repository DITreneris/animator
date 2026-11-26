"""PICK A SIDE: the whole film's sound as one timeline (Tomas 26 Nov, /grill-me on the sound):
  - the office's vibes bed, The Onboarding's "A" (sound_ob_music, reused): soft rolled chords and a bass note, no
    percussion, 24 bars over the film (8-bar phrases: the loop has no musical join); off in Father's club (scene 4,
    the club's bass only); it stops for the lines that must land (lesson 390): "BOTH." and the shock in 6.1b;
  - every scene's effects as ps_film / ps_film_end place them (captured from their own sound maps, not copied);
  - the voices levelled to one loudness (+-1 dB), at their takes' times;
  - foley in the gaps the audit found (only for something seen on screen);
  - one linear gain to -15 LUFS and a look-ahead peak limiter on the whole film (no per-scene normalising, no dynamic
    loudnorm: lesson 463).
  python3 ps_mix.py -> /tmp/ps_mix_v1.wav (and its report); ps_mix.py mux -> /tmp/ps_master_v2_1080.mp4 + a 540 copy"""
import os
import sys
import subprocess
import numpy as np
import soundfile as sf
import of_sound as osd
import sound_ob_music as obm
import ps_film_fix as fx
import ps_film as pf

SR = osd.SR
VOICE_RMS = -20.0                                            # dBFS, every take's speech RMS before the master
BED_UNDER = 15.0                                             # dB the bed sits under the voices (lesson 429: measure it)
BARS = 24
FX_DUCK = 8.0                                                # dB the effects dip under a line
DUCK = 5.0                                                   # dB the bed dips under a line (2.5 "my" was lost under it: 0.67)
STOPS = [("2.10", "take1", -0.20, 0.90), ("6.1b", "start", 0.0, 1.45)]   # the bed out for "BOTH." (from its take) and the shock
FOLEY = []
OPENER = [True]                                              # v3 (Tomas 26 Nov: "a killer opener, not Chopin"); False = sound v2
MID = [True]                                                 # v4 (Tomas: "not the max version, drop something"): the effort and
                                                             # the servo only in the last round, fewer and softer slats
OB_DRIVE, OB_OVER = 3.0, -3.0  # the opener bus's saturation and level
CRASH_AT = 0.20                                              # 1.2a: the blind lands (ps_film's own crash time)
VIDS = ["/tmp/ps_film_s1_v6_1080.mp4", "/tmp/ps_film_s2_v5_1080.mp4", "/tmp/ps_film_s3_v6_1080.mp4",
        "/tmp/ps_film_s4_v11_1080.mp4", "/tmp/ps_film_s5_v10_1080.mp4", "/tmp/ps_film_s6_v5_1080.mp4"]
VID_LEN = []                                                   # filled by foley_map() once the starts are known


def starts_all():
    """-> {scene: start}, {sid: start} in the joined film: each scene as long as its drawings (as its video)"""
    sc, sh, acc = {}, {}, 0.0
    for n in (1, 2, 3, 4, 5, 6):
        sc[n] = acc
        a2 = acc
        for sid in pf.SCENES[n]:
            sh[sid] = a2
            a2 += pf.DUR[sid]
        acc += VID_LEN[n - 1] if VID_LEN else sum(int(round(pf.DUR[sid] * pf.DPS)) for sid in pf.SCENES[n]) / pf.DPS
    return sc, sh, acc


def _vid_len():
    """each scene's video as it is muxed (the concat's last drawing is held one frame more): the timeline is the picture's"""
    out = []
    for v in VIDS:
        if not os.path.exists(v):
            return []
        out.append(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", v],
                                        capture_output=True, text=True).stdout))
    return out


def effects(n):
    """the scene's effect placements, captured from its own sound map: (array, time in the scene, gain); takes muted"""
    got = []
    put0, take0 = osd.put, pf._take
    def put(buf, a, t0, g):
        if np.any(a):
            got.append((np.array(a, dtype=float), t0, g))
        return put0(buf, a, t0, g)
    def take(sid):
        a, sr = take0(sid)
        return np.zeros_like(a), sr
    osd.put, pf._take = put, take
    try:
        import ps_film_end as fe                             # scenes 1-4: ps_film's own map (fe.setup() swaps pf.sound for
        (fe._old_sound if n < 5 else fe.sound)(n, "/tmp/ps_mix_fx_s%d.wav" % n)   # the ending's, which maps 5-6 only)
    finally:
        osd.put, pf._take = put0, take0
    return got


def rms_db(a):
    return 20 * np.log10(np.sqrt(np.mean(a ** 2)) + 1e-12)


def speech_rms(a):
    """RMS of the take's voiced part (frames over -40 dB of its peak)"""
    w = int(0.02 * SR)
    fr = a[:len(a) // w * w].reshape(-1, w)
    e = np.sqrt((fr ** 2).mean(axis=1))
    keep = fr[e > e.max() * 10 ** (-30 / 20)]
    return rms_db(keep.ravel())


def tone(f0, f1, d, k_=8.0):
    tt = osd.t_(d); ph = 2 * np.pi * np.cumsum(np.linspace(f0, f1, len(tt))) / SR
    return np.sin(ph) * np.minimum(1.0, tt / 0.005) * np.exp(-tt * k_)


def foley_map(sh):
    """the audit's gaps, each given the sound of what is on screen then (no sound for something not seen)"""
    tt = osd.t_(0.04); clk = osd.hp(osd.noise(0.04), 2) * np.exp(-tt * 120)
    rustle = lambda d: osd.hp(osd.noise(d), 2) * np.sin(np.pi * osd.t_(d) / d) ** 2
    out = []
    out.append((rustle(0.5), sh["1.4"] + 1.35, 0.10))                         # 1.4 the roll comes up out of the blind cape
    for j in range(3):                                                        # 2.4 Pam's three hops over the tape
        out.append((clk, sh["2.4"] + 0.15 + 0.14 * j, 0.40))
    out.append((rustle(0.3), sh["2.7"] + 0.05, 0.12))                         # 2.7 her coat as she stops mid-step
    out.append((tone(1800, 600, 0.25, 9) * 0.5 + osd.hp(osd.noise(0.25), 2) * np.exp(-osd.t_(0.25) * 18) * 0.6,
                sh["3.2"] + 0.0, 0.25))                                       # 3.2 the flash's whine and pop
    out.append((tone(880, 1320, 0.09, 30), sh["3.5"] + 0.62, 0.12))           # 3.5 the post lands: a soft blip
    out.append((tone(120, 120, 1.2, 0.6) * 0.6 + 0.3 * tone(240, 240, 1.2, 0.8), sh["4.1"] + 0.0, 0.10))   # 4.1 the neon's hum, up
    for j in range(2):                                                        # 4.3 the guards shift their weight
        out.append((osd.lp(osd.noise(0.12), 4) * np.exp(-osd.t_(0.12) * 25), sh["4.3"] + 1.05 + 0.4 * j, 0.25))
    out.append((tone(1700, 1700, 0.05, 40), sh["6.1"] + fx_end().PRESS_61, 0.20))   # 6.1 the tap on ACCEPT, louder
    return out


def opener(sc, sh):
    """the blind war's own sounds: 1.1's six strokes (Don down, the robot up; each round louder and faster), Don's
    effort, the robot's servo, the crash of 1.2a; 6.2's down and up into the seam, the slats settling over it, and the
    cord creaking under frame 0 until his first yank"""
    import ps_blind_sfx as bs
    import ps_motion as pm_
    out = []
    D = pf.DUR["1.1"]
    strokes = [x for x in pm_.TUG if x[2] != "hold"]
    out.append((bs.creak(pf.HOLD0), 0.0, 0.28 if MID[0] else 0.40))                               # under frame 0: the cord takes his weight
    grunts = ["Hup!", "Huh!", "Hah!"]
    for k_, (a_, b_, kind, _w) in enumerate(strokes):
        ta = pf.HOLD0 + (a_ - 0.2) * ((D - pf.HOLD0) / 1.6)
        tb = pf.HOLD0 + (b_ - 0.2) * ((D - pf.HOLD0) / 1.6)
        rnd = k_ // 2
        g = 0.6 * 10 ** (4.0 * rnd / 20)                                      # each round +4 dB before the bus (about +2.5 after)
        d = tb - ta
        up = kind == "up"
        last = k_ >= len(strokes) - 2                                        # the last round (his and its)
        out.append((bs.zip_(d, 1.0, 26 + 14 * rnd, 70 + 20 * rnd), ta, 0.55 * g))
        out.append((bs.slats(d, (8 if MID[0] else 12) + 3 * rnd, up=up), ta + 0.02, (0.45 if MID[0] else 0.60) * g))
        out.append((bs.clack(top=up), tb - 0.01, 0.55 * g))
        if up and (last or not MID[0]):
            out.append((bs.servo(d, 620 * (1.15 ** rnd)), ta, 0.30 * g))
        elif not up and (last or not MID[0]):
            out.append((bs.grunt(grunts[rnd]), ta + 0.01, 1.4 * g))
    out.append((bs.crash(), sh["1.2a"] + CRASH_AT, 2.2))                    # 1.2a: it comes down off its brackets
    t2 = sh["6.2"]                                                            # 6.2: his yank down, the robot's up
    import ps_film_end as fe
    a0, a1 = fe.DOWN_62
    out.append((bs.zip_(a1 - a0, 1.0, 40, 100), t2 + a0, 0.70))
    out.append((bs.slats(a1 - a0, 16), t2 + a0 + 0.02, 0.75))
    out.append((bs.grunt("Hah!"), t2 + a0 + 0.01, 1.6))
    out.append((bs.clack(), t2 + a1 - 0.01, 0.70))
    b0, b1 = fe.UP_62
    out.append((bs.zip_(b1 - b0, 1.0, 40, 100), t2 + b0, 0.70))
    out.append((bs.slats(b1 - b0, 16, up=True), t2 + b0 + 0.02, 0.75))
    out.append((bs.servo(b1 - b0, 620 * 1.15 ** 3), t2 + b0, 0.38))
    out.append((bs.clack(top=True), t2 + b1 - 0.01, 0.70))
    end = sc[6] + VID_LEN[5] if VID_LEN else t2 + pf.DUR["6.2"]
    out.append((bs.settle(end - (t2 + b1)), t2 + b1 + 0.05, 0.8))            # the slats swing still, into the seam
    return out


def fx_end():
    import ps_film_end as fe
    return fe


def build(path="/tmp/ps_mix_v1.wav"):
    fx.setup()
    VID_LEN[:] = _vid_len()
    sc, sh, total = starts_all()
    L = int((total + 0.05) * SR)
    voice, efx, bedL, bedR = np.zeros(L), np.zeros(L), None, None
    report = []
    for n in (1, 2, 3, 4, 5, 6):                             # the voices, levelled
        acc = sc[n]
        for sid in pf.SCENES[n]:
            for tk, at in zip(pf.TIMING[sid]["takes"], pf.TAKE_AT[sid]):
                a, sr = pf._take(tk)
                if sr != SR:
                    from scipy.signal import resample_poly
                    a = resample_poly(a, SR, sr)
                g = 10 ** ((VOICE_RMS - speech_rms(a)) / 20)
                report.append("voice %-6s %+5.1f dB" % (tk, 20 * np.log10(g)))
                osd.put(voice, a, sh[sid] + at, g)
    s62 = sh["6.2"] - sc[6]
    onsets = [sh[sid] + at for n in (1, 2, 3, 4, 5, 6) for sid in pf.SCENES[n] for at in pf.TAKE_AT[sid]]
    for n in (1, 2, 3, 4, 5, 6):                             # every scene's own effects, at its place
        for a, t0, g in effects(n):
            if OPENER[0] and (n == 1 or (n == 6 and t0 >= s62 - 0.01)):
                continue                                     # the blind's own sounds below replace the tug's and 6.2's
            T, d_ = sc[n] + t0, len(a) / SR
            hit = [o for o in onsets if T - 0.02 <= o < T + d_]
            if hit and d_ < 0.3:                             # v5: a short effect on a line's first syllable moves ahead of it
                report.append("moved a %.2f-s effect off the line at %.2f s" % (d_, hit[0]))   # (2.9's second beep: "Order")
                T = hit[0] - d_ - 0.03
            osd.put(efx, a, T, g)
    ob_ = np.zeros(L)
    if OPENER[0]:                                            # the blind's sounds on their own bus, saturated (their pings'
        ob = np.zeros(L)                                     # crest drove the whole opening into the limiter: v3a's first 4 s
        for a, t0, g in opener(sc, sh):                      # sat at the ceiling, flat, the rounds and the crash level)
            osd.put(ob, a, t0, g)
        pk = np.abs(ob).max() + 1e-9
        ob = np.tanh(OB_DRIVE * ob / pk) / np.tanh(OB_DRIVE)
        vr0 = rms_db(voice[np.abs(voice) > 1e-4])
        seg = ob[int(0.4 * SR):int(pf.DUR["1.1"] * SR)]
        ob *= 10 ** ((vr0 + OB_OVER - rms_db(seg)) / 20)     # the tug as loud as a line (OB_OVER dB over it)
        ob_ = ob
        report.append("opener bus: drive %.1f, the tug %+.1f dB over the voices" % (OB_DRIVE, OB_OVER))
    club = osd.lp(osd.noise(sc[5] - sc[4]), 40) * 0.5          # Father's club: a low murmur of the room under the bass
    osd.put(efx, club * np.minimum(1, osd.t_(sc[5] - sc[4]) / 0.15) * np.minimum(1, (sc[5] - sc[4] - osd.t_(sc[5] - sc[4])) / 0.1),
            sc[4], 0.05)                                     # (44-45.5 s was the film's only gap left at -45 dB)
    for a, t0, g in foley_map(sh):
        osd.put(efx, a, t0, g)
    if OPENER[0]:                                            # bar 1 on the crash; whole bars up to the shock
        t_in = sh["1.2a"] + CRASH_AT
        span = sh["6.1b"] - t_in
        nb = max(8, int(round(span / 2.96)))
        bl0, br0, bar = obm.bed(nb * (span / nb) + 3.0, nb + 1, "A")
        i0 = int(t_in * SR)
        bl, br = np.zeros(L), np.zeros(L)
        n_ = min(L - i0, len(bl0)); bl[i0:i0 + n_] = bl0[:n_]; br[i0:i0 + n_] = br0[:n_]
    else:
        bl, br, bar = obm.bed(total, BARS, "A")              # the bed
    env = np.ones(L)
    def fade_out(t0, t1, d=0.12):
        i0, i1 = int(t0 * SR), int(t1 * SR); k = int(d * SR)
        env[i0:i1] = 0.0
        env[max(0, i0 - k):i0] = np.minimum(env[max(0, i0 - k):i0], np.linspace(1, 0, i0 - max(0, i0 - k)))
        env[i1:i1 + k] = np.minimum(env[i1:i1 + k], np.linspace(0, 1, len(env[i1:i1 + k])))
    fade_out(sc[4], sc[5], 0.08)                             # Father's club: the club's own bass only
    if OPENER[0]:                                            # v3: the bed comes in on the blind's crash (bar 1) and is out
        t_in = sh["1.2a"] + CRASH_AT                         # from the shock to the end: the seam and the tug are the blind's
        fade_out(0.0, t_in, 0.01)
        fade_out(sh["6.1b"], total + 0.1, 0.12)
    for sid, ref, a_, b_ in STOPS:
        t0 = sh[sid] + (pf.TAKE_AT[sid][1] if ref == "take1" else 0.0)
        fade_out(t0 + a_, t0 + b_)
        report.append("bed stop %s %.2f-%.2f s" % (sid, t0 + a_, t0 + b_))
    bm = (bl[:L] + br[:L]) / 2 if len(bl) >= L else np.pad((bl + br) / 2, (0, L - len(bl)))
    va = osd.lp(np.abs(voice), int(0.03 * SR))                # the bed ducks under every line (DUCK dB), back in 0.25 s
    act = np.clip(va / (np.percentile(va[va > 1e-4], 50) + 1e-9), 0, 1)
    from scipy.ndimage import maximum_filter1d
    k = int(0.25 * SR); act = maximum_filter1d(act, size=k, origin=-(k // 2) + 1)    # held 0.25 s after the line
    env = env * (1 - (1 - 10 ** (-DUCK / 20)) * osd.lp(act, int(0.08 * SR)))
    vr = rms_db(voice[np.abs(voice) > 1e-4])
    br_ = rms_db(bm[np.abs(bm) > 1e-5])
    gb = 10 ** ((vr - BED_UNDER - br_) / 20)
    bed = bm * env * gb
    report.append("bed: %.1f dB under the voices (gain %.3f), %d bars of %.2f s" % (BED_UNDER, gb, BARS, bar))
    room = osd.room(L / SR + 0.01)[:L] * 0.012
    pre = np.maximum(act, np.roll(act, -int(0.12 * SR)))          # 0.12 s ahead: the first consonant clear (2.9's beep ate the "B")
    efx_duck = 1 - (1 - 10 ** (-FX_DUCK / 20)) * osd.lp(pre, int(0.04 * SR))   # v5: the effects step back under a line too
    mix = voice + efx * efx_duck + ob_ + bed + room                   # (2.10's squeak ate "Both.": 0.00; 2.9's beeps the "B")
    x = mix / (np.abs(mix).max() + 1e-9) * 0.5               # one linear gain to -15 LUFS, a look-ahead limiter (pf.sound's)
    from scipy.ndimage import minimum_filter1d
    g, ceil = 1.0, 10 ** (-4.0 / 20)
    for _ in range(10):
        y = x * g
        need = np.minimum(1.0, ceil / (np.abs(y) + 1e-9))
        need = minimum_filter1d(need, size=int(0.004 * SR) * 2 + 1)
        need = np.minimum(need, osd.lp(need, int(0.05 * SR)))
        y = y * need
        sf.write(path, y.astype(np.float32), SR)
        I, P = osd.levels(path)
        if abs(I + 15.0) < 0.2 and P <= -2.0:
            break
        g *= 10 ** ((-15.0 - I) / 20)
    report.append("mix: %.1f LUFS, %.1f dB peak, %.2f s" % (I, P, total))
    print("\n".join(report))
    return path, total


def mux(wav="/tmp/ps_mix_v1.wav", out="/tmp/ps_master_v5_1080.mp4"):
    vids = VIDS
    with open("/tmp/ps_mix_vids.txt", "w") as f:
        for v in vids:
            f.write("file '%s'\n" % v)
    tags = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709"]
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", "/tmp/ps_mix_vids.txt",
                           "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest"]
                          + tags + [out])
    c540 = os.path.join(pf.OUT, "ps_film_master_v5_540.mp4")
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", out, "-vf", "scale=540:960:flags=lanczos,format=yuv420p",
                           "-c:v", "libx264", "-crf", "20", "-preset", "veryfast"] + tags + ["-c:a", "copy", c540])
    print("wrote", out, c540, osd.levels(out))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "mux":
        mux()
    else:
        build()
