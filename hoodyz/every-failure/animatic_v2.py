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
PILE = (90, GL - 40)

def antenna(x, gy, s): return (x, gy - 430 * s)

def ai_state(f):
    """MY AI: (x, gy, s, kw) per frame - behind him, hop off his back onto the deck, walk over, bow, walk back eating the deck, hop home."""
    s = AS
    if f < 135 or f >= 495: return AX, GL, s, dict(eye='open', look=(14, -12), talk=.7 if any(0 <= f - b < 4 for _, b in THROWS.values()) else 0)
    if f < 147:                                                                           # up onto his back
        t = seg(f, 135, 147); x = lerp(AX, HX + 30, t); y = lerp(GL, GL - 690, t) - 120 * math.sin(math.pi * t)
        return x, y, s, dict(eye='happy', arms=('up', 'up'))
    if f < 160:                                                                           # off his back, down onto the deck (BUG)
        t = seg(f, 147, 160); x = lerp(HX + 30, 478, t); y = lerp(GL - 690, DECK, t) - 160 * math.sin(math.pi * t)
        return x, y, s, dict(eye='happy', arms=('up', 'down'))
    if f < 182:                                                                           # strides over BUG and 404 to the far bank
        t = seg(f, 160, 182); x = lerp(478, 780, t); y = DECK if x < CX1 else GL
        return x, y, s, dict(eye='happy', walk=f * .7)
    if f < 300:                                                                           # the bow, held
        b = ss(seg(f, 190, 204)) * (1 - ss(seg(f, 226, 238)))
        return 780, GL, s, dict(eye='happy', rot=-.3 * b, talk=0)                    # bows towards Hoody: the performer's bow
    if f < 330:                                                                           # walks back over the deck, towards Hoody
        t = seg(f, 300, 330); x = lerp(780, 478, t); y = DECK if x < CX1 else GL
        return x, y, s, dict(eye='happy', walk=f * .7, turn=-.5, talk=.8 if 285 <= f < 320 else 0)
    if f < 345: return 478, DECK, s, dict(eye='happy', turn=-.5)
    if f < 360:                                                                           # hops over his head, home
        t = seg(f, 345, 360); x = lerp(478, AX, t); y = lerp(DECK, GL, t) - 520 * math.sin(math.pi * t)
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

