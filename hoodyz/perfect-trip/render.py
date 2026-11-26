"""ME + MY AI - Perfect Trip. Timed rough: 10 shots, 1080x1920, 30 fps.
Each place: the live scene (MY AI directs, Hoody loses his role), the shutter, the album photo with its stamp.
Rome: the couple photo, HIS TRIP -> ITS TRIP, the pull back to the phone in Hoody's hands, "THANKS FOR THE PHOTOS!", "ONE MORE?".
Hoody's lines and reactions are Tomas's recorded takes (vo/h_*.wav).
Usage: python3 render.py frames 0 60 ...  |  python3 render.py video  |  python3 render.py final"""
import os, sys, math, subprocess, cairo
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import trip_photos as TP
import photo as PH
import places as P
from trip_photos import R, K, Sh, E, A, tele_arm, backpack_cat, camel, suitcase
from kit import INK, WHITE, NAVY, YEL, rr, fs, ell, limb, hx, lerp, cl, ss, txt
W, H = 1080, 1920
oe = lambda t: 1 - (1 - cl(t)) ** 3

# ---------------- voices: where each line sits (shot index, seconds in); the mix and the lip sync both read this
VO = [('h_invite', 0, .07, .8), ('ai_plan', 0, 2.75, .7), ('h_selfie', 2, .1, .8), ('h_proud', 3, .35, .6), ('ai_stepback', 5, .25, .7),
      ('h_huh', 5, 1.25, .6), ('ai_more', 7, .2, .95), ('h_whoa', 7, .75, .6), ('h_effort', 7, 1.35, .5),
      ('h_howtrip', 11, .3, .8), ('ai_thanks', 11, 3.0, .7), ('h_sigh', 11, 4.1, .55), ('h_another', 12, .35, .8)]   # Hoody: Tomas's takes
_ENV = {}
def env(name):
    if name not in _ENV:
        import soundfile as sf, numpy as np
        x, sr = sf.read(os.path.join(HERE, 'vo', name + '.wav')); x = x if x.ndim == 1 else x[:, 0]
        n = sr // 30; m = len(x) // n
        e = 20 * np.log10(np.sqrt((x[:m * n].reshape(m, n) ** 2).mean(1)) + 1e-6)
        lo, hi = np.percentile(e, 35), np.percentile(e, 97)
        _ENV[name] = np.clip(np.convolve(np.clip((e - lo) / (hi - lo + 1e-9), 0, 1), [.2, .6, .2], 'same'), 0, 1) ** 1.3
    return _ENV[name]
def talk(f, name):
    for nm, shot, off, g in VO:
        if nm == name:
            i = f - SHOTS[shot][1] - int(round(off * 30)); e = env(name)
            return float(e[i]) if 0 <= i < len(e) else 0.0
    return 0.0

def flash(c, r):
    """The shutter: a soft white fade (never a full white frame)."""
    if r < 5: c.set_source_rgba(1, 1, 1, .55 * (1 - r / 5)); c.paint()
def edge_pisa(y, q): return 640 + math.tan(math.radians(8)) * (P.GY - 60 - y) + q * 115

# ---------------- the shots
# ---------------- the bench, before and after (the series' home: Perfect Date's park)
BS, BX0, BX1 = 1450, 140, 940                                              # seat height, bench ends (in the zoomed frame)
def bench_scene(c, f):
    R.park(c, f, zoom=1.35, cy=1500)
    R.bench(c, BX0, BX1, BS, BS + 150)
    Sh.cat_one_eye(c, 860, BS - 6, .8, open_eye=False)
def eva_seated(c, x, es, expr='evacalm', tilt=0, pose='coffee', sip=.2, hand_to=None, blink=False):
    c.save(); c.rectangle(0, 0, W, BS + 6); c.clip()
    hand = E.eva(c, x, BS + 250 * es, es, expr, sip=sip, tilt=tilt, pose=pose, hand_to=hand_to, blink=blink); c.restore()
    for q in (-1, 1):
        limb(c, [(x + q * 34 * es, BS + 4), (x + q * 38 * es, BS + 150)], 32 * es, E.TROUS)
        ell(c, x + q * 34 * es, BS + 6, 36 * es, 26 * es); fs(c, E.TROUS, 5)
        ell(c, x + q * 42 * es, BS + 156, 30 * es, 14 * es); fs(c, E.SHOE, 4)
    return hand

