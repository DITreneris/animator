"""v2 (mom_on3_v1.py = v1, kept), after the outside review of sheet v1 (19 Nov). The design is kept; less noise at
phone size, and a quieter "Approved.":
- the fur collar is four large lobes a side (v1: seven small ones), and the fur cuff is one band (v1: six lobes);
- mouth="dry": the bored mouth opened a crack, for one dry word (v1 used the shouting mouth shape);
- chain=False draws her glasses without the pearl chain, for wide shots (the chain stays everywhere else);
- pose "q_read": the hundred held up beside her eyes in her screen-left hand; she reads it, and nothing else moves.
MOM, "Office Noir 3: The Last Round", v1: the queen of the dark city (Tomas, 19 Nov, /grill-me).
In the Client's dream she drives the long black car, hands out the folder, takes the money and approves the punch.
What Tomas picked:
- a BLACK COAT with a FUR COLLAR over her suit; the brooch that became an order is pinned on the fur;
- a small black HAT, and under it the ONE forgotten curler (her mark since Office Noir);
- RINGS on every finger; a LONG CIGARETTE HOLDER;
- TAROT CARDS (symbols only, never words: the top card carries the Client's gear), she RAKES MONEY in with a
  croupier's rake, and she likes CHAMPAGNE (a coupe);
- her face is BORED: half-lidded, level brows, the mouth a short flat line. She does not look at the fight.
  Her eyes come up twice: "stern" for "Where are you going, skunk?", "glare" (mom_fs's) when she understands the glove.
Built as mom_fs is: mom_bc.mom's own source with the coat block, the hat hair and the faces swapped; mom_bc, mom_fs and
mom_on draw exactly as before.
Usage: o = queen(k, x, feet, s, pose, face, look, mouth=None, holder=False, cards=False, rake_=False, coupe=False,
                 note=False) -> {"head", "hands"}
Poses (new names): "q_stand", "q_holder", "q_cards", "q_rake", "q_lick" (the thumb, and the hundred in her other
hand), "q_toast", "q_wheel" (both hands high on the wheel)."""
import math
import inspect
import kit
import mom_on as mo
import mom_bc as mb
import mom_fs as mf
import client_ob as co
from kit import INK, cut, rect, ellipse

SKIN, HAIR, HAIR_DARK = mo.SKIN, mo.HAIR, mo.HAIR_DARK
BT, HY, HEM, SH_X, WAIST = mo.BT, mo.HY, mo.HEM, mo.SH_X, mo.SASH
COAT = (0.10, 0.10, 0.12)
SLEEVE = (0.17, 0.17, 0.20)                               # a tone up, so an arm across the coat still reads
COAT_LINE = (0.46, 0.46, 0.52)                             # its seams, lighter than the cloth
FUR = (0.90, 0.89, 0.86)                                   # silver fox: it frames her face against the black
FUR_SHADE = (0.62, 0.61, 0.60)
HAT = (0.08, 0.08, 0.10)
HAT_BAND = (0.36, 0.36, 0.40)
STOCKING = (0.42, 0.36, 0.34)
SHOE = (0.07, 0.07, 0.08)
PLUM = (0.38, 0.10, 0.22)
GOLD = (0.86, 0.68, 0.24)
GEM = (0.97, 0.98, 1.0)
HOLDER = (0.06, 0.06, 0.07)
NOTE = (0.90, 0.93, 0.86)
CARD = (0.97, 0.95, 0.90)
CARD_BACK = (0.22, 0.22, 0.27)


