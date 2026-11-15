"""Perfect Date mix: park ambience, a synthesised romance tune (the speaker), its dead stop at the hand-hold, voices and effects.
Shot starts come from render.py, so the sound follows any re-timing. Writes mix.wav (mono, 48 kHz, exactly NF frames)."""
import os, sys, numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE); sys.path.insert(0, HERE)
import render as R
SR = 48000; N = R.NF * SR // 30
T0 = [a / 30 for fn, a, b in R.SHOTS]                          # shot start times, s (index 0 = shot 1)
rng = np.random.default_rng(5)
vo = np.zeros(N); mus = np.zeros(N); fx = np.zeros(N); amb = np.zeros(N)
T = lambda d: np.arange(int(d * SR)) / SR
def add(buf, t, x, g=1.0, wrap=False):
    i = int(t * SR); n = len(x)
    if wrap and i + n > N:                                      # the loop: what runs past the end comes in at the start
        buf[i:] += x[:N - i] * g; buf[:i + n - N] += x[N - i:] * g; return
    x = x[:max(0, N - i)]; buf[i:i + len(x)] += x * g
def load(p): x, sr = sf.read(p); assert sr == SR; return x / np.abs(x).max()
midi = lambda n: 440 * 2 ** ((n - 69) / 12)
def lowpass(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); y = np.zeros_like(x); p = 0.
    for i in range(len(x)): p = (1 - a) * x[i] + a * p; y[i] = p
    return y
def epiano(f, d, v=1.0):
    t = T(d); e = np.exp(-t * 3.2) * np.minimum(1, t * 200)
    return v * e * (np.sin(2 * np.pi * f * t) + .35 * np.sin(4 * np.pi * f * t) * np.exp(-t * 6) + .12 * np.sin(6 * np.pi * f * t) * np.exp(-t * 9))
def pad(f, d):
    t = T(d); e = np.minimum(1, t * 3) * np.minimum(1, (d - t) * 3)
    return e * sum(np.sin(2 * np.pi * f * k * t + k) / k for k in (1, 2, 3)) * .5

# ---- park ambience: soft wind and birds, under everything
amb += lowpass(rng.standard_normal(N), 500) * .02
t = .3
while t < N / SR - .3:
    d = rng.uniform(.06, .12); f0 = rng.uniform(3200, 4600); tt = T(d)
    chirp = np.sin(2 * np.pi * (f0 * tt + rng.uniform(-9000, 9000) * tt ** 2)) * np.sin(np.pi * tt / d)
    add(amb, t, chirp, .025); t += rng.uniform(.5, 1.6)

# ---- the rose: a harp sting (shot 8)
for i, n in enumerate([72, 76, 79, 84, 88]): add(fx, T0[7] + .05 + i * .045, epiano(midi(n), .9), .12)

# ---- the speaker: a little romance tune from "play" (shot 10, frame 12) to the hand-hold (shot 16)
start, stop = T0[9] + 12 / 30, T0[15]
beat = 60 / 92
mel = [77, 81, 84, 81, 79, 82, 86, 82, 77, 81, 84, 89, 88, 84, 79, 82]
ch = [(53, 57, 60), (50, 53, 57), (46, 50, 53), (48, 52, 55)]
t, k = start, 0
while t < stop:
    add(mus, t, epiano(midi(mel[k % len(mel)]), beat * 1.6), .22)
    if k % 3 == 0:
        for n in ch[(k // 3) % 4]: add(mus, t, pad(midi(n), beat * 3), .05)
    t += beat / 2; k += 1
mus[int(stop * SR):] = 0                                         # dead stop: she takes its hand
# the trip (shot 12): the tune warbles while the speaker flies
a, b = int((T0[11] + .2) * SR), int((T0[11] + .75) * SR)
seg = mus[a:b].copy(); idx = np.cumsum(1 + .12 * np.sin(np.linspace(0, 9 * np.pi, b - a))); idx = idx / idx[-1] * (len(seg) - 1)
mus[a:b] = np.interp(idx, np.arange(len(seg)), seg)

# ---- effects
for i in range(10): add(fx, T0[3] + i * .045, np.diff(rng.standard_normal(int(.03 * SR)), prepend=0) * np.exp(-T(.03) * 80), .06)   # paws
yt = T(.22); add(fx, T0[5] + .05, np.sin(2 * np.pi * (900 * yt + 2400 * yt ** 2)) * np.exp(-yt * 9), .10)                  # yelp
st = T(.12); add(fx, T0[12] + .1, np.sin(2 * np.pi * (1500 * st + 9000 * st ** 2)) * np.exp(-st * 25), .05)               # balloon squeak
for i in range(4): add(fx, T0[19] + .1 + i * .28, lowpass(rng.standard_normal(int(.05 * SR)), 900) * np.exp(-T(.05) * 60), .25)   # her footsteps

# ---- voices: Hoody = Tomas (whisper take 3, whoa 2, ooh 2, oh 3, sigh 1, breath 3); MY AI = its Learn to Code voice
for f, t, g, w in (('h_whisper', T0[2] + .07, .7, False), ('ai_watch', T0[6] + .15, .6, False),
                   ('h_whoa', T0[11] + .2, .55, False), ('h_ooh', T0[12] + .22, .55, False), ('h_oh', T0[14] + .27, .5, False),
                   ('ai_turn', T0[17] + .2, .6, False), ('h_sigh', T0[18] + .07, .45, False), ('h_breath', T0[19] + .55, .5, True)):
    add(vo, t, load(f'vo/{f}.wav'), g, wrap=w)

# ---- duck music and ambience under the voices, then sum
w = int(.03 * SR); e = np.clip(np.convolve(np.abs(vo), np.ones(w) / w, 'same') * 10, 0, 1)
s = np.zeros(N); p = 0.; rl = np.exp(-1 / (.2 * SR))
for i in range(N): p = e[i] if e[i] > p else p * rl; s[i] = p
out = vo + mus * (1 - .55 * s) + amb * (1 - .85 * s) + fx      # birds clear out of the way of every line
out = out / np.abs(out).max() * .9
sf.write('mix.wav', out, SR, subtype='PCM_16'); print('mix ok', round(len(out) / SR, 2), 's')