AI_HIDE, AI_UP = 1662, 1310                                               # MY AI behind the bench: only its antenna showing / popped up
def two_shot(c, f, ai_gy, ai_kw, hoody_op, eva_expr='evacalm', nod=0, hoody_gaze=20):
    """The bench two-shot that opens and closes the film (so the loop is seamless): MY AI's antenna peeks over the backrest."""
    bench_scene_back(c, f)
    c.save(); c.rectangle(0, 0, W, BS - 204); c.clip()                  # behind the backrest: only what rises above it shows
    A.myai(c, 540, ai_gy, 1.1, **ai_kw); c.restore()
    bench_front(c)
    R.hoody(c, 330, BS, 1.0, expr='hopeful', pose='sit', seat=(BX0, BX1), arms=('rest', 'rest'), op=hoody_op, gaze=hoody_gaze, f=f)
    eva_seated(c, 760, 1.0, eva_expr, tilt=nod, blink=K.blinking(f, 7))

def s_invite(c, f, r):  # before: "Do you want to go on a trip?" - she nods - MY AI (its antenna there all along) pops up
    pop = oe((r - 76) / 8)
    two_shot(c, f, lerp(AI_HIDE, AI_UP, pop),
             dict(eye='focus' if r > 86 else 'wide', arms=('up', 'up') if r < 90 else ('down', 'wave'), talk=talk(f, 'ai_plan')),
             .2 + .8 * talk(f, 'h_invite'), 'charmed' if r >= 62 else 'evacalm',
             math.sin(cl((r - 62) / 12) * math.pi * 2) * .08 if 62 <= r < 74 else 0)
    if r < 78: R.bubble(c, ['DO YOU WANT TO', 'GO ON A TRIP?'], 10, (394, 1176), cy=905, cx=430, size=54)   # up at frame 0; short tail to his cheek (v2)
    if r >= 80: R.bubble(c, ["I'LL PLAN", 'EVERYTHING!'], r - 80, (540, lerp(AI_HIDE, AI_UP, pop) - 420 * 1.1), cy=720, cx=560, size=58)
def bench_scene_back(c, f):
    R.park(c, f, zoom=1.35, cy=1500)
def bench_front(c):
    R.bench(c, BX0, BX1, BS, BS + 150)
    Sh.cat_one_eye(c, 860, BS - 6, .8, open_eye=False)

_PHOTO = None
def s_after(c, f, r):   # after: "How did you like our trip?" - she turns her phone: the Rome photo. MY AI: "THANKS FOR THE PHOTOS!"
    global _PHOTO
    if _PHOTO is None:
        _PHOTO = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); TP.rome(cairo.Context(_PHOTO), 0, label='ITS TRIP')
    bench_scene(c, f)
    R.hoody(c, 300, BS, 1.0, expr='hopeful' if r < 96 else 'bored', pose='sit', seat=(BX0, BX1), arms=('rest', 'rest'),
            op=.2 + .8 * talk(f, 'h_howtrip'), gaze=20, f=f)
    A.myai(c, 880, BS - 6, 1.0, eye='happy', arms=('down', 'wave' if r > 90 else 'down'), talk=talk(f, 'ai_thanks'))
    turn = oe((r - 62) / 10)
    eva_seated(c, 640, 1.0, 'charmed', tilt=-.15 * turn, blink=K.blinking(f, 7))
    if turn > 0:                                                         # her phone, turned to him: the Rome photo
        pw, ph = 250 * turn + 20, 440
        px, py = 480 - pw / 2, 1170
        limb(c, [(564, 1160), (600, 1330), (px + pw + 4, py + ph * .62)], 30, E.COAT)          # her yellow sleeve: it's her phone
        rr(c, px - 10, py - 10, pw + 20, ph + 20, 30); fs(c, hx('1d2130'), 6)
        c.save(); rr(c, px, py, pw, ph, 22); c.clip(); c.translate(px, py); c.scale(pw / W, ph / H); c.set_source_surface(_PHOTO, 0, 0); c.paint(); c.restore()
        ell(c, px + pw + 6, py + ph * .6, 26, 30); fs(c, E.SKIN_E, 5)
    if r < 88: R.bubble(c, ['HOW DID YOU LIKE', 'OUR TRIP?'], r - 4, (366, 1176), cy=905, cx=430, size=56)
    if r >= 90: R.bubble(c, ['THANKS FOR', 'THE PHOTOS!'], r - 90, (880, BS - 6 - 420), cy=755, cx=700, size=56)
