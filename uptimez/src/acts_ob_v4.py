"""v4, pinned. v4 (acts_ob_v3.py = v3, kept), 17 Nov:
  - plan_open(): what is on his drawing. The gear read as a settings icon, and the line did not explain it. It is now
    the plan of his ten garages: ten numbered bays in two rows, white on blue. "Ten garages. And I keep losing this."
    plan_strip() is the piece of it that lands in his palm (beat 10): a bay and its number. blueprint_open() (the gear)
    is kept for the older sheets.
  - Pam on the floor has hips: her body sat on her legs like a card on two sticks. A rounded seat joins the thighs, and
    the cardigan's hem hangs over it in a curve.
Added after the audit of 17 Nov (new acts, opt-in: everything older draws as before):
  PAM "floor" / "floor_up": she is ON the floor. The old "kneel" was her standing figure sunk into it. Now she sits on
    her knees, turned to Don: two thighs and two knees forward, the shins folded back along the floor, a white shoe
    behind her; her body leans forward; one hand is on one blue strip on the floor, clear of her knees (wall shows
    between arm, body and legs); the other holds what she has collected against her chest. "floor": her eyes on the
    strip. "floor_up": she looks up at Don, hopeful, a small smile: "I'll fix it. Did you notice?"
  DON "tug" / "tug_down": caught, he takes hold of the front edges of his vest and pulls it straight (two fists with
    thumbs, on the zip edges; "tug_down" is the pull). It replaces two fists on his stomach ("pro", kept).
THE ONBOARDING: the acting of Don, Pam and the Client, v3 (acts_ob_v2.py = v2, kept): the arms. They read as broken:
  - the elbow was above the line from shoulder to hand in every reach (Don's open hand, Pam's finger), a Z;
    now the elbow hangs: of the two ways an arm can reach a point, the one with the lower elbow is taken;
  - an arm was two outlined rectangles, with a corner and a line across it at the elbow; now it is one cut-out with a
    rounded elbow and a rounded shoulder (arm(), swapped in for kit.arm while Don or Pam is drawn: arms()). The
    Client's arms (client_ob.limb) and Sofia's (a sleeve to the elbow, a bare forearm) already were whole.
  - Pam's "lower": the upper arm stays at her side and the forearm folds up; the hand no longer crosses her chest.
THE ONBOARDING: the acting of Don, Pam and the Client, v2 (acts_ob_v1.py = v1, kept), after the acting audit:
hands with a wrist and fingers (hands_ob), and faces that follow the action.
  DON: "hand_out" is an open palm toward the Client; "holds" is pleased with himself (it was the same grin); in
    "set_down" and "away" the pupils go much further, and "away" tips his head; "pro" replaces "jealous": caught, he
    does not get angry, he gets 10 % more professional: brows up, a tight wide smile, both hands on his vest.
  PAM: the raised finger is a pointing hand; scatter() lays the strips down as a mess, overlapping.
  THE CLIENT: "hesitate" (he holds the roll back a moment: he cares about it), "watch" with his eyes down on it,
    "pocket" (his face stays with the room while his hand puts the strip away).
Below, the notes of v1, which hold except where the list above replaces them.
THE ONBOARDING: the acting of Don, Pam and the Client (v1), from script v1 and the grill of 17 Nov. No new costumes:
Don is his office self (don_v4: fleece vest, lanyard, the ketchup stain), Pam is as in The Best Candidate (pam_bc), the
Client is sheet v3 (client_ob). Nothing in those modules is changed: this file only poses them and adds the props.
DON: small and tight. "hand_out" (an open hand for the roll), "holds" (he has it), "set_down" (his eyes on Sofia,
  off right; his other hand stands the roll in what is beside him, without looking), "away" (caught staring: he looks
  away and a hand goes to his vest), "jealous" (two short brows; he keeps selling), "hand_up" (beat 08).
PAM: no lines. "typing" (before anyone has moved), "finger" (she lifts a finger to interrupt), "lower" (she looks at
  Don, and lowers it), "empty" (Sofia has taken the tablet), "kneel" (on her knees, a fist full of blue strips).
THE CLIENT: "give" (he hands the roll over; he does not leave it lying), "watch" (his silent signature),
  "palm" (the strip settles in it), and his existing "stand" for pocketing it.
The shredder stands on the floor beside Don, a slot in its top and a clear bin: it looks like somewhere you might
stand a roll. That is the accident."""
import math
import kit
import don_v4 as dv
import pam_bc as pb
import client_ob as co
import sofia_ob as so
import hands_ob as hd
from kit import INK, cut, rect, ellipse

