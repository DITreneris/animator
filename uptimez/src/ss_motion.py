"""v2 (ss_motion_v1.py = v1, kept): take A chosen; shot 14 now lets Pam be sad, quietly: a blank stare at the
barred tag, the twitch, then the hurt face (brows up in the middle, lids down, a small down-turned mouth) and a
small sink. No tears: 15 returns to incredulous, 16 to attempt two. Writes ss_motion_v2_A.mp4.
v1: The redaction motion test for "Secret Santa": shots 11-14, silent, 540x960, 30 fps on a 12 fps drawing grid.
11 the sender (an ordinary hit), 12 the recipient from Pam's eyes (heavier, then a 0.4 s beat), 13 the hover over
the kiss, then the hit, 14 Pam's silent ECU (a twitch, then nothing). Two takes of shot 13:
  A: the big THUNK. (biggest impact, the biggest shake)
  B: a small, polite tap (it lowers the stamp gently, a tiny touch, no shake).
Writes ss_motion_v1_A.mp4, ss_motion_v1_B.mp4 and ss_motion_v1_AB.mp4 (side by side, labelled)."""
import os
import sys
import math
import random
import subprocess
import cairo
import kit
import pam_ss as ps
import robot_ss as rs
import props_ss as props
import ss_set_sheet as sss
from kit import Ctx, INK
from charsheets import corp

FPS, GRID = 30, 12
U = 540 / 98.0
SHOTS = [("11", 0.9), ("12", 1.7), ("13", 2.3), ("14", 1.2)]


def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def fall(x):
    x = max(0.0, min(1.0, x))
    return x * x


def shake(t, t_hit, amp, dur=0.25, seed=1):
    if t < t_hit or t > t_hit + dur or amp == 0:
        return 0.0, 0.0
    r = random.Random(int((t - t_hit) * GRID) + seed * 100)
    d = 1 - (t - t_hit) / dur
    return (r.uniform(-1, 1) * amp * d, r.uniform(-1, 1) * amp * d)


def stamp_track(t, t_hit, lift_hi, up_after=0.25, gentle=False):
    """Lift of the stamp above its bar: comes down to 0 at t_hit, rests, then rises again."""
    if t < t_hit:
        k = (t_hit - t) / (0.4 if gentle else 0.22)
        return lift_hi * (ease(min(1, k)) if gentle else fall(min(1, k)))
    if t < t_hit + up_after:
        return 0.0
    return lift_hi * ease((t - t_hit - up_after) / 0.3)


def tag(k, x, y, s, bars, rot=0.0):
    sss.tag(k, x, y, s, bars, rot=rot)


BC = {"from": (3, 8), "to": (1, -10), "kiss": (23, 8)}


def shot11(k, t):
    c = k.c
    t_hit = 0.36
    dx, dy = shake(t, t_hit, 1.2, seed=11)
    c.translate(dx, dy)
    sss.table_top(c, 40)
    hit = t >= t_hit
    tag(k, 49, 112, 2.0, ("from",) if hit else ())
    bx, by = 49 + BC["from"][0] * 2.0, 112 + BC["from"][1] * 2.0
    lift = stamp_track(t, t_hit, 70) + 6
    rs.stamp_prop(k, bx, by - lift, 0.84, "down" if lift < 7 else "up", 0.0, 7)
    if hit and t < t_hit + 0.18:
        rs.impact_lines(c, bx, by, 1, 0.84)


def shot12(k, t):                       # high angle, Pam's eyes: the stamp from the top, the bar on the name
    import pam_mf as pm
    c = k.c
    t_hit = 0.45
    dx, dy = shake(t, t_hit, 2.4, 0.3, seed=12)
    c.translate(dx, dy)
    c.set_source_rgb(0.97, 0.97, 0.95); c.rectangle(-10, -10, 120, 200); c.fill()
    c.set_source_rgb(0.86, 0.86, 0.83); c.set_line_width(1.2)
    for gx in range(-20, 120, 16):
        c.move_to(gx, 0); c.line_to(49 + (gx - 49) * 1.4, 174); c.stroke()
    hit = t >= t_hit
    c.save(); c.translate(49, 92); c.scale(1, 0.82); c.translate(-49, -92)
    tag(k, 49, 92, 2.4, ("from", "to") if hit else ("from",), rot=0.08)
    c.restore()
    for sx in (-1, 1):
        cx_ = 49 + sx * 34
        kit.cut(k, [(cx_ - 16, 180), (cx_ + 16, 180), (cx_ + 12, 150), (cx_ - 12, 150)], pm.PURPLE, shadow=False, lw=2)
        kit.ellipse(k, cx_ - sx * 2, 146 + (1.5 if hit and t < t_hit + 0.2 else 0), 11, 9, pm.SKIN, 6,
                    shadow=False, lw=2)
    lift = stamp_track(t, t_hit, 80, up_after=0.35)
    sc = 1.1 + 0.5 * (lift / 80)                       # from above, it grows as it comes up toward the camera
    c.save(); c.translate(50, 66 - lift * 0.55); c.scale(1, 0.62)
    rs.stamp_prop(k, 0, 0, sc, "up", 0.0, 7)
    c.restore()
    if hit and t < t_hit + 0.24:
        rs.impact_lines(c, 50, 70, 2, 1.1)


