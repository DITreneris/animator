"""OFFICE NOIR 3: the corner and the ring, v2 (Tomas, 19 Nov, /grill-me; v2 after the outside review, "Proceed").
v6 (Tomas, "Improve", on the weak points of v5; cast_on3_v5.py is v5, pinned):
  - Pam's apron has a pale hem band and pale pocket stitching, so it parts from her dark skirt in the dream's look.
  - the Referee's sleeves and shoulder caps are a light grey, his chest white: two tones, so the arm parts from the body.
v5 (Tomas, /grill-me, 19 Nov; cast_on3_v4.py is v4, pinned). What he picked, nothing else:
  - Pam reads as corner, not office: sleeves rolled to the elbow, a darker work apron with stains, the towel round
    her neck. The cotton bud and the bead chain are gone (cap, towel, stopwatch stay). Her glasses sit lower and her
    face is drawn 13% larger about the eye line, so her eyes are clear of the frames. stance="work" (the default for
    "p_tape" and "p_pull"): she leans in and her knees are bent. reach() makes a pose from two points on the screen.
  - the Referee: no balloon shoulders. A shirt sleeve to the elbow, rolled, with a cuff band; the forearm bare.
v4 (Tomas, "Improve", on the weak points of v3; cast_on3_v3.py is v3, pinned):
  - the Referee's hairline is higher in every drawing (one smooth line, a taller forehead), so his hair no longer
    moves when the eyebrow does. brow=True moves the brow and nothing else.
v3 (Tomas, "Improve", on the weak points of v2; cast_on3_v2.py is v2, pinned):
  - the Referee's eyebrow has room: with brow=True his hairline lifts over that eye, so the brow goes about twice
    as high as in v2, and the other brow is left alone again (one eyebrow, as the rule says).
  - his idle hands hang relaxed: shorter fingers, close together (they looked like rakes).
  - Pam's stopwatch on her chest is a fifth larger, same centre, same cord.
  - "ref_break": the palm is up, fingers to the ceiling (it drooped).
v2 (cast_on3_v1.py is v1, pinned):
  - the Referee: a grey shade where each sleeve meets the chest (they were one white shape in the dream's look);
    his eyebrow is thicker and arched, and the other brow comes down flat, so the pair reads as one cocked
    brow; his idle hands are open, with fingers (a ball fist is the shape of the Client's gloves).
  - Pam: her frames are dark for this special (FRAME; gold frames went pale grey on her skin in the dream's look);
    watch="hand" and the pose "p_watch": the stopwatch held up in her hand, thumb on the crown, the cord still
    round her neck. That is its job: she starts it on the bell (5.2) and holds it up through the count (5.6).
    Her eyes, her cap and the cord's length are as in v1.
  pam_corner()  Pam as the Client's cutman. Office Noir 2's sweeper (pam_on's figure, the pale apron, the flat cap)
                without the broom, and what Tomas picked: a towel on her shoulder, a cotton bud behind her ear, a
                stopwatch on a cord, a bucket and a sponge; the roll of tape is the script's. Nothing on her is red.
                Poses: "p_stand", "p_tape" (both hands up at his brow, the roll in one), "p_pull" (both hands on his
                robe), "p_sponge" (the sponge held up over him).
  referee()     The Bartender of Office Noir 2 (cand_bc's macho, clean-shaven, slicked hair) without his glass:
                a white shirt, sleeves short on bare forearms, a black bow tie, dark trousers. Bare hands, the only
                ones in the ring. Poses: "ref_stand", "ref_bell" (one arm up, about to drop), "ref_count" (an arm out
                and down, fingers up: count=1..5), "ref_break" (a bare palm out to screen left). brow=True: his one
                eyebrow. His face does nothing else.
  bucket(), sponge(), tape_roll()   the corner's props.
noir2_cast, pam_on and cand_bc draw exactly as before."""
import math
import inspect
import kit
import pam_ss as ps
import noir2_cast as n2
import pam_on as pn
import cand_bc as cb
from kit import INK, cut, rect, ellipse