BLUE = (0.16, 0.38, 0.80)
STRIP = (0.20, 0.42, 0.84)
LN = 48


def _ik(sx, sy, side, tx, ty):
    """Shoulder to hand. Of the two elbows that reach it, the lower one: an elbow hangs (side only breaks a tie)."""
    dx, dy = tx - sx, ty - sy
    d = min(math.hypot(dx, dy), 2 * LN - 0.2)
    base, a = math.degrees(math.atan2(dx, dy)), math.degrees(math.acos(d / (2 * LN)))
    both = [(base + sd * a, -sd * 2 * a) for sd in (side, -side)]
    drop = [math.cos(math.radians(u)) for u, _ in both]
    return both[0] if drop[0] >= drop[1] - 1e-6 else both[1]


def arm(k, sx, sy, a1, a2, col, skin, seed, ln=48, w=17):
    """kit.arm as one cut-out: no corner and no line at the elbow. Same arguments, same hand, same return."""
    d = lambda a: (math.sin(math.radians(a)), math.cos(math.radians(a)))
    d1, d2 = d(a1), d(a1 + a2)
    ex, ey = sx + d1[0] * ln, sy + d1[1] * ln
    hx, hy = ex + d2[0] * ln, ey + d2[1] * ln
    h = w / 2.0
    n1, n2 = (-d1[1], d1[0]), (-d2[1], d2[0])
    turn = d1[0] * d2[1] - d1[1] * d2[0]
    sg = 1 if turn >= 0 else -1                            # the side the arm bends toward: the inside of the elbow
    inner, outer = [], []
    if abs(a2) > 4:
        mx, my = n1[0] + n2[0], n1[1] + n2[1]
        m = math.hypot(mx, my) or 1.0
        cosh = max(0.45, m / 2.0)                          # cos of half the bend
        inner = [(ex + sg * mx / m * h / cosh, ey + sg * my / m * h / cosh)]
        b1, b2 = math.atan2(-sg * n1[1], -sg * n1[0]), math.atan2(-sg * n2[1], -sg * n2[0])
        dd = (b2 - b1 + math.pi) % (2 * math.pi) - math.pi
        outer = [(ex + h * math.cos(b1 + dd * i / 4.0), ey + h * math.sin(b1 + dd * i / 4.0)) for i in range(5)]
    b0 = math.atan2(sg * n1[1], sg * n1[0])                # the shoulder, rounded, from the inner side round the back
    back = math.atan2(-d1[1], -d1[0])
    dd = (back - b0 + math.pi) % (2 * math.pi) - math.pi
    cap = [(sx + h * math.cos(b0 + 2 * dd * i / 4.0), sy + h * math.sin(b0 + 2 * dd * i / 4.0)) for i in range(4, -1, -1)]
    pts = cap + inner + [(hx + sg * n2[0] * h, hy + sg * n2[1] * h), (hx - sg * n2[0] * h, hy - sg * n2[1] * h)] + outer[::-1]
    cut(k, pts, col, shadow=False, lw=2)
    ellipse(k, hx, hy, w * 0.6, w * 0.6, skin, seed, shadow=False, lw=2)
    return hx, hy


class arms:
    """with arms(): ...  every kit person drawn inside has whole arms."""
    def __enter__(self):
        self.old = kit.arm; kit.arm = arm
        return self

    def __exit__(self, *a):
        kit.arm = self.old


