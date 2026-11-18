"""Perfect Date v2.3: the bench version (v2.1) again, with its composition fixed and a real loop.
v2.3: MY AI stands on the path in front of the bench, fully in frame; Eva is not cropped; nothing covers a face or a body.
The ending walks MY AI and Eva back into exactly their frame-0 places while he shakes off the stars and turns to MY AI,
so the last frame is frame 0 minus the bubble. The fall is him with speed lines; PFF! is bigger. (v2.2 is dropped.)
v2.1:
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
# ---- v2.3: one size rule for the whole film. Hoody and Eva are the same height; MY AI is 0.6 of it (1.07 x their scale).
# Only distance from the camera changes a character's size, and it changes everyone in that plane together.
# The v1 shots below each set their own scales (MY AI from 0.52 to 0.93 of Eva); they are re-scaled from their own source.
import inspect as _insp
def _rescale(name, pairs):
    src = _insp.getsource(getattr(R, name))
    for a, b in pairs:
        assert src.count(a) == 1, (name, a); src = src.replace(a, b)
    exec(compile(src, f'render.py:{name}', 'exec'), R.__dict__)
_rescale('s5', [("ai(c, 400, 1780, 1.6,", "ai(c, 400, 1780, 1.08,"),
                ("bubble(c, ['WATCH!'], r - 4, (400 + 14 * 1.6, 1780 - 420 * 1.6)", "bubble(c, ['WATCH!'], r - 4, (400 + 14 * 1.08, 1780 - 420 * 1.08 - 10)")])                       # Eva .95 -> MY AI 1.02, a step nearer the camera
_rescale('s7', [("rx, rs = 770, 1.15", "rx, rs = 770, 1.07")])                              # Hoody 1.0
_rescale('s10', [("hand = E.eva(c, 880, GY + 40, .9,", "hand = E.eva(c, 880, GY + 40, .8,"),   # Hoody .78
                 ("ai(c, 100, GY + 70, .85,", "ai(c, 100, GY + 70, .84,")])
_rescale('s11', [("rs = 1.3; rx = 330;", "rs = 1.02; rx = 330;")])                         # Eva .95
ZOOM, ZC = 1.14, (560, 1400)                                          # the bench shot, framed the same at both ends

def bench_shot(c, f):
    c.save(); c.translate(*ZC); c.scale(ZOOM, ZOOM); c.translate(-ZC[0], -ZC[1])
    park(c, f); bench(c, 220, 780, SEAT, GY)
AI_X, EVA_X = 255, 885                                               # frame-0 places (bench coordinates), shared with the ending
def bench_people(c, f, ai_x=AI_X, eva_x=EVA_X, ai_walk=None, eva_walk=None, bounce=True):
    """Eva with the dog on the right, MY AI on the path in front of the bench's left end (drawn in front of the bench)."""
    col = E.dog(c, eva_x - 120, GY + 40, .72, look=0, f=f)
    hand = E.eva(c, eva_x, GY + 30, .85, 'evacalm', sip=.2, walk=eva_walk, blink=K.blinking(f, 7))
    E.leash(c, hand, col, sag=40)
    b = abs(math.sin(f * .55)) if bounce else 0; sq = .06 * b         # MY AI bounces on its toes, eager, rubbing its mitts
    c.save(); c.translate(ai_x, GY + 70); c.scale(1 + sq * .5, 1 - sq); c.translate(-ai_x, -(GY + 70) - 26 * b)
    ai(c, ai_x, GY + 70, .88, eye='happy', tilt=10 if bounce else 0, look=(12, -4), arms=('hold', 'hold') if bounce else ('down', 'down'), walk=ai_walk, f=f)
    if bounce:
        mx, my = ai_x + 70 * .9, GY + 70 - 150 * .9
        for q in (-1, 1): ell(c, mx + q * (14 + 10 * math.sin(f * 1.3)), my + q * 4, 22, 20); fs(c, WHITE, 5)
    c.restore()

