"""Safe-zone gate for Perfect Trip: every bubble (pop included), stamp and title text inside x 60-960, y 210-1600, per frame."""
import sys, os, json, math, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
mod = os.path.join(HERE, 'render.py'); out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'safe.json'); step = 1
spec = importlib.util.spec_from_file_location('trip_mod', mod); T = importlib.util.module_from_spec(spec); sys.modules['trip_mod'] = T; spec.loader.exec_module(T)
import cairo
REC = []; cur = [0]
import tails as TLm
STAMPS = {}
orig_s = T.P.stamp
def stamp(c, place, x=None, y=570, k=1.0, op=.85):
    name, col, rot, x0 = T.P.STAMP[place]; x = x0 if x is None else x
    sc = 1 + .5 * (1 - k); cs, sn = abs(math.cos(rot)), abs(math.sin(rot))
    hw = (130 * cs + 62 * sn) * sc; hh = (130 * sn + 62 * cs) * sc
    STAMPS[place] = (x - hw, y - hh, x + hw, y + hh, 'k=%.2f' % k)
    return orig_s(c, place, x=x, y=y, k=k, op=op)
T.P.stamp = stamp
orig_kb = T.kenburns
def kb(c, place, r, d, f, **kw):
    orig_kb(c, place, r, d, f, **kw)
    if place in STAMPS:
        x1, y1, x2, y2, _ = STAMPS[place]; t = T.ss(T.cl(r / d)); z = 1 + .09 * t; tx, ty = T.KB_TARGET[place]
        REC.append((cur[0], 'stamp:' + place, tx + z * (x1 - tx), ty + z * (y1 - ty), tx + z * (x2 - tx), ty + z * (y2 - ty)))
T.kenburns = kb
for f in range(0, T.NF, step):
    cur[0] = f; TLm.BOXES.clear(); T.draw(f)
    for lab, x1, y1, x2, y2 in TLm.BOXES: REC.append((f, 'bubble:' + lab, x1, y1, x2, y2))
bad = {}
for f, nm, x1, y1, x2, y2 in REC:
    v = []
    if x1 < 60: v.append(('left', round(60 - x1)))
    if x2 > 960: v.append(('right', round(x2 - 960)))
    if y1 < 210: v.append(('top', round(210 - y1)))
    if y2 > 1600: v.append(('bottom', round(y2 - 1600)))
    if v: bad.setdefault(nm, []).append((f, v, round(x1), round(x2), round(y1), round(y2)))
res = {nm: dict(first=b[0][0], last=b[-1][0], n=len(b), worst=max(max(a for _, a in v[1]) for v in b), sample=b[0]) for nm, b in bad.items()}
json.dump(res, open(out, 'w'), indent=1, default=str); print(len(REC), 'boxes;', len(res), 'items outside the zone'); print(json.dumps(res, indent=1, default=str)[:3000])
sys.exit(1 if res else 0)
