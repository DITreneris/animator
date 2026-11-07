#!/usr/bin/env python3
# Payday Slot Machine: draws every frame with Pillow and synthesizes the soundtrack with NumPy.
# Usage: render.py check T [T …]  |  render.py scene ID [ID …]  |  render.py audio
import json, math, os, random, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.abspath(__file__))
P = json.load(open(os.path.join(ROOT, 'plan.json')))
W, H, FPS = P['format']['width'], P['format']['height'], P['format']['fps']
DUR = P['format']['duration']
C = P['careers']
FONTS = os.path.join(ROOT, '..', 'fonts')
ANTON = os.path.join(FONTS, 'Anton-Regular.ttf')
ARCH = os.path.join(FONTS, 'ArchivoBlack-Regular.ttf')
PAPER, INK, RED, GOLD = (250, 248, 240), (17, 17, 17), (208, 16, 28), (255, 201, 40)
MX, BW = 110, 860
TOP, BOTTOM, STRIP_H, STRIP_STEP = 400, 1530, 104, 116
REEL_H, REEL_GAP, REEL_PAD = 164, 16, 30
REEL_W = (BW - 2 * REEL_PAD - 3 * REEL_GAP) // 4
_f = {}


def font(path, size):
    k = (path, int(size))
    if k not in _f: _f[k] = ImageFont.truetype(path, int(size))
    return _f[k]


def fit(text, size, maxw, path=None):
    # largest size <= size whose width fits maxw, so text stays on screen with any Anton build
    while size > 10 and font(path or ANTON, size).getlength(text) > maxw: size -= 1
    return size


def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def eout(x): x = clamp(x); return 1 - (1 - x) ** 3
def eback(x): x = clamp(x); s = 1.7; x -= 1; return x * x * ((s + 1) * x + s) + 1
def lerp(a, b, u): return a + (b - a) * u
def hexc(s): s = s.lstrip('#'); return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def text_c(d, xy, s, f, fill): d.text(xy, s, font=f, fill=fill, anchor='mm')


# ---------- original characters, drawn at 1000x1000 and downsampled ----------
def base():
    im = Image.new('RGBA', (1000, 1000), (0, 0, 0, 0)); return im, ImageDraw.Draw(im)


def ch_employee():
    im, d = base(); L = 15
    d.polygon([(90, 1000), (170, 790), (390, 700), (610, 700), (830, 790), (910, 1000)], fill=(255, 255, 255, 255), outline=INK + (255,), width=L)
    d.polygon([(440, 725), (560, 725), (535, 800), (580, 1000), (420, 1000), (465, 800)], fill=INK + (255,))
    d.polygon([(385, 695), (500, 790), (420, 860), (345, 725)], fill=(255, 255, 255, 255), outline=INK + (255,), width=L)
    d.polygon([(615, 695), (500, 790), (580, 860), (655, 725)], fill=(255, 255, 255, 255), outline=INK + (255,), width=L)
    d.rounded_rectangle([285, 90, 715, 720], 200, fill=(158, 158, 158, 255), outline=INK + (255,), width=L)
    d.ellipse([390, 340, 430, 380], fill=INK + (255,)); d.ellipse([570, 340, 610, 380], fill=INK + (255,))
    d.line([(500, 380), (535, 480), (480, 480)], fill=INK + (255,), width=12)
    d.line([(420, 575), (585, 575)], fill=INK + (255,), width=14)
    return im


