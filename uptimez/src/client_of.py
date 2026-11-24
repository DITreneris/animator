"""THE OFFER (episode 13 on): the Client in his own garage, v1 (decided 22 Nov: a new outfit, same man; client_ob.py v3
stays the office version and is not changed).

Same face, head, build and rig as client_ob v3 (the code below is client_ob.client, read at import and changed in
named places, so the man stays one man). What changes:
  - his navy work overalls, the top half peeled down and its sleeves knotted round his waist; a plain white T-shirt,
    crew neck, short sleeves; bare forearms with oil on the hands; the good watch stays;
  - a red rag hanging from his back pocket (the silhouette's cue now that the blueprint roll is gone);
  - no jacket, no collar pin, no visitor badge, no blueprint, no car fob;
  - faces for this episode (the mute test of 22 Nov read his old faces as fear): "bored" at rest (heavy lids, level
    brows a touch low, a short mouth turned slightly down), "listen", "glance" (to the watch), "stare" (the half-beat
    look, straight, unhurried). His other faces still work (client_ob.FACES).

  client(k, x, feet, s, pose="open", face="bored", look=(0, 0), seed=900, turn=0.0)
     turn: -1..1, a three-quarter turn (the body narrows, the features slide); used by the turnaround.
  python3 client_of.py [out]  ->  ../characters/uptimez-client-of-v1-sheet.png"""
import inspect
import math
import sys
import cairo
import kit
import client_ob as co
from kit import INK, cut, rect, ellipse, Ctx

NAVY, NAVY_D = (0.17, 0.22, 0.34), (0.11, 0.14, 0.23)
TEE, TEE_D = (0.96, 0.95, 0.91), (0.80, 0.79, 0.75)
RAG = co.RAG

FACES = {
    "bored": dict(bl=(3, 3), br=(3, 3), lid=0.46, eye=9.6, iris=5.0, lift=(0, 0), tilt=0.0, corners=0.35),
    "listen": dict(bl=(2, 2), br=(1, 3), lid=0.36, eye=9.8, iris=5.1, lift=(0, 0), tilt=0.02, corners=0.0),
    "glance": dict(bl=(3, 3), br=(3, 3), lid=0.44, eye=9.6, iris=5.0, lift=(0, 0), tilt=0.04, corners=0.2),   # use look=GLANCE
    "stare": dict(bl=(3, 5), br=(5, 3), lid=0.40, eye=9.6, iris=5.0, lift=(0, 0), tilt=0.0, corners=0.0),     # v2: brows level
}                                                                                  # and low at the middle, lids heavy: "are you finished?"
GLANCE = (1.9, 2.0)                                                                # the pupils right down on the watch wrist
_UNUSED = {
}


def _face(k, y, face, look, mouth, seed, chin):
    """the garage faces through client_ob's own face drawing (its 'plain' branch: a level, closed mouth)."""
    if face not in FACES:
        return co._face(k, y, face, look, mouth, seed, chin)
    f = FACES[face]
    old = co.FACES["plain"]
    co.FACES["plain"] = {q: v for q, v in f.items() if q != "corners"}
    try:
        co._face(k, y, "plain", look, mouth, seed, chin)
    finally:
        co.FACES["plain"] = old
    if f["corners"]:                                                           # the corners turned a little down
        c = k.c
        my = y + 34
        c.set_source_rgb(*INK); c.set_line_width(2.6); c.set_line_cap(1)
        d = 3.5 * f["corners"]
        for sx, ex in ((-1, -11), (1, 12)):
            c.move_to(ex, my); c.curve_to(ex + sx * 2, my + 0.5, ex + sx * 3.5, my + d * 0.6, ex + sx * 4, my + d); c.stroke()