def s_ask(c, f, r):   # frame 0: on the bench, the ask already on screen; MY AI in front of the bench, eager; Eva right there
    bench_shot(c, f)
    Sh.cat_one_eye(c, 705, SEAT - 6, .62, open_eye=False)
    hoody(c, 500, SEAT, .82, expr='hopeful', pose='sit', seat=(220, 780), gaze=-20 + 14 * math.sin(f * .4),
          op=.15 + .6 * talk(f, 'h_whisper'), f=f)                      # he fidgets, eyes darting (no rot: it tilts the seat plank)
    bench_people(c, f)
    c.restore()
    bubble(c, ['HELP ME', 'IMPRESS HER!'], 20, (600, 975), cy=560, cx=600)          # full size on frame 0

def s_pump(c, f, r):  # MY AI on a floor pump: both mitts on the T-handle, it pushes down with its whole body; PFF, the balloon swells
    park(c, f, zoom=1.2, cy=1450)
    rs = 1.25; rx, gy = 380, 1580
    p = max(0, math.sin((r - 6) * math.pi / 6)) if r >= 6 else 0      # one stroke every 12 frames: 0 = handle up, 1 = pushed down
    dy = 40 * p                                                        # it sinks with the stroke, the hands take the handle down
    GRIP = (94, -140)                                                  # both hands in front of its chest (the reachable pose closest to a pump grip)
    hands = [A.hand_at(rx, gy + dy, rs, q, GRIP) for q in (-1, 1)]
    hx_ = (hands[0][0] + hands[1][0]) / 2; hy_ = (hands[0][1] + hands[1][1]) / 2
    base = gy + 70                                                     # the pump stands on the path right in front of it
    top = hy_ - dy + 40 + 22                                           # the cylinder ends just below the handle's lowest point
    c.save(); c.translate(rx, gy + dy); c.scale(1 + .05 * p, 1 - .08 * p); c.translate(-rx, -(gy + dy))
    ai(c, rx, gy + dy, rs, eye='happy', arms=(GRIP, GRIP), f=f)
    c.restore()
    rr(c, hx_ - 120, base - 26, 240, 32, 12); fs(c, hx('3a4152'), 6)                       # foot plate
    rr(c, hx_ - 62, top, 124, base - 20 - top, 30); fs(c, hx('ff8a3d'), 8)                # cylinder, in front of its legs
    rr(c, hx_ - 62, top + 30, 124, 26, 10); c.set_source_rgba(1, 1, 1, .3); c.fill()
    c.rectangle(hx_ - 9, hy_, 18, top - hy_); c.set_source_rgb(*hx('c9ced8')); c.fill()     # the rod, from the cylinder up to the handle
    half = abs(hands[1][0] - hands[0][0]) / 2 + 50
    rr(c, hx_ - half, hy_ - 24, 2 * half, 48, 24); fs(c, INK, 6)                           # the T-handle, exactly where its hands are
    for hx2, hy2 in hands: ell(c, hx2, hy2, 36, 32); fs(c, WHITE, 6)                       # its mitts gripping the handle
    k = cl((r - 6) / 18); bk = 1.4 + 1.2 * k + .06 * math.sin(r * 1.4) * k
    tip = (840, 860)
    c.move_to(hx_ + 44, base - 60); c.curve_to(hx_ + 220, base - 10, tip[0] + 40, tip[1] + 420, tip[0], tip[1] + 30)   # the hose, pump to balloon
    c.set_source_rgb(*INK); c.set_line_width(30); c.stroke_preserve(); c.set_source_rgb(*hx('ff8a3d')); c.set_line_width(18); c.stroke()
    string(c, tip, (hx_ + 30, base - 30)); heart(c, *tip, bk)            # tied to the pump's foot
    if p > .3:
        for i in range(4):
            a_ = -.5 + i * .8; ell(c, tip[0] + math.cos(a_) * 70 * p, tip[1] + 40 + math.sin(a_) * 40 * p, 16 * p, 16 * p); c.set_source_rgba(1, 1, 1, .9); c.fill()
        txt(c, 'PFF!', tip[0] - 250, tip[1] - 60, 130, NAVY, lw=10)
    if r >= 6: sparkles(c, tip[0], tip[1] + 20, r)

