"""CUSTOMER SUCCESS (episode 11): animatic v1, storyboard v5 timed to the voice takes (cs_voices/film_v3).
Each frame is held for its board length or, where it carries lines, for the lines (0.25 s lead, 0.2 s between two
lines in one shot, 0.35 s of air after). The spoken line is a caption card at the top (y 96, the narration's place,
clear of the platforms' bottom quarter); the phones' buzz under 1.1 and 6.6. Loudness to about -15 LUFS on the AAC.
  python3 cs_animatic.py [out_dir]  ->  cs_animatic_v1.mp4 and cs_animatic_timing_v1.json"""
import json
import os
import subprocess
import sys
import cairo
import numpy as np
import soundfile as sf
import cs_board5 as b5

V = "v1"
BOARD = ["cs_board_v5"]
SR = 48000
TAKES = "cs_voices/film_v3"
LEAD, GAP, TAIL = 0.25, 0.20, 0.35
LINES = {"1.4": ("1.4r", "1.4d"), "2.1": ("2.1",), "2.2": ("2.2",), "3.1": ("3.1r", "3.1d"), "3.3": ("3.3",),
         "3.5": ("3.5",), "4.4": ("4.4",), "5.1": ("5.1",), "5.4a": ("5.4d",), "6.5": ("6.5",)}
WHO = {"ROBOT": "ROBOT", "DON": "DON", "CLIENT": "CLIENT", "SOFIA": "SOFÍA"}


def timing():
    meta = json.load(open(TAKES + "/takes.json"))
    rows, t = [], 0.0
    for shot, ln, fn, note in b5.SHOTS:
        keys = LINES.get(shot, ())
        need = (LEAD + sum(meta[k]["len"] for k in keys) + GAP * (len(keys) - 1) + TAIL) if keys else 0.0
        d = round(max(ln, need) * 30) / 30.0
        lines, tt = [], t + LEAD
        for k in keys:
            m = meta[k]
            lines.append({"key": k, "who": m["who"], "text": m["text"], "t0": round(tt, 3), "t1": round(tt + m["len"], 3)})
            tt += m["len"] + GAP
        rows.append({"shot": shot, "start": round(t, 3), "len": d, "lines": lines})
        t += d
    return rows, t


def caption(png, text, who):
    """The line as a card at the top, under the bar (y 96)."""
    s = cairo.ImageSurface.create_from_png(png)
    o = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(o)
    c.set_source_surface(s, 0, 0); c.paint()
    c.select_font_face("Inter", 0, 1); c.set_font_size(24)
    label = "%s: %s" % (WHO.get(who, who), text)
    words, rows_, cur = label.split(), [], ""
    for w in words:
        if c.text_extents((cur + " " + w).strip()).x_advance > 460:
            rows_.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    rows_.append(cur)
    h = 20 + 32 * len(rows_)
    c.set_source_rgba(1, 1, 1, 0.94); c.rectangle(30, 96, 480, h); c.fill()
    c.set_source_rgb(0.1, 0.1, 0.12); c.set_line_width(2); c.rectangle(30, 96, 480, h); c.stroke()
    for i, r in enumerate(rows_):
        c.move_to(44, 96 + 36 + 32 * i); c.show_text(r)
    return o


def buzz(dur=1.0):
    t = np.arange(int(dur * SR)) / SR
    env = ((t * 6) % 1 < 0.6).astype(float) * np.minimum(1, (dur - t) * 8)
    return 0.25 * np.sign(np.sin(2 * np.pi * 160 * t)) * env * (0.6 + 0.4 * np.sin(2 * np.pi * 7 * t))


def main(out_dir):
    rows, total = timing()
    tmp = "/tmp/cs_anim"; os.makedirs(tmp, exist_ok=True)
    board = os.path.join(out_dir, BOARD[0])
    # pictures: one still per caption state, joined with the concat demuxer
    lst = open(tmp + "/list.txt", "w")
    n = 0
    for r in rows:
        png = "%s/cs_board_%s.png" % (board, r["shot"])
        segs, t = [], r["start"]
        for ln in r["lines"]:
            if ln["t0"] - 0.05 > t:
                segs.append((t, ln["t0"] - 0.05, None))
            segs.append((max(t, ln["t0"] - 0.05), min(r["start"] + r["len"], ln["t1"] + 0.25), ln))
            t = min(r["start"] + r["len"], ln["t1"] + 0.25)
        if t < r["start"] + r["len"] - 1e-6:
            segs.append((t, r["start"] + r["len"], None))
        for a, b, ln in segs:
            if b - a < 1e-3:
                continue
            p = "%s/f%03d.png" % (tmp, n); n += 1
            (caption(png, ln["text"], ln["who"]) if ln else cairo.ImageSurface.create_from_png(png)).write_to_png(p)
            lst.write("file '%s'\nduration %.4f\n" % (p, b - a))
    lst.write("file '%s'\n" % p); lst.close()
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", tmp + "/list.txt",
                    "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                    "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", tmp + "/v.mp4"], check=True)
    # sound
    a = np.zeros(int((total + 0.5) * SR))
    for r in rows:
        for ln in r["lines"]:
            x, sr = sf.read("%s/%s.wav" % (TAKES, ln["key"]))
            p = int(ln["t0"] * SR); a[p:p + len(x)] += x[:len(a) - p]
    for shot in ("1.1", "6.6"):
        r = [q for q in rows if q["shot"] == shot][0]
        z = buzz(min(1.2, r["len"])); p = int((r["start"] + 0.05) * SR); a[p:p + len(z)] += z[:len(a) - p]
    sf.write(tmp + "/a.wav", (a / max(1e-9, np.abs(a).max()) * 0.7).astype(np.float32), SR)
    r_ = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", tmp + "/a.wav", "-af", "ebur128", "-f", "null", "-"],
                        capture_output=True, text=True)
    cur = float([x for x in r_.stderr.split("\n") if "I:" in x][-1].split("I:")[1].split("LUFS")[0])
    out = os.path.join(out_dir, "cs_animatic_%s.mp4" % V)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp + "/v.mp4", "-i", tmp + "/a.wav", "-map", "0:v", "-map", "1:a",
                    "-af", "volume=%.2fdB,alimiter=limit=0.60:attack=2:release=40:level=disabled" % (-11.5 - cur),
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", tmp + "/out.part.mp4"], check=True)
    os.replace(tmp + "/out.part.mp4", out)
    shots = [{"shot": r["shot"] + ("" if i == 0 else "_%d" % i), "line": dict(ln, who=ln["who"])}
             for r in rows for i, ln in enumerate(r["lines"])]
    json.dump({"total": total, "rows": rows, "shots": shots}, open("cs_animatic_timing_%s.json" % V, "w"), indent=1)
    print("wrote", out, "%.2f s" % total)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "v2"]
    if "v2" in sys.argv[1:]:                                             # animatic v2: storyboard v6
        import cs_board6 as b6
        V = "v2"; BOARD[0] = "cs_board_v6"; b5.SHOTS = b6.SHOTS
    if "v3" in sys.argv[1:]:                                             # animatic v3: storyboard v7
        import cs_board7 as b7
        args = [a for a in args if a != "v3"]
        V = "v3"; BOARD[0] = "cs_board_v7"; b5.SHOTS = b7.SHOTS
    main(args[0] if args else "../customer-success")
