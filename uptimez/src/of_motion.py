"""THE OFFER (episode 13), stage 6: motion tests (series/production-process.md). The four moments that a still frame
cannot carry, each drawn from the scene file (of_scenes.py) at film rate: 15 drawings a second, each held for two
frames of the 30 fps camera. Shot lengths are the recorded takes' (of_timing_v2.json); lines carry their bubbles.

  1. rock   0.8 -> 0.9 -> 0.10  the hand on the roof rocks the car; under it, "Off the car."; the hand comes off at
                                once, he steps back, and only then looks to Father
  2. veto   1.5 -> 1.6 -> 1.7   the loyal one's head turns to Father, the flame held; Father's eyebrow and a small
                                shake; the lid snaps shut while he still looks at Father
  3. lamp   2.3                 the Client holds the lamp back without looking; bodyguard 1 takes it, unasked, and
                                holds it over the engine
  4. turn   3.4                 the robot's head turns, slowly, to Don; its smile never changes

  python3 of_motion.py [test ...]  ->  ../the-offer/of_motion_<test>_v1_540.mp4 (silent) and
                                       /tmp/of_motion/<test>_strip8.png (8 fps strip for the cold viewers)
Each drawing goes through the scene file's own checks (signs, scale) and its bubble check; the build stops on a fault."""
import math
import os
import subprocess
import sys
import cairo
import of_scenes as sc
import of_set as gs

OUT = sc.OUT
TMP = "/tmp/of_motion"
DPS = 15                                                   # drawings a second
FPS = 30