def _hair_queen(curler):
    """mom_bc's hair and curls; the pillbox hat is small and black, with a jewel; the one curler shows under it."""
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
        if curler:
            mo._curler(c, -60, HY - 34, 42, -1.0, big=True)
        for i in range(7):
            u = i / 6.0
            cx = -45 + 90 * u
            cy = HY - 27 - 9 * math.sin(math.pi * u)
            c.new_path(); c.arc(cx, cy, 9.5, 0, 2 * math.pi); mo._fill_stroke(c, HAIR, 2.0)
            c.set_source_rgb(*HAIR_DARK); c.set_line_width(1.4)
            c.new_path(); c.arc(cx, cy, 4.5, 0.2 * math.pi, 1.5 * math.pi); c.stroke()
        c.save(); c.translate(6, top + 4); c.rotate(0.10)                # the hat, tipped
        mo._rrect(c, -34, -24, 68, 34, 9); mo._fill_stroke(c, HAT, 2.4)
        c.new_path(); c.rectangle(-34, 0, 68, 9); mo._fill_stroke(c, HAT_BAND, 1.8)
        c.set_source_rgba(0.80, 0.80, 0.86, 0.9); c.set_line_width(2.0); c.set_line_cap(1)          # a light on its crown
        c.new_path(); c.move_to(-24, -17); c.line_to(6, -18); c.stroke(); c.set_line_cap(0)
        c.new_path()                                                    # its jewel
        for i in range(4):
            a = i * math.pi / 2
            (c.move_to if i == 0 else c.line_to)(22 + 8 * math.cos(a), 4 + 10 * math.sin(a))
        c.close_path(); mo._fill_stroke(c, GEM, 1.6)
        c.restore()
    return draw


def _faces(inner_eyes, inner_brows, inner_mouth):
    """mom_fs's faces (sweet, glare, mom_on's own), plus bored."""
    e0, b0, m0 = mf._faces(inner_eyes, inner_brows, inner_mouth)

    def eyes(c, face, look, turn=0.0):
        if face != "bored":
            return e0(c, face, look, turn)
        ey = HY - 4
        for sx in (-1, 1):
            x = sx * 20 + turn
            c.new_path(); c.save(); c.translate(x, ey); c.scale(9.0, 8.0); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
            mo._fill_stroke(c, (1, 1, 1), 2.0)
            c.new_path(); c.arc(x + look[0] * 3.5, ey + 4.2 + look[1] * 1.5, 3.8, 0, 2 * math.pi); c.set_source_rgb(*INK); c.fill()
            lid = 1.5                                                    # more than half shut
            c.save(); c.new_path(); c.save(); c.translate(x, ey); c.scale(10.0, 9.0); c.arc(0, 0, 1, 0, 2 * math.pi)
            c.restore(); c.clip()
            c.new_path(); c.rectangle(x - 14, ey - 14, 28, 14 + lid); c.set_source_rgb(*mo.SKIN_SHADE); c.fill(); c.restore()
            c.set_source_rgb(*INK); c.set_line_width(3.0); c.set_line_cap(1)
            c.new_path(); c.move_to(x - 10, ey + lid); c.line_to(x + 10, ey + lid); c.stroke(); c.set_line_cap(0)
            c.set_source_rgb(*mo.SKIN_SHADE); c.set_line_width(1.4)
            c.new_path(); c.arc(x, ey + 6, 8, 0.25 * math.pi, 0.75 * math.pi); c.stroke()

    def brows(c, face, turn=0.0):
        if face != "bored":
            return b0(c, face, turn)
        by = HY - 22
        c.set_source_rgb(*HAIR_DARK); c.set_line_width(5.2); c.set_line_cap(1)
        for sx in (-1, 1):                                               # level, a little high: nothing to see here
            x = sx * 20 + turn
            c.new_path(); c.move_to(x - 11, by - 3); c.line_to(x + 11, by - 3); c.stroke()
        c.set_line_cap(0)

    def mouth(c, face, m, turn=0.0):
        if face != "bored":
            return m0(c, face, m, turn)
        if m and m != "dry":
            return m0(c, "stern", m, turn)
        m0(c, "stern", None, turn)
        my = HY + 30
        c.set_source_rgb(*mo.SKIN); c.rectangle(turn - 17, my - 4, 34, 12); c.fill()
        c.set_source_rgb(*mo.MAUVE); c.set_line_width(4.2); c.set_line_cap(1)
        c.new_path(); c.move_to(turn - 8, my + 1); c.line_to(turn + 8, my + 1); c.stroke(); c.set_line_cap(0)
        if m == "dry":                                                   # opened a crack: one dry word
            c.new_path(); c.save(); c.translate(turn, my + 1.5); c.scale(6.5, 3.0); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
            mo._fill_stroke(c, (0.22, 0.13, 0.15), 2.6, mo.MAUVE)
    return eyes, brows, mouth