def s_rose(c, f, r):  # the rose, with Hoody in the shot: he watches it work
    park(c, f, zoom=1.2, cy=1450)
    hoody(c, 140, 1800, .9, expr='hopeful', gaze=20, f=f)
    k = oe((r - 2) / 8)
    ai(c, 470, 1760, .96, eye='focus', arms=('down', 'offer'), props=(None, A.rose), rot=-.12 * k, f=f)
    E.eva(c, 850, 1760, .9, 'impressed' if r >= 8 else 'evacalm', sip=.1, blink=K.blinking(f, 7))

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

def s_land(c, f, r):  # the fall, BOOM onto the bench, dizzy 0.5 s; then MY AI and Eva walk back to their frame-0 places
    if r < R.IMPACT:                                                  # him, falling, with speed lines (the old streak read as 'a dark bar')
        park(c, f); bench(c, 220, 780, SEAT, GY); Sh.cat_one_eye(c, 700, SEAT - 6, .62, open_eye=False)
        y = SEAT - 900 + r * 300
        for i in range(5): c.move_to(330 + i * 45, y - 520 - i * 20); c.line_to(330 + i * 45, y - 900 - i * 20); c.set_source_rgba(1, 1, 1, .95); c.set_line_width(9); c.stroke()
        hoody(c, 420, y, .82, expr='shock', pose='float', arms=('flail', 'flail'), legs='pedal', f=f, blink=False); return
    if r < 9: R.s20(c, f, r); return
    q = r - 9
    bench_shot(c, f)
    Sh.cat_one_eye(c, 705, SEAT - 6, .62, open_eye=5 < q < 15)
    shake = q >= 15; u = (q - 15) / 7 if shake else 0
    gz = (-20 if u >= 1 else 34 * math.sin(u * 3 * math.pi)) if shake else 0
    hoody(c, 500, SEAT, .82, expr='spiral' if not shake or u < .4 else 'hopeful', pose='sit', seat=(220, 780), gaze=gz, f=f, blink=False)
    hy = SEAT - 520
    for i in range(3):                                                # stars circling his head, flung off on the shake
        if shake and u > .8: break
        a = q * .5 + i * 2.1; fly = 1 + 6 * cl(u) if shake else 1
        c.save(); c.translate(500 + math.cos(a) * 110 * fly, hy + math.sin(a) * 22 * fly - 120 * cl(u)); c.scale(.6, .6); c.move_to(0, -30)
        for j in range(1, 10): rad = 30 if j % 2 == 0 else 12; c.line_to(rad * math.sin(j * math.pi / 5), -rad * math.cos(j * math.pi / 5))
        c.close_path(); fs(c, YEL, 4); c.restore()
    for i in range(5):                                                # the last of the dust
        ell(c, 260 + i * 90, GY - 10, 60, 30); c.set_source_rgba(.88, .80, .64, max(0, .5 - q * .03)); c.fill()
    if q >= 12:                                                       # they walk back in, in front of the bench, and stop on their marks
        k = ss(cl((q - 12) / 20)); moving = k < .99
        bench_people(c, f, ai_x=lerp(-160, AI_X, k), eva_x=lerp(1240, EVA_X, k),
                     ai_walk=q * .5 if moving else None, eva_walk=q * .55 if moving else None, bounce=not moving)
    c.restore()

PLAN = [(s_ask, 36), (R.s5, 18), (s_rose, 27), (R.s7, 33), (R.s8, 24), (s_pump, 30), (R.s10, 52), (s_take, 30), (R.s12, 24),
        (R.s13, 30), (R.s14, 30), (s_plonk, 30), (R.s16, 27), (R.s17, 27), (R.s18, 24), (R.s19, 12), (s_land, 45)]
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
