import sys, math, cairo
sys.path.insert(0, "/home/claude/animator/uptimez/src")
import ps_scenes as ps, dh_cast as dc, hands_ps as hp, of_scenes as ofs
from kit import Ctx
ps.FIX_V4[0] = True; ps.NO_SHIFT[0] = False
by = {s["id"]: s for s in ps.SHOTS}
GXS = [float(x) for x in sys.argv[1].split(",")]; GSC = float(sys.argv[2]); GFEET = float(sys.argv[3]); LEANV = float(sys.argv[4])
KK = Ctx(cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 4, 4)), 0)
def pinch_pose(flip):
    """the guard's arm angles that bring one hand to his nose (searched on his own rig)."""
    b = None
    for up in range(-180, 181, 10):
        for fo in range(-180, 181, 10):
            for side in (0, 1):
                p = (up, fo, dc.GUARD_POSE[2], dc.GUARD_POSE[3]) if side == 0 else (dc.GUARD_POSE[0], dc.GUARD_POSE[1], up, fo)
                o = dc.guard(KK, 0, 0, 1.0, pose=p, flip=flip)
                nose = (o["head"][0], o["head"][1] + 12)
                d = min(math.hypot(h[0] - nose[0], h[1] - nose[1]) for h in o["hands"])
                if b is None or d < b[0]: b = (d, p)
    print("  pinch gap %.1f pose %s" % b); return b[1]
POSE = {False: pinch_pose(False), True: pinch_pose(True)}
orig = ps.cps.booth_room
STATE = [0]
def room(k, w, h, seat, tbl, x0=0):
    orig(k, w, h, seat, tbl, x0)
    c = k.c
    for i, gx in enumerate(GXS):
        sgn = -1 if i == 0 else 1; flip = (i == 1)
        c.save(); c.rectangle(-200, -200, 1400, tbl + 200); c.clip()
        if STATE[0]:
            c.translate(gx, tbl); c.rotate(sgn * LEANV); c.translate(-gx, -tbl)
            o = dc.guard(k, gx, seat + GFEET, GSC, pose=POSE[flip], flip=flip)
            nose = (o["head"][0], o["head"][1] + 14 * GSC)
            m_ = 1 if flip else -1                           # the rig draws that hand behind his head: the same hand again, on the nose
            elbow = (nose[0] + m_ * 70 * GSC, nose[1] + 62 * GSC)
            ofs.insert_cuff(c, nose, elbow, 30 * GSC, (0.91, 0.67, 0.55), (0.10, 0.10, 0.12), cuff=(0.97, 0.97, 0.95), stub=34 * GSC)
            hp.draw(k, "fist", nose[0], nose[1], 30 * GSC, (0.91, 0.67, 0.55), (-m_ * 0.75, -0.66), m_)
        else:
            dc.guard(k, gx, seat + GFEET, GSC, flip=flip)
        c.restore()
    if STATE[0]:                                             # what they smell: three wavy lines off the Client (ep 9 canon: gas and oil)
        for j, x in enumerate((352, 424, 496)):              # v2: big green stink lines (1 of 2 read the small brown ones)
            y = seat - 400 - 18 * (j % 2)
            for col, lw in (((0.10, 0.16, 0.05), 11), ((0.56, 0.78, 0.22), 6)):
                c.set_source_rgb(*col); c.set_line_width(lw); c.set_line_cap(1); c.new_path(); c.move_to(x, y + 110)
                c.curve_to(x - 30, y + 80, x + 30, y + 60, x, y + 36); c.curve_to(x - 26, y + 18, x + 20, y + 8, x, y - 10); c.stroke()
ps.cps.booth_room = room
tiles = []
for st, part in ((0, 0), (1, 0), (1, 1)):
    STATE[0] = st; ps.PART[0] = part
    surf, msgs = ps.render(by["4.3"]); tiles.append(surf); print(st, part, [x[:80] for x in msgs]); surf.write_to_png("/tmp/gags/M2_%d.png" % len(tiles))
ps.PART[0] = 0
out = cairo.ImageSurface(cairo.FORMAT_RGB24, len(tiles) * 280 + 10, 500); c = cairo.Context(out); c.set_source_rgb(.15, .15, .16); c.paint()
for j, im in enumerate(tiles):
    c.save(); c.translate(10 + j * 280, 10); c.scale(0.5, 0.5); c.set_source_surface(im, 0, 0); c.paint(); c.restore()
out.write_to_png("/tmp/gags/M2.png")
