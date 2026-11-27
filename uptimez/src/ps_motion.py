"""PICK A SIDE (episode 14): stage 6, the motion tests (series/production-process.md), after the board's second cold test
(23 Nov: what the stills can't carry). Each test is drawn by ps_scenes' own rigs, set and cameras, at the film's rate:
15 drawings a second on a 30 fps camera, 540 x 960. For the cold viewers: an 8 fps strip of each.
  A  1.1  the blinds tug of war, frame 0 to 0:01.8: down, up, down, up, each faster (the 0:01 physical joke)
  B  2.11 Don pulls the robot off the tape onto his side, it rolls back (1.4 s); again (1.0 s); the third time he steps
          into its path and it bumps him (3 of 3 cold viewers read the still as "the robot trips Don")
  C  5.4  the office gag: a knee up, the foot hovering over the line 0.6 s, back down, the vest straightened
          (2 of 3 read the still as "Don trips over the line")
v2 (23 Nov, two cold viewers on v1): A: who pulls was not seen (his fist never moved, both cords moved together):
now each cord ends in its owner's hand, and one pull yanks the other's hand up: a tug of war on one cord loop.
B: the robot seemed to roll by itself, and the bump was a jump between two drawings: now Don's hand grips the robot's
arm and he leans back hauling; he walks into the gap; the robot rolls into his back; impact. C: the foot comes down and
the arms fold to the vest over 0.3 s, not in one cut. v1 is ps_motion_v1.py.
v3 (the v2 cold test): A read who pulls (2 of 2) but "not a fight": the puller's face strains and he leans, harder each
round; the yanked one is caught out. B: the haul bigger (95), the third one drags it past him, he walks onto its spot
(0.7 s), it rolls straight back into him with speed lines. C passed (2 of 2), unchanged.
  python3 ps_motion.py [A B C]  ->  ../pick-a-side/ps_motion_<X>_v2.mp4 and ps_motion_<X>_strip_v2.png"""
import math
import os
import sys
import subprocess
import cairo
import ps_scenes as ps
import ps_set as pss
import don_ps as dp
import pm_ps as pm
import acts_ob as ac
from kit import Ctx, INK

DON_H, DON_S = 1.12, ps.SC["don"]


def don_arms(x, feet, left=None, right=None):
    """Don's arm angles that put his hands on world points (the rig's own IK)."""
    to = lambda p: ((p[0] - x) / DON_S, (p[1] - feet) / DON_S) if p else None
    return ac._pose(DON_H, left=to(left), right=to(right))


def cord_to(c, x, top, hand, pull):
    hx, hy = hand
    c.set_source_rgb(*pss.CORD); c.set_line_width(4.0); c.set_line_cap(1)
    c.move_to(x, top); c.line_to(hx, hy); c.stroke(); c.set_line_cap(0)
    c.save(); c.translate(hx, hy + 6); c.scale(5, 8); c.new_path(); c.arc(0, 0, 1, 0, 6.3); c.restore()
    c.set_source_rgb(*pull); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.4); c.stroke()

OUT = ps.OUT
F = ps.F
DRAW = 15                                                    # drawings a second
FPS = 30


