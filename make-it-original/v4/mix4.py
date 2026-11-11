"""v4 soundtrack. His 1986 take and the cat's paw take share the same notes and timing.
Stadium windows are huge (arena reverb + crowd); cuts to reality drop dead to a thin amp or a small speaker.
The speaker plays the cat's version; inside his fantasy it becomes his own guitar. Writes mix.wav (mono)."""
import sys, os, numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..'))
import sound as S
from timeline import RIFF, AI_TUNE, AI_CHORD, ONSETS
from film import G, END, R86, NF
SR = S.SR; N = NF * SR // 30; TOT = N + 3 * SR      # exactly the video's length
rng = np.random.default_rng(7); t_ = np.arange(TOT) / SR
def at(sig, t, buf=None, g=1.0):
    buf = np.zeros(TOT) if buf is None else buf
    i = int(round(t * SR)); n = min(len(sig), TOT - i); buf[i:i + n] += sig[:n] * g; return buf
def bandpass(x, lo, hi): return S.onepole_lp(x, hi) - S.onepole_lp(x, lo)
def conv(x, ir):
    n = len(x) + len(ir); m = 1 << (n - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(x, m) * np.fft.rfft(ir, m), m)[:len(x)]
def window(a, b, fi=.005, fo=.005):
    w = np.zeros(TOT); i, j = int(a * SR), min(TOT, int(b * SR)); w[i:j] = 1
    n = max(1, int(fi * SR)); w[i:i + n] = np.linspace(0, 1, n)
    n = max(1, int(fo * SR)); w[j - n:j] *= np.linspace(1, 0, n); return w
def vo(n): x, sr = sf.read(os.path.join(HERE, '..', 'vo', n + '.wav')); return S.norm(x, .9)

take, _ = S.guitar_phrase(RIFF, detune_cents=18, seed=11); take = S.norm(take, .8)          # his 1986 take
frag, _ = S.guitar_phrase(RIFF[:3], detune_cents=8, seed=21); frag = S.norm(frag, .6)
paws, _ = S.guitar_phrase(RIFF, paws=True, seed=31); paws = S.norm(paws, .8)                # the cat's take
meow = S.meow()
ir = rng.normal(0, 1, int(2.2 * SR)) * np.exp(-np.arange(int(2.2 * SR)) / SR * 2.6); ir = S.onepole_lp(ir, 5000); ir /= np.abs(ir).sum() ** .5 * 6

his = at(take, R86 - .02); his = at(take, G['demo'] - .02, his)                               # his guitar: 1986 and inside the 2026 fantasy
big = his + conv(his, ir) * .9
thin = bandpass(at(take, R86 - .02), 350, 3500) * 1.6
catline = at(paws, G['demo'] - .02); catline = at(paws, G['demo'] + 2.0 - .02, catline)       # the cat video on the monitor, two passes
catline = at(meow, G['demo'] + 2.0 + ONSETS[-1] + .05, catline, .7)
speaker = bandpass(catline, 400, 4500) * 2.5

crowd = bandpass(rng.normal(0, 1, TOT), 300, 2800) * (0.7 + 0.3 * np.sin(2 * np.pi * 2 * t_))
for k in range(26):
    ts = rng.uniform(0, END); d = rng.uniform(.25, .6); n = int(d * SR); tt = np.arange(n) / SR
    f = rng.uniform(1600, 2600) + 500 * np.sin(np.pi * tt / d)
    crowd = at(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * tt / d) * .5, ts, crowd)
crowd = S.norm(crowd, .35)

st1 = window(0, G['wave86'], .01, .004)                       # his fantasy, 1986
stc = window(G['catstad'], 9.0, .02, .004)                    # the cat on his stage (he imagines it)
st2 = window(G['bloom'], G['back'], .25, .004)                # his fantasy, 2026
mix = big * .7 * (st1 + st2) + crowd * .8 * (st1 + st2 * .8) + crowd * 1.0 * stc
mix += thin * window(G['wave86'], 3.7, .004, .1)
bigmeow = at(meow, G['catstad'] + .28); mix += (bigmeow + conv(bigmeow, ir) * 1.2) * 1.1
mix += speaker * (window(G['demo'], G['bloom'], .01, .05) + window(G['back'], END + 3, .004, .01))
mix *= 1 - .55 * window(G['orig'] - .05, G['orig'] + 1.2, .05, .2)

hum = (np.sin(2 * np.pi * 60 * t_) * .006 + np.sin(2 * np.pi * 120 * t_) * .004) * window(G['wave86'], 3.7, .01, .1)
street = S.onepole_lp(rng.normal(0, 1, TOT), 500) * .012 * (window(4.1, 8.0, .1, .01) + window(9.0, 9.5, .01, .05))
fan = S.onepole_lp(rng.normal(0, 1, TOT), 900) * .02 * window(9.9, END + 3, .2, .01) * (1 - window(G['bloom'], G['back'], .25, .004))
mix += hum + street + fan
mix = at(S.norm(S.tape_ff(0.4), .5), G['ff1'], mix); mix = at(S.norm(S.tape_ff(0.4), .5), G['ff2'], mix)
# 2016
mix = at(frag, G['frag'] - .02, mix)
thump = S.onepole_lp(rng.normal(0, 1, int(.12 * SR)), 180) * np.exp(-np.arange(int(.12 * SR)) / SR * 30) * 3
mix = at(thump, G['land'] + .14, mix); mix = at(S.norm(S.ks_pluck(98, .5, .3), .25), G['land'] + .14, mix)     # strings ring as it lands
mix = at(paws, G['cat16'] - .02, mix, 1.7)
mix = at(S.norm(S.tick_roll(0.45), .35), G['views10'], mix)
# robot
def beep(f, d=.06, g=.25): n = int(d * SR); tt = np.arange(n) / SR; return np.sin(2 * np.pi * f * tt) * np.minimum(1, (d - tt) / .02) * g
for i in range(3): mix = at(beep(880 + i * 40), 12.22 + i * .1, mix)
mix = at(beep(1175, .09, .3), 12.52, mix); mix = at(beep(1568, .14, .3), 12.61, mix)
def servo(d=.18, g=.12):
    n = int(d * SR); tt = np.arange(n) / SR; f = 300 + 500 * tt / d
    return S.onepole_lp(np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.sin(np.pi * tt / d) * g, 2500)
mix = at(servo(), G['glance'] + .08, mix); mix = at(servo(.25, .14), G['turn'], mix)
ai, _ = S.tune(AI_TUNE, AI_CHORD, 'epiano'); ai = S.norm(ai, .55)
mix += at(ai, G['ai'] - .02) * window(G['ai'] - .03, G['wave26'] + .05, .005, .04)
mix = at(S.norm(S.swipe(.2), .25), G['recoil'], mix)
for n, t in (('drum', G['drum']), ('ask', G['ask']), ('know', G['know']), ('orig', G['orig'])): mix = at(vo(n), t, mix, 1.75)
mix += S.onepole_lp(rng.normal(0, 1, TOT), 400) * .003
sf.write('mix.wav', mix[:N].astype(np.float32), SR)     # clean downbeat cut at the loop point
print('mix', round(N / SR, 2), 's')
