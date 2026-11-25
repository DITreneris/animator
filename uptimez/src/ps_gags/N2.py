import sys, math, cairo
sys.path.insert(0, "/home/claude/animator/uptimez/src")
import ps_scenes as ps, ps_motion as m, robot_on3 as ro, hands_ps as hp, dh_cast as dc
from kit import INK, Ctx
ps.FIX_V4[0] = True; ps.pss.NO_DOOR_CONFETTI[0] = ps.rp.SUN_UP[0] = True
ps.sp.CV_WORD[0] = "HR?"; ps.NO_SHIFT[0] = True
F = ps.F; SC = ps.SC; P = ps.P
GX, RX, SX = [float(x) for x in sys.argv[1:4]]
GUP, GFO = [float(x) for x in sys.argv[5].split(',')]
CAM = tuple(float(x) for x in sys.argv[4].split(","))
GS = 0.56 / 0.52 * 0.60
CAN = 1.3
def cast53(stage):
    def cast(k):
        heads = {}; c = k.c
        PAM = SX != 0
        ps.pm.stool(k, P["pam_stool"][0], F + P["pam_stool"][1], SC["pam"])
        pf = (P["pam_stool"][0], F + P["pam_stool"][1] - 98 * SC["pam"])
        tmp = cairo.ImageSurface(cairo.FORMAT_RGB24, 4, 4)
        hh = ps.pm.pam(Ctx(cairo.Context(tmp), 0), *pf, SC["pam"], "rail", "frozen", (1, -0.1))["hands"]
        ps.pm.blind_rail(k, hh[0], hh[1], SC["pam"])
        gp = (dc.GUARD_POSE[0], dc.GUARD_POSE[1], GUP, GFO) if stage == 0 else dc.GUARD_POSE
        og = dc.guard(k, GX, F + 46, GS, pose=gp)                 # bodyguard 2, one step inside the door, behind Pam's stool
        heads["guard"] = og["head"] + (40 * GS,)
        o, heads["pam"] = ps.pam(k, pf, "rail", "frozen", (1, -0.1), late=False)
        ps.pm.rail_bar(k, o["hands"][0], o["hands"][1], SC["pam"]); hp.redraw_late(k)
        gh = max(og["hands"], key=lambda h: h[0]); ry = F + 50
        def reach(T):
            kk = Ctx(cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 4, 4)), 0); b = None
            for up in range(-170, 10, 6):
                for fo in range(-150, 60, 6):
                    oo, _ = ps.robot(kk, (RX, ry), arms=((up, fo), (10, 0))); h = oo["hands"][0]
                    d = math.hypot(h[0] - T[0], h[1] - T[1])
                    if b is None or d < b[0]: b = (d, up, fo)
            return b
        if stage == 0:
            can = (gh[0] + 16, gh[1] + 14)
            d, up, fo = reach((gh[0] + 34, gh[1] - 8)); print("   stage0 robot hand gap %.1f arm %s" % (d, (up, fo)))
            _, heads["robot"] = ps.robot(k, (RX, ry), arms=((up, fo), (10, 0)), look=(-1, 0.6))
            ps.rp.oil_can(k, gh[0] + 2, gh[1] + 18, 1.15, 0.0)     # in front: the can is the shot
        else:
            arm = (120, 60)                                    # the can held in its right hand, level; its spout over the left joint
            larm = (-70, -110)
            c.push_group(); orb, _ = ps.robot(k, (RX, ry), arms=(larm, arm)); c.pop_group()
            rh = orb["hands"][1]
            _, heads["robot"] = ps.robot(k, (RX, ry), arms=(larm, arm), visor="heart", look=(-1, 1))
            tip = ps.rp.oil_can(k, rh[0] + 4, rh[1] + 16, 1.15, 0.0, drop=False)
            c.set_source_rgb(0.07, 0.06, 0.06)
            for dy, r_ in ((16, 1.0), (52, 1.4)):               # two big drops falling from the spout onto its raised joint
                c.new_path(); c.move_to(tip[0], tip[1] + dy - 12 * r_); c.curve_to(tip[0] + 9 * r_, tip[1] + dy, tip[0] + 6 * r_, tip[1] + dy + 9 * r_, tip[0], tip[1] + dy + 9 * r_)
                c.curve_to(tip[0] - 6 * r_, tip[1] + dy + 9 * r_, tip[0] - 9 * r_, tip[1] + dy, tip[0], tip[1] + dy - 12 * r_); c.fill()
        if SX > 0:
            osf, heads["sofia"] = ps.sofia(k, (SX, F + 62), "chest", "smile", (-1, 0.2))
            hx, hy = osf["hands"][0]
            ps.sp.cv_coo(k, hx - 2, hy + 6, 0.72)
        print("   guard hands", [[round(v) for v in h] for h in og["hands"]], "head", [round(v) for v in og["head"]])
        return heads
    return cast
tiles = []
for stage in (0, 1):
    sh = ps.S("5.3", CAM, dict(blind="rehung", tape=True, spun=True), cast53(stage))
    surf, msgs = ps.render(sh); tiles.append(surf); print(stage, sorted(set(x[:80] for x in msgs))); surf.write_to_png("/tmp/gags/N2_%d.png" % stage)
out = cairo.ImageSurface(cairo.FORMAT_RGB24, len(tiles) * 280 + 10, 500); c = cairo.Context(out); c.set_source_rgb(.15, .15, .16); c.paint()
for j, im in enumerate(tiles):
    c.save(); c.translate(10 + j * 280, 10); c.scale(0.5, 0.5); c.set_source_surface(im, 0, 0); c.paint(); c.restore()
out.write_to_png("/tmp/gags/N2.png")
