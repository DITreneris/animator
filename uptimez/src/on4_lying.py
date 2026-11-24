"""OFFICE NOIR 4, 3.3-3.5: Pam-Cat lying on the crossing, v3 (23 Nov; v1 and v2 pinned as on4_lying_v1.py, on4_lying_v2.py).
v3, the second (last) audit: her hands are the series' one hand (hands_ps fists, thumb and fingers), not balls; the flung
arm starts at a shoulder you can see at the edge of her chest, runs along the road under her head with a thick upper arm,
a bent elbow and a slimmer forearm (lessons 99, 116); the face on one axis (the eyes level along it, the nose and the open
mouth on the centre line CX), the mask about 20 % smaller, the brows above it.
v2 (23 Nov). After the outside
audit and Tomas ("fix it, and the face in three-quarter"): she LIES (3.3-3.5), flat, pressed onto the road with a dark
contact; the legs apart in tone, both boots whole (toes up on her back); the flung arm bent; her head drawn
three-quarter, turned toward her body (lesson 182: the face in two halves about a centre line moved toward the turn,
the far half 0.55 wide, the bob framing it: lesson 88); the bills the shadows came for, on her and round her; one
shadow stands, the other bends to pluck a bill off her coat, both on the money, never on her (protect list 1); their
gloves the series' one hand (hands_ps) in the pale colour; their thrown shadows shorter, without heads (The Offer's
were plain wedges).
v1: a standalone picture first (lessons 152, 153), with
shadows as in The Offer (Tomas, 23 Nov: "the lying body must have shadows like The Offer"):
  - contact shadows under her, soft and edgeless, where her head, shoulders, hip and heels touch the road
    (of_set.legs draws its legs on them first);
  - the long cast shadows of two shadows standing behind her on the road (black against the lit house), thrown toward us
    across the road and over her body by the double lamp behind them, as the bodyguards' shadows lie across the garage
    floor in The Offer (rough cut v21, 0:01-0:03).
One body, not a standing figure laid down (lesson 153): on her back, the head turned toward us, shoulders, chest, waist,
hip; one leg straight, the other knee up (alive, not hurt: it is the hit-and-shrug, protect list 2); one arm flung out
over her head, the other across her belt; dazed stars over her head.
The head is the series rig's (pam_bc, the Pam-Cat costume of on4_cast v2), clipped to the head's own region (hair, ears,
face, jaw), never to a circle round the whole figure (lesson 150); the coat under the chin reads as her collar.
NOT imported by any film. python3 on4_lying.py -> ../office-noir-4/on4_lying_v3.png (1080x1920) and a phone copy."""
import math
import cairo
import kit
import engine_on as eng
import on_set as ons
import on4_cast as oc
import on4_street as st
from kit import Ctx, INK, cut
from garage_lying_on3 import _tube, _blob, _line

S = 0.86                       # her scale here (Pam-Cat's head as in the sheet's close shots)
HEAD = (112, 610)              # where her head lies
BACK_Y = 690                   # the road under her back
ANG = -1.15                    # the head turned with the body (top of the head to the left)
DON_GREY = (0.20, 0.20, 0.22)


CX, FAR = 10.0, 0.55          # the face's centre line (head units, toward the turn) and the far half's width
SKIN = kit.PEOPLE["PAM"]["skin"]
HAIR = kit.PEOPLE["PAM"]["hair"]
STREAK = (0.62, 0.62, 0.64)
BERRY = (0.78, 0.27, 0.43)