def _build():
    src = inspect.getsource(co.client)
    rep = [
        ("def client(k, x, feet, s=1.0, pose=\"arrive\", face=\"confident\", look=(0, 0), seed=900, mouth=None, variant=\"B\",\n           roll=None, badge=True):",
         "def client(k, x, feet, s=1.0, pose=\"open\", face=\"bored\", look=(0, 0), seed=900, mouth=None, variant=\"B\",\n           roll=False, badge=False, turn=0.0):"),
        ("    c.save(); c.translate(x, feet); c.scale(s, s)\n",
         "    c.save(); c.translate(x, feet); c.scale(s * (1 - 0.18 * abs(turn)), s)\n"),
        ("TROUSERS_DARK", "NAVY_D"),
        ("TROUSERS", "NAVY"),
        ("    if not NO_FOB[0]:", "    if False:"),
        # the shirt -> a crew-neck T-shirt; no collar, no placket, no buttons, no belt
        ("(-74, bt + 70)], SHIRT, lw=2.2)", "(-74, bt + 70)], TEE, lw=2.2)"),
        ("    cut(k, [(0, bt + 34), (-20, bt - 9), (20, bt - 9)], SKIN, shadow=False, lw=1.6)\n",
         "    _crew(k, bt, seed)\n"),
        ("        cut(k, [(sx * 20, bt - 10), (sx * 40, bt - 6), (sx * 31, bt + 20), (sx * 3, bt + 30)], SHIRT, shadow=False, lw=1.8)\n",
         "        pass\n"),
        ("    c.move_to(0, bt + 34); c.line_to(0, HIP - 8); c.stroke()\n", ""),
        ("        ellipse(k, 0, yy, 3.2, 3.2, (0.90, 0.90, 0.88), seed + 44 + i, shadow=False, lw=1.2)\n", "        pass\n"),
        ("    rect(k, -64, HIP - 8, 128, 13, BELT, seed + 46, shadow=False, lw=1.6)      # a good belt\n",
         "    _waist(k, seed)\n"),
        ("    rect(k, -9, HIP - 10, 18, 17, STEEL, seed + 47, shadow=False, lw=1.5)\n", ""),
        # no jacket, collar, flaps, pin, badge, roll
        ("    cut(k, [(-98, bt + 32), (-82, bt + 3), (-38, bt - 9), (-27, bt + 16), (-25, HIP + 30), (-80, HIP + 30), (-94, bt + 96)],\n        J, lw=2.4)\n", ""),
        ("    if pocket:                                                               # swept back behind the hip\n", "    if False:\n"),
        ("    else:\n        cut(k, [(98, bt + 32), (82, bt + 3), (38, bt - 9), (27, bt + 16), (25, HIP + 30), (80, HIP + 30), (94, bt + 96)],\n            J, lw=2.4)\n", ""),
        ("    for sx in (-1, 1):                                                       # the cord collar, and a pocket flap\n", "    for sx in ():\n"),
        ("    gear(k, -44, bt + 20, 7.5, col=GOLD, seed=seed + 42)                        # the garages' mark: a pin on his collar\n", ""),
        # the arms: a short white sleeve, a bare forearm
        ("limb(k, sx_, sy_, u, f_, LN1, LN2, 47, 39, J, J, SKIN, hr, seed + 10 + side)",
         "limb(k, sx_, sy_, u, f_, LN1, LN2, 47, 37, TEE, SKIN, SKIN, hr, seed + 10 + side)"),
        ("        ellipse(k, side * (SH[0] - 1), sy_ - 1, 23, 20, J, seed + 14 + side, shadow=False, lw=2)   # the shoulder\n        c.set_source_rgb(*J); c.rectangle(min(side * 60, side * 86), sy_ - 12, 26, 32); c.fill()\n",
         "        ellipse(k, side * (SH[0] - 1), sy_ - 1, 23, 20, TEE, seed + 14 + side, shadow=False, lw=2)   # the shoulder\n        c.set_source_rgb(*TEE); c.rectangle(min(side * 60, side * 86), sy_ - 12, 26, 32); c.fill()\n        _sleeve(k, sx_, sy_, u, seed + 15 + side)\n"),
        ("(wx - px * 19 - ux * 7, wy - py * 19 - uy * 7)], SHIRT, shadow=False, lw=1.8)",
         "(wx - px * 19 - ux * 7, wy - py * 19 - uy * 7)], SKIN, shadow=False, lw=0.01, outline=False)"),
        # the head turns with the body
        ("    c.save(); c.translate(back[0], hy + 55 + back[1]); c.rotate(f[\"tilt\"] - TILT * 0.6); c.scale(HEAD, HEAD)",
         "    c.save(); c.translate(back[0], hy + 55 + back[1]); c.rotate(f[\"tilt\"] - TILT * 0.6); c.scale(HEAD / (1 - 0.18 * abs(turn)), HEAD)"),
        ("    _face(k, hy + 4, face, look, mouth, seed + 30, v[\"chin\"])",
         "    c.save(); c.translate(20 * turn, 0); _face(k, hy + 4, face, look, mouth, seed + 30, v[\"chin\"]); c.restore()"),
        ("    f = FACES[face]\n    hy = HY", "    f = FACES[face] if face in FACES else co.FACES[face]\n    hy = HY"),
    ]
    for a, b in rep:
        if a not in src:
            raise SystemExit("client_of: client_ob.client changed; cannot find:\n" + a)
        src = src.replace(a, b)
    g = dict(vars(co))
    g.update(NAVY=NAVY, NAVY_D=NAVY_D, TEE=TEE, _crew=_crew, _waist=_waist, _sleeve=_sleeve, FACES=FACES, _face=_face, co=co)
    exec(compile(src, "client_of<client_ob.client>", "exec"), g)
    return g["client"]


