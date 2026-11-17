"""THE ONBOARDING: the animatic, v2 (ob_animatic_v1.py = v1, kept): Sofia's "Oh..." is take A, chosen by ear on 17 Nov
(0.63 s, the short fall); the shot is shorter by the difference. Nothing else changed.
THE ONBOARDING: the animatic, v1. Storyboard v3 (ob_storyboard.py, untouched) held shot by shot for the lengths the
measured voice takes need (sound_ob.film_takes: 20 lines, 28.7 s spoken), with each line's bubble up while it is said.
It is a timing test, 540 x 960 at 30 fps: stills, no movement, no lip-sync; the mouths are the storyboard's.
  - a single is the storyboard tile at full frame; the four stage wides are the stage at its own size;
  - a two-shot or three-shot is the storyboard's double tile as a panel across the frame (it is not yet composed for
    9:16: that is the composition gate, later), with its bubble in the paper above it;
  - a caption is identical to its line; the robot's is in capitals, as on its screen.
TIMING is the one table: a spoken shot is (lead-in, tail) round the take's measured length, a silent shot is its hold.
  python3 ob_animatic.py timing            -> ob_timing_v1.json and a table
  python3 ob_animatic.py sheet <png>       -> every still on one sheet (bubbles on), for checking
  python3 ob_animatic.py video <mix.wav>   -> ../the-onboarding/ob_animatic_v1.mp4"""
import os
import sys
import json
import subprocess
import cairo
import kit
import ob_storyboard as sb
from kit import Ctx, INK

V = "v2"
W, H, FPS = 540, 960, 30
OUT = "../the-onboarding"
TMP = "/tmp/ob_animatic"
TAKES = "ob_voices/film/takes.json"
STAGE = {"1.1", "8.2", "8.4", "10.4"}
PAPER = (0.97, 0.96, 0.93)
PY = 250                                                   # where a panel's top sits
MONO = "DejaVu Sans Mono"

# shot -> hold in seconds (silent), or (lead-in, tail) round the measured take
TIMING = {
    "1.1": 1.5, "1.2": 1.2, "1.3": (0.15, 0.25), "1.4": 0.8,
    "2.1": (0.30, 0.20), "2.2": (0.50, 0.25), "2.3": (0.40, 0.25), "2.4": 0.8,          # 2.2: the snap, a beat, the ruling
    "3.1": (0.25, 0.45), "3.2": (0.20, 0.30), "3.3": (0.25, 0.35), "3.4": 0.8, "3.5": 0.7, "3.6": 0.9,
    "3.7": (0.40, 0.40), "3.8": 1.1, "3.9": 1.1, "3.10": 1.0, "3.11": 0.9, "3.12": (0.25, 0.25),
    "4.1": (0.20, 0.30), "4.2": 1.1, "4.3": (0.35, 0.25), "4.4": 1.1, "4.5": 1.5, "4.6": 0.8,
    "5.1": 1.1, "5.2": 0.7, "5.3": 1.3, "5.4": (0.25, 0.25), "5.5": (0.12, 0.45), "5.6": 0.8,
    "6.1": 1.1, "6.2": (0.45, 0.35), "6.3": 0.5, "6.4": 0.9, "6.5": (0.20, 0.25), "6.6": 0.7, "6.7": 1.2,
    "6.8": (0.25, 0.35), "6.9": 0.7,
    "7.1": 1.0, "7.2": 0.9, "7.3": (0.15, 0.25), "7.4": 0.8,
    "8.1": (0.15, 0.25), "8.2": 1.2, "8.3": (0.20, 0.30), "8.4": 1.2, "8.5": 1.2,
    "9.1": 4.0,
    "10.1": 1.1, "10.2": 1.0, "10.3": 1.3, "10.4": (1.00, 0.80),                         # the door, the stamp, the ruling
}
# shot -> (who, box left, box top, tip x, tip y, size): where the bubble stands and where its tail ends
BUBBLES = {
    "1.3": ("CLIENT", None, 48, 250, 158, 32), "2.1": ("DON", None, 268, 434, 372, 28),
    "2.2": ("ROBOT", None, 270, 300, 462, 24), "2.3": ("DON", None, 200, 298, 332, 32),
    "3.1": ("CLIENT", 18, 160, 116, 322, 26), "3.2": ("SOFIA", None, 60, 200, 205, 28),
    "3.3": ("CLIENT", None, 50, 254, 152, 32), "3.7": ("SOFIA", 270, 215, 226, 252, 36),
    "3.12": ("CLIENT", None, 40, 258, 216, 28), "4.1": ("DON", None, 150, 270, 336, 28),
    "4.3": ("DON", 207, 268, 434, 372, 26), "5.4": ("CLIENT", None, 70, 264, 214, 28),
    "5.5": ("DON", None, 230, 272, 348, 34), "6.2": ("SOFIA", None, 175, 408, 276, 30),
    "6.5": ("CLIENT", None, 45, 270, 156, 32), "6.8": ("SOFIA", 60, 50, 536, 100, 28),      # she is out of frame, right
    "7.3": ("ROBOT", 18, 300, 350, 400, 26), "8.1": ("ROBOT", None, 36, 276, 168, 24),
    "8.3": ("DON", None, 255, 258, 428, 32), "10.4": ("ROBOT", 18, 850, 212, 808, 24),     # on the floor: the door keeps its stamp
}
FIT = {"3.2": 0.78, "5.4": 0.82}


