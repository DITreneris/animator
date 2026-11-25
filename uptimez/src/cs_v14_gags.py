"""ONE STAR v14: key poses for the three other physical beats Tomas picked (25 Nov), stills for approval, no motion.
  M  1.4  Don presses without looking: first the robot's antenna (it twangs), then its visor
  R  3.1  the sheet comes out faster than he can catch it and unrolls across the floor to the door
  C  3.5  the Client screws the AI's plan into a ball and throws it; 3.5b it lands on Don's forehead
  python3 cs_v14_gags.py [out.png]"""
import math
import sys
import cairo
import cs_scene1_v14 as v14
import cs_scene1 as s1
import cs_scene3 as s3
from cs_scene1 import S, at, base, sb, kit, cp, ellipse, rect, INK
from cs_board import impact, X

import cs_hands as ch
import hands_ps as hp

BLUE = (0.20, 0.45, 0.85)
REC = []                                                   # this drawing's hands as the hook got them


def shapes(*g):
    """The series' hand (hands_ps) for the tile being drawn: one shape per human hand, in drawing order."""
    ch.STATE[None] = list(g)


def _hook(k, hx, hy, w, skin, seed, d, side):
    n = hp._N[0]
    ch.hook(k, hx, hy, w, skin, seed, d, side)
    if hp._N[0] > n:
        REC.append((hx, hy, w * 1.25, skin, d, -1 if n % 2 == 0 else 1, k.c.get_matrix()))


def again(k, i, g):
    """Draw hand i once more on top (the object first, then the fingers over it: one hand, two passes)."""
    hx, hy, w, skin, d, arm, m_ = REC[i]
    c = k.c
    c.save(); c.set_matrix(m_); hp.draw(k, g, hx, hy, w, skin, d, arm); c.restore()


def ribbon(c, pts, w=7.0, shadow=None):
    """The printed sheet as a band along pts: a contact shadow, ink edge, blue, and the print across it."""
    def path():
        c.new_path(); c.move_to(*pts[0])
        for q in pts[1:]:
            c.line_to(*q)
    c.set_line_join(1); c.set_line_cap(0)
    if shadow:
        c.save(); c.translate(*shadow); path(); c.set_source_rgba(0.25, 0.18, 0.10, 0.22); c.set_line_width(w + 1); c.stroke(); c.restore()
    path(); c.set_source_rgb(*INK); c.set_line_width(w + 2.4); c.stroke()
    path(); c.set_source_rgb(*BLUE); c.set_line_width(w); c.stroke()
    c.set_source_rgba(1, 1, 1, 0.9); c.set_line_width(0.9)
    acc = 0.0
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):                                   # print: short strokes across the band
        l = math.hypot(x1 - x0, y1 - y0); acc += l
        if acc >= 6.0 and l > 0:
            acc = 0.0
            nx, ny = -(y1 - y0) / l, (x1 - x0) / l
            h = w * (0.34 if int(x0 + y0) % 3 else 0.18)
            c.move_to(x0 - nx * h, y0 - ny * h); c.line_to(x0 + nx * h, y0 + ny * h)
    c.stroke()


def slot(k, sx, by, rr):
    """The robot's print slot: a dark mouth with a lip, so the sheet has somewhere to come from."""
    c = k.c
    v14._rr(c, sx - 0.62 * rr, by - 0.17 * rr, 1.24 * rr, 0.34 * rr, 0.12 * rr)
    c.set_source_rgb(0.62, 0.64, 0.70); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.1); c.stroke()
    c.set_source_rgb(0.06, 0.08, 0.12); c.rectangle(sx - 0.5 * rr, by - 0.07 * rr, 1.0 * rr, 0.14 * rr); c.fill()
STEP = 10.0                                                # Don a step nearer the robot in 1.4: the elbow stays bent
LN = 48 * 0.60


def _reach(tx, ty):
    from cand_bc import ik
    sh = (s1.DON_SH[0] - STEP, s1.DON_SH[1])
    a1, a2 = ik(sh[0], sh[1], tx, ty, LN, LN, 1)
    d = math.hypot(tx - sh[0], ty - sh[1])
    bend = 180 - math.degrees(math.acos(max(-1, min(1, (2 * LN * LN - d * d) / (2 * LN * LN)))))
    return (a1, a2, 8, 0), bend


