"""ONE STAR v14 (25 Nov, Tomas: "the first joke physical; I miss action"): four physical beats, in the motion.
  1.1   the opening gag (cs_scene1_v14): the buzz throws Don's phone off the robot's head into its claw, ★ 1/5
  1.4   Don presses without looking: he grabs the robot's antenna first (it twangs), then the visor: "Approved."
  3.1   the sheet shoots out faster than his hand; he closes his fist on air; it runs off over the floor
  3.1b  (new insert) the roll's end trundles over the floor and bumps the glass door
  3.5   the Client screws the plan into a ball in his fist, "Is this a joke?", and throws it
  3.5b  PLOK on Don's forehead: his head knocked back, the ball drops, he freezes, one eye twitching
install() after cs_film_v13.setup(); the robot keeps Don's phone in its claw through 1.4."""
import math
import cs_scene1_v14 as v14
import cs_v14_gags as g
import cs_scene1 as s1
import cs_scene3 as s3
import cs_hands as ch
import hands_ps as hp
import kit
from cs_scene1 import S, at, base, sb, cp, ellipse, INK
from cs_board import impact, X

DPS = 12


def _t():
    return s1.CUR_D[0] / float(DPS)


def _ease(u):
    return s1.ease(u)


def _lerp(a, b, u):
    return (a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u)


# ---- 1.4: the antenna, then the visor --------------------------------------------------------------------------------

STEP = g.STEP
SH14 = (s1.DON_SH[0] - STEP, s1.DON_SH[1])
REST14 = (s1.DON_REST[0] - STEP, s1.DON_REST[1])
GO_A = (1.80, 2.10)                                        # out to the antenna (s): he isn't looking
HOLD_A = (2.10, 2.40)                                      # he has it: it bends and twangs
GO_V = (2.40, 2.80)                                        # over onto the visor: lands on "Approved." (2.818)
BACK = s1.LINE_D[1] + 0.15                                 # then the arm goes home (0.4 s)
GEO14 = {}
ARM14 = ["paddle"]                                         # v15 (bubbles): "none", the phone held low
ELBOW14 = [1]                                              # v17: -1 lifts the elbow out of his body's outline at the visor
DOOR31b = [False]                                          # v17: the handle, rail, glints and PUSH sticker (cs_v17)
LEAN14 = [0.0]                                             # v17: how far he leans in for the visor (0: v14; cs_v17 sets it)


def _lean14(t):
    """0..1: in with the reach to the visor, out with the arm going home."""
    if t < GO_V[0]:
        return 0.0
    if t < BACK:
        return _ease((t - GO_V[0]) / (GO_V[1] - GO_V[0]))
    return 1 - _ease((t - BACK) / 0.4)


def _geo14():
    if not GEO14:
        def probe(k_, o):
            GEO14["s"] = o["robot"]["screen"]
        s1.draw(lambda k_, d: S(k_, s1.TWO14_IN, auto=False, extra=probe,
                                **base(cl=False, sf=False, pm=False, mm=False, door=0.0, rb=at("robot", arm=ARM14[0]))), 0)
        sx, sy = GEO14["s"]
        rr = 50 * sb.SC["robot"]
        GEO14["A"] = (sx + 0.34 * rr, sy - 1.40 * rr)
        GEO14["V"] = (sx + 0.92 * rr, sy + 0.02 * rr)
    return GEO14


def _arm14(t):
    """(target, state): state rest / reach / antenna / visor / press."""
    G = _geo14()
    if t < GO_A[0]:
        return REST14, "rest"
    if t < GO_A[1]:
        u = _ease((t - GO_A[0]) / (GO_A[1] - GO_A[0]))
        p = _lerp(REST14, G["A"], u)
        return (p[0], p[1] - 8 * math.sin(math.pi * u)), "reach"
    if t < HOLD_A[1]:
        return G["A"], "antenna"
    if t < GO_V[1]:
        u = _ease((t - GO_V[0]) / (GO_V[1] - GO_V[0]))
        p = _lerp(G["A"], G["V"], u)
        return (p[0] + 6 * math.sin(math.pi * u), p[1]), "reach"
    if t < BACK:
        press = s1.LINE_D[0] <= t <= s1.LINE_D[0] + 0.25
        return (G["V"][0] - (2.0 if press else 0.0), G["V"][1]), "visor"
    u = _ease((t - BACK) / 0.4)
    return _lerp(G["V"], REST14, u), ("reach" if u < 1 else "rest")