def s_another(c, f, r): # "...Another trip?" - quietly, to her. MY AI ducks back behind the bench: the last frame is frame 0
    duck = oe((r - 22) / 10)                                               # a facepalm at "another trip?", then it ducks back down
    fp = 3 <= r < 22
    two_shot(c, f, lerp(AI_UP, AI_HIDE, duck), dict(eye='blank' if fp else 'happy', arms=('down', 'chest' if fp else 'down'), tilt=-12 if fp else 0),
             .2 + .8 * talk(f, 'h_another'))
    if r < 50: R.bubble(c, ['...ANOTHER TRIP?'], r - 8, (394, 1176), cy=940, cx=450, size=58)
    else: R.bubble(c, ['DO YOU WANT TO', 'GO ON A TRIP?'], 10, (394, 1176), cy=905, cx=430, size=54)   # v2: the question for the loop, up before frame 0

def s_rome_act(c, f, r):  # MY AI hands Hoody the phone ("you take it") and sits down with Eva: the cameraman is made
    P.rome(c, f, s=.62, cx=540, horizon=1230)
    PH.ledge(c, 200, 1000, 1520)
    k = oe((r - 6) / 14)
    rx = lerp(820, 450, oe((r - 18) / 16))
    A.myai(c, rx, lerp(1840, 1514, oe((r - 18) / 16)), 1.3, eye='happy', arms=('down', 'give' if r < 18 else 'wave'))   # hands it over, then hops up beside her
    eva_rome(c)
    hx_ = 160; R.hoody(c, hx_, 1880, 1.0, expr='hopeful' if r < 20 else 'bored', arms=('rest', 'take'), f=f)
    hp = (lerp(820 + 130, hx_ + 200, k), lerp(1600, 1420, k))                 # the phone, from its hand to his
    rr(c, hp[0] - 40, hp[1] - 70, 80, 140, 16); fs(c, hx('1d2130'), 6)
    backpack_cat(c, 900, 1720, .9, 'resigned')
def eva_rome(c):
    es, ex, TOP = 1.05, 650, 1520
    c.save(); c.rectangle(0, 0, W, TOP + 6); c.clip()
    E.eva(c, ex, TOP + 250 * es, es, 'charmed', sip=.1, tilt=-.1); c.restore()
    for q in (-1, 1):
        limb(c, [(ex + q * 34 * es, TOP + 4), (ex + q * 38 * es, TOP + 200)], 32 * es, E.TROUS)
        ell(c, ex + q * 34 * es, TOP + 6, 36 * es, 26 * es); fs(c, E.TROUS, 5)

def s_open(c, f, r):   # frame 0: the giant face in the phone preview at Pisa - "ONE SELFIE?"
    P.pisa(c, f)
    E.eva_head(c, 900, 1420, 1.0, 'charmed', tilt=-.15)                     # she's in the frame too, squeezed at the edge
    K.hoodie(c, 540, 1080 + 150 * 2.8, 2.8 * 1.1)
    K.hoodyz_head(c, 540, 1080, 2.8, era='young', expr='happy', blink=False, op=.2 + .8 * talk(f, 'h_selfie'))
    phone_ui(c)
    R.bubble(c, ['ONE SELFIE?'], r + 5, (640, 1262), cy=1130, cx=750, size=54)   # beside the face, short tail to the mouth corner (v2)
    flash(c, r)                                                            # the shutter fires: a hard cut into the photo, no crossfade (v2)
