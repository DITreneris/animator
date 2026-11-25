"""PICK A SIDE (episode 14), stage 7: the film, scene by scene (plan v2, 25 Nov). Modelled on of_film.py (episode 13):
one function per shot taking the shot's own time t and returning the shot to draw (ps_scenes.S), drawn by ps_scenes'
rigs, set and cameras under board v4 (gags_v5), at 15 drawings a second on the 30 fps camera.

One map (lesson 109): SHOT_FN, printed and asserted by every build. A shot not in it is a hold on its board key frame.
Each shot's camera is locked to its board key frame's camera (a face-framed camera would follow the moving cast).

  python3 ps_film.py stills 1   ->  ../pick-a-side/ps_film_s1_stills_v1.png (the key poses of scene 1, before any video)"""
import math
import os
import sys
import cairo
import ps_scenes as ps
import ps_set as pss
import ps_motion as pm_
import don_ps as dp
from kit import Ctx, INK

DPS, FPS = 15, 30
OUT = ps.OUT
SCENES = {1: ["1.1", "1.2a", "1.3", "1.4"]}                  # v3 (Tomas 25 Nov): 1.2b cut (misread 3 times), its 0.5 s to 1.3
import json as _json
TIMING = {r["shot"]: r for r in _json.load(open(os.path.join(ps.OUT, "ps_timing_v3.json")))["shots"]}
DUR = {k: v["len"] for k, v in TIMING.items()}               # the takes' timing (v3): 1.3 2.61, 1.4 2.65
DUR["1.3"] += DUR["1.2b"]                                    # v3: 1.3 starts where 1.2b did; its take stays where it was
TAKE_AT = {k: list(v["take_at"]) for k, v in TIMING.items()}
TAKE_AT["1.3"] = [TAKE_AT["1.3"][0] + DUR["1.2b"]]


def lead(sid):
    return TAKE_AT[sid][0] if TAKE_AT[sid] else 0.15