def _alerp(A, B, u):
    return tuple(a + (((b - a + 180) % 360) - 180) * u for a, b in zip(A, B))


def angles14(t):
    """v17 ((a1, a2), lean): with ELBOW14 -1 the elbow is up and out of his body's outline from the antenna to the
    visor; the swings from and back to rest blend the joint angles (an IK flip there jumped)."""
    from cand_bc import ik
    ln_ = LEAN14[0] * _lean14(t)
    sx, sy = SH14[0] - ln_, SH14[1]
    tgt, _ = _arm14(t)
    up = ELBOW14[0]
    if up == 1 or t < GO_A[0] or t >= BACK + 0.4:
        return ik(sx, sy, tgt[0], tgt[1], g.LN, g.LN, 1), ln_
    G = _geo14()
    if t < GO_A[1]:
        u = _ease((t - GO_A[0]) / (GO_A[1] - GO_A[0]))
        return _alerp(ik(sx, sy, REST14[0], REST14[1], g.LN, g.LN, 1), ik(sx, sy, G["A"][0], G["A"][1], g.LN, g.LN, up), u), ln_
    if t < BACK:
        return ik(sx, sy, tgt[0], tgt[1], g.LN, g.LN, up), ln_
    u = _ease((t - BACK) / 0.4)
    return _alerp(ik(sx, sy, G["V"][0], G["V"][1], g.LN, g.LN, up), ik(sx, sy, REST14[0], REST14[1], g.LN, g.LN, 1), u), ln_


def _shapes14():
    _, st = _arm14(_t())
    return [{"rest": "quiet", "reach": "grab", "antenna": "grab", "visor": "point"}[st], "quiet"]


