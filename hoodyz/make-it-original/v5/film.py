"""Make It Original v5.1: the loop, plus the fixes from the v5 mute test: a 6-frame flash cut to the 1986 drummer's
wave-off inside his 2026 wave-off (he became her), MY AI's tune drawn as shapes nobody has seen, and years that jump
straight to their target instead of rolling through 2011.
v5: the loop. Everything up to 18.1 s is v4 (imported, not copied); the office tail is replaced by a
stadium bookend in frame 0's exact framing: the cat on HIS stage playing the riff with one lazy paw, old Hoody in the
front row playing air guitar, the cat yawning on the last note. The cut lands on frame 0, the year flips 2026 -> 1986,
and the riff carries straight through it. "NOW THAT'S ORIGINAL!" holds 1.2 s.
python3 film.py keys | t ... | seam | (no args: full render; needs fin.wav from mix5.py)"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
V4 = os.path.join(HERE, '..', 'v4'); sys.path.insert(0, V4)
_cwd = os.getcwd(); os.chdir(V4)
import film as F4                                  # v4's shots, timing and lip flap, unchanged
os.chdir(_cwd)
from film import A, G, D, R86, END, NF, FPS, W, H, SHOTS, KEY_T, NAMES, sub, guitar, lazy_cat, paw_motif, crowd, dream_edge
import cast
from cast import hoodyz, topbar_a, ell, YEL, INK, WHITE, cl, lerp, ss
from timeline import ONSETS
P2 = G['demo'] + 2.0                               # the cat's second pass: its last note ends exactly on the loop point

def paw_at(t, t0):
    paw, hit = 0.0, False
    for o in ONSETS:
        d = t - t0 - o
        if -.08 <= d < 0: paw = max(paw, 1 + d / .08)
        elif 0 <= d < .15: paw = max(paw, 1 - d / .15 * .7)
        if 0 <= d < .08: hit = True
    return paw, hit

def s19(c, t, f):  # (local time) frame 0's stadium, the same camera; the cat has his stage, he's in the crowd
    tg = t + D
    k = lerp(1.05, 1.0, cl((tg - G['back']) / .25)); A.cam(c, k, 540, 1060, 540, 1060)   # eases into frame 0's exact framing
    A.stadium(c, tg, wide=True, flash=A.note_hit(tg, P2))
    guitar(c, 400, 1420, 1.45, rot=0)
    paw, hit = paw_at(tg, P2)
    last = P2 + ONSETS[-1]
    yawn = math.sin(math.pi * cl((tg - last - .05) / .4)) if tg > last + .05 else 0
    tip = lazy_cat(c, 570, 1400, 1.5, paw, yawn, f)
    if hit: ell(c, tip[0], 1420, 60, 14); c.set_source_rgba(*YEL, .85); c.fill()
    paw_motif(c, tg, P2, 490, 830, 1.0, life=1.6)
    crowd(c, tg, 1600)
    bob = .07 * math.sin((tg - P2) / .25 * math.pi)                                    # old Hoody in the front row, air guitar, smug
    hoodyz(c, 880, 2190, .95, 2026, 'smuggrin', 'air', f, head_rot=-.06 + bob, lean=-.04)
    dream_edge(c)

F4.LATE[19] = s19

# ---- v5.1: the flash cut. Inside his 2026 wave-off, 6 frames of the drummer's 1986 wave at the same phase ----
FLASH = (G['wave26'] + .49, G['wave26'] + .49 + 6 / FPS)
_s15 = F4.LATE[15]
def s15(c, t, f):  # (local time)
    tg = t + D
    if FLASH[0] <= tg < FLASH[1]:
        F4.OLD[3](c, G['wave86'] + (tg - G['wave26']), f)                              # the matched framing, same arm path
        if tg < FLASH[0] + 1.5 / FPS: c.rectangle(0, 0, W, H); c.set_source_rgba(1, 1, 1, .45); c.fill()
    else: _s15(c, t, f)
F4.LATE[15] = s15

# ---- v5.1: the AI's tune looks like nothing anyone has seen: a strange glyph on every note ----
_ai_art = cast.ai_art
def glyph(c, kind, x, y, r):
    c.save(); c.translate(x, y); c.set_source_rgb(*INK); c.set_line_width(max(3, r * .22))
    if kind == 0:                                                                       # a spiral
        c.move_to(0, 0)
        for i in range(1, 40): a = i * .45; c.line_to(math.cos(a) * r * i / 40, math.sin(a) * r * i / 40)
        c.stroke()
    elif kind == 1:                                                                     # a seven-point star
        for i in range(15): a = i * math.pi / 7 - math.pi / 2; q = r if i % 2 == 0 else r * .45; (c.move_to if i == 0 else c.line_to)(math.cos(a) * q, math.sin(a) * q)
        c.close_path(); c.fill()
    elif kind == 2:                                                                     # an eye
        c.move_to(-r, 0); c.curve_to(-r * .4, -r * .8, r * .4, -r * .8, r, 0); c.curve_to(r * .4, r * .8, -r * .4, r * .8, -r, 0); c.stroke()
        c.arc(0, 0, r * .3, 0, 2 * math.pi); c.fill()
    else:                                                                               # a zigzag
        c.move_to(-r, r * .5)
        for i in range(1, 6): c.line_to(-r + i * r * .4, r * .5 if i % 2 == 0 else -r * .5)
        c.stroke()
    c.restore()
def ai_art(c, x, y, w, h, t, t0=None):
    _ai_art(c, x, y, w, h, t, t0)
    import timeline as TL
    rows, colsn = 8, 16; cw, ch = w / colsn, h / rows; pos = 0
    for i, (m, l) in enumerate(TL.AI_TUNE):
        r_ = rows - 1 - (m - 72) % rows
        glyph(c, i % 4, x + (pos + l / 2) * cw, y + (r_ + .5) * ch, min(ch, l * cw) * .5); pos += l
cast.ai_art = ai_art

def s14(c, t, f):  # (local) as v4, but the notes rising off the grid are strange glyphs on bright tiles, not blue diamonds
    E = A.E; A.office26(c, t)
    rec = ss((t - E['recoil']) / .18)
    nod = .05 * math.sin((t - E['ai']) * 4 * math.pi) * (1 - rec) if t < E['recoil'] else 0
    hoodyz(c, 540, 700 + 602 * 1.25, 1.25, 2026, 'polite' if rec < .5 else 'aghast', 'recoil' if rec > .3 else 'rest', f,
           lean=-.1 * rec, head_rot=nod - .16 * rec, legs_on=False, head_dx=-20 * rec)
    F4.monitor(c, 590, 1100, 440, 320, 'ai', t, f)
    cast.rr(c, 760, 1436, 100, 120, 10); cast.fs(c, cast.hx('1b2030'))
    from timeline import AI_TUNE, AI_ONSETS
    tiles = [cast.hx('6fd0ff'), cast.hx('ff7ac8'), cast.hx('ffd84a'), cast.hx('7af0b0')]
    for i, ((m, _), on) in enumerate(zip(AI_TUNE, AI_ONSETS)):
        dt = t - (E['ai'] + on)
        if 0 <= dt < 2.0 and E['ai'] + on < E['wave26']:
            a = cl(dt / .08) * cl((2.0 - dt) / .5); x = 690 + i * 62; y = 990 - (m - 72) * 18 - dt * 40
            c.save(); c.push_group(); cast.rr(c, x - 30, y - 30, 60, 60, 14); cast.fs(c, tiles[i % 4], 5); glyph(c, i % 4, x, y, 20)
            c.pop_group_to_source(); c.paint_with_alpha(a); c.restore()
F4.LATE[14] = s14
NAMES[19] = 'the stadium again: the cat on his stage, him in the crowd'
KEY_T[19] = 19.0

def subs(c, t, year):
    year = 1986 if t < G['ff1'] + .2 else 2016 if t < G['ff2'] + .2 else 2026                 # v5.1: jump, don't roll through 2011
    if FLASH[0] <= t < FLASH[1]: year = 1986
    topbar_a(c, year)
    sub(c, t, G['drum'], G['drum'] + 1.4, 'PLAY SOMETHING WE KNOW.')
    sub(c, t, G['ask'], G['ask'] + 1.7, 'MAKE SOMETHING|COMPLETELY ORIGINAL.')
    sub(c, t, G['know'], G['know'] + 1.12, 'PLAY SOMETHING WE KNOW.')
    sub(c, t, G['orig'], G['orig'] + 1.2, "NOW THAT'S ORIGINAL!")
F4.subs = subs

if __name__ == '__main__':
    a = sys.argv[1:]
    os.chdir(HERE)
    if a and a[0] == 'keys': F4.keys()
    elif a and a[0] == 'seam':                                   # the loop point: the last frame beside frame 0
        from PIL import Image
        im = Image.new('RGB', (1080, 960), 'white')
        for i, fr in enumerate((NF - 1, 0)): im.paste(F4.frame_img(fr).resize((540, 960)), (i * 540, 0))
        im.save('keys/seam.png'); Image.blend(F4.frame_img(NF - 1), F4.frame_img(0), .5).resize((540, 960)).save('keys/overlay_seam.png'); print('seam ok')
    elif a:
        for x in a: fr = int(round(float(x) * FPS)); F4.draw(fr).write_to_png(f'chk_{fr:03d}.png')
    else: F4.render('make_it_original_v5.mp4')
