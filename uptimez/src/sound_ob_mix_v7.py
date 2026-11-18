"""v7, pinned: the mix as The Onboarding v11 used it. sound_ob_mix.py is current.
v7 (sound_ob_mix_v6.py = v6, kept): music= picks another bed from sound_ob_music.py (sparse vibes A, B or C) in place
of the bossa; without it every mix is as before. v6 (sound_ob_mix_v5.py = v5, kept): anim=7 is the mix for animation v10: everything of anim=6 without the rustle that
followed Pam's line by a tenth of a second (speech recognition heard it as a last syllable: "scooper"). v5 (sound_ob_mix_v4.py = v4, kept): anim=6 is the mix for animation v8: everything of anim=5, and the office's music
(the ceiling-speaker bossa of The Best Candidate), cut dead by the cannon and back with the stamp. v4 (sound_ob_mix_v3.py = v3, kept): anim=5 is the mix for animation v7: Pam's line in the hold of beat 09 with nothing
under it, and the cues of the trimmed ending. v3 (sound_ob_mix_v2.py = v2, kept): anim=4 is the mix for animation v6: no emoji pops, the vest cue inside the one
shot of Don's reaction (3.9), and takes= names the folder of voice takes (ob_voices/film_v6 has "Oh..." without its breath).
The mix for "The Onboarding", animatic v2 (sound_ob_mix_v1.py = v1, kept; only the "Oh..." take differs): the 20 measured takes (ob_voices/film), stings and foley, room tone.
No music (the grill of 17 Nov): the silences in beats 03, 05, 09 and 10 are part of the timing under test, so they hold
only the room. Every cue is placed from ob_timing_v1.json (ob_animatic.py timing), never from typed times.
  python3 sound_ob_mix.py  ->  ob_mix_v1.wav, then ob_mix_v1_master.wav at -14 LUFS (one constant gain, soft knee)"""
import json
import numpy as np
import soundfile as sf
import sound_iwry as si
import sound_xmas as sx
import sound_on as so
import sound_bc_mix as bm

SR = 48000
V = "v2"
rng = np.random.default_rng(91)
fx, fade = bm.fx, bm.fade


def tt(d):
    return np.arange(int(d * SR)) / float(SR)


def door(d=0.5):
    """A glass door on a motor: air, a low hum that rises a little, a soft stop."""
    t = tt(d)
    air = si.lp(rng.standard_normal(len(t)), 18) * np.sin(np.pi * t / d) ** 1.5
    hum = np.sin(2 * np.pi * np.cumsum(120 + 50 * t / d) / SR) * np.sin(np.pi * t / d) * 0.5
    a = np.concatenate([air * 0.8 + hum, np.zeros(int(0.12 * SR))])
    stop = fx(sx.thunk(0.1, 110), 0.5)
    i0 = int((d - 0.02) * SR); a[i0:i0 + len(stop)] += stop[:len(a) - i0]
    return a


def snap():
    """The paddle: a hard flat crack, no tail."""
    t = tt(0.09)
    n = rng.standard_normal(len(t))
    return (n - si.lp(n, 3)) * np.exp(-t * 110) + np.sin(2 * np.pi * 240 * t * (1 + 0.5 * np.exp(-t * 60))) * np.exp(-t * 45) * 0.8


def paper(d=0.16):
    """A roll of paper springing shut: a quick rasp and a slap."""
    t = tt(d)
    n = rng.standard_normal(len(t))
    rasp = (n - si.lp(n, 6)) * (t / d) ** 2
    slap = fx(snap(), 0.9)
    return np.concatenate([rasp * 0.5, slap])