def shot13(k, t, take="A"):
    c = k.c
    t_hit = 1.55 if take == "A" else 1.75
    amp = 3.6 if take == "A" else 0.0
    dx, dy = shake(t, t_hit, amp, 0.35, seed=13)
    c.translate(dx, dy)
    sss.table_top(c, 70)
    hit = t >= t_hit
    tx = 36                                              # the kiss well inside the frame, the robot soft at left
    tag(k, tx, 128, 1.8, ("from", "to", "kiss") if hit else ("from", "to"))
    bx, by = tx + BC["kiss"][0] * 1.8, 128 + BC["kiss"][1] * 1.8
    if take == "A":
        if t < 1.25:                                     # the hover: hanging still, a breath of drift
            lift = 34 + 1.2 * math.sin(t * 5)
        else:
            lift = stamp_track(t, t_hit, 34, up_after=0.4)
    else:
        if t < 1.25:
            lift = 34 + 1.2 * math.sin(t * 5)
        elif t < t_hit:
            lift = 34 * (1 - ease((t - 1.25) / (t_hit - 1.25)))   # lowered gently, all the way
        elif t < t_hit + 0.3:
            lift = 0.0
        else:
            lift = 20 * ease((t - t_hit - 0.3) / 0.3)
    rs.stamp_prop(k, bx, by - lift - 4, 1.1 * 0.84, "down" if lift < 2 and take == "A" else "up", 0.0, 9)
    if hit and t < t_hit + 0.3:
        rs.impact_lines(c, bx, by, 3 if take == "A" else 1, 0.84 if take == "A" else 0.4)
    kx, ky = bx, by - lift - 4 - 46 * 0.92              # the knob, where its hand holds the stamp
    def fg(lc):                                          # over its shoulder: the back of its head, its arm to the knob
        import waiter_kit as w
        k2 = Ctx(lc, 0)
        kit.ellipse(k2, -4, 18, 42, 38, w.BODY, 3, shadow=False, lw=2.4)
        lc.set_source_rgb(*INK); lc.set_line_width(11); lc.set_line_cap(1)
        lc.move_to(14, 40); lc.line_to(kx - 6, ky - 2); lc.stroke()
        lc.set_source_rgb(0.60, 0.62, 0.66); lc.set_line_width(7.5)
        lc.move_to(14, 40); lc.line_to(kx - 6, ky - 2); lc.stroke()
    props.soft(c, fg, 1.6)
    kit.ellipse(k, kx - 3, ky, 6.5, 6.5, (0.60, 0.62, 0.66), 41, shadow=False, lw=1.6)   # its hand, sharp, on the knob


def shot14(k, t):                       # Pam's silent ECU: eyes on the barred tag; a twitch at 0.4 s, then nothing
    c = k.c
    c.set_source_rgb(*kit.WALL); c.rectangle(0, 0, 98, 174); c.fill()
    face = "incredulous" if 0.42 <= t < 0.58 else "pressed"
    sink = 0.0
    if SAD14 and t >= 0.58:                              # v2: then the hurt lands, and she sinks a little
        face = "hurt"
        sink = 3.0 * ease((t - 0.58) / 0.3)
    ps.pam(k, 49, 78 + sink - ps.HY * 1.5, 1.5, "stand", face, look=(0.1, 1.0), glasses="chain")
    sss.tag(k, 50, 166, 1.3, ("from", "to", "kiss"), rot=0.03)


SAD14 = False


def render(take, outdir):
    os.makedirs(outdir, exist_ok=True)
    n = 0
    for name, dur in SHOTS:
        frames = int(round(dur * FPS))
        for f in range(frames):
            t = math.floor(f / FPS * GRID) / GRID              # the 12 fps drawing grid
            surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)
            c = cairo.Context(surf)
            c.set_source_rgb(*kit.WALL); c.paint()
            k = Ctx(c, 0)
            c.scale(U, U)
            {"11": shot11, "12": shot12, "14": shot14}.get(name, lambda k_, t_: shot13(k_, t_, take))(k, t)
            surf.write_to_png(os.path.join(outdir, "f%04d.png" % n))
            n += 1
    return n


def encode(outdir, out):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(outdir, "f%04d.png"),
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", out], check=True)


if __name__ == "__main__" and sys.argv[1:] == ["v2"]:
    rs.BIG_ICON = True
    SAD14 = True
    subprocess.run(["rm", "-rf", "/tmp/ssmt2_A"])
    render("A", "/tmp/ssmt2_A")
    encode("/tmp/ssmt2_A", "ss_motion_v2_A.mp4")
elif __name__ == "__main__":
    rs.BIG_ICON = True
    for take in ("A", "B"):
        d = "/tmp/ssmt_" + take
        subprocess.run(["rm", "-rf", d])
        render(take, d)
        encode(d, "ss_motion_v1_%s.mp4" % take)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "ss_motion_v1_A.mp4", "-i", "ss_motion_v1_B.mp4",
                    "-filter_complex",
                    "[0]pad=iw:ih+60:0:60:white,drawtext=text='A  THUNK.':fontsize=34:x=20:y=14:fontcolor=black[a];"
                    "[1]pad=iw:ih+60:0:60:white,drawtext=text='B  polite tap':fontsize=34:x=20:y=14:fontcolor=black[b];"
                    "[a][b]hstack", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
                    "ss_motion_v1_AB.mp4"], check=True)