def ease(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def _shot(sid):
    for title, where, scene, shots in sc.SCENES:
        for sh in shots:
            if sh["id"] == sid:
                return sh, scene
    raise KeyError(sid)


def lerp(a, b, u):
    return tuple(p + (q - p) * u for p, q in zip(a, b))


# --- the four tests: [(shot id, seconds, function(t, len) -> (state overrides, pose overrides))] -----------------------
def hold(u):
    """v2: an action's key drawings: 0..1 over its time, then held at 1 (the result stays on screen)."""
    return ease(u)


def rock():
    def s08(t, L):                                             # v2: two big pumps, then the car settles; the legs jolt
        if t < 0.15:
            return dict(tilt=0.0, legs_jolt=0.0), {}
        ph = (t - 0.15) / 0.30
        a = -0.17 * abs(math.sin(ph * math.pi)) if ph < 2 else -0.17 * abs(math.sin(ph * math.pi)) * math.exp(-(ph - 2) * 1.5)
        return dict(tilt=a, legs_jolt=-60 * a), {}
    def s09(t, L):
        return dict(sway_v=46 * math.sin(t * 8.0) * math.exp(-t * 1.0)), {}
    def s010(t, L):
        u = hold(t / 0.20)                                     # the hand off at once: 3 drawings, then it stays off
        x, f = sc.BLOCK[1]["g1"]
        roof = sc._pt("roof", x, f)
        off = sc._pt("off_r", x, f)
        back = -30 * hold((t - 0.15) / 0.20)                   # a step away from Father
        turn = -1.0 * hold((t - 0.40) / 0.20)                  # only then does he look at Father; held
        return {}, dict(g1=dict(targets_xy=[lerp(roof, off, u)], back=back, turn=turn),
                        father=dict(look=(1, -0.1), face="brow" if t > 0.75 else "hard"))
    return [("0.8", s08), ("0.9", s09), ("0.10", s010)]


def veto():
    def s15(t, L):                                             # the flame held; his head turns to Father, held 0.4 s
        return {}, dict(g2=dict(targets=["lighter"], lighter=1.0, turn=-1.0 * hold((t - 0.10) / 0.25)))
    def s16(t, L):                                             # the brow up at 0.15, then two clear shakes
        face = "brow2" if t > 0.15 else "hard"                     # v3: the brow arches high, then a small no
        shake = 0.0 if t < 0.40 else math.sin((t - 0.40) * 2 * math.pi * 2.0) * math.exp(-(t - 0.40) * 1.4)
        return dict(fshake=shake * 14), dict(father=dict(face=face, look=(1 + 0.8 * shake, -0.2)))
    def s17(t, L):                                             # still looking at Father: the lid shuts, held
        lid = 1.0 - hold((t - 0.15) / 0.12)                     # v3: SNAP, then the hand comes down off the plan
        import of_set as gs
        bx, by = gs.bay7()
        down = 90 * hold((t - 0.32) / 0.25)
        return {}, dict(g2=dict(targets_xy=[(bx + 2, by + 92 + down)], lighter=1.0 if lid > 0.6 else 0.0, lid=lid, turn=-1.0))
    return [("1.5", s15), ("1.6", s16), ("1.7", s17)]


def lamp():
    """v3: the lamp never near a face. It passes low, at the bay's edge, unlit; bodyguard 1 lifts it high over the bay and
    points it down: the light falls on the engine, the Client's eyes and hands stay in it; Father watches at the left."""
    bx, bf = sc.BENT_AT
    start, out_ = (bx - 30, 718), (bx + 60, 724)
    x, f = sc.BLOCK[3]["g1"]
    rest = (x - 44, f - 120)
    def s23(t, L):
        u1 = hold(t / 0.35)                                    # his hand comes back with it, low, not looking
        u2 = hold((t - 0.35) / 0.25)                           # the bodyguard's hand comes down to it
        u3 = hold((t - 0.65) / 0.35)                           # he lifts it high and points it down; held
        gh = lerp(rest, out_, u2)
        if u3 > 0:
            gh = lerp(out_, sc.LAMP_HIGH, u3)
            return {}, dict(client=dict(kind="bent", hand_back=True, hand_back_at=lerp(out_, start, u3), client_lamp=False),
                            g1=dict(targets_xy=[gh], lamp=True, lamp_xy=gh, cone=u3), father=dict(look=(1, -0.2)))
        return {}, dict(client=dict(kind="bent", hand_back=True, hand_back_at=lerp(start, out_, u1), lamp_lit=False),
                        g1=dict(targets_xy=[gh]), father=dict(look=(1, -0.2)))
    return [("2.3", s23)]


def turn():
    def s34(t, L):                                             # the turn over 0.6 s, then held; Don in the frame
        return dict(turn=hold((t - 0.15) / 0.60), don_edge=True), {}
    return [("3.4", s34)]


TESTS = dict(rock=rock, veto=veto, lamp=lamp, turn=turn)
VERSION = dict(rock=2, veto=2, lamp=3, turn=2)


def render_test(name):
    seq = TESTS[name]()
    tm = sc._timing()
    d = os.path.join(TMP, name)
    os.makedirs(d, exist_ok=True)
    for f_ in os.listdir(d):
        os.remove(os.path.join(d, f_))
    n = 0
    probs = []
    strip = []
    for sid, fn in seq:
        sh0, scene = _shot(sid)
        L = tm[sid]["len"]
        nd = max(1, round(L * DPS))
        for i in range(nd):
            t = i / DPS
            st_over, pose_over = fn(t, L)
            sh = dict(sh0, state=dict(sh0["state"], **st_over))
            saved = sc.POSES.get(sid)
            if pose_over:
                base = dict(saved or {})
                for who, ps in pose_over.items():
                    base[who] = dict(base.get(who, {}), **ps)
                sc.POSES[sid] = base
            try:
                surf, p = sc.board_frame(sh, scene)
            finally:
                if saved is None:
                    sc.POSES.pop(sid, None)
                else:
                    sc.POSES[sid] = saved
            probs += ["%s %s t=%.2f: %s" % (name, sid, t, q) for q in p]
            for _ in range(FPS // DPS):
                surf.write_to_png(os.path.join(d, "f%04d.png" % n)); n += 1
            if i % 2 == 0:                                       # 15 -> 7.5, close to the 8 fps strip
                strip.append((sid, t, surf))
    mp4 = os.path.join(OUT, "of_motion_%s_v%d_540.mp4" % (name, VERSION.get(name, 1)))
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS), "-i", os.path.join(d, "f%04d.png"), "-vf",
                    "scale=540:960:flags=lanczos,format=yuv420p", "-c:v", "libx264", "-crf", "20", "-preset", "veryfast",
                    "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", mp4], check=True)
    cols, tw, th = 8, 216, 384
    rows = (len(strip) + cols - 1) // cols
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, (cols * (tw + 8) + 8) * 2, (rows * (th + 30) + 10) * 2); S.set_device_scale(2, 2)
    c = cairo.Context(S); c.set_source_rgb(1, 1, 1); c.paint()
    for i, (sid, t, img) in enumerate(strip):
        x = 8 + (i % cols) * (tw + 8); y = 6 + (i // cols) * (th + 30)
        c.save(); c.translate(x, y); c.scale(tw / 540.0, th / 960.0); c.set_source_surface(img, 0, 0); c.paint(); c.restore()
        c.set_source_rgb(0, 0, 0); c.select_font_face("Inter", 0, 1); c.set_font_size(13)
        c.move_to(x, y + th + 18); c.show_text("%d" % (i + 1))
    S.write_to_png(os.path.join(TMP, "%s_strip8.png" % name))
    return n, probs


if __name__ == "__main__":
    names = sys.argv[1:] or list(TESTS)
    allp = []
    for nm in names:
        n, p = render_test(nm)
        print("%-5s %d frames, %d problems" % (nm, n, len(p)), flush=True)
        allp += p
    for q in allp[:20]:
        print("FAIL", q)
    sys.exit(1 if allp else 0)
