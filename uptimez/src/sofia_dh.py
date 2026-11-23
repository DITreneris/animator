"""SOFÍA in "Daddy's Home" (episode 12): the power suit. Tomas, 21 Nov, /grill-me: a power suit, cream, her hair loose as it
was, and she changes for the visit: episode 11's look (sofia_cs, wine) until beat 8; from 8.4 she is back in this, CV
in hand. Dressed for the investor, not for Don.
Built like sofia_cs: the same rig (sofia_ob), colours swapped in and put back, so nothing older changes.
- a cream blazer with wide padded shoulders and peaked lapels edged in gold, two gold buttons;
- a black silk top under it (the cream reads against it, and against the black and burgundy of Father's people);
- a cream pencil skirt; her triangle earrings and her hair stay.
  o = sofia(k, x, feet, s, pose, face_kind, look, ...)      the same signature as sofia_cs.sofia
  python3 sofia_dh.py  -> ../daddys-home/dh_sofia_v1.png"""
import math
import cairo
import kit
import sofia_v4 as sf
import sofia_ss as ss
import sofia_bc as sbc
import sofia_ob as so
import sofia_cs as scs
from kit import Ctx, INK, cut, ellipse, rect
from sofia_v4 import GOLD, GOLD_LIGHT

CREAM = (0.99, 0.97, 0.91)                                 # lighter than the office wall (0.91, 0.86, 0.76), so she stands off it
CREAM_SHADE = (0.84, 0.78, 0.64)
SILK = (0.09, 0.09, 0.11)
SILK_SHADE = (0.20, 0.20, 0.23)


def hoop(k, x, y, lgx=0.0, spark=0.0, seed=0):
    """v2: a small chunky gold hoop at the lobe (x, y), a third of the triangle's size. Both ears show now."""
    c = k.c
    c.save(); c.translate(x, y + 9); c.rotate(max(-0.2, min(0.2, -lgx * 0.05)))
    for col, lw in ((INK, 7.6), (GOLD, 5.0)):
        c.set_source_rgb(*col); c.set_line_width(lw); c.new_path(); c.arc(0, 0, 5.4, 0, 2 * math.pi); c.stroke()
    c.set_source_rgb(*GOLD_LIGHT); c.set_line_width(1.6); c.new_path(); c.arc(0, 0, 6.4, 3.5, 4.6); c.stroke()
    c.restore()


def triangles(k, x, y, lgx=0.0, spark=0.0, seed=0):
    """v3 (Tomas, 21 Nov: "Leave triangle earrings"): her gold triangles, on both ears now that her hair is pulled back."""
    if x >= 0:
        return scs.triangle(k, x, y, lgx, spark, seed)
    c = k.c
    c.save(); c.scale(-1, 1)
    scs.triangle(k, -x, y, -lgx, spark, seed)
    c.restore()


def _suit(base):
    def blazer(k, body_top, seed):
        """v4 (the second look review): a jacket to the hips, in at the waist and out over them; shoulders that stand
        out past her arms; plain lapels (the triangles are the only points near her face); a deep V of black silk; two
        gold buttons. The pencil skirt under it is sofia_ss.PENCIL."""
        c = k.c
        bt = body_top
        cut(k, [(-17, bt - 1), (17, bt - 1), (13, bt + 150), (-13, bt + 150)], SILK, shadow=False, lw=1.6)      # the black silk top
        cut(k, [(0, bt + 46), (-12, bt - 2), (12, bt - 2)], sf.SKIN, shadow=False, lw=1.6)                      # a deep V
        for sx in (-1, 1):
            cut(k, [(sx * 24, bt - 10), (sx * 62, bt - 6), (sx * 67, bt + 20), (sx * 52, bt + 34), (sx * 36, bt + 30)],
                CREAM, shadow=False, lw=2.2)                                                                    # the shoulder, square, past the arm
            cut(k, [(sx * 40, bt - 1), (sx * 15, bt - 1), (sx * 8, bt + 60), (sx * 10, bt + 152), (sx * 44, bt + 150),
                    (sx * 40, bt + 124), (sx * 27, bt + 88), (sx * 45, bt + 34)], CREAM, shadow=False, lw=2.2)   # in at the waist, out to the hips
            c.set_source_rgb(*CREAM_SHADE); c.set_line_width(1.6); c.set_line_cap(1)
            c.move_to(sx * 31, bt + 40); c.curve_to(sx * 24, bt + 64, sx * 21, bt + 84, sx * 25, bt + 112); c.stroke()   # the dart
            c.move_to(sx * 20, bt + 126); c.line_to(sx * 37, bt + 125); c.stroke()                                 # a flap pocket
            cut(k, [(sx * 15, bt - 1), (sx * 31, bt - 4), (sx * 24, bt + 44), (sx * 8, bt + 62)], CREAM, shadow=False, lw=1.8)   # a plain lapel
            c.set_source_rgb(*GOLD); c.set_line_width(1.6)
            c.move_to(sx * 31, bt - 3); c.line_to(sx * 24, bt + 43); c.line_to(sx * 9, bt + 60); c.stroke()
        for yy in (bt + 82, bt + 104):
            ellipse(k, 11, yy, 4.6, 4.6, GOLD, seed + 48 + int(yy), shadow=False, lw=1.5)
    return blazer


