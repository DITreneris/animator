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

import da_arms
da_arms.setup()                                              # Tomas 26 Nov: no two left hands (thumbs inward on hanging arms)

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


def father(out=EP + "uptimez-father-v6-sheet.png"):
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
        _t(c, 30, 70, "UptimeZ Inc. · character sheet v6 · the first sheet (12 on) · dh_cast.father · episode 15 jobs", 12)
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


def lineup(out=EP + "uptimez-lineup-civil-war-v4.png"):
    W, H = 1500, 760
    s, c, k = _surf(W, H)
    _t(c, 30, 46, "THE CIVIL WAR CAST · height line-up v4", 26, 1)
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



# ---- Don and Pam, episode 15 (Tomas 26 Nov, /grill-me: the sheets, then S8r, then the hand check) ----------------------

MUSTARD = (0.86, 0.66, 0.16)                                 # da_set.MUG
PAM_CANON = dict(lips="rose", brooch=False)                  # the office canon (pam-ss-v2, pam-mf-v2, pam-xmas-v4): dusty rose, no
                                                             # brooch. pm_ps's defaults (berry, the flower) are episode 8's touches
GOLD_BOW = (0.93, 0.74, 0.22)


def gift_mug(k, x, y, s, bow=True, col=MUSTARD, seed=5600):
    """Pam's new mug (Don's gift, 2.4): the series mug shape (pm_ps.mug_at), mustard, a gold bow on its handle."""
    import pm_ps
    old = pm_ps.MUG; pm_ps.MUG = col
    try:
        pm_ps.mug_at(k, x, y, s)
    finally:
        pm_ps.MUG = old
    if bow:
        c = k.c
        c.save(); c.translate(x, y - 24 * s); c.scale(s, s)                                   # the bow on the rim, to us
        for sx in (-1, 1):
            kit.cut(k, [(0, 0), (sx * 14, -9), (sx * 14, 9)], GOLD_BOW, shadow=False, lw=1.8)
        kit.ellipse(k, 0, 0, 4, 4, GOLD_BOW, seed, shadow=False, lw=1.6)
        c.restore()


def _shards(k, x, y, s, col=(0.36, 0.62, 0.80), seed=5650):
    import random
    r = random.Random(seed)
    for i in range(6):
        a = r.uniform(0, 6.28); d_ = r.uniform(8, 34) * s
        px, py = x + d_ * 1.6 * (1 if i % 2 else -1) * abs(math.cos(a)), y - r.uniform(0, 5) * s
        k.c.save(); k.c.translate(px, py); k.c.rotate(r.uniform(-1, 1))
        kit.cut(k, [(-7 * s, 0), (6 * s, -5 * s), (8 * s, 2 * s)], col, shadow=False, lw=1.6)
        k.c.restore()


import math  # noqa: E402  (used by the episode sheets below)