def ease(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def lerp(a, b, u):
    return a + (b - a) * u


BOARD = {s["id"]: s for s in ps.SHOTS}


# --- scene 1 ------------------------------------------------------------------------------------------------------------
HOLD0 = 0.4                                                 # G5: frame 0 complete and held 0.4 s before anything moves


def s11(t):
    """the tug of war: motion test A (approved v3) after a 0.4 s frame 0; its four pulls in the remaining 1.4 s, each
    faster. Drawn by test A's own function on board v4's set (the robot a step left of the door frame, as the board)."""
    ta = 0.0 if t < HOLD0 else 0.2 + (t - HOLD0) * (1.6 / (DUR["1.1"] - HOLD0))
    return pm_.shot_A(ta, v4=True)


def s12a(t):
    """the blind tears off its rail and drops over Don (0.25 s), lands; daylight in through the bare glass."""
    u = ease(t / 0.25)
    base = BOARD["1.2a"]
    def cast(k):
        heads = {}
        o, heads["don"] = ps.don(k, "don_door", "stand", "shock", (0, -0.6 * (1 - u)))
        if u >= 1.0:
            dp.blind_over(k, o["head"], ps.SC["don"])
        else:                                                # in the air: the slats alone (blind_over's face gap would
            hx, hy = o["head"]; sc_ = ps.SC["don"]           # draw a second face up there), falling onto him
            w, h = 150 * sc_, 300 * sc_
            top = lerp(pss.GY0 - 10, hy - 70 * sc_, u)
            c = k.c
            c.save(); c.translate(hx, top); c.rotate(0.10 * (1 - u))
            c.new_path(); c.rectangle(-w / 2, 0, w, h); c.set_source_rgb(0.93, 0.91, 0.86); c.fill_preserve()
            c.set_source_rgb(*INK); c.set_line_width(2.4); c.stroke()
            c.set_line_width(1.2)
            for j in range(1, 22):
                c.move_to(-w / 2 + 4, j * h / 22); c.line_to(w / 2 - 4, j * h / 22); c.stroke()
            c.set_line_width(2.2)
            for dx in (-w * 0.3, 0, w * 0.3):                # speed lines above it
                c.move_to(dx, -14); c.line_to(dx, -44); c.stroke()
            c.restore()
        if u > 0.5:
            ps.light_in(k)
        _, heads["robot"] = ps.robot(k, (pss.GX0 + 196, ps.F + 4), visor="sun")
        return heads
    return ps.S("1.2a", base["cam"], base["room"], cast)


HEARD_12B = 0.12                                             # 1.2b: the crash reaches them (two drawings in)


def s12b(t):
    """v2 (cold test 0/2 twice: "a cutaway with no setup"): they are chatting, Pam's cup on its way up; the crash: three
    heads snap to it, the cup jolts and stops halfway, held. The rigs' own poses and faces, the cup's pose interpolated."""
    import pm_ps
    hit = t >= HEARD_12B
    q = min(t, HEARD_12B) / HEARD_12B                         # the cup rising, mid .. halfway to her chin
    if hit:
        q = 0.5 - 0.18 * math.exp(-(t - HEARD_12B) * 14)     # the jolt down, then it stops where it is
    else:
        q = 0.5 * q
    a, b = pm_ps.P_POSES["cup_mid"], pm_ps.P_POSES["cup_chin"]
    pm_ps.P_POSES["cup_t"] = tuple(x + (y - x) * q for x, y in zip(a, b)); pm_ps.P_HANDS["cup_t"] = ("relax_s", "cup")
    hop = 12 * math.exp(-(t - HEARD_12B) * 18) if hit else 0.0   # the startle: all three jump a little, together
    def cast(k):
        heads = {}
        k.c.translate(0, -hop)
        _, heads["pam"] = ps.pam(k, "trio_pam", "cup_t", "frozen" if hit else "neutral", (-1, -0.1) if hit else (0.8, 0))
        _, heads["mom"] = ps.mom(k, "trio_mom", "folded", "stern" if hit else "unimpressed", (-1, 0) if hit else (-0.6, 0))
        _, heads["sofia"] = ps.sofia(k, "trio_sof", "hip_out", "surprised" if hit else "smile", (-1, 0) if hit else (-0.8, 0))
        k.c.translate(0, hop)
        return {n: (h[0], h[1] - hop, h[2]) for n, h in heads.items()}
    return ps.S("1.2b", BOARD["1.2b"]["cam"], BOARD["1.2b"]["room"], cast)


def s13(t):
    """Don frozen under the blind, whispering. The visible change (lesson 200): the fallen blind still sways from the
    crash and settles (review 25 Nov: the loose slat read as "run through him"; cut)."""
    base = BOARD["1.3"]
    def cast(k):
        heads = {}
        o, heads["don"] = ps.don(k, "don_door", "stand", "neutral", (0, 0))
        hx, hy = o["head"]
        sw = 0.05 * math.cos(t * 9.0) * math.exp(-t * 2.2)    # a damped sway about the rail on his head
        c = k.c
        c.save(); c.translate(hx, hy - 70 * ps.SC["don"]); c.rotate(sw); c.translate(-hx, -(hy - 70 * ps.SC["don"]))
        dp.blind_over(k, o["head"], ps.SC["don"])
        c.restore()
        return heads
    return ps.S("1.3", base["cam"], base["room"], cast)


LIFT_14 = (1.35, 1.75)                                      # 1.4: the roll comes up on "Without me." (take 0.15-2.30)
LOOK_14 = 2.3                                               # then, after his line, the three look at each other


def s14(t):
    base = BOARD["1.4"]
    u = ease((t - LIFT_14[0]) / (LIFT_14[1] - LIFT_14[0]))
    v = ease((t - LOOK_14) / 0.25)
    close = t >= LOOK_14 - 0.05                               # review 25 Nov: at phone size the look was invisible: a cut
    def cast(k):                                             # in to the three, their own faces (the rigs' existing ones)
        ps.LOOK_14[0] = v
        ps.LIFT_14[0] = u
        ps.FACES_14[0] = FACES_LOOK if close else None
        ps.ROLL_RIGHT_14[0] = True                           # v2: his box sits left of his head in 1.4a: the roll goes up right
        return ps.cast_14(k)
    return ps.S("1.4b" if close else "1.4a", ["pam", "mom", "sofia"] if close else ["don"], base["room"], cast)


FACES_LOOK = ("doubt", "stern", "eyebrow")                   # Pam worried, Mom narrowed, Sofía one brow up


SHOT_FN = {"1.1": s11, "1.2a": s12a, "1.2b": s12b, "1.3": s13, "1.4": s14}


def print_map():
    for sid in sorted(SHOT_FN):
        assert sid in BOARD, sid
        print("  %-5s -> %s" % (sid, SHOT_FN[sid].__name__))


CAMS = {}


def shot_at(sid, t):
    """the shot to draw at its time t, its camera locked to the board key frame's."""
    ps.ROOM_OWN[0] = False
    sh = SHOT_FN[sid](t) if sid in SHOT_FN else BOARD[sid]
    key = sh["id"]                                           # a cut inside a shot ("1.4b") has its own locked camera
    if key not in CAMS:
        ps.NO_SHIFT[0] = key != sid
        ps.render(BOARD[sid] if key == sid else sh); CAMS[key] = ps._last_cam[0]
        if key in NUDGE:                                     # screen px: the frame moved so no sign is cut (G3);
            fx, fy, z = CAMS[key]; nx, ny, zz = NUDGE[key]     # zz: closer, about the frame's centre
            CAMS[key] = (fx + nx / z, fy + ny / z, z * zz)
    cam = CAMS[key]
    if key in PUSH:                                          # v3: a push in from another camera (the board's wide)
        frm, t0_, t1_ = PUSH[key]
        if frm not in CAMS:
            ps.NO_SHIFT[0] = False; ps.render(BOARD[frm]); CAMS[frm] = ps._last_cam[0]
        u = ease((t - t0_) / (t1_ - t0_))
        cam = tuple(a + (b - a) * u for a, b in zip(CAMS[frm], CAMS[key]))
    ps.NO_SHIFT[0] = True
    ps.ROOM_OWN[0] = sid in SHOT_FN                          # the board's 1.1 room is its key frame's; the film's moves
    return dict(sh, cam=cam, id=sid)


PUSH = {"1.4a": ("1.4", 0.20, 0.50)}                         # v3 (cold test 2/2 "another room"): 1.4 opens wide (the door,
                                                             # the three, one room), then pushes in to Don


NUDGE = {"1.4b": (10, 10, 1.3), "1.4a": (0, 40, 1.0)}                                   # 1.4b: $49,999, SHRED off the right, OUR FIRST CLIENT off the top


def draw(sid, t):
    import ps_checks as pc
    sh = shot_at(sid, t)                                     # (its camera probe renders first, outside the checks)
    pc.install_scene(ps); pc.begin()
    surf, msgs = ps.render(sh)
    msgs += pc.frame_checks(ps, ps.LAST[0])
    return surf, msgs


STILLS = {1: [("1.1", 0.0, "frame 0, held 0.4 s"), ("1.1", 0.70, "pull 1: Don, down"), ("1.1", 1.05, "the robot, up"),
              ("1.2a", 0.45, "the blind lands"), ("1.3", 0.3, "the blind still sways"),
              ("1.4", 0.2, "1.4a opens wide"), ("1.4", 1.2, "pushed in: Don speaks"), ("1.4", 1.9, "the roll up"), ("1.4", 2.5, "the three look")]}


def stills(n):
    ps.gags_v5()
    ps.pss.NO_DOOR_CONFETTI[0] = ps.rp.SUN_UP[0] = True
    ps.LIGHT_V5[0] = True; import pm_ps; pm_ps.MUG_RING[0] = True   # the film's look (review 25 Nov)
    print_map()
    tiles, faults = [], []
    for sid, t, label in STILLS[n]:
        surf, msgs = draw(sid, t)
        faults += ["%s @%.2f: %s" % (sid, t, m) for m in msgs]
        tiles.append((surf, "%s  %.2f s  %s" % (sid, t, label)))
    tw, th, cols = 270, 480, 4
    rows = (len(tiles) + cols - 1) // cols
    o = cairo.ImageSurface(cairo.FORMAT_RGB24, 20 + cols * (tw + 14), 20 + rows * (th + 34))
    c = cairo.Context(o); c.set_source_rgb(0.55, 0.55, 0.55); c.paint()
    for j, (im, lab) in enumerate(tiles):
        x, y = 20 + (j % cols) * (tw + 14), 20 + (j // cols) * (th + 34)
        c.save(); c.translate(x, y); c.scale(0.5, 0.5); c.set_source_surface(im, 0, 0); c.paint(); c.restore()
        c.set_source_rgb(0, 0, 0); c.set_font_size(13); c.move_to(x, y + th + 18); c.show_text(lab)
    p = os.path.join(OUT, "ps_film_s%d_stills_v4.png" % n)
    o.write_to_png(p)
    print("wrote", p)
    for f in faults:
        print("FAULT", f)
    return not faults


# --- the film: drawings, lips, bubbles, sound ----------------------------------------------------------------------------
LEAD, LIP_AHEAD = 0.15, 2.0 / FPS                            # the take starts 0.15 s into its shot; lips 2 frames ahead
TAKES = os.path.join(ps.HERE if hasattr(ps, "HERE") else os.path.dirname(os.path.abspath(__file__)), "ps_voices", "takes")
_TAKE = {}


def _take(sid):
    import soundfile as sf
    if sid not in _TAKE:
        a, sr = sf.read(os.path.join(TAKES, "%s.wav" % sid))
        _TAKE[sid] = (a if a.ndim == 1 else a.mean(axis=1), sr)
    return _TAKE[sid]


def loud(sid, t):
    """0..1: the take's loudness at the drawing (the of_film fallback rule: no viseme track for these takes)."""
    if not TIMING[sid]["takes"]:
        return 0.0
    a, sr = _take(sid)
    tt = t - lead(sid) + LIP_AHEAD
    if tt < 0 or tt > len(a) / sr:
        return 0.0
    i0, i1 = int(tt * sr), int((tt + 1.0 / DPS) * sr)
    w = a[i0:i1]
    peak = max(1e-6, (a ** 2).mean() ** 0.5 * 3.0)
    return float(min(1.0, (w ** 2).mean() ** 0.5 / peak)) if len(w) else 0.0


def bubble_on(sid, t):
    if not TIMING[sid]["takes"]:
        return False
    a, sr = _take(sid)
    t_on = max(lead(sid) - 0.02, max((p_[2] for k_, p_ in PUSH.items() if k_.startswith(sid)), default=0.0))
    return t_on <= t <= lead(sid) + len(a) / sr + 1.0 / DPS    # v3: a box doesn't ride a camera move (it hopped 3 times)


def mouth(k, head, o):
    """the speaker's open mouth over the rig's own closed one, its height the take's loudness."""
    if o < 0.12:
        return
    hx, hy, r = head
    c = k.c
    c.save(); c.translate(hx, hy + 0.64 * r); c.scale(0.15 * r, 0.11 * r * (0.40 + 0.60 * o))   # on the drawn mouth line
    c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    c.set_source_rgb(0.33, 0.10, 0.10); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.0); c.stroke()


def drawing(sid, t):
    sh = shot_at(sid, t)
    line = TIMING[sid]["line"]
    if line and bubble_on(sid, t) and not (sid == "1.4" and t >= LOOK_14 - 0.05):
        surf, msgs = ps.board_frame(sh, line)
    else:
        import ps_checks as pc
        pc.install_scene(ps); pc.begin()
        surf, msgs = ps.render(sh)
    msgs = msgs + __import__("ps_checks").frame_checks(ps, ps.LAST[0])
    who = (ps.says(line)[0][0] if line else None)
    if who and who in ps.LAST[0]:
        mouth(Ctx(cairo.Context(surf), 0), ps.LAST[0][who], loud(sid, t))
    return surf, msgs


def sound(n, path):
    """the scene's stretch: the takes at their shots, the effects from of_sound's synth (reused), room tone; -15 LUFS."""
    import numpy as np, soundfile as sf
    import of_sound as osd
    SR = osd.SR
    starts, acc = {}, 0.0                                    # the film's own cut (v3: 1.2b out)
    for sid in SCENES[n]:
        starts[sid] = acc; acc += DUR[sid]
    total = acc
    buf = np.zeros(int((total + 0.3) * SR))
    for sid in SCENES[n]:
        st = starts[sid]
        for tk, at in zip(TIMING[sid]["takes"], TAKE_AT[sid]):
            a, sr = _take(tk)
            if sr != SR:
                from scipy.signal import resample_poly
                a = resample_poly(a, SR, sr)
            osd.put(buf, a, st + at, 1.0)
    if n == 1:
        def rattle_run(d, pitch):                            # the slats running down or up: a burst of clicks
            out = np.zeros(int(d * SR))
            for j in range(int(d * 40)):
                c_ = osd.rattle() * (0.5 + 0.5 * osd.rng.random())
                i = int((j / 40.0 + 0.004 * osd.rng.random()) * SR)
                out[i:i + len(c_)] += c_[:max(0, len(out) - i)]
            return osd.hp(out, max(1, int(6 / pitch)))
        for k_, (a_, b_, kind, _w) in enumerate([x for x in pm_.TUG if x[2] != "hold"]):
            ta = HOLD0 + (a_ - 0.2) * ((DUR["1.1"] - HOLD0) / 1.6)
            tb = HOLD0 + (b_ - 0.2) * ((DUR["1.1"] - HOLD0) / 1.6)
            osd.put(buf, rattle_run(tb - ta, 1.0 + 0.25 * k_), ta, 0.25 + 0.08 * k_)   # rising, each faster
        st = starts["1.2a"]
        crash = osd.slam() * 1.0
        osd.put(buf, crash, st + 0.20, 0.9)                  # the blind lands
        osd.put(buf, rattle_run(0.45, 1.6), st + 0.18, 0.6)  # the slats
    buf += osd.room(len(buf) / SR)[:len(buf)] * 0.012
    tmp = path + ".raw.wav"
    x = buf / (np.abs(buf).max() + 1e-9) * 0.5
    sf.write(tmp, x.astype(np.float32), SR)
    from scipy.ndimage import minimum_filter1d               # of_sound.master's loop (it writes 13's file, so not called):
    g, ceil = 1.0, 10 ** (-5.0 / 20)                         # one gain to -15 LUFS, a look-ahead limiter on the peak
    for _ in range(8):
        y = x * g
        need = np.minimum(1.0, ceil / (np.abs(y) + 1e-9))
        need = minimum_filter1d(need, size=int(0.004 * SR) * 2 + 1)
        need = np.minimum(need, osd.lp(need, int(0.05 * SR)))
        y = y * need
        sf.write(path, y.astype(np.float32), SR)
        I, P = osd.levels(path)
        if abs(I + 15.0) < 0.3 and P <= -3.0:
            break
        g *= 10 ** ((-15.0 - I) / 20)
    os.remove(tmp)
    return I, P


HOLD_D = 5                                                   # drawings (0.33 s), as of_film


def film(n, ver=1):
    import subprocess, shutil
    ps.gags_v5()
    ps.pss.NO_DOOR_CONFETTI[0] = ps.rp.SUN_UP[0] = True
    ps.LIGHT_V5[0] = True; import pm_ps; pm_ps.MUG_RING[0] = True
    print_map()
    d = "/tmp/ps_film_s%d" % n
    shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    frames, faults = [], {}
    for sid in SCENES[n]:
        m = int(round(DUR[sid] * DPS))
        for i in range(m):
            t = i / DPS
            surf, msgs = drawing(sid, t)
            for x in msgs:
                faults.setdefault("%s: %s" % (sid, x.split(" at ")[0]), []).append(round(t, 2))
            p = os.path.join(d, "%04d.png" % len(frames)); surf.write_to_png(p); frames.append(p)
    lst = os.path.join(d, "list.txt")
    with open(lst, "w") as f:
        for p in frames:
            f.write("file '%s'\nduration %.5f\n" % (p, 1.0 / DPS))
        f.write("file '%s'\n" % frames[-1])
    wav = os.path.join(d, "s%d.wav" % n)
    I, P = sound(n, wav)
    mp4 = os.path.join(OUT, "ps_film_s%d_v%d_540.mp4" % (n, ver))
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-i", wav,
                           "-vf", "fps=%d,format=yuv420p" % FPS, "-c:v", "libx264", "-crf", "20", "-preset", "veryfast",
                           "-c:a", "aac", "-b:a", "192k", "-shortest", mp4])
    sheets(n, frames)
    print("wrote %s  (%d drawings, %.1f LUFS, peak %.1f dB)" % (mp4, len(frames), I, P))
    real = {}
    for k_, v in faults.items():                             # of_film's held_only: a prop passing through a dead zone in a
        if ("ZONE" in k_ or "SIGN cut" in k_) and len(v) < HOLD_D:   # move (or a sign crossing the edge in a camera move) is not a fault; 5 drawings is
            print("passing %s  (%d drawings, from %.2f s)" % (k_, len(v), v[0]))
            continue
        real[k_] = v
        print("FAULT %s  (%d drawings, from %.2f s)" % (k_, len(v), v[0]))
    return not real