def timing():
    """[{shot, t0, d, f0, n, line: {who, text, t0, t1}}], on the 30 fps grid; the film's length."""
    tk = json.load(open(TAKES))
    out, f = [], 0
    for shot, span, what, line, fn in sb.frames(None, None):
        tm = TIMING[shot]
        if isinstance(tm, tuple):
            d = tm[0] + tk[shot]["len"] + tm[1]
        else:
            assert shot not in tk, shot
            d = tm
        n = int(round(d * FPS))
        row = dict(shot=shot, span=span, t0=round(f / float(FPS), 4), d=round(n / float(FPS), 4), f0=f, n=n, what=what)
        if isinstance(tm, tuple):
            t0 = row["t0"] + tm[0]
            row["line"] = dict(who=tk[shot]["who"], text=tk[shot]["text"], t0=round(t0, 4), t1=round(t0 + tk[shot]["len"], 4))
        out.append(row); f += n
    return out, f / float(FPS)


# ---------------------------------------------------------------- the stills
def _lines(c, text, width):
    words, rows, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if c.text_extents(t).x_advance > width and cur:
            rows.append(cur); cur = w
        else:
            cur = t
    return rows + [cur]


def bubble(k, shot, text):
    who, bx, by, tx, ty, size = BUBBLES[shot]
    c = k.c
    mono = who == "ROBOT"
    c.select_font_face(MONO if mono else kit.FONT, cairo.FONT_SLANT_NORMAL,
                       cairo.FONT_WEIGHT_BOLD if mono else cairo.FONT_WEIGHT_NORMAL)
    c.set_font_size(size)
    maxw = W - 2 * 22 - 44 if bx is None else W - 22 - bx - 44
    rows = _lines(c, text, min(maxw, 400))
    ws = [c.text_extents(r).x_advance for r in rows]
    lh = size * 1.14
    bw, bh = max(ws) + 44, len(rows) * lh + 26
    if bx is None:
        bx = tx - bw / 2
    bx = max(18, min(W - 18 - bw, bx))
    cx = max(bx + 30, min(bx + bw - 30, tx))
    if ty > by + bh:                                       # the speaker is below the box
        tail = [(cx - 13, by + bh - 3), (tx, ty), (cx + 13, by + bh - 3)]
    elif ty < by:
        tail = [(cx - 13, by + 3), (tx, ty), (cx + 13, by + 3)]
    else:                                                  # beside it
        ex = bx + 3 if tx < bx else bx + bw - 3
        yy = max(by + 16, min(by + bh - 16, ty))
        tail = [(ex, yy - 11), (tx, ty), (ex, yy + 11)]
    kit.cut(k, tail, (1, 1, 1))
    kit.cut(k, kit.rough_rect_pts(k, bx, by, bw, bh, 900 + len(text), j=1.6), (1, 1, 1))
    c.set_source_rgb(1, 1, 1); c.move_to(*tail[0]); c.line_to(*tail[1]); c.line_to(*tail[2]); c.close_path(); c.fill()
    c.select_font_face(MONO if mono else kit.FONT, cairo.FONT_SLANT_NORMAL,
                       cairo.FONT_WEIGHT_BOLD if mono else cairo.FONT_WEIGHT_NORMAL)
    c.set_font_size(size); c.set_source_rgb(*INK)
    for i, (r, w) in enumerate(zip(rows, ws)):
        c.move_to(bx + (bw - w) / 2, by + 13 + lh * (i + 0.80)); c.show_text(r)
    return bx, by, bw, bh


