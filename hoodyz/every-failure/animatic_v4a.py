"""Every Failure - rough animatic (process step 7, rough): the whole 18 s in motion, drawn per frame from the locked key poses.
Placeholder voices in vo/ (Kokoro). No video is encoded here: `python3 animatic.py sheet` writes 4 fps contact sheets
(with and without bubbles) for the cold mute test; `python3 animatic.py frames N...` writes stills.
The loop: frames 0-35 and 525-539 are frame 0's composition (F.draw at f=0 pose), so the last frame is frame 0 exactly."""
import os, sys, math, random, cairo
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import frame0 as F
import keyposes as KP
from keyposes import (R, K, E, A, GL, CX0, CX1, W, H, YEL, TEAL, HS, HX, AX, AS, HY, DECK, BRIDGE, rock, slab, shadow,
                      success_sign, braced_hoody, sweat, backdrop, chasm, step_hoody, visor_glow, capsule_pop, ear, TL)
from kit import INK, WHITE, NAVY, rr, fs, ell, hx, txt, limb

NF = 540
cl = lambda v: max(0.0, min(1.0, v))
lerp = lambda a, b, t: a + (b - a) * t
ss = lambda t: t * t * (3 - 2 * t)
def seg(f, a, b): return cl((f - a) / (b - a))

# ---- the stones: when each lands, when each dissolves (frames)
THROWS = {'FAIL': (36, 48), 'REJECTED': (66, 76), 'BUG': (84, 94), '404': (100, 110)}   # flight start, landing
LIFTS = {'REJECTED': (52, 58), 'BUG': (78, 84), '404': (95, 100)}                     # rises from the pile into his hands
GONE = {'404': (312, 330), 'REJECTED': (330, 350), 'FAIL': (340, 360), 'BUG': (372, 379)} # dissolve windows
RC = (HX + 10, GL - 300 * HS - 326 * HS - 200 * HS); RS = 1.25 * HS                   # the stone over his head (frame 0)
PILE = (165, GL - 40)                                                                  # the new stones' pile: words inside x 60

def antenna(x, gy, s): return (x, gy - 430 * s)

def ai_state(f):
    """MY AI: (x, gy, s, kw) per frame - behind him, hop off his back onto the deck, walk over, bow, walk back eating the deck, hop home."""
    s = AS
    if f < 135 or f >= 495: return AX, GL, s, dict(eye='open', look=(14, -12), talk=.7 if any(0 <= f - b < 4 for _, b in THROWS.values()) else 0)
    if f < 139:                                                                           # anticipation: it crouches
        return AX, GL, s, dict(eye='happy', squash=ss(seg(f, 135, 139)))
    if f < 147:                                                                           # up onto his shoulder (behind him)
        t = seg(f, 139, 147); x = lerp(AX, HX + 20, t); y = lerp(GL, GL - 470, t) - 140 * math.sin(math.pi * t)
        return x, y, s, dict(eye='happy', arms=('up', 'up'), rot=.15)
    if f < 149: return HX + 20, GL - 470, s, dict(eye='happy', squash=.6, rot=.1)         # kicks off him
    if f < 159:                                                                           # a parabola onto the deck, under the title bar
        t = seg(f, 149, 159); x = lerp(HX + 20, 478, t); y = lerp(GL - 470, DECK, t * t) - 70 * math.sin(math.pi * t)
        return x, y, s, dict(eye='happy', arms=('up', 'down'), rot=.2)
    if f < 162: return 478, DECK, s, dict(eye='happy', squash=1 - seg(f, 159, 162))       # lands: absorbs it
    if f < 182:                                                                           # strides over BUG and 404 to the far bank
        t = seg(f, 162, 182); x = lerp(478, 780, t); y = DECK if x < CX1 else GL
        return x, y, s, dict(eye='happy', walk=(x - 478) / 34)                         # legs locked to the ground it covers
    if f < 300:                                                                           # the bow, held
        b = ss(seg(f, 190, 204)) * (1 - ss(seg(f, 226, 238)))
        return 780, GL, s, dict(eye='happy', rot=-.3 * b, talk=0)                    # bows towards Hoody: the performer's bow
    if f < 330:                                                                           # walks back over the deck, towards Hoody
        t = seg(f, 300, 330); x = lerp(780, 478, t); y = DECK if x < CX1 else GL
        return x, y, s, dict(eye='happy', walk=(780 - x) / 34, turn=-.5, talk=.8 if 285 <= f < 320 else 0)
    if f < 345: return 478, DECK, s, dict(eye='happy', turn=-.5)
    if f < 360:                                                                           # hops over his head, home
        t = seg(f, 345, 360); x = lerp(478, AX, t); y = lerp(DECK, GL, t) - 430 * math.sin(math.pi * t)   # head stays under the title bar
        return x, y, s, dict(eye='happy', arms=('up', 'up'))
    if f < 420: return AX, GL, s, dict(eye='happy')
    if f < 434: b = ss(seg(f, 420, 426)) * (1 - ss(seg(f, 428, 434))); return AX, GL, s, dict(eye='happy', rot=-.35 * b)   # bends to the pile
    return AX, GL, s, dict(eye='happy', arms=('up', 'up') if f >= 470 else ('down', 'down'), talk=.6 if 440 <= f < 454 else 0)   # "More?"

