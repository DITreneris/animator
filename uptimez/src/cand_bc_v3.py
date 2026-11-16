"""v3, pinned. v3 (cand_bc_v2.py = v2, kept), after the second audit ("a frightened child", "a friendly gym instructor"):
THE SMALL ONE reads as an adult genius, not a schoolboy: longer legs, a smaller head, a receding hairline, bags
under his eyes, stubble dots, taped glasses with one lens hanging lower, a badly knotted tie, one sweat drop instead
of three; the CV he hugs is bigger than his torso and stuffed (cv_brick(stuffed=True)); "finger" shows three fingers.
THE NICE MACHO is impossibly powerful and gentle: upper arms 35 % thicker, a deeper chest, a harder taper to the
waist, round shoulder caps, short sleeves biting into the muscle, bigger hands, friendlier (more open) eyes; new pose
"pinch": Pam's pen returned between two enormous fingertips, the little finger out.
THE BEST CANDIDATE, v2 (cand_bc_v1.py = v1, kept): the two new candidates, after the outside audit ("three
variations of nice": the silhouettes must read with the faces hidden). Both are drawn here from kit primitives (own
proportions, legs and arms), so kit.person and every earlier character are untouched.

THE SMALL ONE, 90 % nervous energy. Silhouette: hunched and uneven. A narrow head sunk between his shoulders, one
shoulder higher than the other, knock knees, pigeon toes; big round glasses sitting crooked, tiny pupils, a
clenched smile, sweat; messy sandy hair; a grey suit two sizes too big (sleeves over his hands), a crooked mustard
tie, a pencil behind his ear. Seated, his trousers ride up: two different socks. Still perfect on paper: he grips
a CV as thick as a brick. The awkwardness is posture, face and clothes first; the socks and pencil are the only
two extras. Faces: hopeful (wired, the default), proud (manic), neutral (the stare), crushed.

THE NICE MACHO, 110 % confidence, still kind. Silhouette: a huge inverted V. Shoulders 35 % wider than v1, big
upper arms, a deep chest, a narrow waist, enormous hands; a square jaw with a cleft, stubble, a dark quiff, a wide
easy grin under slightly lowered lids; a sky-blue shirt with the sleeves rolled and two buttons working hard, dark
jeans. Human, not a superhero: normal legs, no pose he would strike on purpose. He picks up Pam's pen and holds a
tiny cookie tin between his huge hands. Faces: smile (the confident grin), warm, listen, gracious.

Usage: o = small(k, x, feet, s, pose, face, look, mouth=None, cv=False, tiptoe=0, seated=False)
       o = macho(k, x, feet, s, pose, face, look, mouth=None, glint=False, tin=False, pen=False, seated=False)
Both return {"head", "hands", "top"} in canvas coordinates; pose is a name in POSES_* or (a1, a2, b1, b2) degrees
(0 = down, +90 = screen right, 180 = up), as in kit.ARM_POSES."""
import math
import kit
import iwry_mouths as im
import props_bc_v3 as props
from kit import INK, cut, rect, ellipse

# ------------------------------------------------------------------ shared
VIS_ORANGE = (0.96, 0.56, 0.14)
SWEAT = (0.62, 0.84, 0.97)


def _d(a):
    return math.sin(math.radians(a)), math.cos(math.radians(a))


