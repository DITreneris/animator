"""Make It Original, version A (final): 13 shots, about 14.1 s.
Story: the stadium is his fantasy; the drummer's line cuts to the real garage. In 2026 he rejects the AI's original
with the drummer's exact gesture, the robot glances at his old demo cassette and plays his riff, the stadium comes back,
"Now THAT'S original!", and the robot turns to us.
python3 shots.py keys | t ... | lowres | (no args: full render, needs fin.wav)"""
import sys, os, math, subprocess
import numpy as np, cairo, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__))
import cast
from cast import *
sys.path.insert(0, os.path.join(HERE, '..'))
from timeline import RIFF, AI_TUNE, ONSETS, AI_ONSETS, S16, FPS

# ---------------- timeline (seconds) ----------------
R86 = 0.067
E = dict(wave86=1.6, drum=1.65, ff=3.7, ask=4.7, ai=6.95, recoil=7.6, wave26=8.5, know=8.55, glance=9.75,
         demo=10.2, bloom=11.0, orig=11.5, back=12.3, turn=13.05)
END = E['demo'] + 2 * 2.0 - R86              # cut where a third pass would start: lands on frame 0's riff
NF = int(round(END * FPS))
cast.AI_T0 = E['ai']; cast.DEMO_T0 = E['demo']
SHOTS = [(1, 0.0, 0.8), (2, 0.8, 1.6), (3, 1.6, 3.1), (4, 3.1, 3.7), ('ff', 3.7, 4.1),
         (9, 4.1, 4.6), (10, 4.6, 6.4), (11, 6.4, 6.9), (12, 6.9, 8.5), (13, 8.5, 9.7),
         (14, 9.7, 10.2), (15, 10.2, 11.0), (16, 11.0, 12.3), (17, 12.3, END)]
KEY_T = {1: .5, 2: 1.45, 3: 2.4, 4: 3.6, 9: 4.4, 10: 5.3, 11: 6.8, 12: 7.9, 13: 9.0, 14: 10.05, 15: 10.6, 16: 11.42, 17: 13.6}
NAMES = {1: 'stadium (fantasy)', 2: 'stadium MCU', 3: 'reality: the drummer', 4: 'deflates; demo tape', 9: 'wide 2026',
         10: 'lean-in', 11: 'robot ready', 12: 'recoil', 13: 'his gesture', 14: 'robot eyes the tape', 15: 'the demo plays',
         16: 'stadium returns', 17: 'smug; robot turns to us'}
CHARS = True