TOWEL = (0.97, 0.97, 0.95)
TOWEL_SHADE = (0.72, 0.74, 0.78)
CHROME = (0.86, 0.87, 0.90)
STEEL = (0.52, 0.54, 0.60)
TAPE = (0.98, 0.97, 0.94)
SPONGE = (0.88, 0.80, 0.52)
APRON, APRON_D = (0.31, 0.30, 0.28), (0.17, 0.17, 0.17)     # v5: a work apron, darker than the hall behind her
STAIN = (0.21, 0.20, 0.19)
HEM_BAND = (0.74, 0.72, 0.66)                              # v6
SLEEVE = (0.84, 0.84, 0.86)                                # v6: the Referee's sleeves, a tone under his chest
WORK = (-6.0, 12)                                          # v5: the working stance: lean (degrees), drop (units)
FRAME = (0.30, 0.27, 0.24)                                 # v2: her frames, dark in the dream's look
REF_SHADE = (0.70, 0.70, 0.72)                             # v2: under the Referee's sleeves
BT, HY, HEM = pn.BT, pn.HY, pn.HEM
_ik = pn.pm.ik
P_POSES = {
    "p_stand": _ik(-1, -34, BT + 92) + _ik(1, 30, BT + 92),
    "p_tape": _ik(-1, -88, BT + 6) + _ik(1, -46, BT + 34),     # both hands out to him, below her own chin
    "p_pull": _ik(-1, -84, BT + 34) + _ik(1, -40, BT + 46),
    "p_sponge": _ik(-1, -74, HY - 30) + _ik(1, 30, BT + 92),
    "p_watch": _ik(-1, -94, BT + 30) + _ik(1, 30, BT + 92),    # v2: the stopwatch held up, beside her shoulder
}
cb.POSES_MACHO.update({                                    # new names only
    "ref_stand": (-11, 4, 11, -4),
    "ref_bell": (-11, 4) + cb._m_ik(1, 132, cb.M_BT - 40),
    "ref_count": (-11, 4) + cb._m_ik(1, 150, cb.M_BT + 96),
    "ref_break": cb._m_ik(-1, -176, cb.M_BT + 64) + (11, -4),
})


def tape_roll(k, x, y, s=1.0, strip=0.0, ang=0.0, seed=0):
    """A roll of white tape; strip > 0: that many units pulled off it, away at ang."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    if strip:
        c.save(); c.rotate(ang)
        cut(k, [(8, -7), (8 + strip, -6), (8 + strip, 5), (8, 7)], TAPE, shadow=False, lw=1.6)
        c.restore()
    ellipse(k, 0, 0, 14, 14, TAPE, seed, shadow=False, lw=2)
    ellipse(k, 0, 0, 6, 6, (0.30, 0.30, 0.34), seed + 1, shadow=False, lw=1.4)
    c.restore()


def sponge(k, x, y, s=1.0, drip=True, seed=0):
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    cut(k, [(-17, -10), (15, -12), (18, 9), (-15, 11)], SPONGE, shadow=False, lw=2)
    c.set_source_rgba(0.45, 0.38, 0.20, 0.8)
    for dx, dy in ((-8, -3), (3, 2), (9, -5), (-2, 5)):
        c.new_path(); c.arc(dx, dy, 2.2, 0, 2 * math.pi); c.fill()
    if drip:
        c.set_source_rgb(0.80, 0.90, 0.98)
        for dx, dy in ((-8, 20), (4, 30), (10, 18)):
            c.new_path(); c.move_to(dx, dy - 7); c.curve_to(dx + 5, dy, dx + 3, dy + 5, dx, dy + 5)
            c.curve_to(dx - 3, dy + 5, dx - 5, dy, dx, dy - 7); c.fill_preserve()
            c.set_source_rgb(*INK); c.set_line_width(1.2); c.stroke(); c.set_source_rgb(0.80, 0.90, 0.98)
    c.restore()


def bucket(k, x, y, s=1.0, seed=0):
    """A tin bucket of water, a sponge on its rim. (x, y): the middle of its base."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    c.set_source_rgb(*INK); c.set_line_width(4.6); c.new_path(); c.arc(0, -44, 26, math.pi, 2 * math.pi); c.stroke()
    c.set_source_rgb(*STEEL); c.set_line_width(2.4); c.new_path(); c.arc(0, -44, 26, math.pi, 2 * math.pi); c.stroke()
    cut(k, [(-26, -44), (26, -44), (20, 0), (-20, 0)], CHROME, lw=2.2)
    ellipse(k, 0, -44, 26, 7, (0.70, 0.84, 0.94), seed, shadow=False, lw=2)
    c.set_source_rgb(*STEEL); c.set_line_width(1.8)
    c.new_path(); c.move_to(-24, -30); c.line_to(24, -30); c.stroke()
    c.new_path(); c.move_to(-21, -10); c.line_to(21, -10); c.stroke()
    c.restore()
    sponge(k, x + 18 * s, y - 50 * s, s * 0.8, drip=False, seed=seed + 3)