def sheets(n, frames):
    """the cold viewers' 4 fps sheet of the scene and an 8 fps strip of its first 2.8 s (1.1-1.2b), time stamps."""
    for fps, until, name in ((4, None, "sheet4"), (8, 2.8, "strip8")):
        dur = len(frames) / DPS if until is None else until
        picks = [(j / fps, frames[min(len(frames) - 1, int(round(j / fps * DPS)))]) for j in range(int(dur * fps) + 1)]
        tw, th, cols = 180, 320, 8
        rows = (len(picks) + cols - 1) // cols
        o = cairo.ImageSurface(cairo.FORMAT_RGB24, 20 + cols * (tw + 10), 20 + rows * (th + 26))
        c = cairo.Context(o); c.set_source_rgb(0.15, 0.15, 0.16); c.paint()
        for j, (t, p) in enumerate(picks):
            x, y = 20 + (j % cols) * (tw + 10), 20 + (j // cols) * (th + 26)
            im = cairo.ImageSurface.create_from_png(p)
            c.save(); c.translate(x, y); c.scale(tw / 540, tw / 540); c.set_source_surface(im, 0, 0); c.paint(); c.restore()
            c.set_source_rgb(1, 1, 1); c.set_font_size(13); c.move_to(x, y + th + 16); c.show_text("%d  %.2f s" % (j + 1, t))
        o.write_to_png("/tmp/ps_film_s%d/%s.png" % (n, name))


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "film":
        sys.exit(0 if film(int(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 1) else 1)   # a new version, a new name
    if len(sys.argv) > 2 and sys.argv[1] == "stills":
        sys.exit(0 if stills(int(sys.argv[2])) else 1)
    print(__doc__)