def stone_at(name, f):
    """Where a thrown stone is: None (not yet), ('flight', x, y, k) or ('set', alpha)."""
    a, b = THROWS[name]; gx = [e for e in BRIDGE if e[0] == name][0]
    if f < a: return None
    if f < b:
        u = seg(f, a, b); tx = 1 - (1 - u) ** 2; ty = u * u                              # forward off his hands at once, then falls
        return ('flight', lerp(RC[0], gx[1], tx), lerp(RC[1] - 60, gx[2], ty) - 90 * math.sin(math.pi * min(1, u * 1.4)), u)
    if name in GONE:
        g0, g1 = GONE[name]
        if f >= g1: return ('gone',)
        return ('set', 1 - seg(f, g0, g1))
    return ('set', 1.0)

def robot(c, x, y, s, kw):
    kw = dict(kw); q = kw.pop('squash', 0)
    if q:                                                                                  # squash about its feet: crouch / landing
        c.save(); c.translate(x, y); c.scale(1 + .12 * q, 1 - .2 * q); c.translate(-x, -y); A.myai(c, x, y, s, **kw); c.restore()
    else: A.myai(c, x, y, s, **kw)

def particles(c, src, dst, k, n=26, col=TEAL, seed=1):
    """Blocks streaming from src to dst; k = progress 0..1 of the stream (each block leaves a little later)."""
    rnd = random.Random(seed)
    for i in range(n):
        t = cl(k * 1.6 - i / n * .6)
        if t <= 0 or t >= 1: continue
        x = lerp(src[0], dst[0], t) + rnd.uniform(-18, 18) * (1 - t); y = lerp(src[1], dst[1], t * t * (3 - 2 * t))
        z = 36 - 18 * t; c.rectangle(x - z / 2, y - z / 2, z, z); c.set_source_rgba(*col, .95); c.fill_preserve(); c.set_source_rgba(*INK, .5); c.set_line_width(2); c.stroke()