def s1_4(k, d):
    """47 drawings (as v13). The robot speaks, its visor typing REPLY, his phone still in its raised claw. Don, smug,
    looking off, puts his hand out without a look: it closes on the antenna (which bends and twangs), lets go, and lands
    on the visor on "Approved." (thumb 1 is now a fingertip); the green tick."""
    from cand_bc import ik
    t = d / float(DPS)
    g.REC.clear()
    tgt, st = _arm14(t)
    (a1, a2), ln_ = angles14(t)
    talk = 0.0
    if s1.LINE_D[0] <= t <= s1.LINE_D[1]:
        talk = (1.0, 0.5, 1.0, 0.0)[int((t - s1.LINE_D[0]) * DPS / 2) % 4]
    tick = t >= s1.LINE_D[0] + 0.15
    speaking = s1.LINE_R[0] <= t <= s1.LINE_R[1]
    G = _geo14()

    def ex(k_, o):
        c_ = k_.c
        sx, sy = o["robot"]["screen"]
        rr = 50 * sb.SC["robot"]
        hx, hy = o["robot"]["hands"][1]
        v14._phone(k_, hx, hy - 10, -0.2, 1.25)                                     # his phone, held low in its claw (v15: the wall
                                                                                    # on its left is the bubble's)
        lit = 0.6 if (speaking and (d // 2) % 3 == 0) else 1.0
        ellipse(k_, sx, sy, 0.80 * rr, 0.62 * rr, (0.06, 0.08, 0.12), 990, shadow=False, lw=1.6)
        if tick:
            c_.set_source_rgb(*cp.GRN); c_.set_line_width(0.12 * rr); c_.set_line_cap(1)
            c_.move_to(sx - 0.3 * rr, sy); c_.line_to(sx - 0.08 * rr, sy + 0.22 * rr); c_.line_to(sx + 0.34 * rr, sy - 0.25 * rr); c_.stroke()
        else:
            n = min(len(s1.TYPE), max(0, int((t - s1.LINE_R[0]) * 6)))
            if n:
                cp.T(c_, s1.TYPE[:n], sx - 0.48 * rr, sy + 0.12 * rr, 0.36 * rr, col=tuple(v * lit for v in cp.CYAN), center=False)
        if st == "antenna" or (HOLD_A[1] <= t < HOLD_A[1] + 0.25):                    # bent while held; still ringing after
            held = st == "antenna"
            c_.set_source_rgb(*INK); c_.set_line_width(0.9); c_.set_line_cap(1)
            amp = 1.0 if held else 0.6
            for sg in (-1, 1):
                for q in ((5, 9) if (d % 2 or held) else (7,)):
                    c_.new_path(); c_.arc(sx, sy - 1.42 * rr, q * amp, (-0.5 if sg > 0 else math.pi - 0.5), (0.5 if sg > 0 else math.pi + 0.5)); c_.stroke()
            if held:
                c_.set_source_rgb(0.45, 0.45, 0.50); c_.set_line_width(1.6)
                c_.move_to(sx, sy - 0.95 * rr); c_.curve_to(sx, sy - 1.2 * rr, sx + 0.1 * rr, sy - 1.35 * rr, G["A"][0], G["A"][1] - 0.02 * rr); c_.stroke()
                ellipse(k_, G["A"][0] + 0.02 * rr, G["A"][1] - 0.04 * rr, 2.6, 2.6, (0.98, 0.80, 0.20), 949, shadow=False, lw=1.0)
                g.again(k_, 0, "grab")
        if st == "visor":
            g.again(k_, 0, "point")

    with s1.A.Don(s1.A.UP, talk), s1.Breath(sb, "don", s1.br(d)), s1.Breath(sb, "robot", s1.br(d, 0.5, 0.006)):
        u = _ease((t - s1.PUSH[0]) / (s1.PUSH[1] - s1.PUSH[0]))
        cam = tuple(a_ + (b_ - a_) * u for a_, b_ in zip(s1.TWO14, s1.TWO14_IN))
        if True:
            S(k, cam, auto=False, portrait="hang", extra=ex,
              **base(cl=False, sf=False, pm=False, mm=False, door=0.0, rb=at("robot", arm=ARM14[0]),
                     dn=at("don", x=X["don"] - STEP - ln_, pose=(a1, a2, 8, 0), face="smug", look=(1, -0.3))))




# ---- 3.1: faster than his hand -------------------------------------------------------------------------------------------

SHOOT = (0.20, 0.62)                                       # the sheet's tip from the slot to off the frame's left (s)
GRAB = (0.30, 0.55)                                        # his hand goes for it ...
GRAB_AT = [(366.0, 724.0)]
LUNGE = 26.0                                               # he lunges a step at it
SHUT = 0.62                                                # ... and closes on air
LOOK = (0.95, 2.20)                                        # he looks at his empty fist
DROP = 2.30                                                # the arm comes down; "Approved." follows, unread


def _path31(sx, by, floor):
    """The sheet's whole run: out of the slot in an arc, down to the floor, away over it to the left, in low waves."""
    pts = []
    for i in range(16):
        u = i / 15.0
        pts.append((sx - 4 - 14 * u * u, by + (floor - 3 - by) * (u ** 1.3)))
    x0 = pts[-1][0]
    for i in range(1, 50):
        u = i / 49.0
        pts.append((x0 - 210 * u, floor - 3 - 3.0 * abs(math.sin(u * 8.0)) * (1 - 0.5 * u)))
    return pts


def _len(pts):
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]))


def _cut(pts, L):
    out, acc = [pts[0]], 0.0
    for a, b in zip(pts, pts[1:]):
        l = math.hypot(b[0] - a[0], b[1] - a[1])
        if acc + l >= L:
            u = (L - acc) / l if l else 0
            out.append((a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u)); return out
        out.append(b); acc += l
    return out