def head34(k, s=S, look=(0.6, -0.5)):
    """Pam-Cat's head drawn three-quarter, turned toward +x (lesson 182, for a head with a bob: lesson 88), from her own
    measures: the bob about 40 wide and 55 above the eyes, the eyes 17 either side of the face's centre and 4 below the
    head point, the lips 30 below; Pam's skin, hair and grey streak, the berry lips; Pam-Cat's ears and mask.
    The face's centre line is moved toward the turn (CX); the near half at full width, the far half 0.55; only the near
    side of the bob over the near cheek; the far edge is the cheek, broken once by the brow and the nose."""
    c = k.c
    c.save(); c.scale(s, s)
    ex_n, ex_f = CX - 17, CX + 17 * FAR                                    # the near and far eye
    # the far ear (behind the head) and the bob's mass behind the face
    cut(k, [(14, -50), (30, -46), (24, -84)], oc.EAR, shadow=False, lw=2.0)
    cut(k, [(-48, 30), (-54, -6), (-48, -38), (-28, -58), (2, -64), (26, -56), (38, -40), (40, -22), (30, -16), (-30, 30)], HAIR, shadow=False, lw=2.4)
    # the face, turned: the far edge is the cheek, broken by the brow and the nose
    face = [(-26, -32), (-32, -4), (-28, 24), (-14, 40), (4, 48), (22, 44), (32, 34), (36, 24), (37, 14),
            (38, 4), (40, -6), (35, -14), (32, -30), (12, -40), (-10, -40)]   # v3: the brow breaks the far edge; the nose is on the face
    cut(k, face, SKIN, shadow=False, lw=2.4)
    # the near side of the bob over the near cheek, and the fringe with its grey streak
    cut(k, [(-52, -14), (-30, -20), (-26, 6), (-30, 30), (-40, 36), (-52, 30)], HAIR, shadow=False, lw=2.2)
    cut(k, [(-34, -50), (-10, -60), (20, -58), (36, -40), (34, -24), (18, -32), (0, -30), (-20, -28), (-32, -24)], HAIR, shadow=False, lw=2.2)
    c.set_source_rgb(*STREAK); c.set_line_width(7); c.set_line_cap(1)
    c.move_to(-26, -34); c.curve_to(-18, -50, 0, -56, 18, -50); c.stroke()
    c.set_source_rgb(*INK); c.set_line_width(1.4); c.move_to(-26, -38); c.curve_to(-18, -55, 0, -60, 18, -55); c.stroke()
    # the near ear, big, on the bob
    cut(k, [(-40, -40), (-16, -54), (-38, -88)], oc.EAR, shadow=False, lw=2.2)
    cut(k, [(-34, -46), (-21, -54), (-35, -76)], oc.EAR_IN, shadow=False, outline=False)
    # the mask, about 20 % smaller than v2: a thinner band, a shorter near flick, the far side tucked behind the cheek
    c.new_path()
    c.move_to(-38, -16); c.curve_to(-26, -10, ex_n, -10, CX + 2, -5); c.curve_to(ex_f, -10, 32, -8, 36, -7)
    c.line_to(37, 2); c.curve_to(32, 9, ex_f + 4, 12, CX + 2, 9); c.curve_to(ex_n + 6, 13, -14, 11, -20, 6)
    c.curve_to(-28, 2, -34, -6, -38, -16); c.close_path()
    for ex, w in ((ex_n, 13.0), (ex_f, 13.0 * FAR)):                       # almond holes, the far one narrow
        c.new_sub_path(); c.move_to(ex - w, 2); c.curve_to(ex - w * 0.6, -8, ex + w * 0.6, -9, ex + w, -2)
        c.curve_to(ex + w * 0.6, 11, ex - w * 0.6, 12, ex - w, 2); c.close_path()
    c.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    c.set_source_rgb(*oc.MASK); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.0); c.stroke()
    c.set_fill_rule(cairo.FILL_RULE_WINDING)
    # the eyes, level on one axis (y = 2), dazed; the far one narrow
    for ex, w in ((ex_n, 9.0), (ex_f, 9.0 * FAR)):
        kit.ellipse(k, ex, 2, w, 9, (1, 1, 1), 5200 + int(ex), shadow=False, lw=2)
        kit.ellipse(k, ex + look[0] * 3.0 * w / 9, 2 + look[1] * 3.0, 4.0 * w / 9 + 0.6, 4.0, INK, 5210 + int(ex), shadow=False, outline=False)
    c.set_source_rgb(*INK); c.set_line_width(3.4); c.set_line_cap(1)        # the brows, lifted, on the skin above the mask
    c.move_to(ex_n - 9, -17); c.curve_to(ex_n - 3, -21, ex_n + 3, -21, ex_n + 8, -19); c.stroke()
    c.move_to(ex_f - 4, -19); c.line_to(ex_f + 5, -18); c.stroke()
    # the nose on the centre line, turned: down from between the eyes toward the turn, its tip, the nostril
    c.set_line_width(2.2); c.new_path()
    c.move_to(CX + 3, 8); c.curve_to(CX + 9, 14, CX + 13, 19, CX + 11, 22); c.curve_to(CX + 8, 24, CX + 4, 23, CX + 2, 21); c.stroke()
    # the mouth on the centre line: open in shock, the near half wider
    my = 33
    c.new_path(); c.move_to(CX - 8, my); c.curve_to(CX - 6, my - 7, CX + 6, my - 7, CX + 8, my)
    c.curve_to(CX + 6, my + 9, CX - 6, my + 9, CX - 8, my); c.close_path()
    c.set_source_rgb(0.30, 0.07, 0.10); c.fill_preserve(); c.set_source_rgb(*BERRY); c.set_line_width(2.6); c.stroke()
    c.set_source_rgb(*INK); c.set_line_width(1.2); c.stroke()
    c.restore()


