"""Make It Original: timed-slideshow rough. Fixed composition per era, one main action per beat.
Usage: python3 rough.py [frame ...]  -> check PNGs; no args -> rough.mp4 (with fin.wav)."""
import sys, math, subprocess, numpy as np, cairo
from kit import *
from timeline import *
LIPS = np.load('lips.npy')
HX, HY, HS = 420, 900, .8          # Hoodyz's head: the same spot in every era
DX, DY, DS = 820, 930, .66         # the drummer
SUB_Y = 1470

def lip(who, f):
    v = LIPS[0 if who == 'drum' else 1][f] if f < LIPS.shape[1] else 0
    return v if v > .12 else 0

def sub(c, t, a, b, text):
    if not a <= t < b: return
    c.save(); c.identity_matrix()
    k = cl((t - a) / .12); lines = text.split('|')
    for i, ln in enumerate(lines):
        size = 66; c.select_font_face('Lilita One'); c.set_font_size(size); w = c.text_extents(ln).width
        size = min(size, size * 820 / w)        # fit inside the safe width (clear of the right-hand buttons)
        txt(c, ln, 500, SUB_Y + (i - (len(lines) - 1)) * 80, size * (.9 + .1 * k), fill=WHITE, lw=12, alpha=k)
    c.restore()

# ---------- note motifs ----------
def note_glyph(c, x, y, s, col, paw=False, alpha=1):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.push_group()
    ell(c, 0, 0, 20, 15); fs(c, col, 6)
    c.move_to(18, 0); c.line_to(18, -62); c.set_source_rgb(*INK); c.set_line_width(7); c.stroke()
    c.move_to(18, -62); c.curve_to(34, -52, 40, -38, 30, -26); c.set_line_width(7); c.stroke()
    if paw:
        for px, py, r in ((-34, 20, 9), (-24, 6, 6), (-40, 6, 6), (-46, 18, 5), (-20, 18, 5)):
            ell(c, px, py, r, r); c.set_source_rgb(*INK); c.fill()
    c.pop_group_to_source(); c.paint_with_alpha(alpha); c.restore()

def motif(c, t, t0, x0, y0, paws=False, drop=None):
    """The riff's note motif: one glyph per note at its onset, y from pitch, rising and fading.
    drop: time at which the last note falls out of the air (the rejection)."""
    for i, ((m, _), on) in enumerate(zip(RIFF, ONSETS)):
        dt = t - (t0 + on)
        if dt < 0 or dt > 2.2: continue
        a = cl(dt / .08) * cl((2.2 - dt) / .5)
        x = x0 + i * 62; y = y0 - (m - 60) * 16 - dt * 40
        if drop is not None and i == len(RIFF) - 1 and t > drop:
            fd = t - drop; y += 900 * fd * fd; a = cl(1 - fd / .6)
        note_glyph(c, x, y, .9 if i < 5 else 1.1, YEL, paws, a)

def ai_motif(c, t, t0, x0, y0):
    for i, ((m, _), on) in enumerate(zip(AI_TUNE, AI_ONSETS)):
        dt = t - (t0 + on)
        if dt < 0 or dt > 2.4: continue
        a = cl(dt / .08) * cl((2.4 - dt) / .5)
        x = x0 + i * 50; y = y0 - (m - 72) * 14 - dt * 30
        c.save(); c.translate(x, y); c.rotate(math.pi / 4); rr(c, -14, -14, 28, 28, 6)
        c.set_source_rgba(*BLUE, a); c.fill_preserve(); c.set_source_rgba(*INK, a); c.set_line_width(5); c.stroke(); c.restore()

