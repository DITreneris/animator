import contextlib
import cairo
import ring_on3_v2 as rg
import cast_on3_v6 as ca
import client_on3 as b
import client_ob as co
import robot_on3 as r
import sofia_on3 as so3
from kit import Ctx, cut, INK

F, SC = rg.F, rg.SC
Q = SC * b.REL


@contextlib.contextmanager
def head_back(a=-0.24):
    """His head tipped back toward the plan, up and to screen right, for one drawing."""
    f = co.FACES["hard"]; old = f["tilt"]; f["tilt"] = old + a
    try:
        yield
    finally:
        f["tilt"] = old


def probe(fn):
    return fn(Ctx(cairo.Context(cairo.ImageSurface(cairo.FORMAT_RGB24, 8, 8)), 0))


def cast51a():
    """5.1a: he is still coming through the ropes, in the robe, his head back and one glove half up toward the plan;
    Pam waits inside with the towel; the robot and the Referee are clear of Sofia's card."""
    def client(k):
        rg.shadow(k, 112, F - 44, 44)
        with head_back():
            b.boxer(k, 112, F - 44, Q, (-9, 6, 150, 22), "hard", (0.7, -0.9))
        rg.side_rope(k, 0)                                  # the ropes, still across him

    def pam(k):
        rg.shadow(k, 222, F - 14, 34); ca.pam_corner(k, 222, F - 14, SC, "p_stand", "neutral", (-0.9, 0.0))

    def ref(k):
        rg.shadow(k, 316, F - 92, 36); ca.referee(k, 316, F - 92, SC * ca.REL_REF, "ref_stand", look=(-0.8, 0))

    def robot(k):
        rg.shadow(k, 388, F - 46, 40); r.robot(k, 388, F - 46, SC * r.REL, "r_wait", "furious", side=-1)

    def sofia(k):
        so3.sofia(k, 584, F + 108, 0.92, "r_card", "spotted", (-1, 0), card_="ROUND 1")
    return [ref, robot, client, pam], [sofia]


CL, PAM = (128, F - 28), (292, F - 14)


def cast51b():
    """5.1b: the robe is off his shoulders; one sleeve is stretched, inside out, from his glove to Pam's two hands; she
    leans back on it and watches it; his head is back, his eyes on the plan's end above them."""
    pose = (-9, 6, 56, 2)
    cl = lambda k: b.boxer(k, *CL, Q, pose, "hard", (0.7, -0.9), strip=True)
    gx, gy = probe(cl)["hands"][1]                          # his screen-right glove
    ex, ey = gx + 86, gy + 12                                # where the sleeve ends, in her hands

    def client(k):
        rg.shadow(k, CL[0], CL[1], 44)
        with head_back():
            cl(k)
        c = k.c                                             # the sleeve: taut, stopped at the glove
        cut(k, [(gx + 4, gy - 22), (ex, ey - 12), (ex + 4, ey + 12), (gx + 8, gy + 24)], b.KEY, shadow=False, lw=2.2)
        c.set_source_rgb(*b.SHADE); c.set_line_width(2.0); c.set_line_cap(1)
        for t in (0.25, 0.5, 0.75):
            x_ = gx + 8 + (ex - gx - 6) * t
            c.move_to(x_, gy - 16 + 12 * t); c.line_to(x_ + 5, gy + 18 + 2 * t); c.stroke()
        cut(k, [(ex - 3, ey - 14), (ex + 10, ey - 13), (ex + 12, ey + 14), (ex - 1, ey + 15)], b.IVORY, shadow=False, lw=1.8)

    def pam(k):
        px_, pf = PAM
        rg.shadow(k, px_, pf, 34)
        ca.pam_corner(k, px_, pf, SC, ca.reach(px_, pf, SC, (ex + 4, ey - 6), (ex + 12, ey + 8), stance=(8.0, 12)), "neutral", (-0.9, 0.7),
                      stance=(8.0, 12))
    return [client, pam], []


def cast52():
    """5.2: he is robed again; he swings; the glove stops a clear gap short, two stop marks in front of it; the Referee
    behind the robot with his arm up; Pam's stopwatch at the frame's edge."""
    cl = lambda k: b.boxer(k, 288, F - 40, Q, "b_swing", "hard", (0.9, 0))
    gx, gy = probe(cl)["hands"][1]

    def ref(k):
        rg.shadow(k, 542, F - 96, 36); ca.referee(k, 542, F - 96, SC * ca.REL_REF, "ref_bell", look=(-0.8, 0.2))

    def robot(k):
        rg.shadow(k, 492, F - 46, 40); r.robot(k, 492, F - 46, SC * r.REL, "r_wait", "furious", side=-1)

    def client(k):
        rg.shadow(k, 288, F - 40, 44); cl(k)
        c = k.c
        c.set_source_rgb(0.96, 0.96, 0.94); c.set_line_width(3.2); c.set_line_cap(1)
        for dy in (-14, 0, 14):                             # it stopped here
            c.move_to(gx + 26, gy + dy); c.line_to(gx + 38 - abs(dy) * 0.3, gy + dy * 1.25); c.stroke()

    def pam(k):
        x, f = 196, F - 6
        ca.pam_corner(k, x, f, SC, ca.reach(x, f, SC, (246, F - 204), (216, F - 84), stance="stand"), "neutral", (0.9, 0.1),
                      watch="hand", stance="stand")
    return [ref, robot, pam, client], []


SPECS = (("R1", cast51a, dict(money=True)), ("R3", cast51b, dict(near=False, hats=False)), ("R2", cast52, dict(near=False, hats=False)))
