"""Don from behind, for over-the-shoulder shots (Daddy's Home v8, Tomas 24 Nov: "reikia dono is nugaros").
Built like fs_storyboard._client_back: the back of his bald head, the headset band round the back of it with both ear cups,
the one hair, the white shirt and the navy vest's back. Optionally one arm raised, ending in the series hand.
New file, opt-in: nothing that exists calls it.
  don_back(k, x, y, s, arm=None)  x, y: the head's centre in the frame's own (540x960) units; s: 1.0 = a head of r 64.
  arm = (tx, ty, shape): the hand's position in the same units and its hands_ps shape ("point", "fist", "relax")."""
import math
import kit
import hands_ps as hp
from kit import INK, ellipse, cut

SKIN = kit.PEOPLE["DON"]["skin"]
VEST = (0.13, 0.13, 0.17)
SHIRT = (0.98, 0.98, 0.96)
BAND = (0.20, 0.20, 0.23)
CUP = (0.12, 0.12, 0.14)


def _sleeve(c, pts, w):
    for col, ww in ((INK, w + 6), (SHIRT, w)):
        c.set_source_rgb(*col); c.set_line_width(ww); c.set_line_cap(1); c.set_line_join(1)
        c.new_path(); c.move_to(*pts[0])
        for p in pts[1:]:
            c.line_to(*p)
        c.stroke()
    c.set_line_cap(0); c.set_line_join(0)


UPPER, FORE = 190, 180                                       # fixed bones (rules page: two bones, never stretched)


def don_arm(k, x, y, s, arm, side=1, bend=None, cuff=False, sh_at=(118, 132)):
    """The raised arm alone (drawn after the back, not logged as him: a bubble's tail looks for his crown). Two bones of
    fixed length (of_scenes.ik2), the upper arm wider than the forearm, the wrist narrowest, the sleeve no wider than the
    arm; the elbow bends out, away from his body."""
    import of_scenes as osc
    c = k.c
    sh = (x + side * sh_at[0] * s, y + sh_at[1] * s)      # opt-in sh_at: the shoulder joint in his back's units
    tx, ty, shape = arm
    el = osc.ik2((tx, ty), sh, UPPER * s, FORE * s, side if bend is None else bend)
    L_ = math.hypot(tx - el[0], ty - el[1]) or 1.0
    d = ((tx - el[0]) / L_, (ty - el[1]) / L_)
    reach = UPPER * s + FORE * s
    far = math.hypot(tx - sh[0], ty - sh[1])
    if far > reach:                                         # out of reach: the hand stops where the arm ends
        tx, ty = el[0] + d[0] * FORE * s, el[1] + d[1] * FORE * s
    wr = (tx - d[0] * 22 * s, ty - d[1] * 22 * s)
    for e, ink in ((3.0, True), (0.0, False)):
        col = INK if ink else SHIRT
        osc._limb(c, sh, el, 50 * s, 42 * s, col, e)
        osc._limb(c, el, wr, 42 * s, 32 * s, col, e)
    if cuff:                                                # opt-in (Daddy's Home v8, review 3): his shirt cuff and gold
        n_ = (-d[1], d[0])                                  # cufflink, as in the APPROVE insert: one hand in both shots
        cx_, cy_ = wr[0] - d[0] * 46 * s, wr[1] - d[1] * 46 * s
        c.set_source_rgb(*INK); c.set_line_width(2.6 * s); c.new_path()
        c.move_to(cx_ + n_[0] * 17 * s, cy_ + n_[1] * 17 * s); c.line_to(cx_ - n_[0] * 17 * s, cy_ - n_[1] * 17 * s); c.stroke()
        ellipse(k, wr[0] - d[0] * 34 * s + n_[0] * 8 * s, wr[1] - d[1] * 34 * s + n_[1] * 8 * s, 7 * s, 6 * s,
                (0.95, 0.76, 0.22), 3512, shadow=False, lw=1.8 * s)
    hp.draw(k, shape, tx, ty, 62 * s, SKIN, d, side)


