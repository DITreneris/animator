"""(pinned: mom v3 look v1) MOM, "First Search" (episode 10): v3, the mask off. In "The Best Candidate" she came to the interview dressed as a
sweet old lady (mom_bc: the pillbox hat, the teal wool coat). Now she has the job (ASSISTANT TO DON) and the office is
hers. Picked by Tomas (19 Nov):
- a boxy teal skirt suit with shoulder pads: the jacket to the hip, mustard notched lapels and piping, two big mustard
  buttons, a darker teal pencil skirt; the cream blouse buttoned to the top;
- the brooch grown into an order: a mustard star with the housecoat flower on it and two striped ribbon tails;
- the hat gone: the set grey curls and the ONE forgotten lilac curler (her mark since Office Noir), now in plain view;
- the same heavy glasses on the pearl chain, darker plum lips;
- her desk: the mug (WORLD'S BEST MOM, the heir of Office Noir's #1 MOM), a candy dish (for Pam only), her knitting
  (a scarf for Don).
Faces: everything mom_bc has ("sweet" for Pam and Don; mom_on's stern, unimpressed, shout, proud) and one new:
"glare", for Sofía and the robot: the glasses slid down her nose, the eyes over the top of the frames, heavy lids,
brows down at the middle, the lips pressed thin.
mom_bc.py and mom_on.py are untouched: their functions are swapped for the length of one call and restored.
Usage: o = mom(k, x, feet, s, pose, face, look, mouth=None, lean=0, bag=None) -> {"head", "hands"}
       mug(k, x, y, s), candy(k, x, y, s), knitting(k, x, y, s)"""
import math
import kit
import mom_on as mo
import mom_bc as mb
from kit import INK, cut, rect, ellipse

TEAL, TEAL_DARK, MUSTARD, MUSTARD_DARK, CREAM = mo.TEAL, mo.TEAL_DARK, mo.MUSTARD, mo.MUSTARD_DARK, mo.CREAM
SKIN, HAIR, HAIR_DARK, LEGS = mo.SKIN, mo.HAIR, mo.HAIR_DARK, mo.LEGS
BT, HY, HEM, SH_X, WAIST = mo.BT, mo.HY, mo.HEM, mo.SH_X, mo.SASH
SKIRT = (0.10, 0.36, 0.38)
PLUM = (0.50, 0.16, 0.32)
JACKET_HEM = WAIST + 46
POSES = mb.POSES


def _hair_nohat(curler):
    """mom_bc's hair without the pillbox hat: the set curls, the one curler."""
    def draw(k, seed, back=False):
        c = k.c
        top = HY - 58
        for sx in (-1, 1):
            c.new_path()
            c.move_to(sx * 50, HY - 28); c.curve_to(sx * 66, HY - 16, sx * 64, HY + 10, sx * 54, HY + 18)
            c.line_to(sx * 46, HY + 6); c.line_to(sx * 46, HY - 26); c.close_path()
            mo._fill_stroke(c, HAIR, 2.2)
        c.new_path()
        c.move_to(-56, HY - 22); c.curve_to(-62, top - 8, 62, top - 8, 56, HY - 22)
        c.curve_to(30, HY - 34, -30, HY - 34, -56, HY - 22); c.close_path()
        mo._fill_stroke(c, HAIR, 2.4)
        for i in range(9):                                              # the set curls, a full crown now
            u = i / 8.0
            cx = -50 + 100 * u
            cy = HY - 30 - 22 * math.sin(math.pi * u)
            c.new_path(); c.arc(cx, cy, 10.5, 0, 2 * math.pi); mo._fill_stroke(c, HAIR, 2.0)
            c.set_source_rgb(*HAIR_DARK); c.set_line_width(1.4)
            c.new_path(); c.arc(cx, cy, 5, 0.2 * math.pi, 1.5 * math.pi); c.stroke()
        if curler:                                                      # the one she missed, in plain view
            mo._curler(c, -54, top - 2, 44, -0.9, big=True)
    return draw