def shredder(d=1.25):
    """A cheap office shredder: a motor that takes the load, paper being chewed, a short run-down."""
    t = tt(d)
    up = np.minimum(1, t / 0.08)
    f = 96 * (0.75 + 0.25 * up) * (1 - 0.06 * np.clip((t - 0.15) / 0.3, 0, 1) * np.clip((d - 0.3 - t) / 0.2, 0, 1))
    ph = 2 * np.pi * np.cumsum(f) / SR
    motor = (2 * ((ph / (2 * np.pi)) % 1) - 1) * 0.5 + np.sin(ph * 2) * 0.3
    motor = si.lp(motor, 10)
    n = rng.standard_normal(len(t))
    chew = (si.lp(n, 4) - si.lp(n, 30)) * (0.55 + 0.45 * np.sign(np.sin(2 * np.pi * 31 * t))) \
        * np.clip((t - 0.12) / 0.1, 0, 1) * np.clip((d - 0.28 - t) / 0.1, 0, 1)
    down = np.clip((d - t) / 0.22, 0, 1)
    return fade((motor * 0.7 + chew * 1.3) * up * down, 0.005, 0.03)


def toot():
    """The cannon's cheap fanfare: three notes on a party horn."""
    out = []
    for f, d in ((392, 0.10), (392, 0.10), (523, 0.36)):
        t = tt(d)
        ph = 2 * np.pi * np.cumsum(f * (1 + 0.012 * np.sin(2 * np.pi * 6.5 * t))) / SR
        a = si.lp(np.sign(np.sin(ph)) * 0.6 + np.sin(ph * 3) * 0.2, 5)
        out.append(fade(a, 0.006, 0.03 if d < 0.2 else 0.12)); out.append(np.zeros(int(0.025 * SR)))
    return np.concatenate(out)


def ticks(ts, f=4200):
    out = np.zeros(int((max(ts) + 0.1) * SR))
    for t0 in ts:
        a = si.tick(f); i0 = int(t0 * SR); out[i0:i0 + len(a)] += a[:len(out) - i0]
    return out