def ch_freelancer():
    im, d = base(); L = 15; rnd = random.Random(4)
    d.polygon([(70, 1000), (150, 790), (330, 710), (670, 710), (850, 790), (930, 1000)], fill=(38, 38, 42, 255), outline=INK + (255,), width=L)
    d.ellipse([260, 620, 740, 880], fill=(58, 58, 62, 255), outline=INK + (255,), width=L)
    d.polygon([(400, 660), (600, 660), (620, 780), (380, 780)], fill=(247, 232, 214, 255))
    d.ellipse([255, 120, 745, 760], fill=(247, 232, 214, 255), outline=INK + (255,), width=L)
    for _ in range(120):
        a = rnd.uniform(math.pi * 1.02, math.pi * 1.98); r0 = rnd.uniform(205, 250)
        x0, y0 = 500 + r0 * math.cos(a), 380 + r0 * 1.15 * math.sin(a)
        L2 = rnd.uniform(70, 170); b = a + rnd.uniform(-.8, .8)
        d.line([(x0, y0), (x0 + L2 * math.cos(b), y0 + L2 * math.sin(b))], fill=INK + (255,), width=rnd.randint(9, 15))
    for ex in (390, 610):
        d.ellipse([ex - 78, 385, ex + 78, 515], fill=(112, 88, 140, 255))
        d.ellipse([ex - 54, 395, ex + 54, 480], fill=(255, 235, 235, 255), outline=INK + (255,), width=9)
        d.ellipse([ex - 22, 416, ex + 22, 460], fill=(190, 40, 50, 255)); d.ellipse([ex - 9, 430, ex + 9, 448], fill=INK + (255,))
    d.line([(305, 400), (450, 345)], fill=INK + (255,), width=15); d.line([(695, 400), (550, 345)], fill=INK + (255,), width=15)
    d.line([(500, 490), (530, 550), (475, 555)], fill=INK + (255,), width=10)
    d.rounded_rectangle([395, 590, 605, 665], 26, fill=(255, 255, 255, 255), outline=INK + (255,), width=12)
    for x in range(430, 600, 35): d.line([(x, 594), (x, 661)], fill=INK + (255,), width=6)
    d.line([(398, 627), (602, 627)], fill=INK + (255,), width=6)
    for _ in range(70):
        x, y = rnd.uniform(320, 680), rnd.uniform(560, 735)
        if ((x - 500) / 230) ** 2 + ((y - 440) / 310) ** 2 < 1 and not (390 < x < 610 and 585 < y < 670): d.ellipse([x, y, x + 6, y + 6], fill=INK + (255,))
    return im


def ch_founder(sun=False):
    im, d = base(); L = 15
    d.polygon([(90, 1000), (200, 770), (390, 700), (610, 700), (800, 770), (910, 1000)], fill=(24, 24, 26, 255), outline=INK + (255,), width=L)
    d.rounded_rectangle([390, 640, 610, 770], 30, fill=(24, 24, 26, 255))
    d.polygon([(280, 230), (720, 230), (735, 480), (665, 640), (560, 705), (440, 705), (335, 640), (265, 480)], fill=(255, 226, 196, 255), outline=INK + (255,), width=L)
    d.ellipse([235, 350, 300, 480], fill=(255, 226, 196, 255), outline=INK + (255,), width=12)
    d.ellipse([700, 350, 765, 480], fill=(255, 226, 196, 255), outline=INK + (255,), width=12)
    d.polygon([(260, 330), (250, 180), (350, 95), (560, 70), (720, 130), (755, 240), (735, 340), (700, 245), (530, 225), (360, 250), (300, 280)], fill=(248, 206, 85, 255), outline=INK + (255,), width=L)
    d.line([(370, 110), (620, 205)], fill=(200, 155, 45, 255), width=11); d.line([(500, 90), (690, 195)], fill=(200, 155, 45, 255), width=11)
    if sun:
        d.rounded_rectangle([315, 345, 485, 450], 22, fill=INK + (255,)); d.rounded_rectangle([515, 345, 685, 450], 22, fill=INK + (255,))
        d.line([(280, 380), (720, 380)], fill=INK + (255,), width=20)
        d.line([(345, 370), (395, 370)], fill=(255, 255, 255, 255), width=10); d.line([(545, 370), (595, 370)], fill=(255, 255, 255, 255), width=10)
        d.arc([400, 520, 660, 640], 15, 150, fill=INK + (255,), width=15)
    else:
        for ex in (400, 600):
            d.ellipse([ex - 45, 380, ex + 45, 430], fill=(255, 255, 255, 255), outline=INK + (255,), width=9)
            d.ellipse([ex - 16, 388, ex + 16, 424], fill=INK + (255,))
        d.line([(340, 350), (455, 350)], fill=INK + (255,), width=16); d.line([(545, 350), (660, 350)], fill=INK + (255,), width=16)
        d.line([(445, 590), (565, 590)], fill=INK + (255,), width=14)
    d.line([(500, 435), (525, 515), (480, 520)], fill=INK + (255,), width=10)
    return im