def _faces(inner_eyes, inner_brows, inner_mouth):
    """mom_bc's sweet, plus the glare."""
    sweet_eyes, sweet_brows, sweet_mouth = mb._sweet(inner_eyes, inner_brows, inner_mouth)

    def eyes(c, face, look, turn=0.0):
        if face != "glare":
            return sweet_eyes(c, face, look, turn)
        ey = HY - 8                                                     # over the top of the frames
        for sx in (-1, 1):
            x = sx * 20 + turn
            c.new_path(); c.save(); c.translate(x, ey); c.scale(9.5, 7.5); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
            mo._fill_stroke(c, (1, 1, 1), 2.0)
            c.new_path(); c.arc(x + look[0] * 3.8, ey + 1.5, 3.8, 0, 2 * math.pi); c.set_source_rgb(*INK); c.fill()
            c.save(); c.new_path(); c.save(); c.translate(x, ey); c.scale(10.5, 8.5); c.arc(0, 0, 1, 0, 2 * math.pi)
            c.restore(); c.clip()
            c.new_path(); c.rectangle(x - 14, ey - 14, 28, 13.5)                              # the heavy lid, half down
            c.set_source_rgb(*mo.SKIN_SHADE); c.fill(); c.restore()
            c.set_source_rgb(*INK); c.set_line_width(3.0)
            c.new_path(); c.move_to(x - 11, ey - 0.5); c.line_to(x + 11, ey - 0.5); c.stroke()

    def brows(c, face, turn=0.0):
        if face != "glare":
            return sweet_brows(c, face, turn)
        by = HY - 24
        c.set_source_rgb(*HAIR_DARK); c.set_line_width(5.6); c.set_line_cap(1)
        for sx in (-1, 1):
            x = sx * 20 + turn
            c.new_path(); c.move_to(x - sx * 10, by + 9); c.line_to(x + sx * 12, by - 3); c.stroke()
        c.set_line_cap(0)

    def mouth(c, face, m, turn=0.0):
        if face != "glare":
            return sweet_mouth(c, face, m, turn)
        inner_mouth(c, "stern", "M", turn)                              # nose and jaw lines; then the lips, pressed thin
        my = HY + 30
        c.set_source_rgb(*mo.SKIN); c.rectangle(turn - 16, my - 4, 32, 10); c.fill()
        c.set_source_rgb(*PLUM); c.set_line_width(3.4); c.set_line_cap(1)
        c.new_path(); c.move_to(turn - 9, my + 2); c.line_to(turn + 9, my + 2); c.stroke()
        c.set_source_rgb(*mo.SKIN_SHADE); c.set_line_width(1.2)                            # the purse lines
        for dx in (-6, -2, 2, 6):
            c.new_path(); c.move_to(turn + dx, my - 3); c.line_to(turn + dx, my - 0.5); c.stroke()
        c.set_line_cap(0)
    return eyes, brows, mouth


def _glasses_low(inner):
    def g(c, turn=0.0, with_chain=True):
        c.save(); c.translate(0, 10)                                    # slid down her nose
        inner(c, turn, with_chain)
        c.restore()
    return g


