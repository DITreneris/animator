"""DON in "Pick a Side" (episode 14): his look as ever (fleece vest, the ketchup stain, the headset, the one hair); this
episode's poses and props. Tomas, 23 Nov, /grill-me:
- under the fallen blind his face pokes out through a bent gap in the slats (1.2-1.3); then he wears it as a cape (1.4);
- the selfie: chin up, double thumbs-up (3.1); one thumb onto the pad without looking (3.4);
- the office gag (5.4): a knee up, the foot hovering over the tape, arms a little out, then back down;
- the last frame (6.1): thumbs in the vest, elbows wide, a warm, satisfied smile.
Nothing in his rig changes: fs_storyboard.don draws him, with arm poses passed by angle; the blind, the tape roll, the
thumbs and the raised leg are drawn over him (the leg: his trousers clipped at the knee and redrawn).
  don(k, x, feet, s, pose, face, look, knee=0.0, lean=0.0, chin=False)
v2 (23 Nov, "Improve" after two audits): one hand for everything (hands_ps: thumbs-up, salute, palms, fists);
a face per beat that climbs (commanding, proud, manic grin, nerves, smug); the knee as a real bent leg, the foot over
the tape; a body behind the fallen blind; the bump bends him at the waist.
  python3 don_ps.py [out_dir]  ->  ps_don_v2.png (sheet), ps_don_phone_v2.png (phone check)"""
import math
import os
import sys
import cairo
import kit
import fs_storyboard as sb
import don_v4 as dv
import acts_ob as ac
import hands_ps as hp
from kit import Ctx, INK, cut, rect, ellipse

TAPE = (0.95, 0.78, 0.15)
SLAT, SLAT_D = (0.86, 0.86, 0.82), (0.55, 0.55, 0.52)
WAIST_Y = -98                                             # just under his belt, in his own units (feet at 0)
POSES = {"cord": (-8, 0, 168, 8), "salute": (-8, 0, 110, 95), "thumbs": (-48, -118, 48, 118), "point_roll": (-8, 0, 92, 4),
         "balance": (-58, -10, 58, 10), "vest": (-60, 150, 60, -150), "push": (-60, 40, 60, -40), "lift_roll": (-30, 60, 120, 60),
         "bump": (-150, -10, 40, -30), "stand": (-8, 0, 8, 0)}
HANDS = {"cord": ("relax", "fist"), "salute": ("relax", "salute"), "thumbs": ("thumb", "thumb"), "point_roll": ("relax", "fist"),
         "balance": ("palm", "palm"), "vest": ("fist", "fist"), "push": ("palm", "palm"), "lift_roll": ("fist", "fist"),
         "bump": ("palm", "palm"), "stand": ("relax", "relax")}


def don(k, x, feet, s=0.60, pose="stand", face="neutral", look=(0, 0), knee=0.0, lean=0.0, chin=0, hands=None):
    """knee 0..1: his screen-right knee up, the foot hovering (5.4). lean: radians about his feet. chin: features lifted.
    hands: (left, right) hands_ps shapes; None = the pose's own; False = leave kit.HAND as it is (the before rows)."""
    c = k.c
    p = POSES.get(pose, pose)
    if hands is not False:
        old = kit.HAND[0]; kit.HAND[0] = hp.hand; hp.reset(*(hands or HANDS.get(pose, ("relax", "relax"))))
    c.save(); c.translate(x, feet); c.rotate(lean); c.translate(-x, -feet)
    if knee > 0:
        c.save(); c.rectangle(x - 400, feet - 2000, 800, 2000 + WAIST_Y * s); c.clip()
    try:
        o = _sbdon(k, x, feet, s, p, face, look, chin)
        hp.redraw_late(k)
    finally:
        if hands is not False:
            kit.HAND[0] = old
    if knee > 0:
        c.restore()
        _legs(k, x, feet, s, knee)
    c.restore()
    return o


def bumped(k, x, feet, s, face="shock", look=(1, 0)):
    """2.11: bumped from his right: the legs stagger (one foot up), the top half thrown further, one arm out for balance."""
    c = k.c
    wy = feet + WAIST_Y * s
    c.save(); c.translate(x, feet); c.rotate(-0.08); c.translate(-x, -feet)
    _legs(k, x, feet, s, 0.45)                                           # the legs stagger
    c.restore()
    c.save(); c.translate(x, feet); c.rotate(-0.08); c.translate(-x, -feet)
    c.translate(x, wy); c.rotate(-0.24); c.translate(-x, -wy)
    c.rectangle(x - 400, feet - 2000, 800, 2000 + WAIST_Y * s + 4); c.clip()
    o = don(k, x, feet, s, "bump", face, look)
    c.restore()
    return o