def bridge(c, f, ant):
    rubble = False
    for name, x, y, sx, sy, r in BRIDGE:
        st = stone_at(name, f)
        if not st or st[0] in ('flight', 'gone'): continue
        if name == 'REJECTED' and st[1] > .5: rubble = True
        c.push_group(); slab(c, x, y, sx, sy, name, r); c.pop_group_to_source(); c.paint_with_alpha(st[1])
        if name in GONE and st[1] < 1: particles(c, (x, y), ant, 1 - st[1], seed=hash(name) % 97)
        a, b = THROWS[name]
        if 0 <= f - b < 8:                                                                # landing dust
            for kk in range(6): ell(c, x - 110 + kk * 44, y - 30 - (kk % 2) * 14, 28 * (1 + (f - b) * .08), 16); c.set_source_rgba(*hx('e9c98f'), .8 * (1 - (f - b) / 8)); c.fill()
    if f >= 110:                                                                          # the montage's small failures, wedged under the deck
        a_ = 1 - seg(f, 330, 350)
        if a_ > 0:
            for w_, x_, y_, s_ in SMALL:
                c.push_group(); rock(c, x_, y_, s_, w_, rot=(x_ % 7 - 3) * .06, ty=0); c.pop_group_to_source(); c.paint_with_alpha(a_)
            if a_ < 1: particles(c, (570, GL + 120), ant, 1 - a_, n=30, seed=23)
    if rubble:
        for x, y, r in ((CX0 + 34, GL + 300, 26), (CX1 - 30, GL + 290, 24), (CX0 + 40, GL + 92, 22), (CX1 - 38, GL + 96, 22), (572, GL + 86, 20), (CX0 + 30, GL + 500, 28), (CX1 - 26, GL + 520, 26)):
            ell(c, x, y, r, r * .8); fs(c, hx('8c8c88'), 5)
    for name in THROWS:                                                                   # stones in flight, over everything in the chasm
        st = stone_at(name, f)
        if st and st[0] == 'flight':
            e = [b for b in BRIDGE if b[0] == name][0]
            if st[3] < .5: rock(c, st[1], st[2], RS, name, rot=-.06 + st[3] * 1.2, ty=-34)
            else: slab(c, st[1], st[2], lerp(RS, e[3], st[3]), lerp(RS, e[4], st[3]), name, e[5] + (1 - st[3]) * .6)

def held_stone(f):
    """The stone over Hoody's head (name), if he is holding one, else None."""
    if f < 36: return 'FAIL'
    for name, (a, b) in LIFTS.items():
        if b <= f < THROWS[name][0]: return name
    if f >= 495: return 'FAIL'
    return None