def _arm_rolled(k, sx, sy, a1, a2, col, skin, seed, ln=48, w=17):
    """kit.arm with the sleeve rolled to the elbow: the forearm bare, a band of sleeve above the joint."""
    d = lambda a_: (math.sin(math.radians(a_)), math.cos(math.radians(a_)))
    ex, ey = sx + d(a1)[0] * ln, sy + d(a1)[1] * ln
    hx, hy = ex + d(a1 + a2)[0] * ln, ey + d(a1 + a2)[1] * ln
    for (ax, ay, bx, by, cl, ww) in ((ex, ey, hx, hy, skin, w - 3), (sx, sy, ex, ey, col, w)):
        ang = math.atan2(by - ay, bx - ax)
        nx, ny = -math.sin(ang) * ww / 2, math.cos(ang) * ww / 2
        cut(k, [(ax + nx, ay + ny), (bx + nx, by + ny), (bx - nx, by - ny), (ax - nx, ay - ny)], cl, shadow=False, lw=2)
    ang = math.atan2(ey - sy, ex - sx)
    ux, uy, nx, ny = math.cos(ang), math.sin(ang), -math.sin(ang) * (w / 2 + 3), math.cos(ang) * (w / 2 + 3)
    cut(k, [(ex + nx - ux * 9, ey + ny - uy * 9), (ex + nx + ux * 2, ey + ny + uy * 2), (ex - nx + ux * 2, ey - ny + uy * 2),
            (ex - nx - ux * 9, ey - ny - uy * 9)], tuple(min(1, v + 0.08) for v in col), shadow=False, lw=1.8)
    ellipse(k, hx, hy, w * 0.6, w * 0.6, skin, seed, shadow=False, lw=2)
    return hx, hy


def _legs_work(drop, lean=0.0):
    """pam_on's legs with the knees bent: the body is drawn `drop` lower, the feet stay on the floor, apart. The legs
    are turned back by the lean about the hips, so she bends from the hip and her shoes stay flat."""
    def legs(k, seed, stance=1.0):
        c = k.c
        c.save(); c.translate(0, -92); c.rotate(-math.radians(lean)); c.translate(0, 92)
        for o in (-1, 1):
            kx, ax = o * 12, o * 23
            cut(k, [(kx - 7, -86), (kx + 7, -86), (ax + 6, -14 - drop), (ax - 6, -14 - drop)], pn.STOCKING, shadow=False, lw=1.8)
            cut(k, [(ax - 7, -16 - drop), (ax + 7, -16 - drop), (ax + 7 + o * 8, -2 - drop), (ax + 7 + o * 8, -drop),
                    (ax - 7, -drop)], pn.PUMP, shadow=False, lw=1.6)
        c.restore()
        cut(k, [(-40, HEM - 8), (40, HEM - 8), (38, -50), (-38, -50)], pn.SKIRT, lw=2.2)
    return legs


def _big_face(real, e=1.13):
    """pam_ss._wrapped_faces, the whole face drawn e times larger about the eye line."""
    def wrapped(orig, lips, gstate):
        mf0 = real(orig, lips, gstate)

        def mf(inner, g, mouth):
            fd = mf0(inner, g, mouth)

            def face_draw(k, x, y, face, look, glasses=False, seed=0):
                c = k.c
                c.save(); c.translate(x, y); c.scale(e, e); c.translate(-x, -y)
                try:
                    fd(k, x, y, face, look, glasses=glasses, seed=seed)
                finally:
                    c.restore()
            return face_draw
        return mf
    return wrapped


