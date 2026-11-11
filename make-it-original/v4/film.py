"""Make It Original v4: the cat returns (19 shots, about 19.9 s).
Reuses version A (../v3) for 1986 and 2026, shifted by D seconds, and adds 2016: the lazy cat, CAT: 10M, and
Hoodyz picturing the cat on his stadium stage. The ending: his joy, the cat on the monitor, the robot's turn, the old cat's yawn.
python3 film.py keys | t ... | lowres | (no args: full render; needs fin.wav from mix4.py)"""
import sys, os, math, subprocess
import numpy as np, cairo, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'v3')); sys.path.insert(0, os.path.join(HERE, '..'))
import cast, shots as A
from cast import *
from timeline import RIFF, ONSETS, S16, FPS

D = 5.8                                   # 2026 starts this much later than in version A
R86 = A.R86
G = dict(wave86=1.6, drum=1.65, ff1=3.7, frag=4.2, views3=4.75, land=5.1, cat16=5.6, views10=7.45, catstad=8.0, ff2=9.5,
         ask=A.E['ask'] + D, ai=A.E['ai'] + D, recoil=A.E['recoil'] + D, wave26=A.E['wave26'] + D, know=A.E['know'] + D,
         glance=A.E['glance'] + D, demo=A.E['demo'] + D, bloom=A.E['bloom'] + D, orig=A.E['orig'] + D, back=A.E['back'] + D,
         turn=18.75, yawn=19.3)
END = G['demo'] + 4.0 - R86
NF = int(round(END * FPS))
SHOTS = [(1, 0.0, 0.8), (2, 0.8, 1.6), (3, 1.6, 3.1), (4, 3.1, 3.7), ('ff1', 3.7, 4.1),
         (5, 4.1, 5.1), (6, 5.1, 5.5), (7, 5.5, 7.3), (8, 7.3, 8.0), (9, 8.0, 9.0), (10, 9.0, 9.5), ('ff2', 9.5, 9.9),
         (11, 9.9, 10.4), (12, 10.4, 12.2), (13, 12.2, 12.7), (14, 12.7, 14.3), (15, 14.3, 15.5),
         (16, 15.5, 16.0), (17, 16.0, 16.8), (18, 16.8, 18.1), (19, 18.1, END)]
KEY_T = {1: .5, 2: 1.45, 3: 2.4, 4: 3.6, 5: 4.95, 6: 5.35, 7: 6.35, 8: 7.8, 9: 8.55, 10: 9.3, 11: 10.2, 12: 11.1, 13: 12.6,
         14: 13.7, 15: 14.8, 16: 15.85, 17: 16.4, 18: 17.42, 19: 19.55}
NAMES = {1: 'stadium (his fantasy)', 2: 'stadium, close', 3: 'garage: the drummer', 4: 'he deflates', 5: '2016: 3 VIEWS',
         6: 'guitar lands', 7: 'the lazy paw', 8: 'CAT: 10M', 9: 'the cat on HIS stage', 10: 'deadpan', 11: 'wide 2026',
         12: 'lean-in', 13: 'robot ready', 14: 'recoil', 15: 'his gesture', 16: 'robot eyes the cat', 17: 'the cat video',
         18: 'his stadium returns', 19: 'smug; robot turns; cat yawns'}

