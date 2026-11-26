"""Pick a Side: the new ending's key frames (story audit v1, Tomas's picks A1 B1 C1 D1, 26 Nov). Stills only, opt-in:
nothing here changes the board or the locked scenes. Run: python3 ps_ending_v2.py VER -> ps_ending_stills_vN.png.

5.1  the guard at the OPEN office door, the CV in his hand, his knuckles on the door (he has come back from the club)
5.3a the robot to him: "Welcome."; Sofía behind, no CV yet
5.3c the hand-over: his hand gives the CV, hers takes it, both owners in frame
5.5b 2.8's heel insert again, now both shoes past the tape, walking away
6.1  Pam in frame behind Don, her thumb on ACCEPT while he says "Everyone's with me."
6.2  Don yanks the blind DOWN, eyes shut (he won't see it); the robot's hand pulls up: 1.1's tug of war
"""
import math
import os
import sys
import cairo
import kit
from kit import Ctx, INK, cut, rect
import ps_scenes as ps
import ps_film as pf
import ps_motion as pm_
import dh_cast as dc
import client_ob as co
import hands_ps as hp

F = ps.F
pss, sp = ps.pss, ps.sp
GS = ps.GUARD_S
HALL = (0.36, 0.38, 0.42)


def look():
    """the film's look (as ps_film's stills); Tomas 26 Nov: the CV is Father's invitation"""
    ps.gags_v5()
    sp.INVITE[0] = True
    pf.dp.BLIND_GAP_FIX[0] = pf.dp.ROLL_TAIL[0] = True
    pss.NO_DOOR_CONFETTI[0] = ps.rp.SUN_UP[0] = True
    ps.LIGHT_V5[0] = True
    import pm_ps
    pm_ps.MUG_RING[0] = True


def open_door(k):
    """the glass door swung in: the doorway shows the corridor, the panel edge-on at its hinge (screen right)"""
    c = k.c
    x0, y0, w, h = pss.GX0, pss.GY0, pss.GW, pss.GH
    g = cairo.LinearGradient(0, y0, 0, y0 + h)
    g.add_color_stop_rgb(0, *HALL); g.add_color_stop_rgb(1, 0.26, 0.27, 0.30)
    c.set_source(g); c.rectangle(x0, y0, w, h); c.fill()
    c.set_source_rgb(0.30, 0.31, 0.34); c.rectangle(x0, y0 + h - 40, w, 40); c.fill()       # the corridor's floor
    cut(k, [(x0 + w, y0), (x0 + w + 34, y0 - 14), (x0 + w + 34, y0 + h + 14), (x0 + w, y0 + h)],
        (0.80, 0.90, 0.95), shadow=False, lw=2.4)                                           # the panel, swung in
    c.set_source_rgba(1, 1, 1, 0.5); c.set_line_width(3)
    c.move_to(x0 + w + 12, y0 + 40); c.line_to(x0 + w + 22, y0 + h - 60); c.stroke()


def guard_at(k, x, pose_r=None, pose_l=None, flip=False):
    """bodyguard 2 at x on the floor line; pose_r / pose_l: hand targets in his rig units, or None for the folded hands"""
    g = list(dc.GUARD_POSE)
    if pose_l:
        g[0], g[1] = dc.ik(-co.SH[0], co.BT + 26, pose_l[0], pose_l[1], co.LN1, co.LN2, -1)
    if pose_r:
        g[2], g[3] = dc.ik(co.SH[0], co.BT + 26, pose_r[0], pose_r[1], co.LN1, co.LN2, 1)
    return dc.guard(k, x, F + 46, GS, pose=tuple(g), flip=flip)


def cv_plain(k, x, y, s, word=True, ang=-0.06):
    was = sp.CV_N[0]
    sp.CV_N[0] = None if word else 0
    try:
        sp.cv_coo(k, x, y, s, ang)
    finally:
        sp.CV_N[0] = was


