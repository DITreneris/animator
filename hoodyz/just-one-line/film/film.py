"""Just One Line: the film (integrated cut). One set, the fight from ../fight.py (v12) in the middle.
  A  0.0-0.5  frame 0: Hoody, smug, holds out the TASK card, "Just one line."; MY AI snatches it and flicks it onto the laptop
  F  0.5-8.2  the fight (six hits), the counter climbing 0 -> 32
  G  8.2-9.7  close-up: the laptop, 32 -> 47, a big tick
  H  9.7-12.3 HARV walks in past Hoody on the floor, looks only at the tick, stamps the card APPROVED, hands MY AI the briefcase
  J 12.3-14.2 the takeover: MY AI in Hoody's chair with his mug; Hoody bows with the coffee pot
  K 14.2-16.8 the same framing as frame 0, swapped: MY AI holds out the TASK card, "Just one line."; Hoody takes it; eye twitch
Usage: python3 film.py sheet [step] | final  (final -> video.mp4, no sound)."""
import os, sys, math, json, subprocess, cairo
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..'))
import fight as FI
import kp as P
from kp import K, A, INK, WHITE, NAVY, GREY, YEL, RED, rr, fs, ell, limb, txt, hx, lerp, W, H, FLOOR, HS, AS, LAP, DESK_Y
cl, oe, io = FI.cl, FI.oe, FI.io

SHOTS = [('A', 15), ('F', FI.NF), ('G', 45), ('H', 80), ('J', 55), ('K', 80)]
START = {}; _t = 0
for n, d in SHOTS: START[n] = _t; _t += d
NF = _t
TOP = (800, 900)                                                       # the TASK card, stuck on top of the laptop's screen
GREEN_T = hx('5df08a')
BOXES = []                                                             # every text box drawn, per frame (safe-zone gate)

# ---------------- the TASK card's timeline (one card; the last shot's card is the same drawing, unstamped) ----------------
def card_on_laptop(c, stamp=False):
    P.card(c, *TOP, .55, rot=.06, stamp=stamp)

def fly_card(c, fr):                                                   # f6: in MY AI's hand; f8-16: flicked onto the laptop
    if fr < 8: return
    u = cl((fr - 8) / 8); x = lerp(P.HAND_OFF[0] + 160, TOP[0], u); y = lerp(P.HAND_OFF[1] - 120, TOP[1], u) - 260 * math.sin(math.pi * u)
    if u < 1: P.card(c, x, y, lerp(.9, .55, u), rot=6.28 * u + .06)
    else: card_on_laptop(c)

# ---------------- bubbles (screen space, fitted and registered) ----------------
def bubble(c, text, tip, cx, cy, size=70):
    c.save(); c.select_font_face('Lilita One'); c.set_font_size(size); w = c.text_extents(text).width + 100; c.restore()
    h = size * 1.12 + 56
    cx = min(max(cx, 60 + w / 2 + 10), 960 - w / 2 - 10)
    P.bubble(c, [text], size, tip, cx, cy)
    BOXES.append((text, cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2))

def tip_hoody(p): return (p[0] + 30, p[1] - 200)                       # just above his hair, on the side facing the bubble
def tip_ai(p, s=1.0): return (p[0] - 40 * s, p[1] - 150 * s)            # above its head, beside the antenna