def _shapes31():
    t = _t()
    if t < GRAB[0]:
        return ["point", "quiet"]
    if t < SHUT:
        return ["grab", "quiet"]
    return ["fist" if t < DROP + 0.3 else "quiet", "quiet"]


def s3_1(k, d):
    """44 drawings (as v13). Don points at the robot: recover it. The robot speaks, PRINT; the sheet shoots out of its
    chest slot in an arc and is gone over the floor to the left before his hand gets there: it shuts on air. He looks at
    his fist; the arm drops; "Approved.", unread."""
    from cand_bc import ik
    t = d / float(DPS)
    floor = sb.F + 4
    pt = s3.POINT_AT
    grab_at = GRAB_AT[0]
    lunge = LUNGE * (_ease((t - GRAB[0]) / 0.2) if t < DROP else 1 - _ease((t - DROP) / 0.4))
    if t < GRAB[0]:
        tgt = _lerp((420.0, 736.6), pt, _ease(t / 0.25))
        lunge = 0.0
    elif t < SHUT:
        tgt = _lerp(pt, grab_at, _ease((t - GRAB[0]) / (SHUT - GRAB[0])))
    elif t < DROP:
        tgt = (grab_at[0] + 2, grab_at[1] - 2)
    else:
        tgt = _lerp(grab_at, (420.0, 736.6), _ease((t - DROP) / 0.4))
    a1, a2 = ik(s3.DON_SH_L[0] - lunge, s3.DON_SH_L[1], tgt[0], tgt[1], s3.LN, s3.LN, 1)
    talk = 0.0
    if s3.LINE31D[0] <= t <= s3.LINE31D[1]:
        talk = (1.0, 0.5, 1.0, 0.0)[int((t - s3.LINE31D[0]) * DPS / 2) % 4]
    P = _ease((t - SHOOT[0]) / (SHOOT[1] - SHOOT[0]))
    if t < 0.40:
        face, look = "smug", (-1, -0.1)
    elif t < LOOK[0]:
        face, look = "shock", (-1, 0.4)
    elif t < LOOK[1]:
        face, look = "neutral", (-0.6, 0.9)
    else:
        face, look = "smug", (-1, -0.1)

    def ex(k_, o):
        c = k_.c
        sx, sy = o["robot"]["screen"]
        r = 50 * sb.SC["robot"]
        by = sy + 1.50 * r
        ellipse(k_, sx, sy, 0.80 * r, 0.62 * r, (0.06, 0.08, 0.12), 990, shadow=False, lw=1.6)
        if P < 1:                                                                 # the robot only does its job: PRINT and a bar
            cp.T(c, "PRINT", sx, sy - 0.02 * r, 0.30 * r, col=cp.CYAN)
            c.set_source_rgb(*cp.CYAN); c.rectangle(sx - 0.45 * r, sy + 0.14 * r, 0.9 * r * P, 0.12 * r); c.fill()
        else:
            c.set_source_rgb(*cp.GRN); c.set_line_width(0.12 * r); c.set_line_cap(1)
            c.move_to(sx - 0.3 * r, sy); c.line_to(sx - 0.08 * r, sy + 0.22 * r); c.line_to(sx + 0.34 * r, sy - 0.25 * r); c.stroke()
        g.slot(k_, sx, by, r)
        if P > 0:
            pts = _path31(sx, by, floor)
            if P < 1:                                                             # in flight: the tip still up, curling
                part = _cut(pts, _len(pts) * P)
                lift = 10 * math.sin(math.pi * P)
                part = [(x, y - lift * (i / float(len(part))) ** 2) for i, (x, y) in enumerate(part)]
                g.ribbon(c, part, 7.0)
                tx, ty = part[-1]
                c.set_source_rgb(*INK); c.set_line_width(1.0); c.set_line_cap(1)
                for i in range(3):
                    c.move_to(tx + 8 + i * 9, ty - 6 + i * 2); c.line_to(tx + 15 + i * 9, ty - 6 + i * 2)
                c.stroke()
            else:
                g.ribbon(c, pts, 7.0, shadow=(1.5, 3.0))
        if SHUT <= t < SHUT + 0.17:                                               # air: a puff where his fist shut
            c.save(); c.translate(grab_at[0] - 8, grab_at[1] - 4); c.scale(0.22, 0.22); impact(c, 0, 0, 40); c.restore()

    with s1.A.Don(s1.A.MOUTH, talk), s1.Breath(sb, "don", s1.br(d)), s1.Breath(sb, "robot", s1.br(d, 0.5, 0.006)):
        S(k, s3.CAM31, auto=False, portrait="hang", extra=ex,
          **base(cl=False, sf=False, pm=False, mm=False, door=0.0, rb=at("robot", arm="none"),
                 dn=at("don", x=X["don"] - lunge, pose=(a1, a2, 8, 0), face=face, look=look)))