# ---------- sets ----------
def garage(c):
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, *hx('8ea0b6')); g.add_color_stop_rgb(1, *hx('6f7f94'))
    c.set_source(g); c.paint()
    c.rectangle(0, 1380, W, H - 1380); c.set_source_rgb(*hx('9a9590')); c.fill()
    for i in range(9):   # roll-up garage door, left
        rr(c, -20, 420 + i * 108, 230, 96, 8); fs(c, hx('c9ced6'), 5)
    c.move_to(540, 360); c.line_to(540, 450); c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
    ell(c, 540, 470, 26, 30); c.set_source_rgb(*hx('fff2b0')); c.fill()
    rr(c, 600, 470, 300, 230, 10); fs(c, hx('1b1b2a'), 6)
    txt(c, 'THE LOUD', 750, 545, 54, fill=hx('ff5a6a'), lw=0); txt(c, "LIVE '86", 750, 630, 44, fill=YEL, lw=0)
    rr(c, 40, 1180, 200, 230, 14); fs(c, hx('2a2a32'))                          # amp
    for i in range(4): ell(c, 140, 1290, 60 - i * 12, 60 - i * 12); c.set_source_rgb(*hx('3c3c48')); c.fill()
    rr(c, 50, 1100, 180, 80, 10); fs(c, hx('d8d2c4'), 6)                        # cassette recorder on the amp
    ell(c, 210, 1125, 9, 9); c.set_source_rgb(*RED); c.fill()                   # REC light
    cassette(c, 120, 1140, .38)

def room16(c):
    c.set_source_rgb(*hx('e8dcc6')); c.paint()
    c.rectangle(0, 1380, W, H - 1380); c.set_source_rgb(*hx('b49a78')); c.fill()
    rr(c, 600, 470, 300, 230, 10); fs(c, hx('1b1b2a'), 6)                        # the same poster, faded
    txt(c, 'THE LOUD', 750, 545, 54, fill=hx('c88a90'), lw=0); txt(c, "LIVE '86", 750, 630, 44, fill=hx('d8c070'), lw=0)
    rr(c, 40, 1100, 180, 300, 10); fs(c, hx('8a6a4a'))                           # shelf with the cassette
    cassette(c, 130, 1080, .38)

def couch(c):
    rr(c, 560, 1180, 470, 120, 40); fs(c, hx('3f7a6a'))
    rr(c, 530, 1260, 530, 160, 40); fs(c, hx('4f8f7c'))

def office26(c):
    c.set_source_rgb(*hx('dfe6ea')); c.paint()
    c.rectangle(0, 1380, W, H - 1380); c.set_source_rgb(*hx('a7a39c')); c.fill()
    rr(c, 300, 470, 200, 150, 10); fs(c, WHITE, 6); txt(c, 'BAND', 400, 525, 36, fill=INK, lw=0); txt(c, "'86", 400, 580, 32, fill=INK, lw=0)
    c.save(); c.translate(130, 560); c.rotate(-1.35); guitar(c, 0, 0, .5, dust=1); c.restore()    # dusty on the wall
    c.move_to(110, 420); c.line_to(150, 440); c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()

def desk(c, t, mon_on=None):
    rr(c, 520, 1180, 540, 40, 10); fs(c, hx('8a6a4a'))                           # standing desk
    for x in (560, 1010): c.rectangle(x, 1220, 26, 200); c.set_source_rgb(*hx('5a4a3a')); c.fill()
    rr(c, 660, 860, 240, 180, 14); fs(c, hx('1b2030'))                           # monitor, kept left of the buttons
    rr(c, 674, 874, 212, 152, 8); c.set_source_rgb(*hx('0e2a3a') if mon_on else hx('20262f')); c.fill()
    c.rectangle(770, 1040, 20, 140); c.set_source_rgb(*hx('1b2030')); c.fill()
    cassette(c, 900, 1158, .3, dust=1)