def main(out=None, timing=None, anim=False, takes="ob_voices/film", music=None):
    """timing: another timing file of the same shape (the animation's, on the drawing grid). anim: the cues that only
    the animation has (the emoji pop) and the ones it moved (the vest, when his hands get there)."""
    out = out or "ob_mix_%s.wav" % V
    T = json.load(open(timing or "ob_timing_%s.json" % V))
    S = {s["shot"]: s for s in T["shots"]}
    total = T["total"]
    L = int(round(total * SR))
    vox = np.zeros(L)
    fl, fr = np.zeros(L), np.zeros(L)

    def put(a, t, pan=0.0, g=1.0):
        a = np.asarray(a, dtype=np.float64)
        i0 = int(round(t * SR)); a = a[:max(0, L - i0)]
        fl[i0:i0 + len(a)] += a * g * (1 - max(0, pan)); fr[i0:i0 + len(a)] += a * g * (1 + min(0, pan))

    def at(shot, off=0.0):
        return S[shot]["t0"] + off

    def said(shot, off=0.0):                                  # from the end of the shot's line
        return S[shot]["line"]["t1"] + off

    for s in T["shots"]:
        if "line" in s:
            a = so.room(sf.read("%s/%s.wav" % (takes, s["shot"]))[0].astype(np.float64), 0.10)
            i0 = int(round(s["line"]["t0"] * SR)); vox[i0:i0 + len(a)] += a[:L - i0]

    # ---- stings and foley
    put(fx(door(0.5), 0.14), at("1.1", 0.05), -0.5)
    put(fx(bm.steps(3, 0.30), 0.10), at("1.1", 0.62), -0.4)
    put(fx(so.swish(0.25), 0.12), at("1.4", 0.40 if anim in (3, 4, 5, 6, 7) else 0.15), 0.2)    # the vest
    put(fx(si.servo(0.14, 300, 520), 0.07), at("2.2", 0.0), 0.0)                  # it is between them
    put(fx(snap(), 0.45), at("2.2", 0.12), 0.0)                                   # the paddle
    put(fx(bm.buzzer(0.30), 0.13), at("2.2", 0.16), 0.0)
    put(fx(paper(), 0.22), said("3.1", 0.12), -0.4)                               # the drawing springs shut
    put(fx(ticks((0.20, 0.52, 0.80)), 0.035), at("3.8", 0.0), 0.2)                # the pearl, rolling; it stops in 3.10
    if "3.11" in S:
        put(fx(so.swish(0.25), 0.11), at("3.11", 0.50 if anim in (2, 3) else 0.30 if anim else 0.15), 0.2)    # the vest again
    else:                                                                         # v3 (anim=4): Don's reaction is one shot
        put(fx(so.swish(0.25), 0.11), at("3.9", 9 / 12.0), 0.2)
    if anim and anim not in (4, 5, 6, 7):                                                        # anim=4: no emoji, no pop
        put(fx(so.pop(), 0.10), at("3.9", 7 / 12.0), 0.3)                         # the emoji over Don
    if anim == 3:
        put(fx(so.pop(), 0.10), at("5.3", 7 / 12.0), 0.3)                         # and the one over Pam
    put(fx(sx.rustle(0.22), 0.09), at("4.3", 0.12), 0.0)                          # the roll changes hands
    put(fx(sx.thunk(0.12, 150), 0.20), at("4.4", 0.80), 0.3)                      # set down, without a look
    put(fx(shredder(S["4.5"]["d"] - 0.2), 0.30), at("4.5", 0.05), 0.2)
    put(fx(so.swish(0.2), 0.10), at("6.1", 0.25), 0.3)                            # the tablet changes hands
    put(fx(si.tick(1800), 0.12), at("6.3", 0.38), 0.0)                            # his thumb
    put(fx(bm.chime((660, 880)), 0.14), at("6.4", 0.03), 0.0)
    put(fx(sx.rustle(0.3), 0.09), at("6.8", 0.05), 0.2)                           # her CV, into the pack
    put(fx(sx.thunk(0.1, 170), 0.12), at("7.1", 0.15), 0.1)                       # the terminal, pushed across
    put(fx(si.tick(2400), 0.12), at("7.1", 0.70), -0.1)                           # his card
    put(fx(bm.chime((880, 1175), 0.09, 0.45), 0.16), at("7.2", 0.03), 0.0)        # the small payment beep
    put(fx(si.servo(0.3, 300, 460), 0.08), at("7.3", 0.0), 0.2)                   # it leans toward the card
    put(fx(sx.whoosh(0.14), 0.12), at("7.4", 0.25), 0.2)                          # one dollar: the fist
    put(fx(si.servo(0.4, 260, 380), 0.08), at("8.1", 0.0), -0.2)
    put(fx(si.rattle(0.3), 0.12), said("8.1", -0.05), -0.1)                       # the bin, into the cannon
    put(fx(sx.boom(), 0.50), at("8.2", 0.08), 0.0)
    put(fx(toot(), 0.16), at("8.2", 0.22), -0.1)
    put(fx(sx.rustle(0.9), 0.07), at("8.2", 0.3), 0.0)                            # it comes down
    put(fx(bm.steps(3 if anim in (5, 6, 7) else 4, 0.26), 0.10), at("8.4", 0.05 if anim in (5, 6, 7) else 0.10), -0.4)
    if anim in (5, 6, 7):                                                            # v4: Pam speaks in the hold; nothing under her line
        put(fx(sx.rustle(0.3), 0.06), at("9.1", 0.05), 0.4)
        if anim != 7:                                                             # v6 (anim=7): nothing right after it either:
            put(fx(sx.rustle(0.25), 0.06), said("9.1", 0.10), 0.5)                # a rustle a tenth after "scoop." was heard as "scooper"
    else:
        for off, pan in ((0.6, 0.4), (1.7, 0.5), (2.9, 0.35)):                    # Pam, collecting
            put(fx(sx.rustle(0.3), 0.06), at("9.1", off), pan)
        put(fx(si.servo(0.7, 620, 640), 0.03), at("9.1", 1.1), 0.1)               # the robot prints its report
    put(fx(sx.rustle(0.2), 0.07), at("10.3", 0.30 if anim in (5, 6, 7) else 0.45), -0.3)                         # into his pocket
    put(fx(bm.steps(2, 0.3), 0.09), at("10.3", 0.62 if anim in (5, 6, 7) else 0.80), -0.4)
    put(fx(door(0.45), 0.14), at("10.4", 0.05), -0.5)
    put(fx(sx.whoosh(0.2), 0.14), at("10.4", 0.52), -0.3)
    put(fx(sx.thunk(0.3, 70), 0.50), at("10.4", 0.70), -0.3)                      # the stamp, on the glass
    put(fx(si.lock(), 0.18), at("10.4", 0.70), -0.3)
    tn = rng.standard_normal(L)                                                   # the room, all the way through
    tn = si.lp(tn, 60) * 0.5 + np.sin(2 * np.pi * 100 * np.arange(L) / SR) * 0.02
    fl += fx(tn, 0.012); fr += fx(np.roll(tn, 7919), 0.012)
    info = {}
    if anim in (6, 7):                                                                 # v5: the office's music
        # The ceiling-speaker bossa of The Best Candidate (sound_bc_mix.bed), built the same way: whole four-bar phrases
        # over the film's length, so the loop has no musical join; ducked under every line. The cannon cuts it dead;
        # it is back with the stamp on the glass.
        if music:                                                                 # v7: another bed (sound_ob_music), opt-in
            import sound_ob_music as om
            bars = 8 * max(1, int(round(total / 3.1 / 8)))
            bl, br, bar = om.bed(total, bars, music)
        else:
            bars = 4 * max(1, int(round(total / 2.5 / 4)))
            bl, br, bar = bm.bed(total, bars)
        env = si.lp(np.abs(vox), int(0.06 * SR))
        duck = si.lp(1 - 0.6 * np.clip(env / 0.05, 0, 1), int(0.08 * SR))
        if music:                                                                 # the new beds duck BEFORE a line: the follower lags a
            la = int(0.25 * SR)                                                   # voice by a tenth of a second, and "Oh..." (0.5 s) was
            ahead = np.concatenate([duck[la:], np.ones(la)])                      # over before the bed had moved. Whisper heard "No".
            duck = si.lp(np.minimum(duck, ahead), int(0.05 * SR))
        gate = np.ones(L)
        i0, i1 = int(at("8.2", 0.08) * SR), int(at("10.4", 0.70) * SR)
        gate[i0:i1] = 0.0
        n = int(0.012 * SR); gate[i0 - n:i0] = np.linspace(1, 0, n)
        m = int(0.12 * SR); gate[i1:i1 + m] = np.linspace(0, 1, m)
        g = om.GAIN[music] if music else 0.105                                    # 0.105: The Best Candidate's level
        ml, mr = bl[:L] * duck * gate * g, br[:L] * duck * gate * g
        fl += ml; fr += mr
        talk = env > 0.02
        db = lambda x: 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)
        info = dict(bars=bars, bar=round(bar, 4), bpm=round(240 / bar, 1), off=[round(i0 / SR, 2), round(i1 / SR, 2)],
                    voice_over_music_db=round(db(vox[talk]) - db((ml[talk] + mr[talk]) / 2), 1),
                    music_between_lines_db=round(db(((ml + mr) / 2)[(~talk) & (gate > 0.99)]), 1), voice_db=round(db(vox[talk]), 1))
        print("music", info)
    st = np.stack([fl + vox, fr + vox], axis=1)
    st = np.tanh(st * 1.15) / 1.15
    sf.write(out, st.astype(np.float32), SR)
    gaps, last = [], 0.0                                                          # the longest stretches with no voice
    for s in T["shots"]:
        if "line" in s:
            gaps.append((round(s["line"]["t0"] - last, 2), s["shot"])); last = s["line"]["t1"]
    print("wrote", out, "%.2f s" % total, " longest gaps between lines:", sorted(gaps, reverse=True)[:5])
    return out


if __name__ == "__main__":
    bm.master(main(), "ob_mix_%s_master.wav" % V)