def head(k, x, y, ang, s=S, look=(0.6, -0.5)):
    """Pam-Cat's head, three-quarter, laid with the body by ang (top of the head to the left)."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang)
    head34(k, s, look)
    c.restore()


def stars(c, x, y, s=1.0, t=0.0):
    """Dazed stars circling over her head."""
    for i in range(3):
        a = t * 2.4 + i * 2 * math.pi / 3
        oc.star(c, x + math.cos(a) * 46 * s, y + math.sin(a) * 14 * s, 11 * s, (0.98, 0.95, 0.80))


def contact(c, cx, cy, rx, ry, a=0.70):
    c.save(); c.translate(cx, cy); c.scale(rx, ry)
    g = cairo.RadialGradient(0, 0, 0.1, 0, 0, 1)
    g.add_color_stop_rgba(0, 0, 0, 0, a); g.add_color_stop_rgba(0.7, 0, 0, 0, a * 0.5); g.add_color_stop_rgba(1, 0, 0, 0, 0)
    c.set_source(g); c.arc(0, 0, 1, 0, 2 * math.pi); c.fill(); c.restore()


def fist(k, ex, ey, hx, hy, w=26, side=-1):
    """A gloved fist from the series' one hand (hands_ps), its forearm running from the elbow (ex, ey) to (hx, hy)."""
    import hands_ps as hp
    L = math.hypot(hx - ex, hy - ey) or 1
    hp.draw(k, "fist", hx, hy, w, oc.GLOVE_DARK, ((hx - ex) / L, (hy - ey) / L), side)


def arm(k, sh, el, wr, col=oc.COAT):
    """An arm from the shoulder: a thick upper arm, the elbow with a fold, a slimmer forearm (lesson 116)."""
    c = k.c
    _tube(k, [sh, ((sh[0] + el[0]) / 2, (sh[1] + el[1]) / 2), el], (15, 14, 12.5), col, lw=2.6, caps=(True, True))
    _tube(k, [el, ((el[0] + wr[0]) / 2, (el[1] + wr[1]) / 2), wr], (12.5, 11, 9.5), col, lw=2.6, caps=(True, False))
    c.set_source_rgb(*oc.COAT_DARK); c.set_line_width(1.8); c.set_line_cap(1)          # the fold at the elbow
    c.new_path(); c.arc(el[0], el[1], 8, -0.6, 0.8); c.stroke(); c.set_line_cap(0)


