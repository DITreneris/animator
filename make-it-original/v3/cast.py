"""v2 cast: full bodies, the pose library, new robot faces and the monitor content.
Builds on the episode kit (../kit.py). Body coordinates are local units: feet at y=0, head centre at y=-602."""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import kit
from kit import *

HEAD_Y, NECK_Y = -602, -442
JEANS = hx('3d5a8a'); SHOE = hx('f2f2f2'); SOLE = hx('c94a3a')

def finger_hand(c, x, y, s, ang):
    """Fist with the index finger raised along ang."""
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    rr(c, 0, -9, 52, 18, 9); fs(c, SKIN, 5)
    ell(c, 0, 0, 26, 24); fs(c, SKIN, 6); c.restore()

def legs(c, s=1.0, stance=46):
    for q in (-1, 1):
        limb(c, [(q * 38, -250), (q * stance, -130), (q * (stance + 6), -26)], 64, JEANS)
        rr(c, q * (stance + 6) - 44 + q * 14, -36, 88, 40, 18); fs(c, SHOE, 6)
        c.rectangle(q * (stance + 6) - 44 + q * 14, -6, 88, 6); c.set_source_rgb(*SOLE); c.fill()

# arm keypoints per pose (local units); 'L' is the viewer's left arm
POSES = {
    'rest':     dict(L=[(-120, -300), (-110, -205)], R=[(120, -300), (110, -205)]),
    'play':     dict(L=[(-150, -227), (-7, -200)],   R=[(187, -290), (187, -267)], guitar=((37, -190), -.45)),
    'proud':    dict(L=[(-215, -330), (-175, -480)], R=[(187, -290), (187, -267)], guitar=((37, -190), -.45)),
    'deflated': dict(L=[(-110, -250), (-40, -160)],  R=[(140, -250), (150, -170)], guitar=((40, -120), -.15)),
    'air':      dict(L=[(-215, -330), (-175, -480)], R=[(187, -290), (187, -267)]),
    'airstrum': dict(L=[(-150, -227), (-7, -200)],   R=[(187, -290), (187, -267)]),
    'point':    dict(L=[(-120, -300), (-110, -205)], R=[(230, -470), (300, -590)], finger=True),
    'recoil':   dict(L=[(-130, -300), (-60, -350)], R=[(130, -300), (60, -350)]),
    'phone':    dict(L=[(-90, -250), (-15, -330)],   R=[(90, -250), (30, -328)], phone=True),
    'wave':     dict(L=None, R=[(120, -300), (110, -205)]),
}

def hoodyz(c, x, gy, s, era, expr='calm', pose='rest', f=0, lean=0, head_rot=0, op=0, legs_on=True, wave_k=0,
           strum=0, deflate=0, blink=None, gaze=0, head_dx=0):
    """Full Hoodyz. lean rotates the body about the feet (+ toward the viewer's right).
    strum offsets the strumming hand; deflate 0..1 drops shoulders and head."""
    P = POSES[pose]
    c.save(); c.translate(x, gy); c.rotate(lean); c.scale(s, s)
    if legs_on: legs(c)
    dy = 26 * deflate
    shl, shr = hoodie(c, 0, NECK_Y + dy, 1.2)
    shl = (shl[0] + 8 * deflate, shl[1] + 10 * deflate); shr = (shr[0] - 8 * deflate, shr[1] + 10 * deflate)
    if 'guitar' in P:
        (gx, gyy), gr = P['guitar']; guitar(c, gx, gyy + dy, .69, rot=gr)
    if P['L'] is None:
        arm(c, waveoff(shl, 1.2, wave_k, -1), 1.0, flick=1.0 if .38 < wave_k < .8 else 0)
    else:
        e, h = P['L']; h = (h[0], h[1] + strum)
        arm(c, [shl, e, h], 1.0)
    e, h = P['R']
    if P.get('finger'):
        limb(c, [shr, e, h], 44, NAVY); finger_hand(c, h[0], h[1], 1.0, -1.1)
    elif P.get('palm'):
        limb(c, [shr, e, h], 44, NAVY); palm(c, h[0], h[1], 1.0, -1.2, 0)
    else:
        arm(c, [shr, e, h], 1.0)
    if P.get('phone'):
        rr(c, -50, -400, 90, 150, 14); fs(c, INK, 0); rr(c, -42, -392, 74, 134, 10); c.set_source_rgb(*hx('6fd0ff')); c.fill()
    hoodyz_head(c, head_dx, HEAD_Y + dy * 1.3, 1.08, era, expr, f, head_rot, op=op, blink=blink, gaze=gaze)
    c.restore()