def _thumb(k, o):
    pass                                                    # v5: the hand is hands_ps's own shape (grab, point)


def m(k, hit):
    """1.4. hit False: his thumb on the bow tie (the visor still asks); True: on the visor, the green tick."""
    geo = {}

    def probe(k_, o):
        geo["s"] = o["robot"]["screen"]
    s1.draw(lambda k_, d: S(k_, s1.TWO14_IN, auto=False, extra=probe,
                            **base(cl=False, sf=False, pm=False, mm=False, door=0.0, rb=at("robot", arm="none"))), 0)
    sx, sy = geo["s"]
    rr = 50 * sb.SC["robot"]
    shapes("point" if hit else "grab", "quiet")
    tgt = (sx + 0.92 * rr, sy + 0.02 * rr) if hit else (sx + 0.34 * rr, sy - 1.40 * rr)
    pose, bend = _reach(*tgt)
    M_BEND[hit] = bend

    def ex(k_, o):
        c_ = k_.c
        ellipse(k_, sx, sy, 0.80 * rr, 0.62 * rr, (0.06, 0.08, 0.12), 990, shadow=False, lw=1.6)
        if hit:
            c_.set_source_rgb(*cp.GRN); c_.set_line_width(0.12 * rr); c_.set_line_cap(1)
            c_.move_to(sx - 0.3 * rr, sy); c_.line_to(sx - 0.08 * rr, sy + 0.22 * rr); c_.line_to(sx + 0.34 * rr, sy - 0.25 * rr); c_.stroke()
            again(k_, 0, "point")
        else:
            cp.T(c_, "REPLY", sx, sy + 0.12 * rr, 0.34 * rr, col=cp.CYAN)
            c_.set_source_rgb(*INK); c_.set_line_width(0.9); c_.set_line_cap(1)                # the antenna twangs
            for sg in (-1, 1):
                for q in (5, 9):
                    c_.new_path(); c_.arc(sx, sy - 1.42 * rr, q, (-0.5 if sg > 0 else math.pi - 0.5), (0.5 if sg > 0 else math.pi + 0.5)); c_.stroke()
            c_.set_source_rgb(0.45, 0.45, 0.50); c_.set_line_width(1.6)                          # the stalk bent over by his fingers
            c_.move_to(sx, sy - 0.95 * rr); c_.curve_to(sx, sy - 1.2 * rr, sx + 0.1 * rr, sy - 1.35 * rr, sx + 0.24 * rr, sy - 1.42 * rr); c_.stroke()
            ellipse(k_, sx + 0.26 * rr, sy - 1.44 * rr, 2.6, 2.6, (0.98, 0.80, 0.20), 949, shadow=False, lw=1.0)
            again(k_, 0, "grab")
        _thumb(k_, o)

    with s1.A.Don(s1.A.UP, 1.0 if hit else 0.0):
        S(k, s1.TWO14_IN, auto=False, portrait="hang", extra=ex,
          **base(cl=False, sf=False, pm=False, mm=False, door=0.0, rb=at("robot", arm="none"),
                 dn=at("don", x=X["don"] - STEP, pose=pose, face="smug", look=(1, -0.3))))