def _sbdon(k, x, feet, s, p, face, look, chin):
    """fs_storyboard.don with dv.don's chin passed through (the same rig, the same signs)."""
    kit.ARM_POSES["_ps"] = p
    try:
        with ac.arms():
            o = dv.don(k, x, feet, s, "_ps", face, look=look, seed=500, chin=chin)
    finally:
        del kit.ARM_POSES["_ps"]
    sb.don_signs(k, o["head"], s, "up", "up")
    return o


def _cap(c, pts, t, col, lw=2.0):
    for cc, w in ((INK, t + 2 * lw), (col, t)):
        c.set_source_rgb(*cc); c.set_line_width(w); c.set_line_cap(1); c.set_line_join(1)
        c.new_path(); c.move_to(*pts[0])
        for q in pts[1:]:
            c.line_to(*q)
        c.stroke()
    c.set_line_cap(0); c.set_line_join(0)


LEG = [None]


def _legs(k, x, feet, s, u):
    """Under the belt: the screen-left leg planted; the screen-right one bent, the knee up and out, the foot in profile
    hovering, toes toward the line. u 0..1: how high."""
    c = k.c
    c.save(); c.translate(x, feet); c.scale(s, s)
    w = WAIST_Y
    cut(k, [(-45, w), (2, w), (-2, -10), (-47, -10)], dv.KHAKI, shadow=False, lw=2)          # the planted leg
    e_ = 3 if LEG[0] and LEG[0].get("wide") else 0        # opt-in: the standing shoe 10 % wider (the weight is on it)
    cut(k, [(-50 - e_, -12), (2 + e_, -12), (4 + e_, 2), (-52 - e_, 2)], (0.24, 0.18, 0.13), shadow=False, lw=2)   # its shoe
    lift = 44 * u
    kx, ky = 30 + 34 * u, w + 30 - 8 * u                                                      # the knee
    ax, ay = kx + 16 * u, -16 - lift                                                          # the ankle
    L_ = LEG[0]                                              # opt-in (5.4, review 26 Nov): knee and ankle moved (x u), the shoe
    if L_:                                                   # smaller and tipped toes-down, a softer shadow
        kx, ky = kx + L_["knee"][0] * u, ky + L_["knee"][1] * u
        ax, ay = ax + L_["ankle"][0] * u, ay + L_["ankle"][1] * u
    c.set_source_rgba(0, 0, 0, L_["shadow"] if L_ else 0.18); c.save(); c.translate(ax + 22, 4); c.scale(1, 0.22)
    c.new_path(); c.arc(0, 0, 34 - 10 * u, 0, 2 * math.pi); c.restore(); c.fill()           # the shadow under the foot
    _cap(c, [(24, w + 10), (kx, ky)], 44, dv.KHAKI)                                           # the thigh
    _cap(c, [(kx, ky), (ax, ay)], 38, dv.KHAKI)                                               # the shin
    c.set_source_rgb(*dv.KHAKI); c.new_path(); c.arc(kx, ky, 21, 0, 2 * math.pi); c.fill()  # the knee, one piece
    c.set_source_rgb(*INK); c.set_line_width(1.6); c.new_path(); c.arc(kx - 4, ky + 2, 14, -0.6, 0.9); c.stroke()  # the fold
    if L_:
        c.save(); c.translate(ax, ay); c.rotate(L_["tilt"] * u); c.scale(L_["shoe"], L_["shoe"]); c.translate(-ax, -ay)
    c.new_path()                                                                              # the shoe, side on, toes right
    c.move_to(ax - 18, ay - 6); c.line_to(ax + 14, ay - 8); c.curve_to(ax + 40, ay - 6, ax + 52, ay + 4, ax + 50, ay + 14)
    c.line_to(ax - 20, ay + 14); c.close_path()
    c.set_source_rgb(0.24, 0.18, 0.13); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2); c.stroke()
    if not (L_ and L_.get("nohem")):                       # (review 26 Nov: the hem's own shape read as "an extra joint")
        _cap(c, [(ax - 18, ay - 10), (ax + 16, ay - 12)], 10, dv.KHAKI)                      # the hem over it
    if L_:
        c.restore()
    if u > 0.6:
        c.set_source_rgb(*INK); c.set_line_width(1.8); c.set_line_cap(1)                       # it wobbles
        for i in (-1, 1):
            c.new_path(); c.move_to(ax + 16 + i * 4, ay + 26); c.line_to(ax + 16 + i * 12, ay + 34); c.stroke()
        c.set_line_cap(0)
    c.restore()