def ch_coder():
    im, d = base(); L = 15
    d.polygon([(250, 1000), (290, 790), (390, 725), (610, 725), (710, 790), (750, 1000)], fill=(255, 255, 255, 255), outline=INK + (255,), width=L)
    for pts, cx, cy in (([(305, 815), (180, 690), (130, 560)], 120, 505), ([(695, 815), (820, 690), (870, 560)], 880, 505)):
        d.line(pts, fill=INK + (255,), width=62, joint='curve'); d.line(pts, fill=(255, 255, 255, 255), width=34, joint='curve')
        d.ellipse([cx - 70, cy - 70, cx + 70, cy + 70], fill=(255, 255, 255, 255), outline=INK + (255,), width=L)
        for k in (-28, 4, 34): d.line([(cx + k, cy - 42), (cx + k, cy - 10)], fill=INK + (255,), width=8)
    d.ellipse([235, 225, 765, 785], fill=(255, 255, 255, 255), outline=INK + (255,), width=L)
    hat = [(340, 305), (640, 275), (455, 20)]
    d.polygon(hat, fill=(255, 92, 130, 255), outline=INK + (255,), width=L)
    d.polygon([(382, 200), (577, 180), (612, 235), (358, 263)], fill=(255, 215, 40, 255))
    d.polygon([(420, 120), (523, 110), (546, 145), (402, 160)], fill=(55, 135, 240, 255))
    d.polygon(hat, outline=INK + (255,), width=L)
    d.ellipse([415, -15, 495, 65], fill=(255, 215, 40, 255), outline=INK + (255,), width=12)
    for ex, r in ((395, 70), (610, 78)):
        d.ellipse([ex - r, 340, ex + r, 340 + 2 * r], fill=(255, 255, 255, 255), outline=INK + (255,), width=12)
        d.ellipse([ex - 25, 375, ex + 25, 425], fill=INK + (255,))
    d.chord([300, 400, 700, 740], 10, 170, fill=(190, 25, 40, 255))
    d.rectangle([322, 600, 678, 642], fill=(255, 255, 255, 255))
    d.line([(322, 642), (678, 642)], fill=INK + (255,), width=8)
    for x in range(365, 660, 45): d.line([(x, 602), (x, 642)], fill=INK + (255,), width=6)
    d.chord([300, 400, 700, 740], 10, 170, outline=INK + (255,), width=15)
    return im


CH = {'employee': ch_employee, 'freelancer': ch_freelancer, 'founder': ch_founder, 'founder_sun': lambda: ch_founder(True), 'coder': ch_coder}
_ch = {}
def char(kind, h):
    k = (kind, int(h))
    if k not in _ch:
        if kind not in _ch: _ch[kind] = CH[kind]()
        _ch[k] = _ch[kind].resize((int(h), int(h)), Image.LANCZOS)
    return _ch[k]


# ---------- reels ----------
POOL = ['$3k', '$900', '$0', '$600k', '-$200', '$1.5k', '$500', '$2k', '$7', '$40k', '?']
REELS = []
for i, c in enumerate(C):
    row = []
    for j in range(4):
        spin_at = c['start'] + 0.3
        D = max(10, int((c['stops'][j] - spin_at) * 18))
        rnd = random.Random(100 * i + j)
        seq = ['?'] + [rnd.choice(POOL) for _ in range(D - 1)] + [c['values'][j]] + [rnd.choice(POOL)]
        row.append(dict(t0=spin_at, t1=c['stops'][j], D=D, seq=seq, ink=hexc(c['ink'])))
    REELS.append(row)


def reel_pos(r, t):
    if t <= r['t0']: return 0.0
    if t < r['t1']:
        p = (t - r['t0']) / (r['t1'] - r['t0'])
        return r['D'] * (1 - (1 - p) ** 2.4)
    s = t - r['t1']
    return r['D'] + 0.13 * math.exp(-9 * s) * math.sin(s * 22)