def don_sheet(out=EP + "uptimez-don-da-v2-sheet.png"):
    """Don's beats in 15, canon hands (hands_v4: grab, pinch, fist; quiet at rest), tapered arms (da_arms, opt-in)."""
    import hands_ps as hp
    import hands_v4 as hv
    import da_arms
    from cand_bc import ik
    W, H = 1500, 1020
    s, c, k = _surf(W, H)
    _t(c, 30, 46, "DON · The Double Agent (15) · his beats · v2", 26, 1)
    _t(c, 30, 70, "Cold test F1 (the establishing frame: Don read as a robot 0/3): a readable human face in every beat. Canon hands"
       " (hands_v4 grab / pinch / fist, quiet at rest); tapered arms (da_arms, opt-in).", 11)
    F, S = 470, 0.95
    _floor(c, 30, W - 30, F)
    bt = -300 * 1.12 + 78
    hv.enable()
    try:
        with da_arms.tapered():
            x = 110                                                                   # 2.3 offended, the vest straightened
            don_ps.don(k, x, F, S, (-36, 150, 36, -150), "squint", look=(0, -0.3), chin=1, hands=("fist", "fist"))
            _t(c, x - 70, F + 22, "2.3 offended: the vest, chin up", 11)
            x = 330                                                                   # 2.4 the gift: the mug held out
            o = don_ps.don(k, x, F, S, (-8, 0) + ik(40, bt + 14, 104, bt + 70, 48, 48, 1), "happy", look=(1, 0),
                           hands=("quiet", "grab"))
            hx, hy = o["hands"][1]
            gift_mug(k, hx + 16 * S, hy + 2 * S, S * 0.9); hp.redraw_at(k, hx, hy)
            _t(c, x - 60, F + 22, "2.4 the gift: grab, the bow", 11)
            x = 560                                                                   # 6.4 suspicion -> delight
            don_ps.don(k, x - 50, F, S * 0.8, "stand", "squint", look=(1, 0), hands=("quiet", "quiet"))
            don_ps.don(k, x + 60, F, S * 0.8, "stand", "grin", look=(1, 0), hands=("quiet", "quiet"))
            _arrow(c, x - 10, F - 240, x + 30, F - 230)
            _t(c, x - 110, F + 22, "6.4 suspicion -> delight", 11)
            x = 790                                                                   # 6.8 the whisper into the mic
            o = don_ps.don(k, x, F, S, (-8, 0) + ik(40, bt + 14, 30, bt - 40, 48, 48, 1), "squint", look=(-1, 0),
                           hands=("quiet", "pinch"))
            _t(c, x - 70, F + 22, "6.8 the mic to his mouth: pinch", 11)
            x = 1020                                                                  # 7.2 "Approved." the strip held high
            o = don_ps.don(k, x, F, S, (-50, -40) + ik(40, bt + 14, 70, bt - 110, 48, 48, 1), "happy", look=(-1, 0), chin=1,
                           hands=("palm", "grab"))
            hx, hy = o["hands"][1]
            c.save(); c.translate(hx, hy); kit.cut(k, [(-6, 0), (6, 0), (12, 120), (0, 124)], (0.95, 0.78, 0.15), shadow=False, lw=2); c.restore()
            hp.redraw_at(k, hx, hy)
            _t(c, x - 60, F + 22, "7.2 \"Approved.\": the strip, grab", 11)
            x = 1270                                                                  # 7.4 the dive for the armrest
            don_ps.don(k, x, F, S, (60, 30, 100, -30), "panic", look=(1, 0), lean=0.22, hands=("grab", "grab"))
            _t(c, x - 70, F + 22, "7.4 the dive: grab, grab", 11)
        # the new job
        y2 = F + 90
        _t(c, 30, y2, "NEW JOB, NOT IN THE CANON TABLE (rules-hands 0.2: three silhouettes, two cold viewers, the row first):", 13, 1)
        _t(c, 30, y2 + 20, "5.2 the saucer sip with the little finger up (cup and saucer in two hands, one finger raised). Not drawn"
           " until the row exists.", 12)
        _t(c, 30, y2 + 50, "Watch (rules-hands, Gestures): 6.8's hand at the cheek reads as a phone call. Here that is the joke"
           " (spy comms into his own headset); keep it, check it cold.", 12)
    finally:
        hv.disable()
    s.write_to_png(out)
    print("wrote", out)


