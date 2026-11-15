"""PAM, "Secret Santa", v1. Her Mandatory Fun office look (pam_mf, untouched) with the episode's changes:
- lips="rose": the dusty-rose nude, clearly rosy (a full lip shape along each expression's mouth line, a little
  gloss); speaking mouths get the rose lips too. lips=None keeps her natural mouth (shot 1, before she puts it on).
- glasses="chain": taken off and dropped on the gold bead chain, hanging folded at her chest (shot 4 onward);
  "low" (on, the default) and "off" work as in pam_mf; POSE_GLASSES + finger="bridge" is the hand taking them off.
- New faces: "proud" (shot 9: shy closed smile, blush, eyes down on the tag), "incredulous" (shot 15 and the loop:
  narrowed eyes, flat mouth), "decide" (shot 7: eyes find the present, a small firm mouth).
- apply=True: POSE_APPLY, her screen-right hand up at her mouth with the uncapped lipstick (shot 2).
Usage: o = pam(k, x, feet, s, pose, face, look, glasses="low", lips="rose", apply=False, mouth=None, ...)"""
import math
import kit
import pam_mf as pm
import props_ss as props
import iwry_mouths as im
from kit import INK, ellipse

ROSE = props.DUSTY_ROSE
ROSE_LINE = (0.42, 0.18, 0.22)
SKIN = pm.SKIN
HY = pm.HY
POSE_APPLY = (-8, 0) + pm.ik(1, 30, HY + 62)          # shot 2: the hand up at her mouth with the lipstick
POSE_SHY = pm.POSE_SHY
POSE_GLASSES = pm.POSE_GLASSES
POSE_TABLE = pm.POSE_TABLE

# each expression's closed mouth as a cubic centreline (offsets from the head centre)
CENTRE = {
    "neutral": ((-8, 27), (-3, 29), (3, 29), (8, 26)),
    "hopeful": ((-8, 26), (-3, 31), (3, 31), (8, 26)),
    "fade": ((-9, 28), (-3, 28), (4, 28), (9, 30)),
    "quiet": ((-10, 26), (-4, 31), (4, 31), (11, 23)),
    "dinner": ((-10, 25), (-6, 32), (2, 32), (8, 26)),
    "peer": ((-9, 28), (0, 28), (6, 28), (11, 22)),
    "avert": ((-7, 28), (-2, 28), (2, 28), (7, 28)),
    "proud": ((-11, 25), (-4, 32), (4, 32), (11, 25)),
    "incredulous": ((-8, 28), (-3, 28), (3, 28), (8, 28)),
    "decide": ((-7, 28), (-2, 28.5), (3, 28), (8, 26)),
}
NEW = {"proud": ("neutral", (0.1, 0.9)), "incredulous": ("neutral", (0.0, 0.3)), "decide": ("neutral", (0.7, 0.8))}


def _bez(p, t):
    u = 1 - t
    return tuple(u ** 3 * p[0][i] + 3 * u * u * t * p[1][i] + 3 * u * t * t * p[2][i] + t ** 3 * p[3][i] for i in (0, 1))


def lips_along(c, x, y, cl, gloss=True):
    """A lipstick mouth: upper and lower lip around the centreline, rose fill, a darker parting line."""
    n = 26
    cl = tuple((q[0] * 1.18, q[1]) for q in cl)                 # a touch wider than her plain mouth: it must read
    pts = [_bez(cl, i / (n - 1)) for i in range(n)]
    up, lo = [], []
    for i, (px_, py_) in enumerate(pts):
        t = i / (n - 1)
        sh = math.sin(math.pi * t) ** 0.7
        bow = 1 - 0.38 * math.exp(-((t - 0.5) / 0.09) ** 2)          # the cupid's bow
        up.append((x + px_, y + py_ - 4.6 * sh * bow))
        lo.append((x + px_, y + py_ + 6.2 * sh))
    c.move_to(*up[0])
    for q in up[1:]:
        c.line_to(*q)
    for q in reversed(lo[:-1]):
        c.line_to(*q)
    c.close_path()
    c.set_source_rgb(*ROSE); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(1.7); c.set_line_join(1); c.stroke()
    c.set_source_rgb(*ROSE_LINE); c.set_line_width(2.2); c.set_line_cap(1)
    c.move_to(x + cl[0][0], y + cl[0][1])
    c.curve_to(x + cl[1][0], y + cl[1][1], x + cl[2][0], y + cl[2][1], x + cl[3][0], y + cl[3][1]); c.stroke()
    if gloss:
        gx, gy = pts[int(n * 0.36)]
        c.set_source_rgba(1, 1, 1, 0.85); c.arc(x + gx, y + gy + 2.6, 1.3, 0, 2 * math.pi); c.fill()