_strips = {}
def strip_img(i, j, blur):
    k = (i, j, blur)
    if k in _strips: return _strips[k]
    r = REELS[i][j]; n = len(r['seq'])
    im = Image.new('RGBA', (REEL_W, REEL_H * n), (255, 255, 255, 255)); d = ImageDraw.Draw(im)
    for q, s in enumerate(r['seq']):
        col = r['ink'] if q == r['D'] else ((RED if s.startswith('-') else INK))
        size = 92
        while font(ANTON, size).getlength(s) > REEL_W - 38: size -= 2
        text_c(d, (REEL_W / 2, REEL_H * q + REEL_H / 2), s, font(ANTON, size), col + (255,))
    if blur:
        a = np.asarray(im).astype(np.float32)
        kern = 71; c = np.cumsum(np.pad(a, ((kern // 2 + 1, kern // 2), (0, 0), (0, 0)), mode='edge'), axis=0)
        im = Image.fromarray(((c[kern:] - c[:-kern]) / kern).astype(np.uint8), 'RGBA')
    _strips[k] = im
    return im


def draw_reels(im, i, x, y, t):
    d = ImageDraw.Draw(im)
    for j in range(4):
        rx = x + REEL_PAD + j * (REEL_W + REEL_GAP)
        text_c(d, (rx + REEL_W / 2, y - 26), P['months'][j], font(ARCH, 28), INK + (255,))
        r = REELS[i][j]; pos = reel_pos(r, t)
        speed = (reel_pos(r, t + .02) - pos) / .02
        st = strip_img(i, j, speed > 7)
        top = int(pos * REEL_H)
        crop = st.crop((0, top, REEL_W, top + REEL_H)).convert('RGBA')
        if speed > 7: pass
        im.paste(crop, (rx, y))
        d.rectangle([rx, y, rx + REEL_W, y + REEL_H], outline=INK + (255,), width=8)
        if t >= r['t1'] and r['seq'][r['D']] == '$600k':
            d.rectangle([rx + 8, y + 8, rx + REEL_W - 8, y + REEL_H - 8], outline=GOLD + (255,), width=7)


# ---------- machine and summary strip ----------
def active_top(i): return TOP + i * STRIP_STEP


def machine(i, t):
    c = C[i]; top = active_top(i); h = BOTTOM - top
    tint = hexc(c['tint'])
    if i == 2 and t >= c['stops'][3]: tint = GOLD
    im = Image.new('RGBA', (BW, h), tint + (255,)); d = ImageDraw.Draw(im)
    name_size = fit(c['name'], 112 if h > 950 else 92, BW - 80)
    text_c(d, (BW / 2, name_size * 0.62 + 12), c['name'], font(ANTON, name_size), INK + (255,))
    cap = c['caption']
    if i == 2 and t >= c['stops'][3]: cap = 'JACKPOT'
    cap_y = name_size * 1.22 + 22
    text_c(d, (BW / 2, cap_y), cap, font(ARCH, 40 if cap != 'JACKPOT' else 46), (RED if cap == 'JACKPOT' else INK) + (255,))
    ry = h - REEL_H - 24
    area_top = int(cap_y + 28); area = ry - 40 - area_top
    ch_h = max(150, area)
    cx = BW / 2; cy = area_top + area / 2
    if i == 0:
        ci = char('employee', ch_h)
        im.alpha_composite(ci, (int(cx - ch_h / 2), area_top))
    elif i == 1:
        jit = math.sin(t * 75) * 3 + (math.sin(t * 31) * 2)
        ci = char('freelancer', ch_h)
        im.alpha_composite(ci, (int(cx - ch_h / 2 + jit), area_top))
        for k, (sx, sy) in enumerate(((0.2, 0.28), (0.8, 0.22), (0.72, 0.42))):
            ph = (t * .85 + k * .37) % 1
            dx = cx - ch_h / 2 + sx * ch_h + jit; dy = area_top + (sy + ph * .24) * ch_h; s = ch_h * .022
            d.polygon([(dx, dy - s * 1.7), (dx - s, dy), (dx + s, dy)], fill=(70, 170, 245, 255))
            d.ellipse([dx - s, dy - s, dx + s, dy + s], fill=(70, 170, 245, 255))
    elif i == 2:
        j = c['stops'][3]; ci = char('founder_sun' if t >= j + .28 else 'founder', ch_h)
        im.alpha_composite(ci, (int(cx - ch_h / 2), area_top))
        if j <= t < j + .28:
            g = char('founder_sun', ch_h).crop((int(.27 * ch_h), int(.33 * ch_h), int(.72 * ch_h), int(.46 * ch_h)))
            y0 = lerp(-.1, .33, eout((t - j) / .28))
            im.alpha_composite(g, (int(cx - ch_h / 2 + .27 * ch_h), max(0, int(area_top + y0 * ch_h))))
    else:
        cheers = sum(t >= s for s in c['stops'])
        bounce = abs(math.sin((t - c['start']) * 7.2)) * ch_h * (.03 + .018 * cheers)
        rot = math.sin((t - c['start']) * 7.2) * (2 + cheers * .8)
        ci = char('coder', ch_h).rotate(rot, Image.BICUBIC)
        im.alpha_composite(ci, (int(cx - ch_h / 2), max(0, int(area_top - bounce))))
    draw_reels(im, i, 0, ry, t)
    d = ImageDraw.Draw(im); d.rectangle([0, 0, BW - 1, h - 1], outline=INK + (255,), width=10)
    return im


_st = {}
def summary(i):
    if i in _st: return _st[i]
    c = C[i]; im = Image.new('RGBA', (BW, STRIP_H), hexc(c['tint']) + (255,)); d = ImageDraw.Draw(im)
    d.text((26, STRIP_H / 2), c['name'], font=font(ANTON, 52), fill=INK + (255,), anchor='lm')
    x = BW - 22
    for v in reversed(c['values']):
        col = RED if v.startswith('-') else INK
        d.text((x, STRIP_H / 2), v, font=font(ANTON, 42), fill=col + (255,), anchor='rm')
        x -= max(92, font(ANTON, 42).getlength(v) + 22)
    d.rectangle([0, 0, BW - 1, STRIP_H - 1], outline=INK + (255,), width=8)
    _st[i] = im
    return im


# ---------- particles ----------
COLS = [(255, 92, 130), (255, 215, 40), (55, 135, 240), (60, 200, 120), (250, 120, 40)]
def confetti(d, t, t0, n=46, seed=1, x0=540, y0=950, power=1.0):
    u = t - t0
    if u <= 0 or u > 2.2: return
    rnd = random.Random(seed)
    for _ in range(n):
        a = rnd.uniform(-math.pi * .95, -math.pi * .05); sp = rnd.uniform(500, 1400) * power; col = rnd.choice(COLS); s = rnd.uniform(9, 19); sp2 = rnd.uniform(5, 15); ph = rnd.uniform(0, 6)
        x = x0 + math.cos(a) * sp * u * math.exp(-.7 * u); y = y0 + math.sin(a) * sp * u * math.exp(-.7 * u) + 500 * u * u
        r = ph + u * sp2; cs, sn = math.cos(r) * s, math.sin(r) * s
        d.polygon([(x + cs, y + sn), (x - sn * .55, y + cs * .55), (x - cs, y - sn), (x + sn * .55, y - cs * .55)], fill=col)


def coins(d, t, t0):
    u = t - t0
    if u <= 0: return
    rnd = random.Random(9)
    for _ in range(70):
        x0 = rnd.uniform(60, 1020); dly = rnd.uniform(0, .75); sp = rnd.uniform(1050, 1800); r = rnd.uniform(26, 48); w = rnd.uniform(5, 12)
        if u < dly: continue
        y = -80 + (u - dly) * sp
        if y > H + 80: continue
        sq = abs(math.cos((u - dly) * w)) * .85 + .15
        d.ellipse([x0 - r * sq, y - r, x0 + r * sq, y + r], fill=GOLD, outline=INK, width=4)
        if sq > .5: text_c(d, (x0, y), '$', font(ANTON, r * 1.15), INK)


def rays(d, t, cx, cy):
    for k in range(16):
        a = t * .8 + k * math.pi / 8; da = math.pi / 17
        d.polygon([(cx, cy), (cx + 1600 * math.cos(a - da), cy + 1600 * math.sin(a - da)), (cx + 1600 * math.cos(a + da), cy + 1600 * math.sin(a + da))], fill=(255, 225, 105))


# ---------- frames ----------
TITLE = fit('CHOOSE YOUR CAREER', 128, 1000)
HOOK = fit('CAREER', 275, 1000 / 1.45)
ENDL = min(fit(x, 165, 960) for x in P['endline'])
def title(frame, y=None, t=0):
    d = ImageDraw.Draw(frame)
    f = font(ANTON, TITLE)
    d.text((540, 306), 'CHOOSE YOUR CAREER', font=f, fill=INK, anchor='mm')


def hook(t):
    im = Image.new('RGB', (W, H), PAPER); d = ImageDraw.Draw(im)
    ws = [('CHOOSE', .05, 1040 - 300), ('YOUR', .36, 950), ('CAREER', .67, 1160)]
    words = [('CHOOSE', .05, 720), ('YOUR', .36, 960), ('CAREER', .67, 1200)]
    u = eout((t - 1.0) / .25) if t > 1.0 else 0
    if u > 0:
        im = Image.new('RGB', (W, H), PAPER); d = ImageDraw.Draw(im)
    for s, ts, y in words:
        if t < ts: continue
        k = eback((t - ts) / .14)
        size = lerp(HOOK * (1.45 - .45 * k), TITLE, u)
        yy = lerp(y, 306, u)
        xx = 540
        if u > 0:
            tf = font(ANTON, size); tl = tf.getlength('CHOOSE YOUR CAREER'); pre = {'CHOOSE': '', 'YOUR': 'CHOOSE ', 'CAREER': 'CHOOSE YOUR '}[s]
            offs = -tl / 2 + tf.getlength(pre) + tf.getlength(s) / 2
            xx = 540 + offs * u ** .45
        d.text((xx, yy), s, font=font(ANTON, size), fill=INK, anchor='mm')
    return im


def body(t):
    im = Image.new('RGB', (W, H), PAPER); d = ImageDraw.Draw(im)
    if 10.9 <= t < 12.2: rays(d, t, 540, 960)
    title(im)
    # shake offset applies to the board
    sx, sy = 0, 0
    if 10.9 <= t < 11.35:
        v = 1 - (t - 10.9) / .45
        sx, sy = int(math.sin(t * 95) * 24 * v), int(math.cos(t * 83) * 24 * v)
    for s in C[3]['stops']:
        if s <= t < s + .18:
            v = 1 - (t - s) / .18; sx += int(math.sin(t * 110) * 13 * v); sy += int(math.cos(t * 97) * 11 * v)
    i = max(k for k in range(4) if C[k]['start'] <= t)
    for k in range(i):
        im.paste(summary(k), (MX + sx, TOP + k * STRIP_STEP + sy))
    u = clamp((t - C[i]['start']) / .32)
    # hide the new strip until the old machine has folded into it
    if i > 0 and u < 1:
        old_y0 = active_top(i - 1); old_h = BOTTOM - old_y0
        y = lerp(old_y0, TOP + (i - 1) * STRIP_STEP, u); h = lerp(old_h, STRIP_H, eout(u))
        # paper out the strip while folding
        d.rectangle([MX, TOP + (i - 1) * STRIP_STEP, MX + BW, TOP + (i - 1) * STRIP_STEP + STRIP_H], fill=PAPER)
        im_old = machine(i - 1, C[i]['start'] - .001).resize((BW, max(10, int(h))), Image.BILINEAR)
        im.paste(im_old, (MX, int(y)))
        if eout(u) > .78: im.paste(summary(i - 1), (MX, TOP + (i - 1) * STRIP_STEP))
    mach = machine(i, t)
    y = lerp(H + 20, active_top(i), eout(u))
    im.paste(mach, (MX + sx, int(y) + sy))
    d = ImageDraw.Draw(im)
    if t >= 10.9 and i == 2:
        coins(d, t, 10.9)
    if i == 3:
        for n, s in enumerate(C[3]['stops']): confetti(d, t, s, seed=20 + n, x0=MX + REEL_PAD + n * (REEL_W + REEL_GAP) + REEL_W / 2, y0=1320, power=.55)
    return im


def endframe(t):
    u = t - 16.2
    im = Image.new('RGB', (W, H), (255, 231, 90)); d = ImageDraw.Draw(im)
    rays_col = (255, 243, 160)
    for k in range(14):
        a = t * .35 + k * math.pi / 7; da = math.pi / 15
        d.polygon([(540, 1050), (540 + 1600 * math.cos(a - da), 1050 + 1600 * math.sin(a - da)), (540 + 1600 * math.cos(a + da), 1050 + 1600 * math.sin(a + da))], fill=rays_col)
    ch_h = 720; bounce = abs(math.sin(u * 6.5)) * 30; rot = math.sin(u * 6.5) * 5
    confetti(d, t, 16.3, n=70, seed=77, x0=540, y0=1120, power=1.05)
    confetti(d, t, 17.3, n=50, seed=78, x0=540, y0=1120, power=1.05)
    ci = char('coder', ch_h).rotate(rot, Image.BICUBIC)
    y0 = lerp(1920, 765, eback(u / .35)) - bounce
    im.paste(ci, (int(540 - ch_h / 2), int(y0)), ci)
    for k, s in enumerate(P['endline']):
        ts = .12 + k * .22
        if u < ts: continue
        q = eback((u - ts) / .16); size = ENDL * (1.3 - .3 * q)
        y = 280 + k * 160
        d.text((540, y), s, font=font(ANTON, size), fill=INK, anchor='mm', stroke_width=0)
    # scrolling bill along the bottom safe line
    if u > .75:
        band_y = 1450
        d.rectangle([0, band_y, W, band_y + 100], fill=INK)
        scroll = (u - .75) * 240
        s = '-$200   ' * 14
        d.text((-scroll % 240 - 240, band_y + 50), s, font=font(ANTON, 72), fill=(255, 70, 70), anchor='lm')
    return im


def frame(t):
    if t < C[0]['start']: return hook(t)
    if t < 16.2: return body(t)
    if t < 16.4:
        a = (t - 16.2) / .2
        return Image.blend(body(16.199), endframe(t), a)
    return endframe(t)


# ---------- audio ----------
SR = 44100
def add(buf, t, x, gain=1.0):
    s = int(t * SR); e = min(len(buf), s + len(x))
    if s < len(buf): buf[s:e] += x[:e - s] * gain


def env(n, d): return np.exp(-np.arange(n) / SR / d)
def tone(f, dur, wave='sine', d=.15):
    n = int(dur * SR); tt = np.arange(n) / SR; ph = 2 * np.pi * f * tt
    y = np.sin(ph) if wave == 'sine' else 2 * ((tt * f) % 1) - 1 if wave == 'saw' else np.sign(np.sin(ph))
    return y * env(n, d)


def sweep(f0, f1, dur, wave='saw'):
    n = int(dur * SR); fr = np.linspace(f0, f1, n); ph = np.cumsum(2 * np.pi * fr / SR)
    y = np.sin(ph) if wave == 'sine' else 2 * ((ph / (2 * np.pi)) % 1) - 1
    w = np.minimum(1, np.minimum(np.arange(n) / 600, (n - np.arange(n)) / 2400))
    return y * w


def audio(path):
    n = int(DUR * SR); buf = np.zeros(n); rnd = np.random.default_rng(3)
    noise = rnd.standard_normal(SR)
    tick = np.sin(2 * np.pi * 1900 * np.arange(1000) / SR) * env(1000, .004)
    thunk = tone(95, .22, 'sine', .07) * 1.0 + noise[:int(.22 * SR)] * env(int(.22 * SR), .008) * .22
    bass = {0: 55.0, 1: 65.41, 2: 49.0, 3: 73.42}
    beat = .5
    for q in range(int(DUR / beat)):
        tb = q * beat
        if 9.2 < tb < 10.9 or tb > 16.0: continue
        add(buf, tb, tone(bass[(q // 2) % 4], .3, 'sine', .11), .23)
        add(buf, tb + beat / 2, noise[:1800] * env(1800, .006), .03)
    for ts in (.05, .36, .67):
        add(buf, ts, tone(62, .32, 'sine', .11) + noise[:int(.32 * SR)] * env(int(.32 * SR), .01) * .3, .95)
    for i, row in enumerate(REELS):
        for j, r in enumerate(row):
            last = 0; ft = r['t0']
            while ft < r['t1']:
                c = int(reel_pos(r, ft))
                if c != last:
                    add(buf, ft, tick, .1); last = c
                ft += 1 / 240
            g = .75
            add(buf, r['t1'], thunk, g)
    # employee beep
    for s in C[0]['stops']: add(buf, s, tone(440, .18, 'square', .06), .08)
    for s, f in zip(C[1]['stops'], (330, 494, 262, 587)): add(buf, s, tone(f, .24, 'square', .07), .11)
    for s in C[2]['stops'][:3]: add(buf, s, sweep(220, 120, .22, 'saw'), .12)
    # heartbeat suspense
    for tb in np.arange(9.3, 10.85, .42):
        add(buf, tb, tone(58, .18, 'sine', .05), .55); add(buf, tb + .14, tone(50, .16, 'sine', .05), .4)
    # jackpot
    for k, f in enumerate((523.25, 659.25, 783.99, 1046.5, 1318.5, 1567.98)):
        add(buf, 10.9 + k * .08, tone(f, .55, 'square', .22), .17)
    for k in range(22):
        tc = 10.98 + k * .055 + rnd.uniform(-.01, .01)
        add(buf, tc, np.sin(2 * np.pi * rnd.uniform(3200, 5200) * np.arange(2600) / SR) * env(2600, .018), .12)
    # vibe coder: every bill bites, every cheer is happy
    for s in C[3]['stops']:
        add(buf, s, sweep(520, 170, .2, 'saw'), .16)
        add(buf, s + .08, noise[:int(.11 * SR)] * env(int(.11 * SR), .03), .09)
    add(buf, 14.62, sweep(420, 980, .42, 'saw'), .15)
    # end: party horn, then a small sad trombone
    add(buf, 16.32, sweep(390, 1050, .55, 'saw'), .19)
    for ts, f0, f1, dd in ((17.0, 311, 293, .24), (17.27, 293, 277, .24), (17.54, 277, 262, .24), (17.81, 262, 220, .72)):
        add(buf, ts, sweep(f0, f1, dd, 'saw'), .17)
    # short fade at the very end
    fade = int(.15 * SR); buf[-fade:] *= np.linspace(1, 0, fade)
    # soft clip and normalize to -2.5 dBFS
    buf = np.tanh(buf * 1.05); buf = buf / max(1e-6, np.max(np.abs(buf))) * (10 ** (-2.5 / 20))
    pcm = (np.clip(buf, -1, 1) * 32767).astype('<i2')
    st = np.stack((pcm, pcm), 1)
    import wave
    w = wave.open(path, 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes()); w.close()


# ---------- output ----------
def render_scene(sc, out):
    a, b = int(round(sc['start'] * FPS)), int(round(sc['end'] * FPS))
    tmp = out + '.tmp.mp4'
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p', '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', '-threads', '4',
                          '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv', '-an', tmp], stdin=subprocess.PIPE)
    for f in range(a, b): p.stdin.write(frame(f / FPS).tobytes())
    p.stdin.close()
    if p.wait() != 0: sys.exit(f'ffmpeg failed on {sc["id"]}')
    os.replace(tmp, out)


def main():
    cmd, args = (sys.argv[1], sys.argv[2:]) if len(sys.argv) > 1 else ('', [])
    if cmd == 'check' and args:
        os.makedirs(os.path.join(ROOT, 'check'), exist_ok=True)
        for s in args:
            out = os.path.join(ROOT, 'check', f't{float(s):05.2f}.png'); frame(float(s)).save(out); print(out)
    elif cmd == 'scene':
        os.makedirs(os.path.join(ROOT, 'scenes'), exist_ok=True)
        for sc in P['scenes']:
            if not args or sc['id'] in args:
                render_scene(sc, os.path.join(ROOT, 'scenes', sc['id'] + '.mp4')); print('rendered', sc['id'], flush=True)
    elif cmd == 'audio':
        audio(os.path.join(ROOT, 'audio.wav'))
    else:
        sys.exit(__doc__ or 'usage: render.py check T… | scene [ID…] | audio')


if __name__ == '__main__':
    main()
