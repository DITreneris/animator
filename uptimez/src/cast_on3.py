"""OFFICE NOIR 3: the corner and the ring, v2 (Tomas, 19 Nov, /grill-me; v2 after the outside review, "Proceed").
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
import kit
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
APRON, APRON_D = (0.93, 0.92, 0.88), (0.70, 0.69, 0.66)
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


def pam_corner(k, x, feet, s=1.0, pose="p_stand", face="neutral", look=(0, 0), seed=40, towel=True, tape=None,
               sponge_=None, watch=None):
    """tape / sponge_: None = by pose ("p_tape" holds the roll, "p_sponge" the sponge).
    watch: "chest" (hanging on its cord), "hand" (held up in her screen-left hand); None = by pose ("p_watch": hand)."""
    if watch is None:
        watch = "hand" if pose == "p_watch" else "chest"
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
            c.rectangle(-17, HEM + 6, 34, 24); c.stroke()
            if watch == "chest":
                c.set_source_rgb(*INK); c.set_line_width(1.8)                                # the stopwatch, on its cord
                c.new_path(); c.move_to(-13, bt + 2); c.line_to(-2, bt + 62); c.move_to(13, bt + 2); c.line_to(2, bt + 62); c.stroke()
                rect(k_, -3, bt + 56, 6, 8, STEEL, seed_ + 70, shadow=False, lw=1.2)
                ellipse(k_, 0, bt + 76, 15, 15, CHROME, seed_ + 71, shadow=False, lw=2)
                ellipse(k_, 0, bt + 76, 10.5, 10.5, (0.98, 0.98, 0.96), seed_ + 72, shadow=False, lw=1.2)
                c.set_source_rgb(*INK); c.set_line_width(1.6); c.set_line_cap(1)
                c.new_path(); c.move_to(0, bt + 76); c.line_to(0, bt + 67.5); c.move_to(0, bt + 76); c.line_to(6, bt + 78.5); c.stroke()
                c.set_line_cap(0)
            else:                                                                        # only the cord, round her neck
                c.set_source_rgb(*INK); c.set_line_width(1.8)
                c.new_path(); c.move_to(-13, bt + 2); c.line_to(-17, bt + 20); c.move_to(13, bt + 2); c.line_to(-10, bt + 26); c.stroke()
            if towel:                                                                    # over her screen-right shoulder
                cut(k_, [(14, bt - 8), (48, bt - 4), (54, bt + 74), (40, bt + 82), (22, bt + 72)], TOWEL, shadow=False, lw=2.2)
                c.set_source_rgb(*TOWEL_SHADE); c.set_line_width(2.0)
                c.new_path(); c.move_to(25, bt + 56); c.line_to(51, bt + 60); c.stroke()
                c.new_path(); c.move_to(26, bt + 64); c.line_to(51, bt + 68); c.stroke()
        return hook
    with n2._swap((pn, "_costume", costume), (pn, "HOOP_GOLD", FRAME)):
        o = pn.pam_noir(k, x, feet, s, a, face, look, roll=False, seed=seed)
    hx, hy = o["head"]
    n2.flat_cap(k, hx, hy - 30 * s, s * 1.02, seed + 60)
    c = k.c
    c.save(); c.translate(hx + 47 * s, hy - 8 * s); c.rotate(-0.9); c.scale(s, s)             # the cotton bud, behind her ear
    c.set_source_rgb(*INK); c.set_line_width(4.4); c.set_line_cap(1); c.new_path(); c.move_to(-14, 0); c.line_to(14, 0); c.stroke()
    c.set_source_rgb(1, 1, 1); c.set_line_width(2.2); c.new_path(); c.move_to(-14, 0); c.line_to(14, 0); c.stroke(); c.set_line_cap(0)
    ellipse(k, 15, 0, 4.2, 3.6, (1, 1, 1), seed + 63, shadow=False, lw=1.2)
    c.restore()
    (lx, ly), (rx, ry) = o["hands"]
    if tape if tape is not None else pose == "p_tape":
        tape_roll(k, rx + 4 * s, ry - 2 * s, s, strip=40, ang=math.pi + 0.15, seed=seed + 64)
    if sponge_ if sponge_ is not None else pose == "p_sponge":
        sponge(k, lx, ly - 4 * s, s * 1.15, seed=seed + 66)
    if watch == "hand":                                                                  # v2: held up, face to us
        wx, wy = lx, ly - 23 * s
        c.set_source_rgb(*INK); c.set_line_width(1.8 * s); c.new_path()
        c.move_to(x - 17 * s, feet + (BT + 20) * s); c.curve_to(x - 30 * s, feet + (BT + 52) * s, wx + 20 * s, wy + 44 * s, wx + 3 * s, wy + 16 * s)
        c.move_to(x - 10 * s, feet + (BT + 26) * s); c.curve_to(x - 22 * s, feet + (BT + 60) * s, wx + 30 * s, wy + 50 * s, wx + 8 * s, wy + 14 * s)
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


def referee(k, x, feet, s=1.0, pose="ref_stand", look=(-0.6, 0.0), brow=False, count=3, seed=700):
    with n2._swap((cb, "M_SHIRT", n2.WHITE_JACKET), (cb, "M_SHIRT_DARK", n2.WHITE_SHADE), (cb, "M_JEANS", (0.10, 0.10, 0.12)),
                  (cb, "M_JEANS_DARK", (0.05, 0.05, 0.06)), (cb, "M_BELT", (0.08, 0.08, 0.09)), (cb, "M_BOOT", (0.07, 0.07, 0.08)),
                  (cb, "_macho_face", n2._clean_face(cb._macho_face))):
        o = cb.macho(k, x, feet, s, pose, "plain", look=look, badge=False, seed=seed)
    c = k.c
    c.save(); c.translate(x, feet); c.scale(s, s)
    bt = cb.M_BT                                           # v2: shade where sleeve meets chest, and under the chest
    for sx in (-1, 1):
        c.new_path(); c.move_to(sx * 61, bt + 4); c.curve_to(sx * 54, bt + 30, sx * 58, bt + 56, sx * 78, bt + 62)
        c.line_to(sx * 70, bt + 84); c.curve_to(sx * 46, bt + 70, sx * 44, bt + 30, sx * 52, bt + 2); c.close_path()
        c.set_source_rgb(*REF_SHADE); c.fill()
        c.set_source_rgb(*INK); c.set_line_width(2.2); c.set_line_cap(1); c.new_path()
        c.move_to(sx * 61, bt + 4); c.curve_to(sx * 54, bt + 30, sx * 58, bt + 56, sx * 78, bt + 62); c.stroke()
        c.set_source_rgb(*REF_SHADE); c.set_line_width(5.0); c.new_path()
        c.move_to(sx * 8, bt + 86); c.curve_to(sx * 26, bt + 103, sx * 62, bt + 99, sx * 77, bt + 68); c.stroke(); c.set_line_cap(0)
    by = cb.M_BT + 6                                       # the bow tie
    for sx in (-1, 1):
        cut(k, [(0, by), (sx * 15, by - 8), (sx * 15, by + 8)], (0.07, 0.07, 0.08), shadow=False, lw=1.6)
    ellipse(k, 0, by, 3.6, 4.4, (0.07, 0.07, 0.08), seed + 40, shadow=False, lw=1.2)
    c.restore()
    hx, hy = o["head"]
    if brow:                                               # v3: the hairline lifts over that eye, and the brow with it
        c.save(); c.translate(hx, hy); c.scale(s, s)
        B = n2.BROW_Y
        c.new_path(); c.move_to(-10, B - 7); c.line_to(-11, B - 16.5); c.curve_to(-3, B - 21, 8, B - 27, 20, B - 27); c.curve_to(30, B - 26.5, 35, B - 22, 38, B - 15); c.line_to(41, B - 2); c.close_path()
        c.set_source_rgb(*cb.M_SKIN); c.fill()
        ellipse(k, 20, B - 1, 17, 8, cb.M_SKIN, seed + 41, shadow=False, outline=False)
        ellipse(k, 33, B + 2, 7, 5, cb.M_SKIN, seed + 43, shadow=False, outline=False)
        c.set_source_rgb(*INK); c.set_line_width(2.4); c.set_line_cap(1); c.new_path()
        c.move_to(-11, B - 16.5); c.curve_to(-3, B - 21, 8, B - 27, 20, B - 27); c.curve_to(30, B - 26.5, 35, B - 22, 38, B - 15); c.stroke()
        c.set_source_rgb(*cb.M_HAIR); c.set_line_width(7.0)
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
