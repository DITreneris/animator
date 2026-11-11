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
    'point':    dict(L=[(-120, -300), (-110, -205)], R=[(175, -520), (160, -650)], finger=True),
    'recoil':   dict(L=[(-120, -300), (-110, -205)], R=[(170, -380), (150, -480)], palm=True),
    'phone':    dict(L=[(-90, -250), (-15, -330)],   R=[(90, -250), (30, -328)], phone=True),
    'wave':     dict(L=None, R=[(120, -300), (110, -205)]),
}

def hoodyz(c, x, gy, s, era, expr='calm', pose='rest', f=0, lean=0, head_rot=0, op=0, legs_on=True, wave_k=0,
           strum=0, deflate=0, blink=None):
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
        limb(c, [shr, e, h], 44, NAVY); finger_hand(c, h[0], h[1], 1.0, -1.75)
    elif P.get('palm'):
        limb(c, [shr, e, h], 44, NAVY); palm(c, h[0], h[1], 1.0, -1.2, 0)
    else:
        arm(c, [shr, e, h], 1.0)
    if P.get('phone'):
        rr(c, -50, -400, 90, 150, 14); fs(c, INK, 0); rr(c, -42, -392, 74, 134, 10); c.set_source_rgb(*hx('6fd0ff')); c.fill()
    hoodyz_head(c, 0, HEAD_Y + dy * 1.3, 1.08, era, expr, f, head_rot, op=op, blink=blink)
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

_visor = kit.visor
def visor2(c, emote, eye, blink, f):
    if emote == 'loading':
        rr(c, -82, -54, 164, 92, 40); fs(c, hx('0b1020'), 6)
        rr(c, -60, -10, 120, 22, 11); c.set_source_rgb(*hx('1f3a4a')); c.fill()
        k = (f % 24) / 24; rr(c, -60, -10, 120 * (.2 + .8 * k), 22, 11); c.set_source_rgb(*BLUE); c.fill()
        return
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
def ai_art(c, x, y, w, h, t):
    """The AI's 'completely original' piece: confident, colourful, abstract; pulses with its notes."""
    c.set_source_rgb(*hx('101a2e')); c.rectangle(x, y, w, h); c.fill()
    cols = [hx('6fd0ff'), hx('ff7ac8'), hx('ffd84a'), hx('7af0b0')]
    for i in range(7):
        a = t * (0.8 + i * .17) + i
        cx = x + w * (.5 + .32 * math.cos(a)); cy = y + h * (.5 + .3 * math.sin(a * 1.3))
        r = min(w, h) * (.12 + .05 * math.sin(t * 6 + i))
        c.save(); c.translate(cx, cy); c.rotate(a)
        if i % 3 == 0: c.move_to(0, -r); c.line_to(r, r); c.line_to(-r, r); c.close_path()
        elif i % 3 == 1: rr(c, -r, -r, 2 * r, 2 * r, r * .3)
        else: ell(c, 0, 0, r, r)
        c.set_source_rgba(*cols[i % 4], .85); c.fill(); c.restore()

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

def monitor(c, x, y, w, h, content, t, f, glow=True):
    rr(c, x - 16, y - 16, w + 32, h + 32, 20); fs(c, hx('1b2030'))
    if content == 'ai': ai_art(c, x, y, w, h, t)
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