def drummer_body(c, x, y_head, s, expr='deadpan', f=0, head_rot=0, op=0, wave_k=None, sticks=True):
    """The drummer from the waist up (he sits behind the kit). y_head = head centre."""
    c.save(); c.translate(x, y_head); c.scale(s, s)
    shl, shr = vest(c, 0, 160, 1.2)
    if wave_k is not None:
        arm(c, waveoff(shl, 1.2, wave_k, -1), 1.0, SKIN, flick=1.0 if .38 < wave_k < .8 else 0)
    else:
        arm(c, [shl, (-90, 330), (-120, 380)], 1.0, SKIN)
        if sticks: stick(c, -120, 380, -2.6, 1.0)
    arm(c, [shr, (90, 330), (120, 380)], 1.0, SKIN)
    if sticks: stick(c, 120, 380, -.5, 1.0)
    drummer_head(c, 0, 0, 1.08, expr, f, head_rot, op=op)
    c.restore()

# ---------- extra faces ----------
kit.FACES['rocking'] = ('happy', ('raised', 'raised'), 'grin')       # eyes shut, grinning: lost in the riff
kit.FACES['yuck'] = ('narrow', ('angry', 'angry'), 'wobble')          # the recoil
kit.FACES['eager'] = ('open', ('up', 'up'), 'grin')                   # the lean-in
kit.FACES['aghast'] = ('big', ('worried', 'worried'), 'wobble')       # the recoil: wide eyes, wobbling mouth

_visor = kit.visor
def visor2(c, emote, eye, blink, f):
    if emote == 'loading':
        rr(c, -82, -54, 164, 92, 40); fs(c, hx('0b1020'), 6)
        rr(c, -60, -10, 120, 22, 11); c.set_source_rgb(*hx('1f3a4a')); c.fill()
        k = (f % 24) / 24; rr(c, -60, -10, 120 * (.2 + .8 * k), 22, 11); c.set_source_rgb(*BLUE); c.fill()
        return
    if emote == 'ready':
        rr(c, -82, -54, 164, 92, 40); fs(c, hx('0b1020'), 6)
        c.move_to(-34, 0); c.line_to(-8, 24); c.line_to(40, -26); c.set_source_rgb(*GREEN); c.set_line_width(14); c.stroke(); return
    if emote == 'side':        # eyes slid hard to the viewer's right (toward the old cat), half-lidded
        rr(c, -82, -54, 164, 92, 40); fs(c, hx('0b1020'), 6); c.set_source_rgb(*BLUE)
        for q in (-1, 1):
            ell(c, q * 30 + 30, 0, 16, 18); c.fill()
            c.move_to(q * 30 + 10, -16); c.line_to(q * 30 + 50, -16); c.set_line_width(8); c.stroke()
        return
    return _visor(c, emote, eye, blink, f)
kit.visor = visor2

def robot_body(c, x, y, s, emote=None, eye=(0, 0), f=0, roll=0, present=0):
    """Robot sitting on the desk. roll 0..1: shoulder roll (arms lift and drop); present 0..1: arm toward the monitor."""
    arms = []
    lsx, lsy = x - 70 * s, y + 110 * s; rsx, rsy = x + 70 * s, y + 110 * s
    lift = math.sin(math.pi * roll) * 50 * s
    arms.append([(lsx, lsy), (lsx - 50 * s, lsy + 60 * s - lift), (lsx - 30 * s, lsy + 120 * s - lift)])
    if present:
        arms.append([(rsx, rsy), (rsx + lerp(50, 90, present) * s, rsy + lerp(60, -10, present) * s),
                     (rsx + lerp(30, 190, present) * s, rsy + lerp(120, -70, present) * s)])
    else:
        arms.append([(rsx, rsy), (rsx + 50 * s, rsy + 60 * s - lift), (rsx + 30 * s, rsy + 120 * s - lift)])
    return robot(c, x, y, s, emote, eye, f, seed=2, arms=arms)

