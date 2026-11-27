"""Every Failure - safe-zone gate (the apps' dead zones): every text box inside x 60-960, y 210-1600 on every frame,
measured where it is drawn (words on stones and the sign, bubbles with their pop, the series bar), the camera's push included.
Exits 1 if anything is outside. Usage: python3 safe.py [report.json]"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); os.chdir(HERE)
import frame0 as F, keyposes as KP, animatic as AN, tails as TL
Z = dict(x0=60, x1=960, y0=210, y1=1600)
REC = []

def wrap_txt(mod):
    orig = mod.txt
    def txt(c, s, x, y, size, *a, **k):
        if s and not (c.get_target().get_width() == 1080 and c.get_target().get_height() == 420):   # words inside the bar surface: the bar box covers them
            c.save(); c.select_font_face('Lilita One'); c.set_font_size(size); w = c.text_extents(s).width; c.restore()
            al = k.get('align', 'c'); x0 = x - w / 2 if al == 'c' else (x if al == 'l' else x - w)
            pts = [c.user_to_device(px, py) for px, py in ((x0, y - size * .4), (x0 + w, y - size * .4), (x0, y + size * .4), (x0 + w, y + size * .4))]
            REC.append(('text:' + s, min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts)))
        return orig(c, s, x, y, size, *a, **k)
    mod.txt = txt
for m in (F, KP): wrap_txt(m)

orig_bar, orig_pop = F.topbar, KP.capsule_pop
def bar(c, label, *a, **k): REC.append(('bar:' + label, 64, 218.5, 956, 222 + 142 * F.BARK)); return orig_bar(c, label, *a, **k)
def pop(c, label, k=1.0): REC.append(('bar:' + label, 64, 218.5, 956, 222 + 142 * F.BARK)); return orig_pop(c, label, k)
F.topbar = bar; KP.capsule_pop = pop; AN.capsule_pop = pop

bad = {}
n = 0
for f in range(AN.NF):
    REC.clear(); TL.BOXES.clear(); AN.draw(f)
    boxes = REC[:] + [('bubble:' + l, *b) for l, *b in TL.BOXES]
    of = AN.old_of(f) if AN.M1 <= f < 525 else f                       # the montage re-timed the middle: the push lives in old frames
    if 360 <= of < 420:                                                  # the medium shot: everything but the bar was drawn before the push
        z, cx, cy, ox, oy = 1.25, 540, 1000, 415, AN.GL - 360
        boxes = [(l, cx + (a - ox) * z, cy + (b - oy) * z, cx + (c_ - ox) * z, cy + (d - oy) * z) if not l.startswith('bar') else (l, a, b, c_, d) for l, a, b, c_, d in boxes]
    for l, a, b, c_, d in boxes:
        n += 1
        if c_ < 0 or a > 1080 or d < 0 or b > 1920: continue           # off screen entirely (a push crops it): not shown
        if a < Z['x0'] or c_ > Z['x1'] or b < Z['y0'] or d > Z['y1']:
            bad.setdefault(l, []).append((f, round(a), round(b), round(c_), round(d)))
print(f'{n} boxes; {len(bad)} items outside the zone')
for l, v in bad.items(): print(f'  {l}: frames {v[0][0]}-{v[-1][0]} ({len(v)}), e.g. {v[0][1:]}')
if len(sys.argv) > 1: json.dump(bad, open(sys.argv[1], 'w'))
sys.exit(1 if bad else 0)
