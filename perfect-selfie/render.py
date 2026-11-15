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
VO = [('h_invite', 0, .3, .8), ('ai_plan', 0, 2.75, .7), ('h_selfie', 1, .1, .8), ('h_proud', 2, .35, .6), ('ai_stepback', 4, .25, .7),
      ('h_huh', 4, 1.25, .6), ('ai_more', 6, .2, .7), ('h_whoa', 6, .75, .6), ('h_effort', 6, 1.35, .5),
      ('h_howtrip', 10, .3, .8), ('ai_thanks', 10, 3.0, .7), ('h_sigh', 10, 4.1, .55), ('h_another', 11, .35, .8)]   # Hoody: Tomas's takes
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

def s_invite(c, f, r):  # before: "Do you want to go on a trip?" - she nods - MY AI pops up from behind the bench
    pop = oe((r - 76) / 8)
    bench_scene_back(c, f)
    if pop > 0: A.myai(c, 540, BS + 330 - 470 * pop, 1.1, eye='focus' if r > 86 else 'wide', arms=('up', 'up') if r < 90 else ('down', 'wave'), talk=talk(f, 'ai_plan'))
    bench_front(c)
    R.hoody(c, 330, BS, 1.0, expr='hopeful', pose='sit', seat=(BX0, BX1), arms=('rest', 'rest'), op=.2 + .8 * talk(f, 'h_invite'), gaze=20, f=f)
    nod = math.sin(cl((r - 62) / 12) * math.pi * 2) * .08 if 62 <= r < 74 else 0
    eva_seated(c, 760, 1.0, 'charmed' if r >= 62 else 'evacalm', tilt=nod, blink=K.blinking(f, 7))
    if r < 78: R.bubble(c, ['DO YOU WANT TO', 'GO ON A TRIP?'], r - 4, (360, 1000), cy=560, cx=430, size=58)
    if r >= 80: R.bubble(c, ["I'LL PLAN", 'EVERYTHING!'], r - 80, (540, BS + 330 - 470 * pop - 420 * 1.1), cy=560, cx=560, size=58)
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
        rr(c, px - 10, py - 10, pw + 20, ph + 20, 30); fs(c, hx('1d2130'), 6)
        if turn > .3:
            c.save(); rr(c, px, py, pw, ph, 22); c.clip(); c.translate(px, py); c.scale(pw / W, ph / H); c.set_source_surface(_PHOTO, 0, 0); c.paint(); c.restore()
        ell(c, px + pw + 6, py + ph * .6, 26, 30); fs(c, E.SKIN_E, 5)
    if r < 88: R.bubble(c, ['HOW DID YOU LIKE', 'OUR TRIP?'], r - 4, (330, 1000), cy=560, cx=430, size=56)
    if r >= 90: R.bubble(c, ['THANKS FOR', 'THE PHOTOS!'], r - 90, (880, BS - 6 - 420), cy=600, cx=700, size=56)
def s_another(c, f, r): # "...Another trip?" - quietly, not giving up. Loops into the invitation
    R.park(c, f, zoom=1.6, cy=1300)
    K.hoodie(c, 500, 1040 + 150 * 2.4, 2.4 * 1.1)
    K.hoodyz_head(c, 500, 1040, 2.4, era='young', expr='hopeful', blink=False, gaze=18, op=.15 + .7 * talk(f, 'h_another'))
    R.bubble(c, ['...ANOTHER TRIP?'], r - 8, (560, 1230), cy=620, cx=600, size=60)

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
    K.hoodie(c, 540, 1060 + 150 * 3.0, 3.0 * 1.1)
    K.hoodyz_head(c, 540, 1060, 3.0, era='young', expr='happy', blink=False, op=.2 + .8 * talk(f, 'h_selfie'))
    phone_ui(c)
    R.bubble(c, ['ONE SELFIE?'], r + 5, (600, 1250), cy=620, cx=760, size=62)
def phone_ui(c):
    """The camera preview: dark rounded corners and a shutter dot."""
    c.rectangle(0, 0, W, H); rr(c, 40, 40, W - 80, H - 80, 70); c.set_fill_rule(cairo.FILL_RULE_EVEN_ODD); c.set_source_rgb(*hx('1d2130')); c.fill()
    c.set_fill_rule(cairo.FILL_RULE_WINDING)
    ell(c, 540, 1800, 52, 52); fs(c, WHITE, 8)