def body(k):
    """Her body from the neck: shoulders by the head, the hips to the right; the coat, the belt, the legs, the boots."""
    c = k.c
    X0, Y = HEAD[0] + 34, BACK_Y
    # contact shadows first, under everything that touches the road
    for (cx, rx, ry) in ((HEAD[0] + 6, 52, 9), (X0 + 70, 90, 9), (X0 + 190, 64, 9), (X0 + 326, 30, 7), (X0 + 290, 30, 7)):
        contact(c, cx, Y + 3, rx, ry)
    c.set_source_rgba(0, 0, 0, 0.55); c.set_line_width(3)                          # where her back meets the road
    c.move_to(X0 - 20, Y + 1); c.line_to(X0 + 220, Y + 3); c.stroke()
    # the arm flung out on the road beyond her head, gloved (clear of the head, so it is not read as part of it)
    contact(c, X0 - 64, Y + 4, 64, 7)
    SH, EL, WR = (X0 + 14, Y - 22), (X0 - 44, Y - 18), (X0 - 98, Y - 2)                  # shoulder, elbow, wrist
    arm(k, SH, EL, WR)
    fist(k, EL[0], EL[1], WR[0] - 8, WR[1] + 2, 26, -1)
    # the straight leg, along the road
    FAR_LEG = (0.24, 0.24, 0.26)                                                     # the far leg a step lighter than the near
    _tube(k, [(X0 + 190, Y - 22), (X0 + 260, Y - 18), (X0 + 318, Y - 14)], (19, 15, 12), FAR_LEG, lw=2.8)
    cut(k, [(X0 + 312, Y - 6), (X0 + 312, Y - 30), (X0 + 322, Y - 60), (X0 + 338, Y - 62), (X0 + 340, Y - 30), (X0 + 344, Y - 2)],
        oc.BOOT, shadow=False, lw=2)                                                 # its boot, toe up (she is on her back)
    # the torso: shoulder, chest (rising), waist, hip
    _blob(k, [(X0, Y - 66), (X0 + 40, Y - 76), (X0 + 100, Y - 70), (X0 + 140, Y - 54), (X0 + 180, Y - 58),
              (X0 + 214, Y - 44), (X0 + 220, Y - 12), (X0 + 190, Y + 2), (X0 + 100, Y + 2), (X0 + 20, Y), (X0 - 8, Y - 26)],
          oc.COAT, lw=3.2)
    _line(c, [(X0 + 46, Y - 60), (X0 + 96, Y - 50), (X0 + 136, Y - 40)], oc.COAT_DARK, 2.2)       # a fold across the chest
    _line(c, [(X0 + 4, Y - 4), (X0 + 20, Y - 34), (X0 + 40, Y - 30)], oc.COAT_DARK, 2.0)          # the shoulder's seam: the arm leaves here
    for bx in (X0 + 70, X0 + 108):                                                                 # the coat's buttons
        kit.ellipse(k, bx, Y - 40, 3.4, 3.4, (0.34, 0.34, 0.36), 5110 + bx, shadow=False, lw=1.2)
    cut(k, [(X0 + 146, Y - 58), (X0 + 166, Y - 62), (X0 + 170, Y), (X0 + 150, Y + 2)], oc.COAT_DARK, shadow=False, lw=1.6)   # the belt
    cut(k, [(X0 + 150, Y - 36), (X0 + 166, Y - 38), (X0 + 167, Y - 22), (X0 + 151, Y - 20)], (0.55, 0.55, 0.57), shadow=False, lw=1.2)
    # the collar at her neck, grey and wide
    cut(k, [(X0 - 10, Y - 60), (X0 + 26, Y - 80), (X0 + 40, Y - 56), (X0 + 10, Y - 30)], oc.COLLAR, shadow=False, lw=2.0)
    # the near leg, knee up, the sole flat on the road (alive: she will sit up)
    _tube(k, [(X0 + 196, Y - 40), (X0 + 246, Y - 104), (X0 + 286, Y - 18)], (21, 17, 13), oc.SUIT_LEG, lw=3.0)
    c.set_source_rgba(1, 1, 1, 0.14); c.new_path(); c.arc(X0 + 246, Y - 104, 9, 0, 2 * math.pi); c.fill()   # the knee, lit
    cut(k, [(X0 + 268, Y - 26), (X0 + 296, Y - 28), (X0 + 316, Y - 10), (X0 + 316, Y + 2), (X0 + 266, Y + 2)], oc.BOOT, shadow=False, lw=2)
    c.set_source_rgba(1, 1, 1, 0.22); c.set_line_width(2.2); c.move_to(X0 + 212, Y - 52); c.line_to(X0 + 244, Y - 94); c.stroke()   # the near thigh's lit edge
    # the arm across her belt
    arm(k, (X0 + 44, Y - 60), (X0 + 94, Y - 30), (X0 + 136, Y - 46))
    fist(k, X0 + 94, Y - 30, X0 + 146, Y - 50, 24, 1)


