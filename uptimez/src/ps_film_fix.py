"""PICK A SIDE: the audit's drawing faults (P1-P15, story audit v1 §3) fixed across the locked scenes, opt-in: every
switch is set only by setup() here, so the locked versions still build byte-identical from ps_film alone.

  python3 ps_film_fix.py film 1 6    (and 2 5, 4 12; scenes 5 and 6 through ps_film_end: setup() calls both)

P1  1.4   his face "hollow" (grey eyes = sunglasses) -> FACE_14
P2  roll  the hand a disc inside the roll -> don_ps.ROLL_GRIP: the ring hangs under the fist, the fist redrawn on its rim
P3  2.3   the roll over his face as it points -> BEATS_23 lower (the arm at shoulder height)
P4  2.8   the tape a short piece ending mid-frame -> sofia_ps.TAPE_LONG: edge to edge
P15 6.1b  the shock's hands piled on his chest -> the arms flung out (pose "balance")"""
import sys
import ps_film as pf
import ps_scenes as ps
import don_ps as dp

FIX = dict(trim210=0.90, face14="neutral", roll_grip=24, shock61b="balance", beats23=((0.35, 0.75, 96), (0.75, 1.15, 106), (1.15, 1.55, 116)))


_DUR210 = pf.DUR["2.10"]
DUR_21C = 0.6
DAD_HIDE = {"2.1b", "2.5", "2.7", "2.9b", "3.1", "3.3", "5.4", "6.1", "6.1b"}  # shots whose camera cuts "DAD ->" at the frame's edge: not drawn
                                                             # there (signs whole or out of frame; 6.1: three-quarters behind Don)


def _dad_drawing(fn):
    def drawing(sid, t, *a, **kw):
        was = ps.pss.DAD_MARK[0]
        ps.pss.DAD_MARK[0] = was and sid not in DAD_HIDE
        try:
            return fn(sid, t, *a, **kw)
        finally:
            ps.pss.DAD_MARK[0] = was
    drawing._dad = True
    return drawing


def s21c(t):
    """2.1c (0.6 s, new): the floor from above, the tape down the middle: "<- DON" on his side as he wrote it in 2.1b,
    and "DAD ->" written on the other as we look (its strokes drawn on in 0.35 s; a marker's squeak in ps_mix)"""
    import kit
    def draw(k):
        c = k.c
        c.set_source_rgb(*kit.FLOOR); c.paint()
        kit.cut(k, [(236, 960), (304, 960), (290, 0), (250, 0)], ps.pss.TAPE, shadow=False, lw=2.4)
        c.set_source_rgba(1, 1, 1, 0.40); c.set_line_width(3); c.move_to(258, 950); c.line_to(262, 10); c.stroke()
        def mark(x, y, word, right, u=1.0):
            c.save(); c.translate(x, y); c.rotate(-0.05 if not right else 0.05)
            c.select_font_face("Permanent Marker", 0, 1); c.set_font_size(46); c.set_source_rgb(0.08, 0.08, 0.10)
            e = c.text_extents(word)
            n = max(0, min(len(word), int(round(u * 1.6 * len(word)))))
            c.move_to(-e.x_advance / 2, 0); c.show_text(word[:n])
            ua = max(0.0, min(1.0, (u - 0.6) / 0.4))
            if ua > 0:
                c.set_line_width(8); c.set_line_cap(1)
                sx = (e.x_advance / 2 + 10) if right else -(e.x_advance / 2 + 10)
                ex = sx + (55 if right else -55) * ua
                c.move_to(sx, -18); c.line_to(ex, -18); c.stroke()
                if ua >= 1:
                    hx = sx + (55 if right else -55); d_ = -1 if right else 1
                    c.move_to(hx, -18); c.line_to(hx + 20 * d_, -36); c.stroke()
                    c.move_to(hx, -18); c.line_to(hx + 20 * d_, 0); c.stroke()
                c.set_line_cap(0)
            c.restore()
        mark(150, 500, "DON", False)
        mark(392, 500, "DAD", True, min(1.0, t / 0.35))
        return {}
    return ps.S("2.1c", "screen", draw=draw)


def setup():
    ps.FACE_14[0] = FIX["face14"]
    dp.ROLL_GRIP[0] = FIX["roll_grip"]
    pf.BEATS_23[0] = FIX["beats23"]
    ps.sp.TAPE_LONG[0] = True
    pf.SHOT_FN["1.4"] = s14
    ps.pss.DAD_MARK[0] = True                                # "DAD ->" on the far side of the tape (Tomas 26 Nov)
    pf.DUR["2.10"] = _DUR210 - FIX["trim210"]         # the robot froze 1.2 s after "Both." (read as a glitch)
    if "2.1c" not in pf.SCENES[2]:                           # the two sides named at the start (Tomas 26 Nov, /grill-me)
        pf.SCENES[2].insert(pf.SCENES[2].index("2.1b") + 1, "2.1c")
    pf.TIMING["2.1c"] = dict(shot="2.1c", len=DUR_21C, line=None, takes=[], take_at=[])
    pf.DUR["2.1c"], pf.TAKE_AT["2.1c"] = DUR_21C, []
    pf.SHOT_FN["2.1c"] = s21c
    pf.BOARD["2.1c"] = dict(s21c(0.0), id="2.1c")
    if not getattr(pf.drawing, "_dad", False):
        pf.drawing = _dad_drawing(pf.drawing)
    import ps_film_end as fe
    fe.setup()                                               # scenes 5 and 6: the new ending
    fe.SHOCK_POSE_61B[0] = FIX["shock61b"]