BLIND_GAP_FIX = [False]


def blind_over(k, head, s, seed=4800):
    """1.2-1.3: the whole blind over him, his face through a bent gap in the slats, the cord dangling."""
    c = k.c
    hx, hy = head
    w, top, bot = 150 * s, hy - 70 * s, hy + 230 * s
    c.save()
    c.set_source_rgba(0.25, 0.22, 0.20, 0.0)
    c.new_path(); c.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    c.rectangle(hx - w / 2, top, w, bot - top)
    c.save(); c.translate(hx, hy + 6 * s); c.scale(44 * s, 40 * s)
    if BLIND_GAP_FIX[0]:                                     # opt-in (Pick a Side film, 25 Nov): without a new sub-path the
        c.new_sub_path()                                     # arc joined the rectangle's corner: a stroke across his eye,
    c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()              # read as "an eyepatch" by 6 cold viewers
    c.set_source_rgb(*SLAT); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.2); c.stroke()
    c.set_fill_rule(cairo.FILL_RULE_WINDING)
    c.set_source_rgba(0.10, 0.12, 0.25, 0.13)                                         # his body, a shadow through the slats
    c.new_path(); c.move_to(hx - 30 * s, hy + 84 * s)                                 # shoulders and torso, one shape
    c.curve_to(hx - 66 * s, hy + 88 * s, hx - 70 * s, hy + 110 * s, hx - 62 * s, hy + 230 * s)
    c.line_to(hx + 62 * s, hy + 230 * s); c.curve_to(hx + 70 * s, hy + 110 * s, hx + 66 * s, hy + 88 * s, hx + 30 * s, hy + 84 * s)
    c.close_path(); c.fill()
    c.set_source_rgb(*SLAT_D); c.set_line_width(1.4)
    yy = top + 10 * s
    while yy < bot:
        dy = abs(yy - (hy + 6 * s))
        bulge = 7 * s if abs(yy - (hy + 108 * s)) < 22 * s else 0                    # the slats bow over his shoulders
        if dy < 40 * s:                                                               # the slats bend round his face
            half = 44 * s * math.sqrt(max(0.0, 1 - (dy / (40 * s)) ** 2))
            c.move_to(hx - w / 2, yy); c.line_to(hx - half - 3, yy); c.stroke()
            c.move_to(hx + half + 3, yy); c.line_to(hx + w / 2, yy); c.stroke()
        else:
            c.move_to(hx - w / 2, yy); c.curve_to(hx - w / 4, yy - bulge, hx + w / 4, yy - bulge, hx + w / 2, yy); c.stroke()
        yy += 11 * s
    c.restore()
    for sgn in (-1, 1):                                                               # two slats bent out round his face
        c.set_source_rgb(*SLAT); c.set_line_width(5 * s); c.new_path()
        c.move_to(hx - 50 * s, hy + sgn * 42 * s); c.curve_to(hx - 20 * s, hy + sgn * 62 * s, hx + 20 * s, hy + sgn * 62 * s, hx + 50 * s, hy + sgn * 42 * s)
        c.stroke_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.4); c.stroke()
    rect(k, hx - w / 2 - 6 * s, top - 10 * s, w + 12 * s, 12 * s, (0.70, 0.70, 0.66), seed, shadow=False, lw=2)   # the rail, askew
    c.set_source_rgb(0.30, 0.30, 0.30); c.set_line_width(2.2)
    c.move_to(hx + w / 2 - 8 * s, top); c.curve_to(hx + w / 2 + 6 * s, hy + 60 * s, hx + w / 2 - 4 * s, hy + 140 * s, hx + w / 2 + 10 * s, hy + 200 * s)
    c.stroke()
    ellipse(k, hx + w / 2 + 10 * s, hy + 204 * s, 4 * s, 6 * s, (0.92, 0.88, 0.70), seed + 1, shadow=False, lw=1.4)


