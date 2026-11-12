"""The waiter robot for "I Will Replace You" (UptimeZ Inc.), paper-cutout kit.
A short, round TRAINEE on one wobbly wheel: red bow tie, staff badge, a tray arm and a pointing arm,
and a round screen head. Pathetic, never evil. Distinct from DON 2.0 (a grey box with a red tie).

Three silhouettes carry the punchline (the review's top note), so the body changes, not just the screen:
  "nervous": compact and upright, head sunk into the shoulders, hands clasped in front
  "lock":    wheel clamp on, body snapped upright and tall, pointing arm straight out, held still
  "lean":    both arms dropped, head sunk on a short neck, body tipped toward Don, face looking up at him
plus working poses: "travel" (tray out, leaning into the move), "serve", "lift" (dome), "tie" (bow-tie fix).

robot(k, x, feet, s, pose, face, look, wobble, side, talk, tray, seed) -> {"head", "hands", "tray"}
  face:  eager | pleading | stern | timid | proud
  side:  +1 faces right (toward Don in the film), -1 faces left; the point always goes the other way
  wobble: body tilt in radians (animate only while travelling or recovering)
Coordinates: feet = bottom of the wheel; the screen centre sits at feet - 238*s."""
import math
import kit
import brand
from kit import INK, cut, rect, ellipse, text

BODY = (0.95, 0.94, 0.90)          # off-white shell
BODY_SHADE = (0.84, 0.83, 0.78)
STEEL = (0.60, 0.63, 0.68)
STEEL_DARK = (0.36, 0.38, 0.43)
SCREEN = (0.10, 0.15, 0.27)        # navy screen
GLOW = (0.55, 0.92, 1.00)          # screen ink: cyan
GLOW_STERN = (1.00, 0.36, 0.30)    # stern: red
TIE = (0.85, 0.10, 0.14)
CLAMP = (0.90, 0.20, 0.16)
TRAY = (0.80, 0.82, 0.85)

HEAD_Y = -238                      # screen centre, local units
SHOULDER_Y = -150

#   (body tilt toward the facing side, crouch, head drop, back arm (a1, a2), front arm (a1, a2))
#   back arm = the -x arm (points at Sofía), front arm = the +x arm (holds the tray toward Don);
#   arm angles: kit.arm, 0 = down, +90 = toward +x; the whole robot is mirrored for side = -1
POSES = {
    "stand":   (0.00, 0, 0, (-20, 0), (20, 0)),
    "travel":  (0.10, 0, 4, (-24, 10), (60, 30)),        # tray held out front, leaning into the move
    "serve":   (0.06, 0, 2, (-20, 0), (60, 30)),
    "lift":    (0.04, 0, 0, (-20, 0), (130, 30)),        # front hand up, lifting the dome away
    "tie":     (0.02, 0, 6, (-20, 0), (-22, -134)),      # front hand at the bow tie
    "nervous": (0.00, 22, 30, (25, -60), (-25, 60)),     # compact and upright: head sunk into the shoulders, hands clasped
    "lock":    (0.00, -12, -8, (-90, 0), (20, 0)),       # tall, still; back arm points straight out at Sofía
    "lean":    (0.22, 24, 34, (-5, 0), (5, 0)),          # collapsed: head low, neck short, both arms dropped, tipped to Don
}


def _wheel(k, locked, seed):
    c = k.c
    c.set_source_rgb(*INK); c.set_line_width(5)                       # fork
    c.move_to(-14, -60); c.line_to(-8, -24); c.move_to(14, -60); c.line_to(8, -24); c.stroke()
    c.set_source_rgb(*STEEL); c.set_line_width(2.6)
    c.move_to(-14, -60); c.line_to(-8, -24); c.move_to(14, -60); c.line_to(8, -24); c.stroke()
    ellipse(k, 0, -24, 24, 24, (0.16, 0.16, 0.18), seed, lw=2.2)
    ellipse(k, 0, -24, 9, 9, STEEL, seed + 1, shadow=False, lw=1.6)
    if locked:                                                        # red clamp snapped onto the wheel
        rect(k, -30, -34, 14, 22, CLAMP, seed + 2, shadow=False, lw=1.8)
        rect(k, 16, -34, 14, 22, CLAMP, seed + 3, shadow=False, lw=1.8)
        c.set_source_rgb(*INK); c.set_line_width(2)
        c.move_to(-16, -23); c.line_to(16, -23); c.stroke()


def _bow_tie(k, x, y, seed):
    cut(k, [(x, y), (x - 20, y - 11), (x - 20, y + 11)], TIE, shadow=False, lw=1.8)
    cut(k, [(x, y), (x + 20, y - 11), (x + 20, y + 11)], TIE, shadow=False, lw=1.8)
    ellipse(k, x, y, 6, 6, TIE, seed, shadow=False, lw=1.6)