def _coat(k, seed):
    """Drawn where mom_bc's wool coat is: a black coat to mid-calf, a silver fur collar, the order pinned on it."""
    c = k.c
    pts = mo._coat_pts(k, seed)
    cut(k, pts, COAT)
    c.set_source_rgb(*COAT_LINE); c.set_line_width(2.0); c.set_line_cap(1)
    c.new_path(); c.move_to(4, BT + 60); c.line_to(9, HEM); c.stroke()                            # the front edge
    c.new_path(); c.move_to(-SH_X - 10, HEM - 7); c.line_to(SH_X + 10, HEM - 7); c.stroke()      # the hem
    for sx in (-1, 1):                                                                           # pocket flaps
        c.new_path(); c.move_to(sx * 22, WAIST + 30); c.line_to(sx * 52, WAIST + 30); c.stroke()
    for i, by in enumerate((BT + 92, BT + 126)):                                                 # two big buttons
        ellipse(k, -7, by, 7, 7, HAT_BAND, seed + 30 + i, shadow=False, lw=1.8)
    c.set_line_cap(0)
    c.new_path(); c.move_to(-12, BT - 4); c.line_to(0, BT + 30); c.line_to(12, BT - 4); c.close_path()
    mo._fill_stroke(c, mo.CREAM, 1.8)                                                            # her blouse, at the neck
    for sx in (-1, 1):                                                                           # the fur, in lobes
        lobes = [(sx * 30, BT - 8, 21), (sx * 48, BT + 16, 20), (sx * 34, BT + 42, 19), (sx * 12, BT + 62, 15)]
        for i, (lx, ly, lr) in enumerate(lobes):
            ellipse(k, lx, ly, lr, lr * 0.92, FUR, seed + 200 + i + (10 if sx > 0 else 0), shadow=False, lw=2)
        for (lx, ly, lr) in lobes:                                                               # joined inside
            ellipse(k, lx - sx * 4, ly, lr * 0.80, lr * 0.74, FUR, seed + 230, shadow=False, outline=False)
        c.set_source_rgb(*FUR_SHADE); c.set_line_width(1.5); c.set_line_cap(1)
        for (lx, ly, lr) in lobes[:-1]:
            c.new_path(); c.move_to(lx - 4, ly - 2); c.line_to(lx + sx * 3, ly + 5); c.stroke()
            c.new_path(); c.move_to(lx + 3, ly - 5); c.line_to(lx + sx * 8, ly + 1); c.stroke()
        c.set_line_cap(0)
    mf.order(k, 36, BT + 30, 0.95, seed + 40)


def _hand(k, x, y, seed):
    """Her hand, a ring on every finger: a row of gold bands and two stones."""
    c = k.c
    ellipse(k, x, y, 16, 15, FUR, seed + 40, shadow=False, lw=1.8)   # a fur cuff: one band (v2)
    ellipse(k, x, y, 11, 11, SKIN, seed, shadow=False, lw=2)
    for i, dx in enumerate((-6.5, -2.2, 2.2, 6.5)):
        c.new_path(); c.rectangle(x + dx - 1.8, y + 3.2, 3.6, 4.4); mo._fill_stroke(c, GOLD, 1.0)
    for dx in (-2.2, 6.5):
        c.new_path(); c.arc(x + dx, y + 2.6, 2.3, 0, 2 * math.pi); mo._fill_stroke(c, GEM, 1.0)


