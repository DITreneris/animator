"""Safe-zone gate: every text box (bubbles, chat messages, the receipt) inside x 60-960, y 210-1600 in every frame,
plus every bubble tail tip. Exits 1 on any miss. Usage: python3 safe.py"""
import sys, math
sys.argv = ['film.py']
import film as F
bad = 0; n = 0
for f in range(F.NF):
    F.draw(f)
    for lab, x0, y0, x1, y1 in F.BOXES:
        n += 1
        if x0 < F.SAFE['x0'] or x1 > F.SAFE['x1'] or y0 < F.SAFE['y0'] or y1 > F.SAFE['y1']:
            bad += 1; print(f'FAIL f{f} {lab!r}: ({x0:.0f},{y0:.0f})-({x1:.0f},{y1:.0f})')
print(f'{n} boxes checked, {bad} outside the safe area'); print('SAFE PASS' if not bad else 'SAFE FAIL'); sys.exit(1 if bad else 0)
