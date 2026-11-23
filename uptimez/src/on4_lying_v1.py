"""OFFICE NOIR 4, 3.2-3.6: Pam-Cat lying on the crossing, drawn as a standalone picture first (lessons 152, 153), with
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
NOT imported by any film. python3 on4_lying.py -> ../office-noir-4/on4_lying_v1.png (1080x1920) and a phone copy."""
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


def head(k, x, y, ang, s=S, face="wide", look=(0.4, -0.5)):
    """Pam-Cat's head only: the whole rig drawn, clipped to the head's own region, turned by ang."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    c.new_path()
    c.rectangle(-62, -100, 124, 128)                                 # hair, ears and face down to the jaw line
    c.save(); c.translate(0, 26); c.scale(40, 26); c.arc(0, 0, 1, 0, math.pi); c.restore()   # the jaw, round
    c.clip()
    c.scale(1 / s, 1 / s)
    o = oc.pam_cat(k, 0, -oc.HY * s, s, "sag", face, look)          # drawn with its head at (0, 0)
    c.restore()
    return o


def stars(c, x, y, s=1.0, t=0.0):
    """Dazed stars circling over her head."""
    for i in range(3):
        a = t * 2.4 + i * 2 * math.pi / 3
        oc.star(c, x + math.cos(a) * 46 * s, y + math.sin(a) * 14 * s, 11 * s, (0.98, 0.95, 0.80))


def contact(c, cx, cy, rx, ry, a=0.42):
    c.save(); c.translate(cx, cy); c.scale(rx, ry)
    g = cairo.RadialGradient(0, 0, 0.1, 0, 0, 1)
    g.add_color_stop_rgba(0, 0, 0, 0, a); g.add_color_stop_rgba(0.7, 0, 0, 0, a * 0.5); g.add_color_stop_rgba(1, 0, 0, 0, 0)
    c.set_source(g); c.arc(0, 0, 1, 0, 2 * math.pi); c.fill(); c.restore()


def body(k):
    """Her body from the neck: shoulders by the head, the hips to the right; the coat, the belt, the legs, the boots."""
    c = k.c
    X0, Y = HEAD[0] + 34, BACK_Y
    # contact shadows first, under everything that touches the road
    for (cx, rx, ry) in ((HEAD[0] + 6, 52, 10), (X0 + 70, 80, 11), (X0 + 190, 60, 10), (X0 + 330, 40, 8), (X0 + 268, 26, 7)):
        contact(c, cx, Y + 6, rx, ry)
    # the arm flung out on the road beyond her head, gloved (clear of the head, so it is not read as part of it)
    contact(c, X0 - 70, Y + 4, 60, 7)
    _tube(k, [(X0 + 20, Y - 30), (X0 - 40, Y - 10), (X0 - 110, Y - 4)], (13, 11, 9), oc.COAT, lw=2.6)
    kit.ellipse(k, X0 - 120, Y - 6, 13, 11, oc.GLOVE_DARK, 5101, shadow=False, lw=2)
    # the straight leg, along the road
    _tube(k, [(X0 + 190, Y - 22), (X0 + 260, Y - 18), (X0 + 322, Y - 14)], (19, 15, 12), oc.SUIT_LEG, lw=2.8)
    cut(k, [(X0 + 316, Y - 30), (X0 + 346, Y - 34), (X0 + 352, Y - 4), (X0 + 318, Y)], oc.BOOT, shadow=False, lw=2)
    # the torso: shoulder, chest (rising), waist, hip
    _blob(k, [(X0, Y - 66), (X0 + 40, Y - 76), (X0 + 100, Y - 70), (X0 + 140, Y - 54), (X0 + 180, Y - 58),
              (X0 + 214, Y - 44), (X0 + 220, Y - 12), (X0 + 190, Y + 2), (X0 + 100, Y + 2), (X0 + 20, Y), (X0 - 8, Y - 26)],
          oc.COAT, lw=3.2)
    _line(c, [(X0 + 46, Y - 60), (X0 + 96, Y - 50), (X0 + 136, Y - 40)], oc.COAT_DARK, 2.2)       # a fold across the chest
    for bx in (X0 + 70, X0 + 108):                                                                 # the coat's buttons
        kit.ellipse(k, bx, Y - 40, 3.4, 3.4, (0.34, 0.34, 0.36), 5110 + bx, shadow=False, lw=1.2)
    cut(k, [(X0 + 146, Y - 58), (X0 + 166, Y - 62), (X0 + 170, Y), (X0 + 150, Y + 2)], oc.COAT_DARK, shadow=False, lw=1.6)   # the belt
    cut(k, [(X0 + 150, Y - 36), (X0 + 166, Y - 38), (X0 + 167, Y - 22), (X0 + 151, Y - 20)], (0.55, 0.55, 0.57), shadow=False, lw=1.2)
    # the collar at her neck, grey and wide
    cut(k, [(X0 - 10, Y - 60), (X0 + 26, Y - 80), (X0 + 40, Y - 56), (X0 + 10, Y - 30)], oc.COLLAR, shadow=False, lw=2.0)
    # the near leg, knee up, the sole flat on the road (alive: she will sit up)
    _tube(k, [(X0 + 196, Y - 40), (X0 + 246, Y - 104), (X0 + 286, Y - 18)], (21, 17, 13), oc.SUIT_LEG, lw=3.0)
    c.set_source_rgba(1, 1, 1, 0.14); c.new_path(); c.arc(X0 + 246, Y - 104, 9, 0, 2 * math.pi); c.fill()   # the knee, lit
    cut(k, [(X0 + 272, Y - 22), (X0 + 304, Y - 20), (X0 + 310, Y + 2), (X0 + 270, Y + 2)], oc.BOOT, shadow=False, lw=2)
    # the arm across her belt
    _tube(k, [(X0 + 40, Y - 56), (X0 + 90, Y - 30), (X0 + 138, Y - 48)], (12, 11, 9), oc.COAT, lw=2.6)
    kit.ellipse(k, X0 + 146, Y - 50, 12, 10, oc.GLOVE_DARK, 5102, shadow=False, lw=2)


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


def thug_shadow(k, fx, fy, s, dx, dy, a=0.55, pose="open", seed=4100):
    """The ground shadow of a thug standing at (fx, fy): the same body (client_ob, as on4_street.thug), projected onto
    the road toward (dx, dy) by the lamp behind him."""
    import client_ob as co
    c = k.c
    H = 300 * s
    c.push_group()
    c.save(); c.translate(fx, fy); c.transform(cairo.Matrix(1, 0, -dx / H, -dy / H, 0, 0)); c.translate(-fx, -fy)
    co.client(k, fx, fy, s, pose, "plain", look=(0, 0), roll=False, badge=False, seed=seed)
    c.restore()
    g = c.pop_group()
    c.set_source_rgba(0.02, 0.02, 0.03, a); c.mask(g)


def rim(k, fx, fy, s, seed=4100):
    """The thug's outline lit from behind: his body, pale, a little bigger and raised, under the black figure."""
    import client_ob as co
    c = k.c
    for dx, dy in ((0, -3), (-2.5, -1.5), (2.5, -1.5)):
        c.push_group()
        c.save(); c.translate(dx, dy)
        co.client(k, fx, fy, s, "open", "plain", look=(0, 0), roll=False, badge=False, seed=seed)
        c.restore()
        g = c.pop_group()
        c.set_source_rgba(0.85, 0.85, 0.82, 0.9); c.mask(g)


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
    for fx in (318, 430):                    # a rim of the lamp's light on their heads and shoulders, so their black
        rim(k, fx, 584, 0.42, seed=4100 + fx)  # heads do not sink into the night sky behind them (as Office Noir 2's hat)
        st.thug(k, fx, 584, 0.42, "open", seed=4100 + fx)
    body(k)
    head(k, *HEAD, ANG)
    stars(c, HEAD[0] - 20, HEAD[1] - 70, 1.0, t)
    for (fx, dx) in ((318, -50), (430, 20)):
        thug_shadow(k, fx, 584, 0.42, dx, 300, 0.48, seed=4100 + fx)
    eng.TONE = "v3"; eng.accent_pass(s, [(st.NEON, 1.0), (st.GOLD, 0.35)])
    c = cairo.Context(s); st.light_c(c)
    return s


if __name__ == "__main__":
    big = scene(2)
    big.write_to_png("../office-noir-4/on4_lying_v1.png")
    sm = cairo.ImageSurface(cairo.FORMAT_RGB24, 270, 480); c = cairo.Context(sm); c.scale(0.5, 0.5)
    c.set_source_surface(big, 0, 0); c.paint()
    sm.write_to_png("../office-noir-4/on4_lying_phone_v1.png")
    print("ok")