def fingers(k, x, y, n=3, ln=7.0, w=4.0, d=-1, skin=co.SKIN):
    """fingertips over an edge (lesson 224: the object, then the fingers over it); d: the side they come from"""
    c = k.c
    for i in range(n):
        for col, lw in ((INK, w + 1.6), (skin, w)):
            c.set_source_rgb(*col); c.set_line_width(lw); c.set_line_cap(1)
            c.move_to(x - d * 2, y + i * (w + 0.8)); c.line_to(x + d * ln, y + i * (w + 0.8)); c.stroke()
    c.set_line_cap(0)


# --- 5.1 ---------------------------------------------------------------------------------------------------------------
# v4 (Tomas 26 Nov: "analizuok duris the-onboarding"): the set's own door, not an invented one. The Onboarding's glass door
# (set_ob.door, the same DOOR rect as ours) SLIDES left, the bright street behind it; a visitor outside is drawn inside the
# opening with the glass over him (ob_anim._through_glass); it slides open in ~0.15 s (lesson 133) and shut behind him
# (ob s10_4). ps_set already has it opt-in: DOOR_OPEN. v1-v3 drew a hinged panel and a dark corridor: wrong.
import set_ob as sto


def through_glass(k, draw_, open_):
    """ob_anim._through_glass (reused): someone outside, inside the opening, the glass over him where it has not slid"""
    c = k.c
    x, y, w, h = sto.DOOR
    c.save(); c.rectangle(x, y, w, h); c.clip()
    out = draw_()
    px = x - w * 0.92 * open_
    c.set_source_rgba(*sto.GLASS, 0.26); c.rectangle(px, y, w, h); c.fill()
    c.restore()
    return out


def cast_51(k):
    """the door SHUT: he is outside on the bright street, in colour (3.6 showed only his dark shape), the CV in one hand,
    his knuckles on the glass"""
    heads = {}
    def draw_():
        return guard_at(k, sto.DOOR[0] + sto.DOOR[2] / 2 - 4, pose_r=(104, -262), pose_l=(-40, -200))   # knock at chest height: a fist by the ear reads as a call (rules §1)
    o = through_glass(k, draw_, 0.0)
    heads["guard"] = (o["head"][0], o["head"][1], 40 * GS)
    lx, ly = o["hands"][0]
    cv_plain(k, lx - 4, ly + 22, 0.62, word=False)           # blank: 5.2 writes on it
    fingers(k, lx + 6, ly + 2, d=-1)
    rx, ry = o["hands"][1]                                   # knock, knock: his knuckles ON the glass (a pale flat spot where they
    c = k.c                                                  # touch, v6, review: "clearly touch"), the strokes from that spot
    c.set_source_rgba(1, 1, 1, 0.55); c.save(); c.translate(rx + 8, ry); c.scale(5, 10); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(2.6); c.set_line_cap(1)
    for a in (-0.7, 0.0, 0.7):
        c.move_to(rx + 14 + 6 * math.cos(a), ry + 12 * math.sin(a)); c.line_to(rx + 14 + 18 * math.cos(a), ry + 24 * math.sin(a)); c.stroke()
    c.set_line_cap(0)
    return heads


def s51():
    pss.DOOR_OPEN[0] = 0.0
    return ps.S("5.1n", (130, F - 150, 1.75), dict(blind="torn", tape=True, spun=True), cast_51)


# --- 5.3a ---------------------------------------------------------------------------------------------------------------
def cast_53a(k):
    """the door has slid open (the set's DOOR_OPEN, as the robot opens it in the board); he steps in off the street"""
    heads = {}
    o = guard_at(k, pss.GX0 + pss.GW / 2 + 40, pose_l=(-40, -200))
    heads["guard"] = (o["head"][0], o["head"][1], 40 * GS)
    lx, ly = o["hands"][0]
    cv_plain(k, lx - 4, ly + 22, 0.62)                      # HR? written now (5.2)
    fingers(k, lx + 6, ly + 2, d=-1)
    _, heads["sofia"] = ps.sofia(k, (350, F + 60), "hip", "smile", (-1, -0.2))
    _, heads["robot"] = ps.robot(k, (262, F + 40), arms=((-80, -30), (40, 0)), look=(-1, -0.3))
    return heads