def cast_shadow(c, foot_x, foot_y, height, dx, dy, width=34, a=0.55, who="thug"):
    """A standing figure's shadow lying on the road: from its feet toward (dx, dy), a head at the far end, two legs at the
    near end; soft at the head (the lamp is wide)."""
    L = math.hypot(dx, dy); ux, uy = dx / L, dy / L; nx, ny = -uy, ux
    def at(u, v):
        return (foot_x + ux * height * u + nx * width * v, foot_y + uy * height * u + ny * width * v)
    pts = [at(0, -0.55), at(0.45, -0.62), at(0.72, -1.0), at(0.80, -0.9), at(0.84, -0.42), at(0.88, -0.50), at(1.0, -0.30),
           at(1.0, 0.30), at(0.88, 0.50), at(0.84, 0.42), at(0.80, 0.9), at(0.72, 1.0), at(0.45, 0.62), at(0, 0.55),
           at(0, 0.10), at(0.40, 0.04), at(0, -0.10)]
    c.new_path(); c.move_to(*pts[0])
    for p in pts[1:]:
        c.line_to(*p)
    c.close_path()
    g = cairo.LinearGradient(*at(0, 0), *at(1.0, 0))
    g.add_color_stop_rgba(0, 0.02, 0.02, 0.03, a); g.add_color_stop_rgba(1, 0.02, 0.02, 0.03, a * 0.7)
    c.set_source(g); c.fill()


BILL = (0.80, 0.84, 0.74)
BX, BLEAN = 336, -0.55           # the bending shadow: his feet, his lean
LOG = {}


def _rot(o, p, a):
    """p turned by a about o (the rig returns its points before the lean)."""
    dx, dy = p[0] - o[0], p[1] - o[1]
    return (o[0] + dx * math.cos(a) - dy * math.sin(a), o[1] + dx * math.sin(a) + dy * math.cos(a))


def bill(k, x, y, ang, s=1.0, seed=0):
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    cut(k, [(-16, -8), (16, -8), (16, 8), (-16, 8)], BILL, shadow=False, lw=1.4)
    c.set_source_rgba(0.3, 0.35, 0.28, 0.8); c.new_path(); c.arc(0, 0, 4, 0, 2 * math.pi); c.set_line_width(1.2); c.stroke()
    c.restore()


def thug_shadow(k, fx, fy, s, dx, dy, a=0.55, pose="open", seed=4100):
    """The ground shadow of a thug standing at (fx, fy): the same body (client_ob, as on4_street.thug), projected onto
    the road toward (dx, dy) by the lamp behind him."""
    import client_ob as co
    c = k.c
    H = 300 * s
    c.push_group()
    c.save(); c.translate(fx, fy); c.transform(cairo.Matrix(1, 0, -dx / H, -dy / H, 0, 0)); c.translate(-fx, -fy)
    c.rectangle(fx - 200, fy - H * 0.60, 400, H * 0.60 + 4); c.clip()                # v2: legs and body only, no head
    co.client(k, fx, fy, s, pose, "plain", look=(0, 0), roll=False, badge=False, seed=seed)
    c.restore()
    g = c.pop_group()
    c.set_source_rgba(0.02, 0.02, 0.03, a); c.mask(g)


V4 = [False]                    # v4 (opt-in, the board review): a soft rim from above only, contact shadows under their feet


def rim(k, fx, fy, s, seed=4100, lean=0.0, pose="open"):
    """The thug's outline lit from behind: his body, pale, a little bigger and raised, under the black figure."""
    import client_ob as co
    c = k.c
    for dx, dy in ((0, -3), (-2.5, -1.5), (2.5, -1.5)):
        c.push_group()
        c.save(); c.translate(dx, dy)
        if lean:
            c.translate(fx, fy); c.rotate(lean); c.translate(-fx, -fy)
        co.client(k, fx, fy, s, pose, "plain", look=(0, 0), roll=False, badge=False, seed=seed)
        c.restore()
        g = c.pop_group()
        c.set_source_rgba(0.85, 0.85, 0.82, 0.9 if not V4[0] else (0.38 if dy == -3 else 0.0)); c.mask(g)


