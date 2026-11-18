"""Make It Original v5.2: v5.1 (imported, unchanged) plus the rejection made visible without words, and Tomas's new
drummer take. In 1986 the drummer has laid her sticks down on the drum: she has stopped playing for him. In 2026,
while he waves MY AI's tune away, his other hand turns its screen away from him. The drummer's line is the
18 Nov take ("Play something we KNOW."), 0.75 semitone down (1.5 turned "play" into "place" for the recognizer).
python3 film.py keys | t ... | seam | (no args: full render; needs fin.wav from mix52.py)"""
import sys, os, math, importlib.util
import numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location('film5', os.path.join(HERE, '..', 'v5', 'film.py'))
F5 = importlib.util.module_from_spec(_spec); _cwd = os.getcwd(); _spec.loader.exec_module(F5); os.chdir(_cwd)
F4, A, G, D, FPS, W, H, NF = F5.F4, F5.A, F5.G, F5.D, F5.FPS, F5.W, F5.H, F5.NF
import cast
from cast import rr, fs, ell, limb, hx, cl, lerp, ss, INK, SKIN, NAVY

# ---- the new drummer take: its lip flap ----
x, sr = sf.read(os.path.join(HERE, 'drum_v52.wav')); hop = sr // FPS
r = np.array([np.sqrt((x[i * hop:(i + 1) * hop] ** 2).mean()) for i in range(len(x) // hop)]); r /= r.max() + 1e-9
A.ENV['drum'][:] = 0; f0 = int(round(G['drum'] * FPS)); A.ENV['drum'][f0:f0 + len(r)] = r[:len(A.ENV['drum']) - f0]
DRUM_LEN = len(x) / sr

# ---- 1986: her sticks lie on the drum; she has stopped playing for him ----
_db = A.drummer_body
def drummer_body(c, *a, **k):
    if k.get('wave_k') is not None: k['sticks'] = False
    _db(c, *a, **k)
A.drummer_body = drummer_body
_fg = A.drums_foreground
def drums_foreground(c, y):
    _fg(c, y)
    for dx, rot in ((0, .08), (26, -.05)):                                    # two sticks resting across the floor tom
        c.save(); c.translate(720 + dx, y + 105); c.rotate(rot)
        rr(c, -120, -9, 240, 18, 9); fs(c, hx('d9a86c'), 5); ell(c, 118, 0, 12, 11); fs(c, hx('f3dcb5'), 4); c.restore()
A.drums_foreground = drums_foreground

# ---- 2026: his free hand turns MY AI's screen away while he waves its tune off ----
_s15 = F4.LATE[15]
def s15(c, t, f):
    _s15(c, t, f)
    tg = t + D
    if F5.FLASH[0] <= tg < F5.FLASH[1]: return
    k = cl((tg - G['wave26']) / 1.4)
    turn = ss((k - .28) / .3)                                              # 0: facing him, 1: turned away
    cx, top, w0, h0 = 880, 860, 300, 210
    w = w0 * max(.06, abs(math.cos(turn * math.pi * .8)))
    rr(c, cx - 16, top + h0, 32, 120, 8); fs(c, hx('2a2f3a'))             # the stand
    rr(c, cx - w / 2, top, w, h0, 16); fs(c, hx('1b2030'), 9)
    if turn < .55:
        c.save(); c.rectangle(cx - w / 2 + 12, top + 12, w - 24, h0 - 24); c.clip()
        c.translate(cx, top + h0 / 2); c.scale(w / w0, 1); c.translate(-cx, -(top + h0 / 2))
        cast.ai_art(c, cx - w0 / 2 + 12, top + 12, w0 - 24, h0 - 24, A.E['ai'] + 1.0, A.E['ai']); c.restore()
    else:
        rr(c, cx - w / 2 + 14, top + 14, max(4, w - 28), h0 - 28, 10); fs(c, hx('3a4152'))   # its blank back
    if .15 < k < .95:                                                       # his hand on the screen's edge, pushing it round
        hx_, hy_ = cx - w / 2 - 6, top + h0 * .55
        limb(c, [(690, 1190), (740, 1110), (hx_, hy_)], 70, NAVY); ell(c, hx_, hy_, 34, 30); fs(c, SKIN, 6)
F4.LATE[15] = s15

def subs(c, t, year):
    year = 1986 if t < G['ff1'] + .2 else 2016 if t < G['ff2'] + .2 else 2026
    if F5.FLASH[0] <= t < F5.FLASH[1]: year = 1986
    cast.topbar_a(c, year)
    F5.sub(c, t, G['drum'], G['drum'] + DRUM_LEN, 'PLAY SOMETHING WE KNOW.')
    F5.sub(c, t, G['ask'], G['ask'] + 1.7, 'MAKE SOMETHING|COMPLETELY ORIGINAL.')
    F5.sub(c, t, G['know'], G['know'] + 1.12, 'PLAY SOMETHING WE KNOW.')
    F5.sub(c, t, G['orig'], G['orig'] + 1.2, "NOW THAT'S ORIGINAL!")
F4.subs = subs

if __name__ == '__main__':
    a = sys.argv[1:]
    os.chdir(HERE); os.makedirs('keys', exist_ok=True)
    if a and a[0] == 'keys': F4.keys()
    elif a and a[0] == 'seam':
        from PIL import Image
        im = Image.new('RGB', (1080, 960), 'white')
        for i, fr in enumerate((NF - 1, 0)): im.paste(F4.frame_img(fr).resize((540, 960)), (i * 540, 0))
        im.save('keys/seam.png'); print('seam ok')
    elif a:
        for v in a: fr = int(round(float(v) * FPS)); F4.draw(fr).write_to_png(f'chk_{fr:03d}.png')
    else: F4.render('make_it_original_v52.mp4')