def _crew(k, bt, seed):
    c = k.c
    c.set_source_rgb(*co.SKIN); c.move_to(-22, bt - 9); c.curve_to(-14, bt + 6, 14, bt + 6, 22, bt - 9); c.close_path(); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(2.2); c.set_line_cap(1)
    c.move_to(-24, bt - 9); c.curve_to(-15, bt + 8, 15, bt + 8, 24, bt - 9); c.stroke()
    c.set_source_rgb(*TEE_D); c.set_line_width(1.6)
    c.move_to(-21, bt - 5); c.curve_to(-13, bt + 10, 13, bt + 10, 21, bt - 5); c.stroke()


def _waist(k, seed):
    """v2: the coveralls' top, peeled down: a navy band round his hips, ONE clear knot at the front, and the two sleeve
    ends hanging apart, each with its cuff; the red rag out of the back pocket on his right side."""
    c = k.c
    HIP = co.HIP
    cut(k, [(-68, HIP - 16), (68, HIP - 16), (70, HIP + 14), (-70, HIP + 14)], NAVY, shadow=False, lw=2.2)
    for sx, ang in ((-1, 0.42), (1, -0.42)):                                                               # the ends, apart
        c.save(); c.translate(sx * 10, HIP + 8); c.rotate(ang)
        cut(k, [(-10, 0), (10, 0), (11, 52), (-9, 54)], NAVY, shadow=False, lw=2)
        cut(k, [(-10, 50), (11, 48), (12, 60), (-10, 62)], NAVY_D, shadow=False, lw=1.8)                     # its cuff
        c.restore()
    ellipse(k, 0, HIP + 2, 17, 14, NAVY_D, seed + 61, shadow=False, lw=2.2)                                  # the knot
    c.set_source_rgb(*INK); c.set_line_width(1.6); c.set_line_cap(1)
    c.move_to(-8, HIP - 6); c.curve_to(0, HIP + 4, 2, HIP + 6, 9, HIP + 10); c.stroke()
    c.save(); c.translate(-64, HIP + 10); c.rotate(0.18)                                                    # the rag
    cut(k, [(-10, -6), (12, -8), (16, 38), (6, 52), (-2, 40), (-12, 50), (-14, 30)], RAG, lw=2)
    c.set_source_rgba(0.35, 0.08, 0.08, 0.6); c.set_line_width(1.4)
    for a_, b_ in (((-6, 8), (8, 20)), ((-8, 26), (6, 34))):
        c.move_to(*a_); c.line_to(*b_); c.stroke()
    c.restore()


def _sleeve(k, sx, sy, u, seed):
    """the T-shirt's short sleeve: its hem across the upper arm."""
    c = k.c
    dx, dy = math.sin(math.radians(u)), math.cos(math.radians(u))
    mx, my = sx + dx * 34, sy + dy * 34
    px, py = -dy, dx
    c.set_source_rgb(*INK); c.set_line_width(2.2); c.set_line_cap(1)
    c.move_to(mx + px * 25, my + py * 25); c.line_to(mx - px * 25, my - py * 25); c.stroke()


client = _build()


# --- the profile (v2): one true side view, for 2.2 (into the engine) and 0.5 / 0.9 (on his back) ---------------------
MOUTH34 = [None]                                                                # opt-in: a lip-sync mouth on the 3/4 head