def ground(k):
    """The crossing seen low: the road from y 560, the stripes under her, the kerb at the top; the lamp's pool."""
    c = k.c
    def road():
        c.new_path(); c.rectangle(-10, 560, 560, 410)
    road(); c.set_source_rgb(*st.ROAD); c.fill()
    st.setts(k, road, 560, 960, -10, 550, -10, 550, seed=31)
    for i in range(8):                                                       # the stripes, seen low: wide, flat bands
        x0 = -40 + i * 82
        st.poly(k, [(x0 + 14, 600), (x0 + 58, 600), (x0 + 66, 760), (x0 + 2, 760)], (0.93, 0.92, 0.88), 1.4)
    st.poly(k, [(-10, 548), (550, 548), (550, 562), (-10, 562)], (0.40, 0.37, 0.35), 1.6)            # the kerb


def scene(scale=2, t=0.0):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540 * scale, 960 * scale); s.set_device_scale(scale, scale)
    c = cairo.Context(s); k = Ctx(c, 0)
    st.setup_c(k)                                                            # the street behind, as setup C
    ground(k)
    # two shadows stand behind her on the road, black against the lit house (lesson 47); the double lamp behind them
    # throws their shadows toward us, over her (as the bodyguards' shadows lie across the garage floor in The Offer)
    # depth: they stand behind her (further up the road), so they are drawn first and smaller; her raised knee is in
    # front of them; their shadows, on the road, are drawn over her (they fall across her)
    import client_ob as co
    reach = (-10, 5) + co._ik(-1, -110, co.BT + 175)                 # his screen-left hand down to her coat
    if V4[0]:
        for fx in (468, BX):
            c.save(); c.translate(fx, 586); c.scale(46, 8); c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
            c.set_source_rgba(0, 0, 0, 0.6); c.fill()
    rim(k, 468, 584, 0.42, seed=4418)                                 # a rim of the lamp's light on the one standing
    st.thug(k, 468, 584, 0.42, "open", seed=4418, hands=("relax", "relax"))
    rim(k, BX, 588, 0.42, seed=4448, lean=BLEAN, pose=reach)          # the other stands behind her and bends over her
    o2 = st.thug(k, BX, 588, 0.42, reach, seed=4448, hands=("grab", "relax"), lean=BLEAN)
    body(k)
    head(k, *HEAD, ANG)
    stars(c, HEAD[0] - 20, HEAD[1] - 74, 1.0, t)
    for (x, y, a) in ((250, 630, 0.3), (330, 668, -0.5), (60, 708, 0.9), (430, 700, 0.2), (190, 720, -0.2)):
        bill(k, x, y, a, 1.0, seed=int(x))                            # the bills: on her and round her
    import hands_ps as hp
    m, hx0, hy0, w, d, side = o2["rec"][0]                            # his glove comes over her coat, plucking a bill
    hx, hy = _rot((BX, 588), o2["hands"][0], BLEAN)
    bill(k, hx - 4, hy + 10, 0.4, 1.0, seed=286)
    c.save(); c.set_matrix(m); hp.draw(k, "grab", hx0, hy0, w * 1.25, st.GLOVE, d, -1); c.restore()
    for (fx, dx) in ((468, 30), (BX + 40, -30)):
        thug_shadow(k, fx, 584, 0.42, dx, 200, 0.42, seed=4100 + fx)
    LOG["hand"] = (round(hx), round(hy))
    eng.TONE = "v3"; eng.accent_pass(s, [(st.NEON, 1.0), (st.GOLD, 0.35)])
    c = cairo.Context(s); st.light_c(c)
    return s


if __name__ == "__main__":
    big = scene(2)
    big.write_to_png("../office-noir-4/on4_lying_v3.png")
    sm = cairo.ImageSurface(cairo.FORMAT_RGB24, 270, 480); c = cairo.Context(sm); c.scale(0.5, 0.5)
    c.set_source_surface(big, 0, 0); c.paint()
    sm.write_to_png("../office-noir-4/on4_lying_phone_v3.png")
    print("ok", LOG)
