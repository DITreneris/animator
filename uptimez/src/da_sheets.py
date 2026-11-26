"""The Double Agent (episode 15), stage 3: the character sheets the canon is missing (plan v2 §1, Tomas 26 Nov: "we need
the sheets, we need Father"). Drawn with the film's own rigs, so the sheets and the film always match. Nothing older
changes: this module only calls the rigs.
  python3 da_sheets.py father  -> ../the-double-agent/uptimez-father-v2-sheet.png  (v1 had no hands, no step, no feet-up)
  python3 da_sheets.py lineup  -> ../the-double-agent/uptimez-lineup-civil-war-v2.png (v2: Father x 0.94, Sofía charcoal)
The canon repo (DITreneris/uptimez characters/) gets them only when Tomas asks."""
import sys
import cairo
import numpy as np
import kit
from kit import Ctx
import don_ps
import pm_ps
import sofia_da
import client_ps as cps
import dh_cast as dc
import robot_ps

EP = "../the-double-agent/"
BG = (0.93, 0.89, 0.82)
INKT = (0.15, 0.15, 0.18)
F_S = 0.52 * 1.19 * 0.94               # Father's scale at the home line. v2 (character audit 26 Nov): x 0.94, so his hair
                                       # stays under Don's skull (it was 12 px above it at x 1.19; Don's curl hid it)


def _surf(w, h):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, w * 2, h * 2)
    c = cairo.Context(s); c.scale(2, 2); c.set_source_rgb(*BG); c.paint()
    return s, c, Ctx(c, 0)


def _t(c, x, y, txt, size=12, bold=0, col=INKT):
    c.select_font_face("Inter", 0, bold); c.set_font_size(size); c.set_source_rgb(*col); c.move_to(x, y); c.show_text(txt)


def _floor(c, x0, x1, y):
    c.set_source_rgb(0.45, 0.40, 0.34); c.set_line_width(1.4); c.move_to(x0, y); c.line_to(x1, y); c.stroke()


