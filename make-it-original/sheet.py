"""Character sheets: sheet_cast.png (cast, the wave-off, cat, robot, props) and sheet_faces.png (expressions)."""
import cairo, sys
from kit import *
BG = hx('f6efe0')

def label(c, t, x, y, size=40):
    txt(c, t, x, y, size, fill=INK, lw=0)

def bust(c, x, y, s, era, expr, f=7, rot=0, arm_k=None, side=1, who='hoodyz'):
    shadow(c, x, y + 330 * s, 120 * s)
    if who == 'hoodyz': shl, shr = hoodie(c, x, y + 160 * s, 1.2 * s)
    else: shl, shr = vest(c, x, y + 160 * s, 1.2 * s)
    sleeve = NAVY if who == 'hoodyz' else SKIN
    if arm_k is not None:
        arm(c, waveoff(shr if side > 0 else shl, s * 1.2, arm_k, side), s, sleeve, flick=1.0)
    if who == 'hoodyz': hoodyz_head(c, x, y, s * 1.08, era, expr, f, rot, blink=False)
    else: drummer_head(c, x, y, s * 1.08, expr, f, rot)

def cast():
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(S)
    c.set_source_rgb(*BG); c.paint(); topbar(c, 1986)
    label(c, 'HOODYZ AT THREE AGES  (same hoodie, head in the same place)', 540, 405, 32)
    for x, era, ex in ((190, 1986, 'hopeful'), (540, 2016, 'shock'), (890, 2026, 'smug')):
        bust(c, x, 580, .58, era, ex); label(c, str(era), x, 838, 44)
    label(c, 'THE WAVE-OFF  (same arm, height, timing)', 540, 905, 32)
    bust(c, 220, 1050, .56, None, 'dismissive', rot=-.12, arm_k=.6, side=1, who='drummer'); label(c, 'Drummer, 1986', 220, 1290, 36)
    bust(c, 690, 1050, .56, 2026, 'dismissive', rot=-.12, arm_k=.6, side=1); label(c, 'Hoodyz, 2026', 690, 1290, 36)
    label(c, 'THE CAT  (orange tabby)', 720, 1345, 32)
    guitar(c, 300, 1490, .62, rot=0)
    cat(c, 330, 1470, .62, 'walk', phase=.5, paw_down=1, f=7)
    label(c, '2016: walks the guitar', 300, 1590, 34)
    cat(c, 830, 1530, .62, 'sleep', old=True, f=7)
    label(c, '2026: old, asleep', 830, 1590, 34)
    label(c, 'ROBOT FACES  +  PROPS', 540, 1650, 34)
    for i, (em, eye) in enumerate((('proud', (0, 0)), (None, (-16, 6)), ('sideeye', (0, 0)))):
        robot(c, 130 + i * 200, 1760, .5, em, eye, f=7)
        label(c, ['pride', 'glance', 'side-eye'][i], 130 + i * 200, 1880, 30)
    cassette(c, 740, 1760, .6); drumkit(c, 950, 1860, .26)
    return S

def faces():
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(S)
    c.set_source_rgb(*BG); c.paint(); topbar(c, 2026)
    rows = [(1986, ['hopeful', 'sheepish']), (2016, ['calm', 'shock', 'deadpan']),
            (2026, ['confident', 'polite', 'dismissive', 'smug'])]
    y = 570
    for era, exs in rows:
        label(c, str(era), 540, y - 150, 46)
        n = len(exs)
        for i, ex in enumerate(exs):
            x = 540 + (i - (n - 1) / 2) * 250
            hoodyz_head(c, x, y, .62, era, ex, 7, blink=False); label(c, ex, x, y + 140, 34)
        y += 420
    label(c, 'Drummer: deadpan / dismissive', 540, y - 150, 40)
    for i, ex in enumerate(('deadpan', 'dismissive')):
        drummer_head(c, 400 + i * 280, y - 10, .55, ex, 7)
    return S

if __name__ == '__main__':
    cast().write_to_png('sheet_cast.png'); faces().write_to_png('sheet_faces.png')
    from PIL import Image
    for n in ('sheet_cast', 'sheet_faces'):
        Image.open(n + '.png').resize((540, 960), Image.LANCZOS).save(n + '_phone.png')
    print('ok')
