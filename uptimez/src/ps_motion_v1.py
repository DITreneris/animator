"""PICK A SIDE (episode 14): stage 6, the motion tests (series/production-process.md), after the board's second cold test
(23 Nov: what the stills can't carry). Each test is drawn by ps_scenes' own rigs, set and cameras, at the film's rate:
15 drawings a second on a 30 fps camera, 540 x 960. For the cold viewers: an 8 fps strip of each.
  A  1.1  the blinds tug of war, frame 0 to 0:01.8: down, up, down, up, each faster (the 0:01 physical joke)
  B  2.11 Don pulls the robot off the tape onto his side, it rolls back (1.4 s); again (1.0 s); the third time he steps
          into its path and it bumps him (3 of 3 cold viewers read the still as "the robot trips Don")
  C  5.4  the office gag: a knee up, the foot hovering over the line 0.6 s, back down, the vest straightened
          (2 of 3 read the still as "Don trips over the line")
  python3 ps_motion.py [A B C]  ->  ../pick-a-side/ps_motion_<X>_v1.mp4 and ps_motion_<X>_strip_v1.png"""
import os
import sys
import subprocess
import cairo
import ps_scenes as ps
import ps_set as pss
import don_ps as dp
from kit import Ctx

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
    def cast(k):
        heads = {}
        a1 = lerp(-168, -150, u / 0.92); a2 = lerp(6, -20, u / 0.92)            # his hand rides the cord down
        _, heads["don"] = ps.don(k, "don_cord", (a1, a2, 8, 0), "squint" if who != "don" else "smug", (-0.4, -0.6))
        up = who == "robot"                                                      # its hand on its cord when it pulls
        arms = ((-8, 0), (lerp(172, 150, 1 - u / 0.92), lerp(-4, 20, 1 - u / 0.92))) if up else ((-8, 0), (8, 0))
        _, heads["robot"] = ps.robot(k, "rob_cord", arms=arms, visor="sun" if u > 0.45 else None)
        if u > 0:
            k.c.set_source_rgba(0.05, 0.05, 0.10, 0.32 * u / 0.92); k.c.rectangle(-400, 0, 1800, 1200); k.c.fill()
        return heads
    room = dict(blind="down", u=u, dim=False) if u > 0.01 else dict(blind="up")
    return ps.S("1.1", ps.S2, room, cast)


# --- B: the pulls and the bump ------------------------------------------------------------------------------------------
RX0 = ps.tape_x(140) - 10                                    # the robot balanced on the tape
DX0 = ps.tape_x(140) - 195                                   # Don, on his side
PULLS = [(0.0, 0.35, 1.40), (1.40, 1.65, 2.40)]              # (pull from, pulled by, back on the line at)


def b_state(t):
    """-> robot x, its tilt, Don x, Don pose, Don's lean, phase."""
    for p0, p1, p2 in PULLS:
        if p0 <= t < p1:                                      # he hauls it by the arm onto his side
            u = ease((t - p0) / (p1 - p0))
            return lerp(RX0, RX0 - 70, u), -0.10 * u, DX0, "push", 0.0, "pull"
        if p1 <= t < p2:                                      # let go: it rolls back onto the line, arms out, wobbling
            u = ease((t - p1) / (p2 - p1))
            return lerp(RX0 - 70, RX0, u), 0.12 * (1 - u) * (1 if int(t * 8) % 2 else -1), DX0, "vest", 0.0, "back"
    if t < 2.62:                                              # the third pull
        u = ease((t - 2.40) / 0.22)
        return lerp(RX0, RX0 - 70, u), -0.10, DX0, "push", 0.0, "pull"
    if t < 2.85:                                              # he steps into the gap, admiring his line; it comes back at once
        u = ease((t - 2.62) / 0.23)
        return lerp(RX0 - 70, RX0 - 30, u), 0.0, lerp(DX0, RX0 + 30, u), "vest", 0.0, "step"
    u = ease((t - 2.85) / 0.25)                               # BONK: he tips away
    return RX0 - 30, 0.06, RX0 + 30 + 26 * u, "bump", 0.30 * u, "bump"


def shot_B(t):
    rx, tilt, dx, pose, lean, phase = b_state(t)
    def cast(k):
        heads = {}
        o, heads["robot"] = ps.robot(k, (rx, F + 140), arms=((-95, 0), (95, 0)), tilt=tilt)
        face = {"pull": "confused", "back": "smug", "step": "smug", "bump": "shock"}[phase]
        o, heads["don"] = ps.don(k, (dx, F + 170), pose, face, (1, 0) if phase != "step" else (-1, 0.6), lean=lean)
        if phase == "bump":                                  # the impact lines
            c = k.c; c.set_source_rgb(0.1, 0.1, 0.1); c.set_line_width(3); c.set_line_cap(1)
            for i in (-1, 0, 1):
                c.move_to(rx + 20, F + 60 + i * 26); c.line_to(rx + 44, F + 54 + i * 30); c.stroke()
        return heads
    return ps.S("2.11", (ps.tape_x(140) - 60, F - 40, 1.30), ps.ROOM2S, cast)


# --- C: the office gag --------------------------------------------------------------------------------------------------
def shot_C(t):
    if t < 0.3:
        knee, pose, face, look = ease(t / 0.3), "balance", "neutral", (0.7, 1.0)
    elif t < 0.9:
        knee, pose, face, look = 1.0, "balance", "neutral", (0.7, 1.0)                 # held 0.6 s over his own line
    elif t < 1.2:
        knee, pose, face, look = 1 - ease((t - 0.9) / 0.3), "balance", "neutral", (-0.6, 0.2)
    else:
        knee, pose, face, look = 0.0, "vest", "smug", (-1, 0)                           # nothing happened
    def cast(k):
        heads = {}
        _, heads["don"] = ps.don(k, "don_line", pose, face, look, knee=knee) if knee > 0.01 else \
            ps.don(k, "don_line", pose, face, look)
        return heads
    return ps.S("5.4", [ "don"], ps.ROOM5, cast)


TESTS = {"A": (shot_A, 1.8), "B": (shot_B, 3.6), "C": (shot_C, 1.6)}
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
    mp4 = os.path.join(OUT, "ps_motion_%s_v1.mp4" % name)
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
    o = os.path.join(OUT, "ps_motion_%s_strip_v1.png" % name)
    s.write_to_png(o)


if __name__ == "__main__":
    for n in (sys.argv[1:] or ["A", "B", "C"]):
        render_test(n)