def limb(k, sx, sy, a1, a2, ln1, ln2, w1, w2, col1, col2, skin, hand_r, seed, hand_first=False, cuff=None, bulge=0.0,
         hand_off=1.0, seam=None, sleeve=None):
    """A two-part arm. hand_first: the hand is drawn under the sleeve end (a sleeve that is too long), hand_off
    units past it. cuff: a rolled-sleeve band at the elbow, (colour, width). bulge > 0: the upper arm swells in
    the middle (w1 * bulge) and narrows to the elbow."""
    ex, ey = sx + _d(a1)[0] * ln1, sy + _d(a1)[1] * ln1
    hx, hy = ex + _d(a1 + a2)[0] * ln2, ey + _d(a1 + a2)[1] * ln2
    if hand_first:
        ellipse(k, hx + _d(a1 + a2)[0] * hand_off, hy + _d(a1 + a2)[1] * hand_off, hand_r, hand_r, skin, seed,
                shadow=False, lw=2)
    ang = math.atan2(hy - ey, hx - ex)
    nx, ny = -math.sin(ang) * w2 / 2, math.cos(ang) * w2 / 2
    cut(k, [(ex + nx, ey + ny), (hx + nx * 0.86, hy + ny * 0.86), (hx - nx * 0.86, hy - ny * 0.86), (ex - nx, ey - ny)],
        col2, shadow=False, lw=2)
    ang = math.atan2(ey - sy, ex - sx)
    ux, uy = math.cos(ang), math.sin(ang)
    px, py = -uy, ux
    if bulge:
        prof = ((0.0, 0.92), (0.25, bulge * 0.94), (0.5, bulge), (0.78, 0.9), (1.0, 0.72))
    else:
        prof = ((0.0, 1.0), (1.0, 1.0))
    one = [(sx + ux * ln1 * t + px * w1 / 2 * f, sy + uy * ln1 * t + py * w1 / 2 * f) for t, f in prof]
    two = [(sx + ux * ln1 * t - px * w1 / 2 * f, sy + uy * ln1 * t - py * w1 / 2 * f) for t, f in reversed(prof)]
    cut(k, one + two, skin if sleeve else col1, shadow=False, lw=2)
    if sleeve:                                                          # a short sleeve, tight over the muscle below it
        st = sleeve

        def wf(t):
            for (t0, f0), (t1, f1) in zip(prof, prof[1:]):
                if t0 <= t <= t1:
                    return f0 + (f1 - f0) * (t - t0) / (t1 - t0)
            return prof[-1][1]
        ts = [t for t, _ in prof if t < st] + [st]
        a_ = [(sx + ux * ln1 * t + px * w1 / 2 * wf(t), sy + uy * ln1 * t + py * w1 / 2 * wf(t)) for t in ts]
        b_ = [(sx + ux * ln1 * t - px * w1 / 2 * wf(t), sy + uy * ln1 * t - py * w1 / 2 * wf(t)) for t in reversed(ts)]
        cut(k, a_ + b_, col1, shadow=False, lw=2)
        hw = w1 / 2 * wf(st) - 1.5                                      # the band bites in
        bx, by = sx + ux * ln1 * st, sy + uy * ln1 * st
        cut(k, [(bx + px * hw - ux * 8, by + py * hw - uy * 8), (bx + px * hw, by + py * hw), (bx - px * hw, by - py * hw),
                (bx - px * hw - ux * 8, by - py * hw - uy * 8)], (0.80, 0.90, 0.98), shadow=False, lw=1.8)
        c = k.c                                                         # the muscle under it
        c.set_source_rgb(0.72, 0.50, 0.36); c.set_line_width(2); c.set_line_cap(1)
        q0 = (bx + ux * 5 + px * w1 * 0.12, by + uy * 5 + py * w1 * 0.12)
        q1 = (sx + ux * ln1 * 0.86 + px * w1 * 0.05, sy + uy * ln1 * 0.86 + py * w1 * 0.05)
        c.move_to(*q0); c.curve_to(q0[0] - px * w1 * 0.25, q0[1] - py * w1 * 0.25, q1[0] - px * w1 * 0.25,
                                   q1[1] - py * w1 * 0.25, *q1); c.stroke()
    if seam:                                                            # the sleeve giving up over the muscle
        skin_c, dark = seam
        c = k.c
        mx, my = sx + ux * ln1 * 0.47, sy + uy * ln1 * 0.47
        c.save(); c.translate(mx, my); c.rotate(ang)
        c.save(); c.scale(11, 3.4); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        c.set_source_rgb(*skin_c); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.3); c.stroke()
        c.set_source_rgb(*dark); c.set_line_width(1.5); c.set_line_cap(1)
        for d in (-6, 0, 6):
            c.move_to(d, -5.5); c.line_to(d, 5.5); c.stroke()
        c.restore()
    if cuff:
        col, cw = cuff
        hw = w1 / 2 * (0.72 if bulge else 1.0) + 2.5
        cut(k, [(ex + px * hw - ux * cw, ey + py * hw - uy * cw), (ex + px * hw, ey + py * hw), (ex - px * hw, ey - py * hw),
                (ex - px * hw - ux * cw, ey - py * hw - uy * cw)], col, shadow=False, lw=1.8)
    if not hand_first:
        ellipse(k, hx, hy, hand_r, hand_r, skin, seed, shadow=False, lw=2)
    return hx, hy


def ik(sx, sy, tx, ty, ln1, ln2, side):
    """Shoulder angles (a1, a2) that put the hand at (tx, ty); the elbow bends away from the body."""
    vx, vy = tx - sx, ty - sy
    D = max(abs(ln1 - ln2) + 0.5, min(math.hypot(vx, vy), ln1 + ln2 - 0.5))
    angD = math.degrees(math.atan2(vx, vy))
    al = math.degrees(math.acos((ln1 * ln1 + D * D - ln2 * ln2) / (2 * ln1 * D)))
    be = math.degrees(math.acos((ln1 * ln1 + ln2 * ln2 - D * D) / (2 * ln1 * ln2)))
    best = None
    for sg in (1, -1):
        a1 = angD + sg * al
        ex = sx + math.sin(math.radians(a1)) * ln1
        if best is None or ex * side > best[0]:
            best = (ex * side, a1, -sg * (180 - be))
    return best[1], best[2]