def pam_sheet(out=EP + "uptimez-pam-da-v3-sheet.png"):
    """Pam's beats in 15: Don's gift (the mustard mug, the blue one shattered), the open and the closed mouth, the
    lean-in, the duck. Canon hands: the mug in a grab (not the legacy "cup"), quiet at rest."""
    import hands_ps as hp
    import hands_v4 as hv
    import pm_ps
    import pam_mf as pmf
    W, H = 1500, 900
    s, c, k = _surf(W, H)
    _t(c, 30, 46, "PAM · The Double Agent (15) · her beats · v3", 26, 1)
    _t(c, 30, 70, "Her mug is now Don's gift: mustard, a gold bow in 2.4 and 3.2 (off from 3.3); the blue mug of 12-14 shatters in 2.4."
       " Canon hands: grab for a held mug, quiet at rest.", 11)
    _t(c, 30, 88, "v2 (Tomas: to the canon): dusty-rose lips, no brooch (the office canon: pam-ss-v2, pam-mf-v2, pam-xmas-v4);"
       " the closed hold is \"pressed\" (thin lips, an ink line).", 11)
    F, S = 470, 1.0
    _floor(c, 30, W - 30, F)
    PB = pmf.BT
    extra = {"_mug": (-8, 0) + pmf.ik(1, 40, PB + 70), "_drop": pmf.ik(-1, -60, PB + 40) + pmf.ik(1, 60, PB + 40),
             "_rest": (-8, 0, 8, 0)}
    hands = {"_mug": ("quiet", "grab"), "_drop": ("palm", "palm"), "_rest": ("quiet", "quiet")}
    pm_ps.P_POSES.update(extra); pm_ps.P_HANDS.update(hands)
    hv.enable()
    try:
        x = 110                                                                       # 2.4 she takes the gift
        o = pm_ps.pam(k, x, F, S, "_mug", "hopeful", look=(-1, 0), mug=False, **PAM_CANON)
        hx, hy = o["hands"][1]; gift_mug(k, hx + 12 * S, hy + 4 * S, S); hp.redraw_at(k, hx, hy)
        _t(c, x - 60, F + 22, "2.4 Don's gift: grab, the bow", 11)
        x = 330                                                                       # 2.4 the blue mug drops and shatters
        pm_ps.pam(k, x, F, S, "_drop", "peer", look=(0, 1), mug=False, mouth="O", **PAM_CANON)
        pm_ps.mug_at(k, x + 40, F - 120, S, tilt=0.6)
        _shards(k, x, F - 2, S)
        _t(c, x - 70, F + 22, "2.4 the old blue mug falls, shatters", 11)
        x = 560
        pm_ps.pam(k, x, F, S, "_rest", "doubt", look=(-1, 0), mug=False, mouth="O", **PAM_CANON)
        _t(c, x - 70, F + 22, "6.5 opens her mouth to correct him", 11)
        x = 780
        pm_ps.pam(k, x, F, S, "_rest", "pressed", look=(-1, 0), mug=False, **PAM_CANON)
        _t(c, x - 70, F + 22, "6.7 closes it: pressed (held 0.6 s)", 11)
        x = 1000
        c.save(); c.translate(x, F); c.rotate(-0.16); c.translate(-x, -F)              # the lean, about her feet
        pm_ps.pam(k, x, F, S, "_rest", "peer", look=(-1, 0), mug=False, **PAM_CANON); c.restore()
        _t(c, x - 60, F + 22, "6.8 leans in to hear", 11)
        x = 1230
        c.save(); c.translate(x, F); c.rotate(0.42); c.translate(-x, -F)
        pm_ps.pam(k, x, F, S, "_rest", "quiet", look=(1, 0.4), mug=False, **PAM_CANON); c.restore()
        _t(c, x - 60, F + 22, "7.2 ducks under the strip", 11)
        _t(c, 30, F + 80, "Not on this sheet: her hands on the plan (7.3, 8.1) are the locked S8's palms; the mug carried with Don's cup and"
           " saucer (3.2-3.3) is a two-prop carry to test cold at stage 4.", 12)
    finally:
        hv.disable()
        for kk in extra:
            pm_ps.P_POSES.pop(kk, None); pm_ps.P_HANDS.pop(kk, None)
    s.write_to_png(out)
    print("wrote", out)


def client_sheet(out=EP + "uptimez-client-da-v1-sheet.png"):
    """The Client in 15 (Tomas 28 Nov, /grill-me): the canon's garage owner, oil in the creases only (client_ps.CLEAN):
    washed hands with dark crease lines, a clean white T-shirt, the red rag clean on his shoulder, no grease on his face.
    Episode 14's filthy booth look stays in 14. His beats here: bored in Don's office, at the door for Pam's mug (3.3),
    pointing (the plan, 7.3), and the hands up close against 14's."""
    import client_ps as cp
    W, H = 1500, 1000
    s, c, k = _surf(W, H)
    _t(c, 30, 46, "THE CLIENT · The Double Agent (15) · v1", 26, 1)
    _t(c, 30, 70, "Owner of ten garages, not a mechanic under a car: canon client_ob (\"oil in the creases of his hands\"). Episode 14's"
       " filthy booth look (black hands, palm print, cheek smear) stays in 14.", 11)
    _t(c, 30, 88, "client_ps.CLEAN (opt-in, default off: 14 byte-identical); da_set turns it on for this episode.", 11)
    F, S = 560, 0.60
    _floor(c, 30, W - 30, F)
    keep = cp.CLEAN[0]
    try:
        cp.CLEAN[0] = True
        cp.client(k, 150, F, S, pose="open", face="bored", look=(1, 0))
        _t(c, 70, F + 22, "office: bored, arms open", 11)
        x = 420                                                                          # IK arms (of_cast), as the shots draw him
        cp.cast_client(k, x, F, S, look=(-1, 0), face="bored", targets=[(x - 130, F - 230), (x + 40, F - 150)],
                       hands={-1: "fist", 1: "fist"})
        kit.ellipse(k, x - 146, F - 226, 14, 16, (0.83, 0.62, 0.16), 4890, lw=2)        # her mug in his hand
        _t(c, x - 80, F + 22, "3.3 at the door: takes her mug", 11)
        x = 720
        cp.cast_client(k, x, F, S, look=(1, 0.6), face="bored", targets=[(x - 70, F - 120), (x + 150, F - 210)],
                       hands={-1: "fist", 1: "point"}, aim=(x + 260, F - 180))
        _t(c, x - 60, F + 22, "7.3 \"Don't lose it.\": points at the plan", 11)
        x = 1000
        cp.cast_client(k, x, F, S, look=(1, 0.4), face="confident", targets=[(x - 100, F - 190), (x + 100, F - 190)],
                       hands={-1: "palm", 1: "palm"})
        _t(c, x - 90, F + 22, "open palms: the plan's hand-over (the plan is the shot's)", 11)
        for i, (clean, cap) in enumerate(((True, "15: washed, oil in the creases"), (False, "14: the booth (not used here)"))):
            cp.CLEAN[0] = clean
            x = 1230 + i * 150
            c.save(); c.translate(x, 200); c.scale(2.2, 2.2)
            cp._STYLE["now"] = "fist"
            cp.hand(k, 0, 0, 22, cp.co.SKIN if clean else cp.OIL, 4801, (1, 0.2), 1)
            c.restore()
            _t(c, x - 70, 260, cap, 10)
        cp.CLEAN[0] = True
        _t(c, 1160, 140, "the hand, close", 13, 1)
        F2, S2 = 900, 0.30                                                               # the phone check: feed size
        _floor(c, 30, 700, F2)
        for x in (90, 260, 430):
            cp.client(k, x, F2, S2, pose="open", face="bored", look=(1, 0))
        _t(c, 30, F2 + 22, "feed size: no dark blobs to read as gloves or a stain", 11)
    finally:
        cp.CLEAN[0] = keep
    s.write_to_png(out)
    print("wrote", out)