def blind_cape(k, head, s, seed=4810):
    """1.4: the blind over his shoulders like a cape (drawn before him: behind), its rail across his shoulders."""
    c = k.c
    hx, hy = head
    top, bot = hy + 56 * s, hy + 300 * s
    c.new_path(); c.move_to(hx - 70 * s, top); c.line_to(hx + 70 * s, top); c.curve_to(hx + 86 * s, top + 90 * s, hx + 110 * s, bot - 60 * s, hx + 96 * s, bot)
    for i in range(6, -1, -1):                                                        # the hem hangs in scallops
        c.line_to(hx - 96 * s + i * 32 * s, bot - (10 * s if i % 2 else 0))
    c.curve_to(hx - 110 * s, bot - 60 * s, hx - 86 * s, top + 90 * s, hx - 70 * s, top); c.close_path()
    c.set_source_rgb(*SLAT); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.2); c.stroke()
    c.set_source_rgb(*SLAT_D); c.set_line_width(1.4)
    yy = top + 10 * s
    while yy < bot:
        t = (yy - top) / (bot - top)
        hw = 74 * s + 22 * s * t
        c.move_to(hx - hw, yy); c.curve_to(hx - hw / 3, yy + 6 * s * t, hx + hw / 3, yy + 6 * s * t, hx + hw, yy); c.stroke(); yy += 11 * s


def cape_rail(k, head, s, seed=4811):
    hx, hy = head
    c = k.c
    c.save(); c.translate(hx, hy + 60 * s); c.rotate(-0.08)
    rect(k, -78 * s, -6 * s, 156 * s, 12 * s, (0.70, 0.70, 0.66), seed, shadow=False, lw=2)
    c.restore()


ROLL_TAIL = [False]