def holder(k, x, y, s=1.0, ang=-0.5, seed=0, smoke=True):
    """A long cigarette holder from her hand at (x, y), up and away at ang; a thread of smoke."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    c.set_source_rgb(*INK); c.set_line_width(5.6); c.set_line_cap(1)
    c.new_path(); c.move_to(-6, 0); c.line_to(58, 0); c.stroke()
    c.set_source_rgb(*HOLDER); c.set_line_width(3.2); c.new_path(); c.move_to(-6, 0); c.line_to(46, 0); c.stroke()
    c.set_source_rgb(1, 1, 1); c.set_line_width(3.4); c.new_path(); c.move_to(46, 0); c.line_to(66, 0); c.stroke()
    c.set_source_rgb(0.60, 0.60, 0.62); c.set_line_width(3.4); c.new_path(); c.move_to(66, 0); c.line_to(69, 0); c.stroke()
    c.set_line_cap(0)
    c.restore()
    if smoke:
        tx, ty = x + math.cos(ang) * 69 * s, y + math.sin(ang) * 69 * s
        c.set_source_rgba(1, 1, 1, 0.75); c.set_line_width(2.6 * s); c.set_line_cap(1)
        c.new_path(); c.move_to(tx, ty - 3 * s)
        c.curve_to(tx - 10 * s, ty - 18 * s, tx + 12 * s, ty - 30 * s, tx - 2 * s, ty - 46 * s)
        c.curve_to(tx - 12 * s, ty - 58 * s, tx + 6 * s, ty - 66 * s, tx + 2 * s, ty - 78 * s); c.stroke(); c.set_line_cap(0)


def tarot(k, x, y, s=1.0, seed=0):
    """Three cards fanned in her hand, faces to us. Symbols only: a star, a tower, and on top the Client's gear."""
    c = k.c
    for i, (ang, sym) in enumerate(((-0.42, "star"), (0.0, "tower"), (0.42, "gear"))):
        c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
        cut(k, [(-17, -58), (17, -58), (17, -4), (-17, -4)], CARD, lw=2)
        c.set_source_rgb(*INK); c.set_line_width(1.2); c.rectangle(-13, -54, 26, 46); c.stroke()
        if sym == "gear":
            co.gear(k, 0, -31, 10, col=CARD, seed=seed + 5)
        elif sym == "star":
            c.new_path()
            for j in range(10):
                a = math.pi * 2 * j / 10 - math.pi / 2
                rr = 11 if j % 2 == 0 else 4.6
                (c.move_to if j == 0 else c.line_to)(rr * math.cos(a), -31 + rr * math.sin(a))
            c.close_path(); c.set_source_rgb(*INK); c.fill()
        else:
            c.set_source_rgb(*INK)
            c.rectangle(-6, -42, 12, 26); c.fill()
            for dx in (-6, -1, 4):
                c.rectangle(dx, -47, 3, 5); c.fill()
        c.restore()


def card_back(k, x, y, s=1.0, ang=0.0, seed=0):
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    cut(k, [(-17, -27), (17, -27), (17, 27), (-17, 27)], CARD_BACK, lw=2)
    c.set_source_rgb(*COAT_LINE); c.set_line_width(1.2); c.rectangle(-12, -22, 24, 44); c.stroke()
    c.restore()


def banknote(k, x, y, s=1.0, ang=0.0, seed=0):
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    cut(k, [(-24, -12), (24, -12), (24, 12), (-24, 12)], NOTE, lw=1.8)
    c.set_source_rgb(*INK); c.set_line_width(1.0); c.rectangle(-20, -8, 40, 16); c.stroke()
    kit.text(k, "100", 0, 0, 13, INK)
    c.restore()


def rake(k, x, y, x1, y1, s=1.0, seed=0, notes=3):
    """A croupier's rake from her hand (x, y) to its head at (x1, y1), and the notes it pulls in."""
    c = k.c
    for i in range(notes):
        banknote(k, x1 + (14 + i * 9) * s, y1 + (6 - i * 5) * s, s, 0.2 - i * 0.25, seed + i)
    c.set_source_rgb(*INK); c.set_line_width(6.0 * s); c.set_line_cap(1)
    c.new_path(); c.move_to(x, y); c.line_to(x1, y1); c.stroke()
    c.set_source_rgb(0.62, 0.46, 0.28); c.set_line_width(3.4 * s); c.new_path(); c.move_to(x, y); c.line_to(x1, y1); c.stroke()
    c.set_line_cap(0)
    a = math.atan2(y1 - y, x1 - x)
    c.save(); c.translate(x1, y1); c.rotate(a + math.pi / 2); c.scale(s, s)
    cut(k, [(-20, -5), (20, -5), (20, 6), (-20, 6)], (0.20, 0.20, 0.23), lw=2)
    c.restore()


