import sys, math, cairo
sys.path.insert(0, "/home/claude/animator/uptimez/src")
import ps_scenes as ps, ps_motion as m, dh_cast as dc
from kit import INK, Ctx
ps.gags_v5(); ps.pss.NO_DOOR_CONFETTI[0] = ps.rp.SUN_UP[0] = True; ps.NO_SHIFT[0] = True
F, W, H = ps.F, ps.W, ps.H
def mask(draw_bg, draw_all):
    a = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); draw_bg(Ctx(cairo.Context(a), 0)); a.flush(); B = bytes(a.get_data())
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); draw_all(Ctx(cairo.Context(s), 0)); s.flush(); d = s.get_data()
    out = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); out.flush(); od = out.get_data()
    for i in range(0, len(B), 4):
        v = 0 if (abs(d[i] - B[i]) + abs(d[i + 1] - B[i + 1]) + abs(d[i + 2] - B[i + 2])) > 24 else 255
        od[i] = od[i + 1] = od[i + 2] = v
    out.mark_dirty(); return out
def mask_render(sid, cam, room, cast):
    return mask(lambda k: _paint(ps.render(ps.S(sid, cam, room, lambda kk: {}))[0], k),
                lambda k: _paint(ps.render(ps.S(sid, cam, room, cast))[0], k))
def _paint(surf, k):
    k.c.set_source_surface(surf, 0, 0); k.c.paint()
def sheet(tiles, path):
    o = cairo.ImageSurface(cairo.FORMAT_RGB24, 10 + 3 * 280, 520); c = cairo.Context(o); c.set_source_rgb(.55, .55, .55); c.paint()
    for j, im in enumerate(tiles):
        c.save(); c.translate(10 + j * 280, 10); c.scale(0.5, 0.5); c.set_source_surface(im, 0, 0); c.paint(); c.restore()
        c.set_source_rgb(0, 0, 0); c.set_font_size(18); c.move_to(14 + j * 280, 510); c.show_text(str(j + 1))
    o.write_to_png(path)
G = dc.GUARD_POSE
# 1. the guards' reaction to the oily Client (4.3)
def booth(variant, with_people=True):
    def draw(k):
        c = k.c; seat, tbl = 760, 700
        ps.cps.booth_room(k, W, H, seat, tbl)
        if with_people:
            for i, gx in enumerate((300, 548)):
                sgn, flip = (-1, False) if i == 0 else (1, True)
                c.save(); c.rectangle(-200, -200, 1400, tbl + 200); c.clip()
                c.translate(gx, tbl); c.rotate(sgn * (0.24 if variant == 2 else 0.13)); c.translate(-gx, -tbl)
                if variant == 0:   pose, front = (G[0], G[1], -100, -60), 1      # pinching his nose (the board)
                elif variant == 1: pose, front = (-150, -30, -110, -40), 1       # a flat hand over his face, the other fanning
                else:              pose, front = (-150, -120, -40, -150), None   # leaning hard away, both palms out
                dc.ARM_FRONT[0] = front
                try: dc.guard(k, gx, seat + 10, 0.95, pose=pose, flip=flip)
                finally: dc.ARM_FRONT[0] = None
                c.restore()
            import client_on3 as co
            ps.cps.cast_client(k, 424, seat - co.HIP * 1.15, 1.15, look=(-1.2, 1.4), targets=[(265, tbl - 128), (464, tbl - 6)],
                               clip_hip=True, hands={-1: "point"}, aim=(230, tbl - 122))
        ps.cps.table(k, W, tbl)
    return draw
sheet([mask(booth(v, False), booth(v)) for v in range(3)], "/tmp/sil/g1.png")
# 2. the oil can (5.3b)
CAM = ps.TREAT_53
def treat(variant):
    def cast(k):
        c = k.c
        og = dc.guard(k, 196, F + 46, ps.GUARD_S, pose=(G[0], G[1], 10, 20))
        rxy = (312, F + 50)
        if variant == 0:   arms, hand, ang = (ps.LARM_53[0], (20, 10)), 0, 0.0         # held up by its handle (the board)
        elif variant == 1: arms, hand, ang = ((-20, -30), (20, 10)), 0, 0.0           # still in the guard's hand, the robot's hand on it
        else:              arms, hand, ang = ((-40, -70), (40, 70)), 0, 0.0           # hugged to its chest in both arms
        c.push_group(); orb, _ = ps.robot(k, rxy, arms=arms); c.pop_group()
        rh = orb["hands"][hand]
        if variant == 1:
            gh = max(og["hands"], key=lambda h: h[0]); rh = gh
        if variant == 2:
            rh = ((orb["hands"][0][0] + orb["hands"][1][0]) / 2, (orb["hands"][0][1] + orb["hands"][1][1]) / 2)
        ps.robot(k, rxy, arms=arms, visor="heart")
        hx_, hy_ = ps.rp.CAN_HANDLE[0] * 1.15, ps.rp.CAN_HANDLE[1] * 1.15
        ps.rp.oil_can(k, rh[0] - hx_, rh[1] - hy_ if variant != 2 else rh[1] + 20, 1.15, ang)
        return {}
    return cast
sheet([mask_render("5.3", CAM, dict(blind="rehung", tape=True, spun=True), treat(v)) for v in range(3)], "/tmp/sil/g2.png")
# 3. Don's tired arm (3.4): three key poses of three gestures
DX, FD = ps.tape_x(140) - 190, F + 140
TH = ps.dp.POSES["thumbs"]
c0 = m._board_cam("3.4"); ps.NO_SHIFT[0] = True; CAM3 = (DX + 85 / 2.3, c0[1] - 10, 2.3)
def pose3(variant):
    def cast(k):
        ps.robot(k, "rob_tape", selfie=0.6, phone="public", arms=((-95, 0), (-20, -40)), tele=-1.25, phone_s=0.58)
        if variant == 0:      # the arm dropped halfway, heaved (the gag)
            ik = m.don_arms(DX, FD, right=(DX + 70, FD - 150)); pose = (TH[0], TH[1], ik[2], ik[3])
        elif variant == 1:    # the arm hanging, the thumb still up at his knee
            ik = m.don_arms(DX, FD, right=(DX + 60, FD - 70)); pose = (TH[0], TH[1], ik[2], ik[3])
        else:                 # the other hand propping the raised arm's elbow
            o_, _ = ps.don(Ctx(cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 4, 4)), 0), (DX, FD), TH, "grin", (0, -0.3), chin=1)
            el = (DX + 62, FD - 175)
            ik = m.don_arms(DX, FD, left=el); pose = (ik[0], ik[1], TH[2], TH[3])
        ps.don(k, (DX, FD), pose, "grin", (0, -0.3), chin=1, hands=("thumb", "thumb"))
        return {}
    return cast
sheet([mask_render("3.4", CAM3, ps.ROOM3, pose3(v)) for v in range(3)], "/tmp/sil/g3.png")
print("ok")
