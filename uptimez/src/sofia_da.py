"""SOFÍA in "The Double Agent" (episode 15): the next day after 14, a new outfit. Tomas, 26 Nov: "a new outfit for
Sofía, it's another day"; /grill-me: **the job interview** (14 offered her the robot's HR job: she comes dressed for it).
Built like sofia_ps / sofia_dh: the same rig (sofia_ob), colours and parts swapped in and put back, so nothing older
changes.
- a navy fitted blazer with padded shoulders (sofia_dh's suit cut), a navy pencil skirt: the interview suit;
- a white blouse under it (the navy reads against the office wall and against Father's black and burgundy);
- pearls: the strand and pearl drops (sofia_ob's own, which sofia_ps switched off), not 14's gold shields;
- her hair pulled back sleek (sofia_ss.SLEEK, PULLED) into a high ponytail;
- black pumps (no gold heel: the heel was 14's story prop).
  o = sofia(k, x, feet, s, pose, face_kind, look, ...)      the same signature as sofia_ps.sofia
  python3 sofia_da.py [out]  ->  ../the-double-agent/da_sofia_v1.png (the look sheet)"""
import math
import sys
import cairo
import kit
import sofia_v4 as sf
import sofia_ss as ss
import sofia_bc as sbc
import sofia_ob as so
import sofia_cs as scs
import sofia_dh as sdh
import sofia_fs
from kit import Ctx, INK, cut, ellipse, rect

NAVY = (0.14, 0.19, 0.33)                                   # v1 (Don's vest is navy too: changed in v2)
NAVY_SHADE = (0.09, 0.12, 0.22)
CHARCOAL = (0.30, 0.31, 0.35)                               # v2 (character audit 26 Nov; Tomas: "whatever is better"): charcoal,
CHARCOAL_SHADE = (0.20, 0.21, 0.24)                         # apart from Don's navy vest and Father's black and burgundy
SUIT = [CHARCOAL, CHARCOAL_SHADE]
PEARL_BTN = (0.90, 0.89, 0.86)
WHITE = (0.98, 0.98, 0.96)
WHITE_SHADE = (0.84, 0.85, 0.86)
PONY = [True]                                               # the high ponytail (off: the sleek hair alone)


def ponytail(k, hy, seed, lgx=0.0, lgy=0.0):
    """The series' own high ponytail (sofia_fs.ponytail, episode 10's), drawn behind her head."""
    sofia_fs.ponytail(k, hy, lgx, lgy, seed)


def _interview_blazer(k, body_top, seed):
    """v2 (the character audit): sofia_dh's jacket cut, the shoulders 12 % narrower (an interview, not a uniform), no gold
    edge on the lapels and pearl buttons in place of gold (fewer small things competing at phone size)."""
    c = k.c
    bt = body_top
    col, sh = SUIT
    cut(k, [(-17, bt - 1), (17, bt - 1), (13, bt + 150), (-13, bt + 150)], WHITE, shadow=False, lw=1.6)          # the white blouse
    cut(k, [(0, bt + 40), (-11, bt - 2), (11, bt - 2)], sf.SKIN, shadow=False, lw=1.6)                          # the V
    for sx in (-1, 1):
        cut(k, [(sx * 22, bt - 9), (sx * 55, bt - 5), (sx * 59, bt + 18), (sx * 47, bt + 31), (sx * 33, bt + 28)],
            col, shadow=False, lw=2.2)                                                                       # the shoulder, 12 % in
        cut(k, [(sx * 38, bt - 1), (sx * 15, bt - 1), (sx * 8, bt + 60), (sx * 10, bt + 152), (sx * 42, bt + 150),
                (sx * 38, bt + 124), (sx * 26, bt + 88), (sx * 42, bt + 32)], col, shadow=False, lw=2.2)
        c.set_source_rgb(*sh); c.set_line_width(1.6); c.set_line_cap(1)
        c.move_to(sx * 29, bt + 40); c.curve_to(sx * 23, bt + 64, sx * 20, bt + 84, sx * 24, bt + 112); c.stroke()
        cut(k, [(sx * 15, bt - 1), (sx * 29, bt - 4), (sx * 23, bt + 42), (sx * 8, bt + 60)], col, shadow=False, lw=1.8)
    for yy in (bt + 82, bt + 104):
        ellipse(k, 11, yy, 4.2, 4.2, PEARL_BTN, seed + 48 + int(yy), shadow=False, lw=1.4)