def s_pisa(c, f, r):   # live: Hoody does the pose proudly; MY AI's arm telescopes up and props the very top
    P.pisa(c, f)
    k = oe((r - 16) / 26)
    sh = (330 + 72 * .85, 1600 - 280 * .85 + 112 * .85)
    tgt = (edge_pisa(470, -1) + 10, 470)
    A.myai(c, 330, 1600, .85, eye='focus' if k < 1 else 'happy', arms=('hip', None if k > 0 else 'down'), tilt=8)
    if k > 0: tele_arm(c, 330, 1600, .85, 1, (lerp(sh[0] + 40, tgt[0], k), lerp(sh[1] - 60, tgt[1], k)), tip='palm')
    E.eva(c, 150, 1880, .92, 'bored', sip=.5, gaze=-14, blink=K.blinking(f, 7))
    a = oe(r / 10)
    R.hoody(c, 860, 1830, 1.05, expr='happy', arms=('out' if a > .5 else 'rest', 'rest'), rot=-.06 * a, f=f)
    backpack_cat(c, 210, 1720, .9, 'suspicious')
def s_photo(place):
    def shot(c, f, r):
        getattr(TP, place)(c, f)
        flash(c, r)
    shot.__name__ = f's_{place}_photo'; return shot

def s_paris(c, f, r):  # live: "STEP BACK!" - Hoody backs away and shrinks into an extra; MY AI steps in, finger to the spire
    rx, rgy, rs, hz = 900, 1760, 1.25, 1640
    tipxy = (500, 760); s = ((hz - 10) - tipxy[1]) / 1370
    P.paris(c, f, s=s, cx0=tipxy[0], horizon=hz)
    w = ss(cl((r - 14) / 42))                                              # he walks back, slowly, looking back at the robot
    hx_, hgy, hs = lerp(520, 200, w), lerp(1880, hz + 40, w), lerp(1.0, .5, w)
    hx_ = lerp(640, 200, w)
    him = lambda: R.hoody(c, hx_, hgy + math.sin(r * .9) * 10 * (0 < w < 1) * hs, hs, expr='hopeful' if w < .6 else 'bored', arms=('rest', 'rest'), gaze=24 * w, f=f)
    if w >= .5: him()                                                      # once he's far back, Eva is in front of him
    E.eva(c, 400, 1900, .9, 'impressed' if r > 50 else 'evacalm', sip=.2, gaze=18 if r > 46 else -6, blink=K.blinking(f, 7))
    if w < .5: him()
    k = oe((r - 50) / 18)
    A.myai(c, rx, rgy, rs, eye='focus', arms=(None if k > 0 else 'wave', 'down'), tilt=-4, talk=talk(f, 'ai_stepback'))
    if k > 0:
        sh = (rx - 72 * rs, rgy - 280 * rs + 112 * rs)
        tele_arm(c, rx, rgy, rs, -1, (lerp(sh[0] - 40, tipxy[0], k), lerp(sh[1] - 60, tipxy[1] + 26, k)), tip='finger')
    backpack_cat(c, 210, 1720, .9, 'shocked' if r > 30 else 'suspicious')
    R.bubble(c, ['STEP BACK!'], r - 4, (rx, rgy - 420 * rs), cy=560, cx=720)

