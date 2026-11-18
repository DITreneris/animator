"""v1, pinned: the motion test as first shown (on2_motion_test_v1.mp4). on2_motion.py is current.
OFFICE NOIR 2: the motion test, v1. Beats 01 and 02 of script v2 (the taxi, the street), animated. 17 Nov.
What it tests before the whole film is animated: the walk from behind, the run in the long gown (a cycle of four
drawings), his hand coming in, the wrap, the rain, the lamp, and the narration as a line of italics at the bottom.
Twelve drawings a second, held; 30 frames a second. The noir pass and the light are the storyboard's.
Narration: kind A for now (the audition decides). Sound: the first film's jazz, rain, her heels, the compact.
Writes ../office-noir-2/on2_motion_test_v1.mp4 (540 x 960) and on2_motion_timing_v1.json.
  KOKORO_DIR=/tmp/kokoro python3 on2_motion.py [A|B|C]"""
import json
import math
import os
import subprocess
import sys
import cairo
import numpy as np
import soundfile as sf

os.environ.setdefault("KOKORO_DIR", "/tmp/kokoro")
import on2_board_v5 as b
import on2_sound as snd
import engine_on as eng
import noir2_cast_v9 as n
import client_ob as co
from kit import Ctx, INK, ellipse, rect, cut

V = "v1"
W, H, FPS = 540, 960, 30
SAFE = (18, 96, 522, 820)
LEAD, TAIL = 0.25, 0.42
PLAN = [("1.1", 2.0, "n1"), ("1.2", 2.0, None), ("2.1", 1.5, "n2"), ("2.2", 1.0, None), ("2.3", 1.0, None), ("2.4", 1.5, None),
        ("2.5", 1.0, None), ("2.6", 2.0, "n3")]
TEXT = dict(snd.NARR)