HANDS = [("quiet", "quiet")]                                 # v3 (hands canon, 26 Nov): her two hands, through hands_ps
F_W = 15                                                       # the class sheet: female hand width 15 (male 17)


def _canon_arm(k, sx, sy, a1, a2, seed, ln=48, w=17):
    """sofia_v4._arm with the canon hand: the same sleeve and forearm, then hands_ps (the job's shape) in place of the
    ball and its red nail (the class sheet: one hand for the cast, no nail). A hand named None is not drawn: a
    board_two clutch is that hand."""
    import hands_ps as hp
    d = lambda a: (math.sin(math.radians(a)), math.cos(math.radians(a)))
    ex, ey = sx + d(a1)[0] * ln, sy + d(a1)[1] * ln
    hx, hy = ex + d(a1 + a2)[0] * ln, ey + d(a1 + a2)[1] * ln
    w = F_W
    for (ax, ay, bx, by), col in (((sx, sy, ex, ey), sf.BLOUSE), ((ex, ey, hx, hy), sf.SKIN)):
        ang = math.atan2(by - ay, bx - ax)
        wa = w + 2 if col is sf.BLOUSE else w - 1                 # the upper arm wider, the forearm narrower (rules: not a tube)
        nx, ny = -math.sin(ang) * wa / 2, math.cos(ang) * wa / 2
        cut(k, [(ax + nx, ay + ny), (bx + nx, by + ny), (bx - nx, by - ny), (ax - nx, ay - ny)], col, shadow=False, lw=2)
    side = 0 if sx < 0 else 1
    g = HANDS[0][side]
    if g is not None:
        hp.GEST[0] = HANDS[0]; hp._N[0] = side
        hp.hand(k, hx, hy, w * 1.15, sf.SKIN, seed, d(a1 + a2), 1 if a2 >= 0 else -1)
    return hx, hy


def sofia(k, x, feet, s=1.0, pose="hold", face_kind="smile", look=(0, 0), lag=(0, 0), seed=7, badge=True, lean=0.0,
          mouth=None, sparkle=0.0, tablet_kind="auto"):
    """sofia_dh's suit cut in navy over a white blouse, pearls, the sleek hair and the high ponytail."""
    old = (ss.BLOUSE, ss.BLOUSE_SHADE, ss.SKIRT, sf.BLOUSE, sbc.BLAZER, sbc.BLAZER_EDGE, ss.SWEPT[0], sbc._blazer,
           ss.PULLED[0], ss.PENCIL[0], ss.SLEEK[0])
    old_arm = sf._arm
    sf._arm = _canon_arm
    ss.PULLED[0] = True; ss.PENCIL[0] = True; ss.SLEEK[0] = True; ss.SWEPT[0] = False
    ss.BLOUSE, ss.BLOUSE_SHADE, ss.SKIRT, sf.BLOUSE = WHITE, WHITE_SHADE, SUIT[0], WHITE
    suit_old = (sdh.CREAM, sdh.CREAM_SHADE, sdh.SILK)
    sbc.BLAZER, sbc.BLAZER_EDGE = SUIT[0], SUIT[1]
    sbc._blazer = _interview_blazer
    own = face_kind if face_kind in scs.OWN else None
    orig_face = so._face
    if own:
        so._face = lambda o, sp: scs._mine(orig_face(o, sp), own)
    if face_kind == "tight":                                # the fake-professional smile (sofia_ps's "tight", from sofia_dh)
        so._face = lambda o, sp: sdh._tight(orig_face(o, sp))
        face_kind = "smile"
    c = k.c
    if PONY[0]:
        c.save(); c.translate(x, feet); c.rotate(math.radians(lean)); c.scale(s, s)
        ponytail(k, sofia_fs.HY, seed + 1, lag[0], lag[1])
        c.restore()
    try:
        return so.sofia(k, x, feet, s, pose, scs.OWN.get(face_kind, face_kind), look, lag, seed, badge, lean, mouth,
                        sparkle, tablet_kind)
    finally:
        so._face = orig_face
        sf._arm = old_arm
        sdh.CREAM, sdh.CREAM_SHADE, sdh.SILK = suit_old
        (ss.BLOUSE, ss.BLOUSE_SHADE, ss.SKIRT, sf.BLOUSE, sbc.BLAZER, sbc.BLAZER_EDGE, ss.SWEPT[0], sbc._blazer,
         ss.PULLED[0], ss.PENCIL[0], ss.SLEEK[0]) = old