def head34(k, hy, face="bored", look=(0.9, 1.0), seed=900):
    """v1 (23 Nov; lessons 87 and 88): his head drawn three-quarter, turned toward +x, built from his own parts and
    measures (client_ob's outline, hair, ear, stubble and face). A turned front drawing only slides a bare head; here the
    face is drawn in two halves about a centre line moved toward +x: the near half at full width, the far half 0.6 as wide
    and nearer the middle; only the near ear and the near grey temple; the far edge is the cheek. Client units; the
    head's neck point is (0, hy + 55), as in client_ob."""
    c = k.c
    CX, FAR = 18.0, 0.55                                                        # the face's centre line; the far half's width
    pts0 = co._head_pts(k, hy, seed + 20)

    def sk(p_):                                                                 # v2 (cold test): an outline that turns: the back of
        x_, y_ = p_                                                             # the skull full, the far cheek tucked in, the jaw and
        x_ = x_ * 1.16 if x_ < 0 else x_ * 0.80                                 # chin carried toward the turn; v3: the back of the skull behind the ear
        if y_ > hy + 16:
            x_ += 10 * min(1.0, (y_ - hy - 16) / 40)
        return x_ - 2, y_
    pts = [sk(q) for q in pts0]
    far = max(range(len(pts)), key=lambda i: pts[i][0] - abs(pts[i][1] - hy - 8) * 0.3)   # v2: the brow and the nose break the far edge
    fx_, fy_ = pts[far]
    pts = pts[:far] + [(fx_, hy - 8), (fx_ + 3, hy + 8), (fx_ + 6, hy + 20), (fx_ + 4, hy + 25), (fx_, hy + 28)] + pts[far + 1:]   # v4: ONE nose line
    cut(k, pts, co.SKIN, shadow=False)                                          # v4: no offset shadow (it doubled the nose's edge)

    def inside():
        c.move_to(*pts[0])
        for q in pts[1:]:
            c.line_to(*q)
        c.close_path(); c.clip()
    c.save(); inside()                                                          # two days' shadow
    c.set_source_rgba(0.20, 0.15, 0.13, 0.17)
    c.move_to(-56, hy + 12); c.curve_to(-30, hy + 22, -12, hy + 24, CX - 10, hy + 39)
    c.curve_to(CX, hy + 25, CX + 16, hy + 25, CX + 22, hy + 37); c.curve_to(CX + 26, hy + 24, 40, hy + 18, 56, hy + 8)
    c.line_to(56, hy + 72); c.line_to(-56, hy + 72); c.close_path(); c.fill()
    r = k.rng(seed + 27)                                                        # the stubble's dots, as on his front head
    c.save(); inside()
    c.set_source_rgba(0.16, 0.11, 0.10, 0.42); c.set_line_width(1.3); c.set_line_cap(1)
    for _ in range(26):
        qx = r.uniform(-42, 42); qy = hy + r.uniform(26, 58)
        if abs(qx) < 21 and qy < hy + 44:
            continue
        qx = CX + qx * (1.0 if qx < 0 else FAR)
        c.move_to(qx, qy); c.line_to(qx, qy + 2.6); c.stroke()
    c.restore()
    c.restore()
    c.save(); inside()                                                          # the face, in two halves
    for lo, hi, sc_ in ((-80, CX, 1.0), (CX, 80, FAR)):
        c.save(); c.rectangle(lo - 0.6, hy - 90, hi - lo + 1.2, 200); c.clip()   # overlap: no seam
        c.translate(CX, 0); c.scale(sc_, 1)                                     # (v4's squash of the far half split the mouth: out)
        _face(k, hy + 8, face, look, None, seed + 30, "stubble")                # +4: the features lower, he looks down
        c.restore()
    if MOUTH34[0]:                                                              # v5 (23 Nov, cold tests: "It found nothing" didn't
        import iwry_mouths as im_                                               # move): the take's mouth, on the turned face's
        c.save(); c.translate(CX, 0); c.scale(0.8, 1)                           # centre line, a little narrower (turned)
        im_.mouth(k, 0, hy + 8 + 34, MOUTH34[0], co.SKIN, erase=(12, 6), seed=seed + 96)
        c.restore()
    c.restore()
    hair = [sk(q) for q in [(-47, hy - 2), (-50, hy - 30), (-40, hy - 54), (-10, hy - 66), (24, hy - 64), (46, hy - 46),
                            (50, hy - 24), (47, hy - 10), (40, hy - 26), (28, hy - 38), (2, hy - 40), (-24, hy - 36),
                            (-40, hy - 20)]]
    cut(k, hair, co.HAIR, shadow=False, lw=2)                                   # swept back
    cut(k, [sk(q) for q in [(-47, hy - 2), (-49, hy - 26), (-41, hy - 30), (-39, hy - 14)]], co.GREY, shadow=False, lw=1.6)   # the near temple
    c.set_source_rgba(1, 1, 1, 0.20); c.set_line_width(2.6); c.set_line_cap(1)
    for dy in (0, 9):
        c.move_to(-36, hy - 46 + dy); c.curve_to(-14, hy - 60 + dy, 10, hy - 60 + dy, 30, hy - 50 + dy); c.stroke()
    ellipse(k, -30, hy + 4, 6, 9, co.SKIN, seed + 26, shadow=False, lw=2)       # the near ear, on the side of the head
    c.set_source_rgb(*co.SKIN_DARK); c.set_line_width(1.4)
    c.new_path(); c.arc(-30, hy + 4, 3.2, 1.8, 4.6); c.stroke()


