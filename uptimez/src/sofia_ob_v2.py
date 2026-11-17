"""v2, pinned. SOFIA, "The Onboarding", v2 (sofia_ob_v1.py = v1, kept), after the performance audit (17 Nov): the design is kept,
the acting is corrected. What a viewer has to see is her going from professional, to interested, to back in control.
- EYES DOWN / EYES UP are drawn here, not borrowed: the lids sit a little higher (a third of the eye, not half) and the
  pupils are smaller, so they can travel. Down: on the lower rim, white above them. Up: tucked against the lid,
  white below them. look=(lx, 1) is down, look=(lx, -0.2) is up; the lids, the brows and the mouth do not move;
- the hand on the pearls is a hand: the wrist out to the side, the index and middle fingers apart, lifting ONE pearl
  (the strand moves with it); the other fingers curled. v1 was a ball with two red marks;
- "Oh..." is not a round mouth (that is surprise, and it is Don's): the lips part a little, one corner higher;
- "real" (new): the one thing she would rather hide. Half a second in beat 06: the lower lids pushed up by her cheeks,
  an open smile with teeth, no blush. She catches it with "tiny" and a glance at who noticed;
- the strand is a little shorter and higher, clear of the badge; in "necklace" the tablet hangs at her side in her
  other hand, so the close-up has the pearls, the fingers and nothing else;
- "low" (new pose): both arms down, the tablet hanging at her side: for the close shots of her face;
- THE PEARL RULE, for every episode: untouched = composed; two fingers lift one pearl = interested; "lapel" (new pose:
  she lets go and smooths her lapel with a flat hand) = she has won. Once an episode at most.
Below, the notes of v1, which hold except where the list above replaces them.
SOFIA, "The Onboarding", v1. Her office look from The Best Candidate (sofia_bc: teal wrap blouse, ink-navy blazer,
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
LOW = sbc.POSES["stand"][:2]                              # the tablet arm, lowered: the tablet hangs at her side
POSES = {
    "hold": CARRY + REST,
    "low": LOW + REST,
    "necklace": LOW + _ik(1, 27, BODY_TOP + 42),
    "lapel": LOW + _ik(1, 25, BODY_TOP + 60),
    "show": _ik(-1, -104, BODY_TOP + 52) + REST,
    "trophy": _ik(-1, -62, BODY_TOP + 66) + REST,
}
SPECIAL = {"appraise": "unimpressed", "oh": "unimpressed", "breath": "closed", "real": "smile"}
LIFT = 5                                                  # the pearl her fingers lift
_lift = [False]


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


def strand_pts(n=9, lift=False):
    """The strand: a shallow curve from lapel to lapel, lowest in the middle, just under her chin and clear of the
    badge. lift: her fingers are under one pearl, which sits higher, and its neighbours follow."""
    out = []
    for i in range(n):
        t = i / float(n - 1) * 2 - 1
        up = (4.5 if i == LIFT else 1.8 if abs(i - LIFT) == 1 else 0.0) if lift else 0.0
        out.append((t * 25.5, BODY_TOP + 9 + 14.0 * (1 - t * t) - up))
    return out


def strand(k, seed):
    pts = strand_pts(lift=_lift[0])
    c = k.c
    c.set_source_rgb(*INK); c.set_line_width(1.4)
    c.move_to(*pts[0])
    for q in pts[1:]:
        c.line_to(*q)
    c.stroke()
    order = sorted(range(len(pts)), key=lambda i: -abs(pts[i][0]))           # the middle pearls on top
    for i in order:
        pearl(k, pts[i][0], pts[i][1], 4.3, seed + 60 + i)


def _eyes(k, x, y, look, seed):
    """Her appraising eyes: lids over the top third, small pupils that travel from the lower rim to under the lid."""
    c = k.c
    lx, ly = look
    r = 11.5
    t = min(1.0, max(0.0, (ly + 0.2) / 1.2))
    for sx in (-17, 17):
        o = -1 if sx < 0 else 1
        c.save(); c.rectangle(x + sx - 22, y - 13.5, 44, 29); c.clip()                 # the borrowed eye, covered
        ellipse(k, x + sx, y - 1, r + 8.5, r + 5, SKIN, seed + sx + 40, shadow=False, outline=False)
        c.restore()
        ellipse(k, x + sx, y, r, r, (1, 1, 1), seed + sx, shadow=False, lw=2)
        px_, py_ = x + sx + lx * (6.6 - 2.6 * t), y - 0.4 + 7.0 * t
        c.save(); c.arc(x + sx, y, r - 0.8, 0, 2 * math.pi); c.clip()
        ellipse(k, px_, py_, 4.7, 4.7, INK, seed + sx + 1, shadow=False, outline=False)
        c.set_source_rgb(1, 1, 1); c.arc(px_ + 1.6, py_ - 1.7, 1.4, 0, 2 * math.pi); c.fill()
        c.restore()
        c.save(); c.rectangle(x + sx - 16, y - 17, 32, 13); c.clip()                      # the lid: the top third
        ellipse(k, x + sx, y, r + 3, r + 3, SKIN, seed + sx + 2, shadow=False, outline=False)
        c.restore()
        c.set_source_rgb(*INK); c.set_line_width(3.5); c.set_line_cap(1)
        c.move_to(x + sx - 10.6, y - 4); c.line_to(x + sx + 10.6, y - 4); c.stroke()
        c.set_line_width(3.4)
        c.move_to(x + sx + o * (r - 1), y - 4); c.line_to(x + sx + o * (r + 7), y - 10); c.stroke()
        c.set_line_width(2.4)
        for ax in (5, 9):
            c.move_to(x + sx + o * ax, y - 4); c.line_to(x + sx + o * (ax + 2.5), y - 7.5); c.stroke()


def _fingers(k, hx, hy, tips, seed, flat=False, roots=None):
    """A hand over the kit's round one at (hx, hy). tips: where the fingertips end. Two fingers apart with the rest
    curled (the pearl), or flat=True: four together (the lapel)."""
    c = k.c
    n = len(tips)
    roots = roots or [(hx - 5.5 + 9.0 * i / max(1, n - 1), hy - 4.5 - (1.5 if 0 < i < n - 1 else 0)) for i in range(n)]
    for (ax, ay), (bx, by) in zip(roots, tips):
        for col, w in ((INK, 7.6 if not flat else 6.6), (SKIN, 4.9 if not flat else 4.0)):
            c.set_source_rgb(*col); c.set_line_width(w); c.set_line_cap(1)
            c.move_to(ax, ay); c.line_to(bx, by); c.stroke()
        d = math.hypot(bx - ax, by - ay)
        ux, uy = (bx - ax) / d, (by - ay) / d
        c.set_source_rgb(*RED); c.set_line_width(4.0 if not flat else 3.3); c.set_line_cap(1)          # the nail
        c.move_to(bx - ux * 2.4, by - uy * 2.4); c.line_to(bx + ux * 0.4, by + uy * 0.4); c.stroke()
    ellipse(k, hx, hy, 9.4, 8.2, SKIN, seed, shadow=False, lw=2)
    if not flat:                                                            # the other fingers, curled into the palm
        c.set_source_rgb(*INK); c.set_line_width(1.6); c.set_line_cap(1)
        c.arc(hx - 2.5, hy + 2.5, 3.6, 0.2, 2.6); c.stroke()
        c.arc(hx + 3.0, hy + 3.0, 3.2, 0.2, 2.4); c.stroke()


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
            if special in ("appraise", "oh"):
                _eyes(k, x, y, look, seed)
            if special == "real":                                       # her cheeks push the lower lids up
                for sx in (-17, 17):
                    c.save(); c.arc(x + sx, y, 12.4, 0, 2 * math.pi); c.clip()
                    c.move_to(x + sx - 13, y + 8.5); c.curve_to(x + sx - 5, y + 3.2, x + sx + 5, y + 3.2, x + sx + 13, y + 8.5)
                    c.line_to(x + sx + 13, y + 14); c.line_to(x + sx - 13, y + 14); c.close_path()
                    c.set_source_rgb(*SKIN); c.fill()
                    c.restore()
                    c.set_source_rgb(*INK); c.set_line_width(2.2); c.set_line_cap(1)
                    c.move_to(x + sx - 10.5, y + 7.2); c.curve_to(x + sx - 4, y + 3.6, x + sx + 4, y + 3.6, x + sx + 10.5, y + 7.2); c.stroke()
                ellipse(k, x, my - 2, 23, 13.5, SKIN, seed + 77, shadow=False, outline=False)
                c.move_to(x - 14, my - 6); c.curve_to(x - 6, my - 3.5, x + 6, my - 3.5, x + 14, my - 6)
                c.curve_to(x + 11, my + 9.5, x - 11, my + 9.5, x - 14, my - 6); c.close_path()
                c.set_source_rgb(1, 1, 1); c.fill_preserve()
                c.set_source_rgb(*RED); c.set_line_width(4.4); c.set_line_join(1); c.stroke()
            if special in ("appraise", "breath"):                       # a small closed smile, one corner up
                ellipse(k, x, my, 20, 11.5, SKIN, seed + 74, shadow=False, outline=False)
                for col, w in ((INK, 6.6), (RED, 4.3)):
                    c.set_source_rgb(*col); c.set_line_width(w); c.set_line_cap(1)
                    c.move_to(x - 7, my + 0.5); c.curve_to(x - 2, my + 3.2, x + 3, my + 2.8, x + 8, my - 2.0); c.stroke()
                c.set_source_rgb(*INK); c.set_line_width(1.6)
                c.move_to(x + 10, my - 5.5); c.line_to(x + 12, my - 2); c.stroke()
                c.set_source_rgba(1, 1, 1, 0.75); c.set_line_width(1.4); c.move_to(x - 2.5, my + 1.9); c.line_to(x + 1.5, my + 1.8); c.stroke()
            elif special == "oh":                                       # the lips part a little; one corner higher
                ellipse(k, x, my, 20, 11.5, SKIN, seed + 75, shadow=False, outline=False)
                c.save(); c.translate(x + 0.5, my + 0.8); c.rotate(-0.10); c.scale(5.6, 2.9)
                c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
                c.set_source_rgb(0.45, 0.06, 0.08); c.fill()
                c.set_source_rgb(*RED); c.set_line_cap(1)
                c.set_line_width(3.4)                                   # the upper lip
                c.move_to(x - 7.5, my - 0.6); c.curve_to(x - 3.5, my - 4.6, x + 3.5, my - 5.0, x + 8.5, my - 3.0); c.stroke()
                c.set_line_width(4.6)                                   # the lower lip, fuller
                c.move_to(x - 7.0, my + 1.2); c.curve_to(x - 3.0, my + 7.0, x + 4.0, my + 6.4, x + 8.5, my - 1.4); c.stroke()
                c.set_source_rgb(*INK); c.set_line_width(1.5)
                c.move_to(x + 10.5, my - 5.5); c.line_to(x + 12.3, my - 2.4); c.stroke()
                c.set_source_rgba(1, 1, 1, 0.75); c.set_line_width(1.4); c.move_to(x - 2.5, my + 4.6); c.line_to(x + 1.5, my + 4.6); c.stroke()
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
    tablet_kind: "auto" (by pose: hold -> "hold", low, necklace and lapel -> "low", show -> "show", trophy -> "trophy"),
    or None."""
    special = face_kind if face_kind in SPECIAL else None
    kind = SPECIAL.get(face_kind, face_kind)
    tk = {"hold": "hold", "low": "low", "necklace": "low", "lapel": "low", "show": "show", "trophy": "trophy"}.get(pose) if tablet_kind == "auto" else tablet_kind
    _lift[0] = pose == "necklace"
    old = (sbc.POSES, sbc.fringe, sbc._face, sbc._hook)
    poses = dict(sbc.POSES); poses.update(POSES)
    sbc.POSES, sbc.fringe, sbc._face, sbc._hook = poses, drop, _face(old[2], special), _hook(old[3])
    try:
        out = sbc.sofia(k, x, feet, s, pose, kind, look, lag, seed, badge, lean, mouth, sparkle)
    finally:
        sbc.POSES, sbc.fringe, sbc._face, sbc._hook = old
        _lift[0] = False
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
    if tk == "low":                                                     # hanging at her side, the sheet toward us
        tablet(k, hx - 3, hy + 24, 0.06, "back", seed + 80)
    if tk == "hold":                                                    # against her, the sheet toward us
        tablet(k, hx + 20, hy - 12, -0.10, "back", seed + 80)
    elif tk == "show":                                                  # turned to him, at arm's length
        tablet(k, hx - 14, hy - 34, -0.14, "form", seed + 80)
    elif tk == "trophy":                                                # held up beside her, the print to us
        tablet(k, hx - 10, hy - 34, -0.10, "print", seed + 80)
    if tk in ("hold", "show", "trophy", "low"):                                          # her hand again, over the tablet
        ellipse(k, hx, hy, 9, 9, SKIN, seed + 81, shadow=False, lw=2)
        ellipse(k, hx + ux * 7, hy + uy * 7, 3.2, 3.2, RED, seed + 82, shadow=False, outline=False)
    px, py = -uy, ux                                                    # the bracelet, across her screen-left wrist
    wx, wy = hx - ux * 12.5, hy - uy * 12.5
    c.set_source_rgb(*INK); c.set_line_width(1.2); c.move_to(wx + px * 8, wy + py * 8); c.line_to(wx - px * 8, wy - py * 8); c.stroke()
    for i, t in enumerate((-6.6, -2.2, 2.2, 6.6)):
        pearl(k, wx + px * t, wy + py * t, 3.3, seed + 90 + i, lw=1.3)
    if pose == "necklace":                                              # two fingers, apart, under one pearl
        _, _, rx, ry = arms[1]
        qx, qy = strand_pts(lift=True)[LIFT]
        dd = math.hypot(qx - rx, qy - ry)
        ux, uy = (qx - rx) / dd, (qy - ry) / dd
        px_, py_ = -uy, ux
        tips = [(qx - ux * 5.2 + px_ * g, qy - uy * 5.2 + py_ * g) for g in (-4.2, 4.2)]
        _fingers(k, rx, ry, tips, seed + 96, roots=[(rx + ux * 4 + px_ * g, ry + uy * 4 + py_ * g) for g in (-3.4, 3.4)])
    elif pose == "lapel":                                               # a flat hand down the lapel
        _, _, rx, ry = arms[1]
        _fingers(k, rx, ry, [(rx - 13.5, ry + 8.5), (rx - 11.5, ry + 12.0), (rx - 8.5, ry + 14.5), (rx - 5.0, ry + 15.5)],
                 seed + 97, flat=True)
    c.restore()
    return out