def eva_draw(c, f):
    if f < 118 or f >= 440: KP.eva(c, 'urge'); return
    ex = lerp(890, 955, ss(seg(f, 182, 196))) if f < 420 else lerp(955, 890, ss(seg(f, 420, 440)))
    ell(c, ex + 70, GL - 22, 16, 22); fs(c, hx('f3efe6'), 5)                               # her cup, set down on the sand while she claps
    if f < 245:                                                                           # claps from his step on - for HIM; turns, still clapping, to IT
        apart = (f // 3) % 2; ex_ = 'laugh' if f < 150 else ('notices' if f < 166 else 'laugh')
        shadow(c, ex, 70); E.eva(c, ex, GL, HS, ex_, pose='holdlow', hand_to=(ex + (70 if not apart else -60) * HS, GL - (560 if not apart else 600) * HS), leash=False, cup=False)
        if not apart:                                                                     # the clap's spark lines
            for q in (-1, 0, 1): c.move_to(ex + 70 * HS + q * 26, GL - 620 * HS); c.line_to(ex + 70 * HS + q * 40, GL - 680 * HS); c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
    else:
        shadow(c, ex, 70); E.eva(c, ex, GL, HS, 'amused', leash=False, cup=False)

def hoody_draw(c, f):
    if f >= 495 and f < 525 or 36 <= f < 52 and False: pass
    held = held_stone(f)
    if held:
        teeter = .09 if f >= 495 else .06
        if 495 <= f < 510: teeter = lerp(.0, .09, seg(f, 495, 510))
        shadow(c, HX + 10, 95)
        c.save(); c.translate(HX, GL); c.rotate(teeter); c.translate(-HX, -GL)
        lift = 1.0
        if held in LIFTS: lift = ss(seg(f, *LIFTS[held]))
        if f >= 495: lift = ss(seg(f, 480, 495))
        cx, cy = lerp(PILE[0], RC[0], lift), lerp(PILE[1], RC[1], lift)
        if 495 <= f < 512: cy += 26 * math.sin(math.pi * seg(f, 495, 512))               # the weight lands on him: a sag
        sc = RS                                                                           # every held stone: frame 0's rock, its word above his hair
        rock(c, cx, cy, sc, held, rot=-.06, ty=-34)
        braced_hoody(c, HX, HS, f, (cx, cy), sc, teeter); sweat(c, HX + 150 * HS, HY - 20 * HS, HS); c.restore(); return
    if 105 <= f < 232:                                                                    # "Success!": foot up; it overtakes; the foot comes down
        k = ss(seg(f, 112, 124)) * (1 - ss(seg(f, 200, 230)))
        step_hoody(c, 'happy' if f < 150 else ('shock' if f < 215 else 'deadpan'), foot=(150 * k, -130 * k)); return
    if 360 <= f < 420:                                                                    # steps onto BUG - it vanishes under his foot
        k = ss(seg(f, 360, 372)) * (1 - ss(seg(f, 400, 414)))                           # foot out onto BUG ... and back
        drop = 22 * ss(seg(f, 379, 385)) * (1 - ss(seg(f, 400, 410)))                      # BUG gone: the foot sinks a little
        flail = 396 <= f < 412; lean = -.13 * ss(seg(f, 396, 400)) * (1 - ss(seg(f, 408, 416)))
        expr = 'hopeful' if f < 379 else ('shock' if f < 388 else ('deadpan' if f < 396 else 'shock'))   # looks down - at us - then panics
        step_hoody(c, expr, foot=(150 * k, -40 * k + drop), lean=lean if lean else None, arms=('flail', 'flail') if flail else ('rest', 'rest')); return
    shadow(c, HX, 95); R.hoody(c, HX, GL, HS, expr='deadpan' if f >= 200 else 'calm', arms=('rest', 'rest'))

def label(f): return 'ITS SUCCESS' if 245 <= f < 500 else 'HIS SUCCESS'

def bubbles(c, f):
    ax, ay, s, _ = ai_state(f)
    if f < 45 or f >= 505: TL.bubble(c, ['EVERY FAILURE...'], 10, ear(), cy=1010, cx=650, size=52, bend=-.1)
    elif f < 105: TL.bubble(c, ['...BUILDS SUCCESS!'], f - 45, ear(), cy=1010, cx=650, size=52, bend=-.1)
    if 116 <= f < 150: TL.bubble(c, ['SUCCESS!'], f - 116, ear(), cy=640, cx=600, size=60, bend=-.1)
    if 285 <= f < 345: TL.bubble(c, ['THANKS FOR THE', 'TRAINING DATA!'], f - 285, TL.robot_top(ax, ay, s, 1, dx=40), cy=600, cx=660, size=54, bend=.1)
    if 440 <= f < 478: TL.bubble(c, ['MORE?'], f - 440, TL.robot_top(AX, GL, AS, -1, dx=40), cy=500, cx=190, size=60, bend=.05)

def hook(f, with_bubbles):
    """Frames 0-35 and 525-539: frame 0's composition exactly (its stills pose), teeter swaying about .09."""
    g = f if f < 36 else f - (NF - 1)                                                  # the last frame is frame 0
    S, _, _ = F.draw(0, .09 + .03 * math.sin(2 * math.pi * g / 36))
    if with_bubbles: TL.bubble(cairo.Context(S), ['EVERY FAILURE...'], 10, ear(), cy=1010, cx=650, size=52, bend=-.1)
    return S

def draw_old(f, with_bubbles=True):
    if f < 36 or f >= 525: return hook(f, with_bubbles)
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(S)
    if 240 <= f < 270:                                                                    # the deadpan close-up; only the capsule pops
        g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, *hx('ffd27a')); g.add_color_stop_rgb(1, *hx('fff3d6')); c.set_source(g); c.paint()
        K.hoodie(c, 540, 1080 + 150 * 2.4, 2.4 * 1.1)
        K.hoodyz_head(c, 540, 1080, 2.4, era='young', expr='deadpan', blink=252 <= f < 257, gaze=lerp(0, -14, ss(seg(f, 256, 268))))   # a slow blink, eyes slide away
        capsule_pop(c, label(f), 1.0); return S
    ax, ay, s, kw = ai_state(f); ant = antenna(ax, ay, s)
    sign = ss(seg(f, 182, 188)) * (1 - ss(seg(f, 270, 300)))
    backdrop(c, 0); chasm(c); rock(c, 60, GL - 34, .4, ''); rock(c, 118, GL - 26, .3, ''); success_sign(c, 845, 470, sign, word=not 360 <= f < 420)   # the push-in crops the sign: its word would sit under the app buttons
    bridge(c, f, ant)
    if 270 <= f < 305: particles(c, (845, 470), (ax, ay - 288 * s), seg(f, 270, 305), n=20, col=YEL, seed=4)
    eva_draw(c, f)
    if ay >= GL - 40 and kw.get('rot', 0) == 0: shadow(c, ax, 60, ay)
    def halo():                                                                           # the success, kept: a gold halo BEHIND its head (the screen stays bright)
        if not (282 <= f < 420): return
        hx_, hy_ = ax, ay - 288 * s
        for r_, a_ in ((150, .22), (120, .32)): ell(c, hx_, hy_, r_ * s, r_ * .8 * s); c.set_source_rgba(*YEL, a_); c.fill()
        for k_ in range(4):
            a_ = f * .2 + k_ * 1.57; sx_, sy_ = hx_ + math.cos(a_) * 160 * s, hy_ + math.sin(a_) * 120 * s
            c.move_to(sx_ - 12, sy_); c.line_to(sx_ + 12, sy_); c.move_to(sx_, sy_ - 12); c.line_to(sx_, sy_ + 12); c.set_source_rgb(*hx('f0b400')); c.set_line_width(5); c.stroke()
    behind = f < 150 or f >= 345                                                          # going up onto his back it passes BEHIND him: his face stays clear
    if behind: halo(); robot(c, ax, ay, s, kw)
    hoody_draw(c, f)
    if not behind: halo(); robot(c, ax, ay, s, kw)
    if 420 <= f < 495:                                                                    # the new FAIL: from the pile, up into its hands, offered
        k = ss(seg(f, 426, 438)); up = ss(seg(f, 470, 484)); over = ss(seg(f, 484, 495))
        x = lerp(PILE[0], AX + 70, k); y = lerp(PILE[1], GL - 190, k)
        x, y = lerp(x, AX + 45, up), lerp(y, RC[1] - 40, up)                               # held up on ITS side, left of his face
        x, y = lerp(x, RC[0], over), lerp(y, RC[1], over)                                  # then over, above his head
        rock(c, x, y, lerp(.55, RS, max(up * .5, over)), 'FAIL', rot=-.06, ty=lerp(-10, -34, over))
    if with_bubbles: bubbles(c, f)
    if 360 <= f < 420:                                                                    # medium shot: his face and the foot over the void
        big = S; S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); cc = cairo.Context(S)
        cc.translate(540, 1000); cc.scale(1.25, 1.25); cc.translate(-415, -(GL - 360)); cc.set_source_surface(big, 0, 0); cc.paint(); c = cc; c.identity_matrix()   # Eva (x 975) out of frame, the robot in
    lab = label(f)
    pop = 1.0
    F.topbar(c, lab) if not (500 <= f < 510) else capsule_pop(c, lab, 1.0)
    return S