# ---------- characters in place ----------
def hoodyz(c, era, t, f, expr, rot=0, arm_k=None, guitar_play=None, phone=False, lean=0):
    x, y, s = HX + lean * 14, HY, HS
    shadow(c, x, 1400, 120)
    shl, shr = hoodie(c, x, y + 160 * s, 1.2 * s)
    if guitar_play is not None:   # playing: body at the waist, neck up to the viewer's right
        strum = math.sin(guitar_play * 18) * 8
        guitar(c, x + 30, y + 330, .55, rot=-.45)
        arm(c, [shl, (x - 120, y + 300), (x - 6, y + 322 + strum)], s)
        arm(c, [shr, (x + 150, y + 250), (x + 150, y + 268)], s)
    elif phone:
        arm(c, [shl, (x - 70, y + 330), (x - 10, y + 260)], s); arm(c, [shr, (x + 70, y + 330), (x + 20, y + 262)], s)
        rr(c, x - 50, y + 190, 90, 150, 14); fs(c, INK, 0); rr(c, x - 42, y + 198, 74, 134, 10); c.set_source_rgb(*hx('6fd0ff')); c.fill()
    else:
        sh = shl
        if arm_k is not None: arm(c, waveoff(shl, s * 1.2, arm_k, -1), s, flick=1.0 if .38 < arm_k < .8 else 0)
        else: arm(c, [shl, (x - 100, y + 300), (x - 90, y + 380)], s)
        arm(c, [shr, (x + 100, y + 300), (x + 90, y + 380)], s)
    hoodyz_head(c, x, y, s * 1.08, era, expr, f, rot, op=lip('hoodyz', f))

def drummer(c, t, f, arm_k=None, expr='deadpan'):
    x, y, s = DX, DY, DS
    shl, shr = vest(c, x, y + 160 * s, 1.2 * s)
    if arm_k is not None: arm(c, waveoff(shl, s * 1.2, arm_k, -1), s, SKIN, flick=1.0 if .38 < arm_k < .8 else 0)
    else:
        arm(c, [shl, (x - 90, y + 260), (x - 120, y + 300)], s, SKIN); stick(c, x - 120, y + 300, -2.6, s)
    arm(c, [shr, (x + 90, y + 260), (x + 120, y + 300)], s, SKIN); stick(c, x + 120, y + 300, -.5, s)
    drummer_head(c, x, y, s * 1.08, expr, f, -.12 if arm_k is not None and arm_k > .3 else 0, op=lip('drum', f))
    drumkit(c, x + 10, 1430, .62)

def bot(c, t, f, emote=None, eye=(0, 0), present=0):
    x, y, s = 610, 1048, .6
    arms = None
    if present:
        sx, sy = x + 70 * s, y + 110 * s
        arms = [[(sx, sy), (lerp(sx + 20, sx + 60, present), lerp(sy + 60, sy - 20, present)), (lerp(sx + 30, sx + 120, present), lerp(sy + 90, sy - 60, present))]]
    robot(c, x, y, s, emote, eye, f, seed=2, arms=arms)

# ---------- phone close-ups (screen space) ----------
def phone_ui(c, t, which, k_swipe=0, views=None):
    c.set_source_rgb(*hx('20242c')); c.paint()
    rr(c, 170, 420, 740, 1080, 60); fs(c, hx('0b0d12'), 10)
    c.save(); rr(c, 196, 446, 688, 1028, 44); c.clip()
    c.set_source_rgb(*hx('14161c')); c.paint()
    for idx, who in enumerate(('his', 'cat')):
        oy = (idx - k_swipe) * 1028
        if abs(oy) > 1100: continue
        c.save(); c.translate(0, oy)
        rr(c, 236, 500, 608, 640, 30); fs(c, hx('2b3140'), 0)
        if who == 'his': hoodyz_head(c, 540, 820, 1.1, 2016, 'hopeful', 7, blink=False)
        else: cat(c, 560, 940, 1.1, 'walk', phase=.3, f=7)
        v = '3 VIEWS' if who == 'his' else (views or '10M VIEWS')
        txt(c, v, 540, 1270, 110 if who == 'cat' else 100, fill=WHITE if who == 'his' else YEL, lw=14)
        c.restore()
    c.restore()

# ---------- fast-forward ----------
def ff(c, k, y0, y1):
    for i in range(14):
        yy = (i * 151 + k * 2400) % H; c.rectangle(0, yy, W, 10 + (i % 3) * 8)
        c.set_source_rgba(1, 1, 1, .35); c.fill()
    c.rectangle(0, 0, W, H); c.set_source_rgba(.95, .95, 1, .25 * math.sin(math.pi * k)); c.fill()