def coupe(k, x, y, s=1.0, seed=620):
    """Office Noir 2's champagne coupe, kept as it is."""
    import noir2_cast as n2
    n2.coupe(k, x, y, s, seed)


def cash_box(k, x, y, s=1.0, open_=True, seed=0):
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    if open_:
        cut(k, [(-34, -22), (34, -22), (38, -58), (-30, -58)], (0.30, 0.30, 0.34), lw=2)          # the lid, up
        for i in range(3):
            banknote(k, -14 + i * 14, -24 - i * 2, 0.8, -0.1 + i * 0.1, seed + i)
    cut(k, [(-36, -22), (36, -22), (36, 8), (-36, 8)], (0.22, 0.22, 0.26), lw=2.2)
    rect(k, -6, -16, 12, 9, GOLD, seed + 7, shadow=False, lw=1.4)
    c.restore()


def _build():
    src = inspect.getsource(mb.mom)
    a, b = src.index("    pts = mo._coat_pts(k, seed)"), src.index("    tdx, tdy, tsc")
    src = src[:a] + "    _coat(k, seed)\n" + src[b:]
    for x, y in (("_hair_hat(curler)", "_hair_queen(curler)"), ("_sweet(old[1], old[2], old[3])", "_faces(old[1], old[2], old[3])"),
                 ("u, f, TEAL, SKIN, seed + 10 + side", "u, f, SLEEVE, SKIN, seed + 10 + side")):
        assert x in src, x
        src = src.replace(x, y)
    ns = dict(vars(mb))
    ns.update(_coat=_coat, _hair_queen=_hair_queen, _faces=_faces, _hand=_hand, COAT=COAT, SLEEVE=SLEEVE, LEGS=STOCKING, SHOE=SHOE,
              POSES=dict(mb.POSES,
                         q_stand=mo.ik(-1, -30, WAIST + 8) + mo.ik(1, 30, WAIST + 8),
                         q_holder=mo.ik(-1, -30, WAIST + 8) + mo.ik(1, 66, BT + 6),
                         q_cards=mo.ik(-1, -34, WAIST + 10) + mo.ik(1, 26, BT + 62),
                         q_rake=mo.ik(-1, -92, BT + 52) + mo.ik(1, 30, WAIST + 8),
                         q_lick=mo.ik(-1, -34, WAIST + 2) + mo.ik(1, 31, HY + 52),
                         q_toast=mo.ik(-1, -30, WAIST + 8) + mo.ik(1, 90, BT + 6),
                         q_wheel=mo.ik(-1, -48, HY + 41) + mo.ik(1, 48, HY + 41),
                         q_read=mo.ik(-1, -70, HY + 14) + mo.ik(1, 30, WAIST + 8)))
    exec(src, ns)
    return ns["mom"]


_body = _build()


def wheel(k, x, y, r, seed=0):
    """The big steering wheel she sits low behind: (x, y) its hub."""
    c = k.c
    for col, lw in ((INK, 16), ((0.40, 0.40, 0.45), 11)):
        c.set_source_rgb(*col); c.set_line_width(lw); c.new_path(); c.arc(x, y, r, 0, 2 * math.pi); c.stroke()
    c.set_source_rgba(0.80, 0.80, 0.86, 0.9); c.set_line_width(2.0)
    c.new_path(); c.arc(x, y, r + 2.5, 1.15 * math.pi, 1.6 * math.pi); c.stroke()
    for a in (math.pi * 0.5, math.pi * 1.17, math.pi * 1.83):
        c.set_source_rgb(*INK); c.set_line_width(11); c.new_path(); c.move_to(x, y)
        c.line_to(x + (r - 4) * math.cos(a), y + (r - 4) * math.sin(a)); c.stroke()
        c.set_source_rgb(0.40, 0.40, 0.45); c.set_line_width(7); c.new_path(); c.move_to(x, y)
        c.line_to(x + (r - 4) * math.cos(a), y + (r - 4) * math.sin(a)); c.stroke()
    ellipse(k, x, y, 15, 15, (0.26, 0.26, 0.30), seed, shadow=False, lw=2)