# ---------- monitor content ----------
def ai_art(c, x, y, w, h, t, t0=None):
    """The AI's 'completely original' tune as a glowing music sequencer: a note grid, a playhead, notes lighting as they play."""
    c.set_source_rgb(*hx('101a2e')); c.rectangle(x, y, w, h); c.fill()
    rows, colsn = 8, 16; cw, ch = w / colsn, h / rows
    for r_ in range(rows + 1): c.move_to(x, y + r_ * ch); c.line_to(x + w, y + r_ * ch)
    for k in range(colsn + 1): c.move_to(x + k * cw, y); c.line_to(x + k * cw, y + h)
    c.set_source_rgba(.4, .6, .9, .25); c.set_line_width(2); c.stroke()
    import timeline as TL
    play = (t - (t0 if t0 is not None else t)) / TL.S16
    cols = [hx('6fd0ff'), hx('ff7ac8'), hx('ffd84a'), hx('7af0b0')]
    pos = 0
    for i, (m, l) in enumerate(TL.AI_TUNE):
        r_ = rows - 1 - (m - 72) % rows
        lit = pos <= play < pos + l
        rr(c, x + pos * cw + 2, y + r_ * ch + 3, l * cw - 4, ch - 6, 6)
        c.set_source_rgba(*cols[i % 4], 1 if lit else .55); c.fill()
        if lit: rr(c, x + pos * cw - 4, y + r_ * ch - 3, l * cw + 8, ch + 6, 9); c.set_source_rgba(*cols[i % 4], .35); c.fill()
        pos += l
    px = x + min(play, colsn) * cw
    c.move_to(px, y); c.line_to(px, y + h); c.set_source_rgb(1, 1, 1); c.set_line_width(4); c.stroke()

def cat_clip(c, x, y, w, h, t, f, playing=True):
    """The 2016 cat video on a screen: couch, guitar, the cat; 10M and a play bar."""
    c.save(); c.rectangle(x, y, w, h); c.clip()
    c.set_source_rgb(*hx('e8dcc6')); c.paint()
    k = w / 600
    rr(c, x + 20 * k, y + h - 190 * k, 560 * k, 150 * k, 30 * k); fs(c, hx('4f8f7c'), 0)
    guitar(c, x + 170 * k, y + h - 150 * k, .5 * k)
    px = x + (420 - 60 * ((t * 1.5) % 2)) * k
    cat(c, px, y + h - 160 * k, .5 * k, 'walk', phase=t * 3, f=f)
    rr(c, x + 14 * k, y + 14 * k, 210 * k, 70 * k, 20 * k); fs(c, hx('0b0d12'), 0)
    txt(c, '10M', x + 119 * k, y + 49 * k, 54 * k, fill=YEL, lw=0)
    c.rectangle(x, y + h - 14 * k, w, 14 * k); c.set_source_rgb(*hx('333333')); c.fill()
    c.rectangle(x, y + h - 14 * k, w * ((t * .4) % 1), 14 * k); c.set_source_rgb(*RED); c.fill()
    c.restore()

AI_T0 = 11.55
def monitor(c, x, y, w, h, content, t, f, glow=True):
    rr(c, x - 16, y - 16, w + 32, h + 32, 20); fs(c, hx('1b2030'))
    if content == 'ai': ai_art(c, x, y, w, h, t, AI_T0)
    elif content == 'cat': cat_clip(c, x, y, w, h, t, f)
    else: c.rectangle(x, y, w, h); c.set_source_rgb(*hx('20262f')); c.fill()