def _pose(h, left=None, right=None):
    """Arm angles for a kit person of height factor h; left/right are hand targets in the person's own coordinates."""
    sy = -300 * h + 78 + 14
    L = _ik(-40, sy, -1, *left) if left else (-8, 0)
    R = _ik(40, sy, 1, *right) if right else (8, 0)
    return tuple(L) + tuple(R)


def strips(k, x, y, s, n=7, seed=3, fan=1.0):
    r = k.rng(seed) if hasattr(k, "rng") else None
    c = k.c
    for i in range(n):
        a = (-0.9 + 1.8 * i / max(1, n - 1)) * fan + (0.12 if i % 2 else -0.10)
        c.save(); c.translate(x, y); c.rotate(a)
        rect(k, -3.2 * s, -34 * s, 6.4 * s, 34 * s, STRIP, seed + i, shadow=False, lw=1.2 * s)
        c.set_source_rgb(1, 1, 1); c.set_line_width(1.0 * s); c.move_to(0, -30 * s); c.line_to(0, -8 * s); c.stroke()
        c.restore()


def scatter(k, x0, x1, floor, s=1.0, n=14, seed=5):
    """Strips on the floor: lying down, at all angles, some across others."""
    c = k.c
    for i in range(n):
        u = ((i * 7919 + seed * 131) % 1000) / 1000.0
        v = ((i * 104729 + seed * 17) % 1000) / 1000.0
        c.save(); c.translate(x0 + (x1 - x0) * u, floor + (2 + 12 * v) * s); c.rotate((v - 0.5) * 1.5 + (0.9 if i % 5 == 0 else 0))
        rect(k, -15 * s, -2.6 * s, 30 * s, 5.2 * s, STRIP, seed + i, shadow=False, lw=1.1 * s)
        c.set_source_rgb(1, 1, 1); c.set_line_width(0.9 * s); c.move_to(-11 * s, 0); c.line_to(6 * s, 0); c.stroke()
        c.restore()


def blueprint_open(k, x, y, s=1.0, seed=60):
    """His drawing, open: one large gear and a few dimension lines, white on blue. The same gear is on his collar
    pin, and half of it is on the strip that lands in his palm."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    rect(k, -62, -42, 124, 84, BLUE, seed, lw=2.2)
    c.set_source_rgb(1, 1, 1); c.set_line_width(2.6); c.set_line_cap(1)
    c.arc(-8, 2, 20, 0, 2 * math.pi); c.stroke()
    c.arc(-8, 2, 6, 0, 2 * math.pi); c.stroke()
    for i in range(10):
        a = i * math.pi / 5
        c.move_to(-8 + 20 * math.cos(a), 2 + 20 * math.sin(a)); c.line_to(-8 + 28 * math.cos(a), 2 + 28 * math.sin(a)); c.stroke()
    c.set_line_width(1.4)
    c.move_to(30, -30); c.line_to(52, -30); c.move_to(30, -18); c.line_to(46, -18); c.move_to(-52, 34); c.line_to(40, 34); c.stroke()
    c.restore()


def _bays():
    """The ten bays of the plan, in the sheet's own coordinates: (number, x, y, w, h)."""
    return [(i + 1 + 5 * r, -52 + i * 21.25, (-35, 8)[r], 19, 26) for r in (0, 1) for i in range(5)]


