"""Perfect Date v2.1: the hook and the loop.
v2.1: motion in the first second (MY AI bounces and rubs its mitts, he fidgets), the ask 1.2 s, the rose by ~2 s with
Hoody in the shot, a head-shake bridge into the loop, the pink close-up and the rose trimmed.
v2: Built on render.py (imported, not touched).
- Frame 0 is the ask: on the bench, "HELP ME IMPRESS HER!" already on screen, MY AI leaning in, Eva right there.
- The film ends in the same shot: he crashes onto the bench, dizzy and alone, held 0.8 s. The cut lands on frame 0:
  the same bench, him asking MY AI again. The label resets ITS -> HIS on the cut.
- Cut: the opening close-up, the park wide, the cat-and-dog cutaway, the top-down shot. Trimmed: "Your turn!", the float.
- Clearer: a real hand pump with PFF puffs, ITS DATE pops twice the size and holds 0.8 s, the string snaps on PLONK.
python3 render2.py frames F ... | final"""
import os, sys, math, subprocess, cairo
HERE = os.path.dirname(os.path.abspath(__file__)); PD = os.path.join(HERE, '..')
sys.path.insert(0, PD); _cwd = os.getcwd(); os.chdir(PD)
import render as R
os.chdir(_cwd)
from render import (K, A, E, Sh, W, H, GY, SEAT, park, bench, hoody, ai, bubble, talk, heart, string, sparkles, notes, txt, rr, fs, ell,
                    limb, hx, lerp, cl, ss, oe, NAVY, INK, YEL, WHITE, RED)
ZOOM, ZC = 1.22, (520, 1400)                                          # the bench shot, framed the same at both ends

def bench_shot(c, f):
    c.save(); c.translate(*ZC); c.scale(ZOOM, ZOOM); c.translate(-ZC[0], -ZC[1])
    park(c, f); bench(c, 220, 780, SEAT, GY)
def s_ask(c, f, r):   # frame 0: on the bench, the ask already on screen; MY AI leans in, Eva right there with her coffee
    bench_shot(c, f)
    Sh.cat_one_eye(c, 700, SEAT - 6, .62, open_eye=False)
    col = E.dog(c, 880 - 135 * .9, GY + 40, .72, look=0, f=f)
    hand = E.eva(c, 880, GY + 30, .85, 'evacalm', sip=.2, blink=K.blinking(f, 7))
    E.leash(c, hand, col, sag=40)
    b = abs(math.sin(f * .55)); sq = .06 * b                         # MY AI bounces on its toes, eager, rubbing its mitts
    c.save(); c.translate(170, GY + 50); c.scale(1 + sq * .5, 1 - sq); c.translate(-170, -(GY + 50) - 26 * b)
    ai(c, 170, GY + 50, .9, eye='happy', tilt=12, look=(12, -4), arms=('hold', 'hold'), f=f)
    mx, my = 170 + 70 * .9, GY + 50 - 150 * .9
    for q in (-1, 1): ell(c, mx + q * (14 + 10 * math.sin(f * 1.3)), my + q * 4, 22, 20); fs(c, WHITE, 5)
    c.restore()
    hoody(c, 420, SEAT, .82, expr='hopeful', pose='sit', seat=(220, 780), gaze=-20 + 14 * math.sin(f * .4), rot=.04 * math.sin(f * .7),
          op=.15 + .6 * talk(f, 'h_whisper'), f=f)            # he fidgets, eyes darting to her
    c.restore()
    bubble(c, ['HELP ME', 'IMPRESS HER!'], 20, (440, 1110), cy=600, cx=430)          # full size on frame 0