def phone_ui(c):
    """The camera preview: dark rounded corners and a shutter dot."""
    c.rectangle(0, 0, W, H); rr(c, 40, 40, W - 80, H - 80, 70); c.set_fill_rule(cairo.FILL_RULE_EVEN_ODD); c.set_source_rgb(*hx('1d2130')); c.fill()
    c.set_fill_rule(cairo.FILL_RULE_WINDING)
    ell(c, 540, 1800, 52, 52); fs(c, WHITE, 8)

def director_frame(c, x, y, s):
    """MY AI's two hands making a director's frame [ ] in front of its face: the perfectionist sizing up the shot."""
    for q in (-1, 1):
        c.move_to(x + q * 30 * s, y - 50 * s); c.line_to(x + q * 74 * s, y - 50 * s); c.line_to(x + q * 74 * s, y + 50 * s); c.line_to(x + q * 30 * s, y + 50 * s)
        c.set_source_rgb(*INK); c.set_line_width(26 * s); c.stroke_preserve(); c.set_source_rgb(*WHITE); c.set_line_width(14 * s); c.stroke()

def s_pisa(c, f, r):   # live: MY AI sizes up the shot (a director's frame), Hoody strikes the pose, its arm telescopes under the overhang
    k = oe((r - 18) / 24); a = oe(r / 10)
    TP.pisa(c, f, k=k, hoody_a=a, photo=False)
    c.identity_matrix()
    if r < 16:
        rx, rgy, rs = TP.PISA_AI; director_frame(c, rx, rgy - 280 * rs, rs)
# ---------------- the photo-story look: a title card, slow drift towards Hoody's spot, a soft vignette and grain
KB_TARGET = dict(pisa=(720, 1300), paris=(200, 1500), giza=(400, 1330), rome=(300, 1400))   # where the drift ends: his spot (Rome: where he isn't)
def memory_filter(c, f):
    g = cairo.RadialGradient(540, 980, 420, 540, 980, 1200); g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, .1, .06, .02, .32)
    c.set_source(g); c.paint()
    import random
    rnd = random.Random(f * 7919)
    for _ in range(900):
        x, y = rnd.random() * W, rnd.random() * H; v = rnd.random()
        c.rectangle(x, y, 2, 2); c.set_source_rgba(v, v, v, .07); c.fill()
def photo_surface(fn, **kw):
    """Render an album photo without the series bar (the drift must not scale the bar)."""
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); cc = cairo.Context(S)
    keep = Sh.topbar; Sh.topbar = lambda *a, **k: None
    try: fn(cc, 0, **kw)
    finally: Sh.topbar = keep
    return S
_PHOTOS = {}
def kenburns(c, place, r, d, f, **kw):
    if place not in _PHOTOS: _PHOTOS[place] = photo_surface(getattr(TP, place), **kw)
    t = ss(cl(r / d)); z = 1 + .09 * t; tx, ty = KB_TARGET[place]
    c.save(); c.translate(tx, ty); c.scale(z, z); c.translate(-tx, -ty); c.set_source_surface(_PHOTOS[place], 0, 0); c.paint(); c.restore()
    memory_filter(c, f)
def s_photo(place, d):
    def shot(c, f, r):
        kenburns(c, place, r, d, f)
        flash(c, r)
    shot.__name__ = f's_{place}_photo'; return shot
def focus_box(c, k):
    cx, cy, half, L = 720, 840, lerp(360, 250, k), 64
    for col, lw in ((INK, 15), (WHITE, 8)):
        for sx in (-1, 1):
            for sy in (-1, 1):
                c.move_to(cx + sx * half, cy + sy * (half - L)); c.line_to(cx + sx * half, cy + sy * half); c.line_to(cx + sx * (half - L), cy + sy * half)
                c.set_source_rgb(*col); c.set_line_width(lw); c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke()
    c.set_line_cap(cairo.LINE_CAP_BUTT)