def _tight(orig_builder):
    """9.6: the mouth smiles and nothing else does. A small closed smile, pressed; the eyes narrowed and still; the brows
    level and a little low."""
    def builder(inner, blush, sp=None):
        base = orig_builder(inner, blush, sp)

        def face(k, x, y, kind="neutral", look=(0, 0), seed=0):
            snap = scs._snap(k.c)
            base(k, x, y, kind, look, seed)
            c = k.c
            my = y + 29
            scs._cover(k, x, y, seed, snap)
            so._eyes(k, x, y, (max(-0.6, min(0.6, look[0])), 0.0), seed, lid=3.5)
            scs._brow(c, x - 27, y - 18, x - 8, y - 17, lift=0.5)
            scs._brow(c, x + 8, y - 17, x + 27, y - 18, lift=0.5)
            ellipse(k, x, my, 24, 13, so.SKIN, seed + 310, shadow=False, outline=False)
            c.set_source_rgb(*so.RED); c.set_line_width(6.4); c.set_line_cap(1)
            c.move_to(x - 11, my - 1); c.curve_to(x - 5, my + 2.5, x + 5, my + 2.5, x + 11, my - 1); c.stroke()
            c.set_source_rgb(*INK); c.set_line_width(1.3)
            c.move_to(x - 10, my - 0.6); c.curve_to(x - 5, my + 2.6, x + 5, my + 2.6, x + 10, my - 0.6); c.stroke()
            for sx in (-1, 1):                                # the corners, pulled tight
                c.move_to(x + sx * 12, my - 4); c.line_to(x + sx * 14, my + 1); c.stroke()
        return face
    return builder


