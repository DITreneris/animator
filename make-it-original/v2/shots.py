"""Make It Original v2: 17 shots on the riff's beat grid.
python3 shots.py keys   -> key-pose stills, silhouette sheet, matched-pair overlays (keys/)
python3 shots.py t ...  -> check frames at times t (seconds)
python3 shots.py        -> make_it_original_v2.mp4 (needs fin.wav from mix2.py)"""
import sys, os, math, subprocess
import numpy as np, cairo, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__))
from cast import *
sys.path.insert(0, os.path.join(HERE, '..'))
from timeline import RIFF, AI_TUNE, ONSETS, AI_ONSETS, S16, FPS

# ---------------- timeline (seconds) ----------------
R86 = 0.067
E = dict(drum=1.95, wave86=1.9, frag=4.4, views3=5.0, land=5.35, cat16=5.8, views10=7.75,
         ask=9.3, ai=11.55, recoil=12.6, know=13.35, wave26=13.3, glance=14.5, cat26=15.0, orig=16.3, catlook=17.95)
END = E['cat26'] + 2 * 2.0 - R86
NF = int(round(END * FPS))
SHOTS = [(1, 0.0, 0.8), (2, 0.8, 1.9), (3, 1.9, 3.4), (4, 3.4, 3.9), ('ff1', 3.9, 4.3),
         (5, 4.3, 5.3), (6, 5.3, 5.7), (7, 5.7, 7.6), (8, 7.6, 8.3), ('ff2', 8.3, 8.7),
         (9, 8.7, 9.2), (10, 9.2, 11.0), (11, 11.0, 11.5), (12, 11.5, 13.3), (13, 13.3, 14.5),
         (14, 14.5, 15.0), (15, 15.0, 16.0), (16, 16.0, 17.3), (17, 17.3, END)]
KEY_T = {1: .5, 2: 1.55, 3: 2.75, 4: 3.8, 5: 5.15, 6: 5.55, 7: 6.6, 8: 8.0, 9: 9.0, 10: 9.9, 11: 11.4,
         12: 12.95, 13: 13.95, 14: 14.85, 15: 15.6, 16: 16.45, 17: 18.6}
CHARS = True     # False: draw sets only (used for the silhouette check)

