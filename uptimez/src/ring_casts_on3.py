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
    """5.1a: he is caught mid-step coming through the far ropes on his side, in the robe, toward us: Pam holds the top
    two ropes up in one hand, the low one still crosses his trailing shin. The robot and the Referee wait."""
    cx, cf = 168, rg.FAR + 14
    peak = (222, rg.FAR - 126)
    x0, x1 = rg.POST_F

    def ropes(k, which):
        c = k.c
        c.set_source_rgb(0.84, 0.84, 0.86); c.set_line_width(5); c.set_line_cap(1); c.set_line_join(1)
        if which == "back":                                 # the top two, gathered up in her hand
            for t_, dy in ((92, 0), (62, 9)):
                c.move_to(x0, rg.FAR - t_); c.line_to(peak[0] - 70, rg.FAR - t_ - 4); c.line_to(peak[0], peak[1] + dy)
                c.line_to(peak[0] + 80, rg.FAR - t_ - 2); c.line_to(x1, rg.FAR - t_); c.stroke()
        else:                                               # the low one: in front of his trailing leg only
            c.move_to(x0, rg.FAR - 32); c.line_to(cx - 4, rg.FAR - 32); c.stroke()
            c.move_to(cx + 44, rg.FAR - 32); c.line_to(x1, rg.FAR - 32); c.stroke()
        c.set_line_cap(0)

    def client(k):
        ropes(k, "back")
        rg.shadow(k, cx + 8, cf, 46)
        c = k.c
        c.save(); c.translate(cx, cf); c.rotate(0.16); c.translate(-cx, -cf)                      # ducking in under them
        with head_back(-0.06):
            b.boxer(k, cx, cf, Q, (-9, 6, 24, 10), "hard", (0.8, -0.5))
        c.restore()
        ropes(k, "front")

    def pam(k):
        px_, pf = 262, rg.FAR + 30
        rg.shadow(k, px_, pf, 34)
        ca.pam_corner(k, px_, pf, SC, ca.reach(px_, pf, SC, (peak[0] + 4, peak[1] + 6), (px_ + 30, pf - 96), stance="stand"), "neutral",
                      (-0.9, 0.2), stance="stand")

    def ref(k):
        rg.shadow(k, 336, F - 84, 36); ca.referee(k, 336, F - 84, SC * ca.REL_REF, "ref_stand", look=(-0.8, 0))

    def robot(k):
        rg.shadow(k, 408, F - 40, 40); r.robot(k, 408, F - 40, SC * r.REL, "r_wait", "furious", side=-1)

    def sofia(k):
        so3.sofia(k, 580, F + 108, 0.92, "r_card", "spotted", (-1, -0.2), card_="ROUND 1")
    return [client, pam, ref, robot], [sofia]


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
    """5.2: he is robed again; he swings, a little low; the glove stops a clear gap short; the Referee is at the far
    ropes, halfway between them, one arm up, his dark trousers behind the gap; Pam's stopwatch at the frame's edge."""
    def ref(k):
        rg.shadow(k, 420, F - 110, 36)
        with bell_pose():
            ca.referee(k, 420, F - 110, SC * ca.REL_REF, "ref_bell", look=(-0.5, 0.4))

    def robot(k):
        rg.shadow(k, 500, F - 46, 40); r.robot(k, 500, F - 46, SC * r.REL, "r_wait", "furious", side=-1)

    def client(k):
        rg.shadow(k, 286, F - 40, 44); b.boxer(k, 286, F - 40, Q, (-9, 6, 70, -2), "hard", (0.9, 0.1))

    def pam(k):
        x, f = 174, F - 6
        ca.pam_corner(k, x, f, SC, ca.reach(x, f, SC, (224, F - 204), (194, F - 84), stance="stand"), "neutral", (0.9, 0.1),
                      watch="hand", stance="stand")
    return [ref, robot, pam, client], []


def frames():
    """The four frames of beat 05's opening, in order: 5.1a, 5.1b (his view of the plan), 5.1c (the robe), 5.2."""
    out = []
    m, f = cast51a(); out.append(rg.frame("R1", m, f, money=True, far_ropes=False))
    out.append(rg.plan_pov())
    m, f = cast51b(); out.append(rg.frame("R3", m, f, near=False, hats=False))
    m, f = cast52(); out.append(rg.frame("R2", m, f, near=False, hats=False))
    return out