def sofia(k, x, feet, s=1.0, pose="hold", face_kind="smile", look=(0, 0), lag=(0, 0), seed=7, badge=True, lean=0.0,
          mouth=None, sparkle=0.0, tablet_kind="auto"):
    """v2 (Tomas, 21 Nov: "Ponytail, small chunky hoops"): episode 10's high ponytail (sofia_fs.ponytail), tidy, both
    ears showing; small gold hoops; the sharper suit. The same swaps as sofia_cs.sofia, with her hair not swept."""
    import sofia_fs
    old = (ss.BLOUSE, ss.BLOUSE_SHADE, ss.SKIRT, sf.BLOUSE, sbc.BLAZER, sbc.BLAZER_EDGE, so.drop, so.strand, so.pearl,
           ss.SWEPT[0], sbc._blazer, ss.PULLED[0], ss.PENCIL[0])
    ss.PULLED[0] = True; ss.PENCIL[0] = True
    ss.BLOUSE, ss.BLOUSE_SHADE, ss.SKIRT, sf.BLOUSE = CREAM, CREAM_SHADE, CREAM, CREAM
    sbc.BLAZER, sbc.BLAZER_EDGE = CREAM, CREAM_SHADE
    so.drop, so.strand, so.pearl = triangles, (lambda k_, seed_: None), scs._gold_bead
    ss.SWEPT[0] = False
    sbc._blazer = _suit(sbc._blazer)
    own = face_kind if face_kind in scs.OWN else None
    orig_face = so._face
    if own:
        so._face = lambda o, sp: scs._mine(orig_face(o, sp), own)
    if face_kind == "tight":
        so._face = lambda o, sp: _tight(orig_face(o, sp))
        face_kind = "smile"
    c = k.c
    c.save(); c.translate(x, feet); c.scale(s, s)             # the ponytail, behind everything
    sofia_fs.ponytail(k, sofia_fs.HY, lag[0], lag[1], seed + 1)
    c.save(); c.translate(27, sofia_fs.HY - 59); c.rotate(-0.55)   # v4: the tie, so the ponytail has a root
    rect(k, -9, -5, 18, 10, GOLD, seed + 2, shadow=False, lw=1.6)
    c.restore()
    c.restore()
    try:
        return so.sofia(k, x, feet, s, pose, scs.OWN.get(face_kind, face_kind), look, lag, seed, badge, lean, mouth,
                        sparkle, tablet_kind)
    finally:
        so._face = orig_face
        (ss.BLOUSE, ss.BLOUSE_SHADE, ss.SKIRT, sf.BLOUSE, sbc.BLAZER, sbc.BLAZER_EDGE, so.drop, so.strand, so.pearl,
         ss.SWEPT[0], sbc._blazer, ss.PULLED[0], ss.PENCIL[0]) = old


def cv(k, x, y, s=1.0, ang=-0.08, seed=3100):
    """Her CV (episode 9's sheet): held out in 9.6."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    rect(k, -26, -36, 52, 72, (0.99, 0.98, 0.95), seed, lw=2)
    kit.text(k, "CV", 0, -18, 15, INK)
    ellipse(k, -12, 2, 7, 7, (0.90, 0.74, 0.62), seed + 1, shadow=False, lw=1.3)
    c.set_source_rgb(*INK); c.set_line_width(1.6)
    for yy in (-4, 4, 16, 24):
        c.move_to(2 if yy < 10 else -18, yy); c.line_to(20, yy); c.stroke()
    c.restore()


def sheet(out="../daddys-home/dh_sofia_v4.png"):
    Wd, Hd, Z = 1500, 1000, 2.2
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, Wd, Hd); c = cairo.Context(surf)
    c.set_source_rgb(*kit.WALL); c.paint()
    c.set_source_rgb(*kit.FLOOR); c.rectangle(0, 880, Wd, 120); c.fill()
    k = Ctx(c, 0)
    kit.text(k, "DADDY'S HOME · SOFÍA · the power suit · v4", Wd / 2, 46, 34, INK)
    kit.text(k, "she changes for the visit: episode 11's look until beat 8, the suit from 8.4", Wd / 2, 82, 19, INK, font=kit.MONO)
    F = 900
    S = 0.56 * Z
    scs.sofia(k, 190, F, S, "hold", "smile", look=(0.6, 0))
    sofia(k, 520, F, S, "stand", "smile", look=(-0.6, 0))
    sofia(k, 850, F, S, "lapel", "interested", look=(0.8, 0))
    o2 = sofia(k, 1190, F, S, "stand", "tight", look=(0.8, 0.1))
    cv(k, o2["hands"][1][0] + 26, o2["hands"][1][1] - 10, 1.5) if isinstance(o2, dict) and "hands" in o2 else None
    for name, note, x in (("EPISODE 11", "the wine look: beats 1 to 7", 190), ("THE SUIT", "hip-length, waisted, square shoulders", 520),
                          ("8.4", "she walks back in, smoothing a lapel", 850), ("9.6", "the CV is taken; a small tight smile; her eyes don't move", 1190)):
        kit.text(k, name, x, 940, 24, INK); kit.text(k, note, x, 968, 15, INK, font=kit.MONO)
    surf.write_to_png(out); print("wrote", out)


if __name__ == "__main__":
    sheet()