def ease(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def lerp(a, b, u):
    return a + (b - a) * u


# --- A: the tug ---------------------------------------------------------------------------------------------------------
TUG = [(0.00, 0.20, "hold", 0), (0.20, 0.55, "down", 0), (0.55, 0.85, "up", 1), (0.85, 1.12, "down", 0),
       (1.12, 1.36, "up", 1), (1.36, 1.58, "down", 0), (1.58, 1.80, "up", 1)]


def tug_state(t):
    for t0, t1, kind, who in TUG:
        if t < t1:
            u = ease((t - t0) / (t1 - t0))
            if kind == "hold":
                return 0.0, None
            return (u if kind == "down" else 1 - u) * 0.92, ("don" if kind == "down" else "robot")
    return 0.0, None


VISOR_A = [True]                                             # opt-in: False = no sun pictogram on its visor (6.2 ending: 3/3 read it as "brightness up")
DIM_A = [0.32]                                               # opt-in: how dark the room gets as the blind comes down (6.2 ending: lighter)


def shot_A(t, v4=False):
    u, who = tug_state(t)
    n = u / 0.92                                              # 0 up .. 1 down
    top = pss.GY0 - 10 + 12
    def cast(k):
        heads = {}
        x, f = ps.at("don_cord")
        x += 26                                              # a step right of his cord: the arm reaches out and up, not across his face
        hd = (pss.CORD_L + 2, lerp(f - 310 * DON_S, f - 160 * DON_S, n))                     # his hand: down as it closes
        rnd = sum(1 for t0, t1, kind, _ in TUG if kind == "down" and t0 <= t)              # v3: the struggle grows
        dface = "confused" if who == "don" else ("smug" if n > 0.5 else "shock" if who == "robot" else "squint")
        o, heads["don"] = ps.don(k, (x, f), don_arms(x, f, left=hd), dface, (-0.4, -0.6),
                                 lean=(-0.05 * rnd if who == "don" else 0.0))
        hi = (-176, 0); lo = (-150, -24)                     # its near hand: yanked up as he pulls, down as it pulls
        arm = (lerp(lo[0], hi[0], n), lerp(lo[1], hi[1], n))
        rx, rf = ps.at("rob_cord")
        if v4:                                               # the film (ps_film, board v4): the robot a step left of the door
            rx -= 30; hi = (-180, 0); arm = (lerp(lo[0], hi[0], n), lerp(lo[1], hi[1], n))   # frame, as board v4's 1.1
        o2, heads["robot"] = ps.robot(k, (rx + 12, rf), arms=(arm, (8, 0)), visor="sun" if (n > 0.5 and VISOR_A[0]) else None,
                                      tilt=(0.10 if who == "robot" else 0.0))
        c = k.c
        cord_to(c, pss.CORD_L, top, o["hands"][0], pss.PULL)
        cord_to(c, pss.CORD_R, top, o2["hands"][0], pss.PULL_R)
        if who:                                              # whoever pulls: two short motion lines under the hand
            hx, hy = o["hands"][0] if who == "don" else o2["hands"][0]
            c.set_source_rgb(*INK); c.set_line_width(2.2); c.set_line_cap(1)
            for dx in (-8, 8):
                c.move_to(hx + dx, hy + 18); c.line_to(hx + dx, hy + 34); c.stroke()
        if u > 0:
            c.set_source_rgba(0.05, 0.05, 0.10, DIM_A[0] * n); c.rectangle(-400, 0, 1800, 1200); c.fill()
        return heads
    room = dict(blind="down", u=u, dim=False, cords=False) if u > 0.01 else dict(blind="up", cords=False)
    return ps.S("1.1", ps.S2, room, cast)


# --- B: the pulls and the bump ------------------------------------------------------------------------------------------
RX0 = ps.tape_x(140) - 10                                    # the robot balanced on the tape
DX0 = ps.tape_x(140) - 195                                   # Don, on his side
PULLS = [(0.0, 0.40, 1.30), (1.30, 1.60, 2.20)]              # (pull from, pulled by, back on the line at)
HAUL = 95                                                    # v3: how far he hauls it (v2's 60 read as "it barely moves")


def b_state(t):
    """-> robot x, tilt, Don x, phase, progress. v3: the third haul drags it past him to his left; he walks right onto
    its spot on the line (0.7 s, in front of it), stops to admire the line; it rolls straight back into his back."""
    for p0, p1, p2 in PULLS:
        if p0 <= t < p1:
            u = ease((t - p0) / (p1 - p0))
            return lerp(RX0, RX0 - HAUL, u), -0.12 * u, DX0 - 10 * u, "pull", u
        if p1 <= t < p2:
            u = ease((t - p1) / (p2 - p1))
            return lerp(RX0 - HAUL, RX0, u), 0.12 * (1 - u) * (1 if int(t * 8) % 2 else -1), DX0, "back", u
    if t < 2.55:                                              # the third haul, hard: right past him
        u = ease((t - 2.20) / 0.35)
        return lerp(RX0, DX0 - 70, u), -0.14, DX0 + 10 * u, "pull", u
    if t < 3.25:                                              # he walks right, onto the line, in front of nothing
        u = ease((t - 2.55) / 0.70)
        return DX0 - 70, 0.0, lerp(DX0 + 10, RX0, u), "step", u
    if t < 3.50:                                              # it comes straight back along the floor, into his back
        u = ease((t - 3.25) / 0.25)
        return lerp(DX0 - 70, RX0 - 46, u), 0.0, RX0, "hit", u
    u = ease((t - 3.50) / 0.30)
    return RX0 - 46, 0.06, RX0 + 28 * u, "bump", u


def shot_B(t):
    rx, tilt, dx, phase, u = b_state(t)
    fd = F + 170
    def cast(k):
        heads = {}
        o, heads["robot"] = ps.robot(k, (rx, F + 140), arms=((-95, 0), (95, 0)), tilt=tilt)
        if phase == "pull":                                  # his hand on its arm, leaning back, hauling
            pose = don_arms(dx, fd, right=o["hands"][0])
            o2, heads["don"] = ps.don(k, (dx, fd), pose, "confused", (1, 0), lean=-0.10 * u)
        elif phase in ("back", "step"):
            o2, heads["don"] = ps.don(k, (dx, fd), "vest", "smug", (1, 0.6) if phase == "step" else (1, 0))
        elif phase == "hit":
            o2, heads["don"] = ps.don(k, (dx, fd), "vest", "smug", (1, 0.6))
        else:
            o2, heads["don"] = ps.don(k, (dx, fd), "bump", "shock", (-1, 0), lean=0.30 * u)
        if phase == "hit":                                   # it rolls fast: speed lines behind it
            c = k.c; c.set_source_rgb(*INK); c.set_line_width(2.6); c.set_line_cap(1)
            for i in (-1, 0, 1):
                c.move_to(rx - 60, F + 70 + i * 18); c.line_to(rx - 30, F + 70 + i * 18); c.stroke()
        if phase in ("hit", "bump") and (phase == "bump" or u > 0.8):     # the impact
            c = k.c; c.set_source_rgb(*INK); c.set_line_width(3); c.set_line_cap(1)
            for i in (-1, 0, 1):
                c.move_to(rx + 22, F + 40 + i * 26); c.line_to(rx + 46, F + 34 + i * 30); c.stroke()
        return heads
    return ps.S("2.11", (ps.tape_x(140) - 110, F - 40, 1.15), ps.ROOM2S, cast)


# --- C: the office gag --------------------------------------------------------------------------------------------------
def shot_C(t):
    if t < 0.3:
        knee, pose, face, look = ease(t / 0.3), "balance", "neutral", (0.7, 1.0)
    elif t < 0.9:
        knee, pose, face, look = 1.0, "balance", "neutral", (0.7, 1.0)                 # held 0.6 s over his own line
    elif t < 1.2:
        knee, pose, face, look = 1 - ease((t - 0.9) / 0.3), "balance", "neutral", (-0.6, 0.2)
    elif t < 1.45:                                                                      # v2: the arms fold in, in between
        u = ease((t - 1.2) / 0.25)
        b, v = dp.POSES["balance"], dp.POSES["vest"]
        knee, pose, face, look = 0.0, tuple(lerp(p, q, u) for p, q in zip(b, v)), "neutral" if u < 0.5 else "smug", (-1, 0)
    else:
        knee, pose, face, look = 0.0, "vest", "smug", (-1, 0)                           # nothing happened
    def cast(k):
        heads = {}
        _, heads["don"] = ps.don(k, "don_line", pose, face, look, knee=knee) if knee > 0.01 else \
            ps.don(k, "don_line", pose, face, look)
        return heads
    return ps.S("5.4", [ "don"], ps.ROOM5, cast)


# --- D: 2.1, the tape rips toward the camera through the group (Tomas 24 Nov) -------------------------------------------
def tape_part(c, d):
    """the tape from the back wall to depth d (world units below the floor line), the set's own geometry."""
    import ps_set as pss_
    x0, x1 = pss_.LINE_X, pss_.LINE_X + 34
    L = lambda y: (x0 - 8.5) + (y - F) * ((x1 - 20) - (x0 - 8.5)) / (960 - F)
    R_ = lambda y: (x0 + 8.5) + (y - F) * ((x1 + 20) - (x0 + 8.5)) / (960 - F)
    y = F + d
    c.new_path(); c.move_to(L(F), F); c.line_to(R_(F), F); c.line_to(R_(y), y); c.line_to(L(y), y); c.close_path()
    c.set_source_rgb(*pss_.TAPE); c.fill_preserve(); c.set_source_rgb(0.30, 0.22, 0.02); c.set_line_width(2.4); c.stroke()


DD = 300                                                     # v1b: Don this far forward, so the floor between shows the rip


def d_state(t):
    """-> the tape's front (depth), Don's yank (0 arm up .. 1 down), and each one's hop (0..1) and step aside (0..1)."""
    yank = ease((t - 0.15) / 0.20)
    front = DD * ease((t - 0.25) / 0.45) if t > 0.25 else 0.0
    def hop(depth, t0=None):
        tc = 0.25 + 0.45 * 0.45 * depth / 60 if t0 is None else t0        # when the front reaches their feet
        u = (t - tc) / 0.30
        return (4 * u * (1 - u) if 0 < u < 1 else 0.0), ease(u)
    return front, yank, hop(40), hop(34), hop(44)


def shot_D(t):
    front, yank, (ph, pa), (mh, ma), (sh_, sa) = d_state(t)
    def cast(k):
        heads = {}
        c = k.c
        tape_part(c, front)
        _, heads["pam"] = ps.pam(k, (520 - 46 * pa, F + 40 - 34 * ph), "stand", "shock" if ph > 0 or pa > 0.5 else "neutral",
                                 (1, 0.4))
        _, heads["mom"] = ps.mom(k, "trio_mom", "folded", "unimpressed", (0, 0.6) if front > 30 else (-1, 0))   # stays on it
        _, heads["sofia"] = ps.sofia(k, (662 + 64 * sa, F + 44 - 46 * sh_), "hip_out", "smile" if sa < 0.2 else "smile",
                                     (-1, 0.4))
        x, f = ps.tape_x(DD) - 96, F + DD                     # v1b: beside the tape, not over it: the floor reads
        pose = (-8, 0, lerp(110, 40, yank), lerp(20, 60, yank))
        o, heads["don"] = ps.don(k, (x, f), pose, "confused" if yank < 1 else "grin", (1, -0.4), chin=1)
        hx, hy = o["hands"][1]
        if front > 2:                                        # the strip from the roll down to the tape's front
            fx_, fy_ = ps.tape_x(front), F + front
            for col, w in ((INK, 11), (pss.TAPE, 8)):
                c.set_source_rgb(*col); c.set_line_width(w); c.new_path(); c.move_to(hx, hy)
                c.curve_to(hx + 4, hy + 40, fx_ - 4, fy_ - 20, fx_, fy_); c.stroke()
            if 0.25 < t < 0.75:                              # it rips: speed lines behind the front, along the tape
                c.set_source_rgb(*INK); c.set_line_width(2.6); c.set_line_cap(1)
                for dx in (-30, 30):
                    c.move_to(ps.tape_x(front - 50) + dx, F + front - 50); c.line_to(fx_ + dx * 1.2, fy_ - 8); c.stroke()
        dp.tape_roll(k, hx, hy, ps.SC["don"] * 0.9, ang=0.2 + 0.6 * (1 - yank))
        return heads
    return ps.S("2.1", (520, 820, 1.0), dict(blind="torn", tape=False, mark=False), cast)


# --- E: 3.1 -> 3.2, the selfie: the arm telescopes up, Don swings into his pose, FLASH, the photo fills the screen ------
E_CAM = {}


def shot_E(t):
    if t < 0.80:
        sel = ease(t / 0.35)
        u = ease((t - 0.20) / 0.30)
        st, th = dp.POSES["stand"], dp.POSES["thumbs"]
        pose = "thumbs" if u >= 1 else tuple(lerp(p_, q_, u) for p_, q_ in zip(st, th))
        def cast(k):
            heads = {}
            _, heads["mom"] = ps.mom(k, "mom_tape", "folded", "unimpressed", (-1, 0))
            _, heads["don"] = ps.don(k, (ps.tape_x(140) - 190, F + 140), pose, "grin" if u > 0.5 else "neutral",
                                     (0, -0.3), chin=1 if u > 0.5 else 0)
            _, heads["robot"] = ps.robot(k, "rob_tape", selfie=max(sel, 0.01), arms=((-95, 0), (160, 0)))
            return heads
        if "cam" not in E_CAM:                              # the board's own 3.1 camera (framed on the arm fully up)
            ps.render([x for x in ps.SHOTS if x["id"] == "3.1"][0]); E_CAM["cam"] = ps._last_cam[0]
        return ps.S("3.1m", E_CAM["cam"], ps.ROOM3, cast)        # (not "3.1": render would shift it again)
    if t < 0.87:                                             # the FLASH: one white drawing
        def white(k):
            k.c.set_source_rgb(1, 1, 1); k.c.paint()
        return ps.S("3.2f", "screen", draw=white)
    a = 0.6 * (1 - ease((t - 0.87) / 0.4))
    def photo(k):
        ps.ins_photo(k, flash=False)
        if a > 0.01:
            k.c.set_source_rgba(1, 1, 1, a); k.c.paint()
    return ps.S("3.2", "screen", draw=photo)


# --- F: 5.6, Pam frozen on the stool in front; beyond her Sofía steps across the tape ----------------------------------
def shot_F(t):
    u = ease((t - 0.5) / 1.1)                                # 0.5-1.6 s: the walk across
    x0, x1 = ps.tape_x(60) - 70, ps.tape_x(60) + 50         # v1b: she stops just past the line, still in frame
    step = int(t * 5) % 2 if 0.5 < t < 1.6 else 1           # a step every 0.2 s
    def cast(k):
        heads = {}
        _, heads["sofia"] = ps.sofia(k, (lerp(x0, x1, u), F + 60), "walk" if step == 0 else "stand", "smile",
                                     (1, -0.1))
        return heads
    return ps.S("5.6", (ps.tape_x(60) - 90 + 20, F - 150, 1.6), ps.ROOM5, cast, fg=ps.fg_56,   # v1b: 85 px left, room
                story=["pam", "sofia"])                                                       # past the line


# --- G: 6.1, Don sincere in front; behind him Pam reaches across the line to her phone; nobody looks at him -------------
G_AT = {}


def shot_G(t):
    r = ease((t - 0.6) / 0.8)
    st, rc = pm.P_POSES["stand"], pm.P_POSES["reach"]
    def cast(k):
        heads = {}
        _, heads["mom"] = ps.mom(k, "mom_tape", "folded", "stern", (1, -0.6))
        o, heads["sofia"] = ps.sofia(k, (640, F + 40), "chest", "smile", (0.2, 0.6))
        hx, hy = o["hands"][0]
        ps.sp.cv_coo(k, hx + 4, hy + 40, 0.8)                # v2: lower, off her face (2 of 2 saw her face covered)
        pose = "reach" if r >= 1 else tuple(lerp(p_, q_, r) for p_, q_ in zip(st, rc))
        o, heads["pam"] = ps.pam(k, (ps.tape_x(55) - 40, F + 55), pose, "avert", (1, 0.6), mug=False)
        if "phone" not in G_AT:                              # where her full reach ends (as the board draws it)
            tmp = cairo.ImageSurface(cairo.FORMAT_RGB24, 4, 4)
            oo = pm.pam(Ctx(cairo.Context(tmp), 0), ps.tape_x(55) - 40, F + 55, ps.SC["pam"], "reach", "avert", (1, 0.6), mug=False)
            G_AT["phone"] = (oo["hands"][1][0] - 4, oo["hands"][1][1] - 10)
        pss.phone_close(k, *G_AT["phone"], 0.30)              # v3: standing, its lit screen to us (v2: "a blue glow", 2 of 2)       # the phone stays put; her hand comes to it
        return heads
    def fg(k):
        face = "smug" if t < 1.6 else "grin"
        o = dp.don(k, 170, 1150, 0.60 * 2.5, "vest", face, (0, 0), chin=1)
        return {"don": (o["head"][0], o["head"][1], ps.R["don"] * 0.60 * 2.5)}
    return ps.S("6.1", (580, F - 170, 1.30), ps.ROOM5, cast, fg=fg, story=["don", "sofia"])   # the board's camera (v4 shift)


# --- H: 2.10b -> 2.11 (review round 1): "BOTH." the arms open across the tape; then ONE push: he hauls it onto his side,
# it rolls straight back into him, he staggers (Tomas 24 Nov: one cycle of test B, 1.6 s) ----------------------------
def _board_cam(sid, part=None):
    """the board's own camera for a shot (its key frame's), so the test matches the approved board"""
    key = (sid, part)
    if key not in CAMS:
        sh = next(x for x in ps.SHOTS if x["id"] == sid)
        ps.PART[0], keep = part, ps.NO_SHIFT[0]
        ps.NO_SHIFT[0] = False
        st = list(ps.STEP_55); ps.STEP_55[:] = [1.0, "chest", 0.0, 0.0, 0.0]       # the board's key frame, not the test's drawing
        legs = ps.sp.ss.LEGS[0]; ps.sp.ss.LEGS[0] = None
        try:
            ps.render(sh)
        finally:
            ps.PART[0], ps.NO_SHIFT[0] = None, keep
            ps.STEP_55[:] = st
            ps.sp.ss.LEGS[0] = legs
        CAMS[key] = ps._last_cam[0]
    return CAMS[key]


CAMS = {}


def h_state(t):
    """2.11's one cycle, t from 0 to 1.6 -> robot x, tilt, Don x, phase, progress"""
    if t < 0.45:
        u = ease(t / 0.45)
        return lerp(RX0 - 150, DX0 - 70, u), -0.14, DX0 + 10 * u, "pull", u   # from inside the frame (v1: under the rail)
    if t < 0.65:
        return DX0 - 70, 0.0, DX0 + 10, "step", 1.0
    if t < 0.90:
        u = ease((t - 0.65) / 0.25)
        return lerp(DX0 - 70, DX0 - 34, u), 0.0, DX0 + 10, "hit", u
    u = ease(min(1.0, (t - 0.90) / 0.30))
    return DX0 - 34, 0.06, DX0 + 10 + 28 * u, "bump", u


def unlean(p, foot, a):
    """A world point into the frame of a person leaned by a (radians) about foot: aim the IK there and the leaned hand lands on p."""
    dx, dy = p[0] - foot[0], p[1] - foot[1]
    return (foot[0] + dx * math.cos(-a) - dy * math.sin(-a), foot[1] + dx * math.sin(-a) + dy * math.cos(-a))


def haul_arms():
    """v3 (round 2: 2 of 3 read 'the robot shoves him'): its near arm raised to his chest, so his hands reach out clear of
    his body; tilted toward him, being dragged."""
    return (((-125, 0), (95, 0)), -0.22) if VER["H"] >= 3 else (((-95, 0), (95, 0)), -0.14)


def rob_hand(o, rx, ry, tilt):
    """The robot's screen-left hand as drawn: the rig returns it untilted; it tilts about its wheel (x, feet)."""
    hx, hy = o["hands"][0]
    dx, dy = hx - rx, hy - ry
    return (rx + dx * math.cos(tilt) - dy * math.sin(tilt), ry + dx * math.sin(tilt) + dy * math.cos(tilt))


def _rob_at(dx, q):
    """v2: the robot along its haul path relative to Don at dx: q 0 = an arm's length out toward the tape, 1 = in front of him."""
    return dx + lerp(145, 40, q), F + lerp(150, 200, q)


def grip_q(dx, fd, lean):
    """v2 (lesson 263): the farthest point on the path where both of Don's leaned hands touch the robot's hand (gap < 4 px)."""
    key = (round(dx, 1), round(lean, 3), VER["H"])
    if key in GRIP:
        return GRIP[key]
    s_ = cairo.ImageSurface(cairo.FORMAT_ARGB32, 4, 4); k = Ctx(cairo.Context(s_), 0)
    arms, tilt = haul_arms()
    def touches(q):
        rp_ = _rob_at(dx, q)
        o, _ = ps.robot(k, rp_, arms=arms, tilt=tilt)
        hp = rob_hand(o, rp_[0], rp_[1], tilt) if VER["H"] >= 3 else o["hands"][0]
        tg = ((hp[0] - 6, hp[1]), (hp[0] + 6, hp[1]))
        pose = don_arms(dx, fd, left=unlean(tg[0], (dx, fd), lean), right=unlean(tg[1], (dx, fd), lean))
        o2, _ = ps.don(k, (dx, fd), pose, "confused", (1, 0), lean=lean)
        hs = [unlean(h, (dx, fd), -lean) for h in o2["hands"]]
        return max(math.hypot(hs[i][0] - tg[i][0], hs[i][1] - tg[i][1]) for i in (0, 1)) < 4
    lo = 0.0                                                 # v2: scan in from the far end (the gap is not monotonic: further in,
    while lo < 1.0 and not touches(min(1.0, lo + 0.025)):    # its hand passes his), then refine the first touch
        lo += 0.025
    hi = min(1.0, lo + 0.025)
    for _ in range(6):
        q = (lo + hi) / 2
        lo, hi = (lo, q) if touches(q) else (q, hi)
    GRIP[key] = hi
    return hi


GRIP = {}
H3_END = [None]                                             # v3: where the haul let go (the drag marks end there)
H2 = dict(haul=0.45, sail=0.62, back=0.78, hit=0.95, contact=1.08, end=1.6)   # v2 phases in 2.11's cycle (s)


def h2_state(t):
    """v2 (round 1: 'arms crossed, the robot rolls in', 0 of 3): Don backs off dragging it by its hand, both of his on it,
    leaning away; yanks and lets go; it sails past IN FRONT of him to his left, rolls back behind him, the contact frame
    (2 drawings, strokes, no flash, lesson 114), then the board's bump. -> dict(rx, ry, dx, lean, phase, u)"""
    P = H2
    if VER["H"] >= 4:                                        # v4 (Tomas, after 3 misread hauls, lesson 178): no haul. It opens
        if t < 0.40:                                         # on his side, Don smug (he thinks he won); it rolls back toward
            return dict(rx=DX0 - 110, ry=F + 140, dx=DX0 + 10, lean=0.0, phase="smug", u=t / 0.40)   # the tape, into him
        if t < 0.65:
            u = ease((t - 0.40) / 0.25)
            return dict(rx=lerp(DX0 - 110, DX0 - 34, u), ry=F + 140, dx=DX0 + 10, lean=0.0, phase="hit", u=u)
        if t < 0.78:
            return dict(rx=DX0 - 34, ry=F + 140, dx=DX0 + 14, lean=0.06, phase="contact", u=1.0)
        u = ease(min(1.0, (t - 0.78) / 0.30))
        return dict(rx=DX0 - 34, ry=F + 140, dx=DX0 + 10 + 28 * u, lean=0.30 * u, phase="bump", u=u)
    if t < P["haul"]:
        u = ease(t / P["haul"])
        dx, lean = lerp(DX0 + 30 - (15 if VER["H"] >= 3 else 0), DX0, u), lerp(-0.10, -0.28, u)
        q = grip_q(dx, F + 170, lean)
        rx, ry = _rob_at(dx, q)
        return dict(rx=rx, ry=ry, dx=dx, lean=lean, phase="haul", u=u)
    q_end = grip_q(DX0, F + 170, -0.28)
    rx0, ry0 = _rob_at(DX0, q_end)
    H3_END[0] = (rx0, ry0)
    if t < P["sail"]:
        u = ease((t - P["haul"]) / (P["sail"] - P["haul"]))
        return dict(rx=lerp(rx0, DX0 - 70, u), ry=lerp(ry0, F + 200, u), dx=DX0, lean=lerp(-0.28, 0.0, u), phase="sail", u=u)
    if t < P["back"]:
        u = ease((t - P["sail"]) / (P["back"] - P["sail"]))
        return dict(rx=DX0 - 70, ry=lerp(F + 200, F + 140, u), dx=DX0 + 10 * u, lean=0.0, phase="smug", u=u)
    if t < P["hit"]:
        u = ease((t - P["back"]) / (P["hit"] - P["back"]))
        return dict(rx=lerp(DX0 - 70, DX0 - 34, u), ry=F + 140, dx=DX0 + 10, lean=0.0, phase="hit", u=u)
    if t < P["contact"]:
        return dict(rx=DX0 - 34, ry=F + 140, dx=DX0 + 14, lean=0.06, phase="contact", u=1.0)
    u = ease(min(1.0, (t - P["contact"]) / 0.30))
    return dict(rx=DX0 - 34, ry=F + 140, dx=DX0 + 10 + 28 * u, lean=0.30 * u, phase="bump", u=u)


def shot_H2(t):
    st = h2_state(t)
    fd = F + 170
    def cast(k):
        heads = {}
        c = k.c
        ph, dx = st["phase"], st["dx"]
        front = ph in ("haul", "sail") or (ph == "smug" and st["ry"] > fd)
        harms, htilt = haul_arms()
        def rob():
            if ph == "haul":
                return ps.robot(k, (st["rx"], st["ry"]), arms=harms, tilt=htilt)
            if ph == "sail" and VER["H"] >= 3:               # the raised arm drops back as it sails
                return ps.robot(k, (st["rx"], st["ry"]), arms=((lerp(-125, -95, st["u"]), 0), (95, 0)),
                                tilt=lerp(htilt, 0.0, st["u"]))
            return ps.robot(k, (st["rx"], st["ry"]), arms=((-95, 0), (95, 0)),
                            tilt=(-0.14 if ph == "haul" else 0.06 if ph in ("contact", "bump") else 0.0))
        if VER["H"] == 3:                                    # v3: its wheel's two drag marks on the floor, from where the haul
            x0, y0 = _rob_at(DX0 + 15, grip_q(DX0 + 15, fd, -0.10))   # began to where it is (fixed once it is let go)
            x1, y1 = (st["rx"], st["ry"]) if ph == "haul" else H3_END[0]
            c.set_source_rgba(0.22, 0.18, 0.14, 0.55); c.set_line_cap(1); c.set_line_width(3.2)
            for o_ in (-5, 5):
                c.move_to(x0, y0 + o_ * 0.5 - 2); c.line_to(x1, y1 + o_ * 0.5 - 2); c.stroke()
        if ph == "haul":
            c.push_group(); o, _ = rob(); c.pop_group()      # its hand first, then Don's hands onto it
            hp = rob_hand(o, st["rx"], st["ry"], htilt) if VER["H"] >= 3 else o["hands"][0]
            pose = don_arms(dx, fd, left=unlean((hp[0] - 6, hp[1]), (dx, fd), st["lean"]),
                            right=unlean((hp[0] + 6, hp[1]), (dx, fd), st["lean"]))
            _, heads["don"] = ps.don(k, (dx, fd), pose, "confused", (1, 0), lean=st["lean"])
            _, heads["robot"] = rob()
            c.set_source_rgb(*INK); c.set_line_cap(1); c.set_line_width(2.4)   # effort strokes behind his back
            for i in (-1, 0, 1):
                c.move_to(dx - 52, F + 40 + i * 22); c.line_to(dx - 70, F + 36 + i * 24); c.stroke()
            return heads
        if front:
            if ph == "sail":                                 # its speed lines, trailing right, behind Don (not over his legs)
                c.set_source_rgb(*INK); c.set_line_cap(1); c.set_line_width(2.6)
                for i in (-1, 0, 1):
                    c.move_to(st["rx"] + 50, st["ry"] - 70 + i * 18); c.line_to(st["rx"] + 90, st["ry"] - 70 + i * 18); c.stroke()
            o2, heads["don"] = ps.don(k, (dx, fd), "vest", "smug" if ph == "smug" else "confused", (-1, 0), lean=st["lean"])
            _, heads["robot"] = rob()
        else:
            _, heads["robot"] = rob()
            c.set_source_rgb(*INK); c.set_line_cap(1)        # v2: strokes and the burst under Don, so none crosses his body
            if ph == "contact":                              # the contact frame: a small jagged burst at the touch, no flash
                cx, cy = dx - 30, F + 52
                pts = [(cx + (30 if j % 2 == 0 else 14) * math.cos(j * math.pi / 7), cy + (30 if j % 2 == 0 else 14) *
                        math.sin(j * math.pi / 7)) for j in range(14)]
                c.move_to(*pts[0])
                for p_ in pts[1:]:
                    c.line_to(*p_)
                c.close_path(); c.set_source_rgb(1.0, 0.84, 0.25); c.fill_preserve()
                c.set_source_rgb(*INK); c.set_line_width(2.4); c.stroke()
            if ph == "bump":
                c.set_line_width(3)
                for i in (-1, 0, 1):
                    c.move_to(st["rx"] + 22, F + 40 + i * 26); c.line_to(st["rx"] + 46, F + 34 + i * 30); c.stroke()
            if ph in ("smug", "hit"):
                o2, heads["don"] = ps.don(k, (dx, fd), "vest", "smug", (1, 0.6))
            elif ph == "contact":
                o2, heads["don"] = ps.don(k, (dx, fd), "vest", "shock", (-1, 0), lean=st["lean"])
            else:
                o2, heads["don"] = ps.don(k, (dx, fd), "bump", "shock", (-1, 0), lean=st["lean"])
        c.set_source_rgb(*INK); c.set_line_cap(1)
        if ph == "hit":
            c.set_line_width(2.6)
            for i in (-1, 0, 1):
                c.move_to(st["rx"] - 60, F + 70 + i * 18); c.line_to(st["rx"] - 30, F + 70 + i * 18); c.stroke()
        return heads
    c0 = _board_cam("2.11")
    off = -100 if VER["H"] >= 4 else -70                     # v2-3: -100 put its face under the rail at the haul's start;
    return ps.S("2.11", (c0[0] + off, c0[1], c0[2]), ps.ROOM2S, cast)   # v4 (no haul): -100, its HR badge whole at the left


def shot_H(t):
    if t < 0.8:                                              # 2.10b: its arms open from its sides across the tape
        u = ease(min(1.0, t / 0.35))
        arms = ((lerp(-8, -95, u), 0), (lerp(8, 95, u), 0))
        def cast(k):
            heads = {}
            _, heads["don"] = ps.don(k, (ps.tape_x(140) - 190, F + 140), "vest", "smug", (-1, 0), chin=1)
            _, heads["robot"] = ps.robot(k, "rob_tape", arms=arms, tilt=0.10 * u)
            return heads
        return ps.S("2.10", _board_cam("2.10", 1), ps.ROOM2S, cast)
    if VER["H"] >= 2:
        return shot_H2(t - 0.8)
    rx, tilt, dx, phase, u = h_state(t - 0.8)
    fd = F + 170
    def cast(k):
        heads = {}
        o, heads["robot"] = ps.robot(k, (rx, F + 140), arms=((-95, 0), (95, 0)), tilt=tilt)
        if phase == "pull":
            pose = don_arms(dx, fd, right=o["hands"][0])
            o2, heads["don"] = ps.don(k, (dx, fd), pose, "confused", (1, 0), lean=-0.10 * u)
        elif phase in ("step", "hit"):
            o2, heads["don"] = ps.don(k, (dx, fd), "vest", "smug", (1, 0.6))
        else:
            o2, heads["don"] = ps.don(k, (dx, fd), "bump", "shock", (-1, 0), lean=0.30 * u)
        c = k.c; c.set_source_rgb(*INK); c.set_line_cap(1)
        if phase == "hit":
            c.set_line_width(2.6)
            for i in (-1, 0, 1):
                c.move_to(rx - 60, F + 70 + i * 18); c.line_to(rx - 30, F + 70 + i * 18); c.stroke()
        if phase == "bump" or (phase == "hit" and u > 0.8):
            c.set_line_width(3)
            for i in (-1, 0, 1):
                c.move_to(rx + 22, F + 40 + i * 26); c.line_to(rx + 46, F + 34 + i * 30); c.stroke()
        return heads
    c0 = _board_cam("2.11")                                  # the board's 2.11 camera, 100 left: room for the haul past him
    return ps.S("2.11", (c0[0] - 100, c0[1], c0[2]), ps.ROOM2S, cast)   # (v1 rolled it off the frame's edge, HR cut)


# --- I: 6.1b -> 1.1, the loop's seam (Office Noir 1's startle): the buzz 2 drawings, the eyes round in 1, the hair springs
# with an overshoot over 3, the hold; the cut into frame 0 (1.1) and its first 0.4 s ---------------------------------
SPRING_AT = {2: 1.35, 3: 0.80, 4: 1.12}


def shot_I(t):
    i = int(round(t * DRAW))
    if t < 0.6:
        base = next(x for x in ps.SHOTS if x["id"] == "6.1b")
        if i < 2:
            return dict(base, fg=ps.fg_61)                    # the buzz: still smug, eyes shut
        ps.SPRING_61B[0] = SPRING_AT.get(i, 1.0)
        return base
    ps.SPRING_61B[0] = 1.0
    return next(x for x in ps.SHOTS if x["id"] == "1.1")


# --- J: 4.2, his fingertip comes in from the frame's edge and lands on her heel; the print after ---------------------
def shot_J(t):
    ps.FINGER_42[0] = ease(min(1.0, t / 0.7))
    return next(x for x in ps.SHOTS if x["id"] == "4.2")


# --- K: 5.5, Sofía's step onto the tape with the offer ------------------------------------------------------------------
K_STEPS = ((0.00, 0.34, 1, -60, -30), (0.34, 0.68, 0, -60, 0), (0.68, 0.98, 1, -30, 0))   # v2 (lesson 39): (from, to, leg,
K_LIFT, K_BOB = 16.0, 5.0                                   # v3: bob 3 -> 5 (2 of 3: "the upper body barely moves")
K_LEAN, K_SWING = 4.0, 18.0                                 # v3: lean into the walk (deg), the free arm's swing (deg, elbow kept)                                   # world x from, to): one foot swings while the other stays put; 1 = lead


K_ARM = [0.0, 0.0]                                          # v3: this drawing's arm swing and lean (set by k_gait)


def k_gait(t):
    """v2 (K read as a glide, 0 of 3): three steps onto the tape, each foot planted in world x between its swings;
    the body rides midway between the feet and rises a little at each mid-swing. Returns (body dx, body dy, legs)."""
    f, lift, dy = [-60.0, -60.0], [0.0, 0.0], 0.0
    for a, b, leg, x0, x1 in K_STEPS:
        if t >= b:
            f[leg] = x1
        elif t > a:
            p_ = (t - a) / (b - a)
            f[leg] = lerp(x0, x1, ease(p_))
            lift[leg] = K_LIFT * math.sin(math.pi * p_)
            dy = -K_BOB * math.sin(math.pi * p_)
    bx = (f[0] + f[1]) / 2
    sw = 0.0                                                # v3: the free (screen-right) arm swings against the moving leg
    for a, b, leg, x0, x1 in K_STEPS:
        if a < t < b:
            sw = (1 if leg == 0 else -1) * math.sin(math.pi * (t - a) / (b - a))
    K_ARM[0] = sw * K_SWING
    K_ARM[1] = K_LEAN * min(1.0, t / 0.12) * (1 - ease(max(0.0, min(1.0, (t - 0.80) / 0.25))))
    s_ = ps.SC["sofia"]
    return bx, dy, (((f[0] - bx) / s_, lift[0] + dy / s_), ((f[1] - bx) / s_, lift[1] + dy / s_))   # the rise is the
                                                                                    # standing leg straightening: its sole stays down


def shot_K(t):
    if VER["K"] >= 2:
        bx, dy, legs = k_gait(t)
        ps.sp.ss.LEGS[0] = legs
        if VER["K"] >= 3:
            ch = ps.sp.sbc.POSES["chest"]
            ps.sp.sbc.POSES["chest_step"] = (ch[0], ch[1], ch[2] + K_ARM[0], ch[3])
            ps.STEP_55[:] = [1.0, "chest_step", bx, dy, K_ARM[1]]
        else:
            ps.STEP_55[:] = [1.0, "chest", bx, dy, 0.0]
        return dict(next(x for x in ps.SHOTS if x["id"] == "5.5"), cam=_board_cam("5.5"))
    u = ease(min(1.0, t / 0.7))
    ps.STEP_55[0], ps.STEP_55[1] = u, "chest"               # v1: "walk" lowered the CV into the caption zone (11 drawings)
    return dict(next(x for x in ps.SHOTS if x["id"] == "5.5"), cam=_board_cam("5.5"))   # the board's camera, not her first step


TESTS = {"A": (shot_A, 1.8), "B": (shot_B, 4.0), "C": (shot_C, 1.7), "D": (shot_D, 1.6), "E": (shot_E, 2.0),
         "F": (shot_F, 2.4), "G": (shot_G, 3.0), "H": (shot_H, 2.4), "I": (shot_I, 1.0), "J": (shot_J, 1.2),
         "K": (shot_K, 1.2)}
CAM_OF = {}
NO_SHIFT_TESTS = ("H", "K")
FAULTS = {}
VER = {"D": 2, "E": 1, "F": 1, "G": 3, "H": 4, "I": 1, "J": 1, "K": 3}   # H-K: review round 1 (24 Nov)                       # v4 (24 Nov): the new tests start at v1; A-C stay v3


def render_test(name):
    fn, dur = TESTS[name]
    ps.FIX_V4[0] = name in VER                               # the new tests (D-G) are staged as board v3; A-C as before
    ps.pss.NO_DOOR_CONFETTI[0] = ps.rp.SUN_UP[0] = name in VER   # A-C were drawn before the v4 set fixes (md5)
    d = "/tmp/ps_motion_%s" % name
    os.makedirs(d, exist_ok=True)
    for f_ in os.listdir(d):
        os.remove(os.path.join(d, f_))
    n = int(round(dur * DRAW))
    frames = []
    cam = None
    for i in range(n):
        t = i / DRAW
        sh = fn(t)
        if isinstance(sh["cam"], list):                       # one camera for the whole test, from its first drawing
            if cam is None:
                ps.NO_SHIFT[0] = False
                ps.render(sh)
                cam = ps._last_cam[0]
            sh = dict(sh, cam=cam)
        ps.NO_SHIFT[0] = name in NO_SHIFT_TESTS               # its camera is already the board's, shift included
        if name in VER:                                      # v4: the series' checks on every drawing of the new tests
            import ps_checks as pc
            pc.install_scene(ps); pc.begin()
            surf, msgs = ps.render(sh)
            msgs = [m for m in msgs if not m.startswith("SIGN partly covered: 'SHRED'")]   # SHRED_OK: passing in front of it
            if name == "H":                                  # the floor's DON under his shoes as he is hauled and staggers
                msgs = [m for m in msgs if not m.startswith("SIGN partly covered: 'DON'")]
            msgs += pc.frame_checks(ps, ps.LAST[0])
            for m in msgs:
                FAULTS.setdefault(name, {}).setdefault(m.split(" at ")[0].split(" (")[0], []).append(i)
        else:
            surf, _ = ps.render(sh)
        p = os.path.join(d, "%03d.png" % i); surf.write_to_png(p); frames.append((t, p))
    ps.sp.ss.LEGS[0] = None; ps.STEP_55[:] = [1.0, "chest", 0.0, 0.0, 0.0]   # v2: back to the board's standing Sofia
    lst = os.path.join(d, "list.txt")
    with open(lst, "w") as f:
        for t, p in frames:
            f.write("file '%s'\nduration %.4f\n" % (p, 1.0 / DRAW))
        f.write("file '%s'\n" % frames[-1][1])
    mp4 = os.path.join(OUT, "ps_motion_%s_v%d.mp4" % (name, VER.get(name, 3)))
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-vf",
                           "fps=%d,format=yuv420p" % FPS, "-c:v", "libx264", "-crf", "20", "-preset", "veryfast", mp4])
    strip(name, frames, dur)
    print("wrote", mp4)