# ---- lip flap on the v4 timeline (version A's shot functions read A.ENV by global frame) ----
def _env():
    env = {k: np.zeros(NF + 60) for k in ('drum', 'hoodyz')}
    for n, t, who in (('drum', G['drum'], 'drum'), ('ask', G['ask'], 'hoodyz'), ('know', G['know'], 'hoodyz'), ('orig', G['orig'], 'hoodyz')):
        x, sr = sf.read(os.path.join(HERE, '..', 'vo', n + '.wav')); hop = sr // FPS
        r = np.array([np.sqrt((x[i * hop:(i + 1) * hop] ** 2).mean()) for i in range(len(x) // hop)]); r /= r.max() + 1e-9
        f0 = int(round(t * FPS))
        for i, v in enumerate(r): env[who][f0 + i] = max(env[who][f0 + i], v)
    return env
A.ENV = _env()

# ---- the old cat on the 2026 desk ----
OLDCAT = (930, 1262, .7)
def old_cat(c, yawn=0.0, f=0):
    x, gy, s = OLDCAT
    cat(c, x, gy, s, 'sleep', old=True, f=f)
    if yawn > 0:
        mx, my = x - 117 * s, gy - 29 * s
        ell(c, mx, my, (14 * yawn + 2) * s * 1.6, (20 * yawn + 2) * s * 1.6); fs(c, hx('7a2230'), 5)
        ell(c, mx, my + 6 * s, 8 * yawn * s * 1.6, 7 * yawn * s * 1.6); c.set_source_rgb(*hx('ff8fa6')); c.fill()
YAWN = 0.0
A.TAPE = (745, 1240, .32)
_desk = A.desk26
def desk_with_cat(c, t, f, content='off'):
    _desk(c, t, f, content); old_cat(c, YAWN, f)
A.desk26 = desk_with_cat

def paw_motif(c, t, t0, x0, y0, sc=1.0, life=2.0):
    for i, ((m, _), on) in enumerate(zip(RIFF, ONSETS)):
        dt = t - (t0 + on)
        if dt < 0 or dt > life: continue
        a = cl(dt / .08) * cl((life - dt) / .5)
        x = x0 + i * 62 * sc; y = y0 - (m - 60) * 16 * sc - dt * 40 * sc
        A.note_glyph(c, x, y, sc, YEL, a)
        if a > .5:
            for px, py, r in ((-34, 20, 9), (-24, 6, 6), (-40, 6, 6), (-46, 18, 5), (-20, 18, 5)):
                ell(c, x + px * sc, y + py * sc, r * sc, r * sc); c.set_source_rgb(*INK); c.fill()

# ---- 2016 ----
HX, HGY, HS = A.HX, A.HGY, A.HS
def room16(c, t=0):
    c.set_source_rgb(*hx('ebdfc9')); c.paint()
    c.rectangle(0, 1500, W, H); c.set_source_rgb(*hx('b49a78')); c.fill()
    rr(c, 640, 420, 300, 220, 10); fs(c, hx('9fd0ea'), 8)
    c.move_to(790, 420); c.line_to(790, 640); c.move_to(640, 530); c.line_to(940, 530); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    day = cairo.LinearGradient(790, 640, 600, 1500); day.add_color_stop_rgba(0, 1, 1, .9, .25); day.add_color_stop_rgba(1, 1, 1, .9, 0)
    c.set_source(day); c.paint()
    rr(c, 100, 470, 220, 160, 10); fs(c, hx('1b1b2a'), 6); txt(c, 'THE LOUD', 210, 540, 38, fill=hx('c88a90'), lw=0)
    rr(c, 40, 1220, 160, 290, 10); fs(c, hx('8a6a4a')); cassette(c, 120, 1200, .34)
    ell(c, 120, 1100, 50, 70); fs(c, hx('5fae6a'), 6)
def couch16(c):
    rr(c, 560, 1320, 480, 120, 40); fs(c, hx('3f7a6a')); rr(c, 530, 1400, 540, 150, 40); fs(c, hx('4f8f7c'))

def s5(c, t, f):   # he plays three notes to his phone: 3 VIEWS
    c.save(); A.cam(c, 1.25, 520, 1180, 540, 1120); room16(c, t); couch16(c)
    c.move_to(660, 1500); c.line_to(660, 1240); c.set_source_rgb(*INK); c.set_line_width(8); c.stroke()
    rr(c, 620, 1120, 80, 140, 12); fs(c, INK, 0); rr(c, 628, 1128, 64, 124, 8); c.set_source_rgb(*hx('6fd0ff')); c.fill()
    hoodyz(c, HX, HGY, HS, 2016, 'hopeful', 'play' if t < G['frag'] + .7 else 'rest', f, strum=A.strum_at(t, G['frag']))
    c.restore()
    for i in range(3):
        dt = t - (G['frag'] + ONSETS[i])
        if 0 <= dt < 1.2: A.note_glyph(c, 520 + i * 70, 760 - (RIFF[i][0] - 60) * 18 - dt * 40, 1.0, YEL, cl(dt / .08) * cl((1.2 - dt) / .4))
    if t >= G['views3']: views_badge(c, 760, 860, '3 VIEWS', (t - G['views3']) / .25)

def s6(c, t, f):   # the guitar lands on the couch
    c.set_source_rgb(*hx('ebdfc9')); c.paint()
    rr(c, -40, 1000, 1160, 260, 60); fs(c, hx('3f7a6a')); rr(c, -60, 1200, 1200, 420, 60); fs(c, hx('4f8f7c'))
    u = cl((t - G['land']) / .14); y = lerp(300, 1250, u * u); t1 = G['land'] + .14
    if u >= 1: y = 1250 - abs(math.sin((t - t1) * 18)) * 30 * math.exp(-(t - t1) * 10)
    guitar(c, 380, y, 1.2, rot=lerp(-.6, 0, u))
    if t1 <= t < t1 + .16:
        for i in range(5):
            a = math.pi + i * math.pi / 4; c.move_to(380 + math.cos(a) * 200, 1300 + math.sin(a) * 90); c.line_to(380 + math.cos(a) * 280, 1300 + math.sin(a) * 130)
            c.set_source_rgb(*INK); c.set_line_width(8); c.stroke()

def s7(c, t, f):   # the lazy cat: one paw per note; the notes land where his did in shot 5
    c.set_source_rgb(*hx('ebdfc9')); c.paint(); rr(c, -60, 1000, 1200, 300, 60); fs(c, hx('3f7a6a')); rr(c, -60, 1180, 1200, 760, 60); fs(c, hx('4f8f7c'))
    guitar(c, 300, 1330, 2.0, rot=0)
    tc = t - G['cat16']; paw = 0
    for o in ONSETS:
        d = tc - o
        if -.08 <= d < 0: paw = max(paw, 1 + d / .08)
        elif 0 <= d < .15: paw = max(paw, 1 - d / .15 * .7)
    tip = lazy_cat(c, 760, 1300, 2.0, paw, 0, f)
    if any(0 <= tc - o < .08 for o in ONSETS): ell(c, tip[0], 1330, 80, 18); c.set_source_rgba(*YEL, .85); c.fill()
    paw_motif(c, t, G['cat16'], 520, 760 + 0, 70 / 62 * 1.0, life=1.6)

def phone_face(c, t, f, expr, pop=None):
    room16(c, t); c.save(); A.cam(c, 1.75, HX, 1040, 540, 900)
    hoodyz(c, HX, HGY, HS, 2016, expr, 'phone', f)
    c.restore()
    views_badge(c, 540, 1460, 'CAT: 10M', 1 if pop is None else pop, col=YEL, size=84)
def s8(c, t, f): phone_face(c, t, f, 'shock', (t - G['views10']) / .25 if t >= G['views10'] else 0.0)
def s10(c, t, f): phone_face(c, t, f, 'deadpan')

def s9(c, t, f):   # he pictures it: the cat on HIS stage, yawning at a roaring crowd
    k = lerp(1.0, 1.06, (t - 8.0)); A.cam(c, k, 540, 1060, 540, 1060)
    stadium(c, t, wide=True, flash=.6 * abs(math.sin(t * 9)))
    spot = cairo.RadialGradient(540, 1380, 40, 540, 1380, 420); spot.add_color_stop_rgba(0, 1, 1, .9, .5); spot.add_color_stop_rgba(1, 1, 1, .9, 0)
    c.set_source(spot); c.paint()
    rr(c, 330, 520, 420, 190, 26); fs(c, hx('0b0d12'), 10, WHITE); txt(c, '10M', 540, 615, 130, fill=YEL, lw=0)      # the big screen
    yawn = math.sin(math.pi * cl((t - 8.25) / .6)) if t > 8.25 else 0
    lazy_cat(c, 560, 1440, 2.2, 0, yawn, f)
    crowd(c, t, 1600); dream_edge(c)

# ---- 2026 overrides ----
def s16(c, t, f):  # (local time) the robot's eyes slide to the old cat
    A.cam(c, 2.0, 790, 1150, 540, 1000)
    A.world26(c, t, f, emote='side' if t > 9.85 else None, eye=(-14, 0), him=False)

def s17(c, t, f):  # (local) the monitor plays the cat video
    c.set_source_rgb(*hx('1b2030')); c.paint()
    k = lerp(1.0, 1.06, (t - 10.2) / .8); c.translate(540, 1000); c.scale(k, k); c.translate(-540, -1000)
    monitor(c, 110, 640, 860, 640, 'cat', t, f)
    paw_motif(c, t, A.E['demo'], 240, 700, 1.3)

def s19(c, t, f):  # (local) office: smug; the cat on the monitor; the robot turns to us; the old cat yawns
    global YAWN
    tg = t + D
    tu = ss((tg - G['turn'] + .1) / .4)
    A.cam(c, lerp(1.22, 1.6, tu), lerp(600, 742, tu), lerp(1100, 1150, tu), 540, 1010)      # stays inside the set's right edge
    bob = .06 * math.sin((t - 12.2) / .5 * math.pi * 2)
    turn = ss((tg - G['turn']) / .25)
    YAWN = math.sin(math.pi * cl((tg - G['yawn']) / .55)) if tg > G['yawn'] else 0
    A.world26(c, t, f, content='cat', hpose='air', hexpr='smug', hlean=-.05, hrot=-.08 + bob,
              emote='sideeye' if turn > .5 else None, eye=(-22, 0), turn=turn)
    YAWN = 0
    paw_motif(c, t, A.E['demo'] + 2.0, 560, 980, 1.0)

OLD = {1: A.s1, 2: A.s2, 3: A.s3, 4: A.s4}                                            # global time
NEW16 = {5: s5, 6: s6, 7: s7, 8: s8, 9: s9, 10: s10}                                   # global time
LATE = {11: A.s9, 12: A.s10, 13: A.s11, 14: A.s12, 15: A.s13, 16: s16, 17: s17, 18: A.s16, 19: s19}   # local time (t - D)

def subs(c, t, year):
    topbar_a(c, year)
    A.sub(c, t, G['drum'], G['drum'] + 1.4, 'PLAY SOMETHING WE KNOW.')
    A.sub(c, t, G['ask'], G['ask'] + 1.7, 'MAKE SOMETHING|COMPLETELY ORIGINAL.')
    A.sub(c, t, G['know'], G['know'] + 1.12, 'PLAY SOMETHING WE KNOW.')
    A.sub(c, t, G['orig'], END, "NOW THAT'S ORIGINAL!")

def draw(f):
    t = f / FPS
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(s)
    c.set_source_rgb(0, 0, 0); c.paint()
    shot = next((x for x in SHOTS if x[1] <= t < x[2]), SHOTS[-1]); n = shot[0]
    year = 1986 if t < G['ff1'] else 2016 if t < G['ff2'] else 2026
    c.save()
    if n == 'ff1':
        c.save(); c.translate(-lerp(0, 60, (t - 3.7) / .4), 0); s5(c, 4.1, f); c.restore(); u = (t - 3.7) / .4
        A.ff(c, t, 3.7, 4.1); year = int(lerp(1986, 2016, ss(u)))
    elif n == 'ff2':
        c.save(); c.translate(-lerp(0, 60, (t - 9.5) / .4), 0); A.s9(c, 4.1, f); c.restore(); u = (t - 9.5) / .4
        A.ff(c, t, 9.5, 9.9); year = int(lerp(2016, 2026, ss(u)))
    elif n in OLD: OLD[n](c, t, f)
    elif n in NEW16: NEW16[n](c, t, f)
    else: LATE[n](c, t - D, f)
    c.restore()
    subs(c, t, year)
    return s

def frame_img(fr):
    from PIL import Image
    return Image.frombuffer('RGBA', (W, H), bytes(draw(fr).get_data()), 'raw', 'BGRA', 0, 1).convert('RGB')

def keys():
    from PIL import Image, ImageDraw
    os.makedirs('keys', exist_ok=True); tiles = []
    for n, tk in KEY_T.items():
        fr = int(round(tk * FPS)); im = frame_img(fr); im.save(f'keys/shot{n:02d}.png'); tiles.append((n, im, fr))
    cols = 7; rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * 300, rows * 580), 'white'); d = ImageDraw.Draw(sheet)
    for i, (n, im, fr) in enumerate(tiles):
        x, y = (i % cols) * 300, (i // cols) * 580; sheet.paste(im.resize((300, 533)), (x, y))
        d.text((x + 6, y + 540), f'{n}. {NAMES[n]}  ({fr / FPS:.1f}s)', fill='black')
    sheet.save('keys/key_poses.png')
    for a_t, b_t, lab in ((G['wave86'] + .8, G['wave26'] + .8, 'gesture'), (R86 + ONSETS[-1] + .15, G['demo'] + ONSETS[-1] + .15, 'performance')):
        Image.blend(frame_img(int(round(a_t * FPS))), frame_img(int(round(b_t * FPS))), .5).resize((540, 960)).save(f'keys/overlay_{lab}.png')
    print('keys ok', len(tiles))

def render(path, scale=1.0, crf=16):
    vf = [] if scale == 1 else ['-vf', f'scale={int(W * scale)}:{int(H * scale)}']
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-i', 'fin.wav', *vf, '-c:v', 'libx264', '-preset', 'veryfast', '-crf', str(crf), '-pix_fmt', 'yuv420p',
                          '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709',
                          '-c:a', 'aac', '-b:a', '192k', '-shortest', path + '.tmp.mp4'], stdin=subprocess.PIPE)
    for fr in range(NF): p.stdin.write(bytes(draw(fr).get_data()))
    p.stdin.close(); assert p.wait() == 0
    os.replace(path + '.tmp.mp4', path); print(path, 'frames', NF)

if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == 'keys': keys()
    elif a and a[0] == 'lowres': render('make_it_original_v4_timing.mp4', .5, 23)
    elif a:
        for x in a: fr = int(round(float(x) * FPS)); draw(fr).write_to_png(f'chk_{fr:03d}.png')
    else: render('make_it_original_v4.mp4')