def still(i, with_bubble):
    """Shot i as a 540 x 960 surface."""
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    c = cairo.Context(surf)
    k = Ctx(c, 0)
    shot, span, what, line, fn = sb.frames(k, c)[i]
    if shot in STAGE:
        c.set_source_rgb(*kit.WALL); c.paint()
        fn(0, 0, W, sb.F + 20)                             # the stage at its own size
    elif span == 1:
        c.set_source_rgb(*kit.WALL); c.paint()
        f = FIT.get(shot, 1.0)                              # a speaker who fills the tile is set back, for the bubble
        c.save(); c.translate(W / 2.0, H); c.scale(f * W / float(sb.FW), f * W / float(sb.FW))
        c.translate(-sb.FW / 2.0, -sb.FH); fn(0, 0, sb.FW, sb.FH); c.restore()
    else:
        s = W / float(sb.WIDE)
        c.set_source_rgb(*PAPER); c.paint()
        c.save(); c.translate(0, PY); c.scale(s, s)
        c.rectangle(0, 0, sb.WIDE, sb.FH); c.clip()
        c.set_source_rgb(*kit.WALL); c.paint()
        fn(0, 0, sb.WIDE, sb.FH)
        c.restore()
        c.set_source_rgb(*INK); c.set_line_width(2.5)
        for y in (PY, PY + sb.FH * s):
            c.move_to(0, y); c.line_to(W, y); c.stroke()
    if with_bubble and line and shot in BUBBLES:
        bubble(k, shot, line.split(": ", 1)[1].strip('"'))
    c.select_font_face("Inter", 0, 1); c.set_font_size(15)                         # the shot's number, for notes
    c.set_source_rgba(1, 1, 1, 0.75); c.rectangle(14, H - 40, 16 + c.text_extents(shot).x_advance, 24); c.fill()
    c.set_source_rgb(0.35, 0.40, 0.50); c.move_to(22, H - 22); c.show_text(shot)
    return surf


def sheet(out, bubbles=True, cols=11, s=0.25):
    fr = sb.frames(None, None)
    rows = (len(fr) + cols - 1) // cols
    tw, th = int(W * s), int(H * s)
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, cols * (tw + 4) + 4, rows * (th + 4) + 4)
    c = cairo.Context(surf); c.set_source_rgb(0.2, 0.2, 0.2); c.paint()
    for i in range(len(fr)):
        im = still(i, bubbles)
        c.save(); c.translate(4 + (i % cols) * (tw + 4), 4 + (i // cols) * (th + 4)); c.scale(s, s)
        c.set_source_surface(im, 0, 0); c.paint(); c.restore()
    surf.write_to_png(out)


# ---------------------------------------------------------------- the video
def _encode(png, n, out):
    tmp = out[:-4] + ".tmp.mp4"
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", png, "-vf",
                           "format=yuv420p,loop=-1:1,trim=end_frame=%d" % n, "-c:v", "libx264", "-crf", "18", "-preset",
                           "veryfast", "-pix_fmt", "yuv420p", "-r", str(FPS), "-frames:v", str(n), tmp])
    os.rename(tmp, out)


def video(mix, out=None):
    out = out or "%s/ob_animatic_%s.mp4" % (OUT, V)
    os.makedirs(TMP, exist_ok=True)
    rows, total = timing()
    parts = []
    for i, r in enumerate(rows):
        segs = [(False, r["n"])]
        if "line" in r and r["shot"] in BUBBLES:
            a = int(round((r["line"]["t0"] - r["t0"]) * FPS)) - 1                  # up a frame early, down 0.25 s after
            b = min(r["n"], int(round((r["line"]["t1"] - r["t0"] + 0.25) * FPS)))
            a = max(0, a)
            segs = [(False, a), (True, b - a), (False, r["n"] - b)]
        for j, (bub, n) in enumerate(segs):
            if n <= 0:
                continue
            png = "%s/%02d_%d.png" % (TMP, i, j); mp4 = "%s/%02d_%d.mp4" % (TMP, i, j)
            still(i, bub).write_to_png(png)
            _encode(png, n, mp4)
            parts.append(mp4)
    open(TMP + "/list.txt", "w").write("".join("file '%s'\n" % p for p in parts))
    silent = TMP + "/silent.mp4"
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", TMP + "/list.txt",
                           "-c", "copy", silent])
    tmp = out[:-4] + ".tmp.mp4"
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-i", mix, "-map", "0:v", "-map", "1:a",
                           "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", tmp])
    os.rename(tmp, out)
    print("wrote", out, "%.2f s" % total, len(parts), "parts")
    return out


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "timing"
    if cmd == "timing":
        rows, total = timing()
        json.dump(dict(total=round(total, 4), fps=FPS, shots=rows), open("ob_timing_%s.json" % V, "w"), indent=1)
        beat = None
        for r in rows:
            b = r["shot"].split(".")[0]
            if b != beat:
                beat = b
                print("-- beat %s at %5.2f s" % (b, r["t0"]))
            ln = r.get("line")
            print("%-5s %5.2f  %4.2f s  %s" % (r["shot"], r["t0"], r["d"], ("%s %.2f-%.2f  %s" % (
                ln["who"], ln["t0"], ln["t1"], ln["text"])) if ln else ""))
        print("total %.2f s, %d shots, spoken %.2f s" % (total, len(rows), sum(r["line"]["t1"] - r["line"]["t0"]
                                                                              for r in rows if "line" in r)))
    elif cmd == "sheet":
        sheet(sys.argv[2], bubbles=len(sys.argv) < 4)
    elif cmd == "video":
        video(sys.argv[2])