def r_door(k):
    """3.1b, an insert low at the glass door (the wide of it put everyone small): the sheet has run the floor, the roll's
    end bumps the glass; the Client's boots are already there on the other side."""
    c = k.c
    FLOOR = (0.72, 0.63, 0.48)
    c.set_source_rgb(*kit.WALL); c.paint()
    fy = 640.0
    c.set_source_rgb(*FLOOR); c.rectangle(0, fy, 540, 960 - fy); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(3); c.move_to(0, fy); c.line_to(540, fy); c.stroke()
    # the door: glass to the left of its frame, the street light behind it
    c.set_source_rgb(0.86, 0.91, 0.95); c.rectangle(0, 0, 150, fy + 46); c.fill()
    c.set_source_rgba(1, 1, 1, 0.5)
    for x0 in (30, 70):
        c.move_to(x0, 0); c.line_to(x0 + 22, 0); c.line_to(x0 - 60, fy + 46); c.line_to(x0 - 82, fy + 46); c.close_path(); c.fill()
    # his boots and trouser legs behind the glass
    for bx_ in (38, 92):
        rect(k, bx_ - 16, fy - 200, 34, 214, (0.26, 0.28, 0.34), 981 + bx_, shadow=False, lw=2.4)
        v14._rr(c, bx_ - 22, fy + 2, 54, 30, 12); c.set_source_rgb(0.42, 0.27, 0.16); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.4); c.stroke()
    c.set_source_rgba(0.86, 0.91, 0.95, 0.35); c.rectangle(0, 0, 150, fy + 46); c.fill()          # the glass over him
    rect(k, 150, -10, 22, fy + 60, (0.36, 0.40, 0.47), 986, shadow=False, lw=3)                      # the frame
    # the sheet along the floor toward us from the right, in low waves, and what is left of the roll at the glass
    pts = []
    for i in range(61):
        u = i / 60.0
        pts.append((560 - (560 - 232) * u, fy + 78 - 26 * u - 9 * abs(math.sin(u * 8.2)) * (1 - 0.6 * u)))
    c.save(); ribbon(c, pts, 30.0, shadow=(5, 12)); c.restore()
    c.set_source_rgba(0.25, 0.18, 0.10, 0.25); c.save(); c.translate(214, fy + 62); c.scale(1, 0.25); c.arc(0, 0, 52, 0, 6.3); c.fill(); c.restore()
    ellipse(k, 214, fy + 22, 40, 40, BLUE, 993, shadow=False, lw=3)
    ellipse(k, 214, fy + 22, 27, 27, (0.24, 0.50, 0.90), 996, shadow=False, lw=1.6)
    ellipse(k, 214, fy + 22, 13, 13, (0.95, 0.96, 1.0), 994, shadow=False, lw=2)
    c.save(); c.translate(176, fy + 6); impact(c, 0, 0, 34); c.restore()


M_BEND = {}
CAM_R = (337, 640, 2.0)                                    # the door, the robot and Don: the whole run of the floor


def r(k, stage):
    """3.1. stage 0: the sheet shoots out level, his hand closing on air behind it. 1: it has run across the floor to the
    door; the roll's end against the glass; he looks at his empty hand."""
    from cand_bc import ik
    floor = sb.F + 4
    tgt = (396.0, 716.0) if stage == 0 else (404.0, 724.0)
    a1, a2 = ik(s3.DON_SH_L[0], s3.DON_SH_L[1], tgt[0], tgt[1], s3.LN, s3.LN, 1)

    def ex(k_, o):
        c_ = k_.c
        sx, sy = o["robot"]["screen"]
        rr = 50 * sb.SC["robot"]
        ellipse(k_, sx, sy, 0.80 * rr, 0.62 * rr, (0.06, 0.08, 0.12), 990, shadow=False, lw=1.6)
        cp.T(c_, "PRINT", sx, sy + 0.10 * rr, 0.30 * rr, col=cp.CYAN)
        by = sy + 1.50 * rr
        slot(k_, sx, by, rr)
        if stage == 0:                                                            # out of the slot in an arc, waving, the tip curling
            pts = []
            for i in range(41):
                u = i / 40.0
                x = sx - 0.2 * rr - 66 * u
                y = by + 30 * u * u - 5.0 * math.sin(u * 9.0) * u
                pts.append((x, y))
            ribbon(c_, pts, 7.0)
            c_.set_source_rgb(*INK); c_.set_line_width(1.0); c_.set_line_cap(1)
            for i in range(3):
                c_.move_to(sx - 30 - i * 18, by - 9 - i * 1.5); c_.line_to(sx - 39 - i * 18, by - 8 - i * 1.5)
            c_.stroke()
        else:                                                                     # down in a curve, then away over the floor in low waves
            end = 216.0
            pts = []
            for i in range(13):
                u = i / 12.0
                pts.append((sx - 0.2 * rr - 14 * u * u, by + (floor - 3 - by) * (1 - (1 - u) ** 1.6)))
            x0 = pts[-1][0]
            for i in range(1, 61):
                u = i / 60.0
                x = x0 + (end + 12 - x0) * u
                pts.append((x, floor - 3 - 3.2 * abs(math.sin(u * 9.4)) * (1 - 0.5 * u)))
            ribbon(c_, pts, 6.0, shadow=(1.5, 3.0))
            c_.set_source_rgba(0.25, 0.18, 0.10, 0.25); c_.save(); c_.translate(end + 4, floor + 1); c_.scale(1, 0.25); c_.arc(0, 0, 13, 0, 6.3); c_.fill(); c_.restore()
            ellipse(k_, end + 4, floor - 10, 10, 10, BLUE, 993, shadow=False, lw=1.3)   # what is left of the roll, at the door
            ellipse(k_, end + 4, floor - 10, 3.6, 3.6, (0.95, 0.96, 1.0), 994, shadow=False, lw=0.8)
            c_.save(); c_.translate(end - 9, floor - 11); c_.scale(0.3, 0.3); impact(c_, 0, 0, 40); c_.restore()

    shapes("grab" if stage == 0 else "quiet", "quiet")
    with s1.A.Don(s1.A.MOUTH, 0.0):
        S(k, s3.CAM31 if stage == 0 else CAM_R, auto=False, portrait="hang", extra=ex,
          **base(cl=False, sf=False, pm=False, mm=False, door=0.0, rb=at("robot", arm="none"),
                 dn=at("don", pose=(a1, a2, 8, 0), face="shock" if stage == 0 else "neutral",
                       look=(-1, 0.3) if stage == 0 else (-0.6, 1.0))))