def plan_open(k, x, y, s=1.0, seed=60):
    """His drawing, open: the plan of his ten garages. Two rows of five numbered bays, each open to the yard between
    them, white on blue."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    rect(k, -62, -42, 124, 84, BLUE, seed, lw=2.2)
    c.set_source_rgb(1, 1, 1); c.set_line_width(1.9); c.set_line_join(1)
    c.select_font_face("Inter", 0, 1); c.set_font_size(12.5)
    for n, bx, by, bw, bh in _bays():                                       # a bay is open to the yard
        if by < 0:
            c.move_to(bx, by + bh); c.line_to(bx, by); c.line_to(bx + bw, by); c.line_to(bx + bw, by + bh)
        else:
            c.move_to(bx, by); c.line_to(bx, by + bh); c.line_to(bx + bw, by + bh); c.line_to(bx + bw, by)
        c.stroke()
        t = str(n); e = c.text_extents(t)
        c.move_to(bx + bw / 2 - e.x_advance / 2 - e.x_bearing / 2, by + bh / 2 + 4.6); c.show_text(t)
    c.set_line_width(1.2); c.set_dash([5, 4]); c.move_to(-52, -0.5); c.line_to(52, -0.5); c.stroke(); c.set_dash([])   # the yard
    c.restore()


def plan_strip(k, x, y, s=1.0, n=7, ang=0.35, seed=66):
    """One strip of the plan: a bay's outline and its number, cut through. For his palm in beat 10."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    rect(k, -13, -62, 26, 124, STRIP, seed, lw=2)
    c.save(); c.rectangle(-12, -61, 24, 122); c.clip()
    c.set_source_rgb(1, 1, 1); c.set_line_width(3.2)
    c.rectangle(-30, -34, 52, 72); c.stroke()                               # the bay, most of it on other strips
    c.select_font_face("Inter", 0, 1); c.set_font_size(40)
    e = c.text_extents(str(n)); c.move_to(-e.x_advance / 2 - 3, 16); c.show_text(str(n))
    c.restore(); c.restore()


def shredder(k, x, floor, s=1.0, fill=0.0, seed=20):
    """A floor shredder: a slot in the top, a clear bin below. fill 0..1: blue strips in the bin."""
    c = k.c
    c.save(); c.translate(x, floor); c.scale(s, s)
    rect(k, -34, -112, 68, 112, (0.34, 0.36, 0.42), seed, lw=2.2)
    rect(k, -30, -64, 60, 58, (0.86, 0.92, 0.96), seed + 1, shadow=False, lw=1.6)          # the clear bin
    if fill > 0:
        c.save(); c.rectangle(-29, -63, 58, 56); c.clip()
        hgt = 50 * fill
        for i in range(int(26 * fill) + 3):
            xx = -27 + (i * 37 % 54); yy = -8 - (i * 23 % max(6, int(hgt)))
            c.save(); c.translate(xx, yy); c.rotate((i * 0.9) % 3.1)
            c.set_source_rgb(*STRIP); c.rectangle(-9, -1.8, 18, 3.6); c.fill()
            c.set_source_rgb(1, 1, 1); c.rectangle(-6, -0.4, 12, 0.8); c.fill()
            c.restore()
        c.restore()
    rect(k, -24, -108, 48, 9, (0.12, 0.12, 0.15), seed + 2, shadow=False, lw=1.4)          # the slot
    ellipse(k, 22, -84, 3.2, 3.2, (0.30, 0.74, 0.46), seed + 3, shadow=False, lw=1.0)
    c.restore()


def roll(k, x, y, s, ang, ln=150, seed=71):
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    co.blueprint_roll(k, 0, 0, ang, ln, 11.5, seed)
    c.restore()


