"""OFFICE NOIR 3: a moving rough of beat 05's opening (5.1a, 5.1b, 5.1c, 5.2), mute, for the cold test (19 Nov).
Four cold tests of stills left two things a still cannot show: which way the robe is going, and a punch that stops.
This is a rough: poses change, figures slide, nobody's legs walk. 540x960, 30 fps, one encoded file per shot, joined
with the concat demuxer. In 5.2 the Referee is behind the robot again (script v15).
Usage: python3 ring_rough_on3.py [out.mp4] [sheets_dir]   (default ../office-noir-3/on3_beat05_rough_v1.mp4)"""
import os
import sys
import math
import subprocess
import cairo
import ring_on3 as rg
import ring_casts_on3 as rc
import cast_on3 as ca
import client_on3 as b
import cand_bc as cb
import robot_on3 as r
import sofia_on3 as so3
from kit import cut

F, SC, Q = rg.F, rg.SC, rc.Q
FPS = 30
SHOTS = (("5.1a", 2.0), ("5.1b", 1.0), ("5.1c", 2.6), ("5.2", 1.6))


def lerp(a, b_, t):
    t = max(0.0, min(1.0, t))
    t = t * t * (3 - 2 * t)
    if isinstance(a, tuple):
        return tuple(x + (y - x) * t for x, y in zip(a, b_))
    return a + (b_ - a) * t


WALK, UP, SWING = b.POSES["b_walk"], (-9, 6, 150, 22), b.POSES["b_swing"]
WIND = (-9, 6, -52, 118)                                   # the glove drawn back by his ear


def shot_51a(t):
    """He is in his corner; his glove comes up toward the plan and his head goes back; Sofia walks the card across."""
    up = (t - 0.3) / 0.6

    def client(k):
        rg.shadow(k, 130, F - 30, 44)
        with rc.head_back(lerp(0.0, -0.24, up)):
            b.boxer(k, 130, F - 30, Q, lerp(WALK, UP, up), "hard", (0.7, lerp(0.0, -0.9, up)))

    def pam(k):
        rg.shadow(k, 228, F - 14, 34); ca.pam_corner(k, 228, F - 14, SC, "p_stand", "neutral", (-0.9, 0.0))

    def ref(k):
        rg.shadow(k, 336, F - 96, 36); ca.referee(k, 336, F - 96, SC * ca.REL_REF, "ref_stand", look=(-0.8, 0), waistcoat=True)

    def robot(k):
        rg.shadow(k, 408, F - 42, 40); r.robot(k, 408, F - 42, SC * r.REL, "r_wait", "furious", side=-1)

    def sofia(k):
        x = 720 - 150 * t
        so3.sofia(k, x, F + 108 - 3 * abs(math.sin(t * math.pi * 3.2)), 0.92, "r_card", "spotted", (-1, -0.2), card_="ROUND 1")
    return rg.frame("R1", [ref, robot, client, pam], [sofia], money=True)


def shot_51b(t):
    """His view: the glove comes up under the plan and cannot reach; the plan sways."""
    rise = lerp(300.0, 0.0, t / 0.45) + (3 * math.sin(t * 40) if t > 0.5 else 0)       # it strains, short of the paper
    return rg.plan_pov(glove=True, swing=0.02 * math.sin(t * 5), rise=rise)


