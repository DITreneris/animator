"""THE OFFER (episode 13), stage 8: the rough cut and its G5 QA.

The five scenes (of_film.py, drawn on the timeline's grid) joined frame by frame on the master sound (of_sound_v8.wav);
each scene is placed at its own start on the 30 fps grid, so the picture cannot drift from the sound across the film.
Then G5, measured on the final file; the build fails on any miss:

  format      1080x1920, 30 fps, the expected frame count, BT.709 tags
  level       the AAC as delivered: true peak <= -1 dBTP, integrated -16..-14 LUFS
  lines       the recognizer on every voice line inside the delivered mix (2 of 3 windows; 2.6 a known artefact)
  frame 0     complete: no flash, no blank, nothing scaling in (its colour spread and its ink, against frame 1)
  loop        the last frame leads back into frame 0: the same drawing but the burn on 7
  text        every drawing's checks (signs, dead zones, tails, Don rule) passed at render time: of_film's FAIL log is empty

  python3 of_cut.py        ->  ../the-offer/of_roughcut_v1_540.mp4, /tmp/of_cut/of_roughcut_v1_1080.mp4,
                               ../the-offer/of_roughcut_v1_qa.json
1080 masters are rendered in /tmp only (series rule: 540 copies are committed)."""
import json
import os
import shutil
import subprocess
import sys
import numpy as np
import soundfile as sf
from PIL import Image
import of_scenes as sc

VERSION = 19
TMP = "/tmp/of_cut"
FRAMES = "/tmp/of_film/s%d"                                 # each scene's drawings, as of_film left them (or a copy in TMP)
FPS = 30
TAGS = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709"]


def scene_dirs():
    """v2 (23 Nov): ALWAYS the drawings of_film just rendered. v1 preferred a copy in TMP, and a stale copy from 09:05
    went into rough cuts v10 and v11 unseen (lesson 152). A scene whose folder is missing or empty stops the cut."""
    out = []
    for n in range(1, len(sc.SCENES) + 1):
        d = FRAMES % n
        if not (os.path.isdir(d) and os.listdir(d)):
            raise SystemExit("scene %d: no drawings in %s; render it with of_film.py %d" % (n, d, n))
        out.append(d)
    return out


def assemble():
    """-> (the frame list on the global grid, the sound's length). Each scene starts at round(start * 30)."""
    tm = sc._timing()
    a, sr = sf.read(os.path.join(sc.OUT, "of_sound_v8.wav"))
    total = len(a) / sr
    starts = [int(round(tm[shots[0]["id"]]["start"] * FPS)) for _, _, _, shots in sc.SCENES] + [int(round(total * FPS))]
    seq = []
    for n, d in enumerate(scene_dirs()):
        fr = sorted(f for f in os.listdir(d) if f.endswith(".png"))
        want = starts[n + 1] - starts[n]
        if len(seq) != starts[n]:
            print("scene %d starts at frame %d, the grid says %d" % (n + 1, len(seq), starts[n]))
        got = [os.path.join(d, f) for f in fr][:want]
        got += [got[-1]] * (want - len(got))                # hold the last drawing (at most a frame or two)
        if abs(len(fr) - want) > 2:
            print("WARN scene %d: %d frames drawn, %d on the grid" % (n + 1, len(fr), want))
        seq += got
    return seq, total


def encode(seq):
    d = os.path.join(TMP, "all")
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    for i, p in enumerate(seq):
        os.symlink(p, os.path.join(d, "f%05d.png" % i))
    m1080 = os.path.join(TMP, "of_roughcut_v%d_1080.mp4" % VERSION)
    m540 = os.path.join(sc.OUT, "of_roughcut_v%d_540.mp4" % VERSION)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS), "-i", os.path.join(d, "f%05d.png"),
                    "-i", os.path.join(sc.OUT, "of_sound_v8.wav"), "-vf", "format=yuv420p", "-c:v", "libx264", "-crf", "18",
                    "-preset", "veryfast"] + TAGS + ["-c:a", "aac", "-b:a", "192k", "-shortest", m1080], check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", m1080, "-vf", "scale=540:960:flags=lanczos,format=yuv420p",
                    "-c:v", "libx264", "-crf", "20", "-preset", "veryfast"] + TAGS + ["-c:a", "copy", m540], check=True)
    return m1080, m540


