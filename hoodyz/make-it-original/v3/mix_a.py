"""Version A soundtrack. The same 1986 take plays three times (garage, then the tape on the monitor twice).
In the stadium windows it's huge (arena reverb + crowd); the cut to reality drops it dead to a thin garage amp or a
small computer speaker. Writes mix.wav (mono)."""
import sys, os, numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..'))
import sound as S
from timeline import RIFF, AI_TUNE, AI_CHORD
from shots import E, END, R86
SR = S.SR; N = int(round(END * SR)); TOT = N + 3 * SR
rng = np.random.default_rng(7)
t_ = np.arange(TOT) / SR

def at(sig, t, buf=None, g=1.0):
    buf = np.zeros(TOT) if buf is None else buf
    i = int(round(t * SR)); n = min(len(sig), TOT - i); buf[i:i + n] += sig[:n] * g; return buf
def bandpass(x, lo, hi): return S.onepole_lp(x, hi) - S.onepole_lp(x, lo)
def conv(x, ir):
    n = len(x) + len(ir); m = 1 << (n - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(x, m) * np.fft.rfft(ir, m), m)[:len(x)]
def window(a, b, fade_in=.005, fade_out=.005):
    w = np.zeros(TOT); i, j = int(a * SR), int(b * SR); w[i:j] = 1
    fi = max(1, int(fade_in * SR)); w[i:i + fi] = np.linspace(0, 1, fi)
    fo = max(1, int(fade_out * SR)); w[j - fo:j] *= np.linspace(1, 0, fo); return w
def vo(n): x, sr = sf.read(os.path.join(HERE, '..', 'vo', n + '.wav')); return S.norm(x, .9)

# ---- the riff: one 1986 take, placed three times ----
take, _ = S.guitar_phrase(RIFF, detune_cents=18, seed=11); take = S.norm(take, .8)
riff = at(take, R86 - .02); riff = at(take, E['demo'] - .02, riff); riff = at(take, E['demo'] + 2.0 - .02, riff)
ir = rng.normal(0, 1, int(2.2 * SR)) * np.exp(-np.arange(int(2.2 * SR)) / SR * 2.6); ir = S.onepole_lp(ir, 5000); ir /= np.abs(ir).sum() ** .5 * 6
big = riff + conv(riff, ir) * .9                                    # arena
thin = bandpass(riff, 350, 3500) * 1.6                               # a tiny garage amp
speaker = bandpass(riff, 500, 4000) * 1.4                            # a desk speaker
# crowd: band-limited noise that swells with the beat, plus whistles and cheers
crowd = bandpass(rng.normal(0, 1, TOT), 300, 2800) * (0.7 + 0.3 * np.sin(2 * np.pi * 2 * t_))
for k in range(18):
    ts = rng.uniform(0, END); d = rng.uniform(.25, .6); n = int(d * SR); tt = np.arange(n) / SR
    f = rng.uniform(1600, 2600) + 500 * np.sin(np.pi * tt / d)
    crowd = at(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * tt / d) * .5, ts, crowd)
crowd = S.norm(crowd, .35)

st1 = window(0, E['wave86'], .01, .004)                              # stadium 1: ends dead on the cut to the garage
st2 = window(E['bloom'], E['back'], .25, .004)                       # stadium 2: blooms in, cut dead back to the office
mix = big * .7 * (st1 + st2) + crowd * .8 * (st1 + st2 * .8)
mix += thin * window(E['wave86'], 3.7, .004, .1)
mix += speaker * (window(E['demo'], E['bloom'], .01, .05) + window(E['back'], END + 3, .004, .01))
duck = 1 - .55 * window(E['orig'] - .05, E['orig'] + 1.2, .05, .2)  # crowd ducks under the line
mix = mix * duck

# ---- reality layers ----
hum = (np.sin(2 * np.pi * 60 * t_) * .006 + np.sin(2 * np.pi * 120 * t_) * .004) * window(E['wave86'], 3.7, .01, .1)
fan = S.onepole_lp(rng.normal(0, 1, TOT), 900) * .02 * window(4.1, END + 3, .2, .01) * (1 - window(E['bloom'], E['back'], .25, .004))
mix += hum + fan
mix = at(S.norm(S.tape_ff(0.4), .5), E['ff'], mix)
# robot: loading blips, a ready chime, glance and turn servos
def beep(f, d=.06, g=.25): n = int(d * SR); tt = np.arange(n) / SR; return np.sin(2 * np.pi * f * tt) * np.minimum(1, (d - tt) / .02) * g
for i in range(3): mix = at(beep(880 + i * 40), 6.42 + i * .1, mix)
mix = at(beep(1175, .09, .3), 6.72, mix); mix = at(beep(1568, .14, .3), 6.81, mix)
def servo(d=.18, g=.12):
    n = int(d * SR); tt = np.arange(n) / SR; f = 300 + 500 * tt / d
    return np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.sin(np.pi * tt / d) * g
mix = at(S.onepole_lp(servo(), 2500), E['glance'] + .08, mix); mix = at(S.onepole_lp(servo(.25, .14), 2500), E['turn'], mix)
# the AI's tune, cut off when he interrupts
ai, _ = S.tune(AI_TUNE, AI_CHORD, 'epiano'); ai = S.norm(ai, .55)
mix += at(ai, E['ai'] - .02) * window(E['ai'] - .03, E['wave26'] + .05, .005, .04)
mix = at(S.norm(S.swipe(.2), .25), E['recoil'], mix)               # the recoil whoosh
for n, t in (('drum', E['drum']), ('ask', E['ask']), ('know', E['know']), ('orig', E['orig'])): mix = at(vo(n), t, mix, 1.75)   # lines sit on top of the music
mix += S.onepole_lp(rng.normal(0, 1, TOT), 400) * .003              # faint room tone everywhere
# Loop seam: a clean downbeat cut. The opening stadium starts loud, and carrying the speaker's tail into it would
# muddy the riff's first note (checked by the loop-seam measurement).
out = mix[:N].copy()
sf.write('mix.wav', out.astype(np.float32), SR)
print('mix', round(N / SR, 2), 's')