def shot_51c(t):
    """The robe is on; Pam takes the collar and pulls it down off his shoulders; one sleeve comes with her, stretches,
    and stops at the glove; she pulls twice more; she lets go; she shoves it back up over his shoulders, crooked."""
    cx, cf = rc.CL
    off = 0.35 <= t < 1.75
    if off:
        pull = lerp(0.0, 1.0, (t - 0.35) / 0.25)
        tug = 7 * math.sin((t - 0.6) * math.pi * 3.2) if 0.6 < t < 1.5 else 0
        slack = lerp(0.0, 1.0, (t - 1.5) / 0.25)
        pose = (-9, 6, lerp(20.0, 56.0, pull) + tug * 0.5, 2)
        cl = lambda k: b.boxer(k, cx, cf, Q, pose, "hard", (0.7, -0.9), strip=True)
        gx, gy = rc.probe(cl)["hands"][1]
        ln = lerp(26.0, 86.0, pull) + tug - 30 * slack
        ex, ey = gx + ln, gy + 12 + 26 * slack

        def client(k):
            rg.shadow(k, cx, cf, 44)
            with rc.head_back():
                cl(k)
            c = k.c
            cut(k, [(gx + 4, gy - 22), (ex, ey - 12), (ex + 4, ey + 12), (gx + 8, gy + 24)], b.KEY, shadow=False, lw=2.2)
            c.set_source_rgb(*b.SHADE); c.set_line_width(2.0); c.set_line_cap(1)
            for q in (0.25, 0.5, 0.75):
                x_ = gx + 8 + (ex - gx - 6) * q
                c.move_to(x_, gy - 16 + 12 * q); c.line_to(x_ + 5, gy + 18 + 2 * q); c.stroke()
            cut(k, [(ex - 3, ey - 14), (ex + 10, ey - 13), (ex + 12, ey + 14), (ex - 1, ey + 15)], b.IVORY, shadow=False, lw=1.8)

        def pam(k):
            px_, pf = rc.PAM[0] - 60 + 60 * pull, rc.PAM[1]
            lean = (lerp(-4.0, 8.0, pull) + tug * 0.4 - 6 * slack, 12)
            rg.shadow(k, px_, pf, 34)
            ca.pam_corner(k, px_, pf, SC, ca.reach(px_, pf, SC, (ex + 4, ey - 6), (ex + 12, ey + 8), stance=lean), "neutral",
                          (-0.9, 0.7), stance=lean)
        return rg.frame("R3", [client, pam], [], near=False, hats=False)
    back = lerp(0.0, 1.0, (t - 1.75) / 0.3) if t >= 1.75 else 0.0
    grab = lerp(0.0, 1.0, t / 0.3) if t < 0.35 else 1.0

    def client(k):
        rg.shadow(k, cx, cf, 44)
        with rc.head_back():
            b.boxer(k, cx, cf - (5 * math.sin(back * math.pi) if t >= 1.75 else 0), Q, "b_walk", "hard", (0.7, -0.9))
        if t >= 1.75:                                       # the collar, shoved up on her side: it sits crooked
            c = k.c
            sx, sy = cx + 34 * Q, cf + (b.BT - 6) * Q
            cut(k, [(sx, sy + 26 * Q), (sx + 16 * Q, sy - 40 * Q * back), (sx + 62 * Q, sy - 22 * Q * back), (sx + 74 * Q, sy + 34 * Q)],
                b.KEY, shadow=False, lw=2.2)
            c.set_source_rgb(*b.SHADE); c.set_line_width(2.0); c.set_line_cap(1)
            c.move_to(sx + 22 * Q, sy - 24 * Q * back); c.line_to(sx + 40 * Q, sy + 22 * Q); c.stroke()

    def pam(k):
        tx, ty = cx + 62 * Q, cf + (b.BT - 14) * Q
        if t >= 1.75:
            away = lerp(0.0, 1.0, (t - 2.15) / 0.3)         # she steps back, hands off
            px_, pf = cx + 118 + 40 * away, F - 14
            rg.shadow(k, px_, pf, 34)
            if away > 0.5:
                ca.pam_corner(k, px_, pf, SC, "p_stand", "neutral", (-0.9, 0.2))
            else:
                ca.pam_corner(k, px_, pf, SC, ca.reach(px_, pf, SC, (tx, ty - 10 * back), (tx + 22, ty + 26), stance="work"), "neutral",
                              (-0.9, 0.2), stance="work")
        else:
            px_, pf = cx + 170 - 52 * grab, F - 14
            rg.shadow(k, px_, pf, 34)
            ca.pam_corner(k, px_, pf, SC, ca.reach(px_, pf, SC, (tx + 40 - 40 * grab, ty + 30 - 30 * grab), (tx + 60 - 38 * grab, ty + 60 - 34 * grab),
                                                   stance="work"), "neutral", (-0.9, 0.2), stance="work")
    return rg.frame("R3", [client, pam], [], near=False, hats=False)


BELL, STAND = cb.POSES_MACHO["ref_bell"], cb.POSES_MACHO["ref_stand"]