def profile(k, x, feet, s=1.0, facing=-1, lean=0.0, face="bored", look_up=0.0, hands=None, seed=960, head34=None):
    """Side on, facing screen left (facing=-1) or right (1). lean: radians the body tips forward from the hips (0.6:
    over an engine). hands: points in set units for the near hand (his watch hand) and the far hand; None: hanging.
    look_up: 0..1, the head tipped back (lying on his back, looking up at the sump). Returns {"head", "hands"}."""
    c = k.c
    HIP, BT, HY = co.HIP, co.BT, co.HY
    sk = co.SKIN
    c.save(); c.translate(x, feet); c.scale(s * facing, s)           # drawn facing +x; facing -1 mirrors it
    # legs: far (darker) then near; boots toe forward (+x here)
    for col, dx in ((NAVY_D, 14), (NAVY, -6)):
        cut(k, [(dx - 22, HIP + 6), (dx + 22, HIP + 6), (dx + 20, -12), (dx - 18, -12)], col, shadow=False, lw=2)
        cut(k, [(dx - 22, -20), (dx + 40, -16), (dx + 44, -2), (dx - 22, 0)], co.BOOT, lw=2)
    c.save(); c.translate(0, HIP); c.rotate(lean); c.translate(0, -HIP)
    def arm(target, near):
        sx, sy = 4, BT + 30
        if target:
            tx, ty = target
            tx, ty = (tx - x) / s * facing, (ty - feet) / s
            ca, sa = math.cos(-lean), math.sin(-lean)
            rx, ry = tx * ca - (ty - HIP) * sa, HIP + tx * sa + (ty - HIP) * ca
            a1, a2 = co.ik(sx, sy, rx, ry, co.LN1, co.LN2, 1)
        else:
            a1, a2 = (128, -34) if near else (118, -26)        # forward and over the wing, into the bay
        d = lambda a_: (math.sin(math.radians(a_)), math.cos(math.radians(a_)))
        ex, ey = sx + d(a1)[0] * co.LN1, sy + d(a1)[1] * co.LN1
        hx, hy = ex + d(a1 + a2)[0] * co.LN2, ey + d(a1 + a2)[1] * co.LN2
        skin = sk if near else co.SKIN_DARK
        c.set_line_cap(1)
        for col, lw in ((INK, 42), (skin, 36)):
            c.set_source_rgb(*col); c.set_line_width(lw); c.move_to(ex, ey); c.line_to(hx, hy); c.stroke()
        for col, lw in ((INK, 50), (TEE if near else TEE_D, 44)):
            c.set_source_rgb(*col); c.set_line_width(lw); c.move_to(sx, sy); c.line_to(sx + (ex - sx) * 0.62, sy + (ey - sy) * 0.62); c.stroke()
        ellipse(k, hx, hy, co.HAND, co.HAND * 0.9, skin, seed + (3 if near else 4), shadow=False, lw=2)
        if near:                                                                 # the watch, on the near wrist
            wx, wy = hx + (ex - hx) * 0.32, hy + (ey - hy) * 0.32
            ellipse(k, wx, wy, 10, 10, co.GOLD, seed + 5, shadow=False, lw=1.6)
            ellipse(k, wx, wy, 6.4, 6.4, (0.10, 0.16, 0.14), seed + 6, shadow=False, lw=1.0)
        return hx, hy
    far = arm(hands[1] if hands else None, False)
    if hands and hands[0] is None:
        hands = None
    # the waist: the band, the knot at the front, the sleeve ends, the rag at the back
    cut(k, [(-40, HIP - 16), (52, HIP - 16), (54, HIP + 14), (-42, HIP + 14)], NAVY, shadow=False, lw=2.2)
    ellipse(k, 50, HIP + 2, 13, 12, NAVY_D, seed + 7, shadow=False, lw=2)
    cut(k, [(42, HIP + 8), (60, HIP + 8), (64, HIP + 58), (46, HIP + 60)], NAVY, shadow=False, lw=2)
    c.save(); c.translate(-42, HIP + 4); c.rotate(0.12)
    cut(k, [(-12, -4), (8, -6), (12, 40), (2, 54), (-6, 40), (-14, 50), (-16, 28)], RAG, lw=2)
    c.restore()
    # the torso: a barrel chest forward, the back straighter
    cut(k, [(-34, BT - 4), (20, BT - 8), (52, BT + 30), (62, BT + 82), (52, HIP - 12), (-40, HIP - 12), (-46, BT + 60)], TEE, lw=2.2)
    rect(k, -14, BT - 30, 40, 34, sk, seed + 8, shadow=False, lw=2)              # the neck, thick
    near = arm(hands[0] if hands else None, True)                # under the head: bent over, the arms hang below it
    if head34 is not None:                                                      # v3 (23 Nov, Tomas: "the profile looks bad"): his OWN
        c.save(); c.translate(10, HY + 40); c.rotate(0.22); c.translate(-10, -(HY + 40))   # front head, turned three-quarter toward
        rect(k, -10, HY + 40, 34, 34, co.SKIN, seed + 8, shadow=False, lw=2)     # v5: his neck, into the collar
        c.translate(8, HY + 55); c.scale(co.HEAD, co.HEAD); c.translate(0, -(HY + 55))   # v4: the DRAWN three-quarter head
        globals()["head34"](k, HY, face=face, look=(0.9, 1.0), seed=900)
        c.restore()                                                             # the head's tip
        c.restore()                                                             # the lean
        c.restore()                                                             # (x, feet)
        m = facing
        tr = lambda p_: (x + m * p_[0] * s, feet + p_[1] * s)
        return {"head": (x + m * 40 * s, feet + (HY - 4) * s), "hands": [tr(near), tr(far)]}
    # the head, in profile
    c.save(); c.translate(6, HY + 40); c.rotate(-0.9 * look_up); c.scale(co.HEAD, co.HEAD); c.translate(0, -(HY + 40))
    hy = HY
    head = [(-44, hy - 6), (-46, hy - 32), (-30, hy - 54), (0, hy - 60), (28, hy - 50), (42, hy - 30), (46, hy - 14),
            (58, hy + 6), (52, hy + 12), (54, hy + 22), (48, hy + 30), (50, hy + 40), (40, hy + 52), (8, hy + 56),
            (-20, hy + 46), (-38, hy + 20)]
    cut(k, head, sk, lw=2.4)
    c.save(); c.move_to(*head[0])
    for q in head[1:]:
        c.line_to(*q)
    c.close_path(); c.clip()
    c.set_source_rgba(0.20, 0.15, 0.13, 0.17)                                                            # the stubble
    c.move_to(-14, hy + 50); c.curve_to(-4, hy + 26, 20, hy + 20, 40, hy + 24); c.line_to(70, hy + 30); c.line_to(70, hy + 70)
    c.line_to(-14, hy + 70); c.close_path(); c.fill()
    c.restore()
    cut(k, [(-46, hy - 4), (-48, hy - 34), (-30, hy - 58), (2, hy - 64), (30, hy - 54), (40, hy - 40), (22, hy - 42),
            (-2, hy - 40), (-24, hy - 30), (-30, hy - 8)], co.HAIR, shadow=False, lw=2)                     # swept back
    cut(k, [(-30, hy - 30), (-24, hy - 32), (-16, hy - 10), (-24, hy - 6)], co.GREY, shadow=False, lw=1.6)   # the grey temple
    ellipse(k, -12, hy + 4, 9, 13, sk, seed + 9, shadow=False, lw=2)                                      # the ear
    f = FACES.get(face, FACES["bored"])
    ex_, ey_ = 34, hy - 6                                                                                # the eye, side on
    c.save(); c.move_to(ex_ - 6, ey_ - 6); c.line_to(ex_ + 8, ey_); c.line_to(ex_ - 6, ey_ + 6); c.close_path()
    c.set_source_rgb(1, 1, 1); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.6); c.stroke()
    c.set_source_rgb(0.30, 0.20, 0.10); c.arc(ex_ + 2, ey_ + 1 - 3 * look_up, 3.2, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(*sk); c.rectangle(ex_ - 8, ey_ - 8, 18, 16 * f["lid"]); c.fill()                  # the heavy lid
    c.restore()
    c.set_source_rgb(*INK); c.set_line_width(2.4); c.move_to(ex_ - 7, ey_ - 8 + 16 * f["lid"]); c.line_to(ex_ + 7, ey_ - 4 + 16 * f["lid"] * 0.6); c.stroke()
    c.set_line_width(8); c.set_line_cap(1); c.move_to(ex_ - 12, ey_ - 14); c.line_to(ex_ + 12, ey_ - 13); c.stroke()   # the heavy brow
    c.set_source_rgb(*co.SKIN_DARK); c.set_line_width(2.6); c.move_to(50, hy + 4); c.line_to(56, hy + 10); c.stroke()  # the nose's bump
    c.set_source_rgb(*INK); c.set_line_width(3.2); c.move_to(42, hy + 34); c.line_to(50, hy + 33); c.stroke()     # the mouth, flat
    c.restore()
    c.restore()
    c.restore()
    m = facing
    tr = lambda p_: (x + m * p_[0] * s, feet + p_[1] * s)                       # approximate (ignores the lean for hands)
    return {"head": (x + m * 40 * s, feet + (HY - 4) * s), "hands": [tr(near), tr(far)]}


# --- the sheet --------------------------------------------------------------------------------------------------------
def _label(c, s, x, y, size=16, col=INK, center=True):
    c.select_font_face("Inter", 0, 1); c.set_font_size(size); c.set_source_rgb(*col)
    e = c.text_extents(s); c.move_to(x - (e.x_advance / 2 if center else 0), y); c.show_text(s)


def sheet(out="../characters/uptimez-client-of-v2-sheet.png"):
    import of_cast as oc
    import dh_cast as dc
    import fs_storyboard as sb
    W, H = 2200, 2680
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W * 2, H * 2); surf.set_device_scale(2, 2)
    c = cairo.Context(surf); c.set_source_rgb(0.96, 0.95, 0.92); c.paint()
    k = Ctx(c, 0)
    _label(c, "THE CLIENT · in his garage · v2 (episode 13 on) · same man as client_ob v3, new clothes and faces", 40, 50, 30, center=False)
    _label(c, "Navy coveralls peeled to the waist, sleeves knotted · white T-shirt · bare oily forearms · the watch · red rag in the back pocket",
           40, 84, 18, col=(0.3, 0.3, 0.3), center=False)
    # 1. turnaround (and the line-up at the series' scales)
    _label(c, "1  Turnaround", 40, 140, 22, center=False)
    for i, (tn, nm) in enumerate(((0.0, "front"), (-0.6, "three-quarter"), (-1.0, "side-ish"), (0.6, "three-quarter, other way"))):
        client(k, 170 + i * 260, 640, 1.0, "open", "bored", look=(tn, 0), turn=tn)
        _label(c, nm, 170 + i * 260, 680)
    _label(c, "series scale:", 1200, 300, 16)
    F = 640
    sb.don(k, 1330, F, 0.60 / 0.52, "stand", "neutral", look=(1, 0))
    client(k, 1520, F, 1.0, "open", "bored", look=(-1, 0))
    dc.guard(k, 1720, F, 0.56 / 0.52)
    dc.father(k, 1920, F, 0.62 / 0.52, face="hard", look=(-1, 0))
    for x, n in ((1330, "Don"), (1520, "Client"), (1720, "bodyguard"), (1920, "Father")):
        _label(c, n, x, 680)
    # 2. faces
    _label(c, "2  Faces (bored at rest; never wide-eyed in this episode)", 40, 760, 22, center=False)
    for i, (fc, lk, nm) in enumerate((("bored", (0, 0), "bored (rest)"), ("listen", (-1, 0), "listen"),
                                      ("glance", GLANCE, "glance: the watch"), ("stare", (0, 0), "stare: the half-beat"))):
        c.save(); c.rectangle(40 + i * 300, 790, 280, 300); c.clip()
        c.translate(180 + i * 300, 960); c.scale(2.2, 2.2); c.translate(0, -co.HY)
        client(k, 0, 0, 1.0, "open", fc, look=lk)
        c.restore()
        _label(c, nm, 180 + i * 300, 1120)
    # 3. poses
    _label(c, "3  Episode 13 poses (stand-ins from of_cast: lying, sat, bent, watch, phone, slam, the stare)", 40, 1200, 22, center=False)
    old = oc.client
    xs = [150, 430, 700, 960, 1240, 1520, 1800, 2060]
    floor = 1720
    oc.client_sit(k, xs[1], floor, 0.9)
    profile(k, xs[2] + 20, floor, 0.9, facing=-1, lean=0.75, hands=[(xs[2] - 120, floor - 120), (xs[2] - 100, floor - 110)])
    rect(k, xs[2] - 190, floor - 120, 110, 30, (0.30, 0.30, 0.32), 3601, lw=2)          # the engine, a hint
    oc.client(k, xs[3], floor, 0.9, look=GLANCE, targets=oc.watch_pose(xs[3], floor, 0.9), face="glance")
    o = oc.client(k, xs[4], floor, 0.9, look=(-1, 0), targets=[(xs[4] - 160, floor - 260)])
    oc.phone(k, xs[4] - 170, floor - 276, 1.0, None, ang=-0.1)
    lid_y = floor - 176                                                                   # the bonnet's lid, at the contact
    cut(k, [(xs[5] - 250, lid_y + 6), (xs[5] - 60, lid_y - 10), (xs[5] - 56, lid_y + 4), (xs[5] - 250, lid_y + 22)],
        (0.40, 0.62, 0.80), lw=2.4)
    rect(k, xs[5] - 250, lid_y + 22, 190, 120, (0.20, 0.42, 0.62), 3602, lw=2.4)
    oc.client(k, xs[5], floor, 0.9, look=(-1, 0.8), targets=[(xs[5] - 120, lid_y - 4), (xs[5] - 76, lid_y - 6)])
    c.set_source_rgb(*INK); c.set_line_width(2.4)
    for dx in (-140, -100, -60):                                                        # the impact, at his hands
        c.move_to(xs[5] + dx, lid_y - 26); c.line_to(xs[5] + dx + 6, lid_y - 40); c.stroke()
    client(k, xs[6], floor, 0.9, "stand", "stare", look=(-1, 0))
    oc.rag(k, xs[6] + 70, floor - 250, 1.6)
    c.save(); c.translate(560, 2540); c.rotate(math.pi / 2)                                # lying, in profile, face up
    rect(k, 44, -420, 18, 400, (0.80, 0.16, 0.14), 3603, lw=2)                             # the creeper's board under his back
    for wy in (-390, -40):
        ellipse(k, 70, wy, 8, 8, (0.30, 0.30, 0.32), 3604 + wy, shadow=False, lw=1.6)
    profile(k, 0, 0, 0.9, facing=-1, look_up=0.0, face="bored")
    c.restore()
    for x, n in zip(xs, ("(lying: below, in profile)", "sat on the creeper (1.3)", "bent into the engine (2.2)", "the watch (2.5)",
                          "phone held out (2.8b)", "the slam (2.8d)", "standing, the stare")):
        _label(c, n, x + (40 if n.startswith("lying") else 0), floor + 60, 15)
    # 4. silhouette
    _label(c, "4  Silhouette (the rag and the knotted sleeves read in black)", 40, 1880, 22, center=False)
    s2 = cairo.ImageSurface(cairo.FORMAT_ARGB32, 400, 420)
    c2 = cairo.Context(s2); client(Ctx(c2, 0), 200, 400, 0.9, "stand", "bored")
    c.set_source_rgb(0, 0, 0); c.save(); c.translate(80, 1900); c.mask_surface(s2, 0, 0); c.restore()
    c.save(); c.translate(480, 1900); c.scale(0.5, 0.5); c.set_source_rgb(0, 0, 0); c.mask_surface(s2, 0, 0); c.restore()
    _label(c, "at half size", 580, 2150, 14)
    _label(c, "5  The profile (true side view, for 2.2 and 0.5/0.9)", 1100, 1880, 22, center=False)
    profile(k, 1250, 2300, 1.0, facing=-1)
    profile(k, 1500, 2300, 1.0, facing=1, face="stare")
    profile(k, 1800, 2300, 1.0, facing=-1, lean=0.75, hands=[(1680, 2180), (1700, 2190)])
    for x_, n_ in ((1250, "facing left"), (1500, "facing right, stare"), (1800, "into the engine")):
        _label(c, n_, x_, 2340, 15)
    _label(c, "lying on the creeper, face up (0.5 / 0.9), whole", 790, 2650, 15)
    surf.write_to_png(out)
    print("wrote", out)


if __name__ == "__main__":
    sheet(*sys.argv[1:])