def mom_sheet(out=EP + "uptimez-mom-da-v1-sheet.png"):
    """Mom in 15 (Tomas 28 Nov, /grill-me): the series' Mom (mom_fs: teal suit, the curler stays), her fists on her hips
    and her folded arms in the hand library (da_layouts.MOM_LIB), a smaller rosette (mom_fs.ORDER_S 0.7). Her beats here:
    up from her desk (3.3), the door she slides in front of (3.4, "Your rule, sweetheart."), sitting back, folded (4.1)."""
    import da_layouts as L
    import don_ps
    import hands_v4 as hv
    W, H = 1500, 980
    s, c, k = _surf(W, H)
    _t(c, 30, 46, "MOM · The Double Agent (15) · v1", 26, 1)
    _t(c, 30, 70, "The series' Mom (mom_fs): teal suit, mustard lapels, the curler stays. v1: her fists on her hips and her folded"
       " arms in the episode's hand library; the rosette smaller (0.7 of 1.15).", 11)
    _t(c, 30, 88, "Opt-in: da_layouts.MOM_LIB, mom_fs.ORDER_S, mom_bc.TUPLE_NAME (defaults draw as before, md5-checked).", 11)
    F = 520
    _floor(c, 20, W - 20, F)
    hv.enable()
    with L.ds.no_badges():                                     # (this episode: no name badges on people)
        don_ps.don(k, 110, F, 0.60 * 1.25)
    sc = 1.25
    keep = L.SC["mom"]; L.SC["mom"] = keep * sc
    try:
        L.mom(k, (330, F), "fists", "glare", look=(1, 0))
        L.mom(k, (560, F), "fists", "unimpressed", look=(-1, 0.2), chin=True)
        L.mom(k, (790, F), "fists", "unimpressed", look=(-1, 0.2), chin=True, mouth="A")
        L.mom(k, (1020, F), "folded", "unimpressed", look=(-1, 0.2))
        L.MOM_LIB[0] = False
        L.mom(k, (1300, F), "fists", "glare", look=(1, 0))
        L.MOM_LIB[0] = True
    finally:
        L.SC["mom"] = keep
    for x, lab in ((110, "Don 0.60 (scale)"), (330, "fists on her hips, glare (3.3)"), (560, "the door: chin up (3.4)"),
                   (790, "\"Your rule, sweetheart.\" (A)"), (1020, "folded (4.1)"), (1300, "before: the round fists")):
        _t(c, x - 80, F + 24, lab, 11)
    y2 = F + 60
    _t(c, 30, y2, "UP CLOSE", 13, 1)
    for i, (pose, face, kw, lab) in enumerate((("fists", "glare", {}, "glare"), ("fists", "unimpressed", dict(chin=True), "unimpressed, chin up"),
                                               ("folded", "unimpressed", {}, "folded"))):
        x = 180 + i * 330
        c.save(); c.rectangle(x - 150, y2 + 14, 300, 300); c.clip()
        keep = L.SC["mom"]; L.SC["mom"] = 1.35
        try:
            L.mom(k, (x, y2 + 14 + 560), pose, face, look=(-0.6, 0.2), **kw)
        finally:
            L.SC["mom"] = keep
        c.restore()
        c.set_source_rgb(0.15, 0.15, 0.18); c.set_line_width(1); c.rectangle(x - 150, y2 + 14, 300, 300); c.stroke()
        _t(c, x - 145, y2 + 334, lab, 11)
    _t(c, 1080, y2, "AT PHONE SIZE", 13, 1)
    c.save(); c.translate(1100, y2 + 30); c.scale(0.5, 0.5)
    with L.ds.no_badges():
        don_ps.don(k, 80, 500, 0.60)
    L.mom(k, (230, 500), "fists", "glare"); L.mom(k, (380, 500), "folded", "unimpressed")
    c.restore()
    hv.disable()
    s.write_to_png(out)
    print("wrote", out)


