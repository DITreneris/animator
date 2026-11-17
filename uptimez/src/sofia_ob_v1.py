"""v1, pinned. SOFIA, "The Onboarding", v1. Her office look from The Best Candidate (sofia_bc: teal wrap blouse, ink-navy blazer,
gold belt) with this episode's touches (grill, 17 Nov):
- PEARLS FOR GOLD: a single pearl drop on each ear (a gold stud, a short chain, one pearl; it swings with `lag`), one
  short strand at the collarbone, lying over the dark lapels where it shows, and a one-row pearl bracelet on her
  screen-left wrist: the hand that turns the tablet, taps, and slips the CV into the pack, so the inserts are hers
  without a face in them;
- IN CONTROL: she appraises the Client, she is not flustered by him (that was the macho, her one crack). No blush in
  this film. Three new faces, all built on faces she already has:
    "appraise"  half lids, her one raised eyebrow, a small closed smile: reading him like a CV. Drawn twice, with
                look=(lx, 1) and then look=(lx, 0.45): her eyes go down him and come back up (with half lids a
                higher look reads as rolling her eyes);
    "oh"        the same eyes, the lips a small soft O: "Oh..." (low, drawn out, falling);
    "breath"    lids shut, a small smile: the half-second close to him in beat 06;
  her other faces in this film are old ones: "tiny" then "smile" at the door, "smile" for the question (with a tilt
  of the head: lean), "knowing" for the one glance she gives Don and for the tablet at the end;
- the tablet (tablet=): "hold" against her, its back to us with the sheet clipped to it (the CV, from the first beat);
  "show" held out to the Client, the screen to us, one green button on it ("Tap here."): flat staging, so the viewer
  sees what he taps; "trophy" held up beside her, the screen to us, his thumbprint on the button:
  she looks at it before she tucks it under her arm (the tuck is animation, not a pose here).
New poses: "hold" (the tablet arm), "necklace" (two fingers of her other hand on the strand), "show", "trophy".
sofia_bc.py and every earlier Sofia are untouched: its earring, its lapel hook, its face builder and its poses are
swapped for the length of one call and restored.
Usage: sofia(k, x, feet, s, pose, face_kind, look, lag, seed, badge, lean, mouth, sparkle, tablet)"""
import math
import kit
import sofia_bc as sbc
import props_ss
from kit import INK, cut, rect, ellipse
from sofia_v4 import GOLD, SKIN, RED

PEARL = (0.99, 0.97, 0.93)
PEARL_SHADE = (0.80, 0.77, 0.74)
TABLET = (0.17, 0.18, 0.22)
SCREEN = (0.86, 0.93, 0.97)
PAPER = (0.99, 0.98, 0.95)
OIL = (0.22, 0.17, 0.14)
BODY_TOP, HY, LN = sbc.BODY_TOP, sbc.HY, 48
SH = ((-39, BODY_TOP + 14), (39, BODY_TOP + 14))


def _ik(side, tx, ty):
    """Arm angles (upper, fore relative) that put the hand at (tx, ty); the elbow bends away from the body."""
    sx, sy = SH[0 if side < 0 else 1]
    dx, dy = tx - sx, ty - sy
    d = min(math.hypot(dx, dy), 2 * LN - 0.2)
    base, a = math.degrees(math.atan2(dx, dy)), math.degrees(math.acos(d / (2 * LN)))
    return (base + side * a, -side * 2 * a)


CARRY = _ik(-1, -28, BODY_TOP + 92)                       # the tablet at her hip, clear of the strand and the badge
REST = sbc.POSES["stand"][2:]
POSES = {
    "hold": CARRY + REST,
    "necklace": CARRY + _ik(1, 17, BODY_TOP + 34),
    "show": _ik(-1, -104, BODY_TOP + 52) + REST,
    "trophy": _ik(-1, -62, BODY_TOP + 66) + REST,
}
SPECIAL = {"appraise": "unimpressed", "oh": "unimpressed", "breath": "closed"}


def pearl(k, x, y, r, seed, lw=1.5):
    c = k.c
    ellipse(k, x, y, r, r, PEARL, seed, shadow=False, lw=lw)
    c.set_source_rgba(*PEARL_SHADE, 0.9); c.arc(x + r * 0.22, y + r * 0.26, r * 0.50, 0.1, 1.5); c.set_line_width(r * 0.32); c.stroke()
    c.set_source_rgba(1, 1, 1, 1); c.arc(x - r * 0.30, y - r * 0.32, r * 0.24, 0, 2 * math.pi); c.fill()