# ---- 3.1b: the roll at the door ---------------------------------------------------------------------------------------

N31b = 12


def s3_1b(k, d):
    """12 drawings (1.0 s), an insert low at the glass door, empty street behind it: the last of the roll trundles in
    from the right, unrolling, and bumps the glass; it rocks back once and stops. The robot never comes to look."""
    c = k.c
    c.set_source_rgb(*kit.WALL); c.paint()
    c.translate(-90, -620); c.scale(1.75, 1.75)                                    # low and close at the door
    fy = 640.0
    u = _ease(min(1.0, d / 6.0))
    rock = {7: 5.0, 8: -2.0, 9: 1.0}.get(d, 0.0)
    rx = 560 - (560 - 214) * u + rock
    c.set_source_rgb(*kit.WALL); c.rectangle(0, 0, 540, 960); c.fill()
    c.set_source_rgb(0.72, 0.63, 0.48); c.rectangle(0, fy, 540, 960 - fy); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(3); c.move_to(0, fy); c.line_to(540, fy); c.stroke()
    c.set_source_rgb(0.86, 0.91, 0.95); c.rectangle(0, 0, 150, fy + 46); c.fill()
    c.set_source_rgba(1, 1, 1, 0.5)
    for x0 in (30, 70):
        c.move_to(x0, 0); c.line_to(x0 + 22, 0); c.line_to(x0 - 60, fy + 46); c.line_to(x0 - 82, fy + 46); c.close_path(); c.fill()
    if DOOR31b[0]:                                                                # v17: read as a glass DOOR, not a post
        c.set_source_rgba(1, 1, 1, 0.55)                                          # glints inside the view
        for x0, w_ in ((132, 10), (112, 5)):
            c.move_to(x0, 380); c.line_to(x0 + w_, 380); c.line_to(x0 + w_ - 60, fy + 20); c.line_to(x0 - 60, fy + 20); c.close_path(); c.fill()
        g.rect(k, -10, fy + 14, 162, 32, (0.62, 0.65, 0.70), 985, shadow=False, lw=2.5)   # the metal kick rail
        for yy in (470.0, 590.0):                                                 # the pull handle on its two mounts
            g.rect(k, 120, yy - 4, 18, 8, (0.62, 0.65, 0.70), 985, shadow=False, lw=2)
        g.rect(k, 112, 462, 10, 136, (0.74, 0.77, 0.81), 985, shadow=False, lw=2.5)
        c.save(); c.translate(76, 470); c.rotate(-0.04)
        g.rect(k, -26, -12, 52, 24, (0.98, 0.97, 0.93), 985, shadow=False, lw=2)
        cp.T(c, "PUSH", 0, 6, 15, col=INK)
        c.restore()
    g.rect(k, 150, -10, 22, fy + 60, (0.36, 0.40, 0.47), 986, shadow=False, lw=3)
    pts = []
    for i in range(61):
        q = i / 60.0
        x = 560 + 40 - (600 - rx) * q
        pts.append((x, fy + 78 - 26 * q - 9 * abs(math.sin(q * 8.2)) * (1 - 0.6 * q)))
    g.ribbon(c, pts, 30.0, shadow=(5, 12))
    rad = 46 - 6 * u
    c.set_source_rgba(0.25, 0.18, 0.10, 0.25); c.save(); c.translate(rx, fy + 62); c.scale(1, 0.25); c.arc(0, 0, rad + 12, 0, 6.3); c.fill(); c.restore()
    ellipse(k, rx, fy + 62 - rad, rad, rad, g.BLUE, 993, shadow=False, lw=3)
    ellipse(k, rx, fy + 62 - rad, rad * 0.66, rad * 0.66, (0.24, 0.50, 0.90), 996, shadow=False, lw=1.6)
    ellipse(k, rx, fy + 62 - rad, rad * 0.3, rad * 0.3, (0.95, 0.96, 1.0), 994, shadow=False, lw=2)
    a = -d * 1.1 if d <= 6 else -6.6 - rock * 0.05                                 # it turns as it rolls
    c.set_source_rgb(*INK); c.set_line_width(2)
    c.move_to(rx + math.cos(a) * rad * 0.32, fy + 62 - rad + math.sin(a) * rad * 0.32)
    c.line_to(rx + math.cos(a) * rad * 0.62, fy + 62 - rad + math.sin(a) * rad * 0.62); c.stroke()
    if d in (6, 7):
        c.save(); c.translate(rx - rad - 6, fy + 62 - rad); impact(c, 0, 0, 30 if d == 6 else 22); c.restore()