def s53a():
    ps.ROBOT_WALL["5.3n"] = 1                                # its box not on the guard's side: over or right of it
    pss.DOOR_OPEN[0] = 0.85
    return ps.S("5.3n", (205, F - 160, 1.45), dict(blind="torn", tape=True, spun=True), cast_53a)


# --- 5.3c: the hand-over -----------------------------------------------------------------------------------------------
def cast_53c(k):
    """v6 (Tomas 26 Nov: the series' grab on both): his rig and hers, the card between, then hands_ps "grab" drawn over
    each rig's hand at the very point it returned (one hand per wrist, lesson 208), its fingers over the card's edge
    (lesson 224); no loose finger strokes."""
    heads = {}
    o = guard_at(k, 164, pose_r=(165, -180))
    heads["guard"] = (o["head"][0], o["head"][1], 40 * GS)
    gx, gy = o["hands"][1]
    sx = gx + 50 + 85 + CARD_GAP[0]
    os_, heads["sofia"] = ps.sofia(k, (sx, F + 60), "press", "interested", (-1, 0.1))
    hx, hy = min(os_["hands"], key=lambda h: h[0])
    mx, my = (gx + hx) / 2, (gy + hy) / 2
    cv_plain(k, mx, my, 1.0, ang=-0.04)
    hp.draw(k, "grab", gx, gy, GRAB_W[0], co.SKIN, (1.0, -0.15), 1)            # his: from the left, round the card's edge
    hp.draw(k, "grab", hx, hy, GRAB_W[1], sp.sbc.sf.SKIN, (-1.0, -0.15), -1)   # hers: from the right
    return heads


GRAB_W = [26, 21]
CARD_GAP = [30]      # extra room between the two rigs so each hand sits on one edge of the card, not on top of the other


def s53c():
    return ps.S("5.3c", (306, F - 150, 1.5), dict(blind="rehung", tape=True, spun=True), cast_53c)


# --- 5.5b: both shoes over the tape ----------------------------------------------------------------------------------
def ins_55b(k):
    c = k.c
    c.set_source_rgb(*kit.FLOOR); c.paint()
    cut(k, [(70, 960), (150, 960), (300, 0), (250, 0)], pss.TAPE, shadow=False, lw=2.4)    # the tape, receding
    c.set_source_rgba(1, 1, 1, 0.40); c.set_line_width(3); c.move_to(96, 940); c.line_to(262, 20); c.stroke()
    for x, y, s in ((340, 540, 0.80), (395, 800, 0.95)):     # both feet on Father's side, toes away from Don's
        c.save(); c.translate(x, y); c.scale(-1, 1)
        sp.heel(k, 0, 0, s, tape=False)
        c.restore()
    cut(k, [(150, -10), (470, -10), (480, 120), (420, 140), (330, 150), (230, 140), (160, 120)], (0.97, 0.95, 0.90), lw=2.6)   # her
    c.set_source_rgb(0.80, 0.76, 0.66); c.set_line_width(2)                                    # white coat's hem: whose legs
    c.move_to(320, 0); c.line_to(318, 146); c.stroke()
    kit.text(k, "← DON", 110, 880, 30, INK)


def s55b():
    return ps.S("5.5b", "screen", draw=ins_55b)


# --- 6.1: Pam in frame, her thumb on ACCEPT --------------------------------------------------------------------------
PAM_X_61N = [640]


def cast_61n(k, buzz=False):
    heads = {}
    _, heads["mom"] = ps.mom(k, "mom_tape", "folded", "stern", (1, -0.6))
    o, heads["sofia"] = ps.sofia(k, (ps.SOF_61[0], F + 40), "chest", "smile", (0.2, 0.6))
    hx, hy = o["hands"][0]
    sp.cv_coo(k, hx + 4, hy + 40, ps.CV_61[0] * 0.82)
    o, heads["pam"] = ps.pam(k, (PAM_X_61N[0], F + 40), "cup_mid", "avert", (0.6, 0.8), mug=False)   # eyes down to it
    px, py = o["hands"][1]
    c = k.c
    ph = 0.34
    cy = py + 8                                              # at her chest, under her chin: her face clear (v3: it hid it)
    c.save(); c.translate(px + 2, cy)
    pss.phone_close(k, 0, 0, ph, lit=True, buzz=buzz)
    if not buzz:                                             # ACCEPT pressed: a ring round the button
        c.set_source_rgba(0.20, 0.85, 0.40, 0.65); c.set_line_width(3.5)
        c.new_path(); c.arc(0, 62 * ph, 30 * ph, 0, 2 * math.pi); c.stroke()
    c.restore()
    bx, by = px + 2, cy + 62 * ph                            # her thumb from the hand's side onto the button
    sk = __import__("pam_mf").SKIN
    for col, lw in ((INK, 6.4), (sk, 4.4)):
        c.set_source_rgb(*col); c.set_line_width(lw); c.set_line_cap(1)
        c.move_to(bx + 16, by + 14); c.line_to(bx + 3, by + 1); c.stroke()
    c.set_line_cap(0)
    return heads