def queen(k, x, feet, s=1.0, pose="q_stand", face="bored", look=(0, 0), seed=70, mouth=None, lean=0.0, holder_=False,
          cards=False, rake_=False, coupe_=False, note=False, tilt=0.0, wheel_=False, chain=True):
    """Returns {"head", "hands"}. The props go in the hand the pose frees: holder_ / cards / coupe_ in her
    screen-right hand, rake_ in her screen-left; note: the hundred in her screen-left hand (pose "q_lick")."""
    old, g = mo.MAUVE, mo._glasses
    mo.MAUVE = PLUM
    if not chain:
        mo._glasses = lambda c_, turn=0.0, with_chain=True: g(c_, turn, False)
    try:
        o = _body(k, x, feet, s, pose, face, look, seed, mouth, lean, 0.0, False, True, tilt)
    finally:
        mo.MAUVE, mo._glasses = old, g
    c = k.c
    (lx, ly), (rx, ry) = o["hands"]
    c.save()
    if holder_:
        holder(k, rx + 3 * s, ry - 4 * s, s, -0.62, seed + 90)
    if cards:
        tarot(k, rx, ry + 2 * s, s * 0.95, seed + 91)
    if coupe_:
        coupe(k, rx + 2 * s, ry + 6 * s, s * 0.9, seed + 92)
    if holder_ or cards or coupe_:
        c.save(); c.translate(rx, ry); c.scale(s, s); _hand(k, 0, 0, seed + 61); c.restore()
    if rake_:
        rake(k, lx, ly, lx - 96 * s, ly + 64 * s, s, seed + 93)
        c.save(); c.translate(lx, ly); c.scale(s, s); _hand(k, 0, 0, seed + 60); c.restore()
    if note and pose == "q_read":                        # held up beside her eyes
        banknote(k, lx - 8 * s, ly - 16 * s, s * 1.3, -0.10, seed + 94)
        c.save(); c.translate(lx, ly); c.scale(s, s); _hand(k, 0, 0, seed + 60); c.restore()
    elif note:
        banknote(k, lx - 6 * s, ly - 12 * s, s * 1.1, -0.18, seed + 94)
        c.save(); c.translate(lx, ly); c.scale(s, s); _hand(k, 0, 0, seed + 60); c.restore()
    if pose == "q_lick" and not mouth:                    # her tongue, out to her thumb
        c.save(); c.translate(x, feet); c.scale(s, s)
        c.save(); c.translate(13, HY + 36); c.rotate(0.25); c.scale(10, 5); c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi)
        c.restore(); mo._fill_stroke(c, (0.90, 0.48, 0.55), 1.8)
        c.restore()
    if wheel_:                                             # low behind the wheel: it covers her to the nose
        c.save(); c.translate(x, feet); c.scale(s, s)
        cut(k, [(-150, HY + 46), (150, HY + 46), (150, HY + 260), (-150, HY + 260)], (0.12, 0.12, 0.14), shadow=False, lw=2)   # the dashboard
        c.set_source_rgb(*COAT_LINE); c.set_line_width(2.0); c.new_path(); c.move_to(-150, HY + 50); c.line_to(150, HY + 50); c.stroke()
        wheel(k, 0, HY + 92, 70, seed + 95)
        for sx in (-1, 1):
            _hand(k, sx * 48, HY + 41, seed + 96 + sx)
        c.restore()
    c.restore()
    return o
