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


TESTS = {"A": (shot_A, 1.8), "B": (shot_B, 4.0), "C": (shot_C, 1.7)}
CAM_OF = {}


def render_test(name):
    fn, dur = TESTS[name]
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
        surf, _ = ps.render(sh)
        p = os.path.join(d, "%03d.png" % i); surf.write_to_png(p); frames.append((t, p))
    lst = os.path.join(d, "list.txt")
    with open(lst, "w") as f:
        for t, p in frames:
            f.write("file '%s'\nduration %.4f\n" % (p, 1.0 / DRAW))
        f.write("file '%s'\n" % frames[-1][1])
    mp4 = os.path.join(OUT, "ps_motion_%s_v3.mp4" % name)
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
    o = os.path.join(OUT, "ps_motion_%s_strip_v3.png" % name)
    s.write_to_png(o)


if __name__ == "__main__":
    for n in (sys.argv[1:] or ["A", "B", "C"]):
        render_test(n)