def s_pump(c, f, r):  # MY AI, the proud stage tech, on a real hand pump: handle down, PFF, the balloon swells
    park(c, f, zoom=1.4, cy=1500)
    rs = 1.25; rx, gy = 330, 1830
    p = max(0, math.sin((r - 6) * math.pi / 6)) if r >= 6 else 0      # one stroke every 12 frames
    px, base = 560, 1900                                               # the pump: a cylinder on a foot plate, T-handle on a rod
    rr(c, px - 110, base - 24, 220, 30, 12); fs(c, hx('3a4152'), 6)
    rr(c, px - 46, base - 430, 92, 410, 30); fs(c, hx('ff8a3d'), 8)
    rr(c, px - 46, base - 300, 92, 34, 10); c.set_source_rgba(1, 1, 1, .3); c.fill()
    hy = base - 560 + 120 * p
    c.rectangle(px - 9, hy, 18, base - 430 - hy); c.set_source_rgb(*hx('c9ced8')); c.fill()
    rr(c, px - 150, hy - 26, 300, 52, 24); fs(c, INK, 6)
    ai(c, rx + 40 * p, gy + 30 * p, rs, eye='happy', arms=('hold', 'hold'), tilt=18, f=f)
    for q in (-1, 1): ell(c, px + q * 110, hy, 34, 30); fs(c, WHITE, 6)                     # its mitts on the handle
    k = cl((r - 6) / 18); bk = 1.4 + 1.2 * k + .06 * math.sin(r * 1.4) * k
    tip = (830, 1000)
    c.move_to(px + 46, base - 60); c.curve_to(px + 200, base - 20, tip[0] + 40, tip[1] + 420, tip[0], tip[1] + 30)   # the hose, pump to balloon
    c.set_source_rgb(*INK); c.set_line_width(30); c.stroke_preserve(); c.set_source_rgb(*hx('ff8a3d')); c.set_line_width(18); c.stroke()
    string(c, tip, (930, 1960)); heart(c, *tip, bk)
    if p > .3:
        for i in range(4):
            a_ = -.5 + i * .8; ell(c, tip[0] + math.cos(a_) * 70 * p, tip[1] + 40 + math.sin(a_) * 40 * p, 16 * p, 16 * p); c.set_source_rgba(1, 1, 1, .9); c.fill()
        txt(c, 'PFF!', tip[0] - 40, tip[1] + 330, 76, NAVY, lw=0)
    if r >= 6: sparkles(c, tip[0], tip[1] + 20, r)

def s_rose(c, f, r):  # the rose, with Hoody in the shot: he watches it work
    park(c, f, zoom=1.2, cy=1450)
    hoody(c, 120, 1830, .78, expr='hopeful', gaze=20, f=f)
    k = oe((r - 2) / 8)
    ai(c, 380, 1720, 1.15, eye='focus', arms=('down', 'offer'), props=(None, A.rose), rot=-.12 * k, f=f)
    E.eva(c, 800, 1760, 1.0, 'impressed' if r >= 8 else 'evacalm', sip=.1, blink=K.blinking(f, 7))

def s_take(c, f, r): R.s11(c, f, min(r, 29))                          # she takes its hand -> ITS DATE (the top-down half is cut)

def s_plonk(c, f, r):  # the insert, the string now snaps and curls back; then his deadpan face
    if r >= 12: R.s15(c, f, r); return
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, *R.SKY0); g.add_color_stop_rgb(1, *R.SKY1); c.set_source(g); c.paint()
    c.save(); c.translate(540, 1100); c.rotate(-.5)
    rr(c, -900, -130, 1800, 260, 30); fs(c, hx('7a4a25'), 10)
    for i in range(-3, 4): c.rectangle(i * 240 - 8, -130, 16, 260); c.set_source_rgb(*hx('d9d9d9')); c.fill()
    for j in range(6):
        yy = -100 + j * 40
        if j == 3 and r >= 4:                                         # SNAP: two ends curling away from the break
            k = oe((r - 4) / 5); bx = 60
            for side in (-1, 1):
                end = bx + side * (30 + 200 * k)
                c.move_to(side * 900, yy); c.line_to(end, yy)
                cx_, cy_ = end, yy - 40 * k
                for a in range(0, 13):
                    t = a / 12 * 2 * math.pi * k; rad = 70 * k * (1 - a / 26)
                    c.line_to(cx_ - side * rad * math.sin(t), cy_ + rad * math.cos(t))
                c.set_source_rgb(*hx('f2f2f2')); c.set_line_width(8); c.stroke()
            if r < 7:                                                 # the spark of the break
                for i in range(6):
                    a = i * math.pi / 3; c.move_to(bx + 20 * math.cos(a), yy + 20 * math.sin(a)); c.line_to(bx + 70 * math.cos(a), yy + 70 * math.sin(a))
                c.set_source_rgb(*YEL); c.set_line_width(8); c.stroke()
            continue
        if j == 3: amp = -26 * r / 4; c.move_to(-900, yy); [c.line_to(xx, yy + amp * math.sin((xx + 900) / 1800 * math.pi)) for xx in range(-900, 901, 30)]
        else: c.move_to(-900, yy); c.line_to(900, yy)
        c.set_source_rgb(*hx('f2f2f2')); c.set_line_width(7 if j < 3 else 5); c.stroke()
    c.restore()
    fx_, fy_ = (600, 1050 - 26) if r < 4 else (700, 1250)
    limb(c, [(820, 1500), (740, 1350), (fx_, fy_)], 90, K.SKIN); ell(c, fx_, fy_, 50, 44); fs(c, K.SKIN, 8)
    if r >= 4: txt(c, 'plonk.', 540, 640, 110, NAVY, lw=0)