def chain_glasses(k, x, y, seed=0):
    """The glasses off, hanging folded on the gold bead chain at her chest."""
    c = k.c
    gx, gy = x + 2, y + 88
    c.set_source_rgb(*pm.GOLD)
    for sx in (-1, 1):                                    # the chain: from behind the ears down to the folded glasses
        x0, y0 = x + sx * 40, y + 14
        x1, y1 = gx + sx * 13, gy - 6
        for i in range(14):
            t = i / 13
            bx = x0 + (x1 - x0) * t - sx * 6 * math.sin(math.pi * t)
            by = y0 + (y1 - y0) * t + 6 * math.sin(math.pi * t)
            c.arc(bx, by, 1.5, 0, 2 * math.pi); c.fill()
    c.save(); c.translate(gx, gy); c.rotate(-0.12); c.scale(1.25, 1.25)
    for dx in (-8, 8):                                     # folded: the two half-moons overlap, temples tucked
        pm.half_moon(c, dx, -5, 22, 9)
        c.set_source_rgba(*pm.LENS, 0.75); c.fill_preserve()
        c.set_source_rgb(*INK); c.set_line_width(2.2); c.stroke()
    c.set_source_rgb(1, 1, 1); c.set_line_width(1.8); c.set_line_cap(1)
    c.move_to(-12, 2); c.line_to(-7, -3); c.stroke()
    c.set_source_rgb(*INK); c.set_line_width(2.2)
    c.move_to(-3, -5); c.curve_to(-1, -8, 1, -8, 3, -5); c.stroke()
    c.restore()


def _lids(c, x, y):
    """Narrowed eyes: the upper lids come down to the middle of the eye, brows low and flat."""
    for sx in (-17, 17):
        c.move_to(x + sx - 14, y - 16); c.line_to(x + sx + 14, y - 16); c.line_to(x + sx + 14, y - 2)
        c.line_to(x + sx - 14, y - 1); c.close_path()
        c.set_source_rgb(*SKIN); c.fill()
        c.set_source_rgb(*INK); c.set_line_width(3.4); c.set_line_cap(1)
        c.move_to(x + sx - 12, y - 1); c.curve_to(x + sx - 4, y - 3, x + sx + 4, y - 3, x + sx + 12, y - 2); c.stroke()
    pm._brows(c, x, y, ((-27, -16), (-8, -15)), ((8, -15), (27, -16)), w=3.6)


def _wrapped_faces(orig, lips, gstate):
    def mf(inner, g, mouth):
        base = orig(inner, "off" if gstate == "chain" else g, mouth)

        def face_draw(k, x, y, face, look, glasses=False, seed=0):
            c = k.c
            b, lk = NEW.get(face, (face, None))
            base(k, x, y, b, lk or look, glasses=glasses, seed=seed)
            if face == "proud":
                c.set_source_rgba(*pm.pt.BLUSH, 0.9)
                for sx in (-26, 26):
                    c.save(); c.translate(x + sx, y + 15); c.scale(10, 5.5); c.arc(0, 0, 1, 0, 2 * math.pi)
                    c.restore(); c.fill()
                pm._brows(c, x, y, ((-26, -19), (-9, -24)), ((9, -24), (26, -19)))
            elif face == "incredulous":
                _lids(c, x, y)
            elif face == "decide":
                pm._brows(c, x, y, ((-26, -21), (-9, -18)), ((9, -18), (26, -21)), w=3.8)
            if mouth:
                if lips:
                    pm._mouth_erase(k, x, y, seed)
                    c.save(); c.translate(x, y + 28); c.scale(0.8, 0.8)
                    im.mouth(k, 0, 0, mouth, SKIN, lip_col=ROSE, erase=(1, 1), seed=seed + 96)
                    c.restore()
            elif face in CENTRE and (lips or face in NEW):
                pm._mouth_erase(k, x, y, seed)
                if lips:
                    lips_along(c, x, y, CENTRE[face])
                else:
                    cl = CENTRE[face]
                    c.set_source_rgb(*INK); c.set_line_width(3.6); c.set_line_cap(1)
                    c.move_to(x + cl[0][0], y + cl[0][1])
                    c.curve_to(x + cl[1][0], y + cl[1][1], x + cl[2][0], y + cl[2][1], x + cl[3][0], y + cl[3][1])
                    c.stroke()
            if gstate == "chain":
                chain_glasses(k, x, y, seed)
        return face_draw
    return mf


def pam(k, x, feet, s=1.0, pose="stand", face="neutral", look=(0, 0), seed=40, badge=True, glasses="low",
        lips="rose", apply=False, mouth=None, lean=0.0, finger=False):
    orig = pm._mf_faces
    pm._mf_faces = _wrapped_faces(orig, lips, glasses)
    try:
        if apply:
            pose = POSE_APPLY
        out = pm.pam(k, x, feet, s, pose, face, look, seed, badge, "off" if glasses == "chain" else glasses,
                     None, finger, mouth, lean)
    finally:
        pm._mf_faces = orig
    if apply:                                             # the uncapped lipstick from her fist up to her mouth
        hx, hy = out["hands"][1]
        props.lipstick(k, hx - 2 * s, hy + 2 * s, 0.85 * s, -0.68, 1.0, seed + 30, cap_col=props.CAP_BLACK)
        ellipse(k, hx, hy, 10 * s, 10 * s, SKIN, seed + 31, shadow=False, lw=2 * s)
    return out