def visitor(k, x, y, w=30, rot=-0.06, seed=0):
    """The paper VISITOR sticker both candidates wear (no name: nobody asked)."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(rot)
    rect(k, -w / 2, -9, w, 18, (1, 1, 1), seed + 1, shadow=False, lw=1.5)
    c.set_source_rgb(*VIS_ORANGE); c.rectangle(-w / 2 + 1.2, -7.8, w - 2.4, 6.2); c.fill()
    kit.text(k, "VISITOR", 0, 3.6, w * 0.2, INK, font="Inter", bold=True)
    c.restore()


def _brow(c, x1, y1, x2, y2, w):
    c.set_source_rgb(*INK); c.set_line_width(w); c.set_line_cap(1)
    c.move_to(x1, y1); c.line_to(x2, y2); c.stroke()


def sweat_drop(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(0, -8); c.curve_to(6, 0, 5, 6, 0, 6); c.curve_to(-5, 6, -6, 0, 0, -8); c.close_path()
    c.set_source_rgb(*SWEAT); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.5); c.stroke()
    c.restore()


# ------------------------------------------------------------------ the small one
S_SKIN = (0.99, 0.85, 0.73)
S_HAIR = (0.80, 0.50, 0.22)
S_SUIT = (0.55, 0.58, 0.64)
S_SUIT_DARK = (0.40, 0.43, 0.50)
S_SHIRT = (0.98, 0.98, 0.96)
S_TIE = (0.93, 0.72, 0.18)
S_SHOE = (0.36, 0.22, 0.13)
S_PENCIL = (0.98, 0.80, 0.20)
S_L, S_T = 56, 80
S_HIP = -S_L
S_BT = S_HIP - S_T
S_HY = S_BT - 29                                     # the head sunk between his shoulders
S_SHX = 39
S_SHY = {-1: S_BT + 7, 1: S_BT + 17}                 # one shoulder up by his ear
S_LN = 30
S_TOP = S_HY - 66


def _s_ik(side, tx, ty):
    return ik(side * S_SHX, S_SHY[side], tx, ty, S_LN, S_LN, side)


POSES_SMALL = {
    "stand": (-6, -10, 6, 10),                                           # elbows in, hands toward each other
    "hug": _s_ik(-1, -28, S_BT + 78) + _s_ik(1, 31, S_BT + 54),           # both arms clamped round the CV
    "offer": (-6, -10) + _s_ik(1, 62, S_BT + 8),                          # the CV held out to the panel, on tiptoe
    "finger": (-6, -10) + _s_ik(1, 46, S_BT - 12),                        # "Three degrees.": a hand shoots up
    "sag": (-3, 2, 3, -2),                                                # crushed: arms hang
    "sit": _s_ik(-1, -20, S_BT + 64) + _s_ik(1, 20, S_BT + 66),           # hands clamped on his knees
}


def _small_face(k, y, face, look, mouth, seed):
    c = k.c
    lx, ly = look
    crushed = face == "crushed"
    gy = y + 5 + (9 if crushed else 0)
    R = 19.5
    lens = ((-20.5, 0.0), (20.5, 4.5))                                      # the frame is bent: one lens hangs lower
    c.save(); c.translate(0, gy); c.rotate(0.13 if not crushed else 0.22)   # and the glasses sit crooked
    for sx, sy in lens:
        c.set_source_rgb(1, 1, 1); c.arc(sx, sy, R, 0, 2 * math.pi); c.fill()
        c.save(); c.arc(sx, sy, R - 1, 0, 2 * math.pi); c.clip()            # bags under his eyes: he has not slept
        c.save(); c.translate(sx, sy + R * 0.92); c.scale(R * 0.85, R * 0.42); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        c.set_source_rgb(0.80, 0.71, 0.84); c.fill()
        c.set_source_rgb(0.55, 0.44, 0.62); c.set_line_width(1.6)
        c.arc(sx, sy + R * 1.5, R * 0.98, math.pi * 1.2, math.pi * 1.8); c.stroke()
        c.restore()
    pr = 5.0 if crushed else 3.3                                            # wired: pinpoint pupils
    for sx, sy in lens:
        ex, ey = sx + lx * 6, sy + ly * 6 + (3 if crushed else -1)
        ellipse(k, ex, ey, pr, pr, INK, seed + int(sx) + 1, shadow=False, outline=False)
        c.set_source_rgb(1, 1, 1); c.arc(ex - 1.1, ey - 1.3, 1.1, 0, 2 * math.pi); c.fill()
    if crushed:                                                             # heavy lids, one lower than the other
        for (sx, sy), lid in zip(lens, (0.42, 0.58)):
            c.save(); c.arc(sx, sy, R - 1, 0, 2 * math.pi); c.clip()
            c.set_source_rgb(*S_SKIN); c.rectangle(sx - R, sy - R, 2 * R, 2 * R * lid); c.fill()
            c.restore()
            _brow(c, sx - R * 0.86, sy - R + 2 * R * lid, sx + R * 0.86, sy - R + 2 * R * lid, 2.6)
    c.set_source_rgb(*INK); c.set_line_width(3.4)
    for sx, sy in lens:
        c.arc(sx, sy, R, 0, 2 * math.pi); c.stroke()
    c.set_source_rgb(0.97, 0.96, 0.90); c.rectangle(-4.5, -4, 9, 8.5); c.fill_preserve()    # tape on the bridge
    c.set_source_rgb(*INK); c.set_line_width(1.5); c.stroke()
    c.set_line_width(1); c.move_to(-1.5, -4); c.line_to(-1.5, 4.5); c.move_to(1.8, -4); c.line_to(1.8, 4.5); c.stroke()
    c.set_source_rgba(1, 1, 1, 0.75); c.set_line_width(2.4)
    for sx, sy in lens:
        c.arc(sx, sy, R - 5, math.pi * 1.1, math.pi * 1.4); c.stroke()
    c.restore()
    c.set_source_rgba(0.45, 0.28, 0.15, 0.55)                               # a day and a half of stubble
    for fx, fy in ((-15, 41), (-10, 44), (-4, 43), (3, 45), (9, 43), (15, 41), (-12, 31), (-5, 29), (4, 29), (11, 31),
                   (-19, 36), (19, 36)):
        c.arc(fx, y + fy, 1.0, 0, 2 * math.pi); c.fill()
    by = y - 24
    if face == "hopeful":                                                   # brows shot up, uneven
        _brow(c, -30, by - 3, -12, by - 8, 3.4); _brow(c, 12, by - 2, 30, by + 3, 3.4)
    elif face == "proud":
        _brow(c, -30, by - 6, -12, by - 9, 3.4); _brow(c, 12, by - 5, 30, by - 1, 3.4)
    elif crushed:
        _brow(c, -30, by + 9, -12, by - 1, 3.4); _brow(c, 12, by + 3, 30, by + 12, 3.4)
    else:
        _brow(c, -29, by - 4, -12, by - 5, 3.4); _brow(c, 12, by - 1, 29, by + 1, 3.4)
    c.set_source_rgba(0.75, 0.42, 0.25, 0.7)                                # freckles
    for fx, fy in ((-29, 30), (-24, 34), (-31, 36), (29, 34), (24, 38), (31, 40)):
        c.arc(fx, y + fy, 1.4, 0, 2 * math.pi); c.fill()
    my = y + 35
    if mouth:
        im.mouth(k, 0, my, mouth, S_SKIN, erase=(1, 1), seed=seed + 96)
        return
    c.set_source_rgb(*INK); c.set_line_width(3.2); c.set_line_cap(1); c.set_line_join(1)
    if face == "hopeful":                                                   # a clenched smile, all teeth
        c.move_to(-14, my - 5); c.curve_to(-6, my - 3, 6, my - 3, 14, my - 6)
        c.curve_to(13, my + 4, 9, my + 6, 0, my + 6); c.curve_to(-9, my + 6, -13, my + 4, -14, my - 5); c.close_path()
        c.set_source_rgb(1, 1, 1); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.4); c.stroke()
        c.set_line_width(1.3)
        for d in (-7, 0, 7):
            c.move_to(d, my - 4); c.line_to(d, my + 5.5); c.stroke()
        c.move_to(-13, my + 0.5); c.line_to(13, my); c.stroke()
    elif face == "proud":                                                   # too big, too long
        c.move_to(-16, my - 6); c.curve_to(-8, my - 4, 8, my - 4, 16, my - 7)
        c.curve_to(13, my + 11, -12, my + 11, -16, my - 6); c.close_path()
        c.set_source_rgb(0.40, 0.07, 0.08); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.6); c.stroke()
        c.set_source_rgb(1, 1, 1); c.rectangle(-11, my - 4.5, 22, 4); c.fill()
    elif crushed:
        c.move_to(-10, my + 3); c.curve_to(-5, my - 4, 0, my + 4, 4, my - 1); c.curve_to(6, my - 3, 9, my + 1, 11, my + 3)
        c.stroke()
    else:                                                                   # the stare: a small tight zigzag
        c.move_to(-9, my); c.line_to(-4, my - 2.5); c.line_to(1, my + 1.5); c.line_to(6, my - 2); c.line_to(10, my)
        c.stroke()


def small(k, x, feet, s=1.0, pose="stand", face="hopeful", look=(0, 0), seed=600, mouth=None, badge=True, cv=False,
          tiptoe=0.0, seated=False, sweat=True):
    """cv: True draws the CV brick in his hands (poses "hug" and "offer"). tiptoe: 0..1 lifts his heels.
    seated: legs dangle from a chair seat at `feet` (his shoes hang below it) and the odd socks show."""
    c = k.c
    a = POSES_SMALL[pose] if isinstance(pose, str) else pose
    crushed = face == "crushed"
    slump = 6 if crushed else 0
    c.save(); c.translate(x, feet - tiptoe * 7 * s); c.scale(s, s)
    if seated:
        c.translate(0, S_L - 6)                                             # the seat is at his hips; legs hang
    # legs: knock knees, pigeon toes; trousers too long, pooling on big shoes (seated: they ride up over odd socks)
    hem = -19 if seated else -7
    for sx in (-1, 1):
        c.save(); c.translate(sx * 19, -4 + tiptoe * 4); c.rotate(-sx * 0.20)
        ellipse(k, 0, 0, 20, 8.5, S_SHOE, seed + 3 + sx, shadow=not seated, lw=2)
        c.restore()
        if seated:
            col, col2 = ((0.86, 0.20, 0.22), (1, 1, 1)) if sx < 0 else ((0.20, 0.62, 0.42), (0.98, 0.82, 0.25))
            cut(k, [(sx * 12, hem - 2), (sx * 32, hem - 2), (sx * 30, -8), (sx * 12, -8)], col, shadow=False, lw=1.8)
            c.set_source_rgb(*col2)
            if sx < 0:
                for yy in (hem + 2, hem + 7):
                    c.rectangle(-31, yy, 18, 2.4); c.fill()
            else:
                for dx, dy in ((16, hem + 2), (24, hem + 2), (20, hem + 7), (27, hem + 7)):
                    c.arc(dx, dy, 1.7, 0, 2 * math.pi); c.fill()
        cut(k, [(sx * 4, S_HIP - 2), (sx * 33, S_HIP - 2), (sx * 23, -25), (sx * 36, hem), (sx * 9, hem), (sx * 1, -25)],
            S_SUIT, shadow=False, lw=2)
        if not seated:
            c.set_source_rgb(*S_SUIT_DARK); c.set_line_width(1.8)
            for yy in (-11, -16):
                c.move_to(sx * 11, yy); c.curve_to(sx * 18, yy + 3, sx * 26, yy - 3, sx * 33, yy + 1); c.stroke()
    bt = S_BT + slump
    # jacket: wide, long, the shoulders riding up, one higher than the other
    cut(k, [(-46, bt + 1), (-33, bt - 8), (-10, bt + 2), (12, bt + 4), (31, bt + 3), (45, bt + 12), (48, S_HIP + 14),
            (-48, S_HIP + 14)], S_SUIT, lw=2.4)
    cut(k, [(0, bt + 56), (-14, bt + 6), (14, bt + 6)], S_SHIRT, shadow=False, lw=1.6)
    c.save(); c.translate(2, bt + 22); c.rotate(0.10)                         # the tie: the thin end longer than the front
    cut(k, [(-1, 2), (-4, 10), (-2, 44), (3, 44), (4, 10)], (0.80, 0.60, 0.12), shadow=False, lw=1.4)
    c.rotate(0.16)
    cut(k, [(0, 0), (-6, 8), (0.5, 27), (7, 8)], S_TIE, shadow=False, lw=1.5)
    cut(k, [(-7, -8), (4, -7), (7, 3), (-5, 4)], S_TIE, shadow=False, lw=1.5)          # a knot the size of a fist
    c.restore()
    for sx in (-1, 1):                                                      # lapels
        cut(k, [(sx * 14, bt + 6), (sx * 28, bt + (0 if sx < 0 else 6)), (sx * 21, bt + 38), (0, bt + 58)], S_SUIT,
            shadow=False, lw=1.8)
    c.set_source_rgb(*S_SUIT_DARK); c.set_line_width(2)
    c.move_to(0, bt + 58); c.line_to(1, S_HIP + 14); c.stroke()
    for i, by in enumerate((68, 80)):
        ellipse(k, 5, bt + by, 3, 3, S_SUIT_DARK, seed + 40 + i, shadow=False, lw=1.2)
    c.set_source_rgb(*S_SUIT_DARK); c.set_line_width(1.8)
    c.move_to(-38, bt + 70); c.line_to(-22, bt + 70); c.stroke()
    if badge:
        visitor(k, 18, bt + 50, 23, -0.10, seed + 50)
    hands = []
    held = cv and pose in ("hug", "offer")
    if held and pose == "hug":
        props.cv_brick(k, 2, bt + 60, 0.92, -0.06, seed + 60, stuffed=True)
    for side, (u, f) in ((-1, (a[0], a[1])), (1, (a[2], a[3]))):
        hands.append(limb(k, side * S_SHX, S_SHY[side] + slump, u, f, S_LN, S_LN, 19, 20, S_SUIT, S_SUIT, S_SKIN, 8,
                          seed + 10 + side, hand_first=True, hand_off=(3.0 if held or pose == "finger" else -1.0)))
    # head: narrow, sunk into the collar
    hy = S_HY + slump * 1.5
    for tri in ([(-36, hy - 28), (-54, hy - 40), (-34, hy - 42)], [(-28, hy - 44), (-40, hy - 66), (-18, hy - 52)],
                [(-6, hy - 54), (-4, hy - 74), (8, hy - 55)], [(28, hy - 46), (46, hy - 60), (36, hy - 38)],
                [(36, hy - 26), (55, hy - 32), (39, hy - 16)]):
        cut(k, tri, S_HAIR, shadow=False, lw=2)                               # tufts he has given up on
    ellipse(k, 0, hy, 36, 45, S_SKIN, seed + 22)
    cut(k, [(-36, hy - 12), (-39, hy - 30), (-30, hy - 47), (-10, hy - 54), (13, hy - 53), (30, hy - 44), (38, hy - 28),
            (36, hy - 12), (31, hy - 33), (17, hy - 41), (0, hy - 33), (-14, hy - 42), (-28, hy - 33)], S_HAIR,
        shadow=False, lw=2)                                                    # the hairline is already leaving
    c.set_source_rgb(*INK); c.set_line_width(6.4); c.set_line_cap(1)
    c.move_to(16, hy - 53); c.curve_to(16, hy - 68, 28, hy - 72, 32, hy - 62); c.stroke()
    c.set_source_rgb(*S_HAIR); c.set_line_width(3.4)
    c.move_to(16, hy - 52); c.curve_to(16, hy - 68, 28, hy - 72, 32, hy - 62); c.stroke()
    c.set_source_rgb(*INK); c.set_line_width(6.2)                             # the pencil behind his ear
    c.move_to(30, hy - 24); c.line_to(52, hy - 4); c.stroke()
    c.set_source_rgb(*S_PENCIL); c.set_line_width(3.6); c.move_to(31, hy - 23); c.line_to(48, hy - 7.5); c.stroke()
    c.set_source_rgb(0.95, 0.55, 0.60); c.move_to(29.5, hy - 24.5); c.line_to(32.5, hy - 21.5); c.stroke()
    for sx in (-1, 1):
        ellipse(k, sx * 36, hy + 8, 7.5, 10.5, S_SKIN, seed + 20 + sx, shadow=False, lw=2)
    _small_face(k, hy, face, look, mouth, seed + 30)
    if sweat:
        sweat_drop(c, -45, hy - 14, 0.95)                                    # one drop; a second when it goes wrong
        if crushed:
            sweat_drop(c, 44, hy - 30, 0.75)
    if pose == "finger":                                                    # three fingers: three degrees
        hx_, hy_ = hands[1]
        for i_, da in enumerate((-0.45, 0.0, 0.45)):
            c.save(); c.translate(hx_, hy_); c.rotate(da + 0.35)
            rect(k, -2.6, -19, 5.2, 14, S_SKIN, seed + 73 + i_, shadow=False, lw=1.6)
            c.restore()
        ellipse(k, hx_, hy_, 8, 8, S_SKIN, seed + 72, shadow=False, lw=2)
    if held and pose == "offer":
        hx_, hy_ = hands[1]
        props.cv_brick(k, hx_ + 22, hy_ - 30, 0.74, 0.10, seed + 60, stuffed=True)
        ellipse(k, hx_ + 2, hy_ + 2, 8, 8, S_SKIN, seed + 70, shadow=False, lw=2)
    off = (S_L - 6) if seated else 0
    c.restore()
    fy = feet - tiptoe * 7 * s
    return {"head": (x, fy + (hy + off) * s), "hands": [(x + hx * s, fy + (hy_ + off) * s) for hx, hy_ in hands],
            "top": fy + (S_TOP + off) * s}


# ------------------------------------------------------------------ the nice macho
M_SKIN = (0.87, 0.66, 0.50)
M_SKIN_DARK = (0.72, 0.50, 0.36)
M_HAIR = (0.19, 0.12, 0.08)
M_SHIRT = (0.66, 0.82, 0.95)
M_SHIRT_DARK = (0.44, 0.62, 0.80)
M_JEANS = (0.17, 0.24, 0.40)
M_JEANS_DARK = (0.11, 0.16, 0.29)
M_BELT = (0.42, 0.26, 0.14)
M_BOOT = (0.50, 0.32, 0.18)
M_L, M_T = 146, 140
M_HIP = -M_L
M_BT = M_HIP - M_T
M_HY = M_BT - 54
M_SH = (88, M_BT + 26)
M_LN1, M_LN2 = 56, 52
M_TOP = M_HY - 62
M_HAND = 20


def _m_ik(side, tx, ty):
    return ik(side * M_SH[0], M_SH[1], tx, ty, M_LN1, M_LN2, side)


POSES_MACHO = {
    "stand": (-11, 4, 11, -4),                                             # arms held off the body by his own back
    "pen": (-11, 4) + _m_ik(1, 138, M_BT + 74),                            # hands Pam her pen, palm up
    "tin": _m_ik(-1, -35, M_BT + 112) + _m_ik(1, 35, M_BT + 112),          # the tiny tin between his huge hands
    "pinch": (-11, 4) + _m_ik(1, 176, M_BT + 70),                          # Pam's pen, between two fingertips
    "wave": (-11, 4) + _m_ik(1, 142, M_BT - 22),                           # a small open-hand hello
    "shrug": _m_ik(-1, -146, M_BT + 74) + _m_ik(1, 146, M_BT + 74),        # gracious: palms out, no hard feelings
    "sit": _m_ik(-1, -34, M_BT + 122) + _m_ik(1, 34, M_BT + 122),
}


def _head_pts(k, hy, seed):
    """A head that is mostly jaw: round on top, wider and flat below."""
    r = k.rng(seed)
    pts = []
    n = 32
    for i in range(n):
        a = 2 * math.pi * i / n
        cs, sn = math.cos(a), math.sin(a)
        if sn > 0:
            px = math.copysign(abs(cs) ** 0.48, cs) * 46
            py = (sn ** 0.70) * 52
        else:
            px, py = cs * 44, sn * 46
        pts.append((px * (1 + r.uniform(-0.01, 0.01)), hy + py * (1 + r.uniform(-0.01, 0.01))))
    return pts


def _macho_face(k, y, face, look, mouth, seed, glint):
    c = k.c
    lx, ly = look
    ey = y - 2
    smile = face in ("smile", "warm", "gracious")
    lid = {"smile": 0.12, "warm": 0.0}.get(face, 0.0)                       # the confident grin comes with easy lids
    for sx in (-18, 18):
        ellipse(k, sx, ey, 9.5, 9.5, (1, 1, 1), seed + sx, shadow=False, lw=2)
        ellipse(k, sx + lx * 3.6, ey + ly * 3.6 + lid * 3, 4.6, 4.6, (0.24, 0.15, 0.08), seed + sx + 1, shadow=False,
                outline=False)
        c.set_source_rgb(1, 1, 1); c.arc(sx + lx * 3.6 - 1.5, ey + ly * 3.6 + lid * 3 - 1.6, 1.4, 0, 2 * math.pi); c.fill()
        if lid:
            c.save(); c.arc(sx, ey, 10.2, 0, 2 * math.pi); c.clip()
            c.set_source_rgb(*M_SKIN); c.rectangle(sx - 11, ey - 11, 22, 21 * lid); c.fill()
            c.restore()
            _brow(c, sx - 9.2, ey - 10.5 + 21 * lid, sx + 9.2, ey - 10.5 + 21 * lid, 2.6)
        if smile:                                                           # the cheek pushes the lower lid up
            c.set_source_rgb(*M_SKIN); c.rectangle(sx - 11, ey + 5, 22, 7); c.fill()
            c.set_source_rgb(*INK); c.set_line_width(2.2); c.set_line_cap(1)
            c.move_to(sx - 9, ey + 6); c.curve_to(sx - 4, ey + 3.5, sx + 4, ey + 3.5, sx + 9, ey + 6); c.stroke()
    by = y - 18
    if face == "gracious":
        _brow(c, -31, by + 1, -9, by - 5, 5.6); _brow(c, 9, by - 5, 31, by + 1, 5.6)
    elif face == "listen":
        _brow(c, -31, by - 1, -9, by + 1, 5.6); _brow(c, 9, by - 3, 31, by - 4, 5.6)
    elif face == "smile":                                                   # one brow up: he knows
        _brow(c, -31, by + 1, -9, by, 5.6); _brow(c, 9, by - 5, 31, by - 7, 5.6)
    else:
        _brow(c, -31, by, -9, by - 2, 5.6); _brow(c, 9, by - 2, 31, by, 5.6)
    c.set_source_rgb(*M_SKIN_DARK); c.set_line_width(2.6); c.set_line_cap(1)
    c.move_to(1, y + 4); c.line_to(5, y + 15); c.line_to(-2, y + 16); c.stroke()
    my = y + 32
    if mouth:
        im.mouth(k, 0, my, mouth, M_SKIN, erase=(1, 1), seed=seed + 96)
    elif face == "smile":                                                   # a wide, slightly lopsided grin
        c.move_to(-21, my - 6); c.curve_to(-10, my - 3, 10, my - 4, 23, my - 10)
        c.curve_to(19, my + 10, -14, my + 11, -21, my - 6); c.close_path()
        c.set_source_rgb(1, 1, 1); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.6); c.stroke()
        c.set_line_width(1.3); c.move_to(-17, my + 1.5); c.curve_to(-6, my + 4, 8, my + 3.5, 19, my - 1); c.stroke()
    elif face in ("warm", "gracious"):
        c.set_source_rgb(*INK); c.set_line_width(3.6); c.set_line_cap(1)
        c.move_to(-15, my - 4); c.curve_to(-6, my + 5, 6, my + 5, 15, my - 4); c.stroke()
    else:
        c.set_source_rgb(*INK); c.set_line_width(3.6); c.set_line_cap(1)
        c.move_to(-10, my); c.curve_to(-4, my + 2, 4, my + 2, 11, my - 1); c.stroke()
    if smile:                                                               # dimples
        c.set_source_rgb(*M_SKIN_DARK); c.set_line_width(2.2)
        for sx in (-1, 1):
            c.move_to(sx * 27, my - 10); c.curve_to(sx * 31, my - 6, sx * 31, my - 1, sx * 27, my + 2); c.stroke()
    c.set_source_rgb(*M_SKIN_DARK); c.set_line_width(2.4)                    # the cleft in his chin
    c.move_to(0.5, my + 15); c.line_to(0.5, my + 21); c.stroke()
    if glint and face == "smile":
        c.save(); c.translate(17, my - 6); c.scale(0.7, 0.7)
        c.move_to(0, -8); c.line_to(1.8, -1.8); c.line_to(8, 0); c.line_to(1.8, 1.8); c.line_to(0, 8)
        c.line_to(-1.8, 1.8); c.line_to(-8, 0); c.line_to(-1.8, -1.8); c.close_path()
        c.set_source_rgb(1, 1, 1); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.2); c.stroke()
        c.restore()


def macho(k, x, feet, s=1.0, pose="stand", face="smile", look=(0, 0), seed=700, mouth=None, badge=True, glint=False,
          tin=False, pen=False, seated=False):
    """tin: the tiny cookie tin between his hands (pose "tin"). pen: Pam's pen on his open palm (pose "pen").
    seated: thighs forward (drawn short), for the interview chair; `feet` is still the floor."""
    c = k.c
    a = POSES_MACHO[pose] if isinstance(pose, str) else pose
    c.save(); c.translate(x, feet); c.scale(s, s)
    drop = 0
    if seated:
        drop = 62
        for sx in (-1, 1):
            ellipse(k, sx * 24, -5, 21, 9, M_BOOT, seed + 3 + sx, lw=2)
            cut(k, [(sx * 12, M_HIP + drop + 30), (sx * 36, M_HIP + drop + 30), (sx * 35, -8), (sx * 13, -8)], M_JEANS,
                shadow=False, lw=2)
            cut(k, [(sx * 3, M_HIP + drop - 6), (sx * 40, M_HIP + drop - 6), (sx * 40, M_HIP + drop + 34),
                    (sx * 8, M_HIP + drop + 34)], M_JEANS, shadow=False, lw=2)
    else:
        for sx in (-1, 1):
            ellipse(k, sx * 19, -5, 20, 9, M_BOOT, seed + 3 + sx, lw=2)
            cut(k, [(sx * 1, M_HIP - 4), (sx * 31, M_HIP - 4), (sx * 28, -8), (sx * 7, -8)], M_JEANS, shadow=False, lw=2)
            c.set_source_rgb(*M_JEANS_DARK); c.set_line_width(1.8)
            c.move_to(sx * 27, M_HIP + 14); c.line_to(sx * 24, -12); c.stroke()
    c.translate(0, drop)
    bt = M_BT
    rect(k, -20, bt - 24, 40, 30, M_SKIN, seed + 5, shadow=False, lw=2)       # a neck as wide as his head
    cut(k, [(-100, bt + 24), (-82, bt + 3), (-24, bt - 10), (24, bt - 10), (82, bt + 3), (100, bt + 24), (74, bt + 92),
            (31, M_HIP - 6), (-31, M_HIP - 6), (-74, bt + 92)], M_SHIRT, lw=2.4)
    cut(k, [(0, bt + 42), (-18, bt - 7), (18, bt - 7)], M_SKIN, shadow=False, lw=1.6)          # open collar
    for sx in (-1, 1):
        cut(k, [(sx * 18, bt - 7), (sx * 37, bt - 14), (sx * 29, bt + 18), (sx * 4, bt + 40)], M_SHIRT, shadow=False, lw=1.8)
    c.set_source_rgb(*M_SHIRT_DARK); c.set_line_width(2.2); c.set_line_cap(1)
    c.move_to(0, bt + 42); c.line_to(0, M_HIP - 8); c.stroke()                # placket
    for sx in (-1, 1):                                                       # the chest
        c.move_to(sx * 5, bt + 80); c.curve_to(sx * 24, bt + 98, sx * 64, bt + 94, sx * 80, bt + 58); c.stroke()
    c.set_line_width(1.6)
    for sx in (-1, 1):                                                       # the waist, pulled in
        c.move_to(sx * 56, bt + 104); c.curve_to(sx * 44, bt + 114, sx * 36, bt + 124, sx * 33, bt + 134); c.stroke()
    for i, by in enumerate((112, 130)):
        ellipse(k, 0, bt + by, 3, 3, (1, 1, 1), seed + 40 + i, shadow=False, lw=1.3)
    for gy in (60, 86):                                                      # two buttons, working hard
        c.save(); c.translate(0, bt + gy); c.scale(3.0, 7.5); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        c.set_source_rgb(*M_SKIN); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.3); c.stroke()
        ellipse(k, 0, bt + gy, 3, 3, (1, 1, 1), seed + 45 + gy, shadow=False, lw=1.3)
        c.set_source_rgb(*M_SHIRT_DARK); c.set_line_width(1.4)
        for sx in (-1, 1):
            c.move_to(sx * 5, bt + gy); c.line_to(sx * 15, bt + gy - 3); c.stroke()
    rect(k, -31, M_HIP - 10, 62, 11, M_BELT, seed + 61, shadow=False, lw=1.6)
    rect(k, -7, M_HIP - 12, 14, 15, (0.80, 0.70, 0.36), seed + 62, shadow=False, lw=1.4)
    if badge:
        visitor(k, 46, bt + 40, 28, -0.06, seed + 50)
    hands = []
    for side, (u, f) in ((-1, (a[0], a[1])), (1, (a[2], a[3]))):
        hands.append(limb(k, side * M_SH[0], bt + 26, u, f, M_LN1, M_LN2, 46, 31, M_SHIRT, M_SKIN, M_SKIN, M_HAND,
                          seed + 10 + side, bulge=1.34, sleeve=0.42))
        ellipse(k, side * (M_SH[0] + 1), bt + 22, 27, 24, M_SHIRT, seed + 14 + side, shadow=False, lw=2)   # the shoulder
        c.set_source_rgb(*M_SHIRT); c.rectangle(min(side * 58, side * 86), bt + 12, 28, 34); c.fill()        # joined to the chest
    # head
    hy = M_HY
    pts = _head_pts(k, hy, seed + 20)
    cut(k, pts, M_SKIN)
    c.save()                                                                 # stubble: a shadow on the jaw
    c.move_to(*pts[0])
    for q in pts[1:]:
        c.line_to(*q)
    c.close_path(); c.clip()
    c.set_source_rgba(0.16, 0.10, 0.07, 0.20)
    c.move_to(-52, hy + 14); c.curve_to(-32, hy + 20, -26, hy + 22, -22, hy + 36)
    c.curve_to(-10, hy + 23, 10, hy + 23, 22, hy + 36); c.curve_to(26, hy + 22, 32, hy + 20, 52, hy + 14)
    c.line_to(52, hy + 64); c.line_to(-52, hy + 64); c.close_path(); c.fill()
    c.restore()
    for sx in (-1, 1):
        ellipse(k, sx * 46, hy + 4, 6, 10, M_SKIN, seed + 26 + sx, shadow=False, lw=2)
    cut(k, [(-46, hy - 4), (-47, hy - 30), (-36, hy - 50), (-8, hy - 63), (22, hy - 66), (43, hy - 52), (49, hy - 28),
            (46, hy - 4), (40, hy - 18), (30, hy - 31), (4, hy - 27), (-22, hy - 32), (-38, hy - 22)], M_HAIR,
        shadow=False, lw=2)
    c.set_source_rgba(1, 1, 1, 0.22); c.set_line_width(3); c.set_line_cap(1)
    c.move_to(-20, hy - 50); c.curve_to(-4, hy - 59, 16, hy - 58, 30, hy - 45); c.stroke()
    _macho_face(k, hy + 4, face, look, mouth, seed + 30, glint)
    if tin and pose == "tin":                                               # the tin, tiny between his palms
        mx = (hands[0][0] + hands[1][0]) / 2
        ty = hands[0][1] + 4
        props.cookie_tin(k, mx, ty, 0.42, seed + 80, tag=False)
        for sx in (-1, 1):                                                  # thumbs over the rim
            ellipse(k, mx + sx * 16, ty - 8, 6.5, 4.5, M_SKIN, seed + 84 + sx, shadow=False, lw=1.6)
    if pose == "pinch":                                                     # two enormous fingers, one tiny pen
        hx_, hy_ = hands[1]
        c.save(); c.translate(hx_, hy_); c.rotate(-0.12)
        c.save(); c.translate(-2, -17); c.rotate(-0.5); rect(k, -3.6, -17, 7.2, 17, M_SKIN, seed + 90, shadow=False, lw=1.8)
        c.restore()                                                         # the little finger, out
        for i_, (fy, fa) in enumerate(((-8, -0.16), (9, 0.2))):
            c.save(); c.translate(12, fy); c.rotate(fa)
            c.save(); c.scale(17, 7.5); c.arc(0.55, 0, 1, 0, 2 * math.pi); c.restore()
            c.set_source_rgb(*M_SKIN); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2); c.stroke()
            c.restore()
        if pen:
            props.pen(k, 41, 1, 0.82, math.pi / 2 - 0.1)
        c.restore()
    if pen and pose == "pen":
        hx_, hy_ = hands[1]
        props.pen(k, hx_ + 1, hy_ - 15, 1.0, 0.12)
    c.restore()
    return {"head": (x, feet + (hy + drop) * s), "hands": [(x + hx * s, feet + (hy_ + drop) * s) for hx, hy_ in hands],
            "top": feet + (M_TOP + drop) * s}