def shot_52(t):
    """The Referee, behind the robot, drops his arm; Pam clicks the stopwatch; he winds up and swings with everything;
    the glove stops a hand short; the robot has not moved; he stays there, shaking with the effort."""
    def ref(k):
        rg.shadow(k, 546, F - 96, 36)
        pose = "ref_bell" if t < 0.2 else lerp(BELL, STAND, (t - 0.2) / 0.15) if t < 0.35 else "ref_stand"
        ca.referee(k, 546, F - 96, SC * ca.REL_REF, pose, look=(-0.8, 0.2), waistcoat=True)

    def robot(k):
        rg.shadow(k, 466, F - 46, 40); r.robot(k, 466, F - 46, SC * r.REL, "r_wait", "furious", side=-1)

    def client(k):
        if t < 0.35:
            pose, dx = WALK, 0
        elif t < 0.75:
            pose, dx = lerp(WALK, WIND, (t - 0.35) / 0.3), -14 * lerp(0.0, 1.0, (t - 0.35) / 0.3)
        elif t < 0.87:
            pose, dx = lerp(WIND, SWING, (t - 0.75) / 0.12), -14 + 26 * lerp(0.0, 1.0, (t - 0.75) / 0.12)
        else:
            pose, dx = SWING, 12 + 1.5 * math.sin(t * 60)
        rg.shadow(k, 290 + dx, F - 40, 44); b.boxer(k, 290 + dx, F - 40, Q, pose, "hard", (0.9, 0))

    def pam(k):
        x, f = 190, F - 6
        if 0.2 <= t < 0.5:
            ca.pam_corner(k, x, f, SC, ca.reach(x, f, SC, (240, F - 204), (210, F - 84), stance="stand"), "neutral", (0.9, 0.1),
                          watch="hand", stance="stand")
        else:
            ca.pam_corner(k, x, f, SC, "p_stand", "neutral", (0.9, 0.1))
    return rg.frame((412, 1100, 1.25), [ref, robot, pam, client], [], near=False, hats=False)    # R2, a little wider: his arm


FN = {"5.1a": shot_51a, "5.1b": shot_51b, "5.1c": shot_51c, "5.2": shot_52}


def frames():
    """Every frame in order: (shot, time in the film, surface)."""
    t0 = 0.0
    for name, dur in SHOTS:
        for i in range(round(dur * FPS)):
            yield name, t0 + i / FPS, FN[name](i / FPS)
        t0 += dur


def render(out):
    d = os.path.dirname(os.path.abspath(out))
    parts = []
    for name, dur in SHOTS:
        tmp, fin = os.path.join(d, "_on3_%s.tmp.mp4" % name), os.path.join(d, "_on3_%s.mp4" % name)
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", "540x960", "-r", str(FPS),
                              "-i", "-", "-vf", "format=yuv420p", "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p",
                              "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", tmp], stdin=subprocess.PIPE)
        for i in range(round(dur * FPS)):
            p.stdin.write(bytes(FN[name](i / FPS).get_data()))
        p.stdin.close()
        assert p.wait() == 0, name
        os.replace(tmp, fin); parts.append(fin)
    lst = os.path.join(d, "_on3_list.txt")
    open(lst, "w").write("".join("file '%s'\n" % p_ for p_ in parts))
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", out])
    for p_ in parts + [lst]:
        os.remove(p_)


def sheets(d, prefix="sheet"):
    """Contact sheets for the cold test: every 4th of a second, numbered and timed; the punch at 8 a second; and the
    4-a-second sheet again at phone size."""
    os.makedirs(d, exist_ok=True)
    fr = list(frames())

    def grid(pick, cols, w, name, start=0):
        z = w / 540
        rows = (len(pick) + cols - 1) // cols
        s = cairo.ImageSurface(cairo.FORMAT_RGB24, cols * (w + 8) + 8, rows * (int(960 * z) + 30) + 8)
        c = cairo.Context(s); c.set_source_rgb(0.15, 0.15, 0.16); c.paint()
        for n, (_, t, f) in enumerate(pick):
            x, y = 8 + (n % cols) * (w + 8), 8 + (n // cols) * (int(960 * z) + 30)
            c.save(); c.translate(x, y + 24); c.scale(z, z); c.set_source_surface(f, 0, 0); c.paint(); c.restore()
            c.set_source_rgb(1, 1, 1); c.select_font_face("Inter", 0, 1); c.set_font_size(16)
            c.move_to(x + 2, y + 17); c.show_text("%d   %.2f s" % (start + n + 1, t))
        s.write_to_png(os.path.join(d, name))
    four = [fr[i] for i in range(0, len(fr), 7)]              # about 4 a second
    half = len(four) // 2 + 1
    grid(four[:half], 5, 400, prefix + "_4fps_a.png")
    grid(four[half:], 5, 400, prefix + "_4fps_b.png", start=half)
    punch = [x for x in fr if x[0] == "5.2"][::4]
    grid(punch, 6, 330, prefix + "_8fps_last_shot.png")
    grid(four, 7, 270, prefix + "_phone.png")


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "../office-noir-3/on3_beat05_rough_v1.mp4"
    if len(sys.argv) > 2:
        sheets(sys.argv[2])
    else:
        render(out)