def strip(name, frames, dur):
    """the 8 fps strip, numbered, a time stamp per tile, at 216 px tiles."""
    picks = [frames[min(len(frames) - 1, int(round(j / 8 * DRAW)))] for j in range(int(dur * 8) + 1)]
    tw, th, cols = 216, 384, 8
    rows = (len(picks) + cols - 1) // cols
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, 20 + cols * (tw + 12), 20 + rows * (th + 30))
    c = cairo.Context(s); c.set_source_rgb(0.15, 0.15, 0.16); c.paint()
    for j, (t, p) in enumerate(picks):
        x = 20 + (j % cols) * (tw + 12); y = 20 + (j // cols) * (th + 30)
        im = cairo.ImageSurface.create_from_png(p)
        c.save(); c.translate(x, y); c.scale(tw / 540, tw / 540); c.set_source_surface(im, 0, 0); c.paint(); c.restore()
        c.set_source_rgb(1, 1, 1); c.select_font_face("Inter", 0, 1); c.set_font_size(13)
        c.move_to(x, y + th + 18); c.show_text("%d   %.2f s" % (j + 1, j / 8))
    o = os.path.join(OUT, "ps_motion_%s_strip_v%d.png" % (name, VER.get(name, 3)))
    s.write_to_png(o)


if __name__ == "__main__":
    for n in (sys.argv[1:] or ["A", "B", "C"]):              # v4: D (2.1), E (3.1-3.2), F (5.6), G (6.1) by name
        render_test(n)
        if n in VER:
            print(n, "checks:", "pass" if not FAULTS.get(n) else {m: len(v) for m, v in FAULTS[n].items()})