def don_back(k, x, y, s=1.0, arm=None, side=1):
    """side=1: the raised arm is his right, on screen right (we stand behind him). Returns the head's (x, y, r)."""
    c = k.c
    sh = None
    if arm:                                                   # the shoulder in frame units, before the body is drawn
        sh = (x + side * 118 * s, y + 132 * s)
    c.save(); c.translate(x, y); c.scale(s, s)
    cut(k, [(-170, 150), (-150, 96), (-90, 72), (-34, 66), (34, 66), (90, 72), (150, 96), (170, 150), (176, 520), (-176, 520)],
        SHIRT, shadow=False, lw=3)                                                       # the shirt's shoulders and sleeves
    cut(k, [(-128, 112), (-96, 84), (-40, 74), (40, 74), (96, 84), (128, 112), (132, 520), (-132, 520)],
        VEST, shadow=False, lw=3)                                                        # the vest's back
    c.set_source_rgba(1, 1, 1, 0.16); c.set_line_width(3)                               # its centre seam
    c.move_to(0, 92); c.line_to(0, 520); c.stroke()
    cut(k, [(-40, 40), (40, 40), (44, 80), (-44, 80)], SKIN, shadow=False, lw=2.6)        # the neck
    cut(k, [(-46, 70), (0, 82), (46, 70), (40, 86), (0, 96), (-40, 86)], SHIRT, shadow=False, lw=2.2)   # the collar
    for sx in (-1, 1):                                                                   # the ears, behind the cups
        ellipse(k, sx * 64, 2, 11, 18, SKIN, 7101 + sx, shadow=False, lw=2.4)
    ellipse(k, 0, -6, 64, 70, SKIN, 7100, shadow=False, lw=3)                            # the head, bald
    c.set_source_rgba(1, 1, 1, 0.35); c.set_line_width(6); c.set_line_cap(1)          # a shine on the crown
    c.new_path(); c.arc(-14, -40, 30, 3.6, 4.4); c.stroke()
    c.set_source_rgba(0.80, 0.55, 0.45, 0.5); c.set_line_width(2.5)                    # the folds at the back of the neck
    for yy in (38, 48):
        c.move_to(-22, yy); c.curve_to(-8, yy + 4, 8, yy + 4, 22, yy); c.stroke()
    c.set_line_cap(1)
    for w_, col in ((13, INK), (8, BAND)):                                               # the headset band round the back
        c.set_source_rgb(*col); c.set_line_width(w_)                                     # of his head (the crown stays bare:
        c.new_path(); c.arc(0, -6, 66, math.pi * 0.06, math.pi * 0.94); c.stroke()      # the bubble's tail lands on scalp)
    for sx in (-1, 1):                                                                   # both ear cups
        ellipse(k, sx * 68, 4, 13, 22, CUP, 7103 + sx, shadow=False, lw=2.4)
    for w_, col in ((6, INK), (3.2, (0.45, 0.45, 0.50))):                              # the boom, forward along his right cheek
        c.set_source_rgb(*col); c.set_line_width(w_)
        c.move_to(side * 72, 16); c.curve_to(side * 80, 34, side * 78, 50, side * 70, 62); c.stroke()
    c.set_source_rgb(*INK); c.set_line_width(4.6)                                        # the one hair
    c.move_to(40, -58); c.curve_to(40, -82, 62, -88, 58, -74); c.curve_to(56, -66, 44, -70, 48, -78); c.stroke()   # off the crown
    c.set_line_cap(0)
    c.restore()
    if arm:
        tx, ty, shape = arm
        dx, dy = tx - sh[0], ty - sh[1]
        L = math.hypot(dx, dy)
        el = (sh[0] + dx * 0.5 + side * 22 * s, sh[1] + dy * 0.5 + 10 * s)              # a soft elbow, out to the side
        d = ((tx - el[0]) / math.hypot(tx - el[0], ty - el[1]), (ty - el[1]) / math.hypot(tx - el[0], ty - el[1]))
        wr = (tx - d[0] * 20 * s, ty - d[1] * 20 * s)               # the cuff over the wrist: no gap
        _sleeve(c, [sh, el, wr], 40 * s)
        hp.draw(k, shape, tx, ty, 62 * s, SKIN, d, side)
    return dict(head=(x, y), r=64 * s)                            # his crown: the tail lands on its top                   # left of the hair: the tail lands on bare scalp


def visitor_back(k, x, y, s=1.0):
    """The visitor (the Client's rig in a black service jacket) from behind, over his shoulder: fs_storyboard._client_back
    redrawn with his colours (black jacket, dark hair, grey at the sides). New, opt-in (Daddy's Home v8, 4F)."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    cut(k, [(-150, 120), (-120, 40), (-40, 10), (40, 10), (120, 40), (150, 120), (150, 400), (-150, 400)],
        (0.12, 0.12, 0.14), shadow=False, lw=3)                                              # the black jacket's shoulders
    c.set_source_rgba(1, 1, 1, 0.10); c.set_line_width(3); c.move_to(0, 30); c.line_to(0, 400); c.stroke()
    cut(k, [(-46, 14), (46, 14), (40, 40), (-40, 40)], (0.20, 0.20, 0.23), shadow=False, lw=2.5)   # the collar
    ellipse(k, 0, -40, 64, 74, (0.94, 0.76, 0.62), 1211, shadow=False, lw=3)                  # neck and head
    cut(k, [(-64, -40), (-60, -90), (-30, -116), (30, -116), (60, -90), (64, -40), (50, 10), (-50, 10)],
        (0.16, 0.12, 0.10), shadow=False, lw=3)                                              # his hair, from behind
    for sx in (-1, 1):
        cut(k, [(sx * 64, -50), (sx * 58, -10), (sx * 46, 8), (sx * 52, -40)], (0.55, 0.55, 0.57), shadow=False, lw=2)
    ellipse(k, -66, -36, 9, 16, (0.94, 0.76, 0.62), 1212, shadow=False, lw=2.4)               # an ear
    c.restore()
    return dict(head=(x, y - 40 * s), r=70 * s)