def s_land(c, f, r):  # BOOM onto the bench (as v1), then the same bench shot as frame 0: dizzy, alone, held
    if r < 9: R.s20(c, f, r); return
    q = r - 9
    bench_shot(c, f)
    Sh.cat_one_eye(c, 700, SEAT - 6, .62, open_eye=q > 12)
    shake = q >= 24                                                   # the bridge: he shakes it off, the stars fly away, he turns to MY AI
    u = (q - 24) / 5 if shake else 0
    gz = (-20 if u >= .8 else 34 * math.sin(u * 3 * math.pi)) if shake else 0     # rot would tilt the seat plank too: shake with the eyes
    hoody(c, 420, SEAT, .82, expr='spiral' if not shake or u < .35 else 'hopeful', pose='sit', seat=(220, 780),
          gaze=gz, f=f, blink=False)
    hy = SEAT - 520
    for i in range(3):                                                # stars circling his head, flung off on the shake
        a = q * .5 + i * 2.1; fly = 1 + 6 * cl(u) if shake else 1
        if shake and u > .8: break
        c.save(); c.translate(420 + math.cos(a) * 110 * fly, hy + math.sin(a) * 22 * fly - 120 * cl(u)); c.scale(.6, .6); c.move_to(0, -30)
        for j in range(1, 10): rad = 30 if j % 2 == 0 else 12; c.line_to(rad * math.sin(j * math.pi / 5), -rad * math.cos(j * math.pi / 5))
        c.close_path(); fs(c, YEL, 4); c.restore()
    for i in range(5):                                                # the last of the dust
        ell(c, 260 + i * 90, GY - 10, 60, 30); c.set_source_rgba(.88, .80, .64, max(0, .5 - q * .03)); c.fill()
    c.restore()

PLAN = [(s_ask, 36), (R.s5, 18), (s_rose, 27), (R.s7, 33), (R.s8, 24), (s_pump, 30), (R.s10, 52), (s_take, 30), (R.s12, 24),
        (R.s13, 30), (R.s14, 30), (s_plonk, 30), (R.s16, 27), (R.s17, 27), (R.s18, 24), (R.s19, 12), (s_land, 39)]
SHOTS = []; _t = 0
for fn, d in PLAN: SHOTS.append((fn, _t, _t + d)); _t += d
NF = _t
IMPACT, STEPS = R.IMPACT, R.STEPS                                    # audio2.py reads these
TAKE = 7                                                              # index of the hand-take shot
VO = [('h_whisper', 0, .07, .7), ('ai_watch', 1, .2, .6), ('ai_turn', 3, .25, .6), ('h_oh', 9, .35, .55), ('h_whoa', 14, .25, .55)]
R.SHOTS, R.NF, R.VO = SHOTS, NF, VO                                   # talk() reads these
def pill(f): return 'ITS DATE' if f >= SHOTS[TAKE][1] + 8 else 'HIS DATE'
def pulse(c, f):                                                      # twice the size of v1, held 0.8 s
    t = f - (SHOTS[TAKE][1] + 8)
    if not 0 <= t < 24: return
    k = 1 + 1.6 * (1 - ss(cl((t - 12) / 12))) * min(1, t / 2)
    c.select_font_face('Lilita One'); c.set_font_size(58); w = max(200, c.text_extents('ITS DATE').width + 96)
    px, iy = 1020 - w / 2, 222 + 69
    c.save(); c.translate(px - 120 * (k - 1), iy + 90 * (k - 1)); c.scale(k, k)
    rr(c, -w / 2, -44, w, 88, 44); fs(c, YEL, 7); txt(c, 'ITS DATE', 0, 0, 58, INK, lw=0); c.restore()
R.pill, R.pulse = pill, pulse
def draw(f): return R.draw(f)

if __name__ == '__main__':
    if sys.argv[1:2] == ['frames']:
        for f in map(int, sys.argv[2:]): draw(f).write_to_png(os.path.join(HERE, f'chk_{f:03d}.png'))
    else:
        p = subprocess.Popen(f'ffmpeg -y -v error -f rawvideo -pix_fmt bgra -s {W}x{H} -r 30 -i - -vf format=yuv420p -c:v libx264 -crf 14 -preset slow -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 {os.path.join(HERE, "video.mp4")}'.split(), stdin=subprocess.PIPE)
        for f in range(NF): p.stdin.write(bytes(draw(f).get_data()))
        p.stdin.close(); assert p.wait() == 0; print('video', NF, round(NF / 30, 2), 's')