def _stance(pose, stance):
    if stance is None:
        stance = "work" if pose in ("p_tape", "p_pull") else "stand"
    return WORK if stance == "work" else (0.0, 0) if stance == "stand" else stance


def reach(x, feet, s, left, right, stance="work"):
    """A pose with her hands at two points of the frame (left: her screen-left hand), in the given stance."""
    lean, drop = _stance(None, stance)
    th = -math.radians(lean)
    out = ()
    for side, (px_, py_) in ((-1, left), (1, right)):
        dx, dy = px_ - x, py_ - (feet + drop * s)
        out += _ik(side, (dx * math.cos(th) - dy * math.sin(th)) / s, (dx * math.sin(th) + dy * math.cos(th)) / s)
    return out


def pam_corner(k, x, feet, s=1.0, pose="p_stand", face="neutral", look=(0, 0), seed=40, towel=True, tape=None,
               sponge_=None, watch=None, stance=None):
    """tape / sponge_: None = by pose ("p_tape" holds the roll, "p_sponge" the sponge).
    watch: "chest" (hanging on its cord), "hand" (held up in her screen-left hand); None = by pose ("p_watch": hand).
    stance: "stand", "work" (leaning in, knees bent), or (lean degrees, drop); None = by pose (tape, pull: work)."""
    if watch is None:
        watch = "hand" if pose == "p_watch" else "chest"
    lean, drop = _stance(pose, stance)
    a = P_POSES[pose] if isinstance(pose, str) else pose
    orig = pn._costume

    def costume(badge=True):
        base = orig(badge)

        def hook(k_, name_, p_, bt, seed_):
            base(k_, name_, p_, bt, seed_)
            c = k_.c
            cut(k_, [(-21, bt + 40), (21, bt + 40), (24, HEM - 12), (44, HEM - 8), (42, -34), (-42, -34), (-44, HEM - 8),
                     (-24, HEM - 12)], APRON, shadow=False, lw=2)
            c.set_source_rgb(*INK); c.set_line_width(2.0)
            for sx in (-1, 1):
                c.move_to(sx * 21, bt + 40); c.line_to(sx * 30, bt + 4); c.stroke()
            c.set_source_rgb(*APRON_D); c.set_line_width(1.6)
            c.move_to(-44, HEM - 8); c.line_to(44, HEM - 8); c.stroke()
            cut(k_, [(-44, HEM - 19), (44, HEM - 19), (44, HEM - 9), (-44, HEM - 9)], HEM_BAND, shadow=False, lw=1.8)   # v6: a pale hem
            c.set_source_rgb(*HEM_BAND); c.set_line_width(2.0); c.set_dash([5, 3])
            c.rectangle(-15, HEM - 50, 30, 22); c.stroke(); c.set_dash([])
            c.set_source_rgb(*STAIN)                                                     # stains: it has been used
            for sx_, sy_, rx_, ry_, rot in ((-14, bt + 62, 7, 4, 0.5), (15, bt + 96, 9, 5, -0.4), (-26, HEM + 22, 8, 5, 0.2),
                                            (27, HEM + 44, 6, 9, 0.1)):
                c.save(); c.translate(sx_, sy_); c.rotate(rot); c.scale(rx_, ry_); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
            c.set_source_rgba(0.62, 0.61, 0.58, 0.9); c.set_line_width(2.4); c.set_line_cap(1)
            c.move_to(-34, HEM + 2); c.line_to(-22, HEM + 10); c.move_to(20, bt + 70); c.line_to(30, bt + 76); c.stroke(); c.set_line_cap(0)
            if towel:                                                                    # v5: round her neck, two ends down
                for sx, ln in ((-1, 56), (1, 66)):
                    cut(k_, [(sx * 9, bt - 10), (sx * 33, bt - 6), (sx * 31, bt + ln), (sx * 11, bt + ln + 4)], TOWEL,
                        shadow=False, lw=2.2)
                    c.set_source_rgb(*TOWEL_SHADE); c.set_line_width(2.0)
                    for dy in (12, 20):
                        c.new_path(); c.move_to(sx * 12, bt + ln - dy + 2); c.line_to(sx * 30, bt + ln - dy); c.stroke()
            if watch == "chest":
                c.set_source_rgb(*INK); c.set_line_width(1.8)                            # the stopwatch, on its cord
                c.new_path(); c.move_to(-8, bt + 30); c.line_to(-2, bt + 62); c.move_to(8, bt + 30); c.line_to(2, bt + 62); c.stroke()
                rect(k_, -3, bt + 56, 6, 8, STEEL, seed_ + 70, shadow=False, lw=1.2)
                ellipse(k_, 0, bt + 76, 15, 15, CHROME, seed_ + 71, shadow=False, lw=2)
                ellipse(k_, 0, bt + 76, 10.5, 10.5, (0.98, 0.98, 0.96), seed_ + 72, shadow=False, lw=1.2)
                c.set_source_rgb(*INK); c.set_line_width(1.6); c.set_line_cap(1)
                c.new_path(); c.move_to(0, bt + 76); c.line_to(0, bt + 67.5); c.move_to(0, bt + 76); c.line_to(6, bt + 78.5); c.stroke()
                c.set_line_cap(0)
        return hook
    swaps = [(pn, "_costume", costume), (kit, "arm", _arm_rolled), (ps, "_wrapped_faces", _big_face(ps._wrapped_faces))]
    if drop:
        swaps.append((pn, "_legs", _legs_work(drop, lean)))
    with n2._swap(*swaps):
        o = pn.pam_noir(k, x, feet + drop * s, s, a, face, look, glasses="off", roll=False, seed=seed, lean=lean)
    hx, hy = o["head"]
    c = k.c
    c.save(); c.translate(hx, hy); c.rotate(math.radians(lean)); c.scale(s, s)
    n2.flat_cap(k, 0, -30, 1.02, seed + 60)
    top = 15                                                                             # v5: her glasses, lower, no chain
    for col, lw in ((INK, 5.0), (FRAME, 2.8)):
        c.set_source_rgb(*col); c.set_line_width(lw); c.set_line_cap(1)
        for sx in (-17, 17):
            pn.pm.half_moon(c, sx, top, 25, 10)
            if col is INK:
                c.set_source_rgba(0.93, 0.97, 1.0, 0.45); c.fill_preserve(); c.set_source_rgb(*col)
            c.stroke()
        for sx in (-1, 1):
            c.move_to(sx * 29, top + 1); c.line_to(sx * 43, top - 3); c.stroke()
        c.move_to(-5, top + 1); c.curve_to(-2, top - 3, 2, top - 3, 5, top + 1); c.stroke()
    c.set_line_cap(0)
    c.restore()
    (lx, ly), (rx, ry) = o["hands"]
    if tape if tape is not None else pose == "p_tape":
        tape_roll(k, rx + 4 * s, ry - 2 * s, s, strip=40, ang=math.pi + 0.15, seed=seed + 64)
    if sponge_ if sponge_ is not None else pose == "p_sponge":
        sponge(k, lx, ly - 4 * s, s * 1.15, seed=seed + 66)
    if watch == "hand":                                                                  # held up, face to us
        wx, wy = lx, ly - 23 * s
        c.set_source_rgb(*INK); c.set_line_width(1.8 * s); c.new_path()
        c.move_to(x - 12 * s, feet + (BT + 50) * s); c.curve_to(x - 30 * s, feet + (BT + 70) * s, wx + 20 * s, wy + 44 * s, wx + 3 * s, wy + 16 * s)
        c.move_to(x - 4 * s, feet + (BT + 52) * s); c.curve_to(x - 22 * s, feet + (BT + 78) * s, wx + 30 * s, wy + 50 * s, wx + 8 * s, wy + 14 * s)
        c.stroke()
        rect(k, wx - 4 * s, wy - 26 * s, 8 * s, 10 * s, STEEL, seed + 70, shadow=False, lw=1.4 * s)
        ellipse(k, wx, wy, 17 * s, 17 * s, CHROME, seed + 71, shadow=False, lw=2.2 * s)
        ellipse(k, wx, wy, 12 * s, 12 * s, (0.98, 0.98, 0.96), seed + 72, shadow=False, lw=1.4 * s)
        c.set_source_rgb(*INK); c.set_line_width(2.2 * s); c.set_line_cap(1); c.new_path()
        c.move_to(wx, wy); c.line_to(wx, wy - 9.5 * s); c.move_to(wx, wy); c.line_to(wx + 7 * s, wy + 3 * s); c.stroke(); c.set_line_cap(0)
    for hx_, hy_ in ((lx, ly), (rx, ry)):
        ellipse(k, hx_, hy_, 9 * s, 9 * s, pn.ps.SKIN, seed + 62 + int(hx_), shadow=False, lw=1.8 * s)
    if watch == "hand":                                                                  # the click, off the crown
        c.set_source_rgb(*INK); c.set_line_width(1.8 * s); c.set_line_cap(1); c.new_path()
        for dx, dy in ((-13, -9), (0, -13), (13, -9)):
            c.move_to(wx + dx * 0.9 * s, wy - 29 * s + dy * 0.5 * s); c.line_to(wx + dx * 1.5 * s, wy - 29 * s + dy * 1.1 * s)
        c.stroke(); c.set_line_cap(0)
    return o