def don(k, x, feet, s=1.0, act="stand", look=None, seed=500):
    H = kit.PEOPLE["DON"]["h"]
    sy = -300 * H + 92
    acts = {
        "stand": ((-8, 0, 8, 0), "neutral", (-1, 0)),
        "hand_out": (_pose(H, left=(-112, sy + 40)), "grin", (-1, -0.2)),
        "holds": (_pose(H, left=(-76, sy + 62)), "smug", (-1, -0.2)),
        "set_down": (_pose(H, left=(-66, sy + 86)), "neutral", (1.7, -0.2)),
        "away": (dv.POSE_CHEST, "neutral", (-1.7, -0.9)),
        "pro": (_pose(H, left=(-17, sy + 76), right=(17, sy + 76)), "neutral", (-1.2, 0.0)),
        "tug": (_pose(H, left=(-17, sy + 44), right=(17, sy + 44)), "neutral", (-1.2, 0.0)),
        "tug_down": (_pose(H, left=(-18, sy + 55), right=(18, sy + 55)), "neutral", (-1.2, 0.0)),
        "still": ((-8, 0, 8, 0), "neutral", (-0.3, 1.5)),   # he has seen it: the smile is gone, his eyes are down
        "hand_up": ((-10, 0, 168, 0), "grin", (1, 0.0)),
    }
    pose, face, lk = acts[act]
    kit.ARM_POSES["_ob"] = pose
    c = k.c
    tip = -0.09 if act == "away" else 0.0                  # caught: his head goes with his eyes
    if tip:
        c.save(); c.translate(x, feet); c.rotate(tip); c.translate(-x, -feet)
    try:
        with arms():
            o = dv.don(k, x, feet, s, "_ob", face, look=look or lk, seed=seed, chin=1 if act == "away" else 0)
    finally:
        del kit.ARM_POSES["_ob"]
        if tip:
            c.restore()
    skin = kit.PEOPLE["DON"]["skin"]
    hx, hy = o["hands"][0]
    if act == "hand_out":                                  # an open palm, toward the Client
        hd.palm(k, hx + 4 * s, hy + 1 * s, 1.25 * s, -math.pi / 2 - 0.10, skin, seed + 70)
    elif act in ("pro", "tug", "tug_down"):                # 10 % more professional: brows up, a tight wide smile
        ex, ey = o["head"]
        ellipse(k, ex, ey + 27 * s, 24 * s, 9 * s, skin, seed + 71, shadow=False, outline=False)
        c.set_source_rgb(*INK); c.set_line_width(3.4 * s); c.set_line_cap(1)
        c.move_to(ex - 19 * s, ey + 23 * s); c.curve_to(ex - 15 * s, ey + 28 * s, ex + 15 * s, ey + 28 * s, ex + 19 * s, ey + 23 * s)
        c.stroke()
        c.set_line_width(3.6 * s)
        for sx in (-1, 1):
            c.move_to(ex + sx * 12 * s, ey - 33 * s); c.line_to(ex + sx * 36 * s, ey - 35 * s); c.stroke()
    if act in ("tug", "tug_down"):                         # a fist on each front edge of the vest, thumbs outside
        for sd, (fx_, fy_) in zip((-1, 1), o["hands"]):
            c.save(); c.translate(fx_, fy_); c.scale(s, s)
            ellipse(k, -sd * 9.5, -3.5, 5.2, 8.0, skin, seed + 74 + sd, shadow=False, lw=1.8)      # the thumb, over the edge
            rect(k, -9.5, -8.5, 19, 17, skin, seed + 76 + sd, shadow=False, lw=2)
            c.set_source_rgb(*INK); c.set_line_width(1.3); c.set_line_cap(1)
            for yy in (-3.5, 0.8, 5.0):
                c.move_to(sd * 9.5, yy); c.line_to(sd * 2.5, yy); c.stroke()                       # the fingers, closed on it
            if act == "tug_down":
                c.set_line_width(1.8)
                for xx in (-5, 5):
                    c.move_to(xx, 13); c.line_to(xx, 20); c.stroke()                              # down
            c.restore()
    elif act in ("holds", "set_down"):
        if act == "set_down":                              # the lower end is already in the slot
            roll(k, hx, hy + 6 * s, s, 0.0, ln=96)
        else:
            roll(k, hx, hy - 6 * s, s, -0.25, ln=140)
        ellipse(k, hx, hy, 10.2 * s, 10.2 * s, kit.PEOPLE["DON"]["skin"], seed + 70, shadow=False, lw=2 * s)
    return o


def _band(k, a, b, w0, w1, col, lw=1.9):
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    nx, ny = -math.sin(ang), math.cos(ang)
    cut(k, [(a[0] + nx * w0 / 2, a[1] + ny * w0 / 2), (b[0] + nx * w1 / 2, b[1] + ny * w1 / 2),
            (b[0] - nx * w1 / 2, b[1] - ny * w1 / 2), (a[0] - nx * w0 / 2, a[1] - ny * w0 / 2)], col, shadow=False, lw=lw)


