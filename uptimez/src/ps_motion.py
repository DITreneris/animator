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


def shot_A(t):
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
        o2, heads["robot"] = ps.robot(k, (rx + 12, rf), arms=(arm, (8, 0)), visor="sun" if n > 0.5 else None,
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
            c.set_source_rgba(0.05, 0.05, 0.10, 0.32 * n); c.rectangle(-400, 0, 1800, 1200); c.fill()
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


TESTS = {"A": (shot_A, 1.8), "B": (shot_B, 4.0), "C": (shot_C, 1.7), "D": (shot_D, 1.6), "E": (shot_E, 2.0),
         "F": (shot_F, 2.4), "G": (shot_G, 3.0)}
CAM_OF = {}
FAULTS = {}
VER = {"D": 2, "E": 1, "F": 1, "G": 3}                       # v4 (24 Nov): the new tests start at v1; A-C stay v3


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
                ps.render(sh)
                cam = ps._last_cam[0]
            sh = dict(sh, cam=cam)
        if name in VER:                                      # v4: the series' checks on every drawing of the new tests
            import ps_checks as pc
            pc.install_scene(ps); pc.begin()
            surf, msgs = ps.render(sh)
            msgs = [m for m in msgs if not m.startswith("SIGN partly covered: 'SHRED'")]   # SHRED_OK: passing in front of it
            msgs += pc.frame_checks(ps, ps.LAST[0])
            for m in msgs:
                FAULTS.setdefault(name, {}).setdefault(m.split(" at ")[0].split(" (")[0], []).append(i)
        else:
            surf, _ = ps.render(sh)
        p = os.path.join(d, "%03d.png" % i); surf.write_to_png(p); frames.append((t, p))
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