# ---------- the film ----------
def draw(f):
    t = f / FPS
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(s)
    year, flip = 1986, 0
    wide = not (T['phone1'] <= t < T['couch'] or T['phone2'] <= t < T['ff2'] + .25)
    if wide:   # world zoom: characters bigger on a phone; the empty floor shrinks
        c.set_source_rgb(*hx('a7a39c')); c.paint(); c.translate(540, 1000); c.scale(1.1, 1.1); c.translate(-540, -1000)
    if t < T['ff1'] + .25:                                                     # ---- 1986
        garage(c); drummer_dt = t - T['drum_line']
        dk = cl((t - T['wave86'] - .05) / 1.4) if t >= T['wave86'] else None
        drummer(c, t, f, arm_k=dk, expr='dismissive' if dk and .25 < dk < .85 else 'deadpan')
        lastnote = T['riff86'] + ONSETS[-1]
        lean = ss((t - lastnote) / .2) if t < T['wave86'] else 1 - ss((t - T['wave86'] - .3) / .3)
        expr = 'hopeful' if t < T['wave86'] + .25 else 'sheepish'
        hoodyz(c, 1986, t, f, expr, rot=-.06 * lean, guitar_play=t if t < lastnote + .3 else None, lean=lean)
        motif(c, t, T['riff86'], 420, 640, drop=T['wave86'])
        sub(c, t, T['drum_line'], T['drum_line'] + 1.5, 'PLAY SOMETHING WE KNOW.')
        if t >= T['ff1']: ff(c, (t - T['ff1']) / .5, 0, 0); year = 1986 + int(30 * ss((t - T['ff1']) / .5)); flip = (t - T['ff1']) / .5
    elif t < T['phone1']:                                                      # ---- 2016: he plays to his phone
        room16(c); couch(c); year = 2016
        rr(c, 560, 1080, 90, 150, 12); fs(c, INK, 0)                            # phone propped on the couch arm
        hoodyz(c, 2016, t, f, 'hopeful', guitar_play=t if t < T['frag16'] + .8 else None)
        for i in range(3):
            dt = t - (T['frag16'] + ONSETS[i])
            if 0 <= dt < 1.2: note_glyph(c, 420 + i * 62, 640 - (RIFF[i][0] - 60) * 16 - dt * 40, .9, YEL, False, cl(dt / .08) * cl((1.2 - dt) / .4))
        if t < T['era16']: ff(c, (t - T['ff1']) / .5, 0, 0); year = 1986 + int(30 * ss((t - T['ff1']) / .5)); flip = (t - T['ff1']) / .5
    elif t < T['couch']:                                                       # ---- phone: 3 VIEWS
        phone_ui(c, t, 'his'); year = 2016
    elif t < T['phone2']:                                                      # ---- the cat plays it
        room16(c); couch(c); year = 2016
        guitar(c, 600, 1240, .75, rot=0)
        hoodyz(c, 2016, t, f, 'calm', phone=True)
        # cat walks right to left along the guitar; paws land exactly on note onsets
        tc = t - T['cat16']
        if t >= T['catwalk']:
            if tc < 0: px = lerp(1100, 900, cl((t - T['catwalk']) / .4))
            else: px = 900 - min(tc, ONSETS[-1] + .2) * 140
            on = [i for i, o in enumerate(ONSETS) if 0 <= tc - o < .09]
            cat(c, px, 1215, .8, 'walk', phase=t * 3, paw_down=(on[0] % 4) if on else None, f=f)
            for i in on:   # paw contact: a small impact on the strings
                ell(c, px - 60, 1232, 42, 10); c.set_source_rgba(*YEL, .85); c.fill()
        motif(c, t, T['cat16'], 600, 960, paws=True)
    elif t < T['face16']:                                                      # ---- phone: swipe to 10M
        k = ss((t - T['phone2'] - .1) / .2); n = cl((t - T['phone2'] - .2) / .5)
        v = 10_000_000 * n * n
        views = '10M VIEWS' if n >= 1 else (f'{v / 1e6:.1f}M VIEWS' if v >= 1e6 else f'{v / 1e3:.0f}K VIEWS')
        phone_ui(c, t, 'swipe', k, views); year = 2016
    elif t < T['ff2'] + .25:                                                   # ---- his face: stunned, then deadpan
        room16(c); year = 2016
        e = 'shock' if t < T['face16'] + .28 else 'deadpan'
        hoodyz_head(c, 540, 980, 2.0, 2016, e, f, blink=False)
        if t >= T['ff2']: ff(c, (t - T['ff2']) / .5, 0, 0); year = 2016 + int(10 * ss((t - T['ff2']) / .5)); flip = (t - T['ff2']) / .5
    else:                                                                      # ---- 2026
        office26(c); year = 2026
        on = T['ai'] <= t < T['ai'] + 2.6 or t >= T['cat26']
        desk(c, t, on)
        cat(c, 760, 1180, .55, 'sleep', old=True, f=f)
        # robot
        if t < T['ai']: em, eye, pr = None, (-10, 0), 0
        elif t < T['wave26']: em, eye, pr = 'proud', (0, 0), ss((t - T['ai']) / .3)
        elif t < T['glance']: em, eye, pr = None, (-14, 0), 0
        elif t < T['cat26']: em, eye, pr = None, (18, 8), 0
        elif t < T['sideeye']: em, eye, pr = 'happy', (0, 0), 0
        else: em, eye, pr = 'sideeye', (0, 0), 0
        bot(c, t, f, em, eye, pr)
        # Hoodyz
        rot = 0; arm_k = None
        if t < T['ai']: expr = 'confident'
        elif t < T['wave26']:
            expr = 'polite' if t < T['nod_stop'] + .3 else 'deadpan'
            if t < T['nod_stop']: rot = .05 * math.sin((t - T['ai']) * 2 * math.pi * 2)
        elif t < T['cat26']:
            arm_k = cl((t - T['wave26']) / 1.4); expr = 'dismissive' if .25 < arm_k < .85 else 'deadpan'
            rot = -.12 if .3 < arm_k < .85 else 0
        elif t < T['orig']:
            expr = 'deadpan'; rot = .07 * math.sin((t - T['bob']) * 2 * math.pi * 2) * cl((t - T['bob']) / .3) if t >= T['bob'] else 0
        else:
            expr = 'smug'; rot = .06 * math.sin((t - T['bob']) * 2 * math.pi * 2)
        hoodyz(c, 2026, t, f, expr, rot=rot, arm_k=arm_k)
        if T['ai'] <= t < T['ai'] + 2.6: ai_motif(c, t, T['ai'], 670, 830)
        for p in (0, 1): motif(c, t, T['cat26'] + p * BAR, 600, 760, paws=True)
        sub(c, t, T['ask'], T['ask'] + 1.8, 'MAKE SOMETHING|COMPLETELY ORIGINAL.')
        sub(c, t, T['know'], T['know'] + 1.3, 'PLAY SOMETHING WE KNOW.')
        sub(c, t, T['orig'], END, "NOW THAT'S ORIGINAL.")
    topbar(c, year)            # the year rolls through the numbers during a fast-forward
    return s

if __name__ == '__main__':
    if len(sys.argv) > 1:
        for a in sys.argv[1:]:
            fr = int(round(float(a) * FPS)) if '.' in a else int(a); draw(fr).write_to_png(f'chk_{fr:03d}.png')
        sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-i', 'fin.wav', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p',
                          '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709',
                          '-c:a', 'aac', '-b:a', '192k', '-shortest', 'rough_tmp.mp4'], stdin=subprocess.PIPE)
    for fr in range(NF):
        p.stdin.write(bytes(draw(fr).get_data()))
    p.stdin.close(); assert p.wait() == 0
    import os; os.replace('rough_tmp.mp4', 'make_it_original_rough.mp4'); print('frames', NF)
