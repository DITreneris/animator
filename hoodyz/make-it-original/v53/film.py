"""Make It Original v5.3: v5.2 (imported, unchanged) plus the punchline made visible.
- His finger taps play on the cat clip: he picks the familiar thing himself.
- Right after "Now THAT'S original!", MY AI's deadpan fact-check stamps over the cat on his stage:
  SOURCE: GARAGE DEMO '86 (the cassette from 1986). It is gone before the loop point, so the seam stays clean.
- The AI's tune reads on a phone: a bigger screen and bigger rising glyph tiles.
- Old Hoody is bigger and higher in the front row of the last shot.
python3 film.py keys | t ... | seam | (no args: full render; needs fin.wav from mix53.py)"""
import sys, os, math, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location('film52', os.path.join(HERE, '..', 'v52', 'film.py'))
F52 = importlib.util.module_from_spec(_spec); _cwd = os.getcwd(); _spec.loader.exec_module(F52); os.chdir(_cwd)
F5, F4, A, G, D, FPS, W, H, NF = F52.F5, F52.F4, F52.A, F52.G, F52.D, F52.FPS, F52.W, F52.H, F52.NF
import cast
from cast import rr, fs, ell, limb, hx, cl, lerp, ss, txt, INK, SKIN, NAVY, WHITE, YEL, hoodyz
from timeline import ONSETS
TAP = G['demo'] + .15                    # his finger lands on play just after the clip appears
STAMP = (G['orig'] + 1.4, G['orig'] + 2.68)   # held 1.3 s (0.85 s was too fast for both viewers); gone before the seam

# ---- 2026: the AI's tune, big enough for a phone ----
def s14(c, t, f):
    E = A.E; A.office26(c, t)
    rec = ss((t - E['recoil']) / .18)
    nod = .05 * math.sin((t - E['ai']) * 4 * math.pi) * (1 - rec) if t < E['recoil'] else 0
    hoodyz(c, 470, 700 + 602 * 1.25, 1.25, 2026, 'polite' if rec < .5 else 'aghast', 'recoil' if rec > .3 else 'rest', f,
           lean=-.1 * rec, head_rot=nod - .16 * rec, legs_on=False, head_dx=-20 * rec)
    F4.monitor(c, 560, 1060, 480, 360, 'ai', t, f)
    rr(c, 770, 1436, 100, 120, 10); fs(c, hx('1b2030'))
    from timeline import AI_TUNE, AI_ONSETS
    tiles = [hx('6fd0ff'), hx('ff7ac8'), hx('ffd84a'), hx('7af0b0')]
    for i, ((m, _), on) in enumerate(zip(AI_TUNE, AI_ONSETS)):
        dt = t - (E['ai'] + on)
        if 0 <= dt < 2.0 and E['ai'] + on < E['wave26']:
            a = cl(dt / .08) * cl((2.0 - dt) / .5); x = 640 + i * 78; y = 960 - (m - 72) * 20 - dt * 46
            c.save(); c.push_group(); rr(c, x - 44, y - 44, 88, 88, 20); fs(c, tiles[i % 4], 6); F5.glyph(c, i % 4, x, y, 30)
            c.pop_group_to_source(); c.paint_with_alpha(a); c.restore()
F4.LATE[14] = s14

# ---- the choice is his: his finger taps play on the cat clip ----
_s17 = F4.LATE[17]
def s17(c, t, f):
    _s17(c, t, f)
    tg = t + D
    if tg < TAP + .35:
        k = ss((tg - (TAP - .15)) / .15); px, py = 250, 1200
        if tg < TAP:                                                         # the play button, until he presses it
            c.save(); c.translate(px, py); c.move_to(-50, -64); c.line_to(70, 0); c.line_to(-50, 64); c.close_path()
            c.set_source_rgba(1, 1, 1, .9); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(8); c.stroke(); c.restore()
        else:
            u = cl((tg - TAP) / .2); c.arc(px, py, 60 + 120 * u, 0, 2 * math.pi); c.set_source_rgba(1, 1, 1, .6 * (1 - u)); c.set_line_width(10); c.stroke()
        fy = lerp(2100, py + 40, k) if tg < TAP + .1 else lerp(py + 40, 2100, ss((tg - TAP - .1) / .25))
        limb(c, [(420, 2300), (330, fy + 300), (px + 20, fy + 30)], 90, NAVY)            # his sleeve and finger, from below
        ell(c, px + 20, fy + 30, 46, 42); fs(c, SKIN, 7); rr(c, px + 4, fy - 40, 30, 74, 15); fs(c, SKIN, 6)
F4.LATE[17] = s17

# ---- the last shot: v5's bookend, him bigger in the front row, then MY AI's fact-check stamp ----
def s19(c, t, f):
    tg = t + D
    k = lerp(1.05, 1.0, cl((tg - G['back']) / .25)); A.cam(c, k, 540, 1060, 540, 1060)
    A.stadium(c, tg, wide=True, flash=A.note_hit(tg, F5.P2))
    F5.guitar(c, 400, 1420, 1.45, rot=0)
    paw, hit = F5.paw_at(tg, F5.P2)
    last = F5.P2 + ONSETS[-1]
    yawn = math.sin(math.pi * cl((tg - last - .05) / .4)) if tg > last + .05 else 0
    tip = F5.lazy_cat(c, 570, 1400, 1.5, paw, yawn, f)
    if hit: ell(c, tip[0], 1420, 60, 14); c.set_source_rgba(*YEL, .85); c.fill()
    F5.paw_motif(c, tg, F5.P2, 490, 830, 1.0, life=1.6)
    F5.crowd(c, tg, 1600)
    bob = .07 * math.sin((tg - F5.P2) / .25 * math.pi)
    hoodyz(c, 900, 2050, 1.15, 2026, 'smuggrin', 'air', f, head_rot=-.06 + bob, lean=-.04)
    F5.dream_edge(c)
    if STAMP[0] <= tg < STAMP[1]:                                             # MY AI's deadpan fact-check
        u = tg - STAMP[0]; z = lerp(1.5, 1, ss(u / .12))                       # it slams down onto the frame
        fade = cl((STAMP[1] - tg) / .15)
        c.push_group(); c.save(); c.translate(540, 1010); c.rotate(-.07); c.scale(z, z)
        rr(c, -400, -120, 800, 240, 30); fs(c, hx('1b2030'), 10, WHITE)
        rr(c, -370, -90, 110, 76, 30); fs(c, WHITE, 5); ell(c, -340, -52, 12, 14); c.set_source_rgb(*hx('3fb6ff')); c.fill(); ell(c, -290, -52, 12, 14); c.fill()   # its visor
        txt(c, 'SOURCE:', -40, -52, 64, fill=WHITE, lw=0)
        txt(c, "GARAGE DEMO '86", 0, 52, 92, fill=YEL, lw=0)
        c.restore(); c.pop_group_to_source(); c.paint_with_alpha(fade)
        if u < .05: c.rectangle(0, 0, W, H); c.set_source_rgba(1, 1, 1, .25); c.fill()
F4.LATE[19] = s19

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
    else: F4.render('make_it_original_v53.mp4')