def s61n():
    b = pf.BOARD["6.1"]
    return dict(b, cast=cast_61n, room=dict(b["room"], phone=None))    # her phone is in her hand, not on the counter


def s61bn():
    """6.1b: the phone in Pam's hand buzzes (it is not on the shelf any more)"""
    b = pf.BOARD["6.1b"]
    return dict(b, cast=lambda k: cast_61n(k, buzz=True), room=dict(b["room"], phone=None))


# --- 6.1b as three drawings (Tomas 26 Nov grill: phone -> team -> arms, 1.5 s) -----------------------------------------
def fg_61x(look, face="shock", pose="vest", spring=1.0):
    """Don, near: the board's fg_61b (spring hair, round eyes) with the eyes aimed by look; pose "stand" drops the
    spring (the shock is over) and lets the arms hang."""
    if pose == "vest":
        ps.SPRING_61B[0] = spring; ps.LOOK_61B[0] = look; ps.FACE_61B[0] = face
        try:
            return ps.fg_61b(k_hold[0])
        finally:
            ps.SPRING_61B[0] = 1.0; ps.LOOK_61B[0] = (1, -1); ps.FACE_61B[0] = "shock"
    s_ = 0.60 * 2.5
    o = ps.dp.don(k_hold[0], ps.DON_X_61[0], 1150, s_, pose, face, look, chin=0)
    return {"don": (o["head"][0], o["head"][1], ps.R["don"] * s_)}


k_hold = [None]
LOOK_PHONE = [(1, -1)]      # up-right on screen: Pam's phone
LOOK_TEAM = [(-1, -1)]      # up-left: Mom, Sofía with the card


def s61bx(i):
    b = s61bn()
    def fg(k):
        k_hold[0] = k
        if i == 0:
            return fg_61x(LOOK_PHONE[0])
        if i == 1:
            return fg_61x(LOOK_TEAM[0], spring=0.55)
        return fg_61x((0, 0.6), "confused", "stand")
    return dict(b, fg=fg)


def s61b1(): return s61bx(0)
def s61b2(): return s61bx(1)
def s61b3(): return s61bx(2)


# --- 6.2: Don yanks it DOWN, eyes shut ------------------------------------------------------------------------------
DIM_62 = 0.16                                                # Tomas 26 Nov: lighter darkening than the 1.1 tug (0.32)


def s62x(t, sid, shut):
    """6.2 (1.4 s, Tomas 26 Nov: down -> the robot up -> 1.1): the 1.1 tug's own shot_A at time t, darkening at DIM_62;
    shut=True: Don's eyes screwed shut (he yanks it down and won't look)."""
    pm_.DIM_A[0] = DIM_62
    sh = pm_.shot_A(t, v4=True)
    inner = sh["cast"]
    def cast(k):
        orig = ps.don
        def don_(k_, at, pose, face, *a, **kw):
            return orig(k_, at, pose, "squint" if shut else face, *a, **kw)
        ps.don = don_; pm_.ps.don = don_
        pm_.DIM_A[0] = DIM_62
        try:
            return inner(k)
        finally:
            ps.don = orig; pm_.ps.don = orig; pm_.DIM_A[0] = 0.32
    return dict(sh, cast=cast, id=sid)


def s62n():
    return s62x(0.55, "6.2n", True)                          # all the way down, eyes shut