def tape_roll(k, x, y, s, ang=0.0):
    """The roll of yellow tape: a fat ring, a tongue of tape hanging off it."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    if ROLL_TAIL[0]:                                         # opt-in (film, 25 Nov: the roll read as "a coin, a ring"): a
        cut(k, [(10, 8), (32, 10), (39, 78), (26, 82), (16, 68)], TAPE, lw=1.8)      # longer tongue of tape, flat, a
        c.set_source_rgb(0.80, 0.62, 0.10); c.set_line_width(2)                      # torn end
        c.move_to(26, 82); c.line_to(30, 74); c.line_to(34, 81); c.line_to(39, 78); c.stroke()
    else:
        cut(k, [(10, 8), (30, 10), (34, 60), (22, 64), (14, 56)], TAPE, lw=1.8)
    for col, lw in ((INK, 30), (TAPE, 25)):
        c.set_source_rgb(*col); c.set_line_width(lw); c.new_path(); c.arc(0, 0, 26, 0, 2 * math.pi); c.stroke()
    c.set_source_rgb(0.80, 0.62, 0.10); c.set_line_width(3); c.new_path(); c.arc(0, 0, 16, 0, 2 * math.pi); c.stroke()
    c.restore()


def tape_strip(k, a, b, s):
    """A length of tape pulled off the roll, from a (the roll) to b (the other hand), sagging."""
    c = k.c
    mx, my = (a[0] + b[0]) / 2, max(a[1], b[1]) + 30 * s
    for col, w in ((INK, 13 * s), (TAPE, 9 * s)):
        c.set_source_rgb(*col); c.set_line_width(w); c.new_path(); c.move_to(*a); c.curve_to(mx, my, mx, my, *b); c.stroke()


def _label(c, s, x, y, size=16, col=INK):
    c.select_font_face("Inter", 0, 1); c.set_font_size(size); c.set_source_rgb(*col)
    e = c.text_extents(s); c.move_to(x - e.x_advance / 2, y); c.show_text(s)


def sheet(out):
    W, H = 2400, 1300
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W * 2, H * 2); surf.set_device_scale(2, 2)
    c = cairo.Context(surf); c.set_source_rgb(*kit.WALL); c.paint()
    F = 860
    c.set_source_rgb(*kit.FLOOR); c.rectangle(0, F, W, 200); c.fill()
    k = Ctx(c, 0)
    c.select_font_face("Inter", 0, 1); c.set_font_size(30); c.set_source_rgb(*INK); c.move_to(40, 50)
    c.show_text("PICK A SIDE · DON · his look as ever, this episode's poses and props · v2")
    c.select_font_face("Inter", 0, 0); c.set_font_size(18); c.move_to(40, 84)
    c.show_text("v2: one hand (hands_ps) · a face per beat: deadpan, commanding, proud, shock, manic grin, nerves, smug · a real knee · a body behind the blind")
    S = 0.60 * 1.5
    xs = [140, 400, 660, 920, 1180, 1440, 1700, 1960, 2220]
    o = don(k, xs[0], F, S, "cord", "squint", (1, -0.4))                                             # 1.1
    hx, hy = o["hands"][1]
    c.set_source_rgb(0.3, 0.3, 0.3); c.set_line_width(2.4); c.move_to(hx, hy - 180); c.line_to(hx, hy + 10); c.stroke()
    o = don(k, xs[1], F, S, "stand", "neutral", (0, 0))                                               # 1.3: deadpan
    blind_over(k, o["head"], S)
    tmp = cairo.ImageSurface(cairo.FORMAT_RGB24, 4, 4)
    h0 = sb.don(Ctx(cairo.Context(tmp), 0), xs[2], F, S, "stand", "neutral", (0, 0))["head"]
    blind_cape(k, h0, S)                                                                            # 1.4, behind him
    o = don(k, xs[2], F, S, "lift_roll", "hollow", (0, 0))
    cape_rail(k, o["head"], S)
    tape_strip(k, o["hands"][1], o["hands"][0], S)
    tape_roll(k, *o["hands"][1], S * 0.9)
    o = don(k, xs[3], F, S, "point_roll", "confused", (1, 0), chin=1)                                  # 2.3: commanding, brows down
    tape_roll(k, o["hands"][1][0] + 10, o["hands"][1][1], S * 0.9, ang=0.6)
    don(k, xs[4], F, S, "salute", "pleased", (0.6, 0), chin=1)                                       # 2.5: proud
    bumped(k, xs[5], F, S)                                                                          # 2.11: bumped
    don(k, xs[6], F, S, "thumbs", "grin", (0, -0.3), chin=1)                                          # 3.1: manic
    c.set_source_rgb(*TAPE); c.move_to(xs[7] + 70, F); c.line_to(xs[7] + 92, F); c.line_to(xs[7] + 118, F + 110)
    c.line_to(xs[7] + 92, F + 110); c.fill()                                                         # 5.4: the line under his foot
    don(k, xs[7], F, S, "balance", "neutral", (0.7, 1.0), knee=1.0)                                  # nerves: eyes on the foot
    don(k, xs[8], F, S, "vest", "smug", (0, 0), chin=1)                                              # 6.1: smug, convinced
    for x, n, note in zip(xs, ("1.1", "1.3", "1.4", "2.3", "2.5", "2.11", "3.1", "5.4", "6.1"),
                          ("the cord", "through the slats", "the cape, the tape", "\"Pick a side.\" commanding", "\"Pam. My general.\" proud",
                           "bumped: the stagger", "chin up, manic thumbs", "the foot hovers: nerves", "\"Everyone's with me.\"")):
        _label(c, n, x, F + 140, 20); _label(c, note, x, F + 166, 14, (0.3, 0.3, 0.3))
    surf.write_to_png(out); print("wrote", out)


def phone(out):
    frames = []
    for name, txt in (("medium", "1.3: the first line, through the slats"), ("medium ", "5.4: the knee over the line"),
                      ("close", "6.1: \"Everyone's with me.\"")):
        f = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(f); k = Ctx(c, 0)
        c.set_source_rgb(*kit.WALL); c.paint()
        if name == "medium":
            o = don(k, 270, 1120, 0.60 * 2.4, "stand", "neutral", (0, 0))
            blind_over(k, o["head"], 0.60 * 2.4)
        elif name == "medium ":
            c.set_source_rgb(*kit.FLOOR); c.rectangle(0, 820, 540, 140); c.fill()
            c.set_source_rgb(*TAPE); c.move_to(338, 820); c.line_to(360, 820); c.line_to(410, 960); c.line_to(380, 960); c.fill()
            don(k, 230, 880, 0.60 * 1.7, "balance", "neutral", (0.7, 1.0), knee=1.0)
        else:
            don(k, 270, 1330, 0.60 * 3.0, "vest", "smug", (0, 0), chin=1)
        frames.append((name, txt, f))
    W = 3 * 270 + 4 * 20
    s_ = cairo.ImageSurface(cairo.FORMAT_RGB24, W, 480 + 80); c = cairo.Context(s_); c.set_source_rgb(0.15, 0.15, 0.16); c.paint()
    for i, (name, txt, f) in enumerate(frames):
        c.save(); c.translate(20 + i * 290, 20); c.scale(0.5, 0.5); c.set_source_surface(f, 0, 0); c.paint(); c.restore()
        c.select_font_face("Inter", 0, 1); c.set_font_size(15); c.set_source_rgb(1, 1, 1)
        c.move_to(20 + i * 290, 522); c.show_text(name.strip().upper() + " · at 270 px")
        c.select_font_face("Inter", 0, 0); c.set_font_size(12); c.move_to(20 + i * 290, 542); c.show_text(txt)
    s_.write_to_png(out); print("wrote", out)


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "../pick-a-side"
    os.makedirs(d, exist_ok=True)
    sheet(os.path.join(d, "ps_don_v2.png"))
    phone(os.path.join(d, "ps_don_phone_v2.png"))