def views_badge(c, x, y, text, k=1, col=WHITE, size=72):
    """A pop-up view count: scales in with an overshoot."""
    sc = max(.02, back(k)) if k < 1 else 1
    c.save(); c.translate(x, y); c.scale(sc, sc)
    c.select_font_face('Lilita One'); c.set_font_size(size); w = c.text_extents(text).width
    rr(c, -w / 2 - 34, -size * .75, w + 68, size * 1.5, size * .75); fs(c, hx('0b0d12'), 8, WHITE)
    txt(c, text, 0, 0, size, fill=col, lw=0); c.restore()

def back(t):
    t = cl(t); k = 2.2; return 1 + (k + 1) * (t - 1) ** 3 + k * (t - 1) ** 2

# ---------- the fantasy stadium (shots 1, 2 and 16) ----------
def stadium(c, t, wide=True, k=1.0):
    """Generic stadium rock fantasy: beams, haze, a crowd of phone lights, a dreamy vignette.
    No real band's look or logo. k fades the whole layer in (shot 16 blooms into it)."""
    c.push_group()
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, *hx('120a2e')); g.add_color_stop_rgb(.6, *hx('2a0f4a')); g.add_color_stop_rgb(1, *hx('0b0820'))
    c.set_source(g); c.paint()
    glow = cairo.RadialGradient(540, 900, 40, 540, 900, 760); glow.add_color_stop_rgba(0, 1, .55, .9, .55); glow.add_color_stop_rgba(1, 1, .55, .9, 0)
    c.set_source(glow); c.paint()
    cols = [(1, .3, .6), (.3, .7, 1), (1, .85, .3), (.6, .4, 1), (.3, 1, .8)]
    ty = 400
    for i in range(7):   # beams sweeping from the truss
        x = 120 + i * 140; a = math.sin(t * 1.6 + i * 1.3) * .35 + (i - 3) * .06
        c.save(); c.translate(x, ty); c.rotate(a)
        c.move_to(-14, 0); c.line_to(14, 0); c.line_to(240, 1700); c.line_to(-240, 1700); c.close_path()
        bg = cairo.LinearGradient(0, 0, 0, 1700); r, g_, b = cols[i % 5]
        bg.add_color_stop_rgba(0, r, g_, b, .45); bg.add_color_stop_rgba(1, r, g_, b, 0); c.set_source(bg); c.fill(); c.restore()
    c.rectangle(-20, ty - 26, W + 40, 34); c.set_source_rgb(*hx('3a3a4a')); c.fill()          # truss
    for i in range(7): ell(c, 120 + i * 140, ty + 6, 20, 16); c.set_source_rgb(1, .95, .8); c.fill()
    if wide:
        c.rectangle(0, 1450, W, 110); c.set_source_rgb(*hx('1a1426')); c.fill()                # stage
        c.rectangle(0, 1450, W, 8); c.set_source_rgb(1, .6, .9); c.fill()
    for i in range(5):   # haze
        hz = cairo.RadialGradient(200 + i * 200, 1500, 20, 200 + i * 200, 1500, 320)
        hz.add_color_stop_rgba(0, 1, 1, 1, .12); hz.add_color_stop_rgba(1, 1, 1, 1, 0); c.set_source(hz); c.paint()
    c.pop_group_to_source(); c.paint_with_alpha(k)

def crowd(c, t, y0=1600, k=1.0, rows=2):
    """Foreground crowd: head and raised-arm silhouettes with twinkling phone lights."""
    c.push_group()
    for r_ in range(rows):
        yy = y0 + r_ * 120
        for i in range(12):
            x = (i * 97 + r_ * 48) % (W + 60) - 30; bob = math.sin(t * 8 + i * 1.7) * 10
            ell(c, x, yy + bob, 46, 52); c.set_source_rgb(*hx('07050f')); c.fill()
            c.rectangle(x - 46, yy + 40 + bob, 92, 400); c.fill()
            if (i + r_) % 3 == 0:
                c.move_to(x + 30, yy + 20 + bob); c.line_to(x + 50, yy - 110 + bob); c.set_line_width(24); c.stroke()
                tw = .6 + .4 * math.sin(t * 6 + i * 2)
                rr(c, x + 38, yy - 150 + bob, 26, 40, 5); c.set_source_rgba(1, 1, .85, tw); c.fill(); c.set_source_rgb(*hx('07050f'))
    c.pop_group_to_source(); c.paint_with_alpha(k)