def _ball(k, x, y, rad, seed=0):
    c = k.c
    ellipse(k, x, y, rad, rad * 0.94, BLUE, 995 + seed, shadow=False, lw=1.4)
    c.set_source_rgb(0.10, 0.25, 0.55); c.set_line_width(max(0.5, rad * 0.10)); c.set_line_cap(1)
    for a, b_, l in ((0.4, 2.2, 0.75), (2.9, 4.4, 0.7), (5.0, 0.9, 0.6), (1.6, 3.4, 0.5)):
        c.move_to(x + math.cos(a) * rad * l, y + math.sin(a) * rad * l); c.line_to(x + math.cos(b_) * rad * 0.25, y + math.sin(b_) * rad * 0.25)
        c.stroke()
    c.set_source_rgba(1, 1, 1, 0.8); c.set_line_width(max(0.4, rad * 0.07))
    c.move_to(x - rad * 0.5, y - rad * 0.2); c.line_to(x - rad * 0.1, y - rad * 0.55); c.stroke()


def c1(k, thrown):
    """3.5. The Client, dangerously calm (no red face: narrowed eyes, the lean in): the plan a ball IN his fist by his
    shoulder; thrown: the arm through, the hand open, the ball leaving."""
    pose = (-10, 5, 150, 40) if not thrown else (-10, 5, 95, 30)
    shapes("quiet", "grab" if not thrown else "palm")

    def ex(k_, o):
        hx, hy = o["client"]["hands"][-1]
        s_ = sb.SC["client"]
        if not thrown:
            _ball(k_, hx - 1, hy - 5, 8.5 * s_ / 0.52)
            again(k_, len(REC) - 1, "grab")                                        # his fingers over it
        else:
            _ball(k_, hx + 15, hy - 12, 8.5 * s_ / 0.52)
            v14._zz(k_.c, hx + 15, hy - 12, math.pi - 0.4)

    with s3.Client(mouth=None if thrown else "M", lean=5 if not thrown else 8):
        S(k, (268 if not thrown else 292, 628, 3.4 if not thrown else 3.0), auto=False, portrait=False, extra=ex,
          **base(rb=False, sf=False, dn=False, pm=False, mm=False, door=0.0,
                 cl=at("client", pose=pose, face="suspicious", look=(1, 0.1))))
    s3.b3.flush(k, "client", 0.10)


