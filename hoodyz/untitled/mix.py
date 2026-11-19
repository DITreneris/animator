"""Untitled rough 1 mix: voices (Tomas x2, MY AI x2), park birds, gallery hush, footsteps, the rewind, scan, stamps, ding,
marker, bag, the VANDALISM sting, the kick. numpy only, fixed seeds. Writes mix.wav (mono 48 kHz)."""
import os, sys, numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', 'perfect-date'))
import sound as S
from rough import START, SHOTS, NF, VO
SR = 48000; N = NF * SR // 30; rng = np.random.default_rng(11)
T = lambda d: np.arange(int(d * SR)) / SR
t0 = lambda s, fr=0: (START[s] + fr) / 30
vo = np.zeros(N); fx = np.zeros(N); amb = np.zeros(N)
def add(buf, t, x, g=1.0):
    i = int(t * SR); n = len(x); k = min(n, N - i); buf[i:i + k] += x[:k] * g
    if n > k: buf[:n - k] += x[k:] * g                                    # tails wrap over the loop point
lp = S.onepole_lp
def seg(a, b): return int(a * SR), int(b * SR)
museum = (t0('s5') - .05, t0('s8'))                                        # the gallery: from the rewind's end to the exit
# ---- ambience: park birds everywhere but the gallery; the gallery a low hush
park = lp(rng.standard_normal(N), 500) * .08                                 # rough 6: +6 dB, no more holes
t = .2
while t < N / SR - .2:
    d = rng.uniform(.06, .12); f0 = rng.uniform(3200, 4600); tt = T(d)
    add(park, t, np.sin(2 * np.pi * (f0 * tt + rng.uniform(-9000, 9000) * tt ** 2)) * np.sin(np.pi * tt / d), .1); t += rng.uniform(.4, 1.1)
hush = lp(lp(rng.standard_normal(N), 300), 300) * .35
g = np.ones(N); a, b = seg(*museum); g[a:b] = 0; f = int(.05 * SR); g[a - f:a] = np.linspace(1, 0, f); g[b:b + f] = np.linspace(0, 1, f)
amb = park * g + hush * (1 - g)
# ---- footsteps: the walk-in (frame 0), the exit, the walk-off (into the loop)
def step(t, g=.5):
    tt = T(.09); add(fx, t, lp(rng.standard_normal(len(tt)), 900) * np.exp(-tt * 45), g)
