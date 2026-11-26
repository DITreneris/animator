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

FIX = dict(face14="neutral", roll_grip=24, shock61b="balance", beats23=((0.35, 0.75, 96), (0.75, 1.15, 106), (1.15, 1.55, 116)))


def setup():
    ps.FACE_14[0] = FIX["face14"]
    dp.ROLL_GRIP[0] = FIX["roll_grip"]
    pf.BEATS_23[0] = FIX["beats23"]
    ps.sp.TAPE_LONG[0] = True
    pf.SHOT_FN["1.4"] = s14
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