def s_giza(c, f, r):   # live: "MORE!" - the camel drags Hoody back to the luggage; MY AI takes Eva's hand
    P.egypt(c, f, s=.72, cx0=600, horizon=1460)
    rope_to = camel(c, 150, 1500, .42, f, pull=20)
    for (x, y, w_, h, col, a) in ((250, 1530, 110, 80, '3f7fd6', 0), (262, 1450, 84, 62, 'e8b23a', .25), (330, 1530, 70, 110, '5aa84f', 0)):
        c.save(); c.translate(x, y); c.rotate(a); suitcase(c, 0, 0, w_, h, col); c.restore()
    if r < 18:                                                             # "MORE!": MY AI hands him the bags first
        bx = lerp(820, 600, oe(r / 12)); suitcase(c, bx, 1640, 110, 80, 'e85a4f')
    d = ss(cl((r - 22) / 24))                                              # then the camel yanks him back
    hands, _ = R.hoody(c, lerp(560, 400, d), lerp(1860, 1530, d), lerp(.95, .52, d), expr='shock' if d < .9 else 'wince', arms=('out', 'down'), rot=.3 * d, f=f)
    if d > .05: c.move_to(*hands[0]); c.line_to(*rope_to); c.set_source_rgb(*hx('8a5a2e')); c.set_line_width(5); c.stroke()
    if d > .9: Sh.sweat(c, 450, 1260, .7)
    m = oe((r - 34) / 18)
    rx = lerp(900 if r < 18 else 960, 700, m)
    A.myai(c, rx, 1860, 1.3, eye='focus' if r < 30 else 'happy', arms=('wave', 'hold' if m > .9 else 'down'), tilt=10 * m, talk=talk(f, 'ai_more'))
    hp = A.hand_at(rx, 1860, 1.3, 1, 'hold')
    E.eva(c, 900, 1880, 1.0, 'laugh' if m > .9 else 'impressed', sip=.1, tilt=-.2 * m, pose='holdlow' if m > .9 else 'coffee', hand_to=hp if m > .9 else None)
    backpack_cat(c, 210, 1720, .9, 'disapproving')
    R.bubble(c, ['MORE!'], r - 2, (rx, 1860 - 420 * 1.3), cy=600, cx=720)

def s_rome(c, f, r):   # the couple photo; the label switches after it lands
    TP.rome(c, f, label='ITS TRIP' if r >= 14 else 'HIS TRIP')
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

DUR = [120, 48, 60, 30, 81, 30, 69, 27, 45, 60, 156, 60]
FNS = [s_invite, s_open, s_pisa, s_photo('pisa'), s_paris, s_photo('paris'), s_giza, s_photo('giza'), s_rome_act, s_rome, s_after, s_another]
SHOTS = []; _t = 0
for fn, d in zip(FNS, DUR): SHOTS.append((fn, _t, _t + d)); _t += d
NF = _t
LIVE_LABEL = {s_pisa, s_paris, s_giza, s_rome_act, s_invite}                                     # live shots carry the series bar; photos draw their own

def draw(f):
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(S)
    for fn, a, b in SHOTS:
        if a <= f < b:
            c.save(); fn(c, f, f - a); c.restore(); c.identity_matrix()
            if fn in LIVE_LABEL or fn is s_open: Sh.topbar(c, 'HIS TRIP')
            if fn in (s_after, s_another): Sh.topbar(c, 'ITS TRIP')
            if fn is s_rome and 14 <= f - a < 30: pulse(c, f - a - 14)
            break
    return S

def pulse(c, t):
    k = 1 + .75 * (1 - t / 16) ** 2
    c.select_font_face('Lilita One'); c.set_font_size(58); w = max(200, c.text_extents('ITS TRIP').width + 96)
    px, iy = 1020 - w / 2, 222 + 69
    c.save(); c.translate(px - 40 * (k - 1), iy + 60 * (k - 1)); c.scale(k, k)
    rr(c, -w / 2, -44, w, 88, 44); fs(c, YEL, 7); txt(c, 'ITS TRIP', 0, 0, 58, INK, lw=0); c.restore()

if __name__ == '__main__':
    if sys.argv[1:2] == ['frames']:
        for f in map(int, sys.argv[2:]): draw(f).write_to_png(os.path.join(HERE, f'chk_{f:03d}.png'))
    else:
        CRF, PRESET = ('14', 'slow') if sys.argv[1:2] == ['final'] else ('18', 'veryfast')
        p = subprocess.Popen(f'ffmpeg -y -v error -f rawvideo -pix_fmt bgra -s {W}x{H} -r 30 -i - -vf format=yuv420p -c:v libx264 -crf {CRF} -preset {PRESET} -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 {os.path.join(HERE, "tmp_video.mp4")}'.split(), stdin=subprocess.PIPE)
        for f in range(NF): p.stdin.write(bytes(draw(f).get_data()))
        p.stdin.close(); assert p.wait() == 0; os.rename(os.path.join(HERE, 'tmp_video.mp4'), os.path.join(HERE, 'video.mp4')); print('video ok', NF)