def pam_floor(k, x, floor, s=1.0, up=False, look=None, seed=40, pick=0.0):
    """Pam on her knees, turned to screen left. (x, floor) is the point on the floor under her hips.
    pick (opt-in, the animation): 0 = her hand is on the strip on the floor; 1 = she has lifted it, on its way to the
    others at her chest. Two cold viewers could not tell whether she had fallen or was picking them up."""
    import pam_xmas as px
    c = k.c
    H = kit.PEOPLE["PAM"]["h"]
    sy = -300 * H + 92
    lean, ox, oy = -33.0, 8.0, -60.0 - px.HEM              # her hips are over her knees, 60 above the floor
    T = px.TROUSERS
    c.save(); c.translate(x, floor); c.scale(s, s)
    ellipse(k, 56, -15, 8, 14, px.TRAINER, seed + 61, shadow=False, lw=1.8)                    # the far shoe, on its toe
    _band(k, (-6, -66), (-33, -12), 22, 19, T)                                                # the far thigh, the far knee
    ellipse(k, -33, -12, 10.5, 10.5, T, seed + 62, shadow=False, lw=1.9)
    _band(k, (-30, -8), (52, -8), 15, 13, T)                                                  # the far shin
    _band(k, (-10, -8), (68, -8), 16, 14, T)                                                  # the near shin, along the floor
    c.save(); c.translate(78, -14); c.rotate(0.22)
    ellipse(k, 0, 0, 9, 16, px.TRAINER, seed + 63, shadow=False, lw=2)
    c.set_source_rgb(0.55, 0.58, 0.64); c.set_line_width(1.6); c.move_to(5, -12); c.line_to(5, 12); c.stroke()   # its sole
    c.restore()
    _band(k, (10, -66), (-12, -13), 25, 21, T)                                                # the near thigh, upright
    ellipse(k, -12, -13, 11.5, 11.5, T, seed + 64, shadow=False, lw=1.9)                       # the near knee, on the floor
    c.set_source_rgb(*px.TROUSERS_DARK); c.set_line_width(1.6); c.move_to(6, -56); c.line_to(-9, -20); c.stroke()
    c.save(); c.translate(7, -59); c.rotate(-0.30)                                            # her seat: the thighs grow out of it
    ellipse(k, 0, 0, 21, 14.5, T, seed + 66, shadow=False, lw=1.9)
    c.restore()
    c.set_source_rgb(*T)                                                                      # no line where a thigh leaves it
    for hx_, kx_, w_ in ((10, -12, 21), (-6, -33, 18)):
        c.save(); c.translate(hx_, -66); c.rotate(math.atan2(-(kx_ - hx_), 53)); c.rectangle(-w_ / 2 + 1.2, -4, w_ - 2.4, 24); c.fill()
        c.restore()
    if pick <= 0:
        c.save(); c.translate(-160, -4); c.rotate(-0.08)                                      # the strip she has her hand on
        rect(k, -17, -3, 34, 6, STRIP, seed + 65, shadow=False, lw=1.2)
        c.set_source_rgb(1, 1, 1); c.set_line_width(1.0); c.move_to(-12, 0); c.line_to(6, 0); c.stroke()
        c.restore()
    c.restore()
    th = math.radians(lean)
    loc = lambda wx, wy: ((wx - ox) * math.cos(th) + (wy - oy) * math.sin(th), -(wx - ox) * math.sin(th) + (wy - oy) * math.cos(th))
    pose = _pose(H, left=loc(-157 + 44 * pick, -11 - 66 * pick), right=(14, sy + 60))
    old = px._legs
    px._legs = lambda *a, **kw: None                       # her legs are the ones above
    kit.ARM_POSES["_ob"] = pose
    try:
        with arms():
            pb.pam(k, x + ox * s, floor + oy * s, s, "_ob", "hopeful" if up else "neutral",
                   look=look or ((-0.9, -0.7) if up else (-0.8, 1.0)), seed=seed, lean=lean)
    finally:
        px._legs = old
        del kit.ARM_POSES["_ob"]
    import pam_mf as pm_                                    # the hem, hanging over her seat in a curve
    c.save(); c.translate(x + ox * s, floor + oy * s); c.rotate(th); c.scale(s, s)
    c.rectangle(-80, px.HEM - 0.6, 160, 40); c.clip()
    ellipse(k, 1.5, px.HEM - 1, 40.5, 12, pm_.PURPLE, seed + 67, shadow=False, lw=2)
    c.set_source_rgb(*pm_.PURPLE_DARK); c.set_line_width(1.5)
    c.save(); c.translate(1.5, px.HEM - 5); c.scale(36, 10); c.arc(0, 0, 1, 0.25, math.pi - 0.25); c.restore(); c.stroke()
    c.restore()
    d = lambda g: (math.sin(math.radians(g)), math.cos(math.radians(g)))
    hands = []
    for (sx_, u, f) in ((-40, pose[0], pose[1]), (40, pose[2], pose[3])):
        lx, ly = sx_ + (d(u)[0] + d(u + f)[0]) * LN, sy + (d(u)[1] + d(u + f)[1]) * LN
        hands.append((x + (ox + lx * math.cos(th) - ly * math.sin(th)) * s, floor + (oy + lx * math.sin(th) + ly * math.cos(th)) * s))
    if pick > 0:                                                                              # the one she has just lifted
        lx_, ly_ = hands[0]
        c.save(); c.translate(lx_, ly_); c.rotate(-0.9); c.scale(s, s)
        rect(k, -17, -3, 34, 6, STRIP, seed + 65, shadow=False, lw=1.2)
        c.restore()
        ellipse(k, lx_, ly_, 10 * s, 10 * s, kit.PEOPLE["PAM"]["skin"], seed + 85, shadow=False, lw=2 * s)
    rx, ry = hands[1]
    strips(k, rx - 2 * s, ry - 3 * s, s, n=6, seed=seed + 60, fan=0.5)                         # what she has collected
    ellipse(k, rx, ry, 10.5 * s, 10.5 * s, kit.PEOPLE["PAM"]["skin"], seed + 84, shadow=False, lw=2 * s)
    hx, hy = HEAD_OF(x, floor, s, ox, oy, th)
    return {"head": (hx, hy), "hands": hands}