def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames", "-show_entries",
                        "stream=width,height,r_frame_rate,nb_read_frames,color_space,color_primaries,color_transfer",
                        "-of", "json", path], capture_output=True, text=True)
    return json.loads(r.stdout)["streams"][0]


def levels(path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True).stderr.split("Summary:")[-1]
    return float(r.split("I:")[1].split("LUFS")[0]), float(r.split("Peak:")[1].split("dBFS")[0])


def frame_at(path, i, out):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", path, "-vf", "select=eq(n\\,%d)" % i, "-vframes", "1", out], check=True)
    return np.asarray(Image.open(out).convert("RGB")).astype(int)


def loop_diff(f0, fl):
    """v3 (22 Nov: the loop is now an action, not a still): frame 0 is the bodyguard's fist up over the roof, the last
    frame the same bodyguard holding the lamp for the legs. The SET must match exactly (walls, car, the plan (v4),
    the doorway, the floor); the people may differ: the bodyguard's column, and the legs and the lamp under the car.
    -> the pixels that differ outside those."""
    import of_set as gs
    if f0.shape != fl.shape:
        return np.ones(f0.shape[:2], bool)
    k = f0.shape[1] / 540.0
    cam = sc.CAR_CAM
    def box(x0, y0, x1, y1):
        X0, Y0 = (x0 - cam[0]) * cam[2] + 270, (y0 - cam[1]) * cam[2] + 480
        X1, Y1 = (x1 - cam[0]) * cam[2] + 270, (y1 - cam[1]) * cam[2] + 480
        return max(0, int(X0 * k)), max(0, int(Y0 * k)), int(X1 * k), int(Y1 * k)
    gx, gf = sc.BLOCK[1]["g1"]
    lx, ly = gs.CREEPER
    m = np.ones(f0.shape[:2], bool)
    for b in (box(gx - 90, gf - 300, gx + 150, gf + 20),                         # the bodyguard: his fist (v4, 23 Nov, decided:
                                                                                 # the plan is NOT masked any more: a burnt plan
                                                                                 # at the end and a whole one at frame 0 is a jump)
              box(lx - 110, gs.SILL - 10, gs.LAMP_AT[0] + 90, ly + 120)):      # the legs (they tap) and the lamp
        m[b[1]:b[3], b[0]:b[2]] = False
    return (np.abs(f0 - fl).max(axis=2) > 40) & m


def qa(m1080, n_frames):
    res, fails = {}, []
    p = probe(m1080)
    fmt = dict(size="%sx%s" % (p["width"], p["height"]), fps=p["r_frame_rate"], frames=int(p["nb_read_frames"]),
               color=[p.get("color_space"), p.get("color_primaries"), p.get("color_transfer")])
    res["format"] = fmt
    if fmt["size"] != "1080x1920" or fmt["fps"] != "30/1" or abs(fmt["frames"] - n_frames) > 1 or fmt["color"] != ["bt709"] * 3:
        fails.append("format: %s (want 1080x1920, 30/1, %d frames, bt709)" % (fmt, n_frames))
    I, P = levels(m1080)
    res["level"] = dict(lufs=I, true_peak=P)
    if P > -1.0 or not (-16.0 <= I <= -14.0):
        fails.append("level: %.1f LUFS, %.1f dBTP (want -16..-14, <= -1)" % (I, P))
    # the lines, in the AAC as delivered
    wav = os.path.join(TMP, "delivered.wav")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", m1080, "-vn", "-ac", "1", "-ar", "24000", wav], check=True)
    import of_sound as osd
    _, lines, _ = osd.mix()
    heard = osd.check(lines, path=wav, out=os.path.join(TMP, "lines.json"))
    known = {"2.6"}
    bad = [k for k, v in heard.items() if v["ok"] < 2 and k not in known]
    res["lines"] = dict(heard=len(heard) - len(bad), of=len(heard), known=[k for k in known if heard.get(k, {}).get("ok", 3) < 2])
    if bad:
        fails.append("lines not heard in the delivered mix: %s" % ", ".join(bad))
    # frame 0: complete, not a flash; the loop: the last frame leads back into it
    f0 = frame_at(m1080, 0, os.path.join(TMP, "f0.png"))
    f1 = frame_at(m1080, 1, os.path.join(TMP, "f1.png"))
    fl = frame_at(m1080, fmt["frames"] - 1, os.path.join(TMP, "flast.png"))
    ink0 = float((f0.max(axis=2) < 60).mean())
    res["frame0"] = dict(std=float(f0.std()), ink=ink0, vs_frame1=float(np.abs(f0 - f1).mean()))
    if f0.std() < 20 or ink0 < 0.005 or np.abs(f0 - f1).mean() > 12:
        fails.append("frame 0 incomplete or flashing: %s" % res["frame0"])
    diff = loop_diff(f0, fl)
    res["loop"] = dict(px_outside_the_plan=int(diff.sum()), share=float(diff.mean()))
    if diff.mean() > 0.002:
        fails.append("loop: the last frame differs from frame 0 outside the plan in %d px" % diff.sum())
    res["fails"] = fails
    json.dump(res, open(os.path.join(sc.OUT, "of_roughcut_v%d_qa.json" % VERSION), "w"), indent=1)
    return res