for fr in (0, 7, 14): step(fr / 30, .45)
for fr in (0, 7, 14): step(t0('s8', fr), .4)
for fr in (4, 11, 18, 25): step(t0('s16', fr), .45)
# ---- the rewind (shot 4)
add(fx, t0('s4'), S.tape_ff(dur=18 / 30, up=False), .5)
# ---- scan beep (6), three stamp thuds (7), the dog's tag jingle (9), the rising ding (10)
tt = T(.5); add(fx, t0('s6', 3), np.sin(2 * np.pi * (1500 + 400 * tt) * tt) * np.minimum(1, tt * 40) * np.exp(-tt * 3) * (.6 + .4 * np.sin(2 * np.pi * 14 * tt)), .12)
# ---- the museum beat: 120 BPM from shot 5 to the exit. Lines on beats 0, 6, 8; 10/10 stamps on beats 7, 9, 10, 11
B0, BEAT = t0('s5'), .5
nb = int(round((t0('s8') - B0) / BEAT))
mus = np.zeros(N)
for j in range(nb):
    tb = B0 + j * BEAT
    if j % 2 == 0:                                                            # a soft kick on 1 and 3
        tt = T(.25); add(mus, tb, np.sin(2 * np.pi * np.cumsum(np.geomspace(120, 48, len(tt))) / SR) * np.exp(-tt * 14), .9)
    else:                                                                     # a finger snap on 2 and 4
        tt = T(.08); add(mus, tb, (rng.standard_normal(len(tt)) - lp(rng.standard_normal(len(tt)), 1800)) * np.exp(-tt * 60), .35)
    for h in (0, .25):                                                        # a quiet shaker on the 8ths
        tt = T(.05); add(mus, tb + h * 2 * BEAT / 2, (rng.standard_normal(len(tt)) - lp(rng.standard_normal(len(tt)), 4000)) * np.exp(-tt * 70), .08)
    bass = (45, 45, 48, 50)[(j // 2) % 4]                                     # a walking bass, one note per two beats
    if j % 2 == 0:
        tt = T(.9); add(mus, tb, np.sin(2 * np.pi * S.mtof(bass) * tt) * np.exp(-tt * 3) * np.minimum(1, tt * 80), .28)
k = int(t0('s8') * SR); f2 = int(.04 * SR); mus[k - f2:k] *= np.linspace(1, 0, f2); mus[k:] = 0     # cut on the exit
for j in (7, 9, 10, 11):                                                      # the stamps, on the beat
    tt = T(.18); add(fx, B0 + j * BEAT, (np.sin(2 * np.pi * 110 * tt) + lp(rng.standard_normal(len(tt)), 1200) * .6) * np.exp(-tt * 30), .55)
for j in range(5):
    tt = T(.12); add(fx, t0('s9', 4) + j * .14, np.sin(2 * np.pi * (5200 + 300 * (j % 2)) * tt) * np.exp(-tt * 40), .05)
for j, n in enumerate((76, 81, 88)):
    tt = T(.6); add(fx, t0('s10', 1) + j * .07, np.sin(2 * np.pi * S.mtof(n) * tt) * np.exp(-tt * 5), .16)
# ---- marker squeak + the stick going in (11), bag rustle (12)
tt = T(.35); add(fx, t0('s11', 3), np.sin(2 * np.pi * (1900 + 300 * np.sin(2 * np.pi * 7 * tt)) * tt) * np.sin(np.pi * tt / .35) * .5, .1)
tt = T(.12); add(fx, t0('s11', 22), lp(rng.standard_normal(len(tt)), 600) * np.exp(-tt * 35), .6)
tt = T(.5); add(fx, t0('s12', 14), (rng.standard_normal(len(tt)) - lp(rng.standard_normal(len(tt)), 2500)) * np.sin(np.pi * tt / .5) ** 2 * (.5 + .5 * np.sign(np.sin(2 * np.pi * 11 * tt))), .08)
# ---- VANDALISM sting (13): a low brass-like stab under the line
tt = T(.7); stab = sum(np.sign(np.sin(2 * np.pi * S.mtof(n) * tt)) for n in (38, 45, 50)) / 3
add(fx, t0('s13', 1), lp(stab, 900) * np.exp(-tt * 4) * np.minimum(1, tt * 60), .35)
# ---- the kick (15): thump at contact, a card flap whoosh
tt = T(.15); add(fx, t0('s15', 4), (np.sin(2 * np.pi * 85 * tt) + lp(rng.standard_normal(len(tt)), 700) * .7) * np.exp(-tt * 28), .7)
tt = T(.4); add(fx, t0('s15', 5), lp(rng.standard_normal(len(tt)), 2500) * np.sin(np.pi * tt / .4) * (.6 + .4 * np.sin(2 * np.pi * 18 * tt)), .2)
# ---- rough 6: the dog pants (9); the bag swallows the art: a cartoon slurp (12); Eva's steps and the dog's tag (14);
# the VANDALISM siren after the word (13); a soft room tone under the close-ups so nothing drops to silence
for j in range(5):
    tt = T(.12); add(fx, t0('s9', 2) + j * .16, lp(rng.standard_normal(len(tt)), 2200) * np.sin(np.pi * tt / .12) * (1 if j % 2 else .7), .12)
tt = T(.32); fr = np.geomspace(900, 180, len(tt))
add(fx, t0('s12', 16), np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.sin(np.pi * tt / .32) * (1 + .4 * np.sin(2 * np.pi * 30 * tt)), .22)
for fr_ in (0, 8, 16, 24): step(t0('s14', fr_), .3)
for j in range(4):
    tt = T(.1); add(fx, t0('s14', 2) + j * .2, np.sin(2 * np.pi * (5200 + 300 * (j % 2)) * tt) * np.exp(-tt * 40), .045)
for j in range(3):
    tt = T(.13); add(fx, t0('s13', 22) + j * .13, np.sin(2 * np.pi * (980 if j % 2 == 0 else 760) * tt) * np.sin(np.pi * tt / .13), .07)
room = lp(lp(rng.standard_normal(N), 250), 250) * .25
for s_ in ('s3', 's12b', 's13b'):
    a, b = seg(t0(s_), t0(s_) + dict(SHOTS)[s_] / 30); amb[a:b] += room[a:b]
# ---- voices
for n, s, off in VO:
    x, sr = sf.read(os.path.join(HERE, 'vo', n + '.wav')); assert sr == SR
    add(vo, t0(s, off), x / np.abs(x).max(), 1.0)
# ---- duck the ambience under the voices, sum
w = int(.03 * SR); e = np.clip(np.convolve(np.abs(vo), np.ones(w) / w, 'same') * 10, 0, 1)
hold = np.zeros(N); p_ = 0.; rl = np.exp(-1 / (.25 * SR))                        # a held envelope: the duck stays down between syllables
for i in range(0, N, 48):
    p_ = max(e[i], p_ * rl ** 48); hold[i:i + 48] = p_
e = hold
out = vo + amb * (1 - .9 * e) + mus * (1 - .5 * e) + fx
out = out / np.abs(out).max() * .9
sf.write(os.path.join(HERE, 'mix.wav'), out, SR, subtype='PCM_16'); print('mix ok', round(len(out) / SR, 2), 's')
