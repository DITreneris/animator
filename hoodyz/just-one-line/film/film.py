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
MUTE = bool(os.environ.get('MUTE'))                                     # cold mute test: no bubbles, no comic words
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
def hoody_prone(c, hip, expr, f=0, reach=None):
    """On his front, propped on his elbows, knees bent and feet up (in frame), chin up: he watches from the floor."""
    s = HS; F = FLOOR - 6
    for col, dx, ph in ((P.JEANS_FAR, -24, 1.3), (P.JEANS, 0, 0)):
        kn = (hip - 190 + dx, F - 36); ft = (hip - 150 + dx + 12 * math.sin(f * .25 + ph), F - 220)
        limb(c, [(hip, F - 70), kn, ft], 56 * s, col); c.save(); c.translate(*ft); c.rotate(-1.4); rr(c, -20 * s, -14 * s, 70 * s, 30 * s, 14 * s); fs(c, INK, 0); c.restore()
    neck = (hip + 280, F - 120)
    c.save(); c.translate(*neck); c.rotate(math.pi / 2); K.hoodie(c, 0, 0, s * 1.1); c.restore()
    P.hoody_arm(c, (neck[0] - 40, neck[1] - 30), (neck[0] + 120, F - 40), s, pref=P.DOWN, hand='ball')
    if reach: P.hoody_arm(c, (neck[0], neck[1] - 40), reach, s, pref=P.DOWN, hand='palm')     # reaching for his briefcase
    else: P.hoody_arm(c, (neck[0], neck[1] - 30), (neck[0] + 160, F - 40), s, pref=P.DOWN, hand='ball')
    head = (neck[0] + 70, neck[1] - 170)
    K.hoodyz_head(c, head[0], head[1], s, era='young', expr=expr, blink=False, gaze=14)
    FI.LAST['h'] = c.user_to_device(*head)
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
    for at, amp in ((2, 8), (40, 18), (66, 6)):
        if 0 <= t - at < 7: sh = amp * (1 - (t - at) / 7)
    zz = io((t - 41) / 3) * (1 - io((t - 54) / 3)); z = 1 + 1.2 * zz    # push in on the stamped card: APPROVED, big
    c.save(); c.translate(FI.noise(t, 7) * sh + zz * (540 - CARD_AT[0]), FI.noise(t, 8) * sh + zz * (900 - CARD_AT[1]))
    c.translate(*CARD_AT); c.scale(z, z); c.translate(-CARD_AT[0], -CARD_AT[1])
    P.room(c, door=door); P.desk(c); P.laptop(c, 47, tick=True)
    c.save(); c.translate(690, DESK_Y); P.mug(c, 0, 0, 1.0); c.restore()
    if not (26 <= t < 62): card_on_laptop(c, stamp=t >= 62)
    P.chair(c, 360, P.SEAT_Y)
    # HARV: in through the door, past Hoody, stops at the desk
    hx_ = lerp(165, HV_X, io((t - 3) / 20)); walk = (t - 3) * .55 if 3 <= t < 23 else None
    look = io((t - 22) / 4)                                             # turns to the laptop: the tick, only the tick
    if t < 34: rarm = (None, 'stamp')
    elif t < 40: rarm = ((CARD_AT[0] + 10, CARD_AT[1] - 200 * io((t - 34) / 4)), 'stamp')
    elif t < 46: rarm = ((CARD_AT[0] + 10, CARD_AT[1] - 30), 'stamp')    # THUNK
    else: rarm = (None, None)
    if t < 58: larm = (None, 'case')
    elif t < 70: u = io((t - 58) / 8); larm = ((lerp(hx_ - 100, 545, u), lerp(1300, 1110, u)), 'case' if t < 66 else None)
    else: larm = (None, None)
    hy, hands = harv_full(c, hx_, FLOOR, walk=walk, tilt=.1 * look, mouth='fond' if 46 <= t < 80 else 'flat', arms=(larm, rarm))
    if 22 <= t < 30:                                                    # the glint on his shades as he reads the tick
        u = (t - 22) / 8; FI.burst(c, hx_ + 60, hy - 20, 40 + 20 * u, 4, WHITE, 6)
    # Hoody on the floor by the door
    if t < 3:                                                            # where the fight left him, until the door hits him
        c.save(); c.translate(215, FLOOR - 10); P.hoody_seated(c, 0, 0, 'dizzy', legs=((170, -10), (300, 0))); c.restore()
    elif t < 8:                                                          # BAM: knocked forward onto his front
        u = io((t - 3) / 5); c.save(); c.translate(lerp(215, 240, u), FLOOR - 10); c.rotate(1.3 * u)
        P.hoody_seated(c, 0, 0, 'ouch', legs=((170, -10), (300, 0))); c.restore()
    else: hoody_prone(c, 240, 'dizzy' if t < 14 else 'shock', t, reach=(lerp(560, 545, io((t - 60) / 6)), lerp(1300, 1170, io((t - 60) / 6))) if t >= 60 else None)
    if 3 <= t < 7: FI.burst(c, 300, FLOOR - 330, 110, 10, WHITE, 10)
    # MY AI on the desk: types; holds the card out for the stamp; takes the briefcase
    x, gy = AIX_H, DESK_Y
    if t < 26: left = 'down'; card_hand = None
    elif t < 56:
        u = io((t - 26) / 6); tg = (lerp(TOP[0] - 120, CARD_AT[0], u), lerp(TOP[1] + 80, CARD_AT[1] + 40, u))
        left = P.ai_pose(-1, P.ai_local(x, gy, AS, tg), P.DOWN); card_hand = tg
    elif t < 62: left = P.ai_pose(-1, P.ai_local(x, gy, AS, (CARD_AT[0] + 20, CARD_AT[1] + 40)), P.DOWN); card_hand = None
    else:
        hd = hands[0] if t < 70 else (545, 1110)
        left = P.ai_pose(-1, P.ai_local(x, gy, AS, (max(hd[0], 530), hd[1])), P.DOWN); card_hand = None
    FI.myai_at(c, f=t + 300, x=x, gy=gy, left=left, eye='happy', look=(-14, 2) if 28 <= t < 70 else (18, 0), typing=False)   # hands off the keys: the label stays clear
    if card_hand:
        hxx, hyy = A.hand_at(x, gy, AS, -1, left); P.card(c, hxx - 10, hyy - 50, 1.0, rot=-.08, stamp=t >= 40)
    if 56 <= t < 62:                                                    # back onto the laptop, stamped
        u = (t - 56) / 6; P.card(c, lerp(CARD_AT[0], TOP[0], u), lerp(CARD_AT[1], TOP[1], u) - 120 * math.sin(math.pi * u), lerp(1.0, .55, u), rot=.06, stamp=True)
    if t >= 66:
        hxx, hyy = A.hand_at(x, gy, AS, -1, left); P.briefcase(c, hxx, hyy + 96 * .9, .9)
    if 40 <= t < 44: FI.burst(c, CARD_AT[0] + 10, CARD_AT[1] - 20, 90, 10, RED, 8)
    c.restore()
    return S, c

