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
def rock():
    def s08(t, L):
        k = t / L
        tilt = -0.11 * math.sin(min(1.0, k * 1.6) * math.pi * 3.2) * (1 - 0.6 * k) if t > 0.15 else 0.0
        return dict(tilt=tilt), {}
    def s09(t, L):
        return dict(sway_v=42 * math.sin(t * 9.0) * math.exp(-t * 1.2)), {}
    def s010(t, L):
        u = ease(t / 0.20)                                     # the hand off at once (in 3 drawings)
        x, f = sc.BLOCK[1]["g1"]
        roof = sc._pt("roof", x, f)
        off = [sc._pt("off_l", x - 26 * u, f), sc._pt("off_r", x - 26 * u, f)]
        back = -26 * ease((t - 0.10) / 0.25)                  # away from Father
        turn = -1.0 * ease((t - 0.45) / 0.25)                  # only then does he look at Father
        tg = [lerp(roof, off[1], u)]                            # only the roof hand moves; the other rests
        return {}, dict(g1=dict(targets_xy=tg, back=back, turn=turn), father=dict(look=(1, -0.1), face="hard"))
    return [("0.8", s08), ("0.9", s09), ("0.10", s010)]


def veto():
    def s15(t, L):
        return {}, dict(g2=dict(targets=["lighter"], lighter=1.0, turn=-1.0 * ease((t - 0.15) / 0.35)))
    def s16(t, L):
        face = "brow" if t > 0.18 else "hard"
        shake = 0.0 if t < 0.45 else 0.5 * math.sin((t - 0.45) * 2 * math.pi * 2.2) * math.exp(-(t - 0.45) * 2.5)
        return dict(fshake=shake * 14), dict(father=dict(face=face, look=(1 + shake, -0.2)))
    def s17(t, L):
        lid = 1.0 - ease((t - 0.10) / 0.12)                    # snap
        return {}, dict(g2=dict(targets=["lighter"], lighter=1.0 if lid > 0.5 else 0.0, lid=lid, turn=-1.0))
    return [("1.5", s15), ("1.6", s16), ("1.7", s17)]


def lamp():
    bx, bf = sc.BENT_AT
    start, out_ = (bx - 30, 700), (bx + 78, 646)
    x, f = sc.BLOCK[3]["g1"]
    def s23(t, L):
        u1 = ease(t / 0.45)                                    # his hand comes back with it, not looking
        hb = lerp(start, out_, u1)
        u2 = ease((t - 0.45) / 0.30)                           # bodyguard 1's hand comes to it
        g_from = (x + 30, f - 150)
        gh = lerp(g_from, (out_[0] + 4, out_[1] - 4), u2)
        u3 = ease((t - 0.80) / 0.45)                           # he takes it over the engine
        if u3 > 0:
            gh = lerp((out_[0] + 4, out_[1] - 4), sc.LAMP_HELD, u3)
            return {}, dict(client=dict(kind="bent", hand_back=True, hand_back_at=lerp(out_, start, u3), client_lamp=False),
                            g1=dict(targets_xy=[gh], lamp=True, lamp_xy=gh), father=dict(look=(1, -0.2)))
        return {}, dict(client=dict(kind="bent", hand_back=True, hand_back_at=hb), g1=dict(targets_xy=[gh]),
                        father=dict(look=(1, -0.2)))
    return [("2.3", s23)]


def turn():
    def s34(t, L):                                             # v2: Don's crown and shoulder at the right edge to turn to
        return dict(turn=ease((t - 0.20) / 0.90), don_edge=True), {}
    return [("3.4", s34)]


TESTS = dict(rock=rock, veto=veto, lamp=lamp, turn=turn)


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
    mp4 = os.path.join(OUT, "of_motion_%s_v1_540.mp4" % name)
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