def drop(k, x, y, lgx=0.0, spark=0.0, seed=0):
    """A gold stud at the lobe (x, y), a short chain, one pearl; the pearl swings with lgx."""
    c = k.c
    c.save(); c.translate(x, y + 2); c.rotate(-lgx * 0.05)
    c.set_source_rgba(0.62, 0.42, 0.10, 0.40); c.arc(0.8, 20.5, 8.8, 0, 2 * math.pi); c.fill()   # a soft shadow on the hair
    c.set_source_rgb(*INK); c.set_line_width(3.6); c.set_line_cap(0); c.move_to(0, 0); c.line_to(0, 12); c.stroke()
    c.set_source_rgb(*GOLD); c.set_line_width(1.9); c.move_to(0, 0); c.line_to(0, 12); c.stroke()
    pearl(k, 0, 19, 7.4, seed + 3, lw=1.8)
    c.restore()
    ellipse(k, x, y, 4.6, 4.6, GOLD, seed, shadow=False, lw=1.7)
    props_ss.sparkle(c, x - 6, y + 14, 9 + 7 * spark, spark)


def strand_pts(n=9):
    """The strand: a shallow curve from lapel to lapel, lowest in the middle, just under her chin."""
    out = []
    for i in range(n):
        t = i / float(n - 1) * 2 - 1
        out.append((t * 27.0, BODY_TOP + 11 + 15.0 * (1 - t * t)))
    return out


def strand(k, seed):
    pts = strand_pts()
    c = k.c
    c.set_source_rgb(*INK); c.set_line_width(1.4)
    c.move_to(*pts[0])
    for q in pts[1:]:
        c.line_to(*q)
    c.stroke()
    order = sorted(range(len(pts)), key=lambda i: -abs(pts[i][0]))           # the middle pearls on top
    for i in order:
        pearl(k, pts[i][0], pts[i][1], 4.3, seed + 60 + i)