def binder(k, cx, cy, s=1.0, seed=4450):
    """Her binder, open to us at her chest (reading): a charcoal cover, a white page with lines. Not blue: blue is the
    Client's blueprint, the only blue paper in the show."""
    c = k.c
    c.save(); c.translate(cx, cy); c.scale(s, s)
    rect(k, -36, -26, 72, 52, (0.22, 0.23, 0.26), seed, lw=2.0)
    rect(k, -31, -22, 62, 44, (0.98, 0.98, 0.95), seed + 1, shadow=False, lw=1.4)
    c.set_source_rgb(0.62, 0.64, 0.68); c.set_line_width(1.6)
    for yy in (-12, -4, 4, 12):
        c.move_to(-24, yy); c.line_to(24, yy); c.stroke()
    c.restore()


def with_board(k, x, feet, s, board, face_kind="smile", look=(0, 0), lag=(0, 0), lift=110, bw=72, bh=52, full=1.0):
    """The row board_two (the canon: a board, tablet, card or printout in two hands, 2/2 in its silhouette test): her
    arms by IK to the board's upper corners, her own hands not drawn, then the board, then a clutch at each corner.
    board: "binder" (reading, 8.1; the fake smile; nervous) or "box" (the clear box of paperclips, 1.4). Returns the rig's points."""
    import hands_v4 as hv
    from cand_bc import ik
    bt = -300 * sf.H + 78
    cy_l = bt + lift                                           # the board's centre, in her units below the feet
    w = F_W * 1.3
    tl = [(side * (bw / 2 - 0.42 * w), cy_l - bh / 2) for side in (-1, 1)]
    pose = ik(-39, bt + 14, tl[0][0], tl[0][1], 48, 48, -1) + ik(39, bt + 14, tl[1][0], tl[1][1], 48, 48, 1)
    sbc.POSES["_board"] = pose
    old = HANDS[0]; HANDS[0] = (None, None)
    try:
        o = sofia(k, x, feet, s, pose="_board", face_kind=face_kind, look=look, lag=lag, tablet_kind="none")
    finally:
        HANDS[0] = old
    cx, cy = x, feet + cy_l * s
    def draw_board(k_):                                        # in her units: the line weight scales with her, as the rig's does
        if board == "box":
            clip_box(k_, 0, bh / 2, bw / 60.0, full=full)
        else:
            binder(k_, 0, 0, bw / 72.0)
    c = k.c
    c.save(); c.translate(cx, cy); c.scale(s, s)
    hv.board_two(k, 0, 0, bw, bh, 0.0, w, sf.SKIN, sf.SKIN, draw_board)
    c.restore()
    return o


