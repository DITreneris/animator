"""Approved. (episode 16): the two key stills, stage 3b (plan rule 2; Tomas /grill-me 28 Nov).

K1, the loop seam (frame 0 = the last frame, script v4 1.1 / 7.2): a LOW CLOSE AT THE CASTER (Tomas's pick): the gold
throne's base, REVIEW · TOMORROW folded under its front caster, Don's dangling legs and his hanging right hand (he is
asleep in it, tilted back), the robot's gripper reaching in for the card, UPTIME 100% glowing from out of frame. No full
seated Don is needed (new poses go through the pose sandbox, Tomas's pick).
K2, the silence (6.2-6.7): the robot SET ON THE SEAT (Tomas's pick: no new robot pose, its wheel off the cushion's
edge), its face APPROVER: CEO with Don's face; Don in front, his fingertip raised toward it and stopped (`point`,
clearly apart from the screen: rules "a finger near a sign reads as holding it"); Father beside, turned to Don.
v1 has no Father finger: dh_cast.father has no arm control (to the pose sandbox, with Don's seated pose).

Both in the night lock (rv_night_cast v6: the grade, the shade 0.30 on people, glows only at their sources), the props
from rv_props (one screen function, the tag). Runs on a checkout with episode 15's modules, as rv_night_cast.
  python3 rv_keys.py all  -> ../the-review/rv_K1_v1.png, rv_K2_v1.png (+ _270)
"""
import math
import sys
import cairo
import kit
import rv_hands as rh
rh.setup()
import bp_frame as bp
import ps_set as pss
import don_ps as dp
import robot_ps as rp
import dh_cast as dc
import hand_lib_v4 as hl
import rv_night_cast as nc
import rv_props as pr

EP = "../the-review/"
F = pss.F
TX, TF, TS = pss.THRONE                                      # (452, 808, 0.6)
SEAT = (452, 742)
KHAKI, SHOE, SHIRT, SKIN = (0.80, 0.74, 0.62), (0.24, 0.18, 0.13), (0.97, 0.97, 0.96), (0.98, 0.84, 0.72)
STEEL, STEEL_D = rp.STEEL, rp.STEEL_D


def _card_under_caster(k, x, y, s=1.0):
    """REVIEW · TOMORROW folded twice into a wedge, its red letters on the visible fold."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    kit.cut(k, [(-27, 0), (30, 0), (26, -9), (-23, -11)], pr.PAPER, lw=1.8, shadow=False)   # v5: wider ("the word sticks out")
    c.select_font_face(kit.FONT); c.set_font_size(6.5); c.set_source_rgb(*pr.RED)
    e = c.text_extents("TOMORROW"); c.move_to(1.5 - e.x_advance / 2, -3); c.show_text("TOMORROW")
    c.restore()


def _lap(k):
    """v1c: what of a sleeping Don shows at the top of the low close: his lap on the seat, the vest's hem, the shirt."""
    c = k.c
    kit.cut(k, [(410, SEAT[1] + 4), (496, SEAT[1] + 4), (500, SEAT[1] - 30), (406, SEAT[1] - 30)], KHAKI, lw=2.0, shadow=False)
    kit.cut(k, [(414, SEAT[1] - 28), (492, SEAT[1] - 28), (488, SEAT[1] - 120), (418, SEAT[1] - 120)], SHIRT, lw=2.0,
            shadow=False)
    for side in (-1, 1):                                     # the vest's two fronts, open over the shirt
        x0 = 452 + side * 40
        kit.cut(k, [(x0, SEAT[1] - 26), (452 + side * 12, SEAT[1] - 24), (452 + side * 10, SEAT[1] - 120), (x0, SEAT[1] - 120)],
                (0.16, 0.22, 0.36), lw=2.0, shadow=False)
    c.set_source_rgb(0.35, 0.25, 0.16); c.rectangle(412, SEAT[1] - 34, 82, 7); c.fill()          # the belt