def ease(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def lerp(a, c, x):
    return a + (c - a) * min(1.0, max(0.0, x))


def rain(k, t, floor=None):
    """Streaks that fall: each one drops the height of the frame in about two thirds of a second."""
    cc = k.c
    cc.set_source_rgba(1, 1, 1, 0.20); cc.set_line_width(1.6); cc.set_line_cap(1)
    for i in range(30):
        x0 = (i * 97) % 580 - 20
        y = ((i * 173) % 1000 + t * 1500) % 1040 - 60
        cc.move_to(x0 - y * 0.26 + 120, y); cc.line_to(x0 - y * 0.26 + 111, y + 34); cc.stroke()


def splash(k, x, y, a):
    """Rings where something met the wet stones. a: 0..1 through its life."""
    if a <= 0 or a >= 1:
        return
    cc = k.c
    cc.set_source_rgba(1, 1, 1, 0.7 * (1 - a)); cc.set_line_width(2.4)
    for r in (16 + 40 * a, 8 + 22 * a):
        cc.save(); cc.translate(x, y); cc.scale(r, r * 0.3); cc.new_path(); cc.arc(0, 0, 1, 0, 2 * math.pi); cc.restore(); cc.stroke()


# ---------------------------------------------------------------- the shots
def m1_1(k, tl):
    b.street(k, 668, (440, 150), rain=False)
    door = ease((tl - 0.25) / 0.34)
    n.taxi(k, 150, 716, 2.5, door=door)
    if tl >= 9 / 12.0:
        y = 716 - (70 if tl < 10 / 12.0 else 26 if tl < 11 / 12.0 else 0)
        b.red_shoe(k, 300, y, 3.4)
    splash(k, 330, 722, (tl - 11 / 12.0) / 0.5)
    rain(k, tl)


def m1_2(k, tl):
    b.street(k, 690, (430, 150), rain=False)
    x = 40 - 640 * ease((tl - 0.5) / 1.1) ** 1.6
    n.taxi(k, x, 730, 1.5, door=0.0)
    rise = 12 if tl < 1 / 12.0 else 5 if tl < 2 / 12.0 else 0
    look = (0.1, -0.2) if tl < 1.25 else (-0.7, 0.0)
    n.star(k, 350, 800 + rise, 1.9, "g_pose", "interested", look, sparkle=1.0 if int(tl * 12) % 6 < 3 else 0.2)
    rain(k, tl + 2)


def m2_1(k, tl, dur=2.75):
    cc = k.c
    b.street(k, 600, (440, 140), rain=False)
    p = tl / dur
    dy = 300 * (1 - ease(tl / 1.4))                                      # his shadow slides onto the stones after her
    cc.save(); cc.translate(0, dy)
    cc.set_source_rgb(*n.BLACK)
    cc.new_path(); cc.move_to(-20, 960); cc.line_to(120, 760); cc.line_to(200, 760); cc.line_to(190, 960); cc.close_path(); cc.fill()
    cc.save(); cc.translate(160, 752); cc.scale(84, 15); cc.new_path(); cc.arc(0, 0, 1, 0, 2 * math.pi); cc.restore(); cc.fill()
    cc.new_path(); cc.move_to(118, 752); cc.line_to(128, 700); cc.line_to(152, 712); cc.line_to(170, 696); cc.line_to(196, 708); cc.line_to(204, 752)
    cc.close_path(); cc.fill()
    cc.restore()
    n.star_back(k, 340, lerp(806, 772, p), lerp(1.92, 1.76, p), step=tl * 1.6)
    rain(k, tl + 4)


def m2_2(k, tl):
    cc = k.c
    cc.set_source_rgb(0.11, 0.11, 0.13); cc.paint()
    b.pool(cc, 300, 200, 420, 0.22)
    ang = 0.16 if tl < 1 / 12.0 else 0.10 if tl < 2 / 12.0 else 0.06
    n._seg(k, 330, 1000, 290, 760, 110, 96, n.KEY, 3.4)
    n.compact2(k, 270, 470, 9.0, ang, hat=tl >= 4 / 12.0)
    ellipse(k, 286, 760, 58, 52, n.KEY, 363, shadow=False, lw=3.4)


def m2_3(k, tl):
    cc = k.c
    cc.set_source_rgb(0.13, 0.13, 0.15); cc.paint()
    b.pool(cc, 380, 160, 420, 0.30)
    face = "interested" if tl < 4 / 12.0 else "real"
    n.star(k, 240, 1270 - (0 if tl < 4 / 12.0 else 6), 3.4, "g_mirror", face, (0.9, -0.1), wrap=False, mirror=True,
           sparkle=1.0 if tl >= 6 / 12.0 else 0.0)


def m2_4(k, tl):
    b.street(k, 720, None, rain=False)
    b.pool(k.c, 300, 120, 520, 0.38)
    slide = -40 * (1 - ease(tl / 0.25))
    n.shadow(k, 20 + slide, 1180, 2.5, "open", lit_hand=None, look_down=1.0)
    reach = ease((tl - 0.25) / 0.5)
    face = "real" if tl < 0.5 else "caught"
    look = (0.9, -0.1) if tl < 0.5 else (-0.6, 0.5) if tl < 0.75 else (-1.0, 0.9)
    o = n.star(k, 340, 1060, 2.6, "g_stand", face, look, wrap=False)
    lx, ly = o["hands"][0]
    ex, ey = lerp(-200, lx - 22, reach), lerp(380, ly - 52, reach)
    if tl >= 0.25:
        b.arm_in(k, ex - 320, ey - 110, ex, ey)


def m2_5(k, tl):
    cc = k.c
    cc.set_source_rgb(*b.GROUND); cc.paint()
    cc.set_source_rgb(0.20, 0.20, 0.23); cc.set_line_width(3)
    for i in range(7):
        cc.move_to(-20, 140 + i * 140); cc.line_to(560, 110 + i * 140); cc.stroke()
    cc.set_source_rgba(1, 1, 1, 0.16); cc.save(); cc.translate(250, 600); cc.scale(260, 200); cc.new_path(); cc.arc(0, 0, 1, 0, 2 * math.pi)
    cc.restore(); cc.fill()
    if tl < 2 / 12.0:                                                   # the compact, falling
        n.compact2(k, 230, 330 + 1500 * tl, 3.6, 0.9 + tl * 6)
    else:
        g = ease((tl - 2 / 12.0) / 0.34)
        cc.save(); cc.translate(220, 640); cc.scale(0.35 + 0.65 * g, 0.35 + 0.65 * g); cc.translate(-220, -640)
        n.powder_puff(k, 220, 640, 5.0)
        cc.restore()
    if 4 / 12.0 <= tl < 6 / 12.0:
        b.red_shoe(k, 330, 610, 3.6)
    elif 6 / 12.0 <= tl < 8 / 12.0:
        b.red_shoe(k, 460, 470, 3.2)
        n.footprints(k, 300, 700, 4.2, n=1, step=30)
    elif tl >= 8 / 12.0:
        n.footprints(k, 300, 700, 4.2, n=1, step=30)
        n.footprints(k, 420, 560, 3.6, n=1, step=30)


def cloth(k, x, y, s, ang):
    cc = k.c
    cc.save(); cc.translate(x, y); cc.rotate(ang); cc.scale(s, s)
    n._cloth(cc, [("M", -5, 0), ("C", -2, -3, 2, -3, 5, 0), ("C", 20, 14, 26, 50, 20, 88), ("C", 18, 104, 12, 114, 8, 122),
                  ("C", 4, 110, 0, 100, -4, 104), ("C", -8, 110, -12, 116, -16, 124), ("C", -22, 104, -26, 50, -5, 0)])
    n._curve(cc, (4, 6, 16, 22, 20, 56, 14, 96), n.WRAP_PALE, 1.6)
    cc.restore()


def m2_6(k, tl, dur=3.5):
    cc = k.c
    b.street(k, 580, (440, 140), rain=False)
    cc.set_source_rgba(1, 1, 1, 0.26); cc.save(); cc.translate(150, 690); cc.scale(190, 96); cc.new_path(); cc.arc(0, 0, 1, 0, 2 * math.pi)
    cc.restore(); cc.fill()
    p = tl / dur
    x, y, s = lerp(250, 470, p), lerp(720, 640, p), lerp(1.42, 1.0, p)
    for i in range(int(tl / 0.5) + 1):                                  # her prints: one every other stride, apart
        q = (i * 0.5) / dur
        n.footprints(k, lerp(250, 470, q) - 46, lerp(720, 640, q) + 6 + (7 if i % 2 else -7), lerp(2.2, 1.5, q), n=1, step=30)
    ph = int(tl * 8) % 4
    n.star(k, x, y - (7 if ph in (1, 3) else 0), s, "g_run3" if ph < 2 else "g_run3b", "caught", (-0.9, 0.0), lean=7 + (2 if ph % 2 else 0),
           lag=(-14 + (5 if ph % 2 else 0), -4), wrap=False, run=True, phase=ph)
    # the wrap: off her shoulders, down to the stones; his hand lifts it, shakes it, lets it go
    if tl < 0.75:                                                       # all of this stays above the narration's line
        f = tl / 0.75
        n.wrap_flying(k, lerp(250, 124, f), lerp(470, 716, f * f), 1.5, lerp(0.5, 0.05, f))
    elif tl < 1.25 or tl >= 3.0:
        n.wrap_flying(k, 124, 722, 1.5, 0.05)
    if 1.0 <= tl < 3.25:
        if tl < 1.25:
            hx, hy = lerp(-60, 124, (tl - 1.0) / 0.25), lerp(620, 712, (tl - 1.0) / 0.25)
        elif tl < 1.67:
            hx, hy = 130, lerp(712, 500, ease((tl - 1.25) / 0.42))
        elif tl < 3.0:
            hx, hy = 130, 500
        else:
            hx, hy = lerp(130, -80, (tl - 3.0) / 0.25), lerp(500, 470, (tl - 3.0) / 0.25)
        b.arm_in(k, hx - 180, hy - 80, hx, hy, 60)
        if 1.25 <= tl < 3.0:
            shake = (0.16 if int(tl * 12) % 2 else -0.16) if 1.67 <= tl < 2.5 else 0.0
            if tl < 2.75:
                cloth(k, hx + 20, hy + 10, 1.75, shake)
            else:                                                       # let go: it falls
                cloth(k, 150, lerp(520, 640, (tl - 2.75) / 0.25), 1.75, 0.5)
    rain(k, tl + 7)


SHOTS = {"1.1": (m1_1, 0, lambda cc: b.shade(cc, -1, 0.45)), "1.2": (m1_2, 0, lambda cc: b.shade(cc, -1, 0.50)), "2.1": (m2_1, 0, None),
         "2.2": (m2_2, 0, None), "2.3": (m2_3, 0, lambda cc: b.shade(cc, -1, 0.55)), "2.4": (m2_4, -0.07, None), "2.5": (m2_5, 0, None),
         "2.6": (m2_6, 0, lambda cc: b.shade(cc, -1, 0.35))}


def timing(kind):
    meta = json.load(open(snd.TAKES + "/takes.json"))
    rows, t = [], 0.0
    for shot, planned, key in PLAN:
        need = (LEAD + meta["%s_%s" % (key, kind)]["len"] + TAIL) if key else 0.0
        d = math.ceil(max(planned, need) * 12 - 1e-6) / 12.0
        row = {"shot": shot, "start": round(t, 4), "len": round(d, 4)}
        if key:
            row["line"] = {"who": "N", "text": TEXT[key], "t0": round(t + LEAD, 3), "t1": round(t + LEAD + meta["%s_%s" % (key, kind)]["len"], 3)}
        rows.append(row); t += d
    return rows, t


def caption(cc, text):
    cc.select_font_face("Inter", cairo.FONT_SLANT_ITALIC, cairo.FONT_WEIGHT_BOLD); cc.set_font_size(23)
    rows, line = [], ""
    for wd in text.split():
        trial = (line + " " + wd).strip()
        if cc.text_extents(trial).x_advance > SAFE[2] - SAFE[0] - 36 and line:
            rows.append(line); line = wd
        else:
            line = trial
    rows.append(line)
    hh = len(rows) * 30 + 22; y0 = SAFE[3] - hh
    cc.set_source_rgba(0.04, 0.04, 0.06, 0.82); cc.rectangle(SAFE[0], y0, SAFE[2] - SAFE[0], hh); cc.fill()
    cc.set_source_rgb(1, 1, 1)
    for j, ln in enumerate(rows):
        e = cc.text_extents(ln); cc.move_to((W - e.x_advance) / 2, y0 + 33 + j * 30); cc.show_text(ln)


def frame(row, tl, t):
    fn, tilt, post = SHOTS[row["shot"]]
    sf_ = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    cc = cairo.Context(sf_); cc.set_source_rgb(*b.NIGHT); cc.paint()
    if tilt:
        cc.translate(W / 2, H / 2); cc.rotate(tilt); cc.scale(1.10, 1.10); cc.translate(-W / 2, -H / 2)
    k = Ctx(cc, int(round(t * 12)) % 3)
    if row["shot"] in ("2.1", "2.6"):
        fn(k, tl, row["len"])
    else:
        fn(k, tl)
    eng.accent_pass(sf_, n.ACCENTS2)
    cc = cairo.Context(sf_)
    if post:
        post(cc)
    b.vignette(cc)
    ln = row.get("line")
    if ln and ln["t0"] - 0.05 <= t <= ln["t1"] + 0.30:
        caption(cc, ln["text"])
    return sf_


def main(kind="A", folder="../office-noir-2"):
    rows, total = timing(kind)
    json.dump({"kind": kind, "total": total, "shots": rows}, open("on2_motion_timing_%s.json" % V, "w"), indent=1)
    tmp = "/tmp/on2/motion"; os.makedirs(tmp, exist_ok=True)
    nfr = int(round(total * FPS))
    enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", "%dx%d" % (W, H), "-r", str(FPS),
                            "-i", "-", "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p", "-colorspace", "bt709",
                            "-color_primaries", "bt709", "-color_trc", "bt709", tmp + "/video.part.mp4"], stdin=subprocess.PIPE)
    last, buf = None, None
    for f in range(nfr):
        t = f / float(FPS)
        d12 = math.floor(t * 12 + 1e-6)                                  # which drawing: twelve a second, held
        row = [r for r in rows if r["start"] <= d12 / 12.0 + 1e-6][-1]
        if d12 != last:
            tl = d12 / 12.0 - row["start"]
            buf = bytes(frame(row, max(0.0, tl), d12 / 12.0).get_data()); last = d12
        enc.stdin.write(buf)
    enc.stdin.close(); enc.wait()
    os.replace(tmp + "/video.part.mp4", tmp + "/video.mp4")
    wav, spans = snd.motion_mix([(r["shot"], r["start"], r["len"]) for r in rows], total, kind, tmp + "/mix.wav")
    out = "%s/on2_motion_test_%s.mp4" % (folder, V)
    # one constant gain to about -14.5 LUFS, then the final file is measured
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", wav, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True)
    cur = float([x for x in r.stderr.split("\n") if "I:" in x][-1].split("I:")[1].split("LUFS")[0])
    gain = -13.5 - cur
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp + "/video.mp4", "-i", wav, "-map", "0:v", "-map", "1:a", "-af",
                    "volume=%.2fdB,alimiter=limit=0.60:attack=2:release=40:level=disabled" % gain, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                    "-shortest", tmp + "/out.part.mp4"], check=True)
    os.replace(tmp + "/out.part.mp4", out)
    return out, rows, total, nfr


if __name__ == "__main__":
    out, rows, total, nfr = main(sys.argv[1] if len(sys.argv) > 1 else "A")
    print("wrote", out, "%.2f s" % total, nfr, "frames")