# ---------------- J and K: the takeover; the last frame mirrors frame 0 ----------------
def pot_at(c, hx_, hy, tilt=0.0):
    """The coffee pot hanging from his hand (handle at the hand); tilt < 0 pours to the left. Returns the spout."""
    c.save(); c.translate(hx_, hy); c.rotate(tilt); P.pot(c, -50 + 50, 90, 1.1); c.restore()
    sx, sy = -40, 40                                                    # the spout, in the pot's frame (top left of its body)
    return (hx_ + sx * math.cos(tilt) - sy * math.sin(tilt), hy + sx * math.sin(tilt) + sy * math.cos(tilt))

def shot_JK(t, k_shot):
    """J (55 f): Hoody steps in and pours coffee into MY AI's mug (it holds it out without looking), steps back; MY AI sips,
    swivels the chair, a thumbs-up. K (80 f): the card, the same framing as frame 0, the eye twitch, the eyes close."""
    S = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(S)
    P.room(c); P.desk(c); P.laptop(c, 47, tick=True); card_on_laptop(c, stamp=True)
    j = -1 if k_shot else t
    swiv = math.sin(math.pi * cl((j - 40) / 8)) if 40 <= j < 48 else 0.0
    P.chair(c, P.CHAIR_X, P.SEAT_Y, spin=swiv * 2.5)
    x = P.CHAIR_X + 10; gy = P.SEAT_Y - 18 + 60 * AS
    REST, OUT, SIP = (x - 150, 1105), (x + 225, 1095), (x - 135, 1010)
    L_ = lambda p, q, u: tuple(lerp(a_, b_, u) for a_, b_ in zip(p, q))
    # J: the mug is in its right hand, held out (without looking) for the pour, then to its face; at 40 the left hand takes it
    if k_shot: mugp = REST
    elif j < 6: mugp = L_((x + 80, 1150), OUT, io(j / 6))
    elif j < 28: mugp = OUT
    elif j < 34: mugp = L_(OUT, SIP, io((j - 28) / 6))
    elif j < 40: mugp = SIP
    else: mugp = L_(SIP, REST, io((j - 40) / 6))
    in_right = not k_shot and j < 40
    lhand = REST if (k_shot or j >= 40) else ((x - 150, 1150) if j < 34 else L_((x - 150, 1150), SIP, io((j - 34) / 6)))
    kt = t if k_shot else -1
    LAP_ = (x + 80, gy - 120); THUMB = (x + 40, gy - 370)
    if k_shot:
        if kt < 10: u = io(kt / 10); rt = (lerp(LAP_[0], P.K4_OFF[0] - 70, u), lerp(LAP_[1], P.K4_OFF[1] + 10, u))
        elif kt < 34: rt = (P.K4_OFF[0] - 70, P.K4_OFF[1] + 10)
        else: u = io((kt - 34) / 8); rt = (lerp(P.K4_OFF[0] - 70, LAP_[0], u), lerp(P.K4_OFF[1] + 10, LAP_[1], u))
    else:
        if j < 40: rt = mugp
        elif j < 44: rt = L_(SIP, LAP_, io((j - 40) / 4))
        elif j < 50: u = io((j - 44) / 4); rt = (lerp(LAP_[0], THUMB[0], u), lerp(LAP_[1], THUMB[1], u))
        else: u = io((j - 50) / 5); rt = (lerp(THUMB[0], LAP_[0], u), lerp(THUMB[1], LAP_[1], u))
    old = A.limb
    A.limb = lambda c_, pts, *a: None if pts in ([(-34, 205), (-34, 280)], [(34, 205), (34, 280)]) else old(c_, pts, *a)
    pr = P.ai_pose(1, P.ai_local(x, gy, AS, rt), P.UP if (not k_shot and j >= 44) else P.DOWN)
    try:
        A.myai(c, x + 10 * swiv, gy, AS, eye='happy' if not (k_shot and 6 <= t < 40) else 'open', look=(16, -4), tilt=-6, turn=.7 * swiv,
               arms=(P.ai_pose(-1, P.ai_local(x, gy, AS, mugp if not in_right else lhand), P.UP), pr))
    finally: A.limb = old
    FI.LAST['ai'] = (x, gy - 280 * AS)
    for q in (-1, 1):
        hip = (x + q * 34 * AS, gy - 75 * AS); kn = (x + q * 40 * AS, gy - 30 * AS); ft = (x + q * 46 * AS + 10 + 6 * math.sin(t * .3 + q), gy + 50 * AS)
        limb(c, [hip, kn, ft], 34 * AS, WHITE)
    P.mug(c, mugp[0] + 6, mugp[1] + 36, 1.1)
    if not k_shot and 46 <= j < 55:                                     # the thumbs-up
        tx, ty = A.hand_at(x, gy, AS, 1, pr); rr(c, tx - 20, ty - 96, 42, 80, 18); fs(c, WHITE, 8)
    P.briefcase(c, x + 170, FLOOR - 6, 1.25)
    # Hoody: steps in with the pot, pours, steps back to his place (the place he stands in the last frame)
    if k_shot: hxp = P.STAND_X
    elif j < 10: hxp = lerp(P.STAND_X, 620, io(j / 10))                  # a half step in; he never comes between it and the screen
    elif j < 36: hxp = 620
    elif j < 48: hxp = lerp(620, P.STAND_X, io((j - 36) / 12))
    else: hxp = P.STAND_X
    twitch = k_shot and t >= 40
    jig = 3 * math.sin(t * 5) if twitch and (t // 3) % 3 == 0 else 0
    bow = .6 + .03 * math.sin(t * .2) - (.15 * math.sin(math.pi * cl(j / 10)) if 0 <= j < 10 or 36 <= j < 48 else 0)
    hop = 10 * abs(math.sin(j * .9)) if (0 <= j < 10 or 36 <= j < 48) else 0
    c.save(); c.translate(jig, -hop)
    shL, shR, head = P.hoody_standing(c, hxp, FLOOR, 'beaten', bow=bow, gaze=-16, side=-1)
    c.restore()
    shL, shR, head = (shL[0] + jig, shL[1] - hop), (shR[0] + jig, shR[1] - hop), (head[0] + jig, head[1] - hop)
    FI.LAST['h'] = head
    if kt < 18: lt = (shL[0] - 30, shL[1] + 200)
    elif kt < 28: u = io((kt - 18) / 10); lt = (lerp(shL[0] - 30, P.K4_OFF[0] + 70, u), lerp(shL[1] + 200, P.K4_OFF[1] + 10, u))
    elif kt < 34: lt = (P.K4_OFF[0] + 70, P.K4_OFF[1] + 10)
    else: u = io((kt - 34) / 10); lt = (lerp(P.K4_OFF[0] + 70, P.K4_OFF[0] + 120, u), lerp(P.K4_OFF[1] + 10, P.K4_OFF[1] + 40, u))
    P.hoody_arm(c, shL, lt, HS, pref=P.DOWN, hand='grip')
    if k_shot:
        if kt < 34:
            hxx, hyy = A.hand_at(x, gy, AS, 1, pr); P.card(c, hxx + 70, hyy - 10, .9, rot=-.05)
        else: P.card(c, lt[0] - 70, lt[1] - 10, .9, rot=-.05)
    # the pot: hanging (K and the walk), lifted over the mug and tipped to pour (J 10-30)
    hang = (shR[0] - 50, shR[1] + 215)
    over = (OUT[0] + 70, OUT[1] - 215)
    pu = io((j - 9) / 4) * (1 - io((j - 30) / 5)) if not k_shot else 0
    ph = (lerp(hang[0], over[0], pu), lerp(hang[1], over[1], pu))
    P.hoody_arm(c, shR, ph, HS, pref=P.DOWN, hand='grip')
    tilt = -1.0 * io((j - 13) / 3) * (1 - io((j - 27) / 3)) if not k_shot else 0
    spout = pot_at(c, ph[0], ph[1] - 90 + 90, tilt)
    if in_right and j < 34: P.mug(c, mugp[0] + 6, mugp[1] + 36, 1.1)    # held out in front of him: drawn over his hoodie
    if not k_shot and 15 <= j < 28:                                     # the coffee, into the mug
        c.move_to(*spout); c.curve_to(spout[0] - 30, spout[1] + 20, mugp[0] + 20, mugp[1] - 60, mugp[0] + 6, mugp[1] - 30)
        c.set_source_rgb(*hx('5a3418')); c.set_line_width(12); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
    if twitch and (t // 3) % 3 == 0:                                    # the eye twitch
        ex, ey = head[0] - 30, head[1] - 20
        for a in (-.6, 0, .6):
            c.move_to(ex + 46 * math.cos(a + math.pi), ey + 46 * math.sin(a + math.pi)); c.line_to(ex + 70 * math.cos(a + math.pi), ey + 70 * math.sin(a + math.pi))
        c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
    if not k_shot and 32 <= j < 42:                                     # slurp
        txt(c, '~', mugp[0] + 40, mugp[1] - 90, 40, INK, lw=0)
    return S, c

# ---------------- the frame ----------------
def shot_at(fr):
    for n, d in SHOTS:
        if fr < START[n] + d: return n, fr - START[n]
LINES_VIS = []      # (name, text, start fr, end fr, who, centre)
OPEN = 4                                                               # the first 7 frames: his eyes open again (waking up)
SFX = [('BONK!', START['F'] + FI.BONK, START['F'] + FI.BONK + 14, 700, 560, -.12),
       ('WHAM!', START['F'] + FI.CONTACT + 4, START['F'] + FI.CONTACT + 14, 360, 1000, .1),
       ('CRASH!', START['F'] + FI.WALL + 4, START['F'] + FI.WALL + 20, 330, 610, -.1)]
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
    for name, text, a, b, who, cen in ([] if MUTE else BUBS):
        if a <= fr < b and who in FI.LAST:
            p = FI.LAST[who]
            tip = (p[0] + 130, p[1] + 70) if name == 'h_but' else tip_hoody(p) if who == 'h' else (tip_ai(p, AS) if who == 'ai' else (p[0] + 40, p[1] - 260))
            bubble(c, text, tip, *cen)
    for word, a, b, x_, y_, rot in ([] if MUTE else SFX):                                 # comic words on the three biggest hits (they work with the sound off)
        if a <= fr < b:
            k = 1 + .35 * (1 - oe((fr - a) / 4)); size = 120 * k
            c.save(); c.select_font_face('Lilita One'); c.set_font_size(size); w = c.text_extents(word).width; c.restore()
            txt(c, word, x_, y_, size, YEL, lw=14, st=INK, rot=rot)
            BOXES.append((word, x_ - w / 2 - 10, y_ - size / 2 - 10, x_ + w / 2 + 10, y_ + size / 2 + 10))
    P.topbar(c)
    if fr >= NF - BLINK: lids(c, io((fr - (NF - BLINK) + 1) / BLINK))   # closing: the last frame is fully shut
    elif fr < OPEN: lids(c, .5 * (1 - oe(fr / OPEN)))                  # opening (Tomas, 23 Nov): the film starts on his eyes opening
    return S

VO = json.load(open(os.path.join(HERE, 'lines.json')))
BUBS = []
_who = dict(h_line='h', h_one='h', h_but='h', ai_onit='ai', ai_almost='ai', ai_line='ai', harv_ok='harv')
_cen = dict(h_line=(380, 480), h_one=(330, 470), h_but=(640, 1440), ai_onit=(660, 470), ai_almost=(640, 470), harv_ok=(420, 470), ai_line=(440, 480))
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