def robot_sheet(out=EP + "uptimez-robot-da-v1-sheet.png"):
    """The robot in 15 (Tomas 28 Nov, /grill-me: a record, no changes): rp.robot with the canon's two hands (at rest,
    the gripper) solved by IK (da_anim_s1.robot_canon), the HR badge (the only badge in this episode), the red bow tie."""
    import da_layouts as L
    import da_anim_s1 as A
    import don_ps
    W, H = 1500, 900
    s, c, k = _surf(W, H)
    _t(c, 30, 46, "THE ROBOT · The Double Agent (15) · v1 (a record: no changes)", 26, 1)
    _t(c, 30, 70, "Canon hands (CANON.md): at rest and the gripper, the arms by two-bone IK for the shoulders the rig draws"
       " (da_anim_s1.robot_canon). The HR badge is the only badge in this episode; the red bow tie stays.", 11)
    F = 520
    _floor(c, 20, W - 20, F)
    with L.ds.no_badges():
        don_ps.don(k, 110, F, 0.60 * 1.25)
    keep = L.SC["robot"]; L.SC["robot"] = keep * 1.25; rs = L.SC["robot"]
    try:
        A.robot_canon(k, 330, F, {})
        A.robot_canon(k, 560, F, {1: ("grip", (560 + 46 * 1.25, F - 150 * rs))}, tilt=0.1, look=(-1, -0.4))
        A.robot_canon(k, 800, F, {-1: ("grip", (800 - 60 * 1.25, F - 60 * 1.25))}, tilt=-0.15, look=(-1, 0.6))
        A.robot_canon(k, 1040, F, {-1: ("grip", (1040 - 70 * 1.25, F - 150 * rs)), 1: ("grip", (1040 + 70 * 1.25, F - 150 * rs))},
                      look=(0, -0.6))
    finally:
        L.SC["robot"] = keep
    for x, lab in ((110, "Don 0.60 (scale)"), (330, "at rest"), (560, "gripper up, frozen (3.4)"), (800, "reaching out (1.4)"),
                   (1040, "both up: the throne (7.4)")):
        _t(c, x - 80, F + 24, lab, 11)
    y2 = F + 60
    _t(c, 30, y2, "UP CLOSE", 13, 1)
    c.save(); c.rectangle(30, y2 + 14, 420, 270); c.clip()
    keep = L.SC["robot"]; L.SC["robot"] = 1.4
    try:
        A.robot_canon(k, 240, y2 + 14 + 470, {1: ("grip", (240 + 46 * 2.9, y2 + 14 + 470 - 150 * 1.4))}, look=(-1, -0.2))
    finally:
        L.SC["robot"] = keep
    c.restore()
    c.set_source_rgb(0.15, 0.15, 0.18); c.set_line_width(1); c.rectangle(30, y2 + 14, 420, 270); c.stroke()
    _t(c, 520, y2, "AT PHONE SIZE", 13, 1)
    c.save(); c.translate(540, y2 + 30); c.scale(0.5, 0.5)
    with L.ds.no_badges():
        don_ps.don(k, 80, 500, 0.60)
    A.robot_canon(k, 230, 500, {})
    c.restore()
    s.write_to_png(out)
    print("wrote", out)


if __name__ == "__main__":
    {"father": father, "lineup": lineup, "don": don_sheet, "pam": pam_sheet, "client": client_sheet, "mom": mom_sheet, "robot": robot_sheet}[sys.argv[1]]()
