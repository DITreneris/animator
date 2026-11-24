#!/usr/bin/env python3
"""Continuity gate: per-frame change between neighbours. A spike that is not a declared cut or impact fails.
usage: continuity.py video.mp4 --cuts 36,54,... (frames where a cut/impact is allowed)   exit 1 on any undeclared spike"""
import sys, subprocess, numpy as np
v = sys.argv[1]; allowed = set()
if '--cuts' in sys.argv:
    allowed = {int(x) for x in sys.argv[sys.argv.index('--cuts') + 1].split(',') if x}
W, H = 270, 480
p = subprocess.run(['ffmpeg', '-v', 'error', '-i', v, '-vf', f'scale={W}:{H}', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'], capture_output=True).stdout
a = np.frombuffer(p, np.uint8).reshape(-1, H, W).astype(np.float32)
d = np.abs(np.diff(a, axis=0)).mean(axis=(1, 2))          # d[i] = change from frame i to i+1
med = np.median(d); thr = max(med * 4, 3.0)
bad = [i + 1 for i, x in enumerate(d) if x > thr and (i + 1) not in allowed and (i + 1) not in {j + 1 for j in allowed}]
print(f'frames {len(a)}  median {med:.2f}  threshold {thr:.2f}')
print('spikes:', [(i + 1, round(float(d[i]), 1)) for i, x in enumerate(d) if x > thr])
print('UNDECLARED:', bad)
sys.exit(1 if bad else 0)