def _open_hand(k, x, y, s, ang, fingers, seed, thumb=True, relax=False):
    """A bare hand at (x, y), its fingers along ang; fingers: how many are up (0..4), the rest curled."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    for i in range(4):
        fy = (-7.5 + i * 5) if relax else (-10.5 + i * 7)
        ln = (13 + (2 if i in (1, 2) else 0) if relax else 24) if i < fingers else 7
        c.set_source_rgb(*INK); c.set_line_width(8.6); c.set_line_cap(1)
        c.new_path(); c.move_to(6, fy); c.line_to(6 + ln, fy); c.stroke()
        c.set_source_rgb(*cb.M_SKIN); c.set_line_width(5.6); c.new_path(); c.move_to(6, fy); c.line_to(6 + ln, fy); c.stroke()
    if thumb:
        c.set_source_rgb(*INK); c.set_line_width(8.6); c.new_path(); c.move_to(-2, -12); c.line_to(6, -24); c.stroke()
        c.set_source_rgb(*cb.M_SKIN); c.set_line_width(5.6); c.new_path(); c.move_to(-2, -12); c.line_to(6, -24); c.stroke()
    c.set_line_cap(0)
    ellipse(k, 0, 0, 14, 14, cb.M_SKIN, seed, shadow=False, lw=2)
    c.restore()


def _macho_ref():
    """cand_bc.macho, its source changed in two places and run in a copy of cand_bc's names (cand_bc itself draws as
    before): the shoulder is a small cap, not a ball, and the arm is a shirt sleeve to the elbow with a rolled cuff."""
    src = inspect.getsource(cb.macho)
    for old, new in (("bulge=1.34, sleeve=0.42", "bulge=1.08, cuff=(M_SHIRT_DARK, 11)"),
                     ("bt + 22, 27, 24, M_SHIRT", "bt + 24, 19, 15, M_SLEEVE"),
                     ("M_LN1, M_LN2, 46, 31, M_SHIRT", "M_LN1, M_LN2, 40, 31, M_SLEEVE"),
                     ("c.set_source_rgb(*M_SHIRT); c.rectangle(min(side * 58, side * 86), bt + 12, 28, 34); c.fill()",
                      "pass")):                               # v6: the seam between sleeve and chest stays drawn
        assert src.count(old) == 1, old
        src = src.replace(old, new)
    ns = dict(vars(cb))
    ns.update(M_SLEEVE=SLEEVE, M_SHIRT=n2.WHITE_JACKET, M_SHIRT_DARK=(0.66, 0.66, 0.69), M_JEANS=(0.10, 0.10, 0.12), M_JEANS_DARK=(0.05, 0.05, 0.06),
              M_BELT=(0.08, 0.08, 0.09), M_BOOT=(0.07, 0.07, 0.08), _macho_face=n2._clean_face(cb._macho_face))
    exec(src, ns)
    return ns["macho"]


_MACHO = _macho_ref()


def referee(k, x, feet, s=1.0, pose="ref_stand", look=(-0.6, 0.0), brow=False, count=3, seed=700):
    o = _MACHO(k, x, feet, s, pose, "plain", look=look, badge=False, seed=seed)
    c = k.c
    c.save(); c.translate(x, feet); c.scale(s, s)
    bt = cb.M_BT                                           # v2: shade where sleeve meets chest, and under the chest
    for sx in (-1, 1):
        c.set_source_rgb(*REF_SHADE); c.set_line_width(3.0); c.set_line_cap(1); c.new_path()     # v5: one fold under the chest
        c.move_to(sx * 66, bt + 30); c.curve_to(sx * 62, bt + 44, sx * 64, bt + 56, sx * 72, bt + 64)        # and one at the armpit
        c.move_to(sx * 8, bt + 86); c.curve_to(sx * 26, bt + 103, sx * 62, bt + 99, sx * 77, bt + 68); c.stroke(); c.set_line_cap(0)
    by = cb.M_BT + 6                                       # the bow tie
    for sx in (-1, 1):
        cut(k, [(0, by), (sx * 15, by - 8), (sx * 15, by + 8)], (0.07, 0.07, 0.08), shadow=False, lw=1.6)
    ellipse(k, 0, by, 3.6, 4.4, (0.07, 0.07, 0.08), seed + 40, shadow=False, lw=1.2)
    c.restore()
    hx, hy = o["head"]
    B = n2.BROW_Y                                          # v4: his hairline, higher, the same in every drawing
    c.save(); c.translate(hx, hy); c.scale(s, s)

    def hairline():
        c.new_path(); c.move_to(-40, B - 9); c.curve_to(-35, B - 21, -23, B - 27, -9, B - 27)
        c.curve_to(1, B - 26.5, 10, B - 27, 20, B - 27); c.curve_to(30, B - 26.5, 35, B - 22, 38, B - 15)
    hairline(); c.line_to(41, B - 7); c.line_to(30, B - 8); c.line_to(-30, B - 8); c.close_path()
    c.set_source_rgb(*cb.M_SKIN); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(2.4); c.set_line_cap(1); hairline(); c.stroke(); c.set_line_cap(0)
    if brow:                                               # his screen-right brow, up; nothing else moves
        ellipse(k, 20, B - 1, 17, 8, cb.M_SKIN, seed + 41, shadow=False, outline=False)
        ellipse(k, 33, B + 2, 7, 5, cb.M_SKIN, seed + 43, shadow=False, outline=False)
        c.set_source_rgb(*cb.M_HAIR); c.set_line_width(7.0); c.set_line_cap(1)
        c.new_path(); c.move_to(8, B - 7); c.curve_to(13, B - 19, 25, B - 19, 32, B - 8); c.stroke()
        c.set_source_rgb(*cb.M_SKIN_DARK); c.set_line_width(1.8)                  # one crease, where it was
        c.new_path(); c.move_to(11, B - 1); c.curve_to(17, B - 4, 23, B - 4, 29, B - 1); c.stroke()
        c.set_line_cap(0)
    c.restore()
    (lx, ly), (rx, ry) = o["hands"]
    if pose == "ref_count":                                # fingers up, over the man on the canvas
        _open_hand(k, rx, ry, s, -math.pi / 2 + 0.25, min(count, 4), seed + 50, thumb=count >= 5)
    elif pose == "ref_break":                              # a flat palm, toward screen left
        _open_hand(k, lx, ly, s, -math.pi / 2 - 0.35, 4, seed + 51)       # v3: fingers up, a palm that stops
    elif pose == "ref_bell":
        _open_hand(k, rx, ry, s, -math.pi / 2, 4, seed + 52)
    if pose != "ref_break":                                # v2: the idle hands hang open
        _open_hand(k, lx, ly, s, math.pi / 2 + 0.12, 4, seed + 53, thumb=False, relax=True)
    if pose in ("ref_stand", "ref_break"):
        _open_hand(k, rx, ry, s, math.pi / 2 - 0.12, 4, seed + 54, thumb=False, relax=True)
    return o


REL_REF = 0.70                                             # the Referee beside the series' other figures, as the Bartender was