def dream_edge(c, k=1.0):
    v = cairo.RadialGradient(540, 960, 420, 540, 960, 1150)
    v.add_color_stop_rgba(0, 0, 0, 0, 0); v.add_color_stop_rgba(1, .9, .7, 1, .35 * k); c.set_source(v); c.paint()

# ---------- the lazy cat (shot 7) ----------
def lazy_cat(c, x, gy, s, paw=0.0, yawn=0.0, f=0, look=-1):
    """Lying on the couch, chin up, one front paw dropping onto the strings. paw: 1 = pressed down.
    yawn 0..1 opens a big yawn with closed eyes. Returns the paw tip (canvas coords)."""
    c.save(); c.translate(x, gy); c.scale(s * look, s)
    c.move_to(-110, -40); c.curve_to(-180, -20, -190, 40, -120, 30)                            # tail curled behind
    c.set_source_rgb(*INK); c.set_line_width(28); c.stroke_preserve(); c.set_source_rgb(*TABBY); c.set_line_width(16); c.stroke()
    ell(c, 0, -46, 125, 52); fs(c, TABBY)
    for i in range(4): c.arc(-70 + i * 38, -70, 24, math.pi * 1.2, math.pi * 1.8); c.set_source_rgb(*TABBY_D); c.set_line_width(8); c.stroke()
    ell(c, 70, -8, 30, 12); fs(c, TABBY, 5)                                                     # tucked paw
    tip = (175, lerp(-60, 18, paw))                                                             # the lazy paw: presses into the strings
    limb(c, [(80, -40), (130, -50 + 10 * paw), tip], 22, TABBY); ell(c, tip[0], tip[1], 17, 11); fs(c, TABBY, 5)
    kit._cat_head(c, 112, -96, 1.0, False, 'sleep' if yawn > .25 else 'open', f)
    if yawn > 0:
        ell(c, 126, -72, 15 * yawn + 2, 22 * yawn + 2); fs(c, hx('7a2230'), 5)
        ell(c, 126, -66, 8 * yawn, 8 * yawn); c.set_source_rgb(*hx('ff8fa6')); c.fill()
    c.restore()
    return (x + look * tip[0] * s, gy + tip[1] * s)

# ================= version A additions =================
def demo_screen(c, x, y, w, h, t, t0):
    """The monitor playing his 1986 garage demo: the cassette label, a waveform, a play bar."""
    c.save(); c.rectangle(x, y, w, h); c.clip()
    c.set_source_rgb(*hx('14161c')); c.paint()
    k = w / 600
    cassette(c, x + w / 2, y + h * .38, 1.15 * k)
    for i in range(48):                                            # waveform of the riff, playing
        xx = x + 30 * k + i * (w - 60 * k) / 48
        a = abs(math.sin(i * .9) * math.sin(i * .37 + 1)) * 40 * k + 6 * k
        played = (i / 48) < ((t - t0) / 4.0) % 1
        c.rectangle(xx, y + h * .78 - a, 6 * k, 2 * a); c.set_source_rgb(*(YEL if played else hx('4a4f5c'))); c.fill()
    c.restore()

_monitor = monitor
def monitor(c, x, y, w, h, content, t, f, glow=True):
    if content == 'demo':
        rr(c, x - 16, y - 16, w + 32, h + 32, 20); fs(c, hx('1b2030')); demo_screen(c, x, y, w, h, t, DEMO_T0); return
    return _monitor(c, x, y, w, h, content, t, f, glow)
DEMO_T0 = 10.2