# ======== v4: the stone montage (A) - accelerating throws, 12 failures, the hole fills; total length unchanged ========
SMALL = [('NO', 455, GL + 60, .34), ('ERROR', 690, GL + 70, .34), ('OOPS', 520, GL + 190, .3), ('500', 640, GL + 200, .3),
         ('NOPE', 430, GL + 150, .3), ('TRY AGAIN', 700, GL + 160, .3), ('?!', 575, GL + 40, .3), ('NULL', 470, GL + 250, .3)]
M0, M1, SHIFT = 36, 145, 35                                       # montage frames; everything after shifts +35, then two holds give 35 back
def old_of(n):
    """New frame -> the frame of the v3 timeline (outside the montage)."""
    o = n - SHIFT
    if o >= 205: o += 20                                          # the held bow: 20 frames shorter
    if o >= 455: o += 15                                          # the hold after "More?": 15 frames shorter
    return o
def new_of(o):
    """v3 frame -> new frame (for sound cues)."""
    if o < 110: return o + SHIFT if o >= 36 else o
    n = o + SHIFT
    if o >= 225: n -= 20
    if o >= 470: n -= 15
    return n
# the montage's throws (new frames): (name, lift start, throw start, landing, kind, x, y)
MTH = [('FAIL', None, 36, 48, 'big'), ('REJECTED', 50, 56, 66, 'big')]
MTH += [(w, t - 3, t, t + 5, 'small') for (w, *_), t in zip(SMALL, range(70, 110, 5))]
MTH += [('BUG', 110, 114, 122, 'big'), ('404', 124, 128, 138, 'big')]
LANDS = [m[3] for m in MTH]
def spot(name):
    for w, x, y, s_ in SMALL:
        if w == name: return x, y, s_
    e = [b for b in BRIDGE if b[0] == name][0]; return e[1], e[2], None