# ---------------- A: frame 0 ----------------
def shot_A(fr):
    S = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(S)
    c.translate(0, 1250 - 1250)                                        # the fight's wide camera (identity)
    P.room(c); P.desk(c); P.laptop(c, 0); c.save(); c.translate(690, DESK_Y); P.mug(c, 0, 0, 1.0); c.restore()
    P.chair(c, P.CHAIR_X, P.SEAT_Y)
    shL, shR, head = P.hoody_seated(c, P.CHAIR_X, P.SEAT_Y, 'smug')
    x, gy = P.STAND_X, FLOOR
    if fr < 6: tgt = (P.HAND_OFF[0] + 70, P.HAND_OFF[1] + 10)          # reaching for the card
    else: u = io((fr - 6) / 3); tgt = (lerp(P.HAND_OFF[0] + 70, P.HAND_OFF[0] + 160, u), lerp(P.HAND_OFF[1] + 10, P.HAND_OFF[1] - 120, u))   # the flick
    pl = P.ai_pose(-1, P.ai_local(x, gy, AS, tgt), P.DOWN)
    A.myai(c, x, gy, AS, eye='open' if fr < 5 else 'happy', look=(-16, -6) if fr < 5 else (18, 0), arms=(pl, 'down'))
    P.hoody_arm(c, shR, (P.HAND_OFF[0] - 70, P.HAND_OFF[1] + 10), HS, pref=P.DOWN, hand='grip')
    if fr < 6: P.card(c, *P.HAND_OFF, .9, rot=-.05)
    elif fr < 8: hxx, hyy = A.hand_at(x, gy, AS, -1, pl); P.card(c, hxx, hyy - 20, .9, rot=-.3)
    fly_card(c, fr)
    P.hoody_arm(c, shL, (shL[0] - 95, shL[1] - 190), HS, pref=P.LEFT, hand='point', ang=-math.pi / 2 - .15)
    FI.LAST['h'] = head; FI.LAST['ai'] = (x, gy - 280 * AS)
    return S, c

# ---------------- G: close-up of the laptop ----------------
def g_count(t): return 32 if t < 4 else min(47, 32 + int(15 * ((t - 4) / 18) ** .7))
def shot_G(t):
    tick = t >= 23
    def cam(c):
        k = lerp(1.0, 2.3, oe(t / 5)); ax, ay = lerp(420, 847, oe(t / 5)), lerp(1250, 1045, oe(t / 5))
        sx = lerp(420, 540, oe(t / 5)); sy = lerp(1250, 960, oe(t / 5))
        sh = 10 * (1 - (t - 23) / 6) if 23 <= t < 29 else 0
        c.translate(sx + FI.noise(t, 5) * sh, sy + FI.noise(t, 6) * sh); c.scale(k, k); c.translate(-ax, -ay)
    def over(c, g):
        if 23 <= t < 32:
            u = (t - 23) / 9; ell(c, LAP['x1'] - 40, LAP['y0'] + 40, 26 + 70 * u, 26 + 70 * u); c.set_source_rgba(.36, .94, .54, .6 * (1 - u)); c.set_line_width(8); c.stroke()
            FI.burst(c, (LAP['x0'] + LAP['x1']) / 2, LAP['y0'] + 172, 150 + 30 * u, 12, GREEN_T, 9)
    return FI.frame(FI.NF - 1 - (t % 2), cnt=g_count(t), tick=tick, cam=cam, extra=lambda c: card_on_laptop(c), overlay=over, bar=False)

