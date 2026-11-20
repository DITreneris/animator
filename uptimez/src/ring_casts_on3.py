import contextlib
import cairo
import ring_on3 as rg
import cast_on3 as ca
import client_on3 as b
import client_ob as co
import cand_bc as cb
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
    """5.1a (v4): no entrance; he arrived in 4.1. He stands in his corner in the robe, head back, one glove half up
    toward the plan; Pam beside him with the towel; the Referee and the robot at centre, clear of Sofia's card."""
    def client(k):
        rg.shadow(k, 130, F - 30, 44)
        with head_back():
            b.boxer(k, 130, F - 30, Q, (-9, 6, 150, 22), "hard", (0.7, -0.9))

    def pam(k):
        rg.shadow(k, 228, F - 14, 34); ca.pam_corner(k, 228, F - 14, SC, "p_stand", "neutral", (-0.9, 0.0))

    def ref(k):
        rg.shadow(k, 336, F - 96, 36); ca.referee(k, 336, F - 96, SC * ca.REL_REF, "ref_stand", look=(-0.8, 0), waistcoat=True)

    def robot(k):
        rg.shadow(k, 408, F - 42, 40); r.robot(k, 408, F - 42, SC * r.REL, "r_wait", "furious", side=-1)

    def sofia(k):
        so3.sofia(k, 580, F + 108, 0.92, "r_card", "spotted", (-1, -0.2), card_="ROUND 1")
    return [ref, robot, client, pam], [sofia]


CL, PAM = (128, F - 28), (292, F - 14)


def cast51b():
    """5.1c: the robe is off his shoulders; one sleeve is stretched, inside out, from his glove to Pam's two hands; she
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


def cast51d():
    """5.1c, its end: she has given up and shoves the robe back up over his shoulders; it sits crooked, one side of the
    collar up by his ear. He has not looked down."""
    cx, cf = CL

    def client(k):
        rg.shadow(k, cx, cf, 44)
        with head_back():
            o = b.boxer(k, cx, cf, Q, "b_walk", "hard", (0.7, -0.9))
        c = k.c                                             # the collar, shoved up on her side
        sx, sy = cx + 34 * Q, cf + (b.BT - 6) * Q
        cut(k, [(sx, sy + 26 * Q), (sx + 16 * Q, sy - 40 * Q), (sx + 62 * Q, sy - 22 * Q), (sx + 74 * Q, sy + 34 * Q)], b.KEY, shadow=False, lw=2.2)
        c.set_source_rgb(*b.SHADE); c.set_line_width(2.0); c.set_line_cap(1)
        c.move_to(sx + 22 * Q, sy - 24 * Q); c.line_to(sx + 40 * Q, sy + 22 * Q); c.stroke()

    def pam(k):
        px_, pf = cx + 118, F - 14
        tx, ty = cx + 62 * Q, cf + (b.BT - 14) * Q
        rg.shadow(k, px_, pf, 34)
        ca.pam_corner(k, px_, pf, SC, ca.reach(px_, pf, SC, (tx, ty), (tx + 22, ty + 26), stance="work"), "neutral", (-0.9, 0.2), stance="work")
    return [client, pam], []


@contextlib.contextmanager
def bell_pose():
    """ "ref_bell" with his other hand at his belt, not hanging where the glove stops, for one drawing."""
    old = cb.POSES_MACHO["ref_bell"]
    cb.POSES_MACHO["ref_bell"] = cb._m_ik(-1, -30, cb.M_BT + 122) + old[2:]
    try:
        yield
    finally:
        cb.POSES_MACHO["ref_bell"] = old


def cast52():
    """5.2 (v4): he swings at shoulder height; the glove stops a clear gap short, in front of the Referee's black
    waistcoat; the Referee is at the far ropes, halfway between them, one arm up; Pam's stopwatch at the frame's edge."""
    def ref(k):
        rg.shadow(k, 416, F - 110, 36)
        with bell_pose():
            ca.referee(k, 416, F - 110, SC * ca.REL_REF, "ref_bell", look=(-0.5, 0.4), waistcoat=True)

    def robot(k):
        rg.shadow(k, 500, F - 46, 40); r.robot(k, 500, F - 46, SC * r.REL, "r_wait", "furious", side=-1)

    def client(k):
        rg.shadow(k, 286, F - 40, 44); b.boxer(k, 286, F - 40, Q, "b_swing", "hard", (0.9, 0))

    def pam(k):
        x, f = 174, F - 6
        ca.pam_corner(k, x, f, SC, ca.reach(x, f, SC, (224, F - 204), (194, F - 84), stance="stand"), "neutral", (0.9, 0.1),
                      watch="hand", stance="stand")
    return [ref, robot, pam, client], []


def frames():
    """Beat 05's opening, in order: 5.1a, 5.1b (his view of the plan), 5.1c (the robe off, stuck), 5.1c's end (the robe
    shoved back on), 5.2."""
    out = []
    m, f = cast51a(); out.append(rg.frame("R1", m, f, money=True))
    out.append(rg.plan_pov())
    m, f = cast51b(); out.append(rg.frame("R3", m, f, near=False, hats=False))
    m, f = cast51d(); out.append(rg.frame("R3", m, f, near=False, hats=False))
    m, f = cast52(); out.append(rg.frame("R2", m, f, near=False, hats=False))
    return out