def montage(n, with_bubbles=True):
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(S)
    k = max([1 - (n - b) / 4 for b in LANDS if 0 <= n - b < 4] + [0])          # camera jolt on every landing
    big = sum(1 for m in MTH if m[4] == 'big' and 0 <= n - m[3] < 4)
    c.save(); c.translate(0, -(abs((n * 53) % 9 - 4) + 2) * 1.6 * k * (2 if big else 1))          # a vertical thump, upwards only: keeps the words inside the safe zone
    backdrop(c, 0); chasm(c); rock(c, 60, GL - 34, .4, ''); rock(c, 118, GL - 26, .3, ''); success_sign(c, 845, 470, 0)
    held = None; flying = None
    for name, lift, t, land, kind in MTH:                                       # landed stones (deepest first), the one in flight
        x, y, s_ = spot(name)
        if n >= land:
            if kind == 'big':
                e = [b for b in BRIDGE if b[0] == name][0]; slab(c, x, y, e[3], e[4], name, e[5])
            else: rock(c, x, y, s_, name, rot=(x % 7 - 3) * .06, ty=0)
            if n - land < 6:
                for kk in range(5): ell(c, x - 80 + kk * 40, y - 24 - (kk % 2) * 10, 22 * (1 + (n - land) * .1), 12); c.set_source_rgba(*hx('e9c98f'), .8 * (1 - (n - land) / 6)); c.fill()
        elif t <= n < land: flying = (name, kind, seg(n, t, land), x, y, s_)
        elif (lift is not None and lift <= n < t) or (name == 'FAIL' and n < t): held = (name, kind, ss(seg(n, lift, t)) if lift is not None else 1)
    if n >= 66:                                                                 # rubble jammed in once REJECTED sits
        for x, y, r in ((CX0 + 34, GL + 300, 26), (CX1 - 30, GL + 290, 24), (CX0 + 30, GL + 500, 28), (CX1 - 26, GL + 520, 26)):
            ell(c, x, y, r, r * .8); fs(c, hx('8c8c88'), 5)
    if flying:
        name, kind, u, x, y, s_ = flying; tx = 1 - (1 - u) ** 2; ty = u * u
        fx_, fy_ = lerp(RC[0], x, tx), lerp(RC[1] - 60, y, ty) - 90 * math.sin(math.pi * min(1, u * 1.4))
        if kind == 'big' and u >= .5:
            e = [b for b in BRIDGE if b[0] == name][0]; slab(c, fx_, fy_, lerp(RS, e[3], u), lerp(RS, e[4], u), name, e[5] + (1 - u) * .6)
        else: rock(c, fx_, fy_, RS if kind == 'big' else .45, name, rot=-.06 + u * 1.2, ty=-34 if kind == 'big' else 0)
    KP.eva(c, 'urge')
    ant_glow = .7 if any(0 <= n - b < 4 for b in LANDS) else 0                  # its antenna blinks on every landing: it is watching (learning)
    shadow(c, AX, 60); A.myai(c, AX, GL, AS, eye='open', look=(14, -12), talk=ant_glow)
    tired = seg(n, 70, 140)                                                     # he wears out: more sweat, then the flat face
    expr = 'shock' if n < 118 else 'deadpan'
    shadow(c, HX + 10, 95)
    if held:
        name, kind, lift = held; teeter = .06 + .05 * tired
        c.save(); c.translate(HX, GL); c.rotate(teeter); c.translate(-HX, -GL)
        sc = RS if kind == 'big' else .5
        src = (PILE[0] + 50, PILE[1]) if kind == 'big' else (HX - 70, GL - 330)                  # small ones come up from behind him, clear of the robot
        cx, cy = lerp(src[0], RC[0], lift), lerp(src[1], RC[1] + (0 if kind == 'big' else 40), lift)
        rock(c, cx, cy, sc, name, rot=-.06, ty=-34 if kind == 'big' else 0)
        braced_hoody(c, HX, HS, n, (cx, cy), sc, teeter)
        for kk in range(1 + int(tired * 3)): sweat(c, HX + (150 - kk * 40) * HS, HY - (20 + kk * 30) * HS, HS)
        c.restore()
    else:
        R.hoody(c, HX, GL, HS, expr=expr, arms=('up', 'up') if 70 <= n < 110 else ('rest', 'rest'), f=n)
        for kk in range(int(tired * 3)): sweat(c, HX + (150 - kk * 40) * HS, HY - (20 + kk * 30) * HS, HS)
    c.restore()
    if with_bubbles:
        if n < 45: TL.bubble(c, ['EVERY FAILURE...'], 10, ear(), cy=1010, cx=650, size=52, bend=-.1)
        elif n < 120: TL.bubble(c, ['...BUILDS SUCCESS!'], n - 45, ear(), cy=1010, cx=650, size=52, bend=-.1)
    F.topbar(c, 'HIS SUCCESS')
    return S