def _suit(k, seed):
    c = k.c
    sk = [(-SH_X - 4, JACKET_HEM - 6), (SH_X + 4, JACKET_HEM - 6), (SH_X + 2, HEM), (-SH_X - 2, HEM)]
    cut(k, sk, SKIRT, lw=2.2)                                           # the pencil skirt
    c.set_source_rgb(*INK); c.set_line_width(1.6)
    c.new_path(); c.move_to(8, HEM); c.line_to(8, HEM - 16); c.stroke()                             # its slit
    r = k.rng(seed)
    pts = [(-SH_X - 19, BT + 10), (-SH_X - 16, BT - 9), (SH_X + 16, BT - 9), (SH_X + 19, BT + 10),
           (SH_X + 15, JACKET_HEM), (-SH_X - 15, JACKET_HEM)]
    cut(k, [(px + r.uniform(-1, 1), py + r.uniform(-1, 1)) for px, py in pts], TEAL)                  # the boxy jacket
    c.set_source_rgb(*MUSTARD); c.set_line_width(3.0)                                                 # mustard piping
    c.new_path(); c.move_to(-SH_X - 12, JACKET_HEM - 4); c.line_to(SH_X + 12, JACKET_HEM - 4); c.stroke()
    c.set_source_rgb(*mo.TEAL_DARK); c.set_line_width(2.2)                                            # the pads' seams
    for sx in (-1, 1):
        c.new_path(); c.move_to(sx * (SH_X - 4), BT - 9); c.curve_to(sx * (SH_X + 2), BT + 2, sx * (SH_X + 2), BT + 12,
                                                                 sx * (SH_X - 2), BT + 22); c.stroke()
    c.new_path(); c.move_to(-14, BT - 6); c.line_to(0, BT + 40); c.line_to(14, BT - 6); c.close_path()
    mo._fill_stroke(c, CREAM, 1.8)                                                                    # the blouse
    for i, by in enumerate((BT + 4, BT + 16, BT + 28)):
        c.new_path(); c.arc(0, by, 1.8, 0, 2 * math.pi); c.set_source_rgb(*INK); c.fill()
    for sx in (-1, 1):                                                                                # notched lapels
        c.new_path(); c.move_to(sx * 16, BT - 7); c.line_to(sx * 34, BT - 4); c.line_to(sx * 30, BT + 16)
        c.line_to(sx * 40, BT + 22); c.line_to(sx * 4, WAIST - 6); c.line_to(sx * 2, BT + 42); c.close_path()
        mo._fill_stroke(c, MUSTARD, 2.0)
    for i, by in enumerate((WAIST + 6, WAIST + 28)):                                                  # two big buttons
        ellipse(k, -8, by, 8, 8, MUSTARD, seed + 30 + i, shadow=False, lw=2)
        c.set_source_rgb(*MUSTARD_DARK)
        for dx in (-2.4, 2.4):
            c.new_path(); c.arc(-8 + dx, by, 1.3, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(1.8)
    c.new_path(); c.move_to(4, WAIST - 6); c.line_to(6, JACKET_HEM); c.stroke()                      # the front edge
    for sx in (-1, 1):
        rect(k, sx * 36 - 14, WAIST + 22, 28, 8, TEAL, seed + 36 + sx, shadow=False, lw=1.8)         # pocket flaps
    order(k, 30, BT + 26, 1.15, seed + 40)


def order(k, x, y, s=1.0, seed=0):
    """The brooch grown into an order: striped ribbon tails, a mustard star, the housecoat flower on it."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    for sx in (-1, 1):
        cut(k, [(sx * 2, 0), (sx * 12, 2), (sx * 15, 34), (sx * 9, 28), (sx * 4, 36)], TEAL_DARK, shadow=False, lw=1.6)
        c.set_source_rgb(*MUSTARD); c.set_line_width(2.2)
        c.new_path(); c.move_to(sx * 7, 2); c.line_to(sx * 9.5, 30); c.stroke()
    c.new_path()
    for i in range(16):
        a = math.pi * 2 * i / 16 - math.pi / 2
        rr = 19 if i % 2 == 0 else 12
        (c.move_to if i == 0 else c.line_to)(rr * math.cos(a), rr * math.sin(a))
    c.close_path(); mo._fill_stroke(c, MUSTARD, 2.0)
    mo.flower(c, 0, 0, 9, 0.2)
    c.set_source_rgb(1, 1, 1); c.new_path(); c.arc(-9, -9, 2.2, 0, 2 * math.pi); c.fill()                # the shine
    c.restore()


def _head_fs(k, face, look, mouth, seed):
    g = mo._glasses
    if face == "glare":
        mo._glasses = _glasses_low(g)
    try:
        mo._head(k, face, look, mouth, seed, "front")
    finally:
        mo._glasses = g


def _build():
    """mom_bc.mom's own source, with the coat block swapped for the suit, the hat hair for the bare curls, the faces
    for _faces: mom_bc's arms, hands, poses and handbag stay exactly its own."""
    import inspect
    src = inspect.getsource(mb.mom)
    a, b = src.index("    pts = mo._coat_pts(k, seed)"), src.index("    tdx, tdy, tsc")
    src = src[:a] + "    _suit(k, seed)\n" + src[b:]
    for x, y in (("_hair_hat(curler)", "_hair_nohat(curler)"), ("_sweet(old[1], old[2], old[3])", "_faces(old[1], old[2], old[3])"),
                 ('mo._head(k, face, look, mouth, seed, "front")', "_head_fs(k, face, look, mouth, seed)")):
        assert x in src, x
        src = src.replace(x, y)
    ns = dict(vars(mb))
    ns.update(_suit=_suit, _hair_nohat=_hair_nohat, _faces=_faces, _head_fs=_head_fs)
    exec(src, ns)
    return ns["mom"]


_body = _build()


def mom(k, x, feet, s=1.0, pose="bag", face="sweet", look=(0, 0), seed=70, mouth=None, lean=0.0, thrust=0.0, bag=None,
        curler=True, tilt=None):
    """The v3 Mom: mom_bc's signature and poses; the suit, the bare curls, the plum lips, the glare."""
    old = mo.MAUVE
    mo.MAUVE = PLUM
    try:
        return _body(k, x, feet, s, pose, face, look, seed, mouth, lean, thrust, bag, curler, tilt)
    finally:
        mo.MAUVE = old


def mug(k, x, y, s=1.0, seed=0):
    """WORLD'S BEST MOM: the heir of Office Noir's #1 MOM mug, bigger letters."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    c.new_path(); c.arc(22, 2, 12, -math.pi / 2, math.pi / 2); c.set_source_rgb(*INK); c.set_line_width(9); c.stroke()
    c.new_path(); c.arc(22, 2, 12, -math.pi / 2, math.pi / 2); c.set_source_rgb(1, 1, 1); c.set_line_width(5); c.stroke()
    mo._rrect(c, -22, -26, 44, 54, 5); mo._fill_stroke(c, (1, 1, 1), 2.4)
    c.new_path(); c.save(); c.translate(0, -26); c.scale(22, 5); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    mo._fill_stroke(c, (0.42, 0.27, 0.16), 1.6)
    kit.text(k, "WORLD'S", 0, -8, 9, TEAL_DARK)
    kit.text(k, "BEST", 0, 4, 11, TEAL_DARK)
    kit.text(k, "MOM", 0, 18, 13, (0.80, 0.10, 0.20))
    c.restore()


def candy(k, x, y, s=1.0, seed=0):
    """A cut-glass candy dish, wrapped sweets: for Pam."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    cols = [(0.90, 0.20, 0.30), MUSTARD, TEAL, (0.60, 0.40, 0.80), (0.95, 0.55, 0.20)]
    for i, (cx, cy) in enumerate(((-16, -10), (-2, -14), (12, -10), (-9, -4), (6, -4))):
        c.save(); c.translate(cx, cy); c.rotate(0.4 * i)
        cut(k, [(-11, -3), (-6, -6), (-6, 6), (-11, 3)], cols[i], shadow=False, lw=1.2)
        cut(k, [(11, -3), (6, -6), (6, 6), (11, 3)], cols[i], shadow=False, lw=1.2)
        ellipse(k, 0, 0, 7, 6, cols[i], seed + i, shadow=False, lw=1.4)
        c.restore()
    cut(k, [(-30, -4), (30, -4), (20, 14), (-20, 14)], (0.80, 0.90, 0.95), lw=2)
    c.set_source_rgba(1, 1, 1, 0.8); c.set_line_width(1.6)
    for dx in (-18, -6, 6, 18):
        c.new_path(); c.move_to(dx, -2); c.line_to(dx * 0.7, 12); c.stroke()
    rect(k, -10, 14, 20, 8, (0.80, 0.90, 0.95), seed + 9, shadow=False, lw=1.8)
    c.restore()


def knitting(k, x, y, s=1.0, seed=0):
    """Two needles in a scarf for Don (teal and mustard stripes), the ball of yarn."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    for i in range(5):
        cut(k, [(-30, -10 + i * 8), (24, -10 + i * 8), (24, -2 + i * 8), (-30, -2 + i * 8)],
            TEAL if i % 2 == 0 else MUSTARD, shadow=False, lw=1.2)
    c.set_source_rgb(*INK); c.set_line_width(1.0)
    for i in range(6):
        for j in range(5):
            c.new_path(); c.move_to(-26 + i * 9, -8 + j * 8); c.line_to(-22 + i * 9, -4 + j * 8); c.line_to(-18 + i * 9, -8 + j * 8)
            c.stroke()
    for a in (-0.5, -0.8):
        c.save(); c.rotate(a)
        c.set_source_rgb(*INK); c.set_line_width(5); c.new_path(); c.move_to(-10, -14); c.line_to(52, -14); c.stroke()
        c.set_source_rgb(0.75, 0.75, 0.80); c.set_line_width(3); c.new_path(); c.move_to(-10, -14); c.line_to(52, -14); c.stroke()
        ellipse(k, 54, -14, 4, 4, (0.80, 0.10, 0.20), seed + 3, shadow=False, lw=1.2)
        c.restore()
    ellipse(k, 44, 26, 15, 15, TEAL, seed + 5, lw=2)
    c.set_source_rgb(*mo.TEAL_DARK); c.set_line_width(1.4)
    for a in (0.3, 1.0, 1.7):
        c.new_path(); c.arc(44, 26, 12, a, a + 1.6); c.stroke()
    c.set_source_rgb(*TEAL); c.set_line_width(2)
    c.new_path(); c.move_to(30, 22); c.curve_to(26, 12, 26, 6, 24, 0); c.stroke()
    c.restore()
