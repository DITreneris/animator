"""Measures every frame of Thank You v2 against the prop timeline in CONCEPT.md: where the toaster and its ray are drawn
(screen px), where HARV is, and how far each speech tail ends from its speaker. Prints one line per shot.
python3 measure.py"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import film as F
seen = {}; cur = [None]
def spy(name, fn, key):
    def w(c, x, y, s, *a, **k):
        d = c.user_to_device(x, y); seen.setdefault((cur[0], name), []).append((round(d[0]), round(d[1]), round(s * c.get_matrix().xx, 2)))
        return fn(c, x, y, s, *a, **k)
    return w
F.R.toaster = spy('toaster', F.R.toaster, 'toaster')
_rb = F.Vv.robot
def boss(c, x, y, s, boss=False, **k):
    if boss: d = c.user_to_device(x, y); seen.setdefault((cur[0], 'HARV'), []).append((round(d[0]), round(d[1]), round(s * c.get_matrix().xx, 2)))
    return _rb(c, x, y, s, boss=boss, **k)
F.Vv.robot = boss
tails = {}
_b, _bs = F.bubble, F.bubble_side
def tb(c, lines, size, tip, *a, **k): tails.setdefault(cur[0], set()).add((round(tip[0]), round(tip[1]))); return _b(c, lines, size, tip, *a, **k)
def tbs(c, lines, size, tip, *a, **k): tails.setdefault(cur[0], set()).add((round(tip[0]), round(tip[1]))); return _bs(c, lines, size, tip, *a, **k)
F.bubble, F.bubble_side = tb, tbs
for f in range(F.NF):
    for n, d in F.SHOTS:
        if F.START[n] <= f < F.START[n] + d: cur[0] = n
    F.draw(f)
for n, d in F.SHOTS:
    row = []
    for what in ('toaster', 'HARV'):
        v = seen.get((n, what))
        if v: xs = [p[0] for p in v]; ys = [p[1] for p in v]; row.append(f'{what} x {min(xs)}..{max(xs)} y {min(ys)}..{max(ys)}')
    t = tails.get(n)
    if t: row.append('tail tips ' + ' '.join(f'{x},{y}' for x, y in sorted(t)[:2]) + (' ...' if len(t) > 2 else ''))
    print(f'{n:2} ' + ' | '.join(row or ['-']))
x0 = seen.get(('A', 'toaster'))[0]; x1 = seen.get(('K', 'toaster'))[-1]
print('toaster frame 0 vs last frame:', x0, x1)