def HEAD_OF(x, floor, s, ox, oy, th):
    import pam_mf as pm
    return (x + (ox - pm.HY * math.sin(th)) * s, floor + (oy + pm.HY * math.cos(th)) * s)


def pam(k, x, feet, s=1.0, act="stand", look=None, floor=None, seed=40):
    if act in ("floor", "floor_up"):
        return pam_floor(k, x, feet, s, act == "floor_up", look, seed)
    H = kit.PEOPLE["PAM"]["h"]
    sy = -300 * H + 92
    hold = (-20, sy + 62)
    acts = {
        "stand": ((-8, 0, 8, 0), (-0.6, 0.0)),
        "typing": (_pose(H, left=hold, right=(14, sy + 50)), (-0.2, 0.9)),
        "finger": (_pose(H, left=hold, right=(90, sy - 26)), (-0.9, 0.6)),
        "lower": (_pose(H, left=hold)[:2] + (15, 120), (-0.8, -0.1)),     # the arm at her side, the forearm folded up
        "empty": (_pose(H, left=(-22, sy + 60), right=(22, sy + 60)), (-0.2, 0.9)),
        "kneel": (_pose(H, left=(-74, sy + 70), right=(26, sy + 40)), (-0.7, 0.9)),
        "crouch": (_pose(H, left=(-70, sy + 84), right=(30, sy + 70)), (-0.7, 1.0)),   # on her way down to the strips
    }
    pose, lk = acts[act]
    c = k.c
    drop = 106 * s if act == "kneel" else 46 * s if act == "crouch" else 0
    if act in ("kneel", "crouch"):
        c.save(); c.rectangle(x - 400 * s, feet - 700 * s, 800 * s, 700 * s); c.clip()
    try:
        with arms():
            o = pb.pam(k, x, feet + drop, s, pose, "neutral", look=look or lk, seed=seed,
                       lean=-7.0 if act == "kneel" else -4.0 if act == "crouch" else 0.0)
    except Exception:
        kit.ARM_POSES["_ob"] = pose
        try:
            with arms():
                o = pb.pam(k, x, feet + drop, s, "_ob", "neutral", look=look or lk, seed=seed,
                           lean=-7.0 if act == "kneel" else 0.0)
        finally:
            del kit.ARM_POSES["_ob"]
    if act in ("kneel", "crouch"):
        c.restore()
    skin = kit.PEOPLE["PAM"]["skin"]
    (lx, ly), (rx, ry) = o["hands"]
    if act in ("typing", "finger", "lower"):               # her tablet, the form on it
        so.tablet(k, lx + 22 * s, ly - 12 * s, -0.08, "form", seed + 80) if s == 1.0 else _scaled(k, lx + 22 * s, ly - 12 * s, s, seed)
        ellipse(k, lx, ly, 10 * s, 10 * s, skin, seed + 81, shadow=False, lw=2 * s)
        if act == "typing":
            ellipse(k, rx, ry, 10 * s, 10 * s, skin, seed + 82, shadow=False, lw=2 * s)
    if act == "finger":                                    # a hand, one finger up
        hd.point(k, rx, ry, 1.22 * s, 0.10, skin, seed=seed + 83, wrist=False)
    if act == "kneel":                                     # a fist full of strips, and one more being picked up
        strips(k, rx, ry - 4 * s, s, n=7, seed=seed + 60, fan=0.55)
        ellipse(k, rx, ry, 10.5 * s, 10.5 * s, skin, seed + 84, shadow=False, lw=2 * s)
    return o