# ---------------- lip flap ----------------
def _env():
    env = {k: np.zeros(NF + 60) for k in ('drum', 'hoodyz')}
    for n, t, who in (('drum', E['drum'], 'drum'), ('ask', E['ask'], 'hoodyz'), ('know', E['know'], 'hoodyz'), ('orig', E['orig'], 'hoodyz')):
        x, sr = sf.read(os.path.join(HERE, '..', 'vo', n + '.wav')); hop = sr // FPS
        r = np.array([np.sqrt((x[i * hop:(i + 1) * hop] ** 2).mean()) for i in range(len(x) // hop)]); r /= r.max() + 1e-9
        f0 = int(round(t * FPS))
        for i, v in enumerate(r): env[who][f0 + i] = max(env[who][f0 + i], v)
    return env
ENV = _env()
def lip(who, f): v = ENV[who][f] if f < len(ENV[who]) else 0; return v if v > .12 else 0

# ---------------- helpers ----------------
def cam(c, k, fx, fy, tx=540, ty=960):
    c.translate(tx, ty); c.scale(k, k); c.translate(-fx, -fy)

def strum_at(t, t0):
    d = 0
    for on in ONSETS:
        dt = t - (t0 + on)
        if 0 <= dt < .18: d = max(d, 34 * (1 - dt / .18))
    return d

def note_hit(t, t0, decay=.25):
    """1 on each riff note, decaying: drives stadium flashes and the toe tap."""
    v = 0
    for on in ONSETS:
        dt = t - (t0 + on)
        if 0 <= dt < decay: v = max(v, 1 - dt / decay)
    return v

def strum_lines(c, x, y, k):
    if k <= 0: return
    for i, r in enumerate((60, 90)):
        c.arc(x, y, r, 2.4, 3.6); c.set_source_rgba(*INK, .6 * k); c.set_line_width(8 - i * 2); c.stroke()

def note_glyph(c, x, y, s, col, alpha=1):
    if alpha <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s); c.push_group()
    ell(c, 0, 0, 20, 15); fs(c, col, 6)
    c.move_to(18, 0); c.line_to(18, -62); c.set_source_rgb(*INK); c.set_line_width(7); c.stroke()
    c.move_to(18, -62); c.curve_to(34, -52, 40, -38, 30, -26); c.set_line_width(7); c.stroke()
    c.pop_group_to_source(); c.paint_with_alpha(alpha); c.restore()

def motif(c, t, t0, x0, y0, sc=1.0, drop=None, life=2.0):
    for i, ((m, _), on) in enumerate(zip(RIFF, ONSETS)):
        dt = t - (t0 + on)
        if dt < 0 or dt > life: continue
        a = cl(dt / .08) * cl((life - dt) / .5)
        x = x0 + i * 62 * sc; y = y0 - (m - 60) * 16 * sc - dt * 40 * sc
        if drop is not None and i == len(RIFF) - 1 and t > drop:
            fd = t - drop; y += 1400 * fd * fd; a = cl(1 - fd / .5)
        note_glyph(c, x, y, sc * (.9 if i < 5 else 1.1), YEL, a)

def sub(c, t, a, b, text, y=1470):
    if not a <= t < b: return
    c.save(); c.identity_matrix(); k = cl((t - a) / .12)
    lines = text.split('|')
    for i, ln in enumerate(lines):
        size = 66; c.select_font_face('Lilita One'); c.set_font_size(size); w = c.text_extents(ln).width
        size = min(size, size * 820 / w)
        txt(c, ln, 500, y + (i - (len(lines) - 1)) * 80, size * (.9 + .1 * k), fill=WHITE, lw=12, alpha=k)
    c.restore()

# ---------------- sets ----------------
HX, HGY, HS = 400, 1560, .9
ROBOT = (640, 1128, .55)
TAPE = (790, 1240, .32)          # the dusty demo cassette on his 2026 desk

def bg_garage_close(c):
    c.set_source_rgb(*hx('6f7f96')); c.paint()
    rr(c, 640, 380, 380, 300, 12); fs(c, hx('1b1b2a'), 6); txt(c, 'THE LOUD', 830, 480, 64, fill=hx('ff5a6a'), lw=0)
    pool = cairo.RadialGradient(560, 900, 60, 560, 900, 800); pool.add_color_stop_rgba(0, 1, .93, .7, .3); pool.add_color_stop_rgba(1, 1, .93, .7, 0)
    c.set_source(pool); c.paint()
def bg_office_close(c):
    c.set_source_rgb(*hx('d3dce2')); c.paint()
    rr(c, 640, 380, 300, 230, 12); fs(c, WHITE, 6); txt(c, 'BAND', 790, 470, 56, fill=INK, lw=0); txt(c, "'86", 790, 550, 48, fill=INK, lw=0)
    glow = cairo.RadialGradient(900, 1000, 60, 900, 1000, 800); glow.add_color_stop_rgba(0, .5, .8, 1, .2); glow.add_color_stop_rgba(1, .5, .8, 1, 0)
    c.set_source(glow); c.paint()

def office26(c, t=0):
    c.set_source_rgb(*hx('dbe3e8')); c.paint()
    c.rectangle(0, 1500, W, H); c.set_source_rgb(*hx('a7a39c')); c.fill()
    rr(c, 300, 470, 200, 150, 10); fs(c, WHITE, 6); txt(c, 'BAND', 400, 525, 36, fill=INK, lw=0); txt(c, "'86", 400, 580, 32, fill=INK, lw=0)
    c.save(); c.translate(130, 640); c.rotate(-1.35); guitar(c, 0, 0, .5, dust=1); c.restore()
    c.move_to(110, 500); c.line_to(150, 520); c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
    rr(c, 640, 560, 340, 24, 6); fs(c, hx('8a6a4a'), 5)
    for i, col in enumerate(('d9534f', '5bc0de', 'f0ad4e', '5cb85c')): rr(c, 660 + i * 34, 470, 28, 90, 4); fs(c, hx(col), 4)
    ell(c, 920, 520, 40, 50); fs(c, hx('5fae6a'), 6)
def desk26(c, t, f, content='off'):
    rr(c, 540, 1260, 520, 40, 10); fs(c, hx('8a6a4a'))
    for x in (580, 1000): c.rectangle(x, 1300, 26, 210); c.set_source_rgb(*hx('5a4a3a')); c.fill()
    monitor(c, 700, 960, 240, 170, content, t, f)
    c.rectangle(810, 1140, 20, 120); c.set_source_rgb(*hx('1b2030')); c.fill()
    cassette(c, *TAPE, dust=1)
    glow = cairo.RadialGradient(800, 1050, 30, 700, 1050, 520)
    glow.add_color_stop_rgba(0, .5, .8, 1, .18 if content != 'off' else .06); glow.add_color_stop_rgba(1, .5, .8, 1, 0); c.set_source(glow); c.paint()

def world26(c, t, f, content='off', hpose='rest', hexpr='calm', hlean=0, hrot=0, wave_k=0, emote=None, eye=(0, 0), roll=0,
            him=True, hgaze=0, hdx=0, turn=0):
    office26(c, t); desk26(c, t, f, content)
    if CHARS:
        if turn: robot_turn(c, *ROBOT, turn, emote, eye, f)
        else: robot_body(c, *ROBOT, emote, eye, f, roll)
        if him: hoodyz(c, HX, HGY, HS, 2026, hexpr, hpose, f, lean=hlean, head_rot=hrot, op=lip('hoodyz', f), wave_k=wave_k, gaze=hgaze, head_dx=hdx)

def bar_and_subs(c, t, year):
    topbar_a(c, year)
    sub(c, t, E['drum'], E['drum'] + 1.4, 'PLAY SOMETHING WE KNOW.')
    sub(c, t, E['ask'], E['ask'] + 1.7, 'MAKE SOMETHING|COMPLETELY ORIGINAL.')
    sub(c, t, E['know'], E['know'] + 1.12, 'PLAY SOMETHING WE KNOW.')
    sub(c, t, E['orig'], END, "NOW THAT'S ORIGINAL!")

# ---------------- shots ----------------
def portrait(c, t, f, era, pose, expr, strum=0, rot=0, sway=0, lean=0, tap=0):
    """Matched performance framing (shots 2 and 16)."""
    c.translate(540, 1300); c.rotate(sway); c.translate(-540, -1300)
    if CHARS: hoodyz(c, 540, 1800, 1.7, era, expr, pose, f, tap=tap, strum=strum, head_rot=rot, lean=lean, op=lip('hoodyz', f))

def s1(c, t, f):   # frame 0: the stadium fantasy, wide
    k = lerp(1.0, 1.05, t / .8); cam(c, k, 540, 1060, 540, 1060)
    stadium(c, t, wide=True, flash=note_hit(t, R86))
    if CHARS:
        hoodyz(c, 540, 1460, 1.0, 1986, 'rocking', 'play', f, strum=strum_at(t, R86), tap=note_hit(t, R86, .2))
        strum_lines(c, 530, 1270, note_hit(t, R86, .12))
    crowd(c, t, 1600); motif(c, t, R86, 620, 820); dream_edge(c)

def s2(c, t, f):   # stadium MCU: the big strum, fist up on the last note
    stadium(c, t, wide=False, flash=note_hit(t, R86))
    last = R86 + ONSETS[-1]
    sway = .03 * math.sin((t - R86) / S16 * math.pi / 2)
    portrait(c, t, f, 1986, 'proud' if t >= last else 'play', 'rocking', strum_at(t, R86), rot=-.1 if t >= last else 0,
             sway=sway, lean=-.05 if t >= last else 0, tap=note_hit(t, R86, .2))
    crowd(c, t, 1640); motif(c, t, R86, 640, 760, 1.2); dream_edge(c)

def gesture_frame(c, t, f, who, t0, era_bg):
    """Matched gesture framing (shots 3 and 13): same screen spot, size and arm path; foreground at the same height."""
    era_bg(c)
    k = cl((t - t0) / 1.4)
    if CHARS:
        if who == 'drummer':
            drummer_body(c, 560, 820, 1.1, 'dismissive' if .25 < k < .85 else 'deadpan', f, -.12 if .3 < k < .85 else 0, lip('drum', f), wave_k=k)
        else:
            hoodyz(c, 560, 820 + 602 * 1.1, 1.1, 2026, 'dismissive' if .25 < k < .85 else 'deadpan', 'wave', f,
                   head_rot=-.12 if .3 < k < .85 else 0, op=lip('hoodyz', f), wave_k=k, legs_on=False)
    fg_y = 1190
    if who == 'drummer': drums_foreground(c, fg_y)
    else:
        rr(c, -40, fg_y, 1160, 60, 14); fs(c, hx('8a6a4a')); c.rectangle(-40, fg_y + 60, 1160, 800); c.set_source_rgb(*hx('6f5a46')); c.fill()
        rr(c, 700, fg_y - 50, 150, 60, 10); fs(c, hx('2a2f3a')); rr(c, 870, fg_y - 80, 70, 90, 12); fs(c, WHITE)

def s3(c, t, f): gesture_frame(c, t, f, 'drummer', E['wave86'], bg_garage_close)

def s4(c, t, f):   # the garage: hand frozen, then he deflates; pull back to the tiny amp and the recording demo tape
    bg_garage_close(c)
    u = cl((t - 3.22) / .3)
    k = lerp(1.22, 1.0, ss((t - 3.1) / .6))
    c.translate(540, 900); c.scale(k, k); c.translate(-540, -900)
    rr(c, 40, 1260, 250, 300, 16); fs(c, hx('2a2a32'))                                       # the tiny amp
    for i in range(4): ell(c, 165, 1410, 80 - i * 16, 80 - i * 16); c.set_source_rgb(*hx('3c3c48')); c.fill()
    rr(c, 30, 1060, 300, 200, 14); fs(c, hx('d8d2c4'), 6)                                      # recorder, REC on: the plant
    if int(t * 4) % 2 == 0: ell(c, 300, 1088, 14, 14); c.set_source_rgb(*RED); c.fill()
    txt(c, 'REC', 262, 1090, 26, fill=RED, lw=0)
    cassette(c, 165, 1170, .95)
    if CHARS:
        hoodyz(c, 580, 820 + 602 * 1.6, 1.6, 1986, 'sheepish' if t > 3.2 else 'rocking', 'proud' if u < .5 else 'deflated', f,
               deflate=u, head_rot=.08 * u, legs_on=False)
    motif(c, t, R86, 600, 520, 1.3, drop=3.15)

def ff(c, t, a, b):
    u = (t - a) / (b - a)
    for i in range(16):
        yy = (i * 137 + u * 2600) % H; c.rectangle(0, yy, W, 8 + (i % 3) * 10); c.set_source_rgba(1, 1, 1, .35); c.fill()
    c.rectangle(0, 0, W, H); c.set_source_rgba(.95, .95, 1, .3 * math.sin(math.pi * u)); c.fill()
    return int(lerp(1986, 2026, ss(u)))

def s9(c, t, f):   # wide 2026
    k = lerp(1.0, 1.04, (t - 4.1) / .5); cam(c, k, 540, 1060, 540 - 10 * (t - 4.1), 1060); world26(c, t, f)

def s10(c, t, f):  # he leans in, finger raised, eyes on the robot
    k = lerp(1.45, 1.6, ss((t - 4.6) / 1.8)); cam(c, k, 470, 1080, 520, 1000)
    lean = .2 * ss((t - 4.65) / .35)
    world26(c, t, f, hpose='point', hexpr='eager', hlean=lean, eye=(-14, 0), hgaze=14, hdx=30 * lean / .2)

def s11(c, t, f):  # robot: shoulder roll, loading -> ready
    cam(c, 2.6, ROBOT[0] + 10, ROBOT[1] + 30, 540, 980)
    world26(c, t, f, emote='loading' if t < 6.72 else 'ready', roll=cl((t - 6.4) / .45), him=False)

def s12(c, t, f):  # the AI's tune on the sequencer; his nod turns into a recoil
    office26(c, t)
    rec = ss((t - E['recoil']) / .18)
    if CHARS:
        nod = .05 * math.sin((t - E['ai']) * 4 * math.pi) * (1 - rec) if t < E['recoil'] else 0
        hoodyz(c, 380, 700 + 602 * 1.25, 1.25, 2026, 'polite' if rec < .5 else 'aghast', 'recoil' if rec > .3 else 'rest', f,
               lean=-.2 * rec, head_rot=nod - .16 * rec, legs_on=False, head_dx=-40 * rec)
    monitor(c, 470, 1080, 440, 320, 'ai', t, f)
    rr(c, 640, 1416, 100, 120, 10); fs(c, hx('1b2030'))
    for i, ((m, _), on) in enumerate(zip(AI_TUNE, AI_ONSETS)):
        dt = t - (E['ai'] + on)
        if 0 <= dt < 2.0 and E['ai'] + on < E['wave26']:
            a = cl(dt / .08) * cl((2.0 - dt) / .5); x = 600 + i * 64; y = 1000 - (m - 72) * 18 - dt * 40
            c.save(); c.translate(x, y); c.rotate(math.pi / 4); rr(c, -18, -18, 36, 36, 8)
            c.set_source_rgba(*BLUE, a); c.fill_preserve(); c.set_source_rgba(*INK, a); c.set_line_width(5); c.stroke(); c.restore()

def s13(c, t, f): gesture_frame(c, t, f, 'hoodyz', E['wave26'], bg_office_close)

def s14(c, t, f):  # robot close-up: its eyes slide to the dusty demo tape
    cam(c, 2.1, 720, 1150, 540, 1000)
    world26(c, t, f, emote='side' if t > 9.85 else None, eye=(-14, 0), him=False)

def s15(c, t, f):  # insert: the monitor plays GARAGE DEMO '86
    c.set_source_rgb(*hx('1b2030')); c.paint()
    k = lerp(1.0, 1.06, (t - 10.2) / .8); c.translate(540, 1000); c.scale(k, k); c.translate(-540, -1000)
    monitor(c, 110, 640, 860, 640, 'demo', t, f)
    motif(c, t, E['demo'], 240, 700, 1.3)

def s16(c, t, f):  # the stadium blooms back: air guitar in the exact shot 2 pose and rhythm
    bg_office_close(c)
    bloom = ss((t - E['bloom']) / .25)
    stadium(c, t, wide=False, k=bloom, flash=note_hit(t, E['demo']))
    last = E['demo'] + ONSETS[-1]
    sway = .03 * math.sin((t - E['demo']) / S16 * math.pi / 2)
    portrait(c, t, f, 2026, 'air' if t >= last else 'airstrum', 'rocking', strum_at(t, E['demo']), rot=-.1 if t >= last else 0,
             sway=sway, lean=-.05 if t >= last else 0, tap=note_hit(t, E['demo'], .2))
    crowd(c, t, 1640, k=bloom); motif(c, t, E['demo'], 640, 760, 1.2); dream_edge(c, bloom)

def s17(c, t, f):  # back in the office: smug air guitar; the robot looks at him, then turns its head to us
    tu = ss((t - E['turn'] + .1) / .45)                     # the camera drifts onto the robot as it turns to us
    cam(c, lerp(1.25, 1.6, tu), lerp(520, 640, tu), lerp(1100, 1120, tu), 540, 1010)
    bob = .06 * math.sin((t - 12.2) / .5 * math.pi * 2)
    turn = ss((t - E['turn']) / .25)
    world26(c, t, f, content='demo', hpose='air', hexpr='smug', hlean=-.05, hrot=-.08 + bob,
            emote='sideeye' if turn > .5 else None, eye=(-22, 0), turn=turn)
    motif(c, t, E['demo'] + 2.0, 620, 980, 1.0)

FN = {1: s1, 2: s2, 3: s3, 4: s4, 9: s9, 10: s10, 11: s11, 12: s12, 13: s13, 14: s14, 15: s15, 16: s16, 17: s17}

def draw(f, chars=True):
    global CHARS; CHARS = chars
    t = f / FPS
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(s)
    c.set_source_rgb(0, 0, 0); c.paint()
    shot = next((x for x in SHOTS if x[1] <= t < x[2]), SHOTS[-1])
    year = 1986 if t < E['ff'] else 2026
    c.save()
    if shot[0] == 'ff':
        c.save(); c.translate(-lerp(0, 60, (t - 3.7) / .4), 0); s9(c, 4.1, f); c.restore(); year = ff(c, t, 3.7, 4.1)
    else: FN[shot[0]](c, t, f)
    c.restore()
    bar_and_subs(c, t, year)
    return s

def frame_img(fr, chars=True):
    from PIL import Image
    return Image.frombuffer('RGBA', (W, H), bytes(draw(fr, chars).get_data()), 'raw', 'BGRA', 0, 1).convert('RGB')

def keys():
    from PIL import Image, ImageDraw, ImageChops
    os.makedirs('keys', exist_ok=True); tiles = []
    for n, tk in KEY_T.items():
        fr = int(round(tk * FPS)); im = frame_img(fr); im.save(f'keys/shot{n:02d}.png'); tiles.append((n, im, fr))
    cols = 5; rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * 300, rows * 580), 'white'); d = ImageDraw.Draw(sheet)
    for i, (n, im, fr) in enumerate(tiles):
        x, y = (i % cols) * 300, (i // cols) * 580; sheet.paste(im.resize((300, 533)), (x, y))
        d.text((x + 6, y + 540), f'{i + 1}. {NAMES[n]}  ({fr / FPS:.1f}s)', fill='black')
    sheet.save('keys/key_poses.png')
    for a_t, b_t, lab in ((E['wave86'] + .8, E['wave26'] + .8, 'gesture'), (R86 + ONSETS[-1] + .15, E['demo'] + ONSETS[-1] + .15, 'performance')):
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
    elif a and a[0] == 'lowres': render('make_it_original_timing.mp4', .5, 23)
    elif a:
        for x in a: fr = int(round(float(x) * FPS)); draw(fr).write_to_png(f'chk_{fr:03d}.png')
    else: render('make_it_original.mp4')