def s62b():
    return s62x(0.72, "6.2b", False)                         # the robot yanks it back up; his eyes open on it


NEW = [("5.1", s51, None, "knocks, the invitation"),
       ("5.3a", s53a, 'ROBOT: "Welcome."', "the door slid open: Welcome."),
       ("5.3c", s53c, None, "the hand-over"),
       ("5.5b", s55b, None, "both shoes over the tape"),
       ("6.1", s61n, 'DON: "Everyone\'s with me."', "Pam's thumb on ACCEPT"),
       ("6.1b", s61b1, None, "buzz: his eyes to her phone"),
       ("6.1b2", s61b2, None, "his eyes to the team"),
       ("6.1b3", s61b3, None, "his arms drop"),
       ("6.2", s62n, None, "down, eyes shut (dim 0.16)"),
       ("6.2b", s62b, None, "the robot yanks it up")]


def frame(fn, line):
    sh = fn()
    try:
        if line:
            return ps.board_frame(sh, line)
        import ps_checks as pc
        pc.install_scene(ps); pc.begin()
        return ps.render(sh)
    finally:
        pss.DOOR_OPEN[0] = 0.0


def main(ver):
    look()
    old = lambda sid, t: pf.drawing(sid, t)
    seq = [("4.3c", lambda: old("4.3", 2.85), "Invite her.", False),
           ("5.1", None, None, True), ("5.2", lambda: old("5.2", 1.3), "he writes her name", False),
           ("5.3a", None, None, True), ("5.3c", None, None, True), ("5.3b", lambda: old("5.3", 2.0), "the can, the heart", False),
           ("5.4", lambda: old("5.4", 1.5), "the foot", False), ("5.5", lambda: old("5.5", 1.0), "the invitation, on the tape", False),
           ("5.5b", None, None, True), ("5.6", lambda: old("5.6", 1.8), "Some draw lines.", False),
           ("5.7", lambda: old("5.7", 1.1), "INVITATION · DAD", False),
           ("6.1", None, None, True), ("6.1b", None, None, True),
           ("6.1b2", None, None, True), ("6.1b3", None, None, True),
           ("6.2", None, None, True), ("6.2b", None, None, True), ("1.1", lambda: old("1.1", 0.0), "→ 1.1 frame 0", False)]
    new = {sid: (fn, line, lab) for sid, fn, line, lab in NEW}
    tiles, faults = [], []
    for sid, fn, lab, is_new in seq:
        if is_new:
            f_, line, lab = new[sid]
            surf, msgs = frame(f_, line)
        else:
            surf, msgs = fn()
        faults += ["%s: %s" % (sid, m) for m in msgs]
        tiles.append((surf, sid, lab, is_new))
        if is_new:
            surf.write_to_png(os.path.join(ps.OUT, "ps_ending_%s_v%d.png" % (sid.replace(".", ""), ver)))
    tw, th, cols = 270, 480, 5
    rows = (len(tiles) + cols - 1) // cols
    o = cairo.ImageSurface(cairo.FORMAT_RGB24, 20 + cols * (tw + 14), 20 + rows * (th + 34))
    c = cairo.Context(o); c.set_source_rgb(0.55, 0.55, 0.55); c.paint()
    for j, (im, sid, lab, is_new) in enumerate(tiles):
        x, y = 20 + (j % cols) * (tw + 14), 20 + (j // cols) * (th + 34)
        if is_new:
            c.set_source_rgb(0.95, 0.75, 0.10); c.rectangle(x - 5, y - 5, tw + 10, th + 10); c.fill()
        c.save(); c.translate(x, y); c.scale(0.5, 0.5); c.set_source_surface(im, 0, 0); c.paint(); c.restore()
        c.set_source_rgb(0, 0, 0); c.set_font_size(13); c.move_to(x, y + th + 18)
        c.show_text("%s%s  %s" % (sid, " NEW" if is_new else "", lab))
    p = os.path.join(ps.OUT, "ps_ending_stills_v%d.png" % ver)
    o.write_to_png(p)
    print("wrote", p)
    for f in faults:
        print("FAULT", f)


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