# ---- 3.5: the ball, and the throw ---------------------------------------------------------------------------------------

N35 = 22
CAM35 = ((268, 628, 3.4), (318, 628, 2.85))                 # wide enough for the raised fist; eases out for the throw
RAISE = (0.0, 0.40)
WIND = (1.25, 1.42)                                          # after "Is this a joke?" (0.25-1.32)
THROW = 1.42


def _shapes35():
    t = _t()
    return ["quiet", "palm" if t >= THROW else "grab"]


def s3_5(k, d):
    """22 drawings (1.8 s; was 20). He crumples the AI's sheet into a ball in his fist as his arm comes up; tilts his
    head, "Is this a joke?", dangerously calm (narrowed eyes, the lean in, only a hint of red); winds up; throws, the
    hand opening; the ball goes out of frame toward Don."""
    t = d / float(DPS)
    g.REC.clear()
    code = s3.talk_code(t, *s3.LINE35)
    stand = sb.co.POSES["stand"] if hasattr(sb.co, "POSES") else (-10, 5, 8, 0)
    up = (-10, 5, 150, 40)
    wind = (-10, 5, 160, 45)                                                    # v16: wound back, the elbow bent
    out = (-10, 5, 108, 32)                                                     # v16: the follow-through bent (elbow gate)
    if t < WIND[0]:                                                               # caught with the arm already up (rule: no raise past the shoulder)
        pose = up
    elif t < THROW:
        u = _ease((t - WIND[0]) / (WIND[1] - WIND[0])); pose = tuple(a + (b - a) * u for a, b in zip(up, wind))
    else:
        u = _ease((t - THROW) / 0.17); pose = tuple(a + (b - a) * u for a, b in zip(wind, out))
    lean = 5 if t < THROW else 8                                                  # v15e: steady while he speaks (the locked bubble sat on his leaning face)
    cu = _ease((t - WIND[0]) / 0.4)
    cam = tuple(a + (b - a) * cu for a, b in zip(*CAM35))
    crumple = min(1.0, t / 0.33)

    def ex(k_, o):
        s_ = sb.SC["client"]
        r = 8.5 * s_ / 0.52
        c = k_.c
        hx, hy, hw, _, hd, _, m_ = g.REC[-1]                                        # his right hand, in its own (leaning) space
        c.save(); c.set_matrix(m_)
        nd = math.hypot(*hd) or 1.0
        hx, hy = hx + hd[0] / nd * 0.40 * hw, hy + hd[1] / nd * 0.40 * hw     # the ball in the palm, the fingers over it
        r = r * 1.35
        if t < THROW:
            c.restore()
            g.again(k_, len(g.REC) - 1, "grab")                                    # v16: the hand round it (fist: a big thumb)
            c.save(); c.set_matrix(m_)
            g._ball(k_, hx + hd[0] / nd * 0.55 * hw, hy + hd[1] / nd * 0.55 * hw, r * (1.3 - 0.15 * crumple), seed=int(crumple * 5))
            c.restore()
            return
        if t < THROW + 0.34:                                                      # leaving, toward the frame's right edge
            q = (t - THROW) / 0.34
            bx, by = hx + 12 + 60 * q, hy - 6 - 14 * q
            g._ball(k_, bx, by, r)
            v14._zz(c, bx, by, math.pi - 0.2)
        c.restore()

    old = sb.pocket_strip
    sb.pocket_strip = lambda *a_, **kw: None                                      # its blue strip stays in the pocket (no edge on the arm)
    try:
        with s3.Client(mouth=code, lean=lean, edge=False), s1.Breath(sb, "client", s1.br(d, 0.4, 0.012)):
            S(k, cam, auto=False, portrait=False, extra=ex,
              **base(rb=False, sf=False, dn=False, pm=False, mm=False, door=0.0,
                     cl=at("client", pose=pose, face="suspicious", look=(1, 0.1))))
    finally:
        sb.pocket_strip = old
    s3.b3.flush(k, "client", min(0.10, max(0.0, (d - 6) / 6.0) * 0.10))


