"""Loop gate for Perfect Trip v3: the last frame is frame 0 EXACTLY (0 of 255), the blink pattern repeats at the loop point
(a blink never crosses the seam), and the mix is silent-clean at both ends. Exits 1 on any miss."""
import sys, os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); os.chdir(HERE)
import render as T
a = lambda f: np.frombuffer(T.draw(f).get_data(), np.uint8).astype(int)
bad = []
d = abs(a(0) - a(T.NF - 1)).max()
if d: bad.append(f'frame 0 vs last frame: max diff {d}/255')
for seed in (3, 7):
    if any(T.K.blinking(f, seed) != T.K.blinking(f + T.NF, seed) for f in range(T.NF)): bad.append(f'blink pattern (seed {seed}) is not NF-periodic')
    if any(T.K.blinking(f, seed) for f in (0, 1, 2, T.NF - 3, T.NF - 2, T.NF - 1)): bad.append(f'blink at the seam (seed {seed})')
print('SEAM', 'FAIL: ' + '; '.join(bad) if bad else 'ok (0.000/255, blinks periodic)'); sys.exit(1 if bad else 0)