def c2(k, after=False):
    """3.5b. On Don's forehead: the ball squashed flat against it, a big burst, his head knocked back, eyes wide.
    after: it has dropped to the floor in front of him; he has not moved."""
    shapes("quiet", "quiet")
    cam = __import__("cs_v19").CAMS19["3.5b"]
    if after:
        cam = (cam[0] - 6, cam[1] + 30, cam[2] * 0.62)

    def ex(k_, o):
        hx, hy = o["don"]["head"]
        s_ = sb.SC["don"]
        c_ = k_.c
        if not after:
            c_.translate(X["don"], sb.F); c_.rotate(math.radians(7.0)); c_.translate(-X["don"], -sb.F)   # with his head, knocked back
            bx, by = hx - 31 * s_, hy - 22 * s_
            c_.save(); c_.translate(bx - 5, by); c_.scale(0.55, 0.55); impact(c_, 0, 0, 40); c_.restore()
            c_.save(); c_.translate(bx - 2, by); c_.rotate(-0.5); c_.scale(0.62, 1.25); _ball(k_, 0, 0, 7.5); c_.restore()
        else:
            fx, fy = hx - 46 * s_, sb.F + 2
            c_.set_source_rgba(0.25, 0.18, 0.10, 0.25); c_.save(); c_.translate(fx, fy + 6); c_.scale(1, 0.3); c_.arc(0, 0, 9, 0, 6.3); c_.fill(); c_.restore()
            _ball(k_, fx, fy, 7.0)
            c_.set_source_rgb(*INK); c_.set_line_width(0.9)                                   # the eye that twitches
            c_.move_to(hx - 2 * s_, hy - 6 * s_); c_.line_to(hx + 5 * s_, hy - 9 * s_); c_.stroke()

    orig = sb.don
    lean = 0.0 if after else 7.0

    def don(k_, x, feet, *a_, **kw):
        c_ = k_.c
        c_.save(); c_.translate(x, feet); c_.rotate(math.radians(lean)); c_.translate(-x, -feet)
        try:
            return orig(k_, x, feet, *a_, **kw)
        finally:
            c_.restore()
    sb.don = don
    try:
        with s1.A.Don(s1.A.MOUTH):
            S(k, cam, auto=False, mic="down", portrait="hang", extra=ex,
              **base(cl=False, sf=False, rb=False, pm=False, mm=False, door=0.0,
                     dn=at("don", face="panic" if not after else "neutral", look=(-1, -0.6) if not after else (-0.2, 0.0))))
    finally:
        sb.don = orig


TILES = [("M1  1.4  he misses: the antenna", lambda k, d: m(k, False)), ("M2  1.4  then the visor: Approved.", lambda k, d: m(k, True)),
         ("R1  3.1  out faster than his hand", lambda k, d: r(k, 0)), ("R2  3.1b  insert: the roll reaches the door", lambda k, d: r_door(k)),
         ("C1  3.5  Is this a joke?", lambda k, d: c1(k, False)), ("C2  3.5  he throws it", lambda k, d: c1(k, True)),
         ("C3  3.5b  PLOK: on Don's forehead", lambda k, d: c2(k)), ("C4  3.5b  it drops; he has not moved", lambda k, d: c2(k, True))]


def sheet(out, tw=380):
    th = tw * 960 // 540
    cols = 4
    rows = (len(TILES) + cols - 1) // cols
    big = cairo.ImageSurface(cairo.FORMAT_RGB24, tw * cols, (th + 34) * rows)
    cc = cairo.Context(big); cc.set_source_rgb(1, 1, 1); cc.paint()
    for i, (name, fn) in enumerate(TILES):
        try:
            REC.clear()
            old = kit.HAND[0]; kit.HAND[0] = _hook
            try:
                sf_ = s1.draw(fn, 0)
            finally:
                kit.HAND[0] = old
        except Exception as e:
            print(name, "FAILED", repr(e)); continue
        x, y = (i % cols) * tw, (i // cols) * (th + 34) + 34
        cc.save(); cc.translate(x, y); cc.scale(tw / 540.0, tw / 540.0); cc.set_source_surface(sf_, 0, 0); cc.paint(); cc.restore()
        cc.set_source_rgb(0.8, 0, 0); cc.select_font_face("Inter", 0, 1); cc.set_font_size(19); cc.move_to(x + 8, y - 10); cc.show_text(name)
    big.write_to_png(out)
    print("elbow bend at the press (deg):", {k_: round(v, 1) for k_, v in M_BEND.items()})


if __name__ == "__main__":
    sheet(sys.argv[1] if len(sys.argv) > 1 else "/tmp/ha/os14_gags_keys_v7.png")