_s14 = pf.s14


def s14(t):
    """1.4 with the grip: the roll at his side rests ON his fist (the ring above it, out of the bottom quarter); as it
    comes up it swings under the fist"""
    u = pf.ease((t - pf.LIFT_14[0]) / (pf.LIFT_14[1] - pf.LIFT_14[0]))
    sh = _s14(t)
    inner = sh["cast"]
    def cast(k):
        was = dp.ROLL_GRIP[0]
        dp.ROLL_GRIP[0] = -22 + (FIX["roll_grip"] + 22) * u
        try:
            return inner(k)
        finally:
            dp.ROLL_GRIP[0] = was
    return dict(sh, cast=cast)


def master(n, ver):
    """G5: scene n at native 1080 (ps_scenes.HIRES 2: the same drawings at 2x), 30 fps, BT.709 tags, the scene's
    sound; written to /tmp (series rule: 1080 masters are not committed). The faults were checked on the 540 build."""
    import os, shutil, subprocess
    ps.gags_v5()
    import dh_cast as dc_; dc_.FRONT_HAND[0], dc_.FRONT_HAND_S[0], dc_.BACK_HAND[0] = "pinch", 0.8, "quiet"
    ps.PINCH_POSE[0], ps.PINCH_LEAD[0] = (-73, -93), 1.6
    import client_ps as cps_, hands_ps as hp_; cps_.POINT_V2[0] = ps.SHOT43_V8[0] = hp_.PINCH_V2[0] = True; cps_.POINT_SKIN[0], cps_.POINT_W[0] = (0.86, 0.64, 0.50), 1.3
    hp_.PINCH_V4[0] = ps.NOSE_43[0] = True; hp_.PINCH_CLOSE[0] = 1.0; cps_.POINT_LEN[0] = 0.85; ps.PHOTO_43[0] = True; ps.FATHER_SPOT[0] = 0.35
    ps.BRIDGE_V2[0] = ps.ZOOM_42[0] = ps.STINK_V2[0] = ps.FATHER_V2[0] = True
    dp.BLIND_GAP_FIX[0] = dp.ROLL_TAIL[0] = True
    ps.pss.NO_DOOR_CONFETTI[0] = ps.rp.SUN_UP[0] = True
    ps.LIGHT_V5[0] = True; import pm_ps; pm_ps.MUG_RING[0] = True       # (the film()'s look, as ps_film.film)
    ps.HIRES[0] = 2
    d = "/tmp/ps_master_s%d" % n
    shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    frames = []
    for sid in pf.SCENES[n]:
        for i in range(int(round(pf.DUR[sid] * pf.DPS))):
            surf, _ = pf.drawing(sid, i / pf.DPS)
            assert surf.get_width() == 1080, surf.get_width()
            p = os.path.join(d, "%04d.png" % len(frames)); surf.write_to_png(p); frames.append(p)
    ps.HIRES[0] = 1
    lst = os.path.join(d, "list.txt")
    with open(lst, "w") as f:
        for p in frames:
            f.write("file '%s'\nduration %.5f\n" % (p, 1.0 / pf.DPS))
        f.write("file '%s'\n" % frames[-1])
    wav = os.path.join(d, "s%d.wav" % n)
    I, P = pf.sound(n, wav)
    out = "/tmp/ps_film_s%d_v%d_1080.mp4" % (n, ver)
    tags = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709"]
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-i", wav,
                           "-vf", "fps=%d,format=yuv420p" % pf.FPS, "-c:v", "libx264", "-crf", "18", "-preset", "veryfast"] + tags +
                          ["-c:a", "aac", "-b:a", "192k", "-shortest", out])
    print("wrote %s  (%d drawings, %.1f LUFS, %.1f dB)" % (out, len(frames), I, P))
    return out


if __name__ == "__main__":
    setup()
    if len(sys.argv) > 2 and sys.argv[1] == "master":
        sys.exit(0 if master(int(sys.argv[2]), int(sys.argv[3])) else 1)
    if len(sys.argv) > 2 and sys.argv[1] == "film":
        sys.exit(0 if pf.film(int(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 1) else 1)
    print(__doc__)