def _legs(k):
    """Don's lower legs hanging from the seat's front edge, his shoes on the floor (asleep, tilted back)."""
    c = k.c
    for x0, x1, f in ((436, 428, F - 2), (468, 480, F)):
        c.set_source_rgb(*KHAKI)
        c.move_to(x0 - 9, SEAT[1] + 2); c.line_to(x0 + 9, SEAT[1] + 2); c.line_to(x1 + 8, f - 12); c.line_to(x1 - 8, f - 12)
        c.close_path(); c.fill_preserve(); c.set_source_rgb(*kit.INK); c.set_line_width(2.0); c.stroke()
        kit.ellipse(k, x1 + 3, f - 7, 13, 6.5, SHOE, 11, shadow=False, lw=1.8)


def _hanging_hand(k):
    """his right arm off the armrest, hanging (RELAXED, the hand library): sleeve then hand, forearm straight down."""
    ax, ay = 392, 702
    wx, wy = 384, 760                                        # v1c: his LEFT arm, off the far armrest (the right one
                                                             # sat on the throne's red lever: read as holding it)
    c = k.c
    c.set_source_rgb(*SHIRT); c.set_line_width(13); c.set_line_cap(1); c.move_to(ax, ay); c.line_to(wx, wy); c.stroke()
    c.set_source_rgb(*kit.INK); c.set_line_width(1.8)
    for dx in (-7, 7):
        c.move_to(ax + dx, ay); c.line_to(wx + dx, wy); c.stroke()
    hl.draw(k, "RELAXED", wx, wy + 2, math.pi / 2 + 0.12, 15, SKIN, side=-1)


def _gripper(k, tx, ty, reach=1.0):
    """v2 (cold round, 2 of 2: "a claw at the edge, hard to tell it is a robot", "covers the W"): more of the robot:
    its round elbow and a second segment in from the frame's right, its jaws on the card's far corner, the glow of its
    face out of frame on them."""
    c = k.c
    ex, ey = tx + 70, ty - 46                                # the elbow
    sx, sy = tx + 150, ty - 120                              # the shoulder, out of frame
    for (ax, ay), (bx, by) in (((sx, sy), (ex, ey)), ((ex, ey), (tx + 14, ty - 4))):
        c.set_source_rgb(*STEEL); c.set_line_width(13); c.set_line_cap(1); c.move_to(ax, ay); c.line_to(bx, by); c.stroke()
        c.set_source_rgb(*kit.INK); c.set_line_width(2.0)
        nx, ny = -(by - ay), (bx - ax); L = math.hypot(nx, ny); nx, ny = nx / L * 6.5, ny / L * 6.5
        for sgn in (-1, 1):
            c.move_to(ax + sgn * nx, ay + sgn * ny); c.line_to(bx + sgn * nx, by + sgn * ny); c.stroke()
    kit.ellipse(k, ex, ey, 11, 11, STEEL_D, 3, shadow=False, lw=2.0)                       # the elbow joint
    c.set_source_rgb(*kit.INK); c.arc(ex, ey, 3, 0, 2 * math.pi); c.fill()
    kit.cut(k, [(tx + 4, ty - 12), (tx + 20, ty - 12), (tx + 20, ty + 4), (tx + 4, ty + 4)], STEEL_D, lw=1.8, shadow=False)
    for dy in (-11, 2):                                      # the two jaws, closed on the card's corner
        kit.cut(k, [(tx - 8, ty + dy), (tx + 6, ty + dy), (tx + 6, ty + dy + 4), (tx - 8, ty + dy + 4)], STEEL, lw=1.6,
                shadow=False)