def _scaled(k, x, y, s, seed):
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    so.tablet(k, 0, 0, -0.08, "form", seed + 80)
    c.restore()


def client(k, x, feet, s=1.0, act="give", look=None, seed=900):
    hang = co.POSES["open"][:2]
    acts = {
        "hesitate": (hang + co._ik(1, 112, co.BT + 96), "puzzled", (0.9, 1.6)),
        "give": (hang + co._ik(1, 166, co.BT + 92), "confident", (0.8, 0.0)),
        "watch": (hang + co._ik(1, 52, co.BT + 74), "confident", (0.9, 2.2)),
        "palm": (hang + co._ik(1, 112, co.BT + 112), "puzzled", (0.9, 1.8)),
        "pocket": ("stand", "warm", (0.8, -0.1)),
    }
    pose, face, lk = acts[act]
    o = co.client(k, x, feet, s, pose, face, look=look or lk, seed=seed)
    c = k.c
    hx, hy = o["hands"][1]
    if act == "hesitate":                                  # still his: held close, upright
        roll(k, hx + 4 * s, hy - 26 * s, s, 0.22, ln=150)
        ellipse(k, hx, hy, co.HAND * s, co.HAND * s, co.SKIN, seed + 71, shadow=False, lw=2 * s)
    elif act == "give":                                    # the roll, held out
        roll(k, hx + 22 * s, hy - 2 * s, s, math.pi / 2 - 0.12, ln=150)
        ellipse(k, hx, hy, co.HAND * s, co.HAND * s, co.SKIN, seed + 71, shadow=False, lw=2 * s)
    elif act == "palm":                                    # one strip, settling
        c.save(); c.translate(hx + 2 * s, hy - 30 * s); c.rotate(0.5)
        rect(k, -5 * s, -24 * s, 10 * s, 48 * s, STRIP, seed + 72, lw=1.6 * s)
        c.set_source_rgb(1, 1, 1); c.set_line_width(1.6 * s); c.move_to(0, -18 * s); c.line_to(0, 6 * s); c.stroke()
        c.arc(0, 12 * s, 4 * s, 0, math.pi); c.stroke()
        c.restore()
    return o