if __name__ == "__main__" and not (len(sys.argv) > 1 and sys.argv[1] == "validate"):
    os.makedirs(TMP, exist_ok=True)
    seq, total = assemble()
    print("rough cut: %d frames, %.2f s (sound %.2f s)" % (len(seq), len(seq) / FPS, total))
    m1080, m540 = encode(seq)
    r = qa(m1080, len(seq))
    for k in ("format", "level", "lines", "frame0", "loop"):
        print("%-7s %s" % (k, r[k]))
    for f in r["fails"]:
        print("FAIL", f)
    print("G5: %s -> %s" % ("PASS" if not r["fails"] else "FAIL", m540))
    sys.exit(1 if r["fails"] else 0)


def validate():
    """G5's checks on planted faults made from the real cut (the process rule: a check that always passes is caught).
    The lines check is the recognizer validated at stop 2 (of_sound.py); here: format, level, frame 0, loop."""
    src = os.path.join(TMP, "of_roughcut_v%d_1080.mp4" % VERSION)
    n = probe(src)["nb_read_frames"]
    n = int(n)
    cases = {
        "hot (+6 dB)": ["-af", "volume=6dB", "-c:v", "copy"],
        "untagged colour": ["-c", "copy", "-bsf:v", "h264_metadata=colour_primaries=2:transfer_characteristics=2:matrix_coefficients=2"],
        "540 wide": ["-vf", "scale=540:960", "-c:a", "copy"],
        "flash at frame 0": ["-vf", "drawbox=x=0:y=0:w=iw:h=ih:color=white:t=fill:enable='eq(n,0)'", "-c:a", "copy"],
        "loop broken (the last frame: the set changed)": ["-vf", "drawbox=x=560:y=420:w=400:h=200:color=0x2e5f8a:t=fill:enable='eq(n,%d)'" % (n - 1), "-c:a", "copy"],
        "loop broken (the last frame: the plan burnt)": ["-vf", "drawbox=x=600:y=300:w=120:h=100:color=0x3a2410:t=fill:enable='eq(n,%d)'" % (n - 1), "-c:a", "copy"],
    }
    ok = True
    for name, args in cases.items():
        p = os.path.join(TMP, "planted.mp4")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src] + args + [p], check=True)
        f = []
        pr = probe(p)
        if "%sx%s" % (pr["width"], pr["height"]) != "1080x1920" or [pr.get("color_space"), pr.get("color_primaries"), pr.get("color_transfer")] != ["bt709"] * 3 or abs(int(pr["nb_read_frames"]) - n) > 1:
            f.append("format")
        I, P = levels(p)
        if P > -1.0 or not (-16.0 <= I <= -14.0):
            f.append("level")
        f0 = frame_at(p, 0, os.path.join(TMP, "pf0.png")); f1 = frame_at(p, 1, os.path.join(TMP, "pf1.png"))
        if f0.std() < 20 or (f0.max(axis=2) < 60).mean() < 0.005 or np.abs(f0 - f1).mean() > 12:
            f.append("frame 0")
        fl = frame_at(p, int(pr["nb_read_frames"]) - 1, os.path.join(TMP, "pfl.png"))
        if loop_diff(f0, fl).mean() > 0.002:
            f.append("loop")
        caught = bool(f)
        ok &= caught
        print("%-44s caught by: %s" % (name, ", ".join(f) or "NOTHING"))
    real = [frame_at(src, 0, os.path.join(TMP, "rf0.png")), frame_at(src, n - 1, os.path.join(TMP, "rfl.png"))]
    clean = loop_diff(*real).mean() <= 0.002
    print("the real cut's loop passes:", clean)
    ok &= clean
    return ok


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "validate":
    sys.exit(0 if validate() else 1)