def _robot_arm_from_behind(k, tip, behind=True, side=1):
    """the robot's own arm style (thin grey segments, a round joint, its small jaws), coming out from BEHIND the throne's
    base: behind=True draws the hidden first segment (before the throne), False the visible rest (after it).
    side=1 from the right (jaws pointing left), -1 from the left (v4b: away from the throne's red lever)."""
    c = k.c
    tx, ty = tip
    p0, p1 = (tx - 40 * side, ty - 34), (tx - 6 * side, ty - 22)
    if behind:
        segs = [((tx - 80 * side, ty - 46), p0)]
    else:
        segs = [(p0, p1), (p1, (tx + 6 * side, ty - 3))]
    for (ax, ay), (bx, by) in segs:
        for col, wdt in ((kit.INK, 10), (STEEL, 6.5)):
            c.set_source_rgb(*col); c.set_line_width(wdt); c.set_line_cap(1); c.move_to(ax, ay); c.line_to(bx, by); c.stroke()
    if not behind:
        kit.ellipse(k, p1[0], p1[1], 6, 6, STEEL_D, 3, shadow=False, lw=1.6)
        for dy in (-6, 1):
            x0, x1 = sorted((tx + 2 * side, tx + 12 * side))
            kit.cut(k, [(x0, ty + dy), (x1, ty + dy), (x1, ty + dy + 3), (x0, ty + dy + 3)], STEEL, lw=1.2, shadow=False)


def _no_hr_badge():
    """the robot without its HR badge (Sofía has it from 2.5): robot_mf.robot (which robot_ps calls) with badge=False
    while it draws."""
    rm = rp.dq.rm
    old = rm.robot

    class _C:
        def __enter__(self):
            rm.robot = lambda *a, **kw: old(*a, **dict(kw, badge=False))

        def __exit__(self, *a):
            rm.robot = old
    return _C()


def _don_head(k, x, y, rr):
    """Don's own rig, small, his head centred in a screen's circle (its head is at -302 units, about 62 round)."""
    s_ = rr / 62.0 * 1.12
    with rh.second_pass():                                   # a picture on a screen: its hands are not the cast's
        dp.don(k, x, y + 302 * s_, s_, "stand", "neutral", look=(0, 0))


def hand_gate(label, cam, draw):
    """the canon hand gate on a key still (rv_hands, da_hand_gate): its job list is rv_scenes.HANDS[label]."""
    import fs_storyboard_v17 as sbv
    import hands_lr
    import rv_scenes as sc
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960); k = kit.Ctx(cairo.Context(s), 0)
    rh.begin()
    k.c.save(); sbv.view(k.c, *cam)
    with hands_lr.shot():
        draw(k)
    k.c.restore()
    faults = [f for f in rh.check(sc.HANDS.get(label)) if not f.startswith("    note")]
    print("hand gate %s: drawn %s: %s" % (label, rh.drawn(), "PASS" if not faults else "FAIL"))
    for f in faults:
        print("    " + f)
    assert not faults, "the hand gate fails %s" % label


def k1(out=EP + "rv_K1_v7.png"):
    """v4 (Tomas 28 Nov "Go 1"): a medium on the whole throne with Don asleep in it (the pose sandbox's don_seated,
    rv_poses v1), REVIEW · TOMORROW folded under the front-right caster. The robot is hidden behind the throne (its
    badge is on its chest at frame 0, not at the end: nothing of its chest may show); its screen's glow spills round
    the throne's back, and its own thin arm reaches out from behind the base to the card."""
    import rv_poses as rpo
    nc.NO_THRONE_CONFETTI[0] = True
    cam = (454, 756, 1.96)                                    # G3: the plaque above the frame, the DON mark and arrow whole
    card = (TX - 80, F + 4)                                 # v4b: the front-LEFT caster (2 of 2: the red lever read
                                                             # as part of the arm), the card larger ("tiny")

    def draw(k):
        nc._room(k, pam_behind=False)
        if nc._PASS[0] != "mask":
            _robot_arm_from_behind(k, (card[0] - 38, card[1] - 2), behind=True, side=-1)
            nc._shadow(k, TX, TF, 70)
            pss.throne(k)
            _card_under_caster(k, card[0], card[1], 1.45)
        rpo.don_sprawl(k, "B", report=True)                 # v6 (Tomas 28 Nov, after four rounds of the front-on seat
                                                             # read as "standing"): asleep across the throne, chin down,
                                                             # the report on his belly; silhouette test B: "dozed" 2 of 2
        if nc._PASS[0] != "mask":
            _robot_arm_from_behind(k, (card[0] - 38, card[1] - 2), behind=False, side=-1)
    hand_gate("K1", cam, draw)                              # v7: under the canon's hands (hands_lr, v4, quiet)
    glows = [(TX - 70, SEAT[1] - 60, 70, 90, bp.NIGHT_MONITOR, 0.40)]   # UPTIME's glow, from behind the throne's left side
    lights = [(TX - 70, SEAT[1] - 60, 180, 1.0), (nc.DOOR[0], nc.DOOR[1], 260, 0.4)]
    try:
        nc._frame(cam, draw, glows, lights, out, cast=nc.LOCK_CAST)
    finally:
        nc.NO_THRONE_CONFETTI[0] = False