def draw(n, with_bubbles=True):
    if n < M0 or n >= 525: return draw_old(n, with_bubbles)
    if n < M1: return montage(n, with_bubbles)
    return draw_old(old_of(n), with_bubbles)

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'sheet'
    if cmd == 'frames':
        for n in map(int, sys.argv[2:]): draw(n).write_to_png(os.path.join(HERE, f'an_{n:03d}.png'))
    elif cmd == 'sheet':
        from PIL import Image, ImageDraw
        out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, 'an_sheets'); os.makedirs(out, exist_ok=True)
        for bub in (True, False):
            fr = list(range(0, NF, 8)); per = 24; tw, th = 240, 427
            for p in range(0, len(fr), per):
                ch = fr[p:p + per]; rows = (len(ch) + 5) // 6
                im = Image.new('RGB', (6 * tw, rows * th), (25, 25, 25)); d = ImageDraw.Draw(im)
                for i, f in enumerate(ch):
                    S = draw(f, bub); x, y = (i % 6) * tw, (i // 6) * th
                    im.paste(Image.frombuffer('RGBA', (W, H), bytes(S.get_data()), 'raw', 'BGRA', 0, 1).convert('RGB').resize((tw, th)), (x, y))
                    d.rectangle([x, y, x + 72, y + 14], fill=(0, 0, 0)); d.text((x + 3, y + 1), '#%d %.2fs' % (p + i + 1, f / 30), fill=(255, 255, 0))
                im.save(os.path.join(out, f'{"bub" if bub else "mute"}_{p // per + 1}.png'))
        print(out)