def _badge(k, x0, y0, seed, label="TRAINEE"):
    """Day One staff badge style: clip, white card, green band with the logo mark, label."""
    c = k.c
    w = 50
    rect(k, x0 + w / 2 - 5, y0 - 5, 10, 6, (0.45, 0.47, 0.52), seed + 1, shadow=False, lw=1.2)
    rect(k, x0, y0, w, 25, (1, 1, 1), seed, shadow=False, lw=1.5)
    c.set_source_rgb(*brand.GREEN); c.rectangle(x0 + 1.5, y0 + 1.5, w - 3, 7); c.fill()
    brand.mark(c, x0 + 3, y0 + 2, 6, zzz=False)
    text(k, label, x0 + w / 2, y0 + 17, 8.6, INK, font="Inter", bold=True)


def screen_face(k, face, look=(0, 0), talk=0.0, side=1):
    """Draws the face inside the screen, centred at (0, 0) in head-local units (screen r ~40 x 33)."""
    c = k.c
    lx, ly = look[0] * 6, look[1] * 4
    col = GLOW_STERN if face == "stern" else GLOW
    c.set_source_rgb(*col)
    c.set_line_cap(1)
    eyes = (-15, 15)
    if face == "blink":                                 # screen blink: a one-frame flat line between faces
        c.set_line_width(4)
        for ex in eyes:
            c.move_to(ex - 8, -3); c.line_to(ex + 8, -3); c.stroke()
        return
    if face == "pleading":                              # big glossy eyes, brows tilted up in the middle
        for ex in eyes:
            c.arc(ex + lx, -4 + ly, 11, 0, 2 * math.pi); c.fill()
        c.set_source_rgb(*SCREEN)
        for ex in eyes:
            c.arc(ex + lx + 3, -8 + ly, 3.6, 0, 2 * math.pi); c.fill()      # big highlight (shine)
            c.arc(ex + lx - 3, 0 + ly, 1.8, 0, 2 * math.pi); c.fill()
        c.set_source_rgb(*col); c.set_line_width(3)
        for sx in (-1, 1):
            c.move_to(sx * 26, -18); c.line_to(sx * 8, -22); c.stroke()     # worried brows
        c.arc(0, 18, 5, math.pi * 1.1, math.pi * 1.9); c.stroke()          # small wobbly mouth
    elif face == "stern":                               # angled bars, red
        c.set_line_width(6)                             # firm, flat bars, a touch lower at the inner end:
        for ex in eyes:                                 # trying to look commanding (v1's inner-high bars read as sad)
            o = 1 if ex > 0 else -1
            c.move_to(ex - 9 + lx, -6 + o * 3); c.line_to(ex + 9 + lx, -6 - o * 3); c.stroke()
    elif face == "timid":                               # small eyes looking down
        for ex in eyes:
            c.arc(ex * 0.8 + lx, 4 + ly, 4, 0, 2 * math.pi); c.fill()
        c.set_line_width(2.6)
        c.move_to(-9, 19)
        for i in range(4):
            c.line_to(-9 + (i + 1) * 4.5, 19 + (2 if i % 2 == 0 else -2))
        c.stroke()
    elif face == "proud":                               # closed happy arcs
        c.set_line_width(4.5)
        for ex in eyes:
            c.arc(ex, 0, 8, math.pi * 1.15, math.pi * 1.85); c.stroke()
    else:                                               # eager: round eyes
        for ex in eyes:
            c.arc(ex + lx, -4 + ly, 7.5, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(*col)
    if face in ("stern", "eager", "proud"):
        if talk > 0.05:                                 # talking mouth opens
            w, h = (16, 4 + 12 * talk) if face != "stern" else (22, 4 + 14 * talk)
            c.rectangle(-w / 2, 13, w, h); c.fill()
        elif face == "stern":
            c.set_line_width(4); c.move_to(-12, 18); c.line_to(12, 18); c.stroke()
        else:
            c.set_line_width(3.5); c.arc(0, 10, 11, 0.2 * math.pi, 0.8 * math.pi); c.stroke()
    elif talk > 0.05 and face in ("timid", "pleading"):
        c.arc(0, 19, 2.5 + 4 * talk, 0, 2 * math.pi); c.fill()


def dome_tray(k, x, y, w=96, dome=1.0, seed=600):
    """Tray centred on (x, y) = its top surface; dome 1 = closed, 0 = lifted away (drawn by the caller)."""
    rect(k, x - w / 2, y, w, 8, TRAY, seed, shadow=False, lw=1.8)
    if dome > 0.5:
        c = k.c
        c.save(); c.translate(x, y)
        c.move_to(-w * 0.42, 0); c.curve_to(-w * 0.42, -w * 0.5, w * 0.42, -w * 0.5, w * 0.42, 0); c.close_path()
        c.set_source_rgb(0.86, 0.88, 0.91); c.fill_preserve()
        c.set_source_rgb(*INK); c.set_line_width(2.2); c.stroke()
        c.set_source_rgba(1, 1, 1, 0.8); c.set_line_width(3)
        c.arc(-4, -w * 0.18, w * 0.24, math.pi * 1.15, math.pi * 1.45); c.stroke()
        ellipse(k, 0, -w * 0.38, 6, 4, STEEL, seed + 1, shadow=False, lw=1.6)
        c.restore()


def blend(p1, p2, u):
    """A pose between two named poses (u 0..1), for animated collapses and snaps: pass the result as pose."""
    a, b = POSES[p1], POSES[p2]
    L = lambda x, y: x + (y - x) * u
    return (L(a[0], b[0]), L(a[1], b[1]), L(a[2], b[2]), (L(a[3][0], b[3][0]), L(a[3][1], b[3][1])),
            (L(a[4][0], b[4][0]), L(a[4][1], b[4][1])))


HEAD_DX = {"travel": 6, "lean": 8}
HEAD_ROT = {"lean": -0.10}


def robot(k, x, feet, s=1.0, pose="stand", face="eager", look=(0, 0), wobble=0.0, side=1, talk=0.0,
          tray=None, seed=900, badge=True, locked=None, head_dx=None, head_rot=None):
    """tray: None | "empty" | "dome" (carried in the front hand).
    pose: a name in POSES, or a tuple from blend() (then pass head_dx / head_rot / locked as needed)."""
    c = k.c
    named = isinstance(pose, str)
    tilt, crouch, drop, near, far = POSES[pose] if named else pose
    if locked is None:
        locked = pose == "lock"
    if head_dx is None:
        head_dx = HEAD_DX.get(pose, 0) if named else 0
    if head_rot is None:
        head_rot = HEAD_ROT.get(pose, 0) if named else 0
    c.save(); c.translate(x, feet); c.scale(s * side, s)          # mirror so +x is the way it faces
    c.save()
    c.rotate(tilt + wobble)                                       # tips over the wheel contact point
    _wheel(k, locked, seed)
    body_y = -118 + crouch
    # body: a round shell, slightly squashed when hunched
    ry = 58 - crouch * 0.4
    ellipse(k, 0, body_y, 52, ry, BODY, seed + 10, lw=2.6)
    c.set_source_rgb(*BODY_SHADE); c.set_line_width(4)
    c.arc(0, body_y, 44, math.pi * 0.15, math.pi * 0.85); c.stroke()
    neck_top = HEAD_Y + 40 + drop + crouch
    rect(k, -9, neck_top, 18, body_y - ry - neck_top + 6, STEEL_DARK, seed + 11, shadow=False, lw=1.6)
    # arms: hands[0] = back (-x) arm, hands[1] = front (+x) arm
    sh_y = SHOULDER_Y + crouch
    hands = []
    for sgn, (a1, a2) in ((-1, near), (1, far)):
        ln = 30 if (locked and sgn < 0) else 44                     # the point stops short of Sofía (set sheet)
        hands.append(kit.arm(k, sgn * 46, sh_y, a1, a2, STEEL, STEEL_DARK, seed + 20 + sgn, ln=ln, w=12))
    _bow_tie(k, 0, body_y - ry + 14, seed + 30)
    if badge:                                                    # badge text never mirrored
        c.save(); c.scale(side, 1); _badge(k, -25, body_y - 18, seed + 31); c.restore()
    if locked:                                                   # pointing finger on the back hand
        hx, hy = hands[0]
        a = math.radians(near[0] + near[1])
        dx, dy = math.sin(a), math.cos(a)
        c.set_source_rgb(*INK); c.set_line_width(7); c.set_line_cap(1)
        c.move_to(hx, hy); c.line_to(hx + dx * 18, hy + dy * 18); c.stroke()
        c.set_source_rgb(*STEEL_DARK); c.set_line_width(4)
        c.move_to(hx, hy); c.line_to(hx + dx * 17, hy + dy * 17); c.stroke()
    tray_pt = None
    if tray:                                                     # tray rests on the near hand
        tx, ty = hands[1]
        tray_pt = (tx, ty - 6)
        dome_tray(k, tx, ty - 6, dome=1.0 if tray == "dome" else 0.0, seed=seed + 40)
    # head: a round screen
    hy = HEAD_Y + drop + crouch
    c.save(); c.translate(head_dx, hy)
    c.rotate(head_rot)                                           # lean: face tipped back, looking up at Don
    ellipse(k, 0, 0, 50, 44, BODY, seed + 50)
    ellipse(k, 0, 0, 40, 33, SCREEN, seed + 51, shadow=False, lw=1.8)
    c.save(); c.scale(side, 1)                                   # keep the face un-mirrored
    screen_face(k, face, look=(look[0] * side, look[1]), talk=talk, side=side)
    c.restore()
    c.set_source_rgb(*INK); c.set_line_width(2.4); c.move_to(0, -44); c.line_to(0, -58); c.stroke()
    ellipse(k, 0, -62, 6, 6, GLOW_STERN if face == "stern" else (1.0, 0.82, 0.25), seed + 52, shadow=False, lw=1.5)
    c.restore()
    c.restore()
    # canvas-space points (rotation ignored for points: tilts are small)
    def P(px, py):
        return (x + px * s * side, feet + py * s)
    c.restore()
    return {"head": P(0, hy), "hands": [P(*h) for h in hands], "tray": P(*tray_pt) if tray_pt else None}