# ---------------- lip flap ----------------
def _env():
    env = {k: np.zeros(NF + 30) for k in ('drum', 'hoodyz')}
    for n, t, who in (('drum', E['drum'], 'drum'), ('ask', E['ask'], 'hoodyz'), ('know', E['know'], 'hoodyz'), ('orig', E['orig'], 'hoodyz')):
        x, sr = sf.read(os.path.join(HERE, '..', 'vo', n + '.wav')); hop = sr // FPS
        r = np.array([np.sqrt((x[i * hop:(i + 1) * hop] ** 2).mean()) for i in range(len(x) // hop)]); r /= r.max() + 1e-9
        f0 = int(round(t * FPS))
        for i, v in enumerate(r): env[who][f0 + i] = max(env[who][f0 + i], v)
    return env
ENV = _env()
def lip(who, f): v = ENV[who][f]; return v if v > .12 else 0

# ---------------- helpers ----------------
def cam(c, k, fx, fy, tx=540, ty=960):
    c.translate(tx, ty); c.scale(k, k); c.translate(-fx, -fy)

def keyed(t, keys):
    """keys: [(t, value...)], smoothstep between; returns tuple."""
    if t <= keys[0][0]: return keys[0][1:]
    if t >= keys[-1][0]: return keys[-1][1:]
    for a, b in zip(keys, keys[1:]):
        if a[0] <= t < b[0]:
            u = ss((t - a[0]) / (b[0] - a[0])); return tuple(lerp(p, q, u) for p, q in zip(a[1:], b[1:]))

def strum_at(t, t0):
    """Strum-hand dip on each riff note of a take starting at t0 (local units)."""
    d = 0
    for on in ONSETS:
        dt = t - (t0 + on)
        if 0 <= dt < .18: d = max(d, 34 * (1 - dt / .18))
    return d

def note_glyph(c, x, y, s, col, paw=False, alpha=1):
    if alpha <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s); c.push_group()
    ell(c, 0, 0, 20, 15); fs(c, col, 6)
    c.move_to(18, 0); c.line_to(18, -62); c.set_source_rgb(*INK); c.set_line_width(7); c.stroke()
    c.move_to(18, -62); c.curve_to(34, -52, 40, -38, 30, -26); c.set_line_width(7); c.stroke()
    if paw:
        for px, py, r in ((-34, 20, 9), (-24, 6, 6), (-40, 6, 6), (-46, 18, 5), (-20, 18, 5)):
            ell(c, px, py, r, r); c.set_source_rgb(*INK); c.fill()
    c.pop_group_to_source(); c.paint_with_alpha(alpha); c.restore()

def motif(c, t, t0, x0, y0, sc=1.0, paws=False, drop=None, n=6, life=2.0):
    for i, ((m, _), on) in enumerate(zip(RIFF[:n], ONSETS[:n])):
        dt = t - (t0 + on)
        if dt < 0 or dt > life: continue
        a = cl(dt / .08) * cl((life - dt) / .5)
        x = x0 + i * 62 * sc; y = y0 - (m - 60) * 16 * sc - dt * 40 * sc
        if drop is not None and i == n - 1 and t > drop:
            fd = t - drop; y += 1400 * fd * fd; a = cl(1 - fd / .5)
        note_glyph(c, x, y, sc * (.9 if i < 5 else 1.1), YEL, paws, a)

def sub(c, t, a, b, text, y=1470):
    if not a <= t < b: return
    c.save(); c.identity_matrix(); k = cl((t - a) / .12)
    for i, ln in enumerate(text.split('|')):
        size = 66; c.select_font_face('Lilita One'); c.set_font_size(size); w = c.text_extents(ln).width
        size = min(size, size * 820 / w)
        txt(c, ln, 500, y + (i - (len(text.split('|')) - 1)) * 80, size * (.9 + .1 * k), fill=WHITE, lw=12, alpha=k)
    c.restore()

# ---------------- sets (world coordinates; Hoodyz stands at x=400, feet y=1560, scale .9) ----------------
HX, HGY, HS = 400, 1560, .9
def garage(c, t=0):
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, *hx('7d8ea6')); g.add_color_stop_rgb(1, *hx('5f6e84'))
    c.set_source(g); c.paint()
    c.rectangle(0, 1500, W, H); c.set_source_rgb(*hx('8e8984')); c.fill()
    for i in range(10): rr(c, -20, 380 + i * 112, 230, 100, 8); fs(c, hx('c3c9d2'), 5)       # roll-up door
    rr(c, 600, 470, 300, 230, 10); fs(c, hx('1b1b2a'), 6)
    txt(c, 'THE LOUD', 750, 545, 54, fill=hx('ff5a6a'), lw=0); txt(c, "LIVE '86", 750, 630, 44, fill=YEL, lw=0)
    sw = math.sin(t * 2.2) * .08                                                            # the bulb sways
    c.save(); c.translate(560, 360); c.rotate(sw)
    c.move_to(0, 0); c.line_to(0, 110); c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
    ell(c, 0, 132, 26, 30); c.set_source_rgb(*hx('fff2b0')); c.fill(); c.restore()
    pool = cairo.RadialGradient(560 + sw * 400, 1200, 50, 560, 1200, 700)                    # warm pool of light
    pool.add_color_stop_rgba(0, 1, .93, .7, .28); pool.add_color_stop_rgba(1, 1, .93, .7, 0); c.set_source(pool); c.paint()
    rr(c, 40, 1280, 200, 230, 14); fs(c, hx('2a2a32'))                                     # amp + recorder
    for i in range(4): ell(c, 140, 1395, 60 - i * 12, 60 - i * 12); c.set_source_rgb(*hx('3c3c48')); c.fill()
    rr(c, 50, 1200, 180, 80, 10); fs(c, hx('d8d2c4'), 6); ell(c, 210, 1225, 9, 9); c.set_source_rgb(*RED); c.fill()
    cassette(c, 120, 1240, .38)
    c.move_to(140, 1510); c.curve_to(300, 1620, 520, 1560, 700, 1640); c.set_source_rgb(*hx('d23a4a')); c.set_line_width(8); c.stroke()   # cable

def drummer_world(c, t, f, wave_k=None, expr='deadpan'):
    c.save(); rr(c, 770, 1330, 70, 160, 10); fs(c, hx('3a3a44')); c.restore()             # stool
    drummer_body(c, 805, 1060, .62, expr, f, op=lip('drum', f), wave_k=wave_k)
    drumkit(c, 815, 1560, .62)

def room16(c, t=0):
    c.set_source_rgb(*hx('ebdfc9')); c.paint()
    c.rectangle(0, 1500, W, H); c.set_source_rgb(*hx('b49a78')); c.fill()
    rr(c, 640, 420, 300, 220, 10); fs(c, hx('9fd0ea'), 8)                                  # window, daylight
    c.move_to(790, 420); c.line_to(790, 640); c.move_to(640, 530); c.line_to(940, 530); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    day = cairo.LinearGradient(790, 640, 600, 1500); day.add_color_stop_rgba(0, 1, 1, .9, .25); day.add_color_stop_rgba(1, 1, 1, .9, 0)
    c.set_source(day); c.paint()
    rr(c, 100, 470, 220, 160, 10); fs(c, hx('1b1b2a'), 6); txt(c, 'THE LOUD', 210, 540, 38, fill=hx('c88a90'), lw=0)   # the poster, faded
    rr(c, 40, 1220, 160, 290, 10); fs(c, hx('8a6a4a')); cassette(c, 120, 1200, .34)           # shelf
    ell(c, 120, 1100, 50, 70); fs(c, hx('5fae6a'), 6)                                        # plant
def couch16(c):
    rr(c, 560, 1320, 480, 120, 40); fs(c, hx('3f7a6a'))
    rr(c, 530, 1400, 540, 150, 40); fs(c, hx('4f8f7c'))

def office26(c, t=0):
    c.set_source_rgb(*hx('dbe3e8')); c.paint()
    c.rectangle(0, 1500, W, H); c.set_source_rgb(*hx('a7a39c')); c.fill()
    rr(c, 300, 470, 200, 150, 10); fs(c, WHITE, 6); txt(c, 'BAND', 400, 525, 36, fill=INK, lw=0); txt(c, "'86", 400, 580, 32, fill=INK, lw=0)
    c.save(); c.translate(130, 640); c.rotate(-1.35); guitar(c, 0, 0, .5, dust=1); c.restore()
    c.move_to(110, 500); c.line_to(150, 520); c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
    rr(c, 640, 560, 340, 24, 6); fs(c, hx('8a6a4a'), 5)                                       # shelf with plant and books
    for i, col in enumerate(('d9534f', '5bc0de', 'f0ad4e', '5cb85c')): rr(c, 660 + i * 34, 470, 28, 90, 4); fs(c, hx(col), 4)
    ell(c, 920, 520, 40, 50); fs(c, hx('5fae6a'), 6)
def desk26(c, t, f, content='off'):
    rr(c, 540, 1260, 520, 40, 10); fs(c, hx('8a6a4a'))
    for x in (580, 1000): c.rectangle(x, 1300, 26, 210); c.set_source_rgb(*hx('5a4a3a')); c.fill()
    monitor(c, 700, 960, 240, 170, content, t, f)
    c.rectangle(810, 1140, 20, 120); c.set_source_rgb(*hx('1b2030')); c.fill()
    glow = cairo.RadialGradient(800, 1050, 30, 700, 1050, 520)                               # cool monitor light
    glow.add_color_stop_rgba(0, .5, .8, 1, .18 if content != 'off' else .06); glow.add_color_stop_rgba(1, .5, .8, 1, 0); c.set_source(glow); c.paint()
def oldcat(c, f): cat(c, 880, 1262, .5, 'sleep', old=True, f=f)
ROBOT = (640, 1128, .55)

def bar_and_subs(c, t, year):
    topbar(c, year)
    sub(c, t, E['drum'], E['drum'] + 1.45, 'PLAY SOMETHING WE KNOW.')
    sub(c, t, E['ask'], E['ask'] + 1.75, 'MAKE SOMETHING|COMPLETELY ORIGINAL.')
    sub(c, t, E['know'], E['know'] + 1.15, 'PLAY SOMETHING WE KNOW.')
    sub(c, t, E['orig'], END, "NOW THAT'S ORIGINAL!")

# ---------------- the shots ----------------
def s1(c, t, f):   # wide 1986, slow push-in
    k = lerp(1.0, 1.05, t / .8); cam(c, k, 540, 1060, 540, 1060); garage(c, t)
    if CHARS:
        drummer_world(c, t, f)
        hoodyz(c, HX, HGY, HS, 1986, 'rocking', 'play', f, strum=strum_at(t, R86))
    motif(c, t, R86, 470, 760)

def portrait(c, t, f, era, pose, expr, strum=0, rot=0, sway=0, lean=0):
    """Matched performance framing (shots 2 and 16): same position, size and sway in both eras."""
    c.translate(540, 1300); c.rotate(sway); c.translate(-540, -1300)
    if CHARS: hoodyz(c, 540, 1800, 1.7, era, expr, pose, f, strum=strum, head_rot=rot, lean=lean, op=lip('hoodyz', f))

def s2(c, t, f):   # MCU 1986: lost in it, strum hand goes up on the last note
    bg_garage_close(c)
    last = R86 + ONSETS[-1]
    pose = 'proud' if t >= last else 'play'
    sway = .03 * math.sin((t - R86) / S16 * math.pi / 2)
    portrait(c, t, f, 1986, pose, 'rocking', strum_at(t, R86), rot=-.1 if t >= last else 0, sway=sway, lean=-.05 if t >= last else 0)
    motif(c, t, R86, 640, 760, 1.2)

def gesture_frame(c, t, f, who, t0, era_bg):
    """Matched gesture framing (shots 3 and 13): the gesturer at the same screen spot, size and arm path."""
    era_bg(c)
    k = cl((t - t0) / 1.4)
    if CHARS:
        if who == 'drummer':
            drummer_body(c, 560, 820, 1.1, 'dismissive' if .25 < k < .85 else 'deadpan', f, -.12 if .3 < k < .85 else 0, lip('drum', f), wave_k=k)
        else:
            hoodyz(c, 560, 820 + 602 * 1.1, 1.1, 2026, 'dismissive' if .25 < k < .85 else 'deadpan', 'wave', f,
                   head_rot=-.12 if .3 < k < .85 else 0, op=lip('hoodyz', f), wave_k=k, legs_on=False)
    fg_y = 1190                                                     # the foreground edge sits at the same height in both eras
    if who == 'drummer':
        ell(c, 330, fg_y + 70, 210, 60); fs(c, hx('d23a4a')); ell(c, 330, fg_y + 62, 180, 44); fs(c, hx('f5efe2'), 6)   # tom
        rr(c, 120, fg_y + 70, 420, 700, 20); fs(c, hx('d23a4a'))
        ell(c, 880, fg_y + 20, 200, 30); fs(c, YEL, 6)                                                                   # cymbal edge
        c.rectangle(540, fg_y + 40, 700, 800); c.set_source_rgb(*hx('3a3a44')); c.fill()
    else:
        rr(c, -40, fg_y, 1160, 60, 14); fs(c, hx('8a6a4a'))                                                                # desk edge
        c.rectangle(-40, fg_y + 60, 1160, 800); c.set_source_rgb(*hx('6f5a46')); c.fill()
        rr(c, 700, fg_y - 50, 150, 60, 10); fs(c, hx('2a2f3a')); rr(c, 870, fg_y - 80, 70, 90, 12); fs(c, WHITE)            # keyboard + mug
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
def s3(c, t, f): gesture_frame(c, t, f, 'drummer', E['wave86'], bg_garage_close)

def s4(c, t, f):   # CU: the strum hand freezes mid-air, then he deflates; camera pulls back
    bg_garage_close(c)
    u = cl((t - 3.55) / .3)
    k = lerp(1.25, 1.0, ss((t - 3.4) / .5))
    c.translate(540, 900); c.scale(k, k); c.translate(-540, -900)
    if CHARS:
        pose = 'proud' if u < .5 else 'deflated'
        hoodyz(c, 540, 820 + 602 * 1.6, 1.6, 1986, 'sheepish' if t > 3.5 else 'rocking', pose, f, deflate=u, head_rot=.08 * u, legs_on=False)
    motif(c, t, R86, 600, 520, 1.3, drop=3.45)

def ff(c, t, a, b, era_from, era_to):
    u = (t - a) / (b - a)
    for i in range(16):
        yy = (i * 137 + u * 2600) % H; c.rectangle(0, yy, W, 8 + (i % 3) * 10); c.set_source_rgba(1, 1, 1, .35); c.fill()
    c.rectangle(0, 0, W, H); c.set_source_rgba(.95, .95, 1, .3 * math.sin(math.pi * u)); c.fill()
    return int(lerp(era_from, era_to, ss(u)))

def sff(c, t, f, a, b, drawer, y0, y1):
    c.save(); c.translate(-lerp(0, 60, (t - a) / (b - a)), 0); drawer(c, t, f); c.restore()
    return ff(c, t, a, b, y0, y1)

def s5(c, t, f):   # 2016 medium: he plays to his phone; 3 VIEWS pops up
    c.save(); cam(c, 1.25, 520, 1180, 540, 1120); room16(c, t); couch16(c)
    c.move_to(660, 1500); c.line_to(660, 1240); c.set_source_rgb(*INK); c.set_line_width(8); c.stroke()      # phone on a stand
    rr(c, 620, 1120, 80, 140, 12); fs(c, INK, 0); rr(c, 628, 1128, 64, 124, 8); c.set_source_rgb(*hx('6fd0ff')); c.fill()
    if CHARS: hoodyz(c, HX, HGY, HS, 2016, 'hopeful', 'play' if t < E['frag'] + .9 else 'rest', f, strum=strum_at(t, E['frag']))
    c.restore()
    for i in range(3):
        dt = t - (E['frag'] + ONSETS[i])
        if 0 <= dt < 1.2: note_glyph(c, 520 + i * 70, 760 - (RIFF[i][0] - 60) * 18 - dt * 40, 1.0, YEL, False, cl(dt / .08) * cl((1.2 - dt) / .4))
    if t >= E['views3']: views_badge(c, 760, 860, '3 VIEWS', (t - E['views3']) / .25)

def s6(c, t, f):   # insert: the guitar lands on the couch
    c.set_source_rgb(*hx('ebdfc9')); c.paint()
    rr(c, -40, 1000, 1160, 260, 60); fs(c, hx('3f7a6a')); rr(c, -60, 1200, 1200, 420, 60); fs(c, hx('4f8f7c'))
    u = cl((t - 5.3) / .14); y = lerp(300, 1250, u * u)
    if u >= 1: y = 1250 - abs(math.sin((t - 5.44) * 18)) * 30 * math.exp(-(t - 5.44) * 10)
    guitar(c, 380, y, 1.2, rot=lerp(-.6, 0, u))
    if 5.44 <= t < 5.6:
        for i in range(5):
            a = math.pi + i * math.pi / 4; c.move_to(380 + math.cos(a) * 200, 1300 + math.sin(a) * 90); c.line_to(380 + math.cos(a) * 280, 1300 + math.sin(a) * 130)
            c.set_source_rgb(*INK); c.set_line_width(8); c.stroke()

def s7(c, t, f):   # low close-up on the paws; the camera pans with the cat
    c.set_source_rgb(*hx('ebdfc9')); c.paint(); rr(c, -60, 1180, 1200, 760, 60); fs(c, hx('4f8f7c'))
    tc = t - E['cat16']
    gx = 150 + max(0, tc + .15) * 230                                       # the guitar slides right = camera follows the cat left
    guitar(c, gx, 1280, 2.0, rot=0)
    on = [i for i, o in enumerate(ONSETS) if 0 <= tc - o < .1]
    if CHARS: cat(c, 640, 1250, 1.6, 'walk', phase=t * 3, paw_down=(on[0] % 4) if on else None, f=f)
    for i in on:
        ell(c, 560, 1262, 90, 18); c.set_source_rgba(*YEL, .85); c.fill()
    for i, ((m, _), on) in enumerate(zip(RIFF, ONSETS)):      # same screen positions as his fragment in shot 5
        dt = t - (E['cat16'] + on)
        if 0 <= dt < 1.6: note_glyph(c, 520 + i * 70, 760 - (m - 60) * 18 - dt * 40, 1.0, YEL, True, cl(dt / .08) * cl((1.6 - dt) / .4))
    if t >= 7.35: views_badge(c, 640, 640, '10M', (t - 7.35) / .25, col=YEL, size=110)

def s8(c, t, f):   # MCU 2016: deadpan; the cat's 10M on his phone
    room16(c, t); c.save(); cam(c, lerp(1.7, 1.8, (t - 7.6) / .7), HX, 1040, 540, 900)
    if CHARS: hoodyz(c, HX, HGY, HS, 2016, 'shock' if t < 7.82 else 'deadpan', 'phone', f)
    c.restore()
    views_badge(c, 540, 1460, 'CAT: 10M', 1, col=YEL, size=84)

def world26(c, t, f, content='off', hpose='rest', hexpr='calm', hlean=0, hrot=0, wave_k=0, remote=None, emote=None, eye=(0, 0), roll=0, present=0, him=True, hgaze=0, hdx=0):
    office26(c, t); desk26(c, t, f, content); oldcat(c, f)
    if CHARS:
        robot_body(c, *ROBOT, emote, eye, f, roll, present)
        if him: hoodyz(c, HX, HGY, HS, 2026, hexpr, hpose, f, lean=hlean, head_rot=hrot, op=lip('hoodyz', f), wave_k=wave_k, gaze=hgaze, head_dx=hdx)
    cassette(c, 160, 1490, .3, dust=1)

def s9(c, t, f):
    k = lerp(1.0, 1.04, (t - 8.7) / .5); cam(c, k, 540, 1060, 540 - 10 * (t - 8.7), 1060); world26(c, t, f)

def s10(c, t, f):  # medium: he leans in, finger raised
    k = lerp(1.45, 1.6, ss((t - 9.2) / 1.8)); cam(c, k, 470, 1080, 520, 1000)
    lean = .2 * ss((t - 9.25) / .35)
    world26(c, t, f, hpose='point', hexpr='eager', hlean=lean, eye=(-14, 0), hgaze=14, hdx=30 * lean / .2)

def s11(c, t, f):  # CU robot: shoulder roll, loading
    cam(c, 2.6, ROBOT[0] + 10, ROBOT[1] + 30, 540, 980)
    world26(c, t, f, emote='loading' if t < 11.33 else 'ready', roll=cl((t - 11.0) / .45), him=False)

def s12(c, t, f):  # over the monitor: the AI's art; his nod turns into a recoil
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
        if 0 <= dt < 2.0:
            a = cl(dt / .08) * cl((2.0 - dt) / .5); x = 600 + i * 64; y = 1000 - (m - 72) * 18 - dt * 40
            c.save(); c.translate(x, y); c.rotate(math.pi / 4); rr(c, -18, -18, 36, 36, 8)
            c.set_source_rgba(*BLUE, a); c.fill_preserve(); c.set_source_rgba(*INK, a); c.set_line_width(5); c.stroke(); c.restore()

def s13(c, t, f): gesture_frame(c, t, f, 'hoodyz', E['wave26'], bg_office_close)

def s14(c, t, f):  # CU robot: its eyes slide to the old cat
    cam(c, 2.1, 760, 1150, 540, 1000)
    world26(c, t, f, emote='side' if t > 14.62 else None, eye=(-14, 0), him=False)

def s15(c, t, f):  # insert: the monitor plays the 2016 cat video; the riff starts
    c.set_source_rgb(*hx('1b2030')); c.paint()
    k = lerp(1.0, 1.06, (t - 15.0) / 1.0); c.translate(540, 1000); c.scale(k, k); c.translate(-540, -1000)
    monitor(c, 110, 640, 860, 640, 'cat', t, f)
    motif(c, t, E['cat26'], 240, 700, 1.3, paws=True)

def s16(c, t, f):  # matched performance: air guitar in the 1986 pose and rhythm
    bg_office_close(c)
    last = E['cat26'] + ONSETS[-1]
    pose = 'air' if t >= last else 'airstrum'
    sway = .03 * math.sin((t - E['cat26']) / S16 * math.pi / 2)
    portrait(c, t, f, 2026, pose, 'rocking', strum_at(t, E['cat26']), rot=-.1 if t >= last else 0, sway=sway,
             lean=-.05 if t >= last else 0)
    motif(c, t, E['cat26'], 640, 760, 1.2, paws=True)

def s17(c, t, f):  # two-shot hold: smug air guitar; the robot looks at him, then at us
    k = lerp(1.25, 1.35, (t - 17.3) / (END - 17.3)); cam(c, k, 520, 1100, 540, 1010)
    bob = .06 * math.sin((t - 17.0) / .5 * math.pi * 2)
    world26(c, t, f, content='cat', hpose='air', hexpr='smug', hlean=-.05, hrot=-.08 + bob,
            emote='side' if t >= E['catlook'] else None, eye=(-22, 0))
    motif(c, t, E['cat26'] + 2.0, 620, 760, 1.0, paws=True)

FN = {1: s1, 2: s2, 3: s3, 4: s4, 5: s5, 6: s6, 7: s7, 8: s8, 9: s9, 10: s10, 11: s11, 12: s12, 13: s13, 14: s14, 15: s15, 16: s16, 17: s17}
def year_of(t): return 1986 if t < 3.9 else 2016 if t < 8.3 else 2026

def draw(f, chars=True):
    global CHARS; CHARS = chars
    t = f / FPS
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(s)
    c.set_source_rgb(0, 0, 0); c.paint()
    shot = next(x for x in SHOTS if x[1] <= t < x[2]) if t < END else SHOTS[-1]
    year = year_of(t)
    c.save()
    if shot[0] == 'ff1': year = sff(c, t, f, 3.9, 4.3, lambda c, t, f: s5(c, 4.3, f), 1986, 2016)
    elif shot[0] == 'ff2': year = sff(c, t, f, 8.3, 8.7, lambda c, t, f: s9(c, 8.7, f), 2016, 2026)
    else: FN[shot[0]](c, t, f)
    c.restore()
    bar_and_subs(c, t, year)
    return s

def shot_name(n): return {1: 'wide 1986', 2: 'MCU, lost in it', 3: 'matched gesture: drummer', 4: 'CU, frozen, deflates', 5: '2016: 3 VIEWS',
    6: 'guitar lands', 7: 'paws play it', 8: 'deadpan, 10M', 9: 'wide 2026', 10: 'lean-in', 11: 'robot loading', 12: 'recoil',
    13: 'matched gesture: Hoodyz', 14: 'robot glance', 15: 'cat video', 16: 'matched performance', 17: 'smug hold'}[n]

def keys():
    from PIL import Image, ImageDraw, ImageChops
    os.makedirs('keys', exist_ok=True)
    tiles = []
    for n, tk in KEY_T.items():
        fr = int(round(tk * FPS)); im = Image.frombuffer('RGBA', (W, H), bytes(draw(fr).get_data()), 'raw', 'BGRA', 0, 1).convert('RGB')
        im.save(f'keys/shot{n:02d}.png'); tiles.append((n, im, fr))
    cols = 6; sheet = Image.new('RGB', (cols * 300, 3 * 580), 'white'); d = ImageDraw.Draw(sheet)
    for i, (n, im, fr) in enumerate(tiles):
        x, y = (i % cols) * 300, (i // cols) * 580; sheet.paste(im.resize((300, 533)), (x, y))
        d.text((x + 6, y + 540), f'{n}. {shot_name(n)}  ({fr / FPS:.1f}s)', fill='black')
    sheet.save('keys/key_poses.png')
    sil = Image.new('RGB', (cols * 300, 3 * 580), 'white'); d = ImageDraw.Draw(sil)          # silhouettes: characters only, solid black
    for i, (n, im, fr) in enumerate(tiles):
        bg = Image.frombuffer('RGBA', (W, H), bytes(draw(fr, chars=False).get_data()), 'raw', 'BGRA', 0, 1).convert('RGB')
        m = ImageChops.difference(im, bg).convert('L').point(lambda v: 255 if v > 18 else 0)
        s_ = Image.new('RGB', (W, H), 'white'); s_.paste((0, 0, 0), mask=m)
        x, y = (i % cols) * 300, (i // cols) * 580; sil.paste(s_.resize((300, 533)), (x, y)); d.text((x + 6, y + 540), f'{n}. {shot_name(n)}', fill='black')
    sil.save('keys/silhouettes.png')
    for a, b, lab in ((3, 13, 'gesture'), (2, 16, 'performance')):        # matched pairs, at the same moment of each gesture
        da = E['wave86'] if a == 3 else R86 + ONSETS[-1]; db = E['wave26'] if b == 13 else E['cat26'] + ONSETS[-1]
        for dt in (.6, .8) if a == 3 else (.15,):
            fa = Image.frombuffer('RGBA', (W, H), bytes(draw(int(round((da + dt) * FPS))).get_data()), 'raw', 'BGRA', 0, 1).convert('RGB')
            fb = Image.frombuffer('RGBA', (W, H), bytes(draw(int(round((db + dt) * FPS))).get_data()), 'raw', 'BGRA', 0, 1).convert('RGB')
            Image.blend(fa, fb, .5).resize((540, 960)).save(f'keys/overlay_{lab}_{dt:.2f}.png')
    print('keys ok')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'keys': keys(); sys.exit()
    if len(sys.argv) > 1:
        for a in sys.argv[1:]: fr = int(round(float(a) * FPS)); draw(fr).write_to_png(f'chk_{fr:03d}.png')
        sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-i', 'fin.wav', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '16', '-pix_fmt', 'yuv420p',
                          '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709',
                          '-c:a', 'aac', '-b:a', '192k', '-shortest', 'v2_tmp.mp4'], stdin=subprocess.PIPE)
    for fr in range(NF): p.stdin.write(bytes(draw(fr).get_data()))
    p.stdin.close(); assert p.wait() == 0
    os.replace('v2_tmp.mp4', 'make_it_original_v2.mp4'); print('frames', NF)
