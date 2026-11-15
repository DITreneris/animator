"""Soundtrack for the rough: places every sound on the shared timeline, wraps the tail across the loop
point, writes mix.wav (mono) and voice placements for lip flap (lips.npy)."""
import numpy as np, soundfile as sf
import sound as S
from timeline import *
N = int(round(END * S.SR)); mix = np.zeros(N + S.SR * 2)
def add(sig, t, g=1.0):
    global mix
    mix = S.place(mix, sig, t, g)
def vo(name):
    x, sr = sf.read(f'vo/{name}.wav'); assert sr == S.SR; return x

g86, _ = S.guitar_phrase(RIFF, detune_cents=18, seed=11)
frag, _ = S.guitar_phrase(RIFF[:3], detune_cents=8, seed=21)
cat, _ = S.guitar_phrase(RIFF, paws=True, seed=31)
cat = S.place(cat, S.meow(), 0.02 + ONSETS[-1] + 0.05, 0.7)
ai, _ = S.tune(AI_TUNE, AI_CHORD, 'epiano')
g86, frag, cat, ai = S.norm(g86, .8), S.norm(frag, .7), S.norm(cat, .8), S.norm(ai, .55)

add(g86, T['riff86'] - 0.02)
add(frag, T['frag16'] - 0.02)
add(cat, T['cat16'] - 0.02)
add(S.norm(S.tape_ff(0.5), .45), T['ff1']); add(S.norm(S.tape_ff(0.5), .45), T['ff2'])
add(S.norm(S.swipe(), .5), T['phone2'] + 0.1)
add(S.norm(S.tick_roll(0.6), .35), T['phone2'] + 0.2)
add(ai, T['ai'] - 0.02)
add(cat, T['cat26'] - 0.02)
add(cat, T['cat26'] + BAR - 0.02, 0.45)          # second pass, ducked under "Now THAT'S original!"
LINES = [('drum', T['drum_line'], 1.0), ('ask', T['ask'], 1.0), ('know', T['know'], 1.0), ('orig', T['orig'], 1.0)]
for n, t, g in LINES: add(S.norm(vo(n), .9), t, g)
room = S.onepole_lp(np.random.default_rng(1).normal(0, 1, len(mix)), 400) * 0.004
mix += room
tail = mix[N:]; mix = mix[:N].copy(); mix[:len(tail)] += tail     # the tail runs across the loop point
sf.write('mix.wav', mix.astype(np.float32), S.SR)

# lip flap: per-frame RMS of each dry voice at its placement
nf = NF; env = {k: np.zeros(nf) for k in ('drum', 'hoodyz')}
for n, t, _ in LINES:
    x = vo(n); hop = S.SR // FPS
    r = np.array([np.sqrt((x[i * hop:(i + 1) * hop] ** 2).mean()) for i in range(len(x) // hop)]); r /= r.max() + 1e-9
    who = 'drum' if n == 'drum' else 'hoodyz'; f0 = int(round(t * FPS))
    for i, v in enumerate(r):
        if f0 + i < nf: env[who][f0 + i] = max(env[who][f0 + i], v)
np.save('lips.npy', np.stack([env['drum'], env['hoodyz']]))
print('mix', round(N / S.SR, 2), 's; frames', NF)