# ---------------- H: HARV ----------------
def stamp_tool(c, x, y, s=1.0, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    rr(c, -14, -86, 28, 60, 10); fs(c, hx('8b5a2b'), 5); ell(c, 0, -92, 22, 16); fs(c, hx('8b5a2b'), 5)
    rr(c, -40, -30, 80, 30, 6); fs(c, GREY, 5); rr(c, -42, 0, 84, 14, 4); c.set_source_rgb(*hx('d0182a')); c.fill()
    c.restore()

HV_S, HV_LEG = 1.25, 330
def harv_full(c, x, gy, walk=None, tilt=0.0, mouth='flat', arms=((None, 'case'), (None, 'stamp'))):
    """HARV, standing (his Says Here head and body on a pair of long legs: the boss is taller than Hoody).
    arms: ((target, prop), (target, prop)) for his screen-left and screen-right hands; target None = hanging."""
    s = HV_S; hy = gy - HV_LEG * s - 220 * s
    for q, ph in ((-1, 0), (1, math.pi)):                              # legs
        sw = math.sin((walk or 0) + ph) * 40 * s if walk is not None else 0; lift = max(0, math.cos((walk or 0) + ph)) * 18 * s if walk is not None else 0
        limb(c, [(x + q * 34 * s, hy + 205 * s), (x + q * 34 * s + sw * .4, gy - HV_LEG * s * .5 - lift), (x + q * 34 * s + sw, gy - lift)], 36 * s, WHITE)
        rr(c, x + q * 34 * s + sw - 26 * s, gy - lift - 22 * s, 64 * s, 28 * s, 12 * s); fs(c, GREY, 5)
    hands = []
    for q, (tgt, prop) in zip((-1, 1), arms):
        sh = (x + q * 70 * s, hy + 110 * s)
        tg = tgt or (sh[0] + q * 30 * s, sh[1] + 150 * s + (8 * math.sin((walk or 0) + q) if walk is not None else 0))
        e, h = P.ik(sh, tg, 85 * s, 85 * s, P.DOWN)
        hands.append((sh, e, h, prop, tgt))
    for sh, e, h, prop, tgt in hands:                                  # hanging arms behind the body
        if tgt is None: _arm(c, sh, e, h, prop, s)
    c.save(); c.translate(x, hy); c.rotate(tilt); c.translate(-x, -hy)
    C_harv(c, x, hy, s, mouth)
    c.restore()
    for sh, e, h, prop, tgt in hands:                                  # reaching arms in front
        if tgt is not None: _arm(c, sh, e, h, prop, s)
    FI.LAST['harv'] = c.user_to_device(x, hy)
    return hy, [h for _, _, h, _, _ in hands]
def _arm(c, sh, e, h, prop, s):
    limb(c, [sh, e, h], 30 * s, WHITE); ell(c, *e, 11 * s, 11 * s); fs(c, GREY, 5)
    if prop == 'case': P.briefcase(c, h[0], h[1] + 96 * .9, .9)
    if prop == 'stamp': stamp_tool(c, h[0], h[1] + 10, .9)
    ell(c, h[0], h[1], 18 * s, 18 * s); fs(c, WHITE, 6)
def C_harv(c, x, y, s, mouth):
    P.C.harv(c, x, y, s, shade=True, mouth=mouth)

HV_X = 420; CARD_AT = (510, 1060); AIX_H = 612                     # MY AI moves along the desk for HARV                                       # where MY AI holds the card for the stamp
def shot_H(t):
    S = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(S)
    door = io(t / 4) * (1 - io((t - 26) / 6))
    sh = 0
    for at, amp in ((2, 8), (40, 18), (57, 6)):
        if 0 <= t - at < 7: sh = amp * (1 - (t - at) / 7)
    c.save(); c.translate(FI.noise(t, 7) * sh, FI.noise(t, 8) * sh)
    P.room(c, door=door); P.desk(c); P.laptop(c, 47, tick=True)
    c.save(); c.translate(690, DESK_Y); P.mug(c, 0, 0, 1.0); c.restore()
    if not (26 <= t < 50): card_on_laptop(c, stamp=t >= 50)
    P.chair(c, 360, P.SEAT_Y)
    # HARV: in through the door, past Hoody, stops at the desk
    hx_ = lerp(165, HV_X, io((t - 3) / 20)); walk = (t - 3) * .55 if 3 <= t < 23 else None
    look = io((t - 22) / 4)                                             # turns to the laptop: the tick, only the tick
    if t < 34: rarm = (None, 'stamp')
    elif t < 40: rarm = ((CARD_AT[0] + 10, CARD_AT[1] - 200 * io((t - 34) / 4)), 'stamp')
    elif t < 46: rarm = ((CARD_AT[0] + 10, CARD_AT[1] - 30), 'stamp')    # THUNK
    else: rarm = (None, None)
    if t < 48: larm = (None, 'case')
    elif t < 60: u = io((t - 48) / 8); larm = ((lerp(hx_ - 100, 545, u), lerp(1300, 1110, u)), 'case' if t < 56 else None)
    else: larm = (None, None)
    hy, hands = harv_full(c, hx_, FLOOR, walk=walk, tilt=.1 * look, mouth='fond' if 46 <= t < 70 else 'flat', arms=(larm, rarm))
    if 22 <= t < 30:                                                    # the glint on his shades as he reads the tick
        u = (t - 22) / 8; FI.burst(c, hx_ + 60, hy - 20, 40 + 20 * u, 4, WHITE, 6)
    # Hoody on the floor by the door
    c.save(); c.translate(150, FLOOR - 10)
    P.hoody_seated(c, 0, 0, 'dizzy' if t < 6 else 'shock', legs=((170, -10), (300, 0)))
    c.restore()
    # MY AI on the desk: types; holds the card out for the stamp; takes the briefcase
    x, gy = AIX_H, DESK_Y
    if t < 26: left = 'down'; card_hand = None
    elif t < 50:
        u = io((t - 26) / 6); tg = (lerp(TOP[0] - 120, CARD_AT[0], u), lerp(TOP[1] + 80, CARD_AT[1] + 40, u))
        left = P.ai_pose(-1, P.ai_local(x, gy, AS, tg), P.DOWN); card_hand = tg
    elif t < 56: left = P.ai_pose(-1, P.ai_local(x, gy, AS, (CARD_AT[0] + 20, CARD_AT[1] + 40)), P.DOWN); card_hand = None
    else:
        hd = hands[0] if t < 60 else (545, 1110)
        left = P.ai_pose(-1, P.ai_local(x, gy, AS, (max(hd[0], 530), hd[1])), P.DOWN); card_hand = None
    FI.myai_at(c, f=t + 300, x=x, gy=gy, left=left, eye='happy', look=(-14, 2) if 28 <= t < 70 else (18, 0), typing=False)   # hands off the keys: the label stays clear
    if card_hand:
        hxx, hyy = A.hand_at(x, gy, AS, -1, left); P.card(c, hxx - 10, hyy - 40, .7, rot=-.08, stamp=t >= 40)
    if 50 <= t < 56:                                                    # back onto the laptop, stamped
        u = (t - 50) / 6; P.card(c, lerp(CARD_AT[0], TOP[0], u), lerp(CARD_AT[1], TOP[1], u) - 120 * math.sin(math.pi * u), lerp(.7, .55, u), rot=.06, stamp=True)
    if t >= 56:
        hxx, hyy = A.hand_at(x, gy, AS, -1, left); P.briefcase(c, hxx, hyy + 96 * .9, .9)
    if 40 <= t < 44: FI.burst(c, CARD_AT[0] + 10, CARD_AT[1] - 20, 90, 10, RED, 8)
    c.restore()
    return S, c

# ---------------- J and K: the takeover; the last frame mirrors frame 0 ----------------
def shot_JK(t, k_shot):
    S = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(S)
    P.room(c); P.desk(c); P.laptop(c, 47, tick=True); card_on_laptop(c, stamp=True)
    P.chair(c, P.CHAIR_X, P.SEAT_Y)
    x = P.CHAIR_X + 10; gy = P.SEAT_Y - 18 + 60 * AS
    sip = (math.sin(t * .35) * .5 + .5) if not k_shot else max(0, 1 - t / 8)
    mugp = (x - 105 - 45 * (1 - sip), lerp(1105, 985, sip))           # lowered clear of its face when not sipping
    kt = t if k_shot else -1
    if kt < 0: rt = (x + 80, gy - 120)                                 # resting in its lap
    elif kt < 10: u = io(kt / 10); rt = (lerp(x + 80, P.K4_OFF[0] - 70, u), lerp(gy - 120, P.K4_OFF[1] + 10, u))
    elif kt < 34: rt = (P.K4_OFF[0] - 70, P.K4_OFF[1] + 10)
    else: u = io((kt - 34) / 8); rt = (lerp(P.K4_OFF[0] - 70, x + 80, u), lerp(P.K4_OFF[1] + 10, gy - 120, u))
    old = A.limb
    A.limb = lambda c_, pts, *a: None if pts in ([(-34, 205), (-34, 280)], [(34, 205), (34, 280)]) else old(c_, pts, *a)
    pr = P.ai_pose(1, P.ai_local(x, gy, AS, rt), P.DOWN)
    try:
        A.myai(c, x, gy, AS, eye='happy' if not (k_shot and 6 <= t < 40) else 'open', look=(16, -4), tilt=-6,
               arms=(P.ai_pose(-1, P.ai_local(x, gy, AS, mugp), P.UP), pr))
    finally: A.limb = old
    FI.LAST['ai'] = (x, gy - 280 * AS)
    for q in (-1, 1):
        hip = (x + q * 34 * AS, gy - 75 * AS); kn = (x + q * 40 * AS, gy - 30 * AS); ft = (x + q * 46 * AS + 10 + 6 * math.sin(t * .3 + q), gy + 50 * AS)
        limb(c, [hip, kn, ft], 34 * AS, WHITE)
    P.mug(c, mugp[0] + 6, mugp[1] + 36, 1.1)
    P.briefcase(c, x + 170, FLOOR - 6, 1.25)
    twitch = k_shot and t >= 40
    jig = 3 * math.sin(t * 5) if twitch and (t // 3) % 3 == 0 else 0
    bow = .6 + .03 * math.sin(t * .2)
    c.save(); c.translate(jig, 0)
    shL, shR, head = P.hoody_standing(c, P.STAND_X, FLOOR, 'beaten', bow=bow, gaze=-16, side=-1)
    c.restore()
    FI.LAST['h'] = (head[0] + jig, head[1])
    # his left hand: hanging (J), up to the card (K), takes it, draws it in
    if kt < 18: lt = (shL[0] - 30, shL[1] + 200)
    elif kt < 28: u = io((kt - 18) / 10); lt = (lerp(shL[0] - 30, P.K4_OFF[0] + 70, u), lerp(shL[1] + 200, P.K4_OFF[1] + 10, u))
    elif kt < 34: lt = (P.K4_OFF[0] + 70, P.K4_OFF[1] + 10)
    else: u = io((kt - 34) / 10); lt = (lerp(P.K4_OFF[0] + 70, P.K4_OFF[0] + 120, u), lerp(P.K4_OFF[1] + 10, P.K4_OFF[1] + 40, u))
    P.hoody_arm(c, shL, lt, HS, pref=P.DOWN, hand='grip')
    if k_shot:
        if kt < 34:
            hxx, hyy = A.hand_at(x, gy, AS, 1, pr); P.card(c, hxx + 70, hyy - 10, .9, rot=-.05)
        else: P.card(c, lt[0] - 70, lt[1] - 10, .9, rot=-.05)
    P.hoody_arm(c, shR, (shR[0] - 50, shR[1] + 215), HS, pref=P.RIGHT, hand='grip')
    P.pot(c, shR[0] - 50, shR[1] + 305, 1.1)
    if twitch and (t // 3) % 3 == 0:                                    # the eye twitch
        ex, ey = head[0] + jig - 30, head[1] - 20
        for a in (-.6, 0, .6):
            c.move_to(ex + 46 * math.cos(a + math.pi), ey + 46 * math.sin(a + math.pi)); c.line_to(ex + 70 * math.cos(a + math.pi), ey + 70 * math.sin(a + math.pi))
        c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
    if not k_shot and t % 18 < 6:                                       # slurp
        txt(c, '~', mugp[0] + 40, mugp[1] - 90, 40, INK, lw=0)
    return S, c

# ---------------- the frame ----------------
def shot_at(fr):
    for n, d in SHOTS:
        if fr < START[n] + d: return n, fr - START[n]
LINES_VIS = []      # (name, text, start fr, end fr, who, centre)
OPEN = 7                                                               # the first 7 frames: his eyes open again (waking up)
BLINK = 9                                                              # the last 9 frames: his eyes close; the loop cuts on the black
def night(fr):                                                         # the nightmare deepens from the first hit to the end
    a = START['F']; return io((fr - a) / (NF - BLINK - a)) if fr >= a else 0.0
def lids(c, k):
    """Eyelids closing over the whole frame (k 0..1), curved like an eye."""
    if k <= 0: return
    if k >= 1: c.rectangle(0, 0, W, H); c.set_source_rgb(.03, .02, .06); c.fill(); return
    o = (1 - k) * 1200; m = H / 2                                       # half the opening; an almond: widest in the middle
    for q in (-1, 1):                                                   # q -1: the upper lid, +1: the lower
        c.move_to(-20, m + q * .75 * o)
        c.curve_to(W * .3, m + q * 1.35 * o, W * .7, m + q * 1.35 * o, W + 20, m + q * .75 * o)
        c.line_to(W + 20, -20 if q < 0 else H + 20); c.line_to(-20, -20 if q < 0 else H + 20); c.close_path()
        c.set_source_rgb(.03, .02, .06); c.fill()
def draw(fr):
    BOXES.clear(); FI.LAST.clear(); P.NIGHT = night(fr)
    n, t = shot_at(fr)
    if n == 'A': S, c = shot_A(t)
    elif n == 'F':
        S = FI.frame(t, tick=False, bar=False, extra=lambda c: fly_card(c, fr)); c = cairo.Context(S)
    elif n == 'G': S = shot_G(t); c = cairo.Context(S)
    elif n == 'H': S, c = shot_H(t)
    else: S, c = shot_JK(t, n == 'K')
    c = cairo.Context(S)
    for name, text, a, b, who, cen in BUBS:
        if a <= fr < b and who in FI.LAST:
            p = FI.LAST[who]
            tip = tip_hoody(p) if who == 'h' else (tip_ai(p, AS) if who == 'ai' else (p[0] + 40, p[1] - 260))
            bubble(c, text, tip, *cen)
    P.topbar(c)
    if fr >= NF - BLINK: lids(c, io((fr - (NF - BLINK) + 1) / BLINK))   # closing: the last frame is fully shut
    elif fr < OPEN: lids(c, .85 * (1 - oe(fr / OPEN)))                  # opening (Tomas, 23 Nov): the film starts on his eyes opening
    return S

VO = json.load(open(os.path.join(HERE, 'lines.json')))
BUBS = []
_who = dict(h_line='h', h_one='h', h_but='h', ai_onit='ai', ai_almost='ai', ai_line='ai', harv_ok='harv')
_cen = dict(h_line=(380, 480), h_one=(330, 470), h_but=(380, 650), ai_onit=(660, 470), ai_almost=(640, 470), harv_ok=(420, 470), ai_line=(440, 480))
for L in VO:
    a = round(L['start'] * 30); b = max(a + 26, round((L['start'] + L['dur']) * 30) + 10)
    if L['name'] == 'h_line': a, b = 0, 31
    if L['name'] == 'h_one': b = min(b, 112)                           # gone before the hoodie goes over his head
    sh = shot_at(a)[0]; b = min(b, START[sh] + dict(SHOTS)[sh])        # a bubble never crosses a cut
    BUBS.append((L['name'], L['text'].upper().replace("BUT THAT'S MY", "BUT… THAT'S MY…"), a, b, _who[L['name']], _cen[L['name']]))

if __name__ == '__main__':
    os.chdir(HERE); mode = (sys.argv[1:] or ['sheet'])[0]
    if mode == 'final':
        p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}', '-r', '30', '-i', '-',
                              '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', '-pix_fmt', 'yuv420p',
                              '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv', 'video.mp4'], stdin=subprocess.PIPE)
        allb = []
        for f in range(NF):
            p.stdin.write(bytes(draw(f).get_data())); allb += [(f,) + b for b in BOXES]
        p.stdin.close(); p.wait()
        bad = [b for b in allb if b[2] < 60 or b[4] > 960 or b[3] < 375 or b[5] > 1600]
        json.dump(allb, open('boxes.json', 'w')); print('video.mp4', NF, 'boxes', len(allb), 'outside', len(bad), bad[:5])
        if bad: sys.exit(1)
    else:
        step = int(sys.argv[2]) if len(sys.argv) > 2 else 6
        fs_ = list(range(0, NF, step)); cols = 12; tw, th = 180, 320
        out = cairo.ImageSurface(cairo.FORMAT_RGB24, cols * tw, ((len(fs_) + cols - 1) // cols) * th); c = cairo.Context(out)
        c.set_source_rgb(1, 1, 1); c.paint()
        for i, f in enumerate(fs_):
            c.save(); c.translate((i % cols) * tw, (i // cols) * th); c.scale(tw / W, th / H); c.set_source_surface(draw(f)); c.paint(); c.restore()
            txt(c, f'{f}', (i % cols) * tw + 26, (i // cols) * th + 16, 18, INK, lw=0)
        out.write_to_png('film_sheet.png'); print('film_sheet.png', NF, NF / 30)