def s_title(c, f, r):  # the memory begins: PERFECT TRIP · NOV 2026 for 0.6 s, then the phone's viewfinder opens on Pisa (v2: no empty second)
    P.pisa(c, f); c.set_source_rgba(1, 1, 1, .45 * cl((20 - r) / 8) + .12); c.paint(); memory_filter(c, f)
    a = cl(r / 5) * cl((18 - r) / 5)
    c.select_font_face('Inter', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    for text, size, y, col in (('PERFECT TRIP', 96, 900, INK), ('NOV 2026', 58, 996, hx('374151'))):
        c.set_font_size(size); e = c.text_extents(text)
        c.move_to(540 - e.width / 2 - e.x_bearing, y + 4); c.set_source_rgba(1, 1, 1, .6 * a); c.text_path(text); c.fill()
        c.move_to(540 - e.width / 2 - e.x_bearing, y); c.set_source_rgba(*col, a); c.show_text(text)
    if r >= 15: focus_box(c, ss(cl((r - 15) / 10)))
    if r >= 14:                                                            # the camera opens: dark rounded corners and the shutter dot
        c.push_group(); phone_ui(c); c.pop_group_to_source(); c.paint_with_alpha(ss(cl((r - 14) / 10)))

def s_paris(c, f, r):  # live: "STEP BACK!" - Hoody backs away and shrinks into an extra; MY AI steps in, finger to the spire
    rx, rgy, rs, hz = 900, 1760, 1.25, 1640
    tipxy = (500, 760); s = ((hz - 10) - tipxy[1]) / 1370
    P.paris(c, f, s=s, cx0=tipxy[0], horizon=hz)
    w = ss(cl((r - 14) / 42))                                              # he walks back, slowly, looking back at the robot
    hx_, hgy, hs = lerp(520, 200, w), lerp(1880, hz + 40, w), lerp(1.0, .5, w)
    hx_ = lerp(640, 200, w)
    him = lambda: R.hoody(c, hx_, hgy, hs, step=r * .45 if 0 < w < 1 else None, expr='hopeful' if w < .6 else 'bored', arms=('rest', 'rest'), gaze=24 * w, f=f)
    if w >= .5: him()                                                      # once he's far back, Eva is in front of him
    E.eva(c, 400, 1900, .9, 'impressed' if r > 50 else 'evacalm', sip=.2, gaze=18 if r > 46 else -6, blink=K.blinking(f, 7))
    if w < .5: him()
    k = oe((r - 50) / 18)
    A.myai(c, rx, rgy, rs, eye='focus', arms=(None if k > 0 else 'wave', 'down'), tilt=-4, talk=talk(f, 'ai_stepback'),
           walk=r * 1.6 if 14 < r < 40 else None)   # tapping its foot while he dawdles
    if k > 0:
        sh = (rx - 72 * rs, rgy - 280 * rs + 112 * rs)
        tele_arm(c, rx, rgy, rs, -1, (lerp(sh[0] - 40, tipxy[0], k), lerp(sh[1] - 60, tipxy[1] + 16, k)), tip='claw', grip=ss(cl((k - .72) / .28)))
    backpack_cat(c, 210, 1720, .9, 'shocked' if r > 30 else 'suspicious')
    R.bubble(c, ['STEP BACK!'], r - 4, (rx, rgy - 420 * rs), cy=700, cx=720)

def s_giza(c, f, r):   # live: "MORE!" - the camel (rope round the bags) hauls Hoody back to the luggage; MY AI takes Eva's hand
    P.egypt(c, f, s=.72, cx0=600, horizon=1460)
    d = R.back((r - 22) / 14) if r >= 22 else 0                            # the YANK: overshoot, settle
    rope_to = camel(c, 150, 1500, .42, f, pull=lerp(14, 38, cl(d)))       # the camel leans back as the rope goes taut
    for (x, y, w_, h, col, a) in ((250, 1530, 110, 80, '3f7fd6', 0), (262, 1450, 84, 62, 'e8b23a', .25), (330, 1530, 70, 110, '5aa84f', 0)):
        if y == 1530: ell(c, x, y + 3, w_ * .6, 9); c.set_source_rgba(.45, .3, .1, .25); c.fill()          # contact shadow under the bags
        c.save(); c.translate(x, y); c.rotate(a); suitcase(c, 0, 0, w_, h, col); c.restore()
    if r < 18:                                                             # "MORE!": MY AI hands him the bags first
        bx = lerp(560, 480, oe(r / 12)); suitcase(c, bx, 1640, 110, 80, 'e85a4f')
    hxp, hgy, hs = lerp(560, 400, d), lerp(1860, 1530, d), lerp(.95, .52, d)
    exh = ss(cl((r - 40) / 24))                                            # he wears out: leans further, the knees go deeper
    ell(c, hxp, hgy + 4, 62 * hs / .52 * .52 + 8, 12 * hs / .52 + 3); c.set_source_rgba(.45, .3, .1, .28); c.fill()        # his shadow: feet on the sand
    if .08 < d < 1.05:                                                     # heels drag: a skid line on the sand behind him
        c.move_to(560, 1862); c.line_to(hxp + 10, hgy + 2); c.set_source_rgba(.62, .46, .22, .55); c.set_line_width(7); c.stroke()
    hands, _ = R.hoody(c, hxp, hgy, hs, legs=('drag2' if exh > .5 else 'drag') if d > .03 else 'dangle', expr='shock' if d < .9 else 'wince', arms=('out', 'down'), rot=-(.32 + .12 * exh) * d, f=f)
    if d > .05:
        c.move_to(*hands[0]); c.line_to(*rope_to); c.set_source_rgb(*hx('8a5a2e')); c.set_line_width(6); c.stroke()
        ell(c, hands[0][0], hands[0][1], 17, 14); c.set_source_rgb(*hx('8a5a2e')); c.set_line_width(6); c.stroke()      # the loop round his fist
        ell(c, rope_to[0], rope_to[1] + 14, 22, 16); c.stroke()                                                          # the halter on the camel
        limb(c, [(hands[0][0] - 2, hands[0][1] - 8), (hands[0][0] - 17, hands[0][1] - 3)], 9, K.SKIN)                    # his thumb over the rope
    if d > .9: Sh.sweat(c, 450, 1260, .7)
    if d >= 1.0:                                                           # the trailing toe keeps scuffing: small puffs
        for k in range(3): ell(c, hxp + 58 + k * 22, hgy - 4 - (k % 2) * 8, 10 - k + 3 * math.sin(r * .5 + k), 6); c.set_source_rgba(.92, .82, .62, .7); c.fill()
    if .05 < d < 1.0:                                                      # dust kicked up where his heels drag
        for k in range(6): ell(c, hxp + 30 + k * 24, hgy - 6 - (k % 2) * 10, 26 * (1 - d) + 8, 16 * (1 - d) + 5); c.set_source_rgba(.92, .82, .62, .8); c.fill()
    m = oe((r - 34) / 18)
    rx = lerp(780, 700, m)                                                 # clear of his face, so MORE!'s tail can reach its antenna
    hp = A.hand_at(rx, 1860, 1.3, 1, 'hold')
    E.eva(c, 920, 1880, 1.0, 'laugh' if m > .9 else 'impressed', sip=.1, tilt=-.2 * m, pose='holdlow' if m > .9 else 'coffee', hand_to=hp if m > .9 else None)
    sigh = math.sin(cl(r / 8) * math.pi) * 22 if r < 8 else 0             # a shoulder-drop sigh before MORE!
    if 0 < r < 9: txt(c, 'pff', rx + 120, 1200, 50, NAVY, lw=0)
    A.myai(c, rx, 1860 + sigh, 1.3, eye='focus' if r < 30 else 'happy', arms=('wave', 'hold' if m > .9 else 'down'), tilt=10 * m, talk=talk(f, 'ai_more'))
    backpack_cat(c, 210, 1720, .9, 'disapproving')
    R.bubble(c, ['MORE!'], r - 2, (rx, 1860 - 420 * 1.3), cy=1030, cx=700)

def s_rome(c, f, r):   # the couple photo, drifting; the label switches after it lands
    kenburns(c, 'rome', r, 60, f)
    flash(c, r)

def s_reveal(c, f, r): # pull back: the photo is on the phone in Hoody's hands. "THANKS FOR THE PHOTOS!"
    z = 1 + 1.2 * (1 - oe(r / 12))                                         # from the screen out to the whole picture
    c.save(); c.translate(400, 1480); c.scale(z, z); c.translate(-400, -1480)
    TP.rome_reveal(c, f)
    c.restore()
    if r < 12: Sh.topbar(c, 'ITS TRIP')

def s_more(c, f, r):   # "ONE MORE?" - his hopeful face; MY AI's facepalm; then the loop to the giant face
    P.rome(c, f, s=.62, cx=540, horizon=1230)
    K.hoodie(c, 420, 1080 + 150 * 2.3, 2.3 * 1.1)
    K.hoodyz_head(c, 420, 1080, 2.3, era='young', expr='hopeful', blink=False, op=.2 + .8 * talk(f, 'h_more_STANDIN'))
    R.bubble(c, ['ONE MORE?'], r - 1, (480, 1230), cy=600, cx=560, size=62)
    fp = r >= 16
    A.myai(c, 900, 1760, 1.1, eye='blank' if fp else 'happy', arms=('down', 'chest' if fp else 'down'), tilt=-12 if fp else 0)

DUR = [120, 30, 48, 60, 30, 81, 30, 69, 27, 45, 60, 156, 60]
FNS = [s_invite, s_title, s_open, s_pisa, s_photo('pisa', 30), s_paris, s_photo('paris', 30), s_giza, s_photo('giza', 27), s_rome_act, s_rome, s_after, s_another]
SHOTS = []; _t = 0
for fn, d in zip(FNS, DUR): SHOTS.append((fn, _t, _t + d)); _t += d
NF = _t
TRIP = range(1, 11)                                                       # the "memory": title card to the Rome photo
XF = 6                                                                    # crossfade frames between trip shots, photo-story style

def render_shot(i, f):
    fn, a, b = SHOTS[i]
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(S)
    c.save(); fn(c, f, f - a); c.restore(); return S

def draw(f):
    i = next(k for k, (fn, a, b) in enumerate(SHOTS) if a <= f < b)
    fn, a, b = SHOTS[i]; r = f - a
    S = render_shot(i, f); c = cairo.Context(S)
    if i in TRIP and i - 1 in TRIP and r < XF and fn is not s_open:                            # crossfade from the shot before
        prev = render_shot(i - 1, a - 1); c.set_source_surface(prev, 0, 0); c.paint_with_alpha(1 - (r + 1) / (XF + 1))
    label = 'ITS TRIP' if (fn is s_rome and r >= 14) or fn in (s_after, s_another) else 'HIS TRIP'
    Sh.topbar(c, label)
    if fn is s_rome and 14 <= r < 30: pulse(c, r - 14)
    if fn.__name__.endswith('_photo') or fn is s_rome:                    # the stamp thumps down at the shutter (drawn over the bar's level, unscaled)
        pass
    return S

def pulse(c, t):
    k = 1 + .25 * (1 - t / 16) ** 2                                       # swells in place, down a little: never over ME + MY AI or off the edge
    c.select_font_face('Lilita One'); c.set_font_size(58); w = max(200, c.text_extents('ITS TRIP').width + 96)
    px, iy = 1020 - w / 2, 222 + 69
    c.save(); c.translate(px - 6 * (k - 1), iy + 40 * (k - 1)); c.scale(k, k)
    rr(c, -w / 2, -44, w, 88, 44); fs(c, YEL, 7); txt(c, 'ITS TRIP', 0, 0, 58, INK, lw=0); c.restore()

if __name__ == '__main__':
    if sys.argv[1:2] == ['frames']:
        for f in map(int, sys.argv[2:]): draw(f).write_to_png(os.path.join(HERE, f'chk_{f:03d}.png'))
    else:
        CRF, PRESET = ('14', 'slow') if sys.argv[1:2] == ['final'] else ('18', 'veryfast')
        p = subprocess.Popen(f'ffmpeg -y -v error -f rawvideo -pix_fmt bgra -s {W}x{H} -r 30 -i - -vf format=yuv420p -c:v libx264 -crf {CRF} -preset {PRESET} -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 {os.path.join(HERE, "tmp_video.mp4")}'.split(), stdin=subprocess.PIPE)
        for f in range(NF): p.stdin.write(bytes(draw(f).get_data()))
        p.stdin.close(); assert p.wait() == 0; os.rename(os.path.join(HERE, 'tmp_video.mp4'), os.path.join(HERE, 'video.mp4')); print('video ok', NF)