def tablet(k, x, y, ang, kind, seed=0):
    """kind "back": its back to us, the sheet clipped to it; "form": the screen to us, one green button;
    "print": the screen to us, the thumbprint on the button."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang)
    rect(k, -23, -31, 46, 62, TABLET, seed + 1, lw=2)
    if kind == "back":
        c.save(); c.translate(1.5, -3); c.rotate(0.07)
        rect(k, -19, -30, 38, 54, PAPER, seed + 2, shadow=False, lw=1.6)       # the sheet: a portrait and lines, a CV
        rect(k, -15, -25, 12, 14, (0.98, 0.86, 0.50), seed + 3, shadow=False, lw=1.2)
        c.set_source_rgb(0.62, 0.62, 0.64); c.set_line_width(1.6); c.set_line_cap(1)
        for yy, x0, x1 in ((-23, 1, 15), (-18, 1, 12), (-13, 1, 14), (-5, -15, 15), (0, -15, 11), (5, -15, 14),
                           (10, -15, 9), (15, -15, 13)):
            c.move_to(x0, yy); c.line_to(x1, yy); c.stroke()
        c.restore()
        rect(k, -7, -36, 14, 9, (0.72, 0.74, 0.78), seed + 4, shadow=False, lw=1.5)       # the clip
    else:
        rect(k, -19, -27, 38, 54, SCREEN, seed + 2, shadow=False, lw=1.4)
        c.set_source_rgb(0.62, 0.66, 0.72); c.set_line_width(2.0); c.set_line_cap(1)
        for yy, x1 in ((-19, 10), (-13, 4)):
            c.move_to(-13, yy); c.line_to(x1, yy); c.stroke()
        ellipse(k, 0, 8, 12.5, 12.5, (0.30, 0.74, 0.46), seed + 5, shadow=False, lw=1.6)   # the one button
        if kind == "print":                                                 # his thumb, in oil, on it
            c.save(); c.translate(1, 8); c.rotate(-0.35); c.scale(1.0, 1.3)
            c.set_source_rgba(*OIL, 0.88); c.arc(0, 0, 8.2, 0, 2 * math.pi); c.fill()
            c.set_source_rgba(0.62, 0.55, 0.48, 0.9); c.set_line_width(1.0)
            for r in (2.0, 4.0, 6.0):
                c.arc(0, 1.5, r, 3.5, 6.0); c.stroke()
            c.restore()
    c.restore()


def _face(orig, special):
    def builder(inner, blush, sp=None):
        base = orig(inner, blush, sp)

        def face(k, x, y, kind="neutral", look=(0, 0), seed=0):
            c = k.c
            base(k, x, y, kind, look, seed)
            my = y + 29
            if special in ("appraise", "breath"):                       # a small closed smile, one corner up
                ellipse(k, x, my, 20, 11.5, SKIN, seed + 74, shadow=False, outline=False)
                for col, w in ((INK, 6.6), (RED, 4.3)):
                    c.set_source_rgb(*col); c.set_line_width(w); c.set_line_cap(1)
                    c.move_to(x - 7, my + 0.5); c.curve_to(x - 2, my + 3.2, x + 3, my + 2.8, x + 8, my - 2.0); c.stroke()
                c.set_source_rgb(*INK); c.set_line_width(1.6)
                c.move_to(x + 10, my - 5.5); c.line_to(x + 12, my - 2); c.stroke()
                c.set_source_rgba(1, 1, 1, 0.75); c.set_line_width(1.4); c.move_to(x - 2.5, my + 1.9); c.line_to(x + 1.5, my + 1.8); c.stroke()
            elif special == "oh":                                       # a small soft O, a little long
                ellipse(k, x, my, 20, 11.5, SKIN, seed + 75, shadow=False, outline=False)
                ellipse(k, x + 1, my + 1, 4.6, 6.2, (0.45, 0.06, 0.08), seed + 76, shadow=False, lw=1.8)
                c.set_source_rgb(*RED); c.set_line_width(3.2); c.save(); c.translate(x + 1, my + 1); c.scale(6.0, 7.6)
                c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.stroke()
        return face
    return builder


def _hook(orig):
    def builder(badge):
        base = orig(badge)

        def hook(k, body_top, seed):
            base(k, body_top, seed)
            strand(k, seed)
        return hook
    return builder


def sofia(k, x, feet, s=1.0, pose="hold", face_kind="smile", look=(0, 0), lag=(0, 0), seed=7, badge=True, lean=0.0,
          mouth=None, sparkle=0.0, tablet_kind="auto"):
    """Returns {"head", "hands"} in canvas coordinates (lean not applied to the returned points).
    tablet_kind: "auto" (by pose: hold and necklace -> "hold", show -> "show", trophy -> "trophy"), or None."""
    special = face_kind if face_kind in SPECIAL else None
    kind = SPECIAL.get(face_kind, face_kind)
    tk = {"hold": "hold", "necklace": "hold", "show": "show", "trophy": "trophy"}.get(pose) if tablet_kind == "auto" else tablet_kind
    old = (sbc.POSES, sbc.fringe, sbc._face, sbc._hook)
    poses = dict(sbc.POSES); poses.update(POSES)
    sbc.POSES, sbc.fringe, sbc._face, sbc._hook = poses, drop, _face(old[2], special), _hook(old[3])
    try:
        out = sbc.sofia(k, x, feet, s, pose, kind, look, lag, seed, badge, lean, mouth, sparkle)
    finally:
        sbc.POSES, sbc.fringe, sbc._face, sbc._hook = old
    a = poses[pose]
    d = lambda g: (math.sin(math.radians(g)), math.cos(math.radians(g)))
    arms = []
    for i in (0, 1):
        sx, sy = SH[i]
        ex, ey = sx + d(a[2 * i])[0] * LN, sy + d(a[2 * i])[1] * LN
        hx, hy = ex + d(a[2 * i] + a[2 * i + 1])[0] * LN, ey + d(a[2 * i] + a[2 * i + 1])[1] * LN
        arms.append((ex, ey, hx, hy))
    c = k.c
    c.save(); c.translate(x, feet); c.rotate(math.radians(lean)); c.scale(s, s)
    ex, ey, hx, hy = arms[0]
    ux, uy = (hx - ex) / LN, (hy - ey) / LN
    if tk == "hold":                                                    # against her, the sheet toward us
        tablet(k, hx + 20, hy - 12, -0.10, "back", seed + 80)
    elif tk == "show":                                                  # turned to him, at arm's length
        tablet(k, hx - 14, hy - 34, -0.14, "form", seed + 80)
    elif tk == "trophy":                                                # held up beside her, the print to us
        tablet(k, hx - 10, hy - 34, -0.10, "print", seed + 80)
    if tk in ("hold", "show", "trophy"):                                          # her hand again, over the tablet
        ellipse(k, hx, hy, 9, 9, SKIN, seed + 81, shadow=False, lw=2)
        ellipse(k, hx + ux * 7, hy + uy * 7, 3.2, 3.2, RED, seed + 82, shadow=False, outline=False)
    px, py = -uy, ux                                                    # the bracelet, across her screen-left wrist
    wx, wy = hx - ux * 12.5, hy - uy * 12.5
    c.set_source_rgb(*INK); c.set_line_width(1.2); c.move_to(wx + px * 8, wy + py * 8); c.line_to(wx - px * 8, wy - py * 8); c.stroke()
    for i, t in enumerate((-6.6, -2.2, 2.2, 6.6)):
        pearl(k, wx + px * t, wy + py * t, 3.3, seed + 90 + i, lw=1.3)
    if pose == "necklace":                                              # two fingers of the other hand on the strand
        _, _, rx, ry = arms[1]
        for (fx, fy) in ((8.0, BODY_TOP + 25.0), (13.5, BODY_TOP + 23.5)):
            for col, w in ((INK, 8.4), (SKIN, 5.6)):
                c.set_source_rgb(*col); c.set_line_width(w); c.set_line_cap(1)
                c.move_to(rx - 2, ry - 4); c.line_to(fx, fy); c.stroke()
            ellipse(k, fx - 0.6, fy - 1.0, 2.4, 2.4, RED, seed + 95, shadow=False, outline=False)
        ellipse(k, rx, ry, 8.6, 8.6, SKIN, seed + 96, shadow=False, lw=2)
    c.restore()
    return out
