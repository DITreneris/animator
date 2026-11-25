"""Office Noir 2 v33 (25 Nov; Tomas: "we have big problems with fingers and hands in this film"): the film was drawn on
17-20 Nov, before the series had one hand (hands_ps, 23 Nov) and the rules page (docs/rules-hands-and-phones.md). Its
inserts used a red tube with a ball, or noir2_cast.hand enlarged five times. Here: a gloved forearm that tapers to the
wrist, out of the nearest frame edge, with hands_ps's hand on it; the thing held is drawn first, then the fingers.
  python3 on2_hands.py out.png  ->  the hand sheet: the six shapes, her poses old over new, three inserts old over new"""
import math
import cairo
import hands_ps as hp
import noir2_cast as n
from kit import INK


def forearm(k, x0, y0, x1, y1, w0, w1, hem=True):
    """a gloved forearm from (x0, y0), off the frame, to the wrist (x1, y1): wider at the elbow end, one outline"""
    c = k.c
    a = math.atan2(y1 - y0, x1 - x0); nx, ny = -math.sin(a), math.cos(a)
    pts = [(x0 + nx * w0 / 2, y0 + ny * w0 / 2), (x1 + nx * w1 / 2, y1 + ny * w1 / 2), (x1 - nx * w1 / 2, y1 - ny * w1 / 2), (x0 - nx * w0 / 2, y0 - ny * w0 / 2)]
    c.new_path(); c.move_to(*pts[0])
    for p in pts[1:]:
        c.line_to(*p)
    c.close_path(); c.set_source_rgb(*n.KEY); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(3.0); c.set_line_join(1); c.stroke()
    c.set_source_rgb(*n.GOWN_SHADE); c.set_line_width(2.0); c.set_line_cap(1)                 # the glove's folds above the wrist
    for u in (0.80, 0.88):
        px, py = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
        ww = (w0 + (w1 - w0) * u) * 0.36
        c.move_to(px + nx * ww, py + ny * ww); c.curve_to(px + nx * ww * 0.3 + math.cos(a) * 5, py + ny * ww * 0.3 + math.sin(a) * 5,
                                                          px - nx * ww * 0.3 + math.cos(a) * 5, py - ny * ww * 0.3 + math.sin(a) * 5, px - nx * ww, py - ny * ww); c.stroke()
    return (math.cos(a), math.sin(a))