def k2(out=EP + "rv_K2_v5.png"):
    nc.NO_THRONE_CONFETTI[0] = True
    cam = (474, 770, 1.84)                                   # v1c: the portrait's plaque out (G3: whole or out)
    st = {}

    def draw(k):
        nc._room(k, pam_behind=False)
        if nc._PASS[0] != "mask":
            nc._shadow(k, TX, TF, 70)
            pss.throne(k)
        with _no_hr_badge():                                 # v3: Sofía has had its HR badge since 2.5 (the review)
            r = rp.robot(k, SEAT[0], SEAT[1] + 4, nc.L.SC["robot"], look=(1, 0))  # set on the cushion, wheel at its edge
        if nc._PASS[0] != "mask":
            sx, sy = r["screen"][:2]
            pr.screen(k, sx, sy, 50 * nc.L.SC["robot"] * 1.16, "APPROVER: CEO", face_fn=_don_head)   # v3: Don's own head
            st["screen"] = (sx, sy)
        nc._shadow(k, 584, F + 40, 30)                          # v4 (Tomas 28 Nov: unlocked; script 6.2 and the hand-jobs
        import dh_cast as _dc                                   # v5: the ring off in this frame (cold 2/2: "a red blob"
        _dc.RING_ON[0] = False                                  # at 270 on the hanging hand; the face carries him here)
        try:
            rh.father(k, 584, F + 38, nc.L.SC["father"], hands=("point", "quiet"), pose=(-112, -30, -6, 0), look=(-1, -0.4))
        finally:
            _dc.RING_ON[0] = True
        nc._shadow(k, 372, F + 60, 34)                          # table H5): FATHER's finger reaches toward the screen and
        dp.don(k, 372, F + 58, nc.L.SC["don"], "stand", "shock", look=(1, -0.5))   # stops, clearly apart; Don only looks
    probe = kit.Ctx(cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 4, 4)), 0)
    probe.c.save(); import fs_storyboard_v17 as sbv; sbv.view(probe.c, *cam); draw(probe); probe.c.restore()
    sx, sy = st["screen"]
    hand_gate("K2", cam, draw)
    import da_hand_gate as g_                                  # canon §0.3: measure the gap, finger to screen, at feed size
    for h in g_.HANDS:
        if h["g"] == "point":
            tip = (h["at"][0] + h["d"][0] * 1.45 * h["w"], h["at"][1] + h["d"][1] * 1.45 * h["w"])
            X, Y = 270 + (sx - cam[0]) * cam[2], 480 + (sy - cam[1]) * cam[2]
            gap = math.hypot(tip[0] - X, tip[1] - Y) - 50 * nc.L.SC["robot"] * 1.16 * cam[2]
            print("K2: fingertip to the screen's edge: %.0f px at 540, %.0f px at 270" % (gap, gap / 2))
            assert gap / 2 >= 8, "the finger is on the screen at feed size (rules: a finger near a sign reads as holding it)"
    glows = [(sx, sy, 44, 40, bp.NIGHT_MONITOR, 0.50)]
    lights = [(sx, sy, 180, 1.0), (nc.DOOR[0], nc.DOOR[1], 260, 0.5)]
    try:
        nc._frame(cam, draw, glows, lights, out, cast=nc.LOCK_CAST)
    finally:
        nc.NO_THRONE_CONFETTI[0] = False


if __name__ == "__main__":
    {"all": lambda: (k1(), k2()), "k1": k1, "k2": k2}[sys.argv[1]]()