def drums_foreground(c, y):
    """Shot 3's foreground: a snare and a floor tom with a cymbal edge (replaces the red block)."""
    rr(c, 140, y + 60, 360, 300, 30); fs(c, hx('d23a4a')); ell(c, 320, y + 60, 180, 46); fs(c, hx('f5efe2'), 7)
    for i in range(6): c.move_to(160 + i * 64, y + 90); c.line_to(160 + i * 64, y + 350); c.set_source_rgba(1, 1, 1, .25); c.set_line_width(6); c.stroke()
    rr(c, 560, y + 120, 300, 260, 26); fs(c, hx('d23a4a')); ell(c, 710, y + 120, 150, 38); fs(c, hx('f5efe2'), 7)
    c.move_to(960, y - 60); c.line_to(960, y + 500); c.set_source_rgb(*GREY); c.set_line_width(10); c.stroke()
    ell(c, 900, y - 60, 170, 22); fs(c, YEL, 6)

# legs with a toe tap (shots 2 and 16)
_legs = legs
def legs(c, s=1.0, stance=46, tap=0.0):
    for q in (-1, 1):
        limb(c, [(q * 38, -250), (q * stance, -130), (q * (stance + 6), -26)], 64, JEANS)
        c.save(); c.translate(q * (stance + 6) + q * 14 + q * 40, -16)
        if q == 1 and tap: c.rotate(-.35 * tap)
        c.translate(-(q * 40), 0); rr(c, -44, -20, 88, 40, 18); fs(c, SHOE, 6); c.rectangle(-44, 10, 88, 6); c.set_source_rgb(*SOLE); c.fill()
        c.restore()
TAP = 0.0
import types
_hoodyz = hoodyz
def hoodyz(c, x, gy, s, era, expr='calm', pose='rest', f=0, tap=0.0, **k):
    global legs
    if tap:
        old = globals()['legs']; globals()['legs'] = lambda c, s=1.0: old(c, s, tap=tap)
        try: return _hoodyz(c, x, gy, s, era, expr, pose, f, **k)
        finally: globals()['legs'] = old
    return _hoodyz(c, x, gy, s, era, expr, pose, f, **k)

def robot_turn(c, x, y, s, turn, emote, eye, f):
    """Robot with its whole head turning toward camera (turn 0..1): the body leans, the visor shifts and squashes."""
    c.save(); c.translate(x, y + 200 * s); c.rotate(-.12 * turn); c.translate(-x, -(y + 200 * s))
    robot_body(c, x, y, s, emote, eye, f)
    c.restore()

def topbar_a(c, year):
    """ME + MY AI series bar: the Hoodyz badge (hoodie icon + HOODYZ), the title, and a pill with the story state.
    Drawn in screen space. The title shrinks only if a long pill would crowd it."""
    c.save(); c.identity_matrix()
    rr(c, 40, BAR_Y, 1000, 138, 40); fs(c, WHITE, 8)
    iy = BAR_Y + 69
    rr(c, 58, iy - 38, 196, 76, 38); c.set_source_rgb(*NAVY); c.fill()                    # Hoodyz badge
    c.save(); c.translate(96, iy + 2); c.scale(.62, .62)
    c.move_to(-34, 34); c.line_to(-34, -4); c.curve_to(-34, -46, 34, -46, 34, -4); c.line_to(34, 34); c.close_path()
    c.set_source_rgb(*WHITE); c.fill(); ell(c, 0, -2, 20, 18); c.set_source_rgb(*SKIN); c.fill(); c.restore()
    txt(c, 'HOODYZ', 124, iy, 31, WHITE, lw=0, align='l')
    c.select_font_face('Lilita One'); c.set_font_size(58); w = max(200, c.text_extents(str(year)).width + 96)
    px = 1020 - w / 2
    size = 68; c.set_font_size(size); tw = c.text_extents('ME + MY AI').width; room = (px - w / 2 - 22) - 274
    if tw > room: size *= room / tw
    txt(c, 'ME + MY AI', 274, iy, size, NAVY, lw=0, align='l')
    rr(c, px - w / 2, iy - 44, w, 88, 44); fs(c, YEL, 7); txt(c, str(year), px, iy, 58, INK, lw=0)
    c.restore()

_stadium = stadium
def stadium(c, t, wide=True, k=1.0, flash=0.0):
    _stadium(c, t, wide, k)
    if flash > 0:   # a light flash on each riff note
        c.rectangle(0, 0, W, H); c.set_source_rgba(1, .85, 1, .22 * flash * k); c.fill()