def _height(draw):
    """Ink height and width of one rig drawn alone (transparent surface)."""
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1000, 1000)
    draw(Ctx(cairo.Context(s), 0))
    a = np.frombuffer(s.get_data(), np.uint8).reshape(1000, s.get_stride() // 4, 4)[:, :1000, 3]
    ys, xs = np.where(a > 20)
    return ys.max() - ys.min(), xs.max() - xs.min()


def _tag(k, x, y, s, seed=4600):
    """REVIEW · TOMORROW, the throne's second tag (the $49,999 ticket's shape), hanging from a pinch at (x, y)."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    c.set_source_rgb(0.93, 0.76, 0.28); c.set_line_width(3)
    c.move_to(0, 0); c.line_to(0, 22); c.stroke()
    kit.cut(k, [(-48, 22), (48, 22), (48, 64), (-48, 64)], (0.99, 0.97, 0.90), lw=2.4)      # v4: wider ("TOMORROW" touched the edge)
    c.select_font_face(kit.FONT); c.set_font_size(13); c.set_source_rgb(0.72, 0.08, 0.12)
    for txt, yy in (("REVIEW", 40), ("TOMORROW", 57)):
        e = c.text_extents(txt); c.move_to(-e.x_advance / 2, yy); c.show_text(txt)
    c.restore()


def _arrow(c, x0, y0, x1, y1):
    c.set_source_rgb(*INKT); c.set_line_width(2); c.move_to(x0, y0); c.line_to(x1, y1); c.stroke()
    import math
    a = math.atan2(y1 - y0, x1 - x0)
    for da in (2.6, -2.6):
        c.move_to(x1, y1); c.line_to(x1 + 10 * math.cos(a + da), y1 + 10 * math.sin(a + da)); c.stroke()


def _black_shoe(k, x, y, s, ang, seed):
    """dh_poses._shoe (Daddy's Home, approved: the sole towards us, three treads), in Father's black, a grey rim."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    kit.cut(k, [(-9, -15), (9, -15), (12, 12), (-12, 12)], (0.06, 0.06, 0.07), shadow=False, lw=2)
    c.set_source_rgb(0.46, 0.46, 0.52); c.set_line_width(1.6)
    for yy in (-6, 0, 6):
        c.move_to(-8, yy); c.line_to(8, yy); c.stroke()
    c.restore()


def feet_up(k, x, seat_y, s, desk_x, seed=4700):
    """2.2, v3 (audit: "the thigh grows out of the side, the knee too angular, the shoe a disc"): REUSED from
    dh_poses.don_seated (Daddy's Home, approved): leaning back in the chair, both legs out to screen right, nearly level,
    the ankles crossed on the desk, the soles towards us. Father's black trousers; under the top heel the gold photo
    lying face down (its gold frame and its stand up)."""
    import dh_poses as dq
    c = k.c
    desk_top = seat_y - 78 * s
    kit.rect(k, desk_x, desk_top, 240 * s, 170 * s, (0.56, 0.39, 0.24), seed, lw=2.2)                       # the desk
    kit.rect(k, desk_x, desk_top, 240 * s, 14 * s, (0.76, 0.58, 0.40), seed + 1, shadow=False, lw=2.2)
    c.save(); c.translate(x, seat_y); c.rotate(-0.06)                                                       # the chair, tipped back
    kit.rect(k, -66 * s, -200 * s, 132 * s, 200 * s, (0.22, 0.16, 0.13), seed + 2, lw=2.2)
    c.restore()
    feet = seat_y - dq.WAIST * s
    c.save(); c.translate(x, seat_y); c.rotate(-0.08); c.translate(-x, -seat_y)                              # he leans back
    c.save(); c.rectangle(x - 200 * s, seat_y - 400 * s, 400 * s, 400 * s + 2); c.clip()
    import hands_ps as hp
    hp.reset("quiet", "quiet")
    o = dc.father(k, x, feet, s, pose=(-34, 30, 34, -30), look=(0.6, 0.2))
    c.restore(); c.restore()
    kit.rect(k, x - 72 * s, seat_y - 4 * s, 144 * s, 24 * s, (0.22, 0.16, 0.13), seed + 3, lw=2.2)          # the seat front
    # the photo, face down on the desk: a gold frame seen edge-on, its stand sticking up
    px = desk_x + 96 * s
    kit.rect(k, px - 40 * s, desk_top - 9 * s, 80 * s, 9 * s, (0.88, 0.70, 0.22), seed + 5, shadow=False, lw=1.8)
    c.set_source_rgb(0.30, 0.22, 0.10); c.set_line_width(3 * s); c.move_to(px + 18 * s, desk_top - 9 * s); c.line_to(px + 34 * s, desk_top - 34 * s); c.stroke()
    # the legs (dh_poses' line, in black): hip -> knee -> ankle, the ankles crossed on the photo
    c.save(); c.translate(x, seat_y); c.scale(s, s)
    ax = (px - x) / s
    ay = (desk_top - seat_y) / s - 14
    for pts, sd in (([(14, -8), (ax * 0.48, ay * 0.80 - 18), (ax - 6, ay - 4)], 1), ([(-10, -8), (ax * 0.45, ay * 0.55 - 10), (ax + 8, ay + 8)], 2)):
        for (a_x, a_y), (b_x, b_y) in zip(pts, pts[1:]):
            import math
            an = math.atan2(b_y - a_y, b_x - a_x); nx, ny = -math.sin(an) * 15, math.cos(an) * 15
            kit.cut(k, [(a_x + nx, a_y + ny), (b_x + nx, b_y + ny), (b_x - nx, b_y - ny), (a_x - nx, a_y - ny)], dc.BLACK, shadow=False, lw=2)
        kx, ky = pts[1]
        kit.ellipse(k, kx, ky, 15, 15, dc.BLACK, seed + 10 + sd, shadow=False, lw=2)
        c.set_source_rgb(0.30, 0.30, 0.34); c.set_line_width(2.2)                                         # the crease, lighter
        c.move_to(pts[0][0] + 6, pts[0][1] - 4); c.line_to(kx, ky - 6); c.line_to(pts[2][0] - 8, pts[2][1] - 6); c.stroke()
    c.restore()
    _black_shoe(k, px - 2 * s, desk_top - 30 * s, 2.0 * s, 0.30, seed + 20)
    _black_shoe(k, px + 16 * s, desk_top - 8 * s, 2.0 * s, 0.18, seed + 21)
    return o


import contextlib


@contextlib.contextmanager
def two_sleeves():
    """v3 (audit: "the sleeves merge into one band; which is on top?"): the first arm drawn (under) in the dark velvet,
    the second (over) in the light velvet, so the two forearms separate by value."""
    orig = kit.arm
    n = [0]
    def arm(k_, sx, sy, a1, a2, col, *a, **kw):
        if col == dc.VELVET:
            col = dc.VELVET_D if n[0] == 0 else dc.VELVET_L
            n[0] += 1
        return orig(k_, sx, sy, a1, a2, col, *a, **kw)
    kit.arm = arm
    try:
        yield
    finally:
        kit.arm = orig


@contextlib.contextmanager
def dark_sleeves():
    """His sleeves in the jacket's dark velvet (dh_cast.VELVET_D), so an arm across the jacket reads (audit: the folded
    arms read as holding the lapels: the sleeve was the jacket's own colour)."""
    orig = kit.arm
    kit.arm = lambda k_, sx, sy, a1, a2, col, *a, **kw: orig(k_, sx, sy, a1, a2, dc.VELVET_D if col == dc.VELVET else col, *a, **kw)
    try:
        yield
    finally:
        kit.arm = orig


def _legs(k, pts, wid, col):
    import math
    c = k.c
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        an = math.atan2(by - ay, bx - ax); nx, ny = -math.sin(an) * wid / 2, math.cos(an) * wid / 2
        kit.cut(k, [(ax + nx, ay + ny), (bx + nx, by + ny), (bx - nx, by - ny), (ax - nx, ay - ny)], col, shadow=False, lw=2)
        c.new_path(); c.arc(bx, by, wid / 2 - 1, 0, 6.3); c.set_source_rgb(*col); c.fill()


def walk(k, x, feet, s, stride=1.0):
    """1.3 mid-step: the rig clipped at the jacket's hem, the two legs drawn here (FATHER_STEP showed the velvet body
    between the legs). The back leg straight, the front knee bent, the front heel down."""
    c = k.c
    waist = feet + (-300 * 1.12 + 78 + 158 + 3) * s                       # v3: the pelvis 3 lower mid-step
    c.save(); c.rectangle(-5000, -5000, 10000, 5000 + waist); c.clip()
    dc.father(k, x, feet, s, pose=(-22, 8, 20, -8), look=(1, 0))
    c.restore()
    w = 42 * s
    _legs(k, [(x - 14 * s, waist - 4), (x - 34 * s, feet - 72 * s), (x - 54 * stride * s, feet - 14 * s)], w, dc.BLACK)   # back leg: pushing off
    _legs(k, [(x + 14 * s, waist - 4), (x + 30 * s, feet - 78 * s), (x + 46 * stride * s, feet - 10 * s)], w, dc.BLACK)   # front leg: the weight, knee soft
    for fx, rot in ((x - 58 * stride * s, 0.45), (x + 56 * stride * s, 0.0)):                                         # back heel up, front flat
        c.save(); c.translate(fx, feet - 6 * s); c.rotate(rot)
        kit.ellipse(k, 0, 0, 26 * s, 9 * s, (0.06, 0.06, 0.07), 4810, shadow=False, lw=2)
        c.set_source_rgb(0.46, 0.46, 0.52); c.set_line_width(2.0); c.move_to(-22 * s, -7 * s); c.line_to(22 * s, -7 * s); c.stroke()
        c.restore()


def seated_rest(k, x, seat_y, s, look=(0.4, 0.2), seed=4950):
    """8.1, v4: in Don's chair (the dark leather), leaning back, the ring hand (screen right) resting on the armrest, the
    other flat on his belly. The body is the rig clipped at the seat (da_s8.seated); a desk edge covers the lap."""
    import hands_ps as hp
    from cand_bc import ik
    c = k.c
    LEATHER = (0.22, 0.16, 0.13)
    c.save(); c.translate(x, seat_y); c.rotate(-0.06)
    kit.rect(k, -70 * s, -230 * s, 140 * s, 230 * s, LEATHER, seed, lw=2.2)                              # the chair's back
    c.restore()
    bt = -300 * 1.12 + 78
    feet = seat_y - (bt + 150) * s
    rest = ik(-40, bt + 14, 4, bt + 112, 48, 48, -1) + ik(40, bt + 14, 80, bt + 146, 48, 48, 1)
    hp.reset("quiet", "quiet")
    c.save(); c.translate(x, seat_y); c.rotate(-0.06); c.translate(-x, -seat_y)
    c.save(); c.rectangle(-5000, -5000, 10000, 5000 + seat_y); c.clip()
    for p_ in (0, 1):                                          # pass 0 finds the ring hand; the armrest goes under it
        if p_ == 0:
            c.push_group()
        hp.reset("quiet", "quiet")
        with dark_sleeves():
            o = dc.father(k, x, feet, s, pose=rest, look=look)
        if p_ == 0:
            c.pop_group()
            hx, hy = o["hands"][1]
            kit.rect(k, hx - 24 * s, hy + 7 * s, 50 * s, 13 * s, (0.30, 0.22, 0.17), seed + 1, lw=2)
    c.restore(); c.restore()
    kit.rect(k, x - 100 * s, seat_y - 6 * s, 200 * s, 40 * s, (0.56, 0.39, 0.24), seed + 2, lw=2.2)        # the desk's near edge
    return o


def father(out=EP + "uptimez-father-v5-sheet.png"):
    import hands_ps as hp
    import hands_v4
    from cand_bc import ik
    W, H = 1080, 1500
    s, c, k = _surf(W, H)
    dc.FATHER_HEM[0] = True
    hands_v4.enable()
    kit.HAND[0] = hp.hand
    try:
        _t(c, 30, 46, "FATHER · the investor", 26, 1)
        _t(c, 30, 70, "UptimeZ Inc. · character sheet v5 · the first sheet (12 on) · dh_cast.father · episode 15 jobs", 12)
        _t(c, 30, 88, "v3 (Father v2 audit): feet up reused from Daddy's Home (dh_poses.don_seated); the folded forearms dark under,"
           " light over, a fist with the ring; the tag from the fingertips;", 11)
        _t(c, 30, 120, "v5 (hands canon): every rest hand quiet (no legacy relax); the tag drawn first, the pinch again on top of it"
           " (redraw_at); the tag arm's elbow bent 30.", 11)
        _t(c, 30, 104, "a step with the weight on a soft front knee; the nod a 6-degree head tip (FATHER_NOD, opt-in); seams and shine"
           " (FATHER_HEM, opt-in). He hardly moves.", 11)
        F = 430
        _t(c, 30, 140, "1  SERIES SCALE", 13, 1)
        _floor(c, 30, W - 30, F)
        hp.reset("quiet", "quiet"); don_ps.don(k, 120, F, 0.60); _t(c, 92, F + 20, "Don 0.60", 11)
        hp.reset("quiet", "quiet"); dc.father(k, 260, F, F_S); _t(c, 220, F + 20, "Father %.2f" % F_S, 11)
        hp.reset("quiet", "quiet"); cps.client(k, 410, F, 0.52); _t(c, 380, F + 20, "Client 0.52", 11)
        (dh, dw), (fh, fw) = _height(lambda kk: don_ps.don(kk, 500, 800, 0.60)), _height(lambda kk: dc.father(kk, 500, 800, F_S))
        _t(c, 560, 230, "Height Father / Don = %.2f with Don's curl; his hair 2 px under Don's skull" % (fh / dh), 13, 1)
        _t(c, 560, 250, "Width  Father / Don = %.2f" % (fw / dw), 13, 1)
        _t(c, 560, 276, "Don stays the tallest and widest (Tomas's rule kept).", 11)
        _t(c, 560, 292, "The Client: the canon's exception, never on Don's floor line.", 11)
        # 2. jobs
        y2 = 480
        _t(c, 30, y2, "2  EPISODE 15 JOBS (hands: hands_v4 grab / pinch / fist, the job named under each)", 13, 1)
        F2 = y2 + 330
        _floor(c, 30, W - 30, F2)
        S2 = 0.70
        hp.reset("quiet", "quiet")
        walk(k, 110, F2, S2)
        _t(c, 50, F2 + 22, "1.3 over the tape: mid-step", 11)
        hp.reset("quiet", "pinch")                     # v5 (hands canon): the elbow bent 30 (under 20 is a pole); the
        o = dc.father(k, 330, F2, S2, pose=(-8, 0, 100, 34), look=(0.8, -0.3))      # tag drawn first, the pinch again on top
        import math
        hx, hy = o["hands"][1]; a_ = math.radians(100 + 34)
        _tag(k, hx + math.sin(a_) * 11 * S2, hy + math.cos(a_) * 11 * S2 + 3 * S2, S2)
        hp.redraw_at(k, hx, hy)
        _t(c, 250, F2 + 22, "1.3 hangs the tag: pinch", 11)
        bt = -300 * 1.12 + 78
        # v4 (cold test: the fold misread 3 times, "checking a watch" 2/2; Tomas: change the gesture): seated in Don's chair,
        # leaning back, the ring hand resting on the armrest, the other flat on his belly
        seated_rest(k, 560, F2 - 40, S2)
        _t(c, 470, F2 + 22, "8.1 leaning back, ring hand on the armrest", 11)
        hp.reset("quiet", "quiet"); dc.father(k, 760, F2, S2, look=(0, 0))
        hp.reset("quiet", "quiet"); dc.FATHER_NOD[0] = 6.0
        dc.father(k, 930, F2, S2, face="hard", look=(0, 1.0)); dc.FATHER_NOD[0] = 0.0
        _arrow(c, 812, F2 - 236, 880, F2 - 214)
        _t(c, 740, F2 + 22, "7.3 the nod (a still cannot carry it: motion test)", 11)
        # 3. feet up
        y3 = F2 + 70
        _t(c, 30, y3, "3  2.2: IN DON'S CHAIR, FEET ON THE DESK, THE HEEL ON THE PHOTO (reused: dh_poses.don_seated; silhouette right)", 13, 1)
        hp.reset("quiet", "quiet")
        feet_up(k, 170, y3 + 250, 0.70, 250)
        sil = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1080 * 2, 1500 * 2)
        cs = cairo.Context(sil); cs.scale(2, 2); hp.reset("quiet", "quiet"); feet_up(Ctx(cs, 0), 170, y3 + 250, 0.70, 250)
        c.save(); c.scale(0.5, 0.5)
        c.set_source_rgb(0.12, 0.12, 0.14); c.mask_surface(sil, 1040, 0); c.restore()
        _t(c, 560, y3 + 400, "the silhouette: the knee and the raised shoe must read alone", 11)
        # 4. acting
        y4 = y3 + 440
        _t(c, 30, y4, "4  ACTING: economy of movement (the audit's five; his only moves)", 13, 1)
        for i, line in enumerate(("a slow head turn, the body still", "one brow up (face \"brow\")", "the ring turned on the finger",
                                  "a deliberate lean back in the chair", "a long look, the face unchanged")):
            _t(c, 40, y4 + 22 + i * 17, "· " + line, 11)
    finally:
        dc.FATHER_HEM[0] = False; dc.FATHER_STEP[0] = None
        hands_v4.disable(); kit.HAND[0] = None
    s.write_to_png(out)
    print("wrote", out)


def lineup(out=EP + "uptimez-lineup-civil-war-v3.png"):
    W, H = 1500, 760
    s, c, k = _surf(W, H)
    _t(c, 30, 46, "THE CIVIL WAR CAST · height line-up v3", 26, 1)
    _t(c, 30, 70, "UptimeZ Inc. · episodes 13-17 · the film's own rigs at front desk v4 home scales (= the canon 16:9 sheets'"
       " scales) · one floor line", 12)
    F = 600
    _floor(c, 30, W - 30, F)
    don = lambda kk, x=500, f=800: don_ps.don(kk, x, f, 0.60)
    cast = [("DON", "don_ps 0.60", don),
            ("PAM", "pm_ps 0.50", lambda kk, x=500, f=800: pm_ps.pam(kk, x, f, 0.50, mug=False)),
            ("MOM", "pm_ps 0.50", lambda kk, x=500, f=800: pm_ps.mom(kk, x, f, 0.50)),
            ("SOFÍA", "sofia_da 0.47 (15)", lambda kk, x=500, f=800: sofia_da.sofia(kk, x, f, 0.47, pose="stand", tablet_kind="none")),
            ("FATHER", "dh_cast %.2f" % F_S, lambda kk, x=500, f=800: dc.father(kk, x, f, F_S)),
            ("THE CLIENT", "client_ps 0.52", lambda kk, x=500, f=800: cps.client(kk, x, f, 0.52)),
            ("THE ROBOT", "robot_ps 0.48", lambda kk, x=500, f=800: robot_ps.robot(kk, x, f, 0.48))]
    dh, dw = _height(don)
    import hands_ps as hp
    import hands_v4 as hv
    hv.enable(); kit.HAND[0] = hp.hand                            # v3: the canon hand (quiet at rest) for every rig that takes it
    for i, (name, rig, draw) in enumerate(cast):
        x = 110 + i * 205
        hp.reset("quiet", "quiet")
        draw(k, x, F)
        h, w = _height(draw)
        bad = name != "DON" and (h > dh or w > dw)
        _t(c, x - 60, F + 26, name, 14, 1)
        _t(c, x - 60, F + 44, rig, 11)
        _t(c, x - 60, F + 62, "h %.2f · w %.2f of Don" % (h / dh, w / dw), 11, 1, (0.75, 0.15, 0.12) if bad else INKT)
    hv.disable(); kit.HAND[0] = None
    _t(c, 30, F + 110, "Rules: Don is the tallest and widest in any frame he shares. The Client breaks it (the canon's own sheet draws him at 1.03):"
       " staging rule, never on Don's floor line.", 12)
    _t(c, 30, F + 128, "Episode looks: Sofía the job-interview suit (15, the next day); the Client in his garage overalls (13 on);"
       " Pam's mustard mug from 15 (Don's gift).", 12)
    s.write_to_png(out)
    print("wrote", out)


if __name__ == "__main__":
    {"father": father, "lineup": lineup}[sys.argv[1]]()