def over_shoulder(k, wrist, shape, w, arm=1, under=None, side=1):
    """v35 (cold test v34: "a red hose from the corner", 3/3): the camera over her shoulder. Her hair and her bare
    shoulder big in the near corner, the upper arm (skin, then the glove's top) to an elbow inside the frame, the
    forearm to the wrist, the hand on it (hands_ps glove)"""
    import sofia_ss as ss
    import sofia_ob as so
    c = k.c
    W, H = 540, 960
    shx, shy = (W - 120, H - 70) if side > 0 else (120, H - 70)
    ex, ey = (wrist[0] + shx) / 2 + side * 40, max(wrist[1], shy - 220) + 70
    ex = min(W - 40, max(40, ex)); ey = min(H - 40, ey)
    c.set_source_rgb(*so.SKIN); c.new_path()                                                  # her bare shoulder and back, near
    c.save(); c.translate(shx + side * 70, shy + 90); c.scale(170, 130); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(3.0); c.stroke()
    a = math.atan2(ey - shy, ex - shx)
    gx, gy = shx + (ex - shx) * 0.45, shy + (ey - shy) * 0.45
    for (x0, y0, x1, y1, w0, w1, col) in ((shx, shy, gx, gy, w * 1.3, w * 1.2, so.SKIN), (gx, gy, ex, ey, w * 1.2, w * 1.05, n.KEY)):
        an = math.atan2(y1 - y0, x1 - x0); nx, ny = -math.sin(an), math.cos(an)
        c.new_path(); c.move_to(x0 + nx * w0 / 2, y0 + ny * w0 / 2); c.line_to(x1 + nx * w1 / 2, y1 + ny * w1 / 2); c.line_to(x1 - nx * w1 / 2, y1 - ny * w1 / 2); c.line_to(x0 - nx * w0 / 2, y0 - ny * w0 / 2); c.close_path()
        c.set_source_rgb(*col); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(3.0); c.stroke()
    c.set_source_rgb(*n.KEY); c.new_path(); c.arc(ex, ey, w * 0.52, 0, 2 * math.pi); c.fill()             # the elbow, round
    d = forearm(k, ex, ey, wrist[0], wrist[1], w * 0.95, w * 0.62)
    c.set_source_rgb(*n.KEY); c.new_path(); c.arc(ex, ey, w * 0.46, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(*ss.HAIR); c.new_path()                                                  # her hair over the shoulder, nearest of all
    c.move_to(shx + side * 120, shy - 320); c.curve_to(shx - side * 30, shy - 300, shx - side * 60, shy - 160, shx - side * 40, shy - 40)
    c.curve_to(shx - side * 20, shy + 10, shx + side * 40, shy + 40, shx + side * 140, shy + 40); c.close_path()
    c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(3.0); c.stroke()
    c.set_source_rgb(*ss.HAIR_SHADE); c.set_line_width(2.4); c.set_line_cap(1)
    for i in range(4):
        c.move_to(shx + side * (100 - i * 30), shy - 300 + i * 20); c.curve_to(shx - side * (10 + i * 8), shy - 220 + i * 30, shx - side * (30 - i * 10), shy - 120, shx - side * (10 - i * 12), shy - 20); c.stroke()
    if under:
        under()
    hp.draw(k, shape, wrist[0] + d[0] * w * 0.30, wrist[1] + d[1] * w * 0.30, w, n.KEY, d, arm)
    return d


def insert(k, edge, wrist, shape, w, arm=1, under=None):
    """her arm into an insert: forearm from the frame's edge, then what she holds (under()), then the hand over it"""
    d = forearm(k, edge[0], edge[1], wrist[0], wrist[1], w * 0.95, w * 0.62)
    if under:
        under()
    hp.draw(k, shape, wrist[0] + d[0] * w * 0.30, wrist[1] + d[1] * w * 0.30, w, n.KEY, d, arm)
    return d


GLOVE_CFG = {"shade": n.GOWN_SHADE, "shine": False}


def sheet2(out):
    """v2: hands_ps's glove mode (hands_ps.GLOVE), v1 over v2: the shapes, her poses close, the four inserts"""
    import kit
    import on2_motion as m
    W, H = 2400, 3050
    sf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(sf); k = kit.Ctx(c, 0)
    c.set_source_rgb(0.62, 0.62, 0.64); c.paint()

    def lab(t, x, y, sz=24, bold=1):
        c.select_font_face("Inter", 0, bold); c.set_font_size(sz); c.set_source_rgb(*INK); c.move_to(x, y); c.show_text(t)
    lab("OFFICE NOIR 2 v34 - the glove: hands_ps in glove mode. v1 over v2.", 40, 46, 30)
    for r, on in enumerate((False, True)):
        hp.GLOVE[0] = GLOVE_CFG if on else None
        y0 = 190 + r * 330
        lab("v1" if not on else "v2: one silhouette, longer thinner tapered fingers of four lengths, folds at the wrist", 900 if on else 40, y0 - 122, 22)
        for i, g in enumerate(("quiet", "point", "grab", "fist", "palm")):
            x = 240 + i * 460
            for j, arm in enumerate((-1, 1)):
                dd = {"point": (1.0, 0.0), "palm": (0.0, -1.0), "grab": (1.0, 0.0)}.get(g, (0.0, 1.0))
                hx_, hy_ = (x - 40, y0 - 50 + j * 130) if dd[0] else (x - 90 + j * 180, y0 + 20)
                forearm(k, hx_ - dd[0] * 150, hy_ - dd[1] * 150, hx_, hy_, 70, 48)
                hp.draw(k, g, hx_ + dd[0] * 24, hy_ + dd[1] * 24, 80, n.KEY, dd, arm)
            lab(g, x - 40, y0 + 170, 22)
    poses = (("g_stand", "standing (5.1)"), ("g_pose", "the pose (1.2)"), ("g_mirror", "the compact (2.3)"), ("g_fan", "the money (5.2)"),
             ("g_offer", "her hand out (6.7)"), ("g_hide", "under the desk (7.1)"))
    n.HAND3[0] = n.NO_BAG[0] = n.HIDE3[0] = n.BACK2[0] = n.BACK3[0] = True
    for r, on in enumerate((False, True)):
        hp.GLOVE[0] = GLOVE_CFG if on else None
        y = 1360 + r * 640
        lab("her poses, v1" if not on else "her poses, v2", 40, y - 560, 22)
        for i, (p, name) in enumerate(poses):
            c.save(); c.rectangle(40 + i * 390, y - 540, 380, 560); c.clip()
            n.star(k, 230 + i * 390, y + 330, 2.6, p, "interested", (0.2, 0.0), wrap=False)
            c.restore()
            lab(name, 60 + i * 390, y + 46, 18, 0)
    n.HAND3[0] = n.NO_BAG[0] = n.HIDE3[0] = n.BACK2[0] = n.BACK3[0] = False
    rows, total = m.timing("A2")
    shots = (("5.5", 1.0, "5.5 the note"), ("5.6", 1.5, "5.6 her number"), ("4.1a", 0.55, "4.1a the coin"), ("6.2c", 1.2, "6.2c the plan"))
    for r, on in enumerate((False, True)):
        m.V34[0] = on
        lab("inserts, v1 (v33)" if not on else "inserts, v2 (v34)", 40 + r * 1200, 2500, 22)
        for i, (sh, tl, name) in enumerate(shots):
            row = [x for x in rows if x["shot"] == sh][0]
            f = m.frame(row, tl, row["start"] + tl)
            c.save(); c.translate(40 + r * 1200 + i * 290, 2520); c.scale(0.5, 0.5); c.set_source_surface(f, 0, 0); c.paint(); c.restore()
            lab(name, 40 + r * 1200 + i * 290, 3030, 15, 0)
    hp.GLOVE[0] = None
    sf.write_to_png(out); print("wrote", out)


def sheet(out):
    import kit
    import on2_motion as m
    import on2_motion_b5 as b5
    W, H = 2400, 2500
    sf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(sf); k = kit.Ctx(c, 0)
    c.set_source_rgb(0.62, 0.62, 0.64); c.paint()

    def lab(t, x, y, sz=26, bold=1):
        c.select_font_face("Inter", 0, bold); c.set_font_size(sz); c.set_source_rgb(*INK); c.move_to(x, y); c.show_text(t)
    lab("OFFICE NOIR 2 v33 - her hand: hands_ps (the series' one hand) in the glove's red. Old over new, the film's own poses, one scale.", 40, 50, 30)
    for i, g in enumerate(("quiet", "point", "grab", "fist", "palm", "relax")):                  # the shapes
        x = 200 + i * 380
        for j, (arm, d) in enumerate(((-1, (0.0, 1.0)), (1, (0.0, 1.0)))):
            dd = {"point": (1.0, 0.0), "palm": (0.0, -1.0), "grab": (1.0, 0.0)}.get(g, d)
            hx_, hy_ = (x - 20, 150 + j * 110) if dd[0] else (x - 80 + j * 160, 210)
            forearm(k, hx_ - dd[0] * 130, hy_ - dd[1] * 130, hx_, hy_, 54, 36)
            hp.draw(k, g, hx_ + dd[0] * 18, hy_ + dd[1] * 18, 58, n.KEY, dd, arm)
        lab(g, x - 40, 330, 24)
    poses = (("g_stand", {}, "standing (5.1)"), ("g_pose", {}, "the pose (1.2)"), ("g_mirror", {}, "the compact (2.3)"), ("g_fan", {}, "the money (5.2)"),
             ("g_down", {}, "at the bar (5.3)"), ("g_offer", {}, "her hand out (6.7)"), ("g_hide", {}, "under the desk (7.1)"))
    for r, on in enumerate((False, True)):
        n.HAND3[0] = n.NO_BAG[0] = n.HIDE3[0] = n.BACK2[0] = n.BACK3[0] = on
        y = 900 + r * 620
        lab("BEFORE: a ball at each wrist" if not on else "AFTER: hands_ps, a shape per pose; what she holds is drawn first, the fingers over it", 40, y - 520, 24)
        for i, (p, kw, name) in enumerate(poses):
            n.star(k, 170 + i * 300, y + 80, 1.55, p, "interested", (0.2, 0.0), wrap=False, **kw)
            lab(name, 80 + i * 300, y + 120, 18, 0)
        n.star_back(k, 170 + 7 * 300, y + 80, 1.55, step=0.2)
        lab("from behind (2.1)", 80 + 7 * 300, y + 120, 18, 0)
    n.HAND3[0] = n.NO_BAG[0] = n.HIDE3[0] = n.BACK2[0] = n.BACK3[0] = False
    rows, total = m.timing("A2")                                                              # three inserts, old over new
    shots = (("5.5", 1.0, "5.5 she points at the note"), ("5.6", 1.5, "5.6 she writes her number"), ("4.1a", 0.55, "4.1a the coin"), ("6.2c", 1.2, "6.2c the plan"))
    for r, on in enumerate((False, True)):
        m.V33[0] = on
        lab("BEFORE (v32)" if not on else "AFTER (v33): a forearm from the frame's edge, the hand on it", 40 + r * 1200, 1960, 24)
        for i, (sh, tl, name) in enumerate(shots):
            row = [x for x in rows if x["shot"] == sh][0]
            f = m.frame(row, tl, row["start"] + tl)
            c.save(); c.translate(40 + r * 1200 + i * 290, 1990); c.scale(0.5, 0.5); c.set_source_surface(f, 0, 0); c.paint(); c.restore()
            lab(name, 40 + r * 1200 + i * 290, 2490, 15, 0)
    sf.write_to_png(out); print("wrote", out)


if __name__ == "__main__":
    import sys
    (sheet2 if "v2" in sys.argv else sheet)(sys.argv[1] if len(sys.argv) > 1 else "/tmp/on2_hands_v1.png")