def clip_box(k, x, y, s=1.0, full=1.0, seed=4400):
    """The clear box of paperclips she carries (1.4), its bottom edge centred at (x, y): a lidless clear plastic box,
    silver clips inside up to `full` (0..1)."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    w, h = 60, 34
    cut(k, [(-w / 2, -h), (w / 2, -h), (w / 2, 0), (-w / 2, 0)], (0.86, 0.92, 0.95), shadow=False, lw=2.0)
    if full > 0:
        top = -h * full * 0.85
        cut(k, [(-w / 2 + 3, top), (w / 2 - 3, top), (w / 2 - 3, -3), (-w / 2 + 3, -3)], (0.74, 0.76, 0.80), shadow=False, lw=0)
        c.set_source_rgb(0.40, 0.42, 0.47); c.set_line_width(1.3)
        import random
        r = random.Random(seed)
        for _ in range(int(14 * full)):
            cx, cy = r.uniform(-w / 2 + 8, w / 2 - 8), r.uniform(top + 3, -6)
            c.save(); c.translate(cx, cy); c.rotate(r.uniform(-1, 1)); c.new_path()
            c.move_to(-5, -2); c.line_to(5, -2); c.arc(5, 0, 2, -math.pi / 2, math.pi / 2); c.line_to(-4, 2); c.stroke(); c.restore()
    c.set_source_rgba(1, 1, 1, 0.55); c.set_line_width(3); c.move_to(-w / 2 + 6, -h + 5); c.line_to(-w / 2 + 6, -6); c.stroke()
    c.restore()


def sheet(out="../the-double-agent/da_sofia_v3.png"):
    """v2: 14's look beside the new one at series scale; the jobs of episode 15 (the binder, the box of clips, reading);
    four faces; the phone-size check against Don's navy vest."""
    import sofia_ps
    import don_ps
    W, H = 1080, 1080
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W * 2, H * 2)
    c = cairo.Context(surf); c.scale(2, 2); k = Ctx(c, 0)
    c.set_source_rgb(0.93, 0.89, 0.82); c.paint()
    def t(x, y, s_, size=12, bold=0):
        c.select_font_face("Inter", 0, bold); c.set_font_size(size); c.set_source_rgb(0.15, 0.15, 0.18); c.move_to(x, y); c.show_text(s_)
    t(30, 40, "SOFÍA · The Double Agent (15) · v3 · the next day: the job interview", 20, 1)
    t(30, 62, "v2 (character audit 26 Nov): charcoal, not navy (Don's vest is navy); shoulders 12 % narrower; no gold lapel edge,"
      " pearl buttons; the pearls stay; the series' high ponytail.", 11)
    t(30, 78, "v3 (hands canon): her hands through hands_ps at the class sheet's female width 15, no nail; the binder and the"
      " box are the row board_two (the board, then a clutch at each upper corner).", 11)
    F = 470
    c.set_source_rgb(0.45, 0.40, 0.34); c.set_line_width(1.5); c.move_to(20, F); c.line_to(W - 20, F); c.stroke()
    don_ps.don(k, 90, F, 0.60)
    sofia_ps.sofia(k, 240, F, 0.47)
    import hands_ps as hp
    import hands_v4 as hv
    hv.enable()
    with_board(k, 400, F, 0.47, "binder", face_kind="tight")                              # the binder, fake-professional
    with_board(k, 580, F, 0.47, "box", face_kind="smile", lag=(1.5, 0), lift=118, bw=64, bh=36)   # the clip box (1.4)
    with_board(k, 760, F, 0.47, "binder", face_kind="interested", look=(0, 0.8), lift=100)  # reading (8.1)
    sofia(k, 930, F, 0.47, pose="stand", face_kind="caught", look=(-0.6, 0), tablet_kind="none")   # nervous, hands quiet
    for x, s_ in ((90, "Don 0.60 (navy vest)"), (240, "14: cream suit, bun"), (400, "15: the binder, fake smile"),
                  (580, "15: the clip box (1.4)"), (760, "15: reading (8.1)"), (930, "15: nervous, at rest")):
        t(x - 55, F + 22, s_, 11)
    # faces
    y2 = F + 60
    t(30, y2, "FACES", 13, 1)
    for i, (fk, lab) in enumerate((("smile", "smile"), ("tight", "fake-professional"), ("caught", "nervous"), ("interested", "interested"))):
        x = 140 + i * 240
        c.save(); c.rectangle(x - 100, y2 + 12, 200, 190); c.clip()
        sofia(k, x, y2 + 12 + 440, 1.3, pose="stand", face_kind=fk, tablet_kind="none")
        c.restore()
        c.set_source_rgb(0.15, 0.15, 0.18); c.set_line_width(1); c.rectangle(x - 100, y2 + 12, 200, 190); c.stroke()
        t(x - 95, y2 + 222, lab, 11)
    # phone size: Don, Sofía (v1 navy, v2 charcoal) side by side as in a frame 270 px wide
    y3 = y2 + 270
    t(30, y3, "AT PHONE SIZE (a 270 px frame): Don's vest, v1 navy, v2 charcoal", 13, 1)
    c.save(); c.translate(60, y3 + 10); c.scale(0.5, 0.5)
    don_ps.don(k, 60, 300, 0.60)
    SUIT[0], SUIT[1] = NAVY, NAVY_SHADE
    sofia(k, 200, 300, 0.47)
    SUIT[0], SUIT[1] = CHARCOAL, CHARCOAL_SHADE
    sofia(k, 330, 300, 0.47)
    c.restore()
    hv.disable()
    surf.write_to_png(out)
    print("wrote", out)


if __name__ == "__main__":
    sheet(*sys.argv[1:])