def particles(c, src, dst, k, n=26, col=TEAL, seed=1):
    """Blocks streaming from src to dst; k = progress 0..1 of the stream (each block leaves a little later)."""
    rnd = random.Random(seed)
    for i in range(n):
        t = cl(k * 1.6 - i / n * .6)
        if t <= 0 or t >= 1: continue
        x = lerp(src[0], dst[0], t) + rnd.uniform(-18, 18) * (1 - t); y = lerp(src[1], dst[1], t * t * (3 - 2 * t))
        z = 26 - 14 * t; c.rectangle(x - z / 2, y - z / 2, z, z); c.set_source_rgba(*col, .95); c.fill_preserve(); c.set_source_rgba(*INK, .5); c.set_line_width(2); c.stroke()

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
    if f < 150 or f >= 440: KP.eva(c, 'urge'); return
    if f < 182: KP.EX = 890; E.eva(c, 890, GL, HS, 'notices', gaze=-16, leash=False); shadow(c, 890, 70); return
    ex = lerp(890, 975, ss(seg(f, 182, 196))) if f < 420 else lerp(975, 890, ss(seg(f, 420, 440)))
    ell(c, ex + 70, GL - 22, 16, 22); fs(c, hx('f3efe6'), 5)                               # her cup, set down on the sand while she claps
    if f < 245:
        apart = (f // 3) % 2
        shadow(c, ex, 70); E.eva(c, ex, GL, HS, 'laugh', pose='holdlow', hand_to=(ex + (70 if not apart else -60) * HS, GL - (560 if not apart else 600) * HS), leash=False, cup=False)
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
        sc = RS                                                                           # every held stone: frame 0's rock, its word above his hair
        rock(c, cx, cy, sc, held, rot=-.06, ty=-34)
        braced_hoody(c, HX, HS, f, (cx, cy), sc, teeter); sweat(c, HX + 150 * HS, HY - 20 * HS, HS); c.restore(); return
    if 105 <= f < 232:                                                                    # "Success!": foot up; it overtakes; the foot comes down
        k = ss(seg(f, 112, 124)) * (1 - ss(seg(f, 200, 230)))
        step_hoody(c, 'happy' if f < 150 else ('shock' if f < 215 else 'deadpan'), foot=(150 * k, -130 * k)); return
    if 360 <= f < 420:                                                                    # steps onto BUG - it vanishes under his foot
        k = ss(seg(f, 360, 372)) * (1 - ss(seg(f, 398, 415)))
        step_hoody(c, 'hopeful' if f < 380 else 'shock', foot=(150 * k, -40 * k)); return
    shadow(c, HX, 95); R.hoody(c, HX, GL, HS, expr='deadpan' if f >= 200 else 'calm', arms=('rest', 'rest'))

def label(f): return 'ITS SUCCESS' if 245 <= f < 500 else 'HIS SUCCESS'

def bubbles(c, f):
    ax, ay, s, _ = ai_state(f)
    if f < 45 or f >= 505: TL.bubble(c, ['EVERY FAILURE...'], 10, ear(), cy=1010, cx=650, size=52, bend=-.1)
    elif f < 105: TL.bubble(c, ['...BUILDS SUCCESS!'], f - 45, ear(), cy=1010, cx=650, size=52, bend=-.1)
    if 112 <= f < 150: TL.bubble(c, ['SUCCESS!'], f - 112, ear(), cy=640, cx=600, size=60, bend=-.1)
    if 285 <= f < 345: TL.bubble(c, ['THANKS FOR THE', 'TRAINING DATA!'], f - 285, TL.robot_top(ax, ay, s, 1, dx=40), cy=640, cx=600, size=54, bend=.1)
    if 440 <= f < 478: TL.bubble(c, ['MORE?'], f - 440, TL.robot_top(AX, GL, AS, -1, dx=40), cy=560, cx=190, size=60, bend=.05)

def hook(f, with_bubbles):
    """Frames 0-35 and 525-539: frame 0's composition exactly (its stills pose), teeter swaying about .09."""
    g = f if f < 36 else f - (NF - 1)                                                  # the last frame is frame 0
    S, _, _ = F.draw(0, .09 + .03 * math.sin(2 * math.pi * g / 36))
    if with_bubbles: TL.bubble(cairo.Context(S), ['EVERY FAILURE...'], 10, ear(), cy=1010, cx=650, size=52, bend=-.1)
    return S

def draw(f, with_bubbles=True):
    if f < 36 or f >= 525: return hook(f, with_bubbles)
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(S)
    if 240 <= f < 270:                                                                    # the deadpan close-up; only the capsule pops
        R.head_close(c, f, 'deadpan', bgc=('ffd27a', 'fff3d6'), s=2.4, y=1080)
        capsule_pop(c, label(f), 1.0); return S
    ax, ay, s, kw = ai_state(f); ant = antenna(ax, ay, s)
    sign = ss(seg(f, 182, 188)) * (1 - ss(seg(f, 270, 300)))
    backdrop(c, 0); chasm(c); rock(c, 60, GL - 34, .4, ''); rock(c, 118, GL - 26, .3, ''); success_sign(c, 845, 470, sign)
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
    behind = f < 147 or f >= 345                                                          # going up onto his back it passes BEHIND him: his face stays clear
    if behind: halo(); A.myai(c, ax, ay, s, **kw)
    hoody_draw(c, f)
    if not behind: halo(); A.myai(c, ax, ay, s, **kw)
    if 420 <= f < 495:                                                                    # the new FAIL: from the pile, up into its hands, offered
        k = ss(seg(f, 426, 438)); up = ss(seg(f, 470, 484)); over = ss(seg(f, 484, 495))
        x = lerp(PILE[0], AX + 70, k); y = lerp(PILE[1], GL - 190, k)
        x, y = lerp(x, AX - 10, up), lerp(y, RC[1] - 40, up)                               # held up on ITS side, left of his face
        x, y = lerp(x, RC[0], over), lerp(y, RC[1], over)                                  # then over, above his head
        rock(c, x, y, lerp(.55, RS, max(up * .5, over)), 'FAIL', rot=-.06, ty=lerp(-10, -34, over))
    if with_bubbles: bubbles(c, f)
    if 360 <= f < 420:                                                                    # medium shot: his face and the foot over the void
        big = S; S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); cc = cairo.Context(S)
        cc.translate(540, 1000); cc.scale(1.55, 1.55); cc.translate(-440, -(GL - 380)); cc.set_source_surface(big, 0, 0); cc.paint(); c = cc; c.identity_matrix()
    lab = label(f)
    pop = 1.0
    F.topbar(c, lab) if not (500 <= f < 510) else capsule_pop(c, lab, 1.0)
    return S

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