# ---- 3.5b: PLOK -----------------------------------------------------------------------------------------------------

N35b = 18
LEAN35b = [0, 0, 7, 10, 7, 4, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


def s3_5b(k, d):
    """18 drawings (1.5 s; was 8). Two drawings: the ball comes at him, big; one: it squashes on his forehead, PLOK;
    three: his head knocked back and coming forward; it drops out of frame; then he freezes, one eye twitching."""
    cam = __import__("cs_v19").CAMS19["3.5b"]
    lean = LEAN35b[d]
    w = 0.45 * math.sin((d - 2) * 1.9) * math.exp(-(d - 2) / 2.5) if d >= 2 else 0.0
    pts = s1.A.lerp(s1.A.MOUTH, s1.A.CROOKED4, w)
    face = "smug" if d < 2 else ("panic" if d < 8 else "neutral")
    look = (-1, 0) if d < 2 else ((-1, -0.6) if d < 8 else (-0.1, 0.0))

    def ex(k_, o):
        hx, hy = o["don"]["head"]
        s_ = sb.SC["don"]
        c = k_.c
        fx, fy = hx - 31 * s_, hy - 22 * s_
        c.save(); c.translate(X["don"], sb.F); c.rotate(math.radians(lean)); c.translate(-X["don"], -sb.F)
        if d < 2:                                                                 # coming at him from the left, big, fast
            q = (d + 1) / 3.0
            bx, by = fx - 120 * (1 - q), fy - 30 * (1 - q)
            g._ball(k_, bx, by, 7.5 + 6 * (1 - q))
            v14._zz(c, bx, by, math.pi + 0.25)
        elif d == 2:
            c.save(); c.translate(fx - 5, fy); c.scale(0.6, 0.6); impact(c, 0, 0, 40); c.restore()
            c.save(); c.translate(fx - 2, fy); c.rotate(-0.5); c.scale(0.55, 1.3); g._ball(k_, 0, 0, 7.5); c.restore()
        elif d < 8:                                                               # off his forehead and down out of the frame
            q = (d - 3) / 4.0
            g._ball(k_, fx - 14 - 10 * q, fy + 10 + 260 * q * q, 7.5)
        elif d in (10, 11, 14):                                                   # the eye that twitches
            c.set_source_rgb(*INK); c.set_line_width(1.0); c.set_line_cap(1)
            c.move_to(hx - 2 * s_, hy - 7 * s_); c.line_to(hx + 6 * s_, hy - 10 * s_); c.stroke()
        c.restore()

    orig = sb.don

    def don(k_, x, feet, *a_, **kw):
        c_ = k_.c
        c_.save(); c_.translate(x, feet); c_.rotate(math.radians(lean)); c_.translate(-x, -feet)
        try:
            return orig(k_, x, feet, *a_, **kw)
        finally:
            c_.restore()
    sb.don = don
    try:
        with s1.A.Don(pts), s1.Breath(sb, "don", s1.br(d, 0.0, 0.012)):
            S(k, cam, auto=False, mic="down", portrait="hang", extra=ex,
              **base(cl=False, sf=False, rb=False, pm=False, mm=False, door=0.0,
                     dn=at("don", face=face, look=look)))
    finally:
        sb.don = orig


# ---- install ------------------------------------------------------------------------------------------------------------

def _replace(shots, name, entry):
    i = [x[0] for x in shots].index(name)
    shots[i] = entry


def install():
    v14.install()                                                                  # 1.1 and its sound, s1.V = v14
    _replace(s1.SHOTS, "1.4", ("1.4", s1.N14, s1_4))
    _replace(s3.SHOTS, "3.1", ("3.1", s3.N31, s3_1))
    _replace(s3.SHOTS, "3.5", ("3.5", N35, s3_5))
    _replace(s3.SHOTS, "3.5b", ("3.5b", N35b, s3_5b))
    if not any(x[0] == "3.1b" for x in s3.SHOTS):
        s3.SHOTS.insert(1, ("3.1b", N31b, s3_1b))
    s3.V = "v14"
    import cs_v19
    cs_v19.CAMS19.pop("3.5", None)                                                 # the CU cut off his arm: CAM35 instead
    ch.STATE["1.4"] = _shapes14
    ch.STATE["3.1"] = _shapes31
    ch.STATE["3.5"] = _shapes35
    ch._BYFN.clear()
    orig_hook = ch.hook

    def rec(k, hx, hy, w, skin, seed, d, side):                                    # every hand recorded, so a prop can go
        n = hp._N[0]                                                               # under its fingers (g.again)
        orig_hook(k, hx, hy, w, skin, seed, d, side)
        if hp._N[0] > n:
            g.REC.append((hx, hy, w * 1.25, skin, d, -1 if n % 2 == 0 else 1, k.c.get_matrix()))
    if not getattr(ch.hook, "_v14", False):
        rec._v14 = True
        was = kit.HAND[0] is ch.hook
        ch.hook = rec
        if was:
            kit.HAND[0] = rec
    import cs_film
    import cs_sfx as fx
    cs_film.MUSIC_BACK[0] = 0.75                                                  # after "Approved.", not under it (Whisper: "Approve.")
    cs_film.BUZZ = [("1.1", 0.05, 0.31, 0.8)] + [b for b in cs_film.BUZZ if b[0] != "1.1"]
    cs_film.FX = [x for x in cs_film.FX if not (x[0] == "3.1" and x[1] in (28, 29))]  # the old slow curl and late tick
    cs_film.FX = [(sh, 44 if (sh, d) == ("1.4", 36) else d, x, gn) for sh, d, x, gn in cs_film.FX]   # its tick sat on "-proved": after the word
    cs_film.FX += [("1.1", d, (fx.tap(220.0) if n == "tap" else getattr(fx, n)()), gn) for d, n, gn in v14.SFX]
    cs_film.FX += [("1.4", 26, fx.sweep(900, 520, 0.22), 0.16),                    # the antenna's twang
                   ("3.1", 2, fx.whoosh(0.3), 0.20), ("3.1", 7, fx.tap(260.0), 0.16), ("3.1", 9, fx.pop(880), 0.14),
                   ("3.1b", 0, fx.rustle(0.6), 0.18), ("3.1b", 6, fx.tap(150.0), 0.40),
                   ("3.5", 0, fx.rustle(0.35), 0.22), ("3.5", 17, fx.whoosh(0.2), 0.18),
                   ("3.5b", 2, fx.tap(320.0), 0.55)]                               # PLOK
