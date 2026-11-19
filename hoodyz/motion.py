"""Hoodyz motion check: how much each stretch of a film actually moves.
Usage: python3 hoodyz/motion.py film.mp4 [cuts.json]
cuts.json: [[name, start_s, end_s], ...] (one row per shot); without it the film is cut into 0.5 s windows.
Prints mean frame-to-frame change (0-255 grey levels, at 135x240) and the longest run of near-still frames.
Rough guide from Perfect Date v2.3: below ~0.8 a shot reads as frozen; reactions that read sat at 1-3+.
A deliberate hold (a deadpan, a reaction held after the gag) is fine; say so next to it."""
import json, subprocess, sys
import numpy as np

W, H, FPS = 135, 240, 30
film = sys.argv[1]
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', film, '-vf', f'scale={W}:{H}', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'],
                     capture_output=True).stdout
v = np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.float32)
diff = np.abs(np.diff(v, axis=0))
motion, moving = diff.mean((1, 2)), (diff > 6).mean((1, 2))
if len(sys.argv) > 2: cuts = json.load(open(sys.argv[2]))
else: cuts = [[f'{t:.1f}s', t, min(t + .5, len(v) / FPS)] for t in np.arange(0, len(v) / FPS, .5)]
print(f'{"shot":<14}{"time":>13}{"motion":>8}{"still run":>11}')
for name, a, b in cuts:
    i, j = int(a * FPS), max(int(a * FPS) + 1, int(b * FPS) - 1)
    run = best = 0
    for x in moving[i:j]:
        run = run + 1 if x < .004 else 0; best = max(best, run)
    flag = '  <- frozen?' if motion[i:j].mean() < .8 else ''
    print(f'{name:<14}{a:6.2f}-{b:5.2f}s{motion[i:j].mean():8.2f}{best / FPS:9.2f}s{flag}')
